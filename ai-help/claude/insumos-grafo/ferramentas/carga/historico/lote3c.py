# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 3c: releitura dos objetos e metadata types de Agentforce Sales/Service que estavam como ausência 'desconhecido'.
import json
import b2_mdt as M
from b1_base import ev, af
from b3_obj import field, expo, obj, rel, cob, cnt, APEX_OK

BASE = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/"
CAT = BASE + "catalogo/"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")

# ================================================================ fontes
reg = json.load(open(BASE + "fontes/registro.json"))
B = "https://developer.salesforce.com/docs/atlas.en-us.264.0."
CHK = {"estado": "verificado", "nota": "Conteúdo lido em 2026-11-08 e conferido quanto ao assunto (não apenas HTTP 200)."}
def src(id, t, u, pert, extr):
    return {"id": id, "titulo": t, "url": u, "tipo": "oficial_documentacao", "versao": "68.0", "data_verificacao": "2026-11-08",
            "metodo": "extracao_documental_assistida", "pertinencia": pert, "extracao": "fontes/extracoes/" + extr, "checagem_online": CHK}
OBJS = ["Campaign", "CampaignMember", "Product2", "Pricebook2", "PricebookEntry", "OpportunityLineItem", "Quote", "QuoteLineItem", "ForecastingItem",
        "Territory2", "Territory2Type", "UserTerritory2Association", "ObjectTerritory2Association", "AgentWork", "ServiceChannel", "QueueRoutingConfig",
        "Entitlement", "SlaProcess", "ServiceContract", "MilestoneType", "AssignmentRule", "KnowledgeArticleVersion"]
novas = [src(f"src:objref-{o.lower()}", f"{o} (Object Reference)", B + f"object_reference.meta/object_reference/sforce_api_objects_{o.lower()}.htm",
             f"Chamadas e campos do objeto {o}.", "objref-lote3c.txt") for o in OBJS]
for sid, t, pg in [("assignmentrules", "AssignmentRules", "meta_assignmentrule.htm"), ("escalationrules", "EscalationRules", "meta_escalationrules.htm"),
                   ("servicechannel", "ServiceChannel", "meta_servicechannel.htm"), ("queueroutingconfig", "QueueRoutingConfig", "meta_queueroutingconfig.htm")]:
    novas.append(src(f"src:mdapi-{sid}", f"{t} (Metadata API)", B + f"api_meta.meta/api_meta/{pg}", f"Arquivo, versão e propriedades do tipo {t}.", "mdapi-lote3c.txt"))
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

# ================================================================ helpers de objeto
NOTA_NOME = "Nome listado na Object Reference; tipo e propriedades não extraídos nesta rodada."
TOOL_D = lambda: expo("tooling", "desconhecido", nota="Exposição na Tooling API não verificada.")
def mk(o, s, rows):
    out = []
    for r in rows:
        n, t, p, ver, d = r[:5]; kw = r[5] if len(r) > 5 else {}
        notas = kw.pop("notas", None)
        f = field("obj:" + o, n, t, p, ver, d, s, **kw)
        if notas: f["notas"] = notas
        out.append(f)
    return out
def completa(o, s, nomes, det):
    by = {f["nome"]: f for f in det}
    out = []
    for n in nomes:
        if n in by: out.append(by[n]); continue
        f = field("obj:" + o, n, "(a extrair)", None, None, None, s); f["notas"] = [NOTA_NOME]; out.append(f)
    return out
def O(nome, oq, papel, s, calls, campos, soql, est, esp, nota, desde=None, acesso=None, juncao=False, alertas=None):
    obj(nome, oq, papel, [expo("padrao", "verificado", s, calls, desde=desde, acesso=acesso), TOOL_D()], campos,
        [{"api": "padrao", "soql": soql, "contexto": "API padrão.", "validacao": "documental"}], APEX_OK(s),
        cob(est, esp, len(campos), cnt(campos), nota), s, juncao=juncao, alertas=alertas)
ALL = ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "search()", "undelete()", "update()", "upsert()"]
NODEL = ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "update()", "upsert()"]
ALVO_DESC = ["A página não declara 'Refers to'; o alvo vem da descrição do campo."]
VAL = "Valores conforme a página; não se declara lista completa."

# ---------------- Campaign
s = "src:objref-campaign"
nomes = ("ActualCost, AmountAllOpportunities, AmountWonOpportunities, BriefId, BudgetedCost, CampaignImageId, CampaignMemberRecordTypeId, CampaignStage, CreatedByID, CurrencyIsoCode, "
 "Description, EndDate, ExpectedResponse, ExpectedRevenue, HierarchyActualCost, HierarchyAmountAllOpportunities, HierarchyAmountWonOpportunities, HierarchyBudgetedCost, "
 "HierarchyExpectedRevenue, HierarchyNumberOfContacts, HierarchyNumberOfConvertedLeads, HierarchyNumberOfLeads, HierarchyNumberOfOpportunities, HierarchyNumberOfResponses, "
 "HierarchyNumberOfWonOpportunities, HierarchyNumberSent, HierarchyTotalEmailsDelivered, HierarchyTotalFormSubmissions, HierarchyTotalFormViews, HierarchyTotalLandingPageFormSubmissions, "
 "HierarchyTotalLandingPageViews, HierarchyUniqueEmailOpens, HierarchyUniqueEmailTrackedLinkClicks, HierarchyUniqueMarketingLinkClicks, IsActive, LastActivityDate, LastModifiedById, "
 "LastReferencedDate, LastViewedDate, Name, NumberOfContacts, NumberOfConvertedLeads, NumberOfLeads, NumberOfOpportunities, NumberOfResponses").split(", ")
det = mk("Campaign", s, [("Name", "string", "FGIS", None, "Nome da campanha.", {"req": ("sim", None)}),
 ("IsActive", "boolean", "DFGS", None, "Indica se a campanha está ativa.", {}),
 ("EndDate", "date", "FGNS", None, "Data de término da campanha.", {}),
 ("CampaignMemberRecordTypeId", "reference", "FGNS", None, "Tipo de registro aplicado aos membros desta campanha.", {"ref": ["obj:RecordType"], "rel": "CampaignMemberRecordType"})])
