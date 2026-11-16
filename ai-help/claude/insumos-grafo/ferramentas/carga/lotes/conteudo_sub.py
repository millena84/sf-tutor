"""Issue #34: conteúdo específico dos temas internos (subclassificações). Usado por conteudo_temas.py.

Mesma regra de conteudo_cls.py: só fatos já catalogados nas funcionalidades ou lidos nas notas de extração do #34.
Temas internos sem fonte lida ficam de fora (lista PENDENTES) até a próxima rodada de pesquisa.
"""
from conteudo_cls import E, ini, enc, av, AF

PENDENTES = []  # todos os temas internos têm conteúdo desde o lote 4 (issue #34)

S = {}

# ------------------------------------------------------------------ Organização e configurações base
S["sub:identificacao-e-configuracao-da-org"] = {
    "para_iniciantes": ini("São os dados que identificam a empresa na Salesforce e os parâmetros gerais da org: informações da empresa, "
                           "licenças compradas e os contatos responsáveis pela org.",
                           "O administrador confere as licenças disponíveis e atualiza o contato de segurança da empresa.", E("src:help-setup-company")),
    "encadeamento": enc("É o ponto de partida de Organização: idioma, moeda, ano fiscal e horários são ajustados sobre essa base.", E("src:help-setup-company")),
}
S["sub:settings"] = {
    "para_iniciantes": ini("Settings é uma família de metadata types com nomes terminados em Settings. Cada um guarda um grupo de "
                           "configurações gerais da org, como as de horário comercial.",
                           "BusinessHoursSettings guarda configurações de horário comercial e pode ser recuperado e implantado como qualquer outro metadado.",
                           E("src:mdapi-businesshourssettings", "src:mdapi-intro")),
    "encadeamento": enc("Dentro de Organização, é o lado 'como código': várias configurações gerais existem como metadata types Settings, "
                        "que podem ser recuperados e implantados. Um Settings de assunto com tema próprio é estudado nesse tema.",
                        E("src:mdapi-businesshourssettings", "src:mdapi-intro")),
    "avancado": [av("implantacao", "Confira o suporte de cada Settings",
                    "Cada Settings é um metadata type próprio, com suporte registrado na lista do Salesforce CLI. Confira esse suporte antes "
                    "de incluir um Settings num pipeline de implantação.", E("src:sdr-metadata-support"))],
}
S["sub:localizacao-idiomas-e-traducao"] = {
    "para_iniciantes": ini("Define em que idioma a interface aparece e qual localidade a org usa, o que muda como os valores são exibidos.",
                           "A empresa define português como idioma padrão e a localidade do Brasil para exibir datas e números.", E("src:help-setup-company")),
    "encadeamento": enc("Junto com moedas e ano fiscal, muda como os valores aparecem, sem mudar os dados guardados.", E("src:help-setup-company")),
}
S["sub:moedas-e-calendario-fiscal"] = {
    "para_iniciantes": ini("Define as moedas da org e como o ano fiscal da empresa é contado.",
                           "Uma empresa com ano fiscal de abril a março registra isso na org para que os períodos batam com a contabilidade.",
                           E("src:help-setup-company")),
    "encadeamento": enc("Previsões de vendas, que trabalham por período, ficam em Vendas.", E("src:help-setup-company", "src:help-sales-basics")),
}
S["sub:horarios-comerciais-e-feriados"] = {
    "para_iniciantes": ini("Define os dias, horários e fuso em que o atendimento funciona, e os feriados em que esse horário não vale.",
                           "Suporte de São Paulo: segunda a sexta, das 8h às 18h, no fuso de Brasília.", E("src:help-bh", "src:objref-businesshours"),
                           comece=["func:horario-comercial"]),
    "encadeamento": enc("Outras regras usam esses horários para contar prazos, como o escalonamento de casos e os marcos de SLA, no tema Atendimento.",
                        E("src:help-bh", "src:help-ent-bh")),
    "avancado": [av("atencao", "Horário comercial em cascata",
                    "Nos processos de SLA, o horário do milestone prevalece sobre o do processo, que prevalece sobre o do caso.", E("src:help-ent-bh"))],
}

# ------------------------------------------------------------------ Acesso, identidade e segurança
S["sub:usuarios-e-provisionamento"] = {
    "para_iniciantes": ini("Cada pessoa ou integração que acessa a org é um usuário, com perfil, idioma e fuso. Provisionar é criar, ativar e "
                           "desativar esses usuários ao longo do tempo.",
                           "Uma nova analista entra na empresa: o administrador cria o usuário com o perfil adequado e depois atribui permission sets extras.",
                           E("src:objref-user", "src:help-users"), comece=["func:usuarios"]),
    "encadeamento": enc("Dentro de Acesso, é o primeiro passo: sem usuário não há login, perfil nem permissão.", E("src:objref-user")),
    "avancado": [
        av("atencao", "Desativar, não excluir", "Usuários não podem ser excluídos, só desativados (IsActive); a API não oferece delete() em User.",
           E("src:objref-user", "src:help-users")),
        av("decisao", "Criação no primeiro login", "Com SSO por SAML, o provisionamento just-in-time cria o usuário no primeiro acesso, a partir da asserção do provedor.",
           E("src:mdapi-samlssoconfig")),
    ],
}
S["sub:autenticacao-sso-e-mfa"] = {
    "para_iniciantes": ini("É como a pessoa prova quem é: senha, login único com a conta da empresa (SSO) ou provedores externos, como Google e Microsoft.",
                           "Funcionários entram pelo provedor corporativo; a asserção traz o Federation ID e o usuário é criado no primeiro login.",
                           E("src:mdapi-samlssoconfig", "src:help-auth-provider-oidc"), comece=["func:sso-saml", "func:auth-providers"]),
    "encadeamento": enc("Depois de autenticada, a pessoa passa pelas políticas de sessão e login e só então pelas permissões.", E("src:security-guide")),
    "avancado": [
        av("decisao", "SAML ou provedor de autenticação",
           "Para login com o provedor corporativo, a configuração SAML aceita a asserção e pode criar o usuário no primeiro acesso. Provedores "
           "de autenticação (OpenID Connect, Google, Microsoft) servem tanto para login quanto para obter tokens usados por integrações.",
           E("src:mdapi-samlssoconfig", "src:help-auth-provider-oidc")),
        av("implantacao", "Segredo não vem no retrieve", "O segredo do app do provedor (consumerSecret) não vem no retrieve: é exportado como marcador e precisa ser preenchido em cada ambiente.",
           E("src:mdapi-authprovider")),
    ],
}
S["sub:sessoes-e-politicas-de-login"] = {
    "para_iniciantes": ini("Define as regras de sessão e de login e mostra o estado de acesso de cada usuário, como congelado ou bloqueado.",
                           "Um perfil restringe o login a faixas de IP da empresa; uma tentativa de fora fica registrada no histórico de login.",
                           E("src:objref-userlogin", "src:mdapi-profile", "src:objref-loginhistory"),
                           comece=["func:estado-e-historico-de-login", "func:perfis"]),
    "encadeamento": enc("Fica entre a autenticação e as permissões: a pessoa provou quem é, mas ainda precisa cumprir horários e origens permitidos.",
                        E("src:mdapi-profile")),
    "avancado": [av("atencao", "Onde ficam IP e horário", "Faixas de IP e horários de login são configurados no perfil (Profile.loginIpRanges); o IP de cada "
                    "tentativa fica em LoginHistory.SourceIp.", E("src:mdapi-profile", "src:objref-loginhistory"))],
}
S["sub:permissoes-perfis-e-grupos"] = {
    "para_iniciantes": ini("Define o que cada usuário pode fazer. Todo usuário tem exatamente um perfil, com o acesso básico; permission sets "
                           "somam acessos extras; e permission set groups juntam vários permission sets para atribuir de uma vez.",
                           "O grupo 'Analista de Crédito' reúne três permission sets e é atribuído em um passo.",
                           E("src:mdapi-profile", "src:mdapi-permissionset", "src:mdapi-permissionsetgroup"),
                           comece=["func:permission-sets", "func:permission-set-groups"]),
    "encadeamento": enc("É a camada do 'o que posso fazer'. Quais registros cada um enxerga fica em 'Acesso a registros e hierarquias'.",
                        E("src:mdapi-permissionset", "src:security-guide")),
    "avancado": [
        av("decisao", "Perfil enxuto, acesso por permission set",
           "Mantenha perfis enxutos e conceda acessos adicionais por permission sets, nomeados pela capacidade concedida e não pela pessoa. "
           "Permission set groups modelam papéis de trabalho e permitem silenciar permissões.",
           E("src:help-users", "src:help-perm-sets-create", "src:mdapi-permissionsetgroup")),
        av("implantacao", "Atribuição não vai no deploy",
           "A atribuição é um registro de PermissionSetAssignment, não parte do XML; usuários guest, de integração e de sistema só podem "
           "receber grupos por esse objeto, e só grupos com status Updated podem ser atribuídos.",
           E("src:objref-permissionsetassignment", "src:help-psg-assign")),
    ],
}
S["sub:licencas-e-entitlements-de-acesso"] = {
    "para_iniciantes": ini("Licenças definem o que pode ser concedido a cada usuário: a licença de usuário dá o pacote básico, e licenças de "
                           "recurso liberam funcionalidades extras, como a de usuário do Service Cloud.",
                           "Uma pessoa com licença Salesforce Platform não tem direito a leads, oportunidades nem previsões, segundo a Ajuda.",
                           E("src:help-user-licenses", "src:help-service-feature-license")),
    "encadeamento": enc("Junto com a edição da org, define o que está disponível antes de qualquer permissão.", E("src:help-editions", "src:help-user-licenses")),
}
S["sub:acesso-a-registros-e-hierarquias"] = {
    "para_iniciantes": ini("Decide quais registros cada usuário enxerga: os padrões de acesso da org, o compartilhamento e as equipes.",
                           "Na conta ACME, o executivo de contas é o dono e o engenheiro de pré-venda entra na equipe com acesso de leitura.",
                           E("src:security-guide", "src:objref-accountteammember"), comece=["func:equipes-de-conta-e-oportunidade"]),
    "encadeamento": enc("É a camada do 'quais registros'. O 'que posso fazer com o objeto' fica em 'Permissões, perfis e grupos'.", E("src:security-guide")),
    "avancado": [av("decisao", "Equipe em vez de trocar o dono", "Equipes de conta e de oportunidade dão acesso e responsabilidade compartilhada sem mudar o dono do registro.",
                    E("src:objref-accountteammember", "src:objref-opportunityteammember"))],
}
S["sub:credenciais-certificados-e-protecao-de-dados"] = {
    "para_iniciantes": ini("Guarda os segredos que protegem conexões: certificados e chaves e as credenciais de acesso a sistemas externos.",
                           "Um certificado autoassinado de 4096 bits assina o JWT usado por uma credencial externa.",
                           E("src:mdapi-certificate", "src:help-cert-self-signed", "src:mdapi-namedcredential"), comece=["func:certificados"]),
    "encadeamento": enc("Serve aos dois lados: login, quando o SSO assina com certificados, e integrações, quando credenciais externas usam certificados e OAuth.",
                        E("src:mdapi-certificate", "src:mdapi-externalcredential")),
    "avancado": [av("atencao", "Autenticação mútua", "InboundCertificate só existe com a permissão MutualAuthentication habilitada na org.", E("src:mdapi-inboundcertificate"))],
}

