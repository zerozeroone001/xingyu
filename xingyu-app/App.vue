<script>
	import {
		initTheme,
		getCurrentTheme
	} from './stores/theme.js'

	export default {
		onLaunch: function() {
			console.log('App Launch')

			// 初始化主题系统
			initTheme()

			// 监听主题变化事件
			uni.$on('themeChange', (theme) => {
				console.log('主题已切换:', theme.name)
				// 这里可以添加主题切换的额外逻辑
			})
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/**
	 * 全局样式
	 * 定义CSS变量,便于主题系统使用
	 */

	/* 页面基础样式 */
	page {
		background-color: var(--bg-primary, #FFFFFF);
		color: var(--text-primary, #1A1A1A);
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
		font-size: 28rpx;
		line-height: 1.6;

		/* 添加主题过渡动画 */
		transition: background-color 0.3s ease, color 0.3s ease;
	}

	/* 重置默认样式 */
	view,
	text,
	image,
	button {
		box-sizing: border-box;
	}

	/* 全局容器 */
	.container {
		background-color: var(--bg-primary, #FFFFFF);
		min-height: 100vh;
	}

	/* 卡片样式 */
	.card {
		background-color: var(--bg-card, #FFFFFF);
		border-radius: 16rpx;
		box-shadow: 0 4rpx 12rpx var(--shadow, rgba(0, 0, 0, 0.08));
		transition: all 0.3s ease;
	}

	.card:active {
		transform: scale(0.98);
	}

	/* 按钮样式 */
	.btn-primary {
		background-color: var(--primary, #2979FF);
		color: var(--text-inverse, #FFFFFF);
		border: none;
		border-radius: 8rpx;
		padding: 20rpx 40rpx;
		font-size: 28rpx;
		transition: all 0.3s ease;
	}

	.btn-primary:active {
		background-color: var(--primary-dark, #2962FF);
		transform: scale(0.95);
	}

	/* 文字颜色类 */
	.text-primary {
		color: var(--text-primary, #1A1A1A);
	}

	.text-secondary {
		color: var(--text-secondary, #666666);
	}

	.text-tertiary {
		color: var(--text-tertiary, #999999);
	}

	/* 分割线 */
	.divider {
		height: 1rpx;
		background-color: var(--divider, #F0F0F0);
	}

	/* 加载动画 */
	@keyframes rotate {
		from {
			transform: rotate(0deg);
		}

		to {
			transform: rotate(360deg);
		}
	}

	.loading {
		animation: rotate 1s linear infinite;
	}

	/* 淡入动画 */
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(20rpx);
		}

		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.fade-in {
		animation: fadeIn 0.3s ease;
	}
</style>
