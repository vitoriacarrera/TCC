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

## Configuração de produção

Aplicada em `render.yaml` e `frontend/vercel.json` (passo a passo em `docs/publicacao.md`):

1. API no Render com `--no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*"
   --limit-concurrency 50`. Aceitar `X-Forwarded-For` de qualquer origem é seguro ali porque o serviço só é
   alcançável pelo proxy do Render; fora dessa situação, restrinja `--forwarded-allow-ips`.
2. `RISKPME_SEGREDO` gerado pelo Render; `RISKPME_DOCS=0`; `RISKPME_CORS` com o endereço exato do site;
   `RISKPME_CONTRIBUICOES_DB` com o PostgreSQL do Neon (TLS obrigatório). Nenhum segredo no repositório.
3. Site no Vercel com cabeçalhos de segurança e CSP restrita: só scripts, estilos e fontes do próprio site
   (fontes empacotadas, sem terceiros), chamadas só para a própria origem e `*.onrender.com`, sem iframes,
   formulários ou objetos. Testado com a jornada completa sob essa política, sem bloqueios.
4. HTTPS obrigatório nos dois (as plataformas terminam o TLS; HSTS ligado).
5. Com mais de uma instância, o limite por cliente passa a valer por instância (aceitável no volume do TCC).

## Revisão da arquitetura publicada (02/11/2026)

Escopo: GitHub (código e CI) → Render (API) e Vercel (site), com publicação automática a partir da `main`, e Neon
(base anonimizada). Verificado: `pip-audit -r requirements.lock` e `npm audit` sem vulnerabilidades conhecidas;
histórico do repositório sem segredos (nenhum endereço de banco, token ou chave versionado); `bandit` sem achados.

| Ameaça | Situação | Medida |
|---|---|---|
| Alguém entra na conta do GitHub, Render, Vercel ou Neon e troca o site ou lê a base | **Maior risco.** Quem controla essas contas controla tudo, e as três últimas entram pelo GitHub | Verificação em duas etapas nas quatro contas, de preferência com aplicativo autenticador ou chave de acesso (passkey) |
| Uma mudança indevida chega à `main` e é publicada sozinha | Publicação automática a cada merge | Regra de proteção da `main`: só por PR e só com o CI verde |
| Integrações do Render e do Vercel com acesso a outros repositórios | Depende de como foram autorizadas | Limitar os dois apps do GitHub ao repositório `TCC` |
| Passo do CI comprometido altera o repositório | Token do CI tinha permissão padrão | **Corrigido:** `permissions: contents: read` no `ci.yml` |
| Dependência ganha uma CVE depois da publicação | O CI só audita quando há push | **Corrigido:** `dependabot.yml` (pip, npm e GitHub Actions, semanal) e alertas do Dependabot |
| Invasor da API lê ou apaga a base da pesquisa | A API usava o usuário dono do banco | **Corrigido no código:** a API só executa CREATE/ALTER quando falta a tabela ou a coluna; em produção, usar um usuário que só tem `INSERT` (abaixo). Mesmo com a API comprometida, ninguém lê, altera ou apaga o que já foi gravado |
| Vazamento do endereço do banco (com senha) | Fica só no Render e no computador da autora | Usuário só de `INSERT` no Render; endereço do dono só no computador da autora, sem colar em código, mensagens ou prints |
| Versões de prévia do Vercel (uma por branch) | São públicas por padrão em algumas configurações | Não alcançam a API: o CORS só aceita `https://ciberdecide.vercel.app` |

### Banco com menor privilégio (passo a passo no Neon)

1. Gere uma senha longa no seu computador: `py -c "import secrets; print(secrets.token_urlsafe(24))"`.
2. No Neon, abra **SQL Editor** (conectado como dono) e rode, trocando a senha:

   ```sql
   ALTER TABLE contribuicoes ADD COLUMN IF NOT EXISTS resultado JSONB;
   CREATE ROLE api_coleta WITH LOGIN PASSWORD 'COLE_A_SENHA_AQUI';
   GRANT USAGE ON SCHEMA public TO api_coleta;
   GRANT INSERT ON contribuicoes TO api_coleta;
   ```

   Crie o usuário por SQL, e não pela tela de Roles: usuários criados pela tela recebem privilégios amplos.
3. Monte o endereço do novo usuário: o mesmo endereço do dono, trocando `neondb_owner:SENHA` por
   `api_coleta:SENHA_NOVA`.
4. No Render, em **Environment**, troque `RISKPME_CONTRIBUICOES_DB` por esse endereço e salve.
5. Teste uma contribuição pelo site. Para analisar, continue usando o endereço do **dono**, só no seu computador.

## Riscos residuais (para as Limitações)

- Sem autenticação, um robô paciente consegue gerar contribuições plausíveis respeitando os limites.
- O limite em memória zera quando o servidor reinicia.
- Ações do GitHub (`actions/checkout@v4`, `setup-python@v5`) referenciadas por versão, não por hash do commit.
