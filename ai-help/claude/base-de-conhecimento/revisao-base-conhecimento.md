# Leitura crítica da base de conhecimento no repositório

Revisão de 11 de novembro de 2026 sobre os arquivos existentes em `ai-help/claude/base-de-conhecimento/`. A finalidade é fazer os insumos funcionarem como uma base coerente para leitura humana e uso por IA, não apenas adicionar mais uma versão de roteiro.

## Diagnóstico

A força da base está na progressão do mapa geral até a investigação de componentes, com analogias próximas do repertório back-end e um exemplo contínuo. O principal risco editorial era manter um roteiro revisado ao lado de uma transcrição antiga com orientações incompatíveis, sem uma indicação clara de precedência.

Também havia problemas verificáveis de integração: onze referências de imagem apontavam para uma subpasta inexistente, e alguns avisos dos SVGs usavam texto ciano com opacidade de 16% sobre fundo claro. No documento transacional, a divisão da tabela mudava a numeração oficial e omitia Escalation Rules, embora uma nota posterior ainda dependesse dos números oficiais.

## Achados e tratamento aplicado

| Achado | Tipo | Tratamento |
|---|---|---|
| `passagem-sf-eng.md` republicava roteiro e conversa, incluindo ofertas de edição de um Google Doc não relacionadas ao estado desta pasta. | Coerência e proveniência | Transformado em entrada curta; a apresentação completa tem um único arquivo principal. O conteúdo anterior continua no histórico Git. |
| A revisão anterior afirmava que o original somava 95 minutos. | Erro da própria revisão | Recontado no anexo e no arquivo do repositório: 3+8+10+8+8+10+10+5+8+10+5 = 85. Corrigidos roteiro e leitura crítica; não houve redução de 95 para 85. O recorte antigo de trinta minutos continua somando 41. |
| “Tudo é XML”, browser passivo, “schema físico nunca muda” e metadados de org no SDB apresentados sem ressalva adequada no texto antigo. | Precisão técnica | Retiradas as versões concorrentes; a verificação de infraestrutura do roteiro principal mantém as distinções e referências, sem promover hipótese a fato ([arquitetura multitenant](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-multitenant-architecture.html), [transformação da plataforma](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html)). |
| SOQL inválido e heap antigo ainda apareciam no roteiro antigo. | Consistência técnica | A entrada aponta para os exemplos já corrigidos do principal; limites do guia transacional foram contextualizados por release ([limites Apex](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html), [heap Winter ’27](https://help.salesforce.com/s/articleView?id=release-notes.rn_apex_heap_limit.htm&language=en_US&type=5)). |
| Sequência de insert/update/upsert apresentada como se também descrevesse delete/undelete integralmente. | Escopo técnico | Escopo delimitado; eventos de exclusão/restauração não recebem automaticamente toda a sequência de salvamento ([ordem oficial](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)). |
| `before undelete` listado como evento. | Erro técnico | Removido; restauração admite `after undelete`, nos objetos suportados ([eventos de trigger](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-defining.html)). |
| Escalation Rules ausente, enquanto carga de valores e validações iniciais viravam etapas independentes. | Erro de sequência | Restabelecidas as vinte etapas e a numeração da referência oficial ([ordem oficial](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)). |
| Before-save Flow descrito com Apex invocado, sem distinguir as capacidades desse contexto. | Simplificação enganosa | Removida essa associação da tabela; o contexto é apresentado como atualização do próprio registro sem DML adicional ([guia de automação](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered)). |
| “Validation Rule roda depois de Flows e Triggers” sem recorte. | Generalização | Diferenciadas as validações iniciais específicas e as regras customizadas depois dos mecanismos before, não depois de qualquer Flow/trigger ([ordem oficial](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)). |
| `Trigger.old` e “uma vez adicional” formulados como regra geral de reentrada. | Generalização | Condicionados ao workflow field update documentado; outro DML e repetição com sucesso parcial não recebem a mesma promessa ([considerações de trigger](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html)). |
| QueryLocator limitado a 10 mil “relevante em Batch” sem explicar a exceção. | Omissão técnica | Incluída a exceção do QueryLocator de Batch até 50 milhões, processados em transações por lote ([Batch Apex](https://trailhead.salesforce.com/content/learn/modules/asynchronous_apex/async_apex_batch)). |
| Limite de chamadas `sendEmail` atribuído também à etapa de auto-response. | Mistura de escopos | Tabela separa chamadas Apex de todos os mecanismos de e-mail; não infere consumo Apex de uma regra automática ([governors](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)). |
| Atribuição em before apresentada como “não consome DML”. | Ambiguidade | Explicado que ela não exige DML adicional; a operação iniciadora e demais DML continuam sujeitos aos limites ([triggers](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers.html), [limites](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html)). |
| `System.enqueueJob()` rotulado “chamada após o commit”. | Erro de fronteira | Enfileiramento na transação de origem separado da execução posterior; a classe de integração não é apresentada como pronta sem implementação ([ordem oficial](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html), [Queueable](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-queueing-jobs.html)). |
| Platform Events listados genericamente como pós-commit. | Erro de garantia | Incluída distinção Publish Immediately/Publish After Commit, com ressalva para Pub/Sub API e sem confundir aceitação com processamento externo ([comportamento](https://developer.salesforce.com/docs/platform/platform-events/guide/platform-events-define-ui.html), [publicação Apex](https://developer.salesforce.com/docs/platform/platform-events/guide/platform-events-publish-apex.html)). |
| Pub/Sub descrito genericamente como publicar/consumir “o barramento”. | Precisão de contrato | Explicitado no roteiro que publicar Platform Events não significa publicar alterações CDC ([event bus](https://developer.salesforce.com/docs/platform/pub-sub-api/guide/expanded-event-bus.html)). |
| Lista “recomendação moderna” parecia outra ordem de execução, com validação antes do before trigger. | Ambiguidade didática | Substituída por critérios de desenho e um único mapa temporal; Flow/Apex/híbrido são escolhas contextuais ([guia de decisão](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered)). |
| Exemplos mudavam de Pedido para Opportunity e misturavam duplicidade de nomes de trigger. | Escolha pedagógica | Guia transacional adota `Pedido__c` e explicita que trechos são ilustrativos, não um pacote executável. |
| Onze links `svg/...` dentro de `roteiro-sf-para-techs/`. | Navegação | Corrigidos para `../svg/...`, sem mover os arquivos. |
| Textos ciano translúcidos e conectores claros nos SVGs. | Legibilidade | Rótulos tornam-se escuros e opacos; conectores usam cor escura. Mantidos layout, fundo, títulos, descrições e rodapé de marca. |
| Registro dizia “nenhum arquivo do GitHub foi alterado”, sem marco histórico. | Proveniência | A frase agora descreve apenas a entrega anterior; revisão atual tem registro próprio. |
| Não havia índice nem checagem repetível dos vínculos e do formato. | Manutenção | Criados README e verificador local sem dependências externas. |

## O que foi preservado

- **Roteiro principal:** onze blocos de 0 a 10, até dez minutos cada, com objetivo, três a cinco pontos principais, analogia, desenho e pergunta.
- **Progressão:** responsabilidades antes de siglas, configuração antes de execução e operação simples antes de falha distribuída.
- **Exemplo:** Pedido é a âncora; Account, Contact e Custom Metadata continuam como comparações quando ajudam.
- **Acessibilidade didática:** perguntas de fixação, duas velocidades de leitura, recorte curto e material opcional fora do tempo principal.
- **Identidade visual:** marca Desbugando e a geometria dos onze diagramas permanecem; os arquivos de `marca/` não foram redesenhados.
- **Cautela de evidência:** nada nesta revisão equivale a descobrir comportamento de uma org, confirmar todas as tabelas físicas ou compilar Apex.

## Validação desta revisão

O comando reproduzível é `python3 ai-help/claude/base-de-conhecimento/verificar_base.py`, executado a partir da raiz do repositório. Ele verifica links locais, parsing de SVG/XML, presença dos onze SVGs e a estrutura dos blocos; não substitui validação técnica em uma org.

A checagem passou, assim como os sete testes executados com `python3 -B -m unittest discover -s ai-help/claude/base-de-conhecimento -p 'test_*.py' -v`. Os onze SVGs foram renderizados para inspeção de legibilidade, e `git diff --check` não apontou problemas de whitespace.

- **Estrutura:** onze blocos, identificadores consecutivos, duração máxima de dez minutos, soma coerente com a tabela de tempos, três a cinco pontos principais e presença de objetivo, analogia e imagem.
- **Vínculos:** referências locais dos Markdown resolvem para arquivos ou diretórios existentes, sem depender da estrutura do ZIP anterior.
- **XML:** os SVGs e os trechos XML do roteiro são bem formados; diagramas preservam título, descrição e rodapé. As quebras de linha dos SVGs foram normalizadas para LF; uma comparação XML confirma a preservação semântica dos onze rodapés.
- **Legibilidade:** rótulos do corpo têm cor escura opaca; inspeção renderizada complementa a checagem estrutural.
- **Git:** alterações restritas a esta pasta; sem deploy Salesforce, sem alteração de configuração de org e sem merge na main.

O verificador não valida âncoras de headings, disponibilidade de URLs externas nem todas as combinações de cor/posição. Os exemplos Apex continuam não compilados e não executados; apenas uma validação em ambiente apropriado pode demonstrar seu comportamento real.

## Evoluções propostas, não implementadas neste PR

- **Ficha de investigação:** um formulário curto com componente de origem, referência encontrada, grau de evidência, versão e pergunta pendente.
- **Caso prático executável:** um pacote mínimo do Pedido com permissões, testes e mock de ERP, em trabalho separado; o material atual não deve fingir que já é esse pacote.
- **Cenários de teste:** salvar em lote, provocar validação, simular falha imediata, falha posterior e entrega duplicada; validar em sandbox com requisitos definidos.
- **Manutenção por release:** rever apenas os pontos sensíveis, como heap, defaults de segurança, APIs e automações legadas, em vez de republicar todo o roteiro.
- **Automação de qualidade:** integrar o verificador a CI depois de decidir a política de workflows do repositório; este PR não altera `.github/` nem o aplicativo tutorial.

## Limite desta revisão

A pasta é uma base de ensino, não uma auditoria completa da plataforma ou do aplicativo em `apps/`. Alterações na estrutura do app, no grafo de aprendizagem, nos demais insumos e na marca ficaram fora do escopo autorizado.
