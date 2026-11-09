# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5d (issue #24): contratos, limites e tratamento de falhas (INT-07).
import json
from b1_base import ev, af
from b3_obj import field, expo, obj, cob, cnt, APEX_OK

BASE = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/"
CAT = BASE + "catalogo/"
DATA = "2026-11-09"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")

# ================================================================ fontes
reg = json.load(open(BASE + "fontes/registro.json"))
A = "https://developer.salesforce.com/docs/atlas.en-us.264.0."
CHK = {"estado": "verificado", "nota": f"Conteúdo lido em {DATA} e conferido quanto ao assunto (não apenas HTTP 200)."}
def src(id, t, u, pert):
    return {"id": id, "titulo": t, "url": u, "tipo": "oficial_documentacao", "versao": "68.0", "data_verificacao": DATA, "metodo": "extracao_documental_assistida",
            "pertinencia": pert, "extracao": "fontes/extracoes/lote5d-contratos-limites.txt", "checagem_online": CHK}
novas = [
 src("src:objref-eventbussubscriber", "EventBusSubscriber (Object Reference)", A + "object_reference.meta/object_reference/sforce_api_objects_eventbussubscriber.htm", "Chamadas, acesso e campos de EventBusSubscriber."),
 src("src:objref-platformeventusagemetric", "PlatformEventUsageMetric (Object Reference)", A + "object_reference.meta/object_reference/sforce_api_objects_platformeventusagemetric.htm", "Chamadas, versão e campos de PlatformEventUsageMetric."),
 src("src:rest-limits", "Limits (REST API Developer Guide)", A + "api_rest.meta/api_rest/resources_limits.htm", "Recurso REST que lista limites e alocações da org."),
 src("src:rest-versions", "Versions (REST API Developer Guide)", A + "api_rest.meta/api_rest/resources_versions.htm", "Recurso REST que lista as versões de API disponíveis."),
 src("src:rest-api-eol", "API End-of-Life Policy (REST API Developer Guide)", A + "api_rest.meta/api_rest/api_rest_eol.htm", "Política de suporte, descontinuação e aposentadoria de versões."),
 src("src:limits-api-requests", "API Request Limits and Allocations (Developer Limits Quick Reference)", A + "salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_api.htm",
     "Cálculo do limite diário de requisições, concorrência, timeouts e onde monitorar."),
 src("src:pe-retry-apex", "Retry Event Triggers with EventBus.RetryableException (Platform Events Developer Guide)", A + "platform_events.meta/platform_events/platform_events_subscribe_apex_refire.htm",
     "Retentativas de triggers de eventos e estado de erro do assinante."),
]
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

TOOL_D = lambda: expo("tooling", "desconhecido", nota="Exposição na Tooling API não verificada.")
NUM = lambda s: {"natureza": "numerico", "estado": "verificado", "evidencias": [ev(s)]}

# ================================================================ objetos
S = "src:objref-eventbussubscriber"; O = "obj:EventBusSubscriber"
OBS = lambda novo: ["Obsoleto a partir da 66.0; use " + novo + ".", "Pode vir incorreto se passar do maior inteiro suportado."]
eb = [
 field(O, "ExternalId", "string", "FGNS", None, "Id do assinante, por exemplo o Id do trigger.", S),
 field(O, "IsPartitioned", "boolean", "DFGS", "62.0", "Se o trigger usa assinaturas paralelas.", S, default=("valor", "false", None)),
 field(O, "LastError", "string", "FGNS", "43.0", "Mensagem da última EventBus.RetryableException (só triggers Apex).", S),
 field(O, "LastProcessed", "string", "FGNS", "66.0", "Replay ID do último evento processado pelo assinante; substitui Position.", S),
 field(O, "LastPublished", "string", "FGNS", "66.0", "Replay ID do último evento publicado; substitui Tip.", S,
       notas=["Em eventos de alto volume e de alteração, o valor não existe e vem sempre -1."]),
 field(O, "Name", "string", "FGNS", None, "Nome do assinante (trigger ou processo); 'Process' indica ao menos um elemento Pause de flow.", S),
 field(O, "Position", "int", "FGNS", None, "Replay ID do último evento processado.", S, notas=OBS("LastProcessed")),
 field(O, "Retries", "int", "FGNS", "43.0", "Quantas vezes o trigger foi repetido por EventBus.RetryableException (só triggers Apex).", S),
 field(O, "Status", "picklist", "FGNRS", None, "Situação do assinante.", S, vals=["Error", "Repartitioning", "Running", "Suspended"], completa="sim",
       contexto="Error: desconectado, em geral após passar do máximo de retentativas. Suspended: suspenso por um admin ou erro interno. Repartitioning: mudando a configuração de assinaturas paralelas. Running: escutando."),
 field(O, "Tip", "int", "FGNS", None, "Replay ID do último evento publicado.", S, notas=OBS("LastPublished") + ["Em eventos de alto volume e de alteração, vem sempre -1."]),
 field(O, "Topic", "string", "FGNS", None, "Canal assinado: nome do evento com __e ou nome do evento de alteração (ex.: AccountChangeEvent).", S),
 field(O, "Type", "string", "FGNS", None, "Tipo do assinante, por exemplo ApexTrigger; vazio para processo ou elemento Pause.", S)]
