"""Lote 7l (rodada B4, issues #8 e #9): subtipos que faltavam em tipos centrais e campos das exposições Tooling já confirmadas.

- #9: estruturas de KnowledgeSettings (12) e ForecastingSettings (11), relidas no guia versionado 264.0.
- #8: Profile (ProfileUserPermission, ProfileServicePresenceStatusAccess, com a página relida inteira); CustomObject (BusinessProcess,
  FieldSet e Index como metadata types filhos; SearchLayouts, ProfileSearchLayouts e HistoryRetentionPolicy como estruturas);
  CustomField (Picklist, descontinuado, e FilterItem em summaryFilterItems); ValueSet (ValueSettings e CustomValue);
  campos e chamadas da Tooling API para Profile, PermissionSet, PermissionSetGroup, PermissionSetAssignment, User e RecordType.

Os tipos Profile, CustomObject, CustomField, RecordType, KnowledgeSettings e ForecastingSettings vêm de lotes históricos (catálogo em JSON
é a fonte da verdade): este script liga as estruturas novas às propriedades deles e recalcula a cobertura estrutural.

Ordem: lote7k_qualidade_fecho.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7l_b4_estruturas.py
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga import obj as O                    # noqa: E402
from carga.base import ev, ld, sv, caminho    # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7l-b4-estruturas.txt"
ATLAS = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
TOOL = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_tooling.meta/api_tooling/tooling_api_objects_"


def substituir_fontes(novas):
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


PAGINAS = {  # id -> (título, página, pertinência)
    "src:mdapi-knowledgesettings-subtipos": ("KnowledgeSettings, subtipos (Metadata API)", "meta_knowledgesettings", "Subtipos de KnowledgeSettings."),
    "src:mdapi-forecastingsettings-subtipos": ("ForecastingSettings, subtipos (Metadata API)", "meta_forecastingsettings", "Subtipos de ForecastingSettings."),
    "src:mdapi-profile-subtipos": ("Profile, segunda parte da página (Metadata API)", "meta_profile", "Subtipos de Profile depois do primeiro corte de leitura."),
    "src:mdapi-field-types-v264": ("Field Types, ValueSettings (Metadata API)", "meta_field_types", "Subtipo ValueSettings de ValueSet."),
    "src:mdapi-customvalue": ("CustomValue (Metadata API)", "meta_customvalue", "Campos de CustomValue e StandardValue."),
    "src:mdapi-picklist": ("Picklist, descontinuado (Metadata API)", "meta_picklist", "Campos de Picklist, usado até a API 37.0."),
    "src:mdapi-businessprocess": ("BusinessProcess (Metadata API)", "meta_businessprocess", "Arquivo, versão e propriedades do tipo BusinessProcess."),
    "src:mdapi-fieldset": ("FieldSet (Metadata API)", "meta_fieldset", "Arquivo, versão e propriedades do tipo FieldSet."),
    "src:mdapi-index": ("Index (Metadata API)", "meta_index", "Arquivo, versão e propriedades do tipo Index."),
    "src:mdapi-searchlayouts": ("SearchLayouts (Metadata API)", "meta_searchlayouts", "Campos de SearchLayouts."),
    "src:mdapi-profilesearchlayouts": ("ProfileSearchLayouts (Metadata API)", "meta_profilesearchlayouts", "Campos de ProfileSearchLayouts."),
    "src:mdapi-historyretentionpolicy": ("HistoryRetentionPolicy (Metadata API)", "meta_historyretentionpolicy", "Campos de HistoryRetentionPolicy."),
}
TOOLING = ("Profile", "PermissionSet", "PermissionSetGroup", "PermissionSetAssignment", "User", "RecordType")
substituir_fontes([C.fonte(i, t, ATLAS + pg + ".htm", pert, EXTR, DATA) for i, (t, pg, pert) in PAGINAS.items()]
                  + [C.fonte(f"src:tooling-{n.lower()}", f"{n} (Tooling API)", TOOL + n.lower() + ".htm", f"Chamadas e campos do objeto {n} na Tooling API.",
                             EXTR, DATA) for n in TOOLING])
S_K, S_F, S_PR, S_FT, S_CV, S_PK, S_BP, S_FS, S_IX, S_SL, S_PSL, S_HRP = PAGINAS
B, S, I = "boolean", "string", "int"
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
REG = []


def estrutura(nome, src, usada_por, rows, o_que_e):
    M.struct(nome, src, usada_por, rows, o_que_e)
    REG.append((src, "estruturas", nome))


def valores(*vs):
    return [(v, None) for v in vs]


# ================================================================ #9 KnowledgeSettings
KS = ["mdt:KnowledgeSettings"]
estrutura("KnowledgeAnswerSettings", S_K, KS, [
    P("assignTo", S, None, "Username a quem são atribuídos os artigos criados a partir do Answers."),
    P("defaultArticleType", S, None, "Tipo de artigo padrão desses artigos, pelo nome de API."),
    P("enableArticleCreation", B, None, "Permite criar artigos a partir do Answers."),
], "Opções de criação de artigos a partir do Answers.")
SITES = "KnowledgeSitesSettings"
estrutura("KnowledgeCaseSettings", S_K, KS, [
    P("articlePDFCreationProfile", S, None, "Perfil usado para gerar o PDF de artigos a partir de casos."),
    P("articlePublicSharingCommunities", SITES, None, "Sites do Experience Cloud em que artigos de casos podem ser compartilhados publicamente.", estrutura=SITES),
    P("articlePublicSharingSites", SITES, None, "Sites em que artigos de casos podem ser compartilhados publicamente.", estrutura=SITES),
    P("articlePublicSharingSitesChatterAnswers", SITES, None, "Sites com Chatter Answers para compartilhamento público de artigos de casos.", estrutura=SITES),
    P("assignTo", S, None, "Username a quem são atribuídos os artigos criados a partir de casos."),
    P("customizationClass", S, None, "Classe Apex usada para customização."),
    P("defaultContributionArticleType", S, None, "Tipo de artigo padrão dos artigos criados a partir de casos."),
    P("editor", "KnowledgeCaseEditor", None, "Tipo de editor de rich text.", vals=valores("simple", "standard"),
      notas=["A página não explica a diferença entre os dois valores."]),
    P("enableArticleCreation", B, None, "Permite criar artigos a partir de casos; condiciona os outros campos de casos."),
    P("enableArticlePublicSharingSites", B, None, "Permite compartilhar artigos de casos por URL pública de site."),
    P("enableCaseDataCategoryMapping", B, None, "Liga o mapeamento de data categories em casos."),
    P("useProfileForPDFCreation", B, None, "Usa um perfil para criar o PDF de artigos a partir de casos."),
], "Opções de Knowledge ligadas a casos: criação de artigos, PDF e compartilhamento público.")
estrutura("KnowledgeSitesSettings", S_K, ["mdx:KnowledgeCaseSettings"], [
    P("site", "string[]", None, "Nomes dos sites."),
], "Uma lista de sites usada pelas opções de compartilhamento público.")
estrutura("KnowledgeLanguage", S_K, ["mdx:KnowledgeLanguageSettings"], [
    P("active", B, "28.0", "Indica se o idioma está ligado."),
    P("defaultAssignee", S, "28.0", "Responsável padrão pelos artigos do idioma."),
    P("defaultAssigneeType", "KnowledgeLanguageLookupValueType", "28.0", "Tipo do responsável padrão.", vals=valores("User", "Queue")),
    P("defaultReviewer", S, "28.0", "Revisor padrão dos artigos do idioma."),
    P("defaultReviewerType", "KnowledgeLanguageLookupValueType", "28.0", "Tipo do revisor padrão.", vals=valores("User", "Queue")),
    P("name", S, "28.0", "Código do idioma, como en para inglês."),
], "Um idioma do Knowledge, com responsável e revisor padrão.")
estrutura("KnowledgeLanguageSettings", S_K, KS, [
    P("language", "KnowledgeLanguage[]", "28.0", "Idiomas habilitados no Knowledge.", estrutura="KnowledgeLanguage"),
], "Os idiomas do Knowledge.")
for nome, campo, desde, o_que in (("KnowledgeCaseField", "Campo de caso", "37.0", "casos"), ("KnowledgeWorkOrderField", "Campo de ordem de serviço", "39.0", "ordens de serviço"),
                                  ("KnowledgeWorkOrderLineItemField", "Campo de item de ordem de serviço", "39.0", "itens de ordem de serviço")):
    estrutura(nome, S_K, [f"mdx:{nome.replace('Field', 'FieldsSettings')}"], [
        P("name", S, desde, f"{campo} usado para sugerir artigos."),
    ], f"Um campo usado para sugerir artigos em {o_que}.")
    estrutura(f"{nome.replace('Field', 'FieldsSettings')}", S_K, ["mdx:KnowledgeSuggestedArticlesSettings"], [
        P("field", f"{nome}[]", desde, f"Campos de {o_que} usados para sugerir artigos.", estrutura=nome),
    ], f"Os campos de {o_que} usados para sugerir artigos.")
estrutura("KnowledgeSuggestedArticlesSettings", S_K, KS, [
    P("caseFields", "KnowledgeCaseFieldsSettings", None, "Campos de caso usados para sugerir artigos.", estrutura="KnowledgeCaseFieldsSettings"),
    P("useSuggestedArticlesForCase", B, None, "Usa o conteúdo do caso para sugerir artigos."),
    P("workOrderFields", "KnowledgeWorkOrderFieldsSettings", None, "Campos de ordem de serviço usados para sugerir artigos.",
      estrutura="KnowledgeWorkOrderFieldsSettings"),
    P("workOrderLineItemFields", "KnowledgeWorkOrderLineItemFieldsSettings", None, "Campos de item de ordem de serviço usados para sugerir artigos.",
      estrutura="KnowledgeWorkOrderLineItemFieldsSettings"),
], "As opções de sugestão de artigos em casos e ordens de serviço.")

# ================================================================ #9 ForecastingSettings
FS_ = ["mdt:ForecastingSettings"]
SO_LEITURA = "Somente leitura."
estrutura("WeightedSourceCategory", S_F, ["mdx:ForecastingCategoryMapping"], [
    P("sourceCategoryApiName", S, None, "Categoria de previsão incluída no acumulado: pipeline, best case, commit, closed, omitted ou customcategory.", "S"),
    P("weight", "double", None, "Peso da categoria no acumulado; o único valor aceito é 1.0.", "S"),
], "Uma categoria de previsão que entra num acumulado.")
estrutura("ForecastingCategoryMapping", S_F, FS_, [
    P("forecastingItemCategoryApiName", S, None, "Tipo de acumulado; openpipeline, bestcaseforecast e commitforecast são cumulativos.", "S"),
    P("weightedSourceCategories", "WeightedSourceCategory[]", None, "Categorias de previsão incluídas no acumulado.", estrutura="WeightedSourceCategory"),
], "Como as categorias de previsão se somam em cada acumulado.")
estrutura("ForecastingDisplayedFamilySettings", S_F, FS_, [
    P("productFamily", S, "40.0", "Família de produto permitida nas previsões do Lightning; cada uma aparece uma vez."),
], "Uma família de produto mostrada nas previsões.")
estrutura("ForecastingSubmissionSettings", S_F, FS_, [
    P("allowForecastingSubmissions", B, None, "Liga o envio de previsões num momento definido.", "S",
      notas=["A propriedade de ForecastingSettings que usa esta estrutura existe desde a API 62.0."]),
], "A opção de envio de previsões.")
estrutura("AdjustmentsSettings", S_F, FS_ + ["mdx:ForecastingTypeSettings"], [
    P("allowExpandedColumns", B, None, "Com true, uma coluna por categoria ajustável; com false, o ajuste aparece ao passar o mouse.", "S"),
    P("enableAdjustments", B, None, "Liga os ajustes de gerente; desligar apaga os dados de ajuste.", "S"),
    P("enableOwnerAdjustments", B, None, "Liga os ajustes do dono; desligar apaga os dados de ajuste.", "S"),
], "As opções de ajuste de previsões; precisam ser iguais em todos os tipos de previsão.")
estrutura("ForecastRangeSettings", S_F, FS_ + ["mdx:ForecastingTypeSettings"], [
    P("beginning", I, None, "Mês ou trimestre inicial mostrado por padrão.", "S"),
    P("displaying", I, None, "Quantos meses (até 12) ou trimestres (até 8) aparecem por padrão.", "S"),
    P("periodType", "PeriodTypes", None, "Unidade do período.", "S", vals=valores("Month", "Quarter", "Week", "Year")),
], "O intervalo de períodos mostrado por padrão nas previsões.")
estrutura("QuotasSettings", S_F, FS_ + ["mdx:ForecastingTypeSettings"], [
    P("showQuotas", B, None, "Liga as cotas; precisa ser igual em todos os tipos de previsão.", "S"),
], "A opção de cotas.")
estrutura("OpportunityListFieldsLabelMapping", S_F, ["mdx:ForecastingTypeSettings"], [
    P("field", S, None, "Nome de API do campo de oportunidade.", "S"), P("label", S, None, "Rótulo do campo na interface.", "S"),
], "O rótulo de um campo de oportunidade no painel de previsões.")
estrutura("OpportunityListFieldsSelectedSettings", S_F, ["mdx:ForecastingTypeSettings"], [
    P("field", S, None, "Campo mostrado no painel de oportunidades."),
], "Os campos mostrados no painel de oportunidades das previsões.")
estrutura("OpportunityListFieldsUnselectedSettings", S_F, ["mdx:ForecastingTypeSettings"], [
    P("field", S, None, "Campo que não aparece no painel de oportunidades."),
], "Os campos que não aparecem no painel de oportunidades das previsões.")
REMOVIDO = "Removido na API 53.0; use {}."
estrutura("ForecastingTypeSettings", S_F, FS_, [
    P("active", B, None, "Ativa o tipo de previsão; com false, apaga dados de previsão, ajustes e cotas dele.", "S"),
    P("adjustmentsSettings", "AdjustmentsSettings", None, REMOVIDO.format("globalAdjustmentsSettings"), estrutura="AdjustmentsSettings", ate="52.0"),
    P("displayedCategoryApiNames", S, None, SO_LEITURA + " As quatro categorias mostradas na aba Forecasts."),
    P("forecastedCategoryApiNames", S, None, "As quatro categorias acumuladas usadas; a escolha define acumulado cumulativo ou individual."),
    P("forecastingDateType", "ForecastingDateType", "42.0", "Data usada como base dos valores.", "S", natureza="desconhecida",
      default=("valor", "OpportunityCloseDate", "A página declara OpportunityCloseDate como padrão."),
      contexto="A página cita OpportunityCloseDate, ProductDate, ScheduleDate, formas DateOnly e data customizada (57.0), sem lista fechada."),
    P("forecastRangeSettings", "ForecastRangeSettings", None, REMOVIDO.format("globalForecastRangeSettings"), estrutura="ForecastRangeSettings", ate="52.0"),
    P("hasProductFamily", B, "41.0", "Liga previsões por família de produto neste tipo.", "S"),
    P("isAmount", B, None, SO_LEITURA + " true se o tipo usa valores de receita.", "S"),
    P("isAvailable", B, None, SO_LEITURA + " Se o tipo pode ser usado agora; splits exigem Opportunity Splits.", "S"),
    P("isQuantity", B, None, SO_LEITURA + " true se o tipo usa quantidades de produto.", "S"),
    P("managerAdjustableCategoryApiNames", S, None, SO_LEITURA + " As duas categorias que gerentes podem ajustar."),
    P("masterLabel", S, None, SO_LEITURA + " Rótulo do tipo de previsão.", "S"),
    P("name", S, None, "Nome do tipo de previsão, entre os nomes aceitos, como OpportunityRevenue.", "S"),
    P("opportunityListFieldsLabelMappings", "OpportunityListFieldsLabelMapping", None, SO_LEITURA + " Rótulos dos campos de oportunidade.",
      estrutura="OpportunityListFieldsLabelMapping"),
    P("opportunityListFieldsSelectedSettings", "OpportunityListFieldsSelectedSettings", None, "Campos do painel de oportunidades; inclui Opportunity Name; até 15.",
      "S", estrutura="OpportunityListFieldsSelectedSettings"),
    P("opportunityListFieldsUnselectedSettings", "OpportunityListFieldsUnselectedSettings", None, "Campos fora do painel de oportunidades.", "S",
      estrutura="OpportunityListFieldsUnselectedSettings"),
    P("opportunitySplitName", S, "41.0", "Tipo de split usado, se houver."),
    P("ownerAdjustableCategoryApiNames", S, None, SO_LEITURA + " As duas categorias que donos podem ajustar."),
    P("quotasSettings", "QuotasSettings", None, REMOVIDO.format("globalQuotasSettings"), estrutura="QuotasSettings", ate="52.0"),
    P("territory2ModelName", S, "41.0", "Modelo de territórios usado, se houver."),
], "Um tipo de previsão: o que é previsto, com que categorias, datas e campos.")

# ================================================================ #8 Profile
estrutura("ProfileUserPermission", S_PR, ["mdt:Profile"], [
    P("enabled", B, None, "Indica se a permissão está ligada.", "S"),
    P("name", S, None, "Nome da permissão de app ou de sistema.", "S"),
], "Uma permissão de usuário (de app ou de sistema) do perfil.")
estrutura("ProfileServicePresenceStatusAccess", S_PR, ["mdt:Profile"], [
    P("enabled", B, "64.0", "Indica se os atendentes do perfil podem usar o status.", "S"),
    P("servicePresenceStatus", S, "64.0", "Nome do Service Presence Status.", "S"),
], "O acesso do perfil a um status de presença do Omni-Channel.")

# ================================================================ #8 CustomField e ValueSet
estrutura("CustomValue", S_CV, ["mdx:ValueSetValuesDefinition"], [
    P("color", S, None, "Cor em hexadecimal usada em gráficos; atribuída automaticamente se omitida."),
    P("default", B, None, "Marca o valor padrão do picklist.", "S"),
    P("description", S, None, "Por que o valor existe; até 255 caracteres."),
    P("isActive", B, None, "Indica se o valor está ativo; valores inativos não podem ser escolhidos.",
      default=("valor", True, "A página declara default true.")),
    P("label", S, "39.0", "Rótulo do valor; por padrão, o nome de API."),
    M.FULLNAME_HERDADO(None, "Nome de API do valor; herdado do tipo Metadata."),
], "Um valor de um picklist local ou global. Desde a API 38.0, substitui GlobalPicklistValue.")
estrutura("ValueSettings", S_FT, ["mdx:ValueSet"], [
    P("controllingFieldValue", "string[]", None, "Valores do picklist controlador de que este valor depende. A Metadata API acrescenta, mas não remove.",
      notas=["A página mostra o tipo como stringstring[], provável erro de digitação."]),
    P("valueName", S, None, "Nome do valor no picklist dependente."),
], "A dependência de um valor de picklist dependente em relação aos valores do campo controlador.")
estrutura("Picklist", S_PK, ["mdt:CustomField"], [
    P("controllingField", S, "14.0", "Campo controlador de um picklist dependente."),
    P("picklistValues", "PicklistValue[]", None, "Os valores do picklist.", "S", natureza="tipo_composto",
      contexto="PicklistValue não tem seção nesta página, e a página própria (meta_picklistvalue) devolveu conteúdo ilegível."),
    P("restrictedPicklist", B, "37.0", "Só administradores alteram os valores.", default=("false", False, "A página declara default false.")),
    P("sorted", B, None, "Indica se os valores são ordenados.", default=("false", False, "A página declara default false.")),
], "O picklist de um campo até a API 37.0. Descontinuado: da 38.0 em diante, usa-se valueSet.")

# ================================================================ #8 CustomObject
CO = ["mdt:CustomObject"]
SLD = [("customTabListAdditionalFields", "Campos extras na lista Recent do objeto."), ("excludedStandardButtons", "Botões padrão retirados do layout de busca."),
       ("listViewButtons", "Botões mostrados nas list views do objeto."), ("lookupDialogsAdditionalFields", "Campos extras nas janelas de busca de lookup."),
       ("lookupFilterFields", "Campos que filtram enhanced lookups."), ("lookupPhoneDialogsAdditionalFields", "Campos de telefone nas janelas de lookup ligadas ao softphone."),
       ("massQuickActions", "Quick actions de criação ou atualização executadas em lote."), ("searchFilterFields", "Campos que refinam buscas do objeto."),
       ("searchResultsAdditionalFields", "Campos extras nos resultados de busca."), ("searchResultsCustomButtons", "Botões customizados nos resultados de busca.")]
estrutura("SearchLayouts", S_SL, CO, [P(n, "string[]", None, d) for n, d in SLD],
          "Os layouts de busca e de lookup de um objeto: colunas e botões mostrados em buscas, lookups e listas.")
estrutura("ProfileSearchLayouts", S_PSL, CO, [
    P("fields", "string[]", "48.0", "Campos mostrados nos resultados de busca para o perfil."),
    P("profileName", "string[]", "48.0", "Perfil a que o layout de busca se aplica."),
], "Um layout de resultados de busca por perfil. Desde a API 48.0, em objetos customizados.")
estrutura("HistoryRetentionPolicy", S_HRP, CO, [
    P("archiveAfterMonths", I, "31.0", "Meses antes de arquivar o histórico, de 1 a 18.", "S", default=("valor", 18, "A página declara 18 como padrão.")),
    P("archiveRetentionYears", I, "31.0", "Anos até a exclusão manual do arquivo; serve só de lembrete, sem exclusão automática."),
    P("description", S, "31.0", "Descrição da política."),
    P("gracePeriodDays", I, "31.0", "Dias extras antes do primeiro arquivamento, de 0 a 10.", default=("valor", 1, "A página declara 1 como padrão.")),
], "A política de retenção do histórico de campos de um objeto (Field Audit Trail).")
estrutura("FieldSetItem", S_FS, ["mdt:FieldSet"], [
    P("field", S, None, "Nome do campo.", "S"),
    P("isFieldManaged", B, None, "Somente leitura. Indica se o campo veio de um pacote."),
    P("isRequired", B, None, "Somente leitura. Indica se o campo é obrigatório em todo lugar."),
], "Um campo de um field set.")
estrutura("IndexField", S_IX, ["mdt:Index"], [
    P("name", S, "41.0", "Nome de API de um campo do índice; precisa ser um campo obrigatório do big object.", "S"),
    P("sortDirection", S, "41.0", "Ordem do campo no índice.", "S", vals=valores("ASC", "DESC")),
], "Um campo de um índice de big object.")

M.mdt("BusinessProcess", S_BP,
      "Um business process: o conjunto de valores de picklist que um processo usa (fases de oportunidade, status de caso ou de lead, status "
      "de solução), atribuído a record types.",
      "Versionar e implantar os business processes junto com o objeto.", "17.0", [
          P("description", S, None, "Descrição do processo."),
          P("fullName", S, None, "Nome de API; com o objeto na frente no retrieve, sem ele quando aninhado.", "S", herdada="Metadata"),
          P("isActive", B, None, "Indica se o processo está ativo."),
          P("namespacePrefix", S, None, "Namespace da org que criou o pacote."),
          P("values", "PicklistValue[]", None, "Os valores de picklist do processo.", natureza="tipo_composto",
            contexto="Os campos de PicklistValue ficam numa página própria, que devolveu conteúdo ilegível."),
      ], parent="CustomObject", exemplo=CAB + f"""<!-- No arquivo .object do objeto, este conteúdo fica no elemento <businessProcesses> -->
