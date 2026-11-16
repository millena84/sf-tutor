"""Lote 6d (issue #34, item 3): metadata types do tema Automação de processos e regras de negócio.

Cadastra ApprovalProcess, CustomNotificationType, AutoResponseRules, FlowSettings e ApexTrigger, com 13 estruturas, e liga
cada tipo à funcionalidade criada no lote 6c. Workflow não entra aqui: a referência nova não devolveu o nome de boa parte dos
elementos; o tipo é cadastrado pelo lote 7a, a partir do guia versionado. ApprovalAction.action já aponta para a estrutura
WorkflowActionReference, criada no lote 7a.

Ordem: rode lote6c_automacao.py, depois este script, depois lote7a_tipos_destravados.py, conteudo_temas.py e temas_internos.py.
Reexecutável. Uso: python3 ferramentas/carga/lotes/lote6d_automacao_tipos.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga.base import af, ev, ld, sv, caminho  # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-15"
EXTR = "fontes/extracoes/mdapi-lote6d-automacao.txt"
BASE_URL = "https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-"
VERSAO = "sem versão na URL (referência atual)"


def _f(nome, pertinencia):
    return C.fonte("src:mdapi-" + nome.lower(), f"{nome} (Metadata API)", BASE_URL + nome.lower() + ".html", pertinencia, EXTR, DATA, versao=VERSAO)


def substituir_fontes(novas):
    """Regrava as fontes com os mesmos ids (src:mdapi-approvalprocess nasceu como leitura de busca e passou a leitura da página)."""
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


substituir_fontes([_f(n, f"Arquivo, versão e propriedades do tipo {n}.") for n in
                   ("ApprovalProcess", "CustomNotificationType", "AutoResponseRules", "FlowSettings", "ApexTrigger")])
# src:mdapi-workflow é registrada pelo lote 7a, com a leitura do guia versionado.

S_AP, S_CNT, S_ARR = "src:mdapi-approvalprocess", "src:mdapi-customnotificationtype", "src:mdapi-autoresponserules"
S_FS, S_TRG = "src:mdapi-flowsettings", "src:mdapi-apextrigger"

FALSE = ("false", False, "A página declara default false.")
TRUE = ("valor", "true", None)
FULLNAME = M.FULLNAME_HERDADO(None)
NOTA_COB = "Universo esperado = tabela Fields da página oficial lida em 2026-11-15 (mais fullName herdado)."
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
ACOES = "Ações de workflow executadas quando {}."

# ---------------------------------------------------------------- estruturas de ApprovalProcess
AP = ["mdt:ApprovalProcess"]
M.struct("ApprovalAction", S_AP, AP + ["mdx:ApprovalStep"], [
    P("action", "WorkflowActionReference[]", None, "Ações de workflow a executar, cada uma referenciada pelo nome e pelo tipo.",
      estrutura="WorkflowActionReference"),
], "Lista de ações de workflow ligadas a um momento do processo de aprovação.")
M.struct("ApprovalEntryCriteria", S_AP, AP + ["mdx:ApprovalStep"], [
    P("booleanFilter", "string", None, "Lógica de filtro aplicada aos criteriaItems. Omita se usar formula."),
    P("criteriaItems", "FilterItem[]", None, "Critérios que o registro precisa atender. Entradas com valueField não são suportadas.", estrutura="FilterItem"),
    P("formula", "string", None, "Fórmula que precisa resultar em verdadeiro. Use filtro ou fórmula, não os dois."),
], "Critério de entrada de um processo de aprovação ou de um passo.")
M.struct("ApprovalPageField", S_AP, AP, [
    P("field", "string[]", None, "Campos exibidos ao aprovador."),
], "Campos mostrados na página de aprovação.")
M.struct("ApprovalStep", S_AP, AP, [
    P("allowDelegate", "boolean", None, "Indica se aprovadores delegados são aceitos neste passo."),
    P("approvalActions", "ApprovalAction", None, ACOES.format("o passo é aprovado"), estrutura="ApprovalAction"),
    P("assignedApprover", "ApprovalStepApprover", None, "Aprovadores atribuídos ao passo.", "S", estrutura="ApprovalStepApprover"),
    P("description", "string", None, "Descrição do passo."),
    P("entryCriteria", "ApprovalEntryCriteria", None, "Registros que podem entrar neste passo.", estrutura="ApprovalEntryCriteria"),
    P("ifCriteriaNotMet", "StepCriteriaNotMetType", None, "O que fazer com o registro que não atende ao critério de entrada do passo.", vals=[
        ("ApproveRecord", None), ("RejectRecord", "Só no primeiro passo."), ("GotoNextStep", None)]),
    P("label", "string", None, "Nome do passo.", "S"),
    P("name", "string", None, "Nome único do passo: letras, dígitos e sublinhados simples; começa com letra.", "S"),
    P("rejectBehavior", "ApprovalStepRejectBehavior", None, "Comportamento quando o aprovador rejeita neste passo.",
      "C:Obrigatório, exceto no primeiro passo.", estrutura="ApprovalStepRejectBehavior"),
    P("rejectionActions", "ApprovalAction", None, ACOES.format("o registro é rejeitado neste passo"), estrutura="ApprovalAction"),
], "Um passo do processo de aprovação: quem aprova, que registros entram e o que acontece ao aprovar ou rejeitar.")
M.struct("ApprovalStepApprover", S_AP, ["mdx:ApprovalStep"], [
    P("approver", "Approver[]", None, "Aprovadores atribuídos; até 25 por passo.", estrutura="Approver"),
    P("whenMultipleApprovers", "RoutingType", None, "Como as respostas de vários aprovadores se combinam.", default=("valor", "Unanimous", None),
      vals=[("Unanimous", None), ("FirstResponse", None)]),
], "Conjunto de aprovadores de um passo e a regra para combinar as respostas.")
M.struct("ApprovalStepRejectBehavior", S_AP, ["mdx:ApprovalStep"], [
    P("type", "StepRejectBehaviorType", None, "Tipo de comportamento na rejeição. Não é permitido no primeiro passo.", "S",
      vals=[("RejectRequest", None), ("BackToPrevious", None)]),
], "O que acontece quando um passo é rejeitado.")
M.struct("ApprovalSubmitter", S_AP, AP, [
    P("submitter", "string", None, "Usuário ou grupo específico que pode submeter.",
      "C:Obrigatório, salvo quando type é owner, creator ou allInternalUsers."),
    P("type", "ProcessSubmitterType", None, "Tipo de usuário ou grupo que pode submeter.", "S", vals=[
        (v, None) for v in ("group", "role", "user", "roleSubordinates", "roleSubordinatesInternal", "owner", "creator", "partnerUser",
                            "customerPortalUser", "portalRole", "portalRoleSubordinates", "allInternalUsers")]),
], "Quem pode submeter registros ao processo de aprovação.")
M.struct("Approver", S_AP, ["mdx:ApprovalStepApprover"], [
    P("name", "string", None, "Identifica o aprovador atribuído. É ignorado quando type é adhoc ou userHierarchyField."),
    P("type", "NextOwnerType", None, "Tipo do aprovador; com name, identifica quem aprova.", "S",
      vals=[("adhoc", None), ("user", None), ("userHierarchyField", None), ("relatedUserField", None), ("queue", None)]),
], "Um aprovador de um passo.")
M.struct("NextAutomatedApprover", S_AP, AP, [
    P("useApproverFieldOfRecordOwner", "boolean", None,
      "Indica se o primeiro passo usa o campo de hierarquia do dono do registro, em vez do de quem submeteu.", "S"),
    P("userHierarchyField", "string", None, "Campo de hierarquia de usuário, padrão ou customizado, que fornece o aprovador.", "S"),
], "Campo de hierarquia usado para atribuir aprovadores automaticamente.")

# ---------------------------------------------------------------- estruturas de CustomNotificationType e AutoResponseRules
M.struct("CustomNotificationActionGroup", S_CNT, ["mdt:CustomNotificationType"], [
    P("actions", "CustomNotificationActionDefinition[]", None, "Ações de um grupo de ações móveis.", estrutura="CustomNotificationActionDefinition"),
    P("groupName", "string", None, "Nome único do grupo de ações móveis.", "S"),
], "Grupo de ações que o usuário pode executar direto numa notificação móvel.")
M.struct("CustomNotificationActionDefinition", S_CNT, ["mdx:CustomNotificationActionGroup"], [
    P("actionLabel", "string", None, "Nome da ação mostrado na notificação push.", "S"),
    P("actionName", "string", None, "Identificador único da ação dentro do grupo.", "S"),
    P("actionTarget", "string", None, "Nome da classe Apex que implementa a ação."),
    P("actionType", "NotificationActionType", None, "Tipo da ação.", "S", vals=[
        ("NotificationApiAction", "Ação do lado do servidor: o cliente faz uma chamada à API de ação."),
        ("Share", "Ação do lado do cliente: o app compartilha o conteúdo da notificação.")]),
], "Uma ação executável a partir de uma notificação.")

SEM_VALORES = "A página de AutoResponseRules cita a enumeração {}, mas o texto lido não lista os valores."
M.struct("AutoResponseRule", S_ARR, ["mdt:AutoResponseRules"], [
    P("active", "boolean", None, "Indica se a regra está ativa."),
    P("fullName", "string", None, "Nome da regra; herdado do tipo Metadata. Deve ser informado ao criar, atualizar ou excluir.", "?", herdada="Metadata"),
    P("ruleEntry", "RuleEntry[]", None, "Entradas da regra de resposta automática.", estrutura="AutoResponseRules_RuleEntry"),
], "Uma regra de resposta automática nomeada.")
M.struct("AutoResponseRules_RuleEntry", S_ARR, ["mdx:AutoResponseRule"], [
    P("assignedTo", "string", None, None),
    P("assignedToType", "AssignToLookupValueType", None, None, natureza="desconhecida", contexto=SEM_VALORES.format("AssignToLookupValueType")),
    P("booleanFilter", "string", None, "Condições avançadas de filtro da entrada."),
    P("businessHours", "string", None, None),
    P("businessHoursSource", "BusinessHoursSourceType", None, None, natureza="desconhecida", contexto=SEM_VALORES.format("BusinessHoursSourceType")),
    P("criteriaItems", "FilterItem[]", None, "Itens que definem o critério da entrada.", estrutura="FilterItem"),
    P("disableEscalationWhenModified", "boolean", None, None),
    P("escalationAction", "EscalationAction[]", None, None, estrutura="EscalationAction"),
    P("escalationStartTime", "EscalationStartTimeType", None, None, natureza="desconhecida", contexto=SEM_VALORES.format("EscalationStartTimeType")),
    P("formula", "string", None, "Fórmula da entrada. Use formula ou criteriaItems, não os dois."),
    P("notifyCcRecipients", "boolean", None, None),
    P("overrideExistingTeams", "boolean", None, None),
    P("replyToEmail", "string", None, "Endereço de e-mail que aparece no cabeçalho reply-to."),
    P("senderEmail", "string", None, "Endereço de e-mail da pessoa ou fila que envia a resposta."),
    P("senderName", "string", None, "Nome da pessoa ou fila que envia a resposta."),
    P("team", "string[]", None, None),
    P("template", "string", None, "Template de e-mail enviado automaticamente ao destinatário. A página recomenda templates Classic."),
], "Entrada de uma regra de resposta automática. O id do projeto inclui o tipo pai porque AssignmentRules e EscalationRules têm subtipos com o "
   "mesmo nome RuleEntry. A página lista o RuleEntry genérico, com campos de outros tipos de regra (atribuição e escalonamento) sem descrição.")

# ---------------------------------------------------------------- metadata types
M.mdt("ApprovalProcess", S_AP,
      "Um processo de aprovação clássico: quem pode submeter, que registros entram, os passos com seus aprovadores e as ações de cada momento.",
      "Versionar e implantar processos de aprovação em vez de recriá-los à mão em cada ambiente.", "28.0", [
          P("active", "boolean", None,
            "Indica se o processo está ativo. Depois de ativado, a estrutura dos passos e o comportamento de rejeição e de pulo ficam travados.", "S"),
          P("allowedSubmitters", "ApprovalSubmitter[]", None, "Usuários que podem submeter registros para aprovação.", "?", estrutura="ApprovalSubmitter",
            notas=["A tabela marca o campo como não obrigatório, mas a descrição diz que ele é obrigatório."]),
          P("allowRecall", "boolean", None, "Indica se quem submeteu pode retirar (recall) o pedido. Com false, só administradores podem."),
          P("approvalPageFields", "ApprovalPageField", None, "Campos mostrados na página de aprovação. O padrão inclui Name e Owner.", estrutura="ApprovalPageField"),
          P("approvalStep", "ApprovalStep[]", None, "Definições dos passos de aprovação.", estrutura="ApprovalStep"),
          P("description", "string", None, "Descrição do processo de aprovação."),
          P("emailTemplate", "string", None, "Template Classic usado nos e-mails de pedido de aprovação. Sem ele, vale o template padrão."),
          P("enableMobileDeviceAccess", "boolean", None,
            "Deixa os aprovadores acessarem a página de aprovação por qualquer navegador, sem login. Com true, aprovadores adhoc não são permitidos."),
          P("entryCriteria", "ApprovalEntryCriteria", None, "Define que registros entram no processo. Omitido, entram todos.", estrutura="ApprovalEntryCriteria"),
          P("finalApprovalActions", "ApprovalAction", None, ACOES.format("todas as aprovações exigidas são dadas"), estrutura="ApprovalAction"),
          P("finalApprovalRecordLock", "boolean", None, "Mantém o registro bloqueado depois da aprovação final.", default=FALSE),
          P("finalRejectionActions", "ApprovalAction", None, ACOES.format("o registro chega à rejeição final"), estrutura="ApprovalAction"),
          P("finalRejectionRecordLock", "boolean", None, "Mantém o registro bloqueado depois da rejeição final.", default=FALSE),
          P("initialSubmissionActions", "ApprovalAction", None, ACOES.format("o registro é submetido pela primeira vez"), estrutura="ApprovalAction"),
          P("label", "string", None, "Nome do processo de aprovação.", "S"),
          P("nextAutomatedApprover", "NextAutomatedApprover", None,
            "Campo de hierarquia usado para atribuir automaticamente os aprovadores dos passos. Omitido, a atribuição automática fica desligada.",
            estrutura="NextAutomatedApprover"),
          P("postTemplate", "string", None, "Template de post do Chatter para aprovações. Exige objeto com feed tracking."),
          P("processOrder", "int", None, None),
          P("recallActions", "ApprovalAction", None, ACOES.format("um pedido pendente é retirado"), estrutura="ApprovalAction"),
          P("recordEditability", "RecordEditabilityType", None, "Quem pode editar registros que aguardam aprovação.", "S",
            vals=[("AdminOnly", None), ("AdminOrCurrentApprover", None)]),
          P("showApprovalHistory", "boolean", None, "Inclui a lista relacionada Approval History na página de aprovação."),
          FULLNAME,
      ], exemplo=CAB + f"""<ApprovalProcess {NS}>
    <active>false</active>
    <allowedSubmitters>
        <!-- Valores documentados incluem owner, creator, user, role, group -->
        <type>owner</type>
    </allowedSubmitters>
    <approvalStep>
        <assignedApprover>
            <approver>
                <name>[nome do usuário ou da fila]</name>
                <type>user</type>
            </approver>
            <!-- Valores documentados: Unanimous, FirstResponse -->
            <whenMultipleApprovers>Unanimous</whenMultipleApprovers>
        </assignedApprover>
        <label>[rótulo do passo]</label>
        <name>[Nome_Do_Passo]</name>
    </approvalStep>
    <label>[rótulo do processo]</label>
    <!-- Valores documentados: AdminOnly, AdminOrCurrentApprover -->
    <recordEditability>AdminOnly</recordEditability>
