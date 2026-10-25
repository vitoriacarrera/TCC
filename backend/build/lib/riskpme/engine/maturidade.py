"""Maturidade por cenário a partir das respostas do questionário (RF06, ADR-006).

maturidade(c) = Σ (resposta/4 × peso_c) / Σ peso_c, sobre as perguntas do perfil que alimentam o cenário c.
Duas maturidades por cenário (revisão MAG, FAIR-CAM): de PREVENÇÃO (perguntas que reduzem a chance) e de RESPOSTA
(Detecção, Resposta, Recuperação, backup e resiliência: reduzem o prejuízo). Cada pergunta entra em uma só.
Cenário sem nenhuma pergunta do tipo pedido tem maturidade 0 (sem redução).
"Não sei" (None) conta como `resposta_nao_sei` (1 = "raramente"): postura cautelosa, mostrada no relatório.
Vulnerabilidade(c) = v_min + (v_max − v_min) × (1 − maturidade(c))          (TCC1 §3.6, item 1)
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

from ..catalog.models import Catalogo, Pergunta

Respostas = Mapping[str, int | None]
NOTA_MAXIMA = 4


def nota(resposta: int | None, nao_sei: int) -> int:
    if resposta is None:
        return nao_sei
    if not 0 <= resposta <= NOTA_MAXIMA:
        raise ValueError(f"resposta fora da escala 0–4: {resposta}")
    return resposta


Efeito = Literal["frequencia", "magnitude"]


def maturidade_por_cenario(cat: Catalogo, perguntas: list[Pergunta], respostas: Respostas,
                           efeito: Efeito = "frequencia") -> dict[str, float]:
    """Maturidade de 0 a 1 por cenário. Pergunta sem resposta conta como "Não sei"."""
    nao_sei = cat.parametros_modelo.resposta_nao_sei
    ids = {p.id for p in perguntas}
    extras = set(respostas) - ids
    if extras:
        raise ValueError(f"respostas para perguntas fora do questionário do perfil: {sorted(extras)}")
    soma: dict[str, float] = {c.id: 0.0 for c in cat.cenarios}
    pesos: dict[str, float] = {c.id: 0.0 for c in cat.cenarios}
    pm = cat.parametros_modelo
    for p in perguntas:
        if pm.reduz_magnitude(p.subcategoria) != (efeito == "magnitude"):
            continue
        n = nota(respostas.get(p.id), nao_sei) / NOTA_MAXIMA
        for c, w in p.cenarios.items():
            soma[c] += n * w
            pesos[c] += w
    return {c: (soma[c] / pesos[c] if pesos[c] else 0.0) for c in soma}


def vulnerabilidade(cat: Catalogo, maturidade: float) -> float:
    pm = cat.parametros_modelo
    return pm.vulnerabilidade_min + (pm.vulnerabilidade_max - pm.vulnerabilidade_min) * (1 - maturidade)


def nao_sei(perguntas: list[Pergunta], respostas: Respostas) -> list[str]:
    """Perguntas respondidas com "Não sei" (ou sem resposta), para destacar no relatório."""
    return [p.id for p in perguntas if respostas.get(p.id) is None]
