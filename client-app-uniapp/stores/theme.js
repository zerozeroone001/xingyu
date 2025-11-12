import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 主题配置
 * 10种精心设计的主题，包含完整的颜色方案
 */
const themes = {
  // 1. 明亮主题 - 清新明快
  light: {
    name: '明亮',
    icon: '☀️',
    primary: '#3B7EFF',
    secondary: '#7DABFF',
    bgColor: '#FFFFFF',
    bgSecondary: '#F5F7FA',
    bgThird: '#EDF1F7',
    textColor: '#2C3E50',
    textSecondary: '#606266',
    textThird: '#909399',
    borderColor: '#DCDFE6',
    shadowColor: 'rgba(0, 0, 0, 0.1)',
    cardBg: '#FFFFFF',
    buttonPrimary: '#3B7EFF',
    buttonSecondary: '#ECF5FF',
    successColor: '#67C23A',
    warningColor: '#E6A23C',
    dangerColor: '#F56C6C',
    infoColor: '#909399'
  },

  // 2. 暗黑主题 - 深邃神秘
  dark: {
    name: '暗黑',
    icon: '🌙',
    primary: '#409EFF',
    secondary: '#66B1FF',
    bgColor: '#1C1C1E',
    bgSecondary: '#2C2C2E',
    bgThird: '#3A3A3C',
    textColor: '#FFFFFF',
    textSecondary: '#E5E5EA',
    textThird: '#B0B0B5',
    borderColor: '#48484A',
    shadowColor: 'rgba(0, 0, 0, 0.5)',
    cardBg: '#2C2C2E',
    buttonPrimary: '#409EFF',
    buttonSecondary: '#2D4A6E',
    successColor: '#52C41A',
    warningColor: '#FAAD14',
    dangerColor: '#F5222D',
    infoColor: '#8C8C8C'
  },

  // 3. 清新主题 - 春日绿意
  fresh: {
    name: '清新',
    icon: '🌿',
    primary: '#52C41A',
    secondary: '#73D13D',
    bgColor: '#F6FFED',
    bgSecondary: '#E8F9E8',
    bgThird: '#D9F7BE',
    textColor: '#135200',
    textSecondary: '#237804',
    textThird: '#389E0D',
    borderColor: '#B7EB8F',
    shadowColor: 'rgba(82, 196, 26, 0.15)',
    cardBg: '#FFFFFF',
    buttonPrimary: '#52C41A',
    buttonSecondary: '#F6FFED',
    successColor: '#52C41A',
    warningColor: '#FAAD14',
    dangerColor: '#FF4D4F',
    infoColor: '#8C8C8C'
  },

  // 4. 炫紫主题 - 神秘优雅
  purple: {
    name: '炫紫',
    icon: '💜',
    primary: '#9C27B0',
    secondary: '#BA68C8',
    bgColor: '#F3E5F5',
    bgSecondary: '#E1BEE7',
    bgThird: '#CE93D8',
    textColor: '#4A148C',
    textSecondary: '#6A1B9A',
    textThird: '#7B1FA2',
    borderColor: '#CE93D8',
    shadowColor: 'rgba(156, 39, 176, 0.2)',
    cardBg: '#FFFFFF',
    buttonPrimary: '#9C27B0',
    buttonSecondary: '#F3E5F5',
    successColor: '#66BB6A',
    warningColor: '#FFA726',
    dangerColor: '#EF5350',
    infoColor: '#8C8C8C'
  },

  // 5. 温馨主题 - 暖橙舒适
  warm: {
    name: '温馨',
    icon: '🧡',
    primary: '#FF9800',
    secondary: '#FFB74D',
    bgColor: '#FFF3E0',
    bgSecondary: '#FFE0B2',
    bgThird: '#FFCC80',
    textColor: '#E65100',
    textSecondary: '#EF6C00',
    textThird: '#F57C00',
    borderColor: '#FFCC80',
    shadowColor: 'rgba(255, 152, 0, 0.2)',
    cardBg: '#FFFFFF',
    buttonPrimary: '#FF9800',
    buttonSecondary: '#FFF3E0',
    successColor: '#8BC34A',
    warningColor: '#FFC107',
    dangerColor: '#F44336',
    infoColor: '#9E9E9E'
  },

  // 6. 海洋主题 - 深蓝宁静
  ocean: {
    name: '海洋',
    icon: '🌊',
    primary: '#0288D1',
    secondary: '#4FC3F7',
    bgColor: '#E1F5FE',
    bgSecondary: '#B3E5FC',
    bgThird: '#81D4FA',
    textColor: '#01579B',
    textSecondary: '#0277BD',
    textThird: '#0288D1',
    borderColor: '#81D4FA',
    shadowColor: 'rgba(2, 136, 209, 0.2)',
    cardBg: '#FFFFFF',
    buttonPrimary: '#0288D1',
    buttonSecondary: '#E1F5FE',
    successColor: '#00BCD4',
    warningColor: '#FF9800',
    dangerColor: '#F44336',
    infoColor: '#9E9E9E'
  },

  // 7. 森林主题 - 墨绿深沉
  forest: {
    name: '森林',
    icon: '🌲',
    primary: '#388E3C',
    secondary: '#66BB6A',
    bgColor: '#E8F5E9',
    bgSecondary: '#C8E6C9',
    bgThird: '#A5D6A7',
    textColor: '#1B5E20',
    textSecondary: '#2E7D32',
    textThird: '#388E3C',
    borderColor: '#A5D6A7',
    shadowColor: 'rgba(56, 142, 60, 0.2)',
    cardBg: '#FFFFFF',
    buttonPrimary: '#388E3C',
    buttonSecondary: '#E8F5E9',
    successColor: '#4CAF50',
    warningColor: '#FF9800',
    dangerColor: '#E53935',
    infoColor: '#9E9E9E'
  },

  // 8. 晚霞主题 - 粉橙渐变
  sunset: {
    name: '晚霞',
    icon: '🌅',
    primary: '#F06292',
    secondary: '#FF80AB',
    bgColor: '#FCE4EC',
    bgSecondary: '#F8BBD0',
    bgThird: '#F48FB1',
    textColor: '#880E4F',
    textSecondary: '#AD1457',
    textThird: '#C2185B',
    borderColor: '#F48FB1',
    shadowColor: 'rgba(240, 98, 146, 0.2)',
    cardBg: '#FFFFFF',
    buttonPrimary: '#F06292',
    buttonSecondary: '#FCE4EC',
    successColor: '#66BB6A',
    warningColor: '#FFA726',
    dangerColor: '#EF5350',
    infoColor: '#BDBDBD'
  },

  // 9. 星空主题 - 深蓝静谧
  starry: {
    name: '星空',
    icon: '⭐',
    primary: '#5C6BC0',
    secondary: '#7986CB',
    bgColor: '#1A237E',
    bgSecondary: '#283593',
    bgThird: '#3949AB',
    textColor: '#FFFFFF',
    textSecondary: '#C5CAE9',
    textThird: '#9FA8DA',
    borderColor: '#3949AB',
    shadowColor: 'rgba(92, 107, 192, 0.3)',
    cardBg: '#283593',
    buttonPrimary: '#5C6BC0',
    buttonSecondary: '#3949AB',
    successColor: '#66BB6A',
    warningColor: '#FFB74D',
    dangerColor: '#EF5350',
    infoColor: '#9E9E9E'
  },

  // 10. 简约主题 - 灰度优雅
  minimal: {
    name: '简约',
    icon: '⚪',
    primary: '#607D8B',
    secondary: '#90A4AE',
    bgColor: '#FAFAFA',
    bgSecondary: '#F5F5F5',
    bgThird: '#EEEEEE',
    textColor: '#212121',
    textSecondary: '#424242',
    textThird: '#757575',
    borderColor: '#E0E0E0',
    shadowColor: 'rgba(0, 0, 0, 0.08)',
    cardBg: '#FFFFFF',
    buttonPrimary: '#607D8B',
    buttonSecondary: '#ECEFF1',
    successColor: '#66BB6A',
    warningColor: '#FFA726',
    dangerColor: '#EF5350',
    infoColor: '#9E9E9E'
  }
}

