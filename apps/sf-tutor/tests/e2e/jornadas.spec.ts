// As 7 jornadas obrigatórias do prompt da tarefa 2, sobre os dados reais (public/data copiado de gerado/site).
import { expect, test } from '@playwright/test';
import { abrir, buscarEAbrir, painel, secao, selecao, semErroNoPainel, titulo } from './ajuda';
import { errosDaPagina } from './ajuda';
test.afterEach(async ({ page }) => {
  expect(errosDaPagina(page), 'erros de JavaScript durante o teste').toEqual([]);
});


test('1. User: campos do objeto, sem XML inventado', async ({ page }) => {
  await abrir(page, '?n=func:usuarios');
  await expect(titulo(page)).toHaveText('Usuários');
  const rep = await secao(page, /Representações técnicas/);
  await expect(rep.getByRole('heading', { name: /Sem metadata type \(XML\)/ })).toBeVisible();
  await expect(rep.getByRole('heading', { name: 'Metadata types (XML)' })).toHaveCount(0);
  await rep.getByRole('button', { name: 'User', exact: true }).click();
  await expect(titulo(page)).toHaveText('User');
  expect(await selecao(page)).toMatch(/func:usuarios>obj:User$/);
  await expect(painel(page).locator('summary', { hasText: 'Arquivo no projeto Salesforce' })).toHaveCount(0);
  // o objeto é o último nó: os campos abrem em tabela, numa janela
  const bloco = painel(page).locator('.bloco-tabela');
  const n = Number((await bloco.locator('h3').textContent())!.match(/\((\d+)\)/)![1]);
  expect(n).toBeGreaterThan(100);
  await bloco.getByRole('button', { name: /^Ver \d+ campos em tabela/ }).click();
  const janela = page.locator('#dialogo');
  await expect(janela).toBeVisible();
  await expect(page.locator('#dialogo-titulo')).toContainText('Campos de User');
  await expect(janela.locator('tr.linha-item')).toHaveCount(n);
  await expect(page).toHaveURL(/t=obj%3AUser/);
  await janela.getByRole('searchbox').fill('Username');
  await janela.getByRole('button', { name: 'Username', exact: true }).click();
  await expect(janela.locator('tr.linha-detalhe:not([hidden])')).toContainText('Nome técnico');
  await expect(titulo(page), 'a seleção no mapa continua no objeto').toHaveText('User');
  expect(await selecao(page)).toMatch(/func:usuarios>obj:User$/);
  await expect(janela.locator('.erro')).toHaveCount(0);
  await janela.getByRole('button', { name: 'Fechar' }).click();
  await expect(janela).toBeHidden();
  await expect(page).not.toHaveURL(/t=obj/);
  await semErroNoPainel(page);
});

test('2. PermissionSet: metadata type XML e objeto API são itens distintos', async ({ page }) => {
  await abrir(page);
  await page.locator('#busca').fill('PermissionSet');
  const opcoes = page.locator('#resultados [role=option]');
  await expect(opcoes.filter({ hasText: /Metadata type/ }).filter({ hasText: /^.*PermissionSet/ }).first()).toBeVisible();
  await expect(opcoes.filter({ hasText: /Objeto/ }).first()).toBeVisible();
  await page.keyboard.press('Escape');
  await abrir(page, '?n=func:permission-sets');
  const rep = await secao(page, /Representações técnicas/);
  await expect(rep.getByRole('heading', { name: 'Metadata types (XML)' })).toBeVisible();
  await expect(rep.getByRole('heading', { name: 'Objetos consultáveis via API' })).toBeVisible();
  await rep.getByRole('button', { name: 'PermissionSet', exact: true }).first().click();
  expect(await selecao(page)).toMatch(/>mdt:PermissionSet$/);
  await expect(painel(page).locator('summary', { hasText: 'Arquivo no projeto Salesforce' })).toBeVisible();
  await expect(painel(page).locator('.bloco-tabela h3', { hasText: /^Propriedades XML \(\d+\)/ })).toBeVisible();
  await abrir(page, '?n=obj:PermissionSet');
  await expect(titulo(page)).toHaveText('PermissionSet');
  await expect(painel(page).locator('.bloco-tabela h3', { hasText: /^Campos \(\d+\)/ })).toBeVisible();
  await expect(painel(page).locator('summary', { hasText: 'APIs de acesso e operações' })).toBeVisible();
  await semErroNoPainel(page);
});

