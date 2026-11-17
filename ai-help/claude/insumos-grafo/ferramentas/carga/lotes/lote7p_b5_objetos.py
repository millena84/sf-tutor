"""Lote 7p (rodada B5, parte C; issue #34): completar os objetos API que estavam parciais.

As páginas da Object Reference e da Tooling API que vinham "truncadas" eram, na verdade, cortadas pelo leitor em 100 mil caracteres; com o
parâmetro offset elas foram lidas até o fim da tabela de campos. Este lote acrescenta os campos que faltavam e recalcula a cobertura.

Convenção já usada no catálogo (Group, GroupMember): Id e campos de sistema que a tabela da página não lista não entram, e isso não
impede a cobertura completa. Linhas vazias da tabela também não contam.

Ordem: lote7o_b5_flow.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7p_b5_objetos.py
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import obj as O                    # noqa: E402
from carga.base import ev, ld, sv, caminho    # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7p-b5-objetos.txt"
OR = "https://developer.salesforce.com/docs/atlas.en-us.264.0.object_reference.meta/object_reference/sforce_api_objects_"
TL = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_tooling.meta/api_tooling/tooling_api_objects_"
OBJS = {"Contact": OR, "Campaign": OR, "Quote": OR, "AgentWork": OR, "KnowledgeArticleVersion": OR, "Case": OR, "Opportunity": OR, "Lead": OR,
        "Account": OR, "User": OR, "Product2": OR, "Entitlement": OR, "QueueRoutingConfig": OR, "EventLogFile": OR,
        "EntityDefinition": TL, "FieldDefinition": TL, "CustomField": TL, "CustomObject": TL}
p = caminho("fontes", "registro.json")
reg = json.load(open(p, encoding="utf-8"))
novas = [C.fonte(f"src:objref-{n.lower()}-completa", f"{n} ({'Tooling API' if u == TL else 'Object Reference'}), leitura completa",
                 u + n.lower() + ".htm", f"Tabela de campos de {n} lida até o fim com offset.", EXTR, DATA) for n, u in OBJS.items()]
ids = {x["id"] for x in novas}
reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
SRC = {n: f"src:objref-{n.lower()}-completa" for n in OBJS}
EXISTE = {f[:-5] for f in os.listdir(caminho("catalogo", "objetos-api"))}

# nome|tipo|props|versão|refere-se a|descrição (pt-BR, paráfrase)
NOVOS = {
    "Contact": """
IsPersonAccount|boolean|DFGS|—|—|Somente leitura: a conta-pai é uma conta pessoal.
IsPriorityRecord|boolean|DG|59.0|—|Marca de importância definida pelo usuário; padrão false.
Jigsaw|string|CFGNSU|22.0|—|Id da empresa no Data.com; não editar.
JigsawContactId|string|FGNS|—|—|Id do contato no Data.com; não alterar.
LastActivityDate|date|FGNS|—|—|Data do evento mais recente ou da última tarefa fechada.
LastName|string|CFGSU|—|—|Sobrenome, obrigatório; até 80 caracteres.
LastReferencedDate|dateTime|FNS|—|—|Quando o usuário acessou o registro ou itens ligados a ele.
LastViewedDate|dateTime|FNS|—|—|Quando o usuário abriu o registro ou uma list view.
LeadSource|picklist|CFGNSU|—|—|Origem do lead convertido neste contato.
MailingAddress|address|FN|—|—|Endereço de correspondência composto, somente leitura.
MailingCity|string|CFGNSU|—|—|Cidade de correspondência.
MailingCountry|string|CFGNSU|—|—|País de correspondência.
MailingCountryCode|picklist|CFGNSU|—|—|Código ISO do país de correspondência.
MailingGeocodeAccuracy|picklist|CFGNRSU|—|—|Precisão da geolocalização do endereço de correspondência.
MailingLatitude|double|CFNSU|—|—|Latitude de correspondência, de -90 a 90.
MailingLongitude|double|CFNSU|—|—|Longitude de correspondência, de -180 a 180.
MailingPostalCode|string|CFGNSU|—|—|CEP de correspondência.
MailingState|string|CFGNSU|—|—|Estado ou província de correspondência.
MailingStateCode|picklist|CFGNSU|—|—|Código ISO do estado de correspondência.
MailingStreet|textarea|CFGNSU|—|—|Rua do endereço de correspondência.
MasterRecordId|reference|FGNS|—|Contact|Registro que sobreviveu à mesclagem; nulo nos demais casos.
MiddleName|string|CFGNSU|—|—|Nome do meio; até 40 caracteres.
MobilePhone|phone|CFGNSU|—|—|Celular do contato.
Name|string|FGS|—|—|Nome completo, montado a partir das partes do nome.
OtherAddress|address|FN|—|—|Endereço alternativo composto, somente leitura.
OtherCity|string|CFGNSU|—|—|Cidade alternativa.
OtherCountry|string|CFGNSU|—|—|País alternativo.
OtherCountryCode|picklist|CFGNSU|—|—|Código ISO do país alternativo.
OtherGeocodeAccuracy|picklist|CFGNRSU|—|—|Precisão da geolocalização do endereço alternativo.
OtherLatitude|double|CFNSU|—|—|Latitude alternativa, de -90 a 90.
OtherLongitude|double|CFNSU|—|—|Longitude alternativa, de -180 a 180.
OtherPhone|phone|CFGNSU|—|—|Telefone do endereço alternativo.
OtherPostalCode|string|CFGNSU|—|—|CEP alternativo.
OtherState|string|CFGNSU|—|—|Estado ou província alternativos.
OtherStateCode|picklist|CFGNSU|—|—|Código ISO do estado alternativo.
OtherStreet|textarea|CFGNSU|—|—|Rua do endereço alternativo.
OwnerId|reference|CDFGSU|—|User|Dono da conta-pai.
Phone|phone|CFGNSU|—|—|Telefone comercial.
PhotoUrl|url|FGNS|—|—|Caminho que monta a URL da imagem de perfil social.
Pronouns|picklist|CFGNRSU|—|—|Pronomes do contato, de uma lista definida pelo administrador.
RecordTypeId|reference|CFNU|—|—|Record type atribuído ao contato.
ReportsToId|reference|CFGNSU|—|Contact|Contato a quem este se reporta.
Salutation|picklist|CFGNSU|—|—|Tratamento antes do nome, como Dr. ou Sra.
ScheduledResumeDateTime|dateTime|FNS|54.0|—|Quando a cadência retoma depois de uma pausa ou espera.
Suffix|string|CFGNSU|—|—|Sufixo do nome; até 40 caracteres.
Title|string|CFGNSU|—|—|Cargo do contato, como CEO ou VP.
TitleType|picklist|CFGNRSU|—|—|Nível hierárquico, usado nos recursos de relacionamento com compradores.
""",
    "Campaign": """
