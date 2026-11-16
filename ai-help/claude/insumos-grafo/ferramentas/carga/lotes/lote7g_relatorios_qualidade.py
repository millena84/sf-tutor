"""Lote 7g (rodadas B2 e B3, issue #34): catálogo dos temas Relatórios, analytics e exploração e Qualidade, governança e ciclo de vida.

Lê o guia versionado 264.0 (API 68.0) e cadastra 7 metadata types: Report e Dashboard (só o primeiro nível), ReportType,
ReportFolder e DashboardFolder (página Folder), DuplicateRule e MatchingRules. Cria 5 funcionalidades. As fontes de Ajuda
citadas já estavam registradas (rodadas de texto dos dois temas).

Ordem: lote7f_conteudo_ia.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7g_relatorios_qualidade.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga.base import af, ev, ld, sv, caminho  # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-16"
EXTR = "fontes/extracoes/mdapi-lote7g-relatorios-qualidade.txt"
ATLAS = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
PAGINAS = {"Report": "meta_report", "Dashboard": "meta_dashboard", "ReportType": "meta_reporttype", "Folder": "meta_folder",
           "DuplicateRule": "meta_duplicaterule", "MatchingRules": "meta_matchingrule"}


def substituir_fontes(novas):
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


substituir_fontes([C.fonte(f"src:mdapi-{n.lower()}", f"{n} (Metadata API)", ATLAS + pag + ".htm", f"Arquivo, versão e propriedades de {n}.",
                           EXTR, DATA) for n, pag in PAGINAS.items()])
S_REP, S_DASH, S_RT, S_FOLDER, S_DR, S_MR = (f"src:mdapi-{n.lower()}" for n in PAGINAS)

NOTA_COB = "Universo esperado = tabelas Fields da página do guia versionado 264.0 (API 68.0), lida em 2026-11-16."
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
B, S, I = "boolean", "string", "int"
REGISTRADOS = []


def valores(*vs):
    return [(v, None) for v in vs]


def estrutura(nome, src, usada_por, rows, o_que_e):
    M.struct(nome, src, usada_por, rows, o_que_e)
    REGISTRADOS.append((src, "estruturas", nome))


def tipo(nome, src, *a, **k):
    M.mdt(nome, src, *a, **k)
    REGISTRADOS.append((src, "metadata-types", nome))


def em_pasta(pasta, arquivo, nota, chave, src):
    a = af("verificado", {"pasta": pasta, "arquivo": arquivo}, nota, [ev("src:sdr-registry", f"types.{chave}"), ev(src)])
    return {"source_format": a, "metadata_api_format": a}


RESTAURA = ("Reimplantar um componente com o mesmo fullName de um excluído restaura o original, mesmo já fora da Lixeira, com o Id, a data e o "
            "autor de criação originais.")
SEM_DET = "A página tem {} caracteres; só os primeiros 100.000 foram lidos. Os subtipos {} não foram cadastrados."

# ================================================================ Report
tipo("Report", S_REP,
     "Um relatório customizado: tipo de relatório, formato, colunas, agrupamentos, filtros, fórmulas e gráfico.",
     "Versionar e implantar os relatórios da org entre ambientes.", "14.0", [
         P("aggregateFilters", "ReportAggregateFilter[]", "64.0", "Filtros sobre summary formulas customizadas."),
         P("aggregates", "ReportAggregate[]", None, "Summary formulas customizadas, em relatórios summary, matrix e joined."),
         P("block", "Report[]", None, "Os blocos de um joined report; cada bloco tem o próprio tipo de relatório.", natureza="tipo_composto",
           contexto="Cada bloco é um Report aninhado."),
         P("blockInfo", "ReportBlockInfo", None, "Atributos de cada bloco de um joined report."),
         P("buckets", "ReportBucketField[]", "24.0", "Bucket fields usados no relatório."),
         P("chart", "ReportChart", None, "Gráfico de relatórios summary e matrix."),
         P("colorRanges", "ReportColorRange[]", None, "Destaque condicional de dados resumidos. Só no Salesforce Classic."),
         P("columns", "ReportColumn[]", None, "Campos mostrados; a ordem de exibição segue a ordem no arquivo."),
         P("crossFilters", "ReportCrossFilter[]", "68.0", "Cross filters: objeto, objeto relacionado e condição com ou sem."),
         P("currency", "CurrencyIsoCode", None, "Moeda dos valores convertidos, em código ISO 4217, como USD.", natureza="desconhecida",
           contexto="A página não lista os códigos."),
         P("dataCategoryFilters", S, None, "Filtros por data category."),
         P("description", S, None, "Descrição mostrada com o nome do relatório; até 255 caracteres."),
         P("division", S, "17.0", "Os registros precisam ser desta division."),
         P("filter", "ReportFilter", None, "Limita o resultado a registros com certos dados."),
         P("folderName", S, "35.0", "Pasta que contém o relatório."),
         P("format", "ReportFormat", None, "Formato do relatório, como Tabular.", natureza="desconhecida",
           contexto="A tabela do campo não lista os valores da enumeração."),
         P("formattingRules", "ReportFormattingRule[]", None, "Destaque condicional. Só no Lightning Experience."),
         P("groupingsAcross", "ReportGrouping[]", None, "Agrupamentos de coluna de um relatório matrix; no máximo 2."),
         P("groupingsDown", "ReportGrouping[]", None, "Agrupamentos de linha: até 2 em matrix e até 3 em summary."),
         P("historicalSelector", "ReportHistoricalSelector", "29.0", "Intervalo de datas dos dados de historical trending."),
         P("isSmartTotalDisabled", B, "29.0", "Com false, o relatório mostra o smart totalling."),
         P("name", S, None, "Nome do relatório.", "S"),
         P("numSubscriptions", I, "38.0", "1 se o usuário assina o relatório; 0 se não."),
         P("params", "ReportParam[]", None, "Opções de filtro próprias do tipo de relatório."),
         P("customDetailFormulas", "CustomDetailFormulas", None, "Row-level formulas."),
         P("reportType", S, None, "Tipo de dados do relatório, como Opportunity.", "S"),
         P("reportTypeApiName", S, "48.0", "Nome de API do tipo de relatório."),
         P("roleHierarchyFilter", S, "17.0", "Nome do papel usado para detalhar a hierarquia de papéis."),
         P("rowLimit", I, None, "Máximo de linhas devolvidas."),
         P("scope", S, None, "Escopo dos dados; os valores válidos dependem de reportType."),
         P("showCommonRowsOnly", B, "67.0", "Mostra só as linhas em comum.", default=("false", False, "A página declara default false.")),
         P("showCurrentDate", B, "29.0", "Com true, vale para relatórios matrix de historical trending."),
         P("showDetails", B, None, "Com false, o relatório mostra só cabeçalhos, subtotais e totais.",
           default=("valor", True, "A página declara default true.")),
         P("showGrandTotal", B, None, "Com true, mostra o total geral."),
         P("showSubTotals", B, None, "Com true, mostra os subtotais de cada seção."),
         P("sortColumn", S, None, "Campo de ordenação; usado com sortOrder."),
         P("sortOrder", "SortOrder", None, "Direção da ordenação.", vals=valores("Asc", "Desc")),
         P("territoryHierarchyFilter", S, "17.0", "Nome do território usado para detalhar a hierarquia de territórios."),
         P("timeFrameFilter", "ReportTimeFrameFilter", None, "Limita o resultado a um período."),
         P("userFilter", S, "17.0", "Nome de usuário usado para detalhar."),
         M.FULLNAME_HERDADO(None),
     ], exemplo=CAB + f"""<Report {NS}>
    <description>[o que o relatório responde]</description>
    <name>[nome do relatório]</name>
    <reportType>Opportunity</reportType>
    <showDetails>true</showDetails>
    <showGrandTotal>true</showGrandTotal>
    <sortColumn>[campo de ordenação]</sortColumn>
    <!-- Valores documentados: Asc, Desc -->
    <sortOrder>Asc</sortOrder>
