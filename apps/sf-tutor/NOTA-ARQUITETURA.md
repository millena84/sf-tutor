# sf-tutor — nota de arquitetura (MVP)

## Resumo

Site estático: HTML, CSS e TypeScript, sem servidor e sem chamadas à org. Ele lê a projeção `sf-tutor-site` 1.0.0 gerada em `ai-help/claude/insumos-grafo/gerado/site/`. Não existe base técnica no frontend: todo texto técnico vem dos JSON gerados.

## Comandos

| Comando | O que faz |
|---|---|
| `npm install` | instala dependências (uma vez) |
| `npm run dev` | valida a base, copia os dados e abre o servidor de desenvolvimento |
| `npm run build` | valida a base (`python3 ferramentas/sftutor.py tudo`), copia os dados, checa tipos e gera `dist/` |
| `npm run preview` | serve `dist/` em http://localhost:4173 |
| `npm run lint` | TypeScript estrito + ESLint (proíbe `innerHTML`, `eval` e afins) |
| `npm test` | testes unitários (Vitest) sobre os dados reais |
| `npm run test:e2e` | Playwright: 7 jornadas, navegação, celular 360px (precisa de `dist/`) |
| `npm run perf` | performance com dados reais e com a fixture sintética |
| `npm run verificar` | todos os anteriores, em ordem |
| `npm run dados:sem-validar` | copia os dados sem validar a base (só para depurar a interface) |

## CI e publicação

Dois workflows em `.github/workflows/`:

- **`ci.yml`** roda em todo PR. O job de insumos exige `sftutor.py tudo` com 0 erros e 0 avisos, confere que os arquivos gerados estão no commit e roda os testes. O job do site roda `npm run verificar`, na ordem build → lint → Vitest → e2e → perf, com o Chromium do Playwright. Os resultados (e2e, capturas, `perf-*.json`) ficam anexados ao run.
- **`publicar.yml`** roda quando a `main` muda `apps/sf-tutor/` ou `gerado/site/`. Verifica o site, faz o build final e abre ou atualiza **um** PR de publicação em `millena84/metadata-desbugando`, no ramo `publicar/automatico`. Nunca escreve na `main` do repositório público: a publicação continua entrando por PR revisado.

A parte local da publicação fica em `scripts/publicar-docs.sh <clone do repositório público>`: copia `dist/` para `docs/`, remove `docs/__teste-sintetico` e cria `docs/.nojekyll`. O script recusa um build com alterações locais nos insumos ou com a fixture de performance, e avisa quando só o `build-info.json` mudaria. Serve também para publicar à mão.

A prévia do link (Open Graph) usa `public/og/metadata-desbugado.png`, gerada por `node scripts/gerar-imagem-og.mjs` a partir dos desenhos de `public/marca/` e versionada (o build não a regera). As tags em `index.html` usam URLs absolutas do endereço público; `tests/unit/open-graph.test.ts` confere que elas batem com o repositório de `REPORTE.repoIssues` e com o tamanho real da imagem. Se o endereço mudar, atualize as tags junto.

Para a publicação automática funcionar, o repositório precisa do secret `TUTORIAL_SF_GRAFO_TOKEN`: um token fine-grained restrito a `millena84/metadata-desbugando`, com `Contents: Read and write` e `Pull requests: Read and write`. Sem o secret, o workflow verifica o site, avisa e não publica.

O `build-info.json` registra `commit` (HEAD do build) e `commit_insumos` (último commit que mudou `gerado/site`; fica nulo em clone raso).

## Fluxo de dados

```
insumos-grafo/catalogo + fontes   (fonte única, editada à mão)
        │  ferramentas/sftutor.py tudo   (valida + gera)
        ▼
insumos-grafo/gerado/site/*.json   (projeção versionada, contrato no manifest)
        │  scripts/preparar-dados.mjs    (cópia minificada + build-info.json)
        ▼
apps/sf-tutor/public/data/         (CÓPIA GERADA, ignorada no git)
        │  vite build
        ▼
apps/sf-tutor/dist/                (site publicável)
```

- `public/data/` nunca é editado à mão. Se faltar, `npm run dados` recria.
- O app recusa um contrato com versão maior que a suportada (`VERSAO_CONTRATO_SUPORTADA`).
- As fichas (`entidades/…`) são carregadas sob demanda, ao abrir um nó.

## Peças

| Pasta | Papel |
|---|---|
| `src/data/` | tipos do contrato e carregador (valida contrato; `?dados=sintetico` troca a pasta) |
| `src/model/adaptador.ts` | índice e **cena**. A cena é uma função pura do estado de expansão: quais ocorrências estão visíveis, paginação de 24 em 24 e arestas técnicas entre ocorrências visíveis |
| `src/model/busca.ts`, `filtros.ts` | busca em todo o catálogo (inclui campos e propriedades, que não são nós do mapa); filtros que esmaecem e explicam o motivo |
| `src/graph/` | Cytoscape.js: estilo, layout radial incremental (nós existentes não se movem), ícones SVG |
| `src/ui/` | painel por tipo de nó, modo lista (árvore ARIA), Método, legenda, filtros, busca |
| `src/rotas.ts` | estado na URL (`v`, `m`, `n`, `c`, `r`, `t`, `f`, `dados`): deep link e voltar/avançar |

