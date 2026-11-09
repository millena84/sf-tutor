# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 3b: restante de Agentforce Sales e Service (insumo do relatório de pesquisa de 2026-11-08,
# com releitura direta das páginas oficiais). Aplica por load/modify/save; não reexecutar run.py.
import json
import b2_mdt as M
from b1_base import ev, af
from b3_obj import field, expo, obj, rel, cob, cnt, func, APEX_OK

BASE = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/"
CAT = BASE + "catalogo/"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")

# ================================================================ fontes
reg = json.load(open(BASE + "fontes/registro.json"))
B = "https://developer.salesforce.com/docs/atlas.en-us.264.0."
H = "https://help.salesforce.com/s/articleView?id="
CHK = {"estado": "verificado", "nota": "Conteúdo lido em 2026-11-08 e conferido quanto ao assunto (não apenas HTTP 200)."}
def src(id, t, u, pert, extr, ver="68.0", metodo="extracao_documental_assistida", tipo="oficial_documentacao"):
    return {"id": id, "titulo": t, "url": u, "tipo": tipo, "versao": ver, "data_verificacao": "2026-11-08", "metodo": metodo, "pertinencia": pert,
            "extracao": "fontes/extracoes/" + extr, "checagem_online": CHK}
novas = [
 src("src:mdapi-entitlementprocess", "EntitlementProcess (Metadata API)", B + "api_meta.meta/api_meta/meta_entitlementprocess.htm", "Arquivo, versão e propriedades do tipo EntitlementProcess e subtipos.", "mdapi-EntitlementProcess.txt"),
 src("src:mdapi-territory2model", "Territory2Model (Metadata API)", B + "api_meta.meta/api_meta/meta_territory2model.htm", "Arquivo, versão, restrições de deploy e propriedades de Territory2Model.", "mdapi-Territory2Model.txt"),
 src("src:mdapi-servicepresencestatus", "ServicePresenceStatus (Metadata API)", B + "api_meta.meta/api_meta/meta_servicepresencestatus.htm", "Arquivo, versão e propriedades de ServicePresenceStatus.", "mdapi-ServicePresenceStatus.txt"),
]
for n, t, pert in [("account", "Account", "Chamadas e campos do objeto Account."), ("contact", "Contact", "Chamadas e parte dos campos do objeto Contact."),
                   ("accountteammember", "AccountTeamMember", "Chamadas, campos e disponibilidade de AccountTeamMember."),
                   ("opportunityteammember", "OpportunityTeamMember", "Chamadas, campos e notas de uso de OpportunityTeamMember."),
                   ("leadstatus", "LeadStatus", "Chamadas e campos de LeadStatus."), ("casemilestone", "CaseMilestone", "Chamadas e campos de CaseMilestone."),
                   ("businesshours", "BusinessHours", "Chamadas, campos e notas de uso de BusinessHours.")]:
    novas.append(src(f"src:objref-{n}", f"{t} (Object Reference)", B + f"object_reference.meta/object_reference/sforce_api_objects_{n}.htm", pert, f"objref-{t}.txt"))
for sid, t, art, pert in [
 ("help-quotes-setup", "Set Up Quotes", "quotes_enable.htm", "Caminho Quote Settings, edições e permissão para habilitar cotações."),
 ("help-quotes-noopp", "Enable Quote Creation Without a Related Opportunity", "sales.cpq_quotes_without_opportunities.htm", "Cotações sem oportunidade exigem licença Sales Cloud."),
 ("help-tm2-enable", "Enable Sales Territories", "tm2_enable_tm2.htm", "Caminho Territory Settings, edições e permissão."),
 ("help-tm2-activate", "Activate a Territory Model", "sf.tm2_activate_territory_model.htm", "Permissões para ativar modelo; um modelo ativo por vez."),
 ("help-kb-sales-territories", "Enable Sales Territories (Formerly Known as Enterprise Territory Management) (KB)", "000396697&type=1", "Novo nome Sales Territories (antes Enterprise Territory Management)."),
 ("help-omni-enable", "Enable and Configure Omni-Channel", "omnichannel_enable.htm", "Caminho Omni-Channel Settings, licenças e aposentadoria do Standard Omni-Channel."),
 ("help-omni-upgrade", "Upgrade Standard Omni-Channel to Enhanced", "service.omnichannel_upgrade_standard_to_enhanced.htm", "Enhanced por padrão em orgs após Summer '23; canais standard não suportados."),
 ("help-lk-enable", "Enable Lightning Knowledge", "service.knowledge_lightning_enable.htm", "Caminho Knowledge Settings, licença Knowledge User e irreversibilidade."),
 ("help-ent-sla", "Simplified SLA Setup: Configure Entitlements and Milestones", "service.entitlements_simplified_sla_setup_parent.htm", "Caminho Entitlement Settings e novos nomes SLA Management/SLA Policies."),
 ("help-rn-sla-ga", "Set Up SLA Management Faster with the New Simplified Setup Experience (GA)", "release-notes.rn_entitlements_sla_simplification_ga.htm&release=258", "Edições com Service Cloud em que a configuração simplificada se aplica."),
 ("help-ent-process-create", "Create an Entitlement Process", "entitlements_process_create.htm", "Caminho Entitlement Processes e permissão Manage Entitlements."),
 ("help-bh", "Set Business Hours", "service.customize_supporthours.htm", "Caminho Business Hours, permissão e padrão 24x7."),
 ("help-ent-bh", "How Business Hours Work in Entitlement Management", "sf.entitlements_business_hours.htm", "Precedência de business hours: milestone > processo > caso."),
 ("help-assign-guide", "Guidelines for Assignment Rules", "sf.customize_leadrules.htm", "Caminho Lead/Case Assignment Rules e limites por regra."),
 ("help-assign-setup", "Set Up Assignment Rules", "sf.creating_assignment_rules.htm", "Entradas de regra e atribuição a usuário ou fila."),
 ("help-console-create", "Create and Edit a Custom Lightning Console App", "sf.console_lex_create_custom.htm", "Caminho App Manager, edições e permissões de apps de console."),
 ("help-console-intro", "Salesforce Console in Lightning Experience", "sf.console_lex_intro.htm", "Permissão Lightning Console User para usar apps de console."),
 ("help-service-console-customize", "Best Practices for Customizing the Lightning Service Console", "console_lex_service_customize.htm&type=0", "Service Console: edições com Service Cloud e itens padrão.")]:
    novas.append(src("src:" + sid, t, H + art, pert, "help-nuvens-lote3b.txt", "sem versão (Ajuda Salesforce)", "leitura_resultado_busca", "oficial_ajuda"))
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

