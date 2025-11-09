<template>
  <view class="square-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 发布按钮 -->
      <view class="publish-btn" @click="goToPublish">
        <text class="icon">✏️</text>
        <text class="text">发布动态</text>
      </view>

      <!--动态列表 -->
      <view v-if="loading && postList.length === 0" class="loading-box">
        <text class="loading-text">加载中...</text>
      </view>

      <view v-else-if="postList.length === 0" class="empty-box">
        <text class="empty-text">还没有动态哦</text>
      </view>

      <view v-else class="post-list">
        <view
          v-for="post in postList"
          :key="post.id"
          class="post-card theme-card"
          @click="goToPostDetail(post.id)"
        >
          <!-- 用户信息 -->
          <view class="post-header">
            <image v-if="post.user_avatar" class="avatar" :src="post.user_avatar" mode="aspectFill" />
            <view v-else class="avatar-placeholder">{{ post.user_name.charAt(0) }}</view>
            <view class="user-info">
              <text class="username">{{ post.user_name }}</text>
              <text class="time theme-text-tertiary">{{ formatTime(post.created_at) }}</text>
            </view>
          </view>

          <!-- 动态内容 -->
          <view class="post-content">{{ post.content }}</view>

          <!-- 关联诗词 -->
          <view v-if="post.poetry_id" class="linked-poetry theme-bg-secondary">
            <text class="poetry-tag">📖</text>
            <text class="poetry-title">{{ post.poetry_title }}</text>
          </view>

          <!-- 图片 -->
          <view v-if="post.images && post.images.length" class="post-images">
            <image
              v-for="(img, index) in post.images.slice(0, 3)"
              :key="index"
              class="post-image"
              :src="img"
              mode="aspectFill"
            />
          </view>

          <!-- 互动数据 -->
          <view class="post-actions">
            <view class="action-item">
              <text class="icon">❤️</text>
              <text class="count">{{ post.likes_count || 0 }}</text>
            </view>
            <view class="action-item">
              <text class="icon">💬</text>
              <text class="count">{{ post.comments_count || 0 }}</text>
            </view>
            <view class="action-item">
              <text class="icon">👀</text>
              <text class="count">{{ post.views_count || 0 }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { useUserStore } from '@/store/modules/user';
import { getPostList, type Post } from '@/api/post';
import dayjs from 'dayjs';

const themeStore = useThemeStore();
const userStore = useUserStore();

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

    const response = await getPostList({
      page: page.value,
      size: 20,
    });

    const newPostList = response.data.list || [];

    if (refresh) {
      postList.value = newPostList;
    } else {
      postList.value.push(...newPostList);
    }

    hasMore.value = postList.value.length < (response.data.total || 0);
    page.value++;
  } catch (error) {
    console.error('加载动态列表失败:', error);
  } finally {
    loading.value = false;
  }
};

/**
 * 格式化时间
 */
const formatTime = (time: string) => {
  return dayjs(time).format('MM-DD HH:mm');
};

/**
 * 跳转到发布页
 */
const goToPublish = () => {
  if (!userStore.checkLoginStatus()) {
    return;
  }

  uni.navigateTo({
    url: '/pages/publish-post/publish-post',
  });
};

/**
 * 跳转到动态详情
 */
const goToPostDetail = (id: number) => {
  uni.navigateTo({
    url: `/pages/post-detail/post-detail?id=${id}`,
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

onMounted(() => {
  loadPostList(true);
});

defineExpose({
  onPullDownRefresh,
  onReachBottom,
});
</script>

<style lang="scss" scoped>
.square-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 120rpx;
}

.container {
  padding: $spacing-md;
}

.publish-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-md;
  margin-bottom: $spacing-lg;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-md);
  cursor: pointer;
  transition: all $transition-normal;

  &:active {
    transform: scale(0.98);
  }

  .icon {
    font-size: 32rpx;
    margin-right: $spacing-sm;
  }

  .text {
    font-size: $font-size-md;
    font-weight: $font-weight-medium;
    color: #ffffff;
  }
}

.loading-box,
.empty-box {
  padding: 120rpx 0;
  text-align: center;

  .loading-text,
  .empty-text {
    font-size: $font-size-md;
    color: var(--text-tertiary);
  }
}

.post-list {
  .post-card {
    padding: $spacing-lg;
    margin-bottom: $spacing-lg;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-sm);

    .post-header {
      display: flex;
      align-items: center;
      margin-bottom: $spacing-md;

      .avatar,
      .avatar-placeholder {
        width: 80rpx;
        height: 80rpx;
        border-radius: 50%;
        margin-right: $spacing-sm;
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

      .user-info {
        flex: 1;
        display: flex;
        flex-direction: column;

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
      font-size: $font-size-md;
      line-height: 1.6;
      color: var(--text-primary);
      margin-bottom: $spacing-md;
      word-break: break-word;
    }

    .linked-poetry {
      padding: $spacing-sm $spacing-md;
      margin-bottom: $spacing-md;
      border-radius: $border-radius-md;

      .poetry-tag {
        margin-right: $spacing-xs;
      }

      .poetry-title {
        font-size: $font-size-sm;
        color: var(--text-secondary);
      }
    }

    .post-images {
      display: flex;
      gap: $spacing-xs;
      margin-bottom: $spacing-md;

      .post-image {
        width: 200rpx;
        height: 200rpx;
        border-radius: $border-radius-md;
      }
    }

    .post-actions {
      display: flex;
      align-items: center;
      gap: $spacing-xl;
      padding-top: $spacing-md;
      border-top: 1px solid var(--border-primary);

      .action-item {
        display: flex;
        align-items: center;
        gap: $spacing-xs;

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
}
</style>