obj("EventBusSubscriber", "Representa cada trigger, processo ou flow assinante de um evento de plataforma ou de alteração.",
    "Ver a situação, a posição e as retentativas dos assinantes internos; não inclui clientes CometD nem Pub/Sub API.",
    [expo("padrao", "verificado", S, ["describeSObjects()", "query()"], acesso="Somente leitura; desde o Summer '20, só usuários internos da org."), TOOL_D()],
    eb, [{"api": "padrao", "soql": "SELECT Name, Type, Status, Retries, LastError, LastProcessed, LastPublished FROM EventBusSubscriber WHERE Topic = 'Pedido__e'",
          "contexto": "API padrão, versão 66.0 ou posterior (LastProcessed e LastPublished). Pedido__e é um nome ilustrativo.", "validacao": "documental"}],
    APEX_OK(S), cob("completa", 12, 12, cnt(eb), "Tabela de campos lida completa (12); Id não consta."), S,
    alertas=["O exemplo da página usa Position e Tip, obsoletos a partir da 66.0."])

S = "src:objref-platformeventusagemetric"; O = "obj:PlatformEventUsageMetric"
ENH = ["Só com Enhanced Usage Metrics (PlatformEventSettings.enableEnhancedUsageMetrics)."]
pm = [
 field(O, "Client", "string", "FGNS", None, "Cliente que publicou ou recebeu (sessão CometD, PUB_SUB_API, EVENT_RELAY, APEX, Id de trigger etc.).", S, notas=ENH),
 field(O, "EndDate", "dateTime", "FNS", None, "Fim da janela consultada, em UTC e com granularidade de hora.", S),
 field(O, "EventName", "string", "FGNS", None, "Nome API do evento ou do evento de alteração; exige UsageType na consulta.", S, notas=ENH),
 field(O, "EventType", "picklist", "FGNRS", None, "Tipo de evento consultado; exige UsageType na consulta.", S, vals=["CHANGE_EVENT", "CUSTOM_PLATFORM_EVENT"], completa="sim", notas=ENH),
 field(O, "ExternalId", "string", "FGNS", None, "Não usado.", S),
 field(O, "Name", "picklist", "FGRS", None, "Métrica consultada: eventos publicados ou entregues, de plataforma ou de alteração.", S,
       vals=["CHANGE_EVENTS_DELIVERED", "CHANGE_EVENTS_PUBLISHED", "PLATFORM_EVENTS_DELIVERED", "PLATFORM_EVENTS_PUBLISHED"], completa="sim"),
 field(O, "StartDate", "dateTime", "FNS", None, "Início da janela consultada, em UTC; com métricas detalhadas, até 60 dias e compatível com TimeSegment.", S),
 field(O, "TimeSegment", "picklist", "FGNRS", None, "Intervalo de agregação, conforme o tamanho da janela.", S, vals=["Daily", "Hourly", "FifteenMinutes"], completa="sim", notas=ENH),
 field(O, "UsageType", "picklist", "FGNRS", None, "Publicação ou entrega; usado com EventName ou EventType.", S, vals=["PUBLISH", "DELIVERY"], completa="sim", notas=ENH),
 field(O, "Value", "long", "FGNS", None, "Valor de uso da métrica no período.", S, dominio=NUM(S))]
