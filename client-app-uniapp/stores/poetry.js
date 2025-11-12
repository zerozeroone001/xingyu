import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getPoetryList, getPoetryDetail, getRandomPoetry, getRecommendPoetries } from '@/api/poetry'

/**
 * 诗词 Store
 * 管理诗词数据和状态
 */
export const usePoetryStore = defineStore('poetry', () => {
  // 诗词列表
  const poetryList = ref([])

  // 当前诗词详情
  const currentPoetry = ref(null)

  // 推荐诗词列表
  const recommendList = ref([])

  // 加载状态
  const loading = ref(false)

  /**
   * 获取诗词列表
   * @param {Object} params - 查询参数
   * @returns {Promise} 诗词列表
   */
  const fetchPoetryList = async (params = {}) => {
    try {
      loading.value = true
      const data = await getPoetryList(params)
      poetryList.value = data.items || []
      return data
    } catch (e) {
      console.error('获取诗词列表失败:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取更多诗词（分页加载）
   * @param {Object} params - 查询参数
   * @returns {Promise} 诗词列表
   */
  const fetchMorePoetries = async (params = {}) => {
    try {
      const data = await getPoetryList(params)
      poetryList.value = [...poetryList.value, ...(data.items || [])]
      return data
    } catch (e) {
      console.error('获取更多诗词失败:', e)
      throw e
    }
  }

  /**
   * 获取诗词详情
   * @param {number} poetryId - 诗词ID
   * @returns {Promise} 诗词详情
   */
  const fetchPoetryDetail = async (poetryId) => {
    try {
      loading.value = true
      const data = await getPoetryDetail(poetryId)
      currentPoetry.value = data
      return data
    } catch (e) {
      console.error('获取诗词详情失败:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取随机诗词
   * @returns {Promise} 随机诗词
   */
  const fetchRandomPoetry = async () => {
    try {
      const data = await getRandomPoetry()
      return data
    } catch (e) {
      console.error('获取随机诗词失败:', e)
      throw e
    }
  }

  /**
   * 获取推荐诗词
   * @param {Object} params - 查询参数
   * @returns {Promise} 推荐诗词列表
   */
  const fetchRecommendPoetries = async (params = {}) => {
    try {
      const data = await getRecommendPoetries(params)
      recommendList.value = data.items || []
      return data
    } catch (e) {
      console.error('获取推荐诗词失败:', e)
      throw e
    }
  }

  /**
   * 清空诗词列表
   */
  const clearPoetryList = () => {
    poetryList.value = []
  }

  return {
    poetryList,
    currentPoetry,
    recommendList,
    loading,
    fetchPoetryList,
    fetchMorePoetries,
    fetchPoetryDetail,
    fetchRandomPoetry,
    fetchRecommendPoetries,
    clearPoetryList
  }
})
