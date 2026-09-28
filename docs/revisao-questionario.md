# Revisão do banco de perguntas

Gerado por `riskpme-catalogo revisao`. Edite `audit/perguntas.yaml`, não este arquivo.

## Perguntas por perfil

| Porte | varejo | servicos | saude | industria | tecnologia |
|---|---|---|---|---|---|
| 1 | 13 | 13 | 13 | 12 | 13 |
| 2 | 22 | 22 | 21 | 21 | 22 |
| 3 | 30 | 30 | 30 | 30 | 30 |
| 4 | 43 | 43 | 43 | 43 | 43 |

## Organização e regras (GV)

_Quem cuida da segurança, que regras existem e como os fornecedores são escolhidos._

### GV-01 — Alguém da empresa é responsável por cuidar da segurança digital, mesmo que também faça outras coisas?

**Ajuda:** Não precisa ser um especialista nem ter dedicação exclusiva. O importante é existir uma pessoa que lembre das tarefas (atualizar, conferir o backup, tirar acessos de quem saiu) e que todos saibam a quem recorrer. Quando é "responsabilidade de todos", na prática fica sem dono.

**Recomendação:** Escolha uma pessoa como responsável pela segurança digital e reserve algumas horas por mês para essa função.

`CSF GV.RR-02` · `ISO 27002 5.2` · porte ≥ 2 · setores: todos · pesos: RAN 1, VAZ 1, FRA 1, IND 1, TER 1, IA 1

### GV-02 — A empresa tem regras escritas sobre como usar senhas, e-mail, computadores e dados — e as pessoas conhecem essas regras?

**Ajuda:** Uma política de segurança pode ter uma ou duas páginas: por exemplo, "não compartilhe senhas", "não use pendrive pessoal", "desconfie de pedidos urgentes de pagamento". Regras combinadas por escrito evitam que cada um faça de um jeito.

**Recomendação:** Escreva uma política de segurança curta (1 a 3 páginas), apresente à equipe e peça que todos assinem que leram.

`CSF GV.PO-01` · `ISO 27002 5.1` · porte ≥ 3 · setores: todos · pesos: RAN 1, VAZ 1, FRA 1, IA 1

### GV-03 — Antes de contratar um fornecedor que vai guardar seus dados ou acessar seus sistemas, vocês verificam se ele se protege bem e colocam isso no contrato?

**Ajuda:** Contador, empresa de TI, sistema de gestão online e agência de marketing costumam ter acesso a informações importantes. Se o fornecedor sofre um ataque, a sua empresa também é atingida. Perguntar se ele faz backup e usa verificação em duas etapas, e incluir cláusula de sigilo e de aviso em caso de incidente, já reduz muito esse risco.

**Recomendação:** Faça uma lista dos fornecedores que acessam seus dados e inclua nos contratos cláusulas de segurança, sigilo e obrigação de avisar sobre incidentes.

`CSF GV.SC-05` · `ISO 27002 5.19` · porte ≥ 2 · setores: todos · pesos: TER 3, VAZ 1

### GV-04 — A empresa sabe o que a LGPD exige dela — por exemplo, informar aos clientes como usa os dados deles?

**Ajuda:** A LGPD (Lei Geral de Proteção de Dados) vale para empresas de todos os tamanhos que guardam dados de pessoas. Pequenas empresas têm regras mais simples, mas continuam responsáveis por proteger esses dados e podem ser multadas se houver vazamento por descuido.

**Recomendação:** Faça um diagnóstico simples de adequação à LGPD e publique um aviso de privacidade, indicando o encarregado de dados (contato para assuntos de privacidade). Empresas de pequeno porte têm regras simplificadas (Resolução CD/ANPD nº 2/2022).

`CSF GV.OC-03` · `ISO 27002 5.34` · porte ≥ 2 · setores: todos · pesos: VAZ 2, IA 1

### GV-05 — Pelo menos uma vez por ano, a direção para para avaliar os riscos digitais e decidir quanto investir em segurança?

