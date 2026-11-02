# Infraestrutura

A publicação usa serviços gerenciados, sem servidor próprio:

- API: Render, configurada por `render.yaml` na raiz do repositório;
- site: Vercel, configurado por `frontend/vercel.json`;
- base anonimizada da pesquisa: PostgreSQL no Neon (ADR-016).

Passo a passo em `docs/publicacao.md`; configuração de segurança em `docs/seguranca.md`.
