#!/usr/bin/env python3
"""Ferramentas da base sf-tutor (insumos do tutorial em grafo).

Uso (a partir de ai-help/claude/insumos-grafo/):
    python3 ferramentas/sftutor.py inventario      # gera inventarios/ a partir dos snapshots e do catálogo
    python3 ferramentas/sftutor.py validar         # valida schemas, referências e regras de confiabilidade
    python3 ferramentas/sftutor.py gerar           # gera gerado/ (fichas completas, grafo, busca, cobertura)
    python3 ferramentas/sftutor.py cobertura       # gera relatorios/cobertura.md
    python3 ferramentas/sftutor.py auditar-rascunhos   # inventarios/rascunhos-nomes.json
    python3 ferramentas/sftutor.py importar-wsdl <metadata.wsdl>  # inventarios/wsdl-schema.json
    python3 ferramentas/sftutor.py tudo            # inventario + gerar + cobertura + validar

Saídas são determinísticas: chaves ordenadas, sem carimbo de hora.
"""
import glob, hashlib, json, os, re, shutil, sys, tempfile
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_NS = "http://soap.sforce.com/2006/04/metadata"
ESTADOS = {"verificado", "desconhecido", "nao_aplicavel", "nao_exposto", "bloqueado"}
PASTAS = {"nuvens": "nuvem", "classificacoes": "classificacao", "subclassificacoes": "subclassificacao", "funcionalidades": "funcionalidade",
          "metadata-types": "metadata-type", "estruturas": "estrutura", "objetos-api": "objeto-api", "relacionamentos": "relacionamento"}
DOMINIOS_FONTE = ("https://developer.salesforce.com/", "https://help.salesforce.com/", "https://github.com/forcedotcom/", "https://www.npmjs.com/package/@salesforce/", "https://www.salesforce.com/")


