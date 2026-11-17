"""Lote 7i (fecho da rodada A3, issue #34): o que faltava no tema Interface e experiência do usuário.

Lê o guia versionado 264.0 (API 68.0) e cadastra Network (primeiro nível), CustomSite, NavigationMenu, LightningExperienceSettings,
ListView, WebLink e PathAssistantSettings. Cria as funcionalidades experience-cloud-sites, list-views e
botoes-e-links-customizados, e confirma o caminho de Setup de page layouts.

Ordem: lote7h_filas_grupos.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7i_interface_fecho.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga.base import af, ev, ld, caminho    # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-16"
EXTR = "fontes/extracoes/lote7i-interface-fecho.txt"
ATLAS = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
PAGINAS = {"Network": "meta_network", "CustomSite": "meta_sites", "NavigationMenu": "meta_navigationmenu",
           "LightningExperienceSettings": "meta_lightningexperiencesettings", "ListView": "meta_listview", "WebLink": "meta_weblink",
           "PathAssistantSettings": "meta_pathassistantsettings"}


def substituir_fontes(novas):
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


substituir_fontes([C.fonte(f"src:mdapi-{n.lower()}", f"{n} (Metadata API)", ATLAS + pag + ".htm", f"Arquivo, versão e propriedades do tipo {n}.",
                           EXTR, DATA) for n, pag in PAGINAS.items()])
S_NET, S_SITE, S_NAV, S_LEX, S_LV, S_WL, S_PAS = (f"src:mdapi-{n.lower()}" for n in PAGINAS)

NOTA_COB = "Universo esperado = tabelas Fields da página do guia versionado 264.0 (API 68.0), lida em 2026-11-16."
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
B, S, I = "boolean", "string", "int"
FALSE = ("false", False, "A página declara default false.")
TRUE = ("valor", True, "A página declara default true.")
REGISTRADOS = []


def valores(*vs):
    return [(v, None) for v in vs]


def estrutura(nome, src, usada_por, rows, o_que_e):
    M.struct(nome, src, usada_por, rows, o_que_e)
    REGISTRADOS.append((src, "estruturas", nome))


def tipo(nome, src, *a, **k):
    M.mdt(nome, src, *a, **k)
    REGISTRADOS.append((src, "metadata-types", nome))


def linhas(tipo_, itens):
    """itens: (nome, desde, descrição[, req]) -> lista de P com o mesmo tipo."""
    return [P(n, tipo_, d, t, *r) for n, d, t, *r in itens]


# ================================================================ Network (primeiro nível)
TPL = "Email template usado {}."
estrutura("CommunityRoles", S_NET, ["mdt:Network"], [
    P("customerUserRole", S, None, "Rótulo do papel de usuário Customer."), P("employeeUserRole", S, None, "Rótulo do papel de usuário Employee."),
    P("partnerUserRole", S, None, "Rótulo do papel de usuário Partner."),
], "Os rótulos dos papéis de usuário (Customer, Partner e Employee) de um site. Desde a API 41.0.")
NET = (
    linhas(S, [("allowedExtensions", "36.0", "Tipos de arquivo que os membros podem enviar.")])
    + linhas(B, [("allowInternalUserLogin", "40.0", "Usuários internos entram no site com as credenciais internas, pela página de login do site."),
                 ("allowMembersToFlag", "29.0", "Membros podem sinalizar posts e comentários para revisão de um moderador.")])
    + [P("branding", "Branding", None, "Cores, cabeçalho e rodapé. Descontinuado na API 41.0; substituído por NetworkBranding.", ate="40.0")]
    + linhas(S, [("caseCommentEmailTemplate", None, TPL.format("nos avisos de comentário de caso")),
                 ("changePasswordTemplate", None, TPL.format("quando a senha de um usuário é redefinida")),
                 ("chgEmailVerNewTemplate", None, "Template que confirma a troca de e-mail, enviado ao endereço novo. Não é atualizável pela Metadata API."),
                 ("chgEmailVerOldTemplate", None, "Template que confirma a troca de e-mail, enviado ao endereço antigo. Não é atualizável pela Metadata API.")])
    + [P("communityRoles", "CommunityRoles", "41.0", "Rótulos dos papéis Customer, Partner e Employee.", estrutura="CommunityRoles")]
    + linhas(S, [("description", None, "Descrição do site."), ("deviceActEmailTemplate", "53.0", "Id do email template de ativação de dispositivo.")])
    + [P("disablePvtPagesForPwdResetInLWR", B, "67.0", "Bloqueia páginas privadas de sites LWR até a definição ou redefinição da senha terminar.", default=TRUE)]
    + linhas(B, [("disableReputationRecordConversations", "41.0", "Exclui contribuições em registros da contagem de pontos de reputação.")])
    + linhas(S, [("emailFooterLogo", "41.0", "Nome do documento usado como logo no rodapé dos e-mails."),
                 ("emailFooterText", "41.0", "Texto do rodapé dos e-mails."),
                 ("emailSenderAddress", None, "Endereço de onde os e-mails do site saem. Só pode ser definido na primeira implantação.", "S"),
                 ("emailSenderName", None, "Nome do remetente dos e-mails do site.", "S")])
    + linhas(B, [("embeddedLoginEnabled", None, "Permite pôr o formulário de login do Salesforce num site externo."),
                 ("enableApexCDNCaching", None, "Guarda em cache, em sites com CDN, dados públicos de Apex @wire para visitantes."),
                 ("enableCustomVFErrorPageOverrides", "41.0", "Usa páginas de erro Visualforce customizadas no lugar das padrão."),
                 ("enableDirectMessages", "41.0", "Usuários podem iniciar conversas privadas com vários membros."),
                 ("enableExperienceBundleBasedSnaOverrideEnabled", "52.0", "Usa a página SNA do Experience Builder e a substitui ao publicar."),
                 ("enableGuestChatter", None, "Visitantes acessam grupos públicos do Chatter sem login."),
                 ("enableGuestFileAccess", "41.0", "Visitantes veem asset files compartilhados nas páginas públicas e de login."),
                 ("enableGuestMemberVisibility", "47.0", "Visitantes podem ver membros autenticados."),
                 ("enableImageOptimizationCDN", "56.0", "Otimiza imagens em cache para visitantes de sites com CDN."),
                 ("enableInvitation", None, "Usuários podem convidar outras pessoas para o site."),
                 ("enableKnowledgeable", "30.0", "Membros veem e endossam quem conhece cada tópico."),
                 ("enableMemberVisibility", "45.0", "Liga, para o site, a preferência de ver outros membros.")])
    + [P("enableNicknameDisplay", B, "32.0", "Mostra apelidos em vez de nomes na maior parte dos lugares.", default=FALSE)]
    + linhas(B, [("enablePrivateMessages", "30.0", "Membros enviam e recebem mensagens privadas."),
                 ("enableReputation", "31.0", "Calcula e mostra a reputação dos membros."),
                 ("enableShowAllNetworkSettings", "41.0", "Mostra configurações do site que ficam ocultas por padrão."),
                 ("enableSiteAsContainer", None, "Com true, é um site do Experience Builder; com false, um site de Tabs + Visualforce."),
                 ("enableTalkingAboutStats", "41.0", "Mostra, ao digitar, quantas pessoas falam de um tópico."),
                 ("enableTopicAssignmentRules", "40.0", "Atribui tópicos a artigos automaticamente, por regras de categorias de Knowledge."),
                 ("enableTopicSuggestions", "41.0", "Sugere tópicos quando o usuário escreve um post."),
                 ("enableUpDownVote", "41.0", "Troca o like por votos a favor e contra.")])
    + [P("enableExpFriendlyUrlsAsDefault", B, "58.0", "Liga por padrão os URL slugs em certas páginas de sites LWR e de commerce.",
         notas=["A página traz um intervalo de versões (58.0 a 61.0); o limite final não ficou claro na leitura."])]
    + linhas(S, [("feedChannel", "28.0", "Feed das interações de um channel program ou grupo."),
                 ("forgotPasswordTemplate", None, TPL.format("quando o usuário esquece a senha"), "S")])
    + linhas(B, [("gatherCustomerSentimentData", "40.0", "Coleta dados de visualização de artigos e casos para o Community 360.")])
    + linhas(S, [("lockoutTemplate", "43.0", TPL.format("para usuários bloqueados por falhas de login")),
                 ("logoutUrl", "28.0", "URL para onde o membro vai depois de sair.")])
    + [P("maxFileSizeKb", I, "36.0", "Tamanho máximo de upload, em KB: de 3072 ao máximo da org; em branco, vale 2 GB."),
       P("navigationLinkSet", "NavigationLinkSet", "37.0", "Menu de navegação. Valeu da API 37.0 à 46.0; depois, usa-se NavigationMenu.", ate="46.0"),
       P("networkAuthApiSettings", "NetworkAuthApiSettings", "60.0", "Habilitação, acesso e segurança dos fluxos e APIs headless de identidade."),
       P("networkMemberGroups", "NetworkMemberGroups", None, "Perfis e permission sets cujos usuários são membros do site."),
       P("networkOptionsBit", B, "68.0", "Com true, e-mails de domínios não verificados usam o endereço do remetente.", default=FALSE),
       P("networkPageOverrides", "NetworkPageOverride", "40.0", "Mapeia Change Password, Forgot Password, Home e Login para tipos de página.")]
    + linhas(S, [("newSenderAddress", None, "Novo endereço de remetente ainda não verificado; substitui o atual depois da verificação."),
                 ("pendingSecondaryEmailAddress", "67.0", "Endereço secundário de remetente à espera de verificação."),
                 ("pwdlessRegEmailTemplate", None, TPL.format("no cadastro sem senha, com verificação de identidade")),
                 ("picassoSite", None, "Nome do site ChatterNetworkPicasso ligado ao site.")])
    + [P("recommendationAudience", "RecommendationAudience", "41.0", "Cria ou gerencia audiências de recomendações."),
       P("recommendationDefinition", "RecommendationDefinition", "41.0", "Recomendação customizada dirigida a uma audiência."),
       P("reputationLevels", "ReputationLevelDefinitions", None, "Níveis de reputação atribuídos conforme os membros somam pontos."),
       P("reputationPointsRules", "ReputationPointsRules", None, "Pontos que os membros ganham por ações definidas."),
       P("secondaryEmailSenderEnabled", B, "67.0", "Com true, e-mails com dados sensíveis saem do endereço secundário.", default=FALSE),
       P("selfRegMicroBatchSubErrorEmailTemplate", "reference", "54.0", "Template enviado quando o autocadastro em micro-batch falha.",
         natureza="texto_livre", contexto="A página tipa o campo como reference.")]
    + linhas(S, [("selfRegProfile", "29.0", "Perfil dos usuários autocadastrados; só vale com autocadastro ligado.")])
    + linhas(B, [("selfRegistration", None, "Indica se o autocadastro está disponível no site."),
                 ("sendWelcomeEmail", None, "Envia e-mail de boas-vindas quando um usuário é incluído.")])
    + [P("site", S, None, "O CustomSite associado a este site.", "S"),
       P("siteArchiveStatus", "SitesArchiveStatus", None, "Estado de arquivamento do site.", vals=[
           ("NotArchived", None), ("TemporarilyArchived", "Pode ser desarquivado depois.")]),
       P("status", "NetworkStatus", None, "Estado do site.", "S", vals=valores("Live", "DownForMaintenance", "UnderConstruction"),
         notas=["A tabela tipa o campo como NetworkStatus[]."]),
       P("tabs", "NetworkTabSet", None, "Abas disponíveis no site, escolhidas por quem o criou.", "S")]
    + linhas(S, [("urlPathPrefix", None, "Primeiro segmento do caminho da URL, que distingue este site."),
                 ("verificationTemplate", "44.0", TPL.format("na verificação de identidade, como login sem senha ou dispositivo novo")),
                 ("welcomeTemplate", None, TPL.format("nas boas-vindas a novos membros"))])
    + [M.FULLNAME_HERDADO(None)])
tipo("Network", S_NET,
     "Um site do Experience Cloud: membros, autocadastro, e-mails, moderação, reputação e opções de visitantes.",
     "Versionar e implantar a configuração dos sites do Experience Cloud.", "28.0", NET, exemplo=CAB + f"""<Network {NS}>
    <description>[descrição do site]</description>
    <emailSenderAddress>[endereço de e-mail do remetente]</emailSenderAddress>
    <emailSenderName>[nome do remetente]</emailSenderName>
    <enableSiteAsContainer>true</enableSiteAsContainer>
    <forgotPasswordTemplate>[email template de senha esquecida]</forgotPasswordTemplate>
    <selfRegistration>false</selfRegistration>
    <site>[nome do CustomSite]</site>
    <!-- Valores documentados: Live, DownForMaintenance, UnderConstruction -->
    <status>UnderConstruction</status>
    <urlPathPrefix>[prefixo da URL]</urlPathPrefix>
