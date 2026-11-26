// Boas-vindas e tour guiado (issue #147): um cartão curto na primeira visita e 6 passos sobre a interface real.
// O balão do tour não é modal (o mapa e a ficha continuam visíveis e utilizáveis); Esc sai, Enter/botões avançam.
// "Já vi o tour" fica no armazenamento local, sempre com tratamento de erro (pode estar bloqueado ou indisponível).
import { h } from './dom';

export const CHAVE_TOUR = 'metadata-desbugado:tour-visto';

export function tourVisto(armazenamento: Pick<Storage, 'getItem'> | null = localStorageSeguro()): boolean {
  try { return armazenamento?.getItem(CHAVE_TOUR) === '1'; } catch { return false; }
}

export function marcarTourVisto(armazenamento: Pick<Storage, 'setItem'> | null = localStorageSeguro()): void {
  try { armazenamento?.setItem(CHAVE_TOUR, '1'); } catch { /* sem armazenamento: o cartão volta na próxima visita */ }
}

function localStorageSeguro(): Storage | null {
  try { return window.localStorage; } catch { return null; }
}

/** O que o tour precisa da página: navegar até exemplos reais e abrir a ficha. */
export interface GanchosTour {
  selecionar(caminho: string[]): void;
  abrirId(id: string): void;
  mostrarPainel(): void;
  anunciar(texto: string): void;
}

export interface PassoTour {
  titulo: string;
  texto: string;
  /** Seletor do elemento destacado; se não existir ou estiver oculto, o balão aparece centralizado. */
  alvo: string;
  preparar?: (g: GanchosTour) => void;
}

export const PASSOS: readonly PassoTour[] = [
  {
    titulo: 'Duas formas de ver o mapa',
    texto: 'Por funcionalidade organiza pelo que você quer fazer: acessos, dados, automação. Por nuvem organiza pelos produtos, como Sales Cloud e Service Cloud. O conteúdo é o mesmo; muda o caminho até ele.',
    alvo: '.segmento[aria-label="Visão"]',
  },
  {
    titulo: 'Clique numa bolinha',
    texto: 'Selecionei "Acesso, identidade e segurança". O caminho desde o centro fica destacado no mapa. Para ver o que tem dentro, use "Expandir" na ficha.',
    alvo: '#mapa',
    preparar: (g) => g.selecionar(['salesforce', 'cls:acesso-identidade-e-seguranca']),
  },
  {
    titulo: 'A ficha explica o item',
    texto: 'Aqui ficam o resumo, os detalhes e as fontes oficiais. O selo mostra se a informação foi verificada na fonte ou ainda é uma lacuna; nada é preenchido por suposição.',
    alvo: '#painel',
    preparar: (g) => g.mostrarPainel(),
  },
  {
    titulo: 'Propriedades e campos em tabela',
    texto: 'Abri o PermissionSet, um metadata type. Este botão mostra todas as propriedades do XML numa tabela, com os detalhes e a fonte de cada uma. Objetos API têm o mesmo botão para os campos.',
    alvo: '#conteudo-painel .btn-tabela',
    preparar: (g) => { g.abrirId('mdt:PermissionSet'); g.mostrarPainel(); },
  },
  {
    titulo: 'Busque pelo nome',
    texto: 'Procure por funcionalidade, metadata type, objeto ou campo, em português ou pelo nome técnico. O resultado abre direto na ficha.',
    alvo: '#busca',
  },
  {
    titulo: 'Achou um erro? Avise',
    texto: 'Toda ficha tem "Reportar erro", e nas tabelas o botão aparece ao abrir uma propriedade ou um campo. É sobre o conteúdo do site, não suporte da Salesforce; vai por e-mail ou por issue no GitHub. Em "Método" você vê de onde vêm os dados e o que ainda falta mapear.',
    alvo: '#conteudo-painel .btn-reportar',
    preparar: (g) => g.mostrarPainel(),
  },
];

/** Cartão de boas-vindas (modal curto). Qualquer saída marca o tour como visto. */
export function mostrarBoasVindas(g: GanchosTour): HTMLDialogElement {
  document.getElementById('boas-vindas')?.remove();
  const dlg = h('dialog', { id: 'boas-vindas', class: 'boas-vindas', 'aria-labelledby': 'boas-vindas-titulo' }) as HTMLDialogElement;
  const fazer = h('button', { type: 'button', class: 'btn btn-primario', id: 'btn-fazer-tour' }, 'Fazer o tour');
  const pular = h('button', { type: 'button', class: 'btn', id: 'btn-pular-tour' }, 'Pular');
  let iniciar = false;
  fazer.addEventListener('click', () => { iniciar = true; dlg.close(); });
  pular.addEventListener('click', () => dlg.close());
  dlg.addEventListener('close', () => {
    marcarTourVisto();
    dlg.remove();
    if (iniciar) iniciarTour(g);
    else document.getElementById('mapa')?.focus();
  });
  dlg.append(
    h('img', { class: 'boas-vindas-logo', src: './marca/metadata-desbugado.svg', alt: '', width: '56', height: '56' }),
    h('h2', { id: 'boas-vindas-titulo' }, 'Boas-vindas ao Metadata Desbugado'),
    h('p', null, 'Um mapa do Metadata API da Salesforce: das funcionalidades até os metadata types, objetos API, propriedades e campos, sempre com a fonte oficial.'),
    h('p', null, 'Para quem estuda Salesforce ou precisa consultar rápido, de quem está começando a quem já trabalha com a plataforma.'),
    h('p', null, 'Comece pelo tour (6 passos, cerca de 1 minuto) ou explore direto clicando nas bolinhas.'),
    h('div', { class: 'acoes' }, fazer, pular),
    h('p', { class: 'nota' }, 'Dá para rever o tour pelo rodapé ou em "Método".'),
  );
  document.body.append(dlg);
  dlg.showModal();
  fazer.focus();
  return dlg;
}

