<template>
  <div class="skill-editor">
    <div class="editor-header">
      <div class="header-left">
        <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
        <h1>{{ isEdit ? '编辑技能' : '新建技能' }}</h1>
      </div>
      <div class="header-right">
        <el-button @click="handleSave" :loading="saving" type="primary">
          {{ isEdit ? '更新技能' : '创建技能' }}
        </el-button>
      </div>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="editor-form"
    >
      <el-card shadow="never" class="form-card">
        <el-form-item label="技能名称" prop="name">
          <el-input
            v-model="form.name"
            placeholder="请输入技能名称"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="技能分类" prop="category">
              <el-select
                v-model="form.category"
                filterable
                allow-create
                default-first-option
                placeholder="请选择或输入分类"
                style="width: 100%"
              >
                <el-option label="Frontend" value="Frontend" />
                <el-option label="Backend" value="Backend" />
                <el-option label="Database" value="Database" />
                <el-option label="DevOps" value="DevOps" />
                <el-option label="Tools" value="Tools" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="熟练度" prop="proficiency">
              <el-slider
                v-model="form.proficiency"
                :min="0"
                :max="100"
                :step="5"
                show-input
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="技能描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入技能描述（可选）"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="图标 URL" prop="icon">
              <el-input
                v-model="form.icon"
                placeholder="请输入图标 URL（可选）"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="排序" prop="order">
              <el-input-number
                v-model="form.order"
                :min="0"
                :max="999"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { createSkill, updateSkill, getSkill, type SkillCreate, type SkillUpdate } from '@/api/skill'

const route = useRoute()
const router = useRouter()

const formRef = ref<FormInstance>()
const saving = ref(false)
const isEdit = ref(false)
const skillId = ref('')

const form = reactive({
  name: '',
  category: '',
  proficiency: 50,
  description: '',
  icon: '',
  order: 0
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入技能名称', trigger: 'blur' },
    { min: 2, max: 50, message: '名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择或输入分类', trigger: 'change' }
  ],
  proficiency: [
    { required: true, message: '请设置熟练度', trigger: 'change' },
    { type: 'number', min: 0, max: 100, message: '熟练度范围为 0-100', trigger: 'change' }
  ]
}

// 加载技能数据（编辑模式）
const loadSkill = async () => {
  try {
    const response = await getSkill(skillId.value)
    const skill = response.data

    form.name = skill.name
    form.category = skill.category
    form.proficiency = skill.proficiency
    form.description = skill.description || ''
    form.icon = skill.icon || ''
    form.order = skill.order
  } catch (error: any) {
    ElMessage.error(error.message || '加载技能失败')
    router.push('/skills')
  }
}

// 返回列表
const handleBack = () => {
  router.push('/skills')
}

// 保存技能
const handleSave = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    saving.value = true

    const data = {
      name: form.name,
      category: form.category,
      proficiency: form.proficiency,
      description: form.description || undefined,
      icon: form.icon || undefined,
      order: form.order
    }

    if (isEdit.value) {
      await updateSkill(skillId.value, data as SkillUpdate)
      ElMessage.success('技能更新成功')
    } else {
      await createSkill(data as SkillCreate)
      ElMessage.success('技能创建成功')
    }

    // 返回列表页
    setTimeout(() => {
      router.push('/skills')
    }, 1000)
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  // 检查是否为编辑模式
  if (route.params.id) {
    isEdit.value = true
    skillId.value = route.params.id as string
    loadSkill()
  }
})
</script>

<style scoped>
.skill-editor {
  min-height: 100vh;
  background: var(--bg-primary);
  padding: 2rem;
  transition: background-color 0.3s ease;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-left h1 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-primary);
  font-weight: 600;
  transition: color 0.3s ease;
}

.header-right {
  display: flex;
  gap: 1rem;
}

.editor-form {
  max-width: 1200px;
  margin: 0 auto;
}

.form-card {
  margin-bottom: 1.5rem;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.form-card :deep(.el-card__body) {
  padding: 2rem;
}

:deep(.el-form-item__label) {
  color: var(--text-primary);
  font-weight: 500;
}

:deep(.el-input__inner) {
  background-color: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-primary);
}

:deep(.el-textarea__inner) {
  background-color: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-primary);
}

:deep(.el-select__wrapper) {
  background-color: var(--bg-secondary);
  border-color: var(--border-color);
}

@media (max-width: 768px) {
  .skill-editor {
    padding: 1rem;
  }

  .editor-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .header-left {
    width: 100%;
  }

  .header-right {
    width: 100%;
    justify-content: flex-end;
  }

  .header-left h1 {
    font-size: 1.25rem;
  }
}
</style>
