# sf-tutor: especificação dos insumos e do tutorial em grafo

Este documento define o produto desejado e o contrato entre duas tarefas do Claude Code: produzir a base de conhecimento e construir o tutorial visual que a consome. É uma especificação proposta para este projeto, não uma taxonomia oficial da Salesforce nem uma declaração de que os rascunhos existentes estão tecnicamente corretos.

## Como usar os três arquivos

Coloque estes três arquivos em `ai-help/claude/insumos-grafo/` do repositório `sf-tutor`:

- `00-especificacao-grafo.md`: requisitos comuns às duas tarefas.
- `01-prompt-criar-insumos.md`: instrução para levantar, validar e gerar os dados.
- `02-prompt-criar-tutorial.md`: instrução para construir o tutorial a partir dos dados.

Primeiro execute o prompt da tarefa de insumos. Depois de os validadores passarem e de você revisar o exemplo navegável de dados, execute o prompt do tutorial. Não é necessário esperar o catálogo inteiro estar pronto para testar a interface; a interface deve mostrar explicitamente a cobertura parcial.

Repositório de referência: [millena84/sf-tutor](https://github.com/millena84/sf-tutor/tree/main).

Pasta obrigatória dos insumos: [ai-help/claude/insumos-grafo](https://github.com/millena84/sf-tutor/tree/main/ai-help/claude/insumos-grafo).

Referência de interação: [flavinho.pages.dev](https://flavinho.pages.dev). Foi examinada como inspiração de mapa, busca, filtros e painel de leitura, não como fonte de conteúdo Salesforce nem como código a ser copiado.

## Objetivo e público

Criar um tutorial visual, técnico e didático do ecossistema Salesforce, utilizável por pessoas que já conhecem a plataforma e por iniciantes. A navegação deve permitir entender conceitos, configurações, APIs, campos e relacionamentos sem exigir leitura prévia de XML ou conhecimento da organização do repositório.

O produto não é uma coleção de diagramas estáticos nem um grafo gigante sempre aberto. É uma experiência explorável em que o usuário escolhe um caminho, expande níveis e lê detalhes sem perder o contexto.

O primeiro inventário técnico completo terá escopo Salesforce Platform/Core, delimitado e versionado. A estrutura deve suportar outras nuvens/produtos e o mapa deve apresentá-los; não declarar outras nuvens completas enquanto não tiverem inventário e validação próprios.

## Decisão de navegação

O centro é o logotipo Salesforce, com identificação acessível em texto. O painel desse nó explica o ecossistema, os conceitos de org e plataforma, os principais contextos de produto, metadados, dados e APIs.

Existem duas visões sobre o MESMO catálogo:

```text
Visão inicial: por funcionalidade
Salesforce
  → classificação funcional
    → sub-classificação
      → funcionalidade
        → XML / metadata type
          → propriedade
        → objeto exposto por API
          → campo

Visão alternativa: por nuvem/produto
Salesforce
  → nuvem/produto
    → classificação aplicável
      → sub-classificação aplicável
        → a mesma funcionalidade
          → as mesmas representações e campos
```

Recomendação adotada: abrir por classificação funcional e permitir trocar para “Por nuvem”. A classificação facilita estudar capacidades compartilhadas sem duplicá-las em Sales Cloud e Service Cloud. A escolha é didática, não uma afirmação sobre infraestrutura física ou uma hierarquia comercial oficial.

Uma funcionalidade pode pertencer a várias nuvens e a mais de uma classificação. A interface pode criar ocorrências visuais do mesmo item em caminhos diferentes, mas todos apontam para a mesma identidade canônica e o mesmo conteúdo.

“Salesforce Platform/Core” é tratado como plataforma/camada compartilhada no catálogo, e não como a mãe universal de todos os produtos. Não colocar automaticamente Marketing Cloud Engagement, MuleSoft, Tableau, Slack ou quaisquer outros produtos dentro da mesma org, runtime ou API. Validar o contexto técnico de cada produto.

Sales Cloud, Service Cloud, Salesforce Platform/Core e Data Cloud são entradas iniciais solicitadas para o mapa. Registrar nomes oficiais atuais e aliases históricos separadamente; uma mudança de nome não deve quebrar IDs ou buscas. Outros produtos devem ser descobertos e documentados, não presumidos como completos.

## O ajuste necessário: funcionalidade não é sinônimo de metadata type

A unidade didática é a funcionalidade. Ela pode ter zero, um ou vários metadata types, objetos de API ou artefatos de código associados.

Isso permite representar “Usuários / User” sem criar um metadata type ou um XML fictício. O guia da Metadata API distingue explicitamente metadata components de sObjects e mostra que nem toda estrutura auxiliar é um metadata type independente. [Metadata Components and Types](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_objects_intro.htm)

O objeto `User` é documentado para consulta, provisionamento e alteração de usuários da organização. Não converter seus campos em propriedades de um XML de Metadata API por analogia. [User](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_user.htm)

Também não chamar cada funcionalidade comercial de metadata type. Por exemplo, processos, interfaces e estratégias de execução precisam ser vinculados aos mecanismos técnicos realmente documentados, em vez de receber nomes de tipos inventados.

### Sobre “tabela interna”

Na interface, preferir “Objeto consultável via API”, com uma explicação de que esse é o objeto exposto publicamente. Pode-se manter “objeto interno relacionado” como termo didático, mas nunca afirmar que o catálogo documenta tabelas físicas privadas do banco da Salesforce.

O mapeamento entre metadata types e tipos de dados não é necessariamente direto. Uma associação deve ter justificativa e evidência, e não apenas semelhança de nome. [Metadata Types](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm)

## Taxonomia funcional proposta

Esta árvore é uma organização didática inicial. O Claude deve cruzá-la com a documentação oficial, preservar os nomes oficiais dos itens e registrar referências documentais em cada agrupamento. Não apresentar esta divisão como classificação literal e única da Salesforce.

Uma funcionalidade recebe uma classificação principal e classificações secundárias opcionais. “Relacionada a dados” não significa que toda interface deva ficar fisicamente sob “Dados”: relações transversais resolvem esse caso.

| Classificação | Sub-classificações a desenvolver |
|---|---|
| Organização e configurações base | Identificação e configuração da org; Settings; parâmetros reutilizáveis; localização, idiomas e tradução; moedas e calendário fiscal; horários comerciais e feriados; domínios e URLs; habilitação de recursos |
| Acesso, identidade e segurança | Usuários e provisionamento; autenticação, SSO e MFA; sessões e políticas de login; permissões, perfis e grupos; licenças e entitlements de acesso; acesso a registros e hierarquias; credenciais, certificados e proteção de dados |
| Dados e modelagem | Objetos e entidades; campos e tipos; relacionamentos e junções; tipos de registro e processos de negócio; listas de valores; metadados de configuração de dados; modelos externos e especializações |
| Qualidade, governança e ciclo de vida dos dados | Validação; duplicidade e correspondência; classificação e sensibilidade; retenção, arquivamento e exclusão; rastreabilidade e histórico; consentimento e privacidade |
| Automação de processos e regras de negócio | Flow e orquestração; decisões e aprovações; ações e regras; automação Apex; notificações; mecanismos legados e migração |
| Interface e experiência do usuário | Aplicativos e navegação; tabs; layouts e páginas de registro; Lightning pages e componentes; ações rápidas; orientação visual e Path; experiências web/portais e mobile; acessibilidade e personalização |
| Execução assíncrona, lotes e agendamento | Batch; Queueable; Future e mecanismos legados quando aplicáveis; agendamento; caminhos assíncronos; processamento orientado a eventos; monitoramento de jobs e limites |
| Integração, APIs e eventos | APIs de dados e metadados; autenticação de integrações; chamadas externas e endpoints; credenciais; eventos e mensageria; conectividade e virtualização de dados; contratos, limites e tratamento de falhas |
| Relatórios, analytics e exploração | Reports; dashboards; tipos de relatório; pastas e acesso; métricas e agregações; recursos analíticos específicos de produto |
| Conteúdo, conhecimento e colaboração | Files e documentos; bibliotecas e assets; Knowledge e categorias; colaboração; templates e comunicação |
| Desenvolvimento, testes e entrega | Código e bundles; testes; pacotes e dependências; source format e Metadata API format; ambientes e sandboxes; versionamento, deploy e recuperação |
| Observabilidade, auditoria e operação | Logs e rastreamento; auditoria de configuração; histórico de login; eventos de monitoramento; limites e consumo; jobs, incidentes e diagnóstico |
| IA, agentes e decisões assistidas | Configuração de agentes; ações e tópicos; prompts; modelos e grounding; recursos de recuperação de conhecimento; segurança, avaliação e governança de IA |
| Processos de negócio específicos de produto | Vendas; atendimento; serviço de campo; receita e comércio; experiências externas; capacidades setoriais; outras áreas encontradas no inventário oficial |

Exemplos a classificar e validar: `Profile`, `PermissionSet`, `PermissionSetGroup`, `User`, `UserLogin`, `LoginHistory`, `CustomObject`, `CustomField`, `RecordType`, `PathAssistant`, `FlexiPage`, `QuickAction`, `CustomTab` e `ValidationRule`. Essa relação é uma semente, não o inventário completo.

Não criar `IpLogin` só porque apareceu como dúvida na conversa. Investigar o conceito pretendido e relacionar objetos e configurações documentados. `UserLogin` e `LoginHistory`, por exemplo, têm propósitos diferentes descritos nas respectivas referências. [UserLogin](https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-userlogin.html), [LoginHistory](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_loginhistory.htm)

## Conteúdo exigido em cada nó

### Salesforce, nó central

- O que é o ecossistema e como o mapa está organizado.
- Conceitos técnicos fundamentais: org, produto, plataforma, funcionalidade, metadado, registro e API.
- Relações entre contextos de produto, sem prometer uma única infraestrutura para todos.
- Versão/data da base, escopo e cobertura alcançada.
- Explicação de como navegar e ler as relações.

### Nuvem ou produto

- Nome oficial, aliases, contexto tecnológico e resumo técnico.
- O que é, para que serve e casos de uso.
- Licenças e requisitos relacionados, com fontes e data.
- Diferenciar licença de usuário, licença de permission set, edição e add-on.
- Visão geral das funcionalidades relacionadas.
- Capacidades próprias e capacidades compartilhadas.
- Dependências, limites e pontos de atenção conhecidos.

Não inferir licenciamento pela presença de um metadata type e não prometer funcionalidades para todas as edições. Não incluir preços sem necessidade explícita.

### Classificação e sub-classificação

- Nome, explicação acessível e escopo do agrupamento.
- Tipos de funcionalidades incluídos e exemplos.
- Pré-requisitos e conceitos técnicos relevantes.
- O que fica fora e onde procurar assuntos relacionados.
- Natureza da classificação: curadoria didática ou agrupamento documental oficial.
- Referências oficiais que sustentam o conteúdo.

### Funcionalidade

- Nome em português, nome técnico, aliases e termos de busca.
- O que é, para que serve, exemplo prático e pré-requisitos.
- Nuvens e classificações relacionadas, sem duplicação do cadastro.
- Representações disponíveis: XML, objetos API, código ou configuração de interface.
- Caminho de acesso pelo Setup, se documentado; idioma e contexto.
- Recomendações, boas práticas, pontos de atenção e limitações.
- Quando não houver Setup, XML ou objeto equivalente, declarar isso.

### XML / metadata type

- Nome técnico, explicação, finalidade e referência oficial.
- Nome da pasta no projeto Salesforce, padrão de nome físico e extensão.
- Distinguir source format do formato Metadata API; informar decomposição e arquivos associados quando aplicável.
- Caminho no Setup, quando houver e estiver validado.
- Exemplo XML didático, com namespace e estrutura correta, sem dados pessoais.
- Todas as propriedades documentadas no escopo/versionamento, inclusive herdadas e tipos compostos.
- Relações com objetos API e outras configurações; natureza e limites da correspondência.
- Boas práticas, alertas, dependências e cobertura por canal quando verificada.

Não inventar um elemento `<CustomField>` dentro de `<fields>` apenas porque o tipo de dado desse elemento é `CustomField`. Extrair a serialização da fonte, não converter nomes de tipos automaticamente em tags.

### Objeto consultável via API

- Nome técnico, label, finalidade e papel em relação à funcionalidade.
- APIs de acesso, como lista: padrão, Tooling, ambas quando comprovado ou acesso específico de produto.
- Operações realmente suportadas: consulta, criação, atualização, exclusão e describe.
- Exemplo de SOQL e endpoint/contexto corretos; exemplo Apex apenas se aplicável.
- Restrições de consulta, filtros obrigatórios, permissões, edição, versão e licença.
- Caminho no Setup, quando houver; caso contrário, “não aplicável”.
- Lista completa de campos no universo documentado, com cobertura e lacunas explícitas.
- Correspondências comprovadas com XML e relações com outros objetos.
- Boas práticas, cuidados e limitações.

A opção “API padrão ou Tooling” não deve ser um enum mutuamente exclusivo. Também não misturar Bulk/Streaming/Metadata como se fossem sinônimos de tabelas consultáveis por SOQL.

Uma consulta Apex comum não deve ser oferecida como acesso nativo a um objeto disponível apenas em Tooling. Se houver exemplo de chamada HTTP a Tooling a partir de Apex, identificá-lo como callout e explicitar suas condições, sem exigir sua implementação nesta fase.

### Propriedade XML e campo de objeto API

Ambos precisam do mesmo nível didático, respeitando diferenças técnicas:

- Nome técnico, label oficial quando existir e rótulo didático separado.
- Tipo técnico e tipo explicado; cardinalidade/lista quando aplicável.
- O que é, para que serve e qual efeito produz ou qual informação representa.
- Origem: padrão da plataforma, customizado ou não aplicável.
- Obrigatoriedade: sim, não, condicional, desconhecida ou não aplicável.
- Condições de obrigatoriedade e de disponibilidade.
- Valor padrão, com distinção entre ausência, `null`, `false`, string vazia e informação desconhecida.
- Valores possíveis, significado de cada valor e indicação se a enumeração é fechada, dinâmica ou condicionada.
- Restrições: tamanho, precisão, escala, formato, dependências, fórmula e referência, quando documentadas.
- Exemplo didático.
- Versão, licença/recurso quando aplicável e fontes que sustentam as afirmações.
- Correspondência XML/API quando comprovada, com condição e natureza: direta, parcial, transformada, nenhuma ou desconhecida.

Para campos API, acrescentar nulabilidade, leitura/escrita, criação/atualização, cálculo, default no create, filtros, ordenação, agrupamento, referências e nomes de relacionamento, conforme a documentação/describe. Um campo read-only deve dizer “representa/informa”, não “configura”.

Não deduzir obrigatoriedade de escrita só porque um campo não é nillable. Não tratar `minOccurs` do WSDL como toda a regra funcional; condições adicionais precisam de documentação.

“Padrão” deve ser desambiguado: origem standard/custom não é valor default. Propriedades nativas do schema não se tornam propriedades customizadas só porque configuram um componente customizado.

Para strings abertas, não inventar uma lista de valores. Para listas dependentes de org, tradução ou tipo de registro, declarar o contexto e os limites da fonte.

### Relacionamentos e objetos de junção

Um objeto de junção tem o mesmo nível de documentação de qualquer outro objeto API, incluindo todos os campos. Não ocultá-lo atrás de uma linha sem explicação.

Exemplo de navegação exigido:

```text
Usuários
  → objeto User
    → campo Id
    → campo ProfileId → objeto Profile

Permission sets
  → metadata type PermissionSet → suas propriedades XML
  → objeto PermissionSet → seus campos

User
  ← PermissionSetAssignment.AssigneeId
PermissionSet
  ← PermissionSetAssignment.PermissionSetId
PermissionSetGroup
  ← PermissionSetAssignment.PermissionSetGroupId
```

`PermissionSetAssignment` representa atribuições de permission sets ou grupos a usuários; os campos de relacionamento e suas referências são documentados oficialmente. O grafo deve representar cada vínculo por seus campos, sem inferir que todos os campos opcionais estão preenchidos em toda atribuição. [PermissionSetAssignment](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_permissionsetassignment.htm)

Não rotular “1 metadata type e vários objetos relacionados” como cardinalidade de registros. Separar quantidade de representações técnicas da cardinalidade do relacionamento entre registros.

## Organização dos insumos

Toda a base, suas ferramentas, esquemas, testes, relatórios e instruções locais devem ficar sob:

```text
ai-help/claude/insumos-grafo/
```

Estrutura proposta:

```text
insumos-grafo/
├── 00-especificacao-grafo.md
├── 01-prompt-criar-insumos.md
├── 02-prompt-criar-tutorial.md
├── README.md
├── CLAUDE.md
├── config/
│   ├── escopo.json
│   └── versoes.json
├── schemas/
├── catalogo/
│   ├── salesforce.json
│   ├── nuvens/
│   ├── classificacoes/
│   ├── subclassificacoes/
│   ├── funcionalidades/
│   ├── metadata-types/
│   ├── objetos-api/
│   └── relacionamentos/
├── fontes/
│   ├── registro.json
│   └── snapshots/
├── inventarios/
├── exemplos/
├── ferramentas/
├── testes/
├── relatorios/
└── gerado/
    ├── fichas-completas/
    └── grafo/
```

Os nomes podem ser ajustados pelo Claude se necessário, mas a pasta-raiz obrigatória, os papéis e as garantias devem ser mantidos. Não criar diretórios ou arquivos desnecessários para fingir progresso.

### O que fica em cada JSON

- Nuvem/produto: descrição técnica, licenças, funcionalidades e referências. É um índice ENRIQUECIDO, não apenas uma lista de arquivos e não uma cópia de todas as propriedades.
- Classificação/sub-classificação: descrição técnica e didática, fronteiras e referências para seus itens.
- Funcionalidade: ficha didática e referências para suas representações técnicas.
- Metadata type: ficha do tipo e todas as propriedades XML; vínculos com objetos API.
- Objeto API: definição e todos os seus campos, suas exposições por API e diferenças entre elas.
- Relacionamento: origem, destino, campos de ligação, natureza, cardinalidade de registros quando conhecida e evidência.

O conteúdo técnico de um objeto compartilhado deve ser mantido em um só cadastro. Um gerador produzirá `gerado/fichas-completas/<MetadataType>.json` com as propriedades XML E as informações completas de todos os objetos relacionados e de seus campos, como solicitado na conversa. Assim, um agente pode consumir uma ficha completa sem resolver referências, mas não há manutenção manual duplicada.

Os arquivos em `gerado/` são produtos determinísticos dos cadastros, nunca segunda fonte manual. IDs e referências são detalhes de implementação; a pessoa que aprende não precisa compreender “nodes/edges/domains” para usar ou manter a ficha.

Não duplicar um metadata type em uma pasta por nuvem: as nuvens referenciam o mesmo tipo. Contexto de produto, família de API e versão devem impedir colisões de nomes.

## Rastreabilidade e completude

Cada afirmação técnica deve ser rastreável a uma fonte oficial, uma evidência de schema ou uma observação autorizada em org. Definir `source_id`, URL exata, seção/âncora quando disponível, versão, data de verificação e status.

Explicações, analogias e classificações didáticas devem ser identificadas como curadoria, sem fingir que são labels oficiais. Recomendações devem separar orientação oficial, inferência técnica fundamentada e preferência do projeto.

Não confundir estes estados:

- Desconhecido: ainda não investigado ou sem evidência suficiente.
- Não aplicável: o atributo não faz sentido para aquele item.
- Não exposto: uma fonte verificada documenta a indisponibilidade.
- Bloqueado: falta fonte, acesso, licença ou outra condição.
- Verificado: informação confirmada para a versão e o contexto declarados.

Uma lista vazia de objetos relacionados não comprova que nenhum existe. Deve vir acompanhada do resultado da investigação. O mesmo vale para valores de enum, propriedades e campos.

Os inventários devem separar:

- Tipos e campos disponíveis na documentação da versão.
- Tipos e campos observados em uma org específica.
- Tipos auxiliares do schema versus metadata types implantáveis.
- Recursos incluídos, excluídos e ainda não classificados no recorte Core.
- Completude estrutural versus completude das explicações e dos mapeamentos API.

Nenhum único WSDL, describe ou retrieve de uma org prova cobertura de todo o ecossistema, todas as licenças e todos os campos de todas as versões. `sObject Describe` descreve campos e relacionamentos do objeto no contexto acessado; usar o resultado com esse escopo declarado. [sObject Describe](https://developer.salesforce.com/docs/platform/api-rest/guide/resources-sobject-describe.html)

O relatório deve mostrar contagens, denominadores e lacunas concretas, por exemplo: tipos esperados/inventariados, propriedades esperadas/extraídas/explicadas, objetos API identificados/documentados e relações verificadas. Se não existir denominador confiável, registrar isso em vez de apresentar porcentagem falsa.

## Experiência do tutorial

A referência usa um mapa com filtros e um painel de leitura. Reaproveitar esse princípio de interação, mas adotar identidade própria e todos os requisitos Salesforce deste documento. [Página de inspiração](https://flavinho.pages.dev)

Requisitos:

- Logo Salesforce no centro, com licença/origem do asset registrada e sem sugerir afiliação oficial.
- Alternância “Por funcionalidade / Por nuvem”.
- Expansão progressiva, recolhimento, zoom, pan, reenquadramento e retorno ao centro.
- Painel lateral com conteúdo do nó selecionado; gaveta ou tela equivalente no celular.
- Clicar em nó lê detalhes; ação explícita expande/recolhe. Uma ação não deve destruir a outra.
- Busca em português e por nomes técnicos, labels e aliases, inclusive propriedades/campos ainda não carregados visualmente.
- Filtros por nuvem, classificação, tipo de representação, API e estado de validação.
- Tipos visuais distintos para agrupamentos, funcionalidades, XMLs, objetos API, campos e junções, sem depender só de cor.
- Relações de navegação e relações técnicas distinguíveis; cada conexão técnica pode ser selecionada para explicar “por que estes itens se relacionam”.
- Breadcrumbs e destaque do caminho atual, com referências cruzadas entre nuvens.
- Todos os campos e propriedades devem ser alcançáveis, sem despejar milhares de nós na abertura.
- Detalhes de licença, fontes, versão, limitações e cobertura visíveis.
- Exemplo XML/consulta com cópia de código e sintaxe legível.
- Modo de leitura/lista equivalente, acessível por teclado e leitor de tela.
- Animação reduzível, foco previsível, textos curtos por bloco e informações técnicas recolhíveis.
- Estado navegável na URL, com ID canônico e caminho contextual quando necessário.
- Sem IA em runtime para inventar explicações ausentes e sem credenciais Salesforce no frontend.

Mermaid pode ser uma exportação complementar. Um diagrama Mermaid estático, sozinho, não atende à experiência de exploração solicitada.

## Evidências consultadas e limitações desta especificação

O repositório foi examinado em 2026-11-07, no commit `adf18b7e15e3fbb7cf5af07bddd0ca486c007a80`. Os documentos anteriores são insumos de intenção e hipóteses técnicas, não um catálogo já validado; esta especificação exige sua auditoria antes de reaproveitar afirmações.

Esta entrega contém instruções e critérios, não os JSONs de todos os tipos nem o site implementado. Ela não confirma todas as classificações, licenças, campos ou mapeamentos do futuro catálogo.

Fontes oficiais de partida efetivamente consultadas nesta preparação:

- [Understanding Metadata API](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_intro.htm): escopo de metadados, dados e componentes.
- [Metadata Components and Types](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_objects_intro.htm): tipos, componentes, estruturas auxiliares e enums.
- [Metadata Types](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm): limites de correspondência entre tipos.
- [Metadata Coverage Report](https://developer.salesforce.com/docs/metadata-coverage): ponto de partida da cobertura. A captura textual consultada não expôs a matriz completa; o Claude deve verificá-la antes de preencher suporte.
- [User](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_user.htm): finalidade do objeto.
- [PermissionSetAssignment](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_permissionsetassignment.htm): atribuições e referências.
- [UserLogin](https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-userlogin.html) e [LoginHistory](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_loginhistory.htm): identidade e histórico.
- [sObject Describe](https://developer.salesforce.com/docs/platform/api-rest/guide/resources-sobject-describe.html): campos, URLs e relacionamentos do objeto.
- [Salesforce CLI: sobject describe](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_sobject_describe.html): saída JSON e opção `--use-tooling-api`.

Os links de fontes exportados anteriormente na conversa não foram todos verificados. O Claude deve validar a pertinência do conteúdo, não apenas receber HTTP 200, antes de incorporá-los ao registro de evidências.
