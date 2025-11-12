/**
 * 飞花令游戏相关 API
 */
import { get, post } from '@/utils/request'

/**
 * 创建游戏房间
 * @param {Object} data - 房间配置
 * @returns {Promise} 房间信息
 */
export const createGameRoom = (data) => {
  return post('/game/rooms', data)
}

/**
 * 加入游戏房间
 * @param {number} roomId - 房间ID
 * @returns {Promise} 加入结果
 */
export const joinGameRoom = (roomId) => {
  return post(`/game/rooms/${roomId}/join`)
}

/**
 * 获取游戏房间列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 房间列表
 */
export const getGameRoomList = (params = {}) => {
  return get('/game/rooms', params)
}

/**
 * 获取游戏房间详情
 * @param {number} roomId - 房间ID
 * @returns {Promise} 房间详情
 */
export const getGameRoomDetail = (roomId) => {
  return get(`/game/rooms/${roomId}`)
}

/**
 * 提交答案
 * @param {number} roomId - 房间ID
 * @param {Object} data - 答案数据
 * @returns {Promise} 提交结果
 */
export const submitAnswer = (roomId, data) => {
  return post(`/game/rooms/${roomId}/answer`, data)
}

/**
 * 获取游戏记录
 * @param {number} roomId - 房间ID
 * @returns {Promise} 游戏记录
 */
export const getGameRecords = (roomId) => {
  return get(`/game/rooms/${roomId}/records`)
}

/**
 * 获取用户游戏历史
 * @param {Object} params - 查询参数
 * @returns {Promise} 游戏历史
 */
export const getUserGameHistory = (params = {}) => {
  return get('/game/history', params)
}

/**
 * 获取游戏排行榜
 * @param {Object} params - 查询参数
 * @returns {Promise} 排行榜
 */
export const getGameRank = (params = {}) => {
  return get('/game/rank', params)
}
