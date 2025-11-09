/**
 * uni-app API Shim for H5 Environment
 *
 * This module provides a compatibility layer for uni-app APIs in H5/Web environment.
 * It defines the `uni` object and immediately attaches it to `window.uni` at module load time.
 *
 * IMPORTANT: This module must NOT import any other modules to avoid circular dependencies.
 */

interface ShowToastOptions {
  title: string;
  icon?: 'success' | 'error' | 'loading' | 'none';
  duration?: number;
  mask?: boolean;
  success?: () => void;
  fail?: () => void;
  complete?: () => void;
}

interface ShowLoadingOptions {
  title: string;
  mask?: boolean;
  success?: () => void;
  fail?: () => void;
  complete?: () => void;
}

interface NavigateToOptions {
  url: string;
  success?: () => void;
  fail?: () => void;
  complete?: () => void;
}

interface NavigateBackOptions {
  delta?: number;
  success?: () => void;
  fail?: () => void;
  complete?: () => void;
}

interface StorageOptions {
  key: string;
  data?: any;
  success?: (res?: any) => void;
  fail?: () => void;
  complete?: () => void;
}

// Toast management
let currentToast: HTMLDivElement | null = null;
let toastTimer: number | null = null;

// Loading management
let currentLoading: HTMLDivElement | null = null;

/**
 * Create a toast/loading element
 */