</Report>""", curinga=False,
     arquivos_prontos=em_pasta("reports/<pasta>/", "<Nome>.report",
                               "Os relatórios ficam em subpastas da pasta reports. No source format, o arquivo recebe o sufixo -meta.xml.",
                               "report", S_REP),
     alertas=["Só relatórios customizados: os relatórios padrão não são suportados.",
              "O curinga (*) não funciona: liste as pastas com listMetadata() do tipo ReportFolder e depois os relatórios de cada pasta.",
              "Para referenciar só uma pasta aninhada, o nome dela precisa terminar com barra; sem a barra, a operação falha.",
              RESTAURA],
     cobertura_nota=NOTA_COB + " Primeiro nível: 40 de 40 campos. " + SEM_DET.format(
         "238.060", "(ReportAggregate, ReportBucketField, ReportGrouping, ReportChart, ReportColumn, ReportFilter e os demais)"))

# ================================================================ Dashboard
tipo("Dashboard", S_DASH,
     "Um dashboard: título, pasta, colunas ou grade de componentes, filtros, cores e o usuário cujo acesso define os dados mostrados.",
     "Versionar e implantar os dashboards da org entre ambientes.", "14.0", [
         P("backgroundEndColor", S, None, "Segunda cor do gradiente de fundo dos gráficos, em hexadecimal.", "S"),
         P("backgroundFadeDirection", "ChartBackgroundDirection", None, "Direção do gradiente de fundo.", "S",
           vals=valores("Diagonal", "LeftToRight", "TopToBottom")),
         P("backgroundStartColor", S, None, "Primeira cor do gradiente de fundo dos gráficos, em hexadecimal.", "S"),
         P("chartTheme", "ChartTheme", "42.0", "Tema padrão dos gráficos. Substitui dashboardChartTheme.", vals=valores("light", "dark")),
         P("colorPalette", "ChartColorPalettes", "42.0", "Paleta padrão dos gráficos. Substitui dashboardColorPalette.", vals=valores(
             "accessible", "bluegrass", "branding", "colorSafe", "Default", "dusk", "earth", "fire", "gray", "heat", "justice", "nightfall", "pond",
             "sunrise", "tropic", "unity", "water", "watermelon")),
         P("dashboardChartTheme", "ChartTheme", None, "Tema padrão legado, mantido para compatibilidade com versões anteriores à 42.0.",
           vals=valores("light", "dark")),
         P("dashboardColorPalette", "ChartColorPalettes", None, "Paleta padrão legada, mantida para compatibilidade com versões anteriores à 42.0.",
           natureza="desconhecida", contexto="A linha lista os mesmos valores de colorPalette, menos branding."),
         P("dashboardFilters", "DashboardFilter[]", "23.0", "Filtros do dashboard."),
         P("dashboardGridLayout", "DashboardGridLayout", "35.0", "Componentes em grade, número de colunas e altura das linhas."),
         P("dashboardType", "DashboardType", "19.0", "De quem é o acesso que define os dados mostrados.", vals=[
             ("SpecifiedUser", None), ("LoggedInUser", None), ("MyTeamUser", "Desde a API 20.0.")]),
         P("description", S, None, "Descrição do dashboard; até 255 caracteres."),
         P("folderName", S, "35.0", "Pasta que contém o dashboard."),
         P("fullName", S, None, "Caminho com pasta e título, como folderSales/California. Herdado do tipo Metadata.",
           "C:obrigatório ao criar, atualizar ou excluir", herdada="Metadata"),
         P("isGridLayout", B, "35.0", "Com true, o dashboard usa o layout do Lightning Experience."),
         P("dashboardResultRefreshedDate", S, None, "Data da última atualização do dashboard.", "S"),
         P("dashboardResultRunningUser", S, None, "Usuário que está vendo o dashboard.", "S"),
         P("leftSection", "DashboardComponentSection", None, "Coluna esquerda do dashboard.", "S"),
         P("middleSection", "DashboardComponentSection", None, "Coluna do meio do dashboard."),
         P("numSubscriptions", I, "42.0", "Número de assinaturas do dashboard."),
         P("owner", S, None, "Quem criou o dashboard."),
         P("rightSection", "DashboardComponentSection", None, "Coluna direita do dashboard.", "S"),
         P("runningUser", S, None, "Usuário cujo papel e compartilhamento definem os dados mostrados."),
         P("textColor", S, None, "Cor do texto dos gráficos, em hexadecimal.", "S"),
         P("title", S, None, "Título do dashboard.", "S"),
         P("titleColor", S, None, "Cor do título dos componentes, em hexadecimal.", "S"),
         P("titleSize", I, None, "Tamanho do texto do título; 12 significa 12 pt.", "S"),
     ], exemplo=CAB + f"""<Dashboard {NS}>
    <backgroundEndColor>#FFFFFF</backgroundEndColor>
    <!-- Valores documentados: Diagonal, LeftToRight, TopToBottom -->
    <backgroundFadeDirection>Diagonal</backgroundFadeDirection>
    <backgroundStartColor>#FFFFFF</backgroundStartColor>
    <!-- Valores documentados: SpecifiedUser, LoggedInUser, MyTeamUser -->
    <dashboardType>SpecifiedUser</dashboardType>
    <description>[o que o dashboard mostra]</description>
    <runningUser>[nome de usuário]</runningUser>
    <textColor>#000000</textColor>
    <title>[título do dashboard]</title>
    <titleColor>#000000</titleColor>
    <titleSize>12</titleSize>
