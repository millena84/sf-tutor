"""Lote 7d (rodada A3, issue #34): metadata types e funcionalidades do tema Interface e experiência do usuário.

Lê o guia versionado 264.0 (API 68.0) e cadastra CustomApplication (15 estruturas), Layout (25 estruturas), CompactLayout,
LightningExperienceTheme e BrandingSet (1 estrutura), mais 5 funcionalidades (Lightning apps, page layouts, compact layouts,
Dynamic Forms e temas e branding). Liga LWC, Aura e Visualforce ao tema de Lightning pages e componentes.

As fontes de Ajuda citadas pelas funcionalidades são registradas por conteudo_temas.py (lista em conteudo_detalhe.py).
Ordem: lote7c_assincrono.py, este script, lote7e_observabilidade.py, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7d_interface.py   (com --nota, regrava também a lista de campos da nota de extração)
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga.base import af, ev, ld, sv, caminho  # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-16"
EXTR = "fontes/extracoes/mdapi-lote7d-interface.txt"
ATLAS = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
PAGINAS = {"CustomApplication": "meta_customapplication", "Layout": "meta_layouts", "CompactLayout": "meta_compactlayout",
           "LightningExperienceTheme": "meta_lightningexperiencetheme", "BrandingSet": "meta_brandingset"}


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
S_APP, S_LAY, S_CL, S_THEME, S_BRAND = (f"src:mdapi-{n.lower()}" for n in PAGINAS)

FULLNAME = M.FULLNAME_HERDADO(None)
NOTA_COB = "Universo esperado = tabela Fields da página do guia versionado 264.0 (API 68.0), lida em 2026-11-16."
SEM_REQ = " A página não marca campos como obrigatórios no tipo principal."
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
B, S, I = "boolean", "string", "int"
NOTA_REGISTRO = {}   # tipo ou estrutura -> linhas, para a nota de extração


def valores(*vs):
    return [(v, None) for v in vs]


def conjunto(raiz, src, topo, subs):
    """Registra as estruturas de um tipo; quem usa cada uma sai dos tipos das linhas."""
    usos = {n: set() for n in subs}
    for dono, linhas in [("mdt:" + raiz, topo)] + [("mdx:" + n, r) for n, (_, r) in subs.items()]:
        for linha in linhas:
            base = linha[5].get("estrutura") or linha[1].replace("[]", "")
            if base in usos and dono != "mdx:" + base:
                usos[base].add(dono)
    sem_uso = sorted(n for n, u in usos.items() if not u)
    assert not sem_uso, sem_uso
    for n, (o_que_e, linhas) in subs.items():
        M.struct(n, src, sorted(usos[n]), linhas, o_que_e)
    for nome, linhas in [(raiz, topo)] + [(n, r) for n, (_, r) in subs.items()]:
        NOTA_REGISTRO[nome] = (src, linhas)


CONSOLE = "Só vale em apps de console do Salesforce Classic."
HEX = "Cor em código hexadecimal."

# ================================================================ CustomApplication
APP_SUBS = {
    "AppActionOverride": ("Substituição de uma ação (override) válida dentro de um app do Lightning Experience.", [
        P("actionName", S, None, "Ação substituída. Até a API 43.0, só view; tab entrou na 44.0."),
        P("comment", S, None, "Comentário sobre a substituição."),
        P("content", S, None, "Nome da Lightning page usada na substituição, quando type é flexipage. Componentes instalados usam Namespace__Nome."),
        P("formFactor", "FormFactor", "37.0", "Tamanho de página a que a substituição se aplica.", vals=[
            ("Large", "Desktop no Lightning Experience."), ("Small", "App móvel."), ("Medium", "Reservado.")],
          contexto="Nulo corresponde ao Salesforce Classic."),
        P("pageOrSobjectType", S, None, "Objeto da substituição. Precisa ser standard-home quando actionName é tab."),
        P("skipRecordTypeSelect", B, None, "Pula a página de escolha de record type em registros novos. Só para ações de criação do tipo visualforce."),
        P("type", "ActionOverrideType", None, "Tipo da substituição.", "S", vals=valores("Flexipage", "Default")),
    ]),
    "AppBrand": ("Cores e logo de um app do Lightning Experience. Desde a API 38.0.", [
        P("footerColor", S, None, "Cor do rodapé do app. " + HEX), P("headerColor", S, None, "Cor do cabeçalho do app. " + HEX),
        P("logo", S, None, "Referência a um documento de imagem usado como logo do app."),
        P("logoVersion", I, None, "Número de versão do logo."),
        P("shouldOverrideOrgTheme", B, None, "Com true, o app usa a própria cor e o próprio logo; com false, usa o tema da org."),
    ]),
    "AppComponentList": ("Componentes customizados de console (páginas Visualforce) de um app. " + CONSOLE, [
        P("alignment", S, None, "Como os componentes se alinham no rodapé do console.", "S"),
        P("components", "string[]", None, "Nomes dos componentes customizados de console.",
          notas=["Antes da API 42.0, o campo se chamava customApplicationComponent."]),
    ]),
    "AppPreferences": ("Preferências de um app de console do Salesforce Classic. A página diz que todos os campos são obrigatórios. Desde a API 42.0.", [
        P("enableCustomizeMyTabs", B, None, "Deixa o usuário esconder, mostrar e organizar os itens da aba de navegação.", "S"),
        P("enableKeyboardShortcuts", B, None, "Liga os atalhos de teclado.", "S"),
        P("enableListViewHover", B, None, "Mostra o resumo do registro ao passar o mouse sobre um nome numa lista.", "S"),
        P("enableListViewReskin", B, None, "Usa list views responsivas no lugar das do Classic.", "S"),
        P("enableMultiMonitorComponents", B, None, "Deixa o usuário mover partes do console para outras telas.", "S"),
        P("enablePinTabs", B, None, "Deixa o usuário fixar abas primárias na barra de abas.", "S"),
        P("enableTabHover", B, None, "Mostra o resumo do registro ao passar o mouse sobre uma aba.", "S"),
        P("enableTabLimits", B, None, "Limita abas primárias e subabas por sessão. Com true, tabLimitConfig é obrigatório.", "S"),
        P("saveUserSessions", B, None, "Reabre, no próximo login, as abas que estavam abertas.", "S"),
    ]),
    "AppProfileActionOverride": ("Substituição de página de registro (ou da home) por perfil, dentro de um app. Desde a API 39.0.", [
        P("actionName", S, None, "Ação substituída: Tab ou View. View só funciona dentro de um CustomApplication.", "S"),
        P("content", S, None, "Nome da Lightning page usada na substituição. Somente leitura."),
        P("formFactor", "FormFactor", None, "Tamanho de página; Large é o desktop no Lightning Experience.", "S", natureza="desconhecida",
          contexto="A tabela deste subtipo só cita Large; os demais valores de FormFactor estão em AppActionOverride."),
        P("pageOrSobjectType", S, None, "record-home ou standard-home. Precisa ser standard-home quando actionName é Tab.", "S"),
        P("profile", S, None, "Perfil a que a substituição se aplica."),
        P("recordType", S, None, "Record type da substituição. Nulo para standard-home.", "C:obrigatório quando actionName é View"),
        P("type", "ActionOverrideType", None, "Tipo da substituição. Somente leitura.", "S", vals=valores("flexipage"),
          contexto="A página diz que flexipage é o único valor válido aqui."),
    ]),
    "AppWorkspaceConfig": ("Como os registros abrem num app de console. Antes da API 42.0, chamava-se WorkspaceMappings.", [
        P("mappings", "WorkspaceMappingSingle[]", None, "Mapeamento de cada aba do app.", "S", estrutura="WorkspaceMapping",
          notas=["A tabela do campo usa o nome WorkspaceMappingSingle; a seção da página se chama WorkspaceMapping."]),
    ]),
    "WorkspaceMapping": ("Como uma aba abre num app de console: como aba primária ou como subaba de outra.", [
        P("fieldName", S, None, "Campo que define a aba primária sob a qual esta abre como subaba. Sem ele, abre como primária."),
        P("tab", S, None, "Nome da aba.", "S"),
    ]),
    "CustomShortcut": ("Atalho de teclado customizado de console. " + CONSOLE, [
        P("action", S, None, "Ação do console executada pelo atalho.", "S"), P("active", B, None, "Indica se o atalho está ativo.", "S"),
        P("keyCommand", S, None, "Combinação de teclas: até quatro modificadoras (SHIFT, CTRL, ALT, META) e uma tecla comum.", "S"),
        P("description", S, None, "Descrição do atalho."),
        P("eventName", S, None, "Nome do evento usado pelo código que trata o atalho, no Console Integration Toolkit.", "S"),
    ]),
    "DefaultShortcut": ("Atalho de teclado padrão de console. " + CONSOLE, [
        P("action", S, None, "Ação do console executada pelo atalho.", "S", vals=valores(
            "FOCUS_CONSOLE", "FOCUS_NAVIGATOR_TAB", "FOCUS_DETAIL_VIEW", "FOCUS_PRIMARY_TAB_PANEL", "FOCUS_SUBTAB_PANEL", "FOCUS_LIST_VIEW",
            "FOCUS_FIRST_LIST_VIEW", "FOCUS_SEARCH_INPUT", "MOVE_LEFT", "MOVE_RIGHT", "UP_ARROW", "DOWN_ARROW", "OPEN_TAB_SCROLLER_MENU", "OPEN_TAB",
            "CLOSE_TAB", "ENTER", "EDIT", "SAVE"), contexto="A página lista estes valores para um campo do tipo string."),
        P("active", B, None, "Indica se o atalho está ativo.", "S"),
        P("keyCommand", S, None, "Teclas do atalho, unidas por +: até quatro modificadoras e uma tecla comum no fim."),
    ]),
    "KeyboardShortcuts": ("Atalhos de teclado de um app de console. " + CONSOLE, [
        P("customShortcuts", "CustomShortcut[]", None, "Atalhos customizados.", notas=["Antes da API 42.0, o campo se chamava customShortcut."]),
        P("defaultShortcuts", "DefaultShortcut[]", None, "Atalhos padrão, como abrir e fechar abas e salvar.",
          notas=["Antes da API 42.0, o campo se chamava defaultShortcut."]),
    ]),
    "ListPlacement": ("Como as listas aparecem num app de console. " + CONSOLE, [
        P("height", I, None, "Altura da lista, em pixels ou porcentagem.", "C:obrigatório quando location é top"),
        P("location", S, None, "Onde a lista aparece.", "S", vals=valores("full", "top", "left"), contexto="Valores citados na descrição do campo."),
        P("units", S, None, "Indica se altura e largura estão em pixels ou em porcentagem.", "S"),
        P("width", I, None, "Largura da lista, em pixels ou porcentagem.", "C:obrigatório quando location é left"),
    ]),
    "LiveAgentConfig": ("Configurações de Chat de um app de console. " + CONSOLE, [
        P("enableLiveChat", B, None, "Indica se o Chat está ligado na org."),
        P("openNewAccountSubtab", B, None, "Abre uma subaba de Account quando o agente aceita um chat."),
        P("openNewCaseSubtab", B, None, "Abre uma subaba de Case quando o agente aceita um chat."),
        P("openNewContactSubtab", B, None, "Abre uma subaba de Contact quando o agente aceita um chat."),
        P("openNewLeadSubtab", B, None, "Abre uma subaba de Lead quando o agente aceita um chat."),
        P("openNewVFPageSubtab", B, None, "Abre uma subaba com uma página Visualforce quando o agente aceita um chat."),
        P("pageNamesToOpen", "string[]", "42.0", "Páginas Visualforce abertas em subabas quando o agente aceita um chat."),
        P("showKnowledgeArticles", B, None, "Mostra o componente de Knowledge durante o chat."),
    ]),
    "PushNotification": ("Indicador visual de mudança em listas e páginas de detalhe de um app de console. " + CONSOLE, [
        P("fieldNames", "string[]", None, "Campos cuja mudança dispara a notificação."),
        P("objectName", S, None, "Objeto que dispara a notificação.", "S"),
    ]),
    "ServiceCloudConsoleConfig": ("Configurações de um app de console do Salesforce Classic. Desde a API 42.0.", [
        P("componentList", "AppComponentList", None, "Componentes customizados de console do app."),
        P("detailPageRefreshMethod", S, None, "Como a página de detalhe é atualizada.", "C:obrigatório quando isServiceCloudConsole é true",
          vals=valores("none", "autoRefresh", "flag"), contexto="Valores citados na descrição do campo."),
        P("footerColor", S, None, "Cor do rodapé. " + HEX), P("headerColor", S, None, "Cor do cabeçalho. " + HEX),
        P("keyboardShortcuts", "KeyboardShortcuts", None, "Atalhos de teclado do console."),
        P("listPlacement", "ListPlacement", None, "Como as listas aparecem.", "C:obrigatório quando isServiceCloudConsole é true"),
        P("listRefreshMethod", S, None, "Como as listas são atualizadas.", "C:obrigatório quando isServiceCloudConsole é true",
          vals=valores("none", "refreshList", "refreshListRows"), contexto="Valores citados na descrição do campo."),
        P("liveAgentConfig", "LiveAgentConfig", None, "Configurações de Chat do console."),
        P("primaryTabColor", S, None, "Cor da aba primária. " + HEX),
        P("pushNotifications", "PushNotification[]", None, "Indicadores visuais de mudança em listas e páginas de detalhe."),
        P("tabLimitConfig", "TabLimitConfig", None, "Máximo de abas primárias e subabas por sessão.", "C:obrigatório quando enableTabLimits é true"),
        P("whiteListedDomains", "string[]", None, "Domínios externos que os usuários podem acessar de dentro do console."),
    ]),
    "TabLimitConfig": ("Máximo de abas por sessão num app de console. " + CONSOLE, [
        P("maxNumberOfPrimaryTabs", S, None, "Máximo de abas primárias por sessão: 5, 10, 20 ou 30."),
        P("maxNumberOfSubTabs", S, None, "Máximo de subabas por sessão: 5, 10 ou 15."),
    ]),
}
APP = [
    P("actionOverrides", "AppActionOverride[]", "38.0", "Substituições de ações (overrides) válidas neste app do Lightning Experience."),
    P("brand", "AppBrand", "38.0", "Cores e logo do app no Lightning Experience."),
    P("consoleConfig", "ServiceCloudConsoleConfig", "42.0", "Configurações de um app de console do Salesforce Classic."),
    P("defaultLandingTab", S, None, "Nome da aba, padrão ou customizada, que abre quando o app é escolhido."),
    P("description", S, None, "Descrição do app."),
    P("formFactors", "FormFactor", "38.0", "Onde o app aparece.", vals=[
        ("Small", "App móvel; para Lightning apps, desde a API 47.0."), ("Medium", "Reservado."), ("Large", "Desktop no Lightning Experience.")],
      contexto="Nulo corresponde ao desktop no Salesforce Classic."),
    P("isNavAutoTempTabsDisabled", B, "43.0", "Indica se a navegação deixa de criar abas temporárias. Só na navegação padrão de Lightning apps."),
    P("isNavPersonalizationDisabled", B, "43.0", "Indica se a personalização da navegação está desligada. Só em Lightning apps."),
    P("isNavTabPersistenceDisabled", B, "54.0", "Indica se as abas de workspace são limpas a cada sessão. Só na navegação de console do Lightning."),
    P("isServiceCloudConsole", B, None, "Indica se o app é um app de console do Salesforce Classic. Nulo em apps de console do Lightning."),
    P("label", S, None, "Nome do app."),
    P("logo", S, None, "Referência a um documento de imagem do app."),
    P("navType", "NavType", "38.0", "Tipo de navegação do app. Não pode ser alterado depois.", vals=valores("Standard", "Console")),
    P("preferences", "AppPreferences", "42.0", "Preferências de um app de console do Salesforce Classic."),
    P("profileActionOverrides", "AppProfileActionOverride[]", "39.0",
      "Substituições de página de registro por perfil, neste app; têm precedência sobre as demais. Para a home por perfil, desde a API 45.0."),
    P("setupExperience", S, "39.0", "Árvore de Setup mostrada no app.", vals=valores("all", "essentials", "service"),
      contexto="Valores citados na descrição; nulo equivale a all. AllSetup, ServiceSetup e EssentialsSetup estão descontinuados."),
    P("subscriberTabs", "string[]", "41.0", "Abas que o assinante acrescenta a um Lightning app de pacote gerenciado."),
    P("tabs", "string[]", None, "Abas incluídas no app. Abas padrão usam o prefixo standard-.",
      notas=["Antes da API 42.0, o campo se chamava tab."]),
    P("uiBundle", "string[]", "67.0", "Nome de um app React interno (UIBundle), que passa a aparecer no App Launcher."),
    P("uiType", "UiType", "38.0", "Tipo do app. Não pode ser alterado depois.", vals=[("Aloha", "Salesforce Classic."), ("Lightning", "Lightning Experience.")]),
    P("utilityBar", S, "38.0", "Developer name da utility bar ligada ao app."),
    P("workspaceConfig", "AppWorkspaceConfig", None, "Como os registros abrem num app de console.",
      "C:ligado a isServiceCloudConsole, segundo a página"),
    FULLNAME,
]
conjunto("CustomApplication", S_APP, APP, APP_SUBS)
M.mdt("CustomApplication", S_APP,
      "Um app: o conjunto de abas e itens de navegação que o usuário abre pelo App Launcher, com nome, marca, tipo de navegação e, no "
      "console, as opções de abas e atalhos.",
      "Versionar e implantar os apps da org, tanto os do Lightning Experience quanto os do Salesforce Classic.", "10.0", APP,
      exemplo=CAB + f"""<CustomApplication {NS}>
    <brand>
        <headerColor>[cor em hexadecimal]</headerColor>
        <shouldOverrideOrgTheme>false</shouldOverrideOrgTheme>
    </brand>
    <formFactors>Large</formFactors>
    <label>[nome do app]</label>
    <!-- Valores documentados: Standard, Console. Não pode ser alterado depois -->
    <navType>Standard</navType>
    <tabs>standard-Account</tabs>
    <tabs>[Nome_Da_Aba__c]</tabs>
    <!-- Valores documentados: Aloha (Classic), Lightning -->
    <uiType>Lightning</uiType>
