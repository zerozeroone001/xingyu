<template>
  <view class="discover-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 搜索栏 -->
      <view class="search-bar theme-card" @click="goToSearch">
        <text class="search-icon">🔍</text>
        <text class="search-text theme-text-tertiary">搜索诗词、作者</text>
      </view>

      <!-- 功能入口 -->
      <view class="function-grid">
        <view class="function-item theme-card" @click="goToPoetryList">
          <text class="icon">📖</text>
          <text class="label">诗词列表</text>
        </view>
        <view class="function-item theme-card" @click="goToAuthorList">
          <text class="icon">✍️</text>
          <text class="label">作者列表</text>
        </view>
        <view class="function-item theme-card" @click="goToHotPoetry">
          <text class="icon">🔥</text>
          <text class="label">热门诗词</text>
        </view>
        <view class="function-item theme-card" @click="getRandomPoetryAndGo">
          <text class="icon">🎲</text>
          <text class="label">随机一首</text>
        </view>
      </view>

      <!-- 朝代分类 -->
      <view class="section">
        <view class="section-title">按朝代浏览</view>
        <view class="dynasty-list">
          <view
            v-for="dynasty in dynastyList"
            :key="dynasty"
            class="dynasty-item theme-card"
            @click="goToPoetryByDynasty(dynasty)"
          >
            <text class="dynasty-text">{{ dynasty }}</text>
          </view>
        </view>
      </view>

      <!-- 热门作者 -->
      <view class="section">
        <view class="section-title">
          <text>热门作者</text>
          <text class="more-link" @click="goToAuthorList">更多 →</text>
        </view>
        <view v-if="hotAuthors.length > 0" class="author-grid">
          <view
            v-for="author in hotAuthors"
            :key="author.id"
            class="author-item theme-card"
            @click="goToAuthorDetail(author.id)"
          >
            <view class="author-avatar">{{ author.name.charAt(0) }}</view>
            <view class="author-name">{{ author.name }}</view>
            <view class="author-dynasty theme-text-tertiary">{{ author.dynasty }}</view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { getHotAuthorList, type Author } from '@/api/author';
import { getRandomPoetry } from '@/api/poetry';

const themeStore = useThemeStore();

const hotAuthors = ref<Author[]>([]);
const dynastyList = ['先秦', '汉', '魏晋', '南北朝', '隋', '唐', '宋', '元', '明', '清'];

/**
 * 加载热门作者
 */
const loadHotAuthors = async () => {
  try {
    const response = await getHotAuthorList({ page: 1, size: 6 });
    hotAuthors.value = response.data.items || [];
  } catch (error) {
    console.error('加载热门作者失败:', error);
  }
};

/**
 * 获取随机诗词并跳转
 */
const getRandomPoetryAndGo = async () => {
  try {
    uni.showLoading({ title: '加载中...' });
    const response = await getRandomPoetry();
    uni.hideLoading();

    if (response.data) {
      uni.navigateTo({
        url: `/pages/poetry-detail/poetry-detail?id=${response.data.id}`,
      });
    }
  } catch (error) {
    uni.hideLoading();
    console.error('获取随机诗词失败:', error);
  }
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
 * 跳转到作者列表
 */
const goToAuthorList = () => {
  uni.navigateTo({
    url: '/pages/author-list/author-list',
  });
};

/**
 * 跳转到热门诗词
 */
const goToHotPoetry = () => {
  uni.navigateTo({
    url: '/pages/poetry-list/poetry-list?type=hot',
  });
};

/**
 * 按朝代浏览诗词
 */
const goToPoetryByDynasty = (dynasty: string) => {
  uni.navigateTo({
    url: `/pages/poetry-list/poetry-list?dynasty=${dynasty}`,
  });
};

/**
 * 跳转到作者详情
 */
const goToAuthorDetail = (id: number) => {
  uni.navigateTo({
    url: `/pages/author-detail/author-detail?id=${id}`,
  });
};

onMounted(() => {
  loadHotAuthors();
});
</script>

<style lang="scss" scoped>
.discover-page {
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
  margin-bottom: $spacing-xl;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  .search-icon {
    font-size: 32rpx;
    margin-right: $spacing-sm;
  }

  .search-text {
    flex: 1;
    font-size: $font-size-md;
  }
}

.function-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-md;
  margin-bottom: $spacing-xl;

  .function-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: $spacing-lg;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: all $transition-normal;

    &:active {
      transform: scale(0.95);
    }

    .icon {
      font-size: 48rpx;
      margin-bottom: $spacing-sm;
    }

    .label {
      font-size: $font-size-sm;
      color: var(--text-primary);
      text-align: center;
    }
  }
}

.section {
  margin-bottom: $spacing-xl;

  .section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    color: var(--text-primary);
    margin-bottom: $spacing-md;

    .more-link {
      font-size: $font-size-sm;
      font-weight: $font-weight-normal;
      color: var(--color-primary);
    }
  }

  .dynasty-list {
    display: flex;
    flex-wrap: wrap;
    gap: $spacing-sm;

    .dynasty-item {
      padding: $spacing-sm $spacing-lg;
      background-color: var(--bg-card);
      border-radius: $border-radius-md;
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      transition: all $transition-normal;

      &:active {
        transform: scale(0.95);
      }

      .dynasty-text {
        font-size: $font-size-md;
        color: var(--text-primary);
      }
    }
  }

  .author-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: $spacing-md;

    .author-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: $spacing-lg;
      background-color: var(--bg-card);
      border-radius: $border-radius-lg;
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      transition: all $transition-normal;

      &:active {
        transform: scale(0.95);
      }

      .author-avatar {
        width: 100rpx;
        height: 100rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: $spacing-sm;
        background-color: var(--color-primary);
        color: #ffffff;
        font-size: $font-size-xl;
        font-weight: $font-weight-bold;
        border-radius: 50%;
      }

      .author-name {
        font-size: $font-size-md;
        font-weight: $font-weight-medium;
        color: var(--text-primary);
        margin-bottom: 4rpx;
        text-align: center;
      }

      .author-dynasty {
        font-size: $font-size-xs;
        text-align: center;
      }
    }
  }
}
</style>
