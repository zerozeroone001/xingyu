Component({
  properties: {
    poem: {
      type: Object,
      value: {}
    }
  },

  methods: {
    handleTap() {
      // 组件只向外抛出点击事件，具体跳转由页面决定，避免组件和路由强绑定。
      this.triggerEvent('select', this.properties.poem)
    }
  }
})
