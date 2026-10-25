"""API (Etapa 3): rotas sem estado e coleta anonimizada só com consentimento (ADR-005)."""

from __future__ import annotations

import json
import sqlite3

import pytest
from fastapi.testclient import TestClient

from riskpme.api import contribuicoes
from riskpme.api.app import app


@pytest.fixture(scope="module")
def cliente():
    with TestClient(app) as c:
        yield c


def perfil(**kw):
    base = {"setor": "saude", "receita_operacional_bruta": 1_200_000, "usuarios_ti": 8,
            "registros_pessoais": "ate10k", "tipo_dado": "sensivel", "ativo_critico": "clientes",
            "apetite": "nao_sei", "tolerancia": "nao_sei"}
    return base | kw


def test_saude_e_catalogo(cliente):
    r = cliente.get("/saude").json()
    assert r["status"] == "ok" and len(r["versao_catalogo"]) == 12
    cat = cliente.get("/catalogo").json()
    assert {"instrucoes", "aviso_legal", "escala", "setores", "contexto", "matriz", "glossario"} <= set(cat)
    assert len(cat["portes"]) == 4 and cat["matriz"]["horizonte_anos"] == 5


def test_questionario_classifica_porte_e_aplica_variante(cliente):
    r = cliente.post("/questionario", json={"setor": "varejo", "receita_operacional_bruta": 60_000,
                                            "usuarios_ti": 1}).json()
    assert r["porte"]["nivel"] == 1
    assert "Faixa de receita do MEI" in r["mensagem_porte"]
    ids = [p["id"] for p in r["perguntas"]]
    assert "RS-01" in ids and len(ids) == len(set(ids))
    assert set(r["perguntas"][0]) == {"id", "funcao", "texto", "ajuda"}     # recomendação só no plano


def test_fora_do_escopo(cliente):
    r = cliente.post("/questionario", json={"setor": "varejo", "receita_operacional_bruta": 400_000_000,
                                            "usuarios_ti": 50})
    assert r.status_code == 422 and "R$ 300 milhões" in r.json()["detail"]


def test_simulacao_completa(cliente):
    q = cliente.post("/questionario", json={"setor": "saude", "receita_operacional_bruta": 1_200_000,
                                            "usuarios_ti": 8}).json()
    respostas = {p["id"]: 2 for p in q["perguntas"]}
    respostas[q["perguntas"][0]["id"]] = None                              # "Não sei"
    r = cliente.post("/simulacoes", json={"perfil": perfil(), "respostas": respostas, "semente": 1})
    assert r.status_code == 200
    d = r.json()
    assert len(d["resultado"]["cenarios"]) == 6
    assert sum(len(v) for v in d["matriz"]["celulas"].values()) == 6
    assert d["plano"]["acoes"] and d["plano"]["horizonte_anos"] == 5
    assert q["perguntas"][0]["id"] in d["resultado"]["nao_sei"]
    json.dumps(d)                                                           # tudo serializável


def test_simulacao_rejeita_entrada_invalida(cliente):
    base = {"perfil": perfil(), "respostas": {}}
    assert cliente.post("/simulacoes", json=base | {"respostas": {"XX-99": 2}}).status_code == 422
    assert cliente.post("/simulacoes", json=base | {"respostas": {"GV-01": 7}}).status_code == 422
    assert cliente.post("/simulacoes", json={"perfil": perfil(setor="banco"), "respostas": {}}).status_code == 422
    assert cliente.post("/simulacoes", json={"perfil": perfil(cpf="1"), "respostas": {}}).status_code == 422
    r = cliente.post("/simulacoes", json={"perfil": perfil(apetite="a10", tolerancia="t5"), "respostas": {}})
    assert r.status_code == 422


def test_contribuicao_desativada_sem_banco(cliente, monkeypatch):
    monkeypatch.delenv(contribuicoes.VARIAVEL_BANCO, raising=False)
    r = cliente.post("/contribuicoes", json={"consentimento": True, "setor": "varejo", "porte": 1, "respostas": {}})
    assert r.status_code == 503


def test_contribuicao_grava_so_o_permitido(cliente, monkeypatch, tmp_path):
    banco = tmp_path / "c.sqlite"
    monkeypatch.setenv(contribuicoes.VARIAVEL_BANCO, str(banco))
    sem = cliente.post("/contribuicoes", json={"consentimento": False, "setor": "varejo", "porte": 1,
                                               "respostas": {}})
    assert sem.status_code == 422 and not banco.exists()
    extra = cliente.post("/contribuicoes", json={"consentimento": True, "setor": "varejo", "porte": 1,
                                                 "respostas": {}, "receita_operacional_bruta": 1})
    assert extra.status_code == 422                                         # campo financeiro é recusado
    ok = cliente.post("/contribuicoes", json={"consentimento": True, "setor": "varejo", "porte": 1,
                                              "respostas": {"PR-01": 3, "RS-01": None}})
    assert ok.status_code == 201
    with sqlite3.connect(banco) as con:
        colunas = [c[1] for c in con.execute("PRAGMA table_info(contribuicoes)")]
        linha = con.execute("SELECT * FROM contribuicoes").fetchone()
    assert colunas == ["mes_ano", "versao_catalogo", "setor", "porte", "respostas"]
    assert linha[2:4] == ("varejo", 1) and json.loads(linha[4]) == {"PR-01": 3, "RS-01": None}
    assert contribuicoes.contar_por_celula(banco) == {("varejo", 1): 1}
