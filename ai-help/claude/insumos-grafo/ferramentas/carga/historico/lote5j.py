# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5j (issue #24): objetos API de integração.
import json
from b1_base import ev, af
from b3_obj import field, expo, obj, cob, cnt, APEX_OK
BASE = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/"
CAT = BASE + "catalogo/"
DATA = "2026-11-09"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
A = "https://developer.salesforce.com/docs/atlas.en-us.264.0.object_reference.meta/object_reference/sforce_api_objects_"
CHK = {"estado": "verificado", "nota": f"Conteúdo lido em {DATA} e conferido quanto ao assunto (não apenas HTTP 200)."}
OBJS = ["NamedCredential", "ConnectedApplication", "AuthProvider", "OauthToken", "ExternalDataSource", "CspTrustedSite"]
reg = json.load(open(BASE + "fontes/registro.json")); ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [{"id": f"src:objref-{n.lower()}", "titulo": f"{n} (Object Reference)", "url": A + n.lower() + ".htm", "tipo": "oficial_documentacao", "versao": "68.0",
                   "data_verificacao": DATA, "metodo": "extracao_documental_assistida", "pertinencia": f"Chamadas, acesso e campos de {n}.",
                   "extracao": "fontes/extracoes/lote5j-objetos-integracao.txt", "checagem_online": CHK} for n in OBJS if f"src:objref-{n.lower()}" not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)
TOOL_D = lambda: expo("tooling", "desconhecido", nota="Exposição na Tooling API não verificada.")
LEG = ["Legado: obsoleto a partir da 56.0 (named credentials antigas)."]
INT = ["Uso interno da Salesforce, segundo a página."]
FALSE = ("valor", "false", None)

# ---------------- NamedCredential
S = "src:objref-namedcredential"; O = "obj:NamedCredential"
nc = [
 field(O, "AuthProviderId", "reference", "FGNS", "39.0", "Provedor de autenticação que cuida do login e da aprovação de acesso.", S, ref=["obj:AuthProvider"], rel="AuthProvider",
       notas=LEG + ["Visível só com Customize Application e Manage AuthProviders."]),
 field(O, "AuthTokenEndpointUrl", "textarea", "N", "46.0", "URL onde JWTs são trocados por tokens de acesso.", S, notas=LEG),
 field(O, "CalloutOptionsAllowMergeFieldsInBody", "boolean", "F", "35.0", "Em callouts Apex, permite campos de mesclagem no corpo da requisição.", S),
 field(O, "CalloutOptionsAllowMergeFieldsInHeader", "boolean", "F", "35.0", "Em callouts Apex, permite campos de mesclagem nos cabeçalhos.", S),
 field(O, "CalloutOptionsGenerateAuthorizationHeader", "boolean", "F", "35.0", "A Salesforce adiciona sozinha o cabeçalho de autorização padrão.", S),
 field(O, "DeveloperName", "string", "FGS", None, "Nome de API único na org.", S, notas=["Visível com View DeveloperName ou View Setup and Configuration."]),
 field(O, "Endpoint", "textarea", "N", None, "URL raiz do endpoint.", S, notas=LEG),
 field(O, "JwtAudience", "textarea", "N", "46.0", "Destinatários do JWT (string ou lista em JSON).", S, notas=LEG),
 field(O, "JwtFormulaSubject", "string", "FGNS", "46.0", "Fórmula que calcula o subject do JWT por usuário ('Per User Subject').", S, notas=LEG),
 field(O, "JwtIssuer", "string", "FGNS", "46.0", "Quem emitiu o JWT (diferencia maiúsculas).", S, notas=LEG),
 field(O, "JwtTextSubject", "string", "FGNS", "46.0", "Subject fixo do JWT ('Named Principal Subject').", S, notas=LEG),
 field(O, "JwtValidityPeriodSeconds", "int", "FGNS", "46.0", "Segundos de validade do JWT.", S, notas=LEG),
 field(O, "Language", "picklist", "FGRS", None, "Idioma do MasterLabel.", S),
 field(O, "MasterLabel", "string", "FGS", None, "Rótulo exibido (interno, não traduzido).", S),
 field(O, "NamespacePrefix", "string", "FGNS", None, "Prefixo de namespace do pacote gerenciado (até 15 caracteres).", S),
 field(O, "PrincipalType", "picklist", "FGRS", None, "Identidade usada no sistema externo (a descrição cita Anonymous e Named Principal).", S, notas=LEG)]
