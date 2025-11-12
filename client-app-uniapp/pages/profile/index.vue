<template>
  <view class="profile-page" :style="pageStyle">
    <!-- 用户信息区域 -->
    <view class="profile-header">
      <view class="user-info" v-if="isLogin">
        <image :src="userInfo.avatar || defaultAvatar" class="avatar" mode="aspectFill" @tap="goToEdit"></image>
        <view class="user-details">
          <view class="nickname">{{ userInfo.nickname || '未设置昵称' }}</view>
          <view class="user-meta">
            <text class="level">LV{{ userInfo.level || 1 }}</text>
            <text class="id">ID: {{ userInfo.id }}</text>
          </view>
        </view>
        <view class="edit-btn" @tap="goToEdit">
          <text>✏️</text>
        </view>
      </view>

      <!-- 未登录状态 -->
      <view class="login-prompt" v-else @tap="goToLogin">
        <image :src="defaultAvatar" class="avatar" mode="aspectFill"></image>
        <view class="login-text">点击登录</view>
      </view>

      <!-- 统计信息 -->
      <view class="stats-row" v-if="isLogin">
        <view class="stat-item" @tap="goToFollow">
          <view class="stat-value">{{ userInfo.follow_count || 0 }}</view>
          <view class="stat-label">关注</view>
        </view>
        <view class="stat-item" @tap="goToFollower">
          <view class="stat-value">{{ userInfo.follower_count || 0 }}</view>
          <view class="stat-label">粉丝</view>
        </view>
        <view class="stat-item" @tap="goToCollect">
          <view class="stat-value">{{ userInfo.collect_count || 0 }}</view>
          <view class="stat-label">收藏</view>
        </view>
        <view class="stat-item" @tap="goToLike">
          <view class="stat-value">{{ userInfo.like_count || 0 }}</view>
          <view class="stat-label">点赞</view>
        </view>
      </view>
    </view>

    <!-- 功能菜单 -->
    <view class="menu-section">
      <view class="menu-group">
        <view class="menu-item" @tap="goToCollect">
          <view class="menu-left">
            <text class="menu-icon">⭐</text>
            <text class="menu-title">我的收藏</text>
          </view>
          <text class="menu-arrow">→</text>
        </view>
        <view class="menu-item" @tap="goToHistory">
          <view class="menu-left">
            <text class="menu-icon">📖</text>
            <text class="menu-title">浏览历史</text>
          </view>
          <text class="menu-arrow">→</text>
        </view>
        <view class="menu-item" @tap="goToMessages">
          <view class="menu-left">
            <text class="menu-icon">💬</text>
            <text class="menu-title">消息中心</text>
          </view>
          <view class="menu-right">
            <text v-if="unreadCount > 0" class="badge">{{ unreadCount }}</text>
            <text class="menu-arrow">→</text>
          </view>
        </view>
      </view>

      <view class="menu-group">
        <view class="menu-item" @tap="goToTheme">
          <view class="menu-left">
            <text class="menu-icon">🎨</text>
            <text class="menu-title">主题设置</text>
          </view>
          <view class="menu-right">
            <text class="theme-name">{{ currentThemeName }}</text>
            <text class="menu-arrow">→</text>
          </view>
        </view>
        <view class="menu-item" @tap="goToSettings">
          <view class="menu-left">
            <text class="menu-icon">⚙️</text>
            <text class="menu-title">设置</text>
          </view>
          <text class="menu-arrow">→</text>
        </view>
        <view class="menu-item" @tap="goToAbout">
          <view class="menu-left">
            <text class="menu-icon">ℹ️</text>
            <text class="menu-title">关于</text>
          </view>
          <text class="menu-arrow">→</text>
        </view>
      </view>

      <!-- 退出登录 -->
      <view class="menu-group" v-if="isLogin">
        <view class="menu-item logout-item" @tap="handleLogout">
          <text class="menu-title">退出登录</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'
import { getUnreadCount } from '@/api/message'

// Stores
const userStore = useUserStore()
const themeStore = useThemeStore()

// 数据
const defaultAvatar = '/static/default-avatar.png'
const unreadCount = ref(0)

// 计算属性
const isLogin = computed(() => userStore.isLogin)
const userInfo = computed(() => userStore.userInfo || {})
const currentThemeName = computed(() => themeStore.theme.name)

// 页面样式
const pageStyle = computed(() => {
  const theme = themeStore.theme
  return {
    backgroundColor: theme.bgColor,
    color: theme.textColor
  }
})

/**
 * 加载未读消息数
 */
const loadUnreadCount = async () => {
  if (!isLogin.value) return

  try {
    const data = await getUnreadCount()
    unreadCount.value = data.count || 0
  } catch (e) {
    console.error('获取未读消息数失败:', e)
  }
}

/**
 * 跳转到登录页
 */
const goToLogin = () => {
  uni.navigateTo({
    url: '/pages/login/index'
  })
}

