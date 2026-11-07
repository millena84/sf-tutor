Tratar isso como um **catálogo mestre por domínio de produto**, não como uma lista única de metadata types. Motivo técnico: o **core Salesforce** usa principalmente Metadata API; **Marketing Cloud, B2C Commerce, MuleSoft, Tableau e Slack** possuem configurações e artefatos próprios, expostos por APIs, importações, pacotes ou consoles específicos. A referência oficial do core é a lista de *Metadata Types* do Metadata API. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm)

Abaixo está o catálogo completo no nível adequado para montar tutorial, glossário e material de consulta. Ele cobre o **core Salesforce no maior escopo de licenciamento** e os produtos que normalmente ficam em **instâncias/contas separadas**.

***

# 1. Organização e metadados-base do CORE

Estes tipos definem a org, seu comportamento global, idiomas, moedas, domínio e configurações transversais. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `Organization` | Organização, informações da empresa, moeda padrão, fuso, idioma |
| `Settings` | Família de configurações de produto/org no package manifest |
| `OrgPreferenceSettings` | Preferências da organização |
| `CompanySettings` | Dados da empresa e configurações corporativas |
| `MyDomainSettings` | My Domain, URL da org, login e branding |
| `DomainSettings` | Domínios customizados |
| `LanguageSettings` | Idiomas habilitados e idioma padrão |
| `TranslationSettings` | Traduções e configuração de tradução |
| `Translations` | Arquivo de traduções |
| `Translation` | Tradução de metadados |
| `CustomLabels` | Conjunto de rótulos traduzíveis |
| `CustomLabel` | Rótulo individual reutilizável |
| `CustomLabelTranslation` | Tradução de rótulo |
| `CurrencyType` | Moedas habilitadas |
| `AdvancedCurrencyManagementSettings` | Moedas, taxas e datas efetivas |
| `DatedConversionRate` | Taxa de conversão por data |
| `FiscalYearSettings` | Calendário fiscal |
| `ForecastingSettings` | Forecasting |
| `ForecastingType` | Tipos de forecast |
| `ForecastingCategory` | Categorias de forecast |
| `BusinessHoursSettings` | Horário comercial |
| `HolidaySettings` | Feriados |
| `SearchSettings` | Busca global e configurações de pesquisa |
| `SearchPromotionRule` | Regras de promoção em busca |
| `SynonymDictionary` | Sinônimos para busca |
| `KnowledgeSettings` | Knowledge |
| `DataCategoryGroup` | Categorias de dados para Knowledge |
| `DataCategoryGroupReference` | Referência a categorias |
| `ContentSettings` | Files, Content e biblioteca de conteúdo.  |
| `ContentAsset` | Asset de conteúdo reutilizável |
| `ContentVersion` | Versão de arquivo |
| `Document` | Documento em pasta |
| `Folder` | Pasta de documentos, relatórios, dashboards e e-mails |
| `ReportFolder` | Pasta de relatórios |
| `DashboardFolder` | Pasta de dashboards |
| `EmailFolder` | Pasta de templates de e-mail |
| `ScontrolFolder` | Pasta de S-controls legados |
| `NetworkBranding` | Branding de Experience Cloud |
| `BrandingSet` | Conjunto de branding |
| `BrandingSetProperty` | Propriedade de branding |
| `LightningExperienceSettings` | Lightning Experience |
| `LightningExperienceTheme` | Tema Lightning |
| `LightningOnboardingConfig` | Onboarding Lightning |
| `MobileSettings` | Configurações mobile |
| `MobileApplicationDetail` | Detalhe de app mobile |
| `ConnectedAppSettings` | Connected Apps |
| `DevHubSettings` | Dev Hub |
| `ScratchOrgInfo` | Informações de Scratch Org |
| `SourceTrackingSettings` | Source tracking |
| `ReleaseManagementSettings` | Release management |
| `DeploymentSettings` | Deploy |
| `PackageSettings` | Pacotes |
| `UserInterfaceSettings` | Interface |
| `UserEngagementSettings` | Engajamento do usuário |
| `PathAssistantSettings` | Path |
| `ActivitiesSettings` | Tarefas, eventos e calendário |
| `ActivitySettings` | Atividades |
| `CalendarSettings` | Calendário |
| `EventSettings` | Eventos |
| `TaskSettings` | Tarefas |

***

# 2. Dados, objetos e modelo relacional

Este é o núcleo do modelo de dados do core. `CustomObject` representa objetos customizados e também objetos externos mapeados a dados fora da org. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customobject.htm)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `CustomObject` | Objeto customizado, external object, configurações de comportamento e sharing |
| `CustomField` | Campo em objeto padrão, customizado ou externo |
| `CustomObjectTranslation` | Tradução de objeto |
| `CustomFieldTranslation` | Tradução de campo |
| `RecordType` | Tipos de registro |
| `BusinessProcess` | Processos de Lead, Opportunity, Case e Solution |
| `BusinessProcess` + `RecordType` | Picklists e processos por tipo de registro |
| `PathAssistant` | Path por objeto/record type |
| `GlobalValueSet` | Picklist global |
| `GlobalValueSetTranslation` | Tradução de picklist global |
| `StandardValueSet` | Picklist padrão |
| `StandardValueSetTranslation` | Tradução de picklist padrão |
| `RestrictedPicklist` | Restrição de valores |
| `DependentPicklist` | Dependência entre picklists |
| `NamedFilter` | Lookup filter.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_contentsettings.htm) |
| `ValidationRule` | Validação de dados |
| `DuplicateRule` | Regra de duplicidade |
| `MatchingRule` | Regra de correspondência |
| `DuplicateJobMatchingRule` | Regra usada em job de duplicidade |
| `CleanDataService` | Serviço de limpeza/enriquecimento |
| `FieldSet` | Conjunto de campos |
| `CompactLayout` | Layout compacto |
| `ListView` | Visão de lista |
| `SearchLayouts` | Layouts de busca e lookup |
| `WebLink` | Botão/link customizado |
| `CustomPageWebLink` | Link customizado |
| `QuickAction` | Ação rápida |
| `GlobalAction` | Ação global |
| `GlobalQuickAction` | Ação rápida global |
| `CustomHelpMenuSection` | Ajuda contextual |
| `TopicsForObjects` | Topics em objeto |
| `ManagedTopics` | Tópicos gerenciados |
| `DataCategoryGroup` | Categorias de dados |
| `BigObject` | Objeto de grande volume |
| `Index` | Índice customizado |
| `ExternalDataSource` | Fonte externa via Salesforce Connect |
| `ExternalObject` | Objeto externo |
| `ExternalDataConnector` | Conector de dados externos |
| `ExternalDataConnectorConfig` | Configuração do conector |
| `ObjectMapping` | Mapeamento entre objetos |
| `CustomMetadataType` | Definição de Custom Metadata Type |
| `CustomMetadata` | Registro de Custom Metadata Type |
| `CustomSetting` | Custom Setting |
| `CustomSettings` | Família de custom settings |
| `HierarchySettings` | Custom Setting hierárquico |
| `ListSetting` | Custom Setting de lista |
| `CustomNotificationType` | Tipo de notificação |
| `DataWeaveResource` | Recurso DataWeave |
| `DataPipeline` | Pipeline de dados |
| `DataRaptor` | DataRaptor OmniStudio |
| `DataTransform` | Transformação de dados |
| `DataCloudDataModelObject` | Objeto do modelo de dados Data Cloud |
| `DataCloudDataStream` | Data stream do Data Cloud |
| `DataCloudIdentityResolution` | Identity Resolution |
| `DataCloudSegment` | Segmento |
| `DataCloudActivation` | Ativação de segmento |
| `DataCloudCalculatedInsight` | Calculated Insight |
| `DataCloudDataGraph` | Data Graph |
| `CustomerDataPlatformSettings` | Configurações do Data Cloud.  |

