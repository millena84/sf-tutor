# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 2: aplica as leituras de resolução de bloqueios sobre os JSONs do catálogo (fonte da verdade).
import json, glob, os, re
import b2_mdt as M
from b1_base import ev, af
from b3_obj import field, expo, obj, rel, cob, APEX_TOOLING, cnt

BASE = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/"
CAT = BASE + "catalogo/"

def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")

# ---------------------------------------------------------------- fontes
reg = json.load(open(BASE + "fontes/registro.json"))
B = "https://developer.salesforce.com/docs/atlas.en-us.264.0."
H = "https://help.salesforce.com/s/articleView?id="
def src(id, t, u, pert, extr, ver="68.0", metodo="extracao_documental_assistida", tipo="oficial_documentacao"):
    return {"id": id, "titulo": t, "url": u, "tipo": tipo, "versao": ver, "data_verificacao": "2026-11-07", "metodo": metodo, "pertinencia": pert,
            "extracao": "fontes/extracoes/" + extr, "checagem_online": {"estado": "verificado", "nota": "Conteúdo lido em 2026-11-07 e conferido quanto ao assunto (não apenas HTTP 200)."}}
novas = [
 src("src:fieldref-user", "User (Salesforce Field Reference Guide)", "https://developer.salesforce.com/docs/atlas.en-us.sfFieldRef.meta/sfFieldRef/salesforce_field_reference_User.htm", "Lista de 200 campos do objeto User.", "fieldref-User.txt", "parte 1: 264.0 (68.0); parte 2: página sem número de versão"),
 src("src:mdapi-field-types", "Metadata Field Types", B + "api_meta.meta/api_meta/meta_field_types.htm", "Valores de DeploymentStatus, FieldType, Gender, SharingModel, StartsWith e estruturas ValueSet.", "mdapi-FieldTypes.txt"),
 src("src:tooling-objects-list", "Tooling API Objects (índice)", B + "api_tooling.meta/api_tooling/reference_objects_list.htm", "Quais objetos são expostos pela Tooling API.", "tooling-objetos-lista.txt"),
]
for n, pg in [("flow", "flow"), ("flowdefinition", "flowdefinition"), ("flexipage", "flexipage"), ("quickactiondefinition", "quickactiondefinition"), ("customtab", "customtab"), ("pathassistant", "pathassistant")]:
    novas.append(src(f"src:tooling-{n}", f"{n} (Tooling API)", B + f"api_tooling.meta/api_tooling/tooling_api_objects_{pg}.htm", f"Campos e chamadas do objeto Tooling {n}.", "tooling-varios.txt"))
for sid, t, art, pert in [
 ("help-users", "View and Manage Users", "admin_users.htm", "Caminho no Setup, edições e impossibilidade de excluir usuários."),
 ("help-perm-sets-create", "Create Permission Sets", "sf.perm_sets_create.htm", "Caminho, edições e permissões para criar permission sets."),
 ("help-psg-create", "Create a Permission Set Group", "sf.perm_set_groups_create.htm", "Caminho e edições de permission set groups."),
 ("help-psg-assign", "Assign Permission Set Groups to Users", "platform.perm_set_groups_assign.htm", "Regras de atribuição de grupos (status Updated; usuários especiais via PermissionSetAssignment)."),
 ("help-login-history", "Monitor Login History", "xcloud.users_login_history.htm", "Caminho, edições, permissões e limites da tela de histórico de login."),
 ("help-custom-object-lex", "Create a Custom Object in Lightning Experience", "sf.dev_objectcreate_task_lex.htm", "Caminho, edições e permissão para criar objetos customizados."),
 ("help-object-manager-lex", "Find Object Management Settings in Lightning Experience", "platform.extend_click_find_objectmgmt_lex.htm", "Navegação pelo Object Manager para campos e outras customizações."),
 ("help-kb-validation-rule", "Conditionally Make a Field Required in Salesforce (KB)", "000385092&type=1", "Caminho Object Manager > objeto > Validation Rules."),
 ("help-path-create", "Create a Path", "sf.path_create.htm", "Caminho Path Settings e permissões."),
 ("help-app-builder", "Create an App Page with the Lightning App Builder", "platform.lightning_app_builder_create_app_page.htm", "Caminho, edições e permissão do Lightning App Builder."),
 ("help-custom-tabs", "Create a Custom Object Tab", "platform.creating_custom_object_tabs.htm", "Caminho e edições por tipo de tab."),
 ("help-flows-quickfind", "Prepare Your Salesforce Org for Bring Your Own Channel for Messaging", "service.partner_messaging_prepare_org.htm", "Passo 'Quick Find > Flows' e permissão Manage Flow.")]:
    novas.append(src("src:" + sid, t, H + art, pert, "help-setup.txt", "sem versão (Ajuda Salesforce)", "leitura_resultado_busca", "oficial_ajuda"))
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- utilidades
def setdom(p, vals, srcid, completa="sim", contexto=None, natureza="enum_fechado"):
    d = {"natureza": natureza, "valores": [{"valor": v, "significado": s} if s else {"valor": v} for v, s in vals], "lista_completa": completa, "estado": "verificado", "evidencias": [ev(srcid)]}
    if contexto: d["contexto"] = contexto
    p["dominio"] = d
    if not any(e["fonte"] == srcid for e in p["evidencias"]): p["evidencias"].append(ev(srcid))

