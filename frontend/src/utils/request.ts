/**
 * Axios request utility with interceptors
 */
import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'
import { ElMessage } from 'element-plus'

// Create axios instance
const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Add token to headers if exists
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const res = response.data

    // If response has standard format {code, message, data}
    if (res.code !== undefined) {
      if (res.code === 200 || res.code === 201) {
        return res
      } else {
        ElMessage.error(res.message || 'Request failed')
        return Promise.reject(new Error(res.message || 'Request failed'))
      }
    }

    // Return raw response if not standard format
    return response.data
  },
  (error: AxiosError) => {
    console.error('Response error:', error)

    if (error.response) {
      const status = error.response.status
      const data: any = error.response.data

      switch (status) {
        case 401:
          ElMessage.error('Unauthorized, please login')
          // Clear token and redirect to login
          localStorage.removeItem('access_token')
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('Forbidden')
          break
        case 404:
          ElMessage.error('Resource not found')
          break
        case 500:
          ElMessage.error('Server error')
          break
        default:
          ElMessage.error(data?.message || 'Request failed')
      }
    } else if (error.request) {
      ElMessage.error('Network error, please check your connection')
    } else {
      ElMessage.error('Request failed')
    }

    return Promise.reject(error)
  }
)

export default request
