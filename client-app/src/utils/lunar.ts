/**
 * 农历转换工具
 * 基于简化的农历算法
 */

// 农历数据：1900-2100年
const lunarInfo = [
  0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
  0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
  0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
  0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
  0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
  0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,
  0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
  0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,
  0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
  0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,
  0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
  0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
  0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
  0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
  0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
  0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0,
  0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
  0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
  0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
  0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,
  0x0d520,
];

const solarMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
const Gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
const Zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
const Animals = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪'];
const solarTerm = [
  '小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨',
  '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑',
  '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至',
];
const nStr1 = ['日', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十'];
const nStr2 = ['初', '十', '廿', '卅'];
const monthNong = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊'];

/**
 * 判断是否为闰年
 */
function isLeapYear(year: number): boolean {
  return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
}

/**
 * 获取某年的农历信息
 */
function lunarYearDays(year: number): number {
  let sum = 348;
  for (let i = 0x8000; i > 0x8; i >>= 1) {
    sum += lunarInfo[year - 1900] & i ? 1 : 0;
  }
  return sum + leapDays(year);
}

/**
 * 获取某年的闰月天数
 */
function leapDays(year: number): number {
  if (leapMonth(year)) {
    return lunarInfo[year - 1900] & 0x10000 ? 30 : 29;
  }
  return 0;
}

/**
 * 获取某年的闰月月份
 */
function leapMonth(year: number): number {
  return lunarInfo[year - 1900] & 0xf;
}

/**
 * 获取某年某月的农历天数
 */
function monthDays(year: number, month: number): number {
  return lunarInfo[year - 1900] & (0x10000 >> month) ? 30 : 29;
}

/**
 * 公历转农历
 */
export function solar2lunar(date?: Date): LunarDate {
  const objDate = date || new Date();
  let year = objDate.getFullYear();
  let month = objDate.getMonth() + 1;
  let day = objDate.getDate();

  let offset = 0;
  const yearDays = isLeapYear(year) ? 366 : 365;

  // 计算当年总天数
  for (let i = 1; i < month; i++) {
    offset += solarMonth[i - 1];
  }
  offset += day;
  if (isLeapYear(year) && month > 2) offset++;

  // 从1900年开始计算偏移
  let lunarYear = 1900;
  let lunarMonth = 1;
  let lunarDay = 0;
  let isLeap = false;

  // 计算农历年
  let temp = 0;
  for (let i = 1900; i < 2101 && offset > 0; i++) {
    temp = lunarYearDays(i);
    offset -= temp;
    lunarYear = i;
  }
  if (offset < 0) {
    offset += temp;
    lunarYear--;
  }

  // 计算农历月和日
  const leap = leapMonth(lunarYear);
  isLeap = false;

  for (let i = 1; i < 13 && offset > 0; i++) {
    // 闰月
    if (leap > 0 && i === leap + 1 && !isLeap) {
      --i;
      isLeap = true;
      temp = leapDays(lunarYear);
    } else {
      temp = monthDays(lunarYear, i);
    }

    if (isLeap && i === leap + 1) {
      isLeap = false;
    }

    offset -= temp;
    if (!isLeap) {
      lunarMonth = i;
    }
  }

  if (offset === 0 && leap > 0 && lunarMonth === leap + 1) {
    if (isLeap) {
      isLeap = false;
    } else {
      isLeap = true;
      --lunarMonth;
    }
  }

  if (offset < 0) {
    offset += temp;
    --lunarMonth;
  }

  lunarDay = offset + 1;

  // 天干地支
  const ganIndex = (lunarYear - 4) % 10;
  const zhiIndex = (lunarYear - 4) % 12;
  const ganzhi = Gan[ganIndex] + Zhi[zhiIndex];
  const animal = Animals[zhiIndex];

  // 农历月份和日期中文
  const monthCn = (isLeap ? '闰' : '') + monthNong[lunarMonth - 1] + '月';
  const dayCn = getChinaDay(lunarDay);

  return {
    year: lunarYear,
    month: lunarMonth,
    day: lunarDay,
    isLeap,
    yearCn: ganzhi + '年',
    monthCn,
    dayCn,
    ganzhi,
    animal: animal + '年',
    toString(): string {
      return `${this.yearCn} ${this.animal} ${this.monthCn}${this.dayCn}`;
    },
  };
}

/**
 * 获取农历日期的中文表示
 */
function getChinaDay(day: number): string {
  let s;
  switch (day) {
    case 10:
      s = '初十';
      break;
    case 20:
      s = '二十';
      break;
    case 30:
      s = '三十';
      break;
    default:
      s = nStr2[Math.floor(day / 10)];
      s += nStr1[day % 10];
  }
  return s;
}

/**
 * 农历日期接口
 */
export interface LunarDate {
  year: number;
  month: number;
  day: number;
  isLeap: boolean;
  yearCn: string;
  monthCn: string;
  dayCn: string;
  ganzhi: string;
  animal: string;
  toString(): string;
}

/**
 * 获取星期的中文表示
 */
export function getWeekDay(date?: Date): string {
  const weekDays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
  const day = (date || new Date()).getDay();
  return weekDays[day];
}

/**
 * 格式化日期
 */
export function formatDate(date?: Date): string {
  const d = date || new Date();
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}年${month}月${day}日`;
}
