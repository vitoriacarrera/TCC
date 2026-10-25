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

**Ajuda:** Pode ser alguém da empresa ou uma empresa de TI contratada, e não precisa ser especialista nem ter dedicação exclusiva. O importante é existir alguém que lembre das tarefas (atualizar, conferir o backup, tirar acessos de quem saiu) e que todos saibam a quem recorrer. Quando é "responsabilidade de todos", na prática fica sem dono.

**Recomendação:** Escolha uma pessoa como responsável pela segurança digital e reserve algumas horas por mês para essa função. Se contratar uma empresa de TI, deixe no contrato o que ela faz em segurança (por exemplo: backup, atualizações, antivírus e atendimento a incidentes) e mantenha alguém da empresa como ponto de contato.

`CSF GV.RR-02` · `ISO 27002 5.2` · porte ≥ 2 · setores: todos · pesos: RAN 1, VAZ 1, FRA 1, IND 1, TER 1, IA 1

### GV-02 — A empresa tem regras escritas sobre como usar senhas, e-mail, computadores e dados, e as pessoas conhecem essas regras?

**Ajuda:** Uma política de segurança pode ter poucas páginas, com regras como "não compartilhe senhas", "não use pendrive pessoal" e "desconfie de pedidos urgentes de pagamento". Regras combinadas por escrito evitam que cada um faça de um jeito e mostram a todos o que fazer quando algo der errado.

**Recomendação:** Escreva uma política de segurança curta, apresente à equipe, peça que todos assinem que leram e revise uma vez por ano. Ela deve cobrir, no mínimo: (1) quem é o responsável pela segurança e o papel de cada um; (2) quais informações são sigilosas e quem pode vê-las; (3) regras de acesso: um usuário por pessoa, só o necessário para a função, revisão a cada três meses e retirada no desligamento; (4) senhas e verificação em duas etapas; (5) uso de e-mail, internet, celular ou computador pessoal e ferramentas de IA; (6) cuidados com os equipamentos: atualizações, antivírus, bloqueio de tela; (7) backup: frequência, cópia separada e testes; (8) cuidados com fornecedores; (9) como avisar um problema, como os alertas são classificados por gravidade e em quanto tempo cada um é atendido; (10) treinamento anual. Esta lista não é uma exigência legal: ela segue normas internacionais de segurança da informação e serve como referência de boa prática.

`CSF GV.PO-01` · `ISO 27002 5.1` · porte ≥ 3 · setores: todos · pesos: RAN 1, VAZ 1, FRA 1, IA 1

### GV-03 — Antes de contratar um fornecedor que vai guardar seus dados ou acessar seus sistemas, vocês verificam se ele se protege bem e colocam isso no contrato?

**Ajuda:** Contador, empresa de TI, sistema de gestão online e agência de marketing costumam ter acesso a informações importantes. Se o fornecedor sofre um ataque, a sua empresa também é atingida. Perguntar se ele faz backup e usa verificação em duas etapas, e incluir cláusula de sigilo e de aviso em caso de incidente, já reduz muito esse risco.

**Recomendação:** Faça uma lista dos fornecedores que acessam seus dados e inclua nos contratos cláusulas de segurança, sigilo e obrigação de avisar sobre incidentes.

`CSF GV.SC-05` · `ISO 27002 5.19` · porte ≥ 2 · setores: todos · pesos: TER 3, VAZ 1

### GV-04 — A empresa sabe o que a LGPD exige dela, por exemplo informar aos clientes como usa os dados deles?

**Ajuda:** A LGPD (Lei Geral de Proteção de Dados) vale para empresas de todos os tamanhos que guardam dados de pessoas. Microempresas e empresas de pequeno porte têm regras mais simples, mas todas continuam responsáveis por proteger esses dados e podem ser multadas se houver vazamento por descuido.

**Recomendação:** Faça um diagnóstico simples do que a LGPD exige da empresa e publique um aviso de privacidade explicando quais dados vocês coletam, para quê e com quem compartilham. Microempresas e empresas de pequeno porte têm regras simplificadas (Resolução CD/ANPD nº 2/2022): não precisam indicar um encarregado de dados, mas precisam manter um canal para os clientes tirarem dúvidas e pedirem acesso ou exclusão dos seus dados, e têm prazo em dobro para responder. Atenção: essas facilidades não valem se a empresa trata dados de muitas pessoas e esses dados forem sensíveis (como saúde ou biometria) ou de crianças e idosos; nesse caso, siga as regras completas. Esta é uma orientação geral, não um parecer jurídico: para confirmar as obrigações da sua empresa, consulte um advogado especializado em proteção de dados.

`CSF GV.OC-03` · `ISO 27002 5.34` · porte ≥ 2 · setores: todos · pesos: VAZ 2, IA 1

**Variante (portes 4):**

- recomendacao: Faça um diagnóstico do que a LGPD exige da empresa, publique um aviso de privacidade e indique um encarregado de dados (uma pessoa da empresa ou um serviço contratado), divulgando o contato dele no site. Médias empresas não têm as regras simplificadas para pequenos negócios. Esta é uma orientação geral, não um parecer jurídico: para confirmar as obrigações da sua empresa, consulte um advogado especializado em proteção de dados.

### GV-05 — Pelo menos uma vez por ano, a direção para para avaliar os riscos digitais e decidir quanto investir em segurança?

**Ajuda:** Segurança digital funciona melhor como decisão de gestão, com orçamento definido, do que como gasto de emergência depois de um problema. Esta própria análise é um exemplo do que pode ser revisto todo ano.

**Recomendação:** Uma vez por ano, reserve uma reunião da direção para olhar os riscos digitais. Leve o resultado desta ferramenta (mapa de riscos e plano de ação), os incidentes e alertas graves do ano, o andamento das ações do ano anterior e o que mudou na empresa (sistemas, fornecedores, unidades novas). Decidam quais riscos a empresa aceita e quais vai tratar, aprovem um orçamento de segurança para o ano e definam um responsável e um prazo para cada ação. Registre as decisões em ata. Como referência, o relatório mostra a perda anual estimada: investir mais do que cerca de um terço desse valor raramente compensa.

`CSF GV.RM-01` · `ISO 27002 5.1` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, FRA 1, IND 1, TER 1, IA 1

### GV-06 — Está combinado quais ferramentas de Inteligência Artificial (como ChatGPT ou Gemini) podem ser usadas no trabalho e que tipo de informação nunca deve ser colada nelas?

