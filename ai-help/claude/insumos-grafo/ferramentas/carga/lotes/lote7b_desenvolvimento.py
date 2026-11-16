"""Lote 7b (rodada A1, issue #34): metadata types e funcionalidades do tema Desenvolvimento, testes e entrega.

Lê o guia versionado 264.0 (API 68.0) e cadastra 12 metadata types (ApexClass, ApexPage, ApexComponent, StaticResource,
LightningComponentBundle, AuraDefinitionBundle, ApexTestSuite, InstalledPackage, ApexSettings, DevHubSettings,
SourceTrackingSettings, DeploymentSettings), 5 estruturas e 14 funcionalidades. PackageVersion passa a existir, o que completa
ApexTrigger (lote 6d).

As fontes de Ajuda e dos guias citadas pelas funcionalidades são registradas por conteudo_temas.py (lista em conteudo_detalhe.py).
Ordem: lotes 6a a 6d, lote7a_tipos_destravados.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7b_desenvolvimento.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga.base import af, ev, ld, sv, caminho  # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-16"
EXTR = "fontes/extracoes/mdapi-lote7b-desenvolvimento.txt"
ATLAS = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
PAGINAS = {  # tipo -> página do guia (quando o nome da página não segue o do tipo)
    "ApexClass": "meta_classes", "ApexPage": "meta_pages", "ApexComponent": "meta_component", "StaticResource": "meta_staticresource",
    "LightningComponentBundle": "meta_lightningcomponentbundle", "AuraDefinitionBundle": "meta_auradefinitionbundle",
    "ApexTestSuite": "meta_apextestsuite", "InstalledPackage": "meta_installedpackage", "ApexSettings": "meta_apexsettings",
    "DevHubSettings": "meta_devhubsettings", "SourceTrackingSettings": "meta_sourcetrackingsettings", "DeploymentSettings": "meta_deploymentsettings",
}


def substituir_fontes(novas):
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


substituir_fontes(
    [C.fonte(f"src:mdapi-{n.lower()}", f"{n} (Metadata API)", ATLAS + pag + ".htm", f"Arquivo, versão e propriedades do tipo {n}.", EXTR, DATA)
     for n, pag in PAGINAS.items()]
    + [C.fonte("src:mdapi-ref-lightningcomponentbundle", "LightningComponentBundle (Metadata API, referência nova)",
               "https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-lightningcomponentbundle.html",
               "O que o tipo LightningComponentBundle estende (o artigo versionado não informa).", EXTR, DATA,
               versao="sem versão na URL (referência atual)", metodo="leitura_resultado_busca")])

S_CLS, S_PAGE, S_COMP, S_RES = "src:mdapi-apexclass", "src:mdapi-apexpage", "src:mdapi-apexcomponent", "src:mdapi-staticresource"
S_LWC, S_AURA, S_SUITE, S_PKG = "src:mdapi-lightningcomponentbundle", "src:mdapi-auradefinitionbundle", "src:mdapi-apextestsuite", "src:mdapi-installedpackage"
S_APEXSET, S_DEVHUB, S_TRACK, S_DEPLOY = "src:mdapi-apexsettings", "src:mdapi-devhubsettings", "src:mdapi-sourcetrackingsettings", "src:mdapi-deploymentsettings"

FALSE = ("false", False, "A página declara default false.")
TRUE = ("valor", "true", None)
FULLNAME = M.FULLNAME_HERDADO(None)
NOTA_COB = "Universo esperado = tabela Fields da página do guia versionado 264.0 (API 68.0), lida em 2026-11-16."
SEM_REQ = " A página não marca campos como obrigatórios."
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
B, S, B64 = "boolean", "string", "base64Binary"
NAO_DECLARADO = "não declarado na página"


def bin_(nome, desc, desde=None, **kw):
    """Campo de conteúdo binário: na API trafega em base64; em arquivo, é o próprio arquivo."""
    return P(nome, kw.pop("tipo", B64), desde, desc, natureza="texto_livre",
             contexto="Na API, o conteúdo trafega em base64; no projeto, é o conteúdo do arquivo correspondente.", **kw)


def pacotes(desde, de_que):
    return P("packageVersions", "PackageVersion[]", desde, f"Versões de pacotes gerenciados instalados que {de_que} referencia.",
             estrutura="PackageVersion")


def sem_versao(nome, nota):
    d = ld(f"metadata-types/{nome}.json")
    d["disponibilidade"] = {"desde_versao": None, "ate_versao": None, "estado": "desconhecido", "nota": nota}
    sv(f"metadata-types/{nome}.json", d)


def arquivos_bundle(pasta, arquivo, nota, src):
    reg = ev("src:sdr-registry", f"types.{'lightningcomponentbundle' if pasta == 'lwc' else 'auradefinitionbundle'}")
    a = af("verificado", {"pasta": f"{pasta}/<nome do bundle>/", "arquivo": arquivo}, nota, [reg, ev(src)])
    return {"source_format": a, "metadata_api_format": a}


# ================================================================ estruturas
M.struct("PackageVersion", S_CLS, ["mdt:ApexClass", "mdt:ApexPage", "mdt:ApexComponent", "mdt:AuraDefinitionBundle", "mdt:ApexTrigger"], [
    P("namespace", S, None, "Namespace do pacote gerenciado: de 1 a 15 caracteres alfanuméricos, sem distinção de maiúsculas, único.", "S"),
    P("majorNumber", "int", None, "Número principal da versão do pacote, no formato majorNumber.minorNumber.", "S"),
    P("minorNumber", "int", None, "Número secundário da versão do pacote, no formato majorNumber.minorNumber.", "S"),
], "A versão de um pacote gerenciado instalado que um componente de código referencia. Desde a API 16.0.")
M.struct("Capabilities", S_LWC, ["mdt:LightningComponentBundle"], [
    P("capability", S, None, "Nome de uma capacidade do componente.", vals=[(v, None) for v in (
        "lightningCommunity__RelaxedCSP", "lightning__dynamicComponent", "lightning__ServerRenderable",
        "lightning__ServerRenderableWithHydration", "lightning__ServiceCloudVoiceToolkitApi")],
      contexto="A página lista estes valores válidos para um campo do tipo string."),
], "Lista do que um Lightning web component pode fazer, diferente de onde ele pode ser usado (targets).")
M.struct("LwcResource", S_LWC, ["mdx:LwcResources"], [
    P("filePath", S, None, "Caminho do arquivo do recurso.", "S"),
    bin_("source", "Conteúdo do recurso.", req="S"),
], "Um arquivo de um bundle de Lightning web component.")
M.struct("LwcResources", S_LWC, ["mdt:LightningComponentBundle"], [
    P("lwcResource", "LwcResource", None, "Um recurso do bundle.", estrutura="LwcResource"),
], "Lista dos recursos (arquivos) de um bundle de Lightning web component.")
M.struct("Targets", S_LWC, ["mdt:LightningComponentBundle"], [
    P("target", S, None, "Tipo de página em que o componente pode aparecer nos builders, como Lightning App Builder, Experience Builder ou Flow Builder.",
      notas=["Os valores válidos ficam numa referência ligada à página e não foram lidos."]),
], "Lista dos lugares em que um Lightning web component pode ser usado.")

# ================================================================ código
M.mdt("ApexClass", S_CLS,
      "Uma classe Apex: o código-fonte da classe e o arquivo de metadado que diz a versão da API e o estado.",
      "Versionar e implantar classes Apex junto com o resto do código da org.", "10.0", [
          P("apiVersion", "double", None, "Versão da API da classe, definida na criação."),
          bin_("content", "A definição da classe (o código-fonte); herdado de MetadataWithContent.", tipo="base64", herdada="MetadataWithContent"),
          P("fullName", S, None, "Nome da classe; herdado. Letras, dígitos e sublinhados; começa com letra; sem sublinhado no fim nem dois seguidos.",
            "?", herdada="Metadata"),
          pacotes("16.0", "a classe"),
          P("status", "ApexCodeUnitStatus", None, "Estado da classe.", vals=[
              ("Active", "A classe está ativa."), ("Deleted", "A classe está marcada para exclusão; útil na atualização de pacotes gerenciados.")],
            contexto="A página informa que o valor Inactive só vale para ApexTrigger."),
      ], exemplo=CAB + f"""<!-- Arquivo de metadado que acompanha o código-fonte .cls -->
