"""Lote 7w (rodada de nuvens, decisão da autora em 2026-11-17): nuvens e produtos que faltavam no mapa.

Entram como nó, com nome oficial atual, resumo, contexto técnico, licenças conhecidas e fonte, ligados às
funcionalidades já cadastradas. Não há inventário de metadata types dessas nuvens (cobertura_inventario = nao_iniciada).

- Rodam na org: Experience Cloud, Agentforce Field Service and Operations, Agentforce Revenue Management, Industries.
- Família mista: Agentforce Marketing, Agentforce Commerce, Tableau.
- Plataforma própria, conectada à org: MuleSoft, Slack.
Também: o nó Platform/Core passa a usar o nome atual, Agentforce 360 Platform (antes Salesforce Platform).

O campo `categoria` é classificação didática do projeto (ver schemas/nuvem.schema.json).
Ordem: lote7v_d1_campos_principais.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv, ev           # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7w-nuvens-faltantes.txt"
H = "https://help.salesforce.com/s/articleView?language=en_US&id="
AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")
PROD = dict(tipo="oficial_produto", versao="sem versão (site da Salesforce)", metodo="leitura_resultado_busca")
FONTES = [
    # nome da plataforma
    ("src:prod-agentforce-360-platform", "Agentforce 360 Platform (Formerly Salesforce Platform)", "https://www.salesforce.com/platform/",
     "Página do produto: Agentforce 360 Platform, antes Salesforce Platform; Customer 360 reúne Sales, Service, Marketing, Commerce e Industries.", PROD),
    # Experience Cloud
    ("src:help-experience-cloud-overview", "Experience Cloud", H + "experience.networks_overview.htm&type=5",
     "Experience Cloud cria experiências digitais com a marca da empresa; vários sites na mesma org; edições Enterprise, Performance, Unlimited e Developer.", AJ),
    ("src:help-experience-cloud-create-site", "Create an Experience Cloud Site", H + "experience.networks_creating.htm&type=5",
     "Sites são criados no Setup, em Digital Experiences > All Sites > New.", AJ),
    # Field Service
    ("src:help-fs-overview", "Agentforce Field Service and Operations", H + "service.fs_overview.htm",
     "Field Service agora se chama Agentforce Field Service and Operations; hub de serviço de campo dentro da Salesforce.", AJ),
    ("src:help-fs-set-up", "Set Up Field Service Basics", H + "sf.fs_set_up.htm&type=5",
     "Recursos principais, pacote gerenciado e app móvel do Field Service: edições Enterprise, Unlimited e Developer.", AJ),
    ("src:help-fs-mobile", "Field Service Mobile App", H + "sf.mfs_overview.htm&type=5",
     "O app móvel exige a licença de usuário Field Service Mobile.", AJ),
    ("src:help-fs-key-concepts", "Field Service Key Concepts and Glossary", H + "service.fs_key_concepts.htm&type=5",
     "Despachante precisa do permission set Field Service Dispatcher e da licença Field Service Dispatcher.", AJ),
    # Revenue
    ("src:help-revenue-learn", "Learn About Revenue Management", H + "ind.revenue_lifecycle_management.htm&type=5",
     "Revenue Cloud agora se chama Revenue Management na Ajuda; ciclo de receita das vendas às assinaturas.", AJ),
    ("src:help-revenue-plan", "Plan Your Revenue Management Implementation", H + "ind.plan_your_revenue_cloud_implementation.htm&type=5",
     "Disponível nas edições Enterprise, Unlimited e Developer de Revenue Management.", AJ),
    ("src:help-revenue-coexistence", "Coexistence of Revenue Management with Other Salesforce Products", H + "ind.rev_cloud_coexistence.htm&type=5",
     "Revenue Management convive com outros produtos na mesma org quando ambos estão provisionados.", AJ),
    ("src:prod-agentforce-revenue", "Agentforce Revenue Management (formerly Revenue Cloud)",
     "https://www.salesforce.com/ap/sales/revenue-lifecycle-management/",
     "Página do produto: Agentforce Revenue Management, antes Revenue Cloud.", PROD),
    # Industries
    ("src:help-fsc-admin", "Agentforce Financial Services", H + "ind.fsc_admin.htm&type=5",
     "Agentforce Financial Services (antes Financial Services Cloud) é construído sobre a plataforma CRM e usa recursos de Sales Cloud e Service Cloud.", AJ),
    ("src:help-health-admin", "Agentforce Health", H + "ind.healthcare_admin.htm",
     "Health Cloud agora se chama Agentforce Health; edições Enterprise e Unlimited com Health Cloud.", AJ),
    ("src:help-rn-industries-246", "Industries (Release Notes)", H + "release-notes.rn_industries.htm&release=246&type=5",
     "Notas de versão agrupam as nuvens de setor sob Industries; Energy & Utilities Cloud estende Sales, Service e a Salesforce Platform.", AJ),
    # Marketing
    ("src:prod-agentforce-marketing", "Agentforce Marketing (formerly Marketing Cloud)", "https://www.salesforce.com/marketing/",
     "Marketing Cloud é a marca do conjunto; Marketing Cloud Next foi reconstruído de forma nativa na Salesforce Platform; Engagement vem do ExactTarget.", PROD),
    ("src:prod-agentforce-marketing-explained", "Agentforce Marketing Explained", "https://www.salesforce.com/marketing/agentforce-marketing-explained/",
     "Agentforce Marketing é o novo nome da plataforma de marketing; Marketing Cloud Engagement continua vendido.", PROD),
    ("src:help-rn-account-engagement", "Marketing Cloud Account Engagement (Release Notes)", H + "release-notes.rn_mcae.htm&release=242&type=5",
     "Pardot agora se chama Marketing Cloud Account Engagement.", AJ),
    # Commerce
    ("src:help-b2c-getting-started", "Get Started with B2C Commerce", H + "cc.b2c_getting_started.htm&type=5",
     "Commerce Cloud agora se chama Agentforce Commerce; B2C Commerce é uma plataforma de comércio para lojas que vendem direto ao consumidor.", AJ),
    ("src:help-b2c-account-manager", "How To Set Up Separate Account Manager orgs For B2C Commerce Users On SSO",
     "https://help.salesforce.com/s/articleView?id=000394931&language=en_US&type=1",
     "Usuários do B2C Commerce acessam pelo Account Manager, que tem orgs próprias.", AJ),
    # Tableau
    ("src:help-tableau-portfolio", "Tableau Product Portfolio", H + "sf.tableau_about.htm",
     "Tableau Cloud é uma plataforma de analytics totalmente hospedada; Tableau Next é construído sobre a Salesforce Platform e o Data 360.", AJ),
    ("src:help-tableau-next", "Tableau Next", H + "analytics.tua.htm",
     "Tableau Next exige Data 360 e a camada semântica do Data 360.", AJ),
    # MuleSoft
    ("src:help-mulesoft-anypoint-connection", "Manage Your MuleSoft Anypoint Platform Connections",
     H + "platform.mulesoft_manage_your_anypoint_platform_connection.htm&type=5",
     "Org Salesforce e organização do Anypoint Platform se ligam por uma relação de tenant.", AJ),
    # Slack
    ("src:help-slack-connect-org", "Connect a New Salesforce Org to Slack", H + "slack.slack_apps_digital_hq_multiorg_connect_org.htm&type=5",
     "Com Salesforce for Slack, um workspace do Slack pode se conectar a várias orgs Salesforce.", AJ),
    ("src:help-slack-enable", "Enable Salesforce for Slack Integrations", "https://help.salesforce.com/s/articleView?id=slack.slack_apps_enable.htm&language=en_US",
     "Integração habilitada no Setup, em Slack Apps Setup; a permissão Connect Salesforce with Slack é exigida pela maioria dos apps.", AJ),
]
C.registrar_fontes([C.fonte(i, t + (" (Salesforce Help)" if kw is AJ else ""), u, n, EXTR, DATA, **kw) for i, t, u, n, kw in FONTES])


def afirm(valor, nota, srcs):
    return {"estado": "verificado", "valor": valor, "nota": nota, "evidencias": [ev(s) for s in srcs]}


def lic(nota, itens, estado="verificado"):
    return {"estado": estado, "nota": nota, "itens": [{"nome": n, "tipo": t, "evidencias": [ev(s) for s in ss]} for n, t, ss in itens]}


def ca(func_id):
    """classificacoes_aplicaveis a partir da classificação principal da funcionalidade (sem inventar caminho)."""
    f = ld(f"funcionalidades/{func_id.split(':', 1)[1]}.json")
    return f["classificacao_principal"]["classificacao"], f["classificacao_principal"]["subclassificacao"]


def classificacoes(funcs):
    agr = {}
    for fid in funcs:
        c, s = ca(fid)
        agr.setdefault(c, {}).setdefault(s, []).append(fid)
    return [{"classificacao": c, "subclassificacoes": [{"subclassificacao": s, "funcionalidades": fs} for s, fs in subs.items()]}
            for c, subs in agr.items()]


NUVENS = [
    dict(id="nuv:experience-cloud", nome_oficial="Experience Cloud", aliases=["Digital Experiences", "Comunidades"], sigla="EXP", categoria="na_org",
         resumo="Produto para criar sites, portais e fóruns com a marca da empresa, para clientes, parceiros ou funcionários, dentro da própria org.",
         o_que_e="Na Ajuda, Experience Cloud cria experiências digitais para compartilhar informação e colaborar com quem participa dos processos do negócio. Uma org pode ter vários sites, criados no Setup em Digital Experiences.",
         contexto_tecnico=afirm("Roda na mesma org: os sites são criados e configurados no Setup (Digital Experiences > All Sites) e usam os objetos da org.",
                                "As licenças de usuário externo (comunidade, parceiro) não foram registradas neste lote.",
                                ["src:help-experience-cloud-overview", "src:help-experience-cloud-create-site"]),
         licencas=lic("Edições registradas; licenças de usuário externo não registradas.",
                      [("Enterprise, Performance, Unlimited e Developer", "edicao", ["src:help-experience-cloud-overview"])]),
         funcs=["func:experience-cloud-sites", "func:digital-experiences"],
         evid=["src:help-experience-cloud-overview", "src:help-experience-cloud-create-site"]),
    dict(id="nuv:field-service", nome_oficial="Agentforce Field Service and Operations", aliases=["Field Service", "Field Service Lightning"], sigla="FSO", categoria="na_org",
         resumo="Produto para o trabalho feito no local do cliente: ordens de serviço, agendamento, despacho e app móvel para técnicos. Antes se chamava Field Service.",
         o_que_e="Na Ajuda, é um hub de serviço de campo dentro da Salesforce, configurável e pensado para uso móvel. A Ajuda avisa que o nome antigo, Field Service, ainda aparece em telas e documentos.",
         contexto_tecnico=afirm("Roda na org: recursos principais e pacote gerenciado são habilitados na própria org, e o app móvel acessa os mesmos dados.",
                                "O pacote gerenciado e o app móvel fazem parte do produto; detalhes de instalação não foram registrados.",
                                ["src:help-fs-overview", "src:help-fs-set-up"]),
         licencas=lic("Licenças por papel registradas a partir da Ajuda; lista completa não registrada.",
                      [("Enterprise, Unlimited e Developer", "edicao", ["src:help-fs-set-up"]),
                       ("Field Service Mobile (licença de usuário)", "licenca_usuario", ["src:help-fs-mobile"]),
                       ("Field Service Dispatcher (licença)", "licenca_recurso", ["src:help-fs-key-concepts"])]),
         funcs=["func:field-service"],
         evid=["src:help-fs-overview", "src:help-fs-set-up", "src:help-fs-mobile", "src:help-fs-key-concepts"]),
    dict(id="nuv:revenue", nome_oficial="Agentforce Revenue Management", aliases=["Revenue Management", "Revenue Cloud"], sigla="REV", categoria="na_org",
         resumo="Produto para o ciclo de receita: catálogo, preço, cotação, contrato, pedido e cobrança, inclusive assinaturas. Antes se chamava Revenue Cloud.",
         o_que_e="Na Ajuda, Revenue Management (antes Revenue Cloud) gerencia o ciclo de receita, da venda inicial às assinaturas recorrentes, numa só plataforma.",
         contexto_tecnico=afirm("Roda na org e convive com outros produtos (como a automação de vendas) quando os dois estão provisionados na mesma org.",
                                "A página do produto usa o nome Agentforce Revenue Management; a Ajuda usa Revenue Management.",
                                ["src:help-revenue-learn", "src:help-revenue-coexistence", "src:prod-agentforce-revenue"]),
         licencas=lic("Edições registradas; licenças específicas não registradas.",
                      [("Enterprise, Unlimited e Developer de Revenue Management", "edicao", ["src:help-revenue-plan"])]),
         funcs=["func:revenue-management"],
         evid=["src:help-revenue-learn", "src:help-revenue-plan", "src:help-revenue-coexistence", "src:prod-agentforce-revenue"]),
    dict(id="nuv:industries", nome_oficial="Industries", aliases=["Nuvens de setor", "Salesforce Industries"], sigla="IND", categoria="na_org",
         resumo="Conjunto das nuvens de setor (financeiro, saúde, comunicações, energia e outros), que adaptam a Salesforce às necessidades de cada indústria.",
         o_que_e="As notas de versão agrupam as nuvens de setor sob Industries. Vários produtos foram renomeados: Financial Services Cloud agora é Agentforce Financial Services, e Health Cloud agora é Agentforce Health.",
         contexto_tecnico=afirm("Rodam na org: Agentforce Financial Services é construído sobre a plataforma CRM e usa recursos de Sales e Service; Energy & Utilities Cloud estende Sales, Service e a plataforma.",
                                "Cada nuvem de setor tem licença e configuração próprias; aqui elas aparecem agrupadas.",
                                ["src:help-fsc-admin", "src:help-health-admin", "src:help-rn-industries-246"]),
         licencas=lic("Cada nuvem de setor tem licença própria; só um exemplo foi registrado.",
                      [("Enterprise e Unlimited com Health Cloud (Agentforce Health)", "edicao", ["src:help-health-admin"])]),
         funcs=["func:configuracoes-de-nuvens-de-setor"],
         evid=["src:help-fsc-admin", "src:help-health-admin", "src:help-rn-industries-246"]),
    dict(id="nuv:marketing", nome_oficial="Agentforce Marketing", aliases=["Marketing Cloud", "Marketing Cloud Engagement", "Marketing Cloud Next", "Account Engagement", "Pardot"], sigla="MKT", categoria="misto",
         resumo="Família de produtos de marketing da Salesforce, antes Marketing Cloud. Inclui produtos que rodam na plataforma e produtos com plataforma própria.",
         o_que_e="Marketing Cloud é a marca que cobre os produtos de marketing, novos e clássicos. Marketing Cloud Next foi reconstruído de forma nativa na Salesforce Platform; Marketing Cloud Engagement vem do ExactTarget, adquirido pela Salesforce; Account Engagement é o antigo Pardot.",
         contexto_tecnico=afirm("Família mista: Marketing Cloud Next roda nativamente na Salesforce Platform, com Data 360; Marketing Cloud Engagement (Journey Builder, Content Builder, Automation Studio) tem origem no ExactTarget.",
                                "Por isso os tipos do Marketing Cloud Engagement não são metadata types da Metadata API (critério X1 do escopo).",
                                ["src:prod-agentforce-marketing", "src:prod-agentforce-marketing-explained"]),
         licencas=lic("Licenças e edições não registradas.", [], estado="desconhecido"),
         funcs=[],
         evid=["src:prod-agentforce-marketing", "src:prod-agentforce-marketing-explained", "src:help-rn-account-engagement"]),
    dict(id="nuv:commerce", nome_oficial="Agentforce Commerce", aliases=["Commerce Cloud", "B2C Commerce", "B2B Commerce"], sigla="COM", categoria="misto",
         resumo="Família de produtos de comércio eletrônico da Salesforce, antes Commerce Cloud: lojas B2C, comércio B2B, gestão de pedidos e outros.",
         o_que_e="Na Ajuda, Commerce Cloud agora se chama Agentforce Commerce. B2C Commerce é uma plataforma para lojas que vendem direto ao consumidor.",
         contexto_tecnico=afirm("Família mista: usuários do B2C Commerce acessam pelo Account Manager, que tem orgs próprias; já as lojas B2B são configuradas no app Commerce dentro da org (ver serviços externos registrados).",
                                "A separação entre os produtos da família não foi detalhada além do registrado aqui.",
                                ["src:help-b2c-getting-started", "src:help-b2c-account-manager", "src:help-commerce-extensions-store"]),
         licencas=lic("Licenças e edições não registradas.", [], estado="desconhecido"),
         funcs=["func:servicos-externos-registrados-commerce"],
         evid=["src:help-b2c-getting-started", "src:help-b2c-account-manager", "src:help-commerce-extensions-store"]),
    dict(id="nuv:tableau", nome_oficial="Tableau", aliases=["Tableau Cloud", "Tableau Next"], sigla="TAB", categoria="misto",
         resumo="Família de produtos de analytics da Salesforce. Tableau Cloud é hospedado à parte; Tableau Next roda sobre a Salesforce Platform e o Data 360.",
         o_que_e="Na Ajuda, Tableau é uma plataforma de analytics para combinar, gerenciar e explorar dados, inclusive dados da Salesforce, com visualizações interativas.",
         contexto_tecnico=afirm("Família mista: Tableau Cloud é uma plataforma de analytics totalmente hospedada; Tableau Next é construído sobre a Salesforce Platform e exige o Data 360 e a camada semântica dele.",
                                "CRM Analytics não foi ligado a esta família por falta de fonte que trate da relação.",
                                ["src:help-tableau-portfolio", "src:help-tableau-next"]),
         licencas=lic("Licenças e edições não registradas.", [], estado="desconhecido"),
         funcs=[],
         evid=["src:help-tableau-portfolio", "src:help-tableau-next"]),
    dict(id="nuv:mulesoft", nome_oficial="MuleSoft", aliases=["Anypoint Platform"], sigla="MULE", categoria="plataforma_propria",
         resumo="Plataforma de integração e APIs. Tem organização e contas próprias (Anypoint Platform) e se conecta à org Salesforce.",
         o_que_e="A organização do Anypoint Platform e a org Salesforce são ambientes separados que se ligam por uma relação de confiança (tenant). Depois dela, recursos como o catálogo de APIs aparecem na org.",
         contexto_tecnico=afirm("Plataforma própria: a ligação com a org exige trocar chaves entre o administrador do Anypoint Platform e o da Salesforce.",
                                "Os tipos do Anypoint Platform não são metadata types da Metadata API (critério X1 do escopo).",
                                ["src:help-mulesoft-anypoint-connection"]),
         licencas=lic("Licenças não registradas.", [], estado="desconhecido"),
         funcs=[],
         evid=["src:help-mulesoft-anypoint-connection"]),
    dict(id="nuv:slack", nome_oficial="Slack", aliases=["Salesforce for Slack"], sigla="SLK", categoria="plataforma_propria",
         resumo="Plataforma de comunicação em canais. O workspace do Slack é separado da org e se conecta a ela por apps, como Salesforce for Slack.",
         o_que_e="A integração é habilitada no Setup (Slack Apps Setup) e exige, na maioria dos apps, a permissão Connect Salesforce with Slack. Um workspace pode se conectar a várias orgs.",
         contexto_tecnico=afirm("Plataforma própria: o workspace do Slack é administrado no Slack, e a conexão com a org é feita pelos apps de integração.",
                                "Os tipos do Slack não são metadata types da Metadata API (critério X1 do escopo).",
                                ["src:help-slack-enable", "src:help-slack-connect-org"]),
         licencas=lic("Licenças não registradas; a permissão Connect Salesforce with Slack vale em licenças Salesforce suportadas.", [], estado="desconhecido"),
         funcs=[],
         evid=["src:help-slack-enable", "src:help-slack-connect-org"]),
]

ids = []
for n in NUVENS:
    nome = n["id"].split(":", 1)[1]
    d = {"id": n["id"], "nome_oficial": n["nome_oficial"], "aliases": n["aliases"], "sigla": n["sigla"], "categoria": n["categoria"],
         "resumo": n["resumo"], "o_que_e": n["o_que_e"], "contexto_tecnico": n["contexto_tecnico"], "licencas": n["licencas"],
         "classificacoes_aplicaveis": classificacoes(n["funcs"]),
         "limites": ["Sem inventário de metadata types desta nuvem no MVP; aparecem só as funcionalidades já cadastradas."],
         "cobertura_inventario": "nao_iniciada", "estado": "verificado", "evidencias": [ev(s) for s in n["evid"]]}
    sv(f"nuvens/{nome}.json", d)
    ids.append(n["id"])

# Platform/Core: nome atual
p = ld("nuvens/platform-core.json")
p["nome_oficial"] = "Agentforce 360 Platform"
p["aliases"] = ["Salesforce Platform"] + [a for a in p.get("aliases", []) if a not in ("Salesforce Platform", "Agentforce 360 Platform")]
p["categoria"] = "na_org"
p["limites"] = [x for x in p["limites"] if not x.startswith("'Salesforce Platform' é o nome de uma licença")] + [
    "O nome atual do produto é Agentforce 360 Platform; a licença de usuário continua se chamando Salesforce Platform na Ajuda. Usar o nome para a camada compartilhada é escolha didática do projeto."]
if not any(e["fonte"] == "src:prod-agentforce-360-platform" for e in p["evidencias"]):
    p["evidencias"].append(ev("src:prod-agentforce-360-platform"))
sv("nuvens/platform-core.json", p)
for nid, cat in (("sales-cloud", "na_org"), ("service-cloud", "na_org"), ("data-360", "na_org")):
    d = ld(f"nuvens/{nid}.json"); d["categoria"] = cat; sv(f"nuvens/{nid}.json", d)

sf = ld("salesforce.json")
sf["nuvens"] = [x for x in sf["nuvens"] if x not in ids] + ids
sv("salesforce.json", sf)
print("lote 7w:", len(ids), "nuvens novas; Platform/Core renomeado para Agentforce 360 Platform")
