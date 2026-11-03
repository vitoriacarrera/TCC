"""Estudos para a monografia: perfis de referência, incerteza do Monte Carlo e sensibilidade (ADR-011, princípio P1).

`riskpme-catalogo estudos PASTA` grava em PASTA:
    perfis.csv, incerteza.csv, sensibilidade.csv     dados brutos, para conferência
    estudos.tex                                      macros \\estTabelaPerfis, \\estTabelaCores,
                                                     \\estTabelaIncerteza e \\estTabelaSensibilidade (\\input no Overleaf)

Perfis de referência: 5 setores × 4 portes, com todas as respostas em um mesmo nível (1, 2 ou 3). Respostas
uniformes não representam uma empresa real; servem para isolar o efeito do setor, do porte e da maturidade.
Sensibilidade "um fator por vez": cada parâmetro baseado em julgamento (ou com valor alternativo de fonte) é trocado
pelo alternativo, os demais ficam no valor de base, e os 20 perfis de maturidade 2 são recalculados.
Todas as simulações usam semente fixa, de modo que os números podem ser reproduzidos.
"""

from __future__ import annotations

import copy
import csv
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, stdev

import yaml

from .analise import _tex
from .catalog.loader import ARQUIVOS, carregar_catalogo, diretorio_padrao
from .catalog.models import Catalogo
from .engine.perfil import Perfil
from .engine.plano import plano_de_acao
from .engine.simulacao import simular

SEMENTE = 0
NIVEIS = (1, 2, 3)

# Porte: (receita bruta anual em R$, usuários, faixa de registros). Receita dentro de cada faixa da LC 123/BNDES.
PORTES_REF = {1: (60_000, 1, "ate100"), 2: (250_000, 3, "ate1k"), 3: (1_500_000, 10, "ate10k"),
              4: (20_000_000, 60, "ate100k")}
ATIVO = {"saude": "clientes", "varejo": "vendas", "servicos": "clientes", "tecnologia": "projetos",
         "industria": "producao"}


def perfil_ref(setor: str, porte: int) -> Perfil:
    rob, usuarios, registros = PORTES_REF[porte]
    return Perfil(setor=setor, receita_operacional_bruta=rob, usuarios_ti=usuarios, registros_pessoais=registros,
                  tipo_dado="sensivel" if setor == "saude" else "cadastral", ativo_critico=ATIVO[setor],
                  apetite="nao_sei", tolerancia="nao_sei")


def respostas_uniformes(cat: Catalogo, perfil: Perfil, nivel: int) -> dict[str, int]:
    porte = cat.classificar_porte(perfil.receita_operacional_bruta)
    return {q.id: nivel for q in cat.questionario(porte, perfil.setor, perfil.usuarios_ti)}


@dataclass
class Rodada:
    perda_esperada: float
    receita: float
    chance_horizonte: float
    cores: dict[str, str]
    rupturas: set[str]
    acoes: list[str]          # ordem do plano
    comece: list[str]         # ações dentro do limite de investimento


def rodar(cat: Catalogo, perfil: Perfil, respostas: dict, semente: int = SEMENTE, iteracoes: int | None = None) -> Rodada:
    r = simular(cat, perfil, respostas, iteracoes=iteracoes, semente=semente)
    rupt = [c.id for c in r.cenarios if c.ruptura]
    p = plano_de_acao(cat, perfil, respostas, rupt, semente=semente, iteracoes=iteracoes)
    return Rodada(r.perda_esperada_total, perfil.receita_operacional_bruta, r.chance_algum_prejuizo_horizonte,
                  {c.id: c.cor for c in r.cenarios}, set(rupt), [a.controle for a in p.acoes],
                  [a.controle for a in p.acoes if not a.acima_do_limite])


# ---------------------------------------------------------------------------------------------------------------------
# Variações do catálogo
# ---------------------------------------------------------------------------------------------------------------------

def _multiplicar_horas(d: object, fator: float) -> object:
    if isinstance(d, dict):
        return {k: (_escala(v, fator) if str(k).startswith("horas") else _multiplicar_horas(v, fator))
                for k, v in d.items()}
    if isinstance(d, list):
        return [_multiplicar_horas(x, fator) for x in d]
    return d


def _escala(v: object, fator: float) -> object:
    if isinstance(v, list):
        return [x * fator for x in v]
    return v * fator if isinstance(v, (int, float)) else v


