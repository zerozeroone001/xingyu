<template>
  <view class="poetry-card" :class="{ 'card-small': size === 'small' }" @tap="handleTap">
    <!-- 作者和朝代 -->
    <view class="card-header">
      <view class="author-info">
        <text class="author-name">{{ poetry.author }}</text>
        <text class="dynasty">{{ poetry.dynasty }}</text>
      </view>
      <view v-if="showType" class="poetry-type">
        <text>{{ poetry.type }}</text>
      </view>
    </view>

    <!-- 诗词标题 -->
    <view class="poetry-title">
      <text>{{ poetry.title }}</text>
    </view>

    <!-- 诗词内容 -->
    <view class="poetry-content">
      <text class="content-text" :class="{ 'text-ellipsis-3': !showFullContent }">
        {{ poetry.content }}
      </text>
    </view>

    <!-- 互动信息 -->
    <view class="card-footer" v-if="showStats">
      <view class="stat-item">
        <text class="iconfont icon-view"></text>
        <text class="stat-text">{{ formatNumber(poetry.read_count) }}</text>
      </view>
      <view class="stat-item">
        <text class="iconfont icon-like"></text>
        <text class="stat-text">{{ formatNumber(poetry.like_count) }}</text>
      </view>
      <view class="stat-item">
        <text class="iconfont icon-comment"></text>
        <text class="stat-text">{{ formatNumber(poetry.comment_count) }}</text>
      </view>
      <view class="stat-item">
        <text class="iconfont icon-collect"></text>
        <text class="stat-text">{{ formatNumber(poetry.collect_count) }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { formatNumber } from '@/utils'

/**
 * 诗词卡片组件
 * 用于展示诗词信息
 */
const props = defineProps({
  // 诗词数据
  poetry: {
    type: Object,
    required: true
  },
  // 卡片尺寸：normal, small
  size: {
    type: String,
    default: 'normal'
  },
  // 是否显示统计信息
  showStats: {
    type: Boolean,
    default: true
  },
  // 是否显示诗词类型
  showType: {
    type: Boolean,
    default: true
  },
  // 是否显示完整内容
  showFullContent: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['tap', 'like', 'collect'])

/**
 * 点击卡片
 */
const handleTap = () => {
  emit('tap', props.poetry)
}
</script>

<style lang="scss" scoped>
.poetry-card {
  background-color: $card-bg;
  border-radius: $border-radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-md;
  @include card-shadow;
  @include transition;

  &:active {
    transform: scale(0.98);
    @include hover-shadow;
  }

  &.card-small {
    padding: $spacing-md;
    margin-bottom: $spacing-sm;
  }
}

.card-header {
  @include flex-between;
  margin-bottom: $spacing-sm;
}

.author-info {
  @include flex-align-center;
}

.author-name {
  font-size: $font-size-base;
  font-weight: bold;
  color: $text-color;
  margin-right: $spacing-sm;
}

.dynasty {
  font-size: $font-size-sm;
  color: $text-third;
}

.poetry-type {
  padding: 2rpx 12rpx;
  background-color: $bg-secondary;
  border-radius: $border-radius-sm;
  font-size: $font-size-xs;
  color: $text-secondary;
}

.poetry-title {
  font-size: $font-size-xl;
  font-weight: bold;
  color: $text-color;
  margin-bottom: $spacing-md;
  text-align: center;
}

.poetry-content {
  margin-bottom: $spacing-md;
}

.content-text {
  font-size: $font-size-base;
  color: $text-secondary;
  line-height: 1.8;
  white-space: pre-wrap;
}

.card-footer {
  @include flex-between;
  padding-top: $spacing-sm;
  border-top: 1rpx solid $border-color;
}

.stat-item {
  @include flex-align-center;
  font-size: $font-size-sm;
  color: $text-third;

  .iconfont {
    margin-right: 4rpx;
    font-size: $font-size-base;
  }

  .stat-text {
    margin-left: 4rpx;
  }
}
</style>