O("Campaign", "Representa uma campanha de marketing (evento, envio de e-mail, webinar).", "Agrupar membros e medir resultados de marketing.", s,
  ["describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "search()"], completa("Campaign", s, nomes, det),
  "SELECT Name, IsActive, EndDate FROM Campaign WHERE IsActive = true LIMIT 20", "parcial", None,
  "Object Reference servida truncada: a tabela termina em NumberOfResponses (45 nomes); ParentId, OwnerId, Status, Type e StartDate não foram servidos.",
  acesso="Usuários de Customer Portal não acessam.",
  alertas=["A lista de chamadas da página 68.0 não inclui create(), update() nem delete(). Registrado como na fonte; revalidar."])

# ---------------- CampaignMember
s = "src:objref-campaignmember"
nomes = ("AccountId, CampaignId, City, CompanyOrAccount, ContactId, CurrencyIsoCode, Country, Description, DoNotCall, Email, Fax, FirstName, FirstRespondedDate, HasOptedOutOfEmail, "
 "HasOptedOutOfFax, HasResponded, LastName, LeadId, LeadOrContactId, LeadOrContactOwnerId, LeadSource, MobilePhone, Name, Phone, PostalCode, RecordTypeId, Salutation, State, Status, "
 "Street, Title, Type").split(", ")
cond = ("condicional", "Informe ContactId ou LeadId (não ambos; se vierem os dois, só ContactId é gravado).")
det = mk("CampaignMember", s, [("AccountId", "reference", "CFGS", None, "Conta membro (com Accounts as Campaign Members).", {"ref": ["obj:Account"]}),
 ("CampaignId", "reference", "CFGS", None, "Campanha.", {"ref": ["obj:Campaign"], "req": ("sim", None)}),
 ("ContactId", "reference", "CFGNS", None, "Contato membro.", {"ref": ["obj:Contact"], "req": cond}),
 ("LeadId", "reference", "CFGNS", None, "Lead membro.", {"ref": ["obj:Lead"], "req": cond}),
 ("LeadOrContactId", "reference", "FGNS", None, "Id do lead ou contato (ou conta, com o recurso habilitado).", {}),
 ("Status", "picklist", "CFGNSU", None, "Status do membro (texto do valor, não o Id de CampaignMemberStatus).", {}),
 ("HasResponded", "boolean", "DFGS", None, "Indica se respondeu; definido indiretamente pelo Status.", {})])
O("CampaignMember", "Liga uma campanha a um lead, contato ou conta.", "Registrar quem participa de cada campanha e como respondeu.", s, NODEL,
  completa("CampaignMember", s, nomes, det), "SELECT CampaignId, LeadId, ContactId, Status, HasResponded FROM CampaignMember LIMIT 20", "completa", 32, "Tabela de campos lida completa (32).",
  juncao=True, alertas=["Criar um membro que já existe para o mesmo ContactId ou LeadId retorna erro; atualize pelo Id do CampaignMember."])

# ---------------- Product2
s = "src:objref-product2"
nomes = ("BillingPolicyId, CanUseQuantitySchedule, CanUseRevenueSchedule, ConnectionReceivedId, ConnectionSentId, ConfigureDuringSale, CurrencyIsoCode, Description, DisplayUrl, "
 "ExternalDataSourceId, ExternalId, Family, IsActive, IsArchived, IsAssetizable, IsDeleted, IsSerialized, IsSoldOnlyWithOtherProds, LastReferencedDate, LastViewedDate, Name, "
 "NumberOfQuantityInstallments, NumberOfRevenueInstallments, ProductClass, ProductCode, QuantityInstallmentPeriod, QuantityScheduleType, QuantityUnitOfMeasure, RecalculateTotalPrice, "
 "RevenueInstallmentPeriod, RevenueScheduleType, StockCheckMethod, StockKeepingUnit, TaxPolicyId, TransferRecordMode, Type, UnitOfMeasureId").split(", ")
det = mk("Product2", s, [("Name", "string", "CFGISU", None, "Nome do produto.", {}), ("ProductCode", "string", "CFGNSU", None, "Código do produto.", {}),
 ("IsActive", "boolean", "CDFGSU", None, "Indica se o produto está ativo.", {}), ("Family", "picklist", "CFGNSU", None, "Família (categoria) do produto.", {})])
O("Product2", "Representa um produto que a empresa vende.", "Catálogo de produtos usado em catálogos de preço, oportunidades e cotações.", s, ALL,
  completa("Product2", s, nomes, det), "SELECT Name, ProductCode, Family FROM Product2 WHERE IsActive = true LIMIT 20", "parcial", None,
  "Object Reference servida truncada no meio de UnitOfMeasureId (37 nomes); campos posteriores não foram servidos.",
  alertas=["O objeto Product (sem o 2) deixou de existir na API 8.0; use Product2."])

# ---------------- Pricebook2
s = "src:objref-pricebook2"
pb = mk("Pricebook2", s, [("Description", "string", "CFGNSU", None, "Descrição.", {}), ("IsActive", "boolean", "CDFGSU", None, "Indica se está ativo.", {}),
 ("IsArchived", "boolean", "DFGS", None, "Indica se está arquivado.", {}), ("IsDeleted", "boolean", "DF", None, "Indica se foi excluído.", {}),
 ("IsStandard", "boolean", "DFGS", None, "Indica se é o catálogo de preços padrão.", {}), ("LastReferencedDate", "dateTime", "FNS", None, "Última referência.", {}),
 ("LastViewedDate", "dateTime", "FNS", None, "Última visualização.", {}), ("Name", "string", "CFGISU", None, "Nome do catálogo.", {"req": ("sim", None)}),
 ("ValidFrom", "dateTime", "CFNSU", None, "Início da validade.", {}), ("ValidTo", "dateTime", "CFNSU", None, "Fim da validade.", {})])
O("Pricebook2", "Representa um catálogo de preços.", "Agrupar os preços de produtos; toda org tem um catálogo padrão.", s, ALL, pb,
  "SELECT Name, IsActive, IsStandard FROM Pricebook2", "completa", 10, "Tabela de campos lida completa (10).",
  alertas=["O catálogo padrão pode ser atualizado, mas não criado nem excluído pela API."])

# ---------------- PricebookEntry
s = "src:objref-pricebookentry"
pbe = mk("PricebookEntry", s, [("ActivePriceAdjustmentQuantity", "int", "FGNS", None, "Quantidade de ajustes de preço ativos.", {}),
 ("CurrencyIsoCode", "picklist", "CDFGRS", None, "Moeda da entrada.", {}), ("IsActive", "boolean", "CDFGSU", None, "Indica se a entrada está ativa.", {}),
 ("IsArchived", "boolean", "DFGS", None, "Indica se está arquivada (somente leitura).", {}), ("Name", "string", "FGNS", None, "Nome (do produto).", {}),
 ("Pricebook2Id", "reference", "CFGS", None, "Catálogo de preços.", {"ref": ["obj:Pricebook2"], "req": ("sim", None)}),
 ("Product2Id", "reference", "CFGS", None, "Produto.", {"ref": ["obj:Product2"], "req": ("sim", None)}),
 ("ProductCode", "string", "FGNS", None, "Código do produto.", {}),
 ("ProductSellingModelId", "reference", "CFGS", None, "Modelo de venda do produto.", {"ref": ["ProductSellingModel"]}),
 ("UnitPrice", "currency", "CFSU", None, "Preço unitário.", {"req": ("sim", None)}),
 ("UseStandardPrice", "boolean", "CDFGSU", None, "Usa o preço do catálogo padrão (torna UnitPrice somente leitura).", {})])
O("PricebookEntry", "Liga um produto a um catálogo de preços, com o preço.", "Definir quanto custa cada produto em cada catálogo e moeda.", s, NODEL, pbe,
  "SELECT Product2Id, Pricebook2Id, UnitPrice, IsActive FROM PricebookEntry WHERE IsActive = true LIMIT 20", "completa", 11, "Tabela de campos lida completa (11).",
  juncao=True, alertas=["O preço padrão precisa existir antes dos preços em catálogos customizados.", "Pricebook2Id e Product2Id não mudam depois da criação."])

# ---------------- OpportunityLineItem
s = "src:objref-opportunitylineitem"
nomes = ("CanUseQuantitySchedule, CanUseRevenueSchedule, ConnectionReceivedId, ConnectionSentId, CurrencyIsoCode, Description, Discount, HasQuantitySchedule, HasRevenueSchedule, "
 "HasSchedule, LastReferencedDate, LastSyncTime, LastViewedDate, ListPrice, Name, OpportunityId, PricebookEntryId, ProductId, Product2Id, ProductCode, Quantity, RecalculateTotalPrice, "
 "ServiceDate, SortOrder, Subtotal, TotalPrice, UnitPrice").split(", ")
cpt = ("condicional", "Informe UnitPrice ou TotalPrice, não ambos.")
det = mk("OpportunityLineItem", s, [("OpportunityId", "reference", "CFGS", None, "Oportunidade do item.", {"ref": ["obj:Opportunity"], "req": ("sim", None)}),
 ("PricebookEntryId", "reference", "CFGNS", None, "Entrada de catálogo de preços do produto.", {"ref": ["obj:PricebookEntry"], "req": ("sim", None)}),
 ("ProductId", "reference", "CFN", None, None, {"notas": ["Indisponível desde a API 3.0; mantido só por compatibilidade (Object Reference)."]}),
 ("Product2Id", "reference", "CFGNS", None, "Produto do item (somente leitura desde a API 30.0).", {"ref": ["obj:Product2"]}),
 ("Quantity", "double", "CFSU", None, "Quantidade.", {}), ("UnitPrice", "currency", "CDFNSU", None, "Preço unitário.", {"req": cpt}),
 ("TotalPrice", "currency", "CDFNSU", None, "Preço total.", {"req": cpt}), ("ListPrice", "currency", "FNS", None, "Preço de lista.", {})])
O("OpportunityLineItem", "Representa um produto incluído numa oportunidade.", "Compor o valor da oportunidade a partir de produtos e preços.", s, NODEL,
  completa("OpportunityLineItem", s, nomes, det), "SELECT OpportunityId, Product2Id, Quantity, UnitPrice, TotalPrice FROM OpportunityLineItem LIMIT 20",
  "completa", 27, "Tabela de campos lida completa (27).", juncao=True,
  alertas=["Só existe em orgs com produtos habilitados.", "Cada item precisa de uma PricebookEntry do Pricebook2 da oportunidade."])

# ---------------- Quote
s = "src:objref-quote"
nomes = ("AccountId, AdditionalAddress, AdditionalCity, AdditionalCountry, AdditionalCountryCode, AdditionalLatitude, AdditionalLongitude, AdditionalName, AdditionalPostalCode, "
 "AdditionalState, AdditionalStateCode, AdditionalStreet, BillToContactId, BillingAddress, BillingCity, BillingCountry, BillingCountryCode, BillingLatitude, BillingLongitude, BillingName, "
 "BillingPostalCode, BillingState, BillingStateCode, BillingStreet, CalculationStatus, CanCreateQuoteLineItems, ContactId, ContractId, CurrencyIsoCode, Description, Discount, Email, "
 "ExpirationDate, Fax, GrandTotal, IsSyncing, InsuranceQuoteType, LastReferencedDate, LastViewedDate, LineItemCount, Name, OpportunityId, Phone, Pricebook2Id").split(", ")
det = mk("Quote", s, [("Name", "string", "CFIU", None, "Nome da cotação.", {"req": ("sim", None)}),
 ("OpportunityId", "reference", "CF", None, "Oportunidade da cotação.", {"ref": ["obj:Opportunity"], "notas": ALVO_DESC}),
 ("IsSyncing", "boolean", "DF", None, "Indica se esta cotação está sincronizada com a oportunidade.", {}),
 ("AccountId", "reference", "FGNS", None, "Conta da cotação.", {"ref": ["obj:Account"], "notas": ALVO_DESC}),
 ("ContactId", "reference", "FGNS", None, "Contato da cotação.", {"ref": ["obj:Contact"], "notas": ALVO_DESC})])
O("Quote", "Representa uma cotação: os preços propostos ao cliente.", "Enviar propostas; uma cotação por vez sincroniza com a oportunidade.", s, ALL,
  completa("Quote", s, nomes, det), "SELECT Name, OpportunityId, IsSyncing, GrandTotal FROM Quote LIMIT 20", "parcial", None,
  "Object Reference servida truncada na linha de Pricebook2Id (44 nomes); Status e campos posteriores não foram servidos.")

# ---------------- QuoteLineItem
s = "src:objref-quotelineitem"
nomes = ("BatchIdentifier, BillingFrequency, BillingReference, CurrencyIsoCode, CustomProductName, Description, Discount, DiscountAmount, DoesAutomaticallyRenew, Division, "
 "EffectiveGrantDate, EndDate, EndDateTime, EndQuantity, EndTime, HasQuantitySchedule, HasRevenueSchedule, HasSchedule, IsPrimarySegment, LastReferencedDate, LastViewedDate, "
 "LegalEntityId, LineNumber, ListPrice, ListPriceTotal, Margin, MarginAmount, NetTotalPrice, NetUnitPrice, OpportunityLineItemId, ParentQuoteLineItemId, PartnerDiscountPercent, "
 "PartnerUnitPrice, PeriodBoundary, PeriodBoundaryDay, PeriodBoundaryStartMonth, PricebookEntryId, PriceRevisionPolicyId, PricingContractId, PriceWaterfallIdentifier, PricingTerm, "
 "PricingTermCount, PricingTermUnit, Product2Id, ProductInstanceIdentifier, ProductSellingModelId, ProrationPolicyId, Quantity, QuantityUnitOfMeasureId, QuoteActionId, QuoteId, "
 "QuoteLineGroupId, QuoteLineItemRecipientId, RampIdentifier, RelatedQuoteLineItemId, SegmentIdentifier, SegmentName, SegmentType, SellingModelType, ServiceDate, SortOrder, StartDate, "
 "StartDateTime, StartEndTimeZone, StartTime, StartQuantity, StartingPriceTotal, StartingUnitPriceSource, Status, SubscriptionTerm, SubscriptionTermUnit, Subtotal, TotalAdjustment, "
 "TotalAdjustmentAmount, TotalCost, TotalLineAmount, TotalMargin, TotalMarginAmount, TotalPrice, UnitCost, UnitPrice, UnitPriceUplift, ValidationResult, Visibility").split(", ")
det = mk("QuoteLineItem", s, [("QuoteId", "reference", "CFGS", None, "Cotação do item.", {"ref": ["obj:Quote"], "req": ("sim", None), "notas": ALVO_DESC}),
 ("PricebookEntryId", "reference", "CFGS", None, "Entrada de catálogo de preços.", {"req": ("sim", None)}),
 ("Product2Id", "reference", "CFGS", None, "Produto.", {"req": ("sim", None)}),
 ("OpportunityLineItemId", "reference", "CFGNS", None, "Item de oportunidade correspondente.", {}),
 ("Quantity", "double", "CFSU", None, "Quantidade.", {"req": ("sim", None)}), ("UnitPrice", "currency", "CFSU", None, "Preço unitário.", {"req": ("sim", None)})])
O("QuoteLineItem", "Representa um produto incluído numa cotação.", "Detalhar os itens e preços da proposta.", s, ALL,
  completa("QuoteLineItem", s, nomes, det), "SELECT QuoteId, Product2Id, Quantity, UnitPrice FROM QuoteLineItem LIMIT 20", "completa", 84,
  "Tabela de campos lida completa (84); a página foi cortada depois, na seção Usage. Muitos campos pertencem a recursos de receita (Revenue Cloud) e podem não existir em toda org.",
  alertas=["A cotação só aceita itens se tiver Pricebook2; cada item precisa corresponder a um produto desse catálogo."])

# ---------------- ForecastingItem
s = "src:objref-forecastingitem"
fi = mk("ForecastingItem", s, [("AmountWithoutAdjustments", "double", "FNS", None, "Valor sem ajustes.", {}),
 ("AmountWithoutManagerAdjustment", "double", "FNS", None, "Valor sem ajuste do gestor.", {}), ("AmountWithoutOwnerAdjustment", "double", "FNS", None, "Valor sem ajuste do próprio usuário.", {}),
 ("ForecastAmount", "double", "FNS", None, "Valor previsto.", {}), ("ForecastCategoryName", "picklist", "FGNRS", None, "Categoria de previsão.", {}),
 ("ForecastQuantity", "double", "FNS", "28.0", "Quantidade prevista.", {}), ("ForecastingGroupItemId", "reference", "CFGNS", "60.0", "Item de grupo de previsão.", {"ref": ["ForecastingGroupItem"]}),
 ("ForecastingItemCategory", "picklist", "FGS", None, "Categoria do item.", {}), ("ForecastingTypeId", "reference", "FGS", None, "Tipo de previsão.", {}),
 ("HasAdjustment", "boolean", "DFGS", None, "Indica se há ajuste.", {}), ("HasOwnerAdjustment", "boolean", "DFGS", "33.0", "Indica se há ajuste do próprio usuário.", {}),
 ("IsAmount", "boolean", "DFGS", "28.0", "Indica previsão por valor.", {}), ("IsQuantity", "boolean", "DFGS", "28.0", "Indica previsão por quantidade.", {}),
 ("IsUpToDate", "boolean", "DFGS", None, "Indica se está atualizado.", {}), ("OwnerId", "reference", "FGS", None, "Dono da previsão.", {}),
 ("OwnerOnlyAmount", "double", "FNS", None, "Valor só do dono.", {}), ("OwnerOnlyQuantity", "double", "FNS", "28.0", "Quantidade só do dono.", {}),
 ("ParentForecastingItemId", "reference", "FGNS", None, "Item de previsão pai.", {}), ("PeriodId", "reference", "FGNS", None, "Período.", {}),
 ("ProductFamily", "picklist", "FGNS", "29.0", "Família de produto (somente leitura).", {}), ("QuantityWithoutAdjustments", "double", "FNS", "28.0", "Quantidade sem ajustes.", {}),
 ("QuantityWithoutManagerAdjustment", "double", "FNS", "28.0", "Quantidade sem ajuste do gestor.", {}),
 ("QuantityWithoutOwnerAdjustment", "double", "FNS", "38.0", "Quantidade sem ajuste do dono.", {}), ("SubordinateOverrides", "int", "FGS", "38.0", "Número de ajustes de subordinados.", {}),
 ("Territory2Id", "reference", "FGNS", "43.0", "Território da previsão.", {})])
O("ForecastingItem", "Guarda os valores de previsão de cada usuário ou território, com e sem ajustes.", "Ler a previsão conforme a perspectiva e o papel do usuário.", s,
  ["describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()"], fi,
  "SELECT OwnerId, PeriodId, ForecastAmount, ForecastCategoryName FROM ForecastingItem LIMIT 20", "completa", 25, "Tabela de campos lida completa (25).", desde="26.0",
  acesso="Só usuários com View All Forecasts, Allow Forecasting ou status de gestor delegado.",
  alertas=["Somente leitura.", "Com vários tipos de previsão, filtre por ForecastingTypeId."])

# ---------------- Territory2, Territory2Type, associações
s = "src:objref-territory2"
t2 = mk("Territory2", s, [("AccountAccessLevel", "picklist", "CFGRSU", None, "Acesso a contas do território.", {}), ("CaseAccessLevel", "picklist", "CFGRSU", None, "Acesso a casos.", {}),
 ("ContactAccessLevel", "picklist", "FGRS", None, "Acesso a contatos.", {}), ("Description", "string", "CFNSU", None, "Descrição.", {}),
 ("DeveloperName", "string", "CFGSU", None, "Nome único na API.", {"req": ("sim", None)}), ("ForecastUserId", "reference", "FGNSU", None, "Gestor de previsão do território.", {}),
 ("Name", "string", "CFGSU", None, "Nome do território.", {}), ("OpportunityAccessLevel", "picklist", "CFGRSU", None, "Acesso a oportunidades.", {}),
 ("ParentTerritory2Id", "reference", "CFGNSU", None, "Território pai.", {}), ("Territory2ModelId", "reference", "CFGS", None, "Modelo de territórios.", {}),
 ("Territory2TypeId", "reference", "CFGSU", None, "Tipo do território.", {})])
O("Territory2", "Representa um território de vendas dentro de um modelo.", "Organizar contas e usuários por território.", s,
  ["create()", "delete()", "describeLayout()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"], t2,
  "SELECT Name, DeveloperName, Territory2ModelId FROM Territory2 LIMIT 20", "completa", 11, "Tabela de campos lida completa (11). A página não declara alvos dos campos reference.",
  acesso="Só com Sales Territories habilitado; usuários padrão e parceiros veem modelos ativos.")
s = "src:objref-territory2type"
tt = mk("Territory2Type", s, [("Description", "textarea", "CFGNSU", None, "Descrição.", {}), ("DeveloperName", "string", "CFGSU", None, "Nome único na API.", {"req": ("sim", None)}),
 ("Language", "picklist", "CFGNRSU", None, "Idioma.", {}), ("MasterLabel", "string", "CFGSU", None, "Rótulo.", {"req": ("sim", None)}),
 ("Priority", "int", "CFGSU", None, "Prioridade, usada na atribuição de territórios a oportunidades; única entre os tipos.", {"req": ("sim", None), "notas": ["A página imprime as propriedades como 'Sort' e 'Update' colados."]})])
O("Territory2Type", "Categoria de territórios; todo território tem um tipo.", "Classificar territórios e priorizar atribuições.", s,
  ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"], tt, "SELECT MasterLabel, DeveloperName, Priority FROM Territory2Type",
  "completa", 5, "Tabela de campos lida completa (5).", acesso="Só com Sales Territories habilitado.")
s = "src:objref-userterritory2association"
ut = mk("UserTerritory2Association", s, [("IsActive", "boolean", "DFGS", None, "Indica se a atribuição está ativa.", {}),
 ("RoleInTerritory2", "picklist", "CFGNSU", None, "Papel do usuário no território.", {"vals": ["Owner", "Administrator", "Sales Rep"], "contexto": VAL}),
 ("Territory2Id", "reference", "CFGS", None, "Território.", {}), ("UserId", "reference", "CFGS", None, "Usuário.", {})])
O("UserTerritory2Association", "Liga um usuário a um território.", "Definir quem trabalha em cada território.", s,
  ["create()", "delete()", "describeSObjects()", "query()", "retrieve()"], ut, "SELECT UserId, Territory2Id, RoleInTerritory2 FROM UserTerritory2Association LIMIT 20",
  "completa", 4, "Tabela de campos lida completa (4). A página não declara alvos dos campos reference.", juncao=True,
  acesso="Só com Sales Territories habilitado; campos customizados não são suportados.")
s = "src:objref-objectterritory2association"
ot = mk("ObjectTerritory2Association", s, [("AssociationCause", "picklist", "CFGRS", None, "Motivo da associação.", {}),
 ("ObjectId", "reference", "CFGS", None, "Registro associado: conta (desde 30.0) ou lead (desde 55.0).", {"ref": ["obj:Account", "obj:Lead"]}),
 ("SobjectType", "picklist", "FGNRS", None, "Tipo do registro associado.", {}), ("Territory2Id", "reference", "CFGS", None, "Território.", {"ref": ["obj:Territory2"]})])
O("ObjectTerritory2Association", "Liga uma conta ou lead a um território.", "Registrar quais registros pertencem a cada território.", s,
  ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()"], ot,
  "SELECT ObjectId, Territory2Id, AssociationCause FROM ObjectTerritory2Association LIMIT 20", "completa", 4, "Tabela de campos lida completa (4).", juncao=True,
  acesso="Só com Sales Territories habilitado.", alertas=["Associações excluídas não vão para a lixeira e podem ser consultadas por 12 horas."])

# ---------------- AgentWork, ServiceChannel, QueueRoutingConfig
s = "src:objref-agentwork"
nomes = ("AbandonedDateTime, AcceptDateTime, ActiveTime, AcwExtensionCount, AcwExtensionDuration, AfterConversationActualTime, AgentCapacityWhenDeclined, AssignedDateTime, BotId, BotType, "
 "CancelDateTime, CapacityModel, CapacityPercentage, CapacityWeight, CloseDateTime, DeclineDateTime, DeclineReason, ExternalBotId, HandleTime, IsConference, IsInterruptible, "
 "IsOwnerChangeInitiated, IsPreferredUserRequired, IsStatusChangeInitiated, IsTransfer, Name, OriginalGroupId, OriginalQueueId, OwnerId, PausedCapacityPercentage, PausedCapacityWeight, "
 "PendingServiceRoutingId, PreferredUserId, PushTimeout, PushTimeoutDateTime, RequestDateTime, RoutingModel, RoutingPriority, RoutingType, SecondaryRoutingPriority, ServiceChannelId").split(", ")
det = mk("AgentWork", s, [("ServiceChannelId", "reference", "CFGS", None, "Canal de serviço do trabalho.", {"notas": ["Alvo cortado na página servida."]}),
 ("PendingServiceRoutingId", "reference", "CFGNS", None, "Roteamento pendente que originou o trabalho.", {"ref": ["PendingServiceRouting"]}),
 ("CapacityWeight", "double", "CFNS", None, "Unidades de capacidade consumidas.", {})])
O("AgentWork", "Representa um trabalho atribuído a um atendente pelo Omni-Channel.", "Acompanhar atribuição, aceite e capacidade consumida.", s,
  ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "undelete()", "update()", "upsert()"],
  completa("AgentWork", s, nomes, det), "SELECT Name, ServiceChannelId, CapacityWeight, AcceptDateTime FROM AgentWork LIMIT 20", "parcial", None,
  "Object Reference servida truncada em ServiceChannelId (41 nomes); WorkItemId, UserId e Status não foram servidos.", desde="32.0", acesso="Requer Omni-Channel habilitado.",
  alertas=["Transferir o trabalho cria um novo AgentWork.", "O relatório de pesquisa indicou conflito 30.0 x 32.0; a página relida declara 32.0."])
