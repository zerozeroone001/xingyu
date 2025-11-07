/**
 * 天气工具
 * 提供模拟天气数据
 */

export interface WeatherInfo {
  temperature: number; // 温度
  weather: string; // 天气状况
  icon: string; // 天气图标
  city: string; // 城市
}

/**
 * 天气类型配置
 */
const weatherTypes = [
  { weather: '晴', icon: '☀️', temp: [20, 28] },
  { weather: '多云', icon: '⛅', temp: [18, 25] },
  { weather: '阴', icon: '☁️', temp: [15, 22] },
  { weather: '小雨', icon: '🌧️', temp: [12, 18] },
  { weather: '雨', icon: '🌧️', temp: [10, 16] },
  { weather: '雪', icon: '❄️', temp: [-5, 5] },
];

/**
 * 城市列表
 */
const cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '西安', '南京'];

/**
 * 根据日期获取稳定的随机数
 */
function getSeededRandom(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

/**
 * 获取模拟天气数据
 * 根据当天日期生成，同一天返回相同数据
 */
export function getMockWeather(): WeatherInfo {
  const now = new Date();
  const seed = now.getFullYear() * 10000 + (now.getMonth() + 1) * 100 + now.getDate();

  // 获取当前月份，用于调整温度范围
  const month = now.getMonth() + 1;
  let tempOffset = 0;

  // 根据季节调整温度
  if (month >= 3 && month <= 5) {
    // 春季
    tempOffset = 0;
  } else if (month >= 6 && month <= 8) {
    // 夏季
    tempOffset = 10;
  } else if (month >= 9 && month <= 11) {
    // 秋季
    tempOffset = -5;
  } else {
    // 冬季
    tempOffset = -15;
  }

  // 根据种子选择天气类型
  const weatherIndex = Math.floor(getSeededRandom(seed) * weatherTypes.length);
  const selectedWeather = weatherTypes[weatherIndex];

  // 计算温度
  const tempRange = selectedWeather.temp[1] - selectedWeather.temp[0];
  const temperature = Math.round(
    selectedWeather.temp[0] + getSeededRandom(seed + 1) * tempRange + tempOffset
  );

  // 选择城市
  const cityIndex = Math.floor(getSeededRandom(seed + 2) * cities.length);
  const city = cities[cityIndex];

  return {
    temperature,
    weather: selectedWeather.weather,
    icon: selectedWeather.icon,
    city,
  };
}

/**
 * 根据天气返回诗意描述
 */
export function getWeatherPoetry(weather: string): string {
  const poetryMap: Record<string, string> = {
    '晴': '天朗气清，惠风和畅',
    '多云': '云淡风轻近午天',
    '阴': '黑云翻墨未遮山',
    '小雨': '天街小雨润如酥',
    '雨': '空山新雨后，天气晚来秋',
    '雪': '忽如一夜春风来，千树万树梨花开',
  };

  return poetryMap[weather] || '四时之景不同，而乐亦无穷也';
}