</ApprovalProcess>""", curinga=True,
      alertas=["O metadado não guarda a ordem dos processos ativos: pode ser preciso reordená-los depois do deploy.",
               "Implantar um processo sem entry criteria sobre um que já tem mantém os critérios existentes.",
               "No package.xml, o curinga parcial (por exemplo Lead.*) não é suportado; use * para todos.",
               "Send actions e processos de aprovação de rascunhos de e-mail não são suportados pela Metadata API."],
      divergencias=["Na página (src:mdapi-approvalprocess), allowedSubmitters aparece como não obrigatório na tabela, mas a descrição diz que é obrigatório."],
      cobertura_nota=NOTA_COB)

M.mdt("CustomNotificationType", S_CNT,
      "Um tipo de notificação customizada: nome, descrição e em que canais ela é entregue (desktop e mobile).",
      "Versionar e implantar os tipos de notificação que as automações usam para avisar pessoas.", "46.0", [
          P("actionGroups", "CustomNotificationActionGroup[]", None,
            "Grupos de ações móveis, que deixam o usuário agir direto na notificação do celular.", estrutura="CustomNotificationActionGroup",
            notas=["A página marca o recurso como Beta."]),
          P("customNotifTypeName", "string", None, "Nome do tipo de notificação. Até 80 caracteres.", "S"),
          P("description", "string", None, "Descrição geral, mostrada junto do nome do tipo. Até 255 caracteres."),
          P("desktop", "boolean", None, "Liga (true) ou desliga (false) o canal de entrega no desktop.", "S"),
          P("masterLabel", "string", None, "Rótulo do tipo de notificação.", "S"),
          P("mobile", "boolean", None, "Liga (true) ou desliga (false) o canal de entrega no mobile.", "S"),
          P("slack", "boolean", None, "Reservado para uso futuro."),
          FULLNAME,
      ], exemplo=CAB + f"""<CustomNotificationType {NS}>
    <customNotifTypeName>[nome do tipo, até 80 caracteres]</customNotifTypeName>
    <description>[descrição, até 255 caracteres]</description>
    <!-- Canais de entrega -->
    <desktop>true</desktop>
    <masterLabel>[rótulo do tipo]</masterLabel>
    <mobile>true</mobile>
