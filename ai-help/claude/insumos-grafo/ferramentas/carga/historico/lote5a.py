# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5a (issue #24): integração, APIs e eventos — credenciais, endpoints, eventos, External Services, objetos externos, Auth Providers.
import json
import b2_mdt as M
from b1_base import ev, af

BASE = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/"
CAT = BASE + "catalogo/"
DATA = "2026-11-09"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")

# ================================================================ fontes
reg = json.load(open(BASE + "fontes/registro.json"))
B = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
CHK = {"estado": "verificado", "nota": f"Conteúdo lido em {DATA} e conferido quanto ao assunto (não apenas HTTP 200)."}
PG = {"NamedCredential": "meta_namedcredential.htm", "ExternalCredential": "meta_externalcredential.htm", "RemoteSiteSetting": "meta_remotesitesetting.htm",
      "CspTrustedSite": "meta_csptrustedsite.htm", "CorsWhitelistOrigin": "meta_corswhitelistorigin.htm", "PlatformEventChannel": "meta_platformeventchannel.htm",
      "PlatformEventChannelMember": "meta_platformeventchannelmember.htm", "PlatformEventSubscriberConfig": "meta_platformeventsubscriberconfig.htm",
      "ExternalServiceRegistration": "meta_externalserviceregistration.htm", "ExternalDataSource": "meta_externaldatasource.htm", "AuthProvider": "meta_authproviders.htm"}
novas = [{"id": f"src:mdapi-{n.lower()}", "titulo": f"{n} (Metadata API)", "url": B + pg, "tipo": "oficial_documentacao", "versao": "68.0",
          "data_verificacao": DATA, "metodo": "extracao_documental_assistida", "pertinencia": f"Arquivo, versão e propriedades do tipo {n}.",
          "extracao": "fontes/extracoes/mdapi-lote5a.txt", "checagem_online": CHK} for n, pg in PG.items()]
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

def P(n, t, ver=None, d=None, req="N", **kw): return (n, t, req, ver, d, kw)
DF = ("valor", "false", None)
DT = ("valor", "true", None)
FN = lambda: M.FULLNAME_HERDADO(None)
LEG = {"notas": ["Obsoleto desde 56.0: só vale para named credentials do tipo Legacy."]}
INT = {"notas": ["Reservado para uso interno da Salesforce (página oficial)."]}
def V(*vals): return [(v, None) for v in vals]
SETUP_NV = af("desconhecido", None, "Caminho no Setup não verificado nesta sessão.")

# ================================================================ estruturas
S = "src:mdapi-namedcredential"
M.struct("NamedCredentialParameter", S, ["mdt:NamedCredential"], [
 P("certificate", "string", "56.0", "Certificado usado quando parameterType é ClientCertificate."),
 P("description", "string", "56.0", "Descrição do parâmetro."),
 P("externalCredential", "string", "56.0", "Credencial externa usada quando parameterType é Authentication."),
 P("globalNamedPrincipalCredential", "boolean", "56.0", "Reservado.", **INT),
 P("managedFeatureEnabledCallout", "boolean", "56.0", "Reservado.", **INT),
 P("outboundNetworkConnection", "string", "56.0", "Conexão de rede de saída, usada com o tipo PrivateEndpoint."),
 P("parameterName", "string", "56.0", "Nome do parâmetro (para HttpHeader, o nome do cabeçalho).", "S"),
 P("parameterType", "string", "56.0", "O que o parâmetro configura; vários valores são reservados.", "S",
   vals=V("AllowedManagedPackageNamespaces", "Authentication", "ClientCertificate", "ConnectionStatus", "CreatedByNamespace", "CustomParameter", "HttpHeader",
          "ManagedByComponent", "ManagedByFeature", "ManagedByNamespace", "NamedCredentialOptions", "OutboundNetworkConnection", "SfHttpRequestExtensionName",
          "StandardNamedCredentialType", "Url")),
 P("parameterValue", "string", "56.0", "Valor literal do parâmetro, por exemplo uma URL."),
 P("readOnlyNamedCredential", "boolean", "56.0", "Reservado.", **INT),
 P("sequenceNumber", "int", "56.0", "Ordem dos parâmetros do tipo HttpHeader."),
 P("systemUserNamedCredential", "boolean", "56.0", "Reservado.", **INT)],
 "Parâmetro de uma named credential: URL, cabeçalho HTTP, certificado ou a credencial externa usada na autenticação.")
S = "src:mdapi-externalcredential"
M.struct("ExternalCredentialParameter", S, ["mdt:ExternalCredential"], [
 P("authProvider", "string", None, "Auth provider que conduz o login e a autorização."),
 P("certificate", "string", None, "Certificado usado quando parameterType é SigningCertificate."),
 P("description", "string", None, "Descrição do parâmetro."),
 P("externalAuthIdentityProvider", "string", None, "Provedor de identidade de autenticação externa ligado à credencial; a página o recomenda no lugar de authProvider."),
 P("parameterGroup", "string", None, "Liga o parâmetro a um principal; o padrão depende do tipo do parâmetro."),
 P("parameterName", "string", None, "Nome do parâmetro (para AuthHeader, o nome do cabeçalho).", "S"),
 P("parameterType", "string", None, "Como o parâmetro se comporta.", "S",
   vals=V("AdditionalRefreshStatusCode", "AuthHeader", "AuthParameter", "AuthProtocolVariant", "AuthProvider", "AuthProviderUrl", "AuthProviderUrlQueryParameter",
          "AwsStsPrincipal", "CreatedByNamespace", "CustomPrincipal", "ExternalAuthIdentityProvider", "GlobalNamedPrincipal", "JwtBodyClaim", "JwtHeaderClaim",
          "ManagedByComponent", "ManagedByFeature", "NamedPrincipal", "PerUserPrincipal", "PrincipalIdentityAlias", "SfHttpRequestExtensionName",
          "SigningCertificate", "SystemUserPrincipal")),
 P("parameterValue", "string", None, "Valor literal, quando o tipo do parâmetro é literal."),
 P("principal", "string", "56.0", "Permission set que definia quem usava as credenciais; removido.", ate="57.0", nota_versao="Disponível só na 56.0; removido a partir da 58.0."),
 P("sequenceNumber", "int", None, "Prioridade entre principals quando o usuário se enquadra em vários; menor vale primeiro. Só para NamedPrincipal.")],
 "Parâmetro de uma credencial externa: principal, cabeçalho, claim de JWT, certificado ou provedor de autenticação.")
