/**
 * 评论相关 API
 */
import { get, post, del } from '@/utils/request'

/**
 * 获取评论列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 评论列表
 */
export const getCommentList = (params = {}) => {
  return get('/comments', params)
}

/**
 * 获取评论详情
 * @param {number} commentId - 评论ID
 * @returns {Promise} 评论详情
 */
export const getCommentDetail = (commentId) => {
  return get(`/comments/${commentId}`)
}

/**
 * 删除评论
 * @param {number} commentId - 评论ID
 * @returns {Promise} 删除结果
 */
export const deleteComment = (commentId) => {
  return del(`/comments/${commentId}`)
}

/**
 * 点赞评论
 * @param {number} commentId - 评论ID
 * @returns {Promise} 点赞结果
 */
export const likeComment = (commentId) => {
  return post(`/comments/${commentId}/like`)
}

/**
 * 取消点赞评论
 * @param {number} commentId - 评论ID
 * @returns {Promise} 取消点赞结果
 */
export const unlikeComment = (commentId) => {
  return post(`/comments/${commentId}/unlike`)
}

/**
 * 回复评论
 * @param {number} commentId - 父评论ID
 * @param {Object} data - 回复数据
 * @returns {Promise} 回复结果
 */
export const replyComment = (commentId, data) => {
  return post(`/comments/${commentId}/reply`, data)
}

/**
 * 获取评论的回复列表
 * @param {number} commentId - 评论ID
 * @param {Object} params - 查询参数
 * @returns {Promise} 回复列表
 */
export const getCommentReplies = (commentId, params = {}) => {
  return get(`/comments/${commentId}/replies`, params)
}
