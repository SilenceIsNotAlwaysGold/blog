<template>
  <div class="home-page">
    <!-- Hero -->
    <section class="hero">
      <div class="hero-bg">
        <div class="hero-grid"></div>
        <div ref="glowRef" class="hero-glow"></div>
        <!-- Particles -->
        <vue-particles
          id="hero-particles"
          class="hero-particles"
          :options="particlesOptions"
        />
      </div>
      <div class="hero-content">
        <div class="hero-badge">Developer & Creator</div>
        <h1 ref="titleRef" class="hero-title">
          <span v-for="(word, i) in titleWords" :key="i" class="title-word">
            <template v-if="word === '·'">
              <span class="gradient-text">·</span>
            </template>
            <template v-else>{{ word }}</template>
            {{ ' ' }}
          </span>
        </h1>
        <p class="hero-subtitle">
          <span class="typing-text">{{ typedText }}</span>
          <span class="cursor" :class="{ typing: isTyping }">|</span>
        </p>
        <!-- 有数据时才显示统计 -->
        <div v-if="stats.totalArticles > 0" ref="statsRef" class="hero-stats">
          <div class="stat-card">
            <span class="stat-value">{{ stats.totalArticles }}</span>
            <span class="stat-label">篇文章</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ stats.totalViews }}</span>
            <span class="stat-label">次浏览</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ stats.totalLikes }}</span>
            <span class="stat-label">个赞</span>
          </div>
        </div>
        <!-- 没数据时显示快捷入口 -->
        <div v-else class="hero-links">
          <router-link to="/tech" class="hero-link">技术博客</router-link>
          <router-link to="/projects" class="hero-link">项目展示</router-link>
          <router-link to="/about" class="hero-link">关于我</router-link>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="main-container" :class="{ 'has-sidebar': hasSidebarData }">
      <!-- Articles -->
      <div ref="articlesRef" class="content-area">
        <div class="section-header">
          <h2 class="section-title">
            <span class="title-accent"></span>
            最新文章
          </h2>
          <router-link to="/tech" class="view-all">
            全部文章 <span class="arrow">&rarr;</span>
          </router-link>
        </div>

        <div v-if="loadingRecent" class="loading-cards">
          <div v-for="i in 3" :key="i" class="skeleton-card">
            <div class="skeleton-accent shimmer"></div>
            <div class="skeleton-body">
              <div class="skeleton-line w30 shimmer"></div>
              <div class="skeleton-line w80 shimmer"></div>
              <div class="skeleton-line w50 shimmer"></div>
            </div>
          </div>
        </div>

        <template v-else-if="recentArticles.length > 0">
          <div class="articles-grid">
            <article
              v-for="(article, index) in recentArticles"
              :key="article.id"
              class="article-card reveal-card"
              @click="goToArticle(article)"
            >
              <div class="card-accent" :style="{ background: getAccentColor(index) }"></div>
              <div class="card-body">
                <div class="card-meta">
                  <span class="card-date">{{ formatDate(article.created_at) }}</span>
                  <span class="card-board">{{ article.board === 'tech' ? 'Tech' : 'Life' }}</span>
                </div>
                <h3 class="card-title">{{ article.title }}</h3>
                <p v-if="article.summary" class="card-summary">{{ article.summary }}</p>
                <div class="card-footer">
                  <div class="card-tags" v-if="article.tags.length > 0">
                    <span v-for="tag in article.tags.slice(0, 3)" :key="tag" class="mini-tag">{{ tag }}</span>
                  </div>
                  <div class="card-stats">
                    <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
                    <span><el-icon><Star /></el-icon> {{ article.like_count }}</span>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </template>

        <!-- 空状态 -->
        <div v-else class="empty-state">
          <div class="empty-icon">✍️</div>
          <h3 class="empty-title">还没有文章</h3>
          <p class="empty-desc">登录后可以在管理后台创建第一篇文章</p>
        </div>
      </div>

      <!-- Sidebar: 只在有数据时显示 -->
      <aside v-if="hasSidebarData" ref="sidebarRef" class="sidebar">
        <div v-if="popularArticles.length > 0" class="widget reveal-widget">
          <h3 class="widget-title">热门文章</h3>
          <div class="popular-list">
            <div
              v-for="(article, i) in popularArticles"
              :key="article.id"
              class="popular-item"
              @click="goToArticle(article)"
            >
              <span class="popular-rank" :class="['rank-' + (i + 1)]">{{ i + 1 }}</span>
              <div class="popular-info">
                <span class="popular-title">{{ article.title }}</span>
                <span class="popular-views">{{ article.view_count }} 阅读</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="allTags.length > 0" class="widget reveal-widget">
          <h3 class="widget-title">标签</h3>
          <div class="tag-cloud">
            <span
              v-for="tag in allTags"
              :key="tag.name"
              class="tag-pill"
              @click="goToTag(tag.name)"
            >
              {{ tag.name }}
              <span class="tag-count">{{ tag.article_count }}</span>
            </span>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { View, Star } from '@element-plus/icons-vue'