**Ajuda:** Segurança digital funciona melhor como decisão de gestão, com orçamento definido, do que como gasto de emergência depois de um problema. Esta própria análise é um exemplo do que pode ser revisto todo ano.

**Recomendação:** Inclua a avaliação de riscos digitais (como esta) na pauta anual da diretoria, com um orçamento definido para segurança.

`CSF GV.RM-01` · `ISO 27002 5.1` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, FRA 1, IND 1, TER 1, IA 1

### GV-06 — Está combinado quais ferramentas de Inteligência Artificial (como ChatGPT ou Gemini) podem ser usadas no trabalho e que tipo de informação nunca deve ser colada nelas?

**Ajuda:** Essas ferramentas ajudam muito, mas tudo o que é colado nelas sai da empresa. Em versões gratuitas, o conteúdo pode ser guardado e usado pelo fornecedor. Colar um contrato, uma lista de clientes ou um prontuário pode virar um vazamento sem ninguém perceber.

**Recomendação:** Defina quais ferramentas de IA podem ser usadas (de preferência versões para empresas, que não usam seus dados para treinamento) e proíba colar dados de clientes ou documentos sigilosos nas demais.

`CSF GV.PO-01` · `ISO 27002 5.10` · porte ≥ 1 · setores: todos · pesos: IA 3

### GV-07 — Os serviços em nuvem que vocês usam (como Google Workspace, Microsoft 365 ou o sistema de gestão online) estão com as opções de segurança ativadas, e vocês sabem o que o fornecedor protege e o que é responsabilidade de vocês?

**Ajuda:** Na nuvem existe responsabilidade compartilhada: o fornecedor garante que o serviço funciona, mas quem controla senhas, permissões e quem acessa o quê é a sua empresa. Muitos recursos de segurança já estão incluídos no plano, só não vêm ligados.

**Recomendação:** Revise as configurações de segurança recomendadas pelo seu provedor de nuvem (há guias prontos do Google e da Microsoft) e ative as que estiverem desligadas.

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

**Recomendação:** Monte uma planilha com equipamentos, sistemas e responsáveis e revise a cada seis meses.

`CSF ID.AM-01` · `ISO 27002 5.9` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, IND 1

### ID-02 — Você sabe onde ficam guardadas as informações importantes da empresa (clientes, financeiro, projetos) — em quais computadores, nuvens ou sistemas?

**Ajuda:** Informação espalhada (no computador de cada um, em pendrives, no WhatsApp, em vários e-mails) é difícil de proteger e de copiar no backup. Saber onde está é o primeiro passo.

**Recomendação:** Anote onde ficam os dados importantes e concentre-os em poucos lugares controlados, como uma pasta na nuvem da empresa.

`CSF ID.AM-07` · `ISO 27002 5.9` · porte ≥ 1 · setores: todos · pesos: VAZ 2, RAN 1, TER 1, IA 1

### ID-03 — De tempos em tempos, alguém verifica se o site e os sistemas acessíveis pela internet têm falhas de segurança conhecidas?

**Ajuda:** Criminosos usam programas que varrem a internet o tempo todo procurando sites e sistemas com falhas de segurança conhecidas. Fazer essa mesma verificação antes deles (há serviços e ferramentas para isso) permite corrigir a falha antes que seja explorada.

**Recomendação:** Contrate ou faça uma verificação de falhas de segurança a cada três meses no site e nos sistemas acessíveis pela internet, corrigindo primeiro as mais graves.

`CSF ID.RA-01` · `ISO 27002 8.8` · porte ≥ 3 · setores: todos · pesos: VAZ 2, RAN 2, IND 1


## Proteção no dia a dia (PR)

_Senhas, cópias de segurança, atualizações e cuidados que evitam problemas._

### PR-01 — Para entrar no e-mail, no banco, nas redes sociais e nos sistemas da empresa, além da senha é preciso confirmar pelo celular (verificação em duas etapas)?

