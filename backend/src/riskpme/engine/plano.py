"""Plano de ação priorizado (RF11): quanto cada controle reduz a perda esperada e quanto custa.

Para cada controle ISO/IEC 27002 ligado a perguntas com resposta abaixo de "Sempre" (4) ou "Não sei":
    redução = perda esperada atual − perda esperada com essas respostas em 4
    ROSI    = (redução − custo anual) / custo anual                         (ENISA, 2012)
A perda esperada é ANALÍTICA (determinística): Σ_c LEF_c × E[perda por evento_c], com
    E[primária]  = média da Beta-PERT
    E[secundária] = p × E[min(X, teto)], X ~ Lognormal(μ, σ)
para que a ordem do plano não mude de uma execução para outra. Limite de investimento de Gordon e Loeb (2002):
ações cujo custo acumulado passa de perda esperada total / e são marcadas, não removidas.

Segunda lente (revisão M2 b): quanto cada ação reduz o PREJUÍZO NUM PERÍODO RUIM, o P90 da perda somada no
horizonte da matriz (5 anos, M1). A média dilui eventos raros e graves; o P90 do período mostra a proteção contra
eles. Para que a diferença antes/depois não seja ruído de sorteio, usa números aleatórios comuns: as perdas de cada
evento e o uniforme que define o nº de eventos são sorteados uma vez, e só o nº de eventos muda com a LEF (inversão
da CDF de Poisson, monotônica: LEF menor nunca aumenta a perda de nenhuma iteração).

Riscos de ruptura (revisão M2 c): as ações ligadas a perguntas de preparação (Responder e Recuperar do NIST CSF 2.0,
backup e resiliência; contexto.yaml, matriz.selo_ruptura.preparacao) que alimentam um cenário em ruptura são
marcadas em `protege_ruptura`, mesmo com ROSI negativo.
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
from .simulacao import horizonte, lef_por_cenario


def _phi(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def media_lognormal_com_teto(mu: float, sigma: float, teto: float) -> float:
    """E[min(X, T)] para X ~ Lognormal(μ, σ)."""
    lt = math.log(teto)
    return (math.exp(mu + sigma**2 / 2) * _phi((lt - mu - sigma**2) / sigma)
            + teto * (1 - _phi((lt - mu) / sigma)))


def perda_media_evento(cat: Catalogo, cid: str, res: PerfilResolvido) -> float:
    c = cat.cenario(cid)
    pm = cat.parametros_modelo
    a, m, b = pontos_primaria(c, res.contexto)
    primaria = pert_media(a, m, b, pm.pert_lambda) if b > a else a
    mediana, p95, teto = pontos_secundaria(c, res.contexto, cat.setor(res.setor))
    secundaria = 0.0
    if mediana > 0 and p95 > mediana:
        mu, sigma = lognormal_parametros(mediana, p95, pm.z_p95)
        secundaria = c.perda_secundaria.probabilidade * media_lognormal_com_teto(mu, sigma, teto)
    return primaria + secundaria


def perda_esperada_analitica(cat: Catalogo, res: PerfilResolvido, respostas: Respostas) -> dict[str, float]:
    _, _, lef = lef_por_cenario(cat, res, respostas)
    return {cid: lam * perda_media_evento(cat, cid, res) for cid, lam in lef.items()}


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
    acumulada: dict[str, np.ndarray]    # (n, kmax + 1): coluna k = soma das perdas dos k primeiros eventos

    def perda(self, lef: dict[str, float]) -> np.ndarray:
        """Perda somada no período, por iteração, para as LEF (eventos por ano) dadas."""
        n = next(iter(self.u.values())).size
        total = np.zeros(n)
        linhas = np.arange(n)
        for cid, acum in self.acumulada.items():
            kmax = acum.shape[1] - 1
            cdf = _cdf_poisson(lef[cid] * self.anos, kmax)
            eventos = np.searchsorted(cdf, self.u[cid], side="right").clip(max=kmax)
            total += acum[linhas, eventos]
        return total


def sortear_periodo(cat: Catalogo, res: PerfilResolvido, anos: int, n: int,
                    semente: int | None) -> SorteioPeriodo:
    rng = np.random.default_rng(semente)
    setor = cat.setor(res.setor)
    pm = cat.parametros_modelo
    u, acumulada = {}, {}
    for c in cat.cenarios:
        lam_max = cat.tef(c.id, res.porte, res.setor) * pm.vulnerabilidade_max * anos   # maturidade 0
        kmax = _kmax(lam_max)
        prim, sec = amostrar_perdas_evento(rng, c, res.contexto, setor, pm, n * kmax)
        acum = np.zeros((n, kmax + 1))
        acum[:, 1:] = np.cumsum((prim + sec).reshape(n, kmax), axis=1)
        acumulada[c.id] = acum
        u[c.id] = rng.random(n)
    return SorteioPeriodo(anos=anos, u=u, acumulada=acumulada)


def _preparacao(cat: Catalogo) -> tuple[str, ...]:
    return tuple(cat.contexto["matriz"]["selo_ruptura"]["preparacao"]["subcategorias"])


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
    ruim_atual = float(np.percentile(sorteio.perda(lef_por_cenario(cat, res, respostas)[2]), q))
    em_ruptura = set(cenarios_ruptura or [])
    prep = _preparacao(cat)

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
        lef_melhor = lef_por_cenario(cat, res, melhor)[2]
        reducao_ruim = ruim_atual - float(np.percentile(sorteio.perda(lef_melhor), q))
        protege = sorted({c for p in ps if p.subcategoria.startswith(prep) for c in p.cenarios} & em_ruptura)
        custo = cat.custo_controle(ctrl, res.porte, res.usuarios).total
        rosi = (reducao - custo) / custo if custo > 0 else None
        tem_selo = selo_txt and (ctrl in selo_ctrl or any(p.id in selo_perg for p in ps))
        candidatas.append(Acao(
            prioridade=0, controle=ctrl, controle_nome=cat.controle(ctrl).nome, perguntas=[p.id for p in ps],
            recomendacoes=[p.recomendacao for p in ps], reducao_perda_anual=reducao,
            reducao_periodo_ruim=max(reducao_ruim, 0.0), custo_anual=custo, rosi=rosi, acima_do_limite=False,
            selo=selo_txt if tem_selo else None, protege_ruptura=protege))

    # sem custo primeiro (por redução), depois maior ROSI
    candidatas.sort(key=lambda a: (a.rosi is not None, -(a.rosi if a.rosi is not None else a.reducao_perda_anual)))
    limite = el_atual / math.e
    acumulado = 0.0
    for i, a in enumerate(candidatas, start=1):
        a.prioridade = i
        acumulado += a.custo_anual
        a.acima_do_limite = acumulado > limite

    selo = cat.contexto["matriz"]["selo_ruptura"]
    ruptura = [{"cenario": cid, "texto": selo["texto"], "transferencia": selo["transferencia"],
                "texto_preparacao": selo["texto_preparacao"],
                "preparacao": [a.controle for a in candidatas if cid in a.protege_ruptura]}
               for cid in (cenarios_ruptura or [])]
    return Plano(perda_esperada_atual=el_atual, limite_investimento=limite, horizonte_anos=sorteio.anos,
                 perda_periodo_ruim_atual=ruim_atual, acoes=candidatas, ruptura=ruptura)


def resumo(acoes: list[Acao], n: int = 5) -> list[tuple[int, str, float, float]]:
    """(prioridade, controle, redução, custo) das n primeiras ações — usado no relatório e nos testes."""
    return [(a.prioridade, a.controle, a.reducao_perda_anual, a.custo_anual) for a in acoes[:n]]


__all__ = ["Acao", "Plano", "SorteioPeriodo", "media_lognormal_com_teto", "perda_esperada_analitica", "plano_de_acao", "resumo", "sortear_periodo"]
