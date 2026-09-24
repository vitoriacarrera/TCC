# ADR-005 — Privacidade e efemeridade

**Status:** Aceita

## Contexto
RNF01 (anonimato), RNF02 (efemeridade) e TCC1 §3.9 (Privacy by Design).

## Decisão
- API **sem estado**: cada requisição traz todas as respostas e devolve o resultado; nada é gravado.
- Sem banco de dados, sem login, sem cookies de rastreamento, sem analytics de terceiros.
- Logs de acesso sem corpo de requisição; nível de log não registra payloads.
- PDF gerado em memória e devolvido no próprio response.
- No navegador, o estado vive só em memória da aba (sem localStorage) — fechar a aba apaga tudo.

## Consequências
Não há "salvar e continuar depois". Se desejado no futuro, seria por exportação de um arquivo local pelo próprio usuário.
