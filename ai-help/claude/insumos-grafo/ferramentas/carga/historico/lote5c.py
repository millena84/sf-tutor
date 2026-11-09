# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5c (issue #24): certificados, SAML, provedor de identidade de autenticação externa, conexões de rede, serviços registrados (Commerce), Event Relay, assinaturas gerenciadas.
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

reg = json.load(open(BASE + "fontes/registro.json"))
B = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
CHK = {"estado": "verificado", "nota": f"Conteúdo lido em {DATA} e conferido quanto ao assunto (não apenas HTTP 200)."}
NOMES = ["Certificate", "SamlSsoConfig", "ExternalAuthIdentityProvider", "OutboundNetworkConnection", "RegisteredExternalService",
         "EventRelayConfig", "ManagedEventSubscription", "PlatformEventSettings"]
novas = [{"id": f"src:mdapi-{n.lower()}", "titulo": f"{n} (Metadata API)", "url": B + f"meta_{n.lower()}.htm", "tipo": "oficial_documentacao", "versao": "68.0",
          "data_verificacao": DATA, "metodo": "extracao_documental_assistida", "pertinencia": f"Arquivo, versão e propriedades do tipo {n}.",
          "extracao": "fontes/extracoes/mdapi-lote5c.txt", "checagem_online": CHK} for n in NOMES]
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

_orig = M.arquivos
def _arquivos(nome, parent=None):
    if nome == "PlatformEventSettings":
        s = "src:mdapi-platformeventsettings"
        return {"source_format": af("verificado", {"pasta": "settings/", "arquivo": "PlatformEvent.settings-meta.xml"},
                    "Pasta e sufixo do tipo genérico Settings no registro do Salesforce CLI; o nome-base do arquivo vem da página do tipo.",
                    [ev("src:sdr-registry", "types.settings"), ev(s)]),
                "metadata_api_format": af("verificado", {"pasta": "settings/", "arquivo": "PlatformEvent.settings"},
                    "Um único arquivo; no package.xml, o tipo é Settings e o membro é PlatformEvent.", [ev(s)])}
    return _orig(nome, parent)
M.arquivos = _arquivos

def P(n, t, ver=None, d=None, req="N", **kw): return (n, t, req, ver, d, kw)
DF = ("valor", "false", None)
DT = ("valor", "true", None)
FN = lambda: M.FULLNAME_HERDADO(None)
INT = {"notas": ["Reservado para uso interno da Salesforce (página oficial)."]}
def V(*vals): return [(v, None) for v in vals]
SETUP_NV = af("desconhecido", None, "Caminho no Setup não verificado nesta sessão.")

# ================================================================ estruturas
S = "src:mdapi-externalauthidentityprovider"
M.struct("ExternalAuthIdentityProviderParameter", S, ["mdt:ExternalAuthIdentityProvider"], [
 P("description", "string", None, "Descrição do parâmetro."), P("parameterName", "string", None, "Nome do parâmetro.", "S"),
 P("parameterType", "string", None, "Como o parâmetro se comporta (URLs do provedor, parâmetros e cabeçalhos das requisições de token e refresh etc.).", "S",
   vals=V("AuthorizeRequestQueryParameter", "AuthorizeUrl", "ClientAuthentication", "CreatedByNamespace", "IdentityProviderOptions", "ManagedByComponent",
          "ManagedByFeature", "RefreshRequestBodyParameter", "RefreshRequestHttpHeader", "RefreshRequestQueryParameter", "StandardExternalIdentityProvider",
          "TokenRequestBodyParameter", "TokenRequestHttpHeader", "TokenRequestQueryParameter", "TokenUrl", "UserInfoUrl")),
 P("parameterValue", "string", None, "Valor literal, quando o tipo é literal."), P("sequenceNumber", "int", None, "Ordem de aplicação; número menor tem prioridade.")],
 "Parâmetro de um provedor de identidade de autenticação externa.")