def _reducao_alternativa(dados: dict) -> None:
    for c in dados["cenarios"]["cenarios"]:
        rm = c.get("reducao_magnitude")
        if rm and rm.get("sensibilidade") is not None:
            rm["maxima"] = rm["sensibilidade"]


def _faixa_v(vmin: float, vmax: float) -> Callable[[dict], None]:
    def f(dados: dict) -> None:
        dados["cenarios"]["parametros_modelo"].update(vulnerabilidade_min=vmin, vulnerabilidade_max=vmax)
    return f


def _tef(fator: float, ids: tuple[str, ...]) -> Callable[[dict], None]:
    def f(dados: dict) -> None:
        for c in dados["cenarios"]["cenarios"]:
            if c["id"] in ids:
                c["tef_base"] = c["tef_base"] * fator
    return f


def _porte_alternativo(dados: dict) -> None:
    alt = {1: 0.68, 2: 0.68, 3: 1.00, 4: 1.92}      # csbs2026, métrica "vítimas de crime cibernético" (revisão S1)
    for p in dados["portes"]["portes"]:
        p["multiplicador_tef"] = alt[p["nivel"]]


def _horas(fator: float) -> Callable[[dict], None]:
    def f(dados: dict) -> None:
        dados["custos"]["controles"] = _multiplicar_horas(dados["custos"]["controles"], fator)
    return f


def _gb(valor: float) -> Callable[[dict], None]:
    def f(dados: dict) -> None:
        dados["custos"]["parametros"]["gb_por_usuario"] = valor
    return f


def _nao_sei(valor: int) -> Callable[[dict], None]:
    def f(dados: dict) -> None:
        dados["cenarios"]["parametros_modelo"]["resposta_nao_sei"] = valor
    return f


JULGADOS = ("VAZ", "IND", "TER", "IA")      # repartição 0,7 : 0,5 : 0,4 : 0,3 do restante (julgamento declarado)

VARIACOES: list[tuple[str, str, Callable[[dict], None]]] = [
    ("reducao_alt", "Redução máxima do prejuízo pelos valores alternativos (Tabela~\\ref{tab:reducao})",
     _reducao_alternativa),
    ("v_otimista", "Faixa de vulnerabilidade 0,01 a 0,25 (base 0,02 a 0,35)", _faixa_v(0.01, 0.25)),
    ("v_pessimista", "Faixa de vulnerabilidade 0,05 a 0,50", _faixa_v(0.05, 0.50)),
    ("tef_julg_menos", "Frequência base de VAZ, IND, TER e IA $-50\\%$", _tef(0.5, JULGADOS)),
    ("tef_julg_mais", "Frequência base de VAZ, IND, TER e IA $+50\\%$", _tef(1.5, JULGADOS)),
    ("porte_alt", "Multiplicadores de porte pela métrica ``vítimas de crime'' (0,68; 0,68; 1,00; 1,92)",
     _porte_alternativo),
    ("horas_menos", "Horas de esforço dos controles $-50\\%$", _horas(0.5)),
    ("horas_mais", "Horas de esforço dos controles $+50\\%$", _horas(1.5)),
    ("gb_50", "Backup: 50 GB por usuário (base 100 GB)", _gb(50)),
    ("gb_200", "Backup: 200 GB por usuário", _gb(200)),
]


def catalogo_variado(alterar: Callable[[dict], None], base: Path | None = None) -> Catalogo:
    """Cópia temporária do catálogo com `alterar` aplicada aos YAML já lidos."""
    base = base or diretorio_padrao()
    with tempfile.TemporaryDirectory() as tmp:
        dados = {}
        for nome in ARQUIVOS:
            with (base / f"{nome}.yaml").open(encoding="utf-8") as f:
                dados[nome] = yaml.safe_load(f) or {}
        dados = copy.deepcopy(dados)
        alterar(dados)
        for nome, conteudo in dados.items():
            with (Path(tmp) / f"{nome}.yaml").open("w", encoding="utf-8") as f:
                yaml.safe_dump(conteudo, f, allow_unicode=True, sort_keys=False)
        return carregar_catalogo(tmp)


# ---------------------------------------------------------------------------------------------------------------------
# Estudos
# ---------------------------------------------------------------------------------------------------------------------

def perfis_referencia(cat: Catalogo, nivel: int) -> list[tuple[str, int, Perfil, dict]]:
    out = []
    for s in cat.setores:
        for porte in PORTES_REF:
            p = perfil_ref(s.id, porte)
            out.append((s.id, porte, p, respostas_uniformes(cat, p, nivel)))
    return out


