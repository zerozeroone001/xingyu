<template>
  <view class="user-detail-page" :class="themeStore.themeClass">
    <view v-if="userInfo" class="container">
      <!-- 用户信息卡片 -->
      <view class="user-card theme-card">
        <image
          v-if="userInfo.avatar"
          class="avatar"
          :src="userInfo.avatar"
          mode="aspectFill"
        />
        <view v-else class="avatar-placeholder">
          {{ userInfo.username?.charAt(0) }}
        </view>

        <view class="user-info">
          <view class="nickname">{{ userInfo.nickname || userInfo.username }}</view>
          <view class="username theme-text-tertiary">@{{ userInfo.username }}</view>
          <view v-if="userInfo.bio" class="bio theme-text-secondary">{{ userInfo.bio }}</view>
        </view>

        <!-- 关注按钮 -->
        <button
          class="follow-btn"
          :class="{ followed: isFollowing }"
          @click="handleFollow"
        >
          {{ isFollowing ? '已关注' : '关注' }}
        </button>
      </view>

      <!-- 统计数据 -->
      <view class="stats-card theme-card">
        <view class="stat-item" @click="goToFollowing">
          <view class="stat-value">{{ followStats.following_count || 0 }}</view>
          <view class="stat-label theme-text-tertiary">关注</view>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item" @click="goToFollowers">
          <view class="stat-value">{{ followStats.followers_count || 0 }}</view>
          <view class="stat-label theme-text-tertiary">粉丝</view>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item">
          <view class="stat-value">{{ postList.length }}</view>
          <view class="stat-label theme-text-tertiary">动态</view>
        </view>
      </view>

      <!-- 标签页 -->
      <view class="tabs">
        <view
          v-for="tab in tabs"
          :key="tab.value"
          class="tab-item"
          :class="{ active: currentTab === tab.value }"
          @click="switchTab(tab.value)"
        >
          {{ tab.label }}
        </view>
      </view>

      <!-- 动态列表 -->
      <view v-if="currentTab === 'posts'" class="post-list">
        <view v-if="!loading && postList.length === 0" class="empty-box">
          <text class="empty-text">还没有发布动态</text>
        </view>
        <view
          v-for="post in postList"
          :key="post.id"
          class="post-card theme-card"
          @click="goToPostDetail(post.id)"
        >
          <view class="post-content">{{ post.content }}</view>
          <view v-if="post.poetry_id" class="poetry-link theme-card-secondary">
            <view class="poetry-title">{{ post.poetry_title }}</view>
          </view>
          <view class="post-meta">
            <text class="theme-text-tertiary">{{ formatTime(post.created_at) }}</text>
          </view>
        </view>
      </view>

      <!-- 加载中 -->
      <view v-if="loading" class="loading-box">
        <text class="loading-text">加载中...</text>
      </view>
    </view>

    <!-- 加载中（初始） -->
    <view v-else-if="loading" class="loading-box">
      <text class="loading-text">加载中...</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { useUserStore } from '@/store/modules/user';
import { getUserPostList, type Post } from '@/api/post';
import { followUser, unfollowUser, checkFollowStatus, getFollowStats, type FollowStats } from '@/api/follow';
import type { UserInfo } from '@/api/auth';

const themeStore = useThemeStore();
const userStore = useUserStore();

const userId = ref<number>(0);
const userInfo = ref<UserInfo | null>(null);
const isFollowing = ref(false);
const followStats = ref<FollowStats>({
  following_count: 0,
  followers_count: 0,
  friends_count: 0,
});

const tabs = ref([
  { label: '动态', value: 'posts' },
]);
const currentTab = ref('posts');

const postList = ref<Post[]>([]);
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);

/**
 * 加载用户信息
 */
const loadUserInfo = async () => {
  try {
    loading.value = true;
    // 注意：这里需要有一个获取用户信息的 API
    // 由于当前 API 定义中没有这个接口，这里暂时使用模拟数据
    // 实际使用时需要调用类似 getUserInfo(userId.value) 的接口

    // 模拟用户信息
    userInfo.value = {
      id: userId.value,
      username: 'user_' + userId.value,
      nickname: '用户' + userId.value,
      avatar: '',
      bio: '这是用户的个人简介',
      created_at: new Date().toISOString(),
    };
  } catch (error) {
    console.error('加载用户信息失败:', error);
    uni.showToast({
      title: '加载失败',
      icon: 'none',
      duration: 2000,
    });
  } finally {
    loading.value = false;
  }
};

/**
 * 加载关注状态
 */
const loadFollowStatus = async () => {
  try {
    const response = await checkFollowStatus(userId.value);
    isFollowing.value = response.data.following;
  } catch (error) {
    console.error('加载关注状态失败:', error);
  }
};

/**
 * 加载关注统计
 */
const loadFollowStats = async () => {
  try {
    const response = await getFollowStats(userId.value);
    followStats.value = response.data;
  } catch (error) {
    console.error('加载关注统计失败:', error);
  }
};

/**
 * 加载动态列表
 */
const loadPostList = async (refresh = false) => {
  if (loading.value || (!refresh && !hasMore.value)) {
    return;
  }

  try {
    loading.value = true;

    if (refresh) {
      page.value = 1;
      postList.value = [];
      hasMore.value = true;
    }

    const response = await getUserPostList(userId.value, {
      page: page.value,
      size: 10,
    });

    const newPostList = response.data.items || [];

    if (refresh) {
      postList.value = newPostList;
    } else {
      postList.value.push(...newPostList);
    }

    hasMore.value = postList.value.length < (response.data.total || 0);
    page.value++;
  } catch (error) {
    console.error('加载动态列表失败:', error);
  } finally {
    loading.value = false;
  }
};

/**
 * 关注/取消关注
 */
