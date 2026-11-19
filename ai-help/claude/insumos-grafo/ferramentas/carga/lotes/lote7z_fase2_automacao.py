"""Lote 7z (Fase 2, classificação Automação de processos e regras de negócio): explicação dos campos de primeiro nível de Flow.

Fonte: página de Flow na referência atual da Metadata API (src:mdapi-flow-ref-atual). Texto parafraseado em pt-BR, escrito para
iniciantes. Quando a página informa a versão em que o campo entrou e o catálogo tinha 'desconhecido', a versão também é gravada.
Ficam pendentes, por falta de texto na fonte: Flow.segment, cinco campos de FlowSettings e ApprovalProcess.processOrder
(ver a nota de extração).

Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv               # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-18"
EXTR = "fontes/extracoes/lote7z-fase2-automacao.txt"
SRC = "src:mdapi-flow-ref-atual"
C.registrar_fontes([
    C.fonte(SRC, "Flow (Metadata API, referência atual)",
            "https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-flow.html",
            "Descrição e versão dos campos de primeiro nível de Flow.", EXTR, DATA, versao="68.0 (exibida na página; sem versão na URL)"),
])

# nome: (versão em que entrou ou None, texto)
TEXTOS = {
    "actionCalls": ("31.0", "Lista dos nós que chamam ações durante a execução do flow."),
    "apexPluginCalls": (None, "Lista dos nós que chamam plug-ins escritos em Apex."),
    "assignments": (None, "Lista dos nós de atribuição, que dão ou alteram valores durante a execução."),
    "choices": (None, "Lista das opções de escolha fixas (estáticas) do flow."),
    "collectionFilterCriteria": (None, "Reservado pela Salesforce para uso futuro; não tem efeito hoje."),
    "collectionProcessors": ("50.0", "Lista dos nós que processam coleções (listas de valores ou de registros)."),
    "constants": (None, "Lista das constantes: valores fixos que o flow pode reutilizar sem alterar."),
    "customErrors": (None, "Lista dos erros personalizados definidos no flow."),
    "customProperties": ("63.0", "Lista de propriedades personalizadas do flow, como o indicador de progresso das telas."),
    "decisions": (None, "Lista dos nós de decisão, que escolhem por qual caminho o flow segue."),
    "dynamicChoiceSets": (None, "Lista dos conjuntos de opções montados a partir de uma consulta ao banco de dados."),
    "ends": ("68.0", "Lista dos nós de fim do flow."),
    "exitRules": ("61.0", "Lista das regras que encerram o flow para um usuário, em flows disparados por segmento."),
    "experiments": ("61.0", "Lista de experimentos definidos no flow."),
    "formulas": (None, "Lista das fórmulas: recursos que calculam um valor a partir de outros dados do flow."),
    "groups": ("68.0", "Lista dos nós de grupo do flow."),
    "loops": ("30.0", "Lista dos nós que percorrem coleções, item a item."),
    "orchestratedStages": ("53.0", "Lista dos nós de estágio de uma orquestração."),
    "processMetadataValues": ("31.0", "Valores de metadados do flow."),
    "recordCreates": (None, "Lista dos nós que criam registros no banco de dados."),
    "recordDeletes": (None, "Lista dos nós que excluem registros do banco de dados."),
    "recordLookups": (None, "Lista dos nós que buscam registros no banco de dados."),
    "recordRollbacks": ("52.0", "Lista dos nós que desfazem (rollback) as alterações da transação num screen flow."),
    "recordUpdates": (None, "Lista dos nós que atualizam registros no banco de dados."),
    "screens": (None, "Lista dos nós de tela, as telas que o usuário vê durante o flow."),
    "stages": ("42.0", "Lista dos recursos de estágio, que podem ser usados ao longo do flow."),
    "start": ("47.0", "O elemento Start do flow, que define como e quando ele começa."),
    "steps": (None, "Lista dos nós de passo (step)."),
    "subflows": ("25.0", "Lista dos subflows: outros flows chamados a partir deste."),
    "textTemplates": (None, "Lista dos modelos de texto do flow."),
    "transforms": ("59.0", "Lista das transformações de dados feitas no flow."),
    "variables": (None, "Lista das variáveis do flow, que guardam valores durante a execução."),
    "waits": ("32.0", "Lista dos nós de espera, que pausam o flow."),
    "areMetricsLoggedToDataCloud": ("63.0", "Indica se as métricas do flow são registradas no Data Cloud (hoje Data 360). O padrão é false."),
    "isAdditionalPermissionRequiredToRun": ("47.0", "Com true, só usuários com perfis ou permission sets habilitados para este flow podem executá-lo; muda o comportamento padrão de acesso. O padrão é false."),
    "timeZoneSidKey": ("56.0", "Identificador do fuso horário em que o flow roda."),
}
NOTAS = {}

m = ld("metadata-types/Flow.json")
n = 0
for p in m["propriedades"]:
    if p["nome"] not in TEXTOS or p.get("explicacao") != "pendente":
        continue
    v, txt = TEXTOS[p["nome"]]
    p["o_que_e"] = txt
    p["explicacao"] = "explicada"
    if SRC not in [e["fonte"] for e in p["evidencias"]]:
        p["evidencias"].append({"fonte": SRC})
    if v and p["disponibilidade"].get("estado") == "desconhecido":
        p["disponibilidade"] = {"desde_versao": v, "ate_versao": None, "estado": "verificado"}
    if p["nome"] in NOTAS:
        p.setdefault("notas", []).append(NOTAS[p["nome"]])
    n += 1
sv("metadata-types/Flow.json", m)
print(f"lote 7z: {n} propriedades de Flow explicadas")
