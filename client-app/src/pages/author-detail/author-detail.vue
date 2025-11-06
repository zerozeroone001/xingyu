<template>
  <view class="author-detail-page" :class="themeStore.themeClass">
    <view v-if="author" class="container">
      <!-- 作者信息卡片 -->
      <view class="author-card theme-card">
        <image
          v-if="author.avatar"
          class="avatar"
          :src="author.avatar"
          mode="aspectFill"
        />
        <view v-else class="avatar-placeholder">
          {{ author.name?.charAt(0) }}
        </view>

        <view class="author-name">{{ author.name }}</view>
        <view class="author-dynasty theme-text-secondary">{{ author.dynasty }}</view>

        <view v-if="author.birth_year || author.death_year" class="author-years theme-text-tertiary">
          {{ author.birth_year || '?' }} - {{ author.death_year || '?' }}
        </view>

        <view class="author-stats">
          <view class="stat-item">
            <view class="stat-value">{{ author.poetry_count || 0 }}</view>
            <view class="stat-label theme-text-tertiary">诗词</view>
          </view>
          <view class="stat-divider"></view>
          <view class="stat-item">
            <view class="stat-value">{{ author.views_count || 0 }}</view>
            <view class="stat-label theme-text-tertiary">浏览</view>
          </view>
        </view>
      </view>

      <!-- 作者简介 -->
      <view v-if="author.biography" class="biography-card theme-card">
        <view class="section-title">作者简介</view>
        <view class="biography-text">{{ author.biography }}</view>
      </view>

      <!-- 诗词列表 -->
      <view class="poetry-section">
        <view class="section-title">代表作品</view>
        <view v-if="poetryList.length > 0" class="poetry-list">
          <view
            v-for="poetry in poetryList"
            :key="poetry.id"
            class="poetry-card theme-card"
            @click="goToPoetryDetail(poetry.id)"
          >
            <view class="poetry-title">{{ poetry.title }}</view>
            <view class="poetry-content">{{ formatContent(poetry.content) }}</view>
            <view class="poetry-actions">
              <view class="action-item">
                <text class="icon">❤️</text>
                <text class="count">{{ poetry.likes_count || 0 }}</text>
              </view>
              <view class="action-item">
                <text class="icon">⭐</text>
                <text class="count">{{ poetry.collects_count || 0 }}</text>
              </view>
              <view class="action-item">
                <text class="icon">💬</text>
                <text class="count">{{ poetry.comments_count || 0 }}</text>
              </view>
            </view>
          </view>
        </view>

        <view v-else-if="!loading" class="empty-box">
          <text class="empty-text">暂无作品</text>
        </view>

        <!-- 加载更多 -->
        <view v-if="poetryList.length > 0" class="load-more">
          <text v-if="loading" class="load-more-text">加载中...</text>
          <text v-else-if="!hasMore" class="load-more-text theme-text-tertiary">没有更多了</text>
        </view>
      </view>
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
import { getAuthorDetail, getAuthorPoetryList, type Author } from '@/api/author';
import type { Poetry } from '@/api/poetry';

const themeStore = useThemeStore();

const authorId = ref<number>(0);
const author = ref<Author | null>(null);
const poetryList = ref<Poetry[]>([]);
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);

/**
 * 加载作者信息
 */
const loadAuthorDetail = async () => {
  try {
    loading.value = true;
    const response = await getAuthorDetail(authorId.value);
    author.value = response.data;
  } catch (error) {
    console.error('加载作者信息失败:', error);
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
 * 加载诗词列表
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

    const response = await getAuthorPoetryList(authorId.value, {
      page: page.value,
      size: 10,
    });

    const newPoetryList = response.data.items || [];

    if (refresh) {
      poetryList.value = newPoetryList;
    } else {
      poetryList.value.push(...newPoetryList);
    }

    hasMore.value = poetryList.value.length < (response.data.total || 0);
    page.value++;
  } catch (error) {
    console.error('加载诗词列表失败:', error);
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
 * 跳转到诗词详情
 */
const goToPoetryDetail = (id: number) => {
  uni.navigateTo({
    url: `/pages/poetry-detail/poetry-detail?id=${id}`,
  });
};

/**
 * 下拉刷新
 */
const onPullDownRefresh = async () => {
  await Promise.all([loadAuthorDetail(), loadPoetryList(true)]);
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
  const pages = getCurrentPages();
  const currentPage = pages[pages.length - 1] as any;
  const options = currentPage.options || currentPage.$page?.options || {};
  authorId.value = parseInt(options.id || '0');

  if (authorId.value) {
    loadAuthorDetail();
    loadPoetryList(true);
  }
});

// 导出给页面生命周期使用
defineExpose({
  onPullDownRefresh,
  onReachBottom,
});
</script>

<style lang="scss" scoped>
.author-detail-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 120rpx;
}

.container {
  padding: $spacing-md;
}

.author-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $spacing-xl;
  margin-bottom: $spacing-lg;
  background-color: var(--bg-card);
  border-radius: $border-radius-xl;
  box-shadow: var(--shadow-md);

  .avatar,
  .avatar-placeholder {
    width: 150rpx;
    height: 150rpx;
    border-radius: 50%;
    margin-bottom: $spacing-md;
  }

  .avatar-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--color-primary);
    color: #ffffff;
    font-size: 64rpx;
    font-weight: $font-weight-bold;
  }

  .author-name {
    font-size: $font-size-xxl;
    font-weight: $font-weight-bold;
    color: var(--text-primary);
    margin-bottom: $spacing-xs;
  }

  .author-dynasty {
    font-size: $font-size-md;
    margin-bottom: $spacing-xs;
  }

  .author-years {
    font-size: $font-size-sm;
    margin-bottom: $spacing-lg;
  }

  .author-stats {
    display: flex;
    align-items: center;
    width: 100%;
    padding-top: $spacing-lg;
    border-top: 1px solid var(--border-primary);

    .stat-item {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;

      .stat-value {
        font-size: $font-size-xl;
        font-weight: $font-weight-bold;
        color: var(--text-primary);
        margin-bottom: $spacing-xs;
      }

      .stat-label {
        font-size: $font-size-sm;
      }
    }

    .stat-divider {
      width: 1px;
      height: 60rpx;
      background-color: var(--border-primary);
    }
  }
}

.biography-card {
  padding: $spacing-xl;
  margin-bottom: $spacing-lg;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  .section-title {
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    color: var(--text-primary);
    margin-bottom: $spacing-md;
  }

  .biography-text {
    font-size: $font-size-md;
    line-height: 1.8;
    color: var(--text-primary);
    text-align: justify;
  }
}

.poetry-section {
  .section-title {
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    color: var(--text-primary);
    margin-bottom: $spacing-md;
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
        margin-bottom: $spacing-md;
        text-align: center;
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

  .empty-box {
    padding: 80rpx 0;
    text-align: center;

    .empty-text {
      font-size: $font-size-md;
      color: var(--text-secondary);
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
}

.loading-box {
  padding: 200rpx 0;
  text-align: center;

  .loading-text {
    font-size: $font-size-md;
    color: var(--text-tertiary);
  }
}
</style>
