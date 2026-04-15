<template>
  <div class="project-editor">
    <div class="editor-header">
      <div class="header-left">
        <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
        <h1>{{ isEdit ? '编辑项目' : '新建项目' }}</h1>
      </div>
      <div class="header-right">
        <el-button @click="handleSave" :loading="saving" type="primary">
          {{ isEdit ? '更新项目' : '创建项目' }}
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
        <el-form-item label="项目名称" prop="name">
          <el-input
            v-model="form.name"
            placeholder="请输入项目名称"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入项目描述"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="项目状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
                <el-option label="Completed" value="completed" />
                <el-option label="In Progress" value="in_progress" />
                <el-option label="Planned" value="planned" />
              </el-select>
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

        <el-form-item label="技术栈" prop="tech_stack">
          <el-select
            v-model="form.tech_stack"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请输入技术栈，按回车添加"
            style="width: 100%"
          >
          </el-select>
        </el-form-item>

        <el-form-item label="封面图片" prop="cover_image">
          <el-input
            v-model="form.cover_image"
            placeholder="请输入封面图片 URL（可选）"
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Demo URL" prop="demo_url">
              <el-input
                v-model="form.demo_url"
                placeholder="请输入 Demo URL（可选）"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="GitHub URL" prop="github_url">
              <el-input
                v-model="form.github_url"
                placeholder="请输入 GitHub URL（可选）"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始日期" prop="start_date">
              <el-date-picker
                v-model="form.start_date"
                type="date"
                placeholder="选择开始日期"
                style="width: 100%"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束日期" prop="end_date">
              <el-date-picker
                v-model="form.end_date"
                type="date"
                placeholder="选择结束日期"
                style="width: 100%"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="项目亮点" prop="highlights">
          <el-select
            v-model="form.highlights"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请输入项目亮点，按回车添加"
            style="width: 100%"
          >
          </el-select>
        </el-form-item>
      </el-card>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { createProject, updateProject, getProject, type ProjectCreate, type ProjectUpdate } from '@/api/project'

const route = useRoute()
const router = useRouter()

const formRef = ref<FormInstance>()
const saving = ref(false)
const isEdit = ref(false)
const projectId = ref('')

const form = reactive({
  name: '',
  description: '',
  tech_stack: [] as string[],
  cover_image: '',
  demo_url: '',
  github_url: '',
  start_date: '',
  end_date: '',
  status: 'planned' as 'completed' | 'in_progress' | 'planned',
  highlights: [] as string[],
  order: 0
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 100, message: '名称长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入项目描述', trigger: 'blur' }
  ],
  tech_stack: [
    { required: true, message: '请至少添加一个技术栈', trigger: 'change', type: 'array', min: 1 }
  ],
  status: [
    { required: true, message: '请选择项目状态', trigger: 'change' }
  ]
}

// 加载项目数据（编辑模式）
const loadProject = async () => {
  try {
    const response = await getProject(projectId.value)
    const project = response.data

    form.name = project.name
    form.description = project.description
    form.tech_stack = project.tech_stack || []
    form.cover_image = project.cover_image || ''
    form.demo_url = project.demo_url || ''
    form.github_url = project.github_url || ''
    form.start_date = project.start_date || ''
    form.end_date = project.end_date || ''
    form.status = project.status
    form.highlights = project.highlights || []
    form.order = project.order
  } catch (error: any) {
    ElMessage.error(error.message || '加载项目失败')
    router.push('/projects')
  }
}

// 返回列表
const handleBack = () => {
  router.push('/projects')
}

// 保存项目
const handleSave = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    saving.value = true

    const data = {
      name: form.name,
      description: form.description,
      tech_stack: form.tech_stack,
      cover_image: form.cover_image || undefined,
      demo_url: form.demo_url || undefined,
      github_url: form.github_url || undefined,
      start_date: form.start_date || undefined,
      end_date: form.end_date || undefined,
      status: form.status,
      highlights: form.highlights.length > 0 ? form.highlights : undefined,
      order: form.order
    }

    if (isEdit.value) {
      await updateProject(projectId.value, data as ProjectUpdate)
      ElMessage.success('项目更新成功')
    } else {
      await createProject(data as ProjectCreate)
      ElMessage.success('项目创建成功')
    }

    // 返回列表页
    setTimeout(() => {
      router.push('/projects')
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
    projectId.value = route.params.id as string
    loadProject()
  }
})
</script>

<style scoped>
.project-editor {
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
  .project-editor {
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

