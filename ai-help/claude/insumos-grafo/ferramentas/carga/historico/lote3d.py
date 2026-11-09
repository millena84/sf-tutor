# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 3d: fecha as pendências de Agentforce Sales/Service (metadata types restantes, *Settings, objetos de previsão/presença/Knowledge).
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
def src(id, t, u, pert, extr, tipo="oficial_documentacao", ver="68.0", metodo="extracao_documental_assistida"):
    return {"id": id, "titulo": t, "url": u, "tipo": tipo, "versao": ver, "data_verificacao": "2026-11-08", "metodo": metodo, "pertinencia": pert,
            "extracao": "fontes/extracoes/" + extr, "checagem_online": CHK}
MD = {"Territory2": "meta_territory2.htm", "Territory2Rule": "meta_territory2rule.htm", "Territory2Type": "meta_territory2type.htm", "MilestoneType": "meta_milestonetype.htm",
      "EntitlementTemplate": "meta_entitlementtemplate.htm", "PresenceUserConfig": "meta_presenceuserconfig.htm", "EntitlementSettings": "meta_entitlementsettings.htm",
      "AccountSettings": "meta_accountsettings.htm", "OpportunitySettings": "meta_opportunityssettings.htm", "QuoteSettings": "meta_quotessettings.htm",
      "BusinessHoursSettings": "meta_businesshourssettings.htm", "OmniChannelSettings": "meta_omnichannelsettings.htm", "KnowledgeSettings": "meta_knowledgesettings.htm",
      "LeadConvertSettings": "meta_leadconvertsettings.htm", "ForecastingSettings": "meta_forecastingsettings.htm", "Territory2Settings": "meta_territory2settings.htm",
      "CampaignSettings": "meta_campaignsettings.htm"}
novas = [src(f"src:mdapi-{n.lower()}", f"{n} (Metadata API)", B + f"api_meta.meta/api_meta/{pg}", f"Arquivo, versão e propriedades do tipo {n}.", "mdapi-lote3d.txt") for n, pg in MD.items()]
OB = ["ForecastingAdjustment", "ForecastingOwnerAdjustment", "ForecastingType", "ForecastingFact", "ForecastingQuota", "PendingServiceRouting", "ServicePresenceStatus", "PresenceUserConfig", "KnowledgeArticle"]
novas += [src(f"src:objref-{o.lower()}", f"{o} (Object Reference)", B + f"object_reference.meta/object_reference/sforce_api_objects_{o.lower()}.htm", f"Chamadas e campos do objeto {o}.", "objref-lote3d.txt") for o in OB]
novas.append(src("src:help-escalation-setup", "Set Up Escalation Rules", "https://help.salesforce.com/s/articleView?id=sf.rules_escalation_create.htm",
                 "Caminho Escalation Rules, permissão e regras de uso.", "help-nuvens-lote3d.txt", "oficial_ajuda", "sem versão (Ajuda Salesforce)", "leitura_resultado_busca"))
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

# ================================================================ arquivos de *Settings (pasta settings do registro do CLI)
SETTINGS_FILE = {"EntitlementSettings": "Entitlements", "AccountSettings": "Account", "OpportunitySettings": "Opportunity", "QuoteSettings": "Quote",
                 "BusinessHoursSettings": "BusinessHours", "OmniChannelSettings": "OmniChannel", "KnowledgeSettings": "Knowledge", "ForecastingSettings": "Forecasting",
                 "Territory2Settings": "Territory2", "CampaignSettings": "Campaign"}
_orig_arquivos = M.arquivos
def _arquivos(nome, parent=None):
    if nome in SETTINGS_FILE:
        base = SETTINGS_FILE[nome]; s = f"src:mdapi-{nome.lower()}"
        return {"source_format": af("verificado", {"pasta": "settings/", "arquivo": f"{base}.settings-meta.xml"},
                    "Pasta e sufixo do tipo genérico Settings no registro do Salesforce CLI; o nome-base do arquivo vem da página do tipo.",
                    [ev("src:sdr-registry", "types.settings"), ev(s)]),
                "metadata_api_format": af("verificado", {"pasta": "settings/", "arquivo": f"{base}.settings"},
                    "Um único arquivo por tipo de configuração; no package.xml, o tipo é Settings e o membro é o nome-base.", [ev(s)])}
    return _orig_arquivos(nome, parent)
M.arquivos = _arquivos
NOCUR = False   # curinga não se aplica a um Settings individual (só ao recuperar todos)
ALERTA_SET = "No package.xml, use o tipo Settings com o nome-base do arquivo como membro; o curinga só vale para recuperar todas as configurações."

def P(n, t, ver=None, d=None, req="N", **kw): return (n, t, req, ver, d, kw)
DF = ("false", None, None)
DT = ("valor", "true", None)
FN = lambda: M.FULLNAME_HERDADO(None)

# ================================================================ estruturas
S = "src:mdapi-territory2"
M.struct("FieldValue", S, ["mdt:Territory2", "mdt:Territory2Model"], [P("name", "string", None, "Nome do campo customizado (a página descreve como rótulo do território).", "S"),
 P("value", "anyType", None, "Valor do campo; pode ser nulo; o tipo vai declarado no XML.")], "Par nome-valor de um campo customizado.")
M.struct("Territory2AccessLevel", S, ["mdt:Territory2"], [P("accessLevel", "string", None, "Nível de acesso concedido ao tipo de objeto.", "S", vals=[("Read", None), ("Edit", None), ("Transfer", None), ("All", None)]),
 P("objectType", "string", None, "Tipo de objeto ligado ao território (por exemplo, Lead).", "S")], "Nível de acesso por tipo de objeto (desde 57.0).")
M.struct("Territory2RuleAssociation", S, ["mdt:Territory2"], [P("inherited", "boolean", None, "Se a regra vem do território pai (true) ou é local (false).", "S"),
 P("ruleName", "string", None, "Nome da regra, no mesmo modelo.", "S")], "Regra de atribuição associada ao território.")
S = "src:mdapi-territory2rule"
M.struct("Territory2RuleItem", S, ["mdt:Territory2Rule"], [P("field", "string", None, "Campo avaliado."),
 P("operation", "FilterOperation", None, "Operador do critério.", vals=[(v, None) for v in ["equals", "notEqual", "lessThan", "greaterThan", "lessOrEqual", "greaterOrEqual", "contains", "notContain", "startsWith", "includes", "excludes", "within"]]),
 P("value", "string", None, "Valor(es) comparado(s).")], "Item de critério de uma regra de território.")
S = "src:mdapi-presenceuserconfig"
M.struct("PresenceConfigAssignments", S, ["mdt:PresenceUserConfig"], [P("profiles", "PresenceConfigProfileAssignments", None, "Perfis associados.", estrutura="PresenceConfigProfileAssignments"),
 P("users", "PresenceConfigUserAssignments", None, "Usuários associados.", estrutura="PresenceConfigUserAssignments")], "Atribuição da configuração a perfis e usuários.")
M.struct("PresenceConfigProfileAssignments", S, ["mdx:PresenceConfigAssignments"], [P("profile", "string", None, "Nome do perfil.")], "Perfil associado.")
M.struct("PresenceConfigUserAssignments", S, ["mdx:PresenceConfigAssignments"], [P("user", "string", None, "Nome de usuário associado.")], "Usuário associado.")
S = "src:mdapi-opportunitysettings"
M.struct("FindSimilarOppFilter", S, ["mdt:OpportunitySettings"], [P("similarOpportunitiesDisplayColumns", "string", None, "Colunas exibidas na comparação."),
 P("similarOpportunitiesMatchFields", "string", None, "Campos usados na comparação.")], "Parâmetros de oportunidades semelhantes.")
