"""Issue #34: temas internos que estavam pendentes por falta de fonte (lote 1).
Fontes lidas pelos resultados de busca restritos aos domínios oficiais: fontes/extracoes/temas-pendentes-lote1.txt.
Usado por conteudo_temas.py.
"""
from carga.catalogo import fonte
from conteudo_cls import E, ini, enc, av

DATA = "2026-11-09"
EXT = "fontes/extracoes/temas-pendentes-lote1.txt"
AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")
DOC = dict(metodo="leitura_resultado_busca")


def F(i, t, u, p, **k):
    return fonte(i, t, u, p, EXT, DATA, **k)


FONTES_PENDENTES = [
    F("src:help-custom-report-types", "Custom Report Types", "https://help.salesforce.com/s/articleView?id=sf.reports_report_type_objects.htm", "O que é um tipo de relatório e edições.", **AJ),
    F("src:help-crt-legacy-builder", "Create a Custom Report Type in the Legacy Custom Report Type Builder", "https://help.salesforce.com/s/articleView?id=reports_defining_report_types.htm", "Objeto principal, relações com filhos e campos via lookup.", **AJ),
    F("src:help-report-limits", "Reports and Dashboards Limits and Allocations", "https://help.salesforce.com/s/articleView?id=analytics.rd_reports_dashboards_limits.htm", "Limites de tipos de relatório customizados.", **AJ),
    F("src:help-wf-pb-eos", "Salesforce Workflow Rules & Process Builder End of Support (KB)", "https://help.salesforce.com/s/articleView?id=001096524&type=1", "Fim do suporte de Workflow Rules e Process Builder.", **AJ),
    F("src:help-migrate-to-flow-considerations", "Migrate to Flow Tool Considerations", "https://help.salesforce.com/s/articleView?id=sf.migrate_to_flow_tool_considerations.htm", "O que a ferramenta Migrate to Flow suporta e cuidados.", **AJ),
    F("src:apex-customnotification", "CustomNotification Class (Apex Reference)", "https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_class_Messaging_CustomNotification.htm", "Envio de notificações customizadas pelo Apex.", **DOC),
    F("src:actions-custom-notification", "Custom Notification Actions (Actions Developer Guide)", "https://developer.salesforce.com/docs/platform/api-action/guide/actions-obj-custom-notification.html", "Ação de notificação customizada e permissão exigida.", versao="sem versão na página", **DOC),
    F("src:pkg1-components", "Components Available in First-Generation Managed Packages", "https://developer.salesforce.com/docs/platform/pkg1-dev/guide/first-gen-packageable-components.html", "Limites de CustomNotificationType em orgs assinantes.", versao="sem versão na página", **DOC),
    F("src:apex-debug-logs", "Working with Logs in the Developer Console (Apex Developer Guide)", "https://developer.salesforce.com/docs/atlas.en-us.264.0.apexcode.meta/pages/apex_debugging_system_log_console.htm", "Categorias e níveis de debug log.", **DOC),
    F("src:help-mydomain", "My Domain", "https://help.salesforce.com/s/articleView?id=sf.domain_name_overview.htm", "O que é o My Domain e URLs da org.", **AJ),
    F("src:help-mydomain-changes", "Update Your Org for My Domain Changes", "https://help.salesforce.com/s/articleView?id=sf.domain_name_guidelines.htm", "Impactos de mudar o My Domain.", **AJ),
    F("src:help-mydomain-login-policy", "Set the My Domain Login Policy", "https://help.salesforce.com/s/articleView?id=sf.domain_name_setting_login_policy.htm", "Política de login pelo My Domain.", **AJ),
    F("src:help-custom-settings", "Define Custom Settings", "https://help.salesforce.com/s/articleView?id=platform.cs_define.htm", "Custom settings e recomendação de custom metadata types.", **AJ),
    F("src:help-cmdt-limitations", "Custom Metadata Types Limitations", "https://help.salesforce.com/s/articleView?id=platform.custommetadatatypes_limitations.htm", "Cache, alteração por Apex e bloqueios no deploy.", **AJ),
    F("src:mdapi-custommetadata", "CustomMetadata (Metadata API)", "https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-custommetadata.html", "Registro de custom metadata type como metadado.", **DOC),
    F("src:help-rtf-considerations", "Record-Triggered Flow Considerations", "https://help.salesforce.com/s/articleView?id=sf.flow_considerations_trigger_record.htm", "Callouts e caminho assíncrono em record-triggered flows.", **AJ),
    F("src:help-schedule-flow-considerations", "Schedule-Triggered Flow Considerations", "https://help.salesforce.com/s/articleView?id=flow_considerations_trigger_schedule.htm", "Limites de flows agendados.", **AJ),
]

