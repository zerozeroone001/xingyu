/**
 * 用户状态管理
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { login as loginApi, register as registerApi, getCurrentUser, type LoginParams, type RegisterParams, type UserInfo } from '@/api/auth';
import { setStorage, getStorage, removeStorage } from '@/utils/storage';
import { STORAGE_KEYS } from '@/utils/constants';

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref<string | null>(getStorage(STORAGE_KEYS.TOKEN));
  const userInfo = ref<UserInfo | null>(getStorage(STORAGE_KEYS.USER_INFO));
  const isLoading = ref(false);

  // 计算属性
  const isLoggedIn = computed(() => !!token.value);
  const userId = computed(() => userInfo.value?.id);
  const username = computed(() => userInfo.value?.username);
  const nickname = computed(() => userInfo.value?.nickname || userInfo.value?.username);
  const avatar = computed(() => userInfo.value?.avatar);

  /**
   * 登录
   */
  const login = async (params: LoginParams) => {
    try {
      isLoading.value = true;

      const response = await loginApi(params);
      const { access_token, user } = response.data;

      // 保存 token 和用户信息
      token.value = access_token;
      userInfo.value = user;
      setStorage(STORAGE_KEYS.TOKEN, access_token);
      setStorage(STORAGE_KEYS.USER_INFO, user);

      uni.showToast({
        title: '登录成功',
        icon: 'success',
        duration: 1500,
      });

      return true;
    } catch (error) {
      console.error('登录失败:', error);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * 注册
   */
  const register = async (params: RegisterParams) => {
    try {
      isLoading.value = true;

      await registerApi(params);

      uni.showToast({
        title: '注册成功，请登录',
        icon: 'success',
        duration: 1500,
      });

      return true;
    } catch (error) {
      console.error('注册失败:', error);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * 退出登录
   */
  const logout = async () => {
    try {
      // 清除本地数据
      token.value = null;
      userInfo.value = null;
      removeStorage(STORAGE_KEYS.TOKEN);
      removeStorage(STORAGE_KEYS.USER_INFO);

      uni.showToast({
        title: '已退出登录',
        icon: 'success',
        duration: 1500,
      });

      // 跳转到登录页
      setTimeout(() => {
        uni.reLaunch({
          url: '/pages/login/login',
        });
      }, 1500);

      return true;
    } catch (error) {
      console.error('退出登录失败:', error);
      return false;
    }
  };

  /**
   * 刷新用户信息
   */
  const refreshUserInfo = async () => {
    try {
      if (!isLoggedIn.value) {
        return false;
      }

      const response = await getCurrentUser();
      userInfo.value = response.data;
      setStorage(STORAGE_KEYS.USER_INFO, response.data);

      return true;
    } catch (error) {
      console.error('刷新用户信息失败:', error);
      return false;
    }
  };

  /**
   * 检查登录状态
   */
  const checkLoginStatus = () => {
    if (!isLoggedIn.value) {
      uni.showModal({
        title: '提示',
        content: '请先登录',
        showCancel: true,
        confirmText: '去登录',
        success: (res) => {
          if (res.confirm) {
            uni.navigateTo({
              url: '/pages/login/login',
            });
          }
        },
      });
      return false;
    }
    return true;
  };

  return {
    // 状态
    token,
    userInfo,
    isLoading,

    // 计算属性
    isLoggedIn,
    userId,
    username,
    nickname,
    avatar,

    // 方法
    login,
    register,
    logout,
    refreshUserInfo,
    checkLoginStatus,
  };
});
