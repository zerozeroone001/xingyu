<template>
  <view class="profile-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 未登录状态 -->
      <view v-if="!userStore.isLoggedIn" class="not-logged-in">
        <!-- 默认用户卡片 -->
        <view class="user-card theme-card" @click="goToLogin">
          <view class="avatar-container">
            <view class="avatar-placeholder default">
              <text class="avatar-icon">👤</text>
            </view>
          </view>
          <view class="user-info">
            <view class="nickname">未登录</view>
            <view class="login-hint theme-text-tertiary">点击登录，体验更多功能</view>
          </view>
          <view class="login-arrow">→</view>
        </view>

        <!-- 功能预览 -->
        <view class="feature-preview">
          <view class="preview-title">登录后可以</view>
          <view class="preview-grid">
            <view class="preview-item theme-card" @click="goToLogin">
              <text class="preview-icon">❤️</text>
              <text class="preview-label">点赞诗词</text>
            </view>
            <view class="preview-item theme-card" @click="goToLogin">
              <text class="preview-icon">⭐</text>
              <text class="preview-label">收藏佳作</text>
            </view>
            <view class="preview-item theme-card" @click="goToLogin">
              <text class="preview-icon">📝</text>
              <text class="preview-label">发表动态</text>
            </view>
            <view class="preview-item theme-card" @click="goToLogin">
              <text class="preview-icon">👥</text>
              <text class="preview-label">关注好友</text>
            </view>
          </view>
        </view>

        <!-- 登录按钮 -->
        <button class="login-btn-primary" @click="goToLogin">立即登录</button>
      </view>

      <!-- 已登录状态 -->
      <template v-else>
        <!-- 用户信息卡片 -->
        <view class="user-card theme-card">
          <view class="avatar-container" @click="handleEditProfile">
            <image v-if="userStore.avatar" class="avatar" :src="userStore.avatar" mode="aspectFill" />
            <view v-else class="avatar-placeholder">{{ userStore.username?.charAt(0).toUpperCase() }}</view>
            <view class="edit-badge">
              <text class="edit-icon">✏️</text>
            </view>
          </view>

          <view class="user-info">
            <view class="nickname-row">
              <view class="nickname">{{ userStore.nickname }}</view>
              <view class="edit-btn" @click="handleEditProfile">
                <text>编辑</text>
              </view>
            </view>
            <view class="username theme-text-tertiary">@{{ userStore.username }}</view>
            <view v-if="userStore.userInfo?.bio" class="bio theme-text-secondary">{{ userStore.userInfo.bio }}</view>
            <view v-else class="bio theme-text-tertiary" @click="handleEditProfile">添加个人简介...</view>
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
          <view class="stat-item" @click="goToFollowing">
            <view class="stat-value">{{ stats.following }}</view>
            <view class="stat-label theme-text-tertiary">关注</view>
          </view>
          <view class="stat-divider"></view>
          <view class="stat-item" @click="goToFollowers">
            <view class="stat-value">{{ stats.followers }}</view>
            <view class="stat-label theme-text-tertiary">粉丝</view>
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
import { getFollowStats } from '@/api/follow';
import { getUserLikedPoetryList, getUserCollectedPoetryList } from '@/api/poetry';
import { getUserPostList } from '@/api/post';

const themeStore = useThemeStore();
const userStore = useUserStore();

const stats = ref({
  likes: 0,
  collects: 0,
  posts: 0,
  following: 0,
  followers: 0,
});

const unreadCount = ref(0);
const isLoadingStats = ref(false);

// 模拟统计数据
const mockStats = {
  likes: 28,
  collects: 15,
  posts: 5,
  following: 12,
  followers: 20,
};

/**
 * 加载统计数据
 */
