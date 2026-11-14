"""Issue #34, item 3 (detalhamento dos temas principais): fontes novas e conteúdo que substitui o de temas internos
que estavam rasos (sem nível avançado ou sem fonte própria), um tema principal por vez.

Fontes lidas pelos resultados de busca restritos aos domínios oficiais; uma nota de extração por tema principal
(fontes/extracoes/temas-detalhe-<tema>.txt). Usado por conteudo_temas.py, aplicado por último (prevalece sobre
conteudo_sub.py).
"""
from carga.catalogo import fonte
from conteudo_cls import E, ini, enc, av

AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")
DOC = dict(versao="sem versão na página", metodo="leitura_resultado_busca")

FONTES_DETALHE = []
D = {}

# ====================================================================== Qualidade, governança e ciclo de vida dos dados
_EXT = "fontes/extracoes/temas-detalhe-qualidade.txt"
_DATA = "2026-11-14"


def _f(i, t, u, p, **k):
    FONTES_DETALHE.append(fonte(i, t, u, p, _EXT, _DATA, **k))


_H = "https://help.salesforce.com/s/articleView?id="
_f("src:help-duplicate-management-customize", "Customize Duplicate Management", _H + "sales.duplicate_prevention_map_of_tasks.htm&type=5",
   "Papel das matching rules e das duplicate rules; permissões e edições.", **AJ)
_f("src:help-duplicate-detection-process", "Duplicate Detection and Handling Process", _H + "sf.duplicate_detection_and_handling.htm&type=5",
   "Comparação entre objetos e match keys.", **AJ)
_f("src:help-duplicate-rules-things-to-know", "Things to Know About Duplicate Rules", _H + "sales.duplicate_rules_overview.htm&type=5",
   "Limites de regras ativas, duplicate record sets e global picklists.", **AJ)
_f("src:help-duplicate-rules-customize", "Customize Duplicate Rules", _H + "sales.duplicate_rules_create.htm&type=5",
   "Ações padrão, acesso necessário e ativação.", **AJ)
_f("src:help-duplicate-prevention", "Stop Users from Creating Duplicate Records", _H + "sf.duplicate_prevention.htm&type=5",
   "Regras padrão ativas, person accounts e alerta ou bloqueio.", **AJ)
_f("src:help-matching-rules", "Matching Rules", _H + "sales.matching_rule_map_of_reference.htm&type=5",
   "Matching rules padrão não editáveis.", **AJ)
_f("src:help-matching-rules-considerations", "Things to Know Before You Customize Matching Rules", _H + "sf.matching_rules_considerations.htm&type=5",
   "Limites de matching rules.", **AJ)
_f("src:help-duplicate-jobs-considerations", "Things to Know About Duplicate Jobs", _H + "sf.duplicate_jobs_considerations.htm&type=5",
   "Limites e sobrescrita de duplicate jobs.", **AJ)
_f("src:help-duplicate-rules-classic-view", "Show Duplicate Records in Salesforce Classic", _H + "sf.duplicate_rules_what_my_users_see_classic.htm&type=5",
   "O que o usuário vê; opção Bypass sharing rule.", **AJ)
_f("src:help-duplicate-web-to-lead", "Salesforce Duplicate Matching Rules Blocking Web-to-Lead Submissions (KB)", _H + "000336839&type=1",
   "Web-to-Lead sempre bloqueia o duplicado.", **AJ)
_f("src:help-matching-rule-ineffective", "Unable to Activate Matching Rule to Identify Duplicate Records in a Salesforce Organization (KB)",
   _H + "000383122&type=1", "Matching rule ineficaz não ativa (limiar de 2%).", **AJ)
_f("src:soap-findduplicates", "findDuplicates() (SOAP API Developer Guide)",
   "https://developer.salesforce.com/docs/platform/api/guide/sforce-api-calls-findduplicates.html", "Aplicar duplicate rules pela API; limite de 50 elementos.", **DOC)
_f("src:help-validation-rules", "Validation Rules", _H + "fields_about_field_validation.htm&type=5",
   "Como a validação atua ao salvar; aviso sobre Einstein Prediction Builder.", **AJ)
_f("src:help-validation-considerations", "Validation Rule Considerations", _H + "sf.fields_validation_considerations.htm&type=5",
   "Ordem de processamento das regras.", **AJ)
_f("src:help-validation-tips", "Tips for Writing Validation Rules", _H + "platform.fields_validation_rules_tips.htm&type=5",
   "Boas práticas ao escrever regras de validação.", **AJ)

