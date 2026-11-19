"""Lote 7y5 (issue #10, etapa 2, lote 5): família de IA com o critério C4 ("condicional").

Seis tipos do núcleo de agentes Agentforce ficam "condicional": ligados ao Core e às nuvens que os usam, com a condição registrada.
GenAiFunction e GenAiPlugin estavam pendentes desde a etapa 1; o C4 (decisão da autora em 2026-11-19) resolve a dúvida de licença.
Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-19"
EXTR = "fontes/extracoes/lote7y5-core-ia-c4.txt"
D = "https://developer.salesforce.com/docs/ai/agentforce/"
H = "https://help.salesforce.com/s/articleView?"
C.registrar_fontes([
    C.fonte("src:agentforce-metadata-types", "Agentforce Developer Guide: Metadata Types", D + "references/agents-metadata-tooling/agents-metadata.html",
            "Lista dos metadata types de agentes Agentforce.", EXTR, DATA, versao="v67 e anteriores (título da página)"),
    C.fonte("src:agentforce-testing-metadata", "Agentforce Developer Guide: Metadata API Reference for Testing API",
            D + "references/testing-api/testing-metadata-reference.html",
            "AiEvaluationDefinition só existe com Agentforce habilitado.", EXTR, DATA, versao="sem versão na URL"),
    C.fonte("src:help-enable-agentforce", "Enable Agentforce", H + "id=ai.copilot_setup_enable.htm&language=en_US&type=5",
            "Habilitar o Agentforce exige ligar antes o Einstein Generative AI.", EXTR, DATA, versao="sem versão na URL",
            metodo="leitura_resultado_busca"),
    C.fonte("src:help-agent-setup", "Set Up Your Agent", H + "language=en_US&id=ai.agent_parent_setup.htm&type=5",
            "Licenças add-on variam conforme o tipo de agente.", EXTR, DATA, versao="sem versão na URL", metodo="leitura_resultado_busca"),
    C.fonte("src:help-prompt-builder-edicoes", "Prompt Builder", H + "language=en_US&id=ai.prompt_builder_about.htm&type=5",
            "Prompt templates alimentam IA generativa e agentes; exige add-on Einstein ou Agentforce, ou Agentforce Foundations.", EXTR, DATA,
            versao="sem versão na URL", metodo="leitura_resultado_busca"),
    C.fonte("src:help-prompt-templates-standard", "Standard Prompt Templates",
            H + "id=ai.prompt_builder_standard_prompt_templates.htm&language=en_US&type=5",
            "Prompt templates são pilot, custom ou standard.", EXTR, DATA, versao="sem versão na URL", metodo="leitura_resultado_busca"),
    C.fonte("src:help-prompt-packaging", "Packaging Considerations for Prompt Templates",
            H + "id=ai.prompt_builder_considerations_packaging.htm&language=en_US",
            "Einstein Generative AI precisa estar ativo para instalar prompt templates.", EXTR, DATA, versao="sem versão na URL",
            metodo="leitura_resultado_busca"),
])

TRES = ["nuv:platform-core", "nuv:sales-cloud", "nuv:service-cloud"]
ORIENT = ("Orientação da autora (2026-11-19): é diretamente de Agentforce, seja o agente de Sales, Service ou Core; "
          "liga às três frentes.")
ORIENT_PROMPT = ("Orientação da autora (2026-11-19): prompt templates seguem a linha de Agentforce; Sales e Service trazem prompts "
                 "standard, e o Core tende a usar prompts customizados.")
COND_PROMPT = ("IA generativa (Einstein Generative AI) habilitada, com add-on Einstein for Platform, Einstein ou Agentforce for Sales "
               "ou Service, ou Agentforce Foundations.")
EV_PROMPT = [{"fonte": "src:help-prompt-builder-edicoes", "uso": "lista"}, {"fonte": "src:help-prompt-builder-edicoes", "uso": "licenca"},
             {"fonte": "src:help-prompt-templates-standard", "uso": "lista"}, {"fonte": "src:help-prompt-packaging", "uso": "licenca"}]

COND = "Agentforce habilitado na org (exige Einstein Generative AI ligado; licenças variam por tipo de agente)."
EV_FAM = [{"fonte": "src:agentforce-metadata-types", "uso": "lista"}, {"fonte": "src:help-enable-agentforce", "uso": "licenca"},
          {"fonte": "src:help-agent-setup", "uso": "licenca"}]
TIPOS = {
    "AiAuthoringBundle": ("Contêiner do Agent Script e dos metadados de um agente Agentforce.", COND, TRES, EV_FAM, "familia"),
    "GenAiFunction": ("Ação que pode ser adicionada a agentes Agentforce.", COND, TRES, EV_FAM, "familia"),
    "GenAiPlugin": ("Subagente que agrupa ações de agentes Agentforce.", COND, TRES, EV_FAM, "familia"),
    "AiEvaluationDefinition": ("Define testes de agentes Agentforce; a página do tipo diz que ele só existe com Agentforce habilitado.", COND,
                               TRES,
                               [{"fonte": "src:agentforce-testing-metadata", "uso": "lista"}, {"fonte": "src:agentforce-testing-metadata", "uso": "licenca"}],
                               "proprio_tipo"),
    "Bot": ("Registro principal de um agente Agentforce ou de um Einstein Bot.",
            "Agentforce habilitado na org, ou Einstein Bots (Service Cloud).", TRES, EV_FAM, "familia"),
    "BotVersion": ("Configuração de uma versão de agente Agentforce ou de Einstein Bot.",
                   "Agentforce habilitado na org, ou Einstein Bots (Service Cloud).", TRES, EV_FAM, "familia"),
    "GenAiPromptTemplate": ("Prompt template: instrução reutilizável que alimenta recursos de IA generativa e agentes Agentforce.",
                            COND_PROMPT, TRES, EV_PROMPT, "familia"),
    "EinsteinGptSettings": ("Configurações de IA generativa da org, inclusive o controle de implantação de prompt templates.",
                            COND_PROMPT, TRES, EV_PROMPT, "familia"),
}
PROMPT = {"GenAiPromptTemplate", "EinsteinGptSettings"}
ETAPA1 = {"GenAiFunction", "GenAiPlugin", "GenAiPromptTemplate", "EinsteinGptSettings"}  # pendentes da etapa 1 que este lote resolve

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc, cond = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"]), set(cc.get("condicionais", []))
for t, (o_que, condicao, nuvens, ev, alcance) in TIPOS.items():
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == "Agentforce" or (t in ETAPA1 and atual["decisao"] == "pendente"), f"{t}: decisão inesperada"
    just[t] = {"decisao": "condicional", "criterios": ["C4"], "condicao": condicao,
               "motivo": o_que + " Pelo C4, fica ligado ao Core e às nuvens que o usam, com a condição registrada.",
               "familia": "Agentforce", "nuvens": nuvens, "evidencias": ev, "alcance_da_licenca": alcance, "data": DATA,
               "orientacao_autora": ORIENT_PROMPT if t in PROMPT else ORIENT}
    if t in ETAPA1:
        just[t]["historico"] = "Pendente na etapa 1 (licença não esclarecida); resolvido pelo C4 em 2026-11-19."
    inc.discard(t); exc.discard(t); cond.add(t)
cc["incluidos"], cc["excluidos"], cc["condicionais"] = sorted(inc), sorted(exc), sorted(cond)
cc["justificativas"] = dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y5: {len(TIPOS)} tipos condicionais (C4)")
