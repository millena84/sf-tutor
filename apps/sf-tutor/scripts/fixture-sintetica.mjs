// FIXTURE SINTÉTICA DE PERFORMANCE — NÃO É CONTEÚDO SALESFORCE.
// Gera public/__teste-sintetico/ no formato do contrato sf-tutor-site 1.0.0, com volume muito maior
// que a base real, para medir carga, expansão, paginação e busca. Todo rótulo começa com "SINT".
// A interface mostra a faixa "DADOS SINTÉTICOS DE TESTE" quando carrega estes dados (?dados=sintetico).
import { mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const app = resolve(dirname(fileURLToPath(import.meta.url)), '..');
// destino: argumento (ex.: dist/__teste-sintetico, usado pelo teste de performance) ou public/__teste-sintetico (dev)
const out = resolve(app, process.argv[2] ?? 'public/__teste-sintetico');
const N = { nuvens: 4, cls: 14, subPorCls: 6, funcs: 600, mdts: 1200, propsPorMdt: 30, objs: 1200, camposPorObj: 30, objGigante: 3000 };

rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
const nos = [];
const arestas = [];
const busca = [];
const ents = new Map();
const no = (id, tipo, rotulo, extra = {}) => { nos.push({ id, tipo, rotulo, estado: 'verificado', ...extra }); busca.push({ id, tipo, rotulo, textos: [rotulo, id] }); };
const folha = (id, tipo, rotulo, pai) => busca.push({ id, tipo, rotulo, textos: [rotulo, id], pai, descricao: 'SINT dado sintético' });
const ev = [{ fonte: 'src:sintetica' }];

no('salesforce', 'salesforce', 'SINT Centro');
ents.set('salesforce', { id: 'salesforce', nome: 'SINT Centro', o_que_e: 'Fixture sintética de performance.', estado: 'verificado', evidencias: ev, classificacoes: [], nuvens: [] });
const nuvens = [];
for (let i = 0; i < N.nuvens; i++) { const id = `nuv:sint-${i}`; nuvens.push(id); no(id, 'nuvem', `SINT Nuvem ${i}`, { sigla: `N${i}` }); arestas.push({ origem: 'salesforce', destino: id, tipo: 'navegacao_nuvem' }); }
const subs = [];
const clsIds = [];
for (let c = 0; c < N.cls; c++) {
  const cid = `cls:sint-${c}`; clsIds.push(cid);
  no(cid, 'classificacao', `SINT Classificação ${c}`, { sigla: `C${c}` });
  arestas.push({ origem: 'salesforce', destino: cid, tipo: 'navegacao_classificacao' });
  for (let s = 0; s < N.subPorCls; s++) {
    const sid = `sub:sint-${c}-${s}`; subs.push({ sid, cid });
    no(sid, 'subclassificacao', `SINT Sub ${c}.${s}`, { sigla: `S${c}${s}`, grupo_cor: cid });
    arestas.push({ origem: cid, destino: sid, tipo: 'navegacao_subclassificacao' });
  }
}
const funcsPorSub = new Map(subs.map((s) => [s.sid, []]));
const funcsPorNuvem = new Map(nuvens.map((n) => [n, []]));
for (let f = 0; f < N.funcs; f++) {
  const id = `func:sint-${f}`;
  const sub = subs[f % subs.length];
  no(id, 'funcionalidade', `SINT Funcionalidade ${f}`, { grupo_cor: sub.cid });
  funcsPorSub.get(sub.sid).push(id);
  arestas.push({ origem: sub.sid, destino: id, tipo: 'classificacao_principal' });
  const nv = nuvens[f % nuvens.length];
  funcsPorNuvem.get(nv).push(id);
  arestas.push({ origem: nv, destino: id, tipo: 'nuvem_funcionalidade' });
}
function mdt(i, nProps) {
  const id = `mdt:SintType${i}`;
  no(id, 'metadata_type', `SintType${i}`, { apis: ['metadata'] });
  arestas.push({ origem: `func:sint-${i % N.funcs}`, destino: id, tipo: 'representacao_xml' });
  const props = [];
  for (let p = 0; p < nProps; p++) { const pid = `${id}.prop${p}`; folha(pid, 'propriedade_xml', `prop${p}`, id); props.push({ id: pid, nome: `prop${p}`, o_que_e: 'SINT', estado: 'verificado', evidencias: ev }); }
  ents.set(id, { id, nome: `SintType${i}`, o_que_e: 'SINT metadata type sintético.', estado: 'verificado', evidencias: ev, propriedades: props });
}
function obj(i, nCampos) {
  const id = `obj:SintObj${i}`;
  no(id, 'objeto_api', `SintObj${i}`, { apis: ['padrao'] });
  arestas.push({ origem: `func:sint-${i % N.funcs}`, destino: id, tipo: 'representacao_objeto_api' });
  const campos = [];
  for (let p = 0; p < nCampos; p++) { const fid = `${id}.Campo${p}__c`; folha(fid, 'campo_api', `Campo${p}__c`, id); campos.push({ id: fid, nome: `Campo${p}__c`, o_que_e: 'SINT', estado: 'verificado', evidencias: ev }); }
  if (i > 0) arestas.push({ origem: `${id}.Campo0__c`, destino: `obj:SintObj${i - 1}`, tipo: 'referencia_campo', estado: 'verificado' });
  ents.set(id, { id, nome: `SintObj${i}`, o_que_e: 'SINT objeto sintético.', estado: 'verificado', evidencias: ev, campos });
}
for (let i = 0; i < N.mdts; i++) mdt(i, N.propsPorMdt);
obj(0, N.objGigante); // lista gigante para paginação
for (let i = 1; i < N.objs; i++) obj(i, N.camposPorObj);

const ramo = (id, filhos) => ({ id, filhos });
const visoes = {
  por_funcionalidade: ramo('salesforce', clsIds.map((cid) => ramo(cid, subs.filter((s) => s.cid === cid).map((s) => ramo(s.sid, funcsPorSub.get(s.sid).map((f) => ({ id: f, ocorrencia: 'principal', filhos: [] }))))))),
  por_nuvem: ramo('salesforce', nuvens.map((n) => ramo(n, funcsPorNuvem.get(n).map((f) => ({ id: f, filhos: [] }))))),
};
const contagem = {};
for (const b of busca) contagem[b.tipo] = (contagem[b.tipo] ?? 0) + 1;
const manifesto = {
  contrato: { nome: 'sf-tutor-site', versao: '1.0.0' },
  versao_base: { api_version: 'SINTÉTICO', release: 'fixture de performance', data_referencia: 'n/a', escopo: 'n/a' },
  arquivos: { grafo_base: 'grafo-base.json', visoes: 'visoes.json', busca: 'busca.json', fontes: 'fontes.json', cobertura: 'cobertura.json', entidades: 'entidades/<prefixo>/<nome>.json' },
  contagens: { nos_por_tipo: contagem, entidades: ents.size, fontes: 1, arestas: arestas.length, arestas_base: arestas.length },
  regras: ['FIXTURE SINTÉTICA DE PERFORMANCE: não é conteúdo Salesforce.'],
  nota: 'Gerado por apps/sf-tutor/scripts/fixture-sintetica.mjs. Somente para teste de performance.',
};
const w = (rel, obj) => { const p = join(out, rel); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, JSON.stringify(obj)); };
w('manifest.json', manifesto);
w('grafo-base.json', { nos, arestas });
w('visoes.json', visoes);
w('busca.json', busca);
w('fontes.json', { 'src:sintetica': { titulo: 'FIXTURE SINTÉTICA (não é fonte real)', url: 'https://example.invalid/', tipo: 'sintetica', versao: 'n/a', data_verificacao: 'n/a', metodo: 'gerado' } });
w('cobertura.json', { sintetico: true });
w('build-info.json', { commit: null, data_build: new Date().toISOString(), origem: 'fixture sintética de performance', sintetico: true });
for (const [id, e] of ents) {
  const i = id.indexOf(':');
  w(id === 'salesforce' ? 'entidades/salesforce.json' : `entidades/${id.slice(0, i)}/${encodeURIComponent(id.slice(i + 1))}.json`, e);
}
console.log(`Fixture sintética: ${busca.length} nós (${JSON.stringify(contagem)}), ${arestas.length} arestas, ${ents.size} entidades → ${out}`);