</CustomApplication>""", curinga=True,
      alertas=["navType e uiType não podem ser alterados depois de criado o app.",
               "Recuperar o app faz com que ele apareça também nos componentes Profile e PermissionSet recuperados no mesmo pacote.",
               "Apps padrão têm suporte desde a API 30.0 e usam o prefixo standard__ no package.xml.",
               "Uma substituição do tipo flexipage que é o padrão do app não pode ser excluída pela Metadata API."],
      cobertura_nota=NOTA_COB + SEM_REQ)

# ================================================================ Layout
PX = "em pixels ou em porcentagem, conforme a unidade"
LAY_SUBS = {
    "CustomConsoleComponents": ("Componentes de console de um layout (Visualforce, lookups, related lists). Só no console.", [
        P("primaryTabComponents", "PrimaryTabComponents", "25.0", "Componentes de console nas abas primárias."),
        P("subtabComponents", "SubtabComponents", "25.0", "Componentes de console nas subabas."),
    ]),
    "PrimaryTabComponents": ("Componentes de console das abas primárias.", [
        P("component", "ConsoleComponent[]", None, "Componentes de console de uma seção.", ate="29.0", estrutura="ConsoleComponent",
          notas=["A página informa que o campo vale até a API 29.0."]),
        P("containers", "Container[]", "30.0", "Local e estilo de um conjunto de componentes de barra lateral.", estrutura="Container"),
    ]),
    "SubtabComponents": ("Componentes de console das subabas.", [
        P("component", "ConsoleComponent[]", None, "Componentes de console de uma seção.", ate="29.0", estrutura="ConsoleComponent",
          notas=["A página informa que o campo vale até a API 29.0."]),
        P("containers", "Container[]", "30.0", "Local e estilo de um conjunto de componentes de barra lateral.", estrutura="Container"),
    ]),
    "ConsoleComponent": ("Um componente de console (página Visualforce) num layout.", [
        P("height", I, None, "Altura em pixels, maior que 0 e menor que 999.", "C:quando location é top ou bottom"),
        P("location", S, None, "Posição do componente; uma por layout.", "S", vals=valores("right", "left", "top", "bottom"),
          contexto="Valores citados na descrição do campo."),
        P("visualforcePage", S, None, "Nome único da página Visualforce usada como componente.", "S"),
        P("width", I, None, "Largura em pixels, maior que 0 e menor que 999.", "C:quando location é left ou right"),
    ]),
    "Container": ("Área de um layout de console que agrupa componentes de barra lateral. Desde a API 30.0.", [
        P("height", I, None, f"Altura da área, {PX}.", "C:quando region é top ou bottom"),
        P("isContainerAutoSizeEnabled", B, "32.0", "Indica se os componentes empilhados se ajustam na vertical.", "S"),
        P("region", S, None, "Posição da área.", "S", vals=valores("right", "left", "top", "bottom"), contexto="Valores citados na descrição do campo."),
        P("sidebarComponents", "SidebarComponent[]", None, "Componentes mostrados na área."),
        P("style", S, None, "Como os componentes se organizam: empilhados, em abas ou em sanfona.", "S", vals=valores("stack", "tabs", "accordian"),
          contexto="Valores citados na descrição do campo, com a grafia da página."),
        P("unit", S, None, "Unidade de altura e largura: pixels (1 a 998) ou porcentagem (1 a 99).", "S"),
        P("width", I, None, f"Largura da área, {PX}.", "C:quando region é left ou right"),
    ]),
    "SidebarComponent": ("Um componente de barra lateral num layout de console. Desde a API 30.0.", [
        P("componentType", S, "31.0", "Tipo do componente.", vals=[
            ("KnowledgeOne", None), ("Lookup", None), ("Milestones", None), ("RelatedList", None), ("Topics", None),
            ("Files", "Desde a API 32.0."), ("CaseExperts", "Desde a API 32.0.")], contexto="Valores citados na descrição do campo."),
        P("createAction", S, "42.0", "Quick action usada para criar um registro num lookup."),
        P("enableLinking", B, "42.0", "Deixa o usuário ligar um registro a um lookup."),
        P("height", I, None, f"Altura do componente, {PX}.", "C:quando a área fica em top ou bottom"),
        P("label", S, None, "Nome mostrado ao usuário do console, em áreas em abas ou em sanfona."),
        P("lookup", S, None, "Nome do campo, quando o componente é um lookup."),
        P("page", S, None, "Nome da página Visualforce, quando o componente é uma página."),
        P("relatedlists", "RelatedList[]", "31.0", "Related list, quando o componente é uma related list.", estrutura="RelatedList"),
        P("unit", S, None, "Unidade de altura e largura: pixels (1 a 998) ou porcentagem (1 a 99)."),
        P("updateAction", S, "42.0", "Quick action usada para atualizar o registro de um lookup."),
        P("width", I, None, f"Largura do componente, {PX}.", "C:quando a área fica em left ou right"),
    ]),
    "RelatedList": ("Uma related list usada como componente de console. Desde a API 31.0.", [
        P("hideOnDetail", B, None, "Esconde a lista nas páginas de detalhe em que ela já aparece como componente, para não duplicar."),
        P("name", S, None, "Nome mostrado ao usuário do console."),
    ]),
    "FeedLayout": ("Configuração da visão de feed em layouts baseados em feed. Desde a API 30.0.", [
        P("autocollapsePublisher", B, None, "Com true, o publisher vem recolhido quando a página carrega."),
        P("compactFeed", B, None, "Com true, usa o feed compacto, com itens recolhidos por padrão."),
        P("feedFilterPosition", "FeedLayoutFilterPosition", None, "Onde ficam os filtros do feed.",
          vals=valores("centerDropDown", "leftFixed", "leftFloat")),
        P("feedFilters", "FeedLayoutFilter[]", None, "Filtros da lista de filtros do feed."),
        P("fullWidthFeed", B, None, "Com true, o feed ocupa a largura toda da página."),
        P("hideSidebar", B, None, "Com true, esconde a barra lateral."),
        P("leftComponents", "FeedLayoutComponent[]", None, "Componentes da coluna esquerda da visão de feed."),
        P("rightComponents", "FeedLayoutComponent[]", None, "Componentes da coluna direita da visão de feed."),
    ]),
    "FeedLayoutComponent": ("Um componente numa coluna da visão de feed. Desde a API 30.0.", [
        P("componentType", "FeedLayoutComponentType", None, "Tipo do componente.", "S", vals=[
            ("HelpAndToolLinks", "Só em Case."), ("CustomButtons", None), ("Following", None), ("Followers", None), ("CustomLinks", None),
            ("Milestones", "Só em Case."), ("Topics", None), ("CaseUnifiedFiles", None), ("Visualforce", None)]),
        P("height", I, None, "Altura em pixels. Não se aplica a componentes padrão."),
        P("page", S, None, "Página Visualforce usada como componente customizado."),
    ]),
    "FeedLayoutFilter": ("Um filtro da visão de feed. Desde a API 30.0.", [
        P("feedFilterName", S, None, "Nome de um CustomFeedFilter, com o objeto pai como prefixo (por exemplo Case.MeuFiltro)."),
        P("feedFilterType", "FeedLayoutFilterType", None, "Tipo do filtro.", vals=[
            ("AllUpdates", "Todos os itens de feed."), ("FeedItemType", "Um só tipo de atividade.")]),
        P("feedItemType", "FeedItemType", None, "Tipo de atividade mostrado pelo filtro.", natureza="desconhecida",
          contexto="A página lista 29 valores, vários só para Case ou fora de uso; não foram transcritos um a um."),
    ]),
    "MiniLayout": ("A visão resumida de um registro, usada na aba de console, nos detalhes ao passar o mouse e em eventos.", [
        P("fields", "string[]", None, "Campos da visão resumida, na ordem da tela. Cada um precisa estar também no layout principal."),
        P("relatedLists", "RelatedListItem[]", None, "Related lists da visão resumida, na ordem da tela. Cada uma precisa estar no layout principal."),
    ]),
    "LayoutSection": ("Uma seção do layout, com seus campos, s-controls e links customizados.", [
        P("customLabel", B, None, "Com true, o rótulo é customizado (e traduzível); com false, é um rótulo padrão."),
        P("detailHeading", B, None, "Mostra o título da seção na página de detalhe."),
        P("editHeading", B, None, "Mostra o título da seção na página de edição."),
        P("label", S, None, "Rótulo da seção."),
        P("layoutColumns", "LayoutColumn[]", None, "Colunas da seção, da esquerda para a direita; pode haver 1, 2 ou 3."),
        P("style", "LayoutSectionStyle", None, "Estilo da seção.", vals=[
            ("TwoColumnsTopToBottom", None), ("TwoColumnsLeftToRight", None), ("OneColumn", None), ("CustomLinks", "Só para links customizados.")]),
    ]),
    "LayoutColumn": ("Uma coluna de uma seção do layout.", [
        P("layoutItems", "LayoutItem[]", None, "Itens da coluna, de cima para baixo."),
        P("reserved", S, None, "Reservado para a Salesforce; qualquer valor é ignorado."),
    ]),
    "LayoutItem": ("Um item do layout. Cada item traz um só destes: component, customLink, field, scontrol, page, analyticsCloudComponent ou "
                   "reportChartComponent.", [
        P("behavior", "UiBehavior", None, "Comportamento do campo neste layout.", vals=[
            ("Edit", "Editável e opcional."), ("Required", "Editável e obrigatório."), ("Readonly", "Somente leitura.")]),
        P("canvas", S, "31.0", "Referência a um canvas app."),
        P("component", S, "30.0", "Precisa ser sfa:socialCard. Só dentro de RelatedContentItem, em layouts de contact, account e lead."),
        P("customLink", S, None, "Referência a um link customizado. Só em seções do estilo CustomLinks."),
        P("emptySpace", B, None, "Marca o item como um espaço em branco."),
        P("field", S, None, "Nome do campo, relativo ao objeto do layout (por exemplo Description ou MeuCampo__c)."),
        P("height", I, None, "Altura em pixels. Só para s-controls e páginas."),
        P("page", S, None, "Referência a uma página Visualforce."),
        P("analyticsCloudComponent", "AnalyticsCloudComponentLayoutItem", "34.0", "Dashboard do CRM Analytics colocado na página do objeto."),
        P("reportChartComponent", "ReportChartComponentLayoutItem", None, "Gráfico de relatório colocado na página do objeto."),
        P("scontrol", S, None, "Referência a um s-control."),
        P("showLabel", B, None, "Mostra o rótulo. Só para s-controls e páginas."),
        P("showScrollbars", B, None, "Mostra barras de rolagem. Só para s-controls e páginas."),
        P("width", S, None, "Largura em pixels ou em porcentagem (por exemplo 500 ou 20%)."),
    ]),
    "AnalyticsCloudComponentLayoutItem": ("Um dashboard do CRM Analytics colocado num layout.", [
        P("assetType", S, None, "Tipo do recurso. Só dashboard está disponível.", "S"),
        P("devName", S, None, "Nome único de desenvolvimento do dashboard.", "S"),
        P("error", S, None, "Texto do erro; preenchido só quando o dashboard dá erro."),
        P("filter", S, None, "Filtros iniciais, que ligam os dados do dashboard aos campos do objeto."),
        P("height", I, None, "Altura do dashboard em pixels.", default=("valor", "400", None)),
        P("hideOnError", B, None, "Com true, esconde o dashboard quando há erro.", default=("valor", "true", None)),
        P("showSharing", B, "37.0", "Mostra o ícone de compartilhar, se o dashboard pode ser compartilhado."),
        P("showTitle", B, None, "Mostra o título do dashboard acima dele.", default=("valor", "true", None)),
        P("width", S, None, "Largura em pixels ou em porcentagem.", default=("valor", "100%", None)),
    ]),
    "ReportChartComponentLayoutItem": ("Um gráfico de relatório colocado num layout.", [
        P("cacheData", B, "29.0", "Com true, guarda os dados do gráfico em cache por 24 horas."),
        P("contextFilterableField", S, None, "Campo usado para filtrar os dados do gráfico pelo registro da página."),
        P("error", S, "31.0", "Texto do erro, quando o relatório do gráfico falha."),
        P("hideOnError", B, "29.0", "Com true, esconde o gráfico quando há erro."),
        P("includeContext", B, None, "Filtra o gráfico para os dados relevantes à página."),
        P("reportName", S, None, "Nome de desenvolvimento de um relatório que tem gráfico."),
        P("showTitle", B, None, "Aplica o título do relatório ao gráfico."),
        P("size", "ReportChartComponentSize", None, "Tamanho do gráfico; médio quando não informado.", vals=valores("SMALL", "MEDIUM", "LARGE")),
    ]),
    "PlatformActionList": ("As ações e a ordem delas na barra de ações do app móvel. Desde a API 34.0.", [
        P("actionListContext", "PlatformActionListContext", None, "Contexto da lista de ações, como Record, Chatter ou Global.", "S",
          natureza="desconhecida", contexto="A página lista 19 valores; não foram transcritos um a um."),
        P("platformActionListItems", "PlatformActionListItem[]", None, "Ações da lista."),
        P("relatedSourceEntity", S, None, "Nome de API da related list, quando o contexto é RelatedList ou RelatedListRecord."),
    ]),
    "PlatformActionListItem": ("Uma ação da barra de ações.", [
        P("actionName", S, None, "Nome de API da ação."),
        P("actionType", "PlatformActionType", None, "Tipo da ação.", vals=valores(
            "ActionLink", "CustomButton", "InvocableAction", "ProductivityAction", "QuickAction", "StandardButton")),
        P("sortOrder", I, None, "Posição da ação na lista."),
        P("subtype", S, None, "Subtipo, que depende do tipo; botões padrão e ações de produtividade não têm."),
    ]),
    "QuickActionList": ("As quick actions mostradas no layout. Desde a API 28.0.", [
        P("quickActionListItems", "QuickActionListItem[]", None, "Itens da lista de quick actions; pode ser vazia."),
    ]),
    "QuickActionListItem": ("Uma quick action do layout. Desde a API 28.0.", [P("quickActionName", S, None, "Nome de API da ação.")]),
    "RelatedContent": ("A seção Related Content (Mobile Cards) do layout. Desde a API 29.0.", [
        P("relatedContentItems", "RelatedContentItem[]", None, "Itens da seção Mobile Cards."),
    ]),
    "RelatedContentItem": ("Um item da seção Mobile Cards. Desde a API 29.0.", [P("layoutItem", "LayoutItem", None, "O item de layout mostrado.")]),
    "RelatedListItem": ("Uma related list do layout.", [
        P("customButtons", "string[]", None, "Botões customizados usados na related list."),
        P("excludeButtons", "string[]", None, "Botões escondidos da related list."),
        P("fields", "string[]", None, "Campos mostrados; alguns usam apelidos, como Phone2 a Phone4."),
        P("quickActions", "string[]", None, "Quick actions usadas na related list."),
        P("relatedList", S, None, "Nome da related list.", "S"),
        P("sortField", S, None, "Campo usado para ordenar."),
        P("sortOrder", "SortOrder", None, "Ordem; vale quando sortField está definido.", vals=valores("Asc", "Desc")),
    ]),
    "SummaryLayout": ("A grade do highlights panel no Salesforce Classic, quando o Case Feed está ligado. Desde a API 25.0.", [
        P("masterLabel", S, None, "Nome do rótulo do layout.", "S"),
        P("sizeX", I, None, "Colunas do painel, de 1 a 4.", "S"), P("sizeY", I, None, "Linhas por coluna, 1 ou 2.", "S"),
        P("sizeZ", I, None, "Reservado para uso futuro."),
        P("summaryLayoutItems", "SummaryLayoutItem[]", None, "Posição de cada campo; é preciso ao menos um."),
        P("summaryLayoutStyle", "SummaryLayoutStyle", None, "Estilo do painel.", vals=valores(
            "Default", "QuoteTemplate", "DefaultQuoteTemplate", "CaseInteraction", "QuickActionLayoutLeftRight", "QuickActionLayoutTopDown"),
          natureza="desconhecida", contexto="A leitura resumiu os valores de quick action (API 28.0 ou posterior) sem transcrever os nomes exatos."),
    ]),
    "SummaryLayoutItem": ("Um campo ou link do highlights panel. Desde a API 25.0.", [
        P("customLink", S, None, "Referência a um link customizado, quando o item é um link."),
        P("field", S, None, "Nome do campo; precisa existir também na página de detalhe."),
        P("posX", I, None, "Coluna do item; precisa caber em sizeX.", "S"), P("posY", I, None, "Linha do item; precisa caber em sizeY.", "S"),
        P("posZ", I, None, "Reservado para uso futuro."),
    ]),
}
# summaryLayoutStyle: os nomes dos valores de quick action não foram lidos; o campo fica sem lista.
LAY_SUBS["SummaryLayout"][1][-1] = P(
    "summaryLayoutStyle", "SummaryLayoutStyle", None, "Estilo do painel: padrão, de template de cotação, de interação de caso ou de quick action.",
    natureza="desconhecida", contexto="A leitura não transcreveu os nomes exatos dos valores (os de quick action entram na API 28.0).")
LAY = [
    P("customButtons", "string[]", None, "Botões customizados do layout; cada um referencia um WebLink do mesmo objeto."),
    P("customConsoleComponents", "CustomConsoleComponents", None, "Componentes de console do layout. Só no console."),
    P("emailDefault", B, None, "Estado inicial da caixa de e-mail. Só vale com showEmailCheckbox."),
    P("excludeButtons", "string[]", None, "Botões padrão escondidos do layout, como Delete."),
    P("feedLayout", "FeedLayout", None, "Configuração da visão de feed, em layouts baseados em feed."),
    P("headers", "LayoutHeader[]", None, "Cabeçalhos de tagging do layout.", vals=[
        ("PersonalTagging", "Tags pessoais, privadas."), ("PublicTagging", "Tags visíveis a quem tem acesso ao registro.")]),
    P("layoutSections", "LayoutSection[]", None, "Seções principais do layout, com campos, s-controls e links; a ordem define a tela."),
    P("miniLayout", "MiniLayout", None, "Visão resumida do registro, usada no console, nos detalhes ao passar o mouse e em eventos."),
    P("multilineLayoutFields", "string[]", None, "Campos multilinha especiais dos layouts de OpportunityProduct."),
    P("platformActionList", "PlatformActionList", "34.0", "Ações e ordem delas na barra de ações do app móvel."),
    P("quickActionList", "QuickActionList", "28.0", "Quick actions mostradas no layout, no site completo."),
    P("relatedContent", "RelatedContent", "29.0", "Seção Related Content do layout."),
    P("relatedLists", "RelatedListItem[]", None, "Related lists do layout, na ordem da tela."),
    P("relatedObjects", "string[]", None, "Objetos relacionados mostrados na visão resumida do console."),
    P("runAssignmentRulesDefault", B, None, "Estado inicial da caixa de regras de atribuição. Só vale com showRunAssignmentRulesCheckbox."),
    P("showEmailCheckbox", B, None, "Mostra a caixa de e-mail. Só em layouts de Case, CaseClose e Task."),
    P("showHighlightsPanel", B, "22.0", "Mostra o highlights panel nas páginas de console."),
    P("showInteractionLogPanel", B, "22.0", "Mostra o interaction log nas páginas de console."),
    P("showKnowledgeComponent", B, "20.0", "Mostra a barra lateral de Knowledge em casos no console. Só em layouts de Case."),
    P("showRunAssignmentRulesCheckbox", B, None, "Mostra a caixa de regras de atribuição. Só em Case, Lead e Account."),
    P("showSolutionSection", B, None, "Mostra a seção de solução. Só no layout CaseClose."),
    P("showSubmitAndAttachButton", B, None, "Mostra o botão Submit & Add Attachment a usuários de portal. Só no layout de Case."),
    P("summaryLayout", "SummaryLayout", "18.0", "Grade do highlights panel no Salesforce Classic, com o Case Feed ligado."),
    FULLNAME,
]
conjunto("Layout", S_LAY, LAY, LAY_SUBS)
M.mdt("Layout", S_LAY,
      "Um page layout: as seções, os campos, os botões, as quick actions e as related lists que aparecem na página de um registro.",
      "Versionar e implantar os page layouts de cada objeto.", "13.0", LAY,
      exemplo=CAB + f"""<Layout {NS}>
    <layoutSections>
        <customLabel>false</customLabel>
        <detailHeading>true</detailHeading>
        <editHeading>true</editHeading>
        <label>[rótulo da seção]</label>
        <!-- Valores documentados: TwoColumnsTopToBottom, TwoColumnsLeftToRight, OneColumn, CustomLinks -->
        <style>TwoColumnsTopToBottom</style>
    </layoutSections>
    <quickActionList>
        <!-- Cada item traz o nome de API de uma quick action, em quickActionName -->
    </quickActionList>
    <relatedLists>
        <relatedList>[nome da related list]</relatedList>
    </relatedLists>
