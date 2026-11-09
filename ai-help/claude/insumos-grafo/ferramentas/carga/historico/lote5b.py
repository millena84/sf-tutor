# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5b (issue #24): Connected Apps, External Client Apps (núcleo) e OAuth.
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
NOMES = ["ConnectedApp", "ConnectedAppSettings", "ExternalClientApplication", "ExtlClntAppOauthSettings", "ExtlClntAppGlobalOauthSettings",
         "ExtlClntAppOauthConfigurablePolicies", "ExtlClntAppConfigurablePolicies", "ExternalClientAppSettings", "OauthCustomScope",
         "OauthTokenExchangeHandler", "OauthOidcSettings"]
novas = [{"id": f"src:mdapi-{n.lower()}", "titulo": f"{n} (Metadata API)", "url": B + f"meta_{n.lower()}.htm", "tipo": "oficial_documentacao", "versao": "68.0",
          "data_verificacao": DATA, "metodo": "extracao_documental_assistida", "pertinencia": f"Arquivo, versão e propriedades do tipo {n}.",
          "extracao": "fontes/extracoes/mdapi-lote5b.txt", "checagem_online": CHK} for n in NOMES]
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

# ================================================================ arquivos dos tipos Settings
SET = {"ConnectedAppSettings": "ConnectedApp", "OauthOidcSettings": "OauthOidc", "ExternalClientAppSettings": None}
_orig = M.arquivos
def _arquivos(nome, parent=None):
    if nome in SET:
        base = SET[nome]; s = f"src:mdapi-{nome.lower()}"
        if base is None:
            return {"source_format": af("desconhecido", {"pasta": "settings/", "arquivo": None},
                        "Tipo da família Settings (pasta settings/ do registro do Salesforce CLI); a página não informa o nome-base do arquivo.", [ev("src:sdr-registry", "types.settings"), ev(s)]),
                    "metadata_api_format": af("desconhecido", {"pasta": "settings/", "arquivo": None}, "Nome-base do arquivo não informado na página.", [ev(s)])}
        return {"source_format": af("verificado", {"pasta": "settings/", "arquivo": f"{base}.settings-meta.xml"},
                    "Pasta e sufixo do tipo genérico Settings no registro do Salesforce CLI; o nome-base do arquivo vem da página do tipo.",
                    [ev("src:sdr-registry", "types.settings"), ev(s)]),
                "metadata_api_format": af("verificado", {"pasta": "settings/", "arquivo": f"{base}.settings"},
                    "Um único arquivo por tipo de configuração; no package.xml, o tipo é Settings e o membro é o nome-base.", [ev(s)])}
    return _orig(nome, parent)
M.arquivos = _arquivos

def P(n, t, ver=None, d=None, req="N", **kw): return (n, t, req, ver, d, kw)
DF = ("valor", "false", None)
DT = ("valor", "true", None)
FN = lambda: M.FULLNAME_HERDADO(None)
INT = {"notas": ["Reservado para uso interno da Salesforce (página oficial)."]}
def V(*vals): return [(v, None) for v in vals]
SETUP_NV = af("desconhecido", None, "Caminho no Setup não verificado nesta sessão.")
SCOPES = V("Basic", "Api", "Web", "Full", "Chatter", "CustomApplications", "RefreshToken", "OpenID", "Profile", "Email", "Address", "Phone", "OfflineAccess",
           "CustomPermissions", "Wave", "Eclair", "Pardot", "Lightning", "Content", "CDPIngest", "Chatbot", "ForgotPassword", "UserRegistration", "PwdlessLogin")

# ================================================================ estruturas
S = "src:mdapi-connectedapp"
M.struct("ConnectedAppAttribute", S, ["mdt:ConnectedApp"], [P("formula", "string", None, "Valor do atributo (fórmula).", "S"), P("key", "string", None, "Identificador do atributo.", "S")],
         "Atributo customizado do connected app.")
M.struct("ConnectedAppCanvasConfig", S, ["mdt:ConnectedApp"], [
 P("accessMethod", "string", None, "Como o app canvas inicia o OAuth: Get pede autorização ao usuário; Post usa a instalação feita pelo administrador.", "S", vals=V("Get", "Post")),
 P("canvasUrl", "string", None, "URL do app de terceiro exibido como canvas.", "S"),
 P("lifecycleClass", "string", "31.0", "Classe Apex Canvas.CanvasLifecycleHandler, se houver parâmetros customizados."),
 P("locations", "string[]", None, "Onde o app canvas pode aparecer.", vals=[("Aura", None), ("AppLauncher", "reservado"), ("Chatter", None), ("ChatterFeed", None), ("MobileNav", "desde 31.0"),
   ("None", None), ("OpenCTI", None), ("PageLayout", "desde 31.0"), ("Publisher", None), ("ServiceDesk", None), ("UserProfile", "reservado"), ("Visualforce", None)]),
 P("options", "string[]", None, "Esconde o botão Share ou o cabeçalho, ou permite instalar como app pessoal.", vals=[("HideShare", "desde 30.0"), ("HideHeader", "desde 30.0"), ("PersonalEnabled", "desde 32.0")]),
 P("samlInitiationMethod", "string", None, "Quem inicia o SSO por SAML, ou nenhum.", vals=[("IdpInitiated", None), ("SpInitiated", None), ("None", "desde 31.0")])],
 "Configuração de um connected app exibido como app canvas.")
M.struct("ConnectedAppIpRange", S, ["mdt:ConnectedApp"], [P("description", "string", "31.0", "Que parte da rede a faixa cobre."),
 P("end", "string", None, "Último IP da faixa (inclusive).", "S"), P("start", "string", None, "Primeiro IP da faixa (inclusive).", "S")],
 "Faixa de IPs que acessa o app sem autenticação do usuário.")