def recompute_mdt(m, structs_all):
    props = m["propriedades"]
    names_mdt = M.MDT_NAMES
    unres = sorted(p["nome"] for p in props if p["dominio"]["natureza"] == "tipo_composto" and "estrutura_ref" not in p and p["tipo_tecnico"].replace("[]", "") not in names_mdt)
    m["estruturas"] = sorted({p["estrutura_ref"] for p in props if "estrutura_ref" in p})
    parciais = [s for s in m["estruturas"] if structs_all[s]["cobertura"]["estrutural"]["estado"] != "completa"]
    c = m["cobertura"]
    base_nota = c["estrutural"]["nota"].split(" Primeiro nível completo;")[0].split(" Estruturas usadas ainda parciais:")[0]
    top_ok = c["estrutural"]["esperado"] is not None and c["estrutural"]["esperado"] == len(props)
    est = "completa" if (top_ok and not unres and not parciais) else "parcial"
    nota = base_nota
    if unres: nota += f" Primeiro nível completo; {len(unres)} propriedade(s) de tipo composto ainda sem estrutura detalhada: {', '.join(unres)}."
    if parciais: nota += f" Estruturas usadas ainda parciais: {', '.join(parciais)}."
    c["estrutural"].update({"estado": est, "presente": len(props), "nota": nota})
    expl = sum(1 for p in props if p["explicacao"] == "explicada")
    c["explicativa"] = {"estado": "completa" if expl == len(props) else "parcial", "esperado": len(props), "presente": expl}

def explica(p, txt):
    p["o_que_e"] = txt; p["explicacao"] = "explicada"

# ---------------------------------------------------------------- 1. User: campos da Field Reference
u = ld("objetos-api/User.json")
txt = open(BASE + "fontes/extracoes/fieldref-User.txt").read().split("nomes:")[1]
nomes_fr = txt.split()
exist = {c["nome"] for c in u["campos"]}
desc = {"Id": "Identificador do registro de usuário.", "Name": "Nome completo, composto a partir de nome e sobrenome.", "LastName": "Sobrenome do usuário.",
        "LanguageLocaleKey": "Idioma da interface do usuário.", "LocaleSidKey": "Localidade usada em formatos de data, número e moeda.", "TimeZoneSidKey": "Fuso horário do usuário.",
        "LastLoginDate": "Data e hora do último login.", "Title": "Cargo do usuário.", "Phone": "Telefone do usuário.", "MobilePhone": "Celular do usuário."}
for n in nomes_fr:
    if n in exist:
        c = next(x for x in u["campos"] if x["nome"] == n)
        if not any(e["fonte"] == "src:fieldref-user" for e in c["evidencias"]): c["evidencias"].append(ev("src:fieldref-user"))
        continue
    f = field("obj:User", n, "(a extrair)", None, None, desc.get(n), "src:fieldref-user")
    f["notas"] = ["Nome confirmado pela Field Reference; tipo e propriedades de API não constam dessa fonte."]
    u["campos"].append(f); exist.add(n)
u["campos"].sort(key=lambda c: c["nome"])
so_objref = sorted(exist - set(nomes_fr))
u["cobertura"] = cob("parcial", None, len(u["campos"]), cnt(u["campos"]),
    f"Nomes: 200 da Field Reference + {len(so_objref)} só da Object Reference ({', '.join(so_objref)}). As duas fontes não coincidem e a tabela da Object Reference é servida truncada; tipos e propriedades de API faltam para os campos vindos só da Field Reference.")
u["evidencias"] = [ev("src:objref-user"), ev("src:fieldref-user")]
for e in u["exposicoes"]:
    if e["api"] == "tooling":
        e.update({"estado": "verificado", "nota": "Listado no índice de objetos da Tooling API; a página indica suporte a campos padrão, não a campos customizados. Campos da exposição Tooling não levantados.", "evidencias": [ev("src:tooling-objects-list")]})
sv("objetos-api/User.json", u)

# exposições Tooling de outros objetos
for nome in ("Profile", "PermissionSet", "PermissionSetGroup", "PermissionSetAssignment", "RecordType"):
    o = ld(f"objetos-api/{nome}.json")
    for e in o["exposicoes"]:
        if e["api"] == "tooling":
            e.update({"estado": "verificado", "nota": "Listado no índice de objetos da Tooling API 68.0. Campos e operações dessa exposição não levantados; não presumir que sejam iguais aos da API padrão.", "evidencias": [ev("src:tooling-objects-list")]})
    sv(f"objetos-api/{nome}.json", o)
o = ld("objetos-api/LoginHistory.json")
for e in o["exposicoes"]:
    if e["api"] == "tooling":
        e.update({"estado": "nao_exposto", "nota": "Não consta do índice de objetos da Tooling API 68.0.", "evidencias": [ev("src:tooling-objects-list")]})
sv("objetos-api/LoginHistory.json", o)

# ---------------------------------------------------------------- 2. enums de CustomObject / CustomField + estruturas
FT = "src:mdapi-field-types"
co = ld("metadata-types/CustomObject.json")
SHARING = [("Private", None), ("Read", None), ("ReadSelect", None), ("ReadWrite", None), ("ReadWriteTransfer", None), ("FullAccess", None), ("ControlledByParent", None), ("ControlledByLeadOrContact", None), ("ControlledByCampaign", None)]
for p in co["propriedades"]:
    if p["nome"] == "deploymentStatus": setdom(p, [("InDevelopment", "Em desenvolvimento; oculto para usuários comuns."), ("Deployed", "Implantado e disponível.")], FT)
    if p["nome"] in ("sharingModel", "externalSharingModel"): setdom(p, SHARING, FT, contexto="Os valores aceitos variam por objeto; objetos customizados usam ReadWrite como padrão de compartilhamento segundo a página.")
    if p["nome"] == "gender": setdom(p, [("Neuter", None), ("Masculine", None), ("Feminine", None), ("AnimateMasculine", None)], FT)
    if p["nome"] == "startsWith": setdom(p, [("Consonant", None), ("Vowel", None), ("Special", None)], FT)
