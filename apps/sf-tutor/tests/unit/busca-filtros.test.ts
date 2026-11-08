import { describe, expect, it, beforeAll } from 'vitest';
import { Indice } from '../../src/model/adaptador';
import { IndiceBusca, normalizar } from '../../src/model/busca';
import { filtrosVazios, filtrosAtivos, motivoOculto } from '../../src/model/filtros';
import { montarURL, lerURL } from '../../src/rotas';
import { dadosReais } from './dados-reais';

let ind: Indice;
let busca: IndiceBusca;
beforeAll(() => { const d = dadosReais(); ind = new Indice(d); busca = new IndiceBusca(d.busca); });
const rot = (id: string) => ind.no(id)?.rotulo ?? id;

describe('busca', () => {
  it('normaliza acentos e caixa', () => { expect(normalizar('Permissões')).toBe('permissoes'); });
  it('acha funcionalidade por termo em português', () => {
    expect(busca.buscar('usuários').map((r) => r.item.id)).toContain('func:usuarios');
  });
  it('acha campo ainda não carregado no mapa', () => {
    const ids = busca.buscar('ProfileId').map((r) => r.item.id);
    expect(ids).toContain('obj:User.ProfileId');
  });
  it('nome técnico exato vem primeiro', () => {
    expect(busca.buscar('PermissionSet')[0].item.id).toMatch(/^(mdt|obj):PermissionSet$/);
  });
  it('consulta vazia não retorna nada', () => { expect(busca.buscar('  ')).toEqual([]); });
});

describe('filtros', () => {
  it('sem filtros nada fica oculto', () => {
    expect(filtrosAtivos(filtrosVazios())).toBe(0);
    expect(motivoOculto(ind, 'obj:User', filtrosVazios(), rot)).toBeNull();
  });
  it('filtro por nuvem explica por que um item foi esmaecido', () => {
    const f = filtrosVazios();
    f.nuvens.add('nuv:data-360');
    expect(filtrosAtivos(f)).toBe(1);
    const m = motivoOculto(ind, 'func:usuarios', f, rot);
    expect(m).toBeTruthy();
    expect(typeof m).toBe('string');
  });
  it('grupos (classificações) nunca ficam ocultos', () => {
    const f = filtrosVazios();
    f.nuvens.add('nuv:data-360');
    expect(motivoOculto(ind, 'cls:acesso-identidade-e-seguranca', f, rot)).toBeNull();
  });
});

describe('URL', () => {
  it('ida e volta preserva visão, modo, id e caminho', () => {
    const e = { visao: 'nuvem' as const, modo: 'lista' as const, id: 'func:apps-de-console', caminho: ['salesforce', 'nuv:service-cloud', 'func:apps-de-console'] };
    const u = montarURL(e);
    const l = lerURL(u);
    expect(l.visao).toBe('nuvem');
    expect(l.modo).toBe('lista');
    expect(l.id).toBe(e.id);
    expect(l.caminho).toEqual(e.caminho);
  });
});