obj("PlatformEventUsageMetric", "Guarda o uso de publicação e de entrega de eventos de plataforma e de alteração.",
    "Acompanhar o consumo das alocações de eventos (clientes CometD e Pub/Sub API, empApi e event relays).",
    [expo("padrao", "verificado", S, ["describeSObjects()", "query()"], desde="50.0"), TOOL_D()],
    pm, [{"api": "padrao", "soql": "SELECT Name, StartDate, EndDate, Value FROM PlatformEventUsageMetric WHERE Name = 'PLATFORM_EVENTS_DELIVERED' AND StartDate > 2026-11-01T00:00:00.000Z AND EndDate < 2026-11-08T00:00:00.000Z",
          "contexto": "API padrão; uso diário histórico (datas ilustrativas).", "validacao": "documental"}],
    APEX_OK(S), cob("completa", 10, 10, cnt(pm), "Tabela de campos lida completa (10); Id não consta."), S,
    alertas=["Os valores não cobrem triggers Apex, flows nem processos (ver src:rest-limits)."])

# ================================================================ funcionalidades
INTc, SUB = "integracao-apis-e-eventos", "contratos-limites-e-tratamento-de-falhas"
NAO_MDT = lambda m, s: {"tipo": "metadata_type", "estado": "desconhecido", "motivo": m, "evidencias": [ev(s)]}
def addsub(fid, subs):
    for s in subs:
        d = ld(f"subclassificacoes/{s}.json"); d["funcionalidades"] = sorted(set(d["funcionalidades"]) | {"func:" + fid}); sv(f"subclassificacoes/{s}.json", d)
def F(fid, nome, tec, aliases, oq, fin, ex, secundarias, mdts, objs, srcs, ausencias, setup, codigo=(), interface=(), recs=(), alertas=(), limit=()):
    rep = {"metadata_types": [{"ref": "mdt:" + r, "papel": p} for r, p in mdts], "objetos_api": [{"ref": "obj:" + r, "papel": p} for r, p in objs], "ausencias": ausencias}
    if codigo: rep["codigo"] = list(codigo)
    if interface: rep["interface"] = list(interface)
    f = {"id": "func:" + fid, "nome": nome, "nome_tecnico": tec, "aliases": aliases,
         "termos_busca": sorted(set([nome.lower(), tec.lower()] + [a.lower() for a in aliases])), "o_que_e": oq, "finalidade": fin, "exemplo": ex,
         "classificacao_principal": {"classificacao": "cls:" + INTc, "subclassificacao": "sub:" + SUB},
         "classificacoes_secundarias": [{"classificacao": "cls:" + c, "subclassificacao": "sub:" + s, "motivo": m} for c, s, m in secundarias],
         "representacoes": rep, "setup": setup, "recomendacoes": [{"texto": t, "natureza": n, "evidencias": [ev(s)]} for t, n, s in recs],
         "alertas": list(alertas), "limitacoes": list(limit), "estado": "verificado", "evidencias": [ev(s) for s in srcs]}
    sv(f"funcionalidades/{fid}.json", f); addsub(fid, [SUB] + [x[1] for x in secundarias])

