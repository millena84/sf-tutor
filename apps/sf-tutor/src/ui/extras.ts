// Método, legenda, filtros e busca: blocos de interface fora do painel.
import type { DadosBase } from '../data/tipos';
import type { Indice } from '../model/adaptador';
import type { IndiceBusca } from '../model/busca';
import { filtrosAtivos, type Filtros } from '../model/filtros';
import type { Cores } from '../cores';
import { ESTADO, LIGACAO, NOME_TIPO, NOME_TIPO_LEGENDA, ICONE_TIPO } from '../rotulos';
import { h, limpar } from './dom';

// ------------------------------------------------------------------ Método

export function conteudoMetodo(d: DadosBase, salesforce: Record<string, unknown> | null): HTMLElement {
  const vb = (salesforce?.versao_base ?? d.manifesto.versao_base) as Record<string, string>;
  const cob = d.cobertura as Record<string, Record<string, unknown>>;
  const mdt = cob.metadata_types ?? {};
  const obj = cob.objetos_api ?? {};
  const props = cob.propriedades ?? {};
  const rels = cob.relacionamentos ?? {};
  const tax = cob.taxonomia ?? {};
  const nt = d.manifesto.contagens.nos_por_tipo;
  return h('div', { class: 'metodo' },
    h('h3', null, 'De onde vêm as informações'),
    h('p', null, 'O conteúdo vem da base de insumos do projeto (ai-help/claude/insumos-grafo/ no repositório sf-tutor). Cada afirmação técnica cita a fonte: documentação oficial da Salesforce (Object Reference, Metadata API, Tooling API, Field Reference e Ajuda), evidência de schema (registro do Salesforce CLI) ou observação autorizada em org. Esta versão não tem observações em org: toda validação é documental.'),
    h('p', null, 'Os temas (e os temas dentro deles) são curadoria didática do projeto, não nomenclatura oficial da Salesforce. Nos dados, esses dois níveis se chamam classificação e subclassificação; "tema" é a tradução didática usada na tela. As explicações são redação do projeto a partir das fontes citadas e estão marcadas como tal.'),
    h('h3', null, 'Ligações, datas e nível de evidência'),
    h('p', null, 'Cada ligação técnica (referência entre campos, correspondência XML ↔ API) tem ficha própria com explicação, campos, cardinalidade quando verificada, condições, fontes e data de verificação. O nível de evidência aparece no traço da linha:'),
    h('ul', { class: 'lista' },
      h('li', null, h('span', { class: 'amostra-linha solida' }), ' linha contínua: verificado'),
      h('li', null, h('span', { class: 'amostra-linha tracejada' }), ' linha tracejada: desconhecido (sem evidência suficiente)'),
      h('li', null, h('span', { class: 'amostra-linha pontilhada' }), ' linha pontilhada: não exposto, bloqueado ou não aplicável')),
    h('p', null, 'As ligações da hierarquia (centro → tema → funcionalidade…) organizam a navegação e não afirmam relação entre registros.'),
    h('h3', null, 'Estados de validação'),
    h('dl', { class: 'kv' }, Object.entries(ESTADO).flatMap(([, e]) => [h('dt', null, `${e.simbolo} ${e.rotulo}`), h('dd', null, e.explicacao)])),
    h('h3', null, 'Versão e cobertura desta publicação'),
    h('dl', { class: 'kv' },
      h('dt', null, 'API Salesforce'), h('dd', null, `${vb?.api_version ?? '?'} (${vb?.release ?? '?'}), referência ${vb?.data_referencia ?? '?'}`),
      h('dt', null, 'Contrato de dados'), h('dd', null, `${d.manifesto.contrato.nome} ${d.manifesto.contrato.versao}`),
      h('dt', null, 'Insumos'), h('dd', null, d.build.commit ? `commit ${d.build.commit}` : 'commit não informado', d.build.data_build ? `, build em ${d.build.data_build}` : ''),
      h('dt', null, 'No mapa'), h('dd', null, `${nt.funcionalidade ?? 0} funcionalidades, ${nt.metadata_type ?? 0} metadata types, ${(nt.objeto_api ?? 0) + (nt.objeto_api_juncao ?? 0)} objetos API, ${nt.propriedade_xml ?? 0} propriedades XML, ${nt.campo_api ?? 0} campos, ${d.manifesto.contagens.fontes} fontes registradas`),
      h('dt', null, 'Metadata types'), h('dd', null, `${mdt.cadastrados ?? '?'} cadastrados de ${mdt.universo_v68 ?? '?'} da v68; ${mdt.estruturalmente_completos ?? '?'} com estrutura completa; ${mdt.completos_nas_tres_dimensoes ?? '?'} completos nas três dimensões (estrutura, explicação e mapeamento)`),
      h('dt', null, 'Objetos e campos'), h('dd', null, `${obj.catalogados ?? '?'} objetos; ${obj.campos_listados ?? '?'} campos listados e ${obj.campos_explicados ?? '?'} explicados. ${obj.nota_universo ?? ''}`),
      props && Object.keys(props).length ? [h('dt', null, 'Propriedades'), h('dd', null, resumo(props))] : null,
      rels && Object.keys(rels).length ? [h('dt', null, 'Relacionamentos'), h('dd', null, resumo(rels))] : null,
      tax && Object.keys(tax).length ? [h('dt', null, 'Taxonomia'), h('dd', null, resumo(tax))] : null,
    ),
    h('p', { class: 'nota' }, 'Cobertura parcial é esperada: o inventário completo ainda está em construção. Itens não catalogados aparecem como "ainda não mapeado" e nunca são preenchidos por suposição.'),
    h('h3', null, 'Uso de IA'),
    h('p', null, 'A coleta, a agregação e a redação dos insumos foram feitas com o Claude (Anthropic), a partir das fontes citadas, com revisão humana do projeto. Esta página não usa IA em tempo de execução: nada é gerado no navegador, e lacunas ficam visíveis como lacunas.'),
    h('h3', null, 'Marca e afiliação'),
    h('p', null, 'O sf-tutor é um projeto do canal Desbugando (tecnologia sem mistério); o logo do cabeçalho é a marca Desbugando.'),
    h('p', null, 'Salesforce e os nomes de produtos são marcas da Salesforce, Inc. Este projeto é independente e não é afiliado nem endossado pela Salesforce. Os logos do centro e das nuvens são exibidos por referência aos endereços oficiais registrados nos insumos (config/marcas.json): ao abrir o tutorial, seu navegador também acessa esses servidores da Salesforce. Se a imagem não carregar, aparece um substituto identificado.'),
    h('h3', null, 'Segurança'),
    h('p', null, 'A página não pede nem guarda credenciais Salesforce e não se conecta a nenhuma org. Exemplos de SOQL e XML são apenas texto copiável; nada é executado ao clicar.'),
  );
}