D["sub:validacao"] = {
    "para_iniciantes": ini("Regras de validação são fórmulas que impedem salvar um registro quando uma condição de erro é verdadeira. Ao "
                           "salvar, todas as regras são verificadas; se alguma acusa erro, a mensagem aparece e nada é gravado.",
                           "Impedir salvar um contrato com valor negativo.",
                           E("src:mdapi-validationrule", "src:help-validation-rules"), comece=["func:regras-de-validacao"]),
    "encadeamento": enc("É a primeira barreira de qualidade: atua no momento de salvar e vem antes das regras de atribuição, de resposta "
                        "automática, de workflow e de escalonamento. Duplicados são tratados em 'Duplicidade e correspondência'.",
                        E("src:mdapi-validationrule", "src:help-validation-considerations")),
    "avancado": [
        av("decisao", "Validação, automação ou segurança",
           "A validação bloqueia a gravação; não esconde o campo nem corrige o valor. Para restringir quem edita, use a segurança de "
           "campo; para preencher ou corrigir valores, use automação.", E("src:mdapi-validationrule", "src:security-fls", "src:mdapi-flow")),
        av("implantacao", "Onde a validação entra na gravação",
           "A ordem de processamento é: validation rules, assignment rules, auto-response rules, workflow rules com ações imediatas e "
           "escalation rules. Quando uma regra de validação falha, as demais continuam sendo verificadas. Record-triggered flows também "
           "executam as regras de validação customizadas.",
           E("src:help-validation-considerations", "src:help-rtf-considerations")),
        av("atencao", "Regra que trava dado válido",
           "Regras conflitantes no mesmo campo impedem salvar o registro; por isso a orientação é testar antes de ativar e acompanhar pelo "
           "debug log. Vale considerar tudo o que pode fazer o registro falhar: assignment rules, field updates, segurança de campo e "
           "campos ocultos. Não se recomenda validar um campo numérico gerenciado pelo Einstein Prediction Builder.",
           E("src:help-validation-tips", "src:help-validation-rules")),
        av("decisao", "Fórmulas mais seguras",
           "Em Opportunity, a orientação é evitar os merge fields IsClosed e IsWon e usar ISPICKVAL sobre o Stage. RecordType.Id permite "
           "aplicar a regra só a um tipo de registro.", E("src:help-validation-tips")),
    ],
}
D["sub:duplicidade-e-correspondencia"] = {
    "para_iniciantes": ini("Duas regras trabalham juntas contra registros repetidos. A matching rule define como reconhecer um duplicado "
                           "(quais campos comparar e com que rigor). A duplicate rule define o que fazer quando ele aparece: avisar, "
                           "bloquear ou só registrar para relatório.",
                           "Ao cadastrar um lead com o mesmo e-mail de um contato existente, a vendedora vê o alerta com o possível "
                           "duplicado antes de salvar.",
                           E("src:help-duplicate-management-customize", "src:help-duplicate-detection-process")),
    "encadeamento": enc("Atua quando um registro é criado ou editado; a validação, em 'Validação', olha o valor de cada campo. Para limpar "
                        "duplicados que já existem, duplicate jobs usam as mesmas matching rules.",
                        E("src:help-duplicate-management-customize", "src:mdapi-validationrule")),
    "avancado": [
        av("decisao", "Avisar, bloquear ou reportar",
           "As duplicate rules padrão vêm ativas para business accounts, contatos e leads; para person accounts, é preciso ativá-las. A "
           "ação padrão na criação é permitir com alerta e reportar. Com a opção Report, o registro e seus duplicados entram num "
           "duplicate record set, até 100 duplicados por matching rule executada.",
           E("src:help-duplicate-prevention", "src:help-duplicate-rules-customize", "src:help-duplicate-rules-things-to-know")),
        av("limite", "Quantas regras",
           "Até cinco duplicate rules ativas por objeto, cada uma com até três matching rules. Matching rules: até cinco ativas por objeto, "
           "25 ativas no total e 100 no total, com um único campo de lookup por regra. As matching rules padrão não podem ser editadas. "
           "Valores de global picklist não são suportados em duplicate rules.",
           E("src:help-duplicate-rules-things-to-know", "src:help-matching-rules-considerations", "src:help-matching-rules")),
        av("seguranca", "O que o usuário enxerga",
           "Para ver os duplicados detectados, o usuário precisa de Read no objeto da regra, e a contagem mostra só os registros a que "
           "ele tem acesso. Com Bypass sharing rule, a comparação inclui todos os registros, e a mensagem só indica que há duplicados.",
           E("src:help-duplicate-rules-customize", "src:help-duplicate-rules-classic-view")),
        av("atencao", "Comportamentos que surpreendem",
           "Em Web-to-Lead, um envio que bate com o critério é sempre bloqueado, mesmo com a regra em permitir com alerta. Uma matching "
           "rule considerada ineficaz não pode ser ativada: o limiar padrão é de 2% de match keys repetidas.",
           E("src:help-duplicate-web-to-lead", "src:help-matching-rule-ineffective")),
        av("escala", "Limpeza em massa e API",
           "Duplicate jobs rodam também em objetos customizados, mas sem comparar e mesclar. Rodar de novo com o mesmo objeto e a mesma "
           "matching rule sobrescreve o resultado anterior, e 1.000.000 de duplicados acumulados bloqueia novos jobs. Pela SOAP API, "
           "findDuplicates() aplica as duplicate rules a até 50 registros por chamada.",
           E("src:help-duplicate-jobs-considerations", "src:soap-findduplicates")),
        av("implantacao", "Como metadado",
           "DuplicateRule e MatchingRules constam da lista oficial de metadata types da versão 68; as propriedades deles ainda não estão "
           "detalhadas neste catálogo.", E("src:sdr-metadata-support")),
    ],
}
D["sub:rastreabilidade-e-historico"] = {
    "para_iniciantes": ini("Guarda o histórico de alterações de campos: quem mudou, o que mudou e quando. O rastreamento é ligado campo a "
                           "campo e só registra a partir do momento em que é ligado.",
                           "Um auditor confere quem alterou o valor de um contrato no mês passado.",
                           E("src:security-guide", "src:help-field-history-tracking")),
    "encadeamento": enc("Cruza com Observabilidade: o Security Guide trata o histórico de campos junto com auditoria e monitoramento. "
                        "Por quanto tempo o histórico fica guardado é assunto de 'Retenção, arquivamento e exclusão'.",
                        E("src:security-guide", "src:help-field-history-tracking")),
    "avancado": [
        av("limite", "O que o histórico guarda",
           "Sem Field Audit Trail, o histórico fica até 18 meses (24 pela API), em até 20 campos por objeto. Ele mora num objeto "
           "relacionado (AccountHistory, MyCustomObject__History) e não conta no armazenamento. Campos de texto longo registram só que "
           "houve mudança, não os valores.", E("src:help-field-history-tracking", "src:help-field-audit-trail")),
        av("implantacao", "Como metadado",
           "O rastreamento é ligado no objeto (enableHistory no CustomObject) e em cada campo (trackHistory no CustomField).",
           E("src:mdapi-customobject", "src:mdapi-customfield")),
        av("decisao", "Quando o padrão não basta",
           "O Field Audit Trail amplia para até 200 campos por objeto e guarda o histórico até ser excluído, no big object "
           "FieldHistoryArchive, acessível só por API.", E("src:help-field-audit-trail")),
    ],
}

# ====================================================================== Relatórios, analytics e exploração
_EXT = "fontes/extracoes/temas-detalhe-relatorios.txt"

_f("src:help-reports-overview", "Reports", _H + "analytics.rd_reports_overview.htm&type=5", "Report builder, edição inline e edições.", **AJ)
_f("src:help-reports-build", "Build a Report", _H + "rd_reports_build.htm", "Lightning Report Builder e formato joined.", **AJ)
_f("src:help-joined-reports-concepts", "How Joined Reports Work", _H + "analytics.reports_joined_format_concepts.htm&type=5",
   "Blocos, relação entre tipos de relatório e agrupamentos.", **AJ)
_f("src:help-joined-summary-formulas", "Summary Formulas with Joined Reports", _H + "reports_csf_joined_reports.htm&type=5",
   "Formatos summary e matrix; summary formulas por bloco.", **AJ)
_f("src:help-report-run-page", "Customize Report Views in the Run Page", _H + "sf.lightning_report_builder_run_page.htm&type=5",
   "Métricas do cabeçalho e chaves do rodapé.", **AJ)
_f("src:help-reports-mobile-differences", "Reports and Dashboards: What's Different or Not Available in the Salesforce Mobile App",
   _H + "limits_mobile_sf1_analytics.htm&type=0", "Diferenças no app móvel e quando cada um é atualizado.", **AJ)
_f("src:help-dashboards-build-lex", "Build a Lightning Experience Dashboard", _H + "dashboards_create_lex.htm",
   "Widgets, source reports, filtros e Lightning table.", **AJ)
