/**
 * 用户认证相关 API
 */
import request, { ApiResponse } from '@/utils/request';

// 用户信息接口
export interface UserInfo {
  id: number;
  username: string;
  nickname?: string;
  email?: string;
  avatar?: string;
  bio?: string;
  created_at: string;
}

// 登录请求参数
export interface LoginParams {
  username: string;
  password: string;
}

// 注册请求参数
export interface RegisterParams {
  username: string;
  password: string;
  email?: string;
  nickname?: string;
}

// 登录响应
export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: UserInfo;
}

/**
 * 用户注册
 */
export function register(data: RegisterParams): Promise<ApiResponse<UserInfo>> {
  return request.post('/auth/register', data);
}

/**
 * 用户登录
 */
export function login(data: LoginParams): Promise<ApiResponse<LoginResponse>> {
  return request.post('/auth/login', data);
}

/**
 * 刷新 Token
 */
export function refreshToken(): Promise<ApiResponse<{ access_token: string; token_type: string }>> {
  return request.post('/auth/refresh');
}

/**
 * 获取当前用户信息
 */
export function getCurrentUser(): Promise<ApiResponse<UserInfo>> {
  return request.get('/auth/me');
}
