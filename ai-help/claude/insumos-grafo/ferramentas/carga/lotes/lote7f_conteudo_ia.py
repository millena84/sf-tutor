"""Lote 7f (rodadas A5 e A6, issue #34): temas Conteúdo, conhecimento e colaboração e IA, agentes e decisões assistidas.

Lê o guia versionado 264.0 (API 68.0) e cadastra 9 metadata types: EmailTemplate, Letterhead, Document, ContentAsset e
ChatterSettings (conteúdo); GenAiPromptTemplate, GenAiFunction, GenAiPlugin e EinsteinGptSettings (IA). Cria 9 funcionalidades.

As fontes de Ajuda citadas pelas funcionalidades são registradas por conteudo_temas.py (lista em conteudo_detalhe.py).
Ordem: lote7e_observabilidade.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7f_conteudo_ia.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M                    # noqa: E402
from carga.mdt import P                       # noqa: E402
from carga.base import af, ev, ld, sv, caminho  # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-16"
EXTR = "fontes/extracoes/mdapi-lote7f-conteudo-ia.txt"
ATLAS = "https://developer.salesforce.com/docs/atlas.en-us.264.0.api_meta.meta/api_meta/"
PAGINAS = {"EmailTemplate": "meta_emailtemplate", "Letterhead": "meta_letterhead", "Document": "meta_document",
           "ContentAsset": "meta_contentasset", "ChatterSettings": "meta_chattersettings",
           "GenAiPromptTemplate": "meta_genaiprompttemplate", "GenAiFunction": "meta_genaifunction", "GenAiPlugin": "meta_genaiplugin",
           "EinsteinGptSettings": "meta_einsteingptsettings"}


def substituir_fontes(novas):
    p = caminho("fontes", "registro.json")
    with open(p, encoding="utf-8") as f:
        reg = json.load(f)
    ids = {n["id"] for n in novas}
    reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
    with open(p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


substituir_fontes([C.fonte(f"src:mdapi-{n.lower()}", f"{n} (Metadata API)", ATLAS + pag + ".htm", f"Arquivo, versão e propriedades do tipo {n}.",
                           EXTR, DATA) for n, pag in PAGINAS.items()])
S_ET, S_LH, S_DOC, S_CA, S_CH, S_PT, S_FN, S_PL, S_GPT = (f"src:mdapi-{n.lower()}" for n in PAGINAS)

NOTA_COB = "Universo esperado = tabelas Fields da página do guia versionado 264.0 (API 68.0), lida em 2026-11-16."
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n'
B, S, I = "boolean", "string", "int"
FALSE = ("false", False, "A página declara default false.")
REGISTRADOS = []   # (src, nome do tipo ou estrutura), para a nota de extração


def valores(*vs):
    return [(v, None) for v in vs]


def estrutura(nome, src, usada_por, rows, o_que_e):
    M.struct(nome, src, usada_por, rows, o_que_e)
    REGISTRADOS.append((src, "estruturas", nome))


def tipo(nome, src, *a, **k):
    M.mdt(nome, src, *a, **k)
    REGISTRADOS.append((src, "metadata-types", nome))


def binario(desc):
    return P("content", "base64Binary", None, desc, natureza="texto_livre", herdada="MetadataWithContent",
             contexto="Na API, o conteúdo trafega em base64; no projeto, é o conteúdo do arquivo correspondente.")


def em_pasta(pasta, arquivo, nota, chave, src):
    a = af("verificado", {"pasta": pasta, "arquivo": arquivo}, nota, [ev("src:sdr-registry", f"types.{chave}"), ev(src)])
    return {"source_format": a, "metadata_api_format": a}


# ================================================================ EmailTemplate
estrutura("Attachment", S_ET, ["mdt:EmailTemplate"], [
    P("content", "base64Binary", None, "Conteúdo do arquivo anexado.", "S", natureza="texto_livre", contexto="Na API, o conteúdo trafega em base64."),
    P("name", S, None, "Nome do arquivo anexado.", "S"),
], "Um anexo de um email template.")
tipo("EmailTemplate", S_ET,
     "Um email template: o modelo de e-mail usado em envios individuais, em massa, de lista e do Sales Engagement.",
     "Versionar e implantar os modelos de e-mail da org.", "12.0", [
         P("apiVersion", "double", "16.0", "Versão de API de um template Visualforce, definida na criação."),
         P("attachedDocuments", "string[]", None, "Caminhos de documentos da org incluídos como anexos do template."),
         P("attachments", "Attachment[]", None, "Anexos do template.", estrutura="Attachment"),
         P("available", B, None, "Indica se o template é oferecido aos usuários ao enviar um e-mail.", "S"),
         binario("O corpo do template; o significado depende do tipo do template. Herdado de MetadataWithContent."),
         P("description", S, None, "Motivo da criação do template."),
         P("encodingKey", "Encoding", None, "Codificação de caracteres do template.", "C:obrigatório em templates do Salesforce Classic",
           default=("valor", "UTF-8", "A página informa UTF-8 como padrão."),
           vals=valores("UTF-8", "ISO-8859-1", "Shift_JIS", "ISO-2022-JP", "EUC-JP", "x-SJIS_0213", "ks_c_5601-1987", "Big5", "GB2312", "Big5-HKSCS"),
           notas=["Templates do Lightning Experience ignoram o campo e usam a codificação configurada para o usuário."]),
         P("fullName", S, None, "Nome único de API do template: letras, números e sublinhados, sem espaços. Herdado.", "?", herdada="Metadata"),
         P("letterhead", S, None, "Nome do letterhead associado. Só vale quando type é html."),
         P("name", S, None, "Nome do template.", "S"),
         P("packageVersions", "PackageVersion[]", "16.0", "Versões de pacotes gerenciados que o template referencia. Só para templates Visualforce.",
           estrutura="PackageVersion"),
         P("relatedEntityType", S, None, "Reservado para uso futuro no Lightning Experience.",
           notas=["A página descreve o tipo como uma enumeração de nomes de objeto, sem listar valores."]),
         P("style", "EmailTemplateStyle", None, "Estilo de layout do template. Só vale quando type é html.", "S",
           vals=valores("none", "freeForm", "formalLetter", "promotionRight", "promotionLeft", "newsletter", "products")),
         P("subject", S, None, "Assunto do e-mail. Até 1.000 caracteres em templates do Lightning Experience e 230 nos do Classic."),
         P("textOnly", S, None, "Texto do corpo do e-mail quando type é html ou custom."),
         P("type", "EmailTemplateType", None, "Tipo do template.", "S", vals=[
             ("text", "Texto simples; todos os usuários podem criar ou alterar."),
             ("html", "HTML com letterhead; exige ser administrador ou ter a permissão Edit HTML Templates."),
             ("custom", "HTML sem letterhead; mesma exigência do tipo html."),
             ("visualforce", "Visualforce; exige ser administrador ou ter a permissão Customize Application.")]),
         P("UiType", "EmailTemplateUiType", None, "Interface em que o template pode ser usado.", vals=[
             ("Aloha", "Salesforce Classic."), ("SFX", "Lightning Experience."), ("SFX_Sample", "Template de exemplo do Lightning Experience.")],
           notas=["O nome do campo começa com maiúscula na página.", "O valor SFX exige type custom."]),
     ], exemplo=CAB + f"""<!-- Arquivo -meta.xml que acompanha o arquivo .email (o corpo do template) -->