**Ajuda:** Essas ferramentas ajudam muito, mas tudo o que é colado nelas sai da empresa. Em versões gratuitas, o conteúdo pode ser guardado e usado pelo fornecedor. Colar um contrato, uma lista de clientes ou um prontuário pode virar um vazamento sem ninguém perceber.

**Recomendação:** Defina quais ferramentas de IA podem ser usadas (de preferência versões para empresas, que não usam seus dados para treinamento) e proíba colar dados de clientes ou documentos sigilosos nas demais.

`CSF GV.PO-01` · `ISO 27002 5.10` · porte ≥ 1 · setores: todos · pesos: IA 3

**Variante (portes 1; até 1 usuário(s)):**

- texto: Você já definiu quais ferramentas de Inteligência Artificial (como ChatGPT ou Gemini) usa no trabalho e que tipo de informação nunca cola nelas?
- recomendacao: Escolha as ferramentas de IA que vai usar (de preferência versões para empresas, que não usam seus dados para treinamento) e nunca cole nelas dados de clientes ou documentos sigilosos.

### GV-07 — Os serviços em nuvem que vocês usam (como Google Workspace, Microsoft 365 ou o sistema de gestão online) estão com as opções de segurança ativadas, e vocês sabem o que o fornecedor protege e o que é responsabilidade de vocês?

**Ajuda:** Na nuvem existe responsabilidade compartilhada: o fornecedor garante que o serviço funciona, mas quem controla senhas, permissões e quem acessa o quê é a sua empresa. Muitos recursos de segurança já estão incluídos no plano, só não vêm ligados.

**Recomendação:** Peça a quem administra o Google Workspace, o Microsoft 365 e o sistema de gestão online para seguir a lista de segurança recomendada por cada fornecedor (Google e Microsoft publicam guias e mostram uma nota de segurança no painel de administração). No mínimo, confira: verificação em duas etapas obrigatória para todos; poucas contas de administrador, separadas das de uso diário; compartilhamento de arquivos com pessoas de fora limitado; alertas de login suspeito ligados; e por quanto tempo o fornecedor guarda arquivos apagados. Leia no contrato o que o fornecedor protege e o que fica com a empresa: em geral, ele cuida dos servidores e da estrutura, e a empresa cuida de quem acessa, das configurações e do backup dos próprios dados. Repita a conferência a cada seis meses.

`CSF GV.SC-07` · `ISO 27002 5.23` · porte ≥ 4 · setores: todos · pesos: TER 2, VAZ 1

### VAR-01 — Os pagamentos com cartão passam só por maquininha ou plataforma de pagamento certificada, sem que a empresa guarde números de cartão?

**Ajuda:** Guardar números de cartão (em planilha, caderno ou sistema próprio) torna a empresa responsável por protegê-los segundo regras rígidas das bandeiras. Maquininhas e plataformas certificadas cuidam disso por você.

**Recomendação:** Use apenas maquininhas e plataformas de pagamento certificadas (padrão PCI DSS) e nunca guarde números de cartão.

`CSF GV.OC-03` · `ISO 27002 5.31` · porte ≥ 1 · setores: varejo · pesos: VAZ 3

### IND-02 — O acesso remoto de técnicos e fornecedores às máquinas é liberado só quando necessário e com usuário individual?

**Ajuda:** Programas de acesso remoto deixados sempre ligados, com senha compartilhada entre técnicos, são uma porta de entrada conhecida para ataques a fábricas.

**Recomendação:** Libere o acesso remoto de fornecedores só no momento do atendimento, com usuário próprio para cada técnico, e desligue-o em seguida.

`CSF GV.SC-05` · `ISO 27002 5.19` · porte ≥ 3 · setores: industria · pesos: TER 2, RAN 2


## Conhecer o que proteger (ID)

_Saber quais equipamentos, sistemas e dados a empresa tem e onde estão._

### ID-01 — Vocês têm uma lista atualizada dos computadores, celulares e sistemas que a empresa usa?

**Ajuda:** É um inventário simples, que pode ser uma planilha: qual equipamento, quem usa, qual sistema, quem é o responsável. Sem ele, um notebook antigo esquecido ou um sistema que ninguém atualiza vira a porta de entrada de um ataque.

**Recomendação:** Monte um inventário dos equipamentos e sistemas da empresa. Ele pode ser uma aba da mesma planilha de acessos, para não ter vários controles separados. Para cada item, anote: o que é (notebook, celular, servidor, roteador, câmera, sistema online), quem usa ou é responsável, onde fica, se ainda recebe atualizações do fabricante e se guarda dados importantes. Inclua os celulares e computadores pessoais usados para trabalhar. Revise a cada seis meses e sempre que algo for comprado, trocado ou descartado: equipamento que não está na lista não é protegido nem entra no backup.

`CSF ID.AM-01` · `ISO 27002 5.9` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, IND 1

### ID-02 — Você sabe onde ficam guardadas as informações importantes da empresa (clientes, financeiro, projetos), ou seja, em quais computadores, nuvens ou sistemas?

**Ajuda:** Informação guardada em lugares sem controle (no computador de cada um, em pendrives, no WhatsApp, em e-mails pessoais) é difícil de proteger e fica fora do backup. Saber onde cada informação está é o que permite mantê-la só em locais seguros, com backup e acesso controlado.

**Recomendação:** Faça uma lista de onde ficam as informações importantes da empresa. Mantenha-as só em locais seguros e com backup: os sistemas da empresa (vendas, financeiro, agenda) e, para documentos e planilhas, uma pasta na nuvem da empresa em que cada pessoa acesse apenas o que precisa para o seu trabalho. Evite cópias soltas em pendrives, computadores pessoais e WhatsApp.

`CSF ID.AM-07` · `ISO 27002 5.9` · porte ≥ 1 · setores: todos · pesos: VAZ 2, RAN 1, TER 1, IA 1

### ID-03 — De tempos em tempos, alguém verifica se o site e os sistemas acessíveis pela internet têm falhas de segurança conhecidas?

**Ajuda:** Criminosos usam programas que varrem a internet o tempo todo procurando sites e sistemas com falhas de segurança conhecidas. Fazer essa mesma verificação antes deles (há serviços e ferramentas para isso) permite corrigir a falha antes que seja explorada.

**Recomendação:** Contrate um especialista para fazer, a cada três meses, uma varredura de vulnerabilidades externa. O que pedir: que ele verifique, de fora da empresa e sem invadir nada, o site, o e-mail, o acesso remoto e os demais sistemas acessíveis pela internet, procurando falhas já conhecidas. O que receber: um relatório com as falhas encontradas, ordenadas da mais grave para a menos grave, e o que fazer para corrigir cada uma. Depois das correções, peça uma nova verificação para confirmar. Esse serviço é diferente de um teste de invasão, que é mais caro e em geral não é necessário para empresas desse porte.

