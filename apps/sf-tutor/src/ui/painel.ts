// Painel de leitura: renderiza o cadastro de cada tipo de nó. O conteúdo vem das entidades do catálogo;
// aqui só há rótulos de interface. Chaves não tratadas aparecem em "Outros dados do cadastro".
import type { Afirmacao, Entidade, Fonte, InfoBuild, Manifesto } from '../data/tipos';
import type { Entidades } from '../data/carregador';
import { Indice, TIPOS_FOLHA, TIPOS_OBJETO, type Visao } from '../model/adaptador';
import {
  FORMA_DEFAULT, ICONE_TIPO, LIGACAO, NATUREZA_DOMINIO, NATUREZA_RECOMENDACAO, NOME_API, NOME_TIPO, OBRIGATORIEDADE, ORIGEM,
  PROPRIEDADES_API, TIPO_LICENCA, rotuloEstado,
} from '../rotulos';
import { copiar, h, limpar } from './dom';
import { afirmacao, codigo, fontesEl, listaTexto, restantes, secao, selo, texto, valorEl } from './partes';
import type { ArestaClicada } from '../graph/mapa';

export interface CtxPainel {
  ind: Indice;
  entidades: Entidades;
  fontes: Record<string, Fonte>;
  manifesto: Manifesto;
  build: InfoBuild;
  cobertura: Record<string, unknown>;
  visao(): Visao;
  rotulo(id: string): string;
  abrir(id: string, contexto?: readonly string[]): void;
  abrirCaminho(caminho: readonly string[]): void;
  alternar(caminho: readonly string[]): void;
  expandido(caminho: readonly string[]): boolean;
  focarNoMapa(caminho: readonly string[]): void;
  link(id: string, caminho?: readonly string[]): string;
  abrirMetodo(): void;
  abrirRelacao(relId: string): void;
  motivoOculto(id: string): string | null;
}

const ent = <T = unknown>(e: Record<string, unknown>, k: string): T => e[k] as T;
const arr = <T = unknown>(v: unknown): T[] => (Array.isArray(v) ? (v as T[]) : []);

let geracao = 0;

export async function renderizarNo(ctx: CtxPainel, alvo: HTMLElement, caminho: readonly string[]): Promise<void> {
  const minha = ++geracao;
  const id = caminho[caminho.length - 1];
  const no = ctx.ind.no(id);
  limpar(alvo);
  if (!no) {
    alvo.append(h('p', { class: 'erro' }, `Item ${id} não encontrado nos dados carregados.`));
    return;
  }
  alvo.append(cabecalho(ctx, caminho));
  const corpo = h('div', { class: 'corpo', 'aria-busy': 'true' }, h('p', { class: 'carregando' }, 'Carregando ficha…'));
  alvo.append(corpo);
  try {
    const paiId = TIPOS_FOLHA.has(no.tipo) ? no.pai! : id;
    const e = await ctx.entidades.obter(paiId);
    if (minha !== geracao) return;
    limpar(corpo);
    corpo.removeAttribute('aria-busy');
    const partes = corpoPorTipo(ctx, no.tipo, e, caminho);
    corpo.append(...partes.filter(Boolean) as Node[]);
  } catch (err) {
    if (minha !== geracao) return;
    limpar(corpo);
    corpo.append(h('p', { class: 'erro', role: 'alert' }, `Não foi possível carregar a ficha: ${String((err as Error).message ?? err)}. O mapa continua navegável.`));
  }
}

function cabecalho(ctx: CtxPainel, caminho: readonly string[]): HTMLElement {
  const id = caminho[caminho.length - 1];
  const no = ctx.ind.no(id)!;
  const visao = ctx.visao();
  const total = ctx.ind.quantidadeFilhos(visao, caminho);
  const exp = ctx.expandido(caminho);
  const outros = ctx.ind.caminhosPara(id, visao).filter((c) => c.join('>') !== caminho.join('>'));
  const oculto = ctx.motivoOculto(id);
  const btnLink = h('button', { type: 'button', class: 'btn' }, 'Copiar link');
  btnLink.addEventListener('click', () => copiar(new URL(ctx.link(id, caminho), location.href).toString(), btnLink));
  return h('header', { class: 'cab-painel' },
    h('p', { class: 'tipo-no' }, h('span', { class: `ico ico-${no.tipo}`, 'aria-hidden': 'true' }, ICONE_TIPO[no.tipo] || (no.sigla ?? '•')), NOME_TIPO[no.tipo]),
    h('h2', { id: 'titulo-painel', tabindex: -1 }, no.rotulo),
    no.rotulo_tecnico && no.rotulo_tecnico !== no.rotulo ? h('p', { class: 'nome-tecnico' }, no.rotulo_tecnico) : null,
    TIPOS_FOLHA.has(no.tipo) ? h('p', { class: 'nome-tecnico' }, id.replace(/^(obj|mdt|mdx):/, '')) : null,
    h('p', { class: 'linha-selos' }, no.estado ? selo(no.estado) : null, no.tipo_tecnico ? h('span', { class: 'selo selo-tipo' }, no.tipo_tecnico) : null,
      ...(no.apis ?? []).map((a) => h('span', { class: 'selo selo-api' }, NOME_API[a] ?? a))),
    oculto ? h('p', { class: 'aviso' }, `Esmaecido pelos filtros: ${oculto}.`) : null,
    h('nav', { class: 'migalhas', 'aria-label': 'Caminho no mapa' },
      h('ol', null, caminho.map((c, i) => h('li', null,
        i === caminho.length - 1 ? h('span', { 'aria-current': 'location' }, ctx.rotulo(c))
          : h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho(caminho.slice(0, i + 1)) } }, ctx.rotulo(c)))))),
    h('div', { class: 'acoes' },
      total > 0 ? h('button', { type: 'button', class: 'btn btn-primario', 'aria-expanded': String(exp), on: { click: () => ctx.alternar(caminho) } },
        exp ? `Recolher (${total})` : `Expandir (${total} ${total === 1 ? 'item' : 'itens'})`) : null,
      h('button', { type: 'button', class: 'btn', on: { click: () => ctx.focarNoMapa(caminho) } }, 'Mostrar no mapa'),
      btnLink),
    outros.length ? h('details', { class: 'outros-caminhos' },
      h('summary', null, `Também aparece em ${outros.length} outro${outros.length > 1 ? 's' : ''} caminho${outros.length > 1 ? 's' : ''} (mesma ficha)`),
      h('ul', null, outros.slice(0, 12).map((c) => h('li', null, h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho(c) } }, c.slice(1).map(ctx.rotulo).join(' › ')))))) : null,
  );
}

