"""Distribuições do modelo estocástico (ADR-002).

- Beta-PERT: perda PRIMÁRIA por evento (RF08) — três pontos, limitada.
- Lognormal: perda SECUNDÁRIA por evento (TCC1 §3.6, item 3) — cauda longa, com teto.
- Poisson: número de eventos de perda no ano (LEF).
Todas as funções são vetorizadas (NumPy) para rodar 10.000 iterações em milissegundos (RNF06).
"""

from __future__ import annotations

import math

import numpy as np


# ------------------------------------------------------------------------------------------------ Beta-PERT
def pert_parametros(minimo: float, mais_provavel: float, maximo: float, lam: float = 4.0) -> tuple[float, float]:
    """α e β da Beta-PERT: α = 1 + λ(m − a)/(b − a),  β = 1 + λ(b − m)/(b − a)."""
    if not minimo <= mais_provavel <= maximo:
        raise ValueError(f"PERT exige mín ≤ mais provável ≤ máx, recebido {(minimo, mais_provavel, maximo)}")
    amplitude = maximo - minimo
    if amplitude == 0:
        raise ValueError("PERT degenerada (mín = máx)")
    return 1 + lam * (mais_provavel - minimo) / amplitude, 1 + lam * (maximo - mais_provavel) / amplitude


def pert_media(minimo: float, mais_provavel: float, maximo: float, lam: float = 4.0) -> float:
    """Média analítica: (a + λm + b) / (λ + 2). Com λ = 4: (a + 4m + b) / 6."""
    return (minimo + lam * mais_provavel + maximo) / (lam + 2)


def amostrar_pert(rng: np.random.Generator, minimo: float, mais_provavel: float, maximo: float,
                  n: int, lam: float = 4.0) -> np.ndarray:
    if maximo == minimo:
        return np.full(n, float(minimo))
    alfa, beta = pert_parametros(minimo, mais_provavel, maximo, lam)
    return minimo + (maximo - minimo) * rng.beta(alfa, beta, size=n)


# ------------------------------------------------------------------------------------------------ Lognormal
def lognormal_parametros(mediana: float, p95: float, z95: float = 1.6448536) -> tuple[float, float]:
    """μ e σ a partir de dois pontos intuitivos: μ = ln(mediana); σ = [ln(p95) − ln(mediana)] / z₀,₉₅."""
    if mediana <= 0 or p95 <= mediana:
        raise ValueError(f"lognormal exige 0 < mediana < p95, recebido mediana={mediana}, p95={p95}")
    mu = math.log(mediana)
    return mu, (math.log(p95) - mu) / z95


def lognormal_media(mu: float, sigma: float) -> float:
    """Média analítica (sem teto): exp(μ + σ²/2)."""
    return math.exp(mu + sigma**2 / 2)


def amostrar_lognormal(rng: np.random.Generator, mu: float, sigma: float, n: int,
                       teto: float | None = None) -> np.ndarray:
    """Sorteios lognormais; com `teto`, valores acima são limitados a ele (censura à direita).

    O teto representa um limite econômico plausível (ex.: 100% do faturamento anual) e evita que a cauda
    infinita da lognormal produza perdas sem sentido para o porte da empresa.
    """
    x = rng.lognormal(mu, sigma, size=n)
    return np.minimum(x, teto) if teto is not None else x


# ------------------------------------------------------------------------------------------------ Poisson
def prob_ao_menos_um(lef: float) -> float:
    """P(N ≥ 1) para N ~ Poisson(LEF): 1 − e^(−LEF). É a "chance de acontecer no ano" do mapa de calor."""
    return 1 - math.exp(-lef)
