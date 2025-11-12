import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getUserInfo } from '@/api/user'
import { loginByPassword, loginByWeChat, logout as apiLogout } from '@/api/auth'

/**
 * 用户 Store
 * 管理用户信息和登录状态
 */
export const useUserStore = defineStore('user', () => {
  // 用户信息
  const userInfo = ref(null)

  // Token
  const token = ref('')

  // 是否已登录
  const isLogin = computed(() => !!token.value && !!userInfo.value)

  /**
   * 检查登录状态
   * 从本地存储读取 token 和用户信息
   */
  const checkLogin = async () => {
    try {
      const savedToken = uni.getStorageSync('token')
      const savedUser = uni.getStorageSync('user')

      if (savedToken && savedUser) {
        token.value = savedToken
        userInfo.value = JSON.parse(savedUser)

        // 验证 token 是否有效，获取最新用户信息
        try {
          const freshUserInfo = await getUserInfo()
          userInfo.value = freshUserInfo
          uni.setStorageSync('user', JSON.stringify(freshUserInfo))
        } catch (e) {
          // Token 失效，清除登录状态
          clearLogin()
        }
      }
    } catch (e) {
      console.error('检查登录状态失败:', e)
    }
  }

  /**
   * 账号密码登录
   * @param {string} username - 用户名
   * @param {string} password - 密码
   * @returns {Promise} 登录结果
   */
  const login = async (username, password) => {
    try {
      const data = await loginByPassword(username, password)

      // 保存 token 和用户信息
      token.value = data.access_token
      userInfo.value = data.user

      uni.setStorageSync('token', data.access_token)
      uni.setStorageSync('user', JSON.stringify(data.user))

      uni.showToast({
        title: '登录成功',
        icon: 'success'
      })

      return data
    } catch (e) {
      console.error('登录失败:', e)
      throw e
    }
  }

  /**
   * 微信登录
   * @returns {Promise} 登录结果
   */
  const wechatLogin = async () => {
    try {
      // 获取微信登录code
      const { code } = await new Promise((resolve, reject) => {
        uni.login({
          provider: 'weixin',
          success: resolve,
          fail: reject
        })
      })

      // 调用后端登录接口
      const data = await loginByWeChat(code)

      // 保存 token 和用户信息
      token.value = data.access_token
      userInfo.value = data.user

      uni.setStorageSync('token', data.access_token)
      uni.setStorageSync('user', JSON.stringify(data.user))

      uni.showToast({
        title: '登录成功',
        icon: 'success'
      })

      return data
    } catch (e) {
      console.error('微信登录失败:', e)
      throw e
    }
  }

  /**
   * 登出
   */
  const logout = async () => {
    try {
      // 调用后端登出接口
      await apiLogout()
    } catch (e) {
      console.error('登出失败:', e)
    } finally {
      // 清除本地登录状态
      clearLogin()

      uni.showToast({
        title: '已退出登录',
        icon: 'success'
      })

      // 跳转到登录页
      setTimeout(() => {
        uni.reLaunch({
          url: '/pages/login/index'
        })
      }, 1000)
    }
  }

  /**
   * 清除登录状态
   */
  const clearLogin = () => {
    token.value = ''
    userInfo.value = null
    uni.removeStorageSync('token')
    uni.removeStorageSync('user')
  }

  /**
   * 更新用户信息
   * @param {Object} data - 用户信息
   */
  const updateUserInfo = (data) => {
    userInfo.value = { ...userInfo.value, ...data }
    uni.setStorageSync('user', JSON.stringify(userInfo.value))
  }

  return {
    userInfo,
    token,
    isLogin,
    checkLogin,
    login,
    wechatLogin,
    logout,
    updateUserInfo
  }
})