S = "src:mdapi-outboundnetworkconnection"
M.struct("OutboundNetworkConnProperty", S, ["mdt:OutboundNetworkConnection"], [
 P("propertyName", "string", None, "Qual configuração o par representa.", "S", vals=[("AwsVpcEndpointId", None), ("AwsVpcEndpointServiceName", None), ("Region", None)], completa="nao",
   contexto="A página também lista valores DataCloudPrivateNetwork*, reservados para uso interno."),
 P("propertyValue", "string", None, "Valor da configuração, por exemplo o código da região.", "S")], "Par nome-valor de configuração da conexão.")

# ================================================================ metadata types
def MT(nome, o, f, desde, rows, **kw):
    return M.mdt(nome, f"src:mdapi-{nome.lower()}", o, f, desde, rows, setup=SETUP_NV, **kw)

MT("Certificate", "Certificado (e chave) guardado na org, autoassinado ou assinado por uma autoridade certificadora.",
   "Assinar requisições, autenticar com SSL de duas vias e assinar asserções SAML ou tokens.", "36.0", [
 P("caSigned", "boolean", None, "Se o certificado foi assinado por uma autoridade certificadora.", "S"),
 P("encryptedWithPlatformEncryption", "boolean", None, "Se o certificado é protegido pela Platform Encryption."),
 P("expirationDate", "dateTime", None, "Quando o certificado deixa de valer; nos assinados por AC, passa a ser a validade do certificado enviado.",
   default=("valor", "1 ano (2048 bits) ou 2 anos (4096 bits) após a criação", "Para certificados autoassinados.")),
 P("keySize", "int", None, "Tamanho da chave (2048 é mais rápida; 4096, mais forte); também define a validade.", vals=V("2048", "4096"), default=("valor", "2048", "Quando omitido na criação.")),
 P("masterLabel", "string", None, "Nome exibido na interface (até 64 caracteres).", "S"),
 P("privateKeyExportable", "boolean", None, "Se a chave privada pode ser exportada.", default=("valor", "true", "Quando omitido na criação.")),
 ("content", "base64Binary", "?", None, "Conteúdo do certificado; herdado de MetadataWithContent (a página não o descreve).", {"herdada": "MetadataWithContent"}),
 FN()], estende="MetadataWithContent", curinga=True)
MT("SamlSsoConfig", "Configuração de login único (SSO) por SAML com um provedor de identidade externo.",
   "Permitir que usuários entrem na org com a identidade corporativa, com provisionamento just-in-time opcional.", "28.0", [
 P("attributeNameIdFormat", "string", None, "Formato do NameID quando a identidade vem de um atributo (só SAML 2.0).", vals=V("unspecified", "emailAddress", "persistent")),
 P("attributeName", "string", None, "Nome do atributo informado pelo provedor de identidade."),
 P("decryptionCertificate", "string", "30.0", "Certificado que decifra as asserções recebidas."),
 P("errorUrl", "string", None, "Página exibida depois de um erro de login (pública; absoluta ou relativa)."),
 P("executionUserId", "string", None, "Usuário que executa o handler Apex (precisa de Manage Users).", "C:obrigatório quando há handler JIT"),
 P("identityLocation", "string", None, "Onde a identidade do usuário aparece na asserção.", vals=V("SubjectNameId", "Attribute")),
 P("identityMapping", "string", None, "Identificador do usuário no provisionamento JIT.", vals=V("Username", "FederationId", "UserId")),
 P("issuer", "string", None, "Identificação do provedor de identidade."),
 P("loginUrl", "string", None, "Só SAML 2.0: para onde a Salesforce envia o pedido SAML que inicia o login."),
 P("logoutUrl", "string", None, "Só SAML 2.0: destino depois do logout.", default=("valor", "https://salesforce.com", None)),
 P("name", "string", None, "Nome único de API (começa com letra; letras, números e sublinhado; sem sublinhado final ou duplo)."),
 P("oauthTokenEndpoint", "string", None, "Só SAML 2.0: URL ACS do fluxo de asserção SAML do OAuth."),
 P("redirectBinding", "boolean", None, "Binding HTTP que o provedor espera (a descrição cita HTTP POST e HTTP Redirect)."),
 P("requestSignatureMethod", "string", None, "Algoritmo de assinatura das requisições SAML.", vals=V("RSA-SHA1", "RSA-SHA256")),
 P("requestSigningCertId", "string", None, "Id (18 caracteres) do certificado que assina as requisições ao provedor."),
 P("salesforceLoginUrl", "string", None, "URL de login do fluxo de SSO; com criptografia, inclui o parâmetro sc com o Id da configuração (desde 47.0)."),
 P("samlEntityId", "string", None, "Emissor nas requisições da Salesforce e público esperado nas respostas; a página recomenda a URL de login do My Domain."),
 P("samlJitHandlerId", "string", None, "Classe Apex que implementa Auth.SamlJitHandler."),
 P("samlVersion", "string", None, "Versão do SAML.", vals=V("SAML1_1", "SAML2_0")),
 P("singleLogoutBinding", "string", None, "Como vai a mensagem de logout único: na query string ou no corpo do POST.", vals=V("RedirectBinding", "PostBinding")),
 P("singleLogoutUrl", "string", None, "Endpoint que recebe pedidos ou respostas de logout."),
 P("useConfigRequestMethod", "boolean", None, "Usa o método de assinatura configurado no logout único (senão, RSA-SHA1).", default=DF),
 P("useSameDigestAlgoForSigning", "boolean", "55.0", "O algoritmo de digest acompanha o de assinatura (senão, SHA-1); editável só em configurações antigas.",
   default=("valor", "true", "Em configurações criadas depois do Spring '22.")),
 P("userProvisioning", "boolean", None, "Cria usuários no primeiro login (JIT); exige mapeamento por Federation ID."),
 P("validationCert", "string", None, "Certificado do provedor usado para validar as requisições."), FN()], curinga=True,
 divergencias=["redirectBinding está tipado como boolean na tabela (src:mdapi-samlssoconfig), mas a descrição cita dois bindings nomeados."])
