#!/usr/bin/env python3
"""Exporta uma visão do catálogo de acesso sem alterar a fonte da verdade."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESTINO = Path(__file__).resolve().parent

# Objetos são representações relacionadas, não necessariamente equivalências
# campo a campo nem tabelas físicas do banco de dados da Salesforce.
TEMAS = {
    "User": (None, ["User"], "User é um objeto de dados, não um metadata type XML."),
    "Profile": ("Profile", ["Profile", "User"], None),
    "PermissionSet": ("PermissionSet", ["PermissionSet", "PermissionSetAssignment"], None),
    "PermissionSetGroup": (
        "PermissionSetGroup",
        ["PermissionSetGroup", "PermissionSetAssignment"],
        None,
    ),
    "Role": ("Role", ["UserRole"], None),
    "Groups": ("Group", ["Group", "GroupMember"], None),
    "Queue": (
        "Queue",
        ["Group", "GroupMember", "QueueSobject"],
        "Filas são representadas por registros de Group; nem todo Group é uma fila.",
    ),
    "OWD": (
        "CustomObject",
        ["EntityDefinition"],
        "OWD é uma configuração de compartilhamento, não um metadata type independente. "
        "Em CustomObject, sharingModel e externalSharingModel representam os padrões "
        "de compartilhamento interno e externo, respectivamente. EntityDefinition "
        "é incluído como objeto relacionado à definição do objeto, não como "
        "equivalência comprovada campo a campo de OWD.",
    ),
}


def ler(caminho):
    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def registrar_fontes(valor, ids):
    if isinstance(valor, dict):
        if isinstance(valor.get("fonte"), str):
            ids.add(valor["fonte"])
        for item in valor.values():
            registrar_fontes(item, ids)
    elif isinstance(valor, list):
        for item in valor:
            registrar_fontes(item, ids)


def gerar():
    registro = ler(ROOT / "fontes/snapshots/sdr-13.12.0/metadataRegistry.json")
    fontes = {fonte["id"]: fonte for fonte in ler(ROOT / "fontes/registro.json")["fontes"]}
    ids_fontes = set()
    versao = ler(ROOT / "config/versoes.json")["plataforma_core"]

    for tema, (nome_mdt, nomes_objetos, nota) in TEMAS.items():
        metadata = None
        estruturas = []
        if nome_mdt:
            caminho = ROOT / "catalogo/metadata-types" / f"{nome_mdt}.json"
            if caminho.exists():
                metadata = ler(caminho)
                for referencia in metadata["estruturas"]:
                    nome = referencia.removeprefix("mdx:")
                    estruturas.append(ler(ROOT / "catalogo/estruturas" / f"{nome}.json"))
            else:
                tipo = registro["types"][nome_mdt.lower()]
                metadata = {
                    "nome": tipo["name"],
                    "estado": "parcial",
                    "arquivos": {
                        "source_format": {
                            "pasta": tipo["directoryName"] + "/",
                            "arquivo": f"<Nome>.{tipo['suffix']}-meta.xml",
                        },
                        "metadata_api_format": {
                            "pasta": tipo["directoryName"] + "/",
                            "arquivo": f"<Nome>.{tipo['suffix']}",
                        },
                    },
                    "propriedades": None,
                    "nota": "As propriedades XML não foram levantadas no catálogo.",
                    "evidencias": [{"fonte": "src:sdr-registry"}],
                }

        objetos = []
        for nome in nomes_objetos:
            caminho = ROOT / "catalogo/objetos-api" / f"{nome}.json"
            objetos.append(
                ler(caminho) if caminho.exists() else {
                    "nome": nome,
                    "estado": "desconhecido",
                    "campos": None,
                    "nota": "Objeto relacionado ainda não levantado no catálogo; "
                            "campos, acesso e correspondência precisam de verificação.",
                }
            )

        exportacao = {
            "tema": tema,
            "versao_api_referencia": versao["api_version"],
            "data_referencia": ler(ROOT / "config/versoes.json")["data_referencia"],
            "estado": "parcial",
            "nota": nota,
            "limites": [
                "Esta exportação reproduz o catálogo existente e não demonstra "
                "cobertura completa de propriedades ou campos.",
                "A disponibilidade e os campos de uma org dependem da versão, "
                "licenças, recursos habilitados e permissões.",
                "Objetos de API não são tabelas físicas; nenhuma correspondência "
                "XML/campo é presumida pelo nome.",
            ],
            "metadata_type": metadata,
            "estruturas_xml": estruturas,
            "objetos_api_relacionados": objetos,
        }
        registrar_fontes(exportacao, ids_fontes)
        gravar(DESTINO / f"{tema}.json", exportacao)

    ausentes = ids_fontes - fontes.keys()
    if ausentes:
        raise ValueError(f"Fontes não cadastradas: {sorted(ausentes)}")
    gravar(DESTINO / "fontes.json", {
        "nota": "Caminhos de extração relativos a ai-help/claude/insumos-grafo/.",
        "fontes": [fontes[id_] for id_ in sorted(ids_fontes)],
    })


def gravar(caminho, dados):
    caminho.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    gerar()
