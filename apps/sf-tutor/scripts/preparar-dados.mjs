// Copia a projeção gerada (ai-help/claude/insumos-grafo/gerado/site) para public/data.
// public/data é CÓPIA GERADA (ignorada no git): a única fonte é a base de insumos.
// Sem --sem-validar, regenera e valida a base antes (python3 ferramentas/sftutor.py tudo) e falha se houver erro.
import { execFileSync } from 'node:child_process';
import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const app = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const insumos = resolve(app, '../../ai-help/claude/insumos-grafo');
const origem = join(insumos, 'gerado/site');
const destino = join(app, 'public/data');
const semValidar = process.argv.includes('--sem-validar');

if (!existsSync(insumos)) {
  console.error(`Base de insumos não encontrada em ${insumos}`);
  process.exit(1);
}
if (!semValidar) {
  console.log('Validando e regenerando a base (ferramentas/sftutor.py tudo)…');
  try {
    execFileSync('python3', ['ferramentas/sftutor.py', 'tudo'], { cwd: insumos, stdio: 'inherit' });
  } catch {
    console.error('A validação da base falhou. Corrija os insumos antes de gerar o site (ou use dados:sem-validar só para depurar a interface).');
    process.exit(1);
  }
}
if (!existsSync(join(origem, 'manifest.json'))) {
  console.error(`Projeção do site não encontrada em ${origem}. Rode "python3 ferramentas/sftutor.py gerar".`);
  process.exit(1);
}

rmSync(destino, { recursive: true, force: true });
rmSync(join(app, 'public/__teste-sintetico'), { recursive: true, force: true });
mkdirSync(destino, { recursive: true });

// cópia minificada (JSON) preservando a estrutura de pastas
let arquivos = 0;
let bytes = 0;
function copiar(de, para) {
  for (const nome of readdirSync(de)) {
    const a = join(de, nome);
    const b = join(para, nome);
    if (statSync(a).isDirectory()) {
      mkdirSync(b, { recursive: true });
      copiar(a, b);
    } else if (nome.endsWith('.json')) {
      const txt = JSON.stringify(JSON.parse(readFileSync(a, 'utf8')));
      writeFileSync(b, txt);
      arquivos++;
      bytes += txt.length;
    } else {
      cpSync(a, b);
    }
  }
}
copiar(origem, destino);

let commit = null;
try {
  commit = execFileSync('git', ['rev-parse', '--short', 'HEAD'], { cwd: insumos }).toString().trim();
  const sujo = execFileSync('git', ['status', '--porcelain', '--', '.'], { cwd: insumos }).toString().trim();
  if (sujo) commit += '+alterações-locais';
} catch {
  /* fora de um repositório git */
}
writeFileSync(join(destino, 'build-info.json'), JSON.stringify({
  commit,
  data_build: new Date().toISOString(),
  origem: 'ai-help/claude/insumos-grafo/gerado/site',
}));
console.log(`Dados copiados: ${arquivos} arquivos JSON (${(bytes / 1024).toFixed(0)} KiB) → public/data${semValidar ? ' (SEM validar a base)' : ''}`);
