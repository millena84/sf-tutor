# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5k (issue #24): versão de API ↔ componentes (só Flow declara apiVersion no catálogo).
import json
from b1_base import ev
CAT = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/catalogo/"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
NOTA = "As versões de API têm ciclo de vida (suporte, descontinuação e aposentadoria): ver a funcionalidade Versões de API e ciclo de vida."
d = ld("metadata-types/Flow.json")
for p in d["propriedades"]:
    if p["nome"] == "apiVersion":
        p["notas"] = [n for n in p.get("notas", []) if n != NOTA] + [NOTA]
        if not any(e["fonte"] == "src:rest-api-eol" for e in p["evidencias"]): p["evidencias"].append(ev("src:rest-api-eol"))
sv("metadata-types/Flow.json", d)
f = ld("funcionalidades/versoes-de-api.json")
L = "No catálogo atual, a única propriedade apiVersion cadastrada é mdt:Flow.apiVersion; o schema não tem relação entre funcionalidade e propriedade, por isso a ligação fica só no texto."
f["limitacoes"] = [x for x in f["limitacoes"] if x != L] + [L]
sv("funcionalidades/versoes-de-api.json", f)
print("ok lote 5k")
