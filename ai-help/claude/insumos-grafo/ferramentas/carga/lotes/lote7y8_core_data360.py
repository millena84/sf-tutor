"""Lote 7y8 (issue #10, etapa 2, lote 8): família Data 360, excluída do Core pelo C3 (tipo específico de uma nuvem que é nó próprio do mapa).

Continua no mapa dentro de Data 360. Nada é cadastrado no catálogo. Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-20"
EXTR = "fontes/extracoes/lote7y8-core-data360.txt"
BUSCA = "leitura_resultado_busca"
SV = "sem versão na URL"
C.registrar_fontes([
    C.fonte("src:pkg2-componentes-data360", "Components Available in Second-Generation Managed Packages (componentes de Data 360)",
            "https://developer.salesforce.com/docs/platform/pkg2-dev/guide/packaging-packageable-components.html",
            "Descrição de 16 componentes de Data 360 (data kits, conectores, esquema).", EXTR, DATA, versao=SV),
    C.fonte("src:mdapi-mktcalcinsightobjectdef", "MktCalcInsightObjectDef (Metadata API)",
            "https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_mktcalcinsightobjectdef.htm",
            "Definição de Calculated Insight.", EXTR, DATA, versao=SV, metodo=BUSCA),
    C.fonte("src:data360-s3-datastream", "Data 360: Create an Amazon S3 Data Stream",
            "https://developer.salesforce.com/docs/data/data-cloud-int/references/data-cloud-s3-ref/c360-a-api-create-an-amazon-s3-data-stream-using-salesforce-cdp-apis.html",
            "Data stream do Amazon S3 no Data 360, com DataStreamDefinition e DataConnectorS3.", EXTR, DATA, versao=SV, metodo=BUSCA),
    C.fonte("src:blog-data-cloud-visual", "A Visual Guide to Salesforce Data Cloud Capabilities",
            "https://developer.salesforce.com/blogs/2024/10/a-visual-guide-to-salesforce-data-cloud-capabilities",
            "Activation target guarda autenticação de uma plataforma de ativação do Data Cloud.", EXTR, DATA, versao=SV, metodo=BUSCA,
            tipo="oficial_produto"),
])
PKG = "src:pkg2-componentes-data360"
TIPOS = {t: PKG for t in ["ActivationPlatform", "DataCalcInsightTemplate", "DataCleanRoomProvider", "DataConnector", "DataKitObjectDependency",
                          "DataKitObjectTemplate", "DataObjectBuildOrgTemplate", "DataPackageKitDefinition", "DataPackageKitObject",
                          "DataSourceBundleDefinition", "DataSrcDataModelFieldMap", "DataStreamTemplate", "ExternalDataTranField",
                          "ExternalDataTranObject", "ExtDataTranObjectTemplate", "MktDataConnection"]}
TIPOS.update({"MktCalcInsightObjectDef": "src:mdapi-mktcalcinsightobjectdef", "DataStreamDefinition": "src:data360-s3-datastream",
              "DataConnectorS3": "src:data360-s3-datastream", "ActivationTarget": "src:blog-data-cloud-visual"})
MOTIVO = "Específico de Data 360 (data streams, data kits, conectores, esquema ou ativação); não é camada compartilhada. Continua no mapa dentro de Data 360."

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])
for t, src in TIPOS.items():
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == "Data 360", f"{t}: já tem outra decisão"
    just[t] = {"decisao": "excluido", "criterios": ["C3"], "motivo": MOTIVO, "familia": "Data 360", "nuvens": ["nuv:data-360"],
               "evidencias": [{"fonte": src, "uso": "lista"}], "alcance_da_licenca": "nao_se_aplica", "data": DATA}
    inc.discard(t); exc.add(t)
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y8: {len(TIPOS)} tipos de Data 360 excluídos por C3")