MT("ExternalAuthIdentityProvider", "Define um provedor de identidade de autenticação externa: o fluxo e os endpoints OAuth para obter tokens de APIs protegidas.",
   "Configurar a obtenção de tokens usada por credenciais externas; a página de ExternalCredential o recomenda no lugar do auth provider.", "62.0", [
 P("authenticationFlow", "string", None, "Fluxo usado para obter tokens.", "S", vals=V("AuthorizationCode", "ClientCredentials", "SalesforceDefined")),
 P("authenticationProtocol", "string", None, "Protocolo de acesso ao sistema externo.", "S", vals=V("OAuth", "SalesforceDefined")),
 P("description", "string", None, "Descrição."),
 P("externalAuthIdentityProviderParameters", "ExternalAuthIdentityProviderParameter[]", None, "Parâmetros que completam a configuração.", estrutura="ExternalAuthIdentityProviderParameter"),
 P("label", "string", None, "Nome do provedor.", "S"), FN()], curinga=True,
 alertas=["Exige a permissão Customize Application ou Manage Named Credentials."],
 divergencias=["A tabela (src:mdapi-externalauthidentityprovider) usa externalAuthIdentityProviderParameters; o exemplo XML usa o singular."])
MT("OutboundNetworkConnection", "Define uma conexão de rede privada de saída (AWS PrivateLink) usada por callouts.",
   "Fazer chamadas a serviços na AWS sem passar pela internet pública.", "49.0", [
 P("connectionType", "string", None, "Provedor da conexão.", "S", vals=[("AwsPrivateLink", None), ("DataCloudPrivateConnection", "uso interno")]),
 P("description", "string", None, "Descrição (até 255 caracteres)."), P("isActive", "boolean", None, "Se a conexão está ligada.", "S"),
 P("label", "string", None, "Nome exibido.", "S"),
 P("outboundNetworkConnProperties", "OutboundNetworkConnProperty[]", None, "Configurações da conexão em pares nome-valor.", estrutura="OutboundNetworkConnProperty"),
 P("status", "string", None, "Estado atual; muda sozinho depois das ações Provision, Sync ou Teardown.", "S",
   vals=V("Unprovisioned", "Allocation", "PendingAcceptance", "PendingActivation", "RejectedRemotely", "DeletedRemotely", "TeardownInProgress", "Ready"),
   default=("valor", "Unprovisioned", "Estado inicial.")), FN()], curinga=True)
