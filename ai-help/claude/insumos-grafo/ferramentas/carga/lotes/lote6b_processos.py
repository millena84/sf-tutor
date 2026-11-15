"""Lote 6b (issue #34, item 3): metadata types e funcionalidades do tema Processos de negócio específicos de produto.

- Cadastra LeadConfigSettings, ProductSettings, OrderSettings, ContractSettings, FieldServiceSettings e CommunitiesSettings
  (mais a estrutura ObjectMappingItem).
- Cria as funcionalidades Pedidos, Contratos, Field Service e Digital Experiences; amplia Leads e Produtos e catálogos de preço.
- Troca o texto genérico "Configurações de X da org." de 9 tipos Settings de vendas e atendimento por uma descrição do que
  cada tipo guarda (redação do projeto a partir das propriedades já catalogadas; nenhum fato novo).
CaseSettings e RevenueManagementSettings NÃO entram (ver fontes/extracoes/mdapi-lote6b-processos.txt).

Cita fontes de Ajuda registradas por conteudo_temas.py: rode este script e, em seguida, conteudo_temas.py e temas_internos.py.
Reexecutável. Uso: python3 ferramentas/carga/lotes/lote6b_processos.py
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M              # noqa: E402
from carga.mdt import P                 # noqa: E402
from carga.base import af, ev, ld, sv   # noqa: E402
from carga import catalogo as C         # noqa: E402

DATA = "2026-11-14"
EXTR = "fontes/extracoes/mdapi-lote6b-processos.txt"
BASE_URL = "https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-"
VERSAO = "sem versão na URL (referência atual)"


def _f(nome, pertinencia):
    return C.fonte("src:mdapi-" + nome.lower(), f"{nome} (Metadata API)", BASE_URL + nome.lower() + ".html", pertinencia, EXTR, DATA, versao=VERSAO)


C.registrar_fontes([_f(n, f"Arquivo, versão e propriedades do tipo {n}.") for n in
                    ("LeadConfigSettings", "ProductSettings", "OrderSettings", "ContractSettings", "FieldServiceSettings", "CommunitiesSettings")]
                   + [_f("CaseSettings", "O que o tipo CaseSettings cobre (tipo ainda não cadastrado: a leitura não devolveu os nomes dos elementos).")])

S_LEAD, S_PROD, S_ORDER = "src:mdapi-leadconfigsettings", "src:mdapi-productsettings", "src:mdapi-ordersettings"
S_CONTRACT, S_FS, S_COMM = "src:mdapi-contractsettings", "src:mdapi-fieldservicesettings", "src:mdapi-communitiessettings"

FALSE = ("false", False, "A página declara default false.")
TRUE = ("valor", "true", None)
SETTINGS_PKG = "No package.xml, use o tipo Settings com o nome-base do arquivo como membro; o curinga só vale para recuperar todas as configurações."
FULLNAME = M.FULLNAME_HERDADO(None)
NOTA_COB = "Universo esperado = tabela Fields da página oficial lida em 2026-11-14 (mais fullName herdado)."
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'

# ---------------------------------------------------------------- estrutura
M.struct("ObjectMappingItem", S_FS, ["mdt:FieldServiceSettings"], [
    P("mappingType", "MappingType", None, "Tipo do mapeamento de objetos.", "S", vals=[
        ("WorkPlans_WorkPlanTemplate_WorkPlan", None), ("WorkPlans_WorkStepTemplate_WorkStep", None), ("WorkPlans_WorkPlanTemplateEntry_WorkStep", None)]),
    P("objectMapping", "ObjectMapping", None,
      "Detalhes do mapeamento: objeto de origem, objeto de destino e pares de campos. Nesta página, a origem é WorkPlanTemplate, WorkStepTemplate "
      "ou WorkPlanTemplateEntry, e o destino é WorkPlan ou WorkStep.", "S", estrutura="ObjectMapping"),
], "Um mapeamento de campos customizados usado na geração de work plans e work steps, em FieldServiceSettings.objectMappingItem.")

# ---------------------------------------------------------------- metadata types
M.mdt("LeadConfigSettings", S_LEAD,
      "Configurações de leads para a org inteira: como o lead é convertido, o que a janela de conversão mostra e que ações ficam disponíveis.",
      "Recuperar e implantar as opções da tela Lead Settings, como validação na conversão e preservação do status.", "47.0", [
          P("doesEnableLeadConvertDefaultSubjectBlankTaskCreation", "boolean", None,
            "Com true, a conversão cria tarefas mesmo quando o assunto padrão está em branco; com false, só tarefas com assunto."),
          P("doesHideOpportunityInConvertLeadWindow", "boolean", None, "Esconde a seção de oportunidade da janela Convert Lead.", default=FALSE),
          P("doesPreserveLeadStatus", "boolean", None,
            "Mantém o status do lead na conversão, em vez de adotar o padrão do record type do novo dono.", default=TRUE),
          P("doesSelectNoOpportunityOnConvertLead", "boolean", None, "Impede que uma oportunidade seja criada quando o lead é convertido.", default=FALSE),
          P("doesTrackHistory", "boolean", None, "Liga o histórico de campos de leads, com escolha dos campos acompanhados.", default=FALSE),
          P("enableConversionsOnMobile", "boolean", None, "Permite converter leads em dispositivos móveis.", default=TRUE),
          P("enableOrgWideMergeAndDelete", "boolean", None,
            "Permite que usuários mesclem e excluam leads; eles também precisam do acesso Public Read/Write/Transfer.", default=FALSE),
          P("relateEmailsToContactOnConvert", "boolean", None, "Associa os e-mails do lead ao contato em que ele é convertido.", default=FALSE),
          P("shouldLeadConvertRequireValidation", "boolean", None, "Aplica as regras de validação durante a conversão de leads.", default=TRUE),
          P("shouldSendNotificationEmailWhenLeadOwnerUpdatesViaApexInLEX", "boolean", None,
            "Envia notificação por e-mail quando o Apex troca o dono do lead no Lightning Experience.", default=FALSE),
          FULLNAME,
      ], exemplo=CAB + f"""<LeadConfigSettings {NS}>
    <!-- Mantém o status do lead ao converter -->
    <doesPreserveLeadStatus>true</doesPreserveLeadStatus>
    <doesTrackHistory>false</doesTrackHistory>
    <!-- Regras de validação valem na conversão -->
    <shouldLeadConvertRequireValidation>true</shouldLeadConvertRequireValidation>
