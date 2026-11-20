"""Lote 8h (Fase 2, Processos de negócio, Atendimento parte 2): ServiceContract, Entitlement e Case.CurrencyIsoCode.

Lê a tabela da nota de extração (nome | tipo | versão | descrição) e grava tipo, explicação e versão. Case.CurrencyIsoCode fica com
explicacao = "nao_encontrada" e o texto padrão (versão e release de config/versoes.json). Reexecutável.
Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv               # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-20"
EXTR = "fontes/extracoes/lote8h-fase2-atendimento-2.txt"
G = "https://developer.salesforce.com/docs/get_document_content/"
C.registrar_fontes([
    C.fonte("src:objref-servicecontract-264", "ServiceContract (Object Reference 264.0)",
            G + "object_reference/sforce_api_objects_servicecontract.htm/en-us/264.0", "Campos de ServiceContract.", EXTR, DATA),
    C.fonte("src:objref-entitlement-264", "Entitlement (Object Reference 264.0)",
            G + "object_reference/sforce_api_objects_entitlement.htm/en-us/264.0", "Campos de Entitlement.", EXTR, DATA),
    C.fonte("src:fieldref-case-264", "Case (Field Reference 264.0)", G + "sfFieldRef/salesforce_field_reference_Case.htm/en-us/264.0",
            "Tipo, rótulo e tamanho de CurrencyIsoCode; a Field Reference não traz descrições.", EXTR, DATA),
])
V = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "config", "versoes.json"),
                   encoding="utf-8"))["plataforma_core"]
NAO = (f"Não encontrada descrição oficial na última versão da documentação ({V['numero_interno_documentacao']}, API {V['api_version']}); "
       f"verificado também nas notas da release {V['release']} (por busca).")

texto = open(EXTR, encoding="utf-8").read()


def tabela(secao):
    bloco = texto.split(f"[{secao}]", 1)[1].split("\n[", 1)[0].split("Sem descrição oficial", 1)[0]
    return {m.group(1): (m.group(2), m.group(3), m.group(4).strip())
            for m in re.finditer(r"^  (\w+) \| (\w+) \| ([\d.]+|-) \| (.+)$", bloco, re.M)}


def frase(s):
    s = s[0].upper() + s[1:]
    return s if s.endswith(".") else s + "."


def evid(i, s):
    if s not in [e["fonte"] for e in i["evidencias"]]:
        i["evidencias"].append({"fonte": s})


cont = {"explicada": 0, "nao_encontrada": 0}
for arq, src in [("objetos-api/ServiceContract.json", "src:objref-servicecontract-264"),
                 ("objetos-api/Entitlement.json", "src:objref-entitlement-264")]:
    T = tabela(src)
    d = ld(arq)
    for i in d["campos"]:
        if i["nome"] not in T or i.get("explicacao") != "pendente":
            continue
        tipo, v, txt = T[i["nome"]]
        if i.get("tipo_tecnico") in (None, "(a extrair)"):
            i["tipo_tecnico"] = tipo
        i["o_que_e"], i["explicacao"] = frase(txt), "explicada"
        evid(i, src)
        if v != "-" and i.get("disponibilidade", {}).get("estado") == "desconhecido":
            i["disponibilidade"] = {"desde_versao": v, "ate_versao": None, "estado": "verificado"}
        cont["explicada"] += 1
    d["cobertura"]["explicativa"]["presente"] = sum(1 for x in d["campos"] if x.get("explicacao") == "explicada")
    sv(arq, d)

arq, nota = "objetos-api/Case.json", 'Rótulo oficial: "Case Currency"; tamanho 3 (Field Reference 264.0).'
d = ld(arq)
for i in d["campos"]:
    if i["nome"] == "CurrencyIsoCode" and i.get("explicacao") == "pendente":
        i["o_que_e"], i["explicacao"] = NAO, "nao_encontrada"
        evid(i, "src:fieldref-case-264")
        if i.get("tipo_tecnico") in (None, "(a extrair)"):
            i["tipo_tecnico"] = "picklist"
        velha = "Nome listado na Field Reference; tipo e propriedades não extraídos nesta rodada."   # o tipo agora foi extraído
        i["notas"] = [x for x in i.get("notas", []) if x not in (nota, velha)] + [nota]
        cont["nao_encontrada"] += 1
d["cobertura"]["explicativa"]["presente"] = sum(1 for x in d["campos"] if x.get("explicacao") == "explicada")
sv(arq, d)
print(f"lote 8h: {cont}")
