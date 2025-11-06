/**
 * 作者相关 API
 */
import request, { ApiResponse, PaginationResponse } from '@/utils/request';
import { Poetry } from './poetry';

// 作者接口
export interface Author {
  id: number;
  name: string;
  dynasty: string;
  birth_year?: string;
  death_year?: string;
  biography?: string;
  avatar?: string;
  poetry_count: number;
  views_count: number;
  created_at: string;
  updated_at: string;
}

// 作者列表查询参数
export interface AuthorListParams {
  page?: number;
  size?: number;
  search?: string;
  dynasty?: string;
  sort_by?: string;
  order?: 'asc' | 'desc';
}

/**
 * 获取作者列表
 */
export function getAuthorList(params?: AuthorListParams): Promise<ApiResponse<PaginationResponse<Author>>> {
  return request.get('/authors', { params });
}

/**
 * 获取作者详情
 */
export function getAuthorDetail(id: number): Promise<ApiResponse<Author>> {
  return request.get(`/authors/${id}`);
}

/**
 * 获取作者的诗词列表
 */
export function getAuthorPoetryList(
  id: number,
  params?: { page?: number; size?: number }
): Promise<ApiResponse<PaginationResponse<Poetry>>> {
  return request.get(`/authors/${id}/poetry`, { params });
}

/**
 * 获取热门作者
 */
export function getHotAuthorList(params?: { page?: number; size?: number }): Promise<ApiResponse<PaginationResponse<Author>>> {
  return request.get('/authors/hot', { params });
}

/**
 * 按朝代获取作者
 */
export function getAuthorsByDynasty(
  dynasty: string,
  params?: { page?: number; size?: number }
): Promise<ApiResponse<PaginationResponse<Author>>> {
  return request.get(`/authors/dynasty/${dynasty}`, { params });
}