# ================================================================ metadata types
MDT = "src:mdapi-entitlementprocess"
M.struct("EntitlementProcessMilestoneItem", MDT, ["mdt:EntitlementProcess"], [
 ("businessHours", "string", "N", "30.0", "Business hours aplicadas ao milestone."),
 ("criteriaBooleanFilter", "string", "N", None, "Lógica de filtro para milestones que valem quando critérios são atendidos."),
 ("milestoneCompletionCriteria", "string", "N", None, "Critério para marcar o milestone como concluído."),
 ("milestoneCriteriaFilterItems", "FilterItem[]", "N", None, "Critérios exigidos para o milestone valer.", {"estrutura": "FilterItem"}),
 ("milestoneCriteriaFormula", "string", "N", None, "Fórmula que precisa ser verdadeira para o milestone valer."),
 ("milestoneName", "string", "N", None, "Nome do milestone."),
 ("minutesCustomClass", "string", "N", "30.0", "Classe Apex que calcula o tempo do gatilho."),
 ("minutesToComplete", "int", "N", None, "Minutos após a entrada do caso até o milestone."),
 ("successActions", "WorkflowActionReference[]", "N", None, "Ações executadas quando o milestone é concluído."),
 ("timeTriggers", "EntitlementProcessMilestoneTimeTrigger[]", "N", None, "Gatilhos de tempo do milestone.", {"estrutura": "EntitlementProcessMilestoneTimeTrigger"}),
 ("useCriteriaStartTime", "boolean", "N", None, "Se o milestone começa quando os critérios são atendidos ou na entrada do processo.")],
 "Milestone (etapa com prazo) dentro de um processo de entitlement.")
M.struct("EntitlementProcessMilestoneTimeTrigger", MDT, ["mdx:EntitlementProcessMilestoneItem"], [
 ("actions", "WorkflowActionReference[]", "N", None, "Ações executadas no momento do gatilho, se o milestone ainda estiver aberto."),
 ("timeLength", "int", "N", None, "Distância entre o gatilho e a data-alvo: negativo é aviso, positivo é violação."),
 ("workflowTimeTriggerUnit", "MilestoneTimeUnits", "N", None, "Unidade de tempo do gatilho.", {"vals": [("Minutes", None), ("Hours", None), ("Days", None)], "natureza": "enum_fechado"})],
 "Gatilho de tempo de um milestone (aviso antes ou violação depois do prazo).")
SPS = "src:mdapi-servicepresencestatus"
M.struct("ServiceChannelStatus", SPS, ["mdt:ServicePresenceStatus"], [
 ("channel", "string", "N", None, "Canal de serviço associado ao status de presença.")], "Canal de serviço associado a um status de presença.")

M.mdt("EntitlementProcess", MDT, "Define um processo de entitlement (na configuração simplificada, SLA Policy): a linha do tempo de milestones que o atendimento precisa cumprir.",
      "Aplicar níveis de serviço (prazos de resposta e resolução) a casos ou ordens de trabalho.", "27.0", [
 ("active", "boolean", "N", None, "Se o processo está ativo."),
 ("businessHours", "string", "N", "30.0", "Business hours aplicadas ao processo."),
 ("description", "string", "N", None, "Descrição do processo."),
 ("entryStartDateField", "string", "N", None, "Campo de data do caso usado para a entrada no processo, quando a entrada é por data."),
 ("exitCriteriaBooleanFilter", "string", "N", None, "Lógica que combina os critérios de saída."),
 ("exitCriteriaFilterItems", "FilterItem[]", "N", None, "Critérios que fazem o caso sair do processo.", {"estrutura": "FilterItem"}),
 ("exitCriteriaFormula", "string", "N", None, "Fórmula que, verdadeira, faz o caso sair do processo."),
 ("isVersionDefault", "boolean", "N", "28.0", "Se esta versão é a padrão."),
 ("milestones", "EntitlementProcessMilestoneItem[]", "N", None, "Milestones do processo.", {"estrutura": "EntitlementProcessMilestoneItem"}),
 ("name", "string", "N", None, "Nome do processo exibido na interface."),
 ("SObjectType", "string", "N", None, "Tipo de registro em que o processo roda (por exemplo, caso ou ordem de trabalho)."),
 ("versionMaster", "string", "N", "28.0", "Identificador comum a todas as versões do mesmo processo."),
 ("versionNotes", "string", "N", "28.0", "Descrição desta versão."),
 ("versionNumber", "int", "N", "28.0", "Número da versão, começando em 1.")],
 setup=af("verificado", "Setup > Quick Find: Entitlement Processes > Entitlement Processes (Entitlement Management) > New Entitlement Process",
          "É preciso criar milestones antes. Rótulos em inglês, como na Ajuda.", [ev("src:help-ent-process-create")]), curinga=True,
 alertas=["O nome do arquivo inclui a versão quando houver (ex.: gold_support_v2.entitlementProcess).",
          "Na configuração simplificada (Simplified SLA Setup), o processo se chama SLA Policy e não há versionamento (Ajuda)."],
 divergencias=["O relatório de pesquisa de 2026-11-08 citou entitlementRules, isRecordTypeApplied e recordType; a página 68.0 relida não tem essas linhas (14 propriedades)."])
M.mdt("Territory2Model", "src:mdapi-territory2model", "Define um modelo de territórios de vendas (Sales Territories): a estrutura que agrupa territórios, regras e atribuições.",
      "Versionar e implantar a estrutura de territórios entre orgs.", "32.0", [
 ("customFields", "FieldValue", "N", None, "Campos customizados usados pelo modelo; valores obrigatórios são exigidos no deploy."),
 ("description", "string", "N", None, "Descrição do modelo."),
 ("name", "string", "S", None, "Rótulo do modelo na interface.")],
 setup=af("verificado", "Setup > Quick Find: Territories > Territory Settings > Enable Sales Territories; depois, página Territory Models no Setup",
          "Habilitar exige Customize Application; criar e ativar modelos exige View Setup and Configuration e Manage Territories.", [ev("src:help-tm2-enable"), ev("src:help-tm2-activate")]),
 curinga=True,
 alertas=["Requer Sales Territories habilitado.", "Sem suporte a packaging, change sets e chamadas CRUD.",
          "deploy() exige Manage Territories e só funciona em modelos Planning ou Active; modelos Archived bloqueiam o deploy.",
          "Sem Manage Territories, retrieve() traz só entidades de modelos ativos (dado parcial)."],
 divergencias=["O relatório de pesquisa de 2026-11-08 citou recordVisibility e userRecordAccess; a página 68.0 relida tem só customFields, description e name.",
                           "A página menciona um campo State da API SOAP fora da tabela de propriedades."])
M.mdt("ServicePresenceStatus", SPS, "Define um status de presença do Omni-Channel (por exemplo, disponível para um canal).",
      "Controlar em quais canais o atendente fica disponível ao escolher o status.", "44.0", [
 ("channels", "ServiceChannelStatus", "N", None, "Canais associados ao status; sem canais, o status vira ausente (IsAway = true).", {"estrutura": "ServiceChannelStatus"}),
 ("label", "string", "N", None, "Rótulo do status de presença."),
 M.FULLNAME_HERDADO(SPS)], curinga=True, alertas=["Requer Omni-Channel habilitado."])