***

# 3. Segurança, identidade, acesso e sharing

`Profile` define o conjunto base de permissões do usuário; `PermissionSet` concede acessos adicionais sem alterar o profile; `PermissionSetGroup` organiza permission sets por função. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `User` | Usuário, licença, profile, role, contact, status |
| `Profile` | Perfil base de acesso |
| `ProfilePasswordPolicy` | Política de senha por profile |
| `ProfileSessionSetting` | Sessão por profile |
| `ProfileActionOverride` | Override de ação por profile |
| `ProfileApplicationVisibility` | Visibilidade de app por profile |
| `ProfileApexClassAccess` | Acesso a Apex Class |
| `ProfileApexPageAccess` | Acesso a Visualforce |
| `ProfileCustomMetadataTypeAccess` | Acesso a Custom Metadata Type |
| `ProfileCustomPermissions` | Acesso a Custom Permission |
| `ProfileCustomSettingAccesses` | Acesso a Custom Setting |
| `ProfileExternalDataSourceAccess` | Acesso a External Data Source |
| `ProfileFieldLevelSecurity` | FLS |
| `ProfileFlowAccess` | Acesso a Flow |
| `ProfileLayoutAssignments` | Layout assignments |
| `ProfileLoginFlows` | Login Flow |
| `ProfileLoginIpRange` | Faixa de IP |
| `ProfileObjectPermissions` | Permissões de objeto |
| `ProfileRecordTypeVisibility` | Visibilidade de Record Type |
| `ProfileTabVisibility` | Visibilidade de tab |
| `PermissionSet` | Permission Set.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/namedfilter.htm) |
| `PermissionSetGroup` | Grupo de Permission Sets.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api-meta/meta_customerdataplatformsettings.htm) |
| `MutingPermissionSet` | Remove permissões de um grupo |
| `CustomPermission` | Permissão customizada |
| `PermissionSetAssignment` | Vínculo usuário ↔ permission set |
| `Role` | Role hierarchy |
| `UserRole` | Papel do usuário |
| `Territory` | Território legado |
| `Territory2` | Enterprise Territory Management |
| `Territory2Model` | Modelo de território |
| `Territory2Rule` | Regra de território |
| `Territory2Type` | Tipo de território |
| `Group` | Public Group |
| `Queue` | Fila |
| `QueueSobject` | Objeto habilitado na fila |
| `SharingRules` | Regras de compartilhamento |
| `SharingCriteriaRule` | Sharing por critério |
| `SharingOwnerRule` | Sharing por owner/role |
| `SharingTerritoryRule` | Sharing por território |
| `SharingSet` | Sharing para Experience Cloud |
| `SharingRecalculation` | Recálculo de sharing |
| `AccountSharingRules` | Sharing de Account |
| `ContactSharingRules` | Sharing de Contact |
| `LeadSharingRules` | Sharing de Lead |
| `OpportunitySharingRules` | Sharing de Opportunity |
| `CaseSharingRules` | Sharing de Case |
| `CustomObjectSharingRules` | Sharing de objeto customizado |
| `ApexClassSharingRules` | Sharing relacionado a Apex |
| `SamlSsoConfig` | SAML SSO |
| `SamlJitHandler` | Just-in-Time provisioning |
| `AuthProvider` | OAuth/OIDC/SAML provider |
| `ConnectedApp` | App conectado e OAuth |
| `ExternalClientApplication` | External Client App.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_permissionset.htm) |
| `OAuthCustomScope` | Escopo OAuth customizado |
| `SessionSetting` | Configurações de sessão |
| `SessionTimeoutSettings` | Timeout de sessão |
| `PasswordPolicy` | Política de senha |
| `LoginIpRange` | Faixa IP |
| `LoginFlow` | Flow de login |
| `Certificate` | Certificado digital |
| `Key` | Chave criptográfica |
| `SecuritySettings` | Segurança geral |
| `CspTrustedSite` | Domínio confiável CSP |
| `CorsWhitelistOrigin` | CORS |
| `ClickjackProtectionSettings` | Proteção contra clickjacking |
| `SessionManagementSettings` | Gestão de sessão |
| `IdentityVerificationSettings` | Verificação de identidade |
| `IdentityProviderSettings` | Identity Provider |
| `IdentityProvider` | IdP configurado |
| `SamlServiceProvider` | Service Provider SAML |
| `DelegateGroup` | Delegação administrativa |
| `ShieldPlatformEncryptionSettings` | Shield Platform Encryption |
| `PlatformEncryptionKeyScheme` | Esquema de chave |
| `PlatformEncryptionPolicy` | Política de criptografia |
| `EventMonitoringSettings` | Event Monitoring |
| `TransactionSecurityPolicy` | Política de segurança transacional |
| `TransactionSecurityPolicyAction` | Ação da política |
| `DataProtectionSettings` | Privacidade e proteção de dados |
| `PrivacySettings` | Privacidade |
| `ConsentSettings` | Consentimento |

***

# 4. Automação declarativa e programática