**Ajuda:** Com a verificação em duas etapas, além da senha é pedido um código no celular ou um aplicativo. Mesmo que um golpista descubra a senha, ele não consegue entrar sem o seu celular. É uma das proteções mais eficazes e, na maioria dos serviços, é gratuita.

**Recomendação:** Ative a verificação em duas etapas no e-mail, no banco, nas redes sociais e nos sistemas — comece pelo e-mail e pelo banco. Em geral é gratuito e leva poucos minutos.

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

**Recomendação:** Crie uma lista de verificação de desligamento que retire todos os acessos (e-mail, sistemas, nuvem, grupos) no mesmo dia.

`CSF PR.AA-05` · `ISO 27002 5.18` · porte ≥ 2 · setores: todos · pesos: VAZ 2, TER 1

### PR-05 — Cada pessoa acessa só os dados e sistemas de que realmente precisa para trabalhar?

**Ajuda:** Se todos acessam tudo, uma única conta invadida expõe a empresa inteira. Limitar o acesso por função (o estagiário não precisa ver a folha de pagamento) reduz o tamanho do estrago.

**Recomendação:** Revise quem acessa cada pasta e sistema, retirando os acessos que a função da pessoa não exige.

`CSF PR.AA-05` · `ISO 27002 5.15` · porte ≥ 3 · setores: todos · pesos: VAZ 2, IA 1

### PR-06 — As contas de administrador (as que podem instalar programas e mudar configurações) são poucas, usadas só quando necessário e protegidas com verificação em duas etapas?

**Ajuda:** Se a pessoa usa no dia a dia uma conta de administrador e clica num link malicioso, o vírus ganha o mesmo poder de instalar e apagar tudo. Com uma conta comum, o estrago costuma ficar limitado.

**Recomendação:** Retire o poder de administrador das contas de uso diário e deixe as contas de administrador separadas, com verificação em duas etapas.

`CSF PR.AA-05` · `ISO 27002 8.2` · porte ≥ 3 · setores: todos · pesos: RAN 3, VAZ 1

### PR-07 — As pessoas da empresa recebem orientação, pelo menos uma vez por ano, para reconhecer golpes por e-mail, WhatsApp e telefone?

**Ajuda:** A maioria dos ataques a pequenas empresas começa com uma mensagem falsa que convence alguém a clicar, informar uma senha ou fazer um pagamento. Pessoas que conhecem os golpes mais comuns desconfiam na hora certa.

**Recomendação:** Faça uma conversa ou treinamento curto por ano sobre golpes digitais, mostrando exemplos reais do seu setor.

`CSF PR.AT-01` · `ISO 27002 6.3` · porte ≥ 1 · setores: todos · pesos: FRA 3, RAN 2, VAZ 1, IA 1

### PR-08 — Vocês fazem simulações de golpe (por exemplo, um e-mail falso de teste) para ver se as pessoas caem?

**Ajuda:** É um treino prático: a empresa envia uma mensagem falsa inofensiva e vê quem clica. Quem cai recebe uma orientação na hora. Com o tempo, o número de cliques cai bastante.

**Recomendação:** Faça simulações periódicas de e-mails falsos e ofereça orientação imediata a quem clicar.

`CSF PR.AT-01` · `ISO 27002 6.3` · porte ≥ 4 · setores: todos · pesos: FRA 2, RAN 1

### PR-09 — Antes de pagar um boleto novo ou de aceitar que um fornecedor mudou de conta bancária, vocês confirmam por outro meio (por exemplo, ligando para um número que já conheciam)?

**Ajuda:** Um golpe muito comum: alguém se passa por fornecedor ou sócio e manda um boleto ou uma conta nova, muitas vezes com urgência. Confirmar por outro canal — nunca pelo telefone ou e-mail que veio na própria mensagem — derruba a maioria desses golpes.

**Recomendação:** Crie a regra da dupla confirmação: boletos novos, mudança de conta bancária e pagamentos "urgentes" só são pagos após confirmação por telefone já conhecido.

`CSF PR.AT-02` · `ISO 27002 5.14` · porte ≥ 1 · setores: todos · pesos: FRA 3

