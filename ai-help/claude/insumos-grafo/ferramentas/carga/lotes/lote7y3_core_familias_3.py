"""Lote 7y3 (issue #10, etapa 2, lote 3): recorte Core de CRM Analytics (Wave*) e Experience Cloud.

CRM Analytics: excluído por X2 (licenças por usuário), com fonte por tipo (não há página de lista única).
Experience Cloud: excluído por C3, como Network e CustomSite na etapa 1; C3 não depende de licença (alcance 'nao_se_aplica').
DigitalExperienceBundle fica pendente com motivo (serve a site, marketing e general). Nada é cadastrado no catálogo.
Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-19"
EXTR = "fontes/extracoes/lote7y3-core-familias-3.txt"
A = "https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/"
N = "https://developer.salesforce.com/docs/platform/"
BUSCA = "leitura_resultado_busca"

WAVE = {  # tipo: (id da fonte, url)
    "WaveApplication": ("src:mdapi-waveapplication", A + "meta_waveapplication.htm"),
    "WaveComponent": ("src:mdapi-wavecomponent", A + "meta_wavecomponent.htm"),
    "WaveDashboard": ("src:mdapi-wavedashboard", A + "meta_wavedashboard.htm"),
    "WaveDataflow": ("src:mdapi-wavedataflow", A + "meta_wavedataflow.htm"),
    "WaveDataset": ("src:mdapi-wavedataset", A + "meta_wavedataset.htm"),
    "WaveLens": ("src:mdapi-wavelens", N + "api-metadata/references/meta-types/metadata-wavelens.html"),
    "WaveRecipe": ("src:mdapi-waverecipe", A + "meta_waverecipe.htm"),
    "WaveTemplateBundle": ("src:mdapi-wavetemplatebundle", N + "api-metadata/references/meta-types/metadata-wavetemplatebundle.html"),
    "WaveXmd": ("src:mdapi-wavexmd", A + "meta_wavexmd.htm"),
}
fontes = [C.fonte(sid, f"{t} (Metadata API)", url, f"{t} representa um recurso do aplicativo Analytics (CRM Analytics).", EXTR, DATA,
                  versao="sem versão na URL", metodo=BUSCA) for t, (sid, url) in WAVE.items()]
fontes += [
    C.fonte("src:exp-dev-experiencebundle", "Experience Cloud Developer Guide: ExperienceBundle for Experience Builder Sites",
            N + "communities-dev/guide/communities-dev-migrate-expbundle.html",
            "ExperienceBundle representa em texto os componentes de um site do Experience Builder.", EXTR, DATA, versao="sem versão na URL", metodo=BUSCA),
    C.fonte("src:exp-dev-enhanced-lwr", "Experience Cloud Developer Guide: Avoid Deployment Issues When Moving to Enhanced LWR Sites",
            N + "communities-dev/guide/communities-dev-migrate-enhanced.html",
            "Sites LWR aprimorados usam DigitalExperienceBundle e DigitalExperienceConfig.", EXTR, DATA, versao="sem versão na URL", metodo=BUSCA),
    C.fonte("src:pkg2-componentes", "Components Available in Second-Generation Managed Packages",
            N + "pkg2-dev/guide/packaging-packageable-components.html",
            "CommunityTemplateDefinition e CommunityThemeDefinition definem template e tema de sites do Experience Builder.", EXTR, DATA,
            versao="sem versão na URL", metodo=BUSCA),
    C.fonte("src:mdapi-digitalexperiencebundle", "DigitalExperienceBundle (Metadata API)",
            N + "api-metadata/references/meta-types/metadata-digitalexperiencebundle.html",
            "Workspaces dos tipos site, marketing e general; não é exclusivo de Experience Cloud.", EXTR, DATA, versao="sem versão na URL", metodo=BUSCA),
]
C.registrar_fontes(fontes)

D = {}
for t, (sid, _) in WAVE.items():
    D[t] = {"decisao": "excluido", "criterios": ["C1", "X2"], "familia": "CRM Analytics", "nuvens": ["nuv:platform-core"],
            "motivo": "Representa um recurso do aplicativo CRM Analytics, vendido à parte com licenças por usuário. Depende de licença; "
                      "continua no mapa dentro de CRM Analytics.",
            "evidencias": [{"fonte": sid, "uso": "lista"}, {"fonte": "src:help-crm-analytics-licenses", "uso": "licenca"}],
            "alcance_da_licenca": "familia"}
EXP = "Específico de Experience Cloud (sites do Experience Builder); não é camada compartilhada. Continua no mapa como parte dessa nuvem."
for t, sid in [("ExperienceBundle", "src:exp-dev-experiencebundle"), ("DigitalExperienceConfig", "src:exp-dev-enhanced-lwr"),
               ("CommunityTemplateDefinition", "src:pkg2-componentes"), ("CommunityThemeDefinition", "src:pkg2-componentes")]:
    D[t] = {"decisao": "excluido", "criterios": ["C3"], "familia": "Experience Cloud", "nuvens": ["nuv:experience-cloud"], "motivo": EXP,
            "evidencias": [{"fonte": sid, "uso": "lista"}], "alcance_da_licenca": "nao_se_aplica"}
D["DigitalExperienceBundle"] = {"decisao": "pendente", "criterios": ["C2", "C3"], "familia": "Experience Cloud",
    "nuvens": ["nuv:experience-cloud", "nuv:marketing"],
    "motivo": "Serve a workspaces de site (Experience Cloud), marketing (Marketing Cloud) e general. Por servir a mais de uma nuvem, "
              "poderia entrar no Core pelo C3, mas falta fonte sobre licença fora de Experience Cloud.",
    "evidencias": [{"fonte": "src:mdapi-digitalexperiencebundle", "uso": "lista"}], "alcance_da_licenca": "nao_se_aplica"}

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])
cont = {}
for t, j in D.items():
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == j["familia"], f"{t} já tem outra decisão; não sobrescrever"
    just[t] = {**j, "data": DATA}
    inc.discard(t); exc.discard(t)
    if j["decisao"] == "excluido":
        exc.add(t)
    cont[j["decisao"]] = cont.get(j["decisao"], 0) + 1
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y3: {cont}")
