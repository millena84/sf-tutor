"""Lote 7y10 (issue #10, etapa 2, lote 10): família Atendimento (Service Cloud / Agentforce Service).

Excluídos pelo C3 (específicos da nuvem de atendimento, que é nó próprio do mapa), como CaseSettings e ServiceChannel na etapa 1.
Chat legado, Embedded Service e Messaging ficam pendentes, com motivo. Nada é cadastrado no catálogo. Reexecutável.
Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-20"
EXTR = "fontes/extracoes/lote7y10-core-atendimento.txt"
BUSCA = "leitura_resultado_busca"
B264 = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
FAMILIA = "Atendimento (Service Cloud)"


def f264(nome, pert):
    return C.fonte(f"src:mdapi-{nome.lower()}-264", f"{nome} (Metadata API 264.0)", B264 + f"meta_{nome.lower()}.htm", pert, EXTR, DATA,
                   metodo=BUSCA)


C.registrar_fontes([
    C.fonte("src:omni-dev-mdapi-types", "Omni-Channel Developer Guide: Omni-Channel Metadata API Types",
            "https://developer.salesforce.com/docs/atlas.en-us.omni_channel_dev.meta/omni_channel_dev/omnichannel_metadata_api_intro.htm",
            "Lista dos metadata types usados com Omni-Channel.", EXTR, DATA, versao="sem versão na URL", metodo=BUSCA),
    f264("ServiceCloudVoiceSettings", "Configurações de Service Cloud Voice da org."),
    f264("ConversationVendorInfo", "Ligação entre o sistema do fornecedor parceiro e o recurso de Service Cloud."),
    f264("CallCenterRoutingMap", "Mapeamento de usuário ou fila para o call center de um sistema externo; permissões de contact center."),
    f264("SocialCustomerServiceSettings", "Configurações de Social Customer Service (posts sociais viram casos)."),
    f264("CaseSubjectParticle", "Formato do Subject de casos criados a partir de posts sociais."),
    f264("ServiceSetupAssistantSettings", "Service Setup Assistant, que monta um console de atendimento básico."),
    C.fonte("src:chat-rest-edicoes", "Chat REST API Developer Guide (edições e aposentadoria do chat legado)",
            "https://developer.salesforce.com/docs/atlas.en-us.live_agent_rest.meta/live_agent_rest",
            "Chat disponível com Service Cloud ou Sales Cloud; produto legado aposentado em 14/02/2026.", EXTR, DATA,
            versao="sem versão na URL", metodo=BUSCA),
    C.fonte("src:mdapi-atendimento-canais-264", "Páginas 264.0 da Metadata API dos tipos de Chat, Embedded Service e Messaging", B264,
            "Descrição de LiveAgentSettings, LiveChat*, EmbeddedService*, MessagingChannel, ConversationMessageDefinition e "
            "LiveMessageSettings (uma página por tipo, meta_<nome>.htm).", EXTR, DATA, metodo=BUSCA),
])

MOT_C3 = "Específico de Agentforce Service (atendimento); não é camada compartilhada. Continua no mapa como parte dessa nuvem."
EXCLUIDOS = {
    "OmniSupervisorConfig": "src:omni-dev-mdapi-types",
    "PresenceDeclineReason": "src:omni-dev-mdapi-types",
    "WorkSkillRouting": "src:omni-dev-mdapi-types",
    "ServiceCloudVoiceSettings": "src:mdapi-servicecloudvoicesettings-264",
    "ConversationVendorInfo": "src:mdapi-conversationvendorinfo-264",
    "SocialCustomerServiceSettings": "src:mdapi-socialcustomerservicesettings-264",
    "CaseSubjectParticle": "src:mdapi-casesubjectparticle-264",
    "ServiceSetupAssistantSettings": "src:mdapi-servicesetupassistantsettings-264",
}
INFERIDOS = {
    "CallCenterRoutingMap": ("src:mdapi-callcenterroutingmap-264",
                             "Associação ao atendimento inferida: a página do tipo não cita Service Cloud Voice, mas exige permissões de "
                             "contact center e usa o QuickConnect do Amazon Connect para transferências pelo Omni-Channel. Pendente de "
                             "confirmação."),
}
MOT_CHAT = ("Chat legado: a fonte de edições diz que o Chat existia com Service Cloud ou Sales Cloud (o C3 não fecha como exclusivo de "
            "atendimento) e que o produto foi aposentado em 14/02/2026. Falta decidir como tratar tipos de produto aposentado que ainda "
            "constam do inventário v68.")
MOT_MSG = ("Messaging: nenhuma fonte lida diz se é exclusivo de atendimento ou se também vem com Sales Cloud (como o Chat legado). "
           "Falta frase de edição ou licença.")
PENDENTES = {
    **{t: (["src:chat-rest-edicoes", "src:mdapi-atendimento-canais-264"], ["C3"], MOT_CHAT, ["nuv:service-cloud", "nuv:sales-cloud"])
       for t in ["LiveAgentSettings", "LiveChatAgentConfig", "LiveChatButton", "LiveChatDeployment", "LiveChatSensitiveDataRule",
                 "EmbeddedServiceLiveAgent", "EmbeddedServiceBranding"]},
    "EmbeddedServiceConfig": (["src:mdapi-atendimento-canais-264"], ["C3"],
                              "Serve a Messaging, Chat, agendamento de Field Service e flows embutidos (campo deploymentFeature); por "
                              "servir a mais de uma nuvem, poderia entrar pelo C3, mas falta fonte sobre licença.",
                              ["nuv:service-cloud", "nuv:field-service"]),
    "EmbeddedServiceMenuSettings": (["src:mdapi-atendimento-canais-264"], ["C3"],
                                    "Menu de canais de contato; exige Experiences e Sites habilitados e não há frase que o ligue só ao "
                                    "atendimento.", ["nuv:service-cloud", "nuv:experience-cloud"]),
    **{t: (["src:mdapi-atendimento-canais-264"], ["C2", "C3"], MOT_MSG, ["nuv:service-cloud"])
       for t in ["MessagingChannel", "ConversationMessageDefinition", "LiveMessageSettings"]},
}

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])


def checar(t):
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == FAMILIA, f"{t}: já tem outra decisão"


for t, src in EXCLUIDOS.items():
    checar(t)
    just[t] = {"decisao": "excluido", "criterios": ["C3"], "motivo": MOT_C3, "familia": FAMILIA, "nuvens": ["nuv:service-cloud"],
               "evidencias": [{"fonte": src, "uso": "lista"}], "alcance_da_licenca": "nao_se_aplica", "data": DATA}
    inc.discard(t); exc.add(t)
for t, (src, nota) in INFERIDOS.items():
    checar(t)
    just[t] = {"decisao": "excluido", "criterios": ["C3"], "familia": FAMILIA, "nuvens": ["nuv:service-cloud"],
               "motivo": "Associado a Agentforce Service (fora do Core por ser específico dessa nuvem), com ressalva: associação inferida.",
               "evidencias": [{"fonte": src, "uso": "lista"}], "alcance_da_licenca": "nao_se_aplica", "inferido": True,
               "nota_inferencia": nota, "data": DATA}
    inc.discard(t); exc.add(t)
for t, (srcs, crit, mot, nuvens) in PENDENTES.items():
    checar(t)
    just[t] = {"decisao": "pendente", "criterios": crit, "familia": FAMILIA, "nuvens": nuvens, "motivo": mot,
               "evidencias": [{"fonte": s, "uso": "lista"} for s in srcs], "alcance_da_licenca": "nao_se_aplica", "data": DATA}
    inc.discard(t); exc.discard(t)
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y10: {len(EXCLUIDOS) + len(INFERIDOS)} excluídos por C3 ({len(INFERIDOS)} inferido), {len(PENDENTES)} pendentes com motivo")