</Dashboard>""", curinga=False,
     arquivos_prontos=em_pasta("dashboards/<pasta>/", "<Nome>.dashboard",
                               "Os dashboards ficam em subpastas da pasta dashboards. No source format, o arquivo recebe o sufixo -meta.xml.",
                               "dashboard", S_DASH),
     alertas=["O curinga (*) não funciona: obtenha as pastas com listMetadata() do tipo DashboardFolder e use developer names, não títulos.",
              "Se runningUser faltar ou for inválido no deploy, entra o usuário que está implantando.",
              "Guarde dashboards em pastas visíveis só a quem deve ver os dados.",
              RESTAURA],
     divergencias=["A tabela marca leftSection e rightSection como obrigatórios e também traz dashboardGridLayout, do layout do Lightning "
                   "Experience; o trecho lido não explica como os dois se combinam."],
     cobertura_nota=NOTA_COB + " Primeiro nível: 26 de 26 campos. " + SEM_DET.format(
         "173.302", "(DashboardFilter, DashboardGridLayout, DashboardComponent, DashboardComponentSection e os demais)"))

# ================================================================ ReportType
estrutura("ObjectRelationship", S_RT, ["mdt:ReportType"], [
    P("join", "ObjectRelationship", None, "Junção seguinte, para encadear mais objetos. Até quatro objetos; depois de um outer join não cabe um inner join.",
      estrutura="ObjectRelationship", notas=["A estrutura é recursiva: aponta para outra ObjectRelationship."]),
    P("outerJoin", B, None, "Com true, mantém as linhas que não têm registro relacionado; com false, não.", "S"),
    P("relationship", S, None, "Objeto unido ao objeto principal, como Contacts.", "S"),
], "A junção de um objeto relacionado ao objeto principal de um tipo de relatório.")
estrutura("ReportTypeColumn", S_RT, ["mdx:ReportLayoutSection"], [
    P("checkedByDefault", B, None, "Indica se a coluna vem selecionada por padrão.", "S"),
    P("displayNameOverride", S, None, "Nome customizado da coluna."),
    P("field", S, None, "Nome de API do campo da coluna.", "S"),
    P("table", S, None, "Objeto a que o campo pertence, como Account.", "S"),
], "Uma coluna (campo) disponível num tipo de relatório.")
estrutura("ReportLayoutSection", S_RT, ["mdt:ReportType"], [
    P("columns", "ReportTypeColumn[]", None, "Colunas da seção.", estrutura="ReportTypeColumn"),
    P("masterLabel", S, None, "Rótulo do grupo de colunas no assistente de relatórios.", "S"),
], "Um grupo de colunas de um tipo de relatório.")
tipo("ReportType", S_RT,
     "Um custom report type: o objeto principal, os objetos relacionados e os campos que um relatório desse tipo pode usar.",
     "Versionar e implantar os tipos de relatório customizados.", "14.0", [
         P("autogenerated", B, "29.0", "Indica que o tipo foi criado automaticamente ao ligar historical trending numa entidade."),
         P("baseObject", S, None, "Objeto principal, como Account. Não pode ser trocado depois da criação. External objects desde a API 38.0.", "S"),
         P("category", "ReportTypeCategory", None, "Categoria em que o tipo aparece.", vals=[
             (v, None) for v in ("accounts", "opportunities", "forecasts", "cases", "leads", "campaigns", "activities", "busop", "products", "admin",
                                 "territory")] + [("territory2", "Desde a API 31.0."), ("usage_entitlement", None), ("wdc", "Desde a API 29.0."),
                                                  ("calibration", "Desde a API 29.0."), ("other", None), ("content", None), ("quotes", None),
                                                  ("individual", "Desde a API 45.0."), ("employee", "Desde a API 46.0."),
                                                  ("data_cloud", "Desde a API 55.0."), ("commerce", "Desde a API 60.0."),
                                                  ("flow", "Desde a API 60.0."), ("semantic_model", "Desde a API 60.0.")]),
         P("deployed", B, None, "Com true, o tipo fica disponível aos usuários; com false, está em desenvolvimento.", "S"),
         P("description", S, None, "Descrição do tipo de relatório."),
         P("fullName", S, None, "Nome único de API: letras, números e sublinhados, começando por letra. Herdado.", "?", herdada="Metadata"),
         P("join", "ObjectRelationship", None, "Objeto unido ao objeto principal, como Contacts unidos a Accounts.", estrutura="ObjectRelationship"),
         P("label", S, None, "Rótulo do tipo de relatório.", "S"),
         P("sections", "ReportLayoutSection[]", None, "Grupos de colunas do tipo.", estrutura="ReportLayoutSection"),
     ], exemplo=CAB + f"""<ReportType {NS}>
    <baseObject>Account</baseObject>
    <!-- Valores documentados incluem: accounts, opportunities, cases, leads, other -->
    <category>accounts</category>
    <deployed>true</deployed>
    <description>[para que serve o tipo de relatório]</description>
    <join>
        <outerJoin>true</outerJoin>
        <relationship>Contacts</relationship>
    </join>
    <label>[rótulo do tipo]</label>
    <sections>
        <columns>
            <checkedByDefault>true</checkedByDefault>
            <field>Name</field>
            <table>Account</table>
        </columns>
        <masterLabel>[rótulo do grupo de colunas]</masterLabel>
    </sections>
