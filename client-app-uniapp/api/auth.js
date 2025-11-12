/**
 * 认证相关 API
 */
import { get, post } from '@/utils/request'

/**
 * 微信小程序登录
 * @param {string} code - 微信登录code
 * @returns {Promise} 登录结果
 */
export const loginByWeChat = (code) => {
  return post('/auth/login/wechat', { code })
}

/**
 * 账号密码登录
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @returns {Promise} 登录结果
 */
export const loginByPassword = (username, password) => {
  return post('/auth/login/password', { username, password })
}

/**
 * 刷新 Token
 * @param {string} refreshToken - 刷新令牌
 * @returns {Promise} 新的 token
 */
export const refreshToken = (refreshToken) => {
  return post('/auth/refresh', { refresh_token: refreshToken })
}

/**
 * 注册账号
 * @param {Object} data - 注册信息
 * @returns {Promise} 注册结果
 */
export const register = (data) => {
  return post('/auth/register', data)
}

/**
 * 登出
 * @returns {Promise} 登出结果
 */
export const logout = () => {
  return post('/auth/logout')
}
