# Salesforce para desenvolvedores back-end

Roteiro de conversa orientado à leitura de documentação gerada a partir de um projeto Salesforce DX. A proposta é aproveitar o repertório de um desenvolvedor experiente, sem exigir familiaridade com Salesforce e sem confundir analogias didáticas com detalhes físicos que a fabricante não documenta.

**Verificação das fontes:** 11 de novembro de 2026. O escopo é o core da Salesforce Platform e suas integrações, não todos os produtos do portfólio Salesforce.

**Versão 2, revisão comparativa:** esta versão incorpora a leitura integral do anexo `Roteiro-Salesforce-para-dev-back-end.md`, fornecido como documento de origem dos trechos do repositório. O arquivo `leitura-critica-e-registro-de-mudancas.md` registra o que foi preservado, corrigido e complementado, inclusive limitações da primeira revisão.

## Como usar este material

- **Parte de consulta:** leia as verificações técnicas antes de apresentar. Elas corrigem generalizações do roteiro anterior e delimitam o que é confirmado, conceitual ou não confirmado.
- **Parte de apresentação:** use os onze blocos, de 0 a 10. Cada um contém objetivo, de três a cinco pontos principais, analogia back-end, desenho SVG e uma pergunta de fixação.
- **Fio condutor:** use um exemplo fictício: um cliente faz um `Pedido__c`, com `Valor__c`, `Status__c`, itens e integração com ERP. Os nomes das classes, flows e componentes propostos são ilustrativos, não componentes verificados na sua org.
- **SVGs:** os arquivos da pasta `svg/` são desenhos vetoriais independentes, com texto selecionável e descrições acessíveis. Eles representam modelos didáticos; não são diagramas físicos da infraestrutura Salesforce.
- **Duas velocidades:** os onze blocos são a condução da conversa; verificação técnica, exemplos de arquivos e aprofundamento são material de apoio. Não tente ler todas as ressalvas e todos os exemplos dentro do tempo do bloco.

## Cartão de condução da conversa

Use uma pergunta-guia por bloco. A tabela é um lembrete de apresentação; o detalhamento e as referências aparecem nas seções correspondentes.

| Bloco | Pergunta-guia | O que mostrar |
|---|---|---|
| 0 | Onde está cada responsabilidade? | Mapa das camadas, sem lista exaustiva de produtos. |
| 1 | O que é compartilhado e o que é isolado? | Prédio de orgs e orçamento de uma transação. |
| 2 | Qual é a diferença entre definição, representação e uso? | `Valor__c.field-meta.xml`, um registro e o caminho de implantação. |
| 3 | Como o pedido se relaciona ao cliente e aos itens? | Modelo lógico e uma consulta SOQL válida. |
| 4 | Quem pode operar, sobre quais registros e campos? | Interseção das permissões com o contexto do código. |
| 5 | O que realmente é promovido entre ambientes? | Árvore do projeto e pipeline. |
| 6 | O que acontece antes e depois do commit? | Linha do tempo; depois, o problema de uma query por registro. |
| 7 | Qual ferramenta torna esta regra mais previsível? | Flow, híbrido e Apex com responsabilidades claras. |
| 8 | A UI usa dados padronizados ou lógica customizada? | Dois caminhos: LDS/UI API e Apex. |
| 9 | Como integrar sem perder o controle das falhas? | Entrada, saída e eventos; timeout e idempotência. |
| 10 | O que a documentação prova e o que falta verificar? | Um rastro real e uma hipótese explicitamente marcada. |

## Verificação das cinco perguntas sobre a infraestrutura

### A Salesforce confirmou que abandonou Oracle no core?

**Resposta curta: há confirmação pública do SalesforceDB como banco transacional de CRM; não encontrei declaração pública suficiente para afirmar uma eliminação completa de Oracle em todo o core ou em todos os ambientes.** O guia oficial afirma que o SalesforceDB “handles all transactional CRM data”, mas não anuncia uma data de desligamento definitivo de Oracle nem apresenta um inventário de bancos por ambiente ([Salesforce Architects, transformação da plataforma](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)).

