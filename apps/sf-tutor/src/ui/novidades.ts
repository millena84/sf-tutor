// Novidades: notas de versão para quem usa a página. Uma entrada por publicação marcante, a mais recente primeiro.
// Os números de cada nota são os da data da publicação (registro histórico); os números atuais ficam em Método.
import { h } from './dom';

interface Nota {
  versao: string;
  data: string;
  titulo: string;
  resumo: string;
  secoes: { titulo: string; itens: string[] }[];
  /** créditos de quem reportou erros corrigidos nesta versão (nome ou @usuario do GitHub, como a pessoa autorizou) */
  agradecimentos?: string[];
}

export const NOVIDADES: Nota[] = [
  {
    versao: 'MVP de lançamento',
    data: 'novembro de 2026',
    titulo: 'Primeira versão pública do sf-tutor',
    resumo: 'Um mapa visual e navegável do ecossistema Salesforce: o que cada funcionalidade faz, quais metadata types e objetos ' +
      'a representam e o que significa cada propriedade e cada campo, sempre com a fonte oficial.',
    secoes: [
      {
        titulo: 'O que você encontra',
        itens: [
          'Mapa em duas visões: por funcionalidade (14 temas e 92 temas internos) e por nuvem (14 nós, incluindo Add-ons). Dá para ver como mapa ou como lista.',
          'Clique num item para destacar o que se liga a ele; o resto vai para o segundo plano.',
          'Ficha de cada item: o que é, para que serve, exemplo, disponibilidade, fontes e o estado de cada informação (verificado, desconhecido, não aplicável, não exposto ou bloqueado).',
          '194 metadata types com ficha, incluindo os 154 classificados como Core (a camada compartilhada por todas as nuvens).',
          '84 objetos de API e cerca de 6.900 propriedades XML e campos, abertos numa tabela com tipo, versão, default e explicação em português.',
          'Exemplos de XML e SOQL prontos para copiar (só texto: nada é executado).',
          'Busca em todo o inventário de metadata types da API 68.0, inclusive os que ainda não têm ficha.',
          'Método: de onde vem cada informação, a data de verificação, o nível de evidência de cada ligação e como a IA foi usada.',
          'Navegação por teclado, modo leitura e cores com contraste conferido.',
          'Botão "Reportar erro" em cada ficha e em cada campo da tabela: o aviso sai pelo seu e-mail ou vira uma issue pública no GitHub. Quem reportar pode receber crédito aqui nas Novidades.',
        ],
      },
      {
        titulo: 'Limites desta versão',
        itens: [
          'A lista de metadata types de cada nuvem é parcial: esta versão organizou os tipos pela classificação funcional. Cada nuvem mostra quantos tipos já estão no mapa e quantos ainda estão em avaliação.',
          '646 metadata types do inventário ainda não foram classificados entre Core e nuvens.',
          'A validação é documental, feita na documentação oficial da versão 264.0 (API 68.0, Winter \'27). Nada foi testado numa org real.',
          'As explicações foram redigidas com apoio de IA a partir das páginas oficiais; quando a documentação não descreve um item, a ficha diz isso em vez de supor.',
          'Os temas são uma organização didática do projeto, não a nomenclatura oficial da Salesforce.',
        ],
      },
      {
        titulo: 'Próximos passos',
        itens: [
          'Classificar os metadata types restantes por nuvem e completar as listas de cada nuvem.',
          'Camada de certificações Salesforce ligada aos temas.',
          'Guia "Como descobrir o que existe numa org" (EntityDefinition e afins).',
          'Revisão de acessibilidade com leitor de tela.',
        ],
      },
    ],
  },
];

export function conteudoNovidades(): HTMLElement {
  return h('div', { class: 'novidades' },
    NOVIDADES.map((n) => h('section', { class: 'nota-versao', 'aria-labelledby': `nv-${n.versao.replace(/\W+/g, '-')}` },
      h('h3', { id: `nv-${n.versao.replace(/\W+/g, '-')}` }, `${n.versao} · ${n.data}`),
      h('p', null, h('strong', null, n.titulo), '. ', n.resumo),
      n.secoes.map((s) => [h('h4', null, s.titulo), h('ul', { class: 'lista' }, s.itens.map((i) => h('li', null, i)))]),
      n.agradecimentos?.length ? [h('h4', null, 'Correções da comunidade'),
        h('p', null, `Obrigado a ${n.agradecimentos.join(', ')} por reportar erros corrigidos nesta versão.`)] : null)),
    h('p', { class: 'nota' }, 'Os números de cada nota são os da data da publicação. Os números atuais estão em Método.'));
}
