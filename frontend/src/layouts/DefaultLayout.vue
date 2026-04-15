<template>
  <div class="default-layout">
    <Header />
    <main class="main-content">
      <router-view />
    </main>
    <Footer />
    <el-backtop :right="30" :bottom="30" />
  </div>
</template>

<script setup lang="ts">
import Header from '@/components/common/Header.vue'
import Footer from '@/components/common/Footer.vue'
</script>

<style scoped>
.default-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-primary);
}

.main-content {
  flex: 1;
  width: 100%;
}
</style>