obj("NamedCredential", "Expõe por API as named credentials da org para consulta.", "Ver, sem abrir o Setup, quais named credentials existem e suas opções de callout.",
    [expo("padrao", "verificado", S, ["describeSObjects()", "query()", "retrieve()"], desde="33.0", acesso="Desde o Spring '20, exige View Setup and Configuration."), TOOL_D()],
    nc, [{"api": "padrao", "soql": "SELECT DeveloperName, MasterLabel, CalloutOptionsGenerateAuthorizationHeader FROM NamedCredential", "contexto": "API padrão.", "validacao": "documental"}],
    APEX_OK(S), cob("completa", 16, 16, cnt(nc), "Tabela de campos lida completa (16), conferida em segunda leitura."), S,
    alertas=["Vários campos são do modelo legado (obsoletos a partir da 56.0); o modelo atual separa URL (named credential) e autenticação (external credential).",
             "Alterar campos de autenticação por usuário pode invalidar credenciais e exigir nova autenticação."])

# ---------------- ConnectedApplication
S = "src:objref-connectedapplication"; O = "obj:ConnectedApplication"
TMO = ["1", "5", "10", "15", "30", "60", "90", "120", "240", "480", "720"]
TMO_N = "Minutos: 1, 5, 10, 15, 30 desde a 59.0; 60, 90, 120, 240, 480 e 720 desde a 65.0."
ca = [
 field(O, "MobileSessionTimeout", "picklist", "DFGNRS", None, "Tempo até deslogar usuários inativos no celular.", S),
 field(O, "MobileStartUrl", "url", "FNS", None, "Para onde vai o usuário depois de autenticar no celular.", S),
 field(O, "Name", "string", "FGIS", None, "Nome único.", S),
 field(O, "NamedUserUvidTimeout", "picklist", "FGNRS", "59.0", "Validade dos tokens JWT de usuários nomeados, quando o app tem tempo próprio.", S, vals=TMO, completa="sim", contexto=TMO_N),
 field(O, "OptionsAllowAdminApprovedUsersOnly", "boolean", "F", None, "Só usuários aprovados pelo admin acessam.", S),
 field(O, "OptionsCodeCredentialGuestEnabled", "desconhecido", None, None, "Reservado para uso futuro.", S, notas=["A página não informa tipo nem propriedades."]),
 field(O, "OptionsFullContentPushNotifications", "desconhecido", None, None, "Uso interno.", S, notas=INT),
 field(O, "OptionsHasSessionLevelPolicy", "boolean", "F", None, "Se o app exige sessão de alta garantia.", S),
 field(O, "OptionsIsInternal", "desconhecido", None, None, "Uso interno.", S, notas=INT),
 field(O, "OptionsRefreshTokenValidityMetric", "boolean", "F", None, "true: validade do refresh token conta a partir do último uso; false: pela duração.", S),
 field(O, "OptionsTokenExchangeManageBitEnabled", "boolean", "F", None, "Se o fluxo de troca de token (OAuth 2.0 token exchange) está ligado.", S),
 field(O, "PinLength", "picklist", "FGNRS", None, "Tamanho do PIN exigido em apps móveis.", S, vals=["4", "5", "6", "7", "8"], completa="sim"),
 field(O, "RefreshTokenValidityPeriod", "int", "FGNS", None, "Duração do token antes de expirar (horas, dias ou meses, conforme o app).", S),
 field(O, "StartUrl", "url", "FNS", None, "Para onde vai o usuário depois de autenticar fora do celular.", S),
 field(O, "UvidTimeout", "picklist", "FGNRS", "59.0", "Validade dos tokens JWT de usuários convidados (fluxo Authorization Code and Credentials).", S, vals=TMO, completa="sim", contexto=TMO_N)]
