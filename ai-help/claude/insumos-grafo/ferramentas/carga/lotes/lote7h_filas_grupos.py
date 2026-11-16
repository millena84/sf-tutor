"""Lote 7h (pedido da autora, 2026-11-16; issue #34): filas (queues) e public groups, com metadata types e objetos API.

Lê o guia versionado 264.0 (API 68.0): metadata types Queue (7 estruturas) e Group; objetos API Group, GroupMember e
QueueSobject. Cria as funcionalidades filas e public-groups e liga o que já existia (regras de atribuição, Omni-Channel,
Chatter, pastas de relatórios).

Ordem: lote7g_relatorios_qualidade.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7h_filas_grupos.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga import obj as O                    # noqa: E402
from carga.base import af, ev, ld, caminho    # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-16"
EXTR = "fontes/extracoes/lote7h-filas-grupos.txt"
ATLAS = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"


def substituir_fontes(novas):
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


substituir_fontes(
    [C.fonte(f"src:mdapi-{n.lower()}", f"{n} (Metadata API)", ATLAS + f"meta_{n.lower()}.htm", f"Arquivo, versão e propriedades do tipo {n}.", EXTR, DATA)
     for n in ("Queue", "Group")]
    + [C.fonte_objref(n, EXTR, DATA) for n in ("Group", "GroupMember", "QueueSobject")])
S_Q, S_G = "src:mdapi-queue", "src:mdapi-group"
S_OG, S_OGM, S_OQS = "src:objref-group", "src:objref-groupmember", "src:objref-queuesobject"

NOTA_COB = "Universo esperado = tabelas Fields da página do guia versionado 264.0 (API 68.0), lida em 2026-11-16."
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
B, S = "boolean", "string"
REGISTRADOS = []


def estrutura(nome, src, usada_por, rows, o_que_e):
    M.struct(nome, src, usada_por, rows, o_que_e)
    REGISTRADOS.append((src, "estruturas", nome))


def tipo(nome, src, *a, **k):
    M.mdt(nome, src, *a, **k)
    REGISTRADOS.append((src, "metadata-types", nome))


# ================================================================ Queue (metadata type)
for nome, campo, desc, o_que_e in (
        ("PublicGroups", "publicGroup", "Um public group.", "Public groups usados para dar membros a uma fila."),
        ("RoleAndSubordinates", "roleAndSubordinate", "Um papel com os subordinados, incluindo papéis de clientes e parceiros. Exige digital experiences.",
         "Papéis com subordinados (inclusive de clientes e parceiros) usados para dar membros a uma fila."),
        ("RoleAndSubordinatesInternal", "roleAndSubordinateInternal", "Um papel com os subordinados, sem papéis de clientes e parceiros.",
         "Papéis internos com subordinados usados para dar membros a uma fila."),
        ("Roles", "role", "Um papel.", "Papéis usados para dar membros a uma fila."),
        ("Users", "user", "Um usuário, indicado pelo username.", "Usuários incluídos diretamente como membros de uma fila.")):
    estrutura(nome, S_Q, ["mdx:QueueMembers"], [P(campo, S, None, desc)], o_que_e)
estrutura("QueueMembers", S_Q, ["mdt:Queue"], [
    P("publicGroups", "PublicGroups[]", None, "Public groups cujos membros entram na fila.", estrutura="PublicGroups"),
    P("roleAndSubordinates", "RoleAndSubordinates[]", None, "Papéis e subordinados, inclusive papéis de clientes e parceiros.", estrutura="RoleAndSubordinates",
      notas=["O segundo exemplo XML da página usa queueRoleAndSubordinates e queueRoleAndSubordinate, nomes que não constam da tabela."]),
    P("roleAndSubordinatesInternal", "RoleAndSubordinatesInternal[]", None, "Papéis internos e subordinados, sem papéis de clientes e parceiros.",
      estrutura="RoleAndSubordinatesInternal"),
    P("roles", "Roles[]", None, "Papéis cujos usuários entram na fila.", estrutura="Roles"),
    P("users", "Users[]", None, "Usuários incluídos diretamente.", estrutura="Users"),
], "Os membros de uma fila: incluídos diretamente ou por papéis e public groups.")
estrutura("QueueSobject", S_Q, ["mdt:Queue"], [
    P("sobjectType", S, None, "Objeto que a fila aceita.", vals=[
        ("Case", None), ("ContactRequest", None), ("Lead", None), ("ServiceContract", "Só com Entitlements habilitado."), ("Task", "Desde a API 48.0.")],
      contexto="A página lista estes valores e aceita também objetos customizados.", completa="nao"),
], "Um objeto cujos registros a fila pode receber.")
tipo("Queue", S_Q,
     "Uma fila (queue): um lugar para guardar registros que ainda não têm um dono individual, com os objetos que ela aceita e os membros que podem assumi-los.",
     "Versionar e implantar as filas da org, com objetos e membros.", "24.0", [
         P("doesIncludeBosses", B, "67.0", "Indica se os registros da fila também são compartilhados com os papéis acima na hierarquia.", "S"),
         P("doesSendEmailToMembers", B, None, "Indica se os membros recebem e-mail quando um registro entra na fila."),
         P("email", S, None, "Endereço de e-mail do dono da fila."),
         P("fullName", S, None, "Nome de API da fila; aparece no primeiro exemplo XML da página, não na tabela de campos.", "?"),
         P("name", S, None, "Nome da fila; na interface, é o Label.", "S"),
         P("queueMembers", "QueueMembers[]", "42.0", "Membros da fila, incluídos diretamente ou por papéis e public groups.", estrutura="QueueMembers"),
         P("queueRoutingConfig", S, "42.0", "Nome da routing configuration, em orgs com Omni-Channel."),
         P("queueSobject", "QueueSobject[]", None, "Objetos que a fila aceita.", estrutura="QueueSobject"),
     ], exemplo=CAB + f"""<Queue {NS}>
    <doesIncludeBosses>false</doesIncludeBosses>
    <doesSendEmailToMembers>true</doesSendEmailToMembers>
    <email>[endereço de e-mail da fila]</email>
    <name>[nome da fila]</name>
    <queueMembers>
        <publicGroups>
            <publicGroup>[nome de um public group]</publicGroup>
        </publicGroups>
        <roles>
            <role>[nome de um papel]</role>
        </roles>
        <users>
            <user>[username]</user>
        </users>
    </queueMembers>
    <queueSobject>
        <!-- Valores documentados: Case, ContactRequest, Lead, ServiceContract, Task e objetos customizados -->
        <sobjectType>Case</sobjectType>
    </queueSobject>
