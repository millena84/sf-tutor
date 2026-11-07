# Auditoria dos insumos anteriores

Data: 2026-11-07. Base de comparação: documentação oficial da Salesforce na API 68.0 (Winter '27) e a lista de 993 metadata types da v68 publicada em `METADATA_SUPPORT.md` (forcedotcom/source-deploy-retrieve, commit `d09d2cc`).

Os documentos auditados foram tratados como requisitos, exemplos e hipóteses. Nenhum foi alterado. As correções abaixo valem para a base nova em `catalogo/`; o histórico original fica preservado.

## Escopo e método

Documentos lidos:

- `README.md`;
- `ai-help/fontes.md`;
- `ai-help/ideia-sf-grafo/` (2 arquivos);
- `ai-help/internal-obj/` (1 arquivo);
- `ai-help/perplexity/` (6 arquivos, lidos por seções e trechos-chave);
- `ai-help/claude/tarefas/` (especificação e prompts).

A conferência teve duas etapas:

1. **Automática.** O comando `python3 ferramentas/sftutor.py auditar-rascunhos` extrai os identificadores entre crases iniciados em maiúscula e os compara com a lista oficial v68 e com os objetos catalogados. Resultado em `inventarios/rascunhos-nomes.json`: **814 nomes**.
   - 225 são metadata types da lista v68.
   - 2 são objetos API já catalogados.
   - 587 não foram confirmados. Isso **não** significa que não existam: podem ser objetos, campos, enums, produtos ou nomes inventados.
2. **Manual.** Os pontos estruturais abaixo foram conferidos manualmente contra as fontes registradas em `fontes/registro.json`.

## Divergência de localização dos arquivos de tarefa

A especificação, o prompt da tarefa 1 e as instruções do projeto citam `ai-help/claude/insumos-grafo/00-especificacao-grafo.md`. No repositório, os três arquivos estão em `ai-help/claude/tarefas/`. Em `insumos-grafo/` havia apenas um arquivo vazio chamado `draft`, que foi mantido.

**Decisão:** os arquivos de tarefa não foram movidos nem copiados, porque o prompt proíbe sobrescrever esses documentos sem autorização. A base usa `tarefas/` como referência. A decisão final fica com a dona do repositório.

## Achados e correções

### 1. Unidade do modelo e organização por nuvem

Documentos: `ideia-sf-grafo/draft-sf-tutor-v1.md` e `ideia-sf-grafo/arq-sf-tutor-grafo.md`.

| Rascunho | Problema | Correção na base |
|---|---|---|
| "Um JSON por metadata type = fonte da verdade" | Contradiz a especificação: a unidade didática é a funcionalidade, que pode ter zero, um ou vários metadata types. | Cadastros separados por funcionalidade, metadata type, objeto API e relacionamento (`catalogo/`). |
| `metadata-types/core/User.json` | `User` não está entre os 993 metadata types da v68. Usuários são registros do objeto `User`. | `func:usuarios` não tem metadata type, com ausência justificada e evidenciada. O objeto fica em `catalogo/objetos-api/User.json`. Um teste impede o retorno do erro. |
| Pastas `metadata-types/<nuvem>/` | Duplicaria tipos compartilhados entre nuvens. | Pasta única por categoria; as nuvens só referenciam funcionalidades. |
| `DataExtension`, `Journey`, `Cartridge`, `MuleSoftAPI`, `TableauWorkbook`, `SlackApp` como metadata types | Nenhum está na lista v68 da Metadata API. Pertencem a produtos com contexto próprio ou são nomes não confirmados. | Fora do recorte (`config/escopo.json`, critério X1). Não foram cadastrados. |
| Índices por certificação, quiz, trilha de estudo | Fora do escopo solicitado. | Não criados. |
| Mermaid como saída principal | A especificação exige exploração interativa; Mermaid seria só uma exportação complementar. | A projeção é `gerado/grafo/` (nós, arestas, visões, busca). |
| "Apresente um plano e aguarde aprovação" | Substituído pelo prompt atual da tarefa 1. | Implementação executada. |

### 2. "Tabelas internas" e correspondências

Documento: `draft-sf-tutor-v1.md`.

- **"Tabela interna" com `api: "Tooling API"`.** O rascunho tratava a API como valor único e o objeto como tabela.
  - Na base, o objeto se chama "objeto consultável via API".
  - `exposicoes` é uma lista por API, cada uma com estado próprio (ex.: `obj:ValidationRule` está verificado na Tooling API e não exposto na API padrão).
- **`relacao: "1-para-n"`.** Misturava a quantidade de representações com a cardinalidade de registros.
  - Na base, `cardinalidade_registros` fica no relacionamento, com estado e evidência.
  - A quantidade de representações é implícita nas listas da funcionalidade.
- **`CustomObject.fullName` ↔ `EntityDefinition.QualifiedApiName` como "direta".** Não há evidência; `QualifiedApiName` nem foi lido nesta sessão (a extração parou antes).
  - A correspondência comprovada é `EntityDefinition.Metadata`, tipado como `CustomObject`, de natureza **transformada**.
  - Também foi registrada a representação no objeto Tooling `CustomObject`, com natureza desconhecida.
- **EntityDefinition e FieldDefinition como mapeamentos exclusivos.** Na base, os objetos Tooling `CustomObject` e `CustomField` também foram catalogados, cada um com seu papel.
- **`deploymentStatus` com default `InDevelopment`.** A página de CustomObject 68.0 não declara default nem lista os valores.
  - Na base o default é "não declarado na fonte" e o domínio está como desconhecido.
  - A Tooling (`EntityDefinition.DeploymentStatus`) lista `InDevelopment` e `Deployed`, mas a equivalência com o XML não foi comprovada.
- **`nameField` com `obrigatoria: true`.** A fonte diz que é obrigatório **para objetos customizados**. Na base: condicional, com a condição registrada.
- **Campos de tabela com `default: ""`.** Confundia valor desconhecido com string vazia. Na base, o default tem forma explícita (valor, ausente, null, false, string vazia, não declarado, desconhecido, não aplicável).

### 3. Organization, CurrencyType, DatedConversionRate e Settings

Documento: `perplexity/sf-metadataTypes-properties-xml-nivel-base.md`.

- **Organization.**
  - O rascunho o apresentava como metadata type: pasta `organizations/`, XML com `fullName` 00D… e ~20 propriedades.
  - `Organization` não está na lista de metadata types v68. Isso basta para não cadastrá-lo como XML implantável.
  - A natureza de objeto de dados é provável, mas não foi verificada nesta sessão (pendente na Object Reference).
  - As propriedades e o caminho do rascunho não têm fonte e foram descartados.
- **CurrencyType e DatedConversionRate.**
  - Também apareciam como metadata types, com elemento raiz XML.
  - Nenhum dos dois está na lista v68 e o rascunho não traz fonte. Não foram cadastrados como XML.
  - A configuração de moedas tem um metadata type próprio, `CurrencySettings`, que consta da lista v68 e está pendente de detalhamento.
- **Settings.**
  - O rascunho acerta ao dizer que `Settings` é o agrupador do `package.xml` e que cada configuração tem seu tipo: a lista v68 traz tipos individuais (`CompanySettings`, `MyDomainSettings` etc.) e não traz `Settings`.
  - Correções:
    - Os nomes `Flow.settings`, `Company.settings` correspondem ao formato Metadata API.
    - O Salesforce CLI resolve esses tipos pelo tipo genérico `Settings` (pasta `settings`, sufixo `settings`). O nome físico por tipo está marcado como pendente no inventário.
  - Propriedades e valores citados (ex.: `myDomainSuffix`) não foram verificados e não entraram na base.

### 4. Usuário, perfil e atribuições

Documento: `internal-obj/relationship-profile-user.md`. A maior parte é consistente com o que foi verificado:

- `User.ProfileId` → `Profile` (relacionamento `rel:user-profile`).
- `PermissionSetAssignment` como objeto de junção entre usuário e permission set.

Correções:

- **Usuário → grupo de permission sets.** O rascunho diz que a ligação passa "por meio dos permission sets do grupo". A Object Reference documenta `PermissionSetAssignment.PermissionSetGroupId`: o grupo é atribuído diretamente. Registrado em `rel:psa-permissionsetgroup`.
- **Fontes não oficiais.** As citações de salesforcefaqs.com não entram no registro de fontes.
- **Partes não verificadas.** A cardinalidade "0 ou 1 role" e o trecho de Apex (`UserInfo.getProfileId()`) ficam fora da base. Exemplos Apex não fazem parte desta fase.

### 5. Fontes e versão

Documento: `ai-help/fontes.md`.

- **Links não verificados.** O próprio arquivo declara que os links foram reconstruídos. Os usados nesta sessão foram relidos com o endpoint versionado 264.0 (API 68.0) e registrados com pertinência; os demais continuam não verificados.
- **Versão.** O exemplo de API 64.0 foi substituído pela 68.0, justificada em `config/versoes.json`.
- **Nomes de página.** Algumas páginas do rascunho têm nomes que não correspondem aos da documentação: CustomTab está em `meta_tab.htm` e ValidationRule em `meta_validationformulas.htm`.

### 6. Planos e materiais de CTA

Documentos: `perplexity/plano-levantamento-...md` e `sf-features-*`.

- **Estimativas de escala** ("centenas" de tipos, "milhares a dezenas de milhares" de fields): sem denominador. A base usa o denominador formal de 993 tipos na v68.
- **apis.io** é citado como fonte do WSDL. Não é fonte oficial e não foi usado.
- **Enquadramento de certificação CTA:** fora do escopo. As listas de funcionalidades por área serviram só como insumo comparativo para a taxonomia, que segue a especificação.
- **Recomendação de fixar versão, usar o WSDL e cruzar com o Coverage Report:** mantida e implementada.
  - Versão fixada em 68.0.
  - Importador de WSDL pronto, aguardando o arquivo.
  - Cobertura do CLI importada de `METADATA_SUPPORT.md`.

### 7. Nomes que exigem atenção (amostra da conferência automática)

- **Singular × plural.** `AssignmentRule` e `AutoResponseRule` aparecem nos rascunhos, mas os tipos v68 são `AssignmentRules` e `AutoResponseRules`.
- **Tipo inexistente.** `AccountSharingRules` aparece nos rascunhos; a lista v68 traz `SharingRules`.
- **587 nomes não confirmados.** Ficam como fila de investigação; não podem ser incorporados sem fonte.

## O que foi reaproveitado

- **Princípios:** não inventar; diferenciar propriedade XML, campo API e API de acesso; JSON como fonte e saídas derivadas.
- **Ideias de modelagem:** o vínculo User.ProfileId e o papel de PermissionSetAssignment, confirmados nas fontes.
- **Dicas de fontes:** sugestões de páginas oficiais, como pontos de partida, revalidadas antes do uso.
