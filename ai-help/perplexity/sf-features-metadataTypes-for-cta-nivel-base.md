Dá para montar um catálogo **muito amplo**, mas a Salesforce possui **centenas de metadata types**, e o número cresce a cada release, especialmente por causa de Industry Clouds, Data Cloud, Agentforce e produtos adquiridos. 

>A referência oficial é o **Metadata API Developer Guide** e o **Metadata Coverage Report**, que listam os tipos suportados por API version. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_group.htm)

Abaixo está a lista **completa no nível necessário para CTA**: todos os grandes grupos, os metadata types centrais de cada grupo e as funcionalidades relacionadas. Ela é muito mais abrangente que uma lista de estudos comum, mas não substitui a referência oficial quando você for fazer deploy real.

## 1. Metadados de dados e modelo

Estes tipos definem **o que existe** na org: objetos, campos, relacionamentos, listas, validações e qualidade de dados. [salesforceben](https://www.salesforceben.com/what-is-salesforce-metadata/)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `CustomObject` | Objeto customizado, comportamento, naming, search layout, sharing model, actions |
| `CustomField` | Campo customizado, fórmula, auto-number, external ID, unique, required, default |
| `CustomObjectTranslation` | Tradução de rótulos, seções e ajuda de objetos |
| `CustomFieldTranslation` | Tradução de rótulos e ajuda de campos |
| `RecordType` | Segmentação de processos, picklists e layouts por tipo de registro |
| `BusinessProcess` | Processos de Lead, Opportunity, Case e Solution |
| `PathAssistant` | Path/Kanban por record type e processo |
| `GlobalValueSet` | Picklist global reutilizável |
| `GlobalPicklist` | Base legada de picklist global |
| `StandardValueSet` | Conjunto de valores padrão, como `AccountType` ou `CaseStatus` |
| `StandardValueSetTranslation` | Tradução de valores padrão |
| `GlobalValueSetTranslation` | Tradução de valores de picklist global |
| `ValidationRule` | Regra de validação por objeto |
| `WebLink` | Botões, links e ações customizadas legadas |
| `CustomPageWebLink` | Link customizado em página |
| `FieldSet` | Conjunto reutilizável de campos para páginas e componentes |
| `CompactLayout` | Layout compacto exibido em mobile, lookup e highlights panel |
| `ListView` | Visões de lista por objeto |
| `SearchLayouts` | Layouts de busca, lookup e resultados |
| `DuplicateRule` | Regra de duplicidade |
| `MatchingRule` | Regra de correspondência para identificar duplicados |
| `CleanDataService` | Configuração de limpeza/enriquecimento de dados |
| `DataCategoryGroup` | Categorias de dados para Knowledge e Answers |
| `ManagedTopics` | Tópicos gerenciados para classificação de conteúdo |
| `TopicsForObjects` | Habilitação de Topics em objetos |
| `CustomDataType` | Tipo de dado customizado |
| `ExternalDataSource` | Fonte de dados externa via Salesforce Connect |
| `ExternalObject` | Objeto externo virtualizado |
| `ExternalDataSource` + `ExternalObject` | Acesso a dados fora da org sem replicação total |
| `BigObject` | Objeto de altíssimo volume para arquivamento/histórico |
| `Index` | Índice customizado para performance de consulta |
| `CustomMetadata` | Registro de um Custom Metadata Type |
| `CustomMetadataType` | Definição do tipo de metadado customizado |
| `CustomSettings` | Configuração de aplicação, hierárquica ou de lista |
| `PlatformEventChannel` | Canal de eventos para assinantes |
| `PlatformEventChannelMember` | Associação de objeto/evento a um canal |
| `EventDelivery` | Entrega de eventos para consumidores |
| `EventSubscription` | Assinatura de eventos |
| `EventType` | Definição/tipo de evento |
| `ChangeDataCapture` | Habilitação de CDC por entidade |
| `ObjectMapping` | Mapeamento entre objetos, comum em integrações e Data Cloud |
| `DataWeaveResource` | Recurso DataWeave para transformação de dados |
| `NamedCredential` | Credencial nomeada para callouts |
| `ExternalCredential` | Credencial externa moderna para autenticação |
| `ExternalDataConnector` | Conector de dados externos |
| `RemoteSiteSetting` | Liberação de endpoint para callout legado |
| `CspTrustedSite` | Domínio confiável para Content Security Policy |
| `CorsWhitelistOrigin` | Origem liberada para CORS |

## 2. Segurança, acesso e compartilhamento

Estes tipos controlam **quem acessa o quê**, em qual nível: org, objeto, campo, registro e sistema externo. O `Profile` é associado ao usuário por `User.ProfileId`; Permission Sets são associados por `PermissionSetAssignment`. 

| Metadata type | Funcionalidade relacionada |
|---|---|
| `Profile` | Perfil base: permissões, layouts, apps, tabs, login, IP, senha, sessão |
| `PermissionSet` | Permissões adicionais por usuário |
| `PermissionSetGroup` | Agrupamento de permission sets |
| `MutingPermissionSet` | Remove permissões herdadas de um Permission Set Group |
| `CustomPermission` | Permissão customizada consultável em Apex, Flow e regras |
| `PermissionSetAssignment` | Associação usuário/permissão; normalmente gerenciada como dado/configuração de org |
| `Role` | Hierarquia de papéis |
| `Territory` | Território de vendas |
| `Territory2` | Enterprise Territory Management |
| `Territory2Rule` | Regras de atribuição de território |
| `Territory2Model` | Modelo de territórios |
| `SharingRules` | Regras de compartilhamento por objeto |
| `SharingCriteriaRule` | Compartilhamento baseado em critérios |
| `SharingOwnerRule` | Compartilhamento baseado em owner/role |
| `SharingTerritoryRule` | Compartilhamento por território |
| `SharingSet` | Compartilhamento para usuários de Experience Cloud |
| `SharingCriteriaRule` / `SharingOwnerRule` | Aplicados dentro de `SharingRules` |
| `AccountSharingRules` | Compartilhamento específico de Account |
| `ContactSharingRules` | Compartilhamento específico de Contact |
| `OpportunitySharingRules` | Compartilhamento específico de Opportunity |
| `CaseSharingRules` | Compartilhamento específico de Case |
| `LeadSharingRules` | Compartilhamento específico de Lead |
| `CustomObjectSharingRules` | Compartilhamento de objeto customizado |
| `ApexClassSharingRules` | Compartilhamento relacionado a contexto Apex |
| `Group` | Public Groups e Queues |
| `Queue` | Fila de trabalho e ownership |
| `QueueSobject` | Objetos habilitados para uma Queue |
| `User` | Usuário, licença, profile, role, contact, ativação |
| `SamlSsoConfig` | Configuração SAML SSO |
| `AuthProvider` | Provedor de autenticação externa |
| `ConnectedApp` | App conectado, OAuth scopes, policies e callbacks |
| `OAuthCustomScope` | Escopo OAuth customizado |
| `SessionSetting` | Configurações de sessão e segurança |
| `PasswordPolicy` | Política de senha |
| `LoginIpRange` | Faixa de IP de login |
| `LoginFlow` | Flow executado no login |
| `Certificate` | Certificado para SSO, assinatura e integrações |
| `Key` | Chave criptográfica |
| `SecuritySettings` | Configurações gerais de segurança |
| `NetworkBranding` | Branding de Experience Cloud |
| `CustomPermissions` | Conjunto/permissões customizadas |
| `DelegateGroup` | Grupo de delegação administrativa |
| `ManagedContentType` | Tipo de conteúdo gerenciado |
| `ShieldPlatformEncryptionSettings` | Configuração de criptografia de plataforma |
| `PlatformEncryptionKeyScheme` | Esquema de chave de criptografia |

## 3. Automação declarativa e programática

Aqui ficam as funcionalidades que executam lógica: Flow, Apex, approval, regras, mensageria e processamento assíncrono. [salesforceben](https://www.salesforceben.com/what-is-salesforce-metadata/)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `Flow` | Flow completo: Record-Triggered, Screen, Scheduled, Autolaunched, Platform Event, etc. |
| `FlowDefinition` | Definição/versão ativa e comportamento do Flow |
| `FlowCategory` | Categoria organizacional de Flows |
| `FlowTest` | Teste de Flow |
| `ApexClass` | Classe Apex, incluindo batch, queueable, future, REST, invocable e testes |
| `ApexTrigger` | Trigger Apex |
| `ApexComponent` | Componente Visualforce |
| `ApexPage` | Página Visualforce |
| `ApexTestSuite` | Suíte de testes Apex |
| `ApexEmailNotification` | Notificação de exceções Apex |
| `ApexSettings` | Configurações de Apex |
| `ApprovalProcess` | Processo de aprovação |
| `ApprovalProcess` + `ApprovalStep` | Etapas, approvers, ações e critérios |
| `AssignmentRules` | Regras de atribuição, comuns em Lead e Case |
| `AutoResponseRules` | Respostas automáticas |
| `EscalationRules` | Regras de escalonamento |
| `Workflow` | Workflow Rule legado |
| `WorkflowAlert` | Alerta de e-mail do Workflow |
| `WorkflowFieldUpdate` | Atualização de campo do Workflow |
| `WorkflowOutboundMessage` | Outbound Message do Workflow |
| `WorkflowTask` | Criação de tarefa pelo Workflow |
| `WorkflowRule` | Regra de Workflow |
| `TimeBasedWorkflow` | Ações agendadas do Workflow |
| `EmailTemplate` | Template de e-mail |
| `EmailServicesFunction` | Serviço que processa e-mails recebidos via Apex |
| `EmailServicesAddress` | Endereço associado a um Email Service |
| `Letterhead` | Cabeçalho visual para templates |
| `StaticResource` | Arquivo estático: JS, CSS, imagens, fontes |
| `Document` | Documento armazenado em pasta |
| `ContentAsset` | Asset reutilizável de conteúdo |
| `ContentVersion` | Versão de arquivo |
| `QuickAction` | Ação rápida global ou de objeto |
| `CustomApplicationComponent` | Componente customizado de aplicação |
| `CustomNotificationType` | Tipo de notificação customizada |
| `PlatformEvent` | Evento de plataforma |
| `PushTopic` | Assinatura SOQL push para Streaming API |
| `GenericStreamingChannel` | Canal genérico de streaming |
| `ChangeDataCapture` | Eventos de mudança de registro |
| `OutboundMessage` | Mensagem SOAP enviada ao external system |
| `FutureMethod` | Método Apex assíncrono, dentro de `ApexClass` |
| `Queueable` | Job Apex assíncrono, dentro de `ApexClass` |
| `BatchJob` / `Database.Batchable` | Processamento em lote, dentro de `ApexClass` |
| `Schedulable` | Agendamento Apex, dentro de `ApexClass` |
| `CronTrigger` | Agendamento de job Apex |
| `AsyncApexJob` | Monitoramento de job assíncrono |
| `ApexFlexQueue` | Fila flexível de Batch Apex |
| `Continuation` | Callout assíncrono de longa duração |
| `ExternalServiceRegistration` | Registro de External Service a partir de schema OpenAPI |
| `AIApplication` / `AIApplicationConfig` | Configurações de IA aplicada |
| `GenAiFunction` | Função GenAI/Agentforce |
| `GenAiPlannerBundle` | Planejador/orquestração de agente |
| `GenAiPlugin` | Plugin/ação para agente |
| `GenAiPromptTemplate` | Template de prompt |
| `GenAiResponse` | Configuração de resposta de IA |
| `EinsteinAgentSettings` | Configurações de Agentforce/Einstein |

## 4. Interface, apps e experiência

Estes metadados definem **como o usuário vê e navega** na solução. [salesforceben](https://www.salesforceben.com/what-is-salesforce-metadata/)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `CustomApplication` | Lightning App |
| `CustomTab` | Aba customizada |
| `AppMenu` | Menu de aplicativos |
| `FlexiPage` | Lightning Record Page, App Page ou Home Page |
| `LightningComponentBundle` | Lightning Web Component |
| `AuraDefinitionBundle` | Componente Aura |
| `LightningMessageChannel` | Comunicação entre LWC/Aura via Lightning Message Service |
| `LightningOnboardingConfig` | Configuração de onboarding Lightning |
| `LightningExperienceTheme` | Tema Lightning |
| `BrandingSet` | Conjunto de branding |
| `ThemeLayout` | Layout de tema |
| `NavigationMenu` | Menu de navegação |
| `HomePageLayout` | Layout de home clássico |
| `HomePageComponent` | Componente de home clássico |
| `Layout` | Page Layout |
| `MiniLayout` | Mini page layout |
| `ChannelLayout` | Layout por canal |
| `PathAssistant` | Path visual |
| `CustomHelpMenuSection` | Seção do menu de ajuda |
| `CustomSite` | Site Force.com / Sites |
| `ExperienceBundle` | Experience Cloud site em formato metadata |
| `ExperiencePropertyTypeBundle` | Propriedades de Experience Cloud |
| `Network` | Experience Cloud site/network |
| `NetworkBranding` | Branding da comunidade |
| `CustomPermission` | Pode controlar acesso a componentes e ações |
| `Dashboard` | Dashboard analítico |
| `ReportType` | Tipo de relatório |
| `Report` | Relatório |
| `AnalyticSnapshot` | Snapshot agendado de relatório |
| `DashboardComponent` | Componente de dashboard |
| `EmbeddedServiceConfig` | Configuração de Service Cloud embarcado |
| `EmbeddedServiceLiveAgent` | Chat/Live Agent embarcado |
| `EmbeddedServiceQuickAction` | Quick action embarcada |
| `LiveChatAgentConfig` | Configuração do agente de chat |
| `LiveChatButton` | Botão de chat |
| `LiveChatDeployment` | Deploy de chat |
| `LiveChatSensitiveDataRule` | Regra para dados sensíveis em chat |
| `LiveChatTranscriptFields` | Campos de transcript de chat |
| `LiveChatTranscriptMetadata` | Metadados de transcript |
| `CallCenter` | Configuração de call center/CTI |
| `SoftphoneLayout` | Layout do softphone |
| `MobileApplicationDetail` | Detalhe de aplicativo mobile |
| `MobileSettings` | Configurações mobile |
| `ActionLinkGroupTemplate` | Template de action links |
| `CustomObjectComponent` | Componente associado a objeto |
| `CustomApplicationComponent` | Componente de aplicação |
| `CustomTab` | Navegação |
| `CustomHelpMenuSection` | Ajuda contextual |
| `CustomSite` | Página/site público |
| `SiteDotCom` | Site construído com Site.com |
| `SiteIframeWhiteListUrl` | URL liberada para iframe |
| `ContentAsset` | Imagem/asset de branding |
| `StaticResource` | Recursos front-end |

## 5. Integração, APIs e eventos

Estes metadados definem **como a org conversa com o mundo externo** e como eventos circulam entre sistemas. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_profile.htm)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `ConnectedApp` | OAuth, SSO, API access, callback e policies |
| `NamedCredential` | Endpoint + autenticação reutilizável |
| `ExternalCredential` | Autenticação externa moderna, incluindo OAuth e custom auth |
| `ExternalCredentialPrincipal` | Principal/identidade usado pela credencial |
| `NamedCredential` + `ExternalCredential` | Callouts seguros sem hardcoded credentials |
| `RemoteSiteSetting` | Liberação de domínio para callout |
| `CorsWhitelistOrigin` | CORS |
| `CspTrustedSite` | Domínio confiável CSP |
| `ExternalDataSource` | Salesforce Connect / fonte externa |
| `ExternalObject` | Objeto virtual externo |
| `ExternalServiceRegistration` | Registro de API externa via OpenAPI |
| `ExternalServiceOperation` | Operação exposta pelo External Service |
| `PlatformEvent` | Evento customizado |
| `PlatformEventChannel` | Canal de eventos |
| `PlatformEventChannelMember` | Membro do canal |
| `EventDelivery` | Entrega de evento |
| `EventSubscription` | Assinatura de evento |
| `EventType` | Tipo de evento |
| `PushTopic` | Streaming baseado em SOQL |
| `GenericStreamingChannel` | Streaming genérico |
| `ChangeDataCapture` | Eventos de alteração de dados |
| `OutboundMessage` | Integração SOAP outbound |
| `EmailServicesFunction` | Integração inbound por e-mail |
| `ApexClass` com `WebService` | SOAP inbound |
| `ApexClass` com `@RestResource` | REST inbound |
| `ApexClass` com `@HttpCallout` | REST/SOAP outbound |
| `ApexClass` com `Continuation` | Callout assíncrono |
| `ApexClass` com `@InvocableMethod` | Ação invocável por Flow |
| `MutingPermissionSet` | Pode restringir permissões de integração |
| `SamlSsoConfig` | SSO entre Salesforce e IdP/SP |
| `AuthProvider` | OAuth/OIDC/OpenID Connect |
| `Certificate` | Assinatura, TLS e confiança |
| `Key` | Chave de criptografia/assinatura |
| `DataWeaveResource` | Transformação de payload |
| `IntegrationHubSettings` | Configurações de integração |
| `ApiConfig` | Configuração de API |
| `ApiQuery` | Query de API |
| `ApiRateLimit` | Limite de consumo de API |
| `MuleSoftApplication` | Configuração relacionada a MuleSoft |
| `MuleSoftPolicy` | Política de API MuleSoft |
| `MuleSoftApi` | API gerenciada no MuleSoft |

## 6. DevOps, pacotes e deploy

Estes tipos suportam **versionamento, empacotamento, instalação e movimentação entre ambientes**. O `Package` define quais tipos e membros serão recuperados/deployados pelo Metadata API. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_package.htm)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `Package` | Manifest de retrieve/deploy |
| `PackageTypeMembers` | Membros de um tipo no package |
| `InstalledPackage` | Pacote gerenciado/unlocked instalado |
| `PackagePushRequest` | Push de pacote para assinantes |
| `Package2` | Pacote 2GP |
| `Package2Version` | Versão de pacote 2GP |
| `Package2VersionCreateRequest` | Criação de versão 2GP |
| `SubscriberPackage` | Pacote instalado por assinante |
| `SubscriberPackageVersion` | Versão instalada |
| `StaticResource` | Asset versionável |
| `CustomMetadata` | Configuração deployável |
| `CustomMetadataType` | Definição de configuração deployável |
| `ApexClass` | Código versionável |
| `ApexTrigger` | Código versionável |
| `LightningComponentBundle` | Front-end versionável |
| `AuraDefinitionBundle` | Front-end versionável |
| `Flow` | Automação versionável |
| `Profile` | Configuração versionável, com cuidado em merges |
| `PermissionSet` | Configuração versionável recomendada para permissões |
| `Translation` | Traduções versionáveis |
| `Translations` | Arquivo de traduções |
| `CustomLabels` | Rótulos traduzíveis |
| `CustomLabel` | Label individual |
| `Scontrol` | Componente legado |
| `ReleaseManagementSettings` | Configurações de release |
| `DeploymentSettings` | Configurações de deploy |
| `SourceTrackingSettings` | Source tracking em Scratch Orgs |
| `ScratchOrgInfo` | Informações de Scratch Org |
| `OrgPreferenceSettings` | Preferências da org |
| `Settings` | Família de configurações da org acessada como `Settings` no manifest.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.industries_reference.meta/industries_reference/discovery_framework_metadata_api_parent.htm) |

