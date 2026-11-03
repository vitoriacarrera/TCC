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
    assert set(r["perguntas"][0]) == {"id", "funcao", "texto", "respostas", "ajuda"}   # recomendação só no plano
    assert all(len(p["respostas"]) == 5 for p in r["perguntas"])


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
    d = cliente.post("/simulacoes", json={"perfil": p, "respostas": respostas}).json()
    return {"comprovante": d["comprovante_contribuicao"], "resultado": d["resumo_pesquisa"]}


def test_contribuicao_desativada_sem_banco(cliente, monkeypatch):
    monkeypatch.delenv(contribuicoes.VARIAVEL_BANCO, raising=False)
    comp = _simular_mei(cliente, {})
    r = cliente.post("/contribuicoes", json={"consentimento": True, "setor": "varejo", "porte": 1, "respostas": {},
                                             **comp})
    assert r.status_code == 503


def test_contribuicao_grava_so_o_permitido(cliente, monkeypatch, tmp_path):
    banco = tmp_path / "c.sqlite"
    monkeypatch.setenv(contribuicoes.VARIAVEL_BANCO, str(banco))
    resp = {"PR-01": 3, "RS-01": None}
    comp = _simular_mei(cliente, resp)
    base = {"consentimento": True, "setor": "varejo", "porte": 1, "respostas": resp, **comp}
    sem = cliente.post("/contribuicoes", json=base | {"consentimento": False})
    assert sem.status_code == 422 and not banco.exists()
    extra = cliente.post("/contribuicoes", json=base | {"receita_operacional_bruta": 1})
    assert extra.status_code == 422                                         # campo financeiro é recusado
    ok = cliente.post("/contribuicoes", json=base)
    assert ok.status_code == 201
    with sqlite3.connect(banco) as con:
        colunas = [c[1] for c in con.execute("PRAGMA table_info(contribuicoes)")]
        linha = con.execute("SELECT * FROM contribuicoes").fetchone()
    assert colunas == ["mes_ano", "versao_catalogo", "setor", "porte", "respostas", "resultado"]
    assert linha[2:4] == ("varejo", 1) and json.loads(linha[4]) == resp
    assert contribuicoes.contar_por_celula(str(banco)) == {("varejo", 1): 1}


# ------------------------------------------------------------------ segurança (OWASP API Security Top 10, 2023)
def test_contribuicao_exige_comprovante_da_mesma_simulacao(cliente, monkeypatch, tmp_path):
    monkeypatch.setenv(contribuicoes.VARIAVEL_BANCO, str(tmp_path / "c.sqlite"))
    comp = _simular_mei(cliente, {"PR-01": 3})
    base = {"consentimento": True, "setor": "varejo", "porte": 1, "respostas": {"PR-01": 3}}
    assert cliente.post("/contribuicoes", json=base | {**comp, "comprovante": "123.abc"}).status_code == 403
    assert cliente.post("/contribuicoes", json=base | {"respostas": {"PR-01": 0},
                                                       **comp}).status_code == 403   # respostas trocadas
    assert cliente.post("/contribuicoes", json=base | {"porte": 2, **comp}).status_code == 403
    assert cliente.post("/contribuicoes", json=base | {**comp}).status_code == 201


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


# ------------------------------------------------------------------ base anonimizada: PostgreSQL e análise (ADR-016)
def _contrib(setor, porte, respostas, mes="2026-11"):
    return contribuicoes.Contribuicao(mes, "v1", setor, porte, respostas)


def test_analise_mostra_tudo_a_autora_e_marca_grupos_pequenos(tmp_path):
    from riskpme.analise import N_MINIMO, agrupar, exportar_csv, resumo
    from riskpme.api.app import catalogo
    cat = catalogo()
    dados = [_contrib("varejo", 1, {"PR-01": 4, "RS-01": None})] * N_MINIMO + [_contrib("saude", 3, {"PR-01": 0})]
    g = agrupar(cat, dados)
    assert g["celula"]["varejo|1"].maturidade("PR") == 1.0
    assert g["celula"]["varejo|1"].pct_nao_sei("RS") == 1.0
    texto = resumo(cat, dados)
    linha_saude = next(x for x in texto.splitlines() if x.startswith("Saúde ·"))
    assert "*" in linha_saude and "0%" in linha_saude                       # n = 1: mostrado à autora, marcado
    linha_varejo = next(x for x in texto.splitlines() if x.startswith("Varejo & Comércio ·"))
    assert "*" not in linha_varejo and "100%" in linha_varejo
    publicavel = resumo(cat, dados, minimo=N_MINIMO)
    linha_saude = next(x for x in publicavel.splitlines() if x.startswith("Saúde ·"))
    assert "0%" not in linha_saude                                         # tabela para publicação esconde n < 5
    destino = tmp_path / "dados.csv"
    assert exportar_csv(cat, dados, destino) == N_MINIMO + 1
    linhas = destino.read_text(encoding="utf-8-sig").splitlines()
    cab = linhas[0].split(";")
    primeira = dict(zip(cab, linhas[1].split(";"), strict=True))
    assert primeira["PR-01"] == "4" and primeira["RS-01"] == "nao_sei" and primeira["GV-01"] == ""


