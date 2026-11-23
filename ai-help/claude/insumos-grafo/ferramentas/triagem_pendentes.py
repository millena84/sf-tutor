"""Triagem semântica dos metadata types pendentes de recorte Core (#10): família provável e classificação funcional provável.

O QUE É: uma triagem feita SÓ PELO NOME de cada tipo, com regras de padrão (prefixos, sufixos e nomes conhecidos) escritas à mão
em 2026-11-23, na conversa com a autora. Tudo aqui é INFERIDO. Não é decisão de recorte, não entra no catálogo nem no mapa, e não
substitui a fonte por família exigida para decidir (config/escopo.json). Serve para ordenar os lotes da etapa 2 por família e,
depois, sugerir onde cada tipo pode entrar na classificação funcional quando for cadastrado.

Confiança: alta = nome inequívoco; media = família clara pelo nome, subclassificação escolhida pelo projeto; baixa = nome vago ou sem
subclassificação adequada. Um tipo que nenhuma regra pega fica como "sem pista".

Não altera o catálogo. Grava relatorios/triagem-pendentes.json e relatorios/triagem-pendentes.md.
Uso: python3 ferramentas/triagem_pendentes.py   (rode de novo depois de cada lote de decisões: só os pendentes atuais entram)
"""
import collections
import json
import os
import re

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INV = os.path.join(RAIZ, "inventarios", "metadata-types-v68.json")
SAIDA_JSON = os.path.join(RAIZ, "relatorios", "triagem-pendentes.json")
SAIDA_MD = os.path.join(RAIZ, "relatorios", "triagem-pendentes.md")
DATA_REGRAS = "2026-11-23"

# ----------------------------------------------------------------- classificação funcional (ids sem o prefixo cls:/sub:)
A='acesso-identidade-e-seguranca'
AU='automacao-de-processos-e-regras-de-negocio'
C='conteudo-conhecimento-e-colaboracao'
D='dados-e-modelagem'
DV='desenvolvimento-testes-e-entrega'
EX='execucao-assincrona-lotes-e-agendamento'
IA='ia-agentes-e-decisoes-assistidas'
I='integracao-apis-e-eventos'
UI='interface-e-experiencia-do-usuario'
O='observabilidade-auditoria-e-operacao'
OR='organizacao-e-configuracoes-base'
P='processos-de-negocio-especificos-de-produto'
Q='qualidade-governanca-e-ciclo-de-vida-dos-dados'
R='relatorios-analytics-e-exploracao'

