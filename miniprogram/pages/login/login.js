const { wxLogin, mockGuestLogin } = require('../../services/auth')
const { switchTab } = require('../../utils/route')
const { showLoading, hideLoading, showToast } = require('../../utils/toast')

Page({
  data: {
    phone: '',
    code: ''
  },

  handlePhoneInput(event) {
    this.setData({
      phone: event.detail.value
    })
  },

  handleCodeInput(event) {
    this.setData({
      code: event.detail.value
    })
  },

  getCode() {
    showToast('验证码已发送')
  },

  /**
   * 微信登录入口。
   * mock 模式下 service 会直接写入本地用户，真实环境再调用后端换 token。
   */
  handleWxLogin() {
    showLoading('登录中')
    wxLogin()
      .then(() => {
        showToast('登录成功', 'success')
        switchTab('/pages/home/home')
      })
      .catch(() => {
        showToast('登录接口暂不可用')
      })
      .finally(() => {
        hideLoading()
      })
  },

  /**
   * 当前阶段跳过真实登录，写入 mock 游客身份后进入首页。
   */
  handleGuestEnter() {
    mockGuestLogin().then(() => {
      switchTab('/pages/home/home')
    })
  }
})
