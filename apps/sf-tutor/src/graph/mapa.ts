// Desenho do grafo com Cytoscape.js. Recebe a cena já calculada pelo adaptador; não conhece conteúdo técnico.
import cytoscape from 'cytoscape';
import type { Core, EventObject, NodeSingular, ElementDefinition } from 'cytoscape';
import type { Cena } from '../model/adaptador';
import { LIGACAO } from '../rotulos';
import { posicionar, type Ponto } from './layout';

export interface NoVisual {
  chave: string;
  rotulo: string;
  tipo: string;
  icone: string;
  cor: string;
  oculto: boolean;
  totalFilhos: number;
  expandido: boolean;
  acessivel: string; // nome acessível (anunciado ao selecionar)
}

export interface ArestaClicada {
  id: string;
  ligacao: string;
  origem: string;
  destino: string;
  tecnica: boolean;
  relId?: string;
  estado?: string;
  natureza?: string;
  papel?: string;
  motivo?: string;
}

export interface Eventos {
  selecionarNo(chave: string): void;
  selecionarAresta(a: ArestaClicada): void;
  alternarNo(chave: string): void;
  paginar(chave: string): void;
  limparSelecao(): void;
}

const TAMANHO: Record<string, number> = {
  salesforce: 92, nuvem: 64, classificacao: 58, subclassificacao: 46, funcionalidade: 50,
  metadata_type: 44, objeto_api: 44, objeto_api_juncao: 44, estrutura_auxiliar: 34, propriedade_xml: 24, campo_api: 24, pagina: 34,
};

export class Mapa {
  readonly cy: Core;
  private posicoes = new Map<string, Ponto>();
  private animar: boolean;
  private primeira = true;

  constructor(container: HTMLElement, private ev: Eventos, opts: { reduzirMovimento: boolean }) {
    this.animar = !opts.reduzirMovimento;
    this.cy = cytoscape({
      container,
      elements: [],
      minZoom: 0.08,
      maxZoom: 3,
      boxSelectionEnabled: false,
      autoungrabify: false,
      style: estilo() as never,
      layout: { name: 'preset' },
    });
    this.cy.on('tap', 'node', (e: EventObject) => {
      const n = e.target as NodeSingular;
      if (n.data('tipo') === 'pagina') this.ev.paginar(n.id());
      else this.ev.selecionarNo(n.id());
    });
    this.cy.on('dbltap', 'node', (e: EventObject) => {
      const n = e.target as NodeSingular;
      if (n.data('tipo') !== 'pagina') this.ev.alternarNo(n.id());
    });
    this.cy.on('tap', 'edge', (e: EventObject) => {
      const d = e.target.data();
      this.ev.selecionarAresta({ id: d.id, ligacao: d.ligacao, origem: d.source, destino: d.target, tecnica: d.tecnica, relId: d.relId, estado: d.estado, natureza: d.natureza, papel: d.papel, motivo: d.motivo });
    });
    this.cy.on('tap', (e: EventObject) => {
      if (e.target === this.cy) this.ev.limparSelecao();
    });
    this.cy.on('dragfree', 'node', (e: EventObject) => {
      const n = e.target as NodeSingular;
      this.posicoes.set(n.id(), { ...n.position() });
    });
  }

  setReduzirMovimento(v: boolean): void {
    this.animar = !v;
  }

