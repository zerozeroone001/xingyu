const { wxLogin, mockGuestLogin, getWxUserProfile } = require('../../services/auth')
const { switchTab } = require('../../utils/route')
const { showLoading, hideLoading, showToast } = require('../../utils/toast')

function isAuthCancel(error) {
  const message = error && error.errMsg ? error.errMsg : ''
  return message.indexOf('auth deny') >= 0 || message.indexOf('cancel') >= 0
}

Page({
  data: {
    loading: false
  },

  handleWxLogin() {
    if (this.data.loading) {
      return
    }

    this.setData({ loading: true })
    showLoading('登录中')

    getWxUserProfile()
      .then((profile) => wxLogin(profile))
      .then(() => {
        showToast('登录成功', 'success')
        switchTab('/pages/home/home')
      })
      .catch((error) => {
        if (isAuthCancel(error)) {
          showToast('已取消授权')
          return
        }

        showToast('登录失败，请稍后重试')
      })
      .finally(() => {
        hideLoading()
        this.setData({ loading: false })
      })
  },

  handleGuestEnter() {
    if (this.data.loading) {
      return
    }

    this.setData({ loading: true })
    showLoading('进入中')

    mockGuestLogin()
      .then(() => {
        switchTab('/pages/home/home')
      })
      .catch(() => {
        showToast('游客登录失败，请稍后重试')
      })
      .finally(() => {
        hideLoading()
        this.setData({ loading: false })
      })
  }
})
