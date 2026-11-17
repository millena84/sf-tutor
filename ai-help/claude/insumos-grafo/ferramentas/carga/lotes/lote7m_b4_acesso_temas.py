"""Lote 7m (rodada B4, parte B; issues #8 e #34): compartilhamento, papéis, nuvens de setor, os temas internos sem funcionalidade e os
caminhos de Setup pendentes da issue #8.

- Metadata types Role, SharingRules (com SharingCriteriaRule, SharingOwnerRule, SharingGuestRule e SharingTerritoryRule),
  IndustriesSettings (190 opções) e RevenueManagementSettings (19). Estruturas SharedTo e AccountSharingRuleSettings.
- Objeto API UserRole (a página clássica da Object Reference devolveu conteúdo ilegível; foi lida a página nova da referência de objetos,
  e os nomes de campo vêm da Field Reference).
- Funcionalidades hierarquia-de-papeis, regras-de-compartilhamento, licencas-de-usuario, configuracoes-de-nuvens-de-setor e
  revenue-management; classificações secundárias que dão funcionalidades aos temas internos que não tinham nenhuma.
- Caminhos de Setup de perfis, tipos de registro, contas, contatos, oportunidades, casos, campanhas, produtos e catálogos de preço,
  previsões colaborativas e equipes de conta e de oportunidade.

Ordem: lote7l_b4_estruturas.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7m_b4_acesso_temas.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga import obj as O                    # noqa: E402
from carga.base import af, ev, ld, sv, caminho  # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7m-b4-acesso-temas.txt"
ATLAS = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
H = "https://help.salesforce.com/s/articleView?id="
L = "&language=en_US&type=5"
AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")


def substituir_fontes(novas):
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


MD = {"Role": "meta_role", "RoleOrTerritory": "meta_roleorterritory", "SharingRules": "meta_sharingrules",
      "SharingBaseRule": "meta_sharingbaserule", "SharedTo": "meta_sharedto", "IndustriesSettings": "meta_industriessettings"}
AJUDA = [
    ("src:help-create-clone-profiles", "Create or Clone Profiles", "sf.users_profiles_cloning.htm", "Caminho da lista de perfis e clonagem."),
    ("src:help-create-record-types", "Create Record Types", "platform.creating_record_types.htm", "Criação de record types nas configurações do objeto."),
    ("src:help-shared-contacts-setup", "Set Up Contacts to Multiple Accounts", "sales.shared_contacts_set_up.htm", "Account Settings e Contacts to Multiple Accounts."),
    ("src:help-opportunity-teams-enable", "Turn on Opportunity Teams", "sf.teamselling_enabling.htm", "Opportunity Team Settings."),
    ("src:help-account-teams-enable", "Turn On Account Teams", "sf.accountteam_enable.htm", "Página Account Teams."),
    ("src:help-forecasts-settings", "Turn On Salesforce Forecasting and Define Forecast Settings", "forecasts3_defining_forecasts_settings.htm",
     "Forecasts Settings; ativação automática desde o Winter '24."),
    ("src:help-kb-opportunity-settings", "Enable 'Supply Default Opportunity Line Item Values' (KB)", "000325386", "Página Opportunity Settings."),
    ("src:help-suggested-articles-cases", "Enable Suggested Articles to Solve Cases", "sf.cases_suggest_articles.htm", "Página Support Settings."),
    ("src:help-campaign-influence-enable", "Enable Customizable Campaign Influence", "campaigns_influence_customizable_setup.htm",
     "Campaign Influence Settings."),
    ("src:help-product-settings", "Activate and Deactivate Product Prices with Their Products Simultaneously", "customize_product.htm",
     "Página Product Settings."),
    ("src:help-create-user-role", "Create a User Role", "users_role_view.htm", "Página Roles, permissões e criação de papéis."),
    ("src:help-sharing-rules-criteria", "Create Criteria-Based Sharing Rules", "platform.security_sharing_rules_criteria.htm",
     "Sharing Settings e permissão Manage Sharing."),
    ("src:help-sharing-rules-guest", "Create Guest User Sharing Rules", "sf.security_sharing_rules_guest.htm", "Regras para guest users."),
]
substituir_fontes(
    [C.fonte(f"src:mdapi-{n.lower()}", f"{n} (Metadata API)", ATLAS + pg + ".htm", f"Arquivo, versão e propriedades do tipo {n}.", EXTR, DATA)
     for n, pg in MD.items()]
    + [C.fonte("src:revenue-revenuemanagementsettings", "RevenueManagementSettings (Revenue Management Developer Guide)",
               "https://developer.salesforce.com/docs/revenue/revenue-management/guide/meta-revenuemanagementsettings.html",
               "Arquivo, versão e propriedades do tipo RevenueManagementSettings.", EXTR, DATA, versao="sem versão na página"),
       C.fonte("src:objref-userrole", "UserRole (Object Reference)",
               "https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-userrole.html",
               "Chamadas, acesso e campos de UserRole.", EXTR, DATA, versao="sem versão na página"),
       C.fonte("src:fieldref-userrole", "UserRole (Field Reference)",
               "https://developer.salesforce.com/docs/platform/field-reference/references/field-reference/salesforce-field-reference-userrole.html",
               "Nomes de API, rótulos e tipos dos campos de UserRole.", EXTR, DATA, versao="sem versão na página")]
    + [C.fonte(i, t + " (Salesforce Help)", H + a + L, p, EXTR, DATA, **AJ) for i, t, a, p in AJUDA])
S_ROLE, S_ROT, S_SR, S_SBR, S_ST, S_IND = (f"src:mdapi-{n.lower()}" for n in MD)
S_RMS, S_UR, S_URF = "src:revenue-revenuemanagementsettings", "src:objref-userrole", "src:fieldref-userrole"

NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
B, S = "boolean", "string"
FALSE = ("false", False, "A página declara default false.")
REG = []


def valores(*vs):
    return [(v, None) for v in vs]


def estrutura(nome, src, usada_por, rows, o_que_e):
    M.struct(nome, src, usada_por, rows, o_que_e)
    REG.append((src, "estruturas", nome))


def tipo(nome, src, *a, **k):
    M.mdt(nome, src, *a, **k)
    REG.append((src, "metadata-types", nome))


def sem(tipo_, motivo, estado="desconhecido"):
    return {"tipo": tipo_, "estado": estado, "motivo": motivo}


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


# ================================================================ Role
ACESSO = valores("Read", "Edit", "None")
tipo("Role", S_ROLE,
     "Um papel (role) da hierarquia de papéis: quem fica acima de quem e que acesso o papel dá aos casos, contatos e oportunidades das "
     "contas dos usuários dele.",
     "Versionar e implantar a hierarquia de papéis da org.", "24.0", [
         P("caseAccessLevel", S, None, "Acesso aos casos de outros usuários ligados às contas que o usuário possui.", vals=ACESSO, herdada="RoleOrTerritory",
           notas=["Fica oculto quando o compartilhamento de casos é Public Read/Write; sem valor, vale o padrão da página de Setup."]),
         P("contactAccessLevel", S, None, "Acesso aos contatos de outros usuários ligados às contas que o usuário possui.", vals=ACESSO,
           herdada="RoleOrTerritory", notas=["Fica oculto quando o compartilhamento de contatos é Public Read/Write ou Controlled by Parent."]),
         P("description", S, None, "Descrição do papel.", herdada="RoleOrTerritory"),
         P("fullName", S, None, "Nome de API; aparece como Role Name na interface. Só letras, dígitos e sublinhado, começando por letra.",
           herdada="Metadata"),
         P("mayForecastManagerShare", B, None, "Permite ao gerente de previsão compartilhar a própria previsão manualmente.", herdada="RoleOrTerritory"),
         P("name", S, None, "Nome do papel.", "S", herdada="RoleOrTerritory"),
         P("opportunityAccessLevel", S, None, "Acesso às oportunidades de outros usuários ligadas às contas que o usuário possui.", vals=ACESSO,
           herdada="RoleOrTerritory", notas=["Fica oculto quando o compartilhamento de oportunidades é Public Read/Write."]),
         P("parentRole", S, None, "O papel imediatamente acima na hierarquia."),
     ], estende="RoleOrTerritory", exemplo=CAB + f"""<Role {NS}>
    <caseAccessLevel>Edit</caseAccessLevel>
    <contactAccessLevel>Edit</contactAccessLevel>
    <description>[descrição]</description>
    <mayForecastManagerShare>false</mayForecastManagerShare>
    <name>[Nome do papel]</name>
    <opportunityAccessLevel>Read</opportunityAccessLevel>
    <parentRole>[Nome_Do_Papel_Acima]</parentRole>
