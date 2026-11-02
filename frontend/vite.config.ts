import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Em desenvolvimento, o site chama /api e o Vite repassa para a API local. Assim não há CORS nem confusão entre
// localhost (IPv6 no Windows) e 127.0.0.1. Em produção, VITE_API_URL aponta para o endereço público da API.
const api = {
  '/api': {
    target: process.env.RISKPME_API_LOCAL ?? 'http://127.0.0.1:8000',
    changeOrigin: true,
    rewrite: (caminho: string) => caminho.replace(/^\/api/, ''),
  },
}

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { proxy: api },
  preview: { proxy: api },
  test: { environment: 'node' },
} as never)
