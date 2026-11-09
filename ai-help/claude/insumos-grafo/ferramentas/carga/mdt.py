"""Metadata types, propriedades e estruturas auxiliares (mdt:, mdx:)."""
import json, re
from .base import save, ev, af, caminho, ROOT
import os, glob

SNAP = caminho("fontes", "snapshots", "sdr-13.12.0") + os.sep
REG = json.load(open(SNAP + "metadataRegistry.json"))
MS = {}
for l in open(SNAP + "METADATA_SUPPORT.md", encoding="utf-8"):
    if l.startswith("|") and not l.startswith("|:") and not l.startswith("|Metadata Type"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        MS[c[0]] = (c[1], c[2] if len(c) > 2 else "")


class _NomesMdt:
    """Nomes de metadata types conhecidos: os já catalogados mais os emitidos nesta execução.
    (Os scripts históricos usavam uma lista fixa; aqui a lista acompanha o catálogo.)"""
    def __init__(self):
        self.extra = set()
    def __contains__(self, nome):
        if nome in self.extra:
            return True
        return os.path.exists(os.path.join(ROOT, "metadata-types", nome + ".json"))

MDT_NAMES = _NomesMdt()
PRIM = {"string", "boolean", "int", "number", "double", "dateTime", "date", "picklist", "multipicklist", "reference"}
STRUCTS = {}   # mdx id -> dict
STRUCT_SRC = {}

def dominio_auto(tipo, vals=None, natureza=None, contexto=None, completa="sim", src=None):
    e = [ev(src)] if src else None
    if vals:
        return {"natureza": natureza or "enum_fechado", "valores": [{"valor": v, "significado": s} if s else {"valor": v} for v, s in vals],
                "lista_completa": completa, "estado": "verificado", "evidencias": e, **({"contexto": contexto} if contexto else {})}
    if natureza:
        d = {"natureza": natureza, "estado": "verificado" if natureza in ("texto_livre", "referencia", "tipo_composto") else "desconhecido"}
        if contexto: d["contexto"] = contexto
        if d["estado"] == "verificado": d["evidencias"] = e
        return d
    t = tipo.replace("[]", "")
    if t == "boolean":
        return {"natureza": "booleano", "valores": [{"valor": "true"}, {"valor": "false"}], "lista_completa": "sim", "estado": "verificado", "evidencias": e}
    if t in ("int", "number", "double"):
        return {"natureza": "numerico", "estado": "verificado", "evidencias": e}
    if t == "string":
        return {"natureza": "texto_livre", "estado": "verificado", "evidencias": e,
                "contexto": "A fonte tipa como string sem lista de valores; não inventar valores."}
    if t[:1].isupper() and t not in PRIM:
        return {"natureza": "tipo_composto", "estado": "verificado", "evidencias": e}
    return {"natureza": "desconhecida", "estado": "desconhecido"}

def prop(owner, nome, tipo, req, ver, desc, src, **kw):
    """req: 'S' obrigatório (fonte); 'N' não marcado; 'C:cond' condicional; '?' desconhecido."""
    pid = f"{owner}.{nome}"
    e = [ev(src)]
    if req == "S":
        ob = {"valor": "sim", "estado": "verificado", "evidencias": e}
    elif req.startswith("C:"):
        ob = {"valor": "condicional", "condicao": req[2:], "estado": "verificado", "evidencias": e}
    elif req == "N":
        ob = {"valor": "nao", "estado": "desconhecido",
              "condicao": "A documentação 68.0 não marca o campo como obrigatório; ausência de marcação não comprova opcionalidade (confirmar no WSDL)."}
    else:
        ob = {"valor": "desconhecida", "estado": "desconhecido"}
    d = kw.get("default")
    if d is None:
        dflt = {"forma": "nao_declarado_na_fonte", "estado": "desconhecido"}
    else:
        forma, valor, nota = d
        dflt = {"forma": forma, "estado": "verificado", "evidencias": e}
        if valor is not None: dflt["valor"] = valor
        if nota: dflt["nota"] = nota
    base = tipo.replace("[]", "")
    p = {
        "id": pid, "nome": nome, "tipo_tecnico": tipo,
        "o_que_e": desc or "Explicação pendente: item listado a partir da fonte, ainda sem texto didático.",
        "origem": af("verificado", "padrao_plataforma", "Propriedade definida pelo schema da Metadata API.", e),
        "obrigatoriedade": ob, "default": dflt,
        "dominio": kw.get("dominio") or dominio_auto(tipo, kw.get("vals"), kw.get("natureza"), kw.get("contexto"), kw.get("completa", "sim"), src),
        "disponibilidade": {"desde_versao": ver, "ate_versao": kw.get("ate"), "estado": "verificado" if (ver or kw.get("ate")) else "desconhecido",
                            **({"nota": kw["nota_versao"]} if kw.get("nota_versao") else {})},
        "explicacao": "explicada" if desc else "pendente",
        "estado": kw.get("estado", "verificado"), "evidencias": e}
    if tipo.endswith("[]"): p["cardinalidade"] = "0..n"
    if kw.get("tipo_explicado"): p["tipo_explicado"] = kw["tipo_explicado"]
    if kw.get("rotulo"): p["rotulo_didatico"] = kw["rotulo"]
    if kw.get("finalidade"): p["finalidade"] = kw["finalidade"]
    if kw.get("efeito"): p["efeito"] = kw["efeito"]
    if kw.get("restr"): p["restricoes"] = af("verificado", kw["restr"], None, e)
    if kw.get("exemplo"): p["exemplo"] = kw["exemplo"]
    if kw.get("herdada"): p["herdada_de"] = kw["herdada"]
    if kw.get("notas"): p["notas"] = kw["notas"]
    if ("mdx:" + base) in STRUCTS or kw.get("estrutura"):
        p["estrutura_ref"] = "mdx:" + (kw.get("estrutura") or base)
    return p

def struct(nome, src, usada_por, rows, o_que_e=None):
    sid = "mdx:" + nome
    STRUCTS[sid] = {"nome": nome, "src": src, "usada_por": set(usada_por), "rows": rows, "o_que_e": o_que_e}

def emit_structs():
    for sid, s in sorted(STRUCTS.items()):
        props = [prop(sid, *r[:5], s["src"], **(r[5] if len(r) > 5 else {})) for r in s["rows"]]
        expl = sum(1 for p in props if p["explicacao"] == "explicada")
        save("estruturas", s["nome"], {
            "id": sid, "nome": s["nome"], "natureza": "estrutura_auxiliar",
            "o_que_e": s["o_que_e"] or "Estrutura composta usada como tipo de uma propriedade; não é um metadata type implantável por si só.",
            "usada_por": sorted(s["usada_por"]), "propriedades": props,
            "cobertura": {"estrutural": {"estado": "completa" if not [p for p in props if p["dominio"]["natureza"] == "tipo_composto" and "estrutura_ref" not in p and p["tipo_tecnico"].replace("[]", "") not in MDT_NAMES] else "parcial", "esperado": len(props), "presente": len(props), "nota": "Contagem conforme a seção do subtipo na página oficial; tipos compostos internos sem detalhe tornam a cobertura parcial."},
                          "explicativa": {"estado": "completa" if expl == len(props) else "parcial", "esperado": len(props), "presente": expl},
                          "mapeamento": {"estado": "nao_iniciada", "nota": "Correspondências com campos API não investigadas."}},
            "estado": "verificado", "evidencias": [ev(s["src"])]})

def arquivos(nome, parent=None):
    out = {}
    if parent:
        pt = REG["types"][parent.lower()]
        ch = pt["children"]["types"][nome.lower()]
        out["source_format"] = af("verificado", {"pasta": f"objects/<Objeto>/{ch['directoryName']}/", "arquivo": f"<Nome>.{ch['suffix']}-meta.xml"},
                                   "Componente filho decomposto pelo Salesforce CLI (estratégia folderPerType do tipo pai). Sufixo '-meta.xml' segue a convenção do source format.",
                                   [ev("src:sdr-registry", f"types.{parent.lower()}.children.types.{nome.lower()}")])
        out["metadata_api_format"] = af("verificado", {"pasta": f"{pt['directoryName']}/", "arquivo": f"<Objeto>.{pt['suffix']}", "elemento": "definido dentro do arquivo do tipo pai"},
                                        None, [ev("src:sdr-registry", f"types.{parent.lower()}")])
        return out
    t = REG["types"][nome.lower()]
    out["source_format"] = af("verificado", {"pasta": f"{t['directoryName']}/", "arquivo": f"<Nome>.{t['suffix']}-meta.xml"},
                              "Pasta e sufixo do registro do Salesforce CLI; sufixo '-meta.xml' segue a convenção do source format.",
                              [ev("src:sdr-registry", f"types.{nome.lower()}")])
    out["metadata_api_format"] = af("verificado", {"pasta": f"{t['directoryName']}/", "arquivo": f"<Nome>.{t['suffix']}"}, None,
                                    [ev("src:sdr-registry", f"types.{nome.lower()}")])
    if t.get("strategies", {}).get("decomposition"):
        out["decomposicao"] = af("verificado", t["strategies"], "No source format, componentes filhos ficam em subpastas por tipo.", [ev("src:sdr-registry", f"types.{nome.lower()}.strategies")])
    return out

def suporte(nome):
    st, nota = MS.get(nome, (None, None))
    if st is None:
        return af("desconhecido", None, "Tipo não encontrado em METADATA_SUPPORT.md.")
    m = {"✅": "suportado", "⚠️": "suportado_com_ressalvas", "❌": "nao_suportado_pelo_cli"}[st]
    return af("verificado", {"status": m, "nota_fonte": nota or None}, "Suporte do Salesforce CLI (source-deploy-retrieve), não do Metadata API em geral.", [ev("src:sdr-metadata-support")])

def mdt(nome, src, o_que_e, finalidade, desde, rows, parent=None, exemplo=None, estende="Metadata", setup=None,
        cobertura_nota=None, completa=True, alertas=None, recs=None, divergencias=None, curinga=None, extra_props=None, arquivos_prontos=None):
    props = [prop("mdt:" + nome, *r[:5], src, **(r[5] if len(r) > 5 else {})) for r in rows]
    if extra_props: props += extra_props
    used = sorted({p["estrutura_ref"] for p in props if "estrutura_ref" in p})
    expl = sum(1 for p in props if p["explicacao"] == "explicada")
    unres = sorted(p["nome"] for p in props if p["dominio"]["natureza"] == "tipo_composto" and "estrutura_ref" not in p and p["tipo_tecnico"].replace("[]", "") not in MDT_NAMES)
    MDT_NAMES.extra.add(nome)
    arq = arquivos_prontos if arquivos_prontos is not None else arquivos(nome, parent)
    if curinga is not None:
        arq["curinga_package_xml"] = af("verificado", curinga, None, [ev(src)])
    obj = {
        "id": "mdt:" + nome, "nome": nome, "o_que_e": o_que_e, "finalidade": finalidade, "estende": estende,
        "arquivos": arq,
        "disponibilidade": {"desde_versao": desde, "ate_versao": None, "estado": "verificado"},
        "suporte_cli": suporte(nome),
        "setup": setup or af("desconhecido", None, "Caminho no Setup não validado nesta sessão."),
        "propriedades": props, "estruturas": used,
        "cobertura": {
            "estrutural": {"estado": "completa" if (completa and not unres) else "parcial", "esperado": len(props) if completa else None, "presente": len(props),
                           "nota": (cobertura_nota or "Universo esperado = tabela Fields da página oficial 68.0 (mais fullName herdado quando declarado).")
                                   + (f" Primeiro nível completo; {len(unres)} propriedade(s) de tipo composto ainda sem estrutura detalhada: {', '.join(unres)}." if unres else "")},
            "explicativa": {"estado": "completa" if expl == len(props) else "parcial", "esperado": len(props), "presente": expl},
            "mapeamento": {"estado": "parcial", "nota": "Correspondências registradas apenas onde há evidência; demais pendentes."}},
        "recomendacoes": recs or [], "alertas": alertas or [], "divergencias_documentais": divergencias or [],
        "estado": "verificado", "evidencias": [ev(src), ev("src:sdr-registry"), ev("src:sdr-metadata-support")]}
    if parent: obj["componente_filho_de"] = "mdt:" + parent
    if exemplo: obj["exemplo_xml"] = {"xml": exemplo, "natureza": "didatico_projeto", "nota": "Exemplo escrito pelo projeto apenas com elementos documentados; sem dados reais."}
    for sid in used:
        if sid in STRUCTS: STRUCTS[sid]["usada_por"].add("mdt:" + nome)
    save("metadata-types", nome, obj)
    return obj

FULLNAME_HERDADO = lambda src, desc="Nome completo (API name) do componente; herdado do tipo Metadata.": ("fullName", "string", "?", None, desc, {"herdada": "Metadata"})



def arquivos_settings(nome, base_arquivo, src):
    """Arquivos de um tipo *Settings: pasta settings/ e arquivo <Base>.settings (o registro do CLI só conhece o tipo genérico Settings).
    Use em mdt(..., arquivos_prontos=arquivos_settings(...)). base_arquivo=None registra o nome do arquivo como desconhecido."""
    if base_arquivo is None:
        a = af("desconhecido", {"pasta": "settings/"}, "Nome-base do arquivo não confirmado na página do tipo.", [ev("src:sdr-registry", "types.settings")])
        return {"source_format": a, "metadata_api_format": a}
    return {"source_format": af("verificado", {"pasta": "settings/", "arquivo": f"{base_arquivo}.settings-meta.xml"},
                "Pasta e sufixo do tipo genérico Settings no registro do Salesforce CLI; o nome-base do arquivo vem da página do tipo.",
                [ev("src:sdr-registry", "types.settings"), ev(src)]),
            "metadata_api_format": af("verificado", {"pasta": "settings/", "arquivo": f"{base_arquivo}.settings"},
                f"Um único arquivo; no package.xml, o tipo é Settings e o membro é {base_arquivo}.", [ev(src)])}


def P(nome, tipo, desde=None, descricao=None, req="N", **kw):
    """Linha de propriedade para mdt()/struct(). req: 'S' obrigatória, 'N' não marcada, 'C:condição', '?' desconhecida.
    kw: vals=[(valor, descrição)], estrutura=, default=(forma, valor, nota), ate=, notas=[...], natureza=, contexto=, completa=, restr=, estado=, herdada=."""
    return (nome, tipo, req, desde, descricao, kw)