S = "src:mdapi-platformeventchannel"
M.struct("PlatformEventChannelSelectedEntity", S, ["mdt:PlatformEventChannel"], [
 P("selectedEntity", "string", "45.0", "Nome do evento de alteração da entidade selecionada.", "S", ate="46.0")],
 "Entidade selecionada para captura de alterações; existiu só nas versões 45.0 e 46.0.")
S = "src:mdapi-platformeventchannelmember"
M.struct("EnrichedField", S, ["mdt:PlatformEventChannelMember"], [P("name", "string", None, "Nome do campo incluído no evento de alteração.")],
 "Campo que enriquece os eventos de alteração, enviado mesmo sem ter mudado.")
S = "src:mdapi-externalserviceregistration"
M.struct("ExternalServiceOperation", S, ["mdt:ExternalServiceRegistration"], [
 P("active", "boolean", None, "Se a operação está habilitada.", "S"), P("name", "string", None, "Nome da operação.", "S")],
 "Operação do serviço externo registrada a partir da especificação.")
S = "src:mdapi-externaldatasource"
M.struct("CustomHttpHeaders", S, ["mdt:ExternalDataSource"], [
 P("description", "string", "43.0", "Para que serve o cabeçalho."),
 P("headerFieldName", "string", "43.0", "Nome do cabeçalho HTTP.", "S"),
 P("headerFieldValue", "string", "43.0", "Fórmula que calcula o valor; vazio ou nulo omite o cabeçalho.", "S"),
 P("isActive", "boolean", "43.0", "Se o cabeçalho está em uso.")],
 "Cabeçalho HTTP customizado para conectores OData 2.0 ou 4.0.")
M.struct("ExternalDataSrcDescriptors", S, ["mdt:ExternalDataSource"], [
 P("customObject", "string", "55.0", "Objeto externo ao qual o descritor se aplica."),
 P("descriptor", "string", "55.0", "Documento com os metadados.", "S"),
 P("descriptorVersion", "string", "55.0", "Versão do esquema; permite vários descritores ativos."),
 P("developerName", "string", "55.0", "Nome único do descritor.", "S"),
 P("externalDataSource", "string", "55.0", "Fonte de dados externa dona do descritor.", "S"),
 P("subtype", "string", "55.0", "Finalidade: guardar metadados ou personalizar consultas.", "S", vals=V("SchemaTableMetadata", "SchemaTableQualifiers")),
 P("systemVersion", "int", "55.0", "Versão do formato do descritor.", "S"),
 P("type", "string", "55.0", "Tipo do descritor.", "S", vals=V("Schema"))],
 "Descritor de esquema dos adaptadores Amazon DynamoDB (55.0) e Amazon Athena (56.0).")
S = "src:mdapi-authprovider"
M.struct("AuthProvParamFwdAllowlist", S, ["mdt:AuthProvider"], [
 P("description", "string", None, "Descrição do parâmetro permitido."), P("param", "string", None, "Nome do parâmetro repassado (ex.: ui_locales, login_hint).")],
 "Parâmetro de URL permitido para repasse à URL de autorização (até 10).")

# ================================================================ metadata types
def MT(nome, o, f, desde, rows, **kw):
    return M.mdt(nome, f"src:mdapi-{nome.lower()}", o, f, desde, rows, setup=SETUP_NV, **kw)

MT("NamedCredential", "Define o endpoint de um sistema externo e como chegar a ele numa chamada (callout).",
   "Separar a URL e a autenticação do código: o Apex ou o Flow chamam 'callout:Nome' e a plataforma cuida do endereço e das credenciais.", "33.0", [
 P("allowMergeFieldsInBody", "boolean", "41.0", "Permite ao Apex preencher o corpo da requisição com dados da org via campos de mesclagem.", default=DF),
 P("allowMergeFieldsInHeader", "boolean", "41.0", "Permite ao Apex preencher cabeçalhos HTTP via campos de mesclagem.", default=DF),
 P("authProvider", "string", "46.0", "Auth provider usado na autenticação.", **LEG),
 P("authTokenEndpointUrl", "string", "46.0", "URL onde o JWT é trocado por um token de acesso.", **LEG),
 P("awsAccessKey", "string", "46.0", "Primeira parte da chave AWS usada para assinar (SigV4).", **LEG),
 P("awsAccessSecret", "string", "46.0", "Segunda parte da chave AWS usada para assinar.", **LEG),
 P("awsRegion", "string", "46.0", "Região AWS acessada.", **LEG), P("awsService", "string", "46.0", "Serviço AWS acessado.", **LEG),
 P("calloutStatus", "string", "59.0", "Se a credencial pode ser usada em callouts.", vals=V("Disabled", "Enabled")),
 P("certificate", "string", None, "Certificado de cliente para SSL de duas vias e assinatura.", **LEG),
 P("description", "string", None, "Descrição livre."), P("endpoint", "string", None, "URL ou URL-raiz do endpoint.", **LEG),
 P("generateAuthorizationHeader", "boolean", "41.0", "Se a plataforma gera o cabeçalho de autorização automaticamente.", default=DT),
 P("jwtAudience", "string", None, "Destinatários do JWT.", **LEG), P("jwtFormulaSubject", "string", "46.0", "Fórmula do assunto do JWT por usuário.", **LEG),
 P("jwtIssuer", "string", "46.0", "Emissor do JWT.", **LEG), P("jwtSigningCertificate", "string", "46.0", "Certificado de assinatura do JWT.", **LEG),
 P("jwtTextSubject", "string", "46.0", "Assunto fixo do JWT.", **LEG), P("jwtValidityPeriodSeconds", "int", "46.0", "Validade do JWT em segundos.", **LEG),
 P("label", "string", None, "Nome exibido na interface.", "S"),
 P("namedCredentialParameters", "NamedCredentialParameter[]", "56.0", "Parâmetros que configuram a credencial (URL, cabeçalhos, credencial externa etc.).", estrutura="NamedCredentialParameter"),
 P("namedCredentialType", "string", "56.0", "Tipo e comportamento da credencial.",
   vals=[("Legacy", "modelo anterior à 56.0"), ("PrivateEndpoint", None), ("SecuredEndpoint", None), ("Standard", "uso interno")]),
 P("oauthRefreshToken", "string", None, "Token de renovação.", **LEG), P("oauthScope", "string", None, "Escopo solicitado.", **LEG),
 P("oauthToken", "string", None, "Token de acesso.", **LEG), P("outboundNetworkConnection", "string", "49.0", "Conexão de rede de saída para callouts AWS.", **LEG),
 P("password", "string", None, "Senha de acesso ao sistema externo.", **LEG),
 P("principalType", "string", None, "Uma credencial para todos ou uma por usuário.", vals=V("Anonymous", "NamedUser", "PerUser"), **LEG),
 P("protocol", "string", None, "Método de autenticação.", vals=V("AwsSv4", "Jwt", "JwtExchange", "NoAuthentication", "Oauth", "Password"), **LEG),
 P("username", "string", None, "Usuário de acesso ao sistema externo.", **LEG), FN()], curinga=True,
 alertas=["Desde a 56.0, a autenticação fica numa ExternalCredential, referenciada por um parâmetro do tipo Authentication; os campos de autenticação diretos valem só para o tipo Legacy.",
          "O exemplo XML da página foi servido truncado e não foi copiado."])