<ApexClass {NS}>
    <apiVersion>68.0</apiVersion>
    <!-- Valores documentados para classes: Active, Deleted -->
    <status>Active</status>
</ApexClass>""", estende="MetadataWithContent", curinga=True,
      alertas=["O componente tem dois arquivos: o código-fonte .cls e o arquivo de metadado que o acompanha.",
               "É suportado por todas as chamadas da Metadata API, exceto as CRUD-based.",
               "Por padrão, não se implanta a atualização de uma classe que tem jobs Apex ativos: cancele os jobs ou libere a opção em Deployment Settings."],
      cobertura_nota=NOTA_COB + SEM_REQ)

M.mdt("ApexPage", S_PAGE,
      "Uma página Visualforce: a marcação da página e o arquivo de metadado com rótulo, versão e opções.",
      "Versionar e implantar páginas Visualforce.", "11.0", [
          P("apiVersion", "double", "15.0", "Versão da API da página, definida na criação. Valores abaixo de 15.0 são elevados a 15.0.", "S"),
          bin_("content", "O conteúdo da página (a marcação Visualforce); herdado de MetadataWithContent.", herdada="MetadataWithContent"),
          P("description", S, None, "Descrição do que a página faz."),
          P("fullName", S, None, "Nome único de API da página; herdado do tipo Metadata.", "?", herdada="Metadata"),
          P("availableInTouch", B, "27.0", "Indica se as abas Visualforce ligadas à página aparecem no app móvel.",
            notas=["A página informa que o campo está descontinuado para o Salesforce Touch."]),
          P("confirmationTokenRequired", B, "28.0", "Indica se requisições GET à página exigem um token de confirmação contra CSRF."),
          P("label", S, None, "Rótulo de exibição da página.", "S"),
          pacotes("16.0", "a página"),
      ], exemplo=CAB + f"""<!-- Arquivo de metadado que acompanha a marcação .page -->
<ApexPage {NS}>
    <description>[o que a página faz]</description>
    <label>[rótulo da página]</label>
</ApexPage>""", estende="MetadataWithContent", curinga=True,
      alertas=["Mudar confirmationTokenRequired de false para true faz os links para a página precisarem de token CSRF; sem ele, a página fica inacessível.",
               "Abas de objeto padrão substituídas por uma página Visualforce não são suportadas no app móvel."],
      cobertura_nota=NOTA_COB)

M.mdt("ApexComponent", S_COMP,
      "Um componente Visualforce: um trecho de marcação reutilizável em páginas Visualforce, com seu arquivo de metadado.",
      "Versionar e implantar componentes Visualforce.", "12.0", [
          P("apiVersion", "double", "16.0", "Versão da API do componente, definida na criação."),
          bin_("content", "O conteúdo do componente (a marcação); herdado de MetadataWithContent.", herdada="MetadataWithContent"),
          P("description", S, None, "Descrição do que o componente faz."),
          P("fullName", S, None, "Nome único de API do componente; herdado. Alfanuméricos e sublinhados; começa com letra.", "?", herdada="Metadata"),
          P("label", S, None, "Rótulo do componente.", "S"),
          pacotes("16.0", "o componente"),
      ], exemplo=CAB + f"""<!-- Arquivo de metadado que acompanha a marcação .component -->
<ApexComponent {NS}>
    <apiVersion>68.0</apiVersion>
    <description>[o que o componente faz]</description>
    <label>[rótulo do componente]</label>
</ApexComponent>""", estende="MetadataWithContent", curinga=True,
      alertas=["Componente Visualforce não é o mesmo que componente de pacote: um pacote pode conter muitos tipos de elemento."],
      cobertura_nota=NOTA_COB + " A página não traz exemplo XML; o exemplo desta ficha é do projeto.")

M.mdt("StaticResource", S_RES,
      "Um static resource: um arquivo guardado na org para uso em páginas e componentes, com o tipo de conteúdo declarado.",
      "Versionar e implantar os arquivos estáticos que o código da org usa.", "12.0", [
          P("cacheControl", "StaticResourceCacheControl", "14.0", "Indica se clientes de terceiros podem guardar o conteúdo em cache.", "S",
            vals=[("Private", None), ("Public", None)]),
          bin_("content", "O conteúdo do arquivo; herdado de MetadataWithContent.", herdada="MetadataWithContent"),
          P("contentType", S, None, "Tipo de conteúdo do arquivo, como text/plain.", "S"),
          P("description", S, None, "Descrição do static resource."),
          P("fullName", S, None, "Nome do static resource; herdado. Deve ser informado ao criar, atualizar ou excluir.", "?", herdada="Metadata"),
      ], exemplo=CAB + f"""<!-- Arquivo de metadado que acompanha o arquivo .resource -->
<StaticResource {NS}>
    <!-- Valores documentados: Private, Public -->
    <cacheControl>Private</cacheControl>
    <contentType>text/plain</contentType>
    <description>[descrição do recurso]</description>