# ------------------------------------------------------------------ Dados e modelagem
S["sub:objetos-e-entidades"] = {
    "para_iniciantes": ini("Objetos são as estruturas que guardam registros: os padrão vêm com a Salesforce, como Conta e Contato, e os "
                           "customizados são criados para o que é próprio do negócio.",
                           "Um objeto Contrato_Servico__c para contratos de manutenção.", E("src:mdapi-customobject", "src:objref-data-model"),
                           comece=["func:objetos-customizados"]),
    "encadeamento": enc("É a base do tema: campos, relacionamentos e tipos de registro sempre pertencem a um objeto.", E("src:mdapi-customobject")),
    "avancado": [av("implantacao", "Um metadata type, vários tipos de objeto",
                    "O metadata type CustomObject define objetos customizados e também a definição de objetos externos (sufixo __x) e de "
                    "eventos de plataforma (eventType, publishBehavior).", E("src:mdapi-customobject"))],
}
S["sub:campos-e-tipos"] = {
    "para_iniciantes": ini("Campos são as informações de cada registro. Cada campo tem um tipo, que define o que ele aceita, como texto, "
                           "número, moeda, data ou lista de valores.",
                           "Um campo Valor_Mensal__c do tipo moeda em Contrato_Servico__c.", E("src:mdapi-customfield"),
                           comece=["func:campos-customizados"]),
    "encadeamento": enc("Campos de relacionamento ligam objetos e são estudados em 'Relacionamentos e junções'; regras de validação conferem os valores.",
                        E("src:mdapi-customfield", "src:mdapi-validationrule")),
    "avancado": [av("seguranca", "Campo novo precisa de segurança de campo",
                    "Defina quem vê e edita cada campo pela segurança em nível de campo; tirar o campo do layout não restringe o acesso.", E("src:security-fls"))],
}
S["sub:relacionamentos-e-juncoes"] = {
    "para_iniciantes": ini("Relacionamentos ligam registros de objetos diferentes, como o contato à sua conta. Quando um registro precisa se "
                           "ligar a vários de outro objeto, e vice-versa, usa-se um objeto de junção.",
                           "PermissionSetAssignment liga usuários e permission sets: um usuário pode ter vários permission sets, e um permission set pode estar em vários usuários.",
                           E("src:objref-data-model", "src:objref-contact", "src:objref-permissionsetassignment"), comece=["func:campos-customizados"]),
    "encadeamento": enc("Depende de objetos e campos. No Nível avançado de cada tema, as dependências entre componentes mostram as referências documentadas.",
                        E("src:objref-data-model")),
}
S["sub:tipos-de-registro-e-processos-de-negocio"] = {
    "para_iniciantes": ini("Tipos de registro são variações de um mesmo objeto, com valores de lista, processos e páginas diferentes.",
                           "Contratos 'Manutenção' e 'Licenciamento' com listas de status diferentes.", E("src:mdapi-recordtype"),
                           comece=["func:tipos-de-registro"]),
    "encadeamento": enc("Muda a página e as listas de valores de cada variação; por isso aparece também em Interface e em 'Listas de valores'.",
                        E("src:mdapi-recordtype")),
    "avancado": [av("atencao", "Opportunity exige processo de vendas", "Tipos de registro de Opportunity exigem um processo de vendas (BusinessProcessId em RecordType).",
                    E("src:objref-recordtype"))],
}
S["sub:listas-de-valores"] = {
    "para_iniciantes": ini("Picklists são listas fechadas de valores para um campo, como as etapas de uma oportunidade. Cada tipo de registro "
                           "pode mostrar só parte dos valores.",
                           "Etapas de um contrato: Rascunho, Em análise, Assinado.", E("src:mdapi-customfield", "src:mdapi-recordtype", "src:mdapi-pathassistant"),
                           comece=["func:tipos-de-registro", "func:path"]),
    "encadeamento": enc("O Path usa um campo picklist para mostrar etapas na tela, e o tipo de registro escolhe quais valores aparecem.",
                        E("src:mdapi-pathassistant", "src:mdapi-recordtype")),
    "avancado": [av("atencao", "Um Path por combinação", "Existe um Path por combinação de objeto, picklist e tipo de registro.", E("src:help-path-create"))],
}
S["sub:modelos-externos-e-especializacoes"] = {
    "para_iniciantes": ini("Cobre formas especiais de modelar dados, como objetos externos (sufixo __x), que mostram dados de outro sistema sem copiá-los.",
                           "Pedidos do ERP aparecem como objeto externo Pedido__x, lidos via OData no momento da consulta.",
                           E("src:mdapi-customobject", "src:help-external-data-source-odata")),
    "encadeamento": enc("A conexão com a fonte externa fica em 'Conectividade e virtualização de dados', no tema de integração.",
                        E("src:mdapi-externaldatasource")),
}

# ------------------------------------------------------------------ Qualidade
S["sub:validacao"] = {
    "para_iniciantes": ini("Regras de validação são fórmulas que impedem salvar um registro quando uma condição de erro é verdadeira.",
                           "Impedir salvar um contrato com valor negativo.", E("src:mdapi-validationrule"), comece=["func:regras-de-validacao"]),
    "encadeamento": enc("É a primeira barreira de qualidade: atua no momento de salvar.", E("src:mdapi-validationrule")),
    "avancado": [av("decisao", "Validação, automação ou segurança",
                    "A validação bloqueia a gravação; não esconde o campo nem corrige o valor. Para restringir quem edita, use a segurança de "
                    "campo; para preencher ou corrigir valores, use automação.", E("src:mdapi-validationrule", "src:security-fls", "src:mdapi-flow"))],
}
S["sub:duplicidade-e-correspondencia"] = {
    "para_iniciantes": ini("Trata registros duplicados: ajuda a evitar que o mesmo cliente ou contato seja cadastrado duas vezes, inclusive na "
                           "importação de dados de terceiros.",
                           "Ao tentar cadastrar um contato que já existe, a pessoa é avisada antes de criar outro.", E("src:help-produtos-sales")),
    "encadeamento": enc("Atua na criação e na importação de registros; a validação atua no valor de cada campo.", E("src:help-produtos-sales", "src:mdapi-validationrule")),
}
S["sub:rastreabilidade-e-historico"] = {
    "para_iniciantes": ini("Guarda o histórico de alterações de campos e registros: quem mudou, o que mudou e quando.",
                           "Um auditor confere quem alterou o valor de um contrato no mês passado.", E("src:security-guide")),
    "encadeamento": enc("Cruza com Observabilidade: o Security Guide trata o histórico de campos junto com auditoria e monitoramento.", E("src:security-guide")),
}

