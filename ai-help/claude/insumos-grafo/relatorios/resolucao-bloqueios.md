# Resolução dos bloqueios (lote 2)

Data: 2026-11-07. Ponto de partida: a lista de bloqueios do `retomada.md` da primeira sessão. Vários itens daquela lista eram leituras ainda não feitas, e não bloqueios reais; este lote corrige a classificação e executa as leituras.

Toda fonte nova está em `fontes/registro.json`, com uma nota em `fontes/extracoes/`. Resultado da validação: 0 erros e 24 testes passando.

## Resumo

| # | Item | Situação | Antes → depois |
|---|---|---|---|
| 1 | Campos do User | parcial | 45 → 183 campos (175 nomes da Field Reference + 8 só da Object Reference) |
| 2 | Valores de enums | **resolvido** | 9 domínios agora com lista completa e evidência |
| 3 | Subtipos | parcial | 21 → 40 estruturas (Profile 15 de 21; LookupFilter, FilterItem, ValueSet, ValueSetValuesDefinition) |
| 4 | Objetos API de Flow, Path, FlexiPage, QuickAction, CustomTab | **resolvido** | 6 objetos Tooling completos, 5 correspondências e 7 referências |
| 5 | Exposição Tooling de objetos padrão | **resolvido** no nível de exposição | 6 confirmadas, 1 não exposta, 1 indeterminada |
| 6 | Caminhos de Setup | quase resolvido | 0 → 12 de 14 funcionalidades |
| 7 | Licenças e edições | parcial | edições para 9 funcionalidades; licença add-on do Data 360; licenças de Agentforce Sales e Service (lote 3a) |
| 8 | Contexto técnico do Data 360 | **resolvido** | `bloqueado` → `verificado` |
| 9 | Funcionalidades de Sales e Service Cloud | **mapeado** (lotes 3a, 3b e 3c) | 17 funcionalidades nas duas nuvens; no 3c, 22 objetos, 4 metadata types e 30 relacionamentos relidos |
| 10 | Classificação Core dos 981 tipos | não iniciado | volume; ver sugestão |
| 11 | WSDL | **reclassificado** | não é bloqueio; a documentação foi usada como fonte alternativa |
| 12 | Rede do shell | **contornado** | leitura pelo endpoint versionado; limites de tamanho descobertos |
| 13 | Teste real em org | bloqueio real | sem org; nada foi simulado |

## Detalhe por item

### 1. Campos do User (parcial)

**O que foi feito.**
- A Object Reference é servida truncada (cerca de 54 mil caracteres) nas versões 264.0 e 262.0. A página renderizada não expõe os nomes dos campos.
- A **Salesforce Field Reference** traz a tabela de campos do User. Lida em duas partes: a primeira pelo endpoint versionado (truncada em `SuAccessExpirationDate`) e a segunda pela página renderizada a partir daquele ponto.

**Resultado.**
- 175 nomes distintos. A página declara 200 linhas, então 25 nomes não foram capturados.
- 8 nomes aparecem só na Object Reference: as duas fontes não coincidem.
- Os campos vindos só da Field Reference ficaram com tipo e propriedades de API `desconhecido`.

**O que falta:** os 25 nomes restantes, mais tipo e propriedades dos campos novos.

**Sugestão:** um `describe` somente leitura do User em uma org Developer Edition. É a fonte mais completa para o contexto da org; registrar como observação autorizada e não como lista universal.

### 2. Valores de enums (resolvido)

A página *Metadata Field Types* (68.0) tem as listas de DeploymentStatus, FieldType, Gender, SharingModel e StartsWith; a página de Flow tem processType, runInMode, environments e status.

Divergências registradas no catálogo:
- **FieldType:** `Number` aparece como `Number1`.
- **processType:** `ApprovalWorkflow` e `LoginFlow` aparecem tanto na lista principal quanto na de reservados.
- **status do Flow:** a primeira leitura citava `UnderReview`, que não está na lista oficial de valores.

### 3. Subtipos (parcial)

**Profile.** Lidos 15 subtipos. A documentação termina no meio de `ProfileTabVisibility` (cerca de 112 mil caracteres) e a página renderizada exige JavaScript. Faltam 6:
- ProfileUserPermission;
- ProfileServicePresenceStatusAccess;
- LoginFlow;
- ProfileAgentAccess;
- ProfileActionOverride;
- ProfileLoginHours (detalhe).

