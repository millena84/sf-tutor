"""Lote 8d (Fase 2, Processos de negócio, Vendas parte 1): Product2, OpportunityLineItem, Opportunity e ContractSettings.

Lê a tabela da nota de extração (nome | tipo | versão | descrição) e grava tipo, explicação e versão. Os itens sem descrição oficial
ficam com explicacao = "nao_encontrada". Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv               # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-19"
EXTR = "fontes/extracoes/lote8d-fase2-vendas-1.txt"
G = "https://developer.salesforce.com/docs/get_document_content/object_reference/"
C.registrar_fontes([
    C.fonte("src:objref-product2-264", "Product2 (Object Reference 264.0)", G + "sforce_api_objects_product2.htm/en-us/264.0", "Campos de Product2.", EXTR, DATA),
    C.fonte("src:objref-opportunitylineitem-264", "OpportunityLineItem (Object Reference 264.0)", G + "sforce_api_objects_opportunitylineitem.htm/en-us/264.0",
            "Campos de OpportunityLineItem.", EXTR, DATA),
    C.fonte("src:fieldref-opportunity-atual", "Opportunity (Field Reference, referência nova)",
            "https://developer.salesforce.com/docs/platform/field-reference/references/field-reference/salesforce-field-reference-opportunity.html",
            "Tipo e rótulo de OpportunityScoreId e ReferralCode.", EXTR, DATA, versao="sem versão na página", metodo="leitura_resultado_busca"),
    C.fonte("src:rn-vendas1-busca", "Notas de versão da Salesforce: busca pelos nomes sem descrição (lote 8d)",
            "https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-contractsettings.html",
            "ContractSettings: a referência atual só dá tipo; nenhuma menção nas notas de versão (busca).", EXTR, DATA,
            versao="Winter '27 (busca)", metodo="leitura_resultado_busca"),
])
V = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "config", "versoes.json"), encoding="utf-8"))["plataforma_core"]
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

ALVOS = [("objetos-api/Product2.json", "src:objref-product2-264"), ("objetos-api/OpportunityLineItem.json", "src:objref-opportunitylineitem-264")]
NAO_ENC = {"metadata-types/ContractSettings.json": (["autoExpirationDelay", "autoExpirationRecipient", "autoExpireContracts", "enableContractHistoryTracking"],
                                                    "src:rn-vendas1-busca", {}),
           "objetos-api/Opportunity.json": (["OpportunityScoreId", "ReferralCode"], "src:fieldref-opportunity-atual",
                                            {"OpportunityScoreId": ("reference", 'Rótulo oficial: "Opportunity Score ID".'),
                                             "ReferralCode": ("string", 'Rótulo oficial: "Referral Code"; até 255 caracteres.')})}
cont = {"explicada": 0, "nao_encontrada": 0}

def evid(i, s):
    if s not in [e["fonte"] for e in i["evidencias"]]:
        i["evidencias"].append({"fonte": s})

for arq, src in ALVOS:
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

for arq, (nomes, src, extra) in NAO_ENC.items():
    d = ld(arq)
    chave = "campos" if "campos" in d else "propriedades"
    for i in d[chave]:
        if i["nome"] not in nomes or i.get("explicacao") != "pendente":
            continue
        i["o_que_e"], i["explicacao"] = NAO, "nao_encontrada"
        evid(i, src)
        if i["nome"] in extra:
            tipo, nota = extra[i["nome"]]
            if i.get("tipo_tecnico") in (None, "(a extrair)"):
                i["tipo_tecnico"] = tipo
            i["notas"] = [x for x in i.get("notas", []) if x != nota] + [nota]
        cont["nao_encontrada"] += 1
    if d.get("cobertura", {}).get("explicativa") is not None:
        d["cobertura"]["explicativa"]["presente"] = sum(1 for x in d[chave] if x.get("explicacao") == "explicada")
    sv(arq, d)
print(f"lote 8d: {cont}")
