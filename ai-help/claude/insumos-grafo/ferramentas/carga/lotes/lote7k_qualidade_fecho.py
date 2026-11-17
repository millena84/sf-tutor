"""Lote 7k (fecho da rodada B3, issue #34): funcionalidades para os temas de Qualidade, governança e ciclo de vida que não tinham nenhuma.

Cadastra o metadata type PrivacySettings e os objetos API Individual, ContactPointTypeConsent, DataUsePurpose e FieldHistoryArchive
(guia versionado 264.0). Cria as funcionalidades field-history-tracking, field-audit-trail, recycle-bin, data-classification e
consent-management.

Ordem: lote7j_observabilidade_fecho.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7k_qualidade_fecho.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga import obj as O                    # noqa: E402
from carga.base import af, ev, ld, caminho    # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7k-qualidade-fecho.txt"
ATLAS = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"


def substituir_fontes(novas):
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


substituir_fontes([C.fonte("src:mdapi-privacysettings", "PrivacySettings (Metadata API)", ATLAS + "meta_privacysettings.htm",
                           "Arquivo, versão e propriedades do tipo PrivacySettings.", EXTR, DATA)]
                  + [C.fonte_objref(n, EXTR, DATA) for n in ("Individual", "ContactPointTypeConsent", "DataUsePurpose", "FieldHistoryArchive")])
S_PRIV = "src:mdapi-privacysettings"
S_IND, S_CPTC, S_DUP, S_FHA = "src:objref-individual", "src:objref-contactpointtypeconsent", "src:objref-datausepurpose", "src:objref-fieldhistoryarchive"
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
B = "boolean"
FALSE = ("false", False, "A página declara default false.")

# ================================================================ PrivacySettings
AUT = "Na autorização de consentimento, guarda {}."
M.mdt("PrivacySettings", S_PRIV,
      "Configurações de privacidade da org: consentimento de autorização, nível de sensibilidade padrão, fluxo de eventos de consentimento e "
      "Salesforce Archive.",
      "Recuperar e implantar as opções de privacidade e de classificação de dados em vez de marcá-las à mão em cada ambiente.", "47.0", [
          P("authorizationCaptureBrowser", B, "59.0", AUT.format("os dados do navegador"), default=FALSE),
          P("authorizationCaptureEmail", B, "59.0", AUT.format("o endereço de e-mail"), default=FALSE),
          P("authorizationCaptureIp", B, "59.0", AUT.format("o endereço IP"), default=FALSE),
          P("authorizationCaptureLocation", B, "59.0", AUT.format("a localização"), default=FALSE),
          P("authorizationCustomSharing", B, "59.0", "Liga o compartilhamento customizado dos registros de consentimento de autorização.", default=FALSE),
          P("authorizationCustomSharingPCU", B, "62.0", "O compartilhamento customizado desses registros usa acesso por permissão.", default=FALSE),
          P("authorizationLockingAndVersioning", B, "59.0", "Liga bloqueio e versionamento dos registros de consentimento de autorização.", default=FALSE),
          P("enableConfigurableUserPIIActive", B, "59.0", "Ativa a classificação configurável de dados pessoais de usuários.", default=FALSE),
          P("enableConsentAuditTrail", B, None, "Reservado para uso futuro."),
          P("enableConsentEventStream", B, "47.0", "Publica as mudanças de consentimento como platform events (Consent Event Stream).", default=FALSE),
          P("enableDefaultMetadataValues", B, "47.0", "Aplica um nível de sensibilidade padrão a contatos, leads, contas pessoais e usuários.",
            default=FALSE),
          P("enableSalesforceArchive", B, "61.0", "Liga o Salesforce Archive para arquivar dados ligados à privacidade.", default=FALSE),
          P("useUmaDefaultConsentRecs", B, "58.0", "O Preference Manager do Privacy Center usa as configurações de consentimento padrão do Marketing Cloud.",
            default=FALSE),
          M.FULLNAME_HERDADO(None),
      ], exemplo=CAB + f"""<PrivacySettings {NS}>
    <enableConsentEventStream>false</enableConsentEventStream>
    <enableDefaultMetadataValues>false</enableDefaultMetadataValues>