M.struct("ConnectedAppOauthAssetToken", S, ["mdx:ConnectedAppOauthConfig"], [
 P("assetAudiences", "string", "49.0", "Destinatários do JWT (claim aud).", "S"),
 P("assetIncludeAttributes", "boolean", "49.0", "Inclui atributos customizados no token.", "S", default=DT),
 P("assetIncludeCustomPerms", "boolean", "49.0", "Inclui permissões customizadas no token.", "S", default=DT),
 P("assetSigningCertId", "string", "49.0", "Id do certificado que assina o JWT (até 4 KB).", "S"),
 P("assetValidityPeriod", "int", "49.0", "Expiração do token; precisa expirar em até 3 minutos.", "S")],
 "Configuração do asset token (JWT) do connected app.")
M.struct("ConnectedAppOauthIdToken", S, ["mdx:ConnectedAppOauthConfig"], [
 P("idTokenAudience", "string", None, "Audiências a que o ID token se destina.", default=("valor", "o client_id do app", "Quando nenhuma audiência é definida.")),
 P("idTokenIncludeAttributes", "boolean", None, "Inclui atributos no ID token."),
 P("idTokenIncludeCustomPerms", "boolean", None, "Inclui permissões customizadas no ID token."),
 P("idTokenIncludeStandardClaims", "boolean", None, "Inclui as claims padrão do evento de autenticação."),
 P("idTokenValidity", "int", None, "Validade do token depois de emitido, em minutos (1 a 720).", default=("valor", "2", None))], "Configuração do ID token do app.")
M.struct("ConnectedAppOauthPolicy", S, ["mdt:ConnectedApp"], [
 P("ipRelaxation", "string", None, "Como as restrições de IP se aplicam.", "S", vals=[("ENFORCE", None), ("BYPASS_2FACTOR", None), ("BYPASS", None), ("ENFORCE_RELAXREFRESH", None)], default=("valor", "ENFORCE", None)),
 P("refreshTokenPolicy", "string", None, "Validade do refresh token.", "S",
   vals=[("zero", None), ("infinite", None), ("specific_lifetime:n:HOURS|DAYS|MONTHS", "validade fixa"), ("specific_inactivity:n:HOURS|DAYS|MONTHS", "expira após inatividade")], default=("valor", "infinite", None)),
 P("singleLogoutUrl", "string", None, "Endpoint de logout (URL absoluta https).")], "Políticas OAuth do app.")
M.struct("ConnectedAppSamlConfig", S, ["mdt:ConnectedApp"], [
 P("acsUrl", "string", None, "URL ACS do provedor de serviço.", "S"), P("certificate", "string", None, "Certificado PEM."),
 P("encryptionCertificate", "string", "30.0", "Nome do certificado (Certificate and Key Management) que cifra as asserções."),
 P("encryptionType", "string", "30.0", "Método de cifragem das asserções.", vals=[("AES_128", None), ("AES_256", None)]),
 P("entityUrl", "string", None, "Entity ID do provedor de serviço.", "S"), P("issuer", "string", "29.0", "URI que identifica o emissor da resposta SAML."),
 P("samlIdpSLOBindingEnum", "string", "40.0", "Binding do logout único.", vals=[("PostBinding", None), ("RedirectBinding", None)]),
 P("samlNameIdFormat", "string", "29.0", "Formato do NameID.", vals=[("Unspecified", None), ("EmailAddress", None), ("Persistent", None), ("Transient", None)], default=("valor", "Unspecified", None)),
 P("samlSigningAlgoType", "string", "50.0", "Algoritmo de assinatura.", vals=[("SHA1", None), ("SHA256", None)]),
 P("samlSloUrl", "string", "40.0", "Endpoint de logout único do provedor de serviço."),
 P("samlSubjectCustomAttr", "string", "29.0", "Campo usado como identidade.", "C:com samlSubjectType CustomAttr"),
 P("samlSubjectType", "string", None, "Tipo de identificador do usuário.", "S", vals=[("Username", None), ("FederationId", None), ("UserId", None), ("PersistentID", None), ("CustomAttr", None)])],
 "Configuração SAML do app (Salesforce como provedor de identidade).")
M.struct("ConnectedAppSessionPolicy", S, ["mdt:ConnectedApp"], [
 P("policyAction", "string", None, "O que fazer com sessões de alta garantia.", vals=[("Block", None), ("RaiseSessionLevel", None)]),
 P("sessionLevel", "string", None, "Aplica o nível de sessão de alta garantia (exige MFA)."),
 P("sessionTimeout", "int", None, "Duração da sessão; sem valor, vale a do perfil e depois a da org.", notas=["A página não declara a unidade."])], "Políticas de sessão do app.")
