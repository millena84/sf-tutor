Listando os pontos chave da ideia inicial:

> **Não será um JSON por nuvem contendo tudo.**  
> **Será um JSON por metadata type**, contendo a explicação do tipo, as propriedades do XML, a tabela interna relacionada e os campos dessa tabela.  
> **Os arquivos por nuvem/classificação/certificação serão apenas índices**, que apontam para os JSONs dos metadata types.

Isso evita duplicação: `CustomObject` pode pertencer ao CORE, à classificação “Dados e modelo” e à trilha CTA, mas as propriedades dele são escritas **uma única vez**.

## Estrutura de arquivos

```text
salesforce-metadata-tutorial/
│
├── metadata-types/                  ← FONTE DA VERDADE
│   ├── core/
│   │   ├── CustomObject.json
│   │   ├── CustomField.json
│   │   ├── Flow.json
│   │   ├── Profile.json
│   │   └── User.json
│   │
│   ├── marketing-cloud/
│   │   ├── DataExtension.json
│   │   └── Journey.json
│   │
│   ├── b2c-commerce/
│   │   ├── Cartridge.json
│   │   └── Product.json
│   │
│   └── ecossistema/
│       ├── MuleSoftAPI.json
│       ├── TableauWorkbook.json
│       └── SlackApp.json
│
├── indexes/                         ← APENAS NAVEGAÇÃO
│   ├── por-nuvem/
│   │   ├── core.json
│   │   ├── marketing-cloud.json
│   │   ├── b2c-commerce.json
│   │   └── ecossistema.json
│   │
│   ├── por-classificacao/
│   │   ├── organizacao-e-base.json
│   │   ├── dados-e-modelo.json
│   │   ├── seguranca-e-acesso.json
│   │   ├── automacao.json
│   │   ├── interface.json
│   │   ├── integracao.json
│   │   └── devops.json
│   │
│   └── por-certificacao/
│       ├── application-architect.json
│       ├── system-architect.json
│       └── cta.json
│
└── exports/
    ├── metadata_fields.csv
    └── metadata_types.csv
```

## Regra de ouro

```text
Propriedades vivem em UM lugar só:
metadata-types/<nuvem>/<MetadataType>.json

Nuvem, classificação e certificação são apenas índices:
indexes/...
```

Ou seja:

| Pergunta | Resposta |
|---|---|
| Um JSON por nuvem? | **Não**, para propriedades |
| Um JSON por metadata type? | **Sim** |
| Onde ficam as propriedades do XML? | No JSON do metadata type |
| Onde ficam a tabela interna e os campos? | No mesmo JSON do metadata type |
| Onde fica a explicação didática? | No mesmo JSON do metadata type |
| O que fica no JSON por nuvem? | Apenas a lista de metadata types daquela nuvem |
| O que fica no JSON por classificação? | Apenas a lista de metadata types daquele tema |
| O que fica no JSON por certificação? | Apenas a lista de metadata types daquela trilha |

## Estrutura do JSON por metadata type

Cada arquivo terá **três grandes blocos**:

```text
1. Identificação e explicação do metadata type
2. Propriedades do XML
3. Tabelas internas relacionadas e seus campos
```

### Estrutura base

```json
{
  "metadata_type": "CustomObject",
  "label": "Custom Object",
  "nuvem": "CORE",
  "categorias": [
    "Dados e modelo relacional",
    "DevOps",
    "Segurança e acesso"
  ],
  "o_que_e": "Define um objeto customizado no Salesforce.",
  "para_que_serve": "Criar estruturas de dados próprias, como casos de fraude, transações ou atendimentos.",
  "arquivo_xml": "objects/FraudCase__c/FraudCase__c.object-meta.xml",
  "propriedades": [],
  "tabelas_internas": [],
  "exemplo_xml": "",
  "cuidados_cta": []
}
```

## Bloco 1 — Explicação do metadata type

Este bloco responde:

```text
- O que é?
- Para que serve?
- Em qual nuvem vive?
- A quais classificações pertence?
- Onde fica o XML?
- Quais cuidados de CTA existem?
```

## Bloco 2 — Propriedades do XML

Cada propriedade do XML vira um item da lista `propriedades`.

```json
{
  "nome": "deploymentStatus",
  "label": "Deployment Status",
  "tipo": "lista de opções",
  "obrigatoria": true,
  "default": "InDevelopment",
  "o_que_e": "Situação de implantação do objeto.",
  "o_que_configura": "Se o objeto está disponível para uso.",
  "valores_possiveis": [
    {
      "valor": "InDevelopment",
      "significado": "Objeto ainda em desenvolvimento",
      "default": true
    },
    {
      "valor": "Deployed",
      "significado": "Objeto disponível para uso",
      "default": false
    }
  ],
  "exemplo": "Deployed"
}
```

Se uma propriedade tiver subpropriedades, elas entram em `propriedades_internas`.

```json
{
  "nome": "nameField",
  "label": "Name Field",
  "tipo": "objeto",
  "obrigatoria": true,
  "o_que_e": "Campo que identifica o registro.",
  "o_que_configura": "Nome exibido do registro.",
  "propriedades_internas": [
    {
      "nome": "label",
      "label": "Label",
      "tipo": "texto",
      "obrigatoria": true,
      "o_que_e": "Nome exibido do campo de identificação.",
      "o_que_configura": "Rótulo do campo de nome."
    },
    {
      "nome": "type",
      "label": "Type",
      "tipo": "lista de opções",
      "obrigatoria": true,
      "o_que_e": "Tipo do campo de nome.",
      "o_que_configura": "Se o nome será texto ou numeração automática.",
      "valores_possiveis": [
        {
          "valor": "Text",
          "significado": "Nome em texto livre"
        },
        {
          "valor": "AutoNumber",
          "significado": "Número gerado automaticamente"
        }
      ]
    }
  ]
}
```

