// #147: cartão de boas-vindas na primeira visita e tour guiado de 6 passos (desktop e 360 px).
import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';
import { abrir, errosDaPagina } from './ajuda';

test.afterEach(async ({ page }) => {
  expect(errosDaPagina(page), 'erros de JavaScript durante o teste').toEqual([]);
});

const balao = (page: Page) => page.locator('#tour-balao');
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];

async function semViolacoes(page: Page, seletor: string) {
  const r = await new AxeBuilder({ page }).withTags(TAGS).include(seletor).analyze();
  expect(r.violations.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).join(' | ')}`)).toEqual([]);
}

/** O balão cabe inteiro na tela. */
async function dentroDaTela(page: Page) {
  const caixa = await balao(page).boundingBox();
  const vp = page.viewportSize()!;
  expect(caixa).not.toBeNull();
  expect(caixa!.x).toBeGreaterThanOrEqual(0);
  expect(caixa!.y).toBeGreaterThanOrEqual(0);
  expect(caixa!.x + caixa!.width).toBeLessThanOrEqual(vp.width + 1);
  expect(caixa!.y + caixa!.height).toBeLessThanOrEqual(vp.height + 1);
}

test('primeira visita: boas-vindas, tour completo pelos 6 passos e não volta a aparecer', async ({ page }) => {
  await abrir(page, '', { tourVisto: false });
  const bv = page.locator('#boas-vindas');
  await expect(bv).toBeVisible();
  await expect(bv.getByRole('heading', { name: 'Boas-vindas ao Metadata Desbugado' })).toBeVisible();
  await expect(page.locator('#btn-fazer-tour')).toBeFocused();
  await semViolacoes(page, '#boas-vindas');

  await page.locator('#btn-fazer-tour').click();
  await expect(bv).toHaveCount(0);
  await expect(balao(page)).toBeVisible();
  await expect(page.locator('#tour-contador')).toHaveText('Passo 1 de 6');
  await expect(page.locator('#tour-titulo')).toBeFocused();
  await expect(page.locator('#tour-voltar')).toBeDisabled();
  await expect(page.locator('.segmento[aria-label="Visão"]')).toHaveClass(/tour-alvo/);
  await semViolacoes(page, '#tour-balao');
  await dentroDaTela(page);

  // passo 2: seleciona um exemplo real no mapa
  await page.locator('#tour-proximo').click();
  await expect(page.locator('#tour-contador')).toHaveText('Passo 2 de 6');
  await expect.poll(() => page.evaluate(() => (window as unknown as { __sfTutor: { selecao(): string | null } }).__sfTutor.selecao()))
    .toMatch(/cls:acesso-identidade-e-seguranca$/);
  await dentroDaTela(page);

  // passo 3: ficha
  await page.locator('#tour-proximo').click();
  await expect(page.locator('#tour-contador')).toHaveText('Passo 3 de 6');
  await expect(page.locator('#painel')).toHaveClass(/tour-alvo/);
  await dentroDaTela(page);

  // passo 4: tabela de propriedades do PermissionSet
  await page.locator('#tour-proximo').click();
  await expect(page.locator('#tour-contador')).toHaveText('Passo 4 de 6');
  await expect(page.locator('#titulo-painel')).toHaveText('PermissionSet');
  await expect(page.locator('#conteudo-painel .btn-tabela')).toHaveClass(/tour-alvo/);
  await dentroDaTela(page);

  // passo 5: busca
  await page.locator('#tour-proximo').click();
  await expect(page.locator('#busca')).toHaveClass(/tour-alvo/);
  await dentroDaTela(page);

  // voltar funciona
  await page.locator('#tour-voltar').click();
  await expect(page.locator('#tour-contador')).toHaveText('Passo 4 de 6');
  await page.locator('#tour-proximo').click();

  // passo 6: reportar erro, e concluir
  await page.locator('#tour-proximo').click();
  await expect(page.locator('#tour-contador')).toHaveText('Passo 6 de 6');
  await expect(page.locator('#conteudo-painel .btn-reportar').first()).toHaveClass(/tour-alvo/);
  await expect(page.locator('#tour-proximo')).toHaveText('Concluir');
  await dentroDaTela(page);
  await page.locator('#tour-proximo').click();
  await expect(balao(page)).toHaveCount(0);
  await expect(page.locator('.tour-alvo')).toHaveCount(0);

  // lembrado: ao recarregar, o cartão não volta
  expect(await page.evaluate(() => localStorage.getItem('metadata-desbugado:tour-visto'))).toBe('1');
  await page.reload();
  await page.waitForFunction(() => (window as unknown as { __sfTutor?: { pronto: boolean } }).__sfTutor?.pronto === true);
  await expect(page.locator('#boas-vindas')).toHaveCount(0);
});

test('Pular fecha o cartão, devolve o foco ao mapa e lembra a escolha', async ({ page }) => {
  await abrir(page, '', { tourVisto: false });
  await page.locator('#btn-pular-tour').click();
  await expect(page.locator('#boas-vindas')).toHaveCount(0);
  await expect(balao(page)).toHaveCount(0);
  await expect(page.locator('#mapa')).toBeFocused();
  expect(await page.evaluate(() => localStorage.getItem('metadata-desbugado:tour-visto'))).toBe('1');
});

test('link direto não mostra o cartão de boas-vindas', async ({ page }) => {
  await abrir(page, '?n=mdt:Flow', { tourVisto: false });
  await expect(page.locator('#titulo-painel')).toHaveText('Flow');
  await expect(page.locator('#boas-vindas')).toHaveCount(0);
});

test('rever o tour pelo rodapé e pelo Método; Esc sai do tour', async ({ page }) => {
  await abrir(page);
  await expect(page.locator('#boas-vindas')).toHaveCount(0);
  await page.locator('#btn-tour').click();
  await expect(page.locator('#tour-contador')).toHaveText('Passo 1 de 6');
  await page.keyboard.press('Escape');
  await expect(balao(page)).toHaveCount(0);

  await page.locator('#btn-metodo').click();
  await page.locator('#btn-tour-metodo').click();
  await expect(page.locator('#dialogo')).not.toBeVisible();
  await expect(page.locator('#tour-contador')).toHaveText('Passo 1 de 6');
  await page.locator('#tour-sair').click();
  await expect(balao(page)).toHaveCount(0);
});

test('sem armazenamento local, o cartão aparece e o tour funciona sem erro', async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', { get() { throw new Error('bloqueado'); } });
  });
  await abrir(page, '', { tourVisto: false });
  await expect(page.locator('#boas-vindas')).toBeVisible();
  await page.locator('#btn-pular-tour').click();
  await expect(page.locator('#boas-vindas')).toHaveCount(0);
});
