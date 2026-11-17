"""Lote 7n (rodada B5, parte A; issues #8 e #34): completar a estrutura dos metadata types já cadastrados.

Fecha os tipos compostos e as enumerações que estavam sem detalhe em Profile, CustomObject, CustomField, RecordType, BusinessProcess,
CustomTab, QuickAction, FlexiPage, GenAiPlugin, Network, Layout, AutoResponseRules, DuplicateRule, EntitlementProcess, Translations,
PresenceUserConfig, ListView, ReportFolder e DashboardFolder.

Fontes novas: páginas do guia versionado 264.0 que antes vieram ilegíveis e agora abriram por outro endereço (customfield.htm,
namedfilter.htm) ou foram lidas por partes; o novo site da referência da Metadata API (ActionOverride, SharingReason,
SharingRecalculation, CustomTab), que mostra "API version 68.0"; e a página FieldDefinition da Tooling API, que traz a tabela do
tipo PicklistValue. Flow fica para a parte B (lote 7o).

Ordem: lote7m_b4_acesso_temas.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7n_b5_estruturas.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga.base import af, ev, ld, sv, caminho  # noqa: E402
from carga import catalogo as C               # noqa: E402
from carga import ligacao as LG               # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7n-b5-estruturas.txt"
OLD = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
NEW = "https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/"


def substituir_fontes(novas):
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


FONTES = [  # id, título, url, pertinência
    ("src:mdapi-customfield-v264", "CustomField, releitura (Metadata API)", OLD + "customfield.htm", "Lista dos 60 campos, subtipos Mkt*, LookupFilter e FilterItem."),
    ("src:mdapi-namedfilter", "NamedFilter (Metadata API)", OLD + "namedfilter.htm", "Campos de NamedFilter, removido na API 30.0."),
    ("src:mdapi-flexipage-subtipos", "FlexiPage, subtipos (Metadata API)", OLD + "meta_flexipage.htm", "Subtipos de FlexiPage e valores de FlexiPageType."),
    ("src:mdapi-quickaction-subtipos", "QuickAction, subtipos (Metadata API)", OLD + "meta_quickaction.htm", "Subtipos de QuickAction e valores de QuickActionLabel."),
    ("src:mdapi-genaiplugininstructiondef", "GenAiPluginInstructionDef (Metadata API)", OLD + "meta_genaiplugininstructiondef.htm", "Campos de GenAiPluginInstructionDef."),
    ("src:mdapi-aipluginutterancedef", "AiPluginUtteranceDef (Metadata API)", OLD + "meta_aipluginutterancedef.htm", "Campos de AiPluginUtteranceDef."),
    ("src:mdapi-layouts-enums", "Layouts, enumerações (Metadata API)", OLD + "meta_layouts.htm", "Valores de FeedItemType e SummaryLayoutStyle."),
    ("src:mdapi-escalationrules-enums", "EscalationRules, enumerações (Metadata API)", OLD + "meta_escalationrules.htm", "Valores das enumerações de RuleEntry."),
    ("src:mdapi-network-subtipos", "Network, subtipos (Metadata API)", OLD + "meta_network.htm", "Subtipos de Network lidos de 55 mil caracteres até o fim."),
    ("src:mdapi-presenceuserconfig-v264", "PresenceUserConfig, releitura (Metadata API)", OLD + "meta_presenceuserconfig.htm", "Contagem da tabela e linha vazia."),
    ("src:mdapi-customobjecttranslation-v264", "CustomObjectTranslation, PicklistValueTranslation (Metadata API)", OLD + "meta_customobjecttranslation.htm",
     "Campos de PicklistValueTranslation."),
    ("src:mdapi-profile-parte1", "Profile, primeira parte da página (Metadata API)", OLD + "meta_profile.htm",
     "LoginFlow, ProfileActionOverride, ProfileAgentAccess e ProfileLoginHours, nos primeiros 100 mil caracteres."),
    ("src:mdapi-actionoverride", "ActionOverride (Metadata API, novo site)", NEW + "metadata-actionoverride.html", "Campos de ActionOverride."),
    ("src:mdapi-sharingreason", "SharingReason (Metadata API, novo site)", NEW + "metadata-sharingreason.html", "Campos de SharingReason."),
    ("src:mdapi-sharingrecalculation", "SharingRecalculation (Metadata API, novo site)", NEW + "metadata-sharingrecalculation.html", "Campo de SharingRecalculation."),
    ("src:mdapi-customtab-novo", "CustomTab (Metadata API, novo site)", NEW + "metadata-customtab.html", "Os 100 valores de motif."),
    ("src:mdapi-profile-novo", "Profile (Metadata API, novo site)", NEW + "metadata-profile.html", "Valores de TabVisibility."),
    ("src:tooling-fielddefinition-picklistvalue", "FieldDefinition, seção PicklistValue Metadata (Tooling API)",
     "https://developer.salesforce.com/docs/platform/api-tooling/references/tooling-objects/tooling-fielddefinition.html", "Tabela do tipo PicklistValue."),
]
substituir_fontes([C.fonte(i, t, u, p, EXTR, DATA) for i, t, u, p in FONTES])
(S_CF, S_NF, S_FP, S_QA, S_GPI, S_APU, S_LAY, S_ESC, S_NET, S_PUC, S_COT, S_PR1, S_AO, S_SRS, S_SRC, S_CTN, S_PRN, S_PV) = (f[0] for f in FONTES)

B, S, I = "boolean", "string", "int"
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
REG = []


def valores(*vs):
    return [(v, None) for v in vs]


def estrutura(nome, src, usada_por, rows, o_que_e):
    M.struct(nome, src, usada_por, rows, o_que_e)
    REG.append((src, "estruturas", nome))


AOT = valores("default", "flexipage", "lightningcomponent", "scontrol", "standard", "visualforce")
ACOES = valores("accept", "clone", "delete", "edit", "list", "new", "tab", "view")
FF = [("Large", "Lightning Experience no desktop."), ("Small", "App móvel do Salesforce."), ("Medium", "Reservado para uso futuro.")]

# ================================================================ PicklistValue (metadata type, sem suporte no Salesforce CLI)
PV_ARQ = {"source_format": af("desconhecido", None, "O Salesforce CLI não suporta este tipo (METADATA_SUPPORT.md); não há pasta nem sufixo no registro.",
                              [ev("src:sdr-metadata-support")]),
          "metadata_api_format": af("desconhecido", None, "Os valores aparecem dentro de outros componentes (Picklist de CustomField, RecordType, "
                                    "BusinessProcess); a seção lida não descreve arquivo próprio.", [ev(S_PV)])}
M.mdt("PicklistValue", S_PV,
      "Um valor de picklist com as marcas especiais que alguns campos padrão usam: fase de oportunidade ganha, status de caso fechado, status "
      "de lead convertido, probabilidade, categoria de previsão e outras.",
      "Descrever os valores de picklist dentro de Picklist (até a API 37.0), RecordType e BusinessProcess.", None, [
          P("allowEmail", B, "18.0", "Só para Status de cotação: permite enviar o PDF da cotação por e-mail."),
          P("closed", B, "16.0", "Marca o status de caso ou de tarefa como fechado."),
          P("color", S, "17.0", "Cor em hexadecimal usada em gráficos; atribuída automaticamente se omitida."),
          P("controllingFieldValues", "string[]", "14.0", "Valores do campo controlador de que este valor depende: checked/unchecked para "
                                                          "checkbox ou o fullName do valor no picklist controlador."),
          P("converted", B, "16.0", "Marca o status de lead como convertido."),
          P("cssExposed", B, "16.0", "Mostra o valor no portal de autoatendimento (Case Reason)."),
          P("default", B, None, "Marca o valor padrão do picklist.", "S"),
          P("description", S, "16.0", "Por que o valor customizado existe (campo Stage)."),
          P("forecastCategory", "ForecastCategories", "16.0", "Categoria de previsão de uma fase de oportunidade.",
            vals=valores("Omitted", "Pipeline", "BestCase", "Forecast", "Closed")),
          M.FULLNAME_HERDADO(None, "Nome de API do valor; herdado do tipo Metadata."),
          P("highPriority", B, "16.0", "Marca a prioridade de tarefa como alta."),
          P("probability", I, "16.0", "Probabilidade de ganho de uma fase de oportunidade.",
            notas=["A página fala em true ou false aqui, o que não combina com o tipo int."]),
          P("reverseRole", S, "18.0", "Papel inverso de um parceiro, como contratante para subcontratado."),
          P("reviewed", B, "16.0", "Marca o status de solução como revisado."),
          P("won", B, "16.0", "Marca a fase de oportunidade como ganha."),
      ], exemplo=CAB + f"""<PicklistValue {NS}>
    <fullName>Closed Won</fullName>
    <default>false</default>
    <closed>true</closed>
    <forecastCategory>Closed</forecastCategory>
    <probability>100</probability>
    <won>true</won>
