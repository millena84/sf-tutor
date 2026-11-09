# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Lote 5f (issue #24): REST, SOAP, Metadata e Tooling API como funcionalidades.
import json
from b1_base import ev, af

BASE = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/"
CAT = BASE + "catalogo/"
DATA = "2026-11-09"
def ld(p): return json.load(open(CAT + p, encoding="utf-8"))
def sv(p, d):
    with open(CAT + p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")

reg = json.load(open(BASE + "fontes/registro.json"))
A = "https://developer.salesforce.com/docs/atlas.en-us.264.0."
CHK = {"estado": "verificado", "nota": f"Conteúdo lido em {DATA} e conferido quanto ao assunto (não apenas HTTP 200)."}
def src(id, t, u, pert):
    return {"id": id, "titulo": t, "url": A + u, "tipo": "oficial_documentacao", "versao": "68.0", "data_verificacao": DATA, "metodo": "extracao_documental_assistida",
            "pertinencia": pert, "extracao": "fontes/extracoes/lote5f-apis.txt", "checagem_online": CHK}
novas = [
 src("src:rest-intro", "Introduction to REST API", "api_rest.meta/api_rest/intro_rest.htm", "O que é a REST API e requisitos de acesso."),
 src("src:rest-resources", "REST Resources", "api_rest.meta/api_rest/intro_rest_resources.htm", "Estrutura de URI, formatos e tipos de recurso da REST API."),
 src("src:rest-composite", "Composite (REST API)", "api_rest.meta/api_rest/resources_composite_composite.htm", "Várias requisições em uma chamada e contagem nos limites."),
 src("src:soap-intro", "Introduction to SOAP API", "api.meta/api/sforce_api_quickstart_intro.htm", "O que é a SOAP API, WSDLs, edições e permissão."),
 src("src:mdapi-intro", "Understanding Metadata API", "api_meta.meta/api_meta/meta_intro.htm", "Finalidade da Metadata API, deploy/retrieve e source tracking."),
 src("src:tooling-intro", "Introduction to Tooling API", "api_tooling.meta/api_tooling/intro_api_tooling.htm", "O que é a Tooling API, acesso REST/SOAP e casos de uso."),
]
ids = {f["id"] for f in reg["fontes"]}
reg["fontes"] += [n for n in novas if n["id"] not in ids]
json.dump(reg, open(BASE + "fontes/registro.json", "w"), ensure_ascii=False, indent=2)

INTc, SUB, DEV = "integracao-apis-e-eventos", "apis-de-dados-e-metadados", "desenvolvimento-testes-e-entrega"
AUS = lambda tipo, estado, m, s=None: {"tipo": tipo, "estado": estado, "motivo": m, **({"evidencias": [ev(s)]} if s else {})}
SETUP_NA = af("nao_aplicavel", None, "API acessada por clientes; não é configurada por uma tela de Setup nas fontes deste lote.")
def addsub(fid, subs):
    for s in subs:
        d = ld(f"subclassificacoes/{s}.json"); d["funcionalidades"] = sorted(set(d["funcionalidades"]) | {"func:" + fid}); sv(f"subclassificacoes/{s}.json", d)
def F(fid, nome, aliases, oq, fin, ex, secundarias, srcs, ausencias, codigo=(), recs=(), alertas=(), limit=(), pre=()):
    f = {"id": "func:" + fid, "nome": nome, "nome_tecnico": nome, "aliases": aliases,
         "termos_busca": sorted(set([nome.lower()] + [a.lower() for a in aliases])), "o_que_e": oq, "finalidade": fin, "exemplo": ex,
         "classificacao_principal": {"classificacao": "cls:" + INTc, "subclassificacao": "sub:" + SUB},
         "classificacoes_secundarias": [{"classificacao": "cls:" + c, "subclassificacao": "sub:" + s, "motivo": m} for c, s, m in secundarias],
         "representacoes": {"metadata_types": [], "objetos_api": [], "ausencias": ausencias, "codigo": list(codigo)},
         "setup": SETUP_NA, "pre_requisitos": list(pre), "recomendacoes": [{"texto": t, "natureza": n, "evidencias": [ev(s)]} for t, n, s in recs],
         "alertas": list(alertas), "limitacoes": list(limit), "estado": "verificado", "evidencias": [ev(s) for s in srcs]}
    sv(f"funcionalidades/{fid}.json", f); addsub(fid, [SUB] + [s for _, s, _ in secundarias])

OBJS = lambda s: AUS("objeto_api", "nao_aplicavel", "A API dá acesso aos objetos expostos da org; ela própria não é um objeto. Os objetos aparecem cada um em sua ficha.", s)
NOMDT = lambda s: AUS("metadata_type", "nao_aplicavel", "Uma API não é um componente implantável; nenhum metadata type a representa.", s)
LIM = "Conta no limite diário de requisições de API da org (ver Limites de API e alocações)."

F("rest-api", "REST API", ["rest", "api rest", "/services/data", "composite", "json"],
  "API baseada em HTTP para ler e gravar dados da Salesforce: cada recurso (registro, consulta, metadados de objeto, limites) tem uma URI própria.",
  "Integrar aplicações à Salesforce com chamadas HTTP simples, em JSON ou XML.",
  "Um app de pedidos busca uma conta por Id e cria uma oportunidade com duas requisições HTTP; com o recurso Composite, as duas viram uma só chamada.",
  [], ["src:rest-intro", "src:rest-resources", "src:rest-composite", "src:limits-api-requests"], [NOMDT("src:rest-intro"), OBJS("src:rest-resources")],
  codigo=["URI: https://MyDomainName.my.salesforce.com/services/data/vXX.X/recurso/ (alias latest)", "Formatos: JSON ou XML, escolhidos por Content-Type e Accept (JSON por padrão)",
          "Composite: POST que executa várias requisições REST e conta como uma chamada"],
  recs=[("Use o recurso Composite para encadear requisições dependentes: a série inteira conta como uma chamada para os limites.", "orientacao_oficial", "src:rest-composite")],
  alertas=[LIM, "IDs diferenciam maiúsculas de minúsculas; nomes de objeto e de campo, não."],
  limit=["O número máximo de subrequisições do Composite e o comportamento allOrNone não constam das páginas lidas."],
  pre=["App cliente autorizado por external client app ou connected app, com fluxo OAuth 2.0.", "Org com acesso à API e usuário com acesso à API habilitado."])

F("soap-api", "SOAP API", ["soap", "wsdl", "enterprise wsdl", "partner wsdl"],
  "API baseada em SOAP e WSDL para acessar os objetos da org. Oferece dois WSDLs: Enterprise, fortemente tipado e específico da org; e Partner, fracamente tipado e genérico.",
  "Integrar sistemas que trabalham com contratos WSDL, como muitas plataformas corporativas.",
  "Um ERP gera o cliente a partir do Enterprise WSDL da org; quando um campo customizado é criado, o WSDL precisa ser gerado de novo.",
  [], ["src:soap-intro", "src:limits-api-requests"], [NOMDT("src:soap-intro"), OBJS("src:soap-intro")],
  codigo=["Enterprise WSDL: representação fortemente tipada da org", "Partner WSDL: representação fracamente tipada, para várias orgs", "Padrões: SOAP 1.1, WSDL 1.1, WS-I Basic Profile 1.1"],
  recs=[("Construa e teste em Developer Edition, sandbox ou scratch org antes da produção.", "orientacao_oficial", "src:soap-intro")],
  alertas=[LIM, "O Enterprise WSDL precisa ser gerado de novo quando objetos ou campos customizados mudam."],
  pre=["Edição Enterprise, Performance, Unlimited ou Developer.", "Permissão API Enabled no usuário."])

F("metadata-api", "Metadata API", ["metadata api", "mdapi", "deploy", "retrieve", "implantação"],
  "API que move metadados (a estrutura e a configuração da org) entre orgs. Trabalha com metadata types e seus componentes; não trata dados de negócio.",
  "Implantar, recuperar, criar, atualizar e excluir customizações durante o desenvolvimento.",
  "Um objeto customizado e seu layout são recuperados da sandbox com retrieve() e implantados em produção com deploy().",
  [(DEV, "versionamento-deploy-e-recuperacao", "deploy() e retrieve() são a base da implantação entre orgs.")], ["src:mdapi-intro"],
  [AUS("metadata_type", "nao_aplicavel", "A Metadata API transporta os metadata types, mas não é um deles; os tipos aparecem na visão técnica do mapa.", "src:mdapi-intro"),
   AUS("objeto_api", "nao_aplicavel", "Trata metadados, não registros: para dados de negócio, a página indica SOAP API ou REST API.", "src:mdapi-intro")],
  codigo=["deploy() e retrieve(): movem o modelo completo de metadados", "Source push e pull (Salesforce CLI): movem só o que mudou, com source tracking"],
  recs=[("Use deploy()/retrieve() nas fases finais (por exemplo, implantar em produção) e source push/pull com source tracking nas fases intermediárias.", "orientacao_oficial", "src:mdapi-intro")],
  limit=["Os limites da Metadata API não foram obtidos nesta sessão (a página de limites não pôde ser lida)."])

F("tooling-api", "Tooling API", ["tooling api", "ferramentas de desenvolvimento", "soql em metadados"],
  "API para construir ferramentas de desenvolvimento: expõe, como objetos consultáveis, os metadados usados por essas ferramentas, por REST ou SOAP.",
  "Ler e alterar pedaços pequenos de metadados com rapidez, em ferramentas interativas.",
  "Um editor de código consulta, via SOQL na Tooling API, só a classe Apex que o desenvolvedor abriu, em vez de recuperar todos os metadados.",
  [(DEV, "codigo-e-bundles", "É a API das ferramentas de desenvolvimento que editam código e componentes.")], ["src:tooling-intro"],
  [NOMDT("src:tooling-intro"),
   AUS("objeto_api", "desconhecido", "A Tooling API expõe objetos próprios; a relação deles com os objetos deste catálogo não foi investigada neste lote.")],
  codigo=["REST (recomendado para linguagens não fortemente tipadas, como JavaScript) ou SOAP", "SOQL sobre objetos de metadados para buscar pedaços menores"],
  limit=["A página não compara a Tooling API com a Metadata API; a diferença registrada aqui é a granularidade, como a página descreve.",
         "Não suponha que um objeto da API padrão tem a mesma exposição na Tooling API: cada ficha de objeto registra isso separadamente."])

core = ld("nuvens/platform-core.json")
c = next(x for x in core["classificacoes_aplicaveis"] if x["classificacao"] == "cls:" + INTc)
s = next(x for x in c["subclassificacoes"] if x["subclassificacao"] == "sub:" + SUB)
s["funcionalidades"] = sorted(set(s["funcionalidades"]) | {"func:rest-api", "func:soap-api", "func:metadata-api", "func:tooling-api"})
sv("nuvens/platform-core.json", core)
print("ok lote 5f")
