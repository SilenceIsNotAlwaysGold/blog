<template>
  <div class="about-editor">
    <div class="editor-header">
      <div class="header-left">
        <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
        <h1>编辑 About 页面</h1>
      </div>
      <div class="header-right">
        <el-button @click="handleSave" :loading="saving" type="primary">
          保存更新
        </el-button>
      </div>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      class="editor-form"
    >
      <el-card shadow="never" class="form-card">
        <el-form-item label="页面内容" prop="content">
          <MarkdownEditor
            v-model="form.content"
            height="600px"
            placeholder="请输入 About 页面内容（支持 Markdown）..."
          />
        </el-form-item>
      </el-card>
    </el-form>

    <el-card shadow="never" class="info-card">
      <h3>提示</h3>
      <ul>
        <li>支持 Markdown 语法，可以使用标题、列表、链接、图片等</li>
        <li>建议包含个人简介、技能专长、工作经历、教育背景等信息</li>
        <li>可以添加社交媒体链接和联系方式</li>
        <li>保存后将立即在 About 页面显示</li>
      </ul>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import MarkdownEditor from '@/components/article/MarkdownEditor.vue'
import { getAbout, updateAbout, type AboutUpdate } from '@/api/about'

const router = useRouter()

const formRef = ref<FormInstance>()
const saving = ref(false)

const form = reactive({
  content: ''
})

const rules: FormRules = {
  content: [
    { required: true, message: '请输入页面内容', trigger: 'blur' }
  ]
}

// 加载 About 内容
const loadAbout = async () => {
  try {
    const response = await getAbout()
    form.content = response.data.content || ''
  } catch (error: any) {
    console.error('Failed to load about content:', error)
    // 如果没有内容，使用默认模板
    form.content = `# About Me

## 个人简介

在这里介绍你自己...

## 技能专长

- 技能 1
- 技能 2
- 技能 3

## 工作经历

### 公司名称 - 职位
*时间段*

工作描述...

## 教育背景

### 学校名称 - 专业
*时间段*

教育经历...

## 联系方式

- Email: your.email@example.com
- GitHub: https://github.com/yourusername
`
  }
}

// 返回 About 页面
const handleBack = () => {
  router.push('/about')
}

// 保存内容
const handleSave = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    saving.value = true

    const data: AboutUpdate = {
      content: form.content
    }

    await updateAbout(data)
    ElMessage.success('About 页面更新成功')

    // 返回 About 页面
    setTimeout(() => {
      router.push('/about')
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
  loadAbout()
})
</script>

<style scoped>
.about-editor {
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

.info-card {
  max-width: 1200px;
  margin: 0 auto;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.info-card h3 {
  margin: 0 0 1rem 0;
  color: var(--text-primary);
  font-size: 1.1rem;
}

.info-card ul {
  margin: 0;
  padding-left: 1.5rem;
  color: var(--text-secondary);
  line-height: 1.8;
}

.info-card li {
  margin-bottom: 0.5rem;
}

:deep(.el-form-item__label) {
  color: var(--text-primary);
  font-weight: 500;
}

@media (max-width: 768px) {
  .about-editor {
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