## Bloco 3 — Tabelas internas e campos

Cada metadata type pode ter:

- **uma tabela interna**;
- **várias tabelas internas**;
- **nenhuma tabela diretamente consultável**.

Por isso, `tabelas_internas` é uma **lista**.

```json
{
  "tabelas_internas": [
    {
      "nome_tabela": "EntityDefinition",
      "label": "Entity Definition",
      "api": "Tooling API",
      "relacao": "1-para-n",
      "papel": "Representa a definição de objetos padrão e customizados.",
      "consulta_exemplo": "SELECT QualifiedApiName, Label FROM EntityDefinition",
      "campos": [
        {
          "nome_campo": "QualifiedApiName",
          "label": "Qualified API Name",
          "tipo": "string",
          "obrigatorio": true,
          "default": "",
          "o_que_e": "Nome API qualificado do objeto.",
          "o_que_configura": "Identificação única do objeto.",
          "valores_possiveis": [],
          "exemplo": "FraudCase__c",
          "correspondencia_xml": "CustomObject.fullName",
          "tipo_correspondencia": "direta"
        }
      ]
    }
  ]
}
```

Cada campo da tabela usa **o mesmo nível de informação** das propriedades do XML:

| Campo | Função |
|---|---|
| `nome_campo` | Nome técnico no banco/API |
| `label` | Nome amigável |
| `tipo` | Tipo de dado |
| `obrigatorio` | Se é obrigatório |
| `default` | Valor padrão |
| `o_que_e` | Explicação simples |
| `o_que_configura` | Efeito prático |
| `valores_possiveis` | Domínio de valores |
| `exemplo` | Exemplo real |
| `correspondencia_xml` | Propriedade do XML relacionada |
| `tipo_correspondencia` | `direta`, `derivada`, `parcial` ou `inexistente` |

## Exemplo de correspondência

```text
XML: CustomObject.fullName
Tabela: EntityDefinition.QualifiedApiName
Relação: direta
```

```text
XML: CustomObject.sharingModel
Tabela: EntityDefinition.SharingModel (quando aplicável)
Relação: direta ou derivada
```

```text
XML: CustomObject.fields
Tabela: FieldDefinition
Relação: 1-para-n
```

## O que fica no índice por nuvem

O índice **não repete propriedades**. Ele apenas lista os metadata types.

```json
{
  "nuvem": "CORE",
  "label": "Salesforce Core Platform",
  "descricao": "Plataforma base compartilhada pelas nuvens do core.",
  "metadata_types": [
    {
      "metadata_type": "CustomObject",
      "label": "Custom Object",
      "arquivo": "../metadata-types/core/CustomObject.json"
    },
    {
      "metadata_type": "CustomField",
      "label": "Custom Field",
      "arquivo": "../metadata-types/core/CustomField.json"
    }
  ]
}
```

## O que fica no índice por classificação

```json
{
  "classificacao": "Dados e modelo relacional",
  "label": "Dados e modelo",
  "descricao": "Metadata types que definem objetos, campos e qualidade de dados.",
  "metadata_types": [
    {
      "metadata_type": "CustomObject",
      "arquivo": "../metadata-types/core/CustomObject.json"
    },
    {
      "metadata_type": "CustomField",
      "arquivo": "../metadata-types/core/CustomField.json"
    }
  ]
}
```

## O que fica no índice por certificação

```json
{
  "certificacao": "CTA",
  "label": "Certified Technical Architect",
  "trilhas": [
    {
      "nome": "Dados e modelo",
      "metadata_types": [
        "CustomObject",
        "CustomField"
      ]
    },
    {
      "nome": "Segurança e acesso",
      "metadata_types": [
        "Profile",
        "PermissionSet"
      ]
    }
  ]
}
```

## Como o agente usa

```text
1. Usuário escolhe: CORE → Dados e modelo → CustomObject
2. Agente abre o índice por classificação
3. Índice aponta para metadata-types/core/CustomObject.json
4. Agente lê propriedades, tabelas internas e campos
5. Agente monta a página do tutorial
```

## Resumo final

```text
1 JSON por metadata type = fonte da verdade
1 JSON por nuvem = índice de navegação
1 JSON por classificação = índice de navegação
1 JSON por certificação = índice de navegação
```

Dentro do JSON do metadata type:

```text
- explicação do metadata type
- propriedades do XML
- propriedades internas, quando houver
- tabelas internas relacionadas
- campos das tabelas
- correspondência entre XML e tabela
- exemplo XML
- cuidados de CTA
```

Isso está alinhado ao modelo do Salesforce: um metadata type descreve uma categoria de configuração, e um metadata component é uma instância dessa categoria; a Metadata API trabalha com essas definições e representações XML.  JSON suporta exatamente esse tipo de estrutura: objetos, arrays e aninhamento para representar hierarquias e relações. [help.salesforce](https://help.salesforce.com/s/articleView?id=platform.code_tools_websvcAPI.htm&language=en_US&type=5)
