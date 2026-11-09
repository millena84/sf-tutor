"""Gera esqueletos XML comentados para metadata types sem exemplo (issue #20).

O esqueleto usa SÓ propriedades catalogadas e mostra:
- elementos obrigatórios, com valor ilustrativo e comentário (valores documentados, padrão, condição);
- elementos condicionais como comentário (não ativos), para não criar combinações inválidas;
- se o tipo não tem obrigatórios, até 3 propriedades simples, como amostra.

Valores: listas documentadas usam o primeiro valor; booleanos e números usam o padrão declarado quando existe;
textos ficam entre colchetes, descrevendo o que preencher (nunca um valor inventado como se fosse real).

Uso, a partir de ai-help/claude/insumos-grafo/:
    python3 ferramentas/exemplos_xml.py            # só os tipos sem exemplo
    python3 ferramentas/exemplos_xml.py --mostrar AccountSettings
Depois rode `python3 ferramentas/sftutor.py tudo`.
"""
import glob, json, os, sys
from xml.sax.saxutils import escape

BASE = os.environ.get("SFTUTOR_BASE") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = os.path.join(BASE, "catalogo")
NS = "http://soap.sforce.com/2006/04/metadata"
NOTA = ("Esqueleto gerado por ferramentas/exemplos_xml.py a partir das propriedades catalogadas: mostra os elementos obrigatórios "
        "(e os condicionais, comentados); textos entre colchetes indicam o que preencher. Não é um arquivo pronto para implantação.")
SIMPLES = {"string", "boolean", "int", "double", "number", "long", "date", "dateTime", "picklist"}
MAX_DESC = 90


