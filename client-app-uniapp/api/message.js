/**
 * 消息相关 API
 */
import { get, post, put } from '@/utils/request'

/**
 * 获取消息列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 消息列表
 */
export const getMessageList = (params = {}) => {
  return get('/messages', params)
}

/**
 * 获取未读消息数
 * @returns {Promise} 未读消息数
 */
export const getUnreadCount = () => {
  return get('/messages/unread/count')
}

/**
 * 标记消息为已读
 * @param {number} messageId - 消息ID
 * @returns {Promise} 标记结果
 */
export const markMessageRead = (messageId) => {
  return put(`/messages/${messageId}/read`)
}

/**
 * 标记所有消息为已读
 * @returns {Promise} 标记结果
 */
export const markAllMessagesRead = () => {
  return put('/messages/read/all')
}

/**
 * 删除消息
 * @param {number} messageId - 消息ID
 * @returns {Promise} 删除结果
 */
export const deleteMessage = (messageId) => {
  return del(`/messages/${messageId}`)
}
