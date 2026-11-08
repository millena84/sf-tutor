# Ponto de retomada

Situação em 2026-11-08, após o lote 3d (pendências de Agentforce Sales e Service fechadas) e a projeção do site (`gerado/site/`, contrato 1.0.0). Os números vivos estão em `relatorios/cobertura.md`; o detalhe do que foi resolvido está em `relatorios/resolucao-bloqueios.md`.

## O que está pronto

- **Pipeline executável e validado:** 0 erros e 24 testes passando. O validador também exige que todo nome de propriedade ou campo apareça na nota de extração da fonte citada.
- **Escopo e versão:** fixados em `config/` (API 68.0, Winter '27).
- **Universo de metadata types:** 993 tipos da v68, a partir de snapshots oficiais com hash.
- **Taxonomia proposta:** 14 classificações e 92 subclassificações, ainda sem cruzamento com a documentação oficial.
- **Catálogo do piloto:**
  - 31 funcionalidades (as sem objeto ou metadata type lido declaram a ausência como `desconhecido`);
  - 36 metadata types e 64 estruturas;
  - 60 objetos API;
  - 90 relacionamentos.
- **Caminhos de Setup:** verificados em 20 das 31 funcionalidades (lista das 11 restantes na tabela de lacunas).
- **Data 360:** contexto técnico verificado.
- **Agentforce Sales e Agentforce Service** (antes Sales Cloud e Service Cloud): nome, contexto técnico e licenças verificados. Vendas tem 10 funcionalidades próprias e atendimento, 3; Knowledge, regras de atribuição, horário comercial, apps de console e Path entram como capacidades compartilhadas. O relatório de pesquisa usado como mapa está em `fontes/pesquisas/`.

Os JSONs de `catalogo/` são a fonte da verdade. Os lotes 1, 2 e 3a a 3d foram aplicados por scripts de carga mantidos fora do repositório; edições futuras devem ser feitas nos JSONs ou por ferramentas criadas em `ferramentas/`.

## Acompanhamento no GitHub

Os lotes e o site são acompanhados por issues em millena84/sf-tutor (milestones "MVP do site" e "v2"). Este arquivo continua sendo a fonte do detalhe técnico; cada issue aponta para a seção correspondente. O site é publicado em millena84/tutorial-sf-grafo (GitHub Pages), só com autorização.

## Projeção para o site

`gerado/site/` é gerada por `sftutor.py gerar` com contrato versionado (`manifest.json`, schema em `schemas/site-manifest.schema.json`, testes em `testes/test_insumos.py`). O app em `apps/sf-tutor/` copia essa pasta no build; a cópia é gerada, nunca editada.

**Estado do app (2026-11-08):** MVP local pronto para revisão, ainda sem commit e sem publicação.
- Comandos e arquitetura: `apps/sf-tutor/NOTA-ARQUITETURA.md`.
- `npm run verificar` passa: build com validação da base, lint, 28 testes unitários, 25 E2E (desktop e 360px) e performance (dados reais e fixture sintética).
- Pendências visuais: logo oficial (hoje placeholder identificado) e inspeção da referência flavinho.pages.dev (bloqueada para acesso automatizado).

## Lacunas por item

| Item | Situação | Lacuna concreta |
|---|---|---|
| mdt:PermissionSet, PermissionSetGroup, ValidationRule, PathAssistant | estrutural completa | Mapeamento campo a campo XML↔API pendente; grafias a conferir no WSDL |
| mdt:Profile | parcial | 6 subtipos não servidos pela documentação (ProfileUserPermission, ProfileServicePresenceStatusAccess, LoginFlow, ProfileAgentAccess, ProfileActionOverride, ProfileLoginHours) |
| mdt:CustomObject | parcial | Subtipos (ActionOverride, BusinessProcess, ListView, SearchLayouts…), vários deles metadata types próprios |
| mdt:CustomField | parcial | CustomValue (parcial) e ValueSettings |
| mdt:RecordType | parcial | PicklistValue |
| mdt:Flow | parcial | Subtipos Flow*; 37 propriedades sem explicação |
| mdt:FlexiPage, QuickAction, CustomTab | parcial | Subtipos; falta exemplo XML de FlexiPage |
| obj:User | parcial | 25 nomes da Field Reference não capturados; tipos e propriedades de API dos campos vindos só da Field Reference |
| Exposições Tooling de Profile, PermissionSet, PSG, PSA, User, RecordType | exposição verificada | Campos e operações da exposição Tooling |
| obj:UserLogin (Tooling) | indeterminado | Fora do trecho servido do índice |
| obj:EntityDefinition, FieldDefinition | parcial | Recortes de 13 de 64 e de 12 de 56 campos |
| Setup de 11 funcionalidades | desconhecido | Perfis, tipos de registro, contas, contatos, leads, oportunidades, casos, campanhas, produtos e catálogos de preço, previsões colaborativas, equipes de conta e de oportunidade |
| Licenças de Core | desconhecido | Não registradas |
| Licenças de Sales e Service | parcial | Licença de usuário e feature license registradas; matriz completa de edições pendente |
| obj:Lead | parcial | 74 nomes lidos; tipos e propriedades só de 14 campos |
| obj:Opportunity, obj:Case | parcial | Object Reference truncada; propriedades de API faltam para campos vindos só da Field Reference |
| obj:Account, obj:Contact | parcial | Tabela de conta pessoal (Account) e tabela de Contact servidas truncadas |
| Objetos parciais de Sales e Service | parcial | Contact, Campaign, Product2, Quote, AgentWork, KnowledgeArticleVersion (páginas truncadas); QueueRoutingConfig e Entitlement (linha sem nome); Knowledge__kav sem página própria |
| mdt:KnowledgeSettings, ForecastingSettings | parcial | Subtipos lidos (nota de extração), ainda não cadastrados como estruturas |
| mdt:PresenceUserConfig | parcial | Tabela com uma linha vazia |
| mdt:EntitlementProcess | parcial | WorkflowActionReference sem estrutura detalhada |

## Bloqueios reais

1. **Teste em org.** Não há org disponível; nenhuma execução foi simulada.
2. **Limite de tamanho do endpoint de documentação** (cerca de 54 a 112 mil caracteres por página). Contornável por:
   - liberação de rede para baixar o HTML completo;
   - os PDFs versionados;
   - o `metadata.wsdl`, para as propriedades.

O WSDL **não** é bloqueio: a documentação de cada tipo é a fonte alternativa prevista no prompt.

## Próximos lotes

1. **Lote 3 — fechar as lacunas da tabela acima** que dependem só de documentação:
   - páginas próprias de ActionOverride, BusinessProcess, ListView etc.;
   - campos Tooling das exposições já confirmadas;
   - Setup de Perfis e de Tipos de registro na Ajuda.
2. **Lote 4 — classificação Core** dos 981 tipos pendentes, em famílias, sempre com a página do tipo como evidência.
3. **Lotes 5+ — uma classificação por vez.** Ordem: Acesso, Dados, Automação, Interface, Desenvolvimento, Organização (família Settings).
4. **Revisões transversais:**
   - cruzar a taxonomia com a documentação oficial;
   - cadastrar as estruturas de KnowledgeSettings e ForecastingSettings (as linhas já estão em `fontes/extracoes/mdapi-lote3d.txt`);
   - matriz de licenças e edições.

## Prompt de retomada

```text
Você está no repositório sf-tutor, pasta ai-help/claude/insumos-grafo/.
Leia CLAUDE.md, README.md, relatorios/retomada.md, relatorios/resolucao-bloqueios.md e
relatorios/cobertura.md desta pasta, e ../tarefas/00-especificacao-grafo.md e
../tarefas/01-prompt-criar-insumos.md.
Rode `python3 ferramentas/sftutor.py tudo` e `python3 -m unittest discover -s testes`
e confirme 0 erros antes de mudar algo.
Execute o próximo lote pendente de relatorios/retomada.md (comece pelo Lote 3):
- leia as páginas oficiais pelo endpoint versionado
  https://developer.salesforce.com/docs/get_document_content/<livro>/<pagina>.htm/en-us/264.0
  (atenção ao corte de ~54 a 112 mil caracteres; use offset e registre o que não foi servido)
  e a Ajuda (help.salesforce.com) por busca restrita ao domínio;
- registre cada fonte em fontes/registro.json e a nota em fontes/extracoes/
  (o validador exige que os nomes apareçam na nota);
- edite os JSONs de catalogo/ (fonte da verdade); nunca marque completo sem
  esperado == presente e estruturas detalhadas;
- ao terminar, rode `tudo` e os testes, atualize esta retomada e informe o que foi
  feito, validado, pendente e o próximo passo.
Se o usuário fornecer metadata.wsdl ou PDFs versionados, use-os antes para fechar as
lacunas de páginas truncadas.
Publicação: só com autorização. Fluxo autorizado: branch nova a partir da main
atualizada (confira antes se o PR anterior já foi mergeado), PR com "Closes #n" da
issue correspondente. Nunca push direto na main.
```
