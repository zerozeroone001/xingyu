/**
 * 主题管理Store
 * 使用Vue3 Composition API管理主题状态
 * 支持主题切换和本地持久化
 */
import {
	ref,
	computed,
	watch
} from 'vue'
import {
	getTheme,
	getThemeList
} from '../utils/themes.js'

// 主题状态
const currentThemeKey = ref('light') // 当前主题key
const currentTheme = ref(getTheme('light')) // 当前主题配置对象

/**
 * 初始化主题
 * 从本地存储中读取上次选择的主题
 */
export function initTheme() {
	try {
		const savedTheme = uni.getStorageSync('theme')
		if (savedTheme) {
			setTheme(savedTheme)
		}
	} catch (e) {
		console.error('读取主题配置失败:', e)
	}
}

/**
 * 设置主题
 * @param {String} themeKey 主题key
 */
export function setTheme(themeKey) {
	console.log('切换主题:', themeKey)

	// 更新当前主题key
	currentThemeKey.value = themeKey

	// 更新当前主题配置
	currentTheme.value = getTheme(themeKey)

	// 保存到本地存储
	try {
		uni.setStorageSync('theme', themeKey)
	} catch (e) {
		console.error('保存主题配置失败:', e)
	}

	// 应用主题到全局
	applyTheme(currentTheme.value)
}

/**
 * 应用主题到全局
 * @param {Object} theme 主题配置对象
 */
function applyTheme(theme) {
	// 设置CSS变量到页面根元素
	// uni-app中需要通过页面样式来应用
	// 这里通过事件通知App.vue来应用主题
	uni.$emit('themeChange', theme)
}

/**
 * 获取当前主题key
 */
export function getCurrentThemeKey() {
	return currentThemeKey.value
}

/**
 * 获取当前主题配置
 */
export function getCurrentTheme() {
	return currentTheme.value
}

/**
 * 获取所有主题列表
 */
export function getAllThemes() {
	return getThemeList()
}

/**
 * 切换到下一个主题(用于快速预览)
 */
export function nextTheme() {
	const themes = getThemeList()
	const currentIndex = themes.findIndex(t => t.key === currentThemeKey.value)
	const nextIndex = (currentIndex + 1) % themes.length
	setTheme(themes[nextIndex].key)
}

// 导出响应式数据供组件使用
export function useTheme() {
	return {
		currentThemeKey,
		currentTheme,
		setTheme,
		getAllThemes,
		nextTheme
	}
}
