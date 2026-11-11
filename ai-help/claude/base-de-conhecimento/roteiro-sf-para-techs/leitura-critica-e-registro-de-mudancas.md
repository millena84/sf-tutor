# Leitura crítica do roteiro de origem

Revisão do anexo `Roteiro-Salesforce-para-dev-back-end.md`, usado como referência de origem, em comparação com a primeira versão dos materiais produzidos nesta conversa. A finalidade é manter a força didática do texto, corrigir imprecisões e evitar que uma analogia seja interpretada como garantia técnica.

**Escopo histórico:** revisão de 11 de novembro de 2026, anterior à integração desta base no GitHub. Naquela entrega, o resultado foi a versão 2 do roteiro e do pacote ZIP, sem alterações no repositório; essa descrição não representa o estado das revisões posteriores. Para a versão 3 e as mudanças atuais, veja a [revisão da base no repositório](../revisao-base-conhecimento.md).

## Avaliação geral

O documento de origem funciona bem como esqueleto de conversa: parte de uma visão geral, aproxima Salesforce do repertório back-end e termina com leitura da documentação. Minha avaliação é que seu principal problema não é a ordem dos assuntos, mas a mistura entre afirmações técnicas, simplificações e detalhes internos não confirmados, especialmente no bloco 2.

Também há um problema de condução: o aprofundamento do bloco 2 cresceu muito além de uma fala de dez minutos. A versão revisada mantém o conteúdo como referência, mas separa o que será dito do que só deve ser consultado quando houver uma pergunta específica.

### O que foi preservado

- **Mapa inicial:** dá contexto antes das siglas e permite apontar “estamos nesta camada”.
- **Pedido como fio condutor:** reduz a necessidade de aprender um novo domínio a cada tópico.
- **Analogias back-end:** ORM, aplicação gerenciada, serviço de dados e workflow são pontes úteis, desde que seus limites sejam anunciados.
- **Org bananinha:** permite comparar configuração, dado e execução sem depender de jargão adicional.
- **Fechamento na documentação:** converte o conteúdo em uma habilidade de investigação, não em um catálogo de definições.

## Correções técnicas e de linguagem

Os trechos da primeira coluna identificam a formulação do anexo; a coluna final descreve o tratamento na versão 2. As citações se referem às evidências externas, não à autoria do texto de origem.