</Layout>""", curinga=True, completa=False,
      alertas=["O highlights panel do Lightning Experience não é configurado aqui: os campos dele vêm do compact layout.",
               "Recuperar o layout faz com que ele apareça também nos componentes Profile e PermissionSet recuperados no mesmo pacote.",
               "Em páginas de registro com Dynamic Forms, os campos vêm da Lightning page, não do page layout.",
               "Cada item de layout traz um só conteúdo: campo, link, s-control, página, componente, dashboard ou gráfico."],
      divergencias=["O exemplo XML da página usa os elementos miniLayoutFields e miniRelatedLists, que não constam das tabelas de campos; "
                    "a tabela documenta miniLayout, com fields e relatedLists. Os dois elementos não foram cadastrados.",
                    "A descrição de FeedLayoutFilter cita um valor standardFilter que não aparece na tabela do subtipo."],
      cobertura_nota=NOTA_COB + SEM_REQ + " Primeiro nível: 24 de 24 campos. Parcial: três enumerações (FeedItemType, PlatformActionListContext e "
                     "SummaryLayoutStyle) não tiveram os valores transcritos.")

# ================================================================ CompactLayout, tema e branding
M.mdt("CompactLayout", S_CL,
      "Um compact layout: a lista ordenada dos campos-chave de um registro, mostrada no highlights panel e no app móvel.",
      "Versionar e implantar os compact layouts de um objeto, junto com a definição do objeto.", "29.0", [
          P("fields", "string[]", None, "Campos do compact layout; a ordem define a prioridade de exibição.",
            notas=["A tabela da página tipa o campo como string; o exemplo repete o elemento, um por campo."]),
          P("label", S, None, "Rótulo do compact layout."),
          FULLNAME,
      ], parent="CustomObject", exemplo=CAB + f"""<!-- No arquivo .object do objeto, este conteúdo fica no elemento <compactLayouts> -->
