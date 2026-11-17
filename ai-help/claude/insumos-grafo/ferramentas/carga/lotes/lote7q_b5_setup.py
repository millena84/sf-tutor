"""Lote 7q (rodada B5, parte D; issue #34): caminhos de Setup verificados na Ajuda para 16 funcionalidades que estavam sem caminho.

Ordem: lote7p_b5_objetos.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
Uso: python3 ferramentas/carga/lotes/lote7q_b5_setup.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import caminho                # noqa: E402
from carga import catalogo as C               # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7q-b5-setup.txt"
H = "https://help.salesforce.com/s/articleView?id="
AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")
# funcionalidade, id da fonte, título, artigo, caminho, nota
LINHAS = [
    ("classes-apex", "src:help-apex-classes-list", "Check for API Versions", "xcloud.admin_locales_check_version.htm",
     "Setup > Quick Find: Apex Classes > Apex Classes", "Lista de classes Apex da org, com a versão de cada uma."),
    ("compact-layouts", "src:help-compact-layout-create", "Create Compact Layouts", "platform.compact_layout_create.htm",
     "Setup > Object Manager > [objeto] > Compact Layouts > New", "Nas configurações do objeto; até 10 campos."),
    ("custom-report-types", "src:help-custom-report-type-approval", "Create a Custom Report Type for Approval History", "approval_history_custom_report_type.htm",
     "Setup > Quick Find: Report Types > Report Types > New Custom Report Type", "Exige Manage Custom Report Types."),
    ("duplicate-management", "src:help-duplicate-rules-create", "Customize Duplicate Rules", "sf.duplicate_rules_create.htm",
     "Setup > Quick Find: Duplicate Rules > Duplicate Rules > New Rule; Setup > Quick Find: Matching Rules > Matching Rules > New Rule",
     "Duas páginas: regras de duplicidade e regras de correspondência."),
    ("processos-de-aprovacao", "src:help-approval-standard-wizard", "Create a Classic Approval Process with the Standard Wizard",
     "approvals_creating_approval_processes.htm", "Setup > Quick Find: Approval Processes > Approval Processes > Create New Approval Process",
     "Escolha o objeto e o assistente (Standard Setup Wizard ou Jump Start Wizard)."),
    ("sandboxes", "src:help-sandbox-refresh", "Refresh Your Sandbox (KB)", "000229510",
     "Setup > Quick Find: Sandboxes > Sandboxes", "Lista das sandboxes; criar e atualizar exige Manage Sandboxes."),
    ("static-resources", "src:help-static-resources-define", "Define Static Resources", "pages_static_resources_create.htm",
     "Setup > Quick Find: Static Resources > Static Resources > New", "Exige Customize Application."),
    ("visualforce", "src:help-visualforce-pages-list", "Embed Salesforce Spiff in a Salesforce Page", "sales.spiff_embed.htm",
     "Setup > Quick Find: Visualforce Pages > Visualforce Pages > New", "Lista e criação de páginas Visualforce."),
    ("pacotes-gerenciados", "src:help-installed-packages", "Install the Order Management Basic Reports Package",
     "commerce.om_install_the_order_management_reports_package.htm", "Setup > Quick Find: Installed Packages > Installed Packages",
     "Lista dos pacotes instalados na org."),
    ("transaction-security", "src:help-tsp-condition-builder", "Build a Transaction Security Policy with Condition Builder",
     "sf.enhanced_transaction_security_condition_builder.htm", "Setup > Quick Find: Transaction Security > Transaction Security Policies > New",
     "Exige Customize Application e Modify Transaction Security Policy."),
    ("agentes-agentforce", "src:help-agentforce-enable", "Enable Agentforce", "ai.agent_setup_enable.htm",
     "Setup > Quick Find: Agent > Agentforce Agents", "Se a página não aparece, ligue antes o Einstein Generative AI."),
    ("workflow-rules-e-process-builder", "src:help-workflow-rules-manage", "Manage Automated Actions in Workflow Rules", "platform.managing_workflow_actions.htm",
     "Setup > Quick Find: Workflow Rules > Workflow Rules", "O suporte a Workflow Rules e Process Builder terminou em 31/12/2025; as regras existentes continuam rodando."),
    ("licencas-de-usuario", "src:help-feature-licenses-view", "View Your Organization's Feature Licenses", "platform.users_viewing_feature_licenses.htm",
     "Setup > Quick Find: Company Information > Company Information", "Listas relacionadas User Licenses, Feature Licenses e Permission Set Licenses."),
    ("devops-center", "src:help-devops-center-enable", "Enable and Install DevOps Center in the Org", "sf.devops_center_setup_install.htm",
     "Setup > Quick Find: DevOps Center > DevOps Center", "Não pode ser instalado em sandbox."),
    ("salesforce-files", "src:help-files-general-settings", "Salesforce Files", "sf.collaboration_admin_files.htm",
     "Setup > Quick Find: Salesforce Files > General Settings", "Onde fica a maioria das preferências de arquivos da org."),
    ("asset-files", "src:help-asset-files-edit", "View and Edit Asset Files", "sf.files_asset_files_edit_view.htm",
     "Setup > Quick Find: Asset Files > Asset Files", "Editar ou excluir exige Customize Application."),
]
p = caminho("fontes", "registro.json")
reg = json.load(open(p, encoding="utf-8"))
novas = [C.fonte(i, t + " (Salesforce Help)", H + a + "&language=en_US&type=5", n, EXTR, DATA, **AJ) for _, i, t, a, _c, n in LINHAS]
ids = {x["id"] for x in novas}
reg["fontes"] = [x for x in reg["fontes"] if x["id"] not in ids] + novas
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for fid, i, _t, _a, cam, nota in LINHAS:
    C.definir_setup(fid, cam, nota, [i])
print("lote 7q:", len(LINHAS), "caminhos")
