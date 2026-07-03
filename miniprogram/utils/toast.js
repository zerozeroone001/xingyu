/**
 * 展示普通文本提示。
 * 小程序原生 toast 字数有限，调用方需要传入简短、明确的中文文案。
 */
function showToast(title, icon = 'none') {
  wx.showToast({
    title,
    icon,
    duration: 1800
  })
}

/**
 * 展示加载状态。
 * 统一封装后，页面层不需要直接关心 loading 的样式与遮罩设置。
 */
function showLoading(title = '加载中') {
  wx.showLoading({
    title,
    mask: true
  })
}

function hideLoading() {
  wx.hideLoading()
}

module.exports = {
  showToast,
  showLoading,
  hideLoading
}
