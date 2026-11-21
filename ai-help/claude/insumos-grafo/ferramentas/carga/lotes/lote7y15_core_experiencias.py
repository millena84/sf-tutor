"""Lote 7y15 (issue #10, etapa 2, lote 15): Experiências externas (Experience Cloud).

7 tipos excluídos do Core por C3, como Network e ExperienceBundle. Nada é cadastrado no catálogo. Reexecutável.
Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-21"
EXTR = "fontes/extracoes/lote7y15-core-experiencias.txt"
BUSCA = "leitura_resultado_busca"
B = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
FAMILIA = "Experience Cloud"


def f(id_, titulo, url, pert, versao="68.0"):
    return C.fonte(id_, titulo, url, pert, EXTR, DATA, versao=versao, metodo=BUSCA)


C.registrar_fontes([
    f("src:exp-dev-deploy-256", "Experience Cloud Developer Guide 256.0: Deploy Your Experience Cloud Site with the Metadata API",
      "https://developer.salesforce.com/docs/atlas.en-us.256.0.communities_dev.meta/communities_dev/networks_migrating_from_sandbox.htm",
      "Tipos que definem um site Experience Cloud conforme o framework (inclui SiteDotCom).", versao="256.0"),
    f("src:mdapi-managedtopics", "ManagedTopics (Metadata API, página atual)",
      "https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_managedtopics.htm",
      "Tópicos de navegação e em destaque de um site Experience Cloud.", versao="sem versão na URL"),
    f("src:mdapi-moderationrule-264", "ModerationRule (Metadata API 264.0)", B + "meta_moderationrule.htm", "Regras de moderação de sites Experience Cloud."),
    f("src:mdapi-keywordlist-264", "KeywordList (Metadata API 264.0)", B + "meta_keywordlist.htm", "Listas de palavras da moderação de sites Experience Cloud."),
    f("src:mdapi-experiencebundlesettings-264", "ExperienceBundleSettings (Metadata API 264.0)", B + "meta_experiencebundlesettings.htm",
      "Habilita ExperienceBundle para sites Aura do Experience Cloud."),
    f("src:mdapi-experiencepropertytypebundle-264", "ExperiencePropertyTypeBundle (Metadata API 264.0)", B + "meta_experiencepropertytypebundle.htm",
      "Tipos de propriedade para Lightning web components em sites LWR."),
    f("src:mdapi-cmsconnectsource-264", "CMSConnectSource (Metadata API 264.0)", B + "meta_cmsconnectsource.htm",
      "Conexões com CMS externos que alimentam sites do Experience Builder."),
])

MOT = "Específico de Experience Cloud (sites); não é camada compartilhada. Continua no mapa como parte dessa nuvem."
EXCLUIDOS = {
    "SiteDotCom": "src:exp-dev-deploy-256",
    "ManagedTopics": "src:mdapi-managedtopics",
    "ModerationRule": "src:mdapi-moderationrule-264",
    "KeywordList": "src:mdapi-keywordlist-264",
    "ExperienceBundleSettings": "src:mdapi-experiencebundlesettings-264",
    "ExperiencePropertyTypeBundle": "src:mdapi-experiencepropertytypebundle-264",
    "CMSConnectSource": "src:mdapi-cmsconnectsource-264",
}

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])
for t, src in EXCLUIDOS.items():
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == FAMILIA, f"{t}: já tem outra decisão"
    just[t] = {"decisao": "excluido", "criterios": ["C3"], "familia": FAMILIA, "nuvens": ["nuv:experience-cloud"], "motivo": MOT,
               "evidencias": [{"fonte": src, "uso": "lista"}], "alcance_da_licenca": "nao_se_aplica", "data": DATA}
    exc.add(t); inc.discard(t)
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y15: {len(EXCLUIDOS)} excluídos por C3 (Experience Cloud)")