M.struct("ConnectedAppOauthConfig", S, ["mdt:ConnectedApp"], [
 P("assetTokenConfig", "ConnectedAppOauthAssetToken", "49.0", "Configuração do asset token.", estrutura="ConnectedAppOauthAssetToken"),
 P("callbackUrl", "string", None, "Endereço de retorno do OAuth (redirect URI).", "S"),
 P("certificate", "string", None, "Certificado PEM, se o app usar."),
 P("consumerKey", "string", "32.0", "Identificador público do app (client_id); só definido na criação.", restr="8 a 256 caracteres alfanuméricos, único globalmente."),
 P("consumerSecret", "string", "32.0", "Segredo do app (client_secret); só definido na criação e não devolvido nas respostas de metadata.", restr="8 a 256 caracteres alfanuméricos."),
 P("idTokenConfig", "ConnectedAppOauthIdToken", "43.0", "Configuração do ID token.", estrutura="ConnectedAppOauthIdToken"),
 P("isAdminApproved", "boolean", "46.0", "Só usuários com o perfil ou permission set certo acessam, sem aprovar o app.", default=DF),
 P("isClientCredentialEnabled", "boolean", "56.0", "Habilita o fluxo client credentials; exige oauthClientCredentialUser.", default=DF),
 P("isCodeCredentialEnabled", "boolean", "57.0", "Habilita o fluxo Authorization Code and Credentials (identidade headless).", default=DF),
 P("isCodeCredentialPostOnly", "boolean", "57.0", "Exige as credenciais no corpo do POST.", default=DF),
 P("isConsumerSecretOptional", "boolean", "49.0", "Dispensa o segredo no fluxo web server para apps que não conseguem guardá-lo.", default=DF),
 P("isIntrospectAllTokens", "boolean", "49.0", "Permite inspecionar todos os tokens da org, não só os do app.", default=DF),
 P("isNamedUserJwtEnabled", "boolean", "59.0", "Emite tokens de acesso no formato JWT."),
 P("isPkceRequired", "boolean", "59.0", "Exige PKCE nos fluxos de código de autorização.", default=DF),
 P("isRefreshTokenRotationEnabled", "boolean", "60.0", "Emite novo refresh token a cada uso e invalida o anterior."),
 P("isSecretRequiredForRefreshToken", "boolean", "51.0", "Exige o segredo no fluxo de refresh token.", default=DT),
 P("isSecretRequiredForTokenExchange", "boolean", "60.0", "Exige o segredo na troca de token; só para apps com backend privado."),
 P("isTokenExchangeEnabled", "boolean", "60.0", "Permite trocar tokens de um provedor externo por tokens da Salesforce."),
 P("oauthClientCredentialUser", "string", "56.0", "Usuário com que os tokens do client credentials executam; precisa da permissão API Only."),
 P("scopes", "string[]", None, "Escopos OAuth concedidos.", vals=SCOPES, contexto="Lista dos valores aceitos no deploy, conforme a página."),
 P("singleLogoutUrl", "string", None, "Endereço que recebe o pedido de logout.")],
 "Como o connected app conversa com a Salesforce por OAuth.")
S = "src:mdapi-extlclntappoauthsettings"
M.struct("ExtlClntAppOauthSettingsAttribute", S, ["mdt:ExtlClntAppOauthSettings"], [P("formula", "string", None, "Campo que fornece o valor (ex.: Organization.Country).", "S"),
 P("key", "string", None, "Nome único do atributo.", "S")], "Atributo padrão definido pelo desenvolvedor.")
M.struct("ExtlClntAppOauthIpRange", S, ["mdt:ExtlClntAppOauthSettings"], [P("description", "string", None, "O que a faixa representa."),
 P("endIpAddress", "string", None, "Último endereço (inclusive).", "C:obrigatório junto com startIpAddress"),
 P("startIpAddress", "string", None, "Primeiro endereço (inclusive).", "C:obrigatório junto com endIpAddress")], "Faixa de IPs confiáveis.")
S = "src:mdapi-extlclntappglobaloauthsettings"
M.struct("ExternalAppIdTokenConfig", S, ["mdt:ExtlClntAppGlobalOauthSettings"], [
 P("idTokenAudience", "string", None, "Público do ID token; padrão é o client_id."), P("idTokenIncludeAttributes", "boolean", None, "Inclui atributos no ID token."),
 P("idTokenIncludeStandardClaims", "boolean", None, "Inclui as claims padrão do evento de autenticação."),
 P("idTokenValidityInMinutes", "int", None, "Validade do ID token em minutos (1 a 720).", default=("valor", "2", None))], "Configuração do ID token do external client app.")
S = "src:mdapi-extlclntappoauthconfigurablepolicies"
M.struct("ExtlClntAppOauthPoliciesAttribute", S, ["mdt:ExtlClntAppOauthConfigurablePolicies"], [P("formula", "string", None, "Campo que fornece o valor.", "S"),
 P("key", "string", None, "Nome único do atributo.", "S")], "Atributo padrão definido pelo administrador.")
S = "src:mdapi-oauthtokenexchangehandler"
M.struct("OauthTokenExchHandlerApp", S, ["mdt:OauthTokenExchangeHandler"], [
 P("apexExecutionUser", "string", None, "Usuário que executa o handler Apex (a página recomenda um usuário de integração).", "S"),
 P("connectedApp", "string", None, "Connected app para o qual o handler está habilitado."),
 P("externalClientApp", "string", None, "External client app para o qual o handler está habilitado."),
 P("isDefault", "boolean", None, "Handler padrão do app quando a requisição não indica um.", "S")], "Habilitação do handler de troca de token para um app.")

# ================================================================ metadata types
def MT(nome, o, f, desde, rows, **kw):
    return M.mdt(nome, f"src:mdapi-{nome.lower()}", o, f, desde, rows, setup=SETUP_NV, **kw)
ECA = "Nome do external client app ao qual este componente pertence."