co["divergencias_documentais"] = [d for d in co["divergencias_documentais"] if not d.startswith("O exemplo usa Deployed")]
co["evidencias"].append(ev(FT))
cf = ld("metadata-types/CustomField.json")
FTV = ["AutoNumber", "Lookup", "MasterDetail", "MetadataRelationship", "Checkbox", "Currency", "Date", "DateTime", "Email", "EncryptedText", "Note", "ExternalLookup", "IndirectLookup", "Number", "Percent", "Phone", "Picklist", "MultiselectPicklist", "Summary", "Text", "TextArea", "LongTextArea", "Url", "Hierarchy", "File", "Html", "Location", "Time"]
sig = {"Number": "Número (a página exibe 'Number1', provável artefato de numeração; confirmar no WSDL).", "Note": "Reservado.", "File": "Reservado.", "MetadataRelationship": "Só em custom metadata types.", "ExternalLookup": "Objetos externos.", "IndirectLookup": "Objetos externos."}
cf["divergencias_documentais"] = ["Na página Metadata Field Types o valor 'Number' aparece como 'Number1'; registrado como Number com nota."]
M.struct("LookupFilter", "src:mdapi-customfield", ["mdt:CustomField"], [("active", "boolean", "S", None, "Se o filtro está ativo."), ("booleanFilter", "string", "N", None, "Lógica que combina os itens do filtro."), ("description", "string", "N", None, "Descrição do filtro."),
    ("errorMessage", "string", "N", None, "Mensagem quando o valor não atende ao filtro."), ("filterItems", "FilterItem[]", "S", None, "Condições do filtro."), ("infoMessage", "string", "N", None, "Mensagem informativa na janela de pesquisa."), ("isOptional", "boolean", "S", None, "Se o usuário pode ignorar o filtro.")], "Filtro que restringe os registros aceitos em um campo de lookup.")
M.struct("FilterItem", "src:mdapi-customfield", ["mdx:LookupFilter"], [("field", "string", "N", None, "Campo avaliado."), ("operation", "FilterOperation", "N", None, "Operador de comparação.", {"dominio": {"natureza": "enum_fechado", "lista_completa": "desconhecido", "estado": "desconhecido", "contexto": "Valores de FilterOperation não extraídos."}}),
    ("value", "string", "N", None, "Valor comparado."), ("valueField", "string", "N", None, "Campo cujo valor é comparado.")], "Uma condição de filtro.")
M.struct("ValueSet", FT, ["mdt:CustomField"], [("controllingField", "string", "N", None, "Campo que controla a picklist dependente."), ("restricted", "boolean", "N", None, "Se só aceita os valores definidos.", {"default": ("false", False, "A página declara default false.")}),
    ("valueSetDefinition", "ValueSetValuesDefinition", "N", None, "Valores locais da picklist."), ("valueSetName", "string", "N", None, "Nome do conjunto global de valores herdado."), ("valueSettings", "ValueSettings[]", "N", None, "Mapeamento entre valores dependentes e controladores.")], "Valores de uma picklist: locais ou herdados de um conjunto global.")
M.struct("ValueSetValuesDefinition", FT, ["mdx:ValueSet"], [("sorted", "boolean", "S", None, "Se os valores são ordenados alfabeticamente."), ("value", "CustomValue[]", "S", None, "Valores da picklist.")], "Definição dos valores locais de uma picklist.")
for p in cf["propriedades"]:
    if p["nome"] == "type": setdom(p, [(v, sig.get(v)) for v in FTV], FT)
    if p["nome"] in ("lookupFilter", "valueSet"): p["estrutura_ref"] = "mdx:" + p["tipo_tecnico"]
cf["evidencias"].append(ev(FT))

