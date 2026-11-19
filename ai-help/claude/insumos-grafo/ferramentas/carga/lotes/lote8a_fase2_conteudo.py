"""Lote 8a (Fase 2, classificação Conteúdo, conhecimento e colaboração): explicação dos 35 campos pendentes de KnowledgeArticleVersion.

Fonte: Object Reference 264.0, endpoint versionado. Grava texto parafraseado, o tipo (quando o catálogo tinha '(a extrair)') e a versão
em que o campo entrou, quando a página informa. As propriedades de API (Create, Filter...) não foram lidas e seguem 'desconhecido'.
Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv               # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-18"
EXTR = "fontes/extracoes/lote8a-fase2-conteudo.txt"
SRC = "src:objref-knowledgearticleversion-264"
C.registrar_fontes([C.fonte(SRC, "KnowledgeArticleVersion (Object Reference 264.0)",
    "https://developer.salesforce.com/docs/get_document_content/object_reference/sforce_api_objects_knowledgearticleversion.htm/en-us/264.0",
    "Tipo e descrição dos campos de KnowledgeArticleVersion.", EXTR, DATA)])

MULTI = " Só existe quando a base de conhecimento tem suporte a vários idiomas."
# nome: (tipo, versão, texto)
T = {
    "ArchivedById": ("reference", None, "Usuário que arquivou o artigo."),
    "ArchivedDate": ("dateTime", None, "Data em que esta versão do artigo foi arquivada."),
    "ArticleArchivedById": ("reference", None, "Usuário que arquivou o artigo."),
    "ArticleArchivedDate": ("dateTime", None, "Data em que o artigo foi arquivado."),
    "ArticleCaseAttachCount": ("int", None, "Quantidade de casos aos quais o artigo está anexado."),
    "ArticleCreatedById": ("reference", None, "Usuário que criou o artigo."),
    "ArticleCreatedDate": ("dateTime", None, "Data em que o artigo foi criado."),
    "ArticleMasterLanguage": ("picklist", None, "Idioma original do artigo." + MULTI),
    "ArticleNumber": ("string", None, "Número único dado automaticamente na criação do artigo; formato e valor não podem ser alterados."),
    "ArticleTotalViewCount": ("int", None, "Total de visualizações do artigo."),
    "ArticleType": ("string", "26.0", "Nome de API do tipo de artigo, definido na criação e imutável. Existe em orgs que usam o Knowledge do Salesforce Classic."),
    "AssignedById": ("reference", None, "Usuário que atribuiu o artigo a alguém."),
    "AssignedToId": ("reference", None, "Usuário a quem o artigo está atribuído."),
    "AssignmentDate": ("dateTime", None, "Data em que o artigo foi atribuído a um usuário."),
    "AssignmentDueDate": ("dateTime", None, "Prazo da atribuição do artigo."),
    "AssignmentNote": ("textarea", None, "Observações deixadas por quem atribuiu o artigo para quem o recebeu."),
    "FirstPublishedDate": ("dateTime", None, "Data da primeira publicação do artigo."),
    "IsMasterLanguage": ("boolean", None, "Indica se o artigo tem uma ou mais traduções associadas." + MULTI),
    "IsOutOfDate": ("boolean", None, "Indica se o artigo de origem foi alterado depois que esta tradução foi criada." + MULTI),
    "IsVisibleInApp": ("boolean", None, "Indica se o artigo aparece na aba Articles. A página marca o campo como obrigatório."),
    "IsVisibleInCsp": ("boolean", None, "Indica se o artigo aparece no Customer Portal. A página marca o campo como obrigatório."),
    "IsVisibleInPkb": ("boolean", None, "Indica se o artigo aparece na base de conhecimento pública. A página marca o campo como obrigatório."),
    "IsVisibleInPrm": ("boolean", None, "Indica se o artigo aparece no portal de parceiros. A página marca o campo como obrigatório."),
    "LargeLanguageModel": ("string", "59.0", "Modelo de linguagem (LLM) usado para criar esta versão do artigo."),
    "LastPublishedDate": ("dateTime", None, "Data da última publicação do artigo."),
    "MasterVersionId": ("reference", None, "Artigo de origem, quando este artigo é uma tradução." + MULTI),
    "MigratedToFromArticleVersion": ("string", "43.0", "Versão correspondente do artigo antes ou depois da migração; só tem valor em orgs migrando do Knowledge do Classic para o Lightning Knowledge."),
    "NextReviewDate": ("dateTime", "58.0", "Data em que o artigo deve ser revisado de novo para conferir se continua correto."),
    "OwnerId": ("reference", None, "Dono do artigo."),
    "SourceId": ("reference", None, "Registro a partir do qual o artigo foi criado: um caso (Case) ou uma resposta (Reply)."),
    "Summary": ("textarea", None, "Resumo do artigo, com até 1000 caracteres."),
    "TranslationCompletedDate": ("dateTime", None, "Data e hora da última tradução do artigo." + MULTI),
    "TranslationExportedDate": ("dateTime", None, "Data e hora da última exportação do artigo para tradução." + MULTI),
    "TranslationImportedDate": ("dateTime", None, "Data e hora da última importação de tradução do artigo." + MULTI),
    "ValidationStatus": ("picklist", "24.0", "Indica se o conteúdo do artigo foi validado: Validated ou Not Validated (o padrão é Not Validated)."),
}

o = ld("objetos-api/KnowledgeArticleVersion.json")
n = 0
for c in o["campos"]:
    if c["nome"] not in T or c.get("explicacao") != "pendente":
        continue
    tipo, v, txt = T[c["nome"]]
    if c.get("tipo_tecnico") in (None, "(a extrair)"):
        c["tipo_tecnico"] = tipo
    c["o_que_e"] = txt
    c["explicacao"] = "explicada"
    if SRC not in [e["fonte"] for e in c["evidencias"]]:
        c["evidencias"].append({"fonte": SRC})
    if v and c["disponibilidade"].get("estado") == "desconhecido":
        c["disponibilidade"] = {"desde_versao": v, "ate_versao": None, "estado": "verificado"}
    velha = "Nome listado na Object Reference; tipo e propriedades não extraídos nesta rodada."
    c["notas"] = [x for x in c.get("notas", []) if x != velha] + ["Tipo e descrição lidos na Object Reference 264.0 (lote 8a); propriedades de API (Create, Filter etc.) não extraídas."]
    n += 1
exp = o["cobertura"]["explicativa"]
exp["presente"] = sum(1 for c in o["campos"] if c.get("explicacao") == "explicada")
if exp["presente"] == exp["esperado"]:
    exp["estado"] = "completa"
sv("objetos-api/KnowledgeArticleVersion.json", o)
print(f"lote 8a: {n} campos de KnowledgeArticleVersion explicados")
