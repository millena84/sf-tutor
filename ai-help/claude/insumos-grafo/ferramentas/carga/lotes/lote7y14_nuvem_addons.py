"""Lote 7y14 (decisão da autora em 2026-11-21): nó didático "Add-ons" com a funcionalidade Salesforce Scheduler.

- cataloga AppointmentSchedulingPolicy e AppointmentAssignmentPolicy (páginas 264.0 lidas por inteiro);
- cria func:salesforce-scheduler (principal em Atendimento; secundária em Capacidades setoriais);
- cria nuv:add-ons com natureza = "agrupamento_didatico" (não é nome nem nuvem oficial da Salesforce) e a inclui no centro do mapa;
- no escopo da #10, os dois tipos deixam Industries (inferido) e passam a apontar para nuv:add-ons, sem inferência.
Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv, ev, af       # noqa: E402
from carga import catalogo as C             # noqa: E402
from carga.mdt import mdt, P, emit_structs   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = "2026-11-21"
EXTR = "fontes/extracoes/lote7y14-nuvem-addons-scheduler.txt"
G = "https://developer.salesforce.com/docs/get_document_content/api_meta/"
SASP, SAAP, SINT = "src:mdapi-appointmentschedulingpolicy", "src:mdapi-appointmentassignmentpolicy", "src:scheduler-dev-intro"

C.registrar_fontes([
    C.fonte(SASP, "AppointmentSchedulingPolicy (Metadata API 264.0)", G + "meta_appointmentschedulingpolicy.htm/en-us/264.0",
            "Arquivo, versão, acesso e os 15 campos do tipo (leitura completa).", EXTR, DATA),
    C.fonte(SAAP, "AppointmentAssignmentPolicy (Metadata API 264.0)", G + "meta_appointmentassignmentpolicy.htm/en-us/264.0",
            "Arquivo, versão e os 4 campos do tipo (leitura completa).", EXTR, DATA),
    C.fonte(SINT, "Salesforce Scheduler Developer Guide: Introduction to Salesforce Scheduler",
            "https://developer.salesforce.com/docs/atlas.en-us.salesforce_scheduler_developer_guide.meta/salesforce_scheduler_developer_guide/intro_rate_limits.htm",
            "O que é o Salesforce Scheduler (antes Lightning Scheduler) e o que se configura antes de usar.", EXTR, DATA,
            versao="sem versão na URL", metodo="leitura_resultado_busca"),
])

B = dict(vals=[("true", None), ("false", None)])
INTERVALOS = [(v, None) for v in "5 10 15 20 30 45 60 90 120 150 180 240 300 360 420 480".split()]
mdt("AppointmentSchedulingPolicy", SASP,
    "Política de agendamento do Salesforce Scheduler: as regras que decidem quais horários e quais recursos aparecem ao marcar um compromisso.",
    "Recuperar e implantar as regras de agendamento entre ambientes, em vez de recriá-las à mão.", "47.0", [
        P("appointmentAssignmentPolicy", "string", "53.0", "Nome da política de atribuição de compromissos (AppointmentAssignmentPolicy) usada por esta política."),
        P("appointmentStartTimeInterval", "picklist", None, "Minutos entre os horários de início propostos; com 15, os inícios caem na hora cheia e a cada 15 minutos.",
          "S", vals=INTERVALOS),
        P("extCalEventHandler", "lookup", "50.0", "Nome de API da classe Apex que consulta os eventos de calendário externo dos recursos e devolve os horários já ocupados.",
          "S", natureza="referencia", contexto="Nome de API de uma classe Apex da org."),
        P("isSvcTerritoryMemberShiftUsed", "boolean", "54.0", "Indica se os turnos dos membros do território de serviço contam para a disponibilidade do recurso.", "S"),
        P("isSvcTerrOpHoursWithShiftsUsed", "boolean", "54.0", "Indica se a disponibilidade usa a interseção entre os turnos e o horário de funcionamento do território de serviço.", "S"),
        P("masterLabel", "string", None, "Rótulo da política de agendamento.", "S"),
        P("shouldCheckExternalCalendar", "boolean", "53.0", "Indica se calendários externos são consultados para saber a disponibilidade dos recursos.", "S"),
        P("shouldConsiderCalendarEvents", "boolean", None, "Indica se eventos do calendário Salesforce afetam a disponibilidade dos recursos.", "S"),
        P("shouldEnforceExcludedResource", "boolean", None, "Indica se recursos de serviço marcados como excluídos ficam impedidos de receber compromissos.", "S"),
        P("shouldEnforceRequiredResource", "boolean", None, "Indica se só recursos de serviço obrigatórios podem ser atribuídos aos compromissos.", "S"),
        P("shouldMatchSkill", "boolean", None, "Indica se só recursos obrigatórios com determinadas habilidades podem ser atribuídos.", "S"),
        P("shouldMatchSkillLevel", "boolean", None, "Indica se só recursos obrigatórios com determinadas habilidades e níveis de habilidade podem ser atribuídos.", "S"),
        P("shouldRespectVisitingHours", "boolean", None, "Indica se fica bloqueado agendar fora do horário de visita da conta.", "S"),
        P("shouldUsePrimaryMembers", "boolean", None, "Indica se só membros primários do território de serviço podem ser atribuídos.", "S"),
        P("shouldUseSecondaryMembers", "boolean", None, "Indica se membros secundários do território de serviço podem ser atribuídos.", "S"),
    ],
    cobertura_nota="Universo esperado = tabela Fields da página 264.0 (15 campos), lida por inteiro em 2026-11-21. A leitura não registrou se a página declara fullName herdado; por isso ele não entrou.",
    curinga=True,
    alertas=["Acesso: a página exige as permissões ViewSetup e CustomizeApplication.",
             "Licença: habilitar o Salesforce Scheduler pede a licença Lightning Scheduler Add-On (fonte de Health Cloud, ver a funcionalidade)."],
    exemplo="""<?xml version="1.0" encoding="UTF-8"?>
