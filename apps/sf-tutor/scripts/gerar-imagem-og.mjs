// Gera a imagem de prévia do link (Open Graph), 1200×627, em public/og/metadata-desbugado.png.
// Usa os desenhos de public/marca/ (logo do produto e bug Desbugando) e a paleta do site.
// A imagem gerada é versionada: o build e o CI não rodam este script.
//
// Uso: node scripts/gerar-imagem-og.mjs   (CHROME=<caminho> para usar outro Chromium)
import { chromium } from '@playwright/test';
import { readFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const app = join(dirname(fileURLToPath(import.meta.url)), '..');
const svg = (nome) => 'data:image/svg+xml;base64,' + Buffer.from(readFileSync(join(app, 'public/marca', nome))).toString('base64');
const saida = join(app, 'public/og/metadata-desbugado.png');

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; margin: 0; }
  body { width: 1200px; height: 627px; overflow: hidden; font-family: Inter, system-ui, sans-serif; color: #F5F7FF;
    background: radial-gradient(circle at 22% 45%, #2A1D5C 0, #1C1440 38%, #0B0F2A 75%); }
  .faixa { position: absolute; left: 0; right: 0; bottom: 0; height: 10px; background: linear-gradient(90deg, #3EE6F2, #9B6BFF, #FF4FB8); }
  .logo { position: absolute; left: 70px; top: 120px; width: 330px; height: 330px; filter: drop-shadow(0 0 40px rgba(155,107,255,.45)); }
  .texto { position: absolute; left: 445px; top: 130px; right: 50px; }
  h1 { font-size: 66px; font-weight: 800; letter-spacing: -1.5px; line-height: 1.02; white-space: nowrap; }
  h1 .des { color: #FF4FB8; }
  .sub { margin-top: 20px; font-size: 30px; line-height: 1.3; color: #D6D8E6; }
  .chips { margin-top: 30px; display: flex; flex-wrap: wrap; gap: 10px; }
  .chip { font-size: 19px; font-weight: 600; padding: 6px 14px; border-radius: 999px; border: 2px solid #9B6BFF; color: #E5DEFF; }
  .assina { position: absolute; left: 445px; bottom: 48px; display: flex; align-items: center; gap: 14px; font-size: 26px; color: #D6D8E6; }
  .assina img { width: 58px; height: 58px; }
  .assina b { color: #F5F7FF; } .assina b .des { color: #FF4FB8; }
  .aviso { position: absolute; left: 70px; bottom: 58px; width: 330px; font-size: 15px; line-height: 1.35; color: #9EA2BA; text-align: center; }
</style></head><body>
  <img class="logo" src="${svg('metadata-desbugado.svg')}" alt="">
  <div class="texto">
    <h1>Metadata <span class="des">Des</span>bugado</h1>
    <p class="sub">O Metadata API da Salesforce em mapa, para estudar e consultar</p>
    <div class="chips"><span class="chip">funcionalidades</span><span class="chip">metadata types</span><span class="chip">objetos API</span><span class="chip">campos</span><span class="chip">fontes oficiais</span></div>
  </div>
  <div class="assina"><img src="${svg('desbugando-bug.svg')}" alt=""><span>um projeto <b><span class="des">des</span>bugando</b></span></div>
  <p class="aviso">Projeto independente, sem afiliação com a Salesforce, Inc.</p>
  <div class="faixa"></div>
</body></html>`;

const navegador = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const pagina = await navegador.newPage({ viewport: { width: 1200, height: 627 }, deviceScaleFactor: 1 });
await pagina.setContent(html, { waitUntil: 'load' });
mkdirSync(dirname(saida), { recursive: true });
await pagina.screenshot({ path: saida, type: 'png' });
await navegador.close();
console.log(`imagem: ${saida}`);
