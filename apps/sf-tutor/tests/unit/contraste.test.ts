// #23: contraste AA da paleta Desbugando na interface e nos nós do mapa.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { Cores, PALETA_CLASSIFICACAO, PALETA_NUVEM, contraste, corTexto, luminancia, misturar } from '../../src/cores';

// ambiente jsdom: import.meta.url não é file://; o vitest roda a partir da pasta do app
const css = readFileSync(resolve(process.cwd(), 'src/estilos.css'), 'utf8');
const raiz = css.slice(css.indexOf(':root {'), css.indexOf('}', css.indexOf(':root {')));
function variavel(nome: string): string {
  const m = raiz.match(new RegExp(`--${nome}:\\s*([^;]+);`));
  if (!m) throw new Error(`variável --${nome} não encontrada`);
  const v = m[1].trim();
  return v.startsWith('var(') ? variavel(v.slice(6, -1)) : v;
}

describe('interface (variáveis de estilos.css)', () => {
  const branco = '#ffffff';
  it.each([
    ['texto', 'fundo', 4.5], ['texto', 'superficie', 4.5], ['texto-2', 'fundo', 4.5], ['texto-2', 'superficie', 4.5],
    ['destaque', 'superficie', 4.5], ['destaque-2', 'superficie', 4.5], ['marca-texto', 'superficie', 4.5],
    ['texto', 'destaque-suave', 4.5], ['texto', 'superficie-2', 4.5],
    ['verificado', 'superficie', 4.5], ['desconhecido', 'superficie', 4.5], ['nao-aplicavel', 'superficie', 4.5],
    ['nao-exposto', 'superficie', 4.5], ['bloqueado', 'superficie', 4.5],
    // contorno de foco e bordas de controle: 3:1 (WCAG 1.4.11)
    ['foco', 'fundo', 3], ['foco', 'superficie', 3], ['borda-forte', 'superficie', 3],
    // cabeçalho e rodapé escuros
    ['claro', 'noite', 4.5], ['magenta', 'noite', 4.5], ['claro', 'faixa-roxa', 4.5], ['magenta', 'faixa-roxa', 4.5],
  ])('%s sobre %s ≥ %s:1', (a, b, minimo) => {
    expect(contraste(variavel(a), variavel(b))).toBeGreaterThanOrEqual(minimo as number);
  });
  it('texto branco sobre os botões de destaque', () => {
    expect(contraste(branco, variavel('destaque'))).toBeGreaterThanOrEqual(4.5);
    expect(contraste(branco, variavel('destaque-2'))).toBeGreaterThanOrEqual(4.5);
  });
  it('cores fixas do cabeçalho e do rodapé', () => {
    expect(contraste('#BABDCA', variavel('noite'))).toBeGreaterThanOrEqual(4.5);
    expect(contraste('#D6D8E6', variavel('faixa-roxa'))).toBeGreaterThanOrEqual(4.5);
  });
});

describe('nós do mapa', () => {
  it('a sigla dentro de cada nó tem contraste AA, inclusive nos tons das subclassificações', () => {
    const cores = new Cores([], []);
    for (const base of [...PALETA_CLASSIFICACAO, ...PALETA_NUVEM]) {
      for (const cor of [base, ...[0, 1, 2, 3].map((i) => cores.tom(base, i)), misturar(base, '#000000', 0.08)]) {
        expect(contraste(cor, corTexto(cor)), cor).toBeGreaterThanOrEqual(4.5);
      }
    }
  });
  it('temas vizinhos na escala diferem em luminosidade, não só em matiz', () => {
    for (let i = 0; i + 1 < PALETA_CLASSIFICACAO.length; i++) {
      const [a, b] = [luminancia(PALETA_CLASSIFICACAO[i]), luminancia(PALETA_CLASSIFICACAO[i + 1])];
      expect(Math.abs(a - b), `${PALETA_CLASSIFICACAO[i]} × ${PALETA_CLASSIFICACAO[i + 1]}`).toBeGreaterThan(0.08);
    }
  });
});