</Network>""", curinga=None,
     alertas=["emailSenderAddress só pode ser definido na primeira implantação; mudanças posteriores pela Metadata API são ignoradas, sem erro.",
              "A página recomenda email templates do Classic: os do Lightning Experience não são empacotáveis.",
              "O site aponta para um CustomSite (campo site); implante os dois juntos.",
              "O menu de navegação saiu deste tipo: desde a API 47.0, fica em NavigationMenu."],
     cobertura_nota=NOTA_COB + " Primeiro nível: 70 de 70 campos. A página tem 176.691 caracteres e só os primeiros 100.000 foram lidos: dos "
                    "subtipos, só CommunityRoles foi cadastrado. O trecho lido não traz exemplo XML nem trata do curinga.")

# ================================================================ CustomSite
estrutura("SiteIframeWhiteListUrl", S_SITE, ["mdt:CustomSite"], [P("url", S, None, "Domínio confiável autorizado a mostrar o site num frame.", "S")],
          "Um domínio externo autorizado a enquadrar (frame) o site.")
estrutura("SiteRedirectMapping", S_SITE, ["mdt:CustomSite"], [
    P("action", "SiteRedirect", None, "Tipo de redirecionamento.", "S", vals=valores("Permanent", "Temporary")),
    P("isActive", B, None, "Indica se o redirecionamento está ativo."),
    P("source", S, None, "URL relativa a redirecionar.", "S"), P("target", S, None, "Nova URL, relativa ou completa.", "S"),
], "Uma regra de redirecionamento de URL de um site.")
estrutura("SiteWebAddress", S_SITE, ["mdt:CustomSite"], [
    P("certificate", S, None, "Certificado usado em HTTPS no domínio customizado."),
    P("domainName", S, None, "Domínio do site.", "S"), P("primary", B, None, "Indica se este é o domínio principal.", "S"),
], "Um endereço web customizado de um site.")
PUB = "Deixa visíveis a usuários públicos {}."
VF = "Página Visualforce {}."
CA = " Vale para Chatter Answers."
SITE = (
    [P("active", B, None, "Liga ou desliga o site.", "S")]
    + linhas(B, [("allowHomePage", "15.0", PUB.format("a home page padrão"), "S"),
                 ("allowStandardAnswersPages", "19.0", PUB.format("as páginas padrão de answers")),
                 ("allowStandardIdeasPages", "15.0", PUB.format("as páginas padrão de Ideas"), "S"),
                 ("allowStandardLookups", "15.0", PUB.format("as páginas padrão de lookup"), "S"),
                 ("allowStandardPortalPages", "39.0", "Deixa usuários autenticados acessarem as páginas padrão que seus controles de acesso permitem.", "S"),
                 ("allowStandardSearch", "15.0", PUB.format("as páginas padrão de busca"), "S")])
    + linhas(S, [("analyticsTrackingCode", "17.0", "Código de rastreamento de serviços como o Google Analytics."),
                 ("authorizationRequiredPage", None, VF.format("mostrada quando o visitante não tem acesso à página")),
                 ("bandwidthExceededPage", None, VF.format("mostrada quando a cota de banda é excedida"))])
    + [P("browserXssProtection", B, "41.0", "Liga a proteção contra cross-site scripting refletido.", "S"),
       P("cachePublicVisualforcePagesInProxyServers", B, "52.0", "Proxies guardam em cache as páginas públicas só para visitantes.", default=TRUE)]
    + linhas(S, [("changePasswordPage", None, VF.format("em que usuários de portal trocam a senha")),
                 ("chatterAnswersForgotPasswordConfirmPage", "27.0", "Página que confirma o envio de senha temporária por e-mail." + CA),
                 ("chatterAnswersForgotPasswordPage", "27.0", "Página aberta pelo link de senha esquecida." + CA),
                 ("chatterAnswersHelpPage", "27.0", "Página aberta pelo link de ajuda." + CA),
                 ("chatterAnswersLoginPage", "27.0", "Página em que os usuários entram no portal." + CA),
                 ("chatterAnswersRegistrationPage", "27.0", "Página em que os usuários se cadastram e acessam o portal.")])
    + [P("clickjackProtectionLevel", "SiteClickjackProtectionLevel", "30.0", "Controle de enquadramento (framing) do site.",
         vals=valores("AllowAllFraming", "External", "SameOriginOnly", "NoFraming")),
       P("contentSniffingProtection", B, "41.0", "Impede o navegador de adivinhar tipos MIME, o que bloqueia alguns scripts maliciosos.", "S"),
       P("cspUpgradeInsecureRequests", B, None, "Removido da API 52.0 em diante; ignorado na 51.0 e anteriores.", ate="51.0"),
       P("customWebAddresses", "SiteWebAddress[]", "21.0", "URLs customizadas de raiz; salvar substitui a lista inteira.", estrutura="SiteWebAddress"),
       P("description", S, None, "Descrição do site."),
       P("enableAuraRequests", B, "46.0", "Com true, visitantes usam recursos que só existem em Lightning.")]
    + linhas(S, [("favoriteIcon", None, "Nome do static resource do ícone da aba do navegador."),
                 ("fileNotFoundPage", None, VF.format("mostrada quando o visitante pede uma página que não existe")),
                 ("forgotPasswordPage", None, VF.format("do link Forgot Password; só em sites do Experience Cloud")),
                 ("genericErrorPage", None, VF.format("mostrada em erros não especificados")),
                 ("guestProfile", None, "Nome do perfil do usuário guest. Somente leitura."),
                 ("inMaintenancePage", None, VF.format("mostrada durante manutenção")),
                 ("inactiveIndexPage", None, VF.format("usada como home page do site inativo")),
                 ("indexPage", None, VF.format("usada como home page do site ativo"), "S"),
                 ("masterLabel", None, "Rótulo do site na interface do Salesforce.", "S"),
                 ("myProfilePage", "20.0", VF.format("em que os usuários atualizam seus dados de contato")),
                 ("portal", None, "Portal associado ao site para o login.")])
    + [P("redirectToCustomDomain", B, "52.0", "Redireciona as URLs de sistema para o domínio customizado em HTTPS.",
         notas=["O valor padrão varia conforme o tipo de site."]),
       P("referrerPolicyOriginWhenCrossOrigin", B, "41.0", "O cabeçalho referrer mostra só Salesforce.com, não a URL inteira.", "S"),
       P("requireHttps", B, None, "Removido da API 52.0 em diante; ignorado na 51.0 e anteriores.", ate="51.0"),
       P("requireInsecurePortalAccess", B, None, "Forçava HTTP no login de portal; removido na API 50.0 e posteriores.", ate="49.0")]
    + linhas(S, [("robotsTxtPage", None, VF.format("servida como robots.txt")), ("selfRegPage", None, VF.format("de autocadastro")),
                 ("serverIsDown", "17.0", "Static resource mostrado, a partir do cache, em caso de indisponibilidade."),
                 ("siteAdmin", None, "Username do administrador do site."),
                 ("siteGuestRecordDefaultOwner", "51.0", "Username que fica dono dos registros criados por usuários guest.")])
    + [P("siteIframeWhiteListUrls", "SiteIframeWhiteListUrl[]", "49.0", "Domínios externos autorizados a enquadrar o site.", estrutura="SiteIframeWhiteListUrl",
         notas=["O exemplo XML da página usa o nome no singular, siteIframeWhiteListUrl."]),
       P("siteRedirectMappings", "SiteRedirectMapping[]", "20.0", "As regras de redirecionamento de URL do site.", estrutura="SiteRedirectMapping"),
       P("siteTemplate", S, None, VF.format("usada como template do site")),
       P("siteType", "siteType", "27.0", "Diz se o site é Visualforce, Site.com ou ChatterNetwork.", "S", natureza="desconhecida",
         contexto="A página cita os três tipos na descrição, mas não lista os valores da enumeração."),
       P("subdomain", S, None, "Prefixo de subdomínio customizado anterior. Somente leitura."),
       P("urlPathPrefix", S, None, "Primeiro segmento do caminho da URL, que distingue este site."),
       M.FULLNAME_HERDADO(None)])
tipo("CustomSite", S_SITE,
     "Um site do Salesforce Sites (Visualforce): domínio, páginas de erro e de login, perfil guest e proteções de navegador. Um site do "
     "Experience Cloud também tem um CustomSite por trás.",
     "Versionar e implantar a configuração dos sites.", "14.0", SITE, exemplo=CAB + f"""<CustomSite {NS}>
    <active>true</active>
    <allowHomePage>false</allowHomePage>
    <allowStandardIdeasPages>false</allowStandardIdeasPages>
    <allowStandardLookups>false</allowStandardLookups>
    <allowStandardPortalPages>true</allowStandardPortalPages>
    <allowStandardSearch>false</allowStandardSearch>
    <browserXssProtection>true</browserXssProtection>
    <!-- Valores documentados: AllowAllFraming, External, SameOriginOnly, NoFraming -->
    <clickjackProtectionLevel>SameOriginOnly</clickjackProtectionLevel>
    <contentSniffingProtection>true</contentSniffingProtection>
    <indexPage>[página Visualforce inicial]</indexPage>
    <masterLabel>[rótulo do site]</masterLabel>
    <referrerPolicyOriginWhenCrossOrigin>true</referrerPolicyOriginWhenCrossOrigin>
    <urlPathPrefix>[prefixo da URL]</urlPathPrefix>
