"""Issue #34: temas internos que estavam pendentes por falta de fonte (lote 4: Produto).
Fontes lidas pelos resultados de busca restritos aos domínios oficiais: fontes/extracoes/temas-pendentes-lote4.txt.
"Outras áreas" é um agrupamento do projeto; o conteúdo dele se apoia no universo do inventário (src:sdr-metadata-support).
Usado por conteudo_temas.py.
"""
from carga.catalogo import fonte
from conteudo_cls import E, ini, enc, av

DATA = "2026-11-10"
EXT = "fontes/extracoes/temas-pendentes-lote4.txt"
AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")
DOC = dict(versao="sem versão na página", metodo="leitura_resultado_busca")


def F(i, t, u, p, **k):
    return fonte(i, t, u, p, EXT, DATA, **k)


FONTES_PENDENTES4 = [
    # Serviço de campo
    F("src:help-field-service-overview", "Agentforce Field Service and Operations",
      "https://help.salesforce.com/s/articleView?id=service.fs_overview.htm&type=5", "Core features, managed package, app móvel e edições.", **AJ),
    F("src:dev-field-service-core-data-model", "Field Service Core Data Model",
      "https://developer.salesforce.com/docs/service/field-service-dev/guide/fsl-dev-soap-core.html", "Objetos centrais e como se relacionam.", **DOC),
    F("src:help-field-service-objects", "Field Service Objects",
      "https://help.salesforce.com/s/articleView?id=fs_standard_objects.htm&type=0", "Objetos padrão e objetos do managed package.", **AJ),
    F("src:help-field-service-managed-package", "Install the Field Service Managed Package",
      "https://help.salesforce.com/s/articleView?id=pfs_install.htm&type=5", "O que o pacote traz e pré-requisito de Chatter.", **AJ),
    F("src:help-field-service-sharing", "Limit Access to Field Service Records",
      "https://help.salesforce.com/s/articleView?id=service.fs_sharing.htm&type=5", "OWD após instalar o pacote e compartilhamento por território.", **AJ),
    F("src:help-field-service-scheduling-ready", "Get Ready for Field Service Scheduling and Optimization",
      "https://help.salesforce.com/s/articleView?id=service.pfs_customization.htm&type=5", "Enhanced Scheduling and Optimization e scheduling policies.", **AJ),
    F("src:help-field-service-mobile", "Field Service Mobile App",
      "https://help.salesforce.com/s/articleView?id=service.mfs_overview.htm", "Licença e recursos do app móvel.", **AJ),
    # Experiências externas
    F("src:help-experience-cloud-licenses", "Experience Cloud User Licenses",
      "https://help.salesforce.com/s/articleView?id=users_license_types_communities.htm&type=0", "Licenças externas, usos e limites.", **AJ),
    F("src:help-experience-cloud-license-limitations", "Experience Cloud License Limitations",
      "https://help.salesforce.com/s/articleView?id=networks_licenses_limitations.htm&type=0", "Restrições por licença.", **AJ),
    F("src:help-experience-cloud-sharing-sets", "Create a Sharing Set for Experience Cloud Site Users",
      "https://help.salesforce.com/s/articleView?id=sf.networks_setting_light_users.htm&type=5", "Sharing sets e share groups.", **AJ),
    F("src:help-experience-cloud-create-users", "Create Experience Cloud Site Users",
      "https://help.salesforce.com/s/articleView?id=networks_create_external_users.htm&type=5", "Como nasce um usuário externo e permissões.", **AJ),
    F("src:help-experience-cloud-license-upgrades", "Experience Cloud Licenses Eligible for Upgrades",
      "https://help.salesforce.com/s/articleView?id=sf.networks_license_upgrade_eligible.htm&type=5", "Upgrade e downgrade de licenças externas.", **AJ),
    # Capacidades setoriais
    F("src:help-industries-data-models", "Insurance and Financial Services Data Model",
      "https://help.salesforce.com/s/articleView?id=ind.v_data_models_vlocity_insurance_and_financial_services_data_model_667142.htm&type=5",
      "Modelos de dados setoriais como extensão do modelo padrão.", **AJ),
    F("src:help-health-cloud-psl", "View and Assign Health Cloud Permission Sets and Permission Set Licenses",
      "https://help.salesforce.com/s/articleView?id=ind.admin_permissionset_licenses_assign.htm&type=5", "PSLs e permission sets de uma nuvem setorial.", **AJ),
    F("src:dev-health-cloud-clinical-data-model", "Clinical Data Model (Health Cloud Developer Guide)",
      "https://developer.salesforce.com/docs/industries/health-cloud-dev-guide/guide/hc-clinical-data-model.html", "Modelo ligado por preferência da org.", **DOC),
    F("src:help-industry-psl-integration-user", "Health Cloud: Cannot assign Health Cloud permission set licenses to Salesforce Integration license users (KB)",
      "https://help.salesforce.com/s/articleView?id=005385054&type=1", "Licença Salesforce Integration e PSLs setoriais.", **AJ),
]