</ReportType>""", curinga=True,
     alertas=["O objeto principal (baseObject) não pode ser trocado depois da criação.",
              "A junção encadeia até quatro objetos; depois de um outer join não é permitido um inner join.",
              "Campos históricos (de objetos com historical trending) usam nomes de API com hst, como Field2__c_hst.",
              RESTAURA],
     cobertura_nota=NOTA_COB)

# ================================================================ ReportFolder e DashboardFolder (página Folder)
ACESSO = [("Shared", "Visível só a um conjunto de usuários."), ("Public", "Visível a todos, inclusive usuários de portal."),
          ("PublicInternal", "Visível a todos, menos usuários de portal; só em pastas de relatórios e dashboards."),
          ("Hidden", "Oculta de todos.")]


def pasta_tipo(nome, conteudo, dir_, chave):
    tipo(nome, S_FOLDER,
         f"Uma pasta de {conteudo}: o nome e o modo de acesso. O conteúdo fica nos componentes que a pasta contém.",
         f"Versionar e implantar as pastas de {conteudo} e o acesso a elas.", "11.0", [
             P("accessType", "FolderAccessTypes", None, "Tipo de acesso da pasta.", "S", vals=ACESSO),
             P("fullName", S, None, "Nome único de API: letras, números e sublinhados, começando por letra. Herdado.", "?", herdada="Metadata"),
             P("name", S, None, "Nome da pasta.", "S"),
             P("publicFolderAccess", "PublicFolderAccess", None, "Acesso ao conteúdo quando accessType é Public.", vals=[
                 ("ReadOnly", "Todos leem; ninguém altera."), ("ReadWrite", "Todos leem e alteram.")]),
             P("sharedTo", "SharedTo", None, "Com quem a pasta é compartilhada."),
         ], exemplo=CAB + f"""<{nome} {NS}>
    <!-- Valores documentados: Shared, Public, PublicInternal, Hidden -->
    <accessType>Public</accessType>
    <name>[nome da pasta]</name>
    <!-- Valores documentados: ReadOnly, ReadWrite -->
    <publicFolderAccess>ReadOnly</publicFolderAccess>
