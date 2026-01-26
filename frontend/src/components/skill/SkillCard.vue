<template>
  <div class="skill-card">
    <div class="skill-header">
      <div class="skill-icon" v-if="skill.icon">
        <img :src="skill.icon" :alt="skill.name" />
      </div>
      <div class="skill-icon-placeholder" v-else>
        <el-icon :size="32"><Tools /></el-icon>
      </div>
      <h3 class="skill-name">{{ skill.name }}</h3>
    </div>

    <div class="skill-proficiency">
      <div class="proficiency-label">
        <span>Proficiency</span>
        <span class="proficiency-value">{{ skill.proficiency }}%</span>
      </div>
      <el-progress
        :percentage="skill.proficiency"
        :color="getProgressColor(skill.proficiency)"
        :stroke-width="8"
      />
    </div>

    <p v-if="skill.description" class="skill-description">
      {{ skill.description }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { Tools } from '@element-plus/icons-vue'
import type { Skill } from '@/api/skill'

defineProps<{
  skill: Skill
}>()

const getProgressColor = (proficiency: number) => {
  if (proficiency >= 80) return '#67c23a'
  if (proficiency >= 60) return '#409eff'
  if (proficiency >= 40) return '#e6a23c'
  return '#f56c6c'
}
</script>

<style scoped>
.skill-card {
  padding: 1.5rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.skill-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.skill-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.skill-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
}

.skill-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.skill-icon-placeholder {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 8px;
  color: #909399;
  flex-shrink: 0;
}

.skill-name {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #303133;
}

.skill-proficiency {
  margin-bottom: 1rem;
}

.proficiency-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #606266;
}

.proficiency-value {
  font-weight: 600;
  color: #303133;
}

.skill-description {
  margin: 0;
  font-size: 0.9rem;
  color: #606266;
  line-height: 1.6;
}
</style>
