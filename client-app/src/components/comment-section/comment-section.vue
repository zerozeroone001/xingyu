<template>
  <view class="comment-section" :class="themeClass">
    <!-- 评论标题 -->
    <view class="section-header">
      <text class="section-title">💬 评论 ({{ total }})</text>
      <text v-if="sortBy === 'hot'" class="sort-btn" @click="sortBy = 'time'">最新</text>
      <text v-else class="sort-btn" @click="sortBy = 'hot'">最热</text>
    </view>

    <!-- 评论输入框 -->
    <view class="comment-input theme-card">
      <textarea
        v-model="newComment"
        class="input-box"
        :placeholder="replyTo ? `回复 @${replyTo.user_name}` : '写下你的评论...'"
        :maxlength="500"
        :auto-height="true"
      />
      <view class="input-footer">
        <text class="char-count theme-text-tertiary">{{ newComment.length }}/500</text>
        <button
          class="submit-btn"
          :class="{ disabled: !canSubmit }"
          :disabled="!canSubmit"
          @click="handleSubmit"
        >
          {{ submitting ? '发送中...' : '发送' }}
        </button>
      </view>
    </view>

    <!-- 评论列表 -->
    <view v-if="commentList.length > 0" class="comment-list">
      <view
        v-for="comment in commentList"
        :key="comment.id"
        class="comment-item theme-card"
      >
        <!-- 评论头部 -->
        <view class="comment-header">
          <image
            v-if="comment.user_avatar"
            class="avatar"
            :src="comment.user_avatar"
            mode="aspectFill"
          />
          <view v-else class="avatar-placeholder">
            {{ comment.user_name?.charAt(0) }}
          </view>

          <view class="user-info">
            <view class="username">{{ comment.user_name }}</view>
            <view class="time theme-text-tertiary">{{ formatTime(comment.created_at) }}</view>
          </view>
        </view>

        <!-- 评论内容 -->
        <view class="comment-content">{{ comment.content }}</view>

        <!-- 评论操作 -->
        <view class="comment-actions">
          <view class="action-item" @click="handleReply(comment)">
            <text class="icon">💬</text>
            <text class="label">回复</text>
            <text v-if="comment.replies_count > 0" class="count">{{ comment.replies_count }}</text>
          </view>
          <view class="action-item" @click="handleLike(comment)">
            <text class="icon">{{ comment.is_liked ? '❤️' : '🤍' }}</text>
            <text class="label">{{ comment.likes_count || 0 }}</text>
          </view>
        </view>

        <!-- 回复列表 -->
        <view v-if="comment.replies && comment.replies.length > 0" class="replies-list">
          <view
            v-for="reply in comment.replies"
            :key="reply.id"
            class="reply-item"
          >
            <view class="reply-header">
              <text class="reply-user">{{ reply.user_name }}</text>
              <text class="theme-text-tertiary reply-time">{{ formatTime(reply.created_at) }}</text>
            </view>
            <view class="reply-content">{{ reply.content }}</view>
          </view>

          <!-- 查看更多回复 -->
          <view
            v-if="comment.replies_count > comment.replies.length"
            class="load-more-replies"
            @click="loadReplies(comment)"
          >
            查看更多回复 ({{ comment.replies_count - comment.replies.length }})
          </view>
        </view>

        <!-- 加载更多回复按钮 -->
        <view
          v-else-if="comment.replies_count > 0"
          class="load-replies-btn"
          @click="loadReplies(comment)"
        >
          查看 {{ comment.replies_count }} 条回复
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view v-else-if="!loading" class="empty-box">
      <text class="empty-icon">💭</text>
      <text class="empty-text">暂无评论，快来抢沙发吧~</text>
    </view>

    <!-- 加载中 -->
    <view v-if="loading && commentList.length === 0" class="loading-box">
      <text class="loading-text">加载中...</text>
    </view>

    <!-- 加载更多 -->
    <view v-if="commentList.length > 0 && hasMore" class="load-more">
      <text v-if="loading" class="load-more-text">加载中...</text>
      <text v-else class="load-more-text" @click="loadComments()">加载更多</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import {
  getPoetryCommentList,
  getPostCommentList,
  getCommentReplies,
  createComment,
  type Comment,
} from '@/api/comment';

