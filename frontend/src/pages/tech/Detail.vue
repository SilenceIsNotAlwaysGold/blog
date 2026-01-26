<template>
  <div class="tech-detail">
    <h1>Tech Article Detail</h1>
    <p>Article ID: {{ route.params.id }}</p>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style scoped>
.tech-detail {
  padding: 2rem;
}
</style>