`CSF ID.RA-01` · `ISO 27002 8.8` · porte ≥ 3 · setores: todos · pesos: VAZ 2, RAN 2, IND 1


## Proteção no dia a dia (PR)

_Senhas, cópias de segurança, atualizações e cuidados que evitam problemas._

### PR-01 — Para entrar no e-mail, no banco, nas redes sociais e nos sistemas da empresa, além da senha é preciso confirmar pelo celular (verificação em duas etapas)?

**Ajuda:** Com a verificação em duas etapas, além da senha é pedido um código no celular ou um aplicativo. Mesmo que um golpista descubra a senha, ele não consegue entrar sem o seu celular. É uma das proteções mais eficazes e, na maioria dos serviços, é gratuita.

**Recomendação:** Ative a verificação em duas etapas no e-mail, no banco, nas redes sociais e nos sistemas, começando pelo e-mail e pelo banco. Em geral é gratuito e leva poucos minutos.

`CSF PR.AA-03` · `ISO 27002 8.5` · porte ≥ 1 · setores: todos · pesos: VAZ 3, FRA 3, RAN 2, TER 1

### PR-02 — Cada pessoa tem seu próprio usuário e senha, sem compartilhar o mesmo login com colegas?

**Ajuda:** Quando várias pessoas usam o mesmo login, não dá para saber quem fez o quê, a senha circula em bilhetes e mensagens, e fica difícil tirar o acesso de quem sai da empresa.

**Recomendação:** Crie um usuário para cada pessoa em todos os sistemas e acabe com os logins compartilhados.

`CSF PR.AA-01` · `ISO 27002 5.16` · porte ≥ 2 · setores: todos · pesos: VAZ 2, FRA 1, RAN 1

### PR-03 — As senhas são longas, diferentes para cada serviço e guardadas num gerenciador de senhas (e não em papel, planilha ou anotações do celular)?

**Ajuda:** Quando uma mesma senha é usada em vários lugares, basta um site vazar para o criminoso testar a mesma senha no seu e-mail e no seu banco. Um gerenciador de senhas cria e lembra senhas fortes por você.

**Recomendação:** Adote um gerenciador de senhas para a empresa e troque as senhas repetidas ou fáceis de adivinhar.

`CSF PR.AA-01` · `ISO 27002 5.17` · porte ≥ 1 · setores: todos · pesos: VAZ 2, RAN 1, FRA 1

### PR-04 — Quando alguém sai da empresa ou muda de função, os acessos dessa pessoa são retirados no mesmo dia?

**Ajuda:** Ex-funcionários com acesso ativo ao e-mail, à nuvem ou a grupos de WhatsApp da empresa são uma causa comum de vazamentos, por má-fé ou simplesmente porque a conta antiga é invadida depois.

**Recomendação:** Monte uma planilha simples com cada pessoa e os acessos que ela tem: e-mail, sistemas, nuvem, banco, grupos de mensagens e redes sociais da empresa. Use-a de dois jeitos: (1) quando alguém sair ou mudar de função, retire ou ajuste os acessos no mesmo dia, troque as senhas compartilhadas que a pessoa conhecia e recolha os equipamentos; (2) a cada três meses, revise a planilha com o responsável de cada área e remova os acessos que ninguém usa mais ou não precisa, inclusive de fornecedores e ex-estagiários.

`CSF PR.AA-05` · `ISO 27002 5.18` · porte ≥ 2 · setores: todos · pesos: VAZ 2, TER 1

### PR-05 — Cada pessoa acessa só os dados e sistemas de que realmente precisa para trabalhar?

**Ajuda:** Se todos acessam tudo, uma única conta invadida expõe a empresa inteira. Limitar o acesso por função (o estagiário não precisa ver a folha de pagamento) reduz o tamanho do estrago.

**Recomendação:** Defina, para cada função da empresa (por exemplo: vendas, financeiro, atendimento), quais pastas e sistemas ela precisa acessar. Registre esse padrão na planilha de acessos e, na revisão a cada três meses, compare o que cada pessoa tem com o padrão da função dela, retirando o que sobrar. Acessos fora do padrão só com aprovação do responsável pela área, anotada na planilha.

`CSF PR.AA-05` · `ISO 27002 5.15` · porte ≥ 3 · setores: todos · pesos: VAZ 2, IA 1

### PR-06 — As contas de administrador (as que podem instalar programas e mudar configurações) são poucas, usadas só quando necessário e protegidas com verificação em duas etapas?

**Ajuda:** Se a pessoa usa no dia a dia uma conta de administrador e clica num link malicioso, o vírus ganha o mesmo poder de instalar e apagar tudo. Com uma conta comum, o estrago costuma ficar limitado.

**Recomendação:** Retire o poder de administrador das contas de uso diário e deixe as contas de administrador separadas, com verificação em duas etapas.

`CSF PR.AA-05` · `ISO 27002 8.2` · porte ≥ 3 · setores: todos · pesos: RAN 3, VAZ 1

### PR-07 — As pessoas da empresa recebem orientação, pelo menos uma vez por ano, para reconhecer golpes por e-mail, WhatsApp e telefone?

**Ajuda:** A maioria dos ataques a pequenas empresas começa com uma mensagem falsa que convence alguém a clicar, informar uma senha ou fazer um pagamento. Pessoas que conhecem os golpes mais comuns desconfiam na hora certa.

**Recomendação:** Faça uma conversa ou treinamento curto por ano sobre golpes digitais, mostrando exemplos reais do seu setor.

`CSF PR.AT-01` · `ISO 27002 6.3` · porte ≥ 1 · setores: todos · pesos: FRA 3, RAN 2, VAZ 1, IA 1

**Variante (portes 1; até 1 usuário(s)):**

- texto: Você se informa, pelo menos uma vez por ano, sobre os golpes mais comuns por e-mail, WhatsApp e telefone?
- recomendacao: Reserve um momento por ano para conhecer os golpes digitais mais comuns no seu setor. A Cartilha de Segurança para Internet do CERT.br é gratuita.

### PR-08 — Vocês fazem simulações de golpe (por exemplo, um e-mail falso de teste) para ver se as pessoas caem?

**Ajuda:** É um treino prático: a empresa envia uma mensagem falsa inofensiva e vê quem clica. Quem cai recebe uma orientação na hora. Com o tempo, o número de cliques cai bastante.

