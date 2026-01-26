<template>
  <header class="app-header">
    <div class="container">
      <div class="logo">
        <router-link to="/">Personal Blog</router-link>
      </div>
      <nav class="nav">
        <router-link to="/">Home</router-link>
        <router-link to="/tech">Tech</router-link>
        <router-link to="/life">Life</router-link>
        <router-link to="/about">About</router-link>
      </nav>
      <div class="actions">
        <template v-if="isAuthenticated">
          <router-link to="/admin">Dashboard</router-link>
          <el-button @click="handleLogout" size="small">Logout</el-button>
        </template>
        <template v-else>
          <router-link to="/login">
            <el-button type="primary" size="small">Login</el-button>
          </router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElButton } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const isAuthenticated = computed(() => userStore.isAuthenticated)

const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #409eff;
  text-decoration: none;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav a {
  color: #606266;
  text-decoration: none;
  transition: color 0.3s;
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
</style>
