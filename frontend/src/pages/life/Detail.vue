<template>
  <div class="life-detail">
    <h1>Life Article Detail</h1>
    <p>Article ID: {{ route.params.id }}</p>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style scoped>
.life-detail {
  padding: 2rem;
}
</style>
