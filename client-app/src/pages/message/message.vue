<template>
  <view class="message-page" :class="themeStore.themeClass">
    <!-- 消息类型标签页 -->
    <view class="tabs">
      <view
        v-for="tab in tabs"
        :key="tab.value"
        class="tab-item"
        :class="{ active: currentTab === tab.value }"
        @click="switchTab(tab.value)"
      >
        {{ tab.label }}
        <view v-if="tab.count > 0" class="tab-badge">{{ tab.count > 99 ? '99+' : tab.count }}</view>
      </view>
    </view>

    <view class="container">
      <!-- 空状态 -->
      <view v-if="!loading && messageList.length === 0" class="empty-box">
        <text class="empty-icon">💬</text>
        <text class="empty-text">暂无消息</text>
      </view>

      <!-- 消息列表 -->
      <view v-else class="message-list">
        <view
          v-for="message in messageList"
          :key="message.id"
          class="message-card theme-card"
          :class="{ unread: message.status === 'unread' }"
          @click="handleMessageClick(message)"
        >
          <view class="message-icon">{{ getMessageIcon(message.type) }}</view>
          <view class="message-content">
            <view class="message-title">{{ message.title }}</view>
            <view class="message-text theme-text-secondary">{{ message.content }}</view>
            <view class="message-time theme-text-tertiary">{{ formatTime(message.created_at) }}</view>
          </view>
          <view v-if="message.status === 'unread'" class="unread-dot"></view>
        </view>
      </view>

      <!-- 加载中 -->
      <view v-if="loading && messageList.length === 0" class="loading-box">
        <text class="loading-text">加载中...</text>
      </view>

      <!-- 加载更多 -->
      <view v-if="messageList.length > 0" class="load-more">
        <text v-if="loading" class="load-more-text">加载中...</text>
        <text v-else-if="!hasMore" class="load-more-text theme-text-tertiary">没有更多了</text>
      </view>
    </view>

    <!-- 底部操作栏 -->
    <view v-if="messageList.length > 0" class="bottom-bar theme-card">
      <button class="action-btn" @click="handleMarkAllRead">全部标为已读</button>
      <button class="action-btn danger" @click="handleClearAll">清空消息</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import {
  getNotificationList,
  getUnreadStats,
  markAsRead,
  markAllAsRead,
  deleteAllNotifications,
  type Notification,
  NotificationType,
  type UnreadStats,
} from '@/api/notification';

const themeStore = useThemeStore();

const tabs = ref([
  { label: '全部', value: '', count: 0 },
  { label: '系统', value: NotificationType.SYSTEM, count: 0 },
  { label: '点赞', value: NotificationType.LIKE, count: 0 },
  { label: '评论', value: NotificationType.COMMENT, count: 0 },
  { label: '关注', value: NotificationType.FOLLOW, count: 0 },
  { label: '收藏', value: NotificationType.COLLECT, count: 0 },
]);

const currentTab = ref<string>('');
const messageList = ref<Notification[]>([]);
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);

/**
 * 加载未读统计
 */
const loadUnreadStats = async () => {
  try {
    const response = await getUnreadStats();
    const stats: UnreadStats = response.data;

    tabs.value[0].count = stats.total || 0;
    tabs.value[1].count = stats.system || 0;
    tabs.value[2].count = stats.like || 0;
    tabs.value[3].count = stats.comment || 0;
    tabs.value[4].count = stats.follow || 0;
    tabs.value[5].count = stats.collect || 0;
  } catch (error) {
    console.error('加载未读统计失败:', error);
  }
};

/**
 * 加载消息列表
 */
