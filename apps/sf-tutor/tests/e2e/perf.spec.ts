// Performance: dados reais e FIXTURE SINTÉTICA (rotulada; não é conteúdo Salesforce).
// Rode com "npm run perf" (gera dist/__teste-sintetico antes). Resultados em tests/resultados/perf-*.json.
import { expect, test, type Page } from '@playwright/test';
import { writeFileSync, mkdirSync } from 'node:fs';
import os from 'node:os';

type Medidas = Record<string, number | string>;
// tipo só para o TypeScript; dentro de page.evaluate não pode haver funções do teste
type W = { __sfTutor: { nosRenderizados(): number; totalCatalogo: number; selecao(): string | null } };

async function carregar(page: Page, q: string, m: Medidas): Promise<void> {
  const t0 = Date.now();
  await page.goto(`/${q}`);
  await page.waitForFunction(() => (window as unknown as { __sfTutor?: { pronto: boolean } }).__sfTutor?.pronto === true, null, { timeout: 60_000 });
  m.carga_ate_interativo_ms = Date.now() - t0;
  m.total_no_catalogo = await page.evaluate(() => (window as unknown as W).__sfTutor.totalCatalogo);
  m.nos_desenhados_inicio = await page.evaluate(() => (window as unknown as W).__sfTutor.nosRenderizados());
}

/** mede o tempo de uma ação até o título do painel mudar para o esperado */
async function medir(page: Page, m: Medidas, nome: string, acao: () => Promise<void>, esperado: RegExp | string): Promise<void> {
  const t0 = Date.now();
  await acao();
  await expect(page.locator('#titulo-painel')).toHaveText(esperado, { timeout: 30_000 });
  m[`${nome}_ms`] = Date.now() - t0;
}

function gravar(nome: string, m: Medidas): void {
  mkdirSync('tests/resultados', { recursive: true });
  const amb = { cpu: os.cpus()[0]?.model ?? '?', nucleos: os.cpus().length, memoria_gb: Math.round(os.totalmem() / 2 ** 30), node: process.version, navegador: 'Chrome headless (Playwright)', viewport: '1366x900', data: new Date().toISOString() };
  writeFileSync(`tests/resultados/perf-${nome}.json`, JSON.stringify({ ambiente: amb, medidas: m }, null, 2));
  console.log(nome, JSON.stringify(m));
}

test('dados reais', async ({ page }) => {
  const m: Medidas = {};
  await carregar(page, '', m);
  await medir(page, m, 'abrir_campo_por_busca', async () => {
    await page.locator('#busca').fill('ProfileId');
    await page.locator('#resultados [role=option]').filter({ hasText: 'User' }).first().click();
  }, 'ProfileId');
  await medir(page, m, 'abrir_objeto_e_expandir', async () => {
    await page.locator('#conteudo-painel').locator('p', { hasText: 'Pertence a' }).getByRole('button').click();
  }, 'User');
  let t1 = Date.now();
  await page.locator('#conteudo-painel').getByRole('button', { name: /^Expandir|^Recolher/ }).first().click();
  m.expandir_recolher_ms = Date.now() - t1;
  t1 = Date.now();
  await page.locator('[data-visao=nuvem]').click();
  await page.waitForFunction(() => (window as unknown as W).__sfTutor.selecao()?.includes('nuv:') === true);
  m.trocar_visao_mantendo_selecao_ms = Date.now() - t1;
  m.nos_desenhados_fim = await page.evaluate(() => (window as unknown as W).__sfTutor.nosRenderizados());
  gravar('reais', m);
  expect(m.carga_ate_interativo_ms as number).toBeLessThan(10_000);
});

test('fixture sintética', async ({ page }) => {
  const m: Medidas = { aviso: 'FIXTURE SINTÉTICA — não é conteúdo Salesforce' };
  await carregar(page, '?dados=sintetico', m);
  await expect(page.locator('#faixa-sintetica')).toBeVisible();
  // objeto com 3000 campos: abrir, expandir (1ª página), paginar 3 vezes
  await medir(page, m, 'abrir_objeto_gigante', async () => {
    await page.locator('#busca').fill('SintObj0');
    await page.locator('#resultados [role=option]').filter({ hasText: /^.*SintObj0/ }).first().click();
  }, 'SintObj0');
  let t0 = Date.now();
  await page.locator('#conteudo-painel').getByRole('button', { name: /^Expandir/ }).click();
  await page.waitForFunction(() => (window as unknown as W).__sfTutor.nosRenderizados() > 40);
  m.expandir_3000_campos_1a_pagina_ms = Date.now() - t0;
  m.nos_desenhados_apos_expandir = await page.evaluate(() => (window as unknown as W).__sfTutor.nosRenderizados());
  // carrega mais 4 páginas tocando no nó "+N mais" (chave = caminho do objeto + '>#mais'), para o arraste mover mais de 100 nós
  const chaveObj = await page.evaluate(() => (window as unknown as W).__sfTutor.selecao());
  for (let i = 0; i < 4 && chaveObj; i++) {
    const pm = await page.evaluate((c) => (window as unknown as { __sfTutor: { ponto(a: { no?: string }): { x: number; y: number } | null } }).__sfTutor.ponto({ no: c }), `${chaveObj}>#mais`);
    if (!pm) break;
    await page.locator('#btn-enquadrar').click();
    await page.waitForTimeout(350);
    const pm2 = await page.evaluate((c) => (window as unknown as { __sfTutor: { ponto(a: { no?: string }): { x: number; y: number } | null } }).__sfTutor.ponto({ no: c }), `${chaveObj}>#mais`);
    if (!pm2) break;
    await page.mouse.click(pm2.x, pm2.y);
    await page.waitForTimeout(150);
  }
  m.nos_desenhados_apos_paginar = await page.evaluate(() => (window as unknown as W).__sfTutor.nosRenderizados());
  // campo profundo, fora das páginas carregadas
  await medir(page, m, 'busca_e_revelar_campo_2999', async () => {
    await page.locator('#busca').fill('Campo2999__c');
    await page.locator('#resultados [role=option]').filter({ hasText: 'SintObj0' }).first().click();
  }, 'Campo2999__c');
  t0 = Date.now();
  await page.locator('#busca').fill('SintType1199');
  await expect(page.locator('#resultados [role=option]').first()).toContainText('SintType1199');
  m.busca_em_todo_catalogo_ms = Date.now() - t0;
  m.nos_desenhados_fim = await page.evaluate(() => (window as unknown as W).__sfTutor.nosRenderizados());
  // #42: arrastar o centro move todos os nós desenhados (todos são descendentes); 12 passos de mouse
  await page.keyboard.press('Escape');
  const centro = await page.evaluate(() => (window as unknown as { __sfTutor: { ponto(a: { no?: string }): { x: number; y: number } | null } }).__sfTutor.ponto({ no: 'salesforce' }));
  if (centro) {
    const t2 = Date.now();
    await page.mouse.move(centro.x, centro.y);
    await page.mouse.down();
    for (let i = 1; i <= 12; i++) await page.mouse.move(centro.x + i * 8, centro.y + i * 5);
    await page.mouse.up();
    m.arrastar_centro_12_passos_ms = Date.now() - t2;
    m.nos_movidos_no_arraste = (m.nos_desenhados_fim as number) - 1;
  }
  gravar('sintetico', m);
  expect(m.carga_ate_interativo_ms as number).toBeLessThan(20_000);
  expect(m.nos_desenhados_fim as number).toBeLessThan(400); // expansão progressiva: nunca desenha o catálogo inteiro
});
