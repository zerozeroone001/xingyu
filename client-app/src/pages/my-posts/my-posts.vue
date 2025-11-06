<template>
  <view class="my-posts-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 空状态 -->
      <view v-if="!loading && postList.length === 0" class="empty-box">
        <text class="empty-icon">📝</text>
        <text class="empty-text">还没有发布任何动态</text>
        <button class="publish-btn" @click="goToPublish">发布动态</button>
      </view>

      <!-- 动态列表 -->
      <view v-else class="post-list">
        <view
          v-for="post in postList"
          :key="post.id"
          class="post-card theme-card"
          @click="goToDetail(post.id)"
        >
          <!-- 动态内容 -->
          <view class="post-content">{{ post.content }}</view>

          <!-- 关联诗词 -->
          <view v-if="post.poetry_id" class="poetry-link theme-card-secondary">
            <view class="poetry-title">{{ post.poetry_title }}</view>
            <view class="poetry-content">{{ formatContent(post.poetry_content || '') }}</view>
          </view>

          <!-- 图片列表 -->
          <view v-if="post.images && post.images.length > 0" class="image-list">
            <image
              v-for="(image, index) in post.images.slice(0, 3)"
              :key="index"
              class="image-item"
              :src="image"
              mode="aspectFill"
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

          <!-- 底部信息 -->
          <view class="post-footer">
            <view class="post-meta theme-text-tertiary">
              {{ formatTime(post.created_at) }}
            </view>
            <view class="post-actions">
              <view class="action-item">
                <text class="icon">👁️</text>
                <text class="count">{{ post.views_count || 0 }}</text>
              </view>
              <view class="action-item">
                <text class="icon">❤️</text>
                <text class="count">{{ post.likes_count || 0 }}</text>
              </view>
              <view class="action-item">
                <text class="icon">💬</text>
                <text class="count">{{ post.comments_count || 0 }}</text>
              </view>
            </view>
          </view>

          <!-- 操作按钮 -->
          <view class="post-operations">
            <button class="operation-btn" @click.stop="handleDelete(post.id)">
              删除
            </button>
          </view>
        </view>
      </view>

      <!-- 加载中 -->
      <view v-if="loading && postList.length === 0" class="loading-box">
        <text class="loading-text">加载中...</text>
      </view>

      <!-- 加载更多 -->
      <view v-if="postList.length > 0" class="load-more">
        <text v-if="loading" class="load-more-text">加载中...</text>
        <text v-else-if="!hasMore" class="load-more-text theme-text-tertiary">没有更多了</text>
      </view>
    </view>

    <!-- 悬浮发布按钮 -->
    <view v-if="postList.length > 0" class="fab" @click="goToPublish">
      <text class="fab-icon">+</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { getUserPostList, deletePost, type Post } from '@/api/post';

const themeStore = useThemeStore();

const postList = ref<Post[]>([]);
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);

/**
 * 加载动态列表
 */
const loadPostList = async (refresh = false) => {
  if (loading.value || (!refresh && !hasMore.value)) {
    return;
  }

  try {
    loading.value = true;

    if (refresh) {
      page.value = 1;
      postList.value = [];
      hasMore.value = true;
    }

    const response = await getUserPostList(undefined, {
      page: page.value,
      size: 10,
    });

    const newPostList = response.data.items || [];

    if (refresh) {
      postList.value = newPostList;
    } else {
      postList.value.push(...newPostList);
    }

    hasMore.value = postList.value.length < (response.data.total || 0);
    page.value++;
  } catch (error) {
    console.error('加载动态列表失败:', error);
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
 * 格式化内容（截取前50字）
 */
const formatContent = (content: string) => {
  if (!content) return '';
  return content.length > 50 ? content.substring(0, 50) + '...' : content;
};

/**
 * 格式化时间
 */
const formatTime = (time: string) => {
  const date = new Date(time);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const minute = 60 * 1000;
  const hour = 60 * minute;
  const day = 24 * hour;

  if (diff < minute) {
    return '刚刚';
  } else if (diff < hour) {
    return `${Math.floor(diff / minute)}分钟前`;
  } else if (diff < day) {
    return `${Math.floor(diff / hour)}小时前`;
  } else if (diff < 7 * day) {
    return `${Math.floor(diff / day)}天前`;
  } else {
    return date.toLocaleDateString();
  }
};

/**
 * 删除动态
 */
const handleDelete = async (id: number) => {
  try {
    uni.showModal({
      title: '提示',
      content: '确定要删除这条动态吗？',
      success: async (res) => {
        if (res.confirm) {
          await deletePost(id);
          // 从列表中移除
          postList.value = postList.value.filter(item => item.id !== id);
          uni.showToast({
            title: '删除成功',
            icon: 'success',
            duration: 1500,
          });
        }
      },
    });
  } catch (error) {
    console.error('删除动态失败:', error);
    uni.showToast({
      title: '删除失败',
      icon: 'none',
      duration: 2000,
    });
  }
};

/**
 * 跳转到动态详情
 */
const goToDetail = (id: number) => {
  uni.navigateTo({
    url: `/pages/post-detail/post-detail?id=${id}`,
  });
};

/**
 * 跳转到发布页
 */
const goToPublish = () => {
  uni.navigateTo({
    url: '/pages/publish-post/publish-post',
  });
};

/**
 * 下拉刷新
 */
const onPullDownRefresh = async () => {
  await loadPostList(true);
  uni.stopPullDownRefresh();
};

/**
 * 上拉加载更多
 */
const onReachBottom = () => {
  loadPostList();
};

// 页面加载时获取数据
onMounted(() => {
  loadPostList(true);
});

// 导出给页面生命周期使用
defineExpose({
  onPullDownRefresh,
  onReachBottom,
});
</script>

<style lang="scss" scoped>
.my-posts-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 120rpx;
}

.container {
  padding: $spacing-md;
}

.empty-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 200rpx $spacing-xl 100rpx;

  .empty-icon {
    font-size: 120rpx;
    margin-bottom: $spacing-lg;
    opacity: 0.5;
  }

  .empty-text {
    font-size: $font-size-md;
    color: var(--text-secondary);
    margin-bottom: $spacing-xl;
  }

  .publish-btn {
    width: 300rpx;
    height: 80rpx;
    line-height: 80rpx;
    font-size: $font-size-md;
    color: #ffffff;
    background-color: var(--color-primary);
    border: none;
    border-radius: $border-radius-lg;
  }
}

