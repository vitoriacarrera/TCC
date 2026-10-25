"""Perfil da empresa: respostas do Módulo de Entrada (contexto.yaml) convertidas nos números do motor."""

from __future__ import annotations

from dataclasses import dataclass

from ..catalog.models import Catalogo
from .magnitude import Contexto

HORAS_UTEIS_ANO = 2080   # 52 semanas × 40 h (premissa declarada, revisão C-HORA)


@dataclass(frozen=True)
class Perfil:
    """Respostas de contexto do gestor (ids das opções de `audit/contexto.yaml`)."""

    setor: str
    receita_operacional_bruta: float
    usuarios_ti: int
    registros_pessoais: str                  # id da faixa (ex.: "ate1k")
    tipo_dado: str                           # id da opção (ex.: "cadastral")
    ativo_critico: str                       # id da opção (ex.: "vendas")
    apetite: str                             # id da opção (ex.: "a2" ou "nao_sei")
    tolerancia: str                          # id da opção (ex.: "t10" ou "nao_sei")
    custo_hora_parada: float | None = None   # None = "não sei" → receita ÷ 2.080


@dataclass(frozen=True)
class PerfilResolvido:
    porte: int
    setor: str
    usuarios: int
    contexto: Contexto
    apetite_pct: float
    tolerancia_pct: float
    custo_hora_estimado: bool               # True quando veio da fórmula (mostrado ao gestor)
    tipo_dado: str
    ativo_critico: str

    @property
    def apetite_rs(self) -> float:
        return self.apetite_pct * self.contexto.faturamento_anual

    @property
    def tolerancia_rs(self) -> float:
        return self.tolerancia_pct * self.contexto.faturamento_anual


def _pergunta(cat: Catalogo, pid: str) -> dict:
    for bloco in ("financeiro", "ativos", "calibracao_risco"):
        for q in cat.contexto[bloco]:
            if q["id"] == pid:
                return q
    raise KeyError(f"pergunta de contexto '{pid}' não existe")


def _opcao(cat: Catalogo, pid: str, oid: str) -> dict:
    for op in _pergunta(cat, pid)["opcoes"]:
        if op["id"] == oid:
            return op
    raise ValueError(f"opção '{oid}' não existe na pergunta '{pid}'")


def resolver(cat: Catalogo, p: Perfil) -> PerfilResolvido:
    """Valida o perfil e calcula porte, custo da hora, registros, apetite e tolerância (em % da receita)."""
    cat.setor(p.setor)
    if p.usuarios_ti < 1:
        raise ValueError("usuarios_ti deve ser ≥ 1")
    if p.receita_operacional_bruta <= 0:
        raise ValueError("a receita operacional bruta deve ser positiva")
    porte = cat.classificar_porte(p.receita_operacional_bruta)

    estimado = p.custo_hora_parada is None
    custo_hora = p.receita_operacional_bruta / HORAS_UTEIS_ANO if estimado else float(p.custo_hora_parada)
    registros = int(_opcao(cat, "registros_pessoais", p.registros_pessoais)["valor"])
    _opcao(cat, "tipo_dado", p.tipo_dado)
    _opcao(cat, "ativo_critico", p.ativo_critico)

    apetite = float(_opcao(cat, "apetite_pct", p.apetite)["valor"])
    op_tol = _opcao(cat, "tolerancia_pct", p.tolerancia)
    if op_tol.get("valor_por_setor"):
        tolerancia = float(_pergunta(cat, "tolerancia_pct")["nao_sei_por_setor"][p.setor]["valor"])
    else:
        tolerancia = float(op_tol["valor"])
    if not tolerancia > apetite:
        raise ValueError("a tolerância deve ser maior que o apetite (restrição de contexto.yaml)")

    ctx = Contexto(faturamento_anual=p.receita_operacional_bruta, custo_hora_parada=custo_hora,
                   registros_pessoais=registros)
    return PerfilResolvido(porte=porte, setor=p.setor, usuarios=p.usuarios_ti, contexto=ctx,
                           apetite_pct=apetite, tolerancia_pct=tolerancia, custo_hora_estimado=estimado,
                           tipo_dado=p.tipo_dado, ativo_critico=p.ativo_critico)