| Formulação ou problema | Avaliação | Tratamento aplicado |
|---|---|---|
| “São 10 blocos”, enumerados de 0 a 10. | Erro de contagem. | Corrigido para onze blocos, preservando os identificadores de 0 a 10. |
| “85 minutos” para a sequência original. | O total original está correto: 3+8+10+8+8+10+10+5+8+10+5 = 85. A versão anterior desta leitura crítica errou ao afirmar 95 minutos. | Corrigida a própria crítica; nova distribuição mantém 85 minutos, sem alegar uma redução inexistente. |
| “30 min” com 0, 1, 2, 6 e 9 completos. | Os tempos originais somam 41 minutos. | Criado recorte de trinta minutos com duração parcial explícita, incluindo navegação final. |
| “Tudo isso = metadado (XML)”. | Confunde natureza do componente e representação em arquivos. | Metadados incluem fontes e recursos em diferentes formatos; retirado o equivalente universal “metadado = XML” ([source format](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html)). |
| “XML só existe na fronteira”, “só no deploy/retrieve”, “uma vez”. | A ideia de não reler o projeto local é boa; os absolutos sobre XML e persistência são amplos demais. | Descrita a função de intercâmbio e implantação, sem prometer uma representação única para todo componente ou operação ([Metadata API](https://developer.salesforce.com/docs/platform/api-metadata/guide/file-based.html), [Tooling REST/SOAP](https://developer.salesforce.com/docs/platform/api-tooling/guide/intro-api-tooling.html)). |
| “Todo XML vira linha em tabela”. | Não representa adequadamente fontes, bundles e artefatos preparados para execução. | Separados fontes, descritores, configuração implantada e runtime; não é apresentado um mapeamento físico individual de arquivos para linhas ([source format](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html), [runtime](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html)). |
| “O browser só renderiza”. | Incorreto para uma UI com JavaScript, reatividade e cache cliente. | Browser explicitamente ativo; regras protegidas e operações de dados continuam com responsabilidades server-side ([wire Apex](https://developer.salesforce.com/docs/platform/lwc/guide/apex-wire-method), [cache cliente](https://developer.salesforce.com/docs/platform/lwc/guide/apex-result-caching.html)). |
| “Cache na frente = Vegacache”. | A fonte não estabelece essa equivalência para todos os metadados. | Caches de metadados e caches locais de serviços foram separados da descrição específica do Vegacache ([Metadata Framework e Caching Service](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)). |
| Desenho “SDB: tabelas de metadados + dados”, seguido de ressalva de que isso não está explícito. | Contradição entre o grau de certeza do desenho e o do texto. | SVG usa “configuração na org”; o mapeamento de todos os metadados de org para SalesforceDB continua como não confirmado ([guia oficial](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)). |
| Slots apresentados como explicação física atual. | Válidos como modelo publicado, não como comprovação do esquema atual de cada serviço. | Anotado como modelo conceitual; o paper de 2026 confirma shared-table, mas não todos os nomes e slots históricos ([arquitetura publicada](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html), [paper SalesforceDB](https://www.vldb.org/pvldb/vol19/p4426-arora.pdf)). |
| “Setup grava direto”; “Tooling API: JSON”. | A primeira frase presume implementação interna; a segunda omite SOAP e o escopo parcial de tipos/operações. | Setup como interface sem arquivo local obrigatório; Tooling como API para operações específicas, com REST e SOAP ([Tooling API](https://developer.salesforce.com/docs/platform/api-tooling/guide/intro-api-tooling.html)). |
| Account “nunca vira XML”. | Confunde dado de negócio com formato de transporte. | Registro não é componente de configuração do deploy, mas dados podem ser serializados em XML, inclusive por SOAP ([visão das APIs](https://trailhead.salesforce.com/content/learn/modules/api_basics/api_basics_overview)). |
| SOQL de Custom Metadata “não conta no limite”. | Exige contexto e exceções. | Acrescentadas consultas em Flow, Long Text Area e limite de registros documentado; preservada a distinção de DML comum ([Custom Metadata Allocations](https://help.salesforce.com/s/articleView?id=platform.custommetadatatypes_limits.htm&language=en_US&type=5)). |
| Todo Record-Triggered Flow “executa na mesma transação”. | Correto para o caminho imediato, não para todos os caminhos. | Diferenciados imediato e pós-commit assíncrono; falha posterior não desfaz commit anterior ([order of execution](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)). |
| “Depois ninguém consulta a planta”. | Pode sugerir que a execução deixa de consultar metadados. | Frase reformulada: não consulta o checkout local, mas continua usando definições implantadas e caches ([runtime metadata-driven](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html)). |
| Lookup como “FK opcional”. | Lookup pode ser obrigatório; exclusão e dependência merecem configuração explícita. | Substituída a oposição “fraco/forte” por propriedades de ciclo de vida e acesso ([Object Relationships](https://help.salesforce.com/s/articleView?id=overview_of_custom_object_relationships.htm&language=en_US)). |
| `SELECT Name, Account.Name, (...) FROM Account`. | O caminho `Account.Name` não é uma relação pai apropriada nesse contexto de origem. | Dois exemplos válidos: Account com subconsulta Contacts; Contact com `Account.Name` ([nomes de relacionamento](https://developer.salesforce.com/docs/platform/salesforce-soql-sosl/guide/sforce-api-calls-soql-relationships-understanding.html)). |
| Account → Pedido em master-detail. | Não é um erro por si só; é uma decisão de domínio, não uma relação obrigatória. | Exemplo adota lookup para o cliente e master-detail para itens; a mudança é declarada como proposta, não como correção de algo inválido ([regras de relacionamento](https://help.salesforce.com/s/articleView?id=overview_of_custom_object_relationships.htm&language=en_US)). |
| “Pode entrar” respondido apenas por Profile/Permission Sets. | Mistura autenticação com capacidade de operar objetos/campos. | Bloco passa a começar pela operação autorizada; login/autenticação é uma pergunta distinta ([permissões de objeto](https://help.salesforce.com/s/articleView?id=sf.users_profiles_object_perms.htm&language=en_US&type=5)). |
| Segurança sem mencionar versão de API. | Falta uma dimensão importante da documentação atual. | Incluída a distinção API 67.0+ e anteriores; sharing e modo de acesso continuam explícitos, sem atribuir CRUD/FLS apenas a `with sharing` ([Secure Apex Classes](https://developer.salesforce.com/docs/platform/lwc/guide/apex-security)). |
| “Build não gera binário”, logo deploy seria só aplicar XML. | Uma boa diferença em relação ao upload de um executável não prova ausência de compilação ou representações internas. | Removida a conclusão sobre ausência de compilação; descrita a implantação de fontes/configuração em ambiente gerenciado ([runtime e Apex](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html)). |
| Todo deploy produtivo roda testes; 75% sem contexto. | Não é uma regra universal sobre qualquer payload e test level. | Explicadas cobertura agregada, alguma cobertura de trigger e regra individual de testes especificados ([testes](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-testing-intro.html), [RunSpecifiedTests](https://developer.salesforce.com/docs/platform/api-metadata/guide/meta-deploy-run-specific-tests.html), [testes por ambiente](https://developer.salesforce.com/docs/platform/api-metadata/guide/meta-deploy-run-local-tests.html)). |
| “Validações → before triggers → after triggers → flows → commit”. | Omissão que ensina uma ordem errada para before-save Flow. | Linha do tempo corrigida, claramente identificada como recorte da ordem completa ([sequência oficial](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)). |
| Unit of Work como “DML único”. | Um agrupador de trabalho pode executar várias operações; seu nome não equivale ao commit da transação. | DML bulkificado por trabalho/objeto e distinção entre `commitWork()` e confirmação final ([Trailhead Unit of Work](https://trailhead.salesforce.com/content/learn/modules/apex_patterns_sl/apex_patterns_sl_learn_uow_principles), [commit na plataforma](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)). |
| “Heap 6 MB”. | Valor antigo para o contexto atual do material. | Winter ’27: 10 MB síncrono e 25 MB assíncrono, com ressalva de compatibilidade em orgs não produtivas ([release note](https://help.salesforce.com/s/articleView?id=release-notes.rn_apex_heap_limit.htm&language=en_US&type=5)). |
| “Workflow Rules/Process Builder descontinuados”. | Falta explicar se deixam de executar. | Fim de suporte desde 31/12/2025 não significa desligamento imediato das automações ativas; elas permanecem relevantes na análise ([comunicado oficial](https://help.salesforce.com/s/articleView?id=001096524&language=en_US&type=1)). |
| “Clicks before code”; integração como motivo suficiente para Apex. | Slogan insuficiente para arquitetura. | Escolha por volume, dependências, transação, observabilidade e capacidade do time; Flow e integrações declarativas não são excluídos por princípio ([guia de decisão](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered)). |
| LDS e `@wire` como sinônimos; `@AuraEnabled` como endpoint genérico. | Mistura mecanismos de acesso. | `@wire` também chama Apex cacheável; método exposto à UI não é automaticamente Apex REST público ([wire Apex](https://developer.salesforce.com/docs/platform/lwc/guide/apex-wire-method), [segurança](https://developer.salesforce.com/docs/platform/lwc/guide/apex-security)). |
| “OAuth via Connected App”, sem prioridade atual. | Precisava atualizar a recomendação para novos cenários. | External Client Apps em primeiro plano; Connected Apps existentes não são tratadas como automaticamente inoperantes ([documentação de criação](https://developer.salesforce.com/docs/platform/mobile-sdk/guide/eca-create.html)). |
| Eventos apenas em “saindo”. | Eventos e API de publicação/assinatura não cabem nessa classificação unilateral. | Entrada/saída HTTP separadas do eixo de eventos; SVG indica publicação/consumo bidirecionais de Platform Events, sem sugerir publicação externa de CDC ([Pub/Sub e barramento](https://developer.salesforce.com/docs/platform/pub-sub-api/guide/expanded-event-bus.html)). |
| “Timeout 120 s”. | Ambíguo entre teto individual e orçamento acumulado. | Incluídos 100 callouts, padrão de 10 s por chamada e 120 s acumulados por transação ([Callout Limits](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-callouts-timeouts.html)). |
| Callout depois de DML sem explicar o trabalho pendente. | A regra é sobre estado transacional, não simplesmente ordem textual de duas linhas. | Preservada a restrição com DML pendente; caso avançado de rollback e liberação de savepoints fica fora da fala principal ([Transaction Control](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/langcon-apex-transaction-control.html)). |
| Uma seção da documentação sempre corresponde a uma pasta. | Pode ser índice didático, mas não equivalência universal. | Agrupamento funcional com identidade dos componentes e proveniência preservadas; inventário não é grafo comprovado de execução ([source format](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-source-file-format.html)). |

## O que também melhorou em relação à minha primeira versão

A primeira revisão reforçou a cautela técnica, mas deixou a apresentação mais abstrata do que o documento de origem em alguns pontos. A versão 2 recupera os exemplos concretos sem voltar às afirmações excessivas.

- **Arquivo de campo:** restabelecido o XML de `Valor__c` em um bloco de código legível, para comparar definição e valor.
- **Manifesto:** acrescentado um `package.xml` mínimo que seleciona esse campo; explicitado que ele não cria o objeto pai nem representa toda a org.
- **Árvore do projeto:** recuperados caminhos de objetos, classes, triggers, flows, Custom Metadata, UI e credenciais, sem representar proximidade de pasta como prova de chamada.
- **Org bananinha:** expandida em três casos comparáveis e perguntas de verificação.
- **CLI:** comandos completos para reconhecimento, com dry-run em sandbox; nenhum comando de org foi executado.
- **Unit of Work:** reforçada a distinção entre executar DML e confirmar toda a transação.
- **Automação legada:** explicitado que ausência de suporte não elimina a execução existente.
- **Navegação:** acrescentados cartão de condução e exercício cronometrado para trabalhar diretamente com documentação.
- **SVGs:** fonte/implantação/uso mais claros, requisitos de autenticação separados de autorização e eventos sem classificação unilateral de saída.

## Critérios editoriais adotados

- **Confirmado:** afirmação sustentada pela documentação ou pelo paper citado, respeitando o escopo e o contexto.
- **Conceitual:** desenho útil para entender o comportamento, sem prometer que nomes e estruturas são o esquema físico atual.
- **Não confirmado:** a documentação consultada não permite a conclusão; ausência de comprovação não vira uma negação universal.
- **Exemplo proposto:** componente ou relação fictícia para ensinar; não é uma descoberta feita na org da usuária.
- **Escolha pedagógica:** uma adaptação de tempo, ordem ou metáfora; não deve ser apresentada como “erro técnico” do documento anterior.

## Resultado da revisão

O material continua sendo uma conversa para um desenvolvedor back-end, não uma defesa da implementação interna da Salesforce. A pessoa deve sair sabendo localizar componentes, distinguir configuração e registro, entender acesso e transação e reconhecer quando a documentação estática não responde à pergunta.

Para apresentar, use o cartão de condução e os onze blocos do roteiro principal. Para responder às perguntas mais profundas, use a verificação técnica e os apêndices; para auditar o que mudou, use este registro.
