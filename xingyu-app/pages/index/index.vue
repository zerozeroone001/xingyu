<template>
	<view class="home-page" :style="pageStyle">
		<!-- 导航栏 -->
		<view class="nav-bar">
			<text class="nav-title">星语诗词</text>
			<view class="nav-right">
				<!-- 主题切换按钮 -->
				<ThemeSwitch />
			</view>
		</view>

		<!-- 页面内容 -->
		<scroll-view scroll-y class="page-content" refresher-enabled :refresher-triggered="refreshing"
			@refresherrefresh="handleRefresh">

			<!-- 加载中状态 -->
			<LoadingState v-if="loading" text="正在加载推荐诗词..." />

			<!-- 错误状态 -->
			<ErrorState v-else-if="error" :text="errorMessage" @retry="loadRecommendPoetry" />

			<!-- 空状态 -->
			<EmptyState v-else-if="!poetry" icon="📖" text="暂无推荐诗词" :show-button="true" buttonText="刷新"
				@button-click="loadRecommendPoetry" />

			<!-- 诗词推荐卡片 -->
			<view v-else>
				<PoetryCard :poetry="poetry" />

				<!-- 操作按钮 -->
				<view class="action-buttons">
					<button class="refresh-btn" @click="loadRecommendPoetry">
						<text class="btn-icon">🔄</text>
						<text class="btn-text">换一首</text>
					</button>
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
		</scroll-view>
	</view>
</template>

<script>
	import {
		getRecommendPoetry
	} from '../../api/poetry.js'
	import {
		useTheme
	} from '../../stores/theme.js'
	import PoetryCard from '../../components/poetry/PoetryCard.vue'
	import ThemeSwitch from '../../components/common/ThemeSwitch.vue'
	import LoadingState from '../../components/common/LoadingState.vue'
	import ErrorState from '../../components/common/ErrorState.vue'
	import EmptyState from '../../components/common/EmptyState.vue'

	export default {
		components: {
			PoetryCard,
			ThemeSwitch,
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
				refreshing: false, // 下拉刷新中

				// 数据
				poetry: null, // 推荐诗词
				dailyQuote: '读书破万卷，下笔如有神。', // 每日一句

				// 主题相关
				themeData: null
			}
		},
		computed: {
			/**
			 * 页面样式
			 * 根据当前主题动态设置CSS变量
			 */
			pageStyle() {
				if (!this.themeData) return {}

				const theme = this.themeData.currentTheme.value
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

			// 初始化主题数据
			this.themeData = useTheme()

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
			 */
			async loadRecommendPoetry() {
				console.log('加载推荐诗词')

				this.loading = true
				this.error = false
				this.errorMessage = ''

				try {
					// 调用API获取推荐诗词
					const data = await getRecommendPoetry()
					this.poetry = data

					console.log('推荐诗词:', data)
				} catch (err) {
					console.error('加载推荐诗词失败:', err)

					// 如果没有后端服务,使用模拟数据
					if (err.code === -1 || err.code === 404) {
						console.log('使用模拟数据')
						this.poetry = this.getMockPoetry()
					} else {
						this.error = true
						this.errorMessage = err.message || '加载失败,请重试'
					}
				} finally {
					this.loading = false
					this.refreshing = false
				}
			},

			/**
			 * 获取模拟数据
			 * 用于演示和开发调试
			 * @returns {Object} 模拟诗词数据
			 */
			getMockPoetry() {
				const mockPoems = [{
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
					}
				]

				// 随机返回一首
				return mockPoems[Math.floor(Math.random() * mockPoems.length)]
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
			 * 处理下拉刷新
			 */
			handleRefresh() {
				console.log('下拉刷新')
				this.refreshing = true
				this.loadRecommendPoetry()
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
		background-color: var(--bg-primary, #FFFFFF);
		transition: background-color 0.3s ease;
	}

	/* 导航栏 */
	.nav-bar {
		position: sticky;
		top: 0;
		z-index: 100;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 20rpx 32rpx;
		background-color: var(--bg-card, #FFFFFF);
		border-bottom: 1rpx solid var(--divider, #F0F0F0);
		box-shadow: 0 2rpx 8rpx var(--shadow, rgba(0, 0, 0, 0.05));
	}

	.nav-title {
		font-size: 36rpx;
		font-weight: bold;
		color: var(--text-primary, #1A1A1A);
		letter-spacing: 2rpx;
	}

	.nav-right {
		display: flex;
		align-items: center;
	}

	/* 页面内容 */
	.page-content {
		height: calc(100vh - 140rpx);
	}

	/* 操作按钮 */
	.action-buttons {
		display: flex;
		justify-content: center;
		padding: 32rpx;
	}

	.refresh-btn {
		display: flex;
		align-items: center;
		gap: 16rpx;
		padding: 24rpx 48rpx;
		background: linear-gradient(135deg, var(--primary, #2979FF) 0%, var(--primary-dark, #2962FF) 100%);
		color: var(--text-inverse, #FFFFFF);
		border: none;
		border-radius: 48rpx;
		box-shadow: 0 8rpx 20rpx var(--shadow, rgba(0, 0, 0, 0.1));
		transition: all 0.3s ease;
	}

	.refresh-btn:active {
		transform: scale(0.95);
		box-shadow: 0 4rpx 12rpx var(--shadow, rgba(0, 0, 0, 0.15));
	}

	.btn-icon {
		font-size: 32rpx;
	}

	.btn-text {
		font-size: 28rpx;
		font-weight: 500;
	}

	/* 快捷入口 */
	.quick-links {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 24rpx;
		padding: 32rpx;
		margin-top: 32rpx;
	}

	.quick-link-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 32rpx 24rpx;
		background-color: var(--bg-card, #FFFFFF);
		border-radius: 16rpx;
		box-shadow: 0 4rpx 12rpx var(--shadow, rgba(0, 0, 0, 0.06));
		transition: all 0.3s ease;
	}

	.quick-link-item:active {
		transform: scale(0.95);
		box-shadow: 0 2rpx 8rpx var(--shadow, rgba(0, 0, 0, 0.1));
	}

	.link-icon {
		font-size: 56rpx;
		margin-bottom: 16rpx;
	}

	.link-text {
		font-size: 24rpx;
		color: var(--text-secondary, #666666);
	}

	/* 每日一句 */
	.daily-quote {
		margin: 32rpx;
		padding: 32rpx;
		background: linear-gradient(135deg, var(--bg-secondary, #F7F8FA) 0%, var(--bg-card, #FFFFFF) 100%);
		border-radius: 16rpx;
		border-left: 6rpx solid var(--primary, #2979FF);
	}

	.quote-header {
		margin-bottom: 20rpx;
	}

	.quote-title {
		font-size: 28rpx;
		font-weight: bold;
		color: var(--text-primary, #1A1A1A);
	}

	.quote-content {
		padding: 16rpx 0;
	}

	.quote-text {
		font-size: 26rpx;
		line-height: 1.8;
		color: var(--text-secondary, #666666);
		font-style: italic;
	}
</style>
