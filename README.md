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
| RF01 Perfil (setor/porte) | `audit/portes.yaml`, `audit/setores.yaml` |
| RF02 Calibração financeira | `audit/contexto.yaml` |
| RF03 Apetite e tolerância | `audit/contexto.yaml` (bloco `calibracao_risco`) |
| RF04 Questionário NIST | `audit/perguntas.yaml` |
| RF05 Mapeamento de ativos | `audit/contexto.yaml` (bloco `ativos`) |
| RF06 Tradução → FAIR | meta-tag `cenarios` de cada pergunta; `backend/src/riskpme/engine` |
| RF07 TEF por setor | `audit/cenarios.yaml` × multiplicadores de `setores.yaml` e `portes.yaml` |
| RF08 Beta-PERT | `perda_primaria` de `audit/cenarios.yaml`; `backend/src/riskpme/engine/distribuicoes.py` |
| §3.6 Lognormal no Monte Carlo | `perda_secundaria` de `audit/cenarios.yaml` (ADR-002) |
| RF09–RF12 | backend/frontend (próximas etapas) |
| RNF04 Linguagem acessível | `audit/glossario.yaml`, `ajuda` obrigatória, validador de linguagem (ADR-007) |
| RNF01/RNF02 | Simulação sem estado; contribuição anonimizada só com consentimento (ADR-005) |

## Rodando o validador do catálogo

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
riskpme-catalogo validar          # checa integridade do catálogo
riskpme-catalogo questionario 3 saude   # mostra o questionário de um perfil
riskpme-catalogo custos ../docs/memoria-custos.md   # memória de cálculo dos custos
pytest
```