function createOverlay(
  message: string,
  type: 'toast' | 'loading',
  icon?: 'success' | 'error' | 'loading' | 'none'
): HTMLDivElement {
  const overlay = document.createElement('div');
  overlay.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 16px 24px;
    border-radius: 8px;
    z-index: 10000;
    max-width: 80%;
    text-align: center;
    font-size: 14px;
    line-height: 1.5;
    word-break: break-word;
  `;

  // Add icon if specified
  if (icon && icon !== 'none') {
    const iconEl = document.createElement('div');
    iconEl.style.cssText = `
      font-size: 40px;
      margin-bottom: 8px;
    `;

    switch (icon) {
      case 'success':
        iconEl.textContent = '✓';
        break;
      case 'error':
        iconEl.textContent = '✕';
        break;
      case 'loading':
        iconEl.textContent = '⟳';
        iconEl.style.animation = 'spin 1s linear infinite';
        // Add animation style
        if (!document.getElementById('uni-shim-animation')) {
          const style = document.createElement('style');
          style.id = 'uni-shim-animation';
          style.textContent = `
            @keyframes spin {
              from { transform: rotate(0deg); }
              to { transform: rotate(360deg); }
            }
          `;
          document.head.appendChild(style);
        }
        break;
    }

    overlay.appendChild(iconEl);
  }

  const textEl = document.createElement('div');
  textEl.textContent = message;
  overlay.appendChild(textEl);

  document.body.appendChild(overlay);
  return overlay;
}

/**
 * Remove toast
 */
function removeToast() {
  if (currentToast && currentToast.parentNode) {
    currentToast.parentNode.removeChild(currentToast);
  }
  currentToast = null;
  if (toastTimer !== null) {
    clearTimeout(toastTimer);
    toastTimer = null;
  }
}

/**
 * Get router instance from window if available
 */
function getRouter(): any {
  return (window as any).__APP_ROUTER__;
}

/**
 * Navigate using router or fallback to window.location
 */
function navigateWithRouter(url: string, method: 'push' | 'replace') {
  const router = getRouter();

  if (router) {
    // Remove leading slash if present for router navigation
    const path = url.startsWith('/') ? url : '/' + url;

    if (method === 'push') {
      router.push(path).catch((err: any) => {
        console.warn('Navigation failed:', err);
      });
    } else {
      router.replace(path).catch((err: any) => {
        console.warn('Navigation failed:', err);
      });
    }
  } else {
    // Fallback to window.location
    if (method === 'push') {
      window.history.pushState(null, '', url);
      // Trigger a popstate event to notify any listeners
      window.dispatchEvent(new PopStateEvent('popstate'));
    } else {
      window.location.replace(url);
    }
  }
}

/**
 * uni-app API implementation
 */
const uni = {
  /**
   * Show toast message
   */
  showToast(options: ShowToastOptions) {
    // Remove existing toast
    removeToast();

    // Create new toast
    currentToast = createOverlay(
      options.title,
      'toast',
      options.icon || 'none'
    );

    // Auto hide after duration
    const duration = options.duration || 1500;
    toastTimer = window.setTimeout(() => {
      removeToast();
      options.success?.();
      options.complete?.();
    }, duration);
  },

  /**
   * Show loading indicator
   */
  showLoading(options: ShowLoadingOptions) {
    // Remove existing loading
    if (currentLoading && currentLoading.parentNode) {
      currentLoading.parentNode.removeChild(currentLoading);
    }

    // Create new loading
    currentLoading = createOverlay(options.title, 'loading', 'loading');

    options.success?.();
    options.complete?.();
  },

  /**
   * Hide loading indicator
   */
  hideLoading() {
    if (currentLoading && currentLoading.parentNode) {
      currentLoading.parentNode.removeChild(currentLoading);
    }
    currentLoading = null;
  },

  /**
   * Navigate to a page
   */
  navigateTo(options: NavigateToOptions) {
    try {
      navigateWithRouter(options.url, 'push');
      options.success?.();
    } catch (error) {
      console.error('navigateTo error:', error);
      options.fail?.();
    } finally {
      options.complete?.();
    }
  },

  /**
   * Redirect to a page (replace current page)
   */
  redirectTo(options: NavigateToOptions) {
    try {
      navigateWithRouter(options.url, 'replace');
      options.success?.();
    } catch (error) {
      console.error('redirectTo error:', error);
      options.fail?.();
    } finally {
      options.complete?.();
    }
  },

  /**
   * Relaunch to a page (close all pages and open a new one)
   */
  reLaunch(options: NavigateToOptions) {
    try {
      const router = getRouter();

      if (router) {
        // Remove leading slash if present
        const path = options.url.startsWith('/') ? options.url : '/' + options.url;
        router.replace(path).catch((err: any) => {
          console.warn('reLaunch failed:', err);
        });
      } else {
        // Fallback: replace current location
        window.location.replace(options.url);
      }

      options.success?.();
    } catch (error) {
      console.error('reLaunch error:', error);
      options.fail?.();
    } finally {
      options.complete?.();
    }
  },

  /**
   * Navigate back
   */
  navigateBack(options: NavigateBackOptions = {}) {
    try {
      const delta = options.delta || 1;
      const router = getRouter();

      if (router) {
        router.go(-delta);
      } else {
        // Fallback to window.history
        window.history.go(-delta);
      }

      options.success?.();
    } catch (error) {
      console.error('navigateBack error:', error);
      options.fail?.();
    } finally {
      options.complete?.();
    }
  },

  /**
   * Switch to a tab page
   */
  switchTab(options: NavigateToOptions) {
    try {
      navigateWithRouter(options.url, 'replace');
      options.success?.();
    } catch (error) {
      console.error('switchTab error:', error);
      options.fail?.();
    } finally {
      options.complete?.();
    }
  },

  /**
   * Set storage (async)
   */
  setStorage(options: StorageOptions) {
    try {
      const value = typeof options.data === 'string'
        ? options.data
        : JSON.stringify(options.data);
      localStorage.setItem(options.key, value);
      options.success?.();
    } catch (error) {
      console.error('setStorage error:', error);
      options.fail?.();
    } finally {
      options.complete?.();
    }
  },

  /**
   * Set storage (sync)
   */
  setStorageSync(key: string, data: any) {
    try {
      const value = typeof data === 'string' ? data : JSON.stringify(data);
      localStorage.setItem(key, value);
    } catch (error) {
      console.error('setStorageSync error:', error);
      throw error;
    }
  },

  /**
   * Get storage (async)
   */
  getStorage(options: StorageOptions) {
    try {
      const value = localStorage.getItem(options.key);
      if (value === null) {
        options.fail?.();
      } else {
        let data: any;
        try {
          data = JSON.parse(value);
        } catch {
          data = value;
        }
        options.success?.({ data });
      }
    } catch (error) {
      console.error('getStorage error:', error);
      options.fail?.();
    } finally {
      options.complete?.();
    }
  },

  /**
   * Get storage (sync)
   */
  getStorageSync(key: string): any {
    try {
      const value = localStorage.getItem(key);
      if (value === null) {
        return '';
      }
      try {
        return JSON.parse(value);
      } catch {
        return value;
      }
    } catch (error) {
      console.error('getStorageSync error:', error);
      return '';
    }
  },

  /**
   * Remove storage (async)
   */
  removeStorage(options: StorageOptions) {
    try {
      localStorage.removeItem(options.key);
      options.success?.();
    } catch (error) {
      console.error('removeStorage error:', error);
      options.fail?.();
    } finally {
      options.complete?.();
    }
  },

  /**
   * Remove storage (sync)
   */
  removeStorageSync(key: string) {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('removeStorageSync error:', error);
      throw error;
    }
  },

  /**
   * Clear all storage (async)
   */
  clearStorage(options: Partial<StorageOptions> = {}) {
    try {
      localStorage.clear();
      options.success?.();
    } catch (error) {
      console.error('clearStorage error:', error);
      options.fail?.();
    } finally {
      options.complete?.();
    }
  },

  /**
   * Clear all storage (sync)
   */
  clearStorageSync() {
    try {
      localStorage.clear();
    } catch (error) {
      console.error('clearStorageSync error:', error);
      throw error;
    }
  },

  /**
   * Get storage info (async)
   */
  getStorageInfo(options: Partial<StorageOptions> = {}) {
    try {
      const keys: string[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key) {
          keys.push(key);
        }
      }

      // Calculate approximate size (in KB)
      let currentSize = 0;
      keys.forEach(key => {
        const value = localStorage.getItem(key);
        if (value) {
          currentSize += key.length + value.length;
        }
      });
      currentSize = Math.ceil(currentSize / 1024);

      options.success?.({
        keys,
        currentSize,
        limitSize: 10240 // 10MB (approximate limit)
      });
    } catch (error) {
      console.error('getStorageInfo error:', error);
      options.fail?.();
    } finally {
      options.complete?.();
    }
  },

  /**
   * Get storage info (sync)
   */
  getStorageInfoSync(): {
    keys: string[];
    currentSize: number;
    limitSize: number;
  } {
    try {
      const keys: string[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key) {
          keys.push(key);
        }
      }

      // Calculate approximate size (in KB)
      let currentSize = 0;
      keys.forEach(key => {
        const value = localStorage.getItem(key);
        if (value) {
          currentSize += key.length + value.length;
        }
      });
      currentSize = Math.ceil(currentSize / 1024);

      return {
        keys,
        currentSize,
        limitSize: 10240 // 10MB (approximate limit)
      };
    } catch (error) {
      console.error('getStorageInfoSync error:', error);
      return {
        keys: [],
        currentSize: 0,
        limitSize: 10240
      };
    }
  },

  /**
   * Stop pull-down refresh
   */
  stopPullDownRefresh() {
    console.log('stopPullDownRefresh: Not implemented in H5 environment');
  },

  /**
   * Get system info (sync)
   */
  getSystemInfoSync(): any {
    return {
      platform: 'web',
      theme: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight,
      screenWidth: window.screen.width,
      screenHeight: window.screen.height,
    };
  },

  /**
   * Event emitter (simple implementation for H5)
   */
  $emit(event: string, ...args: any[]) {
    // In H5 environment, we can use custom events
    const customEvent = new CustomEvent(event, { detail: args });
    window.dispatchEvent(customEvent);
  },

  /**
   * Event listener
   */
  $on(event: string, callback: (...args: any[]) => void) {
    window.addEventListener(event, (e: any) => {
      callback(...(e.detail || []));
    });
  },

  /**
   * Remove event listener
   */
  $off(event: string, callback?: (...args: any[]) => void) {
    if (callback) {
      window.removeEventListener(event, callback as any);
    }
  }
};

// Immediately attach uni to window
(window as any).uni = uni;

// Also export for TypeScript module usage
export default uni;
