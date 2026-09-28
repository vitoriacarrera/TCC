# ADR-003 — Fonte dos controles recomendados

**Status:** Proposta

## Contexto
O RF11 pede "lista priorizada de controles ISO 27005". A ISO/IEC 27005:2023 define o **processo** de gestão de
riscos e, na etapa de tratamento, remete à comparação com os controles do Anexo A da ISO/IEC 27001:2022, cujo
detalhamento está na ISO/IEC 27002:2022. A 27005 não possui catálogo próprio de controles.

## Decisão
Cada recomendação do plano de ação referencia um controle da **ABNT NBR ISO/IEC 27002:2022** (ex.: 8.13 Backup),
e cada pergunta referencia também a subcategoria do NIST CSF correspondente. O processo (contexto → identificação →
análise → avaliação → tratamento) segue a 27005.

## Consequências
Redação sugerida para o RF11 no TCC2: "Lista priorizada de controles da ISO/IEC 27002:2022, selecionados no processo
de tratamento de riscos da ISO/IEC 27005:2023".
