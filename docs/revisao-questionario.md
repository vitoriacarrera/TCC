# Revisão do banco de perguntas

Gerado por `riskpme-catalogo revisao`. Edite `audit/perguntas.yaml`, não este arquivo.

## Perguntas por perfil

| Porte | varejo | servicos | saude | industria | tecnologia |
|---|---|---|---|---|---|
| 1 | 12 | 12 | 12 | 12 | 12 |
| 2 | 22 | 22 | 21 | 22 | 22 |
| 3 | 30 | 30 | 30 | 31 | 30 |
| 4 | 43 | 43 | 43 | 44 | 43 |

## Organização e regras (GV)

_Quem cuida da segurança, que regras existem e como os fornecedores são escolhidos._

### GV-01 — Alguém da empresa, ou uma empresa contratada, é responsável por cuidar da segurança digital, mesmo que também faça outras coisas?

**Respostas:** (0) Ninguém cuida disso · (1) Alguém resolve só quando aparece um problema · (2) Alguém cuida, mas só de parte dos sistemas ou sem tempo reservado · (3) Há um responsável, mas a função não está formalizada · (4) Há um responsável definido por escrito, com tarefas e tempo reservados

**Ajuda:** Pode ser alguém da empresa ou uma empresa de TI contratada, e não precisa ser especialista nem ter dedicação exclusiva. O importante é existir alguém que lembre das tarefas (atualizar, conferir o backup, tirar acessos de quem saiu) e que todos saibam a quem recorrer. Quando é "responsabilidade de todos", na prática fica sem dono.

**Recomendação:** Escolha uma pessoa como responsável pela segurança digital e reserve algumas horas por mês para essa função. Se contratar uma empresa de TI, deixe no contrato o que ela faz em segurança (por exemplo: backup, atualizações, antivírus e atendimento a incidentes) e mantenha alguém da empresa como ponto de contato.

`CSF GV.RR-02` · `ISO 27002 5.2` · porte ≥ 2 · setores: todos · pesos: RAN 1, VAZ 1, FRA 1, IND 1, TER 1, IA 1

### GV-02 — A empresa tem regras sobre como usar senhas, e-mail, computadores e dados, e as pessoas conhecem essas regras?

**Respostas:** (0) Não há regras · (1) Há orientações soltas, passadas quando alguém pergunta · (2) Há regras só para alguns temas, ou só algumas pessoas as conhecem · (3) Há regras que todos seguem, mas não estão escritas · (4) Há regras escritas, conhecidas por todos e revisadas periodicamente

**Ajuda:** Uma política de segurança pode ter poucas páginas, com regras como "não compartilhe senhas", "não use pendrive pessoal" e "desconfie de pedidos urgentes de pagamento". Regras combinadas por escrito evitam que cada um faça de um jeito e mostram a todos o que fazer quando algo der errado.

**Recomendação:** Escreva uma política de segurança curta, apresente à equipe, peça que todos assinem que leram e revise uma vez por ano. Ela deve cobrir, no mínimo: (1) quem é o responsável pela segurança e o papel de cada um; (2) quais informações são sigilosas e quem pode vê-las; (3) regras de acesso: um usuário por pessoa, só o necessário para a função, revisão a cada três meses e retirada no desligamento; (4) senhas e verificação em duas etapas; (5) uso de e-mail, internet, celular ou computador pessoal e ferramentas de IA; (6) cuidados com os equipamentos: atualizações, antivírus, bloqueio de tela; (7) backup: frequência, cópia separada e testes; (8) cuidados com fornecedores; (9) como avisar um problema, como os alertas são classificados por gravidade e em quanto tempo cada um é atendido; (10) treinamento anual. Esta lista não é uma exigência legal: ela segue normas internacionais de segurança da informação e serve como referência de boa prática.

`CSF GV.PO-01` · `ISO 27002 5.1` · porte ≥ 3 · setores: todos · pesos: RAN 1, VAZ 1, FRA 1, IA 1

### GV-03 — Antes de contratar um fornecedor que vai guardar seus dados ou acessar seus sistemas, vocês verificam se ele se protege bem e colocam isso no contrato?

**Respostas:** (0) Não verificamos · (1) Verificamos só de vez em quando, sem critério · (2) Verificamos só alguns fornecedores, ou verificamos mas não colocamos no contrato · (3) Verificamos todos e incluímos no contrato, mas sem roteiro escrito · (4) Verificamos todos com um roteiro escrito, e as exigências ficam no contrato

**Ajuda:** Contador, empresa de TI, sistema de gestão online e agência de marketing costumam ter acesso a informações importantes. Se o fornecedor sofre um ataque, a sua empresa também é atingida. Perguntar se ele faz backup e usa verificação em duas etapas, e incluir cláusula de sigilo e de aviso em caso de incidente, já reduz muito esse risco.

**Recomendação:** Faça uma lista dos fornecedores que acessam seus dados e inclua nos contratos cláusulas de segurança, sigilo e obrigação de avisar sobre incidentes.

`CSF GV.SC-05` · `ISO 27002 5.19` · porte ≥ 2 · setores: todos · pesos: TER 3, VAZ 1

### GV-04 — A empresa já colocou em prática o básico da LGPD, por exemplo um aviso aos clientes explicando como usa os dados deles?

**Respostas:** (0) Ainda não fizemos nada sobre a LGPD · (1) Fizemos algo pontual, como um aviso no site, sem continuidade · (2) Parte do básico está feita, mas falta o restante · (3) O básico está feito, mas sem documentação · (4) O básico está feito, documentado e é revisado periodicamente

**Ajuda:** A LGPD (Lei Geral de Proteção de Dados) vale para empresas de todos os tamanhos que guardam dados de pessoas. Microempresas e empresas de pequeno porte têm regras mais simples, mas todas continuam responsáveis por proteger esses dados e podem ser multadas se houver vazamento por descuido.

**Recomendação:** Faça um diagnóstico simples do que a LGPD exige da empresa e publique um aviso de privacidade explicando quais dados vocês coletam, para quê e com quem compartilham. Microempresas e empresas de pequeno porte têm regras simplificadas (Resolução CD/ANPD nº 2/2022): não precisam indicar um encarregado de dados, mas precisam manter um canal para os clientes tirarem dúvidas e pedirem acesso ou exclusão dos seus dados, e têm prazo em dobro para responder. Atenção: essas facilidades não valem se a empresa trata dados de muitas pessoas e esses dados forem sensíveis (como saúde ou biometria) ou de crianças e idosos; nesse caso, siga as regras completas. Esta é uma orientação geral, não um parecer jurídico: para confirmar as obrigações da sua empresa, consulte um advogado especializado em proteção de dados.

`CSF GV.OC-03` · `ISO 27002 5.34` · porte ≥ 2 · setores: todos · pesos: VAZ 2, IA 1

**Variante (portes 4):**

- recomendacao: Faça um diagnóstico do que a LGPD exige da empresa, publique um aviso de privacidade e indique um encarregado de dados (uma pessoa da empresa ou um serviço contratado), divulgando o contato dele no site. Médias empresas não têm as regras simplificadas para pequenos negócios. Esta é uma orientação geral, não um parecer jurídico: para confirmar as obrigações da sua empresa, consulte um advogado especializado em proteção de dados.

### GV-05 — Pelo menos uma vez por ano, a direção para para avaliar os riscos digitais e decidir quanto investir em segurança?

**Respostas:** (0) Isso não acontece · (1) Só acontece depois de algum problema · (2) Acontece às vezes, sem chegar a decisões de investimento · (3) Acontece todo ano, mas sem registro · (4) Acontece todo ano, com registro das decisões e acompanhamento

**Ajuda:** Segurança digital funciona melhor como decisão de gestão, com orçamento definido, do que como gasto de emergência depois de um problema. Esta própria análise é um exemplo do que pode ser revisto todo ano.

**Recomendação:** Uma vez por ano, reserve uma reunião da direção para olhar os riscos digitais. Leve o resultado desta ferramenta (mapa de riscos e plano de ação), os incidentes e alertas graves do ano, o andamento das ações do ano anterior e o que mudou na empresa (sistemas, fornecedores, unidades novas). Decidam quais riscos a empresa aceita e quais vai tratar, aprovem um orçamento de segurança para o ano e definam um responsável e um prazo para cada ação. Registre as decisões em ata. Como referência, o relatório mostra a perda anual estimada: investir mais do que cerca de um terço desse valor raramente compensa.

`CSF GV.RM-01` · `ISO 27002 5.1` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, FRA 1, IND 1, TER 1, IA 1

### GV-06 — Está combinado quais ferramentas de Inteligência Artificial (como ChatGPT ou Gemini) podem ser usadas no trabalho e que tipo de informação nunca deve ser colada nelas?

