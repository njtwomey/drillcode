import path from 'node:path'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Relative base + HashRouter, so the built site works from any GitHub Pages path.
export default defineConfig({
  base: './',
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } },
  server: { fs: { allow: [path.resolve(__dirname, '..')] } },
  worker: { format: 'es' },
})