</{nome}>""", estende="Folder", curinga=False,
         arquivos_prontos=em_pasta(dir_ + "/", f"<Pasta>.{chave[0].lower() + nome[1:]}-meta.xml",
                                   "A pasta não tem arquivo de conteúdo: só o arquivo de metadado, no mesmo diretório dos componentes. O sufixo "
                                   "vem do registro do Salesforce CLI.", chave, S_FOLDER),
         alertas=["A página Folder é comum aos cinco tipos de pasta (documentos, e-mail, email templates, relatórios e dashboards); o exemplo XML "
                  "dela é de DocumentFolder.",
                  "O curinga (*) não funciona no package.xml.",
                  "Para implantar ou recuperar só uma pasta aninhada, o nome completo precisa terminar com barra."]
                 + (["No package.xml, as pastas de relatórios entram sob o tipo Report."] if nome == "ReportFolder" else []),
         cobertura_nota=NOTA_COB + " O subtipo SharedTo tem página própria, não lida.")


pasta_tipo("ReportFolder", "relatórios", "reports", "reportfolder")
pasta_tipo("DashboardFolder", "dashboards", "dashboards", "dashboardfolder")

# ================================================================ DuplicateRule
estrutura("ObjectMappingField", S_DR, ["mdx:ObjectMapping"], [
    P("inputField", S, None, "Campo do objeto de entrada mapeado ao campo de saída.", "S"),
    P("outputField", S, None, "Campo do objeto de saída que recebe o mapeamento.", "S"),
], "O par de campos de um mapeamento entre dois objetos.")
estrutura("ObjectMapping", S_DR, ["mdx:DuplicateRuleMatchRule"], [
    P("inputObject", S, None, "O objeto da duplicate rule, usado como entrada.", "S"),
    P("mappingFields", "ObjectMappingField[]", None, "Mapeamentos de campos do objeto de origem para o de destino.", "S", estrutura="ObjectMappingField"),
    P("outputObject", S, None, "Objeto de destino; o mesmo de matchRuleSObjectType. As duplicate rules dele são ignoradas.", "S"),
], "O mapeamento de campos entre o objeto da regra e o objeto em que a matching rule procura.")
estrutura("DuplicateRuleMatchRule", S_DR, ["mdt:DuplicateRule"], [
    P("matchRuleSObjectType", S, None, "Objeto em que a matching rule procura, como Lead numa regra de Contact.", "S"),
    P("matchingRule", S, None, "Developer name da matching rule associada.", "S"),
    P("objectMapping", "ObjectMapping", None, "Mapeamento de campos entre o objeto de entrada e o de saída.", "S", estrutura="ObjectMapping"),
], "Uma matching rule usada por uma duplicate rule.")
estrutura("DuplicateRuleFilterItem", S_DR, ["mdx:DuplicateRuleFilter"], [
    P("sortOrder", I, None, "Posição do item no filtro.", "S"),
    P("table", S, None, "Objeto que contém o campo indicado em field.", "S"),
], "Um item do filtro de uma duplicate rule. Estende FilterItem: além destes campos, o exemplo XML usa field, operation e value, herdados.")
estrutura("DuplicateRuleFilter", S_DR, ["mdt:DuplicateRule"], [
    P("booleanFilter", S, None, "Lógica que combina os itens do filtro.", "S"),
    P("duplicateRuleFilterItems", "DuplicateRuleFilterItem[]", None, "Itens do filtro.", "S", estrutura="DuplicateRuleFilterItem"),
], "O critério que limita quais registros entram na busca por duplicados.")
tipo("DuplicateRule", S_DR,
     "Uma duplicate rule: o que acontece quando um registro criado ou editado é identificado como duplicado, e com que matching rules se compara.",
     "Versionar e implantar as regras de duplicidade de cada objeto.", None, [
         P("actionOnInsert", "DupeActionType", None, "O que fazer ao criar um duplicado.", "S", vals=[
             ("Allow", "Deixa o usuário prosseguir depois do alerta."), ("Block", "Impede a criação.")]),
         P("actionOnUpdate", "DupeActionType", None, "O que fazer quando uma edição gera um duplicado.", "S", vals=valores("Allow", "Block")),
         P("alertText", S, None, "Mensagem mostrada ou devolvida quando a regra dispara. Só é enviada com a regra ativa e exige Allow na criação ou na edição."),
         P("description", S, None, "Descrição da regra; não aparece na interface.", "S"),
         P("duplicateRuleFilter", "DuplicateRuleFilter", None, "Critério que limita os registros considerados.", "S", estrutura="DuplicateRuleFilter"),
         P("duplicateRuleMatchRules", "DuplicateRuleMatchRule[]", None, "Uma ou mais matching rules que definem o que é um duplicado.", "S",
           estrutura="DuplicateRuleMatchRule"),
         P("isActive", B, None, "Com true, a regra detecta duplicados; com false, não tem efeito.", "S"),
         P("masterLabel", S, None, "Rótulo interno da regra.", "S"),
         P("operationsOnInsert", "string[]", None, "Usado quando actionOnInsert é Allow.", "S", vals=valores("alert", "report"),
           contexto="A página lista estes valores para um campo do tipo string."),
         P("operationsOnUpdate", "string[]", None, "Usado quando actionOnUpdate é Allow.", "S", vals=valores("alert", "report"),
           contexto="A página lista estes valores para um campo do tipo string."),
         P("securityOption", "DupeSecurityOptionType", None, "Define se as sharing rules valem na busca por duplicados.", "S",
           vals=valores("EnforceSharingRules", "BypassSharingRules")),
         P("sortOrder", I, None, "Ordem em que as duplicate rules são aplicadas.", "S"),
         M.FULLNAME_HERDADO(None),
     ], exemplo=CAB + f"""<DuplicateRule {NS}>
    <!-- Valores documentados: Allow, Block -->
    <actionOnInsert>Allow</actionOnInsert>
    <actionOnUpdate>Allow</actionOnUpdate>
    <alertText>[mensagem mostrada ao usuário]</alertText>
    <description>[descrição da regra]</description>
    <duplicateRuleMatchRules>
        <matchRuleSObjectType>Account</matchRuleSObjectType>
        <matchingRule>[developer name da matching rule]</matchingRule>
    </duplicateRuleMatchRules>
    <isActive>true</isActive>
    <masterLabel>[rótulo da regra]</masterLabel>
    <!-- Valores documentados: alert, report -->
    <operationsOnInsert>alert</operationsOnInsert>
    <operationsOnUpdate>alert</operationsOnUpdate>
    <!-- Valores documentados: EnforceSharingRules, BypassSharingRules -->
    <securityOption>EnforceSharingRules</securityOption>
    <sortOrder>1</sortOrder>