<BusinessProcess {NS}>
    <fullName>[Nome_Do_Processo]</fullName>
    <description>[descrição]</description>
    <isActive>true</isActive>
</BusinessProcess>""", arquivos_prontos=M.arquivos("BusinessProcess", "CustomObject"), curinga=None,
      alertas=["O business process é atribuído a record types, e são os record types que se ligam aos perfis.",
               "A atribuição a perfis controla criar e editar, não ler: quem tem acesso lê tudo o que está no processo.",
               "Não guarde dados sensíveis no nome, na descrição ou nos valores.",
               "Segundo a página, o curinga (*) só funciona no package.xml quando RecordType também é especificado."],
      cobertura_nota="Universo esperado = tabela Fields da página do guia versionado 264.0, lida em 2026-11-17 (5 campos). PicklistValue sem detalhe.")
REG.append((S_BP, "metadata-types", "BusinessProcess"))
M.mdt("FieldSet", S_FS,
      "Um field set: um conjunto de campos de um objeto, em ordem, que páginas Visualforce e componentes podem usar sem citar cada campo.",
      "Versionar e implantar os field sets junto com o objeto.", "21.0", [
          P("availableFields", "FieldSetItem[]", None, "Todos os campos que podem entrar no conjunto.", estrutura="FieldSetItem"),
          P("description", S, None, "Para que serve o field set.", "S"),
          P("displayedFields", "FieldSetItem[]", None, "Campos mostrados; a ordem da lista é a ordem de exibição.", estrutura="FieldSetItem"),
          P("fullName", S, None, "Nome de API do field set; aparece no exemplo XML da página.", "?"),
          P("label", S, None, "Rótulo do field set.", "S"),
      ], parent="CustomObject", exemplo=CAB + f"""<!-- No arquivo .object do objeto, este conteúdo fica no elemento <fieldSets> -->
