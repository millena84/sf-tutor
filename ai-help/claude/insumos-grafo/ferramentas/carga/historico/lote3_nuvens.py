# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 3a: nuvens Sales/Service (Agentforce Sales/Service) e funcionalidades próprias Leads, Oportunidades e Casos.
# Aplica sobre os JSONs do catálogo por load/modify/save (não reexecutar run.py).
import json, os
import b1_base
from b1_base import ev, af
from b3_obj import field, expo, obj, rel, cob, cnt, func, APEX_OK, SUB_FUNCS

BASE = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/"
CAT = BASE + "catalogo/"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")

# ---------------------------------------------------------------- fontes
reg = json.load(open(BASE + "fontes/registro.json"))
B = "https://developer.salesforce.com/docs/atlas.en-us.264.0."
FR = "https://developer.salesforce.com/docs/atlas.en-us.sfFieldRef.meta/sfFieldRef/"
H = "https://help.salesforce.com/s/articleView?id="
def src(id, t, u, pert, extr, ver="68.0", metodo="extracao_documental_assistida", tipo="oficial_documentacao"):
    return {"id": id, "titulo": t, "url": u, "tipo": tipo, "versao": ver, "data_verificacao": "2026-11-07", "metodo": metodo, "pertinencia": pert,
            "extracao": "fontes/extracoes/" + extr, "checagem_online": {"estado": "verificado", "nota": "Conteúdo lido em 2026-11-07 e conferido quanto ao assunto (não apenas HTTP 200)."}}
novas = [
 src("src:objref-lead", "Lead (Object Reference)", B + "object_reference.meta/object_reference/sforce_api_objects_lead.htm", "Chamadas suportadas, campos e regras de conversão do objeto Lead.", "objref-Lead.txt"),
 src("src:objref-opportunity", "Opportunity (Object Reference)", B + "object_reference.meta/object_reference/sforce_api_objects_opportunity.htm", "Chamadas suportadas e parte dos campos do objeto Opportunity.", "objref-Opportunity.txt"),
 src("src:objref-case", "Case (Object Reference)", B + "object_reference.meta/object_reference/sforce_api_objects_case.htm", "Chamadas suportadas e parte dos campos do objeto Case.", "objref-Case.txt"),
 src("src:fieldref-opportunity", "Opportunity (Salesforce Field Reference Guide)", FR + "salesforce_field_reference_Opportunity.htm", "Nomes e tipos de campos de Opportunity ausentes da Object Reference truncada.", "fieldref-Opportunity.txt"),
 src("src:fieldref-case", "Case (Salesforce Field Reference Guide)", FR + "salesforce_field_reference_Case.htm", "Nomes e tipos de campos de Case ausentes da Object Reference truncada.", "fieldref-Case.txt"),
]
for sid, t, art, pert in [
 ("help-editions", "Salesforce Editions", "xcloud.overview_edition.htm", "Edições como pacotes de recursos; disponibilidade por área de produto."),
 ("help-user-licenses", "Standard User Licenses", "platform.users_license_types_available.htm", "Licença Salesforce (CRM completo) versus Salesforce Platform (sem leads, oportunidades, campanhas e previsões)."),
 ("help-service-feature-license", "Assign the Service Cloud User Feature License", "console2_assign_service_feature_license.htm", "Novo nome Agentforce Service; feature license Service Cloud User; edições."),
 ("help-service-basics", "Service Basics", "support_admins_intro.htm", "Agentforce Service (antes Service Cloud): casos como base, Omni-Channel, central de ajuda/knowledge, horário comercial."),
 ("help-sales-features", "Sales Features", "sf.sales_core_basics.htm", "Agentforce Sales (antes Sales Cloud): leads, oportunidades/pipeline, contas, previsões, territórios."),
 ("help-sales-basics", "Sales Basics", "sf.sales_core.htm", "Previsões, territórios, equipes de venda, Path e Lightning Sales Console."),
 ("help-lex-comparison", "Compare Lightning Experience and Salesforce Classic", "sf.lex_aloha_comparison.htm", "Agrupa objetos de dados de vendas e de atendimento."),
 ("help-kb-case-management", "Case Management (KB)", "000390829&type=1", "Regras de atribuição e escalonamento, Omni-Channel, entitlements e Knowledge ligados a casos.")]:
    novas.append(src("src:" + sid, t, H + art, pert, "help-nuvens.txt", "sem versão (Ajuda Salesforce)", "leitura_resultado_busca", "oficial_ajuda"))
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- objetos
def campos_de(o, nomes, detalhes, src_padrao, nota_sem_props):
    out = []
    for n in nomes:
        if n in detalhes:
            out.append(detalhes[n])
        else:
            f = field(o, n, "(a extrair)", None, None, None, src_padrao)
            f["notas"] = [nota_sem_props]
            out.append(f)
    return out