**Recomendação:** Contrate um serviço ou especialista para enviar, a cada três meses, e-mails ou mensagens falsas de teste, parecidas com os golpes reais do seu setor (para o técnico: simulação de phishing). Antes, combine com a direção e avise a equipe de que esses testes vão acontecer, sem dizer quando. Quem clicar recebe na hora uma orientação curta mostrando os sinais do golpe: o objetivo é ensinar, não punir. Acompanhe a porcentagem de cliques a cada rodada e use os erros mais comuns no treinamento anual.

`CSF PR.AT-01` · `ISO 27002 6.3` · porte ≥ 4 · setores: todos · pesos: FRA 2, RAN 1

### PR-09 — Antes de pagar um boleto novo ou de aceitar que um fornecedor mudou de conta bancária, vocês confirmam por outro meio (por exemplo, ligando para um número que já conheciam)?

**Ajuda:** Um golpe muito comum: alguém se passa por fornecedor ou sócio e manda um boleto ou uma conta nova, muitas vezes com urgência. Confirmar por outro canal, nunca pelo telefone ou e-mail que veio na própria mensagem, derruba a maioria desses golpes.

**Recomendação:** Crie a regra da dupla confirmação: boletos novos, mudança de conta bancária e pagamentos "urgentes" só são pagos após confirmação por telefone já conhecido.

`CSF PR.AT-02` · `ISO 27002 5.14` · porte ≥ 1 · setores: todos · pesos: FRA 3

### PR-10 — Vocês fazem cópias de segurança (backup) automáticas das informações importantes, pelo menos uma vez por semana?

**Ajuda:** O backup é o que permite recuperar tudo se um vírus trancar os arquivos, um computador quebrar ou alguém apagar algo por engano. Automático é melhor, porque backup que depende de alguém lembrar acaba sendo esquecido.

**Recomendação:** Faça cópias de segurança automáticas das informações importantes pelo menos uma vez por semana, ou com mais frequência se refazer alguns dias de trabalho sair caro. Muitas ferramentas que a empresa já usa (Google Drive, OneDrive, sistema de gestão) têm cópia ou histórico de versões: confira se está ligado. Se não tiverem, faça a cotação de uma ferramenta de backup.

`CSF PR.DS-11` · `ISO 27002 8.13` · porte ≥ 1 · setores: todos · pesos: RAN 3, IND 2, TER 1

**Variante (portes 1):**

- recomendacao: Faça cópias de segurança automáticas das informações importantes pelo menos uma vez por semana, ou com mais frequência se refazer alguns dias de trabalho sair caro. Muitas ferramentas que a empresa já usa (Google Drive, OneDrive, sistema de gestão) têm cópia ou histórico de versões: confira se está ligado. Se não tiverem, faça a cotação de uma ferramenta de backup. Mantenha ao menos uma cópia separada do dia a dia, para que um vírus não apague o backup junto.

### PR-11 — Pelo menos uma cópia do backup fica num lugar que um vírus não alcança, como um HD desligado ou uma nuvem que não deixa apagar as cópias?

**Ajuda:** O sequestro de dados costuma procurar e trancar também os backups que estão conectados à rede. Uma cópia isolada é o que garante que a empresa consiga se recuperar sem pagar resgate.

**Recomendação:** Siga a regra 3-2-1: três cópias dos dados (o original e dois backups), em dois tipos de lugar diferentes, sendo uma fora da empresa e fora do alcance de um vírus. Na prática, escolha uma destas opções: um serviço de backup na nuvem com bloqueio de exclusão (também chamado de imutabilidade), que impede apagar as cópias por alguns dias mesmo com a senha; ou dois HDs externos usados em rodízio, ligados só durante a cópia e guardados desconectados. Proteja o backup com uma conta e senha diferentes das do dia a dia, com verificação em duas etapas.

`CSF PR.DS-11` · `ISO 27002 8.13` · porte ≥ 2 · setores: todos · pesos: RAN 3

**Variante (portes 2):**

- recomendacao: Siga a regra 3-2-1: três cópias dos dados (o original e dois backups), em dois tipos de lugar diferentes, sendo uma fora da empresa e fora do alcance de um vírus. Na prática, escolha uma destas opções: um serviço de backup na nuvem com bloqueio de exclusão (também chamado de imutabilidade), que impede apagar as cópias por alguns dias mesmo com a senha; ou dois HDs externos usados em rodízio, ligados só durante a cópia e guardados desconectados. Proteja o backup com uma conta e senha diferentes das do dia a dia, com verificação em duas etapas, e a cada três meses teste se consegue recuperar alguns arquivos.

### PR-12 — Nos últimos 3 meses, vocês testaram recuperar arquivos do backup para ter certeza de que ele funciona?

**Ajuda:** É comum descobrir só no dia do problema que o backup estava incompleto, parado havia meses ou que a recuperação leva dias. Testar mostra se ele funciona e quanto tempo leva para voltar a operar.

**Recomendação:** A cada três meses, recupere alguns arquivos do backup e confira se abrem; uma vez por ano, recupere uma pasta ou um sistema inteiro. Anote quanto tempo levou e compare com o prazo que a empresa aguenta ficar parada, definido no plano de recuperação. Se demorar mais, ajuste o backup ou o plano.

`CSF PR.DS-11` · `ISO 27002 8.13` · porte ≥ 3 · setores: todos · pesos: RAN 2, IND 2

### PR-13 — Os notebooks e celulares da empresa pedem senha para desbloquear e têm os dados protegidos por criptografia?

**Ajuda:** Se um notebook é roubado no carro ou esquecido num táxi, a criptografia impede que o ladrão leia os arquivos. No Windows ela se chama BitLocker e no Mac, FileVault. Nos celulares modernos, basta ter senha de bloqueio.

**Recomendação:** Ative a criptografia de disco em todos os notebooks. Ela já vem no Windows (BitLocker, nas versões Pro) e no Mac (FileVault) e faz com que quem roubar ou achar o equipamento não consiga ler os dados. Guarde a chave de recuperação num lugar seguro fora do notebook, como a conta de administrador da empresa, senão os dados se perdem junto com a senha. Nos celulares, exija senha ou biometria para desbloquear, o que nos aparelhos atuais já liga a criptografia. Configure o bloqueio automático da tela após poucos minutos sem uso e, se possível, use uma ferramenta de gestão de dispositivos que permite apagar os dados à distância em caso de perda ou roubo (para o técnico: MDM).

`CSF PR.DS-01` · `ISO 27002 8.1` · porte ≥ 4 · setores: todos · pesos: VAZ 2

### PR-15 — Vocês guardam só os dados pessoais de que realmente precisam e apagam os antigos que não usam mais?

