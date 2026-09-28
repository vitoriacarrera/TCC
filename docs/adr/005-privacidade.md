# ADR-005 — Privacidade, efemeridade e base anonimizada para pesquisa

**Status:** Aceita (24/09/2026) · revisada em 28/09/2026 (coleta anonimizada com consentimento)

## Contexto
RNF01 (anonimato), RNF02 (efemeridade) e TCC1 §3.9 (Privacy by Design). Para avaliar o TCC, a autora precisa
analisar como PMEs de diferentes setores e portes responderam ao questionário.

## Decisão
1. **Simulação continua sem estado:** a API de cálculo não grava nada; dados de contexto (faturamento, custo/hora,
   registros) e relatórios são descartados ao fim da sessão. Sem login, sem cookies de rastreamento, sem analytics
   de terceiros; logs sem corpo de requisição.
2. **Contribuição anonimizada opcional (opt-in):** ao final, o usuário pode marcar (desmarcado por padrão)
   "Autorizo o uso anônimo das minhas respostas para pesquisa acadêmica". Só então é gravado, por um endpoint
   separado (`POST /contribuicoes`):
   - setor, nível de porte (1–4), respostas 0–4/"não sei" por id de pergunta, versão do catálogo, mês/ano;
   - **não** são gravados: faturamento ou outros valores financeiros, nº de registros, ativo crítico, IP,
     user-agent, horário exato, texto livre, qualquer id que ligue a contribuição à sessão.
3. **Minimização contra reidentificação:** análises publicadas só por agregados com n ≥ 5 por célula
   setor × porte; células menores são agrupadas.
4. **Retenção:** a base é excluída após a aprovação final do TCC.
5. **Ética:** confirmar com a UFMG se a coleta se enquadra na dispensa de apreciação pelo CEP
   (Res. CNS 510/2016, art. 1º, parágrafo único, I e V). Dado anonimizado não é dado pessoal (LGPD, art. 12),
   mas o termo de consentimento é mantido por transparência.

## Consequências
- Passa a existir um banco de dados (apenas para contribuições), isolado da API de cálculo.
- Redação sugerida para o RNF02 no TCC2: "Dados identificáveis e relatórios são excluídos ao fim da sessão; com
  consentimento explícito, uma versão anonimizada das respostas (setor, porte e respostas) é retida para fins
  acadêmicos até a aprovação do trabalho."
