"""Lote 8g (Fase 2, Processos de negócio, Atendimento parte 1): AgentWork e PendingServiceRouting.

Lê a tabela da nota de extração (nome | tipo | versão | descrição) e grava tipo, explicação e versão. Os itens sem descrição oficial
ficam com explicacao = "nao_encontrada". Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv               # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-20"
EXTR = "fontes/extracoes/lote8g-fase2-atendimento-1.txt"
G = "https://developer.salesforce.com/docs/get_document_content/object_reference/"
C.registrar_fontes([
    C.fonte("src:objref-agentwork-264", "AgentWork (Object Reference 264.0)", G + "sforce_api_objects_agentwork.htm/en-us/264.0", "Campos de AgentWork.", EXTR, DATA),
    C.fonte("src:objref-pendingservicerouting-264", "PendingServiceRouting (Object Reference 264.0)", G + "sforce_api_objects_pendingservicerouting.htm/en-us/264.0",
            "Campos de PendingServiceRouting.", EXTR, DATA),
])

texto = open(EXTR, encoding="utf-8").read()
def tabela(secao):
    bloco = texto.split(f"[{secao}]", 1)[1].split("\n[", 1)[0]
    return {m.group(1): (m.group(2), m.group(3), m.group(4).strip())
            for m in re.finditer(r"^  (\w+) \| (\w+) \| ([\d.]+|-) \| (.+)$", bloco, re.M)}

def frase(s):
    s = s[0].upper() + s[1:]
    return s if s.endswith(".") else s + "."

cont = 0
for arq, src in [("objetos-api/AgentWork.json", "src:objref-agentwork-264"), ("objetos-api/PendingServiceRouting.json", "src:objref-pendingservicerouting-264")]:
    T = tabela(src)
    d = ld(arq)
    for i in d["campos"]:
        if i["nome"] not in T or i.get("explicacao") != "pendente":
            continue
        tipo, v, txt = T[i["nome"]]
        if i.get("tipo_tecnico") in (None, "(a extrair)"):
            i["tipo_tecnico"] = tipo
        i["o_que_e"], i["explicacao"] = frase(txt), "explicada"
        if src not in [e["fonte"] for e in i["evidencias"]]:
            i["evidencias"].append({"fonte": src})
        if v != "-" and i.get("disponibilidade", {}).get("estado") == "desconhecido":
            i["disponibilidade"] = {"desde_versao": v, "ate_versao": None, "estado": "verificado"}
        cont += 1
    d["cobertura"]["explicativa"]["presente"] = sum(1 for x in d["campos"] if x.get("explicacao") == "explicada")
    sv(arq, d)
print(f"lote 8g: {cont} campos explicados")
