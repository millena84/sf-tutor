// Modo lista/árvore: mesmo conteúdo e mesmas ocorrências do mapa, acessível por teclado e leitor de tela.
import type { Cena } from '../model/adaptador';
import { NOME_TIPO } from '../rotulos';
import { h, limpar } from './dom';

export interface CtxLista {
  rotulo(id: string): string;
  tipo(id: string): keyof typeof NOME_TIPO;
  oculto(id: string): string | null;
  expandido(chave: string): boolean;
  selecionar(chave: string): void;
  alternar(chave: string): void;
  paginar(chave: string): void;
}

export function renderizarLista(alvo: HTMLElement, cena: Cena, ctx: CtxLista, selecionada: string | null): void {
  const focoAnterior = (document.activeElement as HTMLElement | null)?.dataset?.chave;
  limpar(alvo);
  const raiz = h('ul', { role: 'tree', class: 'arvore', 'aria-label': 'Mapa em forma de lista' });
  const itens: HTMLElement[] = [];
  const pagPorPai = new Map(cena.paginacoes.map((p) => [p.paiChave, p]));
  const ordem: { tipo: 'o' | 'p'; chave: string; nivel: number }[] = [];
  const filhos = new Map<string, string[]>();
  for (const o of cena.ocorrencias) if (o.paiChave) (filhos.get(o.paiChave) ?? filhos.set(o.paiChave, []).get(o.paiChave)!).push(o.chave);
  const porChave = new Map(cena.ocorrencias.map((o) => [o.chave, o]));
  const visitar = (chave: string, nivel: number) => {
    ordem.push({ tipo: 'o', chave, nivel });
    for (const f of filhos.get(chave) ?? []) visitar(f, nivel + 1);
    const p = pagPorPai.get(chave);
    if (p) ordem.push({ tipo: 'p', chave: p.chave, nivel: nivel + 1 });
  };
  if (cena.ocorrencias.length) visitar(cena.ocorrencias[0].chave, 1);
  for (const it of ordem) {
    if (it.tipo === 'p') {
      const p = cena.paginacoes.find((x) => x.chave === it.chave)!;
      const b = h('button', { type: 'button', tabindex: -1, class: 'item-arvore item-mais', 'data-chave': p.chave, style: `--nivel:${it.nivel}`, on: { click: () => ctx.paginar(p.chave) } }, `Mostrar mais ${Math.min(p.restantes, 24)} de ${p.restantes} restantes`);
      itens.push(b);
      raiz.append(h('li', { role: 'none' }, b));
      continue;
    }
    const o = porChave.get(it.chave)!;
    const exp = ctx.expandido(o.chave);
    const oculto = ctx.oculto(o.id);
    const tipo = ctx.tipo(o.id);
    const sel = selecionada === o.chave;
    const b = h('button', {
      type: 'button', role: 'treeitem', class: `item-arvore${sel ? ' selecionado' : ''}${oculto ? ' oculto' : ''}`, 'data-chave': o.chave,
      'aria-level': it.nivel, 'aria-selected': String(sel), 'aria-expanded': o.totalFilhos ? String(exp) : undefined, style: `--nivel:${it.nivel}`,
      tabindex: -1,
    },
    h('span', { class: 'marcador', 'aria-hidden': 'true' }, o.totalFilhos ? (exp ? '▾' : '▸') : '·'),
    h('span', { class: `ico ico-${tipo}`, 'aria-hidden': 'true' }, ''),
    h('span', { class: 'rot' }, ctx.rotulo(o.id)),
    h('span', { class: 'tipo-mini' }, ` ${NOME_TIPO[tipo]}`),
    o.totalFilhos ? h('span', { class: 'contagem' }, ` (${o.totalFilhos})`) : null,
    oculto ? h('span', { class: 'nota' }, ` — esmaecido: ${oculto}`) : null);
    b.addEventListener('click', () => ctx.selecionar(o.chave));
    b.addEventListener('dblclick', () => ctx.alternar(o.chave));
    itens.push(b);
    raiz.append(h('li', { role: 'none' }, b));
  }
  raiz.addEventListener('keydown', (ev) => {
    const atual = document.activeElement as HTMLElement;
    const i = itens.indexOf(atual);
    if (i < 0) return;
    const chave = atual.dataset.chave!;
    const o = porChave.get(chave);
    if (ev.key === 'ArrowDown') { itens[Math.min(i + 1, itens.length - 1)].focus(); ev.preventDefault(); }
    else if (ev.key === 'ArrowUp') { itens[Math.max(i - 1, 0)].focus(); ev.preventDefault(); }
    else if (ev.key === 'Home') { itens[0].focus(); ev.preventDefault(); }
    else if (ev.key === 'End') { itens[itens.length - 1].focus(); ev.preventDefault(); }
    else if (ev.key === 'ArrowRight' && o?.totalFilhos) {
      if (!ctx.expandido(chave)) ctx.alternar(chave);
      else itens[Math.min(i + 1, itens.length - 1)].focus();
      ev.preventDefault();
    } else if (ev.key === 'ArrowLeft' && o) {
      if (ctx.expandido(chave)) ctx.alternar(chave);
      else if (o.paiChave) itens.find((x) => x.dataset.chave === o.paiChave)?.focus();
      ev.preventDefault();
    } else if (ev.key === '+' && o?.totalFilhos) { ctx.alternar(chave); ev.preventDefault(); }
  });
  alvo.append(raiz);
  const alvoFoco = itens.find((x) => x.dataset.chave === (focoAnterior ?? selecionada)) ?? itens.find((x) => x.dataset.chave === selecionada) ?? itens[0];
  if (alvoFoco) alvoFoco.tabIndex = 0;
  if (focoAnterior && alvoFoco) alvoFoco.focus();
}