s = "src:objref-servicechannel"
acw = ("condicional", "Obrigatório quando HasAcwExtensionEnabled é true.")
sc = mk("ServiceChannel", s, [("AcwExtensionDuration", "int", "CFGNSU", None, "Duração de cada extensão do trabalho pós-conversa.", {"req": acw}),
 ("AfterConvoWorkMaxTime", "int", "CFGNSU", None, "Tempo máximo do trabalho pós-conversa.", {"req": ("condicional", "Obrigatório quando HasAfterConvoWorkTimer é true.")}),
 ("CapacityModel", "picklist", "CFGNRSU", None, "Modelo de capacidade.", {}), ("CustomSoundId", "reference", "CFGNSU", None, "Som customizado.", {"ref": ["StaticResource"], "rel": "CustomSound"}),
 ("DeveloperName", "string", "CFGSU", None, "Nome único na API.", {}), ("DoesCheckCapOnOwnerChange", "boolean", "CDFGSU", None, "Verifica capacidade na troca de dono.", {}),
 ("DoesCheckCapOnStatusChange", "boolean", "CDFGSU", None, "Verifica capacidade na troca de status.", {}),
 ("DoesMinimizeWidgetOnAccept", "boolean", "CDFGSU", None, "Minimiza o widget ao aceitar.", {}), ("DoesOverridePresenceAudio", "boolean", "CDFGSU", None, "Substitui o áudio de presença.", {}),
 ("HasAcwExtensionEnabled", "boolean", "CDFGSU", None, "Permite estender o trabalho pós-conversa.", {}), ("HasAfterConvoWorkTimer", "boolean", "CDFGSU", None, "Ativa o temporizador pós-conversa.", {}),
 ("HasAutoAcceptEnabled", "boolean", "CDFGSU", None, "Aceita o trabalho automaticamente.", {}), ("Language", "picklist", "CDFGNRSU", None, "Idioma.", {}),
 ("MasterLabel", "string", "CFGSU", None, "Rótulo.", {}), ("MaxExtensions", "picklist", "CFGNRSU", None, "Número máximo de extensões.", {"req": acw}),
 ("RelatedEntity", "picklist", "CFGRSU", None, "Objeto roteado pelo canal.", {}),
 ("RoutingConfigurationId", "reference", "CFGNSU", None, "Configuração de roteamento.", {"ref": ["obj:QueueRoutingConfig"], "rel": "RoutingConfiguration"}),
 ("SecRoutingPriorityField", "picklist", "CFGNRSU", None, "Campo de prioridade secundária.", {}), ("SoundLength", "int", "CFGNSU", None, "Duração do som.", {}),
 ("StatusField", "picklist", "CFGNRSU", None, "Campo de status do trabalho.", {})])
