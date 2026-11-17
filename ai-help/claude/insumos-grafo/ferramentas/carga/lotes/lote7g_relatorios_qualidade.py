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
LIDA_EM_PARTES = "A página tem {} caracteres e foi lida inteira, em partes ({}), em 2026-11-16; os {} subtipos documentados foram cadastrados."

# ---------------------------------------------------------------- subtipos de Report (página inteira lida em três partes, 2026-11-16)
RESUMO = [("Sum", None), ("Average", None), ("Maximum", None), ("Minimum", None), ("Unique", None), ("Median", None), ("Noop", None), ("None", None)]
ORDEM = valores("Asc", "Desc")
INTERVALOS = (
    "INTERVAL_CURRENT INTERVAL_CURNEXT1 INTERVAL_CURPREV1 INTERVAL_NEXT1 INTERVAL_PREV1 INTERVAL_CURNEXT3 INTERVAL_CURFY INTERVAL_PREVFY "
    "INTERVAL_PREV2FY INTERVAL_AGO2FY INTERVAL_NEXTFY INTERVAL_PREVCURFY INTERVAL_PREVCUR2FY INTERVAL_CURNEXTFY INTERVAL_CUSTOM INTERVAL_YESTERDAY "
    "INTERVAL_TODAY INTERVAL_TOMORROW INTERVAL_LASTWEEK INTERVAL_THISWEEK INTERVAL_NEXTWEEK INTERVAL_LASTMONTH INTERVAL_THISMONTH INTERVAL_NEXTMONTH "
    "INTERVAL_LASTTHISMONTH INTERVAL_THISNEXTMONTH INTERVAL_CURRENTQ INTERVAL_CURNEXTQ INTERVAL_CURPREVQ INTERVAL_NEXTQ INTERVAL_PREVQ INTERVAL_CURNEXT3Q "
    "INTERVAL_CURY INTERVAL_PREVY INTERVAL_PREV2Y INTERVAL_AGO2Y INTERVAL_NEXTY INTERVAL_PREVCURY INTERVAL_PREVCUR2Y INTERVAL_CURNEXTY INTERVAL_LAST7 "
    "INTERVAL_LAST30 INTERVAL_LAST60 INTERVAL_LAST90 INTERVAL_LAST120 INTERVAL_NEXT7 INTERVAL_NEXT30 INTERVAL_NEXT60 INTERVAL_NEXT90 INTERVAL_NEXT120 "
    "LAST_FISCALWEEK THIS_FISCALWEEK NEXT_FISCALWEEK LAST_FISCALPERIOD THIS_FISCALPERIOD NEXT_FISCALPERIOD LASTTHIS_FISCALPERIOD THISNEXT_FISCALPERIOD "
    "CURRENT_ENTITLEMENT_PERIOD PREVIOUS_ENTITLEMENT_PERIOD PREVIOUS_TWO_ENTITLEMENT_PERIODS TWO_ENTITLEMENT_PERIODS_AGO "
    "CURRENT_AND_PREVIOUS_ENTITLEMENT_PERIOD CURRENT_AND_PREVIOUS_TWO_ENTITLEMENT_PERIODS").split()
OPERADORES = [(v, None) for v in ("equals", "notEqual", "lessThan", "greaterThan", "lessOrEqual", "greaterOrEqual", "contains", "notContain",
                                  "startsWith", "includes", "excludes")]
SEM_VALORES = "A página cita a enumeração, mas não traz a lista de valores."
RP = ["mdt:Report"]

