"""Testes do catálogo de auditoria (Etapa 1)."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from riskpme.catalog import carregar_catalogo, diretorio_padrao
from riskpme.catalog.models import NIVEIS_PORTE
from riskpme.catalog.validate import MIN_PERGUNTAS_ERRO, validar


@pytest.fixture(scope="module")
def cat():
    return carregar_catalogo()


def test_catalogo_real_carrega_e_valida(cat):
    r = validar(cat)
    assert r.ok, r.erros


def test_quatro_portes_e_cinco_setores_do_tcc1(cat):
    assert [p.nivel for p in cat.portes] == [1, 2, 3, 4]
    assert {s.id for s in cat.setores} == {"varejo", "servicos", "saude", "industria", "tecnologia"}
    # Tabela 3.1 do TCC1
    assert cat.porte(1).receita_anual_max == 81_000
    assert cat.porte(3).receita_anual_max == 4_800_000


@pytest.mark.parametrize("porte", NIVEIS_PORTE)
@pytest.mark.parametrize("setor", ["varejo", "servicos", "saude", "industria", "tecnologia"])
def test_todo_perfil_cobre_todos_os_cenarios(cat, porte, setor):
    perguntas = cat.questionario(porte, setor)
    for c in cat.cenarios:
        n = sum(1 for p in perguntas if c.id in p.cenarios)
        assert n >= MIN_PERGUNTAS_ERRO, f"{porte}/{setor}: cenário {c.id} com {n} pergunta(s)"


def test_questionario_cresce_com_o_porte(cat):
    for s in cat.setores:
        tamanhos = [len(cat.questionario(p, s.id)) for p in NIVEIS_PORTE]
        assert tamanhos == sorted(tamanhos), f"{s.id}: {tamanhos}"
        assert tamanhos[0] <= 15, "MEI deve ter questionário curto"


def test_perguntas_setoriais_so_aparecem_no_setor(cat):
    ids_saude = {p.id for p in cat.questionario(4, "saude")}
    ids_varejo = {p.id for p in cat.questionario(4, "varejo")}
    assert "SAU-01" in ids_saude and "SAU-01" not in ids_varejo
    assert "VAR-01" in ids_varejo and "VAR-01" not in ids_saude


def test_tef_do_perfil_combina_multiplicadores(cat):
    base = cat.cenario("RAN").tef_base
    # saúde tem multiplicador 1,4 para ransomware; EPP (nível 3) é a referência 1,0
    assert cat.tef("RAN", 3, "saude") == pytest.approx(base * 1.4)
    # cenário sem multiplicador no setor assume 1,0
    assert cat.tef("TER", 3, "saude") == pytest.approx(cat.cenario("TER").tef_base)
    # MEI é menos exposto que média empresa
    assert cat.tef("VAZ", 1, "varejo") < cat.tef("VAZ", 4, "varejo")


# ---------------------------------------------------------------------- o validador pega erros de digitação
@pytest.fixture
def copia_catalogo(tmp_path: Path) -> Path:
    destino = tmp_path / "audit"
    shutil.copytree(diretorio_padrao(), destino)
    return destino


def _editar(pasta: Path, arquivo: str, fn) -> None:
    caminho = pasta / f"{arquivo}.yaml"
    dados = yaml.safe_load(caminho.read_text(encoding="utf-8"))
    fn(dados)
    caminho.write_text(yaml.safe_dump(dados, allow_unicode=True), encoding="utf-8")


def test_detecta_controle_inexistente(copia_catalogo):
    _editar(copia_catalogo, "perguntas", lambda d: d["perguntas"][0].update(controle="99.9"))
    with pytest.raises(ValueError, match="controle inexistente"):
        carregar_catalogo(copia_catalogo)


def test_detecta_cenario_inexistente(copia_catalogo):
    _editar(copia_catalogo, "perguntas", lambda d: d["perguntas"][0]["cenarios"].update(XYZ=2))
    with pytest.raises(ValueError, match="cenário inexistente"):
        carregar_catalogo(copia_catalogo)


def test_detecta_peso_invalido(copia_catalogo):
    _editar(copia_catalogo, "perguntas", lambda d: d["perguntas"][0]["cenarios"].update(RAN=5))
    with pytest.raises(ValueError, match="peso"):
        carregar_catalogo(copia_catalogo)


def test_detecta_perda_primaria_fora_de_ordem(copia_catalogo):
    _editar(copia_catalogo, "cenarios", lambda d: d["cenarios"][0]["perda_primaria"].update(fixo=[100, 50, 200]))
    with pytest.raises(ValueError, match="mín ≤ mais provável ≤ máx"):
        carregar_catalogo(copia_catalogo)


def test_detecta_secundaria_com_p95_menor_que_mediana(copia_catalogo):
    _editar(copia_catalogo, "cenarios",
            lambda d: d["cenarios"][0]["perda_secundaria"].update(p95={"pct_faturamento": 0.0001}))
    with pytest.raises(ValueError, match="p95"):
        carregar_catalogo(copia_catalogo)


def test_todo_cenario_tem_primaria_e_secundaria(cat):
    for c in cat.cenarios:
        assert 0 <= c.perda_secundaria.probabilidade <= 1
        assert c.perda_primaria.fixo[2] > 0 or c.perda_primaria.pct_faturamento[2] > 0


def test_nist_csf_2_com_seis_funcoes(cat):
    assert set(cat.funcoes) == {"GV", "ID", "PR", "DE", "RS", "RC"}
    usadas = {p.funcao for p in cat.perguntas}
    assert usadas == {"GV", "ID", "PR", "DE", "RS", "RC"}
    # MEI também passa por todas as funções
    assert {p.funcao for p in cat.questionario(1, "varejo")} >= {"GV", "ID", "PR", "RS", "RC"}


def test_detecta_cenario_sem_cobertura(copia_catalogo):
    # remove todas as perguntas de IA => perfis ficam sem medir esse cenário
    _editar(copia_catalogo, "perguntas",
            lambda d: d.update(perguntas=[p for p in d["perguntas"] if "IA" not in p["cenarios"]]))
    r = validar(carregar_catalogo(copia_catalogo))
    assert not r.ok
    assert any("cenário IA" in e for e in r.erros)


# ---------------------------------------------------------------------- custos dos controles
def test_todo_controle_tem_custo_para_todo_porte(cat):
    for c in cat.controles:
        for porte in NIVEIS_PORTE:
            assert cat.custo_controle(c.id, porte, usuarios=10).total >= 0


def test_custo_cresce_com_o_porte(cat):
    # mesmo nº de usuários: o porte muda só as horas e o custo da hora
    for c in cat.controles:
        custos = [cat.custo_controle(c.id, p, usuarios=10).total for p in NIVEIS_PORTE]
        assert custos == sorted(custos), f"{c.id}: {custos}"


def test_custo_nao_diminui_com_usuarios(cat):
    for c in cat.controles:
        for porte in NIVEIS_PORTE:
            custos = [cat.custo_controle(c.id, porte, u).total for u in (1, 5, 50, 500)]
            assert custos == sorted(custos), f"{c.id}/porte {porte}: {custos}"


def test_memoria_de_calculo_gerenciador_de_senhas(cat):
    # 5.17, porte 3, 50 usuários: Bitwarden Teams US$ 4 × 50 × 12 × câmbio + (12/3 + 4) h × R$ 85
    par = cat.custos.parametros
    d = cat.custo_controle("5.17", 3, usuarios=50)
    assert d.usuarios == 50
    assert d.licencas == pytest.approx(4 * 50 * 12 * par.cambio_usd_brl)
    assert d.mao_de_obra == pytest.approx((12 / 3 + 4) * par.custo_hora[2])


def test_backup_escala_com_usuarios(cat):
    # 8.13: Backblaze US$ 6,95/TB/mês × (usuários × GB por usuário ÷ 1024) × 12 × câmbio
    par = cat.custos.parametros
    for u in (3, 40):
        d = cat.custo_controle("8.13", 2, usuarios=u)
        tb = u * par.gb_por_usuario / 1024
        assert d.licencas == pytest.approx(6.95 * tb * 12 * par.cambio_usd_brl)


def test_treinamento_cobra_hora_por_usuario(cat):
    # 6.3: 1 h por pessoa/ano — diferença entre 20 e 10 usuários = 10 h × custo da hora do porte
    par = cat.custos.parametros
    d10, d20 = (cat.custo_controle("6.3", 3, u) for u in (10, 20))
    assert d20.total - d10.total == pytest.approx(10 * par.custo_hora[2])


def test_decomposicao_fixo_mais_por_usuario(cat):
    from riskpme.catalog.custos import custo_fixo_e_por_usuario
    for c in cat.controles:
        fixo, por_u = custo_fixo_e_por_usuario(cat.custos, c.id, 4)
        assert cat.custo_controle(c.id, 4, 37).total == pytest.approx(fixo + por_u * 37)


@pytest.mark.parametrize("usuarios", [0, -1])
def test_usuarios_invalido(cat, usuarios):
    with pytest.raises(ValueError):
        cat.custo_controle("5.17", 1, usuarios)


# ---------------------------------------------------------------------- revisão S3/S4: sem padrões por porte
def test_portes_nao_tem_valores_padrao(cat):
    for p in cat.portes:
        assert not hasattr(p, "padroes")
    assert not hasattr(cat.custos.parametros, "usuarios")
    assert not hasattr(cat.custos.parametros, "dados_tb")


def test_entradas_do_gestor_sao_obrigatorias(cat):
    perguntas = {p["id"]: p for b in ("financeiro", "ativos") for p in cat.contexto[b]}
    for pid in ("faturamento_anual", "registros_pessoais", "usuarios_ti"):
        assert perguntas[pid].get("obrigatorio") is True
        assert perguntas[pid].get("padrao") != "porte"
    assert perguntas["usuarios_ti"]["minimo"] == 1


def test_detecta_padrao_por_porte_reintroduzido(copia_catalogo):
    def volta_padrao(d):
        for p in d["financeiro"]:
            if p["id"] == "faturamento_anual":
                p["padrao"] = "porte"
    _editar(copia_catalogo, "contexto", volta_padrao)
    r = validar(carregar_catalogo(copia_catalogo))
    assert any("faturamento_anual" in e and "S3/S4" in e for e in r.erros)


def test_perfis_de_teste_cobrem_limites_e_faixas(cat):
    from riskpme.catalog.validate import perfis_de_teste
    perfis = perfis_de_teste(cat)
    faixas = {o["valor"] for p in cat.contexto["ativos"] if p["id"] == "registros_pessoais" for o in p["opcoes"]}
    assert {n for _, _, n in perfis} == faixas
    assert {f for _, f, _ in perfis} == {p.receita_anual_max for p in cat.portes}
    assert len(perfis) == len(faixas) * (1 + 2 * 3)   # porte 1: só limite superior; demais: os dois limites


def test_custo_hora_bate_com_salario_e_encargos(cat):
    for mo in cat.custos.mao_de_obra:
        assert mo.custo_hora_calculado == pytest.approx(mo.salario_mensal * (1 + mo.encargos) / 220, abs=0.05)


def test_custo_total_dentro_da_referencia_cis(cat):
    cambio = cat.custos.parametros.cambio_usd_brl
    for porte in NIVEIS_PORTE:
        usuarios = cat.custos.referencia_cis_ig1_empregados[porte - 1]
        total = sum(cat.custo_controle(c.id, porte, usuarios).total for c in cat.controles)
        assert total <= cat.custos.referencia_cis_ig1_usd[porte - 1] * cambio


def test_toda_fonte_de_custo_esta_no_bibtex(cat):
    bib = (diretorio_padrao().parent / "docs" / "referencias.bib").read_text(encoding="utf-8")
    fontes = {p.fonte for p in cat.custos.precos} | {f for m in cat.custos.mao_de_obra for f in m.fonte}
    for f in fontes - {"julgamento", "tcc1"}:
        assert f"{{{f}," in bib, f"fonte {f} sem entrada em docs/referencias.bib"


def test_detecta_preco_inexistente(copia_catalogo):
    _editar(copia_catalogo, "custos",
            lambda d: d["controles"]["5.17"]["licencas"][0].update(preco="nao_existe"))
    with pytest.raises(ValueError, match="preço inexistente"):
        carregar_catalogo(copia_catalogo)