  desenhar(cena: Cena, nos: Map<string, NoVisual>, paginas: Map<string, string>): void {
    const pos = posicionar(cena, this.posicoes);
    this.posicoes = pos;
    const queremos = new Set<string>();
    const add: ElementDefinition[] = [];
    for (const o of cena.ocorrencias) {
      const v = nos.get(o.chave)!;
      queremos.add(o.chave);
      const data = {
        id: o.chave, rotulo: v.rotulo, tipo: v.tipo, icone: v.icone, cor: v.cor, oculto: v.oculto ? 1 : 0,
        filhos: v.totalFilhos, expandido: v.expandido ? 1 : 0, tamanho: TAMANHO[v.tipo] ?? 36,
        marca: v.totalFilhos > 0 ? (v.expandido ? '−' : '+') : '',
      };
      const el = this.cy.getElementById(o.chave);
      if (el.nonempty()) el.data(data);
      else add.push({ group: 'nodes', data, position: { ...pos.get(o.chave)! } });
    }
    for (const p of cena.paginacoes) {
      queremos.add(p.chave);
      const data = { id: p.chave, rotulo: paginas.get(p.chave) ?? `+${p.restantes}`, tipo: 'pagina', icone: 'none', cor: '#e2e8f0', tamanho: TAMANHO.pagina, oculto: 0, marca: '' };
      const el = this.cy.getElementById(p.chave);
      if (el.nonempty()) el.data(data);
      else add.push({ group: 'nodes', data, position: { ...pos.get(p.chave)! } });
    }
    for (const a of cena.arestas) {
      queremos.add(a.id);
      if (this.cy.getElementById(a.id).nonempty()) continue;
      const g = LIGACAO[a.ligacao]?.grupo ?? 'hierarquia';
      add.push({
        group: 'edges',
        data: {
          id: a.id, source: a.origem, target: a.destino, ligacao: a.ligacao, tecnica: a.tecnica, grupo: g,
          relId: a.aresta?.rel_id, estado: a.aresta?.estado ?? (a.tecnica ? 'desconhecido' : ''), natureza: a.aresta?.natureza,
          papel: a.aresta?.papel, motivo: a.aresta?.motivo,
        },
      });
    }
    // arestas de paginação
    for (const p of cena.paginacoes) {
      const id = `p|${p.chave}`;
      queremos.add(id);
      if (this.cy.getElementById(id).empty()) add.push({ group: 'edges', data: { id, source: p.paiChave, target: p.chave, ligacao: 'pagina', grupo: 'pagina', tecnica: false } });
    }
    this.cy.batch(() => {
      this.cy.elements().forEach((e) => {
        if (!queremos.has(e.id())) e.remove();
      });
      this.cy.add(add);
      // posições de nós existentes podem ter sido ajustadas pelo usuário (arrastar); mantemos as atuais
    });
    if (this.primeira) {
      this.primeira = false;
      this.enquadrar(false);
    }
  }

  destacar(chave: string | null, arestaId?: string): void {
    const cy = this.cy;
    cy.batch(() => {
      cy.elements().removeClass('foco vizinho esmaecido selecionado');
      if (!chave && !arestaId) return;
      if (arestaId) {
        const e = cy.getElementById(arestaId);
        if (e.empty()) return;
        cy.elements().addClass('esmaecido');
        e.removeClass('esmaecido').addClass('selecionado');
        e.connectedNodes().removeClass('esmaecido').addClass('vizinho');
        return;
      }
      const n = cy.getElementById(chave!);
      if (n.empty()) return;
      cy.elements().addClass('esmaecido');
      const viz = n.closedNeighborhood();
      viz.removeClass('esmaecido').addClass('vizinho');
      // caminho até o centro
      let atual: NodeSingular = n as unknown as NodeSingular;
      for (let i = 0; i < 40; i++) {
        const pai = atual.incomers('edge[!tecnica]').sources();
        if (pai.empty()) break;
        atual.incomers('edge[!tecnica]').removeClass('esmaecido').addClass('vizinho');
        pai.removeClass('esmaecido').addClass('vizinho');
        atual = pai.first();
      }
      n.removeClass('vizinho').addClass('foco selecionado');
    });
  }

  focar(chave: string, zoom?: number): void {
    const n = this.cy.getElementById(chave);
    if (n.empty()) return;
    if (zoom !== undefined) {
      if (this.animar) this.cy.animate({ center: { eles: n }, zoom }, { duration: 300 });
      else { this.cy.zoom(zoom); this.cy.center(n); }
      return;
    }
    // enquadra o nó com seus vizinhos imediatos (pai, filhos visíveis, relações técnicas), sem zoom exagerado
    const eles = n.closedNeighborhood().nodes();
    const bb = eles.boundingBox({ includeLabels: true });
    const pad = 50;
    const zFit = Math.min((this.cy.width() - 2 * pad) / Math.max(bb.w, 1), (this.cy.height() - 2 * pad) / Math.max(bb.h, 1));
    const z = Math.max(0.35, Math.min(1.3, zFit));
    const alvo = eles.length > 1 ? eles : n;
    if (this.animar) this.cy.animate({ center: { eles: alvo }, zoom: z }, { duration: 300 });
    else { this.cy.zoom(z); this.cy.center(alvo); }
  }

