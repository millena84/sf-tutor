# Auditoria de conteúdo dos nós

Gerado por `ferramentas/auditoria_conteudo.py`. Não edite à mão.
Mede sinais de texto genérico ou incompleto; não julga se o conteúdo está correto (isso exige fonte).

## Universo auditado

- funcionalidades: 137 nós; campos `o_que_e`, `finalidade`, `exemplo`
- metadata-types: 161 nós; campos `o_que_e`, `finalidade`
- objetos-api: 84 nós; campos `o_que_e`, `papel`
- estruturas: 470 nós; campos `o_que_e`
- nuvens: 4 nós; campos `resumo`, `o_que_e`
- classificacoes: 14 nós; campos `descricao`, `escopo`
- subclassificacoes: 92 nós; campos `descricao`, `escopo`

## Resumo

- Campos explicativos vazios: 0
- Campos com menos de 40 caracteres: 79
- Campos que só repetem o nome do nó: 0
- Campos com frase-modelo de preenchimento: 0
- Textos idênticos em mais de um nó: 0
- Nós com propriedades ou campos sem explicação: 26 (509 itens de 1261 nesses nós)

## Campos vazios

Nenhum.

## Campos curtos

- `metadata-types/ExtlClntAppPushSettings`.`finalidade`: Enviar push para o app móvel.
- `metadata-types/Flow`.`finalidade`: Versionar automações declarativas.
- `metadata-types/MilestoneType`.`o_que_e`: Define um tipo de milestone.
- `metadata-types/PlatformEventSettings`.`finalidade`: Ligar métricas de uso detalhadas.
- `metadata-types/Territory2Type`.`o_que_e`: Define um tipo de território.
- `metadata-types/UserAuthCertificate`.`finalidade`: Autenticar o usuário por certificado.
- `objetos-api/Case`.`papel`: Registro central do atendimento.
- `objetos-api/CustomTab`.`o_que_e`: Expõe as tabs pela Tooling API.
- `objetos-api/Flow`.`o_que_e`: Cada registro é uma versão de flow.
- `objetos-api/ForecastingAdjustment`.`papel`: Registrar ajustes de gestores.
- `objetos-api/ForecastingOwnerAdjustment`.`papel`: Registrar ajustes do próprio dono.
- `objetos-api/ForecastingQuota`.`papel`: Registrar metas usadas nas previsões.
- `objetos-api/ForecastingType`.`o_que_e`: Identifica um tipo de previsão.
- `objetos-api/ObjectTerritory2Association`.`o_que_e`: Liga uma conta ou lead a um território.
- `objetos-api/Opportunity`.`papel`: Registro do pipeline de vendas.
- `objetos-api/PathAssistant`.`o_que_e`: Expõe os Paths pela Tooling API.
- `objetos-api/PathAssistant`.`papel`: Consultar Paths programaticamente.
- `objetos-api/Pricebook2`.`o_que_e`: Representa um catálogo de preços.
- `objetos-api/QuoteLineItem`.`papel`: Detalhar os itens e preços da proposta.
- `objetos-api/UserLogin`.`papel`: Estado atual; não é histórico.
- `objetos-api/UserTerritory2Association`.`o_que_e`: Liga um usuário a um território.
- `estruturas/Approver`.`o_que_e`: Um aprovador de um passo.
- `estruturas/AssignmentRule`.`o_que_e`: Uma regra de atribuição nomeada.
- `estruturas/Attachment`.`o_que_e`: Um anexo de um email template.
- `estruturas/BotTranslation`.`o_que_e`: Tradução de um bot. Desde a API 53.0.
- `estruturas/ConnectedAppAttribute`.`o_que_e`: Atributo customizado do connected app.
- `estruturas/ConnectedAppOauthIdToken`.`o_que_e`: Configuração do ID token do app.
- `estruturas/ConnectedAppOauthPolicy`.`o_que_e`: Políticas OAuth do app.
- `estruturas/ConnectedAppSessionPolicy`.`o_que_e`: Políticas de sessão do app.
- `estruturas/ContentAssetRelationships`.`o_que_e`: Com quem um asset file é compartilhado.
- `estruturas/ContentAssetVersion`.`o_que_e`: Uma versão do arquivo de um asset file.
- `estruturas/DashboardFilter`.`o_que_e`: Um filtro de dashboard.
- `estruturas/DashboardFilterOption`.`o_que_e`: Uma opção de um filtro de dashboard.
- `estruturas/EscalationAction`.`o_que_e`: Ação de escalonamento.
- `estruturas/EscalationRule`.`o_que_e`: Uma regra de escalonamento nomeada.
- `estruturas/ExtlClntAppAndroidPushConfig`.`o_que_e`: Configuração de push para Android.
- `estruturas/ExtlClntAppNotificationType`.`o_que_e`: Tipo de notificação assinado pelo app.
- `estruturas/ExtlClntAppOauthIpRange`.`o_que_e`: Faixa de IPs confiáveis.
- `estruturas/FieldSetItem`.`o_que_e`: Um campo de um field set.
- `estruturas/FieldValue`.`o_que_e`: Par nome-valor de um campo customizado.
- `estruturas/FilterItem`.`o_que_e`: Uma condição de filtro.
- `estruturas/FlexiPageEventTarget`.`o_que_e`: O alvo de um evento de página.
- `estruturas/FlexiPageTemplateInstance`.`o_que_e`: O template da página.
- `estruturas/FlowComplexLiteralTranslation`.`o_que_e`: Reservado para uso interno.
- `estruturas/FlowFerovTranslation`.`o_que_e`: Reservado para uso interno.
- `estruturas/FlowInputParameterTranslation`.`o_que_e`: Reservado para uso interno.
- `estruturas/FlowInputValidationRule`.`o_que_e`: Uma validação da entrada do usuário.
- `estruturas/ForecastingSubmissionSettings`.`o_que_e`: A opção de envio de previsões.
- `estruturas/Holidays`.`o_que_e`: Feriado usado em horários comerciais.
- `estruturas/IndexField`.`o_que_e`: Um campo de um índice de big object.
- `estruturas/KnowledgeLanguageSettings`.`o_que_e`: Os idiomas do Knowledge.
- `estruturas/LayoutColumn`.`o_que_e`: Uma coluna de uma seção do layout.
- `estruturas/ListViewFilter`.`o_que_e`: Uma linha de filtro de uma list view.
- `estruturas/PathAssistantStep`.`o_que_e`: Etapa configurada de um Path.
- `estruturas/PicklistValueTranslation`.`o_que_e`: A tradução de um valor de picklist.
- `estruturas/PlatformActionListItem`.`o_que_e`: Uma ação da barra de ações.
- `estruturas/PresenceConfigProfileAssignments`.`o_que_e`: Perfil associado.
- `estruturas/PresenceConfigUserAssignments`.`o_que_e`: Usuário associado.
- `estruturas/PublicKeyCertificateSetKey`.`o_que_e`: Uma chave do conjunto.
- `estruturas/QueueRoutingConfigSkill`.`o_que_e`: Habilidade padrão de roteamento.
- `estruturas/QuickActionLayout`.`o_que_e`: O layout dos campos de uma ação rápida.
- `estruturas/QuickActionLayoutColumn`.`o_que_e`: Uma coluna do layout de ação rápida.
- `estruturas/QuotasSettings`.`o_que_e`: A opção de cotas.
- `estruturas/RecommendationDefinitionDetail`.`o_que_e`: Uma recomendação customizada.
- `estruturas/RelatedListItem`.`o_que_e`: Uma related list do layout.
- `estruturas/ReportBucketFieldValue`.`o_que_e`: Um bucket dentro de um bucket field.
- `estruturas/ReportChart`.`o_que_e`: O gráfico de um relatório.
- `estruturas/ReportTimeFrameFilter`.`o_que_e`: O filtro de período de um relatório.
- `estruturas/ReputationBranding`.`o_que_e`: A imagem de um nível de reputação.
- `estruturas/ReputationLevel`.`o_que_e`: Um nível de reputação.
- `estruturas/ReputationLevelDefinitions`.`o_que_e`: Os níveis de reputação do site.
- `estruturas/ReputationPointsRule`.`o_que_e`: Uma regra de pontos de reputação.
- `estruturas/ScheduledRecommendation`.`o_que_e`: A lista de recomendações agendadas.
- `estruturas/ScheduledRecommendationDetail`.`o_que_e`: Uma recomendação agendada.
- `estruturas/SiteWebAddress`.`o_que_e`: Um endereço web customizado de um site.
- `estruturas/SubtabComponents`.`o_que_e`: Componentes de console das subabas.
- `estruturas/WorkflowEmailRecipient`.`o_que_e`: Um destinatário de um alerta de e-mail.
- `subclassificacoes/agendamento`.`escopo`: Entra a execução em horários definidos.
- `subclassificacoes/files-e-documentos`.`escopo`: Entram arquivos anexados e documentos.

