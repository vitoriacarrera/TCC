# Segurança da API (verificação de 25/10/2026)

Referências: OWASP API Security Top 10 (2023), OWASP REST Security Cheat Sheet, LGPD art. 46 e ADR-005.
Ferramentas: `pip-audit` (base PyPI/OSV), `bandit` (análise estática), testes automatizados em
`backend/tests/test_api.py` e um teste de entradas aleatórias (400 pedidos malformados, nenhum erro 500).

## Dependências e CVEs

`pip-audit -r backend/requirements.lock`: **nenhuma vulnerabilidade conhecida** nas versões de produção
(FastAPI 0.162.0, Starlette 1.10.0, h11 0.16.0, Uvicorn 0.54.0, Pydantic 2.14.1, NumPy 2.5.4, PyYAML 6.0.3).

Os mínimos antigos do `pyproject.toml` permitiam versões vulneráveis e foram elevados:

| Pacote | Versão antes permitida | CVEs | Corrigido em |
|---|---|---|---|
| starlette | 0.37.2 (via fastapi ≥ 0.110) | CVE-2024-47874 e CVE-2025-54121 (negação de serviço em formulários multipart); CVE-2026-48710 e CVE-2026-54282 (URL reconstruída sem validar Host/caminho); CVE-2026-48817 (despacho de método em `HTTPEndpoint`); CVE-2026-48818 (`StaticFiles` no Windows); CVE-2026-54283 (limites de formulário) | 1.3.1 |
| h11 | 0.14.0 | CVE-2025-43859 (request smuggling em corpo chunked) | 0.16.0 |

A API não usa formulários, `StaticFiles` nem `HTTPEndpoint`, então a exposição real era baixa; os mínimos foram
elevados mesmo assim (`starlette>=1.3.1`, `h11>=0.16.0`, `fastapi>=0.162`). O CI passou a rodar `pip-audit` e
`bandit` a cada push. `bandit`: nenhum achado. O catálogo é lido com `yaml.safe_load`.

## OWASP API Security Top 10 (2023)

| Risco | Situação na RiscoPME |
|---|---|
| API1 Autorização por objeto (BOLA) | Não se aplica: não há objetos por usuário nem ids na URL; nada é guardado por sessão. |
| API2 Autenticação | Sem login por decisão (RNF01, anonimato). A única rota que grava exige comprovante HMAC de uma simulação recente com as mesmas respostas. |
| API3 Autorização por propriedade | Entrada com `extra="forbid"` (campo desconhecido é recusado, inclusive valor financeiro na contribuição). Erros de validação não ecoam o valor recebido. |
| API4 Consumo irrestrito de recursos | Corpo até 32 KB (413), no máximo 100 respostas, números finitos e com teto, textos curtos com padrão `[A-Za-z0-9_-]`; iterações da simulação não são controladas pelo cliente; limite por cliente: 30 simulações/min, 60 questionários/min, 5 contribuições/hora (429). |
| API5 Autorização por função | Não há rotas administrativas; a base de contribuições não tem rota de leitura. |
| API6 Fluxos de negócio sensíveis | Contribuição exige consentimento, comprovante válido por 2 h e respostas idênticas às simuladas; limite de 5/hora. Envenenamento por quem simula muitas vezes continua possível: na análise, aplicar a regra n ≥ 5 por célula e filtrar padrões repetidos. |
| API7 SSRF | Não se aplica: a API não faz chamadas de saída. |
| API8 Configuração insegura | CORS só para origens listadas em `RISKPME_CORS`, sem credenciais; cabeçalhos `nosniff`, `no-store` (respostas com dados financeiros não ficam em cache), `X-Frame-Options: DENY`, CSP `default-src 'none'`, `Referrer-Policy: no-referrer`, HSTS; cabeçalho `server` removido; erro 500 sem detalhes; `/docs` desligável (`RISKPME_DOCS=0`). |
| API9 Inventário | Versão da API (0.3.0) e do catálogo (hash dos YAML) em `GET /saude`; rotas documentadas no README. |
| API10 Consumo inseguro de APIs | Não se aplica: nenhuma API de terceiros é consumida. |

## Privacidade (ADR-005)

- Simulação sem estado; o limite por cliente guarda o endereço só na memória do processo, por no máximo 1 hora,
  sem log nem disco.
- Produção com `--no-access-log` (o log de acesso registraria o IP) e `--no-server-header`.
- O comprovante contém só o prazo e um resumo criptográfico das respostas; não é armazenado.

## Para o deploy (30/10)

1. `RISKPME_SEGREDO` com 32 bytes aleatórios (sem ele, a chave muda a cada reinício e comprovantes antigos
   deixam de valer); `RISKPME_DOCS=0`; `RISKPME_CORS` com o domínio do frontend.
2. `uvicorn riskpme.api.app:app --host 0.0.0.0 --no-access-log --no-server-header --proxy-headers
   --forwarded-allow-ips=<proxy da plataforma> --limit-concurrency 50`. Sem `--proxy-headers`, todos os clientes
   atrás do proxy dividem o mesmo limite; com `--forwarded-allow-ips="*"` fora de um proxy confiável, o limite
   pode ser burlado forjando `X-Forwarded-For`.
3. HTTPS obrigatório (a plataforma termina o TLS); imagem `python:3.12-slim` com usuário não root e
   `pip install -r requirements.lock`.
4. Com mais de uma instância, o limite por cliente passa a valer por instância (aceitável no volume do TCC).

## Riscos residuais (para as Limitações)

- Sem autenticação, um robô paciente consegue gerar contribuições plausíveis respeitando os limites.
- O limite em memória zera quando o servidor reinicia.
- Ações do GitHub (`actions/checkout@v4`, `setup-python@v5`) referenciadas por versão, não por hash do commit.