</CustomSite>""", curinga=True,
     alertas=["Segundo a página, o tipo vale para Salesforce Sites e sites Visualforce; sites do Experience Cloud usam o tipo Network (que aponta "
              "para um CustomSite).",
              "Salvar customWebAddresses substitui a lista inteira de endereços.",
              "guestProfile e subdomain são somente leitura."],
     divergencias=["O texto chama o campo de siteIframeWhiteListUrls; o exemplo XML usa siteIframeWhiteListUrl."],
     cobertura_nota=NOTA_COB)

# ================================================================ NavigationMenu
estrutura("NavigationMenuItemBranding", S_NAV, ["mdx:NavigationMenuItem"], [P("tileImage", S, None, "Nome do ContentAsset usado no item.")],
          "A imagem de um item de menu de navegação.")
estrutura("NavigationSubMenu", S_NAV, ["mdx:NavigationMenuItem"], [
    P("navigationMenuItem", "NavigationMenuItem[]", None, "Itens filhos de um item de menu.", estrutura="NavigationMenuItem"),
], "Os itens filhos de um item de menu. Só itens do tipo MenuLabel podem ter filhos. Desde a API 39.0.")
estrutura("NavigationMenuItem", S_NAV, ["mdt:NavigationMenu", "mdx:NavigationSubMenu"], [
    P("defaultListViewId", S, None, "Em itens SalesforceObject, o Id da list view padrão do objeto."),
    P("label", S, None, "Texto do item no menu.", "S"),
    P("menuItemBranding", "NavigationMenuItemBranding", "47.0", "Imagem do item.", estrutura="NavigationMenuItemBranding"),
    P("position", I, None, "Posição do item no menu.", "S"),
    P("publiclyAvailable", B, None, "Com true, usuários guest veem o item."),
    P("subMenu", "NavigationSubMenu", "39.0", "Itens filhos.", estrutura="NavigationSubMenu"),
    P("target", S, None, "URL do link (relativa em InternalLink) ou objeto; não é usado em MenuLabel nem NavigationalTopic.",
      "C:obrigatório quando type é ExternalLink, InternalLink ou SalesforceObject"),
    P("targetPreference", S, None, "Como abrir links externos.", vals=valores("None", "OpenInExternalTab"),
      contexto="A página lista estes valores para um campo string; o exemplo XML dela usa OpenExternalLinkInSameTab, que não está na lista."),
    P("type", S, None, "Tipo do item.", "S", vals=[("SalesforceObject", None), ("ExternalLink", None), ("InternalLink", None),
                                                  ("MenuLabel", "Desde a API 39.0."), ("NavigationalTopic", "Lista suspensa de tópicos do site.")],
      contexto="A página lista estes valores para um campo do tipo string."),
], "Um item de um menu de navegação de site.")
tipo("NavigationMenu", S_NAV,
     "Um menu de navegação de um site do Experience Cloud, com seus itens e subitens.",
     "Versionar e implantar os menus de navegação dos sites.", "47.0", [
         P("container", S, None, "Nome do contêiner do menu."),
         P("containerType", S, None, "Tipo do contêiner.", vals=valores("Network", "CommunityTemplateDefinition"),
           contexto="A página lista estes valores para um campo do tipo string."),
         P("label", S, None, "Rótulo do menu no Experience Builder."),
         P("navigationMenuItem", "NavigationMenuItem[]", None, "Os itens do menu.", estrutura="NavigationMenuItem"),
         M.FULLNAME_HERDADO(None),
     ], exemplo=CAB + f"""<NavigationMenu {NS}>
    <container>[nome do site]</container>
    <!-- Valores documentados: Network, CommunityTemplateDefinition -->
    <containerType>Network</containerType>
    <label>[rótulo do menu]</label>
    <navigationMenuItem>
        <label>[texto do item]</label>
        <position>1</position>
        <publiclyAvailable>true</publiclyAvailable>
        <target>[URL ou objeto]</target>
        <!-- Valores documentados: SalesforceObject, ExternalLink, InternalLink, MenuLabel, NavigationalTopic -->
        <type>InternalLink</type>
    </navigationMenuItem>
