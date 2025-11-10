<template>
  <view class="post-detail-page" :class="themeStore.themeClass">
    <view v-if="post" class="container">
      <!-- 用户信息 -->
      <view class="user-info theme-card" @click="goToUserDetail">
        <image
          v-if="post.user_avatar"
          class="avatar"
          :src="post.user_avatar"
          mode="aspectFill"
        />
        <view v-else class="avatar-placeholder">
          {{ post.user_name?.charAt(0) }}
        </view>

        <view class="user-text">
          <view class="username">{{ post.user_name }}</view>
          <view class="time theme-text-tertiary">{{ formatTime(post.created_at) }}</view>
        </view>
      </view>

      <!-- 动态内容 -->
      <view class="post-content theme-card">
        <view class="content-text">{{ post.content }}</view>

        <!-- 关联诗词 -->
        <view v-if="post.poetry_id" class="poetry-link" @click="goToPoetryDetail">
          <view class="poetry-title">{{ post.poetry_title }}</view>
          <view class="poetry-content theme-text-secondary">{{ post.poetry_content }}</view>
        </view>

        <!-- 图片列表 -->
        <view v-if="post.images && post.images.length > 0" class="image-list">
          <image
            v-for="(image, index) in post.images"
            :key="index"
            class="image-item"
            :src="image"
            mode="aspectFill"
            @click="previewImage(index)"
          />
        </view>

        <!-- 标签 -->
        <view v-if="post.tags && post.tags.length > 0" class="tags">
          <text
            v-for="(tag, index) in post.tags"
            :key="index"
            class="tag theme-text-tertiary"
          >
            #{{ tag }}
          </text>
        </view>
      </view>

      <!-- 互动数据 -->
      <view class="post-stats theme-card">
        <view class="stat-item">
          <text class="icon">👁️</text>
          <text class="count">{{ post.views_count || 0 }}</text>
          <text class="label theme-text-tertiary">浏览</text>
        </view>
        <view class="stat-item">
          <text class="icon">❤️</text>
          <text class="count">{{ post.likes_count || 0 }}</text>
          <text class="label theme-text-tertiary">点赞</text>
        </view>
        <view class="stat-item">
          <text class="icon">💬</text>
          <text class="count">{{ post.comments_count || 0 }}</text>
          <text class="label theme-text-tertiary">评论</text>
        </view>
        <view class="stat-item">
          <text class="icon">⭐</text>
          <text class="count">{{ post.collects_count || 0 }}</text>
          <text class="label theme-text-tertiary">收藏</text>
        </view>
      </view>

      <!-- 评论区 -->
      <comment-section :post-id="post.id" :theme-class="themeStore.themeClass" />
    </view>

    <!-- 底部操作栏 -->
    <view v-if="post" class="bottom-bar theme-card">
      <button class="action-btn" @click="handleLike">
        <text class="icon">{{ isLiked ? '❤️' : '🤍' }}</text>
        <text class="label">点赞</text>
      </button>
      <button class="action-btn" @click="handleCollect">
        <text class="icon">{{ isCollected ? '⭐' : '☆' }}</text>
        <text class="label">收藏</text>
      </button>
      <button class="action-btn" @click="handleComment">
        <text class="icon">💬</text>
        <text class="label">评论</text>
      </button>
    </view>

    <!-- 加载中 -->
    <view v-else-if="loading" class="loading-box">
      <text class="loading-text">加载中...</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { getPostDetail, likePost, unlikePost, collectPost, uncollectPost, type Post } from '@/api/post';
import CommentSection from '@/components/comment-section/comment-section.vue';

const themeStore = useThemeStore();

const postId = ref<number>(0);
const post = ref<Post | null>(null);
const loading = ref(false);
const isLiked = ref(false);
const isCollected = ref(false);

/**
 * 加载动态详情
 */
const loadPostDetail = async () => {
  try {
    loading.value = true;
    const response = await getPostDetail(postId.value);
    post.value = response.data;
  } catch (error) {
    console.error('加载动态详情失败:', error);
    uni.showToast({
      title: '加载失败',
      icon: 'none',
      duration: 2000,
    });
  } finally {
    loading.value = false;
  }
};

/**
 * 格式化时间
 */
const formatTime = (time: string) => {
  const date = new Date(time);
  return date.toLocaleString();
};

/**
 * 点赞/取消点赞
 */
const handleLike = async () => {
  try {
    if (isLiked.value) {
      await unlikePost(postId.value);
      isLiked.value = false;
      if (post.value) post.value.likes_count--;
    } else {
      await likePost(postId.value);
      isLiked.value = true;
      if (post.value) post.value.likes_count++;
    }
  } catch (error) {
    console.error('操作失败:', error);
    uni.showToast({
      title: '操作失败',
      icon: 'none',
      duration: 2000,
    });
  }
};

/**
 * 收藏/取消收藏
 */