_f("src:help-dashboards-view-as", "Configure Dashboard Data Visibility in Lightning Experience", _H + "analytics.dashboards_view_as.htm&type=5",
   "Running user e visibilidade dos dados.", **AJ)
_f("src:help-dynamic-dashboards", "Dynamic Dashboards", _H + "sf.dashboards_dynamic_overview.htm&type=5", "Limites e restrições de dynamic dashboards.", **AJ)
_f("src:help-dynamic-dashboards-create", "Create a Dynamic Dashboard in Lightning Experience", _H + "analytics.dashboards_dynamic_lightning.htm&type=5",
   "Permissão e pastas de um dynamic dashboard.", **AJ)
_f("src:help-dashboard-performance", "Improve Dashboard Performance: Best Practices", _H + "analytics.improving_dashboard_performance.htm&type=5",
   "O que uma atualização dispara e limite por usuário.", **AJ)
_f("src:help-crm-analytics-collections", "Collections of Data in CRM Analytics", _H + "bi_explorer_data_collections.htm&type=5",
   "Datasets, lenses, dashboards e apps.", **AJ)
_f("src:help-crm-analytics-licenses", "Learn about CRM Analytics Platform Licenses and Permission Sets", _H + "bi_help_setup_general.htm&type=5",
   "Licenças por usuário e limite de linhas.", **AJ)
_f("src:help-crm-analytics-enable-kb", "Prerequisites, Licensing Requirements, and Irreversible Effects of Enabling CRM Analytics (KB)",
   _H + "000232305&type=1", "Efeitos de ligar e desligar CRM Analytics.", **AJ)
_f("src:help-crm-analytics-permsets", "Enable CRM Analytics and Create Permission Sets", _H + "bi_setup_enable_create_permset.htm&type=0",
   "Permission sets Manage e View CRM Analytics.", **AJ)
_f("src:help-crm-analytics-tab-studio", "What's the Difference Between Analytics Tab and Analytics Studio?",
   _H + "bi_analytics_tab_studio_difference.htm&type=5", "Caminho de quem usa e de quem cria.", **AJ)
_f("src:help-crm-analytics-experience", "Share CRM Analytics in Experience Cloud Sites", _H + "sf.bi_app_communities.htm&type=5",
   "Licenças externas que podem usar CRM Analytics.", **AJ)

D["sub:reports"] = {
    "para_iniciantes": ini("Um relatório responde uma pergunta sobre os registros da org, como quantas oportunidades estão em cada etapa. "
                           "Ele é montado no report builder, onde se escolhem o tipo de relatório, o formato e os campos, e depois se "
                           "agrupa, filtra e resume.",
                           "Um relatório de oportunidades agrupado por etapa, com a soma do valor de cada grupo.",
                           E("src:help-reports-overview", "src:help-reports-build")),
    "encadeamento": enc("Começa pelo tipo de relatório ('Tipos de relatório'), que define os campos disponíveis. Os cálculos ficam em "
                        "'Métricas e agregações', o relatório alimenta 'Dashboards' e quem o enxerga depende de 'Pastas e acesso'.",
                        E("src:help-reports-overview", "src:help-custom-report-types")),
    "avancado": [
        av("decisao", "Qual formato",
           "Os formatos são tabular, summary (agrupado por linhas), matrix (agrupado por linhas e colunas) e joined. O joined junta até "
           "cinco blocos, com dados de vários tipos de relatório que tenham relação com o mesmo objeto, e aceita até três agrupamentos "
           "comuns aos blocos.", E("src:help-joined-summary-formulas", "src:help-joined-reports-concepts", "src:help-reports-build")),
        av("limite", "O que cabe num relatório",
           "Um tipo de relatório customizado aceita até 60 referências de objeto e 1.000 campos, e o relatório dá erro com colunas de mais "
           "de 20 objetos. Na página de execução, o cabeçalho mostra até 8 métricas.",
           E("src:help-report-limits", "src:help-report-run-page")),
        av("atencao", "No celular é diferente",
           "No app móvel não há joined reports nem criação, edição ou exclusão de relatórios. Um relatório é atualizado cada vez que é "
           "aberto, diferente de um componente de dashboard.", E("src:help-reports-mobile-differences")),
        av("implantacao", "Como metadado",
           "Report, ReportType e ReportFolder constam da lista oficial de metadata types da versão 68; as propriedades deles ainda não "
           "estão detalhadas neste catálogo.", E("src:sdr-metadata-support")),
    ],
}
D["sub:dashboards"] = {
    "para_iniciantes": ini("Um dashboard mostra, em gráficos e tabelas, os resultados de relatórios. Cada peça do painel (widget) tem um "
                           "relatório de origem. O painel mostra os dados da última atualização, não necessariamente os de agora.",
                           "Uma gerente acompanha num painel o funil de oportunidades e os casos abertos por prioridade, cada gráfico "
                           "vindo de um relatório.",
                           E("src:help-dashboards-build-lex", "src:help-reports-mobile-differences")),
    "encadeamento": enc("Vem depois de 'Reports': sem relatório de origem não há widget. Quem pode abrir o painel depende de 'Pastas e "
                        "acesso'; quais dados aparecem depende do running user.",
                        E("src:help-dashboards-build-lex", "src:help-dashboards-view-as")),
    "avancado": [
        av("seguranca", "De quem são os dados do painel",
           "O running user define os dados mostrados. Com Me ou Another person, todos veem conforme o acesso dessa pessoa, mesmo que o "
           "próprio acesso seja menor. Com The dashboard viewer, cada um vê conforme o próprio acesso: é o dynamic dashboard.",
           E("src:help-dashboards-view-as", "src:help-dynamic-dashboards")),
        av("limite", "Dynamic dashboards",
           "Até 5 em Enterprise, 10 em Unlimited e Performance e 3 em Developer; os que estão na lixeira contam até a exclusão "
           "definitiva. Não aceitam atualização agendada, e criar ou editar exige Manage Dynamic Dashboards.",
           E("src:help-dynamic-dashboards", "src:help-dynamic-dashboards-create")),
        av("escala", "Atualização e desempenho",
           "Atualizar roda cada relatório de origem, aplica filtros e redesenha os gráficos. Cada usuário atualiza um painel uma vez por "
           "minuto, e a org pode pedir até 200 atualizações por hora. Em geral, menos relatórios de origem atualizam mais rápido.",
           E("src:help-dashboard-performance", "src:help-report-limits")),
        av("limite", "Tabelas e celular",
           "Uma Lightning table mostra até 200 registros e 10 colunas. No app móvel não dá para criar, editar ou excluir dashboards.",
           E("src:help-dashboards-build-lex", "src:help-reports-mobile-differences")),
        av("implantacao", "Como metadado",
           "Dashboard e DashboardFolder constam da lista oficial de metadata types da versão 68; as propriedades deles ainda não estão "
           "detalhadas neste catálogo.", E("src:sdr-metadata-support")),
    ],
}
D["sub:recursos-analiticos-de-produto"] = {
    "para_iniciantes": ini("São produtos analíticos que vão além dos relatórios nativos e dependem de licença, como CRM Analytics, "
                           "Tableau e Tableau Next. No CRM Analytics, os dados são carregados em datasets, explorados em lenses e "
                           "apresentados em dashboards reunidos em apps.",
                           "Um time de vendas usa um app do CRM Analytics com dashboards prontos sobre o funil, montados a partir de "
                           "um dataset de oportunidades.",
                           E("src:help-produtos-analytics", "src:help-crm-analytics-collections")),
    "encadeamento": enc("Fica ao lado de 'Reports' e 'Dashboards': aqueles são nativos da plataforma; estes exigem licença e "
                        "configuração próprias. O acesso passa por 'Licenças e entitlements de acesso'.",
                        E("src:help-produtos-analytics", "src:help-crm-analytics-licenses")),
    "avancado": [
        av("decisao", "Quem usa e quem cria",
           "Na aba Analytics trabalha quem usa apps e dashboards prontos; no Analytics Studio, quem cria datasets, lenses, dashboards e "
           "apps. Os permission sets típicos são View CRM Analytics e Manage CRM Analytics.",
           E("src:help-crm-analytics-tab-studio", "src:help-crm-analytics-permsets")),
        av("limite", "Licença e volume",
           "CRM Analytics Growth e CRM Analytics Plus são licenças por usuário. A licença limita a instância a 1 bilhão de linhas, e o "
           "limite é contratual, não técnico: cabe à empresa acompanhar.", E("src:help-crm-analytics-licenses")),
        av("atencao", "Ligar e desligar",
           "Ligar CRM Analytics não dá acesso a ninguém: é preciso atribuir licenças e permission sets. Desligar remove as permissões de "
           "CRM Analytics de todos os permission sets e para dataflows e recipes agendados; os assets ficam, mas sem acesso até "
           "reatribuir.", E("src:help-crm-analytics-enable-kb")),
        av("seguranca", "Em sites externos",
           "Em sites Experience Cloud, só usuários com licença Customer Community Plus, Partner Community ou Lightning External Apps "
           "Plus usam CRM Analytics.", E("src:help-crm-analytics-experience")),
        av("implantacao", "Como metadado",
           "WaveDashboard e WaveDataset constam da lista oficial de metadata types da versão 68; não estão detalhados neste catálogo.",
           E("src:sdr-metadata-support")),
    ],
}


