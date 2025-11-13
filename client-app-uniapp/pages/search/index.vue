<template>
  <view class="search-page" :style="pageStyle">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <view class="search-input-wrapper">
        <text class="search-icon">🔍</text>
        <input
          class="search-input"
          v-model="keyword"
          placeholder="搜索诗词、诗人..."
          confirm-type="search"
          @confirm="handleSearch"
          :focus="autoFocus"
        />
        <view class="clear-btn" v-if="keyword" @tap="clearKeyword">
          <text>×</text>
        </view>
      </view>
      <view class="cancel-btn" @tap="goBack">
        <text>取消</text>
      </view>
    </view>

    <!-- 搜索建议 -->
    <scroll-view scroll-y class="scroll-content" v-if="!showResults">
      <!-- 搜索历史 -->
      <view class="section" v-if="searchHistory.length > 0">
        <view class="section-header">
          <text class="section-title">搜索历史</text>
          <view class="clear-history-btn" @tap="clearHistory">
            <text class="icon">🗑️</text>
            <text>清空</text>
          </view>
        </view>
        <view class="tags">
          <view
            class="tag-item"
            v-for="(item, index) in searchHistory"
            :key="index"
            @tap="searchByKeyword(item)"
          >
            {{ item }}
          </view>
        </view>
      </view>

      <!-- 热门搜索 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">热门搜索</text>
          <text class="section-icon">🔥</text>
        </view>
        <view class="hot-list">
          <view
            class="hot-item"
            v-for="(item, index) in hotSearches"
            :key="index"
            @tap="searchByKeyword(item.keyword)"
          >
            <view class="rank" :class="{ 'top': index < 3 }">{{ index + 1 }}</view>
            <text class="keyword">{{ item.keyword }}</text>
            <text class="count">{{ formatNumber(item.count) }}</text>
          </view>
        </view>
      </view>

      <!-- 推荐诗词 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">推荐诗词</text>
        </view>
        <view class="recommend-list">
          <poetry-card
            v-for="poetry in recommendPoetries"
            :key="poetry.id"
            :poetry="poetry"
            @tap="goToPoetryDetail(poetry.id)"
          />
        </view>
      </view>
    </scroll-view>

    <!-- 搜索结果 -->
    <view class="search-results" v-else>
      <!-- 结果标签页 -->
      <view class="result-tabs">
        <view
          class="tab-item"
          :class="{ 'active': resultTab === item.value }"
          v-for="item in resultTabs"
          :key="item.value"
          @tap="switchResultTab(item.value)"
        >
          {{ item.label }}
          <text class="count" v-if="item.count">({{ item.count }})</text>
        </view>
      </view>

      <!-- 结果列表 -->
      <scroll-view scroll-y class="result-list">
        <!-- 加载状态 -->
        <loading-state v-if="loading" text="搜索中..." />

        <!-- 诗词结果 -->
        <view v-else-if="resultTab === 'poetry'" class="results-content">
          <view v-if="poetryResults.length > 0">
            <poetry-card
              v-for="poetry in poetryResults"
              :key="poetry.id"
              :poetry="poetry"
              @tap="goToPoetryDetail(poetry.id)"
            />
          </view>
          <empty-state v-else icon="📖" text="未找到相关诗词" />
        </view>

        <!-- 作者结果 -->
        <view v-else-if="resultTab === 'author'" class="results-content">
          <view v-if="authorResults.length > 0" class="author-list">
            <view
              class="author-item"
              v-for="author in authorResults"
              :key="author.id"
              @tap="goToAuthorDetail(author.name)"
            >
              <view class="author-info">
                <text class="author-name">{{ author.name }}</text>
                <text class="author-meta">
                  {{ author.dynasty }} · {{ author.poetry_count }}首诗词
                </text>
                <text class="author-desc" v-if="author.description">
                  {{ author.description }}
                </text>
              </view>
              <text class="arrow">›</text>
            </view>
          </view>
          <empty-state v-else icon="✍️" text="未找到相关作者" />
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { formatNumber } from '@/utils'
import { searchPoetries, searchAuthors } from '@/api/poetry'
import PoetryCard from '@/components/poetry-card/poetry-card.vue'
import LoadingState from '@/components/loading-state/loading-state.vue'
import EmptyState from '@/components/empty-state/empty-state.vue'