MT("ExternalCredential", "Define como a org se autentica num sistema externo: protocolo, principals e parâmetros.",
   "Reaproveitar a mesma autenticação em várias named credentials e controlar quem pode usá-la.", "56.0", [
 P("authenticationProtocol", "string", None, "Método de autenticação usado para chegar ao sistema externo.", "S",
   vals=[("AwsSv4", None), ("Basic", None), ("Custom", None), ("Jwt", "reservado"), ("JwtExchange", "reservado"), ("NoAuthentication", "reservado"), ("Oauth", None), ("Password", "reservado")]),
 P("description", "string", None, "Descrição livre."),
 P("externalCredentialParameters", "ExternalCredentialParameter[]", None, "Conjuntos de parâmetros que completam a configuração.", estrutura="ExternalCredentialParameter"),
 P("label", "string", None, "Nome da credencial.", "S"), FN()], curinga=True,
 alertas=["O acesso dos usuários aos principals é dado por permission sets (o campo principal, que fazia isso no XML, só existiu na 56.0)."])
MT("RemoteSiteSetting", "Registra um site externo que o código da org pode chamar.",
   "Liberar callouts do Apex (e de outros recursos) para um endereço que não usa named credential.", "19.0", [
 P("description", "string", None, "Para que serve o site remoto."),
 P("disableProtocolSecurity", "boolean", None, "Permite que o código acesse o site por HTTP ou HTTPS indistintamente; use só entendendo o risco.", "S"),
 ("fullName", "string", "?", None, "Nome único do registro: letras e sublinhados, começando por letra, sem sublinhado final ou duplo.", {"herdada": "Metadata"}),
 P("isActive", "boolean", None, "Liga ou desliga o registro.", "S"), P("url", "string", None, "Endereço do site remoto.", "S")], curinga=True,
 recs=[{"texto": "Prefira named credentials para callouts: elas já liberam o endpoint e guardam a autenticação.", "natureza": "preferencia_projeto"}])
CSP_SRC = "Libera o carregamento a partir deste site"
MT("CspTrustedSite", "Registra um site externo como confiável para a política de segurança de conteúdo (CSP) da org.",
   "Permitir que páginas Lightning, sites e Visualforce carreguem scripts, imagens, fontes, frames ou mídia de um domínio externo.", "39.0", [
 P("canAccessCamera", "boolean", "59.0", "Permite ao site usar a câmera; só vale com a política de permissões habilitada nas configurações de segurança.", default=DF),
 P("canAccessMicrophone", "boolean", "59.0", "Permite ao site usar o microfone; mesma condição da câmera.", default=DF),
 P("context", "string", "44.0", "Em que contextos as diretivas valem.",
   vals=[("All", None), ("Communities", None), ("FieldServiceMobileExtension", "desde 47.0"), ("LEX", None), ("LightningOut", "desde 64.0; reservado"), ("VisualForce", "desde 55.0")]),
 P("description", "string", None, "Descrição da URL confiável."),
 P("endpointUrl", "string", None, "URL do site confiável (https:// para APIs; wss:// para WebSocket; curinga * permitido).", "S"),
 P("isActive", "boolean", None, "Liga ou desliga o site confiável.", "S", default=DT),
 P("isApplicableToConnectSrc", "boolean", "48.0", f"{CSP_SRC} por script (connect-src).", default=DF),
 P("isApplicableToFontSrc", "boolean", "48.0", f"{CSP_SRC}: fontes.", default=DF),
 P("isApplicableToFrameSrc", "boolean", "48.0", f"{CSP_SRC}: conteúdo em iframe.", default=DF),
 P("isApplicableToImgSrc", "boolean", "48.0", f"{CSP_SRC}: imagens.", default=DF),
 P("isApplicableToMediaSrc", "boolean", "48.0", f"{CSP_SRC}: áudio e vídeo.", default=DF),
 P("isApplicableToStyleSrc", "boolean", "48.0", f"{CSP_SRC}: folhas de estilo.", default=DF),
 P("mobileExtension", "string", None, "Reservado para uso futuro.", **INT), FN()], curinga=True,
 alertas=["A partir da 59.0, ao menos um campo isApplicableTo* ou canAccess* precisa ser true em cada URL confiável."])
