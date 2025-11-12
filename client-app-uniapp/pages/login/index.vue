<template>
  <view class="login-page" :style="pageStyle">
    <!-- Logo区域 -->
    <view class="logo-section">
      <view class="logo-icon">🌙</view>
      <view class="app-name">星语诗词</view>
      <view class="app-slogan">品读千古诗词，感悟文化之美</view>
    </view>

    <!-- 登录表单 -->
    <view class="login-form">
      <!-- 账号密码登录 -->
      <view v-if="loginType === 'password'" class="form-content">
        <view class="form-item">
          <input
            v-model="username"
            class="form-input"
            placeholder="请输入用户名"
            placeholder-class="input-placeholder"
          />
        </view>
        <view class="form-item">
          <input
            v-model="password"
            class="form-input"
            type="password"
            placeholder="请输入密码"
            placeholder-class="input-placeholder"
          />
        </view>
        <button class="login-btn" @tap="handlePasswordLogin" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
        <view class="switch-type" @tap="switchLoginType">
          <text>微信快捷登录 →</text>
        </view>
      </view>

      <!-- 微信登录 -->
      <view v-else class="form-content">
        <button class="wechat-login-btn" @tap="handleWeChatLogin" :disabled="loading">
          <text class="wechat-icon">💬</text>
          <text>{{ loading ? '登录中...' : '微信快捷登录' }}</text>
        </button>
        <view class="switch-type" @tap="switchLoginType">
          <text>账号密码登录 →</text>
        </view>
      </view>

      <!-- 协议说明 -->
      <view class="agreement">
        <text class="agreement-text">登录即表示同意</text>
        <text class="agreement-link" @tap="showUserAgreement">《用户协议》</text>
        <text class="agreement-text">和</text>
        <text class="agreement-link" @tap="showPrivacyPolicy">《隐私政策》</text>
      </view>
    </view>

    <!-- 快速体验 -->
    <view class="quick-experience" @tap="skipLogin">
      <text>暂不登录，随便看看</text>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'

// Stores
const userStore = useUserStore()
const themeStore = useThemeStore()

// 数据
const loginType = ref('wechat') // wechat | password
const username = ref('')
const password = ref('')
const loading = ref(false)

// 页面样式（应用主题）
const pageStyle = computed(() => {
  const theme = themeStore.theme
  return {
    backgroundColor: theme.bgColor,
    color: theme.textColor
  }
})

/**
 * 切换登录方式
 */
const switchLoginType = () => {
  loginType.value = loginType.value === 'wechat' ? 'password' : 'wechat'
}

/**
 * 账号密码登录
 */
const handlePasswordLogin = async () => {
  if (!username.value.trim()) {
    uni.showToast({ title: '请输入用户名', icon: 'none' })
    return
  }

  if (!password.value.trim()) {
    uni.showToast({ title: '请输入密码', icon: 'none' })
    return
  }

  try {
    loading.value = true
    await userStore.login(username.value, password.value)

    // 登录成功，跳转到首页
    uni.switchTab({
      url: '/pages/index/index'
    })
  } catch (e) {
    console.error('登录失败:', e)
  } finally {
    loading.value = false
  }
}

/**
 * 微信登录
 */
const handleWeChatLogin = async () => {
  try {
    loading.value = true
    await userStore.wechatLogin()

    // 登录成功，跳转到首页
    uni.switchTab({
      url: '/pages/index/index'
    })
  } catch (e) {
    console.error('微信登录失败:', e)
    uni.showToast({
      title: '登录失败，请重试',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

/**
 * 跳过登录
 */
const skipLogin = () => {
  uni.switchTab({
    url: '/pages/index/index'
  })
}

/**
 * 显示用户协议
 */
const showUserAgreement = () => {
  uni.showModal({
    title: '用户协议',
    content: '这里是用户协议内容...',
    showCancel: false
  })
}

/**
 * 显示隐私政策
 */
const showPrivacyPolicy = () => {
  uni.showModal({
    title: '隐私政策',
    content: '这里是隐私政策内容...',
    showCancel: false
  })
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  padding: $spacing-xxl $spacing-lg;
  @include flex-center;
  flex-direction: column;
}

.logo-section {
  @include flex-center;
  flex-direction: column;
  margin-bottom: $spacing-xxl;
}

.logo-icon {
  font-size: 120rpx;
  margin-bottom: $spacing-lg;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20rpx);
  }
}

.app-name {
  font-size: $font-size-xxl;
  font-weight: bold;
  color: $primary-color;
  margin-bottom: $spacing-sm;
}

.app-slogan {
  font-size: $font-size-sm;
  color: $text-third;
}

.login-form {
  width: 100%;
  max-width: 600rpx;
}

.form-content {
  margin-bottom: $spacing-xl;
}

.form-item {
  margin-bottom: $spacing-md;
}

.form-input {
  width: 100%;
  padding: $spacing-md $spacing-lg;
  background-color: $bg-secondary;
  border-radius: $border-radius-lg;
  font-size: $font-size-base;
  color: $text-color;
}

.input-placeholder {
  color: $text-third;
}

.login-btn {
  @include reset-button;
  width: 100%;
  padding: $spacing-md;
  background-color: $button-primary;
  color: #FFFFFF;
  border-radius: $border-radius-lg;
  font-size: $font-size-lg;
  font-weight: bold;
  margin-top: $spacing-lg;
  @include transition;

  &:active:not([disabled]) {
    transform: scale(0.98);
    opacity: 0.8;
  }

  &[disabled] {
    opacity: 0.6;
  }
}

.wechat-login-btn {
  @include reset-button;
  @include flex-center;
  width: 100%;
  padding: $spacing-md;
  background-color: #07C160;
  color: #FFFFFF;
  border-radius: $border-radius-lg;
  font-size: $font-size-lg;
  font-weight: bold;
  @include transition;

  &:active:not([disabled]) {
    transform: scale(0.98);
    opacity: 0.8;
  }

  &[disabled] {
    opacity: 0.6;
  }

  .wechat-icon {
    font-size: 40rpx;
    margin-right: $spacing-sm;
  }
}

.switch-type {
  text-align: center;
  padding: $spacing-lg 0;
  font-size: $font-size-sm;
  color: $primary-color;
}

.agreement {
  text-align: center;
  padding: $spacing-md 0;
  font-size: $font-size-xs;
}

.agreement-text {
  color: $text-third;
}

.agreement-link {
  color: $primary-color;
}

.quick-experience {
  margin-top: $spacing-xl;
  padding: $spacing-md 0;
  font-size: $font-size-sm;
  color: $text-secondary;
  text-align: center;

  &:active {
    opacity: 0.7;
  }
}
</style>
