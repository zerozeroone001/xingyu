<template>
	<!-- 空状态组件 -->
	<view class="empty-state fade-in">
		<view class="empty-icon">
			<text class="icon-text">{{ icon }}</text>
		</view>
		<view class="empty-text">
			<text class="text-primary">{{ text }}</text>
		</view>
		<view v-if="showButton" class="empty-button">
			<button class="btn-primary" @click="handleButtonClick">{{ buttonText }}</button>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'EmptyState',
		props: {
			// 图标emoji
			icon: {
				type: String,
				default: '📭'
			},
			// 提示文字
			text: {
				type: String,
				default: '暂无数据'
			},
			// 是否显示按钮
			showButton: {
				type: Boolean,
				default: false
			},
			// 按钮文字
			buttonText: {
				type: String,
				default: '刷新'
			}
		},
		methods: {
			/**
			 * 处理按钮点击
			 */
			handleButtonClick() {
				this.$emit('button-click')
			}
		}
	}
</script>

<style scoped>
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 120rpx 60rpx;
	}

	.empty-icon {
		margin-bottom: 32rpx;
	}

	.icon-text {
		font-size: 120rpx;
		opacity: 0.6;
	}

	.empty-text {
		margin-bottom: 40rpx;
	}

	.text-primary {
		font-size: 28rpx;
		color: var(--text-secondary, #666666);
	}

	.empty-button {
		width: 240rpx;
	}
</style>
