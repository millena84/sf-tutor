import { expect, test } from '@playwright/test';
import { abrir, painel, titulo } from './ajuda';
import { errosDaPagina } from './ajuda';
test.afterEach(async ({ page }) => {
  expect(errosDaPagina(page), 'erros de JavaScript durante o teste').toEqual([]);
});


test.describe('360px', () => {
  test.skip(({ isMobile }) => !isMobile, 'somente no projeto mobile');
  test('sem rolagem horizontal; painel vira gaveta em meia altura com "Voltar ao mapa"', async ({ page }) => {
    await abrir(page);
    const largura = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(largura).toBeLessThanOrEqual(360);
    await page.screenshot({ path: 'tests/resultados/mobile-inicio.png' });
    await page.locator('#busca').fill('ProfileId');
    await page.locator('#resultados [role=option]').filter({ hasText: 'User' }).first().click();
    await expect(page.locator('#painel')).toHaveClass(/aberto/);
    await expect(page.locator('#painel')).toHaveAttribute('data-estado', 'meio');
    // o campo abre na tabela do objeto, numa janela que cabe na tela
    await expect(titulo(page)).toHaveText('User');
    await expect(page.locator('#dialogo tr.linha-item.aberta')).toHaveAttribute('data-id', 'obj:User.ProfileId');
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(360);
    await page.screenshot({ path: 'tests/resultados/mobile-tabela.png' });
    await page.locator('#dialogo').getByRole('button', { name: 'Fechar' }).click();
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
  test('gaveta em meia altura: mapa visível acima, nó centralizado na área livre; puxador abre e reduz a ficha', async ({ page }) => {
    await abrir(page, '?n=func:named-credentials');
    const gav = page.locator('#painel');
    await expect(gav).toHaveAttribute('data-estado', 'meio');
    await page.waitForTimeout(500);
    const topoGaveta = (await gav.boundingBox())!.y;
    const ponto = async (id: string) => page.evaluate((i) => {
      const t = (window as unknown as { __sfTutor: { chaveDe(id: string): string | null; ponto(a: { no?: string }): { x: number; y: number } | null } }).__sfTutor;
      const c = t.chaveDe(i); return c ? t.ponto({ no: c }) : null;
    }, id);
    const p1 = (await ponto('func:named-credentials'))!;
    expect(p1.y, 'nó acima da gaveta').toBeLessThan(topoGaveta);
    expect(p1.y).toBeGreaterThan(60);
    await expect(painel(page).getByRole('button', { name: 'Mostrar no mapa' })).toBeHidden();
    // navegar por link do painel move o mapa até o novo nó, que continua visível acima da gaveta
    await painel(page).getByRole('button', { name: 'NamedCredential', exact: true }).first().click();
    await expect(titulo(page)).toHaveText('NamedCredential');
    await page.waitForTimeout(500);
    expect((await ponto('mdt:NamedCredential'))!.y).toBeLessThan(topoGaveta);
    // puxador: altura cheia mostra "Mostrar no mapa", que volta para meia altura
    await page.getByRole('button', { name: 'Ver ficha completa' }).click();
    await expect(gav).toHaveAttribute('data-estado', 'cheio');
    await painel(page).getByRole('button', { name: 'Mostrar no mapa' }).click();
    await expect(gav).toHaveAttribute('data-estado', 'meio');
    await page.waitForTimeout(500);
    expect((await ponto('mdt:NamedCredential'))!.y).toBeLessThan((await gav.boundingBox())!.y);
    await page.screenshot({ path: 'tests/resultados/mobile-meia-altura.png' });
  });
});