function resumo(o: Record<string, unknown>): string {
  return Object.entries(o).filter(([, v]) => typeof v === 'number' || typeof v === 'string').map(([k, v]) => `${k.replace(/_/g, ' ')}: ${String(v)}`).join('; ');
}

// ------------------------------------------------------------------ Legenda

export function conteudoLegenda(cores: Cores, visao: 'funcionalidade' | 'nuvem', rotulo: (id: string) => string): HTMLElement {
  const tipos: (keyof typeof NOME_TIPO)[] = ['salesforce', 'nuvem', 'classificacao', 'subclassificacao', 'funcionalidade', 'metadata_type', 'estrutura_auxiliar', 'propriedade_xml', 'objeto_api', 'objeto_api_juncao', 'campo_api'];
  const ligs = ['classificacao_principal', 'classificacao_secundaria', 'representacao_xml', 'tipo_composto', 'referencia_campo', 'correspondencia_xml_api', 'representacao_comum'];
  const escala = visao === 'funcionalidade' ? cores.entradasClassificacao() : cores.entradasNuvem();
  return h('div', { class: 'legenda-conteudo' },
    h('h3', null, 'Tipos de nó'),
    h('p', { class: 'nota' }, 'Forma, borda e sigla distinguem os tipos; a cor indica o contexto.'),
    h('p', { class: 'nota' }, 'Arrastar um item leva junto os itens abaixo dele no ramo; com Shift, move só o item. "Reorganizar" desfaz os arrastes da visão atual.'),
    h('ul', { class: 'lista-legenda' }, tipos.map((t) => h('li', null, h('span', { class: `ico ico-${t}`, 'aria-hidden': 'true' }, ICONE_TIPO[t] || '●'), NOME_TIPO_LEGENDA[t] ?? NOME_TIPO[t]))),
    h('h3', null, 'Ligações'),
    h('ul', { class: 'lista-legenda' }, ligs.map((l) => h('li', null, h('span', { class: `amostra-lig lig-${l}`, 'aria-hidden': 'true' }), LIGACAO[l].rotulo))),
    h('h3', null, 'Traço = nível de evidência'),
    h('ul', { class: 'lista-legenda' },
      h('li', null, h('span', { class: 'amostra-linha solida' }), 'verificado'),
      h('li', null, h('span', { class: 'amostra-linha tracejada' }), 'desconhecido'),
      h('li', null, h('span', { class: 'amostra-linha pontilhada' }), 'não exposto / bloqueado / não aplicável')),
    h('h3', null, visao === 'funcionalidade' ? 'Cores por tema' : 'Cores por nuvem'),
    h('ul', { class: 'lista-legenda cores' }, escala.map(([id, cor]) => h('li', null, h('span', { class: 'amostra-cor', style: `background:${cor}`, 'aria-hidden': 'true' }), rotulo(id)))),
  );
}

