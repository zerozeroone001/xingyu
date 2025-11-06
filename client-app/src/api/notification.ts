/**
 * 消息通知相关 API
 */
import request, { ApiResponse, PaginationResponse } from '@/utils/request';

// 消息类型
export enum NotificationType {
  SYSTEM = 'system',
  LIKE = 'like',
  COMMENT = 'comment',
  FOLLOW = 'follow',
  COLLECT = 'collect',
}

// 消息状态
export enum NotificationStatus {
  UNREAD = 'unread',
  READ = 'read',
}

// 通知接口
export interface Notification {
  id: number;
  user_id: number;
  type: NotificationType;
  title: string;
  content: string;
  link?: string;
  status: NotificationStatus;
  created_at: string;
}

// 消息列表查询参数
export interface NotificationListParams {
  page?: number;
  size?: number;
  type?: NotificationType;
  status?: NotificationStatus;
}

// 未读消息统计
export interface UnreadStats {
  total: number;
  system: number;
  like: number;
  comment: number;
  follow: number;
  collect: number;
}

/**
 * 获取消息列表
 */
export function getNotificationList(params?: NotificationListParams): Promise<ApiResponse<PaginationResponse<Notification>>> {
  return request.get('/notifications', { params });
}

/**
 * 获取未读消息统计
 */
export function getUnreadStats(): Promise<ApiResponse<UnreadStats>> {
  return request.get('/notifications/unread/stats');
}

/**
 * 标记单条消息为已读
 */
export function markAsRead(id: number): Promise<ApiResponse<void>> {
  return request.put(`/notifications/${id}/read`);
}

/**
 * 批量标记消息为已读
 */
export function markAllAsRead(type?: NotificationType): Promise<ApiResponse<void>> {
  return request.put('/notifications/read/all', { type });
}

/**
 * 删除消息
 */
export function deleteNotification(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/notifications/${id}`);
}

/**
 * 批量删除消息
 */
export function deleteAllNotifications(type?: NotificationType): Promise<ApiResponse<void>> {
  return request.delete('/notifications/all', { params: { type } });
}