<EmailTemplate {NS}>
    <available>true</available>
    <description>[para que serve o template]</description>
    <encodingKey>UTF-8</encodingKey>
    <name>[nome do template]</name>
    <!-- Valores documentados: none, freeForm, formalLetter, promotionRight, promotionLeft, newsletter, products -->
    <style>none</style>
    <subject>[assunto do e-mail]</subject>
    <!-- Valores documentados: text, html, custom, visualforce -->
    <type>text</type>
</EmailTemplate>""", estende="MetadataWithContent", curinga=False,
     arquivos_prontos=em_pasta("email/<pasta>/", "<Nome>.email e <Nome>.email-meta.xml",
                               "Os templates ficam em subpastas da pasta email; cada um tem o arquivo do corpo e o arquivo de metadado.",
                               "emailtemplate", S_ET),
     alertas=["O curinga (*) não funciona no package.xml: os nomes precisam ser listados, com a pasta. A página indica listMetadata() para obtê-los.",
              "Segundo a página, o tipo só é aceito em pacotes gerenciados de primeira geração.",
              "Templates do Lightning Experience ignoram encodingKey."],
     cobertura_nota=NOTA_COB)
# PackageVersion é gravada pelo lote 7b; aqui só se acrescenta o novo uso.
_pv = ld("estruturas/PackageVersion.json")
_pv["usada_por"] = sorted(set(_pv["usada_por"]) | {"mdt:EmailTemplate"})
sv("estruturas/PackageVersion.json", _pv)

# ================================================================ Letterhead
HEX = "Cor em código hexadecimal."
estrutura("LetterheadHeaderFooter", S_LH, ["mdt:Letterhead"], [
    P("backgroundColor", S, None, "Cor de fundo do cabeçalho ou do rodapé. " + HEX, "S"),
    P("height", "DashboardComponent[]", None, "Altura do cabeçalho ou do rodapé.", "S", natureza="desconhecida",
      contexto="A tabela da página tipa o campo como DashboardComponent[], o que parece um erro da própria página; o tipo real não foi confirmado."),
    P("horizontalAlignment", "LetterheadHorizontalAlignment", None, "Alinhamento horizontal.", vals=valores("None", "Left", "Center", "Right")),
    P("logo", S, None, "Referência a um documento usado como logo, no formato Pasta/Documento."),
    P("verticalAlignment", "LetterheadVerticalAlignment", None, "Alinhamento vertical.", vals=valores("None", "Top", "Middle", "Bottom")),
], "O estilo do cabeçalho ou do rodapé de um letterhead.")
estrutura("LetterheadLine", S_LH, ["mdt:Letterhead"], [
    P("color", S, None, "Cor da linha. " + HEX, "S"),
    P("height", I, None, "Altura da linha.", "S"),
], "O estilo de uma linha divisória de um letterhead: cor e altura.")
tipo("Letterhead", S_LH,
     "Um letterhead (do Salesforce Classic): as opções de formatação de email templates, como logo, cor da página e linhas.",
     "Versionar e implantar o papel timbrado usado pelos email templates HTML.", "12.0", [
         P("available", B, None, "Indica se o letterhead pode ser usado, por exemplo em email templates.", "S"),
         P("backgroundColor", S, None, "Cor de fundo. " + HEX, "S"),
         P("bodyColor", S, None, "Cor do corpo. " + HEX, "S"),
         P("bottomLine", "LetterheadLine", None, "Estilo da linha inferior.", "S", estrutura="LetterheadLine"),
         P("description", S, None, "Texto que diferencia este letterhead dos demais.", "S"),
         P("fullName", S, None, "Nome interno, derivado de name. Herdado do tipo Metadata.", "S", herdada="Metadata"),
         P("footer", "LetterheadHeaderFooter", None, "Estilo do rodapé.", "S", estrutura="LetterheadHeaderFooter"),
         P("header", "LetterheadHeaderFooter", None, "Estilo do cabeçalho.", "S", estrutura="LetterheadHeaderFooter"),
         P("middleLine", "LetterheadLine", None, "Estilo da linha do meio.", "S", estrutura="LetterheadLine"),
         P("name", S, None, "Nome do letterhead.", "S"),
         P("topLine", "LetterheadLine", None, "Estilo da linha horizontal logo abaixo do cabeçalho.", "S", estrutura="LetterheadLine"),
     ], exemplo=CAB + f"""<Letterhead {NS}>
    <available>true</available>
    <backgroundColor>[cor em hexadecimal]</backgroundColor>
    <bodyColor>[cor em hexadecimal]</bodyColor>
    <bottomLine>
        <color>[cor em hexadecimal]</color>
        <height>[altura]</height>
    </bottomLine>
    <description>[descrição do letterhead]</description>
    <footer>
        <backgroundColor>[cor em hexadecimal]</backgroundColor>
        <height>[altura]</height>
    </footer>
    <header>
        <backgroundColor>[cor em hexadecimal]</backgroundColor>
        <height>[altura]</height>
    </header>
    <middleLine>
        <color>[cor em hexadecimal]</color>
        <height>[altura]</height>
    </middleLine>
    <name>[nome do letterhead]</name>
    <topLine>
        <color>[cor em hexadecimal]</color>
        <height>[altura]</height>
    </topLine>
</Letterhead>""", curinga=False,
     alertas=["O curinga (*) não funciona no package.xml para este tipo.",
              "A introdução da página diz que todos os campos são obrigatórios, menos logo e os dois alinhamentos.",
              "Este tipo é o letterhead do Salesforce Classic; a Ajuda trata os enhanced letterheads do Lightning Experience em separado."],
     divergencias=["A tabela tipa height (cabeçalho e rodapé) como DashboardComponent[], e bottomLine como enumeração de string com os valores "
                   "color e height; os dois casos parecem erros da página. bottomLine foi cadastrado como LetterheadLine, igual às outras linhas."],
     cobertura_nota=NOTA_COB)

# ================================================================ Document
tipo("Document", S_DOC,
     "Um documento da aba Documents (do Salesforce Classic): um arquivo guardado numa pasta de documentos, com seu metadado.",
     "Versionar e implantar documentos da org, como imagens usadas em email templates.", "10.0", [
         binario("O conteúdo do documento. Herdado de MetadataWithContent."),
         P("description", S, None, "Texto que diferencia o documento dos demais."),
         P("fullName", S, None, "Nome com a pasta. Desde a API 18.0, sem a extensão do arquivo. Só letras, números e sublinhados. Herdado.", "?",
           herdada="Metadata"),
         P("internalUseOnly", B, None, "Marca o documento como confidencial. Não pode ser usado junto com public.", "S"),
         P("keywords", S, None, "Palavras que descrevem o documento, usadas na busca."),
         P("name", S, None, "Nome anterior à API 14.0; só é preenchido se o fullName antigo tinha caracteres hoje não aceitos."),
         P("public", B, None, "Indica uma imagem de email template HTML que pode ser vista sem login. Não pode ser usado junto com internalUseOnly.", "S"),
     ], exemplo=CAB + f"""<!-- Arquivo <nome do arquivo com extensão>-meta.xml, ao lado do próprio documento -->
<Document {NS}>
    <description>[descrição do documento]</description>
    <internalUseOnly>false</internalUseOnly>
    <public>true</public>