## 7. Configurações de produto e org (`Settings`)

No package manifest, muitas configurações de produto são agrupadas sob o tipo **`Settings`**, mas cada uma possui um metadata type próprio, como `CaseSettings`, `EntitlementSettings`, `KnowledgeSettings` e `CustomerDataPlatformSettings`. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.industries_reference.meta/industries_reference/discovery_framework_metadata_api_parent.htm)

| Metadata type | Funcionalidade relacionada |
|---|---|
| `AccountSettings` | Configurações de Account |
| `ActivitiesSettings` | Tarefas, eventos e calendário |
| `AddressSettings` | Configurações de endereço |
| `AdvancedCurrencyManagementSettings` | Moedas e taxas |
| `AIReplyRecommendationsSettings` | Recomendações de resposta por IA |
| `ApexSettings` | Apex |
| `AudienceSettings` | Audiências |
| `CaseSettings` | Case, e-mail-to-case, thread, auto-response |
| `ChatterAnswersSettings` | Chatter Answers |
| `ChatterEmailsMDSettings` | E-mails do Chatter |
| `ChatterSettings` | Chatter |
| `CommunitiesSettings` | Experience Cloud |
| `CompanySettings` | Configurações da empresa |
| `ConnectedAppSettings` | Connected Apps |
| `ContentSettings` | Content/Files.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.industries_reference.meta/industries_reference/discovery_framework_metadata_api_parent.htm) |
| `ContractSettings` | Contratos |
| `CustomerDataPlatformSettings` | Data Cloud.  [sfconnect](https://sfconnect.com/articles/1112/standard-metadata-types-in-salesforce-along-with-their-api-names/) |
| `DataProtectionSettings` | Proteção e privacidade de dados |
| `DevHubSettings` | Dev Hub |
| `EmailAdministrationSettings` | Administração de e-mail |
| `EmailTemplateSettings` | Templates de e-mail |
| `EntitlementSettings` | Entitlements e Service Cloud |
| `ExperienceBundleSettings` | Experience Cloud metadata |
| `FieldServiceSettings` | Field Service |
| `ForecastingSettings` | Forecasting |
| `IdeasSettings` | Ideas |
| `KnowledgeSettings` | Knowledge |
| `LanguageSettings` | Idiomas e tradução |
| `LightningExperienceSettings` | Lightning Experience |
| `LiveAgentSettings` | Live Agent/chat |
| `MarketingSettings` | Marketing |
| `MobileSettings` | Mobile |
| `MyDomainSettings` | My Domain |
| `OpportunitySettings` | Opportunity |
| `OrderSettings` | Orders |
| `PathAssistantSettings` | Path |
| `PersonaSettings` | Personas |
| `ProductSettings` | Produtos |
| `QuoteSettings` | Quotes |
| `SearchSettings` | Search |
| `SecuritySettings` | Segurança |
| `SessionSettings` | Sessão |
| `SocialCustomerServiceSettings` | Social Customer Service |
| `SurveySettings` | Surveys |
| `TerritoryManagementSettings` | Territory Management |
| `TranslationSettings` | Traduções |
| `WorkflowSettings` | Workflow |
| `WorkDotComSettings` | Work.com |

## 8. OmniStudio e Industry Clouds

OmniStudio e Industry Clouds possuem metadados próprios, muito relevantes quando o cenário de CTA envolve jornadas guiadas, documentos, seguros, saúde, finanças ou setor público. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_profile.htm)

