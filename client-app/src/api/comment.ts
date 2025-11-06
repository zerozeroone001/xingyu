/**
 * 评论相关 API
 */
import request, { ApiResponse, PaginationResponse } from '@/utils/request';

// 评论接口
export interface Comment {
  id: number;
  poetry_id: number;
  user_id: number;
  user_name: string;
  user_avatar?: string;
  parent_id?: number;
  content: string;
  likes_count: number;
  replies_count: number;
  created_at: string;
  updated_at: string;
}

// 评论列表查询参数
export interface CommentListParams {
  page?: number;
  size?: number;
  sort_by?: string;
  order?: 'asc' | 'desc';
}

// 创建评论参数
export interface CreateCommentParams {
  poetry_id: number;
  content: string;
  parent_id?: number;
}

/**
 * 获取诗词的评论列表（一级评论）
 */
export function getPoetryCommentList(
  poetryId: number,
  params?: CommentListParams
): Promise<ApiResponse<PaginationResponse<Comment>>> {
  return request.get(`/poetry/${poetryId}/comments`, { params });
}

/**
 * 获取评论的回复列表（二级评论）
 */
export function getCommentReplies(
  commentId: number,
  params?: CommentListParams
): Promise<ApiResponse<PaginationResponse<Comment>>> {
  return request.get(`/comments/${commentId}/replies`, { params });
}

/**
 * 创建评论
 */
export function createComment(data: CreateCommentParams): Promise<ApiResponse<Comment>> {
  return request.post('/comments', data);
}

/**
 * 更新评论
 */
export function updateComment(id: number, content: string): Promise<ApiResponse<Comment>> {
  return request.put(`/comments/${id}`, { content });
}

/**
 * 删除评论
 */
export function deleteComment(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/comments/${id}`);
}

/**
 * 获取用户的评论列表
 */
export function getUserCommentList(params?: CommentListParams): Promise<ApiResponse<PaginationResponse<Comment>>> {
  return request.get('/user/comments', { params });
}