</StaticResource>""", estende="MetadataWithContent", curinga=True,
      alertas=["O static resource só pode ser usado dentro da org: não hospeda conteúdo para outros apps ou sites.",
               "A página do tipo não informa limite de tamanho."],
      cobertura_nota=NOTA_COB)

M.mdt("LightningComponentBundle", S_LWC,
      "Um bundle de Lightning web component: a pasta com os arquivos do componente e o arquivo de configuração .js-meta.xml.",
      "Versionar e implantar Lightning web components e dizer onde cada um pode ser usado.", None, [
          bin_("ai", "Descrição interna do componente para IA, que deixa o Agentforce considerar o componente. Só vale em orgs com Setup with Agentforce ligado.",
               "66.0"),
          P("apiVersion", "double", None, "Prende o componente a uma versão da API da Salesforce."),
          P("capabilities", "Capabilities[]", "48.0", "O que o componente pode fazer, diferente de onde ele pode ser usado.", estrutura="Capabilities"),
          P("description", S, None, "Descrição para o usuário, mostrada em list views e como dica nos builders."),
          P("isExplicitImport", B, None, "Com true, os imports entre arquivos são escritos pelo desenvolvedor; com false, o framework os faz."),
          P("isExposed", B, None,
            "Com true, o componente fica disponível a outros namespaces e, se tiver targets, aos builders; com false, fica escondido dos dois."),
          P("lwcResources", "LwcResources[]", None, "Recursos (arquivos) contidos no bundle.", estrutura="LwcResources"),
          P("masterLabel", S, None, "Título do componente, mostrado em list views."),
          bin_("targetConfigs", "Configuração por target: por exemplo, restringir o componente a páginas de registro de um objeto."),
          P("targets", "Targets[]", None, "Onde o componente pode ser usado, como Lightning App Builder ou sites do Experience Builder.",
            estrutura="Targets"),
      ], exemplo=CAB + f"""<!-- Arquivo <nome do componente>.js-meta.xml, na pasta do componente -->
<LightningComponentBundle {NS}>
    <apiVersion>68.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>[tipo de página em que o componente pode ser usado]</target>
    </targets>
</LightningComponentBundle>""", curinga=True,
      arquivos_prontos=arquivos_bundle("lwc", "<nome do bundle>.js-meta.xml",
                                       "Cada componente fica numa subpasta própria da pasta lwc; o arquivo de configuração se chama "
                                       "<nome do componente>.js-meta.xml. O registro do Salesforce CLI não define sufixo para o tipo.", S_LWC),
      alertas=["Todo Lightning web component precisa do arquivo de configuração .js-meta.xml.",
               "A página informa que componentes só podem ser criados em orgs com namespace definido.",
               "Desde Summer '20, só os usuários internos da org acessam este tipo."],
      cobertura_nota=NOTA_COB + SEM_REQ + " Os valores de target ficam numa referência ligada, não lida.")
sem_versao("LightningComponentBundle", "O artigo do guia versionado não informa a versão de entrada do tipo; só a de campos (capabilities desde 48.0, ai desde 66.0).")
d = ld("metadata-types/LightningComponentBundle.json")
if not any(e["fonte"] == "src:mdapi-ref-lightningcomponentbundle" for e in d["evidencias"]):
    d["evidencias"].append(ev("src:mdapi-ref-lightningcomponentbundle", "Campo estende: a referência nova diz que o tipo estende Metadata."))
sv("metadata-types/LightningComponentBundle.json", d)

M.mdt("AuraDefinitionBundle", S_AURA,
      "Um bundle Aura: a pasta com as definições de um Aura component, app, evento, interface ou coleção de tokens.",
      "Versionar e implantar Aura components, um dos dois tipos de Lightning component (o outro é o Lightning web component).", "32.0", [
          P("apiVersion", "double", "35.0", "Versão da API com que o bundle foi salvo, escolhida na criação."),
          P("auraDefinitions", "AuraDefinitions", None, "Reservado para uso interno da Salesforce.", natureza="desconhecida",
            contexto="A página cita o tipo AuraDefinitions, mas não o descreve."),
          bin_("controllerContent", "Código do controller JavaScript do lado do cliente."),
          P("description", S, "35.0", "Texto que descreve o bundle."),
          bin_("designContent", "Conteúdo da definição de design. Só vale em bundles de componente."),
          bin_("documentationContent", "Conteúdo da definição de documentação."),
          bin_("helperContent", "Conteúdo do helper JavaScript."),
          bin_("markup", "Marcação da definição."),
          bin_("modelContent", "Descontinuado; não deve ser usado."),
          pacotes("35.0", "o bundle"),
          bin_("rendererContent", "Código do renderer JavaScript do lado do cliente."),
          bin_("styleContent", "CSS da definição."),
          bin_("SVGContent", "Imagem SVG da definição."),
          bin_("testsuiteContent", "Reservado para uso interno da Salesforce."),
          P("type", "AuraBundleType", None, "Tipo da definição.", vals=[
              ("Application", None), ("Component", None), ("Event", None), ("Interface", None), ("Tokens", None)]),
      ], exemplo=CAB + f"""<AuraDefinitionBundle {NS}>
    <apiVersion>68.0</apiVersion>
    <description>[o que o bundle faz]</description>
</AuraDefinitionBundle>""", estende=NAO_DECLARADO, curinga=True,
      arquivos_prontos=arquivos_bundle("aura", "<nome do bundle>.<sufixo da definição>",
                                       "Cada bundle é uma pasta própria da pasta aura; os nomes dos arquivos começam com o nome do bundle. Sufixos: "
                                       ".app, .cmp, .design, .evt, .intf, .js (controller, helper ou renderer), .svg, .css, .auradoc e .tokens. "
                                       "O registro do Salesforce CLI não define sufixo para o tipo.", S_AURA),
      alertas=["Cada bundle aceita um só arquivo de cada um destes: .app, .cmp, .design, .evt, .intf e .tokens.",
               "A página informa que definições só podem ser criadas em orgs com namespace definido.",
               "Testes Jest não funcionam com Aura components; só com Lightning web components."],
      cobertura_nota=NOTA_COB + SEM_REQ + " A página não traz exemplo XML de metadado; o exemplo desta ficha é do projeto.")
d = ld("metadata-types/AuraDefinitionBundle.json")
if not any(e["fonte"] == "src:lwc-testing" for e in d["evidencias"]):
    d["evidencias"].append(ev("src:lwc-testing", "Jest só funciona com LWC."))
sv("metadata-types/AuraDefinitionBundle.json", d)

# ================================================================ testes, pacotes e settings
M.mdt("ApexTestSuite", S_SUITE,
      "Uma suíte de testes Apex: uma lista de classes de teste para rodar juntas.",
      "Versionar e implantar os conjuntos de testes que a equipe roda numa execução.", "38.0", [
          P("testClassName", "string[]", None, "Nomes das classes de teste Apex incluídas na suíte."),
      ], exemplo=CAB + f"""<ApexTestSuite {NS}>
    <testClassName>[NomeDaClasseDeTeste]</testClassName>
    <testClassName>[OutraClasseDeTeste]</testClassName>
