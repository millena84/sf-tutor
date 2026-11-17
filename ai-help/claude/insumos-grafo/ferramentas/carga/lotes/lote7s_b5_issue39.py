"""Lote 7s (rodada B5, issue #39): itens antes bloqueados por fonte que agora têm fonte.

- REST API: limite de subrequisições do Composite e comportamento de allOrNone.
- Metadata API: limites de arquivos e de tamanho do .zip em deploy e retrieve.
- OAuth: caminho de Setup da página Token Exchange Handlers.
- Private Connect: caminho da conexão de entrada.

Continuam bloqueados (registrado em fontes/extracoes/lote7s-b5-issue39.txt): páginas da Metadata API de
ExtlClntAppAttestSettings, ExtlClntAppAttestConfigurablePolicies, ExtlClntAppOauthSecuritySettings, McpServerDefinition e
ApiNamedQuery (o endpoint versionado devolve binário), mobileAppConfig de ConnectedApp e o caminho para criar escopo OAuth customizado.

Ordem: lote7r_b5_setup_restantes.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv, ev           # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7s-b5-issue39.txt"
DOC = dict(tipo="oficial_documentacao", versao="sem versão (site novo de documentação)", metodo="leitura_resultado_busca")
AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")
D = "https://developer.salesforce.com/docs/platform/"
H = "https://help.salesforce.com/s/articleView?id="
C.registrar_fontes([
    C.fonte("src:rest-composite-post", "Send Multiple Requests Using Composite (REST API Developer Guide)",
            D + "api-rest/guide/resources-composite-composite-post.html",
            "Limite de 25 subrequisições por chamada Composite, até 5 delas de sObject Collections ou consulta.", EXTR, DATA, **DOC),
    C.fonte("src:rest-composite-request-body", "Composite Request Body (REST API Developer Guide)",
            D + "api-rest/guide/requests-composite.html",
            "Comportamento de allOrNone no corpo da requisição Composite.", EXTR, DATA, **DOC),
    C.fonte("src:rest-composite-graph-intro", "Using Composite Graphs (REST API Developer Guide)",
            D + "api-rest/guide/resources-composite-graph-introduction.html",
            "Composite graphs elevam o limite de subrequisições de 25 para 500.", EXTR, DATA, **DOC),
    C.fonte("src:limits-cheatsheet-metadata", "Metadata Limits (Salesforce Developer Limits and Allocations Quick Reference)",
            D + "salesforce-app-limits-cheatsheet/guide/salesforce-app-limits-platform-metadata.html",
            "Limites de arquivos e de tamanho do .zip em deploy e retrieve pela Metadata API.", EXTR, DATA, **DOC),
    C.fonte("src:help-token-exchange-enable", "Enable Apps for a Token Exchange Handler (Salesforce Help)",
            H + "xcloud.remoteaccess_token_exchange_enable.htm&language=en_US&type=5",
            "Página Token Exchange Handlers do Setup.", EXTR, DATA, **AJ),
    C.fonte("src:help-private-connect-inbound-aws", "Establish an Inbound Connection with AWS (Salesforce Help)",
            "https://help.salesforce.com/apex/HTViewHelpDoc?id=private_connect_inbound_aws.htm",
            "Conexão de entrada criada pelo assistente da página Private Connect do Setup.", EXTR, DATA, **AJ),
])


def trocar_limitacao(fid, antiga_prefixo, nova, srcs):
    f = ld(f"funcionalidades/{fid}.json")
    f["limitacoes"] = [x for x in f["limitacoes"] if not (isinstance(x, str) and x.startswith(antiga_prefixo))]
    if nova not in f["limitacoes"]:
        f["limitacoes"].append(nova)
    f["evidencias"] += [ev(s) for s in srcs if not any(e["fonte"] == s for e in f["evidencias"])]
    sv(f"funcionalidades/{fid}.json", f)


trocar_limitacao("rest-api", "O número máximo de subrequisições do Composite",
                 "Composite aceita até 25 subrequisições por chamada, das quais no máximo 5 podem ser sObject Collections ou consultas; "
                 "composite graphs sobem o limite para 500. Com allOrNone verdadeiro, um erro desfaz a requisição inteira; com falso, "
                 "seguem as subrequisições que não dependem da que falhou.",
                 ["src:rest-composite-post", "src:rest-composite-request-body", "src:rest-composite-graph-intro"])
trocar_limitacao("metadata-api", "Os limites da Metadata API não foram obtidos",
                 "Deploy e retrieve aceitam até 10.000 arquivos por vez; o .zip pode ter até 39 MB compactado (o limite de 50 MB da "
                 "mensagem SOAP vale depois da codificação base-64) e até 600 MB descompactado.",
                 ["src:limits-cheatsheet-metadata"])
C.definir_setup("oauth-escopos-e-troca-de-token",
                "Atribuir escopo customizado: Setup > Quick Find: External Client Apps Manager > (app) > Policies > OAuth Policies; "
                "handlers de troca de token: Setup > Quick Find: Token > Token Exchange Handlers",
                "O caminho para criar o escopo customizado não foi confirmado.",
                ["src:help-eca-custom-scope-assign", "src:help-token-exchange-enable"])
C.definir_setup("conexoes-de-rede-privadas",
                "Setup > Quick Find: Private Connect > Private Connect (Create Outbound Connection, ou o assistente de Inbound Connection)",
                "A mesma página reúne as conexões de saída e de entrada; o add-on de Private Connect é cobrado à parte.",
                ["src:help-snowflake-private-connect", "src:help-private-connect-inbound-aws"])
print("lote 7s: 2 limites e 2 caminhos de Setup")
