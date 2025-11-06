/**
 * 推荐相关 API
 */
import request, { ApiResponse, PaginationResponse } from '@/utils/request';
import { Poetry } from './poetry';

/**
 * 获取热门推荐
 */
export function getHotRecommendations(params?: { page?: number; size?: number }): Promise<ApiResponse<PaginationResponse<Poetry>>> {
  return request.get('/recommendations/hot', { params });
}

/**
 * 获取随机推荐
 */
export function getRandomRecommendations(count?: number): Promise<ApiResponse<Poetry[]>> {
  return request.get('/recommendations/random', { params: { count } });
}

/**
 * 获取每日推荐
 */
export function getDailyRecommendations(): Promise<ApiResponse<Poetry[]>> {
  return request.get('/recommendations/daily');
}

/**
 * 获取相似诗词推荐
 */
export function getSimilarPoetry(poetryId: number, limit?: number): Promise<ApiResponse<Poetry[]>> {
  return request.get(`/recommendations/similar/${poetryId}`, { params: { limit } });
}

/**
 * 获取个性化推荐
 */
export function getPersonalizedRecommendations(params?: { page?: number; size?: number }): Promise<ApiResponse<PaginationResponse<Poetry>>> {
  return request.get('/recommendations/personalized', { params });
}