EXT = ["Commerce_Domain_BuyerGroup_EvaluationService", "Commerce_Domain_Cart_Calculate", "Commerce_Domain_Checkout_CreateOrder", "Commerce_Domain_Inventory_CartCalculator",
       "Commerce_Domain_Inventory_Service", "Commerce_Domain_OrderManagement_Product", "Commerce_Domain_Pricing_CartCalculator", "Commerce_Domain_Pricing_Service",
       "Commerce_Domain_Promotions_CartCalculator", "Commerce_Domain_Promotions_ShippingCalculator", "Commerce_Domain_Shipping_CartCalculator", "Commerce_Domain_Shipping_SplitShipment",
       "Commerce_Domain_Tax_CartCalculator", "Commerce_Domain_Tax_Service", "Commerce_Endpoint_Account_Address", "Commerce_Endpoint_Account_Addresses", "Commerce_Endpoint_Cart_Item",
       "Commerce_Endpoint_Cart_ItemCollection", "Commerce_Endpoint_Catalog_Product", "Commerce_Endpoint_Catalog_Products", "Commerce_Endpoint_Gift_Wraps",
       "Commerce_Endpoint_Search_ProductSearch", "Commerce_Endpoint_Search_Products", "Commerce_Endpoint_Search_ProductsByCategory"]
EXTV = {"Commerce_Domain_BuyerGroup_EvaluationService": "desde 65.0", "Commerce_Endpoint_Cart_Item": "desde 62.0", "Commerce_Endpoint_Cart_ItemCollection": "desde 62.0", "Commerce_Endpoint_Gift_Wraps": "desde 65.0"}
MT("RegisteredExternalService", "Registra uma classe Apex como provedor de um serviço do Commerce (preço, estoque, frete, impostos, promoções) ou de um ponto de extensão.",
   "Plugar integrações e extensões no carrinho e no checkout do B2B/D2C Commerce.", "49.0", [
 P("configUrl", "string", None, "Link para a configuração da integração."), P("description", "string", "59.0", "Descrição do provedor."),
 P("documentationUrl", "string", None, "Link para a documentação."),
 P("extensionPointName", "string", "55.0", "Ponto de extensão implementado.", "C:obrigatório quando externalServiceProviderType é Extension", vals=[(v, EXTV.get(v)) for v in EXT]),
 P("externalServiceProvider", "string", None, "Id da classe Apex provedora (implementa uma interface sfdc_checkout ou estende uma classe base de extensão).", "S"),
 P("externalServiceProviderType", "string", None, "Categoria do provedor.", "S",
   vals=[("Extension", "desde 55.0"), ("Inventory", None), ("Price", None), ("Promotions", "desde 53.0"), ("Shipment", None), ("Tax", None)]),
 P("iconUri", "string", "59.0", "Ícone do provedor."), P("isApplication", "boolean", "59.0", "Se o provedor vem de um pacote gerenciado.", default=DF),
 P("isProtected", "boolean", None, "Gerado automaticamente; sem efeito no comportamento.", default=DF), P("masterLabel", "string", None, "Rótulo.", "S"), FN()], curinga=True,
 alertas=["Exige licença B2B Commerce ou D2C Commerce."])
MT("EventRelayConfig", "Define um Event Relay: encaminha eventos de um canal da plataforma para o Amazon EventBridge.",
   "Levar eventos de plataforma e de alteração para a AWS sem código de integração.", "56.0", [
 P("destinationResourceName", "string", None, "Named credential (com prefixo callout:) que guarda a conta AWS de destino.", "S"),
 P("eventChannel", "string", None, "Nome completo do canal de eventos encaminhado.", "S"),
 P("label", "string", None, "Nome exibido (de preferência único e claro)."),
 P("relayOption", "string", None, "JSON que define de onde retomar depois de um erro: eventos novos (LATEST) ou guardados até três dias (EARLIEST).",
   default=("valor", "{\"ReplayRecovery\":\"LATEST\"}", None)),
 P("state", "string", None, "Estado de execução; na criação, só STOP é aceito.", vals=[("RUN", None), ("PAUSE", None), ("STOP", None), ("DELETE", "reservado")],
   default=("valor", "STOP", None)),
 P("usageType", "string", None, "Reservado para uso futuro.", **INT), FN()], curinga=True,
 alertas=["Depois de criado, só state e relayOption podem mudar; eventChannel e destinationResourceName não.", "Exige a permissão Customize Application."])
