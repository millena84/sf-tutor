# Marca Desbugando (logo oficial do site)

Logo oficial do sf-tutor: o **bug fofo com lupa** da família Desbugando (redesenho de 2026-11-21, a pedido da autora; substitui o inseto de traço fino com lupa, que por sua vez veio do símbolo B · lâmpada-bug de 2026-11-08).
- **Desenho:** corpo e cabeça arredondados em Violeta, barriga clara, olhos grandes com brilho, bochechas e antenas em Magenta, perninhas curtas e a lupa em Ciano na mão direita. Corpo, cabeça e olhos são iguais nas duas versões; só mudam o halo, as antenas e pernas, o cabo e a lente.
- **Paleta:** Noite `#0B0F2A`, Faixa roxa `#1C1440`, Ciano `#3EE6F2`, Magenta `#FF4FB8`, Violeta `#9B6BFF`, Verde `#2BBE6A`, Claro `#F5F7FF`. Tons do corpo: Violeta `#9B6BFF`, cabeça `#7E55E0` e barriga `#C9B3FF`. Na versão clara, Magenta e Ciano usam as variações escurecidas (`#D6338F` e `#0B9FB0`).

| Arquivo | Uso |
|---|---|
| `public/marca/desbugando-bug-lupa-clara.svg` | fundo claro |
| `public/marca/desbugando-bug-lupa-escura.svg` | fundo escuro (cabeçalho do site) |
| `public/favicon.svg` | ícone da aba (bloco roxo); em 16 px fica só a silhueta |

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