**Ajuda:** Quanto menos dados a empresa guarda, menor o estrago se houver vazamento. Cadastros de clientes de dez anos atrás ou currículos antigos são risco sem nenhum benefício.

**Recomendação:** Faça uma tabela com os tipos de dados pessoais que a empresa guarda (clientes, funcionários, ex-funcionários, candidatos, fornecedores), para que cada um é usado e por quanto tempo precisa ser guardado, seja por obrigação legal (documentos fiscais, trabalhistas e contábeis têm prazos próprios) ou por necessidade do negócio. Defina um responsável e, uma vez por ano, apague ou anonimize o que passou do prazo, incluindo cópias em e-mails, planilhas e pastas pessoais, e anote o que foi apagado. Esta é uma orientação geral, não um parecer jurídico: confirme os prazos com o contador e com um advogado.

`CSF PR.DS-01` · `ISO 27002 8.10` · porte ≥ 4 · setores: todos · pesos: VAZ 2

### PR-16 — Computadores, celulares, sistemas e o site recebem as atualizações de segurança assim que saem (atualização automática ligada)?

**Ajuda:** As atualizações corrigem falhas que os criminosos já conhecem e exploram. Equipamentos e programas muito antigos, que não recebem mais atualizações (como Windows sem suporte), ficam permanentemente expostos.

**Recomendação:** Ligue as atualizações automáticas em tudo e troque equipamentos e programas que não recebem mais atualizações do fabricante.

`CSF PR.PS-02` · `ISO 27002 8.8` · porte ≥ 1 · setores: todos · pesos: RAN 3, VAZ 2, IND 1

### PR-17 — Todos os computadores têm antivírus ligado e atualizado?

**Ajuda:** O antivírus bloqueia a maior parte dos programas maliciosos conhecidos. O Windows já traz o Microsoft Defender, que só precisa estar ligado. Versões para empresas também avisam um responsável quando detectam algo.

**Recomendação:** Garanta antivírus ligado e atualizado em todos os computadores, com os avisos indo para o responsável pela segurança (em empresas maiores, considere uma solução do tipo EDR).

`CSF PR.PS-05` · `ISO 27002 8.7` · porte ≥ 1 · setores: todos · pesos: RAN 3, VAZ 1

**Variante (portes 1; até 1 usuário(s)):**

- recomendacao: Mantenha o antivírus ligado e atualizado no computador. O Microsoft Defender, que já vem no Windows, é suficiente para começar.

### PR-18 — Quando um equipamento ou sistema novo é instalado, as senhas de fábrica são trocadas e as funções que não serão usadas são desligadas?

**Ajuda:** Roteadores, câmeras e sistemas muitas vezes vêm com senhas padrão (como "admin/admin"), que estão publicadas na internet. Trocá-las e desligar o que não é usado fecha portas fáceis para um criminoso.

**Recomendação:** Crie um roteiro curto de instalação segura e siga-o sempre que entrar um equipamento ou sistema novo (computador, roteador, câmera, impressora, sistema online): (1) trocar a senha de fábrica por uma senha forte, guardada no gerenciador de senhas; (2) instalar as atualizações antes de colocar em uso; (3) desligar funções e contas que não serão usadas, como acesso remoto e usuário convidado; (4) ativar a verificação em duas etapas quando existir; (5) registrar o item no inventário. Peça ao técnico ou fornecedor que fizer a instalação para seguir o roteiro e confirmar por escrito.

`CSF PR.PS-01` · `ISO 27002 8.9` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, IND 1

### PR-19 — O e-mail da empresa tem filtro que bloqueia spam, anexos perigosos e links falsos antes de chegarem às pessoas?

**Ajuda:** Um bom filtro de e-mail barra a maioria das mensagens de golpe antes que alguém precise decidir se clica ou não. Os serviços de e-mail para empresas já têm esse filtro; às vezes só é preciso ativar as opções avançadas.

**Recomendação:** Peça ao seu provedor de e-mail ou a um técnico de TI de confiança para: (1) ligar o filtro que analisa anexos e links antes de chegarem às pessoas (pode exigir um plano pago do Google Workspace ou do Microsoft 365); e (2) configurar no domínio da empresa a proteção que impede golpistas de enviar e-mails como se fossem vocês (para o técnico: SPF, DKIM e DMARC). Se ninguém na empresa cuida disso, contrate algumas horas de um técnico: é um serviço rápido e de baixo custo.

`CSF PR.IR-01` · `ISO 27002 8.23` · porte ≥ 2 · setores: todos · pesos: FRA 2, RAN 2

### PR-20 — O roteador ou firewall da empresa está bem configurado, e o Wi-Fi dos visitantes é separado do Wi-Fi interno?

**Ajuda:** O firewall funciona como um porteiro entre a internet e a rede da empresa. Uma rede Wi-Fi de visitantes separada evita que o celular de um cliente, que pode estar infectado, enxergue os computadores e arquivos da empresa.

**Recomendação:** Peça a um técnico para revisar o roteador/firewall e criar uma rede Wi-Fi de visitantes separada da rede interna.

`CSF PR.IR-01` · `ISO 27002 8.20` · porte ≥ 3 · setores: todos · pesos: RAN 2, VAZ 1, IND 1

### PR-21 — Os sistemas mais importantes têm um 'estepe', por exemplo uma internet reserva ou um serviço que assume se o principal cair?

**Ajuda:** Essa redundância evita que uma queda de internet ou de servidor pare a empresa. Uma segunda conexão de outra operadora (até mesmo 4G/5G) costuma ser barata perto do custo de horas sem vender ou atender.

**Recomendação:** Use a lista de atividades essenciais e o prazo que cada uma aguenta ficar parada, definidos no plano de recuperação, para decidir onde vale ter reserva. Para os servidores e sistemas que não podem parar, contrate um segundo link de internet dedicado de fibra, de outra operadora e com cabeamento e central diferentes do principal, com garantia de disponibilidade em contrato de pelo menos 99,5% ao mês, configurado para assumir automaticamente quando o principal cair. Um 4G/5G serve apenas como contingência mínima para tarefas leves. Para os sistemas que param a operação, peça a um especialista que avalie uma alternativa pronta para assumir, por exemplo uma cópia em nuvem, e compare o custo dela com o prejuízo da parada. Teste a troca para a reserva pelo menos uma vez por ano.

`CSF PR.IR-03` · `ISO 27002 8.14` · porte ≥ 4 · setores: todos · pesos: IND 3