### PR-10 — Vocês fazem cópias de segurança (backup) automáticas das informações importantes?

**Ajuda:** O backup é o que permite recuperar tudo se um vírus trancar os arquivos, um computador quebrar ou alguém apagar algo por engano. Automático é melhor, porque backup que depende de alguém lembrar acaba sendo esquecido.

**Recomendação:** Configure um backup automático diário das informações importantes (muitos serviços de nuvem já oferecem).

`CSF PR.DS-11` · `ISO 27002 8.13` · porte ≥ 1 · setores: todos · pesos: RAN 3, IND 2, TER 1

### PR-11 — Pelo menos uma cópia do backup fica num lugar que um vírus não alcança — um HD desligado ou uma nuvem que não deixa apagar as cópias?

**Ajuda:** O sequestro de dados costuma procurar e trancar também os backups que estão conectados à rede. Uma cópia isolada é o que garante que a empresa consiga se recuperar sem pagar resgate.

**Recomendação:** Mantenha uma cópia de backup isolada: um HD guardado desconectado ou uma nuvem com proteção contra exclusão (regra 3-2-1: três cópias, em dois tipos de mídia, uma fora da empresa).

`CSF PR.DS-11` · `ISO 27002 8.13` · porte ≥ 2 · setores: todos · pesos: RAN 3

### PR-12 — Nos últimos 12 meses, vocês testaram recuperar arquivos do backup para ter certeza de que ele funciona?

**Ajuda:** É comum descobrir só no dia do problema que o backup estava incompleto, parado havia meses ou que a recuperação leva dias. Testar mostra se ele funciona e quanto tempo leva para voltar a operar.

**Recomendação:** A cada seis meses, recupere alguns arquivos do backup, confira se abrem e anote quanto tempo levou.

`CSF PR.DS-11` · `ISO 27002 8.13` · porte ≥ 3 · setores: todos · pesos: RAN 2, IND 2

### PR-13 — Os notebooks e celulares da empresa pedem senha para desbloquear e têm os dados protegidos por criptografia?

**Ajuda:** Se um notebook é roubado no carro ou esquecido num táxi, a criptografia impede que o ladrão leia os arquivos. No Windows ela se chama BitLocker e no Mac, FileVault. Nos celulares modernos, basta ter senha de bloqueio.

**Recomendação:** Ative a criptografia (BitLocker ou FileVault) e o bloqueio automático de tela em todos os notebooks e celulares da empresa.

`CSF PR.DS-01` · `ISO 27002 8.1` · porte ≥ 4 · setores: todos · pesos: VAZ 2

### PR-15 — Vocês guardam só os dados pessoais de que realmente precisam e apagam os antigos que não usam mais?

**Ajuda:** Quanto menos dados a empresa guarda, menor o estrago se houver vazamento. Cadastros de clientes de dez anos atrás ou currículos antigos são risco sem nenhum benefício.

**Recomendação:** Defina por quanto tempo cada tipo de dado pessoal é guardado e apague periodicamente o que não é mais necessário.

`CSF PR.DS-01` · `ISO 27002 8.10` · porte ≥ 4 · setores: todos · pesos: VAZ 2

### PR-16 — Computadores, celulares, sistemas e o site recebem as atualizações de segurança assim que saem (atualização automática ligada)?

**Ajuda:** As atualizações corrigem falhas que os criminosos já conhecem e exploram. Equipamentos e programas muito antigos, que não recebem mais atualizações (como Windows sem suporte), ficam permanentemente expostos.

**Recomendação:** Ligue as atualizações automáticas em tudo e troque equipamentos e programas que não recebem mais atualizações do fabricante.

`CSF PR.PS-02` · `ISO 27002 8.8` · porte ≥ 1 · setores: todos · pesos: RAN 3, VAZ 2, IND 1

### PR-17 — Todos os computadores têm antivírus ligado e atualizado?

**Ajuda:** O antivírus bloqueia a maior parte dos programas maliciosos conhecidos. O Windows já traz o Microsoft Defender, que só precisa estar ligado. Versões para empresas também avisam um responsável quando detectam algo.