</ApexTestSuite>""", estende=NAO_DECLARADO, curinga=True,
      alertas=["Testes de classes com namespace são listados por namespace.",
               "Se as classes de teste já existem na org de destino, ApexClass pode ficar fora do package.xml."],
      cobertura_nota=NOTA_COB)

M.mdt("InstalledPackage", S_PKG,
      "Um pacote instalado: a versão de um pacote gerenciado a instalar ou atualizar na org, identificado pelo namespace.",
      "Instalar ou atualizar pacotes gerenciados de primeira geração por deploy.", "28.0", [
          P("activateRSS", B, "43.0", "Com true, mantém o estado ativo dos remote site settings e das configurações de CSP do pacote; com false, força-os a inativos.",
            "S", default=FALSE),
          P("password", S, None, "Senha do pacote."),
          P("securityType", S, "57.0", "Quem tem acesso ao pacote instalado.", default=("valor", "AllUsers", None),
            vals=[("AdminsOnly", None), ("AllUsers", None)],
            contexto="A página lista estes dois valores para um campo do tipo string."),
          P("versionNumber", S, None, "Versão do pacote, no formato major.minor.patch, como 2.1.3.", "S"),
      ], exemplo=CAB + f"""<!-- O arquivo leva o nome do namespace do pacote -->
<InstalledPackage {NS}>
    <activateRSS>false</activateRSS>
    <!-- Valores documentados: AdminsOnly, AllUsers -->
    <securityType>AllUsers</securityType>
    <versionNumber>[major.minor.patch]</versionNumber>
</InstalledPackage>""", estende=NAO_DECLARADO, curinga=True,
      alertas=["InstalledPackage precisa ser o único tipo do manifesto: não se implanta um pacote junto com outros metadata types.",
               "Implantar uma versão mais nova de um pacote instalado faz o upgrade.",
               "Um deploy instala até 20 pacotes gerenciados de primeira geração.",
               "Pacotes desbloqueados e gerenciados de segunda geração não usam este tipo: são instalados pelo comando sf package install."],
      cobertura_nota=NOTA_COB)

CRITICAL = "Ativa o critical update do Winter '20 que {}."
NUM = {"natureza": "numerico", "estado": "verificado", "evidencias": [ev(S_APEXSET)]}
M.mdt("ApexSettings", S_APEXSET,
      "Configurações de Apex da org: opções de teste, de compilação no deploy, de Apex assíncrono e de segurança.",
      "Recuperar e implantar as opções gerais de Apex em vez de marcá-las à mão em cada ambiente.", "47.0", [
          P("asyncApexExecutionsOverride", "integer", "68.0",
            "Reduz o limite licenciado de execuções de Apex assíncrono em 24 horas. Com 0, nulo ou omitido, vale o limite licenciado. Só em orgs que não são de produção.",
            dominio=NUM),
          P("DefaultQueueableDelay", "integer", None, "Atraso mínimo, em segundos, para jobs enfileirados sem atraso próprio. Aceita de 1 a 600.",
            dominio=NUM, notas=["O nome do campo começa com maiúscula na página."]),
          P("enableAggregateCodeCoverageOnly", B, None, "Guarda só o total agregado da cobertura de testes Apex, em vez dos dados detalhados.", default=FALSE),
          P("enableApexAccessRightsPref", B, None, "Descontinuado."),
          P("enableApexApprovalLockUnlock", B, None, "Permite que código Apex bloqueie e desbloqueie registros em processos de aprovação.", default=FALSE),
          P("enableApexCtrlImplicitWithSharingPref", B, None,
            CRITICAL.format("aplica with sharing a controllers @AuraEnabled com compartilhamento implícito")),
          P("enableApexPropertyGetterPref", B, None, CRITICAL.format("faz valer os modificadores de acesso de propriedades Apex na marcação Lightning")),
          P("enableAsyncApexElasticExecutions", B, "67.0", "Liga os limites elásticos de jobs de Apex assíncrono.", default=FALSE,
            notas=["A página marca o recurso como Beta."]),
          P("enableAuraApexCtrlAuthUserAccessCheckPref", B, None,
            CRITICAL.format("restringe métodos @AuraEnabled conforme o perfil, para usuários autenticados")),
          P("enableAuraApexCtrlGuestUserAccessCheckPref", B, None,
            CRITICAL.format("restringe métodos @AuraEnabled conforme o perfil, para usuários guest e de portal")),
          P("enableBlockPackagedApexExecAnon", B, "67.0", "Liga o release update que bloqueia a execução de Apex anônimo vindo de pacotes gerenciados.",
            default=FALSE),
          P("enableCompileOnDeploy", B, None, "Recompila o Apex em deploys, instalações e upgrades de pacote.",
            notas=["Padrão true em produção e em sandboxes Full, e false nas demais orgs. Não pode ser desligado em produção."]),
          P("enableDisableParallelApexTesting", B, None, "Com true, os testes Apex rodam em série. Os testes de um deploy sempre rodam em série.", default=FALSE),
          P("enableDebugLogsDuringDeployment", B, None, "Gera logs de depuração durante o deploy de metadados, só quando há uma trace flag ativa.", default=FALSE),
          P("enableEnforceSummer26ApexHeapLimit", B, "68.0", "Restringe orgs que não são de produção aos limites menores de heap do Summer '26.",
            default=FALSE, notas=["A página informa que o campo vale só no Winter '27 (API 68.0)."]),
          P("enableGaplessTestAutoNum", B, None, "Impede que execuções de teste avancem campos autonumber de registros que não são de teste.", default=TRUE),
          P("enableMngdCtrlActionAccessPref", B, None, CRITICAL.format("desliga métodos não globais de controllers Apex em pacotes gerenciados")),
          P("enableNonCertifiedApexMdCrud", B, None, "Permite que classes Apex acessem metadados pelo namespace Metadata.", default=FALSE),
          P("enableRestrictCommunityExecAnon", B, None, "Impede usuários guest de rodar Apex anônimo, qualquer que seja a permissão Author Apex.", default=TRUE),
          P("enableSecureNoArgConstructorPref", B, None, "Não usado: o critical update correspondente é aplicado automaticamente."),
          P("enableTestSetupSkipTestResults", B, "61.0", "Com false, os métodos @TestSetup geram resultados de teste; com true, não geram."),
          FULLNAME,
      ], exemplo=CAB + f"""<ApexSettings {NS}>
    <!-- true = testes Apex em série -->
    <enableDisableParallelApexTesting>true</enableDisableParallelApexTesting>