P = {}
P["sub:tipos-de-relatorio"] = {
    "para_iniciantes": ini("Um tipo de relatório define quais registros e campos um relatório pode usar, a partir de um objeto principal e dos "
                           "objetos relacionados a ele. Tipos customizados acrescentam objetos e campos que não vêm prontos.",
                           "Um tipo 'Contas com oportunidades' permite montar relatórios que juntam dados das duas.",
                           E("src:help-custom-report-types")),
    "encadeamento": enc("Fica na base de Reports: todo relatório parte de um tipo de relatório, padrão ou customizado.", E("src:help-custom-report-types")),
    "avancado": [
        av("decisao", "Com ou sem registros filhos", "Na relação com cada objeto filho, 'cada A precisa ter ao menos um B' mostra só pais com filhos; 'A pode ou não "
           "ter B' mostra todos os pais. O objeto principal não pode ser trocado depois de salvo.", E("src:help-crt-legacy-builder")),
        av("limite", "Limites do tipo customizado", "Até 60 referências de objeto por tipo, até 1.000 campos e erro se o relatório tiver colunas de mais de 20 objetos. "
           "Campos de histórico não podem ser incluídos. A quantidade de tipos customizados varia por edição (300 em Enterprise).", E("src:help-report-limits")),
    ],
}
P["sub:mecanismos-legados-e-migracao"] = {
    "para_iniciantes": ini("Workflow Rules e Process Builder são ferramentas antigas de automação. O suporte acabou em 31 de dezembro de 2025: "
                           "o que já existe continua rodando, mas sem suporte nem correção de bugs. O caminho é migrar para Flow.",
                           "Uma regra de workflow que só atualiza um campo é convertida pela ferramenta Migrate to Flow num flow de atualização rápida.",
                           E("src:help-wf-pb-eos", "src:help-migrate-to-flow-considerations")),
    "encadeamento": enc("Explica de onde vêm automações antigas que ainda rodam na org; o destino da migração é 'Flow e orquestração'.",
                        E("src:help-wf-pb-eos", "src:mdapi-flow")),
    "avancado": [
        av("implantacao", "Migre na mesma org", "Migre o processo na mesma org do original, e não numa org intermediária para depois implantar: assim o flow trata as "
           "ações agendadas pendentes do processo antigo.", E("src:help-migrate-to-flow-considerations")),
        av("atencao", "O que a ferramenta não cobre", "A Migrate to Flow só aceita processos disparados por registro; processos com recursão avaliam o registro uma vez; "
           "e flows disparados por registro podem se comportar diferente das regras por causa da ordem de execução. Teste depois de migrar.",
           E("src:help-migrate-to-flow-considerations")),
    ],
}
P["sub:notificacoes"] = {
    "para_iniciantes": ini("Notificações customizadas avisam pessoas no desktop ou no celular quando algo acontece. Primeiro se cria um tipo de "
                           "notificação; depois, um flow, o Apex ou a REST API envia a notificação usando esse tipo.",
                           "Quando um caso de prioridade alta é aberto, um flow envia uma notificação à fila responsável, que abre o caso com um toque.",
                           E("src:actions-custom-notification", "src:apex-customnotification")),
    "encadeamento": enc("Costuma ser o último passo de uma automação; modelos de e-mail, outro canal de aviso, ficam em 'Templates e comunicação'.",
                        E("src:actions-custom-notification")),
    "avancado": [
        av("seguranca", "Permissão para enviar", "Em orgs criadas no Winter '21 ou depois, a permissão Send Custom Notifications é exigida em flows no contexto do usuário, "
           "na REST API e no Apex; não é exigida em flows no contexto de sistema.", E("src:actions-custom-notification")),
        av("limite", "Destinatários e volume", "Cada envio aceita até 500 destinatários (usuários, equipes, grupos ou filas), com título de até 250 e corpo de até 750 "
           "caracteres. Uma org aceita até 500 tipos de notificação e 10.000 ações de notificação por hora.",
           E("src:apex-customnotification", "src:pkg1-components")),
    ],
}
P["sub:logs-e-rastreamento"] = {
    "para_iniciantes": ini("Debug logs registram o que aconteceu numa execução: consultas, gravações, Apex, regras e chamadas externas. Serve para "
                           "investigar por que algo não funcionou.",
                           "Um desenvolvedor liga o log para um usuário, reproduz o erro e lê no log em que linha a gravação falhou.",
                           E("src:apex-debug-logs")),
    "encadeamento": enc("Mostra o que o código e as automações fizeram; os eventos de uso e atividade ficam em 'Eventos de monitoramento'.",
                        E("src:apex-debug-logs", "src:security-guide")),
    "avancado": [
        av("decisao", "Categoria e nível", "O conteúdo do log é definido por categoria (Database, Workflow, Validation, Callout, Apex Code, Apex Profiling, "
           "Visualforce, System) e por nível, de NONE a FINEST. Os níveis são cumulativos, e a maioria dos eventos começa a ser registrada no nível INFO.",
           E("src:apex-debug-logs")),
    ],
}
P["sub:dominios-e-urls"] = {
    "para_iniciantes": ini("O My Domain é o nome da org nas URLs de login e de aplicação, como mycompany.my.salesforce.com e mycompany.my.site.com.",
                           "Os usuários da empresa entram por https://mycompany.my.salesforce.com, e o portal de clientes usa mycompany.my.site.com.",
                           E("src:help-mydomain")),
    "encadeamento": enc("Afeta login, SSO e integrações; os endereços externos que a org chama ficam em 'Chamadas externas e endpoints'.",
                        E("src:help-mydomain-changes")),
    "avancado": [
        av("atencao", "Mudar o My Domain quebra o que está fixo", "Mudar o nome ou o sufixo muda a URL de login: SSO e MFA podem parar de funcionar, e named credentials "
           "e templates com a URL antiga precisam ser atualizados.", E("src:help-mydomain-changes")),
        av("decisao", "Integração com URL devolvida pelo login", "Integrações de API devem usar o serverURL devolvido pelo login, não uma URL fixa. Dá para exigir que "
           "logins SOAP usem o My Domain, e tráfego de API com URL de instância incorreta é bloqueado depois do Summer '26.",
           E("src:help-mydomain-changes", "src:help-mydomain-login-policy")),
    ],
}
P["sub:parametros-reutilizaveis"] = {
    "para_iniciantes": ini("Guarda valores de configuração lidos por várias funcionalidades, como tabelas de regras ou mapeamentos. Há dois "
                           "mecanismos: custom metadata types, cujos registros são metadados, e custom settings, cujos registros são dados.",
                           "Uma tabela de faixas de desconto fica num custom metadata type e é lida por um flow e por uma regra de validação.",
                           E("src:help-custom-settings", "src:mdapi-custommetadata")),
    "encadeamento": enc("É configuração reaproveitada pela org inteira; o lado 'como código' das configurações gerais fica em 'Settings'.",
                        E("src:help-custom-settings")),
    "avancado": [
        av("decisao", "Custom metadata em vez de custom settings", "A Salesforce recomenda custom metadata types: os registros podem ser migrados por pacotes de segunda "
           "geração ou Metadata API, ao contrário dos de list custom settings. Custom settings do tipo Hierarchy personalizam por perfil ou usuário.",
           E("src:help-custom-settings")),
        av("atencao", "Cache e bloqueios", "Registros de custom metadata ficam em cache por tipo depois da primeira leitura; durante o deploy, os registros incluídos ficam "
           "bloqueados e podem causar row lock. Para alterá-los pelo Apex, use o pacote Metadata.", E("src:help-cmdt-limitations")),
        av("implantacao", "Registro como arquivo", "Cada registro é um componente CustomMetadata, com sufixo .md na pasta customMetadata.", E("src:mdapi-custommetadata")),
    ],
}
P["sub:caminhos-assincronos"] = {
    "para_iniciantes": ini("Num flow disparado por registro, o caminho assíncrono roda em segundo plano depois que a gravação é confirmada. É ele "
                           "que permite chamar sistemas externos, o que o caminho imediato não pode fazer.",
                           "Ao criar um pedido, o caminho assíncrono do flow avisa o sistema de entregas sem prender a gravação.",
                           E("src:help-rtf-considerations")),
    "encadeamento": enc("É a parte assíncrona de 'Flow e orquestração'; o equivalente em código fica em Queueable e Future.", E("src:help-rtf-considerations", "src:apex-queueable")),
    "avancado": [
        av("atencao", "Callout só fora do caminho imediato", "Um record-triggered flow falha se tentar acessar dados externos no caminho síncrono, porque callouts não "
           "rodam enquanto o registro é salvo. Caminhos assíncronos não suportam o operador ISCHANGED.", E("src:help-rtf-considerations")),
        av("limite", "Flows agendados", "Flows agendados têm teto de 250.000 entrevistas por 24 horas, ou licenças × 200, o que for maior; transações Apex síncronas "
           "chamadas por flows assíncronos contam nos limites síncronos.", E("src:help-schedule-flow-considerations")),
    ],
}

CONTEUDO_PENDENTES = P