</Document>""", estende="MetadataWithContent", curinga=False,
     arquivos_prontos=em_pasta("documents/<pasta>/", "<arquivo do documento> e <arquivo do documento>-meta.xml",
                               "Os documentos ficam em subpastas da pasta documents; o arquivo de metadado leva o nome do arquivo, com a extensão, "
                               "seguido de -meta.xml.", "document", S_DOC),
     alertas=["O curinga (*) não funciona: liste cada documento com a pasta, como MinhaPasta/MeuDocumento. A página indica listMetadata() com "
              "DocumentFolder para obter a lista.",
              "Deixe public como false quando a imagem é logo de app customizado ou ícone de aba: esses usos exigem login para ver a imagem.",
              "Desde a API 17.0, excluir uma pasta exclui de vez os documentos dela que estão na Lixeira."],
     cobertura_nota=NOTA_COB)

# ================================================================ ContentAsset
estrutura("ContentAssetLink", S_CA, ["mdx:ContentAssetRelationships"], [
    P("access", "ContentAssetAccess", None, "Permissão dada sobre o arquivo compartilhado.", "S", vals=[
        ("VIEWER", None), ("COLLABORATOR", None), ("INFERRED", "A permissão vem da que o usuário já tem.")]),
    P("isManagingWorkspace", B, "39.0", "Indica se o asset reside no workspace.", default=FALSE),
    P("name", S, None, "Reservado para uso futuro."),
], "Um vínculo de compartilhamento de um asset file.")
_REL = "A tabela da página tipa o campo como ContentAsset[]; o exemplo XML usa dentro dele o elemento access, da seção ContentAssetLink."
estrutura("ContentAssetRelationships", S_CA, ["mdt:ContentAsset"], [
    P("emailTemplate", "ContentAssetLink[]", "51.0", "Email templates relacionados ao asset.", estrutura="ContentAssetLink", notas=[_REL]),
    P("insightsApplication", "ContentAssetLink[]", "39.0", "Apps do Insights que usam o asset.", estrutura="ContentAssetLink", notas=[_REL]),
    P("network", "ContentAssetLink[]", "39.0", "Networks (sites) que usam o asset.", estrutura="ContentAssetLink", notas=[_REL]),
    P("organization", "ContentAssetLink[]", "39.0", "Compartilhamento com a org; corresponde a ContentDocumentLink.", estrutura="ContentAssetLink",
      notas=[_REL]),
    P("workspace", "ContentAssetLink[]", "39.0", "Workspaces e bibliotecas donos do asset ou com quem ele é compartilhado.",
      estrutura="ContentAssetLink", notas=[_REL]),
], "Com quem um asset file é compartilhado.")
estrutura("ContentAssetVersion", S_CA, ["mdx:ContentAssetVersions"], [
    P("number", S, None, "Número da versão; reflete ou define o do ContentVersion.", "S"),
    P("pathOnClient", S, None, "Nome original do arquivo; corresponde a ContentVersion.PathOnClient e dá origem ao título.", "S"),
    P("zipEntry", S, None, "Nome do arquivo dentro do zip quando há várias versões; vazio quando há uma só."),
], "Uma versão do arquivo de um asset file.")
estrutura("ContentAssetVersions", S_CA, ["mdt:ContentAsset"], [
    P("version", "ContentAssetVersion[]", None, "Versões do arquivo.", estrutura="ContentAssetVersion"),
], "A lista de versões do arquivo de um asset file.")
tipo("ContentAsset", S_CA,
     "Um asset file: um arquivo do Salesforce Files preparado para uso em configuração, como logos e imagens de marca.",
     "Versionar e implantar os arquivos de marca e design que apps, temas e sites referenciam.", "38.0", [
         binario("O conteúdo do arquivo. Herdado de MetadataWithContent."),
         P("format", "ContentAssetFormat", None, "Formato do arquivo do asset.", vals=[
             ("Original", "Uma única versão."), ("ZippedVersions", "Várias versões, compactadas.")],
           notas=["Com uma só versão, o campo pode ser omitido."]),
         P("fullName", S, None, "Nome de API do asset. Herdado do tipo Metadata.", "?", herdada="Metadata"),
         P("isVisibleByExternalUsers", B, "44.0", "Indica se usuários não autenticados podem ver o arquivo.", default=FALSE),
         P("language", S, None, "Idioma do rótulo do asset.", "S"),
         P("masterLabel", S, None, "Rótulo do asset, mostrado no Setup.", "S"),
         P("originNetwork", S, None, "Site do Experience Cloud atribuído ao implantar ou recuperar; nulo se não houver."),
         P("relationships", "ContentAssetRelationships", None, "Com quem o arquivo é compartilhado.", estrutura="ContentAssetRelationships"),
         P("versions", "ContentAssetVersions", None, "Dados básicos das versões do arquivo; normalmente uma.", "S", estrutura="ContentAssetVersions"),
     ], exemplo=CAB + f"""<!-- Arquivo -meta.xml que acompanha o arquivo .asset -->
<ContentAsset {NS}>
    <language>[idioma do rótulo]</language>
    <masterLabel>[rótulo do asset]</masterLabel>
    <relationships>
        <organization>
            <!-- Valores documentados: VIEWER, COLLABORATOR, INFERRED -->
            <access>VIEWER</access>
        </organization>
    </relationships>
    <versions>
        <version>
            <number>1</number>
            <pathOnClient>[nome original do arquivo]</pathOnClient>
        </version>
    </versions>
</ContentAsset>""", estende="MetadataWithContent", curinga=True,
     alertas=["A recuperação falha se o conteúdo total dos asset files passar de 30 MB.",
              "Valem os limites de empacotamento já existentes para arquivos."],
     divergencias=["Os campos de ContentAssetRelationships aparecem tipados como ContentAsset[], mas o conteúdo documentado deles é o da seção "
                   "ContentAssetLink; foram cadastrados como ContentAssetLink[]."],
     cobertura_nota=NOTA_COB)

# ================================================================ ChatterSettings
tipo("ChatterSettings", S_CH,
     "Configurações do Chatter na org: ligar o recurso, grupos, edição e fixação de posts, rascunhos e prévias de links.",
     "Recuperar e implantar as opções do Chatter em vez de marcá-las à mão em cada ambiente.", "47.0", [
         P("allowChatterGroupArchiving", B, None, "Permite ou bloqueia o arquivamento, manual e automático, de todos os grupos do Chatter."),
         P("allowRecordsInChatterGroup", B, None, "Permite ligar registros a grupos. Desligar mantém os dados de registros já ligados."),
         P("allowSharingInChatterGroup", B, "47.0", "Removido; não tem efeito na org.", ate="47.0",
           notas=["A página diz que o campo só existe na API 47.0."]),
         P("enableApprovalRequest", B, None, "Publica pedidos de aprovação nos feeds do Chatter; cada usuário pode optar por não receber.",
           default=FALSE),
         P("enableCaseFeedRelativeTimestamps", B, "48.0", "Escolhe entre horário relativo e absoluto nos itens do feed de caso.",
           default=("valor", True, "A página declara default true."),
           notas=["A descrição da página usa true para as duas opções; qual valor corresponde a qual formato não ficou confirmado."]),
         P("enableChatter", B, None, "Liga ou desliga o Chatter na org."),
         P("enableChatterEmoticons", B, None, "Converte sequências de caracteres, como carinhas, em emoticons gráficos."),
         P("enableFeedEdit", B, None, "Permite editar posts e comentários do feed a quem tem esse direito: autor, dono do registro ou moderador."),
         P("enableFeedPinning", B, None, "Permite a usuários autorizados fixar até três posts no topo de um feed."),
         P("enableFeedsDraftPosts", B, None, "Salva rascunhos automaticamente a cada sete segundos e cria o feed My Drafts."),
         P("enableFeedsRichText", B, None, "Liga o editor de rich text no publisher do Chatter."),
         P("enableInviteCsnUsers", B, None, "Permite a usuários com licença convidar clientes de fora para grupos privados que gerenciam."),
         P("enableOutOfOfficeEnabledPref", B, None, "Põe no perfil do usuário o controle de mensagem de ausência."),
         P("enableRichLinkPreviewsInFeed", B, None, "Transforma links dos posts em prévias de vídeo, imagem e artigo."),
         P("enableTodayRecsInFeed", B, None, "Publica nos feeds as recomendações do app Salesforce Today."),
         P("unlistedGroupsEnabled", B, None, "Permite grupos unlisted: fora da lista de grupos e só por convite."),
         M.FULLNAME_HERDADO(None),
     ], exemplo=CAB + f"""<ChatterSettings {NS}>
    <enableChatter>true</enableChatter>
    <enableFeedEdit>true</enableFeedEdit>
    <unlistedGroupsEnabled>false</unlistedGroupsEnabled>
