<template>
  <div class="skills-page">
    <!-- Header -->
    <div class="page-hero">
      <div class="hero-content">
        <div class="hero-text">
          <span class="hero-badge">Skills</span>
          <h1 class="hero-title">技术技能</h1>
          <p class="hero-desc">专业领域与技术栈的掌握程度</p>
        </div>
        <button v-if="isAdmin" class="btn-create" @click="handleNewSkill">
          <el-icon><Plus /></el-icon>
          <span>新建技能</span>
        </button>
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="error-state">
      <div class="error-card">
        <span class="error-icon">⚠️</span>
        <p class="error-text">加载失败，请检查网络连接</p>
        <button class="retry-btn" @click="retryFetch">重新加载</button>
      </div>
    </div>

    <!-- Loading -->
    <div v-else-if="loading" class="loading-state">
      <div v-for="i in 2" :key="i" class="skeleton-group">
        <div class="skeleton-line w40 h-lg shimmer" style="margin-bottom: 1.25rem"></div>
        <div class="skeleton-grid">
          <div v-for="j in 3" :key="j" class="skeleton-skill shimmer"></div>
        </div>
      </div>
    </div>

    <!-- Skills -->
    <template v-else-if="Object.keys(skillsGrouped).length > 0">
      <div
        v-for="(skills, category) in skillsGrouped"
        :key="category"
        class="skill-group reveal-group"
      >
        <div class="group-header">
          <h2 class="group-title">{{ category }}</h2>
          <span class="group-count">{{ skills.length }} 项技能</span>
        </div>
        <div class="skills-grid">
          <SkillCard
            v-for="skill in skills"
            :key="skill.id"
            :skill="skill"
            class="reveal-skill"
            @edit="handleEditSkill"
            @delete="handleDeleteSkill"
          />
        </div>
      </div>
    </template>

    <!-- Empty -->
    <div v-else class="empty-state">
      <div class="empty-icon">🎯</div>
      <p class="empty-text">暂无技能数据</p>
      <p class="empty-sub">技能信息即将添加</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import SkillCard from '@/components/skill/SkillCard.vue'
import { getSkillsGrouped, deleteSkill, type SkillsGrouped } from '@/api/skill'
import { useUserStore } from '@/stores/user'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const router = useRouter()
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const loading = ref(false)
const skillsGrouped = ref<SkillsGrouped>({})
const error = ref(false)
let gsapCtx: gsap.Context | null = null

const animateSkillGroups = () => {
  const groups = document.querySelectorAll('.reveal-group')
  if (!groups.length) return
  gsapCtx?.revert()
  groups.forEach((group) => {
    const cards = group.querySelectorAll('.reveal-skill')
    gsap.from(cards, {
      y: 40,
      opacity: 0,
      duration: 0.6,
      stagger: 0.08,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: group,
        start: 'top 85%',
        once: true,
      },
    })
  })
}

onUnmounted(() => { gsapCtx?.revert() })

const fetchSkills = async () => {
  loading.value = true
  error.value = false
  try {
    const response = await getSkillsGrouped()
    skillsGrouped.value = response.data || {}
    await nextTick()
    animateSkillGroups()
  } catch {
    error.value = true
  } finally { loading.value = false }
}

const retryFetch = () => { error.value = false; fetchSkills() }
const handleNewSkill = () => router.push('/admin/skill/new')
const handleEditSkill = (id: string) => router.push(`/admin/skill/edit/${id}`)

const handleDeleteSkill = async (id: string) => {
  try {
    await ElMessageBox.confirm('确定要删除此技能吗？此操作不可恢复。', '删除确认', {
      confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning'
    })
    await deleteSkill(id)
    ElMessage.success('技能已删除')
    fetchSkills()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '删除失败')
  }
}

onMounted(() => { fetchSkills() })
</script>

<style scoped>
.skills-page {
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
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
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

/* Skill Groups */
.skill-group {
  margin-bottom: 2.5rem;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--card-border);
}

.group-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.group-title::before {
  content: '';
  width: 3px;
  height: 1.1em;
  background: var(--accent-gradient);
  border-radius: 2px;
}

.group-count {
  font-size: 0.78rem;
  color: var(--text-disabled);
  font-weight: 500;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
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
.loading-state { padding-top: 1rem; }

.skeleton-group { margin-bottom: 2.5rem; }

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.skeleton-skill {
  height: 140px;
  border-radius: 12px;
  background: var(--bg-tertiary);
}

.skeleton-line { height: 14px; border-radius: 4px; background: var(--bg-tertiary); }
.skeleton-line.h-lg { height: 22px; }
.w40 { width: 40%; }

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
  .skills-page { padding: 0 1rem 2rem; }
  .hero-content { flex-direction: column; align-items: stretch; }
  .btn-create { width: 100%; justify-content: center; }
  .skills-grid { grid-template-columns: 1fr; }
  .skeleton-grid { grid-template-columns: 1fr; }
}
</style>