MT("CorsWhitelistOrigin", "Registra uma origem (domínio) que pode chamar as APIs da org a partir do navegador (CORS).",
   "Permitir que JavaScript de um site externo faça requisições às APIs REST da org.", "32.0", [
 P("urlPattern", "string", None, "Origem permitida: https:// mais domínio e porta opcional; curinga só antes do domínio de segundo nível; extensões de navegador desde 53.0; IP permitido."), FN()],
 curinga=True, divergencias=[
   "O exemplo XML da página (src:mdapi-corswhitelistorigin) usa o elemento developerName, que não aparece na tabela de campos.",
   "A página grafa a pasta e o sufixo em minúsculas (corswhitelistorigins/.corswhitelistorigin); o registro do Salesforce CLI (src:sdr-registry) usa corsWhitelistOrigins/.corsWhitelistOrigin."])
MT("PlatformEventChannel", "Define um canal que agrupa eventos: de captura de alterações ou de plataforma.",
   "Criar canais customizados (MeuCanal__chn) para assinar só os eventos que interessam a um sistema.", "45.0", [
 P("channelMembers", "PlatformEventChannelSelectedEntity[]", "45.0", "Entidades do canal; substituído por componentes PlatformEventChannelMember.", ate="46.0", estrutura="PlatformEventChannelSelectedEntity"),
 P("channelType", "string", None, "Tipo de canal.", "S", vals=[("data", "captura de alterações (Change Data Capture)"), ("event", "eventos de plataforma")]),
 P("eventType", "string", "61.0", "Tipo de evento que o canal aceita (um só por canal).", vals=[("custom", None), ("data", None), ("monitoring", None), ("standard", "uso interno")]),
 P("label", "string", None, "Rótulo do canal.", "S"), FN()], curinga=True)
MT("PlatformEventChannelMember", "Inclui uma entidade num canal de eventos (por exemplo, AccountChangeEvent em ChangeEvents).",
   "Escolher quais objetos geram eventos de alteração e, opcionalmente, filtrar ou enriquecer esses eventos.", "47.0", [
 P("enrichedFields", "EnrichedField[]", "51.0", "Campos enviados em eventos de atualização e exclusão mesmo sem terem mudado.", estrutura="EnrichedField"),
 P("eventChannel", "string", None, "Canal do membro: ChangeEvents (padrão) ou um canal customizado (__chn).", "S"),
 P("filterExpression", "string", "56.0", "Expressão (subconjunto de SOQL) que filtra os eventos do fluxo."),
 P("selectedEntity", "string", None, "Nome do evento de alteração da entidade (ex.: AccountChangeEvent).", "S"), FN()], curinga=True,
 alertas=["createMetadata() e deleteMetadata() não são suportados; exclua via destructiveChanges.xml.", "Exige a permissão Customize Application."])
MT("PlatformEventSubscriberConfig", "Configura como um trigger Apex assina um evento de plataforma.",
   "Ajustar o tamanho do lote, o usuário de execução e o paralelismo do trigger que consome eventos.", "51.0", [
 P("batchSize", "int", None, "Máximo de mensagens por execução do trigger (1 a 2.000); a página desaconselha 1.", default=("valor", "2000", None)),
 P("isProtected", "boolean", None, "Se o componente fica protegido contra referência por componentes da org assinante."),
 P("masterLabel", "string", None, "Rótulo do componente.", "S"),
 P("numPartitions", "int", "62.0", "Quantas assinaturas paralelas internas são criadas para o trigger (1 a 10).", default=("valor", "1", None)),
 P("partitionKey", "string", "62.0", "Campo do evento cujo hash decide a partição: EventUuid ou um campo obrigatório Evento__e.Campo__c.", default=("valor", "EventUuid", None)),
 P("platformEventConsumer", "string", None, "Trigger Apex de evento de plataforma ao qual a configuração se aplica.", "S"),
 P("user", "string", None, "Usuário com que o trigger executa (afeta dono dos registros, logs e e-mail).", default=("valor", "Automated Process", "Quando não informado, executa como a entidade Automated Process.")), FN()],
 curinga=True, alertas=["A pasta é PlatformEventSubscriberConfigs, com inicial maiúscula (página e registro do Salesforce CLI concordam)."])
PROV = [("AgentActionOutputs", "uso interno"), ("AgentToAgent", "desde 66.0"), ("Anypoint", "desde 63.0"), ("AnypointPublic", "uso interno"), ("ApexRest", "desde 63.0"),
        ("AuraEnabled", "desde 65.0"), ("CodeExtension", "uso interno"), ("Commerce", "desde 67.0"), ("ContextDef", "desde 66.0"), ("Custom", None),
        ("CustomExternalConnector", "desde 66.0"), ("DocumentProcessing", "uso interno"), ("ExternalConnector", None), ("Heroku", None), ("MuleSoft", None),
        ("NamedQuery", "desde 64.0"), ("SchemaInferred", "desde 57.0"), ("Standard", None)]
