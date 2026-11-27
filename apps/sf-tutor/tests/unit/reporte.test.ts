import { describe, expect, it } from 'vitest';
import {
  assunto, comoSabe, destinatario, montarTexto, normalizarEmail, normalizarGithub, REPORTE, situacao, SITUACOES, urlIssue, urlMailto,
  type CamposReporte, type ContextoReporte,
} from '../../src/reporte';

const ctx: ContextoReporte = {
  id: 'mdt:SecuritySettings', rotulo: 'Security Settings', tipo: 'Metadata type', status: 'Verificado',
  link: 'https://exemplo.github.io/tutorial/?n=mdt%3ASecuritySettings', versao: 'API 68.0 · contrato 1.4.0 · insumos abc1234',
};
const campos: CamposReporte = {
  situacao: 'errado', atual: 'O default está errado.', correto: 'É true.', fonte: 'https://developer.salesforce.com/x', pratica: true,
  nome: 'Ana', github: '@ana-dev', email: 'ana@exemplo.com',
};

describe('reporte de erro: configuração', () => {
  it('o e-mail do suporte fica codificado no código e é montado só na chamada', () => {
    expect(REPORTE.destinoCodificado).not.toContain('@');
    expect(destinatario()).toMatch(/^[^@\s]+@[^@\s]+\.[a-z]+$/);
  });

  it('"O que aconteceu?" tem as situações previstas, cada uma com suas perguntas; "org" não pergunta nada', () => {
    expect(SITUACOES.map((s) => s.id)).toEqual(['errado', 'desatualizado', 'confuso', 'fonte', 'ligacao', 'outro', 'org']);
    for (const s of SITUACOES.filter((x) => x.id !== 'org')) {
      expect(s.perguntaAtual.endsWith('?') || s.perguntaAtual.endsWith('.')).toBe(true);
      expect(s.perguntaCorreto.length).toBeGreaterThan(5);
    }
    expect(situacao('org')?.perguntaAtual).toBe('');
    expect(situacao('confuso')?.perguntaAtual).toBe('O que ficou confuso?');
  });
});

describe('reporte de erro: validações', () => {
  it('usuário do GitHub é opcional e validado', () => {
    expect(normalizarGithub('ana-dev')).toBe('@ana-dev');
    expect(normalizarGithub('@ana-dev')).toBe('@ana-dev');
    expect(normalizarGithub('')).toBe('');
    expect(normalizarGithub('nome com espaço')).toBe('');
    expect(normalizarGithub('-comeca-com-hifen')).toBe('');
  });

  it('e-mail para aviso é opcional e validado', () => {
    expect(normalizarEmail(' ana@exemplo.com ')).toBe('ana@exemplo.com');
    expect(normalizarEmail('')).toBe('');
    expect(normalizarEmail('ana@')).toBe('');
    expect(normalizarEmail('ana exemplo.com')).toBe('');
  });

  it('"Como você sabe?" junta link e prática', () => {
    expect(comoSabe(campos)).toBe('documentação oficial: https://developer.salesforce.com/x; pela prática');
    expect(comoSabe({ ...campos, fonte: '', pratica: false })).toBe('');
    expect(comoSabe({ ...campos, fonte: '' })).toBe('pela prática');
  });
});

describe('reporte de erro: texto, e-mail e issue', () => {
  it('assunto segue o padrão e leva o item', () => {
    expect(assunto(ctx)).toBe('ERRO REPORTADO: Metadata Desbugado (mdt:SecuritySettings)');
    expect(assunto({ ...ctx, item: { id: 'x', nome: 'sessionTimeout' } })).toContain('mdt:SecuritySettings > sessionTimeout');
  });

  it('o texto usa as perguntas da situação e leva o status do site', () => {
    const t = montarTexto(ctx, { ...campos, parte: 'seção Avançado' }, { hoje: new Date('2026-11-24T12:00:00Z') });
    for (const s of ['Item: Security Settings (mdt:SecuritySettings)', 'Status no site: Verificado', 'Parte da ficha: seção Avançado',
      'Data do reporte: 2026-11-24', 'O que aconteceu: Está errado', 'O que está escrito aqui que parece errado?', 'O default está errado.',
      'Como deveria ser?', 'Como sabe: documentação oficial: https://developer.salesforce.com/x; pela prática', 'Reportado por: Ana · GitHub @ana-dev']) {
      expect(t).toContain(s);
    }
    expect(montarTexto(ctx, { situacao: 'outro', atual: 'x' })).toContain('Reportado por: (anônimo)');
    expect(montarTexto(ctx, { situacao: 'confuso', atual: 'x' })).toContain('O que ficou confuso?');
  });

  it('o e-mail para aviso só entra quando pedido (envio por e-mail e texto copiado)', () => {
    expect(montarTexto(ctx, campos)).not.toContain('ana@exemplo.com');
    expect(montarTexto(ctx, campos, { incluirEmail: true })).toContain('Avisar a correção em: ana@exemplo.com');
    expect(montarTexto(ctx, { ...campos, email: 'invalido' }, { incluirEmail: true })).not.toContain('Avisar a correção');
  });

  it('mailto codifica assunto e corpo, com o e-mail para aviso', () => {
    const u = urlMailto(ctx, campos, 'destino@exemplo.com');
    expect(u.startsWith('mailto:destino@exemplo.com?subject=ERRO%20REPORTADO')).toBe(true);
    const corpo = decodeURIComponent(u.split('&body=')[1]);
    expect(corpo).toContain('O default está errado.');
    expect(corpo).toContain('Avisar a correção em: ana@exemplo.com');
  });

  it('a issue vai para o repositório público, preenchida, e nunca leva o e-mail de quem reporta', () => {
    const u = new URL(urlIssue(ctx, campos));
    expect(u.pathname).toBe(`/${REPORTE.repoIssues}/issues/new`);
    expect(u.searchParams.get('template')).toBe('erro-reportado.yml');
    expect(u.searchParams.get('item')).toBe('Security Settings (mdt:SecuritySettings)');
    expect(u.searchParams.get('tipo')).toBe('Está errado');
    expect(u.searchParams.get('status')).toBe('Verificado');
    expect(u.searchParams.get('descricao')).toBe('O default está errado.');
    expect(u.searchParams.get('fonte')).toBe('documentação oficial: https://developer.salesforce.com/x; pela prática');
    expect(u.searchParams.get('body')).toContain('O que aconteceu: Está errado');
    expect(u.searchParams.get('body')).toContain('O default está errado.');
    expect(u.searchParams.get('body')).not.toContain('Avisar a correção');
    expect(u.toString()).not.toContain('ana%40exemplo.com');
    expect(u.toString()).not.toContain('ana@exemplo.com');
    expect(u.toString()).not.toContain(encodeURIComponent(destinatario()));
  });
});