</LeadConfigSettings>""",
      arquivos_prontos=M.arquivos_settings("LeadConfigSettings", "LeadConfig", S_LEAD), alertas=["No package.xml, use o tipo Settings com o membro LeadConfig."],
      cobertura_nota=NOTA_COB + " O trecho lido não traz declaração sobre o curinga no package.xml.",
      setup=af("verificado", "Setup > Quick Find: Lead Settings > Lead Settings", "Tela das configurações de leads. " + C.UI_EN, [ev("src:help-lead-settings")]))

M.mdt("ProductSettings", S_PROD,
      "Preferências da org para produtos: quantity schedules, revenue schedules e o efeito de ativar ou desativar um produto sobre os preços dele.",
      "Recuperar e implantar a ativação de schedules de produto e a regra de ativação em cascata dos preços.", "28.0", [
          P("enableCascadeActivateToRelatedPrices", "boolean", None,
            "Quando o indicador ativo de um produto muda, atualiza também o indicador ativo dos preços relacionados."),
          P("enableMySettings", "boolean", "47.0",
            "Move as páginas de configurações pessoais para um painel My Settings separado. Afeta todos os usuários.", default=TRUE),
          P("enableQuantitySchedule", "boolean", None, "Liga os quantity schedules para produtos."),
          P("enableRevenueSchedule", "boolean", None, "Liga os revenue schedules para produtos."),
          FULLNAME,
      ], exemplo=CAB + f"""<ProductSettings {NS}>
    <enableCascadeActivateToRelatedPrices>true</enableCascadeActivateToRelatedPrices>
    <!-- Schedules: quando o produto é entregue (quantity) e quando é pago (revenue) -->
    <enableQuantitySchedule>true</enableQuantitySchedule>
    <enableRevenueSchedule>true</enableRevenueSchedule>
