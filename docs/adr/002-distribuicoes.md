# ADR-002 — Distribuições do modelo estocástico

**Status:** Aceita (24/09/2026) — decisão da autora: usar Beta-PERT **e** Lognormal na Simulação de Monte Carlo.

## Contexto
O TCC1 §3.6 prevê Beta-PERT para a incerteza financeira (item 2 e RF08) e diz que, no Monte Carlo, "o valor da
perda" é sorteado de uma Lognormal (item 3). Usar as duas para a mesma grandeza seria contraditório. A saída é
dar a cada distribuição um papel distinto, seguindo a própria ontologia FAIR, que divide a Magnitude da Perda em
**Perda Primária** e **Perda Secundária** (Freund & Jones, 2014; Open FAIR / The Open Group O-RT).

## Decisão

| Grandeza | Distribuição | Por quê |
|---|---|---|
| Nº de eventos de perda no ano | **Poisson(LEF)**, LEF = TEF × Vulnerabilidade | Eventos raros e independentes; P(≥1) = 1 − e^(−LEF) |
| Perda primária por evento (parada, recuperação, valor desviado) | **Beta-PERT(mín, mais provável, máx; λ = 4)** | Custos diretos são limitados e o gestor consegue estimar três pontos (RF08) |
| Ocorrência de perda secundária | **Bernoulli(p)** — SLEF do FAIR | Nem todo incidente gera reação de terceiros |
| Perda secundária por evento (clientes, titulares, ANPD, Justiça) | **Lognormal(μ, σ)** com teto | Cauda longa: na maioria das vezes é pequena, às vezes é enorme (TCC1 §3.6, item 3) |

Parametrização da Lognormal por dois pontos intuitivos, a **mediana** e o **p95**:

- μ = ln(mediana)
- σ = [ln(p95) − ln(mediana)] / 1,645

O valor sorteado é limitado a `teto_pct_faturamento × faturamento` (censura à direita), para que a cauda infinita
da Lognormal não gere perdas economicamente impossíveis para o porte.

Perda anual de um cenário na iteração *i*: Σ (primária + secundária) sobre os N ~ Poisson(LEF) eventos do ano.

## Alternativas descartadas
- **Só Beta-PERT:** subestima eventos extremos (multas, ações coletivas), justamente os que quebram uma PME.
- **Só Lognormal:** exige parâmetros que o usuário leigo não sabe estimar e não tem limite natural para custos diretos.
- **PERT como entrada e Lognormal "ajustada" a ela:** mistura as duas numa única grandeza e perde a
  rastreabilidade com a ontologia FAIR (RNF07).

## Consequências
- O texto do TCC2 deve explicar os itens 2 e 3 do §3.6 como primária (PERT) e secundária (Lognormal).
- `audit/cenarios.yaml` declara os blocos `perda_primaria` e `perda_secundaria` separadamente.
- O relatório pode mostrar ao gestor quanto do risco vem de custos diretos e quanto vem da reação de terceiros.
