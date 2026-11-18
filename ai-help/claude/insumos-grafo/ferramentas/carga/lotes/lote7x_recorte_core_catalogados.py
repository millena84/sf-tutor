"""Lote 7x (issue #10, etapa 1; decisão da autora em 2026-11-18, opção B): recorte Core dos metadata types já catalogados
e ligação das funcionalidades que não tinham nuvem.

1. Funcionalidades sem nuvem: as que rodam na camada compartilhada vão para nuv:platform-core; contratos e pedidos
   vão para nuv:sales-cloud, junto com os demais itens de vendas. É curadoria do projeto, não classificação oficial.
2. Recorte de cada metadata type catalogado, com critério e motivo em config/escopo.json (justificativas):
   - incluido (C1 + C3): usado pela plataforma ou por mais de uma nuvem, sem exigência de licença registrada;
   - excluido (C3): específico de uma nuvem só; continua no mapa como parte dela;
   - excluido (C2/X2): todas as funcionalidades que o usam registram, com fonte, exigência de licença de produto;
   - pendente (C2): a fonte registrada não esclarece a licença (funcionalidades de IA sem esse registro e Field Audit Trail).
Também reescreve o texto do critério C2 conforme a decisão da autora.

Ordem: lote7w_nuvens_faltantes.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
"""
import glob, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv               # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-18"

# Funcionalidades que registram exigência de licença de produto, com fonte, no próprio catálogo (alertas, limitações ou nota de Setup).
LICENCIADAS = {
    "func:agentes-agentforce": "as licenças exigidas variam conforme o tipo de agente",
    "func:agentforce-data-library": "exige Data 360 configurado",
    "func:einstein-trust-layer": "exige Einstein Generative AI e Data Cloud",
    "func:crm-analytics": "cada usuário precisa da permission set license do CRM Analytics",
    "func:transaction-security": "exige Salesforce Shield ou o add-on Event Monitoring",
    "func:servicos-externos-registrados-commerce": "exige licença B2B Commerce ou D2C Commerce",
    "func:field-service": "produto Agentforce Field Service and Operations, com licenças próprias",
    "func:configuracoes-de-nuvens-de-setor": "cada nuvem de setor tem licença própria",
    "func:revenue-management": "exige licença de Revenue Management",
}
# Sem registro de licença, mas a fonte registrada não trata do assunto: fica pendente em vez de suposição.
PENDENTES = {
    "func:prompt-builder": "a fonte registrada não trata da licença; as funcionalidades de IA vizinhas exigem licença",
    "func:subagents-e-agent-actions": "a fonte registrada não trata da licença; as funcionalidades de IA vizinhas exigem licença",
    "func:field-audit-trail": "a fonte registrada não trata da licença do Field Audit Trail",
}
PARA_SALES = {"func:contratos", "func:pedidos"}