O("ServiceChannel", "Representa um canal de serviço do Omni-Channel (casos, mensagens, chamadas).", "Dizer ao Omni-Channel que tipo de registro rotear e como.", s,
  ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"], sc, "SELECT MasterLabel, DeveloperName, RelatedEntity FROM ServiceChannel",
  "completa", 20, "Tabela de campos lida completa (20).", desde="32.0")
s = "src:objref-queueroutingconfig"
qr = mk("QueueRoutingConfig", s, [("CapacityPercentage", "percent", "CFNSU", "33.0", "Percentual de capacidade consumido.", {}),
 ("CapacityWeight", "double", "CFNSU", "33.0", "Unidades de capacidade consumidas.", {}), ("DeveloperName", "string", "CFGSU", None, "Nome único na API.", {}),
 ("DropAdditionalSkillsTimeout", "int", "CFGNSU", None, "Tempo até descartar habilidades adicionais.", {}), ("IsAttributeBased", "boolean", "CDFGSU", "45.0", "Usa regras de roteamento por habilidades.", {}),
 ("Language", "picklist", "CFGNRSU", None, "Idioma.", {}), ("MasterLabel", "string", "CFGSU", None, "Rótulo.", {}),
 ("OverflowAssigneeId", "reference", "CFGNSU", None, "Usuário ou fila de transbordo.", {}),
 ("PausedCapacityPercentage", "percent", "CFNSU", None, "Capacidade consumida em pausa (status-based e Enhanced).", {}),
 ("PausedCapacityWeight", "double", "CFNSU", None, "Unidades consumidas em pausa (status-based e Enhanced).", {}),
 ("PushTimeout", "int", "CFGNSU", "36.0", "Tempo limite de envio; 0 quando desativado.", {}),
 ("RoutingModel", "picklist", "CFGRSU", None, "Modelo de roteamento.", {"vals": ["Least Active", "Most Available"], "contexto": VAL}),
 ("RoutingPriority", "int", "CFGSU", None, "Prioridade de roteamento.", {}),
 ("ServiceChannelId", "reference", "CFGNSU", None, "Canal de serviço.", {"notas": ["A página diz 'available in API 32.0 and earlier', o que parece erro de texto; revalidar."]})])
