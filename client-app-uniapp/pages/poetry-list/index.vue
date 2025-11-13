<template>
  <view class="poetry-list-page" :style="pageStyle">
    <!-- 顶部搜索栏 -->
    <view class="search-bar">
      <view class="search-input" @tap="goToSearch">
        <text class="search-icon">🔍</text>
        <text class="search-placeholder">搜索诗词、诗人...</text>
      </view>
      <view class="filter-btn" @tap="showFilterModal">
        <text class="icon">🎚️</text>
      </view>
    </view>

    <!-- 筛选标签 -->
    <scroll-view scroll-x class="filter-tags">
      <view class="tag-list">
        <view
          class="tag-item"
          :class="{ 'active': selectedDynasty === item.value }"
          v-for="item in dynastyOptions"
          :key="item.value"
          @tap="selectDynasty(item.value)"
        >
          {{ item.label }}
        </view>
      </view>
    </scroll-view>

    <!-- 诗词列表 -->
    <scroll-view
      scroll-y
      class="scroll-content"
      refresher-enabled
      :refresher-triggered="refreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="onLoadMore"
    >
      <!-- 加载状态 -->
      <loading-state v-if="loading && poetries.length === 0" text="加载中..." />

      <!-- 列表内容 -->
      <view v-else-if="poetries.length > 0" class="list-content">
        <poetry-card
          v-for="poetry in poetries"
          :key="poetry.id"
          :poetry="poetry"
          @tap="goToDetail(poetry.id)"
        />

        <!-- 加载更多 -->
        <view class="load-more" v-if="hasMore">
          <text v-if="loadingMore">加载中...</text>
          <text v-else>上拉加载更多</text>
        </view>

        <!-- 没有更多 -->
        <view class="no-more" v-else>
          <text>—— 没有更多了 ——</text>
        </view>
      </view>

      <!-- 空状态 -->
      <empty-state
        v-else
        icon="📚"
        text="暂无诗词"
        description="换个筛选条件试试"
        show-button
        button-text="重置筛选"
        @action="resetFilter"
      />
    </scroll-view>

    <!-- 筛选弹窗 -->
    <view class="filter-modal" v-if="showFilter" @tap="hideFilterModal">
      <view class="modal-content" @tap.stop>
        <view class="modal-header">
          <text class="modal-title">筛选条件</text>
          <text class="modal-close" @tap="hideFilterModal">×</text>
        </view>

        <scroll-view scroll-y class="modal-body">
          <!-- 朝代筛选 -->
          <view class="filter-group">
            <view class="group-title">朝代</view>
            <view class="options-grid">
              <view
                class="option-item"
                :class="{ 'active': tempDynasty === item.value }"
                v-for="item in allDynastyOptions"
                :key="item.value"
                @tap="tempDynasty = item.value"
              >
                {{ item.label }}
              </view>
            </view>
          </view>

          <!-- 类型筛选 -->
          <view class="filter-group">
            <view class="group-title">类型</view>
            <view class="options-grid">
              <view
                class="option-item"
                :class="{ 'active': tempType === item.value }"
                v-for="item in typeOptions"
                :key="item.value"
                @tap="tempType = item.value"
              >
                {{ item.label }}
              </view>
            </view>
          </view>

          <!-- 排序方式 -->
          <view class="filter-group">
            <view class="group-title">排序</view>
            <view class="options-grid">
              <view
                class="option-item"
                :class="{ 'active': tempSort === item.value }"
                v-for="item in sortOptions"
                :key="item.value"
                @tap="tempSort = item.value"
              >
                {{ item.label }}
              </view>
            </view>
          </view>
        </scroll-view>

        <view class="modal-footer">
          <button class="reset-btn" @tap="resetTempFilter">重置</button>
          <button class="confirm-btn" @tap="applyFilter">确定</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { usePoetryStore } from '@/stores/poetry'
