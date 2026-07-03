/**
 * 将接口返回的日期文本格式化为小程序展示文案。
 * 当前初始化阶段只做兜底处理，后续可按业务扩展为“今天”“昨天”等格式。
 */
function formatDate(value) {
  if (!value) {
    return ''
  }

  return String(value).replace('T', ' ').slice(0, 16)
}

module.exports = {
  formatDate
}
