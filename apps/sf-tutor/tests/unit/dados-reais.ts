// Carrega a projeção real direto da base de insumos (não da cópia em public/), para os testes unitários.
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import type { DadosBase } from '../../src/data/tipos';

const SITE = resolve(dirname(fileURLToPath(import.meta.url)), '../../../../ai-help/claude/insumos-grafo/gerado/site');
const ler = <T>(f: string): T => JSON.parse(readFileSync(resolve(SITE, f), 'utf8')) as T;

export function dadosReais(): DadosBase {
  const manifesto = ler<DadosBase['manifesto']>('manifest.json');
  const g = ler<{ nos: DadosBase['nos']; arestas: DadosBase['arestas'] }>('grafo-base.json');
  return {
    manifesto, nos: g.nos, arestas: g.arestas,
    visoes: ler('visoes.json'), busca: ler('busca.json'), fontes: ler('fontes.json'), cobertura: ler('cobertura.json'),
    build: { commit: null, data_build: '', origem: 'teste' },
  };
}
export const entidadeReal = (rel: string) => ler<Record<string, unknown>>(`entidades/${rel}`);