# ---------------------------------------------------------------- 3. Profile: subtipos lidos
PS = "src:mdapi-profile"
pr_structs = {
 "ProfileApplicationVisibility": [("application", "string", "S", None, "Nome do app."), ("default", "boolean", "S", None, "Se é o app padrão do perfil."), ("visible", "boolean", "S", None, "Se o app fica visível.")],
 "ProfileCategoryGroupVisibility": [("dataCategories", "string[]", "S", None, "Categorias de dados visíveis quando a visibilidade é CUSTOM."), ("dataCategoryGroup", "string", "S", None, "Grupo de categorias de dados."), ("visibility", "CategoryGroupVisibility", "S", None, "Nível de visibilidade.", {"vals": [("ALL", None), ("NONE", None), ("CUSTOM", None)]})],
 "ProfileApexClassAccess": [("apexClass", "string", "S", None, "Nome da classe Apex."), ("enabled", "boolean", "S", None, "Se o perfil pode executar a classe.")],
 "ProfileCustomMetadataTypeAccess": [("enabled", "boolean", "S", None, "Se os registros podem ser lidos."), ("name", "string", "S", None, "Nome do custom metadata type.")],
 "ProfileCustomPermissions": [("enabled", "boolean", "S", None, "Se a permissão personalizada está habilitada."), ("name", "string", "S", None, "Nome da permissão personalizada.")],
 "ProfileCustomSettingAccesses": [("enabled", "boolean", "S", None, "Se os registros podem ser lidos."), ("name", "string", "S", None, "Nome da configuração personalizada.")],
 "ProfileExternalDataSourceAccess": [("enabled", "boolean", "S", None, "Se a fonte externa está habilitada."), ("externalDataSource", "string", "N", None, "Nome da fonte externa.")],
 "ProfileFieldLevelSecurity": [("editable", "boolean", "S", None, "Se o campo pode ser editado."), ("field", "string", "S", None, "Campo no formato Objeto.Campo."), ("hidden", "boolean", "N", None, "Ocultação do campo (só até a 22.0).", {"ate": "22.0"}), ("readable", "boolean", "N", None, "Se o campo pode ser lido.")],
 "ProfileFlowAccess": [("enabled", "boolean", "S", None, "Se o flow pode ser acessado."), ("flow", "string", "S", None, "Nome do flow.")],
 "ProfileGenComputingSummaryDefAccess": [("configName", "string", "S", None, "Nome da configuração."), ("enabled", "boolean", "S", None, "Se o acesso está habilitado.")],
 "ProfileLayoutAssignments": [("layout", "string", "S", None, "Layout de página atribuído."), ("recordType", "string", "N", None, "Tipo de registro ao qual o layout se aplica.")],
 "ProfileObjectPermissions": [("allowCreate", "boolean", "N", None, "Permite criar registros."), ("allowDelete", "boolean", "N", None, "Permite excluir registros."), ("allowEdit", "boolean", "N", None, "Permite editar registros."), ("allowRead", "boolean", "N", None, "Permite ver registros."),
     ("modifyAllRecords", "boolean", "N", None, "Permite alterar todos os registros, ignorando o compartilhamento."), ("object", "string", "S", None, "Nome API do objeto."), ("viewAllFields", "boolean", "N", "63.0", "Permite ver todos os campos."), ("viewAllRecords", "boolean", "N", None, "Permite ver todos os registros."),
     ("revokeCreate", "boolean", "N", None, "Obsoleto.", {"ate": "26.0"}), ("revokeDelete", "boolean", "N", None, "Obsoleto.", {"ate": "26.0"}), ("revokeEdit", "boolean", "N", None, "Obsoleto.", {"ate": "26.0"}), ("revokeRead", "boolean", "N", None, "Obsoleto.", {"ate": "26.0"})],
 "ProfileApexPageAccess": [("apexPage", "string", "S", None, "Nome da página Visualforce."), ("enabled", "boolean", "S", None, "Se o perfil pode executar a página.")],
 "ProfileRecordTypeVisibility": [("default", "boolean", "S", None, "Se é o tipo de registro padrão do perfil."), ("personAccountDefault", "boolean", "N", None, "Padrão para contas pessoais."), ("recordType", "string", "S", None, "Tipo de registro no formato Objeto.Tipo."), ("visible", "boolean", "S", None, "Se o tipo fica visível.")],
 "ProfileTabVisibility": [("tab", "string", "S", None, "Nome da tab."), ("visibility", "TabVisibility", "S", None, "Visibilidade da tab.", {"vals": [("DefaultOff", None), ("DefaultOn", None), ("Hidden", None)], "completa": "desconhecido"})],
}
for n, rows in pr_structs.items():
    M.struct(n, PS, ["mdt:Profile"], rows)
pf = ld("metadata-types/Profile.json")
expl_pf = {"agentAccesses": "Agentes visíveis para usuários do perfil.", "categoryGroupVisibilities": "Visibilidade de grupos de categorias de dados.", "customMetadataTypeAccesses": "Custom metadata types cujos registros o perfil pode ler.",
           "customPermissions": "Permissões personalizadas habilitadas.", "customSettingAccesses": "Configurações personalizadas cujos registros o perfil pode ler.", "externalDataSourceAccesses": "Fontes de dados externas com identidade por usuário.",
           "flowAccesses": "Flows que o perfil pode acessar.", "genComputingSummaryDefAccesses": "Acesso a configurações de resumo aprimorado.", "loginFlows": "Fluxos de login associados ao perfil.",
           "pageAccesses": "Páginas Visualforce que o perfil pode executar.", "profileActionOverrides": "Substituições de ação por perfil (só entre 37.0 e 44.0).", "ServicePresenceStatusAccesses": "Status de presença de serviço que o perfil pode usar."}
for p in pf["propriedades"]:
    base = p["tipo_tecnico"].replace("[]", "")
    if "mdx:" + base in M.STRUCTS: p["estrutura_ref"] = "mdx:" + base
    if p["nome"] in expl_pf and p["explicacao"] == "pendente": explica(p, expl_pf[p["nome"]])
pf["cobertura"]["estrutural"]["nota"] = "Campos de primeiro nível completos conforme a página 68.0. Subtipos lidos até ProfileTabVisibility; o conteúdo servido pela documentação termina ali (~112 mil caracteres)."

# ---------------------------------------------------------------- 4. Flow: enums
fl = ld("metadata-types/Flow.json")
FE = "src:mdapi-flow"
PT = ["AppProcess", "ApprovalWorkflow", "AutoLaunchedFlow", "CheckoutFlow", "ContactRequestFlow", "CustomerLifecycle", "CustomEvent", "DigitalForm", "EvaluationFlow", "FieldServiceMobile", "FieldServiceWeb", "Flow", "FlowFeedback", "FSCLending", "IndividualObjectLinkingFlow", "InvocableProcess", "Journey", "LoginFlow", "LoyaltyManagementFlow", "Orchestrator", "PromptFlow", "RecommendationStrategy", "RoutingFlow", "Survey", "SurveyEnrich", "Workflow"]
RES = ["ActionCadenceAutolaunchedFlow", "ActionCadenceStepFlow", "ActionPlan", "CartAsyncFlow", "CartCalculateFlow", "DcvrFrameworkDataCaptureFlow", "EinsteinDecisionStudioFlow", "IdentityUserRegistrationFlow", "InsuranceAgentFlow", "InsuranceClaimsFlow", "ManagedContentFlow", "OrchestrationFlow", "SalesEntryExperienceFlow", "TransactionSecurityFlow", "UserProvisioningFlow"]
for p in fl["propriedades"]:
    if p["nome"] == "processType":
        setdom(p, [(v, None) for v in PT] + [(v, "Reservado; não usar.") for v in RES], FE, contexto="ApprovalWorkflow e LoginFlow aparecem tanto na lista principal quanto na de reservados da página.")
    if p["nome"] == "runInMode": setdom(p, [("DefaultMode", None), ("SystemModeWithSharing", None), ("SystemModeWithoutSharing", None)], FE)
    if p["nome"] == "environments": setdom(p, [("Default", None), ("Slack", None)], FE)
    if p["nome"] == "status": setdom(p, [("Active", None), ("Draft", None), ("Obsolete", None), ("InvalidDraft", None)], FE)
    if p["nome"] == "runInMode" and p["explicacao"] == "pendente": explica(p, "Modo de execução do flow quanto a permissões e compartilhamento.")
    if p["nome"] == "environments" and p["explicacao"] == "pendente": explica(p, "Ambientes em que o flow pode rodar.")
