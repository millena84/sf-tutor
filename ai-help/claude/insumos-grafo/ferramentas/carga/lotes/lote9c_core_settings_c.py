"""Lote 9c (#10, etapa 3, lote C; 2026-11-23): cadastro dos 5 tipos Settings maiores já incluídos no Core e ainda sem ficha.

SecuritySettings (com 5 subtipos), SharingSettings, OrgSettings, UserManagementSettings e MobileSettings (com 3 subtipos removidos ou
obsoletos), lidos nas páginas versionadas 264.0. A página de SecuritySettings tem cerca de 140 mil caracteres e foi lida em duas partes
(offset 0 e 100000). Estrutura e explicação na mesma passada. Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import af                     # noqa: E402
from carga import catalogo as C               # noqa: E402
from carga import mdt as M                    # noqa: E402
from carga.mdt import mdt, P, struct, emit_structs   # noqa: E402

DATA = "2026-11-23"
EXTR = "fontes/extracoes/lote9c-core-settings-c.txt"
G = "https://developer.salesforce.com/docs/get_document_content/api_meta/"


def S(nome):
    # src:mdapi-sharingsettings já existe (página não versionada, lida em 2026-11-10); a leitura 264.0 ganha id próprio.
    return "src:mdapi-" + nome.lower() + ("-264" if nome == "SharingSettings" else "")


TIPOS = ["SecuritySettings", "SharingSettings", "OrgSettings", "UserManagementSettings", "MobileSettings"]
C.registrar_fontes([C.fonte(S(n), f"{n} (Metadata API 264.0)", G + f"meta_{n.lower()}.htm/en-us/264.0",
                            f"Descrição, arquivo, versão, tabela Fields e subtipos do tipo {n} (página lida por inteiro).", EXTR, DATA, versao="264.0")
                    for n in TIPOS])

FALSE = ("false", False, "A página declara default false.")
TRUE = ("valor", "true", "A página declara default true.")


def VAL(v, nota=None):
    return ("valor", v, nota or "Default declarado na página.")


def COND(nota):
    return ("valor", None, nota)


PKG = "No package.xml, use o tipo Settings com o nome-base do arquivo como membro; o curinga só vale para recuperar todas as configurações."
FN = M.FULLNAME_HERDADO(None)
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
ENUM_SEM_VALORES = dict(natureza="enum_fechado", contexto="Enumeração; a leitura não trouxe a lista completa de valores.")
INTERNO = "Reservado para uso interno, segundo a página."


def xml(nome, corpo):
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<{nome} {NS}>\n{corpo}\n</{nome}>'


# ======================================================================= SecuritySettings
struct("IpRange", S("SecuritySettings"), ["mdt:SecuritySettings"], [
    P("description", "string", "34.0", "Descrição da faixa de IP confiável, para identificá-la (por exemplo, qual rede da empresa ela representa)."),
    P("end", "string", None, "Último endereço IP da faixa confiável."),
    P("start", "string", None, "Primeiro endereço IP da faixa confiável."),
], o_que_e="Uma faixa de endereços IP confiáveis.")
struct("NetworkAccess", S("SecuritySettings"), ["mdt:SecuritySettings"], [
    P("ipRanges", "IpRange[]", None, "Faixas de IP confiáveis, das quais o usuário entra sem ativar o computador. Para acrescentar uma faixa é "
      "preciso implantar todas as existentes junto com a nova, senão as existentes são substituídas; para remover todas, deixe o elemento vazio.",
      estrutura="IpRange"),
], o_que_e="As faixas de IP confiáveis da org (Network Access).")
struct("PasswordPolicies", S("SecuritySettings"), ["mdt:SecuritySettings"], [
    P("apiOnlyUserHomePageURL", "string", None, "URL para onde vão os usuários com a permissão API Only, em vez da página de login."),
    P("complexity", "Complexity", None, "Tipos de caractere exigidos na senha.", default=VAL("AlphaNumeric"), vals=[
        ("NoRestriction", "sem exigência (menos seguro)"), ("AlphaNumeric", "ao menos uma letra e um número"),
        ("SpecialCharacters", "letra, número e caractere especial"),
        ("UpperLowerCaseNumeric", "número, maiúscula e minúscula (API 31.0+)"),
        ("UpperLowerCaseNumericSpecialCharacters", "número, maiúscula, minúscula e caractere especial (API 31.0+)"),
        ("Any3UpperLowerCaseNumericSpecialCharacters", "três entre número, maiúscula, minúscula e caractere especial (API 46.0+)")]),
    P("enableSetPasswordInApi", "boolean", None, "Obsoleto e sem efeito nas versões atuais.", ate="51.0",
      notas=["A página diz que foi descontinuado na API 51.0 e removido na 52.0."]),
    P("expiration", "Expiration", None, "Prazo até a senha expirar e precisar ser trocada.", default=VAL("NinetyDays"), vals=[
        ("Never", "nunca"), ("ThirtyDays", "30 dias"), ("SixtyDays", "60 dias"), ("NinetyDays", "90 dias"), ("SixMonths", "seis meses"),
        ("OneYear", "um ano")]),
    P("historyRestriction", "string", None, "Quantas senhas anteriores ficam guardadas para impedir que o usuário as repita. De 0 a 24 (16 antes da "
      "API 31.0).", default=VAL("3"), restr="0 a 24."),
    P("lockoutInterval", "LockoutInterval", None, "Por quanto tempo o login fica bloqueado depois de tentativas erradas.", default=VAL("FifteenMinutes"),
      vals=[("FifteenMinutes", "15 minutos"), ("ThirtyMinutes", "30 minutos"), ("SixtyMinutes", "60 minutos"),
            ("Forever", "até um administrador desbloquear")]),
    P("maxLoginAttempts", "MaxLoginAttempts", None, "Quantas tentativas erradas de login são aceitas antes do bloqueio.", default=VAL("TenAttempts"),
      vals=[("NoLimit", "sem limite"), ("ThreeAttempts", "3"), ("FiveAttempts", "5"), ("TenAttempts", "10")]),
    P("minimumPasswordLength", "string", "35.0", "Tamanho mínimo da senha, de 5 a 50 caracteres. Antes da API 35.0 usava-se a enumeração "
      "minPasswordLength.", default=VAL("8"), restr="5 a 50."),
    P("minimumPasswordLifetime", "boolean", "31.0", "Com true, a senha só pode ser trocada uma vez a cada 24 horas.", default=FALSE),
    P("obscureSecretAnswer", "boolean", None, "Esconde a resposta da pergunta de segurança enquanto o usuário digita. Pode atrapalhar o IME japonês "
      "(Hiragana); se os usuários não conseguirem digitar, desligue.", default=FALSE),
    P("passwordAssistanceMessage", "string", None, "Texto mostrado no e-mail de bloqueio de conta e no fim da tela Confirm Identity, usada para "
      "redefinir a senha."),
    P("passwordAssistanceURL", "string", None, "URL aonde os usuários vão para recuperar a senha esquecida."),
    P("questionRestriction", "QuestionRestriction", None, "Se a resposta da pergunta de dica de senha pode conter a própria senha.",
      default=VAL("DoesNotContainPassword"), vals=[("None", "sem restrição"), ("DoesNotContainPassword", "não pode conter a senha")]),
], o_que_e="Regras de senha e de bloqueio de login da org.")

SESSAO = [
    P("allowUserAuthenticationByCertificate", "boolean", "47.0", "Permite autenticar usuários com certificado digital X.509 (PEM).", default=FALSE),
    P("allowUserCertBasedAuthenticationWithOcspValidation", "boolean", None, "Valida por OCSP ou CRL os certificados usados na autenticação."),
    P("auraBoxcarReductionPref", "boolean", None, "Com true, desliga a otimização dinâmica de boxcar do Aura, que junta várias ações numa requisição.",
      default=FALSE),
    P("canConfirmEmailChangeInLightningCommunities", "boolean", "47.0", "Exige confirmar a troca de e-mail por um link enviado ao endereço novo.",
      default=COND("false em orgs antigas; true nas novas, segundo a página.")),
    P("canConfirmIdentityBySmsOnly", "boolean", "48.0", "Impede verificar a identidade por e-mail quando o usuário tem outro método, como SMS ou "
      "Authenticator.", default=COND("false em orgs antigas; true nas novas, segundo a página.")),
    P("disableTimeoutWarning", "boolean", None, "Com true, desliga o aviso de que a sessão vai expirar."),
    P("enableBuiltInAuthenticator", "boolean", None, "Permite verificar a identidade com o autenticador do próprio dispositivo, como Touch ID ou "
      "Windows Hello.", default=FALSE),
    P("enableCSPOnEmail", "boolean", None, "Aplica política de segurança de conteúdo (CSP) aos modelos de e-mail."),
    P("enableCSRFOnGet", "boolean", None, "Protege contra CSRF as requisições GET de páginas fora do Setup."),
    P("enableCSRFOnPost", "boolean", None, "Protege contra CSRF as requisições POST de páginas fora do Setup."),
    P("enableCacheAndAutocomplete", "boolean", None, "Deixa o navegador guardar o nome de usuário e preencher o campo de login."),
    P("enableClickjackNonsetupSFDC", "boolean", None, "Protege contra clickjacking as páginas da Salesforce fora do Setup."),
    P("enableClickjackNonsetupUser", "boolean", None, "Protege contra clickjacking as páginas Visualforce customizadas com cabeçalho padrão."),
    P("enableClickjackNonsetupUserHeaderless", "boolean", "34.0", "Protege contra clickjacking as páginas Visualforce customizadas sem cabeçalho padrão."),
    P("enableClickjackSetup", "boolean", None, "Protege contra clickjacking as páginas do Setup."),
    P("enableContentSniffingProtection", "boolean", "39.0", "Impede o navegador de adivinhar o tipo MIME e executar arquivos maliciosos como conteúdo "
      "dinâmico.", notas=["Sempre true a partir da API 58.0, segundo a página."]),
    P("enableLightningLogin", "boolean", "47.0", "Permite login sem senha com Lightning Login (Salesforce Authenticator)."),
    P("enableLightningLoginOnlyWithUserPerm", "boolean", "47.0", "Restringe o Lightning Login aos usuários com a permissão específica."),
    P("enableMFADirectUILoginOptIn", "boolean", None, "Exige um segundo fator nos logins diretos na interface com usuário e senha; a permissão de "
      "isenção prevalece."),
    P("enableOauthCorsPolicy", "boolean", "50.0", "Liga CORS nos endpoints OAuth de token, revogação e introspecção.", default=FALSE),
    P("enablePostForSessions", "boolean", "31.0", "Troca as informações de sessão entre domínios por POST em vez de GET, o que é mais seguro."),
    P("enableSMSIdentity", "boolean", None, "Permite receber por SMS um código de uso único para verificar a identidade; exige celular verificado.",
      default=TRUE),
    P("enableU2F", "boolean", "47.0", "Permite usar chave de segurança física compatível com U2F para MFA e verificação de identidade.", default=FALSE),
    P("enableUpgradeInsecureRequests", "boolean", "42.0", "Exige HTTPS nas conexões com domínios de terceiros.", ate="60.0",
      default=COND("true em contas criadas depois do Summer '17, segundo a página.")),
    P("enableXssProtection", "boolean", "39.0", "Ligava o cabeçalho X-XSS-Protection contra XSS refletido; o cabeçalho está obsoleto.", ate="59.0"),
    P("enforceIpRangesEveryRequest", "boolean", "34.0", "Aplica as faixas de Login IP Ranges a cada requisição, não só no login."),
    P("enforceUserDeviceRevoked", "boolean", "50.0", "Impede que um dispositivo revogado entre pelos apps Salesforce; navegadores não são afetados."),
    P("forceLogoutOnSessionTimeout", "boolean", "31.0", "Quando a sessão expira, encerra a sessão e leva o usuário à tela de login.", default=TRUE),
    P("forceRelogin", "boolean", None, "Com true, o administrador que entrou como outro usuário precisa fazer login de novo para voltar à própria sessão."),
    P("hasRetainedLoginHints", "boolean", None, "Mantém os nomes de usuário em cache até o logout, mesmo depois de a sessão expirar.", default=FALSE),
    P("hasUserSwitching", "boolean", None, "Permite trocar de org pelo Switcher; exige o cache de login ligado.", default=TRUE),
    P("hstsOnForcecomSites", "boolean", "41.0", "Exige HTTPS em Visualforce, sites Salesforce e sites do Experience Cloud."),
    P("identityConfirmationOnEmailChange", "boolean", "42.0", "Confirma a identidade ao trocar o e-mail, em vez de exigir novo login."),
    P("identityConfirmationOnTwoFactorRegistrationEnabled", "boolean", "40.0", "Exige confirmar a identidade ao cadastrar um método de MFA, em vez "
      "de novo login."),
    P("lockSessionsToDomain", "boolean", "33.0", "Prende a sessão da interface a um domínio, o que dificulta o uso indevido do ID de sessão.",
      default=COND("true em orgs criadas desde o Spring '15, segundo a página.")),
    P("lockSessionsToIp", "boolean", None, "Prende a sessão ao endereço IP de onde o usuário entrou."),
    P("lockerServiceAPIVersion", "string", "47.0", "Versão de API que o Lightning Locker aplica aos componentes customizados, de 46.0 até a atual.",
      default=COND("A versão da release atual, segundo a página.")),
    P("lockerServiceCSP", "boolean", None, "Liga uma CSP mais rígida, que bloqueia unsafe-inline em script-src, exigida pelo Locker e pelo Lightning "
      "Web Security."),
    P("lockerServiceNext", "boolean", "53.0", "Usa Lightning Web Security nos componentes web; o Locker continua protegendo os componentes Aura."),
    P("lockerServiceNextControl", "boolean", None, INTERNO),
    P("lockerTrustedMode", "boolean", None, INTERNO),
    P("lockerTrustedResources", "string", None, INTERNO),
    P("logoutURL", "string", "34.0", "URL para onde o usuário vai ao sair do Salesforce.",
      default=COND("A URL de login do My Domain da org, segundo a página.")),
    P("redirectBlockModeEnabled", "boolean", "56.0", "Bloqueia o acesso a URLs externas não confiáveis em campos de URL e de texto longo. Não pode "
      "ser usado junto com redirectionWarning.", default=FALSE),
    P("redirectionWarning", "boolean", "42.0", "No Classic, avisa antes de redirecionar para uma URL externa não confiável. Não pode ser usado junto "
      "com redirectBlockModeEnabled.", default=COND("true em orgs criadas desde o Spring '18; false nas anteriores, segundo a página.")),
    P("referrerPolicy", "boolean", "42.0", "Faz as páginas enviarem o cabeçalho referrer-policy com a diretiva de referrerPolicyDirective.", default=TRUE),
    P("referrerPolicyDirective", "ReferrerPolicy", "58.0", "Diretiva usada no cabeçalho Referrer-Policy das páginas; sem efeito com referrerPolicy "
      "em false. Algumas opções estão obsoletas.", default=VAL("strict-origin-when-cross-origin"), **ENUM_SEM_VALORES),
    P("requireHttpOnly", "boolean", "40.0", "Aplica o atributo HttpOnly aos cookies de sessão, que deixam de ser lidos por JavaScript; apps que leem "
      "esses cookies param de funcionar."),
    P("requireHttps", "boolean", "40.0", "Exige HTTPS para entrar no Salesforce; não pode ser desligado (voltar a HTTP depende do Suporte).",
      ate="60.0", default=TRUE),
    P("securityCentralKillSession", "boolean", "36.0", "Descontinuado.", ate="50.0", notas=["A página diz que o campo foi removido na API 51.0."]),
    P("sessionTimeout", "SessionTimeout", None, "Tempo de inatividade depois do qual o usuário é avisado para sair ou continuar, de FifteenMinutes a "
      "TwentyFourHours (este valor desde a API 38.0).", **ENUM_SEM_VALORES),
    P("sidToken3rdPartyAuraApp", "boolean", "59.0", "Em contexto de terceiros (como Lightning Out), troca o cookie de autenticação por um token de sessão."),
    P("skipSFAWhenMFADirectUILogin", "boolean", None, "Define a primeira tela de cadastro de MFA: lista completa de métodos (true) ou só o Salesforce "
      "Authenticator (false)."),
    P("terminateUserSessionsWhenAdminResetsPassword", "boolean", None, "Encerra todas as sessões de interface do usuário quando um administrador "
      "redefine a senha dele."),
    P("unescapedHtmlSanitization", "boolean", "67.0", "Permite desligar a sanitização de HTML do componente aura:unescapedHtml."),
    P("untrustedRedirect", "untrustedRedirect", "64.0", "O que acontece ao clicar em links não confiáveis no Lightning Experience.",
      vals=[("AlwaysAllowed", "sempre permitido"), ("NeverAllowed", "nunca permitido"), ("WithUserPermission", "com permissão do usuário")],
      notas=["Recurso piloto/beta, segundo a página."]),
    P("useLocalStorageForLogoutUrl", "boolean", "52.0", "Leva abas com sessão expirada para a URL de logout personalizada, usando o armazenamento local "
      "do navegador.", default=COND("true em orgs novas; false nas anteriores ao Summer '21, segundo a página.")),
    P("vfInlineScriptInjection", "VfInlineScriptInjection", "67.0", "Reservado para uso futuro, segundo a página.", default=VAL("allow"),
      **ENUM_SEM_VALORES),
    P("welcomeEmailTemplateId", "string", "63.0", "ID do modelo de e-mail de boas-vindas para usuários internos novos; só aceita modelos Classic.",
      natureza="referencia", contexto="ID de um modelo de e-mail Classic da org."),
]
struct("SessionSettings", S("SecuritySettings"), ["mdt:SecuritySettings"], SESSAO,
       o_que_e="Regras de sessão: expiração, proteções do navegador (clickjacking, CSRF, CSP), verificação de identidade e Lightning Locker.")
struct("SingleSignOnSettings", S("SecuritySettings"), ["mdt:SecuritySettings"], [
    P("enableCaseInsensitiveFederationID", "boolean", "47.0", "Faz o Federation ID dos usuários ignorar maiúsculas e minúsculas.", default=FALSE),
    P("enableForceDelegatedCallout", "boolean", "47.0", "Chama o endpoint de SSO mesmo quando há falha de restrição de login na org.", default=FALSE),
    P("enableMultipleSamlConfigs", "boolean", "47.0", "Permite configurar vários provedores SAML. Depois de ligado, não pode ser desligado.",
      default=TRUE),
    P("enableSamlJitProvisioning", "boolean", "47.0", "Permite criar usuários a partir da asserção SAML (just-in-time). Exige enableSamlLogin em true "
      "e enableMultipleSamlConfigs em false.", default=FALSE),
    P("enableSamlLogin", "boolean", "47.0", "Permite SSO por SAML a partir de provedores externos.", default=FALSE),
    P("isLoginWithSalesforceCredentialsDisabled", "boolean", "47.0", "Manda os usuários autenticar em provedores de identidade de terceiros, em vez de "
      "usar as credenciais da Salesforce.", default=FALSE),
], o_que_e="Opções de single sign-on (SSO) da org.")

ENUM_PP = [("Always", "sempre"), ("Never", "nunca"), ("TrustedUrls", "só URLs confiáveis")]
mdt("SecuritySettings", S("SecuritySettings"),
    "Configurações de segurança da org: faixas de IP confiáveis, regras de senha e login, sessão, cabeçalhos de segurança e SSO.",
    "Recuperar e implantar a política de segurança da org, em vez de repetir à mão as telas de Network Access, Password Policies e Session Settings.",
    "27.0", [
        P("canUsersGrantLoginAccess", "boolean", None, "Define se os usuários podem dar acesso de login ao Suporte; se não, só administradores."),
        P("enableAdminLoginAsAnyUser", "boolean", None, "Permite que administradores entrem como qualquer usuário.", default=FALSE),
        P("enableAuditFieldsInactiveOwner", "boolean", "47.0", "Liga a edição de campos de auditoria e a troca de dono para usuários inativos.",
          default=FALSE),
        P("enableAuraSecureEvalPref", "boolean", "47.0", "Impede funções dinâmicas em componentes Aura criados em tempo de execução.", default=FALSE),
        P("enableCoepHeader", "boolean", "55.0", "Aplica o cabeçalho COEP às páginas Visualforce customizadas.", default=FALSE),
        P("enableCoopHeader", "boolean", "55.0", "Aplica o cabeçalho COOP às páginas Visualforce customizadas.", default=FALSE),
        P("enableCrossOrgRedirects", "boolean", "59.0", "Permitia redirecionar usuários para outras orgs; sempre false desde o Summer '24.", ate="60.0"),
        P("enableGraphQLApiGuestUserAccess", "boolean", "68.0", "Permite que usuários guest, sem autenticação, usem a GraphQL API.", default=FALSE),
        P("enablePermissionsPolicy", "boolean", "59.0", "Inclui o cabeçalho Permissions-Policy, que controla recursos do navegador.", default=FALSE),
        P("enableRequireHttpsConnection", "boolean", None, "Obsoleto: tratava da exigência de HTTPS.",
          notas=["A página diz que o campo está obsoleto na API 47.0 e posteriores."]),
        P("grantCameraAccess", "PermissionsPolicy", "59.0", "Quando apps e sites podem usar a câmera.", vals=ENUM_PP),
        P("grantMicrophoneAccess", "PermissionsPolicy", "59.0", "Quando apps e sites podem usar o microfone.", vals=ENUM_PP),
        P("isTLSv12Required", "boolean", None, "Exigia TLS 1.2 ou superior nas conexões.", default=FALSE, ate="50.0",
          notas=["Removido na API 51.0."]),
        P("isTLSv12RequiredCommunities", "boolean", None, "Exigia TLS 1.2 ou superior em sites, portais e Experience Cloud.", default=FALSE, ate="50.0",
          notas=["Removido na API 51.0."]),
        P("networkAccess", "NetworkAccess", None, "Faixas de IP confiáveis, das quais o usuário entra sem ativar o computador.", estrutura="NetworkAccess"),
        P("passwordPolicies", "PasswordPolicies", None, "Regras de senha e de login e ajuda para recuperar senhas.", estrutura="PasswordPolicies"),
        P("sendCspForUncommonClients", "boolean", "59.0", "Inclui ou omite a diretiva frame-ancestors para clientes que não a suportam claramente.",
          default=FALSE),
        P("sessionSettings", "SessionSettings", None, "Regras de expiração e de segurança da sessão.", estrutura="SessionSettings"),
        P("singleSignOnSettings", "SingleSignOnSettings", None, "Opções de single sign-on.", estrutura="SingleSignOnSettings"),
        FN,
    ], arquivos_prontos=M.arquivos_settings("SecuritySettings", "Security", S("SecuritySettings")), curinga=False,
    alertas=[PKG, "Ao implantar networkAccess, mande todas as faixas de IP: as que não forem enviadas são substituídas.",
             "Algumas opções não têm volta, como enableMultipleSamlConfigs depois de ligado."],
    cobertura_nota=f"Universo esperado = tabela Fields da página 264.0 (19 campos, mais fullName herdado), lida em {DATA} em duas partes "
                   "(offset 0 e 100000); subtipos NetworkAccess (1), IpRange (3), PasswordPolicies (13), SessionSettings (59) e SingleSignOnSettings (6).",
    exemplo=xml("SecuritySettings", "    <passwordPolicies>\n        <complexity>AlphaNumeric</complexity>\n        <expiration>NinetyDays</expiration>\n"
                "        <minimumPasswordLength>12</minimumPasswordLength>\n    </passwordPolicies>\n    <sessionSettings>\n"
                "        <forceLogoutOnSessionTimeout>true</forceLogoutOnSessionTimeout>\n    </sessionSettings>"))

# ======================================================================= SharingSettings
SUP = "A página diz que o recurso não vem ligado e exige contato com o Suporte da Salesforce."
mdt("SharingSettings", S("SharingSettings"),
    "Configurações de compartilhamento, visibilidade e acesso a dados da org.",
    "Recuperar e implantar opções gerais de compartilhamento, como visibilidade entre usuários externos e cálculos adiados.", None, [
        P("deferGroupMembership", "boolean", "49.0", "Suspende os cálculos de associação a grupos. Ao voltar para false, os grupos e as regras de "
          "compartilhamento são recalculados (as regras só se deferSharingRules não estiver true), o que pode demorar. Com true, deferSharingRules "
          "não pode ser alterado.", default=FALSE, notas=[SUP]),
        P("deferSharingRules", "boolean", "49.0", "Suspende os cálculos de regras de compartilhamento. Ao voltar para false, as regras são recalculadas, "
          "o que pode demorar. Não pode ser alterado com deferGroupMembership em true.", default=FALSE, notas=[SUP]),
        P("enableAccountRoleOptimization", "boolean", None, "Atribui papéis de pessoa a usuários novos de sites em contas sem usuários (true) em vez "
          "de criar papéis comuns de site (false).", default=FALSE),
        P("enableAssetSharing", "boolean", None, "Liga o compartilhamento próprio de ativos; com false, o acesso segue o registro pai.", default=FALSE),
        P("enableCommunityUserVisibility", "boolean", None, "Deixa usuários do mesmo site se verem, independentemente dos padrões da org. Em orgs "
          "criadas na API 47.0 ou depois, não vale para usuários guest.", default=FALSE),
        P("enableExternalSharingModel", "boolean", None, "Liga o modelo de compartilhamento externo (padrões separados para usuários externos). "
          "Exige Customize Application.", default=COND("true se Salesforce Experiences estiver ligado; false se não, segundo a página.")),
        P("enableKeepManualSharesOnTransfer", "boolean", "68.0", "Mantém (true) ou remove (false) os compartilhamentos manuais quando o registro "
          "passa a outro dono."),
        P("enableManagerGroups", "boolean", None, "Permite compartilhar registros com o grupo de gerentes e com o de gerentes e subordinados. Exige "
          "View e Manage Users.", default=FALSE),
        P("enableManualUserRecordSharing", "boolean", None, "Permite que o usuário compartilhe o próprio registro de usuário.", default=FALSE),
        P("enablePartnerSuperUserAccess", "boolean", None, "Permite dar acesso de super usuário a parceiros em sites. Exige Customize Application.",
          default=FALSE),
        P("enablePortalUserCaseSharing", "boolean", None, "Permite que usuários de portal acessem contatos ligados aos casos que possuem.", default=FALSE),
        P("enablePortalUserVisibility", "boolean", None, "Deixa usuários de portal da mesma conta de cliente ou parceiro se verem, independentemente "
          "dos padrões da org.", default=FALSE, notas=["Para ligar, a página manda contatar o Suporte."]),
        P("enableRemoveTMGroupMembership", "boolean", None, "Remove as associações a grupos do recurso antigo de territórios depois da migração para "
          "Sales Territories. Depois de true, não pode voltar a false.", default=FALSE),
        P("enableRestrictAccessLookupRecords", "boolean", "48.0", "Exige acesso de leitura ao registro para ver o nome dele em campos de lookup e de "
          "sistema.", default=COND("true em orgs criadas no Spring '20 ou depois; false nas demais, segundo a página.")),
        P("enableSecureGuestAccess", "boolean", "47.0", "Com true, usuários guest têm padrões da org Private e só recebem registros por regras de "
          "compartilhamento para guest.", notas=["A partir da API 50.0 o valor é sempre true (retroativo à 47.0); mudá-lo não tem efeito."]),
        P("enableStandardReportVisibility", "boolean", None, "Permite ver relatórios de tipos padrão que podem expor dados de usuários a que a pessoa "
          "não tem acesso.", default=FALSE),
        P("enableTerritoryForecastManager", "boolean", None, "Permite que gerentes de previsão administrem por delegação os territórios abaixo deles.",
          default=FALSE),
        FN,
    ], arquivos_prontos=M.arquivos_settings("SharingSettings", "Sharing", S("SharingSettings")), curinga=False,
    alertas=[PKG, "Acesso: exige a permissão Manage Sharing.",
             "Voltar os cálculos adiados para false dispara recálculos que podem levar muito tempo."],
    divergencias=["A seção Version da página (src:mdapi-sharingsettings) não traz número de versão. O catálogo não registra versão inicial."],
    cobertura_nota=f"Universo esperado = tabela Fields da página 264.0 (17 campos, mais fullName herdado), lida em {DATA}.",
    exemplo=xml("SharingSettings", "    <enableManagerGroups>true</enableManagerGroups>\n    <enableStandardReportVisibility>false</enableStandardReportVisibility>"))

# ======================================================================= OrgSettings
mdt("OrgSettings", S("OrgSettings"),
    "Configurações da org inteira que não pertencem a um recurso específico.",
    "Recuperar e implantar opções gerais, como o Customer Portal e a análise de sentimento no feed.", "46.0", [
        P("enableCustomerSuccessPortal", "boolean", None, "Indica se o Customer Portal está ligado."),
        P("enableManageSelfServiceUsers", "boolean", None, "Indica se a gestão em massa de usuários do Self-Service Portal está ligada."),
        P("enableOrgFeedSentimentAnalysis", "boolean", None, "Indica se a análise de sentimento no feed está ligada na org."),
        FN,
    ], arquivos_prontos=M.arquivos_settings("OrgSettings", None, S("OrgSettings")), curinga=False,
    alertas=[PKG, "Até a API 50.0, enableExtendedMailMerge e saveMailMergeDocsAsSalesforceDocs ficavam aqui; desde a 51.0 estão em MailMergeSettings."],
    divergencias=["O exemplo XML da página (src:mdapi-orgsettings) traz enableMakeDeploymentsMandatory e enableRADeploymentAttributeOnly, que não "
                  "estão na tabela Fields. O catálogo segue a tabela e não cadastra esses dois sem descrição."],
    cobertura_nota=f"Universo esperado = tabela Fields da página 264.0 (3 campos, mais fullName herdado), lida em {DATA}. O nome-base do arquivo "
                   "não foi confirmado (o exemplo de package.xml usa o membro Org).",
    exemplo=xml("OrgSettings", "    <enableOrgFeedSentimentAnalysis>false</enableOrgFeedSentimentAnalysis>"))

# ======================================================================= UserManagementSettings
mdt("UserManagementSettings", S("UserManagementSettings"),
    "Opções de gestão de usuários da página User Management Settings.",
    "Recuperar e implantar as interfaces aprimoradas de usuários, perfis e permissões e as proteções de dados pessoais dos usuários.", "46.0", [
        P("enableConcealPersonalInfo", "boolean", None, "Esconde de usuários externos 10 campos de informação pessoal do registro de usuário. Não "
          "existe em orgs criadas no Winter '22 ou depois; a Salesforce recomenda enableEnhancedConcealPersonalInfo, que exige este em false.",
          default=FALSE),
        P("enableContactlessExternalIdentityUsers", "boolean", "47.0", "Com a licença External Identity (Customer 360 Identity), permite criar "
          "usuários sem contato, o que simplifica a gestão de clientes.", default=FALSE),
        P("enableEnhancedConcealPersonalInfo", "boolean", "53.0", "Esconde de usuários externos os campos de informação pessoal que você escolher. "
          "Exige enableConcealPersonalInfo em false.", default=FALSE),
        P("enableEnhancedPermsetMgmt", "boolean", None, "Liga a visualização aprimorada dos componentes de permission sets, com paginação, filtros e "
          "ordenação.", default=FALSE),
        P("enableEnhancedProfileMgmt", "boolean", None, "Liga a visualização aprimorada de listas de perfis, para ver e editar rapidamente.",
          default=FALSE),
        P("enableEnhcUiUserAccessPolicies", "boolean", "60.0", "Cria e gerencia as políticas de acesso de usuários por uma interface aprimorada. "
          "Sem efeito se as políticas não estiverem ligadas; se estiverem, vira true sozinho, mas pode voltar a false.", default=FALSE),
        P("enableNewProfileUI", "boolean", None, "Liga a interface aprimorada de perfis; só uma interface vale por vez.", default=FALSE),
        P("enableProfileFiltering", "boolean", "50.0", "Mostra o nome dos perfis só a quem precisa deles; com false, todos veem todos os perfis. "
          "Alguns pontos do Setup ainda expõem nomes de perfis (abas, record types, login flows, administração delegada)."),
        P("enableRestrictEmailDomains", "boolean", "53.0", "Mostra (true) ou esconde (false) no Setup a lista de domínios de e-mail permitidos.",
          default=FALSE),
        P("enableScrambleUserData", "boolean", "47.0", "Permite que usuários peçam a remoção dos dados pessoais. A Salesforce não apaga: embaralha os "
          "dados, sem volta, quando o administrador usa o método Apex obfuscateUser."),
        P("enableUserSelfDeactivate", "boolean", None, "Permite que usuários desativem a própria conta do site do Experience Cloud ou do Chatter."),
        P("enhancedPermSetList", "boolean", "63.0", "Gerencia permission sets pela interface atualizada da página de Permissões.", default=FALSE),
        P("enhancedUserListView", "boolean", "62.0", "Gerencia usuários pela interface atualizada da página de Usuários no Setup.", default=FALSE),
        P("enhancedUserRoleListView", "boolean", "63.0", "Gerencia papéis pela interface atualizada da página de Papéis no Setup.", default=FALSE),
        P("groupSummaryUIEnhancement", "boolean", "62.0", "Adiciona e remove membros de grupos públicos pela página de resumo aprimorada; a página "
          "de detalhes continua funcionando.", default=TRUE),
        P("permsetsInFieldCreation", "boolean", "56.0", "Ao criar um campo ou mudar sua segurança ou tipo, atribui a segurança de campo a permission "
          "sets em vez de perfis.", default=FALSE),
        P("psaExpirationUIEnabled", "boolean", "52.0", "Liga a interface com data de expiração para atribuições de permission sets e grupos de "
          "permission sets.", default=FALSE),
        P("restrictedProfileCloning", "boolean", "50.0", "Ao clonar perfis, liga só as permissões a que a org tem acesso; com false, copia todas as "
          "permissões ativas do perfil de origem."),
        P("userAccessPoliciesEnabled", "boolean", "58.0", "Liga as políticas de acesso de usuários, que automatizam atribuições de licenças de pacote, "
          "permission sets e outros acessos por critérios.", default=FALSE),
        P("userFieldHistoryTracking", "boolean", "64.0", "Liga o histórico de alterações dos campos de usuário.", default=FALSE),
        FN,
    ], arquivos_prontos=M.arquivos_settings("UserManagementSettings", "UserManagement", S("UserManagementSettings")), curinga=False,
    alertas=[PKG, "enableScrambleUserData leva a um embaralhamento irreversível dos dados pessoais."],
    cobertura_nota=f"Universo esperado = tabela Fields da página 264.0 (20 campos, mais fullName herdado), lida em {DATA}.",
    exemplo=xml("UserManagementSettings", "    <enableEnhancedPermsetMgmt>true</enableEnhancedPermsetMgmt>\n    <permsetsInFieldCreation>true</permsetsInFieldCreation>"))

# ======================================================================= MobileSettings
REM46 = dict(ate="45.0", notas=["Removido na API 46.0."])
struct("ChatterMobileSettings", S("MobileSettings"), ["mdt:MobileSettings"], [
    P("IPadAuthorized", "boolean", None, "Indicava se o iPad podia usar o Chatter Mobile.", **REM46),
    P("IPhoneAuthorized", "boolean", None, "Indicava se o iPhone podia usar o Chatter Mobile.", **REM46),
    P("androidAuthorized", "boolean", None, "Indicava se dispositivos Android podiam usar o Chatter Mobile.", **REM46),
    P("blackBerryAuthorized", "boolean", None, "Indicava se dispositivos BlackBerry podiam usar o Chatter Mobile.", **REM46),
    P("enableChatterMobile", "boolean", None, "Indicava se o Chatter Mobile estava ligado; com true, as demais opções podiam ser definidas.", **REM46),
    P("enablePushNotifications", "boolean", None, "Indicava se as notificações push do Chatter estavam ligadas.", **REM46),
    P("sessionTimeout", "MobileSessionTimeout", None, "Tempo de inatividade depois do qual o usuário era convidado a sair ou continuar.", vals=[
        ("Never", "nunca"), ("OneMinute", "1 minuto"), ("FiveMinutes", "5 minutos"), ("TenMinutes", "10 minutos"),
        ("ThirtyMinutes", "30 minutos")], **REM46),
], o_que_e="Opções do antigo Chatter Mobile (removidas na API 46.0).")
struct("DashboardMobileSettings", S("MobileSettings"), ["mdt:MobileSettings"], [
    P("enableDashboardIPadApp", "boolean", None, "Indicava se o app Mobile Dashboards para iPad estava ligado.", notas=["Obsoleto, segundo a página."]),
], o_que_e="Opção do antigo app Mobile Dashboards (obsoleto).")
struct("TouchMobileSettings", S("MobileSettings"), ["mdt:MobileSettings"], [
    P("enableTouchBrowserIPad", "boolean", None, "Indicava se o Salesforce Touch pelo navegador estava ligado.", **REM46),
    P("enableTouchAppIPad", "boolean", None, "Indicava se o app baixável Salesforce Touch estava ligado.", **REM46),
], o_que_e="Opções do antigo Salesforce Touch (removidas na API 46.0).")
mdt("MobileSettings", S("MobileSettings"),
    "Configurações móveis da org: o que o app Salesforce mobile permite, como acesso offline e cache seguro.",
    "Recuperar e implantar as opções do app Salesforce mobile entre ambientes.", "27.0", [
        P("chatterMobile", "ChatterMobileSettings", None, "Opções do antigo Chatter Mobile.", estrutura="ChatterMobileSettings", **REM46),
        P("dashboardMobile", "DashboardMobileSettings", None, "Opções do antigo app Mobile Dashboards.", estrutura="DashboardMobileSettings",
          notas=["Obsoleto, segundo a página."]),
        P("enableImportContactFromDevice", "boolean", "47.0", "Permite importar contatos do dispositivo móvel."),
        P("enableLightningOnMobile", "boolean", "47.0", "Indicava se a org estava liberada para o app Salesforce mobile.", ate="47.0",
          notas=["Só na API 47.0; removido na 48.0."]),
        P("enableNewSalesforceMobileAppForTablet", "boolean", None, "Indicava se a org usava a experiência de tablet do app Salesforce mobile.",
          ate="55.0", notas=["Removido na API 56.0."]),
        P("enableNewSalesforceMobileAppForTabletWideScreen", "boolean", "52.0", "Indicava se a org usava a experiência de tablet widescreen do app.",
          ate="55.0", notas=["Removido na API 56.0."]),
        P("enableOfflineDraftsEnabled", "boolean", "47.0", "Permite criar, editar e excluir registros offline no app. Não fica disponível com "
          "enableS1OfflinePref em false.", default=TRUE),
        P("enablePopulateNameManuallyInToday", "boolean", "47.0", "Mostra o nome do usuário na página Today do app.", default=FALSE),
        P("enableS1EncryptedStoragePref2", "boolean", "47.0", "Faz o Salesforce mobile web usar cache seguro e persistente do navegador para ganhar "
          "desempenho.", default=TRUE),
        P("enableS1OfflinePref", "boolean", "47.0", "Permite acessar registros offline no app. Fica true na primeira instalação do app baixável; exige "
          "Salesforce para Android ou iOS 10.0 ou superior e não existe no mobile web."),
        P("touchMobile", "TouchMobileSettings", None, "Opções do antigo Salesforce Touch.", estrutura="TouchMobileSettings", **REM46),
        FN,
    ], arquivos_prontos=M.arquivos_settings("MobileSettings", "Mobile", S("MobileSettings")), curinga=False, alertas=[PKG],
    cobertura_nota=f"Universo esperado = tabela Fields da página 264.0 (11 campos, mais fullName herdado), lida em {DATA}; subtipos "
                   "ChatterMobileSettings (7), DashboardMobileSettings (1) e TouchMobileSettings (2), todos removidos ou obsoletos.",
    exemplo=xml("MobileSettings", "    <enableS1OfflinePref>true</enableS1OfflinePref>\n    <enableOfflineDraftsEnabled>true</enableOfflineDraftsEnabled>"))

emit_structs()

# ======================================================================= Classificação funcional
for fid, n, papel in [
    ("regras-de-compartilhamento", "SharingSettings", "Opções gerais de compartilhamento: visibilidade de usuários externos, cálculos adiados e acesso a lookups."),
]:
    C.ampliar_funcionalidade(fid, mdts=[(n, papel)], srcs=[S(n)])

SEM_OBJ = [{"tipo": "objeto_api", "estado": "desconhecido",
            "motivo": "Objetos API ligados a esta funcionalidade não foram investigados neste lote; a lista vazia não comprova inexistência."}]
SETUP_DESC = af("desconhecido", None, "Caminho no Setup não validado nesta sessão.")
C.funcionalidade(
    "politicas-de-seguranca-da-org", "Políticas de segurança da org", "Security Settings",
    ["políticas de senha", "configurações de sessão", "Network Access"],
    "As regras de segurança da org inteira: faixas de IP confiáveis, regras de senha e bloqueio, expiração e proteção da sessão e SSO.",
    "Definir como os usuários entram e quanto tempo ficam conectados, e proteger as páginas contra ataques comuns do navegador.",
    "A empresa exige senha de 12 caracteres que expira a cada 90 dias e encerra a sessão depois de 2 horas sem uso.",
    ("acesso-identidade-e-seguranca", "sessoes-e-politicas-de-login"),
    [("acesso-identidade-e-seguranca", "autenticacao-sso-e-mfa", "SecuritySettings também guarda as opções de SSO e de verificação de identidade.")],
    [("SecuritySettings", "Faixas de IP, senha, sessão, cabeçalhos de segurança e SSO.")], [], [S("SecuritySettings")], SEM_OBJ, SETUP_DESC)
C.funcionalidade(
    "opcoes-gerais-da-org", "Opções gerais da org", "Org Settings", ["Customer Portal", "Self-Service Portal"],
    "Opções da org inteira que não pertencem a um recurso específico, como o Customer Portal e a análise de sentimento no feed.",
    "Ligar ou desligar recursos gerais herdados, que não têm tela própria de configuração.",
    "Uma org antiga confere se o Customer Portal ainda está ligado antes de migrar para o Experience Cloud.",
    ("organizacao-e-configuracoes-base", "settings"), [],
    [("OrgSettings", "Customer Portal, Self-Service Portal e análise de sentimento no feed.")], [], [S("OrgSettings")], SEM_OBJ, SETUP_DESC)
C.funcionalidade(
    "app-salesforce-mobile", "App Salesforce mobile", "Salesforce Mobile App", ["Salesforce mobile", "acesso offline"],
    "O app Salesforce para celular e tablet, com acesso offline e cache seguro.",
    "Usar a org no celular, inclusive sem conexão.",
    "Um técnico abre os registros offline no app durante uma visita sem sinal e sincroniza ao voltar.",
    ("interface-e-experiencia-do-usuario", "experiencias-web-portais-e-mobile"), [],
    [("MobileSettings", "Opções do app Salesforce mobile, como offline e cache seguro.")], [], [S("MobileSettings")], SEM_OBJ, SETUP_DESC)

C.funcionalidade(
    "gestao-de-usuarios-e-permissoes", "Opções de gestão de usuários", "User Management Settings",
    ["User Management Settings", "interfaces aprimoradas de perfis e permissões"],
    "As opções da página User Management Settings: interfaces aprimoradas de usuários, perfis, papéis e permission sets, políticas de acesso "
    "e proteção dos dados pessoais dos usuários.",
    "Escolher como administradores gerenciam usuários e acessos e quanto dos dados pessoais dos usuários fica visível para externos.",
    "A administradora liga a atribuição de segurança de campo por permission set ao criar campos, em vez de por perfil.",
    ("acesso-identidade-e-seguranca", "usuarios-e-provisionamento"),
    [("acesso-identidade-e-seguranca", "permissoes-perfis-e-grupos", "Boa parte das opções muda a gestão de perfis e permission sets.")],
    [("UserManagementSettings", "Opções de gestão de usuários, perfis, permissões e dados pessoais.")], [], [S("UserManagementSettings")],
    SEM_OBJ, SETUP_DESC)

print("lote 9c: 5 Settings cadastrados")