def ler(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def gravar(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def gravar_texto(p, txt):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(txt)


# --------------------------------------------------------------------------- carga
def carregar(base=BASE):
    cat = os.path.join(base, "catalogo")
    C = {"salesforce": ler(os.path.join(cat, "salesforce.json")), "_arquivos": {}}
    for pasta in PASTAS:
        C[pasta] = {}
        for p in sorted(glob.glob(os.path.join(cat, pasta, "*.json"))):
            d = ler(p)
            if d.get("id") in C[pasta]:
                C.setdefault("_duplicados", []).append(d.get("id"))
            C[pasta][d.get("id")] = d
            C["_arquivos"][d.get("id")] = os.path.relpath(p, base)
    C["fontes"] = {f["id"]: f for f in ler(os.path.join(base, "fontes", "registro.json"))["fontes"]}
    C["escopo"] = ler(os.path.join(base, "config", "escopo.json"))
    C["versoes"] = ler(os.path.join(base, "config", "versoes.json"))
    marcas = os.path.join(base, "config", "marcas.json")
    C["marcas"] = ler(marcas) if os.path.exists(marcas) else None
    inv = os.path.join(base, "inventarios", "metadata-types-v68.json")
    C["inventario"] = ler(inv) if os.path.exists(inv) else None
    return C


def subitens(C):
    """Índice de propriedades (mdt/mdx) e campos (obj) por id."""
    idx = {}
    for pasta in ("metadata-types", "estruturas"):
        for e in C[pasta].values():
            for p in e.get("propriedades", []):
                idx[p["id"]] = (e["id"], p)
    for o in C["objetos-api"].values():
        for c in o.get("campos", []):
            idx[c["id"]] = (o["id"], c)
    return idx


def todas_ids(C):
    ids = {"salesforce"}
    for pasta in PASTAS:
        ids |= set(C[pasta])
    return ids


# --------------------------------------------------------------------------- snapshots e inventário
def ler_metadata_support(base=BASE):
    rows = []
    for l in open(os.path.join(base, "fontes", "snapshots", "sdr-13.12.0", "METADATA_SUPPORT.md"), encoding="utf-8"):
        if l.startswith("|") and not l.startswith("|:") and not l.startswith("|Metadata Type"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            rows.append((c[0], c[1], c[2] if len(c) > 2 else ""))
    return rows


def cmd_inventario(base=BASE):
    reg = ler(os.path.join(base, "fontes", "snapshots", "sdr-13.12.0", "metadataRegistry.json"))
    ms = ler_metadata_support(base)
    esc = ler(os.path.join(base, "config", "escopo.json"))["classificacao_core_por_item"]
    filhos = {}
    for tid, t in reg["types"].items():
        for cid, ch in (t.get("children") or {}).get("types", {}).items():
            filhos[ch["name"]] = (t["name"], ch)
    por_nome = {t["name"]: t for t in reg["types"].values()}
    cad = {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(base, "catalogo", "metadata-types", "*.json"))}
    status_map = {"✅": "suportado", "⚠️": "suportado_com_ressalvas", "❌": "nao_suportado_pelo_cli"}
    itens = []
    for nome, st, nota in ms:
        r = {"nome": nome, "categoria": "metadata_type", "suporte_cli": status_map.get(st, "desconhecido"), "nota_suporte": nota or None,
             "fontes": ["src:sdr-metadata-support"]}
        if nome in por_nome:
            t = por_nome[nome]
            r["registro_sdr"] = {"pasta": t.get("directoryName"), "sufixo": t.get("suffix"), "em_pasta": t.get("inFolder"),
                                 "decomposicao": (t.get("strategies") or {}).get("decomposition")}
            r["fontes"].append("src:sdr-registry")
        elif nome in filhos:
            pai, ch = filhos[nome]
            r["registro_sdr"] = {"filho_de": pai, "pasta": ch.get("directoryName"), "sufixo": ch.get("suffix")}
            r["fontes"].append("src:sdr-registry")
        elif nome.endswith("Settings"):
            r["registro_sdr"] = {"familia": "Settings", "nota": "Resolvido pelo tipo genérico Settings do CLI (pasta settings, sufixo settings); nome físico por tipo a confirmar."}
            r["fontes"].append("src:sdr-registry")
        else:
            r["registro_sdr"] = None
        r["recorte_core"] = "incluido" if nome in esc["incluidos"] else ("excluido" if nome in esc["excluidos"] else "pendente")
        r["cadastro"] = f"catalogo/metadata-types/{nome}.json" if nome in cad else None
        itens.append(r)
    itens.sort(key=lambda x: x["nome"])
    resumo = {"total": len(itens),
              "suporte_cli": {k: sum(1 for i in itens if i["suporte_cli"] == k) for k in sorted(set(status_map.values()))},
              "com_registro_sdr": sum(1 for i in itens if i["registro_sdr"]),
              "recorte_core": {k: sum(1 for i in itens if i["recorte_core"] == k) for k in ("incluido", "excluido", "pendente")},
              "cadastrados": sum(1 for i in itens if i["cadastro"])}
    gravar(os.path.join(base, "inventarios", "metadata-types-v68.json"), {
        "id": "inventario-metadata-types", "versao_api": "68.0", "universo": "METADATA_SUPPORT.md (v68) — denominador do inventário",
        "nota": "Lista de metadata types; estruturas auxiliares (subtipos) não entram aqui e são inventariadas em catalogo/estruturas e, quando houver WSDL, em inventarios/wsdl-schema.json.",
        "resumo": resumo, "itens": itens})
    # objetos: catalogados + alvos citados ainda não catalogados
    C = carregar(base)
    cit = {}
    for o in C["objetos-api"].values():
        for c in o["campos"]:
            for a in (c.get("referencia") or {}).get("alvos", []):
                if not a.startswith("obj:"):
                    cit.setdefault(a, set()).add(c["id"])
    gravar(os.path.join(base, "inventarios", "objetos-api.json"), {
        "id": "inventario-objetos-api", "versao_api": "68.0",
        "nota": "Universo completo de objetos da plataforma ainda não enumerado. Lista = objetos catalogados + alvos de referência citados em campos e ainda não catalogados.",
        "catalogados": sorted(C["objetos-api"]),
        "citados_nao_catalogados": [{"nome": k, "citado_por": sorted(v)} for k, v in sorted(cit.items())]})
    print(f"inventario: {resumo}")
    return resumo


# --------------------------------------------------------------------------- validação
class Erros:
    def __init__(self):
        self.erros, self.avisos = [], []

    def e(self, msg):
        self.erros.append(msg)

    def a(self, msg):
        self.avisos.append(msg)


def validar_schemas(C, R, base=BASE):
    try:
        import jsonschema
        from referencing import Registry, Resource
    except ImportError:
        R.e("dependência ausente: instale requirements.txt (jsonschema)")
        return
    sdir = os.path.join(base, "schemas")
    res = []
    for p in glob.glob(os.path.join(sdir, "*.schema.json")):
        s = ler(p)
        res.append((s["$id"], Resource.from_contents(s)))
    reg = Registry().with_resources(res)
    def chk(nome_schema, doc, rotulo):
        s = ler(os.path.join(sdir, nome_schema + ".schema.json"))
        v = jsonschema.Draft202012Validator(s, registry=reg)
        for err in sorted(v.iter_errors(doc), key=lambda x: list(x.absolute_path)):
            R.e(f"schema[{rotulo}] {'/'.join(map(str, err.absolute_path))}: {err.message[:200]}")
    chk("salesforce", C["salesforce"], "salesforce")
    if C.get("marcas"):
        chk("marcas", C["marcas"], "config/marcas")
    for pasta, sch in PASTAS.items():
        for i, d in C[pasta].items():
            chk(sch, d, i)


def validar_referencias(C, R):
    ids = todas_ids(C)
    sub = subitens(C)
    for d in C.get("_duplicados", []):
        R.e(f"id duplicado: {d}")
    # nomes de arquivo coerentes
    for pasta in PASTAS:
        for i in C[pasta]:
            arq = os.path.splitext(os.path.basename(C["_arquivos"][i]))[0]
            esperado = i.split(":", 1)[1]
            if arq != esperado:
                R.e(f"arquivo {C['_arquivos'][i]} não corresponde ao id {i}")
    sf = C["salesforce"]
    for n in sf["nuvens"] + sf["classificacoes"]:
        if n not in ids: R.e(f"salesforce referencia {n} inexistente")
    for c in C["classificacoes"].values():
        for s in c["subclassificacoes"]:
            if s not in C["subclassificacoes"]: R.e(f"{c['id']} referencia {s} inexistente")
            elif C["subclassificacoes"][s]["classificacao"] != c["id"]: R.e(f"{s} não aponta de volta para {c['id']}")
    for s in C["subclassificacoes"].values():
        if s["classificacao"] not in C["classificacoes"]: R.e(f"{s['id']}: classificação {s['classificacao']} inexistente")
        for f in s["funcionalidades"]:
            if f not in C["funcionalidades"]: R.e(f"{s['id']}: funcionalidade {f} inexistente")
    # funcionalidades
    for f in C["funcionalidades"].values():
        cps = [f["classificacao_principal"]] + f["classificacoes_secundarias"]
        for cp in cps:
            if cp["classificacao"] not in C["classificacoes"]: R.e(f"{f['id']}: classificação {cp['classificacao']} inexistente")
            s = C["subclassificacoes"].get(cp["subclassificacao"])
            if not s: R.e(f"{f['id']}: subclassificação {cp['subclassificacao']} inexistente"); continue
            if s["classificacao"] != cp["classificacao"]: R.e(f"{f['id']}: {cp['subclassificacao']} não pertence a {cp['classificacao']}")
            if f["id"] not in s["funcionalidades"]: R.e(f"{f['id']} não listada em {s['id']}")
        rep = f["representacoes"]
        for r in rep["metadata_types"]:
            if r["ref"] not in C["metadata-types"]: R.e(f"{f['id']}: metadata type {r['ref']} inexistente")
        for r in rep["objetos_api"]:
            if r["ref"] not in C["objetos-api"]: R.e(f"{f['id']}: objeto {r['ref']} inexistente")
        tipos_aus = {a["tipo"] for a in rep["ausencias"]}
        if not rep["metadata_types"] and "metadata_type" not in tipos_aus:
            R.e(f"{f['id']}: sem metadata type e sem ausência declarada (investigação ou motivo)")
        if not rep["objetos_api"] and "objeto_api" not in tipos_aus:
            R.e(f"{f['id']}: sem objeto API e sem ausência declarada")
    # nuvens
    for n in C["nuvens"].values():
        for ca in n["classificacoes_aplicaveis"]:
            if ca["classificacao"] not in C["classificacoes"]: R.e(f"{n['id']}: {ca['classificacao']} inexistente")
            for sc in ca["subclassificacoes"]:
                if sc["subclassificacao"] not in C["subclassificacoes"]: R.e(f"{n['id']}: {sc['subclassificacao']} inexistente")
                for fid in sc["funcionalidades"]:
                    if fid not in C["funcionalidades"]: R.e(f"{n['id']}: {fid} inexistente")
    # estruturas e metadata types
    for e in list(C["metadata-types"].values()) + list(C["estruturas"].values()):
        for p in e["propriedades"]:
            if not p["id"].startswith(e["id"] + "."): R.e(f"{p['id']} não pertence a {e['id']}")
            if p.get("estrutura_ref") and p["estrutura_ref"] not in C["estruturas"]: R.e(f"{p['id']}: estrutura {p['estrutura_ref']} inexistente")
        nomes = [p["nome"] for p in e["propriedades"]]
        if len(nomes) != len(set(nomes)): R.e(f"{e['id']}: propriedades repetidas")
    for e in C["estruturas"].values():
        for u in e["usada_por"]:
            if u not in C["metadata-types"] and u not in C["estruturas"]: R.e(f"{e['id']}: usada_por {u} inexistente")
    for m in C["metadata-types"].values():
        if m.get("componente_filho_de") and m["componente_filho_de"] not in C["metadata-types"]: R.e(f"{m['id']}: pai inexistente")
    # objetos
    for o in C["objetos-api"].values():
        for c in o["campos"]:
            if not c["id"].startswith(o["id"] + "."): R.e(f"{c['id']} não pertence a {o['id']}")
            for a in (c.get("referencia") or {}).get("alvos", []):
                if a.startswith("obj:") and a not in C["objetos-api"]: R.e(f"{c['id']}: alvo {a} inexistente")
        nomes = [c["nome"] for c in o["campos"]]
        if len(nomes) != len(set(nomes)): R.e(f"{o['id']}: campos repetidos")
    # relacionamentos
    for r in C["relacionamentos"].values():
        for lado in ("origem", "destino"):
            ent = r[lado]["entidade"]
            if ent not in ids: R.e(f"{r['id']}: {lado} {ent} inexistente"); continue
            if r[lado].get("campo"):
                sid = f"{ent}.{r[lado]['campo']}"
                if sid not in sub: R.e(f"{r['id']}: {lado} {sid} inexistente")
    # órfãos
    usados_mdt = {r["ref"] for f in C["funcionalidades"].values() for r in f["representacoes"]["metadata_types"]}
    usados_obj = {r["ref"] for f in C["funcionalidades"].values() for r in f["representacoes"]["objetos_api"]}
    rel_ents = {r[l]["entidade"] for r in C["relacionamentos"].values() for l in ("origem", "destino")}
    for m in C["metadata-types"]:
        if m not in usados_mdt: R.e(f"órfão: {m} não é representação de nenhuma funcionalidade")
    for o in C["objetos-api"]:
        if o not in usados_obj and o not in rel_ents: R.e(f"órfão: {o} sem funcionalidade nem relacionamento")
    for f in C["funcionalidades"]:
        if not any(f in s["funcionalidades"] for s in C["subclassificacoes"].values()): R.e(f"órfão: {f} fora de qualquer subclassificação")
    for e in C["estruturas"]:
        if not any(p.get("estrutura_ref") == e for x in list(C["metadata-types"].values()) + list(C["estruturas"].values()) for p in x["propriedades"]):
            R.e(f"órfão: estrutura {e} não usada por nenhuma propriedade")


def _evs_ok(x):
    return bool(x.get("evidencias"))


def validar_marcas(C, R):
    """Logos por referência: alvo existente (centro ou nuvem), um logo por alvo, só domínios permitidos."""
    M = C.get("marcas")
    if not M:
        return
    from urllib.parse import urlparse
    alvos_validos = {"salesforce"} | set(C["nuvens"])
    vistos = set()
    for it in M["itens"]:
        a = it.get("alvo")
        host = urlparse(it["url"]).hostname
        if host not in M["dominios_permitidos"]:
            R.e(f"marcas: domínio não permitido em {it['url']}")
        if a is None:
            continue
        if a not in alvos_validos:
            R.e(f"marcas: alvo {a} não existe (só o centro e nuvens catalogadas recebem logo)")
        if a in vistos:
            R.e(f"marcas: mais de um logo para {a}")
        vistos.add(a)

def validar_regras(C, R):
    inv_nomes = {i["nome"] for i in C["inventario"]["itens"]} if C["inventario"] else None
    if inv_nomes is None:
        R.e("inventário ausente: rode 'inventario' antes de 'validar'")
    proibidos = {"User", "Organization", "CurrencyType", "DatedConversionRate", "UserLogin", "LoginHistory", "PermissionSetAssignment"}
    for m in C["metadata-types"].values():
        if inv_nomes is not None and m["nome"] not in inv_nomes:
            R.e(f"{m['id']}: nome fora da lista oficial de metadata types v68 (possível tipo inventado)")
        if m["nome"] in proibidos:
            R.e(f"{m['id']}: objeto de dados cadastrado como metadata type")
    sub = subitens(C)
    # afirmações com valor sim/condicional/default precisam de evidência
    def checar_item(owner, p):
        ob = p["obrigatoriedade"]
        if ob["valor"] in ("sim", "condicional") and not (ob["estado"] == "verificado" and _evs_ok(ob)):
            R.e(f"{p['id']}: obrigatoriedade '{ob['valor']}' sem evidência verificada")
        if ob["estado"] == "verificado" and not _evs_ok(ob):
            R.e(f"{p['id']}: obrigatoriedade verificada sem evidência")
        if ob["valor"] == "condicional" and not ob.get("condicao"):
            R.e(f"{p['id']}: obrigatoriedade condicional sem condição")
        df = p["default"]
        if df["forma"] in ("valor", "false", "null", "string_vazia", "ausente_no_xml") and not (df["estado"] == "verificado" and _evs_ok(df)):
            R.e(f"{p['id']}: default '{df['forma']}' sem evidência verificada")
        if df["forma"] == "false" and df.get("valor") not in (False, None):
            R.e(f"{p['id']}: default forma false com valor diferente")
        dom = p["dominio"]
        if dom["natureza"] == "enum_fechado" and dom.get("estado") == "verificado" and not dom.get("valores") and not dom.get("contexto"):
            R.e(f"{p['id']}: enum fechado verificado sem valores nem contexto")
        if dom["natureza"] == "enum_fechado" and dom.get("lista_completa") == "sim" and not dom.get("valores"):
            R.e(f"{p['id']}: lista declarada completa sem valores")
        if dom["natureza"] == "lista_dinamica" and dom.get("valores") and dom.get("lista_completa") == "sim":
            R.e(f"{p['id']}: domínio dinâmico declarado como lista completa")
        if dom.get("estado") == "verificado" and not _evs_ok(dom):
            R.e(f"{p['id']}: domínio verificado sem evidência")
        if p["estado"] == "verificado" and not p["evidencias"]:
            R.e(f"{p['id']}: item verificado sem evidência")
        if p["explicacao"] == "explicada" and p["o_que_e"].startswith("Explicação pendente"):
            R.e(f"{p['id']}: marcado como explicado sem explicação")
    for x in list(C["metadata-types"].values()) + list(C["estruturas"].values()):
        for p in x["propriedades"]:
            checar_item(x["id"], p)
    for o in C["objetos-api"].values():
        apis_ok = {e["api"] for e in o["exposicoes"] if e["estado"] not in ("nao_exposto",)}
        apis_ver = {e["api"] for e in o["exposicoes"] if e["estado"] == "verificado"}
        vistas = [e["api"] for e in o["exposicoes"]]
        if len(vistas) != len(set(vistas)): R.e(f"{o['id']}: exposição repetida por API")
        if not apis_ver: R.e(f"{o['id']}: nenhuma exposição verificada")
        for c in o["campos"]:
            checar_item(o["id"], c)
            for a in c["apis"]:
                if a not in apis_ok: R.e(f"{c['id']}: campo atribuído à API {a}, que não expõe o objeto")
            pa = c["propriedades_api"]
            if c.get("somente_leitura") and (pa.get("create") or pa.get("update")):
                R.e(f"{c['id']}: somente leitura contradiz create/update")
            if pa.get("nillable") is False and c["obrigatoriedade"]["valor"] == "sim" and not _evs_ok(c["obrigatoriedade"]):
                R.e(f"{c['id']}: obrigatoriedade deduzida de não-anulável")
        tooling_only = "padrao" not in apis_ok
        sq = o["apex"]["consulta_soql_direta"]
        if tooling_only and sq["estado"] == "verificado" and sq.get("valor") is True:
            R.e(f"{o['id']}: consulta Apex direta oferecida para objeto exposto só na Tooling API")
        for q in o["consultas"]:
            if q["api"] not in apis_ok: R.e(f"{o['id']}: consulta na API {q['api']}, que não expõe o objeto")
            validar_soql(o, q, R)
    # coerência das coberturas declaradas
    nomes_mdt = {m["nome"] for m in C["metadata-types"].values()}
    for x in list(C["metadata-types"].values()) + list(C["estruturas"].values()) + list(C["objetos-api"].values()):
        est = x["cobertura"]["estrutural"]
        itens = x.get("propriedades", x.get("campos", []))
        if est["estado"] == "completa":
            if est.get("esperado") is None or est["esperado"] != len(itens):
                R.e(f"{x['id']}: cobertura estrutural 'completa' sem esperado == presente")
            soltos = [p["nome"] for p in itens if p["dominio"]["natureza"] == "tipo_composto" and not p.get("estrutura_ref") and p["tipo_tecnico"].replace("[]", "") not in nomes_mdt and x["id"].startswith(("mdt:", "mdx:"))]
            if soltos:
                R.e(f"{x['id']}: cobertura estrutural 'completa' com tipos compostos não detalhados: {', '.join(soltos[:5])}")
            for sref in x.get("estruturas", []):
                if sref in C["estruturas"] and C["estruturas"][sref]["cobertura"]["estrutural"]["estado"] != "completa":
                    R.e(f"{x['id']}: cobertura estrutural 'completa' usando estrutura parcial {sref}")
        exp = x["cobertura"]["explicativa"]
        if exp["estado"] == "completa" and any(p["explicacao"] != "explicada" for p in itens):
            R.e(f"{x['id']}: cobertura explicativa 'completa' com itens pendentes")
    # relacionamentos
    for r in C["relacionamentos"].values():
        if r["estado"] == "verificado" and not r["evidencias"]:
            R.e(f"{r['id']}: verificado sem evidência")
        if r["tipo"] == "correspondencia_xml_api":
            o, d = r["origem"]["entidade"], r["destino"]["entidade"]
            if not (o.startswith("mdt:") and d.startswith("obj:")):
                R.e(f"{r['id']}: correspondência XML/API deve ir de mdt: para obj:")
            nat = r.get("natureza_correspondencia")
            if not nat: R.e(f"{r['id']}: correspondência sem natureza")
            if nat == "direta" and not (r["estado"] == "verificado" and r["evidencias"]):
                R.e(f"{r['id']}: correspondência direta sem evidência verificada")
            if nat in ("direta", "parcial", "transformada") and r["estado"] != "verificado":
                R.e(f"{r['id']}: natureza '{nat}' afirmada sem verificação (use 'desconhecida')")
        if r["tipo"] == "referencia_campo":
            if not r["origem"].get("campo"): R.e(f"{r['id']}: referência sem campo de origem")
            else:
                sid = f"{r['origem']['entidade']}.{r['origem']['campo']}"
                item = sub.get(sid)
                if item and r["destino"]["entidade"] not in (item[1].get("referencia") or {}).get("alvos", []):
                    R.e(f"{r['id']}: destino não consta nos alvos do campo {sid}")
        card = r.get("cardinalidade_registros")
        if card and card["estado"] == "verificado" and not card.get("evidencias"):
            R.e(f"{r['id']}: cardinalidade verificada sem evidência")
    # piloto obrigatório
    regras_piloto(C, R)
    # exemplos XML
    for m in C["metadata-types"].values():
        if "exemplo_xml" in m:
            validar_xml(C, m, R)
        else:
            R.a(f"{m['id']}: sem exemplo XML")


def regras_piloto(C, R):
    rels = list(C["relacionamentos"].values())
    def tem(o, campo, d):
        return any(r["tipo"] == "referencia_campo" and r["origem"]["entidade"] == o and r["origem"].get("campo") == campo and r["destino"]["entidade"] == d for r in rels)
    for campo, d in (("AssigneeId", "obj:User"), ("PermissionSetId", "obj:PermissionSet"), ("PermissionSetGroupId", "obj:PermissionSetGroup")):
        if not tem("obj:PermissionSetAssignment", campo, d): R.e(f"piloto: falta PermissionSetAssignment.{campo} -> {d}")
    if not tem("obj:User", "ProfileId", "obj:Profile"): R.e("piloto: falta User.ProfileId -> Profile")
    if any(r["origem"]["entidade"] == "obj:PermissionSetAssignment" and r["destino"]["entidade"] == "obj:Profile" for r in rels):
        R.e("piloto: Profile não deve ser ligado via PermissionSetAssignment")
    if "func:usuarios" in C["funcionalidades"]:
        f = C["funcionalidades"]["func:usuarios"]
        if f["representacoes"]["metadata_types"]: R.e("piloto: Usuários não deve ter metadata type")
    psa = C["objetos-api"].get("obj:PermissionSetAssignment")
    if psa and not psa["juncao"]: R.e("piloto: PermissionSetAssignment deve ser marcado como junção")
    for n in ("CustomObject", "CustomField", "Profile", "PermissionSet", "PermissionSetGroup", "RecordType", "ValidationRule", "Flow", "PathAssistant", "FlexiPage", "QuickAction", "CustomTab"):
        if "mdt:" + n not in C["metadata-types"]: R.e(f"piloto: falta mdt:{n}")
    for n in ("RecordType", "ValidationRule", "Flow", "PathAssistant", "FlexiPage", "QuickAction", "CustomTab"):
        fs = [f for f in C["funcionalidades"].values() if any(r["ref"] == "mdt:" + n for r in f["representacoes"]["metadata_types"])]
        if not fs: R.e(f"piloto: mdt:{n} sem funcionalidade")
        elif not any(f["classificacoes_secundarias"] for f in fs): R.e(f"piloto: funcionalidade de mdt:{n} sem relação secundária")


SOQL_RE = re.compile(r"^\s*SELECT\s+(?P<sel>.+?)\s+FROM\s+(?P<obj>\w+)(?P<resto>.*)$", re.I | re.S)


def validar_soql(o, q, R):
    m = SOQL_RE.match(q["soql"])
    if not m:
        R.e(f"{o['id']}: SOQL não reconhecida: {q['soql'][:60]}"); return
    if m.group("obj") != o["nome"]:
        R.e(f"{o['id']}: SOQL consulta {m.group('obj')} em vez de {o['nome']}")
    campos = {c["nome"]: c for c in o["campos"] if q["api"] in c["apis"]}
    rels = {(c.get("referencia") or {}).get("nome_relacionamento"): c for c in o["campos"] if (c.get("referencia") or {}).get("nome_relacionamento")}
    sistema = {"Id"}
    def ok(tok):
        if "." in tok:
            return tok.split(".")[0] in rels
        return tok in campos or tok in sistema
    for tok in [t.strip() for t in m.group("sel").split(",")]:
        if not ok(tok): R.e(f"{o['id']}: SOQL usa '{tok}', ausente dos campos catalogados para a API {q['api']}")
    resto = re.sub(r"'[^']*'", "''", m.group("resto"))
    for tok in re.findall(r"(?:WHERE|AND|OR|ORDER BY)\s+([A-Za-z_][\w.]*)", resto, re.I):
        if not ok(tok): R.e(f"{o['id']}: SOQL filtra/ordena por '{tok}', ausente dos campos catalogados")


def validar_xml(C, m, R):
    try:
        root = ET.fromstring(m["exemplo_xml"]["xml"].encode("utf-8"))
    except ET.ParseError as ex:
        R.e(f"{m['id']}: exemplo XML mal formado: {ex}"); return
    tag = root.tag
    ns, local = (tag[1:].split("}", 1) if tag.startswith("{") else ("", tag))
    if ns != MD_NS: R.e(f"{m['id']}: namespace do exemplo deve ser {MD_NS}")
    if local != m["nome"]: R.e(f"{m['id']}: raiz do exemplo é {local}, esperado {m['nome']}")
    props = {p["nome"]: p for p in m["propriedades"]}
    por_nome_mdt = {x["nome"]: x for x in C["metadata-types"].values()}
    for ch in root:
        nome = ch.tag.split("}", 1)[-1]
        if nome not in props:
            R.e(f"{m['id']}: exemplo usa <{nome}>, que não é propriedade documentada"); continue
        p = props[nome]
        filhos = list(ch)
        if not filhos: continue
        alvo = None
        if p.get("estrutura_ref") in C["estruturas"]:
            alvo = {x["nome"] for x in C["estruturas"][p["estrutura_ref"]]["propriedades"]}
        elif p["tipo_tecnico"].replace("[]", "") in por_nome_mdt:
            alvo = {x["nome"] for x in por_nome_mdt[p["tipo_tecnico"].replace("[]", "")]["propriedades"]}
        if alvo is None:
            R.a(f"{m['id']}: <{nome}> tem filhos, mas o tipo {p['tipo_tecnico']} não está detalhado; filhos não verificados")
            continue
        for g in filhos:
            gn = g.tag.split("}", 1)[-1]
            if gn not in alvo: R.e(f"{m['id']}: <{nome}><{gn}> não é propriedade documentada de {p['tipo_tecnico']}")


def validar_fontes(C, R, base=BASE):
    usadas = set()
    def walk(x):
        if isinstance(x, dict):
            if "fonte" in x and isinstance(x["fonte"], str):
                usadas.add(x["fonte"])
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(C["salesforce"])
    for pasta in PASTAS:
        walk(C[pasta])
    walk(C["versoes"])
    for u in sorted(usadas):
        if u not in C["fontes"]: R.e(f"fonte {u} usada mas não registrada")
    for f in C["fontes"].values():
        if not f["url"].startswith(DOMINIOS_FONTE): R.e(f"{f['id']}: domínio fora da lista de fontes oficiais")
        if not f.get("pertinencia"): R.e(f"{f['id']}: sem nota de pertinência")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", f.get("data_verificacao", "")): R.e(f"{f['id']}: data de verificação inválida")
        if f.get("extracao") and not os.path.exists(os.path.join(base, f["extracao"])): R.e(f"{f['id']}: arquivo de extração ausente")
        if f["checagem_online"]["estado"] == "verificado" and f["metodo"] in ("citada_na_especificacao", "nao_consultada"):
            R.e(f"{f['id']}: checagem online marcada como verificada sem leitura")
        if f["id"] not in usadas: R.a(f"{f['id']}: registrada mas não usada")
    # rastreabilidade: o nome de cada propriedade/campo precisa aparecer na nota de extração de pelo menos uma de suas fontes
    cache = {}
    def texto(fid):
        ex = C["fontes"].get(fid, {}).get("extracao")
        if not ex: return ""
        if ex not in cache:
            with open(os.path.join(base, ex), encoding="utf-8") as fh: cache[ex] = fh.read()
        return cache[ex]
    for pasta, chave in (("metadata-types", "propriedades"), ("estruturas", "propriedades"), ("objetos-api", "campos")):
        for x in C[pasta].values():
            for it in x[chave]:
                padrao = re.compile(r"(?<![A-Za-z])" + re.escape(it["nome"]) + r"(?![A-Za-z0-9])")
                if not any(padrao.search(texto(e["fonte"])) for e in it["evidencias"]):
                    R.e(f"{it['id']}: nome não encontrado nas notas de extração das fontes citadas")


def validar_gerado(R, base=BASE):
    tmp = tempfile.mkdtemp()
    try:
        a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
        gerar(base, a); gerar(base, b)
        ha, hb = hashes(a), hashes(b)
        if ha != hb: R.e("geração não determinística: duas execuções produziram saídas diferentes")
        atual = hashes(os.path.join(base, "gerado"))
        if atual != ha: R.e("gerado/ desatualizado: rode 'gerar'")
    finally:
        shutil.rmtree(tmp)


def hashes(d):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, "**", "*"), recursive=True)):
        if os.path.isfile(p):
            with open(p, "rb") as f:
                out[os.path.relpath(p, d)] = hashlib.sha256(f.read()).hexdigest()
    return out