</PicklistValue>""", arquivos_prontos=PV_ARQ, curinga=None,
      alertas=["A tabela foi lida na página FieldDefinition da Tooling API, que reproduz o tipo; a página própria do guia (meta_picklistvalue) "
               "devolveu conteúdo ilegível.", "Desde a API 38.0, os picklists de campos customizados usam valueSet; PicklistValue continua em "
                                                 "RecordType e BusinessProcess."],
      cobertura_nota="Universo esperado = tabela PicklistValue Metadata da página FieldDefinition da Tooling API, lida em 2026-11-17 (15 campos).")
REG.append((S_PV, "metadata-types", "PicklistValue"))

# ================================================================ SharingReason (filho de CustomObject)
M.mdt("SharingReason", S_SRS,
      "Um motivo de compartilhamento Apex: o rótulo que diz por que um registro foi compartilhado por código (Apex managed sharing).",
      "Versionar e implantar os motivos de compartilhamento junto com o objeto.", "14.0", [
          P("fullName", S, None, "Nome do motivo; os customizados recebem __c. Precisa ser informado para criar, alterar ou excluir.", herdada="Metadata",
            notas=["Nomes reservados (Manual, Team, Sharing Rule, Record Collection) não são aceitos; até 10 motivos customizados por objeto padrão."]),
          P("label", S, None, "Rótulo do motivo; até 40 caracteres.", "S"),
      ], parent="CustomObject", exemplo=CAB + f"""<!-- No arquivo do objeto, este conteúdo fica no elemento <sharingReasons> -->
<SharingReason {NS}>
    <fullName>[Motivo__c]</fullName>
    <label>[Rótulo do motivo]</label>
