/**
 * 诗词相关 API
 */
import request, { ApiResponse, PaginationResponse } from '@/utils/request';

// 诗词接口
export interface Poetry {
  id: number;
  title: string;
  content: string;
  author_id: number;
  author_name: string;
  dynasty: string;
  type?: string;
  tags?: string[];
  translation?: string;
  annotation?: string;
  appreciation?: string;
  views_count: number;
  likes_count: number;
  collects_count: number;
  comments_count: number;
  created_at: string;
  updated_at: string;
}

// 诗词列表查询参数
export interface PoetryListParams {
  page?: number;
  size?: number;
  search?: string;
  dynasty?: string;
  type?: string;
  author_id?: number;
  sort_by?: string;
  order?: 'asc' | 'desc';
}

/**
 * 获取诗词列表
 */
export function getPoetryList(params?: PoetryListParams): Promise<ApiResponse<PaginationResponse<Poetry>>> {
  return request.get('/poetry', { params });
}

/**
 * 获取诗词详情
 */
export function getPoetryDetail(id: number): Promise<ApiResponse<Poetry>> {
  return request.get(`/poetry/${id}`);
}

/**
 * 获取随机诗词
 */
export function getRandomPoetry(): Promise<ApiResponse<Poetry>> {
  return request.get('/poetry/random');
}

/**
 * 获取热门诗词
 */
export function getHotPoetryList(params?: { page?: number; size?: number }): Promise<ApiResponse<PaginationResponse<Poetry>>> {
  return request.get('/poetry/hot', { params });
}

/**
 * 点赞诗词
 */
export function likePoetry(id: number): Promise<ApiResponse<void>> {
  return request.post(`/poetry/${id}/like`);
}

/**
 * 取消点赞
 */
export function unlikePoetry(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/poetry/${id}/like`);
}

/**
 * 收藏诗词
 */
export function collectPoetry(id: number): Promise<ApiResponse<void>> {
  return request.post(`/poetry/${id}/collect`);
}

/**
 * 取消收藏
 */
export function uncollectPoetry(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/poetry/${id}/collect`);
}

/**
 * 检查点赞状态
 */
export function checkLikeStatus(id: number): Promise<ApiResponse<{ liked: boolean }>> {
  return request.get(`/poetry/${id}/like/status`);
}

/**
 * 检查收藏状态
 */
export function checkCollectStatus(id: number): Promise<ApiResponse<{ collected: boolean }>> {
  return request.get(`/poetry/${id}/collect/status`);
}

/**
 * 获取用户点赞的诗词列表
 */
export function getUserLikedPoetryList(params?: { page?: number; size?: number }): Promise<ApiResponse<PaginationResponse<Poetry>>> {
  return request.get('/user/poetry/likes', { params });
}

/**
 * 获取用户收藏的诗词列表
 */
export function getUserCollectedPoetryList(params?: { page?: number; size?: number }): Promise<ApiResponse<PaginationResponse<Poetry>>> {
  return request.get('/user/poetry/collects', { params });
}
