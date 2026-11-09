# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5e (issue #24): INT-07, segunda parte (callouts, Bulk API, Pub/Sub API).
import json
from b1_base import ev, af

BASE = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/"
CAT = BASE + "catalogo/"
DATA = "2026-11-09"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")

reg = json.load(open(BASE + "fontes/registro.json"))
A = "https://developer.salesforce.com/docs/atlas.en-us.264.0."
CHK = {"estado": "verificado", "nota": f"Conteúdo lido em {DATA} e conferido quanto ao assunto (não apenas HTTP 200)."}
def src(id, t, u, pert, ver="68.0"):
    return {"id": id, "titulo": t, "url": u, "tipo": "oficial_documentacao", "versao": ver, "data_verificacao": DATA, "metodo": "extracao_documental_assistida",
            "pertinencia": pert, "extracao": "fontes/extracoes/lote5e-int07.txt", "checagem_online": CHK}
novas = [
 src("src:apex-callout-limits", "Callout Limits and Limitations (Apex Developer Guide)", A + "apexcode.meta/apexcode/apex_callouts_timeouts.htm", "Limites, timeouts e restrições de callouts em Apex."),
 src("src:limits-bulk-api", "Bulk API and Bulk API 2.0 Limits and Allocations", A + "salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_bulkapi.htm", "Limites de lotes, jobs, arquivos e consultas da Bulk API."),
 src("src:bulk-api-intro", "Introduction to Bulk API 2.0 and Bulk API", A + "api_asynch.meta/api_asynch/asynch_api_intro.htm", "O que é a Bulk API e quando usar."),
 src("src:pubsub-overview", "Pub/Sub API overview", "https://developer.salesforce.com/docs/platform/pub-sub-api/overview", "O que é a Pub/Sub API, protocolo e eventos suportados.", ver="sem versão na página"),
 src("src:pubsub-allocations", "Pub/Sub API and Event Allocations", "https://developer.salesforce.com/docs/platform/pub-sub-api/guide/allocations.html", "Alocações de publicação, assinatura e conexão da Pub/Sub API.", ver="sem versão na página"),
]
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

INTc, INT7 = "integracao-apis-e-eventos", "contratos-limites-e-tratamento-de-falhas"
NAO = lambda tipo, m, s=None: {"tipo": tipo, "estado": "desconhecido", "motivo": m, **({"evidencias": [ev(s)]} if s else {})}
def addsub(fid, subs):
    for s in subs:
        d = ld(f"subclassificacoes/{s}.json"); d["funcionalidades"] = sorted(set(d["funcionalidades"]) | {"func:" + fid}); sv(f"subclassificacoes/{s}.json", d)
def F(fid, nome, tec, aliases, oq, fin, ex, principal, secundarias, mdts, objs, srcs, ausencias, setup, codigo=(), recs=(), alertas=(), limit=()):
    rep = {"metadata_types": [{"ref": "mdt:" + r, "papel": p} for r, p in mdts], "objetos_api": [{"ref": "obj:" + r, "papel": p} for r, p in objs], "ausencias": ausencias}
    if codigo: rep["codigo"] = list(codigo)
    f = {"id": "func:" + fid, "nome": nome, "nome_tecnico": tec, "aliases": aliases,
         "termos_busca": sorted(set([nome.lower(), tec.lower()] + [a.lower() for a in aliases])), "o_que_e": oq, "finalidade": fin, "exemplo": ex,
         "classificacao_principal": {"classificacao": "cls:" + INTc, "subclassificacao": "sub:" + principal},
         "classificacoes_secundarias": [{"classificacao": "cls:" + INTc, "subclassificacao": "sub:" + s, "motivo": m} for s, m in secundarias],
         "representacoes": rep, "setup": setup, "recomendacoes": [{"texto": t, "natureza": n, "evidencias": [ev(s)]} for t, n, s in recs],
         "alertas": list(alertas), "limitacoes": list(limit), "estado": "verificado", "evidencias": [ev(s) for s in srcs]}
    sv(f"funcionalidades/{fid}.json", f); addsub(fid, [principal] + [s for s, _ in secundarias])

