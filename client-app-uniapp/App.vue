<script>
import { useThemeStore } from '@/stores/theme'
import { useUserStore } from '@/stores/user'

export default {
  /**
   * 应用生命周期 - 启动
   * 初始化主题、检查登录状态
   */
  onLaunch() {
    console.log('App Launch')

    // 初始化主题
    const themeStore = useThemeStore()
    themeStore.initTheme()

    // 检查登录状态
    const userStore = useUserStore()
    userStore.checkLogin()
  },

  /**
   * 应用生命周期 - 显示
   */
  onShow() {
    console.log('App Show')
  },

  /**
   * 应用生命周期 - 隐藏
   */
  onHide() {
    console.log('App Hide')
  }
}
</script>

<style lang="scss">
/* 全局样式 */
@import '@/styles/global.scss';

/* 主题变量将通过 CSS Variables 动态注入 */
page {
  background-color: var(--bg-color, #FFFFFF);
  color: var(--text-color, #2C3E50);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style>
