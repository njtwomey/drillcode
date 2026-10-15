import { fileURLToPath } from 'node:url'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Real URLs (BrowserRouter). Locally the base is '/'. For GitHub Pages the workflow sets
// BASE_PATH=/drillcode/ (the repository name) and the build copies index.html to 404.html so
// deep links such as /p/two-sum/read load the app.
export default defineConfig({
  base: process.env.BASE_PATH ?? '/',
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  server: { fs: { allow: [fileURLToPath(new URL('..', import.meta.url))] } },
  worker: { format: 'es' },
  // The bundle embeds every problem's source text, so it is bigger than the default 500 kB.
  build: { chunkSizeWarningLimit: 4000 },
})