function corpoPorTipo(ctx: CtxPainel, tipo: string, e: Entidade, caminho: readonly string[]): (Node | null)[] {
  switch (tipo) {
    case 'salesforce': return painelSalesforce(ctx, e);
    case 'nuvem': return painelNuvem(ctx, e, caminho);
    case 'classificacao': return painelClassificacao(ctx, e, caminho);
    case 'subclassificacao': return painelSub(ctx, e, caminho);
    case 'funcionalidade': return painelFunc(ctx, e, caminho);
    case 'metadata_type': return painelMdt(ctx, e, caminho);
    case 'estrutura_auxiliar': return painelMdx(ctx, e, caminho);
    case 'objeto_api':
    case 'objeto_api_juncao': return painelObj(ctx, e, caminho);
    case 'campo_api':
    case 'propriedade_xml': return painelFolha(ctx, e, caminho);
    default: return [h('p', null, 'Tipo de nó sem painel.')];
  }
}

// ------------------------------------------------------------------ Salesforce

function painelSalesforce(ctx: CtxPainel, e: Entidade): (Node | null)[] {
  const vb = ent<Record<string, string>>(e, 'versao_base') ?? {};
  const cob = ctx.cobertura as Record<string, Record<string, unknown>>;
  const mdt = cob.metadata_types ?? {};
  const obj = cob.objetos_api ?? {};
  const conceitos = arr<Record<string, string>>(e.conceitos);
  return [
    texto('O que é', e.o_que_e, { didatico: true }),
    h('div', { class: 'aviso aviso-logo' }, h('strong', null, 'Logo: '), 'o centro usa um placeholder identificado. ', String(e.nota_logo ?? 'Este projeto não é afiliado à Salesforce.')),
    secao('Conceitos fundamentais', true, h('dl', { class: 'conceitos' }, conceitos.flatMap((c) => [
      h('dt', null, c.termo),
      h('dd', null, c.definicao, c.analogia ? h('p', { class: 'analogia' }, h('strong', null, 'Analogia: '), c.analogia, c.limite_analogia ? h('span', null, ` Limite: ${c.limite_analogia}`) : null) : null),
    ]))),
    secao('Como o mapa está organizado', true, texto('Organização', e.organizacao_do_mapa, { didatico: true }), texto('Relações entre produtos', e.relacoes_entre_produtos, { didatico: true }),
      listaTexto('Como navegar', arr(e.como_navegar))),
    secao('Versão, escopo e cobertura', true,
      h('dl', { class: 'kv' },
        h('dt', null, 'Versão da API'), h('dd', null, `${vb.api_version ?? '?'} (${vb.release ?? '?'})`),
        h('dt', null, 'Data de referência'), h('dd', null, vb.data_referencia ?? '?'),
        h('dt', null, 'Contrato de dados'), h('dd', null, `${ctx.manifesto.contrato.nome} ${ctx.manifesto.contrato.versao}`),
        h('dt', null, 'Insumos (build)'), h('dd', null, ctx.build.commit ? `commit ${ctx.build.commit}` : 'commit não informado', ctx.build.data_build ? ` · ${ctx.build.data_build}` : ''),
        h('dt', null, 'Metadata types'), h('dd', null, `${mdt.cadastrados ?? '?'} cadastrados de ${mdt.universo_v68 ?? '?'} no universo v68; ${mdt.estruturalmente_completos ?? '?'} com estrutura completa; ${mdt.pendentes_de_classificacao ?? '?'} ainda sem classificação Core`),
        h('dt', null, 'Objetos API'), h('dd', null, `${obj.catalogados ?? '?'} catalogados; ${obj.campos_listados ?? '?'} campos listados, ${obj.campos_explicados ?? '?'} explicados. ${obj.nota_universo ?? ''}`),
      ),
      h('p', { class: 'nota' }, 'Cobertura parcial: itens sem cadastro aparecem como "ainda não mapeado". Contagens completas em Método.'),
      h('button', { type: 'button', class: 'btn', on: { click: () => ctx.abrirMetodo() } }, 'Abrir Método e cobertura')),
    secao('Nuvens e classificações', false,
      listaLinks(ctx, 'Nuvens / produtos', arr<string>(e.nuvens)), listaLinks(ctx, 'Classificações funcionais', arr<string>(e.classificacoes))),
    secao('Fontes', false, fontesEl(ctx, arr(e.evidencias))),
    restantes(e, ['id', 'nome', 'nota_logo', 'o_que_e', 'conceitos', 'organizacao_do_mapa', 'relacoes_entre_produtos', 'como_navegar', 'nuvens', 'classificacoes', 'versao_base', 'estado', 'evidencias']),
  ];
}

// ------------------------------------------------------------------ Nuvem