</ProductSettings>""",
      arquivos_prontos=M.arquivos_settings("ProductSettings", "Product", S_PROD), curinga=False, alertas=[SETTINGS_PKG], cobertura_nota=NOTA_COB)

M.mdt("OrderSettings", S_ORDER,
      "Configurações de pedidos (orders) da org: se pedidos estão ligados e que variações são aceitas.",
      "Recuperar e implantar a ativação de pedidos, reduction orders, quantidades zero ou negativas e pedidos sem price book.", "30.0", [
          P("enableEnhancedCommerceOrders", "boolean", "48.0",
            "Indica se enhanced commerce orders estão ligados. Só fica disponível com a licença Salesforce Order Management.", default=FALSE),
          P("enableNegativeQuantity", "boolean", None, "Indica se dá para incluir order products com quantidade negativa. Exige enableOrders em true."),
          P("enableOptionalPricebook", "boolean", None, "Indica se dá para criar pedidos sem price book."),
          P("enableOrderEvents", "boolean", None, "Indica se os eventos de pedido estão ligados (a página remete a OrderStatusChangedEvent, no guia de Platform Events)."),
          P("enableOrders", "boolean", None, "Indica se pedidos estão ligados na org.", "S"),
          P("enableOrderWithMultiplePriceBooks", "boolean", "60.0",
            "Indica se um pedido pode ter itens de mais de um price book. Exige enableOrders e enableEnhancedCommerceOrders em true."),
          P("enableReductionOrders", "boolean", None, "Indica se reduction orders estão ligados. Exige enableOrders em true."),
          P("enableZeroQuantity", "boolean", "42.0", "Indica se dá para incluir order products com quantidade zero. Exige enableOrders em true.", default=FALSE),
          FULLNAME,
      ], exemplo=CAB + f"""<OrderSettings {NS}>
    <!-- Obrigatório: liga pedidos na org -->
    <enableOrders>true</enableOrders>
    <!-- As opções abaixo exigem enableOrders em true -->
    <enableReductionOrders>true</enableReductionOrders>
    <enableZeroQuantity>false</enableZeroQuantity>
</OrderSettings>""",
      arquivos_prontos=M.arquivos_settings("OrderSettings", "Order", S_ORDER), curinga=False, alertas=[SETTINGS_PKG], cobertura_nota=NOTA_COB,
      setup=af("verificado", "Setup > Quick Find: Order Settings > Order Settings", "Tela das configurações de pedidos. " + C.UI_EN, [ev("src:help-orders-enable")]))

M.mdt("ContractSettings", S_CONTRACT,
      "Configurações de contratos da org, como o cálculo automático da data final e o aviso de expiração.",
      "Recuperar e implantar as opções da tela Contract Settings.", "27.0", [
          P("autoCalculateEndDate", "boolean", None, "Indica se a data final do contrato é calculada automaticamente."),
          P("autoExpirationDelay", "string", None, None),
          P("autoExpirationRecipient", "string", None, None),
          P("autoExpireContracts", "boolean", None, None),
          P("enableContractHistoryTracking", "boolean", None, None),
          P("notifyOwnersOnContractExpiration", "boolean", None, "Indica se os donos da conta e do contrato recebem e-mail quando o contrato expira."),
          FULLNAME,
      ], exemplo=CAB + f"""<ContractSettings {NS}>
    <!-- Data final calculada a partir da data de início e do prazo do contrato -->
    <autoCalculateEndDate>true</autoCalculateEndDate>
    <notifyOwnersOnContractExpiration>true</notifyOwnersOnContractExpiration>
