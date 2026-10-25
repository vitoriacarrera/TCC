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
    julgamento: list[str] = field(default_factory=list)   # vai para as Limitações (P1)
    pendentes: list[str] = field(default_factory=list)

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
    for bloco in ("financeiro", "ativos", "calibracao_risco", "matriz"):
        if bloco not in ctx:
            r.erros.append(f"contexto.yaml: bloco '{bloco}' ausente")
    if r.erros:
        return

    perguntas = {p["id"]: p for bloco in ("financeiro", "ativos", "calibracao_risco") for p in ctx[bloco]}
    for obrigatorio in ("receita_operacional_bruta", "custo_hora_parada", "ativo_critico", "tipo_dado",
                        "registros_pessoais", "usuarios_ti", "apetite_pct", "tolerancia_pct"):
        if obrigatorio not in perguntas:
            r.erros.append(f"contexto.yaml: pergunta '{obrigatorio}' ausente")
    if r.erros:
        return

    # revisão S3/S4/C-APET: nenhuma entrada cai num valor padrão escolhido por nós
    for pid in ("receita_operacional_bruta", "registros_pessoais", "usuarios_ti", "apetite_pct", "tolerancia_pct"):
        p = perguntas[pid]
        if "padrao" in p:
            r.erros.append(f"contexto.yaml: {pid} não pode ter valor padrão (revisão S3/S4/C-APET)")
        if not p.get("obrigatorio"):
            r.erros.append(f"contexto.yaml: {pid} deve ser obrigatória (revisão S3/S4/C-APET)")

    cenarios = {c.id for c in cat.cenarios}
    controles = {c.id for c in cat.controles}
    ids_perguntas = {p.id for p in cat.perguntas}
    for p in ctx["ativos"]:
        for op in p.get("opcoes", []):
            for c in op.get("destaca", []):
                if c not in cenarios:
                    r.erros.append(f"contexto.yaml: {p['id']}.{op['id']} destaca cenário inexistente '{c}'")
    tipo = perguntas["tipo_dado"]
    if any("fator_tipo_dado" in op for op in tipo["opcoes"]):
        r.erros.append("contexto.yaml: tipo_dado não multiplica mais o prejuízo (revisão C-DADO)")
    for c in tipo.get("selo_em_controles", []):
        if c not in controles:
            r.erros.append(f"contexto.yaml: selo de tipo_dado em controle inexistente '{c}'")
    for q in tipo.get("selo_em_perguntas", []):
        if q not in ids_perguntas:
            r.erros.append(f"contexto.yaml: selo de tipo_dado em pergunta inexistente '{q}'")

    # "Não sei dizer" do apetite e da tolerância (revisão C-APET)
    if not any(op["id"] == "nao_sei" for op in perguntas["apetite_pct"]["opcoes"]):
        r.erros.append("contexto.yaml: apetite_pct sem a opção 'nao_sei'")
    por_setor = perguntas["tolerancia_pct"].get("nao_sei_por_setor", {})
    fontes = {f.id for f in cat.fontes}
    for s in cat.setores:
        v = por_setor.get(s.id)
        if v is None:
            r.erros.append(f"contexto.yaml: tolerância 'não sei' sem valor para o setor {s.id}")
            continue
        if v.get("fonte") not in fontes:
            r.erros.append(f"contexto.yaml: tolerância 'não sei' de {s.id} com fonte inexistente '{v.get('fonte')}'")
        apetite_ns = next(op["valor"] for op in perguntas["apetite_pct"]["opcoes"] if op["id"] == "nao_sei")
        if not v["valor"] > apetite_ns:
            r.erros.append(f"contexto.yaml: tolerância 'não sei' de {s.id} deve ser maior que o apetite 'não sei'")

    m = ctx["matriz"]
    if [n["nivel"] for n in m.get("impacto", [])] != [1, 2, 3] or [n["nivel"] for n in m.get("probabilidade", [])] != [1, 2, 3]:
        r.erros.append("contexto.yaml: a matriz deve ter 3 níveis de impacto e 3 de probabilidade")
    somas = sorted(x for c in m.get("cores", []) for x in c["soma"])
    if somas != [2, 3, 4, 5, 6]:
        r.erros.append(f"contexto.yaml: as cores da matriz devem cobrir as somas 2 a 6 (recebido {somas})")


def _valor_secundaria(ponto, registros: float, faturamento: float) -> float:
    return ponto.por_registro * registros + ponto.pct_faturamento * faturamento + ponto.fixo


def perfis_de_teste(cat: Catalogo) -> list[tuple[int, float, int]]:
    """Combinações (porte, faturamento, registros) usadas só nas checagens de sanidade — nunca na simulação.

    Não há valor "típico" por porte (revisão S3): percorre os LIMITES de receita de cada porte (`rob_min` e
    `rob_max`; o porte 1, que começa em 0, só usa o limite superior) × todas as faixas de `registros_pessoais`.
    """
    faixas = next(p for p in cat.contexto["ativos"] if p["id"] == "registros_pessoais")["opcoes"]
    registros = [int(o["valor"]) for o in faixas]
    perfis = []
    for porte in sorted(cat.portes, key=lambda x: x.nivel):
        limites = [porte.rob_max] if porte.rob_min == 0 else [porte.rob_min, porte.rob_max]
        perfis += [(porte.nivel, f, n) for f in limites for n in registros]
    return perfis