**Respostas:** (0) Não há nada combinado · (1) Cada um decide; às vezes alguém avisa o que não fazer · (2) Está combinado só para algumas ferramentas ou algumas pessoas · (3) Está combinado com todos, mas não está escrito · (4) Está escrito, todos conhecem e é revisado quando surgem ferramentas novas

**Ajuda:** Essas ferramentas ajudam muito, mas tudo o que é colado nelas sai da empresa. Em versões gratuitas, o conteúdo pode ser guardado e usado pelo fornecedor. Colar um contrato, uma lista de clientes ou um prontuário pode virar um vazamento sem ninguém perceber.

**Recomendação:** Defina quais ferramentas de IA podem ser usadas (de preferência versões para empresas, que não usam seus dados para treinamento) e proíba colar dados de clientes ou documentos sigilosos nas demais.

`CSF GV.PO-01` · `ISO 27002 5.10` · porte ≥ 1 · setores: todos · pesos: IA 3

**Variante (portes 1; até 1 usuário(s)):**

- texto: Estão definidas as ferramentas de Inteligência Artificial (como ChatGPT ou Gemini) que você usa no trabalho e o tipo de informação que nunca deve ser colado nelas?
- recomendacao: Escolha as ferramentas de IA que vai usar (de preferência versões para empresas, que não usam seus dados para treinamento) e nunca cole nelas dados de clientes ou documentos sigilosos.
- respostas: (0) Ainda não defini · (1) Penso nisso só de vez em quando · (2) Defini só para algumas ferramentas ou alguns tipos de informação · (3) Está definido, mas não anotei · (4) Está anotado e reviso quando passo a usar uma ferramenta nova

### GV-07 — Os serviços em nuvem que vocês usam (como Google Workspace, Microsoft 365 ou o sistema de gestão online) estão com as opções de segurança ativadas, e está claro o que o fornecedor protege e o que é responsabilidade de vocês?

**Respostas:** (0) Não configuramos nada além do padrão · (1) Ajustamos algo só quando houve problema · (2) Parte das opções está ativada, ou só em alguns serviços · (3) Tudo ativado e responsabilidades claras, mas sem registro · (4) Tudo ativado, com as responsabilidades registradas e revisadas

**Ajuda:** Na nuvem existe responsabilidade compartilhada: o fornecedor garante que o serviço funciona, mas quem controla senhas, permissões e quem acessa o quê é a sua empresa. Muitos recursos de segurança já estão incluídos no plano, só não vêm ligados.

**Recomendação:** Peça a quem administra o Google Workspace, o Microsoft 365 e o sistema de gestão online para seguir a lista de segurança recomendada por cada fornecedor (Google e Microsoft publicam guias e mostram uma nota de segurança no painel de administração). No mínimo, confira: verificação em duas etapas obrigatória para todos; poucas contas de administrador, separadas das de uso diário; compartilhamento de arquivos com pessoas de fora limitado; alertas de login suspeito ligados; e por quanto tempo o fornecedor guarda arquivos apagados. Leia no contrato o que o fornecedor protege e o que fica com a empresa: em geral, ele cuida dos servidores e da estrutura, e a empresa cuida de quem acessa, das configurações e do backup dos próprios dados. Repita a conferência a cada seis meses.

`CSF GV.SC-07` · `ISO 27002 5.23` · porte ≥ 4 · setores: todos · pesos: TER 2, VAZ 1

### VAR-01 — Os pagamentos com cartão passam só por maquininha ou plataforma de pagamento certificada, sem que a empresa guarde números de cartão?

**Respostas:** (0) A empresa guarda números de cartão · (1) Às vezes anotamos dados de cartão, por exemplo em pedidos por telefone · (2) A maioria dos pagamentos passa por maquininha ou plataforma, com exceções · (3) Todos passam por maquininha ou plataforma, sem regra escrita · (4) Todos passam, com regra escrita que proíbe guardar dados de cartão

**Ajuda:** Guardar números de cartão (em planilha, caderno ou sistema próprio) torna a empresa responsável por protegê-los segundo regras rígidas das bandeiras. Maquininhas e plataformas certificadas cuidam disso por você.

**Recomendação:** Use apenas maquininhas e plataformas de pagamento certificadas (padrão PCI DSS) e nunca guarde números de cartão.

`CSF GV.OC-03` · `ISO 27002 5.31` · porte ≥ 1 · setores: varejo · pesos: VAZ 3

### IND-02 — O acesso remoto de técnicos e fornecedores às máquinas é liberado só quando necessário e com usuário individual?

**Respostas:** (0) O acesso fica sempre liberado, com login compartilhado · (1) É liberado quando pedem, sem controle · (2) Há controle só para parte dos técnicos ou das máquinas · (3) Só é liberado quando preciso, com usuário individual, sem registro · (4) Só é liberado quando preciso, com usuário individual e registro de cada acesso

**Ajuda:** Programas de acesso remoto deixados sempre ligados, com senha compartilhada entre técnicos, são uma porta de entrada conhecida para ataques a fábricas.

**Recomendação:** Libere o acesso remoto de fornecedores só no momento do atendimento, com usuário próprio para cada técnico, e desligue-o em seguida.

`CSF GV.SC-05` · `ISO 27002 5.19` · porte ≥ 3 · setores: industria · pesos: TER 2, RAN 2


## Conhecer o que proteger (ID)

_Saber quais equipamentos, sistemas e dados a empresa tem e onde estão._

### ID-01 — A empresa controla quais computadores, celulares e sistemas usa, mantendo essa informação atualizada?

**Respostas:** (0) Não há esse controle · (1) Sabemos de cabeça, e a informação se perde com o tempo · (2) Há controle só de parte dos equipamentos ou dos sistemas · (3) Há controle de tudo, mas sem registro organizado · (4) Há uma lista completa, atualizada sempre que algo muda

**Ajuda:** É um inventário simples, que pode ser uma planilha: qual equipamento, quem usa, qual sistema, quem é o responsável. Sem ele, um notebook antigo esquecido ou um sistema que ninguém atualiza vira a porta de entrada de um ataque.

**Recomendação:** Monte um inventário dos equipamentos e sistemas da empresa. Ele pode ser uma aba da mesma planilha de acessos, para não ter vários controles separados. Para cada item, anote: o que é (notebook, celular, servidor, roteador, câmera, sistema online), quem usa ou é responsável, onde fica, se ainda recebe atualizações do fabricante e se guarda dados importantes. Inclua os celulares e computadores pessoais usados para trabalhar. Revise a cada seis meses e sempre que algo for comprado, trocado ou descartado: equipamento que não está na lista não é protegido nem entra no backup.

`CSF ID.AM-01` · `ISO 27002 5.9` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, IND 1

### ID-02 — Está mapeado onde ficam guardadas as informações importantes da empresa (clientes, financeiro, projetos), ou seja, em quais computadores, nuvens ou sistemas?

**Respostas:** (0) Não está mapeado · (1) Mais ou menos: as informações ficam espalhadas · (2) Está mapeado só para parte das informações · (3) Está claro onde fica tudo, mas não está registrado · (4) Está registrado onde fica cada informação, e isso é revisado periodicamente

**Ajuda:** Informação guardada em lugares sem controle (no computador de cada um, em pendrives, no WhatsApp, em e-mails pessoais) é difícil de proteger e fica fora do backup. Saber onde cada informação está é o que permite mantê-la só em locais seguros, com backup e acesso controlado.

**Recomendação:** Faça uma lista de onde ficam as informações importantes da empresa. Mantenha-as só em locais seguros e com backup: os sistemas da empresa (vendas, financeiro, agenda) e, para documentos e planilhas, uma pasta na nuvem da empresa em que cada pessoa acesse apenas o que precisa para o seu trabalho. Evite cópias soltas em pendrives, computadores pessoais e WhatsApp.

`CSF ID.AM-07` · `ISO 27002 5.9` · porte ≥ 1 · setores: todos · pesos: VAZ 2, RAN 1, TER 1, IA 1

### ID-03 — De tempos em tempos, alguém verifica se o site e os sistemas acessíveis pela internet têm falhas de segurança conhecidas?

**Respostas:** (0) Ninguém verifica · (1) Só quando surge um alerta ou um problema · (2) Verificamos parte dos sistemas, ou sem frequência definida · (3) Verificamos com frequência, mas sem registro · (4) Verificamos com frequência definida, registramos e corrigimos as falhas

**Ajuda:** Criminosos usam programas que varrem a internet o tempo todo procurando sites e sistemas com falhas de segurança conhecidas. Fazer essa mesma verificação antes deles (há serviços e ferramentas para isso) permite corrigir a falha antes que seja explorada.

