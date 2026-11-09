# Auditoria: integração, APIs e eventos (2026-11-08)

Pedido da Millena: checar se os metadados de integração estão bem documentados.

## Resultado

A classificação `cls:integracao-apis-e-eventos` **não tem nenhuma funcionalidade cadastrada**. Suas 7 sub-classificações existem só como agrupamento vazio, e o site as mostra como "ainda não mapeado":
- APIs de dados e metadados;
- Autenticação de integrações;
- Chamadas externas e endpoints;
- Credenciais;
- Eventos e mensageria;
- Conectividade e virtualização de dados;
- Contratos, limites e tratamento de falhas.

Nenhum metadata type de integração está catalogado. No inventário v68, todos os candidatos abaixo estão com `recorte_core: pendente` e `cadastro: null`.

Não é uma afirmação parcial nem errada sobre integração: o tema simplesmente ainda não foi coberto. A cobertura do site não declara completude para esses itens.

## Método

Filtro **por nome** sobre `inventarios/metadata-types-v68.json` (993 itens). Ele achou 64 nomes candidatos; a lista abaixo agrupa os que parecem de integração.
- O agrupamento é **didático e provisório**: cada tipo precisa ser lido na documentação antes de ser classificado.
- Ficaram de fora falsos positivos do filtro, como `FeatureParameterInteger`, `SalesPlanDataSource`, `RecordAlertDataSource` e `IntegratedPlanDefinition`.

| Grupo provisório | Candidatos (inventário v68) |
|---|---|
| Credenciais e autenticação | NamedCredential, ExternalCredential, AuthProvider, ExternalAuthIdentityProvider, ConnectedApp, ConnectedAppSettings, ExternalClientApplication, ExternalClientAppSettings, ExtlClntAppOauthSettings, ExtlClntAppGlobalOauthSettings, ExtlClntAppOauthConfigurablePolicies, ExtlClntAppOauthSecuritySettings, ExtlClntAppSamlConfigurablePolicies, OauthCustomScope, OauthOidcSettings, OauthTokenExchangeHandler, SamlSsoConfig, Certificate, PublicKeyCertificate, PublicKeyCertificateSet, UserAuthCertificate, InboundCertificate |
| Chamadas externas e endpoints | RemoteSiteSetting, CspTrustedSite, CorsWhitelistOrigin, ExternalServiceRegistration, RegisteredExternalService, OutboundNetworkConnection, WorkflowOutboundMessage, McpServerDefinition, ApiNamedQuery |
| Eventos e mensageria | PlatformEventChannel, PlatformEventChannelMember, PlatformEventSettings, PlatformEventSubscriberConfig, EventRelayConfig, ManagedEventSubscription, LightningMessageChannel (mensageria entre componentes de UI: confirmar se entra aqui) |
| Conectividade e dados externos | ExternalDataSource, ExternalDataConnector, InternalDataConnector, DataConnector, DataConnectorIngestApi, DataConnectorS3, StreamingAppDataConnector, DataSource, DataSourceObject, DataSourceTenant, DataSourceBundleDefinition |
| Outros a avaliar | IntegrationProviderDef, IntegrationProcdDefinition, IntegArtifactDef, ObjIntegProviderDefMapping, OmniIntegrationProcedure, ExternalAIModel, ExternalAiAgentSetup, EmailIntegrationSettings, ConversationServiceIntegrationSettings, TmfOutboundNotificationSettings |

Também faltam os **objetos API** do tema, como os registros de credenciais e de eventos expostos por API padrão ou Tooling, e os platform events customizados (`__e`, que são `CustomObject`). Nenhum nome desses objetos foi verificado nesta auditoria.

## Próximo passo

Lote de integração (issue no GitHub):
1. Definir as funcionalidades, por exemplo Named Credentials, Platform Events, Change Data Capture, Connected/External Client Apps, Remote Site Settings, External Services e External Objects.
2. Ler cada tipo na documentação v68.
3. Cadastrar com fontes e notas de extração, como nos lotes anteriores.

## Andamento

- **2026-11-09, lote 5a:** cadastrados 11 metadata types, 7 estruturas e 9 funcionalidades nas sub-classificações credenciais, chamadas externas e endpoints, APIs de dados e metadados, eventos e mensageria, conectividade e virtualização de dados, e autenticação de integrações. Detalhe em `relatorios/retomada.md`.
- **2026-11-09, lote 5b:** connected apps, external client apps (núcleo) e OAuth, com 11 metadata types e 3 funcionalidades em autenticação de integrações.
- **2026-11-09, lote 5c:** certificados, SSO por SAML, provedor de identidade de autenticação externa, conexões de rede privadas, serviços registrados do Commerce, Event Relay e assinaturas gerenciadas: 8 metadata types e 5 funcionalidades novas.
- **2026-11-09, lote 5d:** contratos, limites e tratamento de falhas deixou de estar vazia: limites de API, versões de API e reprocessamento e monitoramento de eventos, com os objetos EventBusSubscriber e PlatformEventUsageMetric.
- **2026-11-09, lote 5e:** limites e falhas de callouts, Bulk API e Pub/Sub API. INT-07 tem agora 4 funcionalidades principais e 5 secundárias.
- **2026-11-09, lote 5f:** REST, SOAP, Metadata e Tooling API como funcionalidades em APIs de dados e metadados.
- **2026-11-09, lote 5g:** certificados restantes, conexão de rede de entrada e 7 plugins de external client app.
- **2026-11-09, lote 5h:** ConnectedApp com as 4 estruturas antes truncadas; CustomObject como definição de `__e` e `__x`; 2 referências novas.
- Em aberto: a relação entre a versão de API e os componentes; os limites da Metadata API; attest e OAuth security de external client app; ConnectedAppMobileDetailConfig; conectores de dados (recorte a decidir).
