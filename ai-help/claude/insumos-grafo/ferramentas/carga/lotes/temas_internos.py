"""Issue #34, item 3 (limpeza do dado genérico dos temas internos), um tema principal por vez.

Para cada tema interno listado em TEMAS:
- "descricao": troca a frase genérica da carga inicial por uma descrição curta escrita pelo projeto (resumo do tema, sem
  fato técnico novo além dos já catalogados);
- "referencias_oficiais": áreas da documentação oficial já registradas em fontes/registro.json; cada nota começa com
  "Cobre o tema", "Cobre parte do tema" ou "Mais ampla que o tema" (o validador exige);
- "nota_estado": mesma redação dos temas principais. O "estado" continua "desconhecido": o recorte é do projeto e a
  conferência é parcial (o site passa a mostrar "Parcialmente conferido").

Não registra fontes novas: só cita fontes que já existem (o script aborta se alguma faltar).
Reexecutável. Uso: python3 ferramentas/carga/lotes/temas_internos.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from carga.base import ROOT, save, ev  # noqa: E402

DATA = "2026-11-10"  # data do primeiro cruzamento; rodadas seguintes mantêm a mesma nota
NOTA_ESTADO = ("Tema criado pelo projeto (00-especificacao-grafo.md), não é nomenclatura oficial da Salesforce. Cruzado em "
               + DATA + " com áreas da documentação oficial listadas nas referências; a correspondência é parcial e o recorte continua sendo do projeto.")

# id -> (descricao, [referências])
TEMAS = {
    # ------------------------------------------------------------------ Integração, APIs e eventos
    "sub:apis-de-dados-e-metadados": (
        "As APIs que a plataforma oferece para outros sistemas lerem e gravarem na org: REST e SOAP para registros, Bulk API para "
        "grandes volumes, Metadata API para configuração e Tooling API para ferramentas de desenvolvimento.",
        [ev("src:rest-intro", "Cobre parte do tema: REST API.", "Introduction to REST API"),
         ev("src:soap-intro", "Cobre parte do tema: SOAP API e os WSDLs Enterprise e Partner.", "Introduction to SOAP API"),
         ev("src:bulk-api-intro", "Cobre parte do tema: Bulk API 2.0 e Bulk API.", "Introduction to Bulk API 2.0 and Bulk API"),
         ev("src:mdapi-intro", "Cobre parte do tema: Metadata API.", "Understanding Metadata API"),
         ev("src:tooling-intro", "Cobre parte do tema: Tooling API.", "Introduction to Tooling API")],
    ),
    "sub:autenticacao-de-integracoes": (
        "Como um sistema externo prova quem é ao chamar a org: o registro da integração num external client app ou connected app e "
        "os tokens OAuth, com escopos, que esse registro emite.",
        [ev("src:help-eca-create", "Cobre parte do tema: external client apps, o registro recomendado para integrações novas.", "Create an External Client App"),
         ev("src:help-connected-app-basics", "Cobre parte do tema: connected apps.", "Configure Basic Connected App Settings")],
    ),
    "sub:chamadas-externas-e-endpoints": (
        "As chamadas que a org faz para serviços de fora e os endereços liberados para elas: sites remotos, serviços externos "
        "descritos em OpenAPI, conexões privadas e os limites de callout.",
        [ev("src:help-remote-site", "Cobre parte do tema: liberação de endereços para callouts.", "Configure Remote Site Settings"),
         ev("src:apex-callout-limits", "Cobre parte do tema: limites e restrições de callouts em Apex.", "Callout Limits and Limitations")],
    ),
    "sub:credenciais": (
        "Onde a org guarda o endereço de um sistema externo e a forma de se autenticar nele, fora do código: named credentials e, "
        "desde a versão 56.0, external credentials.",
        [ev("src:help-nc-create", "Cobre parte do tema: criação e edição de named credentials.", "Create or Edit a Named Credential"),
         ev("src:mdapi-externalcredential", "Cobre parte do tema: external credentials como metadado.", "ExternalCredential")],
    ),
    "sub:eventos-e-mensageria": (
        "Como a org avisa outros sistemas, e é avisada, sem consulta periódica: eventos de plataforma, eventos de captura de "
        "alterações, a Pub/Sub API para assinar de fora e o Event Relay.",
        [ev("src:help-platform-events-define", "Cobre parte do tema: definição de eventos de plataforma.", "Define and Manage Platform Events"),
         ev("src:pubsub-overview", "Cobre parte do tema: publicação e assinatura de eventos por clientes externos.", "Pub/Sub API overview"),
         ev("src:help-event-relay-create", "Cobre parte do tema: envio de eventos para a AWS.", "Create an Event Relay")],
    ),
    "sub:conectividade-e-virtualizacao-de-dados": (
        "Como mostrar dados de outro sistema dentro da org sem copiá-los: objetos externos, lidos no momento da consulta a partir "
        "de uma fonte de dados externa.",
        [ev("src:help-external-data-source-odata", "Cobre parte do tema: fonte de dados externa pelo adaptador OData do Salesforce Connect.",
            "Define an External Data Source for Salesforce Connect—OData 2.0 or 4.0 Adapter")],
    ),
    "sub:contratos-limites-e-tratamento-de-falhas": (
        "As regras que valem para toda integração: quantas chamadas cabem por dia, quanto tempo cada uma pode levar, quais versões "
        "de API continuam valendo e como tratar falhas e retentativas.",
        [ev("src:limits-api-requests", "Cobre parte do tema: alocações e limites de requisições de API.", "API Request Limits and Allocations"),
         ev("src:rest-api-eol", "Cobre parte do tema: política de fim de vida das versões de API.", "API End-of-Life Policy"),
         ev("src:pe-retry-apex", "Cobre parte do tema: retentativa em assinantes de eventos.")],
    ),
    # ------------------------------------------------------------------ Acesso, identidade e segurança
    "sub:usuarios-e-provisionamento": (
        "O cadastro de quem acessa a org, pessoa ou integração, e o seu ciclo de vida: criar, ativar, congelar e desativar usuários, "
        "inclusive pela criação automática no primeiro login com SSO.",
        [ev("src:help-users", "Cobre parte do tema: gestão de usuários no Setup.", "View and Manage Users"),
         ev("src:objref-user", "Cobre parte do tema: o objeto User na API.", "User")],
    ),
    "sub:autenticacao-sso-e-mfa": (
        "Como uma pessoa prova quem é ao entrar: senha, login único com o provedor da empresa (SAML) e provedores de autenticação "
        "como OpenID Connect, Google e Microsoft.",
        [ev("src:security-guide", "Cobre parte do tema: a seção de autenticação de usuários do guia de segurança.", "Authenticate Users"),
         ev("src:mdapi-samlssoconfig", "Cobre parte do tema: configuração de SSO por SAML como metadado.", "SamlSsoConfig"),
         ev("src:help-auth-provider-oidc", "Cobre parte do tema: provedor de autenticação por OpenID Connect.",
            "Configure an Authentication Provider Using OpenID Connect")],
    ),
    "sub:sessoes-e-politicas-de-login": (
        "As regras de entrada depois que a identidade foi provada: por qual endereço, de quais IPs e em quais horários se pode entrar, "
        "e o histórico e o estado de login de cada usuário.",
        [ev("src:help-mydomain-login-policy", "Cobre parte do tema: política de login do My Domain.", "Set the My Domain Login Policy"),
         ev("src:help-login-history", "Cobre parte do tema: acompanhamento do histórico de login.", "Monitor Login History")],
    ),
    "sub:permissoes-perfis-e-grupos": (
        "O que cada usuário pode fazer: o perfil, único por usuário, dá o acesso básico; permission sets somam acessos; permission set "
        "groups juntam vários para atribuir de uma vez.",
        [ev("src:help-perm-sets-create", "Cobre parte do tema: criação de permission sets.", "Create Permission Sets"),
         ev("src:help-psg-create", "Cobre parte do tema: criação de permission set groups.", "Create a Permission Set Group")],
    ),
    "sub:licencas-e-entitlements-de-acesso": (
        "O teto do que pode ser concedido a um usuário: a licença de usuário dá o pacote básico, e feature licenses e permission set "
        "licenses liberam recursos que ela não inclui.",
        [ev("src:help-user-licenses", "Cobre parte do tema: licenças de usuário padrão.", "Standard User Licenses"),
         ev("src:help-service-feature-license", "Cobre parte do tema: exemplo de feature license (Service Cloud User).",
            "Assign the Service Cloud User Feature License")],
    ),
    "sub:acesso-a-registros-e-hierarquias": (
        "Quais registros cada usuário enxerga: os padrões de acesso da org, o compartilhamento e as equipes de conta e de oportunidade.",
        [ev("src:security-guide", "Cobre parte do tema: as seções de acesso a dados e de compartilhamento do guia de segurança.",
            "Give Users Access to Data; Share Objects and Fields"),
         ev("src:mdapi-sharingsettings", "Cobre parte do tema: configurações de compartilhamento como metadado.", "SharingSettings")],
    ),
    "sub:credenciais-certificados-e-protecao-de-dados": (
        "Os segredos que protegem as conexões da org: certificados e chaves, a autenticação mútua e as credenciais de acesso a "
        "sistemas externos.",
        [ev("src:help-cert-self-signed", "Cobre parte do tema: certificados autoassinados.", "Generate a Self-Signed Certificate"),
         ev("src:mdapi-certificate", "Cobre parte do tema: certificados como metadado.", "Certificate")],
    ),
    # ------------------------------------------------------------------ Dados e modelagem
    "sub:objetos-e-entidades": (
        "As estruturas que guardam os registros: objetos padrão, que vêm com a Salesforce, e objetos customizados, criados para o que é "
        "próprio do negócio.",
        [ev("src:objref-data-model", "Cobre parte do tema: diagramas dos objetos padrão.", "Data Model"),
         ev("src:mdapi-customobject", "Cobre parte do tema: definição de objetos customizados como metadado.", "CustomObject")],
    ),
    "sub:campos-e-tipos": (
        "As informações de cada registro: o tipo de cada campo define o que ele aceita e quais propriedades usa, e regras de validação "
        "barram valores fora do esperado.",
        [ev("src:mdapi-customfield", "Cobre parte do tema: definição de campos customizados como metadado.", "CustomField"),
         ev("src:mdapi-field-types", "Cobre parte do tema: tipos compostos usados na definição dos campos.", "Metadata Field Types")],
    ),
    "sub:relacionamentos-e-juncoes": (
        "As ligações entre registros de objetos diferentes: lookup e master-detail, campos de resumo sobre os filhos e objetos de "
        "junção para relações de muitos para muitos.",
        [ev("src:mdapi-customfield", "Cobre parte do tema: propriedades de campos de relacionamento (tipo, exclusão do pai, junção).", "CustomField")],
    ),
    "sub:tipos-de-registro-e-processos-de-negocio": (
        "Variações de um mesmo objeto, cada uma com valores de lista, processo de negócio e páginas próprios.",
        [ev("src:mdapi-recordtype", "Cobre parte do tema: tipos de registro como metadado.", "RecordType"),
         ev("src:objref-recordtype", "Cobre parte do tema: o objeto RecordType na API.", "RecordType")],
    ),
    "sub:listas-de-valores": (
        "As listas fechadas de valores de um campo: valores próprios ou herdados de um conjunto global, picklists dependentes e o "
        "recorte de valores por tipo de registro.",
        [ev("src:mdapi-field-types", "Cobre parte do tema: estrutura ValueSet das picklists.", "Metadata Field Types"),
         ev("src:mdapi-recordtype", "Cobre parte do tema: valores de picklist por tipo de registro.", "RecordType")],
    ),
    "sub:metadados-de-configuracao-de-dados": (
        "Opções do campo ou do objeto que mudam como os dados se comportam, sem criar dados novos: índices, External ID e Unique, "
        "histórico de campos e feed tracking.",
        [ev("src:dev-ldv-indexes", "Cobre parte do tema: índices padrão e customizados.", "Indexes"),
         ev("src:help-field-history-tracking", "Cobre parte do tema: histórico de campos.", "Field History Tracking Overview")],
    ),
    "sub:modelos-externos-e-especializacoes": (
        "Formas especiais de modelar dados: objetos externos, que mostram dados de outro sistema sem copiá-los, e big objects, como o "
        "arquivo do histórico de campos.",
        [ev("src:help-external-data-source-odata", "Cobre parte do tema: objetos externos pelo adaptador OData do Salesforce Connect.",
            "Define an External Data Source for Salesforce Connect—OData 2.0 or 4.0 Adapter"),
         ev("src:help-field-audit-trail", "Cobre parte do tema: exemplo de big object (FieldHistoryArchive).", "Field Audit Trail")],
    ),
    # ------------------------------------------------------------------ Qualidade, governança e ciclo de vida dos dados
    "sub:validacao": (
        "Regras que barram, no momento de salvar, um registro cujos valores não atendem ao que o negócio exige.",
        [ev("src:help-validation-rules", "Cobre o tema: regras de validação.", "Validation Rules"),
         ev("src:mdapi-validationrule", "Cobre parte do tema: regra de validação como metadado.", "ValidationRule")],
    ),
    "sub:duplicidade-e-correspondencia": (
        "Como a org reconhece registros repetidos e o que faz com eles: matching rules definem a comparação, duplicate rules definem "
        "o alerta ou o bloqueio, e duplicate jobs procuram duplicados que já existem.",
        [ev("src:help-duplicate-management-customize", "Cobre o tema: gestão de duplicados com matching rules e duplicate rules.",
            "Customize Duplicate Management"),
         ev("src:help-duplicate-jobs-considerations", "Cobre parte do tema: duplicate jobs.", "Things to Know About Duplicate Jobs")],
    ),
    "sub:classificacao-e-sensibilidade": (
        "A marcação de cada campo com o nível de sensibilidade, a categoria de conformidade, o responsável e o uso, para orientar "
        "decisões de acesso e de conformidade.",
        [ev("src:help-data-classification-intro", "Cobre o tema: classificação de dados sensíveis.",
            "Classify Sensitive Data to Support Data Management Policies")],
    ),
    "sub:retencao-arquivamento-e-exclusao": (
        "Quanto tempo os dados ficam na org e o que acontece quando são apagados: Recycle Bin, exclusão definitiva e o prazo de guarda "
        "do histórico de campos.",
        [ev("src:help-recycle-bin-lex", "Cobre parte do tema: Recycle Bin.", "Manage the Recycle Bin in Lightning Experience"),
         ev("src:help-delete-unwanted-data", "Cobre parte do tema: graus de exclusão de dados.", "Delete Unwanted Data in a Salesforce Organization"),
         ev("src:help-field-audit-trail", "Cobre parte do tema: retenção do histórico de campos.", "Field Audit Trail")],
    ),
    "sub:rastreabilidade-e-historico": (
        "O registro de quem alterou cada campo rastreado, o valor anterior, o novo e a data, guardado num objeto de histórico ao lado "
        "do registro.",
        [ev("src:help-field-history-tracking", "Cobre o tema: histórico de campos.", "Field History Tracking Overview")],
    ),
    "sub:consentimento-e-privacidade": (
        "O registro do que cada pessoa autorizou sobre os próprios dados: se aceita contato, por qual canal, em qual endereço e para "
        "qual finalidade.",
        [ev("src:help-consent-data-model", "Cobre o tema: modelo de dados de consentimento.", "Understand the Salesforce Consent Data Model"),
         ev("src:help-consent-objects", "Cobre parte do tema: objetos de consentimento.", "Consent Management Objects")],
    ),
    # ------------------------------------------------------------------ Relatórios, analytics e exploração
    "sub:reports": (
        "Relatórios montados no report builder para responder perguntas sobre os registros da org: escolhe-se o tipo de relatório, o "
        "formato e os campos, e depois se agrupa, filtra e resume.",
        [ev("src:help-reports-overview", "Cobre o tema: relatórios.", "Reports"),
         ev("src:help-reports-build", "Cobre parte do tema: construção de relatórios.", "Build a Report")],
    ),
    "sub:dashboards": (
        "Painéis que mostram, em gráficos e tabelas, os resultados de relatórios de origem, com os dados vistos conforme o running user.",
        [ev("src:help-dashboards-build-lex", "Cobre parte do tema: construção de dashboards no Lightning Experience.",
            "Build a Lightning Experience Dashboard"),
         ev("src:help-dashboards-view-as", "Cobre parte do tema: visibilidade dos dados do dashboard.",
            "Configure Dashboard Data Visibility in Lightning Experience")],
    ),
    "sub:tipos-de-relatorio": (
        "A definição de quais registros e campos um relatório pode usar, a partir de um objeto principal e dos objetos relacionados a ele.",
        [ev("src:help-custom-report-types", "Cobre parte do tema: tipos de relatório customizados.", "Custom Report Types")],
    ),
    "sub:pastas-e-acesso": (
        "As pastas onde relatórios e dashboards ficam e os níveis de acesso (Viewer, Editor, Manager) dados a cada usuário, grupo ou papel.",
        [ev("src:help-folder-access-levels", "Cobre o tema: níveis de acesso em pastas de relatórios e dashboards.",
            "Access Levels for Report and Dashboard Folders"),
         ev("src:help-enhanced-folder-sharing", "Cobre parte do tema: enhanced folder sharing.", "Enhanced Folder Sharing for Reports and Dashboards")],
    ),
    "sub:metricas-e-agregacoes": (
        "Os cálculos feitos dentro de um relatório: totais e médias por grupo, fórmulas por registro, fórmulas sobre grupos e faixas "
        "de valores (bucket columns).",
        [ev("src:help-report-formulas", "Cobre o tema: fórmulas e resumos em relatórios.", "Evaluate Report Data with Formulas"),
         ev("src:help-add-bucket-column", "Cobre parte do tema: bucket columns.", "Add a Bucket Column")],
    ),
    "sub:recursos-analiticos-de-produto": (
        "Produtos analíticos que vão além dos relatórios nativos e dependem de licença própria, como CRM Analytics e Tableau.",
        [ev("src:help-produtos-analytics", "Mais ampla que o tema: diretório da documentação de Analytics, que inclui os relatórios nativos.", "Analytics"),
         ev("src:help-crm-analytics-collections", "Cobre parte do tema: assets do CRM Analytics.", "Collections of Data in CRM Analytics")],
    ),
    # ------------------------------------------------------------------ Organização e configurações base
    "sub:identificacao-e-configuracao-da-org": (
        "A ficha cadastral da org: dados da empresa, padrões de idioma, localidade, fuso e moeda, licenças compradas e o Organization "
        "ID que identifica a org.",
        [ev("src:help-company-info-fields", "Cobre o tema: campos da página Company Information.", "Manage Information About Your Company"),
         ev("src:help-setup-company", "Mais ampla que o tema: guia de configuração da empresa, que inclui idioma, moeda e ano fiscal.",
            "Set Up Your Company in Salesforce")],
    ),
    "sub:settings": (
        "A família de metadata types com nome terminado em Settings: cada um guarda um grupo de configurações da org num arquivo "
        ".settings e pode ser recuperado e implantado.",
        [ev("src:mdapi-settings", "Cobre o tema: a família Settings na Metadata API.", "Settings"),
         ev("src:mdapi-companysettings", "Cobre parte do tema: um dos tipos da família.", "CompanySettings")],
    ),
    "sub:parametros-reutilizaveis": (
        "Valores de configuração criados pela empresa e lidos por várias funcionalidades: custom metadata types, cujos registros são "
        "metadados, e custom settings, cujos registros são dados.",
        [ev("src:help-cmdt-about", "Cobre parte do tema: custom metadata types.", "What are Custom Metadata Types?"),
         ev("src:help-custom-settings", "Cobre parte do tema: custom settings.", "Define Custom Settings")],
    ),
    "sub:localizacao-idiomas-e-traducao": (
        "Em que língua e em que formato a org aparece para cada pessoa: idiomas oferecidos, localidade (formatos de data, hora e número) "
        "e tradução de rótulos customizados e custom labels.",
        [ev("src:help-language-locale-currency", "Mais ampla que o tema: idioma e localidade, junto com moeda.", "Language, Locale, and Currency Settings"),
         ev("src:help-supported-languages", "Cobre parte do tema: níveis de suporte a idioma.", "Supported Languages"),
         ev("src:help-translation-workbench", "Cobre parte do tema: tradução de rótulos.", "Translation Workbench"),
         ev("src:help-custom-labels", "Cobre parte do tema: custom labels.", "Custom Labels")],
    ),
    "sub:moedas-e-calendario-fiscal": (
        "As moedas em que a org registra valores, com moeda corporativa e taxas de conversão, e a forma de contar o ano fiscal: padrão "
        "ou customizado.",
        [ev("src:help-multicurrency-manage", "Cobre parte do tema: múltiplas moedas.", "Manage Multiple Currencies"),
         ev("src:help-fiscal-year-define", "Cobre parte do tema: ano fiscal padrão e customizado.", "Define Your Fiscal Year")],
    ),
    "sub:horarios-comerciais-e-feriados": (
        "Os dias, horários e fuso em que o atendimento funciona e os feriados que suspendem esse horário; outras regras usam os dois "
        "para contar prazos.",
        [ev("src:help-bh", "Cobre parte do tema: horários comerciais.", "Set Business Hours"),
         ev("src:help-holidays", "Cobre parte do tema: feriados.", "Set Up Support Holidays")],
    ),
    "sub:dominios-e-urls": (
        "Os endereços pelos quais pessoas e integrações chegam à org: o My Domain, que põe o nome da empresa nas URLs de login e de "
        "aplicação, e os custom domains dos sites.",
        [ev("src:help-mydomain", "Cobre parte do tema: My Domain.", "My Domain"),
         ev("src:help-domains-view", "Cobre parte do tema: custom domains e system-managed domains.", "View Your Custom Domain Details")],
    ),
    "sub:habilitacao-de-recursos": (
        "A ativação de recursos opcionais no Setup. Alguns mudam o comportamento ou o modelo de dados da org e não podem ser desligados "
        "depois; muitas ativações ficam gravadas em tipos da família Settings.",
        [ev("src:mdapi-settings", "Cobre parte do tema: ativações gravadas como metadado na família Settings.", "Settings"),
         ev("src:help-lightning-knowledge-enable", "Cobre parte do tema: exemplo de ativação sem volta.", "Create a Knowledge Base with Salesforce Knowledge")],
    ),
    # ------------------------------------------------------------------ Processos de negócio específicos de produto
    "sub:vendas": (
        "O processo de vendas: leads, contas, contatos e oportunidades, com produtos e catálogos de preço, cotações, contratos, "
        "previsões, equipes e territórios.",
        [ev("src:help-sales-basics", "Mais ampla que o tema: guia de base de vendas, que inclui recursos de plataforma.", "Sales Basics"),
         ev("src:help-lead-settings", "Cobre parte do tema: configurações padrão de leads.", "Define Default Settings for Lead Creation"),
         ev("src:help-contracts-setup", "Cobre parte do tema: contratos.", "Set Up Contracts")],
    ),
    "sub:atendimento": (
        "O processo de atendimento: o caso como registro central, o roteamento pelo Omni-Channel, o conhecimento que apoia as "
        "respostas e os níveis de serviço medidos por entitlements.",
        [ev("src:help-service-basics", "Mais ampla que o tema: guia de base de atendimento.", "Service Basics")],
    ),
    "sub:servico-de-campo": (
        "Field Service: o trabalho feito no local do cliente, com work orders, visitas agendadas (service appointments), técnicos "
        "(service resources) e territórios de serviço.",
        [ev("src:help-field-service-overview", "Cobre o tema: visão geral do Field Service.", "Agentforce Field Service and Operations"),
         ev("src:help-field-service-enable", "Cobre parte do tema: ativação.", "Enable Field Service")],
    ),
    "sub:receita-e-comercio": (
        "O que vem depois da venda acertada: pedidos (orders) na plataforma padrão e os produtos de preço, assinatura e faturamento, "
        "como Salesforce CPQ, Salesforce Billing e Revenue Management.",
        [ev("src:help-orders-enable", "Cobre parte do tema: pedidos.", "Enable Orders"),
         ev("src:help-revenue-get-started", "Cobre parte do tema: Revenue Management.", "Get Started with Revenue Management"),
         ev("src:help-billing-overview", "Cobre parte do tema: Salesforce Billing.", "Salesforce Billing Overview")],
    ),
    "sub:experiencias-externas": (
        "O acesso de clientes e parceiros por sites Experience Cloud: a ativação de digital experiences, as licenças de usuário "
        "externo e o que cada uma permite ver e fazer.",
        [ev("src:help-experience-cloud-licenses", "Cobre parte do tema: licenças de usuário externo.", "Experience Cloud User Licenses"),
         ev("src:help-digital-experiences-enable", "Cobre parte do tema: ativação dos sites.", "Enable Digital Experiences")],
    ),
    "sub:capacidades-setoriais": (
        "O que as nuvens de setor, como Financial Services Cloud e Health Cloud, acrescentam ao modelo padrão: objetos, campos e "
        "recursos próprios, liberados por permission set licenses.",
        [ev("src:help-industries-data-models", "Cobre parte do tema: modelo de dados de seguros e serviços financeiros, como exemplo de nuvem setorial.",
            "Insurance and Financial Services Data Model")],
    ),
    "sub:outras-areas": (
        "Agrupamento provisório deste tutorial para tipos da lista oficial de metadata types que ainda não têm tema próprio; não é uma "
        "área oficial da Salesforce.",
        [ev("src:sdr-metadata-support", "Mais ampla que o tema: lista oficial de metadata types suportados pelo Salesforce CLI, de onde vêm os "
            "itens deste agrupamento.", "METADATA_SUPPORT.md")],
    ),
}


def aplicar():
    with open(os.path.join(ROOT, "..", "fontes", "registro.json"), encoding="utf-8") as f:
        fontes = {x["id"] for x in json.load(f)["fontes"]}
    faltam = sorted({r["fonte"] for _, refs in TEMAS.values() for r in refs} - fontes)
    if faltam:
        raise SystemExit(f"fontes não registradas: {faltam}")
    d = os.path.join(ROOT, "subclassificacoes")
    for tid, (descricao, refs) in TEMAS.items():
        nome = tid.split(":", 1)[1]
        caminho = os.path.join(d, nome + ".json")
        if not os.path.exists(caminho):
            raise SystemExit(f"tema inexistente: {tid}")
        with open(caminho, encoding="utf-8") as f:
            ent = json.load(f)
        ent["descricao"] = descricao
        ent["referencias_oficiais"] = refs
        ent["nota_estado"] = NOTA_ESTADO
        save("subclassificacoes", nome, ent)
    print(f"temas internos atualizados: {len(TEMAS)}")


if __name__ == "__main__":
    aplicar()