</NavigationMenu>""", curinga=True,
     alertas=["Exige a permissão MultipleNavigationMenu.",
              "Nos templates Help Center e LWR (Build Your Own e Microsites) não há páginas genéricas de registro: sem criar as páginas do objeto, "
              "um item do tipo objeto não mostra nada ao usuário."],
     divergencias=["O exemplo XML usa targetPreference com o valor OpenExternalLinkInSameTab, fora da lista documentada (None, OpenInExternalTab)."],
     cobertura_nota=NOTA_COB)

# ================================================================ LightningExperienceSettings
SAI = "{} na API {}; o recurso não existe mais."
LEX = (
    [P("activeThemeName", S, "48.0", "Nome do LightningExperienceTheme customizado ativo. Omitido, vale um tema pronto da Salesforce."),
     P("enableAccessCheckCrucPref", B, None, SAI.format("Descontinuado", "47.0")),
     P("enableApiUserLtngOutAccessPref", B, None, "Descontinuado na API 48.0; tratava da restrição de Lightning Out para usuários API Only."),
     P("enableAuraBoxcarReductionPref", "não informado na página", None, "Com true, desliga uma otimização de agrupamento de requisições do Aura.",
       default=FALSE, natureza="desconhecida", contexto="A página deixa o tipo do campo em branco; a descrição usa true e o default declarado é false."),
     P("enableAuraCDNPref", B, None, "Usa CDN para o conteúdo estático dos Lightning components.", default=TRUE),
     P("enableAuraDepAccessChksCRUCPref", B, None, SAI.format("Removido", "51.0")),
     P("enableAuraSecStaticResCRUCPref", B, None, "Removido na API 68.0."),
     P("enableDeferRenderingWorkspacePage", B, "64.0", "Adia o carregamento de páginas inativas de workspace do console.", default=TRUE),
     P("enableErrorExperienceEnabled", B, None, "Reservado para uso futuro."),
     P("enableFeedbackInMobile", B, None, "Deixa usuários enviarem feedback à Salesforce pelo app móvel.", default=FALSE),
     P("enableGoogleSheetsForSfdcEnabled", B, None, "Reservado; não usar."),
     P("enableIE11DeprecationMsgHidden", B, None, SAI.format("Descontinuado", "47.0")),
     P("enableIE11LEXCrucPref", B, None, SAI.format("Descontinuado", "47.0")),
     P("enableInAppLearning", B, "54.0", "Liga os Learning Paths; com false, bloqueia atribuições.", default=TRUE),
     P("enableInAppTooltips", B, None, "Mostra dicas de primeiros passos no app móvel.", default=FALSE),
     P("enableLEXOnIpadEnabled", B, None, "Liga o Lightning Experience em navegadores de iPad.", default=FALSE),
     P("enableLexEndUsersNoSwitching", B, None, "Desliga o Salesforce Classic e tira o seletor de interface.", default=FALSE),
     P("enableLightningPreviewPref", B, "62.0", "Liga o Local Dev na org.", default=FALSE),
     P("enableNavPersonalizationOptOut", B, None, "Impede os usuários de personalizar a barra de navegação.", default=FALSE),
     P("enableNoBackgroundNavigations", B, None, "Com true, bloqueia chamadas consecutivas de navegação por API em Visualforce.", default=FALSE),
     P("enableQuip", B, "51.0", "Indica se o Quip está disponível na org."),
     P("enableRemoveThemeBrandBanner", B, None, SAI.format("Descontinuado", "47.0")),
     P("enableS1BannerPref", B, None, SAI.format("Descontinuado", "47.0")),
     P("enableS1BrowserEnabled", B, None, "Deixa todos os usuários acessarem a versão web móvel por navegadores suportados."),
     P("enableS1DesktopEnabled", B, None, "Liga o Lightning Experience na org. Depois de ligado, não pode ser desligado."),
     P("enableS1UiLoggingEnabled", B, None, SAI.format("Descontinuado", "47.0")),
     P("enableSidToken3rdPartyAuraApp", B, None, "Reservado para uso interno."),
     P("enableSkypeChatEnabled", B, None, SAI.format("Descontinuado", "50.0")),
     P("enableSparkAllUsers", B, None, SAI.format("Descontinuado", "50.0")),
     P("enableSparkConversationEnabled", B, None, SAI.format("Descontinuado", "50.0")),
     P("enableSplitViewOnStandard", B, None, SAI.format("Removido", "52.0")),
     P("enableStackedModalManagerEnabled", B, "61.0", "Liga os Stacked Modals de LWC.", notas=["O padrão depende da data de criação da org."]),
     P("enableTryLightningOptOut", B, None, "Esconde o convite para experimentar o Lightning Experience.", default=FALSE),
     P("enableUseS1AlohaDesktop", B, None, SAI.format("Descontinuado", "47.0")),
     P("enableUsersAreLightningOnly", B, None, "Desliga o Salesforce Classic para os usuários; parecido com enableLexEndUsersNoSwitching.", default=FALSE),
     P("enableWebExEnabled", B, None, SAI.format("Descontinuado", "50.0")),
     P("enableWebexAllUsers", B, None, SAI.format("Descontinuado", "50.0")),
     P("isLEXExtensionComponentCustomizationOff", B, "48.0", "Com false, desliga o Extension Component Customization para todos."),
     P("isLEXExtensionDarkModeOff", B, "48.0", "Com false, desliga o Extension Dark Mode para todos."),
     P("isLEXExtensionLinkGrabberOff", B, "48.0", "Com false, desliga o Extension Link Grabber para todos."),
     P("isLEXExtensionOff", B, "48.0", "Com false, impede os usuários de ligar a Lightning Extension."),
     M.FULLNAME_HERDADO(None)])
tipo("LightningExperienceSettings", S_LEX,
     "Configurações do Lightning Experience na org: o tema ativo, ligar o Lightning Experience, desligar o Classic e opções de navegação e do app móvel.",
     "Recuperar e implantar as opções do Lightning Experience, inclusive qual tema customizado está ativo.", "47.0", LEX, exemplo=CAB + f"""<LightningExperienceSettings {NS}>
    <activeThemeName>[nome do LightningExperienceTheme ativo]</activeThemeName>
    <enableAuraCDNPref>true</enableAuraCDNPref>
    <enableNavPersonalizationOptOut>false</enableNavPersonalizationOptOut>
    <enableS1DesktopEnabled>true</enableS1DesktopEnabled>
    <enableUsersAreLightningOnly>false</enableUsersAreLightningOnly>
