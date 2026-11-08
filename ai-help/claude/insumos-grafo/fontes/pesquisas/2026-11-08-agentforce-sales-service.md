# Relatório de pesquisa: Agentforce Sales e Agentforce Service (2026-11-08)

## Como usar este arquivo

- **Natureza:** relatório produzido por um agente de pesquisa assistida por IA, a partir de páginas oficiais da Salesforce. Fica guardado como **registro de descoberta** (o que procurar e onde).
- **Não é fonte técnica.** Nada aqui vira afirmação `verificado` no catálogo sem releitura da página oficial, registrada em `fontes/registro.json` e com nota em `fontes/extracoes/`.
- **Tarefa:** `wf-4ea39d77-6b7e-8db1-82ff-45d3ffee2309`.
- **Lote que usou este relatório:** 3b (ver `relatorios/resolucao-bloqueios.md`).

## O que foi relido diretamente no lote 3b

| Item do relatório | Releitura | Resultado |
|---|---|---|
| Account, Contact, AccountTeamMember, OpportunityTeamMember, LeadStatus, CaseMilestone, BusinessHours | Object Reference 264.0 | Catalogados. As tabelas de Contact e as de conta pessoal (Account) vieram truncadas. |
| EntitlementProcess, Territory2Model, ServicePresenceStatus | Metadata API 264.0 | Catalogados. Ver as divergências abaixo. |
| Caminhos de Setup: Quotes, Sales Territories, Omni-Channel, Lightning Knowledge, Entitlement Settings, Business Hours, Assignment Rules, App Manager | Ajuda (busca restrita) | Confirmados e registrados. |
| Licenças e edições: Omni-Channel, Knowledge User, SLA Management, Service Console | Ajuda (busca restrita) | Confirmadas e registradas. |

## Divergências encontradas na releitura

| Relatório disse | Página oficial 68.0 relida | Decisão |
|---|---|---|
| EntitlementProcess tem `entitlementRules`, `isRecordTypeApplied` e `recordType` | Essas linhas não existem; a tabela tem 14 propriedades. | Catalogadas só as 14. |
| Territory2Model tem `recordVisibility` e `userRecordAccess` | Essas linhas não existem; a tabela tem `customFields`, `description` e `name`. | Catalogadas só as 3. |
| ServiceChannelStatus.`channel` é `string[]` | `channel` é `string`. | Usado `string`. |
| Nomes de API de muitos campos "não renderizados" (ex.: `AccountId` em Contact) | O endpoint versionado mostra os nomes. | Nomes registrados pela releitura. |

## Itens ainda só no relatório (não relidos)