MT("ConnectedApp", "Define um connected app: como um sistema externo se conecta à org por OAuth, SAML ou canvas.",
   "Registrar integrações e apps de terceiros, com suas políticas de acesso.", "29.0", [
 P("attributes", "ConnectedAppAttribute[]", None, "Atributos customizados do app.", estrutura="ConnectedAppAttribute",
   notas=["A tabela oficial mostra 'canvasConfig' como tipo desta linha; ver a divergência documental."]),
 P("canvasConfig", "ConnectedAppCanvasConfig", None, "Configuração de app canvas.", estrutura="ConnectedAppCanvasConfig", estado="desconhecido",
   notas=["Leitura do projeto, não confirmada: a tabela tem uma linha sem nome com o tipo AppCanvasConfig logo após attributes."]),
 P("contactEmail", "string", None, "E-mail de contato do responsável pelo app.", "S"), P("contactPhone", "string", None, "Telefone de contato."),
 P("description", "string", None, "Descrição."), P("iconUrl", "string", None, "Reservado para uso futuro.", **INT), P("infoUrl", "string", None, "URL com mais informações."),
 P("ipRanges", "ConnectedAppIpRange[]", None, "Faixas de IP que acessam sem autenticação do usuário.", estrutura="ConnectedAppIpRange"),
 P("label", "string", None, "Nome do app.", "S"),
 P("logoUrl", "string", None, "Logo exibido na lista de apps e na tela de consentimento (https; até 125 px de altura e 200 de largura)."),
 P("mobileStartUrl", "string", None, "Para onde vão os usuários depois de autenticar num dispositivo móvel."),
 P("oauthConfig", "ConnectedAppOauthConfig", None, "Configuração OAuth.", estrutura="ConnectedAppOauthConfig"),
 P("oauthPolicy", "ConnectedAppOauthPolicy", "49.0", "Políticas de acesso OAuth (relaxamento de IP, validade do refresh token etc.).", estrutura="ConnectedAppOauthPolicy"),
 P("permissionSetName", "string", "46.0", "Permission sets exigidos para usar o app (um por linha); exige isAdminApproved = true."),
 P("plugin", "string", None, "Classe Apex que estende Auth.ConnectedAppPlugin."),
 P("pluginExecutionUser", "string", "46.0", "Usuário com que o plugin executa."),
 P("profileName", "string[]", "46.0", "Perfis exigidos para usar o app; exige isAdminApproved = true."),
 P("samlConfig", "ConnectedAppSamlConfig", None, "Configuração de login único por SAML.", estrutura="ConnectedAppSamlConfig"),
 P("sessionPolicy", "ConnectedAppSessionPolicy", "49.0", "Políticas de sessão.", estrutura="ConnectedAppSessionPolicy"),
 P("startUrl", "string", None, "Para onde vão os usuários (fora do celular) depois de autenticar."), FN()], curinga=True,
 alertas=["A página informa que a criação de connected apps é restrita a partir do Spring '26; apps existentes continuam funcionando, e a Salesforce recomenda external client apps.",
          "consumerSecret não é devolvido nas respostas de metadata."],
 divergencias=["A tabela oficial (src:mdapi-connectedapp) mostra a linha 'attributes' com tipo 'canvasConfig' e uma linha seguinte sem nome, com tipo AppCanvasConfig."],
 cobertura_nota="Universo esperado = 19 linhas da tabela Fields (a 2ª sem nome) mais fullName herdado.")
MT("ConnectedAppSettings", "Configurações da org para connected apps.", "Restringir o acesso à API a apps aprovados pelo administrador.", "47.0", [
 P("enableAdminApprovedAppsOnly", "boolean", None, "Só apps aprovados ou instalados pelo administrador podem chamar a API (o API Access Control é habilitado pelo Suporte).", default=DF),
 P("enableAdminApprovedAppsOnlyForExternalUser", "boolean", None, "Clientes e parceiros só usam apps instalados e desbloqueados na org.", default=DF),
 P("enableSkipUserProvisioningWizardWelcomePage", "boolean", None, "Deixa de exibir a página de boas-vindas do assistente de provisionamento de usuários.", default=DF)],
 curinga=False, alertas=["No package.xml, use o tipo Settings com o membro ConnectedApp."])
MT("ExternalClientApplication", "Define um external client app: o sucessor dos connected apps para integrações e apps externos.",
   "Registrar integrações com configuração separada em componentes (OAuth, políticas, plugins), mais fácil de empacotar.", "59.0", [
 P("contactEmail", "string", None, "E-mail do administrador do app na org assinante."), P("contactPhone", "string", None, "Telefone do administrador."),
 P("description", "string", None, "Descrição."),
 P("distributionState", "string", None, "Como o app é distribuído.", vals=[("AutoInstalled", "uso interno"), ("Local", None), ("Managed", "uso interno"), ("Packaged", None)]),
 P("iconUrl", "string", None, "URL do ícone."), P("infoUrl", "string", None, "Reservado para uso futuro.", **INT),
 P("isProtected", "boolean", None, "Controla a visibilidade do componente em orgs assinantes (pacotes).", default=DF),
 P("label", "string", None, "Rótulo."), P("logoUrl", "string", None, "URL do logo."),
 P("managedType", "string", None, "Uso interno.", natureza="desconhecida", contexto="Enumeração de uso interno; valores não listados na página.", **INT),
 P("orgScopedExternalApp", "string", None, "Identificador único [Id da org]:[nome do app]; definido pelo desenvolvedor ou gerado no primeiro deploy."), FN()], curinga=True,
 alertas=["Usar o tipo exige a permissão Opt in to External Client Apps."])
MT("ExtlClntAppOauthSettings", "Configurações OAuth de um external client app definidas pelo desenvolvedor.",
   "Declarar escopos, IPs confiáveis, atributos e o asset token do app.", "59.0", [
 P("areAttributesIncludedInAssetToken", "boolean", "61.0", "Inclui atributos customizados nos asset tokens.", default=DF),
 P("areCustomPermsIncludedInAssetToken", "boolean", "61.0", "Inclui permissões customizadas nos asset tokens.", default=DF),
 P("assetTokenAudiences", "string", "61.0", "Claim aud: quem consome o asset token.", "C:obrigatório no fluxo de asset token"),
 P("assetTokenSigningCertificate", "string", "61.0", "Certificado que assina os asset tokens (até 4 KB).", "C:obrigatório no fluxo de asset token"),
 P("assetTokenValidity", "int", "61.0", "Validade do asset token em segundos.", "C:obrigatório no fluxo de asset token"),
 P("clientAssertionCertificate", "string", None, "Certificado que valida JWTs de atestação do cliente em fluxos headless first-party."),
 P("commaSeparatedOauthScopes", "string", None, "Escopos OAuth do app, separados por vírgula.",
   notas=["A página lista os escopos aceitos (Basic, Api, Web, Full, Chatter, RefreshToken, OpenID, CDP*, EinsteinGPT, MCP, entre outros)."]),
 P("customAttributes", "ExtlClntAppOauthSettingsAttribute[]", None, "Atributos padrão (até 128).", estrutura="ExtlClntAppOauthSettingsAttribute"),
 P("externalClientApplication", "string", None, ECA, "S"),
 P("isFirstPartyAppEnabled", "boolean", None, "Permite a apps first-party chamar o endpoint headless de desafio de autorização no site Experience Cloud."),
 P("label", "string", None, "Rótulo."), P("oauthLink", "string", None, "Valor gerado, somente leitura: Id da org mais o Consumer ID."),
 P("singleLogoutUrl", "string", None, "Endereço que recebe o pedido de logout."),
 P("trustedIpRanges", "ExtlClntAppOauthIpRange[]", None, "Faixas de IP sem exigência de autenticação do usuário (até 128).", estrutura="ExtlClntAppOauthIpRange"), FN()], curinga=True)