# Lead
L = "src:objref-lead"
lead_nomes = ("ActionCadenceAssigneeId, ActionCadenceId, ActionCadenceState, ActiveTrackerCount, ActivityMetricId, ActivityMetricRollupId, Address, AnnualRevenue, City, CleanStatus, "
  "Company, CompanyDunsNumber, ConvertedAccountId, ConvertedContactId, ConvertedDate, ConvertedOpportunityId, ConnectionReceivedId, ConnectionSentId, Country, CountryCode, "
  "CurrencyIsoCode, DandBCompanyId, Description, Division, Email, EmailBouncedDate, EmailBouncedReason, ExportStatus, Fax, FirstCallDateTime, FirstEmailDateTime, FirstName, "
  "GeocodeAccuracy, GenderIdentity, HasOptedOutOfEmail, HasOptedOutOfFax, IndividualId, Industry, IsConverted, IsDeleted, IsPriorityRecord, IsUnreadByOwner, Jigsaw, "
  "JigsawContactId, LastActivityDate, LastName, LastReferencedDate, LastViewedDate, Latitude, LeadSource, Longitude, MasterRecordId, MiddleName, MobilePhone, Name, "
  "NumberOfEmployees, OwnerId, PartnerAccountId, Phone, PhotoUrl, PostalCode, Pronouns, Rating, RecordTypeId, Salutation, ScheduledResumeDateTime, ScoreIntelligenceId, "
  "State, StateCode, Status, Street, Suffix, Title, Website").split(", ")
