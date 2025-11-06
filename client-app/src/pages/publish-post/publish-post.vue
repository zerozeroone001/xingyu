<template>
  <view class="publish-post-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 内容输入框 -->
      <view class="content-section theme-card">
        <textarea
          v-model="formData.content"
          class="content-input"
          placeholder="分享你的想法..."
          :maxlength="500"
          :auto-height="true"
          :focus="true"
        />
        <view class="char-count theme-text-tertiary">
          {{ formData.content.length }}/500
        </view>
      </view>

      <!-- 关联诗词 -->
      <view v-if="selectedPoetry" class="poetry-section theme-card">
        <view class="section-title">
          <text>关联诗词</text>
          <text class="remove-btn" @click="removePoetry">移除</text>
        </view>
        <view class="poetry-card">
          <view class="poetry-title">{{ selectedPoetry.title }}</view>
          <view class="poetry-author theme-text-secondary">
            {{ selectedPoetry.dynasty }} · {{ selectedPoetry.author_name }}
          </view>
        </view>
      </view>

      <!-- 添加诗词按钮 -->
      <view v-else class="add-section theme-card" @click="handleSelectPoetry">
        <text class="add-icon">📖</text>
        <text class="add-text">关联一首诗词</text>
      </view>

      <!-- 图片选择 -->
      <view class="image-section theme-card">
        <view class="section-title">图片（选填，最多3张）</view>
        <view class="image-list">
          <view
            v-for="(image, index) in formData.images"
            :key="index"
            class="image-item"
          >
            <image class="image" :src="image" mode="aspectFill" />
            <view class="remove-btn" @click="removeImage(index)">×</view>
          </view>
          <view
            v-if="formData.images.length < 3"
            class="image-add"
            @click="handleChooseImage"
          >
            <text class="add-icon">+</text>
          </view>
        </view>
      </view>

      <!-- 标签输入 -->
      <view class="tags-section theme-card">
        <view class="section-title">标签（选填）</view>
        <view class="tags-input">
          <view
            v-for="(tag, index) in formData.tags"
            :key="index"
            class="tag-item"
          >
            <text class="tag-text">#{{ tag }}</text>
            <text class="remove-btn" @click="removeTag(index)">×</text>
          </view>
          <input
            v-model="tagInput"
            class="tag-input"
            placeholder="输入标签后按回车"
            @confirm="addTag"
          />
        </view>
      </view>

      <!-- 发布按钮 -->
      <button
        class="publish-btn"
        :class="{ disabled: !canPublish }"
        :disabled="!canPublish || publishing"
        @click="handlePublish"
      >
        {{ publishing ? '发布中...' : '发布' }}
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { createPost, PostType, type CreatePostParams } from '@/api/post';
import type { Poetry } from '@/api/poetry';

const themeStore = useThemeStore();

const formData = ref<CreatePostParams>({
  type: PostType.ORIGINAL,
  content: '',
  images: [],
  tags: [],
  poetry_id: undefined,
});

const selectedPoetry = ref<Poetry | null>(null);
const tagInput = ref('');
const publishing = ref(false);

/**
 * 是否可以发布
 */
const canPublish = computed(() => {
  return formData.value.content.trim().length > 0;
});

/**
 * 选择关联诗词
 */
const handleSelectPoetry = () => {
  uni.showToast({
    title: '功能开发中',
    icon: 'none',
    duration: 2000,
  });
  // TODO: 实现诗词选择功能
  // 可以跳转到诗词列表页面，选择后返回
};

/**
 * 移除关联诗词
 */
const removePoetry = () => {
  selectedPoetry.value = null;
  formData.value.poetry_id = undefined;
  formData.value.type = PostType.ORIGINAL;
};

/**
 * 选择图片
 */
const handleChooseImage = () => {
  uni.chooseImage({
    count: 3 - formData.value.images!.length,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      // 实际使用时需要上传图片到服务器，获取图片URL
      formData.value.images!.push(...res.tempFilePaths);
    },
  });
};

/**
 * 移除图片
 */
const removeImage = (index: number) => {
  formData.value.images!.splice(index, 1);
};

/**
 * 添加标签
 */
const addTag = () => {
  const tag = tagInput.value.trim();
  if (tag && !formData.value.tags!.includes(tag)) {
    if (formData.value.tags!.length < 5) {
      formData.value.tags!.push(tag);
      tagInput.value = '';
    } else {
      uni.showToast({
        title: '最多添加5个标签',
        icon: 'none',
        duration: 2000,
      });
    }
  }
};

/**
 * 移除标签
 */
