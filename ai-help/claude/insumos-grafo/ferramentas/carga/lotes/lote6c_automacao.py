"""Lote 6c (issue #34, item 3): funcionalidades do tema Automação de processos e regras de negócio.

Cria seis funcionalidades: processos de aprovação, Flow Orchestration, regras de resposta automática, Apex triggers,
notificações customizadas e Workflow Rules/Process Builder.

NENHUM metadata type entra neste lote: em 2026-11-15 a leitura das páginas da Metadata API (WebFetch) ficou sem aprovação,
e o resumo da busca não traz a tabela de campos. Os tipos correspondentes (ApprovalProcess, AutoResponseRules, ApexTrigger,
CustomNotificationType, Workflow e filhos, FlowSettings, FlowDefinition) constam do inventário v68 e ficam registrados como
ausência "desconhecido" em cada funcionalidade, para um lote seguinte.

Cita fontes registradas por conteudo_temas.py: rode este script e, em seguida, conteudo_temas.py e temas_internos.py.
Reexecutável. Uso: python3 ferramentas/carga/lotes/lote6c_automacao.py
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import af, ev       # noqa: E402
from carga import catalogo as C     # noqa: E402

AUTO = "automacao-de-processos-e-regras-de-negocio"
SEM_OBJ = {"tipo": "objeto_api", "estado": "desconhecido",
           "motivo": "Objetos API do tema não investigados no lote 6c; a lista vazia não comprova inexistência."}


def sem_mdt(tipos):
    return {"tipo": "metadata_type", "estado": "desconhecido",
            "motivo": f"{tipos} no inventário v68, mas as propriedades não foram lidas no lote 6c (leitura da página sem aprovação em "
                      "2026-11-15); por isso nenhum metadata type está ligado ainda."}


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


SETUP_DESCONHECIDO = af("desconhecido", None, "Caminho de Setup não confirmado nas fontes lidas.", [])

C.funcionalidade(
    "processos-de-aprovacao", "Processos de aprovação", "Approval Processes",
    ["approval process", "classic approval processes", "flow approval processes", "aprovações", "aprovação"],
    "Automatiza como um registro é aprovado: define cada passo, de quem pedir a aprovação e o que acontece em cada ponto. Existe na forma "
    "clássica (Classic Approval Processes) e na forma baseada em flow (Flow Approval Processes).",
    "Garantir que alguém com autoridade decida antes de o processo seguir, com registro de quem aprovou.",
    "Uma despesa acima de certo valor vai para o gestor e depois para a diretoria; enquanto espera, o registro fica bloqueado para edição.",
    (AUTO, "decisoes-e-aprovacoes"), [], [], [],
    ["src:help-approvals-classic", "src:help-approvals-classic-limits", "src:help-approvals-classic-manage", "src:help-flow-approvals-concepts",
     "src:mdapi-approvalprocess"],
    [sem_mdt("ApprovalProcess consta"), SEM_OBJ], SETUP_DESCONHECIDO,
    limitacoes=["Processo clássico: até 30 passos, 25 aprovadores por passo e 40 ações de cada tipo; por objeto, 300 processos ativos.",
                "Processo clássico não aceita o objeto User; Flow Approval Processes aceitam."],
    alertas=["Depois de ativado, um processo clássico não aceita incluir, excluir ou reordenar passos."])

C.funcionalidade(
    "flow-orchestration", "Flow Orchestration", "Flow Orchestration", ["orquestração", "orchestration", "orchestrations", "stages e steps"],
    "Processo de várias etapas que encadeia flows: stages contêm steps; o interactive step atribui um screen flow a uma pessoa, grupo ou fila, "
    "e o background step roda um autolaunched flow sem interação.",
    "Coordenar processos longos, que passam por várias pessoas e sistemas e esperam cada um terminar a sua parte.",
    "Na admissão de um funcionário, o RH preenche um formulário, a TI recebe a tarefa de criar acessos e um passo automático atualiza o registro.",
    (AUTO, "flow-e-orquestracao"), [], [], [],
    ["src:help-orchestration-overview", "src:help-orchestration-types", "src:help-orchestration-steps"],
    [{"tipo": "metadata_type", "estado": "desconhecido",
      "motivo": "A Ajuda informa que orquestrações são construídas no Flow Builder, mas não foi lido como elas são representadas na Metadata "
                "API; por isso não há ligação com mdt:Flow."}, SEM_OBJ],
    SETUP_DESCONHECIDO)

C.funcionalidade(
    "regras-de-resposta-automatica", "Regras de resposta automática", "Auto-Response Rules",
    ["auto-response rules", "resposta automática", "case auto-response rules", "lead auto-response rules"],
    "Regra que envia automaticamente o primeiro e-mail a quem abriu um caso ou enviou um lead pelo site, escolhendo o template conforme os "
    "dados do registro.",
    "Confirmar ao cliente que o pedido chegou, sem depender de alguém responder à mão.",
    "Quem abre um caso pelo formulário do site recebe na hora um e-mail com o número do caso.",
    (AUTO, "acoes-e-regras"),
    [("processos-de-negocio-especificos-de-produto", "atendimento", "Responde a casos de Web-to-Case, Email-to-Case e portais."),
     ("processos-de-negocio-especificos-de-produto", "vendas", "Responde a leads de Web-to-Lead.")],
    [], [], ["src:help-auto-response-setup", "src:help-auto-response-vs-workflow", "src:help-case-rules-overview", "src:help-survey-case-feedback"],
    [sem_mdt("AutoResponseRules consta"), SEM_OBJ],
    setup("Setup > Quick Find: Case Auto-Response Rules > Case Auto-Response Rules", "src:help-survey-case-feedback",
          "Caminho confirmado para as regras de casos; o das regras de leads não foi confirmado."),
    limitacoes=["Só uma regra fica ativa para leads e uma para casos.", "A regra roda só na criação do registro e para na primeira entrada que casar."],
    pre=["Customize Application (para criar regras de resposta automática)."])

C.funcionalidade(
    "apex-triggers", "Apex triggers", "Apex Triggers", ["trigger", "triggers", "gatilho apex", "before trigger", "after trigger"],
    "Código Apex que roda antes ou depois de um registro ser inserido, alterado, excluído, mesclado ou restaurado.",
    "Automatizar o que as ferramentas declarativas não cobrem, no momento exato da gravação.",
    "Ao inserir itens de um pedido, um trigger confere o estoque de todos os itens de uma vez antes de gravar.",
    (AUTO, "automacao-apex"),
    [("desenvolvimento-testes-e-entrega", "codigo-e-bundles", "Trigger é código Apex e segue as regras de teste e implantação.")],
    [], [], ["src:apex-triggers", "src:apex-triggers-order", "src:apex-triggers-bulk", "src:apex-triggers-defining", "src:apex-testing-best-practices"],
    [sem_mdt("ApexTrigger consta"), SEM_OBJ],
    setup("Object management settings do objeto > Triggers > New", "src:apex-triggers-defining",
          "Para Attachment, ContentDocument e Note, o trigger só é criado por ferramentas de desenvolvimento ou Metadata API."),
    limitacoes=["75% do código Apex precisa de cobertura de testes, e todo trigger precisa de alguma cobertura."],
    alertas=["Um trigger pode receber vários registros de uma vez; o código deve ser escrito para mais de um registro."])

C.funcionalidade(
    "notificacoes-customizadas", "Notificações customizadas", "Custom Notifications",
    ["custom notifications", "notification builder", "custom notification type", "send custom notification"],
    "Avisos que aparecem no sino de notificações, no desktop ou no app móvel. Primeiro se cria um tipo de notificação; depois, uma automação "
    "envia a notificação usando esse tipo.",
    "Avisar a pessoa certa quando algo importante acontece, com um toque que leva ao registro.",
    "Quando um caso de prioridade alta é aberto, um flow envia uma notificação à fila responsável.",
    (AUTO, "notificacoes"), [], [], [],
    ["src:help-notif-flow-example", "src:help-notif-considerations", "src:help-notif-builder", "src:actions-custom-notification"],
    [sem_mdt("CustomNotificationType consta"), SEM_OBJ],
    setup("Setup > Quick Find: Notification Builder > Custom Notifications", "src:help-notif-flow-example"),
    limitacoes=["Até 500 tipos de notificação customizados.",
                "Até 10.000 ações de notificação por hora; o que exceder naquela hora é perdido.",
                "Título e corpo aceitam só texto simples."],
    pre=["Customize Application (para criar e editar tipos); Send Custom Notifications (para enviar)."])

C.funcionalidade(
    "workflow-rules-e-process-builder", "Workflow Rules e Process Builder", "Workflow Rules and Process Builder",
    ["workflow rule", "workflow", "process builder", "regras de workflow", "migrate to flow"],
    "Ferramentas antigas de automação declarativa. O suporte acabou em 31 de dezembro de 2025: o que existe continua rodando, mas sem "
    "correção de bugs.",
    "Entender automações antigas que ainda rodam na org e planejar a migração para Flow.",
    "Uma regra de workflow que só atualiza um campo é convertida pela ferramenta Migrate to Flow num flow equivalente.",
    (AUTO, "mecanismos-legados-e-migracao"), [], [], [],
    ["src:help-wf-pb-eos", "src:help-migrate-to-flow-considerations"],
    [sem_mdt("Workflow, WorkflowRule e os demais tipos Workflow* constam"), SEM_OBJ], SETUP_DESCONHECIDO,
    alertas=["Sem suporte desde 31 de dezembro de 2025; a Salesforce recomenda migrar para Flow.",
             "Flows que substituem regras podem se comportar diferente, por causa da ordem de execução; teste depois de migrar."])

print("lote 6c: 6 funcionalidades gravadas (nenhum metadata type)")