  enquadrar(animar = this.animar): void {
    if (animar) this.cy.animate({ fit: { eles: this.cy.elements(), padding: 40 } }, { duration: 300 });
    else this.cy.fit(this.cy.elements(), 40);
  }

  zoom(fator: number): void {
    const z = this.cy.zoom() * fator;
    const c = { x: this.cy.width() / 2, y: this.cy.height() / 2 };
    if (this.animar) this.cy.animate({ zoom: { level: z, renderedPosition: c } }, { duration: 150 });
    else this.cy.zoom({ level: z, renderedPosition: c });
  }

  /** Ponto (coordenadas da página) de um nó ou de uma aresta técnica; usado pelos testes para clicar como o usuário. */
  pontoNaPagina(alvo: { no?: string; relId?: string }): { x: number; y: number } | null {
    const r = this.cy.container()!.getBoundingClientRect();
    if (alvo.no) {
      const n = this.cy.getElementById(alvo.no);
      if (n.empty()) return null;
      const p = n.renderedPosition();
      return { x: r.left + p.x, y: r.top + p.y };
    }
    const es = this.cy.edges().filter((x) => x.data('relId') === alvo.relId);
    if (es.empty()) return null;
    const e = es[0];
    // ponto visível da aresta: percorre a curva (bezier quadrática por S, M, T) e evita pontos cobertos por nós/rótulos
    const S = e.renderedSourceEndpoint();
    const T = e.renderedTargetEndpoint();
    const M = e.renderedMidpoint();
    const C = { x: 2 * M.x - (S.x + T.x) / 2, y: 2 * M.y - (S.y + T.y) / 2 };
    const caixas = this.cy.nodes().map((n) => n.renderedBoundingBox({ includeLabels: true }));
    for (const t of [0.5, 0.4, 0.6, 0.3, 0.7, 0.25, 0.75, 0.2, 0.8]) {
      const x = (1 - t) ** 2 * S.x + 2 * (1 - t) * t * C.x + t ** 2 * T.x;
      const y = (1 - t) ** 2 * S.y + 2 * (1 - t) * t * C.y + t ** 2 * T.y;
      const coberto = caixas.some((b) => x >= b.x1 - 2 && x <= b.x2 + 2 && y >= b.y1 - 2 && y <= b.y2 + 2);
      const dentro = x > 0 && y > 0 && x < this.cy.width() && y < this.cy.height();
      if (!coberto && dentro) return { x: r.left + x, y: r.top + y };
    }
    return null;
  }

  quantidadeNos(): number {
    return this.cy.nodes().length;
  }

  redimensionar(): void {
    this.cy.resize();
  }
}