**Recomendação:** Contrate um especialista para fazer, a cada três meses, uma varredura de vulnerabilidades externa. O que pedir: que ele verifique, de fora da empresa e sem invadir nada, o site, o e-mail, o acesso remoto e os demais sistemas acessíveis pela internet, procurando falhas já conhecidas. O que receber: um relatório com as falhas encontradas, ordenadas da mais grave para a menos grave, e o que fazer para corrigir cada uma. Depois das correções, peça uma nova verificação para confirmar. Esse serviço é diferente de um teste de invasão, que é mais caro e em geral não é necessário para empresas desse porte.

`CSF ID.RA-01` · `ISO 27002 8.8` · porte ≥ 3 · setores: todos · pesos: VAZ 2, RAN 2, IND 1


## Proteção no dia a dia (PR)

_Senhas, cópias de segurança, atualizações e cuidados que evitam problemas._

### PR-01 — Para entrar no e-mail, no banco, nas redes sociais e nos sistemas da empresa, além da senha é preciso confirmar pelo celular (verificação em duas etapas)?

**Respostas:** (0) Em nenhum serviço · (1) Em algum serviço, porque o próprio serviço exigiu · (2) Em parte dos serviços, ou só para algumas pessoas · (3) Em todos os serviços importantes, mas sem regra que obrigue · (4) Em todos, com regra escrita e conferência periódica

**Ajuda:** Com a verificação em duas etapas, além da senha é pedido um código no celular ou um aplicativo. Mesmo que um golpista descubra a senha, ele não consegue entrar sem o seu celular. É uma das proteções mais eficazes e, na maioria dos serviços, é gratuita.

**Recomendação:** Ative a verificação em duas etapas no e-mail, no banco, nas redes sociais e nos sistemas, começando pelo e-mail e pelo banco. Em geral é gratuito e leva poucos minutos.

`CSF PR.AA-03` · `ISO 27002 8.5` · porte ≥ 1 · setores: todos · pesos: VAZ 3, FRA 3, RAN 2, TER 1

### PR-02 — Cada pessoa tem seu próprio usuário e senha, sem compartilhar o mesmo login com colegas?

**Respostas:** (0) Os logins são compartilhados · (1) Cada um tem o seu, mas às vezes compartilhamos · (2) Só parte dos sistemas tem login individual · (3) Todos têm login próprio em todos os sistemas, sem regra escrita · (4) Todos têm login próprio, com regra escrita e conferência periódica

**Ajuda:** Quando várias pessoas usam o mesmo login, não dá para saber quem fez o quê, a senha circula em bilhetes e mensagens, e fica difícil tirar o acesso de quem sai da empresa.

**Recomendação:** Crie um usuário para cada pessoa em todos os sistemas e acabe com os logins compartilhados.

`CSF PR.AA-01` · `ISO 27002 5.16` · porte ≥ 2 · setores: todos · pesos: VAZ 2, FRA 1, RAN 1

### PR-03 — As senhas são longas, diferentes para cada serviço e guardadas em um gerenciador de senhas (e não em papel, planilha ou anotações do celular)?

**Respostas:** (0) Não: as senhas são simples ou repetidas · (1) Algumas senhas são fortes, sem um padrão · (2) Só parte das pessoas ou dos serviços usa senhas fortes ou gerenciador · (3) Todos usam senhas fortes no gerenciador, sem regra escrita · (4) Todos usam gerenciador, com regra escrita e conferência periódica

**Ajuda:** Quando uma mesma senha é usada em vários lugares, basta um site vazar para o criminoso testar a mesma senha no seu e-mail e no seu banco. Um gerenciador de senhas cria e lembra senhas fortes por você.

**Recomendação:** Adote um gerenciador de senhas para a empresa e troque as senhas repetidas ou fáceis de adivinhar.

`CSF PR.AA-01` · `ISO 27002 5.17` · porte ≥ 1 · setores: todos · pesos: VAZ 2, RAN 1, FRA 1

### PR-04 — Quando alguém sai da empresa ou muda de função, os acessos dessa pessoa são retirados no mesmo dia?

**Respostas:** (0) Os acessos não são retirados · (1) São retirados só quando alguém lembra · (2) São retirados em parte, ou só dias depois · (3) São retirados no mesmo dia, mas sem lista do que retirar · (4) São retirados no mesmo dia, seguindo uma lista escrita

**Ajuda:** Ex-funcionários com acesso ativo ao e-mail, à nuvem ou a grupos de WhatsApp da empresa são uma causa comum de vazamentos, por má-fé ou simplesmente porque a conta antiga é invadida depois.

**Recomendação:** Monte uma planilha simples com cada pessoa e os acessos que ela tem: e-mail, sistemas, nuvem, banco, grupos de mensagens e redes sociais da empresa. Use-a de dois jeitos: (1) quando alguém sair ou mudar de função, retire ou ajuste os acessos no mesmo dia, troque as senhas compartilhadas que a pessoa conhecia e recolha os equipamentos; (2) a cada três meses, revise a planilha com o responsável de cada área e remova os acessos que ninguém usa mais ou não precisa, inclusive de fornecedores e ex-estagiários.

`CSF PR.AA-05` · `ISO 27002 5.18` · porte ≥ 2 · setores: todos · pesos: VAZ 2, TER 1

### PR-05 — Cada pessoa acessa só os dados e sistemas de que realmente precisa para trabalhar?

**Respostas:** (0) Todos acessam tudo · (1) Restringimos só em casos pontuais · (2) Só parte dos sistemas tem acesso restrito por função · (3) Cada pessoa acessa só o necessário, sem registro de quem pode o quê · (4) Há um registro de quem acessa o quê, revisado periodicamente

**Ajuda:** Se todos acessam tudo, uma única conta invadida expõe a empresa inteira. Limitar o acesso por função (o estagiário não precisa ver a folha de pagamento) reduz o tamanho do estrago.

**Recomendação:** Defina, para cada função da empresa (por exemplo: vendas, financeiro, atendimento), quais pastas e sistemas ela precisa acessar. Registre esse padrão na planilha de acessos e, na revisão a cada três meses, compare o que cada pessoa tem com o padrão da função dela, retirando o que sobrar. Acessos fora do padrão só com aprovação do responsável pela área, anotada na planilha.

`CSF PR.AA-05` · `ISO 27002 5.15` · porte ≥ 3 · setores: todos · pesos: VAZ 2, IA 1

### PR-06 — As contas de administrador (as que podem instalar programas e mudar configurações) são poucas, usadas só quando necessário e protegidas com verificação em duas etapas?

**Respostas:** (0) Todos usam conta de administrador no dia a dia · (1) Algumas pessoas usam conta comum, sem critério · (2) São poucas, mas usadas no dia a dia ou sem verificação em duas etapas · (3) São poucas, usadas só quando preciso e com verificação em duas etapas · (4) São poucas e protegidas, com regra escrita e revisão periódica de quem tem esse acesso

**Ajuda:** Se a pessoa usa no dia a dia uma conta de administrador e clica em um link malicioso, o vírus ganha o mesmo poder de instalar e apagar tudo. Com uma conta comum, o estrago costuma ficar limitado.

**Recomendação:** Retire o poder de administrador das contas de uso diário e deixe as contas de administrador separadas, com verificação em duas etapas.

`CSF PR.AA-05` · `ISO 27002 8.2` · porte ≥ 3 · setores: todos · pesos: RAN 3, VAZ 1

### PR-07 — As pessoas da empresa recebem orientação, pelo menos uma vez por ano, para reconhecer golpes por e-mail, WhatsApp e telefone?

**Respostas:** (0) As pessoas não recebem orientação · (1) Avisamos só quando aparece um golpe novo · (2) Só parte das pessoas recebe orientação, ou sem frequência definida · (3) Todos recebem orientação todo ano, sem material próprio · (4) Todos recebem orientação todo ano, com material e registro de participação

**Ajuda:** A maioria dos ataques a pequenas empresas começa com uma mensagem falsa que convence alguém a clicar, informar uma senha ou fazer um pagamento. Pessoas que conhecem os golpes mais comuns desconfiam na hora certa.

**Recomendação:** Faça uma conversa ou treinamento curto por ano sobre golpes digitais, mostrando exemplos reais do seu setor.

`CSF PR.AT-01` · `ISO 27002 6.3` · porte ≥ 1 · setores: todos · pesos: FRA 3, RAN 2, VAZ 1, IA 1

**Variante (portes 1; até 1 usuário(s)):**

