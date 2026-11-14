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
- **Arraste de nós:** a posição arrastada não é preservada quando a cena é reconstruída.
- **Rótulos no mapa:** em ramos muito densos podem se sobrepor quando o zoom está afastado. O painel e o modo lista mostram o texto completo.
- **Ganchos de teste:** `window.__sfTutor` expõe apenas leitura (contagens, seleção, coordenada de um nó/aresta para o clique dos testes) e não altera o estado.
- **Fixture sintética:** existe só para medir volume. É rotulada "SINT…", e a interface mostra a faixa "DADOS SINTÉTICOS DE TESTE". Ela vai para `dist/__teste-sintetico` apenas durante `npm run perf`, e o próximo build a remove.
