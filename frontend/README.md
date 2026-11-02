# Frontend CiberDecide (React + TypeScript + Tailwind)

Jornada do gestor: **Empresa → Dinheiro e limites → O que proteger → Como é hoje (questionário por função do
NIST CSF) → Resultado** (mapa de calor 3 × 3, riscos um a um, plano de ação, pontos "Não sei" e contribuição
anônima opcional). Decisões de interface no ADR-015.

## Rodar no computador

Precisa do Node.js 20 ou mais novo (https://nodejs.org, versão LTS) e da API rodando (`backend/`).

```bash
cd frontend
npm install          # só na primeira vez
npm run dev          # abre em http://localhost:5173
```

Em outro terminal, a API: `cd backend`, ative o ambiente virtual e rode `uvicorn riskpme.api.app:app --reload`.

| Comando | O que faz |
|---|---|
| `npm run build` | confere os tipos e gera `dist/` para publicar |
| `npm test` | testes do glossário e da formatação (Vitest) |
| `npm run lint` | análise do código (oxlint) |
| `npm audit` | vulnerabilidades conhecidas nas dependências |

Em desenvolvimento, o site chama `/api` e o Vite repassa para a API em `http://127.0.0.1:8000`, sem CORS. Se
aparecer "O servidor de cálculo não respondeu", a API não está rodando no outro terminal. Em produção,
`VITE_API_URL` aponta para o endereço público da API (veja `.env.example`).

## Onde mexer

- `src/marca.ts`: nome e frases da marca (trocar aqui muda a interface inteira).
- `src/index.css`: cores e fontes (identidade sóbria: marinho, marfim, verde petróleo, dourado).
- `src/telas/`: as telas; `src/componentes/base.tsx`: peças comuns (glossário sublinhado, "Para o técnico").
- Os textos de perguntas, ajudas, recomendações e glossário vêm da API (`audit/*.yaml`), não ficam aqui.
