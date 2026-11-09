# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5g (issue #24): certificados restantes, InboundNetworkConnection e plugins de external client app.
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
NOMES = ["PublicKeyCertificate", "PublicKeyCertificateSet", "UserAuthCertificate", "InboundCertificate", "InboundNetworkConnection",
         "ExtlClntAppMobileSettings", "ExtlClntAppMobileConfigurablePolicies", "ExtlClntAppPushSettings", "ExtlClntAppPushConfigurablePolicies",
         "ExtlClntAppCanvasSettings", "ExtlClntAppNotificationSettings", "ExtlClntAppSamlConfigurablePolicies"]
novas = [{"id": f"src:mdapi-{n.lower()}", "titulo": f"{n} (Metadata API)", "url": B + f"meta_{n.lower()}.htm", "tipo": "oficial_documentacao", "versao": "68.0",
          "data_verificacao": DATA, "metodo": "extracao_documental_assistida", "pertinencia": f"Arquivo, versão e propriedades do tipo {n}.",
          "extracao": "fontes/extracoes/mdapi-lote5g.txt", "checagem_online": CHK} for n in NOMES]
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

def P(n, t, ver=None, d=None, req="N", **kw): return (n, t, req, ver, d, kw)
DF = ("valor", "false", None)
FN = lambda: M.FULLNAME_HERDADO(None)
def V(*vals): return [(v, None) for v in vals]
SETUP_NV = af("desconhecido", None, "Caminho no Setup não verificado nesta sessão.")
def MT(nome, o, f, desde, rows, **kw):
    return M.mdt(nome, f"src:mdapi-{nome.lower()}", o, f, desde, rows, setup=SETUP_NV, **kw)
ECA = lambda: P("externalClientApplication", "string", None, "Nome do external client app associado.", "S")
LBL = lambda d="Rótulo da configuração.": P("label", "string", None, d)
BETA = "Serviço piloto ou beta, sujeito aos termos de serviços beta (página oficial)."
OAUTH = "Exige o plugin OAuth de external client apps."

# ------------------------------------------------ estruturas
M.struct("PublicKeyCertificateSetKey", "src:mdapi-publickeycertificateset", ["mdt:PublicKeyCertificateSet"],
 [P("publicKeyCertificate", "string", None, "PublicKeyCertificate referenciado.", "S")], "Uma chave do conjunto.")
M.struct("InboundNetworkConnProperty", "src:mdapi-inboundnetworkconnection", ["mdt:InboundNetworkConnection"], [
 P("propertyName", "string", None, "Qual configuração o par representa.", "S", vals=[("AwsVpcEndpointId", "só leitura com status Ready"), ("Region", None), ("SourceIpRanges", None)]),
 P("propertyValue", "string", None, "Valor; para SourceIpRanges, JSON com IP inicial e final de cada faixa.", "S")], "Par nome-valor de configuração da conexão de entrada.")
S = "src:mdapi-extlclntapppushsettings"
M.struct("ExtlClntAppAndroidPushConfig", S, ["mdt:ExtlClntAppPushSettings"], [
 P("fcmProject", "string", None, "Id do projeto Google Firebase do app.", "S"),
 P("serviceAccount", "string", None, "Chave privada do Admin SDK da conta de serviço do Firebase, em base64 (até 8.000 caracteres).", "S")], "Configuração de push para Android.")
M.struct("ExtlClntAppApplePushConfig", S, ["mdt:ExtlClntAppPushSettings"], [
 P("applicationBundle", "string", None, "Bundle ID do app iOS (App Store Connect)."),
 P("certificate", "string", None, "Certificado TLS com APNs, em base64 (caminho .p12).", "C:obrigatório no caminho .p12"),
 P("environment", "string", None, "Ambiente do APNs.", "S", vals=V("Production", "Sandbox")),
 P("keyIdentifier", "string", None, "Identificador da signingKey (caminho .p8).", "C:obrigatório no caminho .p8"),
 P("password", "string", None, "Senha do certificado (caminho .p12).", "C:obrigatório no caminho .p12"),
 P("signingKey", "string", None, "Chave privada do APNs em base64 (caminho .p8).", "C:obrigatório no caminho .p8"),
 P("teamIdentifier", "string", None, "Id do time Apple Developer (caminho .p8).", "C:obrigatório no caminho .p8")], "Configuração de push para iOS (chave .p8 ou certificado .p12).")