REGRAS_FUNCIONAIS = [
# legado
(AU,'mecanismos-legados-e-migracao','alta',r'^(WorkflowSend|ProcessFlowMigration|PlatformEventMigration)$'),
# IA
(IA,'seguranca-avaliacao-e-governanca-de-ia','media',r'^(AiTestingDefinition|AiAgentScorerDefinition|AgentforceSessionTracing|Explainability|SceGlobalModelOptOut|AnalyticsLlmOverride)'),
(IA,'prompts','media',r'^(Prompt$|GenComputingSummaryDef|EinsteinGPTSalesEmails|SalesEmailAssistant|GenerativeCampaigns|KnowledgeGeneration)'),
(IA,'recuperacao-de-conhecimento','media',r'^(RetrievalSummaryDefinition|AgenticCtxtDecorDefinition)'),
(IA,'modelos-e-grounding','media',r'^(AIScoringModel|ExternalAIModel|MlDomain|DiscoveryAIModel|PredictionBuilder|AIUsecase|AffinityScore|CustomizablePropensity|AnlytAgntFlbkSmntcModel|WinProbabilityScoring|OpportunityScore|DCOpportunityScoring|LeadScore|Ai4m)'),
(IA,'acoes-e-topicos','media',r'^(AssistantSkill|AssistantContextItem|RecommendationStrategy|RecommendationBuilder|AIReplyRecommendations|ServiceAIRecommendations)'),
(IA,'configuracao-de-agentes','media',r'^(AI|Ai|Agent|Agentforce|Einstein|GenOp|Assistant|ExternalAiAgent|SetupCopilot|SecurityAgent|PrivacyAgent|MediaAgent|SalesDealAgent|SalesBots|ServiceRepAssistant|ServiceAISetup|AnalyticsAgent|McpServerDefinition|BotEmail)'),
# Analytics
(R,'dashboards','media',r'^(AnalyticsDashboard|ReferencedDashboard|CollectionsDashboardSettings)'),
(R,'reports','media',r'^(AnalyticSnapshot|MapReportSettings)'),
(R,'recursos-analiticos-de-produto','media',r'^(Analytics|Wave|Discovery|Disco|AppAnalytics|StatisticalDealInsights|PipelineInsp|UnifiedSalesIntelligence|AccountIntelligence|CustomerIntelligence|ConvIntelligence|ConversationalIntelligence|BusinessValueMetrics)'),
# Acesso
(A,'sessoes-e-politicas-de-login','alta',r'^(ProfilePasswordPolicy|ProfileSessionSetting|IPAddressRange|MyDomainDiscoverableLogin|MobileSecurity|MobSecurity|TransactionSecurityPolicy|RedirectWhitelistUrl|MailAppOwaWhitelist|BlacklistedConsumer)'),
(A,'autenticacao-sso-e-mfa','media',r'^(IdpConfiguration|ExtlClntApp)'),
(A,'usuarios-e-provisionamento','media',r'^(UserProvisioningConfig|UserAccessPolicy|UserCriteria|EmployeeUserSettings|EmployeeDataSync)'),
(A,'licencas-e-entitlements-de-acesso','media',r'^(PermissionSetLicenseDefinition|LicensingSettings)'),
(A,'acesso-a-registros-e-hierarquias','alta',r'^(RestrictionRule|ScopedAccess|AccountRelationshipShareRule|SharingSet|DelegateAccess|DelegateAccs|RelatedRecordAccessDef|PersonAccountOwnerPowerUser|PaymentsSharing|FieldRestrictionRule|EmployeeFieldAccess)'),
(A,'permissoes-perfis-e-grupos','alta',r'^(CustomPermission|MutingPermissionSet|DelegateGroup|PortalDelegablePermissionSet)'),
(A,'credenciais-certificados-e-protecao-de-dados','media',r'^(Security|TenantSecurity|DataMask)'),
# Qualidade/governanca
(Q,'consentimento-e-privacidade','alta',r'^(Consent|GlobalConsent|DsarPolicy|PrivacyOrgConfig)'),
(Q,'classificacao-e-sensibilidade','media',r'^(SensitiveDataRule)'),
(Q,'duplicidade-e-correspondencia','media',r'^(IdentityRsol|CleanDataService|DataDotCom)'),
# Dados
(D,'listas-de-valores','alta',r'^(GlobalValueSet|StandardValue|CustomValue|ChoiceList)'),
(D,'campos-e-tipos','media',r'^(CustomIndex|CustomFieldDisplay|FormulaSettings)'),
(D,'relacionamentos-e-juncoes','media',r'^(ObjectHierarchyRelationship|RelationshipGraphDefinition|FieldSrcTrgtRelationship|ObjectLinkingSettings|ChannelObjectLinkingRule)'),
(D,'metadados-de-configuracao-de-dados','media',r'^(ObjectMappingSettings|ObjectFieldValueMapping|ObjectSourceTargetMap|FieldMappingConfig|ExtDataTranFieldTemplate|RecordAggregationDefinition|DataCategoryGroup|PartyDataModel|PartyProfile|OnboardingDataObjectGroup|CustomObjectBinding|ContextDefinition|ContextMapping|ContextUseCase)'),
(D,'modelos-externos-e-especializacoes','baixa',r'^(D360|CustomerDataPlatform|StreamingAppDataConnector)'),
# Dev
(DV,'codigo-e-bundles','media',r'^(LightningBolt|LightningTypeBundle|UIBundle|UiWidgetBundle|UiPlugin|DataWeaveResource|FunctionReference|ComputeApp|ComputeExtension|InvocableActionExtension|AppFrameworkTemplateBundle|ContentTypeBundle|DigitalExperienceBundle)'),
(DV,'pacotes-e-dependencias','media',r'^(FeatureParameter)'),
(DV,'testes','alta',r'^(FlowTest)$'),
(DV,'versionamento-deploy-e-recuperacao','media',r'^(ReleaseMgmt|BranchManagement|AutomationPipeline|PlatformWebIde|TrialOrg)'),
# Observabilidade
(O,'logs-e-rastreamento','alta',r'^(DebugLevel|EventLogObjectSettings|ApexEmailNotifications)'),
(O,'limites-e-consumo','media',r'^(ApexLimitSettings)'),
(O,'eventos-de-monitoramento','media',r'^(RealTimeEventSettings|Telemetry)'),
# Execucao
(EX,'batch','media',r'^(BatchCalcJobDefinition|BatchProcessJobDefinition)'),
# Integracao
(I,'eventos-e-mensageria','media',r'^(LightningMessageChannel|EventSettings|PlatformCachePartition_X)'),
(I,'apis-de-dados-e-metadados','media',r'^(ApiNamedQuery|EnterpriseApiSettings|CatalogedApi)'),
(I,'conectividade-e-virtualizacao-de-dados','media',r'^(IntegrationProviderDef|IntegArtifactDef|ObjIntegProvider|ExternalDocStorageConfig|ExternalStoragePrvdConfig|FilesConnectSettings|HerokuAppLink|SynchronizeSettings|CanvasMetadata|LightningOutApp)'),
(I,'chamadas-externas-e-endpoints','media',r'^(EmailServicesFunction|EmailIntegrationSettings|GoogleAppsSettings|MsTeamsAppSettings|PlatformSlackSettings|SlackApp)'),
# Automacao
(AU,'flow-e-orquestracao','alta',r'^(FlowDefinition|FlowCategory|FlowValueMap|OrchestrationPlanCtxMapping|ActionableEventOrchDef|DynamicFulfillmentOrchestrator|IndustriesEventOrch|ServiceCloudNotificationOrchestrator|VoiceWorkflow)'),
(AU,'decisoes-e-aprovacoes','media',r'^(DecisionMatrix|DecisionTable|ExpressionSet|PolicyRuleDefinition|ConstraintOptDef|IndustriesConstraints|LogicSettings|CriteriaSettings)'),
(AU,'acoes-e-regras','media',r'^(CommandAction|RecordActionDeployment|ActionLinkGroupTemplate|ActionLauncherItemDef|ActionPlanTemplate|TriggerConfigurationsSettings|AutomatorConfigSettings)'),
(AU,'notificacoes','alta',r'^(NotificationTypeConfig|NotificationsSettings|SystemNotificationSettings|MobileAppNewsflashTopic|RecordAlert|RecAlrt|TmfOutboundNotification)'),
# Conteudo
(C,'templates-e-comunicacao','media',r'^(PostTemplate|EmailTemplateFolder|QuickTextSettings|MailMergeSettings|DocumentTemplate|DocumentGenerationSetting|ReplyEmailConfig|BrandKit)'),
(C,'files-e-documentos','media',r'^(DocumentFolder|EmailFolder|ContentWorkspace|ContentSettings|OcrTemplate|OcrSampleDocument|DocProcDefinition|ESignature|BriefcaseDefinition)'),
(C,'colaboracao','media',r'^(ChatterExtension|ChatterEmailsMD|ChatterAnswers|CustomFeedFilter|IdeasSettings|Tag$|TagSet|TopicsForObjects|SurveySettings|SurveyStyleSet|MeetingsSettings)'),
(C,'knowledge-e-categorias','media',r'^(ServiceMgmtKnwlg|SynonymDictionary|DictionariesSettings)'),
(C,'bibliotecas-e-assets','media',r'^(ManagedContentType)'),
# UI
(UI,'aplicativos-e-navegacao','media',r'^(AppMenu|CustomApplicationComponent|CustomHelpMenuSection|CustomPageWebLink|SearchCustomization|SearchOrgWideObjectConfig|LightningOnboardingConfig|AppExperienceSettings|AppStudioSettings|ViewDefinition)'),
(UI,'layouts-e-paginas-de-registro','media',r'^(HomePageComponent|HomePageLayout|ChannelLayout|DynamicUiCardDefinition|OmniUiCard|UiFormatSpecificationSet|UiPreviewMessageTabDef|UiWidgetSettings|UIBundleSettings|AnimationRule)'),
(UI,'experiencias-web-portais-e-mobile','media',r'^(MobileApplicationDetail|MobilePublisher|DxGlobalTerms|WebToX)'),
(UI,'acessibilidade-e-personalizacao','baixa',r'^(CustomPreferencePageSettings)'),
# Org
(OR,'localizacao-idiomas-e-traducao','alta',r'(Translation$|^GeocodeSettings|^MapsAndLocationSettings|^EclairGeoData)'),
(OR,'habilitacao-de-recursos','baixa',r'^(EssentialsSettings|AdminSuccessSettings|TrailheadSettings|EasyFreemium|GeneralConfigSettings|IoTSettings|BlockchainSettings|Web3Settings|EmergencySettings|DataDotComSettings_X)'),
# Produto: experiencias externas
(P,'experiencias-externas','alta',r'^(Community$|Audience|NetworkBranding|PortalsSettings|DigitalExperience$|SelfSvcPortalTopic|SelfServiceSettings)'),
# Produto: field service
(P,'servico-de-campo','media',r'^(FieldService|DynamicGantt|SchedulingPolicy|SchedulingRecipe|LaborCost|TmshtLabor|ApptBooking|AppointmentBooking|LocationUse|Missionforce|ServiceScheduleConfig|WorkforceScheduling|WorkforceManagement|EnhancedServiceWFM)'),
# Produto: atendimento
(P,'atendimento','media',r'^(Service|Svc|Srvc|Cnfg|EmbeddedService|Messaging|CallCenter|Telephony|TrustedTelephony|SecondaryTelephony|ScndTeleph|Voice|Voce|Thunderbird|ConversationChannel|ConversationService|CommunicationChannel|EngmtChannel|CommBlock|Skill|CommsServiceConsole|CallCoaching|ProcedurePlan|EvidenceMgmt|DripFeed|ChannelRevMgmt)'),
# Produto: receita e comercio
(P,'receita-e-comercio','media',r'^(Billing|Commerce|WebStore|OrderManagement|OnlineSales|Payment|Paynow|GatewayProvider|DigitalWallet|PurchaseOrder|Inventory|InvMgmt|InvLate|StockRotation|Product|LargeQuotes|SubscriptionManagement|TransactionProcessing|TransactableMarketplace|ContractType|Rebate|EasySuites|Accounting|FlexHier|Optimization|OmniChannelPricing|SoFieldMapping|IncludeEst|SalesAgreement|Cmsn|Commission|Spiff|IndustriesRating|IndustriesUsage|IndustriesUnifiedInventory|IndustriesChannelPartnerInventory)'),
# Produto: vendas
(P,'vendas','media',r'^(Account|Acct|AdvA|Forecasting|HighVelocitySales|Sales|MeetingPlaybook|SequenceService|EinsteinDeal|Territory|CampaignInfluence|StageAssignment|StageDefinition|PlanningDim|PlanningMeasure|Enablement|Enbl|PrmCore|MktPlanningOps)'),
# Produto: setoriais
(P,'capacidades-setoriais','media',r'^(Industries|Ins[A-Z]|Insurance|Claim|Benefit|CareProvider|HealthIns|LifeSci|Financial|Household|Fundraising|GiftEntry|Mfg|Manufacturing|QualityManagement|Warranty|RetailExecution|Media|ProviderSample|Reglt|Referral(?!Marketing)|Course|Learning|ParticipantRole|RiskMgmt|GRC|Actionable|Actnbl|Assessment|BusinessProcess|ApplicationSubtype|RecLifecycl|RecordCompanion|AssociationEngine|IntegratedPlan|LoyaltyProgram|EACSettings|EvfSettings|RelatedRecordAssoc|DgtAsset|ConsentTemplate_X|InterestTagging)'),
# Produto: outras areas (marketing etc)
(P,'outras-areas','baixa',r'^(Marketing|Mkt|MCE|ReferralMarketing|Pardot|MarketSegment|WorkDotCom|DiscoveryX)'),
]