obj("ConnectedApplication", "Expõe por API os connected apps da org e suas políticas, só para leitura.", "Auditar políticas de sessão, PIN e tokens dos apps conectados.",
    [expo("padrao", "verificado", S, ["describeSObjects()", "query()", "retrieve()"], acesso="Todos os campos são somente leitura."), TOOL_D()],
    ca, [{"api": "padrao", "soql": "SELECT Name, OptionsAllowAdminApprovedUsersOnly, RefreshTokenValidityPeriod FROM ConnectedApplication", "contexto": "API padrão.", "validacao": "documental"}],
    APEX_OK(S), cob("completa", 15, 15, cnt(ca), "Tabela de campos lida completa (15), conferida em segunda leitura; versão do objeto não declarada."), S)

# ---------------- AuthProvider
S = "src:objref-authprovider"; O = "obj:AuthProvider"
SFM = ["Pode ficar em branco em provedores gerenciados pela Salesforce (desde a 33.0)."]
ap = [
 field(O, "AppleTeam", "string", "CFGNSU", "48.0", "Team ID (10 caracteres) da conta de desenvolvedor Apple.", S, req=("condicional", "Obrigatório para Apple.")),
 field(O, "AuthorizeUrl", "url", "CFNSU", "29.0", "Endpoint de autorização OAuth.", S, req=("condicional", "Obrigatório para OpenID Connect."), notas=SFM),
 field(O, "ConsumerKey", "string", "CFNSU", None, "Chave do app registrado no provedor externo.", S, notas=SFM),
 field(O, "ConsumerSecret", "string", "CN", None, "Segredo do app; definido na criação e não alterável depois.", S, notas=SFM),
 field(O, "CustomMetadataTypeRecord", "string", "CFGNSU", "36.0", "Nome de API do provedor customizado.", S, req=("condicional", "Obrigatório para plug-in customizado.")),
 field(O, "DefaultScopes", "string", "CFNSU", "29.0", "Escopos usados quando o fluxo não informa nenhum.", S),
 field(O, "DeveloperName", "string", "CFGSU", None, "Nome para referenciar o provedor no código.", S, req=("sim", None)),
 field(O, "EcKey", "string", "CFGNSU", "48.0", "Chave usada pelo provedor Apple.", S, req=("condicional", "Obrigatório para Apple.")),
 field(O, "ErrorUrl", "string", "CFNSU", None, "URL customizada para o provedor reportar erros.", S),
 field(O, "ExecutionUserId", "reference", "CFGNSU", "27.0", "Usuário (com Manage Users) que executa o handler de registro.", S, req=("condicional", "Obrigatório com handler de registro."),
       notas=["A página não nomeia o objeto de destino."]),
 field(O, "FlowDefaultAccountId", "reference", "CFGNSU", "64.0", "Conta padrão para novos usuários externos num handler de registro em flow.", S, notas=["Alvo implícito; a configuração do flow prevalece."]),
 field(O, "FlowDefaultProfileId", "reference", "CFGNSU", "64.0", "Perfil padrão para novos usuários num handler de registro em flow.", S, notas=["Alvo implícito; a configuração do flow prevalece."]),
 field(O, "FriendlyName", "string", "CFGISU", None, "Nome amigável.", S, req=("sim", None)),
 field(O, "IconUrl", "url", "CFNSU", "32.0", "Ícone do botão na página de login.", S),
 field(O, "IdTokenIssuer", "string", "CFNSU", "30.0", "Emissor do token (https); quando definido, o id_token é validado.", S),
 field(O, "LinkKickoffUrl", "url", "N", "43.0", "URL para ligar usuários existentes a uma conta externa (somente leitura).", S),
 field(O, "LogoutUrl", "url", "CFNSU", "33.0", "Para onde vai o usuário depois do logout do SSO.", S),
 field(O, "OauthKickoffUrl", "url", "N", "43.0", "URL para obter tokens OAuth de terceiros (somente leitura).", S),
 field(O, "OptionsIncludeOrgIdInId", "boolean", "CFU", "32.0", "Guarda o Id da org externa junto do Id do usuário; depois de ligado, não desliga.", S),
 field(O, "OptionsIsPkceEnabled", "boolean", "CFU", "59.0", "Liga o PKCE (Custom, Facebook, Google, Microsoft, OpenIdConnect e Salesforce).", S),
 field(O, "OptionsRequireMfa", "boolean", "F", None, "Exige MFA no SSO conforme a situação de MFA de cada usuário.", S),
 field(O, "OptionsSendAccessTokenInHeader", "boolean", "CFU", "30.0", "Envia o token ao UserInfoUrl no cabeçalho, não na query string.", S),
 field(O, "OptionsSendClientCredentialsInHeader", "boolean", "CFU", "30.0", "Envia as credenciais do cliente ao tokenUrl num cabeçalho Basic.", S),
 field(O, "OptionsSendSecretInApis", "boolean", "CFU", "47.0", "Inclui o segredo nas respostas da API; desligado, ele não aparece (pode quebrar change sets).", S,
       default=("valor", "true", "A página diz que vem ligado por padrão.")),
 field(O, "PluginId", "reference", "CFGNSU", "39.0", "Classe Apex que estende Auth.AuthProviderPluginClass.", S),
 field(O, "ProviderType", "picklist", "CFGRSU", None, "Tipo do provedor.", S, req=("sim", None),
       vals=["Apple", "Bitbucket", "CommerceCloudAccountManager", "Confluence3LO", "Custom", "Facebook", "GitHub", "Google", "Janrain", "LinkedIn", "Microsoft", "MicrosoftACS",
             "MuleSoftAnypointPlatform", "OpenIdConnect", "Salesforce", "Slack", "Twitter"], completa="sim",
       contexto="Versões: Apple 48.0, Bitbucket 61.0, CommerceCloudAccountManager 67.0, Confluence3LO 67.0, Custom 36.0, GitHub 35.0, LinkedIn 32.0, Microsoft 55.0, MicrosoftACS 31.0, MuleSoftAnypointPlatform 67.0, OpenIdConnect 29.0, Slack 54.0, Twitter 32.0."),
 field(O, "RegistrationHandlerId", "reference", "CFGNSU", None, "Classe Apex que implementa Auth.RegistrationHandler.", S),
 field(O, "SsoKickoffUrl", "url", "N", "43.0", "URL de SSO na Salesforce com credenciais externas (somente leitura).", S),
 field(O, "TokenUrl", "url", "CFNSU", "29.0", "Endpoint de token OpenID Connect.", S),
 field(O, "UserInfoUrl", "url", "CFNSU", "29.0", "Endpoint de user info OpenID Connect.", S, notas=SFM)]
