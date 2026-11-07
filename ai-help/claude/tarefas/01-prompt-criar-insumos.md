# Tarefa 1: prompt para criar os insumos do sf-tutor

Copie o bloco abaixo para uma sessão do Claude Code aberta no repositório `sf-tutor`. O arquivo `00-especificacao-grafo.md` deve estar em `ai-help/claude/insumos-grafo/`; ele contém os requisitos detalhados e prevalece sobre rascunhos anteriores.

O prompt pede implementação da base e dos validadores, não a criação do site. Uma sessão pode trabalhar em lotes; ela não deve confundir “lote concluído” com “catálogo inteiro completo”.

```text
Você está no repositório sf-tutor. Sua tarefa é implementar e preencher a
base de conhecimento que alimentará um tutorial visual e didático em grafo
sobre Salesforce.

LEITURA OBRIGATÓRIA

1. Leia ai-help/claude/insumos-grafo/00-especificacao-grafo.md integralmente.
2. Examine as instruções já existentes do repositório e o git status.
3. Leia README.md e os documentos de:
   - ai-help/ideia-sf-grafo/
   - ai-help/perplexity/
   - ai-help/internal-obj/
   - ai-help/claude/insumos-grafo/
4. Trate esses documentos anteriores como requisitos, exemplos e hipóteses,
   NÃO como referências técnicas já validadas.
5. Registre conflitos e correções, sem sobrescrever o histórico original.

ESCOPO E DIRETÓRIO

Todos os insumos, scripts, esquemas, testes, snapshots permitidos, relatórios,
instruções locais e dados gerados desta tarefa devem ficar exclusivamente em:

ai-help/claude/insumos-grafo/

Não criar agora o tutorial, um frontend, um grafo demonstrativo ou um app.
Não criar quizzes, flashcards, trilhas de certificação ou itens não pedidos.
Não alterar arquivos fora da pasta autorizada nem sobrescrever os três
documentos de especificação/prompt sem autorização.
Não fazer commit, push, deploy ou publicar conteúdo sem solicitação.
Não descartar alterações locais de outras pessoas.

OBJETIVO FUNCIONAL

Produzir todos os insumos necessários ao tutorial, com:
- Salesforce como nó central.
- Visões por classificação funcional e por nuvem/produto.
- Sub-classificações desenvolvidas até o nível de funcionalidade.
- Funcionalidades que tenham XML, objeto API, ambos ou nenhum deles.
- Todos os metadata types do recorte Salesforce Platform/Core definido.
- Todas as propriedades desses tipos, incluindo herdadas e estruturas
  compostas documentadas, sem fabricar tags XML.
- Objetos API relacionados, APIs de acesso e todos os seus campos no
  universo documental definido.
- Objetos de junção e relações por seus campos reais.
- Explicações e detalhes por nível exigidos na especificação.

Não limitar o trabalho a um template ou a cinco exemplos. Os exemplos
iniciais são testes do modelo; o objetivo continua sendo o inventário
integral do recorte, com pendências quantificadas se houver bloqueios.

DECISÕES DE MODELO

Use a organização descrita na especificação. A unidade didática é a
funcionalidade, não apenas o metadata type.

1. Um cadastro JSON por nuvem/produto: informações técnicas, licenças,
   descrições e referências para funcionalidades compartilhadas.
2. Um JSON por classificação e por sub-classificação, com explicações.
3. Um JSON por funcionalidade, com explicação e suas representações.
4. Um JSON por metadata type, com todas as propriedades XML.
5. Um cadastro canônico por objeto API, com todas as exposições por API
   verificadas e campos correspondentes.
6. Relacionamentos técnicos comprovados, inclusive junções.
7. Fichas completas geradas por metadata type, reunindo no MESMO JSON a
   ficha XML e todo o conteúdo dos objetos API relacionados e seus campos.
8. Projeções de grafo e índices gerados a partir desses cadastros.

Evite duplicação manual de conteúdo compartilhado. Referências nos cadastros
podem ser expandidas deterministicamente nas fichas completas para consumo
por agentes. Nenhum conteúdo deve existir só na projeção visual.

Use IDs canônicos estáveis, nomes técnicos originais e texto didático pt-BR.
Considere contexto de produto, família de API e versão para evitar colisões.
Não duplicar cadastros por nuvem só porque um recurso é compartilhado.

CONFIABILIDADE E CORREÇÕES

- Não invente metadata types para funcionalidades que só têm objetos API.
- Não gere User.json dentro de metadata-types como se User fosse um XML
  implantável. Represente a funcionalidade e o objeto User corretamente.
- Audite também Organization, CurrencyType, DatedConversionRate, Settings,
  nomes de Settings, nomes de propriedades e caminhos presentes nos
  rascunhos. Semelhança de nome não comprova categoria nem serialização.
- Não trate cada complexType do WSDL como metadata type independente;
  resolva herança e identifique estruturas auxiliares.
- Não transforme o tipo CustomField em uma tag filha artificial de fields.
- “Tabela interna” significa objeto publicamente exposto por API, não
  uma tabela física privada do banco.
- Não assuma que EntityDefinition ou FieldDefinition sejam o único
  mapeamento possível de CustomObject/CustomField; investigue as
  representações documentadas e explique o papel de cada uma.
- APIs de acesso devem ser uma lista; podem existir exposições padrão e
  Tooling diferentes. Não mesclar campos/operabilidade sem evidência.
- Não classifique Bulk/Streaming como simples alternativas de tabela SOQL.
- Não ofereça consulta Apex direta a objeto Tooling-only.
- Não infira que valores similares em XML e objetos API são equivalentes.
- Registre cardinalidade de registros separada da quantidade de
  representações relacionadas a um metadata type.
- Valor desconhecido não é false, vazio, zero ou inexistente.
- Separe origem standard/custom de valor default e de obrigatoriedade.
- Não use não-nillable como prova isolada de obrigatoriedade de escrita.
- Descreva campos somente leitura pelo que informam, não pelo que configuram.
- Labels didáticos/traduções não devem ser vendidos como labels oficiais.
- Não declarar completa uma lista derivada apenas de uma org.

FONTES E VERSIONAMENTO

Descubra e fixe uma API version/release comprovadamente disponível e registre
a justificativa em config/versoes.json. Não escolher uma versão numérica
antiga dos exemplos por conveniência. Quando um produto tiver ciclo ou API
próprios, registre sua versão separadamente.

Defina em config/escopo.json o que significa Core neste projeto:
plataforma compartilhada, tipos específicos de produtos no mesmo contexto,
produtos fora do recorte, critérios de inclusão e exclusões justificadas.
Não rotular tudo que aparece no Metadata Coverage como “Core universal”.
Itens ainda não classificáveis devem permanecer no inventário como pendentes.

Use e valide:
- Referências oficiais de Metadata API e de cada tipo.
- WSDL/XSD oficial compatível com a versão, quando disponível.
- Metadata Coverage Report para cobertura por canal.
- Referências de objetos da API padrão e da Tooling API.
- Referência oficial de campos e resultados de describe autorizados.
- Referência oficial de source format/CLI para pastas e nomes físicos.
- Documentação de produto/Setup/licenças e release notes quando pertinente.

Use a URL e seção reais de cada fonte. HTTP 200 ou redirecionamento para uma
página genérica não comprovam que o campo ou tipo foi documentado.
Capture a data de verificação e a versão; se não houver versão explícita,
registre esse limite.

Não dependa de uma lista produzida pelo LLM como universo esperado.
Enumere fontes formais/documentais e reconcilie seus inventários.
Se o WSDL não estiver disponível, use fontes oficiais alternativas, registre
a diferença de cobertura e prepare importação para quando ele for fornecido.

Não peça acesso à org antes de investigar fontes públicas suficientes.
Se houver acesso Salesforce já autorizado, usar somente leitura e registrar
o contexto da observação sem expor identidade, IDs reais ou dados de negócio.
Se não houver, o trabalho documental deve continuar. Os testes em org ficam
explicitamente pendentes; não simulá-los como executados.

Não salvar tokens, credenciais, registros reais, PII, auth files ou dumps
sensíveis. Snapshots devem conter apenas schemas/documentação permitidos.
Requisições não devem violar controles de acesso nem termos da fonte.

DETALHE DOS DADOS

Implemente os campos obrigatórios da especificação para:
- Salesforce.
- Nuvem/produto.
- Classificação e sub-classificação.
- Funcionalidade.
- Metadata type/XML.
- Objeto API e objeto de junção.
- Propriedade XML e campo API.
- Relacionamento e correspondência XML/API.

Todo campo/propriedade deve ter nome, label, tipos técnico/didático,
explicação, finalidade, origem padrão/custom, obrigatoriedade e condições,
default com estado explícito, valores possíveis com significados, restrições,
exemplo, versão/contexto e evidências.

Campos API também têm nulabilidade, operação de leitura/escrita,
create/update, cálculo, defaulted-on-create, filtro/ordem/grupo e referências,
quando aplicável e documentado.

Para o objeto API, registrar endpoints/contexto, SOQL e/ou acesso Apex
aplicável, operações, permissões, restrições, Setup se aplicável e alertas.
Para XML, registrar source format e Metadata API format separadamente,
pasta, nome físico, arquivos associados, exemplo e cobertura verificada.

Aceite obrigatoriedade sim/não/condicional/desconhecida/não-aplicável.
Não substitua todos esses estados por um booleano.
Use estados separados para desconhecido, não aplicável, não exposto,
bloqueado e verificado.

Enum fechado, lista dinâmica e texto livre são casos diferentes.
Documente todos os valores conhecidos da versão e todos os seus significados.
Quando o domínio depender de org, idioma, recurso ou record type, declare
o contexto; não prometa uma lista universal inexistente.

ASSOCIAÇÕES OBRIGATÓRIAS NO PILOTO

Crie um recorte verificável para provar:
- Usuários/User sem XML de Metadata API inventado.
- Profile e PermissionSet em suas representações comprovadas.
- PermissionSetGroup.
- PermissionSetAssignment conectando AssigneeId, PermissionSetId e
  PermissionSetGroupId aos destinos documentados.
- User.ProfileId separado de PermissionSetAssignment.
- CustomObject e CustomField com propriedades reais e mapeamentos API.
- RecordType, ValidationRule, Flow, PathAssistant, FlexiPage, QuickAction
  e CustomTab, com classificação principal e relações secundárias.

Esses itens são pilotos e âncoras de qualidade, não substituem o catálogo.

EXECUÇÃO

Etapa inicial:
1. Audite os rascunhos e gere relatorios/auditoria-insumos-anteriores.md.
2. Defina escopo, versões, fontes e taxonomia/subtaxonomia completa proposta.
3. Gere inventarios com origem e destino de cada item e denominadores
   verificáveis. Distinguir metadata type, estrutura auxiliar e objeto API.
4. Informe brevemente as decisões e inicie a implementação. Não interrompa
   só para apresentar um plano, salvo bloqueio ou decisão material.

Implementação:
5. Crie JSON Schemas, registros de fontes, cadastros, exemplos e validadores.
6. Valide o piloto acima e ajuste o contrato antes de escalar.
7. Preencha o restante por lotes reproduzíveis a partir do inventário,
   sem reduzir o escopo silenciosamente a “propriedades principais”.
8. Extraia todos os campos, heranças e tipos compostos, tratando ciclos por
   referência sem recursão infinita.
9. Enriqueça as descrições e os significados com fontes verificadas.
10. Gere fichas completas e projeções de grafo sem inventar relações.
11. Execute todos os validadores e gere os relatórios de cobertura.

Se a sessão não puder terminar o catálogo inteiro:
- Deixe o pipeline executável e o lote atual validado.
- Registre progresso por ID, lacunas, motivos, fontes faltantes e próximo lote.
- Gere um comando/prompt de retomada específico em relatorios/retomada.md.
- Não finalize com “todos completos” e não apague pendências.
- Não pare em um mero esqueleto se for viável continuar os lotes.

TESTES E CRITÉRIOS DE ACEITE

Crie comandos documentados e efetivamente executáveis para validar,
reconstruir e auditar a base. Escolha a implementação mais simples compatível
com o repositório; fixe dependências e não introduza stack desnecessária.

Teste pelo menos:
- Todos os JSONs contra schemas.
- IDs únicos, referências válidas, inexistência de órfãos acidentais.
- Uma funcionalidade compartilhada sem duplicação manual.
- Ausência de User como metadata XML fictício.
- Papéis/campos de PermissionSetAssignment e User.ProfileId.
- Herança e estruturas compostas, inclusive prevenção de ciclos.
- Nenhuma correspondência direta XML/API sem evidência.
- APIs de acesso e diferenças de exposição sem contradição.
- XMLs bem formados e exemplos conforme suas fontes.
- Consultas com campos válidos na API declarada, distinguindo revisão
  documental, validação de schema e execução real em org.
- Domínios dinâmicos não tratados como enums fechados.
- Nenhuma inferência indevida de default ou obrigatoriedade.
- Links resolvidos com checagem de pertinência do conteúdo.
- Geração determinística das fichas e do grafo, sem timestamps variáveis
  desnecessários nos outputs e sem diferenças em rebuild idêntico.
- Relatório que reconcilia inventário esperado com o produzido.

Um tipo só pode ser marcado completo se as propriedades esperadas da
fonte declarada estiverem presentes e explicadas, os objetos/campos relacionados
do mapeamento verificado estiverem documentados e as lacunas estiverem
fechadas ou claramente registradas como limitação de escopo.
Completude estrutural, didática e de mapeamento devem ser avaliadas separadas.

ENTREGA

Ao concluir:
1. Resuma o que foi criado e os comandos de uso.
2. Mostre escopo, versões e fontes efetivamente utilizadas.
3. Mostre cobertura alcançada e denominadores.
4. Liste pendências e bloqueios reais, sem os esconder.
5. Mostre um exemplo de ficha completa por metadata type e um exemplo de
   funcionalidade sem XML.
6. Informe se a base está pronta para a tarefa 2 e quais limitações o site
   deverá exibir.
7. Não publique nem faça push. Deixe os arquivos locais prontos para revisão.
```
