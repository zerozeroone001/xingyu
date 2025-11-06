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
    return uni.getStorageInfoSync();
  } catch (error) {
    console.error('getStorageInfoSync error', error);
    throw error;
  }
}
