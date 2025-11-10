<template>
  <view class="poetry-list-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 筛选栏 -->
      <view class="filter-bar theme-card">
        <view class="filter-item">
          <select v-model="filters.dynasty" class="filter-select" @change="handleFilterChange">
            <option value="">全部朝代</option>
            <option v-for="dynasty in dynastyList" :key="dynasty" :value="dynasty">
              {{ dynasty }}
            </option>
          </select>
        </view>
        <view class="filter-item">
          <select v-model="filters.sort_by" class="filter-select" @change="handleFilterChange">
            <option value="created_at">最新</option>
            <option value="read_count">最多浏览</option>
            <option value="like_count">最多点赞</option>
            <option value="collect_count">最多收藏</option>
          </select>
        </view>
      </view>

      <!-- 诗词列表 -->
      <view v-if="loading && poetryList.length === 0" class="loading-box">
        <text class="loading-text">加载中...</text>
      </view>

      <view v-else-if="poetryList.length === 0" class="empty-box">
        <text class="empty-icon">📚</text>
        <text class="empty-text">暂无诗词</text>
      </view>

      <view v-else class="poetry-list">
        <view
          v-for="poetry in poetryList"
          :key="poetry.id"
          class="poetry-card theme-card"
          @click="goToDetail(poetry.id)"
        >
          <view class="poetry-header">
            <view class="poetry-title">{{ poetry.title }}</view>
            <view class="poetry-meta theme-text-tertiary">
              {{ poetry.dynasty }} · {{ poetry.author?.name || '佚名' }}
            </view>
          </view>
          <view class="poetry-content">{{ formatContent(poetry.content) }}</view>
          <view class="poetry-footer">
            <view class="stats">
              <text class="stat-item">👀 {{ poetry.read_count }}</text>
              <text class="stat-item">❤️ {{ poetry.like_count }}</text>
              <text class="stat-item">⭐ {{ poetry.collect_count }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 加载更多 -->
      <view v-if="hasMore && !loading" class="load-more" @click="loadMore">
        <text class="load-more-text">加载更多</text>
      </view>

      <view v-if="loading && poetryList.length > 0" class="loading-more">
        <text class="loading-text">加载中...</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { getPoetryList, getHotPoetryList, type Poetry, type PoetryListParams } from '@/api/poetry';

const themeStore = useThemeStore();

const poetryList = ref<Poetry[]>([]);
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);

const filters = ref({
  dynasty: '',
  type: '',
  sort_by: 'created_at',
  order: 'desc' as 'asc' | 'desc',
});

const dynastyList = ['先秦', '汉', '魏晋', '南北朝', '隋', '唐', '宋', '元', '明', '清'];

// 从 URL 获取参数
const getQueryParams = () => {
  const search = window.location.search;
  const params = new URLSearchParams(search);

  const type = params.get('type');
  const dynasty = params.get('dynasty');

  if (type) filters.value.type = type;
  if (dynasty) filters.value.dynasty = dynasty;
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

    const params: PoetryListParams = {
      page: page.value,
      size: 20,
      sort_by: filters.value.sort_by,
      order: filters.value.order,
    };

    if (filters.value.dynasty) {
      params.dynasty = filters.value.dynasty;
    }

    if (filters.value.type) {
      params.type = filters.value.type;
    }

    // 根据类型选择API
    const response = filters.value.type === 'hot'
      ? await getHotPoetryList(params)
      : await getPoetryList(params);

    const newPoetryList = response.data.list || [];

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
 * 筛选条件变化
 */
const handleFilterChange = () => {
  loadPoetryList(true);
};

/**
 * 加载更多
 */
const loadMore = () => {
  loadPoetryList(false);
};

/**
 * 格式化内容
 */
const formatContent = (content: string) => {
  if (!content) return '';
  return content.length > 80 ? content.substring(0, 80) + '...' : content;
};

/**
 * 跳转到详情
 */
const goToDetail = (id: number) => {
  window.location.href = `/poetry-detail?id=${id}`;
};

onMounted(() => {
  getQueryParams();
  loadPoetryList(true);
});
</script>

<style lang="scss" scoped>
.poetry-list-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 40px;
}

.container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.filter-bar {
  display: flex;
  gap: 12px;
  padding: 16px;
  margin-bottom: 20px;
  background-color: var(--bg-card);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);

  .filter-item {
    flex: 1;

    .filter-select {
      width: 100%;
      padding: 8px 12px;
      font-size: 14px;
      color: var(--text-primary);
      background-color: var(--bg-secondary);
      border: 1px solid var(--border-primary);
      border-radius: 8px;
      cursor: pointer;

      &:focus {
        outline: none;
        border-color: var(--color-primary);
      }
    }
  }
}

.loading-box,
.empty-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;

  .loading-text {
    font-size: 15px;
    color: var(--text-tertiary);
  }

  .empty-icon {
    font-size: 64px;
    margin-bottom: 16px;
  }

  .empty-text {
    font-size: 16px;
    color: var(--text-secondary);
  }
}

.poetry-list {
  .poetry-card {
    padding: 20px;
    margin-bottom: 16px;
    background-color: var(--bg-card);
    border-radius: 12px;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .poetry-header {
      margin-bottom: 12px;

      .poetry-title {
        font-size: 18px;
        font-weight: bold;
        color: var(--text-primary);
        margin-bottom: 6px;
      }

      .poetry-meta {
        font-size: 13px;
      }
    }

    .poetry-content {
      font-size: 14px;
      line-height: 1.8;
      color: var(--text-secondary);
      margin-bottom: 12px;
      white-space: pre-wrap;
    }

    .poetry-footer {
      .stats {
        display: flex;
        gap: 16px;

        .stat-item {
          font-size: 12px;
          color: var(--text-tertiary);
        }
      }
    }
  }
}

.load-more {
  padding: 16px;
  text-align: center;
  cursor: pointer;

  .load-more-text {
    font-size: 14px;
    color: var(--color-primary);

    &:hover {
      text-decoration: underline;
    }
  }
}

.loading-more {
  padding: 16px;
  text-align: center;

  .loading-text {
    font-size: 14px;
    color: var(--text-tertiary);
  }
}
</style>