`Flow` representa estrutura, lógica e comportamento em runtime; pode criar/atualizar registros, decidir, iterar coleções e invocar Apex ou serviços externos. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `Flow` | Flow completo |
| `FlowDefinition` | Definição/versão ativa |
| `FlowCategory` | Categoria de Flow |
| `FlowTest` | Teste de Flow |
| `FlowActionCall` | Chamada de ação |
| `FlowApexPluginCall` | Chamada de plugin Apex |
| `FlowAssignment` | Atribuição de variável |
| `FlowCollectionProcessor` | Processamento de coleção |
| `FlowDecision` | Decisão |
| `FlowInputAssignment` | Atribuição de entrada |
| `FlowLoop` | Loop |
| `FlowRecordCreate` | Criação de registro |
| `FlowRecordDelete` | Exclusão de registro |
| `FlowRecordLookup` | Consulta de registro |
| `FlowRecordRollback` | Rollback |
| `FlowRecordUpdate` | Atualização de registro |
| `FlowScreen` | Tela |
| `FlowScreenField` | Campo de tela |
| `FlowStage` | Stage |
| `FlowSubflow` | Subflow |
| `FlowTextTemplate` | Template de texto |
| `FlowWaitEvent` | Espera por evento |
| `FlowWait` | Elemento de espera |
| `FlowCustomProperty` | Propriedade customizada.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_permissionsetgroup.htm) |
| `ApexClass` | Classe Apex |
| `ApexTrigger` | Trigger |
| `ApexTestSuite` | Suíte de testes |
| `ApexEmailNotification` | Notificação de erro |
| `ApexSettings` | Configurações Apex |
| `ApexComponent` | Componente Visualforce |
| `ApexPage` | Página Visualforce |
| `ApprovalProcess` | Approval Process |
| `ApprovalStep` | Etapa de aprovação |
| `AssignmentRules` | Regras de atribuição |
| `AssignmentRule` | Regra individual |
| `AutoResponseRules` | Respostas automáticas |
| `AutoResponseRule` | Regra individual |
| `EscalationRules` | Escalonamento |
| `EscalationRule` | Regra individual |
| `Workflow` | Workflow Rule |
| `WorkflowRule` | Regra de workflow |
| `WorkflowAlert` | Alerta de e-mail |
| `WorkflowFieldUpdate` | Field Update |
| `WorkflowOutboundMessage` | Outbound Message |
| `WorkflowTask` | Task automática |
| `TimeBasedWorkflow` | Ação agendada |
| `EmailTemplate` | Template de e-mail |
| `EmailServicesFunction` | Processamento de e-mail recebido |
| `EmailServicesAddress` | Endereço do serviço |
| `Letterhead` | Cabeçalho de e-mail |
| `StaticResource` | Recurso estático |
| `CustomNotificationType` | Notificação customizada |
| `QuickAction` | Ação rápida |
| `PlatformEvent` | Platform Event |
| `PlatformEventChannel` | Canal de eventos |
| `PlatformEventChannelMember` | Membro do canal |
| `EventDelivery` | Entrega de evento |
| `EventSubscription` | Assinatura de evento |
| `EventType` | Tipo de evento |
| `PushTopic` | PushTopic |
| `GenericStreamingChannel` | Canal de streaming genérico |
| `ChangeDataCapture` | Change Data Capture |
| `OutboundMessage` | Mensagem SOAP outbound |
| `FutureMethod` | Future Method |
| `Queueable` | Queueable Apex |
| `BatchJob` | Batch Apex |
| `Schedulable` | Schedulable Apex |
| `CronTrigger` | Agendamento |
| `AsyncApexJob` | Job assíncrono |
| `ApexFlexQueue` | Flex Queue |
| `Continuation` | Callout assíncrono |
| `ExternalServiceRegistration` | Registro de External Service |
| `ExternalServiceOperation` | Operação externa |
| `GenAiFunction` | Função GenAI |
| `GenAiPlugin` | Plugin GenAI |
| `GenAiPlannerBundle` | Planner/orquestrador |
| `GenAiPromptTemplate` | Prompt template |
| `GenAiResponse` | Resposta de IA |
| `EinsteinAgentSettings` | Agentforce/Einstein |
| `Agent` | Agente Agentforce |
| `AgentTopic` | Tópico do agente |
| `AgentAction` | Ação do agente |
| `AgentInstruction` | Instrução do agente |
| `AgentGuardrail` | Guardrail |
| `AgentKnowledge` | Base de conhecimento do agente |
| `AgentUser` | Usuário/agente |

***

# 5. Interface, apps e experiência do usuário

| Metadata type | Funcionalidade relacionada |
|---|---|
| `CustomApplication` | Lightning App |
| `CustomTab` | Aba |
| `AppMenu` | App Launcher |
| `FlexiPage` | Record Page, App Page, Home Page |
| `LightningComponentBundle` | LWC |
| `AuraDefinitionBundle` | Aura Component |
| `LightningMessageChannel` | Lightning Message Service |
| `LightningComponentResource` | Recurso de LWC |
| `LightningExperienceTheme` | Tema |
| `ThemeLayout` | Layout de tema |
| `NavigationMenu` | Menu de navegação |
| `NavigationMenuItem` | Item de menu |
| `Layout` | Page Layout |
| `MiniLayout` | Mini layout |
| `CompactLayout` | Layout compacto |
| `SearchLayouts` | Layouts de busca |
| `HomePageLayout` | Home clássica |
| `HomePageComponent` | Componente de home |
| `PathAssistant` | Path |
| `CustomHelpMenuSection` | Ajuda |
| `CustomSite` | Salesforce Sites |
| `SiteDotCom` | Site.com |
| `SiteIframeWhiteListUrl` | URL de iframe |
| `Network` | Experience Cloud site |
| `ExperienceBundle` | Experience Cloud em metadata |
| `ExperiencePropertyTypeBundle` | Propriedades de Experience |
| `NetworkBranding` | Branding da comunidade |
| `Audience` | Audiência |
| `AudienceCriteria` | Critérios de audiência |
| `PersonalizationSettings` | Personalização |
| `Dashboard` | Dashboard |
| `DashboardComponent` | Componente de dashboard |
| `Report` | Relatório |
| `ReportType` | Tipo de relatório |
| `AnalyticSnapshot` | Snapshot de relatório |
| `EmbeddedServiceConfig` | Service embarcado |
| `EmbeddedServiceLiveAgent` | Chat embarcado |
| `EmbeddedServiceQuickAction` | Quick action embarcada |
| `LiveChatAgentConfig` | Configuração do agente |
| `LiveChatButton` | Botão de chat |
| `LiveChatDeployment` | Deploy de chat |
| `LiveChatSensitiveDataRule` | Dados sensíveis no chat |
| `LiveChatTranscriptFields` | Campos de transcript |
| `LiveChatTranscriptMetadata` | Metadados de transcript |
| `CallCenter` | CTI/call center |
| `SoftphoneLayout` | Softphone |
| `ActionLinkGroupTemplate` | Action links |
| `CustomApplicationComponent` | Componente de aplicação |
| `CustomObjectComponent` | Componente de objeto |
| `CustomTab` | Navegação |
| `MobileApplicationDetail` | App mobile |
| `ContentAsset` | Asset visual |
| `StaticResource` | JS/CSS/imagens |
| `Document` | Documento |

***

# 6. Integração, APIs, eventos e mensageria