const handleFollow = async () => {
  try {
    if (isFollowing.value) {
      await unfollowUser(userId.value);
      isFollowing.value = false;
      followStats.value.followers_count--;
      uni.showToast({
        title: '已取消关注',
        icon: 'success',
        duration: 1500,
      });
    } else {
      await followUser(userId.value);
      isFollowing.value = true;
      followStats.value.followers_count++;
      uni.showToast({
        title: '关注成功',
        icon: 'success',
        duration: 1500,
      });
    }
  } catch (error) {
    console.error('操作失败:', error);
    uni.showToast({
      title: '操作失败',
      icon: 'none',
      duration: 2000,
    });
  }
};

/**
 * 切换标签页
 */
const switchTab = (value: string) => {
  currentTab.value = value;
};

/**
 * 格式化时间
 */
const formatTime = (time: string) => {
  const date = new Date(time);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const minute = 60 * 1000;
  const hour = 60 * minute;
  const day = 24 * hour;

  if (diff < minute) {
    return '刚刚';
  } else if (diff < hour) {
    return `${Math.floor(diff / minute)}分钟前`;
  } else if (diff < day) {
    return `${Math.floor(diff / hour)}小时前`;
  } else if (diff < 7 * day) {
    return `${Math.floor(diff / day)}天前`;
  } else {
    return date.toLocaleDateString();
  }
};

/**
 * 跳转到关注列表
 */
const goToFollowing = () => {
  // 注意：这里应该跳转到该用户的关注列表，需要支持查看其他用户的关注列表
  uni.showToast({
    title: '功能开发中',
    icon: 'none',
    duration: 2000,
  });
};

/**
 * 跳转到粉丝列表
 */
const goToFollowers = () => {
  // 注意：这里应该跳转到该用户的粉丝列表，需要支持查看其他用户的粉丝列表
  uni.showToast({
    title: '功能开发中',
    icon: 'none',
    duration: 2000,
  });
};

/**
 * 跳转到动态详情
 */
const goToPostDetail = (id: number) => {
  uni.navigateTo({
    url: `/pages/post-detail/post-detail?id=${id}`,
  });
};

// 页面加载时获取数据
onMounted(() => {
  const pages = getCurrentPages();
  const currentPage = pages[pages.length - 1] as any;
  const options = currentPage.options || currentPage.$page?.options || {};
  userId.value = parseInt(options.id || '0');

  if (userId.value) {
    loadUserInfo();
    loadFollowStatus();
    loadFollowStats();
    loadPostList(true);
  }
});
</script>

<style lang="scss" scoped>
.user-detail-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 120rpx;
}

.container {
  padding: $spacing-md;
}

.user-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $spacing-xl;
  margin-bottom: $spacing-lg;
  background-color: var(--bg-card);
  border-radius: $border-radius-xl;
  box-shadow: var(--shadow-md);

  .avatar,
  .avatar-placeholder {
    width: 150rpx;
    height: 150rpx;
    border-radius: 50%;
    margin-bottom: $spacing-md;
  }

  .avatar-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--color-primary);
    color: #ffffff;
    font-size: 64rpx;
    font-weight: $font-weight-bold;
  }

  .user-info {
    text-align: center;
    margin-bottom: $spacing-lg;

    .nickname {
      font-size: $font-size-xl;
      font-weight: $font-weight-bold;
      color: var(--text-primary);
      margin-bottom: $spacing-xs;
    }

    .username {
      font-size: $font-size-sm;
      margin-bottom: $spacing-md;
    }

    .bio {
      font-size: $font-size-sm;
      line-height: 1.6;
    }
  }

  .follow-btn {
    width: 300rpx;
    height: 80rpx;
    line-height: 80rpx;
    font-size: $font-size-md;
    color: #ffffff;
    background-color: var(--color-primary);
    border: 1px solid var(--color-primary);
    border-radius: $border-radius-lg;

    &:active {
      opacity: 0.8;
    }

    &.followed {
      color: var(--text-secondary);
      background-color: var(--bg-secondary);
      border-color: var(--border-primary);
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

.tabs {
  display: flex;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  margin-bottom: $spacing-lg;
  padding: 8rpx;

  .tab-item {
    flex: 1;
    padding: $spacing-md;
    font-size: $font-size-md;
    color: var(--text-secondary);
    text-align: center;
    border-radius: $border-radius-md;
    cursor: pointer;
    transition: all $transition-normal;

    &.active {
      color: var(--color-primary);
      background-color: var(--bg-secondary);
      font-weight: $font-weight-medium;
    }
  }
}

.post-list {
  .empty-box {
    padding: 100rpx 0;
    text-align: center;

    .empty-text {
      font-size: $font-size-md;
      color: var(--text-secondary);
    }
  }

  .post-card {
    margin-bottom: $spacing-md;
    padding: $spacing-lg;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-sm);
    transition: all $transition-normal;

    &:active {
      transform: translateY(-4rpx);
      box-shadow: var(--shadow-md);
    }

    .post-content {
      font-size: $font-size-md;
      line-height: 1.8;
      color: var(--text-primary);
      margin-bottom: $spacing-md;
      white-space: pre-wrap;
    }

    .poetry-link {
      padding: $spacing-md;
      background-color: var(--bg-secondary);
      border-radius: $border-radius-md;
      border-left: 4rpx solid var(--color-primary);
      margin-bottom: $spacing-md;

      .poetry-title {
        font-size: $font-size-md;
        font-weight: $font-weight-medium;
        color: var(--text-primary);
      }
    }

    .post-meta {
      font-size: $font-size-xs;
    }
  }
}

.loading-box {
  padding: 80rpx 0;
  text-align: center;

  .loading-text {
    font-size: $font-size-md;
    color: var(--text-tertiary);
  }
}
</style>
