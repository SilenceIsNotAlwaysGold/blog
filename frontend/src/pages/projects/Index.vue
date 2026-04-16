<template>
  <div class="projects-page">
    <!-- Header -->
    <div class="page-hero">
      <div class="hero-content">
        <div class="hero-text">
          <span class="hero-badge">Portfolio</span>
          <h1 class="hero-title">项目作品</h1>
          <p class="hero-desc">技术实践与创造的成果展示</p>
        </div>
        <button v-if="isAdmin" class="btn-create" @click="handleNewProject">
          <el-icon><Plus /></el-icon>
          <span>新建项目</span>
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <div class="filter-group">
        <button
          class="filter-chip"
          :class="{ active: !filterStatus }"
          @click="filterStatus = ''; fetchProjects()"
        >全部</button>
        <button
          v-for="s in statusOptions"
          :key="s.value"
          class="filter-chip"
          :class="{ active: filterStatus === s.value }"
          @click="filterStatus = s.value; fetchProjects()"
        >
          <span class="status-dot" :class="'dot-' + s.value"></span>
          {{ s.label }}
        </button>
      </div>
      <div class="filter-tech">
        <el-select
          v-model="filterTech"
          placeholder="技术栈筛选"
          clearable
          filterable
          size="small"
          @change="fetchProjects"
        >
          <el-option v-for="tech in techList" :key="tech" :label="tech" :value="tech" />
        </el-select>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error-state">
      <div class="error-card">
        <span class="error-icon">⚠️</span>
        <p class="error-text">加载失败，请检查网络连接</p>
        <button class="retry-btn" @click="retryFetch">重新加载</button>
      </div>
    </div>

    <!-- Loading -->
    <div v-else-if="loading" class="grid-skeleton">
      <div v-for="i in 6" :key="i" class="skeleton-card">
        <div class="skeleton-cover shimmer"></div>
        <div class="skeleton-body">
          <div class="skeleton-line w60 shimmer"></div>
          <div class="skeleton-line w90 shimmer"></div>
          <div class="skeleton-line w40 shimmer"></div>
        </div>
      </div>
    </div>

    <!-- Projects Grid -->
    <template v-else-if="projects.length > 0">
      <div ref="gridRef" class="projects-grid">
        <ProjectCard
          v-for="project in projects"
          :key="project.id"
          :project="project"
          class="reveal-project"
          @edit="handleEditProject"
          @delete="handleDeleteProject"
        />
      </div>
    </template>

    <!-- Empty -->
    <div v-else class="empty-state">
      <div class="empty-icon">🚀</div>
      <p class="empty-text">暂无项目</p>
      <p class="empty-sub">精彩项目即将上线</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import ProjectCard from '@/components/project/ProjectCard.vue'
import { getProjects, getTechStack, deleteProject, type Project } from '@/api/project'
import { useUserStore } from '@/stores/user'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const router = useRouter()
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const loading = ref(false)
const projects = ref<Project[]>([])
const techList = ref<string[]>([])
const filterStatus = ref('')
const filterTech = ref('')
const error = ref(false)
const gridRef = ref<HTMLElement | null>(null)
let gsapCtx: gsap.Context | null = null

const animateCards = () => {
  if (!gridRef.value) return
  gsapCtx?.revert()
  gsapCtx = gsap.context(() => {
    gsap.from('.reveal-project', {
      y: 50,
      opacity: 0,
      duration: 0.6,
      stagger: 0.1,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: gridRef.value!,
        start: 'top 85%',
        once: true,
      },
    })
  }, gridRef.value)
}

onUnmounted(() => { gsapCtx?.revert() })

const statusOptions = [
  { label: '已完成', value: 'completed' },
  { label: '进行中', value: 'in_progress' },
  { label: '计划中', value: 'planned' }
]