M.emit_structs()
fi = ld("estruturas/FilterItem.json")
fi["usada_por"] = sorted(set(fi["usada_por"]) | {"mdt:EntitlementProcess", "mdx:EntitlementProcessMilestoneItem"})
sv("estruturas/FilterItem.json", fi)

# ================================================================ objetos
def lista(nome_obj, nomes, det, s, nota):
    out = []
    for n in nomes:
        if n in det: out.append(det[n]); continue
        f = field("obj:" + nome_obj, n, "(a extrair)", None, None, None, s); f["notas"] = [nota]; out.append(f)
    return out
NOTA_NOME = "Nome listado na Object Reference; tipo e propriedades não extraídos nesta rodada."
TOOL_D = lambda: expo("tooling", "desconhecido", nota="Exposição na Tooling API não verificada.")

# Account
A = "src:objref-account"; O = "obj:Account"
acc_nomes = ("AccountNumber, AccountSource, ActivityMetricId, ActivityMetricRollupId, AnnualRevenue, BillingAddress, BillingCity, BillingCountry, BillingCountryCode, BillingGeocodeAccuracy, "
 "BillingLatitude, BillingLongitude, BillingPostalCode, BillingState, BillingStateCode, BillingStreet, ChannelProgramLevelName, ChannelProgramName, CleanStatus, CommerceCustomerReference, "
 "CommerceGroupReference, CommerceOrganizationReference, ConnectionReceivedId, ConnectionSentId, Description, DunsNumber, Fax, Industry, IsBuyer, IsCustomerPortal, IsPartner, IsPersonAccount, "
 "IsPriorityRecord, Jigsaw, JigsawCompanyId, LastActivityDate, LastReferencedDate, LastViewedDate, MasterRecordId, NaicsCode, NaicsDesc, Name, NumberOfEmployees, OperatingHoursId, OwnerId, "
 "Ownership, ParentId, PersonActionCadenceAssigneeId, PersonActionCadenceId, PersonActionCadenceState, PersonIndividualId, PersonScheduledResumeDateTime, Phone, PhotoUrl, Rating, RecordTypeId, "
 "Salutation, ShippingAddress, ShippingCity, ShippingCountry, ShippingCountryCode, ShippingGeocodeAccuracy, ShippingLatitude, ShippingLongitude, ShippingPostalCode, ShippingState, "
 "ShippingStateCode, ShippingStreet, Sic, SicDesc, Site, TickerSymbol, Tradestyle, Type, Website, YearStarted").split(", ")
acc_det = {
 "Name": field(O, "Name", "string", "CFGSU", None, "Nome da conta.", A, req=("sim", None)),
 "ParentId": field(O, "ParentId", "reference", "CFGNSU", None, "Conta-mãe, para hierarquias de contas.", A, ref=["obj:Account"]),
 "OwnerId": field(O, "OwnerId", "reference", "CDFGSU", None, "Dono da conta; na criação, assume o usuário da API se não informado.", A, ref=["obj:User"]),
 "RecordTypeId": field(O, "RecordTypeId", "reference", "CFGNSU", None, "Tipo de registro da conta.", A),
 "Type": field(O, "Type", "picklist", "CFGNSU", None, "Tipo da conta (por exemplo, cliente ou parceiro).", A),
 "Industry": field(O, "Industry", "picklist", "CFGNSU", None, "Setor de atuação da conta.", A),
 "AccountSource": field(O, "AccountSource", "picklist", "CFGNSU", None, "Origem da conta.", A),
 "IsPersonAccount": field(O, "IsPersonAccount", "boolean", "DFGS", None, "Indica se é uma conta pessoal (somente leitura).", A),
 "MasterRecordId": field(O, "MasterRecordId", "reference", "FGNS", None, "Conta sobrevivente quando esta foi excluída por mesclagem.", A, ref=["obj:Account"]),
}
acc_campos = lista("Account", acc_nomes, acc_det, A, NOTA_NOME)
obj("Account", "Representa uma conta: uma organização ou pessoa envolvida com o negócio (cliente, concorrente, parceiro).", "Registro central de clientes, ao qual se ligam contatos, oportunidades e casos.",
    [expo("padrao", "verificado", A, ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "merge()", "query()", "retrieve()", "search()", "undelete()", "update()", "upsert()"]), TOOL_D()],
    acc_campos, [{"api": "padrao", "soql": "SELECT Name, Type, Industry FROM Account WHERE ParentId = null LIMIT 20", "contexto": "API padrão (REST /query ou SOAP query()).", "validacao": "documental"}],
    APEX_OK(A), cob("parcial", None, len(acc_campos), cnt(acc_campos), "Tabela principal de campos lida completa (76). A segunda tabela, de campos de conta pessoal (IsPersonAccount Fields), foi servida truncada e não entrou."), A)

# Contact
C = "src:objref-contact"; O = "obj:Contact"
ct_nomes = ("AccountId, ActionCadenceAssigneeId, ActionCadenceId, ActionCadenceState, ActiveTrackerCount, ActivityMetricId, ActivityMetricRollupId, AssistantName, AssistantPhone, Birthdate, "
 "BuyerAttributes, CanAllowPortalSelfReg, CleanStatus, CommerceCustomerReference, CommerceGroupReference, CommerceOrganizationReference, ConnectionReceivedId, ConnectionSentId, ContactSource, "
 "Department, DepartmentGroup, Description, DoNotCall, Email, EmailBouncedDate, EmailBouncedReason, Fax, FirstCallDateTime, FirstEmailDateTime, FirstName, GenderIdentity, HasOptedOutOfEmail, "
 "HasOptedOutOfFax, HomePhone, IndividualId, IsDeleted, IsEmailBounced").split(", ")
ct_det = {
 "AccountId": field(O, "AccountId", "reference", "CFGNSU", None, "Conta à qual o contato pertence.", C, ref=["obj:Account"]),
 "FirstName": field(O, "FirstName", "string", "CFGNSU", None, "Nome do contato.", C),
 "Email": field(O, "Email", "email", "CFGNSUI", None, "E-mail do contato.", C),
}
ct_campos = lista("Contact", ct_nomes, ct_det, C, NOTA_NOME)
obj("Contact", "Representa uma pessoa, normalmente associada a uma conta.", "Registro das pessoas com quem a empresa se relaciona.",
    [expo("padrao", "verificado", C, ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "merge()", "query()", "retrieve()", "search()", "undelete()", "update()", "upsert()"]), TOOL_D()],
    ct_campos, [{"api": "padrao", "soql": "SELECT FirstName, Email, AccountId FROM Contact LIMIT 20", "contexto": "API padrão (REST /query ou SOAP query()).", "validacao": "documental"}],
    APEX_OK(C), cob("parcial", None, len(ct_campos), cnt(ct_campos), "Object Reference servida truncada: a tabela termina em IsEmailBounced (37 nomes). LastName, OwnerId, RecordTypeId e outros campos posteriores não foram servidos."), C)

