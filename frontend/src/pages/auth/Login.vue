<template>
  <div class="login-page">
    <div class="login-bg">
      <div class="bg-grid"></div>
      <div class="bg-glow"></div>
    </div>

    <div class="login-container">
      <!-- Brand -->
      <router-link to="/" class="brand">
        <span class="brand-icon">X</span>
        <span class="brand-name">LJ's Blog</span>
      </router-link>

      <!-- Login Card -->
      <div class="login-card">
        <h2 class="login-title">登录</h2>
        <p class="login-desc">登录以管理博客内容</p>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-field">
            <label class="field-label">用户名</label>
            <div class="field-input-wrap">
              <input
                v-model="loginForm.username"
                type="text"
                placeholder="请输入用户名"
                class="field-input"
                autocomplete="username"
              />
            </div>
          </div>

          <div class="form-field">
            <label class="field-label">密码</label>
            <div class="field-input-wrap">
              <input
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请输入密码"
                class="field-input"
                autocomplete="current-password"
                @keyup.enter="handleLogin"
              />
              <button type="button" class="toggle-pwd" @click="showPassword = !showPassword">
                {{ showPassword ? '隐藏' : '显示' }}
              </button>
            </div>
          </div>

          <button type="submit" class="login-btn" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? '登录中...' : '登 录' }}
          </button>
        </form>
      </div>

      <router-link to="/" class="back-link">← 返回首页</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const showPassword = ref(false)

const loginForm = reactive({ username: '', password: '' })

const handleLogin = async () => {
  if (!loginForm.username.trim() || !loginForm.password.trim()) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true
  try {
    await userStore.login(loginForm.username, loginForm.password)
    ElMessage.success('登录成功')
    const redirect = router.currentRoute.value.query.redirect as string
    router.push(redirect || '/admin/dashboard')
  } catch (error: any) {
    ElMessage.error(error.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary, #0a0e17);
  position: relative;
  overflow: hidden;
}

.login-bg {
  position: absolute;
  inset: 0;
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 60px 60px;
}

.bg-glow {
  position: absolute;
  top: 30%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(129, 140, 248, 0.15) 0%, transparent 70%);
  filter: blur(60px);
}

.login-container {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 400px;
  padding: 2rem;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  margin-bottom: 2rem;
}

.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--accent-gradient, linear-gradient(135deg, #818cf8, #c084fc));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 800;
  font-size: 1.1rem;
}

.brand-name {
  font-size: 1.3rem;
  font-weight: 700;
  background: var(--accent-gradient, linear-gradient(135deg, #818cf8, #c084fc));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Card */
.login-card {
  width: 100%;
  padding: 2rem;
  background: var(--card-bg, rgba(255,255,255,0.03));
  border: 1px solid var(--card-border, rgba(255,255,255,0.08));
  border-radius: 16px;
  backdrop-filter: blur(20px);
}

.login-title {
  margin: 0 0 0.3rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary, #fff);
}

.login-desc {
  margin: 0 0 1.5rem;
  font-size: 0.85rem;
  color: var(--text-tertiary, rgba(255,255,255,0.5));
}

/* Form */
.login-form { display: flex; flex-direction: column; gap: 1.25rem; }

.form-field {}

.field-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary, rgba(255,255,255,0.7));
  margin-bottom: 0.4rem;
}

.field-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.field-input {
  width: 100%;
  padding: 0.7rem 1rem;
  background: var(--bg-secondary, rgba(255,255,255,0.05));
  border: 1px solid var(--border-color, rgba(255,255,255,0.1));
  border-radius: 10px;
  color: var(--text-primary, #fff);
  font-size: 0.9rem;
  outline: none;
  transition: all 0.2s;
}

.field-input::placeholder { color: var(--text-disabled, rgba(255,255,255,0.3)); }

.field-input:focus {
  border-color: var(--accent-primary, #818cf8);
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.15);
}

.toggle-pwd {
  position: absolute;
  right: 0.75rem;
  background: none;
  border: none;
  color: var(--text-disabled, rgba(255,255,255,0.4));
  font-size: 0.75rem;
  cursor: pointer;
  padding: 0.2rem 0.4rem;
  transition: color 0.2s;
}

.toggle-pwd:hover { color: var(--text-secondary); }

/* Button */
.login-btn {
  width: 100%;
  padding: 0.75rem;
  background: var(--accent-gradient, linear-gradient(135deg, #818cf8, #c084fc));
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.login-btn:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
.login-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Back */
.back-link {
  margin-top: 1.5rem;
  color: var(--text-disabled, rgba(255,255,255,0.4));
  text-decoration: none;
  font-size: 0.82rem;
  transition: color 0.2s;
}

.back-link:hover { color: var(--accent-primary, #818cf8); }

/* Mobile */
@media (max-width: 480px) {
  .login-container { padding: 1rem; }
  .login-card { padding: 1.5rem; }
}
</style>
