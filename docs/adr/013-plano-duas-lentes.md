# ADR-013 — Plano de ação com duas lentes: retorno médio e proteção contra o período ruim

**Status:** Aceita (25/10/2026 — revisão M2; item 3 atualizado pelo ADR-014)

## Contexto
O plano priorizava só pelo ROSI sobre a perda esperada (ENISA, 2012) com o limite de Gordon e Loeb (2002). No
primeiro uso do motor (clínica EPP de saúde), só 1 de 23 ações teve ROSI positivo: a média dilui eventos raros e
graves (vazamento com P90 de R$ 437 mil e 3% de chance ao ano pesa cerca de R$ 13 mil na média). Gordon-Loeb
supõe decisor neutro ao risco; uma PME é avessa ao risco, porque um ano ruim pode encerrar a empresa.

## Decisão
1. **ROSI continua sendo o critério de ordem** (sem custo primeiro, depois ROSI decrescente) e o limite de
   Gordon-Loeb continua marcando as ações acima dele.
2. **Segunda informação por ação (M2 b):** quanto ela reduz o **prejuízo num período ruim**, o P90 da perda
   somada nos 5 anos do horizonte da matriz (ADR-012). Calculado com números aleatórios comuns: as perdas por
   evento e o uniforme que define o número de eventos são sorteados uma vez, e só a LEF muda (inversão da CDF de
   Poisson, monotônica), para que a diferença não seja ruído. Semente fixa por padrão: o mesmo perfil gera o mesmo
   plano.
3. **Riscos de ruptura (M2 c):** as ações ligadas a perguntas de preparação, funções Responder (RS) e Recuperar
   (RC) do NIST CSF 2.0, backup (PR.DS-11) e resiliência (PR.IR-03), que alimentam um cenário em ruptura, são
   marcadas como "protege contra ruptura", mesmo com ROSI negativo, com texto que as explica como seguro.
   Lista declarada em `contexto.yaml` (`matriz.selo_ruptura.preparacao`, fonte `nistcsf2`).

## Consequências
- `Acao.reducao_periodo_ruim` e `Acao.protege_ruptura`; `Plano.perda_periodo_ruim_atual`, `Plano.horizonte_anos`
  e a lista `preparacao` em cada risco de ruptura. Conceito `periodo_ruim` no glossário.
- Custo computacional: uma avaliação vetorizada por ação (< 0,5 s para a clínica).
- A limitação original (respostas só alteravam a frequência) foi resolvida pelo ADR-014: as perguntas de
  detecção e resposta passaram a reduzir o prejuízo, e a lista de preparação passou a ser
  `parametros_modelo.efeito_magnitude` em `cenarios.yaml`.
- No texto do TCC: discutir os limites da perda esperada para decisores avessos ao risco (Resultados e Conclusão).
