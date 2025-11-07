<template>
  <view class="index-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 头部搜索栏 -->
      <view class="header">
        <view class="search-bar theme-card" @click="goToSearch">
          <text class="search-icon">🔍</text>
          <text class="search-text theme-text-tertiary">搜索诗词、作者</text>
        </view>
      </view>

      <!-- 每日推荐 -->
      <view v-if="dailyPoetry" class="daily-section">
        <view class="section-title">
          <text class="title-text">每日一诗</text>
          <text class="title-icon">✨</text>
        </view>
        <view class="daily-card theme-card" @click="goToDetail(dailyPoetry.id)">
          <view class="poetry-title">{{ dailyPoetry.title }}</view>
          <view class="poetry-author theme-text-secondary">
            {{ dailyPoetry.dynasty }} · {{ dailyPoetry.author_name }}
          </view>
          <view class="poetry-content">{{ formatContent(dailyPoetry.content) }}</view>
        </view>
      </view>

      <!-- 诗词列表 -->
      <view class="poetry-section">
        <view class="section-title">
          <text class="title-text">推荐诗词</text>
          <text class="more-link" @click="goToPoetryList">更多 →</text>
        </view>

        <view v-if="loading && poetryList.length === 0" class="loading-box">
          <text class="loading-text">加载中...</text>
        </view>

        <view v-else-if="poetryList.length === 0" class="empty-box">
          <text class="empty-text">暂无数据</text>
        </view>

        <view v-else class="poetry-list">
          <view
            v-for="poetry in poetryList"
            :key="poetry.id"
            class="poetry-card theme-card"
            @click="goToDetail(poetry.id)"
          >
            <view class="poetry-title">{{ poetry.title }}</view>
            <view class="poetry-author theme-text-secondary">
              {{ poetry.dynasty }} · {{ poetry.author_name }}
            </view>
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
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { type Poetry } from '@/api/poetry';
import { mockPoetryList, mockDailyPoetry, getMockPoetryPage } from '@/mock/data';

const themeStore = useThemeStore();

const poetryList = ref<Poetry[]>([]);
const dailyPoetry = ref<Poetry | null>(null);
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);

// 使用模拟数据标志
const useMockData = true;

/**
 * 加载每日推荐
 */
const loadDailyPoetry = async () => {
  try {
    if (useMockData) {
      // 使用模拟数据
      dailyPoetry.value = mockDailyPoetry;
      return;
    }

    // 以下是原来的 API 调用代码（暂时注释）
    // const response = await getDailyRecommendations();
    // if (response.data && response.data.length > 0) {
    //   dailyPoetry.value = response.data[0];
    // } else {
    //   const randomResponse = await getRandomPoetry();
    //   dailyPoetry.value = randomResponse.data;
    // }
  } catch (error) {
    console.error('加载每日推荐失败:', error);
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

    if (useMockData) {
      // 使用模拟数据
      const mockResponse = getMockPoetryPage(page.value, 10);
      const newPoetryList = mockResponse.items;

      if (refresh) {
        poetryList.value = newPoetryList;
      } else {
        poetryList.value.push(...newPoetryList);
      }

      hasMore.value = poetryList.value.length < mockResponse.total;
      page.value++;
      return;
    }

    // 以下是原来的 API 调用代码（暂时注释）
    // const response = await getHotPoetryList({
    //   page: page.value,
    //   size: 10,
    // });
    // const newPoetryList = response.data.items || [];
    // if (refresh) {
    //   poetryList.value = newPoetryList;
    // } else {
    //   poetryList.value.push(...newPoetryList);
    // }
    // hasMore.value = poetryList.value.length < (response.data.total || 0);
    // page.value++;
  } catch (error) {
    console.error('加载诗词列表失败:', error);
    if (typeof uni !== 'undefined') {
      uni.showToast({
        title: '加载失败',
        icon: 'none',
        duration: 2000,
      });
    }
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
const goToDetail = (id: number) => {
  uni.navigateTo({
    url: `/pages/poetry-detail/poetry-detail?id=${id}`,
  });
};

/**
 * 跳转到搜索页
 */
const goToSearch = () => {
  uni.navigateTo({
    url: '/pages/search/search',
  });
};

/**
 * 跳转到诗词列表
 */
const goToPoetryList = () => {
  uni.navigateTo({
    url: '/pages/poetry-list/poetry-list',
  });
};

/**
 * 下拉刷新
 */
const onPullDownRefresh = async () => {
  await Promise.all([loadDailyPoetry(), loadPoetryList(true)]);
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
  loadDailyPoetry();
  loadPoetryList(true);
});

// 导出给页面生命周期使用
defineExpose({
  onPullDownRefresh,
  onReachBottom,
});
</script>

<style lang="scss" scoped>
.index-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 120rpx;
}

.container {
  padding: $spacing-md;
}

.header {
  margin-bottom: $spacing-lg;

  .search-bar {
    display: flex;
    align-items: center;
    padding: $spacing-md $spacing-lg;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: all $transition-normal;

    &:active {
      transform: scale(0.98);
    }

    .search-icon {
      font-size: 32rpx;
      margin-right: $spacing-sm;
    }

    .search-text {
      flex: 1;
      font-size: $font-size-md;
    }
  }
}

.daily-section {
  margin-bottom: $spacing-xl;

  .section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: $spacing-md;

    .title-text {
      font-size: $font-size-lg;
      font-weight: $font-weight-bold;
      color: var(--text-primary);
    }

    .title-icon {
      font-size: 32rpx;
    }
  }

  .daily-card {
    padding: $spacing-xl;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-md);
    cursor: pointer;
    transition: all $transition-normal;

    &:active {
      transform: translateY(-4rpx);
      box-shadow: var(--shadow-lg);
    }

    .poetry-title {
      font-size: $font-size-xl;
      font-weight: $font-weight-bold;
      color: var(--text-primary);
      margin-bottom: $spacing-sm;
      text-align: center;
    }

    .poetry-author {
      font-size: $font-size-sm;
      text-align: center;
      margin-bottom: $spacing-lg;
    }

    .poetry-content {
      font-size: $font-size-md;
      line-height: 1.8;
      color: var(--text-primary);
      white-space: pre-wrap;
    }
  }
}

.poetry-section {
  .section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: $spacing-md;

    .title-text {
      font-size: $font-size-lg;
      font-weight: $font-weight-bold;
      color: var(--text-primary);
    }

    .more-link {
      font-size: $font-size-sm;
      color: var(--color-primary);
      cursor: pointer;

      &:active {
        opacity: 0.7;
      }
    }
  }

  .loading-box,
  .empty-box {
    padding: 80rpx 0;
    text-align: center;

    .loading-text,
    .empty-text {
      font-size: $font-size-md;
      color: var(--text-tertiary);
    }
  }

  .poetry-list {
    .poetry-card {
      margin-bottom: $spacing-lg;
      padding: $spacing-lg;
      background-color: var(--bg-card);
      border-radius: $border-radius-lg;
      box-shadow: var(--shadow-sm);
      cursor: pointer;
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
}
</style>