</CustomNotificationType>""", curinga=False,
      alertas=["O curinga * não é suportado para este tipo no package.xml: liste cada tipo de notificação pelo nome."],
      cobertura_nota=NOTA_COB,
      setup=af("verificado", "Setup > Quick Find: Notification Builder > Custom Notifications", "Lista dos tipos de notificação. " + C.UI_EN,
               [ev("src:help-notif-flow-example")]))

M.mdt("AutoResponseRules", S_ARR,
      "As regras de resposta automática de um objeto (lead ou caso): cada regra tem entradas com critério e template de e-mail.",
      "Versionar e implantar as regras que enviam o primeiro e-mail a quem abriu um caso ou enviou um lead.", "27.0", [
          P("autoResponseRule", "AutoResponseRule[]", None, "Definições das regras de resposta automática nomeadas.", estrutura="AutoResponseRule"),
      ], exemplo=CAB + f"""<AutoResponseRules {NS}>
    <autoResponseRule>
        <fullName>[nome da regra]</fullName>
        <active>false</active>
        <!-- As entradas são avaliadas em ordem; a regra para na primeira que casar -->
        <ruleEntry>
            <senderEmail>[e-mail do remetente]</senderEmail>
            <senderName>[nome do remetente]</senderName>
            <template>[pasta/nome do template de e-mail]</template>
        </ruleEntry>
    </autoResponseRule>
