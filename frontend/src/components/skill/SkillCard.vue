<template>
  <div class="skill-card">
    <!-- Admin -->
    <div v-if="isAdmin" class="admin-bar" @click.stop>
      <button class="admin-action edit" @click="handleEdit" title="编辑">
        <el-icon><Edit /></el-icon>
      </button>
      <button class="admin-action delete" @click="handleDelete" title="删除">
        <el-icon><Delete /></el-icon>
      </button>
    </div>

    <div class="skill-top">
      <div class="skill-icon-wrap">
        <img v-if="skill.icon" :src="skill.icon" :alt="skill.name" class="skill-icon" />
        <span v-else class="skill-icon-fallback">{{ skill.name.charAt(0) }}</span>
      </div>
      <div class="skill-info">
        <h3 class="skill-name">{{ skill.name }}</h3>
        <span class="skill-level" :class="levelClass">{{ levelLabel }}</span>
      </div>
    </div>

    <!-- Progress -->
    <div class="progress-wrap">
      <div class="progress-track">
        <div
          ref="progressFillRef"
          class="progress-fill"
          :style="{ width: animatedWidth + '%', background: progressColor }"
        ></div>
      </div>
      <span class="progress-text">{{ Math.round(animatedValue) }}%</span>
    </div>

    <p v-if="skill.description" class="skill-desc">{{ skill.description }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { Edit, Delete } from '@element-plus/icons-vue'
import type { Skill } from '@/api/skill'
import { useUserStore } from '@/stores/user'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const props = defineProps<{ skill: Skill }>()
const emit = defineEmits<{ edit: [id: string]; delete: [id: string] }>()

const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

// Animated progress
const progressFillRef = ref<HTMLElement | null>(null)
const animatedValue = ref(0)
const animatedWidth = ref(0)

let scrollTween: gsap.core.Tween | null = null

onMounted(() => {
  if (!progressFillRef.value) return
  const card = progressFillRef.value.closest('.skill-card')
  if (!card) return

  scrollTween = gsap.to(animatedValue, {
    value: props.skill.proficiency,
    duration: 1.2,
    ease: 'power2.out',
    scrollTrigger: {
      trigger: card,
      start: 'top 90%',
      once: true,
    },
    onUpdate: () => {
      animatedWidth.value = animatedValue.value
    },
  })
})

onUnmounted(() => {
  scrollTween?.kill()
})

const progressColor = computed(() => {
  const p = props.skill.proficiency
  if (p >= 80) return 'linear-gradient(90deg, #10b981, #34d399)'
  if (p >= 60) return 'linear-gradient(90deg, #3b82f6, #60a5fa)'
  if (p >= 40) return 'linear-gradient(90deg, #f59e0b, #fbbf24)'
  return 'linear-gradient(90deg, #ef4444, #f87171)'
})

const levelClass = computed(() => {
  const p = props.skill.proficiency
  if (p >= 80) return 'level-expert'
  if (p >= 60) return 'level-proficient'
  if (p >= 40) return 'level-intermediate'
  return 'level-beginner'
})

const levelLabel = computed(() => {
  const p = props.skill.proficiency
  if (p >= 80) return '精通'
  if (p >= 60) return '熟练'
  if (p >= 40) return '掌握'
  return '入门'
})

const handleEdit = () => emit('edit', props.skill.id)
const handleDelete = () => emit('delete', props.skill.id)
</script>

<style scoped>
.skill-card {
  position: relative;
  padding: 1.25rem;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.skill-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
  border-color: var(--accent-primary);
}

/* Admin */
.admin-bar {
  position: absolute;
  top: 0.6rem;
  right: 0.6rem;
  display: flex;
  gap: 0.25rem;
  opacity: 0;
  transform: translateY(-4px);
  transition: all 0.25s ease;
}

.skill-card:hover .admin-bar {
  opacity: 1;
  transform: translateY(0);
}

.admin-action {
  width: 26px;
  height: 26px;
  border-radius: 6px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  backdrop-filter: blur(10px);
  transition: all 0.2s;
  font-size: 0.78rem;
}

.admin-action.edit { background: rgba(99, 102, 241, 0.85); color: #fff; }
.admin-action.edit:hover { background: rgba(99, 102, 241, 1); }
.admin-action.delete { background: rgba(239, 68, 68, 0.85); color: #fff; }
.admin-action.delete:hover { background: rgba(239, 68, 68, 1); }

/* Top */
.skill-top {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.85rem;
}

.skill-icon-wrap {
  width: 42px;
  height: 42px;
  flex-shrink: 0;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
}

.skill-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 4px;
}

.skill-icon-fallback {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--accent-primary);
}

.skill-info { flex: 1; min-width: 0; }

.skill-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 650;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.skill-level {
  font-size: 0.68rem;
  font-weight: 600;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.level-expert { background: rgba(16, 185, 129, 0.12); color: #10b981; }
.level-proficient { background: rgba(59, 130, 246, 0.12); color: #3b82f6; }
.level-intermediate { background: rgba(245, 158, 11, 0.12); color: #f59e0b; }
.level-beginner { background: rgba(239, 68, 68, 0.12); color: #ef4444; }

/* Progress */
.progress-wrap {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.75rem;
}

.progress-track {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: var(--bg-tertiary);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease;
}

.progress-text {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-tertiary);
  font-family: 'Consolas', monospace;
  min-width: 2.5rem;
  text-align: right;
}

/* Desc */
.skill-desc {
  margin: 0;
  font-size: 0.8rem;
  color: var(--text-tertiary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Mobile */
@media (max-width: 768px) {
  .admin-bar { opacity: 1; transform: translateY(0); }
}
</style>
