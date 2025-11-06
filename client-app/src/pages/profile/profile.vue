<template>
  <view class="profile-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 未登录状态 -->
      <view v-if="!userStore.isLoggedIn" class="login-prompt theme-card">
        <view class="prompt-icon">👤</view>
        <view class="prompt-text">登录后查看更多功能</view>
        <button class="login-btn" @click="goToLogin">立即登录</button>
      </view>

      <!-- 已登录状态 -->
      <template v-else>
        <!-- 用户信息卡片 -->
        <view class="user-card theme-card">
          <image v-if="userStore.avatar" class="avatar" :src="userStore.avatar" mode="aspectFill" />
          <view v-else class="avatar-placeholder">{{ userStore.username?.charAt(0) }}</view>

          <view class="user-info">
            <view class="nickname">{{ userStore.nickname }}</view>
            <view class="username theme-text-tertiary">@{{ userStore.username }}</view>
          </view>
        </view>

        <!-- 统计数据 -->
        <view class="stats-card theme-card">
          <view class="stat-item" @click="goToMyLikes">
            <view class="stat-value">{{ stats.likes }}</view>
            <view class="stat-label theme-text-tertiary">点赞</view>
          </view>
          <view class="stat-divider"></view>
          <view class="stat-item" @click="goToMyCollects">
            <view class="stat-value">{{ stats.collects }}</view>
            <view class="stat-label theme-text-tertiary">收藏</view>
          </view>
          <view class="stat-divider"></view>
          <view class="stat-item" @click="goToMyPosts">
            <view class="stat-value">{{ stats.posts }}</view>
            <view class="stat-label theme-text-tertiary">动态</view>
          </view>
          <view class="stat-divider"></view>
          <view class="stat-item" @click="goToFollowing">
            <view class="stat-value">{{ stats.following }}</view>
            <view class="stat-label theme-text-tertiary">关注</view>
          </view>
        </view>

        <!-- 功能列表 -->
        <view class="function-list">
          <view class="function-item theme-card" @click="goToMyLikes">
            <view class="item-left">
              <text class="item-icon">❤️</text>
              <text class="item-label">我的点赞</text>
            </view>
            <text class="item-arrow">→</text>
          </view>

          <view class="function-item theme-card" @click="goToMyCollects">
            <view class="item-left">
              <text class="item-icon">⭐</text>
              <text class="item-label">我的收藏</text>
            </view>
            <text class="item-arrow">→</text>
          </view>

          <view class="function-item theme-card" @click="goToMyPosts">
            <view class="item-left">
              <text class="item-icon">📝</text>
              <text class="item-label">我的动态</text>
            </view>
            <text class="item-arrow">→</text>
          </view>

          <view class="function-item theme-card" @click="goToFollowing">
            <view class="item-left">
              <text class="item-icon">👥</text>
              <text class="item-label">我的关注</text>
            </view>
            <text class="item-arrow">→</text>
          </view>

          <view class="function-item theme-card" @click="goToFollowers">
            <view class="item-left">
              <text class="item-icon">👤</text>
              <text class="item-label">我的粉丝</text>
            </view>
            <text class="item-arrow">→</text>
          </view>

          <view class="function-item theme-card" @click="goToMessage">
            <view class="item-left">
              <text class="item-icon">💬</text>
              <text class="item-label">消息通知</text>
              <view v-if="unreadCount > 0" class="badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</view>
            </view>
            <text class="item-arrow">→</text>
          </view>

          <view class="function-item theme-card" @click="goToSetting">
            <view class="item-left">
              <text class="item-icon">⚙️</text>
              <text class="item-label">设置</text>
            </view>
            <text class="item-arrow">→</text>
          </view>
        </view>

        <!-- 退出登录 -->
        <button class="logout-btn" @click="handleLogout">退出登录</button>
      </template>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { useUserStore } from '@/store/modules/user';
import { getUnreadStats } from '@/api/notification';

const themeStore = useThemeStore();
const userStore = useUserStore();

const stats = ref({
  likes: 0,
  collects: 0,
  posts: 0,
  following: 0,
});

const unreadCount = ref(0);

/**
 * 加载未读消息数
 */
const loadUnreadCount = async () => {
  if (!userStore.isLoggedIn) {
    return;
  }

  try {
    const response = await getUnreadStats();
    unreadCount.value = response.data.total || 0;
  } catch (error) {
    console.error('加载未读消息数失败:', error);
  }
};

/**
 * 退出登录
 */
const handleLogout = () => {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: async (res) => {
      if (res.confirm) {
        await userStore.logout();
      }
    },
  });
};

/**
 * 跳转到登录页
 */