O = "obj:Lead"
ld_det = {
 "Company": field(O, "Company", "string", "CFGNSU", None, "Empresa do lead. Se vazio e contas pessoais estiverem habilitadas, a conversão gera uma conta pessoal.", L),
 "LastName": field(O, "LastName", "string", "CFGSU", None, "Sobrenome do lead (até 80 caracteres).", L, req=("sim", None)),
 "IsConverted": field(O, "IsConverted", "boolean", "CDFGS", None, "Indica se o lead já foi convertido.", L),
 "ConvertedAccountId": field(O, "ConvertedAccountId", "reference", "CFGNS", None, "Conta gerada (ou usada) na conversão.", L, ref=["Account"]),
 "ConvertedContactId": field(O, "ConvertedContactId", "reference", "CFGNS", None, "Contato gerado (ou usado) na conversão.", L, ref=["Contact"]),
 "ConvertedOpportunityId": field(O, "ConvertedOpportunityId", "reference", "CFGNS", None, "Oportunidade gerada na conversão, quando houver.", L, ref=["Opportunity"]),
 "OwnerId": field(O, "OwnerId", "reference", "CDFGSU", None, "Dono do lead: um usuário ou uma fila.", L, ref=["Group", "User"]),
 "LeadSource": field(O, "LeadSource", "picklist", "CFGNSU", None, "Origem do lead (de onde o contato veio).", L),
 "Status": field(O, "Status", "picklist", "CDFGSU", None, "Situação do lead no processo de qualificação.", L,
     dominio={"natureza": "lista_dinamica", "estado": "verificado", "evidencias": [ev(L)], "contexto": "Valores definidos na configuração de status de lead da org e expostos pelo objeto LeadStatus."}),
 "Rating": field(O, "Rating", "picklist", "CFGNSU", None, "Classificação do lead.", L),
 "Title": field(O, "Title", "string", "CFGNSU", None, "Cargo da pessoa. Até 128 caracteres; a conversão em conta pessoal falha acima de 80.", L),
 "Phone": field(O, "Phone", "phone", "CFGNSU", None, "Telefone do lead.", L),
 "Website": field(O, "Website", "url", "CFGNSU", None, "Site do lead.", L),
 "RecordTypeId": field(O, "RecordTypeId", "reference", "CFNU", None, "Tipo de registro do lead.", L),
}
lead_campos = campos_de(O, lead_nomes, ld_det, L, "Nome listado na Object Reference; tipo e propriedades não extraídos nesta rodada.")
obj("Lead", "Representa um potencial cliente (pessoa ou empresa) ainda não qualificado.", "Registro dos prospects e da sua conversão em conta, contato e oportunidade.",
    [expo("padrao", "verificado", L, ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "merge()", "query()", "retrieve()", "search()", "undelete()", "update()", "upsert()"],
          acesso="Atualizar ou converter exige a permissão Edit em leads; leads convertidos só podem ser atualizados com View and Edit Converted Leads."),
     expo("tooling", "desconhecido", nota="Não consta da extração do índice de objetos da Tooling API (índice servido truncado); não verificado.")],
    lead_campos,
    [{"api": "padrao", "soql": "SELECT LastName, Company, Status FROM Lead WHERE IsConverted = false LIMIT 20", "contexto": "API padrão (REST /query ou SOAP query()).", "validacao": "documental"}],
    APEX_OK(L),
    cob("parcial", None, len(lead_campos), cnt(lead_campos), "Página lida integralmente em duas partes (131 mil caracteres): 74 nomes. Sem contagem independente de referência, por isso não se declara completa. Tipos e propriedades extraídos só para 14 campos."),
    L, alertas=["Mudar Status para um valor de convertido pela API não converte o lead; a conversão usa convertLead() ou a interface.",
                "Leads convertidos ficam somente leitura, mas continuam consultáveis."])

# Opportunity
P, PF = "src:objref-opportunity", "src:fieldref-opportunity"
opp_objref = ("AccountId, ActivityMetricId, ActivityMetricRollupId, AgeInDays, Amount, CampaignId, CloseDate, ConnectionReceivedId, ConnectionSentId, ContactId, ContractId, "
  "CurrencyIsoCode, Description, ExpectedRevenue, ExportStatus, Fiscal, FiscalQuarter, FiscalYear, ForecastCategory, ForecastCategoryName, HasOpenActivity, HasOpportunityLineItem, "
  "HasOverdueTask, IqScore, IsClosed, IsDeleted, IsExcludedFromTerritory2Filter, IsPriorityRecord, IsPrivate, IsSplit, IsWon, LastActivityDate, LastActivityInDays, "
  "LastAmountChangedHistoryId, LastCloseDateChangedHistoryId, LastReferencedDate, LastStageChangeDate").split(", ")
opp_fr = ("AccountId, ActivityMetricId, ActivityMetricRollupId, AgeInDays, Amount, CampaignId, CloseDate, ContactId, ContractId, CreatedById, CreatedDate, CurrencyIsoCode, Description, "
  "Fiscal, FiscalQuarter, FiscalYear, ForecastCategory, ForecastCategoryName, HasOpenActivity, HasOpportunityLineItem, HasOverdueTask, Id, IqScore, IsClosed, IsDeleted, "
  "IsPriorityRecord, IsWon, LastActivityDate, LastActivityInDays, LastAmountChangedHistoryId, LastCloseDateChangedHistoryId, LastModifiedById, LastModifiedDate, "
  "LastReferencedDate, LastStageChangeDate, LastStageChangeInDays, LastSyncTime, LastViewedDate, LeadSource, Name, NextStep, OpportunityScoreId, OwnerId, Pricebook2Id, "
  "Probability, PushCount, ReferralCode, StageName, SyncedQuoteId, SystemModstamp, Type").split(", ")