# AccountTeamMember
T = "src:objref-accountteammember"; O = "obj:AccountTeamMember"
VAL_ATM = "Valores conforme a página; não se declara lista completa."
atm = [
 field(O, "AccountAccessLevel", "picklist", "CFGNSU", None, "Nível de acesso do membro à conta.", T, vals=["Read", "Edit", "All"], contexto=VAL_ATM),
 field(O, "AccountId", "reference", "CFGS", None, "Conta da equipe.", T, ref=["obj:Account"], req=("sim", None)),
 field(O, "CaseAccessLevel", "picklist", "CFGNSU", "37.0", "Nível de acesso aos casos da conta.", T, vals=["None", "Read", "Edit"], contexto=VAL_ATM),
 field(O, "ContactAccessLevel", "picklist", "CFGNSU", "37.0", "Nível de acesso aos contatos da conta.", T, vals=["None", "Read", "Edit", "Controlled By Parent"], contexto=VAL_ATM),
 field(O, "CurrencyIsoCode", "picklist", "FR", None, "Moeda do registro (códigos permitidos na org).", T),
 field(O, "IsDeleted", "boolean", "DF", None, "Indica se o registro foi excluído.", T),
 field(O, "OpportunityAccessLevel", "picklist", "CFGNSU", "37.0", "Nível de acesso às oportunidades da conta.", T, vals=["None", "Read", "Edit"], contexto=VAL_ATM),
 field(O, "PhotoURL", "url", "FGNS", "37.0", "Foto do usuário (somente leitura).", T),
 field(O, "TeamMemberRole", "picklist", "CFNU", None, "Papel do membro na equipe (valores definidos pela org).", T),
 field(O, "Title", "string", "FGNS", "37.0", "Cargo do usuário (somente leitura).", T),
 field(O, "UserId", "reference", "CF", None, "Usuário membro da equipe.", T, ref=["obj:User"], req=("sim", None))]
obj("AccountTeamMember", "Representa um usuário na equipe de uma conta.", "Liga usuários a contas, com papel e níveis de acesso.",
    [expo("padrao", "verificado", T, ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "update()", "upsert()"],
          acesso="Disponível só em Enterprise, Unlimited e Performance com equipes de conta habilitadas; usuários de Customer Portal não acessam."), TOOL_D()],
    atm, [{"api": "padrao", "soql": "SELECT AccountId, UserId, TeamMemberRole, AccountAccessLevel FROM AccountTeamMember LIMIT 20", "contexto": "API padrão.", "validacao": "documental"}],
    APEX_OK(T), cob("completa", 11, 11, cnt(atm), "Tabela de campos lida completa (11)."), T, juncao=True,
    alertas=["Registros excluídos diretamente não vão para a lixeira (exceto em exclusão em cascata com a conta)."])

# OpportunityTeamMember
P = "src:objref-opportunityteammember"; O = "obj:OpportunityTeamMember"
otm = [
 field(O, "IsDeleted", "boolean", "DF", None, "Indica se o registro foi excluído.", P),
 field(O, "Name", "string", "FNS", None, "Nome do membro.", P),
 field(O, "OpportunityAccessLevel", "picklist", "FNR", None, "Nível de acesso do membro à oportunidade.", P, vals=["Read", "Edit", "All"], contexto=VAL_ATM),
 field(O, "OpportunityId", "reference", "CF", None, "Oportunidade da equipe.", P, ref=["obj:Opportunity"], req=("sim", None)),
 field(O, "PhotoURL", "url", "FGNS", None, "Foto do usuário.", P),
 field(O, "TeamMemberRole", "picklist", "CFNU", None, "Papel do membro (picklist Opportunity Team Roles da org).", P),
 field(O, "Title", "string", "FGNS", None, "Cargo do usuário.", P),
 field(O, "UserId", "reference", "CF", None, "Usuário membro da equipe.", P, ref=["obj:User"], req=("sim", None))]
for f in otm:
    f["notas"] = (f.get("notas") or []) + ["A página lista as propriedades por nome; as letras foram mapeadas na extração."]
obj("OpportunityTeamMember", "Representa um usuário na equipe de uma oportunidade.", "Liga usuários a oportunidades (team selling).",
    [expo("padrao", "verificado", P, ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "update()", "upsert()"],
          acesso="Disponível só em orgs com team selling habilitado."), TOOL_D()],
    otm, [{"api": "padrao", "soql": "SELECT OpportunityId, UserId, TeamMemberRole FROM OpportunityTeamMember LIMIT 20", "contexto": "API padrão.", "validacao": "documental"}],
    APEX_OK(P), cob("completa", 8, 8, cnt(otm), "Tabela de campos lida completa (8)."), P, juncao=True,
    alertas=["Criar um registro com OpportunityId e UserId já existentes atualiza o registro existente.",
             "Para detectar exclusões, usar getDeleted() em vez de IsDeleted em SOQL."])

# LeadStatus
S = "src:objref-leadstatus"; O = "obj:LeadStatus"
ls = [
 field(O, "ApiName", "string", "FGIS", None, "Identificador único do valor de status, independente de Id e rótulo.", S),
 field(O, "IsConverted", "boolean", "DFGS", None, "Indica se o valor representa lead convertido (vários valores podem representar).", S),
 field(O, "IsDefault", "boolean", "DFGS", None, "Indica se é o valor padrão do picklist.", S),
 field(O, "MasterLabel", "string", "FGNS", None, "Rótulo interno, não traduzido, do valor.", S),
 field(O, "SortOrder", "int", "FGNS", None, "Ordem do valor no picklist (pode pular números após exclusões).", S)]
obj("LeadStatus", "Representa um valor do picklist Status de Lead.", "Consultar os valores de status e saber quais indicam conversão.",
    [expo("padrao", "verificado", S, ["describeSObjects()", "query()", "retrieve()"]), TOOL_D()],
    ls, [{"api": "padrao", "soql": "SELECT MasterLabel, IsConverted, IsDefault, SortOrder FROM LeadStatus ORDER BY SortOrder", "contexto": "API padrão; somente leitura.", "validacao": "documental"}],
    APEX_OK(S), cob("completa", 5, 5, cnt(ls), "Tabela de campos lida completa (5)."), S,
    alertas=["Somente leitura pela API de dados (sem create/update)."])