MT("ExtlClntAppGlobalOauthSettings", "Configurações OAuth globais de um external client app: chaves, callback e fluxos habilitados.",
   "Separar segredos e fluxos (que mudam por org) das configurações declaradas pelo desenvolvedor.", "59.0", [
 P("callbackUrl", "string", None, "URL de retorno do OAuth (redirect_uri)."), P("certificate", "string", "60.0", "Certificado PEM; habilita o fluxo JWT Bearer."),
 P("consumerKey", "string", None, "Identificador do consumidor (client_id)."), P("consumerSecret", "string", None, "Segredo do consumidor (client_secret)."),
 P("externalClientApplication", "string", None, ECA, "S"),
 P("idTokenConfig", "ExternalAppIdTokenConfig", None, "Configuração do ID token.", estrutura="ExternalAppIdTokenConfig"),
 P("isClientCredentialsFlowEnabled", "boolean", "60.0", "Habilita o fluxo client credentials."),
 P("isCodeCredFlowEnabled", "boolean", "61.0", "Permite variantes headless, sem senha e de convidado do fluxo código e credenciais.", default=DF),
 P("isCodeCredPostOnly", "boolean", "61.0", "Exige credenciais por POST em services/oauth2/authorize.", default=DF),
 P("isConsumerSecretOptional", "boolean", None, "Dispensa o segredo na troca de token do fluxo web server.", default=DF),
 P("isDeviceFlowEnabled", "boolean", "60.0", "Habilita o fluxo device."),
 P("isIntrospectAllTokens", "boolean", None, "Permite inspecionar e renovar todos os tokens, não só os do app.", default=DF),
 P("isNamedUserJwtEnabled", "boolean", "61.0", "Emite tokens de acesso JWT em vez de opacos.", default=DF),
 P("isPkceRequired", "boolean", None, "Torna o PKCE obrigatório.", default=DT),
 P("isRefreshTokenRotationEnabled", "boolean", "60.0", "Habilita a rotação de refresh tokens."),
 P("isSecretRequiredForRefreshToken", "boolean", None, "Exige o segredo em requisições de refresh.", default=DT),
 P("isSecretRequiredForTokenExchange", "boolean", "60.0", "Exige o segredo na troca de token."),
 P("isTokenExchangeEnabled", "boolean", "60.0", "Habilita a troca de token."), P("label", "string", None, "Rótulo."),
 P("shouldRotateConsumerKey", "boolean", None, "Troca a consumer key no deploy (exige ignorar avisos no comando de deploy).", default=DF),
 P("shouldRotateConsumerSecret", "boolean", None, "Troca o consumer secret no deploy (exige ignorar avisos no comando de deploy).", default=DF), FN()], curinga=True)
MT("ExtlClntAppOauthConfigurablePolicies", "Políticas OAuth de um external client app definidas pelo administrador.",
   "Controlar quem pode usar o app, validade de tokens e sessões, e restrições de IP.", "59.0", [
 P("apexHandler", "string", "61.0", "Handler Apex."), P("clientCredentialsFlowUser", "string", "60.0", "Usuário de execução do client credentials (precisa da permissão API Only)."),
 P("commaSeparatedCustomScopes", "string", "61.0", "Escopos customizados, separados por vírgula."),
 P("commaSeparatedPermissionSet", "string", None, "Ids de permission sets, separados por vírgula; usado com AdminApprovedPreAuthorized."),
 P("commaSeparatedProfile", "string", None, "Perfis, separados por vírgula; usado com AdminApprovedPreAuthorized."),
 P("customAttributes", "ExtlClntAppOauthPoliciesAttribute[]", None, "Atributos padrão definidos pelo administrador (até 128).", estrutura="ExtlClntAppOauthPoliciesAttribute"),
 P("executeHandlerAs", "string", "61.0", "Usuário que executa o handler Apex."),
 P("externalClientApplication", "string", None, ECA, "S"),
 P("guestJwtTimeout", "int", "61.0", "Validade, em minutos, dos tokens JWT de usuários convidados.", "C:obrigatório quando guestJwtSessionTimeoutType é Custom",
   vals=[(v, None) for v in ["1", "5", "10", "15", "30"]] + [(v, "desde 65.0") for v in ["60", "90", "120", "240", "480", "720"]]),
 P("guestJwtSessionTimeoutType", "string", "65.0", "Se a validade do JWT de convidado segue a sessão ou guestJwtTimeout.", vals=V("UserSession", "Custom")),
 P("ipRelaxationPolicyType", "string", None, "Política de restrição de IP.", vals=V("Enforce", "Bypass", "Bypass_2factor", "Enforce_RelaxRefresh")),
 P("isClientCredentialsFlowEnabled", "boolean", "60.0", "Liga o fluxo client credentials.", default=DF),
 P("isGuestCodeCredFlowEnabled", "boolean", "61.0", "Permite a variante de convidado do fluxo código e credenciais (o app precisa emitir JWT).", default=DF),
 P("isNamedUserJwtEnabled", "boolean", None, "Antigo controle de JWT para usuários nomeados; removido.", ate="63.0", default=DF, nota_versao="Obsoleto; removido na 64.0."),
 P("isTokenExchangeFlowEnabled", "boolean", "60.0", "Liga o fluxo de troca de token.", default=DF), P("label", "string", None, "Rótulo."),
 P("namedUserJwtTimeout", "int", "61.0", "Validade, em minutos, dos tokens JWT de usuários nomeados (mesmos valores de guestJwtTimeout).", "C:obrigatório quando namedUserJwtSessionTimeoutType é Custom"),
 P("namedUserJwtSessionTimeoutType", "string", "65.0", "Se a validade do JWT de usuário nomeado segue a sessão ou namedUserJwtTimeout.", vals=V("UserSession", "Custom")),
 P("permittedUsersPolicyType", "string", None, "Quem pode usar o app.", vals=[("AdminApprovedPreAuthorized", "só usuários pré-autorizados pelo administrador"), ("AllSelfAuthorized", "qualquer usuário que autorize")]),
 P("policyAction", "string", None, "Ação quando o nível de sessão exigido não é atendido.", vals=V("Block", "RaiseSessionLevel")),
 P("refreshTokenPolicyType", "string", None, "Quando o refresh token expira.", vals=V("Infinite", "SpecificInactivity", "SpecificLifetime", "Zero")),
 P("refreshTokenValidityPeriod", "int", None, "Quantidade de unidades até expirar.", "C:usado com SpecificInactivity ou SpecificLifetime"),
 P("refreshTokenValidityUnit", "string", None, "Unidade da validade.", "C:usado com SpecificInactivity ou SpecificLifetime", vals=V("Days", "Hours", "Months")),
 P("requiredSessionLevel", "string", None, "Nível de segurança de sessão exigido.", vals=V("HIGH_ASSURANCE", "LOW", "STANDARD")),
 P("sessionTimeoutInMinutes", "int", None, "Duração da sessão; só para apps que emitem tokens opacos."),
 P("singleLogoutUrl", "string", None, "Endereço que recebe o pedido de logout."), P("startUrl", "string", None, "Para onde vão os usuários depois de autenticar."), FN()], curinga=True,
 divergencias=["O exemplo XML da página (src:mdapi-extlclntappoauthconfigurablepolicies) fecha namedUserJwtTimeout com etiqueta errada."])