<FieldSet {NS}>
    <fullName>[Nome_Do_Field_Set]</fullName>
    <description>[para que serve]</description>
    <displayedFields>
        <field>[campo]</field>
        <isFieldManaged>false</isFieldManaged>
        <isRequired>false</isRequired>
    </displayedFields>
    <label>[rótulo]</label>
</FieldSet>""", arquivos_prontos=M.arquivos("FieldSet", "CustomObject"), curinga=True, estende="não declarado na página",
      alertas=["Em pacotes gerenciados, o administrador pode incluir, retirar e reordenar campos do field set sem mexer no código."],
      cobertura_nota="Universo esperado = tabelas Fields da página do guia versionado 264.0, lida em 2026-11-17.")
REG.append((S_FS, "metadata-types", "FieldSet"))
M.mdt("Index", S_IX,
      "Um índice de big object: os campos, em ordem, que formam a chave de consulta do big object.",
      "Versionar e implantar o índice junto com o big object.", "41.0", [
          P("fields", "IndexField[]", None, "Os campos do índice, na ordem da chave.", estrutura="IndexField"),
          P("label", S, "41.0", "Rótulo do índice.", "S"),
          M.FULLNAME_HERDADO(None),
      ], parent="CustomObject", exemplo=CAB + f"""<!-- No arquivo do big object (__b), este conteúdo fica no elemento <indexes> -->
