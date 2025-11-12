/**
 * HTTP 请求封装
 * 基于 uni.request 封装，支持拦截器、loading、错误处理
 */

const BASE_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8000/api/v1'
  : 'https://api.xingyu-poetry.com/api/v1'

/**
 * 请求配置
 */
const config = {
  baseURL: BASE_URL,
  timeout: 60000,
  header: {
    'Content-Type': 'application/json'
  }
}

/**
 * 请求拦截器
 * @param {Object} options - 请求配置
 * @returns {Object} 处理后的请求配置
 */
const requestInterceptor = (options) => {
  // 添加 token
  const token = uni.getStorageSync('token')
  if (token) {
    options.header = options.header || {}
    options.header['Authorization'] = `Bearer ${token}`
  }

  // 显示 loading
  if (options.loading !== false) {
    uni.showLoading({
      title: options.loadingText || '加载中...',
      mask: true
    })
  }

  return options
}

/**
 * 响应拦截器
 * @param {Object} response - 响应数据
 * @returns {Promise} 处理后的响应
 */
const responseInterceptor = (response) => {
  // 隐藏 loading
  uni.hideLoading()

  const { statusCode, data } = response

  // HTTP 状态码检查
  if (statusCode !== 200) {
    return handleHttpError(statusCode, data)
  }

  // 业务状态码检查
  if (data.code === 0) {
    return Promise.resolve(data.data)
  } else {
    return handleBusinessError(data)
  }
}

/**
 * 错误拦截器
 * @param {Error} error - 错误对象
 * @returns {Promise} 拒绝的 Promise
 */
const errorInterceptor = (error) => {
  uni.hideLoading()

  uni.showToast({
    title: '网络请求失败',
    icon: 'none',
    duration: 2000
  })

  console.error('请求错误:', error)
  return Promise.reject(error)
}

/**
 * 处理 HTTP 错误
 * @param {number} statusCode - HTTP 状态码
 * @param {Object} data - 响应数据
 * @returns {Promise} 拒绝的 Promise
 */
const handleHttpError = (statusCode, data) => {
  let message = '请求失败'

  switch (statusCode) {
    case 400:
      message = '请求参数错误'
      break
    case 401:
      message = '未登录或登录已过期'
      // 清除 token 并跳转到登录页
      uni.removeStorageSync('token')
      uni.removeStorageSync('user')
      uni.navigateTo({ url: '/pages/login/index' })
      break
    case 403:
      message = '没有权限访问'
      break
    case 404:
      message = '请求的资源不存在'
      break
    case 500:
      message = '服务器错误'
      break
    case 502:
      message = '网关错误'
      break
    case 503:
      message = '服务不可用'
      break
    default:
      message = `请求失败(${statusCode})`
  }

  uni.showToast({
    title: message,
    icon: 'none',
    duration: 2000
  })

  return Promise.reject({ statusCode, message, data })
}

/**
 * 处理业务错误
 * @param {Object} data - 响应数据
 * @returns {Promise} 拒绝的 Promise
 */
const handleBusinessError = (data) => {
  const message = data.message || '操作失败'

  uni.showToast({
    title: message,
    icon: 'none',
    duration: 2000
  })

  return Promise.reject(data)
}

/**
 * 发起请求
 * @param {Object} options - 请求配置
 * @returns {Promise} 请求结果
 */
const request = (options) => {
  // 合并配置
  options = {
    ...config,
    ...options,
    url: options.baseURL || config.baseURL + options.url,
    header: {
      ...config.header,
      ...options.header
    }
  }

  // 请求拦截
  options = requestInterceptor(options)

  // 发起请求
  return new Promise((resolve, reject) => {
    uni.request({
      ...options,
      success: (response) => {
        responseInterceptor(response)
          .then(resolve)
          .catch(reject)
      },
      fail: (error) => {
        errorInterceptor(error)
          .catch(reject)
      }
    })
  })
}

/**
 * GET 请求
 * @param {string} url - 请求地址
 * @param {Object} params - 请求参数
 * @param {Object} options - 其他配置
 * @returns {Promise} 请求结果
 */
export const get = (url, params = {}, options = {}) => {
  return request({
    url,
    method: 'GET',
    data: params,
    ...options
  })
}

/**
 * POST 请求
 * @param {string} url - 请求地址
 * @param {Object} data - 请求数据
 * @param {Object} options - 其他配置
 * @returns {Promise} 请求结果
 */
export const post = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'POST',
    data,
    ...options
  })
}

/**
 * PUT 请求
 * @param {string} url - 请求地址
 * @param {Object} data - 请求数据
 * @param {Object} options - 其他配置
 * @returns {Promise} 请求结果
 */
export const put = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'PUT',
    data,
    ...options
  })
}

/**
 * DELETE 请求
 * @param {string} url - 请求地址
 * @param {Object} data - 请求数据
 * @param {Object} options - 其他配置
 * @returns {Promise} 请求结果
 */
export const del = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'DELETE',
    data,
    ...options
  })
}

/**
 * 上传文件
 * @param {string} url - 上传地址
 * @param {string} filePath - 文件路径
 * @param {Object} formData - 额外数据
 * @param {Object} options - 其他配置
 * @returns {Promise} 上传结果
 */
export const upload = (url, filePath, formData = {}, options = {}) => {
  const token = uni.getStorageSync('token')

  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: config.baseURL + url,
      filePath,
      name: 'file',
      formData,
      header: {
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: (res) => {
        const data = JSON.parse(res.data)
        if (data.code === 0) {
          resolve(data.data)
        } else {
          handleBusinessError(data).catch(reject)
        }
      },
      fail: (error) => {
        errorInterceptor(error).catch(reject)
      }
    })
  })
}

export default {
  get,
  post,
  put,
  del,
  upload
}
