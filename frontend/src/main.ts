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

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(ElementPlus)

// 初始化性能监控
initPerformanceMonitoring()

app.mount('#app')