O = "obj:Opportunity"
op_det = {
 "AccountId": field(O, "AccountId", "reference", "CFGNSU", None, "Conta à qual a oportunidade pertence.", P, ref=["Account"]),
 "CloseDate": field(O, "CloseDate", "date", "CFGSU", None, "Data prevista de fechamento do negócio.", P, req=("sim", None)),
 "Amount": field(O, "Amount", "currency", "CFNSU", None, "Valor estimado do negócio; quando há produtos, é calculado a partir deles.", P),
 "IsClosed": field(O, "IsClosed", "boolean", "DFGS", None, "Indica se a oportunidade chegou a uma etapa fechada.", P),
 "IsWon": field(O, "IsWon", "boolean", "DFGS", None, "Indica se a oportunidade foi ganha.", P),
 "ForecastCategoryName": field(O, "ForecastCategoryName", "picklist", "CDFGNRSU", None, "Categoria de previsão; normalmente acompanha a etapa.", P),
 "StageName": field(O, "StageName", "picklist", None, None, "Etapa atual da oportunidade no processo de venda.", PF),
 "Name": field(O, "Name", "string", None, None, "Nome da oportunidade (até 120 caracteres).", PF),
 "OwnerId": field(O, "OwnerId", "reference", None, None, "Dono da oportunidade.", PF),
 "Probability": field(O, "Probability", "percent", None, None, "Probabilidade de fechamento, em percentual.", PF),
 "Type": field(O, "Type", "picklist", None, None, "Tipo da oportunidade.", PF),
}
for n in ("StageName", "Name", "OwnerId", "Probability", "Type"):
    op_det[n]["notas"] = ["Tipo pela Field Reference; propriedades de API, obrigatoriedade e alvo de referência não constam dessa fonte (a Object Reference é servida truncada antes deste campo)."]
nomes = opp_objref + [n for n in opp_fr if n not in opp_objref]
opp_campos = []
for n in nomes:
    if n in op_det: opp_campos.append(op_det[n]); continue
    s = P if n in opp_objref else PF
    f = field(O, n, "(a extrair)", None, None, None, s)
    f["notas"] = ["Nome listado na " + ("Object Reference" if s == P else "Field Reference") + "; tipo e propriedades não extraídos nesta rodada."]
    opp_campos.append(f)
obj("Opportunity", "Representa um negócio em andamento, com valor, etapa e data prevista de fechamento.", "Registro do pipeline de vendas.",
    [expo("padrao", "verificado", P, ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "search()", "undelete()", "update()", "upsert()"]),
     expo("tooling", "desconhecido", nota="Não consta da extração do índice de objetos da Tooling API (índice servido truncado); não verificado.")],
    opp_campos,
    [{"api": "padrao", "soql": "SELECT Name, StageName, CloseDate, Amount FROM Opportunity WHERE IsClosed = false LIMIT 20", "contexto": "API padrão (REST /query ou SOAP query()).", "validacao": "documental"}],
    APEX_OK(P),
    cob("parcial", None, len(opp_campos), cnt(opp_campos), "Object Reference servida truncada (~54 mil caracteres, tabela termina em LastStageChangeDate): 37 nomes. Field Reference acrescenta 21 nomes; ela cobre o objeto e tabelas relacionadas (OpportunityFeed, OpportunityShare) e também é servida truncada. Campos das tabelas relacionadas não foram incluídos. Total esperado não comprovado."),
    P, alertas=["IsClosed e IsWon não aceitam create/update pela API: refletem a etapa."])
ob = ld("objetos-api/Opportunity.json"); ob["evidencias"].append(ev(PF)); sv("objetos-api/Opportunity.json", ob)

