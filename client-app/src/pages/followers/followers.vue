<template>
  <view class="followers-page" :class="themeStore.themeClass">
    <view class="container">
      <!-- 空状态 -->
      <view v-if="!loading && userList.length === 0" class="empty-box">
        <text class="empty-icon">👤</text>
        <text class="empty-text">还没有粉丝</text>
        <button class="explore-btn" @click="goToSquare">去广场看看</button>
      </view>

      <!-- 用户列表 -->
      <view v-else class="user-list">
        <view
          v-for="user in userList"
          :key="user.id"
          class="user-card theme-card"
          @click="goToUserDetail(user.id)"
        >
          <view class="user-info">
            <image
              v-if="user.avatar"
              class="avatar"
              :src="user.avatar"
              mode="aspectFill"
            />
            <view v-else class="avatar-placeholder">
              {{ user.username?.charAt(0) }}
            </view>

            <view class="user-text">
              <view class="nickname">{{ user.nickname || user.username }}</view>
              <view class="username theme-text-tertiary">@{{ user.username }}</view>
              <view v-if="user.bio" class="bio theme-text-secondary">{{ user.bio }}</view>
            </view>
          </view>

          <button
            class="follow-btn"
            :class="{ 'followed': followStatus[user.id] }"
            @click.stop="handleFollow(user.id)"
          >
            {{ followStatus[user.id] ? '已关注' : '关注' }}
          </button>
        </view>
      </view>

      <!-- 加载中 -->
      <view v-if="loading && userList.length === 0" class="loading-box">
        <text class="loading-text">加载中...</text>
      </view>

      <!-- 加载更多 -->
      <view v-if="userList.length > 0" class="load-more">
        <text v-if="loading" class="load-more-text">加载中...</text>
        <text v-else-if="!hasMore" class="load-more-text theme-text-tertiary">没有更多了</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { getFollowersList, followUser, unfollowUser, checkFollowStatus } from '@/api/follow';
import type { UserInfo } from '@/api/auth';

const themeStore = useThemeStore();

const userList = ref<UserInfo[]>([]);
const followStatus = ref<Record<number, boolean>>({});
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);

/**
 * 加载粉丝列表
 */
const loadUserList = async (refresh = false) => {
  if (loading.value || (!refresh && !hasMore.value)) {
    return;
  }

  try {
    loading.value = true;

    if (refresh) {
      page.value = 1;
      userList.value = [];
      hasMore.value = true;
    }

    const response = await getFollowersList(undefined, {
      page: page.value,
      size: 20,
    });

    const newUserList = response.data.list || [];

    if (refresh) {
      userList.value = newUserList;
    } else {
      userList.value.push(...newUserList);
    }

    hasMore.value = userList.value.length < (response.data.total || 0);
    page.value++;

    // 检查关注状态
    await loadFollowStatus();
  } catch (error) {
    console.error('加载粉丝列表失败:', error);
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
    for (const user of userList.value) {
      const response = await checkFollowStatus(user.id);
      followStatus.value[user.id] = response.data.following;
    }
  } catch (error) {
    console.error('加载关注状态失败:', error);
  }
};

/**
 * 关注/取消关注
 */
const handleFollow = async (userId: number) => {
  try {
    const isFollowing = followStatus.value[userId];

    if (isFollowing) {
      await unfollowUser(userId);
      followStatus.value[userId] = false;
      uni.showToast({
        title: '已取消关注',
        icon: 'success',
        duration: 1500,
      });
    } else {
      await followUser(userId);
      followStatus.value[userId] = true;
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
 * 跳转到用户主页
 */
const goToUserDetail = (userId: number) => {
  uni.navigateTo({
    url: `/pages/user-detail/user-detail?id=${userId}`,
  });
};

/**
 * 跳转到广场
 */
const goToSquare = () => {
  uni.switchTab({
    url: '/pages/square/square',
  });
};

/**
 * 下拉刷新
 */
const onPullDownRefresh = async () => {
  await loadUserList(true);
  uni.stopPullDownRefresh();
};

/**
 * 上拉加载更多
 */
const onReachBottom = () => {
  loadUserList();
};

// 页面加载时获取数据
onMounted(() => {
  loadUserList(true);
});

// 导出给页面生命周期使用
defineExpose({
  onPullDownRefresh,
  onReachBottom,
});
</script>

<style lang="scss" scoped>
.followers-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 120rpx;
}

.container {
  padding: $spacing-md;
}

.empty-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 200rpx $spacing-xl 100rpx;

  .empty-icon {
    font-size: 120rpx;
    margin-bottom: $spacing-lg;
    opacity: 0.5;
  }

  .empty-text {
    font-size: $font-size-md;
    color: var(--text-secondary);
    margin-bottom: $spacing-xl;
  }

  .explore-btn {
    width: 300rpx;
    height: 80rpx;
    line-height: 80rpx;
    font-size: $font-size-md;
    color: #ffffff;
    background-color: var(--color-primary);
    border: none;
    border-radius: $border-radius-lg;
  }
}

.user-list {
  .user-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
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

    .user-info {
      display: flex;
      align-items: center;
      flex: 1;
      min-width: 0;

      .avatar,
      .avatar-placeholder {
        width: 100rpx;
        height: 100rpx;
        border-radius: 50%;
        margin-right: $spacing-md;
        flex-shrink: 0;
      }

      .avatar-placeholder {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: var(--color-primary);
        color: #ffffff;
        font-size: $font-size-xl;
        font-weight: $font-weight-bold;
      }

      .user-text {
        flex: 1;
        min-width: 0;

        .nickname {
          font-size: $font-size-md;
          font-weight: $font-weight-medium;
          color: var(--text-primary);
          margin-bottom: 4rpx;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .username {
          font-size: $font-size-sm;
          margin-bottom: $spacing-xs;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .bio {
          font-size: $font-size-xs;
          line-height: 1.4;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
        }
      }
    }

    .follow-btn {
      padding: 12rpx 32rpx;
      font-size: $font-size-sm;
      color: #ffffff;
      background-color: var(--color-primary);
      border: 1px solid var(--color-primary);
      border-radius: $border-radius-md;
      flex-shrink: 0;
      margin-left: $spacing-md;

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
}

.loading-box {
  padding: 80rpx 0;
  text-align: center;

  .loading-text {
    font-size: $font-size-md;
    color: var(--text-tertiary);
  }
}

.load-more {
  padding: $spacing-lg 0;
  text-align: center;

  .load-more-text {
    font-size: $font-size-sm;
    color: var(--text-tertiary);
  }
}
</style>
