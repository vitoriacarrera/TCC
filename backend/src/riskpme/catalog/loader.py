"""Carrega os arquivos YAML de `audit/` e monta um `Catalogo` validado."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml

from .models import Catalogo

ARQUIVOS = ("fontes", "portes", "setores", "cenarios", "controles", "perguntas", "contexto", "glossario", "custos")


def diretorio_padrao() -> Path:
    """`RISKPME_AUDIT_DIR` (usado no Docker) ou a pasta `audit/` na raiz do repositório."""
    env = os.environ.get("RISKPME_AUDIT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[4] / "audit"


def _ler(diretorio: Path, nome: str) -> dict:
    caminho = diretorio / f"{nome}.yaml"
    if not caminho.exists():
        raise FileNotFoundError(f"arquivo do catálogo não encontrado: {caminho}")
    with caminho.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def carregar_catalogo(diretorio: str | Path | None = None) -> Catalogo:
    d = Path(diretorio) if diretorio else diretorio_padrao()
    dados = {nome: _ler(d, nome) for nome in ARQUIVOS}
    return Catalogo(
        fontes=dados["fontes"]["fontes"],
        portes=dados["portes"]["portes"],
        setores=dados["setores"]["setores"],
        parametros_modelo=dados["cenarios"]["parametros_modelo"],
        cenarios=dados["cenarios"]["cenarios"],
        controles=dados["controles"]["controles"],
        instrucoes=dados["perguntas"]["instrucoes"],
        funcoes=dados["perguntas"]["funcoes"],
        escala=dados["perguntas"]["escala"],
        glossario=dados["glossario"],
        custos=dados["custos"],
        perguntas=dados["perguntas"]["perguntas"],
        contexto=dados["contexto"],
    )


@lru_cache(maxsize=1)
def catalogo_em_cache() -> Catalogo:
    """Instância única para a API (o catálogo é imutável em tempo de execução)."""
    return carregar_catalogo()
