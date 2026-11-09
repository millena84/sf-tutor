# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5h (issue #24): referências e definição de __e/__x via CustomObject. (As estruturas de ConnectedApp entram pelo lote5b.py atualizado.)
import json
from b1_base import ev
CAT = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/catalogo/"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
NOME = " A referência é pelo nome do componente, no XML (não é um lookup entre registros)."
def ref(pasta, arq, prop, alvo):
    d = ld(f"{pasta}/{arq}.json"); ok = False
    for p in d["propriedades"]:
        if p["nome"] == prop: p["referencia"] = {"alvos": [alvo], "nota": "Referência pelo nome do componente no XML."}; ok = True
    assert ok, (arq, prop); sv(f"{pasta}/{arq}.json", d)
def rel(rid, o, campo, d, expl, s):
    sv(f"relacionamentos/{rid}.json", {"id": "rel:" + rid, "tipo": "referencia_campo", "origem": {"entidade": o, "campo": campo}, "destino": {"entidade": d},
       "explicacao": expl + NOME, "estado": "verificado", "evidencias": [ev(s)]})
ref("estruturas", "ConnectedAppSamlConfig", "encryptionCertificate", "mdt:Certificate")
rel("connectedappsaml-certificate", "mdx:ConnectedAppSamlConfig", "encryptionCertificate", "mdt:Certificate",
    "A configuração SAML do connected app usa um certificado da org (pelo nome) para cifrar as asserções.", "src:mdapi-connectedapp")
ref("metadata-types", "CustomObject", "externalDataSource", "mdt:ExternalDataSource")
rel("customobject-externaldatasource", "mdt:CustomObject", "externalDataSource", "mdt:ExternalDataSource",
    "Um objeto externo (__x) aponta a fonte de dados externa que guarda os seus dados.", "src:mdapi-customobject")
def upd(fid, mdts, srcs):
    f = ld(f"funcionalidades/{fid}.json"); r = f["representacoes"]["metadata_types"]
    have = {x["ref"] for x in r}
    r += [{"ref": "mdt:" + m, "papel": p} for m, p in mdts if "mdt:" + m not in have]
    f["evidencias"] += [ev(s) for s in srcs if not any(e["fonte"] == s for e in f["evidencias"])]
    sv(f"funcionalidades/{fid}.json", f)
upd("platform-events", [("CustomObject", "Definição do evento: um objeto com sufixo __e, com eventType e publishBehavior.")], ["src:mdapi-customobject", "src:objref-eventbussubscriber"])
upd("external-objects", [("CustomObject", "Definição do objeto externo (sufixo __x), com externalDataSource e externalName.")], ["src:mdapi-customobject"])
print("ok lote 5h")
for fid, old, new in [("platform-events", "A definição do evento em si (objeto __e) não foi lida nesta sessão.",
                       "A definição do evento usa CustomObject (eventType, publishBehavior). O sufixo __e vem das páginas de eventos, não da página de CustomObject."),
                      ("external-objects", "A definição do objeto externo (__x) não foi lida nesta sessão.",
                       "A definição do objeto externo usa CustomObject (externalDataSource, externalName, externalRepository); a página de CustomObject confirma o sufixo __x.")]:
    f = ld(f"funcionalidades/{fid}.json"); f["limitacoes"] = [new if x == old else x for x in f["limitacoes"]]; sv(f"funcionalidades/{fid}.json", f)
print("ok limitacoes")