**Recomendação:** Garanta antivírus ligado e atualizado em todos os computadores, com os avisos indo para o responsável pela segurança (em empresas maiores, considere uma solução do tipo EDR).

`CSF PR.PS-05` · `ISO 27002 8.7` · porte ≥ 1 · setores: todos · pesos: RAN 3, VAZ 1

### PR-18 — Quando um equipamento ou sistema novo é instalado, as senhas de fábrica são trocadas e as funções que não serão usadas são desligadas?

**Ajuda:** Roteadores, câmeras e sistemas muitas vezes vêm com senhas padrão (como "admin/admin"), que estão publicadas na internet. Trocá-las e desligar o que não é usado fecha portas fáceis para um criminoso.

**Recomendação:** Defina um roteiro de instalação segura para computadores, roteadores e câmeras: trocar senhas de fábrica e desligar funções não usadas.

`CSF PR.PS-01` · `ISO 27002 8.9` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, IND 1

### PR-19 — O e-mail da empresa tem filtro que bloqueia spam, anexos perigosos e links falsos antes de chegarem às pessoas?

**Ajuda:** Um bom filtro de e-mail barra a maioria das mensagens de golpe antes que alguém precise decidir se clica ou não. Os serviços de e-mail para empresas já têm esse filtro; às vezes só é preciso ativar as opções avançadas.

**Recomendação:** Ative a filtragem avançada de anexos e links do seu provedor de e-mail e peça a quem cuida do domínio para configurar SPF, DKIM e DMARC, que impedem golpistas de enviar e-mails em nome da sua empresa.

`CSF PR.IR-01` · `ISO 27002 8.23` · porte ≥ 2 · setores: todos · pesos: FRA 2, RAN 2

### PR-20 — O roteador ou firewall da empresa está bem configurado, e o Wi-Fi dos visitantes é separado do Wi-Fi interno?

**Ajuda:** O firewall funciona como um porteiro entre a internet e a rede da empresa. Uma rede Wi-Fi de visitantes separada evita que o celular de um cliente, que pode estar infectado, enxergue os computadores e arquivos da empresa.

**Recomendação:** Peça a um técnico para revisar o roteador/firewall e criar uma rede Wi-Fi de visitantes separada da rede interna.

`CSF PR.IR-01` · `ISO 27002 8.20` · porte ≥ 3 · setores: todos · pesos: RAN 2, VAZ 1, IND 1

### PR-21 — Os sistemas mais importantes têm um "estepe" — por exemplo, uma internet reserva ou um serviço que assume se o principal cair?

**Ajuda:** Essa redundância evita que uma queda de internet ou de servidor pare a empresa. Uma segunda conexão de outra operadora (até mesmo 4G/5G) costuma ser barata perto do custo de horas sem vender ou atender.

**Recomendação:** Contrate uma internet reserva de outra operadora e avalie redundância para os sistemas que param a operação.

`CSF PR.IR-03` · `ISO 27002 8.14` · porte ≥ 4 · setores: todos · pesos: IND 3

### SAU-01 — No sistema de prontuário ou de agenda, cada profissional entra com seu próprio login, e o sistema registra quem acessou cada prontuário?

**Ajuda:** Dados de saúde são dados sensíveis pela LGPD, e o vazamento é mais grave. Login individual e registro de quem acessou permitem descobrir abusos e são exigidos pelo Conselho Federal de Medicina no prontuário eletrônico.

**Recomendação:** Use um sistema de prontuário com login individual e registro de acessos (o CFM exige isso no prontuário eletrônico — Res. CFM nº 1.821/2007).

`CSF PR.AA-05` · `ISO 27002 5.15` · porte ≥ 1 · setores: saude · pesos: VAZ 3

### SAU-02 — Os equipamentos de saúde ligados à rede (raio-x, laboratório, monitores) ficam numa rede separada dos computadores da recepção e do administrativo?

