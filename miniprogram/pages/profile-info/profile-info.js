const { getCurrentUser, updateCurrentUser } = require('../../services/user')
const { showToast } = require('../../utils/toast')

Page({
  data: {
    loading: false,
    saving: false,
    form: {
      nickname: '',
      title: '',
      city: '',
      bio: ''
    },
    avatarText: '诗',
    level: 1
  },

  onLoad() {
    this.loadProfile()
  },

  loadProfile() {
    this.setData({ loading: true })

    return getCurrentUser()
      .then((user) => {
        this.setData({
          avatarText: user.avatarText || (user.nickname || '诗').slice(0, 1),
          level: user.level || 1,
          form: {
            nickname: user.nickname || '',
            title: user.title || '',
            city: user.city || '',
            bio: user.bio || ''
          }
        })
      })
      .catch(() => {
        showToast('个人信息暂不可用')
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  handleInput(event) {
    const field = event.currentTarget.dataset.field
    const value = event.detail.value

    this.setData({
      [`form.${field}`]: value
    })
  },

  saveProfile() {
    const form = this.data.form
    const nickname = String(form.nickname || '').trim()

    if (!nickname) {
      showToast('请填写昵称')
      return
    }

    this.setData({ saving: true })

    updateCurrentUser(Object.assign({}, form, { nickname }))
      .then((user) => {
        this.setData({
          avatarText: user.avatarText || nickname.slice(0, 1)
        })
        showToast('个人信息已保存', 'success')
      })
      .catch(() => {
        showToast('保存失败')
      })
      .finally(() => {
        this.setData({ saving: false })
      })
  }
})
