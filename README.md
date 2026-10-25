# RiscoPME — Ferramenta de apoio à decisão em risco cibernético para PMEs

Trabalho de Conclusão de Curso — Engenharia de Sistemas / UFMG
Autora: Vitória Medeiros Carrera de Oliveira · Orientador: Prof. Ramon Lacerda Marques

A ferramenta guia o gestor de uma PME por um questionário em linguagem simples,
traduz as respostas em variáveis da ontologia **FAIR**, estima perdas anuais por
**Simulação de Monte Carlo** e entrega um **mapa de calor** e um **plano de ação**
com controles priorizados, seguindo o processo da **ABNT NBR ISO/IEC 27005:2023**.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `audit/` | Catálogo de auditoria em YAML: portes, setores, cenários de risco, perguntas (com meta-tags FAIR), controles ISO/IEC 27002:2022, glossário, fontes. Editável sem mexer no código. |
| `backend/` | Python (FastAPI + NumPy): carregamento/validação do catálogo, motor FAIR + Monte Carlo, API e relatório PDF. |
| `frontend/` | React + TypeScript (Vite). |
| `infra/` | Dockerfiles, docker-compose e configuração de deploy. |
| `docs/adr/` | Registros de decisão de arquitetura (citáveis na monografia). |
| `docs/referencias.bib` | Referências BibTeX de todas as fontes do catálogo (chaves = `fonte` nos YAML). |
| `docs/memoria-custos.md` | Memória de cálculo do custo dos controles (gerada por `riskpme-catalogo custos`). |

## Rastreabilidade com o TCC1

| Requisito | Onde |
|---|---|
| RF01 Perfil (setor/porte) | `audit/portes.yaml` (porte pela receita bruta, ADR-010), `audit/setores.yaml` (ADR-011) |
| RF02 Calibração financeira | `audit/contexto.yaml` |
| RF03 Apetite e tolerância | `audit/contexto.yaml` (bloco `calibracao_risco`; matriz 3 × 3, ADR-012) |
| RF04 Questionário NIST | `audit/perguntas.yaml` |
| RF05 Mapeamento de ativos | `audit/contexto.yaml` (bloco `ativos`: ativo crítico, tipo de dado, nº de pessoas com dados, nº de usuários — ADR-009) |
| RF06 Tradução → FAIR | meta-tag `cenarios` de cada pergunta; prevenção → frequência, detecção e resposta → prejuízo (ADR-014); `backend/src/riskpme/engine` |
| RF07 TEF por setor | `audit/cenarios.yaml` × multiplicadores de `setores.yaml` e `portes.yaml` |
| RF08 Beta-PERT | `perda_primaria` de `audit/cenarios.yaml`; `backend/src/riskpme/engine/distribuicoes.py` |
| §3.6 Lognormal no Monte Carlo | `perda_secundaria` de `audit/cenarios.yaml` (ADR-002) |
| RF09 Monte Carlo | `backend/src/riskpme/engine/simulacao.py` (comando `riskpme-catalogo simular`) |
| RF10 Mapa de calor | matriz 3 × 3 com horizonte de 5 anos (`contexto.yaml`, bloco `matriz`; ADR-012) |
| RF11 Plano de ação | `backend/src/riskpme/engine/plano.py` (ROSI, Gordon-Loeb, período ruim e preparação; ADR-013) |
| RF12 Relatório | frontend e PDF (próximas etapas); dados prontos em `POST /simulacoes` |
| RNF04 Linguagem acessível | `audit/glossario.yaml`, `ajuda` obrigatória, validador de linguagem (ADR-007) |
| RNF01/RNF02 | API sem estado (`backend/src/riskpme/api`); contribuição anonimizada só com consentimento em `POST /contribuicoes` (ADR-005) |

## API

```bash
cd backend && uvicorn riskpme.api.app:app --reload      # documentação interativa em http://localhost:8000/docs
```

| Rota | O que faz |
|---|---|
| `GET /saude` | status, versão do catálogo (hash dos YAML) e se a coleta anonimizada está ativa |
| `GET /catalogo` | textos para as telas: instruções, aviso legal, escala, setores, portes, perguntas de contexto, matriz, cenários e glossário |
| `POST /questionario` | `{setor, receita_operacional_bruta, usuarios_ti}` → porte, mensagem do porte e perguntas do perfil (sem recomendações) |
| `POST /simulacoes` | `{perfil, respostas, semente?}` → resultado por cenário, células da matriz 3 × 3 e plano de ação. Não grava nada |
| `POST /contribuicoes` | `{consentimento: true, setor, porte, respostas}` → grava só isso, com versão do catálogo e mês/ano (ADR-005) |

Variáveis de ambiente: `RISKPME_CORS` (origens do frontend, separadas por vírgula; padrão `http://localhost:5173`),
`RISKPME_CONTRIBUICOES_DB` (caminho do SQLite; sem ela a coleta fica desativada e a rota responde 503) e
`RISKPME_AUDIT_DIR` (pasta do catálogo, usada no Docker). Campos desconhecidos são recusados (422), o que impede
que um dado financeiro entre na base de pesquisa por engano.

## Rodando o validador do catálogo

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
riskpme-catalogo validar          # checa integridade do catálogo
riskpme-catalogo questionario 3 saude   # mostra o questionário de um perfil
riskpme-catalogo custos ../docs/memoria-custos.md   # memória de cálculo dos custos
riskpme-catalogo simular ../docs/exemplos/clinica-epp.json --semente 42   # motor completo
pytest
```

No Windows (cmd), troque as duas primeiras linhas por:

```bat
cd backend
py -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```
