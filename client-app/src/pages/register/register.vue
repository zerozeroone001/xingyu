<template>
  <view class="register-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 注册表单 -->
      <view class="form-container theme-card">
        <view class="form-title">注册新账号</view>

        <view class="form-item">
          <view class="label">用户名 *</view>
          <input
            v-model="formData.username"
            class="input"
            type="text"
            placeholder="请输入用户名（4-20位）"
            placeholder-class="placeholder"
            maxlength="20"
          />
        </view>

        <view class="form-item">
          <view class="label">昵称</view>
          <input
            v-model="formData.nickname"
            class="input"
            type="text"
            placeholder="请输入昵称（选填）"
            placeholder-class="placeholder"
            maxlength="50"
          />
        </view>

        <view class="form-item">
          <view class="label">邮箱</view>
          <input
            v-model="formData.email"
            class="input"
            type="text"
            placeholder="请输入邮箱（选填）"
            placeholder-class="placeholder"
          />
        </view>

        <view class="form-item">
          <view class="label">密码 *</view>
          <input
            v-model="formData.password"
            class="input"
            type="password"
            placeholder="请输入密码（6-20位）"
            placeholder-class="placeholder"
            maxlength="20"
          />
        </view>

        <view class="form-item">
          <view class="label">确认密码 *</view>
          <input
            v-model="confirmPassword"
            class="input"
            type="password"
            placeholder="请再次输入密码"
            placeholder-class="placeholder"
            maxlength="20"
          />
        </view>

        <button
          class="submit-btn"
          :loading="userStore.isLoading"
          :disabled="!canSubmit"
          @click="handleRegister"
        >
          注册
        </button>

        <view class="footer">
          <text class="link" @click="goToLogin">已有账号？立即登录</text>
        </view>
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
  nickname: '',
  email: '',
  password: '',
});

const confirmPassword = ref('');

// 是否可提交
const canSubmit = computed(() => {
  const { username, password } = formData.value;
  return (
    username.trim().length >= 4 &&
    password.trim().length >= 6 &&
    password === confirmPassword.value
  );
});

/**
 * 处理注册
 */
const handleRegister = async () => {
  if (!canSubmit.value) {
    return;
  }

  // 验证用户名
  if (formData.value.username.length < 4 || formData.value.username.length > 20) {
    uni.showToast({
      title: '用户名长度为4-20位',
      icon: 'none',
      duration: 2000,
    });
    return;
  }

  // 验证密码
  if (formData.value.password.length < 6 || formData.value.password.length > 20) {
    uni.showToast({
      title: '密码长度为6-20位',
      icon: 'none',
      duration: 2000,
    });
    return;
  }

  // 验证确认密码
  if (formData.value.password !== confirmPassword.value) {
    uni.showToast({
      title: '两次输入的密码不一致',
      icon: 'none',
      duration: 2000,
    });
    return;
  }

  // 验证邮箱格式（如果填写了）
  if (formData.value.email) {
    const emailReg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailReg.test(formData.value.email)) {
      uni.showToast({
        title: '邮箱格式不正确',
        icon: 'none',
        duration: 2000,
      });
      return;
    }
  }

  const { username, password, email, nickname } = formData.value;
  const params: any = { username, password };

  if (email) params.email = email;
  if (nickname) params.nickname = nickname;

  const success = await userStore.register(params);

  if (success) {
    // 注册成功，跳转到登录页
    setTimeout(() => {
      uni.navigateBack();
    }, 1500);
  }
};

/**
 * 跳转到登录页
 */
const goToLogin = () => {
  uni.navigateBack();
};
</script>

<style lang="scss" scoped>
.register-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding: $spacing-xl;
}

.container {
  min-height: calc(100vh - 120rpx);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
</style>
