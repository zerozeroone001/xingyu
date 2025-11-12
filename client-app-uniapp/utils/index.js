/**
 * 工具函数集合
 * 提供常用的工具方法
 */

/**
 * 格式化日期时间
 * @param {Date|string|number} date - 日期对象、字符串或时间戳
 * @param {string} format - 格式化模板，默认 'YYYY-MM-DD HH:mm:ss'
 * @returns {string} 格式化后的日期字符串
 */
export const formatDate = (date, format = 'YYYY-MM-DD HH:mm:ss') => {
  if (!date) return ''

  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hour = String(d.getHours()).padStart(2, '0')
  const minute = String(d.getMinutes()).padStart(2, '0')
  const second = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hour)
    .replace('mm', minute)
    .replace('ss', second)
}

/**
 * 格式化相对时间（如：刚刚、3分钟前）
 * @param {Date|string|number} date - 日期
 * @returns {string} 相对时间字符串
 */
export const formatRelativeTime = (date) => {
  if (!date) return ''

  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const now = new Date()
  const diff = now - d
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (seconds < 60) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  if (days < 365) return `${Math.floor(days / 30)}个月前`
  return `${Math.floor(days / 365)}年前`
}

/**
 * 格式化数字（如：10000 -> 1万）
 * @param {number} num - 数字
 * @returns {string} 格式化后的字符串
 */
export const formatNumber = (num) => {
  if (num === undefined || num === null) return '0'

  num = Number(num)
  if (isNaN(num)) return '0'

  if (num < 10000) return String(num)
  if (num < 100000000) return (num / 10000).toFixed(1) + '万'
  return (num / 100000000).toFixed(1) + '亿'
}

/**
 * 防抖函数
 * @param {Function} fn - 要执行的函数
 * @param {number} delay - 延迟时间（毫秒）
 * @returns {Function} 防抖后的函数
 */
export const debounce = (fn, delay = 300) => {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

/**
 * 节流函数
 * @param {Function} fn - 要执行的函数
 * @param {number} delay - 间隔时间（毫秒）
 * @returns {Function} 节流后的函数
 */
export const throttle = (fn, delay = 300) => {
  let last = 0
  return function (...args) {
    const now = Date.now()
    if (now - last >= delay) {
      last = now
      fn.apply(this, args)
    }
  }
}

/**
 * 深拷贝
 * @param {*} obj - 要拷贝的对象
 * @returns {*} 拷贝后的对象
 */
export const deepClone = (obj) => {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj)
  if (obj instanceof Array) return obj.map(item => deepClone(item))

  const clonedObj = {}
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      clonedObj[key] = deepClone(obj[key])
    }
  }
  return clonedObj
}

/**
 * 随机字符串
 * @param {number} length - 长度
 * @returns {string} 随机字符串
 */
export const randomString = (length = 16) => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * 存储数据到本地
 * @param {string} key - 键名
 * @param {*} value - 值
 */
export const setStorage = (key, value) => {
  try {
    uni.setStorageSync(key, JSON.stringify(value))
  } catch (e) {
    console.error('存储数据失败:', e)
  }
}

/**
 * 从本地读取数据
 * @param {string} key - 键名
 * @returns {*} 读取的值
 */
export const getStorage = (key) => {
  try {
    const value = uni.getStorageSync(key)
    return value ? JSON.parse(value) : null
  } catch (e) {
    console.error('读取数据失败:', e)
    return null
  }
}

/**
 * 删除本地数据
 * @param {string} key - 键名
 */
export const removeStorage = (key) => {
  try {
    uni.removeStorageSync(key)
  } catch (e) {
    console.error('删除数据失败:', e)
  }
}

/**
 * 清空本地数据
 */
export const clearStorage = () => {
  try {
    uni.clearStorageSync()
  } catch (e) {
    console.error('清空数据失败:', e)
  }
}

/**
 * 复制文本到剪贴板
 * @param {string} text - 要复制的文本
 * @returns {Promise} 复制结果
 */
export const copyText = (text) => {
  return new Promise((resolve, reject) => {
    uni.setClipboardData({
      data: text,
      success: () => {
        uni.showToast({
          title: '复制成功',
          icon: 'success'
        })
        resolve()
      },
      fail: (error) => {
        uni.showToast({
          title: '复制失败',
          icon: 'none'
        })
        reject(error)
      }
    })
  })
}

/**
 * 显示提示信息
 * @param {string} title - 提示标题
 * @param {string} icon - 图标类型
 * @param {number} duration - 持续时间
 */
export const showToast = (title, icon = 'none', duration = 2000) => {
  uni.showToast({
    title,
    icon,
    duration
  })
}

/**
 * 显示确认对话框
 * @param {string} content - 内容
 * @param {string} title - 标题
 * @returns {Promise<boolean>} 用户选择结果
 */
export const showConfirm = (content, title = '提示') => {
  return new Promise((resolve) => {
    uni.showModal({
      title,
      content,
      success: (res) => {
        resolve(res.confirm)
      }
    })
  })
}

/**
 * 页面跳转
 * @param {string} url - 页面路径
 * @param {Object} params - 参数对象
 */
export const navigateTo = (url, params = {}) => {
  const query = Object.keys(params)
    .map(key => `${key}=${encodeURIComponent(params[key])}`)
    .join('&')

  uni.navigateTo({
    url: query ? `${url}?${query}` : url
  })
}

/**
 * 获取 URL 参数
 * @returns {Object} 参数对象
 */
export const getUrlParams = () => {
  // #ifdef H5
  const search = window.location.search.substring(1)
  if (!search) return {}

  const params = {}
  search.split('&').forEach(item => {
    const [key, value] = item.split('=')
    params[key] = decodeURIComponent(value)
  })
  return params
  // #endif

  // #ifndef H5
  // 小程序环境需要在页面 onLoad 中获取
  return {}
  // #endif
}

/**
 * 验证手机号
 * @param {string} phone - 手机号
 * @returns {boolean} 是否有效
 */
export const validatePhone = (phone) => {
  return /^1[3-9]\d{9}$/.test(phone)
}

/**
 * 验证邮箱
 * @param {string} email - 邮箱
 * @returns {boolean} 是否有效
 */
export const validateEmail = (email) => {
  return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)
}

/**
 * 图片预览
 * @param {Array} urls - 图片地址数组
 * @param {number} current - 当前图片索引
 */
export const previewImage = (urls, current = 0) => {
  uni.previewImage({
    urls,
    current: typeof current === 'number' ? urls[current] : current
  })
}

/**
 * 选择图片
 * @param {Object} options - 配置项
 * @returns {Promise} 选择的图片
 */
export const chooseImage = (options = {}) => {
  return new Promise((resolve, reject) => {
    uni.chooseImage({
      count: options.count || 1,
      sizeType: options.sizeType || ['compressed'],
      sourceType: options.sourceType || ['album', 'camera'],
      success: (res) => {
        resolve(res.tempFilePaths)
      },
      fail: reject
    })
  })
}

/**
 * 分享
 * @param {Object} options - 分享配置
 */
export const share = (options = {}) => {
  // #ifdef MP-WEIXIN
  // 小程序分享需要在页面的 onShareAppMessage 中配置
  return {
    title: options.title || '星语诗词',
    path: options.path || '/pages/index/index',
    imageUrl: options.imageUrl || ''
  }
  // #endif

  // #ifdef H5
  // H5 分享可以使用 Web Share API 或第三方分享
  if (navigator.share) {
    navigator.share({
      title: options.title,
      text: options.text,
      url: options.url || window.location.href
    })
  }
  // #endif
}
