<template>
  <view class="index-page" :style="pageStyle">
    <!-- 顶部操作栏 -->
    <view class="top-bar">
      <view class="app-title">星语诗词</view>
      <view class="top-actions">
        <view class="action-btn" @tap="goToSearch">
          <text class="icon">🔍</text>
        </view>
        <view class="action-btn" @tap="goToTheme">
          <text class="icon">🎨</text>
        </view>
      </view>
    </view>

    <!-- 每日推荐诗词 -->
    <scroll-view
      scroll-y
      class="scroll-content"
      refresher-enabled
      :refresher-triggered="refreshing"
      @refresherrefresh="onRefresh"
    >
      <!-- 诗词展示卡片 -->
      <view class="daily-poetry" v-if="dailyPoetry">
        <view class="poetry-card-large">
          <view class="poetry-header">
            <text class="label">每日一诗</text>
            <view class="date">{{ currentDate }}</view>
          </view>

          <view class="poetry-title">{{ dailyPoetry.title }}</view>

          <view class="poetry-author">
            <text>{{ dailyPoetry.dynasty }} · {{ dailyPoetry.author }}</text>
          </view>

          <view class="poetry-content">
            <text class="content-line" v-for="(line, index) in poetryLines" :key="index">
              {{ line }}
            </text>
          </view>

          <!-- 互动按钮 -->
          <view class="action-buttons">
            <view class="action-item" @tap="handleLike">
              <text class="icon" :class="{ 'active': isLiked }">{{ isLiked ? '❤️' : '🤍' }}</text>
              <text class="count">{{ formatNumber(dailyPoetry.like_count) }}</text>
            </view>
            <view class="action-item" @tap="handleCollect">
              <text class="icon" :class="{ 'active': isCollected }">{{ isCollected ? '⭐' : '☆' }}</text>
              <text class="count">{{ formatNumber(dailyPoetry.collect_count) }}</text>
            </view>
            <view class="action-item" @tap="handleComment">
              <text class="icon">💬</text>
              <text class="count">{{ formatNumber(dailyPoetry.comment_count) }}</text>
            </view>
            <view class="action-item" @tap="handleShare">
              <text class="icon">📤</text>
              <text>分享</text>
            </view>
          </view>

          <button class="detail-btn" @tap="goToDetail">查看详情</button>
        </view>
      </view>

      <!-- 加载状态 -->
      <loading-state v-else-if="loading" text="加载中..." />

      <!-- 空状态 -->
      <empty-state
        v-else
        icon="📝"
        text="暂无推荐诗词"
        description="稍后再来看看吧"
        show-button
        button-text="刷新"
        @action="loadDailyPoetry"
      />

      <!-- 快捷入口 -->
      <view class="quick-entries">
        <view class="section-title">发现更多</view>
        <view class="entries-grid">
          <view class="entry-item" @tap="goToPoetryList">
            <text class="entry-icon">📚</text>
            <text class="entry-text">诗词库</text>
          </view>
          <view class="entry-item" @tap="goToAuthorList">
            <text class="entry-icon">✍️</text>
            <text class="entry-text">诗人</text>
          </view>
          <view class="entry-item" @tap="goToSquare">
            <text class="entry-icon">🌟</text>
            <text class="entry-text">广场</text>
          </view>
          <view class="entry-item" @tap="goToGame">
            <text class="entry-icon">🎮</text>
            <text class="entry-text">飞花令</text>
          </view>
        </view>
      </view>

      <!-- 推荐诗词列表 -->
      <view class="recommend-section">
        <view class="section-title">推荐诗词</view>
        <view v-if="recommendList.length > 0">
          <poetry-card
            v-for="poetry in recommendList"
            :key="poetry.id"
            :poetry="poetry"
            @tap="goToPoetryDetail(poetry.id)"
          />
        </view>
        <empty-state v-else icon="📖" text="暂无推荐" />
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { usePoetryStore } from '@/stores/poetry'
import { formatNumber, formatDate } from '@/utils'
import { getRandomPoetry, likePoetry, collectPoetry } from '@/api/poetry'
import PoetryCard from '@/components/poetry-card/poetry-card.vue'
import LoadingState from '@/components/loading-state/loading-state.vue'
import EmptyState from '@/components/empty-state/empty-state.vue'

