/**
 * 搜索相关 API
 */
import request, { ApiResponse, PaginationResponse } from '@/utils/request';
import { Poetry } from './poetry';

// 搜索参数
export interface SearchParams {
  query: string;
  page?: number;
  size?: number;
  dynasty?: string;
  type?: string;
  tags?: string[];
}

// 搜索建议项
export interface SearchSuggestion {
  text: string;
  type: 'poetry' | 'author' | 'tag';
}

/**
 * 全文搜索诗词
 */
export function searchPoetry(params: SearchParams): Promise<ApiResponse<PaginationResponse<Poetry>>> {
  return request.get('/search/poetry', { params });
}

/**
 * 获取搜索建议
 */
export function getSearchSuggestions(query: string): Promise<ApiResponse<SearchSuggestion[]>> {
  return request.get('/search/suggestions', { params: { query } });
}
