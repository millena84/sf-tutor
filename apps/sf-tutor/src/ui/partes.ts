// Peças reutilizáveis do painel: estado, afirmação, fontes, código copiável, seções expansíveis.
import type { Afirmacao, Fonte } from '../data/tipos';
import { ESTADO, rotuloEstado } from '../rotulos';
import { copiar, h } from './dom';

export interface CtxPartes {
  fontes: Record<string, Fonte>;
}

export function selo(estado?: string): HTMLElement {
  const e = estado ? ESTADO[estado] : undefined;
  return h('span', { class: `selo selo-${estado ?? 'nenhum'}`, title: e?.explicacao ?? 'Estado não informado' }, e ? `${e.simbolo} ${e.rotulo}` : rotuloEstado(estado));
}

export function fontesEl(ctx: CtxPartes, evid?: { fonte: string; secao?: string; nota?: string }[] | null): HTMLElement | null {
  if (!evid?.length) return null;
  return h('ul', { class: 'fontes', 'aria-label': 'Fontes' },
    evid.map((e) => {
      const f = ctx.fontes[e.fonte];
      if (!f) return h('li', null, h('span', { class: 'fonte-id' }, e.fonte), ' (fonte não encontrada no registro)');
      const meta = [f.versao && `versão ${f.versao}`, f.data_verificacao && `verificada em ${f.data_verificacao}`].filter(Boolean).join(' · ');
      return h('li', null,
        h('a', { href: f.url, target: '_blank', rel: 'noopener noreferrer' }, f.titulo),
        meta ? h('span', { class: 'fonte-meta' }, ` — ${meta}`) : null,
        e.secao ? h('span', { class: 'fonte-meta' }, ` · seção: ${e.secao}`) : null,
        e.nota ? h('span', { class: 'fonte-meta' }, ` (${e.nota})`) : null,
      );
    }));
}

export function texto(rotulo: string, valor: unknown, opts: { didatico?: boolean } = {}): HTMLElement | null {
  if (valor === undefined || valor === null || valor === '' || (Array.isArray(valor) && !valor.length)) return null;
  return h('div', { class: 'campo-txt' }, h('h4', null, rotulo, opts.didatico ? h('span', { class: 'marca-didatica', title: 'Redação do projeto a partir das fontes citadas; não é texto oficial.' }, ' · explicação do projeto') : null), valorEl(valor));
}

export function valorEl(v: unknown): Node {
  if (v === null || v === undefined) return h('span', { class: 'vazio' }, 'não informado');
  if (typeof v === 'boolean') return document.createTextNode(v ? 'sim' : 'não');
  if (typeof v === 'string' || typeof v === 'number') return h('p', null, String(v));
  if (Array.isArray(v)) {
    if (v.every((x) => typeof x === 'string' || typeof x === 'number')) return h('ul', { class: 'lista' }, v.map((x) => h('li', null, String(x))));
    return h('ul', { class: 'lista' }, v.map((x) => h('li', null, valorEl(x))));
  }
  if (typeof v === 'object') {
    const o = v as Record<string, unknown>;
    return h('dl', { class: 'kv' }, Object.entries(o).flatMap(([k, x]) => [h('dt', null, k), h('dd', null, valorEl(x))]));
  }
  return document.createTextNode(String(v));
}

/** Afirmação com estado: mostra valor, estado distinto, condição, nota e fontes logo abaixo. */
export function afirmacao(ctx: CtxPartes, rotulo: string, a: Afirmacao | undefined | null, fmt?: (v: unknown) => Node | string | null): HTMLElement {
  if (!a) return h('div', { class: 'afirmacao' }, h('h4', null, rotulo), h('p', { class: 'vazio' }, 'Não registrado no cadastro.'));
  const temValor = a.valor !== undefined && a.valor !== null;
  const val = temValor ? (fmt ? fmt(a.valor) : valorEl(a.valor)) : null;
  return h('div', { class: `afirmacao estado-${a.estado ?? 'nenhum'}` },
    h('h4', null, rotulo, ' ', selo(a.estado)),
    val ? (typeof val === 'string' ? h('p', null, val) : val) : (a.estado && a.estado !== 'verificado' ? h('p', { class: 'vazio' }, semValor(a.estado)) : null),
    a.condicao ? h('p', { class: 'condicao' }, h('strong', null, 'Condição: '), String(a.condicao)) : null,
    a.nota ? h('p', { class: 'nota' }, String(a.nota)) : null,
    fontesEl(ctx, a.evidencias),
  );
}

export function semValor(estado: string): string {
  switch (estado) {
    case 'desconhecido': return 'Desconhecido: ainda não investigado ou sem evidência suficiente.';
    case 'nao_aplicavel': return 'Não aplicável a este item.';
    case 'nao_exposto': return 'Não exposto: a fonte documenta a indisponibilidade.';
    case 'bloqueado': return 'Bloqueado: falta fonte, acesso ou licença.';
    default: return 'Sem valor registrado.';
  }
}

export function codigo(rotulo: string, conteudo: string, linguagem: string, nota?: string | null): HTMLElement {
  const btn = h('button', { type: 'button', class: 'btn-copiar', 'aria-label': `Copiar ${rotulo}` }, 'Copiar');
  btn.addEventListener('click', () => copiar(conteudo, btn));
  return h('figure', { class: 'codigo' },
    h('figcaption', null, h('span', null, rotulo, h('span', { class: 'ling' }, ` · ${linguagem}`)), btn),
    h('pre', { tabindex: 0 }, h('code', null, conteudo)),
    nota ? h('p', { class: 'nota' }, nota) : null,
  );
}

export function secao(titulo: string, aberta: boolean, ...conteudo: (Node | null | false | undefined)[]): HTMLElement | null {
  const itens = conteudo.filter(Boolean) as Node[];
  if (!itens.length) return null;
  const d = h('details', { class: 'secao' }, h('summary', null, titulo), ...itens);
  if (aberta) d.open = true;
  return d;
}

export function listaTexto(rotulo: string, itens: unknown[] | undefined | null, vazio?: string): HTMLElement | null {
  if (!itens?.length) return vazio ? h('div', { class: 'campo-txt' }, h('h4', null, rotulo), h('p', { class: 'vazio' }, vazio)) : null;
  return h('div', { class: 'campo-txt' }, h('h4', null, rotulo), h('ul', { class: 'lista' }, itens.map((x) => h('li', null, valorEl(x)))));
}

/** Seção de segurança: qualquer chave do cadastro que o renderizador não tratou aparece aqui (nada some em silêncio). */
export function restantes(ent: Record<string, unknown>, tratadas: string[]): HTMLElement | null {
  const resto = Object.entries(ent).filter(([k]) => !tratadas.includes(k));
  if (!resto.length) return null;
  return secao('Outros dados do cadastro', false, h('dl', { class: 'kv' }, resto.flatMap(([k, v]) => [h('dt', null, k), h('dd', null, valorEl(v))])));
}