MT("ExternalServiceRegistration", "Registra a especificação (OpenAPI) de uma API externa para usá-la como ações em Flow e Apex.",
   "Chamar APIs externas sem escrever código de integração: as operações viram ações invocáveis.", "39.0", [
 P("catalogedApiVersion", "string", "65.0", "Versão de uma API importada no API Catalog."),
 P("description", "string", None, "Descrição do serviço."), P("label", "string", None, "Nome do serviço no assistente de External Services.", "S"),
 P("namedCredential", "string", None, "Named credential usada pelo serviço."),
 P("namedCredentialReference", "reference", "57.0", "Id da named credential; quando preenchido, prevalece sobre namedCredential."),
 P("operations", "ExternalServiceOperation[]", None, "Operações do serviço.", estrutura="ExternalServiceOperation"),
 P("registrationProvider", "string", None, "Referência ao provedor (nome do conector, Id do HerokuAppLink ou vazio)."),
 P("registrationProviderAsset", "string", "66.0", "Ativo ligado ao registro (named query ou classe Apex)."),
 P("registrationProviderType", "string", None, "Origem da especificação registrada.", vals=PROV),
 P("schema", "string", None, "Conteúdo OpenAPI 2.0.x ou 3.0.x, em JSON ou YAML."),
 P("schemaAbsoluteUrl", "string", None, "URL absoluta do esquema, quando escolhida essa opção."),
 P("schemaType", "string", None, "Formato do esquema; inferido do conteúdo se omitido.", vals=V("OpenAPI")),
 P("schemaUploadFileExtension", "string", None, "Extensão do arquivo enviado."), P("schemaUploadFileName", "string", None, "Nome do arquivo enviado, sem extensão."),
 P("schemaUrl", "string", None, "Caminho do esquema relativo ao endpoint da named credential (começa com /)."),
 P("serviceBinding", "string", "53.0", "Mapeia tipos de mídia não suportados para suportados."),
 P("serviceName", "string", "63.0", "Nome do serviço do API Catalog ao qual o registro pertencia; removido.", ate="64.0", nota_versao="Disponível de 63.0 a 64.0; removido na 65.0."),
 P("status", "string", None, "Se o registro está pronto para uso.", "S", vals=[("complete", "pronto"), ("incomplete", "não concluído")]),
 P("systemVersion", "int", "55.0", "Versão interna do External Services usada no registro (1 a 9); somente leitura e sem atualização no lugar.",
   notas=["A página descreve o que muda em cada versão de 1 a 9 (9 é a atual)."]), FN()], curinga=True)
MT("ExternalDataSource", "Define a conexão com uma fonte de dados externa usada pelos objetos externos (Salesforce Connect).",
   "Exibir e, se permitido, editar dados de outro sistema como objetos da org, sem copiá-los.", "28.0", [
 P("authProvider", "string", None, "Auth provider que faz a autenticação."),
 P("certificate", "string", None, "Certificado para SSL de duas vias e assinatura."),
 P("customConfiguration", "string", None, "JSON com configurações específicas do tipo de adaptador.", notas=["Os conjuntos de parâmetros por adaptador (cross-org, OData, Apex) estão descritos na página, fora das tabelas; não foram extraídos."]),
 P("customHttpHeaders", "CustomHttpHeaders[]", "43.0", "Cabeçalhos HTTP customizados para OData 2.0 ou 4.0.", estrutura="CustomHttpHeaders"),
 P("endpoint", "string", None, "Endereço do sistema externo, ou callout:<NamedCredential> com caminho e query opcionais."),
 P("externalDataSrcDescriptors", "ExternalDataSrcDescriptors[]", "55.0", "Descritores de esquema dos adaptadores DynamoDB e Athena.", estrutura="ExternalDataSrcDescriptors"),
 P("isWritable", "boolean", "35.0", "Permite criar, alterar e excluir registros dos objetos externos; o padrão é somente leitura.", default=("valor", "false", "Somente leitura por padrão; no adaptador cross-org, desde 39.0.")),
 P("label", "string", None, "Nome exibido."), P("namedCredential", "string", None, "Named credential para fontes DynamoDB ou Athena."),
 P("oauthRefreshToken", "string", None, "Token de renovação."), P("oauthScope", "string", None, "Escopo solicitado."), P("oauthToken", "string", None, "Token de acesso."),
 P("password", "string", None, "Senha de acesso ao sistema externo."),
 P("principalType", "string", None, "Uma credencial para todos ou uma por usuário.", vals=V("Anonymous", "NamedCustomPrincipal", "NamedUser", "PerUser")),
 P("protocol", "string", None, "Protocolo de autenticação.", vals=V("NoAuthentication", "Oauth", "Password")),
 P("repository", "string", None, "Só SharePoint Online: define tabelas e campos quando não há metadados."),
 P("type", "string", None, "Tipo de adaptador ou fonte de dados.", "S",
   vals=V("AmazonAthena", "AmazonDynamoDB", "OData", "OData4", "SfdcOrg"), completa="nao",
   contexto="A página lista muitos outros valores (Files Connect, Digital Lending, busca federada, Revenue Cloud, Manufacturing Cloud, Id de classe Apex), vários reservados; não extraídos."),
 P("username", "string", None, "Usuário de acesso ao sistema externo."), P("version", "string", None, "Reservado para uso futuro.", **INT), FN()], curinga=True)