NumberOfWonOpportunities|int|FGS|—|—|Número de oportunidades ganhas ligadas à campanha.
NumberSent|double|FNS|—|—|Indivíduos alcançados, como e-mails enviados.
OwnerId|reference|FGS|—|User|Dono da campanha; por padrão, o usuário logado na API.
ParentCampaign|reference|CFNU|—|—|Campanha-pai na hierarquia de campanhas.
ParentId|reference|FGNS|—|Campaign|Id da campanha-pai, se houver.
RecordTypeId|reference|CFNU|—|—|Record type atribuído à campanha.
StartDate|date|FGNS|—|—|Data de início da campanha.
Status|picklist|DFGNS|—|—|Status da campanha, como Planned ou In Progress.
TenantId|reference|FGNS|51.0|—|Business Unit do Account Engagement (somente leitura).
TotalAmountAllOpportunities|currency|F|—|—|Valor total de todas as oportunidades da hierarquia.
TotalAmountAllWonOpportunities|currency|F|—|—|Valor total das oportunidades ganhas da hierarquia.
TotalEmailsDelivered|int|F|—|—|Total de e-mails entregues.
TotalFormSubmissions|int|F|—|—|Total de envios de formulário.
TotalFormViews|int|F|—|—|Total de visualizações de formulário.
TotalLandingPageFormSubmissions|int|F|—|—|Total de envios de formulário em landing pages.
TotalLandingPageViews|int|F|—|—|Total de visualizações de landing pages.
TotalNumberofLeads|int|F|—|—|Total de leads da hierarquia, inclusive convertidos.
TotalNumberofOpportunities|int|F|—|—|Total de oportunidades da hierarquia.
TotalNumberofResponses|int|F|—|—|Total de respostas da hierarquia (status Responded).
TotalNumberofWonOpportunities|int|F|—|—|Total de oportunidades ganhas da hierarquia.
Type|picklist|DFGNS|—|—|Tipo da campanha, como Direct Mail.
UniqueEmailOpens|int|F|—|—|Aberturas únicas de e-mail.
UniqueEmailTrackedLinkClicks|int|F|—|—|Cliques únicos em links rastreados de e-mail.
UniqueMarketingLinkClicks|int|F|—|—|Cliques únicos em links de marketing.
""",
    "Quote": """
