/**
 * HTTP 请求封装
 */
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { API_BASE_URL, REQUEST_TIMEOUT, STORAGE_KEYS } from './constants';
import { getStorageSync, showLoading, hideLoading, showToast } from './platform';

// 响应数据接口
export interface ApiResponse<T = any> {
  code: number;
  status: boolean;
  msg: string;
  data: T;
}

// 分页响应接口
export interface PaginationResponse<T = any> {
  list: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// 创建 axios 实例
const service: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 添加 token 到请求头
    const token = getStorageSync(STORAGE_KEYS.TOKEN);
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // 显示加载提示（多端兼容）
    showLoading({ title: '加载中...', mask: true });

    return config;
  },
  (error: AxiosError) => {
    hideLoading();
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    hideLoading();

    const res = response.data;

    // 如果响应成功（code为200），直接返回
    if (res.code === 200 && res.status === true) {
      return res;
    }

    // 如果响应成功但code不是200，显示错误信息
    showToast({
      title: res.msg || '请求失败',
      icon: 'none',
      duration: 2000,
    });

    return Promise.reject(new Error(res.msg || '请求失败'));
  },
  (error: AxiosError<ApiResponse>) => {
    hideLoading();

    console.error('响应错误:', error);

    // 处理不同的错误状态码
    const status = error.response?.status;
    const message = error.response?.data?.msg || error.message;

    let toastMessage = '';

    switch (status) {
      case 400:
        toastMessage = message || '请求参数错误';
        break;
      case 401:
        toastMessage = '登录已过期，请重新登录';
        // 清除 token 并跳转到登录页（小程序环境）
        if (typeof uni !== 'undefined') {
          uni.removeStorageSync(STORAGE_KEYS.TOKEN);
          uni.removeStorageSync(STORAGE_KEYS.USER_INFO);
          setTimeout(() => {
            uni.reLaunch({
              url: '/login',
            });
          }, 1500);
        }
        break;
      case 403:
        toastMessage = '没有权限访问';
        break;
      case 404:
        toastMessage = '请求的资源不存在';
        break;
      case 500:
        toastMessage = '服务器错误';
        break;
      default:
        toastMessage = message || '网络请求失败';
    }

    showToast({
      title: toastMessage,
      icon: 'none',
      duration: 2000,
    });

    return Promise.reject(error);
  }
);

// 请求方法封装
export const request = {
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return service.get(url, config);
  },

  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return service.post(url, data, config);
  },

  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return service.put(url, data, config);
  },

  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return service.delete(url, config);
  },

  patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return service.patch(url, data, config);
  },
};

export default request;
