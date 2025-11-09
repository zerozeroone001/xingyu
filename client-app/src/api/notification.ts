/**
 * 消息通知相关 API
 */
import request, { ApiResponse, PaginationResponse } from '@/utils/request';

// 消息类型
export enum MessageType {
  SYSTEM = 'system',
  LIKE = 'like',
  COMMENT = 'comment',
  FOLLOW = 'follow',
  COLLECT = 'collect',
}

// 消息接口
export interface Message {
  id: number;
  user_id: number;
  type: MessageType;
  title: string;
  content: string;
  link?: string;
  is_read: number; // 0未读 1已读
  created_at: string;
}

// 消息列表查询参数
export interface MessageListParams {
  page?: number;
  page_size?: number;
  type?: string;
  is_read?: number; // 0未读 1已读
}

// 消息统计
export interface MessageStats {
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
export function getMessageList(params?: MessageListParams): Promise<ApiResponse<PaginationResponse<Message>>> {
  return request.get('/messages', { params });
}

/**
 * 获取消息统计
 */
export function getMessageStats(): Promise<ApiResponse<MessageStats>> {
  return request.get('/messages/stats');
}

/**
 * 获取未读消息数
 */
export function getUnreadCount(): Promise<ApiResponse<number>> {
  return request.get('/messages/unread-count');
}

/**
 * 获取未读消息统计（兼容旧接口）
 */
export function getUnreadStats(): Promise<ApiResponse<MessageStats>> {
  return getMessageStats();
}

/**
 * 获取消息详情
 */
export function getMessageDetail(id: number): Promise<ApiResponse<Message>> {
  return request.get(`/messages/${id}`);
}

/**
 * 标记单条消息为已读
 */
export function markAsRead(id: number): Promise<ApiResponse<void>> {
  return request.put(`/messages/${id}/read`);
}

/**
 * 批量标记消息为已读
 */
export function markAllAsRead(type?: string): Promise<ApiResponse<number>> {
  return request.put('/messages/read-all', null, { params: { type } });
}

/**
 * 删除消息
 */
export function deleteMessage(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/messages/${id}`);
}