def funcs_por_nuvem():
    m = {}
    for f in glob.glob(os.path.join(RAIZ, "catalogo", "nuvens", "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        for c in d["classificacoes_aplicaveis"]:
            for s in c["subclassificacoes"]:
                for fid in s["funcionalidades"]:
                    m.setdefault(fid, set()).add(d["id"])
    return m


def acrescentar(nuvem_id, func):
    """Põe a funcionalidade na nuvem, sob a classificação e a subclassificação principais dela."""
    n = ld(f"nuvens/{nuvem_id.split(':', 1)[1]}.json")
    c, s = func["classificacao_principal"]["classificacao"], func["classificacao_principal"]["subclassificacao"]
    cls = next((x for x in n["classificacoes_aplicaveis"] if x["classificacao"] == c), None)
    if cls is None:
        cls = {"classificacao": c, "subclassificacoes": []}
        n["classificacoes_aplicaveis"].append(cls)
    sub = next((x for x in cls["subclassificacoes"] if x["subclassificacao"] == s), None)
    if sub is None:
        sub = {"subclassificacao": s, "funcionalidades": []}
        cls["subclassificacoes"].append(sub)
    if func["id"] not in sub["funcionalidades"]:
        sub["funcionalidades"].append(func["id"])
    sv(f"nuvens/{nuvem_id.split(':', 1)[1]}.json", n)


# 1. funcionalidades sem nuvem
funcs = {d["id"]: d for d in (json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(RAIZ, "catalogo", "funcionalidades", "*.json")))}
ja = funcs_por_nuvem()
ligadas = []
for fid in sorted(funcs):
    if fid in ja:
        continue
    acrescentar("nuv:sales-cloud" if fid in PARA_SALES else "nuv:platform-core", funcs[fid])
    ligadas.append(fid)
porn = funcs_por_nuvem()

# 2. recorte de cada metadata type catalogado
func_do_mdt = {}
for fid, d in funcs.items():
    for r in d.get("representacoes", {}).get("metadata_types", []):
        func_do_mdt.setdefault(r["ref"], set()).add(fid)
NOME = {"nuv:sales-cloud": "Agentforce Sales", "nuv:service-cloud": "Agentforce Service", "nuv:experience-cloud": "Experience Cloud",
        "nuv:field-service": "Field Service", "nuv:industries": "Industries", "nuv:revenue": "Revenue Management", "nuv:commerce": "Commerce"}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just = cc.get("justificativas", {})
inc, exc = set(cc["incluidos"]), set(cc["excluidos"])
contagem = {"incluido": 0, "excluido_nuvem": 0, "excluido_licenca": 0, "pendente": 0}
for f in sorted(glob.glob(os.path.join(RAIZ, "catalogo", "metadata-types", "*.json"))):
    m = json.load(open(f, encoding="utf-8"))
    nome, fs = m["nome"], sorted(func_do_mdt.get(m["id"], set()))
    ns = sorted(set().union(*[porn.get(x, set()) for x in fs])) if fs else []
    base = {"funcionalidades": fs, "nuvens": ns, "data": DATA}
    if fs and all(x in LICENCIADAS for x in fs):
        dec = {"decisao": "excluido", "criterios": ["C2", "X2"],
               "motivo": "Exige licença de produto: " + "; ".join(sorted({LICENCIADAS[x] for x in fs})) + ". Continua no mapa como parte do produto."}
        contagem["excluido_licenca"] += 1
    elif fs and all(x in LICENCIADAS or x in PENDENTES for x in fs):
        dec = {"decisao": "pendente", "criterios": ["C2"], "motivo": "Licença não esclarecida: " + "; ".join(sorted({PENDENTES.get(x, LICENCIADAS.get(x)) for x in fs})) + "."}
        contagem["pendente"] += 1
    elif ns == ["nuv:platform-core"] or len(ns) >= 2:
        dec = {"decisao": "incluido", "criterios": ["C1", "C3"],
               "motivo": "Catalogado a partir da página oficial da v68 e usado " + ("pela plataforma compartilhada." if len(ns) == 1 else "por mais de uma nuvem: " + ", ".join(NOME.get(x, "Agentforce 360 Platform") for x in ns) + ".")}
        contagem["incluido"] += 1
    elif len(ns) == 1:
        dec = {"decisao": "excluido", "criterios": ["C3"],
               "motivo": f"Específico de {NOME.get(ns[0], ns[0])}; não é camada compartilhada. Continua no mapa como parte dessa nuvem."}
        contagem["excluido_nuvem"] += 1
    else:
        dec = {"decisao": "pendente", "criterios": ["C3"], "motivo": "Sem funcionalidade ou nuvem associada no catálogo."}
        contagem["pendente"] += 1
    just[nome] = {**dec, **base}
    inc.discard(nome); exc.discard(nome)
    if dec["decisao"] == "incluido":
        inc.add(nome)
    elif dec["decisao"] == "excluido":
        exc.add(nome)
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
for c in esc["criterios_inclusao"]:
    if c["id"] == "C2":
        c["texto"] = ("O item não depende de licença de produto além das edições comuns da plataforma. Quando o catálogo registra, com fonte oficial, "
                      "exigência de licença de produto ou add-on, o item fica fora do Core. Quando não há registro e o item serve à plataforma ou a mais "
                      "de uma nuvem, ele entra. Quando a fonte registrada não esclarece e há indício de licença, fica pendente. "
                      "(Regra ajustada por decisão da autora em 2026-11-18; antes, a falta de fonte deixava tudo pendente.)")
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7x: {len(ligadas)} funcionalidades ligadas a nuvens; recorte dos catalogados: {contagem}")