def parametros_sem_dado(cat: Catalogo) -> tuple[list[str], list[str]]:
    """(julgamento, pendente): parâmetros que vão para as Limitações do TCC (princípio P1)."""
    julg: list[str] = []
    pend: list[str] = []
    for s in cat.setores:
        for c, m in s.multiplicador_tef.items():
            if m.pendente:
                pend.append(f"setor {s.id}, frequência de {c}: valor neutro à espera de dado")
            if m.fonte == "julgamento":
                julg.append(f"setor {s.id}, frequência de {c}")
    for c in cat.cenarios:
        if "julgamento" in c.fonte:
            julg.append(f"cenário {c.id}: parte das magnitudes e/ou da frequência")
    if "julgamento" in cat.custos.parametros.fonte:
        julg.append("custos: horas de esforço por controle e GB por usuário em backup")
    return julg, pend


def validar(cat: Catalogo) -> Relatorio:
    r = Relatorio()
    _validar_contexto(cat, r)
    erros_ling, avisos_ling = verificar_linguagem(cat)
    r.erros += erros_ling
    r.avisos += avisos_ling

    for porte in NIVEIS_PORTE:
        for setor in (s.id for s in cat.setores):
            perguntas = cat.questionario(porte, setor)
            if porte == 1:   # quem trabalha sozinho vê as variantes (Q-SOLO/Q-RSMEI): cobertura no pior caso
                sozinho = cat.questionario(porte, setor, usuarios=1)
                perguntas = sozinho if len(sozinho) <= len(perguntas) else perguntas
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

    # sanidade da calibração (âncora: csbs2026, 12,9% das empresas com evento de perda no ano; revisão CJ1)
    for (porte, setor), (p0, p50, _) in r.prob_evento.items():
        if p0 > 0.95:
            r.avisos.append(f"porte {porte}/{setor}: P(≥1 perda/ano) sem controles = {p0:.0%}: TEF possivelmente alta")
        if not 0.05 <= p50 <= 0.40:
            r.avisos.append(f"porte {porte}/{setor}: P(≥1 perda/ano) com maturidade média = {p50:.0%}, fora de 5% a 40%")

    # sanidade da perda secundária (lognormal) nos perfis de teste — um aviso por cenário, com a contagem
    perfis = perfis_de_teste(cat)
    for c in cat.cenarios:
        ps = c.perda_secundaria
        fora_sigma: list[str] = []
        acima_teto: list[str] = []
        for porte, fat, reg in perfis:
            med, p95 = (_valor_secundaria(x, reg, fat) for x in (ps.mediana, ps.p95))
            sigma = (math.log(p95) - math.log(med)) / cat.parametros_modelo.z_p95
            rotulo = f"porte {porte}, faturamento R$ {fat:,.0f}, {reg} registros (σ={sigma:.2f})"
            if not 0.3 <= sigma <= 2.5:
                fora_sigma.append(rotulo)
            if p95 > ps.teto_pct_faturamento * fat:
                acima_teto.append(rotulo)
        if fora_sigma:
            r.avisos.append(f"{c.id}: σ da lognormal secundária fora de 0,3–2,5 em {len(fora_sigma)}/{len(perfis)}"
                            f" perfis de teste (ex.: {fora_sigma[0]})")
        if acima_teto:
            r.avisos.append(f"{c.id}: p95 da perda secundária acima do teto em {len(acima_teto)}/{len(perfis)}"
                            f" perfis de teste (ex.: {acima_teto[0]})")

    # custos dos controles: soma por porte vs. referência do CIS IG1 (cis2025cost), com o nº de empregados do
    # limite superior de cada Tier do CIS como usuários (pior caso)
    cambio = cat.custos.parametros.cambio_usd_brl
    for porte in NIVEIS_PORTE:
        usuarios = cat.custos.referencia_cis_ig1_empregados[porte - 1]
        total = sum(cat.custo_controle(c.id, porte, usuarios).total for c in cat.controles)
        teto = cat.custos.referencia_cis_ig1_usd[porte - 1] * cambio
        if total > teto:
            r.avisos.append(f"porte {porte} ({usuarios} usuários): custo anual de todos os controles"
                            f" R$ {total:,.0f} acima da faixa CIS IG1 (R$ {teto:,.0f})")

    r.julgamento, r.pendentes = parametros_sem_dado(cat)

    usados = {p.controle for p in cat.perguntas}
    for c in cat.controles:
        if c.id not in usados:
            r.avisos.append(f"controle {c.id} ({c.nome}) não é recomendado por nenhuma pergunta")

    return r