L = "src:limits-api-requests"
F("limites-de-api-e-alocacoes", "Limites de API e alocações", "API Request Limits and Allocations",
  ["limites de api", "api limits", "governor", "alocações", "requisições por dia", "request_limit_exceeded", "sforce-limit-info"],
  "Quantas chamadas e recursos a org pode consumir, e quanto ainda resta. As alocações vêm da edição, das licenças e de add-ons comprados.",
  "Planejar integrações que caibam nas alocações e reagir antes que se esgotem.",
  "Uma org Enterprise com 15 licenças Salesforce tem 115.000 requisições por 24 horas (100.000 + 15 × 1.000), segundo o exemplo da documentação.",
  [], [], [], ["src:rest-limits", L],
  [NAO_MDT("Nenhum metadata type encontrado nas fontes deste lote: as alocações vêm da edição, das licenças e de add-ons, não de um componente implantável.", L),
   {"tipo": "objeto_api", "estado": "desconhecido", "motivo": "Os limites são lidos pelo recurso REST /limits, que não é um objeto (sObject); nenhum objeto API foi identificado nas fontes."}],
  af("verificado", "Setup > System Overview (seção API Usage); Setup > Company Information (API Request Limit per Month); Setup > Quick Find: API Usage Notifications",
     "Onde acompanhar o uso. Rótulos em inglês, como na documentação; a tradução da interface em pt-BR não foi verificada.", [ev(L)]),
  codigo=["REST API: GET /services/data/vXX.X/limits/ (desde 29.0; exige View Setup and Configuration)", "REST API: cabeçalho de resposta Sforce-Limit-Info"],
  recs=[("Evite chamar /limits de forma concorrente ou em rajadas quando precisar de valores consistentes: os números têm precisão de até cinco minutos.", "orientacao_oficial", "src:rest-limits"),
        ("Configure API Usage Notifications para receber e-mail quando o uso passar de uma porcentagem da alocação.", "orientacao_oficial", L)],
  alertas=["O limite diário vale para o total da org, não por usuário; chamadas de pacotes gerenciados contam.",
           "Requisições de 20 segundos ou mais têm limite de simultaneidade (25 em produção e sandbox; 5 em Developer Edition e trial); o excedente recebe REQUEST_LIMIT_EXCEEDED.",
           "Chamadas REST e SOAP expiram após 10 minutos (REQUEST_RUNNING_TOO_LONG no SOAP; QUERY_TIMEOUT no REST)."],
  limit=["Números conforme a documentação v68.0 lida em 2026-11-09; as alocações mudam por edição, licença e contrato.",
         "Orgs pagas ativas podem passar um pouco do limite diário, com teto rígido; trial, Developer Edition e sandbox não."])

F("versoes-de-api", "Versões de API e ciclo de vida", "API Versions and End-of-Life Policy",
  ["versão de api", "api version", "apiVersion", "410 gone", "descontinuação", "aposentadoria de versão", "end-of-life"],
  "Cada chamada e cada componente usam uma versão de API. A Salesforce mantém as versões por um tempo e depois as descontinua e aposenta.",
  "Saber quais versões estão disponíveis e planejar a atualização de integrações antes de uma versão deixar de funcionar.",
  "Uma integração antiga que chama /services/data/v30.0/ passou a receber 410:GONE depois do Summer '25.",
  [], [], [], ["src:rest-versions", "src:rest-api-eol"],
  [NAO_MDT("Versão não é um metadata type. Componentes declaram a versão em propriedades próprias (por exemplo, mdt:Flow.apiVersion); a relação geral entre versão e componentes não foi catalogada neste lote.", "src:rest-api-eol"),
   {"tipo": "objeto_api", "estado": "desconhecido", "motivo": "As versões são listadas pelo recurso REST /services/data/, que não é um objeto (sObject)."}],
  af("nao_aplicavel", None, "Não é configuração de Setup: a versão vem em cada chamada ou componente."),
  codigo=["REST API: GET /services/data/ lista as versões disponíveis (sem autenticação)", "REST API: alias latest no lugar de vXX.X leva à versão mais recente"],
  recs=[("Use o tipo de evento API Total Usage para encontrar requisições em versões antigas ou sem suporte.", "orientacao_oficial", "src:rest-api-eol")],
  alertas=["Versões 31.0 a 40.0 estão em descontinuação: sem suporte a partir do Summer '27 e aposentadas no Summer '28.",
           "Versões 21.0 a 30.0 estão aposentadas desde o Summer '25, e 7.0 a 20.0 desde o Summer '22; chamadas a versões aposentadas recebem 410:GONE."],
  limit=["A política foi lida na documentação da REST API; a aplicação a outras APIs não foi verificada neste lote.",
         "Situação das versões conforme a documentação v68.0 lida em 2026-11-09."])

