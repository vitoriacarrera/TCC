"""Motor completo (Etapa 2): maturidade, Monte Carlo, matriz 3 × 3 e plano de ação."""

from __future__ import annotations

import math
import time

import numpy as np
import pytest

from riskpme.catalog import carregar_catalogo
from riskpme.engine.maturidade import maturidade_por_cenario, vulnerabilidade
from riskpme.engine.perfil import Perfil, resolver
from riskpme.engine.plano import media_lognormal_com_teto, perda_esperada_analitica, plano_de_acao
from riskpme.engine.simulacao import poisson_truncada, simular


@pytest.fixture(scope="module")
def cat():
    return carregar_catalogo()


def perfil(**kw):
    base = {"setor": "saude", "receita_operacional_bruta": 1_200_000, "usuarios_ti": 8,
            "registros_pessoais": "ate10k", "tipo_dado": "sensivel", "ativo_critico": "clientes",
            "apetite": "nao_sei", "tolerancia": "nao_sei"}
    return Perfil(**(base | kw))


def respostas(cat, p: Perfil, valor):
    res = resolver(cat, p)
    return {q.id: valor for q in cat.questionario(res.porte, res.setor, res.usuarios)}


# ------------------------------------------------------------------ perfil
def test_perfil_resolve_porte_custo_hora_e_nao_sei(cat):
    r = resolver(cat, perfil())
    assert r.porte == 3
    assert r.contexto.custo_hora_parada == pytest.approx(1_200_000 / 2080)
    assert r.custo_hora_estimado
    assert r.apetite_pct == 0.01                 # isa320
    assert r.tolerancia_pct == 0.045             # saúde: menor valor entre os setores
    assert r.contexto.registros_pessoais == 5000


def test_perfil_rejeita_tolerancia_menor_que_apetite(cat):
    with pytest.raises(ValueError):
        resolver(cat, perfil(apetite="a10", tolerancia="t5"))


# ------------------------------------------------------------------ maturidade
def test_maturidade_vai_de_0_a_1(cat):
    p = perfil()
    res = resolver(cat, p)
    perguntas = cat.questionario(res.porte, res.setor, res.usuarios)
    assert set(maturidade_por_cenario(cat, perguntas, respostas(cat, p, 4)).values()) == {1.0}
    assert set(maturidade_por_cenario(cat, perguntas, respostas(cat, p, 0)).values()) == {0.0}
    nao_sei = maturidade_por_cenario(cat, perguntas, {})          # tudo "Não sei" = 1 de 4
    assert set(nao_sei.values()) == {0.25}
    pm = cat.parametros_modelo
    assert vulnerabilidade(cat, 1.0) == pm.vulnerabilidade_min
    assert vulnerabilidade(cat, 0.0) == pm.vulnerabilidade_max


def test_resposta_fora_do_questionario_e_rejeitada(cat):
    with pytest.raises(ValueError):
        simular(cat, perfil(), {"PERGUNTA-INEXISTENTE": 3}, iteracoes=1000, semente=1)


# ------------------------------------------------------------------ Monte Carlo
def test_poisson_truncada_nunca_zera_e_tem_media_certa():
    rng = np.random.default_rng(0)
    for lam in (0.01, 0.5, 3.0):
        n = poisson_truncada(rng, lam, 200_000)
        assert n.min() >= 1
        assert n.mean() == pytest.approx(lam / (1 - math.exp(-lam)), rel=0.02)


def test_simulacao_reprodutivel_com_semente(cat):
    p = perfil()
    a = simular(cat, p, respostas(cat, p, 2), iteracoes=5000, semente=7)
    b = simular(cat, p, respostas(cat, p, 2), iteracoes=5000, semente=7)
    assert a.to_dict() == b.to_dict()


def test_10_mil_iteracoes_em_menos_de_um_segundo(cat):
    p = perfil(setor="industria", receita_operacional_bruta=20_000_000, usuarios_ti=80)
    t = time.perf_counter()
    simular(cat, p, respostas(cat, p, 2), semente=1)
    assert time.perf_counter() - t < 1.0                    # RNF06


def test_monte_carlo_bate_com_a_media_analitica(cat):
    p = perfil()
    resp = respostas(cat, p, 2)
    r = simular(cat, p, resp, iteracoes=100_000, semente=3)
    analitica = sum(perda_esperada_analitica(cat, resolver(cat, p), resp).values())
    assert r.perda_esperada_total == pytest.approx(analitica, rel=0.08)