| Metadata type | Funcionalidade relacionada |
|---|---|
| `ConnectedApp` | OAuth, SSO, API access |
| `ExternalClientApplication` | External Client App |
| `NamedCredential` | Endpoint autenticado |
| `ExternalCredential` | Credencial externa |
| `ExternalCredentialPrincipal` | Principal de autenticação |
| `NamedCredential` + `ExternalCredential` | Callout seguro |
| `RemoteSiteSetting` | Liberação de endpoint |
| `CorsWhitelistOrigin` | CORS |
| `CspTrustedSite` | CSP |
| `Certificate` | Certificado |
| `Key` | Chave |
| `AuthProvider` | OAuth/OIDC |
| `SamlSsoConfig` | SAML |
| `ExternalDataSource` | Salesforce Connect |
| `ExternalObject` | Objeto externo |
| `ExternalServiceRegistration` | OpenAPI/External Services |
| `ExternalServiceOperation` | Operação exposta |
| `PlatformEvent` | Evento customizado |
| `PlatformEventChannel` | Canal de eventos |
| `PlatformEventChannelMember` | Membro do canal |
| `EventDelivery` | Entrega de evento |
| `EventSubscription` | Assinatura |
| `EventType` | Tipo de evento |
| `PushTopic` | Streaming SOQL |
| `GenericStreamingChannel` | Streaming genérico |
| `ChangeDataCapture` | CDC |
| `OutboundMessage` | SOAP outbound |
| `EmailServicesFunction` | E-mail inbound |
| `ApexClass` com `@RestResource` | REST inbound |
| `ApexClass` com `WebService` | SOAP inbound |
| `ApexClass` com `@HttpCallout` | Callout outbound |
| `ApexClass` com `Continuation` | Callout assíncrono |
| `ApexClass` com `@InvocableMethod` | Invocable Apex |
| `DataWeaveResource` | Transformação |
| `ApiConfig` | Configuração de API |
| `ApiQuery` | Query de API |
| `ApiRateLimit` | Rate limit |
| `IntegrationHubSettings` | Integration Hub |
| `MuleSoftApplication` | App MuleSoft |
| `MuleSoftApi` | API MuleSoft |
| `MuleSoftPolicy` | Política MuleSoft |
| `MuleSoftEnvironment` | Ambiente MuleSoft |
| `MuleSoftAsset` | Asset do Exchange |
| `MuleSoftConnector` | Conector MuleSoft |
| `MuleSoftDataWeave` | DataWeave |
| `MuleSoftRuntime` | Runtime |
| `MuleSoftWorker` | Worker |
| `MuleSoftVpc` | VPC |
| `MuleSoftPrivateSpace` | Private Space |
| `MuleSoftFlexGateway` | Flex Gateway |
| `MuleSoftApiManager` | API Manager |
| `MuleSoftExchange` | Exchange |
| `MuleSoftDesignCenter` | Design Center |
| `MuleSoftAnypointStudio` | Anypoint Studio |
| `MuleSoftCloudHub` | CloudHub |
| `MuleSoftRuntimeFabric` | Runtime Fabric |

***

# 7. DevOps, pacotes, deploy e SDLC

O `Package` define os tipos e componentes recuperados ou empacotados em uma chamada de retrieve/deploy. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externalclientapplication.htm)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `Package` | Manifest de retrieve/deploy |
| `PackageTypeMembers` | Membros do package |
| `InstalledPackage` | Pacote instalado |
| `PackagePushRequest` | Push de pacote |
| `Package2` | Pacote 2GP |
| `Package2Version` | Versão 2GP |
| `Package2VersionCreateRequest` | Criação de versão |
| `SubscriberPackage` | Pacote do assinante |
| `SubscriberPackageVersion` | Versão do assinante |
| `StaticResource` | Recurso versionável |
| `CustomMetadata` | Configuração versionável |
| `CustomMetadataType` | Definição versionável |
| `ApexClass` | Código versionável |
| `ApexTrigger` | Código versionável |
| `Flow` | Automação versionável |
| `LightningComponentBundle` | LWC versionável |
| `AuraDefinitionBundle` | Aura versionável |
| `Profile` | Configuração versionável |
| `PermissionSet` | Configuração versionável |
| `Translations` | Traduções versionáveis |
| `CustomLabels` | Labels versionáveis |
| `ReleaseManagementSettings` | Release |
| `DeploymentSettings` | Deploy |
| `SourceTrackingSettings` | Source tracking |
| `ScratchOrgInfo` | Scratch Org |
| `OrgPreferenceSettings` | Preferências da org |
| `Settings` | Configurações da org |
| `SandboxInfo` | Informações de sandbox |
| `SandboxProcess` | Processo de sandbox |
| `SandboxSettings` | Configurações de sandbox |
| `ChangeSet` | Change Set |
| `DeploymentConnection` | Conexão de deploy |
| `DeploymentJob` | Job de deploy |
| `Pipeline` | Pipeline DevOps |
| `PipelineStage` | Etapa de pipeline |
| `PipelineEnvironment` | Ambiente de pipeline |
| `CopadoDeployment` | Deploy Copado |
| `CopadoPipeline` | Pipeline Copado |
| `GearsetPipeline` | Pipeline Gearset |
| `AutoRABITPipeline` | Pipeline AutoRABIT |
| `FlosumPipeline` | Pipeline Flosum |
| `SalesforceCLI` | CLI/SFDX |
| `SalesforceDXProject` | Projeto DX |
| `ScratchOrgDefinition` | Definição de Scratch Org |
| `OrgShape` | Org Shape |
| `MetadataCoverage` | Cobertura de metadata |
| `MetadataCoverageReport` | Relatório de cobertura |

***

# 8. Nuvens do CORE: objetos e funcionalidades por nuvem

Aqui o foco muda: dentro do core, várias nuvens compartilham a **mesma org**, mas adicionam objetos padrão, apps, configurações e metadados próprios.

## Sales Cloud

| Metadata type / objeto | Funcionalidade |
|---|---|
| `Account` | Conta |
| `Contact` | Contato |
| `Lead` | Lead |
| `Opportunity` | Oportunidade |
| `OpportunityLineItem` | Produto da oportunidade |
| `Product2` | Produto |
| `Pricebook2` | Lista de preços |
| `PricebookEntry` | Entrada de lista de preços |
| `Quote` | Cotação |
| `QuoteLineItem` | Item de cotação |
| `Order` | Pedido |
| `OrderItem` | Item do pedido |
| `Contract` | Contrato |
| `Asset` | Ativo |
| `Campaign` | Campanha |
| `CampaignMember` | Membro de campanha |
| `ForecastingSettings` | Forecast |
| `ForecastingType` | Tipo de forecast |
| `ForecastingCategory` | Categoria |
| `Territory2` | Território |
| `Territory2Model` | Modelo de território |
| `Territory2Rule` | Regra de território |
| `ProductSettings` | Schedules, revenue e pricing.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_visual_workflow.htm) |
| `QuoteSettings` | Quotes |
| `OrderSettings` | Orders |
| `ContractSettings` | Contracts |

## Service Cloud

