# ADR-001 — Stack tecnológica

**Status:** Aceita (24/09/2026)

## Contexto
O TCC1 (§3.4.2) define Python no backend para as simulações e uma interface web sem instalação (RNF05).
O protótipo do TCC2 duplicava o motor em JavaScript, o que exigia validação cruzada entre duas implementações.

## Decisão
- **Backend:** Python 3.11+, FastAPI, NumPy/SciPy, Pydantic. O motor passa a existir **em um só lugar** (Python).
- **Frontend:** React + TypeScript (Vite, Tailwind), consumindo a API.
- **Infra:** Docker/docker-compose; frontend estático em Vercel/Netlify e API em Render/Railway/Fly.io; CI no GitHub Actions.

## Consequências
- Elimina a divergência entre motores Python e JS (fonte única de verdade para as fórmulas — RNF07).
- Exige uma API disponível; a simulação de 10.000 iterações vetorizada em NumPy leva milissegundos (RNF06).
