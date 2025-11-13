<template>
  <view class="poetry-detail-page" :style="pageStyle">
    <!-- 自定义导航栏 -->
    <view class="custom-navbar" :style="navbarStyle">
      <view class="navbar-content">
        <view class="nav-back" @tap="goBack">
          <text class="icon">←</text>
        </view>
        <view class="nav-title">诗词详情</view>
        <view class="nav-actions">
          <view class="nav-btn" @tap="handleShare">
            <text class="icon">📤</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 滚动内容区域 -->
    <scroll-view scroll-y class="scroll-content" @scroll="onScroll">
      <!-- 加载状态 -->
      <loading-state v-if="loading" text="加载中..." />

      <!-- 诗词内容 -->
      <view v-else-if="poetry" class="detail-content">
        <!-- 诗词头部 -->
        <view class="poetry-header-section">
          <view class="poetry-card">
            <view class="poetry-title">{{ poetry.title }}</view>

            <view class="poetry-meta">
              <text class="dynasty">{{ poetry.dynasty }}</text>
              <text class="separator">·</text>
              <text class="author" @tap="goToAuthor">{{ poetry.author }}</text>
            </view>

            <!-- 诗词正文 -->
            <view class="poetry-content">
              <text
                class="content-line"
                v-for="(line, index) in poetryLines"
                :key="index"
              >
                {{ line }}
              </text>
            </view>

            <!-- 标签 -->
            <view class="tags" v-if="poetry.tags && poetry.tags.length > 0">
              <text
                class="tag"
                v-for="(tag, index) in poetry.tags"
                :key="index"
              >
                #{{ tag }}
              </text>
            </view>

            <!-- 互动数据 -->
            <view class="stats">
              <view class="stat-item">
                <text class="stat-icon">👁️</text>
                <text class="stat-value">{{ formatNumber(poetry.read_count) }}</text>
              </view>
              <view class="stat-item">
                <text class="stat-icon">❤️</text>
                <text class="stat-value">{{ formatNumber(poetry.like_count) }}</text>
              </view>
              <view class="stat-item">
                <text class="stat-icon">⭐</text>
                <text class="stat-value">{{ formatNumber(poetry.collect_count) }}</text>
              </view>
              <view class="stat-item">
                <text class="stat-icon">💬</text>
                <text class="stat-value">{{ formatNumber(poetry.comment_count) }}</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 译文 -->
        <view class="section" v-if="poetry.translation">
          <view class="section-header">
            <text class="section-icon">📖</text>
            <text class="section-title">译文</text>
          </view>
          <view class="section-content">
            <text class="translation-text">{{ poetry.translation }}</text>
          </view>
        </view>

        <!-- 赏析 -->
        <view class="section" v-if="poetry.appreciation">
          <view class="section-header">
            <text class="section-icon">💡</text>
            <text class="section-title">赏析</text>
          </view>
          <view class="section-content">
            <text class="appreciation-text">{{ poetry.appreciation }}</text>
          </view>
        </view>

        <!-- 注释 -->
        <view class="section" v-if="poetry.annotations && poetry.annotations.length > 0">
          <view class="section-header">
            <text class="section-icon">📝</text>
            <text class="section-title">注释</text>
          </view>
          <view class="section-content">
            <view
              class="annotation-item"
              v-for="(item, index) in poetry.annotations"
              :key="index"
            >
              <text class="annotation-term">{{ item.term }}：</text>
              <text class="annotation-explain">{{ item.explain }}</text>
            </view>
          </view>
        </view>

        <!-- 评论区 -->
        <view class="section comments-section">
          <view class="section-header">
            <text class="section-icon">💬</text>
            <text class="section-title">评论 ({{ comments.length }})</text>
          </view>

          <!-- 评论列表 -->
          <view class="comments-list" v-if="comments.length > 0">
            <view
              class="comment-item"
              v-for="comment in comments"
              :key="comment.id"
            >
              <image
                class="comment-avatar"
                :src="comment.user.avatar || defaultAvatar"
                mode="aspectFill"
              />
              <view class="comment-content">
                <view class="comment-header">
                  <text class="comment-username">{{ comment.user.nickname }}</text>
                  <text class="comment-time">{{ formatTime(comment.created_at) }}</text>
                </view>
                <text class="comment-text">{{ comment.content }}</text>

                <!-- 回复按钮 -->
                <view class="comment-actions">
                  <view class="action-btn" @tap="handleReply(comment)">
                    <text class="icon">↩️</text>
                    <text>回复</text>
                  </view>
                  <view
                    class="action-btn"
                    :class="{ 'active': comment.is_liked }"
                    @tap="handleCommentLike(comment)"
                  >
                    <text class="icon">{{ comment.is_liked ? '❤️' : '🤍' }}</text>
                    <text>{{ comment.like_count || 0 }}</text>
                  </view>
                </view>

                <!-- 二级评论 -->
                <view
                  class="reply-list"
                  v-if="comment.replies && comment.replies.length > 0"
                >
                  <view
                    class="reply-item"
                    v-for="reply in comment.replies"
                    :key="reply.id"
                  >
                    <text class="reply-username">{{ reply.user.nickname }}：</text>
                    <text class="reply-text">{{ reply.content }}</text>
                  </view>
                </view>
              </view>
            </view>
          </view>

          <!-- 空状态 -->
          <empty-state
            v-else
            icon="💬"
            text="暂无评论"
            description="快来发表第一条评论吧"
          />
        </view>
      </view>

      <!-- 空状态（未找到诗词） -->
      <empty-state
        v-else
        icon="📖"
        text="诗词不存在"
        description="该诗词可能已被删除"
        show-button
        button-text="返回"
        @action="goBack"
      />
    </scroll-view>

    <!-- 底部操作栏 -->
    <view class="bottom-bar" :style="bottomBarStyle" v-if="poetry">
      <view class="action-group">
        <view class="action-btn" :class="{ 'active': isLiked }" @tap="handleLike">
          <text class="icon">{{ isLiked ? '❤️' : '🤍' }}</text>
          <text class="text">{{ isLiked ? '已赞' : '点赞' }}</text>
        </view>
        <view class="action-btn" :class="{ 'active': isCollected }" @tap="handleCollect">
          <text class="icon">{{ isCollected ? '⭐' : '☆' }}</text>
          <text class="text">{{ isCollected ? '已藏' : '收藏' }}</text>
        </view>
      </view>

      <view class="comment-input" @tap="showCommentInput">
        <text class="placeholder">说说你的看法...</text>
      </view>
    </view>

    <!-- 评论输入弹窗 -->
    <view class="comment-modal" v-if="showComment" @tap="hideCommentInput">
      <view class="modal-content" @tap.stop>
        <view class="modal-header">
          <text class="modal-title">{{ replyTo ? '回复评论' : '发表评论' }}</text>
          <text class="modal-close" @tap="hideCommentInput">×</text>
        </view>
        <textarea
          class="comment-textarea"
          v-model="commentText"
          placeholder="说说你的看法..."
          :focus="showComment"
          maxlength="500"
        />
        <view class="modal-footer">
          <text class="char-count">{{ commentText.length }}/500</text>
          <button class="submit-btn" @tap="submitComment">发送</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { formatNumber, formatTime } from '@/utils'