**CustomField.**
- Adicionados LookupFilter, FilterItem, ValueSet e ValueSetValuesDefinition.
- `CustomValue` foi lido só em parte e `ValueSettings` não foi lido, por isso CustomField continua parcial.

**Ainda pendentes:**
- **CustomObject:** subtipos como ActionOverride, BusinessProcess, ListView e SearchLayouts. Vários são metadata types próprios, com página própria, e entram como cadastros nos próximos lotes.
- **FlexiPage, QuickAction e Flow:** dezenas de subtipos.

### 4. Objetos API das funcionalidades de interface e automação (resolvido)

**Objetos novos.** Seis objetos da Tooling API, com a tabela completa de campos de cada página: `obj:Flow`, `obj:FlowDefinition`, `obj:FlexiPage`, `obj:QuickActionDefinition`, `obj:CustomTab` e `obj:PathAssistant`.

**Correspondências XML ↔ API.** Cinco correspondências de natureza "transformada", todas pelo campo `Metadata` de cada objeto.

**Referências.** Sete relações por campo, entre elas:
- Flow.DefinitionId → FlowDefinition;
- FlowDefinition.ActiveVersionId e LatestVersionId → Flow;
- FlexiPage e QuickActionDefinition → EntityDefinition;
- QuickActionDefinition.TargetRecordTypeId e PathAssistant.RecordTypeId → RecordType.

As funcionalidades deixaram de ter a ausência "objeto API não investigado".

### 5. Exposição Tooling de objetos padrão (resolvido no nível de exposição)

Fonte: o índice de objetos da Tooling API 68.0.

| Situação | Objetos |
|---|---|
| Listados no índice | Profile, PermissionSet, PermissionSetGroup, PermissionSetAssignment, RecordType e User (este só com campos padrão, segundo a página) |
| Ausente da lista (`nao_exposto`) | LoginHistory |
| Indeterminado | UserLogin, que ficaria no trecho do índice que a documentação não serviu |

**O que falta:** os campos e operações de cada exposição Tooling. Não se presume que sejam iguais aos da API padrão.

### 6. Caminhos de Setup (12 de 14)

Fonte: páginas oficiais da Ajuda (help.salesforce.com), encontradas por busca restrita ao domínio.

- **Resolvidos:** Usuários, Permission sets, Grupos de permission sets, Histórico de login, Objetos e Campos customizados, Regras de validação, Flow, Path, Lightning pages, Tabs e Ações rápidas.
- **Faltam:** Perfis e Tipos de registro.

Os rótulos estão em inglês, como na Ajuda. A tradução da interface em pt-BR não foi verificada.

### 7. Licenças e edições (parcial)

As páginas da Ajuda trazem as edições e permissões necessárias. Elas foram registradas em `pre_requisitos` de 9 funcionalidades. Para o Data 360, foi registrada a licença add-on de data spaces.

**Lote 3a:** registradas a licença de usuário Salesforce (CRM padrão; a licença Salesforce Platform não dá direito a leads, oportunidades, campanhas e previsões) e a feature license Service Cloud User (Service Console).

**O que falta:** licenças de Core e matriz completa de licenças e edições das nuvens.

### 8. Contexto técnico do Data 360 (resolvido)

O que dizem as páginas oficiais de arquitetura e de introdução ao desenvolvimento:
- **Org:** o Data 360 é habilitado em uma org existente ou nova (*home org*); outras orgs se conectam como *companion orgs*.
- **Dados:** ficam em lakehouse; os DLO são mapeados para DMO do modelo C360.
- **Desenvolvimento:** empacotamento e autorização diferem dos da plataforma; a API principal é a Data 360 Connect REST API.

### 9. Sales e Service Cloud (iniciado no lote 3a)

Como você observou, a verificação de recursos por nuvem é feita na documentação Salesforce. O que foi feito:

- **Nomes atuais.** A Ajuda usa "Agentforce Sales (formerly Sales Cloud)" e "Agentforce Service (formerly Service Cloud)". O catálogo registra o nome atual como `nome_oficial` e o antigo como alias. Os ids `nuv:sales-cloud` e `nuv:service-cloud` foram mantidos.
- **Contexto técnico** (`verificado`): Lead, Opportunity e Case são objetos padrão da API padrão, na Object Reference da plataforma. Isso vale para os objetos verificados e não se generaliza para todo recurso da nuvem.
- **Funcionalidades próprias:** `func:leads`, `func:oportunidades` e `func:casos`, com objetos API, 4 relacionamentos e ausência de metadata type declarada como `desconhecido`.
- **Compartilhada:** `func:path` foi associada a vendas porque a Ajuda de vendas cita Path. Ela continua sendo da plataforma.