obj("AuthProvider", "Expõe por API os provedores de autenticação (login por serviço externo), com criação e edição.", "Consultar ou automatizar a configuração de provedores de login e OAuth.",
    [expo("padrao", "verificado", S, ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"], desde="27.0",
          acesso="Exige Customize Application e Manage AuthProviders."), TOOL_D()],
    ap, [{"api": "padrao", "soql": "SELECT DeveloperName, FriendlyName, ProviderType FROM AuthProvider", "contexto": "API padrão.", "validacao": "documental"}],
    APEX_OK(S), cob("completa", 30, 30, cnt(ap), "Tabela de campos lida completa (30), conferida em segunda leitura."), S,
    alertas=["ConsumerSecret não muda depois de criado; OptionsIncludeOrgIdInId não pode ser desligado."])

# ---------------- OauthToken
S = "src:objref-oauthtoken"; O = "obj:OauthToken"
ot = [
 field(O, "AccessToken", "string", "FGNS", None, "Token usado na autorização (a página o descreve como refresh token).", S),
 field(O, "AppMenuItemId", "reference", "FGNS", None, "Item do App Picker ligado ao token.", S, ref=["AppMenuItem"]),
 field(O, "AppName", "string", "FGNS", None, "Rótulo do connected app do token.", S),
 field(O, "DeleteToken", "string", "FGNS", None, "Valor usado no endpoint de revogação para remover o token.", S),
 field(O, "Id", "ID", "DFGIS", None, "Reservado para uso futuro; sempre nulo.", S),
 field(O, "LastUsedDate", "dateTime", "FNS", None, "Último uso do token.", S),
 field(O, "RequestToken", "string", "FGNS", None, "Código de autorização usado para pedir o AccessToken.", S),
 field(O, "UseCount", "int", "FGNS", None, "Quantas vezes o token foi usado.", S),
 field(O, "UserId", "reference", "FGNS", None, "Dono do token.", S, ref=["obj:User"], rel="User")]