| Metadata type / família | Funcionalidade relacionada |
|---|---|
| `OmniInteractionConfig` | Configuração de interação OmniStudio |
| `OmniIntegrationProcedure` | Integration Procedure |
| `OmniDataTransform` | DataRaptor |
| `OmniScript` | OmniScript/jornada guiada |
| `OmniUiCard` | FlexCard |
| `OmniProcess` | Processo OmniStudio |
| `OmniProcessType` | Tipo de processo |
| `OmniResourceConfig` | Configuração de recursos |
| `OmniTranslation` | Tradução OmniStudio |
| `OmniSupplementalItem` | Item complementar |
| `OmniSupplementalType` | Tipo de item complementar |
| `OmniInteractionAccess` | Acesso a interação |
| `OmniInteractionDefinition` | Definição de interação |
| `AssessmentQuestion` | Pergunta de assessment |
| `AssessmentQuestionSet` | Conjunto de perguntas.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_profile.htm) |
| `DocumentCategory` | Categoria de documento |
| `DocumentType` | Tipo de documento |
| `DocumentCategoryDocumentType` | Relação categoria/tipo.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_profile.htm) |
| `ContractType` | Tipo de contrato |
| `DocumentTemplate` | Template de documento |
| `ClauseCatgConfiguration` | Configuração de cláusulas |
| `ContextUseCaseMapping` | Mapeamento de contexto |
| `ESignatureConfig` | Configuração de assinatura eletrônica |
| `ESignatureEnvelopeConfig` | Configuração de envelope de assinatura |
| `ExternalDocStorageConfig` | Armazenamento externo de documentos.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.industries_reference.meta/industries_reference/stage_management_metadata_api_parent.htm) |
| `PricingRecipe` | Receita de precificação |
| `PricingActionParameters` | Parâmetros de ação de pricing |
| `ProcedureOutputResolution` | Resolução de saída de pricing |
| `IndustriesPricingSettings` | Configurações de Pricing.  [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api-meta/meta_customerdataplatformsettings.htm) |
| `IndustryCloudSettings` | Configurações de Industry Cloud |
| `IndustryCloudMetadata` | Metadados específicos de Industry Cloud |

