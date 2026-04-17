<template>
  <div class="tech-page">
    <!-- Page Header -->
    <div class="page-hero">
      <div class="hero-content">
        <div class="hero-text">
          <span class="hero-badge">Blog</span>
          <h1 class="hero-title">技术博客</h1>
          <p class="hero-desc">记录技术成长，分享实践经验</p>
        </div>
        <div class="hero-actions">
          <div class="search-box">
            <span class="search-icon">
              <el-icon><Search /></el-icon>
            </span>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索文章..."
              @keyup.enter="handleSearch"
            />
            <button v-if="searchKeyword" class="search-clear" @click="searchKeyword = ''; handleSearch()">
              <el-icon><Close /></el-icon>
            </button>
          </div>
          <button v-if="isAdmin" class="btn-create" @click="$router.push('/admin/article/new')">
            <el-icon><Plus /></el-icon>
            <span>新建文章</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Category Filter -->
    <div class="category-bar">
      <button
        class="cat-chip"
        :class="{ active: !selectedCategoryId }"
        @click="selectedCategoryId = ''; currentPage = 1; fetchArticles()"
      >
        全部
      </button>
      <button
        v-for="cat in categories"
        :key="cat.id"
        class="cat-chip"
        :class="{ active: selectedCategoryId === cat.id }"
        @click="handleCategoryClick(cat)"
      >
        <span class="cat-icon">{{ cat.icon }}</span>
        {{ cat.name }}
        <span class="cat-count">{{ cat.article_count }}</span>
      </button>
    </div>

    <!-- Article List -->
    <div class="article-section">
      <div v-if="loading" class="loading-state">
        <div v-for="i in 3" :key="i" class="skeleton-card">
          <div class="skeleton-cover shimmer"></div>
          <div class="skeleton-body">
            <div class="skeleton-line short shimmer"></div>
            <div class="skeleton-line long shimmer"></div>
            <div class="skeleton-line medium shimmer"></div>
          </div>
        </div>
      </div>

      <template v-else-if="articles.length > 0">
        <div ref="articleListRef" class="article-list-animated">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
          class="reveal-article"
          @click="handleArticleClick"
          @edit="handleArticleEdit"
          @delete="handleArticleDelete"
        />

        </div>
        <div class="pagination-wrap">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 50]"
            layout="total, prev, pager, next"
            @current-change="fetchArticles"
            @size-change="fetchArticles"
          />
        </div>
      </template>

      <div v-else class="empty-state">
        <div class="empty-icon">📝</div>
        <p class="empty-text">暂无文章</p>
        <p class="empty-sub">换个分类看看，或者稍后再来</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Close, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import ArticleCard from '@/components/article/ArticleCard.vue'
import { getArticles, searchArticles, deleteArticle, type Article } from '@/api/article'
import { getCategories, type Category } from '@/api/category'
import { useUserStore } from '@/stores/user'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const router = useRouter()
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)
const articleListRef = ref<HTMLElement | null>(null)
let gsapCtx: gsap.Context | null = null

const animateArticles = () => {
  if (!articleListRef.value) return
  gsapCtx?.revert()
  gsapCtx = gsap.context(() => {
    gsap.from('.reveal-article', {
      x: -50,
      y: 30,
      opacity: 0,
      scale: 0.9,
      duration: 0.7,
      stagger: 0.12,
      ease: 'power3.out',
    })
  }, articleListRef.value)
}

onUnmounted(() => { gsapCtx?.revert() })

interface CategoryUI extends Category { icon: string }

const categoryIcons: Record<string, string> = {
  '数据库技术': '🗄️', '数据与算法': '🧮', 'Linux 与运维': '🐧',
  '其他技术': '🔌', 'Python 全栈': '🐍', 'DevOps 工具': '🛠️',
  'Golang 开发': '🐹', '容器与云原生': '🐳'
}

const categories = ref<CategoryUI[]>([])
const selectedCategoryId = ref('')
const loading = ref(false)
const articles = ref<Article[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchKeyword = ref('')

const fetchCategoriesData = async () => {
  try {
    const res = await getCategories('tech')
    categories.value = res.data.map(cat => ({ ...cat, icon: categoryIcons[cat.name] || '📂' }))
  } catch { ElMessage.error('加载分类失败') }
}

const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await getArticles({
      board: 'tech', is_published: true,
      category_id: selectedCategoryId.value || undefined,
      page: currentPage.value, page_size: pageSize.value
    })
    articles.value = response.data.items
    total.value = response.data.pagination.total
    await nextTick()
    animateArticles()
  } catch (error: any) {
    ElMessage.error(error.message || '加载文章失败')
  } finally { loading.value = false }
}

