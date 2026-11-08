import './estilos.css';
import { carregarBase, Entidades, ErroCarga } from './data/carregador';
import type { DadosBase } from './data/tipos';
import { Indice, chaveDe, caminhoDe, montarCena, recolher, revelarCaminho, SEP, TIPOS_FOLHA, type EstadoExpansao, type Visao, type Cena } from './model/adaptador';
import { IndiceBusca } from './model/busca';
import { filtrosAtivos, filtrosVazios, motivoOculto } from './model/filtros';
import { Cores, misturar } from './cores';
import { Mapa, type ArestaClicada, type NoVisual } from './graph/mapa';
import { iconeSvg, siglaFuncionalidade } from './graph/icones';
import { renderizarAresta, renderizarNo, renderizarRelacaoPorId, type CtxPainel } from './ui/painel';
import { renderizarLista } from './ui/lista';
import { conteudoFiltros, conteudoLegenda, conteudoMetodo, ligarBusca } from './ui/extras';
import { anunciar, h, limpar } from './ui/dom';
import { lerURL, montarURL, type EstadoURL } from './rotas';
import { ICONE_TIPO, NOME_TIPO } from './rotulos';

type Selecao = { tipo: 'no'; caminho: string[] } | { tipo: 'aresta'; a: ArestaClicada } | { tipo: 'rel'; relId: string } | null;

const novoExp = (): EstadoExpansao => ({ expandidos: new Set(['salesforce']), paginas: new Map(), fixados: new Set() });
const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T;

