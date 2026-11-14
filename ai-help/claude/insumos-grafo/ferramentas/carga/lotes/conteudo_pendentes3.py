"""Issue #34: temas internos que estavam pendentes por falta de fonte (lote 3: Conteúdo, IA, Interface, Organização e Dados).
Fontes lidas pelos resultados de busca restritos aos domínios oficiais: fontes/extracoes/temas-pendentes-lote3.txt.
Usado por conteudo_temas.py.
"""
from carga.catalogo import fonte
from conteudo_cls import E, ini, enc, av

DATA = "2026-11-10"
EXT = "fontes/extracoes/temas-pendentes-lote3.txt"
AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")
DOC = dict(versao="sem versão na página", metodo="leitura_resultado_busca")


def F(i, t, u, p, **k):
    return fonte(i, t, u, p, EXT, DATA, **k)


FONTES_PENDENTES3 = [
    # Colaboração
    F("src:help-chatter-overview-parent", "Share Updates with People in Chatter",
      "https://help.salesforce.com/s/articleView?id=sf.collab_chatter_parent.htm&type=5", "Visão geral do Chatter, streams e Chatter desligado em orgs novas.", **AJ),
    F("src:help-chatter-groups", "Chatter Groups",
      "https://help.salesforce.com/s/articleView?id=experience.collab_group_about.htm&type=5", "Tipos de grupo e limites.", **AJ),
    F("src:help-chatter-groups-parent", "Collaborate in Chatter Groups",
      "https://help.salesforce.com/s/articleView?id=collab_groups_parent.htm&type=5", "Grupos unlisted e broadcast.", **AJ),
    F("src:help-chatter-feeds-overview", "Chatter Feeds Overview",
      "https://help.salesforce.com/s/articleView?id=collab_feed_overview.htm&type=5", "O que entra no feed, feed tracking e limpeza automática.", **AJ),
    # Templates e comunicação
    F("src:help-email-templates-lex", "Email Templates in Lightning Experience",
      "https://help.salesforce.com/s/articleView?id=sales.email_templates_lightning_parent.htm&type=5", "Templates privados e públicos, pastas, templates do Classic.", **AJ),
    F("src:help-handlebars-merge-language", "Use the Handlebars Merge Language in Lightning Email Templates, Enhanced Letterhead, and Email Template Builder",
      "https://help.salesforce.com/s/articleView?id=handlebars_template_language.htm&type=5", "HML e SML, merge fields de destinatário.", **AJ),
    F("src:help-enhanced-letterheads-create", "Create Enhanced Letterheads in Lightning Experience",
      "https://help.salesforce.com/s/articleView?id=sales.enhanced_letterheads_create.htm", "Permissão e restrições dos enhanced letterheads.", **AJ),
    F("src:help-merge-fields-considerations", "Considerations for Using Merge Fields in Email Templates and Letterheads",
      "https://help.salesforce.com/s/articleView?id=sf.merge_fields_email_templates.htm", "Restrições de merge fields e limite do assunto.", **AJ),
    F("src:objref-emailtemplate", "EmailTemplate (Object Reference)",
      "https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-emailtemplate.html",
      "Relação com BrandTemplate e EnhancedLetterhead.", **DOC),
    # Recuperação de conhecimento
    F("src:help-agentforce-data-library", "Agentforce Data Library",
      "https://help.salesforce.com/s/articleView?id=ai.data_library_parent.htm&type=5", "Fontes indexadas, edições e dependência do Data 360.", **AJ),
    F("src:help-adl-setup-troubleshoot", "Agentforce: Setup & Troubleshoot Agentforce Data Libraries & Answer Question with Knowledge (KB)",
      "https://help.salesforce.com/s/articleView?id=004333412&type=1", "Índice, retriever, filtro de artigos públicos e rebuild.", **AJ),
    F("src:dev-website-search-index-retriever", "Step 3 - Create Search Index and Retriever",
      "https://developer.salesforce.com/docs/ai/ground-agentforce-on-website/guide/aes-create-search-index-and-retriever.html",
      "Chunks, embeddings e papel do retriever.", **DOC),
    F("src:connect-rest-adl", "Agentforce Connect REST API, Agentforce Data Libraries Resources (Beta)",
      "https://developer.salesforce.com/docs/platform/connect-rest-api/references/connect-rest-api-agentforce",
      "Tipos de fonte, campos imutáveis e exclusão em cascata.", versao="v68.0 (Beta)", metodo="leitura_resultado_busca"),
    # Experiências web/portais e mobile
    F("src:help-experience-cloud-overview", "Experience Cloud",
      "https://help.salesforce.com/s/articleView?id=experience.networks_overview.htm&type=5", "O que é um site Experience Cloud e edições.", **AJ),
    F("src:help-experience-cloud-templates", "Which Experience Cloud Template Should I Use?",
      "https://help.salesforce.com/s/articleView?id=sf.siteforce_commtemp_intro.htm&type=5", "Templates disponíveis e quais usam o Experience Builder.", **AJ),
    F("src:dev-experience-builder-sites-intro", "Get Up to Speed with Experience Builder Sites",
      "https://developer.salesforce.com/docs/platform/communities-dev/guide/communities-dev-intro.html", "Sites Aura e LWR.", **DOC),
    F("src:help-experience-find-your-way", "Find Your Way Around (Experience Cloud)",
      "https://help.salesforce.com/s/articleView?id=sf.exp_cloud_basics_navigation.htm&type=5", "Setup, Experience Workspaces e Experience Builder.", **AJ),
    F("src:help-mobile-app-customize", "Customize the Salesforce Mobile App",
      "https://help.salesforce.com/s/articleView?id=xcloud.salesforce_app_customize.htm&type=5", "Personalização de marca, navegação e launchpad.", **AJ),
    F("src:help-mobile-only-navigation", "Customize the Mobile Only Navigation Menu in the Salesforce Mobile App",
      "https://help.salesforce.com/s/articleView?id=salesforce_app_customize_nav_menu.htm", "Mobile Only legado e regras do menu.", **AJ),
    F("src:help-compact-layouts", "Compact Layouts",
      "https://help.salesforce.com/s/articleView?id=platform.compact_layout_overview.htm&type=5", "Campos-chave no app móvel.", **AJ),
    # Habilitação de recursos
    F("src:mdapi-settings", "Settings (Metadata API)",
      "https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_settings.htm", "O que os tipos Settings representam.", **DOC),
    F("src:mdapi-sharingsettings", "SharingSettings (Metadata API)",
      "https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-sharingsettings.html",
      "Settings no package.xml, um arquivo por setting e curinga.", **DOC),
    F("src:help-lightning-knowledge-enable", "Create a Knowledge Base with Salesforce Knowledge",
      "https://help.salesforce.com/s/articleView?id=knowledge_whatis.htm&type=5", "Lightning Knowledge irreversível e muda o modelo de dados.", **AJ),
    F("src:help-education-cloud-enable", "Turn On Education Cloud",
      "https://help.salesforce.com/s/articleView?id=sfdo.ec_enable_education_cloud.htm&type=5", "Education Cloud não pode ser desligado.", **AJ),
    F("src:help-translation-workbench-enable", "Enable or Disable Translation Workbench",
      "https://help.salesforce.com/s/articleView?id=platform.customize_wbench.htm&type=5", "Recurso que pode ser desligado, com exceção.", **AJ),
    # Metadados de configuração de dados
    F("src:dev-ldv-indexes", "Indexes (Best Practices for Deployments with Large Data Volumes)",
      "https://developer.salesforce.com/docs/atlas.en-us.salesforce_large_data_volumes_bp.meta/salesforce_large_data_volumes_bp/ldv_deployments_infrastructure_indexes.htm",
      "Índices padrão, índices customizados e External ID.", **DOC),
    F("src:help-external-id-unique-index", "Make a SOQL query selective by marking a field as External ID or Unique (KB)",
      "https://help.salesforce.com/s/articleView?id=000383981&type=1", "External ID e Unique criam índice; upsert.", **AJ),
    F("src:help-custom-index-limit", "Maximum Number of Custom Indexes Per Salesforce Object (KB)",
      "https://help.salesforce.com/s/articleView?id=000386304&type=1", "Origens de índice customizado e limite de External ID/Unique.", **AJ),
]

