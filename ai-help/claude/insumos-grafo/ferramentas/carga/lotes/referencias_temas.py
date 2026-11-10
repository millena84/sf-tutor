"""Issue #34, fase 3: referências oficiais dos temas de primeiro nível (classificações).

Cada referência aponta uma área da documentação oficial e diz, no início da nota, como ela corresponde ao tema:
"Cobre o tema", "Cobre parte do tema" ou "Mais ampla que o tema". O estado continua "desconhecido": o recorte é
do projeto e a conferência é parcial (o site mostra "Parcialmente conferido").

Extração: fontes/extracoes/temas-referencias-oficiais.txt. Reexecutável.
Uso: python3 ferramentas/carga/lotes/referencias_temas.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from carga.base import ROOT, save, ev  # noqa: E402
from carga.catalogo import fonte, registrar_fontes  # noqa: E402

DATA = "2026-11-09"
EXT = "fontes/extracoes/temas-referencias-oficiais.txt"
AJUDA = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)")

FONTES = [
    fonte("src:help-produtos-platform", "Salesforce Help — Platform (diretório de documentação)", "https://help.salesforce.com/s/products/platform",
          "Áreas de documentação da plataforma: automação, usuários e acesso, personalização sem código, código, sandboxes, ciclo de vida e segurança.", EXT, DATA, **AJUDA),
    fonte("src:help-produtos-sales", "Salesforce Help — Sales (diretório de documentação)", "https://help.salesforce.com/s/products/sales",
          "Áreas de documentação de vendas, incluindo Sales Basics e Data Quality.", EXT, DATA, **AJUDA),
    fonte("src:help-produtos-analytics", "Salesforce Help — Analytics (diretório de documentação)", "https://help.salesforce.com/s/products/analytics",
          "Reports and Dashboards e produtos analíticos (CRM Analytics, Tableau).", EXT, DATA, **AJUDA),
    fonte("src:help-setup-company", "Set Up Your Company in Salesforce", "https://help.salesforce.com/apex/HTViewHelpDoc?id=admin_profile.htm",
          "Guia Set Up and Maintain Your Salesforce Organization: empresa, idioma, moeda, ano fiscal, interface e atualizações.", EXT, DATA, **AJUDA),
    fonte("src:security-guide", "Salesforce Security Guide",
          "https://developer.salesforce.com/docs/atlas.en-us.securityImplGuide.meta/securityImplGuide/security_guide_intro.htm",
          "Autenticação, acesso a dados, compartilhamento, auditoria e monitoramento de eventos.", EXT, DATA, versao="67.0"),
    fonte("src:apex-async-overview", "Asynchronous Apex (Apex Developer Guide)",
          "https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/api/apex_async_overview.htm",
          "Queueable, Scheduled, Batch e Future em Apex e quando usar cada um.", EXT, DATA),
    fonte("src:integration-patterns", "Integration Patterns Overview (Integration Patterns and Practices)",
          "https://developer.salesforce.com/docs/atlas.en-us.integration_patterns_and_practices.meta/integ_pat_tempate.htm",
          "Padrões de integração, matriz de seleção e boas práticas.", EXT, DATA),
    fonte("src:sfdx-dev-guide", "Salesforce DX Developer Guide",
          "https://developer.salesforce.com/docs/atlas.en-us.262.0.sfdx_dev.meta/sfdx_dev/sfdx_setup_dx_tools.htm",
          "Projetos, scratch orgs, sandboxes, rastreamento de alterações, pacotes e integração contínua.", EXT, DATA, versao="sem rótulo na página (endereço 262.0)"),
    fonte("src:objref-data-model", "Data Model (Object Reference)",
          "https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/data_model.htm",
          "Diagramas entidade-relacionamento dos objetos padrão (Data Model Gallery).", EXT, DATA),
    fonte("src:agentforce-dev-guide", "Get Started — Agentforce Developer Guide", "https://developer.salesforce.com/docs/ai/agentforce/guide",
          "Agentes, ações, Agent Script, modelos e prompts, Trust Layer.", EXT, DATA, versao="sem versão (página de 2026)"),
    fonte("src:data-model-files", "Salesforce Files (Data Model Gallery)", "https://developer.salesforce.com/docs/platform/data-models/guide/salesforce-files.html",
          "Entidades de arquivos, versões, bibliotecas, pastas e ligação a registros.", EXT, DATA, versao="sem versão na página"),
]

PL = "src:help-produtos-platform"
REFS = {
    "cls:organizacao-e-configuracoes-base": [
        ev("src:help-setup-company", "Cobre parte do tema: o guia reúne empresa, idioma, localidade, moeda, ano fiscal e atualizações de release. Horário comercial e domínios não aparecem nesta página.",
           "Set Up and Maintain Your Salesforce Organization"),
    ],
    "cls:acesso-identidade-e-seguranca": [
        ev(PL, "Cobre o tema: as duas áreas tratam de usuários, permissões, acesso a dados, autenticação e proteções da org.", "Manage Users and Data Access; Secure Your Salesforce Org"),
        ev("src:security-guide", "Mais ampla que o tema: além de autenticação, acesso e compartilhamento, o guia traz auditoria e monitoramento, que neste tutorial ficam em \"Observabilidade, auditoria e operação\".",
           "Authenticate Users; Give Users Access to Data; Share Objects and Fields"),
    ],
    "cls:dados-e-modelagem": [
        ev("src:objref-data-model", "Cobre parte do tema: diagramas dos objetos padrão e de suas relações. O modelo dos objetos customizados depende de cada org.", "Data Model"),
        ev(PL, "Mais ampla que o tema: a área também cobre aparência, processos, sites e apps feitos sem código.", "Extend Salesforce with Clicks, Not Code"),
    ],
    "cls:qualidade-governanca-e-ciclo-de-vida-dos-dados": [
        ev("src:help-produtos-sales", "Cobre parte do tema: duplicidade de registros e importação de dados de terceiros.", "Data Quality"),
        ev(PL, "Cobre parte do tema: disponibilidade, conformidade e segurança ao longo do ciclo de vida dos dados, por meio dos produtos Own.", "Own from Salesforce"),
    ],
    "cls:automacao-de-processos-e-regras-de-negocio": [
        ev(PL, "Cobre parte do tema: ferramentas declarativas para experiências guiadas, automação em segundo plano e aprovações. A automação em Apex não aparece na descrição desta área.",
           "Automate Your Business Processes"),
    ],
    "cls:interface-e-experiencia-do-usuario": [
        ev("src:help-setup-company", "Cobre parte do tema: personalização da interface dentro do guia de configuração da org.", "Customize the User Interface"),
        ev(PL, "Mais ampla que o tema: a área inclui aparência e apps, mas também dados e processos.", "Extend Salesforce with Clicks, Not Code"),
    ],
    "cls:execucao-assincrona-lotes-e-agendamento": [
        ev("src:apex-async-overview", "Cobre parte do tema: Queueable, Scheduled, Batch e Future em Apex. Partes assíncronas de automações declarativas e monitoramento de jobs não estão nesta página.",
           "Asynchronous Apex"),
    ],
    "cls:integracao-apis-e-eventos": [
        ev("src:integration-patterns", "Cobre parte do tema: padrões de integração, matriz de seleção e boas práticas. O detalhe de cada API fica nos guias próprios, já citados nas funcionalidades.",
           "Integration Patterns Overview"),
    ],
    "cls:relatorios-analytics-e-exploracao": [
        ev("src:help-produtos-analytics", "Cobre o tema: Reports and Dashboards corresponde a relatórios e dashboards; CRM Analytics e Tableau correspondem a \"Recursos analíticos específicos de produto\".",
           "Reports and Dashboards; CRM Analytics; Tableau"),
    ],
    "cls:conteudo-conhecimento-e-colaboracao": [
        ev("src:data-model-files", "Cobre parte do tema: arquivos, versões, bibliotecas e pastas. Knowledge, colaboração e modelos de comunicação ficam fora deste diagrama.", "Salesforce Files"),
    ],
    "cls:desenvolvimento-testes-e-entrega": [
        ev("src:sfdx-dev-guide", "Cobre parte do tema: projeto, scratch orgs, sandboxes, rastreamento de alterações, pacotes desbloqueados e integração contínua.", "Salesforce DX Developer Guide"),
        ev(PL, "Cobre parte do tema: ambientes de teste e boas práticas de ciclo de vida e release.", "Sandboxes: Staging Environments for Customizing and Testing; Lifecycle Center"),
    ],
    "cls:observabilidade-auditoria-e-operacao": [
        ev("src:security-guide", "Cobre parte do tema: logins, histórico de campos, alterações de configuração e eventos em tempo quase real. Logs de depuração e consumo de limites não estão nestas seções.",
           "Audit and Monitor Your Organization's Security; Real-Time Event Monitoring"),
    ],
    "cls:ia-agentes-e-decisoes-assistidas": [
        ev("src:agentforce-dev-guide", "Cobre parte do tema: agentes, ações, modelos e prompts pelo lado do desenvolvimento; a governança aparece na página relacionada Trust Layer.", "Get Started"),
    ],
    "cls:processos-de-negocio-especificos-de-produto": [
        ev("src:help-produtos-sales", "Cobre parte do tema: documentação do produto de vendas, que corresponde ao tema interno \"Vendas\".", "Sales Basics"),
        ev("src:help-service-basics", "Cobre parte do tema: base do produto de atendimento, que corresponde ao tema interno \"Atendimento\".", "Service Basics"),
    ],
}

NOTA_ESTADO = ("Tema criado pelo projeto (00-especificacao-grafo.md), não é nomenclatura oficial da Salesforce. Cruzado em "
               + DATA + " com áreas da documentação oficial listadas nas referências; a correspondência é parcial e o recorte continua sendo do projeto.")


def aplicar():
    novos = registrar_fontes(FONTES)
    d = os.path.join(ROOT, "classificacoes")
    vistos = set()
    for nome in sorted(os.listdir(d)):
        if not nome.endswith(".json"):
            continue
        with open(os.path.join(d, nome), encoding="utf-8") as f:
            ent = json.load(f)
        if ent["id"] not in REFS:
            raise SystemExit(f"sem referência: {ent['id']}")
        ent["referencias_oficiais"] = REFS[ent["id"]]
        ent["nota_estado"] = NOTA_ESTADO
        save("classificacoes", nome[:-5], ent)
        vistos.add(ent["id"])
    if set(REFS) - vistos:
        raise SystemExit(f"temas inexistentes: {sorted(set(REFS) - vistos)}")
    print(f"fontes novas: {len(novos)}; temas com referência: {len(vistos)}")


if __name__ == "__main__":
    aplicar()
