"""Issue #34, item 3 (limpeza do dado genérico dos temas internos), um tema principal por vez.

Para cada tema interno listado em TEMAS:
- "descricao": troca a frase genérica da carga inicial por uma descrição curta escrita pelo projeto (resumo do tema, sem
  fato técnico novo além dos já catalogados);
- "referencias_oficiais": áreas da documentação oficial já registradas em fontes/registro.json; cada nota começa com
  "Cobre o tema", "Cobre parte do tema" ou "Mais ampla que o tema" (o validador exige);
- "nota_estado": mesma redação dos temas principais. O "estado" continua "desconhecido": o recorte é do projeto e a
  conferência é parcial (o site passa a mostrar "Parcialmente conferido").

Não registra fontes novas: só cita fontes que já existem (o script aborta se alguma faltar).
Reexecutável. Uso: python3 ferramentas/carga/lotes/temas_internos.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from carga.base import ROOT, save, ev  # noqa: E402

DATA = "2026-11-10"
NOTA_ESTADO = ("Tema criado pelo projeto (00-especificacao-grafo.md), não é nomenclatura oficial da Salesforce. Cruzado em "
               + DATA + " com áreas da documentação oficial listadas nas referências; a correspondência é parcial e o recorte continua sendo do projeto.")

# id -> (descricao, [referências])
TEMAS = {
    # ------------------------------------------------------------------ Integração, APIs e eventos
    "sub:apis-de-dados-e-metadados": (
        "As APIs que a plataforma oferece para outros sistemas lerem e gravarem na org: REST e SOAP para registros, Bulk API para "
        "grandes volumes, Metadata API para configuração e Tooling API para ferramentas de desenvolvimento.",
        [ev("src:rest-intro", "Cobre parte do tema: REST API.", "Introduction to REST API"),
         ev("src:soap-intro", "Cobre parte do tema: SOAP API e os WSDLs Enterprise e Partner.", "Introduction to SOAP API"),
         ev("src:bulk-api-intro", "Cobre parte do tema: Bulk API 2.0 e Bulk API.", "Introduction to Bulk API 2.0 and Bulk API"),
         ev("src:mdapi-intro", "Cobre parte do tema: Metadata API.", "Understanding Metadata API"),
         ev("src:tooling-intro", "Cobre parte do tema: Tooling API.", "Introduction to Tooling API")],
    ),
    "sub:autenticacao-de-integracoes": (
        "Como um sistema externo prova quem é ao chamar a org: o registro da integração num external client app ou connected app e "
        "os tokens OAuth, com escopos, que esse registro emite.",
        [ev("src:help-eca-create", "Cobre parte do tema: external client apps, o registro recomendado para integrações novas.", "Create an External Client App"),
         ev("src:help-connected-app-basics", "Cobre parte do tema: connected apps.", "Configure Basic Connected App Settings")],
    ),
    "sub:chamadas-externas-e-endpoints": (
        "As chamadas que a org faz para serviços de fora e os endereços liberados para elas: sites remotos, serviços externos "
        "descritos em OpenAPI, conexões privadas e os limites de callout.",
        [ev("src:help-remote-site", "Cobre parte do tema: liberação de endereços para callouts.", "Configure Remote Site Settings"),
         ev("src:apex-callout-limits", "Cobre parte do tema: limites e restrições de callouts em Apex.", "Callout Limits and Limitations")],
    ),
    "sub:credenciais": (
        "Onde a org guarda o endereço de um sistema externo e a forma de se autenticar nele, fora do código: named credentials e, "
        "desde a versão 56.0, external credentials.",
        [ev("src:help-nc-create", "Cobre parte do tema: criação e edição de named credentials.", "Create or Edit a Named Credential"),
         ev("src:mdapi-externalcredential", "Cobre parte do tema: external credentials como metadado.", "ExternalCredential")],
    ),
    "sub:eventos-e-mensageria": (
        "Como a org avisa outros sistemas, e é avisada, sem consulta periódica: eventos de plataforma, eventos de captura de "
        "alterações, a Pub/Sub API para assinar de fora e o Event Relay.",
        [ev("src:help-platform-events-define", "Cobre parte do tema: definição de eventos de plataforma.", "Define and Manage Platform Events"),
         ev("src:pubsub-overview", "Cobre parte do tema: publicação e assinatura de eventos por clientes externos.", "Pub/Sub API overview"),
         ev("src:help-event-relay-create", "Cobre parte do tema: envio de eventos para a AWS.", "Create an Event Relay")],
    ),
    "sub:conectividade-e-virtualizacao-de-dados": (
        "Como mostrar dados de outro sistema dentro da org sem copiá-los: objetos externos, lidos no momento da consulta a partir "
        "de uma fonte de dados externa.",
        [ev("src:help-external-data-source-odata", "Cobre parte do tema: fonte de dados externa pelo adaptador OData do Salesforce Connect.",
            "Define an External Data Source for Salesforce Connect—OData 2.0 or 4.0 Adapter")],
    ),
    "sub:contratos-limites-e-tratamento-de-falhas": (
        "As regras que valem para toda integração: quantas chamadas cabem por dia, quanto tempo cada uma pode levar, quais versões "
        "de API continuam valendo e como tratar falhas e retentativas.",
        [ev("src:limits-api-requests", "Cobre parte do tema: alocações e limites de requisições de API.", "API Request Limits and Allocations"),
         ev("src:rest-api-eol", "Cobre parte do tema: política de fim de vida das versões de API.", "API End-of-Life Policy"),
         ev("src:pe-retry-apex", "Cobre parte do tema: retentativa em assinantes de eventos.")],
    ),
    # ------------------------------------------------------------------ Acesso, identidade e segurança
    "sub:usuarios-e-provisionamento": (
        "O cadastro de quem acessa a org, pessoa ou integração, e o seu ciclo de vida: criar, ativar, congelar e desativar usuários, "
        "inclusive pela criação automática no primeiro login com SSO.",
        [ev("src:help-users", "Cobre parte do tema: gestão de usuários no Setup.", "View and Manage Users"),
         ev("src:objref-user", "Cobre parte do tema: o objeto User na API.", "User")],
    ),
    "sub:autenticacao-sso-e-mfa": (
        "Como uma pessoa prova quem é ao entrar: senha, login único com o provedor da empresa (SAML) e provedores de autenticação "
        "como OpenID Connect, Google e Microsoft.",
        [ev("src:security-guide", "Cobre parte do tema: a seção de autenticação de usuários do guia de segurança.", "Authenticate Users"),
         ev("src:mdapi-samlssoconfig", "Cobre parte do tema: configuração de SSO por SAML como metadado.", "SamlSsoConfig"),
         ev("src:help-auth-provider-oidc", "Cobre parte do tema: provedor de autenticação por OpenID Connect.",
            "Configure an Authentication Provider Using OpenID Connect")],
    ),
    "sub:sessoes-e-politicas-de-login": (
        "As regras de entrada depois que a identidade foi provada: por qual endereço, de quais IPs e em quais horários se pode entrar, "
        "e o histórico e o estado de login de cada usuário.",
        [ev("src:help-mydomain-login-policy", "Cobre parte do tema: política de login do My Domain.", "Set the My Domain Login Policy"),
         ev("src:help-login-history", "Cobre parte do tema: acompanhamento do histórico de login.", "Monitor Login History")],
    ),
    "sub:permissoes-perfis-e-grupos": (
        "O que cada usuário pode fazer: o perfil, único por usuário, dá o acesso básico; permission sets somam acessos; permission set "
        "groups juntam vários para atribuir de uma vez.",
        [ev("src:help-perm-sets-create", "Cobre parte do tema: criação de permission sets.", "Create Permission Sets"),
         ev("src:help-psg-create", "Cobre parte do tema: criação de permission set groups.", "Create a Permission Set Group")],
    ),
    "sub:licencas-e-entitlements-de-acesso": (
        "O teto do que pode ser concedido a um usuário: a licença de usuário dá o pacote básico, e feature licenses e permission set "
        "licenses liberam recursos que ela não inclui.",
        [ev("src:help-user-licenses", "Cobre parte do tema: licenças de usuário padrão.", "Standard User Licenses"),
         ev("src:help-service-feature-license", "Cobre parte do tema: exemplo de feature license (Service Cloud User).",
            "Assign the Service Cloud User Feature License")],
    ),
    "sub:acesso-a-registros-e-hierarquias": (
        "Quais registros cada usuário enxerga: os padrões de acesso da org, o compartilhamento e as equipes de conta e de oportunidade.",
        [ev("src:security-guide", "Cobre parte do tema: as seções de acesso a dados e de compartilhamento do guia de segurança.",
            "Give Users Access to Data; Share Objects and Fields"),
         ev("src:mdapi-sharingsettings", "Cobre parte do tema: configurações de compartilhamento como metadado.", "SharingSettings")],
    ),
    "sub:credenciais-certificados-e-protecao-de-dados": (
        "Os segredos que protegem as conexões da org: certificados e chaves, a autenticação mútua e as credenciais de acesso a "
        "sistemas externos.",
        [ev("src:help-cert-self-signed", "Cobre parte do tema: certificados autoassinados.", "Generate a Self-Signed Certificate"),
         ev("src:mdapi-certificate", "Cobre parte do tema: certificados como metadado.", "Certificate")],
    ),
}


def aplicar():
    with open(os.path.join(ROOT, "..", "fontes", "registro.json"), encoding="utf-8") as f:
        fontes = {x["id"] for x in json.load(f)["fontes"]}
    faltam = sorted({r["fonte"] for _, refs in TEMAS.values() for r in refs} - fontes)
    if faltam:
        raise SystemExit(f"fontes não registradas: {faltam}")
    d = os.path.join(ROOT, "subclassificacoes")
    for tid, (descricao, refs) in TEMAS.items():
        nome = tid.split(":", 1)[1]
        caminho = os.path.join(d, nome + ".json")
        if not os.path.exists(caminho):
            raise SystemExit(f"tema inexistente: {tid}")
        with open(caminho, encoding="utf-8") as f:
            ent = json.load(f)
        ent["descricao"] = descricao
        ent["referencias_oficiais"] = refs
        ent["nota_estado"] = NOTA_ESTADO
        save("subclassificacoes", nome, ent)
    print(f"temas internos atualizados: {len(TEMAS)}")


if __name__ == "__main__":
    aplicar()
