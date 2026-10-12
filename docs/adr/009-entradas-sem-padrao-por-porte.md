# ADR-009 — Entradas do gestor sem valor padrão por porte

**Status:** Aceita (12/10/2026 — revisão S3 e S4)

## Contexto
A primeira versão do catálogo trazia valores "típicos" por porte, usados quando o gestor não soubesse responder:
faturamento e nº de pessoas com dados guardados (`portes.yaml`, bloco `padroes`), nº de usuários e volume de
backup (`custos.yaml`, `usuarios` e `dados_tb`). Esses valores não tinham fonte e variam muito entre empresas do
mesmo porte, o que contraria o princípio adotado na revisão: **dados antes de julgamento** (P1).

## Decisão
1. **Remover** `portes.padroes`, `custos.parametros.usuarios` e `custos.parametros.dados_tb`.
2. Tornar **obrigatórias** as perguntas de contexto (`audit/contexto.yaml`):
   - `faturamento_anual` (RF02) — sem valor padrão;
   - `registros_pessoais` (RF05) — por faixas; o número usado em cada faixa (50 / 500 / 5.000 / 50.000 / 200.000)
     é uma escolha de modelagem declarada (inventário J7);
   - `usuarios_ti` (nova) — "Quantas pessoas usam computador, celular ou e-mail da empresa para trabalhar?",
     inteiro ≥ 1. Fora das faixas de pessoas do porte gera aviso, não bloqueio.
3. Custo dos controles (`custos.py`): `custo_controle(controle, porte, usuarios)`. Licenças por usuário usam o
   número informado; backup = usuários × `gb_por_usuario` ÷ 1024. A memória de cálculo passa a mostrar cada custo
   como **fixo + por usuário** (o custo é linear no nº de usuários).
4. Validador: as checagens de sanidade usam **perfis de teste** derivados do próprio catálogo, sem inventar
   empresas típicas:
   - lognormal secundária: limites de faturamento de cada porte × todas as faixas de registros;
   - custo total vs. CIS IG1: nº de empregados do limite superior de cada Tier do CIS (10 / 10 / 100 / 999),
     mesma fonte do teto (cis2025cost).

## Consequências
- O gestor responde três números a mais; em troca, o resultado reflete a empresa dele e não uma média inventada.
- `gb_por_usuario = 100` continua sendo julgamento (mesma razão implícita na versão anterior); sem fonte pública
  recente encontrada — entra nas Limitações e na análise de sensibilidade (inventário J8).
- Os perfis de teste revelam que, em empresas pequenas com muitos registros, o p95 da perda secundária ultrapassa
  o teto (perda limitada ao faturamento) — insumo para a revisão de J3.
- Texto do TCC2: atualizar RF02/RF05 e o Módulo de Entrada (observação T10 da revisão).
