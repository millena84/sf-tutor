"""Lote 7y (issue #10, etapa 2, lote 1): recorte Core de tipos ainda não catalogados, por família, com uma fonte de lista por família.

Famílias deste lote: Health Cloud, Net Zero Cloud e Omnistudio. Todas ficam fora do Core pelo critério X2 (dependem de produto de setor),
mas continuam no inventário. Nada é cadastrado no catálogo: só a decisão de recorte em config/escopo.json, com evidências.

Campos de cada decisão (justificativas[<tipo>]):
  decisao, criterios, motivo, familia, nuvens, data e evidencias = [{fonte, uso}], onde uso é:
    - "lista": a fonte de lista da família mostra o nome do tipo;
    - "licenca": frase de edição ou licença usada na decisão;
  e alcance_da_licenca = "proprio_tipo" (a frase está na página do próprio tipo) ou "familia" (a frase vale para o produto ou foi lida
  em outro tipo da mesma lista).
O validador confere que todo tipo com evidência de "lista" aparece na nota de extração da fonte citada.

Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-18"
EXTR = "fontes/extracoes/lote7y-core-familias-1.txt"
B = "https://developer.salesforce.com/docs/"

C.registrar_fontes([
    C.fonte("src:hc-dev-metadata-types", "Health Cloud Developer Guide: Metadata Types", B + "industries/health-cloud-dev-guide/guide/hc-metadata-types.html",
            "Lista oficial dos metadata types de Health Cloud (família do recorte Core).", EXTR, DATA, versao="sem versão na URL"),
    C.fonte("src:hc-dev-guia", "Health Cloud Developer Guide", B + "industries/health-cloud-dev-guide/guide/object-ref-overview.html",
            "Edições exigidas: Enterprise e Unlimited com Health Cloud.", EXTR, DATA, versao="sem versão na URL"),
    C.fonte("src:nzc-dev-metadata-types", "Net Zero Cloud Developer Guide: Metadata API Types",
            B + "industries/netzero-cloud-dev-guide/guide/netzero-cloud-metadata-api-parent.html",
            "Lista oficial dos metadata types de Net Zero Cloud (família do recorte Core).", EXTR, DATA, versao="sem versão na URL"),
    C.fonte("src:nzc-dev-tooling", "Net Zero Cloud Developer Guide: Tooling API Objects",
            B + "atlas.en-us.netzero_cloud_dev_guide.meta/netzero_cloud_dev_guide/netzero_cloud_tooling_api_parent.htm",
            "Lista de objetos de configuração de Net Zero Cloud; cobre três nomes ausentes da lista da Metadata API do guia.", EXTR, DATA,
            versao="sem versão na URL"),
    C.fonte("src:nzc-dev-campos-padrao", "Net Zero Cloud Fields on Standard Objects",
            B + "industries/netzero-cloud-dev-guide/guide/netzero-cloud-fields-on-standard-objects-parent.html",
            "Edições exigidas: Enterprise, Performance e Unlimited com Net Zero Cloud habilitado.", EXTR, DATA, versao="sem versão na URL",
            metodo="leitura_resultado_busca"),
    C.fonte("src:omnistudio-metadata-types", "Industries Common Resources: Omnistudio Metadata API Types",
            B + "industries/industries-common-dev/guide/omnistudio-metadata-api-parent.html",
            "Lista oficial dos metadata types de Omnistudio (família do recorte Core).", EXTR, DATA, versao="sem versão na URL"),
    C.fonte("src:omnistudio-integrationprocedure", "Industries Common Resources: OmniIntegrationProcedure",
            B + "atlas.en-us.industries_reference.meta/industries_reference/meta_omniintegrationprocedure.htm",
            "Special Access Rules: exige licença Omnistudio.", EXTR, DATA, versao="sem versão na URL"),
])


def ev(lista, licenca):
    return [{"fonte": lista, "uso": "lista"}, {"fonte": licenca, "uso": "licenca"}]


FAMILIAS = {
    "Health Cloud": {
        "tipos": ["CareBenefitVerifySettings", "CareLimitType", "CareProviderSearchConfig", "CareRequestConfiguration", "CareSystemFieldMapping",
                  "DocumentExtractionDef", "Icon", "IdentityVerificationProcDef", "ScoreCategory", "TimelineObjectDefinition",
                  "UIObjectRelationConfig", "VirtualVisitConfig"],
        "evidencias": ev("src:hc-dev-metadata-types", "src:hc-dev-guia"),
        "motivo": "Listado entre os metadata types de Health Cloud, disponível só em edições com Health Cloud. Depende de produto de setor.",
    },
    "Net Zero Cloud": {
        "tipos": ["ClauseCatgConfiguration", "DisclosureDefinition", "DisclosureDefinitionVersion", "DisclosureType", "FuelType",
                  "FuelTypeSustnUom", "SustnUomConversion", "SustainabilityUom"],
        "evidencias": ev("src:nzc-dev-metadata-types", "src:nzc-dev-campos-padrao"),
        "motivo": "Listado entre os metadata types de Net Zero Cloud, disponível só em orgs com Net Zero Cloud habilitado. Depende de produto de setor.",
    },
    "Net Zero Cloud (configuração)": {
        "tipos": ["BldgEnrgyIntensityCnfg", "StnryAssetEnvSrcCnfg", "VehicleAssetEmssnSrcCnfg"],
        "evidencias": ev("src:nzc-dev-tooling", "src:nzc-dev-campos-padrao"),
        "motivo": "Listado entre os objetos de configuração de Net Zero Cloud (Tooling API do guia), disponível só em orgs com Net Zero Cloud "
                  "habilitado. Depende de produto de setor.",
    },
    "Omnistudio": {
        "tipos": ["DataMapperDefinition", "FlexcardDefinition", "IntegrationProcdDefinition", "OmniDataTransform", "OmniExtTrackingDef",
                  "OmniIntegrationProcedure", "OmniInteractionAccessConfig", "OmniInteractionConfig", "OmniScript", "OmniscriptDefinition",
                  "OmniStudioSettings", "OmniTrackingGroup"],
        "evidencias": ev("src:omnistudio-metadata-types", "src:omnistudio-integrationprocedure"),
        "motivo": "Listado entre os metadata types de Omnistudio, produto que exige licença Omnistudio. Depende de produto de setor.",
    },
}
# Nota específica: a página do próprio tipo Icon foi lida (pelo resultado de busca) e cita a licença.
NOTAS = {
    "Icon": " A página do tipo também diz que ele exige licença de Health Cloud ou de Financial Services Cloud.",
    "OmniIntegrationProcedure": " A regra de licença está na página do próprio tipo.",
}
PROPRIO = {"OmniIntegrationProcedure"}

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])
n = 0
for fam, d in FAMILIAS.items():
    for t in d["tipos"]:
        assert t in inv, f"{t} não consta do inventário v68"
        atual = just.get(t)
        assert atual is None or atual.get("familia"), f"{t} já tem decisão da etapa 1; não sobrescrever"
        just[t] = {"decisao": "excluido", "criterios": ["C1", "X2"], "motivo": d["motivo"] + NOTAS.get(t, ""),
                   "familia": fam.split(" (")[0], "nuvens": ["nuv:industries"], "evidencias": d["evidencias"],
                   "alcance_da_licenca": "proprio_tipo" if t in PROPRIO else "familia", "data": DATA}
        inc.discard(t); exc.add(t); n += 1
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y: {n} tipos decididos em {len(FAMILIAS)} grupos de família")