estrutura("ReportAggregateFilter", S_REP, RP, [
    P("aggregate", S, None, "Nome da summary formula a que o filtro se aplica.", "S"),
    P("operator", S, None, "Operador do filtro.", "S"),
    P("value", S, None, "Valor do filtro.", "S"),
], "Um filtro sobre uma summary formula customizada.")
estrutura("ReportAggregate", S_REP, RP, [
    P("acrossGroupingContext", S, None, "Agrupamento de linha em que o resultado aparece."),
    P("calculatedFormula", S, None, "A fórmula de resumo customizada.", "S"),
    P("datatype", "ReportAggregateDatatype", None, "Tipo de dado usado para formatar o resultado.", "S", vals=valores("currency", "number", "percent")),
    P("description", S, None, "Descrição da fórmula; até 255 caracteres."),
    P("developerName", S, None, "Nome interno, usado para referenciar a fórmula.", "S"),
    P("downGroupingContext", S, None, "Agrupamento de coluna em que o resultado aparece."),
    P("isActive", B, None, "Indica se o resultado aparece no relatório.", "S"),
    P("isCrossBlock", B, None, "Marca uma fórmula entre blocos, em joined reports."),
    P("masterLabel", S, None, "Rótulo da fórmula.", "S"),
    P("reportType", S, None, "Tipo de relatório dos blocos que a fórmula pode combinar.", "C:obrigatório em joined reports"),
    P("scale", I, None, "Casas decimais do resultado, de 0 a 18."),
], "Uma summary formula customizada: um cálculo sobre os valores resumidos de um relatório.")
estrutura("ReportAggregateReference", S_REP, ["mdx:ReportBlockInfo"], [
    P("aggregate", S, None, "developerName da summary formula usada no bloco.", "S"),
], "A referência a uma summary formula usada num bloco de joined report.")
estrutura("ReportBlockInfo", S_REP, RP, [
    P("aggregateReferences", "ReportAggregateReference[]", None, "Summary formulas usadas no bloco.", estrutura="ReportAggregateReference"),
    P("blockId", S, None, "Identificador do bloco, atribuído automaticamente, de B1 a B5.", "S"),
    P("joinTable", S, None, "Objeto que liga os blocos de um joined report.", "S"),
], "Os atributos de um bloco de joined report.")
estrutura("ReportBucketFieldSourceValue", S_REP, ["mdx:ReportBucketFieldValue"], [
    P("from", "não informado na página", None, "Início de uma faixa de valores (buckets numéricos).", natureza="desconhecida",
      contexto="A página lista sourceValue, from e to como valores de uma enumeração; o exemplo XML os usa como elementos com conteúdo."),
    P("sourceValue", "não informado na página", None, "Um valor de origem agrupado no bucket (buckets de picklist ou texto).", natureza="desconhecida",
      contexto="A página lista sourceValue, from e to como valores de uma enumeração; o exemplo XML os usa como elementos com conteúdo."),
    P("to", "não informado na página", None, "Fim de uma faixa de valores (buckets numéricos).", natureza="desconhecida",
      contexto="A página lista sourceValue, from e to como valores de uma enumeração; o exemplo XML os usa como elementos com conteúdo."),
], "A definição de um bucket: os valores de origem ou a faixa que ele agrupa.")
estrutura("ReportBucketFieldValue", S_REP, ["mdx:ReportBucketField"], [
    P("sourceValues", "ReportBucketFieldSourceValue", None, "O que entra neste bucket, conforme o tipo de bucket field.", estrutura="ReportBucketFieldSourceValue",
      notas=["A tabela tipa o campo como enumeração; o exemplo XML o usa como elemento com filhos."]),
    P("value", S, None, "Nome do bucket.", "S"),
], "Um bucket dentro de um bucket field.")
estrutura("ReportBucketField", S_REP, RP, [
    P("bucketType", "ReportBucketFieldType", None, "Tipo do bucket field, como texto ou número.", "S", natureza="desconhecida", contexto=SEM_VALORES),
    P("developerName", S, None, "Nome único, no formato BucketField_nome, usado para referenciar o campo.", "S"),
    P("masterLabel", S, None, "Rótulo do bucket field; até 40 caracteres.", "S"),
    P("nullTreatment", "ReportBucketFieldNullTreatment", None, "Em buckets numéricos, se valores vazios contam como zero.", natureza="desconhecida",
      contexto=SEM_VALORES),
    P("otherBucketLabel", S, None, "Rótulo do grupo que reúne os valores fora de qualquer bucket."),
    P("sourceColumnName", S, None, "Campo de origem do bucket.", "S"),
    P("values", "ReportBucketFieldValue", None, "Um bucket do bucket field; o elemento se repete.", estrutura="ReportBucketFieldValue",
      notas=["A tabela tipa o campo como enumeração; o exemplo XML o usa como elemento com filhos."]),
], "Um bucket field: um campo calculado que agrupa os valores de outro campo em faixas ou categorias.")
estrutura("ReportGrouping", S_REP, RP, [
    P("aggregateType", "ReportAggrType", None, "Tipo de agregação usado para ordenar o agrupamento.", vals=valores(
        "Sum", "Average", "Maximum", "Minimum", "RowCount", "Unique", "Median", "Noop")),
    P("dateGranularity", "UserDateGranularity", None, "Período usado para agrupar campos de data.", vals=valores(
        "None", "Day", "Week", "Month", "Quarter", "Year", "FiscalQuarter", "FiscalYear", "MonthInYear", "DayInMonth", "FiscalPeriod", "FiscalWeek")),
    P("field", S, None, "Campo usado para agrupar.", "S"),
    P("hierarchyApiName", S, None, "Nome de API da hierarquia usada no relatório."),
    P("sortByName", S, None, "Nome de API da coluna, da agregação ou da fórmula usada para ordenar."),
    P("sortOrder", "SortOrder", None, "Direção da ordenação.", "S", vals=ORDEM),
    P("sortType", "ReportSortType", None, "Se a ordenação usa uma coluna, uma agregação ou uma summary formula.", vals=valores(
        "Column", "Aggregate", "CustomSummaryFormula")),
], "Um agrupamento de linhas (groupingsDown) ou de colunas (groupingsAcross) de um relatório.")
estrutura("ReportHistoricalSelector", S_REP, RP, [
    P("snapshot", S, None, "Data do filtro histórico, relativa ou absoluta."),
], "O intervalo de datas dos dados de historical trending.")
estrutura("CustomDetailFormulas", S_REP, RP, [
    P("calculatedFormula", S, None, "A row-level formula.", "S"),
    P("datatype", "ReportCustomDetailFormulaDatatype", None, "Tipo de dado usado para formatar o resultado.", "S",
      vals=valores("Double", "DateOnly", "DateTime", "Text")),
    P("description", S, None, "Descrição da fórmula; até 255 caracteres."),
    P("developerName", S, None, "Nome interno, usado para referenciar a fórmula.", "S"),
    P("label", S, None, "Nome da fórmula.", "S"),
    P("scale", I, None, "Casas decimais do resultado, de 0 a 18."),
], "Uma row-level formula: um cálculo feito em cada linha do relatório.")
estrutura("ReportColorRange", S_REP, RP, [
    P("aggregate", "ReportSummaryType", None, "Como o campo referenciado é resumido.", "S", vals=RESUMO),
    P("columnName", S, None, "Campo cujas faixas de valor ganham cor de fundo.", "S"),
    P("highBreakpoint", "double", None, "Número que separa a cor do meio da cor alta.", "S"),
    P("highColor", S, None, "Cor HTML da faixa alta.", "S"),
    P("lowBreakpoint", "double", None, "Número que separa a cor baixa da cor do meio.", "S"),
    P("lowColor", S, None, "Cor dos valores abaixo do primeiro limite.", "S"),
    P("midColor", S, None, "Cor da faixa do meio.", "S"),
], "Uma regra de destaque condicional do Salesforce Classic: três cores para três faixas de valores.")
estrutura("ReportColumn", S_REP, RP, [
    P("aggregateTypes", "ReportSummaryType[]", None, "Como cada campo é resumido.", vals=RESUMO),
    P("field", S, None, "Campo mostrado na coluna.", "S"),
    P("isExtendedColumn", B, "65.0", "Indica se a coluna é estendida."),
    P("reverseColors", B, "29.0", "Inverte as cores padrão em relatórios de historical trending."),
    P("showChanges", B, "29.0", "Acrescenta uma coluna com a diferença entre valores históricos."),
], "Uma coluna (campo) mostrada no relatório.")
estrutura("ReportFilterItem", S_REP, ["mdx:ReportFilter", "mdx:ReportCrossFilter"], [
    P("column", S, None, "Campo filtrado.", "S"),
    P("columnToColumn", B, None, "Indica se o filtro compara dois campos."),
    P("isUnlocked", B, "38.0", "Indica se o usuário pode editar o filtro na página de execução."),
    P("operator", "FilterOperation", None, "Operador do filtro.", "S", vals=OPERADORES + [("within", "Só para critérios de distância.")]),
    P("snapshot", S, "29.0", "Data, relativa ou absoluta, em filtros de historical trending."),
    P("value", S, None, "Valor comparado; pode ser convertido para o formato dos EUA."),
], "Uma condição de filtro de um relatório ou de um cross filter.")
estrutura("ReportFilter", S_REP, RP, [
    P("booleanFilter", S, None, "Lógica que combina as condições."),
    P("criteriaItems", "ReportFilterItem", None, "Condições do filtro; o elemento se repete.", estrutura="ReportFilterItem"),
    P("language", "Language", None, "Idioma usado em filtros contains e startsWith sobre picklists.", natureza="desconhecida",
      contexto="A página não lista os valores."),
], "Os filtros de um relatório: as condições e a lógica que as combina.")
estrutura("ReportFormattingRuleValue", S_REP, ["mdx:ReportFormattingRule"], [
    P("backgroundColor", S, None, "Cor de destaque, em hexadecimal; até três cores por regra.", "S"),
    P("rangeUpperBound", "double", None, "Limite superior da faixa; omitido, vale infinito."),
], "Uma cor e o limite da faixa em que ela vale.")
estrutura("ReportFormattingRule", S_REP, RP, [
    P("aggregate", "ReportFormattingSummaryType", None, "Como a coluna é resumida para o destaque.", vals=valores("Sum", "Average", "Maximum", "Minimum", "Unique")),
    P("columnName", S, None, "Campo cujas faixas de valor ganham cor.", "S"),
    P("values", "ReportFormattingRuleValue", None, "As cores de fundo e suas faixas; o elemento se repete.", "S", estrutura="ReportFormattingRuleValue",
      notas=["A tabela tipa o campo como enumeração."]),
], "Uma regra de destaque condicional do Lightning Experience.")
estrutura("ReportParam", S_REP, RP, [
    P("name", S, None, "Nome de uma opção própria do tipo de relatório.", "S"),
    P("value", S, None, "Valor da opção.", "S"),
], "Uma opção de filtro própria do tipo de relatório.")
estrutura("ChartSummary", S_REP, ["mdx:ReportChart", "mdx:DashboardComponent"], [
    P("aggregate", "ReportSummaryType", None, "Método de agregação, como Sum ou Average.", vals=RESUMO),
    P("axisBinding", "ChartAxis", None, "Eixo usado pelo resumo.", vals=[("x", "Eixo X de gráficos de dispersão."), ("y", "Eixo Y."),
                                                                          ("y2", "Eixo Y secundário, em gráficos combinados.")]),
    P("column", S, None, "Campo de resumo usado nos dados do gráfico.", "S"),
], "Um resumo (valor agregado) mostrado num gráfico de relatório ou num componente de dashboard.")
estrutura("ReportChart", S_REP, RP, [
    P("backgroundColor1", S, None, "Cor inicial do gradiente de fundo."),
    P("backgroundColor2", S, None, "Cor final do gradiente de fundo."),
    P("backgroundFadeDir", "ChartBackgroundDirection", None, "Direção do gradiente.", vals=valores("Diagonal", "LeftToRight", "TopToBottom")),
    P("chartSummaries", "ChartSummary[]", None, "Resumos usados no gráfico; os inválidos são ignorados.", estrutura="ChartSummary"),
    P("chartType", "ChartType", None, "Tipo do gráfico; os disponíveis dependem do relatório.", "S", vals=valores(
        "None", "HorizontalBar", "HorizontalBarGrouped", "HorizontalBarStacked", "HorizontalBarStackedTo100", "VerticalColumn", "VerticalColumnGrouped",
        "VerticalColumnStacked", "VerticalColumnStackedTo100", "Line", "LineGrouped", "LineCumulative", "LineCumulativeGrouped", "Pie", "Donut", "Funnel",
        "Scatter", "ScatterGrouped", "VerticalColumnLine", "VerticalColumnGroupedLine", "VerticalColumnStackedLine", "Plugin")),
    P("enableHoverLabels", B, "17.0", "Mostra valores, rótulos e percentuais ao passar o mouse."),
    P("expandOthers", B, "17.0", "Junta grupos pequenos numa fatia Outros."),
    P("groupingColumn", S, None, "Campo usado para agrupar os dados no eixo."),
    P("legendPosition", "ChartLegendPosition", None, "Posição da legenda.", "S", vals=valores("Bottom", "OnChart", "Right")),
    P("location", "ChartPosition", None, "Se o gráfico aparece no topo ou no fim do relatório.", "S", vals=valores("CHART_TOP", "CHART_BOTTOM")),
    P("secondaryGroupingColumn", S, None, "Segundo campo de agrupamento, nos gráficos agrupados."),
    P("showAxisLabels", B, None, "Mostra o nome dos eixos em gráficos de barra e linha."),
    P("showPercentage", B, None, "Mostra percentuais em gráficos de pizza, rosca, funil e medidor."),
    P("showTotal", B, None, "Mostra o total em gráficos de rosca e medidores."),
    P("showValues", B, None, "Mostra os valores de cada registro ou grupo."),
    P("size", "ReportChartSize", None, "Tamanho do gráfico.", "S", vals=valores("Tiny", "Small", "Medium", "Large", "Huge")),
    P("summaryAggregate", "ReportSummaryType", None, "Forma antiga de resumo; sem suporte desde a API 17.0.", vals=RESUMO),
    P("summaryAxisManualRangeEnd", "double", None, "Valor final do eixo quando a faixa é manual."),
    P("summaryAxisManualRangeStart", "double", None, "Valor inicial do eixo quando a faixa é manual."),
    P("summaryAxisRange", "ChartRangeType", None, "Se a faixa do eixo é automática ou manual.", "S", vals=valores("Auto", "Manual")),
    P("summaryColumn", S, None, "Campo de resumo da forma antiga; sem suporte desde a API 17.0.", "S",
      notas=["A tabela marca o campo como obrigatório, embora ele esteja sem suporte desde a API 17.0."]),
    P("textColor", S, None, "Cor dos textos e rótulos do gráfico."),
    P("textSize", I, None, "Tamanho do texto: valores de 8 a 36, limitados a 18."),
    P("title", S, None, "Título do gráfico; até 255 caracteres."),
    P("titleColor", S, None, "Cor do título."),
    P("titleSize", I, None, "Tamanho do título: valores de 8 a 36, limitados a 18."),
], "O gráfico de um relatório.")
estrutura("ReportTimeFrameFilter", S_REP, RP, [
    P("dateColumn", S, None, "Campo de data filtrado.", "S"),
    P("endDate", "date", None, "Fim de um período customizado."),
    P("interval", "UserDateInterval", None, "O período.", "S", vals=valores(*INTERVALOS)),
    P("startDate", "date", None, "Início de um período customizado."),
], "O filtro de período de um relatório.")
estrutura("ReportCrossFilter", S_REP, RP, [
    P("criteriaItems", "ReportFilterItem", None, "Até cinco subfiltros do cross filter.", estrutura="ReportFilterItem"),
    P("operation", "ObjectFilterOperator", None, "Incluir (com) ou excluir (sem) o objeto relacionado.", vals=valores("with", "without")),
    P("primaryTableColumn", S, None, "Campo do objeto pai usado na junção."),
    P("relatedTable", S, None, "Objeto filho usado no cross filter."),
    P("relatedTableJoinColumn", S, None, "Campo do objeto filho que se liga ao pai."),
], "Um cross filter: registros com ou sem registros relacionados de outro objeto.")

