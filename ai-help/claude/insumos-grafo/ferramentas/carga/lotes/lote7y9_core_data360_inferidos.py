"""Lote 7y9 (issue #10, etapa 2, lote 9): Data 360 inferidos, por orientação da autora (2026-11-20).

Os 20 tipos de dados que ficaram sem decisão no lote 8 são associados ao Data 360 (fora do Core pelo C3), com "inferido": true,
porque nenhuma descrição oficial lida os liga ao Data 360. Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import catalogo as C   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-20"
EXTR = "fontes/extracoes/lote7y9-core-data360-inferidos.txt"
C.registrar_fontes([
    C.fonte("src:data360-query-metadata-api", "Data 360 Query Guide: Retrieve Metadata",
            "https://developer.salesforce.com/docs/data/data-cloud-query-guide/references/data-cloud-query-api-reference/c360a-api-metadata-api.html",
            "A API de metadados do Data 360 aceita DataLakeObject, DataModelObject e CalculatedInsight.", EXTR, DATA, versao="sem versão na URL",
            metodo="leitura_resultado_busca"),
    C.fonte("src:coverage-report-data360", "Metadata Coverage Report (tipos de dados)", "https://developer.salesforce.com/docs/metadata-coverage",
            "Lista os tipos de dados sem descrição.", EXTR, DATA, versao="sem versão na URL", metodo="leitura_resultado_busca"),
])
TIPOS = ["CalculatedInsight", "DataAction", "DataActionTarget", "DataGraph", "DataLakeObject", "DataModelObject", "DataObjectSearchIndexConf",
         "DataSource", "DataSourceObject", "DataSourceTenant", "DataStreamBundle", "DataTransform", "ExternalDataConnector",
         "ExternalDataSrcDescriptor", "IdentityResolution", "InternalDataConnector", "MktDataConnectionParam", "MktDataConnectionSrcParam",
         "MktDataTranObject", "DataConnectorIngestApi"]
COM_API = {"CalculatedInsight", "DataLakeObject", "DataModelObject"}
ORIENT = ("Orientação da autora (2026-11-20): associar ao Data Cloud (Data 360) com ressalva, porque a associação não foi confirmada "
          "por fonte.")
INF = ("Associação ao Data 360 inferida por orientação da autora e pelo nome do tipo; a fonte lida só lista o nome, sem descrição. "
       "Pendente de confirmação.")

inv = {i["nome"] for i in json.load(open(os.path.join(RAIZ, "inventarios", "metadata-types-v68.json"), encoding="utf-8"))["itens"]}
esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
cc = esc["classificacao_core_por_item"]
just, inc, exc = cc["justificativas"], set(cc["incluidos"]), set(cc["excluidos"])
for t in TIPOS:
    assert t in inv, f"{t} não consta do inventário v68"
    atual = just.get(t)
    assert atual is None or atual.get("familia") == "Data 360", f"{t}: já tem outra decisão"
    ev = [{"fonte": "src:coverage-report-data360", "uso": "lista"}]
    if t in COM_API:
        ev.append({"fonte": "src:data360-query-metadata-api", "uso": "lista"})
    just[t] = {"decisao": "excluido", "criterios": ["C3"], "familia": "Data 360", "nuvens": ["nuv:data-360"],
               "motivo": "Associado ao Data 360 (fora do Core por ser específico dessa nuvem), com ressalva: associação inferida.",
               "evidencias": ev, "alcance_da_licenca": "nao_se_aplica", "inferido": True, "nota_inferencia": INF,
               "orientacao_autora": ORIENT, "data": DATA}
    inc.discard(t); exc.add(t)
cc["incluidos"], cc["excluidos"], cc["justificativas"] = sorted(inc), sorted(exc), dict(sorted(just.items()))
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print(f"lote 7y9: {len(TIPOS)} tipos associados ao Data 360 como inferidos")
