# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
import b1_base, b2_mdt, b3_obj
b2_mdt.build()
b3_obj.build_objects(); b3_obj.build_rels(); b3_obj.build_funcs()
b1_base.write_taxonomy()   # after funcs so SUB_FUNCS filled
b3_obj.build_clouds(); b3_obj.build_root()
# pós-processamento: completude estrutural transitiva (tipo só é completo se suas estruturas também forem)
import json, glob, os
R = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/catalogo/"
est = {json.load(open(p))["id"]: json.load(open(p)) for p in glob.glob(R + "estruturas/*.json")}
for p in glob.glob(R + "metadata-types/*.json"):
    m = json.load(open(p))
    c = m["cobertura"]["estrutural"]
    parciais = [s for s in m["estruturas"] if est[s]["cobertura"]["estrutural"]["estado"] != "completa"]
    if c["estado"] == "completa" and parciais:
        c["estado"] = "parcial"
        c["nota"] += f" Estruturas usadas ainda parciais: {', '.join(parciais)}."
        with open(p, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, indent=2); f.write("\n")
