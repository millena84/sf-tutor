// Paleta própria do sf-tutor (a referência flavinho.pages.dev não pôde ser aberta: robots bloqueia leitura automática).
// Duas escalas: por classificação e por nuvem. Sub-classificações usam tons próximos da classificação.

const PALETA_CLASSIFICACAO = [
  '#2563eb', '#dc2626', '#059669', '#d97706', '#7c3aed', '#db2777', '#0891b2',
  '#65a30d', '#ea580c', '#4f46e5', '#0d9488', '#9333ea', '#be123c', '#475569',
];
const PALETA_NUVEM = ['#0f766e', '#1d4ed8', '#b45309', '#7e22ce', '#be185d', '#15803d'];

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
    const f = 0.18 + (i % 4) * 0.12;
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

/** Texto legível sobre a cor (contraste simples por luminância). */
export function corTexto(fundo: string): string {
  const [r, g, b] = hex(fundo).map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  const L = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return L > 0.4 ? '#0f172a' : '#ffffff';
}
