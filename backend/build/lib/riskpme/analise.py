"""Análise da base anonimizada (ADR-005 e ADR-016): resumo agregado e exportação para planilha.

Regra de publicação: só se mostram médias de grupos com pelo menos N_MINIMO contribuições (células menores são
marcadas e entram apenas nos totais), para que nenhuma empresa possa ser reconhecida pelas respostas.
Maturidade de uma função = média de resposta/4 nas perguntas respondidas (o "Não sei" não entra na média e é
contado à parte), na mesma escala de 0 a 100% do motor.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .api.contribuicoes import Contribuicao
from .catalog.models import Catalogo

N_MINIMO = 5
NAO_SEI = "nao_sei"


@dataclass
class Grupo:
    nome: str
    n: int = 0
    soma: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    respondidas: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    nao_sei: dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def adicionar(self, c: Contribuicao, funcao: dict[str, str]) -> None:
        self.n += 1
        for pid, v in c.respostas.items():
            f = funcao.get(pid)
            if f is None:
                continue
            if v is None:
                self.nao_sei[f] += 1
            else:
                self.soma[f] += v / 4
                self.respondidas[f] += 1

    def maturidade(self, f: str) -> float | None:
        return self.soma[f] / self.respondidas[f] if self.respondidas[f] else None

    def pct_nao_sei(self, f: str) -> float | None:
        total = self.respondidas[f] + self.nao_sei[f]
        return self.nao_sei[f] / total if total else None


def agrupar(cat: Catalogo, contribs: list[Contribuicao]) -> dict[str, dict[str, Grupo]]:
    """Grupos por setor × porte, por setor, por porte e total."""
    funcao = {p.id: p.funcao for p in cat.perguntas}
    nome_porte = {p.nivel: p.nome for p in cat.portes}
    nome_setor = {s.id: s.nome for s in cat.setores}
    g: dict[str, dict[str, Grupo]] = {"celula": {}, "setor": {}, "porte": {}, "total": {"total": Grupo("Total")}}
    for c in contribs:
        chaves = {
            "celula": (f"{c.setor}|{c.porte}", f"{nome_setor.get(c.setor, c.setor)} · {nome_porte.get(c.porte, c.porte)}"),
            "setor": (c.setor, nome_setor.get(c.setor, c.setor)),
            "porte": (str(c.porte), nome_porte.get(c.porte, str(c.porte))),
        }
        for nivel, (k, nome) in chaves.items():
            g[nivel].setdefault(k, Grupo(nome)).adicionar(c, funcao)
        g["total"]["total"].adicionar(c, funcao)
    return g


def resumo(cat: Catalogo, contribs: list[Contribuicao]) -> str:
    """Texto com contagens e maturidade média por função do NIST CSF, respeitando n ≥ N_MINIMO."""
    if not contribs:
        return "Nenhuma contribuição registrada ainda."
    funcoes = list(cat.funcoes)
    g = agrupar(cat, contribs)
    meses = sorted({c.mes_ano for c in contribs})
    versoes = sorted({c.versao_catalogo for c in contribs})
    linhas = [f"{len(contribs)} contribuições · {meses[0]} a {meses[-1]} · versões do catálogo: {', '.join(versoes)}",
              f"Regra de publicação: médias só para grupos com n ≥ {N_MINIMO} (os demais aparecem como '-').", ""]
    cab = f"{'grupo':<46}{'n':>4}" + "".join(f"{f:>7}" for f in funcoes) + f"{'não sei':>9}"
    for nivel, titulo in (("total", "Total"), ("porte", "Por porte"), ("setor", "Por setor"), ("celula", "Setor × porte")):
        linhas += [titulo, cab]
        for k in sorted(g[nivel]):
            gr = g[nivel][k]
            pode = gr.n >= N_MINIMO
            mats = "".join(f"{(f'{gr.maturidade(f):.0%}' if pode and gr.maturidade(f) is not None else '-'):>7}"
                           for f in funcoes)
            ns_total = sum(gr.nao_sei.values())
            resp_total = sum(gr.respondidas.values()) + ns_total
            ns = f"{ns_total / resp_total:.0%}" if pode and resp_total else "-"
            linhas.append(f"{gr.nome[:45]:<46}{gr.n:>4}{mats}{ns:>9}")
        linhas.append("")
    linhas.append("Funções: " + "; ".join(f"{f} = {cat.funcoes[f].nome}" for f in funcoes))
    return "\n".join(linhas)


def exportar_csv(cat: Catalogo, contribs: list[Contribuicao], destino: Path) -> int:
    """Uma linha por contribuição e uma coluna por pergunta (vazio = não foi perguntada; nao_sei = "Não sei").
    Separador ';' e UTF-8 com BOM, para abrir direto no Excel em português."""
    ids = [p.id for p in cat.perguntas]
    nome_setor = {s.id: s.nome for s in cat.setores}
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["mes_ano", "versao_catalogo", "setor", "setor_nome", "porte", *ids])
        for c in contribs:
            valores = [NAO_SEI if (pid in c.respostas and c.respostas[pid] is None) else c.respostas.get(pid, "")
                       for pid in ids]
            w.writerow([c.mes_ano, c.versao_catalogo, c.setor, nome_setor.get(c.setor, c.setor), c.porte, *valores])
    return len(contribs)
