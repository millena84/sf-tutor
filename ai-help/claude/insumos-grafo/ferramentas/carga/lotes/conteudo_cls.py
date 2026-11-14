"""Issue #34: conteúdo específico dos 13 temas principais restantes (Interface está em conteudo_temas.py).

Cada texto recombina fatos já catalogados nas funcionalidades (com as fontes delas) e das notas
fontes/extracoes/temas-referencias-oficiais.txt e temas-piloto-interface.txt. Usado por conteudo_temas.py.
"""
from carga.base import ev


def E(*ids):
    return [ev(i) for i in ids]


def ini(explicacao, exemplo, evs, comece=None, analogia=None):
    d = {"explicacao": explicacao, "exemplo": exemplo}
    if analogia:
        d["analogia"] = {"texto": analogia[0], "limite": analogia[1]}
    if comece:
        d["por_onde_comecar"] = comece
    d["evidencias"] = evs
    return d


def enc(texto, evs):
    return {"texto": texto, "evidencias": evs}


def av(tipo, titulo, texto, evs):
    return {"tipo": tipo, "titulo": titulo, "texto": texto, "evidencias": evs}


AF = "src:architect-build-forms"

CONTEUDO_CLS = {
    "cls:organizacao-e-configuracoes-base": {
        "para_iniciantes": ini(
            "São as configurações que valem para a org inteira, antes de qualquer processo: dados da empresa, idioma, localidade e "
            "moeda, ano fiscal, horários de funcionamento e quais recursos estão ligados. Mudar algo aqui afeta todos os usuários.",
            "Uma empresa brasileira define o idioma e a moeda padrão, o ano fiscal e o horário do suporte: segunda a sexta, das 8h às 18h, no fuso de Brasília.",
            E("src:help-setup-company", "src:help-bh"),
            comece=["func:horario-comercial"],
            analogia=("Como as configurações de um celular novo: idioma, fuso e região valem para todos os apps.",
                      "No celular, a configuração é de uma pessoa. Na org, um ajuste muda o comportamento para todos os usuários e processos.")),
        "encadeamento": enc(
            "Primeiro vêm os dados que identificam a org e as configurações gerais. Idioma, localidade, moeda e ano fiscal mudam como os "
            "valores aparecem. Horários comerciais e feriados alimentam prazos de outras regras, como escalonamento e marcos de atendimento. "
            "Domínios e habilitação de recursos completam o quadro. No catálogo, só o horário comercial já tem funcionalidade cadastrada.",
            E("src:help-setup-company", "src:help-bh", "src:help-ent-bh")),
        "avancado": [
            av("atencao", "Horário comercial em cascata",
               "Nos processos de SLA, o horário comercial do milestone prevalece sobre o do processo, que prevalece sobre o do caso. Ao "
               "desenhar prazos, decida em que nível cada horário será configurado.", E("src:help-ent-bh")),
            av("implantacao", "Configuração como metadado",
               "Grupos de configurações gerais são metadata types da família Settings, como BusinessHoursSettings. Por isso podem ser "
               "recuperados e implantados pela Metadata API, em vez de repetidos à mão em cada ambiente.",
               E("src:mdapi-businesshourssettings", "src:mdapi-intro")),
            av("atencao", "Atualizações de release",
               "O guia de configuração da org trata as atualizações de release (Release Updates) como tópico próprio: são mudanças que "
               "podem afetar customizações existentes e pedem acompanhamento a cada versão.", E("src:help-setup-company")),
        ],
    },
    "cls:acesso-identidade-e-seguranca": {
        "para_iniciantes": ini(
            "Responde a três perguntas: quem pode entrar na org, como prova quem é e o que pode ver e fazer depois de entrar. Cada pessoa "
            "ou integração é um usuário; o perfil dá o acesso básico e os permission sets somam acessos extras.",
            "Uma nova analista entra com o login da empresa (SSO), recebe o perfil padrão da área e um permission set que libera contratos. "
            "No histórico de login aparece de onde ela acessou.",
            E("src:objref-user", "src:help-users", "src:mdapi-profile", "src:mdapi-permissionset", "src:mdapi-samlssoconfig", "src:help-login-history"),
            comece=["func:usuarios", "func:permission-sets"],
            analogia=("Como um prédio comercial: o crachá identifica a pessoa, a catraca confere a entrada e cada andar tem portas que o crachá abre ou não.",
                      "No prédio, entrar no andar costuma bastar. Na Salesforce há camadas separadas (objeto, campo e registro) e todas precisam permitir o acesso.")),
        "encadeamento": enc(
            "Roteiro pelas sete seções do tema. 1) 'Usuários e provisionamento': primeiro existe o usuário. 2) 'Autenticação, SSO e MFA': "
            "como ele prova quem é (senha, SSO, provedores externos). 3) 'Sessões e políticas de login': de onde, quando e por qual endereço "
            "pode entrar. 4) 'Permissões, perfis e grupos': o que pode fazer depois de entrar. 5) 'Licenças e entitlements de acesso': o "
            "teto do que pode ser concedido. 6) 'Acesso a registros e hierarquias': quais registros enxerga (padrões da org, compartilhamento "
            "e equipes). 7) 'Credenciais, certificados e proteção de dados': os segredos que protegem as conexões com outros sistemas.",
            E("src:security-guide", "src:objref-user", "src:mdapi-profile", "src:mdapi-permissionsetgroup", "src:objref-accountteammember", "src:mdapi-certificate")),
        "avancado": [
            # 1) Usuários e provisionamento
            av("atencao", "Desativar ou congelar, nunca excluir",
               "Usuários não podem ser excluídos, só desativados (IsActive); a API não oferece delete() em User. Para bloquear o acesso sem "
               "desativar, há o congelamento (UserLogin.IsFrozen). O ciclo de vida e o provisionamento precisam contar com isso.",
               E("src:objref-user", "src:help-users", "src:objref-userlogin")),
            # 2) Autenticação, SSO e MFA
            av("decisao", "SAML ou provedor de autenticação",
               "Para login com o provedor corporativo, a configuração SAML aceita a asserção e pode criar o usuário no primeiro acesso "
               "(just-in-time). Provedores de autenticação (OpenID Connect, Google, Microsoft) servem para login e também para obter tokens "
               "usados por integrações. Para integrações novas, a Salesforce recomenda external client apps; a criação de connected apps "
               "está restrita desde o Spring '26.",
               E("src:mdapi-samlssoconfig", "src:help-auth-provider-oidc", "src:help-connected-app-basics", "src:help-eca-create")),
            av("implantacao", "Segredo do provedor não vem no retrieve",
               "O segredo do app do provedor de autenticação (consumerSecret) é exportado como marcador e precisa ser preenchido em cada "
               "ambiente depois do deploy.", E("src:mdapi-authprovider")),
            # 3) Sessões e políticas de login
            av("seguranca", "Por onde se entra",
               "A política de login do My Domain pode impedir o login por login.salesforce.com e exigir que logins SOAP usem a URL do My "
               "Domain; tráfego de API com URL de instância incorreta é bloqueado depois do Summer '26. Faixas de IP e horários de login "
               "ficam no perfil (loginIpRanges).", E("src:help-mydomain-login-policy", "src:mdapi-profile")),
            av("limite", "Histórico de login",
               "A tela Login History mostra até 20.000 registros dos últimos 6 meses, e o download cobre o mesmo período. O IP de cada "
               "tentativa fica em LoginHistory.SourceIp.", E("src:help-login-history", "src:objref-loginhistory")),
            # 4) Permissões, perfis e grupos
            av("decisao", "Perfil enxuto, acesso por permission set",
               "O catálogo registra a recomendação de manter perfis enxutos e conceder acessos adicionais por permission sets, agrupados em "
               "permission set groups quando formam um papel de trabalho. O que só existe no perfil, como horários e faixas de IP de login, continua nele.",
               E("src:help-users", "src:mdapi-profile", "src:help-psg-create")),
            av("implantacao", "Atribuição é registro, não metadado",
               "A atribuição de permission sets e grupos é um registro de PermissionSetAssignment, não parte do XML, e a Metadata API não "
               "move dados de negócio: a atribuição não vai junto no deploy. Grupos só podem ser atribuídos com status Updated.",
               E("src:objref-permissionsetassignment", "src:mdapi-permissionset", "src:mdapi-intro", "src:help-psg-assign")),
            # 5) Licenças e entitlements de acesso
            av("limite", "A licença é o teto",
               "A licença Salesforce dá acesso completo ao CRM padrão; a Salesforce Platform não dá direito a objetos padrão como leads, "
               "oportunidades, campanhas e previsões. Feature licenses e permission set licenses liberam o que a licença de usuário não "
               "inclui, como o Service Cloud User para o Service Console. A licença Salesforce Integration não aceita permission set "
               "licenses de nuvens setoriais.",
               E("src:help-user-licenses", "src:help-service-feature-license", "src:help-health-cloud-psl", "src:help-industry-psl-integration-user")),
            # 6) Acesso a registros e hierarquias
            av("seguranca", "Camadas que precisam permitir",
               "O acesso a dados passa por camadas: permissão no objeto, segurança em nível de campo e compartilhamento de registros. A "
               "segurança de campo prevalece sobre o layout da página: tirar o campo da tela não restringe o acesso.",
               E("src:security-guide", "src:security-fls")),
            av("atencao", "Compartilhar sem trocar o dono",
               "Equipes de conta e de oportunidade dão acesso e responsabilidade compartilhada sem mudar o dono do registro. Alguns padrões "
               "de compartilhamento (SharingSettings) dependem da data de criação da org, então duas orgs podem se comportar diferente.",
               E("src:objref-accountteammember", "src:objref-opportunityteammember", "src:mdapi-sharingsettings")),
            # 7) Credenciais, certificados e proteção de dados
            av("limite", "Certificados",
               "Certificados autoassinados são criados em Certificate and Key Management, com a permissão Manage Certificates e no máximo "
               "50 por org. InboundCertificate, usado na autenticação mútua, só existe com a permissão MutualAuthentication habilitada. "
               "Named credentials e external credentials são estudadas em Integração.",
               E("src:help-cert-self-signed", "src:mdapi-inboundcertificate", "src:mdapi-namedcredential")),
        ],
    },
    "cls:dados-e-modelagem": {
        "para_iniciantes": ini(
            "É a estrutura onde os dados ficam guardados: objetos, os campos de cada registro, os relacionamentos entre objetos, os tipos "
            "de registro e as listas de valores. Antes de automatizar ou desenhar telas, é aqui que se decide o que existe e como se liga.",
            "Uma empresa cria o objeto Contrato_Servico__c, com o campo Valor_Mensal__c do tipo moeda, uma regra que impede valor negativo "
            "e os tipos de registro Manutenção e Licenciamento, com listas de status diferentes.",
            E("src:mdapi-customobject", "src:mdapi-customfield", "src:mdapi-validationrule", "src:mdapi-recordtype"),
            comece=["func:objetos-customizados", "func:campos-customizados"],
            analogia=("Como uma planilha bem organizada: cada aba é um objeto, cada coluna é um campo e cada linha é um registro.",
                      "Na planilha, a aba é um arquivo que você controla por inteiro. Na Salesforce, objetos são definições de metadados com "
                      "regras de acesso, relacionamentos e comportamento próprios, e não tabelas acessadas diretamente.")),
        "encadeamento": enc(
            "Roteiro pelas sete seções do tema. 1) 'Objetos e entidades': o objeto é a base, padrão ou customizado. 2) 'Campos e tipos': "
            "os campos dão forma a cada registro. 3) 'Relacionamentos e junções': campos que ligam objetos, inclusive por objetos de junção. "
            "4) 'Tipos de registro e processos de negócio': variações do mesmo objeto. 5) 'Listas de valores': picklists e conjuntos de "
            "valores, que cada tipo de registro pode recortar. 6) 'Metadados de configuração de dados': índices, histórico e feed. "
            "7) 'Modelos externos e especializações': dados que ficam em outro sistema e outras formas especiais de modelar.",
            E("src:mdapi-customobject", "src:mdapi-customfield", "src:mdapi-recordtype", "src:objref-data-model", "src:mdapi-externaldatasource")),
        "avancado": [
            # 1) Objetos e entidades
            av("decisao", "Objeto padrão, customizado ou externo",
               "Antes de criar um objeto customizado, confira os objetos padrão nos diagramas do Data Model: o customizado serve para "
               "entidades que não existem entre os padrão. Quando os dados ficam em outro sistema e não devem ser copiados, objetos "
               "externos (sufixo __x) mostram os registros sob demanda.",
               E("src:objref-data-model", "src:mdapi-customobject", "src:help-external-data-source-odata")),
            av("implantacao", "Definição pela Tooling API",
               "A definição de objetos e campos pode ser consultada pela Tooling API (EntityDefinition, FieldDefinition, CustomObject, "
               "CustomField). Cada objeto tem exposição própria: não suponha que o que existe na API padrão existe igual na Tooling API.",
               E("src:tooling-entitydefinition", "src:tooling-fielddefinition", "src:tooling-intro")),
            # 2) Campos e tipos
            av("seguranca", "Campo novo precisa de segurança de campo",
               "Ao criar campos, defina quem pode vê-los e editá-los pela segurança em nível de campo. Tirar o campo do layout não "
               "restringe o acesso, porque a segurança de campo prevalece.", E("src:security-fls")),
            av("implantacao", "O tipo define o resto do campo",
               "No CustomField, type escolhe entre tipos como Text, Number, Currency, Date, Picklist, MultiselectPicklist, Lookup, "
               "MasterDetail, Summary e EncryptedText, e cada tipo usa um conjunto diferente de propriedades. Para campos customizados, type "
               "é incluído; em alguns campos padrão, é opcional.", E("src:mdapi-customfield")),
            # 3) Relacionamentos e junções
            av("decisao", "Lookup ou master-detail",
               "No lookup, deleteConstraint decide o que acontece quando o pai é excluído: SetNull (padrão), Restrict ou Cascade. No "
               "master-detail, o filho não muda de pai, a menos que reparentableMasterDetail seja ligado, e writeRequiresMasterRead "
               "define se ler o pai basta para alterar os filhos. Campos de resumo (Summary) agregam filhos com Count, Min, Max ou Sum.",
               E("src:mdapi-customfield")),
            av("implantacao", "Objeto de junção",
               "Num objeto de junção com dois pais master-detail, relationshipOrder marca qual é o primário (0) e qual é o secundário (1). "
               "Um lookupFilter restringe quais registros podem ser escolhidos num lookup.", E("src:mdapi-customfield")),
            # 4) Tipos de registro e processos de negócio
            av("atencao", "Tipos de registro de Opportunity",
               "Tipos de registro de Opportunity exigem um processo de vendas (BusinessProcessId em RecordType).", E("src:objref-recordtype")),
            # 5) Listas de valores
            av("decisao", "Valores locais ou conjunto global",
               "A picklist guarda os próprios valores (valueSetDefinition) ou herda um conjunto global pelo nome (valueSetName). Com "
               "restricted, ela só aceita os valores definidos. Picklists dependentes usam controllingField e valueSettings. Cada tipo de "
               "registro pode mostrar só parte dos valores (picklistValues no RecordType).",
               E("src:mdapi-field-types", "src:mdapi-customfield", "src:mdapi-recordtype")),
            # 6) Metadados de configuração de dados
            av("escala", "Índices e External ID",
               "A plataforma já indexa campos como Id, Name, CreatedDate e chaves estrangeiras. External ID e Unique criam índice; External ID "
               "serve de chave no upsert, mas aceita valores repetidos, e Unique impede repetição. Índice em outros campos é pedido ao Support.",
               E("src:dev-ldv-indexes", "src:help-external-id-unique-index")),
            # 7) Modelos externos e especializações
            av("implantacao", "Um metadata type, vários tipos de objeto",
               "O CustomObject define objetos customizados e também objetos externos (sufixo __x, com externalDataSource) e eventos de "
               "plataforma (eventType, publishBehavior). O arquivamento do Field Audit Trail usa o big object FieldHistoryArchive.",
               E("src:mdapi-customobject", "src:help-field-audit-trail")),
        ],
    },
    "cls:qualidade-governanca-e-ciclo-de-vida-dos-dados": {
        "para_iniciantes": ini(
            "Reúne o que protege a qualidade dos dados ao longo do tempo: regras que impedem gravar dados errados, detecção de "
            "duplicados, marcação de dados sensíveis, retenção, histórico de alterações e registro do consentimento das pessoas.",
            "Uma regra de validação impede salvar um contrato com valor negativo; a detecção de duplicados avisa quando alguém tenta "
            "criar um registro que já existe.",
            E("src:mdapi-validationrule", "src:help-duplicate-management-customize", "src:help-data-classification-intro",
              "src:help-recycle-bin-lex", "src:help-field-history-tracking", "src:help-consent-data-model"),
            comece=["func:regras-de-validacao"],
            analogia=("É como cuidar de um arquivo de fichas: conferir a ficha antes de guardar, não guardar a mesma duas vezes, "
                      "etiquetar o que é confidencial e decidir quando descartar.",
                      "A etiqueta não tranca a gaveta: classificar um campo como sensível não restringe o acesso a ele. Quem "
                      "restringe é a segurança de campo e o compartilhamento.")),
        "encadeamento": enc(
            "Roteiro pelas seis seções do tema. 1) 'Validação': barra o dado errado no momento de salvar. 2) 'Duplicidade e "
            "correspondência': reconhece e trata registros repetidos, na criação e na edição. 3) 'Classificação e sensibilidade': marca "
            "o que é sensível. 4) 'Retenção, arquivamento e exclusão': quanto tempo o dado fica e o que acontece ao apagar. "
            "5) 'Rastreabilidade e histórico': quem mudou o quê e quando. 6) 'Consentimento e privacidade': o que cada pessoa autorizou. "
            "No catálogo, só a validação já tem funcionalidade cadastrada.",
            E("src:mdapi-validationrule", "src:help-duplicate-management-customize", "src:help-data-classification-intro",
              "src:help-recycle-bin-lex", "src:help-field-history-tracking", "src:help-consent-data-model")),
        "avancado": [
            # 1) Validação
            av("decisao", "Validação, automação ou segurança",
               "A regra de validação bloqueia a gravação quando uma condição de erro é verdadeira; ela não esconde o campo nem corrige o "
               "valor. Para restringir quem edita, use a segurança de campo; para preencher ou corrigir valores, use automação.",
               E("src:mdapi-validationrule", "src:security-fls", "src:mdapi-flow")),
            av("implantacao", "Onde a validação entra na gravação",
               "A ordem de processamento é: validation rules, assignment rules, auto-response rules, workflow rules com ações imediatas "
               "e escalation rules. Record-triggered flows também executam as regras de validação customizadas. Regras conflitantes no "
               "mesmo campo impedem salvar, então vale testar antes de ativar.",
               E("src:help-validation-considerations", "src:help-rtf-considerations", "src:help-validation-tips")),
            # 2) Duplicidade e correspondência
            av("decisao", "Duas regras contra duplicados",
               "A matching rule define como reconhecer um duplicado; a duplicate rule define o que fazer: alertar, bloquear ou reportar. "
               "As regras padrão vêm ativas para business accounts, contatos e leads. Cada objeto aceita até cinco duplicate rules ativas.",
               E("src:help-duplicate-management-customize", "src:help-duplicate-prevention", "src:help-duplicate-rules-things-to-know")),
            av("atencao", "Duplicados e acesso",
               "A contagem de duplicados mostra só os registros a que o usuário tem acesso, a menos que a regra use Bypass sharing rule. "
               "Em Web-to-Lead, um envio que bate com o critério é sempre bloqueado, mesmo com a regra em permitir com alerta.",
               E("src:help-duplicate-rules-classic-view", "src:help-duplicate-web-to-lead")),
            # 3) Classificação e sensibilidade
            av("seguranca", "Classificar não é proteger",
               "Data Classification registra no campo o nível de sensibilidade, a categoria de conformidade, o responsável e o uso. É "
               "informação para orientar decisões: marcar Field Usage como Hidden não esconde o campo. Os valores ficam no CustomField "
               "(securityClassification, complianceGroup) e exigem Customize Application ou Modify Data Classification.",
               E("src:help-data-classification-intro", "src:help-data-classification-fields", "src:mdapi-customfield")),
            # 4) Retenção, arquivamento e exclusão
            av("decisao", "Três graus de exclusão",
               "A exclusão comum manda o registro para a Recycle Bin, onde fica 15 dias. Esvaziar a Recycle Bin ou usar hard delete pela "
               "API manda para a fila de purga. Remover da tabela do banco é um physical delete, pedido ao Support.",
               E("src:help-delete-unwanted-data", "src:help-recycle-bin-lex")),
            # 5) Rastreabilidade e histórico
            av("limite", "Histórico de campos",
               "Sem Field Audit Trail, o histórico cobre até 20 campos por objeto e fica até 18 meses (24 pela API). Com Field Audit "
               "Trail, vai a 200 campos e fica até ser excluído, no big object FieldHistoryArchive. Excluir o registro apaga o histórico "
               "relacionado, mas não a cópia já arquivada.", E("src:help-field-history-tracking", "src:help-field-audit-trail")),
            av("atencao", "Histórico de campos também é auditoria",
               "O Security Guide trata o histórico de campos dentro de auditoria e monitoramento, junto com logins e alterações de "
               "configuração. Parte da rastreabilidade se cruza com o tema de observabilidade.", E("src:security-guide")),
            # 6) Consentimento e privacidade
            av("decisao", "Consentimento em quatro níveis",
               "O modelo registra consentimento no nível global (Individual), por canal (ContactPointTypeConsent), por ponto de contato "
               "(ContactPointConsent) e por finalidade (DataUsePurpose). Os objetos só guardam as preferências: cumprir cada uma é "
               "processo que a empresa implementa.", E("src:help-consent-data-model", "src:help-consent-objects")),
            av("seguranca", "Gravar consentimento pela API",
               "A Consent Write API grava consentimento na org inteira, não só nos registros que o usuário vê, e exige ModifyAllData ou "
               "ConsentApiUpdate.", E("src:rest-consent-write")),
        ],
    },
    "cls:automacao-de-processos-e-regras-de-negocio": {
        "para_iniciantes": ini(
            "Reúne o que faz trabalho sem que alguém execute cada passo: fluxos criados sem código, regras que distribuem e escalonam "
            "registros, aprovações e automação em código Apex.",
            "Quando um contrato é assinado, um Flow atualiza o status. Casos de prioridade alta vão automaticamente para a fila de nível 1 por uma regra de atribuição.",
            E("src:help-produtos-platform", "src:mdapi-flow", "src:help-assign-setup"),
            comece=["func:flow", "func:regras-de-atribuicao"],
            analogia=("Como as regras de uma linha de produção: cada etapa dispara a próxima sem alguém empurrar.",
                      "A automação só faz o que foi configurado: se a regra não prevê um caso, ele passa sem tratamento.")),
        "encadeamento": enc(
            "Flow é a ferramenta declarativa principal e pode ser disparado por tela, por registro, por agendamento ou por outros gatilhos. "
            "Decisões e aprovações organizam quem decide; regras definem dono e escalonamento; a automação Apex cobre o que exige código; "
            "notificações avisam pessoas; e os mecanismos legados explicam ferramentas antigas e a migração para as atuais.",
            E("src:mdapi-flow", "src:help-assign-guide", "src:help-escalation-setup", "src:help-produtos-platform")),
        "avancado": [
            av("decisao", "Declarativo ou código",
               "A Ajuda separa as ferramentas declarativas de automação (experiências guiadas, automação em segundo plano e aprovações) "
               "da área de desenvolvimento com código. Para formulários, o guia de decisão lembra que no Screen Flow a lógica fica com "
               "administradores, enquanto LWC exige desenvolvimento.", E("src:help-produtos-platform", AF)),
            av("limite", "Uma regra ativa por tipo",
               "Só uma regra de atribuição de cada tipo fica ativa por vez, e uma regra de atribuição de casos aceita até 3.000 entradas, "
               "incluindo 300 de fórmula.", E("src:help-assign-guide")),
            av("seguranca", "Contexto de execução do Screen Flow",
               "Screen Flow roda no contexto do usuário por padrão, mas pode rodar em contexto de sistema; esse modo deve ficar restrito a "
               "usuários confiáveis.", E(AF)),
            av("atencao", "Chamada externa dentro da transação",
               "Em automação Apex, não é possível chamar um sistema externo depois de DML pendente na mesma transação. Faça a chamada antes "
               "ou leve-a para um processo assíncrono.", E("src:apex-callout-limits")),
        ],
    },
    "cls:execucao-assincrona-lotes-e-agendamento": {
        "para_iniciantes": ini(
            "Reúne o processamento que não acontece na hora do clique: trabalhos em lote, tarefas em fila, execuções agendadas e reações "
            "a eventos. Serve para volumes grandes, chamadas demoradas e tarefas que podem esperar.",
            "Toda madrugada, um job agendado inicia um processamento em lote que recalcula a classificação de milhares de contas.",
            E("src:apex-async-overview"),
            comece=["func:platform-events"],
            analogia=("Como deixar a roupa na lavanderia: você entrega, segue o dia e busca depois.",
                      "Na lavanderia você sempre recebe um tíquete. No Apex, só alguns mecanismos devolvem um identificador para acompanhar o trabalho, como o Queueable.")),
        "encadeamento": enc(
            "Batch divide grandes volumes em partes; Queueable enfileira tarefas e permite encadeá-las; Future é o mecanismo mais antigo; "
            "o agendamento dispara execuções em horários definidos; caminhos assíncronos levam parte de uma automação declarativa para "
            "depois; eventos de plataforma disparam reações quando algo é publicado; e o monitoramento acompanha jobs e limites.",
            E("src:apex-async-overview", "src:apex-queueable", "src:help-platform-events-define")),
        "avancado": [
            av("decisao", "Qual mecanismo Apex",
               "Pelo guia de Apex: Queueable para operações longas com identificador, tipos complexos e encadeamento; Scheduled para rodar "
               "em horário definido; Batch para grandes volumes; Future para métodos longos sem atrasar a transação. A Salesforce recomenda "
               "Queueable no lugar de future methods.", E("src:apex-async-overview", "src:apex-queueable")),
            av("limite", "Fila do Batch Apex",
               "O Batch Apex tem limite de cinco jobs ativos, com uma Flex Queue de até 100 jobs adicionais.", E("src:apex-async-overview")),
            av("atencao", "Retentativa em triggers de evento",
               "Um trigger de evento roda no máximo 10 vezes (a inicial e 9 retentativas). A retentativa reenvia o lote inteiro e desfaz o "
               "DML anterior. Limite as tentativas e tenha uma ação alternativa quando o limite chegar.", E("src:pe-retry-apex")),
            av("atencao", "Callout depois de assíncrono pendente",
               "Não é possível fazer callout depois de Apex assíncrono ou agendado pendente na mesma transação; antes deles, pode.",
               E("src:apex-callout-limits")),
        ],
    },
    "cls:integracao-apis-e-eventos": {
        "para_iniciantes": ini(
            "Reúne como a org conversa com outros sistemas: as APIs que a Salesforce oferece para ler e gravar dados e metadados, as "
            "chamadas que a org faz para fora, as credenciais, os eventos e os limites dessas conversas.",
            "Um ERP cria pedidos pela REST API; quando o pedido é faturado, publica um evento que atualiza a oportunidade; e um Flow chama "
            "a API de frete por uma named credential, sem senha no código.",
            E("src:rest-intro", "src:help-platform-events-define", "src:help-nc-create"),
            comece=["func:rest-api", "func:named-credentials"],
            analogia=("Como os correios entre empresas: cada uma tem endereço, regras de entrega e um jeito de provar quem enviou.",
                      "Nos correios, a carta chega ou não. Numa integração há limites de volume e tempo, versões que deixam de existir e falhas que pedem nova tentativa.")),
        "encadeamento": enc(
            "Roteiro pelas sete seções do tema. 1) 'APIs de dados e metadados': as portas de entrada (REST, SOAP, Bulk, Metadata, Tooling). "
            "2) 'Autenticação de integrações': quem chama prova quem é por um external client app ou connected app, com OAuth. "
            "3) 'Credenciais' e 4) 'Chamadas externas e endpoints': o sentido contrário, a org chamando serviços de fora por named "
            "credentials, sites remotos e serviços externos. 5) 'Eventos e mensageria': avisar sistemas sem consulta periódica (eventos de "
            "plataforma, captura de alterações, Pub/Sub API, Event Relay). 6) 'Conectividade e virtualização de dados': ler dados de fora "
            "sem copiar, com objetos externos. 7) 'Contratos, limites e tratamento de falhas': o que vale para todas as anteriores "
            "(alocações, versões, retentativas).",
            E("src:rest-intro", "src:soap-intro", "src:bulk-api-intro", "src:mdapi-intro", "src:tooling-intro", "src:help-eca-create",
              "src:mdapi-namedcredential", "src:pubsub-overview", "src:help-event-relay-create", "src:help-external-data-source-odata", "src:limits-api-requests")),
        "avancado": [
            # 1) APIs de dados e metadados
            av("decisao", "Qual API usar",
               "REST para chamadas HTTP simples, em JSON ou XML. SOAP quando o sistema trabalha com contrato WSDL (Enterprise, tipado e da "
               "org; Partner, genérico). Bulk API 2.0 para operações com mais de 2.000 registros. Metadata API para mover configuração entre "
               "orgs. Tooling API para ferramentas que leem e alteram pedaços pequenos de metadados.",
               E("src:rest-intro", "src:soap-intro", "src:bulk-api-intro", "src:mdapi-intro", "src:tooling-intro")),
            # 2) Autenticação de integrações
            av("seguranca", "Registrar a integração",
               "Para integrações novas, a Salesforce recomenda external client apps; a criação de connected apps está restrita desde o "
               "Spring '26. Usar external client apps exige a permissão Opt in to External Client Apps. Escopos customizados limitam o que "
               "cada app faz, e há configurações para bloquear fluxos OAuth ou exigir PKCE.",
               E("src:help-connected-app-basics", "src:help-eca-create", "src:mdapi-externalclientapplication",
                 "src:mdapi-oauthcustomscope", "src:mdapi-oauthoidcsettings")),
            # 3) Credenciais e 4) Chamadas externas
            av("seguranca", "Segredo fora do código e o sentido de cada lista",
               "Named credentials guardam o endereço e a autenticação fora do código; desde a 56.0, a autenticação mora na credencial "
               "externa. Sites remotos só liberam o endereço, e a Salesforce recomenda named credentials para callouts novos. CORS é o "
               "sentido contrário: libera chamadas do navegador para a org, não da org para fora.",
               E("src:mdapi-namedcredential", "src:help-remote-site", "src:help-cors")),
            av("limite", "Callouts dentro de uma transação",
               "Uma transação Apex faz até 100 callouts, e a soma dos timeouts não passa de 120 segundos. Não dá para fazer callout depois "
               "de DML, Apex assíncrono, Apex agendado ou envio de e-mail pendentes na mesma transação; antes deles, pode.",
               E("src:apex-callout-limits")),
            # 5) Eventos e mensageria
            av("decisao", "Eventos em vez de consulta periódica",
               "A captura de alterações publica um evento a cada mudança de registro e mantém sistemas sincronizados quase em tempo real. "
               "Pela Pub/Sub API, o cliente controla quantos eventos recebe por vez (até 100 por pedido), com eventos de até 1 MB.",
               E("src:pubsub-qs-events", "src:pubsub-overview", "src:pubsub-allocations")),
            av("atencao", "Falha em quem recebe o evento",
               "Um trigger de evento roda no máximo 10 vezes (a inicial e 9 retentativas) e depois vai para o estado Error; eventos "
               "enviados nesse período não são reenviados. Cada retentativa reenvia o lote inteiro e desfaz o DML anterior. A orientação "
               "oficial é limitar as tentativas e ter uma ação alternativa.", E("src:pe-retry-apex")),
            # 6) Conectividade e virtualização de dados
            av("decisao", "Copiar ou consultar sob demanda",
               "Objetos externos leem os dados no momento da consulta e permitem usá-los em listas, relacionamentos e relatórios sem "
               "manter cópia na org. A definição usa CustomObject (externalDataSource, externalName), com sufixo __x.",
               E("src:help-external-data-source-odata", "src:mdapi-customobject")),
            # 7) Contratos, limites e tratamento de falhas
            av("limite", "Alocação diária e tempo de chamada",
               "O limite diário de requisições vale para a org inteira, não por usuário, e chamadas de pacotes gerenciados contam. "
               "Requisições de 20 segundos ou mais têm limite de simultaneidade (25 em produção e sandbox), e chamadas REST e SOAP expiram "
               "após 10 minutos.", E("src:limits-api-requests", "src:rest-limits")),
            av("escala", "Acompanhar o consumo",
               "API Usage Notifications avisam por e-mail quando o uso passa de uma porcentagem da alocação. O recurso /limits tem precisão "
               "de até cinco minutos, então não deve ser chamado em rajadas. Orgs pagas podem passar um pouco do limite diário, até um teto "
               "rígido; trial, Developer Edition e sandbox não.", E("src:limits-api-requests", "src:rest-limits")),
            av("atencao", "Contratos que mudam",
               "O Enterprise WSDL é específico da org e precisa ser gerado de novo quando objetos ou campos customizados mudam. Num serviço "
               "externo, uma versão nova da especificação exige novo registro, porque systemVersion não é atualizado no lugar. Não há SLA "
               "para a Bulk API, e jobs terminados há mais de 7 dias são apagados.",
               E("src:soap-intro", "src:mdapi-externalserviceregistration", "src:limits-bulk-api", "src:bulk-api-intro")),
            av("atencao", "Versões de API",
               "As versões 31.0 a 40.0 estão em descontinuação: sem suporte a partir do Summer '27 e aposentadas no Summer '28. Chamadas a "
               "versões aposentadas recebem 410:GONE. O evento API Total Usage ajuda a achar integrações antigas.",
               E("src:rest-api-eol", "src:rest-versions")),
        ],
    },
    "cls:relatorios-analytics-e-exploracao": {
        "para_iniciantes": ini(
            "Reúne como os dados da org viram respostas: relatórios e dashboards nativos para analisar e compartilhar resultados e, para "
            "análises maiores, produtos analíticos como CRM Analytics e Tableau.",
            "Uma gerente acompanha num dashboard o resultado de um relatório de oportunidades por etapa.",
            E("src:help-produtos-analytics", "src:help-setup-company")),
        "encadeamento": enc(
            "Relatórios ficam na base; dashboards mostram relatórios em gráficos; tipos de relatório, pastas e métricas organizam o que pode "
            "ser consultado e quem vê. Produtos analíticos à parte, como CRM Analytics e Tableau, entram como recursos de produto. Nenhuma "
            "funcionalidade deste tema está catalogada ainda.", E("src:help-produtos-analytics")),
        "avancado": [
            av("decisao", "Nativo ou produto analítico",
               "A Ajuda separa Reports and Dashboards, nativos, de produtos analíticos como CRM Analytics, Tableau e Tableau Next. Tableau "
               "é a plataforma para combinar e visualizar dados de várias fontes. Antes de escolher, confira licença e onde os dados "
               "precisam ser combinados.", E("src:help-produtos-analytics")),
        ],
    },
    "cls:conteudo-conhecimento-e-colaboracao": {
        "para_iniciantes": ini(
            "Reúne o conteúdo que as pessoas usam e compartilham: arquivos ligados a registros, bibliotecas, artigos de conhecimento e "
            "modelos de comunicação.",
            "Um artigo 'Como trocar a senha' é sugerido ao atendente e publicado no portal; o contrato assinado fica ligado à conta como arquivo.",
            E("src:data-model-files", "src:help-lk-enable"),
            comece=["func:lightning-knowledge"]),
        "encadeamento": enc(
            "Files e bibliotecas guardam documentos e os ligam a registros; Knowledge organiza artigos e categorias para atendentes e "
            "clientes; colaboração e modelos de comunicação cuidam de conversas e mensagens padronizadas.",
            E("src:data-model-files", "src:help-lk-enable")),
        "avancado": [
            av("atencao", "Habilitar Lightning Knowledge não tem volta",
               "Ligar o Lightning Knowledge é irreversível e muda o modelo de dados para tipos de registro; exige ao menos um tipo de "
               "artigo. Decida antes de habilitar em produção.", E("src:help-lk-enable")),
            av("decisao", "Arquivo é documento, versão e vínculo",
               "No modelo de dados de Files, o arquivo (Content Document) tem versões (Content Version) e se liga a registros por Content "
               "Document Link; bibliotecas e pastas organizam o acesso. Isso importa em migrações e em consultas por API.",
               E("src:data-model-files")),
        ],
    },
    "cls:desenvolvimento-testes-e-entrega": {
        "para_iniciantes": ini(
            "Reúne como mudanças são construídas, testadas e levadas de um ambiente para outro: código e componentes, testes, pacotes, os "
            "formatos de arquivo dos metadados, sandboxes e a implantação.",
            "Um desenvolvedor cria uma classe numa scratch org, recupera a mudança para o projeto, roda os testes e implanta em produção pela Metadata API.",
            E("src:sfdx-dev-guide", "src:mdapi-intro", "src:help-produtos-platform"),
            comece=["func:metadata-api", "func:tooling-api"],
            analogia=("Como reformar uma casa com planta: testa-se na maquete antes de mexer na obra.",
                      "Na maquete, tudo vai junto. Aqui, a planta são arquivos de metadados; o que não é metadado, como registros e atribuições de permissão, não vai no deploy.")),
        "encadeamento": enc(
            "Código e componentes vivem como metadados em dois formatos: o source format, usado no projeto, e o Metadata API format. Testes "
            "garantem que funcionam; sandboxes e scratch orgs isolam o trabalho; pacotes agrupam componentes e dependências; e a "
            "implantação leva tudo para produção, com versionamento e caminho de volta.",
            E("src:sfdx-dev-guide", "src:sdr-registry", "src:mdapi-intro", "src:help-produtos-platform")),
        "avancado": [
            av("decisao", "deploy/retrieve ou source tracking",
               "A Metadata API indica deploy() e retrieve() para as fases finais, como implantar em produção, e source push/pull com source "
               "tracking nas fases intermediárias, que movem só o que mudou.", E("src:mdapi-intro")),
            av("decisao", "Metadata API ou Tooling API",
               "A Tooling API expõe metadados como objetos consultáveis e serve a ferramentas que leem e alteram pedaços pequenos com "
               "rapidez; a Metadata API move o modelo completo. A exposição de cada objeto é própria de cada API.",
               E("src:tooling-intro", "src:mdapi-intro")),
            av("atencao", "Nem todo tipo tem source tracking",
               "A lista de suporte do Salesforce CLI marca, para cada metadata type, se há deploy, retrieve e source tracking; alguns tipos "
               "só têm deploy e retrieve. Confira antes de contar com o rastreamento automático.", E("src:sdr-metadata-support")),
            av("testes", "Teste unitário só no pro-code",
               "Só LWC permite testes unitários escritos, por exemplo com Jest; Dynamic Forms e Screen Flow dependem de automação de "
               "interface de ponta a ponta.", E(AF)),
        ],
    },
    "cls:observabilidade-auditoria-e-operacao": {
        "para_iniciantes": ini(
            "Reúne o que mostra como a org está funcionando e o que foi feito nela: logins, alterações de configuração, eventos de uso, "
            "consumo de limites e investigação de problemas.",
            "Depois de uma tentativa de acesso suspeita, a equipe confere no histórico de login de qual IP veio a tentativa que falhou.",
            E("src:security-guide", "src:help-login-history"),
            comece=["func:estado-e-historico-de-login"]),
        "encadeamento": enc(
            "Logs de depuração e rastreamento mostram o que o código fez; a auditoria de configuração registra mudanças no Setup; o "
            "histórico de login guarda tentativas de acesso; eventos de monitoramento registram uso e atividade; limites e consumo mostram "
            "quanto da alocação já foi usado; e jobs e incidentes reúnem o diagnóstico.",
            E("src:security-guide", "src:help-login-history", "src:rest-limits")),
        "avancado": [
            av("limite", "Janela do histórico de login",
               "A tela de Setup mostra até 20.000 registros dos últimos 6 meses, e o download cobre os últimos 6 meses. A retenção do "
               "objeto LoginHistory pela API não foi confirmada.", E("src:help-login-history")),
            av("atencao", "IP: onde está cada coisa",
               "Não existe um item 'IpLogin': as faixas de IP permitidas por perfil ficam em Profile.loginIpRanges, e o IP de cada "
               "tentativa fica em LoginHistory.SourceIp.", E("src:mdapi-profile", "src:objref-loginhistory")),
            av("decisao", "Monitoramento quase em tempo real",
               "O Real-Time Event Monitoring detecta eventos padrão quase em tempo real, guarda os dados para auditoria e permite criar "
               "políticas de segurança de transação.", E("src:security-guide")),
            av("atencao", "Consumo de API",
               "O recurso /limits mostra o consumo com precisão de até cinco minutos: evite consultá-lo em rajadas e configure "
               "notificações de uso de API.", E("src:rest-limits", "src:limits-api-requests")),
        ],
    },
    "cls:ia-agentes-e-decisoes-assistidas": {
        "para_iniciantes": ini(
            "Reúne a configuração de agentes e recursos de IA da plataforma: o que o agente faz, sobre quais assuntos, que instruções e "
            "modelos usa, de onde tira conhecimento e como é controlado.",
            "Um agente de atendimento responde dúvidas sobre pedidos usando artigos de conhecimento e executa uma ação que consulta o status do pedido.",
            E("src:agentforce-dev-guide")),
        "encadeamento": enc(
            "A configuração define o agente; ações e tópicos (desde abril de 2026, tópicos se chamam subagents) dizem o que ele faz e sobre "
            "o quê; prompts e modelos definem como responde; a recuperação de conhecimento traz o conteúdo; e segurança, avaliação e "
            "governança controlam o uso. Nenhuma funcionalidade deste tema está catalogada ainda.", E("src:agentforce-dev-guide")),
        "avancado": [
            av("atencao", "Topics passaram a se chamar subagents",
               "Desde abril de 2026, agent topics se chamam subagents, sem mudança de funcionamento. Documentos e configurações antigas "
               "podem usar o nome anterior.", E("src:agentforce-dev-guide")),
            av("implantacao", "Ferramentas pro-code",
               "Para desenvolvimento, a documentação oferece Agent Script, a linguagem para construir agentes no Agentforce Builder, e "
               "Agentforce DX, com ferramentas para Salesforce CLI e VS Code.", E("src:agentforce-dev-guide")),
        ],
    },
    "cls:processos-de-negocio-especificos-de-produto": {
        "para_iniciantes": ini(
            "Reúne o que é próprio de um produto ou setor, e não da plataforma comum: em vendas, leads, oportunidades, produtos, cotações "
            "e previsões; no atendimento, casos, roteamento, conhecimento e níveis de serviço.",
            "Um lead do site é convertido em conta, contato e oportunidade; depois da venda, o cliente abre um caso que o Omni-Channel "
            "distribui para um atendente disponível.",
            E("src:help-sales-basics", "src:help-service-basics", "src:objref-lead", "src:help-omni-enable"),
            comece=["func:leads", "func:casos"],
            analogia=("Como lojas diferentes num mesmo shopping: cada uma vende algo próprio, mas todas usam o mesmo estacionamento, energia e segurança.",
                      "No shopping, as lojas são separadas. Na Salesforce, a mesma funcionalidade de plataforma, como regras de atribuição, serve a vendas e atendimento ao mesmo tempo.")),
        "encadeamento": enc(
            "Em vendas, o caminho vai de lead a conta, contato e oportunidade, com produtos, cotações, previsões, equipes e territórios. No "
            "atendimento, o caso é a base, com Omni-Channel, Knowledge, entitlements e horário comercial. Serviço de campo, receita e "
            "comércio, experiências externas e capacidades setoriais ainda não têm funcionalidades catalogadas.",
            E("src:help-sales-basics", "src:help-service-basics")),
        "avancado": [
            av("atencao", "Campos de estado derivados",
               "IsClosed e IsWon em oportunidades e IsClosed em casos não são gravados diretamente: refletem a etapa ou o status. "
               "Integrações devem mudar a etapa ou o status, não esses campos.", E("src:objref-opportunity", "src:objref-case")),
            av("atencao", "Converter lead é operação própria",
               "Mudar o status de um lead pela API não o converte; use convertLead() ou a interface.", E("src:objref-lead")),
            av("limite", "Licença Salesforce Platform",
               "Usuários com licença Salesforce Platform não têm direito a leads, oportunidades e previsões, segundo a Ajuda.",
               E("src:help-user-licenses")),
            av("atencao", "Omni-Channel Enhanced",
               "Standard Omni-Channel foi aposentado no Summer '26, com upgrade automático para Enhanced, que não suporta canais standard.",
               E("src:help-omni-upgrade")),
            av("atencao", "Territórios: um modelo ativo",
               "Só um modelo de territórios fica ativo por vez e, depois de ativo, não volta para Planning.", E("src:help-tm2-activate")),
        ],
    },
}