# ================================================================ Report
tipo("Report", S_REP,
     "Um relatório customizado: tipo de relatório, formato, colunas, agrupamentos, filtros, fórmulas e gráfico.",
     "Versionar e implantar os relatórios da org entre ambientes.", "14.0", [
         P("aggregateFilters", "ReportAggregateFilter[]", "64.0", "Filtros sobre summary formulas customizadas.", estrutura="ReportAggregateFilter"),
         P("aggregates", "ReportAggregate[]", None, "Summary formulas customizadas, em relatórios summary, matrix e joined.", estrutura="ReportAggregate"),
         P("block", "Report[]", None, "Os blocos de um joined report; cada bloco tem o próprio tipo de relatório.", natureza="tipo_composto",
           contexto="Cada bloco é um Report aninhado."),
         P("blockInfo", "ReportBlockInfo", None, "Atributos de cada bloco de um joined report.", estrutura="ReportBlockInfo"),
         P("buckets", "ReportBucketField[]", "24.0", "Bucket fields usados no relatório.", estrutura="ReportBucketField"),
         P("chart", "ReportChart", None, "Gráfico de relatórios summary e matrix.", estrutura="ReportChart"),
         P("colorRanges", "ReportColorRange[]", None, "Destaque condicional de dados resumidos. Só no Salesforce Classic.", estrutura="ReportColorRange"),
         P("columns", "ReportColumn[]", None, "Campos mostrados; a ordem de exibição segue a ordem no arquivo.", estrutura="ReportColumn"),
         P("crossFilters", "ReportCrossFilter[]", "68.0", "Cross filters: objeto, objeto relacionado e condição com ou sem.", estrutura="ReportCrossFilter"),
         P("currency", "CurrencyIsoCode", None, "Moeda dos valores convertidos, em código ISO 4217, como USD.", natureza="desconhecida",
           contexto="A página não lista os códigos."),
         P("dataCategoryFilters", S, None, "Filtros por data category."),
         P("description", S, None, "Descrição mostrada com o nome do relatório; até 255 caracteres."),
         P("division", S, "17.0", "Os registros precisam ser desta division."),
         P("filter", "ReportFilter", None, "Limita o resultado a registros com certos dados.", estrutura="ReportFilter"),
         P("folderName", S, "35.0", "Pasta que contém o relatório."),
         P("format", "ReportFormat", None, "Formato do relatório.", vals=valores("Matrix", "Summary", "Tabular", "Joined")),
         P("formattingRules", "ReportFormattingRule[]", None, "Destaque condicional. Só no Lightning Experience.", estrutura="ReportFormattingRule"),
         P("groupingsAcross", "ReportGrouping[]", None, "Agrupamentos de coluna de um relatório matrix; no máximo 2.", estrutura="ReportGrouping"),
         P("groupingsDown", "ReportGrouping[]", None, "Agrupamentos de linha: até 2 em matrix e até 3 em summary.", estrutura="ReportGrouping"),
         P("historicalSelector", "ReportHistoricalSelector", "29.0", "Intervalo de datas dos dados de historical trending.", estrutura="ReportHistoricalSelector"),
         P("isSmartTotalDisabled", B, "29.0", "Com false, o relatório mostra o smart totalling."),
         P("name", S, None, "Nome do relatório.", "S"),
         P("numSubscriptions", I, "38.0", "1 se o usuário assina o relatório; 0 se não."),
         P("params", "ReportParam[]", None, "Opções de filtro próprias do tipo de relatório.", estrutura="ReportParam"),
         P("customDetailFormulas", "CustomDetailFormulas", None, "Row-level formulas.", estrutura="CustomDetailFormulas"),
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
         P("timeFrameFilter", "ReportTimeFrameFilter", None, "Limita o resultado a um período.", estrutura="ReportTimeFrameFilter"),
         P("userFilter", S, "17.0", "Nome de usuário usado para detalhar."),
         M.FULLNAME_HERDADO(None),
     ], exemplo=CAB + f"""<Report {NS}>
    <description>[o que o relatório responde]</description>
    <name>[nome do relatório]</name>
    <columns>
        <field>[campo]</field>
    </columns>
    <!-- Valores documentados: Matrix, Summary, Tabular, Joined -->
    <format>Summary</format>
    <groupingsDown>
        <field>[campo de agrupamento]</field>
        <sortOrder>Asc</sortOrder>
    </groupingsDown>
    <reportType>Opportunity</reportType>
    <showDetails>true</showDetails>
    <showGrandTotal>true</showGrandTotal>
    <sortColumn>[campo de ordenação]</sortColumn>
    <!-- Valores documentados: Asc, Desc -->
    <sortOrder>Asc</sortOrder>
    <timeFrameFilter>
        <dateColumn>[campo de data]</dateColumn>
        <!-- Valores documentados incluem: INTERVAL_CURY, INTERVAL_LAST30, INTERVAL_CUSTOM -->
        <interval>INTERVAL_CURY</interval>
    </timeFrameFilter>
</Report>""", curinga=False,
     arquivos_prontos=em_pasta("reports/<pasta>/", "<Nome>.report",
                               "Os relatórios ficam em subpastas da pasta reports. No source format, o arquivo recebe o sufixo -meta.xml.",
                               "report", S_REP),
     alertas=["Só relatórios customizados: os relatórios padrão não são suportados.",
              "O curinga (*) não funciona: liste as pastas com listMetadata() do tipo ReportFolder e depois os relatórios de cada pasta.",
              "Para referenciar só uma pasta aninhada, o nome dela precisa terminar com barra; sem a barra, a operação falha.",
              RESTAURA],
     divergencias=["O exemplo XML de joined report troca as tags aggregateReference e aggregateReferences na abertura e no fechamento.",
                   "Em ReportBucketField, ReportBucketFieldValue e ReportFormattingRule, a tabela tipa como enumeração campos que o exemplo XML "
                   "usa como elementos com filhos; foram cadastrados como estruturas.",
                   "ReportBucketFieldType e ReportBucketFieldNullTreatment são citados sem lista de valores."],
     cobertura_nota=NOTA_COB + " 40 campos no primeiro nível. " + LIDA_EM_PARTES.format("237.873", "três leituras: 0, 100.000 e 200.000", "21")
                    + " block (Report[]) é o próprio tipo Report, aninhado em joined reports.")

