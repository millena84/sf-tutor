"""Lote 7y4 (issue #10, etapa 2, lote 4): Settings de plataforma e regra C4 (Agentforce condicional).

1. Settings: a página geral de Settings da Metadata API (264.0) dá uma frase por tipo. Pelo C2 ajustado, os que configuram a plataforma e
   não têm registro de licença entram no Core; os que citam recurso com indício de licença ficam pendentes.
2. C4 (decisão da autora em 2026-11-19): tipos de Agentforce ou IA generativa que só funcionam com Agentforce habilitado ficam como
   "condicional": ligados ao Core e às nuvens que os usam (Sales, Service etc.), com a condição registrada. Nenhum tipo é reclassificado
   aqui; a regra fica disponível para o lote da família de IA.
Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-19"
SRC = "src:mdapi-settings-264"
C.registrar_fontes([C.fonte(SRC, "Settings (Metadata API Developer Guide 264.0)",
    "https://developer.salesforce.com/docs/get_document_content/api_meta/meta_settings.htm/en-us/264.0",
    "Lista dos tipos Settings com uma frase cada.", "fontes/extracoes/lote7y4-core-settings-plataforma.txt", DATA)])

INCLUIR = ["ActionsSettings", "ActivitiesSettings", "AddressSettings", "CodeBuilderSettings", "CustomAddressFieldSettings",
           "DataImportManagementSettings", "DynamicFormsSettings", "EmailAdministrationSettings", "EmailAuthorizationSettings",
           "EmailTemplateSettings", "EnhancedNotesSettings", "FileUploadAndDownloadSecuritySettings", "HelpSettings", "IdentityProviderSettings",
           "IframeWhiteListUrlSettings", "InvocableActionSettings", "MobileSettings", "NameSettings", "OrgSettings", "PicklistSettings",
           "RecordPageSettings", "SandboxSettings", "SchemaSettings", "SearchSettings", "SecuritySettings", "SharingSettings", "SiteSettings",
           "UserEngagementSettings", "UserInterfaceSettings", "UserManagementSettings"]
PENDENTES = {
    "EventSettings": "Configura platform events para Event Monitoring, recurso com indício de add-on (Shield); falta frase de licença.",
    "RealTimeEventSettings": "Configura o monitoramento de eventos em tempo real, com indício de add-on; falta frase de licença.",
    "EmailIntegrationSettings": "Inclui Salesforce Inbox, vendido à parte, junto com as integrações de Outlook e Gmail; falta separar o que exige licença.",
    "ObjectLinkingSettings": "Vinculação canal-objeto (Beta); parece específica de canais de atendimento, sem fonte que confirme.",
    "NotificationsSettings": "A página de Settings repete a frase de MobileSettings para este tipo; descrição inconsistente, precisa de outra fonte.",
}

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
crit = esc["criterios_inclusao"]
if not any(c["id"] == "C4" for c in crit):
    crit.append({"id": "C4", "texto": "Agentforce e IA generativa: tipos que só funcionam com Agentforce habilitado na org ficam como "
                 "'condicional': ligados ao Core e às nuvens que os usam (Sales, Service e outras), com a condição registrada. Não contam como "
                 "Core puro nem como excluídos. (Decisão da autora em 2026-11-19; diverge do C2, que deixaria esses tipos fora por licença.)"})
cc = esc["classificacao_core_por_item"]
cc.setdefault("condicionais", [])
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])
ev = [{"fonte": SRC, "uso": "lista"}]
cont = {"incluido": 0, "pendente": 0}
for t in INCLUIR + list(PENDENTES):
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == "Settings de plataforma", f"{t} já tem outra decisão"
    if t in PENDENTES:
        j = {"decisao": "pendente", "criterios": ["C2"], "motivo": PENDENTES[t]}
        inc.discard(t)
    else:
        j = {"decisao": "incluido", "criterios": ["C1", "C2", "C3"],
             "motivo": "Configura a plataforma (frase da página de Settings) e não há registro de licença de produto. Entra no Core pelo C2 ajustado."}
        inc.add(t)
    exc.discard(t)
    just[t] = {**j, "familia": "Settings de plataforma", "nuvens": ["nuv:platform-core"], "evidencias": ev,
               "alcance_da_licenca": "nao_se_aplica", "data": DATA}
    cont[j["decisao"]] += 1
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y4: {cont}")