**Limite encontrado:** o endpoint serve Opportunity e Case truncados (cerca de 54 e 53 mil caracteres). A Field Reference completou nomes e tipos, mas não traz propriedades de API. Os campos customizados de exemplo da Field Reference (`Issue__c`, `Resolution__c`, `Summary__c`) foram excluídos.

**O que falta:** contas, contatos, campanhas, produtos, cotações, previsões, territórios, Omni-Channel, Knowledge, entitlements e regras de atribuição e escalonamento. Todos são citados pela Ajuda, mas ainda não foram catalogados.

### 9b. Restante de Sales e Service (lote 3b)

**Ponto de partida:** relatório de pesquisa assistida de 2026-11-08, guardado em `fontes/pesquisas/2026-11-08-agentforce-sales-service.md`. Ele serviu para descobrir o que ler, não como fonte: cada fato catalogado foi relido na página oficial.

**O que entrou:**
- **14 funcionalidades:**
  - vendas: contas, contatos, campanhas, produtos e catálogos de preço, cotações, previsões colaborativas, territórios de vendas, equipes de conta e de oportunidade;
  - atendimento: Omni-Channel, Lightning Knowledge, entitlements e milestones (SLA Management), regras de atribuição e escalonamento, horário comercial, apps de console.
- **7 objetos:**
  - estrutura completa: AccountTeamMember (11 campos), OpportunityTeamMember (8), LeadStatus (5), CaseMilestone (20), BusinessHours (20);
  - estrutura parcial: Account (tabela de conta pessoal truncada) e Contact (tabela truncada).
