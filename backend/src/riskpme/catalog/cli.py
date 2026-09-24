"""Linha de comando do catálogo.

    riskpme-catalogo validar                    # integridade + cobertura dos 20 perfis
    riskpme-catalogo questionario 3 saude       # perguntas de um perfil
    riskpme-catalogo revisao docs/revisao.md    # exporta o banco de perguntas para revisão
    riskpme-catalogo custos docs/custos.md      # memória de cálculo do custo dos controles
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .loader import carregar_catalogo
from .models import NIVEIS_PORTE, Catalogo
from .validate import validar


def _cmd_validar(cat: Catalogo) -> int:
    r = validar(cat)
    setores = [s.id for s in cat.setores]

    print("Perguntas por perfil (porte × setor)")
    print(f"{'porte':<8}" + "".join(f"{s:>12}" for s in setores))
    for porte in NIVEIS_PORTE:
        print(f"{porte:<8}" + "".join(f"{r.perguntas_por_perfil[(porte, s)]:>12}" for s in setores))

    print("\nP(≥1 evento de perda/ano) com maturidade 0 / 0,5 / 1")
    for porte in NIVEIS_PORTE:
        linha = "".join(
            f"{'/'.join(f'{p:.0%}' for p in r.prob_evento[(porte, s)]):>16}" for s in setores
        )
        print(f"porte {porte}  {linha}")

    for a in r.avisos:
        print(f"AVISO: {a}")
    for e in r.erros:
        print(f"ERRO:  {e}")
    print(f"\n{'OK' if r.ok else 'FALHOU'} — {len(r.erros)} erro(s), {len(r.avisos)} aviso(s)")
    return 0 if r.ok else 1


def _cmd_questionario(cat: Catalogo, porte: int, setor: str) -> int:
    perguntas = cat.questionario(porte, setor)
    print(f"{cat.porte(porte).nome} · {cat.setor(setor).nome} — {len(perguntas)} perguntas\n")
    for p in perguntas:
        pesos = ", ".join(f"{c}:{w}" for c, w in p.cenarios.items())
        print(f"[{p.id}] ({p.subcategoria} · ISO 27002 {p.controle} · {pesos})")
        print(f"   {p.texto}")
    return 0


def _cmd_revisao(cat: Catalogo, destino: Path) -> int:
    setores = [s.id for s in cat.setores]
    linhas = [
        "# Revisão do banco de perguntas",
        "",
        "Gerado por `riskpme-catalogo revisao`. Edite `audit/perguntas.yaml`, não este arquivo.",
        "",
        "## Perguntas por perfil",
        "",
        "| Porte | " + " | ".join(setores) + " |",
        "|---|" + "---|" * len(setores),
    ]
    for porte in NIVEIS_PORTE:
        linhas.append(
            f"| {porte} | " + " | ".join(str(len(cat.questionario(porte, s))) for s in setores) + " |"
        )
    for cod, funcao in cat.funcoes.items():
        linhas += ["", f"## {funcao.nome} ({cod})", "", f"_{funcao.descricao}_", ""]
        for p in (q for q in cat.perguntas if q.funcao == cod):
            pesos = ", ".join(f"{c} {w}" for c, w in p.cenarios.items())
            setores_txt = ", ".join(p.setores) if p.setores else "todos"
            linhas += [
                f"### {p.id} — {p.texto}",
                "",
                f"**Ajuda:** {p.ajuda}",
                "",
                f"**Recomendação:** {p.recomendacao}",
                "",
                (f"`CSF {p.subcategoria}` · `ISO 27002 {p.controle}` · porte ≥ {p.porte_min}"
                 f" · setores: {setores_txt} · pesos: {pesos}"),
                "",
            ]
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"escrito {destino}")
    return 0


def _brl(v: float) -> str:
    return f"R$ {v:,.0f}".replace(",", ".")


def _cmd_custos(cat: Catalogo, destino: Path) -> int:
    m = cat.custos
    par = m.parametros
    L = [
        "# Memória de cálculo — custo anual dos controles",
        "",
        "Gerado por `riskpme-catalogo custos` a partir de `audit/custos.yaml`. Não edite este arquivo.",
        "",
        ("custo_anual = Σ licenças + (horas_implantação ÷ vida útil + horas_anuais + horas_por_usuário × usuários)"
         " × custo_hora"),
        "",
        "## Parâmetros",
        "",
        f"- Câmbio: US$ 1 = R$ {par.cambio_usd_brl:.4f} (PTAX venda, [@bcb2026ptax])",
        f"- Vida útil da implantação: {par.vida_util_anos:g} anos",
        f"- Usuários por porte: {', '.join(str(u) for u in par.usuarios)} ([@tcc1], Tabela 3.1)",
        f"- Dados em backup (TB): {', '.join(f'{d:g}' for d in par.dados_tb)} (estimativa)",
        "",
        "| Portes | Perfil | Salário P50 | Encargos | Custo/hora | Fonte |",
        "|---|---|---|---|---|---|",
    ]
    for mo in m.mao_de_obra:
        L.append(f"| {', '.join(map(str, mo.portes))} | {mo.perfil} | {_brl(mo.salario_mensal)} | "
                 f"{mo.encargos:.2%} | R$ {mo.custo_hora_calculado:.2f} | "
                 + " ".join(f"[@{f}]" for f in mo.fonte) + " |")
    L += ["", "## Preços de licença", "", "| Item | Preço | Unidade | Fonte |", "|---|---|---|---|"]
    for p in m.precos:
        L.append(f"| {p.descricao} | {p.moeda} {p.valor:,.2f} | {p.unidade} | [@{p.fonte}] |")
    L += ["", "## Custo anual por controle (R$)", "",
          "| ISO 27002 | Controle | MEI | ME | EPP | Média |", "|---|---|---|---|---|---|"]
    totais = [0.0] * 4
    for c in cat.controles:
        vals = [cat.custo_controle(c.id, p).total for p in NIVEIS_PORTE]
        totais = [a + b for a, b in zip(totais, vals)]
        L.append(f"| {c.id} | {c.nome} | " + " | ".join(_brl(v) for v in vals) + " |")
    L.append("| | **Total (todos os controles)** | " + " | ".join(f"**{_brl(v)}**" for v in totais) + " |")
    cis = [v * par.cambio_usd_brl for v in m.referencia_cis_ig1_usd]
    L.append("| | Teto CIS IG1 – ferramentas [@cis2025cost] | " + " | ".join(_brl(v) for v in cis) + " |")
    L += ["", "## Detalhamento", ""]
    for c in cat.controles:
        comp = m.controles[c.id]
        L.append(f"**{c.id} {c.nome}** — horas de implantação {list(comp.horas_implantacao)}, "
                 f"horas/ano {list(comp.horas_anuais)}"
                 + (f", {comp.horas_por_usuario_ano:g} h por usuário/ano" if comp.horas_por_usuario_ano else ""))
        for lic in comp.licencas:
            L.append(f"- licença: {m.preco(lic.preco).descricao}, portes {lic.portes}")
        L.append("")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"escrito {destino}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="riskpme-catalogo", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", help="pasta do catálogo (padrão: audit/ do repositório)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validar")
    q = sub.add_parser("questionario")
    q.add_argument("porte", type=int, choices=NIVEIS_PORTE)
    q.add_argument("setor")
    rv = sub.add_parser("revisao")
    rv.add_argument("destino", type=Path)
    cu = sub.add_parser("custos")
    cu.add_argument("destino", type=Path)
    args = ap.parse_args(argv)

    try:
        cat = carregar_catalogo(args.dir)
    except (ValueError, FileNotFoundError) as e:
        print(f"ERRO ao carregar o catálogo:\n{e}", file=sys.stderr)
        return 1

    if args.cmd == "validar":
        return _cmd_validar(cat)
    if args.cmd == "questionario":
        return _cmd_questionario(cat, args.porte, args.setor)
    if args.cmd == "custos":
        return _cmd_custos(cat, args.destino)
    return _cmd_revisao(cat, args.destino)


if __name__ == "__main__":
    sys.exit(main())
