/**
 * HTTP请求封装
 * 统一处理请求、响应、错误
 */

// API基础配置
const BASE_URL = 'http://localhost:8000/api/v1'
const TIMEOUT = 30000 // 请求超时时间(毫秒)

/**
 * HTTP请求封装
 * @param {Object} options 请求配置
 * @returns {Promise}
 */
function request(options) {
	return new Promise((resolve, reject) => {
		// 从本地存储获取token
		const token = uni.getStorageSync('token')

		// 合并请求配置
		const config = {
			url: BASE_URL + options.url,
			method: options.method || 'GET',
			data: options.data || {},
			timeout: options.timeout || TIMEOUT,
			header: {
				'Content-Type': 'application/json',
				...options.header
			}
		}

		// 如果有token,添加到请求头
		if (token) {
			config.header['Authorization'] = 'Bearer ' + token
		}

		console.log('📡 发起请求:', config.method, config.url)

		// 发起请求
		uni.request({
			...config,
			success: (res) => {
				console.log('✅ 请求成功:', res.data)

				// 处理响应
				handleResponse(res, resolve, reject)
			},
			fail: (err) => {
				console.error('❌ 请求失败:', err)

				// 处理错误
				handleError(err, reject)
			}
		})
	})
}

/**
 * 处理响应
 * @param {Object} res 响应对象
 * @param {Function} resolve Promise resolve
 * @param {Function} reject Promise reject
 */
function handleResponse(res, resolve, reject) {
	const {
		statusCode,
		data
	} = res

	// HTTP状态码检查
	if (statusCode >= 200 && statusCode < 300) {
		// 业务状态码检查
		if (data.code === 200) {
			// 成功
			resolve(data.data)
		} else {
			// 业务错误
			const error = {
				code: data.code,
				message: data.message || '请求失败'
			}
			showError(error.message)
			reject(error)
		}
	} else if (statusCode === 401) {
		// 未授权,跳转登录
		handleUnauthorized()
		reject({
			code: 401,
			message: '请先登录'
		})
	} else if (statusCode === 403) {
		// 无权限
		showError('无权限访问')
		reject({
			code: 403,
			message: '无权限访问'
		})
	} else if (statusCode === 404) {
		// 资源不存在
		showError('请求的资源不存在')
		reject({
			code: 404,
			message: '请求的资源不存在'
		})
	} else if (statusCode >= 500) {
		// 服务器错误
		showError('服务器错误,请稍后重试')
		reject({
			code: statusCode,
			message: '服务器错误'
		})
	} else {
		// 其他错误
		showError(data.message || '请求失败')
		reject({
			code: statusCode,
			message: data.message || '请求失败'
		})
	}
}

/**
 * 处理请求错误
 * @param {Object} err 错误对象
 * @param {Function} reject Promise reject
 */
function handleError(err, reject) {
	let message = '网络连接失败'

	if (err.errMsg) {
		if (err.errMsg.includes('timeout')) {
			message = '请求超时,请检查网络'
		} else if (err.errMsg.includes('fail')) {
			message = '网络连接失败,请检查网络'
		}
	}

	showError(message)
	reject({
		code: -1,
		message
	})
}

/**
 * 处理未授权(401)
 */
function handleUnauthorized() {
	// 清除token
	uni.removeStorageSync('token')

	// 提示
	uni.showToast({
		title: '请先登录',
		icon: 'none',
		duration: 2000
	})

	// 延迟跳转到登录页
	setTimeout(() => {
		uni.reLaunch({
			url: '/pages/auth/login'
		})
	}, 2000)
}

/**
 * 显示错误提示
 * @param {String} message 错误信息
 */
function showError(message) {
	uni.showToast({
		title: message,
		icon: 'none',
		duration: 2000
	})
}

/**
 * GET请求
 * @param {String} url 请求URL
 * @param {Object} data 请求参数
 * @param {Object} options 其他配置
 * @returns {Promise}
 */
export function get(url, data = {}, options = {}) {
	return request({
		url,
		method: 'GET',
		data,
		...options
	})
}

/**
 * POST请求
 * @param {String} url 请求URL
 * @param {Object} data 请求数据
 * @param {Object} options 其他配置
 * @returns {Promise}
 */
export function post(url, data = {}, options = {}) {
	return request({
		url,
		method: 'POST',
		data,
		...options
	})
}

/**
 * PUT请求
 * @param {String} url 请求URL
 * @param {Object} data 请求数据
 * @param {Object} options 其他配置
 * @returns {Promise}
 */
export function put(url, data = {}, options = {}) {
	return request({
		url,
		method: 'PUT',
		data,
		...options
	})
}

/**
 * DELETE请求
 * @param {String} url 请求URL
 * @param {Object} data 请求参数
 * @param {Object} options 其他配置
 * @returns {Promise}
 */
export function del(url, data = {}, options = {}) {
	return request({
		url,
		method: 'DELETE',
		data,
		...options
	})
}

// 默认导出
export default {
	get,
	post,
	put,
	del
}
