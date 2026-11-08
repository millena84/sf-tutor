// Adaptador entre a projeção dos insumos (gerado/site) e a representação visual.
// Funções puras: nenhuma depende do DOM nem do Cytoscape, e nenhum conteúdo técnico vive aqui.
//
// Conceitos:
// - id canônico: identidade do item no catálogo (ex.: "obj:User", "obj:User.ProfileId").
// - caminho: sequência de ids canônicos do centro até o item, na visão atual.
// - ocorrência: um item desenhado num caminho. A chave da ocorrência é o caminho; o mesmo id
//   canônico pode ter várias ocorrências (ex.: Permission sets por Sales e por Service), sempre
//   com o mesmo conteúdo.

import type { Aresta, ArvoreVisao, DadosBase, ItemBusca, NoBase, TipoNo } from '../data/tipos';

export type Visao = 'funcionalidade' | 'nuvem';

export const SEP = '>';
export const chaveDe = (caminho: readonly string[]): string => caminho.join(SEP);
export const caminhoDe = (chave: string): string[] => chave.split(SEP);

/** Nó conhecido pelo índice: nós do grafo-base mais folhas (campos/propriedades) vindas da busca. */
export interface NoIndice extends NoBase {
  pai?: string;
  descricao?: string;
  textos?: string[];
}

export interface Filho {
  id: string;
  /** tipo da ligação didática/técnica que leva do pai a este filho */
  ligacao: string;
}

export const TIPOS_FOLHA: ReadonlySet<TipoNo> = new Set(['campo_api', 'propriedade_xml']);
export const TIPOS_OBJETO: ReadonlySet<TipoNo> = new Set(['objeto_api', 'objeto_api_juncao']);

/** Ligações que formam a hierarquia de navegação (o resto é relação técnica entre itens visíveis). */
export const LIGACOES_HIERARQUIA = new Set([
  'navegacao_classificacao', 'navegacao_subclassificacao', 'navegacao_nuvem',
  'nuvem_classificacao', 'nuvem_subclassificacao', 'nuvem_funcionalidade',
  'classificacao_principal', 'classificacao_secundaria',
  'representacao_xml', 'representacao_objeto_api', 'propriedade', 'campo', 'tipo_composto',
]);

/** Relações técnicas desenhadas entre itens visíveis, em qualquer caminho. */
export const LIGACOES_TECNICAS = new Set(['referencia_campo', 'correspondencia_xml_api', 'representacao_comum']);

export class Indice {
  readonly nos = new Map<string, NoIndice>();
  readonly saindo = new Map<string, Aresta[]>();
  readonly entrando = new Map<string, Aresta[]>();
  readonly folhasPorPai = new Map<string, string[]>();
  readonly arestas: Aresta[];
  readonly arvores: Record<Visao, ArvoreVisao>;
  /** caminhos dos níveis superiores (até funcionalidade) por visão */
  private readonly caminhosTopo: Record<Visao, Map<string, string[][]>>;
  readonly nuvensDaFunc = new Map<string, string[]>();
  readonly classificacoesDaFunc = new Map<string, string[]>();
  readonly funcsDoItem = new Map<string, string[]>();

  constructor(d: Pick<DadosBase, 'nos' | 'arestas' | 'visoes' | 'busca'>) {
    for (const n of d.nos) this.nos.set(n.id, { ...n });
    for (const b of d.busca) this.registrarBusca(b);
    this.arestas = d.arestas;
    for (const a of d.arestas) {
      push(this.saindo, a.origem, a);
      push(this.entrando, a.destino, a);
    }
    this.arvores = { funcionalidade: d.visoes.por_funcionalidade, nuvem: d.visoes.por_nuvem };
    this.caminhosTopo = { funcionalidade: new Map(), nuvem: new Map() };
    for (const v of ['funcionalidade', 'nuvem'] as Visao[]) {
      percorrer(this.arvores[v], [], (caminho, no) => {
        const lista = this.caminhosTopo[v].get(no.id) ?? [];
        // ocorrência principal primeiro: é a escolha padrão quando não há contexto
        if (no.ocorrencia === 'principal') lista.unshift(caminho);
        else lista.push(caminho);
        this.caminhosTopo[v].set(no.id, lista);
      });
    }
    for (const a of d.arestas) {
      if (a.tipo === 'nuvem_funcionalidade') push(this.nuvensDaFunc, a.destino, a.origem);
      if (a.tipo === 'classificacao_principal' || a.tipo === 'classificacao_secundaria') {
        const sub = this.nos.get(a.origem);
        if (sub?.grupo_cor) push(this.classificacoesDaFunc, a.destino, sub.grupo_cor);
      }
    }
    // funcionalidades que levam a cada metadata type/objeto (para filtros e contexto)
    for (const a of d.arestas) {
      if (a.tipo === 'representacao_xml' || a.tipo === 'representacao_objeto_api') push(this.funcsDoItem, a.destino, a.origem);
    }
  }

