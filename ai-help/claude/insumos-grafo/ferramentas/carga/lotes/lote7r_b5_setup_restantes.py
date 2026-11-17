"""Lote 7r (rodada B5, fechamento; issue #34): caminhos de Setup das 10 funcionalidades que restavam.

Nove ficam verificadas. Recycle Bin e os serviços externos do Commerce não são telas de Setup:
o caminho registrado é o da interface onde a fonte manda ir (App Launcher e app Commerce), e a nota diz isso.
configuracoes-de-nuvens-de-setor continua 'desconhecido': nenhuma fonte lida dá um caminho único.

Ordem: lote7q_b5_setup.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7r_b5_setup_restantes.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import caminho                # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7r-b5-setup-restantes.txt"
H = "https://help.salesforce.com/s/articleView?id="
AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")
# id da fonte, título, artigo (ou URL completa), nota
FONTES = [
    ("src:help-data-library-create", "Create a Data Library", "ai.data_library_create.htm",
     "Criação de data library pela página Agentforce Data Library do Setup; exige Data 360 configurado."),
    ("src:help-crm-analytics-basic-setup", "Basic CRM Analytics Platform Setup", "analytics.bi_help_setup_basic.htm",
     "Ativação do CRM Analytics em Setup > Analytics > Getting Started."),
    ("src:help-dynamic-forms-migrate", "Migrate a Record Page to Dynamic Forms", "dynamic_forms_migrate.htm",
     "Migração de uma record page para Dynamic Forms a partir de Object Manager > Lightning Record Pages."),
    ("src:help-prompt-field-gen-record-page", "Add a Field Generation Prompt Template to a Lightning Record Page",
     "sf.prompt_builder_add_field_gen_to_lightning_record_page.htm",
     "Descreve o botão Upgrade Now do componente Record Detail, que converte a página para Dynamic Forms."),
    ("src:help-trust-layer-setup", "Set up Einstein Trust Layer", "ai.generative_ai_trust_setup.htm",
     "Página Einstein Trust Layer do Setup, com abas de data masking e de segurança de conteúdo; exige Einstein Generative AI e Data Cloud."),
    ("src:help-track-field-history", "Track Object Field History", "xcloud.tracking_field_history_for_standard_objects.htm",
     "Página Field History Tracking do Setup; objetos sem suporte a política de retenção mostram N/A."),
    ("src:help-orchestrator-build", "Build an Orchestration", "orchestrator_build.htm",
     "Orquestrações são criadas pelo botão New Flow da página Flows do Setup; exige Manage Flow."),
    ("src:help-recycle-bin-manage", "Manage the Recycle Bin in Lightning Experience", "sf.recycle_bin_manage.htm",
     "No Lightning Experience a Recycle Bin é aberta pelo App Launcher ou pela barra de navegação; esvaziar a da org exige Modify All Data."),
    ("src:help-revenue-settings", "Enabling Revenue Settings", "sf.qocal_turn_on_quote_and_order_capture.htm",
     "Página Revenue Settings do Setup, onde se liga Enable Revenue Cloud Features."),
    ("src:help-commerce-extensions-store", "Replace a Default Commerce Process with an Apex Class", "sf.comm_extensions.htm",
     "No app Commerce: loja > Settings > Store > aba Extensions > Select Provider."),
]
# funcionalidade, caminho, nota, fontes
LINHAS = [
    ("agentforce-data-library", "Setup > Quick Find: Agentforce Data Library > Agentforce Data Library > New Library",
     "Exige Data 360 configurado; data libraries consomem créditos do Data 360.", ["src:help-data-library-create"]),
    ("crm-analytics", "Setup > Quick Find: Analytics > Getting Started > Enable CRM Analytics",
     "Ativação da plataforma; o acesso dos usuários vem de permission sets das licenças CRM Analytics.", ["src:help-crm-analytics-basic-setup"]),
    ("dynamic-forms", "Setup > Object Manager > [objeto] > Lightning Record Pages > [página] > Edit; no Lightning App Builder, selecione o componente Record Detail > Upgrade Now",
     "A configuração acontece no Lightning App Builder; nem todo objeto padrão é suportado.",
     ["src:help-dynamic-forms-migrate", "src:help-prompt-field-gen-record-page"]),
    ("einstein-trust-layer", "Setup > Quick Find: Einstein > Einstein Trust Layer",
     "Exige Einstein Generative AI ativado e Data Cloud configurado.", ["src:help-trust-layer-setup"]),
    ("field-audit-trail", "Setup > Quick Find: Field History Tracking > Field History Tracking > [objeto] > View",
     "Aqui se escolhem os campos rastreados. A política de retenção (HistoryRetentionPolicy) é definida e implantada pela Metadata API, não por esta tela.",
     ["src:help-track-field-history"]),
    ("flow-orchestration", "Setup > Quick Find: Flows > Flows > New Flow (escolha um tipo de orquestração)",
     "Mesma página dos flows; exige Manage Flow.", ["src:help-orchestrator-build"]),
    ("recycle-bin", "App Launcher > Recycle Bin",
     "Não é uma tela de Setup: no Lightning Experience a Recycle Bin é aberta pelo App Launcher ou pela barra de navegação.", ["src:help-recycle-bin-manage"]),
    ("revenue-management", "Setup > Quick Find: Revenue Settings > Revenue Settings",
     "Ligue Enable Revenue Cloud Features; exige licença de Revenue Management.", ["src:help-revenue-settings"]),
    ("servicos-externos-registrados-commerce", "App Commerce > [loja] > Settings > Store > Extensions > Select Provider",
     "Não é uma tela de Setup: a escolha do provedor fica no app Commerce. O registro do provedor continua podendo ser feito por API.",
     ["src:help-commerce-extensions-store"]),
]
p = caminho("fontes", "registro.json")
reg = json.load(open(p, encoding="utf-8"))
novas = [C.fonte(i, t + " (Salesforce Help)", H + a + "&language=en_US&type=5", n, EXTR, DATA, **AJ) for i, t, a, n in FONTES]
ids = {x["id"] for x in novas}
reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for fid, cam, nota, srcs in LINHAS:
    C.definir_setup(fid, cam, nota, srcs)
C.definir_setup("configuracoes-de-nuvens-de-setor", None,
                "Sem caminho único confirmado: cada nuvem de setor tem páginas de configuração próprias (por exemplo, Public Sector Solutions Settings), "
                "e nenhuma fonte lida mostra onde ficam, no Setup, as opções gravadas em IndustriesSettings.", [], estado="desconhecido")
print("lote 7r:", len(LINHAS), "caminhos; 1 segue desconhecido")