# ------------------------------------------------------------------ Automação
S["sub:flow-e-orquestracao"] = {
    "para_iniciantes": ini("Flow é a automação declarativa feita no Flow Builder, com elementos, variáveis e decisões. Pode começar por uma "
                           "tela, pela gravação de um registro, por um agendamento ou por outros gatilhos. Uma orquestração junta vários "
                           "flows num processo de etapas, com passos para pessoas e passos automáticos.",
                           "Atualizar o status do contrato quando a assinatura é registrada.",
                           E("src:mdapi-flow", "src:help-flow-types", "src:help-orchestration-overview"), comece=["func:flow", "func:flow-orchestration"]),
    "encadeamento": enc("É a ferramenta principal do tema. O tipo do flow define o que ele pode conter e como é distribuído: screen flow para "
                        "telas, autolaunched para segundo plano, record-triggered para reagir a registros. Screen Flows também aparecem em "
                        "Interface, como opção para formulários de várias telas. Aprovações feitas com flow ficam em 'Decisões e aprovações'.",
                        E("src:mdapi-flow", AF, "src:help-flow-types", "src:help-flow-triggered")),
    "avancado": [
        av("decisao", "Quando o Screen Flow é a escolha", "Para assistentes com várias telas, sem exigência rígida de marca, o guia de decisão indica "
           "Screen Flow: navegação pronta e lógica mantida por administradores.", E(AF)),
        av("seguranca", "Contexto de sistema", "Screen Flow roda no contexto do usuário por padrão, mas pode rodar em contexto de sistema; esse modo deve "
           "ficar restrito a usuários confiáveis.", E(AF)),
        av("decisao", "Antes ou depois de salvar", "Um record-triggered flow before-save altera o próprio registro antes da gravação e é bem mais "
           "rápido. Para o resto, usa-se after-save. Chamada a sistema externo não cabe no caminho síncrono: a Salesforce impede callouts "
           "enquanto o registro é gravado.", E("src:help-flow-triggered", "src:help-flow-record-triggered-considerations")),
        av("limite", "Limites por transação", "Flows seguem os governor limits da transação: 100 consultas SOQL, 50.000 registros lidos, 150 "
           "instruções DML e 10.000 registros gravados. Get Records, Create, Update e Delete Records contam para esses totais.",
           E("src:help-flow-limits-transaction", "src:help-flow-transactions")),
        av("atencao", "Ordem entre flows do mesmo objeto", "Cada record-triggered flow recebe um trigger order de 1 a 2.000. A ordem só vale entre "
           "flows do mesmo objeto e do mesmo tipo de gatilho; o Flow Trigger Explorer mostra e reordena todos.",
           E("src:help-flow-run-order", "src:help-flow-triggered")),
        av("escala", "Caminhos agendados e flows agendados", "Um scheduled path processa até 200 registros por lote e tenta de novo até 5 vezes "
           "depois de falhar. Schedule-triggered flows têm teto diário de entrevistas: 250.000 ou 200 por licença de usuário, o que for maior.",
           E("src:help-flow-scheduled-paths", "src:help-flow-schedule-triggered")),
        av("decisao", "Quando usar orquestração", "Uma orquestração tem stages, e cada stage tem steps. O interactive step atribui um screen "
           "flow a uma pessoa, grupo ou fila e gera um work item; o background step roda um autolaunched flow sem interação. Serve a "
           "processos longos, com várias pessoas e esperas.", E("src:help-orchestration-overview", "src:help-orchestration-steps", "src:help-orchestration-types")),
        av("implantacao", "Como metadado", "Cada flow é um componente Flow. As opções gerais ficam em FlowSettings: por exemplo, "
           "enableFlowDeployAsActiveEnabled decide se flows podem ser implantados já ativos, e o padrão é false em produção.",
           E("src:mdapi-flow", "src:mdapi-flowsettings")),
    ],
}
S["sub:decisoes-e-aprovacoes"] = {
    "para_iniciantes": ini("Organiza os pontos em que alguém precisa decidir antes de o processo seguir, como aprovar um desconto ou um "
                           "contrato. Um approval process define cada passo, de quem pedir a aprovação e o que acontece em cada ponto. Há "
                           "duas formas: Classic Approval Processes e Flow Approval Processes.",
                           "Um desconto acima do padrão vai para aprovação do gestor antes de a cotação ser enviada. Enquanto espera, o "
                           "registro fica bloqueado para edição.",
                           E("src:help-produtos-platform", "src:help-approvals-classic", "src:help-flow-approvals-concepts"),
                           comece=["func:processos-de-aprovacao"]),
    "encadeamento": enc("A Ajuda reúne aprovações entre as ferramentas declarativas de automação. Flow Approval Processes usam stages e steps, "
                        "como as orquestrações de 'Flow e orquestração'. As ações de uma aprovação clássica, como atualizar campo e enviar "
                        "e-mail, são as mesmas das workflow rules de 'Mecanismos legados e migração'.",
                        E("src:help-produtos-platform", "src:help-flow-approvals-concepts", "src:help-approvals-classic")),
    "avancado": [
        av("decisao", "Classic ou Flow Approval Process", "A Ajuda apresenta Flow Approval Processes como alternativa moderna: interface baseada em "
           "flow, disparo por mudança de registro, roteamento dinâmico e log detalhado. O processo clássico é preso a um objeto e não aceita o "
           "objeto User; o baseado em flow aceita.", E("src:help-approvals-classic-considerations", "src:help-approvals-classic-prepare")),
        av("limite", "Limites do processo clássico", "Por org, até 1.000 processos ativos e 2.000 no total; por objeto, 300 ativos e 500 no total. "
           "Cada processo aceita 30 passos, 25 aprovadores por passo e 40 ações de cada tipo.", E("src:help-approvals-classic-limits")),
        av("atencao", "Depois de ativar, a estrutura trava", "Um processo clássico ativado não aceita incluir, excluir ou reordenar passos, nem mudar "
           "o comportamento de rejeição. Precisa de pelo menos um passo para ser ativado; a Ajuda recomenda testar em sandbox.",
           E("src:help-approvals-classic-manage")),
        av("seguranca", "Approval admins", "Quem tem Modify All Records no objeto ou Modify All Data aprova ou rejeita pedidos sem fazer parte do "
           "processo e edita registros bloqueados para aprovação.", E("src:help-approvals-classic-manage")),
        av("atencao", "Flow approval process sem approval step", "Sem nenhum approval step, a submissão é sempre aprovada. Atualizações de registros "
           "relacionados vão num background step depois do approval step. Cada condição de início ou de conclusão aceita até 10 requirements.",
           E("src:help-flow-approvals-steps", "src:help-flow-approvals-considerations")),
        av("implantacao", "Como metadado", "O processo clássico é o metadata type ApprovalProcess: arquivos com sufixo .approvalProcess na pasta "
           "approvalProcesses. O metadado não guarda a ordem dos processos ativos, então pode ser preciso reordená-los depois do deploy. "
           "Implantar um processo sem entry criteria sobre um que já tem mantém os critérios antigos.", E("src:mdapi-approvalprocess")),
    ],
}
S["sub:acoes-e-regras"] = {
    "para_iniciantes": ini("Reúne ações reutilizáveis e regras que disparam comportamento: definir automaticamente o dono de leads e casos, "
                           "escalonar casos e oferecer botões de ação.",
                           "Casos com prioridade alta vão para a fila de nível 1; leads do site vão para a equipe de inbound.",
                           E("src:help-assign-setup", "src:help-escalation-setup", "src:help-quick-actions"),
                           comece=["func:regras-de-atribuicao", "func:regras-de-resposta-automatica", "func:acoes-rapidas"]),
    "encadeamento": enc("São três tipos de regra para leads e casos: atribuição define o dono, resposta automática envia o primeiro e-mail e "
                        "escalonamento sobe o caso parado. Ações rápidas também aparecem em Interface, como botões; as regras também servem a "
                        "Vendas e Atendimento.", E("src:help-quick-actions", "src:help-assign-guide", "src:help-case-rules-overview")),
    "avancado": [
        av("limite", "Uma regra ativa por tipo", "Só uma regra de atribuição de cada tipo fica ativa por vez, e uma regra de atribuição de casos "
           "aceita até 3.000 entradas, incluindo 300 de fórmula. O mesmo vale para resposta automática: uma regra ativa para leads e uma para "
           "casos.", E("src:help-assign-guide", "src:help-auto-response-setup")),
        av("atencao", "A primeira entrada que casar vence", "Numa regra de resposta automática, as entradas são avaliadas em ordem e a regra para "
           "na primeira que casar. A ordem das entradas faz parte da lógica.", E("src:help-auto-response-setup")),
        av("decisao", "Resposta automática ou alerta de e-mail", "A regra de resposta automática roda só na criação e responde a quem abriu o caso "
           "ou enviou o lead. Para avisar outras pessoas, ou reagir a edições, o caminho é outro: alerta de e-mail de workflow, hoje feito em "
           "Flow.", E("src:help-auto-response-vs-workflow", "src:help-wf-pb-eos")),
        av("implantacao", "Como metadado", "Cada tipo de regra é um metadata type com um arquivo por objeto: AssignmentRules, EscalationRules e "
           "AutoResponseRules (por exemplo Case.autoResponseRules). Dentro do arquivo ficam as regras e, em cada regra, as entradas em ordem.",
           E("src:mdapi-autoresponserules", "src:mdapi-assignmentrules", "src:mdapi-escalationrules")),
    ],
}
S["sub:automacao-apex"] = {
    "para_iniciantes": ini("Cobre triggers e classes Apex que automatizam processos quando as ferramentas declarativas não bastam. Um trigger "
                           "é código Apex que roda antes ou depois de um registro ser inserido, alterado ou excluído.",
                           "Um trigger grava o pedido e precisa avisar o ERP; a chamada externa tem de vir antes da gravação ou ir para um processo assíncrono.",
                           E("src:apex-callout-limits", "src:help-produtos-platform", "src:apex-triggers"), comece=["func:apex-triggers"]),
    "encadeamento": enc("Triggers e record-triggered flows reagem à mesma gravação e têm posição definida na ordem de execução. Apex que roda "
                        "depois, em fila ou agendado, fica em 'Execução assíncrona, lotes e agendamento'; testes e deploy ficam em "
                        "'Desenvolvimento, testes e entrega'.", E("src:apex-async-overview", "src:apex-triggers-order")),
    "avancado": [
        av("atencao", "Ordem de execução ao salvar", "Ao salvar um registro, a plataforma segue uma ordem fixa: os record-triggered flows before-save "
           "rodam antes dos before triggers, e as workflow rules vêm mais adiante. Quem mistura flow, trigger e regra no mesmo objeto precisa "
           "conhecer essa ordem.", E("src:apex-triggers-order")),
        av("escala", "Todo trigger é em massa", "Um trigger pode receber vários registros de uma vez, em importações, Bulk API e ações em massa. O "
           "código deve sempre ser escrito para mais de um registro.", E("src:apex-triggers-bulk")),
        av("implantacao", "Trigger exige teste", "Para implantar, 75% do código Apex precisa de cobertura de testes, e todo trigger precisa de alguma "
           "cobertura. A recomendação é testar em massa, com pelo menos 20 registros.", E("src:apex-testing-best-practices")),
        av("implantacao", "Como metadado", "Cada trigger é um componente ApexTrigger, com dois arquivos na pasta triggers: o código-fonte .trigger e "
           "o arquivo de metadado, que guarda a versão da API e o status (Active, Inactive ou Deleted).", E("src:mdapi-apextrigger")),
        av("limite", "Callouts por transação", "Até 100 callouts por transação, e a soma dos timeouts não passa de 120 segundos.", E("src:apex-callout-limits")),
        av("atencao", "Ordem dentro da transação", "Não é possível fazer callout depois de DML, Apex assíncrono, Apex agendado ou envio de e-mail pendentes na mesma transação; antes deles, pode.",
           E("src:apex-callout-limits")),
    ],
}

# ------------------------------------------------------------------ Interface (sub:lightning-pages-e-componentes está em conteudo_temas.py)
S["sub:aplicativos-e-navegacao"] = {
    "para_iniciantes": ini("Um app reúne as abas e ferramentas de um tipo de trabalho. Apps de console abrem vários registros ao mesmo tempo, em abas e subabas.",
                           "No Service Console, o caso abre numa aba, e o contato e a conta relacionados abrem em subabas.",
                           E("src:help-console-intro", "src:help-custom-tabs"), comece=["func:apps-de-console", "func:tabs"]),
    "encadeamento": enc("É a moldura da Interface: dentro do app ficam as abas, e cada aba leva a uma página.", E("src:help-custom-tabs")),
    "avancado": [av("atencao", "Permissão e atribuição do console", "Usar um app de console exige a permissão Lightning Console User e o perfil atribuído ao app. "
                    "O Service Console é atribuído automaticamente a todos os perfis; ajuste as atribuições.", E("src:help-console-create"))],
}
S["sub:tabs"] = {
    "para_iniciantes": ini("Tabs são entradas de navegação para objetos, páginas, componentes ou endereços.",
                           "A tab 'Contratos de Serviço' no app de Operações.", E("src:help-custom-tabs", "src:mdapi-customtab"), comece=["func:tabs"]),
    "encadeamento": enc("Fica entre o app e a página: a aba é o caminho até um objeto, uma Lightning page, um componente ou um endereço.", E("src:help-custom-tabs")),
    "avancado": [av("implantacao", "Tab como metadado", "Cada tab é um componente CustomTab; as edições disponíveis variam por tipo de tab.",
                    E("src:mdapi-customtab", "src:help-custom-tabs"))],
}
S["sub:layouts-e-paginas-de-registro"] = {
    "para_iniciantes": ini("Define como a página de um registro se organiza: quais campos e seções aparecem e em que ordem. Pode ser feito pelo "
                           "page layout ou, nos objetos que suportam, com Dynamic Forms na Lightning page.",
                           "Na página de uma oportunidade, uma seção de campos só aparece quando faz sentido para a etapa atual.",
                           E("src:help-lightning-pages", AF), comece=["func:lightning-pages", "func:tipos-de-registro"]),
    "encadeamento": enc("Cada tipo de registro pode ter a sua página; a página é montada com componentes, tema de 'Lightning pages e componentes'.",
                        E("src:mdapi-recordtype", "src:help-lightning-pages")),
    "avancado": [
        av("decisao", "Dynamic Forms para um único objeto", "Para criar, editar ou ver um único objeto na página de registro, o guia de decisão indica Dynamic "
           "Forms; ele não está disponível em páginas do Experience Cloud.", E(AF)),
        av("seguranca", "Layout não é segurança", "Page layout e segurança de campo se combinam e vale a configuração mais restritiva; a segurança de campo prevalece.",
           E("src:security-fls")),
    ],
}
S["sub:acoes-rapidas"] = {
    "para_iniciantes": ini("Ações rápidas são botões que abrem um formulário curto ou executam uma ação no contexto de um registro ou da navegação global.",
                           "'Registrar renovação' a partir de um contrato, abrindo um flow.", E("src:help-quick-actions", "src:mdapi-quickaction"),
                           comece=["func:acoes-rapidas"]),
    "encadeamento": enc("Aparecem na página do registro ou na navegação global; o que executam pode ser um formulário, um flow ou um componente.",
                        E("src:help-quick-actions", "src:mdapi-quickaction")),
    "avancado": [av("implantacao", "Metadado e objeto de consulta", "A ação é implantada como QuickAction e consultada pela Tooling API como QuickActionDefinition.",
                    E("src:mdapi-quickaction", "src:tooling-quickactiondefinition"))],
}
S["sub:orientacao-visual-e-path"] = {
    "para_iniciantes": ini("O Path é uma barra visual de etapas baseada num campo picklist, com campos e orientação para cada etapa.",
                           "Etapas de um contrato: Rascunho, Em análise, Assinado.", E("src:mdapi-pathassistant", "src:help-path-create"), comece=["func:path"]),
    "encadeamento": enc("Depende de um campo picklist ('Listas de valores') e aparece na página do registro.", E("src:mdapi-pathassistant")),
    "avancado": [av("atencao", "Um Path por combinação", "Existe um Path por combinação de objeto, picklist e tipo de registro.", E("src:help-path-create"))],
}
S["sub:acessibilidade-e-personalizacao"] = {
    "para_iniciantes": ini("Ajusta a aparência da interface, com temas e a marca da empresa, entre os tópicos de personalização da interface do guia de configuração.",
                           "A empresa aplica um tema com as suas cores e o seu logotipo.", E("src:help-setup-company")),
    "encadeamento": enc("Completa Interface com a camada visual; idioma e localidade ficam em Organização.", E("src:help-setup-company")),
}