- texto: Existe um momento definido, pelo menos uma vez por ano, para você se atualizar sobre os golpes mais comuns por e-mail, WhatsApp e telefone?
- recomendacao: Reserve um momento por ano para conhecer os golpes digitais mais comuns no seu setor. A Cartilha de Segurança para Internet do CERT.br é gratuita.
- respostas: (0) Não me atualizo sobre golpes · (1) Leio sobre o assunto só quando aparece na mídia · (2) Busco informação às vezes, sem frequência definida · (3) Faço isso todo ano, mas sem data marcada · (4) Tenho uma data marcada todo ano e anoto o que aprendi

### PR-08 — Vocês fazem simulações de golpe (por exemplo, um e-mail falso de teste) para ver se as pessoas caem?

**Respostas:** (0) Não fazemos · (1) Fizemos uma vez · (2) Fazemos às vezes, ou só com algumas pessoas · (3) Fazemos com frequência, sem registro dos resultados · (4) Fazemos com frequência definida e acompanhamos os resultados

**Ajuda:** É um treino prático: a empresa envia uma mensagem falsa inofensiva e vê quem clica. Quem cai recebe uma orientação na hora. Com o tempo, o número de cliques cai bastante.

**Recomendação:** Contrate um serviço ou especialista para enviar, a cada três meses, e-mails ou mensagens falsas de teste, parecidas com os golpes reais do seu setor (para o técnico: simulação de phishing). Antes, combine com a direção e avise a equipe de que esses testes vão acontecer, sem dizer quando. Quem clicar recebe na hora uma orientação curta mostrando os sinais do golpe: o objetivo é ensinar, não punir. Acompanhe a porcentagem de cliques a cada rodada e use os erros mais comuns no treinamento anual.

`CSF PR.AT-01` · `ISO 27002 6.3` · porte ≥ 4 · setores: todos · pesos: FRA 2, RAN 1

### PR-09 — Antes de pagar um boleto novo ou de aceitar que um fornecedor mudou de conta bancária, vocês confirmam por outro meio (por exemplo, ligando para um número que já conheciam)?

**Respostas:** (0) Não confirmamos · (1) Confirmamos só quando algo parece estranho · (2) Confirmamos só para alguns fornecedores ou valores · (3) Confirmamos sempre, mas sem regra escrita · (4) Confirmamos sempre, com regra escrita que todos conhecem

**Ajuda:** Um golpe muito comum: alguém se passa por fornecedor ou sócio e manda um boleto ou uma conta nova, muitas vezes com urgência. Confirmar por outro canal, nunca pelo telefone ou e-mail que veio na própria mensagem, derruba a maioria desses golpes.

**Recomendação:** Crie a regra da dupla confirmação: boletos novos, mudança de conta bancária e pagamentos "urgentes" só são pagos após confirmação por telefone já conhecido.

`CSF PR.AT-02` · `ISO 27002 5.14` · porte ≥ 1 · setores: todos · pesos: FRA 3

### PR-10 — Vocês fazem cópias de segurança (backup) automáticas das informações importantes, pelo menos uma vez por semana?

**Respostas:** (0) Não fazemos backup · (1) Fazemos manualmente, quando lembramos · (2) Fazemos de parte das informações, ou com frequência menor que semanal · (3) Fazemos backup automático de tudo, sem registro de como funciona · (4) Backup automático de tudo, com rotina escrita e conferência periódica

**Ajuda:** O backup é o que permite recuperar tudo se um vírus trancar os arquivos, um computador quebrar ou alguém apagar algo por engano. Automático é melhor, porque backup que depende de alguém lembrar acaba sendo esquecido.

**Recomendação:** Faça cópias de segurança automáticas das informações importantes pelo menos uma vez por semana, ou com mais frequência se refazer alguns dias de trabalho sair caro. Muitas ferramentas que a empresa já usa (Google Drive, OneDrive, sistema de gestão) têm cópia ou histórico de versões: confira se está ligado. Se não tiverem, faça a cotação de uma ferramenta de backup.

`CSF PR.DS-11` · `ISO 27002 8.13` · porte ≥ 1 · setores: todos · pesos: RAN 3, IND 2, TER 1

**Variante (portes 1):**

- recomendacao: Faça cópias de segurança automáticas das informações importantes pelo menos uma vez por semana, ou com mais frequência se refazer alguns dias de trabalho sair caro. Muitas ferramentas que a empresa já usa (Google Drive, OneDrive, sistema de gestão) têm cópia ou histórico de versões: confira se está ligado. Se não tiverem, faça a cotação de uma ferramenta de backup. Mantenha ao menos uma cópia separada do dia a dia, para que um vírus não apague o backup junto.

### PR-11 — Pelo menos uma cópia do backup fica em um lugar que um vírus não alcança, como um HD desligado ou uma nuvem que não deixa apagar as cópias?

**Respostas:** (0) Não há cópia isolada · (1) Às vezes copiamos para um HD, quando lembramos · (2) Só parte das informações tem cópia isolada · (3) Todas têm cópia isolada, sem rotina escrita · (4) Todas têm cópia isolada, com rotina escrita e conferida

**Ajuda:** O sequestro de dados costuma procurar e trancar também os backups que estão conectados à rede. Uma cópia isolada é o que garante que a empresa consiga se recuperar sem pagar resgate.

**Recomendação:** Siga a regra 3-2-1: três cópias dos dados (o original e dois backups), em dois tipos de lugar diferentes, sendo uma fora da empresa e fora do alcance de um vírus. Na prática, escolha uma destas opções: um serviço de backup na nuvem com bloqueio de exclusão (também chamado de imutabilidade), que impede apagar as cópias por alguns dias mesmo com a senha; ou dois HDs externos usados em rodízio, ligados só durante a cópia e guardados desconectados. Proteja o backup com uma conta e senha diferentes das do dia a dia, com verificação em duas etapas.

`CSF PR.DS-11` · `ISO 27002 8.13` · porte ≥ 2 · setores: todos · pesos: RAN 3

**Variante (portes 2):**

- recomendacao: Siga a regra 3-2-1: três cópias dos dados (o original e dois backups), em dois tipos de lugar diferentes, sendo uma fora da empresa e fora do alcance de um vírus. Na prática, escolha uma destas opções: um serviço de backup na nuvem com bloqueio de exclusão (também chamado de imutabilidade), que impede apagar as cópias por alguns dias mesmo com a senha; ou dois HDs externos usados em rodízio, ligados só durante a cópia e guardados desconectados. Proteja o backup com uma conta e senha diferentes das do dia a dia, com verificação em duas etapas, e a cada três meses teste se consegue recuperar alguns arquivos.

### PR-12 — Vocês testam, pelo menos a cada 3 meses, se conseguem recuperar arquivos do backup?

**Respostas:** (0) Nunca testamos · (1) Testamos só quando precisamos recuperar algo · (2) Testamos às vezes, ou só parte das informações · (3) Testamos a cada 3 meses, sem registro · (4) Testamos a cada 3 meses e registramos o resultado e o tempo gasto

**Ajuda:** É comum descobrir só no dia do problema que o backup estava incompleto, parado havia meses ou que a recuperação leva dias. Testar mostra se ele funciona e quanto tempo leva para voltar a operar.

**Recomendação:** A cada três meses, recupere alguns arquivos do backup e confira se abrem; uma vez por ano, recupere uma pasta ou um sistema inteiro. Anote quanto tempo levou e compare com o prazo que a empresa aguenta ficar parada, definido no plano de recuperação. Se demorar mais, ajuste o backup ou o plano.

`CSF PR.DS-11` · `ISO 27002 8.13` · porte ≥ 3 · setores: todos · pesos: RAN 2, IND 2

### PR-13 — Os notebooks e celulares da empresa pedem senha para desbloquear e têm os dados protegidos por criptografia?

**Respostas:** (0) Não · (1) Alguns aparelhos pedem senha, mas sem criptografia · (2) Só parte dos aparelhos tem senha e criptografia · (3) Todos têm senha e criptografia, sem controle formal · (4) Todos têm, com regra escrita e conferência periódica

**Ajuda:** Se um notebook é roubado no carro ou esquecido em um táxi, a criptografia impede que o ladrão leia os arquivos. No Windows ela se chama BitLocker e no Mac, FileVault. Nos celulares modernos, basta ter senha de bloqueio.

**Recomendação:** Ative a criptografia de disco em todos os notebooks. Ela já vem no Windows (BitLocker, nas versões Pro) e no Mac (FileVault) e faz com que quem roubar ou achar o equipamento não consiga ler os dados. Guarde a chave de recuperação em um lugar seguro fora do notebook, como a conta de administrador da empresa, senão os dados se perdem junto com a senha. Nos celulares, exija senha ou biometria para desbloquear, o que nos aparelhos atuais já liga a criptografia. Configure o bloqueio automático da tela após poucos minutos sem uso e, se possível, use uma ferramenta de gestão de dispositivos que permite apagar os dados à distância em caso de perda ou roubo (para o técnico: MDM).

