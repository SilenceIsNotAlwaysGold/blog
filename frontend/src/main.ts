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

// 初始化性能监控
initPerformanceMonitoring()

app.mount('#app')
