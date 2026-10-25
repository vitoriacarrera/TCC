"""Simulação de Monte Carlo do risco anual (RF09) e avaliação na matriz 3 × 3 (RF10, ADR-012).

Para cada cenário c do perfil:
    LEF_c = TEF_c × V_c,  TEF_c = tef_base × mult_setor × mult_porte,  V_c pela maturidade (maturidade.py)
    N_c ~ Poisson(LEF_c) eventos no ano; cada evento custa Perda Primária (PERT) + Perda Secundária (Bernoulli ×
    Lognormal com teto) — magnitude.py —, multiplicadas pelos fatores de preparação (revisão MAG, ADR-014).
A maturidade de PREVENÇÃO define V; a de RESPOSTA define os fatores de magnitude.
Saídas por cenário: chance no ano P(N ≥ 1) = 1 − e^(−LEF), chance no horizonte da matriz 1 − e^(−H × LEF)
(H = 5 anos, revisão M1), perda esperada por ano, P90 da perda nos anos em que o cenário acontece (N ~ Poisson
truncada em zero, para não sumir com cenários raros) e a célula da matriz (probabilidade pela chance no horizonte).
Saída total: distribuição da perda anual somando os cenários (curva de excedência).
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field

import numpy as np

from ..catalog.models import Catalogo
from .magnitude import amostrar_perdas_evento, fatores_magnitude
from .maturidade import Respostas, maturidade_por_cenario, nao_sei, vulnerabilidade
from .perfil import Perfil, PerfilResolvido, resolver

PERCENTIS_CURVA = (50, 75, 90, 95, 99)


@dataclass
class ResultadoCenario:
    id: str
    nome: str
    maturidade: float               # de prevenção (define a vulnerabilidade)
    maturidade_resposta: float      # de detecção e resposta (define a redução do prejuízo)
    vulnerabilidade: float
    fator_primaria: float           # multiplicador da perda primária pela preparação (1 = sem redução)
    fator_secundaria: float
    lef: float                      # eventos de perda esperados por ano
    chance_ano: float               # P(≥ 1 evento no ano)
    chance_horizonte: float         # P(≥ 1 evento nos próximos H anos): eixo de probabilidade da matriz (M1)
    perda_esperada: float           # R$/ano (Monte Carlo)
    p90_quando_ocorre: float        # R$ no ano, dado que ocorre ao menos um evento
    nivel_impacto: int
    nivel_probabilidade: int
    cor: str
    ruptura: bool                   # rara + acima da tolerância (selo)
    destaque: bool                  # ligado ao ativo crítico informado


@dataclass
class Resultado:
    porte: int
    setor: str
    iteracoes: int
    semente: int | None
    apetite_rs: float
    tolerancia_rs: float
    custo_hora_parada: float
    custo_hora_estimado: bool
    horizonte_anos: int
    cenarios: list[ResultadoCenario]
    chance_algum_prejuizo: float
    chance_algum_prejuizo_horizonte: float
    perda_esperada_total: float
    percentis_total: dict[int, float]
    nao_sei: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def cenario(self, cid: str) -> ResultadoCenario:
        return next(c for c in self.cenarios if c.id == cid)


def _somar_por_ano(n_eventos: np.ndarray, perdas: np.ndarray) -> np.ndarray:
    anos = np.repeat(np.arange(n_eventos.size), n_eventos)
    return np.bincount(anos, weights=perdas, minlength=n_eventos.size)


def poisson_truncada(rng: np.random.Generator, lam: float, n: int) -> np.ndarray:
    """N ~ Poisson(λ) condicionada a N ≥ 1, por inversão da CDF (estável para λ pequeno)."""
    if lam <= 0:
        return np.ones(n, dtype=int)
    kmax = max(10, int(lam + 12 * math.sqrt(lam) + 12))
    k = np.arange(1, kmax + 1)
    logp = -lam + k * math.log(lam) - np.array([math.lgamma(x + 1) for x in k])
    p = np.exp(logp)
    p /= p.sum()
    return 1 + np.searchsorted(np.cumsum(p), rng.random(n), side="right").clip(max=kmax - 1)


def horizonte(cat: Catalogo) -> int:
    """Anos usados no eixo de probabilidade da matriz (contexto.yaml, matriz.horizonte_anos)."""
    return int(cat.contexto["matriz"]["horizonte_anos"])


def chance_em(lef: float, anos: float) -> float:
    """P(≥ 1 evento em `anos` anos) para eventos Poisson com taxa `lef` por ano."""
    return 1 - math.exp(-lef * anos)


def _niveis(cat: Catalogo, p90: float, chance: float, res: PerfilResolvido) -> tuple[int, int, str, bool]:
    m = cat.contexto["matriz"]
    if p90 < res.apetite_rs:
        imp = 1
    elif p90 < res.tolerancia_rs:
        imp = 2
    else:
        imp = 3
    prob = next(n["nivel"] for n in m["probabilidade"] if chance < n["maximo"] or n["nivel"] == 3)
    cor = next(c["cor"] for c in m["cores"] if imp + prob in c["soma"])
    q = m["selo_ruptura"]["quando"]
    return imp, prob, cor, (imp == q["impacto"] and prob == q["probabilidade"])


def lef_por_cenario(cat: Catalogo, res: PerfilResolvido, respostas: Respostas) -> tuple[dict, dict, dict]:
    """(maturidade, vulnerabilidade, LEF) por cenário para o perfil e as respostas."""
    perguntas = cat.questionario(res.porte, res.setor, res.usuarios)
    mat = maturidade_por_cenario(cat, perguntas, respostas)
    vul = {c: vulnerabilidade(cat, m) for c, m in mat.items()}
    lef = {c.id: cat.tef(c.id, res.porte, res.setor) * vul[c.id] for c in cat.cenarios}
    return mat, vul, lef


def fatores_por_cenario(cat: Catalogo, res: PerfilResolvido,
                        respostas: Respostas) -> tuple[dict[str, float], dict[str, tuple[float, float]]]:
    """(maturidade de resposta, (fator primária, fator secundária)) por cenário."""
    perguntas = cat.questionario(res.porte, res.setor, res.usuarios)
    mat = maturidade_por_cenario(cat, perguntas, respostas, "magnitude")
    fat = {c.id: fatores_magnitude(c, res.contexto, cat.parametros_modelo, mat[c.id]) for c in cat.cenarios}
    return mat, fat


def simular(cat: Catalogo, perfil: Perfil, respostas: Respostas, iteracoes: int | None = None,
            semente: int | None = None) -> Resultado:
    res = resolver(cat, perfil)
    n = iteracoes or cat.parametros_modelo.iteracoes
    rng = np.random.default_rng(semente)
    setor = cat.setor(res.setor)
    mat, vul, lef = lef_por_cenario(cat, res, respostas)
    mat_resp, fat = fatores_por_cenario(cat, res, respostas)
    destaca = set(next(op for q in cat.contexto["ativos"] if q["id"] == "ativo_critico"
                       for op in q["opcoes"] if op["id"] == res.ativo_critico).get("destaca", []))

    h = horizonte(cat)
    total = np.zeros(n)
    saidas: list[ResultadoCenario] = []
    for c in cat.cenarios:
        lam = lef[c.id]
        # ano a ano (perda esperada e soma total)
        n_ano = rng.poisson(lam, n)
        k = int(n_ano.sum())
        if k:
            prim, sec = amostrar_perdas_evento(rng, c, res.contexto, setor, cat.parametros_modelo, k, fat[c.id])
            anual = _somar_por_ano(n_ano, prim + sec)
        else:
            anual = np.zeros(n)
        total += anual
        # anos em que o cenário acontece (P90 do impacto)
        n_cond = poisson_truncada(rng, lam, n)
        prim, sec = amostrar_perdas_evento(rng, c, res.contexto, setor, cat.parametros_modelo, int(n_cond.sum()),
                                           fat[c.id])
        p90 = float(np.percentile(_somar_por_ano(n_cond, prim + sec), cat.parametros_modelo.percentil_mapa_calor))
        chance = chance_em(lam, 1)
        chance_h = chance_em(lam, h)
        imp, prob, cor, rup = _niveis(cat, p90, chance_h, res)
        saidas.append(ResultadoCenario(
            id=c.id, nome=c.nome, maturidade=mat[c.id], maturidade_resposta=mat_resp[c.id],
            vulnerabilidade=vul[c.id], fator_primaria=fat[c.id][0], fator_secundaria=fat[c.id][1],
            lef=lam, chance_ano=chance,
            chance_horizonte=chance_h, perda_esperada=float(anual.mean()), p90_quando_ocorre=p90,
            nivel_impacto=imp, nivel_probabilidade=prob, cor=cor, ruptura=rup, destaque=c.id in destaca))

    perguntas = cat.questionario(res.porte, res.setor, res.usuarios)
    return Resultado(
        porte=res.porte, setor=res.setor, iteracoes=n, semente=semente, apetite_rs=res.apetite_rs,
        tolerancia_rs=res.tolerancia_rs, custo_hora_parada=res.contexto.custo_hora_parada,
        custo_hora_estimado=res.custo_hora_estimado, horizonte_anos=h, cenarios=saidas,
        chance_algum_prejuizo=chance_em(sum(lef.values()), 1),
        chance_algum_prejuizo_horizonte=chance_em(sum(lef.values()), h), perda_esperada_total=float(total.mean()),
        percentis_total={q: float(np.percentile(total, q)) for q in PERCENTIS_CURVA},
        nao_sei=nao_sei(perguntas, respostas))
