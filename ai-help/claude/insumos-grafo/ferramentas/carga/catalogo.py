"""Operações de catálogo usadas nos lotes 5a–5k: fontes, referências, relacionamentos e funcionalidades.

Todas leem e gravam JSON do catálogo; nenhuma inventa conteúdo. Quem chama fornece os fatos e as fontes.
"""
import json
from .base import ev, af, ld, sv, caminho

CHECAGEM = lambda data: {"estado": "verificado", "nota": f"Conteúdo lido em {data} e conferido quanto ao assunto (não apenas HTTP 200)."}


# ------------------------------------------------------------------ fontes
def fonte(id, titulo, url, pertinencia, extracao, data, tipo="oficial_documentacao", versao="68.0", metodo="extracao_documental_assistida"):
    """Monta um registro de fonte. extracao: caminho relativo da nota em fontes/extracoes/."""
    return {"id": id, "titulo": titulo, "url": url, "tipo": tipo, "versao": versao, "data_verificacao": data, "metodo": metodo,
            "pertinencia": pertinencia, "extracao": extracao, "checagem_online": CHECAGEM(data)}


def registrar_fontes(novas):
    """Acrescenta fontes a fontes/registro.json sem duplicar ids. Devolve os ids acrescentados."""
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {f["id"] for f in reg["fontes"]}
    add = [n for n in novas if n["id"] not in ids]
    reg["fontes"] += add
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
    return [n["id"] for n in add]


def fonte_mdapi(nome, extracao, data, base="https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"):
    """Fonte padrão da página de um tipo na Metadata API (src:mdapi-<nome em minúsculas>)."""
    return fonte(f"src:mdapi-{nome.lower()}", f"{nome} (Metadata API)", base + f"meta_{nome.lower()}.htm",
                 f"Arquivo, versão e propriedades do tipo {nome}.", extracao, data)


def fonte_objref(nome, extracao, data, base="https://developer.salesforce.com/docs/atlas.en-us.264.0.object_reference.meta/object_reference/sforce_api_objects_"):
    """Fonte padrão da página de um objeto na Object Reference (src:objref-<nome em minúsculas>)."""
    return fonte(f"src:objref-{nome.lower()}", f"{nome} (Object Reference)", base + nome.lower() + ".htm",
                 f"Chamadas, acesso e campos de {nome}.", extracao, data)


# ------------------------------------------------------------------ relacionamentos
NOTA_NOME = " A referência é pelo nome do componente, no XML (não é um lookup entre registros)."


def marcar_referencia(pasta, arquivo, propriedade, alvo, nota="Referência pelo nome do componente no XML."):
    """Grava propriedade.referencia = {alvos: [alvo]} numa propriedade de metadata type ou estrutura.
    pasta: 'metadata-types' ou 'estruturas'. alvo: id mdt:/mdx:. Falha se a propriedade não existir."""
    d = ld(f"{pasta}/{arquivo}.json")
    alvo_ok = False
    for p in d["propriedades"]:
        if p["nome"] == propriedade:
            p["referencia"] = {"alvos": [alvo], "nota": nota}
            alvo_ok = True
    if not alvo_ok:
        raise KeyError(f"{arquivo}.{propriedade} não existe")
    sv(f"{pasta}/{arquivo}.json", d)


def rel_referencia(rid, origem, campo, destino, explicacao, src, sufixo=NOTA_NOME, cardinalidade=None):
    """Relacionamento referencia_campo. Para referência por nome em XML, chame antes marcar_referencia()."""
    r = {"id": "rel:" + rid, "tipo": "referencia_campo", "origem": {"entidade": origem, "campo": campo}, "destino": {"entidade": destino},
         "explicacao": explicacao + (sufixo or ""), "estado": "verificado", "evidencias": [ev(src)]}
    if cardinalidade:
        r["cardinalidade_registros"] = cardinalidade
    sv(f"relacionamentos/{rid}.json", r)


LOOKUP_N1 = {"estado": "desconhecido", "valor": "N:1", "nota": "Lookup indica N:1; obrigatoriedade não declarada na página."}


def rel_lookup(rid, origem, campo, destino, explicacao, src):
    """Lookup entre objetos API (registro → registro)."""
    rel_referencia(rid, origem, campo, destino, explicacao, src, sufixo="", cardinalidade=LOOKUP_N1)


def rel_representacao_comum(rid, mdt, obj, explicacao, srcs):
    """Mesmo componente visto como metadata type e como objeto API, SEM prova campo a campo.
    Use correspondencia_xml_api 'direta'/'transformada' só com prova de campo (ex.: campo Metadata tipado) — há teste para isso."""
    sv(f"relacionamentos/{rid}.json", {"id": "rel:" + rid, "tipo": "representacao_comum", "origem": {"entidade": mdt}, "destino": {"entidade": obj},
       "explicacao": explicacao + " A correspondência campo a campo não foi comprovada.", "estado": "verificado", "evidencias": [ev(s) for s in srcs]})


# ------------------------------------------------------------------ funcionalidades
def ligar_subclassificacoes(fid, subs):
    """Inclui func:<fid> na lista 'funcionalidades' de cada subclassificação (slugs sem prefixo)."""
    for s in subs:
        d = ld(f"subclassificacoes/{s}.json")
        d["funcionalidades"] = sorted(set(d["funcionalidades"]) | {"func:" + fid})
        sv(f"subclassificacoes/{s}.json", d)


