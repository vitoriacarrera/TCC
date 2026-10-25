# Infraestrutura

Etapa 6: Dockerfiles (API e frontend), `docker-compose.yml` para desenvolvimento local e configuração de deploy
(frontend em Vercel/Netlify, API em Render/Railway/Fly.io). Requisitos: a API de simulação não grava nada; o único armazenamento é o SQLite das contribuições anonimizadas (`RISKPME_CONTRIBUICOES_DB`, volume pequeno), conforme a revisão de 28/09 do ADR-005. Rodar o uvicorn com `--no-access-log` para não registrar IP.
