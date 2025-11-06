<template>
  <view class="theme-toggle" @click="handleToggle">
    <view class="toggle-track" :class="{ 'is-dark': isDark }">
      <view class="toggle-thumb">
        <text class="toggle-icon">{{ isDark ? '🌙' : '☀️' }}</text>
      </view>
    </view>
    <text class="toggle-label">{{ isDark ? '暗黑模式' : '明亮模式' }}</text>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useThemeStore } from '@/store/modules/theme';

const themeStore = useThemeStore();

// 计算属性
const isDark = computed(() => themeStore.isDark);

// 切换主题
const handleToggle = () => {
  themeStore.toggleTheme();

  // 提供触觉反馈（仅在支持的平台）
  uni.vibrateShort({
    type: 'light',
    success: () => {},
    fail: () => {},
  });
};
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.theme-toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.toggle-track {
  position: relative;
  width: 96rpx;
  height: 48rpx;
  background-color: #e8ecf0;
  border-radius: 24rpx;
  transition: background-color $transition-base;

  &.is-dark {
    background-color: #3c3f47;
  }
}

.toggle-thumb {
  position: absolute;
  top: 4rpx;
  left: 4rpx;
  width: 40rpx;
  height: 40rpx;
  background-color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform $transition-base;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);

  .is-dark & {
    transform: translateX(48rpx);
  }
}

.toggle-icon {
  font-size: 20rpx;
  line-height: 1;
}

.toggle-label {
  margin-left: $spacing-sm;
  font-size: $font-size-sm;
  color: var(--text-secondary);
  transition: color $transition-base;
}
</style>