test('3. User → PermissionSetAssignment → PermissionSet / PermissionSetGroup', async ({ page }) => {
  await abrir(page, '?n=obj:User');
  const rel = await secao(page, /Relações técnicas/);
  await rel.getByRole('button', { name: 'PermissionSetAssignment.AssigneeId' }).click();
  // o campo leva ao objeto que o contém, com a tabela aberta na linha dele
  await expect(titulo(page)).toHaveText('PermissionSetAssignment');
  const janela = page.locator('#dialogo');
  await expect(janela.locator('tr.linha-item.aberta')).toHaveAttribute('data-id', 'obj:PermissionSetAssignment.AssigneeId');
  await janela.getByRole('button', { name: 'Fechar' }).click();
  await expect(janela).toBeHidden();
  const rel2 = await secao(page, /Relações técnicas/);
  await expect(rel2.getByRole('button', { name: 'PermissionSet', exact: true })).toBeVisible();
  await expect(rel2.getByRole('button', { name: 'PermissionSetGroup', exact: true })).toBeVisible();
  // ficha da relação
  const linha = rel2.locator('li').filter({ hasText: 'PermissionSetGroupId' }).first();
  await linha.getByRole('button', { name: /por que se relacionam/ }).click();
  await expect(page).toHaveURL(/r=rel%3Apsa-permissionsetgroup/);
  await semErroNoPainel(page);
  await page.goBack();
  await expect(titulo(page)).toHaveText('PermissionSetAssignment');
});

test('4. User.ProfileId → Profile, com aresta selecionável no mapa', async ({ page, isMobile }) => {
  await abrir(page);
  await buscarEAbrir(page, 'ProfileId', /User/);
  await expect(titulo(page)).toHaveText('User');
  expect(await selecao(page)).toMatch(/>obj:User$/);
  const janela = page.locator('#dialogo');
  const linha = janela.locator('tr.linha-item.aberta');
  await expect(linha).toHaveAttribute('data-id', 'obj:User.ProfileId');
  await janela.locator('tr.linha-detalhe:not([hidden])').getByRole('button', { name: /^Profile \(abrir objeto no mapa\)/ }).click();
  await expect(janela).toBeHidden();
  await expect(titulo(page)).toHaveText('Profile');
  expect(await selecao(page)).toMatch(/>obj:Profile$/);
  test.skip(!!isMobile, 'clique na aresta testado no desktop');
  await page.getByRole('button', { name: 'Enquadrar' }).click();
  await page.waitForTimeout(900); // fim da animação de enquadramento
  const p = await page.evaluate(() => (window as unknown as { __sfTutor: { ponto(a: object): { x: number; y: number } | null } }).__sfTutor.ponto({ relId: 'rel:user-profile' }));
  expect(p, 'aresta User.ProfileId → Profile desenhada e com trecho visível').not.toBeNull();
  await page.mouse.click(p!.x, p!.y);
  await expect(titulo(page)).toContainText(/Referência|campo/i);
  await expect(painel(page)).toContainText('ProfileId');
  await expect(painel(page)).toContainText('Profile');
});

test('5. CustomObject e CustomField: comparação entre XML e objetos API', async ({ page }) => {
  await abrir(page, '?n=mdt:CustomObject');
  await expect(titulo(page)).toHaveText('CustomObject');
  const rel = await secao(page, /Relações técnicas/);
  await expect(rel).toContainText('EntityDefinition');
  await expect(rel).toContainText(/Correspond/);
  await abrir(page, '?n=mdt:CustomField');
  const rel2 = await secao(page, /Relações técnicas/);
  await expect(rel2).toContainText('FieldDefinition');
  await expect(rel2).toContainText('CustomField');
  await expect(rel2.locator('.selo-desconhecido').first()).toBeVisible(); // correspondência não verificada aparece como tal
  await rel2.locator('li').filter({ hasText: 'FieldDefinition' }).first().getByRole('button', { name: /por que se relacionam/ }).click();
  await semErroNoPainel(page);
});