M.struct("ExtlClntAppNotificationType", "src:mdapi-extlclntappnotificationsettings", ["mdt:ExtlClntAppNotificationSettings"], [
 P("notificationType", "string", None, "Nome API do tipo de notificação (só tipos customizados com canal mobile).", "S"),
 P("pushByDefault", "boolean", None, "Se o tipo é enviado como push no celular; exige ExtlClntAppPushSettings.", "S")], "Tipo de notificação assinado pelo app.")
M.struct("ExtlClntAppSamlConfigurablePoliciesAttribute", "src:mdapi-extlclntappsamlconfigurablepolicies", ["mdt:ExtlClntAppSamlConfigurablePolicies"], [
 P("formula", "string", None, "Referência ao dado do usuário, na forma $Objeto.Campo (ex.: $Organization.Country).", "S"),
 P("key", "string", None, "Nome único do atributo na resposta SAML.", "S")], "Atributo extra enviado na resposta SAML.")

# ------------------------------------------------ certificados e rede
MT("PublicKeyCertificate", "Certificado público ou JSON web key (JWK) guardado na org.", "Validar JWTs emitidos por sistemas do cliente.", "62.0", [
 P("description", "string", None, "Descrição."), P("isActive", "boolean", None, "Se o certificado está ativo.", default=DF),
 P("jsonWebKey", "string", None, "Chave pública usada para verificar tokens."), P("masterLabel", "string", None, "Rótulo.", "S"), FN()], curinga=True,
 divergencias=["O exemplo de jsonWebKey (src:mdapi-publickeycertificate) traz parâmetros de chave privada e de curva elíptica junto com kty RSA; os valores são ilustrativos."])
MT("PublicKeyCertificateSet", "Conjunto de chaves públicas (certificados ou JWKs), informadas uma a uma ou buscadas de um endpoint JWKS.",
   "Validar JWTs de um emissor que publica ou rotaciona várias chaves.", "62.0", [
 P("description", "string", None, "Descrição."), P("jwksEndPoint", "string", None, "URL HTTPS que devolve o JWKS.", "C:usado quando type é JWKS_URL"),
 P("jwtIssuer", "string", None, "Emissor do JWT (diferencia maiúsculas)."), P("masterLabel", "string", None, "Rótulo.", "S"),
 P("publicKeyCertificateSetKeys", "PublicKeyCertificateSetKey[]", None, "Chaves do conjunto.", "C:usado quando type é JWKS", estrutura="PublicKeyCertificateSetKey"),
 P("type", "string", None, "Como as chaves são obtidas (formato JWK).", "S", vals=[("JWKS", "chaves em PublicKeyCertificateSetKey"), ("JWKS_URL", "chaves no jwksEndPoint")]), FN()], curinga=True,
 divergencias=["A seção do subtipo se chama PublicKeyCertificateSetKeys (plural), mas o tipo é PublicKeyCertificateSetKey (src:mdapi-publickeycertificateset).",
               "A obrigatoriedade de jwksEndPoint e de publicKeyCertificateSetKeys conforme o type é implícita na descrição dos valores, não marcada na tabela."])