fl["divergencias_documentais"] = ["processType: ApprovalWorkflow e LoginFlow aparecem na lista principal e na lista de reservados.", "status: a primeira extração citou UnderReview; a leitura das enumerações lista só Active, Draft, Obsolete e InvalidDraft."]

# ---------------------------------------------------------------- 5. objetos Tooling novos
T = ("tooling",)
def tobj(nome, srcid, desde, chamadas, rest, rows, oq, papel, soql, extra_alertas=None, refs=None, restr=None):
    refs = refs or {}
    campos = []
    for n, t, p, d in rows:
        kw = {}
        if n in refs: kw.update(ref=refs[n][0], rel=refs[n][1])
        if n == "Metadata": kw["dominio"] = {"natureza": "tipo_composto", "estado": "verificado", "evidencias": [ev(srcid)]}
        campos.append(field("obj:" + nome, n, t, p, None, d, srcid, T, **kw))
    obj(nome, oq, papel,
        [expo("tooling", "verificado", srcid, chamadas, rest, desde, restr=restr or ["Metadata e FullName só em consultas com no máximo um registro."]),
         expo("padrao", "desconhecido", nota="Não investigado; não presumir.")],
        campos, [{"api": "tooling", "soql": soql, "endpoint": "/services/data/v68.0/tooling/query?q=...", "contexto": "Tooling API.", "validacao": "documental"}],
        APEX_TOOLING, cob("completa", len(campos), len(campos), cnt(campos), "Tabela de campos da página Tooling 68.0."), srcid, alertas=extra_alertas)

tobj("FlowDefinition", "src:tooling-flowdefinition", "34.0", ["query()", "retrieve()", "update()"], ["GET", "HEAD", "PATCH", "POST"], [
    ("ActiveVersion", "Flow", "FGNS", "Versão ativa do flow."), ("ActiveVersionId", "id", "FGNS", "Id da versão ativa."), ("Description", "string", "N", "Descrição da definição."),
    ("DeveloperName", "string", "FGS", "Nome API do flow."), ("FullName", "string", "CGN", "Nome na Metadata API."), ("LatestVersion", "Flow", "FGNS", "Versão mais recente, de qualquer status."),
    ("LatestVersionId", "id", "FGNS", "Id da versão mais recente."), ("ManageableState", "ManageableState", "FGNRS", "Estado em pacotes."), ("MasterLabel", "string", "FGNS", "Rótulo do flow."),
    ("Metadata", "FlowDefinition (Metadata API)", "CNU", "Versão ativa e descrição no formato da Metadata API."), ("NamespacePrefix", "string", "FGNS", "Namespace.")],
    "Agrupa as versões de um flow e indica qual está ativa.", "Consultar versões ativa e mais recente de cada flow.", "SELECT DeveloperName, ActiveVersionId, LatestVersionId FROM FlowDefinition",
    ["Desde a 44.0, Metadata de FlowDefinition não ativa versões; usar o objeto Flow."], {"ActiveVersionId": (["obj:Flow"], "ActiveVersion"), "LatestVersionId": (["obj:Flow"], "LatestVersion")})
tobj("Flow", "src:tooling-flow", "34.0", ["create()", "delete()", "query()", "retrieve()", "update()", "upsert()"], ["DELETE", "GET", "HEAD", "PATCH", "POST"], [
    ("ApiVersion", "double", "N", "Versão de API que controla o comportamento de execução."), ("Definition", "FlowDefinition", "FGNS", "Definição à qual a versão pertence."), ("DefinitionId", "id", "FGS", "Id da definição."),
    ("Description", "string", "FGNS", "Descrição."), ("Environments", "multipicklist", "FN", "Onde o flow pode rodar."), ("FullName", "string", "CGN", "Nome na Metadata API, com sufixo de versão opcional."),
    ("IsTemplate", "boolean", "DFGS", "Se é modelo clonável."), ("ManageableState", "ManageableState", "FGNRS", "Estado em pacotes."), ("MasterLabel", "string", "FGIS", "Rótulo do flow."),
    ("Metadata", "Flow (Metadata API)", "CNU", "Conteúdo do flow no formato da Metadata API; nulo em flows de pacote gerenciado, exceto modelos."), ("ProcessType", "picklist", "FGNS", "Tipo do flow."),
    ("RunInMode", "picklist", "FGNRS", "Modo de execução."), ("Status", "picklist", "FG", "Status da versão."), ("TimeZoneSidKey", "string", "N", "Fuso horário das execuções."), ("VersionNumber", "int", "FGS", "Número da versão.")],
    "Cada registro é uma versão de flow.", "Consultar, criar e alterar versões de flow pela Tooling API.", "SELECT Id, MasterLabel, VersionNumber, Status FROM Flow",
    refs={"DefinitionId": (["obj:FlowDefinition"], "Definition")})
