"""Validação semântica do catálogo — o que o Pydantic não consegue checar sozinho.

Verifica, para os 20 perfis (4 portes × 5 setores), se cada cenário FAIR recebe perguntas suficientes para que
a maturidade calculada seja significativa, e faz uma checagem de sanidade da calibração de frequência.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .linguagem import verificar_linguagem
from .models import NIVEIS_PORTE, Catalogo

MIN_PERGUNTAS_ERRO = 2      # abaixo disso a maturidade de um cenário vira "opinião de uma pergunta só"
MIN_PERGUNTAS_AVISO = 3


@dataclass
class Relatorio:
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)
    perguntas_por_perfil: dict[tuple[int, str], int] = field(default_factory=dict)
    cobertura: dict[tuple[int, str], dict[str, int]] = field(default_factory=dict)
    prob_evento: dict[tuple[int, str], tuple[float, float, float]] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.erros


def vulnerabilidade(cat: Catalogo, maturidade: float) -> float:
    pm = cat.parametros_modelo
    return pm.vulnerabilidade_min + (pm.vulnerabilidade_max - pm.vulnerabilidade_min) * (1 - maturidade)


def prob_ao_menos_um_evento(cat: Catalogo, porte: int, setor: str, maturidade: float) -> float:
    """P(≥ 1 evento de perda no ano) somando os cenários, com maturidade uniforme: 1 − e^(−ΣLEF)."""
    v = vulnerabilidade(cat, maturidade)
    lef_total = sum(cat.tef(c.id, porte, setor) * v for c in cat.cenarios)
    return 1 - math.exp(-lef_total)


def _validar_contexto(cat: Catalogo, r: Relatorio) -> None:
    ctx = cat.contexto
    for bloco in ("financeiro", "ativos", "calibracao_risco", "faixas"):
        if bloco not in ctx:
            r.erros.append(f"contexto.yaml: bloco '{bloco}' ausente")
    if r.erros:
        return

    ids_ativos = {p["id"] for p in ctx["ativos"]}
    for obrigatorio in ("ativo_critico", "tipo_dado", "registros_pessoais"):
        if obrigatorio not in ids_ativos:
            r.erros.append(f"contexto.yaml: pergunta de ativos '{obrigatorio}' ausente (RF05)")

    cenarios = {c.id for c in cat.cenarios}
    for p in ctx["ativos"]:
        for op in p.get("opcoes", []):
            for c in op.get("destaca", []):
                if c not in cenarios:
                    r.erros.append(f"contexto.yaml: {p['id']}.{op['id']} destaca cenário inexistente '{c}'")
            if p["id"] == "tipo_dado" and not op.get("fator_tipo_dado", 0) > 0:
                r.erros.append(f"contexto.yaml: tipo_dado.{op['id']} sem fator_tipo_dado > 0")

    calib = {p["id"]: p for p in ctx["calibracao_risco"]}
    try:
        if not calib["apetite_pct"]["padrao"] < calib["tolerancia_pct"]["padrao"]:
            r.erros.append("contexto.yaml: padrão de apetite deve ser menor que o de tolerância")
    except KeyError as e:
        r.erros.append(f"contexto.yaml: calibração sem {e} (RF03)")

    faixas = [f["id"] for f in ctx["faixas"]]
    if faixas != ["BAIXO", "MEDIO", "ALTO", "CRITICO"]:
        r.erros.append(f"contexto.yaml: faixas devem ser BAIXO, MEDIO, ALTO, CRITICO (recebido {faixas})")


def _valor_secundaria(ponto, registros: float, faturamento: float) -> float:
    return ponto.por_registro * registros + ponto.pct_faturamento * faturamento + ponto.fixo


def validar(cat: Catalogo) -> Relatorio:
    r = Relatorio()
    _validar_contexto(cat, r)
    erros_ling, avisos_ling = verificar_linguagem(cat)
    r.erros += erros_ling
    r.avisos += avisos_ling

    for porte in NIVEIS_PORTE:
        for setor in (s.id for s in cat.setores):
            perguntas = cat.questionario(porte, setor)
            r.perguntas_por_perfil[(porte, setor)] = len(perguntas)
            cob = {c.id: sum(1 for p in perguntas if c.id in p.cenarios) for c in cat.cenarios}
            r.cobertura[(porte, setor)] = cob
            for c, n in cob.items():
                msg = f"perfil porte {porte}/{setor}: cenário {c} com apenas {n} pergunta(s)"
                if n < MIN_PERGUNTAS_ERRO:
                    r.erros.append(msg)
                elif n < MIN_PERGUNTAS_AVISO:
                    r.avisos.append(msg)
            r.prob_evento[(porte, setor)] = tuple(
                prob_ao_menos_um_evento(cat, porte, setor, m) for m in (0.0, 0.5, 1.0)
            )

    # sanidade da calibração (âncora: hiscox2025 — 59% das PMEs relatam ataque por ano)
    for (porte, setor), (p0, p50, _) in r.prob_evento.items():
        if p0 > 0.95:
            r.avisos.append(f"porte {porte}/{setor}: P(≥1 perda/ano) sem controles = {p0:.0%} — TEF possivelmente alta")
        if porte >= 3 and p50 < 0.10:
            r.avisos.append(f"porte {porte}/{setor}: P(≥1 perda/ano) com maturidade média = {p50:.0%} — TEF possivelmente baixa")

    # sanidade da perda secundária (lognormal) no perfil padrão de cada porte
    for porte in NIVEIS_PORTE:
        pad = cat.porte(porte).padroes
        for c in cat.cenarios:
            ps = c.perda_secundaria
            med, p95 = (_valor_secundaria(x, pad.registros_pessoais, pad.faturamento_anual)
                        for x in (ps.mediana, ps.p95))
            sigma = (math.log(p95) - math.log(med)) / cat.parametros_modelo.z_p95
            if not 0.3 <= sigma <= 2.5:
                r.avisos.append(f"porte {porte}/{c.id}: σ da lognormal secundária = {sigma:.2f} (esperado 0,3–2,5)")
            if p95 > ps.teto_pct_faturamento * pad.faturamento_anual:
                r.avisos.append(f"porte {porte}/{c.id}: p95 da perda secundária acima do teto — cauda cortada demais")

    # custos dos controles: soma por porte vs. referência do CIS IG1 (cis2025cost)
    cambio = cat.custos.parametros.cambio_usd_brl
    for porte in NIVEIS_PORTE:
        total = sum(cat.custo_controle(c.id, porte).total for c in cat.controles)
        teto = cat.custos.referencia_cis_ig1_usd[porte - 1] * cambio
        if total > teto:
            r.avisos.append(f"porte {porte}: custo anual de todos os controles R$ {total:,.0f} acima da faixa CIS IG1 (R$ {teto:,.0f})")

    usados = {p.controle for p in cat.perguntas}
    for c in cat.controles:
        if c.id not in usados:
            r.avisos.append(f"controle {c.id} ({c.nome}) não é recomendado por nenhuma pergunta")

    return r