MT("ExtlClntAppConfigurablePolicies", "Liga ou desliga os plugins (OAuth, SAML, canvas, mobile, push, notificação) de um external client app.",
   "Controlar, na org, quais capacidades do app ficam ativas.", "60.0", [
 P("externalClientApplication", "string", None, ECA, "S"),
 P("isEnabled", "boolean", "60.0", "Chave geral: true habilita todos os plugins (salvo os desligados um a um); false desabilita todos.", "S", default=DT),
 P("isCanvasPluginEnabled", "boolean", "66.0", "Liga o plugin de app canvas.", default=DT), P("isMobilePluginEnabled", "boolean", "63.0", "Liga o plugin mobile.", default=DT),
 P("isNotificationPluginEnabled", "boolean", "63.0", "Liga o plugin de notificação.", default=DT), P("isOauthPluginEnabled", "boolean", "60.0", "Liga o plugin OAuth.", default=DT),
 P("isPushPluginEnabled", "boolean", "63.0", "Liga o plugin de push notification.", default=DT), P("isSamlPluginEnabled", "boolean", "63.0", "Liga o plugin SAML.", default=DT),
 P("label", "string", None, "Rótulo."), P("startPage", "string", "63.0", "Que tipo de URL é usada como página inicial.", vals=V("Custom", "None", "OAuth")),
 P("startUrl", "string", "63.0", "URL customizada de destino depois da autenticação."), FN()], curinga=True)
MT("ExternalClientAppSettings", "Configurações da org para external client apps.", "Controlar acesso a segredos via API e empacotamento de apps.", "58.0", [
 P("enableClientSecretInRestApiAccess", "boolean", "62.0", "Se os consumer secrets podem ser lidos pela API REST de credenciais."),
 P("enableConsumerSecretApiAccess", "boolean", None, "Obsoleto: controlava a leitura dos consumer secrets pela Metadata API.", notas=["A página marca como DEPRECATED e orienta usar a interface OAuth do external client app."]),
 P("enablePackageEcaOauthFromDevOrg", "boolean", "62.0", "Permite empacotar external client apps de uma org que não é Dev Hub (orgs efêmeras continuam fora).")],
 curinga=False)
MT("OauthCustomScope", "Define um escopo OAuth customizado, que um connected app pode solicitar.",
   "Dar a sistemas externos permissões específicas, além dos escopos padrão.", "46.0", [
 P("assignedTo", "OauthCustomScopeApp", "49.0", "Connected app que recebe o escopo (com namespace, se empacotado).", natureza="referencia",
   contexto="A página tipa como OauthCustomScopeApp e espera o nome do connected app."),
 P("description", "string", None, "O que o escopo permite (único, alfanumérico, até 60 caracteres; aceita rótulo customizado).", "S"),
 P("developerName", "string", None, "Identificador usado no código.", "S"),
 P("isProtected", "boolean", None, "Componentes protegidos não podem ser referenciados por componentes da org que instala o pacote.", "S"),
 P("isPublic", "boolean", None, "Se o escopo aparece no endpoint de descoberta OpenID Connect do app.", default=DF),
 P("masterLabel", "string", None, "Rótulo (começa com letra; letras, números e sublinhado; sem espaços; único).", "S"), FN()], curinga=True,
 divergencias=["O exemplo XML (src:mdapi-oauthcustomscope) mostra um elemento connectedApp dentro de assignedTo, não descrito na tabela.",
               "A descrição de isProtected na página tem um valor faltando entre parênteses."])
