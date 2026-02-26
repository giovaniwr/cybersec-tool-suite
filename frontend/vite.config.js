import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Em produção o Render serve os arquivos estáticos na raiz
  base: '/',
  server: {
    port: 5173,
    // Proxy só é usado em desenvolvimento local
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    // Garante que rotas como /password funcionem no Render Static Site
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
})

