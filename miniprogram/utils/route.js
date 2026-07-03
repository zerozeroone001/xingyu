/**
 * 普通页面跳转。
 * 适用于非 tabBar 页面，例如诗词详情页。
 */
function navigateTo(url) {
  wx.navigateTo({ url })
}

/**
 * 主导航页面切换。
 * 主入口已接入微信原生 tabBar，统一使用 switchTab 保持 tab 状态和页面栈一致。
 */
function switchTab(url) {
  wx.switchTab({
    fail() {
      wx.reLaunch({ url })
    },
    url
  })
}

/**
 * 返回上一页；如果没有上一页，则回到首页。
 */
function navigateBack() {
  if (getCurrentPages().length > 1) {
    wx.navigateBack()
    return
  }

  wx.switchTab({
    fail() {
      wx.reLaunch({
        url: '/pages/home/home'
      })
    },
    url: '/pages/home/home'
  })
}

module.exports = {
  navigateTo,
  switchTab,
  navigateBack
}
