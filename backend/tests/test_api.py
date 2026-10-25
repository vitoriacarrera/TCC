"""API (Etapa 3): rotas sem estado e coleta anonimizada só com consentimento (ADR-005)."""

from __future__ import annotations

import json
import sqlite3

import pytest
from fastapi.testclient import TestClient

from riskpme.api import contribuicoes, seguranca
from riskpme.api.app import app


@pytest.fixture(scope="module")
def cliente():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def _zera_limites():
    for m in seguranca.INSTANCIAS:
        m.janelas.clear()


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


def _simular_mei(cliente, respostas):
    p = perfil(setor="varejo", receita_operacional_bruta=60_000, usuarios_ti=1, tipo_dado="cadastral")
    return cliente.post("/simulacoes", json={"perfil": p, "respostas": respostas}).json()["comprovante_contribuicao"]


def test_contribuicao_desativada_sem_banco(cliente, monkeypatch):
    monkeypatch.delenv(contribuicoes.VARIAVEL_BANCO, raising=False)
    comp = _simular_mei(cliente, {})
    r = cliente.post("/contribuicoes", json={"consentimento": True, "setor": "varejo", "porte": 1, "respostas": {},
                                             "comprovante": comp})
    assert r.status_code == 503


def test_contribuicao_grava_so_o_permitido(cliente, monkeypatch, tmp_path):
    banco = tmp_path / "c.sqlite"
    monkeypatch.setenv(contribuicoes.VARIAVEL_BANCO, str(banco))
    resp = {"PR-01": 3, "RS-01": None}
    comp = _simular_mei(cliente, resp)
    base = {"consentimento": True, "setor": "varejo", "porte": 1, "respostas": resp, "comprovante": comp}
    sem = cliente.post("/contribuicoes", json=base | {"consentimento": False})
    assert sem.status_code == 422 and not banco.exists()
    extra = cliente.post("/contribuicoes", json=base | {"receita_operacional_bruta": 1})
    assert extra.status_code == 422                                         # campo financeiro é recusado
    ok = cliente.post("/contribuicoes", json=base)
    assert ok.status_code == 201
    with sqlite3.connect(banco) as con:
        colunas = [c[1] for c in con.execute("PRAGMA table_info(contribuicoes)")]
        linha = con.execute("SELECT * FROM contribuicoes").fetchone()
    assert colunas == ["mes_ano", "versao_catalogo", "setor", "porte", "respostas"]
    assert linha[2:4] == ("varejo", 1) and json.loads(linha[4]) == resp
    assert contribuicoes.contar_por_celula(banco) == {("varejo", 1): 1}


# ------------------------------------------------------------------ segurança (OWASP API Security Top 10, 2023)
def test_contribuicao_exige_comprovante_da_mesma_simulacao(cliente, monkeypatch, tmp_path):
    monkeypatch.setenv(contribuicoes.VARIAVEL_BANCO, str(tmp_path / "c.sqlite"))
    comp = _simular_mei(cliente, {"PR-01": 3})
    base = {"consentimento": True, "setor": "varejo", "porte": 1, "respostas": {"PR-01": 3}}
    assert cliente.post("/contribuicoes", json=base | {"comprovante": "123.abc"}).status_code == 403
    assert cliente.post("/contribuicoes", json=base | {"respostas": {"PR-01": 0},
                                                       "comprovante": comp}).status_code == 403   # respostas trocadas
    assert cliente.post("/contribuicoes", json=base | {"porte": 2, "comprovante": comp}).status_code == 403
    assert cliente.post("/contribuicoes", json=base | {"comprovante": comp}).status_code == 201


def test_comprovante_vence():
    c = seguranca.emitir_comprovante("varejo", 1, {"PR-01": 3}, agora=1000.0)
    assert seguranca.comprovante_valido(c, "varejo", 1, {"PR-01": 3}, agora=1000.0 + 60)
    assert not seguranca.comprovante_valido(c, "varejo", 1, {"PR-01": 3},
                                            agora=1000.0 + seguranca.VALIDADE_COMPROVANTE_S + 1)