@pytest.mark.skipif(not __import__("os").environ.get("RISKPME_TESTE_POSTGRES"),
                    reason="defina RISKPME_TESTE_POSTGRES=postgresql://... para testar com um PostgreSQL real")
def test_postgres_grava_e_le(cliente, monkeypatch):
    import os
    url = os.environ["RISKPME_TESTE_POSTGRES"]
    import psycopg
    with psycopg.connect(url) as con:
        con.execute("DROP TABLE IF EXISTS contribuicoes")
    monkeypatch.setenv(contribuicoes.VARIAVEL_BANCO, url)
    resp = {"PR-01": 3, "RS-01": None}
    comp = _simular_mei(cliente, resp)
    r = cliente.post("/contribuicoes", json={"consentimento": True, "setor": "varejo", "porte": 1,
                                             "respostas": resp, **comp})
    assert r.status_code == 201
    lidas = contribuicoes.ler_todas(url)
    assert len(lidas) == 1 and lidas[0].respostas == resp and lidas[0].porte == 1
    with psycopg.connect(url) as con:
        tipo = con.execute("SELECT data_type FROM information_schema.columns WHERE table_name = 'contribuicoes' "
                           "AND column_name = 'respostas'").fetchone()[0]
    assert tipo == "jsonb"


def test_banco_fora_do_ar_responde_503(cliente, monkeypatch):
    monkeypatch.setenv(contribuicoes.VARIAVEL_BANCO, "postgresql://ninguem@127.0.0.1:1/nada")
    resp = {"PR-01": 3}
    comp = _simular_mei(cliente, resp)
    r = cliente.post("/contribuicoes", json={"consentimento": True, "setor": "varejo", "porte": 1,
                                             "respostas": resp, **comp})
    assert r.status_code == 503 and "127.0.0.1" not in r.text


def test_contribuicao_guarda_resultado_sem_reais_e_nao_aceita_adulterado(cliente, monkeypatch, tmp_path):
    banco = tmp_path / "c.sqlite"
    monkeypatch.setenv(contribuicoes.VARIAVEL_BANCO, str(banco))
    resp = {"PR-01": 1, "RS-01": None}
    comp = _simular_mei(cliente, resp)
    res = comp["resultado"]
    assert set(res["cenarios"]) == {"RAN", "VAZ", "FRA", "IND", "TER", "IA"}
    texto = json.dumps(res)
    assert "R$" not in texto and all(k not in texto for k in ("receita_operacional", "custo_anual", "p90", "reducao"))
    base = {"consentimento": True, "setor": "varejo", "porte": 1, "respostas": resp}
    adulterado = json.loads(json.dumps(res))
    adulterado["cenarios"]["RAN"]["cor"] = "verde" if res["cenarios"]["RAN"]["cor"] != "verde" else "vermelho"
    assert cliente.post("/contribuicoes", json=base | comp | {"resultado": adulterado}).status_code == 403
    assert cliente.post("/contribuicoes", json=base | comp | {"resultado": None}).status_code == 403
    assert cliente.post("/contribuicoes", json=base | comp).status_code == 201
    lida = contribuicoes.ler_todas(str(banco))[0]
    assert lida.resultado == res
    assert [a["bloco"] for a in lida.resultado["acoes"]] and {a["bloco"] for a in lida.resultado["acoes"]} <= {
        "comece", "preparo", "depois"}


def test_sqlite_antigo_ganha_coluna_resultado(tmp_path):
    banco = tmp_path / "antigo.sqlite"
    with sqlite3.connect(banco) as con:
        con.execute("CREATE TABLE contribuicoes (mes_ano TEXT, versao_catalogo TEXT, setor TEXT, porte INTEGER, "
                    "respostas TEXT)")
        con.execute("INSERT INTO contribuicoes VALUES ('2026-11', 'v0', 'varejo', 1, '{}')")
    contribuicoes.gravar(str(banco), "v1", "saude", 3, {"PR-01": 2}, {"x": 1})
    lidas = contribuicoes.ler_todas(str(banco))
    assert sorted(((c.versao_catalogo, c.resultado) for c in lidas), key=lambda x: x[0]) == [("v0", None), ("v1", {"x": 1})]