</ContractSettings>""",
      arquivos_prontos=M.arquivos_settings("ContractSettings", "Contract", S_CONTRACT), curinga=False, alertas=[SETTINGS_PKG], cobertura_nota=NOTA_COB,
      setup=af("verificado", "Setup > Quick Find: Contract Settings > Contract Settings", "Tela das configurações de contratos. " + C.UI_EN, [ev("src:help-contracts-setup")]))

STATUS = lambda quando: f"Status padrão da service appointment quando ela {quando}."
M.mdt("FieldServiceSettings", S_FS,
      "Configurações de Field Service da org: ativação do recurso e das work orders, status padrão das visitas, compartilhamento com os técnicos, "
      "app móvel e notificações ao cliente.",
      "Recuperar e implantar a ativação e as preferências de Field Service em vez de marcá-las à mão em cada ambiente.", "40.0", [
          P("advancedDataSyncOrgPreference", "boolean", None, None),
          P("apptAssistantExpiration", "int", "50.0",
            "Tempo depois do qual o cliente deixa de ver a localização e a previsão de chegada do técnico pela URL de rastreamento."),
          P("apptAssistantInfoUrl", "string", "50.0", "URL de rastreamento que mostra ao cliente a previsão de chegada do técnico."),
          P("apptAssistantRadiusUnitValue", "ApptAssistantRadiusUnit", "50.0", "Unidade do raio da geofence.",
            vals=[("Kilometer", None), ("Meter", None), ("Mile", None), ("Yard", None)]),
          P("apptAssistantRadiusValue", "int", "50.0", "Raio da geofence em torno do endereço da visita que dispara a notificação ao cliente."),
          P("apptAssistantStatus", "string", "50.0", "Status da visita que dispara a notificação En Route. Precisa corresponder a uma opção de Status."),
          P("canceledDefaultStatus", "string", "65.0", STATUS("é cancelada")),
          P("cannotCompleteDefaultStatus", "string", "65.0", STATUS("não pode ser concluída")),
          P("canPopulateGoogleAddress", "boolean", "57.0", "Permite que desktop e app móvel enviem dados de geolocalização e de mapa a Google e Apple."),
          P("canSendAppCenterCrashReports", "boolean", "57.0", "Permite que a Salesforce envie relatórios de falha ao Microsoft App Center."),
          P("canStoreMobileAnalytics", "boolean", "57.0", "Permite que terceiros guardem dados de analytics do app móvel."),
          P("completedDefaultStatus", "string", "65.0", STATUS("é concluída")),
          P("deepLinkPublicSecurityKey", "string", "54.0", "Chave pública de segurança para ações de deep link no app móvel Field Service."),
          P("dispatchedDefaultStatus", "string", "65.0", STATUS("é despachada")),
          P("doesAllowEditSaForCrew", "boolean", None, "Permite que membros de equipe (crew) editem as próprias service appointments. Só vale com doesShareSaWithAr ligado."),
          P("doesAvlCalcInclOvertime", "boolean", None, None),
          P("doesAvlCalcInclPrimOnly", "boolean", None, None),
          P("doesShareSaParentWoWithAr", "boolean", None,
            "Compartilha a work order pai com os recursos atribuídos. Depende de doesShareSaWithAr e do compartilhamento de work orders."),
          P("doesShareSaWithAr", "boolean", None,
            "Compartilha as service appointments despachadas com os recursos atribuídos. Depende do acesso de compartilhamento das appointments."),
          P("enableAdvancedDataSync", "boolean", None, None),
          P("enableBatchWindow", "boolean", None, None),
          P("enableDataCaptureControlByParent", "boolean", None, None),
          P("enableDocumentBuilder", "boolean", None, "Libera o acesso ao recurso Document Builder."),
          P("enableFieldServiceNotifications", "boolean", None, None),
          P("enableFloatingWorkOrder", "boolean", None, "Liga floating work orders, cuja recorrência parte da conclusão da work order anterior."),
          P("enableGeolocationBasedActionControlByParent", "boolean", None, None),
          P("enableLsdkMode", "boolean", None, "Liga o Lightning SDK no app móvel Field Service."),
          P("enablePopulateWorkOrderAddress", "boolean", None, "Preenche o endereço das work orders geradas a partir de um maintenance plan."),
          P("enableServiceAppointmentLifecycle", "boolean", None, None),
          P("enableStandbyMode", "boolean", None, "Liga o modo standby do app móvel, que pausa notificações e sincronizações para poupar bateria."),
          P("enableWorkOrders", "boolean", None,
            "Liga o objeto Work Order, com ou sem Field Service. Não pode ser desligado enquanto Field Service está ligado."),
          P("enableWorkPlansAutoGeneration", "boolean", "52.0", "Gera work plans e work steps automaticamente na criação, com base em regras de seleção."),
          P("enableWorkStepManualStatusUpdate", "boolean", None, "Permite atualizar à mão o status de work steps."),
          P("enableWorkStepsHideNotApplicable", "boolean", None, None),
          P("enrouteStatus", "string", None, None),
          P("fieldServiceNotificationsOrgPref", "boolean", None,
            "Liga as notificações no app para mudanças em work orders, no app móvel Salesforce e no Lightning Experience."),
          P("fieldServiceOrgPref", "boolean", None, "Indica se Field Service está ligado."),
          P("inProgressDefaultStatus", "string", "65.0", STATUS("está em andamento")),
          P("isGeoCodeSyncEnabled", "boolean", None, "Sincroniza a localização de um Service Resource com um objeto de inventário."),
          P("isLocationHistoryEnabled", "boolean", None, "Guarda o histórico de localização de um Service Resource."),
          P("mobileFeedbackEmails", "string", "54.0", "Endereço de e-mail que recebe o feedback enviado pelo app móvel Field Service."),
          P("noneDefaultStatus", "string", "65.0", STATUS("não tem status específico")),
          P("o2EngineEnabled", "boolean", "55.0", "Liga o Field Service Enhanced Scheduling and Optimization.", default=FALSE),
          P("objectMappingItem", "ObjectMappingItem[]", "52.0", "Mapeamentos de campos customizados usados na geração de work plans e work steps.",
            estrutura="ObjectMappingItem"),
          P("optimizationServiceAccess", "boolean", None, "Permite que o serviço de otimização acesse dados da org."),
          P("overrideDefaultLwcStyling", "boolean", None, "Permite que o app móvel aplique estilo próprio ou de marca aos Lightning Web Components."),
          P("scheduledDefaultStatus", "string", "65.0", STATUS("é agendada")),
          P("serviceAppointmentsDueDateOffsetOrgValue", "int", None,
            "Quantidade de dias depois da Created Date em que cai a Due Date das appointments criadas automaticamente."),
          P("useBundler", "boolean", None, None),
          P("useLicenselessPermset", "boolean", None, None),
          P("useWorkCapacity", "boolean", None, None),
          P("workOrderDurationSource", "WorkOrderDurationSource", "55.0", "Origem da duração da work order.",
            vals=[("WorkType", None), ("TotalFromWorkPlan", None), ("Custom", None)]),
          P("workOrderLineItemSearchFields", "string[]", None, "Campos de work order line item que a busca examina para sugerir artigos de knowledge."),
          P("workOrderSearchFields", "string[]", None, "Campos de work order que a busca examina para sugerir artigos de knowledge."),
          FULLNAME,
      ], exemplo=CAB + f"""<FieldServiceSettings {NS}>
    <!-- Liga o Field Service e as work orders -->
    <fieldServiceOrgPref>true</fieldServiceOrgPref>
    <enableWorkOrders>true</enableWorkOrders>
    <!-- Compartilha as visitas despachadas com os técnicos atribuídos -->
    <doesShareSaWithAr>true</doesShareSaWithAr>
    <!-- Valores documentados: WorkType, TotalFromWorkPlan, Custom -->
    <workOrderDurationSource>WorkType</workOrderDurationSource>
