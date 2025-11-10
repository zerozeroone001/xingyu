<template>
  <view class="author-list-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 搜索栏 -->
      <view class="search-bar theme-card">
        <text class="search-icon">🔍</text>
        <input
          v-model="searchKeyword"
          class="search-input"
          placeholder="搜索作者"
          @confirm="handleSearch"
        />
      </view>

      <!-- 朝代筛选 -->
      <view class="dynasty-filter">
        <scroll-view class="filter-scroll" scroll-x>
          <view
            v-for="dynasty in dynasties"
            :key="dynasty.value"
            class="filter-item"
            :class="{ active: currentDynasty === dynasty.value }"
            @click="filterByDynasty(dynasty.value)"
          >
            {{ dynasty.label }}
          </view>
        </scroll-view>
      </view>

      <!-- 作者列表 -->
      <view v-if="authorList.length > 0" class="author-list">
        <view
          v-for="author in authorList"
          :key="author.id"
          class="author-card theme-card"
          @click="goToDetail(author.id)"
        >
          <view class="author-info">
            <image
              v-if="author.avatar"
              class="avatar"
              :src="author.avatar"
              mode="aspectFill"
            />
            <view v-else class="avatar-placeholder">
              {{ author.name?.charAt(0) }}
            </view>

            <view class="author-text">
              <view class="author-name">{{ author.name }}</view>
              <view class="author-dynasty theme-text-secondary">{{ author.dynasty }}</view>
              <view v-if="author.biography" class="author-bio theme-text-tertiary">
                {{ formatBio(author.biography) }}
              </view>
            </view>
          </view>

          <view class="author-stats">
            <view class="stat-item">
              <text class="stat-value">{{ author.poetry_count || 0 }}</text>
              <text class="stat-label theme-text-tertiary">诗词</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 空状态 -->
      <view v-else-if="!loading" class="empty-box">
        <text class="empty-icon">📖</text>
        <text class="empty-text">暂无作者数据</text>
      </view>

      <!-- 加载中 -->
      <view v-if="loading && authorList.length === 0" class="loading-box">
        <text class="loading-text">加载中...</text>
      </view>

      <!-- 加载更多 -->
      <view v-if="authorList.length > 0" class="load-more">
        <text v-if="loading" class="load-more-text">加载中...</text>
        <text v-else-if="!hasMore" class="load-more-text theme-text-tertiary">没有更多了</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { getAuthorList, getHotAuthorList, getAuthorsByDynasty, type Author } from '@/api/author';

const themeStore = useThemeStore();

const searchKeyword = ref('');
const currentDynasty = ref('');
const authorList = ref<Author[]>([]);
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);

const dynasties = ref([
  { label: '全部', value: '' },
  { label: '先秦', value: '先秦' },
  { label: '汉代', value: '汉代' },
  { label: '魏晋', value: '魏晋' },
  { label: '南北朝', value: '南北朝' },
  { label: '隋代', value: '隋代' },
  { label: '唐代', value: '唐代' },
  { label: '五代', value: '五代' },
  { label: '宋代', value: '宋代' },
  { label: '金朝', value: '金朝' },
  { label: '元代', value: '元代' },
  { label: '明代', value: '明代' },
  { label: '清代', value: '清代' },
  { label: '近现代', value: '近现代' },
]);

/**
 * 加载作者列表
 */