**Último nó do mapa.** O metadata type (XML) e o objeto API são o último nó. Propriedades, campos e estruturas auxiliares não são desenhados (`TIPOS_FORA_DO_MAPA`): abrem numa tabela em janela (`conteudoTabela` em `src/ui/painel.ts`), a partir da ficha do dono, com o detalhe de cada item na linha aberta. No celular cada linha vira um cartão empilhado.
- `Indice.ancoras(id)` devolve o nó do mapa que contém um campo, propriedade ou estrutura. Busca, links e URLs antigas (`?n=obj:User.ProfileId`) selecionam esse nó e abrem a tabela na linha do item (`t` = dono da tabela, `f` = item em foco).
- Uma relação técnica que sai de um campo ou propriedade é desenhada entre os donos (por exemplo, User → Profile por `User.ProfileId`), uma vez por par.

**Ocorrência × id canônico.** Um mesmo item aparece em vários caminhos; por exemplo, uma funcionalidade aparece em Agentforce Sales e em Agentforce Service.
- A chave de ocorrência é o caminho: ids unidos por `>`.
- A ficha é sempre a do id canônico, igual em todos os caminhos.

## Escolhas e por quê

- **Vite + TypeScript, sem framework de UI.** O app é uma tela só, com um canvas e um painel. A ausência de framework reduz dependências; o DOM é montado por `h()`, que nunca interpreta HTML vindo dos dados.
- **Cytoscape.js.** Grafo com milhares de elementos, eventos em nós e arestas, estilos por dado; licença MIT.
- **Expansão progressiva.** Nada é desenhado sem pedido. Listas longas são paginadas. Um item aberto pela busca fora das páginas carregadas é **fixado** sozinho, em vez de carregar todas as páginas até ele.
- **Filtros esmaecem, não removem.** Assim o caminho e as relações continuam corretos, e o painel diz por que o item está esmaecido.

## Limitações conhecidas

- **Logo do site:** marca Desbugando (lâmpada-bug), em `public/marca/`; ícone da aba em `public/favicon.svg`.
- **Logos da Salesforce e das nuvens:**
  - São exibidos **por referência** aos endereços oficiais registrados em `ai-help/claude/insumos-grafo/config/marcas.json`. O arquivo não é copiado para o projeto.
  - O app pré-carrega cada imagem e só troca o ícone do nó quando ela carrega; se falhar, fica o substituto.
  - O canvas erra o tamanho de SVG sem largura/altura declaradas, caso do logo central. Por isso o logo é um `<img>` comum sobre o nó (camada `.camada-logos`), encaixado no círculo e reposicionado a cada quadro do grafo.
  - Os testes simulam os servidores, carregando e falhando, sem depender da rede.
- **Referência visual (flavinho.pages.dev):** não pôde ser inspecionada (bloqueada para acesso automatizado). A paleta e o layout seguem a especificação do prompt e as diretrizes do projeto, não essa referência.
- **Paleta Desbugando (C2, #23, 2026-11-17):** cabeçalho em Noite, rodapé em Faixa roxa, destaques em Violeta escurecido e contorno de foco e seleção em Magenta escurecido. Os temas usam 7 matizes da marca em dois níveis de luminosidade (`src/cores.ts`). O contraste AA é verificado em `tests/unit/contraste.test.ts`; detalhes em `MARCA.md`.
- **Rótulos em ramos densos (C2, #17):** acima de 12 irmãos, o leque passa a usar dois anéis alternados (`src/graph/layout.ts`, teste em `tests/unit/layout.test.ts`). Os nós esmaecidos ficam por baixo e com rótulo mais apagado; o caminho selecionado e os vizinhos ficam por cima.
- **Arraste de nós:** a posição arrastada não é preservada quando a cena é reconstruída.
- **Rótulos no mapa:** em ramos muito densos podem se sobrepor quando o zoom está afastado. O painel e o modo lista mostram o texto completo.
- **Ganchos de teste:** `window.__sfTutor` expõe apenas leitura (contagens, seleção, coordenada de um nó/aresta para o clique dos testes) e não altera o estado.
- **Fixture sintética:** existe só para medir volume. É rotulada "SINT…", e a interface mostra a faixa "DADOS SINTÉTICOS DE TESTE". Ela vai para `dist/__teste-sintetico` apenas durante `npm run perf`, e o próximo build a remove.

## Busca por pasta e tipos sem ficha

- `busca.json` traz, para cada metadata type, a pasta e o sufixo do arquivo (campo `local`, além de entrarem em `textos`). A origem é o registro do Salesforce CLI, via inventário.
- Os tipos do inventário v68 que ainda não têm ficha entram na busca com `tipo: metadata_type_inventario`, id `inv:<Nome>` e `sem_ficha: true`. Eles não viram nó do mapa nem abrem painel: a descrição aparece no próprio resultado.
- Na pontuação, casar pela pasta ou pelo sufixo vale mais do que um nome que só começa com o termo.

## Boas-vindas e tour guiado

`src/ui/tour.ts`: cartão de boas-vindas na primeira visita (não aparece em links diretos com `?n=`) e tour de 6 passos sobre a interface real (visões, seleção no mapa, ficha, tabela de propriedades do PermissionSet, busca, reportar erro). O balão não é modal; Esc sai. "Já vi" fica em `localStorage` (`metadata-desbugado:tour-visto`), sempre com tratamento de erro. Para rever: "Rever o tour" no rodapé ou "Fazer o tour guiado" em Método. Os textos ficam em `PASSOS`; os testes e2e usam `abrir(page, q, { tourVisto: false })` para ver o cartão (por padrão o helper marca o tour como visto).