interface Props {
  poetryId?: number;
  postId?: number;
  themeClass?: string;
}

const props = withDefaults(defineProps<Props>(), {
  themeClass: '',
});

const commentList = ref<Comment[]>([]);
const newComment = ref('');
const replyTo = ref<Comment | null>(null);
const loading = ref(false);
const submitting = ref(false);
const page = ref(1);
const hasMore = ref(true);
const total = ref(0);
const sortBy = ref<'hot' | 'time'>('hot');

/**
 * 是否可以提交
 */
const canSubmit = computed(() => {
  return newComment.value.trim().length > 0 && !submitting.value;
});

/**
 * 加载评论列表
 */
const loadComments = async (refresh = false) => {
  if (loading.value || (!refresh && !hasMore.value)) {
    return;
  }

  if (!props.poetryId && !props.postId) {
    console.error('poetryId 或 postId 必须提供其中之一');
    return;
  }

  try {
    loading.value = true;

    if (refresh) {
      page.value = 1;
      commentList.value = [];
      hasMore.value = true;
    }

    const params = {
      page: page.value,
      size: 10,
      sort_by: sortBy.value === 'hot' ? 'likes_count' : 'created_at',
      order: 'desc' as const,
    };

    const response = props.poetryId
      ? await getPoetryCommentList(props.poetryId, params)
      : await getPostCommentList(props.postId!, params);

    const newComments = response.data.items || [];
    total.value = response.data.total || 0;

    if (refresh) {
      commentList.value = newComments;
    } else {
      commentList.value.push(...newComments);
    }

    hasMore.value = commentList.value.length < total.value;
    page.value++;
  } catch (error) {
    console.error('加载评论失败:', error);
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
 * 加载回复列表
 */
const loadReplies = async (comment: Comment) => {
  try {
    const response = await getCommentReplies(comment.id, {
      page: 1,
      size: 10,
    });

    comment.replies = response.data.items || [];
  } catch (error) {
    console.error('加载回复失败:', error);
  }
};

/**
 * 提交评论
 */
const handleSubmit = async () => {
  if (!canSubmit.value) return;

  try {
    submitting.value = true;

    await createComment({
      poetry_id: props.poetryId,
      post_id: props.postId,
      content: newComment.value.trim(),
      parent_id: replyTo.value?.id,
    });

    // 清空输入
    newComment.value = '';
    replyTo.value = null;

    // 刷新评论列表
    await loadComments(true);

    uni.showToast({
      title: '评论成功',
      icon: 'success',
      duration: 1500,
    });
  } catch (error) {
    console.error('评论失败:', error);
    uni.showToast({
      title: '评论失败',
      icon: 'none',
      duration: 2000,
    });
  } finally {
    submitting.value = false;
  }
};

/**
 * 回复评论
 */
const handleReply = (comment: Comment) => {
  replyTo.value = comment;
  // 可以滚动到输入框
};

/**
 * 点赞评论
 */
const handleLike = async (comment: Comment) => {
  // TODO: 实现评论点赞功能
  uni.showToast({
    title: '功能开发中',
    icon: 'none',
    duration: 2000,
  });
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

// 监听排序方式变化
watch(sortBy, () => {
  loadComments(true);
});

// 页面加载时获取评论
onMounted(() => {
  loadComments(true);
});

// 暴露给父组件的方法
defineExpose({
  refresh: () => loadComments(true),
});
</script>

<style lang="scss" scoped>
.comment-section {
  padding: $spacing-lg 0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: $spacing-lg;
  padding: 0 $spacing-md;

  .section-title {
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    color: var(--text-primary);
  }

  .sort-btn {
    font-size: $font-size-sm;
    color: var(--color-primary);
    cursor: pointer;

    &:active {
      opacity: 0.7;
    }
  }
}

.comment-input {
  margin: 0 $spacing-md $spacing-lg;
  padding: $spacing-lg;
  background-color: var(--bg-card);
  border-radius: $border-radius-lg;
  box-shadow: var(--shadow-sm);

  .input-box {
    width: 100%;
    min-height: 100rpx;
    font-size: $font-size-md;
    line-height: 1.6;
    color: var(--text-primary);
    margin-bottom: $spacing-md;
  }

  .input-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .char-count {
      font-size: $font-size-xs;
    }

    .submit-btn {
      padding: 8rpx 32rpx;
      font-size: $font-size-sm;
      color: #ffffff;
      background-color: var(--color-primary);
      border: none;
      border-radius: $border-radius-md;

      &:active {
        opacity: 0.8;
      }

      &.disabled {
        opacity: 0.5;
      }
    }
  }
}

.comment-list {
  padding: 0 $spacing-md;

  .comment-item {
    margin-bottom: $spacing-lg;
    padding: $spacing-lg;
    background-color: var(--bg-card);
    border-radius: $border-radius-lg;
    box-shadow: var(--shadow-sm);

    .comment-header {
      display: flex;
      align-items: center;
      margin-bottom: $spacing-md;

      .avatar,
      .avatar-placeholder {
        width: 60rpx;
        height: 60rpx;
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
        font-size: $font-size-md;
        font-weight: $font-weight-bold;
      }

      .user-info {
        flex: 1;

        .username {
          font-size: $font-size-md;
          font-weight: $font-weight-medium;
          color: var(--text-primary);
          margin-bottom: 4rpx;
        }

        .time {
          font-size: $font-size-xs;
        }
      }
    }

    .comment-content {
      font-size: $font-size-md;
      line-height: 1.6;
      color: var(--text-primary);
      margin-bottom: $spacing-md;
      white-space: pre-wrap;
    }

    .comment-actions {
      display: flex;
      align-items: center;
      gap: $spacing-xl;

      .action-item {
        display: flex;
        align-items: center;
        gap: $spacing-xs;
        cursor: pointer;

        &:active {
          opacity: 0.7;
        }

        .icon {
          font-size: 28rpx;
        }

        .label {
          font-size: $font-size-sm;
          color: var(--text-secondary);
        }

        .count {
          font-size: $font-size-sm;
          color: var(--text-tertiary);
        }
      }
    }

    .replies-list {
      margin-top: $spacing-md;
      padding: $spacing-md;
      background-color: var(--bg-secondary);
      border-radius: $border-radius-md;

      .reply-item {
        margin-bottom: $spacing-md;

        &:last-child {
          margin-bottom: 0;
        }

        .reply-header {
          display: flex;
          align-items: center;
          gap: $spacing-sm;
          margin-bottom: 4rpx;

          .reply-user {
            font-size: $font-size-sm;
            font-weight: $font-weight-medium;
            color: var(--text-primary);
          }

          .reply-time {
            font-size: $font-size-xs;
          }
        }

        .reply-content {
          font-size: $font-size-sm;
          line-height: 1.5;
          color: var(--text-primary);
        }
      }

      .load-more-replies {
        font-size: $font-size-sm;
        color: var(--color-primary);
        text-align: center;
        padding: $spacing-sm 0;
        cursor: pointer;

        &:active {
          opacity: 0.7;
        }
      }
    }

    .load-replies-btn {
      margin-top: $spacing-md;
      padding: $spacing-sm;
      font-size: $font-size-sm;
      color: var(--color-primary);
      text-align: center;
      background-color: var(--bg-secondary);
      border-radius: $border-radius-md;
      cursor: pointer;

      &:active {
        opacity: 0.7;
      }
    }
  }
}

.empty-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx $spacing-xl;

  .empty-icon {
    font-size: 100rpx;
    margin-bottom: $spacing-md;
    opacity: 0.5;
  }

  .empty-text {
    font-size: $font-size-md;
    color: var(--text-secondary);
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
    color: var(--color-primary);
    cursor: pointer;

    &:active {
      opacity: 0.7;
    }
  }
}
</style>