MT("ManagedEventSubscription", "Assinatura gerenciada de eventos (Pub/Sub API): a plataforma guarda a posição de leitura do assinante.",
   "Consumir eventos de plataforma ou de alteração sem perder a posição entre conexões.", "60.0", [
 P("defaultReplay", "string", None, "Onde começa na primeira assinatura ou sem posição gravada.", vals=V("LATEST", "EARLIEST"), default=("valor", "LATEST", None)),
 P("errorRecoveryReplay", "string", None, "Onde recomeça se a posição gravada for inválida (por exemplo, fora da retenção).", vals=V("LATEST", "EARLIEST"), default=("valor", "LATEST", None)),
 P("label", "string", None, "Rótulo."),
 P("state", "string", None, "Se a assinatura roda; STOP para a entrega e apaga a posição gravada.", vals=[("RUN", None), ("STOP", None), ("PAUSE", "uso interno")], default=("valor", "RUN", None)),
 P("topicName", "string", None, "Evento, evento de alteração ou canal consumido (/event/Evento__e, /data/ChangeEvents, /data/ObjetoChangeEvent, canais __chn)."),
 P("version", "string", None, "Uso interno.", **INT), FN()], curinga=True,
 divergencias=["O exemplo da página (src:mdapi-managedeventsubscription) usa o sufixo .managedSubscription, diferente do sufixo declarado (.managedEventSubscription)."])
MT("PlatformEventSettings", "Configurações da org para eventos de plataforma.", "Ligar métricas de uso detalhadas.", "58.0", [
 P("enableEnhancedUsageMetrics", "boolean", None, "Liga campos extras e segmentos de tempo menores nas consultas a PlatformEventUsageMetric.", default=DF)],
 curinga=False, alertas=["No package.xml, use o tipo Settings com o membro PlatformEvent."])
M.emit_structs()

# ================================================================ referências por nome
REFS = {("estruturas", "ExternalCredentialParameter", "externalAuthIdentityProvider"): "mdt:ExternalAuthIdentityProvider",
        ("estruturas", "NamedCredentialParameter", "outboundNetworkConnection"): "mdt:OutboundNetworkConnection",
        ("metadata-types", "EventRelayConfig", "destinationResourceName"): "mdt:NamedCredential",
        ("metadata-types", "EventRelayConfig", "eventChannel"): "mdt:PlatformEventChannel"}
for (pasta, arq, prop), alvo in REFS.items():
    d = ld(f"{pasta}/{arq}.json")
    for p in d["propriedades"]:
        if p["nome"] == prop:
            p["referencia"] = {"alvos": [alvo], "nota": "Referência pelo nome do componente no XML."}
    sv(f"{pasta}/{arq}.json", d)
NOME = " A referência é pelo nome do componente, no XML (não é um lookup entre registros)."
def rel(rid, o, campo, d, expl, s):
    sv(f"relacionamentos/{rid}.json", {"id": "rel:" + rid, "tipo": "referencia_campo", "origem": {"entidade": o, "campo": campo}, "destino": {"entidade": d},
       "explicacao": expl + NOME, "estado": "verificado", "evidencias": [ev(s)]})
rel("ecparam-extauthidp", "mdx:ExternalCredentialParameter", "externalAuthIdentityProvider", "mdt:ExternalAuthIdentityProvider",
    "A credencial externa pode usar um provedor de identidade de autenticação externa para obter tokens.", "src:mdapi-externalcredential")
rel("ncparam-outboundnetwork", "mdx:NamedCredentialParameter", "outboundNetworkConnection", "mdt:OutboundNetworkConnection",
    "Uma named credential do tipo PrivateEndpoint aponta a conexão de rede privada.", "src:mdapi-namedcredential")
rel("eventrelay-namedcredential", "mdt:EventRelayConfig", "destinationResourceName", "mdt:NamedCredential",
    "O relay usa uma named credential (prefixo callout:) com a conta AWS de destino.", "src:mdapi-eventrelayconfig")
