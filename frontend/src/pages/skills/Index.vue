<template>
  <div class="skills-page">
    <div class="page-header">
      <h1>Technical Skills</h1>
      <p class="subtitle">My expertise and proficiency across various technologies</p>
    </div>

    <el-skeleton v-if="loading" :rows="10" animated />

    <template v-else-if="Object.keys(skillsGrouped).length > 0">
      <div
        v-for="(skills, category) in skillsGrouped"
        :key="category"
        class="skill-category"
      >
        <h2 class="category-title">
          <el-icon><Collection /></el-icon>
          {{ category }}
        </h2>

        <div class="skills-grid">
          <SkillCard
            v-for="skill in skills"
            :key="skill.id"
            :skill="skill"
          />
        </div>
      </div>
    </template>

    <el-empty v-else description="No skills found" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Collection } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import SkillCard from '@/components/skill/SkillCard.vue'
import { getSkillsGrouped, type SkillsGrouped } from '@/api/skill'

const loading = ref(false)
const skillsGrouped = ref<SkillsGrouped>({})

const fetchSkills = async () => {
  loading.value = true
  try {
    const response = await getSkillsGrouped()
    skillsGrouped.value = response.data.data
  } catch (error: any) {
    ElMessage.error(error.message || 'Failed to fetch skills')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSkills()
})
</script>

<style scoped>
.skills-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
  font-weight: 700;
  color: #303133;
}

.subtitle {
  margin: 0;
  font-size: 1.1rem;
  color: #606266;
}

.skill-category {
  margin-bottom: 3rem;
}

.category-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 1.5rem 0;
  font-size: 1.75rem;
  font-weight: 600;
  color: #303133;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #409eff;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .skills-page {
    padding: 1rem;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .category-title {
    font-size: 1.5rem;
  }

  .skills-grid {
    grid-template-columns: 1fr;
  }
}
</style>
