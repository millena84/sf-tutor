"""Lote 9a (#10, etapa 3, lote A; 2026-11-23): cadastro de 16 tipos Settings já incluídos no Core e ainda sem ficha.

Cada tipo foi lido na página versionada 264.0 do Metadata API Developer Guide (endpoint get_document_content).
Estrutura e explicação entram na mesma passada (sem dívida para a Fase 2).
Classificação funcional: o tipo entra numa funcionalidade existente quando o assunto dela é o mesmo do tipo;
quando não há funcionalidade do assunto, cria uma nova com a página do tipo como fonte (caminho de Setup desconhecido).
Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import af                     # noqa: E402
from carga import catalogo as C               # noqa: E402
from carga import mdt as M                    # noqa: E402
from carga.mdt import mdt, P, struct, emit_structs   # noqa: E402

DATA = "2026-11-23"
EXTR = "fontes/extracoes/lote9a-core-settings-a.txt"
G = "https://developer.salesforce.com/docs/get_document_content/api_meta/"


def S(nome):
    return "src:mdapi-" + nome.lower()


TIPOS = ["NameSettings", "ActionsSettings", "CodeBuilderSettings", "CustomAddressFieldSettings", "DataImportManagementSettings",
         "DynamicFormsSettings", "EmailTemplateSettings", "EnhancedNotesSettings", "HelpSettings", "IframeWhiteListUrlSettings",
         "InvocableActionSettings", "PicklistSettings", "RecordPageSettings", "SchemaSettings", "MacroSettings", "SandboxSettings"]
C.registrar_fontes([C.fonte(S(n), f"{n} (Metadata API 264.0)", G + f"meta_{n.lower()}.htm/en-us/264.0",
                            f"Descrição, arquivo, versão e tabela Fields do tipo {n} (página lida por inteiro).", EXTR, DATA, versao="264.0")
                    for n in TIPOS])

FALSE = ("false", False, "A página declara default false.")
TRUE = ("valor", "true", "A página declara default true.")
PKG = "No package.xml, use o tipo Settings com o nome-base do arquivo como membro; o curinga só vale para recuperar todas as configurações."
FN = M.FULLNAME_HERDADO(None)
SEM_FN = " A leitura não registrou se a página declara fullName herdado; por isso ele não entrou."


def nota(n, linhas, fn=True):
    return f"Universo esperado = tabela Fields da página 264.0 ({linhas} campo{'s' if linhas > 1 else ''}), lida em {DATA}" + \
           (" (mais fullName herdado, declarado na página)." if fn else "." + SEM_FN)


NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'


def exemplo(nome, pares):
    corpo = "\n".join(f"    <{k}>{v}</{k}>" for k, v in pares)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<{nome} {NS}>\n{corpo}\n</{nome}>'


def settings(nome, base, o_que_e, finalidade, desde, linhas, fn=True, alertas=(), ex=None, **kw):
    rows = list(linhas) + ([FN] if fn else [])
    if ex is None:
        ex = [(r[0], "true") for r in linhas if r[1] == "boolean" and not (r[5] or {}).get("ate")][:2]
    kw["exemplo"] = exemplo(nome, ex)
    return mdt(nome, S(nome), o_que_e, finalidade, desde, rows, arquivos_prontos=M.arquivos_settings(nome, base, S(nome)), curinga=False,
               alertas=[PKG] + list(alertas), cobertura_nota=nota(nome, len(linhas), fn), **kw)


settings("NameSettings", "Name",
         "Liga ou desliga os campos de nome formal, nome do meio e sufixo nos objetos de pessoa: Contact, Lead, Person Account e User.",
         "Recuperar e implantar quais partes do nome de pessoa a org usa, em vez de ligar à mão em cada ambiente.", "31.0", [
             P("enableInformalName", "boolean", "48.0", "Reservado para uso interno, segundo a página."),
             P("enableMiddleName", "boolean", None, "Liga (true) ou desliga (false) o nome do meio nos objetos de pessoa."),
             P("enableNameSuffix", "boolean", None, "Liga (true) ou desliga (false) o sufixo do nome (como Jr.) nos objetos de pessoa."),
         ], ex=[("enableMiddleName", "true"), ("enableNameSuffix", "false")], alertas=["Campos de nome local não podem ser ligados pela Metadata API; a página manda fazer isso pela interface."])

settings("ActionsSettings", "Actions",
         "Configurações de ações da org: ações rápidas padrão, publicador multidimensional e ações de terceiros.",
         "Recuperar e implantar como as ações aparecem para os usuários, em vez de repetir a configuração em cada ambiente.", "47.0", [
             P("enableDefaultQuickActionsOn", "boolean", None, "Indica se as ações rápidas padrão são criadas na org.", default=TRUE),
             P("enableDynamicActionsMobileStdObj", "boolean", None, "Indica se Dynamic Actions on Mobile está ligado.", default=FALSE),
             P("enableMdpEnabled", "boolean", None, "Indica se o publicador multidimensional (a barra de ações com várias abas) está ligado.", default=TRUE),
             P("enableThirdPartyActions", "boolean", None, "Indica se ações de terceiros aparecem no publicador multidimensional.", default=FALSE),
             P("enableOfflineWebLinks", "boolean", None, "Indica se um botão ou link fica disponível também offline (true) ou só online (false).", default=FALSE),
         ], divergencias=["Na página (src:mdapi-actionssettings), o exemplo XML usa elementos com nomes diferentes da tabela "
                          "(DefaultQuickActionsOn, MdpEnabled, ThirdPartyActions) e não traz enableDynamicActionsMobileStdObj nem enableOfflineWebLinks. "
                          "O catálogo segue a tabela Fields."])

settings("CodeBuilderSettings", "CodeBuilder",
         "Configuração do Code Builder, o ambiente de desenvolvimento da Salesforce que roda no navegador.",
         "Recuperar e implantar se o Code Builder pode ser instalado e usado na org.", "58.0", [
             P("enableCodeBuilder", "boolean", None, "Liga (true) ou desliga (false) o Code Builder. Ligado, o pacote do Code Builder (versão de "
               "disponibilidade geral) pode ser instalado e usado na org."),
         ])

settings("CustomAddressFieldSettings", "CustomAddressField",
         "Configuração dos campos de endereço personalizados: se o tipo de campo Address pode ser usado em campos customizados.",
         "Recuperar e implantar a liberação do tipo Address para campos customizados.", "55.0", [
             P("enableCustomAddressField", "boolean", None, "Indica se o tipo de campo Address fica disponível para campos customizados.", default=FALSE,
               notas=["Não tem volta: depois de true, não pode voltar a false. A página recomenda revisar requisitos e limitações na Ajuda antes de ligar."]),
         ], alertas=["Ligar campos de endereço personalizados é irreversível; teste em sandbox antes."])

settings("DataImportManagementSettings", "DataImportManagement",
         "Configurações de importação de contatos e leads da org.",
         "Recuperar e implantar se a importação guiada de contatos e leads (Basic Data Import) está ligada.", "57.0", [
             P("enableEasyImport", "boolean", None, "Indica se a Basic Data Import está ligada. Com true, o usuário é guiado passo a passo para escolher "
               "como importar contatos e leads."),
         ], alertas=["Acesso: o tipo só existe quando a org tem a permissão DataImportManagement, disponível só em algumas edições."])

settings("DynamicFormsSettings", "DynamicForms",
         "Configurações do Dynamic Forms, que monta a página de registro com campos e seções colocados um a um.",
         "Recuperar e implantar se o Dynamic Forms no app móvel está ligado.", "58.0", [
             P("enableFormsOnMobile", "boolean", None, "Indica se o Dynamic Forms para mobile está ligado na org.",
               notas=["A página marca o recurso como Beta, sujeito aos termos de Beta Services."]),
         ], fn=False)

settings("EmailTemplateSettings", "EmailTemplate",
         "Configurações de modelos de e-mail da org.",
         "Recuperar e implantar se os modelos de e-mail usam pastas com compartilhamento aprimorado.", "47.0", [
             P("enableTemplateEnhancedFolderPref", "boolean", None, "Indica se pastas e compartilhamento aprimorado para modelos de e-mail estão "
               "ligados; com eles, os usuários criam e gerenciam pastas de modelos.", default=FALSE),
         ], fn=False)

settings("EnhancedNotesSettings", "EnhancedNotes",
         "Configurações de notas aprimoradas da org, como ligar as notas aprimoradas e as tarefas criadas a partir delas.",
         "Recuperar e implantar se as notas aprimoradas e as tarefas em notas estão ligadas.", "47.0", [
             P("enableEnhancedNotes", "boolean", None, "Indica se as notas aprimoradas estão ligadas. Com elas, uma nota pode ser ligada a vários "
               "registros, tem histórico de versões e formatação avançada. O usuário precisa da permissão Use New Notes.", default=TRUE),
             P("enableTasksOnEnhancedNotes", "boolean", None, "Indica se o usuário pode criar tarefas a partir de notas; no app Salesforce, por exemplo, "
               "deslizando sobre uma linha da nota. Também exige a permissão Use New Notes.", default=TRUE),
         ], fn=False)

settings("HelpSettings", "Help",
         "Configuração da org que troca o destino da Ajuda do Salesforce (help.salesforce.com) por uma URL alternativa.",
         "Recuperar e implantar a URL para onde os usuários vão ao abrir a Ajuda, por exemplo uma central interna.", "68.0", [
             P("alternativeUrl", "string", None, "URL alternativa aberta quando o usuário acessa a Ajuda do Salesforce. Até 255 caracteres e precisa ser "
               "uma URL válida; se a validação falha, a implantação devolve INVALID_OPERATION. Omitido no deploy, a URL existente não muda; "
               "em branco, a URL é apagada.", restr="Até 255 caracteres; URL válida."),
         ], fn=False, ex=[("alternativeUrl", "https://ajuda.example.com")], alertas=["Acesso: recuperar ou implantar exige a permissão Customize Application.",
                               "O componente não pode ser criado nem excluído e não é suportado em unlocked packages."])

struct("IframeWhiteListUrl", S("IframeWhiteListUrlSettings"), ["mdt:IframeWhiteListUrlSettings"], [
    P("context", "IFrameWhitelistContext", None, "Tipo de conteúdo exibido no iframe.", "S", vals=[
        ("LightningOut", "Reservado para uso futuro; disponível na API 60.0 e posteriores."), ("Surveys", "Pesquisas."),
        ("VisualforcePages", "Páginas Visualforce."), ("DisclosureAndComplianceHubConnector", "Disclosure and Compliance Hub Connector.")]),
    P("url", "string", None, "Um único domínio autorizado a exibir as páginas. Formatos aceitos: example.com, *example.com e https://example.com."),
], o_que_e="Um domínio externo confiável e o tipo de conteúdo que ele pode exibir em iframe.")
mdt("IframeWhiteListUrlSettings", S("IframeWhiteListUrlSettings"),
    "Lista de domínios externos confiáveis autorizados a exibir (em iframe) páginas Visualforce ou pesquisas da org.",
    "Recuperar e implantar a lista de domínios que podem enquadrar o conteúdo da org, em vez de cadastrá-los à mão em cada ambiente.", "49.0", [
        P("iframeWhiteListUrls", "IframeWhiteListUrl[]", None, "Domínios externos autorizados a exibir as páginas Visualforce ou as pesquisas da org.",
          estrutura="IframeWhiteListUrl"),
    ], curinga=False,
    exemplo=exemplo("IframeWhiteListUrlSettings", [("iframeWhiteListUrls", "\n        <context>VisualforcePages</context>\n        <url>example.com</url>\n    ")]),
    cobertura_nota=f"Universo esperado = tabela Fields da página 264.0 (1 campo, mais o subtipo IframeWhiteListUrl com 2), lida em {DATA}." + SEM_FN)

settings("InvocableActionSettings", "InvocableAction",
         "Configurações de ações invocáveis da org, como permitir o salvamento parcial.",
         "Recuperar e implantar como a org trata falhas quando várias ações invocáveis rodam juntas pela REST API.", "47.0", [
             P("isPartialSaveAllowed", "boolean", None, "Indica se o salvamento parcial vale para a maioria das ações invocáveis chamadas em lote pela "
               "REST API. Com true, o Salesforce tenta três vezes as ações que dão certo e desfaz só as que falham; com false, uma falha desfaz as "
               "demais ações da transação, e a transação inteira falha.",
               notas=["Corresponde à atualização crítica \"Enable Partial Save for Invocable Actions\". A página não declara default."]),
         ])

settings("PicklistSettings", "Picklist",
         "Configurações de picklist da org.",
         "Recuperar e implantar a trava que impede mudar o nome de API dos valores de picklist.", "47.0", [
             P("isPicklistApiNameEditDisabled", "boolean", None, "Com true, ninguém, nem administradores com Customize Application, consegue mudar o "
               "nome de API de um valor de picklist. Isso protege fórmulas e integrações (como importações), que usam o nome de API e continuam "
               "funcionando mesmo quando o rótulo muda.", default=FALSE),
         ])

settings("RecordPageSettings", "RecordPage",
         "Configurações de página de registro da org.",
         "Recuperar e implantar a visualização padrão das páginas de registro e das atividades.", "47.0", [
             P("enableActivityRelatedList", "boolean", None, "Define se a visualização padrão de atividades usa listas relacionadas (true) ou a linha do "
               "tempo de atividades (false)."),
             P("enableDynamicForms", "boolean", None, "Indicava se o Dynamic Forms estava ligado na org.", ate="49.0",
               notas=["A página diz que o campo foi removido na API 50.0 e posteriores; a ligação do Dynamic Forms no mobile está em DynamicFormsSettings."]),
             P("enableFullRecordView", "boolean", None, "Define se a página de registro abre por padrão na visualização completa (true) ou agrupada (false)."),
         ])

settings("SchemaSettings", "Schema",
         "Configurações de schema da org: controlam onde ficam disponíveis os valores de custom settings e de custom metadata types.",
         "Recuperar e implantar as restrições de acesso a custom settings e custom metadata types.", None, [
             P("enableAdvancedCMTSecurity", "boolean", None, "Com true, os valores de custom metadata types só ficam disponíveis para Apex, Flow e "
               "fórmulas; com false, aparecem também em outros contextos, como o Enterprise WSDL e a SOAP API.", default=FALSE),
             P("enableAdvancedCSSecurity", "boolean", None, "A mesma restrição de enableAdvancedCMTSecurity, aplicada aos valores de custom settings.",
               default=FALSE),
             P("enableListCustomSettingCreation", "boolean", None, "Indica se dá para criar custom settings do tipo lista (definição de dados no nível "
               "do app).", default=FALSE),
             P("enableSOSLOnCustomSettings", "boolean", None, "Indica se os valores de custom settings voltam em buscas SOSL.", default=FALSE),
         ], divergencias=["A seção Version da página (src:mdapi-schemasettings) não traz número de versão; o exemplo de package.xml usa 47.0. "
                          "O catálogo não registra versão inicial."])

settings("MacroSettings", "Macro",
         "Configurações de macros da org, como o uso de pastas.",
         "Recuperar e implantar a busca em macros e a organização delas em pastas.", "39.0", [
             P("enableAdvancedSearch", "boolean", None, "Indica se os usuários podem buscar em todos os campos de texto das macros."),
             P("macrosInFolders", "boolean", "44.0", "Indica se os usuários podem organizar e compartilhar macros em pastas."),
         ])

settings("SandboxSettings", "Sandbox",
         "Configurações de sandbox da org de produção.",
         "Recuperar e implantar se a org de produção envia avisos de expiração de sandboxes.", "56.0", [
             P("disableSandboxExpirationEmails", "boolean", None, "Com true, a org de origem (produção) deixa de enviar os e-mails que avisam da exclusão "
               "próxima de sandboxes sem uso há 180 dias ou mais."),
         ])

emit_structs()

# Classificação funcional: tipos do mesmo assunto de uma funcionalidade existente.
for fid, n, papel in [
    ("acoes-rapidas", "ActionsSettings", "Liga as ações rápidas padrão, o publicador multidimensional e ações de terceiros."),
    ("campos-customizados", "CustomAddressFieldSettings", "Libera o tipo Address para campos customizados (sem volta)."),
    ("campos-customizados", "PicklistSettings", "Trava a mudança do nome de API dos valores de picklist."),
    ("dynamic-forms", "DynamicFormsSettings", "Liga o Dynamic Forms no mobile (Beta)."),
    ("dynamic-forms", "RecordPageSettings", "Visualização padrão da página de registro e das atividades."),
    ("email-templates", "EmailTemplateSettings", "Liga pastas e compartilhamento aprimorado para modelos de e-mail."),
    ("visualforce", "IframeWhiteListUrlSettings", "Domínios externos autorizados a exibir páginas Visualforce (e pesquisas) em iframe."),
    ("flow", "InvocableActionSettings", "Salvamento parcial das ações invocáveis chamadas em lote pela REST API."),
    ("custom-metadata-types", "SchemaSettings", "Restringe onde valores de custom metadata types e custom settings ficam disponíveis."),
    ("sandboxes", "SandboxSettings", "Desliga os avisos de expiração de sandboxes enviados pela produção."),
]:
    C.ampliar_funcionalidade(fid, mdts=[(n, papel)], srcs=[S(n)])

SEM_OBJ = [{"tipo": "objeto_api", "estado": "desconhecido", "motivo": "Objetos API ligados a esta funcionalidade não foram investigados neste lote; a lista vazia não comprova inexistência."}]
SETUP_DESC = af("desconhecido", None, "Caminho no Setup não validado nesta sessão.")
C.funcionalidade(
    "nomes-de-pessoa", "Partes do nome de pessoa", "Name Settings", ["nome do meio", "sufixo do nome"],
    "As partes opcionais do nome nos objetos de pessoa (Contact, Lead, Person Account e User): nome do meio e sufixo.",
    "Decidir se a org guarda nome do meio e sufixo nos registros de pessoa.",
    "Uma org com clientes nos EUA liga o sufixo para registrar \"Jr.\" e \"III\" no nome dos contatos.",
    ("dados-e-modelagem", "campos-e-tipos"), [],
    [("NameSettings", "Liga ou desliga nome do meio e sufixo nos objetos de pessoa.")], [], [S("NameSettings")],
    [{"tipo": "objeto_api", "estado": "desconhecido", "motivo": "Os campos MiddleName e Suffix dos objetos de pessoa não foram conferidos neste lote."}],
    SETUP_DESC)
C.funcionalidade(
    "code-builder", "Code Builder", "Code Builder", ["IDE no navegador"],
    "Ambiente de desenvolvimento da Salesforce que roda no navegador, instalado na org como pacote.",
    "Desenvolver e implantar código e metadados sem instalar ferramentas no computador.",
    "Uma pessoa desenvolvedora abre o Code Builder pelo navegador e edita um Lightning web component sem configurar a máquina.",
    ("desenvolvimento-testes-e-entrega", "codigo-e-bundles"), [],
    [("CodeBuilderSettings", "Liga o Code Builder, permitindo instalar e usar o pacote.")], [], [S("CodeBuilderSettings")], SEM_OBJ, SETUP_DESC,
    limitacoes=["A fonte lida é só a página do tipo de configuração; detalhes do produto não foram lidos neste lote."])
C.funcionalidade(
    "importacao-de-dados", "Importação de contatos e leads", "Data Import Management", ["Basic Data Import", "importação guiada"],
    "Importação guiada de contatos e leads para a org.",
    "Trazer contatos e leads de planilhas ou outros sistemas com um passo a passo.",
    "Depois de um evento, a equipe importa a lista de inscritos como leads seguindo o assistente.",
    ("dados-e-modelagem", "objetos-e-entidades"),
    [("processos-de-negocio-especificos-de-produto", "vendas", "Os registros importados são contatos e leads, objetos do processo de vendas.")],
    [("DataImportManagementSettings", "Liga a Basic Data Import.")], [], [S("DataImportManagementSettings")], SEM_OBJ, SETUP_DESC,
    alertas=["O tipo só existe quando a org tem a permissão DataImportManagement, disponível em algumas edições."],
    limitacoes=["A fonte lida é só a página do tipo de configuração; outras ferramentas de importação não foram cadastradas."])
C.funcionalidade(
    "notas-aprimoradas", "Notas aprimoradas", "Enhanced Notes", ["Notes", "notas"],
    "Notas que podem ser ligadas a vários registros, com histórico de versões e formatação avançada.",
    "Registrar anotações sobre clientes e negócios e transformar itens das notas em tarefas.",
    "Depois de uma reunião, a vendedora anota os próximos passos na oportunidade e cria uma tarefa a partir de uma linha da nota.",
    ("conteudo-conhecimento-e-colaboracao", "files-e-documentos"), [],
    [("EnhancedNotesSettings", "Liga as notas aprimoradas e as tarefas a partir de notas.")], [], [S("EnhancedNotesSettings")], SEM_OBJ, SETUP_DESC,
    pre=["Permissão Use New Notes para os usuários."])
C.funcionalidade(
    "destino-da-ajuda", "Destino da Ajuda", "Help Settings", ["URL alternativa da Ajuda"],
    "Configuração que leva o usuário a uma URL alternativa quando ele abre a Ajuda do Salesforce.",
    "Mandar os usuários para uma central de ajuda interna em vez de help.salesforce.com.",
    "Uma empresa troca o destino da Ajuda pela wiki interna com os procedimentos dela.",
    ("interface-e-experiencia-do-usuario", "aplicativos-e-navegacao"), [],
    [("HelpSettings", "Guarda a URL alternativa da Ajuda.")], [], [S("HelpSettings")], SEM_OBJ, SETUP_DESC)
C.funcionalidade(
    "macros", "Macros", "Macros", ["macro"],
    "Sequências de passos gravadas que o usuário executa com um clique para repetir tarefas comuns.",
    "Acelerar tarefas repetitivas e padronizar a execução, organizando as macros em pastas.",
    "Um atendente aplica uma macro que preenche a resposta padrão e muda o status do caso de uma vez.",
    ("automacao-de-processos-e-regras-de-negocio", "acoes-e-regras"),
    [("processos-de-negocio-especificos-de-produto", "atendimento", "O exemplo do projeto é de atendimento; a página do tipo não restringe macros a uma nuvem.")],
    [("MacroSettings", "Busca em macros e organização em pastas.")], [], [S("MacroSettings")], SEM_OBJ, SETUP_DESC,
    limitacoes=["A fonte lida é só a página do tipo de configuração; o metadata type das macros em si não foi cadastrado neste lote."])

print("lote 9a: 16 Settings cadastrados")