const goToLogin = () => {
  uni.navigateTo({
    url: '/pages/login/login',
  });
};

/**
 * 跳转到我的点赞
 */
const goToMyLikes = () => {
  uni.navigateTo({
    url: '/pages/my-likes/my-likes',
  });
};

/**
 * 跳转到我的收藏
 */
const goToMyCollects = () => {
  uni.navigateTo({
    url: '/pages/my-collects/my-collects',
  });
};

/**
 * 跳转到我的动态
 */
const goToMyPosts = () => {
  uni.navigateTo({
    url: '/pages/my-posts/my-posts',
  });
};

/**
 * 跳转到我的关注
 */
const goToFollowing = () => {
  uni.navigateTo({
    url: '/pages/following/following',
  });
};

/**
 * 跳转到我的粉丝
 */
const goToFollowers = () => {
  uni.navigateTo({
    url: '/pages/followers/followers',
  });
};

/**
 * 跳转到消息页
 */
const goToMessage = () => {
  uni.navigateTo({
    url: '/pages/message/message',
  });
};

/**
 * 跳转到设置页
 */
const goToSetting = () => {
  uni.switchTab({
    url: '/pages/setting/setting',
  });
};

onMounted(() => {
  loadUnreadCount();
});
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 120rpx;
}

.container {
  padding: $spacing-md;
}

.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx $spacing-xl;
  background-color: var(--bg-card);
  border-radius: $border-radius-xl;
  box-shadow: var(--shadow-md);

  .prompt-icon {
    font-size: 120rpx;
    margin-bottom: $spacing-lg;
  }

  .prompt-text {
    font-size: $font-size-lg;
    color: var(--text-secondary);
    margin-bottom: $spacing-xl;
  }

  .login-btn {
    width: 400rpx;
    height: 80rpx;
    line-height: 80rpx;
    font-size: $font-size-md;
    color: #ffffff;
    background-color: var(--color-primary);
    border: none;
    border-radius: $border-radius-lg;
  }
}

.user-card {
  display: flex;
  align-items: center;
  padding: $spacing-xl;
  margin-bottom: $spacing-lg;
  background-color: var(--bg-card);
  border-radius: $border-radius-xl;
  box-shadow: var(--shadow-md);

  .avatar,
  .avatar-placeholder {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    margin-right: $spacing-lg;
  }

  .avatar-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--color-primary);
    color: #ffffff;
    font-size: $font-size-xxl;
    font-weight: $font-weight-bold;
  }

  .user-info {
    flex: 1;

    .nickname {
      font-size: $font-size-xl;
      font-weight: $font-weight-bold;
      color: var(--text-primary);
      margin-bottom: $spacing-xs;
    }

    .username {
      font-size: $font-size-sm;
    }
  }
}

.stats-card {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: $spacing-xl;
  margin-bottom: $spacing-lg;
  background-color: var(--bg-card);
  border-radius: $border-radius-xl;
  box-shadow: var(--shadow-md);

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;

    .stat-value {
      font-size: $font-size-xl;
      font-weight: $font-weight-bold;
      color: var(--text-primary);
      margin-bottom: $spacing-xs;
    }

    .stat-label {
      font-size: $font-size-sm;
    }
  }

  .stat-divider {
    width: 1px;
    height: 60rpx;
    background-color: var(--border-primary);
  }
}

.function-list {
  margin-bottom: $spacing-xl;

  .function-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: $spacing-lg $spacing-xl;
    margin-bottom: $spacing-sm;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: all $transition-normal;

    &:active {
      transform: scale(0.98);
    }

    .item-left {
      display: flex;
      align-items: center;
      position: relative;

      .item-icon {
        font-size: 36rpx;
        margin-right: $spacing-md;
      }

      .item-label {
        font-size: $font-size-md;
        color: var(--text-primary);
      }

      .badge {
        position: absolute;
        top: -10rpx;
        left: 40rpx;
        min-width: 32rpx;
        height: 32rpx;
        line-height: 32rpx;
        padding: 0 8rpx;
        font-size: $font-size-xs;
        color: #ffffff;
        background-color: #ff4444;
        border-radius: 16rpx;
        text-align: center;
      }
    }

    .item-arrow {
      font-size: $font-size-lg;
      color: var(--text-tertiary);
    }
  }
}

.logout-btn {
  width: 100%;
  height: 90rpx;
  line-height: 90rpx;
  font-size: $font-size-md;
  font-weight: $font-weight-medium;
  color: var(--color-error);
  background-color: var(--bg-card);
  border: 1px solid var(--border-primary);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  &:active {
    opacity: 0.8;
  }
}
</style>