// Stores
const themeStore = useThemeStore()

// 数据
const keyword = ref('')
const autoFocus = ref(true)
const showResults = ref(false)
const loading = ref(false)
const resultTab = ref('poetry')

// 搜索历史（从本地存储读取）
const searchHistory = ref([])

// 热门搜索
const hotSearches = ref([
  { keyword: '李白', count: 12580 },
  { keyword: '静夜思', count: 9876 },
  { keyword: '苏轼', count: 8765 },
  { keyword: '唐诗三百首', count: 7654 },
  { keyword: '宋词', count: 6543 },
  { keyword: '杜甫', count: 5432 },
  { keyword: '水调歌头', count: 4321 },
  { keyword: '望庐山瀑布', count: 3210 }
])

// 推荐诗词
const recommendPoetries = ref([])

// 搜索结果
const poetryResults = ref([])
const authorResults = ref([])

// 结果标签页
const resultTabs = computed(() => [
  { label: '诗词', value: 'poetry', count: poetryResults.value.length },
  { label: '作者', value: 'author', count: authorResults.value.length }
])

// 页面样式
const pageStyle = computed(() => {
  const theme = themeStore.theme
  return {
    backgroundColor: theme.bgColor,
    color: theme.textColor
  }
})

/**
 * 获取模拟推荐诗词
 */
const getMockRecommendPoetries = () => {
  return [
    {
      id: 1,
      title: '静夜思',
      author: '李白',
      dynasty: '唐代',
      content: '床前明月光\n疑是地上霜\n举头望明月\n低头思故乡',
      like_count: 12580,
      comment_count: 356,
      collect_count: 8964,
      read_count: 45230
    },
    {
      id: 2,
      title: '望庐山瀑布',
      author: '李白',
      dynasty: '唐代',
      content: '日照香炉生紫烟\n遥看瀑布挂前川\n飞流直下三千尺\n疑是银河落九天',
      like_count: 9876,
      comment_count: 234,
      collect_count: 5432,
      read_count: 28900
    }
  ]
}

/**
 * 获取模拟搜索结果
 */
const getMockSearchResults = (query) => {
  const mockPoetries = [
    {
      id: 1,
      title: '静夜思',
      author: '李白',
      dynasty: '唐代',
      content: '床前明月光\n疑是地上霜\n举头望明月\n低头思故乡',
      like_count: 12580,
      comment_count: 356
    },
    {
      id: 2,
      title: '望庐山瀑布',
      author: '李白',
      dynasty: '唐代',
      content: '日照香炉生紫烟\n遥看瀑布挂前川\n飞流直下三千尺\n疑是银河落九天',
      like_count: 9876,
      comment_count: 234
    }
  ]

  const mockAuthors = [
    {
      id: 1,
      name: '李白',
      dynasty: '唐代',
      poetry_count: 980,
      description: '唐代伟大的浪漫主义诗人，被后人誉为"诗仙"。'
    },
    {
      id: 2,
      name: '李清照',
      dynasty: '宋代',
      poetry_count: 45,
      description: '宋代女词人，婉约词派代表，有"千古第一才女"之称。'
    }
  ]

  return {
    poetries: mockPoetries.filter(p =>
      p.title.includes(query) || p.author.includes(query) || p.content.includes(query)
    ),
    authors: mockAuthors.filter(a => a.name.includes(query))
  }
}

/**
 * 加载推荐诗词
 */
const loadRecommendPoetries = async () => {
  try {
    // 尝试从 API 获取
    const data = await searchPoetries({ page: 1, page_size: 3 })
    recommendPoetries.value = data.items || []
  } catch (e) {
    console.warn('加载推荐诗词失败，使用模拟数据:', e)
    recommendPoetries.value = getMockRecommendPoetries()
  }
}