| Metadata type / objeto | Funcionalidade |
|---|---|
| `Case` | Caso |
| `CaseComment` | Comentário |
| `CaseTeamMember` | Equipe do caso |
| `CaseTeamTemplate` | Template de equipe |
| `CaseTeamRole` | Papel da equipe |
| `Entitlement` | Entitlement |
| `EntitlementProcess` | Processo de entitlement |
| `EntitlementTemplate` | Template |
| `MilestoneType` | Milestone |
| `EntitlementSettings` | Configuração de entitlement |
| `ServiceContract` | Contrato de serviço |
| `ServiceResource` | Recurso de serviço |
| `ServiceTerritory` | Território de serviço |
| `ServiceAppointment` | Agendamento |
| `WorkOrder` | Ordem de serviço |
| `WorkOrderLineItem` | Item da ordem |
| `OperatingHours` | Horário operacional |
| `SchedulingPolicy` | Política de agendamento |
| `AppointmentSchedulingPolicy` | Política de agendamento |
| `EmbeddedServiceConfig` | Service embarcado |
| `LiveChatButton` | Chat |
| `LiveChatDeployment` | Chat |
| `LiveChatAgentConfig` | Agente de chat |
| `OmniChannelSettings` | Omni-Channel |
| `ServiceChannel` | Canal de serviço |
| `ServicePresenceStatus` | Status de presença |
| `RoutingConfig` | Configuração de roteamento |
| `QueueRoutingConfig` | Roteamento de fila |
| `CaseSettings` | Configuração de Case |
| `EmailToCaseSettings` | E-mail-to-Case |
| `WebToCaseSettings` | Web-to-Case |
| `SocialCustomerServiceSettings` | Social Service |

## Experience Cloud

| Metadata type / objeto | Funcionalidade |
|---|---|
| `Network` | Comunidade/site |
| `ExperienceBundle` | Site em metadata |
| `ExperiencePropertyTypeBundle` | Propriedades |
| `NetworkBranding` | Branding |
| `CustomSite` | Site |
| `SiteDotCom` | Site.com |
| `SiteIframeWhiteListUrl` | Iframe |
| `SharingSet` | Sharing externo |
| `Audience` | Audiência |
| `AudienceCriteria` | Critérios |
| `NavigationMenu` | Navegação |
| `NavigationMenuItem` | Item de menu |
| `ThemeLayout` | Tema |
| `BrandingSet` | Branding |
| `CommunitiesSettings` | Configurações |
| `ExperienceBundleSettings` | Metadata Experience |
| `UserProvisioningConfig` | Provisionamento de usuário |
| `UserProvisioningLog` | Log de provisionamento |
| `ExternalUser` | Usuário externo |
| `PartnerUser` | Usuário parceiro |
| `CustomerUser` | Usuário cliente |
| `GuestUser` | Usuário guest |
| `SiteGuestUser` | Usuário guest de site |

## Marketing Cloud Growth / Marketing Cloud no core

| Metadata type / objeto | Funcionalidade |
|---|---|
| `Campaign` | Campanha |
| `CampaignMember` | Membro |
| `Segment` | Segmento |
| `Flow` | Journey/automação |
| `EmailTemplate` | Template |
| `ContentAsset` | Conteúdo |
| `MarketingAppExtension` | Extensão de marketing |
| `MarketingSettings` | Configurações |
| `PersonalizationSettings` | Personalização |
| `Audience` | Audiência |
| `DataCloudSegment` | Segmento Data Cloud |
| `DataCloudActivation` | Ativação |
| `DataCloudDataStream` | Data stream |
| `DataCloudIdentityResolution` | Identidade |

## Field Service

| Metadata type / objeto | Funcionalidade |
|---|---|
| `WorkOrder` | Ordem de serviço |
| `WorkOrderLineItem` | Item |
| `ServiceAppointment` | Agendamento |
| `ServiceResource` | Recurso |
| `ServiceTerritory` | Território |
| `OperatingHours` | Horário |
| `SchedulingPolicy` | Política |
| `FieldServiceSettings` | Configurações |
| `MobileApplicationDetail` | App mobile |
| `Location` | Local |
| `Asset` | Ativo |
| `ProductItem` | Item de produto |
| `ProductItemTransaction` | Transação de item |
| `ProductRequired` | Produto requerido |
| `ServiceReport` | Relatório de serviço |
| `ServiceCrew` | Equipe |
| `ServiceCrewMember` | Membro da equipe |
| `ServiceCrewSkillRequirement` | Requisito de skill |
| `SkillRequirement` | Requisito de habilidade |
| `ServiceResourceSkill` | Skill do recurso |
| `AssignedResource` | Recurso atribuído |
| `ResourceAbsence` | Ausência |
| `ResourcePreference` | Preferência |
| `ServiceResourceCapacity` | Capacidade |

## Revenue Cloud / CPQ

| Metadata type / objeto | Funcionalidade |
|---|---|
| `Product2` | Produto |
| `Pricebook2` | Lista de preços |
| `PricebookEntry` | Entrada |
| `Quote` | Cotação |
| `QuoteLineItem` | Item |
| `Order` | Pedido |
| `OrderItem` | Item |
| `Contract` | Contrato |
| `Asset` | Ativo |
| `ProductSettings` | Configuração de produto |
| `PricingRecipe` | Receita de pricing |
| `PricingActionParameters` | Parâmetros |
| `ProcedureOutputResolution` | Resolução de output |
| `IndustriesPricingSettings` | Pricing Industry |
| `RevenueSettings` | Revenue |
| `RevenueSchedule` | Schedule de receita |
| `QuantitySchedule` | Schedule de quantidade |
| `Subscription` | Assinatura |
| `SubscriptionItem` | Item de assinatura |
| `Usage` | Uso |
| `UsageType` | Tipo de uso |
| `BillingAccount` | Conta de billing |
| `BillingDocument` | Documento de billing |
| `Invoice` | Fatura |
| `CreditNote` | Nota de crédito |
| `Payment` | Pagamento |
| `PaymentLineItem` | Item de pagamento |

## Commerce Cloud no CORE

| Metadata type / objeto | Funcionalidade |
|---|---|
| `Product2` | Produto |
| `Pricebook2` | Lista de preços |
| `PricebookEntry` | Entrada |
| `Catalog` | Catálogo |
| `ProductCategory` | Categoria |
| `ProductCategoryProduct` | Produto na categoria |
| `WebStore` | Loja |
| `WebCart` | Carrinho |
| `WebCartLineItem` | Item do carrinho |
| `WebCartDeliveryGroup` | Grupo de entrega |
| `WebCartPaymentGroup` | Grupo de pagamento |
| `WebCartAdjustmentLineItem` | Ajuste |
| `OrderManagementSettings` | Order Management |
| `OrderSummary` | Resumo do pedido |
| `OrderItemSummary` | Item resumido |
| `FulfillmentOrder` | Ordem de fulfillment |
| `FulfillmentOrderLineItem` | Item de fulfillment |
| `FulfillmentOrderItemAdjustmentLineItem` | Ajuste |
| `Shipment` | Entrega |
| `ShipmentItem` | Item de entrega |
| `ReturnOrder` | Devolução |
| `ReturnOrderLineItem` | Item de devolução |
| `CommerceSettings` | Configurações de Commerce |

## Financial Services Cloud

