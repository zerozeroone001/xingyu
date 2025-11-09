<template>
  <div class="index-page">
    <!-- 背景层 -->
    <div class="background-layer"></div>

    <div class="container">
      

      <!-- 日期和天气信息 -->
      <div class="header-info">
        <div class="date-section">
          <div class="date-main">{{ dateInfo.date }}</div>
          <div class="date-sub">{{ dateInfo.weekDay }}</div>
        </div>
        <div class="weather-section">
          <div class="weather-icon">{{ weatherInfo.icon }}</div>
          <div class="weather-info">
            <div class="weather-temp">{{ weatherInfo.temperature }}°C</div>
            <div class="weather-text">{{ weatherInfo.weather }}</div>
          </div>
        </div>
      </div>

      <!-- 顶部搜索框 -->
      <!-- <div class="search-bar" @click="goToSearch">
        <span class="search-icon">⌕</span>
        <span class="search-placeholder">搜索诗词、作者...</span>
      </div> -->

      <!-- 农历信息 -->
      <div class="lunar-section">
        <span class="lunar-text">{{ lunarInfo }}</span>
      </div>

      <!-- 每日一诗 - 支持左右滑动 -->
      <div
        v-if="dailyPoetry"
        class="poetry-container"
        @touchstart="handleTouchStart"
        @touchmove="handleTouchMove"
        @touchend="handleTouchEnd"
        @click="goToDetail(dailyPoetry.id)"
      >
        <div class="poetry-card">
          <div class="poetry-title">{{ dailyPoetry.title }}</div>
          <div class="poetry-author">
            {{ dailyPoetry.dynasty }} · {{ dailyPoetry.author_name }}
          </div>
          <div class="poetry-content">{{ dailyPoetry.content }}</div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-else class="loading-container">
        <span class="loading-text">加载中...</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { getRandomPoetry, type Poetry } from '@/api/poetry';
import { getDailyRecommendations } from '@/api/recommendation';
import { solar2lunar, getWeekDay, formatDate } from '@/utils/lunar';
import { getMockWeather, getWeatherPoetry } from '@/utils/weather';

// 模拟诗词数据（作为后备）
const mockPoetryList: Poetry[] = [
  {
    id: 1,
    title: '静夜思',
    author_name: '李白',
    dynasty: '唐代',
    content: '床前明月光，疑是地上霜。\n举头望明月，低头思故乡。',
    author_id: 1,
    likes_count: 1000,
    collects_count: 800,
    comments_count: 200,
  },
  {
    id: 2,
    title: '登鹳雀楼',
    author_name: '王之涣',
    dynasty: '唐代',
    content: '白日依山尽，黄河入海流。\n欲穷千里目，更上一层楼。',
    author_id: 2,
    likes_count: 900,
    collects_count: 700,
    comments_count: 150,
  },
  {
    id: 3,
    title: '春晓',
    author_name: '孟浩然',
    dynasty: '唐代',
    content: '春眠不觉晓，处处闻啼鸟。\n夜来风雨声，花落知多少。',
    author_id: 3,
    likes_count: 950,
    collects_count: 750,
    comments_count: 180,
  },
  {
    id: 4,
    title: '望庐山瀑布',
    author_name: '李白',
    dynasty: '唐代',
    content: '日照香炉生紫烟，遥看瀑布挂前川。\n飞流直下三千尺，疑是银河落九天。',
    author_id: 1,
    likes_count: 1100,
    collects_count: 850,
    comments_count: 220,
  },
  {
    id: 5,
    title: '江雪',
    author_name: '柳宗元',
    dynasty: '唐代',
    content: '千山鸟飞绝，万径人踪灭。\n孤舟蓑笠翁，独钓寒江雪。',
    author_id: 4,
    likes_count: 880,
    collects_count: 680,
    comments_count: 160,
  },
];

// ========== 工具函数（在响应式数据之前）==========
/**
 * 获取随机模拟诗词
 */
function getRandomMockPoetry(): Poetry {
  const now = new Date();
  const seed = now.getFullYear() * 10000 + (now.getMonth() + 1) * 100 + now.getDate();
  const index = seed % mockPoetryList.length;
  return mockPoetryList[index];
}

// ========== 响应式数据定义 ==========
// 是否使用 mock 数据（开发环境下默认使用）
const useMockData = true;

const dailyPoetry = ref<Poetry | null>(null);
const loading = ref(false);
const page = ref(1);
const hasMore = ref(true);
const poetryList = ref<Poetry[]>([]);

// 日期和天气信息
const dateInfo = ref({
  date: '',
  weekDay: '',
});

const weatherInfo = ref({
  icon: '☀️',
  temperature: 22,
  weather: '晴',
});

const lunarInfo = ref('农历甲辰年 冬月初七');

// 触摸滑动相关
const touchStartX = ref(0);
const touchEndX = ref(0);

/**
 * 处理触摸开始
 */
const handleTouchStart = (e: TouchEvent) => {
  touchStartX.value = e.touches[0].clientX;
};

/**
 * 处理触摸移动
 */
const handleTouchMove = (e: TouchEvent) => {
  touchEndX.value = e.touches[0].clientX;
};

/**
 * 处理触摸结束
 */
const handleTouchEnd = async () => {
  const swipeDistance = touchStartX.value - touchEndX.value;
  const minSwipeDistance = 50; // 最小滑动距离

  if (Math.abs(swipeDistance) > minSwipeDistance) {
    // 左滑或右滑都换一首
    await refreshPoetry();
  }
};