</Queue>""", estende="não declarado na página", curinga=True,
     alertas=["Segundo a página, a fila aceita casos, leads, service contracts (com Entitlements habilitado) e objetos customizados; a lista de "
              "valores de sobjectType traz ainda ContactRequest e Task.",
              "Desde o Summer '20, só usuários autenticados, internos e externos, acessam este tipo.",
              "doesIncludeBosses existe para filas só desde a API 67.0."],
     divergencias=["O segundo exemplo XML da página usa os elementos queueRoleAndSubordinates e queueRoleAndSubordinate; a tabela documenta "
                   "roleAndSubordinates e roleAndSubordinate. Foram cadastrados os nomes da tabela.",
                   "O mesmo exemplo fecha o elemento publicGroups com uma tag de abertura."],
     cobertura_nota=NOTA_COB + " A página não informa obrigatoriedade para a maioria dos campos.")

# ================================================================ Group (metadata type)
tipo("Group", S_G,
     "Um public group: um conjunto que pode reunir usuários, papéis e outros grupos, usado para compartilhar registros e dar acesso.",
     "Versionar e implantar os public groups da org.", "24.0", [
         P("description", S, "62.0", "Texto que descreve o grupo."),
         P("doesIncludeBosses", B, "18.0", "Indica se o acesso dado ao grupo sobe pela hierarquia de papéis. Corresponde à caixa Grant Access Using Hierarchies.", "S"),
         P("fullName", S, None, "Nome único de API: letras, números e sublinhados, começando por letra. Corresponde a Group Name. Herdado.", "?", herdada="Metadata"),
         P("name", S, None, "Nome do grupo; na interface, é o Label.", "S"),
     ], exemplo=CAB + f"""<Group {NS}>
    <doesIncludeBosses>true</doesIncludeBosses>
    <fullName>[Nome_Do_Grupo]</fullName>
    <name>[rótulo do grupo]</name>
