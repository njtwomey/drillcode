import { fileURLToPath } from 'node:url'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Relative base + HashRouter, so the built site works from any GitHub Pages path.
export default defineConfig({
  base: './',
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  server: { fs: { allow: [fileURLToPath(new URL('..', import.meta.url))] } },
  worker: { format: 'es' },
  // The bundle embeds every problem's source text, so it is bigger than the default 500 kB.
  build: { chunkSizeWarningLimit: 4000 },
})
