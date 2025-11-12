<template>
  <view class="theme-page" :class="{ 'theme-transition': isTransitioning }">
    <!-- 页面标题 -->
    <view class="page-header">
      <text class="header-title">主题设置</text>
      <text class="header-subtitle">选择您喜欢的主题风格</text>
    </view>

    <!-- 当前主题预览 -->
    <view class="current-theme">
      <view class="preview-card" :style="currentThemeStyle">
        <view class="preview-header">
          <text class="preview-icon">{{ currentTheme.icon }}</text>
          <view class="preview-info">
            <text class="preview-name">{{ currentTheme.name }}</text>
            <text class="preview-badge">当前使用</text>
          </view>
        </view>
        <view class="preview-colors">
          <view
            v-for="(color, key) in previewColors"
            :key="key"
            class="color-dot"
            :style="{ backgroundColor: color }"
          ></view>
        </view>
      </view>
    </view>

    <!-- 主题列表 -->
    <view class="theme-list">
      <view class="section-title">全部主题（{{ themeList.length }}种）</view>

      <view class="themes-grid">
        <view
          v-for="theme in themeList"
          :key="theme.key"
          class="theme-card"
          :class="{ 'theme-active': theme.key === currentThemeName }"
          @tap="selectTheme(theme.key)"
        >
          <!-- 主题图标 -->
          <view class="theme-icon">
            <text>{{ theme.icon }}</text>
          </view>

          <!-- 主题名称 -->
          <view class="theme-name">{{ theme.name }}</view>

          <!-- 颜色预览 -->
          <view class="theme-colors">
            <view
              class="color-item"
              :style="{ backgroundColor: theme.primary }"
            ></view>
            <view
              class="color-item"
              :style="{ backgroundColor: theme.bgColor }"
            ></view>
            <view
              class="color-item"
              :style="{ backgroundColor: theme.textColor }"
            ></view>
          </view>

          <!-- 选中标识 -->
          <view v-if="theme.key === currentThemeName" class="theme-check">
            <text>✓</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 主题说明 -->
    <view class="theme-description">
      <text class="description-title">🎨 主题说明</text>
      <text class="description-text">
        主题切换会应用到整个应用，包括所有页面和组件。
        切换主题时会有流畅的过渡动画效果。
      </text>
      <text class="description-text">
        每个主题都经过精心设计，包含协调的配色方案，
        为您带来最佳的视觉体验。
      </text>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import { useThemeStore } from '@/stores/theme'

// Store
const themeStore = useThemeStore()

// 计算属性
const themeList = computed(() => themeStore.themeList)
const currentTheme = computed(() => themeStore.theme)
const currentThemeName = computed(() => themeStore.currentTheme)
const isTransitioning = computed(() => themeStore.isTransitioning)

// 当前主题样式
const currentThemeStyle = computed(() => {
  const theme = currentTheme.value
  return {
    background: `linear-gradient(135deg, ${theme.primary} 0%, ${theme.secondary} 100%)`,
    color: '#FFFFFF'
  }
})

// 预览颜色（显示主要颜色）
const previewColors = computed(() => {
  const theme = currentTheme.value
  return {
    primary: theme.primary,
    secondary: theme.secondary,
    bgColor: theme.bgColor,
    textColor: theme.textColor,
    cardBg: theme.cardBg
  }
})

/**
 * 选择主题
 * @param {string} themeKey - 主题key
 */
const selectTheme = (themeKey) => {
  if (themeKey === currentThemeName.value) return

  // 切换主题
  themeStore.setTheme(themeKey)

  // 触发震动反馈
  // #ifndef H5
  uni.vibrateShort({
    type: 'light'
  })
  // #endif
}
</script>

<style lang="scss" scoped>
.theme-page {
  min-height: 100vh;
  padding: $spacing-lg;
  background-color: $bg-color;
}

.page-header {
  @include flex-center;
  flex-direction: column;
  padding: $spacing-xl 0;
}

.header-title {
  font-size: $font-size-xxl;
  font-weight: bold;
  color: $text-color;
  margin-bottom: $spacing-sm;
}

.header-subtitle {
  font-size: $font-size-sm;
  color: $text-third;
}

.current-theme {
  margin-bottom: $spacing-xl;
}

.preview-card {
  padding: $spacing-xl;
  border-radius: $border-radius-xl;
  @include card-shadow;
  @include transition;
}

.preview-header {
  @include flex-align-center;
  margin-bottom: $spacing-lg;
}

.preview-icon {
  font-size: 80rpx;
  margin-right: $spacing-md;
}

.preview-info {
  flex: 1;
}

.preview-name {
  display: block;
  font-size: $font-size-xl;
  font-weight: bold;
  margin-bottom: $spacing-xs;
}

.preview-badge {
  display: inline-block;
  padding: 4rpx 12rpx;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: $border-radius-sm;
  font-size: $font-size-xs;
}

.preview-colors {
  @include flex-align-center;
  gap: $spacing-sm;
}

.color-dot {
  width: 48rpx;
  height: 48rpx;
  border-radius: $border-radius-circle;
  border: 4rpx solid rgba(255, 255, 255, 0.3);
  @include transition;

  &:active {
    transform: scale(1.1);
  }
}

.theme-list {
  margin-bottom: $spacing-xl;
}

.section-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-color;
  margin-bottom: $spacing-md;
}

.themes-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-md;
}

.theme-card {
  position: relative;
  background-color: $card-bg;
  border-radius: $border-radius-lg;
  padding: $spacing-lg;
  @include card-shadow;
  @include transition;

  &:active {
    transform: scale(0.95);
  }

  &.theme-active {
    border: 4rpx solid $primary-color;
    @include hover-shadow;
  }
}

.theme-icon {
  @include flex-center;
  width: 80rpx;
  height: 80rpx;
  margin: 0 auto $spacing-sm;
  background-color: $bg-secondary;
  border-radius: $border-radius-circle;
  font-size: 48rpx;
}

.theme-name {
  text-align: center;
  font-size: $font-size-base;
  font-weight: bold;
  color: $text-color;
  margin-bottom: $spacing-sm;
}

.theme-colors {
  @include flex-center;
  gap: $spacing-xs;
}

.color-item {
  width: 24rpx;
  height: 24rpx;
  border-radius: $border-radius-circle;
  border: 2rpx solid $border-color;
}

.theme-check {
  @include absolute-center;
  @include flex-center;
  width: 60rpx;
  height: 60rpx;
  background-color: $primary-color;
  border-radius: $border-radius-circle;
  color: #FFFFFF;
  font-size: 32rpx;
  font-weight: bold;
  animation: checkIn 0.3s ease;
}

@keyframes checkIn {
  from {
    transform: translate(-50%, -50%) scale(0);
    opacity: 0;
  }
  to {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
}

.theme-description {
  background-color: $card-bg;
  border-radius: $border-radius-lg;
  padding: $spacing-lg;
  @include card-shadow;
}

.description-title {
  display: block;
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-color;
  margin-bottom: $spacing-md;
}

.description-text {
  display: block;
  font-size: $font-size-sm;
  color: $text-secondary;
  line-height: 1.8;
  margin-bottom: $spacing-sm;

  &:last-child {
    margin-bottom: 0;
  }
}
</style>