const loadStats = async () => {
  if (!userStore.isLoggedIn || !userStore.userId) {
    return;
  }

  try {
    isLoadingStats.value = true;

    // 加载关注统计（现在需要userId参数）
    const followResponse = await getFollowStats(userStore.userId);
    stats.value.following = followResponse.data.following_count || 0;
    stats.value.followers = followResponse.data.followers_count || 0;

    // 加载点赞数
    const likesResponse = await getUserLikedPoetryList({ page: 1, size: 1 });
    stats.value.likes = likesResponse.data.total || 0;

    // 加载收藏数
    const collectsResponse = await getUserCollectedPoetryList({ page: 1, size: 1 });
    stats.value.collects = collectsResponse.data.total || 0;

    // 加载动态数
    const postsResponse = await getUserPostList(undefined, { page: 1, size: 1 });
    stats.value.posts = postsResponse.data.total || 0;

    // 如果所有数据都为0，使用模拟数据（用于演示）
    if (
      stats.value.likes === 0 &&
      stats.value.collects === 0 &&
      stats.value.posts === 0 &&
      stats.value.following === 0 &&
      stats.value.followers === 0
    ) {
      stats.value = { ...mockStats };
    }
  } catch (error) {
    console.error('加载统计数据失败:', error);
    // API 调用失败时使用模拟数据
    stats.value = { ...mockStats };
  } finally {
    isLoadingStats.value = false;
  }
};

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

    // 如果未读数为0，可以使用模拟数据（用于演示）
    if (unreadCount.value === 0) {
      unreadCount.value = 3; // 模拟3条未读消息
    }
  } catch (error) {
    console.error('加载未读消息数失败:', error);
    // API 调用失败时使用模拟数据
    unreadCount.value = 3;
  }
};

/**
 * 刷新数据
 */
const refreshData = async () => {
  await Promise.all([loadStats(), loadUnreadCount()]);
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
    url: '/login',
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
    url: '/setting',
  });
};

/**
 * 编辑用户信息
 */
const handleEditProfile = () => {
  uni.showModal({
    title: '编辑资料',
    content: '此功能正在开发中，敬请期待',
    showCancel: false,
  });
  // TODO: 跳转到编辑资料页面
  // uni.navigateTo({
  //   url: '/pages/edit-profile/edit-profile',
  // });
};

onMounted(() => {
  if (userStore.isLoggedIn) {
    loadStats();
    loadUnreadCount();
  }
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

// 未登录状态
.not-logged-in {
  .user-card {
    cursor: pointer;
    transition: all $transition-normal;

    &:active {
      transform: scale(0.98);
    }

    .avatar-placeholder.default {
      background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);

      .avatar-icon {
        font-size: 64rpx;
      }
    }

    .login-hint {
      margin-top: 4rpx;
      font-size: $font-size-sm;
    }

    .login-arrow {
      font-size: 40rpx;
      color: var(--text-tertiary);
      opacity: 0.6;
    }
  }

  .feature-preview {
    margin-top: $spacing-lg;
    margin-bottom: $spacing-xl;

    .preview-title {
      font-size: $font-size-lg;
      font-weight: $font-weight-bold;
      color: var(--text-primary);
      margin-bottom: $spacing-md;
    }

    .preview-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: $spacing-md;

      .preview-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: $spacing-xl;
        background-color: var(--bg-card);
        border-radius: $border-radius-lg;
        box-shadow: var(--shadow-sm);
        cursor: pointer;
        transition: all $transition-normal;

        &:active {
          transform: scale(0.95);
          box-shadow: var(--shadow-md);
        }

        .preview-icon {
          font-size: 48rpx;
          margin-bottom: $spacing-sm;
        }

        .preview-label {
          font-size: $font-size-sm;
          color: var(--text-secondary);
        }
      }
    }
  }

  .login-btn-primary {
    width: 100%;
    height: 90rpx;
    line-height: 90rpx;
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    color: #ffffff;
    background: linear-gradient(135deg, var(--color-primary) 0%, #667eea 100%);
    border: none;
    border-radius: $border-radius-lg;
    box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.3);
    transition: all $transition-normal;

    &:active {
      transform: scale(0.98);
      box-shadow: 0 4rpx 12rpx rgba(102, 126, 234, 0.2);
    }
  }
}

