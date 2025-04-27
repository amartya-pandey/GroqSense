import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default {
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'https://groqsense.onrender.com'
    }
  }
}