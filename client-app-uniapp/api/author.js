/**
 * 作者（诗人）相关 API
 */
import { get } from '@/utils/request'

/**
 * 获取作者列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 作者列表
 */
export const getAuthorList = (params = {}) => {
  return get('/authors', params)
}

/**
 * 获取作者详情
 * @param {number} authorId - 作者ID
 * @returns {Promise} 作者详情
 */
export const getAuthorDetail = (authorId) => {
  return get(`/authors/${authorId}`)
}

/**
 * 获取作者的诗词列表
 * @param {number} authorId - 作者ID
 * @param {Object} params - 查询参数
 * @returns {Promise} 诗词列表
 */
export const getAuthorPoetries = (authorId, params = {}) => {
  return get(`/authors/${authorId}/poetries`, params)
}
