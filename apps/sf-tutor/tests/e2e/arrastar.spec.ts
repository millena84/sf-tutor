// #42 (arrastar leva a subárvore) e #18 (posições guardadas por visão; "Reorganizar").
import { expect, test, type Page } from '@playwright/test';
import { abrir, painel, titulo } from './ajuda';
import { errosDaPagina } from './ajuda';
test.afterEach(async ({ page }) => {
  expect(errosDaPagina(page), 'erros de JavaScript durante o teste').toEqual([]);
});

type Gancho = { posicao(id: string): { x: number; y: number } | null; chaveDe(id: string): string | null; ponto(a: { no?: string }): { x: number; y: number } | null; gaveta(): string };
const t = (page: Page) => ({
  pos: (id: string) => page.evaluate((i) => (window as unknown as { __sfTutor: Gancho }).__sfTutor.posicao(i), id),
  ponto: (id: string) => page.evaluate((i) => { const g = (window as unknown as { __sfTutor: Gancho }).__sfTutor; const c = g.chaveDe(i); return c ? g.ponto({ no: c }) : null; }, id),
  gaveta: () => page.evaluate(() => (window as unknown as { __sfTutor: Gancho }).__sfTutor.gaveta()),
});

async function arrastar(page: Page, id: string, dx: number, dy: number, shift = false): Promise<void> {
  const p = (await t(page).ponto(id))!;
  if (shift) await page.keyboard.down('Shift');
  await page.mouse.move(p.x, p.y);
  await page.mouse.down();
  for (let i = 1; i <= 6; i++) await page.mouse.move(p.x + (dx * i) / 6, p.y + (dy * i) / 6);
  await page.mouse.up();
  if (shift) await page.keyboard.up('Shift');
}

// Ramo usado: funcionalidade (pai arrastado) → metadata type e objeto (filhos, último nó do mapa).
const PAI = 'func:named-credentials', FILHO = 'mdt:NamedCredential', AVO = 'sub:credenciais';

async function prepararRamo(page: Page): Promise<void> {
  await abrir(page, `?n=${PAI}`);
  await painel(page).getByRole('button', { name: /^Expandir/ }).click();
  await expect(titulo(page)).toContainText('Named credentials');
  await page.locator('#btn-animacao').click(); // desliga animações: posições estáveis para medir
  await page.waitForTimeout(400);
}

const perto = (a: number, b: number) => Math.abs(a - b) < 0.6;

test('arrastar leva os filhos; relação técnica e pai ficam; Shift move só o nó; posição volta após trocar de visão; Reorganizar desfaz', async ({ page, isMobile }) => {
  test.skip(isMobile, 'versão desktop');
  await prepararRamo(page);
  const T = t(page);
  const [p0, c0, o0, f0] = await Promise.all([PAI, FILHO, 'salesforce', AVO].map((i) => T.pos(i)));
  expect(p0 && c0 && o0 && f0).toBeTruthy();
  await arrastar(page, PAI, 140, 90);
  const p1 = (await T.pos(PAI))!;
  const c1 = (await T.pos(FILHO))!;
  const dx = p1.x - p0!.x, dy = p1.y - p0!.y;
  expect(Math.hypot(dx, dy)).toBeGreaterThan(40);
  expect(perto(c1.x - c0!.x, dx) && perto(c1.y - c0!.y, dy), 'filho acompanha o mesmo deslocamento').toBe(true);
  expect(await T.pos('salesforce'), 'o centro fica').toEqual(o0);
  expect(await T.pos(AVO), 'pai fica').toEqual(f0);

  // recolher e expandir de novo: os filhos voltam junto do pai arrastado, não para o lugar antigo
  await painel(page).getByRole('button', { name: /^Recolher/ }).click();
  await painel(page).getByRole('button', { name: /^Expandir/ }).click();
  await expect.poll(() => T.pos(FILHO)).toEqual(c1);

  await arrastar(page, PAI, -80, 60, true);
  const p2 = (await T.pos(PAI))!;
  expect(Math.hypot(p2.x - p1.x, p2.y - p1.y)).toBeGreaterThan(30);
  expect(await T.pos(FILHO), 'com Shift o filho fica').toEqual(c1);

  await page.locator('[data-visao=nuvem]').click();
  await page.locator('[data-visao=funcionalidade]').click();
  await expect.poll(() => T.pos(PAI)).toEqual(p2);

  await page.getByRole('button', { name: 'Reorganizar' }).click();
  expect(await T.pos(PAI)).toEqual(p0);
  expect(await T.pos(FILHO)).toEqual(c0);
});

test('celular: arrastar move o ramo e não mexe na gaveta', async ({ page, isMobile }) => {
  test.skip(!isMobile, 'versão celular');
  await prepararRamo(page);
  const T = t(page);
  expect(await T.gaveta()).toBe('meio');
  const c0 = (await T.pos(FILHO))!;
  await arrastar(page, PAI, 40, -30);
  const c1 = (await T.pos(FILHO))!;
  expect(Math.hypot(c1.x - c0.x, c1.y - c0.y)).toBeGreaterThan(10);
  expect(await T.gaveta()).toBe('meio');
});
