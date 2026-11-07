A CTA exige, como pré-requisitos, os dois “domínios” de arquiteto — **Application Architect** e **System Architect** — que são concedidos automaticamente após concluir seus respectivos conjuntos de certificações. A visão mais útil para estudar não é memorizar cada feature isolada, mas organizá-las em **capacidades da plataforma**: identidade/acesso, dados, automação, interface, integração, processamento assíncrono, DevOps e governança. [trailhead.salesforce](https://trailhead.salesforce.com/en/credentials/technicalarchitect)

## Certificações-base da CTA

| Trilha | Certificações necessárias | Foco principal |
|---|---|---|
| **Application Architect** | Platform App Builder, Platform Developer I, Data Architecture and Management Designer, Sharing and Visibility Designer | Modelagem de dados, segurança de dados, compartilhamento, desenvolvimento declarativo e programático.  [trailhead.salesforce](https://trailhead.salesforce.com/en/credentials/technicalarchitect) |
| **System Architect** | Platform Developer I, Integration Architecture Designer, Identity and Access Management Designer, Development Lifecycle and Deployment Designer | Integrações, identidade, segurança entre sistemas, SDLC, deploy e governança.  [trailhead.salesforce](https://trailhead.salesforce.com/en/credentials/technicalarchitect) |
| **CTA** | Application Architect + System Architect + Review Board (avaliação e exame) | Desenho de soluções seguras, performáticas, integradas e sustentáveis no ecossistema Salesforce.  [trailhead.salesforce](https://trailhead.salesforce.com/en/credentials/technicalarchitect) |

## 1. Acesso, identidade e segurança

**Analogia:** pense no Salesforce como um prédio. O *Profile* é a chave padrão do apartamento; *Permission Sets* são permissões extras; *Roles* definem de quem você pode “enxergar” os andares; e *Sharing Rules* são autorizações específicas para determinados visitantes.

| Classificação | Features internas | Pergunta que responde |
|---|---|---|
| **Identidade do usuário** | Users, Contacts associados a Users, User Licenses, MFA, Login Flows, Session Settings, Login IP Ranges, Connected Apps, OAuth, SSO/SAML, Identity Provider | “Quem é a pessoa e como ela entra?” |
| **Perfil e permissões** | Profiles, Permission Sets, Permission Set Groups, Muting Permission Sets, Custom Permissions, User Permissions | “O que a pessoa pode fazer?” |
| **Controle por objeto** | Object Permissions, CRUD, View All, Modify All, Tab Visibility, App Visibility | “Pode ver, criar, editar ou excluir esse tipo de registro?” |
| **Controle por campo** | Field-Level Security (FLS), Field Accessibility, Page Layouts, Compact Layouts | “Quais campos ela pode ver ou editar?” |
| **Controle por registro** | Organization-Wide Defaults (OWD), Role Hierarchy, Sharing Rules, Manual Sharing, Apex Managed Sharing, Ownership, Queues, Teams | “Quais registros específicos ela pode acessar?” |
| **Segurança de código e dados** | Apex Security, CRUD/FLS enforcement, Lightning Web Security, Shield Platform Encryption, Event Monitoring, Field Audit Trail, Data Classification | “Como protegemos código, dados sensíveis e auditoria?” |

A Salesforce trata o acesso em quatro camadas — organização, objeto, campo e registro — e recomenda usar Permission Sets e Permission Set Groups para permissões funcionais, mantendo Profiles para controles como layout, login, IP e visibilidade de apps. [architect.salesforce](https://architect.salesforce.com/docs/architect/well-architected/guide/trust.html)

## 2. Dados e modelagem

**Analogia:** o modelo de dados é a “planta baixa” da solução. Se você modelar errado, toda automação, integração e relatório depois precisará contornar uma estrutura ruim.

| Classificação | Features internas | Exemplo prático |
|---|---|---|
| **Objetos** | Standard Objects, Custom Objects, External Objects, Big Objects, Platform Events, Custom Metadata Types, Custom Settings | `Case`, `FraudCase__c`, `Transaction__c` |
| **Campos** | Standard Fields, Custom Fields, Formula Fields, Roll-Up Summary Fields, Auto Number, External ID, Unique Fields, Encrypted Fields | `CPF__c`, `RiskScore__c`, `TransactionAmount__c` |
| **Relacionamentos** | Lookup, Master-Detail, Many-to-Many via Junction Object, Self-relationship, Hierarchical relationship, External Lookup, Indirect Lookup | `Transaction__c` ligado a `Account`; junction entre `Customer` e `FraudCase` |
| **Comportamento de dados** | Record Types, Picklists/Global Value Sets, Dependent Picklists, Validation Rules, Duplicate Rules, Matching Rules, Data Quality | Diferenciar “fraude confirmada” de “suspeita” |
| **Volume e arquivamento** | Big Objects, Data Archiving, Data Storage, External Objects via Salesforce Connect, Data Cloud | Histórico de transações com milhões de registros |
| **Metadados e configuração** | Custom Metadata Types, Custom Settings, Dynamic Forms, Field Sets, Record Page Settings | Tabelas de parâmetros de risco configuráveis por ambiente |

## 3. Automação de processo

**Analogia:** automação é o “fluxo de trabalho” do prédio: quando alguém entra, o sistema decide se abre a porta, notifica a segurança, cria um chamado ou bloqueia o acesso.

| Classificação | Features internas | Quando usar |
|---|---|---|
| **Automação declarativa** | Record-Triggered Flows, Scheduled Flows, Screen Flows, Autolaunched Flows, Process Builder legado, Workflow Rules legado | Regras de negócio sem código, sempre que possível |
| **Automação programática** | Apex Triggers, Apex Classes, Apex REST, Apex SOAP, Invocable Apex, Continuation Apex | Lógica complexa, integrações e regras que o Flow não cobre bem |
| **Automação de interface** | LWC, Aura Components, Visualforce, Dynamic Forms, Flow Screens, OmniScripts | Formulários, telas e jornadas guiadas |
| **Automação externa/orquestração** | OmniStudio Integration Procedures, DataRaptors, FlexCards, MuleSoft, Flow Orchestrator | Processos multietapa, dados de múltiplas fontes e jornadas complexas |
| **Eventos e mensageria** | Platform Events, Change Data Capture, Push Topics, Streaming API, Outbound Messages | Integração orientada a eventos, como publicar “transação suspeita” para antifraude |

Flow, OmniStudio e LWC podem se integrar ao Apex e suportam platform events e APIs; a escolha depende do contexto de dados, complexidade da interface e necessidade de código. [architect.salesforce](https://architect.salesforce.com/docs/architect/decision-guides/guide/build-forms)

## 4. Interface e experiência

| Classificação | Features internas | Exemplo |
|---|---|---|
| **Aplicativos** | Lightning Apps, App Launcher, Navigation Items, Console Apps, Mobile Apps | App “Antifraude” para analistas |
| **Páginas** | Lightning Record Pages, App Pages, Home Pages, Dynamic Forms, Lightning App Builder | Página de caso com score de risco e histórico |
| **Componentes** | Standard LWC, Custom LWC, Aura Components, Visualforce Pages, Lightning Web Components em Flow | Componente de timeline de transações |
| **Experiência externa** | Experience Cloud, Experience Builder, Digital Experiences, Guest User, Site.com | Portal para cliente acompanhar contestação |
| **Produtividade** | Einstein/Agentforce, Slack, Quip, Email Templates, Quick Actions, Global Actions | Resumo de caso gerado por IA ou ação rápida “Escalar risco” |

## 5. Integração

**Analogia:** integração é a rede de corredores entre prédios. Você precisa definir quem chama quem, com qual credencial, qual formato de mensagem e o que acontece se o outro prédio estiver fora do ar.

| Classificação | Features internas | Padrão típico |
|---|---|---|
| **APIs de dados** | REST API, SOAP API, Bulk API, UI API, Tooling API, Metadata API | Sincronizar ou migrar dados |
| **APIs de eventos** | Platform Events, Change Data Capture, Streaming API, Pub/Sub API | Notificar outro sistema em tempo quase real |
| **Chamadas externas** | Named Credentials, External Credentials, Remote Site Settings, Apex Callouts, External Services | Chamar um serviço de score de crédito |
| **Middleware e orquestração** | MuleSoft, Salesforce Connect, External Objects, Integration Procedures, API Manager | Integrações complexas, reuso e governança |
| **Identidade entre sistemas** | OAuth 2.0, JWT Bearer Flow, SAML, Connected Apps, Named Credentials, Web Server Flow | Integração segura sem expor senha |
| **Padrões de integração** | Request-Reply, Fire-and-Forget, Batch Data Sync, Remote Process Invocation, Event-Driven, Data Virtualization | Escolher o padrão antes de escolher a ferramenta |

## 6. Processamento em lote e assíncrono

**Analogia:** se uma tarefa é “lavar 100 mil pratos”, você não faz tudo no caixa do restaurante: separa em lotes, coloca na máquina e avisa quando terminar.

| Classificação | Features internas | Característica |
|---|---|---|
| **Batch Apex** | `Database.Batchable`, Batch Jobs, Batch Apex Chaining | Grandes volumes, processados em blocos |
| **Agendamento** | Schedulable Apex, Scheduled Flows, Cron-like schedules | Execução recorrente, como consolidação noturna |
| **Filas assíncronas** | Queueable Apex, Future Methods, Async Apex | Tarefas pontuais que não devem bloquear o usuário |
| **Processamento paralelo** | Batch Apex, Queueable, Platform Events, External compute | Escalar carga e reduzir tempo de execução |
| **Limites e monitoramento** | Governor Limits, AsyncApexJob, Apex Flex Queue, Setup Audit Trail, Debug Logs | Controlar consumo, falhas e reprocessamento |
| **Mensageria durável** | Platform Events, Change Data Capture, Pub/Sub API | Desacoplar produtores e consumidores |

## 7. DevOps, ambientes e governança

| Classificação | Features internas | Objetivo |
|---|---|---|
| **Ambientes** | Scratch Orgs, Sandboxes, Developer Edition, Production Org | Separar desenvolvimento, teste e produção |
| **Metadados e deploy** | Metadata API, Change Sets, Salesforce CLI, SFDX, Packages, Unlocked Packages | Versionar e mover configuração/código |
| **CI/CD** | GitHub/GitLab/Azure DevOps, pipelines, Copado, Gearset, AutoRABIT | Automatizar build, teste e deploy |
| **Testes** | Apex Tests, Test Data Factory, Test Classes, Code Coverage, User Acceptance Testing | Garantir qualidade antes de produção |
| **Observabilidade** | Debug Logs, Event Monitoring, Apex Exception Email, System Overview, Health Check | Detectar erros, limites e riscos |
| **Governança** | Setup Audit Trail, Permission Set Groups, Naming Conventions, Release Management, Documentation | Reduzir dívida técnica e risco operacional |

## Mapa mental para CTA

Ao analisar qualquer cenário de CTA, percorra estas perguntas:

1. **Quem acessa?** Usuário, sistema, integração ou agente?
2. **O que ele pode ver e fazer?** Identidade, perfil, permissões, FLS e sharing.
3. **Quais dados existem?** Objetos, campos, relacionamentos, volume e sensibilidade.
4. **O que precisa acontecer automaticamente?** Flow, Apex, OmniStudio, evento ou job assíncrono.
5. **Como o usuário interage?** LWC, Flow Screen, OmniScript, Experience Cloud ou app externo.
6. **Quais sistemas participam?** APIs, middleware, eventos, sincronização ou virtualização.
7. **Qual é o volume e a urgência?** Síncrono, assíncrono, batch, streaming ou Big Object.
8. **Como isso entra em produção com segurança?** Ambientes, testes, CI/CD, observabilidade e governança.

Essa taxonomia cobre o núcleo avaliado nas certificações que alimentam a CTA: dados, sharing/visibility, desenvolvimento, integração, identidade e SDLC/deploy. [trailhead.salesforce](https://trailhead.salesforce.com/en/credentials/technicalarchitect)