/**
 * 执行搜索
 */
const handleSearch = async () => {
  const query = keyword.value.trim()
  if (!query) return

  loading.value = true
  showResults.value = true

  try {
    // 尝试从 API 搜索
    try {
      const [poetryData, authorData] = await Promise.all([
        searchPoetries({ keyword: query }),
        searchAuthors({ keyword: query })
      ])

      poetryResults.value = poetryData.items || []
      authorResults.value = authorData.items || []

      console.log('从 API 搜索成功')
    } catch (apiError) {
      // API 失败时使用模拟数据
      console.warn('API 搜索失败，使用模拟数据:', apiError)

      const mockResults = getMockSearchResults(query)
      poetryResults.value = mockResults.poetries
      authorResults.value = mockResults.authors

      uni.showToast({
        title: '演示模式（后端未连接）',
        icon: 'none',
        duration: 2000
      })
    }

    // 保存到搜索历史
    addToHistory(query)
  } catch (e) {
    console.error('搜索失败:', e)
    const mockResults = getMockSearchResults(query)
    poetryResults.value = mockResults.poetries
    authorResults.value = mockResults.authors
  } finally {
    loading.value = false
  }
}

/**
 * 通过关键词搜索
 */
const searchByKeyword = (kw) => {
  keyword.value = kw
  handleSearch()
}

/**
 * 清空关键词
 */
const clearKeyword = () => {
  keyword.value = ''
  showResults.value = false
  autoFocus.value = true
}

/**
 * 切换结果标签页
 */
const switchResultTab = (tab) => {
  resultTab.value = tab
}

/**
 * 添加到搜索历史
 */
const addToHistory = (query) => {
  // 移除重复项
  const index = searchHistory.value.indexOf(query)
  if (index > -1) {
    searchHistory.value.splice(index, 1)
  }

  // 添加到开头
  searchHistory.value.unshift(query)

  // 限制历史记录数量
  if (searchHistory.value.length > 10) {
    searchHistory.value = searchHistory.value.slice(0, 10)
  }

  // 保存到本地存储
  uni.setStorageSync('searchHistory', searchHistory.value)
}

/**
 * 清空搜索历史
 */
const clearHistory = () => {
  uni.showModal({
    title: '提示',
    content: '确定清空搜索历史吗？',
    success: (res) => {
      if (res.confirm) {
        searchHistory.value = []
        uni.removeStorageSync('searchHistory')
        uni.showToast({
          title: '已清空',
          icon: 'success'
        })
      }
    }
  })
}

/**
 * 返回
 */
const goBack = () => {
  uni.navigateBack()
}

/**
 * 跳转到诗词详情
 */
const goToPoetryDetail = (id) => {
  uni.navigateTo({
    url: `/pages/poetry-detail/index?id=${id}`
  })
}

/**
 * 跳转到作者详情
 */
const goToAuthorDetail = (name) => {
  uni.navigateTo({
    url: `/pages/author-detail/index?name=${name}`
  })
}

// 页面加载
onMounted(() => {
  console.log('搜索页面加载')

  // 从本地存储读取搜索历史
  try {
    const history = uni.getStorageSync('searchHistory')
    if (history) {
      searchHistory.value = history
    }
  } catch (e) {
    console.warn('读取搜索历史失败:', e)
  }

  // 加载推荐诗词
  loadRecommendPoetries()
})
</script>

<style lang="scss" scoped>
.search-page {
  min-height: 100vh;
  @include transition(background-color);
}

// 搜索栏
.search-bar {
  @include flex-between;
  padding: $spacing-md $spacing-lg;
  background-color: $card-bg;
  @include card-shadow;
}

.search-input-wrapper {
  flex: 1;
  @include flex-align-center;
  padding: $spacing-md;
  background-color: $bg-secondary;
  border-radius: $border-radius-lg;
  margin-right: $spacing-md;
}

.search-icon {
  font-size: 32rpx;
  margin-right: $spacing-sm;
  color: $text-third;
}

.search-input {
  flex: 1;
  font-size: $font-size-base;
  color: $text-color;
}

