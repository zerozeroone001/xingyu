/**
 * 诗词相关 API
 */
import { get, post, put, del } from '@/utils/request'

/**
 * 获取诗词列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 诗词列表
 */
export const getPoetryList = (params = {}) => {
  return get('/poetries', params)
}

/**
 * 获取诗词详情
 * @param {number} poetryId - 诗词ID
 * @returns {Promise} 诗词详情
 */
export const getPoetryDetail = (poetryId) => {
  return get(`/poetries/${poetryId}`)
}

/**
 * 随机获取诗词
 * @returns {Promise} 随机诗词
 */
export const getRandomPoetry = () => {
  return get('/poetries/random')
}

/**
 * 获取推荐诗词
 * @param {Object} params - 查询参数
 * @returns {Promise} 推荐诗词列表
 */
export const getRecommendPoetries = (params = {}) => {
  return get('/poetries/recommend', params)
}

/**
 * 搜索诗词
 * @param {string} keyword - 搜索关键词
 * @param {Object} params - 查询参数
 * @returns {Promise} 搜索结果
 */
export const searchPoetries = (keyword, params = {}) => {
  return get('/poetries/search', { keyword, ...params })
}

/**
 * 点赞诗词
 * @param {number} poetryId - 诗词ID
 * @returns {Promise} 点赞结果
 */
export const likePoetry = (poetryId) => {
  return post(`/poetries/${poetryId}/like`)
}

/**
 * 取消点赞诗词
 * @param {number} poetryId - 诗词ID
 * @returns {Promise} 取消点赞结果
 */
export const unlikePoetry = (poetryId) => {
  return post(`/poetries/${poetryId}/unlike`)
}

/**
 * 收藏诗词
 * @param {number} poetryId - 诗词ID
 * @returns {Promise} 收藏结果
 */
export const collectPoetry = (poetryId) => {
  return post(`/poetries/${poetryId}/collect`)
}

/**
 * 取消收藏诗词
 * @param {number} poetryId - 诗词ID
 * @returns {Promise} 取消收藏结果
 */
export const uncollectPoetry = (poetryId) => {
  return post(`/poetries/${poetryId}/uncollect`)
}

/**
 * 获取诗词评论列表
 * @param {number} poetryId - 诗词ID
 * @param {Object} params - 查询参数
 * @returns {Promise} 评论列表
 */
export const getPoetryComments = (poetryId, params = {}) => {
  return get(`/poetries/${poetryId}/comments`, params)
}

/**
 * 发表诗词评论
 * @param {number} poetryId - 诗词ID
 * @param {Object} data - 评论数据
 * @returns {Promise} 评论结果
 */
export const createPoetryComment = (poetryId, data) => {
  return post(`/poetries/${poetryId}/comments`, data)
}
