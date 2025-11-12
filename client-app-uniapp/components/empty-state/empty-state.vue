<template>
  <view class="empty-state">
    <image v-if="image" :src="image" class="empty-image" mode="aspectFit"></image>
    <view v-else class="empty-icon">
      <text class="icon-text">{{ icon }}</text>
    </view>
    <view class="empty-text">{{ text }}</view>
    <view v-if="description" class="empty-description">{{ description }}</view>
    <button v-if="showButton" class="empty-button" @tap="handleAction">
      {{ buttonText }}
    </button>
  </view>
</template>

<script setup>
/**
 * 空状态组件
 * 用于展示无数据、加载失败等状态
 */
const props = defineProps({
  // 空状态图片
  image: {
    type: String,
    default: ''
  },
  // 空状态图标（emoji）
  icon: {
    type: String,
    default: '📝'
  },
  // 空状态文本
  text: {
    type: String,
    default: '暂无数据'
  },
  // 空状态描述
  description: {
    type: String,
    default: ''
  },
  // 是否显示按钮
  showButton: {
    type: Boolean,
    default: false
  },
  // 按钮文本
  buttonText: {
    type: String,
    default: '重新加载'
  }
})

const emit = defineEmits(['action'])

/**
 * 点击按钮
 */
const handleAction = () => {
  emit('action')
}
</script>

<style lang="scss" scoped>
.empty-state {
  @include flex-center;
  flex-direction: column;
  padding: $spacing-xxl 0;
  min-height: 400rpx;
}

.empty-image {
  width: 300rpx;
  height: 300rpx;
  margin-bottom: $spacing-lg;
  opacity: 0.6;
}

.empty-icon {
  margin-bottom: $spacing-lg;
}

.icon-text {
  font-size: 120rpx;
  opacity: 0.6;
}

.empty-text {
  font-size: $font-size-lg;
  color: $text-secondary;
  margin-bottom: $spacing-sm;
}

.empty-description {
  font-size: $font-size-sm;
  color: $text-third;
  margin-bottom: $spacing-lg;
  text-align: center;
  padding: 0 $spacing-xl;
}

.empty-button {
  @include reset-button;
  padding: $spacing-sm $spacing-xl;
  background-color: $button-primary;
  color: #FFFFFF;
  border-radius: $border-radius-md;
  font-size: $font-size-base;
}
</style>
