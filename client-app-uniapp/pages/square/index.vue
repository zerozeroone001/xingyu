<template>
  <view class="square-page" :style="pageStyle">
    <!-- 顶部导航 -->
    <view class="top-bar">
      <view class="nav-tabs">
        <view
          class="tab-item"
          :class="{ 'active': activeTab === item.value }"
          v-for="item in tabs"
          :key="item.value"
          @tap="switchTab(item.value)"
        >
          {{ item.label }}
        </view>
      </view>
      <view class="post-btn" @tap="goToCreatePost">
        <text class="icon">✏️</text>
      </view>
    </view>

    <!-- 内容列表 -->
    <scroll-view
      scroll-y
      class="scroll-content"
      refresher-enabled
      :refresher-triggered="refreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="onLoadMore"
    >
      <!-- 加载状态 -->
      <loading-state v-if="loading && posts.length === 0" text="加载中..." />

      <!-- 帖子列表 -->
      <view v-else-if="posts.length > 0" class="posts-list">
        <view
          class="post-item"
          v-for="post in posts"
          :key="post.id"
          @tap="goToPostDetail(post.id)"
        >
          <!-- 用户信息 -->
          <view class="post-header">
            <image
              class="avatar"
              :src="post.user.avatar || defaultAvatar"
              mode="aspectFill"
              @tap.stop="goToUserProfile(post.user.id)"
            />
            <view class="user-info">
              <text class="username">{{ post.user.nickname }}</text>
              <text class="post-time">{{ formatTime(post.created_at) }}</text>
            </view>
            <view class="more-btn" @tap.stop="showPostMenu(post)">
              <text>⋯</text>
            </view>
          </view>

          <!-- 帖子内容 -->
          <view class="post-content">
            <text class="post-text">{{ post.content }}</text>

            <!-- 图片网格 -->
            <view
              class="images-grid"
              :class="`grid-${Math.min((post.images && post.images.length) || 0, 9)}`"
              v-if="post.images && post.images.length > 0"
            >
              <image
                class="post-image"
                v-for="(img, index) in post.images.slice(0, 9)"
                :key="index"
                :src="img"
                mode="aspectFill"
                @tap.stop="previewImage(post.images, index)"
              />
            </view>

            <!-- 关联诗词 -->
            <view class="related-poetry" v-if="post.poetry" @tap.stop="goToPoetryDetail(post.poetry.id)">
              <view class="poetry-tag">📜 诗词</view>
              <view class="poetry-info">
                <text class="poetry-title">{{ post.poetry.title }}</text>
                <text class="poetry-author">{{ post.poetry.author }}</text>
              </view>
            </view>
          </view>

          <!-- 互动数据 -->
          <view class="post-actions">
            <view class="action-item" @tap.stop="handleLike(post)">
              <text class="icon" :class="{ 'active': post.is_liked }">
                {{ post.is_liked ? '❤️' : '🤍' }}
              </text>
              <text class="count">{{ formatNumber(post.like_count) }}</text>
            </view>
            <view class="action-item" @tap.stop="goToPostDetail(post.id)">
              <text class="icon">💬</text>
              <text class="count">{{ formatNumber(post.comment_count) }}</text>
            </view>
            <view class="action-item" @tap.stop="handleShare(post)">
              <text class="icon">📤</text>
              <text>分享</text>
            </view>
          </view>
        </view>

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
        icon="🌟"
        text="暂无内容"
        description="快来发布第一条动态吧"
        show-button
        button-text="发布动态"
        @action="goToCreatePost"
      />
    </scroll-view>

    <!-- 更多菜单 -->
    <view class="action-sheet" v-if="showMenu" @tap="hidePostMenu">
      <view class="sheet-content" @tap.stop>
        <view class="menu-item" @tap="handleReport">
          <text class="menu-icon">⚠️</text>
          <text class="menu-text">举报</text>
        </view>
        <view class="menu-divider"></view>
        <view class="menu-item cancel" @tap="hidePostMenu">
          <text class="menu-text">取消</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { formatNumber, formatTime } from '@/utils'
import { getPosts, likePost } from '@/api/square'
import LoadingState from '@/components/loading-state/loading-state.vue'
import EmptyState from '@/components/empty-state/empty-state.vue'

// Stores
const themeStore = useThemeStore()

// 数据
const posts = ref([])
const loading = ref(false)
const refreshing = ref(false)
const loadingMore = ref(false)
const hasMore = ref(true)
const currentPage = ref(1)
const pageSize = 10

// 标签页
const activeTab = ref('recommend')
const tabs = [
  { label: '推荐', value: 'recommend' },
  { label: '最新', value: 'latest' },
  { label: '热门', value: 'hot' }
]

// 菜单
const showMenu = ref(false)
const currentPost = ref(null)

// 默认头像
const defaultAvatar = '/static/images/default-avatar.png'

// 页面样式
const pageStyle = computed(() => {
  const theme = themeStore.theme
  return {
    backgroundColor: theme.bgColor,
    color: theme.textColor
  }
})