def funcionalidade(fid, nome, nome_tecnico, aliases, o_que_e, finalidade, exemplo, principal, secundarias, mdts, objs, srcs, ausencias, setup,
                   codigo=(), interface=(), recs=(), alertas=(), limitacoes=(), pre=()):
    """Cria funcionalidades/<fid>.json e liga às subclassificações.
    principal = (classificacao, subclassificacao) sem prefixos; secundarias = [(cls, sub, motivo)];
    mdts/objs = [(Nome, papel)]; recs = [(texto, natureza, src)] com natureza orientacao_oficial|inferencia_tecnica|preferencia_projeto."""
    rep = {"metadata_types": [{"ref": "mdt:" + r, "papel": p} for r, p in mdts], "objetos_api": [{"ref": "obj:" + r, "papel": p} for r, p in objs], "ausencias": list(ausencias)}
    if codigo:
        rep["codigo"] = list(codigo)
    if interface:
        rep["interface"] = list(interface)
    cp, sp = principal
    f = {"id": "func:" + fid, "nome": nome, "nome_tecnico": nome_tecnico, "aliases": list(aliases),
         "termos_busca": sorted(set([nome.lower(), nome_tecnico.lower()] + [a.lower() for a in aliases])), "o_que_e": o_que_e, "finalidade": finalidade, "exemplo": exemplo,
         "classificacao_principal": {"classificacao": "cls:" + cp, "subclassificacao": "sub:" + sp},
         "classificacoes_secundarias": [{"classificacao": "cls:" + c, "subclassificacao": "sub:" + s, "motivo": m} for c, s, m in secundarias],
         "representacoes": rep, "setup": setup, "recomendacoes": [{"texto": t, "natureza": n, "evidencias": [ev(s)]} for t, n, s in recs],
         "alertas": list(alertas), "limitacoes": list(limitacoes), "estado": "verificado", "evidencias": [ev(s) for s in srcs]}
    if pre:
        f["pre_requisitos"] = list(pre)
    sv(f"funcionalidades/{fid}.json", f)
    ligar_subclassificacoes(fid, [sp] + [s for _, s, _ in secundarias])
    return f


def ampliar_funcionalidade(fid, mdts=(), objs=(), srcs=(), alertas=(), remover_ausencia_de=None):
    """Acrescenta representações, evidências e alertas a uma funcionalidade existente, sem duplicar.
    remover_ausencia_de='objeto_api' (ou 'metadata_type') tira a ausência registrada desse tipo."""
    f = ld(f"funcionalidades/{fid}.json")
    r = f["representacoes"]
    for chave, pref, itens in (("metadata_types", "mdt:", mdts), ("objetos_api", "obj:", objs)):
        have = {x["ref"] for x in r[chave]}
        r[chave] += [{"ref": pref + n, "papel": p} for n, p in itens if pref + n not in have]
    if remover_ausencia_de:
        r["ausencias"] = [a for a in r["ausencias"] if a.get("tipo") != remover_ausencia_de]
    f["evidencias"] += [ev(s) for s in srcs if not any(e["fonte"] == s for e in f["evidencias"])]
    f["alertas"] += [a for a in alertas if a not in f["alertas"]]
    sv(f"funcionalidades/{fid}.json", f)


def secundaria(fid, classificacao, subclassificacao, motivo, srcs=()):
    """Acrescenta uma classificação secundária (com motivo) e liga à subclassificação."""
    f = ld(f"funcionalidades/{fid}.json")
    if not any(c["subclassificacao"] == "sub:" + subclassificacao for c in f["classificacoes_secundarias"]):
        f["classificacoes_secundarias"].append({"classificacao": "cls:" + classificacao, "subclassificacao": "sub:" + subclassificacao, "motivo": motivo})
    f["evidencias"] += [ev(s) for s in srcs if not any(e["fonte"] == s for e in f["evidencias"])]
    sv(f"funcionalidades/{fid}.json", f)
    ligar_subclassificacoes(fid, [subclassificacao])


UI_EN = "Rótulos em inglês, como na fonte; a tradução da interface em pt-BR não foi verificada."


def definir_setup(fid, valor, nota, srcs, estado="verificado"):
    """Caminho de Setup de uma funcionalidade, com fonte. Sem fonte, use estado 'desconhecido' e valor None."""
    f = ld(f"funcionalidades/{fid}.json")
    f["setup"] = af(estado, valor, (nota + " " + UI_EN).strip() if valor else nota, [ev(s) for s in srcs])
    f["evidencias"] += [ev(s) for s in srcs if not any(e["fonte"] == s for e in f["evidencias"])]
    sv(f"funcionalidades/{fid}.json", f)


def ligar_nuvem(nuvem, classificacao, subclassificacao, fids):
    """Inclui funcionalidades (só as de classificação principal, como nas demais) em nuvens/<nuvem>.json."""
    n = ld(f"nuvens/{nuvem}.json")
    c = next((x for x in n["classificacoes_aplicaveis"] if x["classificacao"] == "cls:" + classificacao), None)
    if c is None:
        c = {"classificacao": "cls:" + classificacao, "subclassificacoes": []}
        n["classificacoes_aplicaveis"].append(c)
    s = next((x for x in c["subclassificacoes"] if x["subclassificacao"] == "sub:" + subclassificacao), None)
    if s is None:
        s = {"subclassificacao": "sub:" + subclassificacao, "funcionalidades": []}
        c["subclassificacoes"].append(s)
        c["subclassificacoes"].sort(key=lambda x: x["subclassificacao"])
    s["funcionalidades"] = sorted(set(s["funcionalidades"]) | {"func:" + f for f in fids})
    sv(f"nuvens/{nuvem}.json", n)
