// Regressão do destaque (issue #22): o realce do nó, dos vizinhos e do caminho até o centro precisa sobreviver a qualquer refatoração do painel.
import { expect, test, type Page } from '@playwright/test';
import { abrir, painel, secao, titulo } from './ajuda';
import { errosDaPagina } from './ajuda';
test.afterEach(async ({ page }) => {
  expect(errosDaPagina(page), 'erros de JavaScript durante o teste').toEqual([]);
});

const classes = (page: Page, id: string) =>
  page.evaluate((i) => (window as unknown as { __sfTutor: { classes(id: string): string[] | null } }).__sfTutor.classes(i), id);

test('navegar por link do painel mantém foco, vizinhos, caminho e esmaecimento', async ({ page }) => {
  await abrir(page, '?n=func:named-credentials');
  await expect(titulo(page)).toHaveText(/Named credentials/i);
  const rep = await secao(page, /Representações técnicas/);
  await rep.getByRole('button', { name: 'NamedCredential', exact: true }).first().click();
  await expect(titulo(page)).toHaveText('NamedCredential');
  await expect.poll(() => classes(page, 'mdt:NamedCredential')).toContain('foco');
  expect(await classes(page, 'func:named-credentials')).toContain('vizinho');
  expect(await classes(page, 'salesforce')).toContain('vizinho');
  expect(await classes(page, 'cls:dados-e-modelagem')).toContain('esmaecido');
  await expect(painel(page)).toBeVisible();
});
