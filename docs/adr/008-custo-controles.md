# ADR-008 — Custo dos controles com memória de cálculo

**Status:** Aceita (24/09/2026)

## Contexto
O ROI do plano de ação (RF11) depende do custo anual de cada controle. Na primeira versão esses custos eram
valores fixos estimados, sem fonte — ponto frágil perante a banca.

## Decisão
O custo passa a ser **calculado** (`audit/custos.yaml`, `riskpme.catalog.custos`), seguindo a composição de custo da
solução de ENISA (2012) — licenças + implantação + operação:

custo_anual = Σ licenças + (horas_implantação ÷ vida útil + horas_anuais + horas_por_usuário × usuários) × custo_hora

| Componente | Fonte |
|---|---|
| Preço de licenças | Listas públicas: Microsoft, Bitwarden, Backblaze, Cloudflare |
| Câmbio | PTAX do Banco Central |
| Custo da hora | Guia Salarial Robert Half 2026 (P50) + encargos (Simples: 39,37%; Presumido/Real: 68,18%) ÷ 220 h |
| Horas de esforço, volume de dados | **Estimativa declarada** — limitação a registrar no TCC2 |
| Razoabilidade do total | CIS (2025): custo de ferramentas do IG1 por porte; teste automatizado garante que o total fica dentro da faixa |

Priorização econômica no motor (Etapa 2): ROSI (ENISA, 2012) por controle e o limite de Gordon & Loeb (2002) —
investimento ótimo ≤ 1/e ≈ 36,8% da perda esperada — como alerta de superinvestimento.

## Consequências
- `riskpme-catalogo custos docs/memoria-custos.md` gera a memória de cálculo citável no apêndice.
- Referências em `docs/referencias.bib` (chaves iguais às de `audit/fontes.yaml`).
- Preços em dólar e câmbio devem ser atualizados na data de fechamento do texto.