def test_mais_maturidade_menos_perda(cat):
    p = perfil()
    fraca = simular(cat, p, respostas(cat, p, 0), iteracoes=20_000, semente=5)
    forte = simular(cat, p, respostas(cat, p, 4), iteracoes=20_000, semente=5)
    assert forte.perda_esperada_total < fraca.perda_esperada_total
    assert forte.chance_algum_prejuizo < fraca.chance_algum_prejuizo


def test_p90_quando_ocorre_nao_some_em_cenario_raro(cat):
    p = perfil()
    r = simular(cat, p, respostas(cat, p, 4), iteracoes=10_000, semente=9)
    ran = r.cenario("RAN")
    assert ran.chance_ano < 0.10
    assert ran.p90_quando_ocorre > 0                         # ADR-012: impacto condicional


def test_matriz_soma_dos_niveis_e_ruptura(cat):
    p = perfil()
    r = simular(cat, p, respostas(cat, p, 1), iteracoes=10_000, semente=11)
    for c in r.cenarios:
        soma = c.nivel_impacto + c.nivel_probabilidade
        assert c.cor == {2: "verde", 3: "verde", 4: "amarelo", 5: "vermelho", 6: "vermelho"}[soma]
        assert c.ruptura == (c.nivel_impacto == 3 and c.nivel_probabilidade == 1)


def test_destaque_pelo_ativo_critico(cat):
    p = perfil(ativo_critico="financeiro")
    r = simular(cat, p, respostas(cat, p, 2), iteracoes=2000, semente=1)
    assert {c.id for c in r.cenarios if c.destaque} == {"FRA"}


def test_nao_sei_aparece_no_resultado(cat):
    p = perfil()
    resp = respostas(cat, p, 3)
    resp["PR-10"] = None
    r = simular(cat, p, resp, iteracoes=2000, semente=1)
    assert "PR-10" in r.nao_sei


# ------------------------------------------------------------------ plano de ação
def test_media_lognormal_com_teto():
    rng = np.random.default_rng(0)
    x = np.minimum(rng.lognormal(1.0, 1.2, 1_000_000), 20.0)
    assert media_lognormal_com_teto(1.0, 1.2, 20.0) == pytest.approx(x.mean(), rel=0.01)


def test_plano_priorizado_e_coerente(cat):
    p = perfil(setor="varejo", receita_operacional_bruta=60_000, usuarios_ti=1, tipo_dado="cadastral")
    resp = respostas(cat, p, 1)
    plano = plano_de_acao(cat, p, resp)
    assert plano.acoes, "com respostas fracas deve haver ações"
    assert [a.prioridade for a in plano.acoes] == list(range(1, len(plano.acoes) + 1))
    com_rosi = [a.rosi for a in plano.acoes if a.rosi is not None]
    assert com_rosi == sorted(com_rosi, reverse=True)
    assert all(a.reducao_perda_anual > 0 for a in plano.acoes)
    assert plano.limite_investimento == pytest.approx(plano.perda_esperada_atual / math.e)


def test_plano_vazio_quando_tudo_e_sempre(cat):
    p = perfil()
    assert plano_de_acao(cat, p, respostas(cat, p, 4)).acoes == []


def test_plano_usa_texto_da_variante_e_selo(cat):
    p = perfil(setor="varejo", receita_operacional_bruta=60_000, usuarios_ti=1, tipo_dado="sensivel")
    plano = plano_de_acao(cat, p, respostas(cat, p, 0))
    acao_ia = next(a for a in plano.acoes if "GV-06" in a.perguntas)
    assert acao_ia.recomendacoes[0].startswith("Escolha as ferramentas de IA")


def test_selo_de_privacidade_pelo_tipo_de_dado(cat):
    p = perfil()                                             # saúde, EPP, dados sensíveis
    plano = plano_de_acao(cat, p, respostas(cat, p, 0))
    com_selo = {a.controle for a in plano.acoes if a.selo}
    assert "5.34" in com_selo                                # LGPD (GV-04)
    assert all("sensíveis" in a.selo for a in plano.acoes if a.selo)