MT("UserAuthCertificate", "Certificado de usuário em PEM, enviado de fora e associado a um usuário.", "Autenticar o usuário por certificado.", "50.0", [
 P("developerName", "string", None, "Nome do certificado, com sublinhados entre as palavras.", "S", notas=["Só quem tem View DeveloperName ou View Setup and Configuration vê, agrupa, ordena e filtra este campo."]),
 P("expirationDate", "dateTime", None, "Quando o certificado expira.", "S"), P("masterLabel", "string", None, "Nome amigável (até 64 caracteres).", "S"),
 P("serialNumber", "string", None, "Número de série.", "S"), P("user", "string", None, "Usuário do certificado (a tabela diz nome).", "S"), FN()], curinga=True,
 divergencias=["O exemplo (src:mdapi-userauthcertificate) traz um elemento content que não está na tabela, e o valor de user tem formato de Id, não de nome."])
MT("InboundCertificate", "Certificado de autenticação mútua (mTLS) importado para a org.", "Fazer cliente e servidor provarem a identidade um ao outro.", "49.0", [
 P("expirationDate", "date", None, "Quando o certificado expira.", "S"), P("issuer", "string", None, "Emissor.", "S"),
 P("masterLabel", "string", None, "Nome amigável (até 64 caracteres).", "S"), P("serialId", "string", None, "Número de série.", "S")],
 estende="não declarado na página", alertas=["Disponível só com a permissão MutualAuthentication habilitada na org.", "A página não informa o tipo pai; fullName não foi catalogado."])
MT("InboundNetworkConnection", "Conexão privada de entrada (AWS PrivateLink): chamadas de um serviço de terceiros para a org.",
   "Receber chamadas de serviços na AWS sem passar pela internet pública.", "49.0", [
 P("connectionType", "string", None, "Provedor da conexão.", "S", vals=[("AwsPrivateLink", None), ("DataCloudPrivateConnection", "uso interno")]),
 P("description", "string", None, "Descrição (até 255 caracteres).", "S"),
 P("inboundNetworkConnProperties", "InboundNetworkConnProperty[]", None, "Configurações em pares nome-valor.", estrutura="InboundNetworkConnProperty"),
 P("isActive", "boolean", None, "Se a conexão está ligada.", "S", default=DF), P("label", "string", None, "Nome exibido.", "S"),
 P("status", "string", None, "Estado atual; muda sozinho depois das ações Provision, Sync ou Teardown.", "S",
   vals=V("Unprovisioned", "Allocating", "PendingAcceptance", "PendingActivation", "RejectedRemotely", "DeletedRemotely", "TeardownInProgress", "Ready"),
   default=("valor", "Unprovisioned", "Estado inicial.")), FN()], curinga=True,
 divergencias=["Esta página lista o status Allocating; a de OutboundNetworkConnection (src:mdapi-outboundnetworkconnection) lista Allocation."])

# ------------------------------------------------ plugins de external client app
MT("ExtlClntAppMobileSettings", "Configurações de app móvel de um external client app, como o bloqueio de tela.", "Ligar recursos do app móvel do external client app.", "64.0", [
 ECA(), P("isScreenLockEnabled", "boolean", None, "Se o app bloqueia a tela depois de um tempo (definido nas políticas móveis).", "S"), LBL(), FN()],
 alertas=[BETA], divergencias=["isScreenLockEnabled fala de um tempo limite que não está nesta tabela; ele fica em ExtlClntAppMobileConfigurablePolicies.screenLockTimeout."])
MT("ExtlClntAppMobileConfigurablePolicies", "Políticas móveis de um external client app.", "Definir quando o app móvel bloqueia e pede nova autenticação.", "64.0", [
 ECA(), LBL(), P("screenLockTimeout", "string", None, "Tempo até o app bloquear; vale só com isScreenLockEnabled em ExtlClntAppMobileSettings.",
                 vals=[("Never", None), ("One", "1 min"), ("Five", "5 min"), ("Ten", "10 min"), ("Thirty", "30 min"), ("Sixty", "60 min"),
                       ("OneTwenty", "120 min"), ("OneEighty", "180 min"), ("TwoForty", "240 min")]), FN()])
