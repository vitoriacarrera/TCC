# ADR-007 — Linguagem acessível no questionário e nos resultados

**Status:** Aceita (24/09/2026)

## Contexto
O público são gestores de PMEs, em geral sem formação em TI (RNF04). Termos como "MFA", "EDR", "backup imutável"
ou "P90" afastam o usuário e aumentam as respostas "chutadas", o que piora a entrada do modelo ("garbage in,
garbage out" — TCC1 §3.8).

## Decisão
1. **Toda pergunta tem `ajuda` obrigatória**, que explica o que é aquilo e por que importa para o negócio, com exemplo.
2. **Glossário único** (`audit/glossario.yaml`) com termos técnicos e conceitos do resultado (apetite, P90,
   Monte Carlo, ROI...). A interface sublinha automaticamente os termos encontrados no texto (`termos_no_texto`).
3. **Lista de siglas proibidas** (`evitar_no_texto`: MFA, EDR, DLP, SOC, WAF...) que não podem aparecer nas perguntas,
   nas ajudas nem nas opções. Nas recomendações podem aparecer, porque também são lidas por quem vai implementar,
   mas precisam ter explicação no glossário.
4. **Validação automática** (`riskpme-catalogo validar`, rodando no CI): siglas proibidas, termos sem explicação e
   perguntas longas demais são barrados antes de chegar ao usuário.
5. **Funções do NIST com nomes do dia a dia** (ex.: DE → "Perceber quando algo dá errado").
6. **Escala de respostas descritiva**, com a opção "Não sei" (tratada de forma conservadora e sinalizada).

## Consequências
Qualquer pergunta nova precisa passar pelo validador; isso vira evidência objetiva de atendimento ao RNF04 na monografia.
Sugestão para a validação no TCC2: teste de compreensão com 3 a 5 gestores reais.