</ChatterSettings>""", arquivos_prontos=M.arquivos_settings("ChatterSettings", "Chatter", S_CH), curinga=False,
     alertas=["O curinga do package.xml não vale para um settings isolado: só para recuperar todos os settings de uma vez."],
     divergencias=["Na linha de enableChatterEmoticons, o mapeamento para o Setup cita enableChatter, embora o rótulo informado seja Allow Emoticons."],
     cobertura_nota=NOTA_COB + " A página não informa obrigatoriedade de nenhum campo.")

# ================================================================ GenAiPromptTemplate
URI = "No formato de URI, como {}."
estrutura("GenAiPromptTemplateGenerationConfig", S_PT, ["mdx:GenAiPromptTemplateVersion"], [
    P("generationConfigDeveloperName", S, None, "Developer name da política aplicada à versão."),
], "Referência a uma política de geração de uma versão de prompt template.")
estrutura("GenAiPromptTemplateInput", S_PT, ["mdx:GenAiPromptTemplateVersion"], [
    P("apiName", S, None, "Nome do parâmetro de entrada.", "S"),
    P("definition", S, None, "Definição da entrada. " + URI.format("SOBJECT://Account"), "S"),
    P("description", S, None, "Descrição do parâmetro de entrada."),
    P("masterLabel", S, None, "Nome amigável da entrada."),
    P("referenceName", S, None, "Nome usado nas expressões do template, como Input:Recipient.", "S"),
    P("required", B, None, "Indica se a entrada é obrigatória.", "S"),
], "Uma entrada (input) de uma versão de prompt template.")
estrutura("GenAiPromptTemplateDataProviderParam", S_PT, ["mdx:GenAiPromptTemplateDataProvider"], [
    P("definition", S, None, "Definição do parâmetro. " + URI.format("SOBJECT://User"), "S"),
    P("isRequired", B, None, "Indica se o parâmetro é obrigatório.", "S"),
    P("parameterName", S, None, "Nome do parâmetro.", "S"),
    P("valueExpression", S, None, "Valor ou expressão usada no texto do template, como {!$Input:Recipient}."),
], "Um parâmetro passado a um provedor de dados de um prompt template.")
estrutura("GenAiPromptTemplateDataProvider", S_PT, ["mdx:GenAiPromptTemplateVersion"], [
    P("definition", S, None, "Definição do provedor. " + URI.format("flow://ns__CallToActionFlow"), "S"),
    P("description", S, None, "Descrição do provedor de dados."),
    P("label", S, None, "Nome amigável do provedor.", "S"),
    P("parameters", "GenAiPromptTemplateDataProviderParam[]", None, "Parâmetros do provedor.", estrutura="GenAiPromptTemplateDataProviderParam"),
    P("referenceName", S, None, "Nome do provedor usado nas expressões do template.", "S"),
], "Um provedor de dados de uma versão de prompt template: de onde vêm dados para o prompt, como um flow.")
estrutura("GenAiPromptTemplateVersion", S_PT, ["mdt:GenAiPromptTemplate"], [
    P("content", S, None, "O texto da versão do prompt template.", "S"),
    P("description", S, None, "Descrição da versão."),
    P("fileDroppingStrategy", S, None, "Estratégia para arquivos anexados quando o limite de contexto é excedido."),
    P("generationTemplateConfigs", "GenAiPromptTemplateGenerationConfig[]", None, "Políticas aplicadas à versão.",
      estrutura="GenAiPromptTemplateGenerationConfig"),
    P("inputs", "GenAiPromptTemplateInput[]", None, "Entradas da versão.", estrutura="GenAiPromptTemplateInput"),
    P("isCitationEnabled", B, None, "Indica se as respostas geradas trazem citações."),
    P("outputSchema", S, None, "Estrutura de JSON schema esperada para a saída."),
    P("primaryModel", S, None, "Modelo associado à versão."),
    P("responseFormat", "GenAiPromptTemplateResponseFormat", None, "Formato da resposta.", vals=valores("HTML", "JSON", "MarkDown")),
    P("status", "GenAiPromptTemplateStatus", None, "Estado da versão no Prompt Builder.", "S", vals=valores("Published", "Draft")),
    P("templateDataProviders", "GenAiPromptTemplateDataProvider[]", None, "Provedores de dados da versão.",
      estrutura="GenAiPromptTemplateDataProvider"),
    P("versionNumber", I, None, "Número sequencial da versão, a partir de 1. Descontinuado na API 63.0: use versionIdentifier.", "S"),
    P("versionIdentifier", S, None, "Identificador único da versão; é gerado automaticamente quando não informado."),
], "Uma versão de um prompt template: o texto, as entradas, os provedores de dados e o estado.")
tipo("GenAiPromptTemplate", S_PT,
     "Um prompt template: o modelo de instrução, com versões, que o Prompt Builder gerencia e que recursos de IA generativa usam.",
     "Versionar e implantar os prompt templates entre ambientes.", "60.0", [
         P("activeVersion", I, None, "Descontinuado na API 63.0 e sem funcionar da 64.0 em diante: use activeVersionIdentifier."),
         P("activeVersionIdentifier", S, None, "Identificador da versão ativa; usa o valor do versionIdentifier dela."),
         P("description", S, None, "Descrição do prompt template."),
         P("masterLabel", S, None, "Nome amigável, definido na criação.", "S"),
         P("overridable", B, None, "Indica se o template pode ser substituído quando vem num pacote gerenciado."),
         P("relatedEntity", S, None, "Tipo de registro do Salesforce a que o template está ligado."),
         P("relatedField", S, None, "Campo do Salesforce a que o template está ligado."),
         P("templateVersions", "GenAiPromptTemplateVersion[]", None, "As versões do template.", "S", estrutura="GenAiPromptTemplateVersion"),
         P("type", S, None, "Tipo-base do template.", "S", vals=valores(
             "einstein_gpt__fieldCompletion", "einstein_gpt__salesEmail", "einstein_gpt__recordSummary", "einstein_gpt__flex",
             "einstein_gpt__caseEmailDraft"), contexto="A página lista estes valores para um campo do tipo string."),
         P("visibility", "GenAiPromptTemplateVisibilityType", None, "Escopo de visibilidade do template.", vals=valores("API", "Global")),
         M.FULLNAME_HERDADO(None),
     ], exemplo=CAB + f"""<GenAiPromptTemplate {NS}>
    <activeVersionIdentifier>[identificador da versão ativa]</activeVersionIdentifier>
    <description>[para que serve o prompt template]</description>
    <masterLabel>[nome do prompt template]</masterLabel>
    <templateVersions>
        <content>[texto do prompt, com as expressões de entrada]</content>
        <inputs>
            <apiName>[nome da entrada]</apiName>
            <definition>SOBJECT://Account</definition>
            <referenceName>[nome usado nas expressões]</referenceName>
            <required>true</required>
        </inputs>
        <!-- Valores documentados: Published, Draft -->
        <status>Draft</status>
        <versionIdentifier>[identificador da versão]</versionIdentifier>
    </templateVersions>
    <!-- Valores documentados: einstein_gpt__fieldCompletion, einstein_gpt__salesEmail, einstein_gpt__recordSummary, einstein_gpt__flex, einstein_gpt__caseEmailDraft -->
    <type>einstein_gpt__flex</type>
    <!-- Valores documentados: API, Global -->
    <visibility>Global</visibility>