MT("ExtlClntAppPushSettings", "Configuração de notificações push (Apple ou Android) de um external client app.", "Enviar push para o app móvel.", "64.0", [
 P("androidPushConfig", "ExtlClntAppAndroidPushConfig", None, "Configuração para Android.", "C:um entre androidPushConfig, applePushConfig e pushConfigLink", estrutura="ExtlClntAppAndroidPushConfig"),
 P("applePushConfig", "ExtlClntAppApplePushConfig", None, "Configuração para iOS.", "C:um entre androidPushConfig, applePushConfig e pushConfigLink", estrutura="ExtlClntAppApplePushConfig"),
 ECA(), LBL(), P("pushConfigLink", "string", None, "Aponta uma configuração existente (orgId:recordId); gerado ao criar com configuração embutida.", "C:um entre androidPushConfig, applePushConfig e pushConfigLink"),
 P("pushServiceType", "string", None, "Sistema do celular.", "S", vals=V("Apple", "Android")), FN()],
 alertas=[BETA, OAUTH, "Use exatamente um entre androidPushConfig, applePushConfig e pushConfigLink.",
          "Ao instalar o app em outra org, remova as configurações embutidas e mantenha só pushConfigLink.",
          "serviceAccount, signingKey, certificate e password recebem chaves privadas e senhas."],
 recs=[{"texto": "Não versione valores reais de chaves e senhas de push no repositório; fora da org de origem, use pushConfigLink.", "natureza": "inferencia_tecnica"}])
MT("ExtlClntAppPushConfigurablePolicies", "Políticas de notificação push de um external client app.", "Decidir quanto conteúdo aparece na notificação.", "64.0", [
 ECA(), P("isFullContent", "boolean", None, "true: título e corpo completos; false: mensagem genérica (padrão) ou só o título (customizada).", "S"), LBL(), FN()],
 alertas=[BETA, OAUTH])
MT("ExtlClntAppCanvasSettings", "Configurações de app canvas de um external client app: um app de terceiros exibido dentro da Salesforce.",
   "Exibir um app externo em páginas, feed, ações, Visualforce ou componentes Lightning.", "66.0", [
 P("accessMethod", "string", None, "Como o canvas inicia o OAuth.", "S", vals=[("Get", "usuário autoriza; o app inicia o fluxo"), ("Post", "admin autoriza na instalação; autenticação postada na URL")]),
 P("canvasLocationOptions", "string[]", None, "Onde o canvas pode aparecer.", vals=V("Aura", "ChatterFeed", "MobileNav", "None", "PageLayout", "Publisher", "Visualforce")),
 P("canvasOptions", "string[]", None, "Esconde elementos do publisher.", vals=V("HideShare", "HideHeader")),
 P("canvasUrl", "string", None, "URL do app de terceiros.", "S"), ECA(), LBL("Nome do app."),
 P("lifeCycleHandler", "string", None, "Nome da classe Apex de ciclo de vida."),
 P("samlInitiationMethod", "string", None, "Quem inicia o SSO SAML, se usado.", vals=V("IdpInitiated", "SpInitiated", "None")), FN()], curinga=True)
MT("ExtlClntAppNotificationSettings", "Assinaturas de notificação para mobile de um external client app.", "Escolher quais tipos de notificação customizada o app recebe.", "64.0", [
 ECA(), LBL(), P("notificationTypes", "ExtlClntAppNotificationType[]", None, "Tipos assinados; só eles chegam pela API ou como push.", estrutura="ExtlClntAppNotificationType"), FN()],
 alertas=[BETA, OAUTH])