const fetchProjects = async () => {
  loading.value = true
  error.value = false
  try {
    const response = await getProjects({
      status: filterStatus.value || undefined,
      tech: filterTech.value || undefined
    })
    projects.value = response.data || []
    await nextTick()
    animateCards()
  } catch {
    error.value = true
  } finally { loading.value = false }
}

const fetchTechStack = async () => {
  try {
    const response = await getTechStack()
    techList.value = response.data || []
  } catch { /* ignore */ }
}

const retryFetch = () => { error.value = false; fetchProjects(); fetchTechStack() }
const handleNewProject = () => router.push('/admin/project/new')
const handleEditProject = (id: string) => router.push(`/admin/project/edit/${id}`)

const handleDeleteProject = async (id: string) => {
  try {
    await ElMessageBox.confirm('确定要删除此项目吗？此操作不可恢复。', '删除确认', {
      confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning'
    })
    await deleteProject(id)
    ElMessage.success('项目已删除')
    fetchProjects()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '删除失败')
  }
}

onMounted(() => { fetchProjects(); fetchTechStack() })
</script>

<style scoped>
.projects-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 2rem 3rem;
}

/* Hero */
.page-hero { padding: 2.5rem 0 1.5rem; }

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
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
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
  flex-shrink: 0;
}

.btn-create:hover { opacity: 0.9; transform: translateY(-1px); }

/* Filters */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--card-border);
  margin-bottom: 2rem;
}

.filter-group { display: flex; gap: 0.4rem; flex-wrap: wrap; }

.filter-chip {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-chip:hover { border-color: var(--accent-primary); color: var(--accent-primary); }

.filter-chip.active {
  background: rgba(129, 140, 248, 0.12);
  border-color: var(--accent-primary);
  color: var(--accent-primary);
  font-weight: 600;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.dot-completed { background: #10b981; }
.dot-in_progress { background: #3b82f6; }
.dot-planned { background: #f59e0b; }

/* Grid */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
}

/* Error */
.error-state {
  display: flex;
  justify-content: center;
  padding: 4rem 0;
}

.error-card {
  text-align: center;
  padding: 3rem 2rem;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
}

.error-icon { font-size: 3rem; }
.error-text { margin: 1rem 0; color: var(--text-secondary); }

.retry-btn {
  padding: 0.5rem 1.5rem;
  border: 1px solid var(--accent-primary);
  border-radius: 8px;
  background: transparent;
  color: var(--accent-primary);
  cursor: pointer;
  transition: all 0.2s;
}

.retry-btn:hover { background: rgba(129, 140, 248, 0.1); }

/* Skeleton */
.grid-skeleton {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
}

.skeleton-card {
  border: 1px solid var(--card-border);
  border-radius: 12px;
  overflow: hidden;
  background: var(--card-bg);
}

.skeleton-cover { height: 180px; background: var(--bg-tertiary); }
.skeleton-body { padding: 1.25rem; display: flex; flex-direction: column; gap: 0.6rem; }

.skeleton-line { height: 14px; border-radius: 4px; background: var(--bg-tertiary); }
.w40 { width: 40%; }
.w60 { width: 60%; }
.w90 { width: 90%; }

.shimmer {
  background: linear-gradient(90deg, var(--bg-tertiary) 25%, rgba(129, 140, 248, 0.05) 50%, var(--bg-tertiary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* Empty */
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-text { margin: 0; font-size: 1.1rem; font-weight: 600; color: var(--text-secondary); }
.empty-sub { margin: 0.3rem 0 0; font-size: 0.85rem; color: var(--text-disabled); }

/* Mobile */
@media (max-width: 768px) {
  .projects-page { padding: 0 1rem 2rem; }
  .hero-content { flex-direction: column; align-items: stretch; }
  .btn-create { width: 100%; justify-content: center; }
  .filter-bar { flex-direction: column; align-items: stretch; }
  .filter-tech { width: 100%; }
  .filter-tech .el-select { width: 100% !important; }
  .projects-grid { grid-template-columns: 1fr; }
  .grid-skeleton { grid-template-columns: 1fr; }
}
</style>