<CompactLayout {NS}>
    <fullName>[Nome_Do_Compact_Layout]</fullName>
    <fields>Name</fields>
    <fields>[Outro_Campo__c]</fields>
    <label>[rótulo]</label>
</CompactLayout>""", arquivos_prontos=M.arquivos("CompactLayout", "CustomObject"), curinga=True,
      alertas=["Aceita todos os tipos de campo, exceto text area, long text area, rich text area e multi-select picklist.",
               "O compact layout é independente do page layout: tirar um campo de um não o tira do outro.",
               "Para external objects, o tipo existe desde a API 42.0."],
      cobertura_nota=NOTA_COB + SEM_REQ)
d = ld("metadata-types/CompactLayout.json")
if not any(e["fonte"] == "src:help-layout-considerations" for e in d["evidencias"]):
    d["evidencias"].append(ev("src:help-layout-considerations", "Independência entre page layout e compact layout."))
sv("metadata-types/CompactLayout.json", d)

M.mdt("LightningExperienceTheme", S_THEME,
      "Um tema customizado do Lightning Experience: o nome, a versão do design system e o conjunto de cores e imagens (BrandingSet) que ele aplica.",
      "Versionar e implantar a identidade visual da org no Lightning Experience.", "42.0", [
          P("defaultBrandingSet", S, None, "Identificador do BrandingSet cujas propriedades valem para o tema.", "S"),
          P("description", S, None, "Texto descritivo, com até 1000 caracteres."),
          P("designSystemVersion", "LightningDesignSystemVersion", "64.0", "Versão do Salesforce Lightning Design System em que o tema se baseia.",
            default=("valor", "SLDS_v1", None), vals=valores("SLDS_v1", "SLDS_v2")),
          P("isDarkModeEnabled", B, "65.0", "Indica se os usuários podem ligar o dark mode. Para temas customizados de SLDS 2, em edições selecionadas.",
            default=("false", False, "A página declara default false.")),
          P("masterLabel", S, None, "Rótulo mostrado no Setup, com até 70 caracteres.", "S"),
          P("shouldOverrideLoadingImage", B, None, "Com true, o tema troca a imagem da tela de carregamento."),
      ], exemplo=CAB + f"""<LightningExperienceTheme {NS}>
    <defaultBrandingSet>[nome do BrandingSet do tema]</defaultBrandingSet>
    <description>[descrição do tema]</description>
    <masterLabel>[rótulo do tema]</masterLabel>
    <shouldOverrideLoadingImage>false</shouldOverrideLoadingImage>