# Case
C, CF = "src:objref-case", "src:fieldref-case"
case_objref = ("AccountId, AssetWarrantyID, BusinessHoursId, Comments, CaseNumber, ClosedDate, CommunityId, ConnectionReceivedId, ConnectionSentId, ContactEmail, ContactFax, ContactId, "
  "ContactMobile, ContactPhone, CreatorFullPhotoUrl, CreatorName, CreatorSmallPhotoUrl, Description, FeedItemId, HasCommentsUnreadByOwner, HasSelfServiceComments, IsClosed, "
  "IsClosedOnCreate, IsDeleted, IsEscalated, IsSelfServiceClosed, IsStopped, IsVisibleInSelfService, Language, LastReferencedDate, LastViewedDate, MasterRecordId, Origin, OwnerId, "
  "ParentId, Priority, QuestionId, Reason, RecordTypeId, ServiceContractId, SlaStartDate, SourceId, Status").split(", ")
case_fr = ("AccountId, CaseNumber, ClosedDate, Comments, ContactEmail, ContactFax, ContactId, ContactMobile, ContactPhone, CreatedById, CreatedDate, CurrencyIsoCode, Description, Id, "
  "IsClosed, IsDeleted, IsEscalated, Language, LastModifiedById, LastModifiedDate, LastReferencedDate, LastViewedDate, MasterRecordId, Origin, OwnerId, ParentId, Priority, "
  "Reason, SourceId, Status, Subject, SuppliedCompany, SuppliedEmail, SuppliedName, SuppliedPhone, SystemModstamp, Type").split(", ")
O = "obj:Case"
cs_det = {
 "AccountId": field(O, "AccountId", "reference", "CFGNSU", None, "Conta associada ao caso.", C, ref=["Account"]),
 "ContactId": field(O, "ContactId", "reference", "CFGNSU", None, "Contato associado ao caso.", C, ref=["Contact"]),
 "Status": field(O, "Status", "picklist", "CDFGNSU", None, "Situação do caso; determina o valor de IsClosed.", C),
 "Priority": field(O, "Priority", "picklist", "CDFGNSU", None, "Importância ou urgência do caso.", C),
 "Origin": field(O, "Origin", "picklist", "CFGNSU", None, "Canal de origem do caso (por exemplo, e-mail, telefone ou web).", C),
 "IsClosed": field(O, "IsClosed", "boolean", "DFGS", None, "Indica se o caso está fechado; segue o Status e não é definido diretamente.", C),
 "OwnerId": field(O, "OwnerId", "reference", "CDFGSU", None, "Dono do caso: um usuário ou uma fila.", C, ref=["Group", "User"]),
 "RecordTypeId": field(O, "RecordTypeId", "reference", "CFNU", None, "Tipo de registro do caso.", C),
 "ParentId": field(O, "ParentId", "reference", "CFGNSU", None, "Caso pai, numa hierarquia de casos.", C, ref=["Case"]),
 "Subject": field(O, "Subject", "string", None, None, "Assunto do caso (até 255 caracteres).", CF),
 "Type": field(O, "Type", "picklist", None, None, "Tipo do caso.", CF),
 "SuppliedEmail": field(O, "SuppliedEmail", "email", None, None, "E-mail informado por quem abriu o caso (até 80 caracteres).", CF),
}
for n in ("Subject", "Type", "SuppliedEmail"):
    cs_det[n]["notas"] = ["Tipo pela Field Reference; propriedades de API não constam dessa fonte (a Object Reference é servida truncada antes deste campo)."]
nomes = case_objref + [n for n in case_fr if n not in case_objref]
case_campos = []
for n in nomes:
    if n in cs_det: case_campos.append(cs_det[n]); continue
    s = C if n in case_objref else CF
    f = field(O, n, "(a extrair)", None, None, None, s)
    f["notas"] = ["Nome listado na " + ("Object Reference" if s == C else "Field Reference") + "; tipo e propriedades não extraídos nesta rodada."]
    case_campos.append(f)
