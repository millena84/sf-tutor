"""Lote 7t (rodada D1, fechamento do MVP): troca o texto genérico das estruturas de Profile e PermissionSet.

A auditoria de conteúdo (ferramentas/auditoria_conteudo.py) achou 32 estruturas com o mesmo o_que_e genérico.
O texto novo é montado só com o que já está no catálogo, com fonte: a propriedade do metadata type que
usa a estrutura (nome e descrição) e os nomes das propriedades da própria estrutura. Nenhum fato novo.

Ordem: lote7s_b5_issue39.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
"""
import glob, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv                # noqa: E402

GENERICO = "estrutura composta usada como tipo de uma propriedade"
n = 0
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "..", "..", "catalogo", "estruturas", "*.json"))):
    nome = os.path.basename(f)[:-5]
    e = ld(f"estruturas/{nome}.json")
    if not e["o_que_e"].lower().startswith(GENERICO):
        continue
    usos = []
    for u in e["usada_por"]:
        tipo = u.split(":", 1)[1]
        m = ld(f"metadata-types/{tipo}.json")
        usos += [(tipo, p["nome"], p["o_que_e"].rstrip(".")) for p in m["propriedades"] if p.get("estrutura_ref") == e["id"]]
    if not usos:
        continue
    # Prefere a propriedade atual quando há uma antiga (com "até a" na descrição) e uma nova.
    usos.sort(key=lambda x: "até a" in x[2])
    tipo, prop, desc = usos[0]
    props = ", ".join(f"`{p['nome']}`" for p in e["propriedades"])
    texto = f"Cada item da lista `{prop}` de {tipo}: {desc[0].lower() + desc[1:]}. Propriedades do item: {props}."
    if len(usos) > 1:
        texto += " Também é o tipo de " + ", ".join(f"`{p}`" for _, p, _ in usos[1:]) + "."
    e["o_que_e"] = texto
    sv(f"estruturas/{nome}.json", e)
    n += 1
print("lote 7t:", n, "estruturas com descrição específica")