# ----------------------------------------------------------------- família provável e recorte provável
# (família, nuvem do catálogo ou None, recorte provável, confiança, padrão). A ordem importa: a primeira regra que casa vence.
FORA, COND, CORE, APOS = "fora_do_core_provavel", "condicional_provavel", "candidato_core", "aposentado_provavel"
REGRAS_FAMILIA = [
    ("Produto aposentado ou legado", None, APOS, "media",
     r"^(Pardot|DataDotCom|CleanDataService|HomePage|WorkDotCom|WorkflowSend|ProcessFlowMigration|PlatformEventMigration|MailMerge|ChatterAnswers|"
     r"Ideas|EasyFreemium|Eclair|BlacklistedConsumer|MailAppOwa|Thunderbird|Blockchain|Web3)"),
    ("Experience Cloud", "nuv:experience-cloud", FORA, "alta",
     r"^(Community$|Network|Portal|DigitalExperience|Audience|SharingSet|TopicsForObjects|SelfSvcPortal|DxGlobal|SelfServiceSettings)"),
    ("IA, Agentforce e Einstein", None, COND, "media",
     r"^(AI|Ai|Agent|Agentic|Einstein|GenOp|GenComputing|Generative|Assistant|Prompt$|ExternalAI|ExternalAiAgent|Explainability|MlDomain|"
     r"PredictionBuilder|RecommendationBuilder|RecommendationStrategy|RetrievalSummary|SetupCopilot|SecurityAgent|PrivacyAgent|MediaAgent|"
     r"KnowledgeGeneration|CustomizablePropensity|AffinityScore|AnalyticsLlm|AnlytAgnt|SceGlobalModel|McpServerDefinition|Bot)"),
    ("Analytics (CRM Analytics / Tableau)", None, FORA, "media", r"^(Analytics|Wave|Discovery|Disco)"),
    ("Field Service", "nuv:field-service", FORA, "media",
     r"^(FieldService|DynamicGantt|SchedulingPolicy|SchedulingRecipe|LaborCost|TmshtLabor|ApptBooking|AppointmentBooking|LocationUse|Missionforce|"
     r"WorkforceScheduling|WorkforceManagement|EnhancedServiceWFM|ServiceScheduleConfig)"),
    ("Service Cloud", "nuv:service-cloud", FORA, "media",
     r"^(Service|Svc|Srvc|Cnfg|EmbeddedService|Messaging|CallCenter|Telephony|TrustedTelephony|SecondaryTelephony|ScndTeleph|Voice|Voce|"
     r"ConversationChannel|ConversationService|CommunicationChannel|EngmtChannel|CommBlock|Skill|CommsServiceConsole|CallCoaching|ProcedurePlan|"
     r"EvidenceMgmt|DripFeed|CaseSubject|IncludeEst)"),
    ("Commerce", "nuv:commerce", FORA, "media",
     r"^(Commerce|WebStore|OnlineSales|Payment|Paynow|GatewayProvider|DigitalWallet|TransactableMarketplace|ProductDiscovery|ShippingTo)"),
    ("Revenue, CPQ e Billing", "nuv:revenue", FORA, "media",
     r"^(Billing|OrderManagement|PurchaseOrder|Inventory|InvMgmt|InvLate|StockRotation|Product|LargeQuotes|SubscriptionManagement|"
     r"TransactionProcessing|ContractType|ChannelRevMgmt|Rebate|DynamicFulfillment|EasySuites|Accounting|FlexHier|ConstraintOptDef|Optimization|"
     r"OmniChannelPricing|SoFieldMapping|SalesAgreement|Cmsn|Commission|Spiff)"),
    ("Marketing", "nuv:marketing", FORA, "media", r"^(Marketing|Mkt|MCE|InterestTagging|ReferralMarketing|BrandKit|MarketSegment)"),
    ("Sales Cloud", "nuv:sales-cloud", FORA, "media",
     r"^(Account(Forecast|Intelligence|Plan|RelationshipShare)|AcctMgr|AdvA|Forecasting|Opportunity|DCOpportunity|WinProbability|PipelineInsp|"
     r"LeadScore|HighVelocitySales|Sales|Statistical|UnifiedSalesIntelligence|MeetingPlaybook|Meetings|SequenceService|Territory|CampaignInfluence|"
     r"StageAssignment|StageDefinition|PlanningDim|PlanningMeasure|ConvIntelligence|ConversationalIntelligence|Enablement|Enbl|PrmCore)"),
    ("Industries", "nuv:industries", FORA, "media",
     r"^(Industries|Ins[A-Z]|Insurance|Claim|Benefit|CareProvider|HealthIns|LifeSci|Financial|Household|Fundraising|GiftEntry|Mfg|Manufacturing|"
     r"QualityManagement|Warranty|RetailExecution|Media|ProviderSample|Reglt|Referral|Course|Learning|ParticipantRole|EmployeeData|EmployeeField|"
     r"EmployeeUser|Evidence|RiskMgmt|GRC|ActionLauncher|Actionable|Actnbl|Assessment|BusinessProcess|BusinessValue|ApplicationSubtype|"
     r"DecisionMatrix|DecisionTable|ExpressionSet|BatchCalc|BatchProcess|ContextDefinition|ContextMapping|ContextUseCase|OmniUiCard|Orchestration|"
     r"RecAlrt|RecordAlert|RecLifecycl|RecordCompanion|FieldMappingConfig|FieldSrcTrgt|ObjectFieldValueMapping|ObjectSourceTargetMap|ExtDataTran|"
     r"IdentityRsol|PartyDataModel|PartyProfile|OnboardingDataObject|AssociationEngine|PolicyRule|IntegratedPlan|LoyaltyProgram|EACSettings|"
     r"EvfSettings|RelatedRecordAssoc|DgtAsset|AutomatorConfig|TmfOutbound|CollectionsDashboard)"),
    ("Data 360", "nuv:data-360", FORA, "baixa", r"^(D360|CustomerDataPlatform|StreamingAppDataConnector)"),
    ("Slack", "nuv:slack", COND, "media", r"^(SlackApp|PlatformSlackSettings)"),
    ("Plataforma com licença ou add-on provável", None, COND, "baixa",
     r"^(Security(Hub|CustomBaseline|SignalWorkspace)|TenantSecurity|PrivacyOrgConfig|DsarPolicy|Consent|GlobalConsent|DocumentTemplate|"
     r"DocumentGeneration|OcrTemplate|OcrSampleDocument|DocProcDefinition|ESignature|DataMask|MobilePublisher|HerokuAppLink|TransactionSecurityPolicy|"
     r"RealTimeEventSettings|EventLogObjectSettings|SensitiveDataRule|IoTSettings|Survey|ComputeApp|ComputeExtension|FunctionReference)"),
    # Sem regra de produto que case: sobra como candidato ao Core, com confiança baixa (é o resto, não uma evidência).
    ("Plataforma (candidato ao Core)", "nuv:platform-core", CORE, "baixa", r"."),
]