S = "src:mdapi-territory2settings"
M.struct("Territory2SettingsOpportunityFilter", S, ["mdt:Territory2Settings"], [P("apexClassName", "string", None, "Classe Apex."),
 P("enableFilter", "boolean", None, "Usa a classe para atribuir territórios a oportunidades."),
 P("runMultiThreaded", "boolean", "62.0", "Executa a classe em várias threads.", "S", default=DF), P("runOnCreate", "boolean", None, "Executa ao criar oportunidade.")],
 "Filtro de atribuição de territórios a oportunidades por classe Apex.")
M.struct("Territory2SupportedObject", S, ["mdt:Territory2Settings"], [P("defaultAccessLevel", "string", None, "Acesso padrão.", "S", vals=[("Read", None), ("Edit", None), ("Transfer", None), ("All", None)]),
 P("objectType", "string", None, "Objeto suportado (único valor: Lead).", "S", vals=[("Lead", None)]),
 P("state", "string", None, "Se a atribuição está ativa para o objeto.", "S", vals=[("Disabled", None), ("Enabled", None)])], "Objeto com atribuição de território (desde 57.0).")
S = "src:mdapi-businesshourssettings"
dias = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
PT = dict(zip(dias, ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]))
bhe = [P("timeZoneId", "string", None, "Fuso horário."), P("name", "string", None, "Nome do horário (deve ser único)."), P("active", "string", None, "Se está ativo."),
       P("default", "string", None, "Se é o padrão.")]
for d in dias: bhe += [P(f"{d}StartTime", "string", None, f"Início de {PT[d]} (HH:mm:ss.SSSZ)."), P(f"{d}EndTime", "string", None, f"Fim de {PT[d]}; 00:00:00.000Z é meia-noite.")]
M.struct("BusinessHoursEntry", S, ["mdt:BusinessHoursSettings"], bhe, "Um horário comercial dentro das configurações.")
hc = "C:defina startTime e endTime juntos, ou ambos nulos para o dia inteiro"
M.struct("Holidays", S, ["mdt:BusinessHoursSettings"], [P("name", "string", None, "Nome do feriado (não precisa ser único)."), P("description", "string", None, "Descrição."),
 P("isRecurring", "string", None, "Se o feriado se repete."), P("activityDate", "string", None, "Data do feriado não recorrente."),
 P("recurrenceStartDate", "string", None, "Primeira data de recorrência (yyyy-mm-dd)."), P("recurrenceEndDate", "string", None, "Última data de recorrência (yyyy-mm-dd)."),
 P("startTime", "string", None, "Hora de início no feriado.", hc), P("endTime", "string", None, "Hora de fim no feriado.", hc),
 P("recurrenceType", "string", None, "Padrão de recorrência (a página lista sete valores, não extraídos)."), P("recurrenceInterval", "string", None, "Intervalo entre recorrências."),
 P("recurrenceDayOfWeek", "string", None, "Dia da semana."), P("recurrenceDayOfMonth", "string", None, "Dia do mês (1 a 31)."),
 P("recurrenceInstance", "string", None, "Ordinal (First a Last) para recorrências do tipo N-ésimo."), P("recurrenceMonthOfYear", "string", None, "Mês."),
 P("businessHours", "string", None, "Horário comercial ao qual o feriado se aplica.")], "Feriado usado em horários comerciais.")
S = "src:mdapi-leadconvertsettings"
M.struct("ObjectMapping", S, ["mdt:LeadConvertSettings"], [P("inputObject", "string", None, "Objeto de origem (sempre Lead).", "S"),
 P("mappingFields", "ObjectMappingField[]", None, "Pares de campos de origem e destino.", estrutura="ObjectMappingField"),
 P("outputObject", "string", None, "Objeto de destino.", "S", vals=[("Account", None), ("Contact", None), ("Opportunity", None)])], "Mapeamento de campos de lead para um objeto na conversão.")
M.struct("ObjectMappingField", S, ["mdx:ObjectMapping"], [P("inputField", "string", None, "Campo customizado de lead (origem).", "S"),
 P("outputField", "string", None, "Campo customizado de conta, contato ou oportunidade (destino).", "S")], "Par de campos mapeados.")

# ================================================================ metadata types
def MT(nome, o, f, desde, rows, **kw):
    return M.mdt(nome, f"src:mdapi-{nome.lower()}", o, f, desde, rows, **kw)
SALES_T = ["Requer Sales Territories habilitado.", "Sem suporte a packaging, change sets e chamadas CRUD.", "deploy() exige Manage Territories."]
MT("Territory2", "Define um território dentro de um modelo de territórios.", "Implantar a hierarquia de territórios e seus níveis de acesso.", "32.0", [
 P("accountAccessLevel", "string", None, "Acesso a contas atribuídas.", vals=[("Read", None), ("Edit", None), ("All", None)]),
 P("caseAccessLevel", "string", None, "Acesso a casos atribuídos.", vals=[("None", None), ("Read", None), ("Edit", None)]),
 P("contactAccessLevel", "string", None, "Acesso a contatos atribuídos.", vals=[("None", None), ("Read", None), ("Edit", None)]),
 P("customFields", "FieldValue", None, "Valores de campos customizados do território.", estrutura="FieldValue"), P("description", "string", None, "Descrição."),
 P("name", "string", None, "Rótulo do território.", "S"), P("objectAccessLevels", "Territory2AccessLevel", "57.0", "Níveis de acesso por objeto.", estrutura="Territory2AccessLevel"),
 P("opportunityAccessLevel", "string", None, "Acesso a oportunidades atribuídas.", vals=[("None", None), ("Read", None), ("Edit", None)]),
 P("parentTerritory", "string", None, "Nome de desenvolvedor do território pai."),
 P("ruleAssociations", "Territory2RuleAssociation[]", None, "Regras associadas.", estrutura="Territory2RuleAssociation"),
 P("territory2Type", "string", None, "Tipo do território.", "S"), FN()], curinga=True, alertas=SALES_T + ["Fica na pasta territories dentro da pasta do modelo."])
MT("Territory2Rule", "Define uma regra de atribuição de registros a territórios.", "Implantar os critérios que atribuem contas a territórios.", "32.0", [
 P("active", "boolean", None, "Se a regra está ativa.", "S"), P("booleanFilter", "string", None, "Lógica avançada de filtro."), P("name", "string", None, "Rótulo da regra.", "S"),
 P("objectType", "string", None, "Objeto da regra (na 32.0, só Account).", "S"),
 P("ruleItems", "Territory2RuleItem", None, "Itens de critério.", estrutura="Territory2RuleItem"), FN()], curinga=True,
 alertas=SALES_T + ["deploy() também exige Modify Metadata Through Metadata API Functions ou Modify All Data.", "Regras não podem ser executadas pela Metadata API."])
MT("Territory2Type", "Define um tipo de território.", "Implantar as categorias de território e suas prioridades.", "32.0", [
 P("description", "string", None, "Descrição."), P("name", "string", None, "Rótulo do tipo.", "S"),
 P("priority", "int", None, "Prioridade usada na atribuição de territórios a oportunidades; única entre os tipos.", "S"), FN()], curinga=True, alertas=SALES_T)
MT("MilestoneType", "Define um tipo de milestone.", "Implantar as etapas usadas nos processos de entitlement.", "27.0", [
 P("description", "string", None, "Descrição."),
 P("RecurrenceType", "MilestoneTypeRecurrenceType", "29.0", "Como o milestone se repete.", vals=[("none", "ocorre uma vez"), ("recursIndependently", "repete de forma independente"), ("recursChained", "repete em sequência")]), FN()], curinga=True)