### SAU-01 — No sistema de prontuário ou de agenda, cada profissional entra com seu próprio login, e o sistema registra quem acessou cada prontuário?

**Ajuda:** Dados de saúde são dados sensíveis pela LGPD, e o vazamento é mais grave. Login individual e registro de quem acessou permitem descobrir abusos e são exigidos pelo Conselho Federal de Medicina no prontuário eletrônico.

**Recomendação:** Use um sistema de prontuário com login individual e registro de acessos (o CFM exige isso no prontuário eletrônico, conforme a Res. CFM nº 1.821/2007).

`CSF PR.AA-05` · `ISO 27002 5.15` · porte ≥ 1 · setores: saude · pesos: VAZ 3

### SAU-02 — Os equipamentos de saúde ligados à rede (raio-x, laboratório, monitores) ficam numa rede separada dos computadores da recepção e do administrativo?

**Ajuda:** Equipamentos médicos costumam usar programas antigos que não podem ser atualizados. Mantê-los em redes separadas impede que um vírus que entrou por um e-mail da recepção chegue até eles e pare os atendimentos.

**Recomendação:** Coloque os equipamentos de saúde conectados numa rede separada da rede administrativa.

`CSF PR.IR-01` · `ISO 27002 8.22` · porte ≥ 3 · setores: saude · pesos: RAN 2, IND 2

### VAR-02 — A loja virtual está numa plataforma atualizada e tem proteção contra ataques que tentam derrubar ou invadir o site?

**Ajuda:** Lojas virtuais são alvo de robôs que testam falhas conhecidas e de ataques de sobrecarga que tiram o site do ar em datas de muita venda. Muitas plataformas já incluem essa proteção; em sites próprios, ela precisa ser contratada.

**Recomendação:** Mantenha a plataforma da loja virtual atualizada (ou use uma plataforma pronta, que faz isso por você) e ative um serviço de proteção do site, que filtra acessos maliciosos e segura picos de visitas para o site não cair. Vários têm plano gratuito; peça ajuda a quem cuida do site (para o técnico: CDN/WAF).

`CSF PR.IR-01` · `ISO 27002 8.20` · porte ≥ 2 · setores: varejo · pesos: IND 2, VAZ 2

### IND-01 — Os computadores e controladores que comandam as máquinas ficam numa rede separada da rede do escritório e sem acesso direto pela internet?

**Ajuda:** Se a rede de automação industrial está ligada à rede do escritório, um vírus que chega por e-mail pode alcançar as máquinas e parar a produção. Separar as redes funciona como uma porta corta-fogo.

**Recomendação:** Separe a rede das máquinas (automação, CLP, supervisório) da rede do escritório e da internet.

`CSF PR.IR-01` · `ISO 27002 8.22` · porte ≥ 2 · setores: industria · pesos: RAN 3, IND 2

### IND-03 — O computador ligado às máquinas (por exemplo, o que envia os projetos para a CNC) é usado só para a produção, sem navegar na internet, abrir e-mail ou receber pendrive de terceiros?

**Ajuda:** Esses computadores costumam ter sistemas antigos, que não recebem mais atualizações. Um vírus que chega por um pendrive ou por um e-mail aberto nele pode travar as máquinas e parar a produção.

**Recomendação:** Use o computador das máquinas só para a produção. Leve os projetos até ele por um meio controlado (uma pasta na nuvem da empresa ou um pendrive usado só para isso e verificado pelo antivírus) e mantenha uma cópia dos projetos e das configurações das máquinas no backup.

`CSF PR.PS-01` · `ISO 27002 8.1` · porte ≥ 1 · setores: industria · pesos: RAN 3, IND 2

### TEC-01 — O software que vocês desenvolvem passa por uma revisão de segurança antes de ser entregue aos clientes?

**Ajuda:** Uma falha no seu software pode expor os dados dos seus clientes, e a responsabilidade volta para você. A revisão de segurança combina uma segunda leitura do código (por um colega ou, para quem trabalha sozinho, pelo cliente ou por uma ferramenta de IA para empresas) com ferramentas automáticas que procuram falhas conhecidas.

**Recomendação:** Antes de cada entrega, faça uma revisão de segurança do código: com outra pessoa da equipe ou, se você trabalha sozinho, com o cliente ou com uma ferramenta de IA em versão para empresas (que não usa seu código para treinamento). Use também ferramentas automáticas gratuitas que procuram falhas conhecidas no código e nas bibliotecas usadas.

`CSF PR.PS-06` · `ISO 27002 8.28` · porte ≥ 1 · setores: tecnologia · pesos: VAZ 2, TER 2

### TEC-02 — As senhas e acessos que vocês têm aos sistemas dos clientes ficam num cofre de senhas, com verificação em duas etapas, e são revisados de tempos em tempos?

**Ajuda:** Empresas de tecnologia costumam ter as "chaves" de vários clientes. Um único ataque à sua empresa pode alcançar todos eles, o que transforma um incidente seu em vários incidentes dos clientes.

**Recomendação:** Guarde os acessos dos clientes num cofre de senhas com verificação em duas etapas e revise a cada três meses quem tem acesso a cada cliente.

`CSF PR.AA-05` · `ISO 27002 8.2` · porte ≥ 2 · setores: tecnologia · pesos: TER 3, VAZ 2

### SER-01 — Os documentos dos clientes (contratos, processos, declarações) ficam num local com acesso restrito, e não espalhados em e-mails e pastas pessoais?

**Ajuda:** Escritórios guardam documentos muito sensíveis dos clientes. Quando eles estão espalhados no e-mail e no computador de cada um, é difícil controlar quem vê e impossível garantir o backup.

**Recomendação:** Centralize os documentos de clientes num repositório da empresa, com acesso restrito por cliente ou equipe.

`CSF PR.DS-01` · `ISO 27002 5.15` · porte ≥ 1 · setores: servicos · pesos: VAZ 2, IA 1

### SER-02 — Seus clientes sabem como a empresa costuma cobrar e pedir dados, por exemplo que vocês nunca mudam a conta bancária por e-mail?

**Ajuda:** Golpistas também se passam pela sua empresa para enganar seus clientes com boletos falsos. Avisar os clientes sobre os canais oficiais protege os dois lados e a reputação da empresa.

**Recomendação:** Informe aos clientes, por escrito, quais são os canais oficiais de cobrança e que dados bancários nunca mudam por e-mail ou mensagem.

`CSF PR.AT-01` · `ISO 27002 5.14` · porte ≥ 2 · setores: servicos · pesos: FRA 2


## Perceber quando algo dá errado (DE)

_Formas de notar rapidamente um ataque ou um comportamento estranho._

