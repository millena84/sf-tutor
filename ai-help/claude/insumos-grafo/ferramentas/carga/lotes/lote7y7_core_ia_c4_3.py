"""Lote 7y7 (issue #10, etapa 2, lote 7): terceira rodada da família de IA pelo C4.

1 tipo com fonte própria e 7 inferidos pelo nome (marcados com "inferido": true). Estender a marcação de inferência além dos bots é
proposta deste lote, a confirmar pela autora. Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-19"
EXTR = "fontes/extracoes/lote7y7-core-ia-c4-3.txt"
A = "https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/"
BUSCA = "leitura_resultado_busca"
C.registrar_fontes([
    C.fonte("src:mdapi-agentforcefordeveloperssettings", "AgentforceForDevelopersSettings (Metadata API)", A + "meta_agentforcefordeveloperssettings.htm",
            "Configurações de Agentforce for Developers.", EXTR, DATA, versao="sem versão na URL", metodo=BUSCA),
    C.fonte("src:blog-agent-platform-tracing", "Agent Platform Tracing: Debug Agentforce with Trace Trees, SOQL, and Slack",
            "https://developer.salesforce.com/blogs/2026/05/agent-platform-tracing-debug-agentforce-with-trace-trees-soql-and-slack",
            "Agent Platform Tracing grava execuções de ações de Agentforce no Data 360.", EXTR, DATA, versao="sem versão na URL", metodo=BUSCA,
            tipo="oficial_produto"),
    C.fonte("src:mdapi-genaiplannerbundle", "GenAiPlannerBundle (Metadata API)", A + "meta_genaiplannerbundle.htm",
            "Planner de um agente ou template de agente.", EXTR, DATA, versao="sem versão na URL", metodo=BUSCA),
    C.fonte("src:coverage-report-v68-ia", "Metadata Coverage Report v68.0 (tipos de IA)",
            "https://developer.salesforce.com/docs/success/metadata-coverage-report/references/coverage-report/v68.0",
            "Lista os tipos Ai* da API 68.0, sem descrição.", EXTR, DATA, versao="68.0", metodo=BUSCA),
])
TRES = ["nuv:platform-core", "nuv:sales-cloud", "nuv:service-cloud"]
ORIENT = "Orientação da autora (2026-11-19): é diretamente de Agentforce, seja o agente de Sales, Service ou Core; liga às três frentes."
COND = "Agentforce habilitado na org (exige Einstein Generative AI ligado; licenças variam por tipo de agente)."
LIC = [{"fonte": "src:help-enable-agentforce", "uso": "licenca"}, {"fonte": "src:help-agent-setup", "uso": "licenca"}]
COB = {"fonte": "src:coverage-report-v68-ia", "uso": "lista"}
INF = "Associação ao Agentforce inferida pelo nome do tipo: a fonte lida só lista o nome, sem descrição. Proposta a confirmar pela autora."

DEC = {
    "AgentforceForDevelopersSettings": ("Configurações de Agentforce for Developers.", "Agentforce for Developers habilitado na org.",
                                        [{"fonte": "src:mdapi-agentforcefordeveloperssettings", "uso": "lista"}] + LIC, "proprio_tipo", False),
    "AgentforcePlatformTracingSettings": ("Configurações de rastreamento das execuções de ações de Agentforce (Agent Platform Tracing), "
                                          "que gravam dados no Data 360.", COND + " Exige também Data 360 provisionado.",
                                          [{"fonte": "src:blog-agent-platform-tracing", "uso": "lista"}] + LIC, "familia", True),
    "AiSurfaceInput": ("Parte de uma conexão personalizada com agentes (AiSurface), pelo nome.", COND, [COB] + LIC, "familia", True),
    "AiSurfaceInstruction": ("Instrução de uma conexão personalizada com agentes (AiSurface), pelo nome.", COND, [COB] + LIC, "familia", True),
    "AiResponseFormatIstr": ("Instrução de um formato de resposta de agente (AiResponseFormat), pelo nome.", COND, [COB] + LIC, "familia", True),
    "AiAgentDefinitionPlanner": ("Planner de um agente descrito por AiAgentDefinition (API 68), pelo nome.", COND,
                                 [COB, {"fonte": "src:mdapi-genaiplannerbundle", "uso": "lista"}] + LIC, "familia", True),
    "AiPlannerVoiceDef": ("Definição de voz do planner de um agente, pelo nome.", COND, [COB] + LIC, "familia", True),
    "AiPlannerVoiceAvatarDef": ("Definição de avatar de voz do planner de um agente, pelo nome.", COND, [COB] + LIC, "familia", True),
}

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc, cond = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"]), set(cc.get("condicionais", []))
for t, (o_que, condicao, ev, alcance, inferido) in DEC.items():
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == "Agentforce", f"{t}: já tem outra decisão"
    j = {"decisao": "condicional", "criterios": ["C4"], "condicao": condicao, "orientacao_autora": ORIENT, "familia": "Agentforce",
         "nuvens": TRES, "evidencias": ev, "alcance_da_licenca": alcance, "data": DATA,
         "motivo": o_que + " Pelo C4, fica ligado ao Core e às nuvens que o usam, com a condição registrada."}
    if inferido:
        j["inferido"], j["nota_inferencia"] = True, INF
    just[t] = j
    inc.discard(t); exc.discard(t); cond.add(t)
cc["incluidos"], cc["excluidos"], cc["condicionais"] = sorted(inc), sorted(exc), sorted(cond)
cc["justificativas"] = dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y7: {len(DEC)} condicionais ({sum(1 for v in DEC.values() if v[4])} inferidos)")
