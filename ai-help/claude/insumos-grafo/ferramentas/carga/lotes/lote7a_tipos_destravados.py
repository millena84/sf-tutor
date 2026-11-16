"""Lote 7a (rodada B1, issue #34): CaseSettings, Workflow (com sete tipos filhos) e Translations.

Os três tipos estavam fora do catálogo porque a referência nova da documentação não devolvia o nome dos campos. Este lote lê o
guia versionado 264.0 (API 68.0), que é a versão do inventário do projeto, e:

1. regrava as fontes src:mdapi-casesettings, src:mdapi-workflow e src:mdapi-translations apontando para o guia versionado;
2. cadastra CaseSettings (4 estruturas), Workflow, seus 7 tipos filhos (4 estruturas) e Translations (58 estruturas);
3. liga os tipos às funcionalidades casos, workflow-rules-e-process-builder, translation-workbench e custom-labels;
4. completa ApprovalProcess (WorkflowActionReference passa a existir) e marca, nos tipos cadastrados a partir da referência
   nova (lotes 6a, 6b e 6d), os campos que não constam do guia versionado.

Ordem: lote6a_org.py, lote6b_processos.py, lote6c_automacao.py, lote6d_automacao_tipos.py, este script, conteudo_temas.py e
temas_internos.py. Reexecutável (as marcações do item 4 não se duplicam).
Uso: python3 ferramentas/carga/lotes/lote7a_tipos_destravados.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga.base import af, ev, ld, sv, caminho  # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-16"
EXTR = "fontes/extracoes/mdapi-lote7a-versionado.txt"
ATLAS = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
CONFERIDOS = ("FieldServiceSettings", "MyDomainSettings", "ContractSettings", "CommunitiesSettings", "FlowSettings", "ApprovalProcess",
              "AutoResponseRules")


def substituir_fontes(novas):
    """Regrava as fontes com os mesmos ids (as três nasceram como leitura da referência nova, só com o texto geral)."""
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


def _conf(nome):
    return C.fonte(f"src:mdapi-v68-{nome.lower()}", f"{nome} (Metadata API, guia versionado 264.0)", ATLAS + f"meta_{nome.lower()}.htm",
                   f"Lista de campos de {nome} no guia versionado, para conferir o cadastro feito a partir da referência nova.", EXTR, DATA)


substituir_fontes([C.fonte_mdapi(n, EXTR, DATA) for n in ("CaseSettings", "Workflow", "Translations")] + [_conf(n) for n in CONFERIDOS])

S_CASE, S_WF, S_TR = "src:mdapi-casesettings", "src:mdapi-workflow", "src:mdapi-translations"
FULLNAME = M.FULLNAME_HERDADO(None)
NOTA_COB = "Universo esperado = tabela Fields da página do guia versionado 264.0 (API 68.0), lida em 2026-11-16."
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
B, S = "boolean", "string"

# ================================================================ CaseSettings
CS = ["mdt:CaseSettings"]
TEMPLATE = "Template de e-mail da notificação de {}, no formato pasta/nomeDoTemplate."
M.struct("FeedItemSettings", S_CASE, CS, [
    P("characterLimit", "int", None, "Limite de caracteres do item de feed."),
    P("collapseThread", B, "27.0", "Indica se a thread de e-mail aparece recolhida no item de feed.", ate="46.0",
      notas=["A página informa que o campo existiu da API 27.0 à 46.0 e foi removido."]),
    P("displayFormat", "FeedItemDisplayFormat", None, "Formato de exibição do item de feed.",
      vals=[("Default", None), ("HideBlankLines", None)]),
    P("feedItemType", "FeedItemType", None, "Tipo do item de feed a que a configuração se aplica.", vals=[("EmailMessageEvent", None)],
      contexto="A página diz que EmailMessageEvent é o único valor válido aqui."),
], "Configuração de exibição de itens de feed nos layouts de caso baseados em feed. Desde a API 32.0.")
M.struct("WebToCaseSettings", S_CASE, CS, [
    P("caseOrigin", S, None, "Origem padrão dos casos criados pelo Web-to-Case. Só vale com enableWebToCase em true."),
    P("defaultResponseTemplate", S, None, "Template de e-mail da resposta automática aos casos enviados pela web. Só vale com enableWebToCase em true."),
    P("enableWebToCase", B, None, "Indica se o Web-to-Case está ligado."),
], "Configurações do Web-to-Case, que cria casos a partir de um formulário web.")
M.struct("EmailToCaseRoutingAddress", S_CASE, ["mdx:EmailToCaseSettings"], [
    P("addressType", "EmailToCaseRoutingAddressType", None, "Tipo do endereço de roteamento.", vals=[("EmailToCase", None), ("Outlook", None)]),
    P("authorizedSenders", S, None, "Endereços ou domínios de e-mail aceitos pelo On-Demand Email-to-Case, separados por vírgula."),
    P("caseOrigin", S, None, "Origem padrão dos casos criados por este endereço."),
    P("caseOwner", S, None, "Dono padrão dos casos, informado pelo username do usuário ou pelo nome da fila."),
    P("caseOwnerType", S, None, "Indica se o dono padrão é um usuário ou uma fila."),
    P("casePriority", S, None, "Prioridade padrão dos casos criados por este endereço."),
    P("createTask", B, None, "Indica se uma tarefa é criada para o dono quando o caso nasce de um e-mail."),
    P("emailAddress", S, None, "Endereço de e-mail que recebe e roteia as mensagens."),
    P("emailServicesAddress", S, None, "Endereço gerado pela Salesforce, para onde o e-mail é encaminhado. Somente leitura."),
    P("fallbackQueue", S, "56.0", "Fila usada quando o flow de Omni-Channel não consegue rotear o caso."),
    P("isPermsetControlled", B, "61.0", "Indica se só usuários com acesso dado por permission set podem enviar por este endereço."),
    P("isVerified", B, None, "Indica se o endereço foi verificado pelo cliente. Somente leitura."),
    P("newEntityRecordType", S, None, "Record type dos casos criados por este endereço."),
    P("routingFlow", S, "56.0", "Flow de Omni-Channel que roteia os casos deste endereço."),
    P("routingName", S, None, "Nome do endereço de roteamento."),
    P("saveEmailHeaders", B, None, "Indica se as informações de roteamento e de envelope do e-mail são salvas."),
    P("taskStatus", S, None, "Status padrão das tarefas criadas. Só vale com createTask em true."),
], "Um endereço de roteamento do Email-to-Case: o endereço que recebe os e-mails e os padrões dos casos que ele cria.")
M.struct("EmailToCaseSettings", S_CASE, CS, [
    P("enableEmailToCase", B, None, "Liga o Email-to-Case. Depois de ligado, não pode ser desligado."),
    P("enableE2CAttachmentAsFile", B, None, "Indica se os anexos dos e-mails são salvos como Salesforce Files."),
    P("enableE2CDeduplicateAttachments", B, None, "Indica se anexos que já existem são só ligados ao e-mail novo, em vez de salvos de novo."),
    P("enableE2CExternalServer", B, None, "Indica se o envio usa serviços externos de e-mail, como Gmail ou Outlook. Só no Lightning Experience."),
    P("enableE2CSourceTracking", B, None, "Indica se os casos criados pelo Email-to-Case recebem Email como Case Source."),
    P("enableHtmlEmail", B, None, "Indica se o e-mail em HTML está ligado."),
    P("enableNewtoReadTriggers", B, None, "Indica se a mudança de status do e-mail, ao ser aberto, dispara triggers."),
    P("enableOnDemandEmailToCase", B, None, "Indica se o On-Demand Email-to-Case está ligado."),
    P("enableThreadIDInBody", B, None, "Indica se o Thread ID do caso vai no corpo do e-mail. Para orgs sem Lightning Threading."),
    P("enableThreadIDInSubject", B, None, "Indica se o Thread ID do caso vai no assunto do e-mail. Para orgs sem Lightning Threading."),
    P("enableThreadTokenInBody", B, None, "Indica se o compositor Lightning põe o token de threading no corpo. Para orgs com Lightning Threading."),
    P("enableThreadTokenInSubject", B, None, "Indica se o compositor Lightning põe o token de threading no assunto. Para orgs com Lightning Threading."),
    P("notifyOwnerOnNewCaseEmail", B, None, "Indica se o dono do caso é avisado quando chega um e-mail novo."),
    P("overEmailLimitAction", "EmailToCaseOnFailureActionType", None, "O que fazer com os e-mails recebidos acima do limite diário.",
      vals=[("Bounce", None), ("Discard", None), ("Requeue", None)]),
    P("preQuoteSignature", B, None, "Com true, a assinatura fica depois da resposta e antes da thread; com false, no fim do e-mail."),
    P("routingAddresses", "EmailToCaseRoutingAddress[]", None,
      "Endereços de roteamento. Remover um endereço do arquivo o exclui na org de destino.", estrutura="EmailToCaseRoutingAddress"),
    P("replyWithNewContentOnly", B, None, "Indica se a resposta sai sem o conteúdo anterior da thread."),
    P("showGeneratedEmailCheckbox", B, None, "Indica se o remetente precisa confirmar que revisou os e-mails escritos pelo Einstein."),
    P("unauthorizedSenderAction", "EmailToCaseOnFailureActionType", None, "O que fazer com e-mails de remetentes não autorizados.",
      vals=[("Bounce", None), ("Discard", None)], contexto="Para este campo, a página lista só Bounce e Discard."),
    P("useEmailHeadersForThreading", B, None, "Indica se os cabeçalhos do e-mail são usados para casar respostas quando o token falha."),
], "Configurações do Email-to-Case, que cria casos a partir de e-mails recebidos.")

M.mdt("CaseSettings", S_CASE,
      "Configurações gerais de casos da org: dono e usuário padrão, templates de notificação, Case Feed, Email-to-Case e Web-to-Case.",
      "Recuperar e implantar as configurações de atendimento por casos em vez de marcá-las à mão em cada ambiente.", "27.0", [
          P("caseAssignNotificationTemplate", S, None, TEMPLATE.format("atribuição do caso")),
          P("caseAutoProcUser", B, None, "Indica se um registro de resposta automática é criado depois do primeiro e-mail do cliente."),
          P("caseCloseNotificationTemplate", S, None, TEMPLATE.format("fechamento do caso")),
          P("caseCommentNotificationTemplate", S, None, TEMPLATE.format("comentário no caso")),
          P("caseCreateNotificationTemplate", S, None, TEMPLATE.format("criação do caso")),
          P("caseFeedItemSettings", "FeedItemSettings[]", "32.0", "Configuração dos itens de feed nos layouts de caso baseados em feed.",
            estrutura="FeedItemSettings"),
          P("caseFeedReadUnreadLtng", B, None, "Indica se os itens de feed não lidos aparecem em negrito no Lightning Experience."),
          P("caseMergeInLightning", B, None, "Indica se o Case Merge está disponível no Lightning Experience."),
          P("closeCaseThroughStatusChange", B, None, "Indica se Closed aparece no campo Status nas páginas de edição do caso."),
          P("defaultCaseFeedLayoutOn", B, None, "Indica se o layout padrão do Case Feed está ligado."),
          P("defaultCaseOwner", S, None, "Dono padrão do caso, usado quando as regras de atribuição não encontram um dono."),
          P("defaultCaseOwnerType", S, None, "Indica se o dono padrão é um usuário ou uma fila.",
            notas=["A página não lista os valores aceitos."]),
          P("defaultCaseUser", S, None, "Usuário que aparece no Case History nas mudanças automáticas do caso."),
          P("emailActionDefaultsHandlerClass", S, None, "Classe Apex que fornece os valores padrão da ação de e-mail."),
          P("emailToCase", "EmailToCaseSettings", None, "Configurações do Email-to-Case.", estrutura="EmailToCaseSettings"),
          P("enableCaseFeed", B, None, "Indica se o Case Feed está ligado."),
          P("enableCollapseEmailThread", B, "47.0", "Indica se as mensagens anteriores da thread são removidas dos itens de feed de e-mail."),
          P("enableDraftEmails", B, None, "Indica se os rascunhos de e-mail estão ligados. Exige Case Feed e Email-to-Case."),
          P("enableEarlyEscalationRuleTriggers", B, None, "Indica se os gatilhos antecipados das regras de escalonamento estão ligados."),
          P("enableEmailActionDefaultsHandler", B, None, "Indica se a configuração Email Action Default Handler está ligada."),
          P("enableEmailContactOnCasePost", B, None,
            "Indica se o contato do caso recebe e-mail quando há post visível externamente em sites do Experience Builder."),
          P("enableEscalateQfiToCaseInternal", B, None, "Indica se moderadores podem criar casos a partir de perguntas do Chatter na org."),
          P("enableEscalateQfiToCaseNetworks", B, None, "Indica se moderadores podem criar casos a partir de perguntas do Chatter nos sites."),
          P("enableExtNetworksCaseFeedEnabled", B, None, "Indica se os membros do site veem e-mails, comentários e atualizações do caso no feed."),
          P("enableMultiLangSolnSrchCSS", B, None, "Indica se a busca multilíngue de Solutions está ligada nos portais self-service."),
          P("enableMultiLangSolnSrchPKB", B, None, "Indica se a busca multilíngue de Solutions está ligada nas Solutions públicas."),
          P("enableMultiLangSolution", B, None, "Indica se as Solutions multilíngues estão ligadas."),
          P("enableNewEmailDefaultTemplate", B, None, "Indica se os templates padrão de e-mail estão ligados. Só vale com os rascunhos de e-mail ligados."),
          P("enableSolutionCategory", B, None, "Indica se a navegação de Solutions por categoria está ligada."),
          P("enableSolutionInlineCategory", B, None, "Indica se a trilha de categorias aparece nas Solutions."),
          P("enableSolutionShortSummary", B, None, "Indica se os resumos curtos de Solutions estão ligados."),
          P("enableSuggestedArticlesApplication", B, None,
            "Indica se Suggested Articles aparece nas páginas de caso do app. Só vale com enableSuggestedSolutions em false."),
          P("enableSuggestedArticlesCustomerPortal", B, None,
            "Indica se Suggested Articles aparece no Customer Portal. Só vale com enableSuggestedSolutions em false."),
          P("enableSuggestedArticlesPartnerPortal", B, None,
            "Indica se Suggested Articles aparece no portal de parceiros. Só vale com enableSuggestedSolutions em false."),
          P("enableSuggestedSolutions", B, None, "Indica se o botão View Suggested Solutions (ou Find Articles) aparece nas páginas de caso."),
          P("escalateCaseBefore", B, None, "Indica se os gatilhos antecipados de escalonamento estão ligados nas regras de escalonamento."),
          P("genericMessageEnabled", B, None, "Indica se as mensagens genéricas estão ligadas."),
          P("keepCaseMergeRecords", B, None, "Indica se os casos duplicados são mantidos, e não excluídos, depois do merge."),
          P("keepRecordTypeOnAssignmentRule", B, None,
            "Em casos criados à mão, mantém o record type do caso em vez de aplicar o padrão de quem o recebe pela regra de atribuição."),
          P("newEmailDefaultTemplateClass", S, None,
            "Classe Apex que define o template padrão dos novos e-mails do Case Feed. Só vale com enableNewEmailDefaultTemplate em true."),
          P("notifyContactOnCaseComment", B, None, "Indica se contatos que não usam o portal são avisados de um comentário novo."),
          P("notifyDefaultCaseOwner", B, None, "Indica se o dono padrão é avisado quando recebe um caso."),
          P("notifyOwnerOnCaseComment", B, None, "Indica se o dono do caso é avisado de um comentário novo."),
          P("notifyOwnerOnCaseOwnerChange", B, None, "Indica se Send Notification Email já vem marcado quando o dono muda para um usuário."),
          P("predictiveSupportEnabled", B, None, "Indica se o suporte preditivo está ligado."),
          P("showEmailAttachmentsInCaseAttachmentsRL", B, "40.0", "Indica se os anexos de e-mail aparecem na lista relacionada Attachments do caso."),
          P("showFewerCloseActions", B, None, "Indica se o botão Save & Close e o link Cls ficam escondidos."),
          P("systemUserEmail", S, None, "Endereço de e-mail usado quando o usuário padrão do caso é o system user."),
          P("useSystemEmailAddress", B, None,
            "Com true, as notificações parecem vir de um endereço de sistema; com false, do usuário que atualizou o caso."),
          P("useSystemUserAsDefaultCaseUser", B, None,
            "Indica se o system user é o usuário automático do caso. Com false, defaultCaseUser precisa ser informado."),
          P("visibleInCssCheckbox", B, None,
            "Visibilidade padrão do caso no portal self-service (CSS). Segundo a página, false quer dizer visível por padrão."),
          P("webToCase", "WebToCaseSettings", None, "Configurações do Web-to-Case.", estrutura="WebToCaseSettings"),
          FULLNAME,
      ], exemplo=CAB + f"""<CaseSettings {NS}>
    <closeCaseThroughStatusChange>true</closeCaseThroughStatusChange>
    <!-- Dono usado quando as regras de atribuição não encontram ninguém -->
    <defaultCaseOwner>[username do usuário ou nome da fila]</defaultCaseOwner>
    <emailToCase>
        <!-- Depois de ligado, o Email-to-Case não pode ser desligado -->
        <enableEmailToCase>false</enableEmailToCase>
    </emailToCase>
    <webToCase>
        <enableWebToCase>false</enableWebToCase>
    </webToCase>