</PrivacySettings>""", arquivos_prontos=M.arquivos_settings("PrivacySettings", "Privacy", S_PRIV), curinga=True,
      alertas=["Acessar o tipo exige a permissão Customize Application ou Modify Data Classification.",
               "A página diz que o curinga (*) é aceito; no manifesto, o tipo entra como Settings, membro Privacy."],
      cobertura_nota="Universo esperado = tabela Fields da página do guia versionado 264.0 (API 68.0), lida em 2026-11-17: 13 campos, todos "
                     "boolean. A página não informa obrigatoriedade.")
M.emit_structs()

# ================================================================ objetos API
TOOL_D = lambda: O.expo("tooling", "desconhecido", nota="Exposição na Tooling API não verificada.")  # noqa: E731
DPP = "Só existe com Data Protection and Privacy habilitado."
SIM = ("sim", None)

I_ = "obj:Individual"
OPT = "Preferência do cliente contra {}."
ind = [
    O.field(I_, "BirthDate", "date", "CFGNSU", None, "Data de nascimento.", S_IND),
    O.field(I_, "CanStorePiiElsewhere", B, "CDFGSU", None, "Se os dados pessoais podem ficar fora da jurisdição legal do cliente.", S_IND),
    O.field(I_, "ChildrenCount", "int", "CFGNSU", None, "Número de filhos.", S_IND),
    O.field(I_, "ConsumerCreditScore", "int", "CFGNSU", None, "Pontuação de crédito.", S_IND),
    O.field(I_, "ConsumerCreditScoreProviderName", "string", "CFGNSU", None, "Empresa que forneceu a pontuação de crédito.", S_IND),
    O.field(I_, "ConvictionsCount", "int", "CFGNSU", None, "Número de condenações.", S_IND),
    O.field(I_, "DeathDate", "date", "CFGNSU", None, "Data de falecimento.", S_IND),
    O.field(I_, "FirstName", "string", "CFGNSU", None, "Nome; até 40 caracteres.", S_IND),
    O.field(I_, "HasOptedOutGeoTracking", B, "CDFGSU", None, OPT.format("rastreamento de geolocalização em dispositivos móveis"), S_IND),
    O.field(I_, "HasOptedOutProcessing", B, "CDFGSU", None, OPT.format("o processamento dos dados pessoais, inclusive guardá-los e compartilhá-los"), S_IND),
    O.field(I_, "HasOptedOutProfiling", B, "CDFGSU", None, OPT.format("o uso dos dados para prever traços e comportamento pessoais"), S_IND),
    O.field(I_, "HasOptedOutSolicit", B, "CDFGSU", None, OPT.format("receber ofertas de produtos ou serviços"), S_IND),
    O.field(I_, "HasOptedOutTracking", B, "CDFGSU", None, OPT.format("rastreamento de atividade web e de abertura de e-mail"), S_IND),
    O.field(I_, "HasPrivacyHold", B, "CDFGSU", None, "Indica se há um Privacy Hold em vigor.", S_IND),
    O.field(I_, "IndividualsAge", "picklist", "CFGNSU", None, "Se o cliente é considerado menor de idade.", S_IND),
    O.field(I_, "InfluencerRating", "int", "CFGNSU", None, "Medida de influência da pessoa, independentemente da relação comercial.", S_IND),
    O.field(I_, "IsHomeOwner", B, "CDFGSU", None, "Se o cliente é dono de imóvel.", S_IND),
    O.field(I_, "LastName", "string", "CFGSU", None, "Sobrenome; até 80 caracteres.", S_IND, req=SIM),
    O.field(I_, "LastViewedDate", "dateTime", "FNS", None, "Quando o usuário atual viu o registro pela última vez.", S_IND),
    O.field(I_, "MasterRecordId", "reference", "FGNS", None, "Depois de um merge, o registro que sobreviveu; senão, nulo.", S_IND, ref=["obj:Individual"],
            rel="MasterRecord"),
    O.field(I_, "MilitaryService", "picklist", "CFGNSU", None, "Se o cliente serviu nas forças armadas.", S_IND),
    O.field(I_, "Name", "string", "FGS", None, "FirstName e LastName juntos; até 203 caracteres.", S_IND),
    O.field(I_, "Occupation", "string", "CFGNSU", None, "Profissão; até 150 caracteres.", S_IND),
    O.field(I_, "OwnerId", "reference", "CDFGSU", None, "Dono da conta ligada ao cliente.", S_IND, ref=["obj:User"], rel="Owner"),
    O.field(I_, "Salutation", "picklist", "CFGNSU", None, "Forma de tratamento, como Dr. ou Sra.", S_IND),
    O.field(I_, "SendIndividualData", B, "CDFGSU", None, "Preferência por receber a exportação dos próprios dados pessoais.", S_IND),
    O.field(I_, "ShouldForget", B, "CDFGSU", None, "Preferência por ter os registros e dados pessoais excluídos.", S_IND),
    O.field(I_, "Website", "url", "CFGNSU", None, "Site do cliente.", S_IND),
]
O.obj("Individual",
      "O registro de privacidade de uma pessoa: as preferências sobre coleta, processamento, rastreamento, contato, exportação e exclusão dos "
      "dados dela. Leads, contatos, contas pessoais e usuários podem apontar para ele.",
      "Guardar e consultar, num só lugar, o que cada pessoa decidiu sobre o uso dos próprios dados.",
      [O.expo("padrao", "verificado", S_IND, ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "merge()",
                                              "query()", "retrieve()", "search()", "undelete()", "update()", "upsert()"],
              desde="42.0", acesso=DPP), TOOL_D()],
      ind,
      [{"api": "padrao", "soql": "SELECT Name, HasOptedOutTracking, HasOptedOutSolicit, ShouldForget FROM Individual WHERE ShouldForget = true",
        "contexto": "API padrão. Lista as pessoas que pediram para ter os dados excluídos.", "validacao": "documental"}],
      O.APEX_OK(S_IND), O.cob("completa", 28, 28, O.cnt(ind), "Tabela de campos lida completa (28); a página não lista valores dos picklists."), S_IND,
      alertas=["Os campos de preferência só registram o que a pessoa pediu: cumprir o pedido é responsabilidade do processo da empresa.",
               "A página não lista os valores dos picklists (IndividualsAge, MilitaryService, Salutation).",
               "Há objetos associados: IndividualChangeEvent (desde a API 47.0), IndividualHistory e IndividualShare."])

T = "obj:ContactPointTypeConsent"
CANAIS = ["Email", "MailingAddress", "Phone", "Social", "Web"]
cptc = [
    O.field(T, "BusinessBrandId", "reference", "CFGNSU", "53.0", "A marca a que a pessoa deu o consentimento para este canal.", S_CPTC, ref=["BusinessBrand"],
            rel="BusinessBrand"),
    O.field(T, "CaptureContactPointType", "picklist", "CFGNRSU", None, "Canal pelo qual o consentimento foi obtido.", S_CPTC, vals=CANAIS, completa="sim", req=SIM),
    O.field(T, "CaptureDate", "dateTime", "CFNSU", None, "Quando o consentimento foi obtido.", S_CPTC, req=SIM),
    O.field(T, "CaptureSource", "string", "CFGNSU", None, "Como o consentimento foi obtido, como um formulário online.", S_CPTC, req=SIM),
    O.field(T, "ContactPointType", "picklist", "CFGNRSU", None, "Canal a que o consentimento se aplica.", S_CPTC, vals=CANAIS, completa="sim", req=SIM),
    O.field(T, "DataUsePurposeId", "reference", "CFGNSU", None, "A finalidade de uso ligada ao consentimento.", S_CPTC, ref=["obj:DataUsePurpose"],
            rel="DataUsePurpose"),
    O.field(T, "DoubleConsentCaptureDate", "dateTime", "CFNSU", None, "Quando o double opt-in foi concluído.", S_CPTC),
    O.field(T, "EffectiveFrom", "dateTime", "CFNSU", None, "Início da validade do consentimento.", S_CPTC),
    O.field(T, "EffectiveTo", "dateTime", "CFNSU", None, "Fim da validade do consentimento.", S_CPTC),
    O.field(T, "EngagementChannelType", "picklist", "CFGNRSU", None, "Canal a que o consentimento se aplica, quando ContactPointType não é informado.",
            S_CPTC, vals=["Billboard", "Email", "MailingAddress", "Phone", "SMS", "Social", "Web"], completa="sim",
            notas=["A página também descreve o campo como relacionamento com EngagementChannelType."]),
    O.field(T, "LastReferencedDate", "dateTime", "FNS", None, "Quando o usuário atual viu um registro relacionado pela última vez.", S_CPTC),
    O.field(T, "LastViewedDate", "dateTime", "FNS", None, "Quando o usuário atual viu este registro pela última vez.", S_CPTC),
    O.field(T, "Name", "string", "CFGISU", None, "Nome do registro de consentimento.", S_CPTC),
    O.field(T, "OwnerId", "reference", "CDFGSU", None, "Dono do registro.", S_CPTC, ref=["obj:Group", "obj:User"], rel="Owner"),
    O.field(T, "PartyId", "reference", "CFGSU", None, "A pessoa (Individual) que deu o consentimento.", S_CPTC, ref=["obj:Individual"], rel="Party", req=SIM),
    O.field(T, "PartyRoleId", "reference", "CFGNSU", "53.0", "O papel da pessoa neste consentimento.", S_CPTC, ref=["Customer", "Seller"], rel="PartyRole"),
    O.field(T, "PrivacyConsentStatus", "picklist", "CDFGRSU", None, "Se a pessoa aceita esta forma de contato.", S_CPTC,
            vals=["NotSeen", "Seen", "OptIn", "OptInPending", "OptOut", "OptOutPending"], completa="sim", req=SIM,
            notas=["OptInPending e OptOutPending existem desde a API 58.0. A página dá só os nomes dos valores."]),
]
O.obj("ContactPointTypeConsent",
      "O consentimento de uma pessoa para um canal de contato, como e-mail ou telefone, com a finalidade, a marca, a origem e o período de validade.",
      "Registrar e consultar, canal a canal, o que cada pessoa aceitou ou recusou.",
      [O.expo("padrao", "verificado", S_CPTC, ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()",
                                               "retrieve()", "search()", "undelete()", "update()", "upsert()"], desde="45.0", acesso=DPP), TOOL_D()],
      cptc,
      [{"api": "padrao", "soql": "SELECT PartyId, ContactPointType, PrivacyConsentStatus, EffectiveFrom FROM ContactPointTypeConsent WHERE ContactPointType = 'Email'",
        "contexto": "API padrão. Lista os consentimentos de e-mail.", "validacao": "documental"}],
      O.APEX_OK(S_CPTC), O.cob("completa", 17, 17, O.cnt(cptc), "Tabela de campos lida completa (17)."), S_CPTC,
      alertas=["A visibilidade e a edição dos campos dependem do page layout e da segurança de campo.",
               "Há histórico de campos rastreados (ContactPointTypeConsentHistory) e compartilhamento próprio (sharing rules e ContactPointTypeConsentShare)."])

D = "obj:DataUsePurpose"
dup = [
    O.field(D, "CanDataSubjectOptOut", B, "CDFGSU", None, "Se a pessoa pode recusar contato para esta finalidade.", S_DUP, req=SIM),
    O.field(D, "Description", "string", "CFGNSU", None, "Por que a pessoa é contatada.", S_DUP),
    O.field(D, "LastReferencedDate", "dateTime", "FNS", None, "Quando o usuário atual viu um registro relacionado pela última vez.", S_DUP),
    O.field(D, "LastViewedDate", "dateTime", "FNS", None, "Quando o usuário atual viu este registro pela última vez.", S_DUP),
    O.field(D, "LegalBasisId", "reference", "CFGNSU", None, "A base legal da finalidade.", S_DUP, ref=["DataUseLegalBasis"], rel="LegalBasis"),
    O.field(D, "Name", "string", "CFGISU", None, "A finalidade, como cobrança ou marketing.", S_DUP, req=SIM),
    O.field(D, "OwnerId", "reference", "CDFGSU", None, "Dono do registro.", S_DUP, ref=["obj:Group", "obj:User"], rel="Owner"),
    O.field(D, "PurposeId", "reference", "CFGNSU", None, "Registro com dados próprios da finalidade.", S_DUP, ref=["Asset", "CareProgram", "CareRegisteredDevice",
                                                                                                                 "Product2"], rel="Purpose"),
]
O.obj("DataUsePurpose",
      "Uma finalidade de uso de dados: o motivo de contatar alguém, como cobrança, marketing ou pesquisa, e se a pessoa pode recusar.",
      "Cadastrar as finalidades a que os consentimentos se referem.",
      [O.expo("padrao", "verificado", S_DUP, ["create()", "delete()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()",
                                              "retrieve()", "search()", "undelete()", "update()", "upsert()"], desde="45.0", acesso=DPP), TOOL_D()],
      dup,
      [{"api": "padrao", "soql": "SELECT Name, CanDataSubjectOptOut, Description FROM DataUsePurpose",
        "contexto": "API padrão. Lista as finalidades cadastradas.", "validacao": "documental"}],
      O.APEX_OK(S_DUP), O.cob("completa", 8, 8, O.cnt(dup), "Tabela de campos lida completa (8)."), S_DUP,
      alertas=["Há eventos de mudança (DataUsePurposeChangeEvent, desde a API 62.0), histórico e compartilhamento próprios."])

F = "obj:FieldHistoryArchive"
TIPOS_FHA = ["Account", "Article", "Asset", "AuthorizationFormConsent", "Case", "CommSubscriptionConsent", "Contact", "ContactPointConsent",
             "ContactPointTypeConsent", "Contract", "ContractLineItem", "Crisis", "Employee", "EmployeeCrisisAssessment", "Entitlement", "Individual",
             "InternalOrganizationUnit", "Knowledge", "Lead", "Opportunity", "Order", "OrderItem", "PartyConsent", "Pricebook2", "PricebookEntry", "Product2",
             "ServiceAppointment", "ServiceContract", "Solution", "WorkOrder", "WorkOrderLineItem"]
RENOMEIA = "{} no momento do arquivamento; pode variar entre registros depois de renomeações."
fha = [
    O.field(F, "ArchiveFieldName", "string", "N", None, RENOMEIA.format("Nome do campo"), S_FHA),
    O.field(F, "ArchiveParentName", "string", "N", None, RENOMEIA.format("Nome do objeto pai"), S_FHA),
    O.field(F, "ArchiveParentType", "string", "N", None, "Tipo do campo no momento do arquivamento; pode variar depois de mudanças de tipo.", S_FHA),
    O.field(F, "ArchiveTimestamp", "dateTime", "N", None, "Quando o dado foi arquivado.", S_FHA),
    O.field(F, "Field", "picklist", "R", None, "Campo alterado; mostra o Id se o campo ou o objeto pai foi excluído.", S_FHA),
    O.field(F, "FieldHistoryType", "picklist", "FNRS", None, "Objeto pai cujo histórico é guardado.", S_FHA, vals=TIPOS_FHA, completa="sim",
            notas=["AuthorizationFormConsent, CommSubscriptionConsent, ContactPointConsent, ContactPointTypeConsent e PartyConsent existem desde a API 58.0."]),
    O.field(F, "HistoryId", "reference", "FS", "42.0", "O registro do objeto de histórico correspondente, como AccountHistory.", S_FHA,
            notas=["A página não lista os objetos referenciados um a um."]),
    O.field(F, "NewValue", "anyType", "N", None, "Novo valor do campo.", S_FHA),
    O.field(F, "OldValue", "anyType", "N", None, "Valor anterior do campo.", S_FHA),
    O.field(F, "ParentId", "reference", "FS", None, "O registro que contém o campo.", S_FHA, notas=["A página não lista os objetos referenciados."]),
]
O.obj("FieldHistoryArchive",
      "Um big object com o histórico arquivado de campos de todos os objetos que retêm histórico: cada registro é uma mudança de valor de um campo.",
      "Consultar por API o histórico guardado pelo Field Audit Trail, além do prazo do histórico comum.",
      [O.expo("padrao", "verificado", S_FHA, ["describeSObjects()", "query()"], desde="29.0",
              acesso="Só para usuários com a permissão Retain Field History."), TOOL_D()],
      fha,
      [{"api": "padrao", "soql": "SELECT FieldHistoryType, ParentId, Field, OldValue, NewValue FROM FieldHistoryArchive WHERE FieldHistoryType = 'Account'",
        "contexto": "API padrão. Histórico arquivado de contas.", "validacao": "documental"}],
      {"consulta_soql_direta": af("desconhecido", None, "Não verificado se o big object é consultável por SOQL comum em Apex."),
       "nota": "A página só lista describeSObjects() e query()."},
      O.cob("completa", 10, 10, O.cnt(fha), "Tabela de campos lida completa (10). A página cita FieldNameAfterArchival e ParentNameAfterArchival fora da tabela."),
      S_FHA,
      alertas=["É um big object: só aceita describeSObjects() e query(), sem criar, alterar ou excluir pela API.",
               "Ao ordenar, a página indica a sequência FieldHistoryType crescente, ParentId crescente e CreatedDate decrescente.",
               "Quando o campo ou o objeto pai foi excluído, Field devolve o Id; a página cita FieldNameAfterArchival e ParentNameAfterArchival para os "
               "nomes antigos, mas não os lista na tabela."])

C.rel_lookup("cptc-individual", T, "PartyId", I_, "Cada consentimento de canal pertence a uma pessoa (Individual).", S_CPTC)
C.rel_lookup("cptc-datausepurpose", T, "DataUsePurposeId", D, "O consentimento de canal pode apontar a finalidade de uso a que se refere.", S_CPTC)
C.rel_lookup("individual-master", I_, "MasterRecordId", I_, "Depois de um merge, o registro excluído aponta o que sobreviveu.", S_IND)

# ================================================================ nota de extração: lista de campos
ls = ["", "-- Lista de campos transcrita da leitura (gerada por lote7k_qualidade_fecho.py; nome | tipo)"]
ls.append(f"[{S_PRIV}] PrivacySettings: " + ", ".join(f"{q['nome']} | {q['tipo_tecnico']}" for q in ld("metadata-types/PrivacySettings.json")["propriedades"]))
for src, nome, campos in ((S_IND, "Individual", ind), (S_CPTC, "ContactPointTypeConsent", cptc), (S_DUP, "DataUsePurpose", dup), (S_FHA, "FieldHistoryArchive", fha)):
    ls.append(f"[{src}] objeto {nome}: " + ", ".join(f"{c['nome']} | {c['tipo_tecnico']}" for c in campos))
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(ls) + "\n")

# ================================================================ funcionalidades
QUA = "qualidade-governanca-e-ciclo-de-vida-dos-dados"


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


def sem(tipo_, motivo, estado="desconhecido"):
    return {"tipo": tipo_, "estado": estado, "motivo": motivo}


C.funcionalidade(
    "field-history-tracking", "Field History Tracking", "Field History Tracking", ["histórico de campos", "field history", "set history tracking",
                                                                                   "history related list", "accounthistory", "auditoria de campos"],
    "Field History Tracking registra as mudanças nos campos escolhidos de um objeto: quem mudou, quando, o valor anterior e o novo. O histórico "
    "fica num objeto relacionado, como AccountHistory ou MyCustomObject__History, e aparece na related list History do registro.",
    "Saber quem alterou o quê e quando, para auditoria e para entender a evolução de um registro.",
    "Na conta, o campo Rating é rastreado; quando alguém muda de Warm para Hot, a related list History mostra o usuário, a data e os dois valores.",
    (QUA, "rastreabilidade-e-historico"), [],
    [("CustomObject", "Liga o rastreamento no objeto (enableHistory)."), ("CustomField", "Escolhe cada campo rastreado (trackHistory).")], [],
    ["src:help-field-history-tracking", "src:help-track-object-field-history", "src:help-disable-field-history", "src:help-kb-account-date-history",
     "src:help-field-history-security", "src:mdapi-customobject", "src:mdapi-customfield"],
    [sem("objeto_api", "Os objetos de histórico (AccountHistory, <Objeto>History, <Objeto>__History) não foram cadastrados; só IndividualHistory e "
         "ContactPointTypeConsentHistory são citados nas páginas lidas.")],
    setup("Setup > Object Manager > [objeto] > Fields & Relationships > Set History Tracking", "src:help-kb-account-date-history",
          "Marque Enable [objeto] History e escolha os campos."),
    limitacoes=["Até 20 campos por objeto; em eventos e tarefas, até 6.",
                "Sem Field Audit Trail, o histórico fica até 18 meses (até 24 pela API)."],
    alertas=["O histórico só existe a partir de quando o rastreamento é ligado.",
             "Em contas, o limite de 20 campos vale para contas comerciais e contas pessoais juntas.",
             "Não é possível desligar o rastreamento de um objeto se algum código Apex referencia os campos dele.",
             "O histórico de campos não conta no armazenamento de dados.",
             "Definir os campos rastreados exige a permissão Customize Application."])

C.funcionalidade(
    "field-audit-trail", "Field Audit Trail", "Field Audit Trail", ["fieldhistoryarchive", "historyretentionpolicy", "retenção de histórico",
                                                                   "retain field history", "auditoria de longo prazo"],
    "Field Audit Trail amplia o Field History Tracking: rastreia até 200 campos por objeto e guarda o histórico até ele ser excluído, num big "
    "object (FieldHistoryArchive). Uma política de retenção por objeto diz quantos meses o histórico fica no objeto de histórico antes de ser "
    "arquivado.",
    "Cumprir exigências de auditoria e de conformidade que pedem histórico por anos, não por meses.",
    "Uma financeira precisa provar, cinco anos depois, quem alterou o limite de crédito de uma conta; o dado está em FieldHistoryArchive.",
    (QUA, "retencao-arquivamento-e-exclusao"), [(QUA, "rastreabilidade-e-historico", "É a extensão do histórico de campos.")],
    [("CustomObject", "A política de retenção do objeto (historyRetentionPolicy).")],
    [("FieldHistoryArchive", "O histórico arquivado, consultado só por API.")],
    ["src:help-field-audit-trail", "src:mdapi-historyretentionpolicy", "src:mdapi-customobject", S_FHA, "src:help-field-history-security"], [],
    af("desconhecido", None, "Caminho de Setup não lido.", []),
    limitacoes=["Até 200 campos por objeto, contra 20 do rastreamento padrão.", "O histórico arquivado só é acessível por API."],
    alertas=["A política padrão arquiva depois de 18 meses em produção e de um mês em sandbox, e não vem no retrieve: para mudá-la, implante "
             "uma política pela Metadata API.",
             "Excluir um registro apaga o histórico relacionado, mas não a cópia já levada para FieldHistoryArchive.",
             "Consultar FieldHistoryArchive exige a permissão Retain Field History."])

C.funcionalidade(
    "recycle-bin", "Recycle Bin", "Recycle Bin", ["lixeira", "recycle bin", "undelete", "restaurar registro", "soft delete", "hard delete", "isdeleted"],
    "A Recycle Bin guarda por 15 dias os itens excluídos, que podem ser restaurados nesse prazo. Depois, eles são agendados para exclusão "
    "permanente. Esvaziar a lixeira ou usar o hard delete da API manda os registros direto para a fila de exclusão definitiva.",
    "Desfazer exclusões feitas por engano e entender em que momento um dado deixa de existir.",
    "Um vendedor exclui uma oportunidade por engano; no dia seguinte, ele a restaura pela Recycle Bin, com os relacionamentos.",
    (QUA, "retencao-arquivamento-e-exclusao"), [],
    [], [],
    ["src:help-recycle-bin-lex", "src:help-delete-unwanted-data"],
    [sem("metadata_type", "Não investigado se há configuração da Recycle Bin implantável por metadado."),
     sem("objeto_api", "Registros na lixeira aparecem nas consultas com isDeleted = true; nenhum objeto próprio foi investigado.")],
    af("desconhecido", None, "Caminho de acesso à Recycle Bin no Lightning Experience não confirmado nas fontes lidas.", []),
    limitacoes=["Os itens ficam 15 dias; depois, são agendados para exclusão permanente, sem hora garantida."],
    alertas=["Itens na lixeira não contam no armazenamento e não há limite de quantidade.",
             "Restaurar itens de outros usuários e excluir permanentemente exigem Modify All Data.",
             "Hard delete pela API não passa pela lixeira.",
             "Remover o registro da tabela do banco (physical delete) é um pedido ao Support, não uma ação da org."])

C.funcionalidade(
    "data-classification", "Data Classification", "Data Classification", ["classificação de dados", "data sensitivity level", "compliance categorization",
                                                                         "securityclassification", "data owner", "field usage", "pii"],
    "Data Classification marca cada campo com o nível de sensibilidade (Public, Internal, Confidential, Restricted, MissionCritical), as "
    "categorias de conformidade (como GDPR, PII ou HIPAA), o responsável pelo dado e o uso do campo. É só registro: orienta decisões, mas não "
    "muda acesso sozinho.",
    "Saber onde estão os dados sensíveis da org e quem responde por eles, para orientar acesso, relatórios e conformidade.",
    "O campo CPF__c é marcado como Restricted, com a categoria PII e o responsável Jurídico; um relatório lista todos os campos Restricted da org.",
    (QUA, "classificacao-e-sensibilidade"), [],
    [("CustomField", "Os valores de classificação de cada campo (securityClassification, complianceGroup, businessOwnerUser, businessOwnerGroup, businessStatus)."),
     ("PrivacySettings", "Liga o nível de sensibilidade padrão em contatos, leads, contas pessoais e usuários (enableDefaultMetadataValues).")], [],
    ["src:help-data-classification-intro", "src:help-data-classification-fields", "src:help-data-classification-setup", "src:help-data-classification-reports",
     "src:mdapi-customfield", S_PRIV],
    [sem("objeto_api", "FieldDefinition (Tooling API) e FieldSecurityClassification são citados na Ajuda, mas não foram cadastrados.")],
    setup("Setup > Quick Find: Data Classification Settings", "src:help-data-classification-setup",
          "Ali se escolhe usar o nível de sensibilidade padrão. Os valores de cada campo são editados no próprio campo, no Object Manager."),
    alertas=["A classificação vem habilitada em todas as orgs.",
             "Ver ou editar a classificação exige Customize Application ou Modify Data Classification.",
             "Marcar um campo em Field Usage não esconde nem expõe nada: é só registro.",
             "Para relatar sobre a classificação, crie um custom report type com Entity Definition como objeto principal."])

C.funcionalidade(
    "consent-management", "Gestão de consentimento", "Consent Management", ["consentimento", "consent", "individual", "data protection and privacy",
                                                                           "contactpointtypeconsent", "datausepurpose", "opt-in", "opt-out", "lgpd", "gdpr"],
    "A gestão de consentimento registra o que cada pessoa autorizou: em nível global, no Individual; por canal, como e-mail ou telefone, no "
    "ContactPointTypeConsent; por endereço específico, no ContactPointConsent; e por finalidade, no DataUsePurpose. Leads, contatos, contas "
    "pessoais e usuários apontam para o Individual.",
    "Atender pedidos e exigências legais sobre o uso dos dados de cada pessoa, como não receber marketing ou ter os dados excluídos.",
    "Uma cliente aceita receber e-mails de cobrança, mas recusa os de marketing: são dois consentimentos de e-mail, cada um com uma finalidade.",
    (QUA, "consentimento-e-privacidade"), [],
    [("PrivacySettings", "Opções de privacidade, como o Consent Event Stream e a captura de dados no consentimento de autorização.")],
    [("Individual", "As preferências globais de privacidade da pessoa."), ("ContactPointTypeConsent", "O consentimento por canal."),
     ("DataUsePurpose", "As finalidades de uso.")],
    ["src:help-consent-data-model", "src:help-consent-objects", "src:help-consent-event-stream", "src:help-data-privacy-setup", "src:help-kb-individual-record",
     "src:help-verify-data-protection", "src:help-enforce-email-privacy", "src:help-consent-mgmt-platform", S_PRIV, S_IND, S_CPTC, S_DUP],
    [],
    setup("Setup > Quick Find: Data Protection and Privacy > Edit > Make data protection details available in records", "src:help-kb-individual-record"),
    alertas=["Os objetos só guardam as preferências: a empresa decide como honrá-las e implementa o processo.",
             "Para os usuários verem os dados de privacidade, inclua o campo Individual nos page layouts de lead, contato e conta pessoal.",
             "Para o e-mail respeitar as preferências do Individual, ligue também Enforce Email Privacy Settings, em Deliverability.",
             "Os objetos de consentimento só existem com Data Protection and Privacy habilitado."])
print("lote 7k: 1 metadata type e 4 objetos API gravados; 5 funcionalidades novas")