**Ajuda:** Equipamentos médicos costumam usar programas antigos que não podem ser atualizados. Mantê-los em redes separadas impede que um vírus que entrou por um e-mail da recepção chegue até eles e pare os atendimentos.

**Recomendação:** Coloque os equipamentos de saúde conectados numa rede separada da rede administrativa.

`CSF PR.IR-01` · `ISO 27002 8.22` · porte ≥ 3 · setores: saude · pesos: RAN 2, IND 2

### VAR-02 — A loja virtual está numa plataforma atualizada e tem proteção contra ataques que tentam derrubar ou invadir o site?

**Ajuda:** Lojas virtuais são alvo de robôs que testam falhas conhecidas e de ataques de sobrecarga que tiram o site do ar em datas de muita venda. Muitas plataformas já incluem essa proteção; em sites próprios, ela precisa ser contratada.

**Recomendação:** Mantenha a plataforma da loja virtual atualizada e use um serviço de proteção do site contra ataques e sobrecarga (conhecido como CDN/WAF).

`CSF PR.IR-01` · `ISO 27002 8.20` · porte ≥ 2 · setores: varejo · pesos: IND 2, VAZ 2

### IND-01 — Os computadores e controladores que comandam as máquinas ficam numa rede separada da rede do escritório e sem acesso direto pela internet?

**Ajuda:** Se a rede de automação industrial está ligada à rede do escritório, um vírus que chega por e-mail pode alcançar as máquinas e parar a produção. Separar as redes funciona como uma porta corta-fogo.

**Recomendação:** Separe a rede das máquinas (automação, CLP, supervisório) da rede do escritório e da internet.

`CSF PR.IR-01` · `ISO 27002 8.22` · porte ≥ 2 · setores: industria · pesos: RAN 3, IND 2

### TEC-01 — O software que vocês desenvolvem passa por uma revisão de segurança antes de ser entregue aos clientes?

**Ajuda:** Uma falha no seu software pode expor os dados dos seus clientes, e a responsabilidade volta para você. A revisão de segurança combina a revisão do código por outra pessoa e ferramentas automáticas que procuram falhas conhecidas.

**Recomendação:** Torne obrigatória a revisão de código por outra pessoa e inclua ferramentas automáticas de análise de segurança (SAST e de dependências) no processo de entrega.

`CSF PR.PS-06` · `ISO 27002 8.28` · porte ≥ 1 · setores: tecnologia · pesos: VAZ 2, TER 2

### TEC-02 — As senhas e acessos que vocês têm aos sistemas dos clientes ficam num cofre de senhas, com verificação em duas etapas, e são revisados de tempos em tempos?

**Ajuda:** Empresas de tecnologia costumam ter as "chaves" de vários clientes. Um único ataque à sua empresa pode alcançar todos eles, o que transforma um incidente seu em vários incidentes dos clientes.

**Recomendação:** Guarde os acessos dos clientes num cofre de senhas com verificação em duas etapas e revise a cada três meses quem tem acesso a cada cliente.

`CSF PR.AA-05` · `ISO 27002 8.2` · porte ≥ 2 · setores: tecnologia · pesos: TER 3, VAZ 2

### SER-01 — Os documentos dos clientes (contratos, processos, declarações) ficam num local com acesso restrito, e não espalhados em e-mails e pastas pessoais?

**Ajuda:** Escritórios guardam documentos muito sensíveis dos clientes. Quando eles estão espalhados no e-mail e no computador de cada um, é difícil controlar quem vê e impossível garantir o backup.

**Recomendação:** Centralize os documentos de clientes num repositório da empresa, com acesso restrito por cliente ou equipe.

`CSF PR.DS-01` · `ISO 27002 5.15` · porte ≥ 1 · setores: servicos · pesos: VAZ 2, IA 1

### SER-02 — Seus clientes sabem como a empresa costuma cobrar e pedir dados — por exemplo, que vocês nunca mudam a conta bancária por e-mail?

**Ajuda:** Golpistas também se passam pela sua empresa para enganar seus clientes com boletos falsos. Avisar os clientes sobre os canais oficiais protege os dois lados e a reputação da empresa.