</LightningExperienceTheme>""", estende="não declarado na página", curinga=True,
      alertas=["O tema só passa a valer quando é ativado: pela Metadata API, isso é feito em LightningExperienceSettings, não neste tipo.",
               "As cores e imagens ficam no BrandingSet referenciado; implante os dois juntos.",
               "A página informa acesso especial: o tipo fica disponível quando a permissão S1DesktopAllowed está ligada na org."],
      cobertura_nota=NOTA_COB)

M.struct("BrandingSetProperty", S_BRAND, ["mdt:BrandingSet"], [
    P("propertyName", S, None, "Nome da propriedade de marca, como TextColor ou BRAND_COLOR. Nos temas do Lightning Experience, o nome é todo em "
      "maiúsculas e diferencia maiúsculas de minúsculas.", "S"),
    P("propertyValue", S, None, "Valor da propriedade, como #333."),
], "Um par de nome e valor de uma propriedade de marca.")
NOTA_REGISTRO["BrandingSetProperty"] = (S_BRAND, [("propertyName",), ("propertyValue",)])
M.mdt("BrandingSet", S_BRAND,
      "Um conjunto de propriedades de marca (cores e imagens), usado por temas do Lightning Experience, sites do Experience Cloud e Surveys.",
      "Versionar e implantar as cores e imagens da identidade visual.", "40.0", [
          P("brandingSetProperty", "BrandingSetProperty[]", None, "Pares de nome e valor, um por propriedade de marca.", estrutura="BrandingSetProperty"),
          P("description", S, None, "Descrição do conjunto de propriedades."),
          P("masterLabel", S, None, "Nome do conjunto na interface.", "S"),
          P("type", S, None, "Definição de branding set atribuída a este conjunto."),
          FULLNAME,
      ], exemplo=CAB + f"""<BrandingSet {NS}>
    <brandingSetProperty>
        <!-- Em temas do Lightning Experience, os nomes são em maiúsculas -->
        <propertyName>BRAND_COLOR</propertyName>
        <propertyValue>[cor em hexadecimal]</propertyValue>
    </brandingSetProperty>
    <masterLabel>[nome do conjunto]</masterLabel>