</LightningExperienceSettings>""", arquivos_prontos=M.arquivos_settings("LightningExperienceSettings", "LightningExperience", S_LEX), curinga=False,
     alertas=["enableS1DesktopEnabled não volta atrás: depois de ligado, nem a interface nem a API desligam o Lightning Experience.",
              "enableLexEndUsersNoSwitching e enableUsersAreLightningOnly são parecidos: qualquer um com true impede a troca para o Classic.",
              "A página avisa que usar CDN pode mudar o domínio que serve os arquivos; orgs com restrição de IP devem testar antes.",
              "Boa parte dos campos está descontinuada ou removida; a descrição de cada um diz em que versão."],
     divergencias=["A linha de enableAuraBoxcarReductionPref vem sem tipo na página."],
     cobertura_nota=NOTA_COB + " 41 de 41 campos. A página não informa obrigatoriedade; o nome do arquivo (LightningExperience) vem do package.xml de exemplo.")
C.marcar_referencia("metadata-types", "LightningExperienceSettings", "activeThemeName", "mdt:LightningExperienceTheme")

# ================================================================ ListView e WebLink (filhos de CustomObject)
estrutura("ListViewFilter", S_LV, ["mdt:ListView"], [
    P("field", S, None, "Campo a que o filtro se aplica.", "S", notas=["A tabela chama a linha de filter; o exemplo XML usa o elemento field."]),
    P("operation", "FilterOperation", None, "Operador de comparação.", "S", vals=[(v, None) for v in (
        "equals", "notEqual", "lessThan", "greaterThan", "lessOrEqual", "greaterOrEqual", "contains", "notContain", "startsWith", "includes",
        "excludes")] + [("within", "Só para critérios de distância.")]),
    P("value", S, None, "Valor comparado."),
], "Uma linha de filtro de uma list view.")
tipo("ListView", S_LV,
     "Uma list view: a lista filtrada de registros de um objeto, com as colunas mostradas e com quem é compartilhada.",
     "Versionar e implantar as list views públicas de um objeto.", "14.0", [
         P("booleanFilter", S, None, "Lógica que combina as linhas de filtro com AND e OR."),
         P("columns", "string[]", None, "Campos mostrados na lista."),
         P("division", S, "17.0", "Division dos registros, quando a org usa divisions."),
         P("filterScope", "FilterScope", None, "De quem são os registros listados.", "S", vals=[
             ("Everything", "Todos os registros."), ("Mine", "Os do usuário que abre a lista."),
             ("MineAndMyGroups", "Os do usuário e os das filas dele."), ("AssignedToMe", "Atribuídos ao usuário; só ServiceAppointment."),
             ("Queue", "Os atribuídos a uma fila."), ("Delegated", "Delegados a outro usuário. Desde a API 17.0."),
             ("MyTerritory", "Do território do usuário. Desde a API 17.0."), ("MyTeamTerritory", "Do território do time do usuário. Desde a API 17.0."),
             ("Team", "Atribuídos a um time. Desde a API 17.0."), ("SalesTeam", "Oportunidades de uma equipe de oportunidade. Desde a API 49.0."),
             ("ScopingRule", "Os que atendem a uma scoping rule.")]),
         P("filters", "ListViewFilter[]", None, "Linhas de filtro.", estrutura="ListViewFilter"),
         P("fullName", S, None, "Nome de API da list view; precisa ser informado ao criar, atualizar ou excluir. Herdado.", "S", herdada="Metadata"),
         P("label", S, None, "Nome da list view na interface.", "S"),
         P("language", "Language", "17.0", "Idioma do filtro, usado com startsWith e contains no Translation Workbench.", natureza="desconhecida",
           contexto="A página não lista os valores."),
         P("queue", S, None, "Nome da fila. Criar uma fila cria automaticamente a list view correspondente."),
         P("sharedTo", "SharedTo", "17.0", "Com quem a list view é compartilhada."),
     ], parent="CustomObject", exemplo=CAB + f"""<!-- No arquivo .object do objeto, este conteúdo fica no elemento <listViews> -->
