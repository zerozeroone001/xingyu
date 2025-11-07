<template>
  <view class="index-page">
    <!-- 背景层 -->
    <view class="background-layer"></view>

    <view class="container">
      <!-- 顶部日期和天气信息 -->
      <view class="header-info">
        <view class="date-section">
          <view class="date-main">{{ dateInfo.date }}</view>
          <view class="date-sub">{{ dateInfo.weekDay }}</view>
        </view>
        <view class="weather-section">
          <view class="weather-icon">{{ weatherInfo.icon }}</view>
          <view class="weather-info">
            <view class="weather-temp">{{ weatherInfo.temperature }}°C</view>
            <view class="weather-text">{{ weatherInfo.weather }}</view>
          </view>
        </view>
      </view>

      <!-- 农历信息 -->
      <view class="lunar-section">
        <text class="lunar-text">{{ lunarInfo }}</text>
      </view>

      <!-- 每日一诗 - 居中显示 -->
      <view v-if="dailyPoetry" class="poetry-container" @click="goToDetail(dailyPoetry.id)">
        <view class="poetry-card">
          <view class="poetry-title">{{ dailyPoetry.title }}</view>
          <view class="poetry-author">
            {{ dailyPoetry.dynasty }} · {{ dailyPoetry.author_name }}
          </view>
          <view class="poetry-content">{{ dailyPoetry.content }}</view>
        </view>
      </view>

      <!-- 加载状态 -->
      <view v-else class="loading-container">
        <text class="loading-text">加载中...</text>
      </view>

      <!-- 底部操作区 -->
      <view class="bottom-actions">
        <view class="action-btn" @click="refreshPoetry">
          <text class="action-icon">🔄</text>
          <text class="action-text">换一首</text>
        </view>
        <view class="action-btn" @click="goToSearch">
          <text class="action-icon">🔍</text>
          <text class="action-text">搜索</text>
        </view>
        <view class="action-btn" @click="goToPoetryList">
          <text class="action-icon">📚</text>
          <text class="action-text">更多</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/store/modules/theme';
import { getHotPoetryList, getRandomPoetry, type Poetry } from '@/api/poetry';
import { getDailyRecommendations } from '@/api/recommendation';

const themeStore = useThemeStore();

const dailyPoetry = ref<Poetry | null>(null);
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);

/**
 * 加载每日推荐
 */
const loadDailyPoetry = async () => {
  try {
    const response = await getDailyRecommendations();
    if (response.data && response.data.length > 0) {
      dailyPoetry.value = response.data[0];
    } else {
      // 如果没有每日推荐，获取一个随机诗词
      const randomResponse = await getRandomPoetry();
      dailyPoetry.value = randomResponse.data;
    }
  } catch (error) {
    console.error('加载每日推荐失败:', error);
    // 失败时也尝试获取随机诗词
    try {
      const randomResponse = await getRandomPoetry();
      dailyPoetry.value = randomResponse.data;
    } catch (e) {
      console.error('加载随机诗词失败:', e);
    }
  }
};

/**
 * 刷新诗词 - 换一首
 */
const refreshPoetry = async () => {
  try {
    loading.value = true;

    if (refresh) {
      page.value = 1;
      poetryList.value = [];
      hasMore.value = true;
    }

    const response = await getHotPoetryList({
      page: page.value,
      size: 10,
    });

    const newPoetryList = response.data.items || [];

    if (refresh) {
      poetryList.value = newPoetryList;
    } else {
      poetryList.value.push(...newPoetryList);
    }

    hasMore.value = poetryList.value.length < (response.data.total || 0);
    page.value++;
  } catch (error) {
    console.error('加载诗词列表失败:', error);
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
 * 跳转到诗词详情
 */
const goToDetail = (id: number) => {
  if (typeof uni !== 'undefined') {
    uni.navigateTo({
      url: `/pages/poetry-detail/poetry-detail?id=${id}`,
    });
  }
};

/**
 * 跳转到搜索页
 */
const goToSearch = () => {
  if (typeof uni !== 'undefined') {
    uni.navigateTo({
      url: '/pages/search/search',
    });
  }
};

/**
 * 跳转到诗词列表
 */
const goToPoetryList = () => {
  if (typeof uni !== 'undefined') {
    uni.navigateTo({
      url: '/pages/poetry-list/poetry-list',
    });
  }
};

/**
 * 下拉刷新
 */
const onPullDownRefresh = async () => {
  await loadDailyPoetry();
  initDateWeather();
  if (typeof uni !== 'undefined') {
    uni.stopPullDownRefresh();
  }
};

// 页面加载时获取数据
onMounted(() => {
  initDateWeather();
  loadDailyPoetry();
});

// 导出给页面生命周期使用
defineExpose({
  onPullDownRefresh,
});
</script>

<style lang="scss" scoped>
.index-page {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

// 渐变背景层
.background-layer {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  animation: gradientShift 15s ease infinite;
  z-index: -1;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      45deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0.05) 50%,
      rgba(255, 255, 255, 0) 100%
    );
  }
}

