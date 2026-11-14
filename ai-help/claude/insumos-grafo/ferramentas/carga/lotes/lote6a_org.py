"""Lote 6a (issue #34, item 3): metadata types e funcionalidades do tema Organização e configurações base.

Cadastra CompanySettings, CurrencySettings, LanguageSettings, MyDomainSettings, CustomMetadata e CustomLabels (com as
estruturas FiscalYearSettings, Currency, CustomMetadataValue e CustomLabel) e cria as funcionalidades do tema.
Translations NÃO entra: a leitura não confirmou o nome de cada elemento (ver fontes/extracoes/mdapi-lote6a-org.txt).

Cita fontes de Ajuda registradas por conteudo_temas.py: rode este script e, em seguida, conteudo_temas.py e temas_internos.py.
Reexecutável. Uso: python3 ferramentas/carga/lotes/lote6a_org.py
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M          # noqa: E402
from carga.mdt import P             # noqa: E402
from carga.base import af, ev       # noqa: E402
from carga import catalogo as C     # noqa: E402

DATA = "2026-11-14"
EXTR = "fontes/extracoes/mdapi-lote6a-org.txt"
BASE_URL = "https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-"
VERSAO = "sem versão na URL (referência atual; a página cita a API 68.0)"


def _f(sufixo, nome, pertinencia, pagina=None):
    return C.fonte("src:mdapi-" + sufixo, f"{nome} (Metadata API)", BASE_URL + (pagina or sufixo) + ".html", pertinencia, EXTR, DATA, versao=VERSAO)


C.registrar_fontes([
    _f("companysettings", "CompanySettings", "Arquivo, versão e propriedades do tipo CompanySettings."),
    _f("currencysettings", "CurrencySettings", "Arquivo, versão e propriedades do tipo CurrencySettings."),
    _f("languagesettings", "LanguageSettings", "Arquivo, versão e propriedades do tipo LanguageSettings."),
    _f("mydomainsettings", "MyDomainSettings", "Arquivo, versão e propriedades do tipo MyDomainSettings."),
    _f("custommetadata-tipo", "CustomMetadata", "Propriedades do tipo CustomMetadata e do subtipo CustomMetadataValue (leitura da página).",
       pagina="custommetadata"),
    _f("customlabels", "CustomLabels", "Arquivo, versão e propriedades dos tipos CustomLabels e CustomLabel."),
    _f("translations", "Translations", "O que o tipo Translations cobre e como os arquivos de tradução são nomeados (tipo ainda não cadastrado)."),
])

S_COMPANY, S_CURRENCY, S_LANG = "src:mdapi-companysettings", "src:mdapi-currencysettings", "src:mdapi-languagesettings"
S_DOMAIN, S_CMDT, S_LABELS = "src:mdapi-mydomainsettings", "src:mdapi-custommetadata-tipo", "src:mdapi-customlabels"

FALSE = ("false", False, "A página declara default false.")
TRUE = ("valor", "true", None)
SETTINGS_PKG = "No package.xml, use o tipo Settings com o nome-base do arquivo como membro; o curinga só vale para recuperar todas as configurações."
SO_LEITURA = ["Somente leitura, segundo a página."]
FULLNAME_SETTINGS = M.FULLNAME_HERDADO(None)

# ---------------------------------------------------------------- estruturas
M.struct("FiscalYearSettings", S_COMPANY, ["mdt:CompanySettings"], [
    P("fiscalYearNameBasedOn", "string", None,
      "Enumeração com os valores endingMonth e startingMonth. A página não descreve o efeito de cada valor.",
      vals=[("endingMonth", None), ("startingMonth", None)]),
    P("startMonth", "string", None, "Mês em que o ano fiscal se baseia."),
], "Ano fiscal padrão da org, usado em CompanySettings.fiscalYear. Não é o objeto API de mesmo nome.")

M.struct("Currency", S_CURRENCY, ["mdt:CurrencySettings"], [
    P("active", "boolean", None, "Indica se os usuários podem atribuir a moeda a registros. Uma moeda inativa não pode ser a corporativa.",
      default=("valor", "true", "Padrão declarado para moedas novas.")),
    P("conversionRate", "double", None, "Taxa de conversão desta moeda para a moeda corporativa. Para a própria moeda corporativa, é 1.0.",
      "C:Obrigatório para moedas novas, segundo a descrição do campo; a seção do subtipo o lista como não obrigatório."),
    P("isoCode", "string", None, "Código ISO 4217 da moeda, como USD, JPY ou EUR. Precisa ser um código suportado pela Salesforce; outro código devolve erro.", "S"),
    P("scale", "int", None, "Quantidade de casas decimais, de 0 a 6."),
], "Uma moeda da org em CurrencySettings.currency: código, taxa, casas decimais e se está ativa.")

M.struct("CustomMetadataValue", S_CMDT, ["mdt:CustomMetadata"], [
    P("field", "string", None, "Nome de um campo customizado do tipo, com namespace (se vier de pacote gerenciado) e sufixo __c. O nome do tipo não entra.", "S"),
    P("value", "anyType", None, "Valor do campo neste registro. Para campos EntityDefinition e FieldDefinition, é o nome de API qualificado. Pode ser nulo.", "S",
      natureza="texto_livre", contexto="A fonte tipa como anyType: o valor depende do tipo do campo customizado."),
], "Par campo e valor de um registro de custom metadata type.")

M.struct("CustomLabel", S_LABELS, ["mdt:CustomLabels"], [
    P("categories", "string", None, "Categorias do label, separadas por vírgula, usadas em filtros das list views de custom labels. Até 255 caracteres."),
    P("fullName", "string", None, "Nome do custom label; herdado do tipo Metadata.", "?", herdada="Metadata",
      notas=["A tabela marca o campo como não obrigatório, mas a descrição diz que ele deve ser informado ao criar, atualizar ou excluir."]),
    P("language", "string", None, "Idioma do texto do label.", "S"),
    P("protected", "boolean", None, "Indica se o componente é protegido. Um componente protegido não pode ser referenciado por componentes da org que instala o pacote.", "S"),
    P("shortDescription", "string", None, "Termo fácil de reconhecer que identifica o label; é usado em merge fields.", "S"),
    P("value", "string", None, "Texto do label. Até 1.000 caracteres.", "S"),
], "Um custom label dentro do arquivo CustomLabels. A página o trata como metadata type próprio (estende Metadata e pode ser listado por nome no "
   "package.xml), mas ele não consta do inventário de metadata types da v68 usado pelo projeto; por isso fica aqui como estrutura.")

# ---------------------------------------------------------------- exemplos XML (escritos pelo projeto, só com elementos documentados)
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
EX_COMPANY = CAB + f"""<CompanySettings {NS}>
    <!-- false: as previsões usam os períodos fiscais padrão -->
    <enableCustomFiscalYear>false</enableCustomFiscalYear>
    <fiscalYear>
        <!-- Valores documentados: endingMonth ou startingMonth -->
        <fiscalYearNameBasedOn>startingMonth</fiscalYearNameBasedOn>
        <startMonth>[mês de início do ano fiscal]</startMonth>
    </fiscalYear>
