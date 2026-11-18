"""Fase 2 (v2): lista, por classificação, os nós com propriedades ou campos de explicação pendente.

Cada nó técnico (objeto API, metadata type ou estrutura) com itens pendentes é atribuído às classificações das
funcionalidades que o representam (estruturas herdam do metadata type que as usa). Um nó representado por
funcionalidades de temas diferentes aparece em cada um deles, mas o total geral conta cada nó uma vez só.

Não altera o catálogo: grava relatorios/fase2-pendencias-por-classificacao.md.
Uso: python3 ferramentas/pendencias_explicacao.py
"""
import collections
import glob
import json
import os

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CAT = os.path.join(RAIZ, "catalogo")
SAIDA = os.path.join(RAIZ, "relatorios", "fase2-pendencias-por-classificacao.md")
PENDENTE = "Explicação pendente"


def ld(p):
    with open(p, encoding="utf-8") as h:
        return json.load(h)


def main():
    funcs = [ld(f) for f in glob.glob(os.path.join(CAT, "funcionalidades", "*.json"))]
    cls = {d["id"]: d for d in (ld(f) for f in glob.glob(os.path.join(CAT, "classificacoes", "*.json")))}
    subs = {d["id"]: d for d in (ld(f) for f in glob.glob(os.path.join(CAT, "subclassificacoes", "*.json")))}
    # nó técnico -> {(classificação, subclassificação, funcionalidade)}
    onde = collections.defaultdict(set)
    for f in funcs:
        cp = f["classificacao_principal"]
        rep = f.get("representacoes", {})
        for r in rep.get("metadata_types", []) + rep.get("objetos_api", []):
            onde[r["ref"]].add((cp["classificacao"], cp["subclassificacao"], f["id"]))
    pend = {}  # id -> (tipo, pendentes, total)
    for pasta, chave, tipo in (("objetos-api", "campos", "objeto API"), ("metadata-types", "propriedades", "metadata type"),
                               ("estruturas", "propriedades", "estrutura")):
        for f in glob.glob(os.path.join(CAT, pasta, "*.json")):
            d = ld(f)
            itens = d.get(chave, [])
            k = sum(1 for i in itens if (i.get("o_que_e") or "").startswith(PENDENTE) or not (i.get("o_que_e") or "").strip())
            if k:
                pend[d["id"]] = (tipo, k, len(itens), d.get("usada_por", []))
    # estruturas herdam do metadata type que as usa
    for nid, (tipo, _, _, usada) in pend.items():
        if tipo == "estrutura":
            for u in usada:
                onde[nid] |= onde.get(u, set())
    por_cls = collections.defaultdict(lambda: collections.defaultdict(dict))
    sem = []
    for nid, (tipo, k, tot, _) in pend.items():
        if not onde.get(nid):
            sem.append((nid, tipo, k, tot))
            continue
        for c, s, f in onde[nid]:
            por_cls[c][s].setdefault(nid, (tipo, k, tot, set()))[3].add(f)
    total_itens = sum(v[1] for v in pend.values())
    L = ["# Fase 2: explicações pendentes por classificação", "",
         "Gerado por `ferramentas/pendencias_explicacao.py`. Não edite à mão.", "",
         f"**Total:** {total_itens} itens pendentes em {len(pend)} nós (cada nó contado uma vez).",
         "Um nó usado por funcionalidades de temas diferentes aparece em cada tema; por isso a soma das tabelas pode passar do total.", "",
         "Sugestão de uso: escolher uma classificação por sessão, começando pelas de mais itens ou pelas que o público mais visita, "
         "e fechar os nós dela num PR.", "", "## Resumo por classificação", "",
         "| Classificação | Nós | Itens pendentes |", "|---|---|---|"]
    linhas = []
    for c, ss in por_cls.items():
        nos = {n: v for s in ss.values() for n, v in s.items()}
        linhas.append((sum(v[1] for v in nos.values()), c, len(nos)))
    for k, c, n in sorted(linhas, reverse=True):
        L.append(f"| {cls.get(c, {}).get('nome', c)} | {n} | {k} |")
    for k, c, n in sorted(linhas, reverse=True):
        L += ["", f"## {cls.get(c, {}).get('nome', c)} ({k} itens)", ""]
        for s, nos in sorted(por_cls[c].items(), key=lambda x: -sum(v[1] for v in x[1].values())):
            L.append(f"### {subs.get(s, {}).get('nome', s)}")
            L.append("")
            for nid, (tipo, kk, tot, fs) in sorted(nos.items(), key=lambda x: -x[1][1]):
                L.append(f"- [ ] `{nid}` ({tipo}): {kk} de {tot} pendentes. Funcionalidades: {', '.join(sorted(x.split(':', 1)[1] for x in fs))}")
            L.append("")
    if sem:
        L += ["## Sem funcionalidade associada", ""] + [f"- [ ] `{n}` ({t}): {k} de {tot}" for n, t, k, tot in sorted(sem)]
    with open(SAIDA, "w", encoding="utf-8") as h:
        h.write("\n".join(L).rstrip() + "\n")
    print(f"fase 2: {total_itens} itens em {len(pend)} nós; {len(por_cls)} classificações -> {os.path.relpath(SAIDA, RAIZ)}")


if __name__ == "__main__":
    main()
