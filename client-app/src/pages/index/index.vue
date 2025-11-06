<template>
  <view class="index-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 头部 -->
      <view class="header">
        <text class="title">星语诗词</text>
        <text class="subtitle">探索中华诗词之美</text>
      </view>

      <!-- 诗词卡片列表 -->
      <view class="poetry-list">
        <view
          v-for="poetry in poetryList"
          :key="poetry.id"
          class="poetry-card theme-card"
        >
          <view class="poetry-title">{{ poetry.title }}</view>
          <view class="poetry-author theme-text-secondary">
            {{ poetry.dynasty }} · {{ poetry.author }}
          </view>
          <view class="poetry-content">{{ poetry.content }}</view>
          <view class="poetry-actions">
            <view class="action-item">
              <text class="icon">❤️</text>
              <text class="count">{{ poetry.likes }}</text>
            </view>
            <view class="action-item">
              <text class="icon">⭐</text>
              <text class="count">{{ poetry.collects }}</text>
            </view>
            <view class="action-item">
              <text class="icon">💬</text>
              <text class="count">{{ poetry.comments }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 当前主题提示 -->
      <view class="theme-tip">
        <text class="tip-text theme-text-tertiary">
          当前主题: {{ themeStore.isDark ? '暗黑模式' : '明亮模式' }}
        </text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useThemeStore } from '@/store/modules/theme';

const themeStore = useThemeStore();

// 示例诗词数据
const poetryList = ref([
  {
    id: 1,
    title: '静夜思',
    dynasty: '唐',
    author: '李白',
    content: '床前明月光，疑是地上霜。举头望明月，低头思故乡。',
    likes: 1234,
    collects: 567,
    comments: 89,
  },
  {
    id: 2,
    title: '春晓',
    dynasty: '唐',
    author: '孟浩然',
    content: '春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。',
    likes: 987,
    collects: 432,
    comments: 56,
  },
  {
    id: 3,
    title: '登鹳雀楼',
    dynasty: '唐',
    author: '王之涣',
    content: '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。',
    likes: 1567,
    collects: 789,
    comments: 123,
  },
]);

// 下拉刷新
const onPullDownRefresh = () => {
  setTimeout(() => {
    uni.stopPullDownRefresh();
  }, 1000);
};
</script>

<style lang="scss" scoped>
.index-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 120rpx;
}

.header {
  padding: 60rpx 0 40rpx;
  text-align: center;

  .title {
    display: block;
    font-size: $font-size-xxl;
    font-weight: $font-weight-bold;
    color: var(--text-primary);
    margin-bottom: $spacing-xs;
  }

  .subtitle {
    display: block;
    font-size: $font-size-sm;
    color: var(--text-secondary);
  }
}

.poetry-list {
  padding: 0 $spacing-md;
}

.poetry-card {
  margin-bottom: $spacing-lg;
  padding: $spacing-lg;

  .poetry-title {
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    color: var(--text-primary);
    margin-bottom: $spacing-xs;
  }

  .poetry-author {
    font-size: $font-size-sm;
    margin-bottom: $spacing-md;
  }

  .poetry-content {
    font-size: $font-size-md;
    line-height: 1.8;
    color: var(--text-primary);
    margin-bottom: $spacing-md;
    white-space: pre-wrap;
  }

  .poetry-actions {
    display: flex;
    align-items: center;
    gap: $spacing-lg;
    padding-top: $spacing-md;
    border-top: 1px solid var(--border-primary);

    .action-item {
      display: flex;
      align-items: center;
      gap: $spacing-xs;
      cursor: pointer;
      transition: transform $transition-fast;

      &:active {
        transform: scale(0.95);
      }

      .icon {
        font-size: 32rpx;
      }

      .count {
        font-size: $font-size-sm;
        color: var(--text-secondary);
      }
    }
  }
}

.theme-tip {
  position: fixed;
  bottom: 120rpx;
  left: 50%;
  transform: translateX(-50%);
  padding: $spacing-sm $spacing-md;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-md);

  .tip-text {
    font-size: $font-size-xs;
  }
}
</style>