MT("OauthTokenExchangeHandler", "Define um handler Apex que valida tokens de um provedor externo e os troca por tokens da Salesforce.",
   "Implementar o fluxo de troca de token (token exchange) com mapeamento de usuários.", "60.0", [
 P("description", "string", None, "Descrição.", "S"), P("developerName", "string", None, "Nome de API.", "S"),
 P("enablements", "OauthTokenExchHandlerApp[]", None, "Em quais apps e como o handler executa.", estrutura="OauthTokenExchHandlerApp"),
 P("isAccessTokenSupported", "boolean", None, "Aceita tokens de acesso (opacos ou JWT).", "S"),
 P("isContactCreationAllowed", "boolean", None, "Uso interno.", **INT),
 P("isEnabled", "boolean", None, "Se o handler está ativo (a habilitação também exige enablements).", "S"),
 P("isIdTokenSupported", "boolean", None, "Aceita ID tokens OpenID Connect.", "S"), P("isJwtSupported", "boolean", None, "Aceita tokens JWT.", "S"),
 P("isProtected", "boolean", None, "Se orgs assinantes podem referenciar o handler num pacote gerenciado."),
 P("isRefreshTokenSupported", "boolean", None, "Aceita refresh tokens.", "S"), P("isSaml2Supported", "boolean", None, "Aceita asserções SAML 2.0.", "S"),
 P("isUserCreationAllowed", "boolean", None, "Pode criar usuários que ainda não existem na Salesforce.", "S"),
 P("masterLabel", "string", None, "Rótulo.", "S"), P("tokenHandlerApex", "string", None, "Classe Apex que valida tokens e mapeia usuários (estende Oauth2TokenExchangeHandler).", "S"), FN()],
 curinga=True, divergencias=["O exemplo XML (src:mdapi-oauthtokenexchangehandler) fecha connectedApp com a etiqueta conectedApp."])
MT("OauthOidcSettings", "Configurações da org para fluxos OAuth e OpenID Connect.", "Bloquear fluxos inseguros e exigir PKCE em toda a org.", "56.0", [
 P("agentAuthLinking", "boolean", None, "Uso interno.", **INT),
 P("blockOAuthUnPwFlow", "boolean", None, "Bloqueia o fluxo usuário-senha do OAuth.", default=DF),
 P("blockOAuthUsrAgtFlow", "boolean", None, "Bloqueia o fluxo user-agent do OAuth.", default=DF),
 P("enableHdlessFgtPswFlow", "boolean", None, "Uso interno (esqueci a senha headless).", **INT),
 P("isPkceRequired", "boolean", "59.0", "Exige PKCE nas variações do fluxo de código de autorização.", default=DF),
 P("oAuthCdCrdtFlowEnable", "boolean", None, "Habilita o fluxo Authorization Code and Credentials.", default=DF)], curinga=False,
 alertas=["A página traz aviso de recurso em pré-visualização: pode mudar antes da disponibilidade geral.", "No package.xml, use o tipo Settings com o membro OauthOidc."])
M.emit_structs()

# ================================================================ referências por nome
REFS = {("metadata-types", "ExtlClntAppOauthSettings", "externalClientApplication"): "mdt:ExternalClientApplication",
        ("metadata-types", "ExtlClntAppGlobalOauthSettings", "externalClientApplication"): "mdt:ExternalClientApplication",
        ("metadata-types", "ExtlClntAppOauthConfigurablePolicies", "externalClientApplication"): "mdt:ExternalClientApplication",
        ("metadata-types", "ExtlClntAppConfigurablePolicies", "externalClientApplication"): "mdt:ExternalClientApplication",
        ("metadata-types", "OauthCustomScope", "assignedTo"): "mdt:ConnectedApp",
        ("metadata-types", "ConnectedApp", "permissionSetName"): "mdt:PermissionSet",
        ("metadata-types", "ConnectedApp", "profileName"): "mdt:Profile",
        ("estruturas", "OauthTokenExchHandlerApp", "connectedApp"): "mdt:ConnectedApp",
        ("estruturas", "OauthTokenExchHandlerApp", "externalClientApp"): "mdt:ExternalClientApplication"}
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
for t, s in [("ExtlClntAppOauthSettings", "configurações OAuth do desenvolvedor"), ("ExtlClntAppGlobalOauthSettings", "configurações OAuth globais (chaves e fluxos)"),
             ("ExtlClntAppOauthConfigurablePolicies", "políticas OAuth do administrador"), ("ExtlClntAppConfigurablePolicies", "chaves dos plugins")]:
    rel(f"{t.lower()}-eca", "mdt:" + t, "externalClientApplication", "mdt:ExternalClientApplication", f"O componente guarda as {s} de um external client app.", f"src:mdapi-{t.lower()}")
rel("oauthcustomscope-connectedapp", "mdt:OauthCustomScope", "assignedTo", "mdt:ConnectedApp", "O escopo customizado é atribuído a um connected app.", "src:mdapi-oauthcustomscope")
rel("connectedapp-permissionset", "mdt:ConnectedApp", "permissionSetName", "mdt:PermissionSet", "O app pode exigir permission sets para ser usado (com isAdminApproved).", "src:mdapi-connectedapp")
rel("connectedapp-profile", "mdt:ConnectedApp", "profileName", "mdt:Profile", "O app pode exigir perfis para ser usado (com isAdminApproved).", "src:mdapi-connectedapp")
rel("tokenexch-connectedapp", "mdx:OauthTokenExchHandlerApp", "connectedApp", "mdt:ConnectedApp", "O handler de troca de token é habilitado para um connected app.", "src:mdapi-oauthtokenexchangehandler")
rel("tokenexch-eca", "mdx:OauthTokenExchHandlerApp", "externalClientApp", "mdt:ExternalClientApplication", "O handler de troca de token é habilitado para um external client app.", "src:mdapi-oauthtokenexchangehandler")