**Recomendação:** Informe aos clientes, por escrito, quais são os canais oficiais de cobrança e que dados bancários nunca mudam por e-mail ou mensagem.

`CSF PR.AT-01` · `ISO 27002 5.14` · porte ≥ 2 · setores: servicos · pesos: FRA 2


## Perceber quando algo dá errado (DE)

_Formas de notar rapidamente um ataque ou um comportamento estranho._

### DE-01 — Alguém recebe e olha os alertas de segurança — do antivírus, de login suspeito, do banco ou da nuvem?

**Ajuda:** Muitos ataques dão sinais antes do estrago: um aviso de login de outro país, um antivírus que detectou algo, um alerta do banco. Se esses avisos vão para um e-mail que ninguém lê, o problema só é descoberto tarde demais.

**Recomendação:** Direcione os alertas de segurança (antivírus, e-mail, nuvem, banco) para o responsável pela segurança e combine que ele os confira todo dia.

`CSF DE.CM-09` · `ISO 27002 8.16` · porte ≥ 3 · setores: todos · pesos: RAN 2, VAZ 2, FRA 1

### DE-02 — Os registros de quem acessou os sistemas importantes (logs) ficam guardados por pelo menos 6 meses?

**Ajuda:** Os logs são o histórico de quem entrou, quando e de onde. Sem eles, depois de um incidente é impossível saber o que foi acessado — e isso importa inclusive para cumprir a LGPD.

**Recomendação:** Ative e guarde por pelo menos 6 meses os registros de acesso do e-mail, da nuvem e dos sistemas importantes.

`CSF DE.CM-01` · `ISO 27002 8.15` · porte ≥ 4 · setores: todos · pesos: VAZ 1, TER 1

### DE-03 — A empresa conta com monitoramento de segurança 24 horas, feito por uma ferramenta ou por uma empresa especializada?

**Ajuda:** Ataques de sequestro de dados costumam acontecer de madrugada ou no fim de semana, justamente quando ninguém está olhando. Um serviço de monitoramento contínuo percebe e reage nesses horários.

**Recomendação:** Avalie contratar um serviço de monitoramento e resposta 24 horas (conhecido como MDR ou SOC gerenciado).

`CSF DE.CM-01` · `ISO 27002 8.16` · porte ≥ 4 · setores: todos · pesos: RAN 2, VAZ 2

### DE-04 — Vocês sabem quais ferramentas de Inteligência Artificial as pessoas estão usando no trabalho e com que tipo de informação?

**Ajuda:** É comum cada pessoa usar a IA que prefere, na conta pessoal, sem que a empresa saiba. Descobrir quais ferramentas estão em uso é o primeiro passo para oferecer uma opção segura.

**Recomendação:** Pergunte à equipe (ou verifique nos sistemas) quais ferramentas de IA estão em uso e ofereça uma alternativa aprovada no lugar das não autorizadas.

`CSF DE.CM-03` · `ISO 27002 8.12` · porte ≥ 4 · setores: todos · pesos: IA 3

### DE-05 — O e-mail ou a nuvem da empresa bloqueia ou avisa quando alguém tenta enviar para fora informações sensíveis, como listas de clientes?

**Ajuda:** É uma prevenção de vazamento de dados: regras que detectam, por exemplo, um arquivo com centenas de CPFs sendo enviado a um endereço externo e pedem confirmação ou bloqueiam o envio.

**Recomendação:** Ative regras de prevenção de vazamento de dados (DLP) no e-mail e na nuvem para dados pessoais e documentos sigilosos.

`CSF DE.CM-03` · `ISO 27002 8.12` · porte ≥ 4 · setores: todos · pesos: VAZ 2, IA 2


## Reagir a um problema (RS)

_O que a empresa faz nas primeiras horas de um incidente._

### RS-01 — Se um ataque acontecesse hoje, as pessoas saberiam o que fazer e quem chamar?