### DE-01 — Alguém recebe e trata os alertas de segurança (do antivírus, de login suspeito, do banco ou da nuvem), começando pelos mais graves?

**Ajuda:** Muitos ataques dão sinais antes do estrago: um aviso de login de outro país, um antivírus que detectou algo, um alerta do banco. Se esses avisos vão para um e-mail que ninguém lê, o problema só é descoberto tarde demais.

**Recomendação:** Com um especialista, classifique os alertas de segurança pela gravidade para o negócio (por exemplo, crítico: vírus ativo, acesso suspeito à conta do banco ou ao e-mail dos sócios, aviso de vazamento; depois alto, médio e baixo) e defina um prazo de atendimento para cada nível (por exemplo: crítico em até 1 hora, alto no mesmo dia, médio em até uma semana). Direcione os alertas do antivírus, do e-mail, da nuvem e do banco para o responsável pela segurança e registre essas regras na política de segurança. Assim a equipe atende primeiro o que importa, sem ficar sobrecarregada.

`CSF DE.CM-09` · `ISO 27002 8.16` · porte ≥ 3 · setores: todos · pesos: RAN 2, VAZ 2, FRA 1

### DE-02 — Os registros de quem acessou os sistemas importantes (logs) ficam guardados por pelo menos 6 meses?

**Ajuda:** Os logs são o histórico de quem entrou, quando e de onde. Sem eles, depois de um incidente é impossível saber o que foi acessado, e isso importa inclusive para cumprir a LGPD.

**Recomendação:** Ative e guarde por pelo menos 6 meses os registros de acesso (quem entrou, quando e de onde) do e-mail, da nuvem e dos sistemas importantes. Muitos serviços guardam esses registros por pouco tempo no plano básico: confira o prazo e, se for menor, peça ao técnico para copiá-los automaticamente para um local protegido, que só o responsável pela segurança acesse. Esses registros são o que permite descobrir o que aconteceu num incidente. Se a empresa oferece site ou aplicativo com fins comerciais, guardar os registros de acesso por 6 meses é obrigação do Marco Civil da Internet (Lei nº 12.965/2014, art. 15). Esta é uma orientação geral, não um parecer jurídico: para confirmar as obrigações da sua empresa, consulte um advogado.

`CSF DE.CM-01` · `ISO 27002 8.15` · porte ≥ 4 · setores: todos · pesos: VAZ 1, TER 1

### DE-03 — A empresa conta com monitoramento de segurança 24 horas, feito por uma ferramenta ou por uma empresa especializada?

**Ajuda:** Ataques de sequestro de dados costumam acontecer de madrugada ou no fim de semana, justamente quando ninguém está olhando. Um serviço de monitoramento contínuo percebe e reage nesses horários.

**Recomendação:** Contrate um serviço de monitoramento de segurança 24 horas (para o técnico: MDR ou SOC gerenciado). Nele, uma equipe especializada recebe dia e noite os alertas dos computadores, do e-mail e da nuvem e age para conter um ataque, por exemplo isolando um computador infectado de madrugada. No contrato, exija: (1) o que será monitorado; (2) o que a empresa contratada pode fazer sozinha e o que precisa da sua autorização; (3) prazo de resposta para cada nível de gravidade, seguindo a classificação de alertas da sua política de segurança; (4) quem será avisado e por qual canal; (5) um relatório mensal com os alertas e o que foi feito. Compare propostas de pelo menos três fornecedores.

`CSF DE.CM-01` · `ISO 27002 8.16` · porte ≥ 4 · setores: todos · pesos: RAN 2, VAZ 2

### DE-04 — Vocês sabem quais ferramentas de Inteligência Artificial as pessoas estão usando no trabalho e com que tipo de informação?

**Ajuda:** É comum cada pessoa usar a IA que prefere, na conta pessoal, sem que a empresa saiba. Descobrir quais ferramentas estão em uso é o primeiro passo para oferecer uma opção segura.

**Recomendação:** Faça um levantamento das ferramentas de IA em uso: pergunte à equipe, de forma aberta e sem punição, quais usam e para quê, e peça ao técnico para verificar os sites acessados e as extensões instaladas nos navegadores. Com base nisso, escolha uma ou mais ferramentas aprovadas, de preferência versões para empresas, que não usam os dados para treinamento, e registre na política de segurança o que pode e o que nunca pode ser colocado nelas. Ofereça a alternativa aprovada no lugar das não autorizadas e repita o levantamento a cada seis meses, porque novas ferramentas surgem o tempo todo.

`CSF DE.CM-03` · `ISO 27002 8.12` · porte ≥ 4 · setores: todos · pesos: IA 3

### DE-05 — O e-mail ou a nuvem da empresa bloqueia ou avisa quando alguém tenta enviar para fora informações sensíveis, como listas de clientes?

**Ajuda:** É uma prevenção de vazamento de dados: regras que detectam, por exemplo, um arquivo com centenas de CPFs sendo enviado a um endereço externo e pedem confirmação ou bloqueiam o envio.

**Recomendação:** Ative regras que avisam ou bloqueiam quando alguém tenta enviar para fora da empresa informações sensíveis, como CPFs, números de cartão, dados de saúde ou listas de clientes (para o técnico: DLP). Esse recurso costuma fazer parte dos planos mais completos do Microsoft 365 ou do Google Workspace, então confira o custo antes. Defina primeiro, na política de segurança, quais informações são sigilosas. Depois, deixe as regras só avisando por um mês, para ajustá-las sem atrapalhar o trabalho, e então passe a bloquear os casos mais graves.

`CSF DE.CM-03` · `ISO 27002 8.12` · porte ≥ 4 · setores: todos · pesos: VAZ 2, IA 2


## Reagir a um problema (RS)

_O que a empresa faz nas primeiras horas de um incidente._

### RS-01 — Se um ataque acontecesse hoje, as pessoas saberiam o que fazer e quem chamar?

**Ajuda:** Um plano de resposta pode caber numa folha: quem avisar, o que desligar primeiro, telefone do técnico, do banco e do advogado. Nas primeiras horas de um incidente, cada minuto de indecisão aumenta o prejuízo.

**Recomendação:** Escreva um plano de resposta de uma página: quem avisar, o que desligar primeiro e quem chamar. Guarde-o numa pasta compartilhada da empresa e mantenha uma cópia fora dos sistemas da empresa, com o dono ou sócio responsável ou num celular da empresa, porque se um vírus travar os computadores a pasta pode ficar fora do ar. Divulgue para a equipe um número de emergência do responsável (dono, sócio ou técnico de TI contratado). Se a equipe trabalha presencialmente, deixe também uma cópia impressa.

