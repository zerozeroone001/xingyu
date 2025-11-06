<template>
  <view class="poetry-detail-page" :class="themeStore.themeClass">
    <view v-if="loading" class="loading-box">
      <text class="loading-text">加载中...</text>
    </view>

    <view v-else-if="!poetry" class="error-box">
      <text class="error-text">诗词不存在或已删除</text>
      <button class="back-btn" @click="goBack">返回</button>
    </view>

    <view v-else class="container">
      <!-- 诗词头部 -->
      <view class="poetry-header theme-card">
        <view class="poetry-title">{{ poetry.title }}</view>
        <view class="poetry-meta">
          <text class="dynasty">{{ poetry.dynasty }}</text>
          <text class="separator">·</text>
          <text class="author" @click="goToAuthor">{{ poetry.author_name }}</text>
        </view>
      </view>

      <!-- 诗词内容 -->
      <view class="poetry-content theme-card">
        <view class="content-text">{{ poetry.content }}</view>
      </view>

      <!-- 翻译 -->
      <view v-if="poetry.translation" class="poetry-section theme-card">
        <view class="section-title">📖 译文</view>
        <view class="section-content">{{ poetry.translation }}</view>
      </view>

      <!-- 注释 -->
      <view v-if="poetry.annotation" class="poetry-section theme-card">
        <view class="section-title">📝 注释</view>
        <view class="section-content">{{ poetry.annotation }}</view>
      </view>

      <!-- 赏析 -->
      <view v-if="poetry.appreciation" class="poetry-section theme-card">
        <view class="section-title">✨ 赏析</view>
        <view class="section-content">{{ poetry.appreciation }}</view>
      </view>

      <!-- 互动按钮 -->
      <view class="action-bar theme-card">
        <view class="action-item" @click="handleLike">
          <text class="icon" :class="{ active: isLiked }">{{ isLiked ? '❤️' : '🤍' }}</text>
          <text class="label">{{ isLiked ? '已点赞' : '点赞' }}</text>
          <text class="count">{{ poetry.likes_count }}</text>
        </view>
        <view class="action-item" @click="handleCollect">
          <text class="icon" :class="{ active: isCollected }">{{ isCollected ? '⭐' : '☆' }}</text>
          <text class="label">{{ isCollected ? '已收藏' : '收藏' }}</text>
          <text class="count">{{ poetry.collects_count }}</text>
        </view>
        <view class="action-item" @click="scrollToComments">
          <text class="icon">💬</text>
          <text class="label">评论</text>
          <text class="count">{{ poetry.comments_count }}</text>
        </view>
        <view class="action-item" @click="handleShare">
          <text class="icon">📤</text>
          <text class="label">分享</text>
        </view>
      </view>

      <!-- 统计信息 -->
      <view class="stats-bar theme-card">
        <view class="stat-item">
          <text class="stat-value">{{ poetry.views_count }}</text>
          <text class="stat-label">阅读</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">{{ poetry.likes_count }}</text>
          <text class="stat-label">点赞</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">{{ poetry.collects_count }}</text>
          <text class="stat-label">收藏</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">{{ poetry.comments_count }}</text>
          <text class="stat-label">评论</text>
        </view>
      </view>

      <!-- 评论区占位 -->
      <view class="comments-section">
        <view class="section-header">
          <text class="section-title">💬 评论 ({{ poetry.comments_count }})</text>
        </view>
        <view class="comments-placeholder theme-card">
          <text class="placeholder-text">评论功能开发中...</text>
        </view>
      </view>

      <!-- 相似推荐 -->
      <view v-if="similarPoetry.length > 0" class="similar-section">
        <view class="section-header">
          <text class="section-title">📚 相似推荐</text>
        </view>
        <view class="similar-list">
          <view
            v-for="item in similarPoetry"
            :key="item.id"
            class="similar-item theme-card"
            @click="goToDetail(item.id)"
          >
            <view class="similar-title">{{ item.title }}</view>
            <view class="similar-author theme-text-tertiary">
              {{ item.dynasty }} · {{ item.author_name }}
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { useUserStore } from '@/store/modules/user';
import {
  getPoetryDetail,
  likePoetry,
  unlikePoetry,
  collectPoetry,
  uncollectPoetry,
  checkLikeStatus,
  checkCollectStatus,
  type Poetry,
} from '@/api/poetry';
import { getSimilarPoetry } from '@/api/recommendation';