import PoetryCard from '@/components/poetry-card/poetry-card.vue'
import LoadingState from '@/components/loading-state/loading-state.vue'
import EmptyState from '@/components/empty-state/empty-state.vue'

// Stores
const themeStore = useThemeStore()
const poetryStore = usePoetryStore()

// 数据
const poetries = ref([])
const loading = ref(false)
const refreshing = ref(false)
const loadingMore = ref(false)
const hasMore = ref(true)
const currentPage = ref(1)
const pageSize = 10

// 筛选条件
const selectedDynasty = ref('all')
const selectedType = ref('all')
const selectedSort = ref('latest')

// 筛选弹窗
const showFilter = ref(false)
const tempDynasty = ref('all')
const tempType = ref('all')
const tempSort = ref('latest')

// 页面样式
const pageStyle = computed(() => {
  const theme = themeStore.theme
  return {
    backgroundColor: theme.bgColor,
    color: theme.textColor
  }
})

// 朝代选项（顶部快捷筛选）
const dynastyOptions = [
  { label: '全部', value: 'all' },
  { label: '唐', value: '唐代' },
  { label: '宋', value: '宋代' },
  { label: '元', value: '元代' },
  { label: '明', value: '明代' },
  { label: '清', value: '清代' }
]

// 所有朝代选项（弹窗筛选）
const allDynastyOptions = [
  { label: '全部', value: 'all' },
  { label: '先秦', value: '先秦' },
  { label: '两汉', value: '两汉' },
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
  { label: '近现代', value: '近现代' }
]

// 类型选项
const typeOptions = [
  { label: '全部', value: 'all' },
  { label: '五言绝句', value: '五言绝句' },
  { label: '七言绝句', value: '七言绝句' },
  { label: '五言律诗', value: '五言律诗' },
  { label: '七言律诗', value: '七言律诗' },
  { label: '词', value: '词' },
  { label: '曲', value: '曲' }
]

// 排序选项
const sortOptions = [
  { label: '最新', value: 'latest' },
  { label: '最热', value: 'hot' },
  { label: '点赞最多', value: 'like' },
  { label: '收藏最多', value: 'collect' }
]

/**
 * 获取模拟诗词列表
 */
const getMockPoetries = () => {
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
    },
    {
      id: 3,
      title: '春晓',
      author: '孟浩然',
      dynasty: '唐代',
      content: '春眠不觉晓\n处处闻啼鸟\n夜来风雨声\n花落知多少',
      like_count: 8765,
      comment_count: 198,
      collect_count: 4321,
      read_count: 21000
    },
    {
      id: 4,
      title: '登鹳雀楼',
      author: '王之涣',
      dynasty: '唐代',
      content: '白日依山尽\n黄河入海流\n欲穷千里目\n更上一层楼',
      like_count: 7654,
      comment_count: 176,
      collect_count: 3987,
      read_count: 19800
    },
    {
      id: 5,
      title: '相思',
      author: '王维',
      dynasty: '唐代',
      content: '红豆生南国\n春来发几枝\n愿君多采撷\n此物最相思',
      like_count: 6543,
      comment_count: 154,
      collect_count: 3456,
      read_count: 17600
    },
    {
      id: 6,
      title: '水调歌头·明月几时有',
      author: '苏轼',
      dynasty: '宋代',
      content: '明月几时有\n把酒问青天\n不知天上宫阙\n今夕是何年',
      like_count: 10234,
      comment_count: 289,
      collect_count: 6789,
      read_count: 32100
    },
    {
      id: 7,
      title: '如梦令·昨夜雨疏风骤',
      author: '李清照',
      dynasty: '宋代',
      content: '昨夜雨疏风骤\n浓睡不消残酒\n试问卷帘人\n却道海棠依旧',
      like_count: 5432,
      comment_count: 132,
      collect_count: 2876,
      read_count: 15400
    },
    {
      id: 8,
      title: '赤壁赋',
      author: '苏轼',
      dynasty: '宋代',
      content: '壬戌之秋，七月既望\n苏子与客泛舟游于赤壁之下',
      like_count: 4321,
      comment_count: 98,
      collect_count: 2345,
      read_count: 12300
    }
  ]
}