// Stores
const themeStore = useThemeStore()
const poetryStore = usePoetryStore()

// 数据
const dailyPoetry = ref(null)
const recommendList = ref([])
const loading = ref(false)
const refreshing = ref(false)
const isLiked = ref(false)
const isCollected = ref(false)

// 页面样式（应用主题）
const pageStyle = computed(() => {
  const theme = themeStore.theme
  return {
    backgroundColor: theme.bgColor,
    color: theme.textColor
  }
})

// 当前日期
const currentDate = computed(() => {
  return formatDate(new Date(), 'YYYY年MM月DD日')
})

// 诗词内容分行
const poetryLines = computed(() => {
  if (!dailyPoetry.value) return []
  return dailyPoetry.value.content.split('\n').filter(line => line.trim())
})

/**
 * 加载每日诗词
 */
const loadDailyPoetry = async () => {
  try {
    loading.value = true
    dailyPoetry.value = await getRandomPoetry()
  } catch (e) {
    console.error('加载每日诗词失败:', e)
  } finally {
    loading.value = false
  }
}

/**
 * 加载推荐诗词
 */
const loadRecommendPoetries = async () => {
  try {
    const data = await poetryStore.fetchRecommendPoetries({ page: 1, page_size: 5 })
    recommendList.value = data.items || []
  } catch (e) {
    console.error('加载推荐诗词失败:', e)
  }
}

/**
 * 下拉刷新
 */
const onRefresh = async () => {
  refreshing.value = true
  await Promise.all([
    loadDailyPoetry(),
    loadRecommendPoetries()
  ])
  refreshing.value = false
}

/**
 * 点赞
 */
const handleLike = async () => {
  if (!dailyPoetry.value) return

  try {
    await likePoetry(dailyPoetry.value.id)
    isLiked.value = !isLiked.value
    dailyPoetry.value.like_count += isLiked.value ? 1 : -1
  } catch (e) {
    console.error('点赞失败:', e)
  }
}

/**
 * 收藏
 */
const handleCollect = async () => {
  if (!dailyPoetry.value) return

  try {
    await collectPoetry(dailyPoetry.value.id)
    isCollected.value = !isCollected.value
    dailyPoetry.value.collect_count += isCollected.value ? 1 : -1
    uni.showToast({
      title: isCollected.value ? '收藏成功' : '取消收藏',
      icon: 'none'
    })
  } catch (e) {
    console.error('收藏失败:', e)
  }
}

/**
 * 评论
 */
const handleComment = () => {
  if (!dailyPoetry.value) return
  goToDetail()
}

/**
 * 分享
 */
const handleShare = () => {
  uni.showShareMenu({
    title: `${dailyPoetry.value.title} - ${dailyPoetry.value.author}`,
    path: `/pages/poetry-detail/index?id=${dailyPoetry.value.id}`
  })
}

/**
 * 跳转到详情页
 */