import { getArticles, type Article } from '@/api/article'
import request from '@/utils/request'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const router = useRouter()

// Refs
const glowRef = ref<HTMLElement | null>(null)
const titleRef = ref<HTMLElement | null>(null)
const statsRef = ref<HTMLElement | null>(null)
const articlesRef = ref<HTMLElement | null>(null)
const sidebarRef = ref<HTMLElement | null>(null)

// Title words for word-by-word animation
const titleWords = ['探索', '·', '创造', '·', '分享']

// Typing effect
const fullText = '在代码与生活的交汇处，记录思考的轨迹'
const typedText = ref('')
const isTyping = ref(true)
let typingTimer: ReturnType<typeof setTimeout> | null = null

const startTyping = () => {
  let index = 0
  typedText.value = ''
  isTyping.value = true
  const type = () => {
    if (index < fullText.length) {
      typedText.value += fullText.charAt(index)
      index++
      typingTimer = setTimeout(type, 80)
    } else {
      isTyping.value = false
    }
  }
  type()
}

// Particles config
const particlesOptions = {
  fullScreen: { enable: false },
  fpsLimit: 60,
  particles: {
    number: { value: 50, density: { enable: true, area: 900 } },
    color: { value: ['#818cf8', '#c084fc', '#f472b6', '#38bdf8'] },
    shape: { type: 'circle' },
    opacity: {
      value: { min: 0.1, max: 0.5 },
      animation: { enable: true, speed: 0.8, minimumValue: 0.1 }
    },
    size: {
      value: { min: 1, max: 3 },
      animation: { enable: true, speed: 2, minimumValue: 0.5 }
    },
    move: {
      enable: true,
      speed: 0.6,
      direction: 'none' as const,
      random: true,
      straight: false,
      outModes: { default: 'out' as const }
    },
    links: {
      enable: true,
      distance: 130,
      color: '#818cf8',
      opacity: 0.15,
      width: 1
    }
  },
  interactivity: {
    events: {
      onHover: { enable: true, mode: 'grab' },
      resize: { enable: true }
    },
    modes: {
      grab: { distance: 140, links: { opacity: 0.3 } }
    }
  },
  detectRetina: true
}

// GSAP animations
let gsapCtx: gsap.Context | null = null

const initHeroAnimations = () => {
  if (!titleRef.value) return

  gsapCtx = gsap.context(() => {
    // 1. Title words fade-in stagger
    gsap.from('.title-word', {
      y: 30,
      opacity: 0,
      duration: 0.8,
      stagger: 0.15,
      ease: 'power3.out',
      delay: 0.2,
    })

    // 2. Hero badge
    gsap.from('.hero-badge', {
      y: -20,
      opacity: 0,
      duration: 0.6,
      ease: 'power2.out',
    })

    // 3. Stats cards stagger
    gsap.from('.stat-card', {
      y: 20,
      opacity: 0,
      duration: 0.6,
      stagger: 0.1,
      delay: 1.2,
      ease: 'power2.out',
    })

    // 4. Glow breathing animation
    if (glowRef.value) {
      gsap.to(glowRef.value, {
        scale: 1.15,
        opacity: 0.7,
        duration: 4,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
      })
      gsap.to(glowRef.value, {
        x: 30,
        y: -20,
        duration: 6,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
      })
    }
  }, titleRef.value.parentElement!)
}

const initScrollAnimations = () => {
  if (!articlesRef.value) return

  gsap.context(() => {
    gsap.from('.reveal-card', {
      y: 40,
      opacity: 0,
      duration: 0.6,
      stagger: 0.1,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: '.articles-grid',
        start: 'top 85%',
        once: true,
      },
    })
  }, articlesRef.value)
}

const initSidebarAnimations = () => {
  if (!sidebarRef.value) return

  gsap.context(() => {
    gsap.from('.reveal-widget', {
      x: 30,
      opacity: 0,
      duration: 0.7,
      stagger: 0.2,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: sidebarRef.value!,
        start: 'top 85%',
        once: true,
      },
    })
  }, sidebarRef.value)
}

// Data
const loadingRecent = ref(false)
const loadingPopular = ref(false)
const recentArticles = ref<Article[]>([])
const popularArticles = ref<Article[]>([])
const allTags = ref<{ name: string; article_count: number }[]>([])
const stats = ref({ totalArticles: 0, totalViews: 0, totalLikes: 0 })