<AppointmentSchedulingPolicy xmlns="http://soap.sforce.com/2006/04/metadata">
    <masterLabel>Politica padrao</masterLabel>
    <appointmentStartTimeInterval>15</appointmentStartTimeInterval>
    <shouldConsiderCalendarEvents>true</shouldConsiderCalendarEvents>
    <shouldMatchSkill>false</shouldMatchSkill>
</AppointmentSchedulingPolicy>""")

mdt("AppointmentAssignmentPolicy", SAAP,
    "Política de atribuição de compromissos: a regra que distribui os compromissos entre os recursos de serviço para equilibrar a carga.",
    "Recuperar e implantar a regra de distribuição entre ambientes; ela é usada por uma política de agendamento.", "53.0", [
        P("masterLabel", "string", None, "Rótulo da política de atribuição.", "S"),
        P("policyApplicableDuration", "string", None, "Com que frequência a utilização dos recursos de serviço é calculada.", "S",
          vals=[("Monthly", "mensal"), ("ParameterBased", "conforme parâmetro"), ("Weekly", "semanal")]),
        P("policyType", "string", None, "Tipo da política de atribuição; a página dá um único valor.", "S", vals=[("loadBalancing", "balanceamento de carga")]),
        P("utilizationFactor", "string", None, "O que se conta para medir a utilização do recurso.", "S",
          vals=[("NumberOfAppointments", "número de compromissos"), ("TotalAppointmentDuration", "duração total dos compromissos")]),
    ],
    exemplo="""<?xml version="1.0" encoding="UTF-8"?>
<AppointmentAssignmentPolicy xmlns="http://soap.sforce.com/2006/04/metadata">
    <masterLabel>Distribuicao semanal</masterLabel>
    <policyApplicableDuration>Weekly</policyApplicableDuration>
    <policyType>loadBalancing</policyType>
    <utilizationFactor>NumberOfAppointments</utilizationFactor>