MT("EntitlementTemplate", "Define um modelo de entitlement para produtos.", "Pré-definir os termos de suporte de um produto.", "18.0", [
 P("businessHours", "string", None, "Horário comercial coberto."), P("casesPerEntitlement", "int", None, "Total de casos cobertos."),
 P("entitlementProcess", "string", None, "Processo de entitlement associado."), P("isPerIncident", "boolean", None, "Se cobre um número limitado de casos."),
 P("term", "int", None, "Dias de vigência."), P("type", "string", None, "Tipo de suporte (por exemplo, web ou telefone)."), FN()], curinga=True)
acw = "C:obrigatório quando hasAcwExtensionEnabled é true"
MT("PresenceUserConfig", "Define uma configuração de presença do Omni-Channel.", "Definir capacidade e comportamento dos atendentes, por perfil ou usuário.", "44.0", [
 P("acwExtensionDuration", "int", None, "Segundos de cada extensão pós-conversa (10 a 3600).", acw),
 P("afterConvoWorkMaxTime", "int", None, "Segundos máximos de trabalho pós-conversa (10 a 3600).", "C:obrigatório quando hasAfterConvoWorkTimer é true"),
 P("assignments", "PresenceConfigAssignments", None, "Perfis e usuários que recebem a configuração.", estrutura="PresenceConfigAssignments"),
 P("capacity", "int", None, "Máximo de unidades de trabalho simultâneas.", "S"), P("declineReasons", "string", None, "Motivos de recusa disponíveis."),
 P("enableAutoAccept", "boolean", None, "Aceita trabalho automaticamente (só com enableDecline false)."), P("enableDecline", "boolean", None, "Permite recusar trabalho (só com enableAutoAccept false)."),
 P("enableDeclineReason", "boolean", None, "Permite escolher motivo ao recusar."), P("enableDisconnectSound", "boolean", None, "Toca som ao desconectar."),
 P("enableRequestSound", "boolean", None, "Toca som para trabalho novo.", default=DT), P("hasAcwExtensionEnabled", "boolean", None, "Permite estender o pós-conversa.", default=DF),
 P("hasAfterConvoWorkTimer", "boolean", None, "Ativa o tempo de pós-conversa.", default=DF), P("interruptibleCapacity", "int", "57.0", "Máximo de trabalho interrompível; vazio usa capacity."),
 P("label", "string", None, "Rótulo da configuração."), P("maxExtensions", "string", None, "Número máximo de extensões (1 a 10).", acw),
 P("presenceStatusOnDecline", "string", None, "Status aplicado ao recusar."), P("presenceStatusOnPushTimeout", "string", None, "Status aplicado quando o envio expira."), FN()],
 curinga=True, completa=False, cobertura_nota="A tabela da página tem uma linha vazia; universo esperado não comprovado.", alertas=["Requer Omni-Channel habilitado."])
MT("LeadConvertSettings", "Define as configurações de conversão de leads, incluindo o mapeamento de campos customizados.", "Implantar como campos de lead viram campos de conta, contato e oportunidade.", "39.0", [
 P("allowOwnerChange", "boolean", None, "Mostra o campo de dono na conversão."),
 P("objectMapping", "ObjectMapping[]", None, "Mapeamentos de campos customizados (até três: conta, contato e oportunidade).", estrutura="ObjectMapping"),
 P("opportunityCreationOptions", "VisibleOrRequired", None, "Se o campo de oportunidade aparece ou é obrigatório na conversão.",
   vals=[("VisibleOptional", "padrão"), ("VisibleRequired", None), ("NotVisible", None)])], curinga=True)

# *Settings
MT("EntitlementSettings", "Configurações de entitlements da org.", "Ligar entitlements, versionamento, milestones e filtros de busca em casos.", "27.0", [
 P("assetLookupLimitedToActiveEntitlementsOnAccount", "boolean", None, "Limita a busca de ativos aos com entitlements ativos da conta."),
 P("assetLookupLimitedToActiveEntitlementsOnContact", "boolean", None, "Limita a busca de ativos aos com entitlements ativos do contato."),
 P("assetLookupLimitedToSameAccount", "boolean", None, "Limita a busca de ativos à conta do caso."), P("assetLookupLimitedToSameContact", "boolean", None, "Limita a busca de ativos ao contato do caso."),
 P("enableEntitlements", "boolean", None, "Liga ou desliga entitlements."), P("enableEntitlementVersioning", "boolean", "28.0", "Liga o versionamento de processos."),
 P("enableMilestoneFeedItem", "boolean", "47.0", "Publica no feed quando um milestone é concluído ou violado."),
 P("enableMilestoneStoppedTime", "boolean", "47.0", "Mostra tempo parado e tempo real decorrido nos milestones."),
 P("entitlementLookupLimitedToActiveStatus", "boolean", None, "Limita a busca de entitlements aos ativos."),
 P("entitlementLookupLimitedToSameAccount", "boolean", None, "Limita a busca de entitlements à conta do caso."),
 P("entitlementLookupLimitedToSameAsset", "boolean", None, "Limita a busca de entitlements ao ativo do caso."),
 P("entitlementLookupLimitedToSameContact", "boolean", None, "Limita a busca de entitlements ao contato do caso."),
 P("ignoreMilestoneBusinessHours", "boolean", "47.0", "Mostra o tempo restante em horas reais, não comerciais.")], curinga=NOCUR, alertas=[ALERTA_SET],
 divergencias=["O relatório de pesquisa de 2026-11-08 citou 19 propriedades (incluindo enableAgenticMilestones, enableMilestonePurgeEnabled, enableOverdueMilestoneIgnoreBh, enablePauseMilestone, enableSimplifiedSLASetup e enableTimeToNextMilestone); a página 68.0 relida tem 13."])
MT("AccountSettings", "Configurações de contas e contatos da org.", "Ligar equipes de conta, histórico e outros recursos de contas.", "29.0", [
 P("enableAccountDiscovery", "boolean", "57.0", "Liga painéis do Einstein Account Management (Revenue Intelligence, custo extra)."),
 P("enableAccountHistoryTracking", "boolean", "47.0", "Rastreia histórico de contas.", default=DF),
 P("enableAccountInsightsInMobile", "boolean", "47.0", "Recurso descontinuado (Einstein Account Insights no mobile).", ate="58.0"),
 P("enableAccountOwnerReport", "boolean", None, "Permite a todos rodar o relatório Account Owner."),
 P("enableAccountTeams", "boolean", None, "Liga equipes de conta; a Metadata API não desliga."), P("enableContactHistoryTracking", "boolean", "46.0", "Rastreia histórico de contatos."),
 P("enableRelateContactToMultipleAccounts", "boolean", "47.0", "Permite um contato em várias contas.", default=DF),
 P("enableReportsToOnPersonAccount", "boolean", "62.0", "Liga o campo Reports To em contas pessoais."),
 P("showViewHierarchyLink", "boolean", None, "Mostra o link View Hierarchy em contas.")], curinga=NOCUR, alertas=[ALERTA_SET])
