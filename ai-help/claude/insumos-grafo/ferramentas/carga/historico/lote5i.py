# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5i (issue #24): caminhos de Setup das funcionalidades de integração.
import json
from b1_base import ev, af
BASE = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/"
CAT = BASE + "catalogo/"
DATA = "2026-11-09"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
H = "https://help.salesforce.com/s/articleView?id="
CHK = {"estado": "verificado", "nota": f"Conteúdo lido em {DATA} e conferido quanto ao assunto (não apenas HTTP 200)."}
def S(id, t, url, pert, tipo="oficial_ajuda", ver="sem versão (Ajuda Salesforce)"):
    return {"id": id, "titulo": t, "url": url, "tipo": tipo, "versao": ver, "data_verificacao": DATA, "metodo": "leitura_resultado_busca",
            "pertinencia": pert, "extracao": "fontes/extracoes/help-setup-integracao.txt", "checagem_online": CHK}
DEV = dict(tipo="oficial_documentacao", ver="sem versão na página")
FONTES = [
 S("src:help-nc-create", "Create or Edit a Named Credential", H + "sf.nc_create_edit_named_credential.htm&type=5", "Caminho de Setup de named credentials."),
 S("src:help-ext-cred-create", "Create or Edit an OAuth External Credential with the Browser Flow", H + "sf.nc_create_edit_oath_browser_ext_cred.htm&type=5", "Caminho de Setup de external credentials."),
 S("src:help-auth-provider-oidc", "Configure an Authentication Provider Using OpenID Connect", H + "xcloud.sso_provider_openid_connect.htm&type=5", "Caminho de Setup de auth providers."),
 S("src:help-cert-self-signed", "Generate a Self-Signed Certificate", H + "xcloud.security_keys_creating.htm&type=5", "Caminho de Setup de certificados."),
 S("src:help-saml-slo-sp", "Configure SAML Single Logout with Salesforce as the Service Provider", H + "security_auth_slo_saml_sp_configuring.htm&type=5", "Caminho de Setup das configurações de SSO SAML."),
 S("src:help-eca-create", "Create an External Client App", H + "xcloud.create_a_local_external_client_app.htm&type=5", "Caminho de criação de external client apps."),
 S("src:help-eca-jwt", "Configure an External Client App to Issue JWT-Based Access Tokens", H + "jwt_eca_configuration.htm&type=5", "Caminho do External Client App Manager."),
 S("src:help-eca-custom-scope-assign", "Assign an OAuth Custom Scope to an External Client App", H + "xcloud.remoteaccess_oauth_customscopes_assign.htm&type=5", "Caminho para atribuir escopos customizados."),
 S("src:help-connected-app-basics", "Configure Basic Connected App Settings", H + "sf.connected_app_create_basics.htm&type=5", "Caminho de criação de connected apps."),
 S("src:help-remote-site", "Configure Remote Site Settings", H + "sf.configuring_remoteproxy.htm&type=5", "Caminho de Setup de remote site settings."),
 S("src:help-cors", "Configure Salesforce CORS Allowlist", H + "sf.extend_code_cors.htm&type=5", "Caminho de Setup da allowlist de CORS."),
 S("src:help-trusted-urls", "Manage Trusted URLs", H + "sf.csp_trusted_sites.htm&type=5", "Caminho de Setup de trusted URLs (CSP)."),
 S("src:help-event-relay-create", "Create an Event Relay", H + "platform.ev_relay_create_ui.htm&type=5", "Caminho de Setup de event relays."),
 S("src:help-external-services-register", "Paste the JSON or YAML formatted Schema Into Your Browser", H + "sf.external_services_register_json.htm&type=5", "Caminho de Setup de External Services."),
 S("src:help-external-data-source-odata", "Define an External Data Source for Salesforce Connect—OData 2.0 or 4.0 Adapter", H + "sf.platform_connect_add_external_data_source.htm&type=5", "Caminho de Setup de fontes de dados externas."),
 S("src:help-platform-events-define", "Define and Manage Platform Events", H + "platform.platform_events.htm&type=5", "Caminho de Setup de eventos de plataforma."),
 S("src:pe-guide-subscribers", "View and Manage an Event's Subscribers on the Platform Event's Detail Page", "https://developer.salesforce.com/docs/platform/platform-events/guide/platform-events-get-subscribers-apex.html",
   "Onde ver e retomar assinantes de eventos.", **DEV),
 S("src:pubsub-qs-events", "Step 3: Set Up Events (Pub/Sub API quick start)", "https://developer.salesforce.com/docs/platform/pub-sub-api/guide/qs-set-up-events.html", "Onde selecionar objetos do Change Data Capture.", **DEV),
 S("src:help-bulk-jobs", "Monitor Bulk Data Load Jobs", H + "sf.monitoring_async_api_jobs.htm&type=5", "Onde acompanhar jobs da Bulk API."),
 S("src:help-snowflake-private-connect", "Define a Named Credential for Salesforce Connect SQL Adapter for Snowflake", H + "platform.snowflake_named_credentials_external_credentials.htm",
   "Caminho de Setup do Private Connect (conexão de saída)."),
 S("src:commerce-extensions-guide", "Get Started with Salesforce Commerce Extensions", "https://developer.salesforce.com/docs/commerce/salesforce-commerce/guide/extensions.html",
   "Como provedores de extensão do Commerce são registrados.", **DEV),
]
reg = json.load(open(BASE + "fontes/registro.json"))
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [f for f in FONTES if f["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

UI = "Rótulos em inglês, como na fonte; a tradução da interface em pt-BR não foi verificada."
def setup(fid, valor, nota, srcs, estado="verificado"):
    f = ld(f"funcionalidades/{fid}.json")
    f["setup"] = af(estado, valor, (nota + " " + UI).strip() if valor else nota, [ev(s) for s in srcs])
    f["evidencias"] += [ev(s) for s in srcs if not any(e["fonte"] == s for e in f["evidencias"])]
    sv(f"funcionalidades/{fid}.json", f)

setup("named-credentials", "Setup > Quick Find: Named Credentials > Named Credentials > New; credenciais externas: Named Credentials > External Credentials > New",
      "Criação. New Legacy cria a named credential antiga.", ["src:help-nc-create", "src:help-ext-cred-create"])
setup("auth-providers", "Setup > Quick Find: Auth. Providers > New", "Criação.", ["src:help-auth-provider-oidc"])
setup("certificados", "Setup > Quick Find: Certificate and Key Management > Create Self-Signed Certificate", "Criação de certificado autoassinado; a org aceita até 50 certificados.",
      ["src:help-cert-self-signed"])
setup("sso-saml", "Setup > Quick Find: Single Sign-On Settings > SAML Single Sign-On Settings > New", "Criação de uma configuração SAML.", ["src:help-saml-slo-sp"])
setup("external-client-apps", "Criar: Setup > Quick Find: App Manager > New External Client App; gerenciar: Setup > Quick Find: External Client Apps > External Client App Manager",
      "As páginas usam os dois pontos de entrada.", ["src:help-eca-create", "src:help-eca-jwt"])
setup("connected-apps", "Setup > Quick Find: External Client Apps > External Client App Settings > New Connected App",
      "A criação de connected apps está restrita desde o Spring '26.", ["src:help-connected-app-basics"])
setup("oauth-escopos-e-troca-de-token", "Atribuir escopo customizado: Setup > Quick Find: External Client Apps Manager > (app) > Policies > OAuth Policies",
      "Só a atribuição foi verificada; os caminhos para criar o escopo e o handler de troca de token não foram lidos.", ["src:help-eca-custom-scope-assign"])
setup("remote-site-settings", "Setup > Quick Find: Remote Site Settings > New Remote Site", "Criação.", ["src:help-remote-site"])
setup("cors", "Setup > Quick Find: CORS > New", "Adicionar uma origem à allowlist.", ["src:help-cors"])
setup("csp-trusted-sites", "Setup > Quick Find: Trusted URLs > New Trusted URL",
      "Na interface, a tela se chama Trusted URLs; o metadata type continua CspTrustedSite.", ["src:help-trusted-urls"])
setup("event-relay", "Setup > Quick Find: Event Relays > New Event Relay", "Assistente: rótulo, named credential, canal e opção de recuperação de erro; o relay nasce parado.",
      ["src:help-event-relay-create"])
setup("external-services", "Setup > Quick Find: External Services > New External Service", "Registro de um serviço a partir da especificação.", ["src:help-external-services-register"])
setup("external-objects", "Setup > Quick Find: External Data Sources > New External Data Source", "Primeiro passo: a fonte de dados externa (OData 2.0 ou 4.0).",
      ["src:help-external-data-source-odata"])
setup("platform-events", "Setup > Quick Find: Platform Events > New Platform Event", "Definição do evento; o nome de API recebe o sufixo __e.", ["src:help-platform-events-define"])
setup("reprocessamento-e-monitoramento-de-eventos", "Setup > Quick Find: Platform Events > (evento) > Subscriptions > Manage",
      "Ver assinantes e suspender ou retomar um trigger (Resume ou Resume from Tip).", ["src:pe-guide-subscribers"])
setup("change-data-capture", "Setup > Quick Find: Change Data Capture > selecionar os objetos", "Seleção de objetos para o canal padrão.", ["src:pubsub-qs-events"])
setup("bulk-api", "Setup > Quick Find: Bulk Data Load Jobs", "Acompanhar jobs; os concluídos saem da lista após 7 dias. Não é tela de configuração.", ["src:help-bulk-jobs"])
setup("conexoes-de-rede-privadas", "Setup > Quick Find: Private Connect > Create Outbound Connection",
      "Conexão de saída; o caminho da conexão de entrada não foi lido.", ["src:help-snowflake-private-connect"])
setup("servicos-externos-registrados-commerce", None,
      "Nenhum caminho de Setup encontrado: a fonte descreve o registro por API (Commerce Extension Providers) ou inserindo RegisteredExternalService.",
      ["src:commerce-extensions-guide"], estado="desconhecido")
print("ok lote 5i")
