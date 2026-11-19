"""Lote 8c (Fase 2, resto pequeno): 32 itens de Acesso, Dados, Automação, Organização e AutoResponseRules_RuleEntry.

19 ganham explicação; 13 ficam com explicacao = "nao_encontrada" e o texto padrão (versão e release de config/versoes.json).
Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv               # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-19"
EXTR = "fontes/extracoes/lote8c-fase2-resto-pequeno.txt"
G = "https://developer.salesforce.com/docs/get_document_content/"
C.registrar_fontes([
    C.fonte("src:tooling-entitydefinition-264", "EntityDefinition (Tooling API 264.0)", G + "api_tooling/tooling_api_objects_entitydefinition.htm/en-us/264.0",
            "Descrição dos campos de EntityDefinition.", EXTR, DATA),
    C.fonte("src:tooling-fielddefinition-264", "FieldDefinition (Tooling API 264.0)", G + "api_tooling/tooling_api_objects_fielddefinition.htm/en-us/264.0",
            "Descrição do campo Metadata de FieldDefinition.", EXTR, DATA),
    C.fonte("src:objref-businesshours-264", "BusinessHours (Object Reference 264.0)", G + "object_reference/sforce_api_objects_businesshours.htm/en-us/264.0",
            "Descrição de BusinessHoursId.", EXTR, DATA),
    C.fonte("src:mdapi-assignmentrule-264", "AssignmentRules (Metadata API 264.0)", G + "api_meta/meta_assignmentrule.htm/en-us/264.0",
            "Campos de RuleEntry de AssignmentRules.", EXTR, DATA),
    C.fonte("src:mdapi-escalationrules-264", "EscalationRules (Metadata API 264.0)", G + "api_meta/meta_escalationrules.htm/en-us/264.0",
            "Campos de RuleEntry de EscalationRules.", EXTR, DATA),
    C.fonte("src:rn-fase2-busca", "Notas de versão da Salesforce: busca pelos nomes dos campos sem descrição (lote 8c)",
            "https://help.salesforce.com/s/articleView?id=release-notes.rn_automate_flow_release_update_emailsimple_invocable_action_profile_settings.htm&language=en_US&release=252&type=5",
            "Conferência por busca nas notas de versão; única pista: a release update de EmailSimple.", EXTR, DATA, tipo="oficial_ajuda",
            versao="Winter '27 (busca)", metodo="leitura_resultado_busca"),
])
V = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "config", "versoes.json"), encoding="utf-8"))["plataforma_core"]
NAO = (f"Não encontrada descrição oficial na última versão da documentação ({V['numero_interno_documentacao']}, API {V['api_version']}); "
       f"verificado também nas notas da release {V['release']} (por busca).")
RULE = "Descrição tirada da página de {p}: a página de AutoResponseRules não lista este campo no RuleEntry dela."

# arquivo -> {nome: ("explicada", fonte, texto, versão|None, nota|None) | ("nao_encontrada", fontes, None, versão|None, nota|None)}
E = "explicada"; N = "nao_encontrada"
T = {
    "objetos-api/EntityDefinition.json": {
        "Description": (E, "src:tooling-entitydefinition-264", "Descrição do objeto. Uma descrição clara ajuda a distinguir objetos customizados em list views.", "37.0", None),
        "DeveloperName": (E, "src:tooling-entitydefinition-264", "Nome interno do objeto. Não é único: para identificar um objeto sem ambiguidade, use QualifiedApiName.", None, None),
        "IsCustomizable": (E, "src:tooling-entitydefinition-264", "Indica se o objeto aceita campos customizados.", None, None),
        "IsCustomSetting": (E, "src:tooling-entitydefinition-264", "Indica se o objeto é um custom setting.", "35.0", None),
        "IsQueryable": (E, "src:tooling-entitydefinition-264", "Indica se o objeto pode ser consultado.", None, None),
        "MasterLabel": (E, "src:tooling-entitydefinition-264", "Rótulo do objeto como aparece no Setup, no idioma padrão da org (en_US, se não houver).", None, None),
        "NamespacePrefix": (E, "src:tooling-entitydefinition-264", "Prefixo de namespace do objeto. Cada org Developer Edition que cria um pacote gerenciado tem um prefixo único, de até 15 caracteres.", None, None),
    },
    "objetos-api/FieldDefinition.json": {
        "Metadata": (E, "src:tooling-fielddefinition-264", "Metadados completos do campo, no formato CustomField da Metadata API. Só pode ser consultado quando o resultado tem no máximo um registro.", None,
                     "A página oficial descreve este campo como metadados de compact layout; o tipo informado é CustomField, e a menção parece texto copiado de outro objeto."),
    },
    "objetos-api/BusinessHours.json": {
        "BusinessHoursId": (E, "src:objref-businesshours-264", "ID do BusinessHours associado ao SlaProcess (processo de entitlement), segundo a página oficial.", None, None),
    },
    "objetos-api/PermissionSet.json": {"Type": (N, None, None, "46.0", "A página 264.0 só informa que o campo existe desde a API 46.0.")},
    "objetos-api/User.json": {"UserPermissionsMobileUser": (N, None, None, None, None), "UserPreferencesSetupAssistantPrefDisabled": (N, None, None, None, None)},
    "metadata-types/Flow.json": {"segment": (N, None, None, None, "A página só mostra 'segment' dentro de FlowStart (segmento que dispara o flow).")},
    "metadata-types/ApprovalProcess.json": {"processOrder": (N, None, None, None, None)},
    "metadata-types/FlowSettings.json": {
        "enableEmailSimpleRespectProfiles": (N, None, None, None, "Pista: a release update 'Enable EmailSimple Invocable Action to Respect Organization-Wide Profile Settings' parece corresponder, mas não cita o nome do campo."),
        "enableEmailsimpleSecureProfiles": (N, None, None, None, None),
        "enableFlowReactiveChoiceOptions": (N, None, None, None, None),
        "flowOccurrenceLogging": (N, None, None, None, None),
        "isSupportRollbackOnErrorForApexInvocableActionsEnabled": (N, None, None, None, None),
    },
    "metadata-types/MyDomainSettings.json": {
        k: (N, None, None, None, "A página 264.0 tem campos de nome parecido, mas com outro nome; não foram usados como descrição.")
        for k in ("enableShareBrowserSessionAndroidForAuth", "enableShareBrowserSessionIOSForAuth", "isInstancedApiTrafficBlocked")},
    "estruturas/AutoResponseRules_RuleEntry.json": {
        "assignedTo": (E, "src:mdapi-assignmentrule-264", "Nome do usuário ou da fila a quem o item é atribuído.", None, RULE.format(p="AssignmentRules")),
        "assignedToType": (E, "src:mdapi-assignmentrule-264", "Tipo de destino da atribuição: User ou Queue.", None, RULE.format(p="AssignmentRules")),
        "notifyCcRecipients": (E, "src:mdapi-assignmentrule-264", "Se os endereços em Cc de mensagens de Email-to-Case ou Web-to-Lead recebem cópia da resposta automática.", "32.0", RULE.format(p="AssignmentRules")),
        "overrideExistingTeams": (E, "src:mdapi-assignmentrule-264", "Com true, o case team é redefinido na atribuição; com false, o time atual é mantido e o novo é acrescentado.", None, RULE.format(p="AssignmentRules")),
        "team": (E, "src:mdapi-assignmentrule-264", "Nome do case team; pode aparecer zero ou mais vezes.", None, RULE.format(p="AssignmentRules")),
        "businessHours": (E, "src:mdapi-escalationrules-264", "Horário em que as ações de escalonamento rodam; só vale quando businessHoursSource é Static.", None, RULE.format(p="EscalationRules")),
        "businessHoursSource": (E, "src:mdapi-escalationrules-264", "Origem do horário de escalonamento: None, Case ou Static.", None, RULE.format(p="EscalationRules")),
        "disableEscalationWhenModified": (E, "src:mdapi-escalationrules-264", "Indica se o escalonamento é desligado quando o registro é alterado.", None, RULE.format(p="EscalationRules")),
        "escalationAction": (E, "src:mdapi-escalationrules-264", "Ações executadas quando os critérios de escalonamento são atendidos.", None, RULE.format(p="EscalationRules")),
        "escalationStartTime": (E, "src:mdapi-escalationrules-264", "Quando o escalonamento começa a contar: na criação do caso (CaseCreation) ou na última alteração (CaseLastModified).", None, RULE.format(p="EscalationRules")),
    },
}

cont = {E: 0, N: 0}
for arq, campos in T.items():
    d = ld(arq)
    chave = "campos" if "campos" in d else "propriedades"
    for i in d[chave]:
        if i["nome"] not in campos or i.get("explicacao") not in ("pendente", N, E):
            continue
        estado, src, txt, v, nota = campos[i["nome"]]
        if estado == E and i.get("explicacao") == "explicada" and src in [e["fonte"] for e in i["evidencias"]]:
            continue  # já aplicado
        i["explicacao"] = estado
        i["o_que_e"] = txt if estado == E else NAO
        fontes = [src] if src else ["src:rn-fase2-busca"]
        for s in fontes:
            if s not in [e["fonte"] for e in i["evidencias"]]:
                i["evidencias"].append({"fonte": s})
        if v and i.get("disponibilidade", {}).get("estado") == "desconhecido":
            i["disponibilidade"] = {"desde_versao": v, "ate_versao": None, "estado": "verificado"}
        if nota:
            i["notas"] = [x for x in i.get("notas", []) if x != nota] + [nota]
        cont[estado] += 1
    cob = d.get("cobertura", {}).get("explicativa")
    if cob is not None:
        cob["presente"] = sum(1 for x in d[chave] if x.get("explicacao") == "explicada")
    sv(arq, d)
print(f"lote 8c: {cont}")