</CaseSettings>""", arquivos_prontos=M.arquivos_settings("CaseSettings", "Case", S_CASE), curinga=False,
      alertas=["No package.xml, use o tipo Settings com o membro Case; o curinga só vale para recuperar todas as configurações.",
               "enableEmailToCase não pode ser desligado depois de ligado.",
               "Remover um endereço de routingAddresses do arquivo exclui esse endereço na org de destino."],
      divergencias=["A referência nova da documentação lista 69 campos de primeiro nível em CaseSettings; o guia versionado 264.0 (API 68.0), "
                    "usado neste cadastro, lista 52. Os campos a mais não foram cadastrados."],
      cobertura_nota=NOTA_COB + " A tabela não marca nenhum campo como obrigatório.")

# ================================================================ Workflow: estruturas e tipos filhos
PROTECTED = "Indica se o componente é protegido: componentes protegidos não podem ser referenciados por componentes criados em outra org."
NOME_API = "Nome único de API: letras, dígitos e sublinhados simples, começando por letra."
DESDE_WF = "A página não informa a versão do subtipo; o tipo pai, Workflow, existe desde a API 13.0."

M.struct("WorkflowActionReference", S_WF, ["mdt:WorkflowRule", "mdx:WorkflowTimeTrigger", "mdx:ApprovalAction"], [
    P("name", S, None, "Nome da ação de workflow.", "S"),
    P("type", "WorkflowActionType", None, "Tipo da ação.", "S", vals=[
        ("Alert", None), ("FieldUpdate", None), ("FlowAction", "Disponível a partir da API 30.0."), ("OutboundMessage", None), ("Task", None)]),
], "Referência a uma ação de workflow, pelo nome e pelo tipo. É como regras, gatilhos de tempo e processos de aprovação apontam para as ações.")
M.struct("WorkflowEmailRecipient", S_WF, ["mdt:WorkflowAlert"], [
    P("field", S, None, "Nome do campo referenciado pelo type; o campo precisa ser do tipo que esse valor espera."),
    P("recipient", S, None, "O destinatário (por exemplo um usuário, papel ou grupo). A página diz que a exigência depende do type."),
    P("type", "ActionEmailRecipientTypes", None, "Categoria do destinatário.", vals=[(v, None) for v in (
        "accountOwner", "accountTeam", "campaignMemberDerivedOwner", "contactLookup", "creator", "customerPortalOwner", "email", "group",
        "opportunityTeam", "owner", "partnerUser", "portalRole", "portalRoleSubordinates", "role", "roleSubordinates",
        "roleSubordinatesInternal", "user", "userLookup")]),
], "Um destinatário de um alerta de e-mail.")
M.struct("WorkflowFlowActionParameter", S_WF, ["mdt:WorkflowFlowAction"], [
    P("name", S, None, "Nome de API da variável do flow, que precisa estar marcada como entrada.", "S"),
    P("value", S, None, "Valor da variável: merge field, campo de lookup ou literal, compatível com o tipo da variável.", "S"),
], "Um valor passado a uma variável do flow quando o flow trigger o inicia.")
M.struct("WorkflowTimeTrigger", S_WF, ["mdt:WorkflowRule"], [
    P("actions", "WorkflowActionReference[]", None, "Ações executadas quando o gatilho de tempo dispara.", estrutura="WorkflowActionReference"),
    P("offsetFromField", S, None, "Campo de data a partir do qual o tempo é contado, como Created Date ou um campo customizado."),
    P("timeLength", S, None, "Quantidade de tempo antes ou depois da data de referência, na unidade escolhida. Valor negativo quer dizer antes."),
    P("workflowTimeTriggerUnit", "WorkflowTimeUnits", None, "Unidade de timeLength.", vals=[("Hours", None), ("Days", None)]),
], "Ações de uma regra de workflow que rodam um tempo antes ou depois de uma data.")


def arquivos_filho_workflow(nome):
    """Workflow não declara estratégia de decomposição no registro do CLI: o filho fica dentro do arquivo do pai."""
    ch = M.REG["types"]["workflow"]["children"]["types"][nome.lower()]
    reg_pai, reg_filho = ev("src:sdr-registry", "types.workflow"), ev("src:sdr-registry", f"types.workflow.children.types.{nome.lower()}")
    return {
        "source_format": af("verificado", {"pasta": "workflows/", "arquivo": "<Objeto>.workflow-meta.xml", "elemento": ch["xmlElementName"]},
                            "No registro do Salesforce CLI, Workflow não declara estratégia de decomposição: o componente fica dentro do arquivo do "
                            f"tipo pai, no elemento <{ch['xmlElementName']}>. O registro também traz pasta ({ch['directoryName']}) e sufixo ({ch['suffix']}) próprios "
                            "do filho; quando eles são usados não foi verificado.", [reg_pai, reg_filho]),
        "metadata_api_format": af("verificado", {"pasta": "workflows/", "arquivo": "<Objeto>.workflow", "elemento": ch["xmlElementName"]},
                                  f"Definido dentro do arquivo do tipo pai (um por objeto), no elemento <{ch['xmlElementName']}>.", [reg_pai, reg_filho, ev(S_WF)])}


def filho(nome, o_que_e, finalidade, desde, rows, exemplo, alertas=None):
    el = M.REG["types"]["workflow"]["children"]["types"][nome.lower()]["xmlElementName"]
    ex = CAB + f"<!-- No arquivo .workflow do objeto, este conteúdo fica no elemento <{el}> -->\n<{nome} {NS}>\n{exemplo}\n</{nome}>"
    M.mdt(nome, S_WF, o_que_e, finalidade, desde, rows, parent="Workflow", exemplo=ex, arquivos_prontos=arquivos_filho_workflow(nome),
          alertas=[f"No arquivo .workflow, cada componente deste tipo é um elemento <{el}> dentro de Workflow."] + (alertas or []),
          cobertura_nota=NOTA_COB + f" Contagem da seção {nome} da página de Workflow.")
    if desde is None:
        d = ld(f"metadata-types/{nome}.json")
        d["disponibilidade"] = {"desde_versao": None, "ate_versao": None, "estado": "desconhecido", "nota": DESDE_WF}
        sv(f"metadata-types/{nome}.json", d)


filho("WorkflowAlert", "Um alerta de e-mail de workflow: o template enviado, os destinatários e o remetente.",
      "Versionar e implantar os alertas de e-mail usados por regras de workflow, processos de aprovação e flows.", None, [
          P("ccEmails", "string[]", None, "Endereços adicionais em cópia; até 5. O alerta precisa de ccEmails, de recipients ou dos dois."),
          P("description", S, "16.0", "Descrição do alerta de e-mail.", "S"),
          P("fullName", S, None, NOME_API, "S"),
          P("protected", B, None, PROTECTED, "S"),
          P("recipients", "WorkflowEmailRecipient[]", None, "Destinatários do alerta. O alerta precisa de recipients, de ccEmails ou dos dois.",
            estrutura="WorkflowEmailRecipient"),
          P("senderAddress", S, None, "Endereço do remetente. Só vale quando senderType é OrgWideEmailAddress."),
          P("senderType", "ActionEmailSenderType", None, "De quem são os campos From e Reply-To do e-mail.", default=("valor", "CurrentUser", None),
            vals=[("CurrentUser", "O usuário atual."), ("DefaultWorkflowUser", "O usuário padrão de workflow."),
                  ("OrgWideEmailAddress", "Um endereço de e-mail de toda a org.")]),
          P("template", S, None, "Nome do template de e-mail. O template precisa existir na org, mas não precisa estar no mesmo arquivo zip.", "S"),
      ], """    <fullName>[Nome_Do_Alerta]</fullName>
    <description>[descrição do alerta]</description>
    <protected>false</protected>
    <recipients>
        <!-- Valores documentados incluem owner, creator, role, group, user -->
        <type>owner</type>
    </recipients>
    <!-- Valores documentados: CurrentUser, DefaultWorkflowUser, OrgWideEmailAddress -->
    <senderType>CurrentUser</senderType>
    <template>[pasta/nome do template de e-mail]</template>""")

filho("WorkflowFieldUpdate", "Uma atualização de campo de workflow: que campo muda e como o valor novo é calculado.",
      "Versionar e implantar as atualizações de campo usadas por regras de workflow e processos de aprovação.", None, [
          P("description", S, None, "Descrição da atualização de campo: por que ela foi criada."),
          P("field", S, None, "Campo do objeto que será atualizado.", "S"),
          P("formula", S, None, "Fórmula que calcula o valor novo. Usada quando operation é Formula."),
          P("fullName", S, None, NOME_API, "S"),
          P("literalValue", S, None, "Valor fixo a gravar. Usado quando operation é Literal."),
          P("lookupValue", S, None, "Valor de lookup a gravar. Usado quando operation é LookupValue."),
          P("lookupValueType", "LookupValueType", None, "Tipo do registro apontado por lookupValue.",
            vals=[("Queue", None), ("RecordType", None), ("User", None)]),
          P("name", S, "16.0", "Nome do componente.", "S"),
          P("notifyAssignee", B, None, "Indica se o responsável é avisado quando o campo é atualizado.", "S"),
          P("operation", "FieldUpdateOperation", None, "Como o valor novo é obtido.", "S", vals=[
              ("Formula", None), ("Literal", None), ("LookupValue", None), ("NextValue", None), ("Null", None), ("PreviousValue", None)]),
          P("protected", B, None, PROTECTED, "S"),
          P("reevaluateOnChange", B, None,
            "Com true, se o valor mudar, as demais regras de workflow do objeto são reavaliadas, em cascata de até 5 vezes."),
          P("targetObject", S, None, "Campo de chave estrangeira do registro filho que aponta para o pai.",
            notas=["Antes da API 14.0, o campo se chamava sourceField."]),
      ], """    <fullName>[Nome_Da_Atualizacao]</fullName>
    <field>[campo a atualizar]</field>
    <literalValue>[valor fixo]</literalValue>
    <name>[nome do componente]</name>
    <notifyAssignee>false</notifyAssignee>
    <!-- Valores documentados: Formula, Literal, LookupValue, NextValue, Null, PreviousValue -->
    <operation>Literal</operation>
    <protected>false</protected>""",
      alertas=["reevaluateOnChange faz uma atualização de campo reavaliar outras regras, em cascata de até 5 vezes."])

filho("WorkflowFlowAction", "Um flow trigger: uma ação de workflow que inicia um flow.",
      "Recuperar e implantar flow triggers que já existem na org.", "30.0", [
          P("description", S, None, "Descrição do flow trigger."),
          P("flow", S, None, "Nome de API do flow que a ação inicia.", "S"),
          P("flowInputs", "WorkflowFlowActionParameter[]", None, "Valores passados às variáveis do flow quando ele inicia.",
            estrutura="WorkflowFlowActionParameter"),
          P("label", S, None, "Nome de exibição do flow trigger.", "S"),
          P("language", S, None, "Reservado para uso futuro."),
          P("protected", B, None, "Reservado para uso futuro."),
      ], """    <flow>[Nome_De_API_Do_Flow]</flow>
    <flowInputs>
        <name>[variável de entrada do flow]</name>
        <value>[merge field, campo de lookup ou literal]</value>
    </flowInputs>
    <label>[nome de exibição]</label>""",
      alertas=["A página informa que o piloto de flow triggers está encerrado.",
               "O test mode de flow triggers não é suportado pela Metadata API."])

filho("WorkflowKnowledgePublish", "Uma ação de workflow que publica artigos do Salesforce Knowledge.",
      "Versionar e implantar as ações de publicação de artigos usadas por regras de workflow e processos de aprovação.", "27.0", [
          P("action", "KnowledgeWorkflowAction", None, "Ação de publicação.", "S", vals=[
              ("PublishAsNew", "Publica como artigo novo."), ("Publish", "Publica uma versão nova do artigo.")]),
          P("description", S, None, "Descrição breve do artigo."),
          P("label", S, None, "Rótulo que identifica o artigo na interface.", "S"),
          P("language", S, None, "Idioma do artigo."),
          P("protected", B, None, PROTECTED, "S"),
      ], """    <!-- Valores documentados: PublishAsNew, Publish -->
    <action>Publish</action>
    <label>[rótulo]</label>
    <protected>false</protected>""")

filho("WorkflowOutboundMessage", "Uma outbound message: mensagem SOAP enviada a um endpoint externo quando a regra dispara.",
      "Versionar e implantar as outbound messages usadas por regras de workflow, processos de aprovação e flows.", None, [
          P("apiVersion", "double", "18.0",
            "Versão da API da mensagem, definida automaticamente na criação. Valores válidos: 8.0 e 18.0 ou posterior.", "S"),
          P("description", S, None, "Descrição da outbound message."),
          P("endpointUrl", S, None, "URL que recebe a mensagem.", "S"),
          P("fields", "string[]", None, "Nomes dos campos enviados na mensagem."),
          P("fullName", S, None, NOME_API, "S"),
          P("includeSessionId", B, None, "Indica se a mensagem leva o session ID, para o destino chamar a API sem usuário e senha.", "S"),
          P("integrationUser", S, None, "Usuário em nome de quem a mensagem é enviada, referenciado pelo nome.", "S"),
          P("name", S, "16.0", "Nome do componente.", "S"),
          P("protected", B, None, PROTECTED, "S"),
          P("useDeadLetterQueue", B, None, "Indica se a fila de mensagens não entregues é usada quando a entrega falha. Só em orgs com a permissão."),
      ], """    <fullName>[Nome_Da_Mensagem]</fullName>
    <apiVersion>68.0</apiVersion>
    <endpointUrl>[URL do endpoint que recebe a mensagem]</endpointUrl>
    <fields>Id</fields>
    <includeSessionId>false</includeSessionId>
    <integrationUser>[username do usuário de integração]</integrationUser>
    <name>[nome do componente]</name>
    <protected>false</protected>""",
      alertas=["A apiVersion de uma outbound message só pode ser alterada pela Metadata API."])

filho("WorkflowTask", "Uma tarefa de workflow: a tarefa criada e atribuída a alguém quando a regra dispara.",
      "Versionar e implantar as tarefas usadas por regras de workflow e processos de aprovação.", None, [
          P("assignedTo", S, None, "Usuário, papel ou equipe que recebe a tarefa; precisa combinar com assignedToType."),
          P("assignedToType", "ActionTaskAssignedToTypes", None, "Categoria de quem recebe a tarefa.", vals=[(v, None) for v in (
              "accountCreator", "accountOwner", "accountTeam", "creator", "opportunityTeam", "owner", "partnerUser", "portalRole", "role", "user")]),
          P("description", S, None, "Descrição da tarefa."),
          P("dueDateOffset", "int", None, "Dias a partir da data do disparo, ou da data em offsetFromField, até o vencimento. Aceita negativo.", "S"),
          P("fullName", S, None, NOME_API, "S"),
          P("notifyAssignee", B, None, "Indica se um e-mail avisa o responsável quando a tarefa é atribuída.", "S"),
          P("offsetFromField", S, None, "Campo de data a partir do qual o vencimento é calculado."),
          P("priority", S, None, "Prioridade da tarefa criada.", "S"),
          P("protected", B, None, PROTECTED, "S"),
          P("status", S, None, "Status da tarefa criada.", "S"),
          P("subject", S, "16.0", "Assunto da tarefa, usado no e-mail de atribuição.", "S"),
      ], """    <fullName>[Nome_Da_Tarefa]</fullName>
    <!-- Valores documentados incluem owner, creator, role, user -->
    <assignedToType>owner</assignedToType>
    <dueDateOffset>2</dueDateOffset>
    <notifyAssignee>false</notifyAssignee>
    <priority>[prioridade]</priority>
    <protected>false</protected>
    <status>[status]</status>
    <subject>[assunto da tarefa]</subject>""")

filho("WorkflowRule", "Uma regra de workflow: o critério que a dispara, quando ela é avaliada e as ações que executa.",
      "Versionar e implantar regras de workflow que ainda existem na org.", None, [
          P("actions", "WorkflowActionReference[]", None, "Ações executadas quando a regra dispara.", estrutura="WorkflowActionReference"),
          P("active", B, None, "Indica se a regra está ativa.", "S"),
          P("booleanFilter", S, None, "Lógica que combina os criteriaItems, como (1 AND 2) OR 3."),
          P("criteriaItems", "FilterItem[]", None, "Critérios que disparam a regra. Informe criteriaItems ou formula.", estrutura="FilterItem"),
          P("description", S, None, "Descrição da regra."),
          P("failedMigrationToolVersion", S, "54.0", "Versão da API em que uma migração da regra falhou, para tentar de novo depois."),
          P("formula", S, None, "Fórmula que dispara a regra quando resulta em verdadeiro. Informe formula ou criteriaItems."),
          P("fullName", S, None, "Nome único de API da regra; herdado do tipo Metadata.", "?", herdada="Metadata"),
          P("triggerType", "WorkflowTriggerTypes", None, "Quando a regra é avaliada.", vals=[
              ("onAllChanges", None), ("onCreateOnly", None), ("onCreateOrTriggeringUpdate", None)]),
          P("workflowTimeTriggers", "WorkflowTimeTrigger", None, "Ações que rodam um tempo antes ou depois de uma data.",
            estrutura="WorkflowTimeTrigger"),
      ], """    <fullName>[Nome_Da_Regra]</fullName>
    <actions>
        <name>[nome da ação]</name>
        <!-- Valores documentados: Alert, FieldUpdate, FlowAction, OutboundMessage, Task -->
        <type>FieldUpdate</type>
    </actions>
    <active>false</active>
    <formula>[fórmula que resulta em verdadeiro]</formula>
    <!-- Valores documentados: onAllChanges, onCreateOnly, onCreateOrTriggeringUpdate -->
    <triggerType>onCreateOnly</triggerType>""",
      alertas=["Informe criteriaItems ou formula como critério da regra."])

M.mdt("Workflow", S_WF,
      "O conjunto de workflow de um objeto: as regras e todas as ações (alertas, atualizações de campo, tarefas, outbound messages e outras).",
      "Recuperar e implantar, de uma vez, as regras de workflow de um objeto e as ações que elas usam.", "13.0", [
          P("alerts", "WorkflowAlert[]", None, "Alertas de e-mail do objeto."),
          P("fieldUpdates", "WorkflowFieldUpdate[]", None, "Atualizações de campo do objeto."),
          P("flowActions", "WorkflowFlowAction[]", "30.0", "Flow triggers do objeto."),
          P("fullName", S, None, NOME_API, "?", herdada="Metadata"),
          P("knowledgePublishes", "WorkflowKnowledgePublish[]", "27.0", "Ações de publicação de artigos do Knowledge."),
          P("outboundMessages", "WorkflowOutboundMessage[]", None, "Outbound messages do objeto."),
          P("rules", "WorkflowRule[]", None, "Regras de workflow do objeto."),
          P("tasks", "WorkflowTask[]", None, "Tarefas de workflow do objeto."),
      ], exemplo=CAB + f"""<Workflow {NS}>
    <fieldUpdates>
        <fullName>[Nome_Da_Atualizacao]</fullName>
        <field>[campo a atualizar]</field>
        <literalValue>[valor fixo]</literalValue>
        <name>[nome do componente]</name>
        <notifyAssignee>false</notifyAssignee>
        <operation>Literal</operation>
        <protected>false</protected>
    </fieldUpdates>
    <rules>
        <fullName>[Nome_Da_Regra]</fullName>
        <!-- A regra aponta para a ação pelo nome e pelo tipo -->
        <actions>
            <name>[Nome_Da_Atualizacao]</name>
            <type>FieldUpdate</type>
        </actions>
        <active>false</active>
        <formula>[fórmula que resulta em verdadeiro]</formula>
        <triggerType>onCreateOnly</triggerType>
    </rules>
