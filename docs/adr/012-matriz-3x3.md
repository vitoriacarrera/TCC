# ADR-012 — Avaliação de riscos em matriz 3 × 3

**Status:** Aceita (12 e 19/10/2026 — revisão C-FAIXA e G4; horizonte de 5 anos em 25/10 — revisão M1)

## Contexto
A primeira versão tinha 4 faixas sobre o P90 da perda anual, com o limite BAIXO/MÉDIO em 0,5 × apetite (convenção
sem fonte). O P90 anual zera cenários raros (chance < 10% ao ano), escondendo riscos que podem quebrar a empresa.

## Decisão
- **Impacto** (3 níveis, definidos pelo gestor): P90 da perda **nos anos em que o cenário acontece**, abaixo do
  apetite / entre apetite e tolerância / acima da tolerância.
- **Probabilidade** (3 níveis, convenção declarada): chance de pelo menos um evento **nos próximos 5 anos**,
  1 − e^(−5 × LEF): rara < 10%; possível 10% a 50%; provável > 50% (revisão M1, ver abaixo).
- **Cor** pela soma dos níveis: 2–3 verde, 4 amarelo, 5–6 vermelho.
- **Rara + acima da tolerância**: selo "risco de ruptura", com tratamento por preparação e transferência
  (backup isolado testado, contingência, seguro cibernético), enquanto vermelhos pedem redução (ISO/IEC 27005).
  A alternativa de pintar de vermelho foi descartada porque achata a priorização.

## Consequências
- Bloco `matriz` em `audit/contexto.yaml`; conceitos `mapa_calor`, `p90` e `limite_investimento` no glossário.
- O motor (Etapa 2) calcula o P90 condicional e aplica a regra de cor.

## Revisão M1 (25/10/2026): horizonte de 5 anos no eixo de probabilidade
Com a frequência recalibrada pelos eventos de perda do UK CSBS (ADR-011, CJ1), cada cenário fica com 1% a 5% de
chance por ano e todos caíam em "rara": a matriz usava uma coluna só. Alternativas avaliadas: manter (mapa sem
poder de discriminação) e reescalar os limites aos dados (cortes sem fonte, contra o princípio de dados antes de
julgamento). Decisão: medir a chance num horizonte de 5 anos, o mesmo da vida útil dos controles (`custos.yaml`,
K1), mantendo 10% e 50%. O FAIR define risco como frequência num período escolhido por quem modela; o horizonte
alinha a matriz ao plano de ação. Na clínica de exemplo, vazamento, fraude e indisponibilidade passam a "possível"
e a chance de algum prejuízo vai de 12% no ano para 48% em 5 anos. O impacto continua sendo o P90 do ano em que o
cenário acontece. `matriz.horizonte_anos` em `contexto.yaml`; o validador avisa se ele divergir da vida útil.
