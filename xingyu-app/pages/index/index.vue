<template>
	<view class="home-page" :style="pageStyle">
		<!-- 顶部信息栏 -->
		<view class="top-bar">
			<DateWeather />
			<ThemeSwitch />
		</view>

		<!-- 页面内容 -->
		<view class="page-content">
			<!-- 加载中状态 -->
			<LoadingState v-if="loading" text="正在加载推荐诗词..." />

			<!-- 错误状态 -->
			<ErrorState v-else-if="error" :text="errorMessage" @retry="loadRecommendPoetry" />

			<!-- 空状态 -->
			<EmptyState v-else-if="poetryList.length === 0" icon="📖" text="暂无推荐诗词" :show-button="true"
				buttonText="刷新" @button-click="loadRecommendPoetry" />

			<!-- 诗词轮播区域 -->
			<view v-else class="poetry-swiper-container">
				<swiper class="poetry-swiper" :current="currentIndex" @change="onSwiperChange"
					:circular="true" :duration="300">
					<swiper-item v-for="(poem, index) in poetryList" :key="poem.id">
						<view class="swiper-item-wrapper">
							<PoetryCard :poetry="poem" />
						</view>
					</swiper-item>
				</swiper>

				<!-- 滑动指示器 -->
				<view class="swipe-indicator">
					<view class="indicator-left">
						<text class="indicator-icon">←</text>
						<text class="indicator-text">上一首</text>
					</view>
					<view class="indicator-dots">
						<view v-for="(poem, index) in poetryList" :key="index"
							:class="['dot', index === currentIndex ? 'active' : '']"></view>
					</view>
					<view class="indicator-right">
						<text class="indicator-text">下一首</text>
						<text class="indicator-icon">→</text>
					</view>
				</view>

				<!-- 快捷入口 -->
				<view class="quick-links">
					<view class="quick-link-item" @click="navigateTo('/pages/ai/generate')">
						<view class="link-icon">🤖</view>
						<text class="link-text">AI创作</text>
					</view>
					<view class="quick-link-item" @click="navigateTo('/pages/poetry/list')">
						<view class="link-icon">🔍</view>
						<text class="link-text">搜索</text>
					</view>
					<view class="quick-link-item" @click="navigateTo('/pages/game/lobby')">
						<view class="link-icon">🎮</view>
						<text class="link-text">飞花令</text>
					</view>
				</view>

				<!-- 每日一句 -->
				<view class="daily-quote">
					<view class="quote-header">
						<text class="quote-title">📅 每日一句</text>
					</view>
					<view class="quote-content">
						<text class="quote-text">{{ dailyQuote }}</text>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	// 注意: 当前版本使用模拟数据,不请求后端接口
	import {
		useTheme
	} from '../../stores/theme.js'
	import PoetryCard from '../../components/poetry/PoetryCard.vue'
	import ThemeSwitch from '../../components/common/ThemeSwitch.vue'
	import DateWeather from '../../components/common/DateWeather.vue'
	import LoadingState from '../../components/common/LoadingState.vue'
	import ErrorState from '../../components/common/ErrorState.vue'
	import EmptyState from '../../components/common/EmptyState.vue'

	export default {
		components: {
			PoetryCard,
			ThemeSwitch,
			DateWeather,
			LoadingState,
			ErrorState,
			EmptyState
		},
		data() {
			return {
				// 页面状态
				loading: false, // 加载中
				error: false, // 是否有错误
				errorMessage: '', // 错误信息

				// 数据
				poetryList: [], // 诗词列表
				currentIndex: 0, // 当前显示的诗词索引
				dailyQuote: '读书破万卷，下笔如有神。', // 每日一句

				// 主题相关 - 直接在 data 中初始化,避免计算属性访问 undefined
				themeData: useTheme()
			}
		},
		computed: {
			/**
			 * 页面样式
			 * 根据当前主题动态设置CSS变量
			 */
			pageStyle() {
				// 检查 themeData 是否存在
				if (!this.themeData || !this.themeData.currentTheme) return {}

				const theme = this.themeData.currentTheme.value

				// 检查 theme 对象是否存在
				if (!theme) return {}

				return {
					'--bg-primary': theme.bgPrimary,
					'--bg-secondary': theme.bgSecondary,
					'--bg-card': theme.bgCard,
					'--text-primary': theme.textPrimary,
					'--text-secondary': theme.textSecondary,
					'--text-tertiary': theme.textTertiary,
					'--text-inverse': theme.textInverse,
					'--primary': theme.primary,
					'--primary-light': theme.primaryLight,
					'--primary-dark': theme.primaryDark,
					'--accent': theme.accent,
					'--border': theme.border,
					'--divider': theme.divider,
					'--shadow': theme.shadow
				}
			}
		},
		onLoad() {
			console.log('首页加载')

			// 监听主题变化
			uni.$on('themeChange', this.handleThemeChange)

			// 加载推荐诗词
			this.loadRecommendPoetry()

			// 加载每日一句
			this.loadDailyQuote()
		},
		onUnload() {
			// 取消监听
			uni.$off('themeChange', this.handleThemeChange)
		},
		methods: {
			/**
			 * 加载推荐诗词
			 * 使用模拟数据,不请求后端接口
			 */
			async loadRecommendPoetry() {
				console.log('加载推荐诗词(使用模拟数据)')

				this.loading = true
				this.error = false
				this.errorMessage = ''

				// 模拟网络请求延迟,提升用户体验
				await new Promise(resolve => setTimeout(resolve, 500))

				// 直接使用模拟数据
				this.poetryList = this.getMockPoetryList()
				this.currentIndex = 0
				console.log('推荐诗词列表:', this.poetryList)

				this.loading = false
			},

			/**
			 * 获取模拟数据列表
			 * 用于演示和开发调试
			 * @returns {Array} 模拟诗词数据数组
			 */
			getMockPoetryList() {
				return [{
						id: 1,
						title: '静夜思',
						content: '床前明月光,疑是地上霜。举头望明月,低头思故乡。',
						author: '李白',
						dynasty: '唐代',
						read_count: 12345,
						like_count: 567,
						comment_count: 89
					},
					{
						id: 2,
						title: '春晓',
						content: '春眠不觉晓,处处闻啼鸟。夜来风雨声,花落知多少。',
						author: '孟浩然',
						dynasty: '唐代',
						read_count: 23456,
						like_count: 678,
						comment_count: 123
					},
					{
						id: 3,
						title: '登鹳雀楼',
						content: '白日依山尽,黄河入海流。欲穷千里目,更上一层楼。',
						author: '王之涣',
						dynasty: '唐代',
						read_count: 34567,
						like_count: 789,
						comment_count: 234
					},
					{
						id: 4,
						title: '望庐山瀑布',
						content: '日照香炉生紫烟,遥看瀑布挂前川。飞流直下三千尺,疑是银河落九天。',
						author: '李白',
						dynasty: '唐代',
						read_count: 45678,
						like_count: 890,
						comment_count: 345
					},
					{
						id: 5,
						title: '早发白帝城',
						content: '朝辞白帝彩云间,千里江陵一日还。两岸猿声啼不住,轻舟已过万重山。',
						author: '李白',
						dynasty: '唐代',
						read_count: 56789,
						like_count: 901,
						comment_count: 456
					}
				]
			},

			/**
			 * 处理滑动切换事件
			 */
			onSwiperChange(e) {
				this.currentIndex = e.detail.current
				console.log('切换到诗词索引:', this.currentIndex)

				// 震动反馈
				uni.vibrateShort({
					type: 'light'
				})
			},

			/**
			 * 加载每日一句
			 */
			loadDailyQuote() {
				const quotes = [
					'读书破万卷,下笔如有神。',
					'书山有路勤为径,学海无涯苦作舟。',
					'黑发不知勤学早,白首方悔读书迟。',
					'少壮不努力,老大徒伤悲。',
					'问渠那得清如许,为有源头活水来。'
				]
				this.dailyQuote = quotes[Math.floor(Math.random() * quotes.length)]
			},

			/**
			 * 处理主题变化
			 */
			handleThemeChange(theme) {
				console.log('首页收到主题变化:', theme.name)
				// 页面样式会自动更新,这里可以做其他处理
			},

			/**
			 * 页面跳转
			 * @param {String} url 跳转路径
			 */
			navigateTo(url) {
				uni.showToast({
					title: '功能开发中',
					icon: 'none',
					duration: 1500
				})
				// 震动反馈
				uni.vibrateShort({
					type: 'light'
				})
				// TODO: 实际跳转
				// uni.navigateTo({ url })
			}
		}
	}
