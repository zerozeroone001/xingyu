/**
 * 关注相关 API
 */
import request, { ApiResponse, PaginationResponse } from '@/utils/request';
import { UserInfo } from './auth';

// 关注统计
export interface FollowStats {
  following_count: number;
  followers_count: number;
  is_following?: boolean;
  is_followed?: boolean;
}

/**
 * 关注用户
 */
export function followUser(userId: number): Promise<ApiResponse<{ following: boolean }>> {
  return request.post(`/follow/${userId}`);
}

/**
 * 取消关注
 */
export function unfollowUser(userId: number): Promise<ApiResponse<{ following: boolean }>> {
  return request.delete(`/follow/${userId}`);
}

/**
 * 检查关注状态
 */
export function checkFollowStatus(userId: number): Promise<ApiResponse<{ is_following: boolean }>> {
  return request.get(`/follow/${userId}/check`);
}

/**
 * 获取关注统计（需要用户ID）
 */
export function getFollowStats(userId: number): Promise<ApiResponse<FollowStats>> {
  return request.get(`/follow/${userId}/stats`);
}

/**
 * 获取关注列表
 */
export function getFollowingList(
  userId: number,
  params?: { page?: number; page_size?: number }
): Promise<ApiResponse<PaginationResponse<UserInfo>>> {
  return request.get('/follow/following/list', {
    params: { user_id: userId, ...params },
  });
}

/**
 * 获取粉丝列表
 */
export function getFollowersList(
  userId: number,
  params?: { page?: number; page_size?: number }
): Promise<ApiResponse<PaginationResponse<UserInfo>>> {
  return request.get('/follow/followers/list', {
    params: { user_id: userId, ...params },
  });
}

/**
 * 获取好友列表（互关）
 */
export function getFriendsList(params?: { page?: number; page_size?: number }): Promise<ApiResponse<PaginationResponse<UserInfo>>> {
  return request.get('/follow/friends/list', { params });
}