QuoteAccountId|reference|CFGNSU|58.0|Account|Conta ligada à cotação.
QuoteNumber|string|DF|—|—|Número gerado pelo sistema para a cotação.
QuoteToAddress|address|FN|—|—|Endereço composto do destinatário, somente leitura.
QuoteToCity|string|CFGNSU|—|—|Cidade do destinatário.
QuoteToCountry|string|CFGNSU|—|—|País do destinatário.
QuoteToLatitude|double|CFNSU|—|—|Latitude do endereço do destinatário.
QuoteToLongitude|double|CFNSU|—|—|Longitude do endereço do destinatário.
QuoteToName|string|CFNU|—|—|Nome de quem recebe a cotação.
QuoteToPostalCode|string|CFGNSU|—|—|CEP do destinatário.
QuoteToState|string|CFGNSU|—|—|Estado do destinatário.
QuoteToStreet|textarea|CFGNSU|—|—|Rua do destinatário.
RecordSource|picklist|FGNRS|66.0|—|Contexto da aplicação que criou o registro.
RecordTypeID|reference|CFNU|—|—|Record type atribuído.
RelatedWorkId|reference|CFGNS|—|—|Ordem de serviço que originou a cotação.
ShippingAddress|address|FN|—|—|Endereço de entrega composto, somente leitura.
ShippingCity|string|CFGNSU|—|—|Cidade de entrega.
ShippingCountry|string|CFGNSU|—|—|País de entrega.
ShippingCountryCode|picklist|CFGNSU|—|—|Código ISO do país de entrega.
ShippingHandling|currency|CFNU|—|—|Custo total de frete e manuseio.
ShippingLatitude|double|CFNSU|—|—|Latitude de entrega.
ShippingLongitude|double|CFNSU|—|—|Longitude de entrega.
ShippingName|string|CFNU|—|—|Nome de quem recebe a entrega.
ShippingPostalCode|string|CFGNSU|—|—|CEP de entrega.
ShippingState|string|CFGNSU|—|—|Estado de entrega.
ShippingStateCode|picklist|CFGNSU|—|—|Código ISO do estado de entrega.
ShippingStreet|textarea|CFGNSU|—|—|Rua de entrega.
Status|picklist|CDFNU|—|—|Situação da cotação, como rascunho ou aprovada.
Subtotal|currency|FN|—|—|Soma de preço vezes quantidade, sem descontos.
Tax|currency|CFNU|—|—|Total de impostos da cotação.
TotalPrice|currency|FN|—|—|Total dos itens depois dos descontos, antes dos impostos.
TotalPriceWithTax|currency|FNS|55.0|—|TotalPrice somado aos impostos.
TotalTaxAmount|currency|FNS|55.0|—|Valor total dos impostos.
""",
    "AgentWork": """
ShouldSkipCapacityCheck|boolean|CDFGS|—|—|Ignora a verificação de capacidade em itens roteados de fora.
SpeedToAnswer|int|FGNS|—|—|Tempo entre a solicitação e o aceite pelo agente.
Status|picklist|FGRS|—|—|Situação do item de trabalho.
TargetAcceptDateTime|dateTime|FNSU|65.0|—|Prazo para o agente aceitar o item.
TransferRequesterId|reference|CFGNSU|63.0|User|Usuário que reatribuiu o item pela ação Reassign.
UserId|reference|CFGS|—|User|Usuário a quem o item foi atribuído.
WorkItemId|reference|CFGS|—|—|Registro roteado ao agente pelo Omni-Channel, como Case, Lead ou VoiceCall.
""",
    "KnowledgeArticleVersion": """
VersionNumber|int|GS|24.0|—|Número da versão do artigo.
""",
    "Case": """
StopStartDate|dateTime|FNS|—|—|Quando o processo de entitlement foi interrompido.
""",
    "Opportunity": """
PartnerAccountId|reference|FGNS|—|—|Conta parceira do dono da oportunidade.
PricebookId|reference|CDFNU|3.0|—|Campo antigo, removido na API 8.0; use Pricebook2Id.
RecordTypeId|reference|CFNU|—|—|Record type da oportunidade.
Territory2Id|reference|CFGNSU|—|—|Território atribuído à oportunidade.
TotalOpportunityQuantity|double|CFNSU|—|—|Quantidade de itens da oportunidade.
""",
    "Account": """
