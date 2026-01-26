<template>
  <header class="app-header">
    <div class="container">
      <div class="logo">
        <router-link to="/">Personal Blog</router-link>
      </div>

      <!-- Mobile menu button -->
      <button class="mobile-menu-btn" @click="toggleMobileMenu">
        <el-icon :size="24"><Menu /></el-icon>
      </button>

      <!-- Navigation -->
      <nav class="nav" :class="{ 'mobile-open': mobileMenuOpen }">
        <router-link to="/" @click="closeMobileMenu">Home</router-link>
        <router-link to="/tech" @click="closeMobileMenu">Tech</router-link>
        <router-link to="/life" @click="closeMobileMenu">Life</router-link>
        <router-link to="/skills" @click="closeMobileMenu">Skills</router-link>
        <router-link to="/projects" @click="closeMobileMenu">Projects</router-link>
        <router-link to="/about" @click="closeMobileMenu">About</router-link>
      </nav>

      <!-- Actions -->
      <div class="actions" :class="{ 'mobile-open': mobileMenuOpen }">
        <template v-if="isAuthenticated">
          <router-link to="/admin" @click="closeMobileMenu">Dashboard</router-link>
          <el-button @click="handleLogout" size="small">Logout</el-button>
        </template>
        <template v-else>
          <router-link to="/login" @click="closeMobileMenu">
            <el-button type="primary" size="small">Login</el-button>
          </router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Menu } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const isAuthenticated = computed(() => userStore.isAuthenticated)
const mobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const handleLogout = async () => {
  await userStore.logout()
  closeMobileMenu()
  router.push('/login')
}
</script>

<style scoped>
.app-header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.logo a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #409eff;
  text-decoration: none;
  white-space: nowrap;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: #606266;
}

.nav {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav a {
  color: #606266;
  text-decoration: none;
  transition: color 0.3s;
  white-space: nowrap;
}

.nav a:hover,
.nav a.router-link-active {
  color: #409eff;
}

.actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.actions a {
  text-decoration: none;
}

/* Tablet and below */
@media (max-width: 1024px) {
  .nav {
    gap: 1.5rem;
  }

  .nav a {
    font-size: 0.9rem;
  }
}

/* Mobile */
@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block;
  }

  .nav {
    position: fixed;
    top: 65px;
    left: 0;
    right: 0;
    background: #fff;
    flex-direction: column;
    gap: 0;
    padding: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: transform 0.3s, opacity 0.3s, visibility 0.3s;
  }

  .nav.mobile-open {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }

  .nav a {
    padding: 1rem 1.5rem;
    width: 100%;
    display: block;
    border-bottom: 1px solid #ebeef5;
  }

  .nav a:last-child {
    border-bottom: none;
  }

  .actions {
    position: fixed;
    top: calc(65px + 6 * 49px);
    left: 0;
    right: 0;
    background: #fff;
    padding: 1rem 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: transform 0.3s, opacity 0.3s, visibility 0.3s;
    flex-direction: column;
    align-items: stretch;
  }

  .actions.mobile-open {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }

  .actions a {
    width: 100%;
  }

  .actions .el-button {
    width: 100%;
  }
}

/* Small mobile */
@media (max-width: 480px) {
  .logo a {
    font-size: 1.25rem;
  }
}
</style>

