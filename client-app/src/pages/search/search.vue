<template>
  <view class="search-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 搜索框 -->
      <view class="search-bar theme-card">
        <input
          v-model="searchQuery"
          class="search-input"
          type="text"
          placeholder="搜索诗词、作者"
          @input="onSearchInput"
          @confirm="handleSearch"
        />
        <button v-if="searchQuery" class="clear-btn" @click="clearSearch">✕</button>
        <button class="search-btn" @click="handleSearch">搜索</button>
      </view>

      <!-- 搜索建议 -->
      <view v-if="showSuggestions && suggestions.length > 0" class="suggestions-box theme-card">
        <view
          v-for="(item, index) in suggestions"
          :key="index"
          class="suggestion-item"
          @click="selectSuggestion(item.text)"
        >
          <text class="suggestion-icon">{{ getSuggestionIcon(item.type) }}</text>
          <text class="suggestion-text">{{ item.text }}</text>
        </view>
      </view>

      <!-- 搜索历史 -->
      <view v-if="!searching && !hasSearched && searchHistory.length > 0" class="history-section">
        <view class="section-header">
          <text class="section-title">搜索历史</text>
          <text class="clear-history" @click="clearHistory">清空</text>
        </view>
        <view class="history-list">
          <view
            v-for="(item, index) in searchHistory"
            :key="index"
            class="history-item theme-card"
            @click="selectHistory(item)"
          >
            <text class="history-text">{{ item }}</text>
          </view>
        </view>
      </view>

      <!-- 搜索结果 -->
      <view v-if="hasSearched" class="results-section">
        <view class="results-header">
          <text class="results-count">找到 {{ total }} 条结果</text>
        </view>

        <view v-if="searching" class="loading-box">
          <text class="loading-text">搜索中...</text>
        </view>

        <view v-else-if="resultList.length === 0" class="empty-box">
          <text class="empty-icon">🔍</text>
          <text class="empty-text">没有找到相关结果</text>
          <text class="empty-hint">试试其他关键词吧</text>
        </view>

        <view v-else class="result-list">
          <view
            v-for="poetry in resultList"
            :key="poetry.id"
            class="result-item theme-card"
            @click="goToDetail(poetry.id)"
          >
            <view class="poetry-title">{{ poetry.title }}</view>
            <view class="poetry-author theme-text-tertiary">
              {{ poetry.dynasty }} · {{ poetry.author_name }}
            </view>
            <view class="poetry-content">{{ formatContent(poetry.content) }}</view>
            <view class="poetry-stats">
              <text class="stat-item">❤️ {{ poetry.likes_count }}</text>
              <text class="stat-item">⭐ {{ poetry.collects_count }}</text>
              <text class="stat-item">💬 {{ poetry.comments_count }}</text>
            </view>
          </view>
        </view>

        <!-- 加载更多 -->
        <view v-if="hasMore && !searching" class="load-more" @click="loadMore">
          <text class="load-more-text">加载更多</text>
        </view>
      </view>

      <!-- 热门搜索 -->
      <view v-if="!searching && !hasSearched" class="hot-section">
        <view class="section-title">🔥 热门搜索</view>
        <view class="hot-list">
          <view
            v-for="(item, index) in hotSearchList"
            :key="index"
            class="hot-item theme-card"
            @click="selectHistory(item)"
          >
            <text class="hot-rank">{{ index + 1 }}</text>
            <text class="hot-text">{{ item }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { searchPoetry, getSearchSuggestions, type SearchSuggestion } from '@/api/search';
import type { Poetry } from '@/api/poetry';

const themeStore = useThemeStore();

const searchQuery = ref('');
const searching = ref(false);
const hasSearched = ref(false);
const showSuggestions = ref(false);
const suggestions = ref<SearchSuggestion[]>([]);
const resultList = ref<Poetry[]>([]);
const total = ref(0);
const page = ref(1);
const hasMore = ref(true);

// 搜索历史
const searchHistory = ref<string[]>([]);
const hotSearchList = ['李白', '静夜思', '唐诗', '杜甫', '春晓', '登鹳雀楼'];

// 从本地存储加载搜索历史
const loadSearchHistory = () => {
  const history = localStorage.getItem('search_history');
  if (history) {
    searchHistory.value = JSON.parse(history);
  }
};

// 保存搜索历史
const saveSearchHistory = (query: string) => {
  if (!query.trim()) return;

  // 去重并添加到最前面
  const history = searchHistory.value.filter((item) => item !== query);
  history.unshift(query);

  // 最多保存10条
  searchHistory.value = history.slice(0, 10);

  // 保存到本地存储
  localStorage.setItem('search_history', JSON.stringify(searchHistory.value));
};

/**
 * 搜索输入
 */
const onSearchInput = async () => {
  if (!searchQuery.value.trim()) {
    showSuggestions.value = false;
    return;
  }

  // 获取搜索建议
  try {
    const response = await getSearchSuggestions(searchQuery.value);
    suggestions.value = response.data || [];
    showSuggestions.value = suggestions.value.length > 0;
  } catch (error) {
    console.error('获取搜索建议失败:', error);
  }
};

/**
 * 执行搜索
 */
const handleSearch = async (refresh = true) => {
  const query = searchQuery.value.trim();
  if (!query) return;

  try {
    searching.value = true;
    showSuggestions.value = false;

    if (refresh) {
      page.value = 1;
      resultList.value = [];
      hasMore.value = true;
    }

    const response = await searchPoetry({
      query,
      page: page.value,
      size: 20,
    });

    const newResults = response.data.items || [];

    if (refresh) {
      resultList.value = newResults;
      saveSearchHistory(query);
    } else {
      resultList.value.push(...newResults);
    }

    total.value = response.data.total || 0;
    hasMore.value = resultList.value.length < total.value;
    hasSearched.value = true;
    page.value++;
  } catch (error) {
    console.error('搜索失败:', error);
  } finally {
    searching.value = false;
  }
};

/**
 * 选择搜索建议
 */
const selectSuggestion = (text: string) => {
  searchQuery.value = text;
  handleSearch();
};

/**
 * 选择历史记录
 */
const selectHistory = (text: string) => {
  searchQuery.value = text;
  handleSearch();
};

/**
 * 清空搜索
 */
const clearSearch = () => {
  searchQuery.value = '';
  showSuggestions.value = false;
  hasSearched.value = false;
  resultList.value = [];
};

/**
 * 清空历史
 */
const clearHistory = () => {
  searchHistory.value = [];
  localStorage.removeItem('search_history');
};

/**
 * 加载更多
 */
const loadMore = () => {
  handleSearch(false);
};

/**
 * 获取建议图标
 */
const getSuggestionIcon = (type: string) => {
  switch (type) {
    case 'poetry':
      return '📖';
    case 'author':
      return '✍️';
    case 'tag':
      return '🏷️';
    default:
      return '🔍';
  }
};

/**
 * 格式化内容
 */
const formatContent = (content: string) => {
  if (!content) return '';
  return content.length > 60 ? content.substring(0, 60) + '...' : content;
};

/**
 * 跳转到详情
 */
const goToDetail = (id: number) => {
  window.location.href = `/pages/poetry-detail/poetry-detail?id=${id}`;
};

// 初始化
loadSearchHistory();
</script>

<style lang="scss" scoped>
.search-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 40px;
}