</ApexSettings>""", arquivos_prontos=M.arquivos_settings("ApexSettings", "Apex", S_APEXSET), curinga=False,
      alertas=["No package.xml, use o tipo Settings com o membro Apex; o curinga só vale para recuperar todas as configurações.",
               "enableDisableParallelApexTesting tem nome enganoso: true quer dizer rodar em série.",
               "enableTestSetupSkipTestResults tem lógica invertida: false gera os resultados."],
      cobertura_nota=NOTA_COB + SEM_REQ)

M.mdt("DevHubSettings", S_DEVHUB,
      "Configurações do Dev Hub: ligam scratch orgs, empacotamento de segunda geração, Org Shape, snapshots e o DevOps Center.",
      "Recuperar e implantar as opções do Dev Hub em vez de marcá-las à mão.", "47.0", [
          P("enableALMDevopsCorePref", B, "65.0", "Liga o DevOps Center de nova geração, para gestão de mudanças e de releases."),
          P("enableDevOpsCenterGA", B, "56.0", "Liga o pacote gerenciado DevOps Center, a versão anterior."),
          P("enableALMSimpleDeployDataPref", B, "65.0", "Permite migrar dados de configuração para uma org de destino. Exige enableALMSimpleDeployPref."),
          P("enableALMSimpleDeployPref", B, "65.0", "Permite implantar metadados de uma org numa org de destino."),
          P("enableDevopsCenterMigrationPref", B, "67.0", "Permite migrar projetos do pacote gerenciado DevOps Center para a versão de nova geração.",
            notas=["A página marca o recurso como developer preview."]),
          P("enablePackaging2", B, None, "Liga os pacotes desbloqueados e os pacotes gerenciados de segunda geração. Exige enableScratchOrgManagementPref."),
          P("enableScratchOrgManagementPref", B, None, "Liga o Dev Hub, que cria e gerencia scratch orgs."),
          P("enableScratchOrgSnapshotPref", B, "61.0", "Liga os snapshots de scratch orgs configuradas, usados para criar outras scratch orgs."),
          P("enableShapeExportPref", B, "55.0", "Liga o Org Shape, que cria shapes usados como base de scratch orgs."),
          FULLNAME,
      ], exemplo=CAB + f"""<DevHubSettings {NS}>
    <!-- enablePackaging2 exige enableScratchOrgManagementPref -->
    <enablePackaging2>true</enablePackaging2>
    <enableScratchOrgManagementPref>true</enableScratchOrgManagementPref>
</DevHubSettings>""", arquivos_prontos=M.arquivos_settings("DevHubSettings", "DevHub", S_DEVHUB), curinga=False,
      alertas=["No package.xml, use o tipo Settings com o membro DevHub; o curinga só vale para recuperar todas as configurações.",
               "Depois de ligados, o Dev Hub e o empacotamento de segunda geração não podem ser desligados."],
      cobertura_nota=NOTA_COB + SEM_REQ + " A página não declara defaults.")
d = ld("metadata-types/DevHubSettings.json")
if not any(e["fonte"] == "src:pkg2-enable-devhub" for e in d["evidencias"]):
    d["evidencias"].append(ev("src:pkg2-enable-devhub", "Dev Hub e empacotamento 2GP não podem ser desligados."))
sv("metadata-types/DevHubSettings.json", d)

M.mdt("SourceTrackingSettings", S_TRACK,
      "Configuração de source tracking em sandboxes: liga o rastreamento automático de mudanças em sandboxes Developer e Developer Pro.",
      "Recuperar e implantar a opção que faz as sandboxes de desenvolvimento rastrearem o que mudou.", "49.0", [
          P("enableSourceTrackingSandboxes", B, None,
            "Liga o source tracking automático quando sandboxes Developer ou Developer Pro são criadas ou atualizadas (refresh).", default=FALSE),
          FULLNAME,
      ], exemplo=CAB + f"""<SourceTrackingSettings {NS}>
    <enableSourceTrackingSandboxes>true</enableSourceTrackingSandboxes>
</SourceTrackingSettings>""", arquivos_prontos=M.arquivos_settings("SourceTrackingSettings", "SourceTracking", S_TRACK), curinga=False,
      alertas=["A página marca o tipo como Beta.",
               "O campo só vale em orgs de produção; nas demais é ignorado.",
               "Voltar a false não para o rastreamento numa sandbox que já rastreia: ele continua até o próximo refresh dela.",
               "Não é preciso ter o Dev Hub ligado na mesma org."],
      cobertura_nota=NOTA_COB)

M.mdt("DeploymentSettings", S_DEPLOY,
      "Configuração de deploy da org: decide se os deploys pulam a validação de Apex assíncrono.",
      "Recuperar e implantar a opção que protege deploys de classes usadas por jobs em execução.", "47.0", [
          P("doesSkipAsyncApexValidation", B, None,
            "Indica se os deploys pulam a validação de Apex assíncrono. Use false quando uma classe do pacote é usada por um job em lote que pode rodar "
            "durante o deploy.", default=TRUE),
          FULLNAME,
      ], exemplo=CAB + f"""<DeploymentSettings {NS}>
    <doesSkipAsyncApexValidation>true</doesSkipAsyncApexValidation>