P = {}
P["sub:colaboracao"] = {
    "para_iniciantes": ini("Chatter é a rede interna da org: pessoas postam, comentam e acompanham colegas, grupos e registros num feed. "
                           "Grupos reúnem quem trabalha junto, e mudanças em campos rastreados aparecem no feed como posts automáticos. "
                           "O Chatter respeita as permissões da org: só aparece o que a pessoa já pode ver.",
                           "O time de implantação cria um grupo privado para o projeto e segue a oportunidade principal; quando o "
                           "estágio muda, o post automático aparece no feed de todos.",
                           E("src:help-chatter-overview-parent", "src:help-chatter-feeds-overview")),
    "encadeamento": enc("Usa os registros e as permissões já definidos: o feed mostra só o que cada um acessa. Avisos disparados por "
                        "automação ficam em 'Notificações', e arquivos compartilhados ficam em 'Files e documentos'.",
                        E("src:help-chatter-overview-parent")),
    "avancado": [
        av("atencao", "Chatter desligado em orgs novas", "A partir do Summer '26, Chatter vem desligado nas orgs novas. Recursos que dependem "
           "dele ou das Chatter APIs só funcionam depois de ligar em Setup > Chatter Settings.", E("src:help-chatter-overview-parent")),
        av("decisao", "Tipo de grupo", "Grupos podem ser public, private, unlisted ou archived. Unlisted só aparece para membros e para quem tem "
           "Manage Unlisted Groups. Em broadcast groups só donos e gerentes postam. Num grupo arquivado não entra post novo, mas os antigos "
           "ficam.", E("src:help-chatter-groups", "src:help-chatter-groups-parent")),
        av("limite", "Grupos, streams e feed", "Cada pessoa entra em até 300 grupos, e a empresa tem até 30.000. Streams juntam feeds: até 100 "
           "por pessoa, com até 25 feeds cada. Atualizações rastreadas com mais de 45 dias, sem curtidas nem comentários, são apagadas.",
           E("src:help-chatter-groups", "src:help-chatter-overview-parent", "src:help-chatter-feeds-overview")),
        av("escala", "Armazenamento", "Posts, tracked changes e comentários do Chatter não contam no armazenamento de dados da org.",
           E("src:help-chatter-overview-parent")),
    ],
}
P["sub:templates-e-comunicacao"] = {
    "para_iniciantes": ini("Um email template é um e-mail pronto para reaproveitar, com merge fields que trocam marcadores pelos dados "
                           "do registro na hora do envio. Um letterhead padroniza cabeçalho e rodapé, como logo e contato da empresa.",
                           "O template de boas-vindas usa {{{Recipient.FirstName}}}; ao enviar para a contato Ana, o texto sai "
                           "'Olá, Ana'.",
                           E("src:help-email-templates-lex", "src:help-handlebars-merge-language")),
    "encadeamento": enc("Depende dos campos dos objetos, que viram merge fields. Templates usados por automações também aparecem em "
                        "'Notificações'; prompts de IA ficam em 'Prompts'.",
                        E("src:help-merge-fields-considerations")),
    "avancado": [
        av("decisao", "HML ou SML", "Templates Lightning criados desde o Summer '18 usam Handlebars Merge Language ({{{ }}}); os anteriores e os do "
           "Classic usam Salesforce Merge Language ({! }). Enhanced letterheads só funcionam com HML, e a implementação HML não traz todos os "
           "recursos do Handlebars.", E("src:help-handlebars-merge-language", "src:help-enhanced-letterheads-create")),
        av("atencao", "Merge fields que ficam vazios", "Merge field de um objeto que não é o destinatário nem o Related To fica sem valor, e campo "
           "sem dado some do e-mail. Recipient não funciona em templates usados por automações, e nenhum merge field de destinatário vale quando "
           "o destinatário é um usuário.", E("src:help-merge-fields-considerations", "src:help-handlebars-merge-language")),
        av("seguranca", "Quem vê e quem cria", "Templates nascem privados; pastas com enhanced sharing decidem quem usa cada um, e sem elas todos "
           "ficam públicos. Criar ou alterar enhanced letterheads exige Modify All Data, e eles são públicos por padrão.",
           E("src:help-email-templates-lex", "src:help-enhanced-letterheads-create")),
        av("limite", "Assunto e letterhead", "O assunto aceita até 1.000 caracteres no Lightning e 230 no Classic, contando os merge fields. "
           "Letterheads não aparecem no Outlook desktop, e o Email Template Builder não os suporta.",
           E("src:help-merge-fields-considerations", "src:help-enhanced-letterheads-create")),
        av("implantacao", "Template no modelo de dados", "No objeto EmailTemplate, o letterhead clássico vem pela referência ao BrandTemplate e o "
           "enhanced pela relação EnhancedLetterhead. Ao empacotar ou pôr num change set, só alguns tipos de anexo acompanham o template.",
           E("src:objref-emailtemplate", "src:help-email-templates-lex")),
    ],
}
P["sub:recuperacao-de-conhecimento"] = {
    "para_iniciantes": ini("Para um agente de IA responder com base no conteúdo da empresa, esse conteúdo precisa ser encontrável. A "
                           "Agentforce Data Library indexa artigos do Knowledge, arquivos ou páginas web, e um retriever busca os trechos "
                           "mais relevantes para cada pergunta e os entrega ao modelo.",
                           "Um cliente pergunta como trocar a senha; o retriever acha o trecho do artigo de ajuda e o agente responde "
                           "com base nele.",
                           E("src:help-agentforce-data-library", "src:dev-website-search-index-retriever"),
                           analogia=("É como um bibliotecário que separa as páginas certas antes de alguém responder.",
                                     "O bibliotecário não escreve a resposta: quem redige é o modelo, e ele pode errar se os trechos "
                                     "trazidos forem ruins.")),
    "encadeamento": enc("Fica entre o conteúdo e a resposta: os artigos vêm de 'Knowledge e categorias', e o uso dos trechos pelo modelo "
                        "fica em 'Modelos e grounding' e 'Prompts'.",
                        E("src:help-agentforce-data-library", "src:help-adl-setup-troubleshoot")),
    "avancado": [
        av("implantacao", "O que a library cria", "A library divide o conteúdo em chunks, gera embeddings e guarda tudo num vector search index; "
           "depois cria um retriever que a ação Answer Questions with Knowledge usa. A ação só funciona com o índice em Ready.",
           E("src:help-adl-setup-troubleshoot", "src:dev-website-search-index-retriever")),
        av("limite", "Requisitos e custo", "Exige Data 360 e consome créditos dele. Em companion org do Data Cloud One, Knowledge e Files não são "
           "aceitos como fonte; usa-se um custom retriever.", E("src:help-agentforce-data-library")),
        av("atencao", "Artigos que não aparecem", "Com Use Public Knowledge Articles ligado, só entram artigos publicados e visíveis na base pública. "
           "O chunking pega só texto, não imagens dos arquivos. Depois de mudanças grandes, o rebuild reindexa tudo.",
           E("src:help-adl-setup-troubleshoot")),
        av("implantacao", "Library por API (Beta)", "A Connect REST API tem recursos em Beta para criar, indexar e excluir libraries, com fontes "
           "SFDRIVE, KNOWLEDGE, RETRIEVER e SITEMAP. Os campos primaryIndexField1 e primaryIndexField2 não mudam depois de criados, e excluir a "
           "library apaga em cascata o retriever e o search index.", E("src:connect-rest-adl")),
    ],
}
P["sub:experiencias-web-portais-e-mobile"] = {
    "para_iniciantes": ini("A mesma org pode ser usada fora do desktop interno de duas formas: por sites e portais do Experience Cloud, "
                           "para clientes, parceiros ou funcionários, e pelo Salesforce mobile app, no celular. Nos dois casos os dados "
                           "são os da própria org; muda a interface.",
                           "Clientes abrem chamados num portal Customer Service, e o técnico vê o mesmo caso no app do celular.",
                           E("src:help-experience-cloud-overview", "src:help-mobile-app-customize"), comece=["func:digital-experiences"]),
    "encadeamento": enc("Reaproveita o que vem de 'Layouts e páginas de registro' e 'Aplicativos e navegação': o app móvel usa compact "
                        "layouts e a navegação dos Lightning apps. Antes do primeiro site, é preciso ligar digital experiences. As "
                        "capacidades de produto para público externo ficam em 'Experiências externas'.",
                        E("src:help-compact-layouts", "src:help-mobile-only-navigation", "src:help-experience-org-setup")),
    "avancado": [
        av("decisao", "Qual template de site", "Há templates prontos (Customer Account Portal, Partner Central, Customer Service, Help Center) e "
           "os Build Your Own em Aura ou LWR, além de Microsites (LWR). Sites LWR aceitam só Lightning web components; sites Aura aceitam Aura e "
           "LWC juntos. Customer Service exige Chatter ligado.",
           E("src:help-experience-cloud-templates", "src:dev-experience-builder-sites-intro")),
        av("implantacao", "Onde se monta um site", "Em Setup, liga-se Experiences e cria-se o site; em Experience Workspaces, administra-se e "
           "monitora-se; no Experience Builder, montam-se páginas, temas e a publicação. Salesforce Tabs + Visualforce não usa o Experience "
           "Builder.", E("src:help-experience-find-your-way", "src:help-experience-cloud-templates")),
        av("decisao", "Navegação no app móvel", "Mobile Only é legado; a recomendação é a navegação do Lightning app, que o app abre por padrão "
           "desde o Winter '22. No Mobile Only, os quatro primeiros itens vão para a barra inferior, e não há menu diferente por tipo de "
           "usuário: o que aparece segue as abas visíveis no perfil.", E("src:help-mobile-only-navigation")),
        av("atencao", "Campos no celular", "O compact layout define os campos-chave no topo do registro no app móvel, no Lightning Experience e "
           "nas integrações com Outlook e Gmail. Cada objeto tem um padrão do sistema, e cada record type pode ter o seu.",
           E("src:help-compact-layouts")),
    ],
}
P["sub:habilitacao-de-recursos"] = {
    "para_iniciantes": ini("Muitos recursos da Salesforce vêm desligados e são ligados no Setup. Alguns mudam o comportamento ou o modelo "
                           "de dados da org e não podem ser desligados depois; por isso vale testar em sandbox antes de ligar em "
                           "produção.",
                           "Ligar Lightning Knowledge troca article types por record types e não tem volta.",
                           E("src:help-lightning-knowledge-enable")),
    "encadeamento": enc("É a porta de entrada de vários temas: o funcionamento de cada recurso ligado é estudado no tema dele. A "
                        "configuração gravada como metadado fica em 'Settings'.",
                        E("src:mdapi-settings")),
    "avancado": [
        av("atencao", "Ativações sem volta", "Lightning Knowledge e Education Cloud não podem ser desligados depois de ligados. Já o Translation "
           "Workbench pode ser desligado, exceto em Developer org com pacote gerenciado que traga traduções. Conferir a página do recurso antes "
           "de ligar.", E("src:help-lightning-knowledge-enable", "src:help-education-cloud-enable", "src:help-translation-workbench-enable")),
        av("atencao", "O padrão muda com a release", "Um recurso pode mudar de padrão para orgs novas: a partir do Summer '26, Chatter vem "
           "desligado nas orgs novas. Alguns defaults de settings também dependem da data de criação da org.",
           E("src:help-chatter-overview-parent", "src:mdapi-sharingsettings")),
        av("implantacao", "Ligar por metadado", "Muitas ativações ficam gravadas em tipos da família Settings, que representam as configurações da "
           "org ligadas a um recurso. No package.xml, todos são pedidos pelo nome Settings, há um arquivo .settings por componente, e o "
           "curinga * só serve para recuperar todos.", E("src:mdapi-settings", "src:mdapi-sharingsettings")),
        av("seguranca", "Quem pode ligar", "Cada recurso define a permissão necessária; o Translation Workbench, por exemplo, exige Customize "
           "Application.", E("src:help-translation-workbench-enable")),
    ],
}
P["sub:metadados-de-configuracao-de-dados"] = {
    "para_iniciantes": ini("Além de objetos e campos, a org guarda configurações sobre como os dados se comportam: quais campos têm índice "
                           "para buscas rápidas, quais guardam histórico de mudanças e quais aparecem no feed. São opções do campo ou do "
                           "objeto, não dados novos.",
                           "Marcar o campo Código do ERP como External ID cria um índice nele e permite usá-lo como chave no upsert.",
                           E("src:dev-ldv-indexes", "src:help-external-id-unique-index")),
    "encadeamento": enc("Vem depois de 'Objetos e entidades' e 'Campos e tipos', porque essas opções ficam no campo ou no objeto. O uso "
                        "do histórico como trilha de auditoria fica em 'Rastreabilidade e histórico'.",
                        E("src:dev-ldv-indexes", "src:help-field-history-tracking")),
    "avancado": [
        av("implantacao", "Onde ficam no metadado", "No CustomField, externalId, unique, caseSensitive, trackHistory, trackFeedHistory e "
           "trackTrending; no CustomObject, enableHistory, enableFeeds e historyRetentionPolicy.",
           E("src:mdapi-customfield", "src:mdapi-customobject")),
        av("escala", "Índices padrão e customizados", "A plataforma já indexa Id, Name, CreatedDate, Systemmodstamp, RecordTypeId, chaves "
           "estrangeiras e Email de contato e lead. External ID e Unique criam índice; índice em outros campos, inclusive padrão, é pedido ao "
           "Support. Um índice customizado só é usado se o filtro trouxer menos de 10% do primeiro milhão de registros e menos de 5% do resto.",
           E("src:dev-ldv-indexes", "src:help-custom-index-limit")),
        av("limite", "O que não indexa", "Não há índice customizado em text area long ou rich, fórmula não determinística nem texto criptografado. "
           "External ID só existe em Auto Number, Email, Number e Text. Por padrão, valores nulos ficam fora do índice. Marcar External ID ou "
           "Unique tem limite próprio, com padrão de 7 por objeto.", E("src:dev-ldv-indexes", "src:help-custom-index-limit")),
        av("decisao", "External ID ou Unique", "External ID cria índice e serve de chave no upsert, mas aceita valores repetidos. Unique impede "
           "repetição e também cria índice.", E("src:help-external-id-unique-index")),
        av("limite", "Histórico e feed", "O histórico de campos fica até 18 meses (24 pela API) sem Field Audit Trail. Atualizações de feed "
           "tracking com mais de 45 dias e sem interação são apagadas.", E("src:help-field-history-tracking", "src:help-chatter-feeds-overview")),
    ],
}

CONTEUDO_PENDENTES3 = P