tobj("FlexiPage", "src:tooling-flexipage", "31.0", ["create()", "delete()", "describeLayout()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"], ["DELETE", "GET", "HEAD", "PATCH", "POST"], [
    ("Description", "string", "FGNS", "Descrição da página."), ("DeveloperName", "string", "FGS", "Nome API da página."), ("EntityDefinitionId", "string", "FGNS", "Objeto associado; nulo para AppPage e HomePage."),
    ("FullName", "string", "CGN", "Nome na Metadata API."), ("ManageableState", "ManageableState", "FGNRS", "Estado em pacotes."), ("MasterLabel", "string", "FGS", "Rótulo."),
    ("Metadata", "FlexiPageMetadata", "CNU", "Conteúdo da página no formato da Metadata API."), ("NamespacePrefix", "string", "FGNS", "Namespace."), ("ParentFlexiPage", "string", "FGNS", "Página da qual herda comportamento."),
    ("SobjectType", "string", "FGNS", "Objeto associado (obsoleto desde a 39.0; usar EntityDefinitionId)."), ("Type", "picklist", "FGRS", "Tipo da página.")],
    "Expõe as Lightning pages pela Tooling API.", "Consultar e alterar Lightning pages programaticamente.", "SELECT DeveloperName, MasterLabel, Type FROM FlexiPage",
    ["Páginas EmailContentPage e EmailTemplatePage não podem ser recuperadas nem implantadas."], {"EntityDefinitionId": (["obj:EntityDefinition"], None)})
tobj("QuickActionDefinition", "src:tooling-quickactiondefinition", "32.0", ["create()", "delete()", "query()", "retrieve()", "update()", "upsert()"], ["DELETE", "GET", "PATCH", "POST"], [
    ("ActionSubtype", "picklist", "FGNRS", "Subtipo; só para ações LWC."), ("Description", "textarea", "FGNS", "Descrição."), ("DeveloperName", "string", "FGS", "Nome API único."),
    ("EntityDefinitionId", "string", "FGNS", "Objeto associado."), ("FullName", "string", "CGN", "Nome na Metadata API."), ("Height", "int", "FGNS", "Altura em pixels (ícone personalizado)."),
    ("IconId", "reference", "FGNS", "Ícone personalizado (recurso estático)."), ("Label", "string", "FGNS", "Rótulo exibido."), ("Language", "picklist", "DFGNRS", "Idioma da ação."),
    ("ManageableState", "ManageableState", "FGNRS", "Estado em pacotes."), ("MasterLabel", "string", "FGS", "Rótulo."), ("Metadata", "QuickAction (Metadata API)", "CNU", "Conteúdo da ação no formato da Metadata API."),
    ("NamespacePrefix", "string", "FGNS", "Namespace."), ("OptionsCreateFeedItem", "boolean", "F", "Se a conclusão cria item de feed."), ("SobjectType", "picklist", "FGRS", "Objeto associado."),
    ("StandardLabel", "picklist", "FGNRS", "Rótulo padrão."), ("SuccessMessage", "string", "FGNS", "Mensagem de sucesso."), ("TargetField", "picklist", "FGNRS", "Campo do pai no registro criado."),
    ("TargetRecordTypeId", "reference", "FGNS", "Tipo de registro do registro criado."), ("TargetSobjectType", "picklist", "FGNRS", "Objeto criado pela ação."), ("Type", "picklist", "FGRS", "Tipo da ação."), ("Width", "int", "FGNS", "Largura em pixels (ícone personalizado).")],
    "Expõe as ações rápidas pela Tooling API.", "Consultar e alterar ações rápidas programaticamente.", "SELECT DeveloperName, Label, Type, SobjectType FROM QuickActionDefinition",
    refs={"EntityDefinitionId": (["obj:EntityDefinition"], None), "TargetRecordTypeId": (["obj:RecordType"], None), "IconId": (["StaticResource"], None)})
tobj("CustomTab", "src:tooling-customtab", "33.0", ["create()", "delete()", "query()", "retrieve()", "update()"], None, [
    ("ContentId", "reference", "FGNS", "Alvo da tab (somente leitura); nulo para tabs de objeto."), ("Description", "string", "FNS", "Descrição."), ("DeveloperName", "string", "FGNS", "Nome interno."),
    ("EncodingKey", "string", "FGNS", "Codificação de URL (somente leitura; tabs de URL)."), ("FullName", "string", "CGN", "Nome da tab; formato varia por tipo e versão."), ("HasSidebar", "boolean", "DFGS", "Se exibe a barra lateral."),
    ("ManageableState", "ManageableState", "FGNRS", "Estado em pacotes."), ("MasterLabel", "string", "FGINS", "Rótulo exibido no Setup."), ("Metadata", "CustomTabMetadata", "CNU", "Conteúdo da tab no formato da Metadata API."),
    ("MotifName", "string", "FGS", "Nome do estilo da tab (somente leitura)."), ("NamespacePrefix", "string", "FGNS", "Namespace."), ("Type", "picklist", "FGRS", "Tipo de tab."), ("Url", "string", "FNS", "Página externa incorporada.")],
    "Expõe as tabs pela Tooling API.", "Consultar e alterar tabs programaticamente.", "SELECT DeveloperName, MasterLabel, Type FROM CustomTab")
