// Estado navegável na URL: id canônico (n), caminho contextual (c), visão (v), modo (m), relação (r),
// tabela de campos aberta (t) e item em foco nela (f).
// O id é a identidade do item; o caminho só preserva o contexto quando há vários caminhos.
import type { Visao } from './model/adaptador';
import { SEP } from './model/adaptador';

export interface EstadoURL {
  visao: Visao;
  modo: 'mapa' | 'lista';
  id?: string;
  caminho?: string[];
  rel?: string;
  /** dono da tabela de campos ou propriedades aberta (metadata type, estrutura auxiliar ou objeto) */
  tabela?: string;
  /** item em foco na tabela */
  foco?: string;
  sintetico?: boolean;
}

export function lerURL(search: string = location.search): EstadoURL {
  const p = new URLSearchParams(search);
  const v = p.get('v') === 'nuvem' ? 'nuvem' : 'funcionalidade';
  const m = p.get('m') === 'lista' ? 'lista' : 'mapa';
  const c = p.get('c');
  return {
    visao: v,
    modo: m,
    id: p.get('n') ?? undefined,
    caminho: c ? c.split(SEP).filter(Boolean) : undefined,
    rel: p.get('r') ?? undefined,
    tabela: p.get('t') ?? undefined,
    foco: p.get('f') ?? undefined,
    sintetico: p.get('dados') === 'sintetico',
  };
}

export function montarURL(e: EstadoURL): string {
  const p = new URLSearchParams();
  if (e.sintetico) p.set('dados', 'sintetico');
  if (e.visao === 'nuvem') p.set('v', 'nuvem');
  if (e.modo === 'lista') p.set('m', 'lista');
  if (e.rel) p.set('r', e.rel);
  if (e.id) p.set('n', e.id);
  if (e.caminho && e.caminho.length > 1) p.set('c', e.caminho.join(SEP));
  if (e.tabela) p.set('t', e.tabela);
  if (e.tabela && e.foco) p.set('f', e.foco);
  const s = p.toString();
  return s ? `?${s}` : '?';
}