</GenAiPromptTemplate>""", curinga=True,
     alertas=["Templates publicados não podem ser editados, nem pela interface nem pela Metadata API.",
              "activeVersion e versionNumber foram descontinuados na API 63.0 e deixam de funcionar na 64.0: use os campos de identificador.",
              "A página informa acesso especial: exige o Prompt Builder ligado na org e a permissão Prompt Template Manager."],
     cobertura_nota=NOTA_COB)

# ================================================================ GenAiFunction e GenAiPlugin
estrutura("GenAiPlannerAttr", S_FN, ["mdt:GenAiFunction"], [
    P("description", S, None, "Descrição do atributo."),
    P("label", S, None, "Rótulo do atributo.", "S"),
    P("name", S, None, "Nome do atributo.", "S"),
    P("parameterName", S, None, "Nome do parâmetro.", "S"),
    P("parameterType", "PlannerAttrMappingType", None, "Direção do parâmetro.", "S", vals=valores("input", "output")),
], "Um atributo do planner mapeado a um parâmetro de entrada ou de saída de uma agent action.")
tipo("GenAiFunction", S_FN,
     "Uma agent action: a ação que pode ser adicionada a um agente de IA, com o alvo que ela invoca (um flow, uma classe Apex, um prompt template e outros).",
     "Versionar e implantar as agent actions da biblioteca de assets.", "60.0", [
         P("description", S, None, "Explica o propósito geral e o domínio da ação."),
         P("invocationTarget", S, None, "O alvo invocado pela ação.", "S"),
         P("invocationTargetType", "PlannerFunctionInvocableTargetType", None, "Tipo da ação invocável.", "S", vals=valores(
             "api", "apex", "auraEnabled", "createCatalogItemRequest", "executeIntegrationProcedure", "externalService", "flow",
             "generatePromptResponse", "mcpTool", "namedQuery", "quickAction", "retriever", "runExpressionSet", "slack",
             "standardInvocableAction", "stub")),
         P("isConfirmationRequired", B, None, "Indica se a ação pede confirmação."),
         P("isIncludeInProgressIndicator", B, None, "Indica se um indicador de progresso é mostrado."),
         P("mappingAttributes", "GenAiPlannerAttr[]", None, "Atributos do planner mapeados a parâmetros.", estrutura="GenAiPlannerAttr"),
         P("masterLabel", S, None, "Rótulo da ação.", "S"),
         P("pluginField", S, None, "O tópico pai da ação."),
         P("progressIndicatorMessage", S, None, "Texto da mensagem de progresso."),
         M.FULLNAME_HERDADO(None),
     ], exemplo=CAB + f"""<GenAiFunction {NS}>
    <description>[o que a ação faz, em linguagem natural]</description>
    <invocationTarget>[nome do flow, da classe ou de outro alvo]</invocationTarget>
    <!-- Valores documentados incluem: flow, apex, generatePromptResponse, standardInvocableAction -->
    <invocationTargetType>flow</invocationTargetType>
    <isConfirmationRequired>false</isConfirmationRequired>
    <masterLabel>[rótulo da ação]</masterLabel>
</GenAiFunction>""", curinga=True,
     arquivos_prontos={
         "source_format": af("desconhecido", {"pasta": "genAiFunctions/<nome da ação>/"},
                             "O registro do Salesforce CLI trata o tipo como bundle (uma pasta por ação); o nome do arquivo dentro da pasta não foi confirmado.",
                             [ev("src:sdr-registry", "types.genaifunction")]),
         "metadata_api_format": af("verificado", {"pasta": "genAiFunctions/", "arquivo": "<Nome>.genAiFunction"},
                                   "Sufixo e pasta informados na página do tipo; a ação pode trazer pastas input e output, cada uma com um schema.json.",
                                   [ev(S_FN)])},
     alertas=["Além do XML, a ação pode ter pastas input e output com um schema.json cada: neles ficam título, descrição e tipo de cada parâmetro. "
              "Esses campos de JSON não são propriedades do XML e não foram cadastrados aqui.",
              "Em orgs Winter '26 ou posteriores, a página manda usar GenAiPlannerBundle para recuperar ações criadas dentro de um agente; "
              "GenAiFunction fica para as ações da biblioteca de assets.",
              "A página informa acesso especial: o tipo só fica disponível com Agents ligado na org."],
     cobertura_nota=NOTA_COB + " As tabelas de schema.json (pastas input e output) descrevem arquivos JSON e ficaram fora do universo de propriedades XML.")

estrutura("GenAiPluginFunctionDef", S_PL, ["mdt:GenAiPlugin"], [
    P("functionName", S, None, "Nome de API da função (a agent action).", "S"),
], "Referência a uma agent action dentro de um tópico.")
tipo("GenAiPlugin", S_PL,
     "Um tópico de agente: uma categoria de ações ligada a um trabalho que o agente de IA faz, com escopo e instruções.",
     "Versionar e implantar os tópicos da biblioteca de assets.", "62.0", [
         P("aiPluginUtterances", "AiPluginUtteranceDef[]", None, "Frases de exemplo usadas para escolher o tópico em tempo de execução."),
         P("canEscalate", B, None, "Indica se o tópico pode ser escalado para um atendente."),
         P("description", S, None, "Descrição do tópico."),
         P("developerName", S, None, "Nome único de API do tópico: letras, números e sublinhados, sem dois sublinhados seguidos.", "S"),
         P("genAiFunctions", "GenAiPluginFunctionDef[]", None, "As funções (agent actions) do tópico.", estrutura="GenAiPluginFunctionDef"),
         P("genAiPluginInstructions", "GenAiPluginInstructionDef[]", None, "As instruções do tópico."),
         P("language", S, None, "Idioma do tópico.", "S"),
         P("masterLabel", S, None, "Rótulo do tópico.", "S"),
         P("plannerField", S, None, "O planner pai do tópico."),
         P("pluginType", "PluginType", None, "Tipo do plugin.", "S", vals=valores("Topic", "APICustomTopic")),
         P("scope", S, None, "Descrição específica do trabalho coberto pelo tópico."),
         M.FULLNAME_HERDADO(None),
     ], exemplo=CAB + f"""<GenAiPlugin {NS}>
    <description>[descrição do tópico]</description>
    <developerName>[Nome_Do_Topico]</developerName>
    <genAiFunctions>
        <functionName>[nome de API de uma agent action]</functionName>
    </genAiFunctions>
    <language>[idioma]</language>
    <masterLabel>[rótulo do tópico]</masterLabel>
    <!-- Valores documentados: Topic, APICustomTopic -->
    <pluginType>Topic</pluginType>
    <scope>[o que o tópico cobre]</scope>