def estudo_perfis(cat: Catalogo) -> list[dict]:
    linhas = []
    for nivel in NIVEIS:
        for setor, porte, p, resp in perfis_referencia(cat, nivel):
            r = rodar(cat, p, resp)
            linhas.append({"nivel": nivel, "setor": setor, "porte": porte, "perda_pct_receita": r.perda_esperada / r.receita,
                           "chance_5a": r.chance_horizonte,
                           "vermelhos": sum(c == "vermelho" for c in r.cores.values()),
                           "amarelos": sum(c == "amarelo" for c in r.cores.values()),
                           "rupturas": len(r.rupturas), "acoes_comece": len(r.comece),
                           "primeira_acao": r.acoes[0] if r.acoes else "", "cores": r.cores})
    return linhas


def estudo_incerteza(cat: Catalogo, perfil: Perfil, respostas: dict, sementes: int = 20) -> dict:
    """Variação entre sementes (10.000 anos cada) e erro padrão dentro de uma rodada."""
    rodadas = [rodar(cat, perfil, respostas, semente=s) for s in range(sementes)]
    perdas = [r.perda_esperada for r in rodadas]
    base = rodadas[0]
    return {
        "sementes": sementes, "iteracoes": cat.parametros_modelo.iteracoes,
        "perda_media": mean(perdas), "perda_dp": stdev(perdas),
        "perda_min": min(perdas), "perda_max": max(perdas),
        "cores_iguais": mean(all(r.cores[c] == base.cores[c] for c in base.cores) for r in rodadas),
        "rupturas_iguais": mean(r.rupturas == base.rupturas for r in rodadas),
        "primeira_igual": mean(r.acoes[:1] == base.acoes[:1] for r in rodadas),
        "top5_comum": mean(len(set(r.acoes[:5]) & set(base.acoes[:5])) / 5 for r in rodadas),
        "chance_media": mean(r.chance_horizonte for r in rodadas),
    }


def _comparar(base: list[Rodada], alt: list[Rodada]) -> dict:
    celulas = sum(len(b.cores) for b in base)
    return {
        "delta_perda_medio": mean((a.perda_esperada - b.perda_esperada) / b.perda_esperada
                                  for a, b in zip(alt, base, strict=True) if b.perda_esperada),
        "cores_mudaram": sum(a.cores[c] != b.cores[c] for a, b in zip(alt, base, strict=True) for c in b.cores),
        "celulas": celulas,
        "rupturas_mudaram": sum(len(a.rupturas ^ b.rupturas) for a, b in zip(alt, base, strict=True)),
        "primeira_igual": mean(a.acoes[:1] == b.acoes[:1] for a, b in zip(alt, base, strict=True)),
        "top5_comum": mean(len(set(a.acoes[:5]) & set(b.acoes[:5])) / 5 for a, b in zip(alt, base, strict=True)),
    }


def estudo_sensibilidade(cat: Catalogo, nivel: int = 2,
                         extras: list[tuple[str, Perfil, dict]] | None = None) -> list[dict]:
    perfis = [(f"{s}|{p}", pf, r) for s, p, pf, r in perfis_referencia(cat, nivel)] + (extras or [])
    base = [rodar(cat, pf, r) for _, pf, r in perfis]
    linhas = []
    variacoes = VARIACOES + [("nao_sei_0", "``Não sei'' conta como nível 0 (base: nível 1)", _nao_sei(0)),
                             ("nao_sei_2", "``Não sei'' conta como nível 2", _nao_sei(2))]
    for vid, descricao, alterar in variacoes:
        alt_cat = catalogo_variado(alterar)
        if vid.startswith("nao_sei"):
            # o efeito do "Não sei" só aparece com respostas "Não sei": metade das perguntas vira None
            def com_nao_sei(r: dict) -> dict:
                return {k: (None if i % 2 else v) for i, (k, v) in enumerate(sorted(r.items()))}
            b = [rodar(cat, pf, com_nao_sei(r)) for _, pf, r in perfis]
            a = [rodar(alt_cat, pf, com_nao_sei(r)) for _, pf, r in perfis]
        else:
            b = base
            a = [rodar(alt_cat, pf, r) for _, pf, r in perfis]
        linhas.append({"variacao": vid, "descricao": descricao, **_comparar(b, a)})
    return linhas


# ---------------------------------------------------------------------------------------------------------------------
# Saída
# ---------------------------------------------------------------------------------------------------------------------

