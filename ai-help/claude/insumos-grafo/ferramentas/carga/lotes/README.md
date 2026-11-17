# Lotes novos

Scripts de lotes carregados com `ferramentas/carga/` (a partir do lote 6). Veja o esqueleto em `ferramentas/README.md`.

| Script | O que faz |
|---|---|
| `exemplos_regras_e_horarios.py` | Exemplos XML escritos à mão para AssignmentRules, EscalationRules e BusinessHoursSettings (issue #20). |
| `escopo_temas.py` | `escopo` e `fora_do_escopo` de todos os temas (issue #34, fase 2). Reexecutável. |
| `referencias_temas.py` | Fontes e referências oficiais dos 14 temas de primeiro nível (issue #34, fase 3). Reexecutável. |
| `conteudo_temas.py` | Conteúdo específico por tema: `para_iniciantes`, `encadeamento` e `avancado`, cada bloco com fontes (issue #34). Piloto: Interface e Lightning pages e componentes. |
| `conteudo_pendentes.py` | Conteúdo dos temas internos que estavam sem fonte, lote 1 (issue #34). Usado por `conteudo_temas.py`. |
| `conteudo_pendentes2.py` | Lote 2 dos temas sem fonte: classificação e sensibilidade, retenção, consentimento, pastas e acesso, métricas (issue #34). Usado por `conteudo_temas.py`. |
| `conteudo_pendentes3.py` | Lote 3 dos temas sem fonte: colaboração, templates, recuperação de conhecimento, experiências web/portais/mobile, habilitação de recursos, metadados de configuração de dados (issue #34). Usado por `conteudo_temas.py`. |
| `conteudo_pendentes4.py` | Lote 4 dos temas sem fonte: serviço de campo, experiências externas, capacidades setoriais, outras áreas (issue #34). Usado por `conteudo_temas.py`. |
| `temas_internos.py` | Limpeza do dado genérico dos temas internos (issue #34, item 3): descrição, referências oficiais já registradas e nota de estado, um tema principal por vez. Reexecutável. |
| `conteudo_detalhe.py` | Detalhamento dos temas principais (issue #34, item 3): fontes novas e conteúdo que substitui o de temas internos rasos. Aplicado por último por `conteudo_temas.py`. |
| `lote6a_org.py` | Lote 6a (issue #34, item 3): metadata types, estruturas e funcionalidades do tema Organização e configurações base. Reexecutável; rode depois `conteudo_temas.py` e `temas_internos.py`. |
| `lote6b_processos.py` | Lote 6b (issue #34, item 3): metadata types, estrutura e funcionalidades do tema Processos de negócio específicos de produto; corrige a descrição genérica de 9 tipos Settings. Reexecutável; rode depois `conteudo_temas.py` e `temas_internos.py`. |
| `lote6c_automacao.py` | Lote 6c (issue #34, item 3): seis funcionalidades do tema Automação. Reexecutável; rode em seguida `lote6d_automacao_tipos.py`. |
| `lote6d_automacao_tipos.py` | Lote 6d: metadata types e estruturas de Automação (ApprovalProcess, CustomNotificationType, AutoResponseRules, FlowSettings, ApexTrigger) e ligação com as funcionalidades do lote 6c. Reexecutável; rode depois `lote7a_tipos_destravados.py`, `conteudo_temas.py` e `temas_internos.py`. |
| `lote7a_tipos_destravados.py` | Lote 7a (rodada B1): CaseSettings, Workflow com 7 tipos filhos e Translations, lidos do guia versionado 264.0; completa ApprovalProcess e marca, nos tipos dos lotes 6a, 6b e 6d, os campos que não constam do guia versionado. Reexecutável; rode depois dos lotes 6a a 6d e antes de `conteudo_temas.py` e `temas_internos.py`. |
| `lote7b_desenvolvimento.py` | Lote 7b (rodada A1): 12 metadata types, 5 estruturas e 14 funcionalidades do tema Desenvolvimento, testes e entrega, lidos do guia versionado 264.0; completa ApexTrigger. Reexecutável; rode depois de `lote7a_tipos_destravados.py` e antes de `conteudo_temas.py` e `temas_internos.py`. |
| `lote7c_assincrono.py` | Lote 7c (rodada A2): objetos API AsyncApexJob, CronTrigger e CronJobDetail, 2 relacionamentos e 5 funcionalidades do tema Execução assíncrona. Reexecutável; rode depois de `lote7b_desenvolvimento.py` e antes de `conteudo_temas.py` e `temas_internos.py`. |
| `lote7d_interface.py` | Lote 7d (rodada A3): CustomApplication, Layout, CompactLayout, LightningExperienceTheme e BrandingSet, com 41 estruturas, e 5 funcionalidades de Interface. Com `--nota`, regrava a lista de campos da nota de extração. |
| `lote7e_observabilidade.py` | Lote 7e (rodada A4): objetos API SetupAuditTrail e EventLogFile e 3 funcionalidades de Observabilidade. |
| `lote7f_conteudo_ia.py` | Lote 7f (rodadas A5 e A6): EmailTemplate, Letterhead, Document, ContentAsset, ChatterSettings, GenAiPromptTemplate, GenAiFunction, GenAiPlugin e EinsteinGptSettings, com 14 estruturas, e 9 funcionalidades de Conteúdo e de IA e agentes. Regrava a lista de campos da nota de extração. |
| `lote7g_relatorios_qualidade.py` | Lote 7g (rodadas B2 e B3): Report e Dashboard, com os 36 subtipos das duas páginas (lidas inteiras em partes), ReportType, ReportFolder, DashboardFolder, DuplicateRule e MatchingRules, com 46 estruturas; 6 funcionalidades de Relatórios e de Qualidade, inclusive crm-analytics. Regrava a lista de campos da nota de extração. |
| `lote7h_filas_grupos.py` | Lote 7h (pedido da autora): metadata types Queue (7 estruturas) e Group; objetos API Group, GroupMember e QueueSobject; funcionalidades filas e public-groups. Regrava a lista de campos da nota de extração. |
| `lote7i_interface_fecho.py` | Lote 7i (fecho da rodada A3): Network (primeiro nível), CustomSite, NavigationMenu, LightningExperienceSettings, ListView, WebLink e PathAssistantSettings, com 8 estruturas; funcionalidades experience-cloud-sites, list-views e botoes-e-links-customizados. Regrava a lista de campos da nota de extração. |
| `lote7j_observabilidade_fecho.py` | Lote 7j (fecho da rodada A4): objetos da Tooling API TraceFlag, DebugLevel e ApexLog; funcionalidades system-overview, armazenamento-de-dados-e-arquivos e transaction-security. Regrava a lista de campos da nota de extração. |
| `lote7k_qualidade_fecho.py` | Lote 7k (fecho da rodada B3): metadata type PrivacySettings; objetos Individual, ContactPointTypeConsent, DataUsePurpose e FieldHistoryArchive; funcionalidades field-history-tracking, field-audit-trail, recycle-bin, data-classification e consent-management. Regrava a lista de campos da nota de extração. |
| `lote7l_b4_estruturas.py` | Lote 7l (rodada B4, parte A; issues #8 e #9): estruturas de KnowledgeSettings, ForecastingSettings, Profile, CustomObject, CustomField e ValueSet; metadata types BusinessProcess, FieldSet e Index; campos e chamadas da Tooling API de 6 objetos. Liga as estruturas aos tipos históricos e recalcula a cobertura. Regrava a lista de campos da nota de extração. |
| `conteudo_extras.py` | Acréscimos de conteúdo a temas que já têm texto (itens avançados, "comece por"); aplicado por `conteudo_temas.py`, por último. |
