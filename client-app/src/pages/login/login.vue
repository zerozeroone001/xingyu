<template>
  <view class="login-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 顶部装饰 -->
      <view class="header">
        <text class="logo">✨</text>
        <text class="title">星语诗词</text>
        <text class="subtitle">探索中华诗词之美</text>
      </view>

      <!-- 登录表单 -->
      <view class="form-container theme-card">
        <view class="form-title">登录</view>

        <view class="form-item">
          <view class="label">用户名</view>
          <input
            v-model="formData.username"
            class="input"
            type="text"
            placeholder="请输入用户名"
            placeholder-class="placeholder"
          />
        </view>

        <view class="form-item">
          <view class="label">密码</view>
          <input
            v-model="formData.password"
            class="input"
            type="password"
            placeholder="请输入密码"
            placeholder-class="placeholder"
          />
        </view>

        <button
          class="submit-btn"
          :loading="userStore.isLoading"
          :disabled="!canSubmit"
          @click="handleLogin"
        >
          登录
        </button>

        <view class="footer">
          <text class="link" @click="goToRegister">还没有账号？立即注册</text>
        </view>
      </view>

      <!-- 游客模式 -->
      <view class="guest-mode">
        <text class="link" @click="goToHome">游客模式浏览</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useUserStore } from '@/store/modules/user';
import { useThemeStore } from '@/store/modules/theme';

const userStore = useUserStore();
const themeStore = useThemeStore();

// 表单数据
const formData = ref({
  username: '',
  password: '',
});

// 是否可提交
const canSubmit = computed(() => {
  return formData.value.username.trim() && formData.value.password.trim();
});

/**
 * 处理登录
 */
const handleLogin = async () => {
  if (!canSubmit.value) {
    return;
  }

  const success = await userStore.login(formData.value);

  if (success) {
    // 登录成功，跳转到首页
    setTimeout(() => {
      uni.switchTab({
        url: '/',
      });
    }, 1500);
  }
};

/**
 * 跳转到注册页
 */
const goToRegister = () => {
  uni.navigateTo({
    url: '/register',
  });
};

/**
 * 跳转到首页（游客模式）
 */
const goToHome = () => {
  uni.switchTab({
    url: '/',
  });
};
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary-light), var(--color-primary));
  padding: 0;
}

.container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
}

.header {
  text-align: center;
  margin-bottom: 80rpx;

  .logo {
    display: block;
    font-size: 120rpx;
    margin-bottom: $spacing-md;
  }

  .title {
    display: block;
    font-size: $font-size-xxl;
    font-weight: $font-weight-bold;
    color: #ffffff;
    margin-bottom: $spacing-xs;
  }

  .subtitle {
    display: block;
    font-size: $font-size-md;
    color: rgba(255, 255, 255, 0.9);
  }
}

.form-container {
  width: 100%;
  padding: 60rpx 40rpx;
  background-color: var(--bg-card);
  border-radius: $border-radius-xl;
  box-shadow: var(--shadow-lg);

  .form-title {
    font-size: $font-size-xl;
    font-weight: $font-weight-bold;
    color: var(--text-primary);
    text-align: center;
    margin-bottom: 60rpx;
  }

  .form-item {
    margin-bottom: $spacing-lg;

    .label {
      font-size: $font-size-md;
      color: var(--text-secondary);
      margin-bottom: $spacing-sm;
    }

    .input {
      width: 100%;
      height: 90rpx;
      padding: 0 $spacing-md;
      font-size: $font-size-md;
      color: var(--text-primary);
      background-color: var(--bg-secondary);
      border: 1px solid var(--border-primary);
      border-radius: $border-radius-md;
      transition: all $transition-normal;

      &:focus {
        border-color: var(--color-primary);
        background-color: var(--bg-primary);
      }
    }

    .placeholder {
      color: var(--text-tertiary);
    }
  }

  .submit-btn {
    width: 100%;
    height: 90rpx;
    line-height: 90rpx;
    margin-top: 40rpx;
    font-size: $font-size-md;
    font-weight: $font-weight-medium;
    color: #ffffff;
    background-color: var(--color-primary);
    border: none;
    border-radius: $border-radius-md;
    transition: all $transition-normal;

    &:active {
      opacity: 0.8;
      transform: scale(0.98);
    }

    &[disabled] {
      opacity: 0.5;
    }
  }

  .footer {
    margin-top: $spacing-lg;
    text-align: center;

    .link {
      font-size: $font-size-sm;
      color: var(--color-primary);
      cursor: pointer;

      &:active {
        opacity: 0.7;
      }
    }
  }
}

.guest-mode {
  margin-top: 60rpx;
  text-align: center;

  .link {
    font-size: $font-size-md;
    color: rgba(255, 255, 255, 0.9);
    text-decoration: underline;
    cursor: pointer;

    &:active {
      opacity: 0.7;
    }
  }
}
</style>