tobj("PathAssistant", "src:tooling-pathassistant", "36.0", ["retrieve()", "query()"], ["DELETE", "GET", "PATCH", "POST"], [
    ("DeveloperName", "string", "FGS", "Nome API do Path."), ("FullName", "string", "GN", "Nome na Metadata API."), ("IsActive", "boolean", "DFG", "Se o Path está ativo."), ("IsDeleted", "boolean", "S", "Se está na lixeira."),
    ("IsMasterRecordType", "boolean", "DFG", "Se o Path vale para o tipo de registro principal."), ("Language", "string", "FGRS", "Idioma."), ("ManageableState", "ManageableState", "FGNRS", "Estado em pacotes."),
    ("MasterLabel", "string", "FGS", "Rótulo do Path."), ("Metadata", "PathAssistant (Metadata API)", "CNU", "Conteúdo do Path no formato da Metadata API."), ("NamespacePrefix", "string", "FGNS", "Namespace do objeto associado."),
    ("RecordTypeId", "id", "FGNS", "Tipo de registro do Path."), ("SobjectProcessField", "string", "FGRS", "Picklist que define as etapas."), ("SobjectType", "string", "FGRS", "Objeto do Path.")],
    "Expõe os Paths pela Tooling API.", "Consultar Paths programaticamente.", "SELECT DeveloperName, MasterLabel, IsActive, SobjectType FROM PathAssistant",
    refs={"RecordTypeId": (["obj:RecordType"], None)})

for rid, mdtn, objn, srcid, expl in [
    ("cor-flow-tooling", "Flow", "Flow", "src:tooling-flow", "O campo Metadata do objeto Tooling Flow traz a versão do flow no formato do tipo Flow."),
    ("cor-flexipage-tooling", "FlexiPage", "FlexiPage", "src:tooling-flexipage", "O campo Metadata do objeto Tooling FlexiPage traz a página no formato da Metadata API."),
    ("cor-quickaction-tooling", "QuickAction", "QuickActionDefinition", "src:tooling-quickactiondefinition", "O campo Metadata de QuickActionDefinition é tipado como QuickAction."),
    ("cor-customtab-tooling", "CustomTab", "CustomTab", "src:tooling-customtab", "O campo Metadata do objeto Tooling CustomTab traz a tab no formato da Metadata API."),
    ("cor-pathassistant-tooling", "PathAssistant", "PathAssistant", "src:tooling-pathassistant", "O campo Metadata do objeto Tooling PathAssistant traz o Path no formato da Metadata API.")]:
    rel(rid, "correspondencia_xml_api", {"entidade": "mdt:" + mdtn}, {"entidade": "obj:" + objn, "campo": "Metadata"}, expl, "verificado", [srcid], nat="transformada")
N1 = lambda s: af("verificado", "N:1", "Cada versão aponta para uma definição; uma definição agrupa várias versões.", [ev(s)])
rel("flow-flowdefinition", "referencia_campo", {"entidade": "obj:Flow", "campo": "DefinitionId"}, {"entidade": "obj:FlowDefinition"}, "Cada versão de flow pertence a uma definição.", "verificado", ["src:tooling-flow"], N1("src:tooling-flow"))
rel("flowdefinition-activeversion", "referencia_campo", {"entidade": "obj:FlowDefinition", "campo": "ActiveVersionId"}, {"entidade": "obj:Flow"}, "Aponta a versão ativa do flow.", "verificado", ["src:tooling-flowdefinition"], af("desconhecido"))
rel("flowdefinition-latestversion", "referencia_campo", {"entidade": "obj:FlowDefinition", "campo": "LatestVersionId"}, {"entidade": "obj:Flow"}, "Aponta a versão mais recente, de qualquer status.", "verificado", ["src:tooling-flowdefinition"], af("desconhecido"))
rel("flexipage-entitydefinition", "referencia_campo", {"entidade": "obj:FlexiPage", "campo": "EntityDefinitionId"}, {"entidade": "obj:EntityDefinition"}, "Objeto da página de registro.", "verificado", ["src:tooling-flexipage"], af("desconhecido"))
rel("quickaction-entitydefinition", "referencia_campo", {"entidade": "obj:QuickActionDefinition", "campo": "EntityDefinitionId"}, {"entidade": "obj:EntityDefinition"}, "Objeto ao qual a ação pertence.", "verificado", ["src:tooling-quickactiondefinition"], af("desconhecido"))
rel("quickaction-recordtype", "referencia_campo", {"entidade": "obj:QuickActionDefinition", "campo": "TargetRecordTypeId"}, {"entidade": "obj:RecordType"}, "Tipo de registro do registro criado pela ação.", "verificado", ["src:tooling-quickactiondefinition"], af("desconhecido"))
rel("pathassistant-recordtype", "referencia_campo", {"entidade": "obj:PathAssistant", "campo": "RecordTypeId"}, {"entidade": "obj:RecordType"}, "Cada Path vale para um tipo de registro.", "verificado", ["src:tooling-pathassistant"], af("desconhecido"))

# ---------------------------------------------------------------- 6. funcionalidades: representações, Setup e edições
def setup(v, srcs, nota):
    return af("verificado", v, nota + " Rótulos em inglês, como na Ajuda; a tradução da interface em pt-BR não foi verificada.", [ev(s) for s in srcs])