async function iniciar(): Promise<void> {
  const url = lerURL();
  let dados: DadosBase;
  try {
    dados = await carregarBase();
  } catch (e) {
    mostrarErro(e);
    return;
  }
  const ind = new Indice(dados);
  const indBusca = new IndiceBusca(dados.busca);
  const entidades = new Entidades();
  const sf = (await entidades.obter('salesforce').catch(() => null)) as Record<string, unknown> | null;
  const ordemCls = (sf?.classificacoes as string[] | undefined) ?? [...ind.nos.values()].filter((n) => n.tipo === 'classificacao').map((n) => n.id);
  const ordemNuv = (sf?.nuvens as string[] | undefined) ?? [...ind.nos.values()].filter((n) => n.tipo === 'nuvem').map((n) => n.id);
  const cores = new Cores(ordemCls, ordemNuv);
  const reduzir = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const st = {
    visao: url.visao as Visao,
    modo: url.modo,
    exp: { funcionalidade: novoExp(), nuvem: novoExp() } as Record<Visao, EstadoExpansao>,
    sel: null as Selecao,
    filtros: filtrosVazios(),
    reduzir,
    cena: null as Cena | null,
    sintetico: url.sintetico || dados.build.sintetico === true,
  };
  const exp = () => st.exp[st.visao];

  const rotulo = (id: string): string => {
    const n = ind.no(id);
    if (!n) return id;
    return n.rotulo;
  };
  const oculto = (id: string) => (filtrosAtivos(st.filtros) ? motivoOculto(ind, id, st.filtros, rotulo) : null);

  // ------------------------------------------------------------ cabeçalho e estrutura
  if (st.sintetico) $('faixa-sintetica').hidden = false;
  $('versao').textContent = `API ${String((dados.manifesto.versao_base as Record<string, string>).api_version ?? '?')} · contrato ${dados.manifesto.contrato.versao}${dados.build.commit ? ` · insumos ${dados.build.commit}` : ''}`;

  const painel = $('conteudo-painel');
  const aside = $('painel');
  const containerMapa = $('mapa');
  const containerLista = $('lista');

  const mapa = new Mapa(containerMapa, {
    selecionarNo: (chave) => selecionarCaminho(caminhoDe(chave)),
    selecionarAresta: (a) => selecionarAresta(a),
    alternarNo: (chave) => alternar(caminhoDe(chave)),
    paginar: (chave) => paginar(chave),
    limparSelecao: () => { mapa.destacar(null); },
  }, { reduzirMovimento: st.reduzir });

  // ------------------------------------------------------------ cores e ícones por ocorrência
  const corDe = (cam: string[], tipo: string): string => {
    if (tipo === 'salesforce') return '#e0f2fe';
    const base = st.visao === 'funcionalidade' ? cores.classificacao(cam[1]) : cores.nuvem(cam[1]);
    switch (tipo) {
      case 'nuvem':
      case 'classificacao': return base;
      case 'subclassificacao': {
        const pai = ind.no(cam[cam.length - 2]);
        const irmaos = ind.filhos(st.visao, cam.slice(0, -1)).map((f) => f.id);
        return st.visao === 'funcionalidade' || pai?.tipo === 'classificacao' ? cores.tom(base, Math.max(0, irmaos.indexOf(cam[cam.length - 1]))) : base;
      }
      case 'funcionalidade': return misturar(base, '#000000', 0.08);
      case 'metadata_type':
      case 'objeto_api':
      case 'objeto_api_juncao': return misturar(base, '#ffffff', 0.55);
      case 'estrutura_auxiliar': return misturar(base, '#ffffff', 0.68);
      default: return misturar(base, '#ffffff', 0.8);
    }
  };
  const iconeDe = (id: string, tipo: string, cor: string): string => {
    const n = ind.no(id)!;
    if (tipo === 'salesforce') return iconeSvg('Salesforce', cor, { placeholder: true });
    if (tipo === 'nuvem' || tipo === 'classificacao' || tipo === 'subclassificacao') return iconeSvg(n.sigla ?? n.rotulo.slice(0, 3), cor);
    if (tipo === 'funcionalidade') return iconeSvg(siglaFuncionalidade(n.rotulo), cor);
    return iconeSvg(ICONE_TIPO[tipo as keyof typeof ICONE_TIPO] || '•', cor);
  };

  // ------------------------------------------------------------ atualização da cena
  let ocultosNaCena = 0;
  function atualizar(): void {
    const cena = montarCena(ind, st.visao, exp());
    st.cena = cena;
    const vis = new Map<string, NoVisual>();
    ocultosNaCena = 0;
    for (const o of cena.ocorrencias) {
      const n = ind.no(o.id)!;
      const cor = corDe(o.caminho, n.tipo);
      const oc = oculto(o.id);
      if (oc) ocultosNaCena++;
      vis.set(o.chave, {
        chave: o.chave, rotulo: n.tipo === 'salesforce' ? 'Salesforce' : n.rotulo, tipo: n.tipo, icone: iconeDe(o.id, n.tipo, cor), cor,
        oculto: !!oc, totalFilhos: o.totalFilhos, expandido: exp().expandidos.has(o.chave), acessivel: `${NOME_TIPO[n.tipo]}: ${n.rotulo}`,
      });
    }
    const pags = new Map(cena.paginacoes.map((p) => [p.chave, `+${p.restantes} mais`]));
    if (st.modo === 'mapa') mapa.desenhar(cena, vis, pags);
    else renderizarLista(containerLista, cena, ctxLista, st.sel?.tipo === 'no' ? chaveDe(st.sel.caminho) : null);
    destacarSelecao();
    $('status').textContent = `${cena.ocorrencias.length} itens visíveis de ${ind.nos.size} no catálogo${ocultosNaCena ? ` · ${ocultosNaCena} esmaecidos por filtros` : ''}`;
    $('btn-filtros').textContent = filtrosAtivos(st.filtros) ? `Filtros (${filtrosAtivos(st.filtros)})` : 'Filtros';
  }

  function destacarSelecao(): void {
    if (st.modo !== 'mapa') return;
    if (st.sel?.tipo === 'no') mapa.destacar(chaveDe(st.sel.caminho));
    else if (st.sel?.tipo === 'aresta') mapa.destacar(null, st.sel.a.id);
    else mapa.destacar(null);
  }

  // ------------------------------------------------------------ navegação
  function estadoURLAtual(): EstadoURL {
    const s = st.sel;
    return {
      visao: st.visao, modo: st.modo, sintetico: url.sintetico,
      id: s?.tipo === 'no' ? s.caminho[s.caminho.length - 1] : undefined,
      caminho: s?.tipo === 'no' ? s.caminho : undefined,
      rel: s?.tipo === 'rel' ? s.relId : s?.tipo === 'aresta' ? s.a.relId : undefined,
    };
  }
  function gravarURL(push: boolean): void {
    const u = montarURL(estadoURLAtual());
    if (u === location.search || (u === '?' && !location.search)) return;
    if (push) history.pushState(null, '', u);
    else history.replaceState(null, '', u);
  }

  function selecionarCaminho(caminho: string[], o: { push?: boolean; focar?: boolean; gaveta?: boolean } = {}): void {
    const { push = true, focar = true, gaveta = true } = o;
    revelarCaminho(ind, st.visao, exp(), caminho);
    st.sel = { tipo: 'no', caminho };
    atualizar();
    if (gaveta) abrirPainel();
    void renderizarNo(ctxPainel, painel, caminho);
    if (focar && st.modo === 'mapa') mapa.focar(chaveDe(caminho));
    gravarURL(push);
    const n = ind.no(caminho[caminho.length - 1]);
    if (n) anunciar(`${NOME_TIPO[n.tipo]} selecionado: ${n.rotulo}`);
  }

  function abrirId(id: string, contexto?: readonly string[], o: { push?: boolean } = {}): void {
    const ctx = contexto ?? (st.sel?.tipo === 'no' ? st.sel.caminho : undefined);
    let cam = ind.caminhoPreferido(id, st.visao, ctx);
    if (!cam) {
      const outra: Visao = st.visao === 'funcionalidade' ? 'nuvem' : 'funcionalidade';
      const alt = ind.caminhoPreferido(id, outra);
      if (alt) {
        trocarVisao(outra, false);
        anunciar(`Este item só aparece na visão por ${outra === 'nuvem' ? 'nuvem' : 'funcionalidade'}; a visão foi trocada.`);
        cam = alt;
      }
    }
    if (!cam) {
      anunciar('Item sem caminho no mapa.');
      return;
    }
    selecionarCaminho(cam, o);
  }

  function selecionarAresta(a: ArestaClicada): void {
    st.sel = { tipo: 'aresta', a };
    destacarSelecao();
    abrirPainel();
    void renderizarAresta(ctxPainel, painel, a);
    gravarURL(true);
  }

  function alternar(caminho: readonly string[]): void {
    const chave = chaveDe(caminho);
    const e = exp();
    if (e.expandidos.has(chave)) {
      recolher(e, chave);
      // não perde a seleção: se estava dentro do ramo recolhido, passa para o nó recolhido
      if (st.sel?.tipo === 'no' && chaveDe(st.sel.caminho).startsWith(chave + SEP)) st.sel = { tipo: 'no', caminho: [...caminho] };
    } else {
      e.expandidos.add(chave);
    }
    atualizar();
    if (st.sel?.tipo === 'no') void renderizarNo(ctxPainel, painel, st.sel.caminho);
    const n = ind.no(caminho[caminho.length - 1]);
    if (n) anunciar(`${n.rotulo} ${e.expandidos.has(chave) ? 'expandido' : 'recolhido'}`);
  }

  function paginar(chaveMais: string): void {
    const pai = chaveMais.replace(new RegExp(`${SEP}#mais$`), '');
    exp().paginas.set(pai, (exp().paginas.get(pai) ?? 1) + 1);
    atualizar();
  }

  function trocarVisao(v: Visao, manterSelecao = true): void {
    if (st.visao === v) return;
    const idSel = st.sel?.tipo === 'no' ? st.sel.caminho[st.sel.caminho.length - 1] : null;
    st.visao = v;
    marcarSegmentos();
    atualizar();
    if (manterSelecao && idSel) {
      const cam = ind.caminhoPreferido(idSel, v);
      if (cam) selecionarCaminho(cam);
      else { st.sel = null; selecionarCaminho(['salesforce']); anunciar('O item selecionado não existe nesta visão; mostrando o centro.'); }
    }
    mapa.enquadrar();
  }

  function trocarModo(m: 'mapa' | 'lista'): void {
    st.modo = m;
    containerMapa.hidden = m !== 'mapa';
    for (const b of document.querySelectorAll<HTMLElement>('.so-mapa')) b.hidden = m !== 'mapa';
    containerLista.hidden = m !== 'lista';
    marcarSegmentos();
    atualizar();
    if (m === 'mapa') { mapa.redimensionar(); if (st.sel?.tipo === 'no') mapa.focar(chaveDe(st.sel.caminho)); }
    gravarURL(false);
  }

  function marcarSegmentos(): void {
    for (const b of document.querySelectorAll<HTMLButtonElement>('[data-visao]')) b.setAttribute('aria-pressed', String(b.dataset.visao === st.visao));
    for (const b of document.querySelectorAll<HTMLButtonElement>('[data-modo]')) b.setAttribute('aria-pressed', String(b.dataset.modo === st.modo));
  }

  // ------------------------------------------------------------ painel (gaveta no celular)
  function abrirPainel(): void {
    aside.classList.add('aberto');
  }
  function fecharPainel(): void {
    aside.classList.remove('aberto');
    (st.modo === 'mapa' ? containerMapa : (containerLista.querySelector('[tabindex="0"]') as HTMLElement) ?? containerLista).focus();
  }
  $('fechar-painel').addEventListener('click', fecharPainel);

  const ctxPainel: CtxPainel = {
    ind, entidades, fontes: dados.fontes, manifesto: dados.manifesto, build: dados.build, cobertura: dados.cobertura,
    visao: () => st.visao,
    rotulo,
    abrir: (id, contexto) => abrirId(id, contexto),
    abrirCaminho: (c) => selecionarCaminho([...c]),
    alternar: (c) => alternar(c),
    expandido: (c) => exp().expandidos.has(chaveDe(c)),
    focarNoMapa: (c) => { if (st.modo !== 'mapa') trocarModo('mapa'); revelarCaminho(ind, st.visao, exp(), c); atualizar(); mapa.focar(chaveDe(c), 1); if (matchMedia('(max-width: 760px)').matches) fecharPainel(); },
    link: (id, c) => montarURL({ visao: st.visao, modo: 'mapa', id, caminho: c ? [...c] : undefined, sintetico: url.sintetico }),
    abrirMetodo: () => abrirDialogo('metodo'),
    abrirRelacao: (relId) => { st.sel = { tipo: 'rel', relId }; abrirPainel(); void renderizarRelacaoPorId(ctxPainel, painel, relId); gravarURL(true); },
    motivoOculto: oculto,
  };

  const ctxLista = {
    rotulo,
    tipo: (id: string) => (ind.no(id)?.tipo ?? 'funcionalidade') as keyof typeof NOME_TIPO,
    oculto,
    expandido: (chave: string) => exp().expandidos.has(chave),
    selecionar: (chave: string) => selecionarCaminho(caminhoDe(chave), { focar: false }),
    alternar: (chave: string) => alternar(caminhoDe(chave)),
    paginar,
  };

  // ------------------------------------------------------------ diálogos: método, legenda, filtros
  function abrirDialogo(qual: 'metodo' | 'legenda' | 'filtros'): void {
    const d = $<HTMLDialogElement>('dialogo');
    const corpo = $('dialogo-corpo');
    limpar(corpo);
    $('dialogo-titulo').textContent = qual === 'metodo' ? 'Método' : qual === 'legenda' ? 'Legenda' : 'Filtros';
    if (qual === 'metodo') corpo.append(conteudoMetodo(dados, sf));
    if (qual === 'legenda') corpo.append(conteudoLegenda(cores, st.visao, rotulo));
    if (qual === 'filtros') {
      const render = () => { atualizar(); limpar(corpo); corpo.append(conteudoFiltros(ind, st.filtros, rotulo, render, ocultosNaCena)); };
      corpo.append(conteudoFiltros(ind, st.filtros, rotulo, render, ocultosNaCena));
    }
    d.showModal();
  }
  $('fechar-dialogo').addEventListener('click', () => $<HTMLDialogElement>('dialogo').close());
  $('btn-metodo').addEventListener('click', () => abrirDialogo('metodo'));
  $('btn-legenda').addEventListener('click', () => abrirDialogo('legenda'));
  $('btn-filtros').addEventListener('click', () => abrirDialogo('filtros'));

  // ------------------------------------------------------------ ferramentas do mapa e teclado
  $('btn-zoom-mais').addEventListener('click', () => mapa.zoom(1.25));
  $('btn-zoom-menos').addEventListener('click', () => mapa.zoom(0.8));
  $('btn-enquadrar').addEventListener('click', () => mapa.enquadrar());
  $('btn-centro').addEventListener('click', () => selecionarCaminho(['salesforce']));
  $('btn-caminho').addEventListener('click', () => {
    if (st.sel?.tipo === 'no') { destacarSelecao(); mapa.focar(chaveDe(st.sel.caminho), 1); anunciar('De volta ao caminho selecionado.'); }
  });
  const btnAnim = $('btn-animacao');
  const marcarAnim = () => { btnAnim.setAttribute('aria-pressed', String(st.reduzir)); btnAnim.textContent = st.reduzir ? 'Animações: desligadas' : 'Animações: ligadas'; };
  marcarAnim();
  btnAnim.addEventListener('click', () => { st.reduzir = !st.reduzir; mapa.setReduzirMovimento(st.reduzir); marcarAnim(); });
  $('btn-leitura').addEventListener('click', () => {
    const on = document.body.classList.toggle('modo-leitura');
    $('btn-leitura').setAttribute('aria-pressed', String(on));
    if (!on) mapa.redimensionar();
    ($('titulo-painel') ?? painel).focus();
  });
  for (const b of document.querySelectorAll<HTMLButtonElement>('[data-visao]')) b.addEventListener('click', () => trocarVisao(b.dataset.visao as Visao));
  for (const b of document.querySelectorAll<HTMLButtonElement>('[data-modo]')) b.addEventListener('click', () => trocarModo(b.dataset.modo as 'mapa' | 'lista'));

  containerMapa.addEventListener('keydown', (ev) => {
    const sel = st.sel?.tipo === 'no' ? st.sel.caminho : ['salesforce'];
    const cena = st.cena!;
    const chave = chaveDe(sel);
    const occ = cena.ocorrencias.find((x) => x.chave === chave);
    const irmaos = occ?.paiChave ? cena.ocorrencias.filter((x) => x.paiChave === occ.paiChave) : [];
    const i = irmaos.findIndex((x) => x.chave === chave);
    switch (ev.key) {
      case '+': case '=': mapa.zoom(1.25); break;
      case '-': mapa.zoom(0.8); break;
      case '0': mapa.enquadrar(); break;
      case 'c': case 'C': selecionarCaminho(['salesforce']); break;
      case 'Enter': case ' ': alternar(sel); break;
      case 'ArrowUp': if (sel.length > 1) selecionarCaminho(sel.slice(0, -1)); break;
      case 'ArrowDown': {
        const f = ind.filhos(st.visao, sel)[0];
        if (f) selecionarCaminho([...sel, f.id]);
        break;
      }
      case 'ArrowRight': if (irmaos.length) selecionarCaminho(irmaos[(i + 1) % irmaos.length].caminho); break;
      case 'ArrowLeft': if (irmaos.length) selecionarCaminho(irmaos[(i - 1 + irmaos.length) % irmaos.length].caminho); break;
      default: return;
    }
    ev.preventDefault();
  });

  // ------------------------------------------------------------ busca
  ligarBusca($<HTMLInputElement>('busca'), $('resultados'), { indice: indBusca, ind, rotulo, oculto, abrir: (id) => abrirId(id, undefined) });

  // ------------------------------------------------------------ URL e histórico
  function aplicarURL(u: EstadoURL, push: boolean): void {
    if (u.visao !== st.visao) { st.visao = u.visao; }
    if (u.modo !== st.modo) trocarModo(u.modo);
    marcarSegmentos();
    if (u.rel && !u.id) {
      atualizar();
      st.sel = { tipo: 'rel', relId: u.rel };
      abrirPainel();
      void renderizarRelacaoPorId(ctxPainel, painel, u.rel).catch(() => painel.append(h('p', { class: 'erro' }, `Relação ${u.rel} não encontrada.`)));
      return;
    }
    if (u.id && ind.no(u.id)) {
      const cam = u.caminho && u.caminho[u.caminho.length - 1] === u.id && ind.caminhoValido(u.caminho, st.visao) ? u.caminho : null;
      if (cam) selecionarCaminho(cam, { push });
      else abrirId(u.id, undefined, { push });
      return;
    }
    if (u.id) anunciar(`Item ${u.id} não existe nesta versão dos dados.`);
    selecionarCaminho(['salesforce'], { push, focar: false, gaveta: false });
  }
  window.addEventListener('popstate', () => aplicarURL(lerURL(), false));
  const topo = document.querySelector<HTMLElement>('.topo')!;
  const medirTopo = () => document.documentElement.style.setProperty('--topo', `${topo.getBoundingClientRect().bottom}px`);
  new ResizeObserver(medirTopo).observe(topo);
  window.addEventListener('resize', () => { medirTopo(); mapa.redimensionar(); });

  $('carregando').hidden = true;
  $('app').hidden = false;
  trocarModo(st.modo);
  aplicarURL(url, false);
  mapa.redimensionar();
  mapa.enquadrar(false);
  // ganchos de teste e medição (somente leitura)
  (window as unknown as Record<string, unknown>).__sfTutor = {
    nosRenderizados: () => mapa.quantidadeNos(),
    ponto: (alvo: { no?: string; relId?: string }) => mapa.pontoNaPagina(alvo),
    chaveDe: (id: string) => st.cena?.ocorrencias.find((o) => o.id === id)?.chave ?? null,
    selecao: () => (st.sel?.tipo === 'no' ? st.sel.caminho.join(SEP) : null),
    visao: () => st.visao,
    totalCatalogo: ind.nos.size,
    pronto: true,
    folha: (id: string) => TIPOS_FOLHA.has(ind.no(id)?.tipo as never),
  };
}

function mostrarErro(e: unknown): void {
  const c = $('carregando');
  c.hidden = false;
  limpar(c);
  const arquivo = e instanceof ErroCarga ? e.arquivo : 'dados';
  c.append(
    h('h1', null, 'Não foi possível carregar os dados do tutorial'),
    h('p', { role: 'alert' }, String((e as Error)?.message ?? e)),
    h('p', null, `Arquivo: ${arquivo}. Os dados são gerados a partir de ai-help/claude/insumos-grafo/ com "npm run dados" (que valida a base antes de copiar).`),
    h('button', { type: 'button', class: 'btn', on: { click: () => location.reload() } }, 'Tentar de novo'),
  );
}

void iniciar();
