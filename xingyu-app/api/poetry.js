/**
 * 诗词相关API接口
 * 对接后端FastAPI服务
 */
import {
	get,
	post,
	del
} from './request.js'

/**
 * 获取推荐诗词
 * @returns {Promise}
 */
export function getRecommendPoetry() {
	return get('/poetry/recommend')
}

/**
 * 获取诗词列表
 * @param {Object} params 查询参数
 * @param {Number} params.page 页码
 * @param {Number} params.page_size 每页数量
 * @param {String} params.dynasty 朝代(可选)
 * @param {String} params.type 类型(可选)
 * @param {String} params.author 作者(可选)
 * @returns {Promise}
 */
export function getPoetryList(params) {
	return get('/poetry/list', params)
}

/**
 * 搜索诗词
 * @param {Object} params 查询参数
 * @param {String} params.keyword 关键词
 * @param {Number} params.page 页码
 * @param {Number} params.page_size 每页数量
 * @returns {Promise}
 */
export function searchPoetry(params) {
	return get('/poetry/search', params)
}

/**
 * 获取诗词详情
 * @param {Number} id 诗词ID
 * @returns {Promise}
 */
export function getPoetryDetail(id) {
	return get(`/poetry/${id}`)
}

/**
 * 点赞诗词
 * @param {Number} id 诗词ID
 * @returns {Promise}
 */
export function likePoetry(id) {
	return post(`/poetry/${id}/like`)
}

/**
 * 取消点赞
 * @param {Number} id 诗词ID
 * @returns {Promise}
 */
export function unlikePoetry(id) {
	return del(`/poetry/${id}/like`)
}

/**
 * 收藏诗词
 * @param {Number} id 诗词ID
 * @returns {Promise}
 */
export function collectPoetry(id) {
	return post(`/poetry/${id}/collect`)
}

/**
 * 取消收藏
 * @param {Number} id 诗词ID
 * @returns {Promise}
 */
export function uncollectPoetry(id) {
	return del(`/poetry/${id}/collect`)
}

/**
 * 获取诗词评论
 * @param {Number} id 诗词ID
 * @param {Object} params 查询参数
 * @param {String} params.sort 排序方式(latest/hot)
 * @param {Number} params.page 页码
 * @param {Number} params.page_size 每页数量
 * @returns {Promise}
 */
export function getPoetryComments(id, params) {
	return get(`/poetry/${id}/comments`, params)
}

/**
 * 发表评论
 * @param {Object} data 评论数据
 * @param {String} data.target_type 目标类型(poetry/post)
 * @param {Number} data.target_id 目标ID
 * @param {Number} data.parent_id 父评论ID(可选)
 * @param {String} data.content 评论内容
 * @returns {Promise}
 */
export function addComment(data) {
	return post('/comments', data)
}

/**
 * 删除评论
 * @param {Number} id 评论ID
 * @returns {Promise}
 */
export function deleteComment(id) {
	return del(`/comments/${id}`)
}

// 默认导出
export default {
	getRecommendPoetry,
	getPoetryList,
	searchPoetry,
	getPoetryDetail,
	likePoetry,
	unlikePoetry,
	collectPoetry,
	uncollectPoetry,
	getPoetryComments,
	addComment,
	deleteComment
}