obj("OauthToken", "Tokens OAuth emitidos para connected apps, por usuário.", "Montar uma tela de gestão de tokens: ver uso e revogar.",
    [expo("padrao", "verificado", S, ["describeSObjects()", "query()"], desde="32.0", acesso="Com Customize Application, vê todos os tokens; sem, só os próprios."), TOOL_D()],
    ot, [{"api": "padrao", "soql": "SELECT AppName, UserId, LastUsedDate, UseCount FROM OauthToken", "contexto": "API padrão; até 500 linhas por query() e 2.500 no total.", "validacao": "documental"}],
    APEX_OK(S), cob("completa", 9, 9, cnt(ot), "Tabela de campos lida completa (9)."), S,
    alertas=["DML e consulta a OauthToken na mesma chamada Apex geram UncommittedWork.", "Consultas devolvem no máximo 2.500 registros; OFFSET vai até 2.000.",
             "Para revogar, envie o DeleteToken ao endpoint de revogação de tokens OAuth."])

# ---------------- ExternalDataSource
S = "src:objref-externaldatasource"; O = "obj:ExternalDataSource"
ed = [
 field(O, "AuthProviderId", "reference", "FGNS", "39.0", "Provedor de autenticação que cuida do login.", S, ref=["obj:AuthProvider"], rel="AuthProvider",
       notas=["Visível só com Customize Application e Manage AuthProviders."]),
 field(O, "CustomConfiguration", "textarea", "N", None, "Configuração em JSON própria do tipo de fonte.", S),
 field(O, "DeveloperName", "string", "FGS", None, "Nome de API único na org.", S),
 field(O, "Endpoint", "textarea", "N", None, "URL do sistema externo ou de uma named credential (callout:).", S),
 field(O, "isWritable", "boolean", "DFGS", "35.0", "Permite criar, alterar e excluir registros dos objetos externos (só Salesforce Connect).", S,
       notas=["Objetos externos são somente leitura por padrão; com o adaptador cross-org, true só a partir da 39.0."]),
 field(O, "Language", "picklist", "FGRS", None, "Idioma do MasterLabel.", S),
 field(O, "MasterLabel", "string", "FGS", None, "Rótulo (interno, não traduzido).", S),
 field(O, "NamedCredentialId", "reference", "FGNS", "58.0", "Named credential referenciada.", S, ref=["obj:NamedCredential"], rel="NamedCredential",
       notas=["Obrigatório para Amazon DynamoDB, Amazon Athena, GraphQL e OData 4.01; nulo nas demais."]),
 field(O, "NamespacePrefix", "string", "FGNS", None, "Prefixo de namespace (até 15 caracteres).", S),
 field(O, "PrincipalType", "picklist", "FGRS", None, "Uma credencial (NamedUser), uma por usuário (PerUser) ou nenhuma (Anonymous); na tela, Identity Type.", S,
       vals=["NamedUser", "PerUser", "Anonymous"], completa="sim"),
 field(O, "Protocol", "picklist", "FGRS", None, "Autenticação no sistema externo (OAuth, senha ou nenhuma; outros valores para algumas fontes).", S),
 field(O, "Repository", "string", "FGNS", None, "Repositório na fonte (só SharePoint Online).", S),
 field(O, "Type", "picklist", "FGRS", None, "Adaptador que conecta ao sistema externo.", S)]
obj("ExternalDataSource", "Expõe por API as fontes de dados externas da org.", "Consultar como os objetos externos se conectam aos sistemas de origem.",
    [expo("padrao", "verificado", S, ["describeSObjects()", "query()", "retrieve()"], desde="27.0", acesso="Desde a 48.0, só usuários autenticados (internos e externos)."), TOOL_D()],
    ed, [{"api": "padrao", "soql": "SELECT DeveloperName, Type, Endpoint, PrincipalType FROM ExternalDataSource", "contexto": "API padrão.", "validacao": "documental"}],
    APEX_OK(S), cob("completa", 13, 13, cnt(ed), "Tabela de campos lida completa (13)."), S)

