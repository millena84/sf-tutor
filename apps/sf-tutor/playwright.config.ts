import { defineConfig } from '@playwright/test';
import { existsSync } from 'node:fs';

// Usa o Chrome instalado na máquina quando existir (o ambiente de desenvolvimento não baixa navegadores).
const chrome = ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable'].find((p) => existsSync(p));
const launchOptions = chrome ? { executablePath: chrome } : {};

export default defineConfig({
  testDir: 'tests/e2e',
  outputDir: 'test-results',
  fullyParallel: false,
  workers: 2,
  retries: 0,
  timeout: 45_000,
  reporter: [['list'], ['json', { outputFile: 'tests/resultados/e2e.json' }]],
  use: { baseURL: 'http://localhost:4173', trace: 'retain-on-failure', launchOptions },
  // serve o build (dist/): rode "npm run build" antes. O teste de performance acrescenta dist/__teste-sintetico.
  webServer: { command: 'npx vite preview --port 4173 --strictPort', url: 'http://localhost:4173', reuseExistingServer: true, timeout: 30_000 },
  projects: [
    { name: 'desktop', testIgnore: /perf\.spec/, use: { viewport: { width: 1366, height: 900 } } },
    { name: 'mobile', testMatch: /(mobile|jornadas|destaque)\.spec/, use: { viewport: { width: 360, height: 740 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 } },
    { name: 'perf', testMatch: /perf\.spec/, use: { viewport: { width: 1366, height: 900 } } },
  ],
});
