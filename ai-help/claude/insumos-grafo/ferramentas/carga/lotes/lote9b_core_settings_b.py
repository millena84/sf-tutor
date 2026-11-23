"""Lote 9b (#10, etapa 3, lote B; 2026-11-23): cadastro de 10 tipos Settings já incluídos no Core e ainda sem ficha.

Páginas versionadas 264.0 do Metadata API Developer Guide (endpoint get_document_content). Estrutura e explicação na mesma passada.
Classificação funcional como no lote 9a: funcionalidade existente do mesmo assunto ou funcionalidade nova com a página como fonte.
Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import af                     # noqa: E402
from carga import catalogo as C               # noqa: E402
from carga import mdt as M                    # noqa: E402
from carga.mdt import mdt, P, struct, emit_structs   # noqa: E402

DATA = "2026-11-23"
EXTR = "fontes/extracoes/lote9b-core-settings-b.txt"
G = "https://developer.salesforce.com/docs/get_document_content/api_meta/"


def S(nome):
    return "src:mdapi-" + nome.lower()


TIPOS = ["ActivitiesSettings", "AddressSettings", "EmailAdministrationSettings", "EmailAuthorizationSettings",
         "FileUploadAndDownloadSecuritySettings", "IdentityProviderSettings", "SearchSettings", "SiteSettings",
         "UserInterfaceSettings", "UserEngagementSettings"]
C.registrar_fontes([C.fonte(S(n), f"{n} (Metadata API 264.0)", G + f"meta_{n.lower()}.htm/en-us/264.0",
                            f"Descrição, arquivo, versão e tabela Fields do tipo {n} (página lida por inteiro).", EXTR, DATA, versao="264.0")
                    for n in TIPOS])

FALSE = ("false", False, "A página declara default false.")
TRUE = ("valor", "true", "A página declara default true.")
PKG = "No package.xml, use o tipo Settings com o nome-base do arquivo como membro; o curinga só vale para recuperar todas as configurações."
FN = M.FULLNAME_HERDADO(None)
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
SO_CLASSIC = "Só no Salesforce Classic, segundo a página."
SO_LEX = "Só no Lightning Experience, segundo a página."


def exemplo(nome, pares):
    corpo = "\n".join(f"    <{k}>{v}</{k}>" for k, v in pares)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<{nome} {NS}>\n{corpo}\n</{nome}>'


def settings(nome, base, o_que_e, finalidade, desde, linhas, ex, alertas=(), extra_nota="", **kw):
    n = len(linhas)
    nota = (f"Universo esperado = tabela Fields da página 264.0 ({n} campo{'s' if n > 1 else ''}), lida em {DATA} "
            f"(mais fullName herdado, declarado na página).{extra_nota}")
    arq = M.arquivos_settings(nome, base, S(nome))
    return mdt(nome, S(nome), o_que_e, finalidade, desde, list(linhas) + [FN], arquivos_prontos=arq, curinga=False,
               alertas=[PKG] + list(alertas), cobertura_nota=nota, exemplo=exemplo(nome, ex), **kw)


# ---------------------------------------------------------------- ActivitiesSettings
ADM = "A página diz que o administrador controla a opção na tela Activity Settings."
ADM_UI = "A página diz que o administrador controla a opção nas configurações de User Interface."
settings("ActivitiesSettings", "Activities",
         "Configurações de atividades (tarefas e eventos) da org e da interface do calendário.",
         "Recuperar e implantar como tarefas, eventos, lembretes e calendário se comportam, em vez de ligar cada opção à mão.", "28.0", [
             P("allowUsersToRelateMultipleContactsToTasksAndEvents", "boolean", None, "Indica se Shared Activities está ligado: com true, vários "
               "contatos podem ser relacionados a uma tarefa ou evento.",
               notas=["Somente leitura desde a API 36.0: mudar o valor não é suportado e pode quebrar integrações; código antigo que altera o campo deve ser revisto."]),
             P("autoRelateEventAttendees", "boolean", "42.0", "Ao adicionar participantes a um evento, relaciona o evento automaticamente a até 50 "
               "contatos ou a um lead, casando pelo e-mail.", notas=[ADM]),
             P("enableActivityReminders", "boolean", None, "Liga os lembretes pop-up de atividades na org.", notas=[ADM]),
             P("enableCalendarHomeLWC", "boolean", None, "Usa Lightning Web Components no calendário, o que aumenta o limite de itens na página "
               "inicial do calendário e melhora a leitura.", notas=[ADM]),
             P("enableClickCreateEvents", "boolean", None, "Permite criar eventos nas visões diária e semanal com duplo clique num horário, "
               "preenchendo os detalhes numa janela sobreposta; os campos vêm do mini page layout. Não vale para eventos recorrentes nem com "
               "várias pessoas.", notas=[ADM_UI]),
             P("enableDragAndDropScheduling", "boolean", None, "Permite criar um evento ligado a um registro arrastando o registro de uma list view "
               "para o calendário e preenchendo os detalhes numa janela sobreposta.", notas=[ADM_UI]),
             P("enableEmailTracking", "boolean", None, "Liga o rastreamento de e-mails HTML enviados, quando a org usa modelos de e-mail HTML.",
               notas=[ADM]),
             P("enableFlowTaskNotifsViaApex", "boolean", None, "Quando Apex aciona o Process Builder para criar uma tarefa, define se o responsável "
               "recebe e-mail (true) ou não (false)."),
             P("enableGroupTasks", "boolean", None, "Permite atribuir cópias independentes de uma tarefa nova a vários usuários.", notas=[ADM]),
             P("enableHideChildEventsPreference", "boolean", "50.0", "Permite esconder eventos filhos nas visões de calendário e de atividades, "
               "útil em hierarquias complexas.", notas=[ADM]),
             P("enableListViewScheduling", "boolean", None, "Estende o arrastar-e-soltar e o duplo clique para criar eventos aos calendários de "
               "list view.", notas=[ADM_UI]),
             P("enableLogNote", "boolean", None, "Permite criar uma nota e associá-la a um registro existente."),
             P("enableMLSingleClientProfile", "boolean", "50.0", "Liga a criação de perfil de cliente por machine learning, que analisa e consolida "
               "dados de clientes.", notas=[ADM]),
             P("enableMultidayEvents", "boolean", None, "Permite eventos que terminam mais de 24 horas depois do início.", notas=[ADM]),
             P("enableRecurringEvents", "boolean", None, "Permite eventos que se repetem em intervalos definidos.", notas=[ADM]),
             P("enableRecurringTasks", "boolean", None, "Permite tarefas que se repetem em intervalos definidos.", notas=[ADM]),
             P("enableRollUpActivToContactsAcct", "boolean", "47.0", "Soma as atividades de um contato e as mostra também na conta principal "
               "dele.", default=TRUE),
             P("enableSidebarCalendarShortcut", "boolean", None, "Mostra na barra lateral um atalho para a última visão de calendário usada.",
               notas=[ADM]),
             P("enableSimpleTaskCreateUI", "boolean", None, "Define se New Task abre a página de edição normal ou uma página que mostra primeiro "
               "os campos principais.", notas=[ADM]),
             P("enableTimelineCompDateSort", "boolean", None, "Ordena as atividades passadas pela data de conclusão (true) ou pela data de "
               "vencimento (false).", notas=[ADM]),
             P("enableUNSTaskDelegatedToNotifications", "boolean", None, "Mostra ou esconde a opção que deixa cada usuário ligar ou desligar o "
               "e-mail recebido quando uma tarefa é atribuída a ele."),
             P("enableUserListViewCalendars", "boolean", "47.0", "Permite criar e ver calendários de list view de usuários no Lightning Experience."),
             P("meetingRequestsLogo", "string", None, "Logo usado nas solicitações de reunião, escolhido entre os enviados a certas pastas da aba "
               "Documents. Só vale com showCustomLogoMeetingRequests ligado.", notas=[ADM]),
             P("showCustomLogoMeetingRequests", "boolean", None, "Mostra um logo personalizado nos e-mails de solicitação de reunião e na página "
               "da reunião vista pelos convidados.", notas=[ADM]),
             P("showEventDetailsMultiUserCalendar", "boolean", None, "Mostra os detalhes dos eventos na própria tela, em vez de só ao passar o "
               "mouse.", notas=[ADM]),
             P("showHomePageHoverLinksForEvents", "boolean", None, "Na seção de calendário da aba Home, mostra detalhes do evento ao passar o "
               "mouse sobre o assunto e abre o evento ao clicar.", notas=[ADM_UI]),
             P("showMyTasksHoverLinks", "boolean", None, "Na seção My Tasks da Home e na visão diária do calendário, mostra detalhes da tarefa ao "
               "passar o mouse e abre a tarefa ao clicar.", notas=[ADM_UI]),
         ], [("enableRecurringTasks", "true"), ("enableGroupTasks", "true")])

# ---------------------------------------------------------------- AddressSettings
INTEG = ("Texto personalizável ligado ao código ISO, para que integrações feitas antes da ativação das picklists continuem funcionando. "
         "Se não for definido antes da ativação, vale o valor padrão da Salesforce; mudanças depois só afetam registros criados ou atualizados a partir daí.")
DEF_INTEG = ("valor", None, "Para itens padrão, o nome completo do padrão ISO, segundo a página.")
DEF_ISO = ("valor", None, "Preenchido pela Salesforce no retrieve(), segundo a página.")
struct("State", S("AddressSettings"), ["mdt:AddressSettings"], [
    P("active", "boolean", None, "Define se o estado fica disponível na API. Depois de ativar as picklists de estado e país na org, não pode voltar a false."),
    P("integrationValue", "string", None, INTEG, default=DEF_INTEG),
    P("isoCode", "string", None, "Código ISO do estado.", default=DEF_ISO),
    P("label", "string", None, "Rótulo do estado mostrado aos usuários na picklist."),
    P("standard", "boolean", None, "Indica se o estado vem da Salesforce; não é editável."),
    P("visible", "boolean", None, "Mostra o estado aos usuários. Exige active em true."),
], o_que_e="Um estado ou província de um país, com rótulo, código ISO e se está ativo e visível.")
struct("Country", S("AddressSettings"), ["mdt:AddressSettings"], [
    P("active", "boolean", None, "Define se o país ou território fica disponível na API. Depois de ativar as picklists na org, não pode voltar a false."),
    P("integrationValue", "string", None, INTEG, default=DEF_INTEG),
    P("isoCode", "string", None, "Código ISO do país ou território.", default=DEF_ISO),
    P("label", "string", None, "Rótulo do país ou território mostrado aos usuários na picklist."),
    P("orgDefault", "boolean", None, "Define o país ou território como padrão para registros novos da org."),
    P("standard", "boolean", None, "Indica se o país vem da Salesforce; não é editável."),
    P("states", "State[]", None, "Estados ou províncias do país ou território.", estrutura="State"),
    P("visible", "boolean", None, "Mostra o país ou território aos usuários. Exige active em true."),
], o_que_e="Um país ou território das picklists de endereço, com seus estados.")
struct("CountriesAndStates", S("AddressSettings"), ["mdt:AddressSettings"], [
    P("countries", "Country[]", None, "Países e territórios disponíveis nas picklists.", estrutura="Country"),
], o_que_e="O conjunto de países, territórios e estados das picklists de endereço.")
mdt("AddressSettings", S("AddressSettings"),
    "Configuração das picklists de estado e país/território, que trocam o texto livre dos endereços por valores padronizados.",
    "Recuperar e implantar a lista de países, territórios e estados (rótulos, códigos e visibilidade) entre ambientes.", "27.0", [
        P("countriesAndStates", "CountriesAndStates", None, "Países, territórios e estados configurados nas picklists.", estrutura="CountriesAndStates",
          notas=["A página não tem tabela de campos do tipo raiz; o nome do elemento vem do exemplo XML e o tipo, da seção do subtipo CountriesAndStates."]),
        FN,
    ], arquivos_prontos=M.arquivos_settings("AddressSettings", "Address", S("AddressSettings")), curinga=False,
    alertas=[PKG, "Pela Metadata API dá para criar e editar países, territórios e estados, mas não excluí-los.",
             "Depois de ativar as picklists de estado e país na org, active não pode voltar a false."],
    cobertura_nota=f"Universo esperado = elemento countriesAndStates do exemplo XML (a página não tem tabela do tipo raiz) mais fullName herdado; "
                   f"subtipos CountriesAndStates (1), Country (8) e State (6) lidos em {DATA}.",
    exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<AddressSettings {NS}>\n    <countriesAndStates>\n        <countries>\n'
            f'            <active>true</active>\n            <integrationValue>Brasil</integrationValue>\n            <isoCode>BR</isoCode>\n'
            f'            <label>Brasil</label>\n            <visible>true</visible>\n        </countries>\n    </countriesAndStates>\n</AddressSettings>')

# ---------------------------------------------------------------- EmailAdministrationSettings
settings("EmailAdministrationSettings", None,
         "Configurações de administração de e-mail da org: entrega, conformidade de segurança, relay e notificações do sistema.",
         "Recuperar e implantar as regras de envio e recebimento de e-mail da org, em vez de repetir a tela de Deliverability à mão.", "47.0", [
             P("enableComplianceBcc", "boolean", None, "Envia uma cópia oculta de cada e-mail enviado a um endereço de conformidade. Só funciona "
               "com o endereço preenchido em Compliance BCC Email, no Setup.", default=FALSE),
             P("enableEmailConsentManagement", "boolean", None, "Liga Enforce Email Privacy Settings: o Salesforce respeita as preferências de "
               "privacidade de e-mail de cada destinatário.", default=FALSE),
             P("enableEmailSenderIdCompliance", "boolean", None, "Faz os e-mails enviados seguirem o protocolo Sender ID. Exige "
               "enableEmailSpfCompliance em true; a página recomenda avaliar SPF, DKIM e DMARC antes.", default=FALSE),
             P("enableEmailSpfCompliance", "boolean", None, "Faz os e-mails enviados seguirem a autenticação SPF (Sender Policy Framework).",
               default=TRUE),
             P("enableEmailToSalesforce", "boolean", None, "Liga o Email to Salesforce.", default=FALSE),
             P("enableEmailWorkflowApproval", "boolean", None, "Permite responder a pedidos de aprovação direto pelo e-mail. A página recomenda "
               "ler as considerações sobre aprovação por e-mail antes.", default=FALSE),
             P("enableEnhancedEmailEnabled", "boolean", None, "Indica se o Enhanced Email está ligado.", default=TRUE),
             P("enableHandleBouncedEmails", "boolean", None, "Faz e-mails enviados a endereços inválidos voltarem ao Salesforce, mostrando qual "
               "lead, contato ou conta pessoal tem endereço inválido e qual e-mail não foi entregue.", default=TRUE),
             P("enableHtmlEmail", "boolean", None, "Define se os e-mails do Email-to-Case chegam aos usuários em HTML (true, com aviso sobre "
               "possível HTML malicioso) ou em texto (false).", default=FALSE),
             P("enableInternationalEmailAddresses", "boolean", "49.0", "Permite caracteres não latinos nos endereços de e-mail enviados e "
               "recebidos. A página recomenda revisar pré-requisitos e considerações na Ajuda antes.",
               default=("valor", None, "true em orgs criadas a partir do Summer '20; false nas criadas até o Spring '20.")),
             P("enableListEmailLogActivities", "boolean", None, "Registra como atividades os e-mails de lista enviados.", default=TRUE),
             P("enableResendBouncedEmails", "boolean", None, "Envia ao remetente uma cópia de cada e-mail devolvido (true) ou só mostra o alerta "
               "de devolução (false). Exige enableHandleBouncedEmails em true.", default=FALSE),
             P("enableRestrictTlsToDomains", "boolean", None, "Aplica a configuração de TLS escolhida só a domínios listados (true) ou a todos "
               "(false). Exige uma TLS Setting diferente de Preferred e a lista de domínios em Deliverability; os demais domínios usam Preferred.",
               default=FALSE),
             P("enableSendThroughGmailPref", "boolean", None, "Obsoleto, segundo a página, que não traz outra descrição."),
             P("enableSendViaExchangePref", "boolean", None, "Permite que os usuários enviem e-mails pelo Office 365.", default=FALSE),
             P("enableSendViaGmailPref", "boolean", None, "Permite que os usuários enviem e-mails pelo Gmail.", default=FALSE),
             P("enableUseOrgFootersForExtTrans", "boolean", None, "Inclui o rodapé do Salesforce nos e-mails enviados por serviços externos, "
               "como Gmail ou Office 365.", default=FALSE),
             P("sendMassEmailNotification", "boolean", None, "Manda ao usuário um e-mail automático de status para cada e-mail em massa enviado.",
               default=TRUE),
             P("sendTextOnlySystemEmails", "boolean", None, "Envia todos os e-mails do sistema só em texto (true) ou permite outros formatos "
               "(false).", default=FALSE),
         ], [("enableEmailSpfCompliance", "true"), ("enableHandleBouncedEmails", "true")],
         divergencias=["A página (src:mdapi-emailadministrationsettings) escreve o arquivo como EmailAdminstration.settings (sem o \"i\"), "
                       "enquanto o membro do package.xml é EmailAdministration. O catálogo não registra o nome do arquivo."])

settings("EmailAuthorizationSettings", "EmailAuthorization",
         "Configurações de autorização de e-mail da org.",
         "Recuperar e implantar o que acontece com e-mails enviados de domínios não verificados.", "66.0", [
             P("enableSubstituteFromAddress", "boolean", None, "Com true, o Salesforce troca o remetente (From) dos e-mails enviados de domínios "
               "não verificados por um endereço do tipo email@<id>.sfcustomeremail.com, em que o id é o da org ou do site do Experience Cloud. "
               "Com false, usuários e automações só enviam se o domínio estiver verificado. Vale só para e-mails que exigem verificação de "
               "domínio; as exceções estão na Ajuda.", default=FALSE),
         ], [("enableSubstituteFromAddress", "true")],
         extra_nota=" A página diz que o tipo estende MetadataForSettings.")

# ---------------------------------------------------------------- FileUploadAndDownloadSecuritySettings
struct("FileTypeDispositionAssignmentBean", S("FileUploadAndDownloadSecuritySettings"), ["mdt:FileUploadAndDownloadSecuritySettings"], [
    P("behavior", "FileDownloadBehavior", None, "Como o arquivo é tratado ao ser aberto: baixar, executar no navegador ou híbrido. Tipos de risco "
      "(EXE, FLASH, HTML, RFC822, SVG, TXML, UNKNOWN, WEBVIEW, XHTML e XML) não podem ser EXECUTE.",
      vals=[("DOWNLOAD", "baixar"), ("EXECUTE", "executar"), ("HYBRID", "híbrido")]),
    P("filetype", "FileType", None, "Tipo de arquivo ao qual a regra se aplica. A página diz que existem outros tipos, mas só estes são aceitos aqui.",
      vals=[(v, None) for v in "AVI EXCEL EXCEL_X EXE FLASH HTML INSIGHT MOV MP3 MP4 MPEG PDF POWER_POINT POWER_POINT_X RFC822 SVG TXML UNKNOWN "
                               "WAV WEBVIEW WMA WMV WORD WORD_X XHTML XML".split()]),
    P("securityRiskFileType", "boolean", None, "Indica se o tipo de arquivo é de risco e por isso não pode ser EXECUTE. Somente leitura."),
], o_que_e="Regra de comportamento para um tipo de arquivo: baixar, executar ou híbrido.")
settings("FileUploadAndDownloadSecuritySettings", None,
         "Configurações de segurança para envio e download de arquivos.",
         "Recuperar e implantar como cada tipo de arquivo é aberto (baixar ou executar) e se HTML pode ser enviado como anexo.", "39.0", [
             P("dispositions", "FileTypeDispositionAssignmentBean[]", "39.0", "Regras de comportamento por tipo de arquivo.",
               estrutura="FileTypeDispositionAssignmentBean"),
             P("noHtmlUploadAsAttachment", "boolean", "39.0", "Define se uploads de HTML podem ser aceitos como anexos ou registros de documento."),
         ], [("noHtmlUploadAsAttachment", "false")],
         extra_nota=" Subtipo FileTypeDispositionAssignmentBean com 3 campos. A leitura não deu o nome-base do arquivo.")

settings("IdentityProviderSettings", "IdentityProvider",
         "Configurações que ligam ou desligam a Salesforce como provedor de identidade SAML para single sign-on (SSO).",
         "Recuperar e implantar se a org atua como provedor de identidade e qual certificado usa.", "57.0", [
             P("certificateName", "string", None, "Certificado que a Salesforce usa para falar com os provedores de serviço SAML (de terceiros ou "
               "outra org Salesforce). Pode ser autoassinado ou assinado por autoridade certificadora.", "S",
               natureza="referencia", contexto="Nome de um certificado da org."),
             P("enableIdentityProvider", "boolean", None, "Indica se a Salesforce pode ser usada como provedor de identidade SAML.", "S"),
         ], [("certificateName", "MeuCertificado"), ("enableIdentityProvider", "true")],
         alertas=["Acesso: exige a permissão Customize Application."])

# ---------------------------------------------------------------- SearchSettings
OBR = "S"
struct("ObjectSearchSetting", S("SearchSettings"), ["mdt:SearchSettings"], [
    P("enhancedLookupEnabled", "boolean", None, "Liga os lookups aprimorados para o objeto.", OBR),
    P("lookupAutoCompleteEnabled", "boolean", None, "Liga o autocompletar no campo de lookup: o usuário escolhe uma sugestão enquanto digita.", OBR),
    P("name", "string", None, "Nome do objeto configurado.", OBR),
    P("resultsPerPageCount", "int", None, "Quantidade de resultados de busca por página.", OBR),
], o_que_e="Configuração de busca e lookup de um objeto.")
struct("SearchSettingsByObject", S("SearchSettings"), ["mdt:SearchSettings"], [
    P("searchSettingsByObject", "ObjectSearchSetting", None, "Configurações de busca de cada objeto.", estrutura="ObjectSearchSetting"),
], o_que_e="Lista das configurações de busca por objeto.")
settings("SearchSettings", "Search",
         "Configurações de busca da org.",
         "Recuperar e implantar o comportamento da busca global, da barra lateral, dos lookups e da Einstein Search.", "37.0", [
             P("documentContentSearchEnabled", "boolean", None, "Faz busca de texto completo dentro de documentos."),
             P("enableAdvancedSearchInAlohaSidebar", "boolean", "46.0", "Mostra a busca avançada na barra lateral.", notas=[SO_CLASSIC]),
             P("enableEinsteinSearchAssistantDialog", "boolean", "50.0", "Liga a experiência de busca da Einstein Search."),
             P("enableEinsteinSearchEs4kPilot", "boolean", "54.0", "Liga as melhorias da Einstein Search para Knowledge (GA desde o Winter '23).",
               default=("valor", "true", "true na API 56.0 e posteriores, segundo a página.")),
             P("enableEinsteinSearchNaturalLanguage", "boolean", "50.0", "Liga a busca em linguagem natural."),
             P("enableEinsteinSearchNLSFilters", "boolean", "54.0", "Liga os filtros de busca em linguagem natural (piloto)."),
             P("enableEinsteinSearchPersonalization", "boolean", "47.0", "Liga a personalização dos resultados de busca.", notas=[SO_LEX]),
             P("enablePersonalTagging", "boolean", "48.0", "Permite agrupar registros de vários objetos com tags pessoais, visíveis só ao próprio "
               "usuário.", notas=[SO_CLASSIC]),
             P("enablePublicTagging", "boolean", "48.0", "Permite agrupar registros com tags públicas.", notas=[SO_CLASSIC]),
             P("enableSalesforceGeneratedSynonyms", "boolean", "47.0", "Liga os sinônimos de busca gerados pela Salesforce."),
             P("enableSearchTermHistory", "boolean", "48.0", "Pelo nome, liga o histórico de termos buscados; a descrição da página repete o texto "
               "das tags, então o efeito exato não está confirmado.", notas=[SO_CLASSIC]),
             P("enableSetupSearch", "boolean", "47.0", "Faz a caixa de busca do Setup devolver campos, objetos e outros itens de configuração ao "
               "pressionar Enter.", default=("valor", None, "true nas edições Developer, Performance, Professional, Enterprise e Unlimited; false nas demais.")),
             P("enableSuggestArticlesLinksOnly", "boolean", "48.0", "Mostra links para artigos de Knowledge vindos de casos parecidos com o atual."),
             P("enableUseDefaultSearchEntity", "boolean", "48.0", "Faz a busca da barra lateral usar o objeto padrão definido pelo administrador.",
               notas=[SO_CLASSIC]),
             P("optimizeSearchForCJKEnabled", "boolean", None, "Otimiza a busca para japonês, chinês e coreano (barra lateral, busca de contas em "
               "Find Duplicates de leads e busca global). Indicado quando usuários e textos estão sobretudo nesses idiomas.", OBR),
             P("recentlyViewedUsersForBlankLookupEnabled", "boolean", None, "No lookup de usuário em branco, mostra os usuários que o próprio "
               "usuário viu recentemente (true) ou os acessados recentemente na org (false).", OBR),
             P("searchSettingsByObject", "SearchSettingsByObject", None, "Configurações de busca de cada objeto.", OBR, estrutura="SearchSettingsByObject"),
             P("sidebarAutoCompleteEnabled", "boolean", None, "Liga o autocompletar na busca da barra lateral, sugerindo registros vistos "
               "recentemente.", OBR),
             P("sidebarDropDownListEnabled", "boolean", None, "Mostra na barra lateral a lista para buscar em tags, num objeto ou em todos.", OBR),
             P("sidebarLimitToItemsIOwnCheckboxEnabled", "boolean", None, "Mostra a caixa Limit to Items I Own, que restringe a busca aos registros "
               "do próprio usuário.", OBR),
             P("singleSearchResultShortcutEnabled", "boolean", None, "Com um único resultado, abre direto o registro, sem a página de resultados. "
               "Não vale para tags, comentários de caso e busca global.", OBR),
             P("spellCorrectKnowledgeSearchEnabled", "boolean", None, "Liga a correção ortográfica na busca de Knowledge.", OBR),
         ], [("enableSetupSearch", "true"), ("sidebarAutoCompleteEnabled", "true")],
         divergencias=["Na página (src:mdapi-searchsettings), a descrição de enableSearchTermHistory repete o texto de agrupamento de registros "
                       "por tags e não combina com o nome do campo; a de enablePublicTagging repete trecho das tags pessoais. O catálogo registra "
                       "a dúvida em vez de copiar o texto."])

# ---------------------------------------------------------------- SiteSettings
settings("SiteSettings", "Site",
         "Configurações dos sites do Experience Cloud e do Salesforce Sites.",
         "Recuperar e implantar opções gerais dos sites, como a plataforma aprimorada de sites e conteúdo.", "47.0", [
             P("enableEnhancedSitesAndContentPlatform", "boolean", "56.0", "Liga a plataforma aprimorada de sites e conteúdo do Experience Cloud: "
               "sites LWR novos e workspaces de CMS aprimorados passam a ter implantação parcial, busca de conteúdo e gestão de conteúdo mais "
               "simples. Esses sites são representados por DigitalExperienceBundle e DigitalExperienceConfig.", default=TRUE),
             P("enableExpBuilderCopilot", "boolean", "64.0", "Liga o Agentforce (beta) no Experience Builder para sites LWR aprimorados. O uso "
               "consome Einstein Requests.", default=FALSE, notas=["Serviço beta/piloto, sujeito aos termos de serviços beta."]),
             P("enableExperienceFriendlyUrls", "boolean", "58.0", "Liga slugs de URL amigáveis para SEO; só ficam disponíveis em sites LWR do B2C "
               "Commerce.", default=FALSE, ate="58.0", notas=["Na API 59.0 e posteriores, a página manda usar expFriendlyUrlsAsDefault no tipo Network."]),
             P("enableProxyLoginICHeader", "boolean", None, "Indica se tokens de segurança são exigidos em logins de API feitos a partir de callouts.",
               default=TRUE, ate="31.0"),
             P("enableSitesRecordReassignOrgPref", "boolean", "48.0", "Com true, registros criados por usuários guest do site passam a um "
               "proprietário padrão; com false, o usuário guest continua como proprietário.", default=FALSE,
               notas=["A página diz que o campo está descontinuado a partir da API 63.0."]),
             P("enableTopicsInSites", "boolean", None, "Permite que usuários guest e usuários externos autenticados vejam tópicos no Salesforce "
               "Sites e nos portais.", default=FALSE),
             P("enableVisualforceApiAccessAllowed", "boolean", None, "Permite que usuários de páginas Visualforce passem pelas restrições de acesso "
               "às APIs quando enableAdminApprovedAppsOnly, de ConnectedAppSettings, está ligado.", default=FALSE,
               notas=["A página diz que o campo está descontinuado a partir da API 52.0."]),
             P("enableWebruntimeBYOTemplate", "boolean", "48.0", "Indicava se o template Build Your Own (LWC) aparecia no Experience Builder.",
               default=FALSE, ate="50.0", notas=["Removido na API 51.0."]),
         ], [("enableEnhancedSitesAndContentPlatform", "true"), ("enableTopicsInSites", "false")])

# ---------------------------------------------------------------- UserInterfaceSettings
settings("UserInterfaceSettings", None,
         "Configurações que mudam o comportamento da interface do usuário da org.",
         "Recuperar e implantar opções de interface, como edição inline, seções recolhíveis e ordenação de listas por várias colunas.", "46.0", [
             P("dynamicMruActionsOff", "boolean", "52.0", "Segundo a página, com true os usuários podem criar ações personalizadas nas listas de "
               "itens vistos recentemente.", default=TRUE, notas=[SO_LEX, "O nome do campo sugere o contrário (ações dinâmicas desligadas); o catálogo segue a descrição da página."]),
             P("enableAsyncRelatedLists", "boolean", "47.0", "Carrega as listas relacionadas de forma assíncrona.", default=FALSE, notas=[SO_CLASSIC]),
             P("enableClickjackUserPageHeaderless", "boolean", None, "Protege contra clickjacking as páginas Visualforce que escondem o cabeçalho "
               "padrão.", default=TRUE),
             P("enableCollapsibleSections", "boolean", None, "Permite recolher e expandir seções nos detalhes do registro pela seta ao lado do "
               "título.", default=TRUE),
             P("enableCollapsibleSidebar", "boolean", None, "Permite mostrar ou esconder a barra lateral nas páginas que a têm.", default=FALSE,
               notas=[SO_CLASSIC]),
             P("enableCustomObjectTruncate", "boolean", "47.0", "Permite que quem tem Customize Application trunque objetos customizados: apaga os "
               "registros e mantém o objeto e seus metadados.", default=FALSE),
             P("enableCustomeSideBarOnAllPages", "boolean", None, "Mostra os componentes personalizados da barra lateral em todas as páginas para "
               "todos os usuários.", default=FALSE, notas=[SO_CLASSIC, "O nome tem um erro de grafia (\"Custome\") no original; preservado."]),
             P("enableDeleteFieldHistory", "boolean", "47.0", "Permite excluir registros de histórico de campo e de arquivo de histórico de campo.",
               default=FALSE),
             P("enableExternalObjectAsyncRelatedLists", "boolean", "48.0", "Carrega de forma assíncrona as listas relacionadas de objetos externos.",
               default=TRUE, notas=[SO_CLASSIC]),
             P("enableHoverDetails", "boolean", None, "Mostra uma janela sobreposta com detalhes do registro ao passar o mouse; o usuário precisa "
               "de acesso aos campos do mini page layout.", default=TRUE),
             P("enableInlineEdit", "boolean", None, "Permite editar valores de campos direto na página de detalhes do registro.", default=TRUE),
             P("enablePersonalCanvas", "boolean", None, "Permite instalar e usar apps canvas pessoais.", default=TRUE),
             P("enableRelatedListHovers", "boolean", "50.0", "Mostra links de sobreposição das listas relacionadas no topo dos detalhes de "
               "registros e de objetos customizados no Setup.", default=TRUE),
             P("enableSldsV2DarkModeInCosmos", "boolean", "65.0", "Permite ligar o modo escuro no tema Salesforce Cosmos (temas SLDS 2, em "
               "edições selecionadas).", default=FALSE),
             P("enableQuickCreate", "boolean", None, "Mostra a área de criação rápida nas páginas iniciais das abas, para criar registros com "
               "poucas informações; por padrão aparece em leads, contas, contatos e oportunidades."),
             P("listViewIleBypassLayout", "boolean", "68.0", "Permite editar inline em listas qualquer campo editável, sem as restrições do "
               "layout.", default=FALSE, notas=[SO_LEX]),
             P("listViewIleMultiRecordType", "boolean", "68.0", "Permite editar inline em listas com registros de mais de um record type.",
               default=FALSE, notas=["Só no Lightning Experience e em listas LWC, segundo a página."]),
             P("multiColumnSortLv", "boolean", "63.0", "Permite ordenar list views por várias colunas.", default=TRUE),
             P("multiColumnSortRL", "boolean", "63.0", "Permite ordenar listas relacionadas por várias colunas.", default=TRUE),
         ], [("enableInlineEdit", "true"), ("multiColumnSortLv", "true")],
         extra_nota=" A leitura não deu o nome-base do arquivo.")

# ---------------------------------------------------------------- UserEngagementSettings
ATE64 = dict(ate="64.0", notas=["A página indica o campo para a API 64.0 e anteriores."])
IBIL = ["A página diz que o campo está obsoleto na API 51.0 e posteriores."]
settings("UserEngagementSettings", None,
         "Configurações ligadas à transição e à adoção do Lightning Experience, ao menu de Ajuda e às orientações in-app.",
         "Recuperar e implantar o que os usuários veem no menu de Ajuda, as orientações in-app e as opções da troca do Classic para o Lightning.",
         "47.0", [
             P("canUseAdoptionApps", "boolean", "62.0", "Dá acesso às ferramentas de transição (Optimizer, Transition Assistant e Readiness Report). "
               "Só tem efeito em orgs com a página External Application Settings.", default=FALSE),
             P("doesScheduledSwitcherRunDaily", "boolean", None, "Faz a troca automática do Classic para o Lightning rodar todo dia (true) ou toda "
               "semana (false).", default=FALSE),
             P("enableCustomHelpGlobalSection", "boolean", None, "Indica se o menu de Ajuda do Lightning tem uma seção personalizada.", default=FALSE),
             P("enableHelpMenuShowFeedback", "boolean", None, "Mostra no menu de Ajuda o link de feedback para a Salesforce (administradores sempre "
               "o veem).", default=TRUE),
             P("enableHelpMenuShowHelp", "boolean", None, "Mostra a seção Help For This Page no menu de Ajuda.", default=TRUE, **ATE64),
             P("enableHelpMenuShowNewUser", "boolean", None, "Mostra a seção Getting Started no menu de Ajuda.", default=TRUE, **ATE64),
             P("enableHelpMenuShowSearch", "boolean", None, "Mostra no menu de Ajuda o link de busca na documentação.", default=TRUE, **ATE64),
             P("enableHelpMenuShowSfdcContent", "boolean", None, "Mostra no menu de Ajuda os recursos de ajuda criados pela Salesforce.", default=TRUE),
             P("enableHelpMenuShowShortcut", "boolean", None, "Mostra no menu de Ajuda o link de atalhos de teclado.", default=TRUE),
             P("enableHelpMenuShowSupport", "boolean", None, "Mostra no menu de Ajuda o link para a Ajuda do Salesforce.", default=TRUE),
             P("enableHelpMenuShowTrailhead", "boolean", None, "Mostra no menu de Ajuda o link para o Trailhead.", default=TRUE),
             P("enableIBILOptOutDashboards", "boolean", None, "Esconde o aviso \"It's Better in Lightning\" sobre dashboards.", default=TRUE, notas=IBIL),
             P("enableIBILOptOutEvents", "boolean", None, "Esconde o aviso \"It's Better in Lightning\" sobre eventos e calendário.", default=TRUE,
               notas=IBIL),
             P("enableIBILOptOutReports", "boolean", None, "Esconde o aviso \"It's Better in Lightning\" sobre relatórios.", default=TRUE, notas=IBIL),
             P("enableIBILOptOutTasks", "boolean", None, "Esconde o aviso \"It's Better in Lightning\" sobre tarefas.", default=TRUE, notas=IBIL),
             P("enableLexToClassicFeedbackEnable", "boolean", None, "Mostra o formulário de feedback ao trocar para o Salesforce Classic.",
               default=FALSE),
             P("enableOrchestrationInSandbox", "boolean", None, "Mostra a assistência de adoção e as orientações in-app também em sandboxes.",
               default=FALSE),
             P("enableOrgUserAssistEnabled", "boolean", None, "Mostra todas as orientações in-app personalizadas da org (não muda o status ativo de "
               "cada uma).", default=TRUE),
             P("enableScheduledSwitcher", "boolean", None, "Liga a troca automática do Classic para o Lightning.", default=TRUE),
             P("enableSfdcProductFeedbackSurvey", "boolean", None, "Mostra o formulário de feedback sobre produtos Salesforce.", default=TRUE),
             P("enableShowSalesforceUserAssist", "boolean", None, "Mostra as orientações in-app padrão criadas pela Salesforce (não muda o status "
               "ativo de cada uma).", default=TRUE),
             P("isCrucNotificationDisabled", "boolean", None, "Esconde dos administradores as notificações sobre a atualização crítica Turn on "
               "Lightning Experience (Winter '20).", default=FALSE),
             P("isLEXWelcomeMatDisabled", "boolean", None, "Esconde a tela de boas-vindas do Lightning no primeiro login.", default=FALSE),
             P("isMeetTheAssistantDisabledInClassic", "boolean", None, "Esconde dos administradores, no Classic, as notificações do Transition "
               "Assistant.", default=FALSE),
             P("isMeetTheAssistantDisabledInLightning", "boolean", None, "Esconde dos administradores, no Lightning, as notificações do Transition "
               "Assistant.", default=FALSE),
             P("optimizerAppEnabled", "boolean", None, "Liga o Salesforce Optimizer na org.", default=FALSE),
             P("suggestedForYou", "boolean", None, "Liga o recurso Suggested For You na org.", default=TRUE),
         ], [("enableHelpMenuShowTrailhead", "true"), ("enableScheduledSwitcher", "false")],
         alertas=["Permissões e edições dependem de cada recurso; a página manda consultar a Ajuda."],
         extra_nota=" A leitura não deu o nome-base do arquivo.",
         divergencias=["A seção Version da página (src:mdapi-userengagementsettings) fala em \"Prompt components\", aparentemente um erro de cópia; "
                       "o catálogo registra 47.0 como versão do tipo."])

emit_structs()

# ---------------------------------------------------------------- Classificação funcional
for fid, n, papel in [
    ("salesforce-files", "FileUploadAndDownloadSecuritySettings", "Regras de download e execução por tipo de arquivo."),
    ("sso-saml", "IdentityProviderSettings", "Liga a Salesforce como provedor de identidade SAML e define o certificado."),
    ("experience-cloud-sites", "SiteSettings", "Opções gerais dos sites, como a plataforma aprimorada de sites e conteúdo."),
]:
    C.ampliar_funcionalidade(fid, mdts=[(n, papel)], srcs=[S(n)])

SEM_OBJ = [{"tipo": "objeto_api", "estado": "desconhecido",
            "motivo": "Objetos API ligados a esta funcionalidade não foram investigados neste lote; a lista vazia não comprova inexistência."}]
SETUP_DESC = af("desconhecido", None, "Caminho no Setup não validado nesta sessão.")
C.funcionalidade(
    "atividades-e-calendario", "Atividades e calendário", "Activities", ["tarefas", "eventos", "calendário"],
    "Tarefas e eventos ligados a registros, com lembretes, recorrência e calendário.",
    "Registrar e planejar o trabalho com clientes: ligações, reuniões e pendências.",
    "Uma vendedora cria uma tarefa recorrente para ligar todo mês para o cliente e vê a reunião da semana no calendário.",
    ("conteudo-conhecimento-e-colaboracao", "colaboracao"),
    [("processos-de-negocio-especificos-de-produto", "vendas", "Atividades são muito usadas no processo de vendas; a página do tipo não restringe a uma nuvem.")],
    [("ActivitiesSettings", "Opções de tarefas, eventos, lembretes e calendário.")], [], [S("ActivitiesSettings")], SEM_OBJ, SETUP_DESC,
    limitacoes=["Os objetos Task e Event não foram conferidos neste lote."])
C.funcionalidade(
    "picklists-de-estado-e-pais", "Picklists de estado e país", "State and Country/Territory Picklists", ["picklists de endereço"],
    "Listas padronizadas de países, territórios e estados nos campos de endereço, no lugar do texto livre.",
    "Evitar variações de escrita nos endereços e manter relatórios e integrações consistentes.",
    "Em vez de \"SP\", \"S. Paulo\" e \"São Paulo\", todos os registros passam a usar o mesmo valor da picklist.",
    ("dados-e-modelagem", "listas-de-valores"), [],
    [("AddressSettings", "Países, territórios e estados das picklists.")], [], [S("AddressSettings")], SEM_OBJ, SETUP_DESC,
    alertas=["Depois de ativar as picklists, os valores não podem voltar a inativos; pela Metadata API não dá para excluir países ou estados."])
C.funcionalidade(
    "entrega-de-email", "Entrega e administração de e-mail", "Email Administration", ["deliverability", "e-mail da org"],
    "Regras de envio e recebimento de e-mail da org: autenticação (SPF, Sender ID), devoluções, cópia de conformidade, envio por Gmail ou "
    "Office 365 e domínios não verificados.",
    "Garantir que os e-mails da org cheguem, sigam as regras de segurança e fiquem registrados.",
    "A administradora liga o tratamento de devoluções para descobrir quais contatos têm e-mail inválido.",
    ("conteudo-conhecimento-e-colaboracao", "templates-e-comunicacao"), [],
    [("EmailAdministrationSettings", "Entrega, conformidade e relay de e-mail."),
     ("EmailAuthorizationSettings", "Tratamento de e-mails de domínios não verificados.")], [],
    [S("EmailAdministrationSettings"), S("EmailAuthorizationSettings")], SEM_OBJ, SETUP_DESC)
C.funcionalidade(
    "pesquisa", "Pesquisa", "Search", ["busca", "busca global", "Einstein Search"],
    "A busca da org: busca global, barra lateral, lookups e Einstein Search.",
    "Ajustar como os usuários encontram registros e itens de configuração.",
    "A org liga a correção ortográfica na busca de Knowledge e define quantos resultados aparecem por página no lookup de contas.",
    ("interface-e-experiencia-do-usuario", "aplicativos-e-navegacao"), [],
    [("SearchSettings", "Opções de busca global, barra lateral, lookups e Einstein Search.")], [], [S("SearchSettings")], SEM_OBJ, SETUP_DESC)
C.funcionalidade(
    "opcoes-da-interface", "Opções da interface do usuário", "User Interface Settings", ["edição inline", "user interface"],
    "Opções gerais da interface: edição inline, seções recolhíveis, detalhes ao passar o mouse, ordenação de listas e modo escuro.",
    "Ajustar a experiência de uso da org para todos os usuários.",
    "A org liga a ordenação por várias colunas nas list views e a edição inline em listas com mais de um record type.",
    ("interface-e-experiencia-do-usuario", "acessibilidade-e-personalizacao"), [],
    [("UserInterfaceSettings", "Opções gerais de comportamento da interface.")], [], [S("UserInterfaceSettings")], SEM_OBJ, SETUP_DESC)

C.funcionalidade(
    "menu-de-ajuda-e-adocao", "Menu de Ajuda e adoção do Lightning", "User Engagement", ["orientações in-app", "Lightning Experience transition"],
    "O que aparece no menu de Ajuda, as orientações in-app e as ferramentas e avisos da troca do Salesforce Classic para o Lightning Experience.",
    "Apoiar os usuários na adoção do Lightning e controlar os atalhos de ajuda que eles veem.",
    "A org esconde o link para o Trailhead no menu de Ajuda e liga as orientações in-app também nas sandboxes.",
    ("interface-e-experiencia-do-usuario", "aplicativos-e-navegacao"), [],
    [("UserEngagementSettings", "Itens do menu de Ajuda, orientações in-app e opções da troca para o Lightning.")], [],
    [S("UserEngagementSettings")], SEM_OBJ, SETUP_DESC)

print("lote 9b: 10 Settings cadastrados")