const themeStore = useThemeStore();
const userStore = useUserStore();

// 从 URL 获取诗词 ID
const poetryId = ref<number>(0);
const poetry = ref<Poetry | null>(null);
const loading = ref(true);
const isLiked = ref(false);
const isCollected = ref(false);
const similarPoetry = ref<Poetry[]>([]);

/**
 * 获取 URL 参数
 */
const getQueryParam = (name: string): string => {
  const search = window.location.search;
  const params = new URLSearchParams(search);
  return params.get(name) || '';
};

/**
 * 加载诗词详情
 */
const loadPoetryDetail = async () => {
  try {
    loading.value = true;

    const response = await getPoetryDetail(poetryId.value);
    poetry.value = response.data;

    // 加载点赞和收藏状态
    if (userStore.isLoggedIn) {
      loadInteractionStatus();
    }

    // 加载相似推荐
    loadSimilarPoetry();
  } catch (error) {
    console.error('加载诗词详情失败:', error);
  } finally {
    loading.value = false;
  }
};

/**
 * 加载互动状态
 */
const loadInteractionStatus = async () => {
  try {
    const [likeRes, collectRes] = await Promise.all([
      checkLikeStatus(poetryId.value),
      checkCollectStatus(poetryId.value),
    ]);

    isLiked.value = likeRes.data.liked;
    isCollected.value = collectRes.data.collected;
  } catch (error) {
    console.error('加载互动状态失败:', error);
  }
};

/**
 * 加载相似诗词
 */
const loadSimilarPoetry = async () => {
  try {
    const response = await getSimilarPoetry(poetryId.value, 5);
    similarPoetry.value = response.data || [];
  } catch (error) {
    console.error('加载相似诗词失败:', error);
  }
};

/**
 * 处理点赞
 */
const handleLike = async () => {
  if (!userStore.checkLoginStatus()) {
    return;
  }

  try {
    if (isLiked.value) {
      await unlikePoetry(poetryId.value);
      isLiked.value = false;
      if (poetry.value) {
        poetry.value.likes_count--;
      }
    } else {
      await likePoetry(poetryId.value);
      isLiked.value = true;
      if (poetry.value) {
        poetry.value.likes_count++;
      }
    }
  } catch (error) {
    console.error('点赞操作失败:', error);
  }
};

/**
 * 处理收藏
 */
const handleCollect = async () => {
  if (!userStore.checkLoginStatus()) {
    return;
  }

  try {
    if (isCollected.value) {
      await uncollectPoetry(poetryId.value);
      isCollected.value = false;
      if (poetry.value) {
        poetry.value.collects_count--;
      }
    } else {
      await collectPoetry(poetryId.value);
      isCollected.value = true;
      if (poetry.value) {
        poetry.value.collects_count++;
      }
    }
  } catch (error) {
    console.error('收藏操作失败:', error);
  }
};

/**
 * 处理分享
 */
const handleShare = () => {
  alert('分享功能开发中...');
};

/**
 * 滚动到评论区
 */
const scrollToComments = () => {
  const commentsSection = document.querySelector('.comments-section');
  if (commentsSection) {
    commentsSection.scrollIntoView({ behavior: 'smooth' });
  }
};

/**
 * 跳转到作者详情
 */
const goToAuthor = () => {
  if (poetry.value) {
    window.location.href = `/pages/author-detail/author-detail?id=${poetry.value.author_id}`;
  }
};

/**
 * 跳转到其他诗词详情
 */
const goToDetail = (id: number) => {
  window.location.href = `/pages/poetry-detail/poetry-detail?id=${id}`;
};

