# ADR-006 — Catálogo de auditoria declarativo e pesos relativos

**Status:** Aceita

## Contexto
São 20 perfis (4 portes × 5 setores). Escrever 20 questionários e 20 tabelas de frequência à mão é inviável e difícil
de auditar. O protótipo do TCC2 usava pesos absolutos por cenário (somando 1), o que quebra quando o questionário
muda de tamanho conforme o porte.

## Decisão
1. **Tudo que é conhecimento de auditoria fica em YAML** (`audit/`), versionado e revisável sem programar.
2. **TEF do perfil = TEF base do cenário × multiplicador do setor × multiplicador do porte.**
3. **Questionário adaptativo:** cada pergunta tem `porte_min` e, opcionalmente, `setores`.
4. **Pesos relativos (1–3)** por pergunta e cenário; o motor **normaliza** sobre as perguntas presentes no perfil:
   `maturidade(s) = Σ(peso·resposta) / (4·Σ peso)`.
5. Resposta **"Não sei" = 1** (conservador) e sinalizada no relatório.

## Consequências
- Adicionar uma pergunta não exige recalibrar pesos manualmente.
- Um validador automático (`riskpme-catalogo validar`) garante que todo cenário tenha perguntas suficientes em todos os 20 perfis.
