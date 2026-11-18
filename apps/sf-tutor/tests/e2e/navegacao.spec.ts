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

test('busca por um campo abre o objeto no mapa e a tabela na linha do campo', async ({ page }) => {
  await abrir(page);
  const antes = await page.evaluate(() => (window as unknown as { __sfTutor: { nosRenderizados(): number } }).__sfTutor.nosRenderizados());
  await page.locator('#busca').fill('AssigneeId');
  await page.keyboard.press('ArrowDown');
  await page.keyboard.press('Enter');
  await expect(titulo(page)).toHaveText('PermissionSetAssignment');
  expect(await selecao(page)).toMatch(/>obj:PermissionSetAssignment$/);
  await expect(page.locator('#dialogo tr.linha-item.aberta')).toHaveAttribute('data-id', 'obj:PermissionSetAssignment.AssigneeId');
  await expect(page).toHaveURL(/t=obj%3APermissionSetAssignment&f=obj%3APermissionSetAssignment\.AssigneeId/);
  const depois = await page.evaluate(() => (window as unknown as { __sfTutor: { nosRenderizados(): number } }).__sfTutor.nosRenderizados());
  expect(depois).toBeGreaterThan(antes);
  // voltar no histórico não deixa a janela aberta sobre outro item
  await page.keyboard.press('Escape');
  await expect(page.locator('#dialogo')).toBeHidden();
  await expect(page).not.toHaveURL(/t=obj/);
});

test('metadata type e objeto são o último nó; expandir e recolher pela funcionalidade', async ({ page }) => {
  await abrir(page, '?n=obj:User');
  await expect(painel(page).getByRole('button', { name: /^Expandir/ })).toHaveCount(0);
  await abrir(page, '?n=func:permission-sets');
  const qtd = () => page.evaluate(() => (window as unknown as { __sfTutor: { nosRenderizados(): number } }).__sfTutor.nosRenderizados());
  const a = await qtd();
  await painel(page).getByRole('button', { name: /^Expandir \(\d+ itens\)/ }).click();
  expect(await qtd()).toBeGreaterThan(a);
  await page.getByRole('button', { name: /^Recolher/ }).click();
  expect(await qtd()).toBe(a);
});

test('estrutura auxiliar abre como tabela a partir do metadata type', async ({ page }) => {
  await abrir(page, '?n=mdt:NamedCredential');
  const est = await secao(page, /Estruturas auxiliares usadas/);
  await est.getByRole('button', { name: 'NamedCredentialParameter', exact: true }).click();
  const janela = page.locator('#dialogo');
  await expect(page.locator('#dialogo-titulo')).toContainText('Propriedades de NamedCredentialParameter');
  await expect(janela).toContainText('Estrutura auxiliar do schema');
  expect(await janela.locator('tr.linha-item').count()).toBeGreaterThan(0);
  await expect(titulo(page)).toHaveText('NamedCredential');
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
    'mdt:PermissionSet', 'obj:PermissionSetAssignment'];
  for (const id of ids) {
    await abrir(page, `?n=${encodeURIComponent(id)}`);
    await expect(titulo(page), id).not.toBeEmpty();
    expect(await selecao(page), id).toMatch(new RegExp(`${id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`));
    await semErroNoPainel(page);
  }
});

