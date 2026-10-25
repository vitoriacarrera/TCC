"""Base anonimizada para pesquisa (ADR-005): gravada só com consentimento, isolada da simulação.

Grava apenas setor, nível de porte, respostas por id de pergunta, versão do catálogo e mês/ano. Não grava valores
financeiros, nº de registros, nº de usuários, ativo crítico, IP, user-agent, horário exato nem qualquer id de sessão.
A tabela não tem chave sequencial exposta e a API não oferece leitura individual.
"""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import date
from pathlib import Path

VARIAVEL_BANCO = "RISKPME_CONTRIBUICOES_DB"

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS contribuicoes (
    mes_ano          TEXT    NOT NULL,   -- AAAA-MM
    versao_catalogo  TEXT    NOT NULL,
    setor            TEXT    NOT NULL,
    porte            INTEGER NOT NULL CHECK (porte BETWEEN 1 AND 4),
    respostas        TEXT    NOT NULL    -- JSON {id_pergunta: 0..4 | null}
)
"""


def caminho_banco() -> Path | None:
    """Caminho do SQLite, ou None quando a coleta está desativada (variável de ambiente ausente)."""
    v = os.environ.get(VARIAVEL_BANCO)
    return Path(v) if v else None


def gravar(caminho: Path, versao_catalogo: str, setor: str, porte: int, respostas: dict[str, int | None],
           hoje: date | None = None) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    mes = (hoje or date.today()).strftime("%Y-%m")
    with sqlite3.connect(caminho) as con:
        con.execute(_ESQUEMA)
        con.execute("INSERT INTO contribuicoes VALUES (?, ?, ?, ?, ?)",
                    (mes, versao_catalogo, setor, porte, json.dumps(respostas, sort_keys=True)))


def contar_por_celula(caminho: Path) -> dict[tuple[str, int], int]:
    """Quantidade por setor × porte (para a regra n ≥ 5 das análises publicadas)."""
    if not caminho.exists():
        return {}
    with sqlite3.connect(caminho) as con:
        con.execute(_ESQUEMA)
        linhas = con.execute("SELECT setor, porte, COUNT(*) FROM contribuicoes GROUP BY setor, porte").fetchall()
    return {(s, p): n for s, p, n in linhas}
