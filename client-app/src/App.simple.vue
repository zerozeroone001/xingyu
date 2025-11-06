<template>
  <div id="app" :class="themeStore.themeClass">
    <!-- 主内容区 -->
    <div class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>

    <!-- 底部导航栏 -->
    <nav v-if="showTabBar" class="tab-bar theme-card">
      <router-link
        v-for="tab in tabs"
        :key="tab.path"
        :to="tab.path"
        class="tab-item"
        :class="{ active: $route.path === tab.path }"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-text">{{ tab.text }}</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useThemeStore } from '@/store/modules/theme';

const themeStore = useThemeStore();
const route = useRoute();

// 底部导航配置
const tabs = [
  { path: '/', icon: '🏠', text: '首页' },
  { path: '/square', icon: '📢', text: '广场' },
  { path: '/discover', icon: '🔍', text: '发现' },
  { path: '/profile', icon: '👤', text: '我的' },
];

// 需要显示底部导航的路由
const tabBarRoutes = ['/', '/square', '/discover', '/profile'];
const showTabBar = computed(() => tabBarRoutes.includes(route.path));
</script>

<style lang="scss">
@import '@/styles/theme.scss';
@import '@/styles/common.scss';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  width: 100%;
  height: 100%;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  min-height: 100vh;
  background-color: var(--bg-primary);
  transition: background-color 0.3s, color 0.3s;
}

.main-content {
  width: 100%;
  min-height: 100vh;
  padding-bottom: 60px;
}

.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 60px;
  background-color: var(--bg-card);
  border-top: 1px solid var(--border-primary);
  box-shadow: var(--shadow-lg);
  z-index: 1000;

  .tab-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    height: 100%;
    color: var(--text-tertiary);
    text-decoration: none;
    transition: all 0.3s;

    &:hover {
      background-color: var(--bg-hover);
    }

    &.active {
      color: var(--color-primary);

      .tab-icon {
        transform: scale(1.2);
      }
    }

    .tab-icon {
      font-size: 24px;
      margin-bottom: 2px;
      transition: transform 0.3s;
    }

    .tab-text {
      font-size: 12px;
    }
  }
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