def primeira(regras, nome, idx):
    for r in regras:
        if re.search(r[idx], nome):
            return r
    return None


def main():
    inv = json.load(open(INV, encoding="utf-8"))
    pend = sorted(x["nome"] for x in inv["itens"] if x["recorte_core"] == "pendente")
    itens = []
    for n in pend:
        f = primeira(REGRAS_FAMILIA, n, 4)
        c = primeira(REGRAS_FUNCIONAIS, n, 3)
        itens.append({
            "nome": n,
            "familia_provavel": f[0], "nuvem_provavel": f[1], "recorte_provavel": f[2], "confianca_familia": f[3],
            "classificacao_provavel": ("cls:" + c[0]) if c else None, "subclassificacao_provavel": ("sub:" + c[1]) if c else None,
            "confianca_classificacao": c[2] if c else "sem_pista",
            "inferido": True,
        })
    doc = {
        "descricao": "Triagem semântica, só pelo nome, dos metadata types pendentes de recorte Core. Inferida; não é decisão nem fonte.",
        "metodo": "Regras de padrão de nome em ferramentas/triagem_pendentes.py, escritas em " + DATA_REGRAS + " na conversa com a autora.",
        "inventario": "inventarios/metadata-types-v68.json",
        "total": len(itens),
        "itens": itens,
    }
    with open(SAIDA_JSON, "w", encoding="utf-8") as h:
        json.dump(doc, h, ensure_ascii=False, indent=2)
        h.write("\n")
    escrever_md(itens)
    print(f"triagem: {len(itens)} pendentes -> relatorios/triagem-pendentes.json e .md")


