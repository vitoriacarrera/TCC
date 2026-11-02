"""Base anonimizada para pesquisa (ADR-005, ADR-016): gravada só com consentimento, isolada da simulação.

Grava apenas setor, nível de porte, respostas por id de pergunta, o resultado sem valores em R$ (api/pesquisa.py),
versão do catálogo e mês/ano. Não grava valores
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
import socket
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
    respostas        TEXT    NOT NULL,   -- JSON {id_pergunta: 0..4 | null}
    resultado        TEXT                -- JSON do resumo_pesquisa (sem valores em R$), api/pesquisa.py
)
"""
_POSTGRES = """
CREATE TABLE IF NOT EXISTS contribuicoes (
    mes_ano          TEXT     NOT NULL CHECK (mes_ano ~ '^[0-9]{4}-[0-9]{2}$'),
    versao_catalogo  TEXT     NOT NULL,
    setor            TEXT     NOT NULL,
    porte            SMALLINT NOT NULL CHECK (porte BETWEEN 1 AND 4),
    respostas        JSONB    NOT NULL,
    resultado        JSONB
)
"""
# Bases criadas antes da revisão de 02/11/2026 não têm a coluna "resultado".
_MIGRAR_POSTGRES = "ALTER TABLE contribuicoes ADD COLUMN IF NOT EXISTS resultado JSONB"


@dataclass(frozen=True)
class Contribuicao:
    mes_ano: str
    versao_catalogo: str
    setor: str
    porte: int
    respostas: dict[str, int | None]
    resultado: dict | None = None


def destino() -> str | None:
    """Conexão configurada, ou None quando a coleta está desativada."""
    # Tolera o endereço colado com espaços ou entre aspas, como o Neon mostra no exemplo "psql '...'".
    v = (os.environ.get(VARIAVEL_BANCO) or "").strip().strip("'\"").strip()
    if v.startswith("psql "):
        v = v[5:].strip().strip("'\"").strip()
    return v or None


def _postgres(d: str) -> bool:
    return d.startswith(("postgres://", "postgresql://"))


def _parametros_ipv4(d: str) -> dict:
    """Parâmetros de conexão com o endereço IPv4 do servidor já resolvido (`hostaddr`).

    O plano gratuito do Render não tem saída por IPv6, e o endereço do Neon também resolve para IPv6: sem isto, a
    conexão pode tentar só o IPv6 e falhar com "Network is unreachable". O nome do servidor continua em `host`, que
    o TLS usa para conferir o certificado e o Neon usa (SNI) para achar o banco certo.
    """
    from psycopg.conninfo import conninfo_to_dict

    params = conninfo_to_dict(d)
    host = str(params.get("host") or "")
    if host and "hostaddr" not in params and not host.startswith("/") and "," not in host:
        try:
            ips = socket.getaddrinfo(host, int(params.get("port") or 5432), socket.AF_INET, socket.SOCK_STREAM)
        except OSError:
            return params
        if ips:
            params["hostaddr"] = ips[0][4][0]
    return params


@contextmanager
def _conexao(d: str) -> Iterator[tuple[object, str]]:
    """(conexão, marcador de parâmetro). Cria a tabela na primeira vez. Confirma ao sair sem erro."""
    if _postgres(d):
        import psycopg  # só é necessário em produção

        with psycopg.connect(**_parametros_ipv4(d), connect_timeout=10) as con:
            # DDL só quando falta algo: assim a API pode usar um usuário que só tem permissão de INSERT
            # (docs/seguranca.md, "Banco com menor privilégio"), sem CREATE nem ALTER.
            existe = con.execute("SELECT to_regclass('public.contribuicoes') IS NOT NULL").fetchone()[0]
            if not existe:
                con.execute(_POSTGRES)
            elif not con.execute("SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' "
                                 "AND table_name = 'contribuicoes' AND column_name = 'resultado'").fetchone():
                con.execute(_MIGRAR_POSTGRES)
            yield con, "%s"
    else:
        caminho = Path(d)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(caminho)
        try:
            con.execute(_SQLITE)
            if "resultado" not in [c[1] for c in con.execute("PRAGMA table_info(contribuicoes)")]:
                con.execute("ALTER TABLE contribuicoes ADD COLUMN resultado TEXT")
            yield con, "?"
            con.commit()
        finally:
            con.close()


_INSERIR = {
    "%s": "INSERT INTO contribuicoes (mes_ano, versao_catalogo, setor, porte, respostas, resultado) "
          "VALUES (%s, %s, %s, %s, %s, %s)",
    "?": "INSERT INTO contribuicoes (mes_ano, versao_catalogo, setor, porte, respostas, resultado) "
         "VALUES (?, ?, ?, ?, ?, ?)",
}


def gravar(d: str, versao_catalogo: str, setor: str, porte: int, respostas: dict[str, int | None],
           resultado: dict | None = None, hoje: date | None = None) -> None:
    mes = (hoje or date.today()).strftime("%Y-%m")
    res = json.dumps(resultado, sort_keys=True) if resultado is not None else None
    with _conexao(d) as (con, m):
        con.execute(_INSERIR[m], (mes, versao_catalogo, setor, porte, json.dumps(respostas, sort_keys=True), res))


def ler_todas(d: str) -> list[Contribuicao]:
    """Todas as contribuições, para a análise da autora (nunca exposto pela API)."""
    if not _postgres(d) and not Path(d).exists():
        return []
    with _conexao(d) as (con, _):
        linhas = con.execute("SELECT mes_ano, versao_catalogo, setor, porte, respostas, resultado FROM contribuicoes "
                             "ORDER BY mes_ano, setor, porte").fetchall()

    def _json(x):
        return x if (x is None or isinstance(x, dict)) else json.loads(x)
    return [Contribuicao(m, v, s, int(p), _json(r), _json(res)) for m, v, s, p, r, res in linhas]


def contar_por_celula(d: str) -> dict[tuple[str, int], int]:
    """Quantidade por setor × porte (para a regra n ≥ 5 das análises publicadas)."""
    contagem: dict[tuple[str, int], int] = {}
    for c in ler_todas(d):
        contagem[(c.setor, c.porte)] = contagem.get((c.setor, c.porte), 0) + 1
    return contagem
