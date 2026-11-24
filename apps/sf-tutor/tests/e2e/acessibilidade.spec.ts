// #19: varredura automática de acessibilidade com axe-core (WCAG 2.0, 2.1 e 2.2 nível AA) nos estados principais,
// em desktop e em 360px. Falha em qualquer violação; a lista mostra regra, gravidade e elementos.
// O mapa é desenhado em canvas, que o axe não lê; a alternativa textual é o modo Lista, coberto aqui.
import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';
import { abrir } from './ajuda';

const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];

async function varrer(page: Page, contexto?: string) {
  let b = new AxeBuilder({ page }).withTags(TAGS);
  if (contexto) b = b.include(contexto);
  const r = await b.analyze();
  const resumo = r.violations.map((v) => `${v.id} (${v.impact}): ${v.help} — ${v.nodes.slice(0, 3).map((n) => n.target.join(' ')).join(' | ')}`);
  expect(resumo, 'violações de acessibilidade').toEqual([]);
}

const FICHAS: [string, string][] = [
  ['início', ''],
  ['funcionalidade', '?n=func:permission-sets'],
  ['metadata type', '?n=mdt:Flow'],
  ['objeto', '?n=obj:User'],
  ['tema', '?n=sub:vendas'],
  ['nuvem', '?n=nuv:mulesoft'],
];

for (const [nome, q] of FICHAS) {
  test(`sem violações AA: ${nome}`, async ({ page }) => {
    await abrir(page, q);
    await varrer(page);
  });
}

test('sem violações AA: busca aberta', async ({ page }) => {
  await abrir(page, '');
  await page.locator('#busca').fill('PermissionSet');
  await expect(page.locator('#resultados [role=option]').first()).toBeVisible();
  await varrer(page);
});

test('sem violações AA: modo lista', async ({ page }) => {
  await abrir(page, '');
  await page.locator('[data-modo=lista]').click();
  await varrer(page);
});

// Nas janelas, a varredura fica restrita ao diálogo: o fundo escurecido atrás dele impede o axe de medir o contraste da página.
const JANELAS: [string, string, (p: Page) => Promise<void>][] = [
  ['janela de campos', '?n=obj:User', async (p) => { await p.getByRole('button', { name: /^Ver \d+ campos em tabela/ }).first().click(); }],
  ['Método', '', async (p) => { await p.locator('#btn-metodo').click(); }],
  ['Legenda', '', async (p) => { await p.locator('#btn-legenda').click(); }],
  ['Filtros', '', async (p) => { await p.locator('#btn-filtros').click(); }],
];

for (const [nome, q, abrirJanela] of JANELAS) {
  test(`sem violações AA: ${nome}`, async ({ page }) => {
    await abrir(page, q);
    await abrirJanela(page);
    await expect(page.locator('dialog[open]').first()).toBeVisible();
    await varrer(page, 'dialog[open]');
  });
}

test('sem violações AA: janela Reportar erro e Novidades', async ({ page }) => {
  await abrir(page, '?n=mdt:Flow');
  await page.locator('#conteudo-painel').getByRole('button', { name: 'Reportar erro' }).first().click();
  await expect(page.locator('#dialogo-reporte')).toBeVisible();
  await varrer(page, '#dialogo-reporte');
  await page.keyboard.press('Escape');
  await page.getByRole('button', { name: 'Novidades' }).click();
  await expect(page.locator('#dialogo')).toBeVisible();
  await varrer(page, '#dialogo');
});
