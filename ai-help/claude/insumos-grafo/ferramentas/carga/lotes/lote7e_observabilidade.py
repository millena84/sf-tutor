"""Lote 7e (rodada A4, issue #34): objetos API e funcionalidades do tema Observabilidade, auditoria e operação.

Cadastra SetupAuditTrail e EventLogFile (Object Reference versionada 264.0) e três funcionalidades: logs de depuração, Setup
Audit Trail e Event Monitoring. Liga o monitoramento de jobs Apex ao tema de jobs e diagnóstico.

Ordem: lote7d_interface.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7e_observabilidade.py
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import obj as O                    # noqa: E402
from carga.base import af, ev                 # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-16"
EXTR = "fontes/extracoes/objref-lote7c-assincrono.txt"
C.registrar_fontes([C.fonte_objref(n, EXTR, DATA) for n in ("SetupAuditTrail", "EventLogFile")])
S_SAT, S_ELF = "src:objref-setupaudittrail", "src:objref-eventlogfile"
TOOL_D = lambda: O.expo("tooling", "desconhecido", nota="Exposição na Tooling API não verificada.")  # noqa: E731

A = "obj:SetupAuditTrail"
sat = [
    O.field(A, "Action", "string", "FS", None, "Categoria da mudança de Setup, como PermSetCreate (criação de permission set). Os detalhes ficam em Display.", S_SAT),
    O.field(A, "CreatedByContext", "string", "FGNS", "48.0", "Contexto em que a mudança foi feita.", S_SAT),
    O.field(A, "CreatedByIssuer", "string", "FGNS", None, "Reservado para uso futuro.", S_SAT),
    O.field(A, "DelegateUser", "string", "FNS", "35.0", "Usuário de Login-As que fez a mudança. Vazio quando não houve.", S_SAT),
    O.field(A, "Display", "string", "NS", None, "Descrição completa da mudança de Setup.", S_SAT),
    O.field(A, "Section", "string", "NS", None, "Seção do menu de Setup em que a ação ocorreu, como Manage Users.", S_SAT),
]
O.obj("SetupAuditTrail",
      "O registro das mudanças feitas no Setup pelos administradores: o que mudou, em que seção e por quem, por ao menos os últimos 180 dias.",
      "Consultar por API o que a tela View Setup Audit Trail mostra, para auditoria e investigação.",
      [O.expo("padrao", "verificado", S_SAT, ["query()", "retrieve()"], desde="15.0",
              restr=["Não aceita consultas agregadas: SELECT count() funciona, SELECT count(Id) falha."]), TOOL_D()],
      sat,
      [{"api": "padrao", "soql": "SELECT Action, Section, Display, DelegateUser FROM SetupAuditTrail WHERE Section = 'Manage Users'",
        "contexto": "API padrão. Manage Users é o exemplo de seção dado na página.", "validacao": "documental"}],
      O.APEX_OK(S_SAT), O.cob("completa", 6, 6, O.cnt(sat), "Tabela de campos lida completa (6); Id e campos de sistema não constam."), S_SAT,
      alertas=["Depois de 180 dias, os registros são apagados: para guardar por mais tempo, é preciso exportar.",
               "Mudanças de permissões de usuário feitas por change set não aparecem no Setup Audit Trail.",
               "Não serve de standard controller em páginas Visualforce."])

L = "obj:EventLogFile"
elf = [
    O.field(L, "ApiVersion", "double", "FS", "30.0", "Versão da API do arquivo de log.", S_ELF),
    O.field(L, "EventType", "picklist", "FGRS", None, "Tipo de evento, que define o esquema do arquivo. Exemplos: API, Login, Report, URI.", S_ELF,
            notas=["A lista completa de tipos de evento fica em outra página, não lida."]),
    O.field(L, "LogDate", "dateTime", "FS", None, "Data do arquivo. Arquivos diários cobrem 24 horas em UTC; os horários, uma hora.", S_ELF),
    O.field(L, "LogFile", "base64", "", None, "Conteúdo do arquivo .csv, em base64.", S_ELF),
    O.field(L, "LogFileContentType", "string", "FGS", None, "Tipo de conteúdo do arquivo; sempre .csv.", S_ELF),
    O.field(L, "LogFileFieldNames", "string", "N", None, "Lista ordenada dos nomes dos campos do log. Varia por EventType.", S_ELF),
    O.field(L, "LogFileFieldTypes", "string", "N", None, "Lista ordenada dos tipos dos campos do log. Varia por EventType.", S_ELF),
    O.field(L, "LogFileLength", "double", "FS", None, "Tamanho do arquivo em bytes.", S_ELF),
]
O.obj("EventLogFile",
      "Um arquivo de log de eventos do Event Monitoring: um .csv por tipo de evento e período, com o uso e o desempenho da org.",
      "Baixar os logs de eventos por API para analisar uso, desempenho e segurança.",
      [O.expo("padrao", "verificado", S_ELF, ["describeSObjects()", "query()", "retrieve()"], desde="32.0",
              acesso="Exige as permissões View Event Log Files e API Enabled; quem tem View All Data também vê."), TOOL_D()],
      elf,
      [{"api": "padrao", "soql": "SELECT EventType, LogDate, LogFileLength FROM EventLogFile WHERE EventType = 'Login' ORDER BY LogDate",
        "contexto": "API padrão. Login é um dos tipos de evento citados na página.", "validacao": "documental"}],
      O.APEX_OK(S_ELF), O.cob("parcial", None, 8, O.cnt(elf), "A tabela tem 8 linhas, todas cadastradas; a introdução da página cita Interval e Sequence "
                                                           "(API 37.0), que não têm linha na tabela."), S_ELF,
      alertas=["O esquema de cada tipo de log pode mudar a cada release: confira LogFileFieldNames e LogFileFieldTypes.",
               "Os arquivos não contam no armazenamento de dados nem de arquivos da org.",
               "A retenção depende da edição e da licença: sem o add-on, 1 dia."])

OBS = "observabilidade-auditoria-e-operacao"
NAO_IMPLANTAVEL = {"tipo": "metadata_type", "estado": "nao_aplicavel", "motivo": "É registro de execução e tela de acompanhamento, não configuração implantável."}


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


C.funcionalidade(
    "debug-logs", "Logs de depuração", "Debug Logs", ["debug log", "trace flag", "debug level", "developer console", "log de depuração"],
    "Registros detalhados do que a plataforma executou numa requisição: banco de dados, Apex, workflow, validações e callouts. Um log só é "
    "gerado para quem tem uma trace flag ativa, que diz de quem coletar, por quanto tempo e com que nível de detalhe.",
    "Investigar por que uma automação ou um trecho de código se comportou de certo jeito.",
    "Para entender um erro que só acontece com uma usuária, o administrador cria uma trace flag para ela, reproduz o erro e lê o log.",
    (OBS, "logs-e-rastreamento"), [], [], [],
    ["src:apex-debug-log", "src:help-debug-logs", "src:help-debug-setup", "src:help-devconsole-logs", "src:help-kb-traceflags-prod"],
    [NAO_IMPLANTAVEL, {"tipo": "objeto_api", "estado": "desconhecido",
                       "motivo": "A Ajuda cita os objetos TraceFlag e DebugLevel, da Tooling API; não foram lidos nem cadastrados."}],
    setup("Setup > Quick Find: Debug Logs > Debug Logs", "src:help-devconsole-logs", "Página em que se criam as trace flags de usuário."),
    limitacoes=["Cada log tem até 20 MB; ao chegar ao limite, as entradas mais antigas são apagadas.",
                "Logs de depuração do sistema ficam guardados por 24 horas.",
                "O armazenamento padrão de logs de depuração é de 1.000 MB."],
    alertas=["Trace flags de classe e de trigger mudam o nível de detalhe, mas sozinhas não fazem um log ser gerado.",
             "Apagar um debug level apaga as trace flags que o usam.",
             "Em produção, evite trace flags em usuários de API e em código de alto volume."])

C.funcionalidade(
    "setup-audit-trail", "Setup Audit Trail", "Setup Audit Trail", ["view setup audit trail", "auditoria de setup", "histórico de configuração"],
    "O histórico das mudanças feitas no Setup: o que mudou, quando, em que seção e por quem. A tela mostra as 20 mais recentes e permite "
    "baixar os últimos 180 dias.",
    "Saber quem alterou uma configuração, o que é especialmente útil quando há vários administradores.",
    "Um perfil ganhou uma permissão inesperada; o Setup Audit Trail mostra que administrador a concedeu e em que dia.",
    (OBS, "auditoria-de-configuracao"), [], [],
    [("SetupAuditTrail", "As mudanças de Setup, consultáveis por API.")],
    ["src:help-setup-audit-trail", "src:help-security-audit", "src:help-kb-audit-changesets", S_SAT], [NAO_IMPLANTAVEL],
    setup("Setup > Quick Find: View Setup Audit Trail", "src:help-setup-audit-trail", "Lista das 20 mudanças mais recentes; Download baixa 180 dias."),
    limitacoes=["Depois de 180 dias, os registros são apagados."],
    alertas=["Mudanças de permissões de usuário feitas por change set não são registradas.",
             "Para ver o histórico, é preciso a permissão View Setup and Configuration."])

C.funcionalidade(
    "event-monitoring", "Event Monitoring", "Event Monitoring", ["event log file", "eventlogfile", "real-time event monitoring", "event log file browser",
                                                              "salesforce shield", "elf"],
    "Dados detalhados de uso, desempenho e segurança da org. Os arquivos de log de eventos saem por tipo de evento e período, em .csv; o "
    "Real-Time Event Monitoring publica eventos de acesso e de segurança no momento em que acontecem.",
    "Entender como a org é usada e investigar incidentes de segurança ou de desempenho.",
    "A equipe de segurança baixa os logs do tipo Report para ver quem exportou relatórios numa semana.",
    (OBS, "eventos-de-monitoramento"), [], [],
    [("EventLogFile", "Os arquivos de log de eventos, consultáveis por API.")],
    ["src:help-event-monitoring", "src:help-em-enable", "src:help-kb-em-faq", "src:help-kb-rtem-faq", "src:help-rn-elf-browser", S_ELF],
    [{"tipo": "metadata_type", "estado": "desconhecido", "motivo": "Metadata types de configuração do Event Monitoring não investigados."}],
    setup("Setup > Quick Find: Event Log File Browser", "src:help-rn-elf-browser", "Tela para escolher o período e baixar os arquivos em CSV."),
    limitacoes=["Retenção dos arquivos de log: 1 dia sem o add-on; com o add-on, 30 dias por padrão, extensíveis a 1 ano.",
                "O conjunto completo de tipos de evento exige Salesforce Shield ou o add-on Event Monitoring."],
    alertas=["Event Monitoring e Real-Time Event Monitoring guardam coisas diferentes: o primeiro usa o objeto EventLogFile; o segundo, não.",
             "O esquema de um arquivo de log pode mudar a cada release."])

C.secundaria("monitoramento-de-jobs-apex", OBS, "jobs-incidentes-e-diagnostico", "As telas de jobs Apex servem para acompanhar e investigar execuções.",
             srcs=["src:help-apex-job-queue"])
print("lote 7e: 2 objetos API e 3 funcionalidades gravados; monitoramento-de-jobs-apex ligado a Observabilidade")
