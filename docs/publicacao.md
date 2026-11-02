# Publicação do CiberDecide (passo a passo)

Três serviços, todos com plano gratuito e entrada pela conta do GitHub:

| Peça | Serviço | Arquivo de configuração no repositório |
|---|---|---|
| Banco da pesquisa (PostgreSQL) | Neon (neon.tech) | nenhum: a tabela é criada sozinha na primeira contribuição |
| API (cálculo) | Render (render.com) | `render.yaml` |
| Site | Vercel (vercel.com) | `frontend/vercel.json` |

Os três publicam a partir da branch `main`. Toda mudança mesclada na `main` vai para o ar sozinha.

Os planos e as telas dos serviços mudam com o tempo. Se algum botão estiver com outro nome, procure a opção
equivalente.

## 0. Antes de começar

1. Aplique o patch com os arquivos de publicação, suba e **mescle o PR na `main`**.
2. Tenha à mão um bloco de notas para guardar três endereços: o do banco (Neon), o da API (Render) e o do site
   (Vercel).

## 1. Banco de dados no Neon

1. Entre em https://neon.tech e clique em **Sign up**, depois em **Continue with GitHub**.
2. Crie um projeto (**Create project**):
   - nome: `ciberdecide`;
   - versão do PostgreSQL: a sugerida;
   - região: **AWS US East (N. Virginia)**, a mesma que vamos usar no Render, para a API e o banco ficarem perto.
3. No painel do projeto, clique em **Connect**. Aparece o endereço de conexão, parecido com
   `postgresql://neondb_owner:SENHA@ep-xxxx.us-east-1.aws.neon.tech/neondb?sslmode=require`.
4. Copie o endereço completo para o bloco de notas. **Ele contém a senha**: não cole no código, no GitHub, no texto
   do TCC nem em mensagens.

## 2. API no Render

1. Entre em https://render.com e clique em **Get Started**, depois em **GitHub**, e autorize o acesso ao
   repositório `TCC`.
2. No painel, clique em **New +** e depois em **Blueprint**. Escolha o repositório `vitoriacarrera/TCC`.
3. O Render lê o `render.yaml` e mostra o serviço `ciberdecide-api`. Ele pede duas variáveis:
   - `RISKPME_CONTRIBUICOES_DB`: cole o endereço do Neon (passo 1.4);
   - `RISKPME_CORS`: por enquanto, escreva `https://ciberdecide.vercel.app`. Corrigimos no passo 4, se o endereço
     do site sair diferente.
4. Clique em **Apply**. A primeira publicação leva alguns minutos. Acompanhe em **Logs** até aparecer
   "Application startup complete".
5. Copie o endereço do serviço, no topo da página, parecido com `https://ciberdecide-api.onrender.com`.
6. Teste no navegador: `https://ciberdecide-api.onrender.com/saude` deve mostrar
   `"status":"ok"` e `"coleta_anonimizada":true`.

No plano gratuito, a API "dorme" depois de um tempo sem uso, e o primeiro acesso seguinte pode levar perto de um
minuto. Antes de uma demonstração, abra o endereço `/saude` uns minutos antes.

## 3. Site no Vercel

1. Entre em https://vercel.com e clique em **Sign Up**, depois em **Continue with GitHub**.
2. Clique em **Add New...**, depois em **Project**, e importe o repositório `TCC`.
3. Na tela de configuração:
   - **Project Name**: `ciberdecide`;
   - **Root Directory**: clique em **Edit** e escolha `frontend`;
   - **Framework Preset**: Vite (o Vercel detecta sozinho);
   - **Environment Variables**: nome `VITE_API_URL`, valor = endereço da API do passo 2.5, **sem barra no final**.
4. Clique em **Deploy**. Em um ou dois minutos o site estará no ar.
5. Copie o endereço de produção, mostrado em **Domains**, parecido com `https://ciberdecide.vercel.app`.

## 4. Ligar o site à API

A API só aceita chamadas do endereço do site (CORS).

1. Se o endereço do passo 3.5 for exatamente `https://ciberdecide.vercel.app`, pule para o passo 5.
2. Se for outro, volte ao Render, abra `ciberdecide-api`, vá em **Environment**, edite `RISKPME_CORS`, cole o
   endereço do site sem barra no final e clique em **Save Changes**. O Render publica de novo sozinho.

## 5. Teste completo

1. Abra o site pelo endereço do Vercel, no Chrome ou no Edge.
2. Faça uma análise até o resultado, marque a autorização e clique em **Enviar respostas anônimas**. Deve aparecer
   "Obrigado!".
3. No seu computador, confira se a contribuição chegou ao banco:

   ```bat
   cd C:\Users\lallo\Documents\TCC-repo\backend
   .venv\Scripts\activate
   riskpme-catalogo contribuicoes resumo --banco "ENDEREÇO DO NEON"
   ```

4. Apague as contribuições de teste antes de divulgar o link. No Neon, abra o **SQL Editor** e rode
   `DELETE FROM contribuicoes;`.

## Se algo der errado

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Site mostra "Não foi possível falar com o servidor" | `RISKPME_CORS` diferente do endereço do site, ou `VITE_API_URL` errado | Confira os dois endereços (sem barra no final). Mudou `VITE_API_URL`? No Vercel, vá em **Deployments** e use **Redeploy** |
| Demora perto de um minuto no primeiro acesso | API dormindo (plano gratuito) | Normal; abra `/saude` antes |
| `/saude` mostra `"coleta_anonimizada":false` | `RISKPME_CONTRIBUICOES_DB` vazio no Render | Preencha em **Environment** |
| "Não foi possível registrar agora" ao contribuir | Banco inacessível ou endereço do Neon errado | Confira o endereço e os **Logs** do Render |

## Segurança das contas (faça uma vez)

Veja `docs/seguranca.md`, "Revisão da arquitetura publicada": verificação em duas etapas nas quatro contas,
proteção da branch `main`, apps do GitHub limitados ao repositório e usuário do banco só com `INSERT` no Render.

## Depois da aprovação do TCC

Pelo ADR-005, a base é excluída após a aprovação final: no Neon, abra **Settings** e use **Delete project**.
Exporte antes o que precisar (`riskpme-catalogo contribuicoes exportar ...`).
