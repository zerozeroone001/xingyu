const request = require('./request')
const config = require('../utils/config')
const { mockUser } = require('./mock')
const { getStorage, setStorage, removeStorage } = require('../utils/cache')

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

function normalizeProfile(profile = {}) {
  const nickname = profile.nickname || profile.nickName || '诗词访客'
  const avatarUrl = profile.avatar_url || profile.avatarUrl || ''
  const avatarText = profile.avatarText || nickname.slice(0, 2)

  return Object.assign({}, profile, {
    nickname,
    nickName: nickname,
    avatar_url: avatarUrl,
    avatarUrl,
    avatarText
  })
}

function saveLoginData(data = {}) {
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
  return Object.assign({}, data, { token, user })
}

function clearLoginData() {
  removeStorage('token')
  removeStorage('userInfo')
  syncGlobalAuth('', null)
}

function getWxUserProfile() {
  if (config.useMock) {
    return Promise.resolve(normalizeProfile(mockUser))
  }

  if (wx.getUserProfile) {
    return new Promise((resolve, reject) => {
      wx.getUserProfile({
        desc: '用于完善个人资料',
        lang: 'zh_CN',
        success(res) {
          resolve(normalizeProfile(res.userInfo || {}))
        },
        fail: reject
      })
    })
  }

  return new Promise((resolve, reject) => {
    wx.getUserInfo({
      lang: 'zh_CN',
      success(res) {
        resolve(normalizeProfile(res.userInfo || {}))
      },
      fail: reject
    })
  })
}

function requestWxCode() {
  return new Promise((resolve, reject) => {
    wx.login({
      success(loginRes) {
        if (!loginRes.code) {
          reject(new Error('微信登录凭证为空'))
          return
        }

        resolve(loginRes.code)
      },
      fail: reject
    })
  })
}

function wxLogin(profile = {}) {
  const normalizedProfile = normalizeProfile(profile)

  if (config.useMock) {
    return Promise.resolve(
      saveLoginData({
        token: 'mock-token',
        user: Object.assign({}, mockUser, normalizedProfile)
      })
    )
  }

  return requestWxCode()
    .then((code) => {
      return request({
        url: '/auth/wx-login',
        method: 'POST',
        data: {
          code,
          profile: normalizedProfile
        }
      })
    })
    .then(saveLoginData)
}

function logout() {
  const token = getStorage('token', '')
  const clearAndResolve = () => {
    clearLoginData()
    return { logged_out: true }
  }

  if (config.useMock || !token) {
    return Promise.resolve(clearAndResolve())
  }

  return request({
    url: '/auth/logout',
    method: 'POST',
    skipAuthRefresh: true,
    suppressErrorToast: true
  })
    .catch(() => null)
    .then(clearAndResolve)
}

function mockGuestLogin() {
  if (!config.useMock) {
    return request({
      url: '/auth/wx-login',
      method: 'POST',
      data: {
        code: 'guest',
        profile: normalizeProfile({
          nickname: '诗词访客',
          avatarText: '诗'
        })
      }
    }).then(saveLoginData)
  }

  return Promise.resolve(
    saveLoginData({
      token: 'mock-token',
      user: Object.assign({}, mockUser, normalizeProfile(mockUser))
    })
  )
}

module.exports = {
  wxLogin,
  logout,
  mockGuestLogin,
  getWxUserProfile,
  saveLoginData,
  clearLoginData
}
