const config = require('../utils/config')
const { getStorage, removeStorage } = require('../utils/cache')
const { showToast } = require('../utils/toast')

/**
 * 小程序统一请求方法。
 * 所有业务接口都需要经过这里，便于统一处理 token、错误提示和响应格式。
 */
function request(options) {
  const token = getStorage('token', '')
  const header = Object.assign(
    {
      'content-type': 'application/json'
    },
    options.header || {}
  )

  if (token) {
    header.Authorization = `Bearer ${token}`
  }

  return new Promise((resolve, reject) => {
    wx.request({
      url: `${config.apiBaseUrl}${options.url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header,
      timeout: config.requestTimeout,
      success(res) {
        const response = res.data || {}

        // HTTP 401 表示登录态失效，清理本地 token 后提示用户重新登录。
        if (res.statusCode === 401) {
          removeStorage('token')
          showToast('登录已失效，请重新登录')
          reject(response)
          return
        }

        if (res.statusCode < 200 || res.statusCode >= 300) {
          showToast(response.message || '请求失败')
          reject(response)
          return
        }

        // 后端约定 code 为 0 表示成功；如果后端暂未接入，也兼容直接返回数据。
        if (response.code !== undefined && response.code !== 0) {
          showToast(response.message || '操作失败')
          reject(response)
          return
        }

        resolve(response.data !== undefined ? response.data : response)
      },
      fail(error) {
        showToast('网络异常，请稍后重试')
        reject(error)
      }
    })
  })
}

module.exports = request
