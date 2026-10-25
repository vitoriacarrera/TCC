"""Linha de comando do catálogo.

    riskpme-catalogo validar                    # integridade + cobertura dos 20 perfis
    riskpme-catalogo questionario 3 saude       # perguntas de um perfil
    riskpme-catalogo revisao docs/revisao.md    # exporta o banco de perguntas para revisão
    riskpme-catalogo custos docs/custos.md      # memória de cálculo do custo dos controles
    riskpme-catalogo simular perfil.json        # Monte Carlo + matriz 3 × 3 + plano de ação de um perfil
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .custos import custo_fixo_e_por_usuario
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

    if r.pendentes or r.julgamento:
        print("\nParâmetros sem dado (vão para as Limitações do TCC)")
        for x in r.pendentes:
            print(f"  PENDENTE: {x}")
        for x in r.julgamento:
            print(f"  JULGAMENTO: {x}")

    for a in r.avisos:
        print(f"AVISO: {a}")
    for e in r.erros:
        print(f"ERRO:  {e}")
    print(f"\n{'OK' if r.ok else 'FALHOU'} — {len(r.erros)} erro(s), {len(r.avisos)} aviso(s)")
    return 0 if r.ok else 1


def _cmd_questionario(cat: Catalogo, porte: int, setor: str, usuarios: int | None = None) -> int:
    perguntas = cat.questionario(porte, setor, usuarios)
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
            for v in p.variantes:
                cond = []
                if v.quando.portes:
                    cond.append("portes " + ", ".join(map(str, v.quando.portes)))
                if v.quando.usuarios_max is not None:
                    cond.append(f"até {v.quando.usuarios_max} usuário(s)")
                linhas.append(f"**Variante ({'; '.join(cond)}):**")
                linhas.append("")
                for campo in ("texto", "ajuda", "recomendacao"):
                    if getattr(v, campo):
                        linhas.append(f"- {campo}: {getattr(v, campo)}")
                if v.cenarios:
                    linhas.append("- pesos: " + ", ".join(f"{c} {w}" for c, w in v.cenarios.items()))
                linhas.append("")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"escrito {destino}")
    return 0


def _brl(v: float) -> str:
    return f"R$ {v:,.0f}".replace(",", ".")


def _fixo_mais_usuario(fixo: float, por_usuario: float) -> str:
    if por_usuario < 0.5:
        return _brl(fixo)
    return f"{_brl(fixo)} + {_brl(por_usuario)}/usuário"


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
        ("- Usuários: informados pelo gestor (pergunta `usuarios_ti`); por isso cada custo é apresentado como"
         " **parte fixa + parte por usuário**"),
        f"- Volume de backup: usuários × {par.gb_por_usuario:g} GB ÷ 1024 (estimativa declarada)",
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
    L += ["", "## Custo anual por controle (R$): fixo + por usuário", "",
          "custo_anual = fixo + por_usuário × usuários", "",
          "| ISO 27002 | Controle | MEI | ME | EPP | Média |", "|---|---|---|---|---|---|"]
    fixos = [0.0] * 4
    por_u = [0.0] * 4
    for c in cat.controles:
        partes = [custo_fixo_e_por_usuario(m, c.id, p) for p in NIVEIS_PORTE]
        fixos = [a + f for a, (f, _) in zip(fixos, partes)]
        por_u = [a + u for a, (_, u) in zip(por_u, partes)]
        L.append(f"| {c.id} | {c.nome} | " + " | ".join(_fixo_mais_usuario(f, u) for f, u in partes) + " |")
    L.append("| | **Total (todos os controles)** | "
             + " | ".join(f"**{_fixo_mais_usuario(f, u)}**" for f, u in zip(fixos, por_u)) + " |")
    emp = m.referencia_cis_ig1_empregados
    tot_ref = [f + u * e for f, u, e in zip(fixos, por_u, emp)]
    L.append("| | Total com o nº de empregados do limite do Tier CIS | "
             + " | ".join(f"{_brl(t)} ({e} usuários)" for t, e in zip(tot_ref, emp)) + " |")
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


def _cmd_simular(cat: Catalogo, arquivo: Path, semente: int | None) -> int:
    import json

    from ..engine.perfil import Perfil
    from ..engine.plano import plano_de_acao
    from ..engine.simulacao import simular

    dados = json.loads(arquivo.read_text(encoding="utf-8"))
    perfil = Perfil(**dados["perfil"])
    respostas = dados.get("respostas", {})
    r = simular(cat, perfil, respostas, semente=semente)
    print(f"{cat.porte(r.porte).nome} · {cat.setor(r.setor).nome} · {r.iteracoes} anos simulados")
    print(f"Apetite R$ {r.apetite_rs:,.0f} · tolerância R$ {r.tolerancia_rs:,.0f} · custo da hora parada "
          f"R$ {r.custo_hora_parada:,.0f}{' (estimado)' if r.custo_hora_estimado else ''}")
    h = r.horizonte_anos
    print(f"Chance de algum prejuízo: {r.chance_algum_prejuizo:.0%} no ano, {r.chance_algum_prejuizo_horizonte:.0%} "
          f"em {h} anos · perda esperada R$ {r.perda_esperada_total:,.0f}/ano · P90 do ano R$ "
          f"{r.percentis_total[90]:,.0f}\n")
    print(f"{'cenário':<8}{'prev.':>6}{'resp.':>6}{'red.prej.':>10}{'chance/ano':>11}{f'em {h} anos':>11}"
          f"{'perda esp.':>12}{'P90 se ocorre':>15}  célula (impacto, probabilidade)")
    for c in r.cenarios:
        selo = " · RISCO DE RUPTURA" if c.ruptura else ""
        red = 1 - min(c.fator_primaria, c.fator_secundaria)
        print(f"{c.id:<8}{c.maturidade:>6.0%}{c.maturidade_resposta:>6.0%}{red:>10.0%}{c.chance_ano:>11.1%}"
              f"{c.chance_horizonte:>11.1%}{c.perda_esperada:>12,.0f}{c.p90_quando_ocorre:>15,.0f}  {c.cor} "
              f"({c.nivel_impacto},{c.nivel_probabilidade}){selo}")
    print("prev. = maturidade de prevenção (chance); resp. = maturidade de resposta (prejuízo); red.prej. = redução "
          "do prejuízo pela preparação")
    if r.nao_sei:
        print(f"\nRespostas \"Não sei\": {', '.join(r.nao_sei)}")
    plano = plano_de_acao(cat, perfil, respostas, [c.id for c in r.cenarios if c.ruptura])
    print(f"\nPlano de ação · limite de investimento (Gordon-Loeb) R$ {plano.limite_investimento:,.0f}/ano · "
          f"prejuízo num período ruim de {plano.horizonte_anos} anos (P90) R$ {plano.perda_periodo_ruim_atual:,.0f}")
    for a in plano.acoes:
        rosi = "sem custo" if a.rosi is None else f"ROSI {a.rosi:+.0%}"
        lim = " · acima do limite" if a.acima_do_limite else ""
        rup = (" · protege contra ruptura (" + ", ".join(f"{c}: impacto R$ {v:,.0f}" for c, v in a.impacto_ruptura.items())
               + ")") if a.protege_ruptura else ""
        print(f"{a.prioridade:>3}. {a.controle} {a.controle_nome}: reduz R$ {a.reducao_perda_anual:,.0f}/ano "
              f"(período ruim: −R$ {a.reducao_periodo_ruim:,.0f}), custa R$ {a.custo_anual:,.0f}/ano, "
              f"{rosi}{lim}{rup}")
    for x in plano.ruptura:
        prep = ", ".join(x["preparacao"]) or "nenhuma ação de preparação pendente"
        sai = "sai da faixa acima da tolerância" if x["sai_da_ruptura"] else "continua acima da tolerância"
        print(f"\nRisco de ruptura {x['cenario']}: impacto R$ {x['impacto_atual']:,.0f} → R$ "
              f"{x['impacto_com_preparacao']:,.0f} com a preparação ({prep}); tolerância R$ {x['tolerancia']:,.0f}: "
              f"{sai}. Transferência: seguro (cotação com corretor)")
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
    q.add_argument("--usuarios", type=int, default=None, help="nº de usuários (ativa variantes, ex.: 1)")
    rv = sub.add_parser("revisao")
    rv.add_argument("destino", type=Path)
    si = sub.add_parser("simular")
    si.add_argument("arquivo", type=Path)
    si.add_argument("--semente", type=int, default=None)
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
        return _cmd_questionario(cat, args.porte, args.setor, args.usuarios)
    if args.cmd == "custos":
        return _cmd_custos(cat, args.destino)
    if args.cmd == "simular":
        return _cmd_simular(cat, args.arquivo, args.semente)
    return _cmd_revisao(cat, args.destino)


if __name__ == "__main__":
    sys.exit(main())