<ListView {NS}>
    <fullName>[Nome_Da_List_View]</fullName>
    <columns>NAME</columns>
    <!-- Valores documentados incluem: Everything, Mine, Queue -->
    <filterScope>Everything</filterScope>
    <filters>
        <field>[campo]</field>
        <operation>equals</operation>
        <value>[valor]</value>
    </filters>
    <label>[nome da list view]</label>
</ListView>""", arquivos_prontos=M.arquivos("ListView", "CustomObject"), curinga=False,
     alertas=["List views marcadas como visíveis só para o próprio usuário não são acessíveis pela Metadata API.",
              "O curinga (*) não funciona no package.xml para list views.",
              "A página recomenda não empacotar list views padrão sem alteração: elas podem gerar duplicatas na org de destino.",
              "List views de objetos padrão existem na API desde a 17.0; as de objetos customizados, desde a 14.0."],
     cobertura_nota=NOTA_COB + " O subtipo SharedTo tem página própria, não lida.")

NW = "Só vale quando openType é newWindow: "
tipo("WebLink", S_WL,
     "Um botão ou link customizado de um objeto: abre uma URL, uma página Visualforce ou executa JavaScript.",
     "Versionar e implantar os botões e links customizados, junto com o objeto.", "12.0", [
         P("availability", "WebLinkAvailability", None, "Indica se o link funciona só online ou também offline.", "S", vals=valores("online", "offline")),
         P("description", S, None, "Descrição do botão ou link."),
         P("displayType", "WebLinkDisplayType", None, "Como aparece: link, botão ou botão de ação em massa de related list.",
           vals=valores("link", "button", "massActionButton")),
         P("encodingKey", "Encoding", None, "Codificação do conteúdo, quando ele vem de uma URL.", "S", default=("valor", "UTF-8", "A página informa UTF-8 como padrão."),
           vals=valores("UTF-8", "ISO-8859-1", "Shift_JIS", "ISO-2022-JP", "EUC-JP", "x-SJIS_0213", "ks_c_5601-1987", "Big5", "GB2312", "Big5-HKSCS")),
         P("fullName", S, None, "Nome interno: começa por letra; só letras, números e sublinhados. Informado ao criar, atualizar ou excluir. Herdado.", "?",
           herdada="Metadata"),
         P("hasMenubar", B, None, NW + "mostra a barra de menus do navegador."),
         P("hasScrollbars", B, None, NW + "mostra barras de rolagem."),
         P("hasToolbar", B, None, NW + "mostra a barra de ferramentas do navegador."),
         P("height", I, None, "Altura da janela, em pixels.", "C:obrigatório quando openType é newWindow"),
         P("isResizable", B, None, NW + "permite redimensionar a janela."),
         P("linkType", "WebLinkType", None, "De onde vem o conteúdo.", "S", vals=[
             ("url", None), ("sControl", None), ("javascript", None), ("page", "Página Visualforce."), ("flow", "Reservado para uso futuro.")]),
         P("masterLabel", S, None, "Rótulo interno, não traduzido."),
         P("openType", "WebLinkWindowType", None, "Como a janela abre ao clicar.", "S",
           vals=valores("newWindow", "sidebar", "noSidebar", "replace", "onClickJavaScript")),
         P("page", S, None, "Nome da página Visualforce; só quando linkType é page."),
         P("position", "WebLinkPosition", None, NW + "posição da janela.", vals=valores("fullScreen", "none", "topLeft")),
         P("protected", B, None, "Marca o subcomponente como protegido: a org que instala o pacote não pode referenciá-lo.", "S"),
         P("requireRowSelection", B, None, "Só para massActionButton: exige selecionar linhas antes de executar."),
         P("scontrol", S, None, "Nome do s-control; só quando linkType é sControl."),
         P("showsLocation", B, None, NW + "mostra a barra de endereço."),
         P("showsStatus", B, None, NW + "mostra a barra de status."),
         P("url", S, None, "A URL (tipo url) ou o JavaScript (tipo javascript); precisa de escape de XML."),
         P("width", I, None, "Largura da janela, em pixels.", "C:obrigatório quando openType é newWindow"),
     ], parent="CustomObject", exemplo=CAB + f"""<!-- No arquivo .object do objeto, este conteúdo fica no elemento <webLinks> -->
