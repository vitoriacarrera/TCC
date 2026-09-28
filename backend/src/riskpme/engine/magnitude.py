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

    faturamento_anual: float
    custo_hora_parada: float
    registros_pessoais: int
    fator_tipo_dado: float = 1.0

    def __post_init__(self) -> None:
        if self.faturamento_anual <= 0:
            raise ValueError("faturamento_anual deve ser positivo")
        if self.custo_hora_parada < 0 or self.registros_pessoais < 0 or self.fator_tipo_dado <= 0:
            raise ValueError("contexto com valores negativos ou fator de tipo de dado inválido")


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
    custo_registro = ctx.registros_pessoais * setor.multiplicador_custo_registro * ctx.fator_tipo_dado

    def valor(ponto) -> float:
        return ponto.por_registro * custo_registro + ponto.pct_faturamento * ctx.faturamento_anual + ponto.fixo

    return valor(ps.mediana), valor(ps.p95), ps.teto_pct_faturamento * ctx.faturamento_anual


def amostrar_perdas_evento(rng: np.random.Generator, cen: Cenario, ctx: Contexto, setor: Setor,
                           pm: ParametrosModelo, n: int) -> tuple[np.ndarray, np.ndarray]:
    """Sorteia `n` eventos de perda e devolve (perda primária, perda secundária), em R$."""
    primaria = amostrar_pert(rng, *pontos_primaria(cen, ctx), n=n, lam=pm.pert_lambda)

    mediana, p95, teto = pontos_secundaria(cen, ctx, setor)
    ocorre = rng.random(n) < cen.perda_secundaria.probabilidade
    secundaria = np.zeros(n)
    k = int(ocorre.sum())
    if k and mediana > 0 and p95 > mediana:
        mu, sigma = lognormal_parametros(mediana, p95, pm.z_p95)
        secundaria[ocorre] = amostrar_lognormal(rng, mu, sigma, k, teto=teto)
    return primaria, secundaria