**Ajuda:** Um plano de resposta pode caber numa folha: quem avisar, o que desligar primeiro, telefone do técnico, do banco e do advogado. Nas primeiras horas de um incidente, cada minuto de indecisão aumenta o prejuízo.

**Recomendação:** Escreva um plano de resposta de uma página (quem avisar, o que desligar, quem chamar) e deixe uma cópia impressa em local conhecido.

`CSF RS.MA-01` · `ISO 27002 5.24` · porte ≥ 1 · setores: todos · pesos: RAN 2, VAZ 2, FRA 1, IND 1, TER 1

### RS-02 — Vocês sabem quando e como avisar a ANPD e os clientes se dados pessoais vazarem?

**Ajuda:** Pela LGPD, vazamentos que possam causar dano às pessoas precisam ser comunicados à ANPD (o órgão que fiscaliza a lei) e aos afetados, dentro de prazo. Saber isso antes evita multa por comunicação atrasada.

**Recomendação:** Inclua no plano de resposta como e quando comunicar vazamentos à ANPD e aos afetados (Resolução CD/ANPD nº 15/2024).

`CSF RS.CO-03` · `ISO 27002 5.34` · porte ≥ 3 · setores: todos · pesos: VAZ 2

### RS-03 — Vocês têm à mão os contatos do banco, de um técnico de TI e da polícia para acionar rapidamente em caso de golpe ou ataque?

**Ajuda:** Em golpes com PIX, avisar o banco nas primeiras horas aumenta muito a chance de recuperar o dinheiro pelo MED (Mecanismo Especial de Devolução). Ter os contatos prontos, fora do computador que pode estar travado, economiza tempo precioso.

**Recomendação:** Mantenha uma lista impressa de contatos de emergência (gerente do banco, técnico de TI, advogado, delegacia de crimes cibernéticos).

`CSF RS.MA-01` · `ISO 27002 5.24` · porte ≥ 1 · setores: todos · pesos: FRA 2, RAN 1

### RS-04 — Nos últimos 12 meses, a equipe fez alguma simulação de ataque para treinar o plano de resposta?

**Ajuda:** Uma simulação pode ser só uma reunião de uma hora: "e se hoje os computadores amanhecessem trancados?". Ela mostra falhas do plano — telefone desatualizado, ninguém sabe onde está o backup — enquanto ainda há tempo de corrigir.

**Recomendação:** Faça uma vez por ano uma simulação em reunião de um ataque de sequestro de dados e de um vazamento, e corrija o que não funcionou.

`CSF RS.MA-01` · `ISO 27002 5.24` · porte ≥ 4 · setores: todos · pesos: RAN 1, VAZ 1, IND 1


## Voltar a funcionar (RC)

_Como a empresa retoma a operação depois de um problema._

### RC-01 — Você sabe quanto tempo a empresa levaria para voltar a funcionar se os computadores parassem, e existe um plano para isso?

**Ajuda:** Algumas empresas aguentam um dia parado; outras perdem clientes em uma hora. Saber quanto tempo parado é tolerável para cada sistema ajuda a decidir quanto investir em backup e em contingência.

**Recomendação:** Defina por quanto tempo cada sistema importante pode ficar parado e monte um plano de recuperação que caiba nesse prazo.

`CSF RC.RP-01` · `ISO 27002 5.30` · porte ≥ 2 · setores: todos · pesos: RAN 2, IND 3

### RC-02 — Existe um jeito de continuar atendendo os clientes se os sistemas pararem — por exemplo, um processo em papel ou um sistema reserva?

**Ajuda:** Um plano de contingência simples (vendas anotadas em formulário, agenda impressa do dia seguinte) permite continuar funcionando enquanto os sistemas são recuperados, reduzindo a perda com a parada.

**Recomendação:** Prepare um modo de contingência para as atividades essenciais (por exemplo, formulários em papel e agenda impressa) e combine com a equipe quando usá-lo.

`CSF RC.RP-02` · `ISO 27002 5.30` · porte ≥ 1 · setores: todos · pesos: IND 2, RAN 1

