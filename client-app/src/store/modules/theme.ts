/**
 * 主题状态管理
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { ThemeType, STORAGE_KEYS } from '@/utils/constants';
import { getStorageSync, setStorageSync } from '@/utils/storage';

export const useThemeStore = defineStore('theme', () => {
  // 状态
  const currentTheme = ref<ThemeType>(ThemeType.LIGHT);
  const isSystemTheme = ref<boolean>(false); // 是否跟随系统主题

  // 计算属性
  const isDark = computed(() => currentTheme.value === ThemeType.DARK);
  const isLight = computed(() => currentTheme.value === ThemeType.LIGHT);
  const themeClass = computed(() => `theme-${currentTheme.value}`);

  /**
   * 初始化主题
   * 从本地存储读取用户主题偏好，如果没有则默认为明亮模式
   */
  const initTheme = () => {
    const savedTheme = getStorageSync<ThemeType>(STORAGE_KEYS.THEME);

    if (savedTheme && Object.values(ThemeType).includes(savedTheme)) {
      currentTheme.value = savedTheme;
    } else {
      // 尝试获取系统主题偏好
      const systemTheme = getSystemTheme();
      currentTheme.value = systemTheme;
    }

    // 应用主题到页面
    applyTheme(currentTheme.value);
  };

  /**
   * 获取系统主题
   */
  const getSystemTheme = (): ThemeType => {
    try {
      // 在 H5 环境中，使用 window.matchMedia 检测系统主题
      if (typeof window !== 'undefined' && window.matchMedia) {
        const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
        if (darkModeQuery.matches) {
          return ThemeType.DARK;
        }
      }

      // 在小程序环境中，尝试使用 uni API
      if (typeof uni !== 'undefined' && uni.getSystemInfoSync) {
        const systemInfo = uni.getSystemInfoSync();
        if ('theme' in systemInfo) {
          return (systemInfo as any).theme === 'dark' ? ThemeType.DARK : ThemeType.LIGHT;
        }
      }

      // 默认返回明亮模式
      return ThemeType.LIGHT;
    } catch (error) {
      console.error('获取系统主题失败:', error);
      return ThemeType.LIGHT;
    }
  };

  /**
   * 切换主题
   * @param theme 主题类型，如果不传则在明亮和暗黑之间切换
   */
  const toggleTheme = (theme?: ThemeType) => {
    const newTheme = theme || (isDark.value ? ThemeType.LIGHT : ThemeType.DARK);
    setTheme(newTheme);
  };

  /**
   * 设置主题
   * @param theme 主题类型
   */
  const setTheme = (theme: ThemeType) => {
    if (!Object.values(ThemeType).includes(theme)) {
      console.error('无效的主题类型:', theme);
      return;
    }

    currentTheme.value = theme;
    isSystemTheme.value = false;

    // 持久化到本地存储
    setStorageSync(STORAGE_KEYS.THEME, theme);

    // 应用主题到页面
    applyTheme(theme);
  };

  /**
   * 应用主题到页面
   * @param theme 主题类型
   */
  const applyTheme = (theme: ThemeType) => {
    try {
      // 在 H5 环境中，主题通过 App.vue 的 :class 绑定自动应用
      // 不需要额外的操作，只需要确保 currentTheme 已更新

      // 触发自定义事件（如果在 uni-app 环境中）
      if (typeof uni !== 'undefined' && uni.$emit) {
        uni.$emit('themeChanged', theme);
      }

      console.log('主题已切换至:', theme);
    } catch (error) {
      console.error('应用主题失败:', error);
    }
  };

  /**
   * 设置跟随系统主题
   * @param follow 是否跟随系统
   */
  const setFollowSystem = (follow: boolean) => {
    isSystemTheme.value = follow;

    if (follow) {
      const systemTheme = getSystemTheme();
      setTheme(systemTheme);

      // 监听系统主题变化（如果平台支持）
      // 这需要根据具体平台实现
    } else {
      // 停止监听系统主题变化
    }
  };

  /**
   * 重置主题为默认值
   */
  const resetTheme = () => {
    setTheme(ThemeType.LIGHT);
    isSystemTheme.value = false;
  };

  return {
    // 状态
    currentTheme,
    isSystemTheme,

    // 计算属性
    isDark,
    isLight,
    themeClass,

    // 方法
    initTheme,
    toggleTheme,
    setTheme,
    setFollowSystem,
    resetTheme,
    getSystemTheme,
  };
});
