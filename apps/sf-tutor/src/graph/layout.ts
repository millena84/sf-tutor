// Layout em leque, incremental e determinístico: itens já posicionados não se movem ao expandir outros
// (preserva a localização mental). Filhos ficam ao redor do pai, na direção oposta ao avô.
import type { Cena } from '../model/adaptador';
import { TAMANHO_PAGINA } from '../model/adaptador';

export interface Ponto { x: number; y: number }

export function posicionar(cena: Cena, anteriores: Map<string, Ponto>, tamanhoPagina = TAMANHO_PAGINA): Map<string, Ponto> {
  const pos = new Map<string, Ponto>();
  const filhosDe = new Map<string, string[]>();
  for (const o of cena.ocorrencias) if (o.paiChave) lista(filhosDe, o.paiChave).push(o.chave);
  for (const p of cena.paginacoes) lista(filhosDe, p.paiChave).push(p.chave);
  const paiDe = new Map<string, string | null>();
  for (const o of cena.ocorrencias) paiDe.set(o.chave, o.paiChave);
  for (const p of cena.paginacoes) paiDe.set(p.chave, p.paiChave);
  const ordem = [...cena.ocorrencias.map((o) => o.chave), ...cena.paginacoes.map((p) => p.chave)];
  for (const chave of ordem) {
    const ant = anteriores.get(chave);
    if (ant) { pos.set(chave, ant); continue; }
    const pai = paiDe.get(chave) ?? null;
    if (!pai) { pos.set(chave, { x: 0, y: 0 }); continue; }
    const P = pos.get(pai) ?? anteriores.get(pai) ?? { x: 0, y: 0 };
    const avo = paiDe.get(pai) ?? null;
    const irmaos = filhosDe.get(pai) ?? [chave];
    const i = irmaos.indexOf(chave);
    const anel = Math.floor(i / tamanhoPagina);
    const noAnel = Math.min(tamanhoPagina, irmaos.length - anel * tamanhoPagina);
    const j = i % tamanhoPagina;
    if (!avo) {
      const r = Math.max(210, noAnel * 26) + anel * 90;
      const a = (2 * Math.PI * j) / noAnel - Math.PI / 2;
      pos.set(chave, { x: P.x + r * Math.cos(a), y: P.y + r * Math.sin(a) });
      continue;
    }
    const G = pos.get(avo) ?? anteriores.get(avo) ?? { x: 0, y: 0 };
    const dir = Math.atan2(P.y - G.y, P.x - G.x);
    // ~75px de arco entre irmãos para os rótulos não se sobreporem
    const passo = 0.42;
    const abertura = Math.min(1.7 * Math.PI, Math.max(0.5, (noAnel - 1) * passo));
    const r = Math.max(200, (75 * Math.max(noAnel - 1, 1)) / abertura) + anel * 90;
    const a = noAnel === 1 ? dir : dir - abertura / 2 + (abertura * j) / (noAnel - 1);
    pos.set(chave, { x: P.x + r * Math.cos(a), y: P.y + r * Math.sin(a) });
  }
  return pos;
}

function lista<K, V>(m: Map<K, V[]>, k: K): V[] {
  let l = m.get(k);
  if (!l) { l = []; m.set(k, l); }
  return l;
}
