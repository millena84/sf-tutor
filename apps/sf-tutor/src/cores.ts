// Paleta Desbugando (#23; ver MARCA.md). Duas escalas: por tema (classificação nos dados) e por nuvem.
// Temas internos (subclassificação) usam tons próximos da cor do tema.
//
// Escala por tema: 7 matizes tirados da marca (Violeta, Ciano, Magenta, Verde e as misturas azul = Ciano+Violeta,
// orquídea = Magenta+Violeta, teal = Ciano+Verde), cada um em dois níveis de luminosidade: a cor pura e a cor
// misturada a 55% com Noite. A ordem alterna escuro e claro e muda de matiz a cada passo, para que temas vizinhos
// no mapa difiram em luminosidade e não só em matiz.
export const PALETA_CLASSIFICACAO = [
  '#4c388a', '#3ee6f2', '#792c6a', '#2bbe6a', '#375487', '#cd5ddc', '#1d6765',
  '#9b6bff', '#227084', '#ff4fb8', '#195e47', '#6ca8f8', '#62327a', '#34d2ae',
];
// Escala por nuvem: os mesmos 14 tons da escala por tema, em outra ordem (começa pelos escuros),
// para que até 14 nuvens tenham cor própria. A sigla dentro do nó escolhe o texto de maior contraste.
export const PALETA_NUVEM = [
  '#4c388a', '#227084', '#792c6a', '#195e47', '#375487', '#62327a', '#1d6765',
  '#9b6bff', '#3ee6f2', '#ff4fb8', '#2bbe6a', '#6ca8f8', '#cd5ddc', '#34d2ae',
];

export class Cores {
  private cls = new Map<string, string>();
  private nuv = new Map<string, string>();
  constructor(classificacoes: string[], nuvens: string[]) {
    classificacoes.forEach((c, i) => this.cls.set(c, PALETA_CLASSIFICACAO[i % PALETA_CLASSIFICACAO.length]));
    nuvens.forEach((n, i) => this.nuv.set(n, PALETA_NUVEM[i % PALETA_NUVEM.length]));
  }
  classificacao(id: string): string {
    return this.cls.get(id) ?? '#64748b';
  }
  nuvem(id: string): string {
    return this.nuv.get(id) ?? '#64748b';
  }
  /** Tom próximo da cor base para a i-ésima sub-classificação. */
  tom(cor: string, i: number): string {
    const f = 0.30 + (i % 4) * 0.12;
    return misturar(cor, '#ffffff', f);
  }
  entradasClassificacao(): [string, string][] {
    return [...this.cls.entries()];
  }
  entradasNuvem(): [string, string][] {
    return [...this.nuv.entries()];
  }
}

export function misturar(a: string, b: string, t: number): string {
  const pa = hex(a), pb = hex(b);
  const m = pa.map((v, i) => Math.round(v + (pb[i] - v) * t));
  return '#' + m.map((v) => v.toString(16).padStart(2, '0')).join('');
}

function hex(c: string): number[] {
  const s = c.replace('#', '');
  return [0, 2, 4].map((i) => parseInt(s.slice(i, i + 2), 16));
}

/** Luminância relativa (WCAG 2.x). */
export function luminancia(cor: string): number {
  const [r, g, b] = hex(cor).map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/** Razão de contraste WCAG entre duas cores. */
export function contraste(a: string, b: string): number {
  const [x, y] = [luminancia(a), luminancia(b)].sort((m, n) => n - m);
  return (x + 0.05) / (y + 0.05);
}

const TEXTO_ESCURO = '#0b0f2a';
const TEXTO_CLARO = '#ffffff';

/** Texto legível sobre a cor: escolhe, entre Noite e branco, o que dá mais contraste. */
export function corTexto(fundo: string): string {
  return contraste(fundo, TEXTO_ESCURO) >= contraste(fundo, TEXTO_CLARO) ? TEXTO_ESCURO : TEXTO_CLARO;
}
