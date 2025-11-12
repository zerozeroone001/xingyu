/**
 * 广场相关 API
 */
import { get, post, del } from '@/utils/request'
import { upload } from '@/utils/request'

/**
 * 获取广场内容列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 内容列表
 */
export const getPostList = (params = {}) => {
  return get('/posts', params)
}

/**
 * 获取内容详情
 * @param {number} postId - 内容ID
 * @returns {Promise} 内容详情
 */
export const getPostDetail = (postId) => {
  return get(`/posts/${postId}`)
}

/**
 * 发布内容
 * @param {Object} data - 内容数据
 * @returns {Promise} 发布结果
 */
export const createPost = (data) => {
  return post('/posts', data)
}

/**
 * 删除内容
 * @param {number} postId - 内容ID
 * @returns {Promise} 删除结果
 */
export const deletePost = (postId) => {
  return del(`/posts/${postId}`)
}

/**
 * 点赞内容
 * @param {number} postId - 内容ID
 * @returns {Promise} 点赞结果
 */
export const likePost = (postId) => {
  return post(`/posts/${postId}/like`)
}

/**
 * 取消点赞内容
 * @param {number} postId - 内容ID
 * @returns {Promise} 取消点赞结果
 */
export const unlikePost = (postId) => {
  return post(`/posts/${postId}/unlike`)
}

/**
 * 收藏内容
 * @param {number} postId - 内容ID
 * @returns {Promise} 收藏结果
 */
export const collectPost = (postId) => {
  return post(`/posts/${postId}/collect`)
}

/**
 * 取消收藏内容
 * @param {number} postId - 内容ID
 * @returns {Promise} 取消收藏结果
 */
export const uncollectPost = (postId) => {
  return post(`/posts/${postId}/uncollect`)
}

/**
 * 获取内容评论列表
 * @param {number} postId - 内容ID
 * @param {Object} params - 查询参数
 * @returns {Promise} 评论列表
 */
export const getPostComments = (postId, params = {}) => {
  return get(`/posts/${postId}/comments`, params)
}

/**
 * 发表内容评论
 * @param {number} postId - 内容ID
 * @param {Object} data - 评论数据
 * @returns {Promise} 评论结果
 */
export const createPostComment = (postId, data) => {
  return post(`/posts/${postId}/comments`, data)
}

/**
 * 上传图片
 * @param {string} filePath - 文件路径
 * @returns {Promise} 上传结果
 */
export const uploadImage = (filePath) => {
  return upload('/upload/image', filePath)
}