</GenAiPlugin>""", curinga=True,
     alertas=["Em orgs Winter '26 ou posteriores, a página manda usar GenAiPlannerBundle para recuperar tópicos criados dentro de um agente; "
              "GenAiPlugin fica para os tópicos da biblioteca de assets.",
              "Para implantar numa org Summer '25 (API 64.0), recupere com a API 64.0; para Winter '26 em diante, use a 65.0 ou posterior.",
              "A Ajuda atual chama o tópico de subagent; a página do tipo na API 68.0 ainda usa topic.",
              "A página informa acesso especial: o tipo só fica disponível com Agents ligado na org."],
     cobertura_nota=NOTA_COB + " Os subtipos AiPluginUtteranceDef e GenAiPluginInstructionDef são citados, mas a página não traz os campos deles.")

# ================================================================ EinsteinGptSettings
DESLIGA = "Desliga o provedor {} e bloqueia o acesso aos modelos dele."
tipo("EinsteinGptSettings", S_GPT,
     "Configurações de IA generativa da org: ligar os recursos, desligar provedores de modelo e controlar a implantação de prompt templates.",
     "Recuperar e implantar as opções de IA generativa em vez de marcá-las à mão em cada ambiente.", "61.0", [
         P("disableAIProvAWSBedrock", B, None, DESLIGA.format("AWS Bedrock"), default=FALSE),
         P("disableAIProvAzureOpenAI", B, None, DESLIGA.format("Azure OpenAI"), default=FALSE),
         P("disableAIProvOpenAI", B, None, DESLIGA.format("OpenAI"), default=FALSE),
         P("disableAIProvVertexGemini", B, None, DESLIGA.format("Vertex AI (Google)"), default=FALSE),
         P("disableAIProviderRegionFallback", B, None, "Desliga o uso, pelo Azure OpenAI, de endpoints fora da região da org como alternativa.",
           default=FALSE),
         P("enableAIModelBeta", B, None, "Liga modelos em beta para os recursos de IA generativa.", default=FALSE),
         P("enableEinsteinGptAllowUnsafePTInputChanges", B, None, "Reservado para uso interno."),
         P("enableEinsteinGPTDeployPromptTemplatesAsActive", B, None, "Implanta só as versões ativas dos prompt templates e ignora as inativas. "
           "A implantação falha se não houver versão ativa.", default=FALSE),
         P("enableEinsteinGptGlobalLangSupport", B, None, "Liga o uso de idiomas globais com prompt templates.", default=FALSE),
         P("enableEinsteinGptPlatform", B, None, "Liga os recursos de IA generativa no Salesforce.", default=FALSE),
         M.FULLNAME_HERDADO(None),
     ], exemplo=CAB + f"""<EinsteinGptSettings {NS}>
    <enableEinsteinGptGlobalLangSupport>false</enableEinsteinGptGlobalLangSupport>
    <enableEinsteinGptPlatform>true</enableEinsteinGptPlatform>
