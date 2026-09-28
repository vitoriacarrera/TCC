"""Testes das regras de linguagem acessível (RNF04, ADR-007)."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from riskpme.catalog import carregar_catalogo, diretorio_padrao
from riskpme.catalog.linguagem import contem, termos_no_texto, verificar_linguagem


@pytest.fixture(scope="module")
def cat():
    return carregar_catalogo()


def test_catalogo_real_sem_jargao(cat):
    erros, _ = verificar_linguagem(cat)
    assert erros == []


def test_toda_pergunta_tem_ajuda_explicativa(cat):
    for p in cat.perguntas:
        assert len(p.ajuda) >= 40, p.id


def test_siglas_casam_so_em_maiusculas():
    assert contem("Ferramentas de IA no trabalho", "IA")
    assert not contem("Todo dia a empresa faz backup", "IA")      # "dia" não é "IA"
    assert not contem("A média diária", "IA")


def test_detecta_termos_para_sublinhar(cat):
    ids = termos_no_texto(cat.glossario, "Vocês fazem backup e usam verificação em duas etapas?")
    assert "backup" in ids and "duas_etapas" in ids


def test_todos_os_conceitos_do_resultado_estao_explicados(cat):
    ids = {c.id for c in cat.glossario.conceitos_resultado}
    for obrigatorio in ("apetite", "tolerancia", "p90", "perda_esperada", "probabilidade_anual",
                        "mapa_calor", "monte_carlo", "retorno_investimento"):
        assert obrigatorio in ids


@pytest.fixture
def copia(tmp_path: Path) -> Path:
    destino = tmp_path / "audit"
    shutil.copytree(diretorio_padrao(), destino)
    return destino


def _editar(pasta: Path, arquivo: str, fn) -> None:
    caminho = pasta / f"{arquivo}.yaml"
    dados = yaml.safe_load(caminho.read_text(encoding="utf-8"))
    fn(dados)
    caminho.write_text(yaml.safe_dump(dados, allow_unicode=True), encoding="utf-8")


def test_barra_sigla_tecnica_na_pergunta(copia):
    _editar(copia, "perguntas", lambda d: d["perguntas"][0].update(texto="Vocês usam MFA em todos os sistemas?"))
    erros, _ = verificar_linguagem(carregar_catalogo(copia))
    assert any("MFA" in e for e in erros)


def test_barra_pergunta_sem_ajuda(copia):
    _editar(copia, "perguntas", lambda d: d["perguntas"][0].pop("ajuda"))
    with pytest.raises(ValueError, match="ajuda"):
        carregar_catalogo(copia)


def test_sigla_na_recomendacao_e_permitida(cat):
    # recomendações podem citar EDR, DLP etc., porque o glossário os explica
    assert any(contem(p.recomendacao, "DLP") for p in cat.perguntas)
    erros, _ = verificar_linguagem(cat)
    assert not any("recomendacao" in e for e in erros)
