import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/** Vite config with API proxy for local FastAPI development. */
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/recipes': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/ingredients': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
