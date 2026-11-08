import { expect, test } from '@playwright/test';
import { abrir, titulo } from './ajuda';
import { errosDaPagina } from './ajuda';
test.afterEach(async ({ page }) => {
  expect(errosDaPagina(page), 'erros de JavaScript durante o teste').toEqual([]);
});


test.describe('360px', () => {
  test.skip(({ isMobile }) => !isMobile, 'somente no projeto mobile');
  test('sem rolagem horizontal; painel vira gaveta com "Voltar ao mapa"', async ({ page }) => {
    await abrir(page);
    const largura = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(largura).toBeLessThanOrEqual(360);
    await page.screenshot({ path: 'tests/resultados/mobile-inicio.png' });
    await page.locator('#busca').fill('ProfileId');
    await page.locator('#resultados [role=option]').filter({ hasText: 'User' }).first().click();
    await expect(page.locator('#painel')).toHaveClass(/aberto/);
    await expect(titulo(page)).toHaveText('ProfileId');
    await page.waitForTimeout(400);
    await page.screenshot({ path: 'tests/resultados/mobile-painel.png' });
    await page.getByRole('button', { name: 'Voltar ao mapa' }).click();
    await expect(page.locator('#painel')).not.toHaveClass(/aberto/);
    await page.screenshot({ path: 'tests/resultados/mobile-mapa.png' });
  });
  test('alvos de toque com ao menos 36px nos controles principais', async ({ page }) => {
    await abrir(page);
    for (const sel of ['[data-visao=nuvem]', '[data-modo=lista]', '#btn-enquadrar', '#btn-zoom-mais']) {
      const b = await page.locator(sel).boundingBox();
      expect(b!.height, sel).toBeGreaterThanOrEqual(36);
    }
  });
});
