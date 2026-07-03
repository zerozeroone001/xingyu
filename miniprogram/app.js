const { getStorage } = require('./utils/cache')
const config = require('./utils/config')
const { mockGuestLogin } = require('./services/auth')

App({
  globalData: {
    // 后端 API 基础地址。开发阶段默认指向本机 FastAPI 服务，真机调试时需要改成局域网或 HTTPS 域名。
    apiBaseUrl: 'http://127.0.0.1:8000/api/v1',
    userInfo: null,
    token: ''
  },

  onLaunch() {
    // 小程序启动时从本地缓存恢复登录态，避免每次打开都重新登录。
    this.globalData.token = getStorage('token', '')
    this.globalData.userInfo = getStorage('userInfo', null)

    // mock 模式默认跳过微信登录，直接写入游客身份，便于前端页面独立开发。
    if (config.useMock && !this.globalData.token) {
      mockGuestLogin().then((data) => {
        this.globalData.token = data.token
        this.globalData.userInfo = data.user
      })
    }
  }
})