MT("AuthProvider", "Configura um provedor de autenticação externo (OpenID Connect, Google, Microsoft, Salesforce etc.).",
   "Permitir login único na org com contas de terceiros e obter tokens para integrações (usado por credenciais externas).", "27.0", [
 P("appleTeam", "string", "48.0", "Id de time Apple (10 caracteres).", "C:obrigatório para o tipo Apple"),
 P("authorizeUrl", "string", "29.0", "Endpoint de autorização OAuth; vazio para provedores gerenciados pela Salesforce (33.0+).", "C:obrigatório para OpenID Connect"),
 P("consumerKey", "string", None, "Chave do app no provedor; vazia para provedores gerenciados pela Salesforce."),
 P("consumerSecret", "string", None, "Segredo do app: não pode ser alterado depois de definido, deve ir criptografado na criação e é exportado como marcador."),
 P("controlPlane", "string", "57.0", "Onde fica o control plane do MuleSoft.", "C:obrigatório para o tipo MuleSoft", vals=V("None", "US", "EU")),
 P("customMetadataTypeRecord", "string", "36.0", "Nome de API do provedor customizado.", "C:obrigatório para plug-in customizado"),
 P("defaultScopes", "string", "29.0", "Escopos enviados quando o fluxo não especifica nenhum."),
 P("ecKey", "string", "48.0", "Chave privada gerada pela Apple.", "C:obrigatório para o tipo Apple"),
 P("errorUrl", "string", None, "URL customizada para exibir erros."),
 P("executionUser", "string", "27.0", "Usuário (com Manage Users) no contexto do qual o handler de registro executa.", "C:obrigatório quando há handler de registro"),
 P("flow", "string", "64.0", "Flow de registro de usuário (Identity User Registration) usado como handler."),
 P("flowDefaultAccount", "string", "64.0", "Conta padrão de novos usuários externos.", "C:obrigatório no registro por flow, se não definido no próprio flow"),
 P("flowDefaultProfile", "string", "64.0", "Perfil padrão de novos usuários.", "C:obrigatório no registro por flow, se não definido no próprio flow"),
 P("friendlyName", "string", None, "Nome exibido do provedor.", "S"),
 P("iconUrl", "string", "32.0", "Ícone do botão na página de login."),
 P("idTokenIssuer", "string", "30.0", "Emissor do token (URI https) usado para validar o id_token."),
 P("includeOrgIdInIdentifier", "boolean", "32.0", "Guarda também o Id da org de origem para distinguir usuários iguais; não pode ser desligado depois; só provedores Salesforce."),
 P("isPkceEnabled", "boolean", "59.0", "Liga o PKCE do OAuth (tipos Custom, Facebook, Google, Microsoft, OpenIdConnect, Salesforce)."),
 P("linkKickoffUrl", "string", "43.0", "URL para ligar um usuário existente a uma conta de terceiro (somente leitura)."),
 P("logoutUrl", "string", "33.0", "Destino depois do logout de SSO."),
 P("oauthKickoffUrl", "string", "43.0", "URL para obter tokens OAuth (somente leitura)."),
 P("paramForwardAllowlist", "AuthProvParamFwdAllowlist[]", "62.0", "Parâmetros de URL permitidos no repasse à URL de autorização.", estrutura="AuthProvParamFwdAllowlist"),
 P("plugin", "string", "36.0", "Classe Apex que estende Auth.AuthProviderPluginClass."),
 P("portal", "string", None, "Obsoleto: só portais existentes são suportados."),
 P("providerType", "string", None, "Tipo de provedor externo.", "S",
   vals=[("Apple", None), ("Bitbucket", "desde 61.0"), ("Custom", "desde 36.0"), ("Facebook", None), ("GitHub", "desde 35.0"), ("Google", None), ("Janrain", None),
         ("LinkedIn", "desde 32.0"), ("Microsoft", "desde 55.0"), ("MicrosoftACS", "desde 31.0"), ("MuleSoft", "desde 57.0"), ("OpenIdConnect", "desde 29.0"),
         ("Salesforce", None), ("Slack", "desde 54.0"), ("Twitter", "desde 32.0")]),
 P("registrationHandler", "string", None, "Classe Apex que implementa Auth.RegistrationHandler (alternativa ao flow)."),
 P("requireMfa", "boolean", None, "Exige MFA no SSO conforme o status de MFA de cada usuário."),
 P("sendAccessTokenInHeader", "boolean", "30.0", "Envia o token ao userInfoUrl no cabeçalho, não na query string."),
 P("sendClientCredentialsInHeader", "boolean", "30.0", "Envia as credenciais do cliente como Basic auth ao tokenUrl.", "C:obrigatório para OpenID Connect"),
 P("sendSecretInApis", "boolean", "47.0", "Se o segredo criptografado aparece nas respostas de API.", default=DT),
 P("ssoKickoffUrl", "string", "43.0", "URL de SSO na org com credenciais de terceiro (somente leitura)."),
 P("tokenUrl", "string", "29.0", "Endpoint de token OAuth; vazio para provedores gerenciados pela Salesforce."),
 P("userInfoUrl", "string", "29.0", "Endpoint de informações do usuário (OpenID Connect)."), FN()], curinga=True,
 divergencias=["A seção Usage da página (src:mdapi-authprovider) grafa tokenURL; a tabela grafa tokenUrl."],
 alertas=["consumerSecret é exportado como marcador: um retrieve não traz o segredo real."])
M.emit_structs()

# referência por nome: registrada na propriedade (alvos) e no relacionamento
import glob
REFS = {("metadata-types", "ExternalServiceRegistration", "namedCredential"): "mdt:NamedCredential",
        ("metadata-types", "ExternalDataSource", "namedCredential"): "mdt:NamedCredential",
        ("metadata-types", "ExternalDataSource", "authProvider"): "mdt:AuthProvider",
        ("metadata-types", "PlatformEventChannelMember", "eventChannel"): "mdt:PlatformEventChannel",
        ("estruturas", "NamedCredentialParameter", "externalCredential"): "mdt:ExternalCredential",
        ("estruturas", "ExternalCredentialParameter", "authProvider"): "mdt:AuthProvider"}
for (pasta, arq, prop), alvo in REFS.items():
    d = ld(f"{pasta}/{arq}.json")
    for p in d["propriedades"]:
        if p["nome"] == prop:
            p["referencia"] = {"alvos": [alvo], "nota": "Referência pelo nome do componente no XML."}
    sv(f"{pasta}/{arq}.json", d)

# ================================================================ relacionamentos (referência por nome entre componentes de metadata)
def rel(rid, o, campo, d, expl, s):
    sv(f"relacionamentos/{rid}.json", {"id": "rel:" + rid, "tipo": "referencia_campo", "origem": {"entidade": o, "campo": campo}, "destino": {"entidade": d},
       "explicacao": expl, "estado": "verificado", "evidencias": [ev(s)]})
NOME = " A referência é pelo nome do componente, no XML (não é um lookup entre registros)."
rel("ncparam-externalcredential", "mdx:NamedCredentialParameter", "externalCredential", "mdt:ExternalCredential",
    "Um parâmetro do tipo Authentication aponta a credencial externa que autentica a named credential." + NOME, "src:mdapi-namedcredential")
