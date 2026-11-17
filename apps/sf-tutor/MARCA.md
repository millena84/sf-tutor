# Marca Desbugando (logo oficial do site)

Logo oficial do sf-tutor, por decisão de 2026-11-08: o símbolo **B · lâmpada-bug** da família Desbugando.
- **Fonte de design:** canvas "Desbugando — propostas de logo".
- **Paleta:** Noite `#0B0F2A`, Faixa roxa `#1C1440`, Ciano `#3EE6F2`, Magenta `#FF4FB8`, Violeta `#9B6BFF`, Verde `#2BBE6A`, Claro `#F5F7FF`.

| Arquivo | Uso |
|---|---|
| `public/marca/desbugando-lampada-clara.svg` | fundo claro (cabeçalho do site) |
| `public/marca/desbugando-lampada-escura.svg` | fundo escuro |
| `public/favicon.svg` | ícone da aba (bloco roxo) |

## Como a paleta é usada no site (C2, #23, 2026-11-17)

- **Cabeçalho:** fundo Noite, texto Claro, logo na versão escura (`desbugando-bug-lupa-escura.svg`) e "des" em Magenta.
- **Rodapé:** fundo Faixa roxa, borda em Violeta.
- **Área de leitura:** fundo Claro e superfícies brancas.
- **Destaques:** botões principais, seleção e links em Violeta escurecido (`#704FBF` e `#5A429F`). O contorno de foco e o destaque do nó selecionado são em Magenta escurecido (`#D3439E`).
- **Temas no mapa:** 7 matizes da marca (Violeta, Ciano, Magenta, Verde e as misturas azul, orquídea e teal), cada um em dois níveis de luminosidade. As subclassificações usam tons da cor do tema.
- **Nuvens no mapa:** os mesmos matizes, no nível escuro.
- **Regra de contraste:** as cores puras da marca aparecem em fundos e destaques grandes. Texto e controles usam as variações escurecidas, para manter contraste AA. A sigla dentro de cada nó escolhe Noite ou branco, o que der mais contraste. Tudo isso é conferido em `tests/unit/contraste.test.ts`.
- **Tema escuro completo:** foi avaliado e não entrou nesta rodada. O site fica claro, com cabeçalho e rodapé escuros. Um tema "Noite" para a página inteira exige revisar as cores fixas do painel e do mapa; fica como proposta.
- **Slogan:** "tecnologia sem mistério" continua no rodapé sem mudança, à espera da decisão da autora.

Não confundir com o nó "Salesforce" no centro do mapa. Ele representa a Salesforce e continua com o placeholder identificado (sf-tutor #13).