const loadMessageList = async (refresh = false) => {
  if (loading.value || (!refresh && !hasMore.value)) {
    return;
  }

  try {
    loading.value = true;

    if (refresh) {
      page.value = 1;
      messageList.value = [];
      hasMore.value = true;
    }

    const response = await getNotificationList({
      page: page.value,
      size: 20,
      type: currentTab.value ? (currentTab.value as NotificationType) : undefined,
    });

    const newMessageList = response.data.list || [];

    if (refresh) {
      messageList.value = newMessageList;
    } else {
      messageList.value.push(...newMessageList);
    }

    hasMore.value = messageList.value.length < (response.data.total || 0);
    page.value++;
  } catch (error) {
    console.error('加载消息列表失败:', error);
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
 * 切换标签页
 */
const switchTab = (value: string) => {
  currentTab.value = value;
  loadMessageList(true);
};

/**
 * 获取消息图标
 */
const getMessageIcon = (type: NotificationType): string => {
  const iconMap = {
    [NotificationType.SYSTEM]: '📢',
    [NotificationType.LIKE]: '❤️',
    [NotificationType.COMMENT]: '💬',
    [NotificationType.FOLLOW]: '👤',
    [NotificationType.COLLECT]: '⭐',
  };
  return iconMap[type] || '📢';
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
 * 处理消息点击
 */
const handleMessageClick = async (message: Notification) => {
  try {
    // 标记为已读
    if (message.status === 'unread') {
      await markAsRead(message.id);
      message.status = 'read';
      // 更新未读统计
      await loadUnreadStats();
    }

    // 如果有链接，跳转到相应页面
    if (message.link) {
      uni.navigateTo({
        url: message.link,
      });
    }
  } catch (error) {
    console.error('处理消息失败:', error);
  }
};

/**
 * 全部标为已读
 */
const handleMarkAllRead = async () => {
  try {
    uni.showModal({
      title: '提示',
      content: '确定要将全部消息标为已读吗？',
      success: async (res) => {
        if (res.confirm) {
          await markAllAsRead(currentTab.value ? (currentTab.value as NotificationType) : undefined);
          // 重新加载列表和统计
          await Promise.all([loadMessageList(true), loadUnreadStats()]);
          uni.showToast({
            title: '操作成功',
            icon: 'success',
            duration: 1500,
          });
        }
      },
    });
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
 * 清空消息
 */
const handleClearAll = async () => {
  try {
    uni.showModal({
      title: '提示',
      content: '确定要清空所有消息吗？此操作不可恢复。',
      success: async (res) => {
        if (res.confirm) {
          await deleteAllNotifications(currentTab.value ? (currentTab.value as NotificationType) : undefined);
          // 重新加载列表和统计
          await Promise.all([loadMessageList(true), loadUnreadStats()]);
          uni.showToast({
            title: '已清空',
            icon: 'success',
            duration: 1500,
          });
        }
      },
    });
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
 * 下拉刷新
 */
const onPullDownRefresh = async () => {
  await Promise.all([loadMessageList(true), loadUnreadStats()]);
  uni.stopPullDownRefresh();
};

/**
 * 上拉加载更多
 */
const onReachBottom = () => {
  loadMessageList();
};

// 页面加载时获取数据
onMounted(() => {
  loadUnreadStats();
  loadMessageList(true);
});

// 导出给页面生命周期使用
defineExpose({
  onPullDownRefresh,
  onReachBottom,
});
</script>

<style lang="scss" scoped>
.message-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 180rpx;
}

.tabs {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  background-color: var(--bg-card);
  border-bottom: 1px solid var(--border-primary);
  padding: 0 $spacing-md;
  overflow-x: auto;

  .tab-item {
    position: relative;
    flex-shrink: 0;
    padding: $spacing-md $spacing-lg;
    font-size: $font-size-md;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all $transition-normal;

    &.active {
      color: var(--color-primary);
      font-weight: $font-weight-medium;

      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 40rpx;
        height: 4rpx;
        background-color: var(--color-primary);
        border-radius: 2rpx;
      }
    }

    .tab-badge {
      position: absolute;
      top: 8rpx;
      right: 8rpx;
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
  }
}

.message-list {
  .message-card {
    position: relative;
    display: flex;
    align-items: flex-start;
    margin-bottom: $spacing-md;
    padding: $spacing-lg;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-sm);
    transition: all $transition-normal;

    &.unread {
      background-color: var(--bg-secondary);
    }

    &:active {
      transform: translateY(-4rpx);
      box-shadow: var(--shadow-md);
    }

    .message-icon {
      font-size: 48rpx;
      margin-right: $spacing-md;
      flex-shrink: 0;
    }

    .message-content {
      flex: 1;
      min-width: 0;

      .message-title {
        font-size: $font-size-md;
        font-weight: $font-weight-medium;
        color: var(--text-primary);
        margin-bottom: $spacing-xs;
      }

      .message-text {
        font-size: $font-size-sm;
        line-height: 1.6;
        margin-bottom: $spacing-xs;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }

      .message-time {
        font-size: $font-size-xs;
      }
    }

    .unread-dot {
      width: 16rpx;
      height: 16rpx;
      background-color: #ff4444;
      border-radius: 50%;
      flex-shrink: 0;
      margin-left: $spacing-sm;
      margin-top: 8rpx;
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

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: $spacing-md;
  padding: $spacing-md;
  background-color: var(--bg-card);
  border-top: 1px solid var(--border-primary);
  box-shadow: var(--shadow-md);

  .action-btn {
    flex: 1;
    height: 80rpx;
    line-height: 80rpx;
    font-size: $font-size-md;
    color: var(--text-primary);
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-primary);
    border-radius: $border-radius-md;

    &:active {
      opacity: 0.8;
    }

    &.danger {
      color: var(--color-error);
      border-color: var(--color-error);
    }
  }
}
</style>