// ------------------------------------------------------------------ Filtros

export function conteudoFiltros(ind: Indice, f: Filtros, rotulo: (id: string) => string, aoMudar: () => void, ocultos: number): HTMLElement {
  const nuvens = [...ind.nos.values()].filter((n) => n.tipo === 'nuvem');
  const clss = [...ind.nos.values()].filter((n) => n.tipo === 'classificacao');
  const grupo = (titulo: string, opcoes: [string, string][], conj: Set<string>) => h('fieldset', null, h('legend', null, titulo),
    opcoes.map(([v, r]) => {
      const cb = h('input', { type: 'checkbox', value: v });
      cb.checked = conj.has(v);
      cb.addEventListener('change', () => { if (cb.checked) conj.add(v); else conj.delete(v); aoMudar(); });
      return h('label', { class: 'opcao' }, cb, ` ${r}`);
    }));
  const sel = h('select', { 'aria-label': 'Representação técnica' },
    ...[['todas', 'Todas'], ['com_xml', 'Com metadata type (XML)'], ['com_api', 'Com objeto API'], ['sem_xml', 'Sem XML (ex.: Usuários)']].map(([v, r]) => {
      const o = h('option', { value: v }, r);
      if (f.representacao === v) o.selected = true;
      return o;
    }));
  sel.addEventListener('change', () => { f.representacao = sel.value as Filtros['representacao']; aoMudar(); });
  const limparBtn = h('button', { type: 'button', class: 'btn' }, 'Limpar filtros');
  limparBtn.addEventListener('click', () => { f.nuvens.clear(); f.classificacoes.clear(); f.apis.clear(); f.estados.clear(); f.representacao = 'todas'; aoMudar(); });
  return h('div', { class: 'filtros-conteudo' },
    h('p', { class: 'nota', role: 'status' }, `${filtrosAtivos(f)} filtro(s) ativo(s). ${ocultos} item(ns) esmaecido(s) no mapa. Itens filtrados não somem: ficam esmaecidos, para as relações continuarem corretas, e o painel explica o motivo.`),
    grupo('Nuvem / produto', nuvens.map((n) => [n.id, n.rotulo]), f.nuvens),
    grupo('Tema', clss.map((c) => [c.id, rotulo(c.id)]), f.classificacoes),
    h('fieldset', null, h('legend', null, 'Representação'), sel),
    grupo('Família de API (objetos e campos)', [['padrao', 'API padrão'], ['tooling', 'Tooling API']], f.apis),
    grupo('Estado de validação', Object.entries(ESTADO).map(([k, e]) => [k, e.rotulo]), f.estados),
    limparBtn);
}

