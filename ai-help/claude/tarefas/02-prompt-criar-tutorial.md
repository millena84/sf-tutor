# Tarefa 2: prompt para criar o tutorial visual

Execute este prompt depois de a tarefa de insumos ter produzido um recorte validado e um relatório de cobertura. Não é necessário esconder as partes ainda incompletas: o tutorial deve tornar suas limitações visíveis e não preenchê-las com suposições.

O prompt não obriga uma biblioteca de grafo específica. Exige uma experiência interativa equivalente à intenção da referência, respeitando o contrato de dados e os requisitos de cada nível.

```text
Você está no repositório sf-tutor. Sua tarefa é implementar o tutorial visual
e interativo em grafo, consumindo os insumos já produzidos no projeto.

LEITURA E VERIFICAÇÃO INICIAL

1. Leia integralmente:
   ai-help/claude/insumos-grafo/00-especificacao-grafo.md
2. Leia as instruções do repositório e verifique o git status.
3. Leia o README, os schemas, o inventário, o relatório de cobertura e as
   instruções locais em ai-help/claude/insumos-grafo/.
4. Execute os validadores disponíveis antes de programar.
5. Descubra o contrato real dos dados; não presuma que os nomes sugeridos
   nos rascunhos correspondem ao resultado implementado.

Se houver erro estrutural de dados, relate e corrija de forma mínima e
rastreável, sem inventar conteúdo e sem sobrescrever curadoria manual.
Se houver cobertura parcial, implemente a interface sobre o recorte válido,
exiba as limitações e mantenha os itens planejados identificados.

Não gere uma segunda base técnica hardcoded no frontend.
Não reduza o produto a um grafo de demonstração com conteúdo falso.

PASTAS E LIMITES

Toda alteração/criação de insumos, índices, projeções, schemas, ferramentas
de dados e relatórios deve continuar exclusivamente dentro de:

ai-help/claude/insumos-grafo/

O código da aplicação não precisa ficar misturado aos insumos. Reutilize
o frontend já existente, se houver; se não houver, crie em apps/sf-tutor/.
Essa é uma convenção proposta para o código, não uma mudança do local
obrigatório dos insumos.

Não mover os dados para uma pasta public independente que passe a ser
outra fonte manual. Se o build copiar dados públicos, a cópia é gerada.
Não modificar documentos históricos, mudanças de terceiros ou arquivos
fora do necessário para o site, seus testes e sua configuração.
Não fazer commit, push, deploy nem publicar sem solicitação explícita.

REFERÊNCIA E IDENTIDADE

Inspecione https://flavinho.pages.dev para compreender:
- Mapa de conexões.
- Busca e filtros.
- Seleção de nós e de relações.
- Painel de leitura associado ao mapa.
- Controles de navegação e comportamento em telas diferentes.

Use somente como inspiração de interação. Não copie conteúdo político,
textos, imagens, código ou identidade visual da página.
Se não conseguir abrir a referência, informe isso e siga a especificação,
sem fingir que a inspecionou.

Crie identidade própria para sf-tutor, usando o logo Salesforce no centro
conforme asset/origem/condições de uso registrados. Não sugerir afiliação
oficial e não redesenhar uma marca alternativa como se fosse o logo oficial.
Se o asset correto não estiver disponível, usar placeholder identificado
até sua substituição; não chamar esse estado de entrega visual final.

PRODUTO

Não quero apenas Mermaid, uma árvore de diretórios, um dashboard de cards
ou uma figura estática. Quero um tutorial navegável em grafo que permita
explorar a base completa progressivamente e aprender com cada seleção.

Visão inicial:
Salesforce → classificação → sub-classificação → funcionalidade
  → metadata type/XML → propriedades
  → objeto API → campos

Visão alternativa:
Salesforce → nuvem/produto → classificação → sub-classificação
  → as mesmas funcionalidades e representações.

As duas visões devem compartilhar IDs canônicos e o mesmo conteúdo.
Se um item aparecer em dois caminhos, deve abrir a mesma ficha.
Não impor uma hierarquia física falsa entre produtos Salesforce.
Não esconder funcionalidades sem XML: User é um caso obrigatório.

INTERAÇÃO

- A abertura mostra o centro Salesforce e somente o próximo nível.
- Alternância Por funcionalidade / Por nuvem.
- Clique seleciona e abre painel; controle explícito expande/recolhe.
- Zoom, pan, enquadrar conteúdo, voltar ao centro e histórico de navegação.
- Expandir um nível não deve despejar todos os campos da base no canvas.
- Implementar carregamento progressivo e/ou agrupamentos/paginação visual
  para grandes listas, sempre tornando todos os itens alcançáveis.
- Permitir “ver todas as propriedades/campos” em lista no painel, com
  busca e navegação para o nó correspondente.
- Busca global por português, nome técnico, label e aliases, mesmo quando
  o item estiver recolhido ou seu chunk ainda não estiver carregado.
- Resultado de busca abre o caminho necessário e focaliza o item.
- Filtros por nuvem, classificação, representação XML/API, família de API
  e estado de validação; explicar por que um resultado ficou oculto.
- Filtros não devem romper relações deixando significado enganoso.
- Distinguir visualmente hierarquia didática, representação técnica,
  referência entre campos, dependência e correspondência XML/API.
- Diferenciar tipos de nós por forma/ícone/label, além de cor.
- Selecionar uma relação abre descrição, campos, cardinalidade quando
  verificada, condições e fontes.
- Breadcrumbs e destaque dos vizinhos/caminho selecionado.
- Link estável por nó; quando houver múltiplos caminhos, preservar
  contexto na URL sem mudar a identidade do item.
- Respeitar back/forward do navegador.

PAINEL DE CONTEÚDO

Renderize os dados exigidos por tipo de nó na especificação.
Não omita campos só porque não cabem em um card.

Salesforce:
- Visão técnica do ecossistema, conceitos fundamentais, escopo,
  versão/cobertura e orientação de uso.

Nuvem/produto:
- O que é, para que serve, contexto tecnológico, licenças/requisitos
  com data/fontes e visão geral de funcionalidades.

Classificação e sub-classificação:
- O que agrupa, pré-requisitos, exemplos, limites e observações técnicas.
- Indicar quando o agrupamento é curadoria didática.

Funcionalidade:
- Nome pt-BR/técnico, finalidade, exemplo, Setup se houver, práticas,
  alertas, nuvens e representações disponíveis.

Metadata type/XML:
- Pasta Salesforce, padrão de nome físico, formatos de fonte,
  acesso via Setup, finalidade, práticas, pontos de atenção,
  exemplo XML e todas as propriedades.

Objeto API, incluindo objeto de junção:
- Nome técnico/label, finalidade, APIs de acesso comprovadas,
  operações, permissões/restrições, Setup quando aplicável,
  consulta/endpoint/exemplo Apex válido, práticas, alertas e todos os campos.

Propriedade/campo:
- Nome técnico e labels, tipo, explicação, finalidade, origem padrão/custom,
  default, obrigatoriedade/condições, valores possíveis e o significado
  individual de cada valor, restrições, exemplo e fontes.
- Para campos API: exposição por API, leitura/escrita, nulabilidade,
  cálculo, create/update, referências e demais detalhes documentados.
- Domínios extensos devem ser pesquisáveis, mas não truncados silenciosamente.
- Exibir desconhecido/não aplicável/não exposto/bloqueado distintamente.

Em todos os painéis:
- Começar por explicação curta e compreensível.
- Detalhes técnicos em seções expansíveis, sem perder informação.
- Fontes oficiais clicáveis próximas das afirmações correspondentes.
- Versão/contexto e estado de validação visíveis.
- Exemplos copiáveis, sem dados pessoais ou IDs reais.
- Distinguir explicação didática de afirmação oficial.
- Não afirmar que uma propriedade default desconhecida é false ou vazio.
- Não chamar objeto exposto por API de tabela física privada.

PERCURSOS OBRIGATÓRIOS

1. Salesforce → Acesso, identidade e segurança → subgrupo de usuários
   → Usuários → User → campos.
   Não mostrar XML User fictício.
2. Salesforce → permissões → PermissionSet
   → XML/propriedades e objeto API/campos conforme os dados verificados.
3. De User chegar a PermissionSetAssignment e de lá ao PermissionSet
   e PermissionSetGroup pelos respectivos campos documentados.
4. User.ProfileId leva a Profile; não atribuir essa ligação a uma junção.
5. CustomObject/CustomField permitem comparar configuração XML com
   representações API sem afirmar equivalência de todos os campos.
6. FlexiPage, QuickAction e PathAssistant podem ser encontrados por UX e
   por ligações com dados, sem duplicar o cadastro da funcionalidade.
7. Uma funcionalidade compartilhada deve ser acessível por Sales Cloud e
   Service Cloud usando o mesmo conteúdo e identidade.

ARQUITETURA

Inspecione a stack existente e reutilize o que fizer sentido.
Se não existir app, escolha uma solução simples, estática quando viável,
com biblioteca de grafo adequada a múltiplos relacionamentos e expansão.
Não adotar biblioteca só porque foi citada em um rascunho.
Registre a escolha e suas limitações em uma nota curta.

Use adaptador entre catálogo e representação visual, sem embutir o
conteúdo técnico em componentes.
Use os índices/projeções gerados pela tarefa 1; acrescente apenas projeções
determinísticas dentro da pasta de insumos se necessário.
Separe ID canônico de ID de ocorrência visual quando um mesmo item
aparecer em caminhos distintos.
O build deve validar dados antes de gerar a aplicação.

Não expor credenciais Salesforce no cliente.
Não implementar chamadas autenticadas à org como requisito para navegar.
Não usar LLM em runtime para preencher lacunas de conhecimento.
Não executar exemplos SOQL/Apex no browser como consequência de um clique.
Não renderizar HTML arbitrário de conteúdo sem sanitização.

ACESSIBILIDADE E CARGA COGNITIVA

- Layout desktop com mapa e painel lateral.
- Em mobile, painel/gaveta com foco previsível e retorno ao mapa.
- Navegação por teclado e foco visível.
- Alternativa em lista/árvore com o mesmo conteúdo e relações.
- Nomes acessíveis para nós, controles e relações.
- Contraste, tamanho de texto legível, alvos de toque e reduced-motion.
- Não depender de hover, animação contínua ou somente cor.
- Preservar localização mental ao expandir; evitar rearranjos violentos.
- Oferecer modo leitura e “voltar ao caminho” para quem se perder.
- Explicar siglas na primeira ocorrência e separar resumo de aprofundamento.

QUALIDADE E TESTES

Implemente testes unitários do adaptador e de identificação/caminhos.
Implemente testes de integração/E2E sobre os percursos obrigatórios.
Faça testes visuais reais em browser desktop e mobile.

Verifique:
- Todos os tipos de nó possuem painel com os campos exigidos.
- A busca encontra um campo recolhido e abre seu caminho.
- Expandir/recolher não cria identidades duplicadas nem perde seleção.
- Trocar de visão preserva a identidade e ajusta o contexto.
- Selecionar relação/junção explica o vínculo e suas fontes.
- Nenhum campo é omitido silenciosamente por limite visual.
- Dados ausentes não viram mensagens tecnicamente falsas.
- Deep links e back/forward funcionam.
- Filtros, estados vazios, erros de carregamento e dados parciais são claros.
- Uso por teclado e modo lista funcionam sem canvas.
- Layout 360 px e desktop permanecem legíveis e utilizáveis.
- Build, lint e testes passam, ou falhas reais são explicitadas.

Teste performance no dataset real e em fixture sintética grande
claramente identificada como teste, nunca apresentada como conteúdo.
Meça carga inicial, expansão, busca e quantidade de nós renderizados;
registre ambiente e resultados em vez de prometer escalabilidade.
Não force carregar todas as propriedades no primeiro render.

ENTREGA

Implemente, não entregue apenas um plano.
No fim, informe:
- Local do código e comando para executar/testar/buildar.
- Local exato dos insumos consumidos.
- Funcionalidades e percursos entregues.
- Evidências dos testes executados.
- Cobertura dos dados e limitações visíveis na interface.
- Melhorias pendentes e bloqueios reais.

Não publicar, fazer deploy nem push nesta tarefa sem autorização.
Deixe a aplicação local pronta para revisão.
```