# ---------------------------------------------------------------- subtipos de Dashboard (página inteira lida em duas partes e na junção, 2026-11-16)
DSB = ["mdx:DashboardComponent"]
estrutura("DashboardFilterOption", S_DASH, ["mdx:DashboardFilter"], [
    P("operator", "DashboardFilterOperation", "24.0", "Operação do item de filtro.", "S", vals=OPERADORES + [("between", None)]),
    P("values", "string[]", "24.0", "Um ou mais valores do item de filtro.", "S"),
], "Uma opção de um filtro de dashboard.")
estrutura("DashboardFilter", S_DASH, ["mdt:Dashboard"], [
    P("dashboardFilterOptions", "DashboardFilterOption[]", None, "Opções que o usuário escolhe no filtro.", estrutura="DashboardFilterOption"),
    P("name", S, None, "Rótulo do filtro.", "S"),
], "Um filtro de dashboard.")
estrutura("DashboardFilterColumn", S_DASH, DSB, [
    P("column", S, None, "Código da coluna do relatório a que o filtro se aplica.", "S"),
], "A coluna do relatório de origem a que um filtro de dashboard se aplica.")
estrutura("DashboardTableColumn", S_DASH, DSB, [
    P("aggregateType", "ReportSummaryType[]", None, "Tipo de agregação da coluna.", vals=RESUMO),
    P("column", S, None, "Coluna mostrada na tabela.", "S"),
    P("showTotal", B, "19.0", "Mostra o total das colunas que podem ser somadas."),
    P("sortBy", "não informado na página", None, "Opção de ordenação da tabela; uma coluna por tabela.", natureza="desconhecida",
      contexto="A página tipa o campo como DashboardComponentSection, o que parece erro da página."),
], "Uma coluna de um componente de tabela customizado.")
estrutura("DashboardDynamicValue", S_DASH, DSB, [
    P("additionalInfo", S, None, "Metadados extras definidos pelo usuário."),
    P("fieldName", S, None, "Campo que fornece o valor dinâmico.", "S"),
    P("isDynamicUser", B, None, "Indica se o valor é obtido como o running user."),
], "Um valor dinâmico de um componente de dashboard.")
estrutura("DashboardComponentContent", S_DASH, DSB, [
    P("additionalInfo", S, None, "Metadados extras definidos pelo usuário."),
    P("altText", S, None, "Texto alternativo do componente."),
    P("componentParameters", S, None, "Parâmetros do componente."),
    P("fileName", S, None, "Nome do arquivo do componente."),
    P("fit", "Fit", None, "Ajuste da imagem.", vals=valores("FitHeight", "FitWidth", "Original", "Stretch", "Tile")),
    P("horizontalAlignment", "HorizontalAlignment", None, "Alinhamento horizontal.", vals=valores("Left", "Center", "Right")),
    P("richTextContent", S, None, "Conteúdo em rich text."),
    P("tooltip", S, None, "Dica mostrada ao passar o mouse."),
    P("verticalAlignment", "VerticalAlignment", None, "Alinhamento vertical.", vals=valores("Bottom", "Center", "Top")),
], "O conteúdo de um componente de imagem, rich text ou Lightning web component. Desde a API 58.0.")
estrutura("DashboardComponentColumn", S_DASH, ["mdx:DashboardFlexTableComponentProperties"], [
    P("breakPoint1", "double", None, "Valor que separa a cor baixa da cor do meio."),
    P("breakPoint2", "double", None, "Valor que separa a cor do meio da cor alta."),
    P("breakPointOrder", "double", None, "Ordem dos destaques condicionais quando há várias colunas."),
    P("highRangeColor", I, None, "Cor da faixa alta."),
    P("lowRangeColor", I, None, "Cor da faixa baixa."),
    P("midRangeColor", I, None, "Cor da faixa do meio."),
    P("reportColumn", S, None, "Código da coluna do relatório.", "S"),
    P("showTotal", B, None, "Mostra o total da coluna."),
    P("type", "DashboardComponentColumnType", "41.0", "Tipo da coluna da tabela do Lightning.", vals=valores("Details", "Aggregates", "Grouping")),
], "Uma coluna de uma tabela de dashboard do Lightning Experience. Desde a API 41.0.")
estrutura("DashboardComponentSortInfo", S_DASH, ["mdx:DashboardFlexTableComponentProperties"], [
    P("sortColumn", S, None, "Coluna usada na ordenação."), P("sortOrder", S, None, "Direção da ordenação, crescente ou decrescente."),
], "A ordenação de uma tabela de dashboard do Lightning Experience. Desde a API 41.0.")
estrutura("DashboardFlexTableComponentProperties", S_DASH, DSB, [
    P("decimalPrecision", I, None, "Número de dígitos significativos das colunas numéricas."),
    P("flexTableColumn", "DashboardComponentColumn", "41.0", "Uma coluna da tabela; o elemento se repete.", estrutura="DashboardComponentColumn"),
    P("flexTableSortInfo", "DashboardComponentSortInfo", "41.0", "Coluna e direção da ordenação.", estrutura="DashboardComponentSortInfo"),
    P("hideChatterPhotos", B, "41.0", "Esconde as fotos do Chatter."),
    P("useReportTableSetting", B, "65.0", "Permite importar as configurações de tabela do relatório."),
], "As colunas e a ordenação de uma tabela de dashboard do Lightning Experience.")
estrutura("DashboardComponentGroupingSort", S_DASH, ["mdx:DashboardComponentGroupingSortProperties"], [
    P("groupingLevel", S, None, "Nível de agrupamento em que a ordenação vale."),
    P("inheritedReportGroupingSort", S, None, "Indica se a ordem vem do relatório de origem."),
    P("sortColumn", S, None, "Agregação usada na ordenação; nula quando ordena pelo próprio valor."),
    P("sortOrder", S, None, "Direção: Ascending ou Descending."),
], "A ordenação de um nível de agrupamento de um componente.")
estrutura("DashboardComponentGroupingSortProperties", S_DASH, DSB, [
    P("groupingSorts", "DashboardComponentGroupingSort", "46.0", "Ordenação de cada nível de agrupamento; o elemento se repete.",
      estrutura="DashboardComponentGroupingSort"),
], "As ordenações por nível de agrupamento de um componente.")
estrutura("DashboardComponent", S_DASH, ["mdx:DashboardGridComponent", "mdx:DashboardComponentSection"], [
    P("chartAxisRange", "ChartRangeType", None, "Faixa do eixo, automática ou manual, em gráficos de barra e linha.", vals=valores("auto", "manual"),
      notas=["Na página de Dashboard os valores vêm em minúsculas; na de Report, com inicial maiúscula."]),
    P("chartAxisRangeMax", "double", None, "Valor máximo do eixo; só com faixa manual."),
    P("chartAxisRangeMin", "double", None, "Valor mínimo do eixo; só com faixa manual."),
    P("chartSummary", "ChartSummary", "25.0", "Campo de resumo dos dados do gráfico.", "C:obrigatório quando isAutoSelectFromReport é false",
      estrutura="ChartSummary"),
    P("componentType", "DashboardComponentType", None, "Tipo do componente.", "S", vals=valores(
        "Bar", "BarGrouped", "BarStacked", "BarStacked100", "Column", "ColumnGrouped", "ColumnLine", "ColumnLineGrouped", "ColumnLineStacked",
        "ColumnLineStacked100", "ColumnStacked", "ColumnStacked100", "Donut", "FlexTable", "Funnel", "Gauge", "Image", "LightningWebComponent", "Line",
        "LineCumulative", "LineGrouped", "LineGroupedCumulative", "Metric", "Pie", "PulseMetricCard", "RichText", "Scatter", "ScatterGrouped",
        "SControl", "Table", "VisualforcePage")),
    P("dashboardComponentContents", "DashboardComponentContent[]", "58.0", "Conteúdos do componente.", estrutura="DashboardComponentContent"),
    P("dashboardDynamicValues", "DashboardDynamicValue[]", "36.0", "Valores dinâmicos.", estrutura="DashboardDynamicValue"),
    P("dashboardFilterColumns", "DashboardFilterColumn[]", "23.0", "Colunas a que os filtros se aplicam; componentes de relatório precisam de uma.",
      estrutura="DashboardFilterColumn"),
    P("dashboardTableColumn", "DashboardTableColumn[]", None, "Colunas de um componente de tabela customizado.", estrutura="DashboardTableColumn"),
    P("displayUnits", "ChartUnits", None, "Unidade dos valores do gráfico.", vals=valores(
        "Auto", "Integer", "Hundreds", "Thousands", "Millions", "Billions", "Trillions")),
    P("drillDownUrl", S, None, "URL aberta ao clicar; tem precedência sobre as opções de drill."),
    P("drillEnabled", B, "17.0", "Ao clicar, abre o relatório de origem, completo ou filtrado."),
    P("drillToDetailEnabled", B, "20.0", "Ao clicar, abre as páginas de detalhe dos registros."),
    P("enableHover", B, "17.0", "Mostra valores, rótulos e percentuais ao passar o mouse."),
    P("expandOthers", B, "17.0", "Junta grupos de 3% ou menos numa fatia Outros."),
    P("flexComponentProperties", "DashboardFlexTableComponentProperties", "41.0", "Colunas e ordenação de tabelas do Lightning.",
      estrutura="DashboardFlexTableComponentProperties"),
    P("footer", S, None, "Texto do rodapé; até 255 caracteres."),
    P("gaugeMax", "double", None, "Valor máximo do medidor."),
    P("gaugeMin", "double", None, "Valor mínimo do medidor."),
    P("groupingColumn", S, "25.0", "Campo usado para agrupar os dados no eixo."),
    P("GroupingSortProperties", "DashboardComponentGroupingSortProperties", "46.0", "Ordenação quando há agrupamentos.",
      estrutura="DashboardComponentGroupingSortProperties", notas=["O nome começa com maiúscula na página."]),
    P("header", S, None, "Texto do cabeçalho; até 80 caracteres."),
    P("indicatorBreakpoint1", "double", None, "Valor que separa as cores baixa e do meio do medidor."),
    P("indicatorBreakpoint2", "double", None, "Valor que separa as cores do meio e alta do medidor."),
    P("indicatorHighColor", S, None, "Cor da faixa alta do medidor."),
    P("indicatorLowColor", S, None, "Cor da faixa baixa do medidor."),
    P("indicatorMiddleColor", S, None, "Cor da faixa do meio do medidor."),
    P("legendPosition", "ChartLegendPosition", None, "Posição da legenda.", vals=valores("Bottom", "OnChart", "Right")),
    P("maxValuesDisplayed", I, None, "Máximo de elementos no agrupamento de nível superior."),
    P("metricLabel", S, None, "Rótulo de um componente de métrica."),
    P("page", S, None, "Página Visualforce associada."),
    P("pageHeightInPixels", I, None, "Altura da página Visualforce, em pixels."),
    P("report", S, None, "Nome do relatório de origem."),
    P("scontrol", S, None, "S-control associado, em componentes de s-control."),
    P("scontrolHeightInPixels", I, None, "Altura do s-control, em pixels."),
    P("showPercentage", B, None, "Mostra percentuais em medidores e gráficos de pizza, rosca e funil."),
    P("showPicturesOnCharts", B, None, "Mostra fotos do Chatter em certos gráficos de barra."),
    P("showPicturesOnTables", B, None, "Mostra fotos do Chatter em certas tabelas."),
    P("showTotal", B, None, "Mostra o total em medidores e gráficos de rosca."),
    P("showValues", B, None, "Mostra os valores dos registros ou grupos."),
    P("sortBy", "DashboardComponentFilter", None, "Opção de ordenação do componente.", vals=valores(
        "RowLabelAscending", "RowLabelDescending", "RowValueAscending", "RowValueDescending")),
    P("sortLegendValues", B, None, "Ordena os valores da legenda."),
    P("title", S, None, "Título do componente; até 40 caracteres."),
    P("useReportChart", B, None, "Usa o gráfico definido no relatório de origem."),
], "Um componente de dashboard: gráfico, tabela, métrica, medidor, imagem, rich text, página Visualforce ou Lightning web component.")
estrutura("DashboardGridComponent", S_DASH, ["mdx:DashboardGridLayout"], [
    P("colSpan", I, None, "Largura do componente, em colunas.", "S"),
    P("columnIndex", I, None, "Coluna mais à esquerda ocupada pelo componente.", "S"),
    P("dashboardComponent", "DashboardComponent", None, "O componente posicionado.", "S", estrutura="DashboardComponent"),
    P("rowIndex", I, None, "Linha mais alta ocupada pelo componente.", "S"),
    P("rowSpan", I, None, "Altura do componente, em linhas.", "S"),
], "A posição e o tamanho de um componente na grade de um dashboard do Lightning Experience.")
estrutura("DashboardGridLayout", S_DASH, ["mdt:Dashboard"], [
    P("dashboardGridComponents", "DashboardGridComponent[]", None, "Componentes do dashboard.", estrutura="DashboardGridComponent"),
    P("numberOfColumns", I, None, "Número de colunas do dashboard.", "S"),
    P("rowHeight", I, None, "Altura de cada linha, em pixels.", "S"),
], "A grade de um dashboard do Lightning Experience.")
estrutura("DashboardComponentSection", S_DASH, ["mdt:Dashboard"], [
    P("columnSize", "DashboardComponentSize", None, "Largura da coluna.", "S", vals=valores("Medium", "Narrow", "Wide")),
    P("components", "DashboardComponent[]", None, "Componentes da coluna.", estrutura="DashboardComponent"),
], "Uma coluna de um dashboard em colunas (layout do Salesforce Classic).")

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
         P("dashboardFilters", "DashboardFilter[]", "23.0", "Filtros do dashboard.", estrutura="DashboardFilter"),
         P("dashboardGridLayout", "DashboardGridLayout", "35.0", "Componentes em grade, número de colunas e altura das linhas.", estrutura="DashboardGridLayout"),
         P("dashboardType", "DashboardType", "19.0", "De quem é o acesso que define os dados mostrados.", vals=[
             ("SpecifiedUser", None), ("LoggedInUser", None), ("MyTeamUser", "Desde a API 20.0.")]),
         P("description", S, None, "Descrição do dashboard; até 255 caracteres."),
         P("folderName", S, "35.0", "Pasta que contém o dashboard."),
         P("fullName", S, None, "Caminho com pasta e título, como folderSales/California. Herdado do tipo Metadata.",
           "C:obrigatório ao criar, atualizar ou excluir", herdada="Metadata"),
         P("isGridLayout", B, "35.0", "Com true, o dashboard usa o layout do Lightning Experience."),
         P("dashboardResultRefreshedDate", S, None, "Data da última atualização do dashboard.", "S"),
         P("dashboardResultRunningUser", S, None, "Usuário que está vendo o dashboard.", "S"),
         P("leftSection", "DashboardComponentSection", None, "Coluna esquerda do dashboard.", "S", estrutura="DashboardComponentSection"),
         P("middleSection", "DashboardComponentSection", None, "Coluna do meio do dashboard.", estrutura="DashboardComponentSection"),
         P("numSubscriptions", I, "42.0", "Número de assinaturas do dashboard."),
         P("owner", S, None, "Quem criou o dashboard."),
         P("rightSection", "DashboardComponentSection", None, "Coluna direita do dashboard.", "S", estrutura="DashboardComponentSection"),
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
    <leftSection>
        <!-- Valores documentados: Medium, Narrow, Wide -->
        <columnSize>Medium</columnSize>
        <components>
            <!-- Valores documentados incluem: Bar, Column, Donut, Gauge, Metric, Table -->
            <componentType>Column</componentType>
            <report>[pasta/nome do relatório de origem]</report>
        </components>
    </leftSection>
    <rightSection>
        <columnSize>Medium</columnSize>
    </rightSection>
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
                   "Experience; a página não explica como os dois se combinam.",
                   "O exemplo XML de layout em grade usa autoselectColumnsFromReport, e a linha de chartSummary cita isAutoSelectFromReport; "
                   "nenhum dos dois está nas tabelas de campos e não foram cadastrados.",
                   "DashboardTableColumn.sortBy vem tipado como DashboardComponentSection, o que parece erro da página.",
                   "Os textos de introdução de DashboardFilterColumn, DashboardComponentSortInfo e DashboardFlexTableComponentProperties não "
                   "correspondem aos títulos das seções."],
     cobertura_nota=NOTA_COB + " 26 campos no primeiro nível. " + LIDA_EM_PARTES.format(
         "173.302", "leituras a partir de 0, 90.000 e 100.000, para cobrir a junção", "16")
                    + " ChartSummary, definido na página de Report, também é usado aqui.")

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