test('6. FlexiPage, QuickAction e PathAssistant alcançáveis pela busca e pelo mapa', async ({ page }) => {
  await abrir(page);
  for (const nome of ['FlexiPage', 'QuickAction', 'PathAssistant']) {
    await buscarEAbrir(page, nome, new RegExp(`Metadata type`));
    await expect(titulo(page)).toHaveText(nome);
    expect(await selecao(page)).toMatch(new RegExp(`>mdt:${nome}$`));
    await expect(painel(page).locator('.migalhas li')).not.toHaveCount(0);
    await semErroNoPainel(page);
  }
});

test('7. Funcionalidade compartilhada: Sales e Service apontam para a mesma ficha', async ({ page }) => {
  await abrir(page, '?v=nuvem&n=func:apps-de-console');
  await expect(page.locator('[data-visao=nuvem]')).toHaveAttribute('aria-pressed', 'true');
  const primeiro = (await selecao(page))!;
  const outros = painel(page).locator('details.outros-caminhos');
  await outros.locator('summary').click();
  await outros.getByRole('button').first().click();
  const segundo = (await selecao(page))!;
  expect(segundo).not.toBe(primeiro);
  expect(primeiro.endsWith('func:apps-de-console') && segundo.endsWith('func:apps-de-console')).toBe(true);
  const nuvens = new Set([primeiro.split('>')[1], segundo.split('>')[1]]);
  expect(nuvens.has('nuv:sales-cloud') || nuvens.has('nuv:service-cloud')).toBe(true);
  await expect(titulo(page)).toHaveText(/console/i);
  const nuvSec = await secao(page, /Nuvens e temas/);
  await expect(nuvSec.getByRole('button', { name: 'Agentforce Sales' })).toBeVisible();
  await expect(nuvSec.getByRole('button', { name: 'Agentforce Service' })).toBeVisible();
});

test('8. Toda nuvem avisa que a lista de metadata types é parcial', async ({ page }) => {
  for (const n of ['nuv:platform-core', 'nuv:industries', 'nuv:add-ons']) {
    await abrir(page, `?v=nuvem&n=${n}`);
    const aviso = painel(page).locator('.aviso-cobertura');
    await expect(aviso).toContainText('Cobertura parcial');
    await expect(aviso).toContainText(/metadata types ligados a esta nuvem/);
    await semErroNoPainel(page);
  }
});