FirstName|string|CFGNSU|—|—|Conta pessoal: primeiro nome.
LastName|string|CFGNSU|—|—|Conta pessoal: sobrenome.
MiddleName|string|CFGNSU|—|—|Conta pessoal: nome do meio.
PersonAssistantName|string|CFNU|—|—|Conta pessoal: nome do assistente.
PersonAssistantPhone|phone|CFNU|—|—|Conta pessoal: telefone do assistente.
PersonBirthDate|date|CFNU|—|—|Conta pessoal: data de nascimento.
PersonContactId|reference|FNU|—|—|Conta pessoal: contato ligado à conta.
PersonDepartment|string|CFNU|—|—|Conta pessoal: departamento.
PersonEmail|email|CFNU|—|—|Conta pessoal: e-mail.
PersonEmailBouncedDate|dateTime|CFNU|—|—|Conta pessoal: data da falha de entrega de e-mail.
PersonEmailBouncedReason|string|CFNU|—|—|Conta pessoal: motivo da falha de entrega.
PersonGenderIdentity|picklist|CFGNRSU|—|—|Conta pessoal: identidade de gênero.
PersonHasOptedOutOfEmail|boolean|CFNU|—|—|Conta pessoal: recusou e-mails.
PersonHomePhone|phone|CFNU|—|—|Conta pessoal: telefone residencial.
PersonLeadSource|picklist|CFNU|—|—|Conta pessoal: origem do lead.
PersonMailingAddress|address|FN|—|—|Conta pessoal: endereço de correspondência composto.
PersonMailingCity|string|CFNU|—|—|Conta pessoal: cidade de correspondência.
PersonMailingCountry|string|CFNU|—|—|Conta pessoal: país de correspondência.
PersonMailingCountryCode|picklist|CFGNSU|—|—|Conta pessoal: código ISO do país.
PersonMailingGeocodeAccuracy|picklist|NR|—|—|Conta pessoal: precisão da geolocalização.
PersonMailingLatitude|double|CFNSU|—|—|Conta pessoal: latitude de correspondência.
PersonMailingLongitude|double|CFNSU|—|—|Conta pessoal: longitude de correspondência.
PersonMailingPostalCode|string|CFNU|—|—|Conta pessoal: CEP de correspondência.
PersonMailingState|string|CFNU|—|—|Conta pessoal: estado de correspondência.
PersonMailingStateCode|picklist|CFGNSU|—|—|Conta pessoal: código ISO do estado.
PersonMailingStreet|textarea|CFNU|—|—|Conta pessoal: rua de correspondência; até 255 caracteres.
PersonMobilePhone|phone|CFNU|—|—|Conta pessoal: celular.
PersonOtherCity|string|CFNU|—|—|Conta pessoal: cidade alternativa.
PersonOtherCountry|string|CFNU|—|—|Conta pessoal: país alternativo.
PersonOtherCountryCode|picklist|CFGNSU|—|—|Conta pessoal: código ISO do país alternativo.
PersonOtherLatitude|double|CFNSU|—|—|Conta pessoal: latitude alternativa.
PersonOtherLongitude|double|CFNSU|—|—|Conta pessoal: longitude alternativa.
PersonOtherPhone|phone|CFNU|—|—|Conta pessoal: telefone alternativo.
PersonOtherPostalCode|string|CFNU|—|—|Conta pessoal: CEP alternativo.
PersonOtherState|string|CFNU|—|—|Conta pessoal: estado alternativo.
PersonOtherStateCode|picklist|CFGNSU|—|—|Conta pessoal: código ISO do estado alternativo.
PersonOtherStreet|textarea|CFNU|—|—|Conta pessoal: rua alternativa.
PersonPronouns|picklist|CFGNRSU|—|—|Conta pessoal: pronomes, de uma lista controlada.
PersonReportsToId|reference|CFGNSU|62.0|Contact|Conta pessoal: conta ou contato superior.
PersonTitle|string|CFNU|—|—|Conta pessoal: cargo; até 80 caracteres.
Suffix|string|CFGNSU|—|—|Conta pessoal: sufixo do nome; até 40 caracteres.
""",
    "User": """
IsPrmSuperUser|boolean|CDFGSU|24.0|—|Indica superusuário de parceiro.
Manager|picklist|CFRU|—|—|Lookup para escolher o gestor; impede escolher quem se reporta ao próprio usuário.
MiddleName|string|CFGNSU|—|—|Nome do meio; até 40 caracteres.
NumberOfFailedLogins|int|FGNS|—|—|Tentativas de login que falharam na interface.
PasswordExpirationDate|dateTime|FNS|63.0|—|Quando a senha expira.
PortalRole|picklist|CFGNRSU|43.0|—|Papel do usuário no portal de clientes.
StateCode|picklist|CFGNSU|—|—|Código ISO do estado.
Suffix|string|CFGNSU|—|—|Sufixo do nome; até 40 caracteres.
UserPermissionsWirelessUser|boolean|CFU|—|—|Acesso ao Wireless Edition, descontinuado.
UserPreferencesAgentGdprConsent|boolean|CFU|—|—|Consentimento para gravar e analisar chamadas.
UserPreferencesAllowConversationReminders|boolean|CFU|55.0|—|Lembretes de conversa como cartões no Lightning.
UserPreferencesAutoForwardCall|boolean|CFU|—|—|Chamadas tocam no navegador e no telefone ao mesmo tempo.
UserPreferencesDisableAutoSubForFeeds|boolean|CFU|25.0|—|Desliga seguir automaticamente os registros criados; obsoleto.
UserPreferencesDisableFeedbackEmail|boolean|CFU|54.0|—|E-mails sobre feedback do Work.com.
UserPreferencesDisableRewardEmail|boolean|CFU|—|—|E-mails sobre recompensas do Work.com.
UserPreferencesDisableWorkEmail|boolean|CFU|—|—|Bloqueia e-mails de feedback, metas e coaching.
UserPreferencesEnableVoiceCallRecording|boolean|CFU|—|—|Liga a gravação de chamadas de voz.
UserPreferencesEnableVoiceLocalPresence|boolean|CFU|—|—|Mostra números locais no Sales Dialer.
UserPreferencesOptOutOfTouch|boolean|CFU|29.0|—|Desliga o acesso automático ao app Touch no iPad; obsoleto.
UserPreferencesOutboundBridge|boolean|CFU|—|—|Ligações saem pelo telefone do usuário.
UserPreferencesProcessAssistantCollapsed|boolean|CFU|33.0|—|Caminho de vendas recolhido (só nas APIs 33.0 e 34.0).
WirelessEmail|email|CFGNSU|—|—|E-mail usado no Wireless Edition.
""",
    "EntityDefinition": """