obj("Case", "Representa uma questão, problema ou solicitação de cliente a ser tratada.", "Registro central do atendimento.",
    [expo("padrao", "verificado", C, ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "search()", "undelete()", "update()", "upsert()"]),
     expo("tooling", "desconhecido", nota="Não consta da extração do índice de objetos da Tooling API (índice servido truncado); não verificado.")],
    case_campos,
    [{"api": "padrao", "soql": "SELECT CaseNumber, Status, Priority, Origin FROM Case WHERE IsClosed = false LIMIT 20", "contexto": "API padrão (REST /query ou SOAP query()).", "validacao": "documental"}],
    APEX_OK(C),
    cob("parcial", None, len(case_campos), cnt(case_campos), "Object Reference servida truncada (~53 mil caracteres, tabela termina em Status): 43 nomes. Field Reference (lida inteira) acrescenta 12 nomes padrão; os campos customizados que ela mostra (Issue__c, Resolution__c, Summary__c) vêm da org de exemplo e foram excluídos. EntitlementId não aparece em nenhuma das duas leituras. Total esperado não comprovado."),
    C, alertas=["IsClosed segue o Status; não é definido diretamente."])
ob = ld("objetos-api/Case.json"); ob["evidencias"].append(ev(CF)); sv("objetos-api/Case.json", ob)

# ---------------------------------------------------------------- relacionamentos
N1 = lambda s, nota=None: af("desconhecido", "N:1", nota or "Estrutura de lookup indica N:1; não comprovado nesta sessão.")
rel("lead-converted-opportunity", "referencia_campo", {"entidade": "obj:Lead", "campo": "ConvertedOpportunityId"}, {"entidade": "obj:Opportunity"},
    "Depois da conversão, o lead guarda o Id da oportunidade gerada.", "verificado", [L], N1(L), cond="Preenchido só em leads convertidos que geraram oportunidade.")
rel("lead-owner-user", "referencia_campo", {"entidade": "obj:Lead", "campo": "OwnerId"}, {"entidade": "obj:User"},
    "O dono do lead pode ser um usuário; o campo também aceita filas (Group, não catalogado).", "verificado", [L], N1(L), cond="Quando o dono é um usuário.")
rel("case-owner-user", "referencia_campo", {"entidade": "obj:Case", "campo": "OwnerId"}, {"entidade": "obj:User"},
    "O dono do caso pode ser um usuário; o campo também aceita filas (Group, não catalogado).", "verificado", [C], N1(C), cond="Quando o dono é um usuário.")
rel("case-parent-case", "referencia_campo", {"entidade": "obj:Case", "campo": "ParentId"}, {"entidade": "obj:Case"},
    "Um caso pode ter um caso pai (auto-relacionamento), formando hierarquias.", "verificado", [C], N1(C))

# ---------------------------------------------------------------- funcionalidades
NEG = "processos-de-negocio-especificos-de-produto"
SEM_MDT = lambda o: {"tipo": "metadata_type", "estado": "desconhecido",
    "motivo": f"Não investigado: cada {o} é um registro, não um componente implantável; configurações relacionadas podem ter metadata types próprios, ainda não levantados."}
SETUP_NL = af("desconhecido", None, "Caminho de configuração não levantado nesta rodada.")
func("leads", "Leads", "Leads (Lead)", ["lead", "prospect", "conversão de lead"],
     "Lead é um potencial cliente (pessoa ou empresa) que ainda não foi qualificado.",
     "Registrar e qualificar interessados antes de convertê-los em conta, contato e, se fizer sentido, oportunidade.",
     "Uma pessoa preenche o formulário de contato do site; o registro entra como lead, a equipe qualifica e, ao converter, nascem conta, contato e oportunidade.",
     (NEG, "vendas"), [], [], [("Lead", "Registro de cada lead.")], [SEM_MDT("lead")], SETUP_NL,
     alertas=["Mudar o Status pela API não converte o lead; use convertLead() ou a interface.",
              "Usuários com licença Salesforce Platform não têm direito a leads (Ajuda)."],
     limit=["Status de lead (LeadStatus), regras de atribuição e configurações de conversão não catalogados."],
     srcs=["src:objref-lead", "src:help-sales-features", "src:help-user-licenses"])
