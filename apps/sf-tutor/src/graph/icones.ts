// Ícone dentro da bolinha: SVG gerado com sigla/símbolo do tipo (sem marcas de terceiros).
import { corTexto } from '../cores';

const cache = new Map<string, string>();

export function iconeSvg(texto: string, fundo: string, opts: { placeholder?: boolean } = {}): string {
  const chave = `${texto}|${fundo}|${opts.placeholder ? 1 : 0}`;
  const c = cache.get(chave);
  if (c) return c;
  const t = esc(texto);
  const tam = texto.length <= 2 ? 40 : texto.length <= 3 ? 32 : texto.length <= 5 ? 22 : 16;
  const cor = corTexto(fundo);
  const extra = opts.placeholder
    ? `<text x="50" y="72" text-anchor="middle" font-family="system-ui,sans-serif" font-size="10" fill="${cor}" opacity="0.85">logo pendente</text>`
    : '';
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="${fundo}"/><text x="50" y="${opts.placeholder ? 54 : 50}" dy="0.35em" text-anchor="middle" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-weight="700" font-size="${tam}" fill="${cor}">${t}</text>${extra}</svg>`;
  const url = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  cache.set(chave, url);
  return url;
}

function esc(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/** Sigla curta para funcionalidades (até 2 letras das palavras significativas). */
export function siglaFuncionalidade(nome: string): string {
  const pal = nome.split(/[\s/-]+/).filter((p) => p.length > 2 || /^[A-Z]/.test(p));
  const s = (pal.length >= 2 ? pal[0][0] + pal[1][0] : nome.slice(0, 2)).toUpperCase();
  return s;
}