def validar(base=BASE, checar_gerado=True):
    R = Erros()
    C = carregar(base)
    validar_schemas(C, R, base)
    validar_referencias(C, R)
    validar_regras(C, R)
    validar_marcas(C, R)
    validar_fontes(C, R, base)
    if checar_gerado:
        validar_gerado(R, base)
    return R


# --------------------------------------------------------------------------- geração
def expandir(C, prop, visit):
    p = json.loads(json.dumps(prop))
    ref = p.get("estrutura_ref")
    if ref and ref in C["estruturas"]:
        if ref in visit:
            p["estrutura_expandida"] = {"ref": ref, "ciclo": True}
        else:
            e = C["estruturas"][ref]
            p["estrutura_expandida"] = {"id": ref, "nome": e["nome"], "propriedades": [expandir(C, q, visit | {ref}) for q in e["propriedades"]]}
    return p


def gerar(base=BASE, destino=None):
    C = carregar(base)
    out = destino or os.path.join(base, "gerado")
    if os.path.exists(out):
        shutil.rmtree(out)
    rels = list(C["relacionamentos"].values())
    funcs = C["funcionalidades"]
    vb = C["salesforce"]["versao_base"]
    def rels_de(prefixos):
        return sorted([r for r in rels if any(r[l]["entidade"] in prefixos for l in ("origem", "destino"))], key=lambda r: r["id"])
    # fichas completas por metadata type
    for m in C["metadata-types"].values():
        fs = sorted([f for f in funcs.values() if any(r["ref"] == m["id"] for r in f["representacoes"]["metadata_types"])], key=lambda f: f["id"])
        rr = rels_de({m["id"]})
        relacionados = {}
        for r in rr:
            outro = r["destino"]["entidade"] if r["origem"]["entidade"] == m["id"] else r["origem"]["entidade"]
            if outro.startswith("obj:"):
                relacionados.setdefault(outro, set()).add(r["id"])
        for f in fs:
            for o in f["representacoes"]["objetos_api"]:
                relacionados.setdefault(o["ref"], set()).add(f"representacao_comum_em:{f['id']}")
        mm = json.loads(json.dumps(m))
        mm["propriedades"] = [expandir(C, p, frozenset()) for p in m["propriedades"]]
        gravar(os.path.join(out, "fichas-completas", m["nome"] + ".json"), {
            "versao_base": vb, "metadata_type": mm,
            "funcionalidades": [{"id": f["id"], "nome": f["nome"]} for f in fs],
            "relacionamentos": rr,
            "objetos_relacionados": [{"base_da_relacao": sorted(v), "objeto": C["objetos-api"][k],
                                      "relacionamentos_do_objeto": rels_de({k})} for k, v in sorted(relacionados.items())],
            "nota": "Gerado deterministicamente a partir de catalogo/. Não editar à mão."})
    # fichas por funcionalidade (inclui funcionalidades sem XML)
    for f in funcs.values():
        gravar(os.path.join(out, "fichas-funcionalidade", f["id"].split(":")[1] + ".json"), {
            "versao_base": vb, "funcionalidade": f,
            "metadata_types": [{"id": r["ref"], "nome": C["metadata-types"][r["ref"]]["nome"], "papel": r["papel"], "ficha_completa": f"gerado/fichas-completas/{C['metadata-types'][r['ref']]['nome']}.json"} for r in f["representacoes"]["metadata_types"]],
            "objetos_api": [{"papel": r["papel"], "objeto": C["objetos-api"][r["ref"]], "relacionamentos": rels_de({r["ref"]})} for r in f["representacoes"]["objetos_api"]],
            "nota": "Gerado deterministicamente a partir de catalogo/. Não editar à mão."})
    # grafo
    nos, arestas = [], []
    def no(i, tipo, rot, **kw):
        n = {"id": i, "tipo": tipo, "rotulo": rot}; n.update({k: v for k, v in kw.items() if v is not None}); nos.append(n)
    def ar(o, d, tipo, **kw):
        a = {"origem": o, "destino": d, "tipo": tipo}; a.update({k: v for k, v in kw.items() if v is not None}); arestas.append(a)
    sf = C["salesforce"]
    no("salesforce", "salesforce", sf["nome"], estado=sf["estado"])
    for n in C["nuvens"].values():
        no(n["id"], "nuvem", n["nome_oficial"], sigla=n.get("sigla"), estado=n["estado"], grupo_cor=n["id"])
        ar("salesforce", n["id"], "navegacao_nuvem")
        for ca in n["classificacoes_aplicaveis"]:
            for sc in ca["subclassificacoes"]:
                for fid in sc["funcionalidades"]:
                    ar(n["id"], fid, "nuvem_funcionalidade", via=[ca["classificacao"], sc["subclassificacao"]])
    for c in C["classificacoes"].values():
        no(c["id"], "classificacao", c["nome"], sigla=c["sigla"], rotulo_curto=c["nome_curto"], estado=c["estado"], grupo_cor=c["id"])
        ar("salesforce", c["id"], "navegacao_classificacao")
    for s in C["subclassificacoes"].values():
        no(s["id"], "subclassificacao", s["nome"], sigla=s.get("sigla"), estado=s["estado"], grupo_cor=s["classificacao"])
        ar(s["classificacao"], s["id"], "navegacao_subclassificacao")
    for f in funcs.values():
        no(f["id"], "funcionalidade", f["nome"], rotulo_tecnico=f["nome_tecnico"], estado=f["estado"], grupo_cor=f["classificacao_principal"]["classificacao"], resumo=f["o_que_e"])
        ar(f["classificacao_principal"]["subclassificacao"], f["id"], "classificacao_principal")
        for cs in f["classificacoes_secundarias"]:
            ar(cs["subclassificacao"], f["id"], "classificacao_secundaria", motivo=cs["motivo"])
        for r in f["representacoes"]["metadata_types"]:
            ar(f["id"], r["ref"], "representacao_xml", papel=r["papel"])
        for r in f["representacoes"]["objetos_api"]:
            ar(f["id"], r["ref"], "representacao_objeto_api", papel=r["papel"])
    for m in C["metadata-types"].values():
        no(m["id"], "metadata_type", m["nome"], estado=m["estado"], resumo=m["o_que_e"])
        for p in m["propriedades"]:
            no(p["id"], "propriedade_xml", p["nome"], tipo_tecnico=p["tipo_tecnico"], estado=p["estado"], explicacao=p["explicacao"])
            ar(m["id"], p["id"], "propriedade")
            if p.get("estrutura_ref"): ar(p["id"], p["estrutura_ref"], "tipo_composto")
    for e in C["estruturas"].values():
        no(e["id"], "estrutura_auxiliar", e["nome"], estado=e["estado"])
        for p in e["propriedades"]:
            no(p["id"], "propriedade_xml", p["nome"], tipo_tecnico=p["tipo_tecnico"], estado=p["estado"], explicacao=p["explicacao"])
            ar(e["id"], p["id"], "propriedade")
            # estruturas aninhadas também precisam da ligação de tipo composto (antes só saía de mdt:)
            if p.get("estrutura_ref"): ar(p["id"], p["estrutura_ref"], "tipo_composto")
    for o in C["objetos-api"].values():
        no(o["id"], "objeto_api_juncao" if o["juncao"] else "objeto_api", o["nome"], estado=o["estado"], resumo=o["o_que_e"],
           apis=sorted(e["api"] for e in o["exposicoes"] if e["estado"] == "verificado"))
        for c in o["campos"]:
            no(c["id"], "campo_api", c["nome"], tipo_tecnico=c["tipo_tecnico"], estado=c["estado"], explicacao=c["explicacao"], apis=c["apis"])
            ar(o["id"], c["id"], "campo")
    for r in rels:
        o = r["origem"]["entidade"] + ("." + r["origem"]["campo"] if r["origem"].get("campo") else "")
        d = r["destino"]["entidade"] + ("." + r["destino"]["campo"] if r["destino"].get("campo") else "")
        ar(o, d, r["tipo"], rel_id=r["id"], estado=r["estado"], natureza=r.get("natureza_correspondencia"))
    nos.sort(key=lambda n: n["id"]); arestas.sort(key=lambda a: (a["origem"], a["destino"], a["tipo"]))
    gravar(os.path.join(out, "grafo", "nos.json"), nos)
    gravar(os.path.join(out, "grafo", "arestas.json"), arestas)
    # visões (árvores de navegação; ocorrências apontam para o mesmo id canônico)
    pf = {"id": "salesforce", "filhos": []}
    for cid in sf["classificacoes"]:
        c = C["classificacoes"][cid]
        cn = {"id": cid, "filhos": []}
        for sid in c["subclassificacoes"]:
            s = C["subclassificacoes"][sid]
            cn["filhos"].append({"id": sid, "filhos": [{"id": fid, "ocorrencia": "principal" if funcs[fid]["classificacao_principal"]["subclassificacao"] == sid else "secundaria"} for fid in s["funcionalidades"]]})
        pf["filhos"].append(cn)
    pn = {"id": "salesforce", "filhos": []}
    for nid in sf["nuvens"]:
        n = C["nuvens"][nid]
        pn["filhos"].append({"id": nid, "filhos": [{"id": ca["classificacao"], "filhos": [{"id": sc["subclassificacao"], "filhos": [{"id": f} for f in sc["funcionalidades"]]} for sc in ca["subclassificacoes"]]} for ca in n["classificacoes_aplicaveis"]]})
    gravar(os.path.join(out, "grafo", "visoes.json"), {"por_funcionalidade": pf, "por_nuvem": pn,
                                                      "nota": "Uma funcionalidade pode ocorrer em vários caminhos; todas as ocorrências usam o mesmo id canônico."})
    # índice de busca
    busca = []
    for n in nos:
        textos = {n["rotulo"]}
        for k in ("rotulo_tecnico", "rotulo_curto", "sigla"):
            if n.get(k): textos.add(n[k])
        if n["id"] in funcs:
            textos |= set(funcs[n["id"]].get("aliases", [])) | set(funcs[n["id"]].get("termos_busca", []))
        busca.append({"id": n["id"], "tipo": n["tipo"], "textos": sorted(textos)})
    gravar(os.path.join(out, "grafo", "busca.json"), busca)
    cob = cobertura(C, base)
    gravar(os.path.join(out, "cobertura.json"), cob)
    gerar_site(C, base, out, nos, arestas, {"por_funcionalidade": pf, "por_nuvem": pn}, cob)
    return out