# ====================================================================== Organização e configurações base
_EXT = "fontes/extracoes/temas-detalhe-org.txt"

_f("src:help-company-info-fields", "Manage Information About Your Company (Salesforce Help)",
   "https://help.salesforce.com/apex/HTViewHelpDoc?id=company_information_fields.htm",
   "Campos da página Company Information e o que cada um define.", **AJ)
_f("src:help-language-locale-currency", "Language, Locale, and Currency Settings (Salesforce Help)",
   _H + "xcloud.admin_language_locale_currency.htm&language=en_US",
   "Quem define idioma, localidade, fuso e moeda: administrador (padrões da org) e usuário (valores pessoais).", **AJ)
_f("src:help-org-default-timezone", "How to Change Default Time Zones for Users and the Salesforce Organization (Salesforce Help)",
   _H + "000386323&language=en_US&type=1", "O fuso padrão da org vale só para usuários novos.", **AJ)
_f("src:help-org-id", "Find Your Salesforce Organization ID (Salesforce Help)", _H + "000385215&language=en_US&type=1",
   "O que é o Organization ID e a diferença entre produção e sandbox.", **AJ)
_f("src:help-supported-languages", "Supported Languages (Salesforce Help)", _H + "xcloud.faq_getstart_what_languages_does.htm&language=en_US&type=5",
   "Os três níveis de suporte a idioma e onde cada um é gerido no Setup.", **AJ)
_f("src:help-select-languages", "Select Languages for Your Org (Salesforce Help)", _H + "sf.admin_select_languages_for_your_org.htm&language=en_US&type=5",
   "Como ligar idiomas end-user e platform-only e as permissões exigidas.", **AJ)
_f("src:help-locales-overview", "Locales Overview (Salesforce Help)", _H + "sf.admin_locales_overview.htm&language=en_US&type=5",
   "O que a localidade controla e a adoção dos formatos ICU.", **AJ)
_f("src:help-icu-considerations", "Considerations for Adopting the ICU Locale Formats (Salesforce Help)",
   _H + "xcloud.admin_locales_changes_considerations.htm&language=en_US&type=5", "Efeitos de passar dos formatos JDK para ICU.", **AJ)
_f("src:help-translation-workbench", "Translation Workbench (Salesforce Help)", _H + "platform.workbench.htm&language=en_US&type=5",
   "O que o Translation Workbench mantém e em que edições e interfaces.", **AJ)
_f("src:help-translations-manage", "Manage Your Translations (Salesforce Help)", _H + "sf.workbench_overview.htm&language=en_US&type=5",
   "Objetos padrão ficam fora do Translation Workbench.", **AJ)
_f("src:help-translation-languages-add", "Add Translation Languages and Translators (Salesforce Help)",
   _H + "platform.ls_add_translation_language_and_translators.htm&language=en_US&type=5",
   "Caminho no Setup, pré-requisitos e ativação de idiomas de tradução.", **AJ)
_f("src:help-translation-override-packages", "Override Translations in Second-Generation Managed Packages and Unlocked Packages (Salesforce Help)",
   _H + "entering_translated_terms_in_packages.htm&language=en_US&type=5", "Traduções vindas de pacotes e o que pode ser sobrescrito.", **AJ)
_f("src:help-custom-labels", "Custom Labels (Salesforce Help)", _H + "sf.cl_about.htm&language=en_US&type=5",
   "O que são custom labels, limites e permissões.", **AJ)
_f("src:help-custom-labels-edit", "Create and Edit Custom Labels (Salesforce Help)", _H + "sf.cl_edit.htm&language=en_US&type=5",
   "Caminho no Setup e campos de um custom label.", **AJ)
_f("src:help-multicurrency-manage", "Manage Multiple Currencies (Salesforce Help)", _H + "sales.admin_currency.htm&language=en_US&type=5",
   "Passos e caminho no Setup para moeda corporativa, moedas ativas e taxas.", **AJ)
_f("src:help-multicurrency-considerations", "Considerations for Enabling Multiple Currencies (Salesforce Help)",
   _H + "sales.admin_enable_multicurrency_implications.htm&language=en_US&type=5", "Efeitos de ligar múltiplas moedas.", **AJ)
_f("src:help-conversion-rates", "Edit Conversion Rates (Salesforce Help)", _H + "xcloud.editing_conversion_rates.htm&language=en_US&type=5",
   "Como as taxas de conversão são editadas e aplicadas.", **AJ)
_f("src:help-advanced-currency", "About Advanced Currency Management (Salesforce Help)",
   _H + "administration_about_advanced_currency_management.htm&language=en_US", "Taxas de câmbio por data (dated exchange rates).", **AJ)
_f("src:help-advanced-currency-enable", "Enable or Disable Advanced Currency Management (Salesforce Help)",
   "https://help.salesforce.com/apex/HTViewHelpDoc?id=sf.administration_enable_advanced_currency_management.htm&language=en_US",
   "Pré-requisito e efeito de ligar o advanced currency management.", **AJ)
_f("src:help-fiscal-year-set", "Set the Fiscal Year (Salesforce Help)", _H + "sf.setting_the_fiscal_year.htm&language=en_US",
   "Caminho no Setup e efeitos de mudar o ano fiscal.", **AJ)
_f("src:help-fiscal-year-define", "Define Your Fiscal Year (Salesforce Help)", _H + "sf.admin_about_cfy.htm&language=en_US&type=5",
   "Diferença entre ano fiscal padrão e customizado.", **AJ)
_f("src:help-custom-fiscal-year", "Define or Modify a Custom Fiscal Year (Salesforce Help)", "https://help.salesforce.com/apex/HTViewHelpDoc?id=admin_define_cfy.htm",
   "Efeitos do primeiro ano fiscal customizado sobre cotas e ajustes.", **AJ)
_f("src:help-holidays", "Set Up Support Holidays (Salesforce Help)", _H + "sf.customizesupport_holidays.htm&language=en_US&type=5",
   "Caminho no Setup, permissão e efeito dos feriados.", **AJ)
_f("src:help-holidays-guidelines", "Guidelines for Creating Support Holidays (Salesforce Help)",
   _H + "sf.customizesupport_holidays_guidelines.htm&language=en_US&type=5", "Limites e regras dos feriados.", **AJ)
_f("src:help-bh-guidelines", "Guidelines for Setting Business Hours (Salesforce Help)", _H + "sf.customize_supporthours_guidelines.htm&language=en_US&type=5",
   "Como casos e regras de escalonamento usam o horário comercial.", **AJ)
_f("src:help-mydomain-rename", "Change Your My Domain Details (Salesforce Help)", _H + "domain_name_rename.htm&language=en_US&type=0",
   "Caminho no Setup e permissões para mudar o My Domain.", **AJ)
_f("src:help-mydomain-provisioning", "My Domain Provisioning and Deployment (Salesforce Help)", _H + "sf.domain_name_setup.htm&language=en_US&type=5",
   "Os três passos de uma mudança de My Domain.", **AJ)
_f("src:help-domains-view", "View Your Custom Domain Details (Salesforce Help)", _H + "platform.domain_mgmt_view.htm&language=en_US&type=5",
   "Custom domains e system-managed domains na tela Domains.", **AJ)
_f("src:help-cmdt-about", "What are Custom Metadata Types? (Salesforce Help)", _H + "sf.custommetadatatypes_about.htm&language=en_US&type=5",
   "O que são custom metadata types e como os registros migram.", **AJ)
_f("src:help-cmdt-create", "Add or Edit a Custom Metadata Type Declaratively (Salesforce Help)", _H + "custommetadatatypes_ui_create.htm&language=en_US&type=5",
   "Caminho no Setup e regras de nome de custom metadata types.", **AJ)

D["sub:identificacao-e-configuracao-da-org"] = {
    "para_iniciantes": ini(
        "É a ficha cadastral da org. A página Company Information, no Setup, reúne os dados da empresa, os padrões de idioma, localidade "
        "e fuso, a moeda e as licenças compradas. Cada org também tem um Organization ID, o identificador pedido pelo suporte.",
        "A administradora troca o fuso padrão da org; quem for cadastrado depois já recebe o fuso novo.",
        E("src:help-company-info-fields", "src:help-setup-company", "src:help-org-id"), comece=["func:informacoes-da-empresa"]),
    "encadeamento": enc(
        "É o ponto de partida do tema. Os padrões definidos aqui são detalhados em 'Localização, idiomas e tradução' e em 'Moedas e "
        "calendário fiscal'. O administrador define o padrão da org; cada usuário pode trocar idioma, localidade e fuso nas "
        "configurações pessoais.", E("src:help-language-locale-currency")),
    "avancado": [
        av("atencao", "O padrão da org não muda quem já existe",
           "Default Language e Default Time Zone valem para usuários novos. Quem já está cadastrado mantém o idioma e o fuso que tinha, "
           "até trocar nas configurações pessoais.", E("src:help-language-locale-currency", "src:help-org-default-timezone")),
        av("decisao", "Moeda única ou múltiplas moedas muda a página",
           "Em org de moeda única, o administrador define Currency Locale, que dá o formato dos valores em moeda. Em org com múltiplas "
           "moedas, o campo é Corporate Currency: a moeda em que a matriz reporta e a base de todas as taxas de conversão.",
           E("src:help-company-info-fields", "src:help-language-locale-currency")),
        av("atencao", "Sandbox tem outro Organization ID",
           "O Organization ID de produção é diferente do de um sandbox, e cada refresh de sandbox gera um ID novo. O que depender do ID "
           "precisa considerar isso.", E("src:help-org-id")),
        av("implantacao", "O que existe como metadado",
           "CompanySettings é o metadata type das configurações gerais da empresa; na versão lida, os campos dele tratam do ano fiscal. "
           "Para os demais dados da página Company Information, este catálogo ainda não confirmou um metadata type.",
           E("src:mdapi-companysettings")),
    ],
}
D["sub:settings"] = {
    "para_iniciantes": ini(
        "Settings é uma família de metadata types com nomes terminados em Settings. Cada um guarda um grupo de configurações da org e "
        "vira um arquivo .settings na pasta settings.",
        "CurrencySettings guarda a configuração de moedas no arquivo Currency.settings; LanguageSettings guarda a de idiomas em "
        "Language.settings.", E("src:mdapi-settings", "src:mdapi-currencysettings", "src:mdapi-languagesettings")),
    "encadeamento": enc(
        "É o lado 'como código' do tema. Ano fiscal (CompanySettings), moedas (CurrencySettings), idiomas (LanguageSettings), My Domain "
        "(MyDomainSettings) e horários comerciais (BusinessHoursSettings) têm um Settings cada, estudado na seção do assunto. O efeito "
        "de ligar cada recurso fica em 'Habilitação de recursos'.",
        E("src:mdapi-companysettings", "src:mdapi-currencysettings", "src:mdapi-languagesettings", "src:mdapi-mydomainsettings",
          "src:mdapi-businesshourssettings")),
    "avancado": [
        av("implantacao", "Um nome só no package.xml",
           "No package.xml, todos os tipos da família são pedidos pelo nome Settings. O curinga * não vale para um setting individual: "
           "só serve para recuperar todos de uma vez.", E("src:mdapi-settings", "src:mdapi-companysettings")),
        av("atencao", "Nem todo campo pode ser implantado",
           "Alguns campos são somente leitura, como myDomainName e myDomainSuffix em MyDomainSettings. Outros ligam algo sem volta: "
           "implantar enableMultiCurrency como true liga múltiplas moedas, e implantar false numa org que já as tem devolve erro.",
           E("src:mdapi-mydomainsettings", "src:mdapi-currencysettings")),
        av("atencao", "O padrão depende de quando a org foi criada",
           "Alguns defaults mudam conforme a idade da org. enableICULocaleDateFormat nasce true em orgs criadas na API 47.0 ou depois, e "
           "isFirstPartyCookieUseRequired nasce true em orgs criadas a partir do Summer '24. Dois ambientes podem recuperar valores "
           "diferentes sem que ninguém tenha mexido.", E("src:mdapi-languagesettings", "src:mdapi-mydomainsettings")),
        av("implantacao", "Confira o suporte de cada Settings",
           "Cada Settings é um metadata type próprio, com suporte registrado na lista do Salesforce CLI. Confira esse suporte antes de "
           "incluir um Settings num pipeline de implantação.", E("src:sdr-metadata-support")),
    ],
}
D["sub:parametros-reutilizaveis"] = {
    "para_iniciantes": ini(
        "Guarda valores de configuração lidos por várias funcionalidades, como tabelas de regras ou mapeamentos. Há dois mecanismos: "
        "custom metadata types, cujos registros são metadados, e custom settings, cujos registros são dados.",
        "Uma tabela de faixas de desconto fica num custom metadata type e é lida por um flow e por uma regra de validação.",
        E("src:help-custom-settings", "src:help-cmdt-about"), comece=["func:custom-metadata-types"]),
    "encadeamento": enc(
        "É configuração reaproveitada pela org inteira. Textos reaproveitados e traduzíveis são custom labels, em 'Localização, idiomas "
        "e tradução'. O lado 'como código' das configurações gerais fica em 'Settings'.",
        E("src:help-custom-settings", "src:help-custom-labels")),
    "avancado": [
        av("decisao", "Custom metadata em vez de custom settings",
           "A Salesforce recomenda custom metadata types: os registros podem ser migrados por pacotes de segunda geração ou Metadata API, "
           "ao contrário dos de list custom settings. Custom settings do tipo Hierarchy personalizam por perfil ou usuário.",
           E("src:help-custom-settings")),
        av("atencao", "Cache e bloqueios",
           "Registros de custom metadata ficam em cache por tipo depois da primeira leitura; durante o deploy, os registros incluídos "
           "ficam bloqueados e podem causar row lock. Para alterá-los pelo Apex, use o pacote Metadata.", E("src:help-cmdt-limitations")),
        av("seguranca", "Registro protegido",
           "O campo protected marca o registro como protegido. Em pacote gerenciado, isso limita que código pode ler ou alterar o "
           "registro.", E("src:mdapi-custommetadata-tipo")),
        av("implantacao", "Registro como arquivo",
           "Cada registro é um componente CustomMetadata, com sufixo .md na pasta customMetadata. O nome começa com o nome do tipo, sem "
           "__mdt, e os valores vão em pares field e value.", E("src:mdapi-custommetadata", "src:mdapi-custommetadata-tipo")),
    ],
}
D["sub:localizacao-idiomas-e-traducao"] = {
    "para_iniciantes": ini(
        "São três coisas diferentes. Idioma: em que língua a interface aparece. Localidade (locale): como datas, horas, números, nomes e "
        "endereços são formatados. Tradução: o texto dos rótulos customizados em cada idioma. A org define os padrões, e cada usuário "
        "escolhe o próprio idioma e a própria localidade.",
        "Duas pessoas abrem o mesmo registro: uma vê a interface em português e as datas no formato do Brasil; a outra, em inglês e no "
        "formato dos Estados Unidos. O dado guardado é o mesmo.",
        E("src:help-language-locale-currency", "src:help-locales-overview", "src:help-translation-workbench"),
        comece=["func:idiomas-da-org", "func:translation-workbench", "func:custom-labels"]),
    "encadeamento": enc(
        "Os padrões vêm de 'Identificação e configuração da org'. Primeiro escolhem-se os idiomas que a org oferece. Depois, com o "
        "Translation Workbench, traduzem-se os rótulos customizados. Custom labels cobrem os textos usados por código e por páginas. "
        "Moeda e formato de moeda ficam em 'Moedas e calendário fiscal'.",
        E("src:help-select-languages", "src:help-translation-languages-add", "src:help-custom-labels")),
    "avancado": [
        av("decisao", "Três níveis de idioma",
           "Fully supported: recursos e interface no idioma, como Portuguese (Brazil). End-user: a Salesforce traduz rótulos de objetos e "
           "páginas padrão, menos Setup e Help, como Portuguese (European); não deve ser usado como idioma corporativo. Platform-only: "
           "sem tradução padrão, serve para localizar apps e customizações.", E("src:help-supported-languages")),
        av("atencao", "Formato ICU muda o que o usuário lê",
           "A localidade segue os formatos ICU desde o Winter '20; orgs mais antigas usam por padrão os formatos JDK. Migrar pode mudar a "
           "ordem de dia e mês em algumas localidades e causar má leitura de dados. A Ajuda recomenda avisar usuários e parceiros.",
           E("src:help-locales-overview", "src:help-icu-considerations")),
        av("limite", "O que o Translation Workbench não cobre",
           "Objetos padrão ficam fora: para eles, usa-se a tela de renomear abas e rótulos. O Translation Workbench não está disponível "
           "em orgs de idioma único, e a tradução de dados só existe em Lightning Experience, aplicada a B2B Commerce.",
           E("src:help-translations-manage", "src:help-translation-languages-add", "src:help-translation-workbench")),
        av("atencao", "Ative o idioma só no fim",
           "Marcar um idioma como Active mostra as traduções aos usuários; a recomendação é ativar depois de traduzir tudo. Traduções "
           "trazidas por pacote gerenciado aparecem mesmo com o idioma inativo.",
           E("src:help-translation-languages-add", "src:help-translation-override-packages")),
        av("limite", "Custom labels",
           "Até 5.000 custom labels por org, com até 1.000 caracteres cada; os de pacotes gerenciados não contam. Não dá para trocar o "
           "idioma de um label que já existe.", E("src:help-custom-labels", "src:help-custom-labels-edit")),
        av("implantacao", "Como metadado",
           "LanguageSettings guarda a seleção de idiomas e a ativação do Translation Workbench. CustomLabels guarda os textos. As "
           "traduções viajam pelo tipo Translations, em arquivos nomeados pelo código de localidade; esse tipo ainda não está "
           "cadastrado neste catálogo.", E("src:mdapi-languagesettings", "src:mdapi-customlabels", "src:mdapi-translations")),
    ],
}
D["sub:moedas-e-calendario-fiscal"] = {
    "para_iniciantes": ini(
        "Define em que moedas a org registra valores e como o ano fiscal é contado. Por padrão, a org trabalha com uma moeda só; ela "
        "pode ligar múltiplas moedas, com uma moeda corporativa e uma taxa de conversão para cada moeda ativa. O ano fiscal pode ser "
        "padrão (calendário gregoriano, com o mês de início à escolha) ou customizado.",
        "Uma empresa com exercício de abril a março escolhe o ano fiscal padrão começando em abril. A filial do Chile registra valores "
        "em pesos, convertidos para a moeda da matriz pela taxa cadastrada.",
        E("src:help-multicurrency-manage", "src:help-fiscal-year-define", "src:mdapi-currencysettings"),
        comece=["func:multiplas-moedas", "func:ano-fiscal"]),
    "encadeamento": enc(
        "A moeda padrão aparece em 'Identificação e configuração da org' (Currency Locale ou Corporate Currency). As duas decisões "
        "daqui mexem com vendas: oportunidades usam as taxas de conversão, e previsões usam os períodos fiscais. As previsões em si "
        "ficam em 'Vendas'.", E("src:help-company-info-fields", "src:help-advanced-currency", "src:help-fiscal-year-set")),
    "avancado": [
        av("atencao", "Múltiplas moedas não têm volta",
           "Depois de ligar, não dá para desligar. Os registros existentes recebem um código de moeda padrão, e filtros campo a campo em "
           "relatórios deixam de aceitar campos de moeda.", E("src:help-multicurrency-considerations")),
        av("decisao", "Taxa única ou taxa por data",
           "Por padrão, toda conversão usa a taxa atual, e as taxas anteriores não são guardadas. Com advanced currency management, as "
           "taxas valem por intervalo de datas (dated exchange rates), e a oportunidade usa a taxa da data de fechamento. Ao ligar, as "
           "taxas existentes viram o primeiro conjunto datado.",
           E("src:help-conversion-rates", "src:help-advanced-currency", "src:help-advanced-currency-enable")),
        av("atencao", "Mudar o ano fiscal apaga cotas",
           "Mudar o mês de início do ano fiscal apaga cotas (quotas) e ajustes de previsão, e desloca os períodos de oportunidades e "
           "previsões da org inteira. A Ajuda manda exportar um backup antes.", E("src:help-fiscal-year-set")),
        av("atencao", "Ano fiscal customizado não tem volta",
           "Depois de ligado, o ano fiscal customizado não pode ser desligado, e anos customizados não podem ser excluídos. Em org que "
           "usa forecasting, criar o primeiro apaga cotas e ajustes do ano padrão correspondente e dos seguintes.",
           E("src:help-fiscal-year-define", "src:help-custom-fiscal-year")),
        av("implantacao", "Como metadado",
           "CurrencySettings leva a ativação de múltiplas moedas, a moeda corporativa e as moedas com suas taxas. CompanySettings leva o "
           "ano fiscal padrão no campo fiscalYear. Os mesmos avisos da tela valem para o deploy.",
           E("src:mdapi-currencysettings", "src:mdapi-companysettings")),
    ],
}
D["sub:horarios-comerciais-e-feriados"] = {
    "para_iniciantes": ini(
        "Define os dias, horários e fuso em que o atendimento funciona, e os feriados em que esse horário não vale.",
        "Suporte de São Paulo: segunda a sexta, das 8h às 18h, no fuso de Brasília. No feriado de Ano Novo, os prazos param de contar.",
        E("src:help-bh", "src:help-holidays", "src:objref-businesshours"), comece=["func:horario-comercial", "func:feriados"]),
    "encadeamento": enc(
        "Outras regras usam esses horários para contar prazos, como o escalonamento de casos e os marcos de SLA, no tema Atendimento. Um "
        "feriado só vale para os horários comerciais a que foi associado.", E("src:help-bh", "src:help-ent-bh", "src:help-holidays")),
    "avancado": [
        av("atencao", "Horário comercial em cascata",
           "Nos processos de SLA, o horário do milestone prevalece sobre o do processo, que prevalece sobre o do caso.", E("src:help-ent-bh")),
        av("atencao", "O caso herda o horário padrão",
           "O caso recebe o horário comercial padrão da org, a não ser que case com uma regra de escalonamento ligada a outro horário. "
           "Regras de escalonamento só rodam dentro do horário a que estão associadas, e um horário usado em regra não pode ser "
           "desativado.", E("src:help-bh-guidelines")),
        av("limite", "Feriados",
           "Cada horário comercial aceita até 1.000 feriados. O feriado assume o fuso do horário a que foi associado, e só horários "
           "ativos podem ser associados.", E("src:help-holidays-guidelines")),
        av("implantacao", "Como metadado",
           "BusinessHoursSettings leva horários comerciais e feriados no mesmo arquivo, nas listas businessHours e holidays.",
           E("src:mdapi-businesshourssettings")),
    ],
}
D["sub:dominios-e-urls"] = {
    "para_iniciantes": ini(
        "O My Domain é o nome da org nas URLs de login e de aplicação, como mycompany.my.salesforce.com e mycompany.my.site.com.",
        "Os usuários da empresa entram por https://mycompany.my.salesforce.com, e o portal de clientes usa mycompany.my.site.com.",
        E("src:help-mydomain"), comece=["func:my-domain"]),
    "encadeamento": enc(
        "Afeta login, SSO e integrações. Além do My Domain, que a Salesforce gerencia, a org pode ter custom domains para os sites. Os "
        "endereços externos que a org chama ficam em 'Chamadas externas e endpoints'.",
        E("src:help-mydomain-changes", "src:help-domains-view")),
    "avancado": [
        av("atencao", "Mudar o My Domain quebra o que está fixo",
           "Mudar o nome ou o sufixo muda a URL de login: SSO e MFA podem parar de funcionar, e named credentials e templates com a URL "
           "antiga precisam ser atualizados.", E("src:help-mydomain-changes")),
        av("implantacao", "A mudança tem três passos",
           "Salvar a mudança, provisionar os novos domínios e implantá-los. Na implantação mudam juntas a URL de login e as URLs de "
           "aplicação, como as de Visualforce, conteúdo e Experience Cloud. A Ajuda recomenda testar antes em sandbox.",
           E("src:help-mydomain-provisioning", "src:help-mydomain-rename")),
        av("decisao", "Integração com URL devolvida pelo login",
           "Integrações de API devem usar o serverURL devolvido pelo login, não uma URL fixa. Dá para exigir que logins SOAP usem o My "
           "Domain, e tráfego de API com URL de instância incorreta é bloqueado depois do Summer '26.",
           E("src:help-mydomain-changes", "src:help-mydomain-login-policy")),
        av("seguranca", "Exigir o login pelo My Domain",
           "Em MyDomainSettings, canOnlyLoginWithMyDomainUrl obriga os usuários a entrar pela URL do My Domain, e "
           "doesApiLoginRequireOrgDomain faz o mesmo para o acesso por API.", E("src:mdapi-mydomainsettings")),
        av("implantacao", "Como metadado",
           "MyDomainSettings leva políticas de login, redirecionamentos de URLs antigas e opções de cookies. O nome e o sufixo do My "
           "Domain aparecem como campos somente leitura: a troca do nome não é feita por esse tipo.", E("src:mdapi-mydomainsettings")),
    ],
}


