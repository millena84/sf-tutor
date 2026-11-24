import { describe, expect, it } from 'vitest';
import { assunto, destinatario, montarTexto, normalizarGithub, REPORTE, urlIssue, urlMailto, type ContextoReporte } from '../../src/reporte';

const ctx: ContextoReporte = {
  id: 'mdt:SecuritySettings', rotulo: 'Security Settings', tipo: 'Metadata type',
  link: 'https://exemplo.github.io/tutorial/?n=mdt%3ASecuritySettings', versao: 'API 68.0 · contrato 1.3.0 · insumos abc1234',
};
const campos = { tipo: 'Informação incorreta', descricao: 'O default está errado.', correto: 'É true.', fonte: 'https://developer.salesforce.com/x', nome: 'Ana', github: '@ana-dev' };

describe('reporte de erro', () => {
  it('o e-mail fica codificado no código e é montado só na chamada', () => {
    expect(REPORTE.destinoCodificado).not.toContain('@');
    expect(destinatario()).toMatch(/^[^@\s]+@[^@\s]+\.[a-z]+$/);
  });

  it('assunto segue o padrão e leva o item', () => {
    expect(assunto(ctx)).toBe('ERRO REPORTADO: tutorial Salesforce - sf-tutor (mdt:SecuritySettings)');
    expect(assunto({ ...ctx, item: { id: 'x', nome: 'sessionTimeout' } })).toContain('mdt:SecuritySettings > sessionTimeout');
  });

  it('usuário do GitHub é opcional e validado', () => {
    expect(normalizarGithub('ana-dev')).toBe('@ana-dev');
    expect(normalizarGithub('@ana-dev')).toBe('@ana-dev');
    expect(normalizarGithub('')).toBe('');
    expect(normalizarGithub('nome com espaço')).toBe('');
    expect(normalizarGithub('-comeca-com-hifen')).toBe('');
  });

  it('o texto leva contexto, campos e quem reporta; sem nome vira anônimo', () => {
    const t = montarTexto(ctx, campos, new Date('2026-11-24T12:00:00Z'));
    for (const s of ['Item: Security Settings (mdt:SecuritySettings)', 'Versão dos dados: API 68.0', 'Data do reporte: 2026-11-24',
      'Tipo de problema: Informação incorreta', 'O default está errado.', 'Qual seria o correto:', 'Fonte:', 'Reportado por: Ana · GitHub @ana-dev']) {
      expect(t).toContain(s);
    }
    expect(montarTexto(ctx, { tipo: 'Outro', descricao: 'x' })).toContain('Reportado por: (anônimo)');
  });

  it('mailto codifica assunto e corpo', () => {
    const u = urlMailto(ctx, campos, 'destino@exemplo.com');
    expect(u.startsWith('mailto:destino@exemplo.com?subject=ERRO%20REPORTADO')).toBe(true);
    expect(decodeURIComponent(u.split('&body=')[1])).toContain('O default está errado.');
  });

  it('a issue vai para o repositório público, com o modelo e os campos preenchidos', () => {
    const u = new URL(urlIssue(ctx, campos));
    expect(u.pathname).toBe(`/${REPORTE.repoIssues}/issues/new`);
    expect(u.searchParams.get('template')).toBe('erro-reportado.yml');
    expect(u.searchParams.get('item')).toBe('Security Settings (mdt:SecuritySettings)');
    expect(u.searchParams.get('descricao')).toBe('O default está errado.');
    expect(u.searchParams.get('fonte')).toBe('https://developer.salesforce.com/x');
    expect(u.toString()).not.toContain(destinatario());
  });
});
