<template>
  <view class="loading-state" :class="{ 'loading-fullscreen': fullscreen }">
    <view class="loading-spinner">
      <view class="spinner-ring"></view>
      <view class="spinner-ring"></view>
      <view class="spinner-ring"></view>
    </view>
    <view v-if="text" class="loading-text">{{ text }}</view>
  </view>
</template>

<script setup>
/**
 * 加载状态组件
 * 用于展示加载中状态
 */
defineProps({
  // 加载文本
  text: {
    type: String,
    default: '加载中...'
  },
  // 是否全屏显示
  fullscreen: {
    type: Boolean,
    default: false
  }
})
</script>

<style lang="scss" scoped>
.loading-state {
  @include flex-center;
  flex-direction: column;
  padding: $spacing-xl 0;

  &.loading-fullscreen {
    @include absolute-center;
    width: 100%;
    height: 100vh;
    background-color: rgba(255, 255, 255, 0.9);
    z-index: 9999;
  }
}

.loading-spinner {
  position: relative;
  width: 80rpx;
  height: 80rpx;
  margin-bottom: $spacing-md;
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 4rpx solid transparent;
  border-top-color: $primary-color;
  border-radius: $border-radius-circle;
  animation: spin 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;

  &:nth-child(1) {
    animation-delay: -0.45s;
  }

  &:nth-child(2) {
    animation-delay: -0.3s;
  }

  &:nth-child(3) {
    animation-delay: -0.15s;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: $font-size-base;
  color: $text-secondary;
}
</style>
