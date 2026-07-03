const request = require('./request')
const config = require('../utils/config')
const { mockUser } = require('./mock')
const { setStorage, removeStorage } = require('../utils/cache')

/**
 * 调用微信登录并把 code 发送给后端换取业务 token。
 * 后端未接入前，调用方可以先使用游客模式进入首页。
 */
function wxLogin(profile = {}) {
  if (config.useMock) {
    const data = {
      token: 'mock-token',
      user: Object.assign({}, mockUser, profile)
    }
    setStorage('token', data.token)
    setStorage('userInfo', data.user)
    return Promise.resolve(data)
  }

  return new Promise((resolve, reject) => {
    wx.login({
      success(loginRes) {
        request({
          url: '/auth/wx-login',
          method: 'POST',
          data: {
            code: loginRes.code,
            profile
          }
        })
          .then((data) => {
            setStorage('token', data.token || '')
            setStorage('userInfo', data.user || null)
            resolve(data)
          })
          .catch(reject)
      },
      fail: reject
    })
  })
}

function logout() {
  removeStorage('token')
  removeStorage('userInfo')
}

/**
 * 写入游客登录态。
 * mock 开发阶段默认跳过真实微信登录，依然保留一个本地用户对象供个人中心等页面读取。
 */
function mockGuestLogin() {
  setStorage('token', 'mock-token')
  setStorage('userInfo', mockUser)
  return Promise.resolve({
    token: 'mock-token',
    user: mockUser
  })
}

module.exports = {
  wxLogin,
  logout,
  mockGuestLogin
}