MT("OpportunitySettings", "Configurações de oportunidades da org.", "Ligar equipes de oportunidade, Pipeline Inspection, lembretes e outros recursos.", "28.0", [
 P("autoActivateNewReminders", "boolean", None, "Ativa atualizações agendadas para novas oportunidades."),
 P("customizableProductSchedulesEnabled", "boolean", "46.0", "Permite customizar cronogramas de produtos."),
 P("doesEnforceStandardOpportunitySaveLogic", "boolean", "47.0", "Aplica validações e gatilhos padrão em produtos e cronogramas; não pode ser false.", default=DT),
 P("enableExpandedPipelineInspectionSetup", "(em branco na fonte)", "52.0", "Mostra a página completa de configuração do Pipeline Inspection.", default=DF),
 P("enableFindSimilarOpportunities", "boolean", None, "Mostra oportunidades semelhantes."), P("enableForecastCategoryMetrics", "boolean", "57.0", "Mostra métricas por categoria de previsão.", default=DT),
 P("enableOpportunityFieldHistoryTracking", "boolean", "47.0", "Rastreia histórico de campos.", default=DT),
 P("enableOpportunityInsightsInMobile", "boolean", "47.0", "Recurso descontinuado (Einstein Opportunity Insights no mobile).", ate="58.0"),
 P("enableOpportunityTeam", "boolean", None, "Liga equipes de oportunidade."), P("enablePipelineChangesMetrics", "boolean", "57.0", "Mostra mudança líquida do pipeline.", default=DT),
 P("enablePipelineInspection", "boolean", "52.0", "Liga o Pipeline Inspection.", default=DF), P("enablePipelineInspectionFlow", "boolean", "54.0", "Liga o fluxograma do Pipeline Inspection (Revenue Insights)."),
 P("enablePipelineInspectionSingleCategoryRollup", "boolean", "55.0", "Mostra métricas por categoria única ou acumulada.", default=DF),
 P("enableRevenueInsights", "boolean", "54.0", "Configura painéis do Revenue Insights (custo extra)."), P("enableServiceCaseInsights", "boolean", "55.0", "Insights de casos no Pipeline Inspection.", default=DF),
 P("enableUpdateReminders", "boolean", None, "Permite atualizações agendadas de oportunidades."),
 P("findSimilarOppFilter", "FindSimilarOppFilter", None, "Parâmetros de oportunidades semelhantes.", estrutura="FindSimilarOppFilter"),
 P("oppAmountDealMotionEnabled", "boolean", "50.0", "Destaca mudanças de valor.", default=DT), P("oppCloseDateDealMotionEnabled", "boolean", "50.0", "Destaca mudanças de data de fechamento.", default=DT),
 P("promptToAddProducts", "boolean", None, "Sugere adicionar produtos."), P("pushCountEnabled", "boolean", "56.0", "Mostra o campo Push Count.", default=DT),
 P("simpleOppCreateFromContact", "boolean", "54.0", "Cria oportunidade pré-preenchida a partir de contato."),
 P("simpleOppCreateFromEvent", "boolean", "54.0", "Cria oportunidade pré-preenchida a partir de evento.")], curinga=NOCUR,
 alertas=[ALERTA_SET, "A página na documentação se chama meta_opportunityssettings.htm (com 's' a mais)."])
MT("QuoteSettings", "Configurações de cotações da org.", "Ligar cotações e cotações sem oportunidade.", "28.0", [
 P("enableQuote", "boolean", None, "Libera cotações aos usuários."),
 P("enableQuotesWithoutOppEnabled", "boolean", "47.0", "Permite cotações sem oportunidade; antes de desligar, exclua as cotações sem oportunidade.", default=DF)], curinga=NOCUR,
 alertas=[ALERTA_SET, "A página na documentação se chama meta_quotessettings.htm (com 's' a mais)."])
MT("BusinessHoursSettings", "Configurações de horários comerciais e feriados.", "Implantar horários comerciais e feriados da org.", "29.0", [
 P("businessHours", "BusinessHoursEntry[]", None, "Horários comerciais (entitlements, modelos, campanhas e casos).", estrutura="BusinessHoursEntry"),
 P("holidays", "Holidays[]", None, "Feriados e como afetam os horários.", estrutura="Holidays"), FN()], curinga=NOCUR,
 alertas=[ALERTA_SET], divergencias=["O exemplo da página usa businesshours.settings em minúsculas; o texto indica businessHours.settings."])
MT("OmniChannelSettings", "Configurações do Omni-Channel da org.", "Ligar o Omni-Channel e seus modos de roteamento e capacidade.", "44.0", [
 P("enableOmniAutoLoginPrompt", "boolean", "47.0", "Pede confirmação de login ao abrir o console.", default=DF),
 P("enableOmniChannel", "boolean", None, "Liga o Omni-Channel.", default=DF), P("enableOmniSecondaryRoutingPriority", "boolean", "47.0", "Liga a prioridade secundária de roteamento.", default=DF),
 P("enableOmniSkillsRouting", "boolean", None, "Liga o roteamento por habilidades.", default=DF),
 P("enableOmniStatusCapModel", "boolean", None, "Liga o modelo de capacidade por status.", default=DF), FN()], curinga=NOCUR, alertas=[ALERTA_SET])
MT("CampaignSettings", "Configurações de campanhas da org.", "Ligar influência de campanhas, contas como membros e recursos Einstein.", "48.0", [
 P("aiAttributionTimeframe", "int", "49.0", "Meses analisados na atribuição por IA (múltiplo de 3, até 24)."),
 P("enableAIAttribution", "boolean", "49.0", "Liga o Einstein Attribution.", default=DF), P("enableAccountsAsCM", "boolean", "51.0", "Permite contas como membros de campanha.", default=DF),
 P("enableAutoCampInfluenceDisabled", "boolean", None, "Desliga a criação automática de influência (exige enableCampaignInfluence2 false).", default=DF),
 P("enableB2bmaCampaignInfluence2", "boolean", None, "Usa modelos de influência de outros sistemas (exige enableCampaignInfluence2 true).", default=DF),
 P("enableCampaignHistoryTrackEnabled", "boolean", None, "Reservado ao sistema (somente leitura)."),
 P("enableCampaignInfluence2", "boolean", None, "Liga a influência customizável de campanhas.", default=DT),
 P("enableCampaignMemberTWCF", "boolean", None, "Reservado ao sistema (somente leitura)."), P("enableEKAI", "boolean", "53.0", "Liga o Einstein Key Accounts Identification.", default=DF),
 P("enableOpportunityInfluence", "(em branco na fonte)", "63.0", "Liga receita de oportunidade a campanhas (Marketing Cloud Growth/Advanced).", default=DF),
 P("enableSuppressNoValueCI2", "boolean", None, "Reservado ao sistema (somente leitura).")], curinga=NOCUR, alertas=[ALERTA_SET])
MT("Territory2Settings", "Configurações de Sales Territories da org.", "Ligar Sales Territories e definir acessos padrão e atribuição a oportunidades.", "32.0", [
 P("defaultAccountAccessLevel", "string", None, "Acesso padrão a contas em territórios."), P("defaultCaseAccessLevel", "string", None, "Acesso padrão a casos."),
 P("defaultContactAccessLevel", "string", None, "Acesso padrão a contatos."), P("defaultOpportunityAccessLevel", "string", None, "Acesso padrão a oportunidades."),
 P("enableTerritoryManagement2", "boolean", "47.0", "Liga Sales Territories; precisa ser true antes das demais operações.", default=DF),
 P("opportunityFilterSettings", "Territory2SettingsOpportunityFilter", "34.0", "Classe Apex de atribuição de territórios a oportunidades.", estrutura="Territory2SettingsOpportunityFilter"),
 P("showTM2EnabledBanner", "boolean", "49.0", "Mostra o aviso de sucesso na página Territory Settings."),
 P("supportedObjects", "Territory2SupportedObject[]", "57.0", "Acesso por objeto com atribuição de território.", estrutura="Territory2SupportedObject"),
 P("t2ForecastAccessLevel", "string", "49.0", "Acesso de usuários do território pai às oportunidades dos filhos.", vals=[("View", None), ("Edit", None)]),
 P("tm2BypassRealignAccInsert", "boolean", "53.0", "Pula regras de atribuição na inserção de contas."),
 P("tm2EnableUserAssignmentLog", "boolean", "57.0", "Registra a atribuição de usuários a territórios."), FN()], curinga=NOCUR, alertas=[ALERTA_SET] + SALES_T[1:2])