</Role>""", curinga=True,
     alertas=["Os campos de acesso só valem para registros ligados a contas que o usuário possui; o restante segue os padrões da org e o "
              "compartilhamento.", "RoleOrTerritory não pode ser criado diretamente; existe só como base de Role e de Territory."],
     cobertura_nota="Universo esperado = campos de Role (2) mais os herdados de RoleOrTerritory (6), nas páginas do guia versionado 264.0, "
                    "lidas em 2026-11-17.")
REG.append((S_ROT, "metadata-types", "Role"))
C.marcar_referencia("metadata-types", "Role", "parentRole", "mdt:Role")

# ================================================================ UserRole
UR = "obj:UserRole"
NOMES = "Nome de API conferido na Field Reference."
ur = [
    O.field(UR, "CaseAccessForAccountOwner", "picklist", "CFGNRSU", None, "Acesso do dono da conta aos casos ligados a ela.", S_UR,
            notas=[NOMES, "A página não lista os valores."]),
    O.field(UR, "ContactAccessForAccountOwner", "picklist", "CFGNRSU", "10.0", "Acesso do dono da conta aos contatos ligados a ela; fixo quando o "
            "compartilhamento de contatos é Controlled by Parent.", S_UR, notas=[NOMES, "A página não lista os valores."]),
    O.field(UR, "DeveloperName", "string", "CFGNSU", "24.0", "Nome de API único; vale defini-lo em cargas grandes.", S_UR, notas=[NOMES]),
    O.field(UR, "ForecastUserId", "reference", "CFGNSU", "6.0", "Usuário que é o gerente de previsão do papel.", S_UR, ref=["obj:User"], rel="ForecastUser",
            notas=[NOMES]),
    O.field(UR, "MayForecastManagerShare", "boolean", "CDFGSU", "11.0", "Permite ao gerente de previsão compartilhar a própria previsão; padrão "
            "false.", S_UR, notas=[NOMES]),
    O.field(UR, "Name", "string", "CFGISU", None, "Nome do papel.", S_UR, req=("sim", None), notas=[NOMES]),
    O.field(UR, "OpportunityAccessForAccountOwner", "picklist", "CFGRSU", None, "Acesso do dono da conta às oportunidades ligadas a ela; não pode "
            "ficar abaixo do padrão da org.", S_UR, req=("sim", None), notas=[NOMES, "A página não lista os valores."]),
    O.field(UR, "ParentRoleId", "reference", "CFGNSU", None, "O papel imediatamente acima.", S_UR, ref=["obj:UserRole"], rel="ParentRole", notas=[NOMES]),
    O.field(UR, "PortalAccountId", "reference", "CFGNS", "8.0", "Conta de portal ligada ao papel; somente leitura.", S_UR, ref=["obj:Account"],
            rel="PortalAccount", notas=[NOMES]),
    O.field(UR, "PortalAccountOwnerId", "reference", "FGNS", "12.0", "Dono da conta de portal; somente leitura.", S_UR, ref=["obj:User"],
            rel="PortalAccountOwner", notas=[NOMES]),
    O.field(UR, "PortalRole", "picklist", "FGNRS", "12.0", "Nível do papel de portal.", S_UR, vals=["Executive", "Manager", "User", "PersonAccount"],
            notas=[NOMES]),
    O.field(UR, "PortalType", "picklist", "CFGNRS", "9.0", "Tipo de portal do papel: nenhum, de cliente ou de parceiro; substitui IsPartner.", S_UR,
            notas=[NOMES, "A página descreve os três casos, mas não dá os valores de API."]),
    O.field(UR, "RollupDescription", "string", "CFGNSU", None, "Descrição do papel; rótulo Description.", S_UR, notas=[NOMES]),
]
for c in ur:
    c["evidencias"].append(ev(S_URF))
O.obj("UserRole",
      "Um papel da hierarquia de papéis, como registro. O usuário aponta para o papel dele pelo campo UserRoleId, e cada papel aponta para o "
      "papel acima por ParentRoleId.",
      "Consultar a hierarquia por API, por exemplo para descobrir quem está acima de um usuário, e criar ou alterar papéis.",
      [O.expo("padrao", "verificado", S_UR, ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()",
                                            "search()", "update()", "upsert()"],
              acesso="Desde o Summer '20, só quem tem View Roles and Role Hierarchy acessa; editar exige Manage Roles. Aplicações com Manage "
                     "Users podem consultar, criar, alterar e excluir.", nota="A página não informa a versão de entrada do objeto."),
       O.expo("tooling", "desconhecido", nota="Exposição na Tooling API não verificada.")],
      ur,
      [{"api": "padrao", "soql": "SELECT Name, DeveloperName, ParentRoleId FROM UserRole", "contexto": "API padrão. Lista os papéis e o papel acima de cada um.",
        "validacao": "documental"}],
      O.APEX_OK(S_UR), O.cob("completa", 13, 13, O.cnt(ur), "13 campos de negócio da página da referência de objetos; Id e campos de sistema "
                                                          "(LastModifiedById, LastModifiedDate, SystemModstamp) não foram cadastrados."), S_UR,
      alertas=["Nenhum campo de um papel de portal pode ser alterado.",
               "A página nova da referência de objetos não mostra os títulos dos campos; os nomes de API vêm da Field Reference, casados pela "
               "ordem alfabética e pela descrição."])
d = ld("objetos-api/User.json")
for c in d["campos"]:
    if c["nome"] == "UserRoleId":
        c["referencia"] = {"alvos": ["obj:UserRole"], "nome_relacionamento": "UserRole"}
sv("objetos-api/User.json", d)
C.rel_lookup("user-userrole", "obj:User", "UserRoleId", "obj:UserRole", "O papel do usuário na hierarquia.", "src:objref-user")
C.rel_lookup("userrole-parent", UR, "ParentRoleId", UR, "O papel acima na hierarquia.", S_UR)
C.rel_lookup("userrole-forecastuser", UR, "ForecastUserId", "obj:User", "O gerente de previsão do papel.", S_UR)
C.rel_lookup("userrole-portalaccount", UR, "PortalAccountId", "obj:Account", "A conta de portal ligada ao papel.", S_UR)
C.rel_representacao_comum("role-userrole", "mdt:Role", UR, "O papel é recuperado e implantado como Role e consultado como registro em UserRole.",
                          [S_ROLE, S_UR])

# ================================================================ SharingRules
SHT = [("allCustomerPortalUsers", S, "24.0", "Grupo de todos os usuários de customer portal."),
       ("allInternalUsers", S, "24.0", "Grupo de todos os usuários internos."),
       ("allPartnerUsers", S, "24.0", "Grupo de todos os usuários parceiros."),
       ("allRestrictedEmployeeUsers", S, "68.0", "Grupo dos funcionários só com a licença Unified Employee, para ampliar o acesso deles."),
       ("channelProgramGroup", S, "41.0", "Grupo gerido pelo sistema com os parceiros de um channel program ou nível."),
       ("channelProgramGroups", "string[]", "41.0", "Grupos geridos pelo sistema de vários channel programs ou níveis."),
       ("group", "string[]", "22.0", "Grupos que recebem acesso; preferível a groups."),
       ("groups", "string[]", None, "Grupos que recebem acesso; substituído por group."),
       ("guestUser", "string[]", "47.0", "Apelidos de guest users que recebem acesso; só em SharingGuestRule."),
       ("managerSubordinates", "string[]", "24.0", "Usuários cujos subordinados diretos e indiretos recebem acesso."),
       ("managers", "string[]", "24.0", "Usuários cujos gerentes diretos e indiretos recebem acesso."),
       ("portalRole", "string[]", "24.0", "Grupos com todos os usuários de um papel de portal."),
       ("portalRoleandSubordinates", "string[]", "24.0", "Grupos com os usuários de um papel de portal e dos papéis abaixo dele."),
       ("queue", "string[]", "24.0", "Filas que recebem acesso; só em regras de lead, caso e objeto customizado."),
       ("role", "string[]", "22.0", "Papéis que recebem acesso; preferível a roles."),
       ("roleAndSubordinates", "string[]", "22.0", "Papéis e os abaixo deles, inclusive contas de portal; preferível a rolesAndSubordinates."),
       ("roleAndSubordinatesInternal", "string[]", "22.0", "Papéis e os abaixo deles, só internos."),
       ("roles", "string[]", "22.0", "Papéis que recebem acesso; substituído por role."),
       ("rolesAndSubordinates", "string[]", "22.0", "Papéis e os abaixo deles; substituído por roleAndSubordinates."),
       ("territories", "string[]", "22.0", "Territórios que recebem acesso; substituído por territory."),
       ("territoriesAndSubordinates", "string[]", "22.0", "Territórios e os abaixo deles; substituído por territoryAndSubordinates."),
       ("territory", "string[]", "22.0", "Territórios que recebem acesso; com Sales Territories, no formato modelName.territoryName."),
       ("territoryAndSubordinates", "string[]", "22.0", "Territórios e os abaixo deles; com Sales Territories, no formato modelName.territoryName.")]
FILHOS = ("SharingCriteriaRule", "SharingOwnerRule", "SharingGuestRule", "SharingTerritoryRule")
estrutura("SharedTo", S_ST, [f"mdt:{n}" for n in FILHOS], [P(n, t, v, d_) for n, t, v, d_ in SHT],
          "Quem recebe o acesso de uma regra de compartilhamento (ou, em sharedFrom, de quem são os registros): grupos, papéis, territórios, filas "
          "ou guest users.")
estrutura("AccountSharingRuleSettings", S_SBR, ["mdt:SharingCriteriaRule", "mdt:SharingOwnerRule", "mdt:SharingTerritoryRule"], [
    P("caseAccessLevel", S, None, "Acesso aos casos ligados à conta.", "S", vals=valores("None", "Read", "Edit")),
    P("contactAccessLevel", S, None, "Acesso aos contatos ligados à conta.", "S", vals=valores("None", "Read", "Edit")),
    P("opportunityAccessLevel", S, None, "Acesso às oportunidades ligadas à conta.", "S", vals=valores("None", "Read", "Edit")),
], "O acesso que uma regra de compartilhamento de contas dá aos registros filhos da conta.")


def base(conta=True, de="SharingBaseRule"):
    rows = [P("accessLevel", S, None, "Nível de acesso dado pela regra.", "S", herdada=de)]
    if conta:
        rows.append(P("accountSettings", "AccountSharingRuleSettings", None, "Acesso aos casos, contatos e oportunidades da conta (regras de conta).",
                      estrutura="AccountSharingRuleSettings", herdada=de,
                      notas=["A página do tipo-base declara AccountSharingRuleSettings[]; a estrutura aparece uma vez por regra no exemplo."]))
    rows += [P("description", S, None, "Explica a regra; até 1.000 caracteres.", herdada=de),
             P("fullName", S, None, "Nome de API da regra; herdado do tipo Metadata.", herdada="Metadata"),
             P("label", S, None, "Rótulo da regra.", "S", herdada=de),
             P("sharedTo", "SharedTo", None, "Quem recebe o acesso.", "S", estrutura="SharedTo", herdada=de)]
    return rows


CRIT = [P("booleanFilter", S, None, "Lógica avançada que combina as condições."),
        P("criteriaItems", "FilterItem[]", None, "As condições que os registros precisam atender.", estrutura="FilterItem")]
ARQ_FILHO = lambda n: {  # noqa: E731
    "source_format": af("verificado", {"pasta": "sharingRules/", "arquivo": "<Objeto>.sharingRules-meta.xml", "elemento": "definido dentro do arquivo do tipo pai"},
                        "O registro do Salesforce CLI lista o tipo como filho de SharingRules, sem estratégia de decomposição.",
                        [ev("src:sdr-registry", f"types.sharingrules.children.types.{n.lower()}")]),
    "metadata_api_format": af("verificado", {"pasta": "sharingRules/", "arquivo": "<Objeto>.sharingRules", "elemento": "definido dentro do arquivo do tipo pai"},
                              "Um arquivo por objeto, com todas as regras dele.", [ev(S_SR)])}
EX_SR = CAB + f"""<!-- Arquivo sharingRules/<Objeto>.sharingRules -->
<SharingRules {NS}>
    <sharingCriteriaRules>
        <fullName>[Nome_Da_Regra]</fullName>
        <accessLevel>Read</accessLevel>
        <label>[rótulo]</label>
        <sharedTo>
            <group>[Nome_Do_Grupo]</group>
        </sharedTo>
        <criteriaItems>
            <field>[campo]</field>
            <operation>equals</operation>
            <value>[valor]</value>
        </criteriaItems>
        <includeRecordsOwnedByAll>true</includeRecordsOwnedByAll>
    </sharingCriteriaRules>