| Metadata type / objeto | Funcionalidade |
|---|---|
| `FinancialAccount` | Conta financeira |
| `FinancialAccountRole` | Papel na conta |
| `FinancialAccountTransaction` | Transação |
| `FinancialHold` | Bloqueio |
| `FinancialServiceSettings` | Configurações |
| `ActionPlan` | Plano de ação |
| `ActionPlanItem` | Item do plano |
| `ActionPlanTemplate` | Template |
| `ActionPlanTemplateVersion` | Versão |
| `ActionPlanDependency` | Dependência |
| `Assessment` | Assessment |
| `AssessmentIndicatorDefinition` | Indicador |
| `AssessmentQuestion` | Pergunta |
| `AssessmentQuestionSet` | Conjunto de perguntas |
| `AssessmentTask` | Tarefa |
| `AssessmentTaskOrder` | Ordem |
| `Referral` | Referral |
| `ReferralRoutingConfig` | Roteamento |
| `LifeEvents` | Eventos de vida |
| `InteractionSummary` | Resumo de interação |
| `Goal` | Objetivo |
| `GoalAssignment` | Atribuição |
| `GoalLink` | Vínculo |
| `Dispute` | Disputa |
| `DisputeCase` | Caso de disputa |
| `DisputeTransaction` | Transação disputada |

## Health Cloud

| Metadata type / objeto | Funcionalidade |
|---|---|
| `Patient` | Paciente |
| `CarePlan` | Plano de cuidado |
| `CarePlanTemplate` | Template |
| `CarePlanProblem` | Problema |
| `CarePlanGoal` | Objetivo |
| `CarePlanTask` | Tarefa |
| `CarePlanTeamMember` | Equipe |
| `CareRequest` | Solicitação de cuidado |
| `CareRequestBenefitVerification` | Verificação de benefício |
| `CareRequestInsurance` | Seguro |
| `CareRequestReview` | Revisão |
| `HealthCloudSettings` | Configurações |
| `HealthCareProvider` | Prestador |
| `HealthCareProviderFacility` | Facilidade |
| `HealthCareDiagnosis` | Diagnóstico |
| `HealthCareProcedure` | Procedimento |
| `HealthCareDevice` | Dispositivo |
| `HealthCareMedication` | Medicação |
| `HealthCareAllergyIntolerance` | Alergia |
| `HealthCareImmunization` | Imunização |
| `HealthCareCoverage` | Cobertura |
| `HealthCareClaim` | Claim |
| `HealthCareConsent` | Consentimento |

## Nonprofit Cloud / Education Cloud

| Metadata type / objeto | Funcionalidade |
|---|---|
| `Program` | Programa |
| `ProgramCohort` | Coorte |
| `ProgramEnrollment` | Inscrição |
| `ProgramCohortEnrollment` | Inscrição em coorte |
| `Benefit` | Benefício |
| `BenefitAssignment` | Atribuição |
| `BenefitDisbursement` | Repasse |
| `BenefitDisbursementSchedule` | Agenda |
| `ServiceParticipant` | Participante |
| `Service` | Serviço |
| `ServiceSession` | Sessão |
| `ServiceSessionDelivery` | Entrega |
| `Attendance` | Presença |
| `AssessmentTask` | Avaliação |
| `AssessmentTaskDefinition` | Definição |
| `LearningItem` | Item de aprendizagem |
| `LearningItemStatus` | Status |
| `LearningItemRecord` | Registro |
| `Credential` | Credencial |
| `CredentialDefinition` | Definição |
| `CredentialAssignment` | Atribuição |
| `Facility` | Facilidade |
| `FacilityTimeSlot` | Horário |
| `FacilityTimeSlotTemplate` | Template |
| `GrantmakingSettings` | Grantmaking.  |
| `EducationCloudSettings` | Education Cloud |
| `NonprofitCloudSettings` | Nonprofit Cloud |

## Industries: Insurance, Public Sector, Energy, Media, Manufacturing

| Metadata type / família | Funcionalidade |
|---|---|
| `InsurancePolicy` | Apólice |
| `InsurancePolicyAsset` | Ativo da apólice |
| `InsuranceClaim` | Claim |
| `InsuranceClaimLineItem` | Item |
| `InsuranceProductCatalog` | Catálogo |
| `InsuranceSettings` | Configurações |
| `PublicSectorSettings` | Setor público |
| `PublicSectorCase` | Caso público |
| `PublicSectorAssessment` | Assessment |
| `PublicSectorApplication` | Aplicação |
| `PublicSectorBenefit` | Benefício |
| `PublicSectorConsent` | Consentimento |
| `PublicSectorDocument` | Documento |
| `PublicSectorIntake` | Intake |
| `PublicSectorRequest` | Solicitação |
| `EnergyServicePoint` | Ponto de serviço |
| `EnergyUsage` | Uso |
| `EnergySettings` | Configurações |
| `MediaCloudSettings` | Media Cloud |
| `ManufacturingCloudSettings` | Manufacturing |
| `DiscoveryFrameworkSettings` | Discovery Framework.  |
| `StageManagementSettings` | Stage Management.  |
| `ContractsSettings` | Contracts/CLM.  |

***

# 9. MARKETING CLOUD ENGAGEMENT — instância separada

Marketing Cloud Engagement não usa o mesmo modelo de metadata do core. Seus artefatos são objetos/configurações próprias, expostos via SOAP/REST API e organizados por **MID** e **Business Units**. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_package.htm)

| Artefato / objeto | Funcionalidade |
|---|---|
| `Account` / `Client` | Conta, MID e contexto de ownership |
| `BusinessUnit` | Unidade de negócio |
| `User` | Usuário MC |
| `Role` | Papel/permissão MC |
| `Permission` | Permissão granular |
| `DataFolder` | Pasta de conteúdo/dados |
| `DataExtension` | Tabela de dados marketing |
| `DataExtensionField` | Campo da data extension |
| `DataExtensionTemplate` | Template de data extension |
| `DataRetentionPeriod` | Retenção |
| `SendableDataExtensionField` | Campo sendable |
| `SendableSubscriberField` | Campo de subscriber |
| `Subscriber` | Assinante |
| `SubscriberList` | Lista de assinantes |
| `List` | Lista |
| `PublicationList` | Lista de publicação |
| `SuppressionList` | Lista de supressão |
| `Email` | E-mail |
| `EmailSendDefinition` | Definição de envio |
| `Send` | Envio realizado |
| `SendClassification` | Classificação de envio |
| `SendPriority` | Prioridade |
| `DeliveryProfile` | Perfil de entrega |
| `SenderProfile` | Perfil de remetente |
| `ContentArea` | Área de conteúdo |
| `EmailTemplate` | Template |
| `Template` | Template |
| `ImportDefinition` | Importação |
| `ExportDefinition` | Exportação |
| `ExtractDefinition` | Extração |
| `QueryDefinition` | Query / SQL |
| `Automation` | Automação |
| `AutomationActivity` | Atividade |
| `AutomationType` | Tipo |
| `Program` | Programa/journey legado |
| `Journey` | Journey Builder |
| `JourneyVersion` | Versão |
| `Interaction` | Interação |
| `InteractionDefinition` | Definição |
| `EventDefinition` | Evento de entrada |
| `EventDefinitionKey` | Chave do evento |
| `TriggeredSend` | Triggered Send |
| `TriggeredSendDefinition` | Definição de triggered send |
| `SMS` | SMS |
| `SMSSendDefinition` | Envio SMS |
| `MobileMessage` | Mensagem mobile |
| `PushMessage` | Push |
| `MobileConnect` | Mobile Connect |
| `MobilePush` | Mobile Push |
| `MobileGroup` | Grupo mobile |
| `MobileKeyword` | Keyword |
| `MobileOptIn` | Opt-in |
| `MobileOptOut` | Opt-out |
| `AdvertisingStudio` | Advertising |
| `AudienceStudio` | Audiência |
| `Personalization` | Personalization |
| `InteractionStudio` | Interaction Studio |
| `EinsteinContentSelection` | Conteúdo por IA |
| `EinsteinSendTimeOptimization` | Send Time Optimization |
| `EinsteinEngagementFrequency` | Frequência |
| `EinsteinStochasticSplit` | Split estocástico |
| `MarketingCloudConnect` | Integração com core |
| `SynchronizedDataExtension` | Data extension sincronizada |
| `SynchronizedDataExtensionField` | Campo sincronizado |
| `IntegratedPlatformApplication` | App integrado |
| `InstalledPackage` | Pacote instalado MC |
| `APIIntegration` | Integração via API |
| `SFTP` | SFTP |
| `FileLocation` | Local de arquivo |
| `FileTransferActivity` | Transferência de arquivo |
| `FileDropActivity` | File drop |
| `ReportDefinition` | Relatório |
| `TrackingEvent` | Evento de tracking |
| `OpenEvent` | Abertura |
| `ClickEvent` | Clique |
| `BounceEvent` | Bounce |
| `UnsubEvent` | Unsubscribe |
| `SentEvent` | Envio |
| `NotSentEvent` | Não enviado |

