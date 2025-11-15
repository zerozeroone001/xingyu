<template>
	<!-- 加载中组件 -->
	<view class="loading-state">
		<view class="loading-spinner">
			<view class="spinner" :style="{ borderTopColor: spinnerColor }"></view>
		</view>
		<view v-if="text" class="loading-text">
			<text class="text-secondary">{{ text }}</text>
		</view>
	</view>
</template>

<script>
	import {
		getCurrentTheme
	} from '../../stores/theme.js'

	export default {
		name: 'LoadingState',
		props: {
			// 加载文字
			text: {
				type: String,
				default: '加载中...'
			}
		},
		computed: {
			/**
			 * 加载动画颜色
			 * 使用当前主题的主色调
			 */
			spinnerColor() {
				const theme = getCurrentTheme()
				return theme.primary
			}
		}
	}
</script>

<style scoped>
	.loading-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 120rpx 60rpx;
	}

	.loading-spinner {
		margin-bottom: 32rpx;
	}

	/* 加载动画 */
	.spinner {
		width: 80rpx;
		height: 80rpx;
		border: 6rpx solid rgba(0, 0, 0, 0.1);
		border-top-color: var(--primary, #2979FF);
		border-radius: 50%;
		animation: rotate 0.8s linear infinite;
	}

	@keyframes rotate {
		from {
			transform: rotate(0deg);
		}

		to {
			transform: rotate(360deg);
		}
	}

	.loading-text {
		text-align: center;
	}

	.text-secondary {
		font-size: 28rpx;
		color: var(--text-secondary, #666666);
	}
</style>
