"""Lote 7j (fecho da rodada A4, issue #34): o que faltava no tema Observabilidade, auditoria e operação.

Cadastra os objetos da Tooling API TraceFlag, DebugLevel e ApexLog (guia versionado 264.0) e cria as funcionalidades
system-overview, armazenamento-de-dados-e-arquivos e transaction-security. Liga os objetos aos logs de depuração e os limites
de API ao tema Limites e consumo.

Ordem: lote7i_interface_fecho.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7j_observabilidade_fecho.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import obj as O                    # noqa: E402
from carga.base import af, ev, caminho        # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-16"
EXTR = "fontes/extracoes/lote7j-observabilidade-fecho.txt"
BASE = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_tooling.meta/api_tooling/tooling_api_objects_"


def substituir_fontes(novas):
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


substituir_fontes([C.fonte(f"src:tooling-{n.lower()}", f"{n} (Tooling API)", BASE + n.lower() + ".htm", f"Chamadas e campos do objeto {n} na Tooling API.",
                           EXTR, DATA) for n in ("TraceFlag", "DebugLevel", "ApexLog")])
S_TF, S_DL, S_AL = "src:tooling-traceflag", "src:tooling-debuglevel", "src:tooling-apexlog"
T = ("tooling",)
NIVEIS = ["NONE", "ERROR", "WARN", "INFO", "DEBUG", "FINE", "FINER", "FINEST"]
SIM = ("sim", None)
PADRAO_D = lambda: O.expo("padrao", "desconhecido", nota="Exposição na API padrão não verificada; não presumir.")  # noqa: E731
APEX_D = {"consulta_soql_direta": af("desconhecido", None, "Não verificado se o objeto também é consultável por SOQL comum em Apex."),
          "nota": "Página lida só na Tooling API."}
SEM_VERSAO = "A página não informa a versão de entrada do objeto."
END = "/services/data/v68.0/tooling/query?q=..."
CRUD = ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "update()", "upsert()"]
REST = ["Query", "GET", "POST", "PATCH", "DELETE"]


def nivel(obj, nome, desc, src, props="CFGRSU", req=SIM, **k):
    return O.field(obj, nome, "picklist", props, None, desc, src, apis=T, vals=NIVEIS, completa="sim", req=req, **k)


# ================================================================ TraceFlag
F = "obj:TraceFlag"
CATS = [("ApexCode", "do código Apex"), ("ApexProfiling", "das informações de profiling"), ("Callout", "dos callouts externos"),
        ("Database", "da atividade de banco de dados"), ("System", "das chamadas a métodos de sistema"), ("Validation", "das validation rules"),
        ("Visualforce", "do Visualforce"), ("Workflow", "das workflow rules")]
tf = [nivel(F, n, f"Nível de detalhe do log {d}.", S_TF) for n, d in CATS] + [
    O.field(F, "DebugLevelId", "reference", "CFGNSU", None, "O debug level atribuído a esta trace flag; um debug level pode servir a várias.", S_TF,
            apis=T, ref=["obj:DebugLevel"]),
    O.field(F, "ExpirationDate", "dateTime", "CFSU", None, "Data e hora em que a trace flag expira; no máximo 24 horas depois de StartDate.", S_TF,
            apis=T, req=SIM),
    O.field(F, "LogType", "picklist", "CFGRS", None, "Tipo de log.", S_TF, apis=T, completa="sim", req=SIM,
            vals=["CLASS_TRACING", "DEVELOPER_LOG", "PROFILING", "USER_DEBUG"],
            notas=["USER_DEBUG: log de um usuário. CLASS_TRACING: troca o nível de log de uma classe ou trigger, sem gerar log.",
                   "PROFILING: reservado para uso futuro."]),
    O.field(F, "ScopeId", "reference", "CFGNSU", None, "Descontinuado (API 34.0 e anteriores); apontava um usuário, junto com TracedEntityId.", S_TF,
            apis=T, ate="34.0", notas=["A página não informa formalmente o objeto referenciado."]),
    O.field(F, "StartDate", "dateTime", "CFGNSU", None, "Quando a trace flag começa a valer; nulo significa agora.", S_TF, apis=T),
    O.field(F, "TracedEntityId", "reference", "CFGSU", None, "O que é rastreado: uma classe Apex, um trigger Apex ou um usuário.", S_TF, apis=T,
            ref=["ApexClass", "ApexTrigger", "obj:User"], req=SIM),
]
tf.sort(key=lambda c: c["nome"])
O.obj("TraceFlag",
      "Uma trace flag: o que faz um log de depuração ser gerado, para quem, por quanto tempo e com que nível de detalhe.",
      "Criar, consultar e remover trace flags por API, em vez de pela tela Debug Logs.",
      [O.expo("tooling", "verificado", S_TF, CRUD, rest=REST, nota=SEM_VERSAO), PADRAO_D()],
      tf,
      [{"api": "tooling", "soql": "SELECT TracedEntityId, LogType, StartDate, ExpirationDate, DebugLevelId FROM TraceFlag WHERE LogType = 'USER_DEBUG'",
        "endpoint": END, "contexto": "Tooling API. Lista as trace flags de usuário.", "validacao": "documental"}],
      APEX_D, O.cob("completa", 14, 14, O.cnt(tf), "Tabela de campos lida completa (14); Id e campos de sistema não constam."), S_TF,
      alertas=["Para registrar o log de um usuário: LogType USER_DEBUG e TracedEntityId com o Id do usuário. Só funciona para usuários.",
               "Com CLASS_TRACING, a trace flag troca o nível de log de uma classe ou trigger, mas não gera nem guarda log.",
               "A expiração precisa cair em menos de 24 horas depois do início."])

# ================================================================ DebugLevel
D = "obj:DebugLevel"
DCATS = [("ApexCode", "Código Apex, DML, consultas, triggers e testes."), ("ApexProfiling", "Dados de profiling, como limites da org e e-mails enviados."),
         ("Callout", "Chamadas a serviços externos, com o XML de requisição e resposta."),
         ("Database", "Operações de banco de dados, inclusive DML e consultas SOQL e SOSL."),
         ("System", "Chamadas a métodos de sistema, como System.debug."), ("Validation", "Validation rules: nome da regra e resultado."),
         ("Visualforce", "Eventos de Visualforce, como view state e avaliação de fórmulas."), ("Workflow", "Workflow rules: nome da regra e ações executadas.")]
dl = [nivel(D, n, "Nível de log da categoria. " + d, S_DL) for n, d in DCATS] + [
    nivel(D, "dataAccess", "Nível de log das regras e políticas de objetos acessados pela interface, para explicar por que um objeto está inacessível.",
          S_DL, req=None, notas=["A página tipa o campo como ApexLogLevel e escreve o nome com inicial minúscula."]),
    nivel(D, "nba", "Nível de log do Einstein Next Best Action, inclusive a execução de estratégias.", S_DL, req=None,
          notas=["A página tipa o campo como ApexLogLevel e escreve o nome com inicial minúscula."]),
    nivel(D, "Wave", "Nível de log do CRM Analytics, como erros de processamento de templates.", S_DL, req=None,
          notas=["A página tipa o campo como ApexLogLevel."]),
    O.field(D, "DeveloperName", "string", "FGS", None, "Nome interno do debug level, mostrado no Developer Console e no Setup.", S_DL, apis=T),
    O.field(D, "Language", "picklist", "CDFGNRSU", None, "Idioma do MasterLabel.", S_DL, apis=T, completa="desconhecido",
            vals=["zh_CN", "zh_TW", "da", "nl_NL", "en_US", "fi", "fr", "de", "it", "ja", "ko", "no", "pt_BR", "ru", "es", "es_MX", "sv", "th"]),
    O.field(D, "MasterLabel", "string", "FGS", None, "Reservado para uso futuro, mas obrigatório; a página sugere repetir o DeveloperName.", S_DL,
            apis=T, req=SIM),
]
dl.sort(key=lambda c: c["nome"].lower())
O.obj("DebugLevel",
      "Um debug level: um conjunto de níveis de log por categoria, que pode ser atribuído a várias trace flags.",
      "Criar e consultar por API os debug levels usados pelas trace flags.",
      [O.expo("tooling", "verificado", S_DL, CRUD, rest=REST, nota=SEM_VERSAO), PADRAO_D()],
      dl,
      [{"api": "tooling", "soql": "SELECT DeveloperName, ApexCode, Database, Workflow FROM DebugLevel", "endpoint": END,
        "contexto": "Tooling API. Lista os debug levels e três das categorias.", "validacao": "documental"}],
      APEX_D, O.cob("completa", 14, 14, O.cnt(dl), "Tabela de campos lida completa (14); Id e campos de sistema não constam."), S_DL,
      alertas=["Excluir um debug level exclui todas as trace flags que o usam."])

# ================================================================ ApexLog
A = "obj:ApexLog"
al = [
    O.field(A, "Application", "textarea", "FGS", None, "Para clientes de API, o Id do cliente; para o navegador, o valor Browser.", S_AL, apis=T, req=SIM),
    O.field(A, "DurationMilliseconds", "int", "FGS", None, "Duração da transação, em milissegundos.", S_AL, apis=T, req=SIM),
    O.field(A, "Location", "picklist", "FGNRS", None, "Origem do log.", S_AL, apis=T, completa="sim", vals=["Monitoring", "SystemLog"],
            notas=["Monitoring: visível a administradores, guardado por 7 dias. SystemLog: privado, guardado por 24 horas."]),
    O.field(A, "LogLength", "int", "FGS", None, "Tamanho do log ou do heap dump, em bytes.", S_AL, apis=T, req=SIM),
    O.field(A, "LogUserId", "reference", "FGNS", None, "O usuário cujas ações geraram o log.", S_AL, apis=T, ref=["obj:User"]),
    O.field(A, "Operation", "string", "FGS", None, "Nome da operação que gerou o log, como APEXSOAP.", S_AL, apis=T, req=SIM),
    O.field(A, "Request", "string", "FGS", None, "Origem da requisição: API ou Application (a interface do Salesforce).", S_AL, apis=T, req=SIM),
    O.field(A, "RequestIdentifier", "string", "FGS", None, "Identificador único da requisição, usado para ligar logs da mesma requisição.", S_AL, apis=T),
    O.field(A, "StartTime", "dateTime", "FS", None, "Início da transação.", S_AL, apis=T, req=SIM),
    O.field(A, "Status", "string", "FGS", None, "Resultado da transação: Success ou o texto de uma exceção Apex não tratada.", S_AL, apis=T, req=SIM),
]
O.obj("ApexLog",
      "Um log de depuração guardado: quem o gerou, quando, quanto durou a transação, o tamanho e o resultado.",
      "Listar e apagar logs de depuração por API e localizar o log de uma requisição.",
      [O.expo("tooling", "verificado", S_AL, ["delete()", "describeSObjects()", "query()", "retrieve()"], rest=["Query", "GET", "DELETE"],
              nota="A página só informa versão para o recurso REST que devolve o corpo do log (API 28.0 em diante)."), PADRAO_D()],
      al,
      [{"api": "tooling", "soql": "SELECT LogUserId, Operation, Status, DurationMilliseconds, LogLength, StartTime FROM ApexLog ORDER BY StartTime DESC",
        "endpoint": END, "contexto": "Tooling API. Lista os logs mais recentes.", "validacao": "documental"}],
      APEX_D, O.cob("completa", 10, 10, O.cnt(al), "Tabela de campos lida completa (10; há uma linha em branco na tabela); Id não consta."), S_AL,
      alertas=["O objeto traz os dados do log, não o texto: o corpo é lido por um recurso REST próprio (ApexLog Body).",
               "Logs do tipo Monitoring ficam 7 dias, ou até alguém apagar; os do tipo SystemLog, 24 horas.",
               "Use RequestIdentifier para juntar vários logs gerados pela mesma requisição."])

C.rel_lookup("traceflag-debuglevel", F, "DebugLevelId", D, "Cada trace flag usa um debug level, que define os níveis de log por categoria.", S_TF)
C.rel_lookup("traceflag-user", F, "TracedEntityId", "obj:User", "Uma trace flag de usuário aponta o usuário cujo log é coletado.", S_TF)
C.rel_lookup("apexlog-user", A, "LogUserId", "obj:User", "Cada log pertence ao usuário cujas ações o geraram.", S_AL)

# ================================================================ nota de extração: lista de campos
ls = ["", "-- Lista de campos transcrita da leitura (gerada por lote7j_observabilidade_fecho.py; nome | tipo)"]
for src, nome, campos in ((S_TF, "TraceFlag", tf), (S_DL, "DebugLevel", dl), (S_AL, "ApexLog", al)):
    ls.append(f"[{src}] objeto {nome}: " + ", ".join(f"{c['nome']} | {c['tipo_tecnico']}" for c in campos))
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(ls) + "\n")

# ================================================================ funcionalidades
OBS = "observabilidade-auditoria-e-operacao"
NAO_IMPL = {"tipo": "metadata_type", "estado": "nao_aplicavel", "motivo": "É tela de acompanhamento de uso, não configuração implantável."}
SEM_OBJ = {"tipo": "objeto_api", "estado": "desconhecido", "motivo": "Objetos API não investigados neste lote; a lista vazia não comprova inexistência."}


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


C.ampliar_funcionalidade("debug-logs", objs=[("TraceFlag", "Cada trace flag (Tooling API)."), ("DebugLevel", "Os níveis de log por categoria (Tooling API)."),
                                             ("ApexLog", "Cada log de depuração guardado (Tooling API).")],
                         srcs=[S_TF, S_DL, S_AL], remover_ausencia_de="objeto_api",
                         alertas=["Logs guardados para administradores (Monitoring) ficam 7 dias; os do Developer Console (SystemLog), 24 horas."])

C.funcionalidade(
    "system-overview", "System Overview", "System Overview", ["system overview", "limites da org", "uso da org", "api requests last 24 hours", "org health"],
    "A página System Overview mostra o uso e os limites da org em seis grupos: schema, uso de API, lógica de negócio, interface, licenças "
    "mais usadas e portal roles. Avisa quando a org chega a 95% de um limite.",
    "Ver de relance o quanto a org já consumiu de cada limite antes de bater nele.",
    "Antes de instalar um pacote com muitos objetos, a administradora confere em System Overview quantos custom objects ainda cabem.",
    (OBS, "limites-e-consumo"), [], [], [],
    ["src:help-system-overview", "src:help-system-overview-api", "src:help-system-overview-schema", "src:help-monitor-org", "src:help-kb-api-rolling-limits",
     "src:help-org-health"], [NAO_IMPL, SEM_OBJ],
    setup("Setup > Quick Find: System Overview", "src:help-system-overview", "Clique no número de cada métrica para ver o detalhe."),
    alertas=["O limite de requisições de API vale para a org inteira, somando todas as chamadas das últimas 24 horas; não é por usuário.",
             "A janela de 24 horas é móvel: não zera à meia-noite.",
             "Os percentuais de limite de objetos são truncados, não arredondados.",
             "A contagem total de custom objects inclui os excluídos que ainda esperam a exclusão definitiva."])
C.secundaria("limites-de-api-e-alocacoes", OBS, "limites-e-consumo", "Os limites de requisições de API são acompanhados em System Overview e pelo recurso de limites.",
             srcs=["src:help-system-overview-api"])

C.funcionalidade(
    "armazenamento-de-dados-e-arquivos", "Armazenamento de dados e de arquivos", "Data and File Storage",
    ["storage usage", "data storage", "file storage", "armazenamento", "storage limit exceeded"],
    "A org tem duas cotas de armazenamento: data storage, para registros, e file storage, para arquivos. A página Storage Usage mostra o "
    "espaço disponível de cada uma, o uso por tipo de registro, os usuários que mais ocupam e os maiores arquivos.",
    "Acompanhar o consumo de armazenamento e descobrir o que ocupa mais espaço.",
    "A org está perto do limite de arquivos; em Storage Usage, a administradora vê os maiores arquivos, em ordem de tamanho, e quem mais ocupa espaço.",
    (OBS, "limites-e-consumo"), [], [], [],
    ["src:help-storage-resources", "src:help-storage-allocations", "src:help-kb-storage-record-size", "src:help-kb-storage-sandbox",
     "src:help-kb-email-logs-storage"], [NAO_IMPL, SEM_OBJ],
    setup("Setup > Quick Find: Storage Usage", "src:help-kb-email-logs-storage"),
    alertas=["Ver o uso de armazenamento exige as permissões Manage Internal Users e Manage Users.",
             "A maioria dos registros ocupa cerca de 2 KB de data storage; arquivos ocupam o tamanho real do arquivo enviado.",
             "Em sandboxes, os limites contratados são aplicados: ao passar de um deles, criar registros ou enviar arquivos dá o erro "
             "STORAGE_LIMIT_EXCEEDED. Em produção, o limite de dados não é aplicado de forma estrita.",
             "File storage inclui anexos, Files, Salesforce CRM Content, arquivos e fotos do Chatter e a aba Documents."])

C.funcionalidade(
    "transaction-security", "Transaction Security", "Transaction Security",
    ["enhanced transaction security", "transaction security policy", "condition builder", "real-time event monitoring", "loginevent", "reportevent"],
    "Transaction Security intercepta eventos em tempo real e aplica uma ação: bloquear, exigir autenticação multifator ou notificar. Cada "
    "política tem condições que avaliam o evento, escritas no Condition Builder (sem código) ou em Apex.",
    "Reagir na hora a um comportamento de risco, em vez de só registrá-lo.",
    "Uma política de LoginEvent bloqueia logins vindos de certos países; outra, de ReportEvent, avisa quando alguém exporta um relatório muito grande.",
    (OBS, "eventos-de-monitoramento"), [], [], [],
    ["src:help-transaction-security", "src:help-ts-condition-builder", "src:help-ts-login-policies", "src:help-em-considerations"],
    [{"tipo": "metadata_type", "estado": "bloqueado",
      "motivo": "O tipo TransactionSecurityPolicy consta do inventário v68, mas a página dele no guia versionado devolveu conteúdo ilegível na leitura de "
                "2026-11-16; não foi cadastrado."}, SEM_OBJ],
    af("desconhecido", None, "Caminho de Setup não lido.", []),
    limitacoes=["Exige Salesforce Shield ou o add-on Event Monitoring, em Enterprise, Unlimited e Developer Editions."],
    alertas=["A ação de autenticação multifator não funciona no app móvel, no Lightning Experience nem por API: nesses casos, a política bloqueia.",
             "Pode haver várias políticas para o mesmo evento, mas a Ajuda recomenda que elas não se sobreponham: com a mesma ação, a ordem de "
             "execução é indeterminada.",
             "Criar e gerenciar políticas exige Customize Application e Modify Transaction Security Policy."])
C.ampliar_funcionalidade("event-monitoring", srcs=["src:help-transaction-security"],
                         alertas=["Transaction Security faz parte do Real-Time Event Monitoring: usa os eventos em tempo real para bloquear ou notificar."])
C.ampliar_funcionalidade("estado-e-historico-de-login", srcs=["src:help-kb-login-history-export", "src:help-saml-login-history", "src:help-ts-login-policies"],
                         alertas=["A tela Login History mostra até 20.000 registros dos últimos 6 meses; para ver mais, baixe o arquivo ou consulte "
                                  "o objeto LoginHistory pela API."])
print("lote 7j: 3 objetos da Tooling API gravados; 3 funcionalidades novas e 4 ampliadas")
