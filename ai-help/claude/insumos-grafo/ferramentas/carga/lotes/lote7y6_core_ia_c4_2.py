"""Lote 7y6 (issue #10, etapa 2, lote 6): segunda rodada da família de IA pelo C4.

Agentforce liga a Core, Sales e Service (orientação da autora em 2026-11-19). Ver a nota de extração para fontes e limites.
Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-19"
EXTR = "fontes/extracoes/lote7y6-core-ia-c4-2.txt"
D = "https://developer.salesforce.com/docs/"
BUSCA = "leitura_resultado_busca"
SV = "sem versão na URL"
C.registrar_fontes([
    C.fonte("src:agentforce-move-agent", "Agentforce Developer Guide: Move an Agent to a New Org", D + "ai/agentforce/guide/agent-dx-deploy-metadata.html",
            "Na API 68, agentes são recuperados por AiAgentDefinitionVersion.", EXTR, DATA, versao="API 68.0", metodo=BUSCA),
    C.fonte("src:blog-winter27-dev", "The Salesforce Developer's Guide to the Winter '27 Release",
            "https://developer.salesforce.com/blogs/2026/10/developers-guide-to-the-winter-27-release",
            "Desde a API 68.0, um agente é descrito por AiAgentDefinition e AiAgentDefinitionVersion.", EXTR, DATA, versao="Winter '27",
            metodo=BUSCA, tipo="oficial_produto"),
    C.fonte("src:agentforce-custom-connections", "Agentforce Developer Guide: Custom Connections", D + "ai/agentforce/guide/custom-connections.html",
            "AiSurface e AiResponseFormat ligam um cliente externo a um agente Agentforce.", EXTR, DATA, versao=SV, metodo=BUSCA),
    C.fonte("src:mdapi-genaiprompttemplateactv", "GenAiPromptTemplateActv (Metadata API)",
            D + "atlas.en-us.api_meta.meta/api_meta/meta_genaiprompttemplateactv.htm",
            "Status de ativação de um prompt template standard.", EXTR, DATA, versao=SV, metodo=BUSCA),
    C.fonte("src:agentforce-agent-variables", "Agentforce Developer Guide: Send Agent Variables with the Agent API",
            D + "ai/agentforce/guide/agent-api-variables.html",
            "Variáveis de agente ficam em BotVersion, Bot e BotTemplate.", EXTR, DATA, versao=SV, metodo=BUSCA),
    C.fonte("src:mdapi-bot-einstein", "Bot, BotBlock, BotSettings e BotTemplate (Metadata API)",
            D + "atlas.en-us.api_meta.meta/api_meta/meta_botsettings.htm",
            "Tipos descritos como configuração de Einstein Bots.", EXTR, DATA, versao=SV, metodo=BUSCA),
])

TRES = ["nuv:platform-core", "nuv:sales-cloud", "nuv:service-cloud"]
ORIENT = "Orientação da autora (2026-11-19): é diretamente de Agentforce, seja o agente de Sales, Service ou Core; liga às três frentes."
ORIENT_PROMPT = ("Orientação da autora (2026-11-19): prompt templates seguem a linha de Agentforce; Sales e Service trazem prompts standard, "
                 "e o Core tende a usar prompts customizados.")
COND = "Agentforce habilitado na org (exige Einstein Generative AI ligado; licenças variam por tipo de agente)."
COND_BOT = "Agentforce habilitado na org, ou Einstein Bots (Service Cloud)."
COND_PROMPT = ("IA generativa (Einstein Generative AI) habilitada, com add-on Einstein for Platform, Einstein ou Agentforce for Sales "
               "ou Service, ou Agentforce Foundations.")
LIC = [{"fonte": "src:help-enable-agentforce", "uso": "licenca"}, {"fonte": "src:help-agent-setup", "uso": "licenca"}]
LIC_P = [{"fonte": "src:help-prompt-builder-edicoes", "uso": "licenca"}]

DEC = {
    "AiAgentDefinition": ("condicional", "Descreve um agente Agentforce a partir da API 68.0.", COND, ORIENT,
                          [{"fonte": "src:blog-winter27-dev", "uso": "lista"}] + LIC),
    "AiAgentDefinitionVersion": ("condicional", "Versão de um agente Agentforce; ao recuperá-la, vêm as versões certas de flows, Apex e prompt "
                                 "templates usados pelo agente.", COND, ORIENT,
                                 [{"fonte": "src:agentforce-move-agent", "uso": "lista"}, {"fonte": "src:blog-winter27-dev", "uso": "lista"}] + LIC),
    "AiSurface": ("condicional", "Conexão personalizada que liga um cliente web externo a um agente Agentforce.", COND, ORIENT,
                  [{"fonte": "src:agentforce-custom-connections", "uso": "lista"}] + LIC),
    "AiResponseFormat": ("condicional", "Formato de resposta estruturado (esquema JSON) que um agente Agentforce usa numa conexão personalizada.",
                         COND, ORIENT, [{"fonte": "src:agentforce-custom-connections", "uso": "lista"}] + LIC),
    "GenAiPromptTemplateActv": ("condicional", "Status de ativação de um prompt template standard, fornecido pela Salesforce.", COND_PROMPT,
                                ORIENT_PROMPT, [{"fonte": "src:mdapi-genaiprompttemplateactv", "uso": "lista"}] + LIC_P),
    "BotTemplate": ("condicional", "Template de agente ou de Einstein Bot; também guarda variáveis de agentes Agentforce.", COND_BOT, ORIENT,
                    [{"fonte": "src:agentforce-agent-variables", "uso": "lista"}, {"fonte": "src:mdapi-bot-einstein", "uso": "lista"}] + LIC),
}
PEND = "As fontes só falam de Einstein Bots; falta fonte que diga se o tipo serve também ao Agentforce e a que nuvem os bots pertencem."
for t in ("BotBlock", "BotBlockVersion", "BotSettings"):
    DEC[t] = ("pendente", PEND, None, None, [{"fonte": "src:mdapi-bot-einstein", "uso": "lista"}])

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc, cond = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"]), set(cc.get("condicionais", []))
cont = {}
for t, (dec, motivo, condicao, orient, ev) in DEC.items():
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == "Agentforce", f"{t}: já tem outra decisão"
    j = {"decisao": dec, "familia": "Agentforce", "evidencias": ev, "alcance_da_licenca": "familia", "data": DATA}
    if dec == "condicional":
        j.update({"criterios": ["C4"], "condicao": condicao, "orientacao_autora": orient, "nuvens": TRES,
                  "motivo": motivo + " Pelo C4, fica ligado ao Core e às nuvens que o usam, com a condição registrada."})
        cond.add(t)
    else:
        j.update({"criterios": ["C2", "C4"], "motivo": motivo, "nuvens": ["nuv:service-cloud"]})
        cond.discard(t)
        j["alcance_da_licenca"] = "nao_se_aplica"
    just[t] = j
    inc.discard(t); exc.discard(t)
    cont[dec] = cont.get(dec, 0) + 1
cc["incluidos"], cc["excluidos"], cc["condicionais"] = sorted(inc), sorted(exc), sorted(cond)
cc["justificativas"] = dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y6: {cont}")