# --------------------------------------------------------------------------- projeção para o site (contrato versionado)
CONTRATO_SITE = {"nome": "sf-tutor-site", "versao": "1.1.0"}
TIPOS_FOLHA = {"campo_api", "propriedade_xml"}          # vivem dentro da entidade-mãe
TIPOS_ARESTA_FOLHA = {"campo", "propriedade"}           # deriváveis da entidade-mãe


def caminho_entidade(i):
    """id canônico -> caminho relativo do arquivo da entidade em gerado/site/entidades/."""
    if i == "salesforce":
        return "entidades/salesforce.json"
    prefixo, nome = i.split(":", 1)
    return f"entidades/{prefixo}/{nome}.json"


def gerar_site(C, base, out, nos, arestas, visoes, cob):
    """Projeção determinística consumida pelo tutorial (apps/sf-tutor). Não é segunda fonte:
    as entidades são cópias dos cadastros de catalogo/, e o grafo-base é o recorte de grafo/ sem as folhas."""
    site = os.path.join(out, "site")
    pai_de = {}
    for a in arestas:
        if a["tipo"] in TIPOS_ARESTA_FOLHA:
            pai_de[a["destino"]] = a["origem"]
    textos = {}
    for b in json.load(open(os.path.join(out, "grafo", "busca.json"), encoding="utf-8")):
        textos[b["id"]] = b["textos"]
    descr = {}
    for f in C["funcionalidades"].values(): descr[f["id"]] = f["o_que_e"]
    for m in C["metadata-types"].values():
        descr[m["id"]] = m["o_que_e"]
        for p in m["propriedades"]: descr[p["id"]] = p.get("o_que_e")
    for e in C["estruturas"].values():
        descr[e["id"]] = e.get("o_que_e")
        for p in e["propriedades"]: descr[p["id"]] = p.get("o_que_e")
    for o in C["objetos-api"].values():
        descr[o["id"]] = o["o_que_e"]
        for c in o["campos"]: descr[c["id"]] = c.get("o_que_e")
    busca = []
    for n in nos:
        item = {"id": n["id"], "tipo": n["tipo"], "rotulo": n["rotulo"], "textos": textos.get(n["id"], [n["rotulo"]])}
        if n["id"] in pai_de: item["pai"] = pai_de[n["id"]]
        if descr.get(n["id"]): item["descricao"] = descr[n["id"]]
        busca.append(item)
    # logos por referência (config/marcas.json): só no centro e nas nuvens catalogadas
    logos = {it["alvo"]: it for it in (C.get("marcas") or {}).get("itens", []) if it.get("alvo")}
    base_nos = []
    for n in nos:
        if n["tipo"] in TIPOS_FOLHA:
            continue
        if n["id"] in logos:
            it = logos[n["id"]]
            n = {**n, "logo": {"url": it["url"], "formato": it["formato"], "marca": it["marca"]}}
        base_nos.append(n)
    base_arestas = [a for a in arestas if a["tipo"] not in TIPOS_ARESTA_FOLHA]
    gravar(os.path.join(site, "grafo-base.json"), {"nos": base_nos, "arestas": base_arestas})
    gravar(os.path.join(site, "visoes.json"), visoes)
    gravar(os.path.join(site, "busca.json"), busca)
    gravar(os.path.join(site, "cobertura.json"), cob)
    entidades = {"salesforce": C["salesforce"]}
    for chave in ("nuvens", "classificacoes", "subclassificacoes", "funcionalidades", "metadata-types", "estruturas", "objetos-api", "relacionamentos"):
        for e in C[chave].values():
            entidades[e["id"]] = e
    for i, e in sorted(entidades.items()):
        if i in logos:
            e = {**e, "logo_marca": {k: logos[i][k] for k in ("marca", "url", "formato", "fornecido_por", "pagina_origem", "verificacao")}}
        gravar(os.path.join(site, caminho_entidade(i)), e)
    reg = json.load(open(os.path.join(base, "fontes", "registro.json"), encoding="utf-8"))
    fontes = {f["id"]: {k: f.get(k) for k in ("titulo", "url", "tipo", "versao", "data_verificacao", "metodo")} for f in reg["fontes"]}
    gravar(os.path.join(site, "fontes.json"), fontes)
    contagem = {}
    for n in nos:
        contagem[n["tipo"]] = contagem.get(n["tipo"], 0) + 1
    gravar(os.path.join(site, "manifest.json"), {
        "contrato": CONTRATO_SITE,
        "versao_base": C["salesforce"]["versao_base"],
        "arquivos": {"grafo_base": "grafo-base.json", "visoes": "visoes.json", "busca": "busca.json", "cobertura": "cobertura.json",
                     "fontes": "fontes.json", "entidades": "entidades/<prefixo>/<nome>.json (salesforce: entidades/salesforce.json)"},
        "contagens": {"nos_por_tipo": dict(sorted(contagem.items())), "entidades": len(entidades), "fontes": len(fontes),
                      "arestas": len(arestas), "arestas_base": len(base_arestas)},
        "regras": ["Campos (campo_api) e propriedades (propriedade_xml) vivem dentro do arquivo da entidade-mãe; o grafo-base não os traz.",
                   "busca.json cobre todos os nós, inclusive folhas, com o id da entidade-mãe em 'pai'.",
                   "Ids canônicos são estáveis; uma ocorrência visual em outro caminho aponta para o mesmo id.",
                   "Nós do centro e das nuvens podem ter 'logo' (url, formato, marca): imagem exibida por referência ao endereço oficial registrado em config/marcas.json; se não carregar, o site usa um substituto.",
                   "Mudança incompatível neste formato sobe a versão maior do contrato."],
        "nota": "Gerado deterministicamente por ferramentas/sftutor.py a partir de catalogo/ e fontes/. Não editar à mão."})