const loadAuthorList = async (refresh = false) => {
  if (loading.value || (!refresh && !hasMore.value)) {
    return;
  }

  try {
    loading.value = true;

    if (refresh) {
      page.value = 1;
      authorList.value = [];
      hasMore.value = true;
    }

    let response;
    if (currentDynasty.value) {
      response = await getAuthorsByDynasty(currentDynasty.value, {
        page: page.value,
        size: 20,
      });
    } else if (searchKeyword.value) {
      response = await getAuthorList({
        page: page.value,
        size: 20,
        search: searchKeyword.value,
      });
    } else {
      response = await getHotAuthorList({
        page: page.value,
        size: 20,
      });
    }

    const newAuthorList = response.data.list || [];

    if (refresh) {
      authorList.value = newAuthorList;
    } else {
      authorList.value.push(...newAuthorList);
    }

    hasMore.value = authorList.value.length < (response.data.total || 0);
    page.value++;
  } catch (error) {
    console.error('加载作者列表失败:', error);
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
 * 搜索
 */
const handleSearch = () => {
  currentDynasty.value = '';
  loadAuthorList(true);
};

/**
 * 按朝代筛选
 */
const filterByDynasty = (dynasty: string) => {
  currentDynasty.value = dynasty;
  searchKeyword.value = '';
  loadAuthorList(true);
};

/**
 * 格式化简介
 */
const formatBio = (bio: string) => {
  if (!bio) return '';
  return bio.length > 50 ? bio.substring(0, 50) + '...' : bio;
};

/**
 * 跳转到作者详情
 */
const goToDetail = (id: number) => {
  uni.navigateTo({
    url: `/author-detail?id=${id}`,
  });
};

/**
 * 下拉刷新
 */
const onPullDownRefresh = async () => {
  await loadAuthorList(true);
  uni.stopPullDownRefresh();
};

/**
 * 上拉加载更多
 */
const onReachBottom = () => {
  loadAuthorList();
};

// 页面加载时获取数据
onMounted(() => {
  loadAuthorList(true);
});

// 导出给页面生命周期使用
defineExpose({
  onPullDownRefresh,
  onReachBottom,
});
</script>

<style lang="scss" scoped>
.author-list-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 120rpx;
}

.container {
  padding: $spacing-md;
}

.search-bar {
  display: flex;
  align-items: center;
  padding: $spacing-md $spacing-lg;
  margin-bottom: $spacing-md;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  .search-icon {
    font-size: 32rpx;
    margin-right: $spacing-sm;
  }

  .search-input {
    flex: 1;
    font-size: $font-size-md;
    color: var(--text-primary);
  }
}

.dynasty-filter {
  margin-bottom: $spacing-lg;

  .filter-scroll {
    white-space: nowrap;

    .filter-item {
      display: inline-block;
      padding: $spacing-sm $spacing-lg;
      margin-right: $spacing-sm;
      font-size: $font-size-sm;
      color: var(--text-secondary);
      background-color: var(--bg-card);
      border-radius: $border-radius-lg;
      cursor: pointer;
      transition: all $transition-normal;

      &.active {
        color: #ffffff;
        background-color: var(--color-primary);
        font-weight: $font-weight-medium;
      }

      &:active {
        opacity: 0.7;
      }
    }
  }
}

.author-list {
  .author-card {
    display: flex;
    justify-content: space-between;
    margin-bottom: $spacing-md;
    padding: $spacing-lg;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-sm);
    transition: all $transition-normal;

    &:active {
      transform: translateY(-4rpx);
      box-shadow: var(--shadow-md);
    }

    .author-info {
      display: flex;
      align-items: center;
      flex: 1;
      min-width: 0;

      .avatar,
      .avatar-placeholder {
        width: 100rpx;
        height: 100rpx;
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
        font-size: $font-size-xl;
        font-weight: $font-weight-bold;
      }

      .author-text {
        flex: 1;
        min-width: 0;

        .author-name {
          font-size: $font-size-lg;
          font-weight: $font-weight-bold;
          color: var(--text-primary);
          margin-bottom: 4rpx;
        }

        .author-dynasty {
          font-size: $font-size-sm;
          margin-bottom: $spacing-xs;
        }

        .author-bio {
          font-size: $font-size-xs;
          line-height: 1.4;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
      }
    }

    .author-stats {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      margin-left: $spacing-md;

      .stat-item {
        display: flex;
        flex-direction: column;
        align-items: center;

        .stat-value {
          font-size: $font-size-lg;
          font-weight: $font-weight-bold;
          color: var(--text-primary);
          margin-bottom: 4rpx;
        }

        .stat-label {
          font-size: $font-size-xs;
        }
      }
    }
  }
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