/**
 * 初始化日期和天气信息
 */
const initDateWeather = () => {
  const now = new Date();
  const lunarDate = solar2lunar(now);

  dateInfo.value = {
    date: formatDate(now),
    weekDay: getWeekDay(now),
  };

  // 获取模拟天气信息
  const weather = getMockWeather();
  weatherInfo.value = {
    icon: weather.icon,
    temperature: weather.temperature,
    weather: weather.weather,
  };

  // 获取农历信息
  lunarInfo.value = `${lunarDate.yearCn} ${lunarDate.monthCn}${lunarDate.dayCn}`;
};

// ========== API 调用函数 ==========
/**
 * 加载每日推荐
 */
const loadDailyPoetry = async () => {
  if (useMockData) {
    // 使用 mock 数据，随机选择一首诗
    const randomIndex = Math.floor(Math.random() * mockPoetryList.length);
    dailyPoetry.value = mockPoetryList[randomIndex];
    return;
  }

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
      // 所有 API 都失败，使用模拟数据
      dailyPoetry.value = getRandomMockPoetry();
      console.log('使用模拟数据:', dailyPoetry.value);
    }
  }
};

/**
 * 刷新诗词 - 换一首
 */
const refreshPoetry = async () => {
  try {
    loading.value = true;
    const response = await getRandomPoetry();
    dailyPoetry.value = response.data;

    if (typeof uni !== 'undefined') {
      uni.showToast({
        title: '已换一首',
        icon: 'success',
        duration: 1500,
      });
    }
  } catch (error) {
    console.error('刷新诗词失败:', error);
    if (typeof uni !== 'undefined') {
      uni.showToast({
        title: '换一首失败',
        icon: 'none',
        duration: 2000,
      });
    }
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
  console.log('首页挂载，开始初始化...');

  // 先设置模拟诗词，确保页面立即有内容
  dailyPoetry.value = getRandomMockPoetry();
  console.log('设置初始模拟诗词:', dailyPoetry.value);

  // 初始化日期和天气
  initDateWeather();
  console.log('日期信息:', dateInfo.value);
  console.log('天气信息:', weatherInfo.value);
  console.log('农历信息:', lunarInfo.value);

  // 然后尝试从 API 加载
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
  // height: 100vh;
  overflow: hidden;
}

// 渐变背景层
.background-layer {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 50%, #ffecd2 100%);
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
      rgba(255, 255, 255, 0.3) 0%,
      rgba(255, 255, 255, 0.15) 50%,
      rgba(255, 255, 255, 0) 100%
    );
  }
}

@keyframes gradientShift {
  0%,
  100% {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 50%, #ffecd2 100%);
  }
  25% {
    background: linear-gradient(135deg, #ffd3a5 0%, #ffeaa7 50%, #fdcb6e 100%);
  }
  50% {
    background: linear-gradient(135deg, #a29bfe 0%, #fab1a0 50%, #ffeaa7 100%);
  }
  75% {
    background: linear-gradient(135deg, #fdcb6e 0%, #ffecd2 50%, #fab1a0 100%);
  }
}

.container {
  position: relative;
  // height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px;
  color: #2c3e50;
  overflow: hidden;
}

// 搜索框
.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .search-icon {
    font-size: 18px;
    color: #666;
  }

  .search-placeholder {
    flex: 1;
    font-size: 14px;
    color: #999;
  }
}

// 顶部日期和天气
.header-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
  animation: fadeInDown 0.8s ease;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.date-section {
  .date-main {
    font-size: 18px;
    font-weight: 500;
    margin-bottom: 4px;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  }

  .date-sub {
    font-size: 14px;
    opacity: 0.9;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  }
}

.weather-section {
  display: flex;
  align-items: center;
  gap: 8px;

  .weather-icon {
    font-size: 24px;
    filter: drop-shadow(0 1px 4px rgba(0, 0, 0, 0.2));
  }

  .weather-info {
    text-align: right;

    .weather-temp {
      font-size: 16px;
      font-weight: 500;
      text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
    }

    .weather-text {
      font-size: 12px;
      opacity: 0.9;
      text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
    }
  }
}

// 农历信息
.lunar-section {
  text-align: center;
  margin-bottom: 20px;
  animation: fadeIn 1s ease 0.2s both;

  .lunar-text {
    font-size: 14px;
    opacity: 0.95;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
    letter-spacing: 1px;
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
  padding: 20px 0;
  animation: fadeInUp 1s ease 0.4s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(25px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.poetry-card {
  width: 100%;
  max-width: 300px;
  padding: 40px 30px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;

  &:active {
    transform: scale(0.98);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  }

  .poetry-title {
    font-size: 24px;
    font-weight: 600;
    text-align: center;
    margin-bottom: 12px;
    letter-spacing: 2px;
    text-shadow: 0 1px 6px rgba(0, 0, 0, 0.3);
    line-height: 1.4;
  }

  .poetry-author {
    font-size: 14px;
    text-align: center;
    margin-bottom: 30px;
    opacity: 0.9;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
    letter-spacing: 1px;
  }

  .poetry-content {
    font-size: 16px;
    line-height: 2;
    text-align: center;
    white-space: pre-wrap;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
    letter-spacing: 1px;
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
    font-size: 16px;
    opacity: 0.8;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  }
}
</style>