</FieldServiceSettings>""",
      arquivos_prontos=M.arquivos_settings("FieldServiceSettings", None, S_FS), curinga=False,
      alertas=["A página informa só a pasta settings e a extensão .settings; o nome-base do arquivo não foi confirmado.",
               "enableWorkOrders não pode ser desligado enquanto Field Service está ligado."],
      cobertura_nota=NOTA_COB,
      setup=af("verificado", "Setup > Quick Find: Field Service Settings > Field Service Settings", "Tela que liga o Field Service. " + C.UI_EN,
               [ev("src:help-field-service-enable")]))

M.mdt("CommunitiesSettings", S_COMM,
      "Configurações de sites Experience Cloud (antes communities) da org: ativação de digital experiences e workspaces, moderação, usuário "
      "convidado (guest) e parceiros.",
      "Recuperar e implantar as opções gerais que valem para todos os sites da org.", "47.0", [
          P("applyLoginPageTypeToEmbeddedLogin", "boolean", "49.0", "Aplica o tipo de página de login do site a todas as implementações de Embedded Login.",
            default=("valor", "true", "true em orgs novas; false em orgs anteriores ao Summer '20.")),
          P("blockEmbeddedLoginUnknownURLRedirect", "boolean", "52.0", "Bloqueia redirecionamentos a URLs desconhecidas no parâmetro state do OAuth.",
            default=("valor", "true", "true em orgs novas; false em orgs anteriores ao Summer '21.")),
          P("canModerateAllFeedPosts", "boolean", None, "Permite moderação (flags e regras) em todos os posts de feed, inclusive os visíveis no site.", default=FALSE),
          P("canModerateInternalFeedPosts", "boolean", None, "Permite moderação em posts de feed de registro criados por usuários internos.", default=FALSE),
          P("embeddedVisualforcePages", "boolean", "48.0", "Permite links para páginas Visualforce a partir de outras páginas Visualforce, pela API.", default=FALSE),
          P("enableCommunityWorkspaces", "boolean", "48.0", "Permite que administradores liguem o Experience Workspaces."),
          P("enableCspContactVisibilityPref", "boolean", "48.0",
            "Deixa usuários verem contatos de contas privadas a que têm leitura, quando o registro pai controla o contato."),
          P("enableCspNotesOnAccConPref", "boolean", "48.0", "Deixa usuários clientes acessarem notas e anexos de contas e contatos."),
          P("enableEnablePRM", "boolean", "48.0", "Permite que administradores habilitem usuários parceiros."),
          P("enableExternalAccHierPref", "boolean", "48.0", "Liga o objeto External Account Hierarchy."),
          P("enableGuestPermDisOptOutCruc", "boolean", None, None),
          P("enableGuestRecordReassignOrgPref", "boolean", "48.0", "Permite definir um dono padrão para os registros criados por guest users.", ate="63.0",
            notas=["Descontinuado na API 63.0; disponível da 48.0 à 63.0."]),
          P("enableGuestSecurityOptOutCruc", "boolean", None, None),
          P("enableGuvSecurityOptOutPref", "boolean", "49.0", "Permite desligar a visibilidade de guest user."),
          P("enableInviteChatterGuestEnabled", "boolean", "48.0", "Permite convidar guest users para usar o Chatter."),
          P("enableNameFieldsUserPIIEnabled", "boolean", None, None),
          P("enableNetPortalUserReportOpts", "boolean", "48.0", "Permite que usuários externos com a permissão rodem relatórios nos sites."),
          P("enableNetworksEnabled", "boolean", "47.0", "Permite ligar digital experiences."),
          P("enableOotbProfExtUserOpsEnable", "boolean", "48.0", "Permite usar perfis externos padrão no autocadastro e na criação de usuários."),
          P("enablePowerCustomerCaseStatus", "boolean", "48.0", "Permite que usuários com licença Customer Community Plus mudem o status de casos."),
          P("enablePreventBadgeGuestAccess", "boolean", "53.0", "Esconde badges dos guest users em sites Experience Builder."),
          P("enablePRMAccRelPref", "boolean", "48.0", "Liga o objeto Account Relationship e as opções de data sharing rule relacionadas."),
          P("enableRelaxPartnerAccountFieldPref", "boolean", "48.0", "Permite editar campos de conta parceira em oportunidades e leads."),
          P("enableUnsupportedBrowserModalPref", "boolean", "48.0", "Mostra avisos de navegador não suportado nos sites Experience Cloud."),
          P("enableUsernameUniqForOrgPref", "boolean", "48.0", "Define a unicidade de username no nível da org."),
          FULLNAME,
      ], exemplo=CAB + f"""<CommunitiesSettings {NS}>
    <!-- Atenção: digital experiences não podem ser desligadas depois de ligadas -->
    <enableNetworksEnabled>true</enableNetworksEnabled>
    <enableCommunityWorkspaces>true</enableCommunityWorkspaces>
    <enableEnablePRM>false</enableEnablePRM>