function painelNuvem(ctx: CtxPainel, e: Entidade, caminho: readonly string[]): (Node | null)[] {
  const lic = ent<Afirmacao & { itens?: Record<string, unknown>[] }>(e, 'licencas');
  const cas = arr<{ classificacao: string; subclassificacoes: { subclassificacao: string; funcionalidades: string[] }[] }>(e.classificacoes_aplicaveis);
  const funcs = cas.flatMap((c) => c.subclassificacoes.flatMap((s) => s.funcionalidades));
  const unicas = [...new Set(funcs)];
  const compart = unicas.filter((f) => (ctx.ind.nuvensDaFunc.get(f) ?? []).length > 1);
  return [
    texto('Resumo', e.resumo, { didatico: true }),
    listaTexto('Nome oficial e aliases', [String(e.nome_oficial ?? ''), ...arr<string>(e.aliases).map((a) => `Alias: ${a}`)]),
    texto('O que é', e.o_que_e, { didatico: true }),
    listaTexto('Casos de uso', arr(e.casos_de_uso)),
    afirmacao(ctx, 'Contexto tecnológico', ent<Afirmacao>(e, 'contexto_tecnico')),
    secao('Licenças e requisitos', true,
      lic ? h('div', null,
        h('p', null, selo(lic.estado), ' ', lic.nota ?? ''),
        h('ul', { class: 'lista' }, arr<Record<string, unknown>>(lic.itens).map((i) => h('li', null,
          h('strong', null, String(i.nome)), ` — ${TIPO_LICENCA[String(i.tipo)] ?? String(i.tipo)}`, fontesEl(ctx, arr(i.evidencias))))),
        h('p', { class: 'nota' }, 'Licença de usuário, licença de permission set, edição e add-on são coisas diferentes. Preços não são registrados.'),
      ) : h('p', { class: 'vazio' }, 'Licenças não registradas.')),
    secao(`Funcionalidades (${unicas.length})`, true,
      h('p', { class: 'nota' }, `${unicas.length - compart.length} aparecem só nesta nuvem no catálogo atual; ${compart.length} são compartilhadas com outras nuvens (mesma ficha).`),
      ...cas.map((c) => h('div', { class: 'grupo-func' },
        h('h4', null, ctx.rotulo(c.classificacao)),
        ...c.subclassificacoes.map((s) => h('div', null, h('p', { class: 'sub-rotulo' }, ctx.rotulo(s.subclassificacao)),
          h('ul', { class: 'lista-links' }, s.funcionalidades.map((f) => h('li', null,
            h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho([...caminho, c.classificacao, s.subclassificacao, f]) } }, ctx.rotulo(f)),
            compart.includes(f) ? h('span', { class: 'selo selo-compart' }, 'compartilhada') : null)))))))),
    listaTexto('Dependências', arr(e.dependencias)),
    listaTexto('Limites e pontos de atenção', arr(e.limites)),
    texto('Cobertura do inventário desta nuvem', e.cobertura_inventario),
    secao('Fontes', false, fontesEl(ctx, arr(e.evidencias))),
    restantes(e, ['id', 'nome_oficial', 'aliases', 'sigla', 'resumo', 'o_que_e', 'casos_de_uso', 'contexto_tecnico', 'licencas', 'classificacoes_aplicaveis', 'dependencias', 'limites', 'cobertura_inventario', 'estado', 'evidencias']),
  ];
}

// ------------------------------------------------------------------ Classificação / sub

function natureza(n: unknown): HTMLElement {
  return n === 'curadoria_didatica'
    ? h('p', { class: 'aviso' }, 'Agrupamento didático (curadoria do projeto), não nomenclatura oficial da Salesforce.')
    : h('p', null, `Natureza: ${String(n ?? 'não informada')}`);
}

function painelClassificacao(ctx: CtxPainel, e: Entidade, caminho: readonly string[]): (Node | null)[] {
  const subs = arr<string>(e.subclassificacoes);
  const visao = ctx.visao();
  return [
    texto('O que agrupa', e.descricao, { didatico: true }),
    natureza(e.natureza),
    secao(`Sub-classificações (${subs.length})`, true, h('ul', { class: 'lista-links' }, subs.map((s) => {
      const n = ctx.ind.quantidadeFilhos('funcionalidade', ['salesforce', e.id, s]);
      const noCaminho = visao === 'funcionalidade' ? [...caminho, s] : null;
      return h('li', null,
        noCaminho ? h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho(noCaminho) } }, ctx.rotulo(s)) : h('span', null, ctx.rotulo(s)),
        h('span', { class: n ? 'contagem' : 'contagem vazio' }, n ? ` ${n} funcionalidade${n > 1 ? 's' : ''}` : ' ainda não mapeado'));
    }))),
    secao('Pré-requisitos, exemplos e limites', false, h('p', { class: 'vazio' }, 'Não registrados no cadastro desta classificação. Veja os de cada funcionalidade.')),
    afirmacao(ctx, 'Estado do agrupamento', { estado: String(e.estado ?? ''), nota: String(e.nota_estado ?? '') }),
    listaTexto('Referências oficiais', arr(e.referencias_oficiais), 'Nenhuma referência oficial registrada: o agrupamento ainda não foi cruzado com a documentação.'),
    restantes(e, ['id', 'nome', 'nome_curto', 'sigla', 'natureza', 'descricao', 'subclassificacoes', 'referencias_oficiais', 'estado', 'nota_estado']),
  ];
}

function painelSub(ctx: CtxPainel, e: Entidade, caminho: readonly string[]): (Node | null)[] {
  const funcs = arr<string>(e.funcionalidades);
  const principais = new Set((ctx.ind.saindo.get(e.id) ?? []).filter((a) => a.tipo === 'classificacao_principal').map((a) => a.destino));
  const nestaVisao = ctx.ind.filhos(ctx.visao(), caminho).map((f) => f.id);
  return [
    texto('O que agrupa', e.descricao, { didatico: true }),
    natureza(e.natureza),
    h('p', null, 'Classificação: ', h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrir(String(e.classificacao)) } }, ctx.rotulo(String(e.classificacao)))),
    secao(`Funcionalidades (${funcs.length})`, true, funcs.length
      ? h('ul', { class: 'lista-links' }, funcs.map((f) => h('li', null,
        nestaVisao.includes(f) ? h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho([...caminho, f]) } }, ctx.rotulo(f))
          : h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrir(f, caminho) } }, ctx.rotulo(f)),
        h('span', { class: 'selo' }, principais.has(f) ? 'principal' : 'secundária'))))
      : h('p', { class: 'vazio' }, 'Ainda não mapeado: nenhuma funcionalidade catalogada nesta sub-classificação.')),
    secao('Pré-requisitos, exemplos e limites', false, h('p', { class: 'vazio' }, 'Não registrados no cadastro desta sub-classificação.')),
    afirmacao(ctx, 'Estado do agrupamento', { estado: String(e.estado ?? ''), nota: String(e.nota_estado ?? '') }),
    restantes(e, ['id', 'nome', 'sigla', 'classificacao', 'natureza', 'descricao', 'funcionalidades', 'estado', 'nota_estado']),
  ];
}

// ------------------------------------------------------------------ Funcionalidade