# --------------------------------------------------------------------------- cobertura
def cobertura(C, base=BASE):
    inv = C["inventario"]["resumo"] if C["inventario"] else None
    mdts = list(C["metadata-types"].values())
    props = [p for m in mdts for p in m["propriedades"]]
    sprops = [p for e in C["estruturas"].values() for p in e["propriedades"]]
    campos = [c for o in C["objetos-api"].values() for c in o["campos"]]
    rels = list(C["relacionamentos"].values())
    por_tipo = []
    for m in sorted(mdts, key=lambda x: x["nome"]):
        c = m["cobertura"]
        por_tipo.append({"id": m["id"], "estrutural": c["estrutural"]["estado"], "propriedades_esperadas": c["estrutural"]["esperado"],
                         "propriedades_presentes": len(m["propriedades"]), "explicadas": sum(1 for p in m["propriedades"] if p["explicacao"] == "explicada"),
                         "estruturas": len(m.get("estruturas", [])), "mapeamento": c["mapeamento"]["estado"],
                         "completo": all(c[k]["estado"] == "completa" for k in ("estrutural", "explicativa", "mapeamento"))})
    por_obj = []
    for o in sorted(C["objetos-api"].values(), key=lambda x: x["id"]):
        c = o["cobertura"]
        por_obj.append({"id": o["id"], "estrutural": c["estrutural"]["estado"], "campos_esperados": c["estrutural"]["esperado"], "campos_presentes": len(o["campos"]),
                        "explicados": sum(1 for x in o["campos"] if x["explicacao"] == "explicada"),
                        "exposicoes_verificadas": sorted(e["api"] for e in o["exposicoes"] if e["estado"] == "verificado")})
    return {
        "versao_base": C["salesforce"]["versao_base"],
        "inventario_metadata_types": inv,
        "metadata_types": {"universo_v68": inv["total"] if inv else None, "incluidos_no_recorte_core": inv["recorte_core"]["incluido"] if inv else None,
                           "pendentes_de_classificacao": inv["recorte_core"]["pendente"] if inv else None, "cadastrados": len(mdts),
                           "estruturalmente_completos": sum(1 for x in por_tipo if x["estrutural"] == "completa"),
                           "completos_nas_tres_dimensoes": sum(1 for x in por_tipo if x["completo"])},
        "propriedades": {"listadas_tipos": len(props), "explicadas_tipos": sum(1 for p in props if p["explicacao"] == "explicada"),
                         "listadas_estruturas": len(sprops), "explicadas_estruturas": sum(1 for p in sprops if p["explicacao"] == "explicada"),
                         "universo_total": None, "nota_universo": "Sem WSDL não há denominador confiável do total de propriedades do recorte."},
        "objetos_api": {"catalogados": len(por_obj), "campos_listados": len(campos), "campos_explicados": sum(1 for c in campos if c["explicacao"] == "explicada"),
                        "universo_total": None, "nota_universo": "Universo de objetos da plataforma não enumerado."},
        "relacionamentos": {"total": len(rels), "verificados": sum(1 for r in rels if r["estado"] == "verificado"),
                            "por_tipo": {t: sum(1 for r in rels if r["tipo"] == t) for t in sorted({r["tipo"] for r in rels})}},
        "taxonomia": {"classificacoes": len(C["classificacoes"]), "subclassificacoes": len(C["subclassificacoes"]),
                      "subclassificacoes_com_funcionalidades": sum(1 for s in C["subclassificacoes"].values() if s["funcionalidades"]),
                      "funcionalidades": len(C["funcionalidades"])},
        "por_metadata_type": por_tipo, "por_objeto_api": por_obj}