## 9. Metadados de produto adquirido/ecossistema

| Produto/família | Metadata types e funcionalidades relacionadas |
|---|---|
| **Marketing Cloud** | Metadados majoritariamente fora do Metadata API core: Data Extensions, Journeys, Email Studio, Automation Studio, Mobile Studio, Advertising Studio, business units, API events, SFTP e integrações via Marketing Cloud Connect |
| **B2C Commerce** | Cartridges, Site Genesis/SFRA, controllers, scripts, pipelines, slots, renditions, OCAPI, SCAPI, job schedules, locales, catalogs |
| **B2B Commerce** | Catalogs, categories, products, price lists, storefronts, checkout flows, buyer groups |
| **MuleSoft** | APIs, policies, applications, environments, API Manager, Exchange assets, DataWeave, connectors |
| **Tableau** | Workbooks, datasources, dashboards, calculated fields, extracts, sites, projects, permissions |
| **Slack** | Apps, workflows, slash commands, incoming/outgoing webhooks, Bolt, blocks, canvases |
| **Data Cloud** | Data streams, data model objects, identity resolution rulesets, segments, activations, calculated insights, data graphs |
| **Agentforce** | Agents, topics, actions, instructions, prompt templates, guardrails, knowledge, planner, response configurations |

## 10. Tipos que aparecem com frequência em CTA