def test_resumo_com_resultados(tmp_path):
    from riskpme.analise import N_MINIMO, exportar_csv, resumo
    from riskpme.api.app import catalogo
    cat = catalogo()
    r = {"perda_esperada_pct_receita": 0.01, "chance_algum_prejuizo_horizonte": 0.4, "nao_sei": 0, "horizonte_anos": 5,
         "cenarios": {"RAN": {"cor": "amarelo", "impacto": 3, "probabilidade": 1, "ruptura": True,
                              "chance_horizonte": 0.05, "maturidade_prevencao": 0.5, "maturidade_resposta": 0.4,
                              "perda_esperada_pct_receita": 0.002}},
         "acoes": [{"controle": "8.13", "bloco": "comece"}, {"controle": "5.24", "bloco": "preparo"}]}
    dados = [_contrib("varejo", 1, {"PR-01": 2}) for _ in range(N_MINIMO)]
    dados = [contribuicoes.Contribuicao(c.mes_ano, c.versao_catalogo, c.setor, c.porte, c.respostas, r) for c in dados]
    texto = resumo(cat, dados)
    assert "Sequestro de dados" in texto and "100%" in texto
    assert "Fazer cópias de segurança e testar a recuperação" in texto
    destino = tmp_path / "d.csv"
    exportar_csv(cat, dados, destino)
    cab, linha = destino.read_text(encoding="utf-8-sig").splitlines()[:2]
    d = dict(zip(cab.split(";"), linha.split(";"), strict=True))
    assert d["RAN_cor"] == "amarelo" and d["acoes_comece"] == "8.13" and d["acoes_preparo"] == "5.24"


def test_comprovante_aceita_resultado_reserializado_pelo_navegador():
    res = {"a": 1.0, "b": [0.0, 0.25], "c": {"d": 2.0}}
    c = seguranca.emitir_comprovante("varejo", 1, {"PR-01": 3}, res)
    como_js = {"a": 1, "b": [0, 0.25], "c": {"d": 2}}                      # JSON.stringify(1.0) == "1"
    assert seguranca.comprovante_valido(c, "varejo", 1, {"PR-01": 3}, como_js)
    assert not seguranca.comprovante_valido(c, "varejo", 1, {"PR-01": 3}, {**como_js, "a": 2})


def test_resultados_aparecem_com_poucas_contribuicoes():
    from riskpme.analise import resumo
    from riskpme.api.app import catalogo
    r = {"perda_esperada_pct_receita": 0.01, "chance_algum_prejuizo_horizonte": 0.4, "nao_sei": 0, "horizonte_anos": 5,
         "cenarios": {"RAN": {"cor": "vermelho", "impacto": 3, "probabilidade": 2, "ruptura": False,
                              "chance_horizonte": 0.2, "maturidade_prevencao": 0.5, "maturidade_resposta": 0.4,
                              "perda_esperada_pct_receita": 0.002}},
         "acoes": [{"controle": "8.13", "bloco": "comece"}]}
    texto = resumo(catalogo(), [contribuicoes.Contribuicao("2026-11", "v1", "varejo", 1, {"PR-01": 2}, r)])
    assert "Riscos (1 contribuição com resultado) * menos de 5" in texto
    assert "Fazer cópias de segurança e testar a recuperação" in texto


@pytest.mark.skipif(not __import__("os").environ.get("RISKPME_TESTE_POSTGRES"),
                    reason="defina RISKPME_TESTE_POSTGRES=postgresql://... para testar com um PostgreSQL real")
def test_postgres_usuario_so_insert_grava_e_nao_le():
    """docs/seguranca.md: a API usa um usuário que só pode inserir; quem invadir a API não lê a base."""
    import os
    from urllib.parse import urlsplit, urlunsplit

    import psycopg
    url = os.environ["RISKPME_TESTE_POSTGRES"]
    contribuicoes.gravar(url, "v", "saude", 3, {"PR-01": 2}, {"x": 1})           # cria a tabela como dono
    with psycopg.connect(url, autocommit=True) as con:
        con.execute("DROP ROLE IF EXISTS teste_coleta")
        con.execute("CREATE ROLE teste_coleta LOGIN PASSWORD 'teste'")
        con.execute("GRANT USAGE ON SCHEMA public TO teste_coleta")
        con.execute("GRANT INSERT ON contribuicoes TO teste_coleta")
    partes = urlsplit(url)
    limitado = urlunsplit(partes._replace(netloc=f"teste_coleta:teste@{partes.hostname}:{partes.port or 5432}"))
    try:
        contribuicoes.gravar(limitado, "v", "varejo", 1, {"PR-01": 1}, {"x": 2})
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            contribuicoes.ler_todas(limitado)
    finally:
        with psycopg.connect(url, autocommit=True) as con:
            con.execute("REVOKE ALL ON contribuicoes FROM teste_coleta")
            con.execute("REVOKE ALL ON SCHEMA public FROM teste_coleta")
            con.execute("DROP ROLE teste_coleta")