MT("KnowledgeSettings", "Configurações do Salesforce Knowledge da org.", "Ligar Knowledge e Lightning Knowledge, idiomas, sugestões e compartilhamento.", "27.0", [
 P("answers", "KnowledgeAnswerSettings", None, "Configurações de Knowledge com Answers."), P("cases", "KnowledgeCaseSettings", None, "Configurações de Knowledge com casos."),
 P("defaultLanguage", "string", None, "Idioma padrão do Knowledge (ex.: en_US).", "S"),
 P("enableChatterQuestionKBDeflection", "boolean", None, "Rastreia deflexão de casos no Chatter."), P("enableCreateEditOnArticlesTab", "boolean", None, "Cria e edita artigos na aba Articles."),
 P("enableExternalMediaContent", "boolean", None, "Liga conteúdo de mídia externa."), P("enableKbStandardSharing", "boolean", None, "Usa o compartilhamento padrão do Salesforce."),
 P("enableKnowledge", "boolean", None, "Liga o Knowledge.", default=DF), P("enableKnowledgeAgentContribution", "boolean", None, "Cria artigo a partir de caso (só Classic)."),
 P("enableKnowledgeArticleTextHighlights", "boolean", "47.0", "Destaca trechos nos resultados de busca.", default=DT),
 P("enableKnowledgeAnswersPromotion", "boolean", None, "Cria artigo a partir de resposta (só Classic)."), P("enableKnowledgeCaseRL", "boolean", None, "Lista de casos do artigo (só Classic)."),
 P("enableKnowledgeKeywordAutoComplete", "boolean", "47.0", "Autocompleta palavras-chave na busca.", default=DT),
 P("enableKnowledgeTitleAutoComplete", "boolean", "47.0", "Autocompleta títulos na busca.", default=DT),
 P("enableLightningKbAutoLoadRichTextField", "boolean", "47.0", "Campos rich text editáveis ao abrir artigo.", default=DF),
 P("enableLightningKnowledge", "boolean", None, "Liga o Lightning Knowledge."), P("languages", "KnowledgeLanguageSettings", None, "Idiomas habilitados."),
 P("showArticleSummariesCustomerPortal", "boolean", None, "Resumos no Customer Portal."), P("showArticleSummariesInternalApp", "boolean", None, "Resumos na base interna."),
 P("showArticleSummariesPartnerPortal", "boolean", None, "Resumos no portal de parceiros."), P("showValidationStatusField", "boolean", None, "Mostra o status de validação."),
 P("suggestedArticles", "KnowledgeSuggestedArticlesSettings", "37.0", "Campos de caso usados para sugerir artigos."),
 P("votingEnabled", "boolean", "50.0", "Liga votação.")], curinga=NOCUR, completa=True,
 cobertura_nota="Nível principal completo (23 linhas). Os 12 subtipos (33 linhas) foram lidos e estão na nota de extração, mas não foram cadastrados como estruturas nesta rodada.",
 alertas=[ALERTA_SET])
MT("ForecastingSettings", "Configurações de previsões colaborativas da org.", "Ligar previsões e definir tipos, categorias, ajustes, períodos e cotas.", "28.0", [
 P("displayCurrency", "DisplayCurrency", "28.0", "Moeda de exibição (removido; use defaultToPersonalCurrency a partir da 47.0).", ate="46.0", vals=[("CORPORATE", None), ("PERSONAL", None)]),
 P("defaultToPersonalCurrency", "boolean", "47.0", "Usa a moeda pessoal nas previsões com multimoeda.", default=DT),
 P("enableForecasts", "boolean", None, "Liga ou desliga previsões; desligar pode apagar dados."),
 P("forecastingCategoryMappings", "ForecastingCategoryMapping[]", None, "Mapeia tipos de previsão para categorias acumuladas."),
 P("forecastingDisplayedFamilySettings", "ForecastingDisplayedFamilySettings[]", "40.0", "Famílias de produto previstas no Lightning."),
 P("forecastingSubmissionSettings", "ForecastingSubmissionSettings", "62.0", "Opções de submissão de previsões."),
 P("forecastingTypeSettings", "ForecastingTypeSettings[]", None, "Tipos de previsão (máximo de quatro)."),
 P("globalAdjustmentsSettings", "AdjustmentsSettings[]", "53.0", "Opções de ajuste."), P("globalForecastRangeSettings", "ForecastRangeSettings[]", "53.0", "Períodos e intervalo padrão."),
 P("globalQuotasSettings", "QuotasSettings[]", "53.0", "Liga ou desliga cotas.")], curinga=NOCUR,
 cobertura_nota="Nível principal completo (10 linhas). Os 13 subtipos (44 linhas) foram lidos e estão na nota de extração, mas não foram cadastrados como estruturas nesta rodada.",
 alertas=[ALERTA_SET, "A estrutura do tipo mudou bastante nas versões 30.0 e 53.0."])
M.emit_structs()
# Territory2Model: FieldValue agora detalhado
t2m = ld("metadata-types/Territory2Model.json")
for p in t2m["propriedades"]:
    if p["nome"] == "customFields": p["estrutura_ref"] = "mdx:FieldValue"
t2m["estruturas"] = ["mdx:FieldValue"]
e = t2m["cobertura"]["estrutural"]; e["estado"] = "completa"; e["esperado"] = 3; e["nota"] = "Universo esperado = tabela Fields da página oficial 68.0 (3 propriedades). FieldValue detalhado a partir da página de Territory2."
t2m["evidencias"].append(ev("src:mdapi-territory2"))
sv("metadata-types/Territory2Model.json", t2m)

# ================================================================ objetos
TOOL_D = lambda: expo("tooling", "desconhecido", nota="Exposição na Tooling API não verificada.")
def mk(o, s, rows):
    out = []
    for r in rows:
        n, t, p, ver, d = r[:5]; kw = dict(r[5]) if len(r) > 5 else {}
        notas = kw.pop("notas", None); f = field("obj:" + o, n, t, p, ver, d, s, **kw)
        if notas: f["notas"] = notas
        out.append(f)
    return out
def O(nome, oq, papel, calls, rows, soql, desde, acesso=None, alertas=None, nomes=None):
    s = f"src:objref-{nome.lower()}"; campos = mk(nome, s, rows)
    if nomes:
        by = {f["nome"]: f for f in campos}; campos = []
        for n in nomes:
            if n in by: campos.append(by[n]); continue
            f = field("obj:" + nome, n, "(a extrair)", None, None, None, s); f["notas"] = ["Nome listado na Object Reference; tipo e propriedades não extraídos nesta rodada."]; campos.append(f)
    obj(nome, oq, papel, [expo("padrao", "verificado", s, calls, desde=desde, acesso=acesso), TOOL_D()], campos,
        [{"api": "padrao", "soql": soql, "contexto": "API padrão.", "validacao": "documental"}], APEX_OK(s),
        cob("completa", len(campos), len(campos), cnt(campos), f"Tabela de campos lida completa ({len(campos)})."), s, alertas=alertas)
