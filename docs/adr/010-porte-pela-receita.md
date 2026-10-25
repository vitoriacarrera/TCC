# ADR-010 — Porte classificado pela Receita Operacional Bruta

**Status:** Aceita (12/10/2026 — revisão S1 e S2)

## Contexto
O TCC1 (Tabela 3.1) pedia que o gestor escolhesse o porte, com critérios de pessoas e de receita misturados. A
classificação oficial brasileira é pela receita bruta anual (LC 123/2006 para MEI, ME e EPP; BNDES para a média
empresa). Os multiplicadores de frequência por porte eram julgamento.

## Decisão
1. O gestor informa a **receita operacional bruta** dos últimos 12 meses (`contexto.yaml`, com "como calcular" e
   "onde encontrar"); `Catalogo.classificar_porte(rob)` define o nível:

   | Nível | ROB anual | Base |
   |---|---|---|
   | 1 | até R$ 81 mil | LC 123/2006, art. 18-A (faixa de receita do MEI) |
   | 2 | até R$ 360 mil | LC 123/2006, art. 3º, I |
   | 3 | até R$ 4,8 mi | LC 123/2006, art. 3º, II |
   | 4 | até R$ 300 mi | BNDES |

   Acima de R$ 300 mi: fora do escopo. Sem opção "não sei" por faixa: pede-se valor aproximado.
2. `multiplicador_tef` por porte calculado do UK CSBS 2025/26 (% que identificou ataque em 12 meses: micro 42%,
   pequena 46%, média 65%), λ = −ln(1 − p), normalizado pela pequena empresa: **0,88 / 0,88 / 1,00 / 1,70**.

## Consequências
- A classificação serve só para o perfil de risco; a tela avisa que não muda o enquadramento tributário.
- Limitações: dado do Reino Unido; o CSBS não distingue MEI de microempresa (mesmo multiplicador).