/**
 * 加载诗词列表
 */
const loadPoetries = async (append = false) => {
  if (!append) {
    loading.value = true
  } else {
    loadingMore.value = true
  }

  try {
    // 构建查询参数
    const params = {
      page: currentPage.value,
      page_size: pageSize,
      dynasty: selectedDynasty.value !== 'all' ? selectedDynasty.value : undefined,
      poetry_type: selectedType.value !== 'all' ? selectedType.value : undefined,
      sort_by: selectedSort.value
    }

    // 尝试从 API 获取
    try {
      const data = await poetryStore.fetchPoetries(params)
      const newPoetries = data.items || []

      if (append) {
        poetries.value = [...poetries.value, ...newPoetries]
      } else {
        poetries.value = newPoetries
      }

      // 判断是否还有更多
      hasMore.value = newPoetries.length === pageSize

      console.log('从 API 加载诗词列表成功')
    } catch (apiError) {
      // API 失败时使用模拟数据
      console.warn('API 请求失败，使用模拟数据:', apiError)

      const mockData = getMockPoetries()

      // 根据朝代筛选
      let filteredData = mockData
      if (selectedDynasty.value !== 'all') {
        filteredData = mockData.filter(p => p.dynasty === selectedDynasty.value)
      }

      if (!append) {
        poetries.value = filteredData
        if (currentPage.value === 1) {
          uni.showToast({
            title: '演示模式（后端未连接）',
            icon: 'none',
            duration: 2000
          })
        }
      } else {
        // 模拟分页，没有更多数据
        hasMore.value = false
      }
    }
  } catch (e) {
    console.error('加载诗词列表失败:', e)
    if (!append) {
      poetries.value = getMockPoetries()
    }
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

/**
 * 下拉刷新
 */
const onRefresh = async () => {
  refreshing.value = true
  currentPage.value = 1
  hasMore.value = true
  await loadPoetries(false)
  refreshing.value = false
}

/**
 * 加载更多
 */
const onLoadMore = () => {
  if (hasMore.value && !loadingMore.value && !loading.value) {
    currentPage.value += 1
    loadPoetries(true)
  }
}

/**
 * 选择朝代
 */
const selectDynasty = (dynasty) => {
  selectedDynasty.value = dynasty
  currentPage.value = 1
  hasMore.value = true
  loadPoetries(false)
}

/**
 * 显示筛选弹窗
 */
const showFilterModal = () => {
  tempDynasty.value = selectedDynasty.value
  tempType.value = selectedType.value
  tempSort.value = selectedSort.value
  showFilter.value = true
}

/**
 * 隐藏筛选弹窗
 */
const hideFilterModal = () => {
  showFilter.value = false
}

/**
 * 重置临时筛选条件
 */
const resetTempFilter = () => {
  tempDynasty.value = 'all'
  tempType.value = 'all'
  tempSort.value = 'latest'
}

/**
 * 应用筛选
 */
const applyFilter = () => {
  selectedDynasty.value = tempDynasty.value
  selectedType.value = tempType.value
  selectedSort.value = tempSort.value

  currentPage.value = 1
  hasMore.value = true
  hideFilterModal()
  loadPoetries(false)
}

/**
 * 重置筛选
 */
const resetFilter = () => {
  selectedDynasty.value = 'all'
  selectedType.value = 'all'
  selectedSort.value = 'latest'
  currentPage.value = 1
  hasMore.value = true
  loadPoetries(false)
}

/**
 * 跳转到搜索页
 */
const goToSearch = () => {
  uni.navigateTo({
    url: '/pages/search/index'
  })
}

/**
 * 跳转到详情页
 */
const goToDetail = (id) => {
  uni.navigateTo({
    url: `/pages/poetry-detail/index?id=${id}`
  })
}

// 页面加载
onMounted(() => {
  console.log('诗词列表页加载')
  loadPoetries(false)
})
</script>

<style lang="scss" scoped>
.poetry-list-page {
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

.search-input {
  flex: 1;
  @include flex-align-center;
  padding: $spacing-md;
  background-color: $bg-secondary;
  border-radius: $border-radius-lg;
  margin-right: $spacing-md;

  .search-icon {
    font-size: 32rpx;
    margin-right: $spacing-sm;
  }

  .search-placeholder {
    font-size: $font-size-sm;
    color: $text-third;
  }
}

.filter-btn {
  @include flex-center;
  width: 72rpx;
  height: 72rpx;
  background-color: $primary-color;
  border-radius: $border-radius-lg;
  @include transition;

  &:active {
    transform: scale(0.95);
    opacity: 0.8;
  }

  .icon {
    font-size: 32rpx;
  }
}

// 筛选标签
.filter-tags {
  background-color: $card-bg;
  white-space: nowrap;
  border-bottom: 1rpx solid $border-color;
}

.tag-list {
  display: inline-flex;
  padding: $spacing-sm $spacing-lg;
}

.tag-item {
  display: inline-block;
  padding: $spacing-sm $spacing-lg;
  margin-right: $spacing-md;
  background-color: $bg-secondary;
  border-radius: $border-radius-lg;
  font-size: $font-size-sm;
  color: $text-secondary;
  white-space: nowrap;
  @include transition;

  &:active {
    transform: scale(0.95);
  }

  &.active {
    background-color: $primary-color;
    color: #FFFFFF;
  }
}

// 滚动内容
.scroll-content {
  height: calc(100vh - 200rpx);
}

.list-content {
  padding: $spacing-md;
}

// 加载状态
.load-more,
.no-more {
  @include flex-center;
  padding: $spacing-lg;
  font-size: $font-size-sm;
  color: $text-third;
}

// 筛选弹窗
.filter-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  @include flex-center;
  align-items: flex-end;
  z-index: 9999;
}

.modal-content {
  width: 100%;
  max-height: 80vh;
  background-color: $card-bg;
  border-radius: $border-radius-xl $border-radius-xl 0 0;
  overflow: hidden;
}

.modal-header {
  @include flex-between;
  padding: $spacing-lg;
  border-bottom: 1rpx solid $border-color;
}

.modal-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-color;
}

.modal-close {
  font-size: 48rpx;
  color: $text-third;
  line-height: 1;
  @include transition;

  &:active {
    color: $text-color;
  }
}

.modal-body {
  max-height: 60vh;
  padding: $spacing-lg;
}

.filter-group {
  margin-bottom: $spacing-xl;

  &:last-child {
    margin-bottom: 0;
  }
}

.group-title {
  font-size: $font-size-base;
  font-weight: bold;
  color: $text-color;
  margin-bottom: $spacing-md;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-md;
}

.option-item {
  @include flex-center;
  padding: $spacing-md;
  background-color: $bg-secondary;
  border-radius: $border-radius-lg;
  font-size: $font-size-sm;
  color: $text-secondary;
  @include transition;

  &:active {
    transform: scale(0.95);
  }

  &.active {
    background-color: $primary-color;
    color: #FFFFFF;
  }
}

.modal-footer {
  @include flex-between;
  padding: $spacing-md $spacing-lg;
  border-top: 1rpx solid $border-color;
}

.reset-btn,
.confirm-btn {
  @include reset-button;
  flex: 1;
  padding: $spacing-md;
  border-radius: $border-radius-lg;
  font-size: $font-size-base;
  font-weight: bold;
  @include transition;

  &:active {
    transform: scale(0.98);
    opacity: 0.8;
  }
}

.reset-btn {
  background-color: $bg-secondary;
  color: $text-color;
  margin-right: $spacing-md;
}

.confirm-btn {
  background-color: $button-primary;
  color: #FFFFFF;
}
</style>