@pytest.mark.parametrize("valor", ["  /tmp/x.sqlite ", "'/tmp/x.sqlite'", "psql '/tmp/x.sqlite'", '"/tmp/x.sqlite"'])
def test_endereco_do_banco_colado_com_aspas(monkeypatch, valor):
    monkeypatch.setenv(contribuicoes.VARIAVEL_BANCO, valor)
    assert contribuicoes.destino() == "/tmp/x.sqlite"


def test_conexao_postgres_prefere_ipv4(monkeypatch):
    """Render (plano gratuito) não sai por IPv6: o endereço IPv4 vai em hostaddr, o nome continua em host (TLS/SNI)."""
    chamadas = []

    def falso(host, porta, familia, tipo):
        chamadas.append((host, porta, familia))
        return [(familia, tipo, 6, "", ("203.0.113.7", porta))]
    monkeypatch.setattr(contribuicoes.socket, "getaddrinfo", falso)
    p = contribuicoes._parametros_ipv4("postgresql://u:s@ep-x-pooler.neon.tech/neondb?sslmode=require")
    assert p["host"] == "ep-x-pooler.neon.tech" and p["hostaddr"] == "203.0.113.7" and p["sslmode"] == "require"
    assert chamadas == [("ep-x-pooler.neon.tech", 5432, contribuicoes.socket.AF_INET)]
    assert "hostaddr" not in contribuicoes._parametros_ipv4("postgresql://u@localhost/db?host=/tmp")


def test_exportar_latex(tmp_path):
    from riskpme.analise import exportar_latex
    from riskpme.api.app import catalogo
    cat = catalogo()
    r = {"perda_esperada_pct_receita": 0.01, "chance_algum_prejuizo_horizonte": 0.4, "nao_sei": 0, "horizonte_anos": 5,
         "cenarios": {"RAN": {"cor": "amarelo", "impacto": 3, "probabilidade": 1, "ruptura": True,
                              "chance_horizonte": 0.05, "maturidade_prevencao": 0.5, "maturidade_resposta": 0.4,
                              "perda_esperada_pct_receita": 0.002}},
         "acoes": [{"controle": "8.13", "bloco": "comece"}]}
    dados = [contribuicoes.Contribuicao("2026-11", "v1", "varejo", 1, {"PR-01": 2, "GV-01": None}, r)]
    destino = tmp_path / "t.tex"
    assert exportar_latex(cat, dados, destino) == 1
    tex = destino.read_text(encoding="utf-8")
    assert r"\newcommand{\pesqN}{1}" in tex and r"\newcommand{\pesqTabelas}" in tex and r"\label{tab:pesq-riscos}" in tex and r"\label{tab:pesq-acoes}" in tex
    assert r"50\%" in tex and "Comércio*" in tex and "ilustrativa" in tex
    exportar_latex(cat, dados, destino, minimo=5)
    assert "tab:pesq-riscos" not in destino.read_text(encoding="utf-8")
    exportar_latex(cat, [], destino)
    assert "Nenhuma contribuição" in destino.read_text(encoding="utf-8")


def test_estudos_variacao_e_incerteza():
    from pathlib import Path

    from riskpme import estudos
    from riskpme.api.app import catalogo
    cat = catalogo()
    alt = estudos.catalogo_variado(estudos._faixa_v(0.05, 0.5))
    assert alt.parametros_modelo.vulnerabilidade_max == 0.5 and cat.parametros_modelo.vulnerabilidade_max == 0.35
    horas = estudos.catalogo_variado(estudos._horas(2.0))
    assert list(horas.custos.controles["5.1"].horas_anuais) == [2 * h for h in cat.custos.controles["5.1"].horas_anuais]
    perfil, resp = estudos.carregar_clinica(Path(__file__).parents[2] / "docs" / "exemplos" / "clinica-epp.json")
    inc = estudos.estudo_incerteza(cat, perfil, resp, sementes=2)
    assert inc["perda_media"] > 0 and 0 <= inc["cores_iguais"] <= 1
    a = estudos.rodar(cat, perfil, resp)
    assert a == estudos.rodar(cat, perfil, resp)           # semente fixa: reprodutível