const goToDetail = () => {
  if (!dailyPoetry.value) return
  uni.navigateTo({
    url: `/pages/poetry-detail/index?id=${dailyPoetry.value.id}`
  })
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
 * 跳转到搜索页
 */
const goToSearch = () => {
  uni.navigateTo({
    url: '/pages/search/index'
  })
}

/**
 * 跳转到主题设置
 */
const goToTheme = () => {
  uni.navigateTo({
    url: '/pages/theme/index'
  })
}

/**
 * 跳转到诗词列表
 */
const goToPoetryList = () => {
  uni.switchTab({
    url: '/pages/poetry-list/index'
  })
}

/**
 * 跳转到作者列表
 */
const goToAuthorList = () => {
  uni.navigateTo({
    url: '/pages/author-list/index'
  })
}

/**
 * 跳转到广场
 */
const goToSquare = () => {
  uni.switchTab({
    url: '/pages/square/index'
  })
}

/**
 * 跳转到飞花令游戏
 */
const goToGame = () => {
  uni.navigateTo({
    url: '/pages/game/index'
  })
}

// 页面加载
onMounted(() => {
  loadDailyPoetry()
  loadRecommendPoetries()
})
</script>

<style lang="scss" scoped>
.index-page {
  min-height: 100vh;
  @include transition(background-color);
}

.top-bar {
  @include flex-between;
  padding: $spacing-md $spacing-lg;
  background-color: $card-bg;
  @include card-shadow;
}

.app-title {
  font-size: $font-size-xl;
  font-weight: bold;
  color: $primary-color;
}

.top-actions {
  @include flex-align-center;
}

.action-btn {
  @include flex-center;
  width: 60rpx;
  height: 60rpx;
  margin-left: $spacing-sm;
  background-color: $bg-secondary;
  border-radius: $border-radius-circle;
  @include transition;

  &:active {
    transform: scale(0.9);
    background-color: $bg-third;
  }

  .icon {
    font-size: 32rpx;
  }
}

.scroll-content {
  height: calc(100vh - 100rpx);
  padding: $spacing-md;
}

.daily-poetry {
  margin-bottom: $spacing-lg;
}

.poetry-card-large {
  background: linear-gradient(135deg, $card-bg 0%, $bg-secondary 100%);
  border-radius: $border-radius-xl;
  padding: $spacing-xl;
  @include card-shadow;
}

.poetry-header {
  @include flex-between;
  margin-bottom: $spacing-lg;
}

.label {
  font-size: $font-size-sm;
  color: $primary-color;
  font-weight: bold;
  padding: 4rpx 12rpx;
  background-color: rgba($primary-color, 0.1);
  border-radius: $border-radius-sm;
}

.date {
  font-size: $font-size-xs;
  color: $text-third;
}

.poetry-title {
  font-size: $font-size-xxl;
  font-weight: bold;
  color: $text-color;
  text-align: center;
  margin-bottom: $spacing-md;
}

.poetry-author {
  font-size: $font-size-base;
  color: $text-secondary;
  text-align: center;
  margin-bottom: $spacing-xl;
}

.poetry-content {
  margin-bottom: $spacing-xl;
}

.content-line {
  display: block;
  font-size: $font-size-lg;
  color: $text-color;
  line-height: 2;
  text-align: center;
  margin-bottom: $spacing-sm;
}

.action-buttons {
  @include flex-between;
  padding: $spacing-md 0;
  border-top: 1rpx solid $border-color;
  border-bottom: 1rpx solid $border-color;
  margin-bottom: $spacing-md;
}

.action-item {
  @include flex-center;
  flex-direction: column;
  @include transition;

  &:active {
    transform: scale(0.95);
  }

  .icon {
    font-size: 40rpx;
    margin-bottom: 4rpx;
    @include transition;

    &.active {
      transform: scale(1.2);
    }
  }

  .count {
    font-size: $font-size-xs;
    color: $text-third;
  }
}

.detail-btn {
  @include reset-button;
  width: 100%;
  padding: $spacing-md;
  background-color: $button-primary;
  color: #FFFFFF;
  border-radius: $border-radius-lg;
  font-size: $font-size-base;
  font-weight: bold;
  @include transition;

  &:active {
    transform: scale(0.98);
    opacity: 0.8;
  }
}

.quick-entries {
  margin-bottom: $spacing-lg;
}

.section-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-color;
  margin-bottom: $spacing-md;
}

.entries-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-md;
}

.entry-item {
  @include flex-center;
  flex-direction: column;
  padding: $spacing-lg $spacing-sm;
  background-color: $card-bg;
  border-radius: $border-radius-lg;
  @include card-shadow;
  @include transition;

  &:active {
    transform: scale(0.95);
    @include hover-shadow;
  }

  .entry-icon {
    font-size: 48rpx;
    margin-bottom: $spacing-sm;
  }

  .entry-text {
    font-size: $font-size-sm;
    color: $text-secondary;
  }
}

.recommend-section {
  margin-bottom: $spacing-xl;
}
</style>
