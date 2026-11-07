# Insumos do sf-tutor

Base de conhecimento estruturada que alimenta o tutorial visual em grafo sobre Salesforce. Requisitos em `../tarefas/00-especificacao-grafo.md`. Resolução dos bloqueios do primeiro lote: `relatorios/resolucao-bloqueios.md`; prompt desta etapa em `../tarefas/01-prompt-criar-insumos.md`.

**Estado atual:** pipeline completo e piloto validado. O catálogo inteiro **não** está completo. Os números atualizados estão em `relatorios/cobertura.md` e o ponto de retomada em `relatorios/retomada.md`.

## Comandos

Requisitos: Python 3.10+ e `pip install -r requirements.txt` (somente `jsonschema`, versão fixada). Execute a partir desta pasta.

| Comando | O que faz |
|---|---|
| `python3 ferramentas/sftutor.py tudo` | inventário, auditoria de rascunhos, geração, cobertura e validação |
| `python3 ferramentas/sftutor.py validar` | schemas, referências, regras de confiabilidade, fontes e determinismo de `gerado/` |
| `python3 ferramentas/sftutor.py gerar` | reconstrói `gerado/` a partir de `catalogo/` |
| `python3 ferramentas/sftutor.py inventario` | reconstrói `inventarios/` a partir dos snapshots e do catálogo |
| `python3 ferramentas/sftutor.py cobertura` | reescreve `relatorios/cobertura.md` |
| `python3 ferramentas/sftutor.py importar-wsdl <metadata.wsdl>` | importa o WSDL da Metadata API para `inventarios/wsdl-schema.json`, resolvendo herança e ciclos |
| `python3 -m unittest discover -s testes -v` | testes positivos e negativos (defeitos injetados em cópia temporária) |

## Organização

```text
config/           escopo.json (recorte Core e critérios) · versoes.json (API 68.0 e justificativa)
schemas/          JSON Schema 2020-12 de cada tipo de cadastro + comum.schema.json
catalogo/         FONTE DA VERDADE (edição manual)
  salesforce.json        nó central
  nuvens/                um cadastro por nuvem/produto
  classificacoes/        14 classificações didáticas
  subclassificacoes/     92 subclassificações
  funcionalidades/       unidade didática; aponta para metadata types e objetos API
  metadata-types/        um cadastro por tipo, com todas as propriedades XML levantadas
  estruturas/            estruturas auxiliares (subtipos compostos), um cadastro cada
  objetos-api/           um cadastro por objeto, com exposições por API e campos
  relacionamentos/       referências por campo, correspondências XML↔API, representações comuns
fontes/           registro.json · snapshots/ (dados oficiais com sha256) · extracoes/ (notas por página lida)
inventarios/      gerados: metadata-types-v68.json (denominador), objetos-api.json, rascunhos-nomes.json
ferramentas/      sftutor.py
testes/           test_insumos.py + fixtures sintéticas
relatorios/       auditoria, cobertura (gerada), retomada
gerado/           NUNCA editar: fichas-completas/, fichas-funcionalidade/, grafo/, cobertura.json
```

## Decisões de modelo

- **Unidade didática.** É a funcionalidade, que pode ter zero, um ou vários metadata types e objetos API. Toda ausência é declarada com estado e motivo; uma lista vazia sozinha não diz nada.
- **Cadastro único.** Itens compartilhados existem uma só vez. Exemplos:
  - `obj:PermissionSetAssignment` serve a duas funcionalidades.
  - `func:regras-de-validacao` aparece em três subclassificações (uma principal e duas secundárias).
- **IDs estáveis com prefixo:**
  - `func:`, `cls:`, `sub:`, `nuv:`, `mdt:`, `mdx:`, `obj:`, `rel:`;
  - propriedades e campos: `mdt:PermissionSet.label`, `obj:User.ProfileId`.
- **Objetos com o mesmo nome.** Um objeto API com o mesmo nome de um metadata type usa outro prefixo: `obj:ValidationRule` (Tooling) e `mdt:ValidationRule`.
- **Estados de verificação.** Cinco estados distintos: `verificado`, `desconhecido`, `nao_aplicavel`, `nao_exposto`, `bloqueado`.
- **Obrigatoriedade.** Pode ser sim, não, condicional (com a condição), desconhecida ou não aplicável.
  - "Não marcado como obrigatório" fica como `nao` com estado `desconhecido`: a ausência de marcação não prova opcionalidade.
- **Default.** Tem forma explícita: valor, ausente no XML, null, false, string vazia, não declarado na fonte, desconhecido ou não aplicável.
- **Domínio de valores.** Distingue enum fechado, lista dinâmica e texto livre, e indica se a lista está completa.
- **Campos `Permissions*`.** De Profile e PermissionSet, são registrados como domínio dinâmico, não enumerados.
- **APIs de acesso.** São uma lista de exposições, com estado por API.
  - Para objeto exposto só na Tooling, a consulta SOQL direta em Apex fica marcada como `nao_exposto`.
- **Correspondência XML↔API.** Tem natureza (direta, parcial, transformada, nenhuma, desconhecida).
  - Qualquer natureza diferente de "desconhecida" exige verificação e evidência.
  - Semelhança de nome não basta: veja `rel:cor-permissionset-label`.
- **Textos de curadoria.** Classificações, subclassificações, siglas e rótulos didáticos são curadoria do projeto e estão marcados assim.

## Níveis de validação

| Nível | Situação nesta base |
|---|---|
| Documental | **Feito** para o piloto. Páginas oficiais 68.0 lidas pelo endpoint versionado e páginas da Ajuda; extração assistida por IA registrada em `fontes/extracoes/`. O validador exige que todo nome de propriedade ou campo apareça na nota de extração da fonte citada. |
| Schema (WSDL) | **Não usado.** A documentação oficial de cada tipo é a fonte das propriedades, como o prompt prevê na falta do WSDL. O `metadata.wsdl` (gerado numa org) serviria como conferência extra; o importador está pronto e testado com fixture sintética. |
| Teste real em org | **Não executado.** As consultas SOQL têm `validacao: "documental"`; nenhuma execução em org foi simulada. |

## Fontes

Registro em `fontes/registro.json`. Fontes formais usadas para o universo e para os arquivos:

- `METADATA_SUPPORT.md` (v68, 993 tipos);
- `metadataRegistry.json` (Salesforce CLI 13.12.0).

Ambos estão em `fontes/snapshots/` com sha256. As propriedades e os campos vêm das páginas oficiais 68.0 da Metadata API, da Object Reference e da Tooling API.
