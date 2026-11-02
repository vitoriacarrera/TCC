"""Resultado anonimizado que acompanha a contribuição para a pesquisa (ADR-005, revisão de 02/11/2026).

Só posições e proporções, nunca valores em reais: célula da matriz, cor, ruptura, chance no horizonte, maturidades,
perda esperada como fração da receita (a receita não é guardada, então o valor em reais não pode ser reconstruído)
e os controles recomendados, na ordem, com o bloco do plano. O resumo vai assinado no comprovante (HMAC), então a
base só recebe resultados calculados pela própria API.
"""

from __future__ import annotations

from ..engine.plano import Plano
from ..engine.simulacao import Resultado


def bloco(acima_do_limite: bool, protege_ruptura: list[str]) -> str:
    """Mesmo agrupamento da tela (ADR-015): comece, preparo (pior caso) ou depois."""
    if not acima_do_limite:
        return "comece"
    return "preparo" if protege_ruptura else "depois"


def resumo_pesquisa(r: Resultado, plano: Plano, receita: float) -> dict:
    return {
        "horizonte_anos": r.horizonte_anos,
        "chance_algum_prejuizo_horizonte": round(r.chance_algum_prejuizo_horizonte, 4),
        "perda_esperada_pct_receita": round(r.perda_esperada_total / receita, 6),
        "nao_sei": len(r.nao_sei),
        "cenarios": {
            c.id: {
                "impacto": c.nivel_impacto,
                "probabilidade": c.nivel_probabilidade,
                "cor": c.cor,
                "ruptura": c.ruptura,
                "chance_horizonte": round(c.chance_horizonte, 4),
                "maturidade_prevencao": round(c.maturidade, 3),
                "maturidade_resposta": round(c.maturidade_resposta, 3),
                "perda_esperada_pct_receita": round(c.perda_esperada / receita, 6),
            }
            for c in r.cenarios
        },
        "acoes": [{"controle": a.controle, "bloco": bloco(a.acima_do_limite, a.protege_ruptura)} for a in plano.acoes],
    }
