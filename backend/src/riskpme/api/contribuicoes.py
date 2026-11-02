"""Base anonimizada para pesquisa (ADR-005, ADR-016): gravada só com consentimento, isolada da simulação.

Grava apenas setor, nível de porte, respostas por id de pergunta, versão do catálogo e mês/ano. Não grava valores
financeiros, nº de registros, nº de usuários, ativo crítico, IP, user-agent, horário exato nem qualquer id de sessão.
A API não oferece leitura; a análise é feita pela autora com `riskpme-catalogo contribuicoes` (catalog/cli.py).

Destino, pela variável RISKPME_CONTRIBUICOES_DB:
    postgresql://usuario:senha@servidor/banco   PostgreSQL gerenciado (produção: Neon, Supabase), respostas em JSONB
    C:\\caminho\\contribuicoes.sqlite            arquivo SQLite (desenvolvimento local)
    ausente                                      coleta desativada
"""

from __future__ import annotations

import json
import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from pathlib import Path

VARIAVEL_BANCO = "RISKPME_CONTRIBUICOES_DB"

_SQLITE = """
CREATE TABLE IF NOT EXISTS contribuicoes (
    mes_ano          TEXT    NOT NULL,   -- AAAA-MM
    versao_catalogo  TEXT    NOT NULL,
    setor            TEXT    NOT NULL,
    porte            INTEGER NOT NULL CHECK (porte BETWEEN 1 AND 4),
    respostas        TEXT    NOT NULL    -- JSON {id_pergunta: 0..4 | null}
)
"""
_POSTGRES = """
CREATE TABLE IF NOT EXISTS contribuicoes (
    mes_ano          TEXT     NOT NULL CHECK (mes_ano ~ '^[0-9]{4}-[0-9]{2}$'),
    versao_catalogo  TEXT     NOT NULL,
    setor            TEXT     NOT NULL,
    porte            SMALLINT NOT NULL CHECK (porte BETWEEN 1 AND 4),
    respostas        JSONB    NOT NULL
)
"""


@dataclass(frozen=True)
class Contribuicao:
    mes_ano: str
    versao_catalogo: str
    setor: str
    porte: int
    respostas: dict[str, int | None]


def destino() -> str | None:
    """Conexão configurada, ou None quando a coleta está desativada."""
    return os.environ.get(VARIAVEL_BANCO) or None


def _postgres(d: str) -> bool:
    return d.startswith(("postgres://", "postgresql://"))


@contextmanager
def _conexao(d: str) -> Iterator[tuple[object, str]]:
    """(conexão, marcador de parâmetro). Cria a tabela na primeira vez. Confirma ao sair sem erro."""
    if _postgres(d):
        import psycopg  # só é necessário em produção

        with psycopg.connect(d, connect_timeout=10) as con:
            con.execute(_POSTGRES)
            yield con, "%s"
    else:
        caminho = Path(d)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(caminho)
        try:
            con.execute(_SQLITE)
            yield con, "?"
            con.commit()
        finally:
            con.close()


_INSERIR = {"%s": "INSERT INTO contribuicoes VALUES (%s, %s, %s, %s, %s)",
            "?": "INSERT INTO contribuicoes VALUES (?, ?, ?, ?, ?)"}


def gravar(d: str, versao_catalogo: str, setor: str, porte: int, respostas: dict[str, int | None],
           hoje: date | None = None) -> None:
    mes = (hoje or date.today()).strftime("%Y-%m")
    with _conexao(d) as (con, m):
        con.execute(_INSERIR[m], (mes, versao_catalogo, setor, porte, json.dumps(respostas, sort_keys=True)))


def ler_todas(d: str) -> list[Contribuicao]:
    """Todas as contribuições, para a análise da autora (nunca exposto pela API)."""
    if not _postgres(d) and not Path(d).exists():
        return []
    with _conexao(d) as (con, _):
        linhas = con.execute("SELECT mes_ano, versao_catalogo, setor, porte, respostas FROM contribuicoes "
                             "ORDER BY mes_ano, setor, porte").fetchall()
    return [Contribuicao(m, v, s, int(p), r if isinstance(r, dict) else json.loads(r)) for m, v, s, p, r in linhas]


def contar_por_celula(d: str) -> dict[tuple[str, int], int]:
    """Quantidade por setor × porte (para a regra n ≥ 5 das análises publicadas)."""
    contagem: dict[tuple[str, int], int] = {}
    for c in ler_todas(d):
        contagem[(c.setor, c.porte)] = contagem.get((c.setor, c.porte), 0) + 1
    return contagem
