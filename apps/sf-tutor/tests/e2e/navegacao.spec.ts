import { expect, test } from '@playwright/test';
import { abrir, painel, secao, selecao, semErroNoPainel, titulo } from './ajuda';
import { errosDaPagina } from './ajuda';
test.afterEach(async ({ page }) => {
  expect(errosDaPagina(page), 'erros de JavaScript durante o teste').toEqual([]);
});


test('deep link reabre o item e voltar/avançar do navegador funcionam', async ({ page }) => {
  await abrir(page, '?n=obj:User');
  await expect(titulo(page)).toHaveText('User');
  await abrir(page, '?n=obj:Profile');
  await page.goBack();
  await expect(titulo(page)).toHaveText('User');
  await page.goForward();
  await expect(titulo(page)).toHaveText('Profile');
});

test('deep link com caminho preserva o contexto; id inexistente cai no centro sem erro', async ({ page }) => {
  await abrir(page, '?v=nuvem&n=func:apps-de-console&c=salesforce%3Enuv%3Aservice-cloud%3Ecls%3Ainterface-e-experiencia-do-usuario%3Esub%3Aaplicativos-e-navegacao%3Efunc%3Aapps-de-console');
  expect(await selecao(page)).toContain('nuv:service-cloud');
  // caminho inventado é ignorado: abre o item pelo caminho preferido, sem erro
  await abrir(page, '?v=nuvem&n=func:apps-de-console&c=salesforce%3Enuv%3Aservice-cloud%3Efunc%3Aapps-de-console');
  expect(await selecao(page)).toMatch(/>func:apps-de-console$/);
  await abrir(page, '?n=obj:NaoExiste');
  expect(await selecao(page)).toBe('salesforce');
});

test('busca abre um campo que ainda não estava carregado no mapa', async ({ page }) => {
  await abrir(page);
  const antes = await page.evaluate(() => (window as unknown as { __sfTutor: { nosRenderizados(): number } }).__sfTutor.nosRenderizados());
  await page.locator('#busca').fill('AssigneeId');
  await page.keyboard.press('ArrowDown');
  await page.keyboard.press('Enter');
  await expect(titulo(page)).toHaveText('AssigneeId');
  expect(await selecao(page)).toMatch(/obj:PermissionSetAssignment>obj:PermissionSetAssignment\.AssigneeId$/);
  const depois = await page.evaluate(() => (window as unknown as { __sfTutor: { nosRenderizados(): number } }).__sfTutor.nosRenderizados());
  expect(depois).toBeGreaterThan(antes);
});

test('expandir, paginar e recolher pelo painel', async ({ page }) => {
  await abrir(page, '?n=obj:User');
  const qtd = () => page.evaluate(() => (window as unknown as { __sfTutor: { nosRenderizados(): number } }).__sfTutor.nosRenderizados());
  const a = await qtd();
  await painel(page).getByRole('button', { name: /^Expandir \(\d+ itens\)/ }).click();
  const b = await qtd();
  expect(b).toBeGreaterThanOrEqual(a + 24); // 1ª página de campos + nó "mais"
  await page.getByRole('button', { name: /^Recolher/ }).click();
  expect(await qtd()).toBe(a);
});

test('troca de visão mantém o item selecionado quando ele existe na outra visão', async ({ page }) => {
  await abrir(page, '?n=mdt:FlexiPage');
  await page.locator('[data-visao=nuvem]').click();
  await expect(titulo(page)).toHaveText('FlexiPage');
  expect(await selecao(page)).toMatch(/^salesforce>nuv:/);
});

test('modo lista navegável só por teclado', async ({ page }) => {
  await abrir(page, '?m=lista');
  const arvore = page.getByRole('tree');
  await expect(arvore).toBeVisible();
  await arvore.getByRole('treeitem').first().focus();
  await page.keyboard.press('ArrowDown');
  const foco = page.locator(':focus');
  await expect(foco).toHaveAttribute('role', 'treeitem');
  const nome = (await foco.getAttribute('data-chave'))!;
  await page.keyboard.press('ArrowRight'); // expande
  await expect(page.locator(`[data-chave="${nome}"]`)).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('ArrowRight'); // vai para o 1º filho
  await page.keyboard.press('Enter'); // seleciona
  await expect(titulo(page)).toBeVisible();
  expect((await selecao(page))!.startsWith(nome + '>')).toBe(true);
  await page.keyboard.press('ArrowLeft'); // volta ao pai
  await expect(page.locator(':focus')).toHaveAttribute('data-chave', nome);
});

test('filtros esmaecem e explicam o motivo, sem apagar o item', async ({ page }) => {
  await abrir(page, '?m=lista&n=func:usuarios');
  await page.getByRole('button', { name: /^Filtros/ }).click();
  await page.getByRole('dialog').getByRole('checkbox', { name: /Data 360/ }).check();
  await page.getByRole('dialog').getByRole('button', { name: 'Fechar' }).click();
  await expect(page.getByRole('button', { name: /^Filtros \(1\)/ })).toBeVisible();
  const item = page.locator('[data-chave$="func:usuarios"]');
  await expect(item).toHaveClass(/oculto/);
  await expect(item).toContainText('esmaecido');
});

