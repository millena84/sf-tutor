"""Lote 7y12 (issue #10, etapa 2, lote 12): Field Service, Salesforce Scheduler e serviço de campo de Manufacturing Cloud.

Nada é cadastrado no catálogo. Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-20"
EXTR = "fontes/extracoes/lote7y12-core-field-service.txt"
BUSCA = "leitura_resultado_busca"

C.registrar_fontes([
    C.fonte("src:fs-dev-mdapi-264", "Field Service Developer Guide 264.0: Field Service Metadata API",
            "https://developer.salesforce.com/docs/get_document_content/field_service_dev/fsl_dev_metadata.htm/en-us/264.0",
            "Lista dos metadata types usados em Field Service.", EXTR, DATA),
    C.fonte("src:mdapi-appointmentschedulingpolicy-264", "AppointmentSchedulingPolicy (Metadata API 264.0)",
            "https://developer.salesforce.com/docs/get_document_content/api_meta/meta_appointmentschedulingpolicy.htm/en-us/264.0",
            "Regras de agendamento do Lightning Scheduler.", EXTR, DATA),
    C.fonte("src:mdapi-appointmentassignmentpolicy-264", "AppointmentAssignmentPolicy (Metadata API 264.0)",
            "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/meta_appointmentassignmentpolicy.htm",
            "Regra de atribuição de recursos (balanceamento de carga).", EXTR, DATA, metodo=BUSCA),
    C.fonte("src:hc-scheduler-addon", "Health Cloud: Enable Salesforce Scheduler and Omni-Channel for Utilization Management",
            "https://developer.salesforce.com/docs/atlas.en-us.health_cloud.meta/null/admin_utlization_management_salesforce_scheduler.htm",
            "Habilitar o Salesforce Scheduler pede a licença Lightning Scheduler Add-On.", EXTR, DATA, versao="sem versão na URL",
            metodo=BUSCA),
    C.fonte("src:mfg-settings-list-258", "Manufacturing Cloud Developer Guide 258.0: Settings da Metadata API",
            "https://developer.salesforce.com/docs/atlas.en-us.258.0.mfg_api_devguide.meta/mfg_api_devguide/mfg_settings_metadata_api_parent.htm",
            "Lista de Settings de Manufacturing Cloud (versão 258.0; a 264.0 não foi lida).", EXTR, DATA, versao="258.0", metodo=BUSCA),
])

FS, SCH, MFG = "Field Service", "Salesforce Scheduler", "Manufacturing Cloud"
NOTA_SCH = ("O Salesforce Scheduler não tem nó próprio no mapa; a ligação a Industries é inferida (as fontes lidas o mostram em Health "
            "Cloud e em Financial Services Cloud). A exclusão do Core vem da licença e não depende dessa inferência.")
DECISOES = {
    "TimeSheetTemplate": dict(
        familia=FS, decisao="excluido", criterios=["C2", "X2"], nuvens=["nuv:field-service"], alcance_da_licenca="familia",
        motivo="Listado entre os metadata types de Field Service, produto com licenças próprias (como FieldServiceSettings na etapa 1). "
               "Continua no mapa como parte do produto.",
        evidencias=[{"fonte": "src:fs-dev-mdapi-264", "uso": "lista"}, {"fonte": "src:help-fs-key-concepts", "uso": "licenca"}]),
    "Skill": dict(
        familia=FS, decisao="pendente", criterios=["C2", "C3"], nuvens=["nuv:field-service", "nuv:service-cloud"],
        alcance_da_licenca="nao_se_aplica",
        motivo="Habilidades servem a Field Service, ao roteamento de atendimento (Omni-Channel), a Salesforce Scheduler e a Workforce "
               "Engagement: várias nuvens, nenhuma delas a plataforma. Nenhuma fonte lida diz se o tipo exige licença.",
        evidencias=[{"fonte": "src:fs-dev-mdapi-264", "uso": "lista"}]),
    **{t: dict(familia=SCH, decisao="excluido", criterios=["C2"], nuvens=["nuv:industries"], alcance_da_licenca="familia",
               motivo="Faz parte do Salesforce Scheduler, que exige a licença Lightning Scheduler Add-On. Fica fora do Core.",
               evidencias=[{"fonte": src, "uso": "lista"}, {"fonte": "src:hc-scheduler-addon", "uso": "licenca"}],
               inferido=True, nota_inferencia=NOTA_SCH)
       for t, src in [("AppointmentSchedulingPolicy", "src:mdapi-appointmentschedulingpolicy-264"),
                      ("AppointmentAssignmentPolicy", "src:mdapi-appointmentassignmentpolicy-264")]},
    **{t: dict(familia=MFG, decisao="excluido", criterios=["C3"], nuvens=["nuv:industries"], alcance_da_licenca="nao_se_aplica",
               motivo="Listado entre os Settings de Manufacturing Cloud, nuvem de setor; específico dessa nuvem. Continua no mapa em Industries.",
               evidencias=[{"fonte": "src:mfg-settings-list-258", "uso": "lista"}])
       for t in ["IndustriesFieldServiceSettings", "InventoryReplenishmentSettings"]},
}

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])
for t, d in DECISOES.items():
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == d["familia"], f"{t}: já tem outra decisão"
    just[t] = {**d, "data": DATA}
    inc.discard(t); exc.discard(t)
    if d["decisao"] == "excluido":
        exc.add(t)
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
n = {k: sum(d["decisao"] == k for d in DECISOES.values()) for k in ("excluido", "pendente")}
print(f"lote 7y12: {n['excluido']} excluídos (2 com inferido), {n['pendente']} pendente com motivo")
