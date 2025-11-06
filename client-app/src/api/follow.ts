/**
 * 关注相关 API
 */
import request, { ApiResponse, PaginationResponse } from '@/utils/request';
import { UserInfo } from './auth';

// 关注统计
export interface FollowStats {
  following_count: number;
  followers_count: number;
  friends_count: number;
}

/**
 * 关注用户
 */
export function followUser(userId: number): Promise<ApiResponse<void>> {
  return request.post(`/users/${userId}/follow`);
}

/**
 * 取消关注
 */
export function unfollowUser(userId: number): Promise<ApiResponse<void>> {
  return request.delete(`/users/${userId}/follow`);
}

/**
 * 检查关注状态
 */
export function checkFollowStatus(userId: number): Promise<ApiResponse<{ following: boolean }>> {
  return request.get(`/users/${userId}/follow/status`);
}

/**
 * 获取关注统计
 */
export function getFollowStats(userId?: number): Promise<ApiResponse<FollowStats>> {
  const url = userId ? `/users/${userId}/follow/stats` : '/user/follow/stats';
  return request.get(url);
}

/**
 * 获取关注列表
 */
export function getFollowingList(
  userId?: number,
  params?: { page?: number; size?: number }
): Promise<ApiResponse<PaginationResponse<UserInfo>>> {
  const url = userId ? `/users/${userId}/following` : '/user/following';
  return request.get(url, { params });
}

/**
 * 获取粉丝列表
 */
export function getFollowersList(
  userId?: number,
  params?: { page?: number; size?: number }
): Promise<ApiResponse<PaginationResponse<UserInfo>>> {
  const url = userId ? `/users/${userId}/followers` : '/user/followers';
  return request.get(url, { params });
}

/**
 * 获取好友列表（互关）
 */
export function getFriendsList(params?: { page?: number; size?: number }): Promise<ApiResponse<PaginationResponse<UserInfo>>> {
  return request.get('/user/friends', { params });
}
