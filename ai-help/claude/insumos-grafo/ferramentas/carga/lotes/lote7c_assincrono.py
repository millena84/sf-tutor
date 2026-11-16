"""Lote 7c (rodada A2, issue #34): objetos API e funcionalidades do tema Execução assíncrona, lotes e agendamento.

Cadastra três objetos API lidos da Object Reference versionada 264.0 (AsyncApexJob, CronTrigger e CronJobDetail), dois
relacionamentos entre eles e cinco funcionalidades (Batch Apex, Queueable Apex, Future methods, Apex agendado e monitoramento
de jobs Apex). Liga Flow aos temas de agendamento e de caminhos assíncronos. O tema não tem metadata type próprio novo: as
opções da org ficam em ApexSettings (lote 7b).

As fontes de Ajuda e dos guias citadas pelas funcionalidades são registradas por conteudo_temas.py (lista em conteudo_detalhe.py).
Ordem: lote7b_desenvolvimento.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7c_assincrono.py
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import obj as O                    # noqa: E402
from carga.base import af, ev                 # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-16"
EXTR = "fontes/extracoes/objref-lote7c-assincrono.txt"
C.registrar_fontes([C.fonte_objref(n, EXTR, DATA) for n in ("AsyncApexJob", "CronTrigger", "CronJobDetail")])

S_JOB, S_CRON, S_DET = "src:objref-asyncapexjob", "src:objref-crontrigger", "src:objref-cronjobdetail"
CHAMADAS = ["describeSObjects()", "query()", "retrieve()"]
TOOL_D = lambda: O.expo("tooling", "desconhecido", nota="Exposição na Tooling API não verificada.")  # noqa: E731
LISTA = "Valores listados na página."

# ================================================================ AsyncApexJob
J = "obj:AsyncApexJob"
job = [
    O.field(J, "ApexClassId", "reference", "FGNS", None, "Id da classe Apex que executa o job.", S_JOB, ref=["ApexClass"], rel="ApexClass"),
    O.field(J, "CompletedDate", "dateTime", "FNS", None, "Data e hora em que o job terminou.", S_JOB),
    O.field(J, "CronTriggerId", "reference", "FGNS", "53.0", "Id do CronTrigger. Preenchido só em jobs de Apex agendado.", S_JOB,
            ref=["obj:CronTrigger"], rel="CronTrigger"),
    O.field(J, "ExtendedStatus", "string", "FGNS", "19.0", "Descrição curta do primeiro erro ocorrido no batch.", S_JOB),
    O.field(J, "JobItemsProcessed", "int", "FGS", None, "Quantos itens do job já foram processados (na tela, Batches Processed).", S_JOB),
    O.field(J, "JobType", "picklist", "FGRS", None, "Tipo do job.", S_JOB, completa="sim", contexto=LISTA, vals=[
        "ApexToken", "BatchApex", "BatchApexWorker", "Future", "Queueable", "ScheduledApex", "SharingRecalculation", "TestRequest", "TestWorker"]),
    O.field(J, "LastProcessed", "string", "FGNS", None, "Último Id processado e confirmado.", S_JOB),
    O.field(J, "LastProcessedOffset", "int", "FGNS", None, "Deslocamento do último Id processado e confirmado.", S_JOB),
    O.field(J, "MethodName", "string", "FGNS", None, "Nome do método Apex em execução (na tela, Apex Method).", S_JOB),
    O.field(J, "NumberOfErrors", "int", "FGNS", None, "Número de lotes que falharam (na tela, Failures).", S_JOB),
    O.field(J, "ParentJobId", "reference", "FGNS", None, "Id do job pai, nos jobs filhos de um batch dividido em chunks. Vazio nos demais.", S_JOB,
            notas=["A página não informa o objeto referenciado."]),
    O.field(J, "Status", "picklist", "FGRS", None, "Estado do job.", S_JOB, completa="sim",
            contexto=LISTA + " Holding só vale para jobs de batch que estão na Apex flex queue.",
            vals=["Aborted", "Completed", "Failed", "Holding", "Preparing", "Processing", "Queued"]),
    O.field(J, "TotalJobItems", "int", "FGNS", None, "Total de lotes do job (na tela, Total Batches).", S_JOB),
]
O.obj("AsyncApexJob",
      "O registro de um job Apex: batch, future method, Queueable, Apex agendado ou recálculo de sharing. Mostra o tipo, o estado e o andamento.",
      "Consultar, por API ou por SOQL, o que a página Apex Jobs mostra: que jobs rodaram, em que estado estão e quantos lotes falharam.",
      [O.expo("padrao", "verificado", S_JOB, CHAMADAS,
              acesso="Quando o Apex não roda em system mode, exige a permissão View Setup and Configuration para acessar o objeto e enfileirar jobs.",
              nota="A página não informa a versão de entrada do objeto."), TOOL_D()],
      job,
      [{"api": "padrao", "soql": "SELECT JobType, Status, NumberOfErrors, JobItemsProcessed, TotalJobItems, CompletedDate FROM AsyncApexJob "
                                 "WHERE JobType = 'BatchApex' AND Status = 'Failed'",
        "contexto": "API padrão. Lista os jobs de batch que falharam.", "validacao": "documental"}],
      O.APEX_OK(S_JOB), O.cob("completa", 13, 13, O.cnt(job), "Tabela de campos lida completa (13); Id não consta."), S_JOB,
      alertas=["BatchApexWorker e TestWorker são tipos de uso interno: ao consultar o estado de um batch, filtre BatchApexWorker para não ver entradas repetidas.",
               "A página Apex Jobs só lista os jobs dos últimos sete dias; os mais antigos se consultam por este objeto."])

# ================================================================ CronTrigger
T = "obj:CronTrigger"
cron = [
    O.field(T, "CronExpression", "string", "FGNS", None, "Expressão cron que dispara a agenda, dos segundos até o ano (opcional).", S_CRON),
    O.field(T, "CronJobDetailId", "reference", "FGNS", None, "Id do CronJobDetail, que traz o nome e o tipo do job.", S_CRON,
            ref=["obj:CronJobDetail"], rel="CronJobDetail"),
    O.field(T, "EndTime", "dateTime", "FNS", None, "Quando o job terminou ou vai terminar.", S_CRON),
    O.field(T, "NextFireTime", "dateTime", "FNS", None, "Próxima execução agendada. Nulo se o job não vai rodar de novo.", S_CRON),
    O.field(T, "OwnerId", "reference", "FGNS", None, "Dono do job.", S_CRON, notas=["A página não informa o objeto referenciado."]),
    O.field(T, "PreviousFireTime", "dateTime", "FNS", None, "Execução mais recente. Nulo se o job ainda não rodou.", S_CRON),
    O.field(T, "StartTime", "dateTime", "FNS", None, "Início da iteração mais recente do job.", S_CRON),
    O.field(T, "State", "string", "FGNS", None, "Estado do job, gerido pelo sistema.", S_CRON, completa="sim",
            contexto="A página lista estes valores para um campo do tipo string.",
            vals=["WAITING", "ACQUIRED", "EXECUTING", "COMPLETE", "ERROR", "DELETED", "PAUSED", "BLOCKED", "PAUSED_BLOCKED"]),
    O.field(T, "TimesTriggered", "int", "FGNS", None, "Quantas vezes o job foi disparado.", S_CRON),
    O.field(T, "TimeZoneSidKey", "picklist", "FGNRS", None, "Id do fuso horário do job, como America/Los_Angeles.", S_CRON),
]
O.obj("CronTrigger",
      "A agenda de um job agendado: a expressão cron, a próxima e a última execução e o estado. Parecido com um cron job de UNIX.",
      "Consultar os jobs agendados da org: quando cada um roda de novo, quantas vezes já rodou e em que estado está.",
      [O.expo("padrao", "verificado", S_CRON, CHAMADAS, desde="17.0"), TOOL_D()],
      cron,
      [{"api": "padrao", "soql": "SELECT CronExpression, State, NextFireTime, PreviousFireTime, TimesTriggered FROM CronTrigger "
                                 "WHERE State = 'WAITING' ORDER BY NextFireTime",
        "contexto": "API padrão. Lista os jobs que aguardam a próxima execução.", "validacao": "documental"}],
      O.APEX_OK(S_CRON), O.cob("completa", 10, 10, O.cnt(cron), "Tabela de campos lida completa (10); Id não consta."), S_CRON,
      alertas=["O objeto guarda todos os tipos de job agendado, não só Apex: o tipo fica em CronJobDetail.JobType."])

# ================================================================ CronJobDetail
D = "obj:CronJobDetail"
TIPOS = "1 Data Export; 3 Dashboard Refresh; 4 Reporting Snapshot; 6 Scheduled Flow; 7 Scheduled Apex; 8 Report Run; 9 Batch Job; A Reporting Notification."
det = [
    O.field(D, "JobType", "picklist", "FGNRS", None, "Tipo do job agendado, em código. Use o código para filtrar um tipo.", S_DET, completa="sim",
            contexto="Códigos e significados na página: " + TIPOS, vals=["1", "3", "4", "6", "7", "8", "9", "A"]),
    O.field(D, "Name", "string", "FGIS", None, "Nome do job agendado.", S_DET),
]
O.obj("CronJobDetail",
      "Os detalhes de um job agendado: o nome e o tipo (Apex agendado, flow agendado, atualização de dashboard e outros).",
      "Distinguir os tipos de job agendado ao consultar CronTrigger: por exemplo, contar quantos jobs de Apex agendado existem.",
      [O.expo("padrao", "verificado", S_DET, CHAMADAS, desde="29.0"), TOOL_D()],
      det,
      [{"api": "padrao", "soql": "SELECT Name, JobType FROM CronJobDetail WHERE JobType = '7'",
        "contexto": "API padrão. O código 7 corresponde a Scheduled Apex.", "validacao": "documental"}],
      O.APEX_OK(S_DET), O.cob("completa", 2, 2, O.cnt(det), "Tabela de campos lida completa (2); Id não consta."), S_DET)

C.rel_lookup("asyncapexjob-crontrigger", J, "CronTriggerId", T, "Um job de Apex agendado aponta para a agenda que o disparou.", S_JOB)
C.rel_lookup("crontrigger-cronjobdetail", T, "CronJobDetailId", D, "Cada agenda aponta para o detalhe do job, com o nome e o tipo.", S_CRON)

# ================================================================ funcionalidades
ASS = "execucao-assincrona-lotes-e-agendamento"
DEV = "desenvolvimento-testes-e-entrega"
S_APEXSET = "src:mdapi-apexsettings"
SEM_MDT = {"tipo": "metadata_type", "estado": "nao_aplicavel",
           "motivo": "O recurso é código Apex: a classe que o implementa é um componente ApexClass. Não há metadata type próprio do mecanismo."}
CODIGO = [("codigo-e-bundles", "É código Apex e segue as regras de teste e de implantação.")]


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


def sec(pares):
    return [(DEV, s, m) for s, m in pares]


C.funcionalidade(
    "batch-apex", "Batch Apex", "Batch Apex", ["batch", "database.batchable", "executebatch", "job em lote", "apex flex queue"],
    "Forma de processar um volume grande de registros em Apex: a classe coleta os registros e a plataforma os entrega em lotes, um de cada "
    "vez, cada lote com os próprios limites.",
    "Processar o que não cabe numa transação só, como recalcular um campo em todas as contas.",
    "Um batch recalcula a classificação de todas as contas em lotes de 200; o registro do job mostra quantos lotes já rodaram e quantos falharam.",
    (ASS, "batch"), sec(CODIGO),
    [("ApexClass", "A classe que implementa Database.Batchable.")],
    [("AsyncApexJob", "Registro de cada job de batch, com estado e andamento.")],
    ["src:apex-batch-use", "src:apex-batch", "src:apexref-database", "src:help-apex-flex-queue", S_JOB], [],
    setup("Setup > Quick Find: Apex Jobs > Apex Jobs", "src:apex-batch-use", "Página para acompanhar ou parar um job de batch."),
    limitacoes=["Até cinco jobs de batch em fila ou ativos ao mesmo tempo; a Apex flex queue segura até 100 outros em Holding.",
                "Tamanho do lote: 200 por padrão; até 2.000 quando o método start devolve um QueryLocator.",
                "Em 24 horas: 250.000 execuções de método de batch, ou licenças de usuário vezes 200, o que for maior."],
    alertas=["As execuções de start, execute e finish contam no limite de 24 horas.",
             "Com a flex queue cheia, Database.executeBatch lança uma exceção de limite e o job não entra."])

C.funcionalidade(
    "queueable-apex", "Queueable Apex", "Queueable Apex", ["queueable", "system.enqueuejob", "job enfileirado", "encadeamento de jobs"],
    "Forma de enfileirar um trabalho em Apex para rodar em segundo plano. Devolve o Id do job, aceita tipos complexos como parâmetro e "
    "permite encadear um job a outro.",
    "Tirar da transação principal uma operação demorada, como um callout, com como acompanhá-la.",
    "Depois de salvar um pedido, um job enfileirado chama o sistema de estoque; ao terminar, enfileira o job que avisa a transportadora.",
    (ASS, "queueable"), sec(CODIGO),
    [("ApexClass", "A classe que implementa Queueable."),
     ("ApexSettings", "Opções da org para Apex assíncrono, como o atraso mínimo padrão dos jobs enfileirados (DefaultQueueableDelay).")],
    [("AsyncApexJob", "Registro de cada job enfileirado.")],
    ["src:apex-queueable", "src:apexref-system", "src:apex-gov-limits", "src:apex-async-overview", S_APEXSET, S_JOB], [],
    af("desconhecido", None, "Caminho de Setup do atraso padrão não confirmado nas fontes lidas.", []),
    limitacoes=["Jobs adicionados com System.enqueueJob por transação: 50 no contexto síncrono e 1 no assíncrono.",
                "Atraso mínimo ao enfileirar: de 0 a 10 minutos.",
                "Em orgs Developer Edition e Trial, a profundidade máxima da pilha de jobs encadeados é 5."],
    alertas=["Numa cadeia de jobs, crie um mecanismo para frear ou parar; sem ele, chega-se rápido ao limite diário de Apex assíncrono."])

C.funcionalidade(
    "future-methods", "Future methods", "Future Methods", ["@future", "future method", "método future", "future annotation"],
    "Métodos Apex marcados com a anotação Future, que rodam em segundo plano quando há recursos. A documentação diz que Queueable cobre os "
    "mesmos usos e oferece mais: Id do job, tipos não primitivos e encadeamento.",
    "Manter código que já usa o mecanismo; para código novo, a documentação indica Queueable.",
    "Um método future faz um callout depois de um trigger, para não segurar a gravação do registro.",
    (ASS, "future-e-mecanismos-legados"), sec(CODIGO),
    [("ApexClass", "A classe que contém o método anotado.")],
    [("AsyncApexJob", "Registro de cada execução future.")],
    ["src:apex-future", "src:apex-queueable", "src:apex-async-overview", S_JOB], [],
    af("nao_aplicavel", None, "Não há tela de Setup para criar um future method: ele é declarado no código.", []),
    limitacoes=["O método precisa ser static e void; os parâmetros são tipos primitivos, arrays ou coleções de primitivos.",
                "Não se chama um future method a partir de um batch ou de outro future; em contexto queueable, até 50 por invocação.",
                "Em 24 horas: 250.000 execuções, ou licenças de usuário vezes 200, o que for maior."],
    alertas=["Não aceita sObjects nem objetos como parâmetro."])

C.funcionalidade(
    "apex-agendado", "Apex agendado", "Scheduled Apex", ["scheduled apex", "apex scheduler", "schedulable", "system.schedule", "cron expression",
                                                       "job agendado"],
    "Classe Apex que roda em horário definido. A classe implementa a interface Schedulable e é agendada pela tela Schedule Apex ou por "
    "código, com uma expressão cron.",
    "Rodar rotinas periódicas, como uma manutenção diária ou semanal, muitas vezes iniciando um batch.",
    "Toda madrugada, uma classe agendada inicia o batch que recalcula a classificação das contas.",
    (ASS, "agendamento"), sec(CODIGO),
    [("ApexClass", "A classe que implementa Schedulable.")],
    [("CronTrigger", "A agenda de cada job agendado."), ("CronJobDetail", "Nome e tipo de cada job agendado."),
     ("AsyncApexJob", "Registro do job de Apex agendado.")],
    ["src:apex-scheduler", "src:help-schedule-apex", "src:apexref-system", "src:apex-gov-limits", S_CRON, S_DET], [],
    setup("Setup > Quick Find: Apex Classes > Apex Classes > Schedule Apex", "src:help-schedule-apex", "Tela para agendar uma classe."),
    limitacoes=["Até 100 jobs de Apex agendado ao mesmo tempo.",
                "Em 24 horas: 250.000 execuções, ou licenças de usuário vezes 200, o que for maior.",
                "Embora assíncrono, o Apex agendado usa os limites síncronos por transação."],
    alertas=["O agendador roda como system: a classe executa, tenha ou não o usuário permissão para executá-la.",
             "A execução real pode atrasar em relação ao horário agendado, conforme a disponibilidade do serviço.",
             "Com um job agendado ativo, a classe e as que ela referencia não podem ser atualizadas pela interface."])

C.funcionalidade(
    "monitoramento-de-jobs-apex", "Monitoramento de jobs Apex", "Apex Jobs, Apex Flex Queue and Scheduled Jobs",
    ["apex jobs", "apex flex queue", "scheduled jobs", "all scheduled jobs", "fila de jobs", "async apex limit"],
    "As telas do Setup e os objetos API que mostram os jobs assíncronos: Apex Jobs lista os jobs e o uso do limite de 24 horas; Apex Flex "
    "Queue, os batches em espera; Scheduled Jobs, os jobs agendados.",
    "Saber o que está rodando, o que falhou e quanto do limite diário já foi usado, antes que jobs novos sejam rejeitados.",
    "O administrador vê na página Apex Jobs que um batch falhou em três lotes e que a org já usou boa parte do limite de 24 horas.",
    (ASS, "monitoramento-de-jobs-e-limites"), [], [],
    [("AsyncApexJob", "Os jobs Apex, com tipo, estado e andamento."), ("CronTrigger", "As agendas dos jobs agendados."),
     ("CronJobDetail", "Nome e tipo dos jobs agendados.")],
    ["src:help-apex-job-queue", "src:help-apex-flex-queue", "src:help-apex-code-overview", "src:help-org-health", "src:help-kb-asyncapexjob-types",
     "src:rest-limits", "src:apex-elastic-limits", S_JOB, S_CRON, S_DET],
    [{"tipo": "metadata_type", "estado": "nao_aplicavel", "motivo": "São telas de acompanhamento e registros de execução, não configuração implantável."}],
    setup("Setup > Quick Find: Apex Jobs > Apex Jobs", "src:apex-batch-use", "Lista de jobs Apex. As outras duas telas são Apex Flex Queue e Scheduled Jobs."),
    limitacoes=["A página Apex Jobs lista só os jobs submetidos nos últimos sete dias."],
    alertas=["Future methods e classes Queueable ainda não executados aparecem como Future na coluna Job Type.",
             "Um job agendado aparece em Apex Jobs e em All Scheduled Jobs, mas conta uma vez só no limite.",
             "Acima do limite de 24 horas de jobs assíncronos ou do limite de jobs agendados, jobs novos são rejeitados."])

# Ligações com o que já existia
C.secundaria("flow", ASS, "agendamento", "Schedule-triggered flows e scheduled paths rodam em horário definido.",
             srcs=["src:help-flow-schedule-triggered", "src:help-flow-scheduled-paths"])
C.secundaria("flow", ASS, "caminhos-assincronos", "O caminho assíncrono de um record-triggered flow roda depois que a gravação é confirmada.",
             srcs=["src:help-rtf-considerations"])
C.ampliar_funcionalidade("classes-apex", objs=[("AsyncApexJob", "Registro dos jobs assíncronos que executam classes Apex.")], srcs=[S_JOB],
                         remover_ausencia_de="objeto_api")

print("lote 7c: 3 objetos API, 2 relacionamentos e 5 funcionalidades gravados; flow e classes-apex ampliadas")
