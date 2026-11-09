# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Bootstrap (uso único, fora do repositório): helpers e taxonomia.
import json, os, re, unicodedata
ROOT = "/home/claude/sf-tutor/ai-help/claude/insumos-grafo/catalogo"

def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def save(sub, name, obj):
    p = os.path.join(ROOT, sub, name + ".json") if sub else os.path.join(ROOT, name + ".json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")

def ev(src, nota=None, secao=None):
    e = {"fonte": src}
    if secao: e["secao"] = secao
    if nota: e["nota"] = nota
    return e

def af(estado, valor=None, nota=None, evs=None):
    a = {"estado": estado}
    if valor is not None: a["valor"] = valor
    if nota: a["nota"] = nota
    if evs: a["evidencias"] = evs
    return a

# ---------------- Taxonomia (curadoria didática da especificação) ----------------
CLS = [
 ("organizacao-e-configuracoes-base","Organização e configurações base","Org e configurações","ORG",
  "Reúne o que define a org como um todo antes de qualquer processo de negócio: identidade, configurações gerais, idiomas, moedas, calendário, domínios e habilitação de recursos.",
  [("identificacao-e-configuracao-da-org","Identificação e configuração da org","Dados cadastrais e parâmetros gerais que identificam a org."),
   ("settings","Settings","Família de tipos de configuração da org (nomes terminados em Settings), cada um com seu próprio metadata type."),
   ("parametros-reutilizaveis","Parâmetros reutilizáveis","Valores configuráveis reaproveitados por várias funcionalidades, como metadados e configurações personalizadas."),
   ("localizacao-idiomas-e-traducao","Localização, idiomas e tradução","Idiomas habilitados, formatos regionais e traduções da interface e de metadados."),
   ("moedas-e-calendario-fiscal","Moedas e calendário fiscal","Moedas da org, taxas de conversão e definição do ano fiscal."),
   ("horarios-comerciais-e-feriados","Horários comerciais e feriados","Janelas de atendimento e feriados usados por regras e prazos."),
   ("dominios-e-urls","Domínios e URLs","Domínio da org e endereços pelos quais usuários e integrações acessam a plataforma."),
   ("habilitacao-de-recursos","Habilitação de recursos","Ativação de recursos opcionais que mudam o comportamento da org.")]),
 ("acesso-identidade-e-seguranca","Acesso, identidade e segurança","Acesso e segurança","ACS",
  "Reúne quem pode entrar na org, como se autentica e o que cada pessoa ou integração pode ver e fazer.",
  [("usuarios-e-provisionamento","Usuários e provisionamento","Criação, ativação, desativação e manutenção de usuários."),
   ("autenticacao-sso-e-mfa","Autenticação, SSO e MFA","Como a identidade é comprovada: senha, login único e múltiplos fatores."),
   ("sessoes-e-politicas-de-login","Sessões e políticas de login","Regras de sessão, restrições de login e estado de acesso dos usuários."),
   ("permissoes-perfis-e-grupos","Permissões, perfis e grupos","O que um usuário pode fazer: perfis, permission sets e grupos de permission sets."),
   ("licencas-e-entitlements-de-acesso","Licenças e entitlements de acesso","Licenças de usuário e de permission set que limitam o acesso a recursos."),
   ("acesso-a-registros-e-hierarquias","Acesso a registros e hierarquias","Quais registros cada usuário enxerga: padrões da org, papéis e compartilhamento."),
   ("credenciais-certificados-e-protecao-de-dados","Credenciais, certificados e proteção de dados","Segredos, certificados e criptografia usados para proteger dados e integrações.")]),
 ("dados-e-modelagem","Dados e modelagem","Dados e modelagem","DAD",
  "Reúne a estrutura onde os dados vivem: objetos, campos, relacionamentos, tipos de registro e listas de valores.",
  [("objetos-e-entidades","Objetos e entidades","Objetos padrão e customizados que guardam os registros."),
   ("campos-e-tipos","Campos e tipos","Campos de cada objeto, seus tipos de dado e regras de formato."),
   ("relacionamentos-e-juncoes","Relacionamentos e junções","Ligações entre objetos, inclusive objetos de junção para relações muitos-para-muitos."),
   ("tipos-de-registro-e-processos-de-negocio","Tipos de registro e processos de negócio","Variações de um objeto com valores e processos próprios."),
   ("listas-de-valores","Listas de valores","Picklists e conjuntos de valores reutilizáveis."),
   ("metadados-de-configuracao-de-dados","Metadados de configuração de dados","Configurações que descrevem comportamento dos dados, como índices e históricos."),
   ("modelos-externos-e-especializacoes","Modelos externos e especializações","Objetos externos, big objects e outras especializações do modelo de dados.")]),
 ("qualidade-governanca-e-ciclo-de-vida-dos-dados","Qualidade, governança e ciclo de vida dos dados","Qualidade e governança","QLD",
  "Reúne mecanismos que protegem a qualidade dos dados e controlam sua classificação, retenção e privacidade.",
  [("validacao","Validação","Regras que impedem gravar dados inválidos."),
   ("duplicidade-e-correspondencia","Duplicidade e correspondência","Detecção e tratamento de registros duplicados."),
   ("classificacao-e-sensibilidade","Classificação e sensibilidade","Marcação de dados por sensibilidade e conformidade."),
   ("retencao-arquivamento-e-exclusao","Retenção, arquivamento e exclusão","Quanto tempo os dados ficam e como são arquivados ou removidos."),
   ("rastreabilidade-e-historico","Rastreabilidade e histórico","Histórico de alterações de campos e registros."),
   ("consentimento-e-privacidade","Consentimento e privacidade","Registro de consentimento e atendimento a requisitos de privacidade.")]),
 ("automacao-de-processos-e-regras-de-negocio","Automação de processos e regras de negócio","Automação","AUT",
  "Reúne o que executa trabalho automaticamente: fluxos, decisões, aprovações, ações e código Apex.",
  [("flow-e-orquestracao","Flow e orquestração","Fluxos declarativos e orquestrações de várias etapas."),
   ("decisoes-e-aprovacoes","Decisões e aprovações","Processos de aprovação e pontos de decisão."),
   ("acoes-e-regras","Ações e regras","Ações reutilizáveis e regras que disparam comportamento."),
   ("automacao-apex","Automação Apex","Triggers e classes Apex que automatizam processos."),
   ("notificacoes","Notificações","Alertas e notificações enviados por automações."),
   ("mecanismos-legados-e-migracao","Mecanismos legados e migração","Ferramentas antigas de automação e caminhos de migração.")]),
 ("interface-e-experiencia-do-usuario","Interface e experiência do usuário","Interface (UX)","UIX",
  "Reúne o que a pessoa usuária vê e usa: apps, navegação, páginas, ações e orientação visual.",
  [("aplicativos-e-navegacao","Aplicativos e navegação","Apps e itens de navegação."),
   ("tabs","Tabs","Entradas de navegação para objetos, páginas e componentes."),
   ("layouts-e-paginas-de-registro","Layouts e páginas de registro","Organização dos campos e seções na página de um registro."),
   ("lightning-pages-e-componentes","Lightning pages e componentes","Páginas montadas com componentes no Lightning App Builder."),
   ("acoes-rapidas","Ações rápidas","Botões que executam uma tarefa em contexto."),
   ("orientacao-visual-e-path","Orientação visual e Path","Recursos que guiam o usuário pelas etapas de um processo."),
   ("experiencias-web-portais-e-mobile","Experiências web/portais e mobile","Sites, portais e experiência em dispositivos móveis."),
   ("acessibilidade-e-personalizacao","Acessibilidade e personalização","Ajustes de interface por usuário, tema e acessibilidade.")]),
 ("execucao-assincrona-lotes-e-agendamento","Execução assíncrona, lotes e agendamento","Assíncrono e lotes","ASY",
  "Reúne o processamento que não acontece na hora do clique: lotes, filas, agendamentos e eventos.",
  [("batch","Batch","Processamento de grandes volumes em lotes."),
   ("queueable","Queueable","Tarefas enfileiradas para execução posterior."),
   ("future-e-mecanismos-legados","Future e mecanismos legados quando aplicáveis","Métodos assíncronos antigos e quando ainda se aplicam."),
   ("agendamento","Agendamento","Execução em horários definidos."),
   ("caminhos-assincronos","Caminhos assíncronos","Partes assíncronas de automações declarativas."),
   ("processamento-orientado-a-eventos","Processamento orientado a eventos","Reações a eventos publicados na plataforma."),
   ("monitoramento-de-jobs-e-limites","Monitoramento de jobs e limites","Acompanhamento de execuções assíncronas e seus limites.")]),
 ("integracao-apis-e-eventos","Integração, APIs e eventos","Integração e APIs","INT",
  "Reúne como sistemas externos conversam com a org: APIs, autenticação de integrações, chamadas externas e eventos.",
  [("apis-de-dados-e-metadados","APIs de dados e metadados","APIs para ler e gravar registros e metadados."),
   ("autenticacao-de-integracoes","Autenticação de integrações","Como sistemas externos se autenticam na org."),
   ("chamadas-externas-e-endpoints","Chamadas externas e endpoints","Chamadas da org para serviços externos e seus endereços."),
   ("credenciais","Credenciais","Credenciais nomeadas e externas usadas em integrações."),
   ("eventos-e-mensageria","Eventos e mensageria","Eventos de plataforma, captura de alterações e mensagens."),
   ("conectividade-e-virtualizacao-de-dados","Conectividade e virtualização de dados","Acesso a dados externos sem copiá-los para a org."),
   ("contratos-limites-e-tratamento-de-falhas","Contratos, limites e tratamento de falhas","Limites de API, versões e estratégias de erro.")]),
 ("relatorios-analytics-e-exploracao","Relatórios, analytics e exploração","Relatórios","REL",
  "Reúne como os dados são resumidos e explorados: relatórios, dashboards e tipos de relatório.",
  [("reports","Reports","Relatórios sobre os registros da org."),
   ("dashboards","Dashboards","Painéis visuais construídos sobre relatórios."),
   ("tipos-de-relatorio","Tipos de relatório","Definição de quais objetos e campos um relatório pode usar."),
   ("pastas-e-acesso","Pastas e acesso","Organização e compartilhamento de relatórios e dashboards."),
   ("metricas-e-agregacoes","Métricas e agregações","Cálculos de resumo e indicadores."),
   ("recursos-analiticos-de-produto","Recursos analíticos específicos de produto","Recursos analíticos que dependem de produto ou licença.")]),
 ("conteudo-conhecimento-e-colaboracao","Conteúdo, conhecimento e colaboração","Conteúdo","CON",
  "Reúne arquivos, bases de conhecimento, colaboração e modelos de comunicação.",
  [("files-e-documentos","Files e documentos","Arquivos anexados e documentos."),
   ("bibliotecas-e-assets","Bibliotecas e assets","Bibliotecas de conteúdo e recursos estáticos."),
   ("knowledge-e-categorias","Knowledge e categorias","Artigos de conhecimento e categorias de dados."),
   ("colaboracao","Colaboração","Feeds, grupos e recursos de colaboração."),
   ("templates-e-comunicacao","Templates e comunicação","Modelos de e-mail e de comunicação.")]),
 ("desenvolvimento-testes-e-entrega","Desenvolvimento, testes e entrega","Desenvolvimento","DEV",
  "Reúne como mudanças são construídas, testadas e levadas entre ambientes.",
  [("codigo-e-bundles","Código e bundles","Classes, componentes e pacotes de código."),
   ("testes","Testes","Testes automatizados e cobertura."),
   ("pacotes-e-dependencias","Pacotes e dependências","Empacotamento e dependências entre componentes."),
   ("source-format-e-metadata-api-format","Source format e Metadata API format","Os dois formatos de arquivo de metadados e suas diferenças."),
   ("ambientes-e-sandboxes","Ambientes e sandboxes","Orgs de desenvolvimento, teste e produção."),
   ("versionamento-deploy-e-recuperacao","Versionamento, deploy e recuperação","Versões de componentes, implantação e retorno.")]),
 ("observabilidade-auditoria-e-operacao","Observabilidade, auditoria e operação","Observabilidade","OBS",
  "Reúne como a operação da org é acompanhada: logs, auditoria, histórico de login, limites e diagnóstico.",
  [("logs-e-rastreamento","Logs e rastreamento","Logs de depuração e rastreamento de execução."),
   ("auditoria-de-configuracao","Auditoria de configuração","Registro de alterações feitas no Setup."),
   ("historico-de-login","Histórico de login","Tentativas de login e estado de acesso dos usuários."),
   ("eventos-de-monitoramento","Eventos de monitoramento","Eventos que registram uso e atividade."),
   ("limites-e-consumo","Limites e consumo","Uso de limites da plataforma."),
   ("jobs-incidentes-e-diagnostico","Jobs, incidentes e diagnóstico","Acompanhamento de jobs e investigação de problemas.")]),
 ("ia-agentes-e-decisoes-assistidas","IA, agentes e decisões assistidas","IA e agentes","IA",
  "Reúne configuração de agentes, prompts, modelos e governança de recursos de IA.",
  [("configuracao-de-agentes","Configuração de agentes","Definição de agentes e de seu comportamento."),
   ("acoes-e-topicos","Ações e tópicos","O que um agente pode fazer e sobre quais assuntos."),
   ("prompts","Prompts","Modelos de instrução usados por recursos de IA."),
   ("modelos-e-grounding","Modelos e grounding","Modelos usados e dados que fundamentam as respostas."),
   ("recuperacao-de-conhecimento","Recursos de recuperação de conhecimento","Busca de conteúdo para alimentar respostas."),
   ("seguranca-avaliacao-e-governanca-de-ia","Segurança, avaliação e governança de IA","Controles, testes e auditoria de IA.")]),
 ("processos-de-negocio-especificos-de-produto","Processos de negócio específicos de produto","Processos de produto","NEG",
  "Reúne capacidades próprias de um produto ou setor, que não fazem parte da plataforma compartilhada.",
  [("vendas","Vendas","Capacidades próprias de vendas."),
   ("atendimento","Atendimento","Capacidades próprias de atendimento."),
   ("servico-de-campo","Serviço de campo","Capacidades de serviço de campo."),
   ("receita-e-comercio","Receita e comércio","Capacidades de receita, cotação e comércio."),
   ("experiencias-externas","Experiências externas","Capacidades de sites e portais para públicos externos."),
   ("capacidades-setoriais","Capacidades setoriais","Capacidades de nuvens setoriais."),
   ("outras-areas","Outras áreas encontradas no inventário oficial","Áreas descobertas no inventário que ainda não têm agrupamento próprio.")]),
]

# Funcionalidades do piloto por subclassificação (preenchido em b3)
SUB_FUNCS = {}

def write_taxonomy():
    for cid, nome, curto, sigla, desc, subs in CLS:
        sub_ids = []
        for i, (sid, snome, sdesc) in enumerate(subs):
            full = "sub:" + sid
            sub_ids.append(full)
            save("subclassificacoes", sid, {
                "id": full, "nome": snome, "sigla": f"{sigla}-{i+1:02d}", "classificacao": "cls:" + cid,
                "natureza": "curadoria_didatica", "descricao": sdesc,
                "funcionalidades": sorted(SUB_FUNCS.get(full, [])),
                "estado": "desconhecido",
                "nota_estado": "Agrupamento proposto na especificação; fronteira ainda não cruzada com a documentação oficial." })
        save("classificacoes", cid, {
            "id": "cls:" + cid, "nome": nome, "nome_curto": curto, "sigla": sigla, "natureza": "curadoria_didatica",
            "descricao": desc, "subclassificacoes": sub_ids, "referencias_oficiais": [],
            "estado": "desconhecido",
            "nota_estado": "Classificação didática do projeto (00-especificacao-grafo.md), não nomenclatura oficial da Salesforce. Cruzamento com documentação oficial pendente." })