C.funcionalidade(
    "crm-analytics", "CRM Analytics", "CRM Analytics", ["tableau crm", "einstein analytics", "wave", "dataset", "lens", "recipe", "dataflow",
                                                        "data manager", "analytics studio"],
    "CRM Analytics (antes Tableau CRM) é a plataforma analítica que conecta dados de várias fontes, prepara-os em datasets com recipes e "
    "dataflows e os mostra em lenses e dashboards interativos, organizados em apps. É vendido à parte, com licenças próprias.",
    "Analisar grandes volumes de dados, de dentro e de fora da org, com visualizações interativas que os relatórios nativos não oferecem.",
    "Um gerente de vendas abre o app de desempenho e filtra, no próprio dashboard, as cadências em andamento e as taxas de resposta de cada vendedor.",
    (REL, "recursos-analiticos-de-produto"), [], [], [],
    ["src:help-crm-analytics-sales-engagement", "src:help-crm-analytics-data-prep", "src:help-crm-analytics-permissions",
     "src:help-kb-crm-analytics-enable", "src:help-crm-analytics-licenses", "src:help-crm-analytics-limits", "src:help-crm-analytics-row-limit",
     "src:help-crm-analytics-data-manager", "src:help-produtos-analytics"],
    [{"tipo": "metadata_type", "estado": "desconhecido",
      "motivo": "WaveApplication, WaveDashboard, WaveLens, WaveDataflow, WaveRecipe e WaveTemplateBundle constam do inventário v68; as páginas "
                "deles não foram lidas e eles não foram cadastrados."}, SEM_OBJ],
    SEM_SETUP,
    limitacoes=["O total de linhas em datasets depende das licenças (por exemplo, 10 bilhões com CRM Analytics Plus e 100 milhões com Growth); "
                "cada dataset aceita até 2 bilhões de linhas.",
                "O limite de linhas é contratual: a Ajuda diz que cabe ao cliente acompanhar o total."],
    alertas=["Habilitar o CRM Analytics não dá acesso a ninguém: é preciso atribuir permission sets, e cada usuário precisa da permission set "
             "license correspondente.",
             "Desabilitar remove todas as permissões de CRM Analytics dos permission sets e para recipes e dataflows agendados; apps, datasets, "
             "lenses e dashboards não são apagados.",
             "Ao atingir o limite de linhas, recipes, dataflows, data sync e upload de arquivos param até o uso cair.",
             "O Data Manager concentra monitoramento de jobs, fontes de dados, recipes e uso."])

print(f"lote 7g: 7 metadata types e {sum(1 for r in REGISTRADOS if r[1] == 'estruturas')} estruturas gravados; 6 funcionalidades novas")