# ================================================================ funcionalidades
INTc, ACS = "integracao-apis-e-eventos", "acesso-identidade-e-seguranca"
NAO_INV_OBJ = {"tipo": "objeto_api", "estado": "desconhecido", "motivo": "Objetos API do tema não investigados no lote 5b; a lista vazia não comprova inexistência."}
def F(fid, nome, tec, aliases, oq, fin, ex, principal, secundarias, mdts, srcs, alertas=None, limit=None, recs=None):
    cp, sp = principal
    f = {"id": "func:" + fid, "nome": nome, "nome_tecnico": tec, "aliases": aliases,
         "termos_busca": sorted(set([nome.lower(), tec.lower()] + [a.lower() for a in aliases])), "o_que_e": oq, "finalidade": fin, "exemplo": ex,
         "classificacao_principal": {"classificacao": "cls:" + cp, "subclassificacao": "sub:" + sp},
         "classificacoes_secundarias": [{"classificacao": "cls:" + c, "subclassificacao": "sub:" + s, "motivo": m} for c, s, m in secundarias],
         "representacoes": {"metadata_types": [{"ref": "mdt:" + r, "papel": p} for r, p in mdts], "objetos_api": [], "ausencias": [NAO_INV_OBJ]},
         "setup": SETUP_NV, "recomendacoes": recs or [], "alertas": alertas or [], "limitacoes": limit or [], "estado": "verificado", "evidencias": [ev(s) for s in srcs]}
    sv(f"funcionalidades/{fid}.json", f)
    for s in [sp] + [x[1] for x in secundarias]:
        d = ld(f"subclassificacoes/{s}.json"); d["funcionalidades"] = sorted(set(d["funcionalidades"]) | {"func:" + fid}); sv(f"subclassificacoes/{s}.json", d)

F("connected-apps", "Connected apps", "Connected Apps", ["connected app", "app conectado", "oauth app", "consumer key"],
  "Registro de um app ou sistema externo que se conecta à org por OAuth, SAML ou canvas, com suas políticas de acesso.",
  "Autorizar integrações e definir quem pode usá-las e por quanto tempo.",
  "Um sistema de BI se conecta por OAuth com a consumer key de um connected app que só usuários com um permission set podem usar.",
  (INTc, "autenticacao-de-integracoes"), [(ACS, "autenticacao-sso-e-mfa", "Também configura login único por SAML para apps de terceiros.")],
  [("ConnectedApp", "Definição do app."), ("ConnectedAppSettings", "Configurações da org (acesso à API só por apps aprovados).")],
  ["src:mdapi-connectedapp", "src:mdapi-connectedappsettings"],
  alertas=["Criação de connected apps restrita a partir do Spring '26 (página oficial); para novas integrações, a Salesforce recomenda external client apps."],
  limit=["A estrutura do elemento mobileAppConfig (ConnectedAppMobileDetailConfig) não tem tabela de campos na página; aparece só no exemplo XML e não foi catalogada."],
  recs=[{"texto": "Para integrações novas, prefira external client apps.", "natureza": "orientacao_oficial"}])
F("external-client-apps", "External client apps", "External Client Apps", ["external client app", "eca", "app cliente externo"],
  "Sucessor dos connected apps: o app é um componente e as configurações OAuth, políticas e plugins ficam em componentes separados.",
  "Registrar integrações com configuração separada entre desenvolvedor (empacotável) e administrador (por org).",
  "O app 'Portal Parceiros' tem as configurações OAuth no pacote; cada org define as próprias políticas e chaves.",
  (INTc, "autenticacao-de-integracoes"), [],
  [("ExternalClientApplication", "Definição do app."), ("ExtlClntAppOauthSettings", "Configurações OAuth do desenvolvedor."),
   ("ExtlClntAppGlobalOauthSettings", "Chaves, callback e fluxos habilitados."), ("ExtlClntAppOauthConfigurablePolicies", "Políticas OAuth do administrador."),
   ("ExtlClntAppConfigurablePolicies", "Chaves dos plugins."), ("ExternalClientAppSettings", "Configurações da org.")],
  ["src:mdapi-externalclientapplication", "src:mdapi-extlclntappoauthsettings", "src:mdapi-extlclntappglobaloauthsettings",
   "src:mdapi-extlclntappoauthconfigurablepolicies", "src:mdapi-extlclntappconfigurablepolicies", "src:mdapi-externalclientappsettings"],
  alertas=["Exige a permissão Opt in to External Client Apps."],
  limit=["Plugins mobile, push, canvas, notificação, attest, SAML e ExtlClntAppOauthSecuritySettings ficam para o lote 5c."])
F("oauth-escopos-e-troca-de-token", "OAuth: escopos customizados, troca de token e fluxos", "OAuth Custom Scopes and Token Exchange",
  ["oauth", "openid connect", "oidc", "custom scope", "escopo customizado", "token exchange", "troca de token", "pkce"],
  "Recursos de OAuth da org: escopos customizados para apps, handlers Apex de troca de token e configurações que bloqueiam fluxos ou exigem PKCE.",
  "Refinar permissões de integrações e aceitar tokens de provedores externos com segurança.",
  "Um app recebe o escopo customizado 'pedidos_leitura'; um handler troca o token do provedor corporativo por um token da Salesforce.",
  (INTc, "autenticacao-de-integracoes"), [(ACS, "autenticacao-sso-e-mfa", "Políticas de fluxos OAuth e PKCE afetam a autenticação na org.")],
  [("OauthCustomScope", "Escopo customizado."), ("OauthTokenExchangeHandler", "Handler Apex de troca de token."), ("OauthOidcSettings", "Configurações de fluxos OAuth e OIDC.")],
  ["src:mdapi-oauthcustomscope", "src:mdapi-oauthtokenexchangehandler", "src:mdapi-oauthoidcsettings"],
  limit=["Agrupamento didático do projeto: os três tipos não formam uma funcionalidade única na documentação."])

core = ld("nuvens/platform-core.json")
for c in core["classificacoes_aplicaveis"]:
    if c["classificacao"] == "cls:" + INTc:
        for s in c["subclassificacoes"]:
            if s["subclassificacao"] == "sub:autenticacao-de-integracoes":
                s["funcionalidades"] = sorted(set(s["funcionalidades"]) | {"func:connected-apps", "func:external-client-apps", "func:oauth-escopos-e-troca-de-token"})
sv("nuvens/platform-core.json", core)
print("ok lote 5b")