## Campos que repetem o nome

Nenhum.

## Frases-modelo

Nenhum.

## Textos idênticos

Nenhum.

## Propriedades ou campos sem explicação (vazia ou marcada como pendente), por nó

- `objetos-api/QuoteLineItem`: 78 de 84
- `objetos-api/Campaign`: 41 de 69
- `objetos-api/Quote`: 39 de 76
- `objetos-api/AgentWork`: 38 de 48
- `objetos-api/ServiceContract`: 38 de 46
- `metadata-types/Flow`: 37 de 50
- `objetos-api/KnowledgeArticleVersion`: 35 de 42
- `objetos-api/Product2`: 33 de 37
- `objetos-api/User`: 31 de 206
- `objetos-api/PendingServiceRouting`: 28 de 33
- `objetos-api/CampaignMember`: 25 de 32
- `objetos-api/OpportunityLineItem`: 20 de 27
- `metadata-types/FieldServiceSettings`: 14 de 55
- `objetos-api/Entitlement`: 13 de 22
- `estruturas/AutoResponseRules_RuleEntry`: 10 de 17
- `objetos-api/EntityDefinition`: 7 de 86
- `metadata-types/FlowSettings`: 5 de 32
- `metadata-types/ContractSettings`: 4 de 7
- `metadata-types/CommunitiesSettings`: 3 de 26
- `metadata-types/MyDomainSettings`: 3 de 32
- `objetos-api/Opportunity`: 2 de 63
- `metadata-types/ApprovalProcess`: 1 de 22
- `objetos-api/BusinessHours`: 1 de 20
- `objetos-api/Case`: 1 de 57
- `objetos-api/FieldDefinition`: 1 de 59
- `objetos-api/PermissionSet`: 1 de 13
