/**
 * User Pinia store
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, TokenResponse } from '@/types/user'
import type { ApiResponse } from '@/types/common'
import * as authApi from '@/api/auth'

/**
 * Type guard to check if response is wrapped in ApiResponse format
 */
function isApiResponse<T>(response: any): response is ApiResponse<T> {
  return response && typeof response === 'object' && 'code' in response && 'data' in response
}

/**
 * Extract data from response, handling both wrapped and unwrapped formats
 */
function extractData<T>(response: ApiResponse<T> | T): T {
  return isApiResponse<T>(response) ? response.data : response
}

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref<string>(localStorage.getItem('access_token') || '')
  const userInfo = ref<User | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')

  // Actions
  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('access_token', newToken)
  }

  function setUserInfo(user: User) {
    userInfo.value = user
  }

  function clearAuth() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('access_token')
  }

  async function login(username: string, password: string): Promise<TokenResponse> {
    const response = await authApi.login({ username, password })
    const tokenData = extractData<TokenResponse>(response)

    // Store token
    setToken(tokenData.access_token)

    // Fetch user info
    await fetchUserInfo()

    return tokenData
  }

  async function logout() {
    clearAuth()
  }

  async function fetchUserInfo(): Promise<User> {
    const response = await authApi.getCurrentUser()
    const user = extractData<User>(response)

    setUserInfo(user)
    return user
  }

  async function refreshToken(): Promise<void> {
    const response = await authApi.refreshToken()
    const tokenData = extractData<TokenResponse>(response)
    setToken(tokenData.access_token)
  }

  return {
    // State
    token,
    userInfo,
    // Getters
    isAuthenticated,
    isAdmin,
    // Actions
    setToken,
    setUserInfo,
    clearAuth,
    login,
    logout,
    fetchUserInfo,
    refreshToken
  }
})
