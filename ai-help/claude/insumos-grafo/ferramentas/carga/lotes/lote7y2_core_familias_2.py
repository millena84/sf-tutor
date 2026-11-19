"""Lote 7y2 (issue #10, etapa 2, lote 2): recorte Core por família, mesmo padrão do lote 7y.

Famílias: Discovery Framework, Salesforce Pricing e Public Sector (excluídas por X2) e Agentforce IT Service (pendente por C2: a frase
de edição lida não esclarece a licença). Nada é cadastrado no catálogo.

Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/, depois de lote7y_core_familias_1.py.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-18"
EXTR = "fontes/extracoes/lote7y2-core-familias-2.txt"
B = "https://developer.salesforce.com/docs/"
SV = "sem versão na URL"

C.registrar_fontes([
    C.fonte("src:discovery-framework-metadata-types", "Industries Common Resources: Discovery Framework Metadata API Types",
            B + "industries/industries-common-dev/guide/discovery-framework-metadata-api-parent.html",
            "Lista oficial dos metadata types de Discovery Framework.", EXTR, DATA, versao=SV),
    C.fonte("src:discovery-framework-guia", "Industries Common Resources: Discovery Framework",
            B + "industries/industries-common-dev/guide/discovery-framework.html",
            "Edições: Discovery Framework vem incluído em Financial Services Cloud, Health Cloud, Public Sector Solutions e Consumer Goods Cloud.",
            EXTR, DATA, versao=SV),
    C.fonte("src:pricing-metadata-types", "Revenue Management: Salesforce Pricing Metadata API Types",
            B + "revenue/revenue-management/guide/pricing-metadata-api-parent.html",
            "Lista oficial dos metadata types de Salesforce Pricing.", EXTR, DATA, versao=SV),
    C.fonte("src:rlm-pcm-overview", "Revenue Management: Product Catalog Management",
            B + "revenue/revenue-management/guide/pcm-overview.html",
            "Edições: Enterprise, Unlimited e Developer de Revenue Management.", EXTR, DATA, versao=SV, metodo="leitura_resultado_busca"),
    C.fonte("src:psc-metadata-types", "Public Sector Solutions Metadata API Types",
            B + "atlas.en-us.psc_api.meta/psc_api/psc_metadata_api_parent.htm",
            "Lista oficial dos metadata types de Public Sector Solutions.", EXTR, DATA, versao=SV),
    C.fonte("src:psc-data-model-edicoes", "Public Sector: Talent Recruitment Management Data Model",
            B + "industries/public-sector-dev/guide/psc-data-model-talent-recruitment-management.html",
            "Edições: Enterprise, Performance, Unlimited e Developer com Public Sector.", EXTR, DATA, versao=SV, metodo="leitura_resultado_busca"),
    C.fonte("src:aits-tooling-objects", "Agentforce IT Service Tooling API Objects",
            B + "service/agentforce-it-service/guide/agentforce-it-service-tooling-api-parent.html",
            "Lista oficial dos objetos de configuração de Agentforce IT Service.", EXTR, DATA, versao=SV),
    C.fonte("src:aits-edicoes", "Agentforce IT Service Platform Event",
            B + "service/agentforce-it-service/guide/agentforce-it-service-platform-event.html",
            "Edições: Enterprise e Unlimited; a frase não trata de licença.", EXTR, DATA, versao=SV, metodo="leitura_resultado_busca"),
])


def ev(lista, licenca):
    return [{"fonte": lista, "uso": "lista"}, {"fonte": licenca, "uso": "licenca"}]


EXC = {"decisao": "excluido", "criterios": ["C1", "X2"]}
FAMILIAS = {
    "Discovery Framework": {**EXC, "nuvens": ["nuv:industries"],
        "tipos": ["AssessmentQuestion", "AssessmentQuestionSet", "DocumentCategory", "DocumentCategoryDocumentType", "DocumentType"],
        "evidencias": ev("src:discovery-framework-metadata-types", "src:discovery-framework-guia"),
        "motivo": "Listado entre os metadata types de Discovery Framework, que só vem incluído em nuvens de setor (Financial Services, "
                  "Health, Public Sector e Consumer Goods). Depende de produto de setor."},
    "Salesforce Pricing": {**EXC, "nuvens": ["nuv:revenue"],
        "tipos": ["IndustriesPricingSettings", "PricingActionParameters", "PricingRecipe", "ProcedureOutputResolution"],
        "evidencias": ev("src:pricing-metadata-types", "src:rlm-pcm-overview"),
        "motivo": "Listado entre os metadata types de Salesforce Pricing, parte de Revenue Management, disponível nas edições de "
                  "Revenue Management. Depende de produto."},
    "Public Sector": {**EXC, "nuvens": ["nuv:industries"],
        "tipos": ["ApplicationRecordTypeConfig", "DocumentChecklistSettings"],
        "evidencias": ev("src:psc-metadata-types", "src:psc-data-model-edicoes"),
        "motivo": "Listado entre os metadata types de Public Sector Solutions, disponível só em edições com Public Sector. "
                  "Depende de produto de setor."},
    "Agentforce IT Service": {"decisao": "pendente", "criterios": ["C2"], "nuvens": [],
        "tipos": ["CnfgItemAttrDef", "CnfgItemAttrPcklstValDef", "CnfgItemAttrPicklistDef", "CnfgItemAttrSetAttr", "CnfgItemAttrSetDef",
                  "CnfgItemTypeAttrRelDef", "CnfgItemTypeDef", "CnfgItemTypeIdentFieldMap", "CnfgItemTypeIdentRule", "CnfgItemTypeRelationDef",
                  "CnfgMgmtRelationTypeDef", "CnfgMgmtSvcMapLyot", "ServiceMgmtKnwlgArtclConfig", "SrvcMgmtObjCollabAppCnfg"],
        "evidencias": ev("src:aits-tooling-objects", "src:aits-edicoes"),
        "motivo": "Listado entre os objetos de configuração de Agentforce IT Service. A frase de edição lida (Enterprise e Unlimited) "
                  "não esclarece se o produto exige licença própria; fica pendente pelo C2 até haver fonte."},
}

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])
cont = {}
for fam, d in FAMILIAS.items():
    for t in d["tipos"]:
        assert t in inv, f"{t} não consta do inventário v68"
        atual = just.get(t)
        assert atual is None or atual.get("familia") == fam, f"{t} já tem outra decisão; não sobrescrever"
        just[t] = {"decisao": d["decisao"], "criterios": d["criterios"], "motivo": d["motivo"], "familia": fam, "nuvens": d["nuvens"],
                   "evidencias": d["evidencias"], "alcance_da_licenca": "familia", "data": DATA}
        inc.discard(t); exc.discard(t)
        if d["decisao"] == "excluido":
            exc.add(t)
        cont[d["decisao"]] = cont.get(d["decisao"], 0) + 1
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y2: {cont}")
