<template>
	<!-- 主题切换组件 -->
	<view class="theme-switch">
		<!-- 主题切换按钮 -->
		<view class="theme-trigger" @click="showModal = true">
			<text class="theme-icon">{{ currentThemeIcon }}</text>
			<text class="theme-text">主题</text>
		</view>

		<!-- 主题选择弹窗 -->
		<view v-if="showModal" class="theme-modal" @click="showModal = false">
			<view class="modal-content" @click.stop>
				<view class="modal-header">
					<text class="modal-title">选择主题</text>
					<text class="modal-close" @click="showModal = false">✕</text>
				</view>

				<!-- 主题网格 -->
				<view class="theme-grid">
					<view v-for="theme in themeList" :key="theme.key" class="theme-item"
						:class="{ active: currentThemeKey === theme.key }" @click="handleThemeChange(theme.key)">
						<view class="theme-preview"
							:style="{ background: getThemePreviewGradient(theme.key) }">
							<text class="theme-item-icon">{{ theme.icon }}</text>
						</view>
						<text class="theme-name">{{ theme.name }}</text>
						<!-- 选中标记 -->
						<view v-if="currentThemeKey === theme.key" class="theme-check">
							<text class="check-icon">✓</text>
						</view>
					</view>
				</view>

				<!-- 说明文字 -->
				<view class="theme-tip">
					<text class="tip-text">💡 主题会自动保存,下次打开应用时生效</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import {
		useTheme
	} from '../../stores/theme.js'
	import {
		getTheme
	} from '../../utils/themes.js'

	export default {
		name: 'ThemeSwitch',
		data() {
			return {
				showModal: false, // 是否显示主题选择弹窗
			}
		},
		computed: {
			// 获取主题相关数据
			themeData() {
				return useTheme()
			},
			// 当前主题key
			currentThemeKey() {
				return this.themeData.currentThemeKey.value
			},
			// 当前主题图标
			currentThemeIcon() {
				const theme = this.themeData.currentTheme.value
				return theme.icon
			},
			// 主题列表
			themeList() {
				return this.themeData.getAllThemes()
			}
		},
		methods: {
			/**
			 * 处理主题切换
			 * @param {String} themeKey 主题key
			 */
			handleThemeChange(themeKey) {
				// 切换主题
				this.themeData.setTheme(themeKey)

				// 震动反馈
				uni.vibrateShort({
					type: 'light'
				})

				// 提示
				uni.showToast({
					title: '主题已切换',
					icon: 'success',
					duration: 1500
				})

				// 延迟关闭弹窗,让用户看到切换效果
				setTimeout(() => {
					this.showModal = false
				}, 300)
			},

			/**
			 * 获取主题预览渐变色
			 * @param {String} themeKey 主题key
			 * @returns {String} CSS渐变字符串
			 */
			getThemePreviewGradient(themeKey) {
				const theme = getTheme(themeKey)
				return theme.gradient
			}
		}
	}
</script>

<style scoped>
	/* 主题切换按钮 */
	.theme-trigger {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 16rpx;
		cursor: pointer;
	}

	.theme-icon {
		font-size: 48rpx;
		margin-bottom: 8rpx;
	}

	.theme-text {
		font-size: 24rpx;
		color: var(--text-secondary, #666666);
	}

	/* 主题选择弹窗 */
	.theme-modal {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 9999;
		animation: fadeIn 0.3s ease;
	}

	.modal-content {
		background-color: var(--bg-card, #FFFFFF);
		border-radius: 24rpx;
		width: 90%;
		max-width: 600rpx;
		max-height: 80vh;
		overflow-y: auto;
		animation: slideUp 0.3s ease;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}

		to {
			opacity: 1;
		}
	}

	@keyframes slideUp {
		from {
			transform: translateY(100rpx);
			opacity: 0;
		}

		to {
			transform: translateY(0);
			opacity: 1;
		}
	}

	/* 弹窗头部 */
	.modal-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 32rpx;
		border-bottom: 1rpx solid var(--divider, #F0F0F0);
	}

	.modal-title {
		font-size: 32rpx;
		font-weight: bold;
		color: var(--text-primary, #1A1A1A);
	}

	.modal-close {
		font-size: 40rpx;
		color: var(--text-tertiary, #999999);
		width: 48rpx;
		height: 48rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
	}

	/* 主题网格 */
	.theme-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 24rpx;
		padding: 32rpx;
	}

	.theme-item {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		cursor: pointer;
		transition: all 0.3s ease;
	}

	.theme-item.active {
		transform: scale(1.05);
	}

	/* 主题预览 */
	.theme-preview {
		width: 120rpx;
		height: 120rpx;
		border-radius: 20rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 16rpx;
		box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.1);
		transition: all 0.3s ease;
	}

	.theme-item:active .theme-preview {
		transform: scale(0.95);
	}

	.theme-item-icon {
		font-size: 56rpx;
	}

	.theme-name {
		font-size: 24rpx;
		color: var(--text-secondary, #666666);
	}

	/* 选中标记 */
	.theme-check {
		position: absolute;
		top: -8rpx;
		right: 10rpx;
		width: 40rpx;
		height: 40rpx;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 4rpx 12rpx rgba(102, 126, 234, 0.4);
		animation: scaleIn 0.3s ease;
	}

	@keyframes scaleIn {
		from {
			transform: scale(0);
		}

		to {
			transform: scale(1);
		}
	}

	.check-icon {
		color: #FFFFFF;
		font-size: 24rpx;
		font-weight: bold;
	}

	/* 提示文字 */
	.theme-tip {
		padding: 24rpx 32rpx 32rpx;
		border-top: 1rpx solid var(--divider, #F0F0F0);
	}

	.tip-text {
		font-size: 24rpx;
		color: var(--text-tertiary, #999999);
		line-height: 1.5;
	}
</style>
