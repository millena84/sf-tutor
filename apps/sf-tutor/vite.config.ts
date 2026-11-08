import { defineConfig } from 'vite';

// base relativa: o site funciona em subcaminho (GitHub Pages /tutorial-sf-grafo/) sem reconfigurar.
export default defineConfig({
  base: './',
  build: { outDir: 'dist', sourcemap: false, chunkSizeWarningLimit: 900 },
  test: { environment: 'jsdom', include: ['tests/unit/**/*.test.ts'] },
} as never);
