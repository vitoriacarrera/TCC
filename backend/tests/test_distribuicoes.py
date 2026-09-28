"""Testes das distribuições (ADR-002): Beta-PERT, Lognormal e magnitude primária + secundária."""

from __future__ import annotations

import numpy as np
import pytest

from riskpme.catalog import carregar_catalogo
from riskpme.engine.distribuicoes import (
    amostrar_lognormal,
    amostrar_pert,
    lognormal_media,
    lognormal_parametros,
    pert_media,
    pert_parametros,
    prob_ao_menos_um,
)
from riskpme.engine.magnitude import Contexto, amostrar_perdas_evento, pontos_primaria, pontos_secundaria

N = 200_000


@pytest.fixture
def rng():
    return np.random.default_rng(20260924)


@pytest.fixture(scope="module")
def cat():
    return carregar_catalogo()


# ------------------------------------------------------------------ Beta-PERT
def test_pert_parametros_simetrica():
    assert pert_parametros(0, 50, 100) == pytest.approx((3.0, 3.0))


def test_pert_media_do_exemplo_do_tcc2():
    # TCC2, Passo 6: (245.000 + 4×1.150.000 + 2.850.000)/6 = 1.282.500
    assert pert_media(245_000, 1_150_000, 2_850_000) == pytest.approx(1_282_500)


def test_pert_amostras_respeitam_limites_e_media(rng):
    x = amostrar_pert(rng, 245_000, 1_150_000, 2_850_000, N)
    assert x.min() >= 245_000 and x.max() <= 2_850_000
    assert x.mean() == pytest.approx(1_282_500, rel=0.01)


def test_pert_rejeita_pontos_fora_de_ordem():
    with pytest.raises(ValueError):
        pert_parametros(10, 5, 20)


# ------------------------------------------------------------------ Lognormal
def test_lognormal_recupera_mediana_e_p95(rng):
    mu, sigma = lognormal_parametros(100_000, 1_000_000)
    x = amostrar_lognormal(rng, mu, sigma, N)
    assert np.median(x) == pytest.approx(100_000, rel=0.02)
    assert np.percentile(x, 95) == pytest.approx(1_000_000, rel=0.03)
    assert x.mean() == pytest.approx(lognormal_media(mu, sigma), rel=0.05)


def test_lognormal_tem_cauda_longa(rng):
    mu, sigma = lognormal_parametros(100_000, 1_000_000)
    x = amostrar_lognormal(rng, mu, sigma, N)
    assert x.mean() > 1.5 * np.median(x)       # assimetria à direita


def test_lognormal_respeita_teto(rng):
    mu, sigma = lognormal_parametros(100_000, 1_000_000)
    x = amostrar_lognormal(rng, mu, sigma, N, teto=500_000)
    assert x.max() == pytest.approx(500_000)


def test_prob_ao_menos_um_do_exemplo_do_tcc2():
    # TCC2, Passo 4: LEF = 0,553 → 42,5%
    assert prob_ao_menos_um(0.553) == pytest.approx(0.425, abs=0.001)


# ------------------------------------------------------------------ magnitude por cenário
CTX = Contexto(faturamento_anual=2_500_000, custo_hora_parada=1_200, registros_pessoais=10_000, fator_tipo_dado=1.0)


def test_pontos_primaria_ransomware(cat):
    # RAN: horas [8,72,240] × 1.200 + pct [0,5%; 2%; 6%] × 2,5 mi + fixo [2 mil; 10 mil; 50 mil]
    assert pontos_primaria(cat.cenario("RAN"), CTX) == pytest.approx((9_600 + 12_500 + 2_000,
                                                                       86_400 + 50_000 + 10_000,
                                                                       288_000 + 150_000 + 50_000))


def test_pontos_secundaria_usa_setor_e_tipo_de_dado(cat):
    vaz = cat.cenario("VAZ")
    med_varejo, _, _ = pontos_secundaria(vaz, CTX, cat.setor("varejo"))
    med_saude, _, _ = pontos_secundaria(vaz, CTX, cat.setor("saude"))
    assert med_saude > med_varejo                           # saúde: custo por registro 1,59×
    sensivel = Contexto(**{**CTX.__dict__, "fator_tipo_dado": 1.6})
    assert pontos_secundaria(vaz, sensivel, cat.setor("varejo"))[0] > med_varejo


def test_secundaria_ocorre_na_frequencia_declarada(cat, rng):
    vaz = cat.cenario("VAZ")
    _, sec = amostrar_perdas_evento(rng, vaz, CTX, cat.setor("varejo"), cat.parametros_modelo, N)
    assert (sec > 0).mean() == pytest.approx(vaz.perda_secundaria.probabilidade, abs=0.01)
    assert sec.max() <= vaz.perda_secundaria.teto_pct_faturamento * CTX.faturamento_anual + 1e-6


def test_secundaria_cauda_mais_longa_que_primaria(cat, rng):
    vaz = cat.cenario("VAZ")
    prim, sec = amostrar_perdas_evento(rng, vaz, CTX, cat.setor("varejo"), cat.parametros_modelo, N)
    sec_ocorreu = sec[sec > 0]
    razao_prim = np.percentile(prim, 99) / np.median(prim)
    razao_sec = np.percentile(sec_ocorreu, 99) / np.median(sec_ocorreu)
    assert razao_sec > razao_prim