import { getPoetryDetail, likePoetry, collectPoetry } from '@/api/poetry'
import { getPoetryComments, createComment, likeComment } from '@/api/comment'
import LoadingState from '@/components/loading-state/loading-state.vue'
import EmptyState from '@/components/empty-state/empty-state.vue'

// Stores
const themeStore = useThemeStore()

// 路由参数
const poetryId = ref(null)

// 数据
const poetry = ref(null)
const comments = ref([])
const loading = ref(true)
const isLiked = ref(false)
const isCollected = ref(false)
const scrollTop = ref(0)

// 评论相关
const showComment = ref(false)
const commentText = ref('')
const replyTo = ref(null)

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

// 导航栏样式
const navbarStyle = computed(() => {
  const theme = themeStore.theme
  const opacity = Math.min(scrollTop.value / 200, 1)
  return {
    backgroundColor: `rgba(${hexToRgb(theme.cardBg)}, ${opacity})`,
    backdropFilter: opacity > 0.5 ? 'blur(10px)' : 'none'
  }
})

// 底部栏样式
const bottomBarStyle = computed(() => {
  const theme = themeStore.theme
  return {
    backgroundColor: theme.cardBg,
    borderTopColor: theme.borderColor
  }
})

// 诗词内容分行
const poetryLines = computed(() => {
  if (!poetry.value) return []
  return poetry.value.content.split('\n').filter(line => line.trim())
})

