<template>
  <div class="projects-page">
    <div class="page-header">
      <h1>Projects Portfolio</h1>
      <p class="subtitle">Showcase of my work and technical achievements</p>
    </div>

    <div class="filters">
      <el-select
        v-model="filterStatus"
        placeholder="Filter by status"
        clearable
        style="width: 180px"
        @change="fetchProjects"
      >
        <el-option label="Completed" value="completed" />
        <el-option label="In Progress" value="in_progress" />
        <el-option label="Planned" value="planned" />
      </el-select>

      <el-select
        v-model="filterTech"
        placeholder="Filter by technology"
        clearable
        filterable
        style="width: 200px"
        @change="fetchProjects"
      >
        <el-option
          v-for="tech in techList"
          :key="tech"
          :label="tech"
          :value="tech"
        />
      </el-select>
    </div>

    <el-skeleton v-if="loading" :rows="10" animated />

    <template v-else-if="projects.length > 0">
      <div class="projects-grid">
        <ProjectCard
          v-for="project in projects"
          :key="project.id"
          :project="project"
        />
      </div>
    </template>

    <el-empty v-else description="No projects found" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import ProjectCard from '@/components/project/ProjectCard.vue'
import { getProjects, getTechStack, type Project } from '@/api/project'

const loading = ref(false)
const projects = ref<Project[]>([])
const techList = ref<string[]>([])
const filterStatus = ref<string>('')
const filterTech = ref<string>('')

const fetchProjects = async () => {
  loading.value = true
  try {
    const response = await getProjects({
      status: filterStatus.value || undefined,
      tech: filterTech.value || undefined
    })
    projects.value = response.data.data
  } catch (error: any) {
    ElMessage.error(error.message || 'Failed to fetch projects')
  } finally {
    loading.value = false
  }
}

const fetchTechStack = async () => {
  try {
    const response = await getTechStack()
    techList.value = response.data.data
  } catch (error: any) {
    console.error('Failed to fetch tech stack:', error)
  }
}

onMounted(() => {
  fetchProjects()
  fetchTechStack()
})
</script>

<style scoped>
.projects-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
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

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

@media (max-width: 768px) {
  .projects-page {
    padding: 1rem;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .filters {
    flex-direction: column;
  }

  .filters .el-select {
    width: 100% !important;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
