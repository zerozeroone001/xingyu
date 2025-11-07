/**
 * uni-app 全局类型声明
 */

// Toast 配置接口
interface UniToastOptions {
  title: string;
  icon?: 'success' | 'error' | 'loading' | 'none';
  duration?: number;
  mask?: boolean;
}

// Loading 配置接口
interface UniLoadingOptions {
  title?: string;
  mask?: boolean;
}

// 导航配置接口
interface UniNavigateOptions {
  url: string;
  success?: () => void;
  fail?: (error: any) => void;
  complete?: () => void;
}

// 存储相关接口
interface UniStorageOptions {
  key: string;
  data?: any;
  success?: () => void;
  fail?: (error: any) => void;
  complete?: () => void;
}

// uni 全局对象类型
interface Uni {
  showToast(options: UniToastOptions): void;
  showLoading(options: UniLoadingOptions): void;
  hideLoading(): void;
  navigateTo(options: UniNavigateOptions): void;
  redirectTo(options: UniNavigateOptions): void;
  reLaunch(options: UniNavigateOptions): void;
  navigateBack(delta?: number): void;
  switchTab(options: UniNavigateOptions): void;
  setStorage(options: UniStorageOptions): void;
  setStorageSync(key: string, data: any): void;
  getStorage(options: UniStorageOptions): void;
  getStorageSync(key: string): any;
  removeStorage(options: UniStorageOptions): void;
  removeStorageSync(key: string): void;
  stopPullDownRefresh(): void;
}

// 声明全局变量
declare global {
  const uni: Uni;
  interface Window {
    uni: Uni;
  }
}

export {};
