<template>
  <div class="dashboard">
    <h1>Admin Dashboard</h1>
    <p>Welcome, {{ userStore.userInfo?.username }}!</p>
    <p>Admin panel will be implemented here.</p>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}
</style>
