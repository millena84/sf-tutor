# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Bootstrap: metadata types e estruturas auxiliares do piloto.
import json, re
from b1_base import save, ev, af

SNAP = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/fontes/snapshots/sdr-13.12.0/"
REG = json.load(open(SNAP + "metadataRegistry.json"))
MS = {}
for l in open(SNAP + "METADATA_SUPPORT.md", encoding="utf-8"):
    if l.startswith("|") and not l.startswith("|:") and not l.startswith("|Metadata Type"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        MS[c[0]] = (c[1], c[2] if len(c) > 2 else "")

MDT_NAMES = {"PermissionSet", "PermissionSetGroup", "Profile", "CustomObject", "CustomField", "ValidationRule", "RecordType", "Flow", "PathAssistant", "FlexiPage", "QuickAction", "CustomTab"}
PRIM = {"string", "boolean", "int", "number", "double", "dateTime", "date", "picklist", "multipicklist", "reference"}
STRUCTS = {}   # mdx id -> dict
STRUCT_SRC = {}

def dominio_auto(tipo, vals=None, natureza=None, contexto=None, completa="sim", src=None):
    e = [ev(src)] if src else None
    if vals:
        return {"natureza": natureza or "enum_fechado", "valores": [{"valor": v, "significado": s} if s else {"valor": v} for v, s in vals],
                "lista_completa": completa, "estado": "verificado", "evidencias": e, **({"contexto": contexto} if contexto else {})}
    if natureza:
        d = {"natureza": natureza, "estado": "verificado" if natureza in ("texto_livre", "referencia", "tipo_composto") else "desconhecido"}
        if contexto: d["contexto"] = contexto
        if d["estado"] == "verificado": d["evidencias"] = e
        return d
    t = tipo.replace("[]", "")
    if t == "boolean":
        return {"natureza": "booleano", "valores": [{"valor": "true"}, {"valor": "false"}], "lista_completa": "sim", "estado": "verificado", "evidencias": e}
    if t in ("int", "number", "double"):
        return {"natureza": "numerico", "estado": "verificado", "evidencias": e}
    if t == "string":
        return {"natureza": "texto_livre", "estado": "verificado", "evidencias": e,
                "contexto": "A fonte tipa como string sem lista de valores; não inventar valores."}
    if t[:1].isupper() and t not in PRIM:
        return {"natureza": "tipo_composto", "estado": "verificado", "evidencias": e}
    return {"natureza": "desconhecida", "estado": "desconhecido"}

def prop(owner, nome, tipo, req, ver, desc, src, **kw):
    """req: 'S' obrigatório (fonte); 'N' não marcado; 'C:cond' condicional; '?' desconhecido."""
    pid = f"{owner}.{nome}"
    e = [ev(src)]
    if req == "S":
        ob = {"valor": "sim", "estado": "verificado", "evidencias": e}
    elif req.startswith("C:"):
        ob = {"valor": "condicional", "condicao": req[2:], "estado": "verificado", "evidencias": e}
    elif req == "N":
        ob = {"valor": "nao", "estado": "desconhecido",
              "condicao": "A documentação 68.0 não marca o campo como obrigatório; ausência de marcação não comprova opcionalidade (confirmar no WSDL)."}
    else:
        ob = {"valor": "desconhecida", "estado": "desconhecido"}
    d = kw.get("default")
    if d is None:
        dflt = {"forma": "nao_declarado_na_fonte", "estado": "desconhecido"}
    else:
        forma, valor, nota = d
        dflt = {"forma": forma, "estado": "verificado", "evidencias": e}
        if valor is not None: dflt["valor"] = valor
        if nota: dflt["nota"] = nota
    base = tipo.replace("[]", "")
    p = {
        "id": pid, "nome": nome, "tipo_tecnico": tipo,
        "o_que_e": desc or "Explicação pendente: item listado a partir da fonte, ainda sem texto didático.",
        "origem": af("verificado", "padrao_plataforma", "Propriedade definida pelo schema da Metadata API.", e),
        "obrigatoriedade": ob, "default": dflt,
        "dominio": kw.get("dominio") or dominio_auto(tipo, kw.get("vals"), kw.get("natureza"), kw.get("contexto"), kw.get("completa", "sim"), src),
        "disponibilidade": {"desde_versao": ver, "ate_versao": kw.get("ate"), "estado": "verificado" if (ver or kw.get("ate")) else "desconhecido",
                            **({"nota": kw["nota_versao"]} if kw.get("nota_versao") else {})},
        "explicacao": "explicada" if desc else "pendente",
        "estado": kw.get("estado", "verificado"), "evidencias": e}
    if tipo.endswith("[]"): p["cardinalidade"] = "0..n"
    if kw.get("tipo_explicado"): p["tipo_explicado"] = kw["tipo_explicado"]
    if kw.get("rotulo"): p["rotulo_didatico"] = kw["rotulo"]
    if kw.get("finalidade"): p["finalidade"] = kw["finalidade"]
    if kw.get("efeito"): p["efeito"] = kw["efeito"]
    if kw.get("restr"): p["restricoes"] = af("verificado", kw["restr"], None, e)
    if kw.get("exemplo"): p["exemplo"] = kw["exemplo"]
    if kw.get("herdada"): p["herdada_de"] = kw["herdada"]
    if kw.get("notas"): p["notas"] = kw["notas"]
    if ("mdx:" + base) in STRUCTS or kw.get("estrutura"):
        p["estrutura_ref"] = "mdx:" + (kw.get("estrutura") or base)
    return p

def struct(nome, src, usada_por, rows, o_que_e=None):
    sid = "mdx:" + nome
    STRUCTS[sid] = {"nome": nome, "src": src, "usada_por": set(usada_por), "rows": rows, "o_que_e": o_que_e}

def emit_structs():
    for sid, s in sorted(STRUCTS.items()):
        props = [prop(sid, *r[:5], s["src"], **(r[5] if len(r) > 5 else {})) for r in s["rows"]]
        expl = sum(1 for p in props if p["explicacao"] == "explicada")
        save("estruturas", s["nome"], {
            "id": sid, "nome": s["nome"], "natureza": "estrutura_auxiliar",
            "o_que_e": s["o_que_e"] or "Estrutura composta usada como tipo de uma propriedade; não é um metadata type implantável por si só.",
            "usada_por": sorted(s["usada_por"]), "propriedades": props,
            "cobertura": {"estrutural": {"estado": "completa" if not [p for p in props if p["dominio"]["natureza"] == "tipo_composto" and "estrutura_ref" not in p and p["tipo_tecnico"].replace("[]", "") not in MDT_NAMES] else "parcial", "esperado": len(props), "presente": len(props), "nota": "Contagem conforme a seção do subtipo na página oficial; tipos compostos internos sem detalhe tornam a cobertura parcial."},
                          "explicativa": {"estado": "completa" if expl == len(props) else "parcial", "esperado": len(props), "presente": expl},
                          "mapeamento": {"estado": "nao_iniciada", "nota": "Correspondências com campos API não investigadas."}},
            "estado": "verificado", "evidencias": [ev(s["src"])]})

def arquivos(nome, parent=None):
    out = {}
    if parent:
        pt = REG["types"][parent.lower()]
        ch = pt["children"]["types"][nome.lower()]
        out["source_format"] = af("verificado", {"pasta": f"objects/<Objeto>/{ch['directoryName']}/", "arquivo": f"<Nome>.{ch['suffix']}-meta.xml"},
                                   "Componente filho decomposto pelo Salesforce CLI (estratégia folderPerType do tipo pai). Sufixo '-meta.xml' segue a convenção do source format.",
                                   [ev("src:sdr-registry", f"types.{parent.lower()}.children.types.{nome.lower()}")])
        out["metadata_api_format"] = af("verificado", {"pasta": f"{pt['directoryName']}/", "arquivo": f"<Objeto>.{pt['suffix']}", "elemento": "definido dentro do arquivo do tipo pai"},
                                        None, [ev("src:sdr-registry", f"types.{parent.lower()}")])
        return out
    t = REG["types"][nome.lower()]
    out["source_format"] = af("verificado", {"pasta": f"{t['directoryName']}/", "arquivo": f"<Nome>.{t['suffix']}-meta.xml"},
                              "Pasta e sufixo do registro do Salesforce CLI; sufixo '-meta.xml' segue a convenção do source format.",
                              [ev("src:sdr-registry", f"types.{nome.lower()}")])
    out["metadata_api_format"] = af("verificado", {"pasta": f"{t['directoryName']}/", "arquivo": f"<Nome>.{t['suffix']}"}, None,
                                    [ev("src:sdr-registry", f"types.{nome.lower()}")])
    if t.get("strategies", {}).get("decomposition"):
        out["decomposicao"] = af("verificado", t["strategies"], "No source format, componentes filhos ficam em subpastas por tipo.", [ev("src:sdr-registry", f"types.{nome.lower()}.strategies")])
    return out

def suporte(nome):
    st, nota = MS.get(nome, (None, None))
    if st is None:
        return af("desconhecido", None, "Tipo não encontrado em METADATA_SUPPORT.md.")
    m = {"✅": "suportado", "⚠️": "suportado_com_ressalvas", "❌": "nao_suportado_pelo_cli"}[st]
    return af("verificado", {"status": m, "nota_fonte": nota or None}, "Suporte do Salesforce CLI (source-deploy-retrieve), não do Metadata API em geral.", [ev("src:sdr-metadata-support")])

def mdt(nome, src, o_que_e, finalidade, desde, rows, parent=None, exemplo=None, estende="Metadata", setup=None,
        cobertura_nota=None, completa=True, alertas=None, recs=None, divergencias=None, curinga=None, extra_props=None):
    props = [prop("mdt:" + nome, *r[:5], src, **(r[5] if len(r) > 5 else {})) for r in rows]
    if extra_props: props += extra_props
    used = sorted({p["estrutura_ref"] for p in props if "estrutura_ref" in p})
    expl = sum(1 for p in props if p["explicacao"] == "explicada")
    unres = sorted(p["nome"] for p in props if p["dominio"]["natureza"] == "tipo_composto" and "estrutura_ref" not in p and p["tipo_tecnico"].replace("[]", "") not in MDT_NAMES)
    arq = arquivos(nome, parent)
    if curinga is not None:
        arq["curinga_package_xml"] = af("verificado", curinga, None, [ev(src)])
    obj = {
        "id": "mdt:" + nome, "nome": nome, "o_que_e": o_que_e, "finalidade": finalidade, "estende": estende,
        "arquivos": arq,
        "disponibilidade": {"desde_versao": desde, "ate_versao": None, "estado": "verificado"},
        "suporte_cli": suporte(nome),
        "setup": setup or af("desconhecido", None, "Caminho no Setup não validado nesta sessão."),
        "propriedades": props, "estruturas": used,
        "cobertura": {
            "estrutural": {"estado": "completa" if (completa and not unres) else "parcial", "esperado": len(props) if completa else None, "presente": len(props),
                           "nota": (cobertura_nota or "Universo esperado = tabela Fields da página oficial 68.0 (mais fullName herdado quando declarado).")
                                   + (f" Primeiro nível completo; {len(unres)} propriedade(s) de tipo composto ainda sem estrutura detalhada: {', '.join(unres)}." if unres else "")},
            "explicativa": {"estado": "completa" if expl == len(props) else "parcial", "esperado": len(props), "presente": expl},
            "mapeamento": {"estado": "parcial", "nota": "Correspondências registradas apenas onde há evidência; demais pendentes."}},
        "recomendacoes": recs or [], "alertas": alertas or [], "divergencias_documentais": divergencias or [],
        "estado": "verificado", "evidencias": [ev(src), ev("src:sdr-registry"), ev("src:sdr-metadata-support")]}
    if parent: obj["componente_filho_de"] = "mdt:" + parent
    if exemplo: obj["exemplo_xml"] = {"xml": exemplo, "natureza": "didatico_projeto", "nota": "Exemplo escrito pelo projeto apenas com elementos documentados; sem dados reais."}
    for sid in used:
        if sid in STRUCTS: STRUCTS[sid]["usada_por"].add("mdt:" + nome)
    save("metadata-types", nome, obj)
    return obj

FULLNAME_HERDADO = lambda src, desc="Nome completo (API name) do componente; herdado do tipo Metadata.": ("fullName", "string", "?", None, desc, {"herdada": "Metadata"})

NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'

def build():
    # ------------------------- PermissionSet -------------------------
    S = "src:mdapi-permissionset"
    for nome, rows, oq in [
        ("PermissionSetAgentAccess", [("agentName","string","S",None,"Nome do agente de funcionário."),("enabled","boolean","S",None,"Se os usuários atribuídos podem usar o agente.")], None),
        ("PermissionSetGenComputingSummaryDefAccess", [("configName","string","S",None,"Nome da configuração de resumo aprimorado."),("enabled","boolean","S",None,"Se o acesso à configuração está habilitado.")], None),
        ("PermissionSetApplicationVisibility", [("application","string","S",None,"Nome do app."),("visible","boolean","S",None,"Se o app fica visível para os usuários atribuídos.")], None),
        ("PermissionSetApexClassAccess", [("apexClass","string","S",None,"Nome da classe Apex."),("enabled","boolean","S",None,"Se os usuários podem executar os métodos da classe de nível superior.")], None),
        ("PermissionSetCustomMetadataTypeAccess", [("enabled","boolean","S",None,"Se os registros do custom metadata type podem ser lidos."),("name","string","S",None,"Nome do custom metadata type.")], None),
        ("PermissionSetCustomPermissions", [("enabled","boolean","S",None,"Se a permissão personalizada está habilitada."),("name","string","S",None,"Nome da permissão personalizada.")], None),
        ("PermissionSetCustomSettingAccesses", [("enabled","boolean","S",None,"Se os registros da configuração personalizada podem ser lidos."),("name","string","S",None,"Nome da configuração personalizada.")], None),
        ("PermissionSetEmailRoutingAddressAccess", [("enabled","boolean","S",None,"Se o endereço de roteamento de e-mail está habilitado."),("name","string","S",None,"Nome do endereço de roteamento.")], None),
        ("PermissionSetExternalCredentialPrincipalAccess", [("enabled","boolean","S",None,"Se o acesso ao principal da credencial externa está habilitado."),("externalCredentialPrincipal","string","S",None,"Credencial externa e principal, unidos por hífen.")], None),
        ("PermissionSetExternalDataSourceAccess", [("enabled","boolean","S",None,"Se a fonte de dados externa está habilitada."),("externalDataSource","string","N",None,"Nome da fonte de dados externa.")], None),
        ("PermissionSetFieldPermissions", [("editable","boolean","S",None,"Se os usuários podem editar o campo."),("field","string","S",None,"Nome API do campo, no formato Objeto.Campo."),("readable","boolean","N",None,"Se os usuários podem ler o campo.")], None),
        ("PermissionSetFlowAccess", [("enabled","boolean","S",None,"Se os usuários podem acessar o flow.",{"default":("false",False,"A página declara default false.")}),("flow","string","S",None,"Nome do flow.")], None),
        ("PermissionSetObjectPermissions", [("allowCreate","boolean","S",None,"Permite criar registros do objeto."),("allowDelete","boolean","S",None,"Permite excluir registros do objeto."),("allowEdit","boolean","S",None,"Permite editar registros do objeto."),("allowRead","boolean","S",None,"Permite ver registros do objeto."),("modifyAllRecords","boolean","S",None,"Permite ver, editar e excluir todos os registros, ignorando o compartilhamento."),("object","string","S",None,"Nome API do objeto."),("viewAllFields","string","N","63.0","Permite ver todos os campos do objeto.",{"notas":["A página exibe o tipo como string; conferir no WSDL."]}),("viewAllRecords","boolean","S",None,"Permite ver todos os registros, ignorando o compartilhamento.")], "Permissões de um objeto concedidas pelo permission set; cada objeto aparece em um elemento <objectPermissions>."),
        ("PermissionSetApexPageAccess", [("apexPage","string","S",None,"Nome da página Visualforce."),("enabled","boolean","S",None,"Se os usuários podem executar a página.")], None),
        ("PermissionSetRecordTypeVisibility", [("recordType","string","S",None,"Nome do tipo de registro, no formato Objeto.Tipo."),("visible","boolean","S",None,"Se o tipo de registro fica visível.")], None),
        ("PermissionSetTabSetting", [("tab","string","S",None,"Nome da tab."),("visibility","PermissionSetTabVisibility","S",None,"Visibilidade da tab.",{"vals":[("Available","A tab aparece em Todas as tabs e pode ser exibida em qualquer app."),("None","A tab não aparece em Todas as tabs nem em apps."),("Visible","A tab aparece em Todas as tabs e entre as tabs visíveis do app.")]})], None),
        ("PermissionSetUserPermission", [("enabled","boolean","S",None,"Se a permissão está habilitada."),("name","string","S",None,"Nome da permissão de usuário.")], None),
        ("PermissionSetServicePresenceStatusAccess", [("servicePresenceStatus","string","S",None,"Nome do status de presença de serviço."),("enabled","boolean","S",None,"Se o status pode ser usado.")], None)]:
        struct(nome, S, ["mdt:PermissionSet"], rows, oq)
    mdt("PermissionSet", S,
        "Definição implantável de um permission set: o conjunto de permissões que pode ser somado ao perfil de um usuário.",
        "Versionar e implantar entre orgs as permissões de um permission set. A atribuição a usuários não faz parte deste XML.", "22.0", [
        FULLNAME_HERDADO(S),
        ("agentAccesses","PermissionSetAgentAccess[]","N","63.0","Agentes visíveis para usuários com este permission set."),
        ("applicationVisibilities","PermissionSetApplicationVisibility[]","N","29.0","Apps visíveis para os usuários atribuídos.",{"nota_versao":"Apps padrão a partir da 30.0."}),
        ("classAccesses","PermissionSetApexClassAccess[]","N","23.0","Classes Apex cujos métodos os usuários podem executar."),
        ("customMetadataTypeAccesses","PermissionSetCustomMetadataTypeAccess[]","N","47.0","Custom metadata types cujos registros os usuários podem ler."),
        ("customPermissions","PermissionSetCustomPermissions[]","N","31.0","Permissões personalizadas habilitadas."),
        ("customSettingAccesses","PermissionSetCustomSettingAccesses[]","N","47.0","Configurações personalizadas cujos registros os usuários podem ler."),
        ("description","string","N",None,"Descrição do permission set.",{"restr":"Até 255 caracteres."}),
        ("emailRoutingAddressAccesses","PermissionSetEmailRoutingAddressAccess[]","N","62.0","Permissões de endereços de roteamento de e-mail."),
        ("externalCredentialPrincipalAccesses","PermissionSetExternalCredentialPrincipalAccess[]","N","59.0","Principais de credenciais externas que os usuários podem usar em chamadas externas."),
        ("externalDataSourceAccesses","PermissionSetExternalDataSourceAccess[]","N","27.0","Fontes de dados externas com identidade por usuário."),
        ("fieldPermissions","PermissionSetFieldPermissions[]","N","23.0","Campos que os usuários podem ler ou editar."),
        ("flowAccesses","PermissionSetFlowAccess[]","N","47.0","Flows que os usuários podem acessar."),
        ("genComputingSummaryDefAccesses","PermissionSetGenComputingSummaryDefAccess[]","N","66.0","Acesso a configurações de resumo aprimorado."),
        ("hasActivationRequired","boolean","N","37.0","Indica se o permission set só vale com uma sessão ativa associada.",{"rotulo":"Exige ativação de sessão"}),
        ("label","string","S",None,"Nome visível do permission set.",{"restr":"Até 80 caracteres.","rotulo":"Nome visível","exemplo":"<label>Gestão de Contratos</label>"}),
        ("license","string","N","38.0","Licença de permission set ou de usuário associada; substitui userLicense."),
        ("objectPermissions","PermissionSetObjectPermissions[]","N","23.0","Permissões de criar, ler, editar e excluir por objeto."),
        ("pageAccesses","PermissionSetApexPageAccess[]","N","23.0","Páginas Visualforce que os usuários podem executar."),
        ("recordTypeVisibilities","PermissionSetRecordTypeVisibility[]","N","29.0","Tipos de registro visíveis; inativos não são retornados."),
        ("ServicePresenceStatusAccesses","PermissionSetServicePresenceStatusAccess[]","N","64.0","Status de presença de serviço que os usuários podem usar.",{"notas":["Grafia com S maiúsculo conforme a página; confirmar no WSDL."]}),
        ("tabSettings","PermissionSetTabSetting[]","N","26.0","Configurações de visibilidade de tabs.",{"notas":["A página exibe o tipo como PermissionSetTabVisibility e a seção como PermissionSetTabSetting; conferir no WSDL."]}),
        ("userLicense","string","N",None,"Licença de usuário (obsoleto; substituído por license).",{"ate":"37.0"}),
        ("userPermissions","PermissionSetUserPermission[]","N","29.0","Permissões de app ou de sistema e se estão habilitadas.",{"notas":["Desde a 40.0, permissão não informada equivale a desabilitada, segundo a página."]}),
    ], exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<PermissionSet {NS}>\n    <description>Permite ler e editar contratos.</description>\n    <hasActivationRequired>false</hasActivationRequired>\n    <label>Gestão de Contratos</label>\n    <objectPermissions>\n        <allowCreate>false</allowCreate>\n        <allowDelete>false</allowDelete>\n        <allowEdit>true</allowEdit>\n        <allowRead>true</allowRead>\n        <modifyAllRecords>false</modifyAllRecords>\n        <object>Contract</object>\n        <viewAllRecords>false</viewAllRecords>\n    </objectPermissions>\n</PermissionSet>',
        alertas=["A atribuição a usuários é registro do objeto PermissionSetAssignment, não parte do XML."],
        divergencias=["Tipo de tabSettings e de viewAllFields exibidos de forma inconsistente na página; conferir no WSDL."])

    # ------------------------- PermissionSetGroup -------------------------
    S = "src:mdapi-permissionsetgroup"
    mdt("PermissionSetGroup", S, "Definição implantável de um grupo de permission sets.", "Versionar a composição do grupo e os permission sets de silenciamento.", "45.0", [
        FULLNAME_HERDADO(S),
        ("description","string","N",None,"Descrição do grupo."),
        ("hasActivationRequired","boolean","N","53.0","Indica se o grupo exige sessão ativa.",{"default":("false",False,"A página declara default false.")}),
        ("label","string","S",None,"Nome visível do grupo."),
        ("mutingPermissionSets","string","N","46.0","Permission set de silenciamento que desliga permissões dentro do grupo.",{"natureza":"referencia","contexto":"Nome de um permission set de silenciamento existente na org."}),
        ("permissionSets","string","N",None,"Permission sets incluídos no grupo.",{"natureza":"referencia","contexto":"Nomes de permission sets existentes na org."}),
        ("status","string","N",None,"Estado de recálculo do grupo.",{"vals":[("Updated","Grupo atualizado."),("Outdated","Grupo precisa de recálculo."),("Updating","Grupo em recálculo."),("Failed","O último recálculo falhou.")]}),
    ], exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<PermissionSetGroup {NS}>\n    <description>Permissões do papel de analista de crédito.</description>\n    <label>Analista de Crédito</label>\n    <permissionSets>Gestao_de_Contratos</permissionSets>\n</PermissionSetGroup>')

    # ------------------------- Profile -------------------------
    S = "src:mdapi-profile"
    struct("ProfileLoginIpRange", S, ["mdt:Profile"], [("description","string","N",None,"Descrição da faixa."),("endAddress","string","S",None,"Último endereço IP da faixa."),("startAddress","string","S",None,"Primeiro endereço IP da faixa.")], "Faixa de endereços IP de onde usuários do perfil podem entrar.")
    pr = [("agentAccesses","ProfileAgentAccess[]","N","63.0",None),("applicationVisibilities","ProfileApplicationVisibility[]","N",None,"Apps visíveis para o perfil."),("categoryGroupVisibilities","ProfileCategoryGroupVisibility[]","N","41.0",None),
          ("classAccesses","ProfileApexClassAccess[]","N",None,"Classes Apex que o perfil pode executar."),("custom","boolean","N","30.0","Indica se o perfil é customizado em vez de padrão."),("customMetadataTypeAccesses","ProfileCustomMetadataTypeAccess[]","N","47.0",None),
          ("customPermissions","ProfileCustomPermissions[]","N","31.0",None),("customSettingAccesses","ProfileCustomSettingAccesses[]","N","47.0",None),("description","string","N","30.0","Descrição do perfil.",{"restr":"Até 255 caracteres."}),
          ("externalDataSourceAccesses","ProfileExternalDataSourceAccess[]","N","27.0",None),("fieldLevelSecurities","ProfileFieldLevelSecurity[]","N",None,"Segurança de campo (usado até a 22.0).",{"ate":"22.0"}),
          ("fieldPermissions","ProfileFieldLevelSecurity[]","N","23.0","Campos que o perfil pode ler ou editar."),("flowAccesses","ProfileFlowAccess[]","N","47.0",None),("genComputingSummaryDefAccesses","ProfileGenComputingSummaryDefAccess[]","N","66.0",None),
          ("fullName","string","S",None,"Nome do perfil; obrigatório em create, update e delete.",{"herdada":"Metadata"}),("layoutAssignments","ProfileLayoutAssignments[]","N",None,"Layouts de página atribuídos por objeto e tipo de registro."),("loginFlows","LoginFlow[]","N",None,None),
          ("loginHours","ProfileLoginHours[]","N","25.0","Horários em que usuários do perfil podem entrar."),("loginIpRanges","ProfileLoginIpRange[]","N","17.0","Faixas de IP de onde usuários do perfil podem entrar."),
          ("objectPermissions","ProfileObjectPermissions[]","N",None,"Permissões por objeto."),("pageAccesses","ProfileApexPageAccess[]","N",None,None),("profileActionOverrides","ProfileActionOverride[]","N","37.0",None,{"ate":"44.0"}),
          ("recordTypeVisibilities","ProfileRecordTypeVisibility[]","N",None,"Tipos de registro visíveis."),("ServicePresenceStatusAccesses","ProfileServicePresenceStatusAccess[]","N","64.0",None),("tabVisibilities","ProfileTabVisibility[]","N",None,"Visibilidade de tabs."),
          ("userLicense","string","N","17.0","Licença de usuário que define o conjunto base de recursos do perfil."),("userPermissions","ProfileUserPermission[]","N","29.0","Permissões de usuário habilitadas, como acesso à API.")]
    mdt("Profile", S, "Definição implantável de um perfil: permissões base e configurações que só existem no perfil, como horários e IPs de login.",
        "Versionar permissões e configurações de perfil entre orgs.", "10.0", pr,
        exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<Profile {NS}>\n    <custom>true</custom>\n    <loginIpRanges>\n        <description>Rede do escritório</description>\n        <endAddress>203.0.113.255</endAddress>\n        <startAddress>203.0.113.0</startAddress>\n    </loginIpRanges>\n    <userLicense>Salesforce</userLicense>\n</Profile>',
        completa=True, cobertura_nota="Campos de primeiro nível completos conforme a página 68.0; subtipos após ProfileObjectPermissions não foram lidos (página truncada na extração).",
        alertas=["O conteúdo recuperado de um perfil depende dos demais componentes incluídos no mesmo retrieve (documentado na página do tipo; trecho não relido nesta sessão)."])

    # ------------------------- CustomObject -------------------------
    S = "src:mdapi-customobject"
    co = [("actionOverrides","ActionOverride[]","N","18.0","Substituições de ações padrão do objeto."),("allowInChatterGroups","boolean","N","34.0","Se registros podem ser adicionados a grupos do Chatter."),
          ("businessProcesses","BusinessProcess[]","N","17.0","Processos de negócio do objeto."),("compactLayoutAssignment","string","N","29.0","Layout compacto atribuído ao objeto."),("compactLayouts","CompactLayout[]","N","29.0","Layouts compactos do objeto."),
          ("customHelp","string","N","14.0","S-control com ajuda personalizada."),("customHelpPage","string","N","16.0","Página Visualforce com ajuda personalizada."),
          ("customSettingsType","CustomSettingsType","N","17.0","Marca o objeto como configuração personalizada e seu tipo.",{"vals":[("List","Dados estáticos para toda a org."),("Hierarchy","Valores por hierarquia (org, perfil, usuário).")],"default":("valor","Hierarchy","A página declara Hierarchy como default.")}),
          ("customSettingsVisibility","CustomSettingsVisibility","N","17.0","Visibilidade de uma configuração personalizada.",{"ate":"33.0","vals":[("Public","Acessível em orgs assinantes."),("Protected","Só na org do desenvolvedor.")],"default":("valor","Protected","A página declara Protected como default.")}),
          ("dataStewardGroup","string","N",None,"Campo removido (responsável de dados por grupo).",{"ate":"46.0","nota_versao":"Removido na 47.0."}),("dataStewardUser","string","N",None,"Campo removido (responsável de dados por usuário).",{"ate":"46.0","nota_versao":"Removido na 47.0."}),
          ("deploymentStatus","DeploymentStatus","N",None,"Situação de implantação do objeto.",{"natureza":"enum_fechado","contexto":"Valores não listados na página de CustomObject; ver tipo DeploymentStatus.","dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Valores não listados na página de CustomObject. EntityDefinition.DeploymentStatus (Tooling) lista InDevelopment e Deployed, mas equivalência não foi comprovada."}}),
          ("deprecated","boolean","N",None,"Reservado; marca objeto obsoleto em pacote gerenciado."),("description","string","N",None,"Descrição do objeto.",{"restr":"Até 1000 caracteres."}),
          ("enableActivities","boolean","N",None,"Habilita atividades; não disponível para objetos externos."),("enableBulkApi","boolean","N","31.0","Parte da classificação de app corporativo; exige compartilhamento e Streaming API."),
          ("enableDivisions","boolean","N",None,"Habilita divisões no objeto."),("enableEnhancedLookup","boolean","N",None,"Habilita a pesquisa avançada; exige objeto pesquisável."),("enableFeeds","boolean","N","18.0","Habilita o rastreamento de feed do Chatter."),
          ("enableHistory","boolean","N",None,"Habilita o histórico de campos."),("enableLicensing","boolean","N","45.0","Exige licença de permission set para o objeto."),("enableReports","boolean","N",None,"Habilita relatórios sobre o objeto."),
          ("enableSearch","boolean","N","35.0","Torna os registros pesquisáveis; desligado por padrão em objetos novos."),("enableSharing","boolean","N","31.0","Parte da classificação de app corporativo; exige Bulk API e Streaming API."),
          ("enableStreamingApi","boolean","N","31.0","Parte da classificação de app corporativo; exige Bulk API e compartilhamento."),
          ("eventType","PlatformEventType","N","41.0","Tipo de evento de plataforma.",{"vals":[("HighVolume","Evento de alto volume."),("StandardVolume","Obsoleto; uso retorna erro.")]}),
          ("externalDataSource","string","C:Obrigatório para objetos externos.","32.0","Fonte de dados externa que guarda os dados."),("externalName","string","C:Obrigatório para objetos externos.","32.0","Nome da tabela no sistema externo."),
          ("externalRepository","string","N","32.0","Referência de URL de exibição do Salesforce Connect."),("externalSharingModel","SharingModel","N","31.0","Padrão de compartilhamento para usuários externos.",{"dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Valores de SharingModel não listados nesta página."}}),
          ("fields","CustomField[]","N",None,"Campos do objeto.",{"notas":["No formato Metadata API cada item aparece como <fields>; não existe tag <CustomField> dentro de <fields>."]}),("fieldSets","FieldSet","N",None,"Conjunto de campos do objeto."),
          ("fullName","string","S",None,"Nome completo do objeto; obrigatório em create, update e delete.",{"herdada":"Metadata"}),("gender","Gender","N",None,"Gênero gramatical do nome do objeto, para traduções.",{"dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Valores não listados nesta página."}}),
          ("household","boolean","N",None,"Suporte a grupos de relacionamento (Wealth Management)."),("historyRetentionPolicy","HistoryRetentionPolicy","N",None,"Reservado para uso futuro."),
          ("indexes","Index[]","N",None,"Índices de big object."),("label","string","N",None,"Rótulo do objeto; deve ser único na org."),("listViews","ListView[]","N",None,"Visualizações de lista."),
          ("namedFilter","NamedFilter[]","N","17.0","Antigo filtro de pesquisa, hoje em CustomField.",{"ate":"29.0","nota_versao":"Removido na 30.0."}),
          ("nameField","CustomField","C:Obrigatório para objetos customizados.",None,"Campo que guarda o nome do registro."),("pluralLabel","string","C:A página indica que é exigido para objetos customizados.",None,"Rótulo no plural."),
          ("profileSearchLayouts","ProfileSearchLayouts","N","47.0","Layouts de resultado de busca por perfil."),
          ("publishBehavior","PlatformEventPublishBehavior","N","46.0","Quando mensagens de evento de plataforma são publicadas.",{"vals":[("PublishAfterCommit","Publica após o commit da transação."),("PublishImmediately","Publica imediatamente.")],"default":("valor","PublishImmediately","A página declara PublishImmediately como default.")}),
          ("recordTypes","RecordType[]","N",None,"Tipos de registro do objeto."),("recordTypeTrackFeedHistory","boolean","N","19.0","Feed por tipo de registro; exige enableFeeds."),("recordTypeTrackHistory","boolean","N","19.0","Histórico por tipo de registro; exige enableHistory."),
          ("searchLayouts","SearchLayouts","N",None,"Configuração de layouts de busca."),("sharingModel","SharingModel","N",None,"Padrão de compartilhamento da org para o objeto.",{"nota_versao":"Gravável via API a partir da 30.0.","dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Valores de SharingModel não listados nesta página."}}),
          ("sharingReasons","SharingReason[]","N",None,"Motivos de compartilhamento."),("sharingRecalculations","SharingRecalculation[]","N",None,"Recálculos de compartilhamento personalizados."),
          ("startsWith","StartsWith","N",None,"Se o nome começa com vogal, consoante ou caractere especial (traduções).",{"dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Valores não listados nesta página."}}),
          ("validationRules","ValidationRule[]","N",None,"Regras de validação do objeto."),
          ("visibility","SetupObjectVisibility","N","34.0","Visibilidade do objeto ou configuração.",{"vals":[("Public","Visível (default)."),("Protected","Só na org do desenvolvedor."),("PackageProtected","Só custom metadata types (47.0+).")],"default":("valor","Public","A página declara Public como default.")}),
          ("webLinks","WebLink[]","N",None,"Links e botões personalizados.")]
    mdt("CustomObject", S, "Definição de um objeto (customizado, padrão ou externo) e, no formato Metadata API, de seus componentes filhos.",
        "Versionar a estrutura de um objeto: rótulos, compartilhamento, recursos habilitados e componentes filhos.", "10.0", co,
        exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<CustomObject {NS}>\n    <deploymentStatus>Deployed</deploymentStatus>\n    <description>Contratos de manutenção.</description>\n    <label>Contrato de Serviço</label>\n    <nameField>\n        <label>Número do Contrato</label>\n        <type>Text</type>\n    </nameField>\n    <pluralLabel>Contratos de Serviço</pluralLabel>\n    <sharingModel>ReadWrite</sharingModel>\n</CustomObject>',
        cobertura_nota="Tabela Fields lida em 100k de 101,8k caracteres; os ~1,8k finais continham apenas exemplo. Valores de DeploymentStatus, SharingModel, Gender e StartsWith estão em outras páginas.",
        divergencias=["O exemplo usa Deployed e ReadWrite, valores presentes em exemplos oficiais da documentação (amostra da página ValidationRule), mas as listas completas de DeploymentStatus e SharingModel não foram lidas."])

    # ------------------------- CustomField (filho de CustomObject) -------------------------
    S = "src:mdapi-customfield"
    cf = [("businessOwnerGroup","reference","N","45.0","Grupo que ajuda a definir a classificação de segurança do campo."),("businessOwnerUser","reference","N","45.0","Pessoa responsável pela importância do campo."),
          ("businessStatus","picklist","N","45.0","Se o campo está em uso.",{"vals":[("Active","Em uso."),("DeprecateCandidate","Candidato a descontinuação."),("Hidden","Oculto.")]}),
          ("caseSensitive","boolean","N",None,"Se o campo diferencia maiúsculas de minúsculas."),("complianceGroup","multipicklist","N","47.0","Regulamentos que se aplicam aos dados do campo.",{"vals":[("CCPA",None),("COPPA",None),("GDPR",None),("HIPAA",None),("PCI",None),("PII",None)]}),
          ("customDataType","string","N",None,"Obsoleto desde a 45.0.",{"ate":"44.0"}),("defaultValue","string","N",None,"Valor padrão do campo, se definido."),
          ("deleteConstraint","DeleteConstraint","N",None,"O que acontece com o lookup quando o registro pai é excluído.",{"vals":[("Cascade","Exclui os filhos."),("Restrict","Impede a exclusão do pai."),("SetNull","Limpa o campo de lookup.")],"default":("valor","SetNull","A página declara SetNull como default.")}),
          ("deprecated","boolean","N",None,"Reservado para uso futuro."),("description","string","N",None,"Descrição do campo."),("displayFormat","string","N",None,"Formato de exibição do campo."),
          ("displayLocationInDecimal","boolean","N",None,"Exibe geolocalização em decimal (true) ou graus, minutos e segundos (false)."),("elementType","ElementType","N",None,"Reservado para uso futuro.",{"dominio":{"natureza":"desconhecida","estado":"desconhecido"}}),
          ("encryptionScheme","EncryptionScheme","N","44.0","Esquema de criptografia do Shield Platform Encryption.",{"vals":[("CaseInsensitiveDeterministicEncryption",None),("CaseSensitiveDeterministicEncryption",None),("None",None),("ProbabilisticEncryption",None)]}),
          ("externalDeveloperName","string","C:Somente objetos externos.","32.0","Coluna da fonte externa que corresponde ao campo."),("externalId","boolean","N",None,"Se o campo é um ID externo."),
          ("fieldManageability","FieldManageability","N",None,"Quem pode alterar o campo após lançamento em pacote (só custom metadata types).",{"vals":[("Locked",None),("DeveloperControlled",None),("SubscriberControlled",None)]}),
          ("formula","string","N",None,"Fórmula do campo, se houver."),("formulaTreatBlanksAs","TreatBlanksAs","N",None,"Como a fórmula trata valores em branco.",{"vals":[("BlankAsBlank",None),("BlankAsZero",None)]}),
          ("fullName","string","S",None,"Nome completo do campo; obrigatório em create, update e delete.",{"herdada":"Metadata"}),("globalPicklist","string","N","37.0","Picklist global cujos valores são herdados (só na 37.0).",{"ate":"37.0"}),
          ("indexed","boolean","N",None,"Se o campo é indexado (só até a 14.0).",{"ate":"14.0"}),("inlineHelpText","string","N",None,"Texto de ajuda do campo."),("isAIPredictionField","boolean","N","43.0","Campo numérico que guarda dados do Einstein Prediction Builder."),
          ("isFilteringDisabled","boolean","C:Somente objetos externos.","32.0","Exclui o campo externo de filtros."),("isNameField","boolean","C:Somente campos de texto de objetos externos.","32.0","Marca o campo de nome de um objeto externo."),
          ("isSortingDisabled","boolean","C:Somente objetos externos.","32.0","Exclui o campo externo da ordenação."),("label","string","N",None,"Rótulo do campo."),("length","int","N",None,"Tamanho do campo."),
          ("lookupFilter","LookupFilter","N","30.0","Filtro de pesquisa do lookup."),("maskChar","EncryptedFieldMaskChar","N",None,"Caractere de máscara (Classic Encryption).",{"vals":[("asterisk",None),("X",None)]}),
          ("maskType","EncryptedFieldMaskType","N",None,"Formato de máscara (Classic Encryption).",{"vals":[("all",None),("creditCard",None),("lastFour",None),("nino",None),("sin",None),("ssn",None)]}),
          ("metadataRelationshipControllingField","string","C:Relacionamentos de custom metadata.","39.0","Campo que define o objeto de um relacionamento de metadados."),
          ("picklist","Picklist","N",None,"Obsoleto; usar valueSet após a 37.0."),("populateExistingRows","boolean","N",None,"Se linhas existentes são preenchidas."),("precision","int","N",None,"Total de dígitos de um número."),
          ("referenceTargetField","string","C:Lookups indiretos em objetos externos.","32.0","Campo do pai usado no lookup indireto."),("referenceTo","string","N",None,"Objeto referenciado pelo campo.",{"natureza":"referencia","contexto":"Nome API de um objeto existente na org."}),
          ("relationshipLabel","string","N",None,"Rótulo do relacionamento."),("relationshipName","string","N",None,"Nome do relacionamento um-para-muitos."),
          ("relationshipOrder","int","N",None,"Papel do pai em objeto de junção: 0 primário, 1 secundário.",{"default":("valor",0,"A página declara 0 como default.")}),
          ("reparentableMasterDetail","boolean","N","25.0","Se filhos master-detail podem mudar de pai.",{"default":("false",False,"A página declara default false.")}),
          ("required","boolean","N",None,"Se é obrigatório informar valor ao criar o registro.",{"rotulo":"Campo obrigatório"}),("scale","int","N",None,"Dígitos à direita da vírgula decimal."),
          ("securityClassification","picklist","N","45.0","Sensibilidade dos dados do campo.",{"vals":[("Public",None),("Internal",None),("Confidential",None),("Restricted",None),("MissionCritical",None)]}),
          ("startingNumber","int","N",None,"Número inicial de campos de numeração automática.",{"notas":["A página indica 0 para campos padrão e 1 para customizados."]}),("stripMarkup","boolean","N",None,"Remove marcação ao converter texto rico em texto longo."),
          ("summarizedField","string","C:Exigido, exceto quando summaryOperation é Count.",None,"Campo do registro filho que é resumido."),("summaryFilterItems","FilterItem[]","N",None,"Condições para o filho entrar no resumo."),
          ("summaryForeignKey","string","N",None,"Campo master-detail do filho que liga ao pai."),("summaryOperation","SummaryOperations","N",None,"Cálculo do resumo.",{"vals":[("Count",None),("Min",None),("Max",None),("Sum",None)]}),
          ("trackFeedHistory","boolean","N","18.0","Rastreia o campo no feed; exige enableFeeds no objeto."),("trackHistory","boolean","N",None,"Rastreia histórico; exige enableHistory no objeto."),
          ("trackTrending","boolean","N","29.0","Captura histórico de tendências."),("trueValueIndexed","boolean","N",None,"Indexa valores verdadeiros de checkbox (só até a 14.0).",{"ate":"14.0"}),
          ("type","FieldType","C:Incluído para campos customizados; opcional para alguns campos padrão.",None,"Tipo do campo.",{"dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Valores de FieldType não listados na página de CustomField."}}),
          ("unique","boolean","N",None,"Se os valores devem ser únicos."),("valueSet","ValueSet","N","38.0","Valores da picklist ou conjunto global herdado."),("visibleLines","int","N",None,"Número de linhas exibidas."),
          ("writeRequiresMasterRead","boolean","N",None,"Se ler o pai basta para alterar filhos.",{"default":("false",False,"A página declara default false.")})]
    mdt("CustomField", S, "Definição de um campo de objeto. É componente filho de CustomObject.",
        "Versionar tipo, tamanho, regras e segurança de um campo.", "10.0", cf, parent="CustomObject",
        exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<CustomField {NS}>\n    <fullName>Valor_Mensal__c</fullName>\n    <label>Valor Mensal</label>\n    <precision>16</precision>\n    <required>false</required>\n    <scale>2</scale>\n    <type>Currency</type>\n</CustomField>',
        cobertura_nota="Tabela lida em 100k de 112,8k caracteres; subtipos LookupFilter e Mkt* não detalhados. A página declara que, salvo indicação, os campos são criáveis, filtráveis e anuláveis.",
        divergencias=["O exemplo usa Currency como FieldType; a lista de FieldType não foi lida nesta sessão (valor a confirmar)."])

    # ------------------------- ValidationRule (filho) -------------------------
    S = "src:mdapi-validationrule"
    mdt("ValidationRule", S, "Definição de uma regra de validação: fórmula de erro e mensagem. É componente filho de CustomObject.",
        "Impedir a gravação de registros quando a fórmula retorna verdadeiro.", "12.0", [
        ("active","boolean","S",None,"Se a regra está ativa."),("description","string","N",None,"Descrição da regra."),
        ("errorConditionFormula","string","S",None,"Fórmula que, quando verdadeira, bloqueia a gravação e exibe a mensagem.",{"tipo_explicado":"Fórmula","natureza":"texto_livre"}),
        ("errorDisplayField","string","N",None,"Campo ao lado do qual a mensagem aparece; sem valor ou campo fora do layout, vai para o topo da página."),
        ("errorMessage","string","S",None,"Mensagem exibida quando a regra bloqueia.",{"restr":"Até 255 caracteres."}),
        ("fullName","string","S",None,"Nome interno da regra; herdado de Metadata e obrigatório em create, update e delete.",{"herdada":"Metadata"})],
        parent="CustomObject",
        exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<ValidationRule {NS}>\n    <fullName>Valor_Positivo</fullName>\n    <active>true</active>\n    <errorConditionFormula>Valor_Mensal__c &lt; 0</errorConditionFormula>\n    <errorDisplayField>Valor_Mensal__c</errorDisplayField>\n    <errorMessage>O valor mensal não pode ser negativo.</errorMessage>\n</ValidationRule>',
        curinga=False, divergencias=["A amostra XML da página usa <validationMessage>, elemento ausente da tabela de campos."],
        alertas=["Desde a 20.0 não pode usar campos compostos; desde a 40.0 pode ser usada com custom metadata types."])

    # ------------------------- RecordType (filho) -------------------------
    S = "src:mdapi-recordtype"
    struct("RecordTypePicklistValue", S, ["mdt:RecordType"], [("picklist","string","S",None,"Nome do campo picklist."),("values","PicklistValue","N",None,"Valores permitidos neste tipo de registro.")], "Combinação de valores de uma picklist disponível em um tipo de registro.")
    mdt("RecordType", S, "Definição de um tipo de registro. É componente filho de CustomObject.", "Oferecer processos, valores de picklist e layouts diferentes para o mesmo objeto.", "12.0", [
        ("active","boolean","S",None,"Se o tipo de registro está ativo."),
        ("businessProcess","string","C:Obrigatório para Lead, Opportunity, Solution e Case; não permitido nos demais objetos.","17.0","Nome do processo de negócio associado."),
        ("compactLayoutAssignment","string","N","29.0","Layout compacto atribuído ao tipo de registro."),("description","string","N",None,"Descrição.",{"restr":"Até 255 caracteres."}),
        ("fullName","string","S",None,"Nome único com letras, dígitos e sublinhados, começando por letra.",{"herdada":"Metadata"}),("label","string","S",None,"Rótulo do tipo de registro."),
        ("picklistValues","RecordTypePicklistValue[]","N",None,"Valores de picklist disponíveis neste tipo de registro.")], parent="CustomObject",
        exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<RecordType {NS}>\n    <fullName>Manutencao</fullName>\n    <active>true</active>\n    <description>Contratos de manutenção.</description>\n    <label>Manutenção</label>\n</RecordType>')

    # ------------------------- Flow (primeiro nível) -------------------------
    S = "src:mdapi-flow"
    fl = [(n,t,"N",v,None) for n,t,v in [("actionCalls","FlowActionCall[]","31.0"),("apexPluginCalls","FlowApexPluginCall[]",None),("assignments","FlowAssignment[]",None),("choices","FlowChoice[]",None),
          ("collectionFilterCriteria","FlowCollectionFilterCriteria[]",None),("collectionProcessors","FlowCollectionProcessor[]","50.0"),("constants","FlowConstant[]",None),("customErrors","FlowCustomError[]",None),
          ("customProperties","FlowCustomProperty[]","63.0"),("decisions","FlowDecision[]",None),("dynamicChoiceSets","FlowDynamicChoiceSet[]",None),("ends","FlowEnd[]","68.0"),("exitRules","FlowExitRule[]","61.0"),
          ("experiments","FlowExperiment[]","61.0"),("formulas","FlowFormula[]",None),("groups","FlowNodeGroup[]","68.0"),("loops","FlowLoop[]","30.0"),("orchestratedStages","FlowOrchestratedStage[]","53.0"),
          ("processMetadataValues","FlowMetadataValue[]","31.0"),("recordCreates","FlowRecordCreate[]",None),("recordDeletes","FlowRecordDelete[]",None),("recordLookups","FlowRecordLookup[]",None),
          ("recordRollbacks","FlowRecordRollback[]","52.0"),("recordUpdates","FlowRecordUpdate[]",None),("screens","FlowScreen[]",None),("stages","FlowStage[]","42.0"),("start","FlowStart[]","47.0"),
          ("steps","FlowStep[]",None),("subflows","FlowSubflow[]","25.0"),("textTemplates","FlowTextTemplate[]",None),("transforms","FlowTransform[]","59.0"),("variables","FlowVariable[]",None),("waits","FlowWait[]","32.0")]]
    fl += [("apiVersion","number","N","50.0","Versão de API em que o flow é executado."),("areMetricsLoggedToDataCloud","boolean","N","63.0",None),("description","string","N",None,"Descrição do flow."),
           ("environments","FlowEnvironment","N","55.0",None,{"dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Valores não extraídos."}}),
           ("fullName","string","S",None,"Nome API do flow.",{"herdada":"Metadata"}),("interviewLabel","string","N",None,"Rótulo das entrevistas (execuções) do flow."),
           ("isAdditionalPermissionRequiredToRun","boolean","N","47.0",None),("isTemplate","boolean","N","45.0","Se o flow é um modelo."),("label","string","S",None,"Rótulo do flow."),
           ("migratedFromWorkflowRuleName","string","N","54.0","Regra de fluxo de trabalho de origem, quando migrado."),
           ("processType","FlowProcessType","N","31.0","Tipo de processo do flow.",{"dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Lista extraída parcialmente (ex.: AutoLaunchedFlow, Flow, Orchestrator, Workflow); não declarar fechada até conferir no WSDL."}}),
           ("runInMode","FlowRunInMode","N","48.0",None,{"dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Valores não extraídos."}}),
           ("segment","string","N",None,None),("startElementReference","string","N",None,"Elemento inicial do flow."),
           ("status","FlowVersionStatus","N",None,"Status da versão do flow.",{"vals":[("Active",None),("Draft",None),("Obsolete",None),("InvalidDraft",None),("UnderReview",None)],"completa":"desconhecido"}),
           ("timeZoneSidKey","string","N","56.0",None),("triggerOrder","int","N","54.0","Ordem de execução entre flows disparados pelo mesmo evento.")]
    mdt("Flow", S, "Definição de uma versão de flow: elementos, variáveis, recursos e configuração de execução.", "Versionar automações declarativas.", "24.0", fl,
        exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<Flow {NS}>\n    <apiVersion>68.0</apiVersion>\n    <description>Exemplo mínimo.</description>\n    <label>Atualizar contrato</label>\n    <processType>AutoLaunchedFlow</processType>\n    <status>Draft</status>\n</Flow>',
        completa=True, cobertura_nota="Somente campos de primeiro nível (tabela lida em 100k de 113,7k caracteres). Os subtipos de Flow (dezenas) não foram inventariados.",
        alertas=["Os subtipos Flow* formam uma árvore grande; o inventário deve tratá-los como estruturas auxiliares e resolver ciclos por referência."])

    # ------------------------- PathAssistant -------------------------
    S = "src:mdapi-pathassistant"
    struct("PathAssistantStep", S, ["mdt:PathAssistant"], [("fieldNames","string","N",None,"Campos exibidos na etapa."),("info","string","N",None,"Orientação exibida na etapa."),("picklistValueName","string","S",None,"Valor da picklist que corresponde à etapa.")], "Etapa configurada de um Path.")
    mdt("PathAssistant", S, "Definição de um Path: barra de etapas baseada em uma picklist, com campos e orientação por etapa.", "Guiar o usuário pelas etapas de um processo.", "34.0", [
        FULLNAME_HERDADO(S),
        ("active","boolean","N",None,"Se o Path está ativo."),("entityName","string","S",None,"Objeto do Path; fixo para Opportunity, Lead e Quote, informado para objetos customizados.",{"notas":["Somente leitura após a criação, segundo a página."]}),
        ("fieldName","string","S",None,"Picklist que define as etapas.",{"notas":["Somente leitura após a criação."]}),("masterLabel","string","S",None,"Nome exibido do Path."),
        ("pathAssistantSteps","PathAssistantStep[]","N",None,"Etapas configuradas; etapas ausentes ficam sem configuração.",{"notas":["A página tipa como PathAssistantStep (sem []); tratado como lista por conter várias etapas — conferir no WSDL."]}),
        ("recordTypeName","string","S",None,"Tipo de registro do Path; não muda após a criação.")],
        exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<PathAssistant {NS}>\n    <active>true</active>\n    <entityName>Contrato_Servico__c</entityName>\n    <fieldName>Status__c</fieldName>\n    <masterLabel>Etapas do contrato</masterLabel>\n    <pathAssistantSteps>\n        <info>Confira as cláusulas antes de enviar.</info>\n        <picklistValueName>Em_analise</picklistValueName>\n    </pathAssistantSteps>\n    <recordTypeName>__MASTER__</recordTypeName>\n</PathAssistant>',
        divergencias=["Tipo de pathAssistantSteps sem marcação de lista na extração.", "O valor __MASTER__ no exemplo para tipo de registro mestre não foi confirmado na página; usar com cautela."])

    # ------------------------- FlexiPage -------------------------
    S = "src:mdapi-flexipage"
    mdt("FlexiPage", S, "Definição de uma Lightning page: tipo, template, regiões e componentes.", "Versionar páginas montadas no Lightning App Builder.", "29.0", [
        FULLNAME_HERDADO(S),
        ("description","string","N",None,"Descrição da página."),("events","FlexiPageEvent[]","N","53.0","Eventos associados à página."),("flexiPageRegions","FlexiPageRegion[]","N",None,"Regiões que compõem a página."),
        ("masterLabel","string","S",None,"Rótulo da página no Setup."),("pageTemplate","string","S","33.0","Template da página (substituído por template).",{"ate":"38.0"}),
        ("parentFlexiPage","string","N","37.0","Página da qual esta herda comportamento."),("platformActionlist","PlatformActionList","N","34.0","Ações da barra de ações de uma página de app."),
        ("quickActionList","QuickActionList","N",None,"Ações rápidas associadas à página."),("sobjectType","string","N","37.0","Objeto da página; nulo para AppPage e HomePage."),
        ("template","FlexiPageTemplateInstance","S","39.0","Instância de template da página."),
        ("type","FlexiPageType","S","32.0","Tipo de página.",{"vals":[(v,None) for v in ["AppPage","CdpRecordPage","CommAppPage","CommCheckoutPage","CommContractDetailViewPage","CommFlowPage","CommForgotPasswordPage","CommGlobalSearchResultPage","CommLoginPage","CommNoSearchResultsPage","CommObjectPage","CommOrderComfirmationPage","CommQuickActionCreatePage","CommRecordPage","CommRelatedListPage","CommSearchResultPage","CommSelfRegisterPage","CommThemeLayoutPage","EmailContentPage","EmailTemplatePage","EmbeddedServicePage","ForecastingPage","HomePage","MailAppAppPage","OmniSupervisorPageType","QuickAction","RecordPage","RecordPreview","UtilityBar","VoiceExtension"]],"completa":"desconhecido"})],
        cobertura_nota="Campos de primeiro nível; subtipos (FlexiPageRegion, ComponentInstance etc.) não detalhados.",
        divergencias=["pageTemplate marcado como obrigatório mas obsoleto após a 38.0; template obrigatório desde a 39.0."])

    # ------------------------- QuickAction -------------------------
    S = "src:mdapi-quickaction"
    mdt("QuickAction", S, "Definição de uma ação rápida: tipo, objeto-alvo, layout e valores predefinidos.", "Oferecer tarefas frequentes em contexto, como criar um registro relacionado ou abrir um flow.", "28.0", [
        ("actionSubtype","ActionSubtype","N","50.0","Subtipo da ação.",{"vals":[("Action",None),("Create",None),("ScreenAction",None),("Update",None)],"notas":["A extração grafou o tipo como 'ActionSybtype'; conferir no WSDL."]}),
        ("canvas","string","N","29.0","Nome do app Canvas, para ações Canvas."),("description","string","N",None,"Descrição da ação."),("fieldOverrides","FieldOverride[]","N",None,"Valores predefinidos para campos da ação."),
        ("flexiPage","string","N","68.0","Página de ação rápida com campos e layout (Beta)."),("flowDefinition","string","N",None,"Flow invocado pela ação."),("height","int","N",None,"Altura do painel da ação, em pixels."),
        ("icon","string","N",None,"Ícone da ação."),("isProtected","boolean","N",None,"Se o componente fica protegido contra referências em orgs instaladoras."),("label","string","N",None,"Nome da ação exibido ao usuário."),
        ("lightningComponent","string","N","38.0","Componente Lightning invocado."),("optionsCreateFeedItem","boolean","S","36.0","Se a conclusão cria um item de feed (tipos Create, Update e LogACall)."),
        ("page","string","N",None,"Página Visualforce invocada."),("quickActionLayout","QuickActionLayout","N",None,"Layout dos campos da ação."),("quickActionParameters","QuickActionParameter[]","N","63.0","Entradas e saídas da ação."),
        ("standardLabel","QuickActionLabel","N",None,"Rótulo padrão a aplicar.",{"dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Valores não extraídos integralmente (ex.: CreateNew, LogACall, Update)."}}),
        ("successMessage","string","N","36.0","Mensagem após sucesso."),("targetObject","string","N",None,"Objeto criado ou alterado pela ação."),("targetParentField","string","N",None,"Campo que liga o objeto-alvo ao pai."),
        ("targetRecordType","string","N",None,"Tipo de registro a criar."),
        ("type","QuickActionType","S",None,"Tipo da ação.",{"vals":[(v,None) for v in ["Canvas","Create","Flexipage","Flow","LightningComponent","LightningWebComponent","LogACall","Post","SendEmail","SocialPost","Update","VisualforcePage"]]}),
        ("width","int","N",None,"Largura do painel da ação, em pixels.")],
        estende="não declarado no trecho extraído",
        exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<QuickAction {NS}>\n    <description>Abre o flow de renovação.</description>\n    <flowDefinition>Renovar_Contrato</flowDefinition>\n    <label>Registrar renovação</label>\n    <optionsCreateFeedItem>false</optionsCreateFeedItem>\n    <type>Flow</type>\n</QuickAction>',
        alertas=["Nome físico de ações específicas de objeto usa o padrão Objeto.Nome segundo convenção comum, mas a página extraída não declara o padrão; registrado como pendente."])

    # ------------------------- CustomTab -------------------------
    S = "src:mdapi-customtab"
    um = "Apenas um entre auraComponent, customObject, flexiPage, lwcComponent, page, scontrol e url pode ser definido."
    mdt("CustomTab", S, "Definição de uma tab: entrada de navegação para um objeto, página, componente ou URL.", "Dar acesso pela navegação a objetos, páginas e componentes.", "10.0", [
        ("actionOverrides","ActionOverride[]","N","37.0","Substituições de ação da tab, uma por formFactor."),("auraComponent","string","C:"+um,None,"Componente Aura exibido."),
        ("customObject","boolean","C:"+um,None,"Verdadeiro se a tab representa um objeto customizado."),("description","string","N",None,"Descrição."),("flexiPage","string","C:"+um,None,"Lightning page exibida."),
        ("frameHeight","int","C:Necessário para tabs de s-control e de página.",None,"Altura do frame, em pixels."),("fullName","string","?",None,"Nome da tab: nome API do objeto ou nome de desenvolvedor da web tab.",{"herdada":"Metadata"}),
        ("hasSidebar","boolean","N",None,"Se a barra lateral aparece."),("icon","string","N","14.0","Imagem usada quando não se usa um estilo padrão."),("label","string","N",None,"Rótulo (somente web tabs)."),
        ("lwcComponent","string","C:"+um,None,"Lightning web component exibido."),
        ("motif","string","S",None,"Estilo (cor e ícone) da tab.",{"dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"verificado","evidencias":[ev(S)],"contexto":"A página lista estilos Custom1 a Custom100 com nomes de ícone; lista não transcrita aqui."}}),
        ("page","string","C:"+um,None,"Página Visualforce exibida."),("scontrol","string","C:"+um,None,"S-control exibido."),("splashPageLink","string","N",None,"Link personalizado usado como página de abertura."),
        ("url","string","C:"+um,None,"Página web externa incorporada."),("urlEncodingKey","Encoding","N",None,"Codificação de caracteres para tabs de URL.",{"default":("valor","UTF-8","A página declara UTF-8 como default."),"dominio":{"natureza":"enum_fechado","lista_completa":"desconhecido","estado":"desconhecido","contexto":"Outros valores não listados na página."}})],
        exemplo=f'<?xml version="1.0" encoding="UTF-8"?>\n<CustomTab {NS}>\n    <customObject>true</customObject>\n    <description>Tab do objeto Contrato de Serviço.</description>\n    <motif>Custom20: Airplane</motif>\n</CustomTab>',
        divergencias=["O valor de motif no exemplo segue o formato 'CustomN: Nome' visto na documentação, mas o número exato de cada ícone não foi transcrito; conferir antes de usar."])

    emit_structs()