.user-card {
  display: flex;
  align-items: center;
  padding: $spacing-xl * 1.5;
  margin-bottom: $spacing-lg;
  background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card) 100%);
  border-radius: $border-radius-xl;
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;

  // 背景装饰
  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 200rpx;
    height: 200rpx;
    background: linear-gradient(135deg, var(--color-primary) 0%, #667eea 100%);
    opacity: 0.1;
    border-radius: 50%;
  }

  .avatar-container {
    position: relative;
    margin-right: $spacing-lg;
    cursor: pointer;

    .avatar,
    .avatar-placeholder {
      width: 140rpx;
      height: 140rpx;
      border-radius: 50%;
      border: 4rpx solid rgba(102, 126, 234, 0.1);
      transition: all $transition-normal;
    }

    .avatar-placeholder {
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, var(--color-primary) 0%, #667eea 100%);
      color: #ffffff;
      font-size: 56rpx;
      font-weight: $font-weight-bold;
      box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.3);
    }

    .edit-badge {
      position: absolute;
      bottom: 0;
      right: 0;
      width: 44rpx;
      height: 44rpx;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, var(--color-primary) 0%, #667eea 100%);
      border-radius: 50%;
      border: 3rpx solid var(--bg-card);
      box-shadow: 0 4rpx 12rpx rgba(102, 126, 234, 0.3);

      .edit-icon {
        font-size: 20rpx;
      }
    }

    &:active {
      .avatar,
      .avatar-placeholder {
        transform: scale(0.95);
      }
    }
  }

  .user-info {
    flex: 1;
    min-width: 0;

    .nickname-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8rpx;

      .nickname {
        font-size: $font-size-xl;
        font-weight: $font-weight-bold;
        color: var(--text-primary);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        flex: 1;
        margin-right: $spacing-sm;
      }

      .edit-btn {
        padding: 6rpx 16rpx;
        font-size: $font-size-xs;
        color: var(--color-primary);
        background-color: rgba(102, 126, 234, 0.1);
        border-radius: $border-radius-md;
        cursor: pointer;
        transition: all $transition-normal;

        &:active {
          transform: scale(0.95);
          background-color: rgba(102, 126, 234, 0.15);
        }
      }
    }

    .username {
      font-size: $font-size-sm;
      margin-bottom: 8rpx;
      opacity: 0.8;
    }

    .bio {
      font-size: $font-size-sm;
      line-height: 1.5;
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      cursor: pointer;

      &.theme-text-tertiary {
        font-style: italic;
        opacity: 0.6;
      }
    }
  }
}

.stats-card {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: $spacing-xl * 1.2;
  margin-bottom: $spacing-lg;
  background-color: var(--bg-card);
  border-radius: $border-radius-xl;
  box-shadow: var(--shadow-md);

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: all $transition-normal;
    padding: $spacing-sm;
    border-radius: $border-radius-md;

    &:active {
      transform: scale(0.95);
      background-color: rgba(102, 126, 234, 0.05);
    }

    .stat-value {
      font-size: 44rpx;
      font-weight: $font-weight-bold;
      color: var(--color-primary);
      margin-bottom: $spacing-xs;
      line-height: 1;
    }

    .stat-label {
      font-size: $font-size-sm;
      line-height: 1;
    }
  }

  .stat-divider {
    width: 2rpx;
    height: 60rpx;
    background: linear-gradient(to bottom, transparent, var(--border-primary), transparent);
    opacity: 0.5;
  }
}

.function-list {
  margin-bottom: $spacing-xl;

  .function-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: $spacing-lg $spacing-xl;
    margin-bottom: $spacing-md;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: all $transition-normal;
    border: 1px solid transparent;

    &:active {
      transform: scale(0.98);
      box-shadow: var(--shadow-md);
      border-color: rgba(102, 126, 234, 0.1);
    }

    .item-left {
      display: flex;
      align-items: center;
      position: relative;

      .item-icon {
        font-size: 40rpx;
        margin-right: $spacing-md;
        width: 50rpx;
        text-align: center;
      }

      .item-label {
        font-size: $font-size-md;
        font-weight: $font-weight-medium;
        color: var(--text-primary);
      }

      .badge {
        position: absolute;
        top: -10rpx;
        left: 40rpx;
        min-width: 36rpx;
        height: 36rpx;
        line-height: 36rpx;
        padding: 0 10rpx;
        font-size: $font-size-xs;
        font-weight: $font-weight-bold;
        color: #ffffff;
        background: linear-gradient(135deg, #ff6b6b 0%, #ff4444 100%);
        border-radius: 18rpx;
        text-align: center;
        box-shadow: 0 4rpx 12rpx rgba(255, 68, 68, 0.3);
      }
    }

    .item-arrow {
      font-size: $font-size-lg;
      color: var(--text-tertiary);
      opacity: 0.6;
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
  border: 2rpx solid rgba(255, 68, 68, 0.2);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);
  transition: all $transition-normal;

  &:active {
    opacity: 0.8;
    transform: scale(0.98);
    border-color: rgba(255, 68, 68, 0.4);
    box-shadow: var(--shadow-md);
  }
}
</style>