R = "src:pe-retry-apex"
F("reprocessamento-e-monitoramento-de-eventos", "Reprocessamento e monitoramento de eventos", "Event Trigger Retries and Usage Monitoring",
  ["retryableexception", "retentativa", "retry", "assinante de evento", "eventbussubscriber", "uso de eventos", "platformeventusagemetric"],
  "Como um trigger de evento tenta de novo quando algo externo falha, e como acompanhar assinantes e o uso das alocações de eventos.",
  "Evitar perda de eventos em falhas passageiras e detectar assinantes parados ou consumo perto do limite.",
  "Um trigger de Pedido__e lança RetryableException enquanto o ERP está fora; depois de algumas tentativas, avisa um usuário em vez de esgotar as retentativas.",
  [(INTc, "eventos-e-mensageria", "Complementa eventos de plataforma e Change Data Capture com retentativa e monitoramento.")],
  [("PlatformEventSubscriberConfig", "Configuração do trigger assinante."), ("PlatformEventSettings", "Liga as métricas detalhadas de uso.")],
  [("EventBusSubscriber", "Situação, posição e retentativas de cada assinante interno."), ("PlatformEventUsageMetric", "Uso de publicação e entrega de eventos.")],
  [R, "src:objref-eventbussubscriber", "src:objref-platformeventusagemetric"], [], af("desconhecido", None, "Caminho no Setup não verificado nesta sessão."),
  codigo=["Apex: throw new EventBus.RetryableException(...) em trigger de evento", "Apex: EventBus.TriggerContext.currentContext().retries"],
  recs=[("Limite as retentativas a menos de nove e tenha uma ação alternativa quando o limite chegar.", "orientacao_oficial", R)],
  alertas=["Um trigger roda no máximo 10 vezes (a inicial + 9 retentativas); depois disso vai para o estado Error e eventos enviados nesse período não são reenviados.",
           "A retentativa reenvia o lote inteiro e desfaz o DML feito antes dela.",
           "Asserções e exceções não tratadas não levam o assinante ao estado Error."],
  limit=["EventBusSubscriber não inclui clientes CometD nem Pub/Sub API; PlatformEventUsageMetric não cobre triggers, flows nem processos."])

# ---- secundárias em funcionalidades existentes
def sec(fid, motivo, srcs):
    f = ld(f"funcionalidades/{fid}.json")
    if not any(c["subclassificacao"] == "sub:" + SUB for c in f["classificacoes_secundarias"]):
        f["classificacoes_secundarias"].append({"classificacao": "cls:" + INTc, "subclassificacao": "sub:" + SUB, "motivo": motivo})
    f["evidencias"] += [ev(s) for s in srcs if not any(e["fonte"] == s for e in f["evidencias"])]
    sv(f"funcionalidades/{fid}.json", f); addsub(fid, [SUB])
sec("external-services", "Registros e operações de External Services têm alocações próprias, listadas no recurso /limits.", ["src:rest-limits"])
sec("event-relay", "relayOption define de onde o relay retoma depois de um erro.", ["src:mdapi-eventrelayconfig"])
sec("platform-events", "Publicação e entrega de eventos têm alocações próprias, listadas no recurso /limits.", ["src:rest-limits"])

# ---- Private Connect: nome confirmado no recurso /limits
f = ld("funcionalidades/conexoes-de-rede-privadas.json")
if "private connect" not in f["aliases"]:
    f["aliases"].append("private connect"); f["termos_busca"] = sorted(set(f["termos_busca"]) | {"private connect"})
f["limitacoes"] = ["O nome Private Connect aparece no recurso /limits (grupo e limite PrivateConnectOutboundCalloutHourlyLimitMB); o rótulo em português é tradução didática do projeto."]
if not any(e["fonte"] == "src:rest-limits" for e in f["evidencias"]): f["evidencias"].append(ev("src:rest-limits"))
sv("funcionalidades/conexoes-de-rede-privadas.json", f)

# ---- nuvem Platform/Core
core = ld("nuvens/platform-core.json")
c = next(x for x in core["classificacoes_aplicaveis"] if x["classificacao"] == "cls:" + INTc)
NOVAS = {"func:limites-de-api-e-alocacoes", "func:versoes-de-api", "func:reprocessamento-e-monitoramento-de-eventos"}  # só principais, como nas demais
s = next((x for x in c["subclassificacoes"] if x["subclassificacao"] == "sub:" + SUB), None)
if s: s["funcionalidades"] = sorted(set(s["funcionalidades"]) | NOVAS)
else: c["subclassificacoes"].append({"subclassificacao": "sub:" + SUB, "funcionalidades": sorted(NOVAS)})
c["subclassificacoes"].sort(key=lambda x: x["subclassificacao"])
sv("nuvens/platform-core.json", core)
print("ok lote 5d")
