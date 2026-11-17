// #17: em ramos densos, irmãos vizinhos não podem ficar tão perto que os rótulos se sobreponham.
import { describe, expect, it } from 'vitest';
import { DESLOCAMENTO_ALTERNADO, LIMITE_ANEL_UNICO, posicionar } from '../../src/graph/layout';
import type { Cena, Ocorrencia } from '../../src/model/adaptador';

function oc(chave: string, pai: string | null, prof: number): Ocorrencia {
  return { chave, id: chave, caminho: chave.split('>'), profundidade: prof, paiChave: pai, ligacao: null, totalFilhos: 0 };
}

/** raiz > pai (deslocado à direita) > n filhos */
function cena(n: number): Cena {
  const ocorrencias = [oc('r', null, 0), oc('r>p', 'r', 1)];
  for (let i = 0; i < n; i++) ocorrencias.push(oc(`r>p>f${i}`, 'r>p', 2));
  return { ocorrencias, paginacoes: [], arestas: [] };
}

const dist = (a: { x: number; y: number }, b: { x: number; y: number }) => Math.hypot(a.x - b.x, a.y - b.y);

describe('layout em leque', () => {
  it('até o limite, todos os irmãos ficam no mesmo raio', () => {
    const pos = posicionar(cena(LIMITE_ANEL_UNICO), new Map());
    const p = pos.get('r>p')!;
    const raios = Array.from({ length: LIMITE_ANEL_UNICO }, (_, i) => Math.round(dist(pos.get(`r>p>f${i}`)!, p)));
    expect(new Set(raios).size).toBe(1);
  });

  it('acima do limite, os ímpares vão para um anel externo alternado', () => {
    const n = 15;
    const pos = posicionar(cena(n), new Map());
    const p = pos.get('r>p')!;
    const r0 = dist(pos.get('r>p>f0')!, p);
    const r1 = dist(pos.get('r>p>f1')!, p);
    expect(Math.round(r1 - r0)).toBe(DESLOCAMENTO_ALTERNADO);
  });

  it('com 15 irmãos, vizinhos do mesmo anel ficam a mais de 130px (largura máxima do rótulo)', () => {
    const n = 15;
    const pos = posicionar(cena(n), new Map());
    for (let i = 0; i + 2 < n; i++) {
      expect(dist(pos.get(`r>p>f${i}`)!, pos.get(`r>p>f${i + 2}`)!)).toBeGreaterThan(130);
    }
    for (let i = 0; i + 1 < n; i++) {
      expect(dist(pos.get(`r>p>f${i}`)!, pos.get(`r>p>f${i + 1}`)!)).toBeGreaterThan(90);
    }
  });
});