def escrever_md(itens):
    L = ["# Triagem semântica dos tipos pendentes de recorte Core (#10)", "",
         "> **Inferido só pelo nome do tipo.** Não é decisão de recorte nem classificação do catálogo: serve para ordenar os lotes da",
         "> etapa 2 por família e sugerir a classificação funcional no cadastro. Cada decisão continua exigindo fonte por família.",
         "> Gerado por `ferramentas/triagem_pendentes.py` (regras de " + DATA_REGRAS + "); rode de novo depois de cada lote.", "",
         f"Tipos pendentes: **{len(itens)}**.", "", "## Por família provável", "",
         "| Família provável | Recorte provável | Tipos | Exemplos |", "|---|---|---|---|"]
    por_f = collections.defaultdict(list)
    for i in itens:
        por_f[(i["familia_provavel"], i["recorte_provavel"])].append(i["nome"])
    rot = {FORA: "fora do Core", COND: "condicional", CORE: "candidato ao Core", APOS: "aposentado"}
    for (f, r), ns in sorted(por_f.items(), key=lambda kv: -len(kv[1])):
        L.append(f"| {f} | {rot[r]} | {len(ns)} | {', '.join(ns[:5])} |")
    L += ["", "## Por classificação funcional provável", "", "| Classificação | Subclassificação | Tipos |", "|---|---|---|"]
    por_c = collections.Counter((i["classificacao_provavel"], i["subclassificacao_provavel"]) for i in itens)
    for (c, s), k in sorted(por_c.items(), key=lambda kv: (str(kv[0][0]), -kv[1])):
        L.append(f"| {(c or 'sem pista').replace('cls:', '')} | {(s or '-').replace('sub:', '')} | {k} |")
    conf = collections.Counter(i["confianca_classificacao"] for i in itens)
    L += ["", "Confiança da classificação funcional: " + ", ".join(f"{k} {v}" for k, v in sorted(conf.items())) + ".", "",
          "## Lacunas do mapa que a triagem revelou", "",
          "- Marketing não tem subclassificação própria em processos de negócio; os tipos de Marketing caem em \"outras áreas\".",
          "- Data 360 não tem lugar claro na classificação funcional.",
          "", "## Lista completa", "", "| Tipo | Família provável | Classificação provável | Confiança |", "|---|---|---|---|"]
    for i in itens:
        cl = (i["subclassificacao_provavel"] or "sem pista").replace("sub:", "")
        L.append(f"| {i['nome']} | {i['familia_provavel']} | {cl} | {i['confianca_familia']} / {i['confianca_classificacao']} |")
    with open(SAIDA_MD, "w", encoding="utf-8") as h:
        h.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