</DuplicateRule>""", curinga=True, completa=False,
     arquivos_prontos=em_pasta("duplicateRules/", "<Objeto>.<Nome_Da_Regra>.duplicateRule",
                               "O nome do arquivo começa pelo objeto da regra. No source format, o arquivo recebe o sufixo -meta.xml.",
                               "duplicaterule", S_DR),
     alertas=["alertText só pode ser definido quando a ação na criação ou na edição é Allow; fora disso, a validação falha.",
              "Com Allow e alerta, salvar pela API exige allowSave igual a true no cabeçalho DuplicateRuleHeader."],
     divergencias=["A leitura da página devolveu disponibilidade a partir da API 68.0, mas o package.xml de exemplo da própria página usa a versão 38.0. "
                   "A versão inicial ficou registrada como desconhecida."],
     cobertura_nota=NOTA_COB + " Os campos herdados de FilterItem por DuplicateRuleFilterItem não estão listados na página.")
_d = ld("metadata-types/DuplicateRule.json")
_d["disponibilidade"] = {"desde_versao": None, "ate_versao": None, "estado": "desconhecido",
                         "nota": "A leitura da página devolveu 68.0; o package.xml de exemplo da mesma página usa 38.0. Não confirmado."}
sv("metadata-types/DuplicateRule.json", _d)

# ================================================================ MatchingRules
estrutura("MatchingRuleItem", S_MR, ["mdx:MatchingRule"], [
    P("blankValueBehavior", "BlankValueBehavior", None, "Define se campos em branco podem ser considerados iguais.",
      default=("valor", "NullNotAllowed", "A página indica NullNotAllowed como padrão."), vals=valores("MatchBlanks", "NullNotAllowed")),
    P("fieldName", S, None, "Campo comparado para decidir se os registros correspondem.", "S"),
    P("matchingMethod", "MatchingMethod", None, "Como o campo é comparado.", "S", vals=[
        ("Exact", "Comparação exata.")] + [(v, "Comparação aproximada (fuzzy).") for v in (
            "FirstName", "LastName", "CompanyName", "Phone", "City", "Street", "Zip", "Title")]),
], "Um critério de uma matching rule: o campo e o método de comparação.")
estrutura("MatchingRule", S_MR, ["mdt:MatchingRules"], [
    P("booleanFilter", S, None, "Lógica que combina os critérios."),
    P("description", S, None, "Para que serve a regra."),
    P("fullName", S, None, "Nome de API da matching rule; aparece no exemplo XML da página."),
    P("label", S, None, "Nome da matching rule.", "S"),
    P("matchingRuleItems", "MatchingRuleItem[]", None, "Os critérios da regra.", estrutura="MatchingRuleItem",
      notas=["A tabela tipa o campo como MatchingRuleItem; o elemento se repete, um por critério."]),
    P("ruleStatus", "MatchingRuleStatus", None, "Estado de ativação da regra.", "S", vals=valores(
        "Inactive", "Deactivating", "DeactivationFailed", "Active", "Activating", "ActivationFailed"),
      notas=["Num pacote implantado, só Active e Inactive podem ser declarados."]),
], "Uma matching rule: como identificar registros duplicados de um objeto.")
tipo("MatchingRules", S_MR,
     "O conjunto de matching rules de um objeto, padrão ou customizado: as regras que dizem como reconhecer registros duplicados.",
     "Versionar e implantar as matching rules de cada objeto.", "33.0", [
         P("matchingRules", "MatchingRule[]", None, "Cada matching rule do objeto.", estrutura="MatchingRule",
           notas=["O elemento vem do exemplo XML da página; as tabelas documentam os campos de MatchingRule."]),
         M.FULLNAME_HERDADO(None, "Nome do objeto a que as regras pertencem; herdado do tipo Metadata."),
     ], exemplo=CAB + f"""<MatchingRules {NS}>
    <matchingRules>
        <fullName>[Nome_Da_Matching_Rule]</fullName>
        <label>[nome da matching rule]</label>
        <matchingRuleItems>
            <!-- Valores documentados: MatchBlanks, NullNotAllowed -->
            <blankValueBehavior>NullNotAllowed</blankValueBehavior>
            <fieldName>Name</fieldName>
            <!-- Valores documentados incluem: Exact, CompanyName -->
            <matchingMethod>Exact</matchingMethod>
        </matchingRuleItems>
        <!-- Na implantação, só Active e Inactive -->
        <ruleStatus>Inactive</ruleStatus>
    </matchingRules>