/**
 * 获取模拟诗词数据
 */
const getMockPoetry = (id) => {
  return {
    id: id || 1,
    title: '静夜思',
    author: '李白',
    dynasty: '唐代',
    poetry_type: '五言绝句',
    content: '床前明月光\n疑是地上霜\n举头望明月\n低头思故乡',
    tags: ['思乡', '月亮', '经典'],
    like_count: 12580,
    comment_count: 356,
    collect_count: 8964,
    read_count: 45230,
    translation: '明亮的月光洒在床前的窗户纸上，好像地上泛起了一层霜。我禁不住抬起头来，看那天窗外空中的一轮明月，不由得低头沉思，想起远方的家乡。',
    appreciation: '这首诗写的是在寂静的月夜思念家乡的感受。诗的前两句，是写诗人在作客他乡的特定环境中一刹那间所产生的错觉。一个独处他乡的人，白天奔波忙碌，倒还能冲淡离愁，然而一到夜深人静的时候，心头就难免泛起阵阵思念故乡的波澜。',
    annotations: [
      { term: '床', explain: '井栏' },
      { term: '地上霜', explain: '指月光的颜色如霜' },
      { term: '举头', explain: '抬头' },
      { term: '思故乡', explain: '思念故乡' }
    ]
  }
}

/**
 * 获取模拟评论数据
 */
const getMockComments = () => {
  return [
    {
      id: 1,
      user: {
        id: 101,
        nickname: '诗词爱好者',
        avatar: '/static/images/default-avatar.png'
      },
      content: '李白的诗总是这么意境深远，读来让人感同身受。',
      like_count: 23,
      is_liked: false,
      created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
      replies: [
        {
          id: 11,
          user: {
            id: 102,
            nickname: '月下独酌',
            avatar: '/static/images/default-avatar.png'
          },
          content: '确实，李白的诗豪放飘逸，这首静夜思却格外宁静深沉。',
          created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString()
        }
      ]
    },
    {
      id: 2,
      user: {
        id: 103,
        nickname: '明月千里',
        avatar: '/static/images/default-avatar.png'
      },
      content: '每次读这首诗都会想起家乡的明月，游子之心溢于言表。',
      like_count: 15,
      is_liked: false,
      created_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
      replies: []
    }
  ]
}

/**
 * 加载诗词详情
 */
const loadPoetryDetail = async () => {
  try {
    loading.value = true

    // 尝试从 API 获取
    try {
      const data = await getPoetryDetail(poetryId.value)
      poetry.value = data
      console.log('从 API 加载诗词详情成功')
    } catch (apiError) {
      // API 失败时使用模拟数据
      console.warn('API 请求失败，使用模拟数据:', apiError)
      poetry.value = getMockPoetry(poetryId.value)

      uni.showToast({
        title: '演示模式（后端未连接）',
        icon: 'none',
        duration: 2000
      })
    }
  } catch (e) {
    console.error('加载诗词详情失败:', e)
    poetry.value = getMockPoetry(poetryId.value)
  } finally {
    loading.value = false
  }
}

/**
 * 加载评论列表
 */
const loadComments = async () => {
  try {
    const data = await getPoetryComments(poetryId.value, { page: 1, page_size: 20 })
    comments.value = data.items || []
  } catch (e) {
    console.warn('加载评论失败，使用模拟数据:', e)
    comments.value = getMockComments()
  }
}

/**
 * 滚动事件
 */
const onScroll = (e) => {
  scrollTop.value = e.detail.scrollTop
}

/**
 * 返回
 */