rel("eventrelay-channel", "mdt:EventRelayConfig", "eventChannel", "mdt:PlatformEventChannel",
    "O relay encaminha os eventos de um canal (a página pede o nome completo do canal).", "src:mdapi-eventrelayconfig")

# ================================================================ funcionalidades
INTc, ACS = "integracao-apis-e-eventos", "acesso-identidade-e-seguranca"
NAO_INV_OBJ = {"tipo": "objeto_api", "estado": "desconhecido", "motivo": "Objetos API do tema não investigados no lote 5c; a lista vazia não comprova inexistência."}
def addsub(fid, subs):
    for s in subs:
        d = ld(f"subclassificacoes/{s}.json"); d["funcionalidades"] = sorted(set(d["funcionalidades"]) | {"func:" + fid}); sv(f"subclassificacoes/{s}.json", d)
def F(fid, nome, tec, aliases, oq, fin, ex, principal, secundarias, mdts, srcs, alertas=None, limit=None):
    cp, sp = principal
    f = {"id": "func:" + fid, "nome": nome, "nome_tecnico": tec, "aliases": aliases,
         "termos_busca": sorted(set([nome.lower(), tec.lower()] + [a.lower() for a in aliases])), "o_que_e": oq, "finalidade": fin, "exemplo": ex,
         "classificacao_principal": {"classificacao": "cls:" + cp, "subclassificacao": "sub:" + sp},
         "classificacoes_secundarias": [{"classificacao": "cls:" + c, "subclassificacao": "sub:" + s, "motivo": m} for c, s, m in secundarias],
         "representacoes": {"metadata_types": [{"ref": "mdt:" + r, "papel": p} for r, p in mdts], "objetos_api": [], "ausencias": [NAO_INV_OBJ]},
         "setup": SETUP_NV, "recomendacoes": [], "alertas": alertas or [], "limitacoes": limit or [], "estado": "verificado", "evidencias": [ev(s) for s in srcs]}
    sv(f"funcionalidades/{fid}.json", f); addsub(fid, [sp] + [x[1] for x in secundarias])
def upd(fid, mdts, srcs, alertas=()):
    f = ld(f"funcionalidades/{fid}.json"); r = f["representacoes"]["metadata_types"]
    have = {x["ref"] for x in r}
    r += [{"ref": "mdt:" + m, "papel": p} for m, p in mdts if "mdt:" + m not in have]
    f["evidencias"] += [ev(s) for s in srcs if not any(e["fonte"] == s for e in f["evidencias"])]
    f["alertas"] += [a for a in alertas if a not in f["alertas"]]
    sv(f"funcionalidades/{fid}.json", f)

F("certificados", "Certificados e chaves", "Certificate and Key Management", ["certificado", "certificate", "chave privada", "ssl", "mtls"],
  "Certificados e chaves guardados na org, autoassinados ou assinados por uma autoridade certificadora.",
  "Assinar e autenticar integrações e SSO sem expor chaves no código.",
  "Um certificado autoassinado de 4096 bits assina o JWT usado por uma credencial externa.",
  (ACS, "credenciais-certificados-e-protecao-de-dados"), [(INTc, "autenticacao-de-integracoes", "Usados para assinar requisições e autenticar integrações.")],
  [("Certificate", "Certificado e chave.")], ["src:mdapi-certificate"])
F("sso-saml", "Login único por SAML", "SAML Single Sign-On", ["saml", "sso", "single sign-on", "login único", "provedor de identidade", "jit"],
  "Configura a org para aceitar login de um provedor de identidade corporativo via SAML.",
  "Usuários entram com a conta da empresa; o provisionamento just-in-time cria usuários no primeiro acesso.",
  "Funcionários entram pelo provedor corporativo; a asserção traz o Federation ID e o usuário é criado no primeiro login.",
  (ACS, "autenticacao-sso-e-mfa"), [], [("SamlSsoConfig", "Configuração do SSO por SAML.")], ["src:mdapi-samlssoconfig"])