MT("ExtlClntAppSamlConfigurablePolicies", "Políticas SAML de um external client app: a Salesforce atua como provedor de identidade para um provedor de serviço.",
   "Usuários entram em um serviço de terceiros com a conta Salesforce.", "63.0", [
 P("acsUrl", "string", None, "Endpoint ACS do provedor de serviço, que recebe as respostas SAML.", "S"),
 P("certificate", "string", None, "Certificado do provedor de serviço para assinar requisições (fluxo iniciado por ele); se definido, toda requisição precisa vir assinada."),
 P("commaSeparatedPermissionSet", "string", None, "Ids de permission sets exigidos para o SSO, separados por vírgula."),
 P("commaSeparatedProfile", "string", None, "Ids de perfis exigidos para o SSO, separados por vírgula (a página recomenda permission sets)."),
 P("customAttributes", "ExtlClntAppSamlConfigurablePoliciesAttribute[]", None, "Dados extras do usuário na resposta SAML.", estrutura="ExtlClntAppSamlConfigurablePoliciesAttribute"),
 P("encryptionCertificate", "string", None, "Certificado X.509 (Certificate and Key Management) que cifra as asserções."),
 P("encryptionType", "string", None, "Método de cifragem das asserções.", vals=V("AES_128", "AES_256")),
 P("entityUrl", "string", None, "Entity ID único do provedor de serviço.", "S"),
 P("externalClientApplication", "string", None, "Rótulo do external client app pai.", "S"),
 P("issuer", "string", None, "URI usada como emissor das respostas (pode ser a URL de um site Experience Cloud).", default=("valor", "My Domain", "Quando omitido.")),
 LBL(), P("nameIdFormat", "string", None, "Formato do NameID; precisa casar com o provedor de serviço.", vals=V("Unspecified", "EmailAddress", "Persistent", "Transient"), default=("valor", "Unspecified", None)),
 P("signingAlgorithmType", "string", None, "Algoritmo de assinatura das mensagens SAML e de logout.", vals=V("SHA1", "SHA256")),
 P("singleLogoutBindingType", "string", None, "Binding HTTP do logout único.", vals=V("PostBinding", "RedirectBinding")),
 P("singleLogoutUrl", "string", None, "Endpoint de logout único do provedor de serviço."),
 P("startUrl", "string", None, "Página após a autenticação.", notas=["Obsoleto a partir da 64.0; use startUrl em ExtlClntAppConfigurablePolicies."]),
 P("subjectCustomAttribute", "string", None, "Campo do usuário usado como identidade.", "C:obrigatório quando subjectType é CustomAttribute"),
 P("subjectType", "string", None, "Tipo de identificador do usuário no SSO.", vals=V("Username", "FederationId", "UserId", "CustomAttribute", "PersistentId")), FN()], curinga=True,
 alertas=["O app pai precisa de distributionState Local (apps com SAML não podem ser empacotados) e de ExtlClntAppConfigurablePolicies com isSamlPluginEnabled true.",
          "Exige permissões para ver external client apps, ver as configurações e editar as políticas."],
 divergencias=["O exemplo XML (src:mdapi-extlclntappsamlconfigurablepolicies) tem marcadores inválidos nas URLs e certificados truncados; não é implantável como está.",
               "externalClientApplication é descrito como o rótulo do app pai, enquanto os outros plugins usam o nome."])
M.emit_structs()

# ------------------------------------------------ referências por nome
NOME = " A referência é pelo nome do componente, no XML (não é um lookup entre registros)."
def ref(pasta, arq, prop, alvo, nota="Referência pelo nome do componente no XML."):
    d = ld(f"{pasta}/{arq}.json")
    for p in d["propriedades"]:
        if p["nome"] == prop: p["referencia"] = {"alvos": [alvo], "nota": nota}
    sv(f"{pasta}/{arq}.json", d)
def rel(rid, o, campo, d, expl, s, sufixo=NOME):
    sv(f"relacionamentos/{rid}.json", {"id": "rel:" + rid, "tipo": "referencia_campo", "origem": {"entidade": o, "campo": campo}, "destino": {"entidade": d},
       "explicacao": expl + sufixo, "estado": "verificado", "evidencias": [ev(s)]})
ref("estruturas", "PublicKeyCertificateSetKey", "publicKeyCertificate", "mdt:PublicKeyCertificate")
rel("pkcsetkey-pkc", "mdx:PublicKeyCertificateSetKey", "publicKeyCertificate", "mdt:PublicKeyCertificate",
    "Cada chave do conjunto aponta um certificado público.", "src:mdapi-publickeycertificateset")
