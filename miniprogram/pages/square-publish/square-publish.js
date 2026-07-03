const { createSquareTopic } = require('../../services/square')
const { showToast } = require('../../utils/toast')
const { navigateBack } = require('../../utils/route')

Page({
  data: {
    content: '',
    images: [],
    selectedTags: ['随笔'],
    customTag: '',
    submitting: false,
    maxImages: 9,
    tagOptions: [
      { name: '随笔', selected: true },
      { name: '山水', selected: false },
      { name: '摘句', selected: false },
      { name: '飞花令', selected: false },
      { name: '读后感', selected: false },
      { name: '月色', selected: false },
      { name: '春日', selected: false },
      { name: '行旅', selected: false }
    ]
  },

  handleContentInput(event) {
    this.setData({ content: event.detail.value })
  },

  handleCustomTagInput(event) {
    this.setData({ customTag: event.detail.value })
  },

  toggleTag(event) {
    const tag = event.currentTarget.dataset.tag
    const selectedTags = this.data.selectedTags.slice()
    const index = selectedTags.indexOf(tag)

    if (index >= 0) {
      selectedTags.splice(index, 1)
    } else {
      selectedTags.push(tag)
    }

    this.setData({
      selectedTags,
      tagOptions: this.syncTagOptions(this.data.tagOptions, selectedTags)
    })
  },

  addCustomTag() {
    const tag = this.data.customTag.trim()

    if (!tag) {
      showToast('请输入标签')
      return
    }

    const hasOption = this.data.tagOptions.some((item) => item.name === tag)
    const tagOptions = hasOption ? this.data.tagOptions : this.data.tagOptions.concat({ name: tag, selected: true })
    const selectedTags = this.data.selectedTags.indexOf(tag) >= 0 ? this.data.selectedTags : this.data.selectedTags.concat(tag)

    this.setData({
      tagOptions: this.syncTagOptions(tagOptions, selectedTags),
      selectedTags,
      customTag: ''
    })
  },

  syncTagOptions(tagOptions, selectedTags) {
    return tagOptions.map((item) => ({
      name: item.name,
      selected: selectedTags.indexOf(item.name) >= 0
    }))
  },

  chooseImages() {
    const remain = this.data.maxImages - this.data.images.length

    if (remain <= 0) {
      showToast('最多选择 9 张图片')
      return
    }

    wx.chooseImage({
      count: remain,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        this.setData({
          images: this.data.images.concat(res.tempFilePaths || []).slice(0, this.data.maxImages)
        })
      }
    })
  },

  removeImage(event) {
    const index = Number(event.currentTarget.dataset.index)
    const images = this.data.images.slice()

    images.splice(index, 1)
    this.setData({ images })
  },

  previewImage(event) {
    const src = event.currentTarget.dataset.src

    wx.previewImage({
      current: src,
      urls: this.data.images
    })
  },

  submitTopic() {
    const content = this.data.content.trim()
    const tags = this.data.selectedTags.slice()

    if (!content) {
      showToast('请写下配文')
      return
    }

    if (!tags.length) {
      showToast('请至少选择一个标签')
      return
    }

    this.setData({ submitting: true })

    createSquareTopic({
      content,
      tags,
      images: this.data.images
    })
      .then((topic) => {
        showToast('发布成功', 'success')
        wx.redirectTo({
          url: `/pages/square-detail/square-detail?id=${topic.id}`
        })
      })
      .catch(() => {
        showToast('发布失败，请稍后重试')
      })
      .finally(() => {
        this.setData({ submitting: false })
      })
  },

  goBack() {
    navigateBack()
  }
})
