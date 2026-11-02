# ADR-016 — Base anonimizada em PostgreSQL gerenciado e ferramenta de análise

**Status:** Aceita (02/11/2026)

## Contexto
O objetivo da coleta (ADR-005) é a autora analisar como PMEs de setores e portes diferentes respondem ao
questionário. A primeira versão gravava num arquivo SQLite. Os serviços gratuitos de hospedagem de API (Render,
Railway, Fly.io) usam disco temporário, apagado a cada reinício ou nova versão: as contribuições se perderiam.

## Decisão
1. **Produção em PostgreSQL gerenciado** (plano gratuito do Neon ou do Supabase), indicado por
   `RISKPME_CONTRIBUICOES_DB=postgresql://...`; o SQLite continua para desenvolvimento local (caminho de arquivo).
   Mesma tabela e mesmos campos do ADR-005 (mês/ano, versão do catálogo, setor, porte, respostas); no PostgreSQL,
   respostas em `JSONB` e restrições `CHECK` no porte e no formato do mês.
2. **Leitura só pela autora**, fora da API: `riskpme-catalogo contribuicoes resumo` (contagens e maturidade média
   por função do NIST CSF por total, porte, setor e setor × porte) e `riskpme-catalogo contribuicoes exportar
   dados.csv` (uma linha por contribuição, separador `;`, abre direto no Excel). O resumo só mostra médias de grupos
   com n ≥ 5, como manda o ADR-005; o "Não sei" fica fora da média e aparece em coluna própria.
3. **Falha do banco não derruba a ferramenta:** a simulação continua; a contribuição responde 503 sem detalhes.
4. **Credenciais:** o endereço do banco (com senha) fica só nas variáveis de ambiente da hospedagem e no
   computador da autora; projeto exclusivo no Neon, que contém só esta tabela; conexão com TLS
   (`sslmode=require`). Passo a passo em `docs/publicacao.md`.
5. **Nada versionado:** `.gitignore` bloqueia `*.sqlite`, `*.db` e exportações.

## Consequências
- Dependência `psycopg[binary]`; o CI sobe um PostgreSQL 16 e testa gravação e leitura reais.
- Retenção: a base é apagada após a aprovação final do TCC (ADR-005, item 4); com o banco gerenciado, basta apagar o
  projeto no provedor.
- 02/11/2026: coluna `resultado` (JSONB, opcional) com o resultado sem valores em R$ (ADR-005, revisão de 02/11),
  criada automaticamente em bases antigas (`ADD COLUMN IF NOT EXISTS`). O resumo passa a mostrar, para n ≥ 5, a
  distribuição de cores e de rupturas por cenário, a perda esperada média como fração da receita e as ações mais
  indicadas em "Comece por aqui"; a exportação ganha colunas por cenário e as listas de ações por bloco.