`CSF PR.DS-01` · `ISO 27002 8.1` · porte ≥ 4 · setores: todos · pesos: VAZ 2

### PR-15 — Vocês guardam só os dados pessoais de que realmente precisam e apagam os antigos que não usam mais?

**Respostas:** (0) Guardamos tudo e não apagamos nada · (1) Apagamos de vez em quando, sem critério · (2) Fazemos isso só com parte dos dados · (3) Guardamos só o necessário e apagamos o antigo, sem regra escrita · (4) Há prazos de guarda escritos, e a exclusão é feita e registrada

**Ajuda:** Quanto menos dados a empresa guarda, menor o estrago se houver vazamento. Cadastros de clientes de dez anos atrás ou currículos antigos são risco sem nenhum benefício.

**Recomendação:** Faça uma tabela com os tipos de dados pessoais que a empresa guarda (clientes, funcionários, ex-funcionários, candidatos, fornecedores), para que cada um é usado e por quanto tempo precisa ser guardado, seja por obrigação legal (documentos fiscais, trabalhistas e contábeis têm prazos próprios) ou por necessidade do negócio. Defina um responsável e, uma vez por ano, apague ou anonimize o que passou do prazo, incluindo cópias em e-mails, planilhas e pastas pessoais, e anote o que foi apagado. Esta é uma orientação geral, não um parecer jurídico: confirme os prazos com o contador e com um advogado.

`CSF PR.DS-01` · `ISO 27002 8.10` · porte ≥ 4 · setores: todos · pesos: VAZ 2

### PR-16 — Computadores, celulares, sistemas e o site recebem as atualizações de segurança assim que saem (atualização automática ligada)?

**Respostas:** (0) As atualizações não são feitas · (1) São feitas quando alguém lembra ou quando o sistema obriga · (2) A atualização automática está ligada só em parte dos equipamentos ou sistemas · (3) Está ligada em tudo, sem conferência · (4) Está ligada em tudo e é conferida periodicamente

**Ajuda:** As atualizações corrigem falhas que os criminosos já conhecem e exploram. Equipamentos e programas muito antigos, que não recebem mais atualizações (como Windows sem suporte), ficam permanentemente expostos.

**Recomendação:** Ligue as atualizações automáticas em tudo e troque equipamentos e programas que não recebem mais atualizações do fabricante.

`CSF PR.PS-02` · `ISO 27002 8.8` · porte ≥ 1 · setores: todos · pesos: RAN 3, VAZ 2, IND 1

### PR-17 — Todos os computadores têm antivírus ligado e atualizado?

**Respostas:** (0) Não há antivírus · (1) Há antivírus, mas ninguém confere se está ligado e atualizado · (2) Há só em parte dos computadores, ou nem sempre atualizado · (3) Há em todos, ligado e atualizado, sem conferência · (4) Há em todos, e isso é conferido periodicamente

**Ajuda:** O antivírus bloqueia a maior parte dos programas maliciosos conhecidos. O Windows já traz o Microsoft Defender, que só precisa estar ligado. Versões para empresas também avisam um responsável quando detectam algo.

**Recomendação:** Garanta antivírus ligado e atualizado em todos os computadores, com os avisos indo para o responsável pela segurança (em empresas maiores, considere uma solução do tipo EDR).

`CSF PR.PS-05` · `ISO 27002 8.7` · porte ≥ 1 · setores: todos · pesos: RAN 3, VAZ 1

**Variante (portes 1; até 1 usuário(s)):**

- recomendacao: Mantenha o antivírus ligado e atualizado no computador. O Microsoft Defender, que já vem no Windows, é suficiente para começar.

### PR-18 — Quando um equipamento ou sistema novo é instalado, as senhas de fábrica são trocadas e as funções que não serão usadas são desligadas?

**Respostas:** (0) Não trocamos nem desligamos nada · (1) Fazemos às vezes · (2) Fazemos só uma das duas coisas: trocar as senhas ou desligar o que não é usado · (3) Fazemos as duas coisas sempre, sem roteiro escrito · (4) Fazemos as duas coisas sempre, seguindo um roteiro escrito

**Ajuda:** Roteadores, câmeras e sistemas muitas vezes vêm com senhas padrão (como "admin/admin"), que estão publicadas na internet. Trocá-las e desligar o que não é usado fecha portas fáceis para um criminoso.

**Recomendação:** Crie um roteiro curto de instalação segura e siga-o sempre que entrar um equipamento ou sistema novo (computador, roteador, câmera, impressora, sistema online): (1) trocar a senha de fábrica por uma senha forte, guardada no gerenciador de senhas; (2) instalar as atualizações antes de colocar em uso; (3) desligar funções e contas que não serão usadas, como acesso remoto e usuário convidado; (4) ativar a verificação em duas etapas quando existir; (5) registrar o item no inventário. Peça ao técnico ou fornecedor que fizer a instalação para seguir o roteiro e confirmar por escrito.

`CSF PR.PS-01` · `ISO 27002 8.9` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, IND 1

### PR-19 — O e-mail da empresa tem filtro que bloqueia spam, anexos perigosos e links falsos antes de chegarem às pessoas?

**Respostas:** (0) Não há filtro · (1) Há só o filtro padrão do provedor, sem ajuste · (2) Há filtro só para spam, ou só em algumas contas · (3) Há filtro completo em todas as contas, sem acompanhamento · (4) Há filtro completo, acompanhado e ajustado periodicamente

**Ajuda:** Um bom filtro de e-mail barra a maioria das mensagens de golpe antes que alguém precise decidir se clica ou não. Os serviços de e-mail para empresas já têm esse filtro; às vezes só é preciso ativar as opções avançadas.

**Recomendação:** Peça ao seu provedor de e-mail ou a um técnico de TI de confiança para: (1) ligar o filtro que analisa anexos e links antes de chegarem às pessoas (pode exigir um plano pago do Google Workspace ou do Microsoft 365); e (2) configurar no domínio da empresa a proteção que impede golpistas de enviar e-mails como se fossem vocês (para o técnico: SPF, DKIM e DMARC). Se ninguém na empresa cuida disso, contrate algumas horas de um técnico: é um serviço rápido e de baixo custo.

`CSF PR.IR-01` · `ISO 27002 8.23` · porte ≥ 2 · setores: todos · pesos: FRA 2, RAN 2

### PR-20 — O roteador ou firewall da empresa está bem configurado, e o Wi-Fi dos visitantes é separado do Wi-Fi interno?

**Respostas:** (0) O roteador está como veio, com uma rede só · (1) Ajustamos algo na instalação e nunca mais · (2) Fizemos só uma das duas coisas: configurar bem ou separar o Wi-Fi · (3) Está bem configurado e com Wi-Fi separado, sem registro · (4) Está bem configurado, separado, e isso é revisado periodicamente

**Ajuda:** O firewall funciona como um porteiro entre a internet e a rede da empresa. Uma rede Wi-Fi de visitantes separada evita que o celular de um cliente, que pode estar infectado, enxergue os computadores e arquivos da empresa.

**Recomendação:** Peça a um técnico para revisar o roteador/firewall e criar uma rede Wi-Fi de visitantes separada da rede interna.

`CSF PR.IR-01` · `ISO 27002 8.20` · porte ≥ 3 · setores: todos · pesos: RAN 2, VAZ 1, IND 1

### PR-21 — Os sistemas mais importantes têm um 'estepe', por exemplo uma internet reserva ou um serviço que assume se o principal cair?

**Respostas:** (0) Não há reserva · (1) Há uma solução improvisada, como o 4G de um celular · (2) Só parte dos sistemas importantes tem reserva · (3) Todos os sistemas importantes têm reserva, mas a troca não é testada · (4) Todos têm reserva, e a troca é testada pelo menos uma vez por ano

**Ajuda:** Essa redundância evita que uma queda de internet ou de servidor pare a empresa. Uma segunda conexão de outra operadora (até mesmo 4G/5G) costuma ser barata perto do custo de horas sem vender ou atender.

**Recomendação:** Use a lista de atividades essenciais e o prazo que cada uma aguenta ficar parada, definidos no plano de recuperação, para decidir onde vale ter reserva. Para os servidores e sistemas que não podem parar, contrate um segundo link de internet dedicado de fibra, de outra operadora e com cabeamento e central diferentes do principal, com garantia de disponibilidade em contrato de pelo menos 99,5% ao mês, configurado para assumir automaticamente quando o principal cair. Um 4G/5G serve apenas como contingência mínima para tarefas leves. Para os sistemas que param a operação, peça a um especialista que avalie uma alternativa pronta para assumir, por exemplo uma cópia em nuvem, e compare o custo dela com o prejuízo da parada. Teste a troca para a reserva pelo menos uma vez por ano.