</Workflow>""", curinga=True,
      alertas=["Há um arquivo .workflow por objeto, que reúne as regras e as ações desse objeto.",
               "As ações não ficam dentro da regra: a regra aponta para cada ação pelo nome e pelo tipo (WorkflowActionReference).",
               "As mesmas ações também são usadas por processos de aprovação (ApprovalAction)."],
      divergencias=["A referência nova da documentação lista 10 campos de primeiro nível em Workflow, incluindo listas de WorkflowFlowAutomation e de "
                    "WorkflowSend sem descrição; o guia versionado 264.0 (API 68.0), usado neste cadastro, lista 8. WorkflowSend consta do inventário "
                    "v68 como filho de Workflow, mas não é descrito na página e não foi cadastrado."],
      cobertura_nota=NOTA_COB + " Os sete tipos filhos descritos na página estão cadastrados; WorkflowSend, que só consta do inventário, não.")

# ================================================================ Translations: 59 subtipos
def nm(o_que, req="S"):
    return P("name", S, None, f"Nome {o_que}.", req)


def lb(o_que, req="N", extra=""):
    return P("label", S, None, f"Rótulo traduzido {o_que}.{extra}", req)


def ds(o_que):
    return P("description", S, None, f"Descrição traduzida {o_que}.")


CASAR = " Precisa ser igual ao do componente original."
RESERVADO = "Reservado para uso interno."
LEX = "do Lightning Experience"
BOT_DIALOGS = lambda de: P("botDialogs", "BotDialogTranslation[]", None, f"Traduções dos diálogos {de}.")  # noqa: E731
TR = {  # nome: (o que é, linhas)
    "AiCoachAgentScnrDefTranslation": ("Tradução de um cenário do Agentforce Sales Coach. Desde a API 64.0.", [
        P("description", S, None, "Descrição do cenário de coaching."), P("label", S, None, "Título do cenário de coaching."),
        nm("do cenário de coaching"), P("userGuidance", S, None, "Instruções que o representante segue antes de começar a sessão de coaching.")]),
    "BotBlockTranslation": ("Tradução de um bot block. Desde a API 59.0.", [
        P("botBlockVersions", "BotBlockVersionTranslation[]", None, "Traduções das versões do bot block."),
        P("fullName", S, None, "Nome do bot block.", "S")]),
    "BotBlockVersionTranslation": ("Tradução de uma versão de bot block. Desde a API 59.0.", [
        BOT_DIALOGS("da versão do bot block"), P("fullName", S, None, "Nome da versão do bot block.", "S")]),
    "BotTemplateTranslation": ("Tradução de um template de bot. Desde a API 59.0.", [
        BOT_DIALOGS("do template de bot"), P("fullName", S, None, "Nome do template de bot.", "S")]),
    "BotTranslation": ("Tradução de um bot. Desde a API 53.0.", [
        P("botVersions", "BotVersionTranslation[]", None, "Traduções das versões do bot."),
        P("fullName", S, None, "Nome do bot." + CASAR, "S")]),
    "BotVersionTranslation": ("Tradução de uma versão de bot. Desde a API 53.0.", [
        BOT_DIALOGS("desta versão do bot"), P("fullName", S, None, "Nome da versão do bot." + CASAR, "S")]),
    "BotDialogTranslation": ("Tradução de um diálogo de bot. Desde a API 53.0.", [
        P("botSteps", "BotStepTranslation[]", None, "Traduções dos passos executados no diálogo."),
        P("developerName", S, None, "Nome único que distingue os diálogos de uma versão do bot." + CASAR, "S"),
        P("label", S, None, "Rótulo traduzido que identifica o diálogo na interface.")]),
    "BotStepTranslation": ("Tradução de um passo de diálogo de bot. Desde a API 53.0.", [
        P("botMessages", "BotMessageTranslation[]", None, "Traduções das mensagens de um passo do tipo Message."),
        P("botSteps", "BotStepTranslation[]", None, "Traduções dos passos agrupados sob um passo do tipo Group."),
        P("botVariableOperation", "BotVariableOperationTranslation", None, "Tradução da operação de variável de um passo do tipo VariableOperation."),
        P("stepIdentifier", S, None, "Chave única que liga os textos traduzidos ao passo." + CASAR, "S"),
        P("type", "BotStepType", None, "Tipo do passo." + CASAR, "S", vals=[
            ("Navigation", None), ("Invocation", None), ("VariableOperation", None), ("Message", None), ("Wait", None), ("Group", None),
            ("RecordLookup", "Exige API 48.0 ou posterior.")])]),
    "BotMessageTranslation": ("Tradução de uma mensagem de bot. Desde a API 53.0.", [
        P("message", S, None, "Mensagem traduzida que o bot envia ao cliente."),
        P("messageIdentifier", S, None, "Chave única que liga os textos traduzidos à mensagem." + CASAR, "S")]),
    "BotVariableOperationTranslation": ("Tradução de uma operação de variável (passo de pergunta) de bot. Desde a API 53.0.", [
        P("botMessages", "BotMessageTranslation[]", None, "Traduções das mensagens de pergunta de uma operação do tipo Collect."),
        P("botQuickReplyOptions", "BotQuickReplyOptionTranslation[]", None,
          "Traduções das opções fixas de escolha de uma operação Collect com respostas rápidas estáticas."),
        P("quickReplyOptionTemplate", S, None, "Template de fórmula traduzido que monta os rótulos das opções dinâmicas baseadas em objeto."),
        P("retryMessages", "BotMessageTranslation[]", None, "Traduções das mensagens das novas tentativas no Conversation Repair."),
        P("successMessages", "BotMessageTranslation[]", "57.0", "Tradução da mensagem que confirma um upload de arquivo bem-sucedido."),
        P("type", "BotVariableOperationType", None, "Tipo da operação." + CASAR, "S", vals=[
            ("Set", None), ("Unset", None), ("Collect", None), ("SetConversationLanguage", None)]),
        P("variableOperationIdentifier", S, None, "Chave única que liga os textos traduzidos à operação de variável." + CASAR, "S")]),
    "BotQuickReplyOptionTranslation": ("Tradução de uma opção de resposta rápida num passo de pergunta. Desde a API 53.0.", [
        P("literalValue", S, None, "Valor traduzido mostrado ao cliente como item de menu ou botão."),
        P("quickReplyOptionIdentifier", S, None, "Chave única que liga os textos traduzidos à opção de resposta rápida." + CASAR, "S")]),
    "ContextDefinitionTranslation": ("Tradução de uma context definition do Context Service. Desde a API 62.0.", [
        ds("da context definition"), lb("da context definition", "S"), nm("da context definition")]),
    "ConversationMessageDefinitionTranslation": ("Tradução de uma conversation message definition. Desde a API 61.0.", [
        P("constantValueTranslations", "ConversationMessageConstantValueTranslation[]", None, "Traduções dos valores constantes da mensagem."),
        lb("da conversation message definition", "S"), nm("da conversation message definition")]),
    "ConversationMessageConstantValueTranslation": ("Tradução de um valor constante de conversation message. Desde a API 61.0.", [
        nm("do valor constante"), P("value", S, None, "Valor constante traduzido.", "S")]),
    "CustomApplicationTranslation": ("Tradução de um app customizado (CustomApplication).", [
        ds("do app"), lb("do app", extra=" Até 765 caracteres."), nm("do app customizado")]),
    "CustomLabelTranslation": ("Tradução de um custom label (CustomLabels).", [
        P("label", S, None, "Texto traduzido do custom label. Até 765 caracteres.", "S"), nm("do custom label")]),
    "CustomPageWebLinkTranslation": ("Tradução de um web link de componente da home page (CustomPageWebLink).", [
        P("label", S, None, "Texto traduzido do web link.", "S"), nm("do web link")]),
    "CustomTabTranslation": ("Tradução de uma aba customizada (CustomTab).", [lb("da aba", "S"), nm("da aba customizada")]),
    "DashboardComponentTranslation": (f"Tradução de um componente de dashboard {LEX}.", [
        P("description", S, None, "Descrição do componente de dashboard."), P("footer", S, None, "Rodapé do componente de dashboard."),
        P("label", S, None, "Rótulo do componente de dashboard."), nm("do componente de dashboard")]),
    "DashboardTranslation": (f"Tradução de um dashboard {LEX}.", [ds("do dashboard"), lb("do dashboard"), nm("do dashboard")]),
    "DataConnectorTranslation": ("Tradução de um data connector. Desde a API 64.0.", [
        P("attributes", "DataConnectorAttributeTranslation[]", None, "Traduções dos atributos do data connector."),
        ds("do data connector"),
        P("errors", "DataConnectorErrorTranslation[]", None, "Traduções dos erros do data connector."),
        P("help", S, None, "Texto de ajuda traduzido do data connector."), lb("do data connector"),
        P("language", S, None, "Idioma da tradução do data connector."), nm("do data connector", "N")]),
    "DataConnectorAttributeTranslation": ("Tradução de um atributo de data connector. Desde a API 64.0.", [
        P("errorMessage", S, None, "Mensagem de erro traduzida do atributo."), P("infoMessage", S, None, "Mensagem informativa traduzida do atributo."),
        P("inputLabel", S, None, "Rótulo de entrada traduzido do atributo."), lb("do atributo", "S"), nm("do atributo"),
        P("options", "DataConnectorAttributeOptTranslation[]", None, "Traduções das opções do atributo.")]),
    "DataConnectorAttributeOptTranslation": ("Tradução de uma opção de atributo de data connector. Desde a API 64.0.", [
        lb("da opção do atributo", "S"), nm("da opção do atributo")]),
    "DataConnectorErrorTranslation": ("Tradução de um erro de data connector. Desde a API 64.0.", [lb("do erro", "S"), nm("do erro")]),
    "ExplainabilityMsgTemplateFieldTranslation": ("Tradução de um template de mensagem de explicação de decisão, por tipo de elemento de passo.", [
        P("description", S, None, "Descrição do campo de mensagem de explicação."), P("label", S, None, "Nome amigável deste tipo de tradução."),
        nm("da mensagem de explicação de decisão"), P("templateMessage", S, None, "Mensagem para um tipo específico de passo de expression set.")]),
    "FlowDefinitionTranslation": ("Tradução de uma definição de flow (FlowDefinition). Desde a API 41.0.", [
        P("flows", "FlowTranslation[]", None, "Traduções das versões do flow."),
        P("fullName", S, None, "Nome de API da definição do flow.", "S"),
        P("label", S, None, "Rótulo traduzido da definição. Depois de definido, deixa de herdar o rótulo da versão ativa.")]),
    "FlowTranslation": ("Tradução de uma versão de flow (Flow). Desde a API 41.0.", [
        P("choices", "FlowChoiceTranslation[]", None, "Traduções das choices da versão do flow."),
        P("fullName", S, None, "Nome de API da versão do flow. A partir da API 44.0, sem o número da versão."),
        lb("da versão do flow"),
        P("orchestrationStages", "FlowOrchestrationStageTranslation", "63.0", "Traduções dos estágios da orquestração."),
        P("orchestrationSteps", "FlowOrchestrationStepTranslation", "63.0", "Traduções dos passos da orquestração."),
        P("screens", "FlowScreenTranslation[]", None, "Traduções das telas da versão do flow."),
        P("stages", "FlowStageTranslation[]", "43.0", "Traduções dos estágios da versão do flow.")]),
    "FlowChoiceTranslation": ("Tradução de uma choice de uma versão de flow (FlowChoice). Desde a API 41.0.", [
        P("choiceText", S, None, "Rótulo traduzido da choice."), P("name", S, None, "Nome único da choice.", "S"),
        P("userInput", "FlowChoiceUserInputTranslation", None, "Tradução da entrada do usuário associada à choice.")]),
    "FlowChoiceUserInputTranslation": ("Tradução da entrada de usuário de uma choice (FlowChoiceUserInput). Desde a API 41.0.", [
        P("promptText", S, None, "Rótulo traduzido da entrada da choice."),
        P("validationRule", "FlowInputValidationRuleTranslation", None, "Tradução da regra de validação da entrada.")]),
    "FlowInputValidationRuleTranslation": ("Tradução de uma regra de validação de entrada de flow (FlowInputValidationRule). Desde a API 41.0.", [
        P("errorMessage", S, None, "Mensagem de erro traduzida da regra de validação.")]),
    "FlowOrchestrationStageTranslation": ("Tradução de um estágio de uma versão de orquestração (FlowOrchestratedStage). Desde a API 64.0.", [
        P("name", S, None, "Nome único da tradução do estágio.", "S"), P("stageLabel", S, None, "Rótulo traduzido do estágio.")]),
    "FlowOrchestrationStepTranslation": ("Tradução de um passo de uma versão de orquestração (FlowStageStep). Desde a API 63.0.", [
        P("name", S, None, "Nome único da tradução do passo.", "S"), P("stepLabel", S, None, "Rótulo traduzido do passo.")]),
    "FlowScreenTranslation": ("Tradução de uma tela de flow (FlowScreen). Desde a API 41.0.", [
        P("backButtonLabel", S, "54.0", "Rótulo traduzido do botão Back."),
        P("fields", "FlowScreenFieldTranslation[]", None, "Traduções dos componentes da tela."),
        P("helpText", S, None, "Texto de ajuda traduzido da tela."), P("name", S, None, "Nome de API da tela.", "S"),
        P("nextOrFinishButtonLabel", S, "54.0", "Rótulo traduzido do botão Next ou Finish."),
        P("pauseButtonLabel", S, "54.0", "Rótulo traduzido do botão Pause."),
        P("pausedText", S, None, "Mensagem traduzida que confirma a pausa.")]),
    "FlowScreenFieldTranslation": ("Tradução de um componente de tela de flow (FlowScreenField). Desde a API 41.0. "
                                   "Componentes que exigem o runtime Lightning não são suportados.", [
        P("fieldText", S, None, "Rótulo traduzido do componente de tela."), P("helpText", S, None, "Texto de ajuda traduzido do componente."),
        P("inputParameters", "FlowInputParameterTranslation", None, RESERVADO),
        P("name", S, None, "Nome de API do componente de tela.", "S"),
        P("validationRule", "FlowInputValidationRuleTranslation", None, "Tradução da regra de validação do componente.")]),
    "FlowInputParameterTranslation": (RESERVADO, [P("name", S, None, RESERVADO), P("value", "FlowFerovTranslation", None, RESERVADO)]),
    "FlowFerovTranslation": (RESERVADO, [
        P("complexValues", "FlowComplexLiteralTranslation", None, RESERVADO), P("stringValue", S, None, RESERVADO)]),
    "FlowComplexLiteralTranslation": (RESERVADO, [P("customAspectKey", S, None, RESERVADO), P("value", S, None, RESERVADO)]),
    "FlowStageTranslation": ("Tradução de um estágio de uma versão de flow (FlowStage). Desde a API 43.0.", [
        lb("do estágio"), P("name", S, None, "Nome de API do estágio.", "S")]),
    "FlowTextTemplateTranslation": ("Tradução de um text template; vale só para flows do Salesforce Surveys. Desde a API 45.0. "
                                    "Na página, nenhuma tabela traz um campo deste tipo.", [
        P("name", S, None, "Nome único do text template.", "S"), P("text", S, None, "Texto traduzido do template.")]),
    "GlobalPicklistTranslation": ("Tradução de uma global picklist. Existiu só na API 37.0.", [
        nm("da global picklist traduzida"),
        P("picklistValues", "PicklistValueTranslation[]", None, "Valores traduzidos da global picklist.",
          notas=["PicklistValueTranslation não é descrito na página de Translations."])]),
    "GlobalQuickActionTranslation": ("Tradução global (não ligada a um objeto) de uma quick action (QuickAction).", [
        P("aspect", S, "53.0", "Indica a que texto a tradução se aplica: Master ou InfoMessage."),
        P("label", S, None, "Nome traduzido da quick action, usado globalmente.", "S"), nm("da quick action")]),
    "IdentityVerificationFieldTranslation": ("Tradução dos componentes de interface ligados aos campos de verificação de identidade. "
                                             "Desde a API 54.0.", [
        P("customFieldLabel", S, None, "Rótulo customizado do campo que guarda os dados de verificação."),
        P("description", S, None, "Descrição do campo de verificação de identidade."), P("label", S, None, "Nome amigável deste tipo de tradução."),
        nm("do campo de verificação de identidade")]),
    "PipelineInspMetricConfigTranslation": ("Tradução das configurações de métricas de categoria de previsão do Pipeline Inspection. "
                                            "Desde a API 57.0.", [
        P("label", S, None, "Nome traduzido da configuração de métrica.", "S"), nm("da configuração de métrica")]),
    "ProductSpecificationTypeTranslation": ("Tradução de um product specification type. Desde a API 66.0.", [
        ds("do product specification type"), P("label", S, None, "Nome traduzido do product specification type."),
        nm("do product specification type")]),
    "PromptTranslation": ("Tradução de um prompt do In-App Guidance. Desde a API 48.0.", [
        P("description", S, None, "Descrição do prompt."), P("label", S, None, "Nome traduzido do prompt."), nm("do prompt"),
        P("promptVersions", "PromptVersionTranslation", None, "Traduções das versões do prompt.")]),
    "PromptVersionTranslation": ("Tradução de uma versão de prompt do In-App Guidance. Desde a API 48.0.", [
        P("actionButtonLabel", S, None, "Rótulo do botão de ação do prompt."), P("actionButtonLink", S, None, "URL do botão de ação do prompt."),
        P("body", S, None, "Texto do corpo do prompt."), P("description", S, None, "Descrição do prompt."),
        P("dismissButtonLabel", S, None, "Rótulo do botão de dispensar do prompt flutuante."),
        P("header", S, None, "Cabeçalho do prompt ancorado (docked)."),
        P("imageAltText", S, "53.0", "Texto alternativo da imagem do prompt."), P("imageLink", S, "53.0", "URL da imagem do prompt."),
        P("label", S, None, "Nome traduzido do prompt."), nm("do prompt"), P("title", S, None, "Título do prompt."),
        P("videoLink", S, None, "URL do vídeo do prompt ancorado (docked).")]),
    "RecordAlertCategoryTranslation": ("Tradução de uma categoria de record alert. Desde a API 66.0.", [
        ds("da categoria de record alert"), lb("da categoria de record alert", "S"), nm("da categoria de record alert")]),
    "RecordAlertTemplateTranslation": ("Tradução de um template de record alert. Desde a API 66.0.", [
        ds("do template de record alert"), lb("do template de record alert"), nm("do template de record alert"),
        P("subject", S, None, "Assunto traduzido do template de record alert.")]),
    "ReportAggregateTranslation": (f"Tradução de um agregado de relatório {LEX} (ReportAggregate).", [
        P("label", S, None, "Rótulo do agregado."), nm("do agregado"), P("reportName", S, None, "Nome do relatório a que o agregado pertence.", "S")]),
    "ReportBucketFieldTranslation": (f"Tradução de um bucket field de relatório {LEX} (ReportBucketField).", [
        P("label", S, None, "Rótulo do bucket field."), nm("do bucket field"),
        P("reportName", S, None, "Nome do relatório a que o bucket field pertence.", "S")]),
    "ReportChartTranslation": (f"Tradução de um gráfico de relatório {LEX} (ReportChart).", [
        P("label", S, None, "Rótulo do gráfico."), nm("do gráfico"), P("reportName", S, None, "Nome do relatório a que o gráfico pertence.", "S")]),
    "ReportTranslation": (f"Tradução de um relatório {LEX} (Report).", [
        P("description", S, None, "Descrição do relatório."), P("label", S, None, "Rótulo do relatório."), nm("do relatório")]),
    "ReportTypeTranslation": (f"Tradução de um report type customizado {LEX} (ReportType).", [
        ds("do report type"), P("label", S, None, "Nome traduzido do report type."), nm("do report type"),
        P("sections", "ReportTypeSectionTranslation[]", None, "Traduções das seções do report type.")]),
    "ReportTypeSectionTranslation": (f"Tradução de uma seção de report type {LEX}.", [
        P("columns", "ReportTypeColumnTranslation[]", None, "Traduções das colunas da seção."),
        P("label", S, None, "Nome traduzido da seção do report type."), nm("da seção do report type")]),
    "ReportTypeColumnTranslation": (f"Tradução de uma coluna de report type {LEX}.", [
        P("label", S, None, "Nome traduzido da coluna do report type.", "S"), nm("da coluna traduzida")]),
    "ScontrolTranslation": ("Tradução de um s-control, recurso legado que a página diz ter sido substituído por Visualforce.", [
        P("label", S, None, "Nome traduzido do s-control.", "S"), nm("do s-control")]),
    "ServiceProcessAttributeTranslation": ("Tradução de um atributo de service process. Desde a API 64.0.", [
        lb("do atributo do service process", "S"), nm("do atributo do service process"),
        P("serviceProcessName", S, None, "Nome do service process pai.", "S")]),
    "ServiceProcessItemGroupTranslation": ("Tradução de um grupo de itens de service process. Desde a API 64.0.", [
        P("groupName", S, None, "Nome do grupo de itens do service process.", "S"), nm("da tradução do grupo de itens"),
        P("serviceProcessName", S, None, "Nome do service process pai.", "S")]),
    "TimelineObjectDefinitionTranslation": ("Tradução de uma timeline object definition. Desde a API 66.0.", [
        lb("da timeline object definition"), nm("da timeline object definition")]),
}
assert len(TR) == 59, len(TR)

L = lambda nome, tipo, desde, desc, req="N", **kw: P(nome, tipo, desde, desc, req, **kw)  # noqa: E731
TOPO = [
    L("aiCoachAgentScnrDefs", "AiCoachAgentScnrDefTranslation[]", "64.0", "Traduções de cenários do Agentforce Sales Coach."),
    L("botBlocks", "BotBlockTranslation[]", "59.0", "Traduções de bot blocks."),
    L("botTemplates", "BotTemplateTranslation[]", "59.0", "Traduções de templates de bot."),
    L("bots", "BotTranslation[]", "53.0", "Traduções de bots."),
    L("conversationMessageDefinitions", "ConversationMessageDefinitionTranslation[]", "61.0", "Traduções de conversation message definitions."),
    L("contextDefinitions", "ContextDefinitionTranslation[]", "62.0", "Traduções de context definitions do Context Service."),
    L("customApplications", "CustomApplicationTranslation[]", None, "Traduções de apps customizados."),
    L("customLabels", "CustomLabelTranslation[]", None, "Traduções de custom labels."),
    L("customPageWebLinks", "CustomPageWebLinkTranslation[]", None, "Traduções de web links de componentes da home page."),
    L("customTabs", "CustomTabTranslation[]", None, "Traduções de abas customizadas."),
    L("dataConnectors", "DataConnectorTranslation[]", "64.0", "Traduções de data connectors."),
    L("dashboardComponents", "DashboardComponentTranslation[]", "67.0", "Traduções de componentes de dashboard."),
    L("dashboards", "DashboardTranslation[]", "67.0", "Traduções de título e descrição de dashboards.",
      notas=["A página diz que estas traduções são descobertas automaticamente (auto-discoverable)."]),
    L("desFieldTemplateMessages", "ExplainabilityMsgTemplateFieldTranslation[]", None,
      "Traduções dos templates de mensagem de explicação configurados pelo administrador."),
    L("flowDefinitions", "FlowDefinitionTranslation[]", "41.0", "Traduções de flows. Só para os tipos Flow e AutolaunchedFlow."),
    L("identityVerificationCustomFieldLabels", "IdentityVerificationFieldTranslation", "54.0", "Traduções dos campos de verificação de identidade."),
    L("fullName", S, None, "Código do idioma da tradução, como de para alemão. Herdado do tipo Metadata; deve ser informado ao criar, "
      "atualizar ou excluir.", "S", herdada="Metadata"),
    L("globalPicklists", "GlobalPicklistTranslation[]", "37.0", "Traduções de global picklists.", ate="37.0",
      notas=["A página informa que o campo existiu só na API 37.0 e foi removido nas versões seguintes."]),
    L("pipelineInspMetricConfigs", "PipelineInspMetricConfigTranslation", "57.0",
      "Traduções das configurações de métricas de categoria de previsão do Pipeline Inspection."),
    L("productSpecificationTypes", "ProductSpecificationTypeTranslation", "66.0", "Traduções de product specification types."),
    L("prompts", "PromptTranslation", "48.0", "Traduções de prompts do In-App Guidance."),
    L("quickActions", "GlobalQuickActionTranslation[]", None, "Traduções de quick actions globais (não ligadas a um objeto)."),
    L("recordAlertCategories", "RecordAlertCategoryTranslation[]", "66.0", "Traduções de categorias de record alert."),
    L("recordAlertTemplates", "RecordAlertTemplateTranslation[]", "66.0", "Traduções de templates de record alert."),
    L("reportAggregates", "ReportAggregateTranslation[]", "68.0", f"Traduções de agregados de relatórios {LEX}."),
    L("reportBucketFields", "ReportBucketFieldTranslation[]", "68.0", f"Traduções de bucket fields de relatórios {LEX}."),
    L("reportCharts", "ReportChartTranslation[]", "68.0", f"Traduções de gráficos de relatórios {LEX}."),
    L("reports", "ReportTranslation[]", "67.0", "Traduções de nomes de relatórios.",
      notas=["A página diz que estas traduções são descobertas automaticamente (auto-discoverable)."]),
    L("reportTypes", "ReportTypeTranslation[]", None, f"Traduções de report types {LEX}."),
    L("scontrols", "ScontrolTranslation[]", None, "Traduções de s-controls."),
    L("svcCatalogItemAttributes", "ServiceProcessAttributeTranslation[]", "64.0", "Traduções de atributos de itens do service catalog."),
    L("svcCatalogItemGroups", "ServiceProcessItemGroupTranslation[]", "64.0", "Traduções de grupos de itens do service catalog."),
    L("timelineObjectDefinitions", "TimelineObjectDefinitionTranslation[]", "66.0", "Traduções de timeline object definitions."),
]
assert len(TOPO) == 33, len(TOPO)

# Quem usa cada subtipo: calculado a partir dos tipos das linhas, para não repetir a informação à mão.
usos = {n: set() for n in TR}
for dono, linhas in [("mdt:Translations", TOPO)] + [("mdx:" + n, r) for n, (_, r) in TR.items()]:
    for linha in linhas:
        base = linha[1].replace("[]", "")
        if base in usos and dono != "mdx:" + base:
            usos[base].add(dono)
SEM_USO = sorted(n for n, u in usos.items() if not u)
assert SEM_USO == ["FlowTextTemplateTranslation"], SEM_USO
for n, (o_que_e, linhas) in TR.items():
    if n not in SEM_USO:   # o validador recusa estrutura que nenhuma propriedade usa; o subtipo fica só na nota de extração
        M.struct(n, S_TR, sorted(usos[n]), linhas, o_que_e)

M.mdt("Translations", S_TR,
      "As traduções de um idioma para componentes que não são de um objeto específico: apps, abas, custom labels, flows, relatórios, bots e outros.",
      "Versionar e implantar as traduções feitas no Translation Workbench, um arquivo por idioma.", "14.0", TOPO,
      exemplo=CAB + f"""<!-- Arquivo nomeado pelo código do idioma, por exemplo de.translation -->