rel("ecparam-authprovider", "mdx:ExternalCredentialParameter", "authProvider", "mdt:AuthProvider",
    "Um parâmetro da credencial externa pode apontar o auth provider que conduz o login." + NOME, "src:mdapi-externalcredential")
rel("externalservice-namedcredential", "mdt:ExternalServiceRegistration", "namedCredential", "mdt:NamedCredential",
    "O serviço externo usa uma named credential para o endereço e a autenticação." + NOME, "src:mdapi-externalserviceregistration")
rel("externaldatasource-namedcredential", "mdt:ExternalDataSource", "namedCredential", "mdt:NamedCredential",
    "Fontes DynamoDB e Athena usam uma named credential." + NOME, "src:mdapi-externaldatasource")
rel("externaldatasource-authprovider", "mdt:ExternalDataSource", "authProvider", "mdt:AuthProvider",
    "A fonte de dados externa pode autenticar por um auth provider." + NOME, "src:mdapi-externaldatasource")
rel("pecmember-channel", "mdt:PlatformEventChannelMember", "eventChannel", "mdt:PlatformEventChannel",
    "O membro pertence a um canal: ChangeEvents (padrão) ou um canal customizado definido por PlatformEventChannel." + NOME, "src:mdapi-platformeventchannelmember")

# ================================================================ funcionalidades
INTc, ACS, ASY = "integracao-apis-e-eventos", "acesso-identidade-e-seguranca", "execucao-assincrona-lotes-e-agendamento"
NAO_INV_OBJ = {"tipo": "objeto_api", "estado": "desconhecido", "motivo": "Objetos API do tema não investigados no lote 5a; a lista vazia não comprova inexistência."}
def F(fid, nome, tec, aliases, oq, fin, ex, principal, secundarias, mdts, srcs, alertas=None, limit=None, recs=None):
    cp, sp = principal
    f = {"id": "func:" + fid, "nome": nome, "nome_tecnico": tec, "aliases": aliases,
         "termos_busca": sorted(set([nome.lower(), tec.lower()] + [a.lower() for a in aliases])),
         "o_que_e": oq, "finalidade": fin, "exemplo": ex,
         "classificacao_principal": {"classificacao": "cls:" + cp, "subclassificacao": "sub:" + sp},
         "classificacoes_secundarias": [{"classificacao": "cls:" + c, "subclassificacao": "sub:" + s, "motivo": m} for c, s, m in secundarias],
         "representacoes": {"metadata_types": [{"ref": "mdt:" + r, "papel": p} for r, p in mdts], "objetos_api": [], "ausencias": [NAO_INV_OBJ]},
         "setup": SETUP_NV, "recomendacoes": recs or [], "alertas": alertas or [], "limitacoes": limit or [], "estado": "verificado",
         "evidencias": [ev(s) for s in srcs]}
    sv(f"funcionalidades/{fid}.json", f)
    for s in [sp] + [x[1] for x in secundarias]:
        d = ld(f"subclassificacoes/{s}.json"); d["funcionalidades"] = sorted(set(d["funcionalidades"]) | {"func:" + fid}); sv(f"subclassificacoes/{s}.json", d)
    return f

F("named-credentials", "Named credentials e credenciais externas", "Named Credentials", ["named credential", "external credential", "credencial nomeada", "callout:"],
  "Guardam o endereço de um sistema externo e a forma de se autenticar nele, fora do código.",
  "Fazer chamadas seguras a sistemas externos sem espalhar URLs e segredos pelo Apex ou pelo Flow.",
  "Um Flow chama 'callout:ERP/pedidos'; a named credential ERP guarda a URL, e a credencial externa associada guarda o OAuth.",
  (INTc, "credenciais"), [(ACS, "credenciais-certificados-e-protecao-de-dados", "Guardam segredos de autenticação usados em integrações.")],
  [("NamedCredential", "Endpoint e parâmetros da chamada."), ("ExternalCredential", "Protocolo de autenticação e principals.")],
  ["src:mdapi-namedcredential", "src:mdapi-externalcredential"],
  alertas=["Desde a 56.0, a autenticação mora na credencial externa; named credentials do tipo Legacy ainda usam os campos antigos."],
  limit=["Objetos API e permissões de acesso aos principals não investigados nesta sessão."])
F("remote-site-settings", "Sites remotos", "Remote Site Settings", ["remote site", "site remoto", "callout allowlist"],
  "Lista de endereços externos que o código da org pode chamar.", "Liberar callouts para endereços que não usam named credential.",
  "Uma classe Apex chama https://api.exemplo.com; sem o registro do site remoto, a chamada é bloqueada.",
  (INTc, "chamadas-externas-e-endpoints"), [], [("RemoteSiteSetting", "Registro do site remoto.")], ["src:mdapi-remotesitesetting"],
  recs=[{"texto": "Prefira named credentials para callouts novos.", "natureza": "preferencia_projeto"}])
F("csp-trusted-sites", "Sites confiáveis (CSP)", "CSP Trusted Sites", ["csp", "content security policy", "trusted url", "site confiável"],
  "Lista de domínios externos dos quais as páginas da org podem carregar conteúdo (scripts, imagens, fontes, frames, mídia).",
  "Permitir que componentes Lightning, sites e Visualforce usem recursos de outros domínios sem violar a política de segurança.",
  "Um componente que exibe um mapa precisa carregar imagens de tiles.exemplo.com: o domínio entra como site confiável com img-src.",
  (INTc, "chamadas-externas-e-endpoints"), [], [("CspTrustedSite", "Registro do site confiável e das diretivas liberadas.")], ["src:mdapi-csptrustedsite"],
  limit=["Classificação didática: o tema também é de segurança da interface; as configurações de política de permissões ficam em SecuritySettings (não lido)."])
