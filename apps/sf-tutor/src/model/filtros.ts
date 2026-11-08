// Filtros. Itens filtrados continuam no mapa, esmaecidos, para não romper relações com significado enganoso;
// a interface explica o motivo de cada item oculto.
import { Indice, TIPOS_FOLHA, TIPOS_OBJETO } from './adaptador';

export interface Filtros {
  nuvens: Set<string>;          // vazio = todas
  classificacoes: Set<string>;  // vazio = todas
  representacao: 'todas' | 'com_xml' | 'com_api' | 'sem_xml';
  apis: Set<string>;            // 'padrao' | 'tooling'; vazio = todas
  estados: Set<string>;         // vazio = todos
}

export const filtrosVazios = (): Filtros => ({ nuvens: new Set(), classificacoes: new Set(), representacao: 'todas', apis: new Set(), estados: new Set() });

export function filtrosAtivos(f: Filtros): number {
  return f.nuvens.size + f.classificacoes.size + (f.representacao !== 'todas' ? 1 : 0) + f.apis.size + f.estados.size;
}

/** Motivo pelo qual o item fica oculto pelos filtros, ou null se passa. Agrupamentos nunca são ocultados. */
export function motivoOculto(ind: Indice, id: string, f: Filtros, rotulo: (id: string) => string): string | null {
  const n = ind.no(id);
  if (!n) return null;
  if (n.tipo === 'salesforce' || n.tipo === 'classificacao' || n.tipo === 'subclassificacao') return null;
  if (n.tipo === 'nuvem') return f.nuvens.size && !f.nuvens.has(id) ? 'nuvem fora do filtro' : null;
  if (f.estados.size && n.estado && !f.estados.has(n.estado)) return `estado de validação "${n.estado}" fora do filtro`;
  if (f.apis.size && (TIPOS_OBJETO.has(n.tipo) || n.tipo === 'campo_api')) {
    const apis = n.apis ?? ind.no(n.pai ?? '')?.apis ?? [];
    if (!apis.some((a) => f.apis.has(a))) return `sem exposição verificada em ${[...f.apis].map(nomeApi).join(' ou ')}`;
  }
  const funcs = ind.funcionalidadesDe(id);
  if (!funcs.length) return null;
  const passa = funcs.filter((fid) => funcPassa(ind, fid, f));
  if (passa.length) return null;
  const r = motivoFunc(ind, funcs[0], f);
  return n.tipo === 'funcionalidade' ? r : `pertence a ${rotulo(funcs[0])}, oculta: ${r}`;
}

function funcPassa(ind: Indice, fid: string, f: Filtros): boolean {
  return motivoFunc(ind, fid, f) === null;
}

function motivoFunc(ind: Indice, fid: string, f: Filtros): string | null {
  if (f.nuvens.size && !(ind.nuvensDaFunc.get(fid) ?? []).some((n) => f.nuvens.has(n))) return 'não está em nenhuma nuvem selecionada';
  if (f.classificacoes.size && !(ind.classificacoesDaFunc.get(fid) ?? []).some((c) => f.classificacoes.has(c))) return 'fora das classificações selecionadas';
  const s = ind.saindo.get(fid) ?? [];
  const temXml = s.some((a) => a.tipo === 'representacao_xml');
  const temApi = s.some((a) => a.tipo === 'representacao_objeto_api');
  if (f.representacao === 'com_xml' && !temXml) return 'sem metadata type (XML) catalogado';
  if (f.representacao === 'com_api' && !temApi) return 'sem objeto API catalogado';
  if (f.representacao === 'sem_xml' && temXml) return 'tem metadata type (XML)';
  return null;
}

function nomeApi(a: string): string {
  return a === 'padrao' ? 'API padrão' : a === 'tooling' ? 'Tooling API' : a;
}

export { TIPOS_FOLHA };
