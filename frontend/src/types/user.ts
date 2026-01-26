/**
 * User related type definitions
 */

export interface User {
  id: string
  username: string
  email: string
  role: 'admin' | 'user'
  avatar?: string
  created_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  role?: 'admin' | 'user'
}

export interface TokenResponse {
  access_token: string
  token_type: string
  expires_in: number
}