/**
 * 跳转到编辑资料
 */
const goToEdit = () => {
  uni.navigateTo({
    url: '/pages/profile-edit/index'
  })
}

/**
 * 跳转到关注列表
 */
const goToFollow = () => {
  if (!isLogin.value) {
    goToLogin()
    return
  }
  uni.navigateTo({
    url: '/pages/my-follow/index'
  })
}

/**
 * 跳转到粉丝列表
 */
const goToFollower = () => {
  if (!isLogin.value) {
    goToLogin()
    return
  }
  uni.navigateTo({
    url: '/pages/my-follower/index'
  })
}

/**
 * 跳转到收藏
 */
const goToCollect = () => {
  if (!isLogin.value) {
    goToLogin()
    return
  }
  uni.navigateTo({
    url: '/pages/my-collect/index'
  })
}

/**
 * 跳转到点赞
 */
const goToLike = () => {
  if (!isLogin.value) {
    goToLogin()
    return
  }
  uni.navigateTo({
    url: '/pages/my-like/index'
  })
}

/**
 * 跳转到浏览历史
 */
const goToHistory = () => {
  uni.navigateTo({
    url: '/pages/my-history/index'
  })
}

/**
 * 跳转到消息中心
 */
const goToMessages = () => {
  if (!isLogin.value) {
    goToLogin()
    return
  }
  uni.navigateTo({
    url: '/pages/messages/index'
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
 * 跳转到设置
 */
const goToSettings = () => {
  uni.navigateTo({
    url: '/pages/settings/index'
  })
}

/**
 * 跳转到关于
 */
const goToAbout = () => {
  uni.navigateTo({
    url: '/pages/about/index'
  })
}

/**
 * 退出登录
 */
const handleLogout = async () => {
  const confirmed = await new Promise((resolve) => {
    uni.showModal({
      title: '提示',
      content: '确定要退出登录吗?',
      success: (res) => resolve(res.confirm)
    })
  })

  if (confirmed) {
    await userStore.logout()
  }
}

// 页面加载
onMounted(() => {
  loadUnreadCount()
})
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100vh;
}

.profile-header {
  padding: $spacing-xl $spacing-lg;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  color: #FFFFFF;
}

.user-info {
  @include flex-align-center;
  margin-bottom: $spacing-xl;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: $border-radius-circle;
  border: 4rpx solid rgba(255, 255, 255, 0.5);
  margin-right: $spacing-md;
}

.user-details {
  flex: 1;
}

.nickname {
  font-size: $font-size-xl;
  font-weight: bold;
  margin-bottom: $spacing-xs;
}

.user-meta {
  @include flex-align-center;
  font-size: $font-size-sm;
  opacity: 0.9;
}

.level {
  padding: 2rpx 12rpx;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: $border-radius-sm;
  margin-right: $spacing-sm;
}

.edit-btn {
  @include flex-center;
  width: 60rpx;
  height: 60rpx;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: $border-radius-circle;
  font-size: 32rpx;

  &:active {
    opacity: 0.7;
  }
}

.login-prompt {
  @include flex-center;
  flex-direction: column;
  padding: $spacing-xl 0;
}

.login-text {
  font-size: $font-size-lg;
  margin-top: $spacing-md;
}

.stats-row {
  @include flex-between;
  padding: $spacing-lg;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: $border-radius-lg;
}

.stat-item {
  @include flex-center;
  flex-direction: column;
  flex: 1;

  &:active {
    opacity: 0.7;
  }
}

.stat-value {
  font-size: $font-size-xl;
  font-weight: bold;
  margin-bottom: 4rpx;
}

.stat-label {
  font-size: $font-size-xs;
  opacity: 0.8;
}

.menu-section {
  padding: $spacing-lg;
}

.menu-group {
  background-color: $card-bg;
  border-radius: $border-radius-lg;
  margin-bottom: $spacing-md;
  overflow: hidden;
}

.menu-item {
  @include flex-between;
  padding: $spacing-lg;
  border-bottom: 1rpx solid $border-color;
  @include transition;

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background-color: $bg-secondary;
  }

  &.logout-item {
    justify-content: center;
    color: $danger-color;
  }
}

.menu-left {
  @include flex-align-center;
}

.menu-icon {
  font-size: 36rpx;
  margin-right: $spacing-md;
}

.menu-title {
  font-size: $font-size-base;
  color: $text-color;
}

.menu-right {
  @include flex-align-center;
}

.theme-name {
  font-size: $font-size-sm;
  color: $text-third;
  margin-right: $spacing-sm;
}

.menu-arrow {
  font-size: $font-size-base;
  color: $text-third;
}

.badge {
  background-color: $danger-color;
  color: #FFFFFF;
  font-size: $font-size-xs;
  padding: 2rpx 8rpx;
  border-radius: 20rpx;
  margin-right: $spacing-sm;
  min-width: 32rpx;
  text-align: center;
}
</style>
