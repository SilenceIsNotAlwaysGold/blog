<template>
  <footer class="app-footer">
    <div class="container">
      <p>&copy; 2024 Personal Blog. All rights reserved.</p>
      <p>Built with Vue 3 + FastAPI</p>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Footer component
</script>

<style scoped>
.app-footer {
  background: #f5f5f5;
  padding: 2rem 0;
  margin-top: 4rem;
  text-align: center;
  color: #909399;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.app-footer p {
  margin: 0.5rem 0;
}
</style>
