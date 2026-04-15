<template>
  <footer class="app-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <span class="brand-logo">X</span>
          <span class="brand-name">LJ's Blog</span>
        </div>
        <div class="footer-links">
          <router-link to="/tech">技术</router-link>
          <router-link to="/projects">项目</router-link>
          <router-link to="/archives">归档</router-link>
          <router-link to="/about">关于</router-link>
        </div>
      </div>
      <div class="footer-divider"></div>
      <div class="footer-bottom">
        <p class="copyright">&copy; {{ currentYear }} XLJ. Built with Vue 3 + FastAPI + MongoDB</p>
        <p class="powered">Powered with &#9829;</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<style scoped>
.app-footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--card-border);
  padding: 2.5rem 0 1.5rem;
  margin-top: auto;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.footer-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.brand-logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: var(--accent-gradient);
  color: #fff;
  font-weight: 800;
  font-size: 0.85rem;
}

.brand-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.footer-links {
  display: flex;
  gap: 1.5rem;
}

.footer-links a {
  color: var(--text-tertiary);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  transition: color 0.2s;
}

.footer-links a:hover {
  color: var(--accent-primary);
}

.footer-divider {
  height: 1px;
  background: var(--card-border);
  margin: 1.5rem 0;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.copyright {
  margin: 0;
  font-size: 0.8rem;
  color: var(--text-disabled);
}

.powered {
  margin: 0;
  font-size: 0.8rem;
  color: var(--text-disabled);
}

@media (max-width: 768px) {
  .footer-top { flex-direction: column; gap: 1rem; }
  .footer-bottom { flex-direction: column; gap: 0.5rem; text-align: center; }
}
</style>