# CaseMilestone
K = "src:objref-casemilestone"; O = "obj:CaseMilestone"
cm_rows = [("BusinessHoursId", "reference", "FGNS", "Business hours do milestone."), ("CaseId", "reference", "F", "Caso ao qual o milestone pertence."),
 ("CompletionDate", "dateTime", "FNU", "Quando o milestone foi concluído."), ("ElapsedTimeInDays", "double", "FN", "Dias até a conclusão."),
 ("ElapsedTimeInHrs", "double", "FN", "Horas até a conclusão."), ("ElapsedTimeInMins", "int", "FN", "Minutos até a conclusão."),
 ("IsCompleted", "boolean", "DF", "Indica se o milestone foi concluído."), ("IsViolated", "boolean", "DF", "Indica se o milestone foi violado."),
 ("MilestoneTypeId", "reference", "FN", "Tipo de milestone aplicado ao caso."), ("StartDate", "dateTime", "FNU", "Quando o milestone começou no caso."),
 ("TargetDate", "dateTime", "F", "Prazo para concluir o milestone."), ("TargetResponseInDays", "double", "FNS", "Prazo-alvo em dias."),
 ("TargetResponseInHrs", "double", "FNS", "Prazo-alvo em horas."), ("TargetResponseInMins", "int", "FGNS", "Prazo-alvo em minutos."),
 ("TimeRemainingInDays", "double", "GNS", "Dias restantes até o prazo."), ("TimeRemainingInHrs", "text", "N", "Horas restantes até o prazo."),
 ("TimeRemainingInMins", "text", "GNS", "Tempo restante, em minutos e segundos."), ("TimeSinceTargetInDays", "double", "NS", "Dias desde o prazo."),
 ("TimeSinceTargetInHrs", "string", "GNS", "Horas desde o prazo."), ("TimeSinceTargetInMins", "string", "GNS", "Tempo desde o prazo, em minutos e segundos.")]
REFS_CM = {"CaseId": ["obj:Case"], "BusinessHoursId": ["obj:BusinessHours"]}
cm = []
for n, t, p, d in cm_rows:
    f = field(O, n, t, p, None, d, K, **({"ref": REFS_CM[n]} if n in REFS_CM else {}))
    if n in REFS_CM: f["notas"] = ["A página não declara 'Refers to'; o alvo vem da descrição do campo."]
    cm.append(f)
obj("CaseMilestone", "Representa um milestone (etapa com prazo) aplicado a um caso.", "Acompanhar se cada etapa do nível de serviço foi cumprida e quando vence.",
    [expo("padrao", "verificado", K, ["describeLayout()", "describeSObjects()", "query()", "retrieve()", "update()"], desde="18.0"), TOOL_D()],
    cm, [{"api": "padrao", "soql": "SELECT CaseId, MilestoneTypeId, TargetDate, IsCompleted, IsViolated FROM CaseMilestone WHERE IsCompleted = false LIMIT 20", "contexto": "API padrão.", "validacao": "documental"}],
    APEX_OK(K), cob("completa", 20, 20, cnt(cm), "Tabela de campos lida completa (20)."), K,
    alertas=["Não aceita create() nem delete(): milestones nascem do processo de entitlement."])

# BusinessHours
W = "src:objref-businesshours"; O = "obj:BusinessHours"
dias = ["Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"]
DIAS_PT = {"Friday": "sexta", "Monday": "segunda", "Saturday": "sábado", "Sunday": "domingo", "Thursday": "quinta", "Tuesday": "terça", "Wednesday": "quarta"}
bh = [field(O, "BusinessHoursId", "reference", "FGNS", None, None, W, notas=["A descrição na página se refere ao SlaProcess; revalidar se o campo pertence de fato a BusinessHours."]),
      field(O, "IsActive", "boolean", "CDFGSU", None, "Indica se o horário está ativo.", W),
      field(O, "Name", "string", "CFGISU", None, "Nome do horário comercial.", W),
      field(O, "IsDefault", "boolean", "CDFGSU", None, "Indica se é o horário padrão.", W),
      field(O, "LastViewedDate", "dateTime", "FNS", None, "Última visualização.", W)]
for d in ["Friday", "Monday", "Saturday", "Sunday", "Thursday"]:
    bh += [field(O, f"{d}EndTime", "time", "CFNSU", None, f"Fim do expediente de {DIAS_PT[d]}.", W), field(O, f"{d}StartTime", "time", "CFNSU", None, f"Início do expediente de {DIAS_PT[d]}.", W)]
bh.append(field(O, "TimeZoneSidKey", "picklist", "CFGRSU", None, "Fuso horário do horário comercial.", W))
for d in ["Tuesday", "Wednesday"]:
    bh += [field(O, f"{d}EndTime", "time", "CFNSU", None, f"Fim do expediente de {DIAS_PT[d]}.", W), field(O, f"{d}StartTime", "time", "CFNSU", None, f"Início do expediente de {DIAS_PT[d]}.", W)]