const goBack = () => {
  uni.navigateBack()
}

/**
 * 跳转到作者详情
 */
const goToAuthor = () => {
  if (!poetry.value) return
  uni.navigateTo({
    url: `/pages/author-detail/index?name=${poetry.value.author}`
  })
}

/**
 * 点赞
 */
const handleLike = async () => {
  if (!poetry.value) return

  try {
    await likePoetry(poetry.value.id)
    isLiked.value = !isLiked.value
    poetry.value.like_count += isLiked.value ? 1 : -1

    uni.showToast({
      title: isLiked.value ? '点赞成功' : '取消点赞',
      icon: 'none',
      duration: 1000
    })
  } catch (e) {
    console.warn('点赞失败（演示模式）:', e)
    // 演示模式：直接修改数据
    isLiked.value = !isLiked.value
    poetry.value.like_count += isLiked.value ? 1 : -1
  }
}

/**
 * 收藏
 */
const handleCollect = async () => {
  if (!poetry.value) return

  try {
    await collectPoetry(poetry.value.id)
    isCollected.value = !isCollected.value
    poetry.value.collect_count += isCollected.value ? 1 : -1

    uni.showToast({
      title: isCollected.value ? '收藏成功' : '取消收藏',
      icon: 'none',
      duration: 1000
    })
  } catch (e) {
    console.warn('收藏失败（演示模式）:', e)
    // 演示模式：直接修改数据
    isCollected.value = !isCollected.value
    poetry.value.collect_count += isCollected.value ? 1 : -1
  }
}

/**
 * 分享
 */
const handleShare = () => {
  uni.showShareMenu({
    title: poetry.value?.title || '诗词分享',
    path: `/pages/poetry-detail/index?id=${poetryId.value}`
  })
}

/**
 * 显示评论输入框
 */
const showCommentInput = () => {
  showComment.value = true
  replyTo.value = null
  commentText.value = ''
}

/**
 * 隐藏评论输入框
 */
const hideCommentInput = () => {
  showComment.value = false
  replyTo.value = null
  commentText.value = ''
}

/**
 * 回复评论
 */
const handleReply = (comment) => {
  replyTo.value = comment
  showComment.value = true
  commentText.value = ''
}

/**
 * 提交评论
 */
const submitComment = async () => {
  if (!commentText.value.trim()) {
    uni.showToast({
      title: '请输入评论内容',
      icon: 'none'
    })
    return
  }

  try {
    const params = {
      poetry_id: poetryId.value,
      content: commentText.value,
      parent_id: replyTo.value?.id || null
    }

    await createComment(params)

    uni.showToast({
      title: '评论成功',
      icon: 'success'
    })

    // 重新加载评论
    await loadComments()
    hideCommentInput()
  } catch (e) {
    console.warn('评论失败（演示模式）:', e)

    // 演示模式：模拟添加评论
    const newComment = {
      id: Date.now(),
      user: {
        id: 999,
        nickname: '当前用户',
        avatar: '/static/images/default-avatar.png'
      },
      content: commentText.value,
      like_count: 0,
      is_liked: false,
      created_at: new Date().toISOString(),
      replies: []
    }

    if (replyTo.value) {
      // 添加到回复列表
      const parentComment = comments.value.find(c => c.id === replyTo.value.id)
      if (parentComment) {
        if (!parentComment.replies) {
          parentComment.replies = []
        }
        parentComment.replies.push(newComment)
      }
    } else {
      // 添加为一级评论
      comments.value.unshift(newComment)
    }

    poetry.value.comment_count += 1
    hideCommentInput()

    uni.showToast({
      title: '评论成功（演示）',
      icon: 'none'
    })
  }
}

/**
 * 点赞评论
 */
const handleCommentLike = async (comment) => {
  try {
    await likeComment(comment.id)
    comment.is_liked = !comment.is_liked
    comment.like_count += comment.is_liked ? 1 : -1
  } catch (e) {
    console.warn('点赞评论失败（演示模式）:', e)
    // 演示模式：直接修改数据
    comment.is_liked = !comment.is_liked
    comment.like_count = (comment.like_count || 0) + (comment.is_liked ? 1 : -1)
  }
}

