# Fechamento do MVP (rodada D1)

Data: 2026-11-17. Base: API 68.0 (Winter '27). Site publicado em millena84/tutorial-sf-grafo.

Critério combinado com a autora: **nós com informação correta e sem dado genérico.** Este relatório mostra o que o MVP entrega, como foi verificado e o que fica para a v2. Os números saem do catálogo; a fonte de cada um está indicada.

## Resumo

- O mapa tem 14 classificações, 92 subclassificações e 137 funcionalidades, com 161 metadata types, 470 estruturas e 84 objetos API.
- Cobertura **estrutural** completa nos três tipos de nó técnico: todas as propriedades e campos da página oficial estão no catálogo.
- Cobertura **explicativa** completa em 154 de 161 metadata types, 469 de 470 estruturas e 63 de 84 objetos API. Onde falta explicação, o site mostra que ela está pendente; não aparece texto inventado.
- Cobertura **de relacionamentos**: 152 relacionamentos, 149 verificados. O mapeamento entre propriedade XML e campo de API está parcial em todos os tipos; ele não foi objetivo do MVP.
- Fica fora: as demais nuvens Salesforce (rodada D3 ou rodada própria) e a classificação Core dos 981 metadata types não cadastrados (#10).

## Cobertura por dimensão

Fonte: `relatorios/cobertura.md` (gerado) e os campos `cobertura` do catálogo.

| Nó | Estrutural | Explicativa | Mapeamento / relacionamentos |
|---|---|---|---|
| Metadata types (161) | completa em 161 | completa em 154; parcial em 7 | mapeamento parcial em 161 |
| Estruturas (470) | completa em 470 | completa em 469; parcial em 1 | mapeamento não iniciado |
| Objetos API (84) | completa em 84 | completa em 63; parcial em 21 | mapeamento parcial em 84 |
| Relacionamentos | — | — | 152, dos quais 149 verificados |

"Completa" na estrutural quer dizer que o número esperado de itens é igual ao presente, contando a página oficial do tipo ou do objeto. O validador recusa marcar completa sem essa igualdade. Isso não quer dizer que o recorte Core inteiro esteja catalogado: o universo da v68 tem 993 metadata types, e 981 ainda não foram classificados (#10).

## Funcionalidades

- 137 funcionalidades, todas com estado `verificado`.
- Caminho de Setup: 119 verificados, 17 marcados como "não aplicável" (APIs e recursos de código) e 1 desconhecido (configuracoes-de-nuvens-de-setor; nenhuma fonte lida indica um caminho único).

## Auditoria de conteúdo

Ferramenta: `ferramentas/auditoria_conteudo.py`. Relatório: `relatorios/auditoria-conteudo.md` (gerado).

Corrigido na D1:
- 32 estruturas de Profile e PermissionSet tinham o mesmo texto genérico e passaram a ter descrição específica (lote 7t).
- O `o_que_e` do Data 360 estava vazio e foi preenchido (lote 7u).
- O Platform/Core tinha licenças sem fonte e estado `desconhecido`. As licenças agora têm fonte e o nó passou a `verificado` (lote 7u).
- 378 campos de User, Account, Contact, Lead, Opportunity e Case ganharam explicação lida na Object Reference 264.0 (lote 7v).

Sem ocorrências: campos vazios, textos que só repetem o nome, frases-modelo e textos idênticos em nós diferentes.

Fica registrado:
- **509 propriedades e campos com explicação pendente, em 26 nós.** Por decisão da autora, vão para a v2. Os maiores são QuoteLineItem, Campaign, Quote, AgentWork, ServiceContract e Flow. O site mostra que estão pendentes.
- 79 campos explicativos com menos de 40 caracteres. São curtos, mas específicos; entram na revisão didática.

## Revisão do site

- Build local revisado em desktop (1366×900) e mobile (360×740): início, funcionalidade, metadata type, objeto, nós de nuvem e janela de campos. Nenhum erro de JavaScript. As imagens externas (logos referenciados por URL) não carregam no ambiente de teste; no site publicado, dependem do endereço oficial.
- Testes automáticos em cada rodada: Vitest 53; Playwright 41 (6 ignorados) em desktop e mobile; teste de performance com uma fixture sintética de cerca de 78 mil nós.
- O site publicado foi conferido pelo `data/build-info.json`.

## O que o MVP não verifica

- **Teste em org real:** não há org disponível, então toda a validação é documental (#12).
- **Páginas sem conteúdo legível:** ExtlClntAppAttestSettings, ExtlClntAppAttestConfigurablePolicies, ExtlClntAppOauthSecuritySettings, McpServerDefinition e ApiNamedQuery (#39).
- **Leitura assistida:** parte das descrições veio de leitura que condensa a página. O texto foi conferido por coerência com nome e tipo, não linha a linha; as notas de extração registram isso.

## Fica para depois

- **v2:**
  - os 509 itens com explicação pendente;
  - a ligação estrutural entre funcionalidade e propriedade (decisão na #39);
  - a revisão didática dos textos curtos.
- **Rodadas seguintes, já combinadas:**
  - C2 (paleta e rótulos; #23, #17);
  - C3 (acessibilidade; #19);
  - D2 (certificações);
  - D3 (nuvens × funcionalidades). As demais nuvens entram na D3 ou numa rodada própria, a decidir com a autora.
- **Data 360:** conectores de dados (decisão na #39).
- **#15:** a publicação automática está pronta, mas falta configurar o secret `TUTORIAL_SF_GRAFO_TOKEN` no sf-tutor. Enquanto isso, a publicação é feita por PR manual.
