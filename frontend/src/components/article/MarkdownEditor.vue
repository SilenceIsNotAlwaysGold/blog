<template>
  <div class="markdown-editor">
    <div ref="editorRef" class="vditor-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import Vditor from 'vditor'
import 'vditor/dist/index.css'

interface Props {
  modelValue: string
  placeholder?: string
  height?: string
  mode?: 'wysiwyg' | 'ir' | 'sv'
  toolbar?: Array<string | any>
}

interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'change', value: string): void
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: 'Enter content here...',
  height: '500px',
  mode: 'wysiwyg',
  toolbar: () => [
    'emoji',
    'headings',
    'bold',
    'italic',
    'strike',
    'link',
    '|',
    'list',
    'ordered-list',
    'check',
    'outdent',
    'indent',
    '|',
    'quote',
    'line',
    'code',
    'inline-code',
    'insert-before',
    'insert-after',
    '|',
    'upload',
    'table',
    '|',
    'undo',
    'redo',
    '|',
    'fullscreen',
    'edit-mode',
    {
      name: 'more',
      toolbar: [
        'both',
        'code-theme',
        'content-theme',
        'export',
        'outline',
        'preview',
        'devtools',
        'info',
        'help',
      ],
    }
  ]
})

const emit = defineEmits<Emits>()

const editorRef = ref<HTMLElement>()
let vditor: Vditor | null = null

onMounted(() => {
  if (!editorRef.value) return

  vditor = new Vditor(editorRef.value, {
    height: props.height,
    mode: props.mode,
    placeholder: props.placeholder,
    toolbar: props.toolbar,
    cache: {
      enable: false
    },
    after: () => {
      if (vditor && props.modelValue) {
        vditor.setValue(props.modelValue)
      }
    },
    input: (value: string) => {
      emit('update:modelValue', value)
      emit('change', value)
    },
    upload: {
      url: '/api/v1/upload/image',
      fieldName: 'file',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      },
      format(files, responseText) {
        const response = JSON.parse(responseText)
        if (response.code === 200) {
          return JSON.stringify({
            msg: '',
            code: 0,
            data: {
              errFiles: [],
              succMap: {
                [files[0].name]: response.data.url
              }
            }
          })
        }
        return JSON.stringify({
          msg: response.message || 'Upload failed',
          code: 1,
          data: {
            errFiles: [files[0].name],
            succMap: {}
          }
        })
      }
    }
  })
})

onBeforeUnmount(() => {
  if (vditor) {
    vditor.destroy()
    vditor = null
  }
})

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  if (vditor && newValue !== vditor.getValue()) {
    vditor.setValue(newValue)
  }
})

// Expose methods
const getValue = () => {
  return vditor?.getValue() || ''
}

const setValue = (value: string) => {
  vditor?.setValue(value)
}

const focus = () => {
  vditor?.focus()
}

defineExpose({
  getValue,
  setValue,
  focus
})
</script>

<style scoped>
.markdown-editor {
  width: 100%;
}

.vditor-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

:deep(.vditor) {
  border: none;
}
</style>