.clear-btn {
  @include flex-center;
  width: 40rpx;
  height: 40rpx;
  border-radius: $border-radius-circle;
  background-color: $bg-third;
  font-size: 32rpx;
  color: $text-third;
  @include transition;

  &:active {
    opacity: 0.6;
  }
}

.cancel-btn {
  font-size: $font-size-base;
  color: $text-secondary;
  padding: $spacing-sm;
  @include transition;

  &:active {
    opacity: 0.6;
  }
}

// 滚动内容
.scroll-content {
  height: calc(100vh - 100rpx);
  padding: $spacing-md;
}

// 章节
.section {
  margin-bottom: $spacing-xl;
}

.section-header {
  @include flex-between;
  margin-bottom: $spacing-md;
}

.section-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-color;
}

.section-icon {
  font-size: 32rpx;
}

.clear-history-btn {
  @include flex-align-center;
  font-size: $font-size-sm;
  color: $text-third;
  @include transition;

  &:active {
    opacity: 0.6;
  }

  .icon {
    font-size: 24rpx;
    margin-right: 4rpx;
  }
}

// 标签
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-md;
}

.tag-item {
  padding: $spacing-sm $spacing-lg;
  background-color: $bg-secondary;
  color: $text-secondary;
  border-radius: $border-radius-lg;
  font-size: $font-size-sm;
  @include transition;

  &:active {
    transform: scale(0.95);
    background-color: $bg-third;
  }
}

// 热门列表
.hot-list {
  background-color: $card-bg;
  border-radius: $border-radius-lg;
  overflow: hidden;
}

.hot-item {
  @include flex-align-center;
  padding: $spacing-md $spacing-lg;
  border-bottom: 1rpx solid $border-color;
  @include transition;

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background-color: $bg-secondary;
  }
}

.rank {
  @include flex-center;
  width: 40rpx;
  height: 40rpx;
  margin-right: $spacing-md;
  font-size: $font-size-sm;
  font-weight: bold;
  color: $text-third;

  &.top {
    color: $error-color;
  }
}

.keyword {
  flex: 1;
  font-size: $font-size-base;
  color: $text-color;
}

.count {
  font-size: $font-size-xs;
  color: $text-third;
}

// 推荐列表
.recommend-list {
  // Poetry card styles handled by component
}

// 搜索结果
.search-results {
  height: calc(100vh - 100rpx);
}

.result-tabs {
  @include flex-align-center;
  padding: $spacing-md $spacing-lg;
  background-color: $card-bg;
  border-bottom: 1rpx solid $border-color;
}

.tab-item {
  padding: $spacing-sm $spacing-lg;
  margin-right: $spacing-md;
  font-size: $font-size-base;
  color: $text-secondary;
  @include transition;

  &.active {
    color: $primary-color;
    font-weight: bold;
    position: relative;

    &::after {
      content: '';
      position: absolute;
      bottom: -8rpx;
      left: 50%;
      transform: translateX(-50%);
      width: 40rpx;
      height: 4rpx;
      background-color: $primary-color;
      border-radius: 2rpx;
    }
  }

  .count {
    margin-left: 4rpx;
    font-size: $font-size-xs;
  }
}

.result-list {
  height: calc(100vh - 200rpx);
}

.results-content {
  padding: $spacing-md;
}

// 作者列表
.author-list {
  // Author items
}

.author-item {
  display: flex;
  align-items: center;
  padding: $spacing-lg;
  background-color: $card-bg;
  border-radius: $border-radius-lg;
  margin-bottom: $spacing-md;
  @include card-shadow;
  @include transition;

  &:active {
    transform: scale(0.99);
  }
}

.author-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.author-name {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 4rpx;
}

.author-meta {
  font-size: $font-size-sm;
  color: $text-third;
  margin-bottom: 4rpx;
}

.author-desc {
  font-size: $font-size-sm;
  color: $text-secondary;
  line-height: 1.6;
}

.arrow {
  font-size: 48rpx;
  color: $text-third;
}
</style>
