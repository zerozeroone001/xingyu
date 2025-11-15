<template>
	<view class="date-weather">
		<view class="date-info">
			<text class="date">{{ currentDate }}</text>
			<text class="weekday">{{ currentWeekday }}</text>
		</view>
		<view class="weather-info">
			<text class="weather-icon">{{ weatherIcon }}</text>
			<text class="temperature">{{ temperature }}°C</text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				currentDate: '',
				currentWeekday: '',
				weatherIcon: '☀️',
				temperature: 22,
				timer: null
			}
		},
		onLoad() {
			this.updateDateTime()
			// 每分钟更新一次时间
			this.timer = setInterval(() => {
				this.updateDateTime()
			}, 60000)

			// 获取天气信息
			this.getWeatherInfo()
		},
		onUnload() {
			if (this.timer) {
				clearInterval(this.timer)
			}
		},
		methods: {
			/**
			 * 更新日期时间
			 */
			updateDateTime() {
				const now = new Date()

				// 格式化日期: 11月15日
				const month = now.getMonth() + 1
				const day = now.getDate()
				this.currentDate = `${month}月${day}日`

				// 格式化星期
				const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
				this.currentWeekday = weekdays[now.getDay()]
			},

			/**
			 * 获取天气信息
			 * 这里使用模拟数据，实际项目中可以调用天气API
			 */
			getWeatherInfo() {
				// 模拟天气数据
				const weatherTypes = [
					{ icon: '☀️', temp: 22, name: '晴' },
					{ icon: '⛅', temp: 20, name: '多云' },
					{ icon: '☁️', temp: 18, name: '阴' },
					{ icon: '🌧️', temp: 15, name: '雨' }
				]

				// 根据当前小时选择天气（简单模拟）
				const hour = new Date().getHours()
				let weatherIndex = 0
				if (hour >= 6 && hour < 12) {
					weatherIndex = 0 // 早晨晴天
				} else if (hour >= 12 && hour < 18) {
					weatherIndex = 1 // 下午多云
				} else if (hour >= 18 && hour < 22) {
					weatherIndex = 0 // 傍晚晴天
				} else {
					weatherIndex = 2 // 夜晚阴天
				}

				const weather = weatherTypes[weatherIndex]
				this.weatherIcon = weather.icon
				this.temperature = weather.temp

				// TODO: 实际项目中可以调用天气API
				// 例如：uni.request({ url: 'weather-api-url', ... })
			}
		}
	}
</script>

<style scoped>
	.date-weather {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 24rpx;
	}

	.date-info {
		display: flex;
		flex-direction: column;
		gap: 4rpx;
	}

	.date {
		font-size: 28rpx;
		font-weight: 600;
		color: var(--text-primary, #1A1A1A);
	}

	.weekday {
		font-size: 22rpx;
		color: var(--text-secondary, #666666);
	}

	.weather-info {
		display: flex;
		align-items: center;
		gap: 8rpx;
		padding: 8rpx 16rpx;
		background-color: var(--bg-secondary, #F7F8FA);
		border-radius: 20rpx;
	}

	.weather-icon {
		font-size: 28rpx;
	}

	.temperature {
		font-size: 24rpx;
		font-weight: 500;
		color: var(--text-primary, #1A1A1A);
	}
</style>