</Group>""", curinga=True,
     alertas=["Os membros do public group NÃO são migrados quando o tipo Group é implantado: o metadado leva só a definição do grupo.",
              "Desde o Spring '20, só usuários autenticados, internos e externos, acessam este tipo.",
              "Este tipo representa public groups. Grupos do Chatter são outro recurso."],
     cobertura_nota=NOTA_COB)
M.emit_structs()
C.marcar_referencia("estruturas", "PublicGroups", "publicGroup", "mdt:Group")

# ================================================================ objetos API
TOOL_D = lambda: O.expo("tooling", "desconhecido", nota="Exposição na Tooling API não verificada.")  # noqa: E731
SEM_VERSAO = "A página não informa a versão de entrada do objeto."
G = "obj:Group"
TIPOS = [("AllCustomerPortal", "Todos os usuários de Customer Portal ou Customer Community Plus."), ("ChannelProgramGroup", "Parceiros de um channel program."),
         ("CollaborationGroup", "Grupo do Chatter."), ("DataAnalytics", "Usuários de Tableau Next e Data 360."),
         ("Manager", "Gerentes diretos e indiretos de um usuário; somente leitura."),
         ("ManagerAndSubordinatesInternal", "Um usuário e seus subordinados diretos e indiretos; somente leitura."),
         ("Organization", "Todos os usuários da org; somente leitura."), ("Participant", "Grupo do Compliant Data Sharing."),
         ("PRMOrganization", "Todos os parceiros, em org com site ou portal de parceiros."), ("Queue", "Os usuários membros de uma fila."),
         ("Regular", "Public group comum."), ("Role", "Os usuários de um papel (UserRole)."),
         ("RoleAndSubordinates", "Os usuários de um papel e dos papéis abaixo dele."),
         ("RoleAndSubordinatesInternal", "Os usuários de um papel interno e dos papéis internos abaixo dele."),
         ("SharingRecordCollGroup", "Grupo com acesso a uma SharingRecordCollection."), ("Territory", "Os usuários de um território."),
         ("TerritoryAndSubordinates", "Os usuários de um território e dos que ficam abaixo dele.")]
grp = [
    O.field(G, "Description", "textarea", "CFNSU", "62.0", "Descrição do grupo.", S_OG),
    O.field(G, "DefaultDivision", "picklist", "CDFGRSU", None, "Division padrão do registro; só vale com divisions habilitadas.", S_OG),
    O.field(G, "DeveloperName", "string", "CFGNSU", "24.0", "Nome único de API do grupo. Visível só a usuários internos.", S_OG,
            notas=["A página recomenda informá-lo em cargas grandes de dados, para evitar lentidão."]),
    O.field(G, "DoesIncludeBosses", "boolean", "CDFGSU", "18.0",
            "Indica se o acesso sobe para os papéis acima na hierarquia (Grant Access Using Hierarchies). Em filas, existe desde a API 67.0.", S_OG,
            notas=["Em grupos comuns, o padrão é true; em filas, o padrão depende de uma configuração da org."]),
    O.field(G, "DoesSendEmailToMembers", "boolean", "CDFGSU", None, "Indica se os membros do grupo recebem e-mail; vale também para membros de filas.", S_OG),
    O.field(G, "Email", "email", "CFGNSU", None, "Endereço de e-mail do grupo; só se aplica a filas de casos.", S_OG),
    O.field(G, "Name", "string", "CFGISU", None, "Nome do grupo; na interface, é o Label.", S_OG, req=("sim", None)),
    O.field(G, "OwnerId", "reference", "FGS", None, "Usuário dono do grupo.", S_OG, ref=["Organization", "obj:User"], rel="Owner"),
    O.field(G, "QueueRoutingConfigId", "reference", "CU", None, "Routing configuration ligada à fila.", S_OG, ref=["obj:QueueRoutingConfig"],
            notas=["A página lista para este campo as propriedades Create, Delete, Query, Retrieve e Update; só Create e Update foram mapeadas."]),
    O.field(G, "RelatedId", "reference", "FGNS", None, "Registro associado ao grupo; num grupo do tipo Role, é o Id do UserRole.", S_OG,
            ref=["obj:User", "UserRole"], rel="Related"),
    O.field(G, "Type", "picklist", "CFGRS", None, "Tipo do grupo. É este campo que distingue um public group (Regular) de uma fila (Queue) e dos "
            "grupos criados pela plataforma.", S_OG, vals=[v for v, _ in TIPOS], completa="desconhecido", req=("sim", None),
            contexto="Valores da página. Ao criar um grupo, só Regular e Queue (e Personal, citado sem descrição) podem ser usados; os demais são reservados.",
            notas=[f"{v}: {d}" for v, d in TIPOS]),
]
O.obj("Group",
      "Um conjunto de usuários. O mesmo objeto guarda public groups, filas e os grupos que a plataforma cria para papéis, territórios e gerentes; "
      "o campo Type diz qual é qual.",
      "Consultar por API os public groups e as filas da org, e criar ou alterar os dois.",
      [O.expo("padrao", "verificado", S_OG, ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "search()",
                                             "retrieve()", "update()", "upsert()"],
              acesso="Usuários autenticados, internos e externos, acessam o objeto.", nota=SEM_VERSAO), TOOL_D()],
      grp,
      [{"api": "padrao", "soql": "SELECT Name, DeveloperName, Type FROM Group WHERE Type = 'Queue'",
        "contexto": "API padrão. Lista as filas da org; com Type = 'Regular', lista os public groups.", "validacao": "documental"}],
      O.APEX_OK(S_OG), O.cob("completa", 11, 11, O.cnt(grp), "Tabela de campos lida completa (11); Id e campos de sistema não constam."), S_OG,
      alertas=["Só public groups são acessíveis pela API; personal groups, não.",
               "Excluir um public group funciona mesmo que ele seja usado em compartilhamento (desde a API 13.0).",
               "A página é inconsistente sobre quais valores de Type podem ser usados ao criar um grupo."])

GM = "obj:GroupMember"
gm = [
    O.field(GM, "GroupId", "reference", "CFGS", None, "O grupo.", S_OGM, ref=["obj:Group"], rel="Group", req=("sim", None)),
    O.field(GM, "UserOrGroupId", "reference", "CFGS", None, "O membro direto: um usuário ou outro grupo.", S_OGM, ref=["obj:Group", "obj:User"],
            rel="UserOrGroup", req=("sim", None)),
]
O.obj("GroupMember",
      "Um membro direto de um public group: um usuário ou outro grupo. Cada registro liga um grupo a um membro.",
      "Consultar e alterar por API quem participa de cada public group.",
      [O.expo("padrao", "verificado", S_OGM, ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()"],
              nota=SEM_VERSAO), TOOL_D()],
      gm,
      [{"api": "padrao", "soql": "SELECT GroupId, UserOrGroupId FROM GroupMember", "contexto": "API padrão. Lista os membros diretos dos grupos.",
        "validacao": "documental"}],
      O.APEX_OK(S_OGM), O.cob("completa", 2, 2, O.cnt(gm), "Tabela de campos lida completa (2); Id não consta."), S_OGM, juncao=True,
      alertas=["Só há registro para membros DIRETOS de public groups do tipo Regular; membros indiretos não aparecem.",
               "Não há update(): para trocar um membro, exclui-se o registro e cria-se outro.",
               "Criar um registro igual a um existente devolve o existente, sem erro.",
               "Para grupos com mais de 10.000 membros, a página recomenda gerir os membros por este objeto."])

QS = "obj:QueueSobject"
qs = [
    O.field(QS, "QueueId", "reference", "CFGS", None, "A fila (um Group com Type igual a Queue).", S_OQS, ref=["obj:Group"], rel="Queue"),
    O.field(QS, "SobjectType", "picklist", "CFGRS", None, "Tipo de objeto que pode ser ligado à fila.", S_OQS,
            notas=["A página do objeto não lista os valores."]),
]
O.obj("QueueSobject",
      "A ligação entre uma fila e um tipo de objeto que ela aceita, inclusive objetos customizados. Cada registro é um par fila e objeto.",
      "Consultar e alterar por API quais objetos cada fila aceita.",
      [O.expo("padrao", "verificado", S_OQS, ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()"],
              acesso="Desde o Summer '20, só usuários autenticados, internos e externos. Criar um Group exige a permissão Manage Users.",
              restr=["Pela Bulk API, não é possível inserir ou atualizar mais de 18 filas de uma vez."], nota=SEM_VERSAO), TOOL_D()],
      qs,
      [{"api": "padrao", "soql": "SELECT QueueId, SobjectType FROM QueueSobject WHERE SobjectType = 'Case'",
        "contexto": "API padrão. Lista as filas que aceitam casos.", "validacao": "documental"}],
      O.APEX_OK(S_OQS), O.cob("completa", 2, 2, O.cnt(qs), "Tabela de campos lida completa (2); Id não consta."), S_OQS, juncao=True)

C.rel_lookup("groupmember-group", GM, "GroupId", G, "Cada membro pertence a um grupo.", S_OGM)
C.rel_lookup("groupmember-membro-grupo", GM, "UserOrGroupId", G, "O membro pode ser outro grupo (grupo dentro de grupo).", S_OGM)
C.rel_lookup("groupmember-membro-usuario", GM, "UserOrGroupId", "obj:User", "O membro pode ser um usuário.", S_OGM)
C.rel_lookup("queuesobject-group", QS, "QueueId", G, "Cada par fila e objeto aponta para a fila, que é um Group do tipo Queue.", S_OQS)
C.rel_lookup("group-queueroutingconfig", G, "QueueRoutingConfigId", "obj:QueueRoutingConfig", "Uma fila do Omni-Channel aponta para a sua routing configuration.", S_OG)
C.rel_representacao_comum("queue-group", "mdt:Queue", G, "Uma fila é, nos dados, um Group com Type igual a Queue.", [S_Q, S_OQS])
C.rel_representacao_comum("group-group", "mdt:Group", G, "Um public group é, nos dados, um Group com Type igual a Regular.", [S_G, S_OG])
C.rel_referencia("queue-group-membros", "mdx:PublicGroups", "publicGroup", "mdt:Group", "Uma fila pode receber como membros os de um public group.", S_Q)

# ================================================================ nota de extração: lista de campos
linhas = ["", "-- Lista de campos transcrita da leitura (gerada por lote7h_filas_grupos.py; nome | tipo | desde)"]
for src, pasta, nome in REGISTRADOS:
    props = ld(f"{pasta}/{nome}.json")["propriedades"]
    linhas.append(f"[{src}] {nome}: " + ", ".join(f"{q['nome']} | {q['tipo_tecnico']} | {q.get('desde_versao') or '-'}" for q in props))
for src, nome, campos in ((S_OG, "Group", grp), (S_OGM, "GroupMember", gm), (S_OQS, "QueueSobject", qs)):
    linhas.append(f"[{src}] objeto {nome}: " + ", ".join(f"{c['nome']} | {c['tipo_tecnico']}" for c in campos))
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(linhas) + "\n")

# ================================================================ funcionalidades
ACE, AUT, PRO, REL, CON = ("acesso-identidade-e-seguranca", "automacao-de-processos-e-regras-de-negocio", "processos-de-negocio-especificos-de-produto",
                           "relatorios-analytics-e-exploracao", "conteudo-conhecimento-e-colaboracao")


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


C.funcionalidade(
    "filas", "Filas (queues)", "Queues", ["queue", "fila", "queues", "queue members", "fila de casos", "fila de leads", "dono do registro"],
    "Uma fila guarda registros que ainda não têm um dono individual, para que um time divida o trabalho: os registros aparecem numa lista e "
    "qualquer membro pode assumir um deles. Cada fila diz quais objetos aceita e quem são os membros: usuários, papéis, public groups e outros.",
    "Distribuir trabalho a um time sem atribuir cada registro a uma pessoa na entrada.",
    "Os casos novos vão para a fila Suporte Nível 2; um atendente do time abre a lista da fila e assume o próximo caso.",
    (ACE, "acesso-a-registros-e-hierarquias"),
    [(PRO, "atendimento", "Casos são distribuídos por filas, e o Omni-Channel roteia o trabalho a partir delas."),
     (PRO, "vendas", "Leads podem ficar numa fila até alguém assumi-los.")],
    [("Queue", "Cada fila, com os objetos aceitos e os membros.")],
    [("Group", "A fila nos dados: um Group com Type igual a Queue."), ("QueueSobject", "Os objetos que cada fila aceita."),
     ("GroupMember", "Membros diretos de grupos; a página documenta o registro para public groups do tipo Regular.")],
    [S_Q, S_OG, S_OQS, S_OGM, "src:help-queues-create", "src:help-queues-omni", "src:help-queues-action-plans", "src:help-queues-lead-distribution",
     "src:help-sharing-rule-categories"], [],
    setup("Setup > Quick Find: Queues > Queues", "src:help-queues-create", "Lista das filas; New cria uma fila."),
    alertas=["Criar ou alterar filas exige as permissões Customize Application e Manage Public List Views.",
             "Criar uma fila cria junto uma list view; o rótulo da fila é o nome da list view em que os usuários trabalham.",
             "O nome de uma fila não pode conter vírgulas.",
             "Em sharing rules, a categoria Queues cobre os registros cujo dono é a fila, não os registros dos membros dela.",
             "Fila e public group são o mesmo objeto nos dados (Group); o campo Type os distingue."])
C.ampliar_funcionalidade("omni-channel", mdts=[("Queue", "A fila de onde o Omni-Channel roteia o trabalho; aponta a routing configuration.")],
                         objs=[("Group", "A fila, com QueueRoutingConfigId.")], srcs=[S_Q, "src:help-queues-omni"])

C.funcionalidade(
    "public-groups", "Public groups", "Public Groups", ["public group", "grupo público", "group", "grupo", "group member", "personal group",
                                                        "grant access using hierarchies"],
    "Um public group reúne usuários, papéis, outros grupos e demais tipos de membro, para que um conjunto de pessoas que não cabe num único "
    "papel receba o mesmo acesso. Serve de alvo para sharing rules, pastas de relatórios e dashboards, list views e membros de filas.",
    "Compartilhar registros e recursos com um conjunto de pessoas sem criar uma regra para cada uma.",
    "O grupo Comitê de Preços reúne dois papéis de vendas e três pessoas do financeiro; uma sharing rule dá a ele acesso às oportunidades grandes.",
    (ACE, "permissoes-perfis-e-grupos"),
    [(ACE, "acesso-a-registros-e-hierarquias", "Public groups são alvo de sharing rules."),
     (REL, "pastas-e-acesso", "Pastas de relatórios e dashboards são compartilhadas com public groups.")],
    [("Group", "A definição de cada public group (sem os membros).")],
    [("Group", "O public group nos dados: um Group com Type igual a Regular."), ("GroupMember", "Os membros diretos de cada public group.")],
    [S_G, S_OG, S_OGM, "src:help-public-groups", "src:help-public-groups-create", "src:help-group-member-types", "src:help-public-groups-considerations",
     "src:help-public-group-summary", "src:help-sharing-rules", "src:help-sharing-rule-categories", "src:help-public-groups-knowledge"], [],
    setup("Setup > Quick Find: Public Groups > Public Groups", "src:help-public-groups-knowledge", "Lista dos public groups; New cria um grupo."),
    limitacoes=["Com mais de 10.000 membros, editar o grupo pela página de criação ou edição pode ficar lento ou perder membros; a Ajuda manda usar "
                "o access summary do grupo, user access policies ou a API de GroupMember.",
                "A Ajuda recomenda não passar de cinco níveis de grupos dentro de grupos."],
    alertas=["Implantar o metadata type Group NÃO leva os membros: eles precisam ser carregados à parte (objeto GroupMember).",
             "Criar ou editar um public group exige a permissão Manage Users.",
             "Com Grant Access Using Hierarchies marcado, o que é compartilhado com o grupo também chega a quem está acima na hierarquia de papéis.",
             "Editar grupos, papéis e territórios faz as sharing rules serem recalculadas.",
             "Há dois tipos de grupo: public groups, criados por administradores, e personal groups; só os public groups são acessíveis pela API.",
             "Grupo do Chatter é outro recurso: no objeto Group, aparece com Type igual a CollaborationGroup."])
C.ampliar_funcionalidade("chatter", objs=[("Group", "Um grupo do Chatter aparece no objeto Group com Type igual a CollaborationGroup.")], srcs=[S_OG])
C.ampliar_funcionalidade("pastas-de-relatorios-e-dashboards", srcs=["src:help-public-group-summary"],
                         alertas=["O access summary de um public group mostra as pastas de relatórios e dashboards compartilhadas com ele."])
print(f"lote 7h: 2 metadata types, {sum(1 for r in REGISTRADOS if r[1] == 'estruturas')} estruturas e 3 objetos API gravados; 2 funcionalidades novas e 3 ampliadas")
