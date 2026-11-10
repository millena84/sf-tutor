"""Issue #34: conteúdo específico por tema (para_iniciantes, encadeamento, avancado).

Piloto: cls:interface-e-experiencia-do-usuario e sub:lightning-pages-e-componentes.
Textos são redação do projeto; cada bloco cita as fontes dos fatos que usa. Nada de valores, limites ou
caminhos sem fonte. Extração: fontes/extracoes/temas-piloto-interface.txt (fontes novas) e notas já existentes
das funcionalidades citadas.

Reexecutável: grava só os três campos, logo depois de fora_do_escopo.
Uso: python3 ferramentas/carga/lotes/conteudo_temas.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from carga.base import ROOT, save, ev  # noqa: E402
from carga.catalogo import fonte, registrar_fontes  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conteudo_cls import CONTEUDO_CLS  # noqa: E402
from conteudo_sub import CONTEUDO_SUB, PENDENTES  # noqa: E402
from conteudo_pendentes import CONTEUDO_PENDENTES, FONTES_PENDENTES  # noqa: E402
from conteudo_pendentes2 import CONTEUDO_PENDENTES2, FONTES_PENDENTES2  # noqa: E402
from conteudo_pendentes3 import CONTEUDO_PENDENTES3, FONTES_PENDENTES3  # noqa: E402
from conteudo_pendentes4 import CONTEUDO_PENDENTES4, FONTES_PENDENTES4  # noqa: E402

DATA = "2026-11-09"
EXT = "fontes/extracoes/temas-piloto-interface.txt"

FONTES = [
    fonte("src:architect-build-forms", "Building Forms (Salesforce Architects — Platform Decision Guides)",
          "https://architect.salesforce.com/decision-guides/build-forms",
          "Quando usar Dynamic Forms, Screen Flow, Omnistudio ou LWC; segurança, testes e implantação de formulários.",
          EXT, DATA, tipo="oficial_documentacao", versao="sem versão na página"),
    fonte("src:security-fls", "Field-Level Security (Salesforce Security Guide)",
          "https://developer.salesforce.com/docs/atlas.en-us.244.0.securityImplGuide.meta/securityImplGuide/admin_fls.htm",
          "Como page layout e segurança em nível de campo se combinam.", EXT, DATA, versao="58.0"),
    fonte("src:help-lightning-pages", "Lightning Pages (Salesforce Help)", "https://help.salesforce.com/s/articleView?id=sf.lightning_page_overview.htm&type=5",
          "O que são Lightning pages, tipos de página e origem dos componentes.", EXT, DATA,
          tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)"),
    fonte("src:apex-queueable", "Queueable Apex (Apex Developer Guide)",
          "https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/pages/apex_queueing_jobs.htm",
          "Recomendação de Queueable no lugar de future methods; identificador do job.",
          "fontes/extracoes/temas-referencias-oficiais.txt", DATA, metodo="leitura_resultado_busca"),
]

AF = "src:architect-build-forms"

CONTEUDO = {
    "cls:interface-e-experiencia-do-usuario": {
        "para_iniciantes": {
            "explicacao": ("É o que a pessoa vê e usa ao trabalhar na Salesforce: o app aberto, as abas de navegação, a página de "
                           "um registro com seus campos e componentes, os botões de ação e as etapas que guiam um processo. "
                           "Configurar este tema é decidir o que aparece, onde e em que ordem, sem mudar os dados guardados por trás."),
            "exemplo": ("Uma vendedora abre o app de vendas, clica na aba Oportunidades e abre uma oportunidade. Na mesma página "
                        "ela vê os campos principais, um botão de ação rápida e a barra com as etapas da venda."),
            "analogia": {
                "texto": "Pense numa loja: os dados são o estoque no depósito; a interface é a vitrine, as prateleiras e as placas que levam cada cliente ao que precisa.",
                "limite": ("Na loja, tirar um produto da vitrine o esconde. Na Salesforce, tirar um campo da página não é controle "
                           "de acesso: quem decide se a pessoa pode ver ou editar o campo é a segurança em nível de campo."),
            },
            "por_onde_comecar": ["func:lightning-pages", "func:tabs"],
            "evidencias": [ev("src:help-lightning-pages"), ev("src:help-custom-tabs"), ev("src:help-quick-actions"),
                           ev("src:help-path-create"), ev("src:security-fls", "Segurança de campo prevalece sobre o layout.")],
        },
        "encadeamento": {
            "texto": ("As abas são as entradas de navegação de um app e levam a objetos, páginas, componentes ou endereços. Ao abrir um "
                      "registro, uma Lightning page organiza o que aparece, montada com componentes no Lightning App Builder. Ações "
                      "rápidas são botões que abrem um formulário curto ou executam algo no contexto do registro, e o Path mostra as "
                      "etapas de um processo a partir de um campo picklist. Apps de console colocam vários registros em abas e subabas "
                      "ao mesmo tempo. Sites, portais e mobile levam a experiência para fora do app interno; esse tema interno ainda não "
                      "tem funcionalidades catalogadas."),
            "evidencias": [ev("src:help-custom-tabs"), ev("src:help-lightning-pages"), ev("src:help-app-builder"),
                           ev("src:help-quick-actions"), ev("src:help-path-create"), ev("src:help-console-intro")],
        },
        "avancado": [
            {"tipo": "decisao", "titulo": "Qual ferramenta usar para um formulário",
             "texto": ("Para criar, editar ou ver um único objeto numa página de registro, o guia de decisão indica Dynamic Forms: é o "
                       "caminho com menos armadilhas, mas o menos flexível; não faz navegação em várias telas nem reúso e não está "
                       "disponível em páginas do Experience Cloud. Assistentes com várias telas, sem exigência rígida de marca, ficam "
                       "com Screen Flow. Experiência sofisticada e estilo detalhado pedem LWC, com mais liberdade e menos proteções. "
                       "Omnistudio atende clientes de Industries e exige o pacote correspondente."),
             "evidencias": [ev(AF, secao="Building Forms")]},
            {"tipo": "seguranca", "titulo": "A página não é controle de acesso",
             "texto": ("Page layout e segurança em nível de campo se combinam e vale a configuração mais restritiva: um campo obrigatório "
                       "no layout, mas somente leitura na segurança de campo, continua somente leitura. Campos universalmente "
                       "obrigatórios aparecem na edição de qualquer forma. Dynamic Forms e LWC rodam no contexto do usuário; Screen Flow "
                       "também, por padrão, mas pode rodar em contexto de sistema, o que deve ficar restrito a usuários confiáveis."),
             "evidencias": [ev("src:security-fls", "Lida na versão 58.0; a página atual não exibiu o artigo."), ev(AF, secao="Sanitize Inputs")]},
            {"tipo": "testes", "titulo": "Como testar cada abordagem",
             "texto": ("Só LWC permite testes unitários escritos, por exemplo com Jest. Dynamic Forms e Screen Flow dependem de automação "
                       "de interface de ponta a ponta, que confere o resultado na tela, mas não as saídas de métodos."),
             "evidencias": [ev(AF, secao="Consider UI Test Automation Requirements")]},
            {"tipo": "implantacao", "titulo": "Como levar entre ambientes",
             "texto": ("Dynamic Forms, Screen Flows e LWC podem ir por pacotes gerenciados (1GP e 2GP), pacotes desbloqueados, change "
                       "sets e DevOps Center. Omnistudio usa o IDX Workbench e não aceita empacotamento, o que pesa na escolha quando a "
                       "entrega é por pacote."),
             "evidencias": [ev(AF)]},
        ],
    },
    "sub:lightning-pages-e-componentes": {
        "para_iniciantes": {
            "explicacao": ("Uma Lightning page é uma página montada com blocos, chamados componentes, arrastados para as regiões de um "
                           "modelo no Lightning App Builder. É assim que se monta a página inicial, a página de um app ou a página que "
                           "aparece ao abrir um registro."),
            "exemplo": "A página de um contrato com os campos principais no topo, uma aba com o histórico e outra com os registros relacionados.",
            "analogia": {
                "texto": "Como um quadro de avisos com áreas demarcadas: o modelo define as áreas e você prende os cartões (componentes) onde quiser.",
                "limite": "No quadro, qualquer cartão serve em qualquer área. Na Lightning page, componentes customizados podem precisar de configuração para aparecer no Lightning App Builder.",
            },
            "por_onde_comecar": ["func:lightning-pages"],
            "evidencias": [ev("src:help-lightning-pages"), ev("src:help-app-builder")],
        },
        "encadeamento": {
            "texto": ("Dentro de Interface, este é o tema da página em si. As abas levam até ela; ações rápidas e Path são recursos que "
                      "aparecem na página do registro. As páginas de registro também são estudadas em \"Layouts e páginas de registro\", "
                      "onde esta funcionalidade aparece como secundária."),
            "evidencias": [ev("src:help-lightning-pages"), ev("src:help-custom-tabs")],
        },
        "avancado": [
            {"tipo": "decisao", "titulo": "Onde a Lightning page se encaixa",
             "texto": ("A Lightning page fica entre o page layout, que só posiciona campos, e o Visualforce, que é desenvolvimento livre: "
                       "posiciona componentes e se adapta ao dispositivo conforme o modelo escolhido. Para formulários de um único objeto "
                       "na página de registro, o guia de decisão indica Dynamic Forms antes de partir para LWC."),
             "evidencias": [ev("src:help-lightning-pages"), ev(AF, secao="Building Forms")]},
            {"tipo": "implantacao", "titulo": "Como a página aparece nos metadados",
             "texto": ("Cada Lightning page é um componente FlexiPage. A propriedade type diz o tipo de página; entre os valores "
                       "documentados estão AppPage, HomePage, RecordPage e UtilityBar, além de vários tipos de páginas do Experience "
                       "Cloud (prefixo Comm)."),
             "evidencias": [ev("src:mdapi-flexipage", "Propriedade type (enum fechado).")]},
            {"tipo": "seguranca", "titulo": "Visibilidade na página não substitui permissão",
             "texto": ("O que a página mostra não decide o que a pessoa pode acessar: a segurança em nível de campo prevalece sobre o "
                       "layout. Dynamic Forms e LWC colocados na página rodam no contexto do usuário."),
             "evidencias": [ev("src:security-fls", "Lida na versão 58.0."), ev(AF)]},
            {"tipo": "atencao", "titulo": "Componentes customizados",
             "texto": ("Componentes vêm de três origens: os padrão da Salesforce, os customizados e os de terceiros (AppExchange). Os "
                       "customizados podem precisar de configuração para funcionar no Lightning App Builder."),
             "evidencias": [ev("src:help-lightning-pages")]},
        ],
    },
}

CAMPOS = ("para_iniciantes", "encadeamento", "avancado")


def aplicar():
    novos = registrar_fontes(FONTES + FONTES_PENDENTES + FONTES_PENDENTES2 + FONTES_PENDENTES3 + FONTES_PENDENTES4)
    todos = {**CONTEUDO, **CONTEUDO_CLS, **CONTEUDO_SUB, **CONTEUDO_PENDENTES, **CONTEUDO_PENDENTES2, **CONTEUDO_PENDENTES3, **CONTEUDO_PENDENTES4}
    assert not set(todos) & set(PENDENTES), "tema pendente com conteúdo"
    for tid, cont in todos.items():
        pasta = "classificacoes" if tid.startswith("cls:") else "subclassificacoes"
        nome = tid.split(":", 1)[1]
        with open(os.path.join(ROOT, pasta, nome + ".json"), encoding="utf-8") as f:
            ent = json.load(f)
        novo = {}
        for k, v in ent.items():
            if k in CAMPOS:
                continue
            novo[k] = v
            if k == "fora_do_escopo":
                for c in CAMPOS:
                    if c in cont:
                        novo[c] = cont[c]
        save(pasta, nome, novo)
    print(f"fontes novas: {len(novos)}; temas com conteúdo: {len(todos)}")


if __name__ == "__main__":
    aplicar()