ApexTriggers|QueryResult|FGNS|34.0|—|Triggers Apex do objeto.
AssignmentRules|QueryResult|FGNS|34.0|—|Regras de atribuição do objeto.
AutoResponseRules|QueryResult|FGNS|34.0|—|Regras de resposta automática do objeto.
BusinessProcesses|QueryResult|FGNS|34.0|—|Business processes do objeto.
ChildRelationships|QueryResult|FGNS|34.0|—|Relacionamentos filhos do objeto.
CompactLayouts|QueryResult|FGNS|34.0|—|Compact layouts do objeto.
CustomFields|QueryResult|FGNS|34.0|—|Campos customizados do objeto.
DefaultCompactLayout|CompactLayoutInfo|CNU|—|—|Compact layout padrão, se houver.
DefaultCompactLayoutId|string|FGNS|—|—|Id do compact layout padrão.
DefaultImplementation|string|FGNS|—|—|Reservado para uso futuro.
DetailUrl|string|FGNS|34.0|—|URL da página de detalhe, somente leitura.
EditDefinitionUrl|string|FGNS|34.0|—|URL de edição da definição; a página não descreve o campo.
EditUrl|string|FGNS|34.0|—|URL usada para editar a definição do objeto.
ExtendedBy|string|FGNS|—|—|Reservado para uso futuro.
ExtendsInterfaces|string|FGNS|—|—|Reservado para uso futuro.
ExternalSharingModel|picklist|FGRS|38.0|—|Modelo de compartilhamento externo.
FieldSets|QueryResult|FGNS|—|—|Field sets do objeto.
Fields|QueryResult|FGNS|—|—|Campos padrão e customizados do objeto.
FormulaVariables|QueryResult|FGNS|48.0|—|Fórmulas construídas sobre o objeto.
HelpSettingPageName|string|FGNS|34.0|—|Nome da página de ajuda customizada.
HelpSettingPageUrl|string|FGNS|34.0|—|URL da página de ajuda customizada.
ImplementedBy|string|FGNS|—|—|Reservado para uso futuro.
ImplementsInterfaces|string|FGNS|—|—|Reservado para uso futuro.
InternalSharingModel|picklist|FGRS|38.0|—|Modelo de compartilhamento interno.
IsActivityTrackable|boolean|DFGS|37.0|—|Permite registrar tarefas e eventos do objeto.
IsApexTriggerable|boolean|DFGS|—|—|Permite triggers Apex no objeto.
IsAutoActivityCaptureEnabled|boolean|DFGS|41.0|—|Captura automática de atividades do Einstein ligada.
IsCompactLayoutable|boolean|DFGS|—|—|Aceita compact layouts.
IsCreatable|boolean|DFGS|—|—|Permite criar registros; indisponível a partir da API 35.0.
IsDeletable|boolean|DFGS|—|—|Permite excluir; indisponível a partir da API 35.0.
IsDeprecatedAndHidden|boolean|DFGS|35.0|—|Objeto indisponível na versão atual.
IsEverCreatable|boolean|DFGS|35.0|—|Pode ser criado pela API, conforme permissões.
IsEverDeletable|boolean|DFGS|35.0|—|Pode ser excluído pela API, conforme permissões.
IsEverUpdatable|boolean|DFGS|35.0|—|Pode ser alterado pela API, conforme permissões.
IsFeedEnabled|boolean|DFGS|34.0|—|Feed do Chatter ligado para o objeto.
IsFieldHistoryTracked|boolean|DFGS|37.0|—|Rastreia mudanças de campos.
IsFlsEnabled|boolean|DFGS|35.0|—|Aceita segurança em nível de campo.
IsIdEnabled|boolean|DFGS|35.0|—|Permite Id no SELECT.
IsInterface|boolean|DFGS|—|—|Reservado para uso futuro.
IsLayoutable|boolean|DFGS|35.0|—|Aceita page layouts.
IsMruEnabled|boolean|DFGS|37.0|—|Lista de itens recentes ligada.
IsReplicateable|boolean|DFGS|35.0|—|Pode ser replicado.
IsReportingEnabled|boolean|DFGS|37.0|—|Dados disponíveis em relatórios.
IsRetrieveable|boolean|DFGS|35.0|—|Pode ser recuperado.
IsSearchable|boolean|DFGS|35.0|—|Registros indexados para busca.
IsSearchLayoutable|boolean|DFGS|35.0|—|Aceita layouts de busca customizados.
IsTriggerable|boolean|DFGS|35.0|—|Aceita triggers.
IsWorkflowEnabled|boolean|DFGS|—|—|Aceita regras de workflow.
Layouts|QueryResult|FGNS|34.0|—|Page layouts do objeto.
Limits|QueryResult|FGNS|34.0|—|Limites do objeto.
LookupFilters|QueryResult|FGNS|34.0|—|Filtros de lookup do objeto.
NewUrl|string|FGNS|34.0|—|URL para criar um registro.
OwnerChangeOptions|QueryResult|FGNS|35.0|—|Opções de troca de dono; só em subconsultas.
Particles|QueryResult|FGNS|34.0|—|Partículas do objeto.
PluralLabel|string|FGNS|—|—|Rótulo no plural.
Publisher|Publisher|CNU|34.0|—|Quem publicou o objeto: Salesforce, usuário ou pacote.
PublisherId|string|FGNS|34.0|—|Id de quem publicou.
QualifiedApiName|string|FGS|—|—|Nome único com namespace (NamespacePrefix__DeveloperName).
QuickActionDefinitions|QueryResult|FGNS|34.0|—|Ações rápidas do objeto.
RecordTypes|QueryResult|FGNS|34.0|—|Record types do objeto; só em subconsultas.
RecordTypesSupported|RecordTypesSupported|N|34.0|—|Record types associados ao objeto.
RelatedListDefinitions|QueryResult|FGNS|55.0|—|Related lists do objeto.
RelationshipDomains|QueryResult|FGNS|34.0|—|Relacionamentos com outros objetos.
RunningUserEntityAccess|UserEntityAccess|CNU|34.0|—|Acesso do usuário atual ao objeto.
RunningUserEntityAccessId|string|FGNS|34.0|—|Id do registro de acesso.
SearchLayouts|QueryResult|FGNS|34.0|—|Layouts de busca do objeto.
StandardActions|QueryResult|FGNS|34.0|—|Ações padrão do objeto.
ValidationRules|QueryResult|FGNS|34.0|—|Regras de validação do objeto.
WebLinks|QueryResult|FGNS|34.0|—|Botões e links do objeto.
WorkflowAlerts|QueryResult|FGNS|34.0|—|Alertas de workflow do objeto.
WorkflowFieldUpdates|QueryResult|FGNS|34.0|—|Atualizações de campo de workflow.
WorkflowOutboundMessages|QueryResult|FGNS|34.0|—|Mensagens de saída de workflow.
WorkflowTasks|QueryResult|FGNS|34.0|—|Tarefas de workflow do objeto.
""",
    "FieldDefinition": """
