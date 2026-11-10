"""Issue #34: conteúdo específico dos temas internos (subclassificações). Usado por conteudo_temas.py.

Mesma regra de conteudo_cls.py: só fatos já catalogados nas funcionalidades ou lidos nas notas de extração do #34.
Temas internos sem fonte lida ficam de fora (lista PENDENTES) até a próxima rodada de pesquisa.
"""
from conteudo_cls import E, ini, enc, av, AF

PENDENTES = [
    "sub:habilitacao-de-recursos", "sub:metadados-de-configuracao-de-dados", "sub:experiencias-web-portais-e-mobile",
    "sub:colaboracao", "sub:templates-e-comunicacao",
    "sub:recuperacao-de-conhecimento", "sub:servico-de-campo", "sub:experiencias-externas", "sub:capacidades-setoriais", "sub:outras-areas",
]

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
                           "tela, pela gravação de um registro, por um agendamento ou por outros gatilhos.",
                           "Atualizar o status do contrato quando a assinatura é registrada.", E("src:mdapi-flow"), comece=["func:flow"]),
    "encadeamento": enc("É a ferramenta principal do tema. Screen Flows também aparecem em Interface, como opção para formulários de várias telas.",
                        E("src:mdapi-flow", AF)),
    "avancado": [
        av("decisao", "Quando o Screen Flow é a escolha", "Para assistentes com várias telas, sem exigência rígida de marca, o guia de decisão indica "
           "Screen Flow: navegação pronta e lógica mantida por administradores.", E(AF)),
        av("seguranca", "Contexto de sistema", "Screen Flow roda no contexto do usuário por padrão, mas pode rodar em contexto de sistema; esse modo deve "
           "ficar restrito a usuários confiáveis.", E(AF)),
    ],
}
S["sub:decisoes-e-aprovacoes"] = {
    "para_iniciantes": ini("Organiza os pontos em que alguém precisa decidir antes de o processo seguir, como aprovar um desconto ou um contrato.",
                           "Um desconto acima do padrão vai para aprovação do gestor antes de a cotação ser enviada.", E("src:help-produtos-platform")),
    "encadeamento": enc("A Ajuda reúne aprovações entre as ferramentas declarativas de automação, ao lado de experiências guiadas e automação em segundo plano.",
                        E("src:help-produtos-platform")),
}
S["sub:acoes-e-regras"] = {
    "para_iniciantes": ini("Reúne ações reutilizáveis e regras que disparam comportamento: definir automaticamente o dono de leads e casos, "
                           "escalonar casos e oferecer botões de ação.",
                           "Casos com prioridade alta vão para a fila de nível 1; leads do site vão para a equipe de inbound.",
                           E("src:help-assign-setup", "src:help-escalation-setup", "src:help-quick-actions"),
                           comece=["func:regras-de-atribuicao", "func:acoes-rapidas"]),
    "encadeamento": enc("Ações rápidas também aparecem em Interface, como botões; regras de atribuição também servem a Vendas e Atendimento.",
                        E("src:help-quick-actions", "src:help-assign-guide")),
    "avancado": [av("limite", "Uma regra ativa por tipo", "Só uma regra de atribuição de cada tipo fica ativa por vez, e uma regra de atribuição de casos "
                    "aceita até 3.000 entradas, incluindo 300 de fórmula.", E("src:help-assign-guide"))],
}
S["sub:automacao-apex"] = {
    "para_iniciantes": ini("Cobre triggers e classes Apex que automatizam processos quando as ferramentas declarativas não bastam.",
                           "Um trigger grava o pedido e precisa avisar o ERP; a chamada externa tem de vir antes da gravação ou ir para um processo assíncrono.",
                           E("src:apex-callout-limits", "src:help-produtos-platform")),
    "encadeamento": enc("Apex que roda depois, em fila ou agendado, fica em 'Execução assíncrona, lotes e agendamento'.", E("src:apex-async-overview")),
    "avancado": [
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
    "para_iniciantes": ini("Batch Apex processa grandes volumes de registros dividindo o trabalho em partes.",
                           "Recalcular um campo em todas as contas da org durante a madrugada.", E("src:apex-async-overview")),
    "encadeamento": enc("O agendamento dispara execuções em horário definido, e o andamento fica em 'Monitoramento de jobs e limites'.", E("src:apex-async-overview")),
    "avancado": [av("limite", "Fila do Batch Apex", "No máximo cinco jobs Batch Apex ativos, com uma Flex Queue de até 100 jobs adicionais.", E("src:apex-async-overview"))],
}
S["sub:queueable"] = {
    "para_iniciantes": ini("Queueable Apex coloca uma tarefa na fila para rodar em segundo plano quando houver recursos. Devolve um identificador "
                           "para acompanhar o job e permite encadear tarefas.",
                           "Depois de salvar um pedido, a chamada ao ERP vai para a fila e roda em seguida, sem prender a tela.",
                           E("src:apex-queueable", "src:apex-async-overview")),
    "encadeamento": enc("É o caminho recomendado no lugar dos future methods.", E("src:apex-queueable")),
    "avancado": [av("decisao", "Queueable no lugar de future", "A Salesforce recomenda Queueable Apex no lugar de future methods: aceita tipos complexos, "
                    "encadeia jobs e devolve um Id para acompanhar o trabalho.", E("src:apex-queueable", "src:apex-async-overview"))],
}
S["sub:future-e-mecanismos-legados"] = {
    "para_iniciantes": ini("Future methods rodam um método em segundo plano para não atrasar a transação. A Salesforce recomenda substituí-los por Queueable.",
                           "Um método marcado como future faz uma chamada demorada sem atrasar a gravação que o disparou.",
                           E("src:apex-async-overview", "src:apex-queueable")),
    "encadeamento": enc("Fica aqui para quem mantém código existente; para código novo, veja Queueable.", E("src:apex-queueable")),
}
S["sub:agendamento"] = {
    "para_iniciantes": ini("Scheduled Apex roda uma classe em horário definido, como uma rotina diária ou semanal. Flows também podem ser disparados por agendamento.",
                           "Todo domingo, uma rotina gera os lembretes da semana.", E("src:apex-async-overview", "src:mdapi-flow")),
    "encadeamento": enc("Horários comerciais, que contam prazos de atendimento, são outro assunto, em Organização.", E("src:help-bh")),
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
    "para_iniciantes": ini("Acompanha as execuções assíncronas: em que estado está cada job e quanto dos limites já foi usado.",
                           "Um job enfileirado é acompanhado na tela Apex Jobs ou consultando AsyncApexJob pelo identificador devolvido.",
                           E("src:apex-queueable", "src:apex-async-overview")),
    "encadeamento": enc("Completa os mecanismos do tema; o consumo geral da org fica em Observabilidade.", E("src:apex-async-overview", "src:rest-limits")),
    "avancado": [av("limite", "Fila do Batch Apex", "No máximo cinco jobs Batch Apex ativos, com uma Flex Queue de até 100 jobs adicionais.", E("src:apex-async-overview"))],
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
    "para_iniciantes": ini("Cobre classes, componentes e outros artefatos de código vistos como itens a construir e entregar.",
                           "Um editor de código consulta, pela Tooling API, só a classe Apex que o desenvolvedor abriu, em vez de recuperar todos os metadados.",
                           E("src:tooling-intro"), comece=["func:tooling-api"]),
    "encadeamento": enc("O formato dos arquivos fica em 'Source format e Metadata API format'; a entrega, em 'Versionamento, deploy e recuperação'.",
                        E("src:sdr-registry", "src:mdapi-intro")),
    "avancado": [av("decisao", "Tooling API ou Metadata API", "A Tooling API serve a ferramentas que leem e alteram pedaços pequenos de metadados; a Metadata "
                    "API move o modelo completo.", E("src:tooling-intro", "src:mdapi-intro"))],
}
S["sub:testes"] = {
    "para_iniciantes": ini("Cobre os testes automatizados: como conferir que a mudança funciona antes de chegar à produção.",
                           "Os testes rodam automaticamente a cada mudança, num pipeline de integração contínua.", E("src:sfdx-dev-guide", AF)),
    "encadeamento": enc("Fazem parte da entrega; os ambientes isolados ficam em 'Ambientes e sandboxes'.", E("src:sfdx-dev-guide")),
    "avancado": [av("testes", "Unitário ou de interface", "Só LWC permite testes unitários escritos, por exemplo com Jest; Dynamic Forms e Screen Flow "
                    "dependem de automação de interface de ponta a ponta, que não verifica saídas de métodos.", E(AF))],
}
S["sub:pacotes-e-dependencias"] = {
    "para_iniciantes": ini("Pacotes agrupam componentes para distribuir e implantar juntos, registrando as dependências entre eles.",
                           "Uma equipe publica seus componentes como pacote desbloqueado e o instala em outra org.", E("src:sfdx-dev-guide", AF)),
    "encadeamento": enc("É uma das formas de entrega; as outras ficam em 'Versionamento, deploy e recuperação'.", E(AF)),
    "avancado": [av("implantacao", "O que pode ir em pacote", "Dynamic Forms, Screen Flows e LWC podem ir por pacotes gerenciados (1GP e 2GP), pacotes "
                    "desbloqueados, change sets e DevOps Center; Omnistudio não aceita empacotamento.", E(AF))],
}
S["sub:source-format-e-metadata-api-format"] = {
    "para_iniciantes": ini("Os metadados podem ser guardados em dois formatos de arquivo: o source format, usado em projetos do Salesforce CLI, e "
                           "o Metadata API format, usado pela Metadata API.",
                           "Uma Lightning page fica em flexipages/<Nome>.flexipage no Metadata API format e ganha o sufixo -meta.xml no source format.",
                           E("src:sdr-registry", "src:sfdx-dev-guide")),
    "encadeamento": enc("Cada ficha de metadata type mostra a pasta e o sufixo nos dois formatos.", E("src:sdr-registry")),
}
S["sub:ambientes-e-sandboxes"] = {
    "para_iniciantes": ini("São ambientes separados da produção para desenvolver, testar e treinar: sandboxes e scratch orgs.",
                           "Uma mudança é feita numa scratch org, testada numa sandbox e só depois vai para produção.",
                           E("src:help-produtos-platform", "src:sfdx-dev-guide")),
    "encadeamento": enc("É onde as mudanças nascem, antes da entrega.", E("src:sfdx-dev-guide")),
    "avancado": [av("implantacao", "Source tracking em sandbox", "Com o source tracking habilitado em sandboxes Developer e Developer Pro, as ferramentas do "
                    "Salesforce DX rastreiam automaticamente componentes novos, alterados e excluídos.", E("src:sfdx-dev-guide"))],
}
S["sub:versionamento-deploy-e-recuperacao"] = {
    "para_iniciantes": ini("Cobre como as mudanças são versionadas, implantadas e, se preciso, revertidas.",
                           "Um objeto customizado e o seu layout são recuperados da sandbox com retrieve() e implantados em produção com deploy().",
                           E("src:mdapi-intro", "src:help-produtos-platform"), comece=["func:metadata-api"]),
    "encadeamento": enc("Usa os formatos de arquivo e os pacotes do tema; o Lifecycle Center recomenda o controle de versão como fonte única de configuração e código.",
                        E("src:help-produtos-platform")),
    "avancado": [
        av("decisao", "deploy/retrieve ou source tracking", "deploy() e retrieve() nas fases finais; source push/pull com source tracking nas intermediárias, "
           "porque movem só o que mudou.", E("src:mdapi-intro")),
        av("atencao", "O que não vai no deploy", "A Metadata API não move dados de negócio: registros e atribuições de permission set precisam de outro caminho.",
           E("src:mdapi-intro", "src:objref-permissionsetassignment")),
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
    "encadeamento": enc("Contas e contatos são a base; o lead vira conta, contato e oportunidade; produtos e cotações compõem o valor; previsões, "
                        "equipes e territórios organizam a operação.", E("src:help-sales-basics", "src:objref-lead")),
    "avancado": [
        av("atencao", "Converter lead é operação própria", "Mudar o status de um lead pela API não o converte; use convertLead() ou a interface.", E("src:objref-lead")),
        av("atencao", "IsClosed e IsWon", "Em oportunidades, IsClosed e IsWon não são gravados diretamente: refletem a etapa.", E("src:objref-opportunity")),
        av("limite", "Licença Salesforce Platform", "Usuários com licença Salesforce Platform não têm direito a leads, oportunidades e previsões.", E("src:help-user-licenses")),
        av("atencao", "Cotações e territórios", "Cotações não podem ser desabilitadas se houver referências em customizações ou cotações sincronizadas. Só um modelo "
           "de territórios fica ativo por vez e não volta para Planning.", E("src:help-quotes-setup", "src:help-tm2-activate")),
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
    ],
}
S["sub:receita-e-comercio"] = {
    "para_iniciantes": ini("Reúne capacidades de receita, cotação e comércio que vão além das cotações padrão, como Salesforce CPQ, Salesforce Billing, "
                           "Subscription Management e Agentforce Revenue Management.",
                           "Uma empresa usa o Salesforce CPQ para criar, gerenciar e enviar propostas.", E("src:help-produtos-sales")),
    "encadeamento": enc("As cotações padrão, ligadas às oportunidades, ficam no tema interno Vendas.", E("src:help-quotes-setup")),
}

CONTEUDO_SUB = S