test('10. Reportar erro: entrevista com contexto, perguntas por situação e issue no repositório público sem o e-mail', async ({ page }) => {
  await abrir(page, '?v=funcionalidade&n=mdt:SecuritySettings');
  await painel(page).getByRole('button', { name: 'Reportar erro' }).first().click();
  const dlg = page.locator('#dialogo-reporte');
  await expect(dlg.getByRole('heading', { name: 'Reportar erro no conteúdo' })).toBeVisible();
  await expect(dlg).toContainText('Não é suporte da Salesforce');
  await expect(dlg).toContainText('mdt:SecuritySettings');
  await expect(dlg).toContainText('Status no site');
  await expect(dlg).toContainText('Não inclua dados da sua org');
  // antes de escolher, só a pergunta 1 aparece
  await expect(dlg.locator('.perguntas-seguintes')).toBeHidden();
  await expect(dlg.getByRole('button', { name: 'Abrir issue no GitHub' })).toBeHidden();

  // "É um problema na minha org" não vira reporte
  await dlg.getByText('É um problema na minha org').click();
  await expect(dlg.locator('.aviso-org')).toBeVisible();
  await expect(dlg.locator('.aviso-org')).toContainText('não são atendidos aqui');
  await expect(dlg.getByRole('button', { name: 'Enviar por e-mail' })).toBeHidden();

  // "Ficou confuso" troca as perguntas
  await dlg.getByText('Ficou confuso').click();
  await expect(dlg.locator('.aviso-org')).toBeHidden();
  await expect(dlg.getByLabel('O que ficou confuso? (obrigatório)')).toBeVisible();

  // "Está errado": sem a resposta obrigatória, nada sai
  await dlg.getByText('Está errado').click();
  await dlg.getByRole('button', { name: 'Abrir issue no GitHub' }).click();
  await expect(dlg.getByRole('status')).toContainText('Responda');
  await dlg.getByLabel('O que está escrito aqui que parece errado? (obrigatório)').fill('Teste automatizado: o default parece errado.');
  await dlg.getByLabel('Sei pela prática').check();
  await dlg.getByLabel('Usuário do GitHub').fill('@teste');
  await dlg.getByLabel('E-mail para avisar da correção').fill('pessoa@exemplo.com');
  // a issue abre numa nova aba: capturamos o endereço sem abrir o GitHub
  await page.evaluate(() => { (window as unknown as { __abertas: string[] }).__abertas = []; window.open = ((u: string) => { (window as unknown as { __abertas: string[] }).__abertas.push(String(u)); return null; }) as typeof window.open; });
  await dlg.getByRole('button', { name: 'Abrir issue no GitHub' }).click();
  const abertas = await page.evaluate(() => (window as unknown as { __abertas: string[] }).__abertas);
  expect(abertas).toHaveLength(1);
  const u = new URL(abertas[0]);
  expect(u.pathname).toBe('/millena84/metadata-desbugando/issues/new');
  expect(u.searchParams.get('template')).toBe('erro-reportado.yml');
  expect(u.searchParams.get('tipo')).toBe('Está errado');
  expect(u.searchParams.get('descricao')).toContain('Teste automatizado');
  expect(u.searchParams.get('fonte')).toBe('pela prática');
  expect(u.searchParams.get('body')).toContain('Teste automatizado');
  expect(abertas[0]).not.toContain('pessoa');
  await expect(dlg.getByRole('status')).toContainText('nova aba');
  await expect(dlg.getByRole('status')).toContainText('só é criada quando você marcar a confirmação');
  await expect(dlg.getByRole('status')).toContainText('ele já foi copiado');
  await expect(dlg.getByRole('status')).toContainText('Seu e-mail não foi incluído');
  // e-mail malformado barra o envio
  await dlg.getByLabel('E-mail para avisar da correção').fill('pessoa@');
  await dlg.getByRole('button', { name: 'Abrir issue no GitHub' }).click();
  await expect(dlg.getByRole('status')).toContainText('e-mail para aviso parece incompleto');
  // o e-mail do suporte não aparece no HTML da página
  expect(await page.content()).not.toMatch(/millena\.ferreira|suporte\.desbugando/);
});

test('10b. Reportar erro numa propriedade leva o nome e o status da propriedade', async ({ page }) => {
  await abrir(page, '?v=funcionalidade&n=mdt:PermissionSet');
  await painel(page).locator('.btn-tabela').first().click();
  const tabela = page.locator('#dialogo');
  await tabela.getByRole('button', { name: 'description', exact: true }).first().click();
  await tabela.getByRole('button', { name: 'Reportar erro em description' }).click();
  const dlg = page.locator('#dialogo-reporte');
  await expect(dlg).toContainText('PermissionSet › description');
  await expect(dlg.locator('.contexto-reporte')).toContainText(/Status no site\s*(Verificado|Desconhecido|Não aplicável|Não exposto|Bloqueado)/);
});

test('11. Ícones das nuvens são do próprio site (nenhuma imagem de servidores da Salesforce)', async ({ page }) => {
  const externas: string[] = [];
  page.on('request', (r) => { if (/sfdcstatic|sfdcdigital|salesforce\.com/.test(r.url()) && r.resourceType() === 'image') externas.push(r.url()); });
  await abrir(page, '?v=nuvem&n=nuv:service-cloud');
  const icone = painel(page).locator('img.logo-marca');
  await expect(icone).toHaveAttribute('src', /icones\/nuvens\/service-cloud\.svg$/);
  await expect.poll(() => icone.evaluate((i) => (i as HTMLImageElement).naturalWidth)).toBeGreaterThan(0);
  expect(externas).toEqual([]);
});

test('12. Rodapé mostra a release da documentação e até quando os dados foram verificados', async ({ page }) => {
  await abrir(page, '');
  await expect(page.locator('#versao')).toHaveText(/Dados: documentação .+ \(API \d+\.\d\), verificada até \d{2}\/\d{2}\/\d{4}/);
});