# ---------------- CspTrustedSite
S = "src:objref-csptrustedsite"; O = "obj:CspTrustedSite"
DIR = lambda x: field(O, f"IsApplicableTo{x[0]}", "boolean", "CDFGSU", None, x[1], S)
cs = [
 field(O, "CanAccessCamera", "boolean", "CDFGSU", "59.0", "Se a URL pode acessar a câmera do usuário.", S, default=FALSE,
       notas=["Só vale com enablePermissionsPolicy true e grantCameraAccess TrustedUrls em SecuritySettings."]),
 field(O, "CanAccessMicrophone", "boolean", "CDFGSU", "59.0", "Se a URL pode acessar o microfone do usuário.", S, default=FALSE,
       notas=["Só vale com enablePermissionsPolicy true e grantMicrophoneAccess TrustedUrls em SecuritySettings."]),
 field(O, "Context", "picklist", "CFGRSU", "44.0", "Onde as diretivas CSP desta URL valem.", S,
       vals=["All", "Communities", "FieldServiceMobileExtension", "LEX", "LightningOut", "VisualForce"], completa="sim",
       contexto="LightningOut (64.0) é reservado para uso futuro; VisualForce desde a 55.0."),
 field(O, "Description", "textarea", "CFGNSU", None, "Descrição (até 255 caracteres).", S),
 field(O, "DeveloperName", "string", "CFGSU", None, "Nome de desenvolvedor.", S, notas=["Visível com View DeveloperName ou View Setup and Configuration."]),
 field(O, "EndpointUrl", "string", "CFGSU", None, "A URL confiável (domínio, porta opcional, * para subdomínios; https:// para APIs, wss:// para WebSocket).", S),
 field(O, "IsActive", "boolean", "CDFGSU", None, "Se a URL está ativa.", S)] + [DIR(x) for x in [
   ("ConnectSrc", "Permite carregar URLs por interfaces de script (connect-src)."), ("FontSrc", "Permite carregar fontes (font-src)."),
   ("FrameSrc", "Permite carregar conteúdo em iframe (frame-src)."), ("ImgSrc", "Permite carregar imagens (img-src)."),
   ("MediaSrc", "Permite carregar áudio e vídeo (media-src)."), ("StyleSrc", "Permite a componentes Lightning carregar folhas de estilo (style-src).")]] + [
 field(O, "Language", "picklist", "CDFGNRSU", None, "Idioma.", S),
 field(O, "MasterLabel", "string", "CFGSU", None, "Rótulo.", S),
 field(O, "NamespacePrefix", "string", "FGNS", None, "Prefixo de namespace (não criável nem editável).", S)]
