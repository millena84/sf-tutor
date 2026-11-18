# Acessibilidade do sf-tutor

Meta: WCAG 2.2, nível AA. Issue de acompanhamento: #19.

## O que é verificado automaticamente

- `tests/e2e/acessibilidade.spec.ts`: axe-core (WCAG 2.0, 2.1 e 2.2 AA) em desktop e em 360px. Cobre seis fichas (início, funcionalidade, metadata type, objeto, tema, nuvem), a busca aberta, o modo lista, a janela de campos e as janelas Método, Legenda e Filtros. Qualquer violação faz o teste falhar.
- `tests/unit/contraste.test.ts`: contraste da paleta (texto 4,5:1; foco e bordas 3:1) e da sigla dentro de cada nó.
- `tests/e2e/navegacao.spec.ts`: contraste real dos resultados da busca.

O que o axe não alcança:
- O mapa é desenhado em canvas, e o axe não lê o conteúdo dele. A alternativa textual é o modo Lista, com a mesma navegação por caminho.
- A experiência real com leitor de tela, coberta pelo roteiro abaixo.

## Roteiro manual com leitor de tela

Leitores: NVDA no Windows (Chrome ou Firefox) ou VoiceOver no macOS ou iOS (Safari). Anote, para cada passo, o que foi anunciado e se ficou claro.

1. **Abrir o site.** O título da página é anunciado. Com Tab, o primeiro item é o link para pular para o conteúdo; ative-o e confirme que o foco vai para a ficha.
2. **Buscar.** No campo de busca, digite `PermissionSet`. O número de resultados é anunciado, as setas percorrem a lista, cada resultado diz nome e tipo, e Enter abre a ficha.
3. **Ler a ficha.** Navegue por títulos (H no NVDA; rotor no VoiceOver). A ordem esperada é h2 com o nome do item, depois h3 com os blocos ("O que é" e outros), sem pular nível. Os selos de estado ("Verificado", "Desconhecido") são lidos como texto.
4. **Distinguir nomes iguais.** Na ficha "Permission sets", os links "PermissionSet" da seção de representações têm descrição: "Metadata type" para um e "Objeto API" para o outro.
5. **Abrir campos.** Em `User`, ative "Ver N campos em tabela". A janela abre com o foco nela; o título é anunciado; a tabela tem cabeçalhos; Esc fecha e devolve o foco ao botão.
6. **Seguir uma relação.** Na ficha, ative um item relacionado (por exemplo, um objeto). O painel muda, e o novo título é anunciado (região viva). O caminho no topo permite voltar.
7. **Voltar.** Use o caminho no topo da ficha ou o botão "Voltar ao caminho". O foco não pode se perder.
8. **Modo lista.** Troque para "Lista" e repita os passos 2 e 6 sem usar o mapa.
9. **Reduzir animações.** O botão é anunciado como botão de alternância, e o estado (pressionado ou não) bate com o efeito.

Ao terminar, registre o resultado na #19: leitor, navegador, data, passos que funcionaram e problemas, com o texto anunciado.