</AppointmentAssignmentPolicy>""",
    cobertura_nota="Universo esperado = tabela Fields da página 264.0 (4 campos), lida por inteiro em 2026-11-21. A leitura não registrou se a página declara fullName herdado; por isso ele não entrou.",
    curinga=True)
emit_structs()

C.funcionalidade(
    "salesforce-scheduler", "Salesforce Scheduler", "Salesforce Scheduler", ["Lightning Scheduler", "agendamento de compromissos"],
    "Add-on para agendar compromissos com clientes, presenciais, por telefone ou por vídeo, com a pessoa, o local e o horário certos.",
    "Montar a agenda de atendimento: quem atende (recursos de serviço), onde (territórios), sobre o quê (grupos e tipos de trabalho) e com quais regras.",
    "Um banco deixa o cliente marcar, pelo site, uma conversa sobre financiamento com um gerente da agência mais próxima; a política de "
    "agendamento oferece só horários de 15 em 15 minutos e só gerentes com a habilidade certa.",
    ("processos-de-negocio-especificos-de-produto", "atendimento"),
    [("processos-de-negocio-especificos-de-produto", "capacidades-setoriais",
      "As fontes lidas mostram o Scheduler usado com nuvens de setor, como Health Cloud e Financial Services Cloud.")],
    [("AppointmentSchedulingPolicy", "Regras de agendamento (horários propostos, habilidades, territórios, calendários)."),
     ("AppointmentAssignmentPolicy", "Regra de distribuição dos compromissos entre os recursos (balanceamento de carga).")],
    [], [SINT, "src:hc-scheduler-addon", SASP, SAAP],
    [{"tipo": "objeto_api", "estado": "desconhecido",
      "motivo": "Objetos usados pelo Scheduler (territórios, recursos, tipos de trabalho, compromissos) não foram cadastrados neste lote; a lista vazia não comprova inexistência."}],
    af("desconhecido", None, "Caminho no Setup não validado nesta sessão."),
    alertas=["Exige a licença Lightning Scheduler Add-On para ser habilitado (fonte do guia de Health Cloud)."],
    pre=["Licença Lightning Scheduler Add-On."])

NOTA_NAT = ("\"Add-ons\" é um agrupamento criado por este tutorial para reunir add-ons que servem a várias nuvens e não têm nó próprio no mapa. "
            "Não é um produto nem uma nuvem oficial da Salesforce.")
nuv = {
    "id": "nuv:add-ons", "nome_oficial": "Add-ons", "natureza": "agrupamento_didatico", "nota_natureza": NOTA_NAT,
    "aliases": ["add-ons transversais"], "sigla": "ADD", "categoria": "na_org",
    "resumo": "Agrupamento do tutorial para add-ons que servem a várias nuvens, como o Salesforce Scheduler. Cada add-on tem licença própria.",
    "o_que_e": "Reúne produtos vendidos como add-on, que rodam na org e são usados com mais de uma nuvem, sem pertencer a uma só. Por enquanto, só o Salesforce Scheduler.",
    "contexto_tecnico": af("verificado", "O Salesforce Scheduler roda na org: usa territórios, recursos e tipos de trabalho da própria org, com APIs REST, Connect REST, Platform Events e Apex.",
                           "Vale para o Scheduler; outros add-ons serão descritos quando entrarem.", [ev(SINT)]),
    "licencas": {"estado": "verificado", "nota": "Cada add-on do agrupamento tem a sua licença; preços não são registrados.",
                 "itens": [{"nome": "Lightning Scheduler Add-On (Salesforce Scheduler)", "tipo": "add_on", "evidencias": [ev("src:hc-scheduler-addon")]}]},
    "classificacoes_aplicaveis": [],
    "limites": ["Agrupamento do projeto, não nome oficial.", "Só o Salesforce Scheduler entrou até agora; outros add-ons (como Workforce Engagement) podem entrar depois."],
    "cobertura_inventario": "parcial", "estado": "verificado",
    "evidencias": [ev(SINT), ev("src:hc-scheduler-addon")],
}
p = os.path.join(RAIZ, "catalogo", "nuvens", "add-ons.json")
if os.path.exists(p):
    nuv["classificacoes_aplicaveis"] = json.load(open(p, encoding="utf-8"))["classificacoes_aplicaveis"]
sv("nuvens/add-ons.json", nuv)
C.ligar_nuvem("add-ons", "processos-de-negocio-especificos-de-produto", "atendimento", ["salesforce-scheduler"])

sf = ld("salesforce.json")
if "nuv:add-ons" not in sf["nuvens"]:
    sf["nuvens"].append("nuv:add-ons")
    sv("salesforce.json", sf)

esc_p = os.path.join(RAIZ, "config", "escopo.json")
esc = json.load(open(esc_p, encoding="utf-8"))
just = esc["classificacao_core_por_item"]["justificativas"]
for t in ["AppointmentSchedulingPolicy", "AppointmentAssignmentPolicy"]:
    j = just[t]
    j.pop("inferido", None); j.pop("nota_inferencia", None)
    j.update(nuvens=["nuv:add-ons"], data=DATA,
             motivo="Faz parte do Salesforce Scheduler, que exige a licença Lightning Scheduler Add-On. Fica fora do Core e aparece no mapa no "
                    "nó didático Add-ons (decisão da autora em 2026-11-21).")
json.dump(esc, open(esc_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(esc_p, "a", encoding="utf-8").write("\n")
print("lote 7y14: nuv:add-ons, func:salesforce-scheduler, 2 metadata types")