F("cors", "CORS: origens permitidas", "CORS Allowlist", ["cors", "cross-origin", "origem permitida", "allowlist"],
  "Lista de origens (domínios) cujo JavaScript, no navegador, pode chamar as APIs da org.",
  "Permitir que uma aplicação web externa consuma as APIs REST da org direto do navegador.",
  "Um portal em https://app.exemplo.com chama a API REST da org; a origem precisa estar na lista de CORS.",
  (INTc, "apis-de-dados-e-metadados"), [], [("CorsWhitelistOrigin", "Origem permitida.")], ["src:mdapi-corswhitelistorigin"],
  alertas=["CORS controla chamadas que chegam à org (vindas do navegador); não libera chamadas que saem da org (para isso: named credentials ou sites remotos)."])
F("platform-events", "Eventos de plataforma", "Platform Events", ["platform event", "evento de plataforma", "__e", "event bus", "canal de eventos"],
  "Mensagens publicadas num barramento de eventos, que sistemas e automações assinam para reagir.",
  "Desacoplar sistemas: quem publica não precisa saber quem consome.",
  "Um ERP publica PedidoFaturado__e; um trigger Apex assina o evento e atualiza a oportunidade.",
  (INTc, "eventos-e-mensageria"), [(ASY, "processamento-orientado-a-eventos", "Triggers Apex e flows reagem aos eventos publicados.")],
  [("PlatformEventChannel", "Canal customizado que agrupa eventos (channelType event)."), ("PlatformEventSubscriberConfig", "Configuração do trigger Apex assinante.")],
  ["src:mdapi-platformeventchannel", "src:mdapi-platformeventsubscriberconfig"],
  limit=["A definição do evento em si (objeto __e) não foi lida nesta sessão.", "Objetos API do tema não investigados."])
F("change-data-capture", "Captura de alterações de dados", "Change Data Capture", ["cdc", "change event", "evento de alteração", "ChangeEvents"],
  "Publica um evento a cada criação, alteração, exclusão ou restauração de registros dos objetos selecionados.",
  "Manter sistemas externos sincronizados quase em tempo real, sem consultas periódicas.",
  "AccountChangeEvent no canal ChangeEvents avisa um data warehouse a cada conta alterada.",
  (INTc, "eventos-e-mensageria"), [], [("PlatformEventChannelMember", "Seleciona a entidade (e filtros e campos extras) num canal."),
  ("PlatformEventChannel", "Canal customizado de captura de alterações (channelType data).")],
  ["src:mdapi-platformeventchannelmember", "src:mdapi-platformeventchannel"],
  alertas=["PlatformEventChannelMember não aceita createMetadata() nem deleteMetadata(); exclua via destructiveChanges.xml."])
F("external-services", "Serviços externos", "External Services", ["external service", "openapi", "api externa", "ação invocável"],
  "Importa a especificação OpenAPI de uma API externa e transforma suas operações em ações para Flow e Apex.",
  "Integrar sem código: o administrador usa as operações da API como ações num Flow.",
  "A especificação da API de frete é registrada; a operação calcularFrete vira uma ação usada num Screen Flow.",
  (INTc, "chamadas-externas-e-endpoints"), [], [("ExternalServiceRegistration", "Registro da especificação e das operações.")],
  ["src:mdapi-externalserviceregistration"],
  alertas=["systemVersion é somente leitura e não é atualizado no lugar: uma versão nova exige novo registro."])
F("external-objects", "Objetos externos (Salesforce Connect)", "External Objects", ["salesforce connect", "external data source", "odata", "objeto externo", "__x"],
  "Mostra dados de outro sistema como objetos da org, consultados sob demanda e sem cópia.",
  "Usar dados externos em listas, relacionamentos e relatórios sem replicá-los.",
  "Pedidos do ERP aparecem como objeto externo Pedido__x, lidos via OData no momento da consulta.",
  (INTc, "conectividade-e-virtualizacao-de-dados"), [], [("ExternalDataSource", "Conexão e autenticação da fonte de dados externa.")],
  ["src:mdapi-externaldatasource"],
  limit=["A definição do objeto externo (__x) não foi lida nesta sessão.", "Valores completos do campo type e parâmetros de customConfiguration não extraídos."])
F("auth-providers", "Provedores de autenticação", "Auth Providers", ["auth provider", "provedor de autenticação", "login social", "openid connect", "sso"],
  "Configura um provedor externo (OpenID Connect, Google, Microsoft, Salesforce etc.) para login único e para obter tokens.",
  "Deixar usuários entrarem com contas de terceiros e permitir que integrações obtenham tokens OAuth.",
  "Usuários de um portal entram com a conta Microsoft; uma credencial externa usa o mesmo provedor para chamar uma API.",
  (INTc, "autenticacao-de-integracoes"), [(ACS, "autenticacao-sso-e-mfa", "Também serve para login único de usuários na org.")],
  [("AuthProvider", "Configuração do provedor.")], ["src:mdapi-authprovider"],
  alertas=["O segredo do app (consumerSecret) não vem no retrieve: é exportado como marcador."])

# ================================================================ nuvem Platform/Core: classificação de integração
core = ld("nuvens/platform-core.json")
FS = {"credenciais": ["func:named-credentials"], "chamadas-externas-e-endpoints": ["func:csp-trusted-sites", "func:external-services", "func:remote-site-settings"],
      "apis-de-dados-e-metadados": ["func:cors"], "eventos-e-mensageria": ["func:change-data-capture", "func:platform-events"],
      "conectividade-e-virtualizacao-de-dados": ["func:external-objects"], "autenticacao-de-integracoes": ["func:auth-providers"]}
core["classificacoes_aplicaveis"] = [c for c in core["classificacoes_aplicaveis"] if c["classificacao"] != "cls:" + INTc] + [
    {"classificacao": "cls:" + INTc, "subclassificacoes": [{"subclassificacao": "sub:" + s, "funcionalidades": sorted(f)} for s, f in sorted(FS.items())]}]
sv("nuvens/platform-core.json", core)
print("ok lote 5a")
