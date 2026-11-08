// Construção de DOM sem innerHTML: todo conteúdo dos dados entra como texto (sem HTML arbitrário).

type Filho = Node | string | number | null | undefined | false | Filho[];
type ValorAttr = string | number | boolean | undefined | null | EventListener | Record<string, EventListener>;
type Attrs = { [k: string]: ValorAttr; on?: Record<string, EventListener> };

export function h<K extends keyof HTMLElementTagNameMap>(tag: K, attrs?: Attrs | null, ...filhos: Filho[]): HTMLElementTagNameMap[K] {
  const el = document.createElement(tag);
  if (attrs) {
    for (const [k, v] of Object.entries(attrs)) {
      if (v === undefined || v === null || v === false) continue;
      if (k === 'on' && typeof v === 'object') {
        for (const [ev, fn] of Object.entries(v as Record<string, EventListener>)) el.addEventListener(ev, fn);
      } else if (k === 'src') {
        const s = String(v);
        if (/^https:\/\//i.test(s) || s.startsWith('./') || s.startsWith('/')) el.setAttribute('src', s);
      } else if (k === 'href') {
        const s = String(v);
        if (/^https?:\/\//i.test(s) || s.startsWith('?') || s.startsWith('#')) el.setAttribute('href', s);
      } else if (typeof v === 'function') {
        el.addEventListener(k.replace(/^on/, '').toLowerCase(), v as EventListener);
      } else if (v === true) {
        el.setAttribute(k, '');
      } else {
        el.setAttribute(k, String(v));
      }
    }
  }
  anexar(el, filhos);
  return el;
}

function anexar(el: HTMLElement, filhos: Filho[]): void {
  for (const f of filhos) {
    if (f === null || f === undefined || f === false) continue;
    if (Array.isArray(f)) anexar(el, f);
    else if (typeof f === 'string' || typeof f === 'number') el.appendChild(document.createTextNode(String(f)));
    else el.appendChild(f);
  }
}

export function limpar(el: Element): void {
  while (el.firstChild) el.removeChild(el.firstChild);
}

export async function copiar(texto: string, botao?: HTMLElement): Promise<void> {
  try {
    await navigator.clipboard.writeText(texto);
    if (botao) {
      const o = botao.textContent;
      botao.textContent = 'Copiado';
      setTimeout(() => (botao.textContent = o), 1500);
    }
  } catch {
    const ta = h('textarea', null, texto);
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
  }
}

export function anunciar(msg: string): void {
  const r = document.getElementById('anuncio');
  if (r) {
    r.textContent = '';
    setTimeout(() => (r.textContent = msg), 30);
  }
}
