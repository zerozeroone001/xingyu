<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app';
import { useThemeStore } from '@/store/modules/theme';

const themeStore = useThemeStore();

onLaunch(() => {
  console.log('App Launch');

  // 初始化主题
  themeStore.initTheme();

  // 监听主题变化事件
  uni.$on('themeChanged', (theme: string) => {
    console.log('主题已切换:', theme);
    // 可以在这里添加主题切换后的额外逻辑
  });
});

onShow(() => {
  console.log('App Show');
});

onHide(() => {
  console.log('App Hide');
});
</script>

<style lang="scss">
@import '@/styles/theme.scss';
@import '@/styles/common.scss';

// 全局样式
page {
  // 使用CSS变量来支持主题切换
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: background-color 0.3s, color 0.3s;
}

// 确保页面根元素应用主题类
page.theme-light {
  // 明亮模式已在 theme.scss 中定义
}

page.theme-dark {
  // 暗黑模式已在 theme.scss 中定义
}
</style>