def _pct(x: float, casas: int = 0) -> str:
    return f"{x * 100:.{casas}f}".replace(".", ",") + r"\%"


def _num(x: float, casas: int = 0) -> str:
    s = f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def _csv(caminho: Path, linhas: list[dict]) -> None:
    with caminho.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]), delimiter=";")
        w.writeheader()
        w.writerows(linhas)


def _tabela(rotulo: str, legenda: str, colunas: str, cab: list[str], linhas: list[list[str]], nota: str) -> list[str]:
    return [r"\begin{table}[htbp]", r"\centering", r"\footnotesize", f"\\caption{{{legenda}}}", f"\\label{{{rotulo}}}",
            f"\\begin{{tabular}}{{{colunas}}}", r"\hline", " & ".join(cab) + r" \\", r"\hline",
            *[" & ".join(lin) + r" \\" for lin in linhas], r"\hline", r"\end{tabular}",
            f"\\par\\smallskip\\footnotesize {nota}", r"\end{table}", ""]


def gerar(destino: Path, cat: Catalogo | None = None, clinica: tuple[Perfil, dict] | None = None,
          sementes: int = 20) -> dict:
    """Roda os três estudos e grava CSVs e estudos.tex em `destino`. Devolve os números principais."""
    cat = cat or carregar_catalogo()
    destino.mkdir(parents=True, exist_ok=True)
    fonte = "Fonte: elaborado pela autora com o motor do CiberDecide (semente fixa; reprodutível com " \
            r"\texttt{riskpme-catalogo estudos})."
    nome_setor = {s.id: s.nome for s in cat.setores}
    sigla_porte = {1: "MEI", 2: "ME", 3: "EPP", 4: "Média"}

    perfis = estudo_perfis(cat)
    _csv(destino / "perfis.csv", [{k: v for k, v in lin.items() if k != "cores"} for lin in perfis])
    out = ["% Gerado por: riskpme-catalogo estudos (não edite à mão)", ""]

    # Tabela de perfis: perda esperada (% da receita) por setor × porte, para cada nível de maturidade
    linhas = []
    for s in cat.setores:
        cel = []
        for nivel in NIVEIS:
            for porte in PORTES_REF:
                lin = next(x for x in perfis if x["setor"] == s.id and x["porte"] == porte and x["nivel"] == nivel)
                cel.append(_pct(lin["perda_pct_receita"], 2))
        linhas.append([_tex(nome_setor[s.id]), *cel])
    cab = ["Setor", *[f"{sigla_porte[p]}" for _ in NIVEIS for p in PORTES_REF]]
    out += [r"\newcommand{\estTabelaPerfis}{%", r"\begin{table}[htbp]", r"\centering", r"\footnotesize",
            (r"\caption{Perda esperada anual, em percentual da receita bruta, dos 20 perfis de referência com "
            r"todas as respostas no nível 1, 2 ou 3}"), r"\label{tab:est-perfis}",
            r"\setlength{\tabcolsep}{2.5pt}",
            r"\begin{tabular}{>{\raggedright\arraybackslash}p{2.3cm}" + "r" * (len(NIVEIS) * len(PORTES_REF)) + "}",
            r"\hline",
            " & " + " & ".join(f"\\multicolumn{{{len(PORTES_REF)}}}{{c}}{{Nível {n}}}" for n in NIVEIS) + r" \\",
            " & ".join(cab) + r" \\", r"\hline", *[" & ".join(lin) + r" \\" for lin in linhas], r"\hline",
            r"\end{tabular}",
            r"\par\smallskip\footnotesize Receitas de referência: MEI R\$~60 mil, ME R\$~250 mil, EPP R\$~1,5 milhão, "
            r"média R\$~20 milhões; apetite e tolerância ``Não sei dizer''. " + fonte, r"\end{table}", "}", ""]

    # Tabela de cores no nível 2
    contagem = {cen.id: {"vermelho": 0, "amarelo": 0, "verde": 0, "ruptura": 0} for cen in cat.cenarios}
    n2 = [x for x in perfis if x["nivel"] == 2]
    for lin in n2:
        for cid, cor in lin["cores"].items():
            contagem[cid][cor] += 1
    for _setor, _porte, p, resp in perfis_referencia(cat, 2):
        r = simular(cat, p, resp, semente=SEMENTE)
        for c in r.cenarios:
            contagem[c.id]["ruptura"] += c.ruptura
    linhas = [[_tex(cen.nome), *(str(contagem[cen.id][k]) for k in ("vermelho", "amarelo", "verde", "ruptura"))]
              for cen in cat.cenarios]
    out += [r"\newcommand{\estTabelaCores}{%"] + _tabela("tab:est-cores", "Classificação dos cenários no mapa de calor nos 20 perfis de referência com "
                   "maturidade de nível 2", r">{\raggedright\arraybackslash}p{6.2cm}rrrr",
                   ["Cenário", "Vermelho", "Amarelo", "Verde", "Ruptura"], linhas,
                   "Número de perfis (de 20) em cada cor; a coluna Ruptura conta os perfis com o selo. " + fonte) + ["}", ""]

    # Incerteza do Monte Carlo
    resumo: dict = {"perfis": perfis}
    if clinica:
        inc = estudo_incerteza(cat, *clinica, sementes=sementes)
        _csv(destino / "incerteza.csv", [inc])
        resumo["incerteza"] = inc
        cv = inc["perda_dp"] / inc["perda_media"]
        linhas = [["Perda esperada anual (R\\$)", f"{_num(inc['perda_media'])} $\\pm$ {_num(inc['perda_dp'])}",
                   f"{_num(inc['perda_min'])} a {_num(inc['perda_max'])}"],
                  ["Coeficiente de variação da perda esperada", _pct(cv, 1), "--"],
                  ["Chance de algum prejuízo em 5 anos", _pct(inc["chance_media"], 1), "--"],
                  ["Sementes com as mesmas 6 cores do mapa", _pct(inc["cores_iguais"]), "--"],
                  ["Sementes com os mesmos selos de ruptura", _pct(inc["rupturas_iguais"]), "--"],
                  ["Sementes com a mesma primeira ação", _pct(inc["primeira_igual"]), "--"],
                  ["Ações em comum entre as 5 primeiras", _pct(inc["top5_comum"]), "--"]]
        out += [r"\newcommand{\estTabelaIncerteza}{%"] + _tabela("tab:est-incerteza", f"Variação dos resultados do caso da clínica entre {inc['sementes']} "
                       f"sementes de {_num(inc['iteracoes'])} anos simulados cada",
                       r">{\raggedright\arraybackslash}p{7.2cm}rr", ["Indicador", "Média $\\pm$ desvio padrão",
                                                                     "Mínimo a máximo"], linhas,
                       "Percentuais em relação à semente 0, usada no restante do texto. " + fonte) + ["}", ""]

    # Sensibilidade
    extras = [("clinica", *clinica)] if clinica else None
    sens = estudo_sensibilidade(cat, extras=extras)
    _csv(destino / "sensibilidade.csv", sens)
    resumo["sensibilidade"] = sens
    linhas = [[s["descricao"], ("+" if s["delta_perda_medio"] >= 0 else "") + _pct(s["delta_perda_medio"], 1),
               f"{s['cores_mudaram']} de {s['celulas']}", str(s["rupturas_mudaram"]), _pct(s["primeira_igual"]),
               _pct(s["top5_comum"])] for s in sens]
    n_perfis = 20 + (1 if clinica else 0)
    out += [r"\newcommand{\estTabelaSensibilidade}{%"] + _tabela("tab:est-sensibilidade", f"Análise de sensibilidade um fator por vez nos {n_perfis} perfis "
                   "(20 de referência com maturidade de nível 2" + (" e o caso da clínica)" if clinica else ")"),
                   r">{\raggedright\arraybackslash}p{5.6cm}rrrrr",
                   [r"Variação", r"\makecell{$\Delta$ perda\\esperada}", r"\makecell{Cores que\\mudaram}",
                    r"\makecell{Selos de\\ruptura}", r"\makecell{Mesma 1ª\\ação}", r"\makecell{Top 5\\em comum}"],
                   linhas,
                   r"$\Delta$ perda esperada = variação média em relação à base. Selos de ruptura = selos que "
                   r"apareceram ou sumiram. Nas duas linhas do ``Não sei'', metade das perguntas foi respondida "
                   r"``Não sei'' tanto na base quanto na variação. " + fonte) + ["}", ""]
    (destino / "estudos.tex").write_text("\n".join(out) + "\n", encoding="utf-8")
    return resumo


def carregar_clinica(arquivo: Path) -> tuple[Perfil, dict]:
    import json
    d = json.loads(arquivo.read_text(encoding="utf-8"))
    return Perfil(**d["perfil"]), d["respostas"]