***

# 10. B2C COMMERCE — instância separada

B2C Commerce organiza funcionalidade em **cartridges**, que empacotam código e dados e podem conter templates, scripts, controllers e outros recursos. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.nonprofit_cloud_for_grantmaking_dev_guide.meta/nonprofit_cloud_for_grantmaking_dev_guide/grantmaking_metadata_api_types.htm)

| Artefato | Funcionalidade |
|---|---|
| `Realm` | Ambiente/organização B2C |
| `Instance` | Instância B2C |
| `Site` | Site/storefront |
| `Organization` | Organização B2C |
| `Cartridge` | Pacote de código e dados |
| `Cartridge Path` | Ordem de carregamento |
| `Template` | Template ISML |
| `Script` | Script server-side |
| `Controller` | Controller |
| `Pipeline` | Pipeline legado |
| `Form` | Form definition |
| `Form Definition` | Estrutura de formulário |
| `Resource Bundle` | Traduções |
| `Static Content` | JS, CSS, imagens |
| `Slot` | Slot de conteúdo |
| `Slot Configuration` | Configuração de slot |
| `Content Asset` | Conteúdo editorial |
| `Content Library` | Biblioteca |
| `Library Folder` | Pasta |
| `Catalog` | Catálogo |
| `Category` | Categoria |
| `Product` | Produto |
| `Product Variation` | Variação |
| `Variation Group` | Grupo de variação |
| `Variation Attribute` | Atributo |
| `Inventory List` | Inventário |
| `Inventory Record` | Registro de inventário |
| `Price Book` | Lista de preços |
| `Price Book Assignment` | Atribuição |
| `Promotion` | Promoção |
| `Promotion Campaign` | Campanha |
| `Coupon` | Cupom |
| `Coupon Code` | Código |
| `Source Code` | Código de origem |
| `A/B Test` | Teste A/B |
| `Customer Group` | Grupo de clientes |
| `Customer` | Cliente |
| `Customer Address` | Endereço |
| `Customer Payment Instrument` | Meio de pagamento |
| `Basket` | Carrinho |
| `Basket Line Item` | Item |
| `Order` | Pedido |
| `Order Line Item` | Item |
| `Order Payment Instrument` | Pagamento |
| `Shipping Method` | Método de envio |
| `Shipping Zone` | Zona |
| `Tax` | Imposto |
| `Tax Jurisdiction` | Jurisdição |
| `Payment Method` | Método de pagamento |
| `Payment Processor` | Processador |
| `Payment Card` | Cartão |
| `Job` | Job |
| `Job Schedule` | Agendamento |
| `Job Step` | Etapa |
| `Job Parameter` | Parâmetro |
| `OCAPI` | Open Commerce API |
| `SCAPI` | Salesforce Commerce API |
| `Shop API` | Shop API |
| `Admin API` | Admin API |
| `Data API` | Data API |
| `Business Manager` | Console administrativo |
| `Sandbox` | Sandbox |
| `Staging` | Staging |
| `Development` | Desenvolvimento |
| `Production` | Produção |
| `Code Version` | Versão de código |
| `Code Deployment` | Deploy de código |
| `Data Replication` | Replicação |
| `Site Import` | Import de site |
| `Data Import` | Import de dados |
| `Log Center` | Logs |
| `WebDAV` | WebDAV |
| `SLAS` | Shopper Login & API Access |
| `SCAPI Hook` | Hook |
| `Cartridge Hook` | Hook de cartridge |

***

# 11. OUTROS PRODUTOS EM INSTÂNCIAS/CONTEXTO SEPARADO

## MuleSoft

| Artefato | Funcionalidade |
|---|---|
| `Anypoint Platform` | Plataforma |
| `Organization` | Organização MuleSoft |
| `Business Group` | Grupo |
| `Environment` | Ambiente |
| `API` | API |
| `API Version` | Versão |
| `API Specification` | Especificação |
| `RAML` | Especificação RAML |
| `OpenAPI` | Especificação OpenAPI |
| `AsyncAPI` | Especificação AsyncAPI |
| `API Proxy` | Proxy |
| `API Autodiscovery` | Autodiscovery |
| `Policy` | Política |
| `Policy Template` | Template |
| `Application` | Application |
| `Application Registration` | Registro |
| `Client Application` | App consumidor |
| `Contract` | Contrato de API |
| `Tier` | Tier |
| `SLA` | SLA |
| `Exchange Asset` | Asset |
| `Exchange Asset Version` | Versão |
| `Connector` | Conector |
| `Mule Application` | App Mule |
| `Mule Project` | Projeto |
| `Flow` | Flow Mule |
| `Subflow` | Subflow |
| `Global Configuration` | Configuração global |
| `DataWeave Script` | Transformação |
| `DataWeave Module` | Módulo |
| `Property File` | Propriedades |
| `Secure Property` | Propriedade segura |
| `Runtime` | Runtime |
| `Worker` | Worker |
| `CloudHub` | CloudHub |
| `CloudHub 2.0` | CloudHub 2.0 |
| `Runtime Fabric` | Runtime Fabric |
| `Private Space` | Private Space |
| `VPC` | VPC |
| `Flex Gateway` | Flex Gateway |
| `API Manager` | API Manager |
| `Design Center` | Design Center |
| `Anypoint Studio` | Studio |
| `Anypoint Monitoring` | Monitoramento |
| `Anypoint Visualizer` | Visualizer |
| `Object Store` | Object Store |
| `Queue` | Queue |
| `Batch Job` | Batch |
| `Error Handler` | Tratamento de erro |

