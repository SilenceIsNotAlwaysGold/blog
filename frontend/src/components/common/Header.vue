<template>
  <header class="app-header" :class="{ scrolled: isScrolled }">
    <div class="container">
      <div class="logo">
        <router-link to="/">
          <span class="logo-icon">X</span>
          <span class="logo-text">LJ's Blog</span>
        </router-link>
      </div>

      <!-- Mobile menu button -->
      <button class="mobile-menu-btn" @click="toggleMobileMenu">
        <span class="hamburger" :class="{ active: mobileMenuOpen }">
          <span></span><span></span><span></span>
        </span>
      </button>

      <!-- Navigation -->
      <nav class="nav" :class="{ 'mobile-open': mobileMenuOpen }">
        <router-link to="/" @click="closeMobileMenu">
          <span class="nav-icon">~</span> 首页
        </router-link>
        <router-link to="/tech" @click="closeMobileMenu">
          <span class="nav-icon">/</span> 技术
        </router-link>
        <router-link to="/projects" @click="closeMobileMenu">
          <span class="nav-icon">#</span> 项目
        </router-link>
        <router-link to="/archives" @click="closeMobileMenu">
          <span class="nav-icon">@</span> 归档
        </router-link>
        <router-link to="/about" @click="closeMobileMenu">
          <span class="nav-icon">&</span> 关于
        </router-link>
      </nav>

      <!-- Actions -->
      <div class="actions" :class="{ 'mobile-open': mobileMenuOpen }">
        <button class="theme-toggle" @click="toggleTheme" :title="isDark ? '切换亮色' : '切换暗色'">
          <transition name="rotate" mode="out-in">
            <el-icon :size="18" :key="isDark ? 'sun' : 'moon'">
              <Sunny v-if="isDark" />
              <Moon v-else />
            </el-icon>
          </transition>
        </button>

        <el-dropdown v-if="isAdmin" trigger="click" @command="handleAdminCommand">
          <button class="admin-btn" title="管理">
            <el-icon :size="18"><Setting /></el-icon>
          </button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="dashboard"><el-icon><DataBoard /></el-icon> 管理中心</el-dropdown-item>
              <el-dropdown-item command="new-article" divided><el-icon><Document /></el-icon> 新建文章</el-dropdown-item>
              <el-dropdown-item command="new-project"><el-icon><Plus /></el-icon> 新建项目</el-dropdown-item>
              <el-dropdown-item command="new-skill"><el-icon><Plus /></el-icon> 新建技能</el-dropdown-item>
              <el-dropdown-item command="edit-about" divided><el-icon><Edit /></el-icon> 编辑关于</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <template v-if="isAuthenticated">
          <button class="action-btn logout" @click="handleLogout">退出</button>
        </template>
        <template v-else>
          <router-link to="/login" @click="closeMobileMenu">
            <button class="action-btn login">登录</button>
          </router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Sunny, Moon, Setting, Plus, Edit, Document, DataBoard } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const isAuthenticated = computed(() => userStore.isAuthenticated)
const isAdmin = computed(() => userStore.isAdmin)
const mobileMenuOpen = ref(false)
const isDark = ref(false)
const isScrolled = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  isDark.value = savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)
  applyTheme()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const toggleTheme = () => {
  isDark.value = !isDark.value
  applyTheme()
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

const applyTheme = () => {
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
}

const toggleMobileMenu = () => { mobileMenuOpen.value = !mobileMenuOpen.value }
const closeMobileMenu = () => { mobileMenuOpen.value = false }

const handleLogout = async () => {
  await userStore.logout()
  closeMobileMenu()
  router.push('/login')
}

const handleAdminCommand = (command: string) => {
  closeMobileMenu()
  const routes: Record<string, string> = {
    dashboard: '/admin/dashboard',
    'new-article': '/admin/article/new',
    'new-project': '/admin/project/new',
    'new-skill': '/admin/skill/new',
    'edit-about': '/admin/about/edit'
  }
  if (routes[command]) router.push(routes[command])
}
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--glass-bg);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--glass-border);
  padding: 0.75rem 0;
  transition: all 0.3s ease;
}

.app-header.scrolled {
  box-shadow: var(--shadow-md);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo */
.logo a {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  white-space: nowrap;
}

.logo-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--accent-gradient);
  color: #fff;
  font-weight: 800;
  font-size: 1rem;
  letter-spacing: -1px;
}

.logo-text {
  font-size: 1.2rem;
  font-weight: 700;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Navigation */
.nav {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.nav a {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  padding: 0.5rem 0.9rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.nav-icon {
  font-family: 'Consolas', monospace;
  font-weight: 400;
  opacity: 0.5;
  font-size: 0.85rem;
}

.nav a:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.nav a.router-link-exact-active,
.nav a.router-link-active[href="/tech"],
.nav a.router-link-active[href="/projects"],
.nav a.router-link-active[href="/archives"],
.nav a.router-link-active[href="/about"] {
  color: var(--accent-primary);
  background: rgba(129, 140, 248, 0.1);
}

/* Actions */
.actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.theme-toggle,
.admin-btn {
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--text-secondary);
  transition: all 0.2s ease;
}

.theme-toggle:hover,
.admin-btn:hover {
  color: var(--accent-primary);
  border-color: var(--accent-primary);
  background: rgba(129, 140, 248, 0.08);
}

.action-btn {
  padding: 0.4rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.action-btn.login {
  background: var(--accent-gradient);
  color: #fff;
}

.action-btn.login:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.action-btn.logout {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.action-btn.logout:hover {
  color: var(--danger-color);
  border-color: var(--danger-color);
}

/* Rotate transition */
.rotate-enter-active,
.rotate-leave-active {
  transition: all 0.3s ease;
}
.rotate-enter-from { transform: rotate(-90deg); opacity: 0; }
.rotate-leave-to { transform: rotate(90deg); opacity: 0; }

/* Hamburger */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.hamburger {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 22px;
}

.hamburger span {
  display: block;
  height: 2px;
  background: var(--text-secondary);
  border-radius: 1px;
  transition: all 0.3s ease;
}

.hamburger.active span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
.hamburger.active span:nth-child(2) { opacity: 0; }
.hamburger.active span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

/* Mobile */
@media (max-width: 768px) {
  .container { padding: 0 1rem; }
  .mobile-menu-btn { display: block; }

  .nav {
    position: fixed;
    top: 57px;
    left: 0;
    right: 0;
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    flex-direction: column;
    padding: 0.5rem;
    gap: 0;
    border-bottom: 1px solid var(--glass-border);
    transform: translateY(-120%);
    opacity: 0;
    transition: all 0.3s ease;
  }

  .nav.mobile-open {
    transform: translateY(0);
    opacity: 1;
  }

  .nav a {
    padding: 0.85rem 1rem;
    width: 100%;
    border-radius: 8px;
  }

  .actions {
    position: fixed;
    top: calc(57px + 5 * 44px + 1rem);
    left: 0;
    right: 0;
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    padding: 1rem;
    border-bottom: 1px solid var(--glass-border);
    transform: translateY(-120%);
    opacity: 0;
    transition: all 0.3s ease;
    justify-content: center;
  }

  .actions.mobile-open {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