C = "src:apex-callout-limits"
F("limites-e-falhas-de-callouts", "Limites e falhas de callouts", "Apex Callout Limits and Limitations",
  ["callout", "timeout", "settimeout", "timeout_x", "uncommitted work pending", "chamada externa apex", "modo somente leitura"],
  "Regras que valem quando o Apex chama um sistema externo: quantas chamadas, quanto tempo cada uma pode esperar e o que não pode vir antes delas.",
  "Desenhar integrações que não estourem o tempo da transação e falhem de forma previsível.",
  "Um trigger grava o pedido e depois tenta chamar o ERP na mesma transação: a chamada é recusada porque há DML pendente. A solução é chamar antes ou mover a chamada para um processo assíncrono.",
  INT7, [("chamadas-externas-e-endpoints", "Restringe as chamadas a endpoints externos feitas em Apex.")], [], [], [C],
  [NAO("metadata_type", "São regras de execução do Apex, não configuração implantável; nenhum metadata type foi associado nas fontes deste lote.", C),
   NAO("objeto_api", "Nenhum objeto API associado nas fontes deste lote.")],
  af("nao_aplicavel", None, "Não é configuração de Setup: são limites de execução do Apex."),
  codigo=["Apex: HttpRequest.setTimeout(ms) — de 1 a 120.000 ms; padrão de 10 s", "Apex (classes geradas de WSDL): stub.timeout_x = ms",
          "Apex: System.getApplicationReadWriteMode() para detectar o modo somente leitura"],
  recs=[("Em modo somente leitura, pule os callouts: eles executam, mas as gravações que viriam depois são bloqueadas.", "orientacao_oficial", C)],
  alertas=["Até 100 callouts por transação, e a soma dos timeouts não passa de 120 segundos.",
           "Não é possível fazer callout depois de DML, Apex assíncrono, Apex agendado ou envio de e-mail pendentes na mesma transação; antes deles, pode.",
           "Developer Edition: até 20 callouts simultâneos para fora do domínio da org.",
           "Enviar Expect: 100-Continue a um servidor que não responde 100 Continue causa timeout."],
  limit=["A página não lista limites de tamanho de requisição ou resposta, nem nomeia a exceção lançada; não foram catalogados.",
         "Números conforme a documentação v68.0 lida em 2026-11-09."])

B = "src:limits-bulk-api"
F("bulk-api", "Bulk API 2.0 e Bulk API", "Bulk API 2.0 and Bulk API",
  ["bulk api", "bulk api 2.0", "carga em massa", "jobs assíncronos", "dailybulkv2queryjobs", "query_timeout"],
  "APIs REST para grandes volumes de dados: o pedido vira um job processado em segundo plano, e o resultado é buscado depois. A Bulk API (1.0) é a antecessora, ainda disponível.",
  "Inserir, atualizar, fazer upsert, excluir ou consultar muitos registros sem esbarrar nos limites das chamadas síncronas.",
  "Uma migração de 2 milhões de contatos sobe em jobs de ingestão da Bulk API 2.0, com arquivos CSV de cerca de 100 MB.",
  "apis-de-dados-e-metadados", [(INT7, "Tem alocações próprias de lotes, jobs, arquivos e consultas, e regras de retentativa.")], [], [], ["src:bulk-api-intro", B],
  [NAO("metadata_type", "API de dados: não é configurada por metadata type nas fontes deste lote.", "src:bulk-api-intro"),
   NAO("objeto_api", "Jobs e lotes não foram investigados como objetos API neste lote.")],
  af("desconhecido", None, "Caminho no Setup não verificado nesta sessão."),
  codigo=["REST: jobs de ingestão e de consulta da Bulk API 2.0 (lotes automáticos)", "REST: Bulk API 1.0 com lotes criados pelo cliente",
          "Paginação de resultados de consulta na 2.0: parâmetros locator e maxRecords"],
  recs=[("Use a Bulk API 2.0 para operações com mais de 2.000 registros; abaixo disso, prefira chamadas síncronas em lote (REST Composite ou SOAP).", "orientacao_oficial", B)],
  alertas=["Até 15.000 lotes por 24 horas móveis, compartilhados entre 1.0 e 2.0 (na 2.0, só jobs de ingestão consomem).",
           "Ingestão: até 150 milhões de registros por 24 horas; na 2.0, até 150 MB de CSV em base64 por job (subir cerca de 100 MB).",
           "Bulk API 2.0: até 10.000 jobs de consulta e 1 TB de resultados por 24 horas, acompanháveis em /limits.",
           "Jobs terminados há mais de 7 dias são apagados; resultados ficam disponíveis por 7 dias."],
  limit=["Não há SLA garantido para a Bulk API 1.0 nem para a 2.0.", "Números conforme a documentação v68.0 lida em 2026-11-09."])