FA = "Só usuários com View All Forecasts, Allow Forecasting ou status de gestor delegado."
O("ForecastingAdjustment", "Ajuste de um gestor sobre a previsão de um subordinado ou território filho.", "Registrar ajustes de gestores.",
  ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "update()", "upsert()"], [
 ("AdjustedAmount", "double", "CFSU", None, "Valor ajustado."), ("AdjustedQuantity", "double", "CFSU", "28.0", "Quantidade ajustada."),
 ("AdjustmentNote", "textarea", "CFGNSU", None, "Nota do ajuste."), ("CurrencyIsoCode", "picklist", "CDFGRSU", None, "Moeda."),
 ("ForecastCategoryName", "picklist", "CFGNRS", None, "Categoria das oportunidades."), ("ForecastingGroupItemId", "reference", "CFGNS", "60.0", "Item de grupo.", {"ref": ["ForecastingGroupItem"]}),
 ("ForecastingItemCategory", "picklist", "CFGS", None, "Tipo de acumulado."), ("ForecastingItemId", "reference", "FGS", None, "Item de previsão ajustado."),
 ("ForecastingTypeId", "reference", "CFGS", None, "Tipo de previsão."), ("IsAmount", "boolean", "DFGS", "28.0", "Por valor."), ("IsQuantity", "boolean", "DFGS", "28.0", "Por quantidade."),
 ("OwnerId", "reference", "CDFGS", None, "Dono do ajuste."), ("PeriodId", "reference", "FGNS", None, "Período (somente leitura)."),
 ("ProductFamily", "picklist", "CFGNS", "29.0", "Família de produto (somente leitura)."), ("StartDate", "date", "CFGS", None, "Data de início."),
 ("Territory2Id", "reference", "CFGNS", "43.0", "Território.")], "SELECT ForecastingItemId, AdjustedAmount, OwnerId FROM ForecastingAdjustment LIMIT 20", "26.0", FA,
  ["ForecastingItemCategory e ForecastCategoryName precisam ser compatíveis ao inserir."])
O("ForecastingOwnerAdjustment", "Ajuste de um usuário sobre a própria previsão.", "Registrar ajustes do próprio dono.",
  ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "update()", "upsert()"], [
 ("CurrencyIsoCode", "picklist", "CDFGNRSU", None, "Moeda."), ("ForecastCategoryName", "picklist", "CFGNRS", None, "Categoria (pode ser nula com acumulado)."),
 ("ForecastOwnerId", "reference", "CFGNS", None, "Dono da previsão."), ("ForecastingGroupItemId", "reference", "CFGNS", "60.0", "Item de grupo.", {"ref": ["ForecastingGroupItem"], "rel": "ForecastingGroupItem"}),
 ("ForecastingItemCategory", "picklist", "CFGS", None, "Tipo de acumulado."), ("ForecastingItemId", "reference", "FGS", None, "Item de previsão."),
 ("ForecastingTypeId", "reference", "CFGNS", None, "Tipo de previsão."), ("IsAmount", "boolean", "DFGS", None, "Por valor."), ("IsQuantity", "boolean", "DFGS", None, "Por quantidade."),
 ("OwnerAdjustedAmount", "currency", "CFNSU", None, "Valor ajustado pelo dono."), ("OwnerAdjustedQuantity", "double", "CFNSU", None, "Quantidade ajustada pelo dono."),
 ("OwnerAdjustmentNote", "textarea", "CFGNSU", None, "Nota do ajuste."), ("PeriodId", "reference", "FGNS", None, "Período."),
 ("ProductFamily", "picklist", "CFGNS", None, "Família de produto."), ("StartDate", "date", "CFGNS", None, "Data de início."), ("Territory2Id", "reference", "CFGNS", "43.0", "Território.")],
  "SELECT ForecastOwnerId, OwnerAdjustedAmount, PeriodId FROM ForecastingOwnerAdjustment LIMIT 20", "33.0", FA)
O("ForecastingType", "Identifica um tipo de previsão.", "Filtrar previsões, ajustes, cotas e fatos pelo tipo.",
  ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"], [
 ("CanDisplayQuotas", "boolean", "CDFGS", None, "Pode exibir cotas."), ("DateType", "picklist", "CFGRS", None, "Base de data da previsão."),
 ("DeveloperName", "string", "CFGSU", None, "Nome único (na Metadata API, 'name')."), ("ForecastingGroupID", "reference", "CFGNS", None, "Grupo de previsão.", {"ref": ["ForecastingGroup"]}),
 ("HasAdjustments", "boolean", "DFGS", None, "Tem ajustes de gestor."), ("HasOwnerAdjustments", "boolean", "DFGS", None, "Tem ajustes do dono."),
 ("HasProductFamily", "boolean", "CDG", None, "Previsão por família de produto."), ("IsActive", "boolean", "CDFGSU", None, "Ativo."), ("IsAmount", "boolean", "CDFGS", None, "Por valor."),
 ("IsPlatformType", "boolean", "DFGS", None, "Tipo da plataforma."), ("IsQuantity", "boolean", "CDFGS", None, "Por quantidade."), ("Language", "picklist", "CDFGNRSU", None, "Idioma."),
 ("LastActivatedDate", "dateTime", "CFNS", None, "Última ativação."), ("MasterLabel", "string", "CFGSU", None, "Rótulo."),
 ("OpportunitySplitTypeId", "reference", "CFGNS", None, "Tipo de divisão de oportunidade.", {"ref": ["OpportunitySplitType"]}),
 ("OpptyLineItemSplitTypeId", "reference", "CFGNS", None, "Tipo de divisão de item.", {"ref": ["OpptyLineItemSplitType"]}),
 ("RoleType", "picklist", "CFGRS", None, "Base hierárquica: papel (R), Territory1 (T, sem uso) ou Territory2 (Y).", {"vals": ["R", "T", "Y"], "contexto": "Valores conforme a página."}),
 ("Territory2ModelId", "reference", "CFGNS", None, "Modelo de territórios.")], "SELECT DeveloperName, MasterLabel, IsActive FROM ForecastingType", "30.0", FA)
O("ForecastingFact", "Liga um item de previsão às oportunidades que o compõem.", "Rastrear quais oportunidades formam cada valor previsto (somente leitura).",
  ["describeSObjects()", "query()", "retrieve()"], [
 ("ForecastCategoryName", "picklist", "FGRS", None, "Categoria."), ("ForecastedObjectId", "reference", "FGNS", "29.0", "Objeto previsto (somente leitura)."),
 ("ForecastedSubObjectId", "reference", "FGNS", "58.0", "Item de oportunidade ou divisão de item.", {"ref": ["obj:OpportunityLineItem", "OpportunityLineItemSplit"]}),
 ("ForecastingItemId", "reference", "FGNS", None, "Item de previsão."), ("ForecastingTypeId", "reference", "FGNS", None, "Tipo de previsão."),
 ("OpportunityId", "reference", "FGS", None, "Oportunidade."), ("OwnerId", "reference", "FGS", None, "Dono."), ("PeriodId", "reference", "FGNS", None, "Período."),
 ("TargetValue", "double", "FNS", None, "Valor-alvo."), ("Territory2Id", "reference", "FGNS", "43.0", "Território.")],
  "SELECT ForecastingItemId, OpportunityId, ForecastCategoryName FROM ForecastingFact LIMIT 20", "26.0", FA)
O("ForecastingQuota", "Cota de receita ou quantidade de um usuário ou território num período.", "Registrar metas usadas nas previsões.",
  ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "update()", "upsert()"], [
 ("CurrencyIsoCode", "picklist", "CDFGRSU", None, "Moeda."), ("ForecastingGroupItemId", "reference", "CFGNS", "60.0", "Item de grupo.", {"ref": ["ForecastingGroupItem"]}),
 ("ForecastingTypeId", "reference", "CFGS", None, "Tipo de previsão."), ("IsAmount", "boolean", "DFGS", "28.0", "Por valor."), ("IsQuantity", "boolean", "DFGS", "28.0", "Por quantidade."),
 ("PeriodId", "reference", "FGNS", None, "Período (somente leitura)."), ("ProductFamily", "picklist", "CFGNS", "29.0", "Família de produto."),
 ("QuotaAmount", "currency", "CFSU", None, "Valor da cota."), ("QuotaOwnerId", "reference", "CDFGSU", None, "Dono da cota."),
 ("QuotaQuantity", "double", "CFSU", "28.0", "Quantidade da cota."), ("StartDate", "date", "CFGSU", None, "Data de início."), ("Territory2Id", "reference", "CFGNS", "43.0", "Território.")],
  "SELECT QuotaOwnerId, QuotaAmount, StartDate FROM ForecastingQuota LIMIT 20", "25.0", FA,
  ["Criar, alterar ou excluir cotas exige Manage Quotas; não é possível editar a própria cota.", "A tabela termina com uma linha vazia, que não é campo."])
