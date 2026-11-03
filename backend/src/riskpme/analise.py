"""Análise da base anonimizada (ADR-005 e ADR-016): resumo agregado e exportação para planilha.

Inclui os resultados anonimizados (riscos por cenário e ações recomendadas), quando a contribuição os traz.

A autora vê todos os grupos, inclusive os pequenos (revisão de 02/11/2026: a amostra do TCC deve ser pequena).
Grupos com menos de N_PUBLICACAO contribuições aparecem marcados com "*": no texto, descreva-os sem combinar setor,
porte e respostas de um jeito que permita reconhecer a empresa (ADR-005, item 3). `minimo` permite esconder os
grupos pequenos ao gerar uma tabela para publicação.
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

N_PUBLICACAO = 5          # abaixo disso, o grupo é marcado com "*"
N_MINIMO = N_PUBLICACAO  # compatibilidade com quem importava o nome antigo
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


def resumo(cat: Catalogo, contribs: list[Contribuicao], minimo: int = 1) -> str:
    """Contagens e maturidade média por função do NIST CSF. Mostra grupos com n ≥ `minimo` (padrão: todos) e marca
    com "*" os que têm menos de N_PUBLICACAO."""
    if not contribs:
        return "Nenhuma contribuição registrada ainda."
    funcoes = list(cat.funcoes)
    g = agrupar(cat, contribs)
    meses = sorted({c.mes_ano for c in contribs})
    versoes = sorted({c.versao_catalogo for c in contribs})
    plural = "contribuição" if len(contribs) == 1 else "contribuições"
    linhas = [f"{len(contribs)} {plural} · {meses[0]} a {meses[-1]} · versões do catálogo: {', '.join(versoes)}",
              f"* = grupo com menos de {N_PUBLICACAO} contribuições: use no texto sem permitir reconhecer a empresa."
              + (f" Grupos com n < {minimo} aparecem como '-'." if minimo > 1 else ""), ""]
    cab = f"{'grupo':<56}{'n':>4}" + "".join(f"{f:>7}" for f in funcoes) + f"{'não sei':>9}"
    for nivel, titulo in (("total", "Total"), ("porte", "Por porte"), ("setor", "Por setor"), ("celula", "Setor × porte")):
        linhas += [titulo, cab]
        for k in sorted(g[nivel]):
            gr = g[nivel][k]
            pode = gr.n >= minimo
            mats = "".join(f"{(f'{gr.maturidade(f):.0%}' if pode and gr.maturidade(f) is not None else '-'):>7}"
                           for f in funcoes)
            ns_total = sum(gr.nao_sei.values())
            resp_total = sum(gr.respondidas.values()) + ns_total
            ns = f"{ns_total / resp_total:.0%}" if pode and resp_total else "-"
            marca = "*" if gr.n < N_PUBLICACAO else " "
            linhas.append(f"{(gr.nome[:53] + ' ' + marca):<56}{gr.n:>4}{mats}{ns:>9}")
        linhas.append("")
    linhas.append("Funções: " + "; ".join(f"{f} = {cat.funcoes[f].nome}" for f in funcoes))
    linhas += _resumo_resultados(cat, contribs, minimo)
    return "\n".join(linhas)


def _resumo_resultados(cat: Catalogo, contribs: list[Contribuicao], minimo: int = 1) -> list[str]:
    """Riscos e ações mais recomendadas, a partir do resultado anonimizado (só contribuições que o trazem)."""
    com = [c for c in contribs if c.resultado]
    if not com or len(com) < minimo:
        return ["", f"Resultados: {len(com)} contribuição(ões) com resultado."]
    n = len(com)
    aviso = f" * menos de {N_PUBLICACAO}" if n < N_PUBLICACAO else ""
    linhas = ["", f"Riscos ({n} {'contribuição' if n == 1 else 'contribuições'} com resultado){aviso}",
              f"{'cenário':<56}{'vermelho':>9}{'amarelo':>9}{'verde':>7}{'ruptura':>9}{'chance 5a':>11}{'perda/receita':>15}"]
    for cen in cat.cenarios:
        rs = [c.resultado["cenarios"][cen.id] for c in com if cen.id in c.resultado.get("cenarios", {})]
        if not rs:
            continue
        cor = {k: sum(r["cor"] == k for r in rs) / len(rs) for k in ("vermelho", "amarelo", "verde")}
        rup = sum(bool(r["ruptura"]) for r in rs) / len(rs)
        chance = sum(r["chance_horizonte"] for r in rs) / len(rs)
        perda = sum(r["perda_esperada_pct_receita"] for r in rs) / len(rs)
        linhas.append(f"{cen.nome[:55]:<56}{cor['vermelho']:>9.0%}{cor['amarelo']:>9.0%}{cor['verde']:>7.0%}"
                      f"{rup:>9.0%}{chance:>11.1%}{perda:>15.3%}")
    perda_total = sum(c.resultado["perda_esperada_pct_receita"] for c in com) / n
    linhas.append(f"Perda esperada média: {perda_total:.3%} da receita por ano")
    contagem: dict[str, int] = defaultdict(int)
    for c in com:
        for a in c.resultado.get("acoes", []):
            if a.get("bloco") == "comece":
                contagem[a["controle"]] += 1
    if contagem:
        acao = {k.id: k.acao for k in cat.controles}
        linhas += ["", "Ações mais indicadas em \"Comece por aqui\" (% das contribuições)"]
        for ctrl, k in sorted(contagem.items(), key=lambda x: -x[1])[:10]:
            linhas.append(f"{k / n:>6.0%}  {ctrl:<5} {acao.get(ctrl, ctrl)}")
    return linhas


def exportar_csv(cat: Catalogo, contribs: list[Contribuicao], destino: Path) -> int:
    """Uma linha por contribuição e uma coluna por pergunta (vazio = não foi perguntada; nao_sei = "Não sei").
    Separador ';' e UTF-8 com BOM, para abrir direto no Excel em português."""
    ids = [p.id for p in cat.perguntas]
    nome_setor = {s.id: s.nome for s in cat.setores}
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        cens = [c.id for c in cat.cenarios]
        campos = ("cor", "impacto", "probabilidade", "ruptura", "chance_horizonte", "maturidade_prevencao",
                  "maturidade_resposta", "perda_esperada_pct_receita")
        res_cab = ["perda_esperada_pct_receita", "chance_algum_prejuizo_horizonte", "acoes_comece", "acoes_preparo",
                   "acoes_depois"] + [f"{cid}_{k}" for cid in cens for k in campos]
        w.writerow(["mes_ano", "versao_catalogo", "setor", "setor_nome", "porte", *ids, *res_cab])
        for c in contribs:
            valores = [NAO_SEI if (pid in c.respostas and c.respostas[pid] is None) else c.respostas.get(pid, "")
                       for pid in ids]
            r = c.resultado or {}
            blocos = {b: ",".join(a["controle"] for a in r.get("acoes", []) if a.get("bloco") == b)
                      for b in ("comece", "preparo", "depois")}
            por_cen = [r.get("cenarios", {}).get(cid, {}).get(k, "") for cid in cens for k in campos]
            extra = [r.get("perda_esperada_pct_receita", ""), r.get("chance_algum_prejuizo_horizonte", ""),
                     blocos["comece"], blocos["preparo"], blocos["depois"], *por_cen] if r else [""] * len(res_cab)
            w.writerow([c.mes_ano, c.versao_catalogo, c.setor, nome_setor.get(c.setor, c.setor), c.porte, *valores,
                        *extra])
    return len(contribs)


# ---------------------------------------------------------------------------------------------------------------------
# Tabelas em LaTeX para a monografia (seção "Análise das respostas dos empresários")
# ---------------------------------------------------------------------------------------------------------------------

_ESCAPE = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
           "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def _tex(s: object) -> str:
    return "".join(_ESCAPE.get(ch, ch) for ch in str(s))


def _pct(x: float | None, casas: int = 0) -> str:
    if x is None:
        return "--"
    return f"{x * 100:.{casas}f}".replace(".", ",") + r"\%"


def _tabela(rotulo: str, legenda: str, colunas: str, cabecalho: list[str], linhas: list[list[str]],
            nota: str) -> list[str]:
    return [r"\begin{table}[htbp]", r"\centering", r"\footnotesize", f"\\caption{{{legenda}}}", f"\\label{{{rotulo}}}",
            f"\\begin{{tabular}}{{{colunas}}}", r"\hline", " & ".join(cabecalho) + r" \\", r"\hline",
            *[" & ".join(lin) + r" \\" for lin in linhas], r"\hline", r"\end{tabular}",
            f"\\par\\smallskip\\footnotesize {nota}", r"\end{table}", ""]


def exportar_latex(cat: Catalogo, contribs: list[Contribuicao], destino: Path, minimo: int = 1) -> int:
    """Gera um arquivo .tex com macros e tabelas prontas para `\\input` no Overleaf.

    Macros: \\pesqTabelas (imprime as tabelas), \\pesqN (contribuições), \\pesqComResultado, \\pesqPeriodo, \\pesqVersoes. Tabelas (rótulos):
    tab:pesq-amostra, tab:pesq-maturidade, tab:pesq-riscos, tab:pesq-acoes. Grupos com n < N_PUBLICACAO levam "*";
    grupos com n < `minimo` aparecem como "--" (use --minimo 5 para a versão publicada)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    fonte = r"Fonte: elaborado pela autora a partir das contribuições anônimas registradas no CiberDecide."
    marca = f"* grupo com menos de {N_PUBLICACAO} contribuições."
    out = ["% Gerado por: riskpme-catalogo contribuicoes latex (não edite à mão; gere de novo quando chegarem respostas)",
           f"\\newcommand{{\\pesqN}}{{{len(contribs)}}}"]
    com = [c for c in contribs if c.resultado]
    meses = sorted({c.mes_ano for c in contribs})
    out += [f"\\newcommand{{\\pesqComResultado}}{{{len(com)}}}",
            f"\\newcommand{{\\pesqPeriodo}}{{{_tex(meses[0] + ' a ' + meses[-1]) if meses else '--'}}}",
            f"\\newcommand{{\\pesqVersoes}}{{{_tex(', '.join(sorted({c.versao_catalogo for c in contribs}))) or '--'}}}",
            ""]
    if not contribs:
        out.append(r"\newcommand{\pesqTabelas}{\textit{Nenhuma contribuição registrada até a data de geração "
                   r"destas tabelas.}}")
        destino.write_text("\n".join(out) + "\n", encoding="utf-8")
        return 0
    out.append(r"% \pesqTabelas imprime as tabelas onde for chamado (seção de análise das respostas).")
    out.append(r"\newcommand{\pesqTabelas}{%")

    g = agrupar(cat, contribs)
    funcoes = list(cat.funcoes)

    def nome(gr: Grupo) -> str:
        return _tex(gr.nome) + ("*" if gr.n < N_PUBLICACAO else "")

    # Amostra
    linhas = [[r"\textit{Porte}", ""]] + [[nome(gr), str(gr.n)] for _, gr in sorted(g["porte"].items())]
    linhas += [[r"\textit{Setor}", ""]] + [[nome(gr), str(gr.n)] for _, gr in sorted(g["setor"].items())]
    linhas += [[r"\textbf{Total}", rf"\textbf{{{len(contribs)}}}"]]
    out += _tabela("tab:pesq-amostra", "Perfil das empresas participantes", "lr", ["Grupo", "Contribuições"], linhas,
                   f"{marca} {fonte}")

    # Maturidade por função
    def linha_mat(gr: Grupo) -> list[str]:
        pode = gr.n >= minimo
        mats = [_pct(gr.maturidade(f)) if pode else "--" for f in funcoes]
        ns_total = sum(gr.nao_sei.values())
        tot = sum(gr.respondidas.values()) + ns_total
        return [nome(gr), str(gr.n), *mats, _pct(ns_total / tot) if pode and tot else "--"]

    linhas = [linha_mat(g["total"]["total"])]
    linhas += [linha_mat(gr) for _, gr in sorted(g["porte"].items())]
    linhas += [linha_mat(gr) for _, gr in sorted(g["setor"].items())]
    legenda_f = "; ".join(f"{f} = {_tex(cat.funcoes[f].nome)}" for f in funcoes)
    out += _tabela("tab:pesq-maturidade", "Maturidade média por função do NIST CSF 2.0",
                   r">{\raggedright\arraybackslash}p{3.1cm}" + "r" * (len(funcoes) + 2), ["Grupo", "n", *funcoes, r"``Não sei''"], linhas,
                   f"Maturidade = média de resposta/4 nas perguntas respondidas; ``Não sei'' fora da média. "
                   f"{legenda_f}. {marca} {fonte}")

    # Riscos por cenário
    if com and len(com) >= minimo:
        linhas = []
        for cen in cat.cenarios:
            rs = [c.resultado["cenarios"][cen.id] for c in com if cen.id in c.resultado.get("cenarios", {})]
            if not rs:
                continue
            frac = {k: sum(r["cor"] == k for r in rs) / len(rs) for k in ("vermelho", "amarelo", "verde")}
            linhas.append([_tex(cen.nome), _pct(frac["vermelho"]), _pct(frac["amarelo"]), _pct(frac["verde"]),
                           _pct(sum(bool(r["ruptura"]) for r in rs) / len(rs)),
                           _pct(sum(r["chance_horizonte"] for r in rs) / len(rs), 1),
                           _pct(sum(r["perda_esperada_pct_receita"] for r in rs) / len(rs), 2)])
        aviso = f" Resultado com menos de {N_PUBLICACAO} contribuições: leitura apenas ilustrativa." \
            if len(com) < N_PUBLICACAO else ""
        out += _tabela("tab:pesq-riscos", f"Classificação dos cenários nas {len(com)} contribuições com resultado",
                       r">{\raggedright\arraybackslash}p{4.6cm}rrrrrr", ["Cenário", "Vermelho", "Amarelo", "Verde", "Ruptura",
                                          r"\makecell{Chance\\5 anos}", r"\makecell{Perda/\\receita}"], linhas,
                       "Percentuais de contribuições em cada cor do mapa de calor; chance e perda esperada anual "
                       f"(em \\% da receita) são médias simples.{aviso} {fonte}")

        contagem: dict[str, int] = defaultdict(int)
        for c in com:
            for a in c.resultado.get("acoes", []):
                if a.get("bloco") == "comece":
                    contagem[a["controle"]] += 1
        if contagem:
            acao = {k.id: k.acao for k in cat.controles}
            linhas = [[_tex(ctrl), _tex(acao.get(ctrl, ctrl)), _pct(k / len(com))]
                      for ctrl, k in sorted(contagem.items(), key=lambda x: (-x[1], x[0]))[:10]]
            out += _tabela("tab:pesq-acoes", r"Ações mais indicadas no bloco ``Comece por aqui''", r"l>{\raggedright\arraybackslash}p{8.8cm}r",
                           ["Controle", "Ação", "Contribuições"], linhas,
                           f"Controle = item da ABNT NBR ISO/IEC 27002:2022. {fonte}")
    out.append("}")
    destino.write_text("\n".join(out) + "\n", encoding="utf-8")
    return len(contribs)
