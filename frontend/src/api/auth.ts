/**
 * Authentication API
 */
import request from '@/utils/request'
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '@/types/user'
import type { ApiResponse } from '@/types/common'

/**
 * User login
 */
export function login(data: LoginRequest): Promise<ApiResponse<TokenResponse> | TokenResponse> {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

/**
 * User registration (admin only)
 */
export function register(data: RegisterRequest): Promise<ApiResponse<User> | User> {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

/**
 * Refresh access token
 */
export function refreshToken(): Promise<ApiResponse<TokenResponse> | TokenResponse> {
  return request({
    url: '/auth/refresh',
    method: 'post'
  })
}

/**
 * Get current user info
 */
export function getCurrentUser(): Promise<ApiResponse<User> | User> {
  return request({
    url: '/auth/me',
    method: 'get'
  })
}