</script>

<style scoped>
	/* 首页容器 */
	.home-page {
		min-height: 100vh;
		background: linear-gradient(180deg,
				var(--bg-secondary, #F7F8FA) 0%,
				var(--bg-primary, #FFFFFF) 30%);
		transition: background-color 0.3s ease;
	}

	/* 顶部信息栏 */
	.top-bar {
		position: sticky;
		top: 0;
		z-index: 100;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 32rpx 40rpx 24rpx;
		background: linear-gradient(180deg,
				var(--bg-card, #FFFFFF) 0%,
				rgba(255, 255, 255, 0.95) 100%);
		backdrop-filter: blur(20rpx);
		border-bottom: 1rpx solid var(--divider, #F0F0F0);
		box-shadow: 0 4rpx 16rpx var(--shadow, rgba(0, 0, 0, 0.04));
	}

	/* 页面内容 */
	.page-content {
		min-height: calc(100vh - 120rpx);
		padding-top: 20rpx;
	}

	/* 诗词轮播容器 */
	.poetry-swiper-container {
		padding-bottom: 40rpx;
	}

	/* 诗词轮播 */
	.poetry-swiper {
		height: 500rpx;
		margin-bottom: 24rpx;
	}

	.swiper-item-wrapper {
		height: 100%;
		padding: 0 32rpx;
	}

	/* 滑动指示器 */
	.swipe-indicator {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 24rpx 40rpx;
		margin: 0 32rpx 32rpx;
		background-color: var(--bg-card, #FFFFFF);
		border-radius: 24rpx;
		box-shadow: 0 4rpx 16rpx var(--shadow, rgba(0, 0, 0, 0.06));
	}

	.indicator-left,
	.indicator-right {
		display: flex;
		align-items: center;
		gap: 8rpx;
	}

	.indicator-icon {
		font-size: 32rpx;
		color: var(--primary, #2979FF);
	}

	.indicator-text {
		font-size: 24rpx;
		color: var(--text-secondary, #666666);
	}

	.indicator-dots {
		display: flex;
		gap: 12rpx;
	}

	.dot {
		width: 12rpx;
		height: 12rpx;
		background-color: var(--divider, #E0E0E0);
		border-radius: 50%;
		transition: all 0.3s ease;
	}

	.dot.active {
		width: 32rpx;
		background: linear-gradient(90deg,
				var(--primary, #2979FF) 0%,
				var(--primary-dark, #2962FF) 100%);
		border-radius: 6rpx;
	}

	/* 快捷入口 */
	.quick-links {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 24rpx;
		padding: 0 32rpx 32rpx;
	}

	.quick-link-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 40rpx 24rpx;
		background: linear-gradient(135deg,
				var(--bg-card, #FFFFFF) 0%,
				var(--bg-secondary, #F7F8FA) 100%);
		border-radius: 20rpx;
		box-shadow: 0 4rpx 16rpx var(--shadow, rgba(0, 0, 0, 0.06));
		border: 2rpx solid var(--border, #F0F0F0);
		transition: all 0.3s ease;
	}

	.quick-link-item:active {
		transform: translateY(4rpx);
		box-shadow: 0 2rpx 8rpx var(--shadow, rgba(0, 0, 0, 0.1));
	}

	.link-icon {
		font-size: 64rpx;
		margin-bottom: 16rpx;
		filter: drop-shadow(0 2rpx 4rpx rgba(0, 0, 0, 0.1));
	}

	.link-text {
		font-size: 26rpx;
		font-weight: 500;
		color: var(--text-primary, #1A1A1A);
	}

	/* 每日一句 */
	.daily-quote {
		margin: 32rpx;
		padding: 40rpx;
		background: linear-gradient(135deg,
				var(--primary-light, #E3F2FD) 0%,
				var(--bg-card, #FFFFFF) 100%);
		border-radius: 24rpx;
		border-left: 8rpx solid var(--primary, #2979FF);
		box-shadow: 0 8rpx 24rpx var(--shadow, rgba(41, 121, 255, 0.1));
		position: relative;
		overflow: hidden;
	}

	.daily-quote::before {
		content: '"';
		position: absolute;
		top: -20rpx;
		left: 20rpx;
		font-size: 200rpx;
		color: var(--primary, #2979FF);
		opacity: 0.05;
		font-family: Georgia, serif;
	}

	.quote-header {
		margin-bottom: 24rpx;
		position: relative;
		z-index: 1;
	}

	.quote-title {
		font-size: 30rpx;
		font-weight: bold;
		color: var(--primary, #2979FF);
		letter-spacing: 1rpx;
	}

	.quote-content {
		padding: 16rpx 0;
		position: relative;
		z-index: 1;
	}

	.quote-text {
		font-size: 28rpx;
		line-height: 2;
		color: var(--text-primary, #1A1A1A);
		font-style: italic;
		font-weight: 500;
	}
</style>
