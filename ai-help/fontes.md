# sf-tutor — Fontes de referência

> Arquivo de apoio para o projeto `sf-tutor` no Claude Code.
> Reúne as fontes oficiais que sustentam as decisões da conversa de desenho da estrutura (JSON por metadata type, índices, tabelas internas, grafo).
>
> **Aviso de rastreabilidade:** a conversa original citava as fontes por número ([1], [2]...), mas os links não ficaram guardados no histórico. Esta lista foi reconstruída a partir dos temas citados, priorizando documentação oficial. Antes de usar como fonte de verdade, confirme cada link e a API version-alvo.

## Como o agente deve usar este arquivo

- Fonte de verdade para propriedades do XML: **Metadata API Developer Guide** + **metadata.wsdl** da org.
- Fonte de verdade para tabelas internas e campos: **Tooling API Developer Guide** e **Object Reference**.
- Fonte de verdade para cobertura (retrieve, deploy, source tracking, package): **Metadata Coverage Report**.
- Se uma informação não estiver em nenhuma fonte abaixo, marcar como `"a validar"`. Nunca inventar.

---

## 1. Metadata API (propriedades do XML)

| Fonte | Para que serve no projeto | Link |
|---|---|---|
| Metadata API Developer Guide | Visão geral, `deploy()`, `retrieve()`, desenvolvimento file-based | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_intro.htm |
| Metadata Types (lista) | Catálogo de todos os metadata types | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm |
| Understanding Metadata API Types | Metadata type = `complexType` que estende `Metadata`; fields primitivos, enums ou complexTypes | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_understanding_types.htm |
| Metadata Components and Types | Componente é instância de um metadata type | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_objects_intro.htm |
| Working with the Metadata WSDL | Como obter `services/wsdl/metadata` e gerar estrutura | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_quickstart_get_WSDLs.htm |
| retrieve() | Retorna a representação XML dos componentes | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_retrieve.htm |
| describeMetadata() | Lista os tipos disponíveis na org | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_describe.htm |
| describeValueType() | Detalhe granular de um metadata type | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_describeValueType.htm |
| listMetadata() | Propriedades dos componentes existentes | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_listmetadata.htm |

### Páginas de metadata types usados como piloto

| Metadata type | Link |
|---|---|
| CustomObject | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customobject.htm |
| CustomField | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customfield.htm |
| Flow | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_visual_workflow.htm |
| FlowDefinition | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_flowdefinition.htm |
| Profile | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_profile.htm |
| PermissionSet | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_permissionset.htm |
| CustomApplicationComponent | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customapplicationcomponent.htm |

## 2. Metadata Coverage Report (cobertura por canal e versão)

| Fonte | Para que serve | Link |
|---|---|---|
| Metadata Coverage Report | Fonte oficial de suporte por Metadata API, CLI, Change Sets, source tracking e pacotes | https://developer.salesforce.com/docs/metadata-coverage |
| Unsupported Metadata Types | Tipos que não podem ser recuperados/implantados | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_unsupported_types.htm |
| Release Notes | Tipos novos e alterados por release | https://help.salesforce.com/s/articleView?id=release-notes.salesforce_release_notes.htm |

## 3. Tooling API e objetos internos (tabelas e campos)

| Fonte | Para que serve | Link |
|---|---|---|
| Tooling API Developer Guide | Consultas SOQL sobre metadados | https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/intro_api_tooling.htm |
| Tooling API Objects | Lista de objetos da Tooling API | https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/reference_objects_list.htm |
| EntityDefinition | Metadados de objetos padrão e customizados | https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_entitydefinition.htm |
| FieldDefinition | Metadados dos campos de um objeto | https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_fielddefinition.htm |
| Object Reference (API padrão) | Objetos como User, Profile, PermissionSet, SetupEntityAccess | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_list.htm |
| User (objeto) | Campos do objeto User | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_user.htm |
| Profile (objeto) | Campos do objeto Profile | https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_profile.htm |
| Field Types (Primitive Data Types) | Tipos e enums na API | https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/field_types.htm |

## 4. Salesforce CLI (retrieve real da org)

| Fonte | Para que serve | Link |
|---|---|---|
| CLI Command Reference — project | `sf project retrieve start` | https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_project_commands_unified.htm |
| Source Format | Estrutura de arquivos `*-meta.xml` | https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_source_file_format.htm |

## 5. Formatos de dados e grafo

| Fonte | Para que serve | Link |
|---|---|---|
| JSON Schema (draft 2020-12) | Validar os JSONs de metadata type | https://json-schema.org/draft/2020-12 |
| JSON Schema — Getting Started | Tipos, obrigatoriedade, restrições | https://json-schema.org/learn/getting-started-step-by-step |
| RFC 8259 (JSON) | Especificação do formato JSON | https://www.rfc-editor.org/rfc/rfc8259 |
| RFC 4180 (CSV) | Especificação do CSV (exportação derivada) | https://www.rfc-editor.org/rfc/rfc4180 |
| Mermaid — Flowchart | Sintaxe de nós e arestas para os grafos | https://mermaid.js.org/syntax/flowchart.html |

## 6. Claude Code (configuração do projeto)

| Fonte | Para que serve | Link |
|---|---|---|
| Claude Code — Overview | Visão geral | https://docs.anthropic.com/en/docs/claude-code/overview |
| Memory / CLAUDE.md | Regras permanentes do projeto | https://docs.anthropic.com/en/docs/claude-code/memory |
| Subagents | Agentes especializados em `.claude/agents/` | https://docs.anthropic.com/en/docs/claude-code/sub-agents |
| Slash commands | Comandos reutilizáveis em `.claude/commands/` | https://docs.anthropic.com/en/docs/claude-code/slash-commands |
| Best practices | Especificação clara, validação e ciclo de testes | https://www.anthropic.com/engineering/claude-code-best-practices |

## 7. GitHub (repositório)

| Fonte | Para que serve | Link |
|---|---|---|
| About READMEs | Descrição curta vs. README detalhado | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes |
| Classifying your repository with topics | Descrição e topics do repositório | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics |

---

## Checklist antes de usar como fonte de verdade

- [ ] Definir a API version-alvo (ex.: 64.0) e registrar em cada JSON.
- [ ] Abrir cada link e confirmar que a página existe e corresponde ao tema.
- [ ] Baixar o `metadata.wsdl` da sua org (`https://<sua-instancia>.salesforce.com/services/wsdl/metadata`).
- [ ] Cruzar WSDL + Metadata API Guide + Coverage Report + Tooling API.
- [ ] Marcar no JSON a origem de cada informação (`wsdl`, `docs`, `org`, `a validar`).