function painelFunc(ctx: CtxPainel, e: Entidade, caminho: readonly string[]): (Node | null)[] {
  const rep = ent<{ metadata_types: { ref: string; papel: string }[]; objetos_api: { ref: string; papel: string }[]; ausencias: Record<string, unknown>[] }>(e, 'representacoes');
  const cp = ent<{ classificacao: string; subclassificacao: string }>(e, 'classificacao_principal');
  const cs = arr<{ classificacao: string; subclassificacao: string; motivo?: string }>(e.classificacoes_secundarias);
  const nuvens = ctx.ind.nuvensDaFunc.get(e.id) ?? [];
  const rec = arr<{ texto: string; natureza?: string }>(e.recomendacoes);
  return [
    texto('O que é', e.o_que_e, { didatico: true }),
    texto('Para que serve', e.finalidade, { didatico: true }),
    texto('Exemplo', e.exemplo, { didatico: true }),
    secao('Representações técnicas', true,
      repLista(ctx, 'Metadata types (XML)', rep?.metadata_types ?? [], caminho),
      repLista(ctx, 'Objetos consultáveis via API', rep?.objetos_api ?? [], caminho),
      ...(rep?.ausencias ?? []).map((a) => h('div', { class: `afirmacao estado-${String(a.estado)}` },
        h('h4', null, `Sem ${a.tipo === 'metadata_type' ? 'metadata type (XML)' : a.tipo === 'objeto_api' ? 'objeto API' : String(a.tipo)}`, ' ', selo(String(a.estado))),
        h('p', null, String(a.motivo ?? '')), fontesEl(ctx, arr(a.evidencias))))),
    afirmacao(ctx, 'Caminho no Setup', ent<Afirmacao>(e, 'setup')),
    listaTexto('Pré-requisitos, edições e permissões', arr(e.pre_requisitos)),
    secao('Nuvens e classificações', true,
      h('h4', null, 'Nuvens / produtos'),
      nuvens.length ? h('ul', { class: 'lista-links' }, nuvens.map((n) => h('li', null, h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrir(n) } }, ctx.rotulo(n))))) : h('p', { class: 'vazio' }, 'Nenhuma nuvem associada no catálogo.'),
      h('h4', null, 'Classificação principal'),
      cp ? h('p', null, `${ctx.rotulo(cp.classificacao)} › ${ctx.rotulo(cp.subclassificacao)}`) : null,
      cs.length ? h('div', null, h('h4', null, 'Classificações secundárias'), h('ul', { class: 'lista' }, cs.map((c) => h('li', null, `${ctx.rotulo(c.classificacao)} › ${ctx.rotulo(c.subclassificacao)}`, c.motivo ? h('span', { class: 'nota' }, ` — ${c.motivo}`) : null)))) : null),
    rec.length ? secao('Recomendações', false, h('ul', { class: 'lista' }, rec.map((r) => h('li', null, r.texto, h('span', { class: 'selo' }, NATUREZA_RECOMENDACAO[r.natureza ?? ''] ?? r.natureza ?? ''))))) : null,
    listaTexto('Alertas', arr(e.alertas)),
    listaTexto('Limitações conhecidas', arr(e.limitacoes)),
    listaTexto('Aliases e termos de busca', [...new Set([...arr<string>(e.aliases), ...arr<string>(e.termos_busca)])]),
    secao('Fontes', false, fontesEl(ctx, arr(e.evidencias))),
    restantes(e, ['id', 'nome', 'nome_tecnico', 'aliases', 'termos_busca', 'o_que_e', 'finalidade', 'exemplo', 'classificacao_principal', 'classificacoes_secundarias', 'representacoes', 'setup', 'recomendacoes', 'alertas', 'limitacoes', 'estado', 'evidencias', 'pre_requisitos']),
  ];
}

function repLista(ctx: CtxPainel, titulo: string, itens: { ref: string; papel: string }[], caminho: readonly string[]): HTMLElement | null {
  if (!itens.length) return null;
  return h('div', null, h('h4', null, titulo), h('ul', { class: 'lista-links' }, itens.map((r) => h('li', null,
    h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho([...caminho, r.ref]) } }, ctx.rotulo(r.ref)),
    h('span', { class: 'nota' }, ` — ${r.papel}`)))));
}

// ------------------------------------------------------------------ Metadata type / estrutura

function arquivo(v: unknown): string {
  const o = v as { pasta?: string; arquivo?: string };
  return o && typeof o === 'object' ? `Pasta ${o.pasta ?? '?'} · arquivo ${o.arquivo ?? '?'}` : String(v);
}

function painelMdt(ctx: CtxPainel, e: Entidade, caminho: readonly string[]): (Node | null)[] {
  const arqs = ent<Record<string, Afirmacao>>(e, 'arquivos') ?? {};
  const disp = ent<Record<string, string | null>>(e, 'disponibilidade') ?? {};
  const ex = ent<{ xml: string; natureza?: string; nota?: string }>(e, 'exemplo_xml');
  const funcs = ctx.ind.funcsDoItem.get(e.id) ?? [];
  return [
    texto('O que é', e.o_que_e, { didatico: true }),
    texto('Para que serve', e.finalidade, { didatico: true }),
    secao('Arquivo no projeto Salesforce', true,
      afirmacao(ctx, 'Source format (projeto do Salesforce CLI)', arqs.source_format, (v) => arquivo(v)),
      afirmacao(ctx, 'Formato da Metadata API (pacote)', arqs.metadata_api_format, (v) => arquivo(v)),
      arqs.curinga_package_xml ? afirmacao(ctx, 'Curinga (*) no package.xml', arqs.curinga_package_xml, (v) => (v ? 'suportado' : 'não se aplica a este tipo individual')) : null,
      h('p', { class: 'nota' }, 'Source format é o formato decomposto do projeto local; o formato da Metadata API é o do pacote implantado.')),
    afirmacao(ctx, 'Caminho no Setup', ent<Afirmacao>(e, 'setup')),
    h('p', null, h('strong', null, 'Disponível desde a versão: '), disp.desde_versao ?? 'não informado', disp.ate_versao ? ` · até ${disp.ate_versao}` : '', ' ', selo(disp.estado ?? undefined)),
    afirmacao(ctx, 'Suporte no Salesforce CLI', ent<Afirmacao>(e, 'suporte_cli')),
    e.componente_filho_de ? texto('Componente filho de', e.componente_filho_de) : null,
    ex?.xml ? codigo('Exemplo XML', ex.xml, 'XML', `${ex.natureza === 'didatico_projeto' ? 'Exemplo didático do projeto, sem dados reais. ' : ''}${ex.nota ?? ''}`) : h('p', { class: 'vazio' }, 'Exemplo XML ainda não registrado no cadastro.'),
    listaPropriedades(ctx, arr(e.propriedades), caminho, 'Propriedades XML'),
    estruturas(ctx, arr<string>(e.estruturas)),
    coberturaEl(e),
    relacoes(ctx, e.id),
    funcs.length ? listaLinks(ctx, 'Funcionalidades que usam este tipo', funcs) : null,
    listaTexto('Recomendações', arr<{ texto: string }>(e.recomendacoes).map((r) => r.texto)),
    listaTexto('Pontos de atenção', arr(e.alertas)),
    listaTexto('Divergências encontradas na documentação', arr(e.divergencias_documentais)),
    secao('Fontes', false, fontesEl(ctx, arr(e.evidencias))),
    restantes(e, ['id', 'nome', 'o_que_e', 'finalidade', 'estende', 'arquivos', 'disponibilidade', 'suporte_cli', 'setup', 'propriedades', 'estruturas', 'cobertura', 'recomendacoes', 'alertas', 'divergencias_documentais', 'estado', 'evidencias', 'exemplo_xml', 'componente_filho_de']),
  ];
}