</SharingRules>"""

def ex_filho(n, corpo):
    el = n[0].lower() + n[1:] + "s"
    return CAB + f"""<!-- No arquivo sharingRules/<Objeto>.sharingRules, este conteúdo fica no elemento <{el}> -->
<{n} {NS}>
    <fullName>[Nome_Da_Regra]</fullName>
    <accessLevel>Read</accessLevel>
    <label>[rótulo]</label>
    <sharedTo>
        <group>[Nome_Do_Grupo]</group>
    </sharedTo>
{corpo}
</{n}>"""


CRIT_XML = """    <criteriaItems>
        <field>[campo]</field>
        <operation>equals</operation>
        <value>[valor]</value>
    </criteriaItems>"""
DE_XML = """    <sharedFrom>
        <role>[Nome_Do_Papel]</role>
    </sharedFrom>"""
tipo("SharingRules", S_SR,
     "O contêiner das regras de compartilhamento de um objeto: um arquivo por objeto, com as regras por critério, por dono, por território e "
     "de guest user.",
     "Versionar e implantar as regras que abrem acesso a registros além do padrão da org.", "24.0", [
         P("fullName", S, None, "Nome do objeto a que as regras pertencem; herdado do tipo Metadata.", herdada="Metadata"),
         P("sharingCriteriaRules", "SharingCriteriaRule[]", "33.0", "Regras por critério."),
         P("sharingGuestRules", "SharingGuestRule[]", "47.0", "Regras de guest user."),
         P("sharingOwnerRules", "SharingOwnerRule[]", "33.0", "Regras por dono."),
         P("sharingTerritoryRules", "SharingTerritoryRule[]", "33.0", "Regras por território."),
     ], exemplo=EX_SR, curinga=True,
     alertas=["Desde o Spring '20, só quem tem View Setup and Configuration acessa o tipo; editar exige Manage Sharing.",
              "Compartilhamento manual não é recuperado nem implantado.",
              "Até a API 32.0 havia um tipo por objeto (AccountSharingRules, CaseSharingRules, CustomObjectSharingRules e outros), removidos na 33.0."],
     divergencias=["A página escreve object.sharingRule num trecho e .sharingRules nos demais."],
     cobertura_nota="Universo esperado = tabela Fields da página do guia versionado 264.0, lida em 2026-11-17 (4 campos mais fullName herdado).")
tipo("SharingCriteriaRule", S_SR,
     "Uma regra de compartilhamento por critério: dá acesso aos registros que atendem a condições de campo.",
     "Versionar e implantar as regras por critério de um objeto.", "33.0",
     base() + CRIT + [P("includeRecordsOwnedByAll", B, None, "Inclui registros de donos sem papel, como usuários de alto volume, de sistema e de "
                                                               "processo automatizado.", "S", notas=["Não muda depois de criada a regra."])],
     parent="SharingRules", estende="SharingBaseRule", exemplo=ex_filho("SharingCriteriaRule", CRIT_XML + "\n    <includeRecordsOwnedByAll>true</includeRecordsOwnedByAll>"), arquivos_prontos=ARQ_FILHO("SharingCriteriaRule"), curinga=True,
     cobertura_nota="Universo esperado = campos do tipo na página de SharingRules mais os herdados de SharingBaseRule e Metadata.")
tipo("SharingOwnerRule", S_SR,
     "Uma regra de compartilhamento por dono: dá acesso aos registros que pertencem a um grupo, papel ou território.",
     "Versionar e implantar as regras por dono de um objeto.", "33.0",
     base() + [P("sharedFrom", "SharedTo", None, "De quem são os registros compartilhados. Com Sales Territories, territory e "
                                                  "territoryAndSubordinates usam modelName.territoryName.", "S", estrutura="SharedTo")],
     parent="SharingRules", estende="SharingBaseRule", exemplo=ex_filho("SharingOwnerRule", DE_XML), arquivos_prontos=ARQ_FILHO("SharingOwnerRule"), curinga=True,
     cobertura_nota="Universo esperado = campos do tipo na página de SharingRules mais os herdados de SharingBaseRule e Metadata.")
tipo("SharingGuestRule", S_SR,
     "Uma regra de compartilhamento de guest user: dá a usuários não autenticados de um site acesso de leitura a registros que atendem a "
     "condições.",
     "Versionar e implantar o acesso de guest users aos registros.", "47.0",
     base(conta=False) + [P("booleanFilter", S, "48.0", "Lógica avançada que combina as condições."),
                          P("criteriaItems", "FilterItem[]", "48.0", "As condições que os registros precisam atender.", estrutura="FilterItem"),
                          P("includeHVUOwnedRecords", B, "52.0", "Inclui registros de usuários de alto volume de sites.", "S", default=FALSE,
                            notas=["Sem ele, entram só registros de usuários autenticados, guest users e filas. Não muda depois de criada a regra."])],
     parent="SharingRules", estende="SharingBaseRule", exemplo=ex_filho("SharingGuestRule", CRIT_XML + "\n    <includeHVUOwnedRecords>false</includeHVUOwnedRecords>").replace("<group>[Nome_Do_Grupo]</group>", "<guestUser>[apelido do guest user]</guestUser>"), arquivos_prontos=ARQ_FILHO("SharingGuestRule"), curinga=True,
     alertas=["accessLevel só aceita Read.", "Herda de SharingBaseRule todos os campos, menos accountSettings."],
     cobertura_nota="Universo esperado = campos do tipo na página de SharingRules mais os herdados de SharingBaseRule (menos accountSettings) e Metadata.")
tipo("SharingTerritoryRule", S_SR,
     "Uma regra de compartilhamento por território: como a regra por dono, mas a origem dos registros é um território.",
     "Versionar e implantar as regras por território de um objeto.", "33.0",
     base(de="SharingOwnerRule") + [P("sharedFrom", "SharedTo", None, "De quem são os registros compartilhados.", "S", estrutura="SharedTo",
                                      herdada="SharingOwnerRule")],
     parent="SharingRules", estende="SharingOwnerRule", exemplo=ex_filho("SharingTerritoryRule", DE_XML.replace("<role>[Nome_Do_Papel]</role>", "<territory>[modelo.território]</territory>")), arquivos_prontos=ARQ_FILHO("SharingTerritoryRule"), curinga=True,
     cobertura_nota="A página não lista campos próprios; universo = campos herdados de SharingOwnerRule.")
for n in FILHOS:
    REG.append((S_SBR, "metadata-types", n))

# ================================================================ IndustriesSettings (190 opções booleanas)
IND = {
    "Financial Services Cloud": [
        ("allowBenefitAssignmentWithInactiveProgramEnrollment", "65.0", "Permite atribuir benefício com inscrição em programa inativa."),
        ("allowMultipleProducersToWorkOnSamePolicy", None, "Permite vários produtores na mesma apólice."),
        ("brwrCntctFrExtrnlSrcsPref", None, "Busca dados de contato do tomador em sistemas externos."),
        ("collectionAsaAgentPref", None, "Liga a preferência Collection as an Agent."),
        ("clctnAndRecoveryAgntPref", None, "Liga o agente de cobrança e recuperação."),
        ("createCustomerPropertyFromLAProperty", None, "Cria o imóvel do cliente a partir do imóvel da proposta de crédito."),
        ("createFinancialAccountFromLAAsset", None, "Cria contas financeiras a partir dos ativos da proposta de crédito."),
        ("createFinancialAccountFromLALiability", None, "Cria contas financeiras a partir dos passivos da proposta de crédito."),
        ("createFinancialAccountsFromLAFinancials", None, "Cria a conta financeira do financiamento a partir da proposta."),
        ("createFinancialAccountsFromLAProperty", None, "Cria a conta financeira do novo imóvel a partir do imóvel."),
        ("createFSCAssetFromLAAsset", None, "Cria registros de ativo a partir dos ativos da proposta."),
        ("createFSCAssetFromLAProperty", None, "Cria o ativo do imóvel adquirido a partir do imóvel."),
        ("createFSCLiabilityFromLAFinancial", None, "Cria o passivo do novo financiamento a partir do imóvel."),
        ("createFSCLiabilityFromLALiability", None, "Cria registros de passivo a partir dos passivos da proposta."),
        ("enableAccessToMasterListOfCoverageTypes", None, "Dá aos agentes de seguro acesso à lista principal de tipos de cobertura."),
        ("enableAccountScoreEnabled", None, "Liga o Account Scoring para contas de serviços financeiros."),
        ("enableB2B", None, "Liga os recursos B2B de serviços financeiros."),
        ("enableB2BAccountPlan", None, "Liga o planejamento de contas B2B para gerentes de relacionamento."),
        ("enableB2BEinstein", None, "Liga o Einstein para serviços financeiros B2B."),
        ("enableCallReportAdminContextPref", None, "Deixa o administrador controlar a visibilidade de Account Interactions."),
        ("enableCalculationUsingParentPolicyOnly", None, "Calcula prêmios só pela apólice-mãe."),
        ("enableCollectionFLowOps", None, "Liga fluxos automatizados de cobrança."),
        ("enableCollectionRiskScoringCFE", None, "Liga a pontuação de risco de cobrança com IA (CFE)."),
        ("enableCollectionTimeline", None, "Liga a linha do tempo das atividades de cobrança."),
        ("enableCompliantDataSharingForInteraction", None, "Liga o Compliant Data Sharing para Interaction."),
        ("enableClaimMgmt", None, "Liga avisos de primeira perda e gestão de participantes de sinistro."),
        ("enableCompliantDataSharingForAccount", None, "Liga o Compliant Data Sharing para Account."),
        ("enableCompliantDataSharingForCustomObjects", None, "Liga o Compliant Data Sharing para objetos customizados."),
        ("enableCompliantDataSharingForOpportunity", None, "Liga o Compliant Data Sharing para Opportunity."),
        ("enableCompliantDataSharingForInteractionSummary", None, "Liga o Compliant Data Sharing para Interaction Summary."),
        ("enableDealManagement", None, "Liga o Financial Deal Management."),
        ("enableDigitalLendingPref", None, "Liga a plataforma de crédito digital."),
        ("enableDigitalLendingReadOnlyOrgPref", None, "Deixa o Digital Lending somente leitura na org."),
        ("enableDiscoveryFrameworkMetadata", None, "Liga perguntas e conjuntos de perguntas de avaliação."),
        ("enableEinsteinDocReaderMappings", None, "Liga os mapeamentos do Intelligent Form Reader."),
        ("enableEnhancedQuestionCreation", None, "Liga a criação aprimorada de perguntas do Discovery Framework."),
        ("enableFinancialAccountMgmt", None, "Liga os objetos padrão de gestão de contas financeiras."),
        ("enableFinancialDealRoleHierarchy", None, "Faz o compartilhamento de deals seguir a hierarquia de papéis."),
        ("enableFinancialDealCallReportCmpPref", "54.0", "Permite usar junções de deal nos componentes de Interaction."),
        ("enableFinancialDealCallReportPref", "54.0", "Liga a junção entre deals e interações."),
        ("enableFSCInsuranceReport", "48.0", "Dá a gerentes de vendas acesso a dashboard e relatórios de seguros."),
        ("enableIndustriesAssessment", None, "Liga o Industries Assessment no Discovery Framework."),
        ("enableIndustriesKYC", None, "Liga o Industries KYC (Know Your Customer)."),
        ("enableInteractionRoleHierarchy", None, "Liga o compartilhamento por hierarquia de papéis em interações."),
        ("enableInteractionSummaryPref", None, "Liga a configuração Interaction Summary."),
        ("enableInteractionSummaryRoleHierarchy", None, "Liga o compartilhamento por hierarquia de papéis em resumos de interação."),
        ("enableManyToManyRelationships", None, "Permite ligações muitos-para-muitos entre sinistros, casos e ativos."),
        ("enableMortgageRlaTotalsOrgPref", None, "Liga os totais de ativos e passivos em propostas de crédito imobiliário."),
        ("enablePolicyAdministration", None, "Liga as entidades do modelo de administração de apólices."),
        ("enableRBLUsingCalcService", None, "Liga o Roll-by-Lookup pelo Calc Service."),
        ("enableRecordRollup", None, "Liga a otimização de Record Rollup."),
        ("enableReferralScoring", None, "Liga o Einstein Referral Scoring."),
        ("enableSlackForCib", None, "Liga recursos do Financial Services Cloud no Slack."),
        ("enableSyncInteractionsPref", None, "Sincroniza interações com o Einstein Activity Capture."),
        ("enableTimelinePref", None, "Liga os recursos de Timeline."),
        ("enableWealthManagementAIPref", "63.0", "Liga recursos de IA para gestão de patrimônio."),
        ("loanApplicantAddressAutoCreation", "51.0", "Cria automaticamente endereços de solicitante para contas pessoais."),
        ("loanApplicantAutoCreation", "51.0", "Cria automaticamente solicitantes de crédito para contas pessoais."),
        ("rlaEditIfAccHasEdit", None, "Exige edição na conta para editar a proposta de crédito."),
        ("showCollectionContactAndAccount", None, "Mostra contato e conta de cobrança nos fluxos."),
        ("transformRBLtoDPE", None, "Converte regras RBL em definições do Data Processing Engine."),
    ],
    "Health Cloud": [
        ("enableAuthorizationCustomSharingPCU", None, "Compartilhamento customizado para ver e gerir formulários de consentimento."),
        ("enableCandidateMatching", None, "Casa candidatos com estudos clínicos automaticamente."),
        ("enableCareMgmtSlackAccess", "56.0", "Liga o app Care Coordination for Slack."),
        ("enableClinicalDataModel", "51.0", "Liga o Clinical Data Model."),
        ("enableContactCenterAccess", "56.0", "Liga o app Contact Center for Health Cloud."),
        ("enableCustomFlowsOnCycleCount", "56.0", "Liga flows customizados na página Cycle Count."),
        ("enableCustomFlowsOnExpiryPage", "56.0", "Liga flows customizados na página Expiry."),
        ("enableDiseaseSurveillancePref", "64.0", "Liga a vigilância de doenças infecciosas."),
        ("enableHcCorePatientConsole", None, "Liga o console de pacientes pronto do Health Cloud."),
        ("enableHcStdRelationshipJunctions", None, "Usa as opções de group membership da plataforma em vez das do pacote."),
        ("enableHlsClinicalDcsnSuptAccessOrgPreference", None, "Liga o Clinical Decision Support."),
        ("enableHlsFhirSubscriptionSetting", None, "Liga os processos de Documentation Template Rule.",),
        ("enableIndustriesLPIPreference", "63.0", "Liga Licensing, Permitting, and Inspections."),
        ("enableLifeSciencesClinialTrialManagement", None, "Liga recrutamento e inscrição de participantes."),
        ("enableMedicationManagementEnabled", "53.0", "Liga o Medication Management."),
        ("enableMedicalDeviceEnabled", None, "Liga recursos de Intelligent Sales."),
        ("enableMedRecSetting", "54.0", "Liga a reconciliação de medicamentos."),
        ("enableMultipleCareProgramEnrolleeOrgPref", "49.0", "Liga a inscrição em vários programas de cuidado."),
        ("enableProviderSearchSyncOrgPref", None, "Sincroniza a busca de prestadores a cada seis horas."),
        ("enableRosterFileFeatureOrgPreference", None, "Define a preferência de roster file no Provider Network Management."),
        ("enableTrialManagementConsentManagement", None, "Liga a gestão de consentimento de candidatos a estudos."),
        ("enableUMPayerAppAccessOrgPreference", None, "Liga o app pronto de Utilization Management para operadoras."),
        ("enableVisitInventoryEnabled", None, "Liga o modelo de dados de visitas."),
        ("IsHomeHealthEnabled", None, "Permite agendar e realizar visitas de atendimento domiciliar."),
    ],
    "Life Sciences Cloud": [
        ("enableAccountBasedSharing", None, "Controla o acesso pelos donos das contas."),
        ("enableAdverseEvents", "61.0", "Liga Adverse Events e o modelo de dados dele."),
        ("enableAppAlerts", None, "Liga alertas e notificações no app."),
        ("enableCarePlansPreference", None, "Liga preferências de planos de cuidado."),
        ("enableComprehendMedical", "54.0", "Liga a análise Comprehend Medical."),
        ("enableCPBestConTimeSharing", None, "Compartilha o melhor horário de contato do paciente nos planos de cuidado."),
        ("enableCPSocialCustomSharing", None, "Liga compartilhamento social customizado nos planos de cuidado."),
        ("enableGroupMembershipPref", None, "Liga preferências de group membership."),
        ("enableIESentimentAnalysis", "54.0", "Liga o Industries Einstein Sentiment Insights."),
        ("enableIndCrossObjChangelog", None, "Liga um registro de mudanças entre objetos relacionados."),
        ("enableLifeSciGenericWorkflow", None, "Liga o motor genérico de workflow de ciências da vida."),
        ("enableLifeSciInquiry", None, "Liga a gestão e a resposta a consultas (inquiries)."),
        ("enableLifeSciListsAndFilters", None, "Liga listas e filtros de ordenação e busca."),
        ("enableLifeSciencesActivityPlan", None, "Liga planos de atividade."),
        ("enableLifeSciencesClinialTrailManagement", "61.0", "Liga o Clinical Trial Management e o modelo de dados dele."),
        ("enableLifeSciencesConsent", None, "Liga a gestão do consentimento de pacientes ou clientes."),
        ("enableLifeSciencesCustomerEngagementBase", None, "Liga os componentes de base do Customer Engagement."),
        ("enableLifeSciencesMergeManagement", None, "Liga a mesclagem de registros duplicados."),
        ("enableLifeSciencesProviderEngagementCompliance", None, "Liga recursos de conformidade no relacionamento com prestadores."),
        ("enableLifeSciencesSiteManagement", None, "Liga a gestão de centros de estudo e outros locais."),
        ("enableLSC4CEDocumentManagement", None, "Liga a gestão de documentos do Customer Engagement."),
        ("enableLSC4CEEmailAndTemplate", None, "Liga a gestão de e-mails e modelos."),
        ("enableLSC4CEKeyAccountManagement", None, "Liga o Key Account Management."),
        ("enableLSC4CEMedInsights", None, "Liga o Medical Insights para equipes médicas."),
        ("enableLSC4CEPackage", None, "Liga o pacote central do Customer Engagement."),
        ("enableLSC4CERemoteEngagement", None, "Liga o relacionamento remoto com clientes."),
        ("enableLSC4CEVisits", None, "Liga o registro de visitas a clientes."),
        ("enableNextBestAction", None, "Liga recomendações de próxima melhor ação por IA."),
        ("enableNextBestCustomer", None, "Indica os clientes de maior valor."),
        ("enableNextBestMessage", None, "Indica a mensagem mais eficaz a enviar."),
        ("enablePATSTerritoryBasedSharing", None, "Liga o compartilhamento por território do PATS."),
        ("enablePrimaryProviderRestriction", None, "Liga restrições pelo prestador principal."),
        ("enableProdAdminBusinessGrpFilter", None, "Liga o filtro por Business Group na administração de produtos."),
        ("enableProdTerrAlgnPrtHrchyAcc", None, "Liga o acesso à hierarquia de parceiros do Product Territory."),
        ("enableProdTerrAvlRecSharing", None, "Liga o compartilhamento dos registros disponíveis de Product Territory."),
        ("enableProviderSummarization", None, "Liga resumos de dados de prestadores."),
        ("enableSampleLimits", None, "Liga limites de amostras na distribuição de produtos."),
        ("enableTrialManagementRandomization", "61.0", "Liga procedimentos de randomização de estudos clínicos."),
        ("enableVisitPlanningAndExecutionAction", None, "Liga ações de planejamento e realização de visitas."),
        ("enableWaitlistManagementPref", None, "Liga preferências de gestão de lista de espera."),
        ("enableLSC4CEEDetailing", "63.0", "Liga o eDetailing do Customer Engagement."),
        ("enableLifeSciFieldEvents", "65.0", "Expõe campos de ciências da vida nos objetos de Event Management."),
        ("enableInsDocRelationship", "66.0", "Liga o record type de conta Institutional Doctor."),
        ("enableLSCAdminConsolePerms", "66.0", "Aplica as permissões do Admin Console por usuário."),
        ("enableStories", "67.0", "Liga Briefings, narrativas de insights em vários formatos."),
        ("enableMngEventBasedSharing", "67.0", "Liga o compartilhamento derivado de eventos para Subject Assignments."),
        ("enableEvtPtcpTypeRoleSelection", "67.0", "Mostra tipo e papel do participante como picklists."),
        ("enableMngEvtTypeAutoPopulation", "67.0", "Preenche o Managed Event Type pelo mapeamento de record type."),
        ("enableMngNonLSCShareRowCause", "67.0", "Inclui todos os tipos de compartilhamento nos fluxos de ciências da vida."),
        ("enableStoreCheck", "68.0", "Liga store checks na org."),
        ("enableLifeSciRecTypeRoutgPref", "68.0", "Encaminha usuários a experiências conforme o record type."),
        ("enableLSDraftOrderCapture", "68.0", "Liga a captura e a gestão de pedidos em rascunho."),
        ("enableLSVisitAgent", "68.0", "Liga o Visit Agent no app móvel."),
        ("noninterchangeable", "68.0", "Liga a execução seletiva de handlers de trigger por condições em JSON."),
    ],
    "Automotive Cloud": [("enableCriteriaBasedSearchAndFilter", None, "Liga a busca e o filtro por critérios.")],
    "Net Zero Cloud": [
        ("enableGnrcDisclsFrmwrk", "57.0", "Liga o Disclosure and Compliance Hub."),
        ("enableInformationLibrary", "59.0", "Liga o Information Library."),
        ("enableMaterialityAssessment", "59.0", "Liga a gestão de avaliações de materialidade."),
        ("enableNZCMngEsgPgm", "59.0", "Liga a gestão de programas ESG."),
        ("enableSCAssignFootprint", "54.0", "Liga a atribuição de pegadas de carbono a registros de consumo de energia."),
        ("enableSCBEIEnabled", "54.0", "Liga a gestão de intensidade energética de edifícios."),
        ("enableSCCarbonAccounting", "54.0", "Liga a contabilidade de carbono."),
        ("enableSCCarbonCreditAlloc", "56.0", "Liga a alocação de créditos de carbono a emissões inevitáveis."),
        ("enableSCCreateFootprint", "54.0", "Liga a criação automática de pegadas de carbono."),
        ("enableSCDGF", "54.0", "Liga a gestão de lacunas de dados."),
        ("enableSCExpansionUseCase", "57.0", "Liga a contabilidade de carbono para fronteiras organizacionais ampliadas."),
        ("enableSCExternalEngMgmt", "54.0", "Liga a gestão de dados de sustentabilidade de fornecedores."),
        ("enableSCEmssnsForecasting", "54.0", "Liga a previsão de emissões de carbono."),
        ("enableSCSNGManagement", "57.0", "Liga a gestão social e de governança."),
        ("enableSCScope3HubEnabled", "54.0", "Liga o hub de compras do Escopo 3."),
        ("enableSCTargetSetting", "54.0", "Liga a gestão de metas de emissão."),
        ("enableSCWasteManagement", "54.0", "Liga a gestão de dados de resíduos."),
        ("enableSCWaterManagement", "56.0", "Liga a gestão de dados de água."),
        ("enableSustainabilityCloud", "54.0", "Liga o Net Zero Cloud na org."),
    ],
    "Public Sector Solutions": [
        ("enableBenefitAndGoalSharingPref", None, "Liga o compartilhamento de benefícios e metas."),
        ("enableBenefitManagementPreference", None, "Liga a gestão de programas e benefícios."),
        ("enableEnhancedUIForISPref", "61.0", "Liga um único flow guiado para notas de interação."),
    ],
    "Salesforce Scheduler": [
        ("appointmentDistributionOrgPref", "52.0", "Agenda recursos pela distribuição de compromissos."),
        ("captureResourceUtilizationOrgPref", "52.0", "Calcula em segundo plano o uso de recursos a partir dos compromissos."),
        ("enableAnyResourceTypeOrgPref", "57.0", "Considera recursos de serviço do tipo Agent no agendamento."),
        ("enableAppFrmAnywhereOrgPref", "56.0", "Liga canais de engajamento para turnos, tipos de trabalho e reservas."),
        ("enableBlockResourceAvailabilityOrgPref", "47.0", "Inclui compromissos nos calendários Salesforce dos usuários."),
        ("enableCapacitySchedulingPref", "62.0", "Liga o agendamento por capacidade."),
        ("enableCreateMultiAttendeeEventOrgPref", "55.0", "Agrupa eventos numa única lista de participantes."),
        ("enableDropInAppointmentsOrgPref", "58.0", "Liga a gestão de participantes sem agendamento (drop-in)."),
        ("enableDropInSkillMatchingOrgPref", "58.0", "Liga o casamento de habilidades para recursos em lista de espera."),
        ("enableEventManagementOrgPref", "47.0", "Inclui compromissos nos calendários Salesforce."),
        ("enableEventWriteOrgPref", "49.0", "Publica eventos de alto volume quando compromissos mudam."),
        ("enableMultipleTopicsForShiftsOrgPref", "56.0", "Liga vários tópicos por turno."),
        ("enableMultiResourceOrgPref", "47.0", "Permite vários recursos de serviço por compromisso."),
        ("enableOverbookingOrgPref", "47.0", "Permite vários compromissos no mesmo horário."),
        ("enableShareSaWithArOrgPref", "55.0", "Compartilha compromissos com os recursos atribuídos."),
        ("enableTopicOrTemplate", "52.0", "Gere compromissos do Health Cloud com o Scheduler."),
        ("enableTopicTimeSlot", "52.0", "Horários de funcionamento para membros de grupos de tipos de trabalho."),
    ],
    "Education Cloud": [
        ("enableEducationCloud", "57.0", "Liga o Education Cloud."), ("enableStudentSuccess", "58.0", "Liga o Student Success."),
        ("enableAcademicOperations", "59.0", "Liga o Academic Operations."), ("enableAlumniRelations", "59.0", "Liga o Alumni Relations."),
        ("enableMentoring", "60.0", "Liga o Mentoring."), ("enableAdvancementGenAI", "64.0", "Liga os recursos de IA generativa de Advancement."),
        ("enableAdvisingAgent", "64.0", "Liga o Advising Agent."), ("enableEduAdvncdAcadOper", "64.0", "Liga os recursos avançados de Academic Operations."),
        ("enableStudentRecruitmentAgent", "64.0", "Liga o Student Recruitment Agent."),
    ],
    "Nonprofit Cloud": [("enableGiftEntryGrid", "64.0", "Liga o Gift Entry Grid."), ("enablePhilResearchAgent", "64.0", "Liga o Philanthropic Research Agent.")],
}
DUP = {"enableCarePlansPreference": ("Public Sector Solutions", "58.0", "Liga criar e editar planos de cuidado."),
       "enableVisitInventoryEnabled": ("Life Sciences Cloud", None, "Liga o controle de estoque nas visitas.")}
ind = []
for secao, linhas in IND.items():
    for nome, desde, desc in linhas:
        notas = [f"Seção {secao} da página."]
        if nome in DUP:
            s2, v2, d2 = DUP[nome]
            notas = [f"Aparece em duas seções da página: {secao} e {s2} ({d2.rstrip('.')}" + (f"; versão {v2}" if v2 else "") + ")."]
        kw = {"natureza": "desconhecida"} if nome == "enableEnhancedUIForISPref" else {}
        ind.append(P(nome, "não informado na página" if nome == "enableEnhancedUIForISPref" else B, desde, f"{secao}: {desc}", notas=notas, **kw))
ind.append(M.FULLNAME_HERDADO(None))
tipo("IndustriesSettings", S_IND,
     "As opções das nuvens de setor numa org: Financial Services Cloud, Health Cloud, Life Sciences Cloud, Net Zero Cloud, Public Sector, "
     "Salesforce Scheduler, Education Cloud, Nonprofit Cloud e Automotive Cloud. Cada opção liga um recurso de uma dessas nuvens.",
     "Recuperar e implantar as ativações das nuvens de setor, para repetir a mesma configuração em sandboxes e em produção.", "47.0", ind,
     exemplo=CAB + f"""<IndustriesSettings {NS}>
    <enableSustainabilityCloud>true</enableSustainabilityCloud>
    <enableClinicalDataModel>false</enableClinicalDataModel>
