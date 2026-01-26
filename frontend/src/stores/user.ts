/**
 * User Pinia store
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, TokenResponse } from '@/types/user'

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

  async function login(_username: string, _password: string): Promise<TokenResponse> {
    // This will be implemented when auth API is ready
    // For now, just a placeholder
    throw new Error('Not implemented')
  }

  async function logout() {
    clearAuth()
  }

  async function fetchUserInfo(): Promise<User> {
    // This will be implemented when auth API is ready
    // For now, just a placeholder
    throw new Error('Not implemented')
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
    fetchUserInfo
  }
})