nomes_psr = ("BotId, BotType, CapacityPercentage, CapacityWeight, CustomRequestedDateTime, DropAdditionalSkillsTimeout, ExternalBotId, GroupId, IsInterruptible, IsOwnerChangeInitiated, "
 "IsPreferredUserRequired, IsPushAttempted, IsPushed, IsReadyForRouting, IsStatusChangeInitiated, IsTransfer, LastDeclinedAgentSession, Name, OwnerId, PausedCapacityPercentage, "
 "PausedCapacityWeight, PreferredUserId, PushTimeout, QueueId, RoutingModel, RoutingPriority, RoutingType, SecondaryRoutingPriority, Serial, ServiceChannelId, TargetAcceptDateTime, "
 "TransferRequesterId, WorkItemId").split(", ")
O("PendingServiceRouting", "Representa um trabalho aguardando roteamento no Omni-Channel.", "Controlar o roteamento por fila ou por habilidades antes da atribuição.",
  ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "undelete()", "update()", "upsert()"], [
 ("WorkItemId", "reference", "CFGS", None, "Registro a ser roteado.", {"ref": ["obj:Account", "obj:Case", "obj:Lead", "obj:Opportunity", "WorkOrder"],
   "notas": ["A página lista mais alvos (inclusive objetos customizados); aqui só alguns."]}),
 ("ServiceChannelId", "reference", "CFGS", None, "Canal de serviço."), ("QueueId", "reference", "FGNS", None, "Fila do Omni-Channel (a página recomenda GroupId)."),
 ("RoutingType", "picklist", "CDFGNRS", None, "Roteamento por fila ou por habilidades.", {"vals": ["QueueBased", "SkillsBased"], "contexto": "Valores conforme a página."}),
 ("IsReadyForRouting", "boolean", "CDFGSU", None, "Pronto para roteamento; quando true, o registro não pode ser editado.")],
  "SELECT WorkItemId, RoutingType, IsReadyForRouting FROM PendingServiceRouting LIMIT 20", "40.0", "Requer Omni-Channel habilitado.",
  ["No roteamento por fila, não dispara triggers de before/after insert.", "Não defina PushTimeout quando IsPreferredUserRequired for true."], nomes=nomes_psr)
O("ServicePresenceStatus", "Representa um status de presença que pode ser associado a canais de serviço.", "Consultar e criar os status de presença dos atendentes.",
  ["create()", "query()", "update()", "retrieve()"], [("DeveloperName", "string", "CFGS", None, "Nome único."), ("Language", "picklist", "CFGNRS", None, "Idioma."),
 ("MasterLabel", "string", "CFGS", None, "Rótulo.")], "SELECT DeveloperName, MasterLabel FROM ServicePresenceStatus", "32.0", "Requer Omni-Channel habilitado; só usuários autenticados.")
O("PresenceUserConfig", "Representa uma configuração de presença do Omni-Channel.", "Consultar capacidade e opções dos atendentes.",
  ["create()", "delete()", "describeSObjects()", "update()", "query()", "retrieve()"], [
 ("AcwExtensionDuration", "int", "CFGNSU", "56.0", "Duração de cada extensão pós-conversa."), ("AfterConvoWorkMaxTime", "int", "CFGNSU", "56.0", "Tempo máximo pós-conversa."),
 ("Capacity", "int", "CFGS", None, "Capacidade."), ("CustomSoundId", "reference", "CFGNSU", None, "Som customizado.", {"ref": ["StaticResource"], "rel": "CustomSound"}),
 ("DeveloperName", "string", "CFGS", None, "Nome único."), ("HasAcwExtensionEnabled", "boolean", "CDFGSU", "56.0", "Permite estender o pós-conversa."),
 ("HasAfterConvoWorkTimer", "boolean", "CDFGSU", "56.0", "Ativa o tempo de pós-conversa."), ("Language", "picklist", "CFGNRS", None, "Idioma."),
 ("MasterLabel", "string", "CFGS", None, "Rótulo."), ("MaxExtensions", "picklist", "CFGNRSU", "56.0", "Máximo de extensões."),
 ("OptionsIsAllowAnyDestinationQueueForTransferEnabled", "boolean", "CFU", "61.0", "Permite transferir para qualquer fila."),
 ("OptionsIsAllowAnyDestinationFlowForTransferEnabled", "boolean", "CFU", "61.0", "Permite transferir para qualquer flow."),
 ("OptionsIsAllowAnyDestinationProfileForTransferEnabled", "boolean", "CFU", "61.0", "Permite transferir para qualquer perfil."),
 ("OptionsIsAutoAcceptEnabled", "boolean", "CF", None, "Aceite automático (só sem recusa)."), ("OptionsIsDeclineEnabled", "boolean", "CF", None, "Permite recusar (só sem aceite automático)."),
 ("OptionsIsDeclineReasonEnabled", "boolean", "CF", None, "Permite motivo de recusa."), ("OptionsIsDisconnectSoundEnabled", "boolean", "CF", None, "Som ao desconectar."),
 ("OptionsIsRequestSoundEnabled", "boolean", "CF", None, "Som para trabalho novo."), ("PresenceStatusOnDeclineId", "reference", "CFGNS", None, "Status aplicado ao recusar."),
 ("PresenceStatusOnPushTimeoutId", "reference", "CFGNS", "36.0", "Status aplicado quando o envio expira."), ("SoundLength", "int", "CFGNSU", None, "Duração do som.")],
  "SELECT DeveloperName, Capacity FROM PresenceUserConfig", "32.0", "Requer Omni-Channel habilitado; só usuários autenticados.")
O("KnowledgeArticle", "Representa um artigo de conhecimento, independente da versão.", "Consultar artigos (o Id não muda entre versões).",
  ["describeSObjects()", "query()", "retrieve()"], [
 ("ArchivedById", "reference", "FGNS", None, "Quem arquivou."), ("ArchivedDate", "dateTime", "FNS", None, "Data de arquivamento."),
 ("ArticleNumber", "string", "DFIS", None, "Número do artigo (autonumeração).", {"notas": ["A página também marca a propriedade Autonumber."]}),
 ("CaseAssociationCount", "int", "FGS", None, "Casos associados."), ("FirstPublishedDate", "dateTime", "FNS", None, "Primeira publicação."),
 ("IsGeneratedByLlm", "boolean", "DFGS", None, "Gerado por modelo de linguagem."), ("LastPublishedDate", "dateTime", "FNS", None, "Última publicação."),
 ("LastReferencedDate", "dateTime", "FNS", None, "Última referência."), ("LastViewedDate", "dateTime", "FNS", None, "Última visualização."),
 ("MasterLanguage", "picklist", "FGRS", None, "Idioma principal."), ("MigratedToFromArticle", "string", "FGNS", None, "Artigo migrado de/para."),
 ("TotalViewCount", "int", "FGNS", None, "Total de visualizações.")], "SELECT ArticleNumber, MasterLanguage, LastPublishedDate FROM KnowledgeArticle LIMIT 20", "19.0",
  "Exige Knowledge habilitado e View Articles; usuários de Knowledge precisam da feature license Knowledge User.",
  ["Somente leitura, exceto a exclusão do artigo principal."])
# alvos agora catalogados
for o, m in {"AgentWork": {"PendingServiceRoutingId": ["obj:PendingServiceRouting"]}, "KnowledgeArticleVersion": {"KnowledgeArticleId": ["obj:KnowledgeArticle"]}}.items():
    d = ld(f"objetos-api/{o}.json")
    for c in d["campos"]:
        if c["nome"] in m: c["referencia"]["alvos"] = m[c["nome"]]
    sv(f"objetos-api/{o}.json", d)