## Tableau

| Artefato | Funcionalidade |
|---|---|
| `Site` | Site Tableau |
| `Project` | Projeto |
| `Workbook` | Workbook |
| `Worksheet` | Worksheet |
| `Dashboard` | Dashboard |
| `Story` | Story |
| `View` | View |
| `Datasource` | Datasource |
| `Data Source Connection` | Conexão |
| `Extract` | Extract |
| `Live Connection` | Conexão live |
| `Data Source Filter` | Filtro |
| `Calculated Field` | Campo calculado |
| `Parameter` | Parâmetro |
| `Set` | Set |
| `Group` | Grupo |
| `Hierarchy` | Hierarquia |
| `User` | Usuário |
| `Group` | Grupo |
| `Permission` | Permissão |
| `Role` | Papel |
| `Flow` | Tableau Prep Flow |
| `Prep Flow` | Prep |
| `Catalog` | Catalog |
| `Data Management` | Data Management |
| `Pulse` | Pulse |
| `Mobile App` | Mobile |
| `Embedded Analytics` | Analytics embarcado |
| `Connected App` | Connected App |
| `Web Data Connector` | WDC |
| `Tableau CRM Asset` | CRM Analytics |

## Slack

| Artefato | Funcionalidade |
|---|---|
| `Workspace` | Workspace |
| `Enterprise Grid` | Grid |
| `Organization` | Organização |
| `Channel` | Canal |
| `Private Channel` | Canal privado |
| `Shared Channel` | Canal compartilhado |
| `Direct Message` | DM |
| `Group DM` | DM em grupo |
| `User` | Usuário |
| `User Group` | Grupo |
| `App` | App |
| `Bot` | Bot |
| `Workflow` | Workflow |
| `Workflow Step` | Etapa |
| `Slash Command` | Slash command |
| `Incoming Webhook` | Webhook de entrada |
| `Outgoing Webhook` | Webhook de saída |
| `Block Kit` | UI blocks |
| `Message` | Mensagem |
| `Canvas` | Canvas |
| `List` | Listas |
| `Bookmark` | Bookmark |
| `Reminder` | Lembrete |
| `Huddle` | Huddle |
| `Connect` | Slack Connect |
| `Salesforce App` | App Salesforce |
| `Salesforce Notifications` | Notificações |
| `Salesforce Records` | Registros no Slack |
| `Salesforce Flows` | Flows acionados |
| `Einstein/Agentforce` | IA no Slack |

## Data Cloud

| Artefato | Funcionalidade |
|---|---|
| `Data Space` | Data Space |
| `Data Stream` | Entrada de dados |
| `Data Source` | Fonte |
| `Data Source Object` | Objeto da fonte |
| `Data Model Object` | DMO |
| `Data Lake Object` | DLO |
| `Profile` | Perfil unificado |
| `Identity Resolution` | Resolução de identidade |
| `Identity Resolution Ruleset` | Regras |
| `Match Rule` | Regra de match |
| `Reconciliation Rule` | Reconciliação |
| `Segment` | Segmento |
| `Segmentation` | Segmentação |
| `Publishing` | Publicação |
| `Activation` | Ativação |
| `Activation Target` | Destino |
| `Calculated Insight` | Insight calculado |
| `Data Graph` | Data Graph |
| `Prompt Template` | Prompt |
| `Einstein Personalization` | Personalização |
| `Data Sharing` | Compartilhamento |
| `Data Cloud API` | APIs |
| `Data Cloud Query` | Query |
| `Data Cloud SQL` | SQL |
| `Data Cloud Metadata` | Metadados |
| `Data Cloud Consent` | Consentimento |
| `Data Cloud Privacy` | Privacidade |

## Agentforce

| Artefato | Funcionalidade |
|---|---|
| `Agent` | Agente |
| `Agentforce Agent` | Agente |
| `Topic` | Tópico |
| `Action` | Ação |
| `Instruction` | Instrução |
| `Guardrail` | Guardrail |
| `Planner` | Planejador |
| `Reasoning Engine` | Motor de raciocínio |
| `Prompt Template` | Prompt |
| `Prompt Library` | Biblioteca |
| `Grounding` | Grounding |
| `Knowledge` | Conhecimento |
| `Retriever` | Retriever |
| `Vector Store` | Vector store |
| `Search Index` | Índice |
| `Model` | Modelo |
| `Model Card` | Card do modelo |
| `Response` | Resposta |
| `Conversation` | Conversa |
| `Session` | Sessão |
| `Feedback` | Feedback |
| `Evaluation` | Avaliação |
| `Audit` | Auditoria |
| `Atlas Reasoning Engine` | Atlas |
| `Einstein Trust Layer` | Trust Layer |

***

# 12. Como usar este material

Para tutorial, recomendo organizar cada capítulo assim:

```text
1. O que é
2. Onde vive: CORE, Marketing Cloud, Commerce, MuleSoft, Tableau, Slack, Data Cloud
3. Metadata type / artefato principal
4. Objetos e campos relacionados
5. Quem acessa
6. Como automatiza
7. Como integra
8. Limites e volumes
9. Deploy e DevOps
10. Cenário prático
```

Exemplo aplicado a antifraude:

```text
Produto: CORE Salesforce
Metadata: CustomObject
Artefato: FraudCase__c
Objetos: Case, Account, Transaction__c
Acesso: Profile, Permission Set, Sharing Rules
Automação: Flow, Apex, Platform Event
Integração: Named Credential, MuleSoft
Deploy: SFDX, Scratch Org, CI/CD
```

```text
Produto: Marketing Cloud
Artefato: DataExtension
Objetos: Subscriber, Send, Journey
Acesso: Business Unit, Role, Permission
Automação: Automation Studio, Journey Builder
Integração: Marketing Cloud Connect, API Events
Deploy: Package Manager, API, SFTP
```

```text
Produto: B2C Commerce
Artefato: Cartridge
Objetos: Product, Catalog, Basket, Order
Acesso: Business Manager, roles, sites
Automação: Jobs, scripts, controllers
Integração: OCAPI, SCAPI, SLAS
Deploy: Code version, site import, data replication
```

***

# 13. Fonte de verdade para manter atualizado

Para o material de consulta, use três fontes oficiais:

1. **Metadata API Types** — lista oficial dos metadata types do core. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm)
2. **Metadata Coverage Report** — mostra suporte por tipo, API version e operação. 
3. **APIs específicas por produto** — Marketing Cloud Engagement APIs, B2C Commerce APIs, MuleSoft Anypoint, Tableau REST API e Slack API. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_package.htm)

A lista acima é ampla o suficiente para servir como **mapa mestre de consulta**, mas, para deploy em produção, cada tipo deve ser validado na documentação da API version usada pelo seu projeto, porque a Salesforce adiciona, deprecia e altera cobertura de metadados continuamente. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm)