<WebLink {NS}>
    <fullName>[Nome_Do_Botao]</fullName>
    <!-- Valores documentados: online, offline -->
    <availability>online</availability>
    <!-- Valores documentados: link, button, massActionButton -->
    <displayType>button</displayType>
    <encodingKey>UTF-8</encodingKey>
    <!-- Valores documentados: url, sControl, javascript, page -->
    <linkType>url</linkType>
    <masterLabel>[rótulo do botão]</masterLabel>
    <!-- Valores documentados: newWindow, sidebar, noSidebar, replace, onClickJavaScript -->
    <openType>replace</openType>
    <protected>false</protected>
    <url>[URL]</url>
</WebLink>""", arquivos_prontos=M.arquivos("WebLink", "CustomObject"), curinga=False,
     alertas=["O curinga (*) não funciona no package.xml para este tipo.",
              "height e width são obrigatórios quando a janela abre em newWindow e devem ficar vazios nos demais casos.",
              "Botões e links da home page são outro tipo (CustomPageWebLink), não lido."],
     cobertura_nota=NOTA_COB)

# ================================================================ PathAssistantSettings
tipo("PathAssistantSettings", S_PAS,
     "Configurações do Path na org: ligar o recurso e lembrar se cada usuário deixou o path aberto.",
     "Recuperar e implantar as opções gerais do Path.", "34.0", [
         P("canOverrideAutoPathCollapseWithUserPref", B, "47.0", "Mantém o path aberto até o usuário recolhê-lo. Só funciona com o Path ligado.", default=FALSE),
         P("pathAssistantEnabled", B, "35.0", "Liga o Path.", notas=["Segundo a página, o padrão é true em Enterprise Edition e false nas demais."]),
         P("pathAssistantForOpportunityEnabled", B, "34.0", "Controlava o Path só para Opportunity. Existe até a API 34.0.", ate="34.0"),
         M.FULLNAME_HERDADO(None),
     ], exemplo=CAB + f"""<PathAssistantSettings {NS}>
    <canOverrideAutoPathCollapseWithUserPref>false</canOverrideAutoPathCollapseWithUserPref>
    <pathAssistantEnabled>true</pathAssistantEnabled>
