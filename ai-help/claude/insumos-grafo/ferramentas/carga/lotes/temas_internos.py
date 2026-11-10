"""Issue #34, item 3 (limpeza do dado genérico dos temas internos), um tema principal por vez.

Para cada tema interno listado em TEMAS:
- "descricao": troca a frase genérica da carga inicial por uma descrição curta escrita pelo projeto (resumo do tema, sem
  fato técnico novo além dos já catalogados);
- "referencias_oficiais": áreas da documentação oficial já registradas em fontes/registro.json; cada nota começa com
  "Cobre o tema", "Cobre parte do tema" ou "Mais ampla que o tema" (o validador exige);
- "nota_estado": mesma redação dos temas principais. O "estado" continua "desconhecido": o recorte é do projeto e a
  conferência é parcial (o site passa a mostrar "Parcialmente conferido").

Não registra fontes novas: só cita fontes que já existem (o script aborta se alguma faltar).
Reexecutável. Uso: python3 ferramentas/carga/lotes/temas_internos.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from carga.base import ROOT, save, ev  # noqa: E402

DATA = "2026-11-10"
NOTA_ESTADO = ("Tema criado pelo projeto (00-especificacao-grafo.md), não é nomenclatura oficial da Salesforce. Cruzado em "
               + DATA + " com áreas da documentação oficial listadas nas referências; a correspondência é parcial e o recorte continua sendo do projeto.")

# id -> (descricao, [referências])
TEMAS = {
    # ------------------------------------------------------------------ Integração, APIs e eventos
    "sub:apis-de-dados-e-metadados": (
        "As APIs que a plataforma oferece para outros sistemas lerem e gravarem na org: REST e SOAP para registros, Bulk API para "
        "grandes volumes, Metadata API para configuração e Tooling API para ferramentas de desenvolvimento.",
        [ev("src:rest-intro", "Cobre parte do tema: REST API.", "Introduction to REST API"),
         ev("src:soap-intro", "Cobre parte do tema: SOAP API e os WSDLs Enterprise e Partner.", "Introduction to SOAP API"),
         ev("src:bulk-api-intro", "Cobre parte do tema: Bulk API 2.0 e Bulk API.", "Introduction to Bulk API 2.0 and Bulk API"),
         ev("src:mdapi-intro", "Cobre parte do tema: Metadata API.", "Understanding Metadata API"),
         ev("src:tooling-intro", "Cobre parte do tema: Tooling API.", "Introduction to Tooling API")],
    ),
    "sub:autenticacao-de-integracoes": (
        "Como um sistema externo prova quem é ao chamar a org: o registro da integração num external client app ou connected app e "
        "os tokens OAuth, com escopos, que esse registro emite.",
        [ev("src:help-eca-create", "Cobre parte do tema: external client apps, o registro recomendado para integrações novas.", "Create an External Client App"),
         ev("src:help-connected-app-basics", "Cobre parte do tema: connected apps.", "Configure Basic Connected App Settings")],
    ),
    "sub:chamadas-externas-e-endpoints": (
        "As chamadas que a org faz para serviços de fora e os endereços liberados para elas: sites remotos, serviços externos "
        "descritos em OpenAPI, conexões privadas e os limites de callout.",
        [ev("src:help-remote-site", "Cobre parte do tema: liberação de endereços para callouts.", "Configure Remote Site Settings"),
         ev("src:apex-callout-limits", "Cobre parte do tema: limites e restrições de callouts em Apex.", "Callout Limits and Limitations")],
    ),
    "sub:credenciais": (
        "Onde a org guarda o endereço de um sistema externo e a forma de se autenticar nele, fora do código: named credentials e, "
        "desde a versão 56.0, external credentials.",
        [ev("src:help-nc-create", "Cobre parte do tema: criação e edição de named credentials.", "Create or Edit a Named Credential"),
         ev("src:mdapi-externalcredential", "Cobre parte do tema: external credentials como metadado.", "ExternalCredential")],
    ),
    "sub:eventos-e-mensageria": (
        "Como a org avisa outros sistemas, e é avisada, sem consulta periódica: eventos de plataforma, eventos de captura de "
        "alterações, a Pub/Sub API para assinar de fora e o Event Relay.",
        [ev("src:help-platform-events-define", "Cobre parte do tema: definição de eventos de plataforma.", "Define and Manage Platform Events"),
         ev("src:pubsub-overview", "Cobre parte do tema: publicação e assinatura de eventos por clientes externos.", "Pub/Sub API overview"),
         ev("src:help-event-relay-create", "Cobre parte do tema: envio de eventos para a AWS.", "Create an Event Relay")],
    ),
    "sub:conectividade-e-virtualizacao-de-dados": (
        "Como mostrar dados de outro sistema dentro da org sem copiá-los: objetos externos, lidos no momento da consulta a partir "
        "de uma fonte de dados externa.",
        [ev("src:help-external-data-source-odata", "Cobre parte do tema: fonte de dados externa pelo adaptador OData do Salesforce Connect.",
            "Define an External Data Source for Salesforce Connect—OData 2.0 or 4.0 Adapter")],
    ),
    "sub:contratos-limites-e-tratamento-de-falhas": (
        "As regras que valem para toda integração: quantas chamadas cabem por dia, quanto tempo cada uma pode levar, quais versões "
        "de API continuam valendo e como tratar falhas e retentativas.",
        [ev("src:limits-api-requests", "Cobre parte do tema: alocações e limites de requisições de API.", "API Request Limits and Allocations"),
         ev("src:rest-api-eol", "Cobre parte do tema: política de fim de vida das versões de API.", "API End-of-Life Policy"),
         ev("src:pe-retry-apex", "Cobre parte do tema: retentativa em assinantes de eventos.")],
    ),
}


def aplicar():
    with open(os.path.join(ROOT, "..", "fontes", "registro.json"), encoding="utf-8") as f:
        fontes = {x["id"] for x in json.load(f)["fontes"]}
    faltam = sorted({r["fonte"] for _, refs in TEMAS.values() for r in refs} - fontes)
    if faltam:
        raise SystemExit(f"fontes não registradas: {faltam}")
    d = os.path.join(ROOT, "subclassificacoes")
    for tid, (descricao, refs) in TEMAS.items():
        nome = tid.split(":", 1)[1]
        caminho = os.path.join(d, nome + ".json")
        if not os.path.exists(caminho):
            raise SystemExit(f"tema inexistente: {tid}")
        with open(caminho, encoding="utf-8") as f:
            ent = json.load(f)
        ent["descricao"] = descricao
        ent["referencias_oficiais"] = refs
        ent["nota_estado"] = NOTA_ESTADO
        save("subclassificacoes", nome, ent)
    print(f"temas internos atualizados: {len(TEMAS)}")


if __name__ == "__main__":
    aplicar()
