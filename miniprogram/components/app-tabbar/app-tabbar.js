Component({
  properties: {
    active: {
      type: String,
      value: 'home'
    }
  },

  methods: {
    goPage(event) {
      const url = event.currentTarget.dataset.url
      const current = `/${getCurrentPages().slice(-1)[0].route}`

      // 当前页重复点击不重新加载，避免列表滚动位置被重置。
      if (current === url) {
        return
      }

      wx.reLaunch({ url })
    }
  }
})