func("oportunidades", "Oportunidades", "Opportunities (Opportunity)", ["oportunidade", "opportunity", "pipeline", "negócio"],
     "Oportunidade é um negócio em andamento, com valor estimado, etapa e data prevista de fechamento.",
     "Acompanhar o pipeline de vendas até o ganho ou a perda.",
     "Uma proposta de renovação para um cliente, em negociação, com fechamento previsto para o fim do trimestre.",
     (NEG, "vendas"), [], [], [("Opportunity", "Registro de cada oportunidade.")], [SEM_MDT("oportunidade")], SETUP_NL,
     alertas=["IsClosed e IsWon não são gravados diretamente: refletem a etapa.",
              "Usuários com licença Salesforce Platform não têm direito a oportunidades (Ajuda)."],
     limit=["Produtos, cotações, previsões (forecasting) e equipes de venda não catalogados.",
            "Tipos de registro de Opportunity exigem processo de vendas (BusinessProcessId em RecordType); BusinessProcess não catalogado."],
     srcs=["src:objref-opportunity", "src:fieldref-opportunity", "src:help-sales-features", "src:help-user-licenses", "src:objref-recordtype"])
func("casos", "Casos", "Cases (Case)", ["caso", "case", "chamado", "ticket"],
     "Caso é o registro de uma questão, problema ou solicitação de um cliente.",
     "Organizar o atendimento: quem pediu, por qual canal, com que prioridade e em que situação, até o fechamento.",
     "Um cliente escreve relatando atraso na entrega; o caso registra o contato, a origem por e-mail, a prioridade e segue até ser fechado.",
     (NEG, "atendimento"), [], [], [("Case", "Registro de cada caso.")], [SEM_MDT("caso")], SETUP_NL,
     alertas=["IsClosed segue o Status; não é definido diretamente."],
     limit=["Omni-Channel, Knowledge, entitlements, regras de atribuição e escalonamento e horário comercial são citados pela Ajuda junto com casos, mas não foram catalogados."],
     srcs=["src:objref-case", "src:fieldref-case", "src:help-service-basics", "src:help-kb-case-management"])

for sid, fs, nota in [("vendas", ["func:leads", "func:oportunidades"], "Agrupamento didático. Leads e oportunidades são citados pela Ajuda como recursos de Agentforce Sales (src:help-sales-features); a fronteira completa da subclassificação ainda não foi cruzada."),
                      ("atendimento", ["func:casos"], "Agrupamento didático. Casos são a base de Agentforce Service na Ajuda (src:help-service-basics); a fronteira completa da subclassificação ainda não foi cruzada.")]:
    s = ld(f"subclassificacoes/{sid}.json")
    s["funcionalidades"] = sorted(set(s["funcionalidades"]) | set(fs)); s["nota_estado"] = nota
    sv(f"subclassificacoes/{sid}.json", s)