function painelMdx(ctx: CtxPainel, e: Entidade, caminho: readonly string[]): (Node | null)[] {
  return [
    texto('O que é', e.o_que_e, { didatico: true }),
    h('p', { class: 'nota' }, 'Estrutura auxiliar do schema da Metadata API: aparece dentro de um XML, mas não é um metadata type implantável sozinho.'),
    listaLinks(ctx, 'Usada por', arr<string>(e.usada_por)),
    listaPropriedades(ctx, arr(e.propriedades), caminho, 'Propriedades'),
    coberturaEl(e),
    secao('Fontes', false, fontesEl(ctx, arr(e.evidencias))),
    restantes(e, ['id', 'nome', 'natureza', 'o_que_e', 'usada_por', 'propriedades', 'cobertura', 'estado', 'evidencias']),
  ];
}

function estruturas(ctx: CtxPainel, ids: string[]): HTMLElement | null {
  if (!ids.length) return null;
  return secao(`Estruturas auxiliares usadas (${ids.length})`, false, h('ul', { class: 'lista-links' }, ids.map((s) => h('li', null, h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrir(s) } }, ctx.rotulo(s))))));
}

// ------------------------------------------------------------------ Objeto API

function painelObj(ctx: CtxPainel, e: Entidade, caminho: readonly string[]): (Node | null)[] {
  const exps = arr<Record<string, unknown>>(e.exposicoes);
  const cons = arr<{ api: string; soql: string; contexto?: string; validacao?: string }>(e.consultas);
  const apex = ent<{ consulta_soql_direta?: Afirmacao; nota?: string }>(e, 'apex');
  const funcs = ctx.ind.funcsDoItem.get(e.id) ?? [];
  return [
    texto('O que é', e.o_que_e, { didatico: true }),
    texto('Papel na funcionalidade', e.papel, { didatico: true }),
    e.juncao ? h('p', { class: 'aviso' }, 'Objeto de junção: liga registros de dois objetos. Tem o mesmo nível de documentação dos demais, com todos os campos.') : null,
    h('p', { class: 'nota' }, 'Objeto consultável via API: é a interface pública documentada, não uma tabela física interna da Salesforce.'),
    secao('APIs de acesso e operações', true, ...exps.map((x) => h('div', { class: `afirmacao estado-${String(x.estado)}` },
      h('h4', null, NOME_API[String(x.api)] ?? String(x.api), ' ', selo(String(x.estado))),
      arr<string>(x.chamadas).length ? h('p', null, h('strong', null, 'Chamadas suportadas: '), arr<string>(x.chamadas).join(', ')) : null,
      x.acesso_especial ? h('p', null, h('strong', null, 'Permissões e restrições: '), String(x.acesso_especial)) : null,
      x.desde_versao ? h('p', null, `Desde a versão ${String(x.desde_versao)}`) : null,
      x.nota ? h('p', { class: 'nota' }, String(x.nota)) : null,
      fontesEl(ctx, arr(x.evidencias)))),
      h('p', { class: 'nota' }, 'API padrão e Tooling API não são equivalentes; cada exposição é verificada separadamente.')),
    secao('Consultas e Apex', true,
      ...cons.map((c) => codigo(`Consulta SOQL (${NOME_API[c.api] ?? c.api})`, c.soql, 'SOQL', `${c.contexto ?? ''} Validação: ${c.validacao === 'documental' ? 'documental, não executada em org' : c.validacao ?? '?'}. O exemplo não é executado por esta página.`)),
      apex ? afirmacao(ctx, 'Consulta SOQL direta em Apex', apex.consulta_soql_direta ?? null, (v) => (v ? 'sim' : 'não')) : null,
      apex?.nota ? h('p', { class: 'nota' }, apex.nota) : null),
    afirmacao(ctx, 'Caminho no Setup', ent<Afirmacao>(e, 'setup')),
    e.dominio_dinamico_de_campos ? texto('Campos dinâmicos', e.dominio_dinamico_de_campos) : null,
    listaCampos(ctx, arr(e.campos), caminho),
    coberturaEl(e),
    relacoes(ctx, e.id, true),
    funcs.length ? listaLinks(ctx, 'Funcionalidades', funcs) : null,
    listaTexto('Alertas', arr(e.alertas)),
    secao('Fontes', false, fontesEl(ctx, arr(e.evidencias))),
    restantes(e, ['id', 'nome', 'o_que_e', 'papel', 'exposicoes', 'campos', 'consultas', 'apex', 'juncao', 'setup', 'cobertura', 'alertas', 'estado', 'evidencias', 'dominio_dinamico_de_campos']),
  ];
}

// ------------------------------------------------------------------ listas pesquisáveis de folhas