  private registrarBusca(b: ItemBusca): void {
    const ex = this.nos.get(b.id);
    if (ex) {
      ex.textos = b.textos;
      ex.descricao = b.descricao;
      return;
    }
    this.nos.set(b.id, { id: b.id, tipo: b.tipo, rotulo: b.rotulo, pai: b.pai, descricao: b.descricao, textos: b.textos });
    if (b.pai) push(this.folhasPorPai, b.pai, b.id);
  }

  no(id: string): NoIndice | undefined {
    return this.nos.get(id);
  }

  /** Funcionalidades a que um item pertence (direta ou indiretamente). */
  funcionalidadesDe(id: string): string[] {
    const n = this.nos.get(id);
    if (!n) return [];
    if (n.tipo === 'funcionalidade') return [id];
    if (n.tipo === 'metadata_type' || TIPOS_OBJETO.has(n.tipo)) return this.funcsDoItem.get(id) ?? [];
    const out = new Set<string>();
    for (const p of this.paisHierarquicos(id)) for (const f of this.funcionalidadesDe(p)) out.add(f);
    return [...out];
  }

  /** Pais na hierarquia abaixo da funcionalidade (independentes da visão). */
  paisHierarquicos(id: string): string[] {
    const n = this.nos.get(id);
    if (!n) return [];
    if (n.pai) return [n.pai];
    if (n.tipo === 'estrutura_auxiliar') return (this.entrando.get(id) ?? []).filter((a) => a.tipo === 'tipo_composto').map((a) => a.origem);
    if (n.tipo === 'metadata_type' || TIPOS_OBJETO.has(n.tipo)) return this.funcsDoItem.get(id) ?? [];
    return [];
  }

  /** Filhos naturais da ocorrência no fim do caminho, na visão dada. */
  filhos(visao: Visao, caminho: readonly string[]): Filho[] {
    const id = caminho[caminho.length - 1];
    const n = this.nos.get(id);
    if (!n) return [];
    if (n.tipo === 'salesforce' || n.tipo === 'nuvem' || n.tipo === 'classificacao' || n.tipo === 'subclassificacao') {
      const sub = localizar(this.arvores[visao], caminho);
      if (!sub) return [];
      const prof = caminho.length; // 1 = centro
      return (sub.filhos ?? []).map((f) => ({ id: f.id, ligacao: ligacaoTopo(visao, prof, f) }));
    }
    if (n.tipo === 'funcionalidade') {
      const s = this.saindo.get(id) ?? [];
      const xml = s.filter((a) => a.tipo === 'representacao_xml');
      const api = s.filter((a) => a.tipo === 'representacao_objeto_api');
      return [...xml, ...api].map((a) => ({ id: a.destino, ligacao: a.tipo }));
    }
    if (n.tipo === 'metadata_type' || n.tipo === 'estrutura_auxiliar') {
      return (this.folhasPorPai.get(id) ?? []).map((f) => ({ id: f, ligacao: 'propriedade' }));
    }
    if (TIPOS_OBJETO.has(n.tipo)) {
      return (this.folhasPorPai.get(id) ?? []).map((f) => ({ id: f, ligacao: 'campo' }));
    }
    if (n.tipo === 'propriedade_xml') {
      // tipo composto: a propriedade leva à estrutura auxiliar; evita ciclo no mesmo caminho
      return (this.saindo.get(id) ?? [])
        .filter((a) => a.tipo === 'tipo_composto' && !caminho.includes(a.destino))
        .map((a) => ({ id: a.destino, ligacao: 'tipo_composto' }));
    }
    return [];
  }

  quantidadeFilhos(visao: Visao, caminho: readonly string[]): number {
    return this.filhos(visao, caminho).length;
  }

  /** Todos os caminhos do centro até o id, na visão (limitado para evitar explosão combinatória). */
  caminhosPara(id: string, visao: Visao, limite = 40): string[][] {
    const topo = this.caminhosTopo[visao].get(id);
    if (topo) return topo.slice(0, limite).map((c) => [...c]);
    if (id === this.arvores[visao].id) return [[id]];
    const out: string[][] = [];
    const visitando = new Set<string>();
    const rec = (alvo: string, sufixo: string[]): void => {
      if (out.length >= limite || visitando.has(alvo)) return;
      const t = this.caminhosTopo[visao].get(alvo);
      if (t) {
        for (const c of t) {
          if (out.length >= limite) return;
          out.push([...c, ...sufixo]);
        }
        return;
      }
      visitando.add(alvo);
      for (const p of this.paisHierarquicos(alvo)) rec(p, [alvo, ...sufixo]);
      visitando.delete(alvo);
    };
    for (const p of this.paisHierarquicos(id)) rec(p, [id]);
    return out;
  }

