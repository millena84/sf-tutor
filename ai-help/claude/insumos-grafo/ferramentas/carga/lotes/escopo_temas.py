"""Issue #34, fase 2: escopo (critério de inclusão) e fora_do_escopo de cada tema.

Os temas são curadoria didática do projeto (00-especificacao-grafo.md, seção "Classificação e
sub-classificação": "escopo do agrupamento" e "o que fica fora e onde procurar"). Os textos abaixo são
redação do projeto: delimitam o recorte e apontam o tema vizinho. Não afirmam fatos técnicos da Salesforce
além dos nomes já catalogados.

Reexecutável: grava só os dois campos, logo depois de "descricao", sem tocar no resto do cadastro.
Uso: python3 ferramentas/carga/lotes/escopo_temas.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from carga.base import ROOT, save  # noqa: E402

# id -> (escopo, fora_do_escopo)
TEXTOS = {
    # ------------------------------------------------------------------ Organização e configurações base
    "cls:organizacao-e-configuracoes-base": (
        "Entra o que vale para a org inteira e não pertence a um processo de negócio: dados da org, configurações gerais (Settings), parâmetros reaproveitados, idiomas, moedas, calendário fiscal, horários comerciais, domínios e ativação de recursos.",
        "Configuração de segurança e de acesso fica em \"Acesso, identidade e segurança\". Estrutura de dados (objetos e campos) fica em \"Dados e modelagem\". Configurações que só existem para um produto ficam em \"Processos de negócio específicos de produto\".",
    ),
    "sub:identificacao-e-configuracao-da-org": (
        "Entram os dados cadastrais e os parâmetros gerais que identificam a org como um todo.",
        "Domínio e endereços de acesso ficam em \"Domínios e URLs\". Ativação de recursos opcionais fica em \"Habilitação de recursos\".",
    ),
    "sub:settings": (
        "Entram os metadata types da família Settings (nomes terminados em Settings) quando o assunto principal deles é a configuração geral da org.",
        "Um Settings dedicado a um assunto com tema próprio (por exemplo, horário comercial ou Knowledge) é estudado nesse tema e só citado aqui.",
    ),
    "sub:parametros-reutilizaveis": (
        "Entram os mecanismos que guardam valores configuráveis para serem lidos por várias funcionalidades, como metadados e configurações personalizadas.",
        "A definição de objetos e campos comuns fica em \"Objetos e entidades\" e \"Campos e tipos\".",
    ),
    "sub:localizacao-idiomas-e-traducao": (
        "Entram idiomas habilitados, formatos regionais e tradução de rótulos da interface e de metadados.",
        "Moedas e conversão ficam em \"Moedas e calendário fiscal\".",
    ),
    "sub:moedas-e-calendario-fiscal": (
        "Entram as moedas da org, as taxas de conversão e a definição do ano fiscal.",
        "Previsões de vendas que usam o calendário fiscal ficam em \"Vendas\".",
    ),
    "sub:horarios-comerciais-e-feriados": (
        "Entram as janelas de funcionamento e os feriados que outras regras usam para calcular prazos.",
        "As regras que consomem esses horários (escalonamento, marcos de SLA) ficam em \"Ações e regras\" e \"Atendimento\".",
    ),
    "sub:dominios-e-urls": (
        "Entram o domínio da org e os endereços pelos quais pessoas e integrações chegam à plataforma.",
        "Endereços externos chamados pela org ficam em \"Chamadas externas e endpoints\".",
    ),
    "sub:habilitacao-de-recursos": (
        "Entram as ativações de recursos opcionais que mudam o comportamento da org depois de ligadas.",
        "Quando o recurso ativado tem tema próprio, o funcionamento dele é estudado nesse tema.",
    ),
    # ------------------------------------------------------------------ Acesso, identidade e segurança
    "cls:acesso-identidade-e-seguranca": (
        "Entra tudo que responde a três perguntas: quem pode entrar na org, como comprova quem é, e o que pode ver e fazer depois de entrar. Vale para pessoas e para integrações.",
        "Registro de tentativas de login como dado de auditoria fica também em \"Observabilidade, auditoria e operação\". Como uma integração se conecta (APIs, callouts) fica em \"Integração, APIs e eventos\".",
    ),
    "sub:usuarios-e-provisionamento": (
        "Entram a criação, a ativação, a desativação e a manutenção de usuários.",
        "O que o usuário pode fazer fica em \"Permissões, perfis e grupos\". Como ele se autentica fica em \"Autenticação, SSO e MFA\".",
    ),
    "sub:autenticacao-sso-e-mfa": (
        "Entram as formas de comprovar identidade: senha, login único, provedores de autenticação, múltiplos fatores e apps conectados usados no login.",
        "A autenticação de sistemas externos tratada como integração fica também em \"Autenticação de integrações\". Regras de sessão ficam em \"Sessões e políticas de login\".",
    ),
    "sub:sessoes-e-politicas-de-login": (
        "Entram as regras de sessão, as restrições de login e o estado de acesso dos usuários.",
        "O histórico de logins como trilha de auditoria fica em \"Histórico de login\".",
    ),
    "sub:permissoes-perfis-e-grupos": (
        "Entram os mecanismos que dizem o que um usuário pode fazer: perfis, permission sets e grupos de permission sets.",
        "Quais registros o usuário enxerga fica em \"Acesso a registros e hierarquias\". Limites impostos pela licença ficam em \"Licenças e entitlements de acesso\".",
    ),
    "sub:licencas-e-entitlements-de-acesso": (
        "Entram as licenças de usuário e de permission set que limitam quais recursos uma pessoa pode receber.",
        "Entitlements de atendimento (SLA de casos) são outro assunto e ficam em \"Atendimento\".",
    ),
    "sub:acesso-a-registros-e-hierarquias": (
        "Entram os mecanismos que decidem quais registros cada usuário enxerga: padrões da org, papéis, compartilhamento e equipes.",
        "Permissão sobre o objeto inteiro (ler, criar, editar) fica em \"Permissões, perfis e grupos\".",
    ),
    "sub:credenciais-certificados-e-protecao-de-dados": (
        "Entram segredos, certificados, chaves e criptografia usados para proteger dados e conexões.",
        "O uso de credenciais por integrações é estudado também em \"Credenciais\", no tema de integração.",
    ),
    # ------------------------------------------------------------------ Dados e modelagem
    "cls:dados-e-modelagem": (
        "Entra a estrutura onde os dados vivem: objetos, campos, relacionamentos, tipos de registro, listas de valores e especializações do modelo.",
        "Regras que protegem a qualidade e o ciclo de vida dos dados ficam em \"Qualidade, governança e ciclo de vida dos dados\". Como os campos aparecem na tela fica em \"Interface e experiência do usuário\".",
    ),
    "sub:objetos-e-entidades": (
        "Entram os objetos padrão e customizados que guardam registros.",
        "Objetos externos e outras especializações ficam em \"Modelos externos e especializações\".",
    ),
    "sub:campos-e-tipos": (
        "Entram os campos de cada objeto, seus tipos de dado e regras de formato.",
        "Campos que ligam objetos são estudados em \"Relacionamentos e junções\". Listas de opções ficam em \"Listas de valores\".",
    ),
    "sub:relacionamentos-e-juncoes": (
        "Entram as ligações entre objetos (lookup e mestre-detalhe) e os objetos de junção para relações muitos-para-muitos.",
        "Relações entre um metadata type e um objeto API, usadas pelo mapa, são explicadas em cada ficha de ligação, não neste tema.",
    ),
    "sub:tipos-de-registro-e-processos-de-negocio": (
        "Entram as variações de um mesmo objeto com valores, layouts e processos próprios.",
        "A página que cada tipo de registro mostra fica em \"Layouts e páginas de registro\".",
    ),
    "sub:listas-de-valores": (
        "Entram picklists e conjuntos de valores reaproveitáveis.",
        "O uso visual dos valores como etapas fica em \"Orientação visual e Path\".",
    ),
    "sub:metadados-de-configuracao-de-dados": (
        "Entram configurações que descrevem o comportamento dos dados sem ser um objeto ou campo em si.",
        "Histórico de alterações como requisito de rastreabilidade fica em \"Rastreabilidade e histórico\".",
    ),
    "sub:modelos-externos-e-especializacoes": (
        "Entram objetos externos, big objects e outras formas especiais de modelar dados.",
        "Como a org se conecta à fonte externa fica em \"Conectividade e virtualização de dados\".",
    ),
    # ------------------------------------------------------------------ Qualidade, governança e ciclo de vida dos dados
    "cls:qualidade-governanca-e-ciclo-de-vida-dos-dados": (
        "Entra o que protege a qualidade dos dados e controla sua classificação, retenção, histórico e privacidade.",
        "A estrutura dos dados fica em \"Dados e modelagem\". Quem pode ver os dados fica em \"Acesso, identidade e segurança\".",
    ),
    "sub:validacao": (
        "Entram as regras que impedem gravar dados inválidos.",
        "Regras que disparam ações (atribuição, escalonamento) ficam em \"Ações e regras\".",
    ),
    "sub:duplicidade-e-correspondencia": (
        "Entram a detecção e o tratamento de registros duplicados.",
        "Validação de formato de um campo fica em \"Validação\".",
    ),
    "sub:classificacao-e-sensibilidade": (
        "Entram as marcações de dados por sensibilidade e por requisito de conformidade.",
        "Criptografia e proteção técnica ficam em \"Credenciais, certificados e proteção de dados\".",
    ),
    "sub:retencao-arquivamento-e-exclusao": (
        "Entram o tempo de permanência dos dados e as formas de arquivá-los ou removê-los.",
        "Recuperação de metadados depois de um deploy fica em \"Versionamento, deploy e recuperação\".",
    ),
    "sub:rastreabilidade-e-historico": (
        "Entra o histórico de alterações de campos e de registros.",
        "O histórico de alterações de configuração no Setup fica em \"Auditoria de configuração\".",
    ),
    "sub:consentimento-e-privacidade": (
        "Entram o registro de consentimento e o atendimento a requisitos de privacidade sobre dados de pessoas.",
        "Classificação dos dados por sensibilidade fica em \"Classificação e sensibilidade\".",
    ),
    # ------------------------------------------------------------------ Automação
    "cls:automacao-de-processos-e-regras-de-negocio": (
        "Entra o que executa trabalho sem ação manual a cada passo: fluxos, decisões, aprovações, regras que disparam comportamento, automação em Apex e notificações.",
        "Execuções que acontecem depois, em fila ou em horário marcado, ficam em \"Execução assíncrona, lotes e agendamento\". Regras que só bloqueiam dado inválido ficam também em \"Validação\".",
    ),
    "sub:flow-e-orquestracao": (
        "Entram os fluxos declarativos e as orquestrações de várias etapas.",
        "Caminhos assíncronos de um fluxo ficam em \"Caminhos assíncronos\". Versões e implantação de fluxos ficam em \"Versionamento, deploy e recuperação\".",
    ),
    "sub:decisoes-e-aprovacoes": (
        "Entram os processos de aprovação e os pontos de decisão de um processo.",
        "Decisões assistidas por IA ficam em \"IA, agentes e decisões assistidas\".",
    ),
    "sub:acoes-e-regras": (
        "Entram ações reutilizáveis e regras que disparam comportamento, como atribuição e escalonamento.",
        "Ações rápidas vistas como botão da interface ficam também em \"Ações rápidas\".",
    ),
    "sub:automacao-apex": (
        "Entram triggers e classes Apex usados para automatizar processos.",
        "Apex assíncrono fica em \"Execução assíncrona, lotes e agendamento\". Código como artefato de entrega fica em \"Código e bundles\".",
    ),
    "sub:notificacoes": (
        "Entram alertas e notificações enviados por automações.",
        "Modelos de e-mail usados nas notificações ficam em \"Templates e comunicação\".",
    ),
    "sub:mecanismos-legados-e-migracao": (
        "Entram ferramentas antigas de automação e os caminhos de migração para as atuais.",
        "Mecanismos assíncronos antigos ficam em \"Future e mecanismos legados quando aplicáveis\".",
    ),
    # ------------------------------------------------------------------ Interface
    "cls:interface-e-experiencia-do-usuario": (
        "Entra o que a pessoa usuária vê e usa: apps, navegação, tabs, páginas de registro, componentes, ações, orientação visual e experiências externas e móveis.",
        "A estrutura de dados por trás da tela fica em \"Dados e modelagem\". Quem pode ver cada item fica em \"Acesso, identidade e segurança\".",
    ),
    "sub:aplicativos-e-navegacao": (
        "Entram os apps e os itens de navegação que agrupam o trabalho da pessoa usuária.",
        "Cada entrada de navegação, vista isoladamente, fica em \"Tabs\".",
    ),
    "sub:tabs": (
        "Entram as entradas de navegação para objetos, páginas e componentes.",
        "O app que reúne as tabs fica em \"Aplicativos e navegação\".",
    ),
    "sub:layouts-e-paginas-de-registro": (
        "Entra a organização de campos, seções e componentes na página de um registro.",
        "A montagem de páginas com componentes no Lightning App Builder fica em \"Lightning pages e componentes\".",
    ),
    "sub:lightning-pages-e-componentes": (
        "Entram as páginas montadas com componentes no Lightning App Builder.",
        "O código dos componentes como artefato de entrega fica em \"Código e bundles\".",
    ),
    "sub:acoes-rapidas": (
        "Entram os botões que executam uma tarefa no contexto de um registro ou da página.",
        "A lógica executada por trás da ação fica em \"Automação de processos e regras de negócio\".",
    ),
    "sub:orientacao-visual-e-path": (
        "Entram os recursos que guiam a pessoa pelas etapas de um processo na tela.",
        "Os valores que definem as etapas ficam em \"Listas de valores\".",
    ),
    "sub:experiencias-web-portais-e-mobile": (
        "Entram sites, portais e a experiência em dispositivos móveis, vistos como interface.",
        "Capacidades de produto para públicos externos ficam em \"Experiências externas\".",
    ),
    "sub:acessibilidade-e-personalizacao": (
        "Entram ajustes de interface por usuário, temas visuais e acessibilidade.",
        "Idioma e formato regional ficam em \"Localização, idiomas e tradução\".",
    ),
    # ------------------------------------------------------------------ Execução assíncrona
    "cls:execucao-assincrona-lotes-e-agendamento": (
        "Entra o processamento que não acontece no momento da ação da pessoa usuária: lotes, filas, agendamentos, reações a eventos e o acompanhamento dessas execuções.",
        "A publicação e o transporte de eventos entre sistemas ficam em \"Eventos e mensageria\". Automações síncronas ficam em \"Automação de processos e regras de negócio\".",
    ),
    "sub:batch": (
        "Entra o processamento de grandes volumes dividido em lotes.",
        "Carga de dados por API em lotes fica em \"APIs de dados e metadados\".",
    ),
    "sub:queueable": (
        "Entram as tarefas enfileiradas para execução posterior.",
        "Acompanhamento das filas fica em \"Monitoramento de jobs e limites\".",
    ),
    "sub:future-e-mecanismos-legados": (
        "Entram os métodos assíncronos mais antigos e os casos em que ainda se aplicam.",
        "Mecanismos legados de automação declarativa ficam em \"Mecanismos legados e migração\".",
    ),
    "sub:agendamento": (
        "Entra a execução em horários definidos.",
        "Horários comerciais usados em prazos ficam em \"Horários comerciais e feriados\".",
    ),
    "sub:caminhos-assincronos": (
        "Entram as partes assíncronas de automações declarativas.",
        "O fluxo como um todo fica em \"Flow e orquestração\".",
    ),
    "sub:processamento-orientado-a-eventos": (
        "Entram as reações, dentro da org, a eventos publicados na plataforma.",
        "Publicação, assinatura externa e transporte de eventos ficam em \"Eventos e mensageria\".",
    ),
    "sub:monitoramento-de-jobs-e-limites": (
        "Entram o acompanhamento de execuções assíncronas e os limites que se aplicam a elas.",
        "Limites gerais da org e de API ficam em \"Limites e consumo\" e em \"Contratos, limites e tratamento de falhas\".",
    ),
    # ------------------------------------------------------------------ Integração
    "cls:integracao-apis-e-eventos": (
        "Entra como a org conversa com outros sistemas, nos dois sentidos: APIs oferecidas pela plataforma, autenticação de integrações, chamadas para fora, credenciais, eventos, dados externos e os limites e falhas dessas conversas.",
        "Login de pessoas fica em \"Acesso, identidade e segurança\". Processamento interno de eventos fica em \"Processamento orientado a eventos\".",
    ),
    "sub:apis-de-dados-e-metadados": (
        "Entram as APIs que leem e gravam registros e metadados na org.",
        "Limites e versões dessas APIs ficam em \"Contratos, limites e tratamento de falhas\".",
    ),
    "sub:autenticacao-de-integracoes": (
        "Entram as formas de um sistema externo se autenticar na org.",
        "Login de pessoas por SSO e MFA fica em \"Autenticação, SSO e MFA\".",
    ),
    "sub:chamadas-externas-e-endpoints": (
        "Entram as chamadas da org para serviços externos e o registro dos endereços permitidos.",
        "Credenciais usadas nessas chamadas ficam em \"Credenciais\".",
    ),
    "sub:credenciais": (
        "Entram as credenciais nomeadas e externas usadas por integrações.",
        "Certificados e chaves como proteção geral ficam em \"Credenciais, certificados e proteção de dados\".",
    ),
    "sub:eventos-e-mensageria": (
        "Entram eventos de plataforma, captura de alterações, assinatura externa e transporte de mensagens.",
        "A reação a eventos dentro da org fica em \"Processamento orientado a eventos\".",
    ),
    "sub:conectividade-e-virtualizacao-de-dados": (
        "Entra o acesso a dados externos sem copiá-los para a org.",
        "A modelagem desses dados como objetos externos fica em \"Modelos externos e especializações\".",
    ),
    "sub:contratos-limites-e-tratamento-de-falhas": (
        "Entram limites de API, versões, retentativas e estratégias de erro das integrações.",
        "Limites gerais de consumo da org ficam em \"Limites e consumo\".",
    ),
    # ------------------------------------------------------------------ Relatórios
    "cls:relatorios-analytics-e-exploracao": (
        "Entra como os dados da org são resumidos e explorados: relatórios, dashboards, tipos de relatório, pastas, métricas e recursos analíticos de produto.",
        "Monitoramento técnico da org fica em \"Observabilidade, auditoria e operação\".",
    ),
    "sub:reports": (
        "Entram os relatórios sobre os registros da org.",
        "A definição de quais objetos um relatório usa fica em \"Tipos de relatório\".",
    ),
    "sub:dashboards": (
        "Entram os painéis visuais construídos sobre relatórios.",
        "Compartilhamento dos painéis fica em \"Pastas e acesso\".",
    ),
    "sub:tipos-de-relatorio": (
        "Entra a definição de quais objetos e campos um relatório pode usar.",
        "Os relatórios em si ficam em \"Reports\".",
    ),
    "sub:pastas-e-acesso": (
        "Entram a organização e o compartilhamento de relatórios e dashboards.",
        "Acesso aos registros que aparecem no relatório fica em \"Acesso a registros e hierarquias\".",
    ),
    "sub:metricas-e-agregacoes": (
        "Entram os cálculos de resumo e os indicadores.",
        "Campos de resumo definidos no modelo de dados ficam em \"Campos e tipos\".",
    ),
    "sub:recursos-analiticos-de-produto": (
        "Entram os recursos analíticos que dependem de um produto ou licença.",
        "Relatórios e dashboards da plataforma ficam em \"Reports\" e \"Dashboards\".",
    ),
    # ------------------------------------------------------------------ Conteúdo
    "cls:conteudo-conhecimento-e-colaboracao": (
        "Entram arquivos, bibliotecas, bases de conhecimento, colaboração e modelos de comunicação.",
        "Recuperação de conhecimento para respostas de IA fica em \"Recursos de recuperação de conhecimento\".",
    ),
    "sub:files-e-documentos": (
        "Entram arquivos anexados e documentos.",
        "Recursos estáticos e bibliotecas ficam em \"Bibliotecas e assets\".",
    ),
    "sub:bibliotecas-e-assets": (
        "Entram bibliotecas de conteúdo e recursos estáticos.",
        "Arquivos ligados a registros ficam em \"Files e documentos\".",
    ),
    "sub:knowledge-e-categorias": (
        "Entram artigos de conhecimento e categorias de dados.",
        "O uso do Knowledge no atendimento é estudado também em \"Atendimento\".",
    ),
    "sub:colaboracao": (
        "Entram feeds, grupos e recursos de colaboração.",
        "Notificações enviadas por automações ficam em \"Notificações\".",
    ),
    "sub:templates-e-comunicacao": (
        "Entram modelos de e-mail e de outras comunicações.",
        "Prompts usados por IA ficam em \"Prompts\".",
    ),
    # ------------------------------------------------------------------ Desenvolvimento
    "cls:desenvolvimento-testes-e-entrega": (
        "Entra como mudanças são construídas, testadas, empacotadas e levadas entre ambientes, incluindo os formatos de arquivo de metadados.",
        "As APIs usadas por ferramentas de desenvolvimento são estudadas também em \"APIs de dados e metadados\". Logs de execução ficam em \"Logs e rastreamento\".",
    ),
    "sub:codigo-e-bundles": (
        "Entram classes, componentes e outros artefatos de código vistos como itens a construir e entregar.",
        "O papel do código em uma automação fica em \"Automação Apex\".",
    ),
    "sub:testes": (
        "Entram testes automatizados e cobertura.",
        "Avaliação de agentes de IA fica em \"Segurança, avaliação e governança de IA\".",
    ),
    "sub:pacotes-e-dependencias": (
        "Entram o empacotamento e as dependências entre componentes.",
        "O processo de implantação fica em \"Versionamento, deploy e recuperação\".",
    ),
    "sub:source-format-e-metadata-api-format": (
        "Entram os dois formatos de arquivo de metadados e as diferenças entre eles.",
        "A API que implanta e recupera os arquivos fica em \"APIs de dados e metadados\".",
    ),
    "sub:ambientes-e-sandboxes": (
        "Entram as orgs usadas para desenvolvimento, teste e produção.",
        "Os dados que identificam uma org ficam em \"Identificação e configuração da org\".",
    ),
    "sub:versionamento-deploy-e-recuperacao": (
        "Entram as versões de componentes, a implantação e o retorno a uma versão anterior.",
        "Retenção e exclusão de dados de negócio ficam em \"Retenção, arquivamento e exclusão\".",
    ),
    # ------------------------------------------------------------------ Observabilidade
    "cls:observabilidade-auditoria-e-operacao": (
        "Entra o que mostra como a org está funcionando e o que foi feito nela: logs, auditoria, histórico de login, eventos de monitoramento, consumo de limites e diagnóstico.",
        "Regras de acesso ficam em \"Acesso, identidade e segurança\". Relatórios sobre dados de negócio ficam em \"Relatórios, analytics e exploração\".",
    ),
    "sub:logs-e-rastreamento": (
        "Entram logs de depuração e rastreamento de execução.",
        "Eventos de uso e atividade ficam em \"Eventos de monitoramento\".",
    ),
    "sub:auditoria-de-configuracao": (
        "Entra o registro de alterações feitas no Setup.",
        "Histórico de alterações de registros fica em \"Rastreabilidade e histórico\".",
    ),
    "sub:historico-de-login": (
        "Entram as tentativas de login e o estado de acesso vistos como trilha de auditoria.",
        "Regras que restringem o login ficam em \"Sessões e políticas de login\".",
    ),
    "sub:eventos-de-monitoramento": (
        "Entram os eventos que registram uso e atividade na org.",
        "Eventos de negócio publicados para integrações ficam em \"Eventos e mensageria\".",
    ),
    "sub:limites-e-consumo": (
        "Entra o uso dos limites da plataforma pela org.",
        "Limites específicos de APIs e integrações ficam em \"Contratos, limites e tratamento de falhas\".",
    ),
    "sub:jobs-incidentes-e-diagnostico": (
        "Entram o acompanhamento de jobs e a investigação de problemas na operação.",
        "Limites de execuções assíncronas ficam em \"Monitoramento de jobs e limites\".",
    ),
    # ------------------------------------------------------------------ IA
    "cls:ia-agentes-e-decisoes-assistidas": (
        "Entra a configuração de agentes e recursos de IA: comportamento, ações, prompts, modelos, recuperação de conhecimento e governança.",
        "Bases de conhecimento mantidas por pessoas ficam em \"Knowledge e categorias\". Automações sem IA ficam em \"Automação de processos e regras de negócio\".",
    ),
    "sub:configuracao-de-agentes": (
        "Entram a definição de agentes e de seu comportamento.",
        "O que o agente pode executar fica em \"Ações e tópicos\".",
    ),
    "sub:acoes-e-topicos": (
        "Entram as ações que um agente pode executar e os assuntos que ele atende.",
        "Ações rápidas da interface ficam em \"Ações rápidas\".",
    ),
    "sub:prompts": (
        "Entram os modelos de instrução usados por recursos de IA.",
        "Modelos de e-mail ficam em \"Templates e comunicação\".",
    ),
    "sub:modelos-e-grounding": (
        "Entram os modelos usados e os dados que fundamentam as respostas.",
        "A busca de conteúdo para as respostas fica em \"Recursos de recuperação de conhecimento\".",
    ),
    "sub:recuperacao-de-conhecimento": (
        "Entra a busca de conteúdo para alimentar respostas de IA.",
        "Os artigos de conhecimento em si ficam em \"Knowledge e categorias\".",
    ),
    "sub:seguranca-avaliacao-e-governanca-de-ia": (
        "Entram controles, testes e auditoria específicos de recursos de IA.",
        "Segurança geral da org fica em \"Acesso, identidade e segurança\".",
    ),
    # ------------------------------------------------------------------ Produto
    "cls:processos-de-negocio-especificos-de-produto": (
        "Entram capacidades próprias de um produto ou setor, que não fazem parte da plataforma compartilhada por todas as nuvens.",
        "Recursos de plataforma usados por vários produtos ficam no tema funcional deles (por exemplo, \"Automação\" ou \"Interface\"), e a funcionalidade aparece aqui só como secundária.",
    ),
    "sub:vendas": (
        "Entram as capacidades próprias do processo de vendas.",
        "Recursos de plataforma usados em vendas, como regras de atribuição, ficam no tema funcional e aparecem aqui como secundários.",
    ),
    "sub:atendimento": (
        "Entram as capacidades próprias do processo de atendimento.",
        "Recursos de plataforma usados no atendimento, como apps de console e Knowledge, ficam no tema funcional e aparecem aqui como secundários.",
    ),
    "sub:servico-de-campo": (
        "Entram as capacidades próprias de serviço de campo.",
        "O atendimento por casos fica em \"Atendimento\".",
    ),
    "sub:receita-e-comercio": (
        "Entram as capacidades de receita, cotação e comércio.",
        "Cotações do processo de vendas da plataforma ficam em \"Vendas\".",
    ),
    "sub:experiencias-externas": (
        "Entram as capacidades de produto voltadas a públicos externos, como clientes e parceiros.",
        "Sites e portais vistos como interface ficam em \"Experiências web/portais e mobile\".",
    ),
    "sub:capacidades-setoriais": (
        "Entram as capacidades das nuvens setoriais.",
        "Capacidades de vendas e atendimento comuns a vários setores ficam em \"Vendas\" e \"Atendimento\".",
    ),
    "sub:outras-areas": (
        "Entram, de forma provisória, áreas encontradas no inventário oficial que ainda não têm tema próprio.",
        "Quando uma área ganhar tema próprio, ela sai daqui.",
    ),
}


def aplicar():
    vistos = set()
    for pasta in ("classificacoes", "subclassificacoes"):
        d = os.path.join(ROOT, pasta)
        for nome in sorted(os.listdir(d)):
            if not nome.endswith(".json"):
                continue
            with open(os.path.join(d, nome), encoding="utf-8") as f:
                ent = json.load(f)
            if ent["id"] not in TEXTOS:
                raise SystemExit(f"sem escopo: {ent['id']}")
            escopo, fora = TEXTOS[ent["id"]]
            novo = {}
            for k, v in ent.items():
                if k in ("escopo", "fora_do_escopo"):
                    continue
                novo[k] = v
                if k == "descricao":
                    novo["escopo"] = escopo
                    novo["fora_do_escopo"] = fora
            save(pasta, nome[:-5], novo)
            vistos.add(ent["id"])
    sobras = set(TEXTOS) - vistos
    if sobras:
        raise SystemExit(f"temas inexistentes no catálogo: {sorted(sobras)}")
    print(f"escopo aplicado a {len(vistos)} temas")


if __name__ == "__main__":
    aplicar()
