# ADR-004 — Versão do NIST CSF

**Status:** Aceita (24/09/2026) — decisão da autora

## Contexto
O TCC1 (RF04, §3.4.1) cita os "cinco pilares" do NIST CSF (Identificar, Proteger, Detectar, Responder, Recuperar).
Em fev/2024 o NIST publicou o **CSF 2.0**, que acrescenta a função **Governar (GV)** — responsabilidades,
política, gestão de riscos de fornecedores — e publicou guias de início rápido para pequenas empresas.

## Decisão
Etiquetar as perguntas com as **6 funções do CSF 2.0** e as subcategorias 2.0 (ex.: `PR.AA-03`).

## Alternativa
Manter 5 funções, aderente ao texto do TCC1: basta mapear `GV → ID` na exibição. O campo `funcao` do catálogo
permite trocar sem reescrever perguntas.

## Justificativa
Governança e risco de fornecedores são justamente pontos fracos de PMEs; usar a versão vigente evita crítica de
banca por referência desatualizada.

## Na interface
As funções aparecem com nomes amigáveis (`audit/perguntas.yaml`, bloco `funcoes`): Organização e regras (GV),
Conhecer o que proteger (ID), Proteção no dia a dia (PR), Perceber quando algo dá errado (DE), Reagir a um problema (RS)
e Voltar a funcionar (RC). O TCC2 deve atualizar o RF04 e o §3.4.1 de "cinco pilares" para as seis funções do CSF 2.0.