@pytest.mark.parametrize("ajuste", [
    {"custo_hora_parada": "Infinity"}, {"custo_hora_parada": "NaN"}, {"receita_operacional_bruta": 1e300},
    {"usuarios_ti": 10**9}, {"setor": "x" * 200}, {"setor": "../../etc"},
])
def test_entradas_absurdas_viram_422_e_nao_500(cliente, ajuste):
    corpo = json.dumps({"perfil": perfil(), "respostas": {}})
    for k, v in ajuste.items():
        antigo = json.dumps(perfil()[k]) if k in perfil() else None
        novo = v if v in ("Infinity", "NaN") else json.dumps(v)
        corpo = corpo.replace(f'"{k}": {antigo}', f'"{k}": {novo}') if antigo else corpo
    if "custo_hora_parada" in ajuste:
        corpo = corpo.replace('"tolerancia": "nao_sei"', f'"tolerancia": "nao_sei", "custo_hora_parada": {ajuste["custo_hora_parada"]}')
    r = cliente.post("/simulacoes", content=corpo, headers={"content-type": "application/json"})
    assert r.status_code == 422


def test_resposta_booleana_e_semente_negativa_recusadas(cliente):
    assert cliente.post("/simulacoes", json={"perfil": perfil(), "respostas": {"GV-01": True}}).status_code == 422
    assert cliente.post("/simulacoes", json={"perfil": perfil(), "respostas": {}, "semente": -1}).status_code == 422


def test_corpo_grande_recusado(cliente):
    enorme = json.dumps({"perfil": perfil(), "respostas": {f"k{i}": 1 for i in range(20_000)}})
    r = cliente.post("/simulacoes", content=enorme, headers={"content-type": "application/json"})
    assert r.status_code == 413
    r = cliente.post("/simulacoes", json={"perfil": perfil(), "respostas": {f"k{i}": 1 for i in range(150)}})
    assert r.status_code == 422 and len(r.text) < 2000                      # mais de 100 respostas; erro curto


def test_limite_de_requisicoes(cliente):
    q = {"setor": "varejo", "receita_operacional_bruta": 60_000, "usuarios_ti": 1}
    codigos = [cliente.post("/questionario", json=q).status_code for _ in range(seguranca.LIMITES["/questionario"][0] + 1)]
    assert codigos[:-1] == [200] * seguranca.LIMITES["/questionario"][0]
    assert codigos[-1] == 429


def test_cabecalhos_de_seguranca(cliente):
    h = cliente.get("/saude").headers
    assert h["x-content-type-options"] == "nosniff"
    assert h["cache-control"] == "no-store"
    assert "default-src 'none'" in h["content-security-policy"]
    assert h["x-frame-options"] == "DENY"
    assert "server" not in h


def test_cors_so_para_origem_permitida(cliente):
    pre = {"Access-Control-Request-Method": "POST"}
    ruim = cliente.options("/simulacoes", headers=pre | {"Origin": "https://site-malicioso.example"})
    assert ruim.headers.get("access-control-allow-origin") is None
    bom = cliente.options("/simulacoes", headers=pre | {"Origin": "http://localhost:5173"})
    assert bom.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_limite_esquece_clientes_parados(monkeypatch):
    m = seguranca.LimiteRequisicoes(app=None, limites={"/x": (2, 10)})
    t = [0.0]
    monkeypatch.setattr(seguranca.time, "monotonic", lambda: t[0])
    assert m._permitir("/x", "a") is None and m._permitir("/x", "a") is None
    assert m._permitir("/x", "a") is not None                               # terceiro na janela: bloqueado
    t[0] = 11.0
    assert m._permitir("/x", "b") is None
    assert ("/x", "a") not in m.janelas                                     # "a" esquecido depois da janela