const hasSidebarData = computed(() => popularArticles.value.length > 0 || allTags.value.length > 0)

const fetchRecentArticles = async () => {
  loadingRecent.value = true
  try {
    const response = await getArticles({ board: 'tech', is_published: true, page: 1, page_size: 6 })
    recentArticles.value = response.data.items
    stats.value.totalArticles = response.data.pagination.total
    stats.value.totalViews = recentArticles.value.reduce((s, a) => s + a.view_count, 0)
    stats.value.totalLikes = recentArticles.value.reduce((s, a) => s + a.like_count, 0)
    await nextTick()
    initScrollAnimations()
  } catch {
    // silent
  } finally {
    loadingRecent.value = false
  }
}

const fetchPopularArticles = async () => {
  loadingPopular.value = true
  try {
    const response = await getArticles({ board: 'tech', is_published: true, page: 1, page_size: 5 })
    popularArticles.value = [...response.data.items].sort((a, b) => b.view_count - a.view_count).slice(0, 5)
  } catch {
    // silent
  } finally {
    loadingPopular.value = false
  }
}

const fetchTags = async () => {
  try {
    const response: any = await request({ url: '/tags', method: 'get' })
    allTags.value = response.data || []
  } catch {
    // silent
  }
}

// Watch for sidebar data ready
watch(hasSidebarData, (val) => {
  if (val) {
    nextTick(() => initSidebarAnimations())
  }
})

const goToArticle = (article: Article) => router.push(`/tech/${article.id}`)
const goToTag = (tagName: string) => router.push({ path: '/tags', query: { tag: tagName } })

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

const accentColors = [
  'linear-gradient(135deg, #818cf8, #c084fc)',
  'linear-gradient(135deg, #34d399, #06b6d4)',
  'linear-gradient(135deg, #fb923c, #f472b6)',
  'linear-gradient(135deg, #38bdf8, #818cf8)',
  'linear-gradient(135deg, #a78bfa, #f472b6)',
  'linear-gradient(135deg, #fbbf24, #f97316)',
]
const getAccentColor = (index: number) => accentColors[index % accentColors.length]

onMounted(() => {
  fetchRecentArticles()
  fetchPopularArticles()
  fetchTags()
  startTyping()
  nextTick(() => initHeroAnimations())
})

onUnmounted(() => {
  if (typingTimer) clearTimeout(typingTimer)
  gsapCtx?.revert()
})
</script>

<style scoped>
/* Hero */
.hero {
  position: relative;
  padding: 5rem 2rem 4rem;
  text-align: center;
  overflow: hidden;
  background: var(--hero-gradient);
}

.hero-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}

.hero-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(129, 140, 248, 0.2) 0%, transparent 70%);
  filter: blur(60px);
  will-change: transform, opacity;
}

.hero-particles {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 700px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-block;
  padding: 0.3rem 0.9rem;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 100px;
  color: rgba(255,255,255,0.8);
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  margin-bottom: 1.25rem;
  backdrop-filter: blur(10px);
  background: rgba(255,255,255,0.05);
}

.hero-title {
  font-size: 3.2rem;
  font-weight: 800;
  color: #fff;
  margin: 0 0 0.75rem;
  letter-spacing: 0.05em;
  line-height: 1.2;
}

.title-word {
  display: inline-block;
  will-change: transform, opacity;
}

.gradient-text {
  background: linear-gradient(135deg, #818cf8, #c084fc, #f472b6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: rgba(255,255,255,0.65);
  margin: 0 0 2rem;
  font-weight: 300;
}

.cursor {
  opacity: 0;
  animation: blink 1s infinite;
  font-weight: 100;
  color: rgba(255,255,255,0.6);
}
.cursor.typing { animation: none; opacity: 1; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

/* Hero Stats */
.hero-stats {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
}

.stat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.85rem 1.75rem;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  backdrop-filter: blur(10px);
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 700;
  color: #fff;
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.55);
  margin-top: 0.15rem;
}

/* Hero Links (when no data) */
.hero-links {
  display: flex;
  justify-content: center;
  gap: 0.6rem;
}

.hero-link {
  padding: 0.5rem 1.2rem;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 8px;
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s;
  backdrop-filter: blur(10px);
  background: rgba(255,255,255,0.04);
}

.hero-link:hover {
  background: rgba(255,255,255,0.12);
  border-color: rgba(255,255,255,0.35);
}

/* Main Container */
.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 2rem 3rem;
}

.main-container.has-sidebar {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 2rem;
}

/* Section Header */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.title-accent {
  width: 3px;
  height: 18px;
  border-radius: 2px;
  background: var(--accent-gradient);
}