const removeTag = (index: number) => {
  formData.value.tags!.splice(index, 1);
};

/**
 * 发布动态
 */
const handlePublish = async () => {
  if (!canPublish.value || publishing.value) {
    return;
  }

  try {
    publishing.value = true;

    await createPost(formData.value);

    uni.showToast({
      title: '发布成功',
      icon: 'success',
      duration: 1500,
    });

    setTimeout(() => {
      uni.navigateBack();
    }, 1500);
  } catch (error) {
    console.error('发布失败:', error);
    uni.showToast({
      title: '发布失败',
      icon: 'none',
      duration: 2000,
    });
  } finally {
    publishing.value = false;
  }
};
</script>

<style lang="scss" scoped>
.publish-post-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 120rpx;
}

.container {
  padding: $spacing-md;
}

.content-section {
  padding: $spacing-lg;
  margin-bottom: $spacing-md;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  .content-input {
    width: 100%;
    min-height: 300rpx;
    font-size: $font-size-md;
    line-height: 1.8;
    color: var(--text-primary);
    margin-bottom: $spacing-md;
  }

  .char-count {
    font-size: $font-size-xs;
    text-align: right;
  }
}

.poetry-section,
.add-section {
  padding: $spacing-lg;
  margin-bottom: $spacing-md;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);
}

.add-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
  cursor: pointer;
  transition: all $transition-normal;

  &:active {
    transform: scale(0.98);
  }

  .add-icon {
    font-size: 40rpx;
    margin-right: $spacing-md;
  }

  .add-text {
    font-size: $font-size-md;
    color: var(--text-primary);
  }
}

.poetry-section {
  .section-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: $font-size-md;
    font-weight: $font-weight-medium;
    color: var(--text-primary);
    margin-bottom: $spacing-md;

    .remove-btn {
      font-size: $font-size-sm;
      color: var(--color-error);
      cursor: pointer;
    }
  }

  .poetry-card {
    padding: $spacing-md;
    background-color: var(--bg-secondary);
    border-radius: $border-radius-md;
    border-left: 4rpx solid var(--color-primary);

    .poetry-title {
      font-size: $font-size-md;
      font-weight: $font-weight-medium;
      color: var(--text-primary);
      margin-bottom: $spacing-xs;
    }

    .poetry-author {
      font-size: $font-size-sm;
    }
  }
}

.image-section,
.tags-section {
  padding: $spacing-lg;
  margin-bottom: $spacing-md;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  .section-title {
    font-size: $font-size-md;
    font-weight: $font-weight-medium;
    color: var(--text-primary);
    margin-bottom: $spacing-md;
  }
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-md;

  .image-item {
    position: relative;
    width: 200rpx;
    height: 200rpx;

    .image {
      width: 100%;
      height: 100%;
      border-radius: $border-radius-md;
    }

    .remove-btn {
      position: absolute;
      top: -16rpx;
      right: -16rpx;
      width: 48rpx;
      height: 48rpx;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 40rpx;
      color: #ffffff;
      background-color: rgba(0, 0, 0, 0.6);
      border-radius: 50%;
      cursor: pointer;
    }
  }

  .image-add {
    width: 200rpx;
    height: 200rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--bg-secondary);
    border-radius: $border-radius-md;
    border: 2rpx dashed var(--border-primary);
    cursor: pointer;

    .add-icon {
      font-size: 60rpx;
      color: var(--text-tertiary);
    }
  }
}

.tags-input {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-sm;
  padding: $spacing-md;
  background-color: var(--bg-secondary);
  border-radius: $border-radius-md;

  .tag-item {
    display: flex;
    align-items: center;
    padding: 8rpx 16rpx;
    background-color: var(--bg-card);
    border-radius: $border-radius-sm;

    .tag-text {
      font-size: $font-size-sm;
      color: var(--color-primary);
      margin-right: $spacing-xs;
    }

    .remove-btn {
      font-size: 32rpx;
      color: var(--text-tertiary);
      cursor: pointer;
    }
  }

  .tag-input {
    flex: 1;
    min-width: 200rpx;
    font-size: $font-size-sm;
    color: var(--text-primary);
    background-color: transparent;
    border: none;
  }
}

.publish-btn {
  width: 100%;
  height: 90rpx;
  line-height: 90rpx;
  font-size: $font-size-lg;
  font-weight: $font-weight-medium;
  color: #ffffff;
  background-color: var(--color-primary);
  border: none;
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-md);

  &:active {
    opacity: 0.8;
  }

  &.disabled {
    opacity: 0.5;
  }
}
</style>
