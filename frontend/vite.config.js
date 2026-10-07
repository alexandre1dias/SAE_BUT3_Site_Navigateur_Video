import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@views': path.resolve(__dirname, 'src/views'),
      '@model': path.resolve(__dirname, 'src/model'),
      '@components': path.resolve(__dirname, 'src/components'),
    }
  },
  test: {
    globals: true,        // permet d'utiliser describe, it, expect directement
    environment: 'jsdom', // simule un navigateur
    include: ['tests/**/*.spec.js'], // chemins vers tes tests
  },
})
