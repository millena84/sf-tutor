// Retorno honesto depois do mailto: a página nunca afirma que o e-mail foi enviado.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { acompanharMailto } from '../../src/ui/reporte';

function docFalso() {
  const ouvintes = new Set<() => void>();
  const doc = {
    visibilityState: 'visible' as DocumentVisibilityState,
    addEventListener: (_: string, f: () => void) => ouvintes.add(f),
    removeEventListener: (_: string, f: () => void) => ouvintes.delete(f),
  };
  const mudar = (v: DocumentVisibilityState) => { doc.visibilityState = v; [...ouvintes].forEach((f) => f()); };
  return { doc: doc as unknown as Document, mudar, ouvintes };
}

describe('acompanharMailto', () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it('sem sair da página: avisa que nenhum app abriu e que nada foi enviado', () => {
    const { doc, ouvintes } = docFalso();
    const avisos: string[] = [];
    acompanharMailto((t) => avisos.push(t), doc, 2500);
    vi.advanceTimersByTime(2500);
    expect(avisos).toHaveLength(1);
    expect(avisos[0]).toMatch(/nenhum app de e-mail abriu.*nada foi enviado/);
    expect(ouvintes.size).toBe(0);
  });

  it('saiu para o app e voltou: lembra que só chega se tocou em Enviar', () => {
    const { doc, mudar, ouvintes } = docFalso();
    const avisos: string[] = [];
    acompanharMailto((t) => avisos.push(t), doc, 2500);
    mudar('hidden');
    vi.advanceTimersByTime(10000);
    expect(avisos).toHaveLength(0);
    mudar('visible');
    expect(avisos).toHaveLength(1);
    expect(avisos[0]).toMatch(/só chega se você tocou em Enviar.*Se cancelou, nada foi enviado/);
    expect(ouvintes.size).toBe(0);
  });

  it('nunca diz que o e-mail foi enviado', () => {
    const { doc, mudar } = docFalso();
    const avisos: string[] = [];
    acompanharMailto((t) => avisos.push(t), doc, 10);
    vi.advanceTimersByTime(10);
    acompanharMailto((t) => avisos.push(t), doc, 10);
    mudar('hidden'); mudar('visible');
    expect(avisos).toHaveLength(2);
    for (const a of avisos) {
      expect(a).not.toMatch(/enviado com sucesso|e-mail enviado|reporte enviado/i);
      expect(a).toMatch(/nada foi enviado/);
    }
  });
});
