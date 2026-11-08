import { expect, type Page } from '@playwright/test';

const erros = new WeakMap<Page, string[]>();

/** Erros de JavaScript da página durante todo o teste (não só na carga). */
export const errosDaPagina = (page: Page): string[] => erros.get(page) ?? [];

export async function abrir(page: Page, consulta = ''): Promise<void> {
  if (!erros.has(page)) {
    const lista: string[] = [];
    erros.set(page, lista);
    page.on('pageerror', (e) => lista.push(e.message));
  }
  await page.goto(`/${consulta}`);
  await page.waitForFunction(() => (window as unknown as { __sfTutor?: { pronto: boolean } }).__sfTutor?.pronto === true, null, { timeout: 20_000 });
  expect(errosDaPagina(page), 'erros de JavaScript na carga').toEqual([]);
}

export const titulo = (page: Page) => page.locator('#titulo-painel');
export const painel = (page: Page) => page.locator('#conteudo-painel');
export const selecao = (page: Page) => page.evaluate(() => (window as unknown as { __sfTutor: { selecao(): string | null } }).__sfTutor.selecao());

export async function buscarEAbrir(page: Page, termo: string, textoResultado: RegExp): Promise<void> {
  await page.locator('#busca').fill(termo);
  const r = page.locator('#resultados [role=option]').filter({ hasText: textoResultado }).first();
  await expect(r).toBeVisible();
  await r.click();
}

/** Abre uma seção <details> do painel pelo título (se estiver fechada). */
export async function secao(page: Page, tituloSecao: RegExp) {
  const d = painel(page).locator('details.secao').filter({ has: page.locator('summary', { hasText: tituloSecao }) }).first();
  await expect(d).toBeVisible();
  if (!(await d.getAttribute('open') !== null)) await d.locator('summary').click();
  return d;
}

export async function semErroNoPainel(page: Page): Promise<void> {
  await expect(painel(page).locator('.erro')).toHaveCount(0);
}
