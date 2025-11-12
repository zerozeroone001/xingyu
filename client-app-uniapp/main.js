import { createSSRApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

/**
 * 创建应用实例
 * @returns {Object} Vue 应用实例
 */
export function createApp() {
  const app = createSSRApp(App)

  // 使用 Pinia 状态管理
  const pinia = createPinia()
  app.use(pinia)

  return {
    app
  }
}