function listaFolhas(ctx: CtxPainel, titulo: string, itens: Record<string, unknown>[], caminho: readonly string[], extra: (i: Record<string, unknown>) => string): HTMLElement {
  const filtro = h('input', { type: 'search', class: 'filtro-lista', placeholder: `Filtrar ${itens.length} itens…`, 'aria-label': `Filtrar ${titulo.toLowerCase()}` });
  const ul = h('ul', { class: 'lista-folhas' });
  const render = () => {
    limpar(ul);
    const q = filtro.value.trim().toLowerCase();
    const vis = itens.filter((i) => !q || String(i.nome).toLowerCase().includes(q) || String(i.o_que_e ?? '').toLowerCase().includes(q));
    for (const i of vis) {
      ul.append(h('li', null,
        h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho([...caminho, String(i.id)]) } }, String(i.nome)),
        h('span', { class: 'tipo-mini' }, ` ${String(i.tipo_tecnico ?? '')}`), ' ', selo(String(i.estado)),
        extra(i) ? h('span', { class: 'nota' }, ` ${extra(i)}`) : null,
        i.o_que_e ? h('p', { class: 'resumo-folha' }, String(i.o_que_e)) : h('p', { class: 'resumo-folha vazio' }, 'Explicação pendente.')));
    }
    if (!vis.length) ul.append(h('li', { class: 'vazio' }, 'Nenhum item com esse filtro.'));
  };
  filtro.addEventListener('input', render);
  render();
  return secao(`${titulo} (${itens.length}) — lista completa`, itens.length <= 30, h('p', { class: 'nota' }, 'Ordem da documentação. Cada item abre a própria ficha e o leva ao nó no mapa.'), filtro, ul)!;
}

function listaPropriedades(ctx: CtxPainel, itens: Record<string, unknown>[], caminho: readonly string[], titulo: string): HTMLElement | null {
  if (!itens.length) return h('p', { class: 'vazio' }, 'Nenhuma propriedade registrada.');
  return listaFolhas(ctx, titulo, itens, caminho, (i) => {
    const o = i.obrigatoriedade as { valor?: string } | undefined;
    return o?.valor === 'sim' ? '· obrigatória' : o?.valor === 'condicional' ? '· condicional' : '';
  });
}

function listaCampos(ctx: CtxPainel, itens: Record<string, unknown>[], caminho: readonly string[]): HTMLElement | null {
  if (!itens.length) return h('p', { class: 'vazio' }, 'Nenhum campo registrado.');
  return listaFolhas(ctx, 'Campos', itens, caminho, (i) => {
    const r = i.referencia as { alvos?: string[] } | undefined;
    return r?.alvos?.length ? `→ ${r.alvos.map((a) => a.replace(/^obj:/, '')).join(', ')}` : '';
  });
}

// ------------------------------------------------------------------ Propriedade / campo

function painelFolha(ctx: CtxPainel, pai: Entidade, caminho: readonly string[]): (Node | null)[] {
  const id = caminho[caminho.length - 1];
  const lista = arr<Record<string, unknown>>(pai.campos ?? pai.propriedades);
  const f = lista.find((x) => x.id === id);
  if (!f) return [h('p', { class: 'erro' }, `O item ${id} não foi encontrado no cadastro de ${String(pai.id)}.`)];
  const ehCampo = 'propriedades_api' in f;
  const ob = f.obrigatoriedade as Afirmacao & { valor?: string } | undefined;
  const df = f.default as Afirmacao & { forma?: string; valor?: unknown } | undefined;
  const dom = f.dominio as Afirmacao & { natureza?: string; valores?: { valor: string; significado?: string }[]; lista_completa?: string; contexto?: string } | undefined;
  const disp = f.disponibilidade as Record<string, string | null> | undefined;
  const pa = f.propriedades_api as Record<string, unknown> | undefined;
  const ref = f.referencia as { alvos?: string[]; nome_relacionamento?: string } | undefined;
  return [
    h('p', null, 'Pertence a ', h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho(caminho.slice(0, -1)) } }, String(pai.nome ?? pai.id))),
    texto('O que é', f.o_que_e, { didatico: true }),
    f.rotulo_didatico ? texto('Rótulo didático (não oficial)', f.rotulo_didatico) : null,
    h('dl', { class: 'kv' },
      h('dt', null, 'Nome técnico'), h('dd', null, String(f.nome)),
      h('dt', null, 'Tipo técnico'), h('dd', null, String(f.tipo_tecnico ?? '?'), f.tipo_explicado ? ` — ${String(f.tipo_explicado)}` : ''),
      f.cardinalidade ? [h('dt', null, 'Cardinalidade'), h('dd', null, valorEl(f.cardinalidade))] : null,
      f.herdada_de ? [h('dt', null, 'Herdada de'), h('dd', null, String(f.herdada_de))] : null,
      ehCampo ? [h('dt', null, 'APIs'), h('dd', null, arr<string>(f.apis).map((a) => NOME_API[a] ?? a).join(', ') || 'não informado')] : null,
      ehCampo ? [h('dt', null, 'Somente leitura'), h('dd', null, f.somente_leitura === null || f.somente_leitura === undefined ? 'desconhecido' : f.somente_leitura ? 'sim (representa/informa; não configura)' : 'não')] : null,
    ),
    afirmacao(ctx, 'Origem (padrão ou customizado)', f.origem as Afirmacao, (v) => ORIGEM[String(v)] ?? String(v)),
    afirmacao(ctx, 'Obrigatoriedade', ob ? { ...ob, valor: ob.valor ? OBRIGATORIEDADE[ob.valor] ?? ob.valor : undefined } : null),
    afirmacao(ctx, 'Valor padrão (default)', df ? { ...df, valor: df.forma ? (df.forma === 'valor' ? `${FORMA_DEFAULT.valor}: ${String(df.valor)}` : FORMA_DEFAULT[df.forma] ?? df.forma) : undefined } : null),
    dom ? dominioEl(ctx, dom) : null,
    disp ? h('p', null, h('strong', null, 'Disponibilidade: '), disp.desde_versao ? `desde ${disp.desde_versao}` : 'versão inicial não informada', disp.ate_versao ? ` · até ${disp.ate_versao}` : '', ' ', selo(disp.estado ?? undefined)) : null,
    ehCampo ? propsApi(ctx, pa) : null,
    ref?.alvos?.length ? h('div', { class: 'campo-txt' }, h('h4', null, 'Referência (lookup)'),
      h('ul', { class: 'lista-links' }, ref.alvos.map((a) => h('li', null, ctx.ind.no(a)
        ? h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrir(a, caminho) } }, `${ctx.rotulo(a)} (abrir objeto)`)
        : h('span', null, `${a} (objeto não catalogado)`)))),
      ref.nome_relacionamento ? h('p', null, `Nome do relacionamento: ${ref.nome_relacionamento}`) : null) : null,
    f.restricoes ? texto('Restrições', f.restricoes) : null,
    f.exemplo ? texto('Exemplo', f.exemplo, { didatico: true }) : null,
    listaTexto('Notas', arr(f.notas)),
    relacoes(ctx, id),
    secao('Fontes', true, fontesEl(ctx, arr(f.evidencias))),
    h('p', { class: 'linha-selos' }, 'Explicação: ', String(f.explicacao ?? '?'), ' · Estado: ', rotuloEstado(String(f.estado))),
    restantes(f, ['id', 'nome', 'tipo_tecnico', 'o_que_e', 'origem', 'obrigatoriedade', 'default', 'dominio', 'disponibilidade', 'explicacao', 'estado', 'evidencias', 'cardinalidade', 'estrutura_ref', 'herdada_de', 'notas', 'restricoes', 'rotulo_didatico', 'exemplo', 'tipo_explicado', 'apis', 'propriedades_api', 'somente_leitura', 'referencia']),
    f.estrutura_ref ? h('p', null, 'Tipo composto: ', h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho([...caminho, String(f.estrutura_ref)]) } }, ctx.rotulo(String(f.estrutura_ref)))) : null,
  ];
}

