# Triagem semântica dos tipos pendentes de recorte Core (#10)

> **Inferido só pelo nome do tipo.** Não é decisão de recorte nem classificação do catálogo: serve para ordenar os lotes da
> etapa 2 por família e sugerir a classificação funcional no cadastro. Cada decisão continua exigindo fonte por família.
> Gerado por `ferramentas/triagem_pendentes.py` (regras de 2026-11-23); rode de novo depois de cada lote.

Tipos pendentes: **646**.

## Por família provável

| Família provável | Recorte provável | Tipos | Exemplos |
|---|---|---|---|
| Plataforma (candidato ao Core) | candidato ao Core | 158 | ActionLinkGroupTemplate, ActionPlanTemplate, AdminSuccessSettings, AnalyticSnapshot, AnimationRule |
| Industries | fora do Core | 130 | ActionLauncherItemDef, ActionableEventOrchDef, ActionableEventTypeDef, ActionableListDefinition, ActnblListKeyPrfmIndDef |
| Service Cloud | fora do Core | 82 | CallCenter, CallCoachingMediaProvider, CnfgItemAttrDef, CnfgItemAttrPcklstValDef, CnfgItemAttrPicklistDef |
| IA, Agentforce e Einstein | condicional | 57 | AIApplication, AIApplicationConfig, AIReplyRecommendationsSettings, AIScoringModelDefVersion, AIScoringModelDefinition |
| Sales Cloud | fora do Core | 47 | AccountForecastSettings, AccountIntelligenceSettings, AccountPlanObjMeasCalcDef, AccountPlanSettings, AccountRelationshipShareRule |
| Plataforma com licença ou add-on provável | condicional | 42 | ComputeApp, ComputeExtension, ConsentPreferenceFormDef, ConsentTemplate, DataMaskPolicy |
| Revenue, CPQ e Billing | fora do Core | 35 | AccountingFieldMapping, AccountingModelConfig, AccountingSettings, BillingSettings, ChannelRevMgmtSettings |
| Produto aposentado ou legado | aposentado | 20 | BlacklistedConsumer, BlockchainSettings, ChatterAnswersSettings, CleanDataService, DataDotComSettings |
| Field Service | fora do Core | 18 | AppointmentBookingSettings, ApptBookingConfig, ApptBookingUrlConfig, DynamicGanttSettings, EnhancedServiceWFMSettings |
| Marketing | fora do Core | 14 | BrandKitSettings, InterestTaggingSettings, MCETransformationsSettings, MarketSegment, MarketSegmentActivation |
| Commerce | fora do Core | 13 | CommerceSettings, DigitalWalletSettings, GatewayProviderPaymentMethodType, OnlineSalesSettings, PaymentGatewayProvider |
| Analytics (CRM Analytics / Tableau) | fora do Core | 12 | AnalyticsAgentDefinition, AnalyticsDashboard, AnalyticsDatasetDefinition, AnalyticsSettings, AnalyticsVisualization |
| Experience Cloud | fora do Core | 12 | Audience, Community, DigitalExperience, DigitalExperienceBundle, DxGlobalTermsSettings |
| Data 360 | fora do Core | 3 | CustomerDataPlatformSettings, D360, StreamingAppDataConnector |
| Slack | condicional | 3 | PlatformSlackSettings, SlackApp, SlackAppTemplate |

## Por classificação funcional provável

| Classificação | Subclassificação | Tipos |
|---|---|---|
| sem pista | - | 1 |
| acesso-identidade-e-seguranca | acesso-a-registros-e-hierarquias | 12 |
| acesso-identidade-e-seguranca | sessoes-e-politicas-de-login | 11 |
| acesso-identidade-e-seguranca | credenciais-certificados-e-protecao-de-dados | 10 |
| acesso-identidade-e-seguranca | usuarios-e-provisionamento | 5 |
| acesso-identidade-e-seguranca | permissoes-perfis-e-grupos | 4 |
| acesso-identidade-e-seguranca | autenticacao-sso-e-mfa | 4 |
| acesso-identidade-e-seguranca | licencas-e-entitlements-de-acesso | 2 |
| automacao-de-processos-e-regras-de-negocio | decisoes-e-aprovacoes | 14 |
| automacao-de-processos-e-regras-de-negocio | flow-e-orquestracao | 10 |
| automacao-de-processos-e-regras-de-negocio | notificacoes | 9 |
| automacao-de-processos-e-regras-de-negocio | acoes-e-regras | 7 |
| automacao-de-processos-e-regras-de-negocio | mecanismos-legados-e-migracao | 3 |
| conteudo-conhecimento-e-colaboracao | files-e-documentos | 11 |
| conteudo-conhecimento-e-colaboracao | colaboracao | 11 |
| conteudo-conhecimento-e-colaboracao | templates-e-comunicacao | 8 |
| conteudo-conhecimento-e-colaboracao | knowledge-e-categorias | 4 |
| conteudo-conhecimento-e-colaboracao | bibliotecas-e-assets | 1 |
| dados-e-modelagem | metadados-de-configuracao-de-dados | 14 |
| dados-e-modelagem | listas-de-valores | 7 |
| dados-e-modelagem | relacionamentos-e-juncoes | 5 |
| dados-e-modelagem | campos-e-tipos | 3 |
| dados-e-modelagem | modelos-externos-e-especializacoes | 3 |
| desenvolvimento-testes-e-entrega | codigo-e-bundles | 14 |
| desenvolvimento-testes-e-entrega | versionamento-deploy-e-recuperacao | 5 |
| desenvolvimento-testes-e-entrega | pacotes-e-dependencias | 3 |
| desenvolvimento-testes-e-entrega | testes | 1 |
| execucao-assincrona-lotes-e-agendamento | batch | 2 |
| ia-agentes-e-decisoes-assistidas | configuracao-de-agentes | 32 |
| ia-agentes-e-decisoes-assistidas | modelos-e-grounding | 15 |
| ia-agentes-e-decisoes-assistidas | seguranca-avaliacao-e-governanca-de-ia | 8 |
| ia-agentes-e-decisoes-assistidas | acoes-e-topicos | 7 |
| ia-agentes-e-decisoes-assistidas | prompts | 6 |
| ia-agentes-e-decisoes-assistidas | recuperacao-de-conhecimento | 2 |
| integracao-apis-e-eventos | conectividade-e-virtualizacao-de-dados | 10 |
| integracao-apis-e-eventos | chamadas-externas-e-endpoints | 7 |
| integracao-apis-e-eventos | apis-de-dados-e-metadados | 5 |
| integracao-apis-e-eventos | eventos-e-mensageria | 2 |
| interface-e-experiencia-do-usuario | aplicativos-e-navegacao | 10 |
| interface-e-experiencia-do-usuario | layouts-e-paginas-de-registro | 9 |
| interface-e-experiencia-do-usuario | experiencias-web-portais-e-mobile | 8 |
| interface-e-experiencia-do-usuario | acessibilidade-e-personalizacao | 1 |
| observabilidade-auditoria-e-operacao | eventos-de-monitoramento | 6 |
| observabilidade-auditoria-e-operacao | logs-e-rastreamento | 3 |
| observabilidade-auditoria-e-operacao | limites-e-consumo | 1 |
| organizacao-e-configuracoes-base | habilitacao-de-recursos | 9 |
| organizacao-e-configuracoes-base | localizacao-idiomas-e-traducao | 4 |
| processos-de-negocio-especificos-de-produto | capacidades-setoriais | 86 |
| processos-de-negocio-especificos-de-produto | atendimento | 73 |
| processos-de-negocio-especificos-de-produto | receita-e-comercio | 50 |
| processos-de-negocio-especificos-de-produto | vendas | 33 |
| processos-de-negocio-especificos-de-produto | servico-de-campo | 18 |
| processos-de-negocio-especificos-de-produto | outras-areas | 14 |
| processos-de-negocio-especificos-de-produto | experiencias-externas | 7 |
| qualidade-governanca-e-ciclo-de-vida-dos-dados | consentimento-e-privacidade | 9 |
| qualidade-governanca-e-ciclo-de-vida-dos-dados | duplicidade-e-correspondencia | 3 |
| qualidade-governanca-e-ciclo-de-vida-dos-dados | classificacao-e-sensibilidade | 1 |
| relatorios-analytics-e-exploracao | recursos-analiticos-de-produto | 18 |
| relatorios-analytics-e-exploracao | dashboards | 3 |
| relatorios-analytics-e-exploracao | reports | 2 |

