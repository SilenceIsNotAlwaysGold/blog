<template>
  <div class="project-card">
    <div v-if="project.cover_image" class="project-cover">
      <img :src="project.cover_image" :alt="project.name" />
      <div class="project-status" :class="`status-${project.status}`">
        {{ getStatusLabel(project.status) }}
      </div>
    </div>
    <div v-else class="project-cover-placeholder">
      <el-icon :size="64"><Folder /></el-icon>
      <div class="project-status" :class="`status-${project.status}`">
        {{ getStatusLabel(project.status) }}
      </div>
    </div>

    <div class="project-content">
      <h3 class="project-name">{{ project.name }}</h3>

      <p class="project-description">{{ project.description }}</p>

      <div v-if="project.highlights && project.highlights.length > 0" class="project-highlights">
        <div
          v-for="(highlight, index) in project.highlights.slice(0, 3)"
          :key="index"
          class="highlight-item"
        >
          <el-icon><Check /></el-icon>
          <span>{{ highlight }}</span>
        </div>
      </div>

      <div class="project-tech">
        <el-tag
          v-for="tech in project.tech_stack.slice(0, 5)"
          :key="tech"
          size="small"
          type="info"
        >
          {{ tech }}
        </el-tag>
        <el-tag v-if="project.tech_stack.length > 5" size="small" type="info">
          +{{ project.tech_stack.length - 5 }}
        </el-tag>
      </div>

      <div class="project-footer">
        <div class="project-date" v-if="project.start_date">
          <el-icon><Calendar /></el-icon>
          <span>{{ formatDate(project.start_date) }}</span>
        </div>

        <div class="project-links">
          <el-button
            v-if="project.demo_url"
            size="small"
            :icon="Link"
            @click.stop="openLink(project.demo_url)"
          >
            Demo
          </el-button>
          <el-button
            v-if="project.github_url"
            size="small"
            :icon="Link"
            @click.stop="openLink(project.github_url)"
          >
            GitHub
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Folder, Check, Calendar, Link } from '@element-plus/icons-vue'
import type { Project } from '@/api/project'

defineProps<{
  project: Project
}>()

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    completed: 'Completed',
    in_progress: 'In Progress',
    planned: 'Planned'
  }
  return labels[status] || status
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short'
  })
}

const openLink = (url: string) => {
  window.open(url, '_blank')
}
</script>

<style scoped>
.project-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.project-cover {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.project-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.project-card:hover .project-cover img {
  transform: scale(1.05);
}

.project-cover-placeholder {
  position: relative;
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.project-status {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-completed {
  background: #67c23a;
  color: #fff;
}

.status-in_progress {
  background: #409eff;
  color: #fff;
}

.status-planned {
  background: #e6a23c;
  color: #fff;
}

.project-content {
  padding: 1.5rem;
}

.project-name {
  margin: 0 0 0.75rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #303133;
}

.project-description {
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
  color: #606266;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-highlights {
  margin-bottom: 1rem;
}

.highlight-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
  color: #606266;
}

.highlight-item .el-icon {
  color: #67c23a;
  flex-shrink: 0;
}

.project-tech {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.project-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #ebeef5;
}

.project-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #909399;
}

.project-links {
  display: flex;
  gap: 0.5rem;
}
</style>
