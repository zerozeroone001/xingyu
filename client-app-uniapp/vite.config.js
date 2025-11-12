import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

/**
 * Vite 配置文件
 * @see https://vitejs.dev/config/
 */
export default defineConfig({
  plugins: [uni()],

  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },

  css: {
    preprocessorOptions: {
      scss: {
        additionalData: '@import "@/styles/variables.scss";'
      }
    }
  }
})
