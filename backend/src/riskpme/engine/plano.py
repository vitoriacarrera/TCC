"""Plano de ação priorizado (RF11): quanto cada controle reduz a perda esperada e quanto custa.

Para cada controle ISO/IEC 27002 ligado a perguntas com resposta abaixo de "Sempre" (4) ou "Não sei":
    redução = perda esperada atual − perda esperada com essas respostas em 4
    ROSI    = (redução − custo anual) / custo anual                         (ENISA, 2012)
A perda esperada é ANALÍTICA (determinística): Σ_c LEF_c × E[perda por evento_c], com
    E[primária]  = fator_primária × média da Beta-PERT
    E[secundária] = fator_secundária × p × E[min(X, teto)], X ~ Lognormal(μ, σ)
Os fatores vêm da maturidade de resposta (revisão MAG, ADR-014): uma ação reduz a chance (perguntas de prevenção)
ou o prejuízo (detecção e resposta), conforme a subcategoria NIST das suas perguntas.
para que a ordem do plano não mude de uma execução para outra. Limite de investimento de Gordon e Loeb (2002):
ações cujo custo acumulado passa de perda esperada total / e são marcadas, não removidas.

Segunda lente (revisão M2 b): quanto cada ação reduz o PREJUÍZO NUM PERÍODO RUIM, o P90 da perda somada no
horizonte da matriz (5 anos, M1). A média dilui eventos raros e graves; o P90 do período mostra a proteção contra
eles. Para que a diferença antes/depois não seja ruído de sorteio, usa números aleatórios comuns: as perdas de cada
evento e o uniforme que define o nº de eventos são sorteados uma vez, e só o nº de eventos muda com a LEF (inversão
da CDF de Poisson, monotônica: LEF menor nunca aumenta a perda de nenhuma iteração).

Riscos de ruptura (revisão M2 c, MAG): as ações com perguntas que reduzem o prejuízo (parametros_modelo.efeito_magnitude
em cenarios.yaml) e alimentam um cenário em ruptura são marcadas em `protege_ruptura`, mesmo com ROSI negativo, e
mostram quanto baixam o IMPACTO do cenário (P90 da perda no ano em que ele acontece, o eixo de impacto da matriz).
Cada risco de ruptura informa o impacto atual, o impacto com todas as ações de preparação e se ele cairia abaixo
da tolerância (deixando a faixa "acima da tolerância"). Mede só o efeito no prejuízo (a chance não muda).
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import numpy as np

from ..catalog.models import Catalogo
from .distribuicoes import lognormal_parametros, pert_media
from .magnitude import amostrar_perdas_evento, pontos_primaria, pontos_secundaria
from .maturidade import NOTA_MAXIMA, Respostas
from .perfil import Perfil, PerfilResolvido, resolver
from .simulacao import fatores_por_cenario, horizonte, lef_por_cenario, poisson_truncada


def _phi(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def media_lognormal_com_teto(mu: float, sigma: float, teto: float) -> float:
    """E[min(X, T)] para X ~ Lognormal(μ, σ)."""
    lt = math.log(teto)
    return (math.exp(mu + sigma**2 / 2) * _phi((lt - mu - sigma**2) / sigma)
            + teto * (1 - _phi((lt - mu) / sigma)))


def perda_media_evento(cat: Catalogo, cid: str, res: PerfilResolvido,
                       fatores: tuple[float, float] = (1.0, 1.0)) -> float:
    c = cat.cenario(cid)
    pm = cat.parametros_modelo
    a, m, b = pontos_primaria(c, res.contexto)
    primaria = pert_media(a, m, b, pm.pert_lambda) if b > a else a
    mediana, p95, teto = pontos_secundaria(c, res.contexto, cat.setor(res.setor))
    secundaria = 0.0
    if mediana > 0 and p95 > mediana:
        mu, sigma = lognormal_parametros(mediana, p95, pm.z_p95)
        secundaria = c.perda_secundaria.probabilidade * media_lognormal_com_teto(mu, sigma, teto)
    return fatores[0] * primaria + fatores[1] * secundaria


def perda_esperada_analitica(cat: Catalogo, res: PerfilResolvido, respostas: Respostas) -> dict[str, float]:
    _, _, lef = lef_por_cenario(cat, res, respostas)
    _, fat = fatores_por_cenario(cat, res, respostas)
    return {cid: lam * perda_media_evento(cat, cid, res, fat[cid]) for cid, lam in lef.items()}


# ------------------------------------------------------------------ prejuízo num período ruim (M2 b)
def _cdf_poisson(lam: float, kmax: int) -> np.ndarray:
    k = np.arange(kmax + 1)
    if lam <= 0:
        return np.ones(kmax + 1)
    logp = -lam + k * math.log(lam) - np.array([math.lgamma(x + 1) for x in k])
    return np.cumsum(np.exp(logp))


def _kmax(lam: float, eps: float = 1e-6) -> int:
    """Menor k com P(N > k) < eps para N ~ Poisson(λ)."""
    k, p, acum = 0, math.exp(-lam), math.exp(-lam)
    while 1 - acum >= eps:
        k += 1
        p *= lam / k
        acum += p
    return max(k, 1)


@dataclass
class SorteioPeriodo:
    """Números aleatórios comuns para comparar o período ruim antes e depois de cada ação."""

    anos: int
    u: dict[str, np.ndarray]            # uniforme por iteração: define o nº de eventos no período
    acum_primaria: dict[str, np.ndarray]    # (n, kmax + 1): coluna k = soma das perdas primárias dos k primeiros
    acum_secundaria: dict[str, np.ndarray]  # idem, perda secundária (sem fatores de preparação)

    def perda(self, lef: dict[str, float],
              fatores: dict[str, tuple[float, float]] | None = None) -> np.ndarray:
        """Perda somada no período, por iteração, para as LEF (eventos por ano) e fatores de preparação dados.
        Monotônica: LEF e fatores menores nunca aumentam a perda de nenhuma iteração."""
        n = next(iter(self.u.values())).size
        total = np.zeros(n)
        linhas = np.arange(n)
        for cid, prim in self.acum_primaria.items():
            kmax = prim.shape[1] - 1
            fp, fs = (fatores or {}).get(cid, (1.0, 1.0))
            cdf = _cdf_poisson(lef[cid] * self.anos, kmax)
            eventos = np.searchsorted(cdf, self.u[cid], side="right").clip(max=kmax)
            total += fp * prim[linhas, eventos] + fs * self.acum_secundaria[cid][linhas, eventos]
        return total


def sortear_periodo(cat: Catalogo, res: PerfilResolvido, anos: int, n: int,
                    semente: int | None) -> SorteioPeriodo:
    rng = np.random.default_rng(semente)
    setor = cat.setor(res.setor)
    pm = cat.parametros_modelo
    u, acp, acs = {}, {}, {}
    for c in cat.cenarios:
        lam_max = cat.tef(c.id, res.porte, res.setor) * pm.vulnerabilidade_max * anos   # maturidade 0
        kmax = _kmax(lam_max)
        prim, sec = amostrar_perdas_evento(rng, c, res.contexto, setor, pm, n * kmax)
        for destino, x in ((acp, prim), (acs, sec)):
            acum = np.zeros((n, kmax + 1))
            acum[:, 1:] = np.cumsum(x.reshape(n, kmax), axis=1)
            destino[c.id] = acum
        u[c.id] = rng.random(n)
    return SorteioPeriodo(anos=anos, u=u, acum_primaria=acp, acum_secundaria=acs)


def amostrar_impacto(cat: Catalogo, res: PerfilResolvido, cid: str, lef: float, n: int,
                     semente: int | None) -> tuple[np.ndarray, np.ndarray]:
    """(perda primária, perda secundária) somadas por ano, nos anos em que o cenário acontece, sem fatores.
    Números aleatórios comuns: aplicar fatores diferentes a esta mesma amostra compara antes e depois."""
    rng = np.random.default_rng(semente)
    n_cond = poisson_truncada(rng, lef, n)
    prim, sec = amostrar_perdas_evento(rng, cat.cenario(cid), res.contexto, cat.setor(res.setor),
                                       cat.parametros_modelo, int(n_cond.sum()))
    anos = np.repeat(np.arange(n), n_cond)
    return np.bincount(anos, prim, n), np.bincount(anos, sec, n)


@dataclass
class Acao:
    prioridade: int
    controle: str
    controle_nome: str
    perguntas: list[str]
    recomendacoes: list[str]
    reducao_perda_anual: float
    reducao_periodo_ruim: float     # quanto reduz o P90 da perda somada no horizonte (M2 b)
    custo_anual: float
    rosi: float | None              # None quando o custo é zero
    acima_do_limite: bool           # custo acumulado passou de perda esperada / e (Gordon-Loeb)
    selo: str | None                # selo de privacidade pelo tipo de dado (revisão C-DADO)
    protege_ruptura: list[str]      # cenários em ruptura cujo impacto a ação ajuda a aguentar (M2 c)
    impacto_ruptura: dict[str, float]   # P90 no ano em que o cenário acontece, só com esta ação (por cenário)


@dataclass
class Plano:
    perda_esperada_atual: float
    limite_investimento: float
    horizonte_anos: int
    perda_periodo_ruim_atual: float     # P90 da perda somada no horizonte, com as respostas atuais
    acoes: list[Acao]
    ruptura: list[dict]             # cenários raros e graves: preparação e transferência

    def to_dict(self) -> dict:
        return asdict(self)


def plano_de_acao(cat: Catalogo, perfil: Perfil, respostas: Respostas,
                  cenarios_ruptura: list[str] | None = None, semente: int | None = 0,
                  iteracoes: int | None = None) -> Plano:
    """Plano priorizado. `semente` fixa (padrão 0) para que o mesmo perfil gere sempre o mesmo plano."""
    res = resolver(cat, perfil)
    perguntas = cat.questionario(res.porte, res.setor, res.usuarios)
    atual = perda_esperada_analitica(cat, res, respostas)
    el_atual = sum(atual.values())
    q = cat.parametros_modelo.percentil_mapa_calor
    sorteio = sortear_periodo(cat, res, horizonte(cat), iteracoes or cat.parametros_modelo.iteracoes, semente)
    ruim_atual = float(np.percentile(sorteio.perda(lef_por_cenario(cat, res, respostas)[2],
                                                   fatores_por_cenario(cat, res, respostas)[1]), q))
    em_ruptura = set(cenarios_ruptura or [])
    pm = cat.parametros_modelo
    n = iteracoes or pm.iteracoes
    lef_atual = lef_por_cenario(cat, res, respostas)[2]
    fat_atual = fatores_por_cenario(cat, res, respostas)[1]
    amostras = {cid: amostrar_impacto(cat, res, cid, lef_atual[cid], n, semente) for cid in em_ruptura}

    def impacto(cid: str, f: tuple[float, float]) -> float:
        prim, sec = amostras[cid]
        return float(np.percentile(f[0] * prim + f[1] * sec, q))

    tipo = next(q for q in cat.contexto["ativos"] if q["id"] == "tipo_dado")
    selo_txt = next(op for op in tipo["opcoes"] if op["id"] == res.tipo_dado).get("selo")
    selo_ctrl = set(tipo.get("selo_em_controles", []))
    selo_perg = set(tipo.get("selo_em_perguntas", []))

    por_controle: dict[str, list] = {}
    for p in perguntas:
        r = respostas.get(p.id)
        if r is None or r < NOTA_MAXIMA:
            por_controle.setdefault(p.controle, []).append(p)

    candidatas: list[Acao] = []
    for ctrl, ps in por_controle.items():
        melhor = dict(respostas) | {p.id: NOTA_MAXIMA for p in ps}
        reducao = el_atual - sum(perda_esperada_analitica(cat, res, melhor).values())
        if reducao <= 0:
            continue
        fat_melhor = fatores_por_cenario(cat, res, melhor)[1]
        perda_melhor = sorteio.perda(lef_por_cenario(cat, res, melhor)[2], fat_melhor)
        reducao_ruim = ruim_atual - float(np.percentile(perda_melhor, q))
        protege = sorted({c for p in ps if pm.reduz_magnitude(p.subcategoria) for c in p.cenarios} & em_ruptura)
        imp = {c: impacto(c, fat_melhor[c]) for c in protege}
        custo = cat.custo_controle(ctrl, res.porte, res.usuarios).total
        rosi = (reducao - custo) / custo if custo > 0 else None
        tem_selo = selo_txt and (ctrl in selo_ctrl or any(p.id in selo_perg for p in ps))
        candidatas.append(Acao(
            prioridade=0, controle=ctrl, controle_nome=cat.controle(ctrl).nome, perguntas=[p.id for p in ps],
            recomendacoes=[p.recomendacao for p in ps], reducao_perda_anual=reducao,
            reducao_periodo_ruim=max(reducao_ruim, 0.0), custo_anual=custo, rosi=rosi, acima_do_limite=False,
            selo=selo_txt if tem_selo else None, protege_ruptura=protege, impacto_ruptura=imp))

    # sem custo primeiro (por redução), depois maior ROSI
    candidatas.sort(key=lambda a: (a.rosi is not None, -(a.rosi if a.rosi is not None else a.reducao_perda_anual)))
    limite = el_atual / math.e
    acumulado = 0.0
    for i, a in enumerate(candidatas, start=1):
        a.prioridade = i
        acumulado += a.custo_anual
        a.acima_do_limite = acumulado > limite

    selo = cat.contexto["matriz"]["selo_ruptura"]
    ruptura = []
    for cid in cenarios_ruptura or []:
        prep = [a for a in candidatas if cid in a.protege_ruptura]
        todas = dict(respostas) | {pid: NOTA_MAXIMA for a in prep for pid in a.perguntas}
        com_prep = impacto(cid, fatores_por_cenario(cat, res, todas)[1][cid])
        ruptura.append({"cenario": cid, "texto": selo["texto"], "transferencia": selo["transferencia"],
                        "texto_preparacao": selo["texto_preparacao"], "preparacao": [a.controle for a in prep],
                        "impacto_atual": impacto(cid, fat_atual[cid]), "impacto_com_preparacao": com_prep,
                        "tolerancia": res.tolerancia_rs, "sai_da_ruptura": com_prep < res.tolerancia_rs})
    return Plano(perda_esperada_atual=el_atual, limite_investimento=limite, horizonte_anos=sorteio.anos,
                 perda_periodo_ruim_atual=ruim_atual, acoes=candidatas, ruptura=ruptura)


def resumo(acoes: list[Acao], n: int = 5) -> list[tuple[int, str, float, float]]:
    """(prioridade, controle, redução, custo) das n primeiras ações — usado no relatório e nos testes."""
    return [(a.prioridade, a.controle, a.reducao_perda_anual, a.custo_anual) for a in acoes[:n]]


__all__ = ["Acao", "Plano", "SorteioPeriodo", "amostrar_impacto", "media_lognormal_com_teto", "perda_esperada_analitica",
           "plano_de_acao", "resumo", "sortear_periodo"]
