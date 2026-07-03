const { storagePrefix } = require('./config')

/**
 * 生成带项目命名空间的缓存 key。
 * 这样可以避免和同一微信环境下的其他调试项目发生 key 冲突。
 */
function buildKey(key) {
  return `${storagePrefix}${key}`
}

/**
 * 写入本地缓存。
 * @param {string} key 业务缓存 key
 * @param {*} value 需要缓存的数据
 */
function setStorage(key, value) {
  wx.setStorageSync(buildKey(key), value)
}

/**
 * 读取本地缓存。
 * @param {string} key 业务缓存 key
 * @param {*} defaultValue 缓存不存在时返回的默认值
 */
function getStorage(key, defaultValue = null) {
  const value = wx.getStorageSync(buildKey(key))
  return value === '' || value === undefined ? defaultValue : value
}

/**
 * 删除指定缓存。
 * @param {string} key 业务缓存 key
 */
function removeStorage(key) {
  wx.removeStorageSync(buildKey(key))
}

/**
 * 清理当前项目命名空间下的所有缓存。
 * 注意：不会删除其他小程序或其他项目写入的缓存。
 */
function clearProjectStorage() {
  const info = wx.getStorageInfoSync()
  info.keys.forEach((key) => {
    if (key.indexOf(storagePrefix) === 0) {
      wx.removeStorageSync(key)
    }
  })
}

module.exports = {
  buildKey,
  setStorage,
  getStorage,
  removeStorage,
  clearProjectStorage
}