O("QueueRoutingConfig", "Configuração de roteamento de uma fila do Omni-Channel.", "Definir prioridade, modelo de roteamento e capacidade do trabalho da fila.", s,
  ["create()", "delete()", "query()", "retrieve()", "update()"], qr, "SELECT MasterLabel, RoutingModel, RoutingPriority FROM QueueRoutingConfig", "parcial", 15,
  "A tabela tem 15 linhas, mas uma veio sem nome de campo; 14 catalogadas.", desde="32.0")

# ---------------- Entitlement, SlaProcess, ServiceContract, MilestoneType
s = "src:objref-entitlement"
nomes = ("AccountId, AssetId, AssetWarrantyID, BusinessHoursId, CasesPerEntitlement, ContractLineItemId, EndDate, IsPerIncident, LastReferencedDate, LastViewedDate, LocationID, Name, "
 "SvcApptBookingWindowsId, RemainingCases, RemainingWorkOrders, ServiceContractId, SlaProcessId, StartDate, Status, SvcApptBookingWindows, Type, WorkOrdersPerEntitlement").split(", ")
NREQ = ["A extração marcou 'Required', mas o campo é anulável; obrigatoriedade não registrada."]
det = mk("Entitlement", s, [("Name", "string", "CFU", None, "Nome do entitlement.", {"req": ("sim", None)}),
 ("AccountId", "reference", "CFGS", None, "Conta com direito ao suporte.", {"ref": ["obj:Account"]}),
 ("SlaProcessId", "reference", "CFNU", "19.0", "Processo de entitlement (SLA Policy) aplicado.", {"ref": ["obj:SlaProcess"]}),
 ("BusinessHoursId", "reference", "FGNS", None, "Horário comercial do entitlement.", {"ref": ["obj:BusinessHours"], "notas": NREQ}),
 ("ServiceContractId", "reference", "CFNU", None, "Contrato de serviço.", {"ref": ["obj:ServiceContract"], "notas": NREQ}),
 ("AssetId", "reference", "FGNS", None, "Ativo coberto.", {"ref": ["Asset"], "notas": NREQ}),
 ("StartDate", "date", "CFNU", None, "Início.", {}), ("EndDate", "date", "CFNU", None, "Fim.", {}), ("Status", "picklist", "FN", None, "Situação do entitlement.", {})])