</BrandingSet>""", curinga=True,
      alertas=["A página lista 34 nomes de propriedade para temas do Lightning Experience; parte vale só para temas SLDS 1 e parte só para SLDS 2.",
               "Propriedades de imagem precisam apontar para asset files que já existem na org.",
               "A página informa que todos os usuários, inclusive guest não autenticados, acessam o tipo."],
      cobertura_nota=NOTA_COB + " Os 34 nomes de propriedade de tema são valores de propertyName, não campos; não foram cadastrados um a um.")

M.emit_structs()

# ================================================================ nota de extração: lista de campos
for _n, _s in (("CompactLayout", S_CL), ("LightningExperienceTheme", S_THEME), ("BrandingSet", S_BRAND)):
    NOTA_REGISTRO[_n] = (_s, [(q["nome"],) for q in ld(f"metadata-types/{_n}.json")["propriedades"]])
if "--nota" in sys.argv:
    linhas = ["", "-- Lista de campos transcrita da leitura (gerada por lote7d_interface.py --nota; nome | tipo | desde | obrigatoriedade)"]
    for nome, (src, rows) in NOTA_REGISTRO.items():
        campos = ", ".join(" | ".join(str(x) for x in (r[0], r[1], r[3] or "-", r[2])) if len(r) > 1 else r[0] for r in rows)
        linhas.append(f"[{src}] {nome}: {campos}")
    p = caminho(EXTR)
    t = open(p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
    open(p, "w", encoding="utf-8").write(t + "\n" + "\n".join(linhas) + "\n")

# ================================================================ funcionalidades
UI = "interface-e-experiencia-do-usuario"
SEM_OBJ = {"tipo": "objeto_api", "estado": "desconhecido",
           "motivo": "Objetos API do tema não investigados na rodada A3; a lista vazia não comprova inexistência."}


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


C.funcionalidade(
    "lightning-apps", "Lightning apps", "Lightning Apps", ["lightning app", "app manager", "app launcher", "navigation bar", "utility bar", "app"],
    "Um app é um conjunto de itens que trabalham juntos para uma função: abas de objetos, páginas e utilitários, com nome, logo e cor "
    "próprios. O usuário troca de app pelo App Launcher.",
    "Dar a cada área da empresa a navegação de que ela precisa, sem mostrar o que não usa.",
    "O app Financeiro mostra as abas Contas, Faturas e Relatórios, tem a cor da área e fica disponível só para os perfis do financeiro.",
    (UI, "aplicativos-e-navegacao"), [],
    [("CustomApplication", "Cada app, com abas, marca, tipo de navegação e substituições de página.")], [],
    [S_APP, "src:help-lightning-apps-create", "src:help-build-app", "src:help-app-builder-apps", "src:help-utility-bar"], [SEM_OBJ],
    setup("Setup > Quick Find: App > App Manager", "src:help-lightning-apps-create", "Lista dos apps; o botão New Lightning App abre o assistente."),
    alertas=["O tipo de navegação (padrão ou console) é escolhido na criação e não pode ser alterado depois.",
             "Uma utility bar só com itens de segundo plano não aparece: é preciso ao menos um item visível."])
C.ampliar_funcionalidade("apps-de-console", mdts=[("CustomApplication", "O app de console, com navType Console e as opções de abas.")], srcs=[S_APP])

C.funcionalidade(
    "page-layouts", "Page layouts", "Page Layouts", ["page layout", "layout de página", "page layout editor", "related lists", "layout"],
    "O page layout define quais campos, seções, botões, quick actions e related lists aparecem na página de um registro, e se cada campo "
    "é editável, obrigatório ou somente leitura naquela página.",
    "Organizar a página de registro de cada objeto, com variações por perfil e por record type.",
    "No layout de Conta do time de vendas, o campo Segmento é obrigatório e a related list de Oportunidades vem antes da de Casos.",
    (UI, "layouts-e-paginas-de-registro"), [],
    [("Layout", "Cada page layout, com seções, itens, ações e related lists.")], [],
    [S_LAY, "src:help-layouts-lex", "src:help-layout-considerations", "src:help-dynamic-forms"], [SEM_OBJ],
    af("desconhecido", None, "Caminho de Setup não confirmado nas fontes lidas.", []),
    limitacoes=["Mudanças de layout podem levar cerca de 15 minutos para aparecer no Lightning Experience, e até uma hora para outros usuários."],
    alertas=["O highlights panel não é configurado pelo page layout: os campos dele vêm do compact layout.",
             "Em páginas com Dynamic Forms, os campos vistos ao criar, editar ou clonar vêm da Lightning page, não do page layout.",
             "Tirar um campo do layout não é controle de acesso: quem decide é a segurança em nível de campo."])

C.funcionalidade(
    "compact-layouts", "Compact layouts", "Compact Layouts", ["compact layout", "highlights panel", "campos-chave"],
    "O compact layout lista os campos-chave de um registro, mostrados de relance no highlights panel do Lightning Experience, no app "
    "móvel e nas integrações com Outlook e Gmail.",
    "Pôr no topo do registro a informação que o usuário mais procura.",
    "No compact layout de Oportunidade ficam Nome, Valor, Data de fechamento e Fase; são eles que aparecem no topo da página.",
    (UI, "layouts-e-paginas-de-registro"), [],
    [("CompactLayout", "Cada compact layout, definido junto com o objeto.")], [],
    [S_CL, "src:help-compact-layouts", "src:help-compact-layout-notes", "src:help-compact-layout-create", "src:help-lightning-std-components"], [SEM_OBJ],
    af("desconhecido", None, "A Ajuda indica as configurações de gerenciamento do objeto, seção Compact Layouts; o caminho completo de Setup não foi lido.", []),
    limitacoes=["Até 10 campos por compact layout; o highlights panel do Lightning Experience usa os sete primeiros.",
                "Cada record type tem um só compact layout atribuído; compact layouts não são atribuídos a perfis nem a usuários."],
    alertas=["Não aceita campos text area, long text area, rich text area nem multi-select picklist."])

C.funcionalidade(
    "dynamic-forms", "Dynamic Forms", "Dynamic Forms", ["dynamic form", "field section", "dynamic highlights panel", "visibility rules"],
    "Com Dynamic Forms, os campos e as seções saem do page layout e viram componentes individuais na Lightning page: podem ser postos em "
    "colunas e abas, e mostrados ou escondidos por regras de visibilidade.",
    "Mostrar a cada usuário só os campos que fazem sentido naquele momento, sem criar vários page layouts.",
    "Na página de Caso, a seção Reembolso só aparece quando o tipo do caso é Devolução.",
    (UI, "layouts-e-paginas-de-registro"), [(UI, "lightning-pages-e-componentes", "Os campos passam a ser componentes da Lightning page.")],
    [("FlexiPage", "A Lightning page que passa a conter os campos e as seções.")], [],
    ["src:help-dynamic-forms", "src:help-lightning-std-components", "src:help-rn-dynamic-highlights", "src:architect-build-forms", "src:mdapi-flexipage"],
    [SEM_OBJ], af("desconhecido", None, "A configuração é feita no Lightning App Builder; o caminho de Setup não foi lido.", []),
    limitacoes=["Até 100 campos por região da página; um espaço em branco conta como campo.",
                "O Dynamic Highlights Panel aceita até 12 campos.",
                "Segundo o guia de decisão de formulários, não está disponível em páginas do Experience Cloud."],
    alertas=["Em páginas com Dynamic Forms, os campos de criar, editar e clonar vêm da página, não do page layout."])

C.funcionalidade(
    "temas-e-branding", "Temas e branding", "Themes and Branding", ["theme", "tema", "branding", "dark mode", "slds", "salesforce cosmos", "density"],
    "Um tema é o conjunto de estilos visuais da interface: cores, logo e imagens. A org usa um tema pronto da Salesforce ou um tema "
    "customizado com a própria marca. Cada usuário ainda escolhe a densidade da tela e, se o tema permitir, o dark mode.",
    "Dar à org a identidade visual da empresa e deixar cada pessoa ajustar a leitura da tela.",
    "A org ativa um tema com o logo e a cor da empresa; uma usuária prefere a densidade Compact e o dark mode.",
    (UI, "acessibilidade-e-personalizacao"), [],
    [("LightningExperienceTheme", "Cada tema customizado."), ("BrandingSet", "As cores e imagens que o tema aplica.")], [],
    [S_THEME, S_BRAND, "src:help-themes", "src:help-rn-dark-mode", "src:help-personalize-display"], [SEM_OBJ],
    setup("Setup > Quick Find: Themes and Branding", "src:help-rn-dark-mode", "Lista de temas; New Theme cria um tema customizado."),
    alertas=["Ativar um tema SLDS 2 liga o SLDS 2 para a org.",
             "O dark mode vale para temas SLDS 2 e está em Beta, com disponibilidade por edição.",
             "Cada app pode usar a própria cor e o próprio logo no lugar do tema da org."])

# LWC, Aura e Visualforce aparecem também no tema de páginas e componentes (pendência da rodada A1).
for fid, motivo in (("lightning-web-components", "Componentes customizados usados nas Lightning pages."),
                    ("aura-components", "Componentes customizados usados nas Lightning pages."),
                    ("visualforce", "Páginas e componentes customizados de interface.")):
    C.secundaria(fid, UI, "lightning-pages-e-componentes", motivo)

print(f"lote 7d: 5 metadata types e {len(APP_SUBS) + len(LAY_SUBS) + 1} estruturas gravados; 5 funcionalidades novas e 4 ampliadas")