/**
 * 获取模拟帖子列表
 */
const getMockPosts = () => {
  return [
    {
      id: 1,
      user: {
        id: 101,
        nickname: '诗词爱好者',
        avatar: '/static/images/default-avatar.png'
      },
      content: '今天读到李白的《静夜思》，突然想起远方的家人。每次读这首诗都能感受到诗人浓浓的思乡之情。',
      images: [],
      poetry: {
        id: 1,
        title: '静夜思',
        author: '李白'
      },
      like_count: 128,
      comment_count: 23,
      is_liked: false,
      created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
    },
    {
      id: 2,
      user: {
        id: 102,
        nickname: '月下独酌',
        avatar: '/static/images/default-avatar.png'
      },
      content: '分享一下今天在公园拍的照片，突然想起苏轼的"竹外桃花三两枝，春江水暖鸭先知"，春天真的来了！',
      images: [
        '/static/images/default-avatar.png',
        '/static/images/default-avatar.png',
        '/static/images/default-avatar.png'
      ],
      poetry: null,
      like_count: 256,
      comment_count: 45,
      is_liked: false,
      created_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString()
    },
    {
      id: 3,
      user: {
        id: 103,
        nickname: '明月千里',
        avatar: '/static/images/default-avatar.png'
      },
      content: '今天尝试自己写了一首小诗，欢迎大家批评指正～',
      images: [],
      poetry: null,
      like_count: 89,
      comment_count: 12,
      is_liked: true,
      created_at: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString()
    },
    {
      id: 4,
      user: {
        id: 104,
        nickname: '清风徐来',
        avatar: '/static/images/default-avatar.png'
      },
      content: '参加了今天的飞花令比赛，虽然没有赢，但是收获很多！感谢各位诗友的指点。',
      images: [],
      poetry: null,
      like_count: 167,
      comment_count: 34,
      is_liked: false,
      created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
    }
  ]
}

/**
 * 加载帖子列表
 */
