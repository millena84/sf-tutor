"""Acréscimos de conteúdo a temas que já têm texto (rodadas A3 e A4 em diante).

Diferente de conteudo_detalhe.py, que substitui o conteúdo do tema, aqui cada entrada só ACRESCENTA: itens de nível avançado
(sem repetir título), o texto de encadeamento (quando informado) e a lista "por onde começar" (quando informada).
Aplicado por conteudo_temas.py, por último.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ev  # noqa: E402


def E(*ids):
    return [ev(i) for i in ids]


def av(tipo, titulo, texto, evs):
    return {"tipo": tipo, "titulo": titulo, "texto": texto, "evidencias": evs}


UI, OBS = "cls:interface-e-experiencia-do-usuario", "cls:observabilidade-auditoria-e-operacao"
X = {}

# ------------------------------------------------------------------ Interface e experiência do usuário (A3)
X[UI] = {"comece": ["func:lightning-apps", "func:lightning-pages", "func:page-layouts"], "avancado": [
    av("decisao", "Page layout, compact layout ou Dynamic Forms", "Três recursos decidem o que aparece no registro. O page layout define "
       "seções, campos, botões e related lists. O compact layout define os campos do highlights panel, no topo. Com Dynamic Forms, os "
       "campos saem do page layout e viram componentes da Lightning page, com regras de visibilidade.",
       E("src:help-layouts-lex", "src:help-compact-layouts", "src:help-dynamic-forms")),
    av("implantacao", "Como metadado", "CustomApplication guarda cada app; Layout, cada page layout; CompactLayout, cada compact layout "
       "(dentro do objeto); FlexiPage, cada Lightning page; LightningExperienceTheme e BrandingSet, o tema e suas cores e imagens. O "
       "código de interface fica em LightningComponentBundle, AuraDefinitionBundle, ApexPage e ApexComponent.",
       E("src:mdapi-customapplication", "src:mdapi-layout", "src:mdapi-compactlayout", "src:mdapi-flexipage", "src:mdapi-lightningexperiencetheme",
         "src:mdapi-brandingset", "src:mdapi-lightningcomponentbundle")),
    av("atencao", "A mudança não aparece na hora", "Mudanças em page layouts, compact layouts e Lightning pages levam cerca de 15 minutos "
       "para aparecer no Lightning Experience ao recarregar a página; para outros usuários, até uma hora.", E("src:help-layout-considerations")),
    av("atencao", "Recuperar puxa perfis e permission sets", "Ao recuperar um app ou um page layout pela Metadata API, ele passa a aparecer "
       "também nos componentes Profile e PermissionSet recuperados no mesmo pacote.", E("src:mdapi-customapplication", "src:mdapi-layout")),
]}
X["sub:aplicativos-e-navegacao"] = {"comece": ["func:lightning-apps", "func:tabs"], "avancado": [
    av("implantacao", "O que se escolhe ao criar um app", "No App Manager, o assistente pede o nome e a marca, o tipo de navegação (padrão "
       "ou console), os form factors em que o app aparece, a utility bar, os itens de navegação e os perfis que o veem.",
       E("src:help-lightning-apps-create", "src:help-app-builder-apps")),
    av("atencao", "O que não muda depois", "No metadado do app, o tipo de navegação (navType) e o tipo de interface (uiType) não podem ser "
       "alterados depois da criação.", E("src:mdapi-customapplication")),
    av("atencao", "Utility bar invisível", "Itens de utilitário de segundo plano não aparecem na barra. Se a utility bar só tem itens de "
       "segundo plano, ela não aparece no app.", E("src:help-utility-bar")),
    av("implantacao", "Como metadado", "Cada app é um CustomApplication, na pasta applications, com sufixo .app. Guarda as abas, a marca, as "
       "substituições de página por perfil e, em apps de console do Classic, as opções de abas e atalhos. Apps padrão usam o prefixo "
       "standard__ no package.xml.", E("src:mdapi-customapplication")),
]}
X["sub:layouts-e-paginas-de-registro"] = {"comece": ["func:page-layouts", "func:compact-layouts", "func:dynamic-forms"], "avancado": [
    av("decisao", "Quem controla cada parte da página", "No Lightning Experience, o highlights panel é a única parte da página de registro "
       "que o page layout editor não configura: os campos dele vêm do compact layout, e as ações, de uma seção do page layout. Os dois "
       "layouts são independentes: tirar um campo de um não o tira do outro.", E("src:help-layouts-lex", "src:help-layout-considerations",
                                                                              "src:help-lightning-std-components")),
    av("limite", "Compact layout", "Até 10 campos; o highlights panel do Lightning Experience usa os sete primeiros, e o app móvel, até dez. "
       "Cada record type tem um só compact layout, e ele não é atribuído a perfis nem a usuários. Não aceita campos de texto longo nem "
       "multi-select picklist.", E("src:help-compact-layout-notes", "src:help-compact-layout-create", "src:mdapi-compactlayout")),
    av("decisao", "Quando usar Dynamic Forms", "Com Dynamic Forms, campos e seções viram componentes da Lightning page, distribuídos em "
       "colunas e abas e mostrados por regras de visibilidade. Nessas páginas, os campos de criar, editar e clonar vêm da página, não do "
       "page layout. Há limite de 100 campos por região, e o Dynamic Highlights Panel aceita até 12 campos.",
       E("src:help-dynamic-forms", "src:help-lightning-std-components", "src:help-rn-dynamic-highlights")),
    av("implantacao", "Como metadado", "Layout guarda o page layout: seções (LayoutSection), itens (LayoutItem, com o comportamento Edit, "
       "Required ou Readonly), quick actions e related lists. CompactLayout fica dentro do arquivo do objeto. As páginas com Dynamic "
       "Forms são componentes FlexiPage.", E("src:mdapi-layout", "src:mdapi-compactlayout", "src:mdapi-flexipage")),
]}
X["sub:lightning-pages-e-componentes"] = {"avancado": [
    av("implantacao", "Componentes customizados como metadado", "Componentes customizados de página vêm de Lightning web components "
       "(LightningComponentBundle) ou de Aura components (AuraDefinitionBundle). No LWC, é o arquivo de configuração que diz em que "
       "tipos de página o componente pode ser usado.", E("src:mdapi-lightningcomponentbundle", "src:mdapi-auradefinitionbundle", "src:lwc-config-file")),
]}
X["sub:acessibilidade-e-personalizacao"] = {"comece": ["func:temas-e-branding"], "avancado": [
    av("implantacao", "Tema da org", "Um tema é o conjunto de estilos visuais da interface. A org usa um tema pronto ou um customizado, "
       "criado em Themes and Branding, no Setup. Os temas se baseiam no Salesforce Lightning Design System; ativar um tema SLDS 2 liga o "
       "SLDS 2 para a org.", E("src:help-themes", "src:help-rn-dark-mode")),
    av("decisao", "O que cada usuário ajusta", "Cada pessoa escolhe a densidade da tela: Comfy, com rótulos acima dos campos e mais espaço, "
       "ou Compact, com rótulos à esquerda e menos espaço. Se o administrador ligou o dark mode, escolhe também tema claro ou escuro.",
       E("src:help-personalize-display")),
    av("atencao", "Dark mode", "O dark mode vale para temas SLDS 2, está em Beta e depende da edição. No metadado do tema, o campo é "
       "isDarkModeEnabled, disponível a partir da API 65.0.", E("src:help-rn-dark-mode", "src:mdapi-lightningexperiencetheme")),
    av("implantacao", "Como metadado", "LightningExperienceTheme guarda o tema e aponta para um BrandingSet, que guarda as cores e imagens "
       "como pares de nome e valor. Implantar o tema não o ativa: a ativação fica em outro tipo, LightningExperienceSettings, não "
       "cadastrado. Cada app pode usar a própria cor e o próprio logo no lugar do tema.",
       E("src:mdapi-lightningexperiencetheme", "src:mdapi-brandingset", "src:mdapi-customapplication")),
]}

# ------------------------------------------------------------------ Observabilidade, auditoria e operação (A4)
X[OBS] = {"comece": ["func:setup-audit-trail", "func:debug-logs", "func:event-monitoring"], "avancado": [
    av("decisao", "Qual registro responde a qual pergunta", "O que o código fez numa requisição: log de depuração. Quem mudou uma "
       "configuração: Setup Audit Trail. Quem entrou e de onde: histórico de login. Como a org é usada e com que desempenho: Event "
       "Monitoring. O que rodou em segundo plano: Apex Jobs.",
       E("src:help-debug-logs", "src:help-setup-audit-trail", "src:help-event-monitoring", "src:help-apex-job-queue")),
    av("limite", "Por quanto tempo cada coisa fica", "Logs de depuração do sistema: 24 horas. Setup Audit Trail: 180 dias. Arquivos de log "
       "de eventos: 1 dia sem o add-on; com ele, 30 dias por padrão, até 1 ano. Apex Jobs: a tela lista sete dias.",
       E("src:apex-debug-log", "src:help-setup-audit-trail", "src:help-kb-em-faq", "src:help-apex-job-queue")),
    av("implantacao", "É dado, não metadado", "Quase nada deste tema é configuração implantável: logs, auditoria e eventos são registros, "
       "consultados por tela ou por API. Os objetos cadastrados aqui são SetupAuditTrail, EventLogFile, LoginHistory e AsyncApexJob.",
       E("src:objref-setupaudittrail", "src:objref-eventlogfile", "src:objref-asyncapexjob")),
    av("seguranca", "Quem pode ver", "Setup Audit Trail exige View Setup and Configuration. Logs de depuração exigem View All Data. "
       "EventLogFile exige View Event Log Files e API Enabled.", E("src:help-setup-audit-trail", "src:help-debug-setup", "src:objref-eventlogfile")),
]}
X["sub:logs-e-rastreamento"] = {"comece": ["func:debug-logs"], "avancado": [
    av("implantacao", "Quando um log é gerado", "Um log de depuração nasce quando há uma trace flag de usuário ativa, quando se rodam testes "
       "Apex ou quando a requisição traz parâmetros ou cabeçalhos de depuração. Trace flags de classe e de trigger só mudam o nível de "
       "detalhe.", E("src:help-debug-logs", "src:apex-debug-log")),
    av("limite", "Tamanho e retenção", "Cada log tem até 20 MB; ao chegar ao limite, entradas antigas são apagadas e as mais novas ficam. "
       "Logs de depuração do sistema ficam 24 horas. O armazenamento padrão de logs é de 1.000 MB.",
       E("src:apex-debug-log", "src:help-debug-logs", "src:help-kb-traceflags-prod")),
    av("escala", "Nível de log", "O nível de log define quanta informação é guardada. Reduzir o nível reduz o tamanho do log e facilita a "
       "leitura; em produção, evite trace flags em usuários de API e em código de alto volume.",
       E("src:help-devconsole-logs", "src:help-kb-traceflags-prod")),
    av("seguranca", "Permissão", "Ver, guardar e apagar logs de depuração exige View All Data.", E("src:help-debug-setup")),
]}
X["sub:auditoria-de-configuracao"] = {"comece": ["func:setup-audit-trail"], "avancado": [
    av("limite", "O que a tela guarda", "A tela View Setup Audit Trail mostra as 20 mudanças mais recentes; o botão Download baixa o "
       "histórico dos últimos 180 dias. Depois disso, os registros são apagados: para guardar mais, é preciso exportar com regularidade.",
       E("src:help-setup-audit-trail", "src:objref-setupaudittrail")),
    av("atencao", "O que fica de fora", "Mudanças de permissões de usuário feitas por change set não são registradas no Setup Audit Trail. "
       "Mudanças em valores de campos de registros são outro recurso, o Field History Tracking.",
       E("src:help-kb-audit-changesets", "src:help-security-audit")),
    av("implantacao", "Por API", "O objeto SetupAuditTrail traz a categoria da mudança (Action), a seção do Setup (Section), a descrição "
       "completa (Display) e, quando houve Login-As, o usuário delegado (DelegateUser). Não aceita consultas agregadas.",
       E("src:objref-setupaudittrail")),
]}
X["sub:eventos-de-monitoramento"] = {"comece": ["func:event-monitoring"], "avancado": [
    av("decisao", "Arquivos de log ou eventos em tempo real", "Event Monitoring guarda logs de ocorrência, erro e desempenho em arquivos, "
       "no objeto EventLogFile. Real-Time Event Monitoring publica eventos de acesso e de segurança no momento em que acontecem, fora do "
       "EventLogFile.", E("src:help-kb-rtem-faq", "src:help-event-monitoring")),
    av("limite", "Licença e retenção", "O conjunto completo exige Salesforce Shield ou o add-on Event Monitoring. Sem o add-on, os tipos de "
       "evento são limitados e os arquivos ficam 1 dia; com ele, 30 dias por padrão, extensíveis a 1 ano.",
       E("src:help-em-enable", "src:help-kb-em-faq")),
    av("implantacao", "Como baixar", "Pelo Setup, o Event Log File Browser lista os arquivos por período e baixa em CSV. Por API, consulta-se "
       "EventLogFile: cada registro é um arquivo de um tipo de evento, com a lista dos campos do log.",
       E("src:help-rn-elf-browser", "src:objref-eventlogfile")),
    av("atencao", "O esquema muda", "O esquema de cada tipo de log pode mudar a cada release. Quem processa os arquivos deve conferir os "
       "campos LogFileFieldNames e LogFileFieldTypes depois de cada atualização.", E("src:objref-eventlogfile")),
]}
X["sub:jobs-incidentes-e-diagnostico"] = {"comece": ["func:monitoramento-de-jobs-apex"], "avancado": [
    av("implantacao", "Onde olhar os jobs", "A página Apex Jobs lista os jobs Apex dos últimos sete dias e o uso do limite de 24 horas; "
       "Apex Flex Queue mostra os batches em espera; Scheduled Jobs, os agendados. Por API, os mesmos dados estão em AsyncApexJob, "
       "CronTrigger e CronJobDetail.", E("src:help-apex-job-queue", "src:objref-asyncapexjob")),
    av("decisao", "Roteiro de investigação", "Para um erro numa execução: veja o job e o primeiro erro em AsyncApexJob; ligue uma trace "
       "flag e reproduza para obter o log de depuração; confira no Setup Audit Trail se alguma configuração mudou perto do horário.",
       E("src:objref-asyncapexjob", "src:help-debug-logs", "src:help-setup-audit-trail")),
]}
X["sub:limites-e-consumo"] = {"avancado": [
    av("limite", "Limites de Apex assíncrono", "O painel de saúde da org no Setup acompanha o limite de 24 horas de jobs assíncronos e o "
       "limite de jobs agendados; acima deles, jobs novos são rejeitados. Pela REST API, o recurso de limites traz o rótulo "
       "DailyAsyncApexExecutions.", E("src:help-org-health", "src:rest-limits")),
]}

# ------------------------------------------------------------------ Conteúdo, conhecimento e colaboração (A5)
CON, IA = "cls:conteudo-conhecimento-e-colaboracao", "cls:ia-agentes-e-decisoes-assistidas"
X[CON] = {"comece": ["func:salesforce-files", "func:chatter", "func:email-templates"], "avancado": [
    av("implantacao", "Como metadado", "EmailTemplate guarda cada email template; Letterhead, o letterhead do Classic; Document, os documentos "
       "da aba Documents; ContentAsset, cada asset file; ChatterSettings e KnowledgeSettings, as opções do Chatter e do Knowledge. Os arquivos "
       "do Salesforce Files são registros (ContentDocument e ContentVersion), não metadado.",
       E("src:mdapi-emailtemplate", "src:mdapi-letterhead", "src:mdapi-document", "src:mdapi-contentasset", "src:mdapi-chattersettings",
         "src:mdapi-knowledgesettings", "src:help-kb-files-data-model")),
    av("atencao", "Sem curinga no package.xml", "EmailTemplate, Letterhead e Document não aceitam o curinga (*): cada componente precisa ser "
       "listado pelo nome, e templates e documentos levam a pasta no nome.",
       E("src:mdapi-emailtemplate", "src:mdapi-letterhead", "src:mdapi-document")),
]}
X["sub:files-e-documentos"] = {"comece": ["func:salesforce-files"], "avancado": [
    av("limite", "Limites de publicação", "Até 30.000.000 de documentos publicados, contando os arquivados, e até 200.000 novas versões a cada "
       "24 horas (2.500 em Developer Edition e em trials).", E("src:objref-contentdocument-nota")),
    av("atencao", "Consulta sem ID não traz tudo", "Consultar ContentDocument ou ContentVersion sem informar um ID não devolve todos os arquivos "
       "que o usuário pode ver: ficam de fora os que ele só acessa por ter acesso a um registro com o qual o arquivo é compartilhado.",
       E("src:objref-contentversion-nota")),
    av("decisao", "Files não é Documents", "A aba Documents, do Salesforce Classic, é outro recurso: guarda documentos em pastas e tem o metadata "
       "type Document. É dela que saem, por exemplo, as imagens de logo dos Classic letterheads.", E("src:mdapi-document", "src:mdapi-letterhead")),
]}
X["sub:bibliotecas-e-assets"] = {"comece": ["func:asset-files", "func:static-resources"], "avancado": [
    av("decisao", "Asset file ou static resource", "Asset files são versões empacotáveis de arquivos do Salesforce Files, para marca e design: "
       "logos, cabeçalhos e arquivos referenciados por componentes. A Ajuda os apresenta como alternativa a static resources para deixar "
       "arquivos públicos. Para o uso comum e colaborativo de arquivos, não é preciso criar asset files.",
       E("src:help-asset-files", "src:help-kb-files-public")),
    av("implantacao", "Como metadado", "Cada asset file é um ContentAsset, na pasta contentassets, com sufixo .asset. O metadado guarda o rótulo, "
       "o idioma, as versões e com quem o arquivo é compartilhado. A recuperação falha se o conteúdo total passar de 30 MB.",
       E("src:mdapi-contentasset")),
]}
X["sub:colaboracao"] = {"comece": ["func:chatter"], "avancado": [
    av("limite", "Quantos grupos", "Cada usuário participa de até 300 grupos; a org pode ter até 30.000.", E("src:help-chatter-groups")),
    av("decisao", "Broadcast group", "Qualquer grupo (público, privado ou unlisted) pode ser posto em modo broadcast: só donos e gerentes "
       "publicam; os membros leem e comentam.", E("src:help-chatter-broadcast")),
    av("implantacao", "Como metadado", "As opções do Chatter ficam em ChatterSettings (arquivo Chatter.settings): ligar o Chatter, grupos "
       "unlisted, registros em grupos, edição e fixação de posts, rascunhos e prévias de links. O metadata type Group é outra coisa: "
       "representa public groups, usados em compartilhamento.", E("src:mdapi-chattersettings")),
]}
X["sub:templates-e-comunicacao"] = {"comece": ["func:email-templates"], "avancado": [
    av("implantacao", "Como metadado", "Cada template é um EmailTemplate, numa subpasta da pasta email: um arquivo .email com o corpo e um "
       "arquivo de metadado. O campo type diz o tipo (text, html, custom ou visualforce) e UiType, a interface (Aloha para o Classic, SFX para "
       "o Lightning Experience). O letterhead do Classic é o tipo Letterhead.", E("src:mdapi-emailtemplate", "src:mdapi-letterhead")),
    av("atencao", "Dois letterheads diferentes", "Classic letterheads valem para templates HTML do Classic e são geridos em Classic Letterheads, "
       "no Setup. Enhanced letterheads são do Lightning Experience, públicos por padrão, e exigem Modify All Data para criar.",
       E("src:help-classic-letterheads", "src:help-enhanced-letterheads")),
    av("atencao", "Templates do Classic no Lightning", "Os templates do Classic podem ser usados no Lightning Experience, mas são editados no "
       "Setup, em Classic Email Templates. Ao enviar, os anexos do template são somente leitura.",
       E("src:help-classic-templates-in-lex", "src:help-classic-html-templates")),
]}

# ------------------------------------------------------------------ IA, agentes e decisões assistidas (A6)
X[IA] = {"comece": ["func:agentes-agentforce", "func:subagents-e-agent-actions", "func:prompt-builder"], "avancado": [
    av("decisao", "Como as peças se encaixam", "O agente é formado por subagents (antes topics); cada subagent tem instruções e ações; uma ação "
       "chama um recurso da plataforma, como um flow, uma classe Apex ou um prompt template. O prompt template recebe dados da org por "
       "grounding, e uma data library permite buscar trechos de conteúdo da empresa. O Einstein Trust Layer protege os dados no caminho até o "
       "modelo.", E("src:help-agentforce-glossary", "src:help-prompt-concepts", "src:help-data-library", "src:help-trust-layer")),
    av("implantacao", "Como metadado", "GenAiPromptTemplate guarda cada prompt template; GenAiPlugin, cada tópico (subagent) da biblioteca de "
       "assets; GenAiFunction, cada agent action; EinsteinGptSettings, as opções de IA generativa da org. As páginas dos tipos avisam que, em "
       "orgs Winter '26 ou posteriores, o que é criado dentro de um agente sai em GenAiPlannerBundle.",
       E("src:mdapi-genaiprompttemplate", "src:mdapi-genaiplugin", "src:mdapi-genaifunction", "src:mdapi-einsteingptsettings")),
]}
X["sub:configuracao-de-agentes"] = {"comece": ["func:agentes-agentforce"], "avancado": [
    av("seguranca", "O agente tem um usuário", "Agentes de atendimento operam como um agent user: um usuário com as permissões de que o agente "
       "precisa para acessar dados e executar ações.", E("src:help-agent-service-template")),
    av("decisao", "Dois construtores", "A Ajuda atual descreve o Agentforce Builder, que usa a linguagem Agent Script, e o Legacy Agentforce "
       "Builder, um espaço visual. Agent Script combina instruções em linguagem natural com expressões programáticas, como condições e variáveis.",
       E("src:help-agent-script", "src:help-agentforce-builder-legacy")),
]}
X["sub:acoes-e-topicos"] = {"comece": ["func:subagents-e-agent-actions"], "avancado": [
    av("implantacao", "Como metadado", "GenAiPlugin guarda o tópico: rótulo, escopo, instruções e a lista de ações, citadas pelo nome de API. "
       "GenAiFunction guarda a ação: o alvo invocado (invocationTarget) e o tipo dele (invocationTargetType), como flow, apex ou "
       "generatePromptResponse. A ação pode trazer pastas input e output, com um schema.json que descreve os parâmetros.",
       E("src:mdapi-genaiplugin", "src:mdapi-genaifunction")),
    av("atencao", "Onde criar uma ação", "As ações da org ficam em Agentforce Assets, no Setup. Ao criar uma, escolhe-se o tipo de recurso que "
       "ela chama (Reference Action Type), como um flow ou um prompt template.", E("src:help-agent-action-custom")),
]}
X["sub:prompts"] = {"comece": ["func:prompt-builder"], "avancado": [
    av("decisao", "Tipo do template", "O tipo é escolhido ao criar o template. Field Generation gera conteúdo para um campo de registro, "
       "acionado por um botão; Flex serve para casos que os outros tipos não cobrem. A Ajuda traz a tabela completa de tipos.",
       E("src:help-prompt-template-types", "src:help-prompt-flex", "src:help-prompt-field-gen")),
    av("implantacao", "Como metadado", "Cada prompt template é um GenAiPromptTemplate, com uma lista de versões. Cada versão tem o texto, as "
       "entradas, os provedores de dados (por exemplo, um flow) e o estado: Draft ou Published. activeVersionIdentifier aponta a versão ativa.",
       E("src:mdapi-genaiprompttemplate")),
    av("atencao", "Publicado não se edita", "Um template publicado não pode ser editado, nem pela interface nem pela Metadata API. Em "
       "EinsteinGptSettings, uma opção faz a implantação levar só as versões ativas; nesse caso, ela falha se não houver versão ativa.",
       E("src:mdapi-genaiprompttemplate", "src:mdapi-einsteingptsettings")),
]}
X["sub:modelos-e-grounding"] = {"comece": ["func:prompt-builder", "func:agentforce-data-library"], "avancado": [
    av("decisao", "Duas formas de grounding", "Grounding é acrescentar ao prompt os dados de que o modelo precisa. No Prompt Builder, isso é "
       "feito por merge fields que referenciam campos de registro, flows, Apex e arquivos. Com RAG, um retriever busca trechos relevantes em "
       "conteúdo indexado no Data 360.", E("src:help-prompt-concepts", "src:help-prompt-rag", "src:help-agentforce-glossary")),
    av("implantacao", "Provedores de modelo como metadado", "EinsteinGptSettings tem opções para desligar provedores de modelo (AWS Bedrock, "
       "Azure OpenAI, OpenAI e Vertex AI) e para ligar modelos em beta. Em cada versão de prompt template, primaryModel aponta o modelo usado.",
       E("src:mdapi-einsteingptsettings", "src:mdapi-genaiprompttemplate")),
]}
X["sub:recuperacao-de-conhecimento"] = {"comece": ["func:agentforce-data-library", "func:lightning-knowledge"]}
X["sub:seguranca-avaliacao-e-governanca-de-ia"] = {"comece": ["func:einstein-trust-layer"], "avancado": [
    av("seguranca", "O que o Trust Layer faz", "Retenção zero: os provedores externos de modelo não guardam os dados nem os usam em treinamento. "
       "Mascaramento: dados sensíveis são identificados e trocados por marcadores antes do envio ao modelo. Detecção de toxicidade: respostas "
       "potencialmente nocivas são sinalizadas. Auditoria: prompts, respostas e sinais de confiança ficam registrados.",
       E("src:help-trust-layer", "src:help-trust-masking", "src:help-employee-agent-considerations")),
    av("atencao", "Mascaramento tem exceções", "No Agentforce Employee Agent, o mascaramento fica desligado. Quando o modelo é hospedado dentro "
       "do limite de confiança da Salesforce, os dados não saem desse limite.",
       E("src:help-employee-agent-considerations", "src:help-agent-masking-limits")),
    av("seguranca", "Onde fica a auditoria", "Os dados de auditoria de IA generativa (como o mascaramento aplicado e as pontuações de "
       "toxicidade) e os dados de feedback ficam guardados no Data 360.", E("src:help-trust-audit")),
    av("seguranca", "Permissões continuam valendo", "Agentes respeitam os controles de acesso padrão do Salesforce.", E("src:help-agentforce-trust")),
]}

EXTRAS = X