let tourAtual: { sair(): void } | null = null;

/** Inicia (ou reinicia) o tour. Devolve uma função para sair. */
export function iniciarTour(g: GanchosTour, passos: readonly PassoTour[] = PASSOS): () => void {
  tourAtual?.sair();
  const origem = document.activeElement instanceof HTMLElement ? document.activeElement : null;
  let i = 0;
  let alvoAtual: Element | null = null;

  const contador = h('p', { class: 'tour-contador', id: 'tour-contador' });
  const titulo = h('h2', { id: 'tour-titulo', tabindex: '-1' });
  const texto = h('p', { id: 'tour-texto' });
  const voltar = h('button', { type: 'button', class: 'btn', id: 'tour-voltar' }, 'Voltar');
  const proximo = h('button', { type: 'button', class: 'btn btn-primario', id: 'tour-proximo' }, 'Próximo');
  const sairBtn = h('button', { type: 'button', class: 'btn tour-sair', id: 'tour-sair' }, 'Sair do tour');
  const balao = h('div', { class: 'tour-balao', id: 'tour-balao', role: 'dialog', 'aria-modal': 'false', 'aria-labelledby': 'tour-titulo', 'aria-describedby': 'tour-texto' },
    contador, titulo, texto, h('div', { class: 'acoes' }, voltar, proximo, sairBtn));

  const limparAlvo = (): void => { alvoAtual?.classList.remove('tour-alvo'); alvoAtual = null; };
  const visivel = (el: Element | null): el is HTMLElement => !!el && (el as HTMLElement).getClientRects().length > 0;

  function posicionar(): void {
    balao.classList.remove('tour-centro', 'tour-acima', 'tour-abaixo');
    balao.style.removeProperty('top'); balao.style.removeProperty('left');
    if (!visivel(alvoAtual)) { balao.classList.add('tour-centro'); return; }
    const r = alvoAtual.getBoundingClientRect();
    const b = balao.getBoundingClientRect();
    const margem = 12;
    const vw = document.documentElement.clientWidth, vh = window.innerHeight;
    const abaixo = vh - r.bottom, acima = r.top;
    // alvo grande (mapa, ficha) ou sem espaço: balão centralizado na parte de baixo ou de cima da tela
    let top: number;
    if (abaixo >= b.height + margem * 2) top = r.bottom + margem;
    else if (acima >= b.height + margem * 2) top = r.top - b.height - margem;
    else top = acima > abaixo ? margem : vh - b.height - margem;
    const left = Math.min(Math.max(margem, r.left + r.width / 2 - b.width / 2), vw - b.width - margem);
    balao.style.top = `${Math.max(margem, top)}px`;
    balao.style.left = `${Math.max(margem, left)}px`;
  }

  function mostrar(n: number): void {
    i = n;
    const p = passos[i];
    limparAlvo();
    posicionar();
    try { p.preparar?.(g); } catch { /* um passo que não consegue preparar o exemplo ainda mostra o texto */ }
    // espera a interface reagir (seleção, gaveta, ficha carregada) antes de medir; desiste em ~1,5 s e centraliza
    const passoAtual = i;
    let tentativas = 0;
    const procurar = (): void => {
      if (!balao.isConnected || i !== passoAtual) return;
      const el = document.querySelector(p.alvo);
      if (!visivel(el) && tentativas++ < 15) { setTimeout(procurar, 100); return; }
      if (visivel(el)) {
        alvoAtual = el;
        el.classList.add('tour-alvo');
        el.scrollIntoView({ block: 'center', inline: 'nearest' });
      }
      posicionar();
      // a gaveta da ficha (celular) e a rolagem podem ainda estar em movimento: confere de novo depois da animação
      setTimeout(() => {
        if (!balao.isConnected || i !== passoAtual) return;
        if (visivel(alvoAtual)) alvoAtual.scrollIntoView({ block: 'center', inline: 'nearest' });
        posicionar();
      }, 450);
    };
    requestAnimationFrame(() => requestAnimationFrame(procurar));
    contador.textContent = `Passo ${i + 1} de ${passos.length}`;
    titulo.textContent = p.titulo;
    texto.textContent = p.texto;
    voltar.disabled = i === 0;
    proximo.textContent = i === passos.length - 1 ? 'Concluir' : 'Próximo';
    titulo.focus();
    g.anunciar(`Tour, passo ${i + 1} de ${passos.length}: ${p.titulo}. ${p.texto}`);
  }

  const aoTeclar = (e: KeyboardEvent): void => {
    if (e.key === 'Escape' && !document.querySelector('dialog[open]')) { e.preventDefault(); sair(); }
  };
  const aoRedimensionar = (): void => posicionar();

  function sair(): void {
    limparAlvo();
    balao.remove();
    document.removeEventListener('keydown', aoTeclar);
    window.removeEventListener('resize', aoRedimensionar);
    tourAtual = null;
    marcarTourVisto();
    g.anunciar('Tour encerrado.');
    (origem?.isConnected ? origem : document.getElementById('mapa'))?.focus();
  }

  voltar.addEventListener('click', () => { if (i > 0) mostrar(i - 1); });
  proximo.addEventListener('click', () => { if (i < passos.length - 1) mostrar(i + 1); else sair(); });
  sairBtn.addEventListener('click', sair);
  document.addEventListener('keydown', aoTeclar);
  window.addEventListener('resize', aoRedimensionar);
  document.body.append(balao);
  tourAtual = { sair };
  mostrar(0);
  return sair;
}
