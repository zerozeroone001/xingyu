/**
 * 主题配置文件
 * 定义了10种精美主题,每种主题包含完整的颜色系统
 *
 * 主题包括:
 * 1. light - 明亮主题(默认)
 * 2. dark - 暗黑主题
 * 3. forest - 森林主题
 * 4. purple - 炫紫主题
 * 5. ocean - 海洋主题
 * 6. sunset - 日落主题
 * 7. sakura - 樱花主题
 * 8. night - 夜空主题
 * 9. autumn - 秋叶主题
 * 10. ice - 冰雪主题
 */

export const themes = {
	// 1. 明亮主题 - 清新简洁
	light: {
		name: '明亮',
		icon: '☀️',

		// 背景色
		bgPrimary: '#FFFFFF',           // 主背景
		bgSecondary: '#F7F8FA',         // 次要背景
		bgCard: '#FFFFFF',              // 卡片背景

		// 文字颜色
		textPrimary: '#1A1A1A',         // 主文字
		textSecondary: '#666666',       // 次要文字
		textTertiary: '#999999',        // 三级文字
		textInverse: '#FFFFFF',         // 反色文字

		// 主题色
		primary: '#2979FF',             // 主色调
		primaryLight: '#82B1FF',        // 主色调-浅
		primaryDark: '#2962FF',         // 主色调-深

		// 强调色
		accent: '#FF6B6B',              // 强调色
		accentLight: '#FFB3B3',         // 强调色-浅

		// 边框和分割线
		border: '#E5E5E5',              // 边框色
		divider: '#F0F0F0',             // 分割线

		// 状态色
		success: '#4CAF50',             // 成功
		warning: '#FF9800',             // 警告
		error: '#F44336',               // 错误
		info: '#2196F3',                // 信息

		// 阴影
		shadow: 'rgba(0, 0, 0, 0.08)',  // 阴影颜色

		// 渐变色
		gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
	},

	// 2. 暗黑主题 - 护眼舒适
	dark: {
		name: '暗黑',
		icon: '🌙',

		bgPrimary: '#0F0F0F',
		bgSecondary: '#1A1A1A',
		bgCard: '#1E1E1E',

		textPrimary: '#E0E0E0',
		textSecondary: '#B0B0B0',
		textTertiary: '#808080',
		textInverse: '#1A1A1A',

		primary: '#BB86FC',
		primaryLight: '#E1BEE7',
		primaryDark: '#9C27B0',

		accent: '#03DAC6',
		accentLight: '#B2DFDB',

		border: '#2C2C2C',
		divider: '#252525',

		success: '#66BB6A',
		warning: '#FFA726',
		error: '#EF5350',
		info: '#42A5F5',

		shadow: 'rgba(0, 0, 0, 0.5)',

		gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
	},

	// 3. 森林主题 - 自然清新
	forest: {
		name: '森林',
		icon: '🌲',

		bgPrimary: '#F5F9F5',
		bgSecondary: '#E8F5E9',
		bgCard: '#FFFFFF',

		textPrimary: '#1B5E20',
		textSecondary: '#388E3C',
		textTertiary: '#66BB6A',
		textInverse: '#FFFFFF',

		primary: '#43A047',
		primaryLight: '#81C784',
		primaryDark: '#2E7D32',

		accent: '#8BC34A',
		accentLight: '#C5E1A5',

		border: '#C8E6C9',
		divider: '#E8F5E9',

		success: '#4CAF50',
		warning: '#FFC107',
		error: '#F44336',
		info: '#00BCD4',

		shadow: 'rgba(67, 160, 71, 0.1)',

		gradient: 'linear-gradient(135deg, #43A047 0%, #66BB6A 100%)',
	},

	// 4. 炫紫主题 - 梦幻神秘
	purple: {
		name: '炫紫',
		icon: '💜',

		bgPrimary: '#F3E5F5',
		bgSecondary: '#E1BEE7',
		bgCard: '#FFFFFF',

		textPrimary: '#4A148C',
		textSecondary: '#6A1B9A',
		textTertiary: '#8E24AA',
		textInverse: '#FFFFFF',

		primary: '#9C27B0',
		primaryLight: '#CE93D8',
		primaryDark: '#7B1FA2',

		accent: '#E91E63',
		accentLight: '#F8BBD0',

		border: '#E1BEE7',
		divider: '#F3E5F5',

		success: '#9C27B0',
		warning: '#FF6F00',
		error: '#D32F2F',
		info: '#7C4DFF',

		shadow: 'rgba(156, 39, 176, 0.15)',

		gradient: 'linear-gradient(135deg, #9C27B0 0%, #E91E63 100%)',
	},

	// 5. 海洋主题 - 清凉宁静
	ocean: {
		name: '海洋',
		icon: '🌊',

		bgPrimary: '#E0F7FA',
		bgSecondary: '#B2EBF2',
		bgCard: '#FFFFFF',

		textPrimary: '#006064',
		textSecondary: '#00838F',
		textTertiary: '#0097A7',
		textInverse: '#FFFFFF',

		primary: '#00BCD4',
		primaryLight: '#80DEEA',
		primaryDark: '#0097A7',

		accent: '#03A9F4',
		accentLight: '#B3E5FC',

		border: '#B2EBF2',
		divider: '#E0F7FA',

		success: '#00BCD4',
		warning: '#FF9800',
		error: '#F44336',
		info: '#2196F3',

		shadow: 'rgba(0, 188, 212, 0.12)',

		gradient: 'linear-gradient(135deg, #00BCD4 0%, #03A9F4 100%)',
	},

	// 6. 日落主题 - 温暖浪漫
	sunset: {
		name: '日落',
		icon: '🌅',

		bgPrimary: '#FFF3E0',
		bgSecondary: '#FFE0B2',
		bgCard: '#FFFFFF',

		textPrimary: '#E65100',
		textSecondary: '#EF6C00',
		textTertiary: '#F57C00',
		textInverse: '#FFFFFF',

		primary: '#FF9800',
		primaryLight: '#FFCC80',
		primaryDark: '#F57C00',

		accent: '#FF5722',
		accentLight: '#FFCCBC',

		border: '#FFE0B2',
		divider: '#FFF3E0',

		success: '#FF9800',
		warning: '#FFC107',
		error: '#F44336',
		info: '#FF6F00',

		shadow: 'rgba(255, 152, 0, 0.15)',

		gradient: 'linear-gradient(135deg, #FF9800 0%, #FF5722 100%)',
	},

	// 7. 樱花主题 - 浪漫优雅
	sakura: {
		name: '樱花',
		icon: '🌸',

		bgPrimary: '#FCE4EC',
		bgSecondary: '#F8BBD0',
		bgCard: '#FFFFFF',

		textPrimary: '#880E4F',
		textSecondary: '#AD1457',
		textTertiary: '#C2185B',
		textInverse: '#FFFFFF',

		primary: '#E91E63',
		primaryLight: '#F48FB1',
		primaryDark: '#C2185B',

		accent: '#FF4081',
		accentLight: '#FF80AB',

		border: '#F8BBD0',
		divider: '#FCE4EC',

		success: '#E91E63',
		warning: '#FF6F00',
		error: '#D32F2F',
		info: '#F06292',

		shadow: 'rgba(233, 30, 99, 0.12)',

		gradient: 'linear-gradient(135deg, #E91E63 0%, #FF4081 100%)',
	},

	// 8. 夜空主题 - 深邃神秘
	night: {
		name: '夜空',
		icon: '🌌',

		bgPrimary: '#1A237E',
		bgSecondary: '#283593',
		bgCard: '#303F9F',

		textPrimary: '#E8EAF6',
		textSecondary: '#C5CAE9',
		textTertiary: '#9FA8DA',
		textInverse: '#1A237E',

		primary: '#5C6BC0',
		primaryLight: '#9FA8DA',
		primaryDark: '#3F51B5',

		accent: '#7E57C2',
		accentLight: '#B39DDB',

		border: '#3F51B5',
		divider: '#283593',

		success: '#5C6BC0',
		warning: '#FFB300',
		error: '#E53935',
		info: '#42A5F5',

		shadow: 'rgba(0, 0, 0, 0.4)',

		gradient: 'linear-gradient(135deg, #283593 0%, #5C6BC0 100%)',
	},

	// 9. 秋叶主题 - 温馨怀旧
	autumn: {
		name: '秋叶',
		icon: '🍂',

		bgPrimary: '#FBE9E7',
		bgSecondary: '#FFCCBC',
		bgCard: '#FFFFFF',

		textPrimary: '#BF360C',
		textSecondary: '#D84315',
		textTertiary: '#E64A19',
		textInverse: '#FFFFFF',

		primary: '#FF5722',
		primaryLight: '#FF8A65',
		primaryDark: '#E64A19',

		accent: '#FF6F00',
		accentLight: '#FFB74D',

		border: '#FFCCBC',
		divider: '#FBE9E7',

		success: '#FF5722',
		warning: '#FFC107',
		error: '#F44336',
		info: '#FF6F00',

		shadow: 'rgba(255, 87, 34, 0.12)',

		gradient: 'linear-gradient(135deg, #FF5722 0%, #FF6F00 100%)',
	},

	// 10. 冰雪主题 - 清冷纯净
	ice: {
		name: '冰雪',
		icon: '❄️',

		bgPrimary: '#E1F5FE',
		bgSecondary: '#B3E5FC',
		bgCard: '#FFFFFF',

		textPrimary: '#01579B',
		textSecondary: '#0277BD',
		textTertiary: '#0288D1',
		textInverse: '#FFFFFF',

		primary: '#03A9F4',
		primaryLight: '#81D4FA',
		primaryDark: '#0288D1',

		accent: '#00BCD4',
		accentLight: '#B2EBF2',

		border: '#B3E5FC',
		divider: '#E1F5FE',

		success: '#03A9F4',
		warning: '#FFA000',
		error: '#E53935',
		info: '#2196F3',

		shadow: 'rgba(3, 169, 244, 0.1)',

		gradient: 'linear-gradient(135deg, #03A9F4 0%, #00BCD4 100%)',
	}
}

/**
 * 获取所有主题列表
 * @returns {Array} 主题列表
 */
export function getThemeList() {
	return Object.keys(themes).map(key => ({
		key,
		name: themes[key].name,
		icon: themes[key].icon
	}))
}

/**
 * 获取主题配置
 * @param {String} themeKey 主题key
 * @returns {Object} 主题配置对象
 */
export function getTheme(themeKey = 'light') {
	return themes[themeKey] || themes.light
}
