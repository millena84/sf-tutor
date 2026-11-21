"""Lote 7y13 (issue #10, etapa 2): decisões da autora em 2026-11-20.

- cria o critério de exclusão X3 (produto aposentado) e marca os 7 tipos do Chat legado com o bloco "aposentado";
- Messaging (3 tipos): excluídos por C3 com inferido;
- MacroSettings: inclusão marcada como não confirmada (inferido + nota).
Nada é cadastrado no catálogo. Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-20"
EXTR = "fontes/extracoes/lote7y13-core-decisoes-autora.txt"

C.registrar_fontes([
    C.fonte("src:objref-lista-releases", "Object Reference: seletor de versões (Winter '26 a Summer '26)",
            "https://developer.salesforce.com/docs/atlas.en-us.226.0.api.meta/api/sforce_api_objects_currencytype.htm",
            "Correspondência entre nome de release e versão da API (Spring '26 = API 66.0).", EXTR, DATA, versao="226.0 (seletor mostra até 67.0)",
            metodo="leitura_resultado_busca"),
])

X3 = {"id": "X3", "texto": "Produto aposentado: tipos que ainda constam da cobertura de metadados da versão, mas cujo produto foi aposentado, "
                           "ficam fora do Core e levam o bloco 'aposentado' (data, release e fonte). (Decisão da autora em 2026-11-20.)"}
CHAT = ["LiveAgentSettings", "LiveChatAgentConfig", "LiveChatButton", "LiveChatDeployment", "LiveChatSensitiveDataRule",
        "EmbeddedServiceLiveAgent", "EmbeddedServiceBranding"]
APOS = {"data": "2026-02-14", "release": "Spring '26 (API 66.0)", "fonte": "src:chat-rest-edicoes", "release_inferida": True,
        "evidencia_release": {"fonte": "src:objref-lista-releases"},
        "nota_release": "A fonte oficial dá só a data (14/02/2026). A release foi deduzida pela data, que cai no período da Spring '26 "
                        "(API 66.0, entre a Winter '26 e a Summer '26 no seletor de versões); o calendário de releases não foi lido."}
MSG = ["MessagingChannel", "ConversationMessageDefinition", "LiveMessageSettings"]
NOTA_MSG = ("Associação exclusiva ao atendimento inferida (orientação da autora em 2026-11-20): as fontes lidas ligam Messaging a "
            "Omni-Channel e a Service Cloud Voice, mas nenhuma diz que ele é exclusivo de atendimento. Pendente de confirmação.")
NOTA_MACRO = ("Inclusão não confirmada (orientação da autora em 2026-11-20): a decisão vem da regra C2 ajustada, sem frase oficial que "
              "diga que macros não exigem licença de produto.")

esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
if not any(x["id"] == "X3" for x in esc["criterios_exclusao"]):
    esc["criterios_exclusao"].append(X3)
cc = esc["classificacao_core_por_item"]
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])

for t in CHAT:
    j = just[t]
    assert j.get("familia") == "Atendimento (Service Cloud)", t
    j.update(decisao="excluido", criterios=["X3"], aposentado=APOS, data=DATA,
             motivo="Produto de chat legado, aposentado em 14/02/2026 (fonte oficial). Fica fora do Core pelo X3 e continua no inventário "
                    "v68 porque ainda consta da cobertura dessa versão. Antes do aposentamento, servia a Service Cloud e a Sales Cloud.")
    exc.add(t); inc.discard(t)
for t in MSG:
    j = just[t]
    assert j.get("familia") == "Atendimento (Service Cloud)", t
    j.update(decisao="excluido", criterios=["C3"], nuvens=["nuv:service-cloud"], inferido=True, nota_inferencia=NOTA_MSG, data=DATA,
             motivo="Associado a Agentforce Service (fora do Core por ser específico dessa nuvem), com ressalva: associação inferida.")
    exc.add(t); inc.discard(t)
m = just["MacroSettings"]
assert m["decisao"] == "incluido"
m.update(inferido=True, nota_inferencia=NOTA_MACRO)

cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y13: {len(CHAT)} aposentados (X3), {len(MSG)} Messaging excluídos com inferido, MacroSettings não confirmado")