</IndustriesSettings>""", arquivos_prontos=M.arquivos_settings("IndustriesSettings", "Industries", S_IND),
     alertas=["Cada opção só existe nas edições em que a nuvem correspondente está ligada.",
              "A página avisa que parte da terminologia do produto mudou, mas o nome do tipo foi mantido para não quebrar implementações.",
              "Nem toda descrição bate com o nome: a de enableMedicalDeviceEnabled, por exemplo, fala em Intelligent Sales."],
     divergencias=["enableEnhancedUIForISPref aparece sem tipo na página.",
                   "enableCarePlansPreference e enableVisitInventoryEnabled aparecem em duas seções; foram cadastradas uma vez."],
     cobertura_nota="Universo esperado = os 192 itens das tabelas da página do guia versionado 264.0 (150 mil caracteres, lida por partes "
                    "em 2026-11-17), menos duas repetições: 190 opções, mais fullName herdado. A página não informa obrigatoriedade.")

# ================================================================ RevenueManagementSettings
RMS = [("enableAdvCreateOrdersFromQuote", "65.0", "Deixa escolher como criar vários pedidos a partir de uma cotação."),
       ("enableAdvancedDetailLinePricing", "65.0", "Liga o preço avançado nos itens de cotação e de pedido."),
       ("enableAsIsRenewals", "64.0", "Permite renovar ativos como estão."),
       ("enableAutoAddDerivedAsset", "62.0", "Inclui ativos de preço derivado quando os produtos que contribuem são incluídos."),
       ("enableAutoLineItemSequencing", "66.0", "Mantém a ordem automática dos itens da cotação ao pedido."),
       ("enableCoreCPQ", None, "Dá acesso de leitura e escrita aos recursos e objetos de Revenue Management."),
       ("enableDeltaPricing", "63.0", "Recalcula o preço só dos itens alterados da cotação ou do pedido."),
       ("enableGroupRamp", None, "Reservado para uso interno da Salesforce."),
       ("enableGroupRampMultiSchedulePref", "66.0", "Permite vários cronogramas de ramp por transação."),
       ("enableGroupRampPref", "65.0", "Cria ramp deals de vários produtos com segmentos de group ramp."),
       ("enableGroupRampTrialSegmentPref", "67.0", "Inclui segmentos de preço de teste nos cronogramas de group ramp."),
       ("enableRampDeal", "62.0", "Cria segmentos de ramp por item, com datas, quantidades e preços."),
       ("enableRevUnifiedSetup", None, "Liga um procedure plan para o cálculo de preço."),
       ("enableTransactionCloning", "64.0", "Clona a cotação ou o pedido inteiro, em vez de itens e grupos."),
       ("enableTransactionProcessor", "63.0", "Liga tipos de transação para cotações e pedidos; não pode ser desligado depois."),
       ("groupsEnabled", "62.0", "Permite agrupar itens de cotações e pedidos."),
       ("hidePriceRefreshNtfcn", "65.0", "Esconde o aviso de preços desatualizados na cotação ou no pedido."),
       ("relaxUniqueCipValidation", "64.0", "Permite customizar preços de itens de contrato ignorando validações de registro."),
       ("skipOrgSttPricing", None, "Ignora os procedimentos de preço padrão e de transação de venda; exige enableRevUnifiedSetup.")]
ARQ_RMS = {"source_format": af("verificado", {"pasta": "settings/", "arquivo": "revenuemanagement.settings-meta.xml"},
                               "Pasta e sufixo do tipo genérico Settings no registro do Salesforce CLI; o nome do arquivo vem da página do tipo.",
                               [ev("src:sdr-registry", "types.settings"), ev(S_RMS)]),
           "metadata_api_format": af("verificado", {"pasta": "settings/", "arquivo": "revenuemanagement.settings"},
                                     "Um único arquivo; no package.xml, o tipo é Settings. O nome do membro não foi confirmado.", [ev(S_RMS)])}
tipo("RevenueManagementSettings", S_RMS,
     "As opções de Revenue Management (Revenue Cloud): grupos de itens, ramp deals, preço incremental, renovações e criação de pedidos a partir "
     "de cotações.",
     "Recuperar e implantar a configuração de Revenue Management entre orgs.", "60.0", [P(n, B, v, d_) for n, v, d_ in RMS] + [M.FULLNAME_HERDADO(None)],
     arquivos_prontos=ARQ_RMS, exemplo=CAB + f"""<RevenueManagementSettings {NS}>
    <groupsEnabled>true</groupsEnabled>
    <enableRampDeal>true</enableRampDeal>
