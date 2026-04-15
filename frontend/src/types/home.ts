/**
 * 首页相关类型定义
 */

// 主题类型
export type Theme = 'light' | 'dark'

// 设备类型
export interface DeviceInfo {
  isMobile: boolean
  isTablet: boolean
  isDesktop: boolean
}

// 导航按钮配置
export interface NavigationButton {
  label: string
  route: string
  icon?: string
  color: string
}

// 粒子配置
export interface ParticleConfig {
  count: number
  color: string
  opacity: number
  size: number
  speed: number
}

// 欢迎标语
export interface WelcomeContent {
  mainTitle: string
  subTitle: string
}