function dominioEl(ctx: CtxPainel, d: Afirmacao & { natureza?: string; valores?: { valor: string; significado?: string }[]; lista_completa?: string; contexto?: string }): HTMLElement {
  const vals = d.valores ?? [];
  const comp = d.lista_completa === 'sim' ? 'lista completa' : d.lista_completa === 'nao' ? 'lista parcial' : vals.length ? 'não se sabe se a lista é completa' : '';
  const ul = h('ul', { class: 'lista valores' });
  const filtro = vals.length > 12 ? h('input', { type: 'search', class: 'filtro-lista', placeholder: `Filtrar ${vals.length} valores…`, 'aria-label': 'Filtrar valores possíveis' }) : null;
  const render = () => {
    limpar(ul);
    const q = filtro?.value.trim().toLowerCase() ?? '';
    for (const v of vals.filter((x) => !q || x.valor.toLowerCase().includes(q) || (x.significado ?? '').toLowerCase().includes(q))) {
      ul.append(h('li', null, h('code', null, v.valor), v.significado ? ` — ${v.significado}` : h('span', { class: 'vazio' }, ' — significado não registrado')));
    }
  };
  filtro?.addEventListener('input', render);
  render();
  return h('div', { class: `afirmacao estado-${d.estado ?? 'nenhum'}` },
    h('h4', null, 'Valores possíveis', ' ', selo(d.estado)),
    h('p', null, NATUREZA_DOMINIO[d.natureza ?? ''] ?? d.natureza ?? 'não informado', comp ? ` · ${comp}` : ''),
    d.contexto ? h('p', { class: 'nota' }, d.contexto) : null,
    filtro, vals.length ? ul : null,
    fontesEl(ctx, d.evidencias));
}

function propsApi(ctx: CtxPainel, pa?: Record<string, unknown>): HTMLElement {
  if (!pa || pa.estado !== 'verificado') {
    return h('div', { class: 'afirmacao estado-desconhecido' }, h('h4', null, 'Propriedades de API (describe)', ' ', selo(String(pa?.estado ?? 'desconhecido'))),
      h('p', { class: 'vazio' }, 'Não extraídas com segurança. Não presumir leitura/escrita, nulabilidade nem filtros.'));
  }
  return h('div', { class: 'afirmacao estado-verificado' }, h('h4', null, 'Propriedades de API (describe)', ' ', selo('verificado')),
    h('table', { class: 'tabela-props' }, h('tbody', null, PROPRIEDADES_API.map(([k, rot]) => h('tr', null, h('th', { scope: 'row' }, rot), h('td', null, pa[k] === true ? 'sim' : pa[k] === false ? 'não' : 'não informado'))))),
    fontesEl(ctx, arr(pa.evidencias)));
}

// ------------------------------------------------------------------ relações, cobertura, utilidades

function relacoes(ctx: CtxPainel, id: string, incluirCampos = false): HTMLElement | null {
  const { saindo, entrando } = ctx.ind.relacoesTecnicas(id);
  let ent = entrando;
  // para objetos: também as referências que chegam a qualquer campo do objeto e as que saem dos campos
  let sai = saindo;
  if (incluirCampos) {
    for (const f of ctx.ind.folhasPorPai.get(id) ?? []) {
      const r = ctx.ind.relacoesTecnicas(f);
      sai = [...sai, ...r.saindo];
      ent = [...ent, ...r.entrando];
    }
  }
  if (!sai.length && !ent.length) return null;
  // campos/propriedades aparecem como Objeto.Campo, para não haver ambiguidade entre objetos
  const nome = (x: string) => {
    const n = ctx.ind.no(x);
    return n?.pai && (n.tipo === 'campo_api' || n.tipo === 'propriedade_xml') ? `${ctx.rotulo(n.pai)}.${n.rotulo}` : ctx.rotulo(x);
  };
  const item = (a: { origem: string; destino: string; tipo: string; rel_id?: string; estado?: string }, outro: string, dir: string) => h('li', null,
    h('span', { class: `selo ligacao-${LIGACAO[a.tipo]?.grupo ?? ''}` }, LIGACAO[a.tipo]?.rotulo ?? a.tipo), ' ', dir, ' ',
    h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrir(outro) } }, nome(outro)),
    ' ', selo(a.estado),
    a.rel_id ? h('button', { type: 'button', class: 'link link-sec', on: { click: () => ctx.abrirRelacao(a.rel_id!) } }, ' (por que se relacionam?)') : null);
  return secao(`Relações técnicas (${sai.length + ent.length})`, true,
    sai.length ? h('div', null, h('h4', null, 'Deste item para outros'), h('ul', { class: 'lista' }, sai.map((a) => item(a, a.destino, `${nome(a.origem)} →`)))) : null,
    ent.length ? h('div', null, h('h4', null, 'De outros itens para este'), h('ul', { class: 'lista' }, ent.map((a) => item(a, a.origem, '←')))) : null,
    h('p', { class: 'nota' }, 'Cada relação mostra seu estado de evidência; "por que se relacionam?" abre a ficha da relação com campos, cardinalidade e fontes.'));
}

