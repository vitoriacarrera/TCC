# ADR-015 — Interface do gestor (CiberDecide)

**Status:** Aceita (26/10/2026)

## Decisões
1. **Nome:** CiberDecide (escolhido pela autora entre sugestões que precisavam dizer, sozinhas, que o tema é risco
   cibernético e que a ferramenta apoia decisões). Centralizado em `frontend/src/marca.ts`.
2. **Identidade:** sóbria, de consultoria de negócios, sem estética "high tech": faixas em marinho para contraste,
   fundo marfim, verde petróleo nas ações, dourado em detalhes; títulos com serifa (Source Serif 4), texto sem serifa
   (Source Sans 3). Verde, âmbar e vermelho só no mapa de calor.
3. **Linguagem:** tudo em linguagem de gestor; siglas e números do modelo (LEF, P90, ROSI, controle ISO,
   subcategoria NIST) ficam em "Para o técnico", recolhido. Cada ação do plano tem um título de "o que fazer"
   (`controles.yaml`, campo `acao`); o nome da norma aparece só para o técnico. Palavras do glossário aparecem
   sublinhadas na primeira vez em cada texto e mostram a explicação ao toque.
4. **Plano em três blocos:** "Comece por aqui" (dentro do limite de Gordon-Loeb), "Prepare-se para o pior caso"
   (acima do limite, mas reduzem o prejuízo de riscos de ruptura, ADR-013/014) e "Avalie depois".
5. **Privacidade (ADR-005):** fontes empacotadas no próprio site (sem Google Fonts, que receberia o IP do
   visitante); estado só em `sessionStorage` da aba, apagado ao fechar ou em "Apagar tudo"; nenhum rastreador;
   `referrer` desligado; contribuição com caixa desmarcada por padrão e texto do que é e do que não é enviado.
6. **Celular e computador:** escala de respostas em lista no celular e em 5 colunas no computador; explicação do
   glossário como painel fixo na base da tela do celular.
7. **Relatório:** "Salvar em PDF ou imprimir" pelo navegador, com estilo de impressão; o PDF próprio fica para o
   deploy (30/10), se houver tempo.

## Consequências
- Interface sem textos de domínio próprios: perguntas, ajudas, recomendações e glossário vêm da API, então a revisão
  de linguagem continua num lugar só (`audit/`).
- Teste ponta a ponta (Playwright, computador e celular) percorre a jornada inteira e envia uma contribuição.