O("Entitlement", "Representa o direito de um cliente a um tipo de suporte.", "Verificar se o cliente tem direito e aplicar o processo de SLA.", s,
  ["create()", "delete()", "describeLayout()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "search()", "undelete()", "update()", "upsert()"],
  completa("Entitlement", s, nomes, det), "SELECT Name, AccountId, SlaProcessId, Status FROM Entitlement LIMIT 20", "parcial", 23,
  "A tabela tem 23 linhas, mas uma veio sem nome de campo; 22 catalogadas.", desde="18.0",
  alertas=["A lista de chamadas da página não inclui describeSObjects(); registrado como na fonte.", "CasesPerEntitlement e RemainingCases só valem com IsPerIncident = true."])
s = "src:objref-slaprocess"
sp = mk("SlaProcess", s, [("BusinessHoursId", "reference", "FGNS", None, "Horário comercial do processo.", {"notas": NREQ}),
 ("Description", "textarea", "FN", None, "Descrição.", {}), ("IsActive", "boolean", "DF", None, "Indica se está ativo.", {}),
 ("IsVersionDefault", "boolean", "DFGS", "28.0", "Indica a versão padrão.", {}), ("LastViewedDate", "dateTime", "FNS", None, "Última visualização.", {}),
 ("Name", "string", "FI", None, "Nome do processo.", {}), ("NameNorm", "string", "FGS", "28.0", "Nome normalizado (minúsculas).", {}),
 ("SObjectType", "picklist", "FGRS", None, "Objeto em que o processo roda (caso ou ordem de trabalho).", {}), ("StartDateField", "picklist", "FR", None, "Campo de data de entrada.", {}),
 ("VersionMaster", "string", "FGNS", "28.0", "Identificador comum às versões.", {}), ("VersionNotes", "textarea", "FGNS", "28.0", "Notas da versão.", {}),
 ("VersionNumber", "int", "FGNS", "28.0", "Número da versão.", {})])
O("SlaProcess", "Representa um processo de entitlement (SLA Policy) como registro consultável.", "Consultar os processos aplicados a entitlements.", s,
  ["describeSObjects()", "query()", "retrieve()", "search()", "describeLayout()"], sp, "SELECT Name, IsActive, SObjectType, VersionNumber FROM SlaProcess",
  "completa", 12, "Tabela de campos lida completa (12).", desde="19.0")
s = "src:objref-servicecontract"
nomes = ("AccountId, ActivationDate, AdditionalDiscount, ApprovalStatus, BillingAddress, BillingCity, BillingCountry, BillingCountryCode, BillingLatitude, BillingLongitude, BillingPostalCode, "
 "BillingState, BillingStateCode, BillingStreet, ContactId, ContractNumber, Description, Discount, EndDate, GrandTotal, IsDeleted, LastReferencedDate, LastViewedDate, LineItemCount, Name, "
 "OwnerId, ParentServiceContractId, Pricebook2Id, RootServiceContractId, ShippingAddress, ShippingCity, ShippingCountry, ShippingCountryCode, ShippingLatitude, ShippingLongitude, "
 "ShippingPostalCode, ShippingState, ShippingStateCode, ShippingStreet, SpecialTerms, StartDate, Status, Subtotal, Tax, Term, TotalPrice").split(", ")
det = mk("ServiceContract", s, [("Name", "string", "CFGSU", None, "Nome do contrato.", {}),
 ("AccountId", "reference", "FGNS", None, "Conta do contrato.", {"ref": ["obj:Account"], "notas": ALVO_DESC}),
 ("ContactId", "reference", "FGNS", None, "Contato do contrato.", {"ref": ["obj:Contact"]}),
 ("StartDate", "date", "CFNU", None, "Início.", {}), ("EndDate", "date", "FGNS", None, "Fim.", {}), ("Status", "picklist", "FN", None, "Situação.", {}),
 ("Pricebook2Id", "reference", "CFGNSU", None, "Catálogo de preços.", {"ref": ["obj:Pricebook2"]}),
 ("ParentServiceContractId", "reference", "CFGNSU", None, "Contrato pai.", {"ref": ["obj:ServiceContract"]}),
 ("BillingAddress", "address", None, None, None, {"notas": ["Marcado como beta na página."]}), ("ShippingAddress", "address", None, None, None, {"notas": ["Marcado como beta na página."]})])
O("ServiceContract", "Representa um contrato de serviço com o cliente.", "Definir o suporte contratado no nível do contrato.", s, ALL,
  completa("ServiceContract", s, nomes, det), "SELECT Name, AccountId, StartDate, EndDate, Status FROM ServiceContract LIMIT 20", "completa", 46, "Tabela de campos lida completa (46).", desde="18.0")
s = "src:objref-milestonetype"
mt = mk("MilestoneType", s, [("Description", "textarea", "CFNU", None, "Descrição.", {}), ("Name", "string", "CFIU", None, "Nome do milestone.", {}),
 ("RecurrenceType", "picklist", "CU", None, "Tipo de recorrência.", {})])
O("MilestoneType", "Representa um tipo de milestone (por exemplo, primeira resposta).", "Definir as etapas usadas nos processos de entitlement.", s,
  ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"], mt, "SELECT Name, RecurrenceType FROM MilestoneType",
  "completa", 3, "Tabela de campos lida completa (3).", desde="18.0")

# ---------------- AssignmentRule, KnowledgeArticleVersion
s = "src:objref-assignmentrule"
ar = mk("AssignmentRule", s, [("Active", "boolean", "DFGS", None, "Indica se a regra está ativa.", {}), ("Name", "string", "FGNS", None, "Nome da regra.", {}),
 ("SobjectType", "picklist", "FGNRS", None, "Objeto da regra (caso ou lead).", {})])
O("AssignmentRule", "Representa uma regra de atribuição de casos ou leads.", "Obter o Id da regra para usá-la no AssignmentRuleHeader.", s,
  ["describeSObjects()", "query()", "retrieve()", "search()"], ar, "SELECT Name, SobjectType, Active FROM AssignmentRule WHERE Active = true", "completa", 3, "Tabela de campos lida completa (3).",
  alertas=["Consulte a regra pelo nome e informe o Id em AssignmentRuleHeader ao criar ou atualizar Case ou Lead (SOAP, REST ou Bulk API)."])
s = "src:objref-knowledgearticleversion"
nomes = ("ArchivedById, ArchivedDate, ArticleArchivedById, ArticleArchivedDate, ArticleCaseAttachCount, ArticleCreatedById, ArticleCreatedDate, ArticleMasterLanguage, ArticleNumber, "
 "ArticleTotalViewCount, ArticleType, AssignedById, AssignedToId, AssignmentDate, AssignmentDueDate, AssignmentNote, FirstPublishedDate, IsLatestVersion, IsMasterLanguage, IsOutOfDate, "
 "IsVisibleInApp, IsVisibleInCsp, IsVisibleInPkb, IsVisibleInPrm, KnowledgeArticleId, Language, LargeLanguageModel, LastPublishedDate, MasterVersionId, MigratedToFromArticleVersion, "
 "NextReviewDate, OwnerId, PublishStatus, SourceId, Summary, Title, TranslationCompletedDate, TranslationExportedDate, TranslationImportedDate, UrlName, ValidationStatus").split(", ")
det = mk("KnowledgeArticleVersion", s, [("KnowledgeArticleId", "reference", "FGS", None, "Id do artigo, independente da versão.", {"ref": ["KnowledgeArticle"]}),
 ("PublishStatus", "picklist", "DFGRS", None, "Situação de publicação.", {"vals": ["Draft", "Online", "Archived"], "contexto": VAL}),
 ("Language", "picklist", "FGRS", None, "Idioma da versão.", {}), ("Title", "string", "FGIS", None, "Título (até 255 caracteres).", {"req": ("sim", None)}),
 ("UrlName", "string", "FGIS", None, "Nome de URL, único (até 255 caracteres; letras, números e hífens).", {"req": ("sim", None)}),
 ("IsLatestVersion", "boolean", "DFGS", "24.0", "Indica a versão mais recente.", {})])
O("KnowledgeArticleVersion", "Representa uma versão de artigo de conhecimento, comum a todos os tipos de artigo.", "Consultar e buscar artigos entre tipos; atualizar campos padrão de rascunhos.", s,
  ["describeLayout()", "describeSObjects()", "query()", "retrieve()", "search()"], completa("KnowledgeArticleVersion", s, nomes, det),
  "SELECT Title, UrlName, PublishStatus, Language FROM KnowledgeArticleVersion WHERE PublishStatus = 'Online' AND Language = 'en_US' LIMIT 20", "parcial", None,
  "Object Reference servida truncada depois de ValidationStatus (41 nomes).", desde="18.0",
  alertas=["Knowledge__kav deriva deste objeto: no Lightning Knowledge, criar, atualizar e excluir é feito por Knowledge__kav."])

# ================================================================ metadata types
SA, SE = "src:mdapi-assignmentrules", "src:mdapi-escalationrules"
FN = lambda s: ("fullName", "string", "S", None, "Nome da regra; herdado de Metadata e obrigatório em create, update e delete.", {"herdada": "Metadata"})
M.struct("AssignmentRule", SA, ["mdt:AssignmentRules"], [("active", "boolean", "N", None, "Se a regra está ativa."), FN(SA),
 ("ruleEntry", "RuleEntry[]", "N", None, "Entradas da regra.", {"estrutura": "AssignmentRules_RuleEntry"})], "Uma regra de atribuição nomeada.")
M.struct("AssignmentRules_RuleEntry", SA, ["mdx:AssignmentRule"], [
 ("assignedTo", "string", "N", None, "Usuário ou fila que recebe o registro."),
 ("assignedToType", "AssignToLookupValueType", "N", None, "Se o destino é usuário ou fila.", {"vals": [("User", None), ("Queue", None)]}),
 ("booleanFilter", "string", "N", None, "Lógica avançada de filtro."),
 ("criteriaItems", "FilterItem[]", "N", None, "Critérios da entrada (use isto ou formula).", {"estrutura": "FilterItem"}),
 ("formula", "string", "N", None, "Fórmula de critério (use isto ou criteriaItems)."),
 ("notifyCcRecipients", "boolean", "N", "32.0", "Copia os destinatários em Cc na resposta automática (Email-to-Case, Web-to-Lead)."),
 ("overrideExistingTeams", "boolean", "N", None, "Se a equipe do caso é substituída (true) ou acrescida (false)."),
 ("team", "string[]", "N", None, "Equipes de caso predefinidas."), ("template", "string", "N", None, "Modelo de e-mail enviado ao novo dono.")],
 "Entrada de uma regra de atribuição. O id do projeto inclui o tipo pai porque EscalationRules tem outro subtipo com o mesmo nome RuleEntry.")
M.struct("EscalationRule", SE, ["mdt:EscalationRules"], [("active", "boolean", "N", None, "Se a regra está ativa."), FN(SE),
 ("ruleEntry", "RuleEntry[]", "N", None, "Entradas da regra.", {"estrutura": "EscalationRules_RuleEntry"})], "Uma regra de escalonamento nomeada.")
M.struct("EscalationRules_RuleEntry", SE, ["mdx:EscalationRule"], [
 ("booleanFilter", "string", "N", None, "Lógica avançada de filtro."),
 ("businessHours", "string", "N", None, "Horário em que as ações rodam; só quando businessHoursSource é Static."),
 ("businessHoursSource", "string", "N", None, "Origem do horário comercial.", {"vals": [("None", None), ("Case", None), ("Static", None)]}),
 ("criteriaItems", "FilterItem", "N", None, "Critérios da entrada.", {"estrutura": "FilterItem"}),
 ("disableEscalationWhenModified", "boolean", "N", None, "Desliga o escalonamento quando o registro é alterado."),
 ("escalationAction", "EscalationAction[]", "N", None, "Ações executadas quando os critérios são atendidos.", {"estrutura": "EscalationAction"}),
 ("escalationStartTime", "string", "N", None, "Momento de início da contagem.", {"vals": [("CaseCreation", None), ("CaseLastModified", None)]}),
 ("formula", "string", "N", None, "Fórmula de critério (use isto ou criteriaItems).")],
 "Entrada de uma regra de escalonamento. O id do projeto inclui o tipo pai porque AssignmentRules tem outro subtipo com o mesmo nome RuleEntry.")
M.struct("EscalationAction", SE, ["mdx:EscalationRules_RuleEntry"], [
 ("assignedTo", "string", "N", None, "Usuário ou fila que recebe o caso."), ("assignedToTemplate", "string", "N", None, "Modelo de e-mail para o novo dono."),
 ("assignedToType", "string", "N", None, "Se o destino é usuário ou fila.", {"vals": [("User", None), ("Queue", None)]}),
 ("minutesToEscalation", "int", "N", None, "Minutos até o escalonamento."), ("notifyCaseOwner", "boolean", "N", None, "Notifica o dono do caso."),
 ("notifyEmail", "string", "N", None, "E-mail a notificar."), ("notifyTo", "string", "N", None, "Usuário a notificar."),
 ("notifyToTemplate", "string", "N", None, "Modelo do e-mail de notificação.")], "Ação de escalonamento.")
SC, SQ = "src:mdapi-servicechannel", "src:mdapi-queueroutingconfig"
M.struct("ServiceChannelFieldPriority", SC, ["mdt:ServiceChannel"], [("priority", "int", "S", None, "Número de prioridade do valor mapeado."),
 ("type", "picklist", "S", None, "Situação do trabalho do valor mapeado.", {"vals": [("IN_PROGRESS", None), ("PAUSED", None), ("COMPLETED", None)]}),
 ("value", "string", "S", None, "Valor do campo de status ou do campo de prioridade secundária do canal pai.",
  {"notas": ["A página lista duas linhas chamadas value (uma para statusField e outra para secondaryRoutingPriorityField); aqui uma única propriedade."]})],
 "Mapeamento de valores de campo para prioridade ou situação do trabalho.")
M.struct("QueueRoutingConfigSkill", SQ, ["mdt:QueueRoutingConfig"], [("skill", "string", "N", None, "Habilidade usada para rotear o trabalho.")], "Habilidade padrão de roteamento.")

M.mdt("AssignmentRules", SA, "Contêiner das regras de atribuição de um objeto (um arquivo por objeto, como Case.assignmentRules).",
      "Implantar as regras que definem o dono de casos e leads.", "27.0",
      [("assignmentRule", "AssignmentRule[]", "N", None, "Regras de atribuição do objeto.", {"estrutura": "AssignmentRule"})], curinga=True,
      setup=af("verificado", "Setup > Quick Find: Assignment Rules > Lead Assignment Rules | Case Assignment Rules", None, [ev("src:help-assign-guide")]),
      alertas=["A página fala em 'todos os objetos aplicáveis' sem listá-los; os exemplos usam Case."])
M.mdt("EscalationRules", SE, "Contêiner das regras de escalonamento de casos (arquivo Case.escalationRules).",
      "Implantar as regras que escalonam casos não resolvidos a tempo.", "27.0",
      [("escalationRule", "EscalationRule[]", "N", None, "Regras de escalonamento, processadas na ordem do contêiner.", {"estrutura": "EscalationRule"})], curinga=True,
      divergencias=["A tabela da página grafa a propriedade herdada como 'fullname'; o tipo Metadata usa fullName."])
M.mdt("ServiceChannel", SC, "Define um canal de serviço do Omni-Channel.", "Implantar canais e suas regras de capacidade e trabalho pós-conversa.", "44.0", [
 ("acwExtensionDuration", "int", "C:obrigatório quando hasAcwExtensionEnabled é true", None, "Segundos de cada extensão pós-conversa (10 a 3600; Messaging e Voice)."),
 ("afterConvoWorkMaxTime", "int", "C:obrigatório quando hasAfterConvoWorkTimer é true", None, "Segundos máximos de trabalho pós-conversa (10 a 3600; Messaging e Voice)."),
 ("capacityModel", "picklist", "N", "65.0", "Quando a capacidade do atendente é liberada.", {"vals": [("STATUS_BASED", None), ("TAB_BASED", None)]}),
 ("doesCheckCapOnOwnerChange", "boolean", "N", "65.0", "Mantém o trabalho com o atendente na troca de dono.", {"default": ("false", None, None)}),
 ("doesCheckCapOnStatusChange", "boolean", "N", "65.0", "Reatribui trabalho reaberto ao mesmo atendente.", {"default": ("false", None, None)}),
 ("doesMinimizeWidgetOnAccept", "boolean", "N", "48.0", "Minimiza o widget ao aceitar o trabalho."),
 ("hasAcwExtensionEnabled", "boolean", "N", "56.0", "Permite estender o trabalho pós-conversa.", {"default": ("false", None, None)}),
 ("hasAfterConvoWorkTimer", "boolean", "N", None, "Ativa o tempo de trabalho pós-conversa (Voice desde 52.0, Messaging desde 56.0).", {"default": ("false", None, None)}),
 ("hasAutoAcceptEnabled", "boolean", "N", None, "Abre o trabalho automaticamente, sem aceite manual."),
 ("interactionComponent", "string", "N", None, "Componente do console aberto no rodapé ao aceitar."),
 ("isInterruptible", "boolean", "N", "57.0", "Se o trabalho usa capacidade interrompível ou primária.", {"default": ("false", None, None)}),
 ("label", "string", "S", None, "Rótulo do canal."),
 ("maxExtensions", "picklist", "C:obrigatório quando hasAcwExtensionEnabled é true", "56.0", "Número máximo de extensões (1 a 10)."),
 ("relatedEntityType", "string", "S", None, "Objeto associado ao canal."),
 ("secondaryRoutingPriorityField", "string", "N", "47.0", "Campo usado na prioridade secundária."),
 ("serviceChannelStatusFieldMappings", "ServiceChannelFieldPriority", "N", "65.0", "Valores que indicam trabalho concluído e em andamento.", {"estrutura": "ServiceChannelFieldPriority"}),
 ("serviceChannelFieldPriorities", "ServiceChannelFieldPriority[]", "S", "47.0", "Mapeia valores de prioridade secundária para prioridades.", {"estrutura": "ServiceChannelFieldPriority"}),
 ("statusField", "picklist", "N", "65.0", "Campo de status do trabalho no modelo por status."), M.FULLNAME_HERDADO(SC)], curinga=True, alertas=["Requer Omni-Channel habilitado."])
M.mdt("QueueRoutingConfig", SQ, "Define uma configuração de roteamento de fila do Omni-Channel.", "Implantar prioridade, modelo de roteamento e capacidade de filas.", "44.0", [
 ("capacityPercentage", "double", "N", None, "Percentual da capacidade consumido (voz exige 100)."),
 ("capacityType", "CapacityType", "N", None, "Controla se o trabalho gerado é interrompível; sem valor, age como INHERITED.",
  {"vals": [("INHERITED", None), ("INTERRUPTIBLE", None), ("NOT INTERRUPTIBLE", None)], "completa": "desconhecido",
   "contexto": "Valores descritos no texto da página; grafia de 'NOT INTERRUPTIBLE' a confirmar no WSDL."}),
 ("capacityWeight", "double", "N", None, "Unidades de capacidade consumidas."), ("dropAdditionalSkillsTimeout", "int", "N", None, "Segundos até descartar habilidades adicionais."),
 ("isAttributeBased", "boolean", "N", None, "Se usa regras de roteamento por habilidades."), ("label", "string", "S", None, "Rótulo da configuração."),
 ("PausedCapacityPercentage", "double", "N", "64.0", "Capacidade consumida em pausa."), ("PausedCapacityWeight", "double", "N", "64.0", "Unidades consumidas em pausa."),
 ("pushTimeout", "int", "N", None, "Tempo limite de envio em segundos; 0 quando desativado."), ("queueOverflowAssignee", "string", "N", None, "Fila de transbordo."),
 ("QueueRoutingConfigSkill", "QueueRoutingConfigSkill[]", "N", None, "Habilidades padrão de roteamento.", {"estrutura": "QueueRoutingConfigSkill"}),
 ("routingModel", "RoutingModel", "S", None, "Como o trabalho é enviado aos atendentes.", {"vals": [("LEAST_ACTIVE", None), ("MOST_AVAILABLE", None), ("EXTERNAL_ROUTING", None)]}),
 ("routingPriority", "int", "S", None, "Ordem de roteamento entre configurações; menor vai primeiro."), ("userOverflowAssignee", "string", "N", None, "Usuário de transbordo."),
 M.FULLNAME_HERDADO(SQ)], curinga=True, alertas=["Requer Omni-Channel habilitado."],
 divergencias=["A seção de sufixo da página cita 'ServicePresenceStatus components' e a descrição de label fala em status de presença; parecem erros de cópia na documentação."])
M.emit_structs()
for sid in ("AssignmentRules_RuleEntry", "EscalationRules_RuleEntry"):
    d = ld(f"estruturas/{sid}.json"); d["nome"] = "RuleEntry"; sv(f"estruturas/{sid}.json", d)
fi_ = ld("estruturas/FilterItem.json")
fi_["usada_por"] = sorted(set(fi_["usada_por"]) | {"mdx:AssignmentRules_RuleEntry", "mdx:EscalationRules_RuleEntry"})
sv("estruturas/FilterItem.json", fi_)

# ================================================================ relacionamentos
N1 = lambda: af("desconhecido", "N:1", "Estrutura de lookup indica N:1; não comprovado nesta sessão.")
R = [("campaign-campaignmember-recordtype", "Campaign", "CampaignMemberRecordTypeId", "RecordType", "A campanha define o tipo de registro dos seus membros.", "src:objref-campaign", None),
 ("campaignmember-campaign", "CampaignMember", "CampaignId", "Campaign", "Cada membro pertence a uma campanha.", "src:objref-campaignmember", None),
 ("campaignmember-lead", "CampaignMember", "LeadId", "Lead", "O membro pode ser um lead.", "src:objref-campaignmember", "Quando o membro é um lead."),
 ("campaignmember-contact", "CampaignMember", "ContactId", "Contact", "O membro pode ser um contato.", "src:objref-campaignmember", "Quando o membro é um contato."),
 ("campaignmember-account", "CampaignMember", "AccountId", "Account", "O membro pode ser uma conta.", "src:objref-campaignmember", "Com Accounts as Campaign Members habilitado."),
 ("pricebookentry-pricebook2", "PricebookEntry", "Pricebook2Id", "Pricebook2", "A entrada pertence a um catálogo de preços.", "src:objref-pricebookentry", None),
 ("pricebookentry-product2", "PricebookEntry", "Product2Id", "Product2", "A entrada dá preço a um produto.", "src:objref-pricebookentry", None),
 ("oli-opportunity", "OpportunityLineItem", "OpportunityId", "Opportunity", "O item pertence a uma oportunidade.", "src:objref-opportunitylineitem", None),
 ("oli-pricebookentry", "OpportunityLineItem", "PricebookEntryId", "PricebookEntry", "O item usa uma entrada do catálogo da oportunidade.", "src:objref-opportunitylineitem", None),
 ("oli-product2", "OpportunityLineItem", "Product2Id", "Product2", "O item aponta para o produto.", "src:objref-opportunitylineitem", None),
 ("quote-opportunity", "Quote", "OpportunityId", "Opportunity", "A cotação pertence a uma oportunidade.", "src:objref-quote", None),
 ("quote-account", "Quote", "AccountId", "Account", "A cotação pode ter uma conta.", "src:objref-quote", None),
 ("quote-contact", "Quote", "ContactId", "Contact", "A cotação pode ter um contato.", "src:objref-quote", None),
 ("qli-quote", "QuoteLineItem", "QuoteId", "Quote", "O item pertence a uma cotação.", "src:objref-quotelineitem", None),
 ("ot2a-territory2", "ObjectTerritory2Association", "Territory2Id", "Territory2", "A associação aponta para o território.", "src:objref-objectterritory2association", None),
 ("ot2a-account", "ObjectTerritory2Association", "ObjectId", "Account", "O registro associado pode ser uma conta.", "src:objref-objectterritory2association", "Quando o registro é uma conta (desde 30.0)."),
 ("ot2a-lead", "ObjectTerritory2Association", "ObjectId", "Lead", "O registro associado pode ser um lead.", "src:objref-objectterritory2association", "Quando o registro é um lead (desde 55.0)."),
 ("servicechannel-queueroutingconfig", "ServiceChannel", "RoutingConfigurationId", "QueueRoutingConfig", "O canal pode usar uma configuração de roteamento.", "src:objref-servicechannel", None),
 ("entitlement-account", "Entitlement", "AccountId", "Account", "O entitlement pertence a uma conta.", "src:objref-entitlement", None),
 ("entitlement-slaprocess", "Entitlement", "SlaProcessId", "SlaProcess", "O entitlement aplica um processo de SLA.", "src:objref-entitlement", None),
 ("entitlement-businesshours", "Entitlement", "BusinessHoursId", "BusinessHours", "O entitlement pode ter horário comercial próprio.", "src:objref-entitlement", None),
 ("entitlement-servicecontract", "Entitlement", "ServiceContractId", "ServiceContract", "O entitlement pode vir de um contrato de serviço.", "src:objref-entitlement", None),
 ("servicecontract-account", "ServiceContract", "AccountId", "Account", "O contrato pertence a uma conta.", "src:objref-servicecontract", None),
 ("servicecontract-contact", "ServiceContract", "ContactId", "Contact", "O contrato tem um contato.", "src:objref-servicecontract", None),
 ("servicecontract-pricebook2", "ServiceContract", "Pricebook2Id", "Pricebook2", "O contrato pode usar um catálogo de preços.", "src:objref-servicecontract", None),
 ("servicecontract-parent", "ServiceContract", "ParentServiceContractId", "ServiceContract", "Contratos podem ter contrato pai.", "src:objref-servicecontract", None)]
for rid, oo, campo, dd, expl, s, cond in R:
    rel(rid, "referencia_campo", {"entidade": "obj:" + oo, "campo": campo}, {"entidade": "obj:" + dd}, expl, "verificado", [s], N1(), cond=cond)
for a, b, srcs, t in [("entitlementprocess-slaprocess", ("EntitlementProcess", "SlaProcess"), ["src:mdapi-entitlementprocess", "src:objref-slaprocess"], "processos de entitlement; o nome do arquivo corresponde a SlaProcess.NameNorm"),
                      ("servicechannel", ("ServiceChannel", "ServiceChannel"), ["src:mdapi-servicechannel", "src:objref-servicechannel"], "canais de serviço"),
                      ("queueroutingconfig", ("QueueRoutingConfig", "QueueRoutingConfig"), ["src:mdapi-queueroutingconfig", "src:objref-queueroutingconfig"], "configurações de roteamento"),
                      ("assignmentrules", ("AssignmentRules", "AssignmentRule"), ["src:mdapi-assignmentrules", "src:objref-assignmentrule"], "regras de atribuição")]:
    rel(f"rep-{a}", "representacao_comum", {"entidade": f"mdt:{b[0]}"}, {"entidade": f"obj:{b[1]}"},
        f"Metadata type e objeto API descrevem {t} por caminhos diferentes: definição implantável versus registro consultável. A correspondência campo a campo não foi comprovada.", "verificado", srcs)

# ================================================================ funcionalidades
def upd(fid, objs=None, mdts=None, ausencias=None, ev_add=(), limit=None):
    f = ld(f"funcionalidades/{fid}.json"); r = f["representacoes"]
    if objs: r["objetos_api"] += [{"ref": "obj:" + o, "papel": p} for o, p in objs]
    if mdts: r["metadata_types"] += [{"ref": "mdt:" + m, "papel": p} for m, p in mdts]
    if ausencias is not None: r["ausencias"] = ausencias
    for s in ev_add:
        if not any(e["fonte"] == s for e in f["evidencias"]): f["evidencias"].append(ev(s))
    if limit is not None: f["limitacoes"] = limit
    sv(f"funcionalidades/{fid}.json", f)
D = lambda tipo, m: {"tipo": tipo, "estado": "desconhecido", "motivo": m}
upd("campanhas", [("Campaign", "Registro de cada campanha."), ("CampaignMember", "Membro da campanha (junção com lead, contato ou conta).")],
    ausencias=[D("metadata_type", "Não investigado. Candidato no inventário v68, ainda não lido: CampaignSettings.")], ev_add=["src:objref-campaign", "src:objref-campaignmember"], limit=[])
upd("produtos-e-catalogos-de-preco", [("Product2", "Produto."), ("Pricebook2", "Catálogo de preços."), ("PricebookEntry", "Preço de um produto num catálogo (junção)."),
    ("OpportunityLineItem", "Produto incluído numa oportunidade.")], ausencias=[D("metadata_type", "Não investigado.")],
    ev_add=["src:objref-product2", "src:objref-pricebook2", "src:objref-pricebookentry", "src:objref-opportunitylineitem"], limit=[])
upd("cotacoes", [("Quote", "Registro de cada cotação."), ("QuoteLineItem", "Produto incluído numa cotação.")],
    ausencias=[D("metadata_type", "Não investigado. Candidato no inventário v68, ainda não lido: QuoteSettings.")], ev_add=["src:objref-quote", "src:objref-quotelineitem"])
upd("previsoes-colaborativas", [("ForecastingItem", "Valores de previsão por usuário ou território (somente leitura).")],
    ausencias=[D("objeto_api", "Ainda não relidos: ForecastingAdjustment, ForecastingOwnerAdjustment, ForecastingType, ForecastingFact, ForecastingQuota."),
               D("metadata_type", "Não investigado. Candidato no inventário v68, ainda não lido: ForecastingSettings.")], ev_add=["src:objref-forecastingitem"])
upd("territorios-de-vendas", [("Territory2", "Território."), ("Territory2Type", "Tipo de território."), ("UserTerritory2Association", "Usuário no território (junção)."),
    ("ObjectTerritory2Association", "Conta ou lead no território (junção).")], ausencias=[],
    ev_add=["src:objref-territory2", "src:objref-territory2type", "src:objref-userterritory2association", "src:objref-objectterritory2association"],
    limit=["Metadata types Territory2, Territory2Rule, Territory2Type e Territory2Settings constam do inventário v68, mas não foram lidos."])
upd("omni-channel", [("AgentWork", "Trabalho atribuído a um atendente."), ("ServiceChannel", "Canal de serviço consultável."), ("QueueRoutingConfig", "Configuração de roteamento consultável.")],
    [("ServiceChannel", "Canal de serviço implantável."), ("QueueRoutingConfig", "Configuração de roteamento implantável.")],
    ausencias=[D("objeto_api", "Ainda não relidos: ServicePresenceStatus (objeto), PresenceUserConfig, PendingServiceRouting."),
               D("metadata_type", "Não investigado. Candidatos no inventário v68, ainda não lidos: PresenceUserConfig, OmniChannelSettings.")],
    ev_add=["src:objref-agentwork", "src:objref-servicechannel", "src:objref-queueroutingconfig", "src:mdapi-servicechannel", "src:mdapi-queueroutingconfig"])
upd("lightning-knowledge", [("KnowledgeArticleVersion", "Versão de artigo, comum a todos os tipos.")],
    ausencias=[D("objeto_api", "Ainda não relidos: Knowledge__kav, KnowledgeArticle."), D("metadata_type", "Não investigado. Candidato no inventário v68, ainda não lido: KnowledgeSettings.")],
    ev_add=["src:objref-knowledgearticleversion"])
upd("entitlements-e-milestones", [("Entitlement", "Direito do cliente ao suporte."), ("SlaProcess", "Processo de entitlement consultável."),
    ("ServiceContract", "Contrato de serviço."), ("MilestoneType", "Tipo de milestone.")],
    ausencias=[D("metadata_type", "Não investigado. Candidatos no inventário v68, ainda não lidos: EntitlementSettings, EntitlementTemplate, MilestoneType.")],
    ev_add=["src:objref-entitlement", "src:objref-slaprocess", "src:objref-servicecontract", "src:objref-milestonetype"])
upd("regras-de-atribuicao", [("AssignmentRule", "Regra de atribuição consultável (Id para o AssignmentRuleHeader).")],
    [("AssignmentRules", "Regras de atribuição implantáveis, por objeto."), ("EscalationRules", "Regras de escalonamento implantáveis.")], ausencias=[],
    ev_add=["src:objref-assignmentrule", "src:mdapi-assignmentrules", "src:mdapi-escalationrules"],
    limit=["Caminho de Escalation Rules no Setup não verificado."])

# ================================================================ nuvens
sales = ld("nuvens/sales-cloud.json")
sales["limites"][0] = "Metadata types de configuração (*Settings) e alguns objetos de previsão ainda não lidos diretamente (ver relatorios/retomada.md)."
sv("nuvens/sales-cloud.json", sales)
serv = ld("nuvens/service-cloud.json")
serv["limites"][0] = "Objetos de presença do Omni-Channel, Knowledge__kav e metadata types *Settings ainda não lidos diretamente (ver relatorios/retomada.md)."
sv("nuvens/service-cloud.json", serv)
print("ok")