</RevenueManagementSettings>""",
     alertas=["Só existe em orgs com Revenue Management.", "enableTransactionProcessor não pode ser desligado depois de ligado.",
              "A página está no guia de Revenue Management, não no guia da Metadata API; não mostra número de versão da documentação."],
     divergencias=["A página escreve o arquivo em minúsculas (revenuemanagement.settings), ao contrário de outros tipos Settings."],
     cobertura_nota="Universo esperado = tabela de campos da página do guia de Revenue Management, lida em 2026-11-17 (19 campos). A página não "
                    "informa obrigatoriedade.")

M.emit_structs()
d = ld("estruturas/FilterItem.json")
d["usada_por"] = sorted(set(d["usada_por"]) | {"mdt:SharingCriteriaRule", "mdt:SharingGuestRule"})
sv("estruturas/FilterItem.json", d)

# ================================================================ funcionalidades novas
ACE, ORG, PRO, DAD = "acesso-identidade-e-seguranca", "organizacao-e-configuracoes-base", "processos-de-negocio-especificos-de-produto", "dados-e-modelagem"
C.funcionalidade(
    "hierarquia-de-papeis", "Hierarquia de papéis", "Role Hierarchy", ["roles", "papéis", "role", "userrole", "hierarquia de funções"],
    "A hierarquia de papéis organiza os usuários em níveis, como um organograma de acesso: quem está num papel vê e pode agir sobre os registros "
    "de quem está nos papéis abaixo.",
    "Dar a gestores acesso aos registros das equipes deles sem abrir esses registros para toda a org.",
    "O papel Gerente de Vendas Sul fica acima de Vendedor Sul; o gerente enxerga as oportunidades dos vendedores, mesmo com o padrão da org em "
    "Private.",
    (ACE, "acesso-a-registros-e-hierarquias"), [],
    [("Role", "Cada papel e o papel acima dele.")], [("UserRole", "O papel como registro."), ("User", "O papel de cada usuário (UserRoleId).")],
    [S_ROLE, S_ROT, S_UR, S_URF, "src:help-create-user-role", "src:objref-user"], [],
    setup("Setup > Quick Find: Roles > Roles > Set Up Roles > Add Role", "src:help-create-user-role",
          "Set Up Roles só aparece se a página Understanding Roles for exibida."),
    alertas=["Ver papéis exige View Roles and Role Hierarchy; criar, editar e excluir exige Manage Roles; atribuir usuários exige Manage "
             "Internal Users."])
C.funcionalidade(
    "regras-de-compartilhamento", "Regras de compartilhamento", "Sharing Rules",
    ["sharing rules", "compartilhamento", "criteria-based sharing", "owner-based sharing", "guest user sharing", "sharingrules"],
    "Regras de compartilhamento abrem acesso a registros além do padrão da org: por dono (registros de um grupo ou papel), por critério (registros "
    "com certos valores de campo) ou para guest users de um site.",
    "Dar a grupos de usuários acesso automático a registros que não são deles, sem mexer no padrão da org.",
    "Num objeto customizado de candidaturas, uma regra por critério compartilha com os gerentes de TI todas as candidaturas com Department = IT.",
    (ACE, "acesso-a-registros-e-hierarquias"), [],
    [("SharingRules", "O arquivo de regras de cada objeto."), ("SharingCriteriaRule", "Regra por critério."), ("SharingOwnerRule", "Regra por dono."),
     ("SharingGuestRule", "Regra de guest user."), ("SharingTerritoryRule", "Regra por território.")], [],
    [S_SR, S_SBR, S_ST, "src:help-sharing-rules-criteria", "src:help-sharing-rules-guest"],
    [sem("objeto_api", "Os objetos de compartilhamento (AccountShare, <Objeto>__Share) não foram cadastrados.")],
    setup("Setup > Quick Find: Sharing Settings > Sharing Settings > [objeto] Sharing Rules > New", "src:help-sharing-rules-criteria"),
    alertas=["Criar regras exige Manage Sharing.", "Regras de guest user só dão leitura; a Ajuda recomenda avaliar com cuidado o que fica exposto.",
             "Para usar public groups numa regra, crie os grupos antes."])
C.funcionalidade(
    "licencas-de-usuario", "Licenças de usuário e de permission set", "User Licenses and Permission Set Licenses",
    ["user license", "licença", "permission set license", "feature license", "userlicense"],
    "A licença de usuário define o pacote básico do que um usuário pode ter; cada perfil pertence a uma licença. Feature licenses e permission set "
    "licenses liberam recursos que a licença de usuário não inclui.",
    "Saber o teto do que pode ser dado a cada usuário antes de montar perfis e permission sets.",
    "A licença Salesforce Platform não inclui leads, oportunidades, campanhas nem previsões; um usuário com ela não recebe esses acessos por "
    "nenhum perfil.",
    (ACE, "licencas-e-entitlements-de-acesso"), [],
    [("Profile", "A licença do perfil (userLicense)."), ("PermissionSet", "A licença associada ao permission set (license).")],
    [("Profile", "A licença do perfil (UserLicenseId)."), ("PermissionSet", "A licença do permission set (LicenseId).")],
    ["src:help-user-licenses", "src:help-service-feature-license", "src:mdapi-profile", "src:mdapi-permissionset", "src:objref-permissionset"],
    [sem("objeto_api", "Os objetos UserLicense, PermissionSetLicense e PermissionSetLicenseAssign não foram cadastrados."),
     sem("metadata_type", "Licenças não são implantadas como metadado; vêm do contrato da org.", "nao_aplicavel")],
    af("desconhecido", None, "Caminho de Setup não lido nesta rodada.", []),
    alertas=["Licenças vêm do contrato da org; o catálogo não registra quantidades nem preços."])
C.funcionalidade(
    "configuracoes-de-nuvens-de-setor", "Configurações das nuvens de setor", "Industries Settings",
    ["industriessettings", "industries", "financial services cloud", "health cloud", "life sciences cloud", "net zero cloud", "education cloud"],
    "As nuvens de setor (Financial Services, Health, Life Sciences, Net Zero, Education, Nonprofit, Public Sector e outras) acrescentam objetos "
    "e recursos ao modelo padrão. Os recursos opcionais de cada uma são ligados por opções guardadas num único tipo, IndustriesSettings.",
    "Ligar recursos de uma nuvem de setor e repetir a mesma configuração entre orgs.",
    "Uma org de Net Zero Cloud liga enableSustainabilityCloud e enableSCCarbonAccounting; o arquivo Industries.settings leva as duas opções para "
    "a sandbox seguinte.",
    (PRO, "capacidades-setoriais"), [(ORG, "settings", "É um tipo da família Settings."), (ORG, "habilitacao-de-recursos", "Cada opção ativa um recurso opcional.")],
    [("IndustriesSettings", "As opções de todas as nuvens de setor.")], [],
    [S_IND, "src:help-industries-data-models"], [sem("objeto_api", "Os objetos de cada nuvem de setor não foram cadastrados.")],
    af("desconhecido", None, "Cada nuvem tem a própria página de configuração; nenhuma foi lida nesta rodada.", []),
    alertas=["Cada opção só existe nas edições com a nuvem correspondente."])
C.funcionalidade(
    "revenue-management", "Revenue Management", "Revenue Management", ["revenue cloud", "revenuemanagementsettings", "ramp deal", "rlm"],
    "Revenue Management (Revenue Cloud) cuida do ciclo de receita depois da venda acertada: catálogo, preço, cotações, pedidos, ativos e "
    "renovações. As opções gerais ficam no tipo RevenueManagementSettings.",
    "Ligar e versionar as opções de Revenue Management numa org que tem o produto.",
    "Uma empresa de software liga groupsEnabled e enableRampDeal para vender contratos de três anos com preço crescente por ano.",
    (PRO, "receita-e-comercio"), [(ORG, "settings", "As opções gerais ficam num tipo da família Settings.")],
    [("RevenueManagementSettings", "As opções gerais do produto.")], [],
    [S_RMS, "src:help-revenue-get-started"], [sem("objeto_api", "Os objetos de Revenue Management não foram cadastrados.")],
    af("desconhecido", None, "Caminho de Setup não lido nesta rodada.", []),
    alertas=["Só existe em orgs com Revenue Management.", "Ligar enableTransactionProcessor não tem volta."])

# ================================================================ secundárias que dão funcionalidades aos temas internos
for fid, cls, sub, motivo, srcs in [
    ("field-history-tracking", DAD, "metadados-de-configuracao-de-dados", "Liga o histórico por opções do objeto e do campo, sem criar dados novos.", ["src:mdapi-customfield"]),
    ("campos-customizados", DAD, "metadados-de-configuracao-de-dados", "External ID e Unique são opções do campo (externalId, unique).", ["src:mdapi-customfield"]),
    ("external-objects", DAD, "modelos-externos-e-especializacoes", "Objetos externos mostram dados de outro sistema sem copiá-los.", []),
    ("field-audit-trail", DAD, "modelos-externos-e-especializacoes", "O histórico arquivado fica num big object (FieldHistoryArchive).", []),
    ("objetos-customizados", DAD, "modelos-externos-e-especializacoes", "Big objects são objetos com sufixo __b, com índice próprio (Index).", ["src:mdapi-index"]),
    ("lightning-knowledge", ORG, "habilitacao-de-recursos", "Ligar o Lightning Knowledge não tem volta e muda o modelo de dados.", ["src:help-lightning-knowledge-enable"]),
    ("multiplas-moedas", ORG, "habilitacao-de-recursos", "Depois de ligar múltiplas moedas, não dá para desligar.", []),
    ("digital-experiences", ORG, "habilitacao-de-recursos", "Depois de ligar digital experiences, não dá para desligar.", []),
    ("lightning-knowledge", ORG, "settings", "As opções ficam em KnowledgeSettings.", []),
    ("previsoes-colaborativas", ORG, "settings", "As opções ficam em ForecastingSettings.", []),
    ("chatter", ORG, "settings", "As opções ficam em ChatterSettings.", []),
    ("path", ORG, "settings", "A ativação fica em PathAssistantSettings.", []),
    ("consent-management", ORG, "settings", "As opções ficam em PrivacySettings.", []),
    ("multiplas-moedas", ORG, "settings", "As opções ficam em CurrencySettings.", []),
    ("my-domain", ORG, "settings", "As opções ficam em MyDomainSettings.", []),
]:
    C.secundaria(fid, cls, sub, motivo, srcs)

# ================================================================ caminhos de Setup (issue #8)
for fid, valor, src, nota in [
    ("perfis", "Setup > Quick Find: Profiles > Profiles", "src:help-create-clone-profiles", "Lista de perfis; para clonar, abra um perfil e clique em Clone."),
    ("tipos-de-registro", "Setup > Object Manager > [objeto] > Record Types > New", "src:help-create-record-types", "A partir das configurações do objeto."),
    ("contas", "Setup > Quick Find: Account Settings > Account Settings", "src:help-shared-contacts-setup", "Página das opções de contas; ver ou editar exige Customize Application."),
    ("contatos", "Setup > Quick Find: Account Settings > Account Settings > Allow users to relate a contact to multiple accounts",
     "src:help-shared-contacts-setup", "Opção Contacts to Multiple Accounts, que fica nas configurações de contas."),
    ("oportunidades", "Setup > Quick Find: Opportunity Settings > Opportunity Settings", "src:help-kb-opportunity-settings", "Página das opções de oportunidades."),
    ("casos", "Setup > Quick Find: Support Settings > Support Settings", "src:help-suggested-articles-cases", "Página das opções de atendimento (casos)."),
    ("campanhas", "Setup > Quick Find: Influence > Campaign Influence Settings", "src:help-campaign-influence-enable", "Opções de Campaign Influence."),
    ("produtos-e-catalogos-de-preco", "Setup > Quick Find: Product Settings > Product Settings", "src:help-product-settings", "Página das opções de produtos."),
    ("previsoes-colaborativas", "Setup > Quick Find: Forecasts Settings > Forecasts Settings", "src:help-forecasts-settings",
     "Desde o Winter '24, a previsão já vem ligada com tipos padrão."),
    ("equipes-de-conta-e-oportunidade", "Setup > Quick Find: Account Teams > Account Teams; Setup > Quick Find: Opportunity Team Settings > Opportunity Team Settings",
     "src:help-account-teams-enable", "Duas páginas: uma para equipes de conta, outra para equipes de oportunidade (Enable Team Selling)."),
]:
    srcs = [src] + (["src:help-opportunity-teams-enable"] if fid == "equipes-de-conta-e-oportunidade" else [])
    C.definir_setup(fid, valor, nota, srcs)

# ================================================================ nota de extração: lista de campos
ls = ["", "-- Lista de campos transcrita da leitura (gerada por lote7m_b4_acesso_temas.py; nome | tipo)"]
for src, pasta, nome in REG:
    ls.append(f"[{src}] {nome}: " + ", ".join(f"{q['nome']} | {q['tipo_tecnico']}" for q in ld(f"{pasta}/{nome}.json")["propriedades"]))
ls.append(f"[{S_UR}] objeto UserRole: " + ", ".join(f"{c['nome']} | {c['tipo_tecnico']}" for c in ur))
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(ls) + "\n")
print("lote 7m: ok")
