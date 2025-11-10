<template>
  <view class="my-likes-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 空状态 -->
      <view v-if="!loading && poetryList.length === 0" class="empty-box">
        <text class="empty-icon">❤️</text>
        <text class="empty-text">还没有点赞任何诗词</text>
        <button class="explore-btn" @click="goToIndex">去发现</button>
      </view>

      <!-- 诗词列表 -->
      <view v-else class="poetry-list">
        <view
          v-for="poetry in poetryList"
          :key="poetry.id"
          class="poetry-card theme-card"
          @click="goToDetail(poetry.id)"
        >
          <view class="poetry-title">{{ poetry.title }}</view>
          <view class="poetry-author theme-text-secondary">
            {{ poetry.dynasty }} · {{ poetry.author?.name || '佚名' }}
          </view>
          <view class="poetry-content">{{ formatContent(poetry.content) }}</view>
          <view class="poetry-footer">
            <view class="poetry-actions">
              <view class="action-item">
                <text class="icon">❤️</text>
                <text class="count">{{ poetry.like_count || 0 }}</text>
              </view>
              <view class="action-item">
                <text class="icon">⭐</text>
                <text class="count">{{ poetry.collect_count || 0 }}</text>
              </view>
              <view class="action-item">
                <text class="icon">💬</text>
                <text class="count">{{ poetry.comment_count || 0 }}</text>
              </view>
            </view>
            <button
              class="unlike-btn"
              @click.stop="handleUnlike(poetry.id)"
            >
              取消点赞
            </button>
          </view>
        </view>
      </view>

      <!-- 加载中 -->
      <view v-if="loading && poetryList.length === 0" class="loading-box">
        <text class="loading-text">加载中...</text>
      </view>

      <!-- 加载更多 -->
      <view v-if="poetryList.length > 0" class="load-more">
        <text v-if="loading" class="load-more-text">加载中...</text>
        <text v-else-if="!hasMore" class="load-more-text theme-text-tertiary">没有更多了</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { getUserLikedPoetryList, unlikePoetry, type Poetry } from '@/api/poetry';

const themeStore = useThemeStore();

const poetryList = ref<Poetry[]>([]);
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);

/**
 * 加载点赞列表
 */
const loadPoetryList = async (refresh = false) => {
  if (loading.value || (!refresh && !hasMore.value)) {
    return;
  }

  try {
    loading.value = true;

    if (refresh) {
      page.value = 1;
      poetryList.value = [];
      hasMore.value = true;
    }

    const response = await getUserLikedPoetryList({
      page: page.value,
      size: 10,
    });

    const newPoetryList = response.data.list || [];

    if (refresh) {
      poetryList.value = newPoetryList;
    } else {
      poetryList.value.push(...newPoetryList);
    }

    hasMore.value = poetryList.value.length < (response.data.total || 0);
    page.value++;
  } catch (error) {
    console.error('加载点赞列表失败:', error);
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
 * 格式化内容（截取前80字）
 */
const formatContent = (content: string) => {
  if (!content) return '';
  return content.length > 80 ? content.substring(0, 80) + '...' : content;
};

/**
 * 取消点赞
 */
const handleUnlike = async (id: number) => {
  try {
    uni.showModal({
      title: '提示',
      content: '确定要取消点赞吗？',
      success: async (res) => {
        if (res.confirm) {
          await unlikePoetry(id);
          // 从列表中移除
          poetryList.value = poetryList.value.filter(item => item.id !== id);
          uni.showToast({
            title: '已取消点赞',
            icon: 'success',
            duration: 1500,
          });
        }
      },
    });
  } catch (error) {
    console.error('取消点赞失败:', error);
    uni.showToast({
      title: '操作失败',
      icon: 'none',
      duration: 2000,
    });
  }
};

/**
 * 跳转到诗词详情
 */
const goToDetail = (id: number) => {
  uni.navigateTo({
    url: `/poetry-detail?id=${id}`,
  });
};

/**
 * 跳转到首页
 */
const goToIndex = () => {
  uni.switchTab({
    url: '/',
  });
};

/**
 * 下拉刷新
 */
const onPullDownRefresh = async () => {
  await loadPoetryList(true);
  uni.stopPullDownRefresh();
};

/**
 * 上拉加载更多
 */
const onReachBottom = () => {
  loadPoetryList();
};

// 页面加载时获取数据
onMounted(() => {
  loadPoetryList(true);
});

// 导出给页面生命周期使用
defineExpose({
  onPullDownRefresh,
  onReachBottom,
});
</script>

<style lang="scss" scoped>
.my-likes-page {
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

  .explore-btn {
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

.poetry-list {
  .poetry-card {
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

    .poetry-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: $spacing-md;
      border-top: 1px solid var(--border-primary);

      .poetry-actions {
        display: flex;
        align-items: center;
        gap: $spacing-lg;

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

      .unlike-btn {
        padding: 8rpx 24rpx;
        font-size: $font-size-sm;
        color: var(--text-secondary);
        background-color: transparent;
        border: 1px solid var(--border-primary);
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
</style>
