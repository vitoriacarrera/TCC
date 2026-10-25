# ADR-012 — Avaliação de riscos em matriz 3 × 3

**Status:** Aceita (12 e 19/10/2026 — revisão C-FAIXA e G4)

## Contexto
A primeira versão tinha 4 faixas sobre o P90 da perda anual, com o limite BAIXO/MÉDIO em 0,5 × apetite (convenção
sem fonte). O P90 anual zera cenários raros (chance < 10% ao ano), escondendo riscos que podem quebrar a empresa.

## Decisão
- **Impacto** (3 níveis, definidos pelo gestor): P90 da perda **nos anos em que o cenário acontece**, abaixo do
  apetite / entre apetite e tolerância / acima da tolerância.
- **Probabilidade** (3 níveis, convenção declarada): rara < 10%/ano; possível 10% a 50%; provável > 50%.
- **Cor** pela soma dos níveis: 2–3 verde, 4 amarelo, 5–6 vermelho.
- **Rara + acima da tolerância**: selo "risco de ruptura", com tratamento por preparação e transferência
  (backup isolado testado, contingência, seguro cibernético), enquanto vermelhos pedem redução (ISO/IEC 27005).
  A alternativa de pintar de vermelho foi descartada porque achata a priorização.

## Consequências
- Bloco `matriz` em `audit/contexto.yaml`; conceitos `mapa_calor`, `p90` e `limite_investimento` no glossário.
- O motor (Etapa 2) calcula o P90 condicional e aplica a regra de cor.