const handleSearch = async () => {
  if (!searchKeyword.value.trim()) { fetchArticles(); return }
  loading.value = true
  try {
    const response = await searchArticles(searchKeyword.value, currentPage.value, pageSize.value)
    articles.value = response.data.items
    total.value = response.data.pagination.total
  } catch (error: any) {
    ElMessage.error(error.message || '搜索失败')
  } finally { loading.value = false }
}

const handleArticleClick = (article: Article) => router.push(`/tech/${article.id}`)
const handleArticleEdit = (article: Article) => router.push(`/admin/article/edit/${article.id}`)

const handleArticleDelete = async (article: Article) => {
  try {
    await ElMessageBox.confirm(`确定要删除文章「${article.title}」吗？`, '删除确认', {
      confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning'
    })
    await deleteArticle(article.id)
    ElMessage.success('文章已删除')
    fetchArticles()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '删除失败')
  }
}

const handleCategoryClick = (cat: CategoryUI) => {
  selectedCategoryId.value = selectedCategoryId.value === cat.id ? '' : cat.id
  currentPage.value = 1
  fetchArticles()
}

onMounted(() => { fetchCategoriesData(); fetchArticles() })
</script>

<style scoped>
.tech-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 2rem 3rem;
}

/* Hero */
.page-hero {
  padding: 2.5rem 0 1.5rem;
}

.hero-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 2rem;
}

.hero-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  background: rgba(129, 140, 248, 0.15);
  color: var(--accent-primary);
  margin-bottom: 0.5rem;
}

.hero-title {
  margin: 0;
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}

.hero-desc {
  margin: 0.3rem 0 0;
  font-size: 0.95rem;
  color: var(--text-tertiary);
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

/* Search */
.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  color: var(--text-disabled);
  font-size: 0.9rem;
  display: flex;
}

.search-box input {
  width: 220px;
  padding: 0.55rem 2rem 0.55rem 2.2rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 0.85rem;
  outline: none;
  transition: all 0.2s;
}

.search-box input::placeholder { color: var(--text-disabled); }
.search-box input:focus { border-color: var(--accent-primary); box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.1); }

.search-clear {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  color: var(--text-disabled);
  cursor: pointer;
  display: flex;
  padding: 0.2rem;
}

/* Create Button */
.btn-create {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.55rem 1rem;
  background: var(--accent-gradient);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-create:hover { opacity: 0.9; transform: translateY(-1px); }

/* Category Bar */
.category-bar {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--card-border);
  margin-bottom: 1.5rem;
}

.cat-chip {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.85rem;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.cat-chip:hover { border-color: var(--accent-primary); color: var(--accent-primary); }

.cat-chip.active {
  background: rgba(129, 140, 248, 0.12);
  border-color: var(--accent-primary);
  color: var(--accent-primary);
  font-weight: 600;
}

.cat-icon { font-size: 1rem; }

.cat-count {
  font-size: 0.7rem;
  padding: 0.05rem 0.35rem;
  border-radius: 8px;
  background: var(--bg-tertiary);
  color: var(--text-disabled);
  font-weight: 600;
}

.cat-chip.active .cat-count {
  background: rgba(129, 140, 248, 0.2);
  color: var(--accent-primary);
}

/* Article Section */
.article-section { min-height: 400px; }

/* Skeleton */
.skeleton-card {
  display: flex;
  gap: 1.25rem;
  padding: 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid var(--card-border);
  border-radius: 12px;
  background: var(--card-bg);
}

.skeleton-cover {
  flex-shrink: 0;
  width: 180px;
  height: 120px;
  border-radius: 8px;
  background: var(--bg-tertiary);
}

.skeleton-body { flex: 1; display: flex; flex-direction: column; gap: 0.6rem; padding: 0.5rem 0; }

.skeleton-line {
  height: 14px;
  border-radius: 4px;
  background: var(--bg-tertiary);
}

.skeleton-line.short { width: 30%; }
.skeleton-line.long { width: 80%; }
.skeleton-line.medium { width: 55%; }

.shimmer {
  background: linear-gradient(90deg, var(--bg-tertiary) 25%, rgba(129, 140, 248, 0.05) 50%, var(--bg-tertiary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* Pagination */
.pagination-wrap {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--card-border);
}

/* Empty */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-text { margin: 0; font-size: 1.1rem; font-weight: 600; color: var(--text-secondary); }
.empty-sub { margin: 0.3rem 0 0; font-size: 0.85rem; color: var(--text-disabled); }

/* Mobile */
@media (max-width: 768px) {
  .tech-page { padding: 0 1rem 2rem; }
  .hero-content { flex-direction: column; align-items: stretch; }
  .hero-actions { flex-direction: column; }
  .search-box input { width: 100%; }
  .btn-create { width: 100%; justify-content: center; }
  .category-bar { overflow-x: auto; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }
  .skeleton-card { flex-direction: column; }
  .skeleton-cover { width: 100%; height: 140px; }
}
</style>
