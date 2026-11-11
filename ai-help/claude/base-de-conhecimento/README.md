# Base de conhecimento: Salesforce para desenvolvedores

Material de letramento técnico para quem já desenvolve back-end e está começando a investigar uma org Salesforce. O objetivo é reconhecer componentes, reconstruir comportamentos com evidências e distinguir contrato público, analogia e implementação interna não confirmada.

## Por onde começar

| Sua necessidade | Arquivo | Como usar |
|---|---|---|
| Preparar ou conduzir uma conversa | [Roteiro principal](roteiro-sf-para-techs/roteiro-salesforce-backend.md) | Onze blocos de até dez minutos, com objetivo, três a cinco pontos, analogia, SVG e pergunta de fixação. |
| Entender o mapa e o percurso | [Passagem para engenharia](passagem-sf-eng.md) | Entrada curta; aponta para o roteiro principal sem manter uma segunda versão concorrente. |
| Investigar gravação, reentrada e limites | [Order of Execution](orderOfExecution.md) | Referência transacional; a tabela completa não precisa ser decorada na apresentação. |
| Auditar a revisão do documento de origem | [Leitura crítica de origem](roteiro-sf-para-techs/leitura-critica-e-registro-de-mudancas.md) | Registro da revisão anterior, com escopo e data próprios. |
| Auditar a revisão desta pasta | [Revisão da base no repositório](revisao-base-conhecimento.md) | Achados, correções implementadas, validações e evoluções ainda propostas. |

## Percurso progressivo

- **Primeiro contato:** use o recorte de trinta minutos do roteiro; deixe banco físico, slots e detalhes de limites como consulta.
- **Consolidação:** siga os três encontros sugeridos, retomando o mesmo `Pedido__c`. Comece cada encontro pedindo uma explicação curta do anterior.
- **Aplicação:** abra a documentação gerada e siga objeto → automação → acesso → integração, marcando cada ligação como evidência ou hipótese.
- **Retomada:** use as perguntas de fixação para encontrar a lacuna; não volte ao início de todo o conteúdo quando apenas um conceito precisar de reforço.

## Contrato editorial

- **Referência principal:** `roteiro-sf-para-techs/roteiro-salesforce-backend.md` concentra a apresentação e a verificação de infraestrutura. Os outros documentos complementam esse texto, sem republicar o roteiro inteiro.
- **Exemplo fictício:** `Pedido__c`, seus campos e integrações servem ao ensino; não são componentes descobertos em uma org real.
- **Evidência técnica:** afirmações dependentes de release/API precisam de contexto e referência oficial próxima. Ausência de evidência não comprova ausência de um componente ou comportamento.
- **Insumo para IA:** ler este índice primeiro; não tratar histórico de conversa, nomes plausíveis ou diagramas conceituais como prova de execução real.
- **Manutenção:** mudanças de comportamento devem atualizar texto, desenho e referência afetados; conferir caminhos relativos depois de reorganizar arquivos.

## Diagramas e identidade visual

Os [onze SVGs](svg/) ficam em uma pasta irmã de `roteiro-sf-para-techs/`; por isso o roteiro usa caminhos `../svg/`. Os arquivos de [marca](marca/) são recursos visuais, não documentação da arquitetura Salesforce.

A revisão preserva a identidade Desbugando e usa texto escuro opaco sobre o fundo claro dos diagramas. As cores decorativas não devem tornar avisos ou setas difíceis de perceber.

## Verificação local

Na raiz do repositório, execute `python3 ai-help/claude/base-de-conhecimento/verificar_base.py`. O verificador usa somente a biblioteca padrão, não acessa a rede nem uma org e retorna erro se encontrar links locais quebrados, SVG/XML malformado ou perda da estrutura dos onze blocos.

Para exercitar os testes do próprio verificador, execute `python3 -B -m unittest discover -s ai-help/claude/base-de-conhecimento -p 'test_*.py' -v`. Há casos negativos de imagem ausente, XML inválido, texto translúcido, duração inválida e divergência de soma/tabela; esses testes também não acessam uma org.

Última revisão editorial: 11 de novembro de 2026. Os exemplos Apex e os comandos Salesforce continuam ilustrativos; não foram compilados, implantados ou executados em uma org nesta revisão.