@keyframes gradientShift {
  0%,
  100% {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  }
  25% {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #ffd3a5 100%);
  }
  50% {
    background: linear-gradient(135deg, #ffd3a5 0%, #fd6585 50%, #667eea 100%);
  }
  75% {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 50%, #667eea 100%);
  }
}

.container {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 60rpx 40rpx 40rpx;
  color: #ffffff;
}

// 顶部日期和天气
.header-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30rpx;
  animation: fadeInDown 0.8s ease;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.date-section {
  .date-main {
    font-size: 36rpx;
    font-weight: 500;
    margin-bottom: 8rpx;
    text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
  }

  .date-sub {
    font-size: 28rpx;
    opacity: 0.9;
    text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
  }
}

.weather-section {
  display: flex;
  align-items: center;
  gap: 16rpx;

  .weather-icon {
    font-size: 48rpx;
    filter: drop-shadow(0 2rpx 8rpx rgba(0, 0, 0, 0.2));
  }

  .weather-info {
    text-align: right;

    .weather-temp {
      font-size: 32rpx;
      font-weight: 500;
      text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
    }

    .weather-text {
      font-size: 24rpx;
      opacity: 0.9;
      text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
    }
  }
}

// 农历信息
.lunar-section {
  text-align: center;
  margin-bottom: 40rpx;
  animation: fadeIn 1s ease 0.2s both;

  .lunar-text {
    font-size: 28rpx;
    opacity: 0.95;
    text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
    letter-spacing: 2rpx;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

// 诗词容器 - 居中显示
.poetry-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40rpx 0;
  animation: fadeInUp 1s ease 0.4s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(50rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.poetry-card {
  width: 100%;
  max-width: 600rpx;
  padding: 80rpx 60rpx;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20rpx);
  border-radius: 32rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 16rpx 64rpx rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  cursor: pointer;

  &:active {
    transform: scale(0.98);
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.3);
  }

  .poetry-title {
    font-size: 48rpx;
    font-weight: 600;
    text-align: center;
    margin-bottom: 24rpx;
    letter-spacing: 4rpx;
    text-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.3);
    line-height: 1.4;
  }

  .poetry-author {
    font-size: 28rpx;
    text-align: center;
    margin-bottom: 60rpx;
    opacity: 0.9;
    text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
    letter-spacing: 2rpx;
  }

  .poetry-content {
    font-size: 32rpx;
    line-height: 2;
    text-align: center;
    white-space: pre-wrap;
    text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
    letter-spacing: 2rpx;
    word-break: keep-all;
  }
}

// 加载状态
.loading-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;

  .loading-text {
    font-size: 32rpx;
    opacity: 0.8;
    text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
  }
}

// 底部操作区
.bottom-actions {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 40rpx 0 20rpx;
  animation: fadeInUp 1s ease 0.6s both;

  .action-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12rpx;
    padding: 20rpx 40rpx;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10rpx);
    border-radius: 20rpx;
    border: 1rpx solid rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
    cursor: pointer;

    &:active {
      transform: scale(0.95);
      background: rgba(255, 255, 255, 0.3);
    }

    .action-icon {
      font-size: 40rpx;
      filter: drop-shadow(0 2rpx 8rpx rgba(0, 0, 0, 0.2));
    }

    .action-text {
      font-size: 24rpx;
      opacity: 0.95;
      text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
    }
  }
}
</style>
