// "Já vi o tour" no armazenamento local, sem quebrar quando ele falha.
import { describe, expect, it } from 'vitest';
import { CHAVE_TOUR, marcarTourVisto, PASSOS, tourVisto } from '../../src/ui/tour';

describe('tour: armazenamento', () => {
  it('lê e grava a marca', () => {
    const m = new Map<string, string>();
    const s = { getItem: (k: string) => m.get(k) ?? null, setItem: (k: string, v: string) => { m.set(k, v); } };
    expect(tourVisto(s)).toBe(false);
    marcarTourVisto(s);
    expect(m.get(CHAVE_TOUR)).toBe('1');
    expect(tourVisto(s)).toBe(true);
  });

  it('armazenamento ausente ou que lança erro: trata como não visto e não quebra', () => {
    const quebrado = { getItem: () => { throw new Error('bloqueado'); }, setItem: () => { throw new Error('cheio'); } };
    expect(tourVisto(quebrado)).toBe(false);
    expect(() => marcarTourVisto(quebrado)).not.toThrow();
    expect(tourVisto(null)).toBe(false);
  });
});

describe('tour: passos', () => {
  it('tem 6 passos com título, texto e alvo', () => {
    expect(PASSOS).toHaveLength(6);
    for (const p of PASSOS) {
      expect(p.titulo.length).toBeGreaterThan(3);
      expect(p.texto.length).toBeGreaterThan(20);
      expect(p.alvo.length).toBeGreaterThan(1);
    }
  });
});
