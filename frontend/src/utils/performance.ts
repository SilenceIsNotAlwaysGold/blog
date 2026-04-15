/**
 * 性能监控工具
 */

export interface PerformanceMetrics {
  // 页面加载性能
  domContentLoaded: number
  loadComplete: number
  firstPaint: number
  firstContentfulPaint: number

  // 资源加载
  resourceCount: number
  totalResourceSize: number

  // 内存使用（如果可用）
  memoryUsed?: number
  memoryLimit?: number
}

/**
 * 获取性能指标
 */
export function getPerformanceMetrics(): PerformanceMetrics | null {
  if (!window.performance) {
    console.warn('Performance API not supported')
    return null
  }

  const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming
  const paint = performance.getEntriesByType('paint')

  const metrics: PerformanceMetrics = {
    domContentLoaded: navigation?.domContentLoadedEventEnd - navigation?.domContentLoadedEventStart || 0,
    loadComplete: navigation?.loadEventEnd - navigation?.loadEventStart || 0,
    firstPaint: 0,
    firstContentfulPaint: 0,
    resourceCount: 0,
    totalResourceSize: 0
  }

  // 获取绘制时间
  paint.forEach((entry) => {
    if (entry.name === 'first-paint') {
      metrics.firstPaint = entry.startTime
    } else if (entry.name === 'first-contentful-paint') {
      metrics.firstContentfulPaint = entry.startTime
    }
  })

  // 获取资源信息
  const resources = performance.getEntriesByType('resource') as PerformanceResourceTiming[]
  metrics.resourceCount = resources.length
  metrics.totalResourceSize = resources.reduce((sum, resource) => {
    return sum + (resource.transferSize || 0)
  }, 0)

  // 获取内存信息（如果可用）
  if ('memory' in performance) {
    const memory = (performance as any).memory
    metrics.memoryUsed = memory.usedJSHeapSize
    metrics.memoryLimit = memory.jsHeapSizeLimit
  }

  return metrics
}

/**
 * 格式化字节大小
 */
export function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

/**
 * 输出性能报告到控制台
 */
export function logPerformanceReport(): void {
  const metrics = getPerformanceMetrics()

  if (!metrics) {
    return
  }

  console.group('📊 性能报告')
  console.log(`⏱️  DOM 加载: ${Math.round(metrics.domContentLoaded)}ms`)
  console.log(`⏱️  页面完全加载: ${Math.round(metrics.loadComplete)}ms`)
  console.log(`🎨 首次绘制: ${Math.round(metrics.firstPaint)}ms`)
  console.log(`🎨 首次内容绘制: ${Math.round(metrics.firstContentfulPaint)}ms`)
  console.log(`📦 资源数量: ${metrics.resourceCount}`)
  console.log(`📦 资源总大小: ${formatBytes(metrics.totalResourceSize)}`)

  if (metrics.memoryUsed && metrics.memoryLimit) {
    const memoryPercent = (metrics.memoryUsed / metrics.memoryLimit * 100).toFixed(1)
    console.log(`💾 内存使用: ${formatBytes(metrics.memoryUsed)} / ${formatBytes(metrics.memoryLimit)} (${memoryPercent}%)`)
  }

  console.groupEnd()
}

/**
 * 在页面加载完成后自动输出性能报告
 */
export function initPerformanceMonitoring(): void {
  if (typeof window === 'undefined') {
    return
  }

  window.addEventListener('load', () => {
    // 延迟一点时间确保所有指标都已记录
    setTimeout(() => {
      logPerformanceReport()
    }, 100)
  })
}