def test_plano_traz_transferencia_para_ruptura(cat):
    p = perfil()
    plano = plano_de_acao(cat, p, respostas(cat, p, 1), cenarios_ruptura=["RAN"])
    assert plano.ruptura[0]["cenario"] == "RAN"
    assert "corretor de seguros" in plano.ruptura[0]["transferencia"]


# ------------------------------------------------------------------ revisões M1, M2 e M3 (25/10)
def test_m1_probabilidade_pela_chance_em_5_anos(cat):
    from riskpme.engine.simulacao import chance_em, horizonte
    assert horizonte(cat) == 5 == cat.custos.parametros.vida_util_anos
    p = perfil()
    r = simular(cat, p, respostas(cat, p, 2), iteracoes=5000, semente=3)
    limites = {n["nivel"]: n["maximo"] for n in cat.contexto["matriz"]["probabilidade"]}
    for c in r.cenarios:
        assert c.chance_horizonte == pytest.approx(chance_em(c.lef, 5))
        assert c.chance_horizonte > c.chance_ano
        esperado = 1 if c.chance_horizonte < limites[1] else 2 if c.chance_horizonte < limites[2] else 3
        assert c.nivel_probabilidade == esperado
    assert r.horizonte_anos == 5
    assert r.chance_algum_prejuizo_horizonte == pytest.approx(chance_em(sum(c.lef for c in r.cenarios), 5))


def test_m1_matriz_deixa_de_ter_uma_coluna_so(cat):
    p = perfil()
    r = simular(cat, p, respostas(cat, p, 2), iteracoes=5000, semente=3)
    assert len({c.nivel_probabilidade for c in r.cenarios}) >= 2


def test_m2_periodo_ruim_monotonico_e_reprodutivel(cat):
    p = perfil()
    resp = respostas(cat, p, 1)
    a = plano_de_acao(cat, p, resp, semente=7)
    b = plano_de_acao(cat, p, resp, semente=7)
    assert [x.reducao_periodo_ruim for x in a.acoes] == [x.reducao_periodo_ruim for x in b.acoes]
    assert a.horizonte_anos == 5 and a.perda_periodo_ruim_atual > 0
    assert all(0 <= x.reducao_periodo_ruim <= a.perda_periodo_ruim_atual for x in a.acoes)
    assert any(x.reducao_periodo_ruim > 0 for x in a.acoes)


def test_m2_sorteio_comum_nao_aumenta_perda_quando_lef_cai(cat):
    from riskpme.engine.plano import sortear_periodo
    res = resolver(cat, perfil())
    s = sortear_periodo(cat, res, 5, 4000, semente=1)
    lef = {c.id: 0.05 for c in cat.cenarios}
    menor = {c: v / 2 for c, v in lef.items()}
    assert np.all(s.perda(menor) <= s.perda(lef))


def test_m2_ruptura_destaca_acoes_de_preparacao(cat):
    p = perfil()
    resp = respostas(cat, p, 1)
    plano = plano_de_acao(cat, p, resp, cenarios_ruptura=["RAN"])
    prep = tuple(cat.contexto["matriz"]["selo_ruptura"]["preparacao"]["subcategorias"])
    marcadas = [a for a in plano.acoes if a.protege_ruptura]
    assert marcadas, "backup e plano de incidentes devem proteger contra ruptura de ransomware"
    assert "8.13" in {a.controle for a in marcadas}
    for a in marcadas:
        assert a.protege_ruptura == ["RAN"]
        subcats = {q.id: q.subcategoria for q in cat.perguntas}
        assert any(subcats[pid].startswith(prep) for pid in a.perguntas)
    assert plano.ruptura[0]["preparacao"] == [a.controle for a in marcadas]
    assert plano.ruptura[0]["texto_preparacao"]
    assert all(not a.protege_ruptura for a in plano_de_acao(cat, p, resp).acoes)   # sem ruptura, sem marca


def test_m3_mei_fora_da_saude_ve_o_selo_de_privacidade(cat):
    p = perfil(setor="varejo", receita_operacional_bruta=60_000, usuarios_ti=1, tipo_dado="sensivel")
    plano = plano_de_acao(cat, p, respostas(cat, p, 0))
    com_selo = [a for a in plano.acoes if a.selo]
    assert com_selo and any("ID-02" in a.perguntas for a in com_selo)
