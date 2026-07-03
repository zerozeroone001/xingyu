const { logout } = require('../../services/auth')
const { clearProjectStorage } = require('../../utils/cache')
const { showToast } = require('../../utils/toast')

Page({
  data: {
    stats: [
      { label: '诗作', value: '128' },
      { label: '获赞', value: '3.2k' },
      { label: '禅值', value: '980' }
    ],
    menus: [
      { title: '我的点赞', subtitle: '共赏诗情画意', type: 'heart' },
      { title: '我的收藏', subtitle: '私藏千古绝句', type: 'bookmark' },
      { title: '我的关注', subtitle: '结交诗友文豪', type: 'users' },
      { title: '我的发布', subtitle: '墨香流传千秋', type: 'edit' }
    ]
  },

  openMenu() {
    showToast('菜单开发中')
  },

  openSearch() {
    showToast('搜索开发中')
  },

  openMenuItem(event) {
    showToast(`${event.currentTarget.dataset.title}开发中`)
  },

  clearCache() {
    clearProjectStorage()
    showToast('缓存已清理', 'success')
  },

  handleLogout() {
    logout()
    showToast('已退出登录', 'success')
  }
})
