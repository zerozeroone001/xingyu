/**
 * 常量定义
 */

// 主题类型
export enum ThemeType {
  LIGHT = 'light',
  DARK = 'dark',
}

// 本地存储键名
export const STORAGE_KEYS = {
  THEME: 'theme',
  TOKEN: 'token',
  USER_INFO: 'userInfo',
} as const;

// API 基础地址
export const API_BASE_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8000/api/v1'
  : 'https://api.xingyu.com/api/v1';

// 页面路径
export const PAGE_PATHS = {
  INDEX: '/pages/index/index',
  LOGIN: '/pages/login/login',
  PROFILE: '/pages/profile/profile',
  SETTING: '/pages/setting/setting',
  POETRY_DETAIL: '/pages/poetry-detail/poetry-detail',
  POETRY_LIST: '/pages/poetry-list/poetry-list',
  SQUARE: '/pages/square/square',
  GAME: '/pages/game/game',
  MESSAGE: '/pages/message/message',
} as const;

// 请求超时时间
export const REQUEST_TIMEOUT = 10000;

// 分页默认大小
export const PAGE_SIZE = 20;
