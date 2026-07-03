const { submitFeedback } = require('../../services/user')
const { showToast } = require('../../utils/toast')

Page({
  data: {
    categories: ['功能建议', '内容纠错', '体验问题'],
    activeCategory: '功能建议',
    content: '',
    contact: '',
    submitting: false
  },

  chooseCategory(event) {
    this.setData({
      activeCategory: event.currentTarget.dataset.category
    })
  },

  handleInput(event) {
    const field = event.currentTarget.dataset.field

    this.setData({
      [field]: event.detail.value
    })
  },

  submit() {
    const content = String(this.data.content || '').trim()

    if (content.length < 5) {
      showToast('请至少输入 5 个字')
      return
    }

    this.setData({ submitting: true })

    submitFeedback({
      category: this.data.activeCategory,
      content,
      contact: String(this.data.contact || '').trim()
    })
      .then(() => {
        showToast('反馈已提交', 'success')
        this.setData({
          content: '',
          contact: '',
          activeCategory: '功能建议'
        })
      })
      .catch(() => {
        showToast('提交失败')
      })
      .finally(() => {
        this.setData({ submitting: false })
      })
  }
})
