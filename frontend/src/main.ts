import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './styles/global.css'
import './styles/theme.css'
import './styles/responsive.css'
import App from './App.vue'
import router from './router'
import { initPerformanceMonitoring } from './utils/performance'
import Particles from '@tsparticles/vue3'
import { loadSlim } from '@tsparticles/slim'
import { vTilt } from './directives/tilt'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.use(Particles, {
  init: async (engine: any) => {
    await loadSlim(engine)
  },
})
app.directive('tilt', vTilt)

// 初始化性能监控
initPerformanceMonitoring()

// 启动时若已有 token，恢复用户信息（保证 isAdmin 等响应式状态可用）
import { useUserStore } from './stores/user'
const userStore = useUserStore()
if (userStore.token) {
  userStore.fetchUserInfo().catch(() => userStore.clearAuth())
}

app.mount('#app')
