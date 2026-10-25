"""Plano de ação priorizado (RF11): quanto cada controle reduz a perda esperada e quanto custa.

Para cada controle ISO/IEC 27002 ligado a perguntas com resposta abaixo de "Sempre" (4) ou "Não sei":
    redução = perda esperada atual − perda esperada com essas respostas em 4
    ROSI    = (redução − custo anual) / custo anual                         (ENISA, 2012)
A perda esperada é ANALÍTICA (determinística): Σ_c LEF_c × E[perda por evento_c], com
    E[primária]  = média da Beta-PERT
    E[secundária] = p × E[min(X, teto)], X ~ Lognormal(μ, σ)
para que a ordem do plano não mude de uma execução para outra. Limite de investimento de Gordon e Loeb (2002):
ações cujo custo acumulado passa de perda esperada total / e são marcadas, não removidas.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

from ..catalog.models import Catalogo
from .distribuicoes import lognormal_parametros, pert_media
from .magnitude import pontos_primaria, pontos_secundaria
from .maturidade import NOTA_MAXIMA, Respostas
from .perfil import Perfil, PerfilResolvido, resolver
from .simulacao import lef_por_cenario


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


@dataclass
class Acao:
    prioridade: int
    controle: str
    controle_nome: str
    perguntas: list[str]
    recomendacoes: list[str]
    reducao_perda_anual: float
    custo_anual: float
    rosi: float | None              # None quando o custo é zero
    acima_do_limite: bool           # custo acumulado passou de perda esperada / e (Gordon-Loeb)
    selo: str | None                # selo de privacidade pelo tipo de dado (revisão C-DADO)


@dataclass
class Plano:
    perda_esperada_atual: float
    limite_investimento: float
    acoes: list[Acao]
    ruptura: list[dict]             # cenários raros e graves: preparação e transferência

    def to_dict(self) -> dict:
        return asdict(self)


def plano_de_acao(cat: Catalogo, perfil: Perfil, respostas: Respostas,
                  cenarios_ruptura: list[str] | None = None) -> Plano:
    res = resolver(cat, perfil)
    perguntas = cat.questionario(res.porte, res.setor, res.usuarios)
    atual = perda_esperada_analitica(cat, res, respostas)
    el_atual = sum(atual.values())

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
        custo = cat.custo_controle(ctrl, res.porte, res.usuarios).total
        rosi = (reducao - custo) / custo if custo > 0 else None
        tem_selo = selo_txt and (ctrl in selo_ctrl or any(p.id in selo_perg for p in ps))
        candidatas.append(Acao(
            prioridade=0, controle=ctrl, controle_nome=cat.controle(ctrl).nome, perguntas=[p.id for p in ps],
            recomendacoes=[p.recomendacao for p in ps], reducao_perda_anual=reducao, custo_anual=custo,
            rosi=rosi, acima_do_limite=False, selo=selo_txt if tem_selo else None))

    # sem custo primeiro (por redução), depois maior ROSI
    candidatas.sort(key=lambda a: (a.rosi is not None, -(a.rosi if a.rosi is not None else a.reducao_perda_anual)))
    limite = el_atual / math.e
    acumulado = 0.0
    for i, a in enumerate(candidatas, start=1):
        a.prioridade = i
        acumulado += a.custo_anual
        a.acima_do_limite = acumulado > limite

    selo = cat.contexto["matriz"]["selo_ruptura"]
    ruptura = [{"cenario": cid, "texto": selo["texto"], "transferencia": selo["transferencia"]}
               for cid in (cenarios_ruptura or [])]
    return Plano(perda_esperada_atual=el_atual, limite_investimento=limite, acoes=candidatas, ruptura=ruptura)


def resumo(acoes: list[Acao], n: int = 5) -> list[tuple[int, str, float, float]]:
    """(prioridade, controle, redução, custo) das n primeiras ações — usado no relatório e nos testes."""
    return [(a.prioridade, a.controle, a.reducao_perda_anual, a.custo_anual) for a in acoes[:n]]


__all__ = ["Acao", "Plano", "media_lognormal_com_teto", "perda_esperada_analitica", "plano_de_acao", "resumo"]