.view-all {
  color: var(--text-tertiary);
  text-decoration: none;
  font-size: 0.82rem;
  font-weight: 500;
  transition: color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.view-all:hover { color: var(--accent-primary); }
.view-all .arrow { transition: transform 0.2s; }
.view-all:hover .arrow { transform: translateX(3px); }

/* Article Cards */
.articles-grid {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.article-card {
  display: flex;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.25s ease;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--border-hover);
}

.card-accent {
  width: 3px;
  flex-shrink: 0;
}

.card-body {
  flex: 1;
  padding: 1rem 1.25rem;
  min-width: 0;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.35rem;
}

.card-date {
  font-size: 0.75rem;
  color: var(--text-tertiary);
  font-family: 'Consolas', monospace;
}

.card-board {
  font-size: 0.65rem;
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  background: rgba(129, 140, 248, 0.1);
  color: var(--accent-primary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.card-title {
  margin: 0 0 0.3rem;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  transition: color 0.2s;
}

.article-card:hover .card-title { color: var(--accent-primary); }

.card-summary {
  margin: 0 0 0.6rem;
  font-size: 0.82rem;
  color: var(--text-secondary);
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-tags { display: flex; gap: 0.3rem; flex-wrap: wrap; }

.mini-tag {
  font-size: 0.68rem;
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  font-weight: 500;
}

.card-stats {
  display: flex;
  gap: 0.6rem;
  color: var(--text-tertiary);
  font-size: 0.72rem;
}

.card-stats span {
  display: flex;
  align-items: center;
  gap: 0.15rem;
}

/* Sidebar */
.sidebar {
  padding-top: 2.75rem;
}

.widget {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 10px;
  padding: 1.1rem;
  margin-bottom: 0.85rem;
}

.widget-title {
  margin: 0 0 0.85rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* Popular */
.popular-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.5rem 0;
  cursor: pointer;
  border-bottom: 1px solid var(--card-border);
}

.popular-item:last-child { border-bottom: none; }
.popular-item:hover .popular-title { color: var(--accent-primary); }

.popular-rank {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.68rem;
  font-weight: 700;
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
}

.popular-rank.rank-1 { background: linear-gradient(135deg, #818cf8, #c084fc); color: #fff; }
.popular-rank.rank-2 { background: linear-gradient(135deg, #6366f1, #818cf8); color: #fff; }
.popular-rank.rank-3 { background: linear-gradient(135deg, #4f46e5, #6366f1); color: #fff; }

.popular-info { flex: 1; min-width: 0; }

.popular-title {
  display: block;
  font-size: 0.82rem;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: color 0.2s;
}

.popular-views {
  font-size: 0.68rem;
  color: var(--text-disabled);
  margin-top: 0.1rem;
  display: block;
}

/* Tag Cloud */
.tag-cloud { display: flex; flex-wrap: wrap; gap: 0.35rem; }

.tag-pill {
  font-size: 0.75rem;
  padding: 0.25rem 0.55rem;
  border-radius: 5px;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.tag-pill:hover {
  background: rgba(129, 140, 248, 0.12);
  color: var(--accent-primary);
}

.tag-count {
  font-size: 0.6rem;
  color: var(--text-disabled);
  font-weight: 600;
}

/* Empty */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }

.empty-title {
  margin: 0 0 0.35rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.empty-desc {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-disabled);
}

/* Loading Skeleton */
.loading-cards {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.skeleton-card {
  display: flex;
  border: 1px solid var(--card-border);
  border-radius: 10px;
  overflow: hidden;
  background: var(--card-bg);
}

.skeleton-accent {
  width: 3px;
  flex-shrink: 0;
}

.skeleton-body {
  flex: 1;
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.skeleton-line {
  height: 13px;
  border-radius: 3px;
  background: var(--bg-tertiary);
}

.w30 { width: 30%; }
.w50 { width: 50%; }
.w80 { width: 80%; }

.shimmer {
  background: linear-gradient(90deg, var(--bg-tertiary) 25%, rgba(129, 140, 248, 0.05) 50%, var(--bg-tertiary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* Responsive */
@media (max-width: 1024px) {
  .main-container.has-sidebar {
    grid-template-columns: 1fr;
  }
  .sidebar { padding-top: 0; }
}

@media (max-width: 768px) {
  .hero { padding: 3.5rem 1rem 3rem; }
  .hero-title { font-size: 2.2rem; }
  .hero-stats { flex-wrap: wrap; }
  .stat-card { padding: 0.7rem 1.1rem; }
  .hero-links { flex-wrap: wrap; justify-content: center; }
  .main-container { padding: 1.5rem 1rem 2rem; }
}
</style>
