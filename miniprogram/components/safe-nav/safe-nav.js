Component({
  options: {
    multipleSlots: true,
    styleIsolation: 'shared'
  },

  properties: {
    background: {
      type: String,
      value: 'rgba(251, 248, 240, 0.9)'
    },
    border: {
      type: Boolean,
      value: true
    },
    offsetTop: {
      type: Number,
      value: 8
    },
    sideGap: {
      type: Number,
      value: 14
    }
  },

  data: {
    navHeight: 88,
    rowTop: 32,
    navBarHeight: 40,
    rightInset: 110,
    borderStyle: 'border-bottom: 1rpx solid rgba(31, 51, 70, 0.07);'
  },

  lifetimes: {
    attached() {
      this.updateLayout()
    }
  },

  methods: {
    updateLayout() {
      const info = wx.getWindowInfo ? wx.getWindowInfo() : wx.getSystemInfoSync()
      const capsule = wx.getMenuButtonBoundingClientRect ? wx.getMenuButtonBoundingClientRect() : null
      const statusBarHeight = info.statusBarHeight || 0
      const offsetTop = Number(this.data.offsetTop) || 0
      const sideGap = Number(this.data.sideGap) || 14

      let navHeight = statusBarHeight + 64
      let rowTop = statusBarHeight + 8 + offsetTop
      let navBarHeight = 44
      let rightInset = 110

      if (capsule && capsule.top && capsule.height) {
        const windowWidth = info.windowWidth || capsule.right || 0
        rowTop = capsule.top + offsetTop
        navBarHeight = capsule.height
        navHeight = capsule.bottom + offsetTop + 8
        rightInset = Math.max(96, windowWidth - capsule.left + sideGap)
      }

      const layout = {
        navHeight,
        rowTop,
        navBarHeight,
        rightInset,
        borderStyle: this.data.border ? 'border-bottom: 1rpx solid rgba(31, 51, 70, 0.07);' : 'border-bottom: 0;'
      }

      this.setData(layout)
      this.triggerEvent('layoutready', layout)
    }
  }
})