- **Objetos:** Campaign, CampaignMember, Product2, Pricebook2, PricebookEntry, OpportunityLineItem, Quote, QuoteLineItem, ForecastingItem e relacionados, Territory2 e associações, AgentWork, ServiceChannel, QueueRoutingConfig, Entitlement, SlaProcess, ServiceContract, Knowledge__kav.
- **Metadata types:** AccountSettings, CampaignSettings, QuoteSettings, ForecastingSettings, LeadConvertSettings, EntitlementSettings, KnowledgeSettings, AssignmentRules, EscalationRules, BusinessHoursSettings, ServiceChannel, QueueRoutingConfig.
- **Outros:** limites de territórios por edição; aposentadoria do Territory Management original (Summer '21); caminho de Escalation Rules.

---

# Texto do relatório (como entregue)

> Texto preservado para rastreabilidade. As afirmações abaixo não foram todas confirmadas; consulte as tabelas acima antes de usar qualquer item.

## Resumo do relatório

Fontes oficiais confirmaram o núcleo estrutural das 15 funcionalidades:

- Supported Calls;
- tipos de Metadata API;
- caminhos de Setup e edições;
- notas de aposentadoria.

A cobertura é desigual. Ficaram completos:

- Supported Calls de Account e Contact;
- AccountTeamMember, LeadStatus, CaseMilestone;
- Territory2Model e ServicePresenceStatus (metadata);
- EntitlementSettings e EntitlementProcess;
- a aposentadoria do Standard Omni-Channel.

Ficaram incompletas as listas de campos da maioria dos objetos. As páginas novas do Object Reference mostram tipos e propriedades, mas a extração omitiu muitos nomes de API.

**Verificado com fonte primária, segundo o relatório**

- Supported Calls de Account, Contact, AccountTeamMember, OpportunityTeamMember, LeadStatus e CaseMilestone.
- Metadados Territory2Model (`territory2Model`), ServicePresenceStatus (`.servicePresenceStatus`), EntitlementSettings (`Entitlements.settings`) e EntitlementProcess (`.entitlementProcess`).
- Caminhos de Setup e edições de Quotes, Sales Territories, Lightning Knowledge, Business Hours, Omni-Channel e Lightning console apps.

**Aposentadorias e novos nomes**

- O Standard Omni-Channel foi aposentado no Summer '26, com upgrade automático para Enhanced.
- Enterprise Territory Management agora se chama "Sales Territories".
- Na Simplified SLA Setup, Entitlement Management aparece como "SLA Management".

**Lacunas declaradas pelo relatório**

- Listas completas e contagens de campos.
- Supported Calls de Product2, Pricebook2, PricebookEntry, Quote, ForecastingQuota, Territory2 e associações, ServiceContract, Knowledge__kav, BusinessHours, AssignmentRule e UserServicePresence.
- Propriedades de AssignmentRules, EscalationRules, KnowledgeSettings, ForecastingSettings, OpportunitySettings, QuoteSettings, ProductSettings, CaseSettings e AccountSettings.

## Por funcionalidade (síntese do relatório)

### 1. Accounts (Account)

- **O que é:** organização ou pessoa envolvida com o negócio.
- **Supported Calls:** `create()`, `delete()`, `describeLayout()`, `describeSObjects()`, `getDeleted()`, `getUpdated()`, `merge()`, `query()`, `retrieve()`, `search()`, `undelete()`, `update()`, `upsert()`.
- **Campos citados:**
  - Name: obrigatório, até 255 caracteres; concatenado e não editável em Person Account.
  - Parent e MasterRecord → Account.
  - PersonContact → Contact.
  - OperatingHours → OperatingHours (38.0, Field Service).
  - Is Person Account: somente leitura.
  - Account Source (24.0).
  - CleanStatus: picklist restrita (25.0) com Acknowledged, Different, Inactive, Matched, NotFound, Pending, SelectMatch, Skipped.
- **Metadata:** `AccountSettings` citado como exemplo de settings.
- **Regra:** `AssignmentRuleHeader` em `create()` dispara regras de Territory Management.

### 2. Contacts (Contact)

- **O que é:** pessoa associada a uma conta; pode nascer da conversão de leads.
- **Supported Calls:** iguais às de Account.
- **Campos citados:**
  - Account → Account.
  - Multipicklist de papel do comprador (61.0).
  - CleanStatus (25.0).
- **Permissão citada:** "Set Audit Fields upon Record Creation" (KB 000386699).

### 3. Campaigns (Campaign, CampaignMember)

- **O que é:** Campaign rastreia campanhas de marketing; CampaignMember liga campanha a lead, contato ou, opcionalmente, conta.
- **Campos parciais pela Field Reference:** CampaignMemberRecordTypeId e ParentId em Campaign; CampaignId, ContactId, LeadId, LeadOrContactId e LeadOrContactOwnerId em CampaignMember.
- **Regra:** CampaignMember usa `CampaignMemberRecordTypeId` de Campaign em vez de `RecordTypeId`.
- **Metadata:** `CampaignSettings` existe.

### 4. Products and Price Books

- **O que é:**
  - OpportunityLineItem liga Product2 a uma Opportunity.
  - PricebookEntry associa Pricebook2 e Product2.
- **Campos citados:** OpportunityId, PricebookEntryId e Product2Id em OpportunityLineItem; Pricebook2Id e HasOpportunityLineItem em Opportunity.
- **Ressalva:** a versão 60.0 citada no guia de Revenue Lifecycle Management não vale para o objeto core.

### 5. Quotes (Quote, QuoteLineItem)

- **O que é:** preços propostos ao cliente; várias cotações por oportunidade, uma sincronizada por vez.
- **QuoteLineItem:**
  - OpportunityLineItem (40.0) preenchido pela API.
  - PricebookEntry obrigatório com Products habilitado.
- **Setup:** Quote Settings.
- **Edições:** Performance e Developer; em vendas, também Professional, Enterprise e Unlimited.
- **Permissão:** Customize Application.
- **Licença:** cotação sem oportunidade exige licença Sales Cloud.

### 6. Collaborative Forecasting

- **ForecastingItem:** somente leitura (26.0).
- **ForecastingAdjustment:** 26.0.
- **ForecastingOwnerAdjustment:** 33.0.
- **ForecastingSubmissionItem:** 62.0.
- **ForecastingType, ForecastingFact e ForecastingQuota:** versões não verificadas.
- **Metadata:** `AccountForecastSettings` pertence a Account Forecasting.

### 7. Sales Territories (antes Enterprise Territory Management)

- **Aposentadoria:** o Territory Management original foi aposentado no Summer '21.
- **Objeto legado:** `Territory` vale para as APIs 7.0 a 52.0.
- **Modelo de dados:** Territory2, Territory2Model, Territory2Type, UserTerritory2Association, ObjectTerritory2Association e regras.
- **Metadata Territory2Model:** sufixo `territory2Model`, versão 32.0; sem packaging, change sets nem CRUD; deploy só com Manage Territories e em estados Planning ou Active. **Atenção:** o relatório citou `recordVisibility` e `userRecordAccess`, que não existem na página 68.0.
- **Setup:** Territory Settings > Enable Sales Territories.
- **Edições:** Performance e Developer; Enterprise e Unlimited com Sales.
- **Limites citados:** Enterprise tem 2 modelos e 1.000 territórios por modelo.

### 8. Opportunity/Account Teams

- **Supported Calls (ambos):** `create()`, `delete()`, `describeLayout()`, `describeSObjects()`, `getDeleted()`, `getUpdated()`, `query()`, `retrieve()`, `update()`, `upsert()`.
- **AccountTeamMember:** níveis de acesso a conta, casos, contatos e oportunidades; disponível em Enterprise, Unlimited e Performance com account teams.
- **OpportunityTeamMember:** só com team selling; create com par OpportunityId+UserId existente atualiza o registro.

### 9. LeadStatus e conversão

- **LeadStatus:** Supported Calls `describeSObjects()`, `query()`, `retrieve()`; 5 campos.
- **`convertLead()`:** até 100 conversões por chamada.
- **Metadata:** `LeadConvertSettings` e `LeadConfigSettings` existem.

### 10. Omni-Channel

- **Objetos:** AgentWork, PendingServiceRouting, QueueRoutingConfig, ServiceChannel, ServiceChannelStatus, ServicePresenceStatus e outros. ServicePresenceStatus também está na Tooling API (65.0).
- **Conflito de versão de AgentWork:** 30.0 contra 32.0.
- **Metadata:** ServicePresenceStatus (44.0, `channels`, `label`), QueueRoutingConfig e ServiceChannel.
- **Setup:** Omni-Channel Settings.
- **Aposentadoria:** Standard aposentado no Summer '26; Enhanced por padrão em orgs após Summer '23; Enhanced não funciona no Classic.

### 11. Lightning Knowledge

- Habilitar é irreversível e muda o modelo para record types.
- **Setup:** Knowledge Settings.
- **Licença:** feature license Knowledge User, em Professional, Enterprise, Performance, Unlimited e Developer.
- **Classic:** migração exigida até 1º de junho de 2025.

### 12. Entitlement Management (SLA Management)

- **CaseMilestone:** 18.0; Supported Calls `describeLayout()`, `describeSObjects()`, `query()`, `retrieve()`, `update()`.
- **Entitlement:** 18.0; campos AccountId, AssetId, BusinessHoursId, ServiceContractId, SlaProcessId e outros.
- **SlaProcess:** 19.0.
- **EntitlementSettings:** arquivo `Entitlements.settings`, 27.0, 19 campos.
- **EntitlementProcess:** sufixo `.entitlementProcess`, 27.0. **Atenção:** o relatório citou `entitlementRules`, `isRecordTypeApplied` e `recordType`, que não existem na página 68.0.
- **Licença:** só orgs com Agentforce Service.

### 13. Assignment Rules e Escalation Rules

- **Metadata:** AssignmentRules e EscalationRules existem.
- **Setup:** Lead Assignment Rules / Case Assignment Rules.
- **Limites citados:** 2.000 regras; 50 ativas e 500 por objeto; 3.000 entradas por regra; 300 de fórmula; 25 critérios por entrada; 200 ações por regra.

### 14. Business Hours

- **Padrão:** 24x7 no fuso da org.
- **Setup:** Business Hours.
- **Permissão:** Manage Business Hours Holidays.
- **Limite:** até 1.000 feriados por horário comercial.
- **Metadata:** `BusinessHoursSettings` existe.

### 15. Lightning console apps

- **Setup:** App Manager > New Lightning App > Console navigation.
- **Edições:** Essentials, Professional, Enterprise, Performance, Unlimited e Developer; o Service Console exige Service Cloud.
- **Salesforce Platform:** custo extra, via permission set license Lightning Console.

## Fontes citadas pelo relatório

| id do relatório | URL |
|---|---|
| src-objref-account | https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-account.html |
| src-objref-contact | https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-contact.html |
| src-api-create | https://developer.salesforce.com/docs/platform/api/guide/sforce-api-calls-create.html |
| src-fr-campaign | https://developer.salesforce.com/docs/platform/field-reference/references/field-reference/salesforce-field-reference-campaign.html |
| src-fr-campaignmember | https://developer.salesforce.com/docs/platform/field-reference/references/field-reference/salesforce-field-reference-campaignmember.html |
| src-objref-recordtype | https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-recordtype.html |
| src-fr-oli | https://developer.salesforce.com/docs/platform/field-reference/references/field-reference/salesforce-field-reference-opportunitylineitem.html |
| src-fr-opportunity | https://developer.salesforce.com/docs/platform/field-reference/references/field-reference/salesforce-field-reference-opportunity.html |
| src-objref-pbe-ja | https://developer.salesforce.com/docs/atlas.ja-jp.object_reference.meta/object_reference/sforce_api_objects_pricebookentry.htm |
| src-objref-qli | https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-quotelineitem.html |
| src-fr-qli | https://developer.salesforce.com/docs/platform/field-reference/references/field-reference/salesforce-field-reference-quotelineitem.html |
| src-help-quotes-setup | https://help.salesforce.com/s/articleView?id=quotes_enable.htm&language=en_US&type=5 |
| src-help-quotes-noopp | https://help.salesforce.com/s/articleView?id=sf.cpq_quotes_without_opportunities.htm&language=en_US&type=5 |
| src-help-quotes | https://help.salesforce.com/s/articleView?language=en_US&id=sf.quotes_overview.htm&release=238.5.0&type=5 |
| src-help-quotes-manage | https://help.salesforce.com/s/articleView?id=sf.quotes_manage_your_quotes.htm&language=en_US |
| src-objref-forecastingitem | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_forecastingitem.htm |
| src-meta-territory2model | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_territory2model.htm |
| src-meta-territory2 | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_territory2.htm |
| src-meta-territory2rule | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_territory2rule.htm |
| src-objref-territory2type | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_territory2type.htm |
| src-objref-territory | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_territory.htm |
| src-dm-territory | https://developer.salesforce.com/docs/platform/data-models/guide/territory-management.html |
| src-help-tm2-enable | https://help.salesforce.com/apex/HTViewHelpDoc?id=tm2_enable_tm2.htm |
| src-help-tm2-activate | https://help.salesforce.com/s/articleView?id=sf.tm2_activate_territory_model.htm&language=en_US&type=5 |
| src-help-tm2-perms | https://help.salesforce.com/s/articleView?id=sf.tm2_how_access_permissions_work.htm&language=en_US&type=5 |
| src-help-tm2-alloc | https://help.salesforce.com/apex/HTViewHelpDoc?id=sf.tm2_allocations.htm&language=en_US |
| src-rn-etm-rename | https://help.salesforce.com/s/articleView?id=release-notes.rn_sales_spm_etm_to_sales_territories.htm&language=en_US&release=250&type=5 |
| src-objref-otm | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_opportunityteammember.htm |
| src-objref-atm | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_accountteammember.htm |
| src-objref-leadstatus | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_leadstatus.htm |
| src-objref-lead | https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-lead.html |
| src-api-convertlead | https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_convertlead.htm |
| src-meta-leadconvert-ja | https://developer.salesforce.com/docs/atlas.ja-jp.api_meta.meta/api_meta/meta_leadconvertsettings.htm |
| src-mcr-v67 | https://developer.salesforce.com/docs/success/metadata-coverage-report/references/metadata-types/v67.0/metadata-types.html |
| src-mcr-v66 | https://developer.salesforce.com/docs/success/metadata-coverage-report/references/metadata-types/v66.0 |
| src-mcr-v65 | https://developer.salesforce.com/docs/success/metadata-coverage-report/references/metadata-types/v65.0/metadata-types.html |
| src-mcr-v61 | https://developer.salesforce.com/docs/success/metadata-coverage-report/references/metadata-types/v61.0/metadata-types.html |
| src-mcr-v53 | https://developer.salesforce.com/docs/success/metadata-coverage-report/references/metadata-types/v53.0 |
| src-omni-objects | https://developer.salesforce.com/docs/service/service-presence-developer-guide/guide/service-presence-soap-api-intro.html |
| src-omni-meta | https://developer.salesforce.com/docs/service/service-presence-developer-guide/guide/omnichannel-metadata-api-intro.html |
| src-meta-sps | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_servicepresencestatus.htm |
| src-objref-sps | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_servicepresencestatus.htm |
| src-tooling-sps | https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_servicepresencestatus.htm |
| src-objref-qrc | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_queueroutingconfig.htm |
| src-fr-qrc | https://developer.salesforce.com/docs/platform/field-reference/references/field-reference/salesforce-field-reference-queueroutingconfig.html |
| src-objref-scs | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_servicechannelstatus.htm |
| src-objref-agentwork | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_agentwork.htm |
| src-help-omni-intro | https://help.salesforce.com/s/articleView?id=service.omnichannel_intro.htm&language=en_US&type=5 |
| src-help-omni-setup | https://help.salesforce.com/s/articleView?language=en_US&id=sf.service_presence_intro.htm&type=5 |
| src-help-omni-enable | https://help.salesforce.com/s/articleView?language=en_US&id=omnichannel_enable.htm |
| src-help-omni-upgrade | https://help.salesforce.com/s/articleView?id=service.omnichannel_upgrade_standard_to_enhanced.htm&language=en_US&type=5 |
| src-help-omni-compare | https://help.salesforce.com/s/articleView?id=service.omnichannel_std_vs_enhanced.htm&language=en_US&type=5 |
| src-help-lk-enable | https://help.salesforce.com/s/articleView?id=service.knowledge_lightning_enable.htm&language=en_US&type=5 |
| src-help-lk-access | https://help.salesforce.com/s/articleView?id=sf.knowledge_lightning_user_access.htm&language=en_US&type=5 |
| src-help-featurelic | https://help.salesforce.com/s/articleView?id=sf.users_feature_licenses_available.htm&language=en_US |
| src-help-k-classic | https://help.salesforce.com/s/articleView?language=en_US&id=sf.knowledge_setup.htm&type=5 |
| src-help-ent-about | https://help.salesforce.com/s/articleView?id=service.entitlements_about.htm&language=en_US&type=5 |
| src-help-ent-sla | https://help.salesforce.com/s/articleView?language=en_US&id=service.entitlements_simplified_sla_setup_parent.htm&type=5 |
| src-help-ent-access | https://help.salesforce.com/s/articleView?id=sf.entitlements_giving_users_access.htm&language=en_US&type=5 |
| src-help-ent-bh | https://help.salesforce.com/s/articleView?language=en_US&id=sf.entitlements_business_hours.htm&release=234.16.0&type=5 |
| src-pdf-ent-guide | https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_entitlements_implementation_guide.pdf |
| src-meta-entsettings | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_entitlementsettings.htm |
| src-meta-entprocess | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_entitlementprocess.htm |
| src-objref-casemilestone | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_casemilestone.htm |
| src-objref-entitlement | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_entitlement.htm |
| src-objref-slaprocess | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_slaprocess.htm |
| src-help-assign-guide | https://help.salesforce.com/s/articleView?language=en_US&id=sf.customize_leadrules.htm |
| src-help-rules-limits | https://help.salesforce.com/s/articleView?language=en_US&id=service.rules_limits.htm&type=5 |
| src-help-bh | https://help.salesforce.com/s/articleView?language=en_US&id=service.customize_supporthours.htm&type=5 |
| src-meta-bhsettings-ja | https://developer.salesforce.com/docs/atlas.ja-jp.api_meta.meta/api_meta/meta_businesshourssettings.htm |
| src-help-console-create | https://help.salesforce.com/s/articleView?id=sf.console_lex_create_custom.htm&language=en_US&type=5 |
| src-help-service-console | https://help.salesforce.com/s/articleView?language=en_US&id=service.console_lex_service_intro.htm&type=5 |
| src-meta-typeslist | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm |
