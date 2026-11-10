"""Issue #34: temas internos que estavam pendentes por falta de fonte (lote 2: Qualidade e Relatórios).
Fontes lidas pelos resultados de busca restritos aos domínios oficiais: fontes/extracoes/temas-pendentes-lote2.txt.
Usado por conteudo_temas.py.
"""
from carga.catalogo import fonte
from conteudo_cls import E, ini, enc, av

DATA = "2026-11-10"
EXT = "fontes/extracoes/temas-pendentes-lote2.txt"
AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")
DOC = dict(versao="sem versão na página", metodo="leitura_resultado_busca")


def F(i, t, u, p, **k):
    return fonte(i, t, u, p, EXT, DATA, **k)


FONTES_PENDENTES2 = [
    # Classificação e sensibilidade
    F("src:help-data-classification-intro", "Classify Sensitive Data to Support Data Management Policies",
      "https://help.salesforce.com/s/articleView?id=platform.data_classification_intro.htm&type=5", "Para que serve a classificação de dados e permissões.", **AJ),
    F("src:help-data-classification-fields", "Data Classification Metadata Fields",
      "https://help.salesforce.com/s/articleView?id=platform.data_classification_metadata_fields.htm&type=5", "Os quatro campos de classificação, valores padrão e correspondência na API.", **AJ),
    F("src:help-data-classification-setup", "Set Up Data Classification Metadata",
      "https://help.salesforce.com/s/articleView?id=sf.data_classification_set_up.htm", "Configuração, níveis de alto risco, upload e download em CSV.", **AJ),
    # Retenção, arquivamento e exclusão
    F("src:help-recycle-bin-lex", "Manage the Recycle Bin in Lightning Experience",
      "https://help.salesforce.com/s/articleView?id=xcloud.recycle_bin_manage.htm&type=5", "Prazo da Recycle Bin, armazenamento e permissões.", **AJ),
    F("src:help-delete-unwanted-data", "Delete Unwanted Data in a Salesforce Organization (KB)",
      "https://help.salesforce.com/s/articleView?id=000387294&type=1", "Soft delete, hard delete e physical delete.", **AJ),
    F("src:help-field-history-tracking", "Field History Tracking Overview",
      "https://help.salesforce.com/s/articleView?id=tracking_field_history.htm&type=0", "Retenção do histórico de campos e onde ele fica.", **AJ),
    F("src:help-field-audit-trail", "Field Audit Trail (KB)",
      "https://help.salesforce.com/s/articleView?id=000383595&type=1", "Comparação com Field History Tracking e política de retenção.", **AJ),
    F("src:mdapi-historyretentionpolicy", "HistoryRetentionPolicy (Metadata API)",
      "https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_historyretentionpolicy.htm",
      "Política de arquivamento do histórico de campos, em meses.", **DOC),
    # Consentimento e privacidade
    F("src:help-consent-data-model", "Understand the Salesforce Consent Data Model",
      "https://help.salesforce.com/s/articleView?id=sf.consent_data_model_mc_about.htm&type=5", "Os quatro níveis do modelo de consentimento.", **AJ),
    F("src:help-consent-objects", "Consent Management Objects",
      "https://help.salesforce.com/s/articleView?id=sf.consent_mgmt_fields.htm&type=5", "Objetos de consentimento e papel do Individual.", **AJ),
    F("src:help-contact-point-type-consent-fields", "Fields in Contact Point Type Consent Records",
      "https://help.salesforce.com/s/articleView?id=sf.contact_point_type_fields.htm", "Campos do consentimento por tipo de contato.", **AJ),
    F("src:rest-consent-write", "Consent Write (REST API Developer Guide)",
      "https://developer.salesforce.com/docs/platform/api-rest/guide/resources-consent-write.html", "Gravação de consentimento em vários registros e permissão exigida.", **DOC),
    F("src:help-consent-event-stream", "Use the Consent Event Stream",
      "https://help.salesforce.com/s/articleView?id=sf.consent_event_stream.htm&type=5", "Eventos de mudança de consentimento e permissão.", **AJ),
    # Pastas e acesso
    F("src:help-folder-access-levels", "Access Levels for Report and Dashboard Folders",
      "https://help.salesforce.com/s/articleView?id=sf.analytics_folder_access.htm&type=5", "Viewer, Editor e Manager em pastas de relatórios e dashboards.", **AJ),
    F("src:help-enhanced-folder-sharing", "Enhanced Folder Sharing for Reports and Dashboards",
      "https://help.salesforce.com/s/articleView?id=analytics.analytics_sharing_enable.htm&type=5", "Diferenças entre o compartilhamento legado e o enhanced.", **AJ),
    F("src:help-share-folder-lightning", "Share a Lightning Report or Dashboard Folder",
      "https://help.salesforce.com/s/articleView?id=analytics.rd_folders_share_enhanced.htm&type=5", "Com quem compartilhar, limites e regra do maior nível.", **AJ),
    F("src:help-folder-sharing-mdapi", "Automatically update Report or Dashboard folder sharing with Metadata API (KB)",
      "https://help.salesforce.com/s/articleView?id=000233549&type=1", "Compartilhamento de pastas como metadado (FolderShare.accessLevel).", **AJ),
    # Métricas e agregações
    F("src:help-report-formulas", "Evaluate Report Data with Formulas",
      "https://help.salesforce.com/s/articleView?id=sf.reports_formulas_overview.htm&type=5", "Summaries, row-level formulas e summary formulas.", **AJ),
    F("src:help-summary-formula-tips", "Get the Most Out of Summary Formulas: Tips, Limits, and Limitations",
      "https://help.salesforce.com/s/articleView?id=analytics.reports_csf_tips.htm&type=5", "Restrições das summary formulas.", **AJ),
    F("src:help-row-level-formula-limits", "Get the Most Out of Row-Level Formulas: Tips, Limits, and Limitations",
      "https://help.salesforce.com/s/articleView?id=sf.reports_formulas_row_level_limits.htm&type=5", "Limites das row-level formulas.", **AJ),
    F("src:help-add-bucket-column", "Add a Bucket Column",
      "https://help.salesforce.com/s/articleView?id=reports_bucketing_adding.htm&type=5", "Bucket columns: tipos e limites.", **AJ),
]

P = {}
P["sub:classificacao-e-sensibilidade"] = {
    "para_iniciantes": ini("Data Classification marca cada campo com o quanto o dado é sensível e com as regras de conformidade que se "
                           "aplicam a ele, além de quem responde pelo campo e se ele ainda está em uso. A marcação é informativa: "
                           "serve para orientar decisões de acesso, relatórios e conformidade.",
                           "O campo de CPF de um cliente recebe o nível Restricted e a categoria PII; um relatório sobre os metadados "
                           "lista todos os campos Restricted para revisão do time de segurança.",
                           E("src:help-data-classification-intro", "src:help-data-classification-fields"),
                           analogia=("É como a etiqueta 'confidencial' num arquivo de papel: avisa como tratar o conteúdo.",
                                     "A etiqueta não tranca a gaveta. Na Salesforce, quem limita o acesso é a segurança em nível de campo "
                                     "e o compartilhamento, não a classificação.")),
    "encadeamento": enc("Abre o assunto de governança em Qualidade: depois de saber o que é sensível, decide-se quanto tempo guardar "
                        "('Retenção, arquivamento e exclusão') e como registrar a vontade da pessoa ('Consentimento e privacidade'). "
                        "Criptografia e proteção técnica ficam em 'Credenciais, certificados e proteção de dados'.",
                        E("src:help-data-classification-intro")),
    "avancado": [
        av("implantacao", "Classificação como metadado", "Os valores ficam no próprio campo: no CustomField, as propriedades securityClassification, "
           "complianceGroup, businessOwnerUser, businessOwnerGroup e businessStatus; na Tooling API, em FieldDefinition (SecurityClassification, "
           "ComplianceGroup, BusinessOwnerId, BusinessStatus). As listas de valores são os StandardValueSet SecurityClassification, "
           "ComplianceGroup e FieldBusinessStatus.", E("src:help-data-classification-fields", "src:mdapi-customfield")),
        av("atencao", "Field Usage não esconde campo", "Marcar um campo como Hidden ou DeprecateCandidate em Field Usage não esconde nem expõe "
           "nada: é só registro. Para o objeto User, Data Owner, Data Sensitivity Level e Field Usage não aparecem no Object Manager; use "
           "CustomField ou o Data Classification Upload. Em contas pessoais, a categorização dos campos __pc aparece consultando Contact.",
           E("src:help-data-classification-fields")),
        av("escala", "Classificar em massa", "O Data Classification Upload aceita CSV de até 10.000 linhas (objeto, campo e nível). O download "
           "traz só campos com nível de sensibilidade, em arquivo de até 5 MB e até 2.000 registros por nível.", E("src:help-data-classification-setup")),
        av("seguranca", "Quem pode classificar", "Ver ou editar a classificação exige Customize Application ou Modify Data Classification. "
           "Níveis de sensibilidade podem ser marcados como High-risk level para indicar dados muito sensíveis à empresa.",
           E("src:help-data-classification-intro", "src:help-data-classification-setup")),
    ],
}
P["sub:retencao-arquivamento-e-exclusao"] = {
    "para_iniciantes": ini("Trata de quanto tempo um dado fica na org e do que acontece quando é apagado. Um registro excluído vai para a "
                           "Recycle Bin, onde pode ser restaurado por 15 dias; depois é apagado de vez. O histórico de mudanças de campos "
                           "também tem prazo: sem Field Audit Trail, fica até 18 meses.",
                           "Um vendedor exclui uma conta por engano e a restaura da Recycle Bin no dia seguinte.",
                           E("src:help-recycle-bin-lex", "src:help-field-history-tracking")),
    "encadeamento": enc("Vem depois de 'Classificação e sensibilidade': o que é sensível costuma ter regra de guarda e de descarte. Recuperar "
                        "metadados depois de um deploy fica em 'Versionamento, deploy e recuperação'.",
                        E("src:help-recycle-bin-lex", "src:help-delete-unwanted-data")),
    "avancado": [
        av("decisao", "Três graus de exclusão", "A exclusão comum (soft delete) manda para a Recycle Bin. Esvaziar a Recycle Bin ou usar hard "
           "delete pela API manda o registro para a fila de purga, sem passar pela Recycle Bin. Para remover o registro da tabela do banco, "
           "o caminho é pedir um physical delete ao Support.", E("src:help-delete-unwanted-data")),
        av("limite", "Recycle Bin", "Itens ficam 15 dias e depois são agendados para exclusão permanente, sem hora garantida. Não contam no "
           "armazenamento e não há limite de quantidade. Restaurar itens de outros usuários e excluir permanentemente exigem Modify All Data.",
           E("src:help-recycle-bin-lex")),
        av("decisao", "Field History Tracking ou Field Audit Trail", "O rastreamento padrão guarda até 20 campos por objeto por 18 a 24 meses "
           "no objeto de histórico. O Field Audit Trail vai até 200 campos, guarda até ser excluído no big object FieldHistoryArchive e só "
           "é acessível por API.", E("src:help-field-audit-trail", "src:help-field-history-tracking")),
        av("implantacao", "Política de retenção do histórico", "Com Field Audit Trail, a política HistoryRetentionPolicy define, por objeto, "
           "quantos meses o histórico fica antes de ser arquivado, e é implantada pela Metadata API. O padrão (18 meses em produção, um mês em "
           "sandbox) não vem no retrieve do objeto: só políticas customizadas vêm.",
           E("src:help-field-audit-trail", "src:mdapi-historyretentionpolicy")),
        av("atencao", "Excluir não apaga o arquivo", "Excluir um registro em produção apaga o histórico relacionado, mas não a cópia já levada "
           "para FieldHistoryArchive.", E("src:help-field-audit-trail")),
    ],
}
P["sub:consentimento-e-privacidade"] = {
    "para_iniciantes": ini("Guarda o que cada pessoa autorizou: se aceita ser contatada, por qual canal, em qual endereço e para qual "
                           "finalidade. O objeto Individual concentra as preferências gerais de privacidade, e outros objetos "
                           "detalham o consentimento por canal e por ponto de contato.",
                           "Uma cliente aceita receber e-mail, mas não ligações: o registro de ContactPointTypeConsent de e-mail fica "
                           "Opt In e o de telefone, Opt Out.",
                           E("src:help-consent-data-model", "src:help-contact-point-type-consent-fields")),
    "encadeamento": enc("Fecha o trio de governança de Qualidade: depois de classificar e definir retenção, registra-se a vontade da pessoa "
                        "sobre os próprios dados. Lead, Contact, User e contas pessoais se ligam ao Individual.",
                        E("src:help-consent-data-model", "src:help-consent-objects")),
    "avancado": [
        av("decisao", "Em que nível registrar", "O modelo tem quatro níveis: global (Individual), canal (ContactPointTypeConsent), ponto de contato "
           "(ContactPointConsent) e finalidade (DataUsePurpose, ligada aos dois anteriores). BusinessBrand separa preferências de marcas "
           "diferentes na mesma org.", E("src:help-consent-data-model")),
        av("atencao", "Os objetos só guardam", "Os objetos de consentimento registram as preferências, mas não as cumprem sozinhos: a empresa "
           "decide como honrar a privacidade e implementa o processo.", E("src:help-consent-objects")),
        av("seguranca", "Consent Write passa por cima do compartilhamento", "A Consent Write API grava consentimento em vários objetos ligados por "
           "lookup ou e-mail, até 1.000 ids por chamada. Exige ModifyAllData ou ConsentApiUpdate e grava na org inteira, não só nos registros "
           "que o usuário vê. A resposta pode vir com 200 mesmo havendo erros.", E("src:rest-consent-write")),
        av("escala", "Acompanhar mudanças", "O Consent Event Stream emite um evento a cada mudança de consentimento ou contato nos objetos "
           "principais; cada evento fica disponível por 24 horas. Exige ReadAllData ou PrivacyDataAccess.", E("src:help-consent-event-stream")),
        av("limite", "Criptografia e Consent API", "A Consent API não localiza registros cujo e-mail esteja protegido por Shield Platform Encryption.",
           E("src:help-consent-data-model")),
    ],
}
P["sub:pastas-e-acesso"] = {
    "para_iniciantes": ini("Relatórios e dashboards ficam em pastas, e é a pasta que se compartilha. Cada pessoa, grupo ou papel recebe um "
                           "nível na pasta: Viewer vê, Editor salva e altera os itens e Manager também controla quem tem acesso.",
                           "O gerente cria a pasta 'Relatórios regionais', dá Viewer ao grupo de vendedores e Manager à gerente de vendas.",
                           E("src:help-folder-access-levels")),
    "encadeamento": enc("Vem depois de montar relatórios e dashboards: decide quem enxerga cada um. O acesso aos registros que aparecem "
                        "dentro do relatório fica em 'Acesso a registros e hierarquias'.",
                        E("src:help-folder-access-levels")),
    "avancado": [
        av("seguranca", "Pasta e permissão se somam", "O nível na pasta não decide sozinho o que a pessoa faz: as permissões do usuário também "
           "contam. Manage Reports in Public Folders e View Reports in Public Folders alcançam todas as pastas, menos as pessoais de outros "
           "usuários. Uma pasta nova só é acessível ao criador e a administradores até ser compartilhada.",
           E("src:help-folder-access-levels", "src:help-enhanced-folder-sharing")),
        av("decisao", "Legado ou enhanced folder sharing", "No legado, a pasta era somente leitura ou leitura e escrita e visível a todos, oculta "
           "ou a grupos e papéis. No enhanced, a pasta tem só nome, e cada compartilhamento recebe View, Edit ou Manage.",
           E("src:help-enhanced-folder-sharing")),
        av("limite", "Quantos compartilhamentos", "Pela interface, até 25 usuários, grupos, papéis ou territórios; pela folder sharing REST API, até "
           "500. Quem aparece em mais de uma entrada fica com o maior nível.", E("src:help-share-folder-lightning")),
        av("implantacao", "Compartilhamento como metadado", "O compartilhamento das pastas pode ser recuperado e implantado pela Metadata API, "
           "editando accessLevel em FolderShare, com os valores View, EditAllContents e Manage.", E("src:help-folder-sharing-mdapi")),
    ],
}
P["sub:metricas-e-agregacoes"] = {
    "para_iniciantes": ini("São os cálculos feitos dentro do relatório. Summaries somam, tiram média, mínimo ou máximo de uma coluna, por "
                           "grupo e no total. Row-level formulas calculam algo para cada registro, e summary formulas calculam sobre os "
                           "grupos. Bucket columns agrupam valores em faixas sem precisar de fórmula.",
                           "Num relatório de oportunidades, uma row-level formula calcula os dias até fechar cada uma, e uma bucket "
                           "column separa os valores em pequeno, médio e grande.",
                           E("src:help-report-formulas", "src:help-add-bucket-column")),
    "encadeamento": enc("Funciona sobre o tipo de relatório escolhido ('Tipos de relatório'): só entram campos que ele oferece. Campos de "
                        "resumo definidos no modelo de dados ficam em 'Campos e tipos'.",
                        E("src:help-report-formulas", "src:help-custom-report-types")),
    "avancado": [
        av("decisao", "Qual cálculo usar", "Summaries não exigem fórmula. Row-level formula responde perguntas por registro; summary formula compara "
           "grupos, e PREVGROUPVAL e PARENTGROUPVAL comparam com o grupo anterior ou com o grupo pai e o total. Para reusar um agrupamento em "
           "vários relatórios, um formula field no objeto substitui a bucket column, que vale só no relatório onde foi criada.",
           E("src:help-report-formulas", "src:help-add-bucket-column")),
        av("limite", "Row-level formulas", "Até duas por relatório, cada uma com até 5 campos distintos. Não referenciam buckets, summary formulas "
           "nem outras row-level formulas, e não existem em tipos 'with or without', joined reports e reporting snapshots.",
           E("src:help-row-level-formula-limits")),
        av("limite", "Summary formulas e buckets", "Summary formulas não usam datas, não referenciam outra summary formula nem row-level formula e "
           "exigem relatório agrupado; não dá para agrupar, filtrar ou reordenar por elas. Cada relatório aceita até 5 bucket fields, com até "
           "20 buckets de até 20 valores.", E("src:help-summary-formula-tips", "src:help-add-bucket-column")),
        av("atencao", "Moeda e erros", "Row-level formulas usam sempre a moeda padrão da org, mesmo com multimoeda no relatório. Em summary "
           "formulas, percentuais são decimais (20% vira 0,20), e divisão por zero mostra #Error!.",
           E("src:help-row-level-formula-limits", "src:help-summary-formula-tips")),
    ],
}

CONTEUDO_PENDENTES2 = P