</SharingReason>""", arquivos_prontos=M.arquivos("SharingReason", "CustomObject"), curinga=None,
      alertas=["Motivos em objetos padrão só existem a partir da API 68.0; em objetos customizados, desde a 14.0."],
      cobertura_nota="Universo esperado = tabela Fields da página do novo site da referência (API 68.0), lida em 2026-11-17 (2 campos).")
REG.append((S_SRS, "metadata-types", "SharingReason"))

# ================================================================ estruturas novas
estrutura("ActionOverride", S_AO, ["mdt:CustomObject", "mdt:CustomTab"], [
    P("actionName", S, None, "Ação padrão que é substituída.", vals=ACOES, notas=["A descrição diz Required, mas a marcação do campo diz que não."]),
    P("comment", S, None, "Comentário livre sobre a substituição."),
    P("content", S, None, "Nome da página Lightning, componente, s-control ou página Visualforce usada; componentes instalados usam Namespace__Nome."),
    P("formFactor", "FormFactor", "37.0", "Tamanho de página a que a substituição se aplica; nulo vale para o Classic.", vals=FF),
    P("skipRecordTypeSelect", B, "21.0", "Pula a tela de escolha de record type ao criar registro."),
    P("type", "ActionOverrideType", None, "Que tipo de substituição é usado.", vals=AOT, notas=["A descrição diz Required, mas a marcação do campo diz que não."]),
], "Uma substituição de ação padrão (nova, editar, ver, lista e outras) por uma página ou componente, num objeto ou numa aba.")
estrutura("SharingRecalculation", S_SRC, ["mdt:CustomObject"], [
    P("className", S, "14.0", "Classe Apex que recalcula o compartilhamento Apex do objeto; precisa implementar Database.Batchable.", "S"),
], "A classe Apex que recalcula o compartilhamento gerido por Apex de um objeto customizado.")
estrutura("NamedFilter", S_NF, ["mdt:CustomObject"], [
    P("active", B, "17.0", "Liga ou desliga o filtro de lookup.", "S", ate="29.0"),
    P("booleanFilter", S, "17.0", "Lógica avançada que combina as condições.", ate="29.0"),
    P("description", S, "17.0", "Para que serve o filtro.", ate="29.0"),
    P("errorMessage", S, "17.0", "Mensagem quando o filtro recusa um valor.", ate="29.0"),
    P("field", S, "17.0", "Nome completo do campo ligado ao filtro.", "S", ate="29.0"),
    P("filterItems", "FilterItem[]", "17.0", "As condições do filtro.", "S", estrutura="FilterItem", ate="29.0",
      notas=["A página grafa o tipo como FilterItems[]."]),
    P("fullName", S, "17.0", "Identificador exigido para criar, alterar e excluir.", "S", ate="29.0", herdada="Metadata"),
    P("infoMessage", S, "17.0", "Aviso que explica por que itens ficaram de fora.", ate="29.0"),
    P("isOptional", B, "17.0", "Indica se o filtro pode ser ignorado.", "S", ate="29.0"),
    P("name", S, "17.0", "Rótulo do filtro; atribuído pela interface.", "S", ate="29.0"),
    P("sourceObject", S, "17.0", "Objeto do campo de lookup, quando o filtro usa campos dele.", ate="29.0"),
], "Um filtro de lookup no formato antigo, até a API 29.0. Removido na 30.0: o filtro passou a ficar em lookupFilter do CustomField.")

# Profile
estrutura("LoginFlow", S_PR1, ["mdt:Profile"], [
    P("flow", S, None, "Flow usado; precisa estar ativo.", "C:Quando uiLoginFlowType é VisualWorkflow."),
    P("flowtype", "LoginFlowType", None, "Tipo do login flow.", "S", vals=valores("UI")),
    P("friendlyname", S, None, "Nome do login flow.", "S"),
    P("uiLoginFlowType", "UiLoginFlowType", None, "Se o login flow é um flow ou uma página Visualforce.", "S", vals=valores("VisualWorkflow", "VisualForce")),
    P("useLightningRuntime", B, None, "Usa o runtime do Lightning; só com VisualWorkflow.", default=("false", False, "A página declara default false.")),
    P("vfFlowPage", S, None, "Página Visualforce usada.", "C:Quando uiLoginFlowType é VisualForce."),
    P("vfFlowPageTitle", S, None, "Título da página Visualforce.", "C:Quando uiLoginFlowType é VisualForce.",
      notas=["A descrição na página repete a de vfFlowPage."]),
], "O login flow ligado ao perfil: um flow ou uma página Visualforce que roda no login.")
estrutura("ProfileActionOverride", S_PR1, ["mdt:Profile"], [
    P("actionName", S, None, "Ação substituída.", "S", vals=ACOES),
    P("content", S, None, "Nome da página ou componente usado.", "C:Quando type é flexipage, lightningcomponent, scontrol ou visualforce."),
    P("formFactor", "FormFactor", None, "Tamanho de página; nulo vale para o Classic.", vals=FF),
    P("pageOrSobjectType", S, None, "Objeto ou página; standard-home quando actionName é tab."),
    P("recordType", S, None, "Record type a que a substituição se aplica; nulo com standard-home."),
    P("type", "ActionOverrideType", None, "Tipo de substituição.", "S", vals=AOT, notas=["Valores conforme a página de ActionOverride."]),
], "Uma substituição de ação por perfil, como a página inicial do Lightning Experience. A propriedade do perfil existe da API 37.0 à 44.0.")
estrutura("ProfileAgentAccess", S_PR1, ["mdt:Profile"], [
    P("agentName", S, None, "Nome do agente.", "S"),
    P("enabled", B, None, "Indica se os usuários do perfil podem usar o agente.", "S"),
], "O acesso do perfil a um agente de funcionário do Agentforce (API 63.0 ou posterior).")
DIAS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
estrutura("ProfileLoginHours", S_PR1, ["mdt:Profile"],
          [P(f"{d_}{k}", S, None, f"{'Início' if k == 'Start' else 'Fim'} do horário de login em {d_}, em minutos desde a meia-noite, múltiplo de 60.")
           for d_ in DIAS for k in ("Start", "End")],
          "O horário em que os usuários do perfil podem entrar. Quem define o início de um dia precisa definir o fim; para tirar as restrições, "
          "envie loginHours vazio.")

# QuickAction
estrutura("FieldOverride", S_QA, ["mdt:QuickAction"], [
    P("field", S, None, "Campo que recebe o valor predefinido.", "S"),
    P("formula", S, None, "Fórmula que calcula o valor predefinido.", notas=["Em picklists de seleção única, desde a API 43.0."]),
    P("literalValue", S, None, "Valor fixo; só para picklists."),
], "Um valor predefinido de campo numa ação rápida.")
estrutura("QuickActionLayoutItem", S_QA, ["mdx:QuickActionLayoutColumn"], [
    P("emptySpace", B, None, "Marca o item como espaço em branco."),
    P("field", S, None, "Campo mostrado no item."),
    P("uiBehavior", "UiBehavior", None, "Regra de entrada do campo.", vals=valores("Edit", "Required", "Readonly")),
], "Um item de uma coluna do layout de ação rápida.")
estrutura("QuickActionLayoutColumn", S_QA, ["mdx:QuickActionLayout"], [
    P("quickActionLayoutItems", "QuickActionLayoutItem[]", None, "Itens da coluna.", estrutura="QuickActionLayoutItem"),
], "Uma coluna do layout de ação rápida.")
estrutura("QuickActionLayout", S_QA, ["mdt:QuickAction"], [
    P("layoutSectionStyle", "LayoutSectionStyle", None, "Estrutura do layout.", "S",
      vals=valores("TwoColumnsTopToBottom", "TwoColumnsLeftToRight", "OneColumn", "CustomLinks")),
    P("quickActionLayoutColumns", "QuickActionLayoutColumn[]", None, "Colunas do layout.", estrutura="QuickActionLayoutColumn"),
], "O layout dos campos de uma ação rápida.")
estrutura("QuickActionParameter", S_QA, ["mdt:QuickAction"], [
    P("name", S, "63.0", "Nome do parâmetro.", "S"),
    P("type", "QuickActionParameterType", "63.0", "Direção do parâmetro; só Input é aceito.", "S", vals=valores("Input")),
    P("value", S, "63.0", "Valor do parâmetro."),
], "Um parâmetro de entrada de uma ação rápida (API 63.0 ou posterior).")

# FlexiPage
F53 = "53.0"
estrutura("FlexiPageEventSourceProperty", S_FP, ["mdx:FlexiPageEvent"], [
    P("name", S, F53, "Nome da propriedade; só eventName.", "S", vals=valores("eventName")),
    P("value", S, F53, "Nome do evento; com componente LWC, precisa bater com o js-meta.xml.", "S"),
], "Uma propriedade da origem de um evento de página.")
estrutura("FlexiPageEventPropertyMapping", S_FP, ["mdx:FlexiPageEventTarget"], [
    P("name", S, F53, "Propriedade do alvo que muda com o evento.", "S"),
    P("value", S, F53, "Valor aplicado; aceita {!Event.nomeDaPropriedade} em string, inteiro e boolean.", "S"),
], "Uma ligação entre uma propriedade do evento e uma propriedade do alvo.")
estrutura("FlexiPageEventTargetProperty", S_FP, ["mdx:FlexiPageEventTarget"], [
    P("name", S, F53, "Nome da propriedade; só componentIdentifier.", "S", vals=valores("componentIdentifier")),
    P("value", S, F53, "identifier do ComponentInstance alvo.", "S"),
], "Uma propriedade do alvo de um evento de página.")
estrutura("FlexiPageEventTarget", S_FP, ["mdx:FlexiPageEvent"], [
    P("mappings", "FlexiPageEventPropertyMapping[]", F53, "Ligações de propriedades entre origem e alvo.", estrutura="FlexiPageEventPropertyMapping"),
    P("method", S, F53, "Ação do alvo; só updateProperties.", "S", vals=valores("updateProperties")),
    P("name", S, F53, "Nome do alvo.", "S", vals=valores("flexipage:componentService")),
    P("properties", "FlexiPageEventTargetProperty[]", F53, "Propriedades do alvo.", estrutura="FlexiPageEventTargetProperty"),
    P("type", "FlexiPageEventTargetTypeEnum", F53, "Tipo do alvo.", "S", vals=valores("FlexipageServices")),
], "O alvo de um evento de página.")
estrutura("FlexiPageEvent", S_FP, ["mdt:FlexiPage"], [
    P("sourceName", S, F53, "Nome do item de origem (um componente).", "S"),
    P("sourceProperties", "FlexiPageEventSourceProperty[]", F53, "Propriedades da origem.", estrutura="FlexiPageEventSourceProperty"),
    P("sourceType", "FlexipageEventSourceTypeEnum", F53, "Tipo da origem.", "S", vals=valores("Component")),
    P("targets", "FlexiPageEventTarget[]", F53, "Alvos ligados à origem.", estrutura="FlexiPageEventTarget"),
], "Um evento de página: quando um componente dispara um evento, propriedades de outros componentes mudam (API 53.0 ou posterior).")
estrutura("UiFormulaCriterion", S_FP, ["mdx:UiFormulaRule"], [
    P("leftValue", S, "41.0", "Campo ou expressão testada: {!$Client.FormFactor}, {!$Permission...}, {!Record.campo}, {!$User.campo}.", "S",
      notas=["Uma expressão pode atravessar no máximo cinco campos."]),
    P("operator", S, "41.0", "Operador de comparação.", "S", vals=valores("CONTAINS", "EQUAL", "NE", "GT", "GE", "LE", "LT")),
    P("rightValue", S, "41.0", "Valor comparado."),
], "Uma condição de uma regra de visibilidade.")
estrutura("UiFormulaRule", S_FP, ["mdx:ComponentInstance", "mdx:FieldInstance"], [
    P("booleanFilter", S, "41.0", "Lógica que combina as condições, como 1 AND 2."),
    P("criteria", "UiFormulaCriterion[]", "41.0", "As condições.", estrutura="UiFormulaCriterion"),
], "Uma regra de visibilidade: quando o componente ou o campo aparece. Nula, o item aparece sempre.")
estrutura("ComponentInstancePropertyListItem", S_FP, ["mdx:ComponentInstancePropertyList"], [
    P("value", S, "49.0", "Valor de um elemento da lista."),
], "Um elemento de uma lista de valores de propriedade.")
estrutura("ComponentInstancePropertyList", S_FP, ["mdx:ComponentInstanceProperty"], [
    P("valueListItems", "ComponentInstancePropertyListItem[]", "49.0", "Elementos da lista.", estrutura="ComponentInstancePropertyListItem"),
], "Uma lista de valores de propriedade (API 49.0 ou posterior).")
estrutura("ComponentInstanceProperty", S_FP, ["mdx:ComponentInstance", "mdx:FlexiPageTemplateInstance"], [
    P("name", S, None, "Nome da propriedade, único na instância."),
    P("type", "ComponentInstancePropertyTypeEnum", "38.0", "Se a propriedade vale para o decorador; nulo vale para o componente.", vals=valores("decorator"),
      notas=["decorator só é aceito em páginas UtilityBar."]),
    P("value", S, None, "Valor ou referência; até 10.000 caracteres."),
    P("valueList", "ComponentInstancePropertyList", "49.0", "Lista de valores.", estrutura="ComponentInstancePropertyList"),
], "Uma propriedade configurada de um componente na página.")
estrutura("ComponentInstance", S_FP, ["mdx:FlexiPageRegion", "mdx:ItemInstance"], [
    P("componentInstanceProperties", "ComponentInstanceProperty[]", None, "Propriedades configuradas.", estrutura="ComponentInstanceProperty"),
    P("componentName", S, None, "Nome do componente.", "S"),
    P("identifier", S, "53.0", "Identificador único da instância; até 120 caracteres.", "S"),
    P("visibilityRule", "UiFormulaRule", "41.0", "Quando o componente aparece.", estrutura="UiFormulaRule"),
], "Um componente colocado numa região da página.")
estrutura("FieldInstanceProperty", S_FP, ["mdx:FieldInstance"], [
    P("name", S, "49.0", "Nome da propriedade.", vals=[("uiBehavior", "Desde a API 49.0."), ("conditionalFormatRuleset", "Desde a API 62.0.")]),
    P("value", S, "49.0", "Valor; com uiBehavior, None, Readonly ou Required.", notas=["A página não lista valores para conditionalFormatRuleset."]),
], "Uma propriedade de um campo colocado na página (Dynamic Forms).")
estrutura("FieldInstance", S_FP, ["mdx:ItemInstance"], [
    P("fieldInstanceProperties", "FieldInstanceProperty[]", "49.0", "Propriedades do campo.", estrutura="FieldInstanceProperty"),
    P("fieldItem", S, "49.0", "Nome de API do campo, com o contexto na frente, como Record."),
    P("identifier", S, "53.0", "Identificador único; até 120 caracteres.", "S"),
    P("visibilityRule", "UiFormulaRule", "49.0", "Quando o campo aparece.", estrutura="UiFormulaRule"),
], "Um campo colocado numa região (só em páginas com Dynamic Forms).")
estrutura("ItemInstance", S_FP, ["mdx:FlexiPageRegion"], [
    P("componentInstance", "ComponentInstance", "49.0", "Um componente.", estrutura="ComponentInstance"),
    P("fieldInstance", "FieldInstance", "49.0", "Um campo (Dynamic Forms).", estrutura="FieldInstance"),
], "Um item de uma região: um componente ou um campo (API 49.0 ou posterior).")
FLAG = valores("disabled", "enabled")
estrutura("FlexiPageRegion", S_FP, ["mdt:FlexiPage"], [
    P("appendable", "RegionFlagStatus", "35.0", "Se dá para acrescentar itens no fim.", vals=FLAG),
    P("componentInstances", "ComponentInstance[]", None, "Componentes da região; substituído por itemInstances.", estrutura="ComponentInstance", ate="48.0"),
    P("itemInstances", "ItemInstance[]", "49.0", "Componentes e campos da região.", estrutura="ItemInstance"),
    P("mode", "FlexiPageRegionMode", "35.0", "Reservado para uso futuro.", vals=valores("Append", "Prepend", "Replace")),
    P("name", S, None, "Nome único da região.", "S"),
    P("prependable", "RegionFlagStatus", "35.0", "Se dá para acrescentar itens no começo.", vals=FLAG),
    P("replaceable", "RegionFlagStatus", "35.0", "Se dá para substituir itens.", vals=FLAG),
    P("type", "FlexiPageRegionType", "35.0", "Tipo de região.", "S", vals=[("Background", "Só em barras de utilitário."), ("Facet", None), ("Region", None)]),
], "Uma região da página. Com as três marcas em enabled ou ausentes, a região fica destravada; todas em disabled a travam. Até 100 componentes.")
estrutura("FlexiPageTemplateInstance", S_FP, ["mdt:FlexiPage"], [
    P("name", S, None, "Nome do template.", "S"),
    P("properties", "ComponentInstanceProperty[]", None, "Propriedades do template; só em CommThemeLayoutPage e em RecordPage com Dynamic Forms "
                                                          "de conta, caso ou lead.", estrutura="ComponentInstanceProperty"),
], "O template da página.")

# GenAiPlugin
estrutura("AiPluginUtteranceDef", S_APU, ["mdt:GenAiPlugin"], [
    P("developerName", S, None, "Nome de API; letras, números e sublinhado, começando por letra.", "S"),
    P("language", S, None, "Idioma da frase.", "S"),
    P("masterLabel", S, None, "Rótulo da frase.", "S"),
    P("utterance", S, None, "Frase de exemplo usada para escolher o tópico.", "S"),
], "Uma frase de exemplo de um tópico de agente (API 63.0 ou posterior; só com Agents ligado). Estende Metadata e não tem arquivo próprio.")
estrutura("GenAiPluginInstructionDef", S_GPI, ["mdt:GenAiPlugin"], [
    P("description", S, None, "O que a instrução orienta.", "S"),
    P("developerName", S, None, "Nome de API único.", "S"),
    P("language", S, None, "Idioma da instrução.", "S"),
    P("masterLabel", S, None, "Rótulo da instrução.", "S"),
    P("sortOrder", I, None, "Ordem de aplicação da instrução."),
], "Uma instrução de um tópico de agente (API 62.0 ou posterior; só com Agents ligado). Estende Metadata e não tem arquivo próprio.")

# Network
ESTR_NET = "mdt:Network"
estrutura("Branding", S_NET, [ESTR_NET], [P(n, S, None, d_, ate="40.0") for n, d_ in [
    ("loginFooterText", "Texto do rodapé da página de login."), ("loginLogo", "Logo da página de login para usuários externos."),
    ("pageFooter", "Imagem de rodapé das páginas (arquivo HTML)."), ("pageHeader", "Imagem de cabeçalho das páginas."),
    ("primaryColor", "Cor da aba ativa."), ("primaryComplementColor", "Cor de fonte que acompanha primaryColor."),
    ("quaternaryColor", "Cor de fundo da página."), ("quaternaryComplementColor", "Cor de fonte que acompanha quaternaryColor."),
    ("secondaryColor", "Cor da borda superior de listas e tabelas."), ("tertiaryColor", "Fundo dos cabeçalhos das seções de edição e detalhe."),
    ("tertiaryComplementColor", "Cor de fonte que acompanha tertiaryColor."), ("zeronaryColor", "Cor de fundo do cabeçalho."),
    ("zeronaryComplementColor", "Cor de fonte que acompanha zeronaryColor.")]],
    "As cores e imagens antigas do site, até a API 40.0; da 41.0 em diante, substituídas por NetworkBranding.")
estrutura("NavigationLinkSet", S_NET, [ESTR_NET], [
    P("navigationMenuItem", "NavigationMenuItem[]", "37.0", "Itens do menu de navegação.", estrutura="NavigationMenuItem", ate="46.0"),
], "O menu de navegação antigo do site (APIs 37.0 a 46.0); na 47.0, substituído pelo tipo NavigationMenu.")
estrutura("NetworkEmailTmplAllowlist", S_NET, ["mdx:NetworkAuthApiSettings"], [
    P("emailTemplate", S, "60.0", "Modelo de e-mail permitido nos fluxos sem interface.", "S"),
], "Um modelo de e-mail permitido nos fluxos de verificação sem interface (headless).")
H60 = "60.0"
estrutura("NetworkAuthApiSettings", S_NET, [ESTR_NET], [P(n, t, H60, d_, *r, **({"natureza": "referencia", "contexto": "Id de registro de usuário."} if t == "Id" else {}))
                                                        for n, t, d_, *r in [
    ("doesForgotPasswordRequireAuth", B, "Exige token de integração para pedidos de senha esquecida sem interface."),
    ("doesPasswordLoginRequireAuth", B, "Exige reCAPTCHA no login com usuário e senha sem interface."),
    ("doesPwdlessLoginRequireAuth", B, "Exige token de integração no login sem senha."),
    ("doesRegistrationRequireAuth", B, "Exige token de integração no cadastro sem interface."),
    ("headlessDiscoveryExecutionUser", "Id", "Id do usuário de integração que roda o handler de descoberta."),
    ("headlessDiscoveryHandler", S, "Classe Apex que implementa a interface de descoberta."),
    ("isFirstPartyAppsAllowed", B, "Permite fluxos sem interface com OAuth de primeira parte."),
    ("isForgotPwdAllowed", B, "Liga o fluxo de senha esquecida sem interface."),
    ("isForgotPwdEmailTemplateAllowlistingEnabled", B, "Restringe os e-mails de senha esquecida aos modelos permitidos."),
    ("isHeadlessUserRegistrationAllowed", B, "Liga o cadastro sem interface."),
    ("IsPwdlessLoginAllowed", B, "Liga o login sem senha sem interface."),
    ("isRecaptchaRequiredForgotPwd", B, "Exige reCAPTCHA na senha esquecida."),
    ("isRecaptchaRequiredPwdlessLogin", B, "Exige reCAPTCHA no login sem senha."),
    ("isRecaptchaRequiredRgstr", B, "Exige reCAPTCHA no cadastro."),
    ("isUniversalClientRgstrAllowed", B, "Liga o autocadastro pela Universal Registration API."),
    ("isUserDisambiguationAllowedForgotPwd", B, "Usa o handler de descoberta na senha esquecida."),
    ("isUserDisambiguationAllowedUsernamePwd", B, "Usa o handler de descoberta no login."),
    ("maxPasswordResetAttempts", I, "Tentativas de redefinição antes de exigir novo código."),
    ("recaptchaScoreThreshold", "double", "Pontuação mínima do reCAPTCHA v3, de 0,5 a 1.", "C:Quando o reCAPTCHA é exigido."),
    ("recaptchaSecretKey", S, "Chave secreta do reCAPTCHA fornecida pelo Google.", "C:Quando o reCAPTCHA é exigido."),
    ("registrationExecutionUser", S, "Usuário que roda o handler de cadastro."),
    ("registrationHandler", S, "Handler Apex do cadastro sem interface."),
    ("registrationUserDefaultProfile", S, "Perfil dado a quem se cadastra."),
]] + [P("emailTmplsAllowlist", "NetworkEmailTmplAllowlist[]", H60, "Modelos de e-mail permitidos nos fluxos sem interface.",
        estrutura="NetworkEmailTmplAllowlist")],
    "As opções da autenticação sem interface (headless) do site: cadastro, login sem senha, senha esquecida e reCAPTCHA (API 60.0 ou posterior).")
estrutura("NetworkMemberGroups", S_NET, [ESTR_NET], [
    P("permissionSet", S, None, "Permission set cujos usuários são membros do site."),
    P("profile", S, None, "Perfil cujos usuários são membros do site."),
], "Os perfis e permission sets que dão acesso ao site. A seção da página chama-se NetworkMemberGroup.")
OVR = valores("Configurable", "Designer", "Standard", "VisualForce")
estrutura("NetworkPageOverride", S_NET, [ESTR_NET], [P(f"{n}PageOverrideSetting", "NetworkPageOverrideSetting", None, f"Tipo da página de {d_}.", "S", vals=OVR)
                                                    for n, d_ in [("changePassword", "troca de senha"), ("forgotPassword", "senha esquecida"),
                                                                  ("home", "início"), ("login", "login"), ("selfRegProfile", "autocadastro")]],
          "Que tipo de página o site usa para login, autocadastro, senha esquecida, troca de senha e início.")
estrutura("RecommendationAudienceDetail", S_NET, ["mdx:RecommendationAudience"], [
    P("audienceCriteriaType", "AudienceCriteriaType", "41.0", "Critério do público.", vals=valores("CustomList", "MaxDaysInCommunity")),
    P("audienceCriteriaValue", S, "41.0", "Máximo de dias como membro; nulo em listas customizadas."),
    P("setupName", S, "41.0", "Nome do público."),
], "Os detalhes de um público de recomendações.")
estrutura("RecommendationAudience", S_NET, [ESTR_NET], [
    P("recommendationAudienceDetails", "RecommendationAudienceDetail", "41.0", "Detalhes do público.", estrutura="RecommendationAudienceDetail"),
], "Um público de recomendações do site (API 41.0 ou posterior).")
estrutura("ScheduledRecommendationDetail", S_NET, ["mdx:ScheduledRecommendation"], [
    P("channel", "RecommendationChannel", "41.0", "Onde a recomendação aparece.",
      vals=valores("DefaultChannel", "CustomChannel1", "CustomChannel2", "CustomChannel3", "CustomChannel4", "CustomChannel5")),
    P("enabled", B, "41.0", "Liga a recomendação no site."),
    P("rank", I, "41.0", "Posição; sem valor, vai para o fim."),
    P("recommendationAudience", S, "41.0", "Público da recomendação."),
], "Uma recomendação agendada.")
estrutura("ScheduledRecommendation", S_NET, ["mdx:RecommendationDefinitionDetail"], [
    P("scheduledRecommendationDetails", "ScheduledRecommendationDetail[]", "41.0", "Recomendações agendadas.", estrutura="ScheduledRecommendationDetail"),
], "A lista de recomendações agendadas.")
estrutura("RecommendationDefinitionDetail", S_NET, ["mdx:RecommendationDefinition"], [
    P("actionUrl", S, "41.0", "Endereço do botão de ação."), P("description", S, "41.0", "O que o usuário pode fazer."),
    P("linkText", S, "41.0", "Rótulo do botão."),
    P("scheduledRecommendations", "ScheduledRecommendation", "41.0", "Recomendações agendadas.", estrutura="ScheduledRecommendation"),
    P("setupName", S, "41.0", "Nome mostrado no Setup."), P("title", S, "41.0", "Título da recomendação."),
], "Uma recomendação customizada.")
estrutura("RecommendationDefinition", S_NET, [ESTR_NET], [
    P("recommendationDefinitionDetails", "RecommendationDefinitionDetail[]", "41.0", "Recomendações customizadas.", estrutura="RecommendationDefinitionDetail"),
], "As recomendações customizadas do site (API 41.0 ou posterior).")
estrutura("ReputationBranding", S_NET, ["mdx:ReputationLevel"], [
    P("smallImage", S, "32.0", "Imagem do nível (.jpeg, .png ou .gif); sem ela, vale a padrão."),
], "A imagem de um nível de reputação.")
estrutura("ReputationLevel", S_NET, ["mdx:ReputationLevelDefinitions"], [
    P("branding", "ReputationBranding[]", "32.0", "Imagem do nível.", estrutura="ReputationBranding"),
    P("label", S, None, "Nome do nível; padrão Level 1 a Level 10."),
    P("lowerThreshold", "double", None, "Menor pontuação da faixa do nível.", "S"),
], "Um nível de reputação.")
estrutura("ReputationLevelDefinitions", S_NET, [ESTR_NET], [
    P("level", "ReputationLevel[]", None, "Os níveis de reputação.", estrutura="ReputationLevel"),
], "Os níveis de reputação do site.")
EVT = ("FeedItemWriteAPost", "FeedItemWriteAComment", "FeedItemReceiveAComment", "FeedItemLikeSomething", "FeedItemReceiveALike",
       "FeedItemMentionSomeone", "FeedItemSomeoneMentionsYou", "FeedItemShareAPost", "FeedItemSomeoneSharesYourPost", "FeedItemPostAQuestion",
       "FeedItemAnswerAQuestion", "FeedItemReceiveAnAnswer", "FeedItemMarkAnswerAsBest", "FeedItemYourAnswerMarkedBest",
       "FeedItemEndorseSomeoneForKnowledgeOnATopic", "FeedItemEndorsedForKnowledgeOnATopic")
estrutura("ReputationPointsRule", S_NET, ["mdx:ReputationPointsRules"], [
    P("eventType", S, None, "Evento que dá pontos.", "S", vals=valores(*EVT)),
    P("points", I, None, "Pontos por evento; os padrões são +1, +5 ou +20.", "S"),
], "Uma regra de pontos de reputação.")
estrutura("ReputationPointsRules", S_NET, [ESTR_NET], [
    P("pointsRule", "ReputationPointsRule[]", None, "Os eventos e seus pontos.", estrutura="ReputationPointsRule"),
], "As regras de pontos de reputação do site.")
estrutura("NetworkTabSet", S_NET, [ESTR_NET], [
    P("customTab", S, None, "Aba customizada do site."), P("defaultTab", S, None, "Aba inicial depois do login."),
    P("standardTab", S, None, "Aba padrão do site."),
], "As abas de um site Salesforce Tabs + Visualforce.")

# Translations
estrutura("PicklistValueTranslation", S_COT, ["mdx:GlobalPicklistTranslation"], [
    P("masterLabel", S, None, "Valor original do picklist, mostrado quando não há tradução.", "S"),
    P("translation", S, None, "O texto traduzido.", "S"),
], "A tradução de um valor de picklist.")

M.emit_structs()

# ================================================================ ligações e enumerações nos cadastros existentes
for s_ in ("FilterItem",):
    LG.definir_valores("estruturas", s_, "operation", ["equals", "notEqual", "lessThan", "greaterThan", "lessOrEqual", "greaterOrEqual", "contains",
                                                        "notContain", "startsWith", "includes", "excludes", "within"], S_CF,
                       "within só vale em critérios de distância.")
LG.definir_valores("estruturas", "FeedLayoutFilter", "feedItemType", [
    "ActivityEvent", "AdvancedTextPost", "AnnouncementPost", "ApprovalPost", "AttachArticleEvent", "BasicTemplateFeedItem", "CallLogPost", "CanvasPost",
    "CaseCommentPost", "ChangeStatusPost", "ChatTranscriptPost", "CollaborationGroupCreated", "CollaborationGroupUnarchived", "ContentPost",
    "CreatedRecordEvent", "DashboardComponentSnapshot", "EmailMessageEvent", "FacebookPost", "LinkPost", "MilestoneEvent", "PollPost",
    "ProfileSkillPost", "QuestionPost", "ReplyPost", "RypplePost", "SocialPost", "TextPost", "TrackedChange", "UserStatus"], S_LAY,
    "A página marca AnnouncementPost, BasicTemplateFeedItem, CollaborationGroupUnarchived, FacebookPost e UserStatus como não usados.")
LG.definir_valores("estruturas", "SummaryLayout", "summaryLayoutStyle", ["Default", "QuoteTemplate", "DefaultQuoteTemplate", "CaseInteraction",
                                                                         "QuickActionLayoutLeftRight", "QuickActionLayoutTopDown"], S_LAY)
LG.definir_valores("estruturas", "PlatformActionList", "actionListContext", [
    "Assistant", "BannerPhoto", "Chatter", "Dockable", "FeedElement", "Flexipage", "Global", "ListView", "ListViewDefinition", "ListViewRecord",
    "Lookup", "MruList", "MruRow", "ObjectHomeChart", "Photo", "Record", "RecordEdit", "RelatedList", "RelatedListRecord"], S_FP)
LG.definir_valores("estruturas", "AutoResponseRules_RuleEntry", "assignedToType", ["User", "Queue"], S_ESC)
LG.definir_valores("estruturas", "AutoResponseRules_RuleEntry", "businessHoursSource", ["None", "Case", "Static"], S_ESC)
LG.definir_valores("estruturas", "AutoResponseRules_RuleEntry", "escalationStartTime", ["CaseCreation", "CaseLastModified"], S_ESC)
LG.definir_valores("estruturas", "ProfileTabVisibility", "visibility", ["DefaultOff", "DefaultOn", "Hidden"], S_PRN)
LG.definir_valores("metadata-types", "QuickAction", "standardLabel", [
    "AddRecord", "AddMember", "ChangeDueDate", "ChangePriority", "ChangeStatus", "CreateNew", "CreateNewRecordType", "Defer", "EditDescription",
    "EnrollInProgram", "Escalate", "EscalateToRecord", "Forward", "LogACall", "LogANote", "ModifyAppointment", "New", "NewChild", "NewChildRecordType",
    "NewRecordType", "OfferFeedback", "PatientDetails", "PerformCount", "Quick", "QuickRecordType", "RelocateAsset", "ReplaceAsset", "Reply", "ReplyAll",
    "RequestFeedback", "SendEmail", "Update"], S_QA)
LG.definir_valores("metadata-types", "FlexiPage", "type", [
    "CdpRecordPage", "AppPage", "CommAppPage", "CommContractDetailViewPage", "CommCheckoutPage", "CommFlowPage", "CommForgotPasswordPage",
    "CommGlobalSearchResultPage", "CommLoginPage", "CommNoSearchResultsPage", "CommObjectPage", "CommOrderComfirmationPage", "CommQuickActionCreatePage",
    "CommRecordPage", "CommRelatedListPage", "CommSearchResultPage", "CommSelfRegisterPage", "CommThemeLayoutPage", "EmbeddedServicePage",
    "EmailContentPage", "EmailTemplatePage", "ForecastingPage", "HomePage", "MailAppAppPage", "OmniSupervisorPageType", "QuickAction", "RecordPage",
    "RecordPreview", "UtilityBar", "VoiceExtension"], S_FP,
    "Grafias como estão na página (CommOrderComfirmationPage, OmniSupervisorPageType); CommFlowPage aparece duas vezes e entrou uma vez.")
MOTIF = ("Heart Fan Sun Hexagon Leaf Triangle Square Diamond Lightning Moon Star Circle Box Hands People Bank Sack Form Wrench Airplane Computer "
         "Telephone Envelope Building Alarmclock Flag Laptop Cellphone PDA Radardish Car Factory Desk Insect Microphone Train Bridge Camera Telescope "
         "Creditcard Cash Treasurechest Jewel Hammer Ticket Stamp Knight Trophy CD/DVD Bigtop Apple Balls Bell Boat Books Bottle BuildingBlock Caduceus "
         "Can Umbrella Castle Chalkboard Chip Compass Cup Dice Gears Globe Guitar Handsaw Headset Helicopter HighwaySign HotAirBalloon IPPhone Keys "
         "Locked Map MeasuringTape Motorcycle MusicalNote Whistle Pencil Presenter RealEstateSign RedCross Safe Sailboat Saxophone Scales Shield Ship "
         "ShoppingCart Stethoscope Stopwatch StreetSign Thermometer Truck TVCRT TVWidescreen").split()
assert len(MOTIF) == 100
LG.definir_valores("metadata-types", "CustomTab", "motif", [f"Custom{i}:{m}" for i, m in enumerate(MOTIF, 1)], S_CTN,
                   "A página marca o campo como não obrigatório, mas a descrição diz Required.")

# DuplicateRuleFilterItem herda os campos de FilterItem, que a página de DuplicateRule não repete
LG.acrescentar_propriedades("estruturas", "DuplicateRuleFilterItem", [
    P("field", S, None, "Campo comparado.", herdada="FilterItem"),
    P("operation", "FilterOperation", None, "Operação do filtro.", herdada="FilterItem",
      vals=valores("equals", "notEqual", "lessThan", "greaterThan", "lessOrEqual", "greaterOrEqual", "contains", "notContain", "startsWith",
                   "includes", "excludes", "within")),
    P("value", S, None, "Valor comparado.", herdada="FilterItem"),
    P("valueField", S, None, "Campo cujo valor é comparado, em vez de um valor fixo.", herdada="FilterItem"),
], S_CF)

# ordem: estruturas internas antes dos tipos que as usam
for s_ in ("EntitlementProcessMilestoneTimeTrigger", "EntitlementProcessMilestoneItem"):
    LG.ligar("estruturas", s_, {"actions": "WorkflowActionReference", "successActions": "WorkflowActionReference"} if "Trigger" in s_ else
             {"successActions": "WorkflowActionReference"}, nota="Contagem conforme a seção do subtipo na página oficial.")
LG.ligar("estruturas", "GlobalPicklistTranslation", {"picklistValues": "PicklistValueTranslation"}, nota="Contagem conforme a seção do subtipo na página oficial.")
LG.ligar("estruturas", "Picklist", {}, nota="Contagem conforme a seção do subtipo na página oficial.")
LG.ligar("estruturas", "RecordTypePicklistValue", {}, nota="Contagem conforme a seção do subtipo na página oficial.")
LG.ligar("estruturas", "DuplicateRuleFilterItem", {}, esperado=6,
         nota="2 campos próprios na página de DuplicateRule e 4 herdados de FilterItem, conforme a página de CustomField relida em 2026-11-17.")
LG.ligar("estruturas", "DuplicateRuleFilter", {})

NOTA_PR = ("Campos de primeiro nível completos conforme a página 68.0. Em 2026-11-17, a página foi relida inteira: LoginFlow, ProfileActionOverride, "
           "ProfileAgentAccess e ProfileLoginHours estão nos primeiros 100 mil caracteres (a nota anterior dizia, por engano, que não tinham seção). "
           "ProfileUserPermission e ProfileServicePresenceStatusAccess estão na segunda parte.")
ESTADO = {
    "Profile": LG.ligar("metadata-types", "Profile", {"loginFlows": "LoginFlow", "profileActionOverrides": "ProfileActionOverride",
                                                      "agentAccesses": "ProfileAgentAccess", "loginHours": "ProfileLoginHours"}, nota=NOTA_PR, src=S_PR1),
    "CustomField": LG.ligar("metadata-types", "CustomField", {}, nota=(
        "Página relida em 2026-11-17 pelo endereço customfield.htm (116 mil caracteres): os 60 campos do primeiro nível conferem. Os subtipos "
        "MktDataLakeFieldAttributes e MktDataModelFieldAttributes (Data 360) são descritos, mas nenhum campo de CustomField os usa; ficaram de fora. "
        "elementType é reservado para uso futuro e não tem valores listados. A página declara que, salvo indicação, os campos são criáveis, "
        "filtráveis e anuláveis.")),
    "RecordType": LG.ligar("metadata-types", "RecordType", {}),
    "BusinessProcess": LG.ligar("metadata-types", "BusinessProcess", {}, nota="Universo esperado = tabela Fields da página do guia versionado 264.0, "
                                "lida em 2026-11-17 (5 campos). values usa o tipo PicklistValue, cadastrado no lote 7n."),
    "CustomObject": LG.ligar("metadata-types", "CustomObject", {"actionOverrides": "ActionOverride", "namedFilter": "NamedFilter",
                                                                "sharingRecalculations": "SharingRecalculation"},
                             nota="Tabela Fields lida em 100k de 101,8k caracteres; os ~1,8k finais continham apenas exemplo. Em 2026-11-17: SearchLayouts, "
                                  "ProfileSearchLayouts, HistoryRetentionPolicy, ActionOverride, NamedFilter (até a API 29.0) e SharingRecalculation "
                                  "viraram estruturas; BusinessProcess, FieldSet, Index e SharingReason, metadata types filhos."),
    "CustomTab": LG.ligar("metadata-types", "CustomTab", {"actionOverrides": "ActionOverride"}, src=S_AO,
                          nota="Universo esperado = tabela Fields da página oficial 68.0 (mais fullName herdado quando declarado). urlEncodingKey: a página "
                               "remete a lista de Encoding a outra referência; o padrão é UTF-8."),
    "QuickAction": LG.ligar("metadata-types", "QuickAction", {"fieldOverrides": "FieldOverride", "quickActionLayout": "QuickActionLayout",
                                                              "quickActionParameters": "QuickActionParameter"}, src=S_QA),
    "FlexiPage": LG.ligar("metadata-types", "FlexiPage", {"events": "FlexiPageEvent", "flexiPageRegions": "FlexiPageRegion",
                                                          "platformActionlist": "PlatformActionList", "quickActionList": "QuickActionList",
                                                          "template": "FlexiPageTemplateInstance"}, src=S_FP, esperado=12,
                          nota="Universo esperado = tabela Fields da página do guia versionado 264.0 (11 campos mais fullName herdado), relida inteira em 2026-11-17 com os "
                               "subtipos."),
    "GenAiPlugin": LG.ligar("metadata-types", "GenAiPlugin", {"aiPluginUtterances": "AiPluginUtteranceDef", "genAiPluginInstructions": "GenAiPluginInstructionDef"},
                            nota="Universo esperado = tabelas Fields da página do guia versionado 264.0 (API 68.0), lida em 2026-11-16. Os subtipos "
                                 "AiPluginUtteranceDef e GenAiPluginInstructionDef têm páginas próprias, lidas em 2026-11-17."),
    "Network": LG.ligar("metadata-types", "Network", {
        "branding": "Branding", "navigationLinkSet": "NavigationLinkSet", "networkAuthApiSettings": "NetworkAuthApiSettings",
        "networkMemberGroups": "NetworkMemberGroups", "networkPageOverrides": "NetworkPageOverride", "recommendationAudience": "RecommendationAudience",
        "recommendationDefinition": "RecommendationDefinition", "reputationLevels": "ReputationLevelDefinitions",
        "reputationPointsRules": "ReputationPointsRules", "tabs": "NetworkTabSet"}, src=S_NET,
        nota="Universo esperado = tabelas Fields da página do guia versionado 264.0 (API 68.0). Primeiro nível: 70 de 70 campos, mais fullName. Os "
             "subtipos foram lidos em 2026-11-17, de 55 mil caracteres até o fim da página (176.651)."),
    "Layout": LG.ligar("metadata-types", "Layout", {}, esperado=24,
                       nota="Universo esperado = tabela Fields da página do guia versionado 264.0 (API 68.0). A página não marca campos como obrigatórios "
                            "no tipo principal. Primeiro nível: 24 de 24 campos. As enumerações FeedItemType, SummaryLayoutStyle e "
                            "PlatformActionListContext foram transcritas em 2026-11-17."),
    "AutoResponseRules": LG.ligar("metadata-types", "AutoResponseRules", {}, esperado=1,
                                  nota="Universo esperado = tabela Fields da página oficial lida em 2026-11-15. Os valores das três enumerações de "
                                       "RuleEntry foram lidos na página de EscalationRules em 2026-11-17."),
    "DuplicateRule": LG.ligar("metadata-types", "DuplicateRule", {}, esperado=13,
                              nota="Universo esperado = tabelas Fields da página do guia versionado 264.0 (API 68.0), lida em 2026-11-16. Os campos "
                                   "que DuplicateRuleFilterItem herda de FilterItem foram acrescentados em 2026-11-17."),
    "EntitlementProcess": LG.ligar("metadata-types", "EntitlementProcess", {},
                                   nota="Universo esperado = tabela Fields da página oficial 68.0 (mais fullName herdado quando declarado). "
                                        "WorkflowActionReference ligado em 2026-11-17."),
    "Translations": LG.ligar("metadata-types", "Translations", {}, esperado=33,
                             nota="Universo esperado = tabela Fields da página do guia versionado 264.0 (API 68.0). Primeiro nível: 33 de 33 campos. "
                                  "Dos 59 subtipos descritos na página, 58 estão cadastrados; FlowTextTemplateTranslation ficou fora, porque nenhum "
                                  "campo o usa. PicklistValueTranslation veio da página de CustomObjectTranslation."),
    "PresenceUserConfig": LG.ligar("metadata-types", "PresenceUserConfig", {}, esperado=18,
                                   nota="A tabela da página tem 18 linhas: 17 campos e uma linha vazia, sem nome, tipo nem descrição (conferido em "
                                        "2026-11-17). Universo = 17 campos mais fullName herdado."),
    "ListView": LG.ligar("metadata-types", "ListView", {"sharedTo": "SharedTo"}, src="src:mdapi-sharedto",
                         nota="Universo esperado = tabelas Fields da página do guia versionado 264.0 (API 68.0). SharedTo foi cadastrado no lote 7m. "
                              "language usa a lista de idiomas de outra página."),
    "ReportFolder": LG.ligar("metadata-types", "ReportFolder", {"sharedTo": "SharedTo"}, src="src:mdapi-sharedto",
                             nota="Universo esperado = tabelas Fields da página do guia versionado 264.0 (API 68.0). SharedTo foi cadastrado no lote 7m."),
    "DashboardFolder": LG.ligar("metadata-types", "DashboardFolder", {"sharedTo": "SharedTo"}, src="src:mdapi-sharedto",
                                nota="Universo esperado = tabelas Fields da página do guia versionado 264.0 (API 68.0). SharedTo foi cadastrado no lote 7m."),
}
# FilterItem e as estruturas que mudaram também recalculam
for s_ in ("FilterItem", "FeedLayoutFilter", "SummaryLayout", "PlatformActionList", "AutoResponseRules_RuleEntry", "ProfileTabVisibility"):
    LG.ligar("estruturas", s_, {})
LG.ligar("metadata-types", "QuickAction", {})
LG.ligar("metadata-types", "FlexiPage", {})
LG.ligar("metadata-types", "CustomTab", {})

# ================================================================ nota de extração: lista de campos
ls = ["", "-- Lista de campos transcrita da leitura (gerada por lote7n_b5_estruturas.py; nome | tipo)"]
for src, pasta, nome in REG:
    ls.append(f"[{src}] {nome}: " + ", ".join(f"{q['nome']} | {q['tipo_tecnico']}" for q in ld(f"{pasta}/{nome}.json")["propriedades"]))
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(ls) + "\n")
C.ampliar_funcionalidade("tipos-de-registro", mdts=[("PicklistValue", "Os valores de picklist liberados em cada record type e business process.")], srcs=[S_PV])
C.ampliar_funcionalidade("campos-customizados", mdts=[("PicklistValue", "Os valores de picklists no formato antigo (até a API 37.0).")], srcs=[S_PV])
d = ld("metadata-types/PresenceUserConfig.json")
if not any(e.get("fonte") == S_PUC for e in d["evidencias"]):
    d["evidencias"].append(ev(S_PUC))
sv("metadata-types/PresenceUserConfig.json", d)
C.ampliar_funcionalidade("objetos-customizados", mdts=[("SharingReason", "Os motivos do compartilhamento gerido por Apex.")], srcs=[S_SRS])
print("lote 7n:", ESTADO)