P = {}
P["sub:servico-de-campo"] = {
    "para_iniciantes": ini("Field Service (hoje Agentforce Field Service and Operations) organiza o trabalho feito na casa ou no local do "
                           "cliente: o que precisa ser feito (work order), a visita marcada (service appointment), quem vai "
                           "(service resource) e onde essa pessoa atua (service territory).",
                           "Um cliente pede conserto do ar-condicionado; nasce uma work order, que gera uma service appointment para "
                           "quinta à tarde, atribuída ao técnico da região.",
                           E("src:help-field-service-overview", "src:dev-field-service-core-data-model")),
    "encadeamento": enc("Costuma vir depois de 'Atendimento': uma work order pode nascer de um case e ligar-se a asset, entitlement e "
                        "service contract. Horários de trabalho usam operating hours, e o acesso aos registros segue 'Acesso a "
                        "registros e hierarquias'.",
                        E("src:dev-field-service-core-data-model", "src:help-field-service-sharing")),
    "avancado": [
        av("decisao", "Core, pacote ou app", "Habilitar Field Service libera os objetos padrão. O managed package acrescenta Guided Setup, "
           "agendamento e otimização, o Classic Dispatch Console e objetos customizados. O app móvel, offline, exige a licença Field Service "
           "Mobile. Os três estão nas edições Enterprise, Unlimited e Developer.",
           E("src:help-field-service-overview", "src:help-field-service-objects", "src:help-field-service-mobile")),
        av("seguranca", "Compartilhamento depois do pacote", "Ao instalar o pacote, Work Order, Work Order Line Item e Service Appointment ficam "
           "Public Read/Write. Para restringir, o User Territories Sharing cria um public group por território e compartilha os appointments com "
           "ele; dispatchers precisam de Read/Write no próprio território.", E("src:help-field-service-sharing")),
        av("atencao", "Pré-requisitos que mudaram", "O pacote pede Chatter ligado, e orgs novas vêm com Chatter desligado. Desde o Summer '23, "
           "orgs novas já têm Enhanced Scheduling and Optimization; orgs antigas precisam aderir.",
           E("src:help-field-service-managed-package", "src:help-field-service-scheduling-ready")),
        av("implantacao", "Como o modelo se encaixa", "Toda service appointment tem um registro pai, em geral a work order ou um line item. Work "
           "types padronizam duração e skill requirements; assigned resource liga o técnico à visita; service territory members dizem onde cada "
           "técnico trabalha.", E("src:dev-field-service-core-data-model")),
    ],
}
P["sub:experiencias-externas"] = {
    "para_iniciantes": ini("Clientes e parceiros acessam a org por sites Experience Cloud usando licenças próprias para usuários externos. "
                           "A licença escolhida define o que a pessoa pode ver e fazer: de abrir casos e ler artigos até trabalhar leads "
                           "e oportunidades como parceiro.",
                           "Clientes com Customer Community abrem casos no portal; revendedores com Partner Community registram "
                           "oportunidades.",
                           E("src:help-experience-cloud-licenses")),
    "encadeamento": enc("Vem depois de montar o site em 'Experiências web/portais e mobile' e se apoia em 'Licenças e entitlements de "
                        "acesso' e 'Acesso a registros e hierarquias', porque o compartilhamento muda conforme a licença.",
                        E("src:help-experience-cloud-licenses", "src:help-experience-cloud-sharing-sets")),
    "avancado": [
        av("decisao", "Qual licença externa", "Customer Community serve B2C em grande volume, com casos e knowledge. Customer Community Plus "
           "acrescenta relatórios, dashboards e compartilhamento padrão. Partner Community é para B2B com dados de vendas e não aceita conta "
           "pessoal. Cada uma tem versão por login.", E("src:help-experience-cloud-licenses", "src:help-experience-cloud-license-limitations")),
        av("seguranca", "Sharing set em vez de sharing rule", "Customer Community não aceita sharing rules; o caminho é o sharing set, que dá "
           "acesso a registros ligados à mesma conta ou contato do usuário e vale em todos os sites dele. Há um sharing set por perfil.",
           E("src:help-experience-cloud-license-limitations", "src:help-experience-cloud-sharing-sets")),
        av("limite", "Sites, papéis e escala", "Em Enterprise, Performance e Unlimited dá para criar até 100 sites sem comprar licença, mas alguns "
           "templates exigem uma (Partner Central pede Partner Community). Customer Community Plus e Partner Community usam papéis, com limite "
           "padrão de 50.000 papéis de portal.", E("src:help-experience-cloud-licenses")),
        av("implantacao", "Criar e trocar usuários", "O usuário externo nasce do contato (Enable Customer User ou Enable Partner User), e a conta "
           "precisa ter dono com papel. Subir de licença remove sharing sets, permission sets e PSLs do usuário; descer exige desabilitar e "
           "reabilitar o contato.", E("src:help-experience-cloud-create-users", "src:help-experience-cloud-license-upgrades")),
    ],
}
P["sub:capacidades-setoriais"] = {
    "para_iniciantes": ini("As nuvens setoriais (como Financial Services Cloud e Health Cloud) acrescentam objetos, campos e recursos "
                           "próprios de um setor sobre o modelo padrão da Salesforce. O acesso vem de permission set licenses, que liberam "
                           "o que a licença de usuário comum não inclui.",
                           "Uma operadora de saúde usa Health Cloud para registrar prestadores e especialidades sem criar objetos "
                           "customizados para isso.",
                           E("src:help-industries-data-models", "src:help-health-cloud-psl")),
    "encadeamento": enc("Parte do modelo padrão estudado em 'Objetos e entidades' e de 'Licenças e entitlements de acesso'. Vendas e "
                        "atendimento comuns a vários setores ficam em 'Vendas' e 'Atendimento'.",
                        E("src:help-industries-data-models", "src:help-health-cloud-psl")),
    "avancado": [
        av("decisao", "Estender em vez de recriar", "Os modelos setoriais são extensões aditivas do modelo padrão: Account, Contact e outros "
           "continuam valendo, e o setor acrescenta objetos e campos.", E("src:help-industries-data-models")),
        av("seguranca", "PSL e permission set juntos", "Cada nuvem define suas PSLs; no Health Cloud, todo usuário interno precisa ao menos da "
           "Health Cloud Platform. Atribuir o permission set atribui junto a PSL correspondente.", E("src:help-health-cloud-psl")),
        av("atencao", "Usuário de integração", "A licença Salesforce Integration não aceita PSLs de nuvens setoriais; um usuário de integração "
           "nessa licença não acessa os objetos do Health Cloud.", E("src:help-industry-psl-integration-user")),
        av("implantacao", "Modelos ligados por preferência", "Partes do modelo podem depender de uma preferência da org: o Clinical Data Model do "
           "Health Cloud é ligado em FHIR R4 Support Settings e, ao ligar, acrescenta campos a objetos padrão como Account e Contact.",
           E("src:dev-health-cloud-clinical-data-model")),
    ],
}
P["sub:outras-areas"] = {
    "para_iniciantes": ini("É um agrupamento provisório deste tutorial, não uma área oficial da Salesforce. O inventário do projeto parte "
                           "da lista oficial de metadata types (METADATA_SUPPORT.md, v68); quando um tipo pertence a uma área que ainda "
                           "não tem tema próprio aqui, ele fica neste tema até ganhar um.",
                           "Um metadata type de um produto sem tema no tutorial ficaria aqui até o tema desse produto ser criado.",
                           E("src:sdr-metadata-support")),
    "encadeamento": enc("Funciona como fila de espera: quando uma área ganha tema próprio, os itens saem daqui e passam a ser estudados "
                        "nesse tema.",
                        E("src:sdr-metadata-support")),
}

CONTEUDO_PENDENTES4 = P