Confiança da classificação funcional: alta 80, baixa 27, media 538, sem_pista 1.

## Lacunas do mapa que a triagem revelou

- Marketing não tem subclassificação própria em processos de negócio; os tipos de Marketing caem em "outras áreas".
- Data 360 não tem lugar claro na classificação funcional.

## Lista completa

| Tipo | Família provável | Classificação provável | Confiança |
|---|---|---|---|
| AIApplication | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AIApplicationConfig | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AIReplyRecommendationsSettings | IA, Agentforce e Einstein | acoes-e-topicos | media / media |
| AIScoringModelDefVersion | IA, Agentforce e Einstein | modelos-e-grounding | media / media |
| AIScoringModelDefinition | IA, Agentforce e Einstein | modelos-e-grounding | media / media |
| AIUsecaseDefinition | IA, Agentforce e Einstein | modelos-e-grounding | media / media |
| AIWorksheetTemplate | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AccountForecastSettings | Sales Cloud | vendas | media / media |
| AccountIntelligenceSettings | Sales Cloud | recursos-analiticos-de-produto | media / media |
| AccountPlanObjMeasCalcDef | Sales Cloud | vendas | media / media |
| AccountPlanSettings | Sales Cloud | vendas | media / media |
| AccountRelationshipShareRule | Sales Cloud | acesso-a-registros-e-hierarquias | media / alta |
| AccountingFieldMapping | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| AccountingModelConfig | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| AccountingSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| AcctMgrTargetSettings | Sales Cloud | vendas | media / media |
| ActionLauncherItemDef | Industries | acoes-e-regras | media / media |
| ActionLinkGroupTemplate | Plataforma (candidato ao Core) | acoes-e-regras | baixa / media |
| ActionPlanTemplate | Plataforma (candidato ao Core) | acoes-e-regras | baixa / media |
| ActionableEventOrchDef | Industries | flow-e-orquestracao | media / alta |
| ActionableEventTypeDef | Industries | capacidades-setoriais | media / media |
| ActionableListDefinition | Industries | capacidades-setoriais | media / media |
| ActnblListKeyPrfmIndDef | Industries | capacidades-setoriais | media / media |
| AdminSuccessSettings | Plataforma (candidato ao Core) | habilitacao-de-recursos | baixa / baixa |
| AdvAccountForecastSet | Sales Cloud | vendas | media / media |
| AdvAcctForecastDimSource | Sales Cloud | vendas | media / media |
| AdvAcctForecastPeriodGroup | Sales Cloud | vendas | media / media |
| AffinityScoreDefinition | IA, Agentforce e Einstein | modelos-e-grounding | media / media |
| AgentPlatformSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AgentforceAccountManagementSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AgentforceProspectingSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AgentforceSessionTracingSettings | IA, Agentforce e Einstein | seguranca-avaliacao-e-governanca-de-ia | media / media |
| AgenticCtxtDecorDefinition | IA, Agentforce e Einstein | recuperacao-de-conhecimento | media / media |
| Ai4mSettings | IA, Agentforce e Einstein | modelos-e-grounding | media / media |
| AiAgentBundleAssignment | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AiAgentScorerDefinition | IA, Agentforce e Einstein | seguranca-avaliacao-e-governanca-de-ia | media / media |
| AiBundle | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AiBundleVersion | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AiTestingDefinition | IA, Agentforce e Einstein | seguranca-avaliacao-e-governanca-de-ia | media / media |
| AnalyticSnapshot | Plataforma (candidato ao Core) | reports | baixa / media |
| AnalyticsAgentDefinition | Analytics (CRM Analytics / Tableau) | configuracao-de-agentes | media / media |
| AnalyticsDashboard | Analytics (CRM Analytics / Tableau) | dashboards | media / media |
| AnalyticsDatasetDefinition | Analytics (CRM Analytics / Tableau) | recursos-analiticos-de-produto | media / media |
| AnalyticsLlmOverride | IA, Agentforce e Einstein | seguranca-avaliacao-e-governanca-de-ia | media / media |
| AnalyticsSettings | Analytics (CRM Analytics / Tableau) | recursos-analiticos-de-produto | media / media |
| AnalyticsVisualization | Analytics (CRM Analytics / Tableau) | recursos-analiticos-de-produto | media / media |
| AnalyticsWorkspace | Analytics (CRM Analytics / Tableau) | recursos-analiticos-de-produto | media / media |
| AnimationRule | Plataforma (candidato ao Core) | layouts-e-paginas-de-registro | baixa / media |
| AnlytAgntFlbkSmntcModel | IA, Agentforce e Einstein | modelos-e-grounding | media / media |
| ApexEmailNotifications | Plataforma (candidato ao Core) | logs-e-rastreamento | baixa / alta |
| ApexLimitSettings | Plataforma (candidato ao Core) | limites-e-consumo | baixa / media |
| ApiNamedQuery | Plataforma (candidato ao Core) | apis-de-dados-e-metadados | baixa / media |
| AppAnalyticsSettings | Plataforma (candidato ao Core) | recursos-analiticos-de-produto | baixa / media |
| AppExperienceSettings | Plataforma (candidato ao Core) | aplicativos-e-navegacao | baixa / media |
| AppFrameworkTemplateBundle | Plataforma (candidato ao Core) | codigo-e-bundles | baixa / media |
| AppMenu | Plataforma (candidato ao Core) | aplicativos-e-navegacao | baixa / media |
| AppStudioSettings | Plataforma (candidato ao Core) | aplicativos-e-navegacao | baixa / media |
| ApplicationSubtypeDefinition | Industries | capacidades-setoriais | media / media |
| AppointmentBookingSettings | Field Service | servico-de-campo | media / media |
| ApptBookingConfig | Field Service | servico-de-campo | media / media |
| ApptBookingUrlConfig | Field Service | servico-de-campo | media / media |
| AssessmentConfiguration | Industries | capacidades-setoriais | media / media |
| AssistantContextItem | IA, Agentforce e Einstein | acoes-e-topicos | media / media |
| AssistantDefinition | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AssistantSkillQuickAction | IA, Agentforce e Einstein | acoes-e-topicos | media / media |
| AssistantSkillSobjectAction | IA, Agentforce e Einstein | acoes-e-topicos | media / media |
| AssistantVersion | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| AssociationEngineSettings | Industries | capacidades-setoriais | media / media |
| Audience | Experience Cloud | experiencias-externas | alta / alta |
| AutomationPipeline | Plataforma (candidato ao Core) | versionamento-deploy-e-recuperacao | baixa / media |
| AutomatorConfigSettings | Industries | acoes-e-regras | media / media |
| BatchCalcJobDefinition | Industries | batch | media / media |
| BatchProcessJobDefinition | Industries | batch | media / media |
| BenefitAction | Industries | capacidades-setoriais | media / media |
| BillingSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| BlacklistedConsumer | Produto aposentado ou legado | sessoes-e-politicas-de-login | media / alta |
| BlockchainSettings | Produto aposentado ou legado | habilitacao-de-recursos | media / baixa |
| BotEmailDefinition | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| BranchManagementSettings | Plataforma (candidato ao Core) | versionamento-deploy-e-recuperacao | baixa / media |
| BrandKitSettings | Marketing | templates-e-comunicacao | media / media |
| BriefcaseDefinition | Plataforma (candidato ao Core) | files-e-documentos | baixa / media |
| BusinessProcessGroup | Industries | capacidades-setoriais | media / media |
| BusinessProcessTypeDefinition | Industries | capacidades-setoriais | media / media |
| BusinessValueMetricsSettings | Industries | recursos-analiticos-de-produto | media / media |
| CallCenter | Service Cloud | atendimento | media / media |
| CallCoachingMediaProvider | Service Cloud | atendimento | media / media |
| CampaignInfluenceModel | Sales Cloud | vendas | media / media |
| CanvasMetadata | Plataforma (candidato ao Core) | conectividade-e-virtualizacao-de-dados | baixa / media |
| CareProviderAfflRoleConfig | Industries | capacidades-setoriais | media / media |
| CatalogedApi | Plataforma (candidato ao Core) | apis-de-dados-e-metadados | baixa / media |
| CatalogedApiArtifactVersionInfo | Plataforma (candidato ao Core) | apis-de-dados-e-metadados | baixa / media |
| CatalogedApiVersion | Plataforma (candidato ao Core) | apis-de-dados-e-metadados | baixa / media |
| ChannelLayout | Plataforma (candidato ao Core) | layouts-e-paginas-de-registro | baixa / media |
| ChannelObjectLinkingRule | Plataforma (candidato ao Core) | relacionamentos-e-juncoes | baixa / media |
| ChannelRevMgmtSettings | Revenue, CPQ e Billing | atendimento | media / media |
| ChatterAnswersSettings | Produto aposentado ou legado | colaboracao | media / media |
| ChatterEmailsMDSettings | Plataforma (candidato ao Core) | colaboracao | baixa / media |
| ChatterExtension | Plataforma (candidato ao Core) | colaboracao | baixa / media |
| ChoiceList | Plataforma (candidato ao Core) | listas-de-valores | baixa / alta |
| ClaimCoverageProdtProcDef | Industries | capacidades-setoriais | media / media |
| ClaimFinancialSettings | Industries | capacidades-setoriais | media / media |
| ClaimMgmtFoundationEnabledSettings | Industries | capacidades-setoriais | media / media |
| CleanDataService | Produto aposentado ou legado | duplicidade-e-correspondencia | media / media |
| CmsnStmtLineItemConfig | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| CmsnStmtLineItemTypConfig | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| CnfgItemAttrDef | Service Cloud | atendimento | media / media |
| CnfgItemAttrPcklstValDef | Service Cloud | atendimento | media / media |
| CnfgItemAttrPicklistDef | Service Cloud | atendimento | media / media |
| CnfgItemAttrSetAttr | Service Cloud | atendimento | media / media |
| CnfgItemAttrSetDef | Service Cloud | atendimento | media / media |
| CnfgItemSourceDefinition | Service Cloud | atendimento | media / media |
| CnfgItemTypeAttrRelDef | Service Cloud | atendimento | media / media |
| CnfgItemTypeDef | Service Cloud | atendimento | media / media |
| CnfgItemTypeIdentFieldMap | Service Cloud | atendimento | media / media |
| CnfgItemTypeIdentRule | Service Cloud | atendimento | media / media |
| CnfgItemTypeRelationDef | Service Cloud | atendimento | media / media |
| CnfgItmAstSyncRule | Service Cloud | atendimento | media / media |
| CnfgItmTypAttrSrcRcnRule | Service Cloud | atendimento | media / media |
| CnfgItmTypCmplCond | Service Cloud | atendimento | media / media |
| CnfgItmTypCmplCrit | Service Cloud | atendimento | media / media |
| CnfgItmTypDefCmplCrit | Service Cloud | atendimento | media / media |
| CnfgItmTypSrcRcnRule | Service Cloud | atendimento | media / media |
| CnfgMgmtAssetStsQual | Service Cloud | atendimento | media / media |
| CnfgMgmtDataBndl | Service Cloud | atendimento | media / media |
| CnfgMgmtItemFieldMap | Service Cloud | atendimento | media / media |
| CnfgMgmtItemValueMap | Service Cloud | atendimento | media / media |
| CnfgMgmtRcnRuleSugg | Service Cloud | atendimento | media / media |
| CnfgMgmtRelationTypeDef | Service Cloud | atendimento | media / media |
| CnfgMgmtSvcMapLyot | Service Cloud | atendimento | media / media |
| CollectionsDashboardSettings | Industries | dashboards | media / media |
| CommBlockOutTime | Service Cloud | atendimento | media / media |
| CommandAction | Plataforma (candidato ao Core) | acoes-e-regras | baixa / media |
| CommerceSettings | Commerce | receita-e-comercio | media / media |
| CommissionStatementConfig | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| CommsServiceConsoleSettings | Service Cloud | atendimento | media / media |
| CommunicationChannelLine | Service Cloud | atendimento | media / media |
| CommunicationChannelType | Service Cloud | atendimento | media / media |
| Community | Experience Cloud | experiencias-externas | alta / alta |
| ComputeApp | Plataforma com licença ou add-on provável | codigo-e-bundles | baixa / media |
| ComputeExtension | Plataforma com licença ou add-on provável | codigo-e-bundles | baixa / media |
| ConsentPreferenceFormDef | Plataforma com licença ou add-on provável | consentimento-e-privacidade | baixa / alta |
| ConsentTemplate | Plataforma com licença ou add-on provável | consentimento-e-privacidade | baixa / alta |
| ConstraintOptDef | Revenue, CPQ e Billing | decisoes-e-aprovacoes | media / media |
| ContentSettings | Plataforma (candidato ao Core) | files-e-documentos | baixa / media |
| ContentTypeBundle | Plataforma (candidato ao Core) | codigo-e-bundles | baixa / media |
| ContentWorkspace | Plataforma (candidato ao Core) | files-e-documentos | baixa / media |
| ContentWorkspacePermission | Plataforma (candidato ao Core) | files-e-documentos | baixa / media |
| ContextDefinition | Industries | metadados-de-configuracao-de-dados | media / media |
| ContextMappingConfig | Industries | metadados-de-configuracao-de-dados | media / media |
| ContextUseCaseMapping | Industries | metadados-de-configuracao-de-dados | media / media |
| ContractType | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| ConvIntelligenceSignalRule | Sales Cloud | recursos-analiticos-de-produto | media / media |
| ConversationChannelDefinition | Service Cloud | atendimento | media / media |
| ConversationServiceIntegrationSettings | Service Cloud | atendimento | media / media |
| ConversationalIntelligenceSettings | Sales Cloud | recursos-analiticos-de-produto | media / media |
| CourseWaitlistConfig | Industries | capacidades-setoriais | media / media |
| CriteriaSettings | Plataforma (candidato ao Core) | decisoes-e-aprovacoes | baixa / media |
| CustomApplicationComponent | Plataforma (candidato ao Core) | aplicativos-e-navegacao | baixa / media |
| CustomFeedFilter | Plataforma (candidato ao Core) | colaboracao | baixa / media |
| CustomFieldDisplay | Plataforma (candidato ao Core) | campos-e-tipos | baixa / media |
| CustomHelpMenuSection | Plataforma (candidato ao Core) | aplicativos-e-navegacao | baixa / media |
| CustomIndex | Plataforma (candidato ao Core) | campos-e-tipos | baixa / media |
| CustomObjectBinding | Plataforma (candidato ao Core) | metadados-de-configuracao-de-dados | baixa / media |
| CustomObjectTranslation | Plataforma (candidato ao Core) | localizacao-idiomas-e-traducao | baixa / alta |
| CustomPageWebLink | Plataforma (candidato ao Core) | aplicativos-e-navegacao | baixa / media |
| CustomPermission | Plataforma (candidato ao Core) | permissoes-perfis-e-grupos | baixa / alta |
| CustomPreferencePageSettings | Plataforma (candidato ao Core) | acessibilidade-e-personalizacao | baixa / baixa |
| CustomValue | Plataforma (candidato ao Core) | listas-de-valores | baixa / alta |
| CustomerDataPlatformSettings | Data 360 | modelos-externos-e-especializacoes | baixa / baixa |
| CustomerIntelligenceSettings | Plataforma (candidato ao Core) | recursos-analiticos-de-produto | baixa / media |
| CustomizablePropensityScoringSettings | IA, Agentforce e Einstein | modelos-e-grounding | media / media |
| D360 | Data 360 | modelos-externos-e-especializacoes | baixa / baixa |
| DCOpportunityScoringSettings | Sales Cloud | modelos-e-grounding | media / media |
| DataCategoryGroup | Plataforma (candidato ao Core) | metadados-de-configuracao-de-dados | baixa / media |
| DataDotComSettings | Produto aposentado ou legado | duplicidade-e-correspondencia | media / media |
| DataMaskPolicy | Plataforma com licença ou add-on provável | credenciais-certificados-e-protecao-de-dados | baixa / media |
| DataMaskSettings | Plataforma com licença ou add-on provável | credenciais-certificados-e-protecao-de-dados | baixa / media |
| DataWeaveResource | Plataforma (candidato ao Core) | codigo-e-bundles | baixa / media |
| DebugLevel | Plataforma (candidato ao Core) | logs-e-rastreamento | baixa / alta |
| DecisionMatrixDefinition | Industries | decisoes-e-aprovacoes | media / media |
| DecisionMatrixDefinitionVersion | Industries | decisoes-e-aprovacoes | media / media |
| DecisionTable | Industries | decisoes-e-aprovacoes | media / media |
| DecisionTableDatasetLink | Industries | decisoes-e-aprovacoes | media / media |
| DelegateAccessDataSet | Plataforma (candidato ao Core) | acesso-a-registros-e-hierarquias | baixa / alta |
| DelegateAccessDef | Plataforma (candidato ao Core) | acesso-a-registros-e-hierarquias | baixa / alta |
| DelegateAccsDataSetObj | Plataforma (candidato ao Core) | acesso-a-registros-e-hierarquias | baixa / alta |
| DelegateGroup | Plataforma (candidato ao Core) | permissoes-perfis-e-grupos | baixa / alta |
| DgtAssetMgmtProvider | Industries | capacidades-setoriais | media / media |
| DgtAssetMgmtPrvdLghtCpnt | Industries | capacidades-setoriais | media / media |
| DictionariesSettings | Plataforma (candidato ao Core) | knowledge-e-categorias | baixa / media |
| DigitalExperience | Experience Cloud | experiencias-externas | alta / alta |
| DigitalExperienceBundle | Experience Cloud | codigo-e-bundles | alta / media |
| DigitalWalletSettings | Commerce | receita-e-comercio | media / media |
| DiscoSettings | Analytics (CRM Analytics / Tableau) | recursos-analiticos-de-produto | media / media |
| DiscoveryAIModel | Analytics (CRM Analytics / Tableau) | modelos-e-grounding | media / media |
| DiscoveryGoal | Analytics (CRM Analytics / Tableau) | recursos-analiticos-de-produto | media / media |
| DiscoverySettings | Analytics (CRM Analytics / Tableau) | recursos-analiticos-de-produto | media / media |
| DiscoveryStory | Analytics (CRM Analytics / Tableau) | recursos-analiticos-de-produto | media / media |
| DocProcDefinition | Plataforma com licença ou add-on provável | files-e-documentos | baixa / media |
| DocumentFolder | Plataforma (candidato ao Core) | files-e-documentos | baixa / media |
| DocumentGenerationSetting | Plataforma com licença ou add-on provável | templates-e-comunicacao | baixa / media |
| DocumentTemplate | Plataforma com licença ou add-on provável | templates-e-comunicacao | baixa / media |
| DripFeedConfigSettings | Service Cloud | atendimento | media / media |
| DsarPolicy | Plataforma com licença ou add-on provável | consentimento-e-privacidade | baixa / alta |
| DxGlobalTermsSettings | Experience Cloud | experiencias-web-portais-e-mobile | alta / media |
| DynamicFulfillmentOrchestratorSettings | Revenue, CPQ e Billing | flow-e-orquestracao | media / alta |
| DynamicGanttSettings | Field Service | servico-de-campo | media / media |
| DynamicUiCardDefinition | Plataforma (candidato ao Core) | layouts-e-paginas-de-registro | baixa / media |
| EACSettings | Industries | capacidades-setoriais | media / media |
| ESignatureConfig | Plataforma com licença ou add-on provável | files-e-documentos | baixa / media |
| ESignatureEnvelopeConfig | Plataforma com licença ou add-on provável | files-e-documentos | baixa / media |
| EasyFreemiumSettings | Produto aposentado ou legado | habilitacao-de-recursos | media / baixa |
| EasySuitesInvoicingSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| EclairGeoData | Produto aposentado ou legado | localizacao-idiomas-e-traducao | media / alta |
| EinsteinAISettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| EinsteinAgentSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| EinsteinAssistantSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| EinsteinCopilotSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| EinsteinDealInsightsSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| EinsteinDocumentCaptureSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| EinsteinGPTSalesEmailsSettings | IA, Agentforce e Einstein | prompts | media / media |
| EmailFolder | Plataforma (candidato ao Core) | files-e-documentos | baixa / media |
| EmailIntegrationSettings | Plataforma (candidato ao Core) | chamadas-externas-e-endpoints | baixa / media |
| EmailServicesFunction | Plataforma (candidato ao Core) | chamadas-externas-e-endpoints | baixa / media |
| EmailTemplateFolder | Plataforma (candidato ao Core) | templates-e-comunicacao | baixa / media |
| EmbeddedServiceConfig | Service Cloud | atendimento | media / media |
| EmbeddedServiceFlowConfig | Service Cloud | atendimento | media / media |
| EmbeddedServiceMenuSettings | Service Cloud | atendimento | media / media |
| EmergencySettings | Plataforma (candidato ao Core) | habilitacao-de-recursos | baixa / baixa |
| EmployeeDataSyncProfile | Industries | usuarios-e-provisionamento | media / media |
| EmployeeFieldAccessSettings | Industries | acesso-a-registros-e-hierarquias | media / alta |
| EmployeeUserSettings | Industries | usuarios-e-provisionamento | media / media |
| EnablementCompetencyDef | Sales Cloud | vendas | media / media |
| EnablementMeasureDefinition | Sales Cloud | vendas | media / media |
| EnablementProgramDefinition | Sales Cloud | vendas | media / media |
| EnblProgramTaskSubCategory | Sales Cloud | vendas | media / media |
| EngmtChannelTypeConfig | Service Cloud | atendimento | media / media |
| EnhancedServiceWFMSettings | Field Service | servico-de-campo | media / media |
| EnterpriseApiSettings | Plataforma (candidato ao Core) | apis-de-dados-e-metadados | baixa / media |
| EssentialsSettings | Plataforma (candidato ao Core) | habilitacao-de-recursos | baixa / baixa |
| EventLogObjectSettings | Plataforma com licença ou add-on provável | logs-e-rastreamento | baixa / alta |
| EventSettings | Plataforma (candidato ao Core) | eventos-e-mensageria | baixa / media |
| EvfSettings | Industries | capacidades-setoriais | media / media |
| EvidenceMgmtSettings | Service Cloud | atendimento | media / media |
| ExplainabilityActionDefinition | IA, Agentforce e Einstein | seguranca-avaliacao-e-governanca-de-ia | media / media |
| ExplainabilityActionVersion | IA, Agentforce e Einstein | seguranca-avaliacao-e-governanca-de-ia | media / media |
| ExplainabilityMsgTemplate | IA, Agentforce e Einstein | seguranca-avaliacao-e-governanca-de-ia | media / media |
| ExpressionSetDefinition | Industries | decisoes-e-aprovacoes | media / media |
| ExpressionSetDefinitionVersion | Industries | decisoes-e-aprovacoes | media / media |
| ExpressionSetMessageToken | Industries | decisoes-e-aprovacoes | media / media |
| ExpressionSetObjectAlias | Industries | decisoes-e-aprovacoes | media / media |
| ExtDataTranFieldTemplate | Industries | metadados-de-configuracao-de-dados | media / media |
| ExternalAIModel | IA, Agentforce e Einstein | modelos-e-grounding | media / media |
| ExternalAiAgentSetup | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| ExternalDocStorageConfig | Plataforma (candidato ao Core) | conectividade-e-virtualizacao-de-dados | baixa / media |
| ExternalStoragePrvdConfig | Plataforma (candidato ao Core) | conectividade-e-virtualizacao-de-dados | baixa / media |
| ExtlClntAppAttestConfigurablePolicies | Plataforma (candidato ao Core) | autenticacao-sso-e-mfa | baixa / media |
| ExtlClntAppAttestSettings | Plataforma (candidato ao Core) | autenticacao-sso-e-mfa | baixa / media |
| ExtlClntAppOauthSecuritySettings | Plataforma (candidato ao Core) | autenticacao-sso-e-mfa | baixa / media |
| FeatureParameterBoolean | Plataforma (candidato ao Core) | pacotes-e-dependencias | baixa / media |
| FeatureParameterDate | Plataforma (candidato ao Core) | pacotes-e-dependencias | baixa / media |
| FeatureParameterInteger | Plataforma (candidato ao Core) | pacotes-e-dependencias | baixa / media |
| FieldMappingConfig | Industries | metadados-de-configuracao-de-dados | media / media |
| FieldRestrictionRule | Plataforma (candidato ao Core) | acesso-a-registros-e-hierarquias | baixa / alta |
| FieldServiceMobileConfig | Field Service | servico-de-campo | media / media |
| FieldServiceMobileExtension | Field Service | servico-de-campo | media / media |
| FieldSrcTrgtRelationship | Industries | relacionamentos-e-juncoes | media / media |
| FilesConnectSettings | Plataforma (candidato ao Core) | conectividade-e-virtualizacao-de-dados | baixa / media |
| FinancialAppUiConfig | Industries | capacidades-setoriais | media / media |
| FinancialClientComponentConfig | Industries | capacidades-setoriais | media / media |
| FinancialEvaluationDef | Industries | capacidades-setoriais | media / media |
| FinancialPortfolioUiConfig | Industries | capacidades-setoriais | media / media |
| FlexHierConfig | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| FlowCategory | Plataforma (candidato ao Core) | flow-e-orquestracao | baixa / alta |
| FlowDefinition | Plataforma (candidato ao Core) | flow-e-orquestracao | baixa / alta |
| FlowTest | Plataforma (candidato ao Core) | testes | baixa / alta |
| FlowValueMap | Plataforma (candidato ao Core) | flow-e-orquestracao | baixa / alta |
| ForecastingFilter | Sales Cloud | vendas | media / media |
| ForecastingFilterCondition | Sales Cloud | vendas | media / media |
| ForecastingGroup | Sales Cloud | vendas | media / media |
| ForecastingObjectListSettings | Sales Cloud | vendas | media / media |
| ForecastingSourceDefinition | Sales Cloud | vendas | media / media |
| ForecastingType | Sales Cloud | vendas | media / media |
| ForecastingTypeSource | Sales Cloud | vendas | media / media |
| FormulaSettings | Plataforma (candidato ao Core) | campos-e-tipos | baixa / media |
| FunctionReference | Plataforma com licença ou add-on provável | codigo-e-bundles | baixa / media |
| FundraisingConfig | Industries | capacidades-setoriais | media / media |
| GRCIntelligenceUddSettings | Industries | capacidades-setoriais | media / media |
| GatewayProviderPaymentMethodType | Commerce | receita-e-comercio | media / media |
| GenComputingSummaryDef | IA, Agentforce e Einstein | prompts | media / media |
| GenOpAgentConfig | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| GenOpPlanEligibilityConfig | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| GeneralConfigSettings | Plataforma (candidato ao Core) | habilitacao-de-recursos | baixa / baixa |
| GenerativeCampaignsSettings | IA, Agentforce e Einstein | prompts | media / media |
| GeocodeSettings | Plataforma (candidato ao Core) | localizacao-idiomas-e-traducao | baixa / alta |
| GiftEntryGridTemplate | Industries | capacidades-setoriais | media / media |
| GlobalConsentDefinition | Plataforma com licença ou add-on provável | consentimento-e-privacidade | baixa / alta |
| GlobalConsentExtendedAttribute | Plataforma com licença ou add-on provável | consentimento-e-privacidade | baixa / alta |
| GlobalConsentManagementLayout | Plataforma com licença ou add-on provável | consentimento-e-privacidade | baixa / alta |
| GlobalConsentPurpose | Plataforma com licença ou add-on provável | consentimento-e-privacidade | baixa / alta |
| GlobalConsentStatus | Plataforma com licença ou add-on provável | consentimento-e-privacidade | baixa / alta |
| GlobalValueSet | Plataforma (candidato ao Core) | listas-de-valores | baixa / alta |
| GlobalValueSetTranslation | Plataforma (candidato ao Core) | listas-de-valores | baixa / alta |
| GoogleAppsSettings | Plataforma (candidato ao Core) | chamadas-externas-e-endpoints | baixa / media |
| HealthInsDataSyncDefn | Industries | capacidades-setoriais | media / media |
| HerokuAppLinkSettings | Plataforma com licença ou add-on provável | conectividade-e-virtualizacao-de-dados | baixa / media |
| HighVelocitySalesSettings | Sales Cloud | vendas | media / media |
| HomePageComponent | Produto aposentado ou legado | layouts-e-paginas-de-registro | media / media |
| HomePageLayout | Produto aposentado ou legado | layouts-e-paginas-de-registro | media / media |
| HouseholdNamingConfig | Industries | capacidades-setoriais | media / media |
| HouseholdUiConfiguration | Industries | capacidades-setoriais | media / media |
| IPAddressRange | Plataforma (candidato ao Core) | sessoes-e-politicas-de-login | baixa / alta |
| IdeasSettings | Produto aposentado ou legado | colaboracao | media / media |
| IdentityRsolDataSyncDef | Industries | duplicidade-e-correspondencia | media / media |
| IdpConfiguration | Plataforma (candidato ao Core) | autenticacao-sso-e-mfa | baixa / media |
| IncludeEstTaxInQuoteCPQSettings | Service Cloud | receita-e-comercio | media / media |
| IncludeEstTaxInQuoteSettings | Service Cloud | receita-e-comercio | media / media |
| IndustriesAutomotiveSettings | Industries | capacidades-setoriais | media / media |
| IndustriesChannelPartnerInventorySettings | Industries | receita-e-comercio | media / media |
| IndustriesCommunicationsSalesSettings | Industries | capacidades-setoriais | media / media |
| IndustriesConnectedServiceSettings | Industries | capacidades-setoriais | media / media |
| IndustriesConstraintsSettings | Industries | decisoes-e-aprovacoes | media / media |
| IndustriesContextSettings | Industries | capacidades-setoriais | media / media |
| IndustriesEinsteinFeatureSettings | Industries | capacidades-setoriais | media / media |
| IndustriesEnergyUtilitiesMultiSiteSettings | Industries | capacidades-setoriais | media / media |
| IndustriesEventOrchSettings | Industries | flow-e-orquestracao | media / alta |
| IndustriesGamificationSettings | Industries | capacidades-setoriais | media / media |
| IndustriesInsuranceSettings | Industries | capacidades-setoriais | media / media |
| IndustriesLoyaltySettings | Industries | capacidades-setoriais | media / media |
| IndustriesLsCommercialSettings | Industries | capacidades-setoriais | media / media |
| IndustriesMaczPricingSettings | Industries | capacidades-setoriais | media / media |
| IndustriesManufacturingSettings | Industries | capacidades-setoriais | media / media |
| IndustriesMfgAdvnOrderSettings | Industries | capacidades-setoriais | media / media |
| IndustriesMfgSampleManagementSettings | Industries | capacidades-setoriais | media / media |
| IndustriesRatingSettings | Industries | receita-e-comercio | media / media |
| IndustriesRepossessionSettings | Industries | capacidades-setoriais | media / media |
| IndustriesUnifiedInventorySettings | Industries | receita-e-comercio | media / media |
| IndustriesUnifiedPromotionsSettings | Industries | capacidades-setoriais | media / media |
| IndustriesUsageSettings | Industries | receita-e-comercio | media / media |
| InsBillingConfig | Industries | capacidades-setoriais | media / media |
| InsPlcyCoverageSpecConfig | Industries | capacidades-setoriais | media / media |
| InsPlcyLimitConsumptionRule | Industries | capacidades-setoriais | media / media |
| InsPlcyLineOfBusConfig | Industries | capacidades-setoriais | media / media |
| InsPolicyLifecycleConfig | Industries | capacidades-setoriais | media / media |
| InsPolicyManagementConfig | Industries | capacidades-setoriais | media / media |
| InsRatePlanCmsnConfig | Industries | capacidades-setoriais | media / media |
| InsRatePlanTypeConfig | Industries | capacidades-setoriais | media / media |
| InsuranceBrokerageSettings | Industries | capacidades-setoriais | media / media |
| InsuranceUnderwriterSettings | Industries | capacidades-setoriais | media / media |
| IntegArtifactDef | Plataforma (candidato ao Core) | conectividade-e-virtualizacao-de-dados | baixa / media |
| IntegratedPlanDefinition | Industries | capacidades-setoriais | media / media |
| IntegrationProviderDef | Plataforma (candidato ao Core) | conectividade-e-virtualizacao-de-dados | baixa / media |
| InterestTaggingSettings | Marketing | capacidades-setoriais | media / media |
| InvLatePymntRiskCalcSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| InvMgmtForUnusableQtySettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| InventoryAllocationSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| InventorySettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| InvocableActionExtension | Plataforma (candidato ao Core) | codigo-e-bundles | baixa / media |
| IoTSettings | Plataforma com licença ou add-on provável | habilitacao-de-recursos | baixa / baixa |
| KnowledgeGenerationSettings | IA, Agentforce e Einstein | prompts | media / media |
| LaborCostOptimCrewMgmtSettings | Field Service | servico-de-campo | media / media |
| LaborCostOptimizationSettings | Field Service | servico-de-campo | media / media |
| LargeQuotesandOrdersForRlmSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| LeadScoreSettings | Sales Cloud | modelos-e-grounding | media / media |
| LearningAchievementConfig | Industries | capacidades-setoriais | media / media |
| LearningItemType | Industries | capacidades-setoriais | media / media |
| LicensingSettings | Plataforma (candidato ao Core) | licencas-e-entitlements-de-acesso | baixa / media |
| LifeSciConfigCategory | Industries | capacidades-setoriais | media / media |
| LifeSciConfigRecord | Industries | capacidades-setoriais | media / media |
| LightningBolt | Plataforma (candidato ao Core) | codigo-e-bundles | baixa / media |
| LightningMessageChannel | Plataforma (candidato ao Core) | eventos-e-mensageria | baixa / media |
| LightningOnboardingConfig | Plataforma (candidato ao Core) | aplicativos-e-navegacao | baixa / media |
| LightningOutApp | Plataforma (candidato ao Core) | conectividade-e-virtualizacao-de-dados | baixa / media |
| LightningTypeBundle | Plataforma (candidato ao Core) | codigo-e-bundles | baixa / media |
| LocationUse | Field Service | servico-de-campo | media / media |
| LogicSettings | Plataforma (candidato ao Core) | decisoes-e-aprovacoes | baixa / media |
| LoyaltyProgramSetup | Industries | capacidades-setoriais | media / media |
| MCETransformationsSettings | Marketing | outras-areas | media / baixa |
| MailAppOwaWhitelist | Produto aposentado ou legado | sessoes-e-politicas-de-login | media / alta |
| MailMergeSettings | Produto aposentado ou legado | templates-e-comunicacao | media / media |
| ManagedContentType | Plataforma (candidato ao Core) | bibliotecas-e-assets | baixa / media |
| MapReportSettings | Plataforma (candidato ao Core) | reports | baixa / media |
| MapsAndLocationSettings | Plataforma (candidato ao Core) | localizacao-idiomas-e-traducao | baixa / alta |
| MarketSegment | Marketing | outras-areas | media / baixa |
| MarketSegmentActivation | Marketing | outras-areas | media / baixa |
| MarketSegmentDefinition | Marketing | outras-areas | media / baixa |
| MarketingAppExtActivity | Marketing | outras-areas | media / baixa |
| MarketingAppExtension | Marketing | outras-areas | media / baixa |
| MarketingHierarchyGroupDef | Marketing | outras-areas | media / baixa |
| MarketingHierarchyGroupNodeDef | Marketing | outras-areas | media / baixa |
| MarketingHierarchyNodeDef | Marketing | outras-areas | media / baixa |
| McpServerDefinition | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| MediaAdSalesSettings | Industries | capacidades-setoriais | media / media |
| MediaAgentSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| MeetingPlaybookDefinition | Sales Cloud | vendas | media / media |
| MeetingsSettings | Sales Cloud | colaboracao | media / media |
| MessagingMobileAppChannel | Service Cloud | atendimento | media / media |
| MessagingMobileAppChannelButton | Service Cloud | atendimento | media / media |
| MessagingMobileAppChannelButtonSet | Service Cloud | atendimento | media / media |
| MfgProgramTemplate | Industries | capacidades-setoriais | media / media |
| MfgServiceConsoleSettings | Industries | capacidades-setoriais | media / media |
| MissionforceLogisticsSettings | Field Service | servico-de-campo | media / media |
| MissionforceSettings | Field Service | servico-de-campo | media / media |
| MktPlanningOpsSettings | Marketing | vendas | media / media |
| MlDomain | IA, Agentforce e Einstein | modelos-e-grounding | media / media |
| MobSecurityCertPinConfig | Plataforma (candidato ao Core) | sessoes-e-politicas-de-login | baixa / alta |
| MobileAppNewsflashTopic | Plataforma (candidato ao Core) | notificacoes | baixa / alta |
| MobileApplicationDetail | Plataforma (candidato ao Core) | experiencias-web-portais-e-mobile | baixa / media |
| MobilePublisherAppConfig | Plataforma com licença ou add-on provável | experiencias-web-portais-e-mobile | baixa / media |
| MobilePublisherAppVersion | Plataforma com licença ou add-on provável | experiencias-web-portais-e-mobile | baixa / media |
| MobilePublisherDelegateDistributionAccount | Plataforma com licença ou add-on provável | experiencias-web-portais-e-mobile | baixa / media |
| MobilePublisherPrivateDistributionAccount | Plataforma com licença ou add-on provável | experiencias-web-portais-e-mobile | baixa / media |
| MobilePublisherProject | Plataforma com licença ou add-on provável | experiencias-web-portais-e-mobile | baixa / media |
| MobileSecurityAssignment | Plataforma (candidato ao Core) | sessoes-e-politicas-de-login | baixa / alta |
| MobileSecurityPolicy | Plataforma (candidato ao Core) | sessoes-e-politicas-de-login | baixa / alta |
| MsTeamsAppSettings | Plataforma (candidato ao Core) | chamadas-externas-e-endpoints | baixa / media |
| MutingPermissionSet | Plataforma (candidato ao Core) | permissoes-perfis-e-grupos | baixa / alta |
| MyDomainDiscoverableLogin | Plataforma (candidato ao Core) | sessoes-e-politicas-de-login | baixa / alta |
| NetworkBranding | Experience Cloud | experiencias-externas | alta / alta |
| NotificationTypeConfig | Plataforma (candidato ao Core) | notificacoes | baixa / alta |
| NotificationsSettings | Plataforma (candidato ao Core) | notificacoes | baixa / alta |
| ObjIntegProviderDefMapping | Plataforma (candidato ao Core) | conectividade-e-virtualizacao-de-dados | baixa / media |
| ObjectFieldValueMapping | Industries | metadados-de-configuracao-de-dados | media / media |
| ObjectHierarchyRelationship | Plataforma (candidato ao Core) | relacionamentos-e-juncoes | baixa / media |
| ObjectLinkingSettings | Plataforma (candidato ao Core) | relacionamentos-e-juncoes | baixa / media |
| ObjectMappingSettings | Plataforma (candidato ao Core) | metadados-de-configuracao-de-dados | baixa / media |
| ObjectSourceTargetMap | Industries | metadados-de-configuracao-de-dados | media / media |
| OcrSampleDocument | Plataforma com licença ou add-on provável | files-e-documentos | baixa / media |
| OcrTemplate | Plataforma com licença ou add-on provável | files-e-documentos | baixa / media |
| OmniChannelPricingSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| OmniUiCard | Industries | layouts-e-paginas-de-registro | media / media |
| OnboardingDataObjectGroup | Industries | metadados-de-configuracao-de-dados | media / media |
| OnlineSalesSettings | Commerce | receita-e-comercio | media / media |
| OpportunityScoreSettings | Sales Cloud | modelos-e-grounding | media / media |
| OptimizationSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| OrchestrationPlanCtxMapping | Industries | flow-e-orquestracao | media / alta |
| OrderManagementSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| PardotEinsteinSettings | Produto aposentado ou legado | outras-areas | media / baixa |
| PardotSettings | Produto aposentado ou legado | outras-areas | media / baixa |
| ParticipantRole | Industries | capacidades-setoriais | media / media |
| PartyDataModelSettings | Industries | metadados-de-configuracao-de-dados | media / media |
| PartyProfileDataObjectValidityDefinition | Industries | metadados-de-configuracao-de-dados | media / media |
| PaymentGatewayProvider | Commerce | receita-e-comercio | media / media |
| PaymentsManagementEnabledSettings | Commerce | receita-e-comercio | media / media |
| PaymentsSettings | Commerce | receita-e-comercio | media / media |
| PaymentsSharingSettings | Commerce | acesso-a-registros-e-hierarquias | media / alta |
| PaynowStarterUpgradeEnabledSettings | Commerce | receita-e-comercio | media / media |
| PermissionSetLicenseDefinition | Plataforma (candidato ao Core) | licencas-e-entitlements-de-acesso | baixa / media |
| PersonAccountOwnerPowerUser | Plataforma (candidato ao Core) | acesso-a-registros-e-hierarquias | baixa / alta |
| PipelineInspMetricConfig | Sales Cloud | recursos-analiticos-de-produto | media / media |
| PlanningDimensionDef | Sales Cloud | vendas | media / media |
| PlanningMeasureDef | Sales Cloud | vendas | media / media |
| PlanningMeasureGroup | Sales Cloud | vendas | media / media |
| PlatformCachePartition | Plataforma (candidato ao Core) | sem pista | baixa / sem_pista |
| PlatformEventMigration | Produto aposentado ou legado | mecanismos-legados-e-migracao | media / alta |
| PlatformSlackSettings | Slack | chamadas-externas-e-endpoints | media / media |
| PlatformWebIdeSettings | Plataforma (candidato ao Core) | versionamento-deploy-e-recuperacao | baixa / media |
| PolicyRuleDefinition | Industries | decisoes-e-aprovacoes | media / media |
| PolicyRuleDefinitionSet | Industries | decisoes-e-aprovacoes | media / media |
| PortalDelegablePermissionSet | Experience Cloud | permissoes-perfis-e-grupos | alta / alta |
| PortalsSettings | Experience Cloud | experiencias-externas | alta / alta |
| PostTemplate | Plataforma (candidato ao Core) | templates-e-comunicacao | baixa / media |
| PredictionBuilderSettings | IA, Agentforce e Einstein | modelos-e-grounding | media / media |
| PrivacyAgentSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| PrivacyOrgConfig | Plataforma com licença ou add-on provável | consentimento-e-privacidade | baixa / alta |
| PrmCoreSettings | Sales Cloud | vendas | media / media |
| ProcedurePlanDefinition | Service Cloud | atendimento | media / media |
| ProcessFlowMigration | Produto aposentado ou legado | mecanismos-legados-e-migracao | media / alta |
| ProductAttrDisplayConfig | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| ProductAttributeSet | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| ProductCatalogManagementSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| ProductConfiguratorSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| ProductDiscoverySettings | Commerce | receita-e-comercio | media / media |
| ProductSpecificationRecType | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| ProductSpecificationType | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| ProfilePasswordPolicy | Plataforma (candidato ao Core) | sessoes-e-politicas-de-login | baixa / alta |
| ProfileSessionSetting | Plataforma (candidato ao Core) | sessoes-e-politicas-de-login | baixa / alta |
| Prompt | IA, Agentforce e Einstein | prompts | media / media |
| ProviderSampleLimitTemplate | Industries | capacidades-setoriais | media / media |
| PurchaseOrderMgmtSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| QualityManagementSettings | Industries | capacidades-setoriais | media / media |
| QuickTextSettings | Plataforma (candidato ao Core) | templates-e-comunicacao | baixa / media |
| RealTimeEventSettings | Plataforma com licença ou add-on provável | eventos-de-monitoramento | baixa / media |
| RebateAndAccrualMgmtAdvncdSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| RecAlrtDataSrcExpSetDef | Industries | notificacoes | media / alta |
| RecLifecyclCompanCpblDef | Industries | capacidades-setoriais | media / media |
| RecLifecyclCompanDef | Industries | capacidades-setoriais | media / media |
| RecommendationBuilderSettings | IA, Agentforce e Einstein | acoes-e-topicos | media / media |
| RecommendationStrategy | IA, Agentforce e Einstein | acoes-e-topicos | media / media |
| RecordActionDeployment | Plataforma (candidato ao Core) | acoes-e-regras | baixa / media |
| RecordAggregationDefinition | Plataforma (candidato ao Core) | metadados-de-configuracao-de-dados | baixa / media |
| RecordAlertCategory | Industries | notificacoes | media / alta |
| RecordAlertDataSource | Industries | notificacoes | media / alta |
| RecordAlertTemplate | Industries | notificacoes | media / alta |
| RecordCompanionSettings | Industries | capacidades-setoriais | media / media |
| RedirectWhitelistUrl | Plataforma (candidato ao Core) | sessoes-e-politicas-de-login | baixa / alta |
| ReferencedDashboard | Plataforma (candidato ao Core) | dashboards | baixa / media |
| ReferralIntakeConfiguration | Industries | capacidades-setoriais | media / media |
| ReferralManagementSettings | Industries | capacidades-setoriais | media / media |
| ReferralMarketingConfig | Marketing | outras-areas | media / baixa |
| ReferralMarketingSettings | Marketing | outras-areas | media / baixa |
| ReferralReceiverConfiguration | Industries | capacidades-setoriais | media / media |
| RegltCntntActnDef | Industries | capacidades-setoriais | media / media |
| RegltCntntActnTgtDef | Industries | capacidades-setoriais | media / media |
| RegltCntntPolicyDef | Industries | capacidades-setoriais | media / media |
| RegltCntntProcDef | Industries | capacidades-setoriais | media / media |
| RegltCntntProcStsDef | Industries | capacidades-setoriais | media / media |
| RegltCntntRoleDef | Industries | capacidades-setoriais | media / media |
| RegltCntntStsDef | Industries | capacidades-setoriais | media / media |
| RegltCntntTypeDef | Industries | capacidades-setoriais | media / media |
| RegltCntntTypeRoleDef | Industries | capacidades-setoriais | media / media |
| RelatedRecordAccessDef | Plataforma (candidato ao Core) | acesso-a-registros-e-hierarquias | baixa / alta |
| RelatedRecordAssocCriteria | Industries | capacidades-setoriais | media / media |
| RelationshipGraphDefinition | Plataforma (candidato ao Core) | relacionamentos-e-juncoes | baixa / media |
| ReleaseMgmtSettings | Plataforma (candidato ao Core) | versionamento-deploy-e-recuperacao | baixa / media |
| ReplyEmailConfig | Plataforma (candidato ao Core) | templates-e-comunicacao | baixa / media |
| RestrictionRule | Plataforma (candidato ao Core) | acesso-a-registros-e-hierarquias | baixa / alta |
| RetailExecutionSettings | Industries | capacidades-setoriais | media / media |
| RetrievalSummaryDefinition | IA, Agentforce e Einstein | recuperacao-de-conhecimento | media / media |
| RiskMgmtSettings | Industries | capacidades-setoriais | media / media |
| SalesAgreementSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| SalesBotsSettings | Sales Cloud | configuracao-de-agentes | media / media |
| SalesCloudSurfacesSettings | Sales Cloud | vendas | media / media |
| SalesDealAgentSettings | Sales Cloud | configuracao-de-agentes | media / media |
| SalesEmailAssistantSettings | Sales Cloud | prompts | media / media |
| SalesPlanDataSource | Sales Cloud | vendas | media / media |
| SalesWorkQueueSettings | Sales Cloud | vendas | media / media |
| SceGlobalModelOptOutSettings | IA, Agentforce e Einstein | seguranca-avaliacao-e-governanca-de-ia | media / media |
| SchedulingPolicy | Field Service | servico-de-campo | media / media |
| SchedulingRecipeSettings | Field Service | servico-de-campo | media / media |
| ScndTelephPrvdOtbdDtl | Service Cloud | atendimento | media / media |
| ScopedAccess | Plataforma (candidato ao Core) | acesso-a-registros-e-hierarquias | baixa / alta |
| SearchCustomization | Plataforma (candidato ao Core) | aplicativos-e-navegacao | baixa / media |
| SearchOrgWideObjectConfig | Plataforma (candidato ao Core) | aplicativos-e-navegacao | baixa / media |
| SecondaryTelephonyProvider | Service Cloud | atendimento | media / media |
| SecurityAgentSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| SecurityCustomBaseline | Plataforma com licença ou add-on provável | credenciais-certificados-e-protecao-de-dados | baixa / media |
| SecurityHubSettings | Plataforma com licença ou add-on provável | credenciais-certificados-e-protecao-de-dados | baixa / media |
| SecuritySignalWorkspace | Plataforma com licença ou add-on provável | credenciais-certificados-e-protecao-de-dados | baixa / media |
| SelfServiceSettings | Experience Cloud | experiencias-externas | alta / alta |
| SelfSvcPortalTopic | Experience Cloud | experiencias-externas | alta / alta |
| SensitiveDataRuleElmntGrp | Plataforma com licença ou add-on provável | classificacao-e-sensibilidade | baixa / media |
| SequenceServiceSettings | Sales Cloud | vendas | media / media |
| ServiceAIRecommendationsSettings | Service Cloud | acoes-e-topicos | media / media |
| ServiceAISetupDefinition | Service Cloud | configuracao-de-agentes | media / media |
| ServiceAISetupField | Service Cloud | configuracao-de-agentes | media / media |
| ServiceCatalogSettings | Service Cloud | atendimento | media / media |
| ServiceCloudNotificationOrchestratorSettings | Service Cloud | flow-e-orquestracao | media / alta |
| ServiceHamSettings | Service Cloud | atendimento | media / media |
| ServiceHeliosSettings | Service Cloud | atendimento | media / media |
| ServiceIssueManagementSettings | Service Cloud | atendimento | media / media |
| ServiceItamSettings | Service Cloud | atendimento | media / media |
| ServiceItomSettings | Service Cloud | atendimento | media / media |
| ServiceItsmChangeManagementSettings | Service Cloud | atendimento | media / media |
| ServiceItsmIntelligenceUddSettings | Service Cloud | atendimento | media / media |
| ServiceLegalStatusesSettings | Service Cloud | atendimento | media / media |
| ServiceMgmtKnwlgArtclConfig | Service Cloud | knowledge-e-categorias | media / media |
| ServiceMgmtKnwlgArtclConfigSettings | Service Cloud | knowledge-e-categorias | media / media |
| ServiceProcess | Service Cloud | atendimento | media / media |
| ServiceProcessSettings | Service Cloud | atendimento | media / media |
| ServiceRepAssistantSettings | Service Cloud | configuracao-de-agentes | media / media |
| ServiceScheduleConfig | Field Service | servico-de-campo | media / media |
| SetupCopilotSettings | IA, Agentforce e Einstein | configuracao-de-agentes | media / media |
| SharingSet | Experience Cloud | acesso-a-registros-e-hierarquias | alta / alta |
| Skill | Service Cloud | atendimento | media / media |
| SkillType | Service Cloud | atendimento | media / media |
| SlackApp | Slack | chamadas-externas-e-endpoints | media / media |
| SlackAppTemplate | Slack | chamadas-externas-e-endpoints | media / media |
| SoFieldMappingSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| SpiffSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| SrvcMgmtCollabAppFldDef | Service Cloud | atendimento | media / media |
| SrvcMgmtCollabAppObjDef | Service Cloud | atendimento | media / media |
| SrvcMgmtObjCollabAppCnfg | Service Cloud | atendimento | media / media |
| StageAssignment | Sales Cloud | vendas | media / media |
| StageDefinition | Sales Cloud | vendas | media / media |
| StandardValue | Plataforma (candidato ao Core) | listas-de-valores | baixa / alta |
| StandardValueSet | Plataforma (candidato ao Core) | listas-de-valores | baixa / alta |
| StandardValueSetTranslation | Plataforma (candidato ao Core) | listas-de-valores | baixa / alta |
| StatisticalDealInsightsSettings | Sales Cloud | recursos-analiticos-de-produto | media / media |
| StockRotationSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| StreamingAppDataConnector | Data 360 | modelos-externos-e-especializacoes | baixa / baixa |
| SubscriptionManagementSettings | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| SurveySettings | Plataforma com licença ou add-on provável | colaboracao | baixa / media |
| SurveyStyleSet | Plataforma com licença ou add-on provável | colaboracao | baixa / media |
| SvcCatalogCategory | Service Cloud | atendimento | media / media |
| SvcCatalogFilterCriteria | Service Cloud | atendimento | media / media |
| SvcCatalogFulfillmentFlow | Service Cloud | atendimento | media / media |
| SvcCatalogItemDef | Service Cloud | atendimento | media / media |
| SynchronizeSettings | Plataforma (candidato ao Core) | conectividade-e-virtualizacao-de-dados | baixa / media |
| SynonymDictionary | Plataforma (candidato ao Core) | knowledge-e-categorias | baixa / media |
| SystemNotificationSettings | Plataforma (candidato ao Core) | notificacoes | baixa / alta |
| Tag | Plataforma (candidato ao Core) | colaboracao | baixa / media |
| TagSet | Plataforma (candidato ao Core) | colaboracao | baixa / media |
| TelemetryActionDefStep | Plataforma (candidato ao Core) | eventos-de-monitoramento | baixa / media |
| TelemetryActionDefinition | Plataforma (candidato ao Core) | eventos-de-monitoramento | baixa / media |
| TelemetryActnDefStepAttr | Plataforma (candidato ao Core) | eventos-de-monitoramento | baixa / media |
| TelemetryDefinition | Plataforma (candidato ao Core) | eventos-de-monitoramento | baixa / media |
| TelemetryDefinitionVersion | Plataforma (candidato ao Core) | eventos-de-monitoramento | baixa / media |
| TelephonyProvider | Service Cloud | atendimento | media / media |
| TenantSecurityPlaybookDef | Plataforma com licença ou add-on provável | credenciais-certificados-e-protecao-de-dados | baixa / media |
| TenantSecurityPlaybookDefStep | Plataforma com licença ou add-on provável | credenciais-certificados-e-protecao-de-dados | baixa / media |
| TenantSecurityPlaybookDefVer | Plataforma com licença ou add-on provável | credenciais-certificados-e-protecao-de-dados | baixa / media |
| TenantSecurityStepDef | Plataforma com licença ou add-on provável | credenciais-certificados-e-protecao-de-dados | baixa / media |
| TenantSecurityStepDefVer | Plataforma com licença ou add-on provável | credenciais-certificados-e-protecao-de-dados | baixa / media |
| Territory | Sales Cloud | vendas | media / media |
| ThunderbirdVoiceSettings | Produto aposentado ou legado | atendimento | media / media |
| TmfOutboundNotificationSettings | Industries | notificacoes | media / alta |
| TmshtLaborCostOptimAiSettings | Field Service | servico-de-campo | media / media |
| TopicsForObjects | Experience Cloud | colaboracao | alta / media |
| TrailheadSettings | Plataforma (candidato ao Core) | habilitacao-de-recursos | baixa / baixa |
| TransactableMarketplacePrivateOfferSettings | Commerce | receita-e-comercio | media / media |
| TransactionProcessingType | Revenue, CPQ e Billing | receita-e-comercio | media / media |
| TransactionSecurityPolicy | Plataforma com licença ou add-on provável | sessoes-e-politicas-de-login | baixa / alta |
| TrialOrgSettings | Plataforma (candidato ao Core) | versionamento-deploy-e-recuperacao | baixa / media |
| TriggerConfigurationsSettings | Plataforma (candidato ao Core) | acoes-e-regras | baixa / media |
| TrustedTelephonyProvider | Service Cloud | atendimento | media / media |
| UIBundle | Plataforma (candidato ao Core) | codigo-e-bundles | baixa / media |
| UIBundleSettings | Plataforma (candidato ao Core) | codigo-e-bundles | baixa / media |
| UiFormatSpecificationSet | Plataforma (candidato ao Core) | layouts-e-paginas-de-registro | baixa / media |
| UiPlugin | Plataforma (candidato ao Core) | codigo-e-bundles | baixa / media |
| UiPreviewMessageTabDef | Plataforma (candidato ao Core) | layouts-e-paginas-de-registro | baixa / media |
| UiWidgetBundle | Plataforma (candidato ao Core) | codigo-e-bundles | baixa / media |
| UiWidgetSettings | Plataforma (candidato ao Core) | layouts-e-paginas-de-registro | baixa / media |
| UnifiedSalesIntelligenceSettings | Sales Cloud | recursos-analiticos-de-produto | media / media |
| UserAccessPolicy | Plataforma (candidato ao Core) | usuarios-e-provisionamento | baixa / media |
| UserCriteria | Plataforma (candidato ao Core) | usuarios-e-provisionamento | baixa / media |
| UserProvisioningConfig | Plataforma (candidato ao Core) | usuarios-e-provisionamento | baixa / media |
| ViewDefinition | Plataforma (candidato ao Core) | aplicativos-e-navegacao | baixa / media |
| VoceEngmtMediaLblObjAsgnt | Service Cloud | atendimento | media / media |
| VoiceEngagementMediaFile | Service Cloud | atendimento | media / media |
| VoiceEngagementMediaUsage | Service Cloud | atendimento | media / media |
| VoiceEngmtMediaFileAsgnt | Service Cloud | atendimento | media / media |
| VoiceSettings | Service Cloud | atendimento | media / media |
| VoiceWorkflowDefinition | Service Cloud | flow-e-orquestracao | media / alta |
| VoiceWorkflowVersion | Service Cloud | flow-e-orquestracao | media / alta |
| WarrantyLifecycleMgmtSettings | Industries | capacidades-setoriais | media / media |
| WaveAnalyticAssetCollection | Analytics (CRM Analytics / Tableau) | recursos-analiticos-de-produto | media / media |
| Web3Settings | Produto aposentado ou legado | habilitacao-de-recursos | media / baixa |
| WebStoreBundle | Commerce | receita-e-comercio | media / media |
| WebStoreTemplate | Commerce | receita-e-comercio | media / media |
| WebToXSettings | Plataforma (candidato ao Core) | experiencias-web-portais-e-mobile | baixa / media |
| WinProbabilityScoringSetup | Sales Cloud | modelos-e-grounding | media / media |
| WorkDotComSettings | Produto aposentado ou legado | outras-areas | media / baixa |
| WorkflowSend | Produto aposentado ou legado | mecanismos-legados-e-migracao | media / alta |
| WorkforceManagementSettings | Field Service | servico-de-campo | media / media |
| WorkforceSchedulingSettings | Field Service | servico-de-campo | media / media |