# ------------------------------------------------------------------ Execução assíncrona
S["sub:batch"] = {
    "para_iniciantes": ini("Batch Apex processa grandes volumes de registros dividindo o trabalho em lotes. A classe tem três métodos: start "
                           "coleta os registros, execute processa um lote de cada vez e finish roda no fim.",
                           "Recalcular um campo em todas as contas da org durante a madrugada.",
                           E("src:apex-async-overview", "src:apex-batch-use", "src:apex-batch"), comece=["func:batch-apex"]),
    "encadeamento": enc("O agendamento dispara execuções em horário definido, e o andamento fica em 'Monitoramento de jobs e limites'.",
                        E("src:apex-async-overview", "src:apex-batch-use")),
    "avancado": [
        av("limite", "Fila do Batch Apex", "No máximo cinco jobs de batch em fila ou ativos ao mesmo tempo. A Apex flex queue segura até 100 "
           "outros em Holding; quando há recursos, eles saem do topo da fila e passam a Queued. Com a flex queue cheia, o envio de um job "
           "novo dá erro de limite.", E("src:apex-batch", "src:help-apex-flex-queue", "src:apex-batch-use")),
        av("escala", "Tamanho do lote", "Por padrão, os registros são entregues em lotes de 200. Quando start devolve um QueryLocator, o "
           "tamanho pode ir até 2.000. Os governor limits recomeçam a cada lote.", E("src:apexref-database", "src:apex-batch-use", "src:apex-gov-limits")),
        av("limite", "Limite de 24 horas", "250.000 execuções de método de batch por 24 horas, ou licenças de usuário vezes 200, o que for "
           "maior. Contam as execuções de start, execute e finish.", E("src:apex-batch-use")),
        av("implantacao", "Como acompanhar", "Database.executeBatch devolve o Id de um registro AsyncApexJob, que mostra o estado, os lotes "
           "processados e os que falharam. Na interface: Setup, Apex Jobs. Um batch também pode ser agendado para rodar uma vez, com "
           "System.scheduleBatch.", E("src:apex-batch-use", "src:objref-asyncapexjob", "src:apexref-system")),
        av("testes", "Em teste", "Num teste em execução, dá para submeter no máximo 5 jobs de batch.", E("src:apex-batch-use")),
    ],
}
S["sub:queueable"] = {
    "para_iniciantes": ini("Queueable Apex coloca uma tarefa na fila para rodar em segundo plano quando houver recursos. Devolve um identificador "
                           "para acompanhar o job e permite encadear tarefas.",
                           "Depois de salvar um pedido, a chamada ao ERP vai para a fila e roda em seguida, sem prender a tela.",
                           E("src:apex-queueable", "src:apex-async-overview"), comece=["func:queueable-apex"]),
    "encadeamento": enc("É o caminho recomendado no lugar dos future methods. O acompanhamento fica em 'Monitoramento de jobs e limites'.",
                        E("src:apex-queueable", "src:apex-future")),
    "avancado": [
        av("decisao", "Queueable no lugar de future", "A Salesforce recomenda Queueable Apex no lugar de future methods: aceita tipos complexos, "
           "encadeia jobs e devolve um Id para acompanhar o trabalho.", E("src:apex-queueable", "src:apex-async-overview", "src:apex-future")),
        av("limite", "Quantos jobs por transação", "Uma transação síncrona enfileira até 50 jobs com System.enqueueJob; uma transação "
           "assíncrona, só 1. É por isso que, dentro de um job, o encadeamento é de um job por vez.", E("src:apex-gov-limits")),
        av("atencao", "Cadeias precisam de freio", "Numa cadeia de jobs, a documentação pede um mecanismo para frear ou parar; sem ele, "
           "chega-se rápido ao limite diário de Apex assíncrono. Dá para definir a profundidade máxima da pilha; em orgs Developer Edition e "
           "Trial, o máximo é 5.", E("src:apex-queueable", "src:apexref-system")),
        av("implantacao", "Atraso ao enfileirar", "System.enqueueJob aceita um atraso mínimo de 0 a 10 minutos, ignorado em testes. O "
           "metadata type ApexSettings guarda um atraso mínimo padrão da org para jobs enfileirados sem atraso próprio (DefaultQueueableDelay, "
           "de 1 a 600 segundos).", E("src:apexref-system", "src:mdapi-apexsettings")),
        av("escala", "Limites maiores", "Alguns governor limits são maiores do que no Apex síncrono, como o de heap.", E("src:apex-queueable")),
    ],
}
S["sub:future-e-mecanismos-legados"] = {
    "para_iniciantes": ini("Future methods rodam um método em segundo plano para não atrasar a transação. A Salesforce recomenda substituí-los por Queueable.",
                           "Um método marcado como future faz uma chamada demorada sem atrasar a gravação que o disparou.",
                           E("src:apex-async-overview", "src:apex-queueable", "src:apex-future"), comece=["func:future-methods"]),
    "encadeamento": enc("Fica aqui para quem mantém código existente; para código novo, veja Queueable.", E("src:apex-queueable", "src:apex-future")),
    "avancado": [
        av("limite", "Regras do método", "O método precisa ser static e void. Os parâmetros são tipos primitivos, arrays ou coleções de "
           "primitivos: não aceita sObjects nem objetos.", E("src:apex-future")),
        av("atencao", "De onde não se chama", "Não se chama um future method a partir de um batch ou de outro future. Em contexto queueable, o "
           "limite é de 50 chamadas por invocação; a documentação não recomenda abrir muitos future methods a partir de um job enfileirado.",
           E("src:apex-future")),
        av("decisao", "Para que ainda serve", "Além de callouts, a documentação cita o uso para isolar operações DML em tipos diferentes de "
           "objeto e evitar o erro de mixed DML. Queueable cobre os mesmos usos.", E("src:apex-future")),
        av("limite", "Limite de 24 horas", "250.000 execuções por 24 horas, ou licenças de usuário vezes 200, o que for maior.", E("src:apex-future")),
    ],
}
S["sub:agendamento"] = {
    "para_iniciantes": ini("Scheduled Apex roda uma classe em horário definido, como uma rotina diária ou semanal. Flows também podem ser disparados por agendamento.",
                           "Todo domingo, uma rotina gera os lembretes da semana.",
                           E("src:apex-async-overview", "src:mdapi-flow", "src:apex-scheduler"), comece=["func:apex-agendado", "func:flow"]),
    "encadeamento": enc("Horários comerciais, que contam prazos de atendimento, são outro assunto, em Organização.", E("src:help-bh")),
    "avancado": [
        av("implantacao", "Duas formas de agendar", "A classe implementa a interface Schedulable. Agenda-se pela tela Schedule Apex (Setup, Apex "
           "Classes) ou por código, com System.schedule, que recebe o nome do job, uma expressão cron e a classe.",
           E("src:apex-scheduler", "src:help-schedule-apex", "src:apexref-system")),
        av("limite", "Quantos jobs", "Só pode haver 100 jobs de Apex agendado ao mesmo tempo. A contagem se vê na página Scheduled Jobs ou "
           "consultando CronTrigger e CronJobDetail.", E("src:apex-scheduler", "src:objref-cronjobdetail")),
        av("atencao", "O horário não é garantia", "A plataforma agenda a classe para o horário pedido, mas a execução real pode atrasar "
           "conforme a disponibilidade do serviço.", E("src:apex-scheduler", "src:help-schedule-apex")),
        av("seguranca", "Roda como system", "O agendador roda como system: a classe executa, tenha ou não o usuário permissão para executá-la.",
           E("src:help-schedule-apex")),
        av("atencao", "Classe presa por job ativo", "Com um job agendado ativo, a classe e as classes que ela referencia não podem ser "
           "atualizadas pela interface; há uma opção para liberar a atualização por deploy.", E("src:apex-scheduler")),
        av("escala", "Limites síncronos", "Embora assíncrono, o Apex agendado usa os limites síncronos por transação. É comum a classe agendada "
           "apenas iniciar um batch: a documentação cita o agendamento como ideal para manutenção diária ou semanal com Batch Apex.",
           E("src:apex-gov-limits", "src:apex-scheduler")),
        av("limite", "Flows agendados", "Schedule-triggered flows têm teto de 250.000 entrevistas por 24 horas, ou licenças de usuário vezes "
           "200, o que for maior; cada registro devolvido pela consulta do flow cria uma entrevista.", E("src:help-flow-schedule-triggered")),
    ],
}
S["sub:processamento-orientado-a-eventos"] = {
    "para_iniciantes": ini("Reage, dentro da org, a eventos publicados no barramento: um trigger ou automação assina o evento e faz o trabalho quando ele chega.",
                           "Um ERP publica PedidoFaturado__e; um trigger Apex assina o evento e atualiza a oportunidade.",
                           E("src:help-platform-events-define", "src:mdapi-platformeventsubscriberconfig"), comece=["func:platform-events"]),
    "encadeamento": enc("A publicação e o transporte do evento ficam em 'Eventos e mensageria', no tema de integração.", E("src:help-platform-events-define")),
    "avancado": [av("atencao", "Retentativa em triggers de evento", "Um trigger de evento roda no máximo 10 vezes; a retentativa reenvia o lote inteiro e "
                    "desfaz o DML anterior. Limite as tentativas a menos de nove e tenha uma ação alternativa.", E("src:pe-retry-apex"))],
}
S["sub:monitoramento-de-jobs-e-limites"] = {
    "para_iniciantes": ini("Acompanha as execuções assíncronas: em que estado está cada job e quanto dos limites já foi usado. Há três telas no "
                           "Setup (Apex Jobs, Apex Flex Queue e Scheduled Jobs) e três objetos consultáveis por API.",
                           "Um job enfileirado é acompanhado na tela Apex Jobs ou consultando AsyncApexJob pelo identificador devolvido.",
                           E("src:apex-queueable", "src:apex-async-overview", "src:help-apex-job-queue", "src:help-apex-flex-queue"),
                           comece=["func:monitoramento-de-jobs-apex"]),
    "encadeamento": enc("Completa os mecanismos do tema; o consumo geral da org fica em Observabilidade.", E("src:apex-async-overview", "src:rest-limits")),
    "avancado": [
        av("implantacao", "O que cada tela mostra", "Apex Jobs lista os jobs dos últimos sete dias e o uso do limite de 24 horas de Apex "
           "assíncrono. Apex Flex Queue lista os batches em Holding e permite reordená-los. Scheduled Jobs lista os jobs agendados. Um job "
           "agendado aparece em duas telas, mas conta uma vez só no limite.",
           E("src:help-apex-job-queue", "src:help-apex-flex-queue", "src:help-apex-code-overview")),
        av("implantacao", "Os mesmos dados por API", "AsyncApexJob guarda os jobs Apex, com tipo, estado e lotes processados; serve para "
           "consultar o que saiu da tela, que só mostra sete dias. CronTrigger guarda a agenda de cada job agendado, e CronJobDetail, o "
           "nome e o tipo. Pela REST API, o recurso de limites traz o rótulo DailyAsyncApexExecutions.",
           E("src:objref-asyncapexjob", "src:objref-crontrigger", "src:objref-cronjobdetail", "src:rest-limits", "src:help-apex-job-queue")),
        av("atencao", "Nomes que confundem na tela", "Na coluna Job Type, future methods e classes Queueable ainda não executados aparecem como "
           "Future. Em AsyncApexJob, os tipos BatchApexWorker e TestWorker são de uso interno: ao consultar um batch, filtre BatchApexWorker.",
           E("src:help-apex-job-queue", "src:help-kb-asyncapexjob-types")),
        av("limite", "Quando o limite estoura", "Acima do limite de 24 horas de jobs assíncronos ou do limite de jobs agendados, jobs novos são "
           "rejeitados. A opção de limites elásticos, em Beta, processa o excedente em ritmo reduzido; em ApexSettings, o campo é "
           "enableAsyncApexElasticExecutions.", E("src:help-org-health", "src:apex-elastic-limits", "src:mdapi-apexsettings")),
        av("limite", "Fila do Batch Apex", "No máximo cinco jobs de batch em fila ou ativos, com uma Apex flex queue de até 100 jobs adicionais.",
           E("src:apex-async-overview", "src:help-apex-flex-queue")),
        av("seguranca", "Permissão para consultar", "Fora do system mode, acessar AsyncApexJob exige a permissão View Setup and Configuration.",
           E("src:objref-asyncapexjob")),
    ],
}

