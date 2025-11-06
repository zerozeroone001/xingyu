<template>
  <view class="setting-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 页面标题 -->
      <view class="page-header">
        <text class="page-title">设置</text>
      </view>

      <!-- 设置列表 -->
      <view class="setting-list">
        <!-- 主题设置 -->
        <view class="setting-section">
          <view class="section-title theme-text-secondary">外观设置</view>

          <view class="setting-item theme-card">
            <view class="item-left">
              <text class="item-icon">🎨</text>
              <text class="item-label">主题模式</text>
            </view>
            <view class="item-right">
              <theme-toggle />
            </view>
          </view>

          <view class="setting-item theme-card">
            <view class="item-left">
              <text class="item-icon">🌈</text>
              <text class="item-label">主题色</text>
            </view>
            <view class="item-right">
              <view class="color-preview" :style="{ backgroundColor: primaryColor }"></view>
              <text class="item-value theme-text-tertiary">优雅蓝</text>
            </view>
          </view>
        </view>

        <!-- 主题效果预览 -->
        <view class="setting-section">
          <view class="section-title theme-text-secondary">主题预览</view>

          <view class="preview-card theme-card">
            <view class="preview-title">色彩示例</view>
            <view class="color-samples">
              <view class="color-sample">
                <view class="sample-color" style="background-color: var(--color-primary)"></view>
                <text class="sample-label">主色调</text>
              </view>
              <view class="color-sample">
                <view class="sample-color" style="background-color: var(--color-success)"></view>
                <text class="sample-label">成功</text>
              </view>
              <view class="color-sample">
                <view class="sample-color" style="background-color: var(--color-warning)"></view>
                <text class="sample-label">警告</text>
              </view>
              <view class="color-sample">
                <view class="sample-color" style="background-color: var(--color-error)"></view>
                <text class="sample-label">错误</text>
              </view>
            </view>
          </view>

          <view class="preview-card theme-card">
            <view class="preview-title">文字示例</view>
            <view class="text-samples">
              <text class="sample-text" style="color: var(--text-primary)">主要文字</text>
              <text class="sample-text" style="color: var(--text-secondary)">次要文字</text>
              <text class="sample-text" style="color: var(--text-tertiary)">辅助文字</text>
              <text class="sample-text" style="color: var(--text-disabled)">禁用文字</text>
            </view>
          </view>

          <view class="preview-card theme-card">
            <view class="preview-title">按钮示例</view>
            <view class="button-samples">
              <button class="theme-button">主要按钮</button>
              <button class="theme-button button-secondary">次要按钮</button>
              <button class="theme-button button-text">文字按钮</button>
            </view>
          </view>
        </view>

        <!-- 其他设置 -->
        <view class="setting-section">
          <view class="section-title theme-text-secondary">通用设置</view>

          <view class="setting-item theme-card">
            <view class="item-left">
              <text class="item-icon">🔔</text>
              <text class="item-label">消息通知</text>
            </view>
            <view class="item-right">
              <switch :checked="true" color="var(--color-primary)" />
            </view>
          </view>

          <view class="setting-item theme-card">
            <view class="item-left">
              <text class="item-icon">📱</text>
              <text class="item-label">震动反馈</text>
            </view>
            <view class="item-right">
              <switch :checked="true" color="var(--color-primary)" />
            </view>
          </view>
        </view>

        <!-- 关于 -->
        <view class="setting-section">
          <view class="section-title theme-text-secondary">关于</view>

          <view class="setting-item theme-card">
            <view class="item-left">
              <text class="item-icon">ℹ️</text>
              <text class="item-label">版本号</text>
            </view>
            <view class="item-right">
              <text class="item-value theme-text-tertiary">v1.0.0</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useThemeStore } from '@/store/modules/theme';

const themeStore = useThemeStore();

const primaryColor = computed(() =>
  themeStore.isDark ? '#4a90e2' : '#1a73e8'
);
</script>

<style lang="scss" scoped>
.setting-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 40rpx;
}

.page-header {
  padding: 40rpx $spacing-md 20rpx;

  .page-title {
    font-size: $font-size-xxl;
    font-weight: $font-weight-bold;
    color: var(--text-primary);
  }
}

.setting-list {
  padding: 0 $spacing-md;
}

.setting-section {
  margin-bottom: $spacing-xl;

  .section-title {
    font-size: $font-size-sm;
    padding: $spacing-sm 0;
    margin-bottom: $spacing-sm;
  }
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: $spacing-md;
  margin-bottom: $spacing-md;

  .item-left {
    display: flex;
    align-items: center;
    gap: $spacing-sm;

    .item-icon {
      font-size: 40rpx;
    }

    .item-label {
      font-size: $font-size-md;
      color: var(--text-primary);
    }
  }

  .item-right {
    display: flex;
    align-items: center;
    gap: $spacing-sm;

    .item-value {
      font-size: $font-size-sm;
    }

    .color-preview {
      width: 48rpx;
      height: 48rpx;
      border-radius: $border-radius-sm;
      border: 2rpx solid var(--border-primary);
    }
  }
}

.preview-card {
  padding: $spacing-lg;
  margin-bottom: $spacing-md;

  .preview-title {
    font-size: $font-size-md;
    font-weight: $font-weight-medium;
    color: var(--text-primary);
    margin-bottom: $spacing-md;
  }

  .color-samples {
    display: flex;
    gap: $spacing-md;

    .color-sample {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: $spacing-xs;

      .sample-color {
        width: 100%;
        height: 80rpx;
        border-radius: $border-radius-md;
      }

      .sample-label {
        font-size: $font-size-xs;
        color: var(--text-tertiary);
      }
    }
  }

  .text-samples {
    display: flex;
    flex-direction: column;
    gap: $spacing-sm;

    .sample-text {
      font-size: $font-size-md;
    }
  }

  .button-samples {
    display: flex;
    flex-direction: column;
    gap: $spacing-md;

    button {
      width: 100%;
    }
  }
}
</style>