</CompanySettings>"""
EX_CURRENCY = CAB + f"""<CurrencySettings {NS}>
    <!-- Moeda corporativa: precisa estar cadastrada e ativa -->
    <corporateCurrency>USD</corporateCurrency>
    <currency>
        <active>true</active>
        <!-- A moeda corporativa tem taxa 1.0 -->
        <conversionRate>1.0</conversionRate>
        <isoCode>USD</isoCode>
        <scale>2</scale>
    </currency>
    <currency>
        <active>true</active>
        <conversionRate>[taxa de conversão para a moeda corporativa]</conversionRate>
        <isoCode>EUR</isoCode>
        <scale>2</scale>
    </currency>
    <!-- Atenção: ligar múltiplas moedas é irreversível -->
    <enableMultiCurrency>true</enableMultiCurrency>
</CurrencySettings>"""
EX_LANG = CAB + f"""<LanguageSettings {NS}>
    <!-- Idiomas exibidos, na ordem da lista (códigos usados como exemplo na documentação) -->
    <displayedLanguages>en_US,fr,de,ja</displayedLanguages>
    <enableEndUserLanguages>true</enableEndUserLanguages>
    <enableTranslationWorkbench>true</enableTranslationWorkbench>
</LanguageSettings>"""
EX_DOMAIN = CAB + f"""<MyDomainSettings {NS}>
    <!-- Usuários e API só entram pela URL do My Domain -->
    <canOnlyLoginWithMyDomainUrl>true</canOnlyLoginWithMyDomainUrl>
    <doesApiLoginRequireOrgDomain>true</doesApiLoginRequireOrgDomain>
    <!-- Valores documentados: Redirect, WarnOnRedirect, NoRedirect -->
    <instancedUrlRedirectHandling>WarnOnRedirect</instancedUrlRedirectHandling>
    <redirectPriorMyDomain>true</redirectPriorMyDomain>
</MyDomainSettings>"""
EX_CMDT = CAB + f"""<CustomMetadata {NS}>
    <label>[rótulo do registro]</label>
    <protected>false</protected>
    <!-- Um bloco values por campo customizado do tipo -->
    <values>
        <field>[NomeDoCampo__c]</field>
        <value>[valor do campo neste registro]</value>
    </values>
</CustomMetadata>"""
EX_LABELS = CAB + f"""<CustomLabels {NS}>
    <!-- Um bloco labels por custom label -->
    <labels>
        <fullName>[NomeDoLabel]</fullName>
        <language>[código do idioma do texto]</language>
        <protected>false</protected>
        <shortDescription>[termo curto que identifica o label]</shortDescription>
        <value>[texto do label, até 1.000 caracteres]</value>
    </labels>