# ------------------------------------------------------------------ Integração
S["sub:apis-de-dados-e-metadados"] = {
    "para_iniciantes": ini("São as portas de entrada da org para outros sistemas: REST e SOAP para dados, Bulk API para grandes volumes, "
                           "Metadata API para configuração e Tooling API para ferramentas de desenvolvimento.",
                           "Um app de pedidos busca uma conta por Id e cria uma oportunidade com duas requisições HTTP; com o recurso Composite, as duas viram uma só chamada.",
                           E("src:rest-intro", "src:soap-intro", "src:bulk-api-intro", "src:mdapi-intro", "src:tooling-intro", "src:rest-composite"),
                           comece=["func:rest-api", "func:bulk-api"]),
    "encadeamento": enc("Toda chamada precisa de autenticação ('Autenticação de integrações') e consome alocações ('Contratos, limites e tratamento de falhas').",
                        E("src:rest-intro", "src:limits-api-requests")),
    "avancado": [
        av("decisao", "Qual API usar", "REST para HTTP simples; SOAP para contrato WSDL; Bulk API 2.0 acima de 2.000 registros; Metadata API para mover "
           "configuração; Tooling API para ferramentas que leem pedaços pequenos de metadados.",
           E("src:rest-intro", "src:soap-intro", "src:bulk-api-intro", "src:mdapi-intro", "src:tooling-intro")),
        av("atencao", "Enterprise WSDL muda com a org", "O Enterprise WSDL é tipado e específico da org: precisa ser gerado de novo quando objetos ou campos "
           "customizados mudam. O Partner WSDL é genérico.", E("src:soap-intro")),
        av("atencao", "CORS é para o navegador", "CORS libera o JavaScript de outras origens a chamar as APIs da org pelo navegador; não libera chamadas da org para fora.",
           E("src:help-cors")),
    ],
}
S["sub:autenticacao-de-integracoes"] = {
    "para_iniciantes": ini("É como um sistema externo prova quem é ao chamar a org: um connected app ou external client app registra a "
                           "integração, e o OAuth entrega tokens com escopos definidos.",
                           "Um sistema de BI se conecta por OAuth com a consumer key de um app que só usuários com um permission set podem usar.",
                           E("src:mdapi-connectedapp", "src:mdapi-externalclientapplication", "src:mdapi-oauthcustomscope"),
                           comece=["func:external-client-apps", "func:connected-apps"]),
    "encadeamento": enc("Depois de autenticada, a integração usa as APIs do tema. Nas chamadas da org para fora, a autenticação mora em credenciais externas.",
                        E("src:help-eca-create", "src:mdapi-externalcredential")),
    "avancado": [
        av("decisao", "External client app para integrações novas", "A Salesforce recomenda external client apps para integrações novas; a criação de "
           "connected apps está restrita desde o Spring '26. O external client app separa o que vai no pacote do que cada org define.",
           E("src:help-connected-app-basics", "src:mdapi-externalclientapplication")),
        av("atencao", "Permissão para usar external client apps", "Usar external client apps exige a permissão Opt in to External Client Apps; os plugins de "
           "mobile, push e notificação são piloto ou beta.", E("src:help-eca-create", "src:mdapi-externalclientapplication")),
        av("seguranca", "Escopos e troca de token", "Escopos customizados refinam o que cada app pode fazer, e handlers Apex de troca de token aceitam tokens de "
           "provedores externos; há configurações para bloquear fluxos ou exigir PKCE.",
           E("src:mdapi-oauthcustomscope", "src:mdapi-oauthtokenexchangehandler", "src:mdapi-oauthoidcsettings")),
    ],
}
S["sub:chamadas-externas-e-endpoints"] = {
    "para_iniciantes": ini("Cobre as chamadas que a org faz para serviços de fora e os endereços liberados para isso: sites remotos, sites "
                           "confiáveis para conteúdo, serviços externos importados por OpenAPI e conexões privadas.",
                           "A especificação da API de frete é registrada; a operação calcularFrete vira uma ação usada num Screen Flow.",
                           E("src:help-remote-site", "src:help-trusted-urls", "src:help-external-services-register", "src:mdapi-outboundnetworkconnection"),
                           comece=["func:external-services", "func:remote-site-settings"]),
    "encadeamento": enc("A autenticação dessas chamadas fica em 'Credenciais'; os limites, em 'Contratos, limites e tratamento de falhas'.",
                        E("src:mdapi-namedcredential", "src:apex-callout-limits")),
    "avancado": [
        av("seguranca", "Named credential no lugar de site remoto", "Sites remotos só liberam o endereço; para callouts novos, a Salesforce recomenda named "
           "credentials, que guardam endereço e autenticação fora do código.", E("src:help-remote-site", "src:mdapi-namedcredential")),
        av("atencao", "Sites confiáveis são outra lista", "Sites confiáveis (CSP) liberam conteúdo carregado pelas páginas da org, como scripts e imagens; não "
           "liberam callouts.", E("src:help-trusted-urls")),
        av("atencao", "Versão nova de serviço externo", "Em serviços externos, systemVersion é somente leitura e não é atualizado no lugar: uma versão nova da "
           "especificação exige novo registro.", E("src:mdapi-externalserviceregistration")),
        av("limite", "Callouts por transação", "Até 100 callouts por transação, com soma de timeouts de até 120 segundos.", E("src:apex-callout-limits")),
    ],
}
S["sub:credenciais"] = {
    "para_iniciantes": ini("Named credentials guardam o endereço de um sistema externo e a forma de se autenticar nele, fora do código.",
                           "Um Flow chama 'callout:ERP/pedidos'; a named credential ERP guarda a URL, e a credencial externa associada guarda o OAuth.",
                           E("src:mdapi-namedcredential", "src:help-nc-create"), comece=["func:named-credentials"]),
    "encadeamento": enc("São usadas por Apex e Flow nas chamadas externas; os certificados usados nelas ficam em 'Credenciais, certificados e proteção de dados'.",
                        E("src:mdapi-namedcredential", "src:mdapi-certificate")),
    "avancado": [av("atencao", "Autenticação na credencial externa", "Desde a 56.0, a autenticação mora na credencial externa; named credentials do tipo "
                    "Legacy ainda usam os campos antigos.", E("src:mdapi-namedcredential", "src:mdapi-externalcredential"))],
}
S["sub:eventos-e-mensageria"] = {
    "para_iniciantes": ini("Eventos avisam outros sistemas quando algo acontece, sem consulta periódica: eventos de plataforma, eventos de "
                           "captura de alterações a cada mudança de registro, a Pub/Sub API para assinar de fora e o Event Relay para levar eventos à AWS.",
                           "AccountChangeEvent no canal ChangeEvents avisa um data warehouse a cada conta alterada.",
                           E("src:help-platform-events-define", "src:pubsub-qs-events", "src:pubsub-overview", "src:help-event-relay-create"),
                           comece=["func:platform-events", "func:change-data-capture"]),
    "encadeamento": enc("A reação dentro da org fica em 'Processamento orientado a eventos'; retentativas e monitoramento, em 'Contratos, limites e tratamento de falhas'.",
                        E("src:help-platform-events-define", "src:pe-retry-apex")),
    "avancado": [
        av("limite", "Pub/Sub API", "Cada evento tem no máximo 1 MB, cada pedido busca até 100 eventos e a org tem até 200 assinaturas gerenciadas; acima de "
           "4 MB por requisição, a chamada falha.", E("src:pubsub-allocations")),
        av("implantacao", "Excluir membro de canal", "PlatformEventChannelMember não aceita createMetadata() nem deleteMetadata(); a exclusão é feita via destructiveChanges.xml.",
           E("src:mdapi-platformeventchannelmember")),
        av("atencao", "Event Relay depois de criado", "Depois de criado, só o estado e a opção de retomada do Event Relay podem mudar.", E("src:mdapi-eventrelayconfig")),
    ],
}
S["sub:conectividade-e-virtualizacao-de-dados"] = {
    "para_iniciantes": ini("Mostra dados de outro sistema como objetos da org, consultados sob demanda e sem cópia.",
                           "Pedidos do ERP aparecem como objeto externo Pedido__x, lidos via OData no momento da consulta.",
                           E("src:help-external-data-source-odata", "src:mdapi-externaldatasource"), comece=["func:external-objects"]),
    "encadeamento": enc("A modelagem como objeto externo (__x) é detalhada em 'Modelos externos e especializações'.", E("src:mdapi-customobject")),
    "avancado": [av("decisao", "Consultar sob demanda em vez de copiar", "Objetos externos leem os dados no momento da consulta: permitem usá-los em listas, "
                    "relacionamentos e relatórios sem manter uma cópia na org.", E("src:help-external-data-source-odata"))],
}
S["sub:contratos-limites-e-tratamento-de-falhas"] = {
    "para_iniciantes": ini("Reúne as regras do 'contrato' de uma integração: quantas chamadas cabem por dia, quanto tempo cada uma pode levar, "
                           "quais versões de API continuam valendo e como tratar falhas e retentativas.",
                           "Uma org Enterprise com 15 licenças Salesforce tem 115.000 requisições por 24 horas (100.000 + 15 × 1.000), segundo o exemplo da documentação.",
                           E("src:limits-api-requests", "src:rest-versions", "src:pe-retry-apex"),
                           comece=["func:limites-de-api-e-alocacoes", "func:versoes-de-api"]),
    "encadeamento": enc("Vale para todas as APIs e eventos do tema; o consumo também aparece em Observabilidade.", E("src:rest-limits")),
    "avancado": [
        av("limite", "Alocação diária e tempo de chamada", "O limite diário vale para a org inteira, não por usuário. Requisições de 20 segundos ou mais têm "
           "limite de simultaneidade (25 em produção e sandbox), e chamadas REST e SOAP expiram após 10 minutos.", E("src:limits-api-requests")),
        av("atencao", "Versões em descontinuação", "As versões 31.0 a 40.0 ficam sem suporte a partir do Summer '27 e são aposentadas no Summer '28; versões "
           "aposentadas respondem 410:GONE.", E("src:rest-api-eol")),
        av("atencao", "Bulk API sem SLA", "Não há SLA garantido para a Bulk API 1.0 nem para a 2.0; jobs terminados há mais de 7 dias são apagados.",
           E("src:limits-bulk-api", "src:bulk-api-intro")),
    ],
}

