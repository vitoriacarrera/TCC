"""Magnitude da perda por evento (FAIR: Perda Primária + Perda Secundária).

Transforma os coeficientes declarados em `audit/cenarios.yaml` em valores em R$ para uma empresa concreta,
e sorteia perdas por evento: Beta-PERT para a primária e Bernoulli × Lognormal para a secundária.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..catalog.models import Cenario, ParametrosModelo, Setor
from .distribuicoes import amostrar_lognormal, amostrar_pert, lognormal_parametros


@dataclass(frozen=True)
class Contexto:
    """Dados da empresa coletados no Módulo de Entrada (RF02, RF05)."""

    faturamento_anual: float        # Receita Operacional Bruta anual (pergunta `receita_operacional_bruta`)
    custo_hora_parada: float
    registros_pessoais: int

    def __post_init__(self) -> None:
        if self.faturamento_anual <= 0:
            raise ValueError("faturamento_anual deve ser positivo")
        if self.custo_hora_parada < 0 or self.registros_pessoais < 0:
            raise ValueError("contexto com valores negativos")


def pontos_primaria(cen: Cenario, ctx: Contexto) -> tuple[float, float, float]:
    """(mín, mais provável, máx) da perda primária em R$."""
    pp = cen.perda_primaria
    return tuple(
        pp.horas_parada[i] * ctx.custo_hora_parada + pp.pct_faturamento[i] * ctx.faturamento_anual + pp.fixo[i]
        for i in range(3)
    )  # type: ignore[return-value]


def pontos_secundaria(cen: Cenario, ctx: Contexto, setor: Setor) -> tuple[float, float, float]:
    """(mediana, p95, teto) da perda secundária em R$, dado que ela ocorre."""
    ps = cen.perda_secundaria
    custo_registro = ctx.registros_pessoais * setor.custo_registro   # tipo de dado não pesa (revisão C-DADO)

    def valor(ponto) -> float:
        return ponto.por_registro * custo_registro + ponto.pct_faturamento * ctx.faturamento_anual + ponto.fixo

    return valor(ps.mediana), valor(ps.p95), ps.teto_pct_faturamento * ctx.faturamento_anual


def fatores_magnitude(cen: Cenario, ctx: Contexto, pm: ParametrosModelo,
                      maturidade_resposta: float) -> tuple[float, float]:
    """(fator da perda primária, fator da perda secundária) pela preparação (revisão MAG, ADR-014).

    redução = maxima × maturidade de resposta. Para "horas_parada", a redução vale só para a parte da perda primária
    que é receita perdida (horas × custo da hora): como a média da Beta-PERT é linear nos três pontos, o fator
    multiplicativo 1 − redução × (média das horas em R$ / média total) preserva exatamente a perda média.
    """
    rm = cen.reducao_magnitude
    r = rm.maxima * maturidade_resposta
    if rm.componente == "primaria":
        return 1 - r, 1.0
    if rm.componente == "secundaria":
        return 1.0, 1 - r
    lam = pm.pert_lambda
    a, m, b = pontos_primaria(cen, ctx)
    h = [x * ctx.custo_hora_parada for x in cen.perda_primaria.horas_parada]
    media, media_h = a + lam * m + b, h[0] + lam * h[1] + h[2]
    return (1 - r * media_h / media if media > 0 else 1.0), 1.0


def amostrar_perdas_evento(rng: np.random.Generator, cen: Cenario, ctx: Contexto, setor: Setor,
                           pm: ParametrosModelo, n: int,
                           fatores: tuple[float, float] = (1.0, 1.0)) -> tuple[np.ndarray, np.ndarray]:
    """Sorteia `n` eventos de perda e devolve (perda primária, perda secundária), em R$, já com os fatores de
    preparação (fatores_magnitude)."""
    primaria = amostrar_pert(rng, *pontos_primaria(cen, ctx), n=n, lam=pm.pert_lambda)

    mediana, p95, teto = pontos_secundaria(cen, ctx, setor)
    ocorre = rng.random(n) < cen.perda_secundaria.probabilidade
    secundaria = np.zeros(n)
    k = int(ocorre.sum())
    if k and mediana > 0 and p95 > mediana:
        mu, sigma = lognormal_parametros(mediana, p95, pm.z_p95)
        secundaria[ocorre] = amostrar_lognormal(rng, mu, sigma, k, teto=teto)
    return primaria * fatores[0], secundaria * fatores[1]
