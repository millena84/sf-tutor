"""Ajustes em tipos e estruturas já gravados: ligar propriedades a estruturas, completar enumerações e recalcular a cobertura estrutural.

Usado pelos lotes que completam cadastros históricos (o catálogo em JSON é a fonte da verdade). Cada função grava o arquivo alterado.
"""
import json, os, re

from carga.base import ev, ld, sv, caminho

MARCAS = (" Primeiro nível completo;", " Estruturas usadas ainda parciais:", " Enumerações sem lista de valores:")


def _registrados():
    return {f[:-5] for f in os.listdir(caminho("catalogo", "metadata-types"))}


def estado_estrutura(sid, visto=None):
    """True se a estrutura existe, está completa e todas as estruturas que ela usa também estão (recursivo)."""
    visto = visto if visto is not None else set()
    if sid in visto:
        return True
    visto.add(sid)
    p = caminho("catalogo", "estruturas", sid[4:] + ".json")
    if not os.path.exists(p):
        return False
    d = json.load(open(p, encoding="utf-8"))
    if d["cobertura"]["estrutural"]["estado"] != "completa":
        return False
    return all(estado_estrutura(q["estrutura_ref"], visto) for q in d["propriedades"] if q.get("estrutura_ref"))


def _pendentes(props):
    reg = _registrados()
    return sorted(q["nome"] for q in props if q["dominio"]["natureza"] == "tipo_composto" and "estrutura_ref" not in q
                  and q["tipo_tecnico"].replace("[]", "") not in reg)


def _dono(pasta, nome):
    return ("mdt:" if pasta == "metadata-types" else "mdx:") + nome


def ligar(pasta, nome, ligacoes=None, nota=None, src=None, esperado=None):
    """Liga propriedades a estruturas ({prop: NomeDaEstrutura}) e recalcula a cobertura estrutural.
    nota: substitui a nota-base (o texto antes das marcas automáticas). esperado: fixa o universo esperado (int)."""
    rel = f"{pasta}/{nome}.json"
    d = ld(rel)
    dono = _dono(pasta, nome)
    for q in d["propriedades"]:
        if ligacoes and q["nome"] in ligacoes:
            sid = "mdx:" + ligacoes[q["nome"]]
            q["estrutura_ref"] = sid
            if src and not any(e.get("fonte") == src for e in q["evidencias"]):
                q["evidencias"].append(ev(src))
            e = ld(f"estruturas/{sid[4:]}.json")
            e["usada_por"] = sorted(set(e["usada_por"]) | {dono})
            sv(f"estruturas/{sid[4:]}.json", e)
    usadas = sorted({q["estrutura_ref"] for q in d["propriedades"] if q.get("estrutura_ref")})
    if pasta == "metadata-types":
        d["estruturas"] = usadas
    est = d["cobertura"]["estrutural"]
    if esperado is not None:
        est["esperado"] = esperado
    est["presente"] = len(d["propriedades"])
    pend = _pendentes(d["propriedades"])
    parciais = [s for s in usadas if not estado_estrutura(s)]
    base = nota if nota is not None else est.get("nota") or ""
    for m in MARCAS:
        base = base.split(m)[0]
    if pend:
        base += f" Primeiro nível completo; {len(pend)} propriedade(s) de tipo composto ainda sem estrutura detalhada: {', '.join(pend)}."
    if parciais:
        base += f" Estruturas usadas ainda parciais: {', '.join(parciais)}."
    completa = est.get("esperado") is not None and est["esperado"] == est["presente"] and not pend and not parciais
    est.update({"estado": "completa" if completa else "parcial", "nota": base.strip()})
    sv(rel, d)
    return est["estado"]


def definir_valores(pasta, nome, prop, valores, src, nota=None):
    """Completa o domínio de uma propriedade com a lista fechada de valores lida na fonte."""
    rel = f"{pasta}/{nome}.json"
    d = ld(rel)
    for q in d["propriedades"]:
        if q["nome"] == prop:
            q["dominio"] = {"natureza": "enum_fechado", "valores": [{"valor": v} for v in valores], "lista_completa": "sim",
                            "estado": "verificado", "evidencias": [ev(src)]}
            if nota:
                q["dominio"]["contexto"] = nota
            if not any(e.get("fonte") == src for e in q["evidencias"]):
                q["evidencias"].append(ev(src))
            break
    else:
        raise SystemExit(f"{rel}: propriedade {prop} não encontrada")
    sv(rel, d)


def acrescentar_propriedades(pasta, nome, linhas, src):
    """Acrescenta propriedades montadas por mdt.prop (por exemplo, campos herdados que a página não repete). Não duplica nomes."""
    from carga import mdt as M
    rel = f"{pasta}/{nome}.json"
    d = ld(rel)
    nomes = {q["nome"] for q in d["propriedades"]}
    for r in linhas:
        if r[0] in nomes:
            continue
        d["propriedades"].append(M.prop(_dono(pasta, nome), *r[:5], src, **(r[5] if len(r) > 5 else {})))
    d["propriedades"].sort(key=lambda q: q["nome"].lower())
    sv(rel, d)


def nota_base(texto):
    """Remove as marcas automáticas de uma nota de cobertura."""
    for m in MARCAS:
        texto = texto.split(m)[0]
    return re.sub(r"\s+", " ", texto).strip()