.post-list {
  .post-card {
    margin-bottom: $spacing-lg;
    padding: $spacing-lg;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-sm);
    transition: all $transition-normal;

    &:active {
      transform: translateY(-4rpx);
      box-shadow: var(--shadow-md);
    }

    .post-content {
      font-size: $font-size-md;
      line-height: 1.8;
      color: var(--text-primary);
      margin-bottom: $spacing-md;
      white-space: pre-wrap;
    }

    .poetry-link {
      padding: $spacing-md;
      background-color: var(--bg-secondary);
      border-radius: $border-radius-md;
      border-left: 4rpx solid var(--color-primary);
      margin-bottom: $spacing-md;

      .poetry-title {
        font-size: $font-size-md;
        font-weight: $font-weight-medium;
        color: var(--text-primary);
        margin-bottom: $spacing-xs;
      }

      .poetry-content {
        font-size: $font-size-sm;
        color: var(--text-secondary);
        line-height: 1.6;
      }
    }

    .image-list {
      display: flex;
      gap: $spacing-sm;
      margin-bottom: $spacing-md;

      .image-item {
        width: 200rpx;
        height: 200rpx;
        border-radius: $border-radius-md;
      }
    }

    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: $spacing-sm;
      margin-bottom: $spacing-md;

      .tag {
        padding: 4rpx 16rpx;
        font-size: $font-size-xs;
        background-color: var(--bg-secondary);
        border-radius: $border-radius-sm;
      }
    }

    .post-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: $spacing-md;
      margin-bottom: $spacing-md;
      border-top: 1px solid var(--border-primary);

      .post-meta {
        font-size: $font-size-xs;
      }

      .post-actions {
        display: flex;
        align-items: center;
        gap: $spacing-lg;

        .action-item {
          display: flex;
          align-items: center;
          gap: $spacing-xs;

          .icon {
            font-size: 28rpx;
          }

          .count {
            font-size: $font-size-sm;
            color: var(--text-secondary);
          }
        }
      }
    }

    .post-operations {
      display: flex;
      justify-content: flex-end;

      .operation-btn {
        padding: 8rpx 24rpx;
        font-size: $font-size-sm;
        color: var(--color-error);
        background-color: transparent;
        border: 1px solid var(--color-error);
        border-radius: $border-radius-md;
        line-height: 1.5;

        &:active {
          opacity: 0.7;
        }
      }
    }
  }
}

.loading-box {
  padding: 80rpx 0;
  text-align: center;

  .loading-text {
    font-size: $font-size-md;
    color: var(--text-tertiary);
  }
}

.load-more {
  padding: $spacing-lg 0;
  text-align: center;

  .load-more-text {
    font-size: $font-size-sm;
    color: var(--text-tertiary);
  }
}

.fab {
  position: fixed;
  right: 60rpx;
  bottom: 180rpx;
  width: 100rpx;
  height: 100rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-primary);
  border-radius: 50%;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  transition: all $transition-normal;

  &:active {
    transform: scale(0.95);
  }

  .fab-icon {
    font-size: 60rpx;
    font-weight: $font-weight-bold;
    color: #ffffff;
    line-height: 1;
  }
}
</style>