  /**
   * Caminho preferido: mantém o contexto atual quando possível (mesmo prefixo mais longo),
   * senão usa a ocorrência principal.
   */
  caminhoPreferido(id: string, visao: Visao, contexto?: readonly string[]): string[] | null {
    const todos = this.caminhosPara(id, visao);
    if (!todos.length) return null;
    if (!contexto?.length) return todos[0];
    let melhor = todos[0];
    let melhorPrefixo = -1;
    for (const c of todos) {
      let k = 0;
      while (k < c.length && k < contexto.length && c[k] === contexto[k]) k++;
      if (k > melhorPrefixo) {
        melhor = c;
        melhorPrefixo = k;
      }
    }
    return melhor;
  }

  /** Um caminho é válido se cada passo é filho do anterior na visão. */
  caminhoValido(caminho: readonly string[], visao: Visao): boolean {
    if (!caminho.length || caminho[0] !== this.arvores[visao].id) return false;
    for (let i = 1; i < caminho.length; i++) {
      if (!this.filhos(visao, caminho.slice(0, i)).some((f) => f.id === caminho[i])) return false;
    }
    return true;
  }

  /** Relações técnicas que tocam um id (para painel e destaque). */
  relacoesTecnicas(id: string): { saindo: Aresta[]; entrando: Aresta[] } {
    const f = (a: Aresta) => LIGACOES_TECNICAS.has(a.tipo);
    return { saindo: (this.saindo.get(id) ?? []).filter(f), entrando: (this.entrando.get(id) ?? []).filter(f) };
  }
}

// ----------------------------------------------------------------- ocorrências visíveis

export interface Ocorrencia {
  chave: string;
  id: string;
  caminho: string[];
  profundidade: number;
  paiChave: string | null;
  ligacao: string | null;
  /** quantos filhos naturais existem (para o controle expandir) */
  totalFilhos: number;
}

export interface Paginacao {
  chave: string;
  paiChave: string;
  restantes: number;
  proximaPagina: number;
}

export interface ArestaVisivel {
  id: string;
  origem: string; // chave da ocorrência
  destino: string;
  ligacao: string;
  tecnica: boolean;
  aresta?: Aresta;
}

export interface EstadoExpansao {
  expandidos: Set<string>;
  /** páginas mostradas por chave (1 = primeira página) */
  paginas: Map<string, number>;
  /** ocorrências fixadas fora das páginas carregadas (ex.: campo aberto pela busca no fim de uma lista longa) */
  fixados?: Set<string>;
}

export const TAMANHO_PAGINA = 24;

export interface Cena {
  ocorrencias: Ocorrencia[];
  paginacoes: Paginacao[];
  arestas: ArestaVisivel[];
}

/** Deriva a cena visível a partir do estado de expansão. Determinística: a mesma entrada gera a mesma cena. */
export function montarCena(ind: Indice, visao: Visao, exp: EstadoExpansao, tamanhoPagina = TAMANHO_PAGINA): Cena {
  const raiz = ind.arvores[visao].id;
  const ocorrencias: Ocorrencia[] = [];
  const paginacoes: Paginacao[] = [];
  const arestas: ArestaVisivel[] = [];
  const visitar = (caminho: string[], paiChave: string | null, ligacao: string | null): void => {
    const chave = chaveDe(caminho);
    const filhos = ind.filhos(visao, caminho);
    const id = caminho[caminho.length - 1];
    ocorrencias.push({ chave, id, caminho, profundidade: caminho.length - 1, paiChave, ligacao, totalFilhos: filhos.length });
    if (paiChave) arestas.push({ id: `h|${paiChave}|${chave}`, origem: paiChave, destino: chave, ligacao: ligacao ?? '', tecnica: false });
    if (!exp.expandidos.has(chave)) return;
    const pags = Math.max(1, exp.paginas.get(chave) ?? 1);
    const limite = Math.min(filhos.length, pags * tamanhoPagina);
    for (const f of filhos.slice(0, limite)) visitar([...caminho, f.id], chave, f.ligacao);
    let fixadosAqui = 0;
    if (limite < filhos.length && exp.fixados?.size) {
      for (const f of filhos.slice(limite)) {
        if (exp.fixados.has(chave + SEP + f.id)) { visitar([...caminho, f.id], chave, f.ligacao); fixadosAqui++; }
      }
    }
    if (limite < filhos.length) {
      paginacoes.push({ chave: `${chave}${SEP}#mais`, paiChave: chave, restantes: filhos.length - limite - fixadosAqui, proximaPagina: pags + 1 });
    }
  };
  visitar([raiz], null, null);
  // relações técnicas entre ocorrências visíveis (por id canônico)
  const porId = new Map<string, Ocorrencia[]>();
  for (const o of ocorrencias) push(porId, o.id, o);
  for (const o of ocorrencias) {
    for (const a of ind.saindo.get(o.id) ?? []) {
      if (!LIGACOES_TECNICAS.has(a.tipo)) continue;
      const alvos = porId.get(a.destino);
      if (!alvos) continue;
      // liga à ocorrência de destino mais próxima no caminho (maior prefixo comum)
      const alvo = maisProxima(o, alvos);
      if (alvo.chave === o.chave) continue;
      arestas.push({ id: `t|${a.tipo}|${o.chave}|${alvo.chave}`, origem: o.chave, destino: alvo.chave, ligacao: a.tipo, tecnica: true, aresta: a });
    }
  }
  return { ocorrencias, paginacoes, arestas };
}

