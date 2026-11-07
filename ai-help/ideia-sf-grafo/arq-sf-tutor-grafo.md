Arquitetura para o projeto `sf-tutor`. Mas eu faria em **duas fases**, para não pedir ao Claude que crie tudo de uma vez e depois descobrir que o modelo de dados precisa mudar.

A lógica é:

```text
Fase 1 — criar a estrutura e os JSONs-fonte
Fase 2 — criar o gerador do tutorial visual em grafo
```

O Claude Code lê o repositório, segue convenções do `CLAUDE.md` e pode gerar documentação, testes e artefatos a partir da estrutura existente.  Para o tutorial visual, Mermaid é uma boa escolha porque usa nós e arestas em sintaxe de texto simples. [code.claude](https://code.claude.com/docs/en/common-workflows)

## Fase 1 — Estrutura e JSONs

Nesta fase, o objetivo é criar:

```text
1. Estrutura de pastas do repositório
2. JSON Schema que padroniza os arquivos
3. Índices por nuvem, classificação e certificação
4. JSONs completos por metadata type
5. Validação automática dos JSONs
6. Exportações CSV derivadas
```

A regra central é:

```text
Um JSON por metadata type = fonte da verdade.
Índices por nuvem/classificação/certificação = apenas navegação.
```

Assim, `CustomObject` terá **um único arquivo** com:

- Explicação do metadata type.
- Propriedades do XML.
- Propriedades internas, quando houver.
- Tabelas internas relacionadas.
- Campos das tabelas.
- Correspondência entre XML e tabela.
- Exemplo XML.
- Cuidados de CTA.

Os índices apenas apontam para esse arquivo.

## Fase 2 — Tutorial visual em grafo

Só depois de ter uma base mínima validada, você cria o gerador do tutorial.

Ele deve ler os JSONs e produzir:

```text
- Páginas Markdown por metadata type
- Grafos Mermaid por metadata type
- Grafos por classificação
- Glossário
- Trilha de estudo
- Quiz
- Mapa de dependências entre metadata types
```

O grafo não deve ser escrito manualmente: ele deve ser **gerado a partir dos JSONs**, para nunca dessincronizar.

## Prompt pronto para o Claude Code

Você pode colar isto no Claude Code, dentro do projeto `sf-tutor`:

```text
Quero criar um repositório chamado sf-tutor para armazenar e gerar
um tutorial visual e didático sobre o ecosistema Salesforce.

O repositório terá duas camadas:

1. Camada de dados
- Um arquivo JSON por metadata type.
- Cada JSON conterá:
  - explicação do metadata type
  - propriedades do XML
  - propriedades internas, quando houver
  - tabelas internas relacionadas
  - campos das tabelas internas
  - correspondência entre propriedades do XML e campos das tabelas
  - exemplo XML
  - cuidados de arquitetura e CTA

2. Camada de navegação
- Índices por nuvem
- Índices por classificação
- Índices por certificação
- Os índices não devem conter propriedades; apenas referenciam os JSONs.

Regras importantes:
- Não inventar propriedades, campos, valores ou relacionamentos.
- Se uma informação não estiver disponível, marcar como "a validar".
- Diferenciar claramente:
  - propriedade do XML
  - campo da tabela interna
  - API de acesso
  - relação entre metadata types
- Um metadata type pode ter uma, várias ou nenhuma tabela interna.
- Usar JSON como fonte primária.
- Gerar CSV apenas como exportação derivada.
- Usar Mermaid para os grafos.

Fase 1:
- Criar a estrutura de pastas.
- Criar o JSON Schema.
- Criar índices iniciais.
- Criar os primeiros JSONs completos.
- Criar script de validação.
- Criar script de exportação CSV.

Fase 2:
- Criar gerador de tutorial em Markdown.
- Criar gerador de grafo Mermaid.
- Gerar páginas por metadata type.
- Gerar grafos por metadata type e por classificação.

Antes de implementar:
- Apresente um plano.
- Mostre a estrutura de pastas proposta.
- Mostre o JSON Schema.
- Mostre um exemplo completo de JSON para CustomObject.
- Aguarde minha aprovação antes de criar os demais arquivos.
```

## Estrutura que ele deve criar

```text
sf-tutor/
├── CLAUDE.md
├── README.md
├── schema/
│   └── metadata-type.schema.json
├── data/
│   ├── metadata-types/
│   │   ├── core/
│   │   ├── marketing-cloud/
│   │   ├── b2c-commerce/
│   │   └── ecossistema/
│   ├── indexes/
│   │   ├── por-nuvem/
│   │   ├── por-classificacao/
│   │   └── por-certificacao/
│   └── examples/
├── content/
│   └── pt-BR/
├── graphs/
├── exports/
├── tools/
└── tests/
```

## Ordem de execução recomendada

```text
1. Criar estrutura de pastas
2. Criar JSON Schema
3. Criar CLAUDE.md
4. Criar índices iniciais
5. Criar JSONs piloto:
   - CustomObject
   - CustomField
   - Flow
   - Profile
   - User
6. Criar validador
7. Criar exportador CSV
8. Criar gerador de Markdown
9. Criar gerador de Mermaid
10. Só depois expandir para todos os metadata types
```

## Por que essa ordem funciona

Porque ela separa:

```text
dados → validação → conteúdo → visual
```

Assim, se o formato do JSON mudar, você corrige uma vez e regenera todo o tutorial e os grafos.

O Claude Code funciona melhor quando recebe uma especificação clara, valida o próprio trabalho e usa comandos/testes para fechar o ciclo.  O `CLAUDE.md` deve conter as regras estáveis do projeto, enquanto subagentes podem isolar tarefas específicas, como curadoria de JSON, geração de grafo e revisão didática. [code.claude](https://code.claude.com/docs/en/best-practices)

## Resposta direta

- **Sim, você consegue estruturar isso no Claude Code.**
- **Mas não peça “crie tudo” de uma vez.**
- **Primeiro, crie a estrutura e os JSONs-fonte.**
- **Depois, crie o gerador do tutorial visual em grafo.**
- **Use o prompt acima como ponto de partida.**
- **O resultado será um repositório GitHub com dados versionados, validação automática e tutorial gerado a partir deles.**
