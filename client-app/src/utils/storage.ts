/**
 * 本地存储工具类
 * 封装 uni.storage API，提供统一的存储接口
 */

/**
 * 存储数据
 * @param key 存储键名
 * @param value 存储值
 * @returns Promise
 */
export function setStorage<T = any>(key: string, value: T): Promise<void> {
  return new Promise((resolve, reject) => {
    if (typeof uni === 'undefined') {
      // 在非 uni 环境中使用 localStorage 作为后备
      try {
        localStorage.setItem(key, JSON.stringify(value));
        resolve();
      } catch (error) {
        reject(error);
      }
      return;
    }

    uni.setStorage({
      key,
      data: value,
      success: () => resolve(),
      fail: (error) => reject(error),
    });
  });
}

/**
 * 同步存储数据
 * @param key 存储键名
 * @param value 存储值
 */
export function setStorageSync<T = any>(key: string, value: T): void {
  try {
    if (typeof uni === 'undefined') {
      // 在非 uni 环境中使用 localStorage 作为后备
      localStorage.setItem(key, JSON.stringify(value));
      return;
    }

    uni.setStorageSync(key, value);
  } catch (error) {
    console.error(`setStorageSync error for key: ${key}`, error);
    throw error;
  }
}

/**
 * 获取数据
 * @param key 存储键名
 * @returns Promise<T>
 */
export function getStorage<T = any>(key: string): Promise<T | null> {
  return new Promise((resolve, reject) => {
    if (typeof uni === 'undefined') {
      // 在非 uni 环境中使用 localStorage 作为后备
      try {
        const value = localStorage.getItem(key);
        resolve(value ? JSON.parse(value) : null);
      } catch (error) {
        resolve(null);
      }
      return;
    }

    uni.getStorage({
      key,
      success: (res) => resolve(res.data as T),
      fail: () => resolve(null),
    });
  });
}

/**
 * 同步获取数据
 * @param key 存储键名
 * @returns T | null
 */
export function getStorageSync<T = any>(key: string): T | null {
  try {
    if (typeof uni === 'undefined') {
      // 在非 uni 环境中使用 localStorage 作为后备
      const value = localStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    }

    const value = uni.getStorageSync(key);
    return value !== undefined && value !== '' ? (value as T) : null;
  } catch (error) {
    console.error(`getStorageSync error for key: ${key}`, error);
    return null;
  }
}

/**
 * 移除数据
 * @param key 存储键名
 * @returns Promise
 */
export function removeStorage(key: string): Promise<void> {
  return new Promise((resolve, reject) => {
    if (typeof uni === 'undefined') {
      try {
        localStorage.removeItem(key);
        resolve();
      } catch (error) {
        reject(error);
      }
      return;
    }

    uni.removeStorage({
      key,
      success: () => resolve(),
      fail: (error) => reject(error),
    });
  });
}

/**
 * 同步移除数据
 * @param key 存储键名
 */
export function removeStorageSync(key: string): void {
  try {
    if (typeof uni === 'undefined') {
      localStorage.removeItem(key);
      return;
    }

    uni.removeStorageSync(key);
  } catch (error) {
    console.error(`removeStorageSync error for key: ${key}`, error);
    throw error;
  }
}

/**
 * 清空所有存储数据
 * @returns Promise
 */
export function clearStorage(): Promise<void> {
  return new Promise((resolve, reject) => {
    if (typeof uni === 'undefined') {
      try {
        localStorage.clear();
        resolve();
      } catch (error) {
        reject(error);
      }
      return;
    }

    uni.clearStorage({
      success: () => resolve(),
      fail: (error) => reject(error),
    });
  });
}

/**
 * 同步清空所有存储数据
 */
export function clearStorageSync(): void {
  try {
    if (typeof uni === 'undefined') {
      localStorage.clear();
      return;
    }

    uni.clearStorageSync();
  } catch (error) {
    console.error('clearStorageSync error', error);
    throw error;
  }
}

/**
 * 获取存储信息
 * @returns Promise
 */
export function getStorageInfo(): Promise<UniApp.GetStorageInfoSuccess> {
  return new Promise((resolve, reject) => {
    if (typeof uni === 'undefined') {
      try {
        const keys = Object.keys(localStorage);
        let currentSize = 0;
        keys.forEach(key => {
          currentSize += (localStorage.getItem(key) || '').length;
        });
        resolve({
          keys,
          currentSize,
          limitSize: 10240, // 模拟值
        } as UniApp.GetStorageInfoSuccess);
      } catch (error) {
        reject(error);
      }
      return;
    }

    uni.getStorageInfo({
      success: (res) => resolve(res),
      fail: (error) => reject(error),
    });
  });
}

/**
 * 同步获取存储信息
 * @returns 存储信息
 */
export function getStorageInfoSync(): UniApp.GetStorageInfoSuccess {
  try {
    if (typeof uni === 'undefined') {
      const keys = Object.keys(localStorage);
      let currentSize = 0;
      keys.forEach(key => {
        currentSize += (localStorage.getItem(key) || '').length;
      });
      return {
        keys,
        currentSize,
        limitSize: 10240, // 模拟值
      } as UniApp.GetStorageInfoSuccess;
    }

    return uni.getStorageInfoSync();
  } catch (error) {
    console.error('getStorageInfoSync error', error);
    throw error;
  }
}