BusinessOwnerId|reference|FGNS|45.0|—|Pessoa ou grupo responsável pelo campo.
BusinessStatus|picklist|FGNS|45.0|—|Se o campo está em uso.
CompactLayoutItems|QueryResult|FGS|34.0|—|Itens de compact layout ligados ao campo.
ComplianceGroup|multipicklist|FN|47.0|—|Normas de conformidade ligadas aos dados.
ControlledFields|QueryResult|FGS|34.0|—|Campos controlados, em picklists dependentes.
ControllingFieldDefinition|FieldDefinition|FGS|14.0|—|Campo controlador de um picklist dependente.
ControllingFieldDefinitionId|string|FGS|34.0|—|Id do campo controlador.
EntityDefinition|EntityDefinition|FGS|—|—|Objeto que contém o campo.
ExtraTypeInfo|string|FGS|34.0|—|Detalhe adicional do tipo do campo.
IsApiFilterable|boolean|DFGS|34.0|—|Pode ser usado em filtros de consulta.
IsApiGroupable|boolean|DFGS|34.0|—|Pode ser usado em GROUP BY.
IsApiSortable|boolean|DFGS|34.0|—|Pode ordenar consultas.
IsCalculated|boolean|DFGS|34.0|—|O valor é calculado.
IsCompactLayoutable|boolean|DFGS|34.0|—|Pode entrar num compact layout.
IsCompound|boolean|DFGS|38.0|—|É composto por outros campos.
IsEverApiAccessible|boolean|DFGS|49.0|—|Aparece no describe da API.
IsFieldHistoryTracked|boolean|DFGS|34.0|—|Histórico rastreado.
IsFlsEnabled|boolean|DFGS|35.0|—|Aceita segurança em nível de campo.
IsHighScaleNumber|boolean|DFGS|34.0|—|Guarda números com oito casas decimais.
IsHtmlFormatted|boolean|DFGS|34.0|—|Contém HTML.
IsIndexed|boolean|DFGS|35.0|—|É indexado no banco de dados.
IsListFilterable|boolean|DFGS|34.0|—|Pode filtrar uma related list.
IsListSortable|boolean|DFGS|34.0|—|Pode ordenar uma related list.
IsListVisible|boolean|DFGS|34.0|—|Pode aparecer numa related list.
IsNameField|boolean|DFGS|34.0|—|É o campo de nome.
IsPolymorphicForeignKey|boolean|DFGS|41.0|—|Chave estrangeira para vários tipos de objeto.
IsSearchPrefilterable|boolean|DFGS|40.0|—|Aceita pré-filtro em SOSL.
IsWorkflowFilterable|boolean|DFGS|34.0|—|Pode filtrar workflow.
LookupFilters|QueryResult|FGNS|34.0|—|Filtros de lookup ligados ao campo.
MasterLabel|string|FGS|—|—|Rótulo interno, sem tradução.
NamespacePrefix|string|FGS|—|—|Namespace do objeto.
Particles|QueryResult|FGS|34.0|—|EntityParticles ligados ao campo.
Precision|int|FGS|34.0|—|Máximo de dígitos.
Publisher|Publisher|FGS|34.0|—|Quem publicou o campo: Salesforce, usuário ou pacote.
PublisherId|string|FGS|34.0|—|Id de quem publicou.
ReferenceTargetField|string|FGS|34.0|—|Campo do objeto-pai usado na correspondência.
ReferenceTo|RelationshipReferenceTo|FGS|34.0|—|Tipos de objeto que o campo pode referenciar.
RelationshipDomains|QueryResult|FGS|34.0|—|Relacionamentos do campo.
RunningUserFieldAccessId|string|—|34.0|—|Uso interno.
Scale|int|FGS|34.0|—|Dígitos depois da vírgula.
SecurityClassification|picklist|FGNS|45.0|—|Sensibilidade dos dados do campo.
ServiceDataType|DataType|FGS|34.0|—|Tipo de dado de serviço do campo.
ServiceDataTypeId|string|FGS|34.0|—|Id do ServiceDataType; só por compatibilidade.
ServiceDataTypes|QueryResult|FGS|34.0|—|ServiceDataTypes ligados ao campo.
ValueType|DataType|FGS|35.0|—|Tipo de dado do campo.
ValueTypeId|string|FGS|35.0|—|Id do tipo de valor.
WorkflowFieldUpdates|QueryResult|FGS|34.0|—|Atualizações de campo de workflow.
""",
}

NOTAS = {
    "Contact": "Tabela lida até o fim em duas partes (116 mil caracteres): termina em TitleType.",
    "Campaign": "Tabela lida até o fim: termina em UniqueMarketingLinkClicks.",
    "Quote": "Tabela lida até o fim: termina em TotalTaxAmount.",
    "AgentWork": "Tabela lida até o fim: 48 linhas, terminando em WorkItemId.",
    "KnowledgeArticleVersion": "Tabela lida até o fim: 42 linhas, terminando em VersionNumber.",
    "Case": "Tabela da Object Reference lida até o fim (50 linhas, terminando em Type), mais os nomes padrão que só a Field Reference traz "
            "(Id e campos de auditoria). EntityId não aparece em nenhuma das duas.",
    "Opportunity": "Tabela da Object Reference lida até o fim (55 linhas e uma linha vazia depois de AccountId, terminando em Type), mais os nomes que só "
                   "a Field Reference traz (como OpportunityScoreId, ReferralCode, Id e campos de auditoria).",
    "Lead": "Tabela lida até o fim em duas partes (150 mil caracteres): 74 nomes, de ActionCadenceAssigneeId a Website.",
    "Account": "Tabela principal (76) e tabela de campos de conta pessoal (IsPersonAccount Fields, 41 nomes) lidas até o fim (106 mil caracteres).",
    "User": "Tabela da Object Reference lida até o fim em três partes (268 mil caracteres): termina em WirelessEmail. Também entram os nomes que só "
            "a Field Reference traz (como Id) e WorkspaceId, que só existe na Tooling API.",
    "Product2": "Tabela lida até o fim: 37 linhas, de BillingPolicyId a UnitOfMeasureId; nenhum campo faltava.",
    "Entitlement": "Tabela lida até o fim: 22 campos nomeados e uma linha vazia, sem nome, tipo nem descrição.",
    "QueueRoutingConfig": "Tabela lida até o fim: 14 campos nomeados e uma linha vazia (a 9ª), sem nome, tipo nem descrição.",
    "EventLogFile": "Tabela de 8 linhas, todas cadastradas. A introdução da página cita Interval e Sequence (API 37.0), mas eles não têm linha na tabela.",
    "EntityDefinition": "Tabela da Tooling API lida até o fim em duas partes (145 mil caracteres): termina em WorkflowTasks.",
    "FieldDefinition": "Tabela da Tooling API lida até o fim em duas partes (184 mil caracteres), com leitura extra na junção: termina em "
                       "WorkflowFieldUpdates.",
    "CustomField": "Tabela da Tooling API conferida: 6 campos, todos cadastrados.",
    "CustomObject": "Tabela da Tooling API conferida: 10 campos, todos cadastrados.",
}
CONVENCAO = {  # objetos cujo único motivo de parcial era a ausência de Id e campos de sistema, que a tabela não lista
    "PermissionSet": "Tabela de campos completa, menos os Permissions*, que são dinâmicos (ver domínio dinâmico de campos).",
    "PermissionSetAssignment": "Tabela de campos completa.", "PermissionSetGroup": "Tabela de campos completa.",
    "Profile": "Tabela de campos completa, menos os Permissions*, que são dinâmicos (ver domínio dinâmico de campos).",
    "RecordType": "Tabela de campos completa.", "UserLogin": "Tabela de campos completa.",
    "LoginHistory": "Tabela de campos completa. A página não declara o tempo de retenção.",
}
ID_SISTEMA = " Id e campos de sistema que a tabela não lista não foram cadastrados (convenção do catálogo)."


def props_letras(s):
    return "".join(ch for ch in s if ch in "CDFGNRSUI") if s != "—" else ""


resumo = {}
for nome, src in SRC.items():
    rel = f"objetos-api/{nome}.json"
    d = ld(rel)
    existentes = {c["nome"] for c in d["campos"]}
    novos = 0
    for linha in NOVOS.get(nome, "").strip().splitlines():
        n, t, pr, ver, ref, desc = [x.strip() for x in linha.split("|")]
        if n in existentes:
            continue
        kw = {}
        if ref != "—" and ref in EXISTE:
            kw["ref"] = [f"obj:{ref}"]
        if nome == "Opportunity" and n == "PricebookId":
            kw["ate"] = "7.0"
        d["campos"].append(O.field(f"obj:{nome}", n, t, props_letras(pr), None if ver == "—" else ver, desc, src, **kw))
        existentes.add(n)
        novos += 1
    d["campos"].sort(key=lambda c: c["nome"].lower())
    if not any(e.get("fonte") == src for e in d["evidencias"]):
        d["evidencias"].append(ev(src))
    n_ = len(d["campos"])
    d["cobertura"]["estrutural"] = {"estado": "completa", "esperado": n_, "presente": n_, "nota": NOTAS[nome] + ID_SISTEMA}
    d["cobertura"]["explicativa"] = {"estado": "completa" if O.cnt(d["campos"]) == n_ else "parcial", "esperado": n_, "presente": O.cnt(d["campos"])}
    sv(rel, d)
    resumo[nome] = (novos, n_)
for nome, nota in CONVENCAO.items():
    rel = f"objetos-api/{nome}.json"
    d = ld(rel)
    n_ = len(d["campos"])
    est = d["cobertura"]["estrutural"]
    tooling = est.get("nota", "").split(" Tooling API (2026-11-17):")
    d["cobertura"]["estrutural"] = {"estado": "completa", "esperado": n_, "presente": n_,
                                    "nota": nota + ID_SISTEMA + ((" Tooling API (2026-11-17):" + tooling[1]) if len(tooling) > 1 else "")}
    sv(rel, d)
    resumo[nome] = (0, n_)

# nota de extração: lista dos campos de cada objeto relido
ls = ["", "-- Lista de campos transcrita da leitura (gerada por lote7p_b5_objetos.py; nome | tipo)"]
for nome, src in SRC.items():
    ls.append(f"[{src}] objeto {nome}: " + ", ".join(f"{c['nome']} | {c['tipo_tecnico']}" for c in ld(f"objetos-api/{nome}.json")["campos"]))
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(ls) + "\n")
print("lote 7p:", resumo)