FUP = {
 "usuarios": dict(setup=setup("Setup > Quick Find: Users > Users", ["src:help-users"], "Lista de usuários."), pre=["Edições (Ajuda): Contact Manager, Essentials, Group, Professional, Enterprise, Performance, Unlimited, Developer e Database.com.", "Ver a lista: View Setup and Configuration; gerenciar: Manage Users."], ev=["src:help-users"]),
 "permission-sets": dict(setup=setup("Setup > Quick Find: Permission Sets > Permission Sets > New", ["src:help-perm-sets-create"], "Criação."), pre=["Edições (Ajuda): Essentials, Contact Manager, Professional, Group, Enterprise, Performance, Unlimited, Developer e Database.com.", "Criar: Manage Profiles and Permission Sets; atribuir: Assign Permission Sets."], ev=["src:help-perm-sets-create"]),
 "permission-set-groups": dict(setup=setup("Setup > Quick Find: Permission Set Groups > New Permission Set Group", ["src:help-psg-create"], "Criação."), pre=["Edições (Ajuda): Contact Manager, Group, Essentials, Professional, Enterprise, Performance, Unlimited, Developer e Database.com.", "Criar: Manage Profiles and Permission Sets."],
                               ev=["src:help-psg-create", "src:help-psg-assign"], alert=["Só grupos com status Updated podem ser atribuídos; usuários guest, de integração e de sistema só podem ser atribuídos pelo objeto PermissionSetAssignment (Ajuda)."]),
 "estado-e-historico-de-login": dict(setup=setup("Setup > Quick Find: Login History", ["src:help-login-history"], "Tela de histórico."), pre=["Edições (Ajuda): Contact Manager, Group, Professional, Enterprise, Performance, Unlimited e Developer.", "Monitor Login History ou Manage Users."],
                               ev=["src:help-login-history"], alert=["A tela de Setup mostra até 20.000 registros dos últimos 6 meses; o download cobre os últimos 6 meses (Ajuda). Retenção do objeto LoginHistory na API não confirmada."]),
 "objetos-customizados": dict(setup=setup("Setup > Object Manager > Create > Custom Object", ["src:help-custom-object-lex"], "Lightning Experience."), pre=["Edições (Ajuda): Contact Manager, Group, Professional, Enterprise, Performance, Unlimited e Developer.", "Customize Application."], ev=["src:help-custom-object-lex"]),
 "campos-customizados": dict(setup=setup("Setup > Object Manager > [objeto] > Fields & Relationships > New", ["src:help-object-manager-lex"], "Lightning Experience."), pre=[], ev=["src:help-object-manager-lex"]),
 "regras-de-validacao": dict(setup=setup("Setup > Object Manager > [objeto] > Validation Rules > New", ["src:help-kb-validation-rule"], "Lightning Experience (artigo da base de conhecimento)."), pre=[], ev=["src:help-kb-validation-rule"]),
 "flow": dict(setup=setup("Setup > Quick Find: Flows > Flows > New Flow", ["src:help-flows-quickfind"], "Passo citado em artigo de configuração."), pre=["Abrir, editar ou criar flows: Manage Flow."], ev=["src:help-flows-quickfind"]),
 "path": dict(setup=setup("Setup > Quick Find: Path Settings > New Path", ["src:help-path-create"], "Path Settings precisa estar habilitado."), pre=["Modify All Data ou Customize Application."], ev=["src:help-path-create"],
              alert=["Um Path por combinação de objeto, picklist e tipo de registro (Ajuda)."]),
 "lightning-pages": dict(setup=setup("Setup > Quick Find: App Builder > Lightning App Builder > New", ["src:help-app-builder"], "Criação de página."), pre=["Edições (Ajuda): Group, Essentials, Professional, Enterprise, Performance, Unlimited e Developer.", "Customize Application."], ev=["src:help-app-builder"]),
 "tabs": dict(setup=setup("Setup > Quick Find: Tabs > Tabs > New", ["src:help-custom-tabs"], "Tabs de objeto."), pre=["Edições variam por tipo de tab (Ajuda); tabs de Lightning page: todas as edições exceto Database.com."], ev=["src:help-custom-tabs"]),
}
NOVOS_OBJ = {"flow": [("Flow", "Versão de flow (Tooling)."), ("FlowDefinition", "Definição que agrupa as versões (Tooling).")], "path": [("PathAssistant", "Path consultável (Tooling).")],
             "lightning-pages": [("FlexiPage", "Página consultável (Tooling).")], "acoes-rapidas": [("QuickActionDefinition", "Ação consultável (Tooling).")], "tabs": [("CustomTab", "Tab consultável (Tooling).")]}
for p in glob.glob(CAT + "funcionalidades/*.json"):
    fid = os.path.basename(p)[:-5]
    f = json.load(open(p))
    if fid in FUP:
        x = FUP[fid]
        f["setup"] = x["setup"]
        if x["pre"]: f["pre_requisitos"] = x["pre"]
        for s in x["ev"]:
            if not any(e["fonte"] == s for e in f["evidencias"]): f["evidencias"].append(ev(s))
        f["alertas"] += x.get("alert", [])
    if fid in NOVOS_OBJ:
        f["representacoes"]["objetos_api"] += [{"ref": "obj:" + n, "papel": pp} for n, pp in NOVOS_OBJ[fid]]
        f["representacoes"]["ausencias"] = [a for a in f["representacoes"]["ausencias"] if a["tipo"] != "objeto_api"]
        for n, _ in NOVOS_OBJ[fid]:
            s = "src:tooling-" + n.lower()
            if not any(e["fonte"] == s for e in f["evidencias"]): f["evidencias"].append(ev(s))
    if fid == "usuarios":
        f["alertas"] = ["Usuários não podem ser excluídos por completo: são desativados (IsActive). A API não oferece delete() em User e a Ajuda confirma."]
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(f, fh, ensure_ascii=False, indent=2); fh.write("\n")

# ---------------------------------------------------------------- estruturas novas e recálculo de cobertura
M.emit_structs()
structs_all = {json.load(open(p))["id"]: json.load(open(p)) for p in glob.glob(CAT + "estruturas/*.json")}
# usada_por de estruturas aninhadas
for sid, s in structs_all.items():
    pass
for m, path in ((co, "metadata-types/CustomObject.json"), (cf, "metadata-types/CustomField.json"), (pf, "metadata-types/Profile.json"), (fl, "metadata-types/Flow.json")):
    recompute_mdt(m, structs_all); sv(path, m)
# coerência transitiva para os demais tipos
for p in glob.glob(CAT + "metadata-types/*.json"):
    m = json.load(open(p)); recompute_mdt(m, structs_all)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2); fh.write("\n")
print("ok")