<Index {NS}>
    <fullName>[Nome_Do_Indice]</fullName>
    <fields>
        <name>[campo obrigatório do big object]</name>
        <!-- Valores documentados: ASC, DESC -->
        <sortDirection>DESC</sortDirection>
    </fields>
    <label>[rótulo]</label>
</Index>""", arquivos_prontos=M.arquivos("Index", "CustomObject"), curinga=False,
      alertas=["Todo campo do índice precisa estar também em fields do big object e marcado como obrigatório.",
               "A ordem dos campos na definição é a ordem da chave do índice.",
               "Espaços no começo ou no fim do nome de um campo do índice podem impedir a exclusão de registros consultados por SOQL."],
      cobertura_nota="Universo esperado = tabelas Fields da página do guia versionado 264.0, lida em 2026-11-17.")
REG.append((S_IX, "metadata-types", "Index"))
M.emit_structs()

# ================================================================ ligações nos tipos e estruturas históricos
REGISTRADOS = {f[:-5] for f in os.listdir(caminho("catalogo", "metadata-types"))}


def _estado_estrutura(sid, visto=None):
    visto = visto or set()
    if sid in visto:
        return True
    visto.add(sid)
    p = caminho("catalogo", "estruturas", sid[4:] + ".json")
    if not os.path.exists(p):
        return False
    d = json.load(open(p, encoding="utf-8"))
    if d["cobertura"]["estrutural"]["estado"] != "completa":
        return False
    return all(_estado_estrutura(q["estrutura_ref"], visto) for q in d["propriedades"] if q.get("estrutura_ref"))


def _pendentes(props):
    return sorted(q["nome"] for q in props if q["dominio"]["natureza"] == "tipo_composto" and "estrutura_ref" not in q
                  and q["tipo_tecnico"].replace("[]", "") not in REGISTRADOS)


def ligar(pasta, nome, ligacoes, nota=None, src=None):
    """Liga propriedades a estruturas e recalcula a cobertura estrutural de um tipo ou estrutura já gravado."""
    rel = f"{pasta}/{nome}.json"
    d = ld(rel)
    dono = ("mdt:" if pasta == "metadata-types" else "mdx:") + nome
    for q in d["propriedades"]:
        if q["nome"] in ligacoes:
            sid = "mdx:" + ligacoes[q["nome"]]
            q["estrutura_ref"] = sid
            if src and not any(e.get("fonte") == src for e in q["evidencias"]):
                q["evidencias"].append(ev(src))
            e = ld(f"estruturas/{sid[4:]}.json")
            e["usada_por"] = sorted(set(e["usada_por"]) | {dono})
            sv(f"estruturas/{sid[4:]}.json", e)
    usadas = sorted({q["estrutura_ref"] for q in d["propriedades"] if q.get("estrutura_ref")})
    if pasta == "metadata-types":
        d["estruturas"] = usadas
    est = d["cobertura"]["estrutural"]
    pend = _pendentes(d["propriedades"])
    parciais = [s for s in usadas if not _estado_estrutura(s)]
    base = re.split(r" Primeiro nível completo;| Estruturas usadas ainda parciais:", nota if nota is not None else est["nota"])[0]
    if pend:
        base += f" Primeiro nível completo; {len(pend)} propriedade(s) de tipo composto ainda sem estrutura detalhada: {', '.join(pend)}."
    if parciais:
        base += f" Estruturas usadas ainda parciais: {', '.join(parciais)}."
    completa = est.get("esperado") is not None and est["esperado"] == est["presente"] and not pend and not parciais
    est.update({"estado": "completa" if completa else "parcial", "nota": base})
    sv(rel, d)
    return est["estado"]


# ordem: estruturas internas primeiro, para o estado delas valer no tipo que as usa
ligar("estruturas", "ValueSet", {"valueSettings": "ValueSettings"}, src=S_FT)
ligar("estruturas", "ValueSetValuesDefinition", {"value": "CustomValue"}, src=S_CV)
ligar("estruturas", "RecordTypePicklistValue", {}, nota="Contagem conforme a seção do subtipo na página oficial. PicklistValue: a página própria "
      "(meta_picklistvalue) devolveu conteúdo ilegível em 2026-11-17.")
NOTA_KF = ("Nível principal completo ({} linhas). Os subtipos foram relidos no guia versionado 264.0 em 2026-11-17 e cadastrados como estruturas{}.")
ESTADO = {
    "KnowledgeSettings": ligar("metadata-types", "KnowledgeSettings", {
        "answers": "KnowledgeAnswerSettings", "cases": "KnowledgeCaseSettings", "languages": "KnowledgeLanguageSettings",
        "suggestedArticles": "KnowledgeSuggestedArticlesSettings"}, nota=NOTA_KF.format(23, " (12)"), src=S_K),
    "ForecastingSettings": ligar("metadata-types", "ForecastingSettings", {
        "forecastingCategoryMappings": "ForecastingCategoryMapping", "forecastingDisplayedFamilySettings": "ForecastingDisplayedFamilySettings",
        "forecastingSubmissionSettings": "ForecastingSubmissionSettings", "forecastingTypeSettings": "ForecastingTypeSettings",
        "globalAdjustmentsSettings": "AdjustmentsSettings", "globalForecastRangeSettings": "ForecastRangeSettings", "globalQuotasSettings": "QuotasSettings"},
        nota=NOTA_KF.format(10, " (11). ForecastingGroup e ForecastingGroupItem são descritos na página, mas nenhuma propriedade os usa; "
                                "não foram cadastrados"), src=S_F),
    "Profile": ligar("metadata-types", "Profile", {"userPermissions": "ProfileUserPermission", "ServicePresenceStatusAccesses": "ProfileServicePresenceStatusAccess"},
                     nota="Campos de primeiro nível completos conforme a página 68.0. Em 2026-11-17, a página foi relida a partir de 100.000 caracteres "
                          "até o fim: ProfileUserPermission e ProfileServicePresenceStatusAccess foram cadastrados; LoginFlow, ProfileAgentAccess, "
                          "ProfileActionOverride e ProfileLoginHours não têm seção na página.", src=S_PR),
    "CustomObject": ligar("metadata-types", "CustomObject", {"searchLayouts": "SearchLayouts", "profileSearchLayouts": "ProfileSearchLayouts",
                                                             "historyRetentionPolicy": "HistoryRetentionPolicy"},
                          nota="Tabela Fields lida em 100k de 101,8k caracteres; os ~1,8k finais continham apenas exemplo. Valores de DeploymentStatus, "
                               "SharingModel, Gender e StartsWith estão em outras páginas. Em 2026-11-17: SearchLayouts, ProfileSearchLayouts e "
                               "HistoryRetentionPolicy viraram estruturas; BusinessProcess, FieldSet e Index, metadata types filhos. As páginas de "
                               "ActionOverride, SharingReason, SharingRecalculation e NamedFilter devolveram conteúdo ilegível."),
    "CustomField": ligar("metadata-types", "CustomField", {"picklist": "Picklist", "summaryFilterItems": "FilterItem"}),
    "RecordType": ligar("metadata-types", "RecordType", {}),
}

# ================================================================ #8 Tooling API: chamadas e campos
TF = {  # objeto -> (desde, SOAP, REST, campos [(nome, tipo, props, desde, descrição)], acesso, notas)
    "Profile": ("32.0", ["getDeleted()", "getUpdated()", "query()", "retrieve()", "search()"], ["GET", "HEAD"], [
        ("Description", "string", "FGNS", None, "Descrição do perfil; até 255 caracteres."),
        ("FullName", "string", "CGN", None, "Nome único do perfil, usado antes de haver um Id."),
        ("Metadata", "ProfileMetadata", "CNU", None, "O conteúdo de metadado do perfil."),
        ("Name", "string", "FGIS", None, "Nome do perfil."),
        ("TimeSheetTemplateAssignments", "tns:QueryResult", "N", "46.0", "Modelo de folha de horas atribuído ao perfil; só em subconsultas.")],
        "Desde o Summer '20, usuários de Customer Portal e Partner Portal não acessam. Ver configurações exige View Setup and Configuration.",
        ["FullName e Metadata só podem ser consultados quando o resultado tem no máximo um registro."]),
    "PermissionSet": ("28.0", ["describeSObjects()", "query()", "retrieve()", "search()"], None, [
        ("Description", "string", "FNGS", None, "Descrição; até 255 caracteres."),
        ("HasActivationRequired", "boolean", "DFGS", None, "Se o permission set exige uma sessão ativa."),
        ("IsCustom", "boolean", "DFGS", None, "true se criado por administrador; false se ligado a uma licença."),
        ("IsOwnedByProfile", "boolean", "DFGS", "25.0", "true se pertence a um perfil."),
        ("Label", "string", "FGS", None, "Rótulo; até 80 caracteres."),
        ("ManageableState", "ManageableState", "FGNRS", None, "Estado do componente num pacote, como beta, released ou unmanaged."),
        ("Name", "string", "FGS", None, "Nome do permission set."),
        ("NamespacePrefix", "string", "FGNS", "30.0", "Prefixo de namespace do pacote."),
        ("PermissionSetGroupId", "reference", "FGNS", "45.0", "Grupo dono, ou nulo."),
        ("ProfileId", "reference", "FGNS", None, "Perfil dono, ou nulo."),
        ("Type", "picklist", "DFGNRS", None, "Tipo do permission set.")],
        "Desde o Summer '20, exige View Setup and Configuration, Manage Session Permission Set Activations, Assign Permission Sets ou Manage Profiles and Permission Sets.",
        ["A página não lista métodos REST.", "A descrição de Name na página fala em grupo de permission sets, provável erro de cópia."]),
    "PermissionSetGroup": ("45.0", ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"],
                           ["Query", "GET", "POST", "PATCH", "DELETE"], [
        ("Description", "textarea", "CFGNSU", None, "Descrição do grupo."),
        ("DeveloperName", "string", "CFGSU", None, "Nome de API do grupo; ver exige permissão própria."),
        ("HasActivationRequired", "boolean", "CDFGSU", "53.0", "Se o grupo exige uma sessão ativa."),
        ("Language", "picklist", "CDFGNRSU", None, "Idioma do grupo."),
        ("ManageableState", "ManageableState", "FGNRS", None, "Estado no pacote: beta, deleted, deprecated, installed, released, unmanaged e outros."),
        ("MasterLabel", "string", "CFGSU", None, "Rótulo do grupo."),
        ("NamespacePrefix", "string", "FGNS", None, "Prefixo de namespace."),
        ("Status", "string", "DFGRS", None, "Estado do recálculo: Updated, Outdated, Updating ou Failed.")],
        "Ver exige View Setup and Configuration, Manage Session Permission Set Activations ou Assign Permission Sets; editar exige Manage Profiles and Permission Sets.",
        []),
    "PermissionSetAssignment": ("22.0", ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"],
                                ["DELETE", "GET", "HEAD", "PATCH", "POST", "Query"], [
        ("AssigneeId", "reference", "CFGS", None, "Usuário que recebe o permission set ou o grupo."),
        ("ExpirationDate", "dateTime", "CFNSU", "52.0", "Quando a atribuição deixa de valer."),
        ("IsActive", "boolean", "DFGS", "52.0", "Se a atribuição está em vigor."),
        ("IsRevoked", "boolean", "DFGSU", "57.0", "Se a atribuição foi revogada (beta)."),
        ("LastCreatedByChangeId", "reference", "FGNS", "57.0", "Mudança de acesso que criou a atribuição (beta)."),
        ("LastDeletedByChangeId", "reference", "CFGS", "57.0", "Mudança de acesso da revogação (beta)."),
        ("PermissionSetGroupId", "reference", "CFGNS", "45.0", "Grupo atribuído."),
        ("PermissionSetId", "reference", "CFGNS", None, "Permission set atribuído.")],
        "Desde o Summer '20, exige View Setup and Configuration, Assign Permission Sets ou Manage User.",
        ["IsRevoked, LastCreatedByChangeId e LastDeletedByChangeId estão em beta."]),
    "User": ("32.0", ["describeLayout()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "search()", "update()"], ["GET", "PATCH"], [
        ("FirstName", "string", "CFGNSU", None, "Nome."), ("LastName", "string", "CFGNSU", None, "Sobrenome."),
        ("Name", "string", "FGS", None, "Nome e sobrenome juntos; até 121 caracteres."),
        ("Username", "string", "CFGISU", None, "Nome de usuário na org."),
        ("WorkspaceId", "id", "FGNSU", None, "Id do último workspace aberto no Developer Console.")],
        "Exposto na Tooling API para quem tem ViewSetup.",
        ["Pela Tooling API saem só campos padrão, não os customizados.", "Desde a API 45.0, consultas de usuário guest vão pela SOAP API."]),
    "RecordType": ("32.0", ["create()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "update()", "upsert()"], ["GET", "PATCH", "POST"], [
        ("BusinessProcessId", "id", "CFGNSU", None, "Business process associado."),
        ("Description", "string", "FGNS", None, "Descrição; até 255 caracteres."),
        ("EntityDefinitionId", "string", "FGS", None, "Id da entidade a que o record type pertence."),
        ("FullName", "string", "CGN", None, "Nome do componente correspondente na Metadata API."),
        ("IsActive", "boolean", "DFGSU", None, "Se o record type pode ser usado em registros."),
        ("ManageableState", "ManageableState", "FGNRS", None, "Estado do componente no pacote."),
        ("Metadata", "RecordTypeMetadata", "CNU", None, "O metadado do record type."),
        ("Name", "string", "N", None, "Nome do record type."),
        ("NamespacePrefix", "string", "N", None, "Prefixo de namespace."),
        ("SobjectType", "string", "FGNS", None, "Objeto de que o record type deriva.")],
        None, ["FullName e Metadata só podem ser consultados quando o resultado tem no máximo um registro.",
               "Em sandboxes, ligue o source tracking para os valores de picklist aparecerem em Metadata.picklistValues."]),
}
for objn, (desde, soap, rest, campos, acesso, notas) in TF.items():
    src = f"src:tooling-{objn.lower()}"
    rel = f"objetos-api/{objn}.json"
    d = ld(rel)
    existentes = {c["nome"]: c for c in d["campos"]}
    so_tooling = []
    for nome, tipo, props, ver, desc in campos:
        if nome in existentes:
            c = existentes[nome]
            if "tooling" not in c["apis"]:
                c["apis"].append("tooling")
            if not any(e.get("fonte") == src for e in c["evidencias"]):
                c["evidencias"].append(ev(src))
        else:
            d["campos"].append(O.field(f"obj:{objn}", nome, tipo, props, ver, desc, src, apis=("tooling",)))
            so_tooling.append(nome)
    d["campos"].sort(key=lambda c: c["nome"])
    d["exposicoes"] = [x for x in d["exposicoes"] if x["api"] != "tooling"] + [
        O.expo("tooling", "verificado", src, soap, rest=rest, desde=desde, acesso=acesso,
               nota=" ".join(notas + [f"Campos na página da Tooling API: {len(campos)}; só nela: {', '.join(so_tooling) or 'nenhum'}. "
                                      "As propriedades de campo registradas valem para a API padrão; na Tooling API podem diferir."]))]
    est = d["cobertura"]["estrutural"]
    est["presente"] = len(d["campos"])
    est["nota"] = est["nota"].split(" Tooling API (2026-11-17):")[0] + f" Tooling API (2026-11-17): {len(campos)} campos lidos; {len(so_tooling)} só nela."
    d["cobertura"]["explicativa"]["esperado"] = len(d["campos"])
    d["cobertura"]["explicativa"]["presente"] = O.cnt(d["campos"])
    sv(rel, d)

# ================================================================ nota de extração: lista de campos
ls = ["", "-- Lista de campos transcrita da leitura (gerada por lote7l_b4_estruturas.py; nome | tipo)"]
for src, pasta, nome in REG:
    ls.append(f"[{src}] {nome}: " + ", ".join(f"{q['nome']} | {q['tipo_tecnico']}" for q in ld(f"{pasta}/{nome}.json")["propriedades"]))
for objn, (_, _, _, campos, _, _) in TF.items():
    ls.append(f"[src:tooling-{objn.lower()}] objeto {objn}: " + ", ".join(f"{c[0]} | {c[1]}" for c in campos))
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(ls) + "\n")

C.ampliar_funcionalidade("tipos-de-registro", mdts=[("BusinessProcess", "Os valores de picklist por processo, atribuídos a record types.")], srcs=[S_BP])
C.ampliar_funcionalidade("campos-customizados", mdts=[("FieldSet", "Um conjunto ordenado de campos do objeto, usado por páginas e componentes.")], srcs=[S_FS])
C.ampliar_funcionalidade("objetos-customizados", mdts=[("Index", "O índice de um big object (objeto com sufixo __b), definido dentro do próprio objeto.")],
                         srcs=[S_IX])
print("lote 7l:", ESTADO)