</EinsteinGptSettings>""", arquivos_prontos=M.arquivos_settings("EinsteinGptSettings", "EinsteinGpt", S_GPT), curinga=None,
     divergencias=["No exemplo XML da página, as tags de fechamento não correspondem às de abertura (fecham com nomes de campos de outro tipo).",
                   "O package.xml de exemplo usa a versão 63.0, embora o tipo exista desde a 61.0."],
     cobertura_nota=NOTA_COB + " A página não informa obrigatoriedade de nenhum campo nem trata do curinga.")

M.emit_structs()
C.marcar_referencia("estruturas", "GenAiPluginFunctionDef", "functionName", "mdt:GenAiFunction")
C.marcar_referencia("metadata-types", "EmailTemplate", "letterhead", "mdt:Letterhead")

# ================================================================ nota de extração: lista de campos
linhas = ["", "-- Lista de campos transcrita da leitura (gerada por lote7f_conteudo_ia.py; nome | tipo | desde | obrigatoriedade)"]
for src, pasta, nome in REGISTRADOS:
    props = ld(f"{pasta}/{nome}.json")["propriedades"]
    campos = ", ".join(f"{q['nome']} | {q['tipo_tecnico']} | {q.get('desde_versao') or '-'}" for q in props)
    linhas.append(f"[{src}] {nome}: {campos}")
_p = caminho(EXTR)
_t = open(_p, encoding="utf-8").read().split("\n-- Lista de campos transcrita")[0].rstrip("\n")
open(_p, "w", encoding="utf-8").write(_t + "\n" + "\n".join(linhas) + "\n")

# ================================================================ relacionamentos
C.rel_referencia("emailtemplate-letterhead", "mdt:EmailTemplate", "letterhead", "mdt:Letterhead",
                 "Um email template do tipo html aponta o letterhead que define logo, cores e linhas.", S_ET)
C.rel_referencia("genaiplugin-genaifunction", "mdx:GenAiPluginFunctionDef", "functionName", "mdt:GenAiFunction",
                 "Um tópico lista, pelo nome de API, as agent actions que o compõem.", S_PL)

# ================================================================ funcionalidades
CON, IA = "conteudo-conhecimento-e-colaboracao", "ia-agentes-e-decisoes-assistidas"


def setup(valor, src, nota=""):
    return af("verificado", valor, (nota + " " + C.UI_EN).strip(), [ev(src)])


def sem(tipo_, motivo, estado="desconhecido"):
    return {"tipo": tipo_, "estado": estado, "motivo": motivo}


SEM_OBJ = sem("objeto_api", "Objetos API do tema não investigados nas rodadas A5 e A6; a lista vazia não comprova inexistência.")

C.funcionalidade(
    "email-templates", "Email templates", "Email Templates", ["email template", "modelo de e-mail", "letterhead", "enhanced letterhead", "merge fields",
                                                              "hml", "classic email templates"],
    "Um email template é um modelo de e-mail reutilizável, com campos de mesclagem (merge fields) que são trocados pelos dados do registro. Há "
    "templates do Salesforce Classic (texto, HTML com letterhead, HTML customizado e Visualforce) e templates do Lightning Experience.",
    "Padronizar os e-mails enviados e poupar o tempo de escrevê-los de novo.",
    "A equipe de vendas usa um template de boas-vindas: ao enviar, o nome do contato e o da conta entram sozinhos no texto.",
    (CON, "templates-e-comunicacao"), [],
    [("EmailTemplate", "Cada email template, com o corpo e o metadado."), ("Letterhead", "O letterhead do Classic usado por templates HTML."),
     ("Document", "Documentos do Classic usados como imagem ou logo em templates e letterheads.")], [],
    [S_ET, S_LH, S_DOC, "src:help-email-templates-lex", "src:help-email-template-create", "src:help-email-merge-fields", "src:help-classic-letterheads",
     "src:help-classic-templates-in-lex", "src:help-enhanced-letterheads", "src:help-classic-html-templates"], [SEM_OBJ],
    setup("Setup > Quick Find: Classic Email Templates", "src:help-classic-html-templates",
          "Vale para os templates do Classic, por quem pode editar templates públicos. Os do Lightning Experience são criados a partir do próprio e-mail."),
    limitacoes=["Templates criados no Lightning Experience não podem ser usados no Salesforce Classic.",
                "Templates HTML com Classic letterhead podem ser usados no Lightning Experience, mas não criados nele."],
    alertas=["Há duas linguagens de merge fields: os templates do Lightning Experience criados desde o Summer '18 usam HML, com três chaves; os "
             "do Classic usam SML.",
             "Classic letterheads e enhanced letterheads são recursos diferentes; um template do Lightning precisa usar HML para ter um enhanced letterhead.",
             "Templates do Lightning Experience nascem privados; para outros usarem, vão para uma pasta pública."])

C.funcionalidade(
    "salesforce-files", "Salesforce Files", "Salesforce Files", ["files", "arquivos", "contentdocument", "contentversion", "contentdocumentlink", "anexos"],
    "Salesforce Files é o recurso de arquivos da plataforma: enviar, versionar e compartilhar arquivos com pessoas, grupos, registros e "
    "bibliotecas. Não existe um objeto chamado File: o modelo usa ContentDocument (o arquivo), ContentVersion (cada versão) e "
    "ContentDocumentLink (com quem o arquivo é compartilhado).",
    "Guardar documentos junto do trabalho e controlar quem os vê.",
    "A proposta em PDF é anexada à oportunidade; ao subir uma versão corrigida, a anterior continua guardada.",
    (CON, "files-e-documentos"), [], [], [],
    ["src:help-kb-files-data-model", "src:objref-contentdocument-nota", "src:objref-contentversion-nota", "src:help-chatter-files-groups"],
    [sem("metadata_type", "Metadata types de configuração de Files não investigados."),
     sem("objeto_api", "A Ajuda cita ContentDocument, ContentVersion e ContentDocumentLink; as páginas dos objetos não foram lidas por inteiro e eles não "
         "foram cadastrados.")],
    af("desconhecido", None, "Caminho de Setup não lido; o uso do recurso é pela aba Files e pelos registros.", []),
    limitacoes=["Até 30.000.000 de documentos publicados; arquivos arquivados contam nesse limite.",
                "Até 200.000 novas versões a cada 24 horas (2.500 em Developer Edition e em trials)."],
    alertas=["Consultas a ContentDocument e ContentVersion sem informar um ID não devolvem todos os arquivos a que o usuário tem acesso: os que "
             "ele só vê por ter acesso a um registro ficam de fora.",
             "Um arquivo privado compartilhado com um grupo privado ou unlisted passa a ser visto pelos membros do grupo."])

C.funcionalidade(
    "asset-files", "Asset files", "Asset Files", ["asset file", "content asset", "asset library", "contentasset", "logo"],
    "Um asset file é a versão empacotável de um arquivo do Salesforce Files, usada em marca e design: logos, imagens de cabeçalho e arquivos "
    "referenciados por componentes. Fica na Asset Library, em Files.",
    "Ter imagens e arquivos de configuração que possam ser referenciados, versionados e implantados.",
    "O logo da empresa vira um asset file e é usado no tema da org e no site do Experience Cloud.",
    (CON, "bibliotecas-e-assets"), [],
    [("ContentAsset", "Cada asset file, com o arquivo, as versões e o compartilhamento.")], [],
    [S_CA, "src:help-asset-files", "src:help-kb-files-public"], [SEM_OBJ],
    af("desconhecido", None, "A Ajuda indica a Asset Library, em Files home; não é uma página de Setup.", []),
    alertas=["Não é preciso criar asset files para o uso comum e colaborativo de arquivos: só para usos de configuração.",
             "Asset files são uma alternativa a static resources para deixar arquivos públicos.",
             "A recuperação por Metadata API falha se o conteúdo total dos asset files passar de 30 MB."])
C.secundaria("static-resources", CON, "bibliotecas-e-assets", "Static resources são os arquivos estáticos que o código da org usa.", srcs=["src:help-kb-files-public"])

C.funcionalidade(
    "chatter", "Chatter", "Chatter", ["feed", "chatter group", "grupo do chatter", "unlisted group", "broadcast group", "post"],
    "Chatter é o recurso de colaboração: feeds em perfis, registros e grupos, com posts, comentários e arquivos. Os grupos podem ser públicos, "
    "privados ou unlisted, e ainda arquivados.",
    "Conversar e compartilhar informação no contexto do trabalho, no próprio registro ou num grupo do time.",
    "O time de um projeto cria um grupo privado; só os membros veem os posts e os arquivos.",
    (CON, "colaboracao"), [],
    [("ChatterSettings", "As opções do Chatter na org.")], [],
    [S_CH, "src:help-chatter-groups", "src:help-chatter-unlisted", "src:help-chatter-unlisted-enable", "src:help-chatter-broadcast",
     "src:help-chatter-files-groups"],
    [sem("objeto_api", "Objetos de feed e de grupos do Chatter não investigados.")],
    setup("Setup > Quick Find: Chatter > Chatter Settings", "src:help-chatter-unlisted-enable", "Página das opções do Chatter, como os grupos unlisted."),
    limitacoes=["Cada usuário pode participar de até 300 grupos; a org pode ter até 30.000 grupos."],
    alertas=["Grupo privado não é invisível: quem não é membro ainda vê nome, foto, descrição e membros. Para esconder o grupo, use unlisted.",
             "Grupos unlisted vêm desligados por padrão.",
             "Num broadcast group, só donos e gerentes do grupo publicam; os membros leem e comentam.",
             "O tipo de metadado Group é outra coisa: representa public groups, usados em compartilhamento, não grupos do Chatter."])

C.funcionalidade(
    "prompt-builder", "Prompt Builder", "Prompt Builder", ["prompt template", "modelo de prompt", "grounding", "flex template", "field generation",
                                                         "einstein generative ai"],
    "Prompt Builder é a ferramenta para criar, testar e gerenciar prompt templates: prompts reutilizáveis, com espaços reservados que são "
    "preenchidos com dados da org (campos de registro, flows, Apex, arquivos) antes de irem ao modelo. Esse preenchimento se chama grounding.",
    "Levar IA generativa ao trabalho do usuário com instruções padronizadas e dados atuais.",
    "Um template Field Generation preenche o campo Resumo do caso: o usuário clica num botão e o texto gerado entra no campo.",
    (IA, "prompts"), [(IA, "modelos-e-grounding", "O grounding liga o prompt aos dados; cada versão do template aponta o modelo usado.")],
    [("GenAiPromptTemplate", "Cada prompt template, com versões, entradas e provedores de dados."),
     ("EinsteinGptSettings", "Liga a IA generativa na org, desliga provedores de modelo e controla a implantação de templates.")], [],
    [S_PT, S_GPT, "src:help-prompt-builder", "src:help-prompt-concepts", "src:help-prompt-template-types", "src:help-prompt-flex",
     "src:help-prompt-field-gen", "src:help-prompt-rag"], [SEM_OBJ],
    setup("Setup > Quick Find: Prompt Builder", "src:help-prompt-flex", "O botão New Prompt Template pede o tipo do template."),
    alertas=["Para pôr um template Field Generation numa página de registro, a página precisa usar Dynamic Forms.",
             "Templates publicados não podem ser editados, nem pela interface nem pela Metadata API.",
             "Criar e gerenciar templates exige permissão própria; a Ajuda cita o permission set Prompt Template Manager."])

C.funcionalidade(
    "agentes-agentforce", "Agentes do Agentforce", "Agentforce Agents", ["agentforce", "agent", "agente", "agentforce builder", "agentforce studio",
                                                                        "agent script", "agent user"],
    "Um agente do Agentforce é um assistente de IA que responde perguntas e executa tarefas, para clientes ou para funcionários. Ele é montado "
    "com subagents (antes chamados topics), que agrupam instruções e ações.",
    "Automatizar atendimentos e tarefas que dependem de conversa, usando os dados e as automações da org.",
    "Um agente de atendimento consulta o pedido do cliente e abre a devolução, seguindo as instruções do subagent de devoluções.",
    (IA, "configuracao-de-agentes"), [], [], [],
    ["src:help-agentforce-glossary", "src:help-agentforce-builder-legacy", "src:help-agent-script", "src:help-agent-service-template"],
    [sem("metadata_type", "As páginas de GenAiFunction e GenAiPlugin citam GenAiPlannerBundle como o tipo que traz o conteúdo criado dentro de um agente; "
         "ele não consta do inventário de tipos da API 68.0 usado pelo projeto. Bot e BotVersion, que constam, não foram lidos."), SEM_OBJ],
    af("desconhecido", None, "A Ajuda indica o Agentforce Studio, aberto pelo App Launcher; caminho de Setup não lido.", []),
    alertas=["A Ajuda atual tem dois construtores: o Agentforce Builder, que usa Agent Script, e o Legacy Agentforce Builder.",
             "Agentes de atendimento rodam como um agent user: um usuário com exatamente as permissões de que o agente precisa.",
             "As licenças exigidas variam conforme o tipo de agente."])

C.funcionalidade(
    "subagents-e-agent-actions", "Subagents (topics) e agent actions", "Subagents and Agent Actions",
    ["topic", "tópico", "subagent", "agent action", "ação de agente", "agentforce assets", "reference action", "instructions"],
    "Um subagent (antes chamado topic) é um trabalho específico que o agente sabe fazer: reúne instruções, que orientam as decisões, e ações. "
    "Uma agent action é o que o agente executa para buscar informação ou fazer uma tarefa; ela chama um recurso da plataforma, como um flow, "
    "uma classe Apex ou um prompt template.",
    "Definir, em linguagem natural, o que o agente pode fazer e com que ferramentas.",
    "O subagent Devoluções tem a instrução de sempre confirmar o número do pedido e a ação que roda o flow de devolução.",
    (IA, "acoes-e-topicos"), [],
    [("GenAiPlugin", "Cada tópico (subagent) da biblioteca de assets."), ("GenAiFunction", "Cada agent action da biblioteca de assets.")], [],
    [S_PL, S_FN, "src:help-agentforce-glossary", "src:help-agent-action-custom", "src:help-agentforce-builder-legacy"], [SEM_OBJ],
    setup("Setup > Quick Find: Agent > Agentforce Assets", "src:help-agent-action-custom", "Lista das ações da org; New Agent Action cria uma ação."),
    alertas=["O nome mudou: a Ajuda atual diz subagent; o metadado GenAiPlugin, na API 68.0, ainda diz topic.",
             "O agente escolhe a ação pelo nome e pelas instruções dela: descreva em linguagem natural o que a ação faz.",
             "Subagents e ações criados dentro de um agente saem em outro tipo de metadado (GenAiPlannerBundle), segundo as páginas dos tipos."])

C.funcionalidade(
    "einstein-trust-layer", "Einstein Trust Layer", "Einstein Trust Layer", ["trust layer", "data masking", "zero data retention", "toxicity",
                                                                             "audit trail de ia", "mascaramento"],
    "O Einstein Trust Layer é a arquitetura de segurança da IA generativa na plataforma: um conjunto de acordos, tecnologia de segurança e "
    "controles de dados e privacidade. Inclui a política de retenção zero com os provedores de modelo, o mascaramento de dados sensíveis "
    "antes do envio ao modelo, a detecção de toxicidade e a trilha de auditoria.",
    "Usar IA generativa sem expor dados da empresa e dos clientes.",
    "O nome e o e-mail do cliente são trocados por marcadores antes de o prompt ir ao modelo externo; a resposta volta com os dados no lugar.",
    (IA, "seguranca-avaliacao-e-governanca-de-ia"), [], [], [],
    ["src:help-trust-layer", "src:help-trust-masking", "src:help-trust-audit", "src:help-agentforce-trust", "src:help-employee-agent-considerations",
     "src:help-agent-masking-limits"],
    [sem("metadata_type", "Metadata types de configuração do Trust Layer não investigados."), SEM_OBJ],
    af("desconhecido", None, "Caminho de Setup não lido.", []),
    alertas=["O mascaramento não vale igual em todo lugar: a Ajuda informa que ele fica desligado no Agentforce Employee Agent.",
             "A trilha de auditoria e os dados de feedback ficam guardados no Data 360.",
             "Agentes respeitam os controles de acesso normais do Salesforce; o Trust Layer não substitui permissões e compartilhamento."])

C.funcionalidade(
    "agentforce-data-library", "Agentforce Data Library", "Agentforce Data Library", ["data library", "retriever", "rag", "search index", "grounding",
                                                                                      "retrieval augmented generation"],
    "Uma data library indexa conteúdo (artigos de Knowledge, arquivos enviados ou fontes da web) para que agentes e prompt templates baseiem "
    "as respostas nele. A busca do trecho relevante é feita por um retriever; essa forma de grounding se chama RAG (retrieval augmented "
    "generation).",
    "Fazer a IA responder com base no conteúdo da própria empresa, e não só no que o modelo aprendeu no treinamento.",
    "O agente de atendimento responde uma dúvida sobre garantia citando o artigo de Knowledge que trata do assunto.",
    (IA, "recuperacao-de-conhecimento"), [(IA, "modelos-e-grounding", "RAG é uma forma de grounding.")], [], [],
    ["src:help-data-library", "src:help-agentforce-glossary", "src:help-prompt-rag"],
    [sem("metadata_type", "Metadata types de data libraries e retrievers não investigados."), SEM_OBJ],
    af("desconhecido", None, "Caminho de Setup não lido.", []),
    alertas=["Exige o Data 360 configurado.",
             "Em prompt templates, os retrievers buscam no conhecimento indexado no Data 360."])
C.secundaria("lightning-knowledge", IA, "recuperacao-de-conhecimento", "Artigos de Knowledge são uma das fontes que uma data library indexa.",
             srcs=["src:help-data-library"])

print(f"lote 7f: 9 metadata types e {sum(1 for r in REGISTRADOS if r[1] == 'estruturas')} estruturas gravados; 9 funcionalidades novas e 2 ligadas")
