"""Lote 7o (rodada B5, parte B; issue #34): os subtipos de Flow.

A página de Flow no guia versionado 264.0 (meta_visual_workflow, 825.034 caracteres) foi lida por partes de 100 mil caracteres, com
leituras extras nas junções. Cada seção de subtipo vira uma estrutura; os campos herdados (FlowBaseElement → FlowElement → FlowNode)
entram em cada estrutura marcados com herdada_de, como nos demais tipos do catálogo. FlowBaseElement, FlowElement e FlowNode não viram
estruturas próprias, porque nenhuma propriedade os usa diretamente.

Ordem: lote7n_b5_estruturas.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7o_b5_flow.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga.base import ev, ld, sv, caminho    # noqa: E402
from carga import catalogo as C               # noqa: E402
from carga import ligacao as LG               # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7o-b5-flow.txt"
SRC = "src:mdapi-flow-subtipos"
p = caminho("fontes", "registro.json")
reg = json.load(open(p, encoding="utf-8"))
reg["fontes"] = [x for x in reg["fontes"] if x["id"] != SRC] + [C.fonte(
    SRC, "Flow, subtipos (Metadata API)", "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/meta_visual_workflow.htm",
    "As seções de subtipo da página de Flow (de FlowActionCall a FlowWaitEventOutputParameter).", EXTR, DATA)]
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

B, S, I = "boolean", "string", "int"
FERV = "FlowElementReferenceOrValue"
CON = "FlowConnector"
RES = "Reservado para uso futuro."
DT_BASE = ["Currency", "Date", "Number", "String", "Boolean", "Time"]
ASC = ["Asc", "Desc"]
OPS_ATR = ["Add", "AddAtStart", "AddItem", "Assign", "AssignCount", "RemoveAfterFirst", "RemoveAll", "RemoveBeforeFirst", "RemoveFirst",
           "RemovePosition", "RemoveUncommon", "Subtract"]
CMP = ["Contains", "EndsWith", "EqualTo", "GreaterThan", "GreaterThanLastNumberOfDays", "GreaterThanOrEqualTo", "HasError", "HasNoValue", "HasValue",
       "In", "IsAfter", "IsAnniversaryOfToday", "IsBefore", "IsBlank", "IsChanged", "IsEmpty", "IsLastMonth", "IsNextMonth", "IsNotAnniversaryOfToday",
       "IsNull", "IsOn", "IsThisMonth", "IsToday", "IsTomorrow", "IsYesterday", "LastNumberOfDays", "LastNumberOfMonths", "LastNumberOfYears", "LastYear",
       "LessThan", "LessThanOrEqualTo", "NextNumberOfDays", "NextNumberOfMonths", "NextYear", "None", "NotEqualTo", "NotIn", "StartsWith", "ThisYear",
       "WasSelected", "WasSet", "WasVisited"]
OFFSET = ["Months", "Days", "Hours", "Minutes"]
LOGICA = "Combinação das condições: and, or ou lógica customizada, como 1 AND (2 OR 3)."
ENUM_FORA = "Enumeração com valores agrupados por produto na página; a lista não foi transcrita."


def F(nome, tipo, desde=None, desc="", req="N", vals=None, **kw):
    """Linha de campo de subtipo. Tipos de data e hora e Id recebem a natureza certa; enumerações sem lista ficam 'desconhecida' com contexto."""
    t = tipo.replace("[]", "")
    if vals:
        kw["vals"] = [(v, None) for v in vals]
    elif t in ("date", "dateTime", "time", "Time"):
        kw.setdefault("natureza", "data_hora")
    elif t in ("String",):
        kw.setdefault("natureza", "texto_livre")
    return (nome, tipo, desde, desc, req, kw)


FBE = [F("processMetadataValues", "FlowMetadataValue[]", "32.0", "Informações de contexto sobre o elemento.")]
FE = [F("description", S, None, "Descrição do elemento."), F("name", S, None, "Nome único do elemento.", "S")]
FN = [F("elementSubtype", "FlowElementSubtype", None, "Reservado para uso interno.", natureza="desconhecida", contexto="Reservado para uso interno."),
      F("group", S, "68.0", "Grupo a que o nó pertence."), F("label", S, None, "Nome de exibição do nó; não precisa ser único."),
      F("locationX", I, None, "Posição horizontal, em pixels; 0 no auto-layout.", "S"),
      F("locationY", I, None, "Posição vertical, em pixels; 0 no auto-layout.", "S")]
HER = {"FlowBaseElement": FBE, "FlowElement": FE + FBE, "FlowNode": FN + FE + FBE}
DONO_HER = {"processMetadataValues": "FlowBaseElement", "description": "FlowElement", "name": "FlowElement", "elementSubtype": "FlowNode",
            "group": "FlowNode", "label": "FlowNode", "locationX": "FlowNode", "locationY": "FlowNode"}
INP = [F("name", S, None, "Nome único do parâmetro.", "S"), F("value", FERV, None, "Valor do parâmetro.")]
OUTP = [F("assignToReference", S, None, "Variável que recebe a saída.", "S"), F("name", S, None, "Nome único da saída.", "S")]
OUT_RES = [F("assignToReference", S, None, RES), F("name", S, None, "Nome único da saída.", "S")]

# seção: (estende, versão, o que é, campos próprios)
SEC = {
    "FlowActionCall": ("FlowNode", None, "Um elemento Action: chama uma ação invocável, como enviar e-mail, rodar Apex ou chamar outro serviço.", [
        F("actionCallPaths", "ActionCallPath[]", None, RES, notas=["A página grafa o tipo como ActionCallPath[]; a seção correspondente é FlowActionCallPath."]),
        F("actionName", S, None, "Nome da ação.", "S"),
        F("actionType", "InvocableActionType", None, "Tipo da ação chamada.", "S", natureza="desconhecida", contexto=ENUM_FORA),
        F("connector", CON, None, "Próximo nó."), F("dataTypeMappings", "FlowDataTypeMapping[]", "48.0", "Mapeamentos de tipo para dados sObject."),
        F("einsteinDecidePath", S, None, RES), F("faultConnector", CON, None, "Nó executado em caso de erro."),
        F("flowTransactionModel", "FlowTransactionModel", "51.0", "Como a ação lida com a transação.", "S", natureza="desconhecida",
          contexto="A seção lida não lista os valores."),
        F("inputParameters", "FlowActionCallInputParameter[]", None, "Entradas da ação."),
        F("isWaitUntilCompleted", B, "61.0", "Pausa o flow até a ação terminar."),
        F("nameSegment", S, "58.0", "Nome da ação versionada.", ate="61.0", notas=["Descontinuado na API 62.0."]),
        F("offset", I, "61.0", "Quantidade de tempo de espera."), F("offsetUnit", "FlowScheduledPathOffsetUnit", "61.0", "Unidade do tempo de espera.", vals=OFFSET),
        F("outputParameters", "FlowActionCallOutputParameter[]", None, "Saídas devolvidas ao flow."),
        F("storeOutputAutomatically", B, "48.0", "Disponibiliza as saídas sem criar variáveis."),
        F("timeoutConnector", CON, "62.0", "Nó executado quando o tempo se esgota."),
        F("timeoutPathUsage", "FlowActionCallTimeoutPath", "66.0", "Liga ou desliga o caminho de tempo esgotado.", natureza="desconhecida",
          contexto="A seção lida não lista os valores."),
        F("versionSegment", I, "58.0", "Versão da ação versionada.", ate="61.0", notas=["Descontinuado na API 62.0."]),
        F("versionString", S, None, RES)]),
    "FlowActionCallInputParameter": ("FlowBaseElement", "31.0", "Uma entrada de uma ação.", INP),
    "FlowActionCallOutputParameter": ("FlowBaseElement", "31.0", "Uma saída de uma ação.", OUTP),
    "FlowActionCallPath": ("FlowBaseElement", "63.0", "Um caminho de saída de uma ação.", [
        F("connector", CON, None, "Nó executado em seguida.", "S"), F("pathName", S, None, "Nome único do caminho.", "S")]),
    "FlowApexPluginCall": ("FlowNode", None, "Uma chamada a um plug-in Apex (formato antigo de ação Apex).", [
        F("apexClass", S, None, "Classe Apex.", "S"), F("connector", CON, None, "Próximo nó."), F("faultConnector", CON, None, "Nó executado em caso de erro."),
        F("inputParameters", "FlowApexPluginCallInputParameter[]", None, "Entradas do plug-in."),
        F("outputParameters", "FlowApexPluginCallOutputParameter[]", None, "Saídas do plug-in.")]),
    "FlowApexPluginCallInputParameter": ("FlowBaseElement", None, "Uma entrada de um plug-in Apex.", INP),
    "FlowApexPluginCallOutputParameter": ("FlowBaseElement", None, "Uma saída de um plug-in Apex.", OUTP),
    "FlowAssignment": ("FlowNode", None, "Um elemento Assignment: muda valores de variáveis.", [
        F("assignmentItems", "FlowAssignmentItem[]", None, "Operações, na ordem."), F("connector", CON, None, "Próximo nó.")]),
    "FlowAssignmentItem": ("FlowBaseElement", None, "Uma operação de um Assignment.", [
        F("assignToReference", S, None, "Variável alterada."), F("operator", "FlowAssignmentOperator", None, "Operação aplicada.", vals=OPS_ATR),
        F("value", FERV, None, "Valor usado pela operação.")]),
    "FlowChoice": ("FlowElement", None, "Uma opção de escolha usada em componentes de tela.", [
        F("choiceIcon", "FlowIcon", "64.0", "Ícone ao lado da opção."), F("choiceText", S, None, "Texto mostrado ao usuário.", "S"),
        F("dataType", "FlowDataType", None, "Tipo do valor da opção.", "S", vals=DT_BASE),
        F("userInput", "FlowChoiceUserInput", None, "Campo de texto que aparece quando a opção é escolhida."),
        F("value", FERV, None, "Valor usado em tempo de execução.")]),
    "FlowChoiceUserInput": ("FlowBaseElement", None, "A entrada de texto ligada a uma opção.", [
        F("isRequired", B, None, "Torna a entrada obrigatória."), F("promptText", S, None, "Texto de orientação; aceita merge fields."),
        F("validationRule", "FlowInputValidationRule", None, "Validação da entrada.")]),
    "FlowCollectionProcessor": ("FlowNode", "50.0", "Um elemento que ordena, filtra ou transforma uma coleção.", [
        F("assignNextValueToReference", S, None, "Variável que recebe cada item."),
        F("collectionProcessorType", "FlowCollectionProcessorType", None, "Tipo de processamento.",
          vals=["SortCollectionProcessor", "RecommendationMapCollectionProcessor", "FilterCollectionProcessor"]),
        F("collectionReference", S, None, "Coleção processada."), F("conditionLogic", S, None, LOGICA + " Também aceita Formula."),
        F("conditions", "FlowCondition[]", None, "Condições de filtro."), F("connector", CON, None, "Próximo nó."),
        F("formula", S, None, "Fórmula do filtro; os registros que a atendem ficam."), F("limit", I, "51.0", "Máximo de itens na saída."),
        F("mapItems", "FlowCollectionMapItem[]", None, "Regras de mapeamento de campos."), F("outputSObjectType", S, None, "Tipo sObject da saída."),
        F("sortOptions", "FlowCollectionSortOption[]", "51.0", "Opções de ordenação.")]),
    "FlowCollectionSortOption": (None, "51.0", "Uma opção de ordenação de coleção.", [
        F("doesPutEmptyStringAndNullFirst", B, None, "Põe vazios e nulos primeiro; padrão false."),
        F("sortField", S, None, "Campo de ordenação; não vale para listas de primitivos.", "C:Em coleções de registros."),
        F("sortOrder", "SortOrder", None, "Direção da ordenação.", vals=ASC)]),
    "FlowCustomError": ("FlowNode", None, "Um elemento Custom Error: mostra mensagens de erro ao usuário.", [
        F("connector", CON, None, "Próximo nó.", "S"), F("customErrorMessages", "FlowCustomErrorMessage[]", None, "Mensagens de erro.")]),
    "FlowCustomErrorMessage": ("FlowBaseElement", None, "Uma mensagem de erro customizada.", [
        F("errorMessage", S, None, "Texto da mensagem.", "S"), F("fieldSelection", S, None, "Campo ligado à mensagem."),
        F("isFieldError", B, None, "true mostra no campo; false mostra numa janela; padrão false.", "S")]),
    "FlowCondition": ("FlowBaseElement", None, "Uma condição: compara um lado esquerdo com um lado direito.", [
        F("aggregationOperator", S, None, "Operação aplicada à variável.", vals=["Count"]), F("conditionLogic", S, None, "and ou or.", vals=["and", "or"]),
        F("conditionType", "FlowWaitConditionType", None, "Papel da condição.", vals=["Container", "EntryCondition", "ExitCondition"]),
        F("conditions", "FlowCondition[]", None, "Condições aninhadas."), F("leftValueReference", S, None, "Elemento do lado esquerdo.", "S"),
        F("operator", "FlowComparisonOperator", None, "Operador de comparação.", "S", vals=CMP,
          notas=["Vários valores exigem versões mínimas (52.0 a 67.0), indicadas na página."]),
        F("rightValue", FERV, None, "Lado direito: elemento ou valor literal.")]),
    "FlowDataLookup": ("FlowElement", "68.0", "Uma busca de registros relacionados feita no início do flow.", [
        F("lookupField", S, "68.0", "Campo do objeto de origem usado na junção.", "S"), F("lookupReference", S, "68.0", "Referência de lookup a partir do registro principal.", "S"),
        F("sourceApiName", S, "68.0", "Nome de API do objeto buscado.", "S"), F("sourceType", S, "68.0", "Tipo do objeto de origem.", "S", vals=["DataModelObject"])]),
    "FlowCustomProperty": (None, "63.0", "Uma propriedade customizada do flow, como o indicador de progresso da tela.", [
        F("name", S, "63.0", "Nome único da propriedade.", "S"), F("value", FERV, "63.0", "Valor da propriedade.")]),
    "FlowConnector": ("FlowBaseElement", None, "Uma ligação de um nó para o próximo.", [
        F("isGoTo", B, "53.0", "Torna o conector um Go To; padrão false."), F("targetReference", S, None, "Nó executado em seguida.", "S")]),
    "FlowCollectionMapItem": (None, "51.0", "Uma regra de mapeamento de campo numa coleção.", [
        F("assignToFieldReference", S, "51.0", "Campo que recebe o valor.", "S"),
        F("operator", "FlowAssignmentOperator", "51.0", "Operação aplicada ao campo.", "S", vals=OPS_ATR,
          notas=["Valores conforme a seção FlowAssignmentOperator."]),
        F("value", FERV, "51.0", "Valor aplicado.", "S")]),
    "FlowDataTypeMapping": ("FlowBaseElement", "48.0", "O tipo sObject concreto de um parâmetro genérico.", [
        F("apexClass", S, "61.0", "Classe Apex."), F("typeName", S, "48.0", "Nome do parâmetro; prefixo T__ na entrada e U__ na saída.", "S"),
        F("typeValue", S, "48.0", "Tipo sObject mapeado.", "S")]),
    "FlowConstant": ("FlowElement", None, "Uma constante do flow.", [
        F("dataType", "FlowDataType", None, "Tipo do valor.", "S", vals=DT_BASE),
        F("value", FERV, None, "Valor fixo; sem merge fields.")]),
    "FlowDecision": ("FlowNode", None, "Um elemento Decision: escolhe o caminho pela primeira regra verdadeira.", [
        F("attributes", "FlowAttribute[]", "65.0", "Atributos da decisão."), F("defaultConnector", CON, None, "Nó quando nenhuma regra é verdadeira."),
        F("defaultConnectorLabel", S, None, "Rótulo do caminho padrão."), F("rules", "FlowRule[]", None, "Regras, na ordem.")]),
    "FlowAttribute": (None, "65.0", "Um atributo de decisão ou de regra, como um texto para LLM.", [
        F("value", S, "65.0", "Valor do atributo."), F("type", "FlowAttributeType", "65.0", "Tipo do atributo.", vals=["LlmDescription", "LlmPrompt"])]),
    "FlowDynamicChoiceSet": ("FlowElement", None, "Um conjunto de opções gerado a partir de registros, de um picklist ou de uma coleção.", [
        F("collectionReference", S, "54.0", "Coleção usada para gerar as opções."),
        F("dataType", "FlowDataType", None, "Tipo das opções.", "S", vals=["Boolean", "Currency", "Date", "Multipicklist", "Number", "Picklist", "Record", "String", "Time"]),
        F("displayField", S, None, "Campo mostrado como rótulo.", "C:Em opções de registro."), F("filters", "FlowRecordFilter[]", None, "Filtros dos registros."),
        F("limit", I, "25.0", "Máximo de opções; padrão e máximo de 200."), F("object", S, None, "Objeto consultado.", "C:Em opções de registro."),
        F("outputAssignments", "FlowOutputFieldAssignment[]", None, "Campos do registro escolhido levados a variáveis."),
        F("picklistField", S, "35.0", "Campo picklist que fornece as opções."), F("picklistObject", S, "35.0", "Objeto do campo picklist."),
        F("sortField", S, "25.0", "Campo de ordenação."), F("sortOrder", "SortOrder", "25.0", "Direção da ordenação.", vals=ASC),
        F("valueField", S, None, "Campo guardado como valor, como o Id.")]),
    "FlowElementReferenceOrValue": (None, None, "Um valor: literal, referência a um recurso do flow ou fórmula.", [
        F("apexValue", S, None, "Valor JSON de um registro Apex."), F("booleanValue", B, None, "Valor booleano."),
        F("complexValue", S, "63.0", "Recursos e campos de uma estrutura de dados."),
        F("complexValueType", "FlowComplexValueType", "63.0", "Tipo da estrutura.", vals=["ComplexObjectFieldDetails", "JoinDefinition", "FieldReference"]),
        F("dateTimeValue", "dateTime", "30.0", "Valor de data e hora."), F("dateValue", "date", None, "Valor de data."),
        F("elementReference", S, None, "Nome de um recurso do flow."),
        F("formulaDataType", "FlowDataType", "59.0", "Tipo do resultado da fórmula.",
          vals=["Apex", "Boolean", "Currency", "Date", "DateTime", "Number", "String", "sObject", "Time"]),
        F("formulaExpression", S, "59.0", "Fórmula que transforma dados do flow."), F("numberValue", "double", None, "Valor numérico."),
        F("setupReference", S, None, "Nome de uma referência de Setup."), F("setupReferenceType", S, None, "Tipo da referência de Setup."),
        F("sobjectValue", S, None, "Valor JSON de um registro sObject."), F("stringValue", S, None, "Valor de texto."),
        F("transform", "FlowInlineTransform", "62.0", "Transformação de dados embutida."), F("transformValueReference", S, None, RES)]),
    "FlowEnd": ("FlowNode", "68.0", "Um elemento End: marca o fim de um caminho; só em flows com auto-layout. Não tem campos próprios.", []),
    "FlowExitRule": ("FlowElement", "62.0", "Uma regra de saída de um flow disparado por segmento.", [
        F("conditions", "FlowCondition[]", None, "Condições da regra."), F("label", S, None, "Rótulo da regra.", "S"),
        F("logicalOperator", S, None, "Combinação das condições.", "S", vals=["and", "or"]), F("ruleOrder", I, None, "Ordem da regra; única no flow.")]),
    "FlowExperiment": ("FlowNode", "61.0", "Um experimento: divide os registros entre caminhos.", [
        F("duration", I, "64.0", "Duração do experimento."), F("durationUnit", S, "64.0", "Unidade da duração.", vals=["Minutes", "Hours", "Days", "Weeks", "Months"]),
        F("paths", "FlowExperimentPath[]", None, "Caminhos do experimento."), F("testGroupPercentage", I, "64.0", "Percentual do grupo de teste, de 0 a 99."),
        F("type", "FlowExperimentType", None, "Tipo do experimento.", "S", vals=["Random"])]),
    "FlowExperimentPath": ("FlowElement", "61.0", "Um caminho de experimento.", [
        F("connector", CON, None, "Próximo nó."), F("label", S, None, "Rótulo do caminho.", "S"), F("percentage", I, None, "Fatia do caminho.", "S")]),
    "FlowFormula": ("FlowElement", None, "Uma fórmula do flow.", [
        F("dataType", "FlowDataType", "31.0", "Tipo do resultado; padrão Number.", vals=["Boolean", "Currency", "Date", "DateTime", "Number", "String", "Time"]),
        F("expression", S, None, "A fórmula; o retorno precisa bater com o tipo.", "S"), F("scale", I, None, "Casas decimais; só Number e Currency.")]),
    "FlowIcon": (None, "64.0", "Um ícone do Lightning Design System.", [F("iconName", "String", "64.0", "Nome do ícone.")]),
    "FlowInlineTransform": (None, "62.0", "Uma transformação de dados embutida num valor.", [
        F("apexClass", S, None, "Classe Apex dos dados transformados."),
        F("dataType", "FlowDataType", None, "Tipo dos dados transformados.", "S",
          vals=["Apex", "Boolean", "Currency", "Date", "DateTime", "Multipicklist", "Number", "Picklist", "sObject", "String", "Time"]),
        F("isCollection", B, None, "Se o valor é uma coleção; padrão false."), F("transformValues", "FlowTransformValue[]", None, "Valores da transformação.")]),
    "FlowInputFieldAssignment": ("FlowBaseElement", None, "Um valor atribuído a um campo de registro.", [
        F("field", S, None, "Campo do registro.", "S"), F("value", FERV, None, "Valor atribuído.")]),
    "FlowInputValidationRule": (None, None, "Uma validação da entrada do usuário.", [
        F("errorMessage", S, None, "Mensagem quando a validação falha.", "S"), F("formulaExpression", S, None, "Fórmula que valida a entrada.", "S")]),
    "FlowLoop": ("FlowNode", "30.0", "Um elemento Loop: percorre uma coleção.", [
        F("assignNextValueToReference", S, None, "Variável que recebe o item atual."), F("collectionReference", S, None, "Coleção percorrida."),
        F("iterationOrder", "iterationOrder", None, "Ordem da iteração.", vals=ASC), F("nextValueConnector", CON, None, "Nó para cada item."),
        F("noMoreValuesConnector", CON, None, "Nó depois do último item.")]),
    "FlowMetadataValue": (None, "31.0", "Um par nome e valor com informação de contexto.", [
        F("name", S, None, "Nome do valor.", "S"), F("value", FERV, None, "Valor ou referência.")]),
    "FlowNodeGroup": ("FlowNode", "68.0", "Um grupo de nós.", [
        F("faultConnector", CON, None, RES), F("groupType", "GroupType", None, "Tipo do grupo.", "S", vals=["generic"]),
        F("sourceBranchApiName", S, None, "Ramo de conector onde o grupo fica, como regular, default, fault ou o nome de um caminho."),
        F("sourceReference", S, None, "Nó logo antes do grupo; __Start se for o primeiro.")]),
    "FlowOrchestratedStage": ("FlowNode", "53.0", "Um estágio de orquestração, com passos e condições de saída.", [
        F("connector", CON, None, "Próximo nó."), F("exitActionInputParameters", "FlowStageStepExitActionInputParameter[]", None, "Entradas do flow de avaliação de saída."),
        F("exitActionName", S, None, "Flow de avaliação usado como condição de saída."),
        F("exitActionOutputParameters", "FlowStageStepExitActionOutputParameter[]", None, "Saídas do flow de avaliação."),
        F("exitActionType", "InvocableActionType", None, "Tipo do flow de avaliação.", vals=["EvaluationFlow"]),
        F("exitConditionLogic", S, None, LOGICA + " Também aceita Formula."), F("exitConditions", "FlowCondition[]", None, "Condições para sair do estágio."),
        F("faultConnector", CON, None, "Não usado."), F("stageSteps", "FlowStageStep[]", None, "Passos do estágio.")]),
    "FlowOutputFieldAssignment": ("FlowBaseElement", None, "Um campo de registro levado a uma variável.", [
        F("assignToReference", S, None, "Variável que recebe o valor.", "S"), F("field", S, None, "Campo do registro.", "S")]),
    "FlowRelatedRecordLookup": ("FlowBaseElement", None, "Uma busca de registros relacionados dentro de um Get Records (beta).", [
        F("filterLogic", S, None, "Lógica dos filtros."), F("filters", "FlowRecordFilter[]", None, "Critérios de seleção."),
        F("getFirstRecordOnly", B, None, "Guarda só um registro."), F("limit", FERV, None, "Máximo de registros, de 2 a 20.000."),
        F("queriedFields", "string[]", None, "Campos guardados.", notas=["A página grafa o tipo como strings[]."]),
        F("relatedObject", S, None, "Objeto relacionado."), F("relatedRecords", "FlowRelatedRecordLookup[]", None, "Buscas relacionadas aninhadas."),
        F("relationshipField", S, None, "Campo de relacionamento com o objeto relacionado."), F("sortField", S, None, "Campo de ordenação."),
        F("sortOrder", "SortOrder", None, "Direção da ordenação.", vals=ASC)]),
    "FlowRecordCreate": ("FlowNode", None, "Um elemento Create Records (cria ou faz upsert de registros).", [
        F("assignRecordIdToReference", S, None, "Variável que recebe o Id criado."), F("connector", CON, None, "Próximo nó."),
        F("doesUpsert", B, "62.0", "Cria ou atualiza; padrão false."), F("doesUpsertAllOrNone", B, "62.0", "Upsert tudo ou nada; padrão true."),
        F("faultConnector", CON, None, "Nó em caso de erro."), F("filterLogic", S, "61.0", "Lógica dos filtros."),
        F("filters", "FlowRecordFilter[]", "61.0", "Critérios dos registros criados ou atualizados."),
        F("inputAssignments", "FlowInputFieldAssignment[]", None, "Valores dos campos."), F("inputReference", S, None, "Variável de registro com os valores."),
        F("object", S, None, "Objeto criado.", "S"),
        F("operationMultMatchingRecords", S, "61.0", "O que fazer quando vários registros batem.", vals=["None", "UpdateAllRecords", "UpdateLatestRecord"]),
        F("operationOneMatchingRecord", S, "61.0", "O que fazer quando um registro bate.", vals=["None", "UpdateAllRecords"]),
        F("operationZeroMatchingRecords", S, "61.0", "O que fazer quando nenhum registro bate.", vals=["None"]),
        F("storeOutputAutomatically", B, "48.0", "Disponibiliza o Id sem variável; padrão false."),
        F("upsertExternalIdField", S, "62.0", "Campo External ID do upsert."), F("upsertStandardIdField", S, "62.0", "Campo de Id padrão do upsert.")]),
    "FlowRecordDelete": ("FlowNode", None, "Um elemento Delete Records.", [
        F("connector", CON, None, "Próximo nó."), F("faultConnector", CON, None, "Nó em caso de erro."), F("filters", "FlowRecordFilter[]", None, "Critérios dos registros excluídos."),
        F("inputReference", S, None, "Variável de registro cujo Id é excluído."), F("object", S, None, "Objeto.", "S")]),
    "FlowRecordFilter": ("FlowBaseElement", None, "Um filtro de registros.", [
        F("field", S, None, "Campo filtrado.", "S"),
        F("operator", "FlowRecordFilterOperator", None, "Operador.", "S", vals=["EqualTo", "NotEqualTo", "GreaterThan", "LessThan", "GreaterThanOrEqualTo",
                                                                          "LessThanOrEqualTo", "StartsWith", "EndsWith", "Contains", "IsNull"]),
        F("value", FERV, None, "Valor comparado.")]),
    "FlowRecordLookup": ("FlowNode", None, "Um elemento Get Records.", [
        F("assignNullValuesIfNoRecordsFound", B, "30.0", "Anula as variáveis quando nada é encontrado."), F("connector", CON, None, "Próximo nó."),
        F("faultConnector", CON, None, "Nó em caso de erro."), F("filterLogic", S, "50.0", "Lógica dos filtros."), F("filters", "FlowRecordFilter[]", None, "Critérios."),
        F("getFirstRecordOnly", B, "47.0", "Guarda só o primeiro registro."), F("limit", FERV, "63.0", "Máximo de registros, de 2 a 20.000."),
        F("object", S, None, "Objeto consultado."), F("outputAssignments", "FlowOutputFieldAssignment[]", None, "Campos levados a variáveis."),
        F("outputReference", S, None, "Variável que guarda os valores."), F("queriedFields", "string[]", None, "Campos guardados na variável de registro."),
        F("relatedRecords", "FlowRelatedRecordLookup[]", None, "Registros relacionados (beta)."), F("sortField", S, "25.0", "Campo de ordenação."),
        F("sortOrder", "SortOrder", "25.0", "Direção da ordenação.", vals=ASC), F("storeOutputAutomatically", B, "47.0", "Disponibiliza os campos sem variáveis.")]),
    "FlowRecordRollback": ("FlowNode", "52.0", "Um elemento Roll Back Records: desfaz as mudanças da transação.", [F("connector", CON, None, "Próximo nó.")]),
    "FlowRecordUpdate": ("FlowNode", None, "Um elemento Update Records.", [
        F("connector", CON, None, "Próximo nó."), F("faultConnector", CON, None, "Nó em caso de erro."), F("filters", "FlowRecordFilter[]", None, "Critérios."),
        F("inputAssignments", "FlowInputFieldAssignment[]", None, "Valores dos campos."), F("inputReference", S, None, "Variável de registro com os valores."),
        F("object", S, None, "Objeto atualizado.", "S")]),
    "FlowRule": ("FlowElement", None, "Uma regra de decisão.", [
        F("attributes", "FlowAttribute[]", "65.0", "Atributos da regra."), F("conditionLogic", S, None, LOGICA + " Até 1.000 caracteres."),
        F("conditions", "FlowCondition[]", None, "Condições."), F("connector", CON, None, "Nó quando a regra é verdadeira."),
        F("doesRequireRecordChangedToMeetCriteria", B, "50.0", "Exige que o registro passe a atender aos critérios."), F("label", S, None, "Rótulo do caminho.", "S")]),
    "FlowSchedule": (None, "47.0", "O agendamento de um flow agendado.", [
        F("dayOfMonthToRun", I, "66.0", "Dia do mês; -1 é o último dia."), F("daysOfWeekToRun", S, "66.0", "Dias da semana, de 1 (domingo) a 7 (sábado), separados por vírgula."),
        F("endDate", "date", None, RES), F("endTime", "time", None, RES),
        F("frequency", "FlowStartFrequency", None, "Frequência.", vals=["Once", "Daily", "Weekly", "OnActivate", "Hourly", "Monthly", "Weekdays", "Yearly"]),
        F("frequencyNumber", I, "66.0", "Número de execuções em flows por segmento."), F("startDate", "date", None, "Data de início."),
        F("startTime", "time", None, "Hora, no fuso padrão da org.")]),
    "FlowScheduledPath": ("FlowElement", "51.0", "Um caminho agendado de um flow disparado por registro.", [
        F("connector", CON, None, "Próximo nó."), F("label", S, None, "Rótulo do caminho."), F("maxBatchSize", I, None, "Entrevistas por lote, de 1 a 200; padrão 200."),
        F("offsetNumber", I, None, "Deslocamento; negativo antecipa."), F("offsetUnit", "FlowScheduledPathOffsetUnit", None, "Unidade do deslocamento.", vals=OFFSET),
        F("pathType", "FlowScheduledPathType", None, "Tipo do caminho; nulo ou AsyncAfterCommit.", vals=["AsyncAfterCommit"]),
        F("recordField", S, None, "Campo que define o momento."),
        F("timeSource", "FlowScheduledPathTimeSource", None, "Origem do horário.", vals=["RecordField", "RecordTriggerEvent"])]),
    "FlowScreen": ("FlowNode", None, "Um elemento Screen: uma tela do flow.", [
        F("actions", "FlowScreenAction[]", "59.0", "Ações da tela."), F("allowBack", B, "26.0", "Mostra o botão Previous."),
        F("allowFinish", B, "26.0", "Mostra o botão Finish."), F("allowPause", B, "33.0", "Mostra o botão Pause."), F("backButtonLabel", S, None, "Rótulo do botão de voltar."),
        F("connector", CON, None, "Próximo nó."), F("fields", "FlowScreenField[]", None, "Componentes da tela."), F("helpText", S, "26.0", "Texto de ajuda."),
        F("nextOrFinishButtonLabel", S, None, "Rótulo de Next ou Finish."), F("pauseButtonLabel", S, None, "Rótulo de Pause."),
        F("pausedText", S, "33.0", "Mensagem depois da pausa."),
        F("rules", "não informado na página", None, RES, natureza="desconhecida", contexto="A página não informa o tipo; o campo é reservado."),
        F("showFooter", B, "42.0", "Mostra o rodapé no Lightning."), F("showHeader", B, "42.0", "Mostra o cabeçalho no Lightning."),
        F("stageReference", FERV, None, "Estágio associado."), F("styleSettings", "FlowScreenStyleSetting[]", "66.0", "Estilos da tela."),
        F("triggers", "FlowScreenTrigger[]", "59.0", "Gatilhos de campos e atributos.")]),
    "FlowScreenAction": (None, "59.0", "Uma ação de tela.", [
        F("actionName", S, None, "Nome de API da ação.", "S"), F("actionType", "InvocableActionType", None, "Tipo da ação.", "S", vals=["flow"]),
        F("inputParameters", "FlowScreenActionInputParameter[]", None, "Entradas da ação."), F("label", S, None, "Rótulo da ação.", "S"),
        F("nameSegment", S, None, "Nome de API da ação."), F("versionString", S, "63.0", "Versão da ação.")]),
    "FlowScreenActionInputParameter": ("FlowScreenFieldInputParameter", "59.0", "Uma entrada de uma ação de tela.", INP),
    "FlowScreenField": ("FlowElement", None, "Um componente de tela: campo, texto, escolha, seção ou componente Lightning.", [
        F("choiceReferences", "string[]", "26.0", "Opções, na ordem."),
        F("dataType", "FlowDataType", "26.0", "Tipo do campo de entrada.", vals=["Boolean", "Currency", "Date", "DateTime", "Number", "String", "Time"]),
        F("dataTypeMappings", "FlowDataTypeMapping[]", None, RES), F("defaultSelectedChoiceReference", S, "26.0", "Opção padrão."),
        F("defaultValue", FERV, None, "Valor padrão."), F("extensionName", S, "42.0", "Componente Lightning mostrado."),
        F("fields", "FlowScreenField[]", "49.0", "Colunas ou campos dentro de uma seção."), F("fieldText", S, None, "Rótulo; aceita merge fields."),
        F("fieldType", "FlowScreenFieldType", None, "Tipo de componente.", "S",
          vals=["DisplayText", "InputField", "LargeTextArea", "PasswordField", "RadioButtons", "DropdownBox", "MultiSelectCheckboxes", "MultiSelectPicklist",
                "ComponentInstance", "ComponentChoice", "ComponentInput", "Region", "RegionContainer", "ObjectProvided"]),
        F("helpText", S, "26.0", "Texto do ícone de ajuda."), F("inputParameters", "FlowScreenFieldInputParameter[]", "42.0", "Entradas de componentes."),
        F("inputsOnNextNavToAssocScrn", "FlowScreenFieldInputsRevisited", "51.0", "Mantém ou refaz as entradas ao voltar à tela.", vals=["UseStoredValues", "ResetValues"]),
        F("isRequired", B, None, "O usuário precisa preencher."), F("isVisible", B, None, "A página não descreve o campo."),
        F("objectFieldReference", S, None, "Campo de objeto em componentes ObjectProvided."),
        F("outputParameters", "FlowScreenFieldOutputParameter[]", "42.0", "Saídas de componentes."),
        F("regionContainerType", "FlowRegionContainerType", "55.0", "Seção com ou sem cabeçalho.", vals=["SectionWithHeader", "SectionWithoutHeader"]),
        F("scale", I, None, "Casas decimais, de 0 a 17."), F("sourceTemplateApiName", S, "62.0", "Nome de API do template."),
        F("sourceTemplateProviderType", S, "62.0", "Quem fornece o template."), F("storeOutputAutomatically", B, "47.0", "Disponibiliza as saídas sem variáveis."),
        F("styleProperties", "FlowScreenFieldStyleProperties", "64.0", "Aparência do componente."),
        F("validationRule", "FlowInputValidationRule", None, "Validação da entrada."), F("visibilityRule", "FlowVisibilityRule", "47.0", "Quando o componente aparece.")]),
    "FlowScreenFieldInputParameter": ("FlowBaseElement", "42.0", "Uma entrada de um componente de tela.", INP),
    "FlowScreenFieldOutputParameter": ("FlowBaseElement", "42.0", "Uma saída de um componente de tela.", OUTP),
    "FlowScreenFieldStyleProperties": (None, "64.0", "A aparência de um componente de tela.", [
        F("styleSettings", "FlowScreenStyleSetting[]", "66.0", "Estilos."), F("width", FERV, "64.0", "Colunas ocupadas, de 1 a 12."),
        F("verticalAlignment", FERV, "64.0", "Alinhamento vertical: top, middle ou bottom.")]),
    "FlowScreenStyleSetting": ("FlowBaseElement", "66.0", "Um estilo de tela.", [
        F("propertyName", S, "66.0", "Nome da propriedade de estilo."), F("propertyValue", FERV, "66.0", "Valor."),
        F("scope", S, "66.0", "Onde o estilo vale.", vals=["Container", "Header", "NextOrFinish", "Previous", "Pause"])]),
    "FlowScreenTrigger": (None, "59.0", "Um gatilho de tela: responde a um evento de campo, atributo ou ação.", [
        F("eventName", S, "59.0", "Evento escutado.", "S"), F("eventSource", S, "59.0", "Onde o evento acontece.", "S"),
        F("handlers", "FlowScreenTriggerHandler[]", "59.0", "Tratadores do evento.")]),
    "FlowScreenTriggerHandler": (None, "59.0", "Um tratador de gatilho de tela.", [
        F("conditions", "FlowCondition[]", "63.0", "Condições para disparar."), F("conditionLogic", S, "63.0", LOGICA),
        F("initBehavior", S, "64.0", "Quando as ações rodam depois que a tela carrega.", vals=["runOnLoad", "runOnRevisit"]),
        F("screenActionName", S, "59.0", "Ação executada.", "S")]),
    "FlowStage": ("FlowElement", None, "Um estágio do flow, usado em indicadores de progresso.", [
        F("isActive", B, None, "Estágio ativo por padrão."), F("label", S, None, "Nome do estágio."), F("stageOrder", I, None, "Posição; única no flow.")]),
    "FlowStageStep": (None, "53.0", "Um passo de um estágio de orquestração.", [
        F("actionName", S, "53.0", "Flow do passo.", "S"),
        F("actionType", "InvocableActionType", "53.0", "Tipo do passo.", "S", vals=["stepApproval", "stepBackground", "stepInteractive", "stepMuleSoft"],
          notas=["stepApproval exige API 62.0 ou posterior."]),
        F("assignees", "FlowStageStepAssignee[]", "53.0", "Quem conclui o passo."), F("canAssigneeEdit", B, None, RES),
        F("debugSimulateStep", B, "65.0", "Roda o passo em modo de reversão."),
        F("entryActionInputParameters", "FlowStageStepEntryActionInputParameter[]", "53.0", "Entradas do flow de entrada."),
        F("entryActionName", S, "53.0", "Flow de avaliação de entrada."),
        F("entryActionOutputParameters", "FlowStageStepEntryActionOutputParameter[]", "53.0", "Saídas do flow de entrada."),
        F("entryActionType", "InvocableActionType", "53.0", "Tipo do flow de entrada.", vals=["EvaluationFlow"]),
        F("entryConditionLogic", S, "53.0", LOGICA + " Também aceita Formula."), F("entryConditions", "FlowCondition[]", "53.0", "Condições para iniciar."),
        F("exitActionInputParameters", "FlowStageStepExitActionInputParameter[]", "53.0", "Entradas do flow de saída."),
        F("exitActionName", S, "53.0", "Flow de avaliação de saída."),
        F("exitActionOutputParameters", "FlowStageStepExitActionOutputParameter[]", "53.0", "Saídas do flow de saída."),
        F("exitActionType", "InvocableActionType", "53.0", "Tipo do flow de saída.", vals=["EvaluationFlow"]),
        F("exitConditionLogic", S, "53.0", LOGICA + " Também aceita Formula."), F("exitConditions", "FlowCondition[]", "53.0", "Condições para sair."),
        F("inputParameters", "FlowStageStepInputParameter[]", "53.0", "Entradas do flow do passo."), F("label", S, "53.0", "Rótulo do passo.", "S"),
        F("outputConfigParams", "FlowStageStepOutputConfigParam[]", "65.0", "Saídas simuladas para depuração."),
        F("outputParameters", "FlowStageStepOutputParameter[]", "53.0", "Saídas do flow do passo."),
        F("requiresAsyncProcessing", B, None, "Não usado na API 63.0."),
        F("requiresMultiMemberApproval", S, "67.0", "Se a aprovação em grupo exige todos.", vals=["0", "100"]),
        F("shouldLock", B, None, RES),
        F("stepSubtype", "FlowElementSubtype", None, "Reservado para uso interno.", natureza="desconhecida", contexto="Reservado para uso interno.")]),
    "FlowStageStepAssignee": (None, "53.0", "Quem conclui um passo: usuário, grupo ou fila.", [
        F("assignee", FERV, "53.0", "Usuário, grupo ou fila."),
        F("assigneeType", "FlowStageStepAssigneeType", "53.0", "Tipo do responsável.", "S", vals=["Group", "Queue", "User", "invalid"])]),
    "FlowStageStepEntryActionInputParameter": ("FlowBaseElement", "53.0", "Uma entrada do flow de entrada de um passo.", INP),
    "FlowStageStepEntryActionOutputParameter": ("FlowBaseElement", "53.0", "Uma saída do flow de entrada de um passo.", [
        F("assignToReference", S, "53.0", RES), F("name", S, "53.0", "Nome da saída.", "S", vals=["isOrchestrationConditionMet"])]),
    "FlowStageStepExitActionInputParameter": ("FlowBaseElement", "53.0", "Uma entrada do flow de saída.", INP),
    "FlowStageStepExitActionOutputParameter": ("FlowBaseElement", "53.0", "Uma saída do flow de saída.", [
        F("assignToReference", S, "53.0", RES), F("name", S, "53.0", "Nome da saída.", "S", vals=["isOrchestrationConditionMet"])]),
    "FlowStageStepInputParameter": ("FlowBaseElement", "53.0", "Uma entrada do flow de um passo.", INP),
    "FlowStageStepOutputConfigParam": ("FlowBaseElement", "65.0", "Uma saída simulada para depurar em modo de reversão.", [
        F("name", S, "65.0", "Nome da saída simulada.", "S"), F("value", FERV, "65.0", "Valor simulado; não guarde dados pessoais.", "S")]),
    "FlowStageStepOutputParameter": ("FlowBaseElement", "53.0", "Uma saída do flow de um passo.", OUT_RES),
    "FlowStart": ("FlowNode", "47.0", "O elemento Start: como e quando o flow começa (registro, agenda, evento, segmento).", [
        F("activation", S, "63.0", "Id da ativação que dispara o flow."), F("activationTemplate", S, "66.0", "Template de pontos de contato de flows por segmento."),
        F("capabilityTypes", "FlowCapability[]", "60.0", "Capacidades que passam dados."), F("connector", CON, None, "Primeiro elemento."),
        F("conditionLogic", S, None, "Combinação das condições.", vals=["And", "Or"]), F("conditions", "FlowCondition[]", None, "Condições do gatilho."),
        F("dataGraph", S, "61.0", "Data graph usado."), F("dataLookups", "FlowDataLookup[]", "68.0", "Buscas de registros relacionados."),
        F("dataTypeMappings", "FlowDataTypeMapping[]", "63.0", "Mapeamentos de tipos genéricos."),
        F("doesRequireRecordChangedToMeetCriteria", B, "50.0", "Exige que o registro passe a atender aos critérios."),
        F("entryType", "FlowEntryType", "60.0", "Quando um indivíduo pode entrar.", vals=["AfterCompletion", "Always", "Never"]),
        F("eventName", S, "61.0", "Evento de automação que dispara o flow."),
        F("eventType", "InvocableActionType", None, "Tipo de evento que dispara o flow.", vals=[
            "exploreConversation", "externalEvent", "processWebStoreUserRgstr", "trgrOnB2cCartAbandoned", "trgrOnCustomEvent", "trgrOnEmailBounceEngagement",
            "trgrOnEmailLinkClickEngagement", "trgrOnEmailOpenEngagement", "trgrOnEmailSubscription", "trgrOnFormSubmission", "trgrOnOrderPlacement",
            "trgrOnPostOrdMktCmpnEngagement", "trgrOnReferralEventSubmission", "trgrOnSmsDeliveryFailureEngagement", "trgrOnSmsLinkClickEngagement",
            "trgrOnSmsResponseEngagement", "trgrOnSmsSubscription", "trgOnVoucherStsChgOtbdEngmt", "trgrOnWebCartAbandoned", "trgrOnWhatsAppDeliveredEngagement",
            "trgrOnWhatsAppDlvrFailureEngmt", "trgrOnWhatsAppLinkClickEngmt", "trgrOnWhatsAppReadEngagement", "trgrOnWhatsAppResponseEngmt", "trgrOnWhatsAppSubscription"]),
        F("fanOutAction", "FlowActionCall", "66.0", "Ação invocável no Start de um flow de transmissão."),
        F("filterFormula", S, "55.0", "Fórmula de filtro; só em flows disparados por registro."), F("filterLogic", S, "50.0", "Lógica dos filtros."),
        F("filters", "FlowRecordFilter[]", None, "Filtros."), F("flowRunAsUser", S, "60.0", "Usuário em nome de quem o flow roda.", vals=["TriggeringUser", "DefaultWorkflowUser"]),
        F("form", S, "59.0", "Chave do formulário que dispara o flow.", "C:Em flows disparados por formulário."),
        F("inputs", "FlowStartInputParameter[]", None, "Entradas do Start."), F("maxBatchSize", I, "67.0", "Entrevistas por lote em flows agendados, de 1 a 200."),
        F("object", S, None, "Objeto dos registros."), F("prioritizedContactPointsList", S, "66.0", "Canais em ordem de prioridade: Email, Phone."),
        F("publishSegment", B, "60.0", "Republica o segmento antes de rodar; padrão false."),
        F("recordTriggerType", "RecordTriggerType", "48.0", "Mudanças de registro que disparam o flow.", vals=["Create", "Update", "CreateAndUpdate", "Delete", "None"]),
        F("schedule", "FlowSchedule", None, "Agenda do flow agendado.", "C:Em flows agendados."),
        F("scheduledPaths", "FlowScheduledPath[]", "51.0", "Caminhos agendados."), F("segment", S, "56.0", "Segmento que dispara o flow."),
        F("sendMsgToOneContactPtPerIndv", B, "66.0", "Um ponto de contato por indivíduo; padrão false."), F("TimeZoneSidKey", S, None, RES),
        F("triggeringDataGraph", S, "63.0", "Data graph com o objeto que dispara o flow."),
        F("triggeringDataModelObjectPath", S, "63.0", "Caminho no Data Cloud até o objeto que dispara."),
        F("triggerType", "FlowTriggerType", None, "O que faz o flow rodar; sem valor, não há gatilho.", vals=[
            "Activation", "AutomationEvent", "Capability", "DataCloudDataChange", "DataGraphDataChange", "EventDrivenJourney", "ExternalSystemChange",
            "IndivRelatedRecord", "PlatformEvent", "RecordAfterSave", "RecordBeforeDelete", "RecordBeforeSave", "Scheduled", "ScheduledJourney", "Segment"],
          notas=["Vários valores exigem versões mínimas, indicadas na página."]),
        F("versionString", S, "65.0", "Versão do evento de automação.")]),
    "FlowCapability": ("FlowElement", "60.0", "Uma capacidade à qual o flow se liga.", [
        F("capabilityName", S, "60.0", "Capacidade, no formato Nome://Nome.", "S"), F("inputs", "FlowCapabilityInput[]", None, "Entradas passadas à capacidade.")]),
    "FlowCapabilityInput": ("FlowElement", "60.0", "Uma entrada de capacidade.", [
        F("capabilityInputName", S, "60.0", "Nome da entrada.", "S"),
        F("dataType", S, "60.0", "Tipo da entrada.", vals=["Boolean", "Currency", "Date", "Number", "sObject", "String"]),
        F("isCollection", B, "60.0", "Se guarda vários valores; padrão false.", "S")]),
    "FlowStartInputParameter": ("FlowBaseElement", "62.0", "Uma entrada do Start.", INP),
    "FlowStep": ("FlowNode", None, "Um elemento Step (formato antigo).", [F("connectors", "FlowConnector[]", None, "Próximos nós.")]),
    "FlowSubflow": ("FlowNode", "25.0", "Um elemento Subflow: chama outro flow.", [
        F("connector", CON, "25.0", "Próximo nó."), F("flowName", S, "25.0", "Nome de API do flow chamado, sem versão."),
        F("inputAssignments", "FlowSubflowInputAssignment[]", "25.0", "Variáveis de entrada."), F("outputAssignments", "FlowSubflowOutputAssignment[]", "25.0", "Variáveis de saída."),
        F("storeOutputAutomatically", B, "49.0", "Disponibiliza as saídas sem variáveis; padrão false.")]),
    "FlowSubflowInputAssignment": ("FlowBaseElement", "25.0", "Uma variável de entrada do flow chamado.", INP),
    "FlowSubflowOutputAssignment": ("FlowBaseElement", "25.0", "Uma variável de saída do flow chamado.", [
        F("assignToReference", S, "25.0", "Variável no flow que chama."), F("name", S, "25.0", "Variável no flow chamado.", "S")]),
    "FlowTransform": ("FlowNode", "59.0", "Um elemento Transform: converte dados de uma forma em outra.", [
        F("apexClass", S, "59.0", "Classe Apex quando o tipo é Apex."), F("connector", "FlowConnector[]", "59.0", "Próximo nó.", notas=["A página tipa como FlowConnector[]."]),
        F("dataType", "FlowDataType", None, "Tipo da saída.", "S",
          vals=["Apex", "Boolean", "Currency", "Date", "DateTime", "Number", "String", "sObject", "Time"]),
        F("isCollection", B, "59.0", "Se a saída é coleção; padrão false."), F("objectType", S, "59.0", "Objeto quando o tipo é sObject."),
        F("scale", I, "59.0", "Casas decimais, até 17."), F("storeOutputAutomatically", B, "59.0", RES),
        F("transformValues", "FlowTransformValue[]", "59.0", "Valores da transformação.")]),
    "FlowTransformValue": ("FlowBaseElement", "59.0", "Um valor de transformação.", [
        F("transformValueActions", "FlowTransformValueAction[]", "59.0", "Ações que fazem a transformação."),
        F("transformValueDescription", S, "59.0", RES), F("transformValueLabel", S, "59.0", RES), F("transformValueName", S, "59.0", RES)]),
    "FlowTransformValueAction": ("FlowBaseElement", "59.0", "Uma ação de transformação.", [
        F("actionName", S, "59.0", RES), F("actionType", "InvocableActionType", "59.0", RES, natureza="desconhecida", contexto="Reservado; a seção não lista valores."),
        F("actionVersionString", S, "59.0", RES), F("assignToReference", S, "59.0", RES),
        F("inputParameters", "FlowTransformValueActionInputParameter[]", "60.0", "Entradas da transformação."),
        F("outputFieldApiName", S, "59.0", "Campo de destino num mapeamento."),
        F("transformType", "FlowTransformValueActionType", "59.0", "Tipo de conversão.", "S",
          vals=["Count", "GetItemByIndex", "InnerJoin", "InvocableAction", "Map", "Sum"]),
        F("value", FERV, "59.0", "Valor transformado.")]),
    "FlowTransformValueActionInputParameter": (None, "60.0", "Uma entrada de ação de transformação.", [
        F("name", S, "60.0", "Chave da entrada.", vals=["aggregationField", "aggregationValues"]), F("value", FERV, "60.0", "Valor da chave.")]),
    "FlowTextTemplate": ("FlowElement", None, "Um modelo de texto com merge fields.", [
        F("isViewedAsPlainText", B, None, "Lembra a visão em texto puro; padrão false."), F("text", S, None, "Texto do modelo.")]),
    "FlowVariable": ("FlowElement", None, "Uma variável do flow.", [
        F("apexClass", S, "46.0", "Classe Apex quando o tipo é Apex."),
        F("dataType", "FlowDataType", None, "Tipo da variável.", "S",
          vals=["Apex", "Boolean", "Currency", "Date", "DateTime", "Multipicklist", "Number", "Picklist", "String", "sObject", "Time"]),
        F("isCollection", B, "30.0", "Se guarda uma coleção; padrão false."), F("isInput", B, "25.0", "Pode receber valor no início do flow."),
        F("isOutput", B, "25.0", "Pode ser lida por Visualforce e por outros flows."), F("objectType", S, None, "Objeto quando o tipo é sObject."),
        F("scale", I, None, "Casas decimais, até 17."), F("value", FERV, None, "Valor padrão; não vale para picklists.")]),
    "FlowVisibilityRule": (None, "47.0", "Quando um componente de tela aparece.", [
        F("conditionLogic", S, "47.0", LOGICA), F("conditions", "FlowCondition[]", "47.0", "Condições.")]),
    "FlowWait": ("FlowNode", "32.0", "Um elemento Wait: pausa o flow até um evento.", [
        F("defaultConnector", CON, "32.0", "Nó quando nenhum evento é verdadeiro."), F("defaultConnectorLabel", S, "32.0", "Rótulo do caminho padrão."),
        F("faultConnector", CON, "32.0", "Nó em caso de erro."), F("timeZoneId", S, "32.0", RES), F("waitEvents", "FlowWaitEvent[]", "32.0", "Eventos esperados.")]),
    "FlowWaitEvent": ("FlowElement", "32.0", "Um evento esperado por um Wait.", [
        F("associatedElement", S, "60.0", "Evento que retoma o flow."), F("automationEventName", S, "32.0", "Nome do evento de automação."),
        F("automationEventType", "InvocableActionType", "32.0", "Tipo do evento de automação.",
          vals=["exploreConversation", "trgrOnCustomEvent", "trgrOnSmsSubscription", "trgrOnEmailSubscription", "trgrOnOrderPlacement", "trgrOnFormSubmission"]),
        F("conditionLogic", S, "32.0", LOGICA), F("conditions", "FlowCondition[]", "32.0", "Condições do evento."),
        F("connector", CON, "32.0", "Nó quando este evento acontece primeiro."),
        F("eventType", S, "32.0", "Tipo do evento; define as entradas.", "S", vals=["AlarmEvent", "DateRefAlarmEvent"]),
        F("extendUntil", "Time", "32.0", RES), F("filterlogic", S, "60.0", "Lógica dos filtros."), F("filters", "FlowRecordFilter[]", "60.0", "Filtros de registros."),
        F("inputParameters", "FlowWaitEventInputParameter[]", "32.0", "Entradas do evento."),
        F("interactionType", "FlowWaitInteractionType", "62.0", "Tipo de mensagem que retoma o flow.", vals=["RcsResponse", "SmsResponse", "WhatsappResponse"]),
        F("label", S, "32.0", "Rótulo do evento.", "S"), F("object", S, "60.0", "Objeto do evento."), F("offset", I, "32.0", RES),
        F("offsetUnit", "FlowScheduledPathOffsetUnit", "32.0", RES, vals=OFFSET, notas=["Valores conforme a seção FlowScheduledPath."]),
        F("outputParameters", "FlowWaitEventOutputParameter[]", "32.0", "Valores do evento levados a variáveis."),
        F("recordTriggerType", "RecordTriggerType", "60.0", "Mudança de registro que retoma o flow.", vals=["Create", "Update", "CreateAndUpdate"])]),
    "FlowWaitEventInputParameter": ("FlowBaseElement", "32.0", "Uma entrada de evento de espera.", [
        F("name", S, "32.0", "Nome da entrada."), F("value", FERV, "32.0", "Valor.")]),
    "FlowWaitEventOutputParameter": ("FlowBaseElement", "32.0", "Uma saída de evento de espera.", OUTP),
}
LIGA_ESPECIAL = {("FlowActionCall", "actionCallPaths"): "FlowActionCallPath"}

# ---------------------------------------------------------------- montar as estruturas
usos = {}
linhas = {}
for nome, (estende, versao, o_que_e, proprios) in SEC.items():
    rows = list(proprios)
    nomes = {r[0] for r in rows}
    cadeia = HER.get(estende, [])
    if estende == "FlowScreenFieldInputParameter":
        cadeia = FBE
    for r in cadeia:
        if nome == "FlowStart" and r[0] in ("name", "label"):
            continue  # a página diz que FlowStart herda de FlowNode, menos name e label
        if r[0] not in nomes:
            nomes.add(r[0])
            kw = dict(r[5]); kw["herdada"] = DONO_HER[r[0]] if estende != "FlowScreenFieldInputParameter" else "FlowBaseElement"
            rows.append((r[0], r[1], r[2], r[3], r[4], kw))
    linhas[nome] = rows

final = {}
for nome, rows in linhas.items():
    out = []
    for (n, t, desde, desc, req, kw) in rows:
        kw = dict(kw)
        alvo = LIGA_ESPECIAL.get((nome, n)) or (t.replace("[]", "") if t.replace("[]", "") in SEC else None)
        if alvo:
            kw["estrutura"] = alvo
            usos.setdefault(alvo, set()).add("mdx:" + nome)
        out.append(P(n, t, desde, desc, req, **kw))
    final[nome] = out

TOPO = {"actionCalls": "FlowActionCall", "apexPluginCalls": "FlowApexPluginCall", "assignments": "FlowAssignment", "choices": "FlowChoice",
        "collectionProcessors": "FlowCollectionProcessor", "constants": "FlowConstant", "customErrors": "FlowCustomError",
        "customProperties": "FlowCustomProperty", "decisions": "FlowDecision", "dynamicChoiceSets": "FlowDynamicChoiceSet", "ends": "FlowEnd",
        "exitRules": "FlowExitRule", "experiments": "FlowExperiment", "formulas": "FlowFormula", "groups": "FlowNodeGroup", "loops": "FlowLoop",
        "orchestratedStages": "FlowOrchestratedStage", "processMetadataValues": "FlowMetadataValue", "recordCreates": "FlowRecordCreate",
        "recordDeletes": "FlowRecordDelete", "recordLookups": "FlowRecordLookup", "recordRollbacks": "FlowRecordRollback",
        "recordUpdates": "FlowRecordUpdate", "screens": "FlowScreen", "stages": "FlowStage", "start": "FlowStart", "steps": "FlowStep",
        "subflows": "FlowSubflow", "textTemplates": "FlowTextTemplate", "transforms": "FlowTransform", "variables": "FlowVariable", "waits": "FlowWait"}
for alvo in TOPO.values():
    usos.setdefault(alvo, set()).add("mdt:Flow")

for nome, rows in final.items():
    estende, versao, o_que_e, _ = SEC[nome]
    extra = []
    if estende:
        extra.append(f"Estende {estende}" + (" (menos name e label)" if nome == "FlowStart" else "") + "; os campos herdados estão marcados.")
    if versao:
        extra.append(f"Disponível desde a API {versao}.")
    if nome not in usos:
        raise SystemExit(f"estrutura sem uso: {nome}")
    M.struct(nome, SRC, sorted(usos[nome]), rows, o_que_e + (" " + " ".join(extra) if extra else ""))
M.emit_structs()

# ---------------------------------------------------------------- Flow: collectionFilterCriteria reservado e ligações
d = ld("metadata-types/Flow.json")
for q in d["propriedades"]:
    if q["nome"] == "collectionFilterCriteria":
        q["dominio"] = {"natureza": "desconhecida", "estado": "desconhecido",
                        "contexto": "Reservado para uso futuro; a página não descreve o tipo FlowCollectionFilterCriteria (conferido em 2026-11-17)."}
        if not any(e.get("fonte") == SRC for e in q["evidencias"]):
            q["evidencias"].append(ev(SRC))
sv("metadata-types/Flow.json", d)
# estruturas com auto-referência ou ciclo: recalcular depois de todas gravadas
for nome in final:
    LG.ligar("estruturas", nome, {}, nota="Contagem conforme a seção do subtipo na página oficial, mais os campos herdados.")
estado = LG.ligar("metadata-types", "Flow", TOPO, src=SRC,
                  nota="Universo esperado = tabela Fields da página do guia versionado 264.0 (50 campos de primeiro nível). As 94 seções de subtipo (89 viraram estruturas) foram lidas em "
                       "2026-11-17, por partes, até o fim da página (825.034 caracteres). collectionFilterCriteria é reservado e não tem seção.")

ls = ["", "-- Lista de campos transcrita da leitura (gerada por lote7o_b5_flow.py; nome | tipo)"]
for nome in final:
    ls.append(f"[{SRC}] {nome}: " + ", ".join(f"{q['nome']} | {q['tipo_tecnico']}" for q in ld(f"estruturas/{nome}.json")["propriedades"]))
ls.append(f"[{SRC}] Flow (propriedades ligadas): " + ", ".join(sorted(TOPO)) + ", collectionFilterCriteria")
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(ls) + "\n")
print("lote 7o: Flow", estado, "| estruturas", len(final))
