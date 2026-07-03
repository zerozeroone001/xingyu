// 小程序端集中配置文件。页面和服务层读取配置时统一从这里取值，避免到处写硬编码。
const config = {
  apiBaseUrl: 'http://127.0.0.1:8000/api/v1',
  requestTimeout: 10000,
  storagePrefix: 'xingyu:',
  // 开发初始化阶段默认使用本地 mock 数据，避免依赖微信登录和后端服务。
  useMock: true
}

module.exports = config