/**
 * 返回上一页
 */
const goBack = () => {
  window.history.back();
};

onMounted(() => {
  const id = getQueryParam('id');
  if (id) {
    poetryId.value = parseInt(id);
    loadPoetryDetail();
  } else {
    loading.value = false;
  }
});
</script>

<style lang="scss" scoped>
.poetry-detail-page {
  min-height: 100vh;
  background-color: var(--bg-primary);
  padding-bottom: 40rpx;
}

.container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.loading-box,
.error-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  text-align: center;

  .loading-text,
  .error-text {
    font-size: 16px;
    color: var(--text-tertiary);
    margin-bottom: 20px;
  }

  .back-btn {
    padding: 10px 24px;
    background-color: var(--color-primary);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
}

.poetry-header {
  padding: 32px;
  margin-bottom: 20px;
  text-align: center;
  background-color: var(--bg-card);
  border-radius: 16px;
  box-shadow: var(--shadow-md);

  .poetry-title {
    font-size: 32px;
    font-weight: bold;
    color: var(--text-primary);
    margin-bottom: 16px;
  }

  .poetry-meta {
    font-size: 14px;
    color: var(--text-secondary);

    .separator {
      margin: 0 8px;
    }

    .author {
      cursor: pointer;
      color: var(--color-primary);

      &:hover {
        text-decoration: underline;
      }
    }
  }
}

.poetry-content {
  padding: 32px;
  margin-bottom: 20px;
  background-color: var(--bg-card);
  border-radius: 16px;
  box-shadow: var(--shadow-sm);

  .content-text {
    font-size: 18px;
    line-height: 2;
    color: var(--text-primary);
    white-space: pre-wrap;
    text-align: justify;
  }
}

.poetry-section {
  padding: 24px;
  margin-bottom: 20px;
  background-color: var(--bg-card);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);

  .section-title {
    font-size: 18px;
    font-weight: bold;
    color: var(--text-primary);
    margin-bottom: 16px;
  }

  .section-content {
    font-size: 15px;
    line-height: 1.8;
    color: var(--text-secondary);
    white-space: pre-wrap;
  }
}

.action-bar {
  display: flex;
  justify-content: space-around;
  padding: 20px;
  margin-bottom: 20px;
  background-color: var(--bg-card);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);

  .action-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s;

    &:active {
      transform: scale(0.95);
    }

    .icon {
      font-size: 32px;
      margin-bottom: 8px;
      transition: all 0.3s;

      &.active {
        transform: scale(1.2);
      }
    }

    .label {
      font-size: 13px;
      color: var(--text-secondary);
      margin-bottom: 4px;
    }

    .count {
      font-size: 12px;
      color: var(--text-tertiary);
    }
  }
}

.stats-bar {
  display: flex;
  justify-content: space-around;
  padding: 20px;
  margin-bottom: 20px;
  background-color: var(--bg-card);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;

    .stat-value {
      font-size: 24px;
      font-weight: bold;
      color: var(--text-primary);
      margin-bottom: 4px;
    }

    .stat-label {
      font-size: 13px;
      color: var(--text-tertiary);
    }
  }
}

.comments-section,
.similar-section {
  margin-bottom: 20px;

  .section-header {
    margin-bottom: 16px;

    .section-title {
      font-size: 18px;
      font-weight: bold;
      color: var(--text-primary);
    }
  }
}

.comments-placeholder {
  padding: 40px;
  text-align: center;
  background-color: var(--bg-card);
  border-radius: 12px;

  .placeholder-text {
    font-size: 14px;
    color: var(--text-tertiary);
  }
}

.similar-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;

  .similar-item {
    padding: 16px;
    background-color: var(--bg-card);
    border-radius: 12px;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-md);
    }

    .similar-title {
      font-size: 16px;
      font-weight: 500;
      color: var(--text-primary);
      margin-bottom: 8px;
    }

    .similar-author {
      font-size: 13px;
    }
  }
}
</style>
