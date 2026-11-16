# Arquitetura da Plataforma Salesforce: guia caixa a caixa

Este guia explica, em até 500 caracteres cada, as caixas do diagrama oficial da Salesforce Architects, para quem vem do back-end e está conhecendo a plataforma.

## O diagrama

![Next Gen Platform Architecture Overview](https://architect.salesforce.com/ns-assets/legacy/image2-architectureoverview.png)

Fonte: [The Salesforce Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation) (Salesforce Architects).

## Como ler

- O diagrama é um mapa por camadas: cada camada inferior é usada pelas de cima. A própria Salesforce diz que as caixas dentro de cada camada são exemplos ilustrativos.
- A leitura recomendada é de baixo para cima: Hyperforce, Metadata Framework, Data, AI, serviços de plataforma e, por fim, apps.
- Não é um diagrama de rede nem de infraestrutura física: não mostra servidores, tabelas nem fluxos de requisição.
- Os textos abaixo são explicações didáticas, com base na página citada e nos links de documentação de cada caixa. Onde a Salesforce não detalha um termo, o texto indica isso.
- Links de ajuda (help.salesforce.com) podem mudar de caminho com o tempo; se algum não abrir, busque pelo nome da caixa na documentação.

## Mapa das camadas

| Camada (de cima para baixo) | Para que serve |
|---|---|
| Apps e Industries | Produtos prontos e agentes |
| User / Developer Experiences | Interfaces para usuários e desenvolvedores |
| APIs e API Management | Acesso programático a tudo |
| Business Capabilities | Capacidades de negócio reutilizáveis |
| App Platform Services | Framework de construção (código, automação, segurança) |
| AI | Modelos, agentes, RAG, confiança |
| Data | Banco transacional, lakehouse, busca |
| Metadata Framework | Aplicação descrita por metadados |
| Hyperforce | Infraestrutura em nuvem pública |
| Integrations | Coluna lateral para o mundo externo |

## Apps e Industries

Camada de topo: os produtos prontos e os agentes construídos sobre o que está embaixo. Tudo aqui consome as camadas inferiores.

### Agents

Agentes de IA (Agentforce) que executam tarefas dentro dos apps: respondem clientes, atualizam registros, acionam Flow ou Apex. Nos apps, aparecem como uma forma a mais de interagir com os mesmos dados e regras. Analogia: um serviço que, em vez de expor só endpoints para humanos, também aceita pedidos em linguagem natural e chama a lógica existente.

Documentação: [Agentforce Developer Guide](https://developer.salesforce.com/docs/ai/agentforce/overview)

### Sales

Cloud de vendas: contas, contatos, oportunidades, previsões e pipeline. É um conjunto de objetos, automações e telas padrão construído sobre a mesma plataforma, não um sistema separado. Analogia: um módulo de domínio (CRM de vendas) que roda sobre o mesmo runtime e banco compartilhado.

Documentação: [Sales Cloud](https://www.salesforce.com/sales/)

### Service

Cloud de atendimento: casos, filas, Knowledge, omnicanal e Field Service. Usa o mesmo modelo de objetos, segurança e automação da plataforma, com recursos específicos de suporte. Analogia: outro módulo de domínio sobre a mesma base, como um bounded context de atendimento.

Documentação: [Service Cloud](https://www.salesforce.com/service/)

### Marketing

Produtos para segmentar públicos, orquestrar jornadas e medir campanhas. Parte usa o núcleo da plataforma e parte roda em serviços próprios, ligados por integração e por Data 360. Por isso, ao avaliar, não presuma o mesmo runtime para todos os produtos do portfólio.

Documentação: [Marketing](https://www.salesforce.com/marketing/)

### Commerce

Soluções de comércio digital (B2B e B2C): catálogo, carrinho, preços, pedidos e pagamentos. O portfólio mistura capacidades nativas da plataforma com componentes próprios; confirme o produto exato antes de assumir limites ou ferramentas de desenvolvimento.

Documentação: [Commerce](https://www.salesforce.com/commerce/)

### Industries

Soluções por setor (serviços financeiros, saúde, comunicações, governo e outros), com modelos de dados, processos e componentes prontos para cada indústria. Analogia: bibliotecas de domínio que estendem o modelo base, no lugar de começar do zero.

Documentação: [Industries](https://www.salesforce.com/industries/)

### Tableau

Análise e visualização de dados. Tableau Next integra métricas, semântica e IA ao Data 360, para que usuários consultem dados governados e recebam insights contextuais, inclusive dentro de fluxos de trabalho da Salesforce.

Documentação: [Tableau Next (guia dev)](https://developer.salesforce.com/docs/analytics/tableau-next-isv-dev/guide/tn-features-overview.html)

### Platform

A própria plataforma como produto: ferramentas low-code e pro-code, modelo de dados, automação, APIs, segurança e distribuição de apps. É a camada em que você constrói customizações e apps próprios, reutilizando o que as camadas inferiores oferecem.

Documentação: [Salesforce Platform](https://www.salesforce.com/platform/)

### AppExchange

Marketplace oficial de apps, componentes e serviços de parceiros (ISVs). Os apps são distribuídos como pacotes de metadados e instalados na org, sem reconstruir a solução. Analogia: um registry de pacotes com versionamento e controle de upgrade.

Documentação: [AppExchange](https://appexchange.salesforce.com/)

### Slack

Plataforma de colaboração usada como interface conversacional e de trabalho. Pode receber alertas, abrir ações sobre registros e hospedar agentes, conectando equipes aos dados e processos da Salesforce sem trocar de ferramenta.

Documentação: [Slack](https://slack.com/)

### Mulesoft

Plataforma de integração e gestão de APIs (Anypoint). Conecta Salesforce a ERPs, bancos e sistemas legados, com conectores, governança, runtimes gerenciados e observabilidade. Analogia: um API gateway somado a um barramento de integração, oferecido como produto.

Documentação: [Documentação MuleSoft](https://docs.mulesoft.com/general/)

## User Experiences

Como as pessoas usam a plataforma. São interfaces geradas a partir de metadados, em vez de telas programadas uma a uma.

### Non-Modal UI (Agent)

Interpretação: a interface conversacional dos agentes, na qual o usuário pede em linguagem natural e o agente age, sem abrir telas modais em sequência. O diagrama não detalha o termo; a página da Salesforce Architects descreve a evolução da plataforma para experiências agênticas conversacionais.

Documentação: [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

### Lightning

A interface web principal, orientada a metadados: páginas, layouts e componentes que mudam sem deploy de código de front-end. A Lightning Web Stack inclui Web Components, Lightning Web Security e Lightning Data Service. Analogia: um front-end renderizado a partir de configuração declarativa.

Documentação: [Lightning Web Components](https://developer.salesforce.com/docs/platform/lwc/overview)

### Collaboration (Slack)

Colaboração integrada: conversas e canais associados a registros e trabalho. Em vez de e-mail solto, discussões e aprovações ficam ligadas ao contexto do dado, e notificações podem chegar direto à ferramenta onde a equipe já trabalha.

Documentação: [Slack](https://slack.com/)

### Mobile

App móvel nativo da Salesforce, que reaproveita apps Lightning sem código novo, além de Mobile SDK para apps próprios. Há recursos offline, e o Mobile Publisher permite marca própria. Analogia: um cliente nativo que consome as mesmas APIs e metadados.

Documentação: [Mobile SDK](https://developer.salesforce.com/docs/platform/mobile-sdk/overview)

## Developer Experiences

Ferramentas para construir, testar e entregar. Cobrem desde low-code até pro-code e ciclo de vida de aplicação.

### Assistants/Builders

Assistentes de IA e construtores visuais para acelerar o desenvolvimento: geração de código, explicação, testes de Apex, criação de agentes e flows. Servem como apoio, e o código gerado ainda precisa de revisão, teste e deploy como qualquer outro.

Documentação: [Agentforce Vibes IDE](https://developer.salesforce.com/docs/platform/code-builder/guide/codebuilder-overview.html)

### CLI/IDE

Salesforce CLI e IDEs (VS Code, Code Builder) para trabalhar com código e metadados em arquivos, versionar no Git e fazer retrieve/deploy. Analogia: o fluxo de repositório + build + deploy que você já conhece, aplicado à configuração da org.

Documentação: [Salesforce DX Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_intro.htm)

### App Lifecycle Management

Gestão do ciclo de vida: sandboxes, scratch orgs, pacotes, DevOps Center e pipelines de CI/CD. Garante que alterações passem por ambientes e validações antes de chegar à produção.

Documentação: [DevOps Center](https://developer.salesforce.com/docs/platform/devops-center-dev/guide/devops-center-dev-overview.html) · [Scratch Orgs](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_scratch_orgs.htm)

### Envs

Ambientes: produção, sandboxes (de diferentes tamanhos e dados) e scratch orgs descartáveis. Analogia: dev, QA, staging e prod, com tipos diferentes de cópia de dados e metadados.

Documentação: [Sandboxes (ajuda)](https://help.salesforce.com/s/articleView?id=sf.create_test_instance.htm&language=en_US&type=5)

## APIs e API Management

As capacidades da plataforma são expostas por APIs. A Salesforce descreve a plataforma como API-first.

### APIs and API Management

Portfólio de APIs: REST e SOAP para operações transacionais, Bulk API para grandes volumes, Pub/Sub API para eventos e APIs específicas de produtos, além de endpoints Apex customizados. O MuleSoft API Manager cobre governança, políticas e analytics de APIs. Analogia: API gateway, versionamento e contratos.

Documentação: [API Library](https://developer.salesforce.com/docs/apis) · [REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm) · [Bulk API 2.0](https://developer.salesforce.com/docs/platform/api-asynch/guide/bulk-api-2-0.html) · [Pub/Sub API](https://developer.salesforce.com/docs/platform/pub-sub-api/overview)

## Business Capabilities

Capacidades de negócio reutilizáveis (as caixas são ilustrativas). Cada uma depende de produto e licenciamento específicos.

### Lead Forecasting

Previsão e pontuação de leads e oportunidades com IA e dados históricos, para priorizar o time comercial. A disponibilidade depende do produto e da licença; confirme na documentação do cloud em uso.

Documentação: [Einstein Sales (ajuda)](https://help.salesforce.com/s/articleView?id=sf.einstein_sales_forecasting_setup.htm&language=en_US&type=5)

### Multi-Channel Messaging

Atendimento e engajamento por vários canais (chat, mensagens, WhatsApp, SMS, e-mail) em uma experiência unificada, com histórico ligado ao cliente. Analogia: um adaptador de canais sobre um mesmo modelo de conversa.

Documentação: [Digital Engagement (ajuda)](https://help.salesforce.com/s/articleView?id=sales.sales_core_digital_engagment.htm&language=en_US&type=5)

### Knowledge Articles

Base de conhecimento com artigos, aprovação, versões e busca, usada por atendentes e por agentes de IA para responder com informação confiável.

Documentação: [Knowledge (ajuda)](https://help.salesforce.com/s/articleView?id=service.knowledge_whatis.htm&language=en_US&type=5)

### Segmentation

Criação de públicos a partir de dados unificados, para campanhas e ativações. No Marketing Cloud Next, a segmentação usa o Data 360 como fonte de dados.

Documentação: [Segmentos de marketing (ajuda)](https://help.salesforce.com/s/articleView?id=mktg.mktg_audiences_segments.htm&language=en_US&type=5)

### Metrics & Visualization

Métricas governadas e visualizações para acompanhar desempenho. Tableau Next oferece camada semântica, KPIs reutilizáveis e dashboards ligados ao Data 360.

Documentação: [Tableau Next](https://developer.salesforce.com/docs/analytics/tableau-next-isv-dev/guide/tn-features-overview.html)

### Payments

Recursos de pagamento ligados a pedidos e cobrança, para cobrar clientes dentro dos processos da Salesforce. Depende do produto e da região; consulte a ajuda para pré-requisitos.

Documentação: [Salesforce Payments (ajuda)](https://help.salesforce.com/s/articleView?id=commerce.payments_product_intro.htm&language=en_US&type=5)

### Order Management

Gestão de pedidos: captura, cumprimento, faturamento e devoluções. Fornece modelo de dados, fluxos e APIs para o ciclo do pedido, e pode ser integrada a ERP e logística.

Documentação: [Order Management Developer Guide (versão 224, pode estar desatualizada)](https://developer.salesforce.com/docs/atlas.en-us.224.0.order_management_developer_guide.meta/order_management_developer_guide/order_management_developer_guide_intro.htm)

### ... (outras)

O diagrama indica que há outras capacidades de negócio além das listadas. Funcionam como blocos prontos que times e parceiros podem estender, em vez de recriar do zero.

Documentação: [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

## App Platform Services

O 'framework' que você usa para construir: identidade, segurança, automação, código, empacotamento e modelagem de dados.

### Tenancy/Identity

Isola cada cliente (tenant/org) e identifica usuários. Cada org vê só seus dados e metadados; o My Domain é o endereço estável que roteia o tráfego. Analogia: tenant ID em toda tabela, com autenticação centralizada.

Documentação: [Multitenant Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture) · [My Domain (ajuda)](https://help.salesforce.com/s/articleView?id=sf.domain_name_overview.htm&language=en_US&type=5)

### Access Controls

Define quem acessa o quê: permissões de objeto e campo (CRUD/FLS), conjuntos de permissões e compartilhamento por registro. Autenticação é outra coisa: ela prova quem é o usuário, enquanto o controle de acesso decide o que ele pode fazer.

Documentação: [Secure Your Salesforce Org](https://developer.salesforce.com/docs/atlas.en-us.securityImplGuide.meta/securityImplGuide/users_profiles_overview.htm) · [Sharing Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture)

### Licensing & Provisioning

Controla quais produtos e recursos cada org pode usar, por licenças de usuário, licenças de conjunto de permissões e provisionamento. É o mecanismo que libera, por tenant, funcionalidades construídas pela Salesforce.

Documentação: [Licenças (ajuda)](https://help.salesforce.com/s/articleView?id=sf.users_licenses_overview.htm&language=en_US&type=5)

### Flow/Workflow/Formulas

Automação declarativa: Flow para processos, fórmulas para campos calculados. Rodam dentro da transação de gravação, em posições definidas pela ordem de execução. Escolha entre Flow e Apex deve considerar complexidade, volume, controle e manutenção.

Documentação: [Flow (ajuda)](https://help.salesforce.com/s/articleView?id=sf.flow_build.htm&language=en_US&type=5)

### Apex Code

Linguagem Java-like, executada no servidor da plataforma, para lógica de negócio, triggers e serviços. Roda sob governor limits e é compilada e armazenada como metadado na org. Analogia: código de serviço em runtime gerenciado, com cotas por transação.

Documentação: [Apex Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_dev_guide.htm) · [Governors e limites](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm)

### Lightning Web Stack

Conjunto de tecnologias de front-end: Lightning Web Components (padrões W3C), Lightning Web Security, Lightning Data Service e design system. O LWC pode usar LDS ou chamar métodos Apex como back-end.

Documentação: [LWC](https://developer.salesforce.com/docs/platform/lwc/overview) · [Lightning Data Service](https://developer.salesforce.com/docs/platform/lwc/guide/data-ui-api.html) · [Lightning Web Security](https://developer.salesforce.com/docs/platform/lwc/guide/security-lwsec-intro.html)

### Sites + CDN

Publicação de sites e portais (Experience Cloud) para clientes e parceiros, com entrega por CDN. Reaproveita o modelo de dados e a segurança da org, e expõe parte deles na internet com controle de acesso.

Documentação: [Experience Cloud (ajuda)](https://help.salesforce.com/s/articleView?id=experience.networks_setup_basics.htm&language=en_US&type=5)

### Packaging

Empacota metadados em artefatos instaláveis, para distribuir apps entre orgs, sem reconstruir. A geração atual (2GP) traz versionamento, dependências e deploy por diferenças. Analogia: pacotes versionados com dependências.

Documentação: [Second-Generation Managed Packages](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_dev_dev2gp.htm)

### Metadata API

API que lê e implanta a configuração da org (objetos, campos, flows, classes e outros). Base do retrieve/deploy das ferramentas. O formato de arquivo varia: a API usa XML, mas o runtime não depende de arquivos XML da forma como você os vê no repositório.

Documentação: [Metadata API](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_intro.htm)

### Data Modeling

Definição de objetos, campos e relacionamentos (lookup, master-detail) como metadados. Criar um objeto custom não cria tabela física equivalente: a plataforma materializa a estrutura em tempo de execução a partir dos metadados.

Documentação: [Object Reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_list.htm) · [Schema Builder (ajuda)](https://help.salesforce.com/s/articleView?id=sf.schema_builder.htm&language=en_US&type=5)

### Data Runtime & Query

O motor que executa consultas e operações sobre os dados do tenant. Os desenvolvedores usam SOQL e SOSL em vez de SQL; o runtime aplica isolamento por tenant, segurança e otimizações automaticamente.

Documentação: [SOQL](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm) · [Multitenant Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture)

### Layered Extension

Modelo em camadas: Salesforce, parceiros, admins/desenvolvedores da org e usuários finais estendem a mesma aplicação sem interferir um no outro. A ordem de execução da gravação aplica lógica das camadas de forma previsível.

Documentação: [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation) · [Order of Execution](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)

### Events & Notifications

Eventos e notificações para desacoplar processos: Platform Events, mensagens assíncronas e Pub/Sub API. A Salesforce descreve Apache Kafka interno por trás de event streams. Analogia: um barramento publish/subscribe com esquemas versionados.

Documentação: [Platform Events](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/platform_events_intro.htm) · [Pub/Sub API](https://developer.salesforce.com/docs/platform/pub-sub-api/overview)

### Data Loss Prevention

Controles para evitar vazamento de dados sensíveis, como classificação, mascaramento e criptografia. O Shield reúne recursos adicionais (criptografia, monitoramento de eventos, trilha de auditoria) e é um produto à parte.

Documentação: [Salesforce Shield](https://www.salesforce.com/platform/shield/)

### Security & Compliance

Controles de segurança e conformidade embutidos: criptografia em trânsito e em repouso, trilha de auditoria e adesão a mais de 40 padrões (como PCI DSS, GDPR, HIPAA e FedRAMP, segundo a Salesforce). A responsabilidade é compartilhada com quem configura a org.

Documentação: [Compliance](https://compliance.salesforce.com/) · [Trust](https://trust.salesforce.com/)

### Globalization/Localization

Suporte a múltiplos idiomas, moedas, fusos e formatos regionais, com ferramentas de tradução de rótulos e metadados. Importante em orgs multinacionais, nas quais o mesmo metadado precisa de várias línguas.

Documentação: [Translation Workbench (ajuda)](https://help.salesforce.com/s/articleView?id=platform.workbench.htm&language=en_US&type=5)

## AI

Camada de IA construída sobre os dados, para experiências agênticas confiáveis. Os nomes das caixas são capacidades; o produto exato muda com o tempo.

### Trust Layer

Camada que protege dados em uso de IA generativa: mascaramento de dados sensíveis, controles de privacidade, moderação de conteúdo, detecção de toxicidade e política de não retenção por terceiros (conforme a documentação). Analogia: um proxy de segurança entre o app e o modelo.

Documentação: [Trust Layer](https://developer.salesforce.com/docs/ai/agentforce/guide/trust.html) · [Trusted AI](https://www.salesforce.com/artificial-intelligence/trusted-ai/)

### Model Management

Gerencia modelos preditivos e generativos: treinar, ajustar, importar e conectar modelos próprios ou de terceiros. Permite escolher o modelo adequado, com governança sobre quem usa e para quê.

Documentação: [Modelos suportados](https://developer.salesforce.com/docs/ai/agentforce/guide/supported-models.html) · [Foundation models (ajuda)](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_foundation_models.htm&language=en_US&type=5)

### AI Gateway

Interface unificada para acessar diferentes provedores de LLM e modelos preditivos, abstraindo diferenças entre eles e aplicando controles de segurança. Analogia: um API gateway para modelos.

Documentação: [Agentforce e Generative AI](https://developer.salesforce.com/docs/einstein/genai/overview)

### AI Inference

Execução de modelos para gerar respostas ou previsões em tempo de uso. Conecta chamadas a LLMs, embeddings, busca vetorial e recuperação para RAG dentro de agentes e fluxos.

Documentação: [Agentforce e Generative AI](https://developer.salesforce.com/docs/einstein/genai/overview)

### Agent Orchestration

Coordena agentes e serviços: entende o pedido, escolhe ações, chama ferramentas e monitora resultados. O Agentforce usa arquitetura assíncrona e orientada a eventos para cenários com múltiplos agentes.

Documentação: [Agentforce Developer Guide](https://developer.salesforce.com/docs/ai/agentforce/overview)

### RAG

Recuperação aumentada por geração: busca dados relevantes (Data 360, índice vetorial) e injeta no prompt para fundamentar a resposta do LLM em dados reais da empresa. Reduz respostas inventadas e dá rastreabilidade à fonte.

Documentação: [Data 360 – Features](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-features-overview.html)

### Planner

Interpreta o pedido do usuário, identifica a intenção, monta um plano estruturado e dispara ações. A abordagem de raciocínio híbrido combina partes determinísticas com raciocínio do LLM.

Documentação: [Hybrid Reasoning](https://architect.salesforce.com/docs/architect/fundamentals/guide/hybrid-reasoning-agentforce-builder-agent-script.html)

### Augmented Analytics

Análises ampliadas por IA: insights proativos, explicação de variações e recomendação de ações sobre dados governados. Tableau Next e Tableau Pulse são os produtos associados a essa capacidade.

Documentação: [Tableau Next](https://developer.salesforce.com/docs/analytics/tableau-next-isv-dev/guide/tn-features-overview.html)

## Data

Armazenamento e processamento. Há um banco relacional transacional para o CRM e uma plataforma de dados (Data 360) para escala analítica e IA.

### SDB

SalesforceDB: banco relacional cloud-native baseado em PostgreSQL, com armazenamento e computação separados, para dados transacionais do CRM e metadados. Não presuma que substitui o Oracle em todo lugar nem que há uma tabela física por objeto; veja o artigo técnico da VLDB.

Documentação: [Artigo VLDB (SalesforceDB)](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf) · [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

### Lakehouse

Armazenamento analítico do Data 360 em Apache Iceberg e Parquet, para dados estruturados e não estruturados em lote, streaming e tempo real. Analogia: um data lakehouse aberto ao lado do banco transacional.

Documentação: [Data 360 Architecture](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-architecture.html)

### Semantic Models

Camada semântica que dá significado de negócio a dados analíticos (métricas, dimensões, hierarquias), permitindo consultas declarativas consistentes por pessoas, dashboards e agentes.

Documentação: [Tableau Semantics (Trailhead)](https://trailhead.salesforce.com/content/learn/modules/tableau-semantics/learn-the-basics-of-tableau-semantics)

### Vector DB

Banco vetorial integrado, que guarda embeddings para busca semântica e para fundamentar LLMs (RAG). Segundo a Salesforce, o Data 360 usa o índice vetorial Milvus no pipeline de dados não estruturados.

Documentação: [Data 360 – Features](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-features-overview.html)

### Unstructured

Suporte a texto, áudio, vídeo e imagens. Um pipeline faz parsing, pré-processamento, chunking, pós-processamento e embedding, para indexar o conteúdo por palavras-chave e por vetores.

Documentação: [Data 360 Architecture](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-architecture.html)

### Files/CMS

Armazenamento de arquivos e gestão de conteúdo (Salesforce CMS), para ativos e conteúdo de sites e portais. O diagrama lista a capacidade, mas a Salesforce não detalha a arquitetura física nesta página.

Documentação: [Salesforce CMS (ajuda)](https://help.salesforce.com/s/articleView?id=xcloud.cms_content_create_manage.htm&language=en_US&type=5)

### Search

Busca como serviço, baseada em Solr e estendida pela Salesforce, com vários clusters por região e ranking de relevância. Inclui busca híbrida e vetorial, usada em RAG e pesquisa agêntica.

Documentação: [Pesquisa (ajuda)](https://help.salesforce.com/s/articleView?id=sf.search_map.htm&language=en_US&type=5) · [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

### Analytic Pipeline

Ingestão e transformação de dados em lote, quase em tempo real e em tempo real (padrão ELT), para análise e IA. O Query Service usa Trino e Hyper para SQL, e o Spark atende processamento pesado.

Documentação: [Data 360 Features](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-features-overview.html)

## Metadata Framework

Núcleo conceitual da plataforma: a aplicação é descrita por metadados e materializada em tempo de execução.

### Metadata Framework

Abstração estável sobre a qual apps são construídos. Inclui um ORM com multitenancy embutido, ordem de execução prescrita e o runtime 'Core' que liga os metadados aos runtimes. Objetos, campos e regras são metadados. Analogia: o schema e o código vivem como dados de configuração, que o runtime interpreta.

Documentação: [Multitenant Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture) · [Architecture Basics](https://architect.salesforce.com/docs/architect/fundamentals/guide/architecture-basics) · [Metadata API](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_intro.htm)

## Hyperforce

Infraestrutura base, executada em provedores de nuvem pública. Para um dev back-end, é onde aparecem regiões, zonas, resiliência e custo.

### Availability/Reliability

Serviços críticos distribuídos por três zonas de disponibilidade, com failover automatizado, limites de raio de impacto (células) e rollbacks rápidos. Analogia: redundância multi-AZ e isolamento por célula.

Documentação: [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation) · [Trust (status)](https://trust.salesforce.com/)

### Security & Certifications

Zero Trust, criptografia ponta a ponta, mTLS entre serviços e adesão a mais de 40 padrões de conformidade, segundo a Salesforce. A segurança é aplicada pela infraestrutura, e não deixada a cada equipe.

Documentação: [Compliance](https://compliance.salesforce.com/) · [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

### Connectivity & Network

Rede com perímetro por região, gateways de entrada e saída, service mesh e políticas entre grupos de serviços. Endpoints dos clientes passam por domínios estáveis (My Domain), sem depender de IPs que mudam.

Documentação: [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation) · [My Domain (ajuda)](https://help.salesforce.com/s/articleView?id=sf.domain_name_overview.htm&language=en_US&type=5)

### Observability/Monitoring

Plataforma padrão de telemetria: métricas, logs, rastreamento distribuído e alertas, com AIOps para detectar e responder a incidentes. Analogia: observabilidade nativa (OpenTelemetry, APM) para todos os serviços.

Documentação: [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

### Operating Zones

Agrupam instâncias do Hyperforce para atender residência de dados e requisitos regulatórios por geografia ou ambiente. É como a plataforma cumpre exigências de onde os dados podem ficar.

Documentação: [Hyperforce (ajuda)](https://help.salesforce.com/s/articleView?id=xcloud.hf_introducing_hyperforce.htm&language=en_US&type=5) · [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

### Elastic Compute

Escalonamento automático de computação: sobe rápido e desce devagar, conforme CPU, memória e filas. Abstrai limites de conta do provedor de nuvem para que as equipes de serviço não os gerenciem à mão.

Documentação: [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

### Resource & Cost Management

Governança de custo (FinOps) em nuvem pública: contas hierárquicas, tags por serviço, planos de capacidade e métricas de custo unitário. Mostra que eficiência é requisito de engenharia, e não só de finanças.

Documentação: [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

### Control Plane

Conjunto de serviços redundantes que criam, gerenciam e monitoram instâncias do Hyperforce, incluindo pipelines de entrega contínua com artefatos assinados. Analogia: o plano de controle de um orquestrador de infraestrutura.

Documentação: [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

## Integrations (coluna lateral)

Pontos de conexão com o que está fora da Salesforce. A coluna atravessa várias camadas, porque integração acontece em todas elas.

### External UI/Dev Tools

Interfaces e ferramentas externas (front-ends próprios, IDEs, pipelines de CI/CD) que consomem as APIs da plataforma. Ligam-se a ela sem passar pela interface padrão da Salesforce.

Documentação: [API Library](https://developer.salesforce.com/docs/apis)

### 3rd-Party APIs

Chamadas a APIs externas a partir da plataforma (callouts) e o consumo de serviços de terceiros. No Apex, callouts têm limites e requerem credenciais e autenticação configuradas.

Documentação: [Apex Callouts](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts.htm)

### External Systems

Sistemas de fora, como ERPs, bancos de dados e legados, que trocam dados e eventos com a plataforma por APIs, eventos, ETL ou MuleSoft. Analogia: padrões de integração (síncrono, assíncrono, eventos).

Documentação: [Integration Patterns](https://architect.salesforce.com/docs/architect/fundamentals/guide/integration-patterns) · [MuleSoft](https://docs.mulesoft.com/general/)

### Other AI Models

Modelos de IA externos (de outros provedores ou próprios) acessíveis via AI Gateway. Permite escolher o modelo conforme custo, desempenho ou política, mantendo os controles do Trust Layer.

Documentação: [Modelos suportados](https://developer.salesforce.com/docs/ai/agentforce/guide/supported-models.html)

### Zero copy + data connectors

Federação de dados com sistemas externos (como Snowflake, BigQuery, Databricks e Redshift) sem copiar tudo para a Salesforce, mais conectores de ingestão. Analogia: consulta federada em vez de ETL pesado.

Documentação: [Data 360 Architecture](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-architecture.html) · [Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)

## Fontes principais

- [The Salesforce Platform – Transformed for Tomorrow](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation)
- [Platform Multitenant Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture)
- [Architecture Basics](https://architect.salesforce.com/docs/architect/fundamentals/guide/architecture-basics)
- [Salesforce Database (VLDB)](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)
