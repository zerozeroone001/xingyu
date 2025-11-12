/**
 * 用户相关 API
 */
import { get, post, put } from '@/utils/request'

/**
 * 获取当前用户信息
 * @returns {Promise} 用户信息
 */
export const getUserInfo = () => {
  return get('/users/me')
}

/**
 * 获取用户详情
 * @param {number} userId - 用户ID
 * @returns {Promise} 用户详情
 */
export const getUserDetail = (userId) => {
  return get(`/users/${userId}`)
}

/**
 * 更新用户信息
 * @param {Object} data - 用户信息
 * @returns {Promise} 更新结果
 */
export const updateUserInfo = (data) => {
  return put('/users/me', data)
}

/**
 * 获取用户关注列表
 * @param {number} userId - 用户ID
 * @param {Object} params - 查询参数
 * @returns {Promise} 关注列表
 */
export const getUserFollows = (userId, params = {}) => {
  return get(`/users/${userId}/follows`, params)
}

/**
 * 获取用户粉丝列表
 * @param {number} userId - 用户ID
 * @param {Object} params - 查询参数
 * @returns {Promise} 粉丝列表
 */
export const getUserFollowers = (userId, params = {}) => {
  return get(`/users/${userId}/followers`, params)
}

/**
 * 关注用户
 * @param {number} userId - 用户ID
 * @returns {Promise} 关注结果
 */
export const followUser = (userId) => {
  return post(`/users/${userId}/follow`)
}

/**
 * 取消关注用户
 * @param {number} userId - 用户ID
 * @returns {Promise} 取消关注结果
 */
export const unfollowUser = (userId) => {
  return post(`/users/${userId}/unfollow`)
}
