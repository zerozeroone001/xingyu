/**
 * 广场/动态相关 API
 */
import request, { ApiResponse, PaginationResponse } from '@/utils/request';

// 动态类型
export enum PostType {
  ORIGINAL = 'original', // 原创
  SHARE = 'share', // 分享诗词
}

// 动态接口
export interface Post {
  id: number;
  user_id: number;
  user_name: string;
  user_avatar?: string;
  type: PostType;
  content: string;
  images?: string[];
  tags?: string[];
  poetry_id?: number;
  poetry_title?: string;
  poetry_content?: string;
  likes_count: number;
  comments_count: number;
  collects_count: number;
  views_count: number;
  created_at: string;
  updated_at: string;
}

// 动态列表查询参数
export interface PostListParams {
  page?: number;
  size?: number;
  type?: PostType;
  user_id?: number;
  sort_by?: string;
  order?: 'asc' | 'desc';
}

// 创建动态参数
export interface CreatePostParams {
  type: PostType;
  content: string;
  images?: string[];
  tags?: string[];
  poetry_id?: number;
}

/**
 * 获取动态列表（广场）
 */
export function getPostList(params?: PostListParams): Promise<ApiResponse<PaginationResponse<Post>>> {
  return request.get('/posts', { params });
}

/**
 * 获取关注用户的动态流
 */
export function getFollowingPostList(params?: { page?: number; size?: number }): Promise<ApiResponse<PaginationResponse<Post>>> {
  return request.get('/posts/following', { params });
}

/**
 * 获取动态详情
 */
export function getPostDetail(id: number): Promise<ApiResponse<Post>> {
  return request.get(`/posts/${id}`);
}

/**
 * 创建动态
 */
export function createPost(data: CreatePostParams): Promise<ApiResponse<Post>> {
  return request.post('/posts', data);
}

/**
 * 更新动态
 */
export function updatePost(id: number, data: Partial<CreatePostParams>): Promise<ApiResponse<Post>> {
  return request.put(`/posts/${id}`, data);
}

/**
 * 删除动态
 */
export function deletePost(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/posts/${id}`);
}

/**
 * 点赞动态
 */
export function likePost(id: number): Promise<ApiResponse<void>> {
  return request.post(`/posts/${id}/like`);
}

/**
 * 取消点赞
 */
export function unlikePost(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/posts/${id}/like`);
}

/**
 * 收藏动态
 */
export function collectPost(id: number): Promise<ApiResponse<void>> {
  return request.post(`/posts/${id}/collect`);
}

/**
 * 取消收藏
 */
export function uncollectPost(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/posts/${id}/collect`);
}

/**
 * 获取用户的动态列表
 */
export function getUserPostList(userId?: number, params?: { page?: number; size?: number }): Promise<ApiResponse<PaginationResponse<Post>>> {
  const url = userId ? `/users/${userId}/posts` : '/user/posts';
  return request.get(url, { params });
}