def _ler(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _interna(p):
    t = " ".join(p.get("notas") or []).lower() + " " + (p.get("o_que_e") or "").lower()
    return "uso interno" in t or "reservado" in t or "internal" in t


def _excluir(p):
    return (p["nome"] == "fullName" or p.get("herdada") or (p.get("disponibilidade") or {}).get("ate_versao")
            or _interna(p) or p["tipo_tecnico"].startswith("(") or p["tipo_tecnico"] in ("base64Binary",))


def _curto(txt):
    txt = (txt or "").strip().rstrip(".")
    return txt if len(txt) <= MAX_DESC else txt[:MAX_DESC - 1].rstrip() + "…"


def _valores(p):
    return [v["valor"] for v in (p.get("dominio") or {}).get("valores") or []]


def _padrao(p):
    d = p.get("default") or {}
    return d.get("valor") if d.get("forma") == "valor" else None


def _valor(p):
    vals = _valores(p)
    t = p["tipo_tecnico"].replace("[]", "")
    pad = _padrao(p)
    if t == "boolean":
        return pad if pad in ("true", "false") else "false"
    if vals:
        return pad if pad in vals else vals[0]
    if t in ("int", "double", "number", "long"):
        try:
            float(pad)
            return pad
        except (TypeError, ValueError):
            return "0"
    if p.get("o_que_e"):
        return f"[{_curto(p['o_que_e'])}]"
    alvos = (p.get("referencia") or {}).get("alvos")
    if alvos:
        return f"[nome do componente {alvos[0].split(':', 1)[1]}]"
    return f"[{p['nome']}]"


def _comentario(p, cond=None):
    partes = []
    ob = p["obrigatoriedade"].get("valor")
    if cond:
        partes.append(f"Condicional ({cond})")
    elif ob == "sim":
        partes.append("Obrigatório")
    else:
        verif = p["obrigatoriedade"].get("estado") == "verificado"
        partes.append("Opcional" if ob == "nao" and verif else "Não marcado como obrigatório na fonte" if ob == "nao" else "Obrigatoriedade não declarada")
    t = p["tipo_tecnico"].replace("[]", "")
    vals = _valores(p)
    if vals and t != "boolean":
        partes.append("Valores: " + ", ".join(vals[:8]) + ("…" if len(vals) > 8 else ""))
    pad = _padrao(p)
    if pad is not None:
        partes.append(f"Padrão: {pad}")
    elif t in ("boolean", "int", "double", "number", "long") and not (vals and t != "boolean"):
        partes.append("Padrão não declarado na fonte")
    return ". ".join(partes)


def _elemento(p, estruturas, ind, prof=0):
    """Linhas XML de uma propriedade (estrutura vira elemento aninhado com seus obrigatórios)."""
    nome = p["nome"]
    sref = p.get("estrutura_ref")
    if sref and sref in estruturas and prof < 2:
        filhos = _selecionar(estruturas[sref]["propriedades"], amostra=1)
        linhas = [f"{ind}<{nome}>"]
        for f in filhos:
            linhas += _bloco(f, estruturas, ind + "    ", prof + 1)
        linhas.append(f"{ind}</{nome}>")
        return linhas
    if p["tipo_tecnico"].replace("[]", "") not in SIMPLES:
        return []
    return [f"{ind}<{nome}>{escape(_valor(p))}</{nome}>"]


def _bloco(p, estruturas, ind, prof=0, cond=None):
    linhas = _elemento(p, estruturas, ind, prof)
    if not linhas:
        return []
    com = _comentario(p, cond).replace("--", "–")
    if cond:  # condicional: o elemento inteiro fica comentado (sem comentários internos, que não podem ser aninhados)
        dentro = [l for l in linhas if not l.strip().startswith("<!--")]
        return [f"{ind}<!-- {escape(com)}:"] + [f"{ind}    {l.strip()}" for l in dentro] + [f"{ind}-->"]
    return ([f"{ind}<!-- {escape(com)} -->"] if com else []) + linhas


def _selecionar(props, amostra=3):
    ok = [p for p in props if not _excluir(p)]
    req = [p for p in ok if p["obrigatoriedade"].get("valor") == "sim"]
    if req:
        return req
    simples = [p for p in ok if p["tipo_tecnico"].replace("[]", "") in SIMPLES]
    return simples[:amostra]


def gerar(m, estruturas):
    """Devolve o XML do esqueleto, ou None se não houver propriedade utilizável."""
    props = m["propriedades"]
    corpo = []
    for p in _selecionar(props):
        corpo += _bloco(p, estruturas, "    ")
    if any(p["obrigatoriedade"].get("valor") == "sim" for p in props if not _excluir(p)):
        for p in props:
            if _excluir(p) or p["obrigatoriedade"].get("valor") != "condicional":
                continue
            corpo += _bloco(p, estruturas, "    ", cond=_curto(p["obrigatoriedade"].get("condicao")) or "ver a ficha")
    if not any(l.strip().startswith("<") and not l.strip().startswith("<!--") for l in corpo):
        return None
    return "\n".join(['<?xml version="1.0" encoding="UTF-8"?>', f'<{m["nome"]} xmlns="{NS}">', *corpo, f"</{m['nome']}>"])


def main(argv):
    estruturas = {e["id"]: e for e in (_ler(p) for p in glob.glob(os.path.join(CAT, "estruturas", "*.json")))}
    if len(argv) > 1 and argv[0] == "--mostrar":
        print(gerar(_ler(os.path.join(CAT, "metadata-types", argv[1] + ".json")), estruturas))
        return 0
    feitos, sem = [], []
    for p in sorted(glob.glob(os.path.join(CAT, "metadata-types", "*.json"))):
        m = _ler(p)
        if "exemplo_xml" in m:
            continue
        xml = gerar(m, estruturas)
        if xml is None:
            sem.append(m["nome"])
            continue
        m["exemplo_xml"] = {"xml": xml, "natureza": "didatico_projeto", "nota": NOTA}
        with open(p, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
            f.write("\n")
        feitos.append(m["nome"])
    print(f"esqueletos gerados: {len(feitos)}; sem propriedade utilizável: {len(sem)} {sem}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