Se você quiser priorizar o estudo, estes são os metadata types que aparecem com mais frequência em decisões de arquitetura:

```text
CustomObject
CustomField
RecordType
GlobalValueSet
ValidationRule
DuplicateRule
MatchingRule
FieldSet
CompactLayout
Layout
FlexiPage
LightningComponentBundle
AuraDefinitionBundle
CustomApplication
CustomTab
Flow
FlowDefinition
ApexClass
ApexTrigger
ApexPage
ApexComponent
StaticResource
CustomLabels
CustomMetadata
CustomMetadataType
CustomSetting
NamedCredential
ExternalCredential
ConnectedApp
AuthProvider
SamlSsoConfig
Certificate
RemoteSiteSetting
CorsWhitelistOrigin
Profile
PermissionSet
PermissionSetGroup
MutingPermissionSet
CustomPermission
Role
Group
Queue
SharingRules
SharingSet
PlatformEvent
PlatformEventChannel
PlatformEventChannelMember
ChangeDataCapture
PushTopic
EventDelivery
EventSubscription
ExternalDataSource
ExternalObject
ExternalServiceRegistration
EmailTemplate
EmailServicesFunction
QuickAction
Dashboard
Report
ReportType
ExperienceBundle
Network
CustomSite
InstalledPackage
Package
Package2
Package2Version
Settings
Translations
```