</AutoResponseRules>""", curinga=True, completa=False,
      alertas=["Há um arquivo por objeto (por exemplo Case.autoResponseRules). Para apontar uma regra específica no package.xml, a página usa o "
               "nome AutoResponseRule com o membro Objeto.regra.",
               "Templates Lightning não são empacotáveis; a página recomenda templates Classic."],
      cobertura_nota="Universo esperado = tabela Fields da página oficial lida em 2026-11-15. Parcial: três enumerações de RuleEntry não têm os "
                     "valores listados no texto lido.")

M.mdt("FlowSettings", S_FS,
      "Configurações de flows e processos da org: runtime, permissões de execução, comportamento de fórmulas e opções de depuração.",
      "Recuperar e implantar as configurações gerais de flows em vez de marcá-las à mão em cada ambiente.", "47.0", [
          P("canDebugFlowAsAnotherUser", "boolean", "50.0", "Indica se flows podem ser depurados como outro usuário."),
          P("doesEnforceApexCpuTimeLimit", "boolean", "51.0", "Indica se a Salesforce mede com precisão o tempo de CPU que flows e processos consomem."),
          P("doesFormulaEnforceDataAccess", "boolean", "48.0", "Indica se recursos e campos de fórmula respeitam a segurança no nível do registro."),
          P("doesFormulaGenerateHtmlOutput", "boolean", "48.0", "Indica se fórmulas que geram HTML, como BR(), incluem marcadores codificados."),
          P("enableEmailSimpleRespectProfiles", "boolean", None, None),
          P("enableEmailsimpleSecureProfiles", "boolean", None, None),
          P("enableFlowBREncodedFixEnabled", "boolean", None, "Define se BR() gera uma quebra de linha ou o literal _BR_ENCODED_."),
          P("enableFlowCustomPropertyEditor", "boolean", "48.0", "Indica se custom property editors estão ligados para ações e campos de tela.", ate="50.0",
            notas=["Descontinuado na API 50.0."]),
          P("enableFlowDeployAsActiveEnabled", "boolean", None, "Indica se processos e flows podem ser implantados já ativos.",
            notas=["Padrão false em produção e true em orgs que não são de produção."]),
          P("enableFlowFieldFilterEnabled", "boolean", None,
            "Indica se Create Records e Update Records gravam só os campos editáveis, em vez de falhar.", default=FALSE),
          P("enableFlowFormulasFixEnabled", "boolean", None, "Indica se fórmulas devolvem nulo, e não exceção, quando o registro ou o campo de lookup é nulo."),
          P("enableFlowInterviewSharingEnabled", "boolean", None, "Indica se usuários retomam entrevistas pausadas a que têm acesso de edição.", default=TRUE),
          P("enableFlowListMetadataLargeCapEnabled", "boolean", None, "Reservado para uso interno."),
          P("enableFlowNullPreviousValueFix", "boolean", None, "Indica se processos avaliam os critérios com os valores originais do registro, do início do processo."),
          P("enableFlowPauseEnabled", "boolean", None, "Indica se as telas podem mostrar o botão Pause.", default=FALSE),
          P("enableFlowReactiveChoiceOptions", "boolean", None, None),
          P("enableFlowReactiveScreens", "boolean", None, "Indica se componentes de tela reagem uns aos outros; vale só para as versões 57.0 e 58.0 da API.",
            default=FALSE),
          P("enableFlowsLightningApp", "boolean", "68.0", "Indica se os usuários podem usar o app Lightning Automation para gerir flows e recursos relacionados."),
          P("enableFlowUseApexExceptionEmail", "boolean", None, "Indica se os e-mails de erro vão para os endereços de Apex Exception Email.", default=FALSE),
          P("enableFlowViaRestUsesUserCtxt", "boolean", "54.0", "Indica se flows rodados por REST usam o perfil e os permission sets do usuário que executa."),
          P("enableInvocableFlowFixEnabled", "boolean", None, "Indica se todas as entrevistas autolaunched executam quando invocadas em massa.",
            notas=["Removido na API 50.0."]),
          P("enableLightningRuntimeEnabled", "boolean", None, "Indica se flows abertos por URL ou pelo Setup usam o runtime Lightning.", default=TRUE),
          P("flowOccurrenceLogging", "boolean", None, None),
          P("isAccessToInvokedApexRequired", "boolean", "47.0", "Indica se flows só invocam Apex quando o usuário tem acesso à classe.", ate="58.0",
            notas=["Descontinuado na API 59.0."]),
          P("isApexPluginAccessModifierRespected", "boolean", "48.0", "Indica se flows respeitam modificadores de acesso public em ações Apex legadas."),
          P("isEnhancedFlowListViewVisible", "boolean", None, "Indica se a list view aprimorada de Flows substitui a Classic.", default=TRUE),
          P("isFlowApexContextRetired", "boolean", "49.0", "Indica se as regras explícitas de acesso a classes Apex estão desligadas.", ate="58.0",
            default=("valor", "true", "true na maioria das orgs."), notas=["Descontinuado na API 59.0."]),
          P("isFlowBlockAccessToSessionIDEnabled", "boolean", None, "Indica se a variável de session ID recebe um texto substituto.", default=FALSE),
          P("isManageFlowRequiredForAutomationCharts", "boolean", None,
            "Indica se a permissão Manage Flow é exigida para ver todos os gráficos do Automation Home.", default=FALSE),
          P("isSupportRollbackOnErrorForApexInvocableActionsEnabled", "boolean", None, None),
          P("isTimeResumedInSameRunContext", "boolean", "57.0", "Indica se flows autolaunched pausados retomam no mesmo contexto e com o mesmo acesso.",
            ate="58.0", notas=["Removido na API 59.0."]),
          FULLNAME,
      ], exemplo=CAB + f"""<FlowSettings {NS}>
    <!-- Implantar flows já ativos: false em produção por padrão -->
    <enableFlowDeployAsActiveEnabled>false</enableFlowDeployAsActiveEnabled>
    <enableFlowPauseEnabled>false</enableFlowPauseEnabled>
    <enableLightningRuntimeEnabled>true</enableLightningRuntimeEnabled>
