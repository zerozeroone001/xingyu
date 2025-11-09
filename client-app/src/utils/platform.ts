/**
 * 多端平台适配工具
 * 支持 H5、小程序、PC 端
 */

// 平台类型
export enum PlatformType {
  H5 = 'h5',
  WECHAT = 'wechat', // 微信小程序
  ALIPAY = 'alipay', // 支付宝小程序
  PC = 'pc',
  UNKNOWN = 'unknown',
}

/**
 * 获取当前运行平台
 */
export function getPlatform(): PlatformType {
  // 检查是否是小程序环境
  if (typeof uni !== 'undefined') {
    // @ts-ignore
    const systemInfo = uni.getSystemInfoSync?.();
    const platform = systemInfo?.platform || '';

    if (platform.includes('devtools') || platform.includes('windows') || platform.includes('mac')) {
      // 小程序开发工具
      return PlatformType.WECHAT;
    }
    return PlatformType.WECHAT;
  }

  // 检查是否是浏览器环境
  if (typeof window !== 'undefined') {
    const ua = navigator.userAgent.toLowerCase();

    // 检查是否是微信浏览器
    if (ua.includes('micromessenger')) {
      return PlatformType.H5;
    }

    // 检查是否是移动设备
    const isMobile = /mobile|android|iphone|ipad|phone/i.test(ua);

    if (isMobile) {
      return PlatformType.H5;
    } else {
      return PlatformType.PC;
    }
  }

  return PlatformType.UNKNOWN;
}

/**
 * 判断是否是 H5 环境
 */
export function isH5(): boolean {
  return getPlatform() === PlatformType.H5;
}

/**
 * 判断是否是小程序环境
 */
export function isMiniProgram(): boolean {
  const platform = getPlatform();
  return platform === PlatformType.WECHAT || platform === PlatformType.ALIPAY;
}

/**
 * 判断是否是 PC 环境
 */
export function isPC(): boolean {
  return getPlatform() === PlatformType.PC;
}

/**
 * 判断是否是移动端（H5 或小程序）
 */
export function isMobile(): boolean {
  return isH5() || isMiniProgram();
}

/**
 * Toast 提示（多端兼容）
 */
export function showToast(options: { title: string; icon?: 'success' | 'error' | 'none'; duration?: number }) {
  if (typeof uni !== 'undefined') {
    // 小程序环境
    uni.showToast({
      title: options.title,
      icon: options.icon === 'error' ? 'none' : options.icon || 'none',
      duration: options.duration || 2000,
    });
  } else if (typeof window !== 'undefined') {
    // H5 环境 - 使用简单的 alert 或者后续可以集成 toast 组件库
    console.log(`[Toast] ${options.title}`);
    // TODO: 可以集成如 vant 的 toast 组件
    alert(options.title);
  }
}

/**
 * Loading 提示（多端兼容）
 */
export function showLoading(options?: { title?: string; mask?: boolean }) {
  if (typeof uni !== 'undefined') {
    uni.showLoading({
      title: options?.title || '加载中...',
      mask: options?.mask !== false,
    });
  } else {
    console.log('[Loading] 显示加载中...');
    // H5 可以使用 loading 组件
  }
}

/**
 * 隐藏 Loading（多端兼容）
 */
export function hideLoading() {
  if (typeof uni !== 'undefined') {
    uni.hideLoading();
  } else {
    console.log('[Loading] 隐藏加载');
  }
}

/**
 * 页面导航（多端兼容）
 */
export function navigateTo(url: string) {
  if (typeof uni !== 'undefined') {
    // 小程序环境
    uni.navigateTo({ url });
  } else if (typeof window !== 'undefined') {
    // H5 环境 - 需要配合 vue-router
    // 这里需要从 url 转换为路由路径
    const path = convertUniUrlToRoutePath(url);
    window.location.hash = path;
  }
}

/**
 * 转换小程序 URL 格式到 H5 路由格式
 * 例如: /pages/poetry-detail/poetry-detail?id=1 -> /poetry-detail/1
 */
function convertUniUrlToRoutePath(uniUrl: string): string {
  const [path, query] = uniUrl.split('?');
  const pageName = path.split('/').pop()?.replace(/\..*$/, '') || '';

  if (query) {
    const params = new URLSearchParams(query);
    const id = params.get('id');
    if (id) {
      return `/${pageName}/${id}`;
    }
  }

  return `/${pageName}`;
}

/**
 * 获取存储（多端兼容）
 */
export function getStorage(key: string): Promise<any> {
  return new Promise((resolve, reject) => {
    if (typeof uni !== 'undefined') {
      uni.getStorage({
        key,
        success: (res: any) => resolve(res.data),
        fail: reject,
      });
    } else if (typeof window !== 'undefined') {
      try {
        const value = localStorage.getItem(key);
        resolve(value ? JSON.parse(value) : null);
      } catch (error) {
        reject(error);
      }
    } else {
      reject(new Error('不支持的环境'));
    }
  });
}

/**
 * 设置存储（多端兼容）
 */
export function setStorage(key: string, data: any): Promise<void> {
  return new Promise((resolve, reject) => {
    if (typeof uni !== 'undefined') {
      uni.setStorage({
        key,
        data,
        success: () => resolve(),
        fail: reject,
      });
    } else if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(key, JSON.stringify(data));
        resolve();
      } catch (error) {
        reject(error);
      }
    } else {
      reject(new Error('不支持的环境'));
    }
  });
}

/**
 * 同步获取存储（多端兼容）
 */
export function getStorageSync(key: string): any {
  if (typeof uni !== 'undefined') {
    return uni.getStorageSync(key);
  } else if (typeof window !== 'undefined') {
    try {
      const value = localStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('读取本地存储失败:', error);
      return null;
    }
  }
  return null;
}

/**
 * 同步设置存储（多端兼容）
 */
export function setStorageSync(key: string, data: any): void {
  if (typeof uni !== 'undefined') {
    uni.setStorageSync(key, data);
  } else if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
      console.error('写入本地存储失败:', error);
    }
  }
}

/**
 * 删除存储（多端兼容）
 */
export function removeStorage(key: string): Promise<void> {
  return new Promise((resolve, reject) => {
    if (typeof uni !== 'undefined') {
      uni.removeStorage({
        key,
        success: () => resolve(),
        fail: reject,
      });
    } else if (typeof window !== 'undefined') {
      try {
        localStorage.removeItem(key);
        resolve();
      } catch (error) {
        reject(error);
      }
    } else {
      reject(new Error('不支持的环境'));
    }
  });
}

export default {
  getPlatform,
  isH5,
  isMiniProgram,
  isPC,
  isMobile,
  showToast,
  showLoading,
  hideLoading,
  navigateTo,
  getStorage,
  setStorage,
  getStorageSync,
  setStorageSync,
  removeStorage,
};
