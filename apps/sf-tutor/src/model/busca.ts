// Busca global sobre busca.json (cobre todos os nós, inclusive campos e propriedades ainda não desenhados).
import type { ItemBusca } from '../data/tipos';

export function normalizar(s: string): string {
  return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
}

export interface Resultado {
  item: ItemBusca;
  pontos: number;
  motivo: string; // onde casou (rótulo, alias, descrição)
}

interface Preparado {
  item: ItemBusca;
  rotulo: string;
  textos: string[];
  descricao: string;
  nomeCurto: string; // para campos/propriedades: só o nome após o ponto
}

export class IndiceBusca {
  private itens: Preparado[];
  constructor(itens: ItemBusca[]) {
    this.itens = itens.map((item) => ({
      item,
      rotulo: normalizar(item.rotulo),
      textos: item.textos.map(normalizar),
      descricao: normalizar(item.descricao ?? ''),
      nomeCurto: normalizar(item.id.includes('.') ? item.id.slice(item.id.lastIndexOf('.') + 1) : item.rotulo),
    }));
  }

  buscar(consulta: string, limite = 40): Resultado[] {
    const q = normalizar(consulta);
    if (q.length < 2) return [];
    const termos = q.split(/\s+/).filter(Boolean);
    const out: Resultado[] = [];
    for (const p of this.itens) {
      let pontos = 0;
      let motivo = '';
      const idn = normalizar(p.item.id);
      if (p.rotulo === q || p.nomeCurto === q) { pontos = 100; motivo = 'nome'; }
      else if (idn === q || idn.endsWith(':' + q) || idn.endsWith('.' + q)) { pontos = 95; motivo = 'nome técnico'; }
      else if (p.rotulo.startsWith(q) || p.nomeCurto.startsWith(q)) { pontos = 80; motivo = 'nome'; }
      else if (p.textos.some((t) => t === q)) { pontos = 75; motivo = 'alias'; }
      else if (p.textos.some((t) => t.startsWith(q))) { pontos = 65; motivo = 'alias'; }
      else if (termos.every((t) => p.rotulo.includes(t) || p.textos.some((x) => x.includes(t)) || idn.includes(t))) { pontos = 50; motivo = 'nome ou alias'; }
      else if (p.descricao && termos.every((t) => p.descricao.includes(t))) { pontos = 30; motivo = 'descrição'; }
      if (!pontos) continue;
      // estruturas maiores primeiro em empate: funcionalidade > objeto/xml > campo
      pontos += PESO_TIPO[p.item.tipo] ?? 0;
      out.push({ item: p.item, pontos, motivo });
    }
    out.sort((a, b) => b.pontos - a.pontos || a.item.rotulo.localeCompare(b.item.rotulo));
    return out.slice(0, limite);
  }
}

const PESO_TIPO: Record<string, number> = {
  funcionalidade: 6, nuvem: 6, classificacao: 5, subclassificacao: 4, metadata_type: 4, objeto_api: 4, objeto_api_juncao: 4,
  estrutura_auxiliar: 2, propriedade_xml: 1, campo_api: 1, salesforce: 6,
};