`CSF PR.IR-03` · `ISO 27002 8.14` · porte ≥ 4 · setores: todos · pesos: IND 3

### SAU-01 — No sistema de prontuário ou de agenda, cada profissional entra com seu próprio login, e o sistema registra quem acessou cada prontuário?

**Respostas:** (0) O login é compartilhado · (1) Cada um tem login, mas às vezes compartilhamos · (2) Há login individual, mas o sistema não registra os acessos · (3) Há login individual e registro dos acessos, sem conferência · (4) Há login individual, registro dos acessos e conferência periódica

**Ajuda:** Dados de saúde são dados sensíveis pela LGPD, e o vazamento é mais grave. Login individual e registro de quem acessou permitem descobrir abusos e são exigidos pelo Conselho Federal de Medicina no prontuário eletrônico.

**Recomendação:** Use um sistema de prontuário com login individual e registro de acessos (o CFM exige isso no prontuário eletrônico, conforme a Res. CFM nº 1.821/2007).

`CSF PR.AA-05` · `ISO 27002 5.15` · porte ≥ 1 · setores: saude · pesos: VAZ 3

### SAU-02 — Os equipamentos de saúde ligados à rede (raio-x, laboratório, monitores) ficam em uma rede separada dos computadores da recepção e do administrativo?

**Respostas:** (0) Está tudo na mesma rede · (1) Separamos algum equipamento, sem critério · (2) Só parte dos equipamentos está em rede separada · (3) Todos estão em rede separada, sem registro da configuração · (4) Todos estão em rede separada, com a configuração registrada e revisada

**Ajuda:** Equipamentos médicos costumam usar programas antigos que não podem ser atualizados. Mantê-los em redes separadas impede que um vírus que entrou por um e-mail da recepção chegue até eles e pare os atendimentos.

**Recomendação:** Coloque os equipamentos de saúde conectados em uma rede separada da rede administrativa.

`CSF PR.IR-01` · `ISO 27002 8.22` · porte ≥ 3 · setores: saude · pesos: RAN 2, IND 2

### VAR-02 — A loja virtual está em uma plataforma atualizada e tem proteção contra ataques que tentam derrubar ou invadir o site?

**Respostas:** (0) A plataforma está desatualizada e sem proteção · (1) Atualizamos só quando a plataforma obriga · (2) Está atualizada, mas sem proteção contra ataques, ou o contrário · (3) Está atualizada e protegida, sem acompanhamento · (4) Está atualizada, protegida e acompanhada periodicamente

**Ajuda:** Lojas virtuais são alvo de robôs que testam falhas conhecidas e de ataques de sobrecarga que tiram o site do ar em datas de muita venda. Muitas plataformas já incluem essa proteção; em sites próprios, ela precisa ser contratada.

**Recomendação:** Mantenha a plataforma da loja virtual atualizada (ou use uma plataforma pronta, que faz isso por você) e ative um serviço de proteção do site, que filtra acessos maliciosos e segura picos de visitas para o site não cair. Vários têm plano gratuito; peça ajuda a quem cuida do site (para o técnico: CDN/WAF).

`CSF PR.IR-01` · `ISO 27002 8.20` · porte ≥ 2 · setores: varejo · pesos: IND 2, VAZ 2

### IND-01 — Os computadores e controladores que comandam as máquinas ficam em uma rede separada da rede do escritório e sem acesso direto pela internet?

**Respostas:** (0) Está tudo na mesma rede · (1) Separamos alguma máquina, sem critério · (2) Só parte está separada, ou ainda há acesso direto pela internet · (3) Tudo separado e sem acesso direto, mas sem registro da configuração · (4) Tudo separado e sem acesso direto, com a configuração registrada e revisada

**Ajuda:** Se a rede de automação industrial está ligada à rede do escritório, um vírus que chega por e-mail pode alcançar as máquinas e parar a produção. Separar as redes funciona como uma porta corta-fogo.

**Recomendação:** Separe a rede das máquinas (automação, CLP, supervisório) da rede do escritório e da internet.

`CSF PR.IR-01` · `ISO 27002 8.22` · porte ≥ 2 · setores: industria · pesos: RAN 3, IND 2

### IND-03 — O computador ligado às máquinas (por exemplo, o que envia os projetos para a CNC) é usado só para a produção, sem navegar na internet, abrir e-mail ou receber pendrive de terceiros?

**Respostas:** (0) Esse computador é usado para tudo · (1) Evitamos usar para outras coisas, mas acontece · (2) É quase só para a produção, com exceções como e-mail ou pendrive · (3) É usado só para a produção, sem regra escrita · (4) É usado só para a produção, com regra escrita e conferida

**Ajuda:** Esses computadores costumam ter sistemas antigos, que não recebem mais atualizações. Um vírus que chega por um pendrive ou por um e-mail aberto nele pode travar as máquinas e parar a produção.

**Recomendação:** Use o computador das máquinas só para a produção. Leve os projetos até ele por um meio controlado (uma pasta na nuvem da empresa ou um pendrive usado só para isso e verificado pelo antivírus) e mantenha uma cópia dos projetos e das configurações das máquinas no backup.

`CSF PR.PS-01` · `ISO 27002 8.1` · porte ≥ 1 · setores: industria · pesos: RAN 3, IND 2

### TEC-01 — O software que vocês desenvolvem passa por uma revisão de segurança antes de ser entregue aos clientes?

**Respostas:** (0) Não há revisão de segurança · (1) Revisamos só quando um cliente pede · (2) Revisamos só parte das entregas · (3) Revisamos todas, sem roteiro escrito · (4) Revisamos todas, com roteiro escrito e registro

**Ajuda:** Uma falha no seu software pode expor os dados dos seus clientes, e a responsabilidade volta para você. A revisão de segurança combina uma segunda leitura do código (por um colega ou, para quem trabalha sozinho, pelo cliente ou por uma ferramenta de IA para empresas) com ferramentas automáticas que procuram falhas conhecidas.

**Recomendação:** Antes de cada entrega, faça uma revisão de segurança do código: com outra pessoa da equipe ou, se você trabalha sozinho, com o cliente ou com uma ferramenta de IA em versão para empresas (que não usa seu código para treinamento). Use também ferramentas automáticas gratuitas que procuram falhas conhecidas no código e nas bibliotecas usadas.

`CSF PR.PS-06` · `ISO 27002 8.28` · porte ≥ 1 · setores: tecnologia · pesos: VAZ 2, TER 2

### TEC-02 — As senhas e acessos que vocês têm aos sistemas dos clientes ficam em um cofre de senhas, com verificação em duas etapas, e são revisados de tempos em tempos?

**Respostas:** (0) Ficam em planilhas, e-mails ou anotações · (1) Parte fica em cofre, sem padrão · (2) Ficam em cofre, mas sem verificação em duas etapas ou sem revisão · (3) Ficam em cofre, com verificação em duas etapas e revisão, sem regra escrita · (4) Ficam em cofre protegido, com regra escrita e revisão periódica

**Ajuda:** Empresas de tecnologia costumam ter as "chaves" de vários clientes. Um único ataque à sua empresa pode alcançar todos eles, o que transforma um incidente seu em vários incidentes dos clientes.

**Recomendação:** Guarde os acessos dos clientes em um cofre de senhas com verificação em duas etapas e revise a cada três meses quem tem acesso a cada cliente.

`CSF PR.AA-05` · `ISO 27002 8.2` · porte ≥ 2 · setores: tecnologia · pesos: TER 3, VAZ 2

### SER-01 — Os documentos dos clientes (contratos, processos, declarações) ficam em um local com acesso restrito, e não espalhados em e-mails e pastas pessoais?

**Respostas:** (0) Ficam espalhados em e-mails e pastas pessoais · (1) Organizamos às vezes, quando alguém lembra · (2) Só parte dos documentos fica em local restrito · (3) Todos ficam em local restrito, sem regra escrita · (4) Todos ficam em local restrito, com regra escrita e revisão dos acessos

**Ajuda:** Escritórios guardam documentos muito sensíveis dos clientes. Quando eles estão espalhados no e-mail e no computador de cada um, é difícil controlar quem vê e impossível garantir o backup.

**Recomendação:** Centralize os documentos de clientes em um repositório da empresa, com acesso restrito por cliente ou equipe.

`CSF PR.DS-01` · `ISO 27002 5.15` · porte ≥ 1 · setores: servicos · pesos: VAZ 2, IA 1

### SER-02 — A empresa avisa os clientes de como costuma cobrar e pedir dados, por exemplo que nunca muda a conta bancária por e-mail?