# ------------------------------------------------------------------ Relatórios
S["sub:reports"] = {
    "para_iniciantes": ini("Relatórios analisam os registros da org para responder uma pergunta, como quantas oportunidades estão em cada etapa.",
                           "Um relatório de oportunidades por etapa mostra onde os negócios estão parados.", E("src:help-produtos-analytics")),
    "encadeamento": enc("Dashboards mostram relatórios em gráficos.", E("src:help-produtos-analytics")),
}
S["sub:dashboards"] = {
    "para_iniciantes": ini("Dashboards mostram, em gráficos, os resultados de relatórios para acompanhar indicadores e compartilhar resultados.",
                           "Um painel com as vendas do trimestre por vendedor.", E("src:help-produtos-analytics")),
    "encadeamento": enc("Dependem de relatórios; a personalização de relatórios e dashboards aparece também no guia de configuração da org.",
                        E("src:help-produtos-analytics", "src:help-setup-company")),
}
S["sub:recursos-analiticos-de-produto"] = {
    "para_iniciantes": ini("São produtos analíticos que vão além dos relatórios nativos e dependem de licença, como CRM Analytics, Tableau e Tableau Next.",
                           "Uma equipe combina dados da Salesforce com outras fontes no Tableau.", E("src:help-produtos-analytics")),
    "encadeamento": enc("Ficam ao lado de Reports e Dashboards, que são nativos.", E("src:help-produtos-analytics")),
}

# ------------------------------------------------------------------ Conteúdo
S["sub:files-e-documentos"] = {
    "para_iniciantes": ini("São os arquivos ligados a registros. Cada arquivo tem versões e pode ser ligado a vários registros.",
                           "O contrato assinado é ligado à conta e, quando revisado, ganha uma nova versão.", E("src:data-model-files")),
    "encadeamento": enc("Bibliotecas e pastas organizam e compartilham esses arquivos.", E("src:data-model-files")),
    "avancado": [av("decisao", "Documento, versão e vínculo", "O arquivo (Content Document) tem versões (Content Version) e se liga a registros por Content "
                    "Document Link. Isso importa em migrações e em consultas por API.", E("src:data-model-files"))],
}
S["sub:bibliotecas-e-assets"] = {
    "para_iniciantes": ini("Bibliotecas e pastas organizam arquivos e controlam quem tem acesso a eles.",
                           "Uma biblioteca de materiais de venda fica disponível só para o time comercial.", E("src:data-model-files")),
    "encadeamento": enc("Organizam os arquivos de 'Files e documentos'.", E("src:data-model-files")),
}
S["sub:knowledge-e-categorias"] = {
    "para_iniciantes": ini("É a base de artigos de conhecimento para atendentes e clientes.",
                           "Um artigo 'Como trocar a senha' é sugerido ao atendente e publicado no portal.", E("src:help-lk-enable", "src:help-service-basics"),
                           comece=["func:lightning-knowledge"]),
    "encadeamento": enc("Também aparece em Atendimento, onde ajuda a responder casos.", E("src:help-service-basics")),
    "avancado": [av("atencao", "Habilitar não tem volta", "Habilitar o Lightning Knowledge é irreversível e muda o modelo de dados para tipos de registro; exige "
                    "ao menos um tipo de artigo.", E("src:help-lk-enable"))],
}