</CustomLabels>"""

# ---------------------------------------------------------------- metadata types
M.mdt("CompanySettings", S_COMPANY,
      "Configurações globais da org que afetam vários recursos. Na versão lida, os campos tratam do ano fiscal.",
      "Recuperar e implantar a definição do ano fiscal padrão e o uso de período fiscal customizado nas previsões.", "27.0", [
          P("enableCustomFiscalYear", "boolean", "47.0",
            "Quando há período fiscal customizado configurado, indica se ele é usado nas previsões (forecasts). Com false, valem os períodos padrão.", "S", default=FALSE),
          P("fiscalYear", "FiscalYearSettings", None,
            "Ano fiscal definido por ano e mês de início. Não fica disponível se Custom Fiscal Year ou Forecasts (Classic) estiver ligado.",
            estrutura="FiscalYearSettings", notas=["Mudar o ano fiscal pode apagar cotas (quotas) e ajustes de previsão."]),
          FULLNAME_SETTINGS,
      ], exemplo=EX_COMPANY, arquivos_prontos=M.arquivos_settings("CompanySettings", "Company", S_COMPANY), curinga=False,
      alertas=[SETTINGS_PKG, "Mudar o ano fiscal por este tipo pode apagar cotas e ajustes de previsão, como na tela de Setup."],
      divergencias=["A página (src:mdapi-companysettings) traz duas seções de subtipo, 'FiscalYearSetting Type' e 'FiscalYearSettings Type', "
                    "com os mesmos dois campos, sem explicar a relação entre elas. O catálogo registra uma estrutura só, FiscalYearSettings, "
                    "que é o tipo declarado no campo fiscalYear."],
      cobertura_nota="Universo esperado = tabela Fields da página oficial lida em 2026-11-14 (mais fullName herdado).",
      setup=af("verificado", "Setup > Quick Find: Fiscal Year > Fiscal Year", "Tela que define o ano fiscal. " + C.UI_EN, [ev("src:help-fiscal-year-set")]))

M.mdt("CurrencySettings", S_CURRENCY,
      "Configuração de moedas da org: múltiplas moedas, moedas ativas, moeda corporativa e taxas com data de vigência.",
      "Recuperar e implantar a configuração de moedas em vez de repeti-la à mão em cada ambiente.", "47.0", [
          P("corporateCurrency", "string", "68.0",
            "Código ISO 4217 da moeda corporativa, cuja taxa é fixa em 1.0. Informar o campo troca a moeda corporativa; a nova precisa estar cadastrada e ativa.",
            notas=["Sem efeito se enableMultiCurrency não for true, antes ou no mesmo deploy."]),
          P("currency", "Currency[]", "68.0",
            "Moedas da org. Uma entrada nova é inserida; uma entrada com isoCode já existente atualiza active, scale e conversionRate.",
            estrutura="Currency", notas=["Sem efeito se enableMultiCurrency não for true."]),
          P("enableCurrencyEffectiveDates", "boolean", None, "Liga as taxas de câmbio com data de vigência. Exige enableMultiCurrency em true.", default=FALSE),
          P("enableCurrencySymbolWithMultiCurrency", "boolean", None,
            "Em org com múltiplas moedas, mostra o símbolo da moeda (true) ou o código ISO (false). Sem efeito com enableMultiCurrency em false.", default=FALSE),
          P("enableMultiCurrency", "boolean", None,
            "Liga múltiplas moedas. A partir da API 68.0, implantar true liga o recurso; em org que já o tem, nada muda. A moeda corporativa vem de "
            "corporateCurrency, se enviado no mesmo deploy, ou da localidade da org.", default=FALSE,
            notas=["Ligar é irreversível. Implantar false numa org com múltiplas moedas devolve erro."]),
          P("isMultiCurrencyActivationAllowed", "boolean", None,
            "Descontinuado na API 49.0 e posteriores: não muda se o administrador pode ativar múltiplas moedas. Só é visível com múltiplas moedas desligadas.",
            default=FALSE),
          P("isParenCurrencyConvDisabled", "boolean", None,
            "Desliga a conversão de moeda entre parênteses. Com false, o usuário vê o valor convertido quando a moeda pessoal difere da moeda do registro.",
            default=TRUE),
          FULLNAME_SETTINGS,
      ], exemplo=EX_CURRENCY, arquivos_prontos=M.arquivos_settings("CurrencySettings", "Currency", S_CURRENCY), curinga=False,
      alertas=[SETTINGS_PKG, "Ligar múltiplas moedas por enableMultiCurrency é irreversível; teste em sandbox antes."],
      divergencias=["Na página (src:mdapi-currencysettings), a descrição de conversionRate diz que o campo é obrigatório para moedas novas, "
                    "mas a seção do subtipo Currency o lista como não obrigatório."],
      cobertura_nota="Universo esperado = tabela Fields da página oficial lida em 2026-11-14 (mais fullName herdado).",
      setup=af("verificado", "Setup > Quick Find: Manage Currencies > Manage Currencies", "Tela de moedas da org. " + C.UI_EN, [ev("src:help-multicurrency-manage")]))

M.mdt("LanguageSettings", S_LANG,
      "Configurações de idioma da org: quais idiomas os usuários podem escolher, formatos de localidade e opções de tradução.",
      "Recuperar e implantar a seleção de idiomas, o formato ICU e a ativação do Translation Workbench.", "47.0", [
          P("displayedLanguages", "string", "68.0",
            "Códigos de idioma a exibir, separados por vírgula (por exemplo en_US, fr, de, ja). A ordem define a ordem da lista; o valor all exibe "
            "todos os idiomas disponíveis na org. Se o campo é omitido, a configuração existente não muda."),
          P("enableCanadaIcuFormat", "boolean", None, "Indica se o formato ICU está ligado para a localidade en_CA.",
            default=("valor", "true", "true em orgs criadas na API 47.0 ou depois; false nas anteriores.")),
          P("enableDataTranslation", "boolean", "49.0", "Indica se a tradução de dados está ligada.", default=FALSE),
          P("enableEndUserLanguages", "boolean", None, "Indica se os idiomas de usuário final (end-user languages) estão ligados.", default=FALSE),
          P("enableICULocaleDateFormat", "boolean", None, "Indica se datas e moedas são formatadas com International Components for Unicode (ICU).",
            default=("valor", "true", "true em orgs criadas na API 47.0 ou depois; false nas anteriores.")),
          P("enableLanguageExtensionPackage", "boolean", "58.0", "Indica se pacotes de extensão de idioma estão ligados.", default=FALSE,
            notas=["A página marca o campo como Beta."]),
          P("enableLocaleInsensitiveFiltering", "boolean", "56.0",
            "Indica se os usuários podem filtrar resultados de consulta sem depender da localidade ou do idioma deles.", default=FALSE),
          P("enableLocalNamesForStdObjects", "boolean", "48.0", "Indica se dá para definir campos de nome local em objetos padrão.", default=FALSE),
          P("enablePlatformLanguages", "boolean", None, "Indica se os idiomas platform-only estão ligados. Passar para true também põe enableEndUserLanguages em true.",
            default=FALSE),
          P("enableTranslationWorkbench", "boolean", None, "Indica se o Translation Workbench está ligado.", default=FALSE),
          P("enableTranslationWorkbenchConnectAPI", "boolean", "67.0", "Indica se a API REST Connect do Translation Workbench está ligada.", default=FALSE),
          P("useLanguageFallback", "boolean", None,
            "Define se a tradução segue a regra de fallback de idioma (true) ou devolve o rótulo primário (false).", default=TRUE),
          FULLNAME_SETTINGS,
      ], exemplo=EX_LANG, arquivos_prontos=M.arquivos_settings("LanguageSettings", "Language", S_LANG), curinga=False, alertas=[SETTINGS_PKG],
      cobertura_nota="Universo esperado = tabela Fields da página oficial lida em 2026-11-14 (mais fullName herdado).",
      setup=af("verificado", "Setup > Quick Find: Company Settings > Language Settings", "Tela de idiomas da org. " + C.UI_EN, [ev("src:help-supported-languages")]))

M.mdt("MyDomainSettings", S_DOMAIN,
      "Configurações do My Domain da org, o recurso que põe o nome da empresa nas URLs.",
      "Recuperar e implantar políticas de login pelo My Domain, redirecionamentos de URLs antigas e opções de roteamento e cookies.", "47.0", [
          P("areLegacyRedirectsMaintained", "boolean", "63.0",
            "Conferido no upgrade para o Summer '25: se false, enableLegacyRedirections é desligado. Sem efeito depois do Summer '25.", default=FALSE),
          P("areLgcyRdirMaintainedWntr26", "boolean", "64.0",
            "Conferido no upgrade para o Winter '26, com o mesmo papel de areLegacyRedirectsMaintained. Sem efeito depois do Winter '26.", default=FALSE),
          P("canOnlyLoginWithMyDomainUrl", "boolean", None, "Com true, os usuários só entram pela URL de login do My Domain.", default=FALSE),
          P("doesApiLoginRequireOrgDomain", "boolean", None, "Com true, o acesso por API exige a URL de login do My Domain.", default=FALSE),
          P("doesWarnOnForceComRedirect", "boolean", "59.0", "Indica se o usuário vê um aviso ao ser redirecionado de uma URL *.force.com anterior.", default=FALSE),
          P("doesWarnOnRedirect", "boolean", "59.0", "Indica se o usuário vê um aviso ao ser redirecionado de uma URL de My Domain anterior.", default=FALSE),
          P("domainPartition", "OrgDomainShard", "55.0", "Partição da org nos domínios particionados.", notas=SO_LEITURA, vals=[
              ("demo", "Disponível na API 60.0 e posteriores; a página não descreve o uso."), ("develop", "Orgs Developer Edition."),
              ("free", "Uso interno."), ("none", "A org não usa domínios particionados."),
              ("patch", "Disponível na API 59.0 e posteriores; a página não descreve o uso."), ("sandbox", "Sandboxes com enhanced domains."),
              ("scratch", "Scratch orgs."), ("sfdctest", "Uso interno."), ("trailblaze", "Trailblazer Playgrounds.")]),
          P("edgeRoutingMethod", "EdgeRoutingOption", "65.0", "Método de roteamento das requisições quando useEdge é true.", notas=SO_LEITURA,
            default=("valor", "global", None), vals=[
              ("global", "Local Edge mais próximo."), ("regional", "Só locais da Salesforce no país da org; apenas Hyperforce Japão."),
              ("gsr", "Nó de rede confiável mais próximo, contornando certos locais de rede do Oriente Médio.")]),
          P("enableCrossDomainPreviewCookies", "boolean", "62.0",
            "Quando isFirstPartyCookieUseRequired é true, indica se cookies entre domínios são permitidos no domínio de preview do Experience Builder."),
          P("enableEdgeDuringRollout", "boolean", "58.0", "Indica se o Edge fica ligado durante a implantação programada. Sem efeito se useEdge é true.", default=TRUE),
          P("enableExtendedRedirections", "boolean", "62.0", "Indica se chamadas a hostnames temporários de redirecionamento estendido são redirecionadas.", default=TRUE),
          P("enableLegacyRedirections", "boolean", "62.0", "Quando redirectPriorMyDomain é true, indica se hostnames legados são redirecionados."),
          P("enableNativeBrowserForAuthOnAndroid", "boolean", None, "Usa o navegador nativo para autenticação nos apps móveis Android.", default=FALSE),
          P("enableNativeBrowserForAuthOnIos", "boolean", None, "Usa o navegador nativo para autenticação nos apps móveis iOS.", default=FALSE),
          P("enableShareBrowserSessionAndroidForAuth", "boolean", None, None),
          P("enableShareBrowserSessionIOSForAuth", "boolean", None, None),
          P("instancedUrlRedirectHandling", "OrgDomainRedirectOption", "59.0",
            "Como são tratadas as visitas à URL da org com nome de instância. Não afeta o login (veja canOnlyLoginWithMyDomainUrl).", vals=[
              ("Redirect", "Redireciona para a página equivalente no My Domain."), ("WarnOnRedirect", "Mostra um aviso breve antes de redirecionar."),
              ("NoRedirect", "Não redireciona; é preciso usar os hostnames do My Domain.")]),
          P("isFirstPartyCookieUseRequired", "boolean", "61.0", "Indica se o atributo SameSite=None é removido dos cookies da Salesforce.",
            default=("valor", "true", "true em orgs criadas no Summer '24 ou depois; false nas demais.")),
          P("isIcorInstApiTrafficBlocked", "boolean", "64.0", "Reservado para uso futuro.", default=FALSE),
          P("isInstancedApiTrafficBlocked", "boolean", None, None),
          P("logRedirections", "boolean", "56.0", "Com true, o log de eventos Hostname Redirects é gerado junto dos logs de eventos diários.", default=FALSE),
          P("myDomainName", "string", "51.0", "Subdomínio usado nas URLs do My Domain.", notas=SO_LEITURA),
          P("myDomainSuffix", "OrgDomainProdSuffix", "51.0", "Sufixo de domínio da URL de login do My Domain.", notas=SO_LEITURA, vals=[
              ("CloudforceLimited", "cloudforce.com."), ("DatabaseLimited", "database.com."),
              ("MySalesforce", "my.salesforce.com, com enhanced domains."), ("MySalesforceLimited", "my.salesforce.com, sem enhanced domains."),
              ("OrgLevelCertificate", "my-salesforce.com."),
              ("OrgLevelCertificateLimited", "my-salesforce.com legado; incompatível com navegadores que bloqueiam cookies de terceiros."),
              ("Restricted1", "Reservado para uso futuro."), ("Restricted2", "Reservado para uso futuro.")]),
          P("onboardCustomerSpecificSuffix", "boolean", "63.0", "Reservado para uso futuro.", default=FALSE),
          P("redirectForceComSiteUrls", "boolean", "55.0", "Com true, URLs de site .force.com são redirecionadas para a URL de site atual do My Domain.", default=TRUE),
          P("redirectPriorMyDomain", "boolean", "54.0", "Com true, URLs do My Domain anterior são redirecionadas para o atual.",
            default=("valor", "true", "Volta a true quando um My Domain novo é implantado.")),
          P("use3rdPartyCookieBlockingCompatibleHostnames", "boolean", "51.0",
            "Indica se o nome da instância entra nas URLs de Visualforce quando cookies de terceiros são bloqueados.", default=TRUE),
          P("useEdge", "boolean", "51.0", "Indica se as URLs qualificadas do My Domain passam pela Salesforce Edge Network.", default=TRUE, notas=SO_LEITURA),
          P("useEnhancedDomainsInSandbox", "boolean", None, "Campo legado: desde a API 58.0 o valor é sempre true, qualquer que seja o valor enviado."),
          P("useStabilizedMyDomainHostnames", "boolean", None,
            "Indica se o nome da instância fica escondido nas URLs de Visualforce, Experience Builder, Site.com Studio e arquivos de conteúdo.", default=TRUE),
          P("useStabilizedSandboxMyDomainHostnames", "boolean", None, "Campo legado: o valor é sempre true em todas as versões da API."),
          FULLNAME_SETTINGS,
      ], exemplo=EX_DOMAIN, arquivos_prontos=M.arquivos_settings("MyDomainSettings", "MyDomain", S_DOMAIN),
      alertas=["No package.xml, use o tipo Settings com o membro MyDomain.",
               "Vários campos são somente leitura (domainPartition, edgeRoutingMethod, myDomainName, myDomainSuffix, useEdge): o nome do My Domain "
               "não é trocado por este tipo."],
      cobertura_nota="Universo esperado = tabela Fields da página oficial lida em 2026-11-14 (mais fullName herdado). O trecho lido não traz "
                     "declaração sobre o curinga no package.xml.",
      setup=af("verificado", "Setup > Quick Find: My Domain > My Domain", "Tela do My Domain. " + C.UI_EN, [ev("src:help-mydomain-rename")]))

M.mdt("CustomMetadata", S_CMDT,
      "Um registro de um custom metadata type. Cada registro é um componente de metadado, com arquivo próprio.",
      "Levar os registros de configuração de um ambiente a outro junto com o resto dos metadados.", "31.0", [
          P("description", "string", None, "Descrição do registro. Até 1.000 caracteres."),
          P("label", "string", None, "Rótulo do registro. A página informa que hoje ele só aparece pela interface de empacotamento."),
          P("protected", "boolean", None, "Indica se o registro é protegido. Em pacote gerenciado, limita que código pode ler ou alterar o registro."),
          P("values", "CustomMetadataValue[]", None, "Valores dos campos customizados do registro, um par campo e valor por item.", estrutura="CustomMetadataValue"),
          M.FULLNAME_HERDADO(None, "Nome do registro; herdado do tipo Metadata. Começa com o nome do tipo, sem o sufixo __mdt, e inclui o namespace "
                                   "quando o tipo vem de pacote gerenciado instalado."),
      ], curinga=True, exemplo=EX_CMDT,
      cobertura_nota="Universo esperado = tabela Fields da página oficial lida em 2026-11-14 (mais fullName herdado).",
      setup=af("verificado", "Setup > Quick Find: Custom Metadata Types > Custom Metadata Types", "Lista dos custom metadata types; os registros são "
               "geridos a partir de cada tipo. " + C.UI_EN, [ev("src:help-cmdt-create")]))

M.mdt("CustomLabels", S_LABELS,
      "O conjunto de custom labels da org: textos customizados que podem ser traduzidos e lidos por código e por páginas.",
      "Versionar e implantar os textos da aplicação em vez de deixá-los fixos no código.", "14.0", [
          P("fullName", "string", None, "Nome do conjunto de custom labels; herdado do tipo Metadata.", "?", herdada="Metadata",
            notas=["A tabela marca o campo como não obrigatório, mas a descrição diz que ele deve ser informado ao criar, atualizar ou excluir."]),
          P("labels", "CustomLabel[]", None, "Lista de custom labels.", estrutura="CustomLabel"),
      ], curinga=True, exemplo=EX_LABELS,
      alertas=["O tipo CustomLabels não recupera labels por nome: para labels específicos, a página manda usar o tipo CustomLabel com os nomes como "
               "membros no package.xml.", "Não é possível recuperar CustomLabels com namespace.",
               "As traduções dos labels não ficam neste arquivo: ficam na pasta translations, em arquivos <código de localidade>.translation "
               "(tipo Translations, ainda não cadastrado no catálogo)."],
      divergencias=["Nas tabelas de CustomLabels e CustomLabel (src:mdapi-customlabels), fullName aparece como não obrigatório, mas a descrição diz Required.",
                    "A página trata CustomLabel como metadata type próprio; ele não consta do inventário v68 do projeto e foi cadastrado como estrutura."],
      cobertura_nota="Universo esperado = tabela Fields da página oficial lida em 2026-11-14.",
      setup=af("verificado", "Setup > Quick Find: Custom Labels > Custom Labels", "Lista de custom labels. " + C.UI_EN, [ev("src:help-custom-labels-edit")]))

M.emit_structs()

# ---------------------------------------------------------------- funcionalidades
ORG = "organizacao-e-configuracoes-base"
SEM_OBJ = {"tipo": "objeto_api", "estado": "desconhecido",
           "motivo": "Objetos API do tema não investigados no lote 6a; a lista vazia não comprova inexistência."}
SEM_MDT = lambda motivo: {"tipo": "metadata_type", "estado": "desconhecido", "motivo": motivo}


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


C.funcionalidade(
    "informacoes-da-empresa", "Informações da empresa", "Company Information", ["dados da org", "company profile", "organization id"],
    "Página de Setup com os dados cadastrais da org: endereço, idioma, localidade e fuso padrão, moeda e as licenças compradas.",
    "Conferir e ajustar os padrões que valem para a org inteira e para os usuários novos.",
    "A administradora troca o fuso padrão da org; quem for cadastrado depois já nasce com o fuso novo.",
    (ORG, "identificacao-e-configuracao-da-org"), [], [], [],
    ["src:help-company-info-fields", "src:help-setup-company", "src:help-supported-languages"],
    [SEM_MDT("Não investigado: os campos de CompanySettings lidos tratam só do ano fiscal, e não foi confirmado qual metadata type guarda os demais "
             "dados desta página."), SEM_OBJ],
    setup("Setup > Quick Find: Company Information > Company Information", "src:help-supported-languages"))

C.funcionalidade(
    "idiomas-da-org", "Idiomas da org", "Language Settings", ["language settings", "idiomas", "end-user languages", "platform-only languages"],
    "Define quais idiomas os usuários podem escolher, entre os três níveis de suporte: totalmente suportados, de usuário final e platform-only.",
    "Liberar para cada pessoa a interface no idioma dela, sem mudar o idioma padrão da empresa.",
    "Uma empresa brasileira com equipe em Portugal liga os idiomas de usuário final e põe Português (Portugal) na lista exibida.",
    (ORG, "localizacao-idiomas-e-traducao"), [], [("LanguageSettings", "Seleção de idiomas, formato ICU e opções de tradução implantáveis.")], [],
    ["src:help-select-languages", "src:help-supported-languages", "src:mdapi-languagesettings"], [SEM_OBJ],
    setup("Setup > Quick Find: Company Settings > Language Settings", "src:help-supported-languages"),
    pre=["Customize Application (para mudar); View Setup and Configuration (para ver)."])

C.funcionalidade(
    "translation-workbench", "Translation Workbench", "Translation Workbench", ["tradução de metadados", "translation language settings", "traduções"],
    "Ferramenta para manter traduções de rótulos de metadados (e de dados, onde houver): escolhe-se o idioma, designam-se tradutores e as "
    "traduções são digitadas na tela ou importadas por arquivo.",
    "Mostrar campos, picklists e outros rótulos customizados no idioma de cada usuário.",
    "O rótulo do campo customizado 'Faixa de desconto' ganha tradução para espanhol, vista por quem usa a interface em espanhol.",
    (ORG, "localizacao-idiomas-e-traducao"), [], [("LanguageSettings", "Liga o Translation Workbench (enableTranslationWorkbench).")], [],
    ["src:help-translation-workbench", "src:help-translation-languages-add", "src:mdapi-languagesettings", "src:mdapi-translations"],
    [SEM_OBJ],
    setup("Setup > Quick Find: Translation Language Settings > Translation Language Settings", "src:help-translation-languages-add"),
    limitacoes=["Objetos padrão não estão no Translation Workbench; a Ajuda manda usar a tela de renomear abas e rótulos.",
                "Não está disponível em orgs de idioma único.",
                "As traduções viajam como metadado pelo tipo Translations, que consta do inventário v68 mas ainda não está cadastrado neste catálogo."],
    pre=["Manage Translation (para incluir idiomas e designar tradutores)."])

C.funcionalidade(
    "custom-labels", "Custom labels", "Custom Labels", ["rótulos customizados", "labels", "system.label"],
    "Textos customizados, com nome próprio, que podem ser traduzidos e lidos por classes Apex, páginas Visualforce, Lightning pages e componentes Lightning.",
    "Tirar do código os textos da aplicação, como mensagens de erro e de ajuda, e mostrá-los no idioma do usuário.",
    "A mensagem 'Informe o CNPJ antes de salvar' fica num custom label; o componente lê o label e mostra a tradução conforme o idioma de quem usa.",
    (ORG, "localizacao-idiomas-e-traducao"), [], [("CustomLabels", "Conjunto de custom labels implantável.")], [],
    ["src:help-custom-labels", "src:help-custom-labels-edit", "src:mdapi-customlabels"], [SEM_OBJ],
    setup("Setup > Quick Find: Custom Labels > Custom Labels", "src:help-custom-labels-edit"),
    limitacoes=["Até 5.000 custom labels por org, com até 1.000 caracteres cada; labels de pacotes gerenciados não contam."],
    pre=["Customize Application (para criar, editar ou excluir)."])

C.funcionalidade(
    "multiplas-moedas", "Múltiplas moedas", "Multiple Currencies", ["multi-currency", "moedas", "corporate currency", "advanced currency management",
                                                                 "dated exchange rates"],
    "Permite registrar valores em mais de uma moeda: há uma moeda corporativa, moedas ativas e a taxa de conversão de cada uma para a corporativa.",
    "Deixar cada equipe trabalhar na própria moeda e ainda somar tudo na moeda da matriz.",
    "A matriz reporta em reais; a filial do Chile registra oportunidades em pesos, convertidas para reais pela taxa cadastrada.",
    (ORG, "moedas-e-calendario-fiscal"), [], [("CurrencySettings", "Ativação de múltiplas moedas, moeda corporativa, moedas e taxas implantáveis.")], [],
    ["src:help-multicurrency-manage", "src:help-multicurrency-considerations", "src:help-advanced-currency", "src:mdapi-currencysettings"], [SEM_OBJ],
    setup("Setup > Quick Find: Manage Currencies > Manage Currencies", "src:help-multicurrency-manage"),
    alertas=["Depois de ligar múltiplas moedas, não dá para desligar."],
    pre=["Customize Application (para alterar moedas); View Setup and Configuration (para ver)."])

C.funcionalidade(
    "ano-fiscal", "Ano fiscal", "Fiscal Year", ["fiscal year", "custom fiscal year", "calendário fiscal", "período fiscal"],
    "Define como a org conta o ano fiscal: padrão (calendário gregoriano, com o mês de início à escolha) ou customizado (períodos definidos pela empresa).",
    "Fazer os períodos de relatórios e previsões baterem com o calendário financeiro da empresa.",
    "Uma empresa com exercício de abril a março escolhe o ano fiscal padrão com início em abril.",
    (ORG, "moedas-e-calendario-fiscal"), [], [("CompanySettings", "Ano fiscal padrão e uso de período customizado nas previsões, implantáveis.")], [],
    ["src:help-fiscal-year-set", "src:help-fiscal-year-define", "src:mdapi-companysettings"], [SEM_OBJ],
    setup("Setup > Quick Find: Fiscal Year > Fiscal Year", "src:help-fiscal-year-set"),
    alertas=["Depois de ligar o ano fiscal customizado, não dá para desligar.", "Mudar o mês de início do ano fiscal apaga cotas e ajustes de previsão."],
    pre=["Customize Application."])

C.funcionalidade(
    "feriados", "Feriados", "Holidays", ["holidays", "support holidays", "feriado recorrente"],
    "Datas e horários em que o atendimento não funciona. Cada feriado é associado a um ou mais horários comerciais e suspende a contagem deles.",
    "Evitar que prazos de escalonamento e marcos de atendimento corram em dia sem expediente.",
    "O feriado 'Ano Novo' vai das 20h de 31 de dezembro às 9h de 2 de janeiro; nesse intervalo, as regras de escalonamento não contam tempo.",
    (ORG, "horarios-comerciais-e-feriados"),
    [("processos-de-negocio-especificos-de-produto", "atendimento", "Suspende regras de escalonamento e marcos de entitlement durante o feriado.")],
    [("BusinessHoursSettings", "Feriados implantáveis junto dos horários comerciais (estrutura Holidays).")], [],
    ["src:help-holidays", "src:help-holidays-guidelines", "src:mdapi-businesshourssettings"], [SEM_OBJ],
    setup("Setup > Quick Find: Holidays > Holidays", "src:help-holidays"),
    limitacoes=["Até 1.000 feriados por horário comercial.", "Só horários comerciais ativos podem ser associados a um feriado."],
    pre=["Manage Business Hours Holidays."])

C.funcionalidade(
    "my-domain", "My Domain", "My Domain", ["domínio da org", "enhanced domains", "url de login"],
    "O subdomínio próprio da org nas URLs que a Salesforce hospeda, como a URL de login e as de aplicação.",
    "Dar à org endereços com o nome da empresa e permitir página de login própria, política de login e single sign-on.",
    "Os usuários entram por https://mycompany.my.salesforce.com em vez de um endereço genérico.",
    (ORG, "dominios-e-urls"), [], [("MyDomainSettings", "Políticas de login, redirecionamentos e opções de roteamento implantáveis.")], [],
    ["src:help-mydomain", "src:help-mydomain-rename", "src:help-mydomain-provisioning", "src:mdapi-mydomainsettings"], [SEM_OBJ],
    setup("Setup > Quick Find: My Domain > My Domain", "src:help-mydomain-rename"),
    alertas=["Quando a URL de login ou de site muda, SSO e MFA podem parar de funcionar; preserve o acesso de administradores antes de implantar a mudança."],
    pre=["Customize Application (para editar); Customize Application e Modify All Data (para definir o nome)."])

C.funcionalidade(
    "custom-metadata-types", "Custom metadata types", "Custom Metadata Types", ["cmdt", "custom metadata", "metadados customizados", "__mdt"],
    "Tipos de metadado criados pela empresa para guardar configuração da aplicação. Os registros de cada tipo são metadados: podem ser "
    "empacotados e implantados.",
    "Guardar tabelas de regras e mapeamentos que várias funcionalidades leem, e levá-las entre ambientes junto com o resto da configuração.",
    "O tipo 'Faixa de desconto' tem um registro por faixa; um flow e uma regra de validação leem esses registros.",
    (ORG, "parametros-reutilizaveis"), [], [("CustomMetadata", "Cada registro de um custom metadata type.")], [],
    ["src:help-cmdt-about", "src:help-cmdt-create", "src:help-cmdt-limitations", "src:mdapi-custommetadata-tipo"],
    [SEM_OBJ],
    setup("Setup > Quick Find: Custom Metadata Types > Custom Metadata Types", "src:help-cmdt-create"),
    limitacoes=["A definição do tipo (o 'molde' dos registros) é tratada pela Ajuda como Custom Metadata Types (CustomObject) na Metadata API; "
                "esse vínculo com mdt:CustomObject ainda não foi lido nem registrado neste catálogo."],
    pre=["Customize Application."])

print("lote 6a: 6 metadata types, 4 estruturas e 9 funcionalidades gravados")