**Respostas:** (0) Não avisamos · (1) Avisamos só quando algum cliente pergunta · (2) Avisamos só parte dos clientes · (3) Avisamos todos, sem um texto padrão · (4) Avisamos todos, com texto padrão em contratos, boletos ou site

**Ajuda:** Golpistas também se passam pela sua empresa para enganar seus clientes com boletos falsos. Avisar os clientes sobre os canais oficiais protege os dois lados e a reputação da empresa.

**Recomendação:** Informe aos clientes, por escrito, quais são os canais oficiais de cobrança e que dados bancários nunca mudam por e-mail ou mensagem.

`CSF PR.AT-01` · `ISO 27002 5.14` · porte ≥ 2 · setores: servicos · pesos: FRA 2


## Perceber quando algo dá errado (DE)

_Formas de notar rapidamente um ataque ou um comportamento estranho._

### DE-01 — Alguém recebe e trata os alertas de segurança (do antivírus, de login suspeito, do banco ou da nuvem), começando pelos mais graves?

**Respostas:** (0) Ninguém olha os alertas · (1) Alguém olha quando dá tempo · (2) Alguém acompanha só parte dos alertas · (3) Alguém acompanha todos, mas sem critério escrito de prioridade · (4) Alguém acompanha todos, com prioridades e prazos escritos

**Ajuda:** Muitos ataques dão sinais antes do estrago: um aviso de login de outro país, um antivírus que detectou algo, um alerta do banco. Se esses avisos vão para um e-mail que ninguém lê, o problema só é descoberto tarde demais.

**Recomendação:** Com um especialista, classifique os alertas de segurança pela gravidade para o negócio (por exemplo, crítico: vírus ativo, acesso suspeito à conta do banco ou ao e-mail dos sócios, aviso de vazamento; depois alto, médio e baixo) e defina um prazo de atendimento para cada nível (por exemplo: crítico em até 1 hora, alto no mesmo dia, médio em até uma semana). Direcione os alertas do antivírus, do e-mail, da nuvem e do banco para o responsável pela segurança e registre essas regras na política de segurança. Assim a equipe atende primeiro o que importa, sem ficar sobrecarregada.

`CSF DE.CM-09` · `ISO 27002 8.16` · porte ≥ 3 · setores: todos · pesos: RAN 2, VAZ 2, FRA 1

### DE-02 — Os registros de quem acessou os sistemas importantes (logs) ficam guardados por pelo menos 6 meses?

**Respostas:** (0) Não guardamos registros · (1) Os registros ficam só pelo prazo padrão de cada sistema · (2) Guardamos por 6 meses só os de parte dos sistemas · (3) Guardamos por 6 meses os de todos os sistemas importantes, sem conferência · (4) Guardamos por 6 meses ou mais, com conferência periódica

**Ajuda:** Os logs são o histórico de quem entrou, quando e de onde. Sem eles, depois de um incidente é impossível saber o que foi acessado, e isso importa inclusive para cumprir a LGPD.

**Recomendação:** Ative e guarde por pelo menos 6 meses os registros de acesso (quem entrou, quando e de onde) do e-mail, da nuvem e dos sistemas importantes. Muitos serviços guardam esses registros por pouco tempo no plano básico: confira o prazo e, se for menor, peça ao técnico para copiá-los automaticamente para um local protegido, que só o responsável pela segurança acesse. Esses registros são o que permite descobrir o que aconteceu em um incidente. Se a empresa oferece site ou aplicativo com fins comerciais, guardar os registros de acesso por 6 meses é obrigação do Marco Civil da Internet (Lei nº 12.965/2014, art. 15). Esta é uma orientação geral, não um parecer jurídico: para confirmar as obrigações da sua empresa, consulte um advogado.

`CSF DE.CM-01` · `ISO 27002 8.15` · porte ≥ 4 · setores: todos · pesos: VAZ 1, TER 1

### DE-03 — A empresa conta com monitoramento de segurança 24 horas, feito por uma ferramenta ou por uma empresa especializada?

**Respostas:** (0) Não há monitoramento · (1) Há alertas, mas ninguém acompanha fora do horário comercial · (2) Há monitoramento só de parte dos sistemas · (3) Há monitoramento 24 horas, sem regras escritas de atendimento · (4) Há monitoramento 24 horas, com regras e prazos de atendimento em contrato

**Ajuda:** Ataques de sequestro de dados costumam acontecer de madrugada ou no fim de semana, justamente quando ninguém está olhando. Um serviço de monitoramento contínuo percebe e reage nesses horários.

**Recomendação:** Contrate um serviço de monitoramento de segurança 24 horas (para o técnico: MDR ou SOC gerenciado). Nele, uma equipe especializada recebe dia e noite os alertas dos computadores, do e-mail e da nuvem e age para conter um ataque, por exemplo isolando um computador infectado de madrugada. No contrato, exija: (1) o que será monitorado; (2) o que a empresa contratada pode fazer sozinha e o que precisa da sua autorização; (3) prazo de resposta para cada nível de gravidade, seguindo a classificação de alertas da sua política de segurança; (4) quem será avisado e por qual canal; (5) um relatório mensal com os alertas e o que foi feito. Compare propostas de pelo menos três fornecedores.

`CSF DE.CM-01` · `ISO 27002 8.16` · porte ≥ 4 · setores: todos · pesos: RAN 2, VAZ 2

### DE-04 — A empresa acompanha quais ferramentas de Inteligência Artificial as pessoas estão usando no trabalho e com que tipo de informação?

**Respostas:** (0) Não acompanhamos · (1) Sabemos de alguns casos, por acaso · (2) Acompanhamos só algumas áreas ou ferramentas · (3) Acompanhamos todas as áreas, sem registro · (4) Há um registro das ferramentas em uso, revisado periodicamente

**Ajuda:** É comum cada pessoa usar a IA que prefere, na conta pessoal, sem que a empresa saiba. Descobrir quais ferramentas estão em uso é o primeiro passo para oferecer uma opção segura.

**Recomendação:** Faça um levantamento das ferramentas de IA em uso: pergunte à equipe, de forma aberta e sem punição, quais usam e para quê, e peça ao técnico para verificar os sites acessados e as extensões instaladas nos navegadores. Com base nisso, escolha uma ou mais ferramentas aprovadas, de preferência versões para empresas, que não usam os dados para treinamento, e registre na política de segurança o que pode e o que nunca pode ser colocado nelas. Ofereça a alternativa aprovada no lugar das não autorizadas e repita o levantamento a cada seis meses, porque novas ferramentas surgem o tempo todo.

`CSF DE.CM-03` · `ISO 27002 8.12` · porte ≥ 4 · setores: todos · pesos: IA 3

### DE-05 — O e-mail ou a nuvem da empresa bloqueia ou avisa quando alguém tenta enviar para fora informações sensíveis, como listas de clientes?

**Respostas:** (0) Não há bloqueio nem aviso · (1) Há algum bloqueio pontual, configurado há muito tempo · (2) Há bloqueio ou aviso só para alguns tipos de informação · (3) Há bloqueio ou aviso para as informações sensíveis, sem acompanhamento · (4) Há bloqueio ou aviso, com acompanhamento e ajuste periódicos

**Ajuda:** É uma prevenção de vazamento de dados: regras que detectam, por exemplo, um arquivo com centenas de CPFs sendo enviado a um endereço externo e pedem confirmação ou bloqueiam o envio.

**Recomendação:** Ative regras que avisam ou bloqueiam quando alguém tenta enviar para fora da empresa informações sensíveis, como CPFs, números de cartão, dados de saúde ou listas de clientes (para o técnico: DLP). Esse recurso costuma fazer parte dos planos mais completos do Microsoft 365 ou do Google Workspace, então confira o custo antes. Defina primeiro, na política de segurança, quais informações são sigilosas. Depois, deixe as regras só avisando por um mês, para ajustá-las sem atrapalhar o trabalho, e então passe a bloquear os casos mais graves.

`CSF DE.CM-03` · `ISO 27002 8.12` · porte ≥ 4 · setores: todos · pesos: VAZ 2, IA 2


## Reagir a um problema (RS)

_O que a empresa faz nas primeiras horas de um incidente._

### RS-01 — Existe um plano simples do que fazer e de quem chamar se acontecer um ataque, e as pessoas o conhecem?

**Respostas:** (0) Não há plano · (1) Cada um sabe um pouco, mas nada está combinado · (2) Há um plano, mas só algumas pessoas o conhecem · (3) Há um plano que todos conhecem, mas não está escrito · (4) Há um plano escrito, que todos conhecem e é revisado

**Ajuda:** Um plano de resposta pode caber em uma folha: quem avisar, o que desligar primeiro, telefone do técnico, do banco e do advogado. Nas primeiras horas de um incidente, cada minuto de indecisão aumenta o prejuízo.