# ------------------------------------------------------------------ Desenvolvimento
S["sub:codigo-e-bundles"] = {
    "para_iniciantes": ini("Reúne os componentes de código da org: classes Apex, Lightning web components, Aura components, páginas e "
                           "componentes Visualforce e static resources. Cada um é um componente de metadado com arquivos próprios.",
                           "Um Lightning web component é uma pasta com o HTML, o JavaScript e o arquivo .js-meta.xml, que diz em que páginas ele pode ser usado.",
                           E("src:mdapi-apexclass", "src:mdapi-lightningcomponentbundle", "src:lwc-config-file", "src:lwc-migrate-bundles"),
                           comece=["func:classes-apex", "func:lightning-web-components"]),
    "encadeamento": enc("Triggers Apex também são código, mas ficam em 'Automação Apex'. O formato dos arquivos fica em 'Source format e "
                        "Metadata API format'; os testes, em 'Testes'; a entrega, em 'Versionamento, deploy e recuperação'.",
                        E("src:mdapi-apextrigger", "src:sdr-registry", "src:mdapi-intro")),
    "avancado": [
        av("implantacao", "Código tem dois arquivos", "Classes Apex, triggers, páginas e componentes Visualforce e static resources estendem "
           "MetadataWithContent: cada componente tem o arquivo de conteúdo e, ao lado, um arquivo de metadado. ApexClass é suportado por "
           "todas as chamadas da Metadata API, exceto as CRUD-based.", E("src:mdapi-apexclass", "src:mdapi-apexpage", "src:mdapi-staticresource")),
        av("implantacao", "Bundles são pastas", "LightningComponentBundle e AuraDefinitionBundle são pastas com vários arquivos. No LWC, o "
           "arquivo .js-meta.xml é obrigatório. Num bundle Aura, controller, helper e renderer são arquivos .js separados; no LWC, viram um só.",
           E("src:mdapi-lightningcomponentbundle", "src:mdapi-auradefinitionbundle", "src:lwc-config-file", "src:lwc-migrate-bundles")),
        av("decisao", "Tooling API ou Metadata API", "A Tooling API serve a ferramentas que leem e alteram pedaços pequenos de metadados; a Metadata "
           "API move o modelo completo.", E("src:tooling-intro", "src:mdapi-intro")),
        av("atencao", "Classe com jobs ativos", "Por padrão, o deploy não atualiza uma classe que tem jobs Apex ativos. As saídas são cancelar os "
           "jobs ou liberar a opção em Deployment Settings. O metadata type DeploymentSettings guarda a opção que pula a validação de Apex "
           "assíncrono.", E("src:mdapi-apexclass", "src:mdapi-deploymentsettings")),
        av("limite", "Tamanhos", "Um static resource tem até 5 MB, e a org, até 250 MB de static resources. O arquivo JavaScript de um "
           "Lightning web component tem até 1 MB.", E("src:lwc-third-party")),
        av("seguranca", "Opções de segurança de Apex", "ApexSettings guarda opções que afetam a segurança: por exemplo, impedir usuários guest "
           "de rodar Apex anônimo (ligado por padrão) e permitir que classes Apex acessem metadados pelo namespace Metadata (desligado por padrão).",
           E("src:mdapi-apexsettings")),
        av("implantacao", "Dependência de pacote registrada no código", "Classes, triggers, páginas e componentes Visualforce e bundles Aura "
           "registram, em packageVersions, as versões de pacotes gerenciados instalados que referenciam.",
           E("src:mdapi-apexclass", "src:mdapi-auradefinitionbundle")),
    ],
}
S["sub:testes"] = {
    "para_iniciantes": ini("Cobre os testes automatizados. Testes Apex são métodos de classes anotadas com @IsTest; a plataforma mede a "
                           "cobertura e exige um mínimo para implantar. Testes Jest conferem Lightning web components fora da org.",
                           "Um deploy para produção roda os testes locais; se um falha, nada é implantado.",
                           E("src:apex-writing-tests", "src:apex-code-coverage", "src:lwc-testing", "src:migration-running-tests"),
                           comece=["func:testes-apex", "func:testes-jest-de-lwc"]),
    "encadeamento": enc("Os testes rodam nos ambientes de 'Ambientes e sandboxes' e fazem parte do deploy, em 'Versionamento, deploy e recuperação'.",
                        E("src:migration-running-tests", "src:sfdx-dev-guide")),
    "avancado": [
        av("limite", "75% de cobertura", "Para implantar ou empacotar Apex, os testes precisam cobrir ao menos 75% do código Apex da org e "
           "passar. Chamadas a System.debug e as próprias classes e métodos de teste não contam. Cobertura indica, mas não garante, que o "
           "teste é eficaz.", E("src:apex-code-coverage", "src:apex-testing-best-practices", "src:sfdx-run-apex-tests")),
        av("testes", "Que testes rodam num deploy", "Sem nível de teste informado, um deploy para produção com classes ou triggers Apex roda "
           "todos os testes locais; sem componentes Apex, nenhum. Fora de produção, por padrão nenhum teste roda. Os níveis são NoTestRun, "
           "RunSpecifiedTests, RunLocalTests e RunAllTestsInOrg; NoTestRun só vale em ambientes de desenvolvimento.",
           E("src:migration-running-tests", "src:migration-run-local-tests", "src:cli-deploy-validate")),
        av("testes", "Unitário ou de interface", "Só LWC permite testes unitários escritos, com Jest; Dynamic Forms e Screen Flow dependem de "
           "automação de interface de ponta a ponta. Testes que dependem do HTML e do DOM do Lightning Experience pedem manutenção contínua, "
           "porque essa estrutura pode mudar.", E(AF, "src:lwc-testing", "src:lwc-e2e")),
        av("implantacao", "Como metadado", "ApexTestSuite agrupa classes de teste para rodar juntas. ApexSettings guarda opções de execução, "
           "como rodar os testes em série (enableDisableParallelApexTesting, em que true quer dizer em série). Os testes Jest ficam na pasta "
           "__tests__ do componente, no controle de versão, e não vão para a org.",
           E("src:mdapi-apextestsuite", "src:mdapi-apexsettings", "src:lwc-component-tests", "src:lwc-jest-create")),
        av("escala", "Execuções grandes", "Em orgs com muitas classes, a opção Store Only Aggregate Code Coverage (Setup, Apex Test Execution, "
           "Options) desliga a cobertura por classe e acelera a coleta. Os testes de um deploy sempre rodam em série.",
           E("src:sfdx-run-apex-tests", "src:mdapi-apexsettings")),
    ],
}
S["sub:pacotes-e-dependencias"] = {
    "para_iniciantes": ini("Um pacote é um contêiner de metadados relacionados, instalado e atualizado como uma unidade. Cada mudança no "
                           "conteúdo gera uma nova versão. Um pacote pode declarar dependência de outros pacotes.",
                           "Uma equipe publica as customizações de atendimento como pacote desbloqueado; cada entrega é uma versão nova, instalada na sandbox e depois em produção.",
                           E("src:sfdx-unlocked-whats", "src:pkg2-key-concepts", "src:sfdx-package-dev-model", "src:sfdx-unlocked-intro"),
                           comece=["func:pacotes-desbloqueados", "func:pacotes-gerenciados"]),
    "encadeamento": enc("É uma das formas de entrega; as outras ficam em 'Versionamento, deploy e recuperação'. O empacotamento de segunda "
                        "geração é ligado no Dev Hub, descrito em 'Ambientes e sandboxes'.", E("src:sfdx-devhub-enable", AF)),
    "avancado": [
        av("decisao", "Desbloqueado ou gerenciado", "Para quem não distribui a vários clientes, a documentação indica pacotes desbloqueados. "
           "Pacotes gerenciados de segunda geração atendem parceiros que distribuem apps: usam o controle de versão como fonte da verdade e "
           "dispensam packaging org e patch org.", E("src:pkg2-intro", "src:sfdx-unlocked-intro")),
        av("implantacao", "O que pode ir em pacote", "Dynamic Forms, Screen Flows e LWC podem ir por pacotes gerenciados (1GP e 2GP), pacotes "
           "desbloqueados, change sets e DevOps Center; Omnistudio não aceita empacotamento.", E(AF)),
        av("implantacao", "Como metadado", "InstalledPackage instala ou atualiza, por deploy, pacotes gerenciados de primeira geração: precisa "
           "ser o único tipo do manifesto, e um deploy instala até 20 pacotes. Pacotes desbloqueados e gerenciados de segunda geração são "
           "instalados pelo Salesforce CLI. DevHubSettings liga o empacotamento de segunda geração.",
           E("src:mdapi-installedpackage", "src:mdapi-devhubsettings")),
        av("atencao", "Ligar não tem volta", "Depois de ligados, o Dev Hub e o empacotamento de segunda geração não podem ser desligados.",
           E("src:pkg2-enable-devhub")),
        av("atencao", "Mudança direta em produção", "No pacote desbloqueado, o metadado instalado pode ser alterado direto em produção. Um "
           "upgrade do pacote pode sobrescrever essas mudanças; a documentação pede que quem altera avise a equipe de desenvolvimento.",
           E("src:sfdx-unlocked-whats")),
    ],
}
S["sub:source-format-e-metadata-api-format"] = {
    "para_iniciantes": ini("Os metadados podem ser guardados em dois formatos de arquivo: o source format, usado em projetos do Salesforce CLI, e "
                           "o Metadata API format, usado pela Metadata API, que recebe e devolve um .zip com um manifesto package.xml.",
                           "Uma Lightning page fica em flexipages/<Nome>.flexipage no Metadata API format e ganha o sufixo -meta.xml no source format.",
                           E("src:sdr-registry", "src:sfdx-dev-guide", "src:sfdx-project-setup", "src:mdapi-zip-file"),
                           comece=["func:projeto-salesforce-dx"]),
    "encadeamento": enc("Cada ficha de metadata type mostra a pasta e o sufixo nos dois formatos. O deploy que usa esses arquivos fica em "
                        "'Versionamento, deploy e recuperação'.", E("src:sdr-registry")),
    "avancado": [
        av("implantacao", "Decomposição", "Decompor é dividir um XML grande em arquivos menores, por subtipo. Por padrão, o projeto sempre "
           "decompõe custom objects e custom object translations; outros tipos, como permission sets e custom labels, são opcionais e "
           "configurados em sfdx-project.json.", E("src:sfdx-decomposed")),
        av("implantacao", "Conversão entre formatos", "O Salesforce CLI converte nos dois sentidos: project convert mdapi leva de Metadata API "
           "format para source format, e project convert source faz o caminho inverso, para implantar pela Metadata API. O arquivo "
           ".forceignore lista o que fica fora.", E("src:sfdx-convert-mdapi", "src:cli-convert-source")),
        av("decisao", "Por que source format", "O source format é otimizado para trabalhar com controle de versão. As extensões do VS Code "
           "supõem esse formato, e o deploy pelo CLI o usa por padrão.", E("src:vscode-source-format", "src:cli-project-deploy-start")),
        av("atencao", "A versão da API do projeto", "O sourceApiVersion, em sfdx-project.json, define que campos de cada metadata type são "
           "recuperados e implantados. Confira esse valor antes de trabalhar com tipos que mudaram de uma versão para outra.",
           E("src:sfdx-project-config")),
        av("implantacao", "O que entra no deploy", "O manifesto package.xml lista o que recuperar ou implantar. Pelo CLI, também se indica por "
           "nomes de componentes ou por caminhos de arquivos.", E("src:mdapi-zip-file", "src:sfdx-develop-any-org")),
    ],
}
S["sub:ambientes-e-sandboxes"] = {
    "para_iniciantes": ini("São os ambientes separados da produção para desenvolver, testar e treinar. Sandboxes são cópias da org de "
                           "produção, em quatro tipos. Scratch orgs são orgs temporárias, criadas vazias e configuradas por um arquivo de definição.",
                           "Uma mudança é feita numa scratch org, testada numa sandbox e só depois vai para produção.",
                           E("src:help-sandbox-licenses", "src:help-sandbox-types", "src:sfdx-scratch-orgs", "src:sfdx-dev-guide"),
                           comece=["func:sandboxes", "func:scratch-orgs-e-dev-hub"]),
    "encadeamento": enc("É onde as mudanças nascem e são testadas, antes da entrega descrita em 'Versionamento, deploy e recuperação'.",
                        E("src:sfdx-dev-guide")),
    "avancado": [
        av("decisao", "Qual sandbox para quê", "Developer e Developer Pro: desenvolvimento e teste isolados, com a configuração de produção; a "
           "Developer Pro comporta mais dados e serve também a testes de integração e treinamento. Partial Copy: ambiente de teste, com "
           "dados definidos por um sandbox template. Full: réplica de produção; o intervalo de refresh longo dificulta usá-la para desenvolver.",
           E("src:help-sandbox-types", "src:help-sandbox-refresh")),
        av("limite", "Intervalo de refresh", "Developer e Developer Pro: 1 dia. Partial Copy: 5 dias. Full: 29 dias. O intervalo conta a partir "
           "do pedido de criação ou de refresh.", E("src:help-sandbox-refresh")),
        av("limite", "Scratch org", "Dura de 1 a 30 dias (padrão 7) e tem 500 MB de dados e 50 MB de arquivos. A edição do Dev Hub define "
           "quantas podem ser criadas por dia e quantas ficam ativas.", E("src:sfdx-scratch-orgs", "src:sfdx-scratch-editions")),
        av("decisao", "Sandbox ou scratch org", "A sandbox é uma cópia da org de produção. A scratch org nasce vazia e é descartável. A "
           "documentação diz que snapshots e scratch orgs não substituem sandboxes no teste de aceitação.",
           E("src:help-sandbox-licenses", "src:sfdx-scratch-orgs", "src:sfdx-snapshots")),
        av("implantacao", "Source tracking em sandbox", "Com o source tracking habilitado em sandboxes Developer e Developer Pro, as ferramentas do "
           "Salesforce DX rastreiam automaticamente componentes novos, alterados e excluídos. A opção fica no metadata type "
           "SourceTrackingSettings, só vale em produção e se aplica quando a sandbox é criada ou atualizada.",
           E("src:sfdx-dev-guide", "src:mdapi-sourcetrackingsettings")),
        av("seguranca", "Permissões", "Criar, atualizar e excluir sandboxes exige Manage Dev Sandboxes (só Developer e Developer Pro) ou Manage "
           "Sandboxes (todos os tipos).", E("src:help-sandbox-refresh")),
        av("atencao", "Onde não se desenvolve", "Apex não é desenvolvido direto em produção. Uma org Developer Edition não tem source tracking "
           "e não serve de ambiente de desenvolvimento no DevOps Center.", E("src:apex-choose-org")),
        av("implantacao", "Como metadado", "DevHubSettings liga o Dev Hub, o Org Shape e os snapshots de scratch org.", E("src:mdapi-devhubsettings")),
    ],
}
S["sub:versionamento-deploy-e-recuperacao"] = {
    "para_iniciantes": ini("Cobre como as mudanças são versionadas e levadas de uma org a outra: pela Metadata API (direto ou pelo Salesforce "
                           "CLI), por change sets ou pelo DevOps Center.",
                           "Um objeto customizado e o seu layout são recuperados da sandbox com retrieve() e implantados em produção com deploy().",
                           E("src:mdapi-intro", "src:help-produtos-platform", "src:help-change-sets", "src:help-lifecycle-center"),
                           comece=["func:metadata-api", "func:change-sets", "func:devops-center"]),
    "encadeamento": enc("Usa os formatos de arquivo e os pacotes do tema; o Lifecycle Center recomenda o controle de versão como fonte única de configuração e código.",
                        E("src:help-produtos-platform", "src:help-lifecycle-center")),
    "avancado": [
        av("decisao", "deploy/retrieve ou source tracking", "deploy() e retrieve() nas fases finais; source push/pull com source tracking nas intermediárias, "
           "porque movem só o que mudou.", E("src:mdapi-intro")),
        av("decisao", "Change set, CLI ou DevOps Center", "Change sets enviam pelo Setup, só entre orgs ligadas à mesma produção. O Salesforce "
           "CLI implanta a partir do projeto local. O Lifecycle Center registra as mudanças no controle de versão e é apresentado como "
           "alternativa aos change sets.",
           E("src:help-change-sets", "src:help-change-sets-connections", "src:cli-project-deploy-start", "src:help-lifecycle-center")),
        av("atencao", "O que não vai no deploy", "A Metadata API não move dados de negócio: registros e atribuições de permission set precisam de outro caminho.",
           E("src:mdapi-intro", "src:objref-permissionsetassignment")),
        av("limite", "Tamanho de um deploy", "Pela Metadata API: até 10.000 arquivos e .zip de até 39 MB (600 MB descompactado). Num change "
           "set: até 10.000 arquivos e 400 MB, com a recomendação de não passar de cerca de 5.000 componentes.",
           E("src:mdapi-zip-file", "src:limits-metadata", "src:help-change-sets-outbound")),
        av("testes", "Testes no deploy", "Em produção, um deploy com Apex roda os testes locais por padrão; se um falha, o deploy inteiro é "
           "revertido. Uma validação roda os testes sem implantar, para implantar depois sem rodá-los de novo.",
           E("src:migration-running-tests", "src:cli-deploy-validate")),
        av("atencao", "Change sets", "Enviar um change set não implanta: o destino precisa fazer o deploy. Inclua os componentes dependentes que "
           "faltam no destino. A org de origem fica bloqueada durante a validação, e a de destino durante o deploy.",
           E("src:help-change-sets-outbound", "src:help-change-sets-best")),
        av("implantacao", "Pipeline do DevOps Center", "Cada estágio do pipeline corresponde a uma org e a um branch. Promover um work item "
           "mescla o branch do estágio atual no do próximo e implanta na org do próximo. O pipeline não pode ser alterado depois que alguma "
           "mudança é promovida.", E("src:help-devops-promote", "src:help-devops-pipeline-plan")),
        av("atencao", "--ignore-errors nunca em produção", "A flag --ignore-errors do deploy pelo CLI implanta o que não deu erro e pula o "
           "resto, sem reverter. A documentação diz para nunca usá-la em produção.", E("src:cli-project-deploy-start")),
    ],
}

# ------------------------------------------------------------------ Observabilidade
S["sub:auditoria-de-configuracao"] = {
    "para_iniciantes": ini("Registra as alterações feitas no Setup: quem mudou o quê e quando.",
                           "Depois de um problema, o administrador confere quem alterou uma configuração na semana anterior.", E("src:security-guide")),
    "encadeamento": enc("Cobre a configuração; o histórico de registros fica em 'Rastreabilidade e histórico'.", E("src:security-guide")),
}
S["sub:historico-de-login"] = {
    "para_iniciantes": ini("Mostra o estado de login de cada usuário e o histórico de tentativas de acesso.",
                           "Verificar de qual IP veio uma tentativa de login que falhou ontem.", E("src:help-login-history", "src:objref-loginhistory"),
                           comece=["func:estado-e-historico-de-login"]),
    "encadeamento": enc("As regras que restringem o login ficam em 'Sessões e políticas de login'.", E("src:mdapi-profile")),
    "avancado": [
        av("limite", "Janela do histórico", "A tela de Setup mostra até 20.000 registros dos últimos 6 meses; o download cobre os últimos 6 meses.", E("src:help-login-history")),
        av("atencao", "IP: onde está cada coisa", "As faixas de IP permitidas ficam em Profile.loginIpRanges; o IP de cada tentativa, em LoginHistory.SourceIp.",
           E("src:mdapi-profile", "src:objref-loginhistory")),
    ],
}
S["sub:eventos-de-monitoramento"] = {
    "para_iniciantes": ini("São eventos que registram uso e atividade na org, para auditoria e detecção quase em tempo real.",
                           "Uma política de segurança de transação reage quando um evento monitorado acontece.", E("src:security-guide")),
    "encadeamento": enc("Eventos de monitoramento em tempo real também podem ser assinados de fora pela Pub/Sub API.", E("src:pubsub-overview")),
}
S["sub:limites-e-consumo"] = {
    "para_iniciantes": ini("Mostra quanto das alocações da org já foi usado, como as requisições de API do dia.",
                           "Um painel de operação consulta o recurso /limits para acompanhar o uso diário de API.", E("src:rest-limits", "src:limits-api-requests")),
    "encadeamento": enc("Os limites de cada integração ficam em 'Contratos, limites e tratamento de falhas'.", E("src:limits-api-requests")),
    "avancado": [av("atencao", "Precisão do /limits", "Os números do /limits têm precisão de até cinco minutos: evite consultas concorrentes ou em rajadas e "
                    "configure notificações de uso de API.", E("src:rest-limits", "src:limits-api-requests"))],
}
S["sub:jobs-incidentes-e-diagnostico"] = {
    "para_iniciantes": ini("Reúne o acompanhamento de jobs e a investigação de problemas na operação.",
                           "A equipe localiza um job assíncrono parado consultando AsyncApexJob.", E("src:apex-queueable")),
    "encadeamento": enc("Os limites de execução assíncrona ficam em 'Monitoramento de jobs e limites'.", E("src:apex-async-overview")),
}