test('links antigos para campo, propriedade e estrutura abrem o nó dono com a tabela', async ({ page }) => {
  const casos: [string, string, string | null][] = [
    ['obj:User.ProfileId', 'obj:User', 'obj:User.ProfileId'],
    ['mdt:PermissionSet.applicationVisibilities', 'mdt:PermissionSet', 'mdt:PermissionSet.applicationVisibilities'],
    ['mdx:AssignmentRules_RuleEntry', 'mdt:AssignmentRules', null],
  ];
  for (const [id, dono, foco] of casos) {
    await abrir(page, `?n=${encodeURIComponent(id)}`);
    expect(await selecao(page), id).toMatch(new RegExp(`>${dono.replace('.', '\\.')}$`));
    const janela = page.locator('#dialogo');
    await expect(janela, id).toBeVisible();
    if (foco) await expect(janela.locator('tr.linha-item.aberta'), id).toHaveAttribute('data-id', foco);
    await expect(janela.locator('.erro'), id).toHaveCount(0);
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

test('desktop: "Mostrar no mapa" só aparece no modo leitura e volta ao mapa com destaque', async ({ page, isMobile }) => {
  test.skip(isMobile, 'somente desktop');
  await abrir(page, '?n=func:event-relay');
  await expect(painel(page).getByRole('button', { name: 'Mostrar no mapa' })).toBeHidden();
  await page.getByRole('button', { name: 'Modo leitura' }).click();
  await painel(page).getByRole('button', { name: 'Mostrar no mapa' }).click();
  await expect(page.locator('body')).not.toHaveClass(/modo-leitura/);
  const cls = await page.evaluate(() => (window as unknown as { __sfTutor: { classes(id: string): string[] | null } }).__sfTutor.classes('func:event-relay'));
  expect(cls).toContain('foco');
});

test('"Sobre este tema" mostra as três camadas na mesma ordem em tema e tema interno (#34)', async ({ page }) => {
  // [id, tem referências oficiais próprias]. Desde o fecho da rodada A4, todos os temas internos têm referências;
  // o caso 'false' (selo "Curadoria do projeto") segue coberto pelo teste unitário de estadoRecorte (adaptador.test.ts).
  const casos: [string, boolean][] = [
    ['cls:integracao-apis-e-eventos', true],
    ['sub:acoes-e-regras', true],
    ['sub:limites-e-consumo', true],
    ['cls:interface-e-experiencia-do-usuario', true],
  ];
  for (const [id, comReferencias] of casos) {
    await abrir(page, `?n=${id}`);
    await expect(painel(page).locator('.tipo-no')).toHaveText(/Tema/);
    // cabeçalho mostra o estado do recorte, não o estado bruto
    await expect(painel(page).locator('.linha-selos')).not.toContainText('Desconhecido');
    await expect(painel(page).locator('.linha-selos .selo-recorte')).toHaveText(comReferencias ? 'Parcialmente conferido' : 'Curadoria do projeto');
    const sobre = await secao(page, /^Sobre este tema$/);
    await expect(sobre.locator('.camada > h4')).toHaveText(['Para quem está começando', 'Para quem já conhece Salesforce']);
    await expect(sobre).toContainText(/Funcionalidades \(\d+\)/);
    const avancado = sobre.locator('details.camada-avancada');
    await expect(avancado.locator('summary').first()).toHaveText('Nível avançado');
    expect(await avancado.evaluate((d) => (d as HTMLDetailsElement).open)).toBe(false);
    await avancado.locator('summary').first().click();
    const recorte = avancado.locator('details.sobre-recorte');
    await recorte.locator('summary').click();
    await expect(recorte.locator('h5')).toContainText(['O que entra neste tema', 'O que fica fora e onde procurar', 'Correspondência com referências oficiais']);
    if (comReferencias) {
      await expect(recorte).toContainText('Parcialmente conferido');
      await expect(recorte.locator('ul.fontes li').first()).toContainText(/Cobre (o tema|parte do tema)|Mais ampla que o tema/);
    } else {
      await expect(recorte).toContainText('Veja as do tema de cima');
    }
    await expect(painel(page)).not.toContainText('Estado do agrupamento');
    for (const t of await painel(page).locator('summary, h4').allTextContents()) expect(t).not.toMatch(/lassificaç/);
    await semErroNoPainel(page);
  }
});

test('tema com conteúdo próprio: exemplo, comece por, encadeamento e decisões com fonte (#34, piloto)', async ({ page }) => {
  await abrir(page, '?n=cls:interface-e-experiencia-do-usuario');
  const sobre = await secao(page, /^Sobre este tema$/);
  const c1 = sobre.locator('.camada').nth(0);
  await expect(c1).toContainText('Exemplo:');
  await expect(c1.locator('.analogia')).toContainText('Onde a analogia para');
  await expect(c1.locator('.comece-por button')).toHaveText(['Lightning apps', 'Lightning pages', 'Page layouts']);
  const c2 = sobre.locator('.camada').nth(1);
  await expect(c2.locator('h5').first()).toHaveText('Como as partes se ligam');
  await expect(c2).toContainText('FlexiPage');
  // metadata types alcançados pelas funcionalidades do tema, inclusive os cadastrados na rodada A3
  await expect(c2).toContainText('CustomApplication');
  const avancado = sobre.locator('details.camada-avancada');
  await avancado.locator('summary').first().click();
  await expect(avancado.locator('.item-avancado h5')).toContainText(['Decisão: Qual ferramenta usar para um formulário', 'Segurança: A página não é controle de acesso']);
  await expect(avancado).toContainText('Implantação: suporte no Salesforce CLI');
  await expect(avancado).toContainText('Dependências entre componentes');
  // todo item curado tem fonte
  const itens = avancado.locator('.item-avancado:has(.fontes-camada)');
  expect(await itens.count()).toBeGreaterThanOrEqual(4);
  // tema interno navega para a funcionalidade pelo "comece por"
  await abrir(page, '?n=sub:lightning-pages-e-componentes');
  const s2 = await secao(page, /^Sobre este tema$/);
  await expect(s2.locator('.camada').nth(1).locator('h5').first()).toHaveText('Como se encaixa no tema de cima');
  await s2.locator('.comece-por button').first().click();
  await expect(titulo(page)).toHaveText('Lightning pages');
});

test('busca pela pasta do projeto acha o metadata type; tipo sem ficha aparece marcado e não abre nada', async ({ page }) => {
  await page.goto('/');
  await page.locator('#busca').fill('applications');
  const primeiro = page.locator('#resultados .resultado').first();
  await expect(primeiro).toContainText('CustomApplication');
  await expect(primeiro).toContainText('pasta applications');
  // ModerationRule é um tipo do inventário, sem ficha no catálogo; se ganhar ficha, troque por outro tipo sem ficha.
  await page.locator('#busca').fill('moderation');
  const semFicha = page.locator('#resultados .resultado.sem-ficha', { hasText: 'ModerationRule' }).first();
  await expect(semFicha).toContainText('ModerationRule');
  await expect(semFicha).toContainText('ainda não tem ficha');
  const antes = page.url();
  await semFicha.dispatchEvent('mousedown');
  expect(page.url()).toBe(antes);
});

// Nuvens que faltavam (2026-11-17): produto com plataforma própria mostra onde roda, marcado como classificação do projeto.
test('nuvem nova mostra onde roda e o nome atual', async ({ page }) => {
  await abrir(page, '?n=nuv:mulesoft');
  await expect(titulo(page)).toHaveText('MuleSoft');
  await expect(painel(page)).toContainText('Plataforma própria, conectada à org');
  await expect(painel(page)).toContainText('classificação do projeto');
  await abrir(page, '?n=nuv:platform-core');
  await expect(titulo(page)).toHaveText('Agentforce 360 Platform');
  await expect(painel(page)).toContainText('Roda na org Salesforce');
});

// Regressão da C2: a lista de resultados fica dentro do cabeçalho escuro e herdava a cor Claro (texto quase invisível).
test('resultados da busca têm contraste AA com o fundo da lista', async ({ page }) => {
  await abrir(page, '');
  await page.locator('#busca').fill('PermissionSet');
  const rot = page.locator('#resultados [role=option] .res-rot').first();
  await expect(rot).toBeVisible();
  const razao = await rot.evaluate((el) => {
    const rgb = (s: string) => (s.match(/\d+(\.\d+)?/g) ?? []).slice(0, 3).map(Number);
    const lum = ([r, g, b]: number[]) => [r, g, b].map((v) => { const c = v / 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; })
      .reduce((t, c, i) => t + c * [0.2126, 0.7152, 0.0722][i], 0);
    const lista = document.getElementById('resultados')!;
    const [a, b] = [lum(rgb(getComputedStyle(el).color)), lum(rgb(getComputedStyle(lista).backgroundColor))].sort((x, y) => y - x);
    return (a + 0.05) / (b + 0.05);
  });
  expect(razao).toBeGreaterThanOrEqual(4.5);
});
