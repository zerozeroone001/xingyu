<template>
	<!-- 错误状态组件 -->
	<view class="error-state fade-in">
		<view class="error-icon">
			<text class="icon-text">{{ icon }}</text>
		</view>
		<view class="error-text">
			<text class="text-primary">{{ text }}</text>
		</view>
		<view class="error-button">
			<button class="btn-primary" @click="handleRetry">{{ buttonText }}</button>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'ErrorState',
		props: {
			// 错误图标emoji
			icon: {
				type: String,
				default: '😕'
			},
			// 错误提示文字
			text: {
				type: String,
				default: '加载失败'
			},
			// 按钮文字
			buttonText: {
				type: String,
				default: '重试'
			}
		},
		methods: {
			/**
			 * 处理重试点击
			 */
			handleRetry() {
				// 震动反馈
				uni.vibrateShort({
					type: 'light'
				})

				this.$emit('retry')
			}
		}
	}
</script>

<style scoped>
	.error-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 120rpx 60rpx;
	}

	.error-icon {
		margin-bottom: 32rpx;
	}

	.icon-text {
		font-size: 120rpx;
		opacity: 0.8;
	}

	.error-text {
		margin-bottom: 40rpx;
	}

	.text-primary {
		font-size: 28rpx;
		color: var(--text-secondary, #666666);
	}

	.error-button {
		width: 240rpx;
	}
</style>