</FlowSettings>""", arquivos_prontos=M.arquivos_settings("FlowSettings", "Flow", S_FS), curinga=False,
      alertas=["No package.xml, use o tipo Settings com o membro Flow; o curinga só vale para recuperar todas as configurações.",
               "Vários campos são legados, com faixa de versões: confira a versão da API antes de implantar."],
      cobertura_nota=NOTA_COB)

M.mdt("ApexTrigger", S_TRG,
      "Um trigger Apex: código que roda antes ou depois de eventos de gravação (DML) num objeto.",
      "Versionar e implantar triggers junto com o resto do código da org.", "10.0", [
          P("apiVersion", "double", None, "Versão da API do trigger, definida na criação.", "S"),
          P("content", "base64Binary", None, "A definição do trigger (o código-fonte).", "?", herdada="MetadataWithContent", natureza="texto_livre",
            contexto="Na API, o conteúdo trafega em base64; em arquivo, é o código-fonte .trigger."),
          P("fullName", "string", None,
            "Nome do trigger; herdado. Começa com letra e não pode terminar com sublinhado nem ter dois sublinhados seguidos.", "?", herdada="Metadata"),
          P("packageVersions", "PackageVersion[]", "16.0", "Versões de pacotes gerenciados instalados que o trigger referencia.",
            notas=["A página remete à referência de ApexClass para os campos de PackageVersion; a estrutura não foi lida."]),
          P("status", "ApexCodeUnitStatus", None, "Estado do trigger.", "S", vals=[
              ("Active", "O trigger está ativo."), ("Inactive", "O trigger está inativo, mas não foi excluído."),
              ("Deleted", "O trigger está marcado para exclusão; útil na atualização de pacotes gerenciados.")]),
      ], exemplo=CAB + f"""<!-- Arquivo de metadado que acompanha o código-fonte .trigger -->
