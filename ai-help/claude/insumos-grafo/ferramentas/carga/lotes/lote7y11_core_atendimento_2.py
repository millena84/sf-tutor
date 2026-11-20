"""Lote 7y11 (issue #10, etapa 2, lote 11): família Atendimento (Service Cloud), parte 2.

Workforce Engagement e gestão de incidentes saem do Core por licença (C2); MacroSettings entra pelo C2 ajustado e pelo C3.
Nada é cadastrado no catálogo. Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-20"
EXTR = "fontes/extracoes/lote7y11-core-atendimento-2.txt"
BUSCA = "leitura_resultado_busca"
B264 = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
FAMILIA = "Atendimento (Service Cloud)"
SV = "sem versão na URL"

C.registrar_fontes([
    C.fonte("src:wem-cookbook-metadata", "Workforce Engagement Cookbook: Workforce Engagement Metadata and Tooling API Reference",
            "https://developer.salesforce.com/docs/service/wem-cookbook-dev-guide/guide/workforce-engagement-metadata.html",
            "Componentes de metadados que vêm com Workforce Engagement habilitado; aviso de aposentadoria programada.", EXTR, DATA,
            versao=SV, metodo=BUSCA),
    C.fonte("src:mdapi-workforceengagementsettings-264", "WorkforceEngagementSettings (Metadata API 264.0)",
            B264 + "meta_workforceengagementsettings.htm", "Configurações de Workforce Engagement; exige licença Workforce Engagement.",
            EXTR, DATA, metodo=BUSCA),
    C.fonte("src:mdapi-incidentmgmtsettings", "IncidentMgmtSettings (Metadata API, página atual)",
            "https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_incidentmgmtsettings.htm",
            "Customer Service Incident Management e Broadcast Communications; exige licença de Service Cloud.", EXTR, DATA,
            versao=SV, metodo=BUSCA),
    C.fonte("src:mdapi-macrosettings-264", "MacroSettings (Metadata API 264.0)", B264 + "meta_macrosettings.htm",
            "Configurações de macros (busca avançada, pastas).", EXTR, DATA, metodo=BUSCA),
    C.fonte("src:objref-macro-264", "Macro (Object Reference 264.0)",
            "https://developer.salesforce.com/docs/atlas.en-us.264.0.object_reference.meta/object_reference/sforce_api_objects_macro.htm",
            "Macros funcionam em objetos padrão e personalizados com quick actions.", EXTR, DATA, metodo=BUSCA),
])

APOS = " O produto está com aposentadoria programada (fonte da família)."
DECISOES = {
    "WorkforceEngagementSettings": {
        "decisao": "excluido", "criterios": ["C2"], "nuvens": ["nuv:service-cloud"], "alcance_da_licenca": "proprio_tipo",
        "motivo": "Exige licença Workforce Engagement (regra na página do próprio tipo). Continua no mapa como parte de Agentforce Service." + APOS,
        "evidencias": [{"fonte": "src:wem-cookbook-metadata", "uso": "lista"},
                       {"fonte": "src:mdapi-workforceengagementsettings-264", "uso": "licenca"}]},
    **{t: {"decisao": "excluido", "criterios": ["C2"], "nuvens": ["nuv:service-cloud"], "alcance_da_licenca": "familia",
           "motivo": "Componente que vem com Workforce Engagement habilitado, produto com licença própria. Continua no mapa como parte de "
                     "Agentforce Service." + APOS,
           "evidencias": [{"fonte": "src:wem-cookbook-metadata", "uso": "lista"},
                          {"fonte": "src:mdapi-workforceengagementsettings-264", "uso": "licenca"}]}
       for t in ["SchedulingObjective", "SchedulingRule"]},
    "IncidentMgmtSettings": {
        "decisao": "excluido", "criterios": ["C2", "C3"], "nuvens": ["nuv:service-cloud"], "alcance_da_licenca": "proprio_tipo",
        "motivo": "Exige licença de Service Cloud (regra na página do próprio tipo) e é específico do atendimento (incidentes e comunicados). "
                  "Continua no mapa como parte de Agentforce Service.",
        "evidencias": [{"fonte": "src:mdapi-incidentmgmtsettings", "uso": "lista"}, {"fonte": "src:mdapi-incidentmgmtsettings", "uso": "licenca"}]},
    "MacroSettings": {
        "decisao": "incluido", "criterios": ["C1", "C2", "C3"], "nuvens": ["nuv:platform-core"], "alcance_da_licenca": "nao_se_aplica",
        "motivo": "Sem registro de licença de produto, e macros funcionam em objetos padrão e personalizados com quick actions (não numa nuvem "
                  "só). Entra no Core pelo C2 ajustado.",
        "evidencias": [{"fonte": "src:mdapi-macrosettings-264", "uso": "lista"}, {"fonte": "src:objref-macro-264", "uso": "lista"}]},
}

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])
for t, d in DECISOES.items():
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == FAMILIA, f"{t}: já tem outra decisão"
    just[t] = {**d, "familia": FAMILIA, "data": DATA}
    (inc if d["decisao"] == "incluido" else exc).add(t)
    (exc if d["decisao"] == "incluido" else inc).discard(t)
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
n_exc = sum(d["decisao"] == "excluido" for d in DECISOES.values())
print(f"lote 7y11: {n_exc} excluídos, {len(DECISOES) - n_exc} incluído")