</CommunitiesSettings>""",
      arquivos_prontos=M.arquivos_settings("CommunitiesSettings", "Communities", S_COMM), curinga=False,
      alertas=[SETTINGS_PKG, "Segundo a Ajuda, digital experiences não podem ser desligadas depois de ligadas."], cobertura_nota=NOTA_COB,
      setup=af("verificado", "Setup > Quick Find: Digital Experiences > Digital Experiences > Settings", "Tela de ativação e opções gerais dos sites. " + C.UI_EN,
               [ev("src:help-digital-experiences-enable")]))

M.emit_structs()

# ObjectMapping já existia (LeadConvertSettings); passa a ser usada também por FieldServiceSettings, via ObjectMappingItem.
om = ld("estruturas/ObjectMapping.json")
om["usada_por"] = sorted(set(om["usada_por"]) | {"mdt:FieldServiceSettings"})
if not any(e["fonte"] == S_FS for e in om["evidencias"]):
    om["evidencias"].append(ev(S_FS, "Mesma estrutura, usada em FieldServiceSettings por ObjectMappingItem.objectMapping."))
sv("estruturas/ObjectMapping.json", om)

# ---------------------------------------------------------------- descrições genéricas de Settings já catalogados
# Redação do projeto a partir das propriedades já catalogadas de cada tipo (nenhum fato novo, nenhuma fonte nova).
O_QUE_E = {
    "AccountSettings": "Grupo de configurações de contas e contatos: equipes de conta, histórico de campos de conta e de contato, relação de um "
                       "contato com várias contas e o link de hierarquia.",
    "CampaignSettings": "Grupo de configurações de campanhas: influência de campanhas sobre oportunidades, contas como membros de campanha, "
                        "histórico de campos e atribuição por IA.",
    "EntitlementSettings": "Grupo de configurações de entitlements: ativação de entitlements e do versionamento, comportamento dos milestones e "
                           "filtros que limitam as buscas de entitlement e de asset em casos.",
    "ForecastingSettings": "Grupo de configurações de previsões colaborativas: ativação, tipos de previsão, mapeamento de categorias, ajustes, "
                           "intervalo de períodos, cotas e moeda de exibição.",
    "KnowledgeSettings": "Grupo de configurações do Salesforce Knowledge: ativação do Knowledge e do Lightning Knowledge, idiomas, uso em casos, "
                         "artigos sugeridos, resumos nos portais e votação.",
    "OmniChannelSettings": "Grupo de configurações do Omni-Channel: ativação, roteamento por skills, prioridade secundária de roteamento e "
                           "capacidade baseada em status.",
    "OpportunitySettings": "Grupo de configurações de oportunidades: equipes de oportunidade, Pipeline Inspection, lembretes de atualização, "
                           "histórico de campos, product schedules customizáveis e atalhos de criação.",
    "QuoteSettings": "Grupo de configurações de cotações: ativação de cotações e permissão de cotações sem oportunidade.",
    "Territory2Settings": "Grupo de configurações de Sales Territories: ativação, níveis de acesso padrão a contas, contatos, casos e "
                          "oportunidades, objetos suportados e filtro de atribuição de território a oportunidades.",
}
for nome, texto in O_QUE_E.items():
    d = ld(f"metadata-types/{nome}.json")
    d["o_que_e"] = texto
    sv(f"metadata-types/{nome}.json", d)

# ---------------------------------------------------------------- funcionalidades
PROD = "processos-de-negocio-especificos-de-produto"
SEM_OBJ = {"tipo": "objeto_api", "estado": "desconhecido",
           "motivo": "Objetos API do tema não investigados no lote 6b; a lista vazia não comprova inexistência."}


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


C.ampliar_funcionalidade("leads", mdts=[("LeadConfigSettings", "Opções de conversão, histórico e ações de leads implantáveis.")], srcs=[S_LEAD, "src:help-lead-settings"])
C.definir_setup("leads", "Setup > Quick Find: Lead Settings > Lead Settings", "Tela das configurações padrão de leads.", ["src:help-lead-settings"])
C.ampliar_funcionalidade("produtos-e-catalogos-de-preco", mdts=[("ProductSettings", "Schedules de produto e ativação em cascata dos preços, implantáveis.")],
                         srcs=[S_PROD, "src:help-product-schedules"], remover_ausencia_de="metadata_type")

C.funcionalidade(
    "pedidos", "Pedidos", "Orders", ["orders", "order", "reduction orders", "order products"],
    "Registro de um pedido de produtos ou serviços feito pelo cliente. O pedido pode estar ligado a um contrato.",
    "Acompanhar pedidos de clientes depois da venda, com seus produtos, status e eventuais reduções.",
    "Depois de fechar a oportunidade, o time registra um pedido com três produtos; mais tarde, uma devolução entra como reduction order.",
    (PROD, "receita-e-comercio"),
    [(PROD, "vendas", "A Ajuda documenta pedidos junto de contratos e produtos, no processo de vendas.")],
    [("OrderSettings", "Ativação de pedidos e de suas variações, implantável.")], [],
    ["src:help-orders-enable", "src:help-orders-manage", "src:help-orders-reduce", "src:help-orders-activation", S_ORDER], [SEM_OBJ],
    setup("Setup > Quick Find: Order Settings > Order Settings", "src:help-orders-enable"),
    limitacoes=["No Lightning Experience não dá para criar reduction orders; a Ajuda manda usar o Salesforce Classic.",
                "Só pedidos ativados podem ser reduzidos, e cada reduction order vale para um único pedido.",
                "Um pedido só pode ser ativado se tiver order products e, quando ligado a um contrato, se o contrato estiver ativo."])

C.funcionalidade(
    "contratos", "Contratos", "Contracts", ["contracts", "contract", "contract settings"],
    "Registro do acordo com o cliente, com data de início, prazo em meses e data final.",
    "Acompanhar a vigência dos acordos; pedidos podem ser ativados para contratos ativos.",
    "Um contrato de 12 meses começa em 1º de março; com o cálculo automático ligado, a data final sai da data de início e do prazo.",
    (PROD, "vendas"), [], [("ContractSettings", "Cálculo da data final e avisos de expiração implantáveis.")], [],
    ["src:help-contracts-setup", "src:help-contracts-things", "src:help-orders-activation", S_CONTRACT], [SEM_OBJ],
    setup("Setup > Quick Find: Contract Settings > Contract Settings", "src:help-contracts-setup"),
    pre=["Customize Application (para mudar as configurações de contratos)."])

C.funcionalidade(
    "field-service", "Field Service", "Field Service", ["serviço de campo", "agentforce field service and operations", "work orders", "fsl"],
    "Conjunto de recursos para o trabalho feito no local do cliente: work orders, agendamento de visitas e gestão da equipe móvel.",
    "Organizar o que precisa ser feito, quem vai, quando e onde.",
    "Um cliente pede conserto do ar-condicionado; nasce uma work order, que gera uma visita para quinta à tarde com o técnico da região.",
    (PROD, "servico-de-campo"), [], [("FieldServiceSettings", "Ativação e preferências de Field Service implantáveis.")], [],
    ["src:help-field-service-overview", "src:help-field-service-enable", "src:help-field-service-setup-basics", S_FS], [SEM_OBJ],
    setup("Setup > Quick Find: Field Service Settings > Field Service Settings", "src:help-field-service-enable"),
    pre=["Customize Application (para ligar o Field Service)."])

C.funcionalidade(
    "digital-experiences", "Digital Experiences (sites Experience Cloud)", "Digital Experiences",
    ["experience cloud", "communities", "sites", "portal", "enable digital experiences"],
    "A ativação e as opções gerais dos sites Experience Cloud da org: portais, centrais de ajuda e sites para clientes e parceiros.",
    "Liberar a criação de sites e definir regras que valem para todos eles, como moderação, usuário convidado e parceiros.",
    "A empresa liga digital experiences e passa a ter um domínio de sites no formato MyDomainName.my.site.com, onde cria o portal de clientes.",
    (PROD, "experiencias-externas"),
    [("interface-e-experiencia-do-usuario", "experiencias-web-portais-e-mobile", "É o ponto de partida para montar sites e portais.")],
    [("CommunitiesSettings", "Ativação e opções gerais dos sites, implantáveis.")], [],
    ["src:help-digital-experiences-enable", "src:help-experience-org-setup", S_COMM], [SEM_OBJ],
    setup("Setup > Quick Find: Digital Experiences > Digital Experiences > Settings", "src:help-digital-experiences-enable"),
    alertas=["Depois de ligar digital experiences, não dá para desligar."],
    pre=["Customize Application (para ligar digital experiences)."])

print("lote 6b: 6 metadata types, 1 estrutura, 4 funcionalidades novas, 2 ampliadas e 9 descrições de Settings gravados")