# ====================================================================== Processos de negócio específicos de produto
# Só fontes: o conteúdo destes temas internos é editado no lugar (conteudo_sub.py e conteudo_pendentes4.py).
_EXT = "fontes/extracoes/temas-detalhe-processos.txt"

_f("src:help-lead-settings", "Define Default Settings for Lead Creation (Salesforce Help)", _H + "sales.customize_leadsettings.htm&language=en_US&type=5",
   "Caminho no Setup e opções padrão de leads e de conversão.", **AJ)
_f("src:help-lead-convert-considerations", "Considerations for Converting Leads (Salesforce Help)", _H + "sales.leads_notes.htm&language=en_US&type=5",
   "Efeitos da conversão de leads sobre campos, validação e visibilidade.", **AJ)
_f("src:help-contracts-setup", "Set Up Contracts (Salesforce Help)", _H + "sf.customize_contract.htm&language=en_US&type=5",
   "Caminho no Setup e opções de contratos.", **AJ)
_f("src:help-contracts-things", "Things to Know About Contracts (Salesforce Help)",
   "https://help.salesforce.com/apex/HTViewHelpDoc?id=sf.contract_supplemental.htm&language=en_us", "Datas e prazo de um contrato.", **AJ)
_f("src:help-product-schedules", "Product Schedules (Salesforce Help)", _H + "sales.products_schedules_def.htm&language=en_US&type=5",
   "O que são quantity schedules, revenue schedules e default schedules.", **AJ)
