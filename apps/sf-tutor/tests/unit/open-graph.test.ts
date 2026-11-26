// Prévia do link (Open Graph): as tags apontam para o endereço público e para a imagem versionada em public/og/.
import { describe, expect, it } from 'vitest';
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { REPORTE } from '../../src/reporte';

const app = join(__dirname, '..', '..');
const html = readFileSync(join(app, 'index.html'), 'utf8');
const meta = (atributo: string, nome: string): string | undefined =>
  html.match(new RegExp(`<meta ${atributo}="${nome}" content="([^"]*)"`))?.[1];

const [dono, repo] = REPORTE.repoIssues.split('/');
const enderecoPublico = `https://${dono}.github.io/${repo}/`;

describe('Open Graph', () => {
  it('tem as tags de título, descrição, URL, imagem e o card grande', () => {
    for (const p of ['og:title', 'og:description', 'og:url', 'og:image', 'og:type', 'og:image:alt']) expect(meta('property', p), p).toBeTruthy();
    expect(meta('name', 'twitter:card')).toBe('summary_large_image');
  });

  it('usa o endereço do repositório público (o mesmo das issues)', () => {
    expect(meta('property', 'og:url')).toBe(enderecoPublico);
    expect(html).toContain(`<link rel="canonical" href="${enderecoPublico}" />`);
    expect(meta('property', 'og:image')?.startsWith(enderecoPublico)).toBe(true);
    expect(meta('name', 'twitter:image')).toBe(meta('property', 'og:image'));
  });

  it('a imagem existe em public/, é PNG e tem 1200×627 como as tags dizem', () => {
    const relativo = meta('property', 'og:image')!.slice(enderecoPublico.length);
    const arquivo = join(app, 'public', relativo);
    expect(existsSync(arquivo), arquivo).toBe(true);
    const b = readFileSync(arquivo);
    expect(b.subarray(1, 4).toString('latin1')).toBe('PNG');
    expect([b.readUInt32BE(16), b.readUInt32BE(20)]).toEqual([1200, 627]);
    expect(meta('property', 'og:image:width')).toBe('1200');
    expect(meta('property', 'og:image:height')).toBe('627');
    expect(b.length).toBeLessThan(5 * 1024 * 1024);
  });
});