PLUG = {"ExtlClntAppMobileSettings": "configurações móveis", "ExtlClntAppMobileConfigurablePolicies": "políticas móveis", "ExtlClntAppPushSettings": "configuração de push",
        "ExtlClntAppPushConfigurablePolicies": "políticas de push", "ExtlClntAppCanvasSettings": "configuração de canvas", "ExtlClntAppNotificationSettings": "assinaturas de notificação"}
for n, d in PLUG.items():
    ref("metadata-types", n, "externalClientApplication", "mdt:ExternalClientApplication")
    rel(f"{n.lower()}-eca", "mdt:" + n, "externalClientApplication", "mdt:ExternalClientApplication", f"O componente guarda as {d} de um external client app.", f"src:mdapi-{n.lower()}")
ref("metadata-types", "ExtlClntAppSamlConfigurablePolicies", "externalClientApplication", "mdt:ExternalClientApplication", "Referência pelo rótulo do app pai, segundo a página.")
rel("extlclntappsamlconfigurablepolicies-eca", "mdt:ExtlClntAppSamlConfigurablePolicies", "externalClientApplication", "mdt:ExternalClientApplication",
    "O componente guarda as políticas SAML de um external client app.", "src:mdapi-extlclntappsamlconfigurablepolicies",
    " A página diz que o valor é o rótulo do app pai (não é um lookup entre registros).")

# ------------------------------------------------ funcionalidades
def upd(fid, mdts, srcs, alertas=(), limit=None):
    f = ld(f"funcionalidades/{fid}.json"); r = f["representacoes"]["metadata_types"]
    have = {x["ref"] for x in r}
    r += [{"ref": "mdt:" + m, "papel": p} for m, p in mdts if "mdt:" + m not in have]
    f["evidencias"] += [ev(s) for s in srcs if not any(e["fonte"] == s for e in f["evidencias"])]
    f["alertas"] += [a for a in alertas if a not in f["alertas"]]
    if limit is not None: f["limitacoes"] = limit
    sv(f"funcionalidades/{fid}.json", f)
upd("certificados", [("PublicKeyCertificate", "Certificado público ou JWK para validar JWTs de clientes."), ("PublicKeyCertificateSet", "Conjunto de chaves públicas (lista ou endpoint JWKS)."),
                     ("UserAuthCertificate", "Certificado de usuário para autenticação."), ("InboundCertificate", "Certificado de autenticação mútua importado.")],
    ["src:mdapi-publickeycertificate", "src:mdapi-publickeycertificateset", "src:mdapi-userauthcertificate", "src:mdapi-inboundcertificate"],
    alertas=["InboundCertificate só existe com a permissão MutualAuthentication habilitada na org."])
upd("conexoes-de-rede-privadas", [("InboundNetworkConnection", "Conexão privada de entrada (chamadas de serviços na AWS para a org).")], ["src:mdapi-inboundnetworkconnection"])
f = ld("funcionalidades/conexoes-de-rede-privadas.json")
f["o_que_e"] = "Conexões privadas entre a org e a AWS, nos dois sentidos: de saída (usadas por named credentials do tipo PrivateEndpoint) e de entrada (chamadas de serviços na AWS para a org)."
f["finalidade"] = "Trocar chamadas com serviços na AWS sem trafegar pela internet pública."
sv("funcionalidades/conexoes-de-rede-privadas.json", f)
upd("external-client-apps", [(n, "Plugin: " + d + ".") for n, d in PLUG.items()] + [("ExtlClntAppSamlConfigurablePolicies", "Plugin: políticas SAML (Salesforce como provedor de identidade).")],
    ["src:mdapi-" + n.lower() for n in list(PLUG) + ["ExtlClntAppSamlConfigurablePolicies"]],
    alertas=["Os plugins de mobile, push e notificação são piloto ou beta, segundo as páginas oficiais."])
print("ok lote 5g")