O uso histórico de Oracle é confirmado pelo anúncio de parceria de 25 de junho de 2013, que menciona Oracle Database, Exadata e implantação de Exadata nos data centers da Salesforce. Isso sustenta a distinção entre usar software Oracle na infraestrutura da Salesforce e hospedar necessariamente o CRM na Oracle Cloud ([anúncio oficial da parceria](https://www.salesforce.com/news/press-releases/2013/06/25/salesforce-com-and-oracle-announce-new-strategic-partnership/?bc=OTH)).

O paper de engenheiros da Salesforce publicado no PVLDB em 2026 descreve o SalesforceDB em produção, construído sobre PostgreSQL, com camada própria de armazenamento e acesso baseada em LSM. A migração de tenants discutida nesse paper é entre instâncias de SalesforceDB; ela não prova uma migração concluída de Oracle para SalesforceDB em toda a frota ([Salesforce Database: A Cloud-Native Multi-Tenant OLTP Database, pp. 4426–4431](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)).

**Fala recomendada:** “A Salesforce documenta hoje o SalesforceDB, baseado em PostgreSQL, como banco dos dados transacionais de CRM. O histórico de Oracle é real, mas não vou transformar isso numa afirmação de que a empresa deixou de usar Oracle em absolutamente todos os ambientes.” ([guia oficial](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html), [anúncio histórico](https://www.salesforce.com/news/press-releases/2013/06/25/salesforce-com-and-oracle-announce-new-strategic-partnership/?bc=OTH)).

### Os metadados das orgs também ficam no SalesforceDB?

**Resposta curta: a documentação consultada não confirma explicitamente o armazenamento de todos os metadados das orgs no SalesforceDB.** O guia identifica o Core runtime como o sistema de registro autoritativo dos metadados de aplicação, conectado a um banco relacional, e declara que o SalesforceDB guarda dados transacionais de CRM e metadados do Data 360 e serviços relacionados; não faz explicitamente a equivalência “todos os metadados de org = SalesforceDB” ([seções Metadata Framework e Transactional Database](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)).

A documentação de multitenancy descreve metadados e dados em um banco compartilhado, com um dicionário de metadados e caches. Essa descrição sustenta explicar a persistência e o runtime, mas não basta para nomear o banco atual de cada categoria de metadado sem uma ressalva ([Platform Multitenant Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html)).

**Fala recomendada:** “Os metadados ficam persistidos na plataforma e alimentam seus runtimes e caches. O Core é a referência autoritativa dos metadados de aplicação; o mapeamento físico completo desses metadados para bancos e serviços não está explicitado nas fontes que consultei.” ([Salesforce Architects](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)).

### A tabela genérica com slots continua válida no SalesforceDB?

**Resposta curta: é um modelo conceitual oficial ainda publicado; a preservação exata de `MT_Data`, `Value0…N` e seus detalhes físicos no SalesforceDB não está confirmada.** A página de arquitetura apresenta `MT_Objects`, `MT_Fields`, `MT_Data`, flex columns e tabelas auxiliares de índice e relacionamento ([modelo de multitenancy](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html)).

O paper de 2026 confirma shared-table multitenancy, esquema físico compartilhado entre tenants e isolamento com predicados de tenant. Ele não especifica os nomes `MT_Data`/`ValueN` nem o mapeamento completo dos objetos Salesforce para essas tabelas no SalesforceDB ([paper do SalesforceDB, pp. 4427 e 4430–4431](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)).

**Fala recomendada:** “Criar um campo lógico não significa criar uma coluna física exclusiva da minha org. A arquitetura publicada explica isso com um dicionário e campos genéricos; vou usar esse desenho como modelo conceitual, não como uma fotografia do esquema atual do SalesforceDB.” ([arquitetura oficial](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html), [paper técnico](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)).

Evite concluir que “o schema físico nunca muda”: o próprio guia descreve atualizações de schema do SalesforceDB, inclusive três grandes atualizações anuais e outras menores. A distinção correta é entre evolução física administrada pela plataforma e personalização lógica administrada pelo cliente ([SalesforceDB no guia de transformação](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)).

### Account tem uma tabela física própria?

**Resposta curta: não há base suficiente nas fontes consultadas para afirmar nem uma tabela física exclusiva de Account nem que todo o seu conteúdo usa exatamente os mesmos slots descritos para o modelo genérico.** A página de multitenancy inclusive usa Account e Case como exemplos na explicação de `MT_Data`, mas não entrega um catálogo físico separado por objetos standard e custom ([passagem sobre MT_Data](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html)).

O paper atual confirma múltiplas tabelas com dados de múltiplos tenants, mas não revela o mapeamento físico de Account. Portanto, retire a suposição anterior de que “standard provavelmente tem tabela própria” e também não a substitua pela certeza oposta ([SalesforceDB, pp. 4427 e 4430](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)).

**Fala recomendada:** “Account é um objeto lógico exposto pela plataforma. Para desenvolver, usamos seu contrato de objeto e APIs; sua tabela física interna não é um contrato público descrito nessas fontes.” ([arquitetura multitenant](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html), [paper técnico](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)).

### Os limites continuam os mesmos?

**Quase todos os números apresentados continuam válidos, mas o heap mudou no Winter ’27.** A tabela abaixo se refere aos limites gerais por transação Apex, não a toda chamada de API nem a todas as exceções e limites de namespaces de pacotes certificados ([Execution Governors and Limits](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)).

| Recurso | Síncrono | Assíncrono usual | Como explicar |
|---|---:|---:|---|
| Consultas SOQL | 100 | 200 | Quantidade de consultas, não de registros; há exceções, como Custom Metadata em determinadas condições ([referência Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)). |
| Registros consultados por SOQL | 50.000 | 50.000 | Não confundir com o alcance de um QueryLocator de Batch Apex ([referência Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)). |
| Instruções DML | 150 | 150 | Uma instrução pode processar uma coleção de registros ([referência Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)). |
| Registros processados por DML | 10.000 | 10.000 | É um orçamento diferente do número de instruções ([referência Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)). |
| CPU | 10.000 ms | 60.000 ms | CPU não equivale ao tempo total de relógio da requisição ([referência Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)). |
| Heap no Winter ’27 | **10 MB** | **25 MB** | Antes: 6 MB e 12 MB; confirme o ambiente com `Limits.getLimitHeapSize()` ([release note oficial](https://help.salesforce.com/s/articleView?id=release-notes.rn_apex_heap_limit.htm&language=en_US&type=5)). |
| Callouts | 100 | 100 | Por transação; o orçamento não é reiniciado para cada classe ([referência Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)). |
| Tempo acumulado de callouts | 120 s | 120 s | Não são 120 s para cada uma de 100 chamadas ([limites de callout](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-callouts-timeouts.html)). |
| Timeout de uma chamada | Padrão de 10 s; configurável até 120 s | Mesma regra | O máximo individual não elimina o teto acumulado da transação ([limites de callout](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-callouts-timeouts.html)). |

- **Assíncrono não é uma categoria uniforme:** Scheduled Apex usa limites síncronos; no Batch Apex os limites são reiniciados a cada execução de `execute`. Evite a frase “tudo que é assíncrono ganha todos os limites maiores” ([referência Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)).
- **Heap em transição:** orgs não produtivas no Winter ’27 podem temporariamente aplicar o limite do Summer ’26 por uma configuração de compatibilidade; a documentação prevê a imposição global dos limites maiores no Spring ’27. Não confunda o heap com o limite separado de tamanho de request/response de callout, ainda listado como 6/12 MB ([release note](https://help.salesforce.com/s/articleView?id=release-notes.rn_apex_heap_limit.htm&language=en_US&type=5), [tabela de limites estáticos](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)).
- **Cobertura padrão:** para os cenários usuais com todos os testes locais, a referência exige cobertura agregada de ao menos 75% e alguma cobertura de cada trigger; não significa 75% individual para toda classe. Com `RunSpecifiedTests`, cada classe e trigger implantados deve atingir pelo menos 75% com os testes executados ([requisitos de cobertura](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-testing-intro.html), [regra de testes especificados](https://developer.salesforce.com/docs/platform/api-metadata/guide/meta-deploy-run-specific-tests.html)).
- **Testes no deploy:** “todo deploy em produção roda testes” é amplo demais; pela regra moderna padrão, a presença de classes ou triggers Apex faz diferença, e o `testLevel` pode alterar a seleção. Declare o nível de testes no pipeline em vez de depender de uma generalização ([testes em sandbox e produção](https://developer.salesforce.com/docs/platform/api-metadata/guide/meta-deploy-run-local-tests.html)).

## Outras correções importantes para o bloco de metadados

- **Nem todo artefato é XML:** metadados descrevem o comportamento da aplicação, mas o projeto inclui código Apex, HTML, JavaScript, CSS e outros recursos, além dos descritores XML. Source format e Metadata API format também não são exatamente a mesma organização de arquivos ([estrutura Salesforce DX](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html)).
- **XML não é o runtime:** deploy/retrieve movem representações de metadados; o runtime usa a configuração persistida e suas representações de execução e cache. Não descreva todo deploy como “converter todo arquivo em uma linha de tabela”, pois há artefatos de código e diferentes tipos de componentes ([Metadata API](https://developer.salesforce.com/docs/platform/api-metadata/guide/file-based.html), [runtime e caches](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html)).
- **O browser não “só renderiza”:** ele também executa JavaScript, mantém estado e participa do cache e da reatividade dos LWC; as operações protegidas de dados e regras server-side continuam na plataforma. `@wire` não significa sempre LDS, pois também pode chamar Apex cacheável ([wire com Apex](https://developer.salesforce.com/docs/platform/lwc/guide/apex-wire-method), [cache de resultados Apex](https://developer.salesforce.com/docs/platform/lwc/guide/apex-result-caching.html)).
- **Caches de metadados não são sinônimo de Vegacache:** o guia descreve caches locais dos serviços e, separadamente, Vegacache baseado em Redis, inclusive para objetos Apex e resultados de SOQL. Não há suporte nessa fonte para dizer que todo metadado de org passa especificamente pelo Vegacache ([Metadata Framework e Caching Service](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)).
- **Setup, Metadata API e Tooling API não são três caminhos exaustivos e equivalentes:** são bons exemplos; Tooling cobre tipos e operações específicos e oferece REST e SOAP, não somente JSON. A interface Setup também não documenta ao cliente seu formato de persistência ou todo o transporte interno ([Tooling API](https://developer.salesforce.com/docs/platform/api-tooling/guide/intro-api-tooling.html), [Metadata API](https://developer.salesforce.com/docs/platform/api-metadata/guide/file-based.html)).
- **Dados podem viajar em XML:** a distinção é “Account não é um arquivo de configuração da Metadata API”, não “dados nunca usam XML”. SOAP API de dados usa XML, e REST também pode oferecer XML; formato de transporte e natureza do recurso são eixos diferentes ([visão oficial das APIs](https://trailhead.salesforce.com/content/learn/modules/api_basics/api_basics_overview)).
- **Custom Metadata não é leitura sem limites:** em Apex, consultas usuais são isentas do contador SOQL, mas consultas com Long Text Area e consultas em Flow contam para os limites; a documentação também lista 50.000 registros retornados por transação. Não aceita DML comum; criação/atualização via Apex Metadata tem restrições de visibilidade e controle do componente ([limites de Custom Metadata](https://help.salesforce.com/s/articleView?id=platform.custommetadatatypes_limits.htm&language=en_US&type=5), [operações permitidas](https://developer.salesforce.com/docs/atlas.en-us.244.0.api_meta.meta/api_meta/meta_custommetadatatypes.htm)).
- **Record-Triggered Flow não é sempre a mesma transação:** o caminho imediato participa do salvamento; caminhos assíncronos ocorrem depois do commit em outra transação. Uma falha posterior não desfaz o salvamento já confirmado ([guia de automação](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered), [order of execution](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)).
- **DML agrupado não significa DML único:** Unit of Work registra mudanças e organiza operações bulkificadas, possivelmente para diferentes objetos; `commitWork()` executa esse trabalho, mas não é o commit definitivo da transação Salesforce. Uma falha posterior na mesma transação ainda pode desfazer essas alterações ([Unit of Work no Trailhead](https://trailhead.salesforce.com/content/learn/modules/apex_patterns_sl/apex_patterns_sl_learn_uow_principles), [fronteira oficial de commit](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)).
- **Automação sem suporte ainda importa para a investigação:** Workflow Rules e Process Builder estão sem suporte desde 31/12/2025, mas automações ativas podem continuar executando. Elas não devem desaparecer da análise só porque a recomendação de novos desenvolvimentos é Flow ([fim de suporte oficial](https://help.salesforce.com/s/articleView?id=001096524&language=en_US&type=1)).
- **Callout e DML:** não faça callout mantendo trabalho não confirmado pendente; ao manter as gravações, separe o processamento externo em outra transação quando necessário. Há um caso avançado documentado de rollback do trabalho e liberação dos savepoints antes do callout; isso não confirma nem preserva as gravações revertidas e não é um “commit manual” em Apex ([Transaction Control](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/langcon-apex-transaction-control.html)).

## Melhorias didáticas para um desenvolvedor experiente

Minha recomendação é priorizar o contrato da plataforma antes de discutir sua implementação física. O interlocutor já conhece banco, APIs e transações; o objetivo não é ensinar esses conceitos novamente, mas mostrar onde Salesforce reaproveita seu repertório e onde muda as regras.

- **Começar por uma requisição concreta:** apresente “salvar um pedido” e retome a pergunta em cada camada: quem executa, com quais permissões, em qual transação e com qual orçamento?
- **Abrir a documentação cedo:** escolha um campo ou flow real no início. Deixe claro quando a explicação passa de evidência da org para um exemplo fictício.
- **Separar quatro planos:** fonte no Git; configuração implantada; execução/transação; infraestrutura física. Misturar esses planos é a principal fonte de confusão sobre XML, Apex e banco.
- **Dosar vocabulário:** diga primeiro a função, depois o nome Salesforce: “permissão de campo, chamada FLS”; “fila de trabalho, aqui Queueable”.
- **Comparar limites de transação com quotas de serviço:** um método isolado não ganha novo orçamento por existir em outra classe. Faça o aluno estimar uma consulta por item antes de apresentar bulkification.
- **Separar evidência e hipótese:** uma referência literal num flow é diferente de supor uma ligação porque duas classes têm nomes parecidos. Na documentação, marque a proveniência e o grau de confirmação.
- **Reservar detalhes avançados:** fflib, LSM, diferenças entre bancos e todas as famílias de API são aprofundamentos, não pré-requisitos para entender a org.
- **Fechar cada bloco com recuperação ativa:** peça que o desenvolvedor explique uma consequência em suas palavras. Se não conseguir, volte ao desenho, não acrescente mais siglas.

## Roteiro completo

### Abertura: enxergar a aplicação, não apenas o CRM

Bloco 0, duração de 3 minutos. Objetivo: localizar dados, lógica, interface, segurança e integração no mesmo mapa.

- **Plataforma de aplicações:** apresente a org como um ambiente lógico de aplicação configurável, não como uma VM com um executável instalado pelo cliente ([arquitetura multitenant](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html)).
- **Metadados e dados:** use “configuração e componentes são representados por metadados; os pedidos concretos são dados”. Evite “tudo é XML” e restrinja o mapa ao core discutido ([arquitetura da plataforma](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html), [source format](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html)).
- **Camadas conectadas:** interface usa serviços e objetos; segurança atravessa essas operações; APIs e eventos conectam a outros sistemas. A plataforma combina um Core com diversos serviços, não apenas um processo monolítico ([transformação da plataforma](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)).
- **Âncora prática:** proponha “salvar `Pedido__c` e enviá-lo ao ERP”. Mostre onde cada parte aparecerá na documentação e avise que o exemplo é fictício.

Analogia back-end: imagine um application server gerenciado, com ORM, autorização, APIs e mecanismos de execução oferecidos pela plataforma. A analogia ajuda a distribuir responsabilidades; não significa que você tenha acesso ao sistema operacional ou ao SQL interno.

Desenho de lousa: três faixas, “Front-end”, “Lógica” e “Dados”, com “Segurança” atravessando o conjunto e “Integração” na lateral. Desenhe primeiro as faixas e só depois acrescente os exemplos verbalmente.

![Mapa das camadas da org](svg/bloco-00-camadas.svg)

Pergunta de fixação: “O pedido de número 123 e a definição do campo Valor são a mesma categoria de coisa?” Transição: “Agora vamos entender como esse ambiente pode compartilhar infraestrutura sem virar uma aplicação misturada com a de outros clientes.”

### Multi-tenancy: isolamento lógico e orçamento de recursos

Bloco 1, duração de 6 minutos. Objetivo: entender por que o tenant é lógico e por que limites influenciam o desenho do código.

- **Org como tenant:** use a identificação da organização como contexto de isolamento, sem imaginar um servidor exclusivo para cada org. O prefixo `00D` identifica Organization; dados e metadados tenant-specific coexistem com recursos compartilhados ([prefixos oficiais](https://help.salesforce.com/s/articleView?id=000385203&language=en_US&type=1), [arquitetura multitenant](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html)).
- **Isolamento além de uma coluna:** o modelo usa identificadores e predicados de tenant; o SalesforceDB verifica esses predicados quando há contexto de tenant na sessão. Isso não deve ser ensinado como “o desenvolvedor lembra de colocar WHERE OrgId” ([SalesforceDB, p. 4430](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)).
- **Governors por transação:** consultas, DML, CPU e heap limitam o trabalho acumulado; limites diários e de org são outra categoria. Abrir outra classe não reinicia o contador ([limites Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)).
- **Infraestrutura e releases gerenciadas:** Hyperforce organiza serviços em células, e a plataforma tem três releases sazonais anuais: Spring, Summer e Winter. Não trate célula como servidor físico nem confunda upgrade automático da plataforma com ausência de versionamento de API nos componentes ([guia de transformação](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html), [processo de releases](https://trailhead.salesforce.com/content/learn/modules/sf_releases/sf_releases_start), [segurança por versão de API](https://developer.salesforce.com/docs/platform/lwc/guide/apex-security)).

Analogia back-end: SaaS multi-tenant com isolamento de contexto e quotas de execução, não apenas rate limiting HTTP. O prédio de apartamentos continua útil: há áreas e serviços compartilhados, mas identificação, autorização e controle de consumo não dependem de cada morador lembrar de se comportar.

Desenho de lousa: um prédio com dois apartamentos, “Org A” e “Org B”, dentro de uma área compartilhada. Na base, escreva “quotas por transação”.

![Orgs em infraestrutura compartilhada](svg/bloco-01-multitenancy.svg)

Pergunta de fixação: “Se o trigger chamar mais três classes, quantos novos orçamentos de SOQL ele ganhou?” Transição: “Como cada apartamento pode ter campos e comportamentos diferentes sem uma cópia completa da aplicação?”

### Metadados, fonte e runtime: o que realmente é executado

Bloco 2, duração de 10 minutos. Objetivo: separar o projeto local, o processo de implantação e o uso da org.

- **Fonte não é execução:** o projeto contém representações de componentes; o deploy valida e implanta essas definições, enquanto o runtime usa a configuração persistida e representações preparadas pela plataforma. A org não relê sua pasta local a cada requisição ([Metadata API](https://developer.salesforce.com/docs/platform/api-metadata/guide/file-based.html), [runtime multitenant](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html)).
- **Metadados não são só XML:** campos, layouts e flows têm descritores; Apex, LWC e recursos incluem outros arquivos. `package.xml` seleciona tipos e membros para operações baseadas em manifesto; não é um retrato automático e completo da org ([source format](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html), [retrieve com manifesto](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-ws-create-from-existing.html)).
- **Modelo conceitual interno:** o dicionário descreve objetos/campos, e tabelas compartilhadas armazenam conteúdo; slots explicam a virtualização do esquema. Apresente `MT_Objects`, `MT_Fields` e `ValueN` como arquitetura publicada, sem garantir identidade física no SalesforceDB atual ([modelo oficial](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html), [shared-table no SalesforceDB](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)).
- **Runtime distribuído e cliente ativo:** o Core é referência autoritativa para metadados de aplicação e serviços mantêm caches locais; o browser executa LWC e consulta serviços. Não diga “todos os metadados estão no Redis” nem “o browser só desenha” ([Metadata Framework e Vegacache](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html), [wire Apex](https://developer.salesforce.com/docs/platform/lwc/guide/apex-wire-method)).
- **Org bananinha:** classifique três exemplos: registro `Config_Frete__mdt` como metadado; registro Account como dado; definição de Flow como metadado e sua execução como trabalho transacional. Acrescente as exceções de limites do Custom Metadata e os caminhos pós-commit do Flow ([Custom Metadata](https://developer.salesforce.com/docs/atlas.en-us.244.0.api_meta.meta/api_meta/meta_custommetadatatypes.htm), [limites](https://help.salesforce.com/s/articleView?id=platform.custommetadatatypes_limits.htm&language=en_US&type=5), [order of execution](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)).

Analogia back-end: fonte e descritores entram num processo de implantação; a aplicação em execução usa estado implantado, artefatos de execução e caches, não o checkout do desenvolvedor. A “planta da casa” funciona se você completar: a casa continua usando configuração e regras, só não consulta sua cópia local da planta.

Reformulação da frase original: “O projeto contém uma representação das definições. O deploy implanta essas definições. A org usa os metadados implantados continuamente; ela não consulta o meu checkout para funcionar.” Evite “ninguém mais consulta a planta”, porque isso pode sugerir que os metadados deixam de participar da execução.

Fala sugerida: “O XML é uma representação usada para transportar muitas definições. Na org, essas definições persistidas orientam o comportamento da plataforma; quando salvo um pedido, não estou executando o XML do meu notebook.”

Desenho de lousa: separe visualmente “implantação” e “uso”. Na primeira linha, projeto → deploy → configuração; na segunda, configuração → runtime → browser.

![Implantação e uso dos metadados](svg/bloco-02-metadados-runtime.svg)

Distribuição sugerida: 2 minutos para fonte/deploy; 3 para runtime; 3 para a bananinha; 2 para a pergunta e a documentação. Deixe LSM e história dos bancos para a seção opcional ao final.

Pergunta de fixação: “Apaguei o projeto local depois do deploy. A org para? Se eu alterar a configuração pelo Setup, o Git fica atualizado sozinho?” Transição: “Agora vamos olhar o contrato de dados que essa configuração expõe.”

### Modelo de dados: um contrato lógico com relacionamentos

Bloco 3, duração de 8 minutos. Objetivo: ler objetos, campos e relações sem pressupor acesso ao esquema físico.

- **Objetos e campos:** apresente standard e custom; no exemplo, `Pedido__c` e `Valor__c` são nomes custom. O projeto decompõe definições de objetos em subdiretórios, o que ajuda a localizar campos e outros componentes ([source format](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html)).
- **Identidade não é chave de negócio:** IDs de registros têm representações de 15 caracteres, case-sensitive, ou 18, case-safe; prefixos como `001` e `003` identificam Account e Contact. Diferencie esse identificador do número de pedido do ERP e proponha uma chave externa para correlação/idempotência ([formatos de ID](https://help.salesforce.com/s/articleView?id=000383751&language=en_US&type=1), [prefixos oficiais](https://help.salesforce.com/s/articleView?id=000385203&language=en_US&type=1)).
- **Lookup e master-detail:** use lookup para a associação do pedido ao cliente e master-detail entre item e pedido, se o ciclo de vida exigir dependência, herança de acesso e agregação. Não apresente todo lookup como obrigatoriamente opcional; confira as propriedades efetivas na definição do campo ([relacionamentos de objetos](https://help.salesforce.com/s/articleView?id=overview_of_custom_object_relationships.htm&language=en_US)).
- **SOQL navega relações:** ele permite percorrer relações parent-to-child e child-to-parent, mas não JOIN arbitrário como SQL. Mostre uma consulta coerente com o objeto de origem, sem `Account.Name` diretamente num `FROM Account` ([Relationship Queries](https://developer.salesforce.com/docs/platform/salesforce-soql-sosl/guide/sforce-api-calls-soql-relationships.html), [nomes de relacionamento](https://developer.salesforce.com/docs/platform/salesforce-soql-sosl/guide/sforce-api-calls-soql-relationships-understanding.html)).
- **Variação e regra:** apresente Record Types, picklists, fórmulas e validações como partes diferentes do contrato lógico. Record Types diferenciam processos, valores de picklist e layouts, mas não devem ser usados como mecanismo de controle de leitura de registros ([RecordType na Metadata API](https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-recordtype.html)).

Analogia back-end: um modelo de domínio exposto por um ORM e por APIs, com constraints e relações administradas pela plataforma. O sObject é a entidade lógica que seu código manipula, não uma prova sobre a tabela física interna.

Exemplos didáticos de SOQL, usando as relações standard documentadas:

```sql
SELECT Id, Name, (SELECT Id, LastName FROM Contacts)
FROM Account
```

```sql
SELECT Id, LastName, Account.Name
FROM Contact
```

O primeiro vai de pai para filhos; o segundo vai de filho para pai. Para relações custom, o nome de navegação precisa corresponder à definição do relacionamento, não a um plural inventado ([Understanding Relationship Names](https://developer.salesforce.com/docs/platform/salesforce-soql-sosl/guide/sforce-api-calls-soql-relationships-understanding.html)).

Desenho de lousa: Account → Pedido → Item, indicando o sentido “o filho referencia o pai” e diferenciando lookup de master-detail. O desenho representa uma proposta para o exemplo, não um relacionamento standard pré-existente.

![Modelo lógico do pedido](svg/bloco-03-modelo-dados.svg)

Pergunta de fixação: “Se o pedido for excluído, o que você quer que aconteça com seus itens? Isso é a mesma pergunta que saber quem pode ler Valor?” Transição: “O schema diz o que existe; agora precisamos saber quem pode fazer o quê.”

### Segurança: capacidade, registros e contexto de execução

Bloco 4, duração de 8 minutos. Objetivo: distinguir CRUD/FLS, acesso a registros e comportamento do código.

- **Objeto e campo:** explique CRUD como capacidade de operar sobre um tipo de objeto, e FLS como acesso a seus campos. Recomende ler concessões de acesso em conjunto, não concluir tudo a partir de um único arquivo de Profile ([modelo de segurança Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-security-sharing-chapter.html)).
- **Registros:** apresente OWD como base de compartilhamento, e hierarquia/regras como mecanismos de acesso a registros. Não desenhe a hierarquia de cargos como se fosse uma permissão de campo nem como um organograma obrigatório da empresa ([compartilhamento e demais camadas](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-security-sharing-chapter.html)).
- **Profiles e Permission Sets:** proponha uma leitura orientada a concessões: o que este usuário pode fazer por suas atribuições? Permission Sets e grupos são a abordagem recomendada para organizar permissões; destaque também que permissões privilegiadas como View All/Modify All podem ultrapassar o compartilhamento comum ([gerenciamento de permissões](https://trailhead.salesforce.com/content/learn/modules/data_security/data_security_objects), [permissões de objeto](https://help.salesforce.com/s/articleView?id=sf.users_profiles_object_perms.htm&language=en_US&type=5)).
- **Código e versão de API:** `with sharing` trata registros, não substitui CRUD/FLS. A documentação atual distingue Apex em API 67.0+ com user mode por padrão do comportamento anterior em API 66.0 e anteriores; leia o `apiVersion` antes de aplicar uma regra memorizada ([Secure Apex Classes](https://developer.salesforce.com/docs/platform/lwc/guide/apex-security)).
- **Intenção explícita:** prefira declarar sharing e modo das operações; `WITH USER_MODE` expressa o contexto de consulta, enquanto DML também precisa de tratamento coerente. `stripInaccessible()` é uma alternativa para degradação controlada, não um passe livre para ignorar segurança ([Secure Apex Classes](https://developer.salesforce.com/docs/platform/lwc/guide/apex-security)).

Analogia back-end: autorização por capacidade combinada com row-level security e políticas de campo. O equivalente prático é perguntar “qual operação?”, “sobre quais linhas?” e “em qual contexto?”, em vez de presumir que autenticar um usuário resolve tudo.

Desenho de lousa: desenhe duas entradas que precisam se encontrar: “CRUD + FLS” e “registros permitidos”. A saída é “operação autorizada”; escreva abaixo “contexto do código explícito”.

![Interseção das camadas de segurança](svg/bloco-04-seguranca.svg)

Pergunta de fixação: “Uma classe `with sharing` pode, só por essa palavra-chave, garantir que um campo sensível nunca seja lido?” Transição: “Agora vamos ver como essa configuração e esse código chegam a um ambiente.”

### Ambientes, projeto e implantação: o que entra no pipeline

Bloco 5, duração de 8 minutos. Objetivo: relacionar diretórios, ambientes e critérios de promoção.

- **Ambientes com finalidades diferentes:** apresente produção, sandbox e scratch org como escolhas de desenvolvimento e validação; não como cópias equivalentes de dados, configuração, duração ou licenças.
- **Projeto DX:** `sfdx-project.json` descreve o projeto e seus package directories; `force-app/main/default` é uma estrutura comum, não o único caminho possível. Objetos podem estar decompostos em campos, record types e outros arquivos ([estrutura DX](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html), [projeto a partir de fonte existente](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-ws-create-from-existing.html)).
- **Retrieve e deploy:** um traz componentes para o projeto e o outro aplica componentes na org; o manifesto seleciona escopo. Isso não deve ser confundido com transportar todos os registros de negócio ([Metadata API](https://developer.salesforce.com/docs/platform/api-metadata/guide/file-based.html), [retrieve com manifesto](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-ws-create-from-existing.html)).
- **Qualidade e cobertura:** mantenha o mínimo de 75% com as distinções entre agregado e `RunSpecifiedTests`; cobertura é um gate, não uma medida suficiente de qualidade. Configure o nível de testes e acrescente assertions de negócio e cenários negativos ([testes específicos](https://developer.salesforce.com/docs/platform/api-metadata/guide/meta-deploy-run-specific-tests.html), [testes por ambiente](https://developer.salesforce.com/docs/platform/api-metadata/guide/meta-deploy-run-local-tests.html)).
- **Entrega e configuração operacional:** apresente CI/CD e packages como estratégias de distribuição e promoção; registre tarefas pós-deploy e segredos fora do repositório. Named/External Credentials têm configuração e credenciais de usuário com papéis diferentes, incluindo armazenamento criptografado de tokens ([credenciais](https://developer.salesforce.com/docs/platform/named-credentials/guide/get-started.html)).

Analogia back-end: entrega de uma aplicação gerenciada, com fontes, configuração e migração de definições validadas no destino. `kubectl apply` ajuda apenas como analogia de aplicação declarativa; não é a semântica literal de deploy Salesforce.

Desenho de lousa: Git → validação/testes → QA/UAT → produção. Faça uma pergunta em cada seta: “o que mudou?”, “qual teste prova?”, “qual configuração depende do ambiente?”

![Pipeline de entrega](svg/bloco-05-deploy.svg)

Pergunta de fixação: “Implantar o objeto Pedido implica levar os pedidos reais da produção?” Transição: “Vamos entrar na execução de uma dessas regras, agora em Apex.”

### Apex e transação: programar para coleções e efeitos encadeados

Bloco 6, duração de 10 minutos. Objetivo: entender o ciclo de salvamento, os limites compartilhados e a organização do código.

- **Apex e triggers:** apresente Apex como a linguagem server-side da plataforma e triggers como pontos de entrada do ciclo de dados. Um trigger pode receber um lote de até 200 registros; isso não significa que todo carregamento de milhares de registros aconteça em uma única transação ([limites Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)).
- **Order of execution:** a versão resumida correta é before-save Flow → before Apex → validações → gravação ainda não confirmada → after Apex → demais etapas/after-save Flow → commit → pós-commit. É um recorte: há regras de duplicidade, atribuição, workflows, rollups e possíveis reentradas entre etapas ([sequência oficial](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)).
- **Bulkification:** colete IDs, consulte em conjunto, use Map/Set e faça DML com coleções; o anti-pattern é uma operação de banco por item que consome o orçamento. Flow e Apex no caminho síncrono também contribuem para a carga da transação ([limites](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html), [guia de automação](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered)).
- **Organização do código:** proponha um trigger fino e um handler; acrescente Service para casos de uso e Selector para consultas quando ajudarem. Domain e Unit of Work são opções de desenho, e fflib é uma implementação open source, não exigência nativa nem garantia de “um único DML para tudo”; `commitWork()` tampouco substitui o commit final da transação ([Unit of Work no Trailhead](https://trailhead.salesforce.com/content/learn/modules/apex_patterns_sl/apex_patterns_sl_learn_uow_principles), [order of execution](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)).
- **Assíncrono e testes:** explique Queueable, Batch e Schedulable por finalidade, sem uma aula de todas as APIs. Use assertions de resultado, execução em lote, falhas e mocks de callout; uma transação posterior não está dentro do rollback do salvamento original ([pós-commit](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html), [limites e contextos](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)).

Analogia back-end: um pipeline transacional que aciona regras e serviços, com ORM e quotas, mas sem a liberdade de instalar seu próprio runtime. Não iguale trigger Apex a uma stored procedure que você gerencia diretamente no banco.

Exercício oral: com 200 pedidos, uma query por pedido pede 200 queries antes de considerar as outras automações. Compare isso com uma consulta em conjunto e a montagem de um mapa; no contexto síncrono usual, 200 excede o limite de 100 ([limites de consultas](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)).

Desenho de lousa: uma linha do tempo com before-save Flow, before Apex/validações, after Apex/Flow, commit e trabalho assíncrono. Circule tudo que vem antes do commit como uma fronteira transacional; avise que o desenho omite etapas intermediárias.

![Fronteira da transação e pós-commit](svg/bloco-06-transacao.svg)

Distribuição sugerida: 3 minutos para transação; 3 para bulkification; 2 para padrões; 2 para assíncrono e pergunta. fflib detalhado fica para uma conversa posterior.

Pergunta de fixação: “After-save significa que o commit já aconteceu? Se o job de ERP falhar depois do commit, ele apaga o pedido?” Transição: “Nem toda regra exige uma classe; precisamos escolher onde implementar cada parte.”

### Flow ou código: escolher pela forma do problema

Bloco 7, duração de 6 minutos. Objetivo: decidir por complexidade, volume, governança e transação, não por slogan.

- **Flow como implementação:** é lógica de aplicação versionável em metadados, não apenas “um desenho que não é código”. Ele precisa de critérios de entrada, gestão de versões e testes; Workflow Rules/Process Builder sem suporte ainda podem executar e precisam ser reconhecidos na documentação da base existente ([guia de automação](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered), [fim de suporte](https://help.salesforce.com/s/articleView?id=001096524&language=en_US&type=1)).
- **Mesmo registro:** before-save Flow é uma opção eficiente para atualizar campos do registro que iniciou o processo; evita DML adicional para essa atualização. Before-context Apex também pode resolver esse tipo de necessidade ([guia de automação](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered)).
- **Escolha contextual:** Flow para orquestração simples; Apex para maior densidade, algoritmos, controle e volumes complexos; combinação com Invocable Apex quando há um bom contrato entre orquestração e cálculo. Não ensine “integração sempre exige Apex” ([decisão Flow/Apex](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered)).
- **Coexistência governada:** procure um ponto principal de entrada e responsabilidades claras por objeto; evite efeitos duplicados e recursão entre automações independentes. Volume, dependências e capacidade de manutenção importam mais do que contar blocos visuais ([guia de automação](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered)).

Analogia back-end: motor de workflow e serviços de domínio cooperando por contratos claros. A pergunta não é “visual ou profissional?”, mas “qual mecanismo deixa esse comportamento mais previsível, testável e operável?”

Desenho de lousa: três colunas, “Flow”, “Flow + Apex” e “Apex”, ao longo de um eixo de complexidade e controle. Diga explicitamente que não é uma régua automática nem uma hierarquia de qualidade.

![Escolha entre Flow, híbrido e Apex](svg/bloco-07-flow-apex.svg)

Pergunta de fixação: “A regra é simples, mas executa em massa e atualiza vários objetos. O fato de caber num Flow decide a arquitetura?” Transição: “Agora vamos ver quem chama essa lógica a partir da interface.”

### Front-end: componentes e caminhos de acesso a dados

Bloco 8, duração de 8 minutos. Objetivo: entender como a UI se conecta ao modelo e ao back-end.

- **Componentes e composição:** apresente LWC como a abordagem de componentes web; Aura e Visualforce ajudam a reconhecer a base existente. Lightning Pages organizam a composição da experiência; isso não elimina o JavaScript dos componentes ([estrutura de componentes no projeto](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html)).
- **LDS/UI API:** prefira recursos de dados da plataforma para operações suportadas; LDS trata sharing, CRUD e FLS. Isso não transfere automaticamente a mesma garantia para qualquer método Apex customizado ([segurança e LDS](https://developer.salesforce.com/docs/platform/lwc/guide/apex-security)).
- **Apex exposto à UI:** `@AuraEnabled` permite chamar métodos Apex; `@wire` com Apex exige `cacheable=true` e é para leitura sem mutação. Chamadas imperativas atendem operações comandadas e outros cenários ([wire Apex](https://developer.salesforce.com/docs/platform/lwc/guide/apex-wire-method), [cache Apex](https://developer.salesforce.com/docs/platform/lwc/guide/apex-result-caching.html)).
- **Estado e cache:** cache cliente existe; dados provisionados por Apex não são gerenciados automaticamente como se fossem todos LDS. Ensine `refreshApex()` e notificações de atualização como mecanismos a avaliar, não “recarregue tudo” ([Client-Side Caching](https://developer.salesforce.com/docs/platform/lwc/guide/apex-result-caching.html)).
- **Comunicação:** explique propriedades públicas, eventos e mensageria entre componentes por necessidade; deixe `@api`, CustomEvent e LMS como termos de reconhecimento. Na documentação, investigue quem contém o componente e quais métodos ele realmente importa/chama.

Analogia back-end: uma UI de componentes que pode consumir um serviço de dados padronizado ou um método de aplicação customizado. Classes `@AuraEnabled` lembram um BFF, mas não são automaticamente endpoints REST públicos.

Desenho de lousa: LWC tem dois caminhos: LDS/UI API e Apex; ambos chegam a dados protegidos da org. Identifique no desenho o caminho padronizado e o customizado.

![Dois caminhos de dados da UI](svg/bloco-08-frontend.svg)

Pergunta de fixação: “Se o método está marcado com `@AuraEnabled`, ele ganhou autorização de negócio e FLS automaticamente em qualquer versão e contexto?” Transição: “O outro consumidor desses serviços pode estar fora da Salesforce.”

### Integração: separar chamadas, eventos e credenciais

Bloco 9, duração de 10 minutos. Objetivo: escolher mecanismos por contrato e confiabilidade, sem decorar uma lista de APIs.

- **Entrada por contrato:** apresente REST/SOAP para operações de dados e Bulk para cargas; situe Composite e contratos Apex customizados como alternativas a avaliar conforme o caso. Não confunda famílias de API com protocolos e formatos; GraphQL também deve ser avaliado pelos recursos suportados, não como substituição universal ([visão das APIs Salesforce](https://trailhead.salesforce.com/content/learn/modules/api_basics/api_basics_overview)).
- **OAuth atual:** comece por External Client Apps; a criação de Connected Apps está restrita desde Spring ’26, embora as existentes continuem utilizáveis. Autenticação do cliente, identidade do usuário de integração e permissões são decisões separadas ([documentação oficial de External Client Apps](https://developer.salesforce.com/docs/platform/mobile-sdk/guide/eca-create.html)).
- **Saída autenticada:** Named Credential identifica endpoint/transporte; External Credential define protocolo e principals; User External Credentials guardam tokens criptografados. Evite “os segredos estão no XML que o utilitário extraiu” ([Get Started with Named Credentials](https://developer.salesforce.com/docs/platform/named-credentials/guide/get-started.html)).
- **Eventos e consumo:** Platform Event representa um contrato de evento definido; CDC comunica alterações de dados; Pub/Sub API publica/consome o barramento, portanto eventos não são apenas uma categoria de “saída”. Ensine replay e checkpoint com a janela documentada de 72 horas, sem prometer retenção ilimitada ([Pub/Sub e event bus](https://developer.salesforce.com/docs/platform/pub-sub-api/guide/expanded-event-bus.html), [durabilidade de mensagens](https://developer.salesforce.com/docs/platform/pub-sub-api/guide/event-message-durability.html)).
- **Confiabilidade e limites:** há 100 callouts e 120 s acumulados por transação Apex, com timeout padrão de 10 s por chamada; não mantenha DML pendente ao fazer callout e desenhe a fronteira de commit antes de escolher trabalho pós-commit. Proponha idempotência, correlação, retentativas e acompanhamento de falhas; middleware, como MuleSoft, é uma decisão arquitetural, não requisito universal ([limites de callout](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-callouts-timeouts.html), [governors](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html), [controle transacional](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/langcon-apex-transaction-control.html)).

Analogia back-end: serviço com APIs gerenciadas, cliente HTTP autenticado e barramento de eventos. A existência de todos os mecanismos não dispensa desenhar contrato, consentimento/autorização, política de entrega e tratamento de duplicidade.

Caso do Pedido: proponha salvar o pedido e processar a integração desacoplada conforme requisitos de consistência. Um timeout no ERP não prova que o ERP deixou de gravar; por isso a próxima tentativa deve ter uma chave de correlação/idempotência e uma política de reconciliação.

Desenho de lousa: aplicativo externo → org; org → ERP por callout; org → barramento → consumidor. O barramento tem setas simplificadas; não atribua a ele garantia de exactly-once de ponta a ponta.

![Integrações síncronas e por eventos](svg/bloco-09-integracao.svg)

Distribuição sugerida: 2 minutos para APIs; 2 para OAuth/credenciais; 3 para eventos; 3 para falhas e limites. A lista completa de APIs fica como referência, não como sequência de slides.

Pergunta de fixação: “O ERP gravou, mas a resposta expirou. O que impede que nossa retentativa crie outro pedido?” Transição: “Vamos fechar reconstruindo esse caminho na documentação.”

### Leitura da documentação: de arquivos a uma história verificável

Bloco 10, duração de 8 minutos. Objetivo: reconstruir um caso de uso com evidências, sem confundir inventário com grafo completo de execução.

- **Mapa de tipos e diretórios:** use pastas como índice inicial, não como equivalência perfeita entre uma pasta e uma funcionalidade. O source format decompõe objetos e organiza bundles; um documento funcional pode agrupar componentes preservando suas identidades ([source format DX](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html)).
- **Escopo da extração:** confira data, versão, org de origem, manifesto e package directories cobertos. Um retrieve orientado a manifesto seleciona componentes; não prova sozinho que tudo da org foi extraído ([retrieve e manifesto](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-ws-create-from-existing.html)).
- **Rastro do pedido:** comece em `objects/Pedido__c`; localize campos, referência de automação, classe, permissão, componente de UI e integração quando houver evidência. Não preencha lacunas com nomes plausíveis.
- **Grau de evidência:** separe referência explícita, vínculo resolvido pelo utilitário e hipótese para revisão. Referências dinâmicas, configuração por ambiente e comportamento de serviços externos podem exigir logs, testes e confirmação operacional.
- **Fechamento prático:** peça ao interlocutor que responda “quem inicia?”, “o que executa?”, “quem tem acesso?”, “onde termina a transação?” e “como a falha é detectada?”. O resultado deve ser uma pequena narrativa verificável, não a memorização de diretórios.

Analogia back-end: combinar documentação de contratos, navegação de código e análise de dependências. Um inventário estático é um mapa útil, mas não equivale a distributed tracing de uma requisição real.

Desenho de lousa: Pedido → automação → integração, com UI/acesso entrando no pedido. Use linha contínua para referência comprovada e tracejada para hipótese; não trate este desenho fictício como descoberta já feita na org.

![Rastro de componentes e grau de evidência](svg/bloco-10-documentacao.svg)

Pergunta de fixação: “Se uma classe aparece na mesma pasta e tem ‘Pedido’ no nome, isso prova que ela executa ao salvar esse objeto?” Fechamento sugerido: “Agora você consegue usar a documentação para formular perguntas concretas, em vez de depender de conhecer cada nome Salesforce de memória.”

## Apoio prático: do arquivo à documentação

Os exemplos abaixo recuperam a concretude do documento original sem transformar a conversa em uma implantação. São exemplos de leitura, não um projeto executável completo, e não foram aplicados em nenhuma org.

### Uma árvore mínima para reconhecer os artefatos

Use esta árvore como índice do exemplo fictício. A estrutura real depende dos package directories e dos componentes recuperados; tipos como objetos custom são decompostos no source format ([estrutura Salesforce DX](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html)).

```text
sfdx-project.json
manifest/
  package.xml
force-app/main/default/
  objects/
    Pedido__c/
      Pedido__c.object-meta.xml
      fields/
        Valor__c.field-meta.xml
        Status__c.field-meta.xml
    Config_Frete__mdt/
      Config_Frete__mdt.object-meta.xml
  customMetadata/
    Config_Frete.SP.md-meta.xml
  classes/
    PedidoService.cls
    PedidoService.cls-meta.xml
  triggers/
    PedidoTrigger.trigger
    PedidoTrigger.trigger-meta.xml
  flows/
    Pedido_Preparar.flow-meta.xml
  permissionsets/
    Operar_Pedidos.permissionset-meta.xml
  lwc/
    pedidoResumo/
      pedidoResumo.html
      pedidoResumo.js
      pedidoResumo.js-meta.xml
  flexipages/
    Pedido_Record_Page.flexipage-meta.xml
  namedCredentials/
    ERP.namedCredential-meta.xml
  externalCredentials/
    ERP_Auth.externalCredential-meta.xml
```

Não leia as pastas em sequência como se fossem uma pilha de chamadas. A árvore indica localização, não prova que `PedidoTrigger` chama `PedidoService`, que o Flow está ativo ou que o LWC aparece em uma página usada por determinado usuário.

### Definição de campo, registro e manifesto

Mostre primeiro a definição de `Valor__c`, em `objects/Pedido__c/fields/Valor__c.field-meta.xml`. Compare a definição com o valor concreto de R$ 500 em um pedido, para separar formato do componente e conteúdo de negócio ([metadados em arquivos](https://developer.salesforce.com/docs/platform/api-metadata/guide/file-based.html)).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Valor__c</fullName>
    <label>Valor</label>
    <precision>16</precision>
    <scale>2</scale>
    <type>Currency</type>
</CustomField>
```

Depois mostre o manifesto mínimo abaixo, que seleciona apenas esse campo. Ele não cria o objeto pai, não seleciona seus registros e não equivale à descrição completa da org; o tipo de metadado e seus membros delimitam o escopo da operação ([retrieve com manifesto](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-ws-create-from-existing.html)).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>Pedido__c.Valor__c</members>
        <name>CustomField</name>
    </types>
    <version>68.0</version>
</Package>
```

A versão 68.0 corresponde à referência Winter ’27 usada nesta revisão; num projeto real, confira a versão suportada pelos ambientes envolvidos e a política de compatibilidade. Não confunda a versão do manifesto com a versão individual de cada classe Apex ([referência Winter ’27](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html), [segurança por versão de API da classe](https://developer.salesforce.com/docs/platform/lwc/guide/apex-security)).

### Três casos da org bananinha, sem pressupor tabelas internas

| Caso | O que é definição | O que acontece no uso | O que procurar na documentação |
|---|---|---|---|
| `Config_Frete__mdt` | Tipo e registros são configuração transportável; o registro de exemplo aparece em `customMetadata/`. | O código consulta uma configuração; não usa DML comum para atualizá-la. | Definição do tipo, registros, referências de consumo e eventuais restrições de acesso ([Custom Metadata](https://developer.salesforce.com/docs/atlas.en-us.244.0.api_meta.meta/api_meta/meta_custommetadatatypes.htm)). |
| Uma Account | Campos e regras são definições; a conta concreta é dado de negócio. | O salvamento aciona as etapas aplicáveis do ciclo transacional. | Campos, regras e automações, sem supor que o retrieve de metadados trouxe todos os clientes ([order of execution](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html), [Metadata API](https://developer.salesforce.com/docs/platform/api-metadata/guide/file-based.html)). |
| Flow em Contact | O arquivo descreve a automação; não é uma execução concreta. | O caminho imediato participa da transação; o assíncrono fica depois do commit. | Objeto/evento, critérios, estado/versão implantada e caminhos configurados ([guia de automação](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered)). |

Pergunte: “O que mudou se eu editar a configuração de frete? E se eu salvar um cliente? E se eu só fizer retrieve do Flow?” O objetivo é verificar se a pessoa diferencia mudança de configuração, operação de negócio e cópia de uma representação.

### Comandos para reconhecer, não para executar nesta conversa

O primeiro exemplo recupera componentes conforme um manifesto. O segundo ilustra validação com testes em sandbox usando dry-run; autenticação, autorização, projeto válido e aliases reais são pré-requisitos, e nenhuma dessas operações foi executada como parte desta revisão ([retrieve](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-ws-create-from-existing.html), [orientação da CLI para validação em sandbox](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_deploy_validate.html)).

```bash
sf project retrieve start \
  --manifest manifest/package.xml \
  --target-org ORG_ORIGEM

sf project deploy start \
  --manifest manifest/package.xml \
  --target-org SANDBOX_DESTINO \
  --dry-run \
  --test-level RunLocalTests
```

Para validar uma implantação destinada à produção, a CLI também oferece `sf project deploy validate`, com testes, sem executar a implantação definitiva; o fluxo e os pré-requisitos não são idênticos aos de uma validação em sandbox. Prefira esses nomes completos aos atalhos ambíguos “sf retrieve” e “sf deploy” do desenho original ([project deploy validate](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_deploy_validate.html)).

### Exercício de navegação em seis minutos

- **Minuto inicial:** abra a documentação de `Pedido__c`; encontre `Valor__c` e a origem da definição.
- **Segundo minuto:** encontre uma automação associada e confira o vínculo explícito com o objeto, não apenas o nome.
- **Terceiro minuto:** se houver uma classe chamada pela automação, siga a referência; caso não haja, registre a lacuna em vez de inventar uma.
- **Quarto minuto:** procure a concessão de acesso e diferencie objeto, campo e registro.
- **Quinto minuto:** investigue interface ou integração, se documentadas; marque as dependências não resolvidas e as configurações que precisam de verificação.
- **Minuto final:** peça uma explicação de volta: “quem iniciou, o que executou, com qual acesso e onde termina a evidência?”

Use esse exercício no encerramento de oito minutos, reservando os dois minutos restantes para recapitulação. No percurso abreviado de trinta minutos, faça apenas objeto → uma referência comprovada → uma pergunta em aberto.

## Distribuição de tempo

O roteiro original soma 95 minutos; os cinco blocos indicados como versão de 30 minutos somam 41 minutos. A revisão abaixo reduz os blocos completos para 85 minutos, sem contar intervalos e perguntas extras.

| Bloco | Tema | Tempo |
|---|---|---:|
| 0 | Mapa geral | 3 min |
| 1 | Multi-tenancy | 6 min |
| 2 | Metadados e runtime | 10 min |
| 3 | Modelo de dados | 8 min |
| 4 | Segurança | 8 min |
| 5 | Ambientes e implantação | 8 min |
| 6 | Apex e transação | 10 min |
| 7 | Flow ou código | 6 min |
| 8 | Front-end | 8 min |
| 9 | Integração | 10 min |
| 10 | Documentação prática | 8 min |
| **Total** | | **85 min** |

### Recorte real de 30 minutos

Este é um recorte, não a execução integral dos blocos selecionados. A proposta é deixar o desenvolvedor apto a navegar e fazer perguntas, não cobrir toda a plataforma.

- **Mapa geral:** 2 minutos do bloco 0.
- **Multi-tenancy:** 4 minutos do bloco 1, com foco no tenant e nos limites.
- **Metadados:** 7 minutos do bloco 2, sem slots detalhados nem banco físico.
- **Transação e Apex:** 7 minutos do bloco 6, incluindo um alerta sobre contexto de segurança.
- **Integração:** 6 minutos do bloco 9, priorizando entrada/saída, credenciais e falhas.
- **Rastro na documentação:** 4 minutos do bloco 10.

### Série de três encontros

- **Fundamentos:** blocos 0 a 3, 27 minutos de conteúdo; reserve aproximadamente 35 minutos com perguntas.
- **Implementação e governança:** blocos 4 a 7, 32 minutos de conteúdo; reserve aproximadamente 40 minutos.
- **Consumo e rastreabilidade:** blocos 8 a 10, 26 minutos de conteúdo; reserve aproximadamente 35 minutos, incluindo navegação prática.

## Aprofundamento opcional: SalesforceDB sem transformar inferência em certeza

Use este trecho apenas se o interlocutor perguntar “qual banco está por baixo?”. Ele é um apêndice de consulta, não um bloco extra obrigatório da apresentação.

- **Base confirmada:** SalesforceDB é construído sobre PostgreSQL, mas usa uma camada própria de armazenamento/acesso baseada em LSM; não é equivalente a “um PostgreSQL padrão com outro nome” ([paper técnico, pp. 4426–4429](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)).
- **Computação e armazenamento:** o guia descreve separação dessas camadas, arquivos imutáveis, logs append-only e armazenamento de objetos, como S3, como sistema de registro definitivo. Caches de armazenamento evitam tratar toda leitura como uma chamada direta ao armazenamento de objetos ([Salesforce Architects](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)).
- **Disponibilidade:** o serviço opera com computação e armazenamento replicados por três zonas de disponibilidade; a computação SQL é descrita com primário e dois standbys, e os serviços usam Kubernetes. Isso não identifica o tipo exato de host EC2, não prova uso de RDS e não autoriza dizer que “não há discos ou caches locais” ([guia oficial](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html), [paper técnico](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)).
- **Células:** uma célula é uma unidade de escala e contenção de impacto que hospeda orgs, não um servidor exclusivo. O guia situa cada org em uma célula com serviço SalesforceDB, mas também descreve serviços independentes; não reduza toda a execução da plataforma a uma única caixa física ([arquitetura Hyperforce e runtime](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)).
- **O que permanece aberto:** conclusão universal da saída de Oracle, localização explícita de todos os metadados de org, identidade física atual dos slots e tabela física de Account. Não use percentual de adoção da “nova plataforma” como percentual comprovado da migração de um banco específico ([guia de transformação](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html), [modelo conceitual](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html), [paper SalesforceDB](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)).

## Checklist da pessoa apresentadora

- **Antes:** escolher um componente real da documentação; conferir versão de API, escopo extraído e release do ambiente; deixar os SVGs abertos.
- **Durante:** manter o mesmo Pedido fictício; diferenciar configuração, dado e execução; anunciar quando o desenho é simplificado.
- **Ao aprofundar:** distinguir contrato público de implementação interna; consultar a referência específica quando um limite ou comportamento depender do contexto.
- **Ao concluir:** pedir ao desenvolvedor que reconstrua o caminho de um salvamento e a fronteira de commit; registrar as perguntas que a documentação estática não resolve.
