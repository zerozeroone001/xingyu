const { logout } = require('../../services/auth')
const { getProfileOverview } = require('../../services/user')
const { clearProjectStorage } = require('../../utils/cache')
const { navigateTo } = require('../../utils/route')
const { showLoading, hideLoading, showToast } = require('../../utils/toast')

Page({
  data: {
    loading: false,
    loggingOut: false,
    user: {
      nickname: '诗词访客',
      avatarText: '诗',
      title: '新晋诗友',
      level: 1
    },
    stats: [
      { label: '诗作', value: 0, type: 'poems' },
      { label: '获赞', value: 0, type: 'likes' },
      { label: '收藏', value: 0, type: 'favorites' },
      { label: '关注', value: 0, type: 'follows' }
    ],
    menus: [
      { title: '个人信息', subtitle: '查看与编辑个人资料', type: 'info', action: 'profileInfo' },
      { title: '飞花令对局', subtitle: '参加的飞花令对局', type: 'game', action: 'feihualing' },
      { title: '意见反馈', subtitle: '提交建议与问题', type: 'feedback', action: 'feedback' },
      { title: '退出登录', subtitle: '安全退出当前账号', type: 'logout', action: 'logout' }
    ]
  },

  onLoad() {
    this.loadOverview()
  },

  onShow() {
    if (!this.data.loggingOut) {
      this.loadOverview()
    }
  },

  loadOverview() {
    if (this.data.loggingOut) {
      return Promise.resolve()
    }

    this.setData({ loading: true })

    return getProfileOverview()
      .then((data) => {
        const user = data.user || {}
        const stats = data.stats || {}
        const nickname = user.nickname || '诗词访客'

        this.setData({
          user: {
            nickname,
            avatarText: user.avatarText || user.avatar_text || nickname.slice(0, 1),
            title: user.title || '新晋诗友',
            level: user.level || 1
          },
          stats: [
            { label: '诗作', value: this.formatCount(stats.poems), type: 'poems' },
            { label: '获赞', value: this.formatCount(stats.likes), type: 'likes' },
            { label: '收藏', value: this.formatCount(stats.favorites), type: 'favorites' },
            { label: '关注', value: this.formatCount(stats.follows), type: 'follows' }
          ]
        })
      })
      .catch(() => {
        showToast('个人中心暂不可用')
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  formatCount(value) {
    const count = Number(value || 0)

    if (count >= 10000) {
      return `${(count / 10000).toFixed(1)}w`
    }

    if (count >= 1000) {
      return `${(count / 1000).toFixed(1)}k`
    }

    return count
  },

  openStat(event) {
    const type = event.currentTarget.dataset.type

    navigateTo(`/pages/profile-list/profile-list?type=${type}`)
  },

  openMenuItem(event) {
    const action = event.currentTarget.dataset.action

    if (action === 'profileInfo') {
      navigateTo('/pages/profile-info/profile-info')
      return
    }

    if (action === 'feihualing') {
      navigateTo('/pages/profile-feihualing/profile-feihualing')
      return
    }

    if (action === 'feedback') {
      navigateTo('/pages/feedback/feedback')
      return
    }

    if (action === 'logout') {
      this.handleLogout()
      return
    }

    showToast(`${event.currentTarget.dataset.title}开发中`)
  },

  clearCache() {
    clearProjectStorage()
    showToast('缓存已清理', 'success')
  },

  handleLogout() {
    if (this.data.loggingOut) {
      return
    }

    wx.showModal({
      title: '退出登录',
      content: '确定退出当前账号吗？',
      confirmText: '退出',
      confirmColor: '#d71818',
      success: (res) => {
        if (!res.confirm) {
          return
        }

        this.setData({ loggingOut: true })
        showLoading('退出中')

        logout()
          .then(() => {
            showToast('已退出登录', 'success')
            wx.reLaunch({
              url: '/pages/login/login'
            })
          })
          .catch(() => {
            showToast('退出失败，请稍后重试')
          })
          .finally(() => {
            hideLoading()
            this.setData({ loggingOut: false })
          })
      }
    })
  }
})