/** Expande todos os ancestrais de um caminho e garante que a página do item esteja visível. */
export function revelarCaminho(ind: Indice, visao: Visao, exp: EstadoExpansao, caminho: readonly string[], tamanhoPagina = TAMANHO_PAGINA): void {
  for (let i = 1; i < caminho.length; i++) {
    const paiCam = caminho.slice(0, i);
    const chave = chaveDe(paiCam);
    exp.expandidos.add(chave);
    const pos = ind.filhos(visao, paiCam).findIndex((f) => f.id === caminho[i]);
    // fora das páginas já carregadas: fixa só este item (não carrega todas as páginas até ele)
    if (pos >= (exp.paginas.get(chave) ?? 1) * tamanhoPagina) {
      exp.fixados ??= new Set();
      exp.fixados.add(chaveDe(caminho.slice(0, i + 1)));
    }
  }
}

/** Recolhe uma ocorrência e tudo abaixo dela. */
export function recolher(exp: EstadoExpansao, chave: string): void {
  for (const k of [...exp.expandidos]) if (k === chave || k.startsWith(chave + SEP)) exp.expandidos.delete(k);
  for (const k of [...exp.paginas.keys()]) if (k === chave || k.startsWith(chave + SEP)) exp.paginas.delete(k);
  for (const k of [...(exp.fixados ?? [])]) if (k.startsWith(chave + SEP)) exp.fixados!.delete(k);
}

// ----------------------------------------------------------------- utilidades

function push<K, V>(m: Map<K, V[]>, k: K, v: V): void {
  const l = m.get(k);
  if (l) l.push(v);
  else m.set(k, [v]);
}

function percorrer(no: ArvoreVisao, caminho: string[], f: (caminho: string[], no: ArvoreVisao) => void): void {
  const c = [...caminho, no.id];
  if (caminho.length) f(c, no);
  for (const x of no.filhos ?? []) percorrer(x, c, f);
}

function localizar(raiz: ArvoreVisao, caminho: readonly string[]): ArvoreVisao | null {
  if (caminho[0] !== raiz.id) return null;
  let atual: ArvoreVisao | undefined = raiz;
  for (let i = 1; i < caminho.length && atual; i++) atual = (atual.filhos ?? []).find((f) => f.id === caminho[i]);
  return atual ?? null;
}

function ligacaoTopo(visao: Visao, profundidadePai: number, filho: ArvoreVisao): string {
  if (visao === 'funcionalidade') {
    if (profundidadePai === 1) return 'navegacao_classificacao';
    if (profundidadePai === 2) return 'navegacao_subclassificacao';
    return filho.ocorrencia === 'secundaria' ? 'classificacao_secundaria' : 'classificacao_principal';
  }
  if (profundidadePai === 1) return 'navegacao_nuvem';
  if (profundidadePai === 2) return 'nuvem_classificacao';
  if (profundidadePai === 3) return 'nuvem_subclassificacao';
  return 'nuvem_funcionalidade';
}

function maisProxima(o: Ocorrencia, alvos: Ocorrencia[]): Ocorrencia {
  let melhor = alvos[0];
  let k0 = -1;
  for (const a of alvos) {
    let k = 0;
    while (k < a.caminho.length && k < o.caminho.length && a.caminho[k] === o.caminho[k]) k++;
    if (k > k0) {
      k0 = k;
      melhor = a;
    }
  }
  return melhor;
}