</MatchingRules>""", curinga=True,
     arquivos_prontos=em_pasta("matchingRules/", "<Objeto>.matchingRule",
                               "Um arquivo por objeto, com todas as matching rules dele. No source format, o arquivo recebe o sufixo -meta.xml.",
                               "matchingrules", S_MR),
     alertas=["Um arquivo reúne todas as matching rules do objeto; o nome do arquivo é o nome do objeto.",
              "Ao implantar, ruleStatus só aceita Active e Inactive.",
              "Person accounts são suportadas desde a API 39.0."],
     cobertura_nota=NOTA_COB)

M.emit_structs()
C.marcar_referencia("estruturas", "DuplicateRuleMatchRule", "matchingRule", "mdt:MatchingRules")

# ================================================================ nota de extração: lista de campos
linhas = ["", "-- Lista de campos transcrita da leitura (gerada por lote7g_relatorios_qualidade.py; nome | tipo | desde)"]
for src, pasta, nome in REGISTRADOS:
    props = ld(f"{pasta}/{nome}.json")["propriedades"]
    linhas.append(f"[{src}] {nome}: " + ", ".join(f"{q['nome']} | {q['tipo_tecnico']} | {q.get('desde_versao') or '-'}" for q in props))
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(linhas) + "\n")

# ================================================================ relacionamentos
C.rel_referencia("duplicaterule-matchingrule", "mdx:DuplicateRuleMatchRule", "matchingRule", "mdt:MatchingRules",
                 "Uma duplicate rule cita, pelo developer name, as matching rules que usa.", S_DR)

# ================================================================ funcionalidades
REL, QUA = "relatorios-analytics-e-exploracao", "qualidade-governanca-e-ciclo-de-vida-dos-dados"
SEM_OBJ = {"tipo": "objeto_api", "estado": "desconhecido",
           "motivo": "Objetos API do tema não investigados nas rodadas B2 e B3; a lista vazia não comprova inexistência."}
SEM_SETUP = af("desconhecido", None, "Caminho de Setup não confirmado nas fontes lidas.", [])

C.funcionalidade(
    "relatorios", "Relatórios", "Reports", ["report", "relatório", "report builder", "joined report", "summary", "matrix", "tabular"],
    "Um relatório responde perguntas sobre os registros da org. É montado no report builder: escolhem-se o tipo de relatório, o formato e "
    "os campos, e depois agrupa-se, filtra-se e resume-se.",
    "Responder perguntas sobre os dados da org sem escrever consultas.",
    "Um relatório de oportunidades agrupado por fase mostra o valor total em cada fase e um gráfico.",
    (REL, "reports"), [(REL, "metricas-e-agregacoes", "Totais, fórmulas e buckets são definidos dentro do relatório.")],
    [("Report", "Cada relatório customizado.")], [],
    [S_REP, "src:help-reports-overview", "src:help-reports-build", "src:help-joined-reports-concepts", "src:help-report-formulas",
     "src:help-add-bucket-column", "src:help-reports-mobile-differences"], [SEM_OBJ],
    af("nao_aplicavel", None, "O report builder abre pela aba Reports ou pela aba Analytics, não pelo Setup.", [ev("src:help-reports-overview")]),
    limitacoes=["Um joined report tem até cinco blocos.",
                "Até 5 bucket fields por relatório, com 20 buckets por campo e 20 valores por bucket.",
                "No app móvel não há joined reports nem criação, edição ou exclusão de relatórios."],
    alertas=["Como metadado, só relatórios customizados são suportados, e o curinga do package.xml não funciona.",
             "Num joined report, os tipos de relatório dos blocos precisam ter relação com o mesmo objeto."])

C.funcionalidade(
    "dashboards", "Dashboards", "Dashboards", ["dashboard", "painel", "widget", "running user", "dynamic dashboard", "source report"],
    "Um dashboard mostra, em gráficos e tabelas, os resultados de relatórios de origem (source reports). Cada componente tem o próprio "
    "relatório. Em View Dashboard As define-se de quem é o acesso que decide os dados mostrados: de quem criou, de outra pessoa ou de "
    "quem está vendo (dynamic dashboard).",
    "Acompanhar indicadores de relance, a partir de relatórios que já existem.",
    "O dashboard de vendas tem um gráfico de pipeline por fase e uma tabela das maiores oportunidades, cada um ligado a um relatório.",
    (REL, "dashboards"), [],
    [("Dashboard", "Cada dashboard, com componentes, filtros e running user.")], [],
    [S_DASH, "src:help-dashboards-build-lex", "src:help-dashboards-view-as", "src:help-dynamic-dashboards", "src:help-dynamic-dashboards-create",
     "src:help-dashboard-performance"], [SEM_OBJ],
    af("nao_aplicavel", None, "Dashboards são criados e vistos na aba Dashboards, não no Setup.", [ev("src:help-dashboards-build-lex")]),
    limitacoes=["Dynamic dashboards por edição: 5 em Enterprise, 10 em Unlimited e Performance, 3 em Developer.",
                "Um dynamic dashboard não aceita atualização agendada.",
                "Uma Lightning table mostra até 200 registros e 10 colunas.",
                "Cada usuário pode atualizar um dashboard uma vez por minuto."],
    alertas=["Com running user fixo, todos veem os dados conforme o acesso daquela pessoa, não o próprio.",
             "Dashboards na Lixeira contam no limite de dynamic dashboards até a exclusão definitiva.",
             "Criar, editar e excluir dynamic dashboards exige a permissão Manage Dynamic Dashboards."])

C.funcionalidade(
    "custom-report-types", "Custom report types", "Custom Report Types", ["report type", "tipo de relatório", "crt", "custom report type"],
    "Um tipo de relatório define quais registros e campos um relatório pode usar, a partir das relações entre um objeto principal e os "
    "objetos relacionados. Tipos customizados incluem objetos e campos além dos tipos padrão.",
    "Dar aos usuários relatórios com a combinação de objetos e campos de que o negócio precisa.",
    "O tipo Contas com ou sem Projetos une Account ao objeto customizado de projetos e expõe campos dos dois.",
    (REL, "tipos-de-relatorio"), [],
    [("ReportType", "Cada custom report type.")], [],
    [S_RT, "src:help-custom-report-types", "src:help-crt-legacy-builder"], [SEM_OBJ], SEM_SETUP,
    limitacoes=["A junção de objetos de um tipo encadeia até quatro objetos."],
    alertas=["O objeto principal não pode ser trocado depois de o tipo ser salvo.",
             "Enquanto deployed é false, o tipo está em desenvolvimento e não aparece para os usuários."])

C.funcionalidade(
    "pastas-de-relatorios-e-dashboards", "Pastas de relatórios e dashboards", "Report and Dashboard Folders",
    ["folder", "pasta", "enhanced folder sharing", "viewer", "editor", "manager", "public reports", "private reports"],
    "Relatórios e dashboards ficam em pastas, e o acesso é dado na pasta: cada usuário, grupo ou papel recebe um nível (Viewer, Editor ou "
    "Manager).",
    "Controlar quem vê e quem altera relatórios e dashboards.",
    "A pasta Diretoria é compartilhada só com o papel de diretores, como Viewer; os analistas que a mantêm são Editors.",
    (REL, "pastas-e-acesso"), [],
    [("ReportFolder", "Cada pasta de relatórios."), ("DashboardFolder", "Cada pasta de dashboards.")], [],
    [S_FOLDER, "src:help-folder-access-levels", "src:help-enhanced-folder-sharing", "src:help-share-folder-lightning", "src:help-folder-sharing-mdapi"],
    [SEM_OBJ], af("nao_aplicavel", None, "As pastas são criadas e compartilhadas nas abas Reports e Dashboards.", [ev("src:help-folder-access-levels")]),
    limitacoes=["Compartilhamento de uma pasta: até 25 entradas pela interface e até 500 pela folder sharing REST API."],
    alertas=["O nível na pasta não decide sozinho: as permissões do usuário sobre relatórios e dashboards também contam.",
             "Uma pasta nova só é acessível a quem a criou e a administradores, até ser compartilhada.",
             "Se o usuário aparece em mais de uma entrada de compartilhamento, vale o maior nível.",
             "Um artigo da Ajuda descreve o compartilhamento de pastas por Metadata API com accessLevel em FolderShare; esse subtipo não foi "
             "lido no guia."])

C.funcionalidade(
    "duplicate-management", "Duplicate Management", "Duplicate Management",
    ["duplicate rule", "matching rule", "regra de duplicidade", "duplicados", "duplicate job", "duplicate record set", "match key"],
    "Duplicate Management reconhece registros repetidos e decide o que fazer com eles. São duas peças: a matching rule define como os "
    "duplicados são identificados; a duplicate rule define o que acontece quando alguém cria ou edita um registro duplicado: alertar e "
    "permitir, ou bloquear.",
    "Manter a base sem registros repetidos de contas, contatos, leads e outros objetos.",
    "Ao criar um lead com o mesmo e-mail de um contato, o usuário vê um alerta com o possível duplicado e decide se salva mesmo assim.",
    (QUA, "duplicidade-e-correspondencia"), [],
    [("DuplicateRule", "Cada duplicate rule."), ("MatchingRules", "As matching rules de cada objeto.")], [],
    [S_DR, S_MR, "src:help-duplicate-management-customize", "src:help-duplicate-detection-process", "src:help-duplicate-rules-things-to-know",
     "src:help-duplicate-rules-customize", "src:help-matching-rules", "src:help-matching-rules-considerations", "src:help-duplicate-web-to-lead"],
    [SEM_OBJ], SEM_SETUP,
    limitacoes=["Até cinco duplicate rules ativas por objeto, e até três matching rules em cada duplicate rule.",
                "Matching rules: até cinco ativas por objeto, 25 ativas no total e 100 no total, entre ativas e inativas."],
    alertas=["Uma duplicate rule só pode ser ativada se todas as matching rules associadas estiverem ativas.",
             "As matching rules padrão não podem ser editadas; é possível criar regras customizadas.",
             "Em Web-to-Lead, um envio que bate com o critério de duplicidade é sempre bloqueado, mesmo com a regra em Allow com alerta.",
             "Criar, editar e ativar regras exige a permissão Customize Application."])

print(f"lote 7g: 7 metadata types e {sum(1 for r in REGISTRADOS if r[1] == 'estruturas')} estruturas gravados; 5 funcionalidades novas")