function estilo(): unknown[] {
  return [
    {
      selector: 'node',
      style: {
        width: 'data(tamanho)', height: 'data(tamanho)', shape: 'ellipse',
        'background-color': 'data(cor)', 'background-image': 'data(icone)', 'background-fit': 'cover', 'background-clip': 'node',
        'border-width': 2, 'border-color': '#0f172a', 'border-opacity': 0.55,
        label: 'data(rotulo)', 'text-valign': 'bottom', 'text-halign': 'center', 'text-margin-y': 5,
        'font-family': 'system-ui, -apple-system, Segoe UI, sans-serif', 'font-size': 11, color: '#0f172a',
        'text-wrap': 'wrap', 'text-max-width': '130px', 'text-overflow-wrap': 'whitespace', 'text-background-color': '#ffffff', 'text-background-opacity': 0.85,
        'text-background-padding': '2px', 'text-background-shape': 'roundrectangle', 'min-zoomed-font-size': 7,
      },
    },
    { selector: 'node[tipo = "salesforce"]', style: { 'border-width': 3, 'border-style': 'dashed', 'border-color': '#0369a1', 'font-size': 14, 'font-weight': 700 } },
    { selector: 'node[tipo = "nuvem"]', style: { 'border-width': 4, 'border-style': 'double', 'font-size': 13, 'font-weight': 700 } },
    { selector: 'node[tipo = "classificacao"]', style: { 'border-width': 4, 'border-style': 'double', 'font-size': 12, 'font-weight': 600 } },
    { selector: 'node[tipo = "subclassificacao"]', style: { 'border-width': 3 } },
    { selector: 'node[tipo = "funcionalidade"]', style: { 'border-width': 3, 'border-color': '#0f172a', 'border-opacity': 0.9, 'font-weight': 600 } },
    { selector: 'node[tipo = "metadata_type"]', style: { 'border-width': 3, 'border-style': 'dashed', 'border-color': '#7c2d12' } },
    { selector: 'node[tipo = "estrutura_auxiliar"]', style: { 'border-width': 2, 'border-style': 'dashed', 'border-color': '#7c2d12' } },
    { selector: 'node[tipo = "objeto_api"]', style: { 'border-width': 3, 'border-color': '#1e3a8a' } },
    { selector: 'node[tipo = "objeto_api_juncao"]', style: { 'border-width': 5, 'border-style': 'double', 'border-color': '#1e3a8a' } },
    { selector: 'node[tipo = "campo_api"], node[tipo = "propriedade_xml"]', style: { 'font-size': 9, 'text-max-width': '90px', 'border-width': 1 } },
    { selector: 'node[tipo = "pagina"]', style: { 'background-image': 'none', shape: 'round-rectangle', width: 64, height: 26, label: 'data(rotulo)', 'text-valign': 'center', 'text-margin-y': 0, 'background-color': '#e2e8f0', 'border-style': 'dashed', 'font-size': 10, 'text-background-opacity': 0 } },
    { selector: 'node[filhos > 0][expandido = 0]', style: { 'border-color': '#0f172a', 'border-opacity': 1 } },
    { selector: 'node[oculto = 1]', style: { opacity: 0.22, 'border-style': 'dotted' } },
    { selector: 'node.foco', style: { 'border-width': 5, 'border-color': '#f59e0b', 'border-opacity': 1, 'z-index': 20 } },
    { selector: 'node.esmaecido', style: { opacity: 0.18 } },
    { selector: 'node.vizinho', style: { opacity: 1 } },
    {
      selector: 'edge',
      style: { width: 1.2, 'line-color': '#94a3b8', 'curve-style': 'bezier', 'target-arrow-shape': 'none', opacity: 0.85 },
    },
    { selector: 'edge[grupo = "hierarquia"]', style: { width: 1.4, 'line-color': '#94a3b8' } },
    { selector: 'edge[ligacao = "classificacao_secundaria"]', style: { 'line-style': 'dashed', 'line-dash-pattern': [2, 4] } },
    { selector: 'edge[grupo = "representacao"]', style: { width: 2.4, 'line-color': '#0f766e', 'target-arrow-shape': 'triangle', 'target-arrow-color': '#0f766e' } },
    { selector: 'edge[grupo = "estrutura"]', style: { width: 0.9, 'line-color': '#cbd5e1' } },
    { selector: 'edge[ligacao = "tipo_composto"]', style: { width: 1.4, 'line-color': '#a16207', 'target-arrow-shape': 'diamond', 'target-arrow-color': '#a16207' } },
    { selector: 'edge[grupo = "referencia"]', style: { width: 2.2, 'line-color': '#2563eb', 'target-arrow-shape': 'vee', 'target-arrow-color': '#2563eb', 'curve-style': 'unbundled-bezier', 'control-point-distances': [40], 'control-point-weights': [0.5] } },
    { selector: 'edge[grupo = "correspondencia"]', style: { width: 2.2, 'line-color': '#9333ea', 'target-arrow-shape': 'tee', 'source-arrow-shape': 'tee', 'target-arrow-color': '#9333ea', 'source-arrow-color': '#9333ea', 'curve-style': 'unbundled-bezier', 'control-point-distances': [-40], 'control-point-weights': [0.5] } },
    // nível de evidência das relações técnicas pelo traço
    { selector: 'edge[?tecnica][estado = "desconhecido"]', style: { 'line-style': 'dashed' } },
    { selector: 'edge[?tecnica][estado = "nao_exposto"], edge[?tecnica][estado = "bloqueado"], edge[?tecnica][estado = "nao_aplicavel"]', style: { 'line-style': 'dotted' } },
    { selector: 'edge[grupo = "pagina"]', style: { 'line-style': 'dotted', 'line-color': '#94a3b8' } },
    { selector: 'edge.esmaecido', style: { opacity: 0.08 } },
    { selector: 'edge.vizinho', style: { opacity: 1 } },
    { selector: 'edge.selecionado', style: { width: 4, 'line-color': '#f59e0b', 'target-arrow-color': '#f59e0b', 'source-arrow-color': '#f59e0b', opacity: 1, 'z-index': 30 } },
  ];
}