F("conexoes-de-rede-privadas", "Conexões de rede privadas de saída", "Outbound Network Connections",
  ["aws privatelink", "conexão privada", "outbound network connection"],
  "Conexão privada entre a org e a AWS, usada por named credentials do tipo PrivateEndpoint.",
  "Fazer callouts para serviços na AWS sem trafegar pela internet pública.",
  "A named credential do serviço de pedidos na AWS usa uma conexão PrivateLink já provisionada.",
  (INTc, "chamadas-externas-e-endpoints"), [], [("OutboundNetworkConnection", "Definição da conexão privada.")], ["src:mdapi-outboundnetworkconnection"],
  limit=["O nome comercial do recurso não foi verificado nas fontes deste lote; o rótulo em português é tradução didática do projeto."])
F("servicos-externos-registrados-commerce", "Serviços externos registrados (Commerce)", "Registered External Services",
  ["registered external service", "extensão commerce", "cálculo de frete", "cálculo de imposto", "checkout"],
  "Registra classes Apex como provedores de preço, estoque, frete, impostos, promoções ou pontos de extensão do Commerce.",
  "Integrar sistemas externos (ERP, cálculo de impostos, transportadoras) ao carrinho e ao checkout.",
  "Uma classe Apex consulta a transportadora e é registrada como provedor Shipment do checkout.",
  (INTc, "chamadas-externas-e-endpoints"), [], [("RegisteredExternalService", "Registro do provedor.")], ["src:mdapi-registeredexternalservice"],
  alertas=["Exige licença B2B Commerce ou D2C Commerce."], limit=["Nuvem de Commerce ainda não catalogada; a funcionalidade fica, por ora, na visão Platform/Core."])
F("event-relay", "Event Relay (Amazon EventBridge)", "Event Relay", ["event relay", "eventbridge", "aws", "encaminhar eventos"],
  "Encaminha eventos de um canal da plataforma para o Amazon EventBridge.",
  "Integrar com a AWS orientado a eventos, sem código.",
  "Eventos PedidoFaturado__e vão para o EventBridge, que aciona uma função na AWS.",
  (INTc, "eventos-e-mensageria"), [], [("EventRelayConfig", "Configuração do relay.")], ["src:mdapi-eventrelayconfig"],
  alertas=["Depois de criado, só o estado e a opção de retomada podem mudar."])
upd("named-credentials", [("ExternalAuthIdentityProvider", "Provedor de identidade de autenticação externa usado pela credencial externa.")],
    ["src:mdapi-externalauthidentityprovider"])
upd("platform-events", [("ManagedEventSubscription", "Assinatura gerenciada (Pub/Sub API)."), ("PlatformEventSettings", "Configurações da org (métricas de uso).")],
    ["src:mdapi-managedeventsubscription", "src:mdapi-platformeventsettings"])
upd("change-data-capture", [("ManagedEventSubscription", "Assinatura gerenciada de eventos de alteração (/data/...).")], ["src:mdapi-managedeventsubscription"])

core = ld("nuvens/platform-core.json")
ADD = {"sub:chamadas-externas-e-endpoints": {"func:conexoes-de-rede-privadas", "func:servicos-externos-registrados-commerce"},
       "sub:eventos-e-mensageria": {"func:event-relay"}}
for c in core["classificacoes_aplicaveis"]:
    if c["classificacao"] == "cls:" + INTc:
        for s in c["subclassificacoes"]:
            if s["subclassificacao"] in ADD: s["funcionalidades"] = sorted(set(s["funcionalidades"]) | ADD[s["subclassificacao"]])
acs = next((c for c in core["classificacoes_aplicaveis"] if c["classificacao"] == "cls:" + ACS), None)
for sub, fid in [("sub:credenciais-certificados-e-protecao-de-dados", "func:certificados"), ("sub:autenticacao-sso-e-mfa", "func:sso-saml")]:
    s = next((x for x in acs["subclassificacoes"] if x["subclassificacao"] == sub), None)
    if s: s["funcionalidades"] = sorted(set(s["funcionalidades"]) | {fid})
    else: acs["subclassificacoes"].append({"subclassificacao": sub, "funcionalidades": [fid]})
acs["subclassificacoes"].sort(key=lambda x: x["subclassificacao"])
sv("nuvens/platform-core.json", core)
print("ok lote 5c")