# ---------------------------------------------------------------- nuvens
sales = ld("nuvens/sales-cloud.json")
sales.update({
 "nome_oficial": "Agentforce Sales", "aliases": ["Sales Cloud"],
 "resumo": "Produto de vendas da Salesforce, antes chamado Sales Cloud. Cobre leads, oportunidades e pipeline, contas, previsões e territórios.",
 "o_que_e": "Na Ajuda, a área de vendas reúne objetos padrão de vendas (leads, oportunidades, contas, campanhas, produtos, cotações) e recursos como previsões, territórios, equipes de venda e Path.",
 "contexto_tecnico": af("verificado", "Os objetos de vendas catalogados (Lead, Opportunity) são objetos padrão da API padrão, documentados na Object Reference da plataforma: rodam na mesma org e pelas mesmas APIs do Core.",
     "Isso vale para os objetos verificados; não generalizar para todo recurso de vendas.", [ev("src:objref-lead"), ev("src:objref-opportunity"), ev("src:help-lex-comparison")]),
 "licencas": {"estado": "verificado",
     "nota": "Lista completa não registrada. A licença de usuário Salesforce dá acesso ao CRM padrão; a licença Salesforce Platform não dá direito a leads, oportunidades, campanhas e previsões.",
     "itens": [{"nome": "Salesforce (licença de usuário)", "tipo": "licenca_usuario", "evidencias": [ev("src:help-user-licenses")]}]},
 "classificacoes_aplicaveis": [
     {"classificacao": "cls:" + NEG, "subclassificacoes": [{"subclassificacao": "sub:vendas", "funcionalidades": ["func:leads", "func:oportunidades"]}]},
     {"classificacao": "cls:interface-e-experiencia-do-usuario", "subclassificacoes": [{"subclassificacao": "sub:orientacao-visual-e-path", "funcionalidades": ["func:path"]}]}],
 "limites": ["Inventário parcial: contas, contatos, campanhas, produtos, cotações, previsões, territórios e equipes de venda são citados pela Ajuda, mas não foram catalogados.",
             "func:path entra como capacidade compartilhada da plataforma citada na Ajuda de vendas; não é exclusiva de vendas.",
             "Ajuda: a edição Unlimited é oferecida para as áreas de vendas, atendimento e indústrias; matriz completa de edições não registrada."],
 "cobertura_inventario": "parcial", "estado": "verificado",
 "evidencias": [ev("src:help-sales-features"), ev("src:help-sales-basics"), ev("src:help-user-licenses"), ev("src:help-editions"), ev("src:help-lex-comparison")]})
sv("nuvens/sales-cloud.json", sales)

serv = ld("nuvens/service-cloud.json")
serv.update({
 "nome_oficial": "Agentforce Service", "aliases": ["Service Cloud"],
 "resumo": "Produto de atendimento da Salesforce, antes chamado Service Cloud. Casos são a base; inclui Omni-Channel, central de ajuda e Knowledge, horário comercial e configurações de suporte.",
 "o_que_e": "Na Ajuda, a área de atendimento reúne objetos padrão (casos, ativos, Knowledge, ordens de trabalho), entitlements e Omni-Channel. O Service Console é liberado pela feature license Service Cloud User.",
 "contexto_tecnico": af("verificado", "O objeto Case é objeto padrão da API padrão, documentado na Object Reference da plataforma: roda na mesma org e pelas mesmas APIs do Core.",
     "Isso vale para o objeto verificado; não generalizar para todo recurso de atendimento.", [ev("src:objref-case"), ev("src:help-lex-comparison")]),
 "licencas": {"estado": "verificado",
     "nota": "Lista completa não registrada. A feature license Service Cloud User dá acesso ao Service Console (edições Essentials, Professional, Enterprise, Performance, Unlimited e Developer).",
     "itens": [{"nome": "Service Cloud User (feature license)", "tipo": "licenca_recurso", "evidencias": [ev("src:help-service-feature-license")]}]},
 "classificacoes_aplicaveis": [
     {"classificacao": "cls:" + NEG, "subclassificacoes": [{"subclassificacao": "sub:atendimento", "funcionalidades": ["func:casos"]}]}],
 "limites": ["Inventário parcial: Omni-Channel, Knowledge, entitlements, regras de atribuição e escalonamento, horário comercial e Service Console são citados pela Ajuda, mas não foram catalogados."],
 "cobertura_inventario": "parcial", "estado": "verificado",
 "evidencias": [ev("src:help-service-basics"), ev("src:help-service-feature-license"), ev("src:help-kb-case-management"), ev("src:help-lex-comparison")]})
sv("nuvens/service-cloud.json", serv)

# schema: tipo de licença 'licenca_recurso' (feature license)
sp = BASE + "schemas/nuvem.schema.json"
sch = json.load(open(sp))
en = sch["properties"]["licencas"]["properties"]["itens"]["items"]["properties"]["tipo"]["enum"]
if "licenca_recurso" not in en: en.append("licenca_recurso")
json.dump(sch, open(sp, "w"), ensure_ascii=False, indent=2); open(sp, "a").write("\n")
print("ok")