def cmd_cobertura(base=BASE):
    C = carregar(base)
    k = cobertura(C, base)
    L = ["# Relatório de cobertura", "", f"Base: API {k['versao_base']['api_version']} ({k['versao_base']['release']}), referência {k['versao_base']['data_referencia']}.",
         "Gerado por `ferramentas/sftutor.py cobertura`. Cobertura estrutural, explicativa e de relacionamentos são medidas separadas.", "",
         "## Metadata types", ""]
    mt = k["metadata_types"]
    L += [f"- Universo v68 (METADATA_SUPPORT.md): **{mt['universo_v68']}** tipos.",
          f"- Classificados como incluídos no recorte Core: {mt['incluidos_no_recorte_core']}; pendentes de classificação: {mt['pendentes_de_classificacao']}.",
          f"- Cadastrados: **{mt['cadastrados']}** de {mt['universo_v68']}. Estruturalmente completos (contra a página oficial): {mt['estruturalmente_completos']}. Completos nas três dimensões: {mt['completos_nas_tres_dimensoes']}.",
          "- Porcentagem do recorte Core: não calculada, porque o denominador do recorte ainda não está definido (classificação item a item pendente).", "",
          "| Tipo | Estrutural | Esperadas | Presentes | Explicadas | Estruturas | Mapeamento | Completo |", "|---|---|---|---|---|---|---|---|"]
    for x in k["por_metadata_type"]:
        L.append(f"| {x['id']} | {x['estrutural']} | {x['propriedades_esperadas'] if x['propriedades_esperadas'] is not None else 'n/d'} | {x['propriedades_presentes']} | {x['explicadas']} | {x['estruturas']} | {x['mapeamento']} | {'sim' if x['completo'] else 'não'} |")
    p = k["propriedades"]
    L += ["", "## Propriedades XML", "", f"- Em metadata types: {p['listadas_tipos']} listadas, {p['explicadas_tipos']} explicadas.",
          f"- Em estruturas auxiliares: {p['listadas_estruturas']} listadas, {p['explicadas_estruturas']} explicadas.", f"- Universo total: {p['nota_universo']}", "",
          "## Objetos consultáveis via API", "", f"- Catalogados: {k['objetos_api']['catalogados']}. Campos listados: {k['objetos_api']['campos_listados']}; explicados: {k['objetos_api']['campos_explicados']}.",
          f"- Universo: {k['objetos_api']['nota_universo']}", "", "| Objeto | Estrutural | Esperados | Presentes | Explicados | APIs verificadas |", "|---|---|---|---|---|---|"]
    for x in k["por_objeto_api"]:
        L.append(f"| {x['id']} | {x['estrutural']} | {x['campos_esperados'] if x['campos_esperados'] is not None else 'n/d'} | {x['campos_presentes']} | {x['explicados']} | {', '.join(x['exposicoes_verificadas'])} |")
    r = k["relacionamentos"]; t = k["taxonomia"]
    L += ["", "## Relacionamentos", "", f"- Total: {r['total']}; verificados: {r['verificados']}.", f"- Por tipo: " + ", ".join(f"{a}: {b}" for a, b in r["por_tipo"].items()), "",
          "## Taxonomia e funcionalidades", "", f"- Classificações: {t['classificacoes']}; subclassificações: {t['subclassificacoes']} (com funcionalidades: {t['subclassificacoes_com_funcionalidades']}).",
          f"- Funcionalidades cadastradas: {t['funcionalidades']} (universo de funcionalidades não definido).", ""]
    gravar_texto(os.path.join(base, "relatorios", "cobertura.md"), "\n".join(L))
    print("cobertura: relatorios/cobertura.md")