const loadPosts = async (append = false) => {
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
      type: activeTab.value
    }

    // 尝试从 API 获取
    try {
      const data = await getPosts(params)
      const newPosts = data.items || []

      if (append) {
        posts.value = [...posts.value, ...newPosts]
      } else {
        posts.value = newPosts
      }

      // 判断是否还有更多
      hasMore.value = newPosts.length === pageSize

      console.log('从 API 加载广场内容成功')
    } catch (apiError) {
      // API 失败时使用模拟数据
      console.warn('API 请求失败，使用模拟数据:', apiError)

      if (!append) {
        posts.value = getMockPosts()
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
    console.error('加载广场内容失败:', e)
    if (!append) {
      posts.value = getMockPosts()
    }
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

/**
 * 切换标签页
 */
const switchTab = (tab) => {
  if (activeTab.value === tab) return

  activeTab.value = tab
  currentPage.value = 1
  hasMore.value = true
  loadPosts(false)
}

/**
 * 下拉刷新
 */
const onRefresh = async () => {
  refreshing.value = true
  currentPage.value = 1
  hasMore.value = true
  await loadPosts(false)
  refreshing.value = false
}

/**
 * 加载更多
 */
const onLoadMore = () => {
  if (hasMore.value && !loadingMore.value && !loading.value) {
    currentPage.value += 1
    loadPosts(true)
  }
}

/**
 * 点赞
 */
const handleLike = async (post) => {
  try {
    await likePost(post.id)
    post.is_liked = !post.is_liked
    post.like_count += post.is_liked ? 1 : -1
  } catch (e) {
    console.warn('点赞失败（演示模式）:', e)
    // 演示模式：直接修改数据
    post.is_liked = !post.is_liked
    post.like_count += post.is_liked ? 1 : -1
  }
}

/**
 * 分享
 */
const handleShare = (post) => {
  uni.showShareMenu({
    title: post.content.slice(0, 30) + '...',
    path: `/pages/post-detail/index?id=${post.id}`
  })
}

/**
 * 预览图片
 */
const previewImage = (images, current) => {
  uni.previewImage({
    urls: images,
    current: current
  })
}

/**
 * 显示帖子菜单
 */
const showPostMenu = (post) => {
  currentPost.value = post
  showMenu.value = true
}

/**
 * 隐藏帖子菜单
 */
const hidePostMenu = () => {
  showMenu.value = false
  currentPost.value = null
}

/**
 * 举报
 */
const handleReport = () => {
  uni.showToast({
    title: '举报功能开发中',
    icon: 'none'
  })
  hidePostMenu()
}

/**
 * 跳转到发布页
 */
const goToCreatePost = () => {
  uni.navigateTo({
    url: '/pages/create-post/index'
  })
}

/**
 * 跳转到帖子详情
 */
const goToPostDetail = (id) => {
  uni.navigateTo({
    url: `/pages/post-detail/index?id=${id}`
  })
}

/**
 * 跳转到用户主页
 */
const goToUserProfile = (userId) => {
  uni.navigateTo({
    url: `/pages/user-profile/index?id=${userId}`
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

// 页面加载
onMounted(() => {
  console.log('广场页面加载')
  loadPosts(false)
})
</script>

<style lang="scss" scoped>
.square-page {
  min-height: 100vh;
  @include transition(background-color);
}

// 顶部导航
.top-bar {
  @include flex-between;
  padding: $spacing-md $spacing-lg;
  background-color: $card-bg;
  @include card-shadow;
}

.nav-tabs {
  @include flex-align-center;
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
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 40rpx;
      height: 4rpx;
      background-color: $primary-color;
      border-radius: 2rpx;
    }
  }
}

.post-btn {
  @include flex-center;
  width: 64rpx;
  height: 64rpx;
  background-color: $primary-color;
  border-radius: $border-radius-circle;
  @include transition;

  &:active {
    transform: scale(0.95);
    opacity: 0.8;
  }

  .icon {
    font-size: 32rpx;
  }
}

// 滚动内容
.scroll-content {
  height: calc(100vh - 100rpx);
  background-color: $bg-secondary;
}

.posts-list {
  padding: $spacing-md;
}

// 帖子卡片
.post-item {
  background-color: $card-bg;
  border-radius: $border-radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-md;
  @include card-shadow;
  @include transition;

  &:active {
    transform: scale(0.99);
  }
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: $spacing-md;
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: $border-radius-circle;
  margin-right: $spacing-md;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.username {
  font-size: $font-size-base;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 4rpx;
}

.post-time {
  font-size: $font-size-xs;
  color: $text-third;
}

.more-btn {
  padding: $spacing-sm;
  font-size: 36rpx;
  color: $text-third;
  @include transition;

  &:active {
    opacity: 0.6;
  }
}

// 帖子内容
.post-content {
  margin-bottom: $spacing-md;
}

.post-text {
  display: block;
  font-size: $font-size-base;
  color: $text-color;
  line-height: 1.6;
  margin-bottom: $spacing-md;
}

// 图片网格
.images-grid {
  display: grid;
  gap: $spacing-sm;
  margin-bottom: $spacing-md;

  &.grid-1 {
    grid-template-columns: 1fr;

    .post-image {
      height: 400rpx;
    }
  }

  &.grid-2,
  &.grid-4 {
    grid-template-columns: repeat(2, 1fr);

    .post-image {
      height: 200rpx;
    }
  }

  &.grid-3,
  &.grid-5,
  &.grid-6,
  &.grid-7,
  &.grid-8,
  &.grid-9 {
    grid-template-columns: repeat(3, 1fr);

    .post-image {
      height: 200rpx;
    }
  }
}

.post-image {
  width: 100%;
  border-radius: $border-radius-sm;
  background-color: $bg-secondary;
}

// 关联诗词
.related-poetry {
  @include flex-align-center;
  padding: $spacing-md;
  background-color: $bg-secondary;
  border-radius: $border-radius-lg;
  border-left: 4rpx solid $primary-color;
  @include transition;

  &:active {
    opacity: 0.8;
  }
}

.poetry-tag {
  padding: 4rpx 12rpx;
  background-color: rgba($primary-color, 0.1);
  color: $primary-color;
  font-size: $font-size-xs;
  border-radius: $border-radius-sm;
  margin-right: $spacing-md;
}

.poetry-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.poetry-title {
  font-size: $font-size-sm;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 4rpx;
}

.poetry-author {
  font-size: $font-size-xs;
  color: $text-third;
}

// 互动操作
.post-actions {
  @include flex-between;
  padding-top: $spacing-md;
  border-top: 1rpx solid $border-color;
}

.action-item {
  @include flex-align-center;
  font-size: $font-size-sm;
  color: $text-third;
  @include transition;

  &:active {
    transform: scale(0.95);
  }

  .icon {
    font-size: 32rpx;
    margin-right: 4rpx;
    @include transition;

    &.active {
      transform: scale(1.2);
    }
  }

  .count {
    margin-left: 4rpx;
  }
}

// 加载状态
.load-more,
.no-more {
  @include flex-center;
  padding: $spacing-lg;
  font-size: $font-size-sm;
  color: $text-third;
}

// 操作菜单
.action-sheet {
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

.sheet-content {
  width: 100%;
  background-color: $card-bg;
  border-radius: $border-radius-xl $border-radius-xl 0 0;
  overflow: hidden;
}

.menu-item {
  @include flex-center;
  padding: $spacing-lg;
  @include transition;

  &:active {
    background-color: $bg-secondary;
  }

  &.cancel {
    color: $text-third;
  }
}

.menu-icon {
  font-size: 32rpx;
  margin-right: $spacing-sm;
}

.menu-text {
  font-size: $font-size-base;
  color: $text-color;
}

.menu-divider {
  height: 1rpx;
  background-color: $border-color;
  margin: 0 $spacing-lg;
}
</style>