_f("src:help-product-schedules-enable", "Enable Product Schedules in Salesforce Classic (Salesforce Help)", _H + "sales.enabling_schedules.htm&language=en_US&type=5",
   "Efeito de ligar e desligar schedules de produto.", **AJ)
_f("src:help-product-schedules-considerations", "Considerations for Using Product Schedules (Salesforce Help)",
   _H + "sales.products_considerations_for_using_schedules.htm&language=en_US&type=5", "Limites de automação e de Apex com schedules.", **AJ)
_f("src:help-orders-enable", "Enable Orders (Salesforce Help)", _H + "sf.customize_order_enable.htm&language=en_US&type=5",
   "Caminho no Setup para ligar pedidos e suas variações.", **AJ)
_f("src:help-orders-manage", "Manage Your Orders (Salesforce Help)", _H + "sales.order_manage_your_orders.htm&language=en_US",
   "Order products, reduction orders e histórico de pedidos.", **AJ)
_f("src:help-orders-reduce", "Reduce Orders (Salesforce Help)", _H + "order_reduce.htm&language=en_US&type=5", "Limites das reduction orders.", **AJ)
_f("src:help-orders-activation", "Considerations for Activation Limitations (Salesforce Help)", _H + "order_activate.htm&language=en_US&type=5",
   "Regras de ativação de pedidos e relação com contratos.", **AJ)
_f("src:help-orders-high-scale", "Enable High Scale Orders for B2B Stores (Salesforce Help)", _H + "sf.comm_high_scale_order_enable.htm&language=en_US&type=5",
   "Enhanced Commerce Orders em lojas B2B.", **AJ)
_f("src:help-revenue-vs-cpq", "Key Differences Between Revenue Management and Salesforce CPQ (Salesforce Help)",
   _H + "ind.rev_migration_revenue_differences_from_cpq.htm&language=en_US&type=5", "Diferenças de arquitetura e de modelo entre Revenue Management e CPQ.", **AJ)
_f("src:help-billing-overview", "Salesforce Billing Overview (Salesforce Help)", _H + "sales.blng_overview.htm&language=en_US&type=5",
   "Como o Salesforce Billing se apoia no Salesforce CPQ.", **AJ)
_f("src:help-revenue-migrate", "Migrate to Revenue Cloud (Salesforce Help)", _H + "ind.rev_data_migration.htm&language=en_US&type=5",
   "O que muda ao sair de CPQ e Billing para o Revenue Cloud.", **AJ)
_f("src:help-revenue-get-started", "Get Started with Revenue Management (Salesforce Help)",
   _H + "sf.revenue_lifecycle_management_get_started.htm&language=en_US&type=5", "Nome atual do produto e como saber qual produto de receita a org usa.", **AJ)
_f("src:help-field-service-enable", "Enable Field Service (Salesforce Help)", _H + "fs_enable.htm&language=en_US&type=5",
   "Caminho no Setup e efeitos de ligar o Field Service.", **AJ)
_f("src:help-field-service-setup-basics", "Set Up Field Service Basics (Salesforce Help)", _H + "service.fs_set_up.htm&language=en_US&type=5",
   "Ordem de configuração do Field Service e o que o managed package acrescenta.", **AJ)
_f("src:help-digital-experiences-enable", "Enable Digital Experiences (Salesforce Help)", _H + "experience.networks_enable.htm&language=en_US&type=5",
   "Caminho no Setup, domínio dos sites e irreversibilidade da ativação.", **AJ)
_f("src:help-experience-org-setup", "Set Up and Configure Your Org for Experience Cloud Sites (Salesforce Help)",
   _H + "experience.networks_setup_maintain_communities.htm&language=en_US&type=5", "Preparação da org antes do primeiro site.", **AJ)