# --------------------------------------------------------------------------- auditoria de rascunhos
def cmd_auditar(base=BASE):
    repo = os.path.dirname(os.path.dirname(base))  # ai-help/
    arquivos = sorted(glob.glob(os.path.join(repo, "ideia-sf-grafo", "*.md")) + glob.glob(os.path.join(repo, "perplexity", "*.md")) +
                      glob.glob(os.path.join(repo, "internal-obj", "*.md")) + [os.path.join(repo, "fontes.md")])
    inv = {i["nome"] for i in ler(os.path.join(base, "inventarios", "metadata-types-v68.json"))["itens"]}
    C = carregar(base)
    objs = {o["nome"] for o in C["objetos-api"].values()}
    achados = {}
    for a in arquivos:
        txt = open(a, encoding="utf-8").read()
        for tok in re.findall(r"`([A-Z][A-Za-z0-9]+)`", txt):
            achados.setdefault(tok, set()).add(os.path.relpath(a, repo))
    itens = []
    for tok, arqs in sorted(achados.items()):
        itens.append({"nome": tok, "arquivos": sorted(arqs), "na_lista_metadata_v68": tok in inv, "objeto_catalogado": tok in objs,
                      "situacao": "metadata_type_oficial" if tok in inv else ("objeto_api_catalogado" if tok in objs else "nao_confirmado")})
    gravar(os.path.join(base, "inventarios", "rascunhos-nomes.json"), {
        "id": "auditoria-nomes-rascunhos", "metodo": "Identificadores entre crases, iniciados em maiúscula, nos rascunhos de ai-help/ (exceto ai-help/claude/). Comparados com METADATA_SUPPORT.md v68 e com os objetos catalogados.",
        "nota": "'nao_confirmado' não significa inexistente: pode ser objeto API, campo, enum, produto ou nome inventado. Exige investigação item a item.",
        "resumo": {k: sum(1 for i in itens if i["situacao"] == k) for k in ("metadata_type_oficial", "objeto_api_catalogado", "nao_confirmado")}, "itens": itens})
    print(f"auditoria: {len(itens)} nomes")