test('painéis de cada tipo de nó abrem sem erro', async ({ page }) => {
  const ids = ['salesforce', 'nuv:sales-cloud', 'cls:acesso-identidade-e-seguranca', 'sub:permissoes-perfis-e-grupos', 'func:permission-sets',
    'mdt:PermissionSet', 'mdx:AssignmentRules_RuleEntry', 'mdt:PermissionSet.applicationVisibilities', 'obj:PermissionSetAssignment', 'obj:User.ProfileId'];
  for (const id of ids) {
    await abrir(page, `?n=${encodeURIComponent(id)}`);
    await expect(titulo(page), id).not.toBeEmpty();
    expect(await selecao(page), id).toMatch(new RegExp(`${id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`));
    await semErroNoPainel(page);
  }
});

test('Método e legenda acessíveis; logo marcado como placeholder', async ({ page }) => {
  await abrir(page);
  await expect(painel(page).locator('.aviso-logo')).toContainText('não é afiliado');
  await page.getByRole('button', { name: 'Método', exact: true }).click();
  await expect(page.getByRole('dialog')).toContainText('não é afiliado');
  await page.getByRole('dialog').getByRole('button', { name: 'Fechar' }).click();
  await page.getByRole('button', { name: 'Legenda' }).click();
  await expect(page.getByRole('dialog')).toBeVisible();
});

test('capturas de tela desktop', async ({ page }) => {
  await abrir(page);
  await page.waitForTimeout(600);
  await page.screenshot({ path: 'tests/resultados/desktop-inicio.png' });
  await abrir(page, '?n=obj:User.ProfileId');
  await page.waitForTimeout(800);
  await page.screenshot({ path: 'tests/resultados/desktop-campo.png' });
  await abrir(page, '?v=nuvem&n=func:apps-de-console');
  await page.waitForTimeout(800);
  await page.screenshot({ path: 'tests/resultados/desktop-nuvem.png' });
});

type WLogo = { __sfTutor: { logo(id: string): string | null } };
const SFDC = /sfdcstatic\.com|sfdcdigital\.com/;

test('logos oficiais carregam por referência (servidores simulados)', async ({ page }) => {
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><circle cx="5" cy="5" r="5" fill="#00a1e0"/></svg>';
  await page.route(SFDC, (r) => r.fulfill({ status: 200, contentType: 'image/svg+xml', body: svg }));
  await abrir(page, '?n=nuv:sales-cloud');
  await expect.poll(() => page.evaluate(() => (window as unknown as WLogo).__sfTutor.logo('salesforce'))).toBe('ok');
  await expect.poll(() => page.evaluate(() => (window as unknown as WLogo).__sfTutor.logo('nuv:sales-cloud'))).toBe('ok');
  await expect(painel(page).locator('img.logo-marca')).toBeVisible();
  await expect(painel(page).locator('details.secao', { hasText: 'Fornecido por' })).toHaveCount(1);
});

test('logo SVG sem largura/altura declaradas cabe dentro do nó central', async ({ page }) => {
  // caso real relatado: a nuvem da Salesforce saía maior que o nó
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 92 64"><ellipse cx="46" cy="32" rx="46" ry="32" fill="#00a1e0"/></svg>';
  await page.route(SFDC, (r) => r.fulfill({ status: 200, contentType: 'image/svg+xml', body: svg }));
  await abrir(page);
  await expect.poll(() => page.evaluate(() => (window as unknown as WLogo).__sfTutor.logo('salesforce'))).toBe('ok');
  type Caixas = { no: DOMRect; img: DOMRect } | null;
  const caixas = async () => page.evaluate(() => (window as unknown as { __sfTutor: { caixasLogo(id: string): Caixas } }).__sfTutor.caixasLogo('salesforce'));
  await expect.poll(async () => (await caixas()) !== null).toBe(true);
  for (const z of ['inicio', 'zoom']) {
    if (z === 'zoom') { await page.getByRole('button', { name: 'Aproximar' }).click(); await page.waitForTimeout(500); }
    const c = (await caixas())!;
    expect(c.img.width, z).toBeLessThan(c.no.width);
    expect(c.img.left, z).toBeGreaterThanOrEqual(c.no.left - 1);
    expect(c.img.right, z).toBeLessThanOrEqual(c.no.right + 1);
    expect(c.img.top, z).toBeGreaterThanOrEqual(c.no.top - 1);
    expect(c.img.bottom, z).toBeLessThanOrEqual(c.no.bottom + 1);
  }
  await page.screenshot({ path: 'tests/resultados/logo-central.png' });
});

test('sem acesso aos servidores dos logos, o mapa usa o substituto sem erro', async ({ page }) => {
  await page.route(SFDC, (r) => r.abort());
  await abrir(page, '?n=salesforce');
  await expect.poll(() => page.evaluate(() => (window as unknown as WLogo).__sfTutor.logo('salesforce'))).toBe('falhou');
  await expect(painel(page).locator('img.logo-marca')).toHaveCount(0);
});

test('funcionalidade sem metadata type mostra código e recursos de API', async ({ page }) => {
  await abrir(page, '?n=func:limites-de-api-e-alocacoes');
  await expect(titulo(page)).toHaveText('Limites de API e alocações');
  const rep = await secao(page, /Representações técnicas/);
  await expect(rep.getByRole('heading', { name: 'Código e recursos de API' })).toBeVisible();
  await expect(rep.getByText(/\/services\/data\/vXX\.X\/limits\//)).toBeVisible();
  await expect(rep.getByRole('heading', { name: /Sem metadata type \(XML\)/ })).toBeVisible();
});

test('funcionalidade de integração mostra caminho de Setup verificado', async ({ page }) => {
  await abrir(page, '?n=func:event-relay');
  await expect(titulo(page)).toHaveText(/Event Relay/);
  await expect(painel(page).getByText(/Quick Find: Event Relays > New Event Relay/)).toBeVisible();
});