<ApexTrigger {NS}>
    <apiVersion>68.0</apiVersion>
    <!-- Valores documentados: Active, Inactive, Deleted -->
    <status>Active</status>
</ApexTrigger>""", estende="MetadataWithContent", curinga=True, completa=False,
      alertas=["O componente tem dois arquivos: o código-fonte .trigger e o arquivo de metadado que o acompanha.",
               "É suportado por todas as chamadas da Metadata API, exceto as CRUD-based."],
      cobertura_nota="Universo esperado = tabela Fields da página oficial lida em 2026-11-15. Parcial: PackageVersion não foi detalhado.",
      setup=af("verificado", "Object management settings do objeto > Triggers", "Lista de triggers do objeto. " + C.UI_EN, [ev("src:apex-triggers-defining")]))

M.emit_structs()

# Estruturas que já existiam e passam a ser usadas também aqui.
for nome, quem, src in (("FilterItem", ["mdx:ApprovalEntryCriteria", "mdx:AutoResponseRules_RuleEntry"], None),
                        ("EscalationAction", ["mdx:AutoResponseRules_RuleEntry"], None)):
    d = ld(f"estruturas/{nome}.json")
    d["usada_por"] = sorted(set(d["usada_por"]) | set(quem))
    sv(f"estruturas/{nome}.json", d)

# ---------------------------------------------------------------- ligação com as funcionalidades do lote 6c
C.ampliar_funcionalidade("processos-de-aprovacao", mdts=[("ApprovalProcess", "Processo de aprovação clássico implantável.")], srcs=[S_AP],
                         remover_ausencia_de="metadata_type")
C.ampliar_funcionalidade("notificacoes-customizadas", mdts=[("CustomNotificationType", "Tipo de notificação customizada implantável.")], srcs=[S_CNT],
                         remover_ausencia_de="metadata_type")
C.ampliar_funcionalidade("regras-de-resposta-automatica", mdts=[("AutoResponseRules", "Regras de resposta automática de um objeto, implantáveis.")],
                         srcs=[S_ARR], remover_ausencia_de="metadata_type")
C.ampliar_funcionalidade("apex-triggers", mdts=[("ApexTrigger", "Cada trigger Apex, com código e arquivo de metadado.")], srcs=[S_TRG],
                         remover_ausencia_de="metadata_type")
C.ampliar_funcionalidade("flow", mdts=[("FlowSettings", "Configurações gerais de flows e processos da org.")], srcs=[S_FS])

print("lote 6d: 5 metadata types e 13 estruturas gravados; 5 funcionalidades ligadas")