P = "src:pubsub-allocations"
F("pub-sub-api", "Pub/Sub API", "Pub/Sub API",
  ["pub/sub api", "pubsub", "grpc", "avro", "managedsubscribe", "assinar eventos", "publicar eventos"],
  "Interface única para publicar e assinar eventos de plataforma, eventos de alteração e eventos de monitoramento em tempo real. Usa gRPC e HTTP/2, com mensagens em Avro.",
  "Integrar sistemas externos aos eventos da org, com o cliente controlando quantos eventos recebe por vez.",
  "Um serviço externo assina AccountChangeEvent pela Pub/Sub API e pede até 100 eventos por chamada, no ritmo em que consegue processar.",
  "eventos-e-mensageria", [(INT7, "Tem alocações próprias de publicação, assinatura e conexões.")],
  [("ManagedEventSubscription", "Assinatura gerenciada, consumida pelo ManagedSubscribe.")],
  [("PlatformEventUsageMetric", "Uso de publicação e entrega; o cliente aparece como PUB_SUB_API.")],
  ["src:pubsub-overview", P, "src:objref-platformeventusagemetric", "src:mdapi-managedeventsubscription"], [],
  af("nao_aplicavel", None, "API acessada por clientes gRPC; não é configurada por uma tela de Setup nas fontes deste lote."),
  codigo=["gRPC: Publish e PublishStream", "gRPC: Subscribe (assinatura por pull)", "gRPC: ManagedSubscribe (Beta na página de alocações)"],
  recs=[("Mantenha cada PublishRequest abaixo de cerca de 3 MB e com até 200 eventos.", "orientacao_oficial", P)],
  alertas=["Acima de 4 MB por requisição, a chamada falha com UNAVAILABLE e o servidor fecha o stream.",
           "Cada evento tem no máximo 1 MB; um evento grande demais falha sozinho, sem impedir os outros do lote.",
           "No máximo 100 eventos pedidos por vez (num_requested) e 200 assinaturas gerenciadas por org.",
           "Até 1.000 streams simultâneos por canal gRPC (conexão HTTP/2)."],
  limit=["As páginas da Pub/Sub API não trazem versão; leitura em 2026-11-09.", "ManagedSubscribe aparece como Beta na página de alocações."])

core = ld("nuvens/platform-core.json")
c = next(x for x in core["classificacoes_aplicaveis"] if x["classificacao"] == "cls:" + INTc)
for sub, fid in [("sub:" + INT7, "func:limites-e-falhas-de-callouts"), ("sub:apis-de-dados-e-metadados", "func:bulk-api"), ("sub:eventos-e-mensageria", "func:pub-sub-api")]:
    s = next(x for x in c["subclassificacoes"] if x["subclassificacao"] == sub)
    s["funcionalidades"] = sorted(set(s["funcionalidades"]) | {fid})
sv("nuvens/platform-core.json", core)
print("ok lote 5e")