# ------------------------------------------------------------------ IA
S["sub:configuracao-de-agentes"] = {
    "para_iniciantes": ini("Define o agente: o que ele faz, para quem e com quais ferramentas.",
                           "Um agente de atendimento é configurado para responder perguntas sobre pedidos.", E("src:agentforce-dev-guide")),
    "encadeamento": enc("As ações e os assuntos do agente ficam em 'Ações e tópicos'.", E("src:agentforce-dev-guide")),
    "avancado": [av("implantacao", "Agent Script e Agentforce DX", "Agent Script é a linguagem para construir agentes no Agentforce Builder; Agentforce DX traz "
                    "ferramentas para Salesforce CLI e VS Code.", E("src:agentforce-dev-guide"))],
}
S["sub:acoes-e-topicos"] = {
    "para_iniciantes": ini("Ações são o que o agente executa; tópicos, chamados de subagents desde abril de 2026, agrupam os assuntos que ele atende.",
                           "Uma ação consulta o status do pedido quando o cliente pergunta onde está a entrega.", E("src:agentforce-dev-guide")),
    "encadeamento": enc("Não confunda com as ações rápidas da interface, que são botões para pessoas.", E("src:agentforce-dev-guide", "src:help-quick-actions")),
    "avancado": [av("atencao", "Mudança de nome", "Desde abril de 2026, agent topics se chamam subagents, sem mudança de funcionamento.", E("src:agentforce-dev-guide"))],
}
S["sub:prompts"] = {
    "para_iniciantes": ini("Prompts são as instruções enviadas aos modelos de IA.",
                           "Um modelo de prompt pede ao modelo um resumo do caso antes de transferi-lo para outra pessoa.", E("src:agentforce-dev-guide")),
    "encadeamento": enc("Trabalham junto com os modelos, em 'Modelos e grounding'.", E("src:agentforce-dev-guide")),
}
S["sub:modelos-e-grounding"] = {
    "para_iniciantes": ini("Cobre os modelos de IA usados e os dados que fundamentam as respostas.",
                           "Uma resposta do agente usa dados do registro do cliente para não ficar genérica.", E("src:agentforce-dev-guide")),
    "encadeamento": enc("O controle de uso fica em 'Segurança, avaliação e governança de IA'.", E("src:agentforce-dev-guide")),
}
S["sub:seguranca-avaliacao-e-governanca-de-ia"] = {
    "para_iniciantes": ini("Reúne controles, testes e auditoria de recursos de IA; na documentação de desenvolvimento, a camada de confiança aparece como Trust Layer.",
                           "Antes de liberar um agente, a equipe avalia as respostas em cenários de teste.", E("src:agentforce-dev-guide")),
    "encadeamento": enc("Completa a segurança geral da org, que fica em 'Acesso, identidade e segurança'.", E("src:security-guide")),
}

# ------------------------------------------------------------------ Produto
S["sub:vendas"] = {
    "para_iniciantes": ini("Reúne o que é próprio do processo de vendas: leads, contas, contatos, oportunidades, produtos e catálogos de preço, "
                           "cotações, previsões, equipes e territórios.",
                           "Uma pessoa preenche o formulário do site; o lead é qualificado e, ao ser convertido, nascem conta, contato e oportunidade.",
                           E("src:help-sales-basics", "src:help-sales-features", "src:objref-lead"), comece=["func:leads", "func:oportunidades"]),
    "encadeamento": enc("Contas e contatos são a base; o lead vira conta, contato e oportunidade; produtos e cotações compõem o valor; contratos "
                        "registram o acordo fechado; previsões, equipes e territórios organizam a operação. Pedidos ficam em 'Receita e comércio'.",
                        E("src:help-sales-basics", "src:objref-lead", "src:help-contracts-things")),
    "avancado": [
        av("atencao", "Converter lead é operação própria", "Mudar o status de um lead pela API não o converte; use convertLead() ou a interface.", E("src:objref-lead")),
        av("atencao", "IsClosed e IsWon", "Em oportunidades, IsClosed e IsWon não são gravados diretamente: refletem a etapa.", E("src:objref-opportunity")),
        av("limite", "Licença Salesforce Platform", "Usuários com licença Salesforce Platform não têm direito a leads, oportunidades e previsões.", E("src:help-user-licenses")),
        av("atencao", "Cotações e territórios", "Cotações não podem ser desabilitadas se houver referências em customizações ou cotações sincronizadas. Só um modelo "
           "de territórios fica ativo por vez e não volta para Planning.", E("src:help-quotes-setup", "src:help-tm2-activate")),
        av("atencao", "Validação na conversão de leads", "Em Lead Settings, a opção Require Validation for Converted Leads decide se as regras valem na "
           "conversão; desmarcada, lookup filters são ignorados. Preserve Lead Status evita que o status mude para o padrão do novo dono. No "
           "metadado, são shouldLeadConvertRequireValidation e doesPreserveLeadStatus, os dois com padrão true.",
           E("src:help-lead-convert-considerations", "src:help-lead-settings", "src:mdapi-leadconfigsettings")),
        av("atencao", "Desligar schedules apaga dados", "Quantity schedule diz quando o produto é entregue; revenue schedule, quando é pago. Desligar "
           "um tipo apaga as informações desse tipo nos produtos ativos. Se o Apex referencia OpportunityLineItemSchedule, só um dos dois tipos "
           "pode ser desligado.", E("src:help-product-schedules", "src:help-product-schedules-enable", "src:help-product-schedules-considerations")),
        av("decisao", "Data final do contrato", "O contrato tem data de início, prazo em meses e data final. Com Auto-calculate Contract End Date, a "
           "data final sai do início e do prazo e deixa de aparecer na edição do contrato.", E("src:help-contracts-things", "src:help-contracts-setup")),
        av("implantacao", "Como metadado", "As opções gerais de vendas ficam em tipos Settings, um por assunto: LeadConfigSettings, OpportunitySettings, "
           "QuoteSettings, ProductSettings, ContractSettings, ForecastingSettings, Territory2Settings, AccountSettings e CampaignSettings.",
           E("src:mdapi-leadconfigsettings", "src:mdapi-productsettings", "src:mdapi-contractsettings", "src:mdapi-opportunitysettings")),
    ],
}
S["sub:atendimento"] = {
    "para_iniciantes": ini("Reúne o que é próprio do atendimento: casos, roteamento pelo Omni-Channel, conhecimento, níveis de serviço e apps de console.",
                           "Um cliente relata atraso na entrega; o caso registra o contato, a origem por e-mail e a prioridade, e segue até ser fechado.",
                           E("src:help-service-basics", "src:objref-case"), comece=["func:casos", "func:omni-channel"]),
    "encadeamento": enc("O caso é a base; o Omni-Channel distribui o trabalho; entitlements medem prazos usando horário comercial; e o Knowledge ajuda a responder.",
                        E("src:help-service-basics", "src:help-omni-enable", "src:help-ent-bh", "src:help-lk-enable")),
    "avancado": [
        av("atencao", "Omni-Channel Enhanced", "Standard Omni-Channel foi aposentado no Summer '26, com upgrade automático para Enhanced, que não suporta canais standard.",
           E("src:help-omni-upgrade")),
        av("atencao", "Nomes na configuração simplificada", "Na configuração simplificada, Entitlement Management se chama SLA Management e Entitlement Processes se chamam SLA Policies, sem versionamento.",
           E("src:help-ent-sla")),
        av("atencao", "IsClosed do caso", "IsClosed segue o Status do caso; não é definido diretamente.", E("src:objref-case")),
        av("implantacao", "Como metadado", "CaseSettings guarda o dono padrão do caso, os templates de notificação e as configurações de Email-to-Case e "
           "Web-to-Case. OmniChannelSettings, EntitlementSettings e KnowledgeSettings cobrem roteamento, entitlements e Knowledge.",
           E("src:mdapi-omnichannelsettings", "src:mdapi-entitlementsettings", "src:mdapi-knowledgesettings", "src:mdapi-casesettings")),
    ],
}
S["sub:receita-e-comercio"] = {
    "para_iniciantes": ini("Reúne o que acontece depois que a venda é acertada: pedidos, preços mais elaborados, assinaturas e faturamento. Na "
                           "plataforma padrão, isso começa nos pedidos (orders). Produtos próprios vão além: Salesforce CPQ, Salesforce Billing, "
                           "Subscription Management e Revenue Management (antes Revenue Cloud).",
                           "Depois de fechar a oportunidade, o time registra um pedido com os produtos vendidos; uma devolução parcial entra "
                           "como reduction order.",
                           E("src:help-produtos-sales", "src:help-orders-enable", "src:help-orders-manage", "src:help-revenue-get-started"),
                           comece=["func:pedidos"]),
    "encadeamento": enc("Vem depois de 'Vendas': as cotações padrão, ligadas às oportunidades, e os contratos ficam lá. O pedido pode ser ativado "
                        "para um contrato ativo. Os produtos de receita assumem a partir da cotação ou do pedido, cada um com licença e modelo "
                        "próprios.", E("src:help-quotes-setup", "src:help-orders-activation", "src:help-billing-overview")),
    "avancado": [
        av("decisao", "Pacote ou plataforma nativa", "Salesforce CPQ é um managed package; Revenue Management roda de forma nativa na plataforma, "
           "com outro modelo de dados e outra forma de configurar. Salesforce Billing é um pacote complementar que recebe o pedido do CPQ para "
           "faturamento, pagamento e reconhecimento de receita.", E("src:help-revenue-vs-cpq", "src:help-billing-overview")),
        av("atencao", "Trocar de produto não é migração de dados comum", "Sair de Salesforce CPQ e Salesforce Billing para o Revenue Cloud muda modelo de "
           "dados, processos e governança. A Ajuda tem um tópico para descobrir qual produto de receita a org usa; comece por ele.",
           E("src:help-revenue-migrate", "src:help-revenue-get-started")),
        av("limite", "Ativação de pedidos", "Um pedido só é ativado se tiver order products e, quando ligado a contrato, se o contrato estiver ativo. "
           "Depois de ativar, dá para alterar os order products, mas não incluir nem remover.", E("src:help-orders-activation")),
        av("limite", "Reduction orders", "Registram redução, devolução ou desativação de produtos de um pedido. Só pedidos ativados podem ser "
           "reduzidos, cada reduction order vale para um pedido, e no Lightning Experience não dá para criá-las.",
           E("src:help-orders-manage", "src:help-orders-reduce")),
        av("implantacao", "Como metadado", "OrderSettings liga pedidos (enableOrders, obrigatório) e as variações: reduction orders, quantidade zero "
           "ou negativa e pedidos sem price book. enableEnhancedCommerceOrders só existe com a licença Salesforce Order Management e é usado por "
           "lojas B2B para pedidos em alta escala.", E("src:mdapi-ordersettings", "src:help-orders-high-scale")),
    ],
}

CONTEUDO_SUB = S