/**
 * 16进制颜色转 RGB
 */
const hexToRgb = (hex) => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result
    ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}`
    : '255, 255, 255'
}

// 页面加载
onMounted(() => {
  // 获取路由参数
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  poetryId.value = currentPage.options.id || 1

  console.log('诗词详情页加载, ID:', poetryId.value)

  loadPoetryDetail()
  loadComments()
})
</script>

<style lang="scss" scoped>
.poetry-detail-page {
  min-height: 100vh;
  @include transition(background-color);
}

// 导航栏
.custom-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  @include transition(background-color);
}

.navbar-content {
  @include flex-between;
  padding: $spacing-md $spacing-lg;
  height: 88rpx;
}

.nav-back,
.nav-btn {
  @include flex-center;
  width: 60rpx;
  height: 60rpx;
  border-radius: $border-radius-circle;
  @include transition;

  &:active {
    transform: scale(0.9);
    background-color: rgba(0, 0, 0, 0.05);
  }

  .icon {
    font-size: 32rpx;
  }
}

.nav-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-color;
}

.nav-actions {
  @include flex-align-center;
}

// 滚动内容
.scroll-content {
  height: 100vh;
  padding-top: 88rpx;
  padding-bottom: 120rpx;
}

.detail-content {
  padding: $spacing-md;
}

// 诗词卡片
.poetry-header-section {
  margin-bottom: $spacing-lg;
}

.poetry-card {
  background: linear-gradient(135deg, $card-bg 0%, $bg-secondary 100%);
  border-radius: $border-radius-xl;
  padding: $spacing-xl;
  @include card-shadow;
}

.poetry-title {
  font-size: 48rpx;
  font-weight: bold;
  color: $text-color;
  text-align: center;
  margin-bottom: $spacing-md;
  line-height: 1.4;
}

.poetry-meta {
  @include flex-center;
  margin-bottom: $spacing-xl;
  font-size: $font-size-base;
  color: $text-secondary;

  .author {
    color: $primary-color;
    font-weight: bold;
    @include transition;

    &:active {
      opacity: 0.7;
    }
  }

  .separator {
    margin: 0 $spacing-sm;
  }
}

.poetry-content {
  margin-bottom: $spacing-lg;
  padding: $spacing-lg 0;
  border-top: 1rpx solid $border-color;
  border-bottom: 1rpx solid $border-color;
}

.content-line {
  display: block;
  font-size: 36rpx;
  color: $text-color;
  line-height: 2.2;
  text-align: center;
  margin-bottom: $spacing-md;
  letter-spacing: 2rpx;
}

// 标签
.tags {
  @include flex-align-center;
  flex-wrap: wrap;
  margin-bottom: $spacing-md;
}

.tag {
  display: inline-block;
  padding: 8rpx 16rpx;
  margin-right: $spacing-sm;
  margin-bottom: $spacing-sm;
  background-color: rgba($primary-color, 0.1);
  color: $primary-color;
  border-radius: $border-radius-sm;
  font-size: $font-size-xs;
}

// 统计数据
.stats {
  @include flex-between;
  padding-top: $spacing-md;
}

.stat-item {
  @include flex-center;
  flex-direction: column;

  .stat-icon {
    font-size: 32rpx;
    margin-bottom: 4rpx;
  }

  .stat-value {
    font-size: $font-size-xs;
    color: $text-third;
  }
}

// 章节
.section {
  background-color: $card-bg;
  border-radius: $border-radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-md;
  @include card-shadow;
}

.section-header {
  @include flex-align-center;
  margin-bottom: $spacing-md;
  padding-bottom: $spacing-md;
  border-bottom: 2rpx solid $border-color;
}

.section-icon {
  font-size: 32rpx;
  margin-right: $spacing-sm;
}

.section-title {
  font-size: $font-size-lg;
  font-weight: bold;
  color: $text-color;
}

.section-content {
  line-height: 1.8;
  color: $text-secondary;
  font-size: $font-size-base;
}

.translation-text,
.appreciation-text {
  display: block;
  line-height: 2;
  text-indent: 2em;
}

// 注释
.annotation-item {
  margin-bottom: $spacing-sm;
  line-height: 1.8;
}

.annotation-term {
  font-weight: bold;
  color: $primary-color;
}

.annotation-explain {
  color: $text-secondary;
}

// 评论区
.comments-section {
  .section-content {
    padding: 0;
  }
}

.comments-list {
  margin-top: $spacing-md;
}

.comment-item {
  display: flex;
  padding: $spacing-md 0;
  border-bottom: 1rpx solid $border-color;

  &:last-child {
    border-bottom: none;
  }
}

.comment-avatar {
  width: 64rpx;
  height: 64rpx;
  border-radius: $border-radius-circle;
  margin-right: $spacing-md;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  @include flex-between;
  margin-bottom: $spacing-xs;
}

.comment-username {
  font-size: $font-size-sm;
  font-weight: bold;
  color: $text-color;
}

.comment-time {
  font-size: $font-size-xs;
  color: $text-third;
}

.comment-text {
  display: block;
  font-size: $font-size-base;
  color: $text-secondary;
  line-height: 1.6;
  margin-bottom: $spacing-sm;
}

.comment-actions {
  @include flex-align-center;

  .action-btn {
    @include flex-align-center;
    margin-right: $spacing-lg;
    font-size: $font-size-xs;
    color: $text-third;
    @include transition;

    &:active {
      transform: scale(0.95);
    }

    &.active {
      color: $error-color;
    }

    .icon {
      font-size: 24rpx;
      margin-right: 4rpx;
    }
  }
}

// 回复列表
.reply-list {
  margin-top: $spacing-sm;
  padding: $spacing-sm;
  background-color: $bg-secondary;
  border-radius: $border-radius-sm;
}

.reply-item {
  margin-bottom: $spacing-xs;
  font-size: $font-size-sm;
  line-height: 1.6;

  &:last-child {
    margin-bottom: 0;
  }
}

.reply-username {
  color: $primary-color;
  font-weight: bold;
}

.reply-text {
  color: $text-secondary;
}

// 底部操作栏
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  @include flex-between;
  padding: $spacing-md $spacing-lg;
  border-top: 1rpx solid;
  z-index: 999;
  @include transition(background-color);
}

.action-group {
  @include flex-align-center;
}

.action-btn {
  @include flex-center;
  flex-direction: column;
  margin-right: $spacing-xl;
  @include transition;

  &:active {
    transform: scale(0.95);
  }

  &.active {
    .icon {
      transform: scale(1.2);
    }
  }

  .icon {
    font-size: 40rpx;
    margin-bottom: 4rpx;
    @include transition;
  }

  .text {
    font-size: $font-size-xs;
    color: $text-third;
  }
}

.comment-input {
  flex: 1;
  padding: $spacing-md;
  background-color: $bg-secondary;
  border-radius: $border-radius-lg;

  .placeholder {
    font-size: $font-size-sm;
    color: $text-third;
  }
}

// 评论弹窗
.comment-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  @include flex-center;
  z-index: 9999;
}

.modal-content {
  width: 90%;
  max-width: 600rpx;
  background-color: $card-bg;
  border-radius: $border-radius-xl;
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

.comment-textarea {
  width: 100%;
  min-height: 240rpx;
  padding: $spacing-lg;
  font-size: $font-size-base;
  color: $text-color;
  line-height: 1.6;
  box-sizing: border-box;
}

.modal-footer {
  @include flex-between;
  padding: $spacing-md $spacing-lg;
  border-top: 1rpx solid $border-color;
}

.char-count {
  font-size: $font-size-xs;
  color: $text-third;
}

.submit-btn {
  @include reset-button;
  padding: $spacing-sm $spacing-xl;
  background-color: $button-primary;
  color: #FFFFFF;
  border-radius: $border-radius-lg;
  font-size: $font-size-base;
  font-weight: bold;
  @include transition;

  &:active {
    transform: scale(0.95);
    opacity: 0.8;
  }
}
</style>