// ------------------------------------------------------------------ Busca

export interface CtxBusca {
  indice: IndiceBusca;
  ind: Indice;
  rotulo(id: string): string;
  oculto(id: string): string | null;
  abrir(id: string): void;
}

export function ligarBusca(input: HTMLInputElement, lista: HTMLElement, ctx: CtxBusca): void {
  let ativo = -1;
  let itens: HTMLElement[] = [];
  const fechar = () => { lista.hidden = true; input.setAttribute('aria-expanded', 'false'); ativo = -1; input.removeAttribute('aria-activedescendant'); };
  const render = () => {
    limpar(lista);
    const rs = ctx.indice.buscar(input.value);
    itens = [];
    if (input.value.trim().length < 2) { fechar(); return; }
    if (!rs.length) {
      lista.append(h('li', { class: 'vazio', role: 'option', 'aria-disabled': 'true' }, 'Nada encontrado. Tente o nome técnico (ex.: ProfileId) ou um termo em português.'));
    }
    rs.forEach((r, i) => {
      const n = ctx.ind.no(r.item.id);
      const contexto = r.item.pai ? ctx.rotulo(r.item.pai) : (ctx.ind.funcionalidadesDe(r.item.id)[0] ? ctx.rotulo(ctx.ind.funcionalidadesDe(r.item.id)[0]) : '');
      const oc = ctx.oculto(r.item.id);
      const li = h('li', { role: 'option', id: `res-${i}`, class: 'resultado', 'aria-selected': 'false' },
        h('span', { class: `ico ico-${r.item.tipo}`, 'aria-hidden': 'true' }, ICONE_TIPO[r.item.tipo] || n?.sigla?.slice(0, 3) || '•'),
        h('span', { class: 'res-texto' },
          h('span', { class: 'res-rot' }, r.item.rotulo),
          h('span', { class: 'res-meta' }, `${NOME_TIPO[r.item.tipo]}${contexto ? ` · ${contexto}` : ''} · casou por ${r.motivo}`),
          oc ? h('span', { class: 'res-oculto' }, `Esmaecido pelos filtros: ${oc}`) : null));
      li.addEventListener('mousedown', (ev) => { ev.preventDefault(); escolher(i); });
      itens.push(li);
      lista.append(li);
    });
    lista.hidden = false;
    input.setAttribute('aria-expanded', 'true');
  };
  const escolher = (i: number) => {
    const rs = ctx.indice.buscar(input.value);
    const r = rs[i];
    if (!r) return;
    fechar();
    ctx.abrir(r.item.id);
  };
  const marcar = (i: number) => {
    itens.forEach((x, k) => x.setAttribute('aria-selected', String(k === i)));
    ativo = i;
    if (itens[i]) { input.setAttribute('aria-activedescendant', itens[i].id); itens[i].scrollIntoView({ block: 'nearest' }); }
  };
  input.addEventListener('input', render);
  input.addEventListener('focus', () => { if (input.value.trim().length >= 2) render(); });
  input.addEventListener('blur', () => setTimeout(fechar, 150));
  input.addEventListener('keydown', (ev) => {
    if (ev.key === 'ArrowDown') { marcar(Math.min(ativo + 1, itens.length - 1)); ev.preventDefault(); }
    else if (ev.key === 'ArrowUp') { marcar(Math.max(ativo - 1, 0)); ev.preventDefault(); }
    else if (ev.key === 'Enter') { escolher(ativo >= 0 ? ativo : 0); ev.preventDefault(); }
    else if (ev.key === 'Escape') { fechar(); }
  });
}