# --------------------------------------------------------------------------- WSDL
XS = "{http://www.w3.org/2001/XMLSchema}"


def importar_wsdl(caminho, destino=None):
    root = ET.parse(caminho).getroot()
    tipos, enums = {}, {}
    for st in root.iter(XS + "simpleType"):
        nome = st.get("name")
        vals = [e.get("value") for e in st.iter(XS + "enumeration")]
        if nome and vals: enums[nome] = vals
    for ct in root.iter(XS + "complexType"):
        nome = ct.get("name")
        if not nome: continue
        base_t, elems = None, []
        ext = ct.find(f".//{XS}extension")
        if ext is not None: base_t = ext.get("base", "").split(":")[-1]
        for el in ct.iter(XS + "element"):
            elems.append({"nome": el.get("name"), "tipo": (el.get("type") or "").split(":")[-1], "minOccurs": el.get("minOccurs", "1"), "maxOccurs": el.get("maxOccurs", "1")})
        tipos[nome] = {"estende": base_t, "elementos": elems}
    def cadeia(n):
        vistos, c = [], tipos.get(n, {}).get("estende")
        while c and c not in vistos:
            vistos.append(c); c = tipos.get(c, {}).get("estende")
        return vistos, bool(c)
    saida = []
    for n in sorted(tipos):
        anc, ciclo = cadeia(n)
        herdados = [dict(e, herdado_de=a) for a in anc for e in tipos.get(a, {}).get("elementos", [])]
        saida.append({"nome": n, "categoria": "metadata_type_candidato" if "Metadata" in anc else "estrutura_auxiliar",
                      "cadeia_heranca": anc, "ciclo_heranca": ciclo, "elementos_proprios": tipos[n]["elementos"], "elementos_herdados": herdados})
    res = {"id": "wsdl-schema", "fonte": os.path.basename(caminho), "nota": "minOccurs do WSDL não é toda a regra funcional de obrigatoriedade.",
           "tipos": saida, "enumeracoes": [{"nome": k, "valores": v} for k, v in sorted(enums.items())]}
    gravar(destino or os.path.join(BASE, "inventarios", "wsdl-schema.json"), res)
    return res


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    c = argv[1]
    if c == "inventario": cmd_inventario()
    elif c == "gerar": gerar(); print("gerado/ atualizado")
    elif c == "cobertura": cmd_cobertura()
    elif c == "auditar-rascunhos": cmd_auditar()
    elif c == "importar-wsdl": importar_wsdl(argv[2]); print("inventarios/wsdl-schema.json")
    elif c in ("validar", "tudo"):
        if c == "tudo":
            cmd_inventario(); cmd_auditar(); gerar(); cmd_cobertura()
        R = validar()
        for a in R.avisos: print("AVISO:", a)
        for e in R.erros: print("ERRO:", e)
        print(f"validação: {len(R.erros)} erro(s), {len(R.avisos)} aviso(s)")
        return 1 if R.erros else 0
    else:
        print(__doc__); return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
