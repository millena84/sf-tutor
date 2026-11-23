# Marca Desbugando (logo oficial do site)

Logo oficial do sf-tutor: o **bug fofo com lupa** desenhado pela autora (2026-11-21). É a figura principal da folha "Mascote: bug fofo" (`mascote.svg`, enviada pela autora pelo Drive), recortada sem alterar o desenho. Substitui o inseto de traço fino com lupa e, antes dele, o símbolo B · lâmpada-bug de 2026-11-08.
- **Desenho:** joaninha lilás (`#A78BFA`) com contorno ameixa (`#4A1D4F`), antenas com bolinhas rosa, olhos grandes com brilho, bochechas, boquinha, pintas rosa e verde e a lupa à direita.
- **Fundo:** quadrado lavanda claro arredondado (`#F3E8FF`), como no favicon que a autora enviou antes. É ele que mantém o desenho legível no cabeçalho escuro: sem esse fundo, o contorno ameixa e as antenas somem. Por isso há um arquivo só.
- **Outras expressões da folha** (sorrindo, feliz, surpresa, bug achado!) e os testes de favicon ficam no arquivo da autora; não foram trazidas para o site.
- **Paleta do site:** Noite `#0B0F2A`, Faixa roxa `#1C1440`, Ciano `#3EE6F2`, Magenta `#FF4FB8`, Violeta `#9B6BFF`, Verde `#2BBE6A`, Claro `#F5F7FF`. Os tons do bug são os do desenho da autora e não entram nos testes de contraste do site.

| Arquivo | Uso |
|---|---|
| `public/marca/desbugando-bug.svg` | logo do cabeçalho (e qualquer fundo) |
| `public/favicon.svg` | ícone da aba (mesmo desenho); a 16 px fica só a silhueta |

## Como a paleta é usada no site (C2, #23, 2026-11-17)

- **Cabeçalho:** fundo Noite, texto Claro, logo `desbugando-bug.svg` e "des" em Magenta.
- **Rodapé:** fundo Faixa roxa, borda em Violeta.
- **Área de leitura:** fundo Claro e superfícies brancas.
- **Destaques:** botões principais, seleção e links em Violeta escurecido (`#704FBF` e `#5A429F`). O contorno de foco e o destaque do nó selecionado são em Magenta escurecido (`#D3439E`).
- **Temas no mapa:** 7 matizes da marca (Violeta, Ciano, Magenta, Verde e as misturas azul, orquídea e teal), cada um em dois níveis de luminosidade. As subclassificações usam tons da cor do tema.
- **Nuvens no mapa:** os mesmos matizes, no nível escuro.
- **Regra de contraste:** as cores puras da marca aparecem em fundos e destaques grandes. Texto e controles usam as variações escurecidas, para manter contraste AA. A sigla dentro de cada nó escolhe Noite ou branco, o que der mais contraste. Tudo isso é conferido em `tests/unit/contraste.test.ts`.
- **Tema escuro completo:** foi avaliado e não entrou nesta rodada. O site fica claro, com cabeçalho e rodapé escuros. Um tema "Noite" para a página inteira exige revisar as cores fixas do painel e do mapa; fica como proposta.
- **Slogan:** "tecnologia sem mistério" continua no rodapé sem mudança, à espera da decisão da autora.

Não confundir com o nó "Salesforce" no centro do mapa. Ele representa a Salesforce e continua com o placeholder identificado (sf-tutor #13).