`CSF RS.MA-01` · `ISO 27002 5.24` · porte ≥ 1 · setores: todos · pesos: RAN 2, VAZ 2, FRA 1, IND 1, TER 1

**Variante (portes 1):**

- texto: Se acontecesse um ataque ou golpe hoje, você saberia o que fazer primeiro e teria à mão os contatos do banco, de um técnico de TI e da polícia?
- ajuda: Nas primeiras horas de um ataque ou golpe, cada minuto conta. Em golpes com PIX, avisar o banco logo aumenta a chance de recuperar o dinheiro pelo MED (Mecanismo Especial de Devolução). Ter um plano curto e os contatos prontos, fora do computador que pode estar travado, evita perder tempo.
- recomendacao: Escreva um plano de uma página: o que desligar primeiro, quem chamar e os contatos de emergência (gerente do banco, técnico de TI, advogado, delegacia de crimes cibernéticos). Guarde-o na nuvem e mantenha uma cópia com você, fora dos computadores da empresa, para acessá-lo mesmo com tudo travado.
- pesos: RAN 2, VAZ 2, FRA 2, IND 1, TER 1

### RS-02 — Vocês sabem quando e como avisar a ANPD e os clientes se dados pessoais vazarem?

**Ajuda:** Pela LGPD, vazamentos que possam causar dano às pessoas precisam ser comunicados à ANPD (o órgão que fiscaliza a lei) e aos afetados em poucos dias úteis. Saber isso antes evita perder o prazo e ser multado por comunicação atrasada.

**Recomendação:** Inclua no plano de resposta o que fazer se dados pessoais vazarem. Avisar a ANPD e as pessoas afetadas é obrigatório quando o vazamento pode causar risco ou dano relevante, por exemplo se envolver dados sensíveis (saúde, biometria), dados financeiros, senhas, dados de crianças ou idosos ou dados de muitas pessoas. O prazo é de 3 dias úteis a partir do momento em que a empresa soube do vazamento (o dobro para microempresas e empresas de pequeno porte), pelo formulário no site da ANPD. Registre todos os incidentes, mesmo os que não precisaram ser comunicados, e guarde o registro por 5 anos (Resolução CD/ANPD nº 15/2024). Esta é uma orientação geral, não um parecer jurídico: para confirmar as obrigações da sua empresa, consulte um advogado especializado em proteção de dados.

`CSF RS.CO-03` · `ISO 27002 5.34` · porte ≥ 3 · setores: todos · pesos: VAZ 2

### RS-03 — Vocês têm à mão os contatos do banco, de um técnico de TI e da polícia para acionar rapidamente em caso de golpe ou ataque?

**Ajuda:** Em golpes com PIX, avisar o banco nas primeiras horas aumenta muito a chance de recuperar o dinheiro pelo MED (Mecanismo Especial de Devolução). Ter os contatos prontos, fora do computador que pode estar travado, economiza tempo precioso.

**Recomendação:** Mantenha a lista de contatos de emergência (gerente do banco, técnico de TI, advogado, delegacia de crimes cibernéticos) junto ao plano de resposta, com uma cópia fora dos sistemas da empresa, para acessá-la mesmo com os computadores travados.

`CSF RS.MA-01` · `ISO 27002 5.24` · porte ≥ 2 · setores: todos · pesos: FRA 2, RAN 1

### RS-04 — Nos últimos 12 meses, a equipe fez alguma simulação de ataque para treinar o plano de resposta?

**Ajuda:** Uma simulação pode ser só uma reunião de uma hora: "e se hoje os computadores amanhecessem trancados?". Ela mostra falhas do plano (telefone desatualizado, ninguém sabe onde está o backup) enquanto ainda há tempo de corrigir.

**Recomendação:** Uma vez por ano, faça um exercício em reunião: alguém apresenta uma situação fictícia, por exemplo 'os computadores amanheceram travados com um pedido de resgate' ou 'um cliente avisou que os dados dele apareceram na internet', e a equipe diz, passo a passo, o que faria seguindo o plano de resposta. Participam a direção, o responsável pela segurança, o técnico ou a empresa de TI e, se possível, quem cuida do jurídico e da comunicação. Anote o que travou (contato desatualizado, backup que ninguém sabia recuperar, dúvida sobre avisar a ANPD) e corrija o plano em até um mês. Um especialista pode preparar e conduzir o exercício.

`CSF RS.MA-01` · `ISO 27002 5.24` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, IND 1


## Voltar a funcionar (RC)

_Como a empresa retoma a operação depois de um problema._

### RC-01 — Vocês sabem por quanto tempo cada atividade essencial pode ficar parada e existe um plano para religar os sistemas dentro desse prazo?

**Ajuda:** Algumas empresas aguentam um dia parado; outras perdem clientes em uma hora. Saber por quanto tempo cada atividade essencial pode ficar parada ajuda a decidir quanto investir em backup, em reserva e em contingência.

**Recomendação:** Para cada atividade essencial da sua lista de contingência, defina por quanto tempo ela pode ficar parada sem prejuízo grave (algumas horas? dois dias?). Depois monte um plano de recuperação que caiba nesse prazo: em que ordem os sistemas voltam, quem faz cada passo, onde estão os backups e os acessos necessários e qual técnico ou empresa chamar se a equipe não der conta. Teste o plano uma vez por ano, simulando uma parada.

`CSF RC.RP-01` · `ISO 27002 5.30` · porte ≥ 2 · setores: todos · pesos: RAN 2, IND 3

### RC-02 — Existe um jeito de continuar atendendo os clientes se os sistemas pararem, por exemplo um processo em papel ou um sistema reserva?

**Ajuda:** Um plano de contingência simples (pedidos anotados em formulário, uma cópia da agenda guardada fora do sistema) permite continuar funcionando, mesmo que mais devagar, enquanto os sistemas são recuperados. Isso reduz a perda com a parada.

**Recomendação:** Liste as atividades sem as quais a empresa para (por exemplo: vender, atender clientes, receber pagamentos, entregar). Para cada uma, defina um jeito de continuar sem os sistemas, mesmo que mais devagar: anotar pedidos num formulário, receber pela maquininha, atender por telefone, consultar uma cópia da agenda guardada fora do sistema. Combine com a equipe quando usar esse modo e como lançar no sistema, depois, o que foi feito durante a parada.

`CSF RC.RP-02` · `ISO 27002 5.30` · porte ≥ 1 · setores: todos · pesos: IND 2, RAN 1