## Como estudar sem se perder

Use esta regra simples:

```text
Metadata type = “o que é isso?”
Metadata component = “a instância específica disso”
Metadata field = “propriedade dessa instância”
```

Por exemplo:

```text
Metadata type: CustomObject
Componente: FraudCase__c
Campos: label, pluralLabel, deploymentStatus, sharingModel, nameField
```

```text
Metadata type: Flow
Componente: Fraud_Triage_RT
Campos: apiVersion, status, processType, startElementReference
```

```text
Metadata type: Profile
Componente: Fraud_Analyst
Campos: custom, userPermissions, fieldPermissions, objectPermissions, layoutAssignments
```

## Aviso importante sobre “lista completa”

A lista acima cobre o universo relevante para CTA e para arquitetura de soluções, mas **não é literalmente cada metadata type existente na plataforma**. A Salesforce mantém tipos específicos por produto, indústria, região, licença e API version; alguns são suportados apenas em retrieve, outros apenas em deploy, e alguns não são suportados pelo Metadata API. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_group.htm)

Para auditoria ou deploy, gere a lista real da sua org com:

```bash
sf org list-metadata-types \
  --target-org minhaOrg \
  --output-file metadata-types.json
```

Ou consulte o **Metadata Coverage Report** oficial, que mostra suporte por tipo, API version, ferramenta e operação. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_group.htm)