- **3 metadata types:** EntitlementProcess (com 2 subtipos), Territory2Model e ServicePresenceStatus (com 1 subtipo).
- **14 relacionamentos novos**, incluindo os alvos Account e Contact que antes não estavam catalogados.
- **Caminhos de Setup confirmados na Ajuda:** 8 funcionalidades.
- **Licenças:** Knowledge User (feature license) e licenças do Omni-Channel.
- **Alertas registrados:**
  - aposentadoria do Standard Omni-Channel (Summer '26);
  - novos nomes Sales Territories e SLA Management/SLA Policies.

**Divergências que a releitura evitou:**
- O relatório citou cinco propriedades que não existem nas páginas 68.0: `entitlementRules`, `isRecordTypeApplied` e `recordType` em EntitlementProcess; `recordVisibility` e `userRecordAccess` em Territory2Model.
- Elas ficaram fora do catálogo e estão registradas em `divergencias_documentais`.

**O que falta:**
- objetos de campanhas, produtos, cotações, previsões, territórios, Omni-Channel, Knowledge e Entitlement (exceto CaseMilestone);
- os tipos *Settings, AssignmentRules e EscalationRules;
- o caminho de Escalation Rules.

Todos estão declarados como ausência `desconhecido`, com os nomes candidatos.

### 9c. Releitura dos itens pendentes (lote 3c)

**O que foi relido** na documentação 68.0:
- **22 objetos:**
  - estrutura completa: CampaignMember, Pricebook2, PricebookEntry, OpportunityLineItem, QuoteLineItem, ForecastingItem, Territory2, Territory2Type, UserTerritory2Association, ObjectTerritory2Association, ServiceChannel, SlaProcess, ServiceContract, MilestoneType, AssignmentRule;
  - estrutura parcial: Campaign, Product2, Quote, AgentWork e KnowledgeArticleVersion (páginas truncadas); QueueRoutingConfig e Entitlement (uma linha sem nome de campo).
- **4 metadata types:**
  - AssignmentRules (com 2 subtipos) e EscalationRules (com 3);
  - ServiceChannel (com 1 subtipo) e QueueRoutingConfig (com 1).
- **26 relacionamentos de campo e 4 representações comuns** entre metadata type e objeto, entre elas EntitlementProcess ↔ SlaProcess.

**Achados registrados como alerta ou divergência, sem correção por suposição:**
- A página de Campaign não lista create(), update() nem delete(); confirmado em segunda leitura.
- A página de Entitlement não lista describeSObjects().
- QueueRoutingConfig (metadata) cita ServicePresenceStatus na seção de sufixo, o que parece erro de cópia.
- EscalationRules grafa a propriedade herdada como `fullname`.
- AgentWork declara a versão 32.0; o relatório de pesquisa havia apontado um conflito 30.0 x 32.0.
- A página de AssignmentRules só responde pelo nome singular, `meta_assignmentrule.htm`.

**Decisão de modelagem:** AssignmentRules e EscalationRules têm subtipos diferentes com o mesmo nome, `RuleEntry`.
- Os ids ficaram `mdx:AssignmentRules_RuleEntry` e `mdx:EscalationRules_RuleEntry`, com nome `RuleEntry`.
- Essa diferenciação dos ids é do projeto; não é nomenclatura oficial.

**O que falta:**
- metadata types *Settings, Territory2, Territory2Rule e Territory2Type, MilestoneType, PresenceUserConfig;
- objetos ForecastingAdjustment, ForecastingType, ForecastingQuota, PendingServiceRouting, Knowledge__kav e KnowledgeArticle;
- o caminho de Escalation Rules no Setup.

### 10. Classificação Core (não iniciado)

É resolvível com documentação, mas exige centenas de leituras. Fica como lote próprio (ver sugestões).

### 11. WSDL (reclassificado)

O prompt prevê fontes oficiais alternativas quando o WSDL não estiver disponível, com registro da diferença de cobertura. As propriedades vêm das páginas oficiais de cada tipo.

O WSDL continua útil para conferir grafias e tipos com divergência documental (`ServicePresenceStatusAccesses`, `tabSettings`, `ActionSybtype`). O importador está pronto.

### 12. Rede do shell (contornado, com limite novo descoberto)

O endpoint `get_document_content/<livro>/<pagina>/en-us/264.0` entrega o HTML das páginas com os nomes técnicos preservados. A página renderizada não serve: exige JavaScript ou perde a coluna de nomes.

**Achado novo:** o endpoint corta páginas longas. Os cortes medidos foram:
- cerca de 54 mil caracteres na Object Reference do User;
- cerca de 100 a 112 mil caracteres nas páginas de Profile, CustomField, EntityDefinition e Flow.

Esse limite explica as lacunas dos itens 1 e 3.

### 13. Teste real em org (bloqueio real)

Continua sem org. As consultas permanecem com `validacao: "documental"`.

## Melhoria já implementada

- **Validador de rastreabilidade.** O nome de cada propriedade e de cada campo precisa aparecer na nota de extração de pelo menos uma das fontes citadas. Isso impede nomes inventados ou de memória.
  - A mesma conferência, feita à mão na primeira sessão, encontrou EntityDefinition.QualifiedApiName sem leitura na fonte; o campo foi removido. Agora a conferência roda em toda validação.
  - Há teste negativo correspondente em `testes/test_insumos.py`.

## Sugestões de melhoria

1. **Liberar `developer.salesforce.com` e `help.salesforce.com` na rede do ambiente.** Com isso, um script poderia baixar o HTML versionado e extrair as tabelas de forma determinística, eliminando a extração assistida por IA e o risco de omissão em páginas longas. Essa é a maior melhoria de confiabilidade possível hoje.
2. **Fornecer os PDFs versionados** (`api_meta.pdf`, `object_reference.pdf` e `api_tooling.pdf` da 68.0) **e o `metadata.wsdl`.** Eles cobrem as páginas que o endpoint corta (subtipos de Profile e campos do User).
3. **Uma org Developer Edition com usuário somente leitura,** para `describe` e execução das consultas de exemplo. Isso permitiria passar parte das validações de "documental" para "org", registrando o contexto sem dados reais.
4. **Revalidar as páginas da Ajuda a cada release.** Elas não têm número de versão; a data de verificação está registrada.
5. **Tipo de licença `licenca_recurso` no schema de nuvem (implementado no lote 3a).** A feature license Service Cloud User não é licença de usuário, de permission set, edição nem add-on.
6. **Relatórios de pesquisa assistida como mapa, não como fonte.** No lote 3b, a releitura encontrou 5 propriedades inexistentes no relatório. Manter a regra: relatório em `fontes/pesquisas/`, fato só com releitura registrada.
7. **Classificação Core em lotes por família de nome.** Começar pelos tipos que já aparecem nas subclassificações (Settings, SharingRules, Role, Group, Queue, GlobalValueSet…), sempre com a página do tipo como evidência. Nunca classificar por semelhança de nome.