obj("BusinessHours", "Representa um horário comercial: dias, horários e fuso em que o atendimento funciona.", "Base de cálculo para regras de escalonamento e prazos de milestones.",
    [expo("padrao", "verificado", W, ["create()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "search()", "update()", "upsert()"],
          acesso="Todos os usuários veem business hours pela API, mesmo sem View Setup and Configuration."), TOOL_D()],
    bh, [{"api": "padrao", "soql": "SELECT Name, IsActive, IsDefault, TimeZoneSidKey FROM BusinessHours WHERE IsActive = true", "contexto": "API padrão.", "validacao": "documental"}],
    APEX_OK(W), cob("completa", 20, 20, cnt(bh), "Tabela de campos lida completa (20)."), W,
    alertas=["Regras de escalonamento só rodam dentro do horário associado.", "Feriados (Holiday) suspendem o horário e as regras de escalonamento.",
             "Padrão: 24 horas, no fuso padrão da org."])

# alvos em objetos do lote 3a, agora catalogados
for o, m in {"Lead": {"ConvertedAccountId": ["obj:Account"], "ConvertedContactId": ["obj:Contact"]},
             "Opportunity": {"AccountId": ["obj:Account"]}, "Case": {"AccountId": ["obj:Account"], "ContactId": ["obj:Contact"]}}.items():
    d = ld(f"objetos-api/{o}.json")
    for c in d["campos"]:
        if c["nome"] in m: c["referencia"]["alvos"] = m[c["nome"]]
    sv(f"objetos-api/{o}.json", d)

# ================================================================ relacionamentos
N1 = lambda: af("desconhecido", "N:1", "Estrutura de lookup indica N:1; não comprovado nesta sessão.")
for rid, oo, campo, dd, expl, s, cond in [
 ("account-parent-account", "Account", "ParentId", "Account", "Uma conta pode ter uma conta-mãe (hierarquia).", A, None),
 ("account-owner-user", "Account", "OwnerId", "User", "Toda conta tem um dono, que é um usuário.", A, None),
 ("contact-account", "Contact", "AccountId", "Account", "O contato costuma pertencer a uma conta.", C, "Campo anulável: contato pode existir sem conta."),
 ("atm-account", "AccountTeamMember", "AccountId", "Account", "Cada membro de equipe pertence a uma conta.", T, None),
 ("atm-user", "AccountTeamMember", "UserId", "User", "O membro da equipe é um usuário.", T, None),
 ("otm-opportunity", "OpportunityTeamMember", "OpportunityId", "Opportunity", "Cada membro de equipe pertence a uma oportunidade.", P, None),
 ("otm-user", "OpportunityTeamMember", "UserId", "User", "O membro da equipe é um usuário.", P, None),
 ("casemilestone-case", "CaseMilestone", "CaseId", "Case", "Cada milestone é aplicado a um caso.", K, None),
 ("casemilestone-businesshours", "CaseMilestone", "BusinessHoursId", "BusinessHours", "O milestone pode usar um horário comercial próprio.", K, None),
 ("lead-converted-account", "Lead", "ConvertedAccountId", "Account", "Depois da conversão, o lead guarda a conta gerada ou usada.", "src:objref-lead", "Só em leads convertidos."),
 ("lead-converted-contact", "Lead", "ConvertedContactId", "Contact", "Depois da conversão, o lead guarda o contato gerado ou usado.", "src:objref-lead", "Só em leads convertidos."),
 ("opportunity-account", "Opportunity", "AccountId", "Account", "A oportunidade pertence a uma conta.", "src:objref-opportunity", None),
 ("case-account", "Case", "AccountId", "Account", "O caso pode estar associado a uma conta.", "src:objref-case", None),
 ("case-contact", "Case", "ContactId", "Contact", "O caso pode estar associado a um contato.", "src:objref-case", None)]:
    rel(rid, "referencia_campo", {"entidade": "obj:" + oo, "campo": campo}, {"entidade": "obj:" + dd}, expl, "verificado", [s], N1(), cond=cond)

# ================================================================ funcionalidades
NEG, AUT, CON, ORG, UIX, ACS = ("processos-de-negocio-especificos-de-produto", "automacao-de-processos-e-regras-de-negocio", "conteudo-conhecimento-e-colaboracao",
                                "organizacao-e-configuracoes-base", "interface-e-experiencia-do-usuario", "acesso-identidade-e-seguranca")
SETUP_NL = af("desconhecido", None, "Caminho de configuração não levantado nesta rodada.")
def sem(tipo, motivo): return {"tipo": tipo, "estado": "desconhecido", "motivo": motivo}
MDT_NI = lambda cand: sem("metadata_type", f"Não investigado. Candidato(s) no inventário v68, ainda não lidos: {cand}." if cand else "Não investigado.")
OBJ_NI = lambda cand: sem("objeto_api", f"Objetos citados no relatório de pesquisa de 2026-11-08 e ainda não relidos: {cand}.")
novas_funcs = []
def F(fid, *a, **k):
    func(fid, *a, **k); novas_funcs.append("func:" + fid)

F("contas", "Contas", "Accounts (Account)", ["conta", "account", "cliente"], "Conta é uma organização ou pessoa com quem a empresa se relaciona: cliente, parceiro ou concorrente.",
  "Centralizar os dados de cada cliente e ligar a ele contatos, oportunidades e casos.", "A empresa ACME é uma conta; seus funcionários são contatos e seus negócios, oportunidades.",
  (NEG, "vendas"), [], [], [("Account", "Registro de cada conta.")], [MDT_NI("AccountSettings")], SETUP_NL,
  limit=["Contas pessoais (Person Accounts) não detalhadas: a tabela de campos foi servida truncada."], srcs=["src:objref-account", "src:help-sales-features", "src:help-lex-comparison"])
F("contatos", "Contatos", "Contacts (Contact)", ["contato", "contact", "pessoa"], "Contato é uma pessoa, normalmente ligada a uma conta.",
  "Registrar as pessoas com quem a empresa fala em cada cliente.", "A gerente de compras da ACME é um contato da conta ACME.",
  (NEG, "vendas"), [], [], [("Contact", "Registro de cada contato.")], [MDT_NI(None)], SETUP_NL, srcs=["src:objref-contact", "src:help-lex-comparison"])
F("campanhas", "Campanhas", "Campaigns", ["campanha", "campaign", "marketing"], "Campanha é uma ação de marketing (evento, e-mail, webinar) e seus participantes.",
  "Medir de onde vêm leads e oportunidades.", "Um webinar de lançamento registra os inscritos como membros da campanha.",
  (NEG, "vendas"), [], [], [], [OBJ_NI("Campaign, CampaignMember"), MDT_NI("CampaignSettings")], SETUP_NL, srcs=["src:help-lex-comparison"],
  limit=["Objetos e configuração não lidos diretamente; ver o relatório de pesquisa."])
F("produtos-e-catalogos-de-preco", "Produtos e catálogos de preço", "Products and Price Books", ["produto", "price book", "catálogo de preços", "itens de oportunidade"],
  "Produtos são o que a empresa vende; catálogos de preço definem quanto custa cada produto.", "Compor o valor de uma oportunidade a partir dos produtos negociados.",
  "Uma oportunidade de 10 licenças usa o preço da licença no catálogo padrão.", (NEG, "vendas"), [], [],
  [], [OBJ_NI("Product2, Pricebook2, PricebookEntry, OpportunityLineItem"), MDT_NI(None)], SETUP_NL, srcs=["src:help-lex-comparison", "src:fieldref-opportunity"],
  limit=["Opportunity já registra Pricebook2Id e HasOpportunityLineItem; os demais objetos não foram lidos diretamente."])
F("cotacoes", "Cotações", "Quotes", ["cotação", "quote", "proposta"], "Cotação mostra ao cliente os preços propostos para produtos e serviços.",
  "Enviar propostas e sincronizar uma delas com a oportunidade.", "Três versões de proposta para o mesmo negócio; a escolhida é sincronizada com a oportunidade.",
  (NEG, "vendas"), [], [], [], [OBJ_NI("Quote, QuoteLineItem"), MDT_NI("QuoteSettings")],
  af("verificado", "Setup > Quick Find: Quote > Quote Settings", "Opcional: Create Quotes Without a Related Opportunity.", [ev("src:help-quotes-setup")]),
  alertas=["Não é possível desabilitar cotações se houver referências em customizações ou cotações sincronizadas."],
  pre=["Habilitar: Customize Application.", "Edições: Performance e Developer; em vendas, também Professional, Enterprise e Unlimited.",
       "Cotações sem oportunidade: licença Sales Cloud e acesso a cotações."], srcs=["src:help-quotes-setup", "src:help-quotes-noopp"])
F("previsoes-colaborativas", "Previsões colaborativas", "Collaborative Forecasts", ["forecast", "previsão de vendas", "forecasting"],
  "Previsão de quanto a equipe vai vender no período, com ajustes de gestores.", "Acompanhar metas e o fechamento esperado por período.",
  "A gerente revisa a previsão do trimestre e ajusta o valor de um vendedor.", (NEG, "vendas"), [], [], [],
  [OBJ_NI("ForecastingItem, ForecastingAdjustment, ForecastingOwnerAdjustment, ForecastingType, ForecastingFact, ForecastingQuota"), MDT_NI("ForecastingSettings")], SETUP_NL,
  limit=["Usuários com licença Salesforce Platform não têm direito a previsões (Ajuda)."], srcs=["src:help-sales-features", "src:help-sales-basics", "src:help-user-licenses"])
F("territorios-de-vendas", "Territórios de vendas", "Sales Territories (Territory2Model)", ["território", "sales territories", "enterprise territory management", "etm"],
  "Organiza contas e vendedores em territórios dentro de um modelo, com regras de atribuição.", "Distribuir a carteira e o acesso a registros por território.",
  "Território Sul com subterritórios por estado; contas atribuídas por regra de endereço.", (NEG, "vendas"), [], [("Territory2Model", "Definição implantável do modelo de territórios.")],
  [], [OBJ_NI("Territory2, Territory2Type, UserTerritory2Association, ObjectTerritory2Association")],
  af("verificado", "Setup > Quick Find: Territories > Territory Settings > Enable Sales Territories", "Customize Application.", [ev("src:help-tm2-enable")]),
  alertas=["Enterprise Territory Management agora se chama Sales Territories (Ajuda).", "Só um modelo pode estar ativo por vez; depois de ativo, não volta para Planning."],
  pre=["Edições: Performance e Developer; Enterprise e Unlimited com Sales.", "Ativar modelo: View Setup and Configuration e Manage Territories."],
  srcs=["src:mdapi-territory2model", "src:help-tm2-enable", "src:help-tm2-activate", "src:help-kb-sales-territories"])
F("equipes-de-conta-e-oportunidade", "Equipes de conta e de oportunidade", "Account Teams and Opportunity Teams", ["equipe de conta", "account team", "opportunity team", "team selling"],
  "Grupo de usuários que trabalha junto numa conta ou oportunidade, cada um com um papel.", "Dar acesso e responsabilidade compartilhada sem mudar o dono do registro.",
  "Na conta ACME, o executivo de contas é dono e o engenheiro de pré-venda entra na equipe com acesso de leitura.",
  (NEG, "vendas"), [(ACS, "acesso-a-registros-e-hierarquias", "AccountTeamMember define níveis de acesso a conta, oportunidades, casos e contatos.")], [],
  [("AccountTeamMember", "Membro da equipe de conta (junção conta–usuário)."), ("OpportunityTeamMember", "Membro da equipe de oportunidade (junção oportunidade–usuário).")],
  [MDT_NI("AccountSettings, OpportunitySettings")], SETUP_NL,
  pre=["Equipes de conta: Enterprise, Unlimited e Performance, com o recurso habilitado.", "Equipes de oportunidade: team selling habilitado."],
  srcs=["src:objref-accountteammember", "src:objref-opportunityteammember", "src:help-sales-basics"])
F("omni-channel", "Omni-Channel", "Omni-Channel", ["omni", "roteamento", "presença", "routing"],
  "Roteia trabalho (casos, mensagens, chamadas) para o atendente mais adequado e disponível.", "Distribuir a fila de atendimento por capacidade e status de presença.",
  "Um caso novo vai automaticamente para um atendente disponível no canal de casos.", (NEG, "atendimento"), [], [("ServicePresenceStatus", "Status de presença implantável.")],
  [], [OBJ_NI("AgentWork, ServiceChannel, ServicePresenceStatus, QueueRoutingConfig, PresenceUserConfig"), MDT_NI("ServiceChannel, QueueRoutingConfig, PresenceUserConfig, OmniChannelSettings")],
  af("verificado", "Setup > Quick Find: Omni-Channel Settings > Omni-Channel Settings", "Customize Application.", [ev("src:help-omni-enable")]),
  alertas=["Standard Omni-Channel foi aposentado no Summer '26; a Salesforce faz o upgrade automático para Enhanced Omni-Channel.",
           "Orgs criadas depois do Summer '23 já têm Enhanced por padrão; Enhanced não suporta canais standard (Chat e Messaging standard)."],
  pre=["Licença: Agentforce Service ou add-ons Digital Engagement, Enhanced Chat, Salesforce Voice ou Workforce Management."],
  srcs=["src:mdapi-servicepresencestatus", "src:help-omni-enable", "src:help-omni-upgrade"])
F("lightning-knowledge", "Lightning Knowledge", "Lightning Knowledge", ["knowledge", "base de conhecimento", "artigos"],
  "Base de artigos de conhecimento para atendentes e clientes.", "Padronizar respostas e permitir autoatendimento.",
  "Um artigo de 'Como trocar a senha' é sugerido ao atendente e publicado no portal.", (CON, "knowledge-e-categorias"),
  [(NEG, "atendimento", "A Ajuda de atendimento inclui Knowledge entre os recursos de Agentforce Service.")], [], [],
  [OBJ_NI("Knowledge__kav, KnowledgeArticleVersion, KnowledgeArticle"), MDT_NI("KnowledgeSettings")],
  af("verificado", "Setup > Quick Find: Knowledge > Knowledge Settings > Edit > Enable Lightning Knowledge", None, [ev("src:help-lk-enable")]),
  alertas=["Habilitar Lightning Knowledge é irreversível e muda o modelo de dados para record types; exige ao menos um article type."],
  pre=["Ver Knowledge Settings: licença Knowledge User."], srcs=["src:help-lk-enable", "src:help-service-basics"])
F("entitlements-e-milestones", "Entitlements e milestones (SLA Management)", "Entitlement Management (EntitlementProcess)", ["entitlement", "sla", "sla management", "milestone", "nível de serviço"],
  "Define a que suporte cada cliente tem direito e os prazos (milestones) que o atendimento precisa cumprir.", "Garantir e medir níveis de serviço em casos.",
  "Clientes Ouro têm primeira resposta em 1 hora; o caso mostra o milestone e o tempo restante.", (NEG, "atendimento"), [],
  [("EntitlementProcess", "Processo de entitlement implantável (SLA Policy).")], [("CaseMilestone", "Milestone aplicado a um caso.")],
  [OBJ_NI("Entitlement, SlaProcess, ServiceContract, MilestoneType"), MDT_NI("EntitlementSettings, EntitlementTemplate, MilestoneType")],
  af("verificado", "Setup > Quick Find: Entitlement Settings > Entitlement Settings", "Para processos: Quick Find Entitlement Processes.", [ev("src:help-ent-sla"), ev("src:help-ent-process-create")]),
  alertas=["Na configuração simplificada, Entitlement Management se chama SLA Management, e Entitlement Processes se chamam SLA Policies; não há versionamento.",
           "Business hours: as do milestone prevalecem sobre as do processo, que prevalecem sobre as do caso."],
  pre=["Criar e atualizar processos: Manage Entitlements.", "Configuração simplificada: Professional, Enterprise, Performance, Unlimited e Developer com Service Cloud."],
  srcs=["src:mdapi-entitlementprocess", "src:objref-casemilestone", "src:help-ent-sla", "src:help-rn-sla-ga", "src:help-ent-process-create", "src:help-ent-bh"])
F("regras-de-atribuicao", "Regras de atribuição e escalonamento", "Assignment Rules and Escalation Rules", ["assignment rules", "escalation rules", "atribuição", "escalonamento"],
  "Regras que definem automaticamente o dono de leads e casos, e quando casos são escalonados.", "Distribuir leads e casos sem trabalho manual.",
  "Casos com prioridade alta vão para a fila de nível 1; leads do site vão para a equipe de inbound.", (AUT, "acoes-e-regras"),
  [(NEG, "atendimento", "Regras de atribuição e escalonamento de casos fazem parte da gestão de casos."), (NEG, "vendas", "Regras de atribuição de leads.")], [], [],
  [OBJ_NI("AssignmentRule"), MDT_NI("AssignmentRules, EscalationRules")],
  af("verificado", "Setup > Quick Find: Assignment Rules > Lead Assignment Rules | Case Assignment Rules", "Caminho de Escalation Rules não verificado.", [ev("src:help-assign-guide"), ev("src:help-assign-setup")]),
  alertas=["Só uma regra de atribuição de cada tipo fica ativa por vez.", "Uma regra de atribuição de casos aceita até 3.000 entradas, incluindo 300 de fórmula."],
  srcs=["src:help-assign-guide", "src:help-assign-setup", "src:help-kb-case-management"])
F("horario-comercial", "Horário comercial", "Business Hours", ["business hours", "expediente", "horário de atendimento"],
  "Define os dias, horários e fuso em que o atendimento funciona.", "Calcular prazos e escalonamentos só dentro do expediente.",
  "Suporte de São Paulo: segunda a sexta, 8h às 18h, fuso de Brasília.", (ORG, "horarios-comerciais-e-feriados"),
  [(NEG, "atendimento", "Usado por casos, regras de escalonamento, milestones e processos de entitlement.")], [], [("BusinessHours", "Registro de cada horário comercial.")],
  [MDT_NI("BusinessHoursSettings")],
  af("verificado", "Setup > Quick Find: Business Hours > Business Hours > New Business Hours", None, [ev("src:help-bh")]),
  pre=["Manage Business Hours Holidays."], srcs=["src:objref-businesshours", "src:help-bh"])
F("apps-de-console", "Apps de console Lightning", "Lightning Console Apps", ["console", "service console", "sales console", "console navigation"],
  "Apps com navegação em abas e subabas para trabalhar vários registros ao mesmo tempo.", "Aumentar a produtividade de quem atende ou vende em volume.",
  "No Service Console, o caso abre numa aba e o contato e a conta relacionados abrem em subabas.", (UIX, "aplicativos-e-navegacao"),
  [(NEG, "atendimento", "O Lightning Service Console é o app padrão de atendimento.")], [], [], [MDT_NI("CustomApplication")],
  af("verificado", "Setup > Quick Find: App > App Manager > New Lightning App > Console navigation", None, [ev("src:help-console-create")]),
  alertas=["Usar exige a permissão Lightning Console User e o perfil atribuído ao app.", "O Service Console é atribuído automaticamente a todos os perfis; ajuste as atribuições."],
  pre=["Gerenciar apps: Customize Application.", "Edições: Essentials, Professional, Enterprise, Performance, Unlimited e Developer; o Service Console exige Service Cloud."],
  srcs=["src:help-console-create", "src:help-console-intro", "src:help-service-console-customize"])

# leads: LeadStatus agora catalogado
fl = ld("funcionalidades/leads.json")
fl["representacoes"]["objetos_api"].append({"ref": "obj:LeadStatus", "papel": "Valores do picklist Status e quais indicam conversão."})
fl["limitacoes"] = ["Regras de atribuição em func:regras-de-atribuicao; configurações de conversão (LeadConvertSettings) não lidas."]
fl["evidencias"].append(ev("src:objref-leadstatus"))
sv("funcionalidades/leads.json", fl)

# subclassificações
for fid in novas_funcs:
    f = ld(f"funcionalidades/{fid[5:]}.json")
    subs = [f["classificacao_principal"]["subclassificacao"]] + [s["subclassificacao"] for s in f["classificacoes_secundarias"]]
    for s in subs:
        d = ld(f"subclassificacoes/{s[4:]}.json"); d["funcionalidades"] = sorted(set(d["funcionalidades"]) | {fid}); sv(f"subclassificacoes/{s[4:]}.json", d)

# ================================================================ nuvens
def ca(pares):
    tree = {}
    for c, s, fs in pares: tree.setdefault("cls:" + c, []).append({"subclassificacao": "sub:" + s, "funcionalidades": sorted(fs)})
    return [{"classificacao": c, "subclassificacoes": v} for c, v in tree.items()]
sales = ld("nuvens/sales-cloud.json")
sales["classificacoes_aplicaveis"] = ca([
 (NEG, "vendas", ["func:leads", "func:oportunidades", "func:contas", "func:contatos", "func:campanhas", "func:produtos-e-catalogos-de-preco", "func:cotacoes",
                  "func:previsoes-colaborativas", "func:territorios-de-vendas", "func:equipes-de-conta-e-oportunidade"]),
 (AUT, "acoes-e-regras", ["func:regras-de-atribuicao"]),
 (UIX, "orientacao-visual-e-path", ["func:path"]), (UIX, "aplicativos-e-navegacao", ["func:apps-de-console"])])
sales["limites"] = ["Campanhas, produtos, cotações e previsões: objetos e metadata types ainda não lidos diretamente (ver o relatório de pesquisa de 2026-11-08).",
                    "func:path, func:regras-de-atribuicao e func:apps-de-console são capacidades compartilhadas: aparecem na Ajuda de vendas, mas não são exclusivas.",
                    "Ajuda: a edição Unlimited é oferecida para as áreas de vendas, atendimento e indústrias; matriz completa de edições não registrada."]
sales["evidencias"] += [ev("src:help-quotes-setup"), ev("src:help-tm2-enable"), ev("src:help-assign-guide")]
sv("nuvens/sales-cloud.json", sales)
serv = ld("nuvens/service-cloud.json")
serv["classificacoes_aplicaveis"] = ca([
 (NEG, "atendimento", ["func:casos", "func:omni-channel", "func:entitlements-e-milestones"]),
 (CON, "knowledge-e-categorias", ["func:lightning-knowledge"]),
 (AUT, "acoes-e-regras", ["func:regras-de-atribuicao"]),
 (ORG, "horarios-comerciais-e-feriados", ["func:horario-comercial"]),
 (UIX, "aplicativos-e-navegacao", ["func:apps-de-console"])])
serv["licencas"]["itens"].append({"nome": "Knowledge User (feature license)", "tipo": "licenca_recurso", "evidencias": [ev("src:help-lk-enable")]})
serv["licencas"]["nota"] += " Omni-Channel vem com a licença de produto Agentforce Service ou com add-ons (Digital Engagement, Enhanced Chat, Salesforce Voice, Workforce Management)."
serv["limites"] = ["Objetos de Omni-Channel, Knowledge e Entitlement (exceto CaseMilestone) ainda não lidos diretamente (ver o relatório de pesquisa de 2026-11-08).",
                   "Regras de atribuição, horário comercial e apps de console são capacidades compartilhadas, não exclusivas de atendimento.",
                   "O Service Console inclui casos, contatos e contas por padrão (Ajuda); contas e contatos estão classificados em vendas."]
serv["evidencias"] += [ev("src:help-omni-enable"), ev("src:help-lk-enable"), ev("src:help-ent-sla"), ev("src:help-bh"), ev("src:help-service-console-customize")]
sv("nuvens/service-cloud.json", serv)
print("ok", len(novas_funcs))