</DeploymentSettings>""", arquivos_prontos=M.arquivos_settings("DeploymentSettings", "Deployment", S_DEPLOY), curinga=False,
      alertas=["No package.xml, use o tipo Settings com o membro Deployment.",
               "Sem a validação, o deploy de um pacote com uma classe usada por um job em lote em execução falha."],
      cobertura_nota=NOTA_COB)

M.emit_structs()

# ================================================================ funcionalidades
DEV = "desenvolvimento-testes-e-entrega"
SEM_OBJ = {"tipo": "objeto_api", "estado": "desconhecido",
           "motivo": "Objetos API do tema não investigados na rodada A1; a lista vazia não comprova inexistência."}
SETUP_DESCONHECIDO = af("desconhecido", None, "Caminho de Setup não confirmado nas fontes lidas.", [])


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


def sem_mdt(estado, motivo):
    return {"tipo": "metadata_type", "estado": estado, "motivo": motivo}


C.funcionalidade(
    "classes-apex", "Classes Apex", "Apex Classes", ["apex", "apex class", "classe apex", "código apex"],
    "Código escrito em Apex, a linguagem da plataforma, organizado em classes. Cada classe é um componente com o código-fonte e um arquivo de "
    "metadado.",
    "Implementar lógica de negócio que a configuração declarativa não cobre, com testes e versionamento.",
    "Uma classe calcula o desconto de um pedido e é chamada por um trigger e por um flow.",
    (DEV, "codigo-e-bundles"), [],
    [("ApexClass", "Cada classe Apex, com código e arquivo de metadado."), ("ApexSettings", "Opções gerais de Apex da org.")], [],
    [S_CLS, S_APEXSET, "src:apex-choose-org", "src:apex-code-coverage"], [SEM_OBJ], SETUP_DESCONHECIDO,
    limitacoes=["Para implantar Apex, os testes precisam cobrir ao menos 75% do código Apex e passar."],
    alertas=["Não se desenvolve Apex direto em produção: usa-se sandbox, scratch org ou Developer Edition.",
             "Por padrão, uma classe com jobs Apex ativos não pode ser atualizada por deploy."])

C.funcionalidade(
    "lightning-web-components", "Lightning Web Components", "Lightning Web Components (LWC)", ["lwc", "lightning web component", "componente lwc"],
    "Componentes de interface escritos em HTML e JavaScript. Cada componente é uma pasta (bundle) com seus arquivos e um arquivo de "
    "configuração .js-meta.xml, que diz onde ele pode ser usado.",
    "Construir interface sob medida quando os componentes padrão e a configuração declarativa não bastam.",
    "Um componente mostra o saldo do cliente na página de registro da conta; o arquivo de configuração o libera para record pages.",
    (DEV, "codigo-e-bundles"), [],
    [("LightningComponentBundle", "O bundle do componente e seu arquivo de configuração.")], [],
    [S_LWC, "src:lwc-config-file", "src:lwc-testing", "src:lwc-third-party"], [SEM_OBJ], SETUP_DESCONHECIDO,
    limitacoes=["O arquivo JavaScript de um componente tem até 1 MB."],
    alertas=["Sem o arquivo de configuração .js-meta.xml, o envio do componente à org dá erro."])

C.funcionalidade(
    "aura-components", "Aura Components", "Aura Components", ["aura", "aura component", "lightning components (aura)"],
    "Um dos dois tipos de Lightning component; o outro é o Lightning web component. Cada bundle é uma pasta com arquivos de marcação, controller, "
    "helper, estilo e outros.",
    "Manter e evoluir componentes de interface construídos em Aura; a documentação de LWC traz a correspondência dos arquivos para migrar.",
    "Um bundle antigo tem sample.cmp, sampleController.js e sampleHelper.js; num LWC, a marcação vai para sample.html e os dois .js viram um só.",
    (DEV, "codigo-e-bundles"), [],
    [("AuraDefinitionBundle", "O bundle Aura, com suas definições.")], [],
    [S_AURA, "src:lwc-migrate-bundles", "src:lwc-testing"], [SEM_OBJ], SETUP_DESCONHECIDO,
    alertas=["Testes Jest não funcionam com Aura components.",
             "Cada bundle aceita um só arquivo de cada tipo principal (.app, .cmp, .design, .evt, .intf, .tokens)."])

C.funcionalidade(
    "visualforce", "Visualforce", "Visualforce", ["visualforce page", "página visualforce", "apex page", "componente visualforce"],
    "Framework de páginas baseado em marcação própria. Páginas e componentes Visualforce são componentes de código, cada um com sua "
    "marcação e um arquivo de metadado.",
    "Manter páginas sob medida já existentes na org.",
    "Uma página Visualforce antiga gera a proposta em formato de impressão a partir de uma oportunidade.",
    (DEV, "codigo-e-bundles"), [],
    [("ApexPage", "Cada página Visualforce."), ("ApexComponent", "Cada componente Visualforce reutilizável.")], [],
    [S_PAGE, S_COMP], [SEM_OBJ], SETUP_DESCONHECIDO,
    alertas=["Abas de objeto padrão substituídas por página Visualforce não são suportadas no app móvel."])

C.funcionalidade(
    "static-resources", "Static resources", "Static Resources", ["static resource", "recurso estático", "arquivos estáticos"],
    "Arquivos guardados na org para uso por páginas e componentes, como uma biblioteca JavaScript carregada por um Lightning web component.",
    "Empacotar e versionar, junto com o código, os arquivos que a interface customizada usa.",
    "Uma biblioteca JavaScript de gráficos é enviada como static resource e carregada por um Lightning web component.",
    (DEV, "codigo-e-bundles"), [],
    [("StaticResource", "Cada static resource, com o arquivo e o metadado.")], [],
    [S_RES, "src:lwc-third-party"], [SEM_OBJ], SETUP_DESCONHECIDO,
    limitacoes=["Até 5 MB por static resource e 250 MB por org."],
    alertas=["O static resource só pode ser usado dentro da org."])

C.funcionalidade(
    "testes-apex", "Testes Apex", "Apex Tests", ["apex test", "teste unitário apex", "@istest", "code coverage", "cobertura de código", "test suite"],
    "Testes unitários escritos em Apex: métodos de classes anotadas com @IsTest que conferem se o código funciona. A plataforma mede a "
    "cobertura, isto é, quanto do código Apex os testes executam.",
    "Garantir que o código funciona antes de chegar à produção; a plataforma exige cobertura mínima para implantar.",
    "Antes do deploy, os testes locais rodam; se um falha, o deploy inteiro é revertido.",
    (DEV, "testes"), [],
    [("ApexTestSuite", "Suíte que agrupa classes de teste para rodar juntas."), ("ApexSettings", "Opções de execução e de cobertura dos testes.")], [],
    ["src:apex-writing-tests", "src:apex-code-coverage", "src:apex-testing-best-practices", "src:sfdx-run-apex-tests", "src:migration-running-tests",
     S_SUITE, S_APEXSET], [SEM_OBJ],
    setup("Setup > Apex Test Execution", "src:sfdx-run-apex-tests", "Tela de execução de testes; em Options fica Store Only Aggregate Code Coverage."),
    limitacoes=["Os testes precisam cobrir ao menos 75% do código Apex e passar, para implantar ou empacotar.",
                "Chamadas a System.debug e as próprias classes e métodos de teste não contam na cobertura."],
    alertas=["Cobertura indica, mas não garante, que os testes são eficazes: o teste precisa verificar o comportamento."])

C.funcionalidade(
    "testes-jest-de-lwc", "Testes Jest de LWC", "Jest Tests for Lightning Web Components", ["jest", "sfdx-lwc-jest", "teste unitário lwc", "__tests__"],
    "Testes unitários de Lightning web components, escritos em JavaScript com Jest. Rodam na máquina do desenvolvedor ou no pipeline, sem "
    "navegador e sem conexão com a org.",
    "Conferir cada componente isoladamente e rápido, a cada mudança.",
    "A pasta __tests__ do componente tem um arquivo .test.js que confere o que o componente mostra depois de um clique.",
    (DEV, "testes"), [], [], [],
    ["src:lwc-testing", "src:lwc-component-tests", "src:lwc-jest-create", "src:lwc-e2e"],
    [sem_mdt("nao_aplicavel", "Os testes Jest ficam na pasta __tests__ do projeto; a documentação manda configurar o projeto para que essa pasta "
                              "nunca seja salva na org. Não há componente de metadado."),
     {"tipo": "objeto_api", "estado": "nao_aplicavel", "motivo": "Os testes rodam fora da org e não geram registros."}],
    af("nao_aplicavel", None, "Não há tela de Setup: os testes rodam fora da org.", []),
    alertas=["Só funcionam com Lightning web components, não com Aura.",
             "Testes de interface que dependem do HTML e do DOM do Lightning Experience quebram com mudanças da plataforma; ficam para ponta a ponta."])

C.funcionalidade(
    "pacotes-desbloqueados", "Pacotes desbloqueados", "Unlocked Packages", ["unlocked package", "unlocked packages", "pacote desbloqueado", "package version"],
    "Um pacote é um contêiner de metadados relacionados. No pacote desbloqueado, a fonte da verdade é o controle de versão, e o metadado "
    "instalado pode ser alterado direto na org. Cada mudança no conteúdo gera uma nova versão do pacote.",
    "Organizar o metadado da org em partes instaláveis e atualizáveis, com dependências declaradas entre elas.",
    "A equipe separa as customizações de atendimento num pacote; cada entrega vira uma versão, instalada primeiro na sandbox e depois em produção.",
    (DEV, "pacotes-e-dependencias"), [],
    [("DevHubSettings", "Liga o empacotamento de segunda geração (enablePackaging2), que inclui os pacotes desbloqueados.")], [],
    ["src:sfdx-unlocked-intro", "src:sfdx-unlocked-whats", "src:sfdx-package-dev-model", "src:sfdx-devhub-enable", S_DEVHUB, S_PKG], [SEM_OBJ],
    setup("Setup > Quick Find: Dev Hub > Dev Hub", "src:sfdx-devhub-enable", "Tela em que se liga o Dev Hub, pré-requisito do empacotamento."),
    alertas=["Como o metadado pode ser alterado direto em produção, um upgrade do pacote pode sobrescrever mudanças feitas à mão: combine a governança.",
             "Pacotes desbloqueados são instalados pelo Salesforce CLI (sf package install), não pelo tipo InstalledPackage."])

C.funcionalidade(
    "pacotes-gerenciados", "Pacotes gerenciados", "Managed Packages", ["managed package", "2gp", "second-generation managed packages", "pacote gerenciado",
                                                                       "installed package"],
    "Pacotes voltados à distribuição de apps a vários clientes, com regras que definem o que pode mudar em cada componente depois de "
    "instalado. Os de segunda geração (2GP) usam o controle de versão como fonte da verdade e o Salesforce CLI.",
    "Distribuir um app a várias orgs e atualizá-lo de forma controlada; do lado de quem instala, receber e atualizar apps de parceiros.",
    "A org instala a versão 2.1.3 de um app de um parceiro; um deploy posterior com versão mais nova faz o upgrade.",
    (DEV, "pacotes-e-dependencias"), [],
    [("InstalledPackage", "Versão de um pacote gerenciado de primeira geração a instalar ou atualizar por deploy."),
     ("DevHubSettings", "Liga o empacotamento de segunda geração (enablePackaging2).")], [],
    ["src:pkg2-intro", "src:pkg2-key-concepts", "src:pkg2-enable-devhub", "src:sfdx-unlocked-whats", S_PKG, S_DEVHUB], [SEM_OBJ], SETUP_DESCONHECIDO,
    limitacoes=["Um deploy instala até 20 pacotes gerenciados de primeira geração, e InstalledPackage precisa ser o único tipo do manifesto."],
    alertas=["Depois de ligado, o empacotamento de segunda geração não pode ser desligado.",
             "Para quem não vai distribuir a vários clientes, a documentação indica pacotes desbloqueados."])

C.funcionalidade(
    "projeto-salesforce-dx", "Projeto Salesforce DX", "Salesforce DX Project", ["sfdx project", "sfdx-project.json", "source format", "package.xml",
                                                                             "metadata format", "force-app"],
    "A estrutura de pastas e arquivos em que o metadado da org fica no computador e no controle de versão. O arquivo sfdx-project.json "
    "identifica o projeto. Os componentes ficam em source format; o manifesto package.xml lista o que recuperar ou implantar.",
    "Guardar código e configuração num repositório, no formato que as ferramentas e o controle de versão trabalham melhor.",
    "Um objeto customizado, que no Metadata API format é um único arquivo .object, vira no projeto uma pasta com um arquivo por campo.",
    (DEV, "source-format-e-metadata-api-format"), [], [], [],
    ["src:sfdx-project-setup", "src:sfdx-project-config", "src:sfdx-decomposed", "src:sfdx-convert-mdapi", "src:cli-convert-source",
     "src:vscode-source-format", "src:mdapi-zip-file"],
    [sem_mdt("nao_aplicavel", "É a estrutura local de pastas e arquivos do projeto, não um componente da org. Cada metadata type do catálogo "
                              "mostra a própria pasta e o sufixo nos dois formatos."),
     {"tipo": "objeto_api", "estado": "nao_aplicavel", "motivo": "O projeto é local; não há registro correspondente na org."}],
    af("nao_aplicavel", None, "Não há tela de Setup: o projeto fica fora da org.", []),
    alertas=["O sourceApiVersion do projeto define que campos de cada metadata type são recuperados e implantados."])

C.funcionalidade(
    "sandboxes", "Sandboxes", "Sandboxes", ["sandbox", "developer sandbox", "partial copy", "full sandbox", "refresh de sandbox"],
    "Cópias da org de produção em ambientes separados e isolados, para desenvolver, testar e treinar. Há quatro tipos: Developer e "
    "Developer Pro copiam a configuração (metadados); Partial Copy é um ambiente de teste cujos dados vêm de um sandbox template; Full é uma "
    "réplica com todos os dados e metadados.",
    "Mudar e testar sem risco para a produção.",
    "A equipe desenvolve numa sandbox Developer, faz o teste de aceitação numa Partial Copy e ensaia o deploy numa Full.",
    (DEV, "ambientes-e-sandboxes"), [],
    [("SourceTrackingSettings", "Liga o source tracking nas sandboxes Developer e Developer Pro.")], [],
    ["src:help-sandbox-types", "src:help-sandbox-refresh", "src:help-sandbox-licenses", S_TRACK], [SEM_OBJ], SETUP_DESCONHECIDO,
    limitacoes=["Intervalo mínimo entre refreshes: 1 dia (Developer e Developer Pro), 5 dias (Partial Copy) e 29 dias (Full).",
                "A quantidade de sandboxes de cada tipo depende da edição; é possível comprar adicionais."],
    alertas=["Ao criar ou atualizar uma Partial Copy, escolhe-se o sandbox template que define os dados copiados.",
             "O intervalo de refresh conta a partir do pedido de criação ou de refresh."])

C.funcionalidade(
    "scratch-orgs-e-dev-hub", "Scratch orgs e Dev Hub", "Scratch Orgs and Dev Hub", ["scratch org", "dev hub", "org shape", "scratch org definition file",
                                                                                   "snapshot"],
    "Scratch orgs são orgs temporárias e configuráveis, criadas pelo Salesforce CLI a partir de um arquivo de definição. O Dev Hub é a org "
    "que as cria e gerencia, junto com pacotes e namespaces.",
    "Ter um ambiente limpo e descartável para cada tarefa, montado a partir do que está no controle de versão.",
    "Para testar uma mudança, o desenvolvedor cria uma scratch org de 7 dias, envia o código do projeto e roda os testes.",
    (DEV, "ambientes-e-sandboxes"), [],
    [("DevHubSettings", "Liga o Dev Hub, o Org Shape e os snapshots de scratch org.")], [],
    ["src:sfdx-scratch-orgs", "src:sfdx-scratch-editions", "src:sfdx-devhub-enable", "src:sfdx-snapshots", S_DEVHUB], [SEM_OBJ],
    setup("Setup > Quick Find: Dev Hub > Dev Hub", "src:sfdx-devhub-enable", "Tela em que se liga o Dev Hub."),
    limitacoes=["Uma scratch org dura de 1 a 30 dias; o padrão é 7.", "Armazenamento de uma scratch org: 500 MB de dados e 50 MB de arquivos.",
                "A edição do Dev Hub define quantas scratch orgs podem ser criadas por dia e quantas ficam ativas."],
    alertas=["A scratch org nasce vazia: sem objetos customizados, perfis, permission sets nem código.",
             "Depois de ligado, o Dev Hub não pode ser desligado."])

C.funcionalidade(
    "change-sets", "Change sets", "Change Sets", ["change set", "outbound change set", "inbound change set", "deployment connection"],
    "Forma de enviar customizações de uma org a outra pela interface do Setup: monta-se um outbound change set na origem e faz-se o "
    "deploy do inbound change set no destino. Só funciona entre orgs ligadas à mesma produção.",
    "Levar mudanças da sandbox para a produção sem ferramentas de linha de comando.",
    "O administrador cria um objeto na sandbox, envia num change set e, em produção, valida e implanta.",
    (DEV, "versionamento-deploy-e-recuperacao"), [], [], [],
    ["src:help-change-sets", "src:help-change-sets-connections", "src:help-change-sets-outbound", "src:help-change-sets-best",
     "src:help-change-sets-deploy", "src:help-lifecycle-center"],
    [sem_mdt("desconhecido", "Não foi lido se o próprio change set ou a deployment connection têm metadata type; o conteúdo de um change set são "
                             "componentes de metadado."), SEM_OBJ],
    setup("Setup > Quick Find: Outbound Change Sets", "src:help-change-sets-deploy", "Lista dos outbound change sets da org de origem."),
    limitacoes=["Um change set tem até 10.000 arquivos e 400 MB; a recomendação é não passar de cerca de 5.000 componentes.",
                "Só leva o que se altera pelo Setup; não leva dados (registros)."],
    alertas=["Enviar não implanta: a org de destino precisa fazer o deploy do change set.",
             "Inclua os componentes dependentes que não existem no destino, ou o deploy falha.",
             "A org de origem fica bloqueada durante a validação, e a de destino durante o deploy."])

C.funcionalidade(
    "devops-center", "DevOps Center e Lifecycle Center", "DevOps Center / Lifecycle Center", ["devops center", "lifecycle center", "work item", "pipeline",
                                                                                            "pipeline stage"],
    "Ferramenta de gestão de mudanças e de releases que registra configuração e código num sistema de controle de versão. O trabalho é "
    "dividido em work items, que avançam por um pipeline de estágios; cada estágio corresponde a uma org e a um branch.",
    "Dar a quem configura por cliques e a quem programa o mesmo caminho de entrega, com histórico no controle de versão.",
    "Um work item é promovido do estágio de integração para o de UAT: o branch é mesclado e a mudança é implantada na org de UAT.",
    (DEV, "versionamento-deploy-e-recuperacao"), [],
    [("DevHubSettings", "Liga o DevOps Center (enableDevOpsCenterGA) e a versão de nova geração (enableALMDevopsCorePref).")], [],
    ["src:help-lifecycle-center", "src:help-devops-pipeline-plan", "src:help-devops-promote", "src:help-devops-center-mp", "src:help-devops-setup",
     S_DEVHUB], [SEM_OBJ], SETUP_DESCONHECIDO,
    limitacoes=["Repositórios suportados pelo pacote gerenciado: GitHub na nuvem; Bitbucket Cloud em beta.",
                "Recomendação de cerca de 50 work items ou menos por estágio sem bundle."],
    alertas=["O pipeline não pode ser alterado depois que alguma mudança é promovida por ele: planeje antes.",
             "Os ambientes de desenvolvimento precisam ter source tracking: sandboxes Developer ou Developer Pro, ou scratch orgs.",
             "A Ajuda usa dois nomes: DevOps Center (Managed Package), a versão anterior, e Lifecycle Center."])

# Ligações com o que já existia
C.ampliar_funcionalidade("metadata-api", mdts=[("DeploymentSettings", "Opção de deploy da org: validação de Apex assíncrono.")], srcs=[S_DEPLOY])
C.ampliar_funcionalidade("apex-triggers", mdts=[("ApexSettings", "Opções gerais de Apex da org.")], srcs=[S_APEXSET])

print("lote 7b: 12 metadata types, 5 estruturas e 14 funcionalidades gravados; 2 funcionalidades ampliadas")