</PathAssistantSettings>""", arquivos_prontos=M.arquivos_settings("PathAssistantSettings", "PathAssistant", S_PAS), curinga=False,
     alertas=["Com canOverrideAutoPathCollapseWithUserPref em false, o path se recolhe a cada carregamento da página."],
     divergencias=["A tabela de campos traz uma quarta linha em branco, sem nome nem tipo."],
     cobertura_nota=NOTA_COB + " A página não informa obrigatoriedade.")

M.emit_structs()
C.marcar_referencia("metadata-types", "Network", "site", "mdt:CustomSite")
C.rel_referencia("network-customsite", "mdt:Network", "site", "mdt:CustomSite", "Um site do Experience Cloud aponta o CustomSite que o sustenta.", S_NET)
C.rel_referencia("lexsettings-theme", "mdt:LightningExperienceSettings", "activeThemeName", "mdt:LightningExperienceTheme",
                 "As configurações do Lightning Experience dizem qual tema customizado está ativo.", S_LEX)

# ================================================================ nota de extração: lista de campos
ls = ["", "-- Lista de campos transcrita da leitura (gerada por lote7i_interface_fecho.py; nome | tipo | desde)"]
for src, pasta, nome in REGISTRADOS:
    props = ld(f"{pasta}/{nome}.json")["propriedades"]
    ls.append(f"[{src}] {nome}: " + ", ".join(f"{q['nome']} | {q['tipo_tecnico']} | {q.get('desde_versao') or '-'}" for q in props))
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(ls) + "\n")

# ================================================================ funcionalidades
UI = "interface-e-experiencia-do-usuario"
SEM_OBJ = {"tipo": "objeto_api", "estado": "desconhecido", "motivo": "Objetos API não investigados neste lote; a lista vazia não comprova inexistência."}


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


C.funcionalidade(
    "experience-cloud-sites", "Sites do Experience Cloud", "Experience Cloud Sites",
    ["experience cloud", "site", "community", "comunidade", "portal", "experience builder", "experience workspaces", "network", "all sites"],
    "Um site do Experience Cloud é um espaço com a marca da empresa para clientes, parceiros ou funcionários, construído sobre a org e os "
    "dados dela. O site nasce de um template, no assistente de criação, e é ajustado no Experience Builder.",
    "Dar a pessoas de fora (ou de dentro) um lugar para se atender, colaborar e fazer negócios com a empresa.",
    "Um portal de clientes em que cada cliente abre casos, acompanha os próprios pedidos e consulta artigos de ajuda.",
    (UI, "experiencias-web-portais-e-mobile"), [],
    [("Network", "A configuração de cada site."), ("CustomSite", "O site que sustenta o Network: domínio, páginas de erro e perfil guest."),
     ("NavigationMenu", "Os menus de navegação do site.")], [],
    [S_NET, S_SITE, S_NAV, "src:help-experience-cloud", "src:help-experience-site-create", "src:help-experience-find-way", "src:help-experience-build"],
    [SEM_OBJ],
    setup("Setup > Quick Find: Digital Experiences > All Sites > New", "src:help-experience-site-create", "O assistente de criação mostra os templates."),
    alertas=["São três lugares de trabalho: o Setup (ligar o recurso, criar o site, permissões), o Experience Workspaces (conteúdo, "
             "configurações e monitoramento) e o Experience Builder (aparência e páginas).",
             "Criar um site exige as permissões Create and Set Up Experiences e View Setup and Configuration.",
             "O número máximo de sites da org aparece no topo da página Sites, no Setup.",
             "Como metadado, o endereço de e-mail do remetente do site só pode ser definido na primeira implantação."])
C.ampliar_funcionalidade("digital-experiences", mdts=[("Network", "Cada site criado depois de ligar o recurso.")], srcs=[S_NET])

C.funcionalidade(
    "list-views", "List views", "List Views", ["list view", "lista", "visão de lista", "filtro", "create new view", "public list view"],
    "Uma list view mostra um conjunto de registros de um objeto que atende a certos filtros, com as colunas escolhidas. Pode ser só de quem "
    "a criou ou compartilhada com outros usuários.",
    "Ver e trabalhar de uma vez os registros que interessam, como os casos abertos de uma fila.",
    "A list view Meus casos abertos mostra só os casos do próprio atendente que ainda não foram fechados.",
    (UI, "aplicativos-e-navegacao"), [],
    [("ListView", "Cada list view pública, definida junto com o objeto.")], [],
    [S_LV, "src:help-list-view-classic", "src:help-kb-list-view-permissions", "src:help-queues-lead-distribution"], [SEM_OBJ],
    af("nao_aplicavel", None, "List views são criadas na própria página de lista do objeto, não no Setup.", [ev("src:help-list-view-classic")]),
    alertas=["Criar list views exige Read no objeto e a permissão Create and Customize List Views; criar, editar ou excluir list views "
             "públicas exige Manage Public List Views.",
             "Criar uma fila cria automaticamente uma list view para ela.",
             "List views visíveis só para o próprio usuário não saem pela Metadata API."])
C.ampliar_funcionalidade("filas", mdts=[("ListView", "A list view criada junto com a fila (campo queue).")], srcs=[S_LV])

C.funcionalidade(
    "botoes-e-links-customizados", "Botões e links customizados", "Custom Buttons and Links",
    ["custom button", "custom link", "botão customizado", "weblink", "list view button", "buttons, links, and actions"],
    "Um botão ou link customizado abre uma URL ou uma página Visualforce, ou executa JavaScript, a partir da página de um registro ou de "
    "uma lista. É definido no objeto, na mesma tela de Setup das quick actions.",
    "Levar o usuário, com um clique, a uma página ou ferramenta relacionada ao registro.",
    "Na lista de contatos, um botão abre a URL de um flow para os registros selecionados.",
    (UI, "acoes-rapidas"), [],
    [("WebLink", "Cada botão ou link customizado, definido junto com o objeto.")], [],
    [S_WL, "src:help-flow-list-button", "src:help-actions-lex", "src:help-actions-page-layout-editor"], [SEM_OBJ],
    setup("Setup > Object Manager > [objeto] > Buttons, Links, and Actions > New Button or Link", "src:help-flow-list-button"),
    alertas=["No Lightning Experience, botões padrão e customizados também contam como ações e aparecem junto das quick actions.",
             "No editor de page layout, a categoria Mobile & Lightning Actions reúne quick actions e botões padrão e customizados."])

C.ampliar_funcionalidade("path", mdts=[("PathAssistantSettings", "Liga o Path na org e guarda a opção de lembrar o path aberto.")],
                         srcs=[S_PAS, "src:help-path-overview", "src:help-path-considerations", "src:help-path-enable", "src:help-kb-path-record-type"],
                         alertas=["Cada objeto pode ter um path por record type; não há limite de paths por org.",
                                  "Em cada etapa cabem até cinco campos-chave e até 1.000 caracteres de orientação.",
                                  "A orientação (Guidance for Success) de leads não aparece quando o path está no record type Master: é preciso um "
                                  "path para o record type específico."])
C.ampliar_funcionalidade("temas-e-branding", mdts=[("LightningExperienceSettings", "Diz qual tema customizado está ativo (activeThemeName).")], srcs=[S_LEX])
C.ampliar_funcionalidade("acoes-rapidas", srcs=["src:help-quick-actions-kb", "src:help-quick-action-considerations", "src:help-global-quick-actions",
                                                "src:help-actions-ordering", "src:help-flow-quick-action"],
                         alertas=["Ações globais não conhecem o contexto: não preenchem campos com dados da página em que o usuário está.",
                                  "Para ver uma ação de objeto no page layout, o usuário precisa de Read e Edit no campo de relacionamento da ação.",
                                  "Quick actions que rodam flows só existem como ações de objeto, e o flow precisa estar ativo."])
C.ampliar_funcionalidade("tabs", srcs=["src:help-custom-tabs-overview", "src:help-custom-tab-considerations", "src:help-vf-tabs", "src:help-app-builder-limits"],
                         alertas=["O limite de custom tabs é fixo por edição e não pode ser aumentado.",
                                  "Um objeto customizado com custom tab é pesquisável por padrão, mesmo que o usuário não mostre a aba."])
C.definir_setup("page-layouts", "Setup > Object Manager > [objeto] > Page Layouts", "Lista dos page layouts do objeto; New cria um layout.",
                ["src:help-kb-page-layout-section", "src:help-page-layouts-create"])
C.ampliar_funcionalidade("page-layouts", srcs=["src:help-page-layouts", "src:help-page-layouts-create", "src:help-kb-page-layout-section"],
                         alertas=["Criar, editar e excluir page layouts exige a permissão Customize Application."])
print(f"lote 7i: 7 metadata types e {sum(1 for r in REGISTRADOS if r[1] == 'estruturas')} estruturas gravados; 3 funcionalidades novas e 8 ampliadas")
