import type { DadosBase, Entidade, InfoBuild } from './tipos';

/** Pasta dos dados publicados. `?dados=sintetico` aponta para a fixture de performance (nunca conteúdo). */
export function pastaDados(busca: string = location.search): string {
  const p = new URLSearchParams(busca);
  return p.get('dados') === 'sintetico' ? './__teste-sintetico/' : './data/';
}

/** Mesmo mapeamento de ferramentas/sftutor.py:caminho_entidade. */
export function caminhoEntidade(id: string): string {
  if (id === 'salesforce') return 'entidades/salesforce.json';
  const i = id.indexOf(':');
  if (i < 0) throw new Error(`id sem prefixo: ${id}`);
  return `entidades/${id.slice(0, i)}/${encodeURIComponent(id.slice(i + 1))}.json`;
}

export class ErroCarga extends Error {
  constructor(public arquivo: string, public causa: string) {
    super(`Não foi possível carregar ${arquivo}: ${causa}`);
  }
}

async function json<T>(base: string, arquivo: string): Promise<T> {
  let r: Response;
  try {
    r = await fetch(base + arquivo);
  } catch (e) {
    throw new ErroCarga(arquivo, String(e));
  }
  if (!r.ok) throw new ErroCarga(arquivo, `HTTP ${r.status}`);
  return (await r.json()) as T;
}

export const VERSAO_CONTRATO_SUPORTADA = 1;

export async function carregarBase(base = pastaDados()): Promise<DadosBase> {
  const manifesto = await json<DadosBase['manifesto']>(base, 'manifest.json');
  const maior = Number(manifesto.contrato?.versao?.split('.')[0]);
  if (manifesto.contrato?.nome !== 'sf-tutor-site' || maior !== VERSAO_CONTRATO_SUPORTADA) {
    throw new ErroCarga('manifest.json', `contrato ${manifesto.contrato?.nome} ${manifesto.contrato?.versao} não suportado (esperado sf-tutor-site ${VERSAO_CONTRATO_SUPORTADA}.x)`);
  }
  const a = manifesto.arquivos;
  const [grafo, visoes, busca, fontes, cobertura, build] = await Promise.all([
    json<{ nos: DadosBase['nos']; arestas: DadosBase['arestas'] }>(base, a.grafo_base),
    json<DadosBase['visoes']>(base, a.visoes),
    json<DadosBase['busca']>(base, a.busca),
    json<DadosBase['fontes']>(base, a.fontes),
    json<DadosBase['cobertura']>(base, a.cobertura),
    json<InfoBuild>(base, 'build-info.json').catch(() => ({ commit: null, data_build: '', origem: 'desconhecida' })),
  ]);
  return { manifesto, nos: grafo.nos, arestas: grafo.arestas, visoes, busca, fontes, cobertura, build };
}

/** Cache de entidades carregadas sob demanda (cada arquivo traz os campos/propriedades da entidade). */
export class Entidades {
  private cache = new Map<string, Promise<Entidade>>();
  constructor(private base = pastaDados()) {}
  obter(id: string): Promise<Entidade> {
    let p = this.cache.get(id);
    if (!p) {
      p = json<Entidade>(this.base, caminhoEntidade(id));
      this.cache.set(id, p);
      p.catch(() => this.cache.delete(id));
    }
    return p;
  }
  carregada(id: string): boolean {
    return this.cache.has(id);
  }
}
