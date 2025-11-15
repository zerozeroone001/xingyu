<template>
	<!-- 诗词推荐卡片 -->
	<view class="poetry-card card fade-in" @click="handleCardClick">
		<!-- 背景装饰 -->
		<view class="card-decoration" :style="{ background: decorationGradient }"></view>

		<!-- 卡片内容 -->
		<view class="card-content">
			<!-- 标题 -->
			<view class="poetry-title">
				<text class="title-text">{{ poetry.title || '无题' }}</text>
			</view>

			<!-- 作者信息 -->
			<view class="poetry-author">
				<text class="author-dynasty">{{ poetry.dynasty || '未知' }}</text>
				<text class="author-dot">·</text>
				<text class="author-name">{{ poetry.author || '佚名' }}</text>
			</view>

			<!-- 诗词内容 -->
			<view class="poetry-content">
				<text class="content-text">{{ formatContent(poetry.content) }}</text>
			</view>

			<!-- 互动数据 -->
			<view class="poetry-stats">
				<view class="stat-item">
					<text class="stat-icon">👁️</text>
					<text class="stat-text">{{ formatNumber(poetry.read_count) }}</text>
				</view>
				<view class="stat-item">
					<text class="stat-icon">❤️</text>
					<text class="stat-text">{{ formatNumber(poetry.like_count) }}</text>
				</view>
				<view class="stat-item">
					<text class="stat-icon">💬</text>
					<text class="stat-text">{{ formatNumber(poetry.comment_count) }}</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import {
		getCurrentTheme
	} from '../../stores/theme.js'

	export default {
		name: 'PoetryCard',
		props: {
			// 诗词数据
			poetry: {
				type: Object,
				required: true,
				default: () => ({
					id: 0,
					title: '',
					content: '',
					author: '',
					dynasty: '',
					read_count: 0,
					like_count: 0,
					comment_count: 0
				})
			}
		},
		computed: {
			/**
			 * 装饰背景渐变色
			 * 使用当前主题的渐变色
			 */
			decorationGradient() {
				const theme = getCurrentTheme()
				return theme.gradient
			}
		},
		methods: {
			/**
			 * 格式化诗词内容
			 * 只显示前4句或前100字
			 * @param {String} content 诗词内容
			 * @returns {String} 格式化后的内容
			 */
			formatContent(content) {
				if (!content) return '暂无内容'

				// 按逗号、句号、问号、感叹号分句
				const lines = content.split(/[,。?!]/g).filter(line => line.trim())

				// 取前4句
				const displayLines = lines.slice(0, 4)

				// 拼接并添加换行
				let result = displayLines.join(',\n')

				// 如果超过4句,添加省略号
				if (lines.length > 4) {
					result += '...'
				}

				// 限制总长度
				if (result.length > 100) {
					result = result.substring(0, 100) + '...'
				}

				return result
			},

			/**
			 * 格式化数字
			 * 大于1000显示为1k+
			 * @param {Number} num 数字
			 * @returns {String} 格式化后的字符串
			 */
			formatNumber(num) {
				if (!num || num === 0) return '0'
				if (num >= 10000) {
					return (num / 10000).toFixed(1) + 'w'
				}
				if (num >= 1000) {
					return (num / 1000).toFixed(1) + 'k'
				}
				return String(num)
			},

			/**
			 * 处理卡片点击
			 * 跳转到诗词详情页
			 */
			handleCardClick() {
				if (!this.poetry.id) {
					uni.showToast({
						title: '诗词信息不完整',
						icon: 'none'
					})
					return
				}

				// 震动反馈
				uni.vibrateShort({
					type: 'light'
				})

				// 跳转到详情页
				uni.navigateTo({
					url: `/pages/poetry/detail?id=${this.poetry.id}`
				})
			}
		}
	}
</script>

<style scoped>
	/* 诗词卡片 */
	.poetry-card {
		position: relative;
		margin: 32rpx;
		padding: 40rpx;
		overflow: hidden;
		min-height: 500rpx;
	}

	/* 背景装饰 */
	.card-decoration {
		position: absolute;
		top: -50%;
		right: -50%;
		width: 200%;
		height: 200%;
		opacity: 0.08;
		transform: rotate(15deg);
		pointer-events: none;
	}

	/* 卡片内容 */
	.card-content {
		position: relative;
		z-index: 1;
	}

	/* 诗词标题 */
	.poetry-title {
		margin-bottom: 24rpx;
		text-align: center;
	}

	.title-text {
		font-size: 44rpx;
		font-weight: bold;
		color: var(--text-primary, #1A1A1A);
		letter-spacing: 4rpx;
	}

	/* 作者信息 */
	.poetry-author {
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 40rpx;
	}

	.author-dynasty,
	.author-name {
		font-size: 26rpx;
		color: var(--text-secondary, #666666);
	}

	.author-dot {
		margin: 0 12rpx;
		color: var(--text-tertiary, #999999);
	}

	/* 诗词内容 */
	.poetry-content {
		margin-bottom: 40rpx;
		padding: 32rpx 0;
		min-height: 280rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.content-text {
		font-size: 32rpx;
		line-height: 2;
		color: var(--text-primary, #1A1A1A);
		text-align: center;
		white-space: pre-line;
		letter-spacing: 2rpx;
	}

	/* 互动数据 */
	.poetry-stats {
		display: flex;
		align-items: center;
		justify-content: space-around;
		padding-top: 32rpx;
		border-top: 1rpx solid var(--divider, #F0F0F0);
	}

	.stat-item {
		display: flex;
		align-items: center;
		gap: 8rpx;
	}

	.stat-icon {
		font-size: 32rpx;
	}

	.stat-text {
		font-size: 24rpx;
		color: var(--text-secondary, #666666);
	}

	/* 卡片点击动画 */
	.poetry-card:active {
		transform: scale(0.98);
	}
</style>