**Recomendação:** Escreva um plano de resposta de uma página: quem avisar, o que desligar primeiro e quem chamar. Guarde-o em uma pasta compartilhada da empresa e mantenha uma cópia fora dos sistemas da empresa, com o dono ou sócio responsável ou em um celular da empresa, porque se um vírus travar os computadores a pasta pode ficar fora do ar. Divulgue para a equipe um número de emergência do responsável (dono, sócio ou técnico de TI contratado). Se a equipe trabalha presencialmente, deixe também uma cópia impressa.

`CSF RS.MA-01` · `ISO 27002 5.24` · porte ≥ 1 · setores: todos · pesos: RAN 2, VAZ 2, FRA 1, IND 1, TER 1

**Variante (portes 1):**

- texto: Existe um roteiro do que fazer primeiro em caso de ataque ou golpe, com os contatos do banco, de um técnico de TI e da polícia à mão?
- ajuda: Nas primeiras horas de um ataque ou golpe, cada minuto conta. Em golpes com PIX, avisar o banco logo aumenta a chance de recuperar o dinheiro pelo MED (Mecanismo Especial de Devolução). Ter um plano curto e os contatos prontos, fora do computador que pode estar travado, evita perder tempo.
- recomendacao: Escreva um plano de uma página: o que desligar primeiro, quem chamar e os contatos de emergência (gerente do banco, técnico de TI, advogado, delegacia de crimes cibernéticos). Guarde-o na nuvem e mantenha uma cópia com você, fora dos computadores da empresa, para acessá-lo mesmo com tudo travado.
- respostas: (0) Não há roteiro · (1) Há uma ideia do que fazer, mas sem os contatos à mão · (2) Há só uma parte: os passos ou os contatos · (3) Os passos e os contatos são conhecidos, mas não estão anotados · (4) O roteiro e os contatos estão anotados e são revisados de tempos em tempos
- pesos: RAN 2, VAZ 2, FRA 2, IND 1, TER 1

### RS-02 — Existe um procedimento de quando e como avisar a ANPD e os clientes se dados pessoais vazarem?

**Respostas:** (0) Não há procedimento · (1) Procuraríamos saber na hora · (2) Sabemos só uma parte: quando avisar ou como avisar · (3) Há um procedimento conhecido, mas não escrito · (4) Há um procedimento escrito, com responsáveis e prazos

**Ajuda:** Pela LGPD, vazamentos que possam causar dano às pessoas precisam ser comunicados à ANPD (o órgão que fiscaliza a lei) e aos afetados em poucos dias úteis. Saber isso antes evita perder o prazo e ser multado por comunicação atrasada.

**Recomendação:** Inclua no plano de resposta o que fazer se dados pessoais vazarem. Avisar a ANPD e as pessoas afetadas é obrigatório quando o vazamento pode causar risco ou dano relevante, por exemplo se envolver dados sensíveis (saúde, biometria), dados financeiros, senhas, dados de crianças ou idosos ou dados de muitas pessoas. O prazo é de 3 dias úteis a partir do momento em que a empresa soube do vazamento (o dobro para microempresas e empresas de pequeno porte), pelo formulário no site da ANPD. Registre todos os incidentes, mesmo os que não precisaram ser comunicados, e guarde o registro por 5 anos (Resolução CD/ANPD nº 15/2024). Esta é uma orientação geral, não um parecer jurídico: para confirmar as obrigações da sua empresa, consulte um advogado especializado em proteção de dados.

`CSF RS.CO-03` · `ISO 27002 5.34` · porte ≥ 3 · setores: todos · pesos: VAZ 2

### RS-03 — Vocês têm à mão os contatos do banco, de um técnico de TI e da polícia para acionar rapidamente em caso de golpe ou ataque?

**Respostas:** (0) Não temos esses contatos · (1) Procuraríamos os contatos na hora · (2) Temos só parte dos contatos · (3) Temos todos os contatos, mas só no celular de alguém · (4) Temos todos em um lugar conhecido por todos, revisados periodicamente

**Ajuda:** Em golpes com PIX, avisar o banco nas primeiras horas aumenta muito a chance de recuperar o dinheiro pelo MED (Mecanismo Especial de Devolução). Ter os contatos prontos, fora do computador que pode estar travado, economiza tempo precioso.

**Recomendação:** Mantenha a lista de contatos de emergência (gerente do banco, técnico de TI, advogado, delegacia de crimes cibernéticos) junto ao plano de resposta, com uma cópia fora dos sistemas da empresa, para acessá-la mesmo com os computadores travados.

`CSF RS.MA-01` · `ISO 27002 5.24` · porte ≥ 2 · setores: todos · pesos: FRA 2, RAN 1

### RS-04 — A equipe faz, pelo menos uma vez por ano, uma simulação de ataque para treinar o plano de resposta?

**Respostas:** (0) Nunca fizemos · (1) Fizemos uma vez · (2) Fazemos às vezes, sem frequência definida · (3) Fazemos todo ano, sem registrar o que aprendemos · (4) Fazemos todo ano e registramos as melhorias no plano

**Ajuda:** Uma simulação pode ser só uma reunião de uma hora: "e se hoje os computadores amanhecessem trancados?". Ela mostra falhas do plano (telefone desatualizado, ninguém sabe onde está o backup) enquanto ainda há tempo de corrigir.

**Recomendação:** Uma vez por ano, faça um exercício em reunião: alguém apresenta uma situação fictícia, por exemplo 'os computadores amanheceram travados com um pedido de resgate' ou 'um cliente avisou que os dados dele apareceram na internet', e a equipe diz, passo a passo, o que faria seguindo o plano de resposta. Participam a direção, o responsável pela segurança, o técnico ou a empresa de TI e, se possível, quem cuida do jurídico e da comunicação. Anote o que travou (contato desatualizado, backup que ninguém sabia recuperar, dúvida sobre avisar a ANPD) e corrija o plano em até um mês. Um especialista pode preparar e conduzir o exercício.

`CSF RS.MA-01` · `ISO 27002 5.24` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, IND 1


## Voltar a funcionar (RC)

_Como a empresa retoma a operação depois de um problema._

### RC-01 — Está definido por quanto tempo cada atividade essencial pode ficar parada, e existe um plano para religar os sistemas dentro desse prazo?

**Respostas:** (0) Nada disso está definido · (1) Temos uma ideia, mas nada combinado · (2) Está definido só para parte das atividades, ou há prazo sem plano · (3) Está definido para todas as atividades essenciais, mas não está escrito · (4) Está escrito, com prazos e plano, e é testado periodicamente

**Ajuda:** Algumas empresas aguentam um dia parado; outras perdem clientes em uma hora. Saber por quanto tempo cada atividade essencial pode ficar parada ajuda a decidir quanto investir em backup, em reserva e em contingência.

**Recomendação:** Para cada atividade essencial da sua lista de contingência, defina por quanto tempo ela pode ficar parada sem prejuízo grave (algumas horas? dois dias?). Depois monte um plano de recuperação que caiba nesse prazo: em que ordem os sistemas voltam, quem faz cada passo, onde estão os backups e os acessos necessários e qual técnico ou empresa chamar se a equipe não der conta. Teste o plano uma vez por ano, simulando uma parada.

`CSF RC.RP-01` · `ISO 27002 5.30` · porte ≥ 2 · setores: todos · pesos: RAN 2, IND 3

### RC-02 — Existe um jeito de continuar atendendo os clientes se os sistemas pararem, por exemplo um processo em papel ou um sistema reserva?

**Respostas:** (0) Não: se os sistemas param, a empresa para · (1) Damos um jeito na hora, sem nada combinado · (2) Há alternativa só para parte das atividades · (3) Há alternativa para todas as atividades essenciais, mas não está escrita · (4) Há alternativa escrita para as atividades essenciais, e ela é testada

**Ajuda:** Um plano de contingência simples (pedidos anotados em formulário, uma cópia da agenda guardada fora do sistema) permite continuar funcionando, mesmo que mais devagar, enquanto os sistemas são recuperados. Isso reduz a perda com a parada.

**Recomendação:** Liste as atividades sem as quais a empresa para (por exemplo: vender, atender clientes, receber pagamentos, entregar). Para cada uma, defina um jeito de continuar sem os sistemas, mesmo que mais devagar: anotar pedidos em um formulário, receber pela maquininha, atender por telefone, consultar uma cópia da agenda guardada fora do sistema. Combine com a equipe quando usar esse modo e como lançar no sistema, depois, o que foi feito durante a parada.

`CSF RC.RP-02` · `ISO 27002 5.30` · porte ≥ 1 · setores: todos · pesos: IND 2, RAN 1