/**
 * 主题 Store
 * 管理应用主题状态和切换
 */
export const useThemeStore = defineStore('theme', () => {
  // 当前主题名称
  const currentTheme = ref('light')

  // 主题切换动画进行中
  const isTransitioning = ref(false)

  /**
   * 获取当前主题配置
   */
  const theme = computed(() => themes[currentTheme.value])

  /**
   * 获取所有可用主题列表
   */
  const themeList = computed(() => {
    return Object.keys(themes).map(key => ({
      key,
      ...themes[key]
    }))
  })

  /**
   * 初始化主题
   * 从本地存储读取用户选择的主题
   */
  const initTheme = () => {
    try {
      const savedTheme = uni.getStorageSync('theme')
      if (savedTheme && themes[savedTheme]) {
        currentTheme.value = savedTheme
      }
      applyTheme()
    } catch (e) {
      console.error('初始化主题失败:', e)
    }
  }

  /**
   * 切换主题
   * @param {string} themeName - 主题名称
   */
  const setTheme = (themeName) => {
    if (!themes[themeName]) {
      console.error(`主题 ${themeName} 不存在`)
      return
    }

    // 设置过渡动画状态
    isTransitioning.value = true

    // 更新主题
    currentTheme.value = themeName

    // 应用主题
    applyTheme()

    // 保存到本地存储
    try {
      uni.setStorageSync('theme', themeName)
    } catch (e) {
      console.error('保存主题失败:', e)
    }

    // 300ms 后结束过渡动画
    setTimeout(() => {
      isTransitioning.value = false
    }, 300)

    // 提示用户
    uni.showToast({
      title: `已切换到${themes[themeName].name}主题`,
      icon: 'none',
      duration: 1500
    })
  }

  /**
   * 应用主题到页面
   * 通过 CSS Variables 动态设置颜色
   */
  const applyTheme = () => {
    const themeConfig = theme.value

    // 在小程序环境中，需要通过 page-meta 组件设置样式变量
    // 在 H5 环境中，可以直接设置 document.documentElement.style
    // #ifdef H5
    const root = document.documentElement
    Object.keys(themeConfig).forEach(key => {
      if (key !== 'name' && key !== 'icon') {
        root.style.setProperty(`--${toKebabCase(key)}`, themeConfig[key])
      }
    })
    // #endif

    // 小程序环境需要通过事件通知页面更新
    // #ifndef H5
    uni.$emit('theme-change', themeConfig)
    // #endif
  }

  /**
   * 将驼峰命名转换为短横线命名
   * @param {string} str - 驼峰命名字符串
   * @returns {string} 短横线命名字符串
   */
  const toKebabCase = (str) => {
    return str.replace(/([A-Z])/g, '-$1').toLowerCase()
  }

  /**
   * 切换到下一个主题（用于演示）
   */
  const nextTheme = () => {
    const keys = Object.keys(themes)
    const currentIndex = keys.indexOf(currentTheme.value)
    const nextIndex = (currentIndex + 1) % keys.length
    setTheme(keys[nextIndex])
  }

  return {
    currentTheme,
    theme,
    themeList,
    isTransitioning,
    initTheme,
    setTheme,
    nextTheme
  }
})