function coberturaEl(e: Entidade): HTMLElement | null {
  const c = e.cobertura as Record<string, { estado?: string; esperado?: number | null; presente?: number; nota?: string }> | undefined;
  if (!c) return null;
  const linha = (k: string, rot: string) => {
    const x = c[k];
    if (!x) return null;
    return h('li', null, h('strong', null, `${rot}: `), x.estado ?? '?',
      x.presente !== undefined ? ` · ${x.presente} presente${x.presente === 1 ? '' : 's'}` : '',
      x.esperado !== undefined ? ` de ${x.esperado ?? 'universo não comprovado'}` : '',
      x.nota ? h('p', { class: 'nota' }, x.nota) : null);
  };
  return secao('Cobertura desta ficha', false, h('ul', { class: 'lista' }, linha('estrutural', 'Estrutural (itens listados)'), linha('explicativa', 'Explicativa (itens explicados)'), linha('mapeamento', 'Mapeamento XML ↔ API')));
}

function listaLinks(ctx: CtxPainel, titulo: string, ids: string[]): HTMLElement | null {
  if (!ids.length) return null;
  return h('div', { class: 'campo-txt' }, h('h4', null, titulo), h('ul', { class: 'lista-links' }, ids.map((i) => h('li', null, h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrir(i) } }, ctx.rotulo(i))))));
}

// ------------------------------------------------------------------ painel de relação (aresta)

export async function renderizarAresta(ctx: CtxPainel, alvo: HTMLElement, a: ArestaClicada): Promise<void> {
  const minha = ++geracao;
  limpar(alvo);
  const idDe = (chave: string) => chave.split('>').pop()!;
  const o = idDe(a.origem), d = idDe(a.destino);
  const lig = LIGACAO[a.ligacao];
  const cab = h('header', { class: 'cab-painel' },
    h('p', { class: 'tipo-no' }, h('span', { class: 'ico', 'aria-hidden': 'true' }, '↔'), a.tecnica ? 'Relação técnica' : 'Ligação de navegação'),
    h('h2', { id: 'titulo-painel', tabindex: -1 }, lig?.rotulo ?? a.ligacao),
    h('p', { class: 'migalhas' },
      h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho(a.origem.split('>')) } }, ctx.rotulo(o)), ' → ',
      h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrirCaminho(a.destino.split('>')) } }, ctx.rotulo(d))));
  alvo.append(cab);
  alvo.append(h('p', null, lig?.explicacao ?? ''));
  if (!a.tecnica) {
    alvo.append(h('p', { class: 'nota' }, 'Ligação da hierarquia didática do mapa: organiza a navegação e não afirma relação entre registros.'));
    if (a.motivo) alvo.append(texto('Motivo da classificação secundária', a.motivo)!);
    if (a.papel) alvo.append(texto('Papel da representação', a.papel, { didatico: true })!);
    return;
  }
  if (a.relId) {
    alvo.append(h('p', { class: 'carregando' }, 'Carregando ficha da relação…'));
    try {
      const r = await ctx.entidades.obter(a.relId);
      if (minha !== geracao) return;
      alvo.lastChild?.remove();
      alvo.append(...corpoRelacao(ctx, r).filter(Boolean) as Node[]);
    } catch (err) {
      if (minha !== geracao) return;
      alvo.append(h('p', { class: 'erro' }, `Não foi possível carregar a relação: ${String(err)}`));
    }
  }
}

export async function renderizarRelacaoPorId(ctx: CtxPainel, alvo: HTMLElement, relId: string): Promise<void> {
  const minha = ++geracao;
  limpar(alvo);
  alvo.append(h('p', { class: 'carregando' }, 'Carregando ficha da relação…'));
  const r = await ctx.entidades.obter(relId);
  if (minha !== geracao) return;
  limpar(alvo);
  alvo.append(h('header', { class: 'cab-painel' },
    h('p', { class: 'tipo-no' }, h('span', { class: 'ico', 'aria-hidden': 'true' }, '↔'), 'Relação técnica'),
    h('h2', { id: 'titulo-painel', tabindex: -1 }, LIGACAO[String(r.tipo)]?.rotulo ?? String(r.tipo))));
  alvo.append(...corpoRelacao(ctx, r).filter(Boolean) as Node[]);
}

function corpoRelacao(ctx: CtxPainel, r: Entidade): (Node | null)[] {
  const o = r.origem as { entidade: string; campo?: string };
  const d = r.destino as { entidade: string; campo?: string };
  const pt = (x: { entidade: string; campo?: string }) => {
    const alvoId = x.campo ? `${x.entidade}.${x.campo}` : x.entidade;
    return h('button', { type: 'button', class: 'link', on: { click: () => ctx.abrir(ctx.ind.no(alvoId) ? alvoId : x.entidade) } }, x.campo ? `${ctx.rotulo(x.entidade)}.${x.campo}` : ctx.rotulo(x.entidade));
  };
  return [
    h('dl', { class: 'kv' },
      h('dt', null, 'Origem'), h('dd', null, pt(o)),
      h('dt', null, 'Destino'), h('dd', null, pt(d)),
      h('dt', null, 'Tipo'), h('dd', null, LIGACAO[String(r.tipo)]?.rotulo ?? String(r.tipo)),
      r.natureza_correspondencia ? [h('dt', null, 'Natureza da correspondência'), h('dd', null, String(r.natureza_correspondencia))] : null,
      h('dt', null, 'Estado'), h('dd', null, selo(String(r.estado)))),
    texto('Por que se relacionam', r.explicacao, { didatico: true }),
    r.cardinalidade_registros ? afirmacao(ctx, 'Cardinalidade entre registros', r.cardinalidade_registros as Afirmacao) : h('p', { class: 'vazio' }, 'Cardinalidade entre registros não registrada.'),
    r.condicao ? texto('Condição', r.condicao) : null,
    h('p', { class: 'nota' }, 'Quantidade de representações técnicas não é cardinalidade entre registros. Campos opcionais não estão necessariamente preenchidos em todo registro.'),
    secao('Fontes', true, fontesEl(ctx, arr(r.evidencias))),
    restantes(r, ['id', 'tipo', 'origem', 'destino', 'explicacao', 'estado', 'evidencias', 'cardinalidade_registros', 'condicao', 'natureza_correspondencia']),
  ];
}

export { TIPOS_OBJETO };
