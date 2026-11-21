"""Lote 8i (Fase 2, fechamento): FieldServiceSettings (14) e CommunitiesSettings (3).

Nenhum dos 17 nomes tem descrição oficial na página 264.0 nem nas notas da release (busca): ficam com explicacao = "nao_encontrada" e o
texto padrão (versão e release de config/versoes.json). Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv               # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-20"
EXTR = "fontes/extracoes/lote8i-fase2-fechamento.txt"
G = "https://developer.salesforce.com/docs/get_document_content/api_meta/"
C.registrar_fontes([
    C.fonte("src:mdapi-fieldservicesettings-264", "FieldServiceSettings (Metadata API 264.0)", G + "meta_fieldservicesettings.htm/en-us/264.0",
            "Página lida por inteiro; 14 nomes do schema v68 não constam dela.", EXTR, DATA),
    C.fonte("src:mdapi-communitiessettings-264", "CommunitiesSettings (Metadata API 264.0)", G + "meta_communitiessettings.htm/en-us/264.0",
            "Página lida por inteiro; 3 nomes do schema v68 não constam dela.", EXTR, DATA),
])
V = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "config", "versoes.json"),
                   encoding="utf-8"))["plataforma_core"]
NAO = (f"Não encontrada descrição oficial na última versão da documentação ({V['numero_interno_documentacao']}, API {V['api_version']}); "
       f"verificado também nas notas da release {V['release']} (por busca).")
NOTA = "O nome vem do schema da v68, mas não está na tabela de campos da página 264.0."

texto = open(EXTR, encoding="utf-8").read()
cont = 0
for arq, src in [("metadata-types/FieldServiceSettings.json", "src:mdapi-fieldservicesettings-264"),
                 ("metadata-types/CommunitiesSettings.json", "src:mdapi-communitiessettings-264")]:
    bloco = texto.split(f"[{src}]", 1)[1].split("\n[", 1)[0]
    d = ld(arq)
    for i in d["propriedades"]:
        if i.get("explicacao") != "pendente":
            continue
        assert re.search(r"(?<![A-Za-z])" + re.escape(i["nome"]) + r"(?![A-Za-z0-9])", bloco), i["nome"]
        i["o_que_e"], i["explicacao"] = NAO, "nao_encontrada"
        if src not in [e["fonte"] for e in i["evidencias"]]:
            i["evidencias"].append({"fonte": src})
        i["notas"] = [x for x in i.get("notas", []) if x != NOTA] + [NOTA]
        cont += 1
    if d.get("cobertura", {}).get("explicativa") is not None:
        d["cobertura"]["explicativa"]["presente"] = sum(1 for x in d["propriedades"] if x.get("explicacao") == "explicada")
    sv(arq, d)
print(f"lote 8i: {cont} nao_encontrada")