# ================================================================ relacionamentos
N1 = lambda: af("desconhecido", "N:1", "Estrutura de lookup indica N:1; não comprovado nesta sessão.")
for rid, oo, campo, dd, expl, s, cond in [
 ("forecastingfact-opportunitylineitem", "ForecastingFact", "ForecastedSubObjectId", "OpportunityLineItem", "O fato pode apontar para o item de oportunidade previsto.", "src:objref-forecastingfact", "Quando o subobjeto é um item de oportunidade."),
 ("pendingservicerouting-case", "PendingServiceRouting", "WorkItemId", "Case", "O trabalho a rotear pode ser um caso.", "src:objref-pendingservicerouting", "Quando o item é um caso."),
 ("agentwork-pendingservicerouting", "AgentWork", "PendingServiceRoutingId", "PendingServiceRouting", "O trabalho atribuído nasce de um roteamento pendente.", "src:objref-agentwork", None),
 ("knowledgearticleversion-knowledgearticle", "KnowledgeArticleVersion", "KnowledgeArticleId", "KnowledgeArticle", "Cada versão pertence a um artigo.", "src:objref-knowledgearticleversion", None)]:
    rel(rid, "referencia_campo", {"entidade": "obj:" + oo, "campo": campo}, {"entidade": "obj:" + dd}, expl, "verificado", [s], N1(), cond=cond)
for a, t in [("Territory2", "territórios"), ("Territory2Type", "tipos de território"), ("MilestoneType", "tipos de milestone"),
             ("PresenceUserConfig", "configurações de presença"), ("ServicePresenceStatus", "status de presença")]:
    rel(f"rep-{a.lower()}", "representacao_comum", {"entidade": f"mdt:{a}"}, {"entidade": f"obj:{a}"},
        f"Metadata type e objeto API descrevem {t} por caminhos diferentes: definição implantável versus registro consultável. A correspondência campo a campo não foi comprovada.",
        "verificado", [f"src:mdapi-{a.lower()}", f"src:objref-{a.lower()}"])

# ================================================================ funcionalidades
def upd(fid, objs=(), mdts=(), ausencias=None, ev_add=(), limit=None, setup=None):
    f = ld(f"funcionalidades/{fid}.json"); r = f["representacoes"]
    have = {x["ref"] for x in r["objetos_api"] + r["metadata_types"]}
    r["objetos_api"] += [{"ref": "obj:" + o, "papel": p} for o, p in objs if "obj:" + o not in have]
    r["metadata_types"] += [{"ref": "mdt:" + m, "papel": p} for m, p in mdts if "mdt:" + m not in have]
    if ausencias is not None: r["ausencias"] = ausencias
    for s in ev_add:
        if not any(e["fonte"] == s for e in f["evidencias"]): f["evidencias"].append(ev(s))
    if limit is not None: f["limitacoes"] = limit
    if setup: f["setup"] = setup
    sv(f"funcionalidades/{fid}.json", f)
CFG = "Configurações da org (Settings)."
upd("previsoes-colaborativas", [("ForecastingAdjustment", "Ajuste de gestor."), ("ForecastingOwnerAdjustment", "Ajuste do próprio dono."), ("ForecastingType", "Tipo de previsão."),
    ("ForecastingFact", "Ligação entre previsão e oportunidades."), ("ForecastingQuota", "Cota por período.")], [("ForecastingSettings", CFG)], [],
    ["src:objref-forecastingadjustment", "src:objref-forecastingowneradjustment", "src:objref-forecastingtype", "src:objref-forecastingfact", "src:objref-forecastingquota", "src:mdapi-forecastingsettings"])
upd("territorios-de-vendas", mdts=[("Territory2", "Território implantável."), ("Territory2Rule", "Regra de atribuição implantável."), ("Territory2Type", "Tipo de território implantável."),
    ("Territory2Settings", CFG)], ev_add=["src:mdapi-territory2", "src:mdapi-territory2rule", "src:mdapi-territory2type", "src:mdapi-territory2settings"], limit=[])
upd("omni-channel", [("PendingServiceRouting", "Trabalho aguardando roteamento."), ("ServicePresenceStatus", "Status de presença consultável."), ("PresenceUserConfig", "Configuração de presença consultável.")],
    [("PresenceUserConfig", "Configuração de presença implantável."), ("OmniChannelSettings", CFG)], [],
    ["src:objref-pendingservicerouting", "src:objref-servicepresencestatus", "src:objref-presenceuserconfig", "src:mdapi-presenceuserconfig", "src:mdapi-omnichannelsettings"])
upd("lightning-knowledge", [("KnowledgeArticle", "Artigo, independente da versão.")], [("KnowledgeSettings", CFG)],
    [{"tipo": "objeto_api", "estado": "desconhecido", "motivo": "Knowledge__kav não tem página própria lida; a página de KnowledgeArticleVersion informa que Knowledge__kav deriva dela."}],
    ["src:objref-knowledgearticle", "src:mdapi-knowledgesettings"])
upd("entitlements-e-milestones", mdts=[("EntitlementSettings", CFG), ("EntitlementTemplate", "Modelo de entitlement implantável."), ("MilestoneType", "Tipo de milestone implantável.")],
    ausencias=[], ev_add=["src:mdapi-entitlementsettings", "src:mdapi-entitlementtemplate", "src:mdapi-milestonetype"])
upd("contas", mdts=[("AccountSettings", CFG)], ausencias=[], ev_add=["src:mdapi-accountsettings"])
upd("campanhas", mdts=[("CampaignSettings", CFG)], ausencias=[], ev_add=["src:mdapi-campaignsettings"])
upd("cotacoes", mdts=[("QuoteSettings", CFG)], ausencias=[], ev_add=["src:mdapi-quotesettings"])
upd("oportunidades", mdts=[("OpportunitySettings", CFG)], ausencias=[], ev_add=["src:mdapi-opportunitysettings"])
upd("leads", mdts=[("LeadConvertSettings", "Configurações de conversão e mapeamento de campos.")], ausencias=[], ev_add=["src:mdapi-leadconvertsettings"],
    limit=["Regras de atribuição em func:regras-de-atribuicao."])
upd("horario-comercial", mdts=[("BusinessHoursSettings", "Horários comerciais e feriados implantáveis.")], ausencias=[], ev_add=["src:mdapi-businesshourssettings"])
upd("equipes-de-conta-e-oportunidade", mdts=[("AccountSettings", "enableAccountTeams liga equipes de conta."), ("OpportunitySettings", "enableOpportunityTeam liga equipes de oportunidade.")],
    ausencias=[], ev_add=["src:mdapi-accountsettings", "src:mdapi-opportunitysettings"])
upd("regras-de-atribuicao", ev_add=["src:help-escalation-setup"], limit=[],
    setup=af("verificado", "Setup > Quick Find: Assignment Rules > Lead Assignment Rules | Case Assignment Rules; Setup > Quick Find: Escalation Rules > Escalation Rules",
             "Escalation Rules: Customize Application; uma regra ativa por vez; até cinco ações por entrada.", [ev("src:help-assign-guide"), ev("src:help-escalation-setup")]))

# ================================================================ nuvens
for n, txt in [("sales-cloud", "Subtipos de ForecastingSettings não cadastrados como estruturas (estão na nota de extração)."),
               ("service-cloud", "Knowledge__kav sem página própria lida; subtipos de KnowledgeSettings não cadastrados como estruturas (estão na nota de extração).")]:
    d = ld(f"nuvens/{n}.json"); d["limites"][0] = txt; sv(f"nuvens/{n}.json", d)
print("ok")