const handleCollect = async () => {
  try {
    if (isCollected.value) {
      await uncollectPost(postId.value);
      isCollected.value = false;
      if (post.value) post.value.collects_count--;
    } else {
      await collectPost(postId.value);
      isCollected.value = true;
      if (post.value) post.value.collects_count++;
    }
  } catch (error) {
    console.error('操作失败:', error);
    uni.showToast({
      title: '操作失败',
      icon: 'none',
      duration: 2000,
    });
  }
};

/**
 * 评论（滚动到评论区）
 */
const handleComment = () => {
  // 可以添加滚动到评论区的逻辑
  uni.showToast({
    title: '请在下方评论',
    icon: 'none',
    duration: 1500,
  });
};

/**
 * 预览图片
 */
const previewImage = (index: number) => {
  if (post.value?.images) {
    uni.previewImage({
      urls: post.value.images,
      current: index,
    });
  }
};

/**
 * 跳转到用户主页
 */
const goToUserDetail = () => {
  if (post.value) {
    uni.navigateTo({
      url: `/pages/user-detail/user-detail?id=${post.value.user_id}`,
    });
  }
};

/**
 * 跳转到诗词详情
 */
const goToPoetryDetail = () => {
  if (post.value?.poetry_id) {
    uni.navigateTo({
      url: `/poetry-detail?id=${post.value.poetry_id}`,
    });
  }
};

// 页面加载时获取数据
onMounted(() => {
  const pages = getCurrentPages();
  const currentPage = pages[pages.length - 1] as any;
  const options = currentPage.options || currentPage.$page?.options || {};
  postId.value = parseInt(options.id || '0');

  if (postId.value) {
    loadPostDetail();
  }
});
</script>

<style lang="scss" scoped>
.post-detail-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 150rpx;
}

.container {
  padding: $spacing-md;
}

.user-info {
  display: flex;
  align-items: center;
  padding: $spacing-lg;
  margin-bottom: $spacing-md;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  .avatar,
  .avatar-placeholder {
    width: 80rpx;
    height: 80rpx;
    border-radius: 50%;
    margin-right: $spacing-md;
    flex-shrink: 0;
  }

  .avatar-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--color-primary);
    color: #ffffff;
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
  }

  .user-text {
    flex: 1;

    .username {
      font-size: $font-size-md;
      font-weight: $font-weight-medium;
      color: var(--text-primary);
      margin-bottom: 4rpx;
    }

    .time {
      font-size: $font-size-xs;
    }
  }
}

.post-content {
  padding: $spacing-xl;
  margin-bottom: $spacing-md;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  .content-text {
    font-size: $font-size-md;
    line-height: 1.8;
    color: var(--text-primary);
    margin-bottom: $spacing-lg;
    white-space: pre-wrap;
  }

  .poetry-link {
    padding: $spacing-lg;
    background-color: var(--bg-secondary);
    border-radius: $border-radius-md;
    border-left: 4rpx solid var(--color-primary);
    margin-bottom: $spacing-lg;
    cursor: pointer;

    .poetry-title {
      font-size: $font-size-lg;
      font-weight: $font-weight-bold;
      color: var(--text-primary);
      margin-bottom: $spacing-sm;
    }

    .poetry-content {
      font-size: $font-size-sm;
      line-height: 1.6;
    }
  }

  .image-list {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: $spacing-sm;
    margin-bottom: $spacing-lg;

    .image-item {
      width: 100%;
      height: 200rpx;
      border-radius: $border-radius-md;
    }
  }

  .tags {
    display: flex;
    flex-wrap: wrap;
    gap: $spacing-sm;

    .tag {
      padding: 8rpx 24rpx;
      font-size: $font-size-sm;
      background-color: var(--bg-secondary);
      border-radius: $border-radius-md;
    }
  }
}

.post-stats {
  display: flex;
  justify-content: space-around;
  padding: $spacing-lg;
  margin-bottom: $spacing-md;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;

    .icon {
      font-size: 32rpx;
      margin-bottom: 8rpx;
    }

    .count {
      font-size: $font-size-lg;
      font-weight: $font-weight-bold;
      color: var(--text-primary);
      margin-bottom: 4rpx;
    }

    .label {
      font-size: $font-size-xs;
    }
  }
}

.comments-section {
  padding: $spacing-xl;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  .section-title {
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    color: var(--text-primary);
    margin-bottom: $spacing-lg;
  }

  .comments-list {
    .empty-text {
      padding: 80rpx 0;
      text-align: center;
      font-size: $font-size-sm;
    }
  }
}

.loading-box {
  padding: 200rpx 0;
  text-align: center;

  .loading-text {
    font-size: $font-size-md;
    color: var(--text-tertiary);
  }
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  padding: $spacing-md $spacing-lg;
  background-color: var(--bg-card);
  border-top: 1px solid var(--border-primary);
  box-shadow: var(--shadow-md);

  .action-btn {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: $spacing-sm;
    font-size: $font-size-sm;
    color: var(--text-primary);
    background-color: transparent;
    border: none;

    &:active {
      opacity: 0.7;
    }

    .icon {
      font-size: 40rpx;
      margin-bottom: 4rpx;
    }

    .label {
      font-size: $font-size-xs;
    }
  }
}
</style>
