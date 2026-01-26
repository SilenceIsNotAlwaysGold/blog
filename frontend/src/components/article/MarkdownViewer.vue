<template>
  <div ref="viewerRef" class="markdown-viewer"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import Vditor from 'vditor'
import 'vditor/dist/index.css'

interface Props {
  content: string
  theme?: 'classic' | 'dark'
}

const props = withDefaults(defineProps<Props>(), {
  content: '',
  theme: 'classic'
})

const viewerRef = ref<HTMLDivElement>()

const renderMarkdown = () => {
  if (!viewerRef.value) return

  Vditor.preview(viewerRef.value, props.content, {
    mode: 'light',
    theme: {
      current: props.theme
    },
    hljs: {
      style: 'github'
    }
  })
}

onMounted(() => {
  renderMarkdown()
})

watch(() => props.content, () => {
  renderMarkdown()
})

watch(() => props.theme, () => {
  renderMarkdown()
})
</script>

<style scoped>
.markdown-viewer {
  width: 100%;
  padding: 1rem;
  background: #fff;
  border-radius: 4px;
}

:deep(.vditor-reset) {
  font-size: 16px;
  line-height: 1.8;
}

:deep(.vditor-reset h1) {
  font-size: 2em;
  margin-top: 1em;
  margin-bottom: 0.5em;
}

:deep(.vditor-reset h2) {
  font-size: 1.5em;
  margin-top: 1em;
  margin-bottom: 0.5em;
}

:deep(.vditor-reset h3) {
  font-size: 1.25em;
  margin-top: 1em;
  margin-bottom: 0.5em;
}

:deep(.vditor-reset pre) {
  background: #f6f8fa;
  border-radius: 4px;
  padding: 1rem;
  overflow-x: auto;
}

:deep(.vditor-reset code) {
  background: #f6f8fa;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: 'Courier New', Courier, monospace;
}

:deep(.vditor-reset blockquote) {
  border-left: 4px solid #dfe2e5;
  padding-left: 1rem;
  color: #6a737d;
}

:deep(.vditor-reset img) {
  max-width: 100%;
  height: auto;
}
</style>