obj("CspTrustedSite", "Expõe por API as trusted URLs (antes CSP Trusted Sites), com criação e edição.", "Consultar ou automatizar a allowlist de URLs e suas diretivas CSP.",
    [expo("padrao", "verificado", S, ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"], desde="39.0"), TOOL_D()],
    cs, [{"api": "padrao", "soql": "SELECT DeveloperName, EndpointUrl, Context, IsActive FROM CspTrustedSite", "contexto": "API padrão.", "validacao": "documental"}],
    APEX_OK(S), cob("completa", 16, 16, cnt(cs), "Tabela de campos lida completa (16)."), S,
    alertas=["Cada registro precisa de ao menos um campo grantAccess* ou isApplicableTo* verdadeiro."])

# ---------------- relacionamentos
def rel(rid, o, campo, d, expl, s):
    sv(f"relacionamentos/{rid}.json", {"id": "rel:" + rid, "tipo": "referencia_campo", "origem": {"entidade": o, "campo": campo}, "destino": {"entidade": d},
       "explicacao": expl, "estado": "verificado", "evidencias": [ev(s)],
       "cardinalidade_registros": {"estado": "desconhecido", "valor": "N:1", "nota": "Lookup indica N:1; obrigatoriedade não declarada na página."}})
rel("namedcredential-authprovider", "obj:NamedCredential", "AuthProviderId", "obj:AuthProvider", "Named credentials legadas guardam o provedor de autenticação (lookup).", "src:objref-namedcredential")
rel("externaldatasource-authprovider", "obj:ExternalDataSource", "AuthProviderId", "obj:AuthProvider", "A fonte de dados externa pode apontar um provedor de autenticação (lookup).", "src:objref-externaldatasource")
rel("externaldatasource-namedcredential", "obj:ExternalDataSource", "NamedCredentialId", "obj:NamedCredential", "Algumas fontes (DynamoDB, Athena, GraphQL, OData 4.01) exigem uma named credential (lookup).", "src:objref-externaldatasource")
rel("oauthtoken-user", "obj:OauthToken", "UserId", "obj:User", "Cada token pertence a um usuário (lookup).", "src:objref-oauthtoken")
def rep(rid, m, o, expl, srcs):
    sv(f"relacionamentos/{rid}.json", {"id": "rel:" + rid, "tipo": "representacao_comum", "origem": {"entidade": m}, "destino": {"entidade": o},
       "explicacao": expl + " A correspondência campo a campo não foi comprovada.", "estado": "verificado", "evidencias": [ev(s) for s in srcs]})
rep("rep-namedcredential", "mdt:NamedCredential", "obj:NamedCredential", "Metadata type e objeto API descrevem named credentials por caminhos diferentes: definição implantável versus registro consultável.",
    ["src:mdapi-namedcredential", "src:objref-namedcredential"])
rep("rep-connectedapp", "mdt:ConnectedApp", "obj:ConnectedApplication", "O metadata type define o connected app; o objeto expõe parte das políticas, só para leitura.",
    ["src:mdapi-connectedapp", "src:objref-connectedapplication"])
rep("rep-authprovider", "mdt:AuthProvider", "obj:AuthProvider", "Metadata type e objeto API descrevem provedores de autenticação: definição implantável versus registro editável por API.",
    ["src:mdapi-authprovider", "src:objref-authprovider"])
rep("rep-externaldatasource", "mdt:ExternalDataSource", "obj:ExternalDataSource", "Metadata type e objeto API descrevem fontes de dados externas: definição implantável versus registro consultável.",
    ["src:mdapi-externaldatasource", "src:objref-externaldatasource"])
rep("rep-csptrustedsite", "mdt:CspTrustedSite", "obj:CspTrustedSite", "Metadata type e objeto API descrevem trusted URLs: definição implantável versus registro editável por API.",
    ["src:mdapi-csptrustedsite", "src:objref-csptrustedsite"])

# ---------------- funcionalidades
def upd(fid, objs, srcs):
    f = ld(f"funcionalidades/{fid}.json"); r = f["representacoes"]["objetos_api"]; have = {x["ref"] for x in r}
    r += [{"ref": "obj:" + o, "papel": p} for o, p in objs if "obj:" + o not in have]
    f["representacoes"]["ausencias"] = [a for a in f["representacoes"]["ausencias"] if a.get("tipo") != "objeto_api"]
    f["evidencias"] += [ev(s) for s in srcs if not any(e["fonte"] == s for e in f["evidencias"])]
    sv(f"funcionalidades/{fid}.json", f)
upd("named-credentials", [("NamedCredential", "Consulta das named credentials (muitos campos são do modelo legado).")], ["src:objref-namedcredential"])
upd("connected-apps", [("ConnectedApplication", "Consulta das políticas do app, só leitura."), ("OauthToken", "Tokens emitidos por usuário; gestão e revogação.")],
    ["src:objref-connectedapplication", "src:objref-oauthtoken"])
upd("auth-providers", [("AuthProvider", "Provedor exposto por API, com criação e edição.")], ["src:objref-authprovider"])
upd("external-objects", [("ExternalDataSource", "Fonte de dados externa exposta para consulta.")], ["src:objref-externaldatasource"])
upd("csp-trusted-sites", [("CspTrustedSite", "Trusted URL exposta por API, com criação e edição.")], ["src:objref-csptrustedsite"])
print("ok lote 5j")