.container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.search-bar {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 20px;
  background-color: var(--bg-card);
  border-radius: 24px;
  box-shadow: var(--shadow-md);

  .search-input {
    flex: 1;
    padding: 0 12px;
    font-size: 15px;
    color: var(--text-primary);
    border: none;
    background: transparent;
    outline: none;
  }

  .clear-btn,
  .search-btn {
    padding: 6px 12px;
    margin-left: 8px;
    font-size: 14px;
    border: none;
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.3s;
  }

  .clear-btn {
    background: var(--bg-secondary);
    color: var(--text-tertiary);
  }

  .search-btn {
    background: var(--color-primary);
    color: white;

    &:hover {
      opacity: 0.9;
    }
  }
}

.suggestions-box {
  padding: 8px 0;
  margin-bottom: 20px;
  background-color: var(--bg-card);
  border-radius: 12px;
  box-shadow: var(--shadow-md);

  .suggestion-item {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      background-color: var(--bg-secondary);
    }

    .suggestion-icon {
      font-size: 18px;
      margin-right: 12px;
    }

    .suggestion-text {
      font-size: 15px;
      color: var(--text-primary);
    }
  }
}

.history-section,
.hot-section {
  margin-bottom: 24px;

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;

    .section-title {
      font-size: 16px;
      font-weight: bold;
      color: var(--text-primary);
    }

    .clear-history {
      font-size: 14px;
      color: var(--text-tertiary);
      cursor: pointer;

      &:hover {
        color: var(--text-primary);
      }
    }
  }

  .section-title {
    font-size: 16px;
    font-weight: bold;
    color: var(--text-primary);
    margin-bottom: 12px;
  }
}

.history-list,
.hot-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;

  .history-item,
  .hot-item {
    display: inline-flex;
    align-items: center;
    padding: 8px 16px;
    background-color: var(--bg-card);
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-sm);
    }

    .history-text,
    .hot-text {
      font-size: 14px;
      color: var(--text-secondary);
    }

    .hot-rank {
      display: inline-block;
      width: 20px;
      height: 20px;
      margin-right: 8px;
      font-size: 12px;
      font-weight: bold;
      color: white;
      background: var(--color-primary);
      border-radius: 50%;
      text-align: center;
      line-height: 20px;
    }
  }
}

.results-section {
  .results-header {
    margin-bottom: 16px;

    .results-count {
      font-size: 15px;
      color: var(--text-secondary);
    }
  }
}

.loading-box,
.empty-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
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
    margin-bottom: 8px;
  }

  .empty-hint {
    font-size: 14px;
    color: var(--text-tertiary);
  }
}

.result-list {
  .result-item {
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

    .poetry-title {
      font-size: 18px;
      font-weight: bold;
      color: var(--text-primary);
      margin-bottom: 8px;
    }

    .poetry-author {
      font-size: 13px;
      margin-bottom: 12px;
    }

    .poetry-content {
      font-size: 14px;
      line-height: 1.6;
      color: var(--text-secondary);
      margin-bottom: 12px;
    }

    .poetry-stats {
      display: flex;
      gap: 16px;

      .stat-item {
        font-size: 12px;
        color: var(--text-tertiary);
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
</style>