<Translations {NS}>
    <customApplications>
        <label>[nome traduzido do app]</label>
        <name>[Nome_Do_App]</name>
    </customApplications>
    <customLabels>
        <label>[texto traduzido do label]</label>
        <name>[Nome_Do_Label]</name>
    </customLabels>
</Translations>""", curinga=True, completa=False,
      alertas=["Ao recuperar, só vêm as traduções dos metadata types listados no package.xml: liste, por exemplo, CustomLabels junto de Translations.",
               "As traduções de objetos customizados não ficam aqui: ficam na pasta objectTranslations (tipo CustomObjectTranslation, não cadastrado).",
               "Em pacote gerenciado, o nome do arquivo leva o namespace e dois sublinhados antes do código do idioma."],
      cobertura_nota=NOTA_COB + " Primeiro nível: 33 de 33 campos. Dos 59 subtipos descritos na página, 58 estão cadastrados como "
                     "estruturas; FlowTextTemplateTranslation ficou fora, porque nenhum campo da página o usa. Parcial: PicklistValueTranslation, usado "
                     "por GlobalPicklistTranslation (campo que só existiu na API 37.0), não é descrito na página.")

M.emit_structs()

d = ld("estruturas/FilterItem.json")
d["usada_por"] = sorted(set(d["usada_por"]) | {"mdt:WorkflowRule"})
sv("estruturas/FilterItem.json", d)

# ================================================================ ligação com as funcionalidades
C.ampliar_funcionalidade("casos", mdts=[("CaseSettings", "Configurações gerais de casos: dono padrão, notificações, Email-to-Case e Web-to-Case.")],
                         srcs=[S_CASE], remover_ausencia_de="metadata_type")
C.ampliar_funcionalidade("workflow-rules-e-process-builder", mdts=[
    ("Workflow", "Arquivo por objeto que reúne as regras de workflow e suas ações."),
    ("WorkflowRule", "Cada regra de workflow: critério, momento de avaliação e ações."),
    ("WorkflowFieldUpdate", "Ação que atualiza um campo."),
    ("WorkflowAlert", "Ação que envia um alerta de e-mail."),
    ("WorkflowTask", "Ação que cria uma tarefa."),
    ("WorkflowOutboundMessage", "Ação que envia uma mensagem SOAP a um endpoint externo."),
    ("WorkflowFlowAction", "Ação que inicia um flow (flow trigger; piloto encerrado)."),
    ("WorkflowKnowledgePublish", "Ação que publica artigos do Knowledge.")], srcs=[S_WF], remover_ausencia_de="metadata_type")
C.ampliar_funcionalidade("translation-workbench", mdts=[("Translations", "Arquivo por idioma com as traduções feitas no Translation Workbench.")],
                         srcs=[S_TR])
C.ampliar_funcionalidade("custom-labels", mdts=[("Translations", "Guarda as traduções dos custom labels (customLabels), um arquivo por idioma.")],
                         srcs=[S_TR])

# ================================================================ conferência dos tipos cadastrados pela referência nova
NOTA_EXTRA = ("Consta da referência nova da documentação, sem descrição, e não consta do guia versionado 264.0 (API 68.0), conferido em "
              "2026-11-16. A disponibilidade na API 68.0 não está confirmada.")
NOTA_DISP = "Campo ausente do guia versionado 264.0 (API 68.0); versão de entrada não informada na fonte."


def conferir(pasta, nome, extras, src, divergencia, grafia=None):
    """Marca, num tipo ou estrutura já cadastrado, os campos que só constam da referência nova. Não remove nada."""
    d = ld(f"{pasta}/{nome}.json")
    achados = set()
    for p in d["propriedades"]:
        if p["nome"] in extras:
            achados.add(p["nome"])
            p["notas"] = [n for n in p.get("notas", []) if n != NOTA_EXTRA] + [NOTA_EXTRA]
            p["disponibilidade"] = {"desde_versao": None, "ate_versao": None, "estado": "desconhecido", "nota": NOTA_DISP}
    faltou = set(extras) - achados
    assert not faltou, (nome, faltou)
    if not any(e["fonte"] == src for e in d["evidencias"]):
        d["evidencias"].append(ev(src, "Lista de campos conferida no guia versionado 264.0."))
    if pasta == "metadata-types":
        for t in [divergencia] + ([grafia] if grafia else []):
            if t not in d["divergencias_documentais"]:
                d["divergencias_documentais"].append(t)
        marca = " Conferência com o guia versionado 264.0:"
        nota = d["cobertura"]["estrutural"]["nota"].split(marca)[0]
        if extras:
            nota += f"{marca} {len(extras)} campo(s) só constam da referência nova e estão marcados como não confirmados na API 68.0."
        d["cobertura"]["estrutural"]["nota"] = nota
    sv(f"{pasta}/{nome}.json", d)
    return len(achados)


def div(nome, total, extras):
    return (f"O guia versionado 264.0 (API 68.0) lista {total} campo(s) em {nome}; a referência nova, usada neste cadastro, lista "
            f"{len(extras)} a mais, todos sem descrição: {', '.join(sorted(extras))}.")


EXTRAS = {
    "FieldServiceSettings": (40, ["advancedDataSyncOrgPreference", "doesAvlCalcInclOvertime", "doesAvlCalcInclPrimOnly", "enableAdvancedDataSync",
                                  "enableBatchWindow", "enableDataCaptureControlByParent", "enableFieldServiceNotifications",
                                  "enableGeolocationBasedActionControlByParent", "enableServiceAppointmentLifecycle",
                                  "enableWorkStepsHideNotApplicable", "enrouteStatus", "useBundler", "useLicenselessPermset", "useWorkCapacity"]),
    "MyDomainSettings": (28, ["enableShareBrowserSessionAndroidForAuth", "enableShareBrowserSessionIOSForAuth", "isInstancedApiTrafficBlocked"]),
    "ContractSettings": (2, ["autoExpirationDelay", "autoExpirationRecipient", "autoExpireContracts", "enableContractHistoryTracking"]),
    "CommunitiesSettings": (22, ["enableGuestPermDisOptOutCruc", "enableGuestSecurityOptOutCruc", "enableNameFieldsUserPIIEnabled"]),
    "FlowSettings": (26, ["enableEmailSimpleRespectProfiles", "enableEmailsimpleSecureProfiles", "enableFlowReactiveChoiceOptions",
                          "flowOccurrenceLogging", "isSupportRollbackOnErrorForApexInvocableActionsEnabled"]),
    "ApprovalProcess": (20, ["processOrder"]),
}
marcados = 0
for nome, (total, extras) in EXTRAS.items():
    marcados += conferir("metadata-types", nome, extras, f"src:mdapi-v68-{nome.lower()}", div(nome, total, extras))

RULE_ENTRY = ["assignedTo", "assignedToType", "businessHours", "businessHoursSource", "disableEscalationWhenModified", "escalationAction",
              "escalationStartTime", "notifyCcRecipients", "overrideExistingTeams", "team"]
S_ARR68 = "src:mdapi-v68-autoresponserules"
marcados += conferir("estruturas", "AutoResponseRules_RuleEntry", RULE_ENTRY, S_ARR68, None)
conferir("metadata-types", "AutoResponseRules", [], S_ARR68,
         "No guia versionado 264.0 (API 68.0), o RuleEntry de AutoResponseRules tem 7 campos; a referência nova, usada neste cadastro, lista 10 a mais, "
         f"todos sem descrição e próprios de outros tipos de regra: {', '.join(RULE_ENTRY)}.",
         grafia="O guia versionado 264.0 grafa autoresponseRule e fullname (em minúsculas); a referência nova, usada neste cadastro, grafa "
                "autoResponseRule e fullName. A grafia não foi conferida no WSDL.")

# ApprovalProcess.allowedSubmitters: o guia versionado marca o campo como Required.
d = ld("metadata-types/ApprovalProcess.json")
for p in d["propriedades"]:
    if p["nome"] == "allowedSubmitters":
        p["obrigatoriedade"] = {"valor": "sim", "estado": "verificado", "evidencias": [ev("src:mdapi-v68-approvalprocess")]}
        p["notas"] = ["O guia versionado 264.0 marca o campo como Required. Na referência nova, a tabela não marca, mas a descrição diz que é obrigatório."]
velha = "Na página (src:mdapi-approvalprocess), allowedSubmitters aparece como não obrigatório na tabela, mas a descrição diz que é obrigatório."
d["divergencias_documentais"] = [x for x in d["divergencias_documentais"] if x != velha]
nova = ("allowedSubmitters: a tabela da referência nova não marca o campo como obrigatório, embora a descrição diga que é; o guia versionado 264.0 "
        "marca como Required. O cadastro segue o guia versionado.")
if nova not in d["divergencias_documentais"]:
    d["divergencias_documentais"].append(nova)
sv("metadata-types/ApprovalProcess.json", d)

print(f"lote 7a: 10 metadata types (CaseSettings, Workflow + 7 filhos, Translations) e {8 + len(TR) - len(SEM_USO)} estruturas gravados; "
      f"4 funcionalidades ligadas; {marcados} campos marcados como não confirmados na API 68.0")
