<template>
  <div id="app" :class="themeStore.themeClass">
    <!-- 路由视图会放在这里 -->
    <div class="app-container">
      <h1>星语诗词</h1>
      <p>前端应用开发中...</p>
      <p>当前主题: {{ themeStore.isDark ? '暗黑模式' : '明亮模式' }}</p>
      <button @click="themeStore.toggleTheme">切换主题</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';

const themeStore = useThemeStore();

onMounted(() => {
  console.log('App mounted');
});
</script>

<style lang="scss">
@import '@/styles/theme.scss';
@import '@/styles/common.scss';

#app {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  background-color: var(--bg-primary);
}

.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  text-align: center;

  h1 {
    font-size: 48px;
    margin-bottom: 20px;
    color: var(--text-primary);
  }

  p {
    font-size: 18px;
    margin-bottom: 10px;
    color: var(--text-secondary);
  }

  button {
    margin-top: 20px;
    padding: 12px 24px;
    font-size: 16px;
    color: #fff;
    background-color: var(--color-primary);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      opacity: 0.9;
      transform: translateY(-2px);
    }

    &:active {
      transform: translateY(0);
    }
  }
}
</style>
