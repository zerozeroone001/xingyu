const config = require('../utils/config')
const { getStorage, setStorage, removeStorage } = require('../utils/cache')
const { showToast } = require('../utils/toast')

let guestLoginTask = null

function getAppInstance() {
  return typeof getApp === 'function' ? getApp() : null
}

function syncGlobalAuth(token = '', user = null) {
  const app = getAppInstance()

  if (!app || !app.globalData) {
    return
  }

  app.globalData.token = token
  app.globalData.userInfo = user
}

function saveAuthData(data = {}) {
  const token = data.token || ''
  const user = data.user || null

  if (token) {
    setStorage('token', token)
  } else {
    removeStorage('token')
  }

  if (user) {
    setStorage('userInfo', user)
  } else {
    removeStorage('userInfo')
  }

  syncGlobalAuth(token, user)
  return data
}

function clearAuthData() {
  removeStorage('token')
  removeStorage('userInfo')
  syncGlobalAuth('', null)
}

function requestGuestToken() {
  if (guestLoginTask) {
    return guestLoginTask
  }

  guestLoginTask = new Promise((resolve, reject) => {
    wx.request({
      url: `${config.apiBaseUrl}/auth/wx-login`,
      method: 'POST',
      data: {
        code: 'guest',
        profile: {
          nickname: '诗词访客',
          avatarText: '诗'
        }
      },
      header: {
        'content-type': 'application/json'
      },
      timeout: config.requestTimeout,
      success(res) {
        const response = res.data || {}

        if (res.statusCode < 200 || res.statusCode >= 300 || (response.code !== undefined && response.code !== 0)) {
          reject(response)
          return
        }

        const data = response.data || response
        saveAuthData(data)
        resolve(data)
      },
      fail: reject
    })
  }).finally(() => {
    guestLoginTask = null
  })

  return guestLoginTask
}

function showRequestToast(options, title, icon = 'none') {
  if (!options.suppressErrorToast) {
    showToast(title, icon)
  }
}

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

        if (res.statusCode === 401) {
          clearAuthData()

          if (config.autoGuestLogin && !options.skipAuthRefresh) {
            requestGuestToken()
              .then(() => request(Object.assign({}, options, { skipAuthRefresh: true })))
              .then(resolve)
              .catch((error) => {
                showRequestToast(options, '登录已失效，请重新登录')
                reject(error)
              })
            return
          }

          showRequestToast(options, '登录已失效，请重新登录')
          reject(response)
          return
        }

        if (res.statusCode < 200 || res.statusCode >= 300) {
          showRequestToast(options, response.message || '请求失败')
          reject(response)
          return
        }

        if (response.code !== undefined && response.code !== 0) {
          showRequestToast(options, response.message || '操作失败')
          reject(response)
          return
        }

        resolve(response.data !== undefined ? response.data : response)
      },
      fail(error) {
        showRequestToast(options, '网络异常，请稍后重试')
        reject(error)
      }
    })
  })
}

module.exports = request
