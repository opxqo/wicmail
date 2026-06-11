<template>
  <AppPage show-footer>
    <n-card>
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:plus-circle text-18" /> 申请新邮箱</span>
      </template>
      <n-form ref="formRef" :model="form" :rules="rules" label-placement="left" label-width="100">
        <n-form-item label="邮箱前缀" path="prefix">
          <n-input v-model:value="form.prefix" placeholder="输入前缀，如 zhangsan" :maxlength="30">
            <template #suffix>
              <span class="opacity-50">@wic.edu.kg</span>
            </template>
          </n-input>
        </n-form-item>
        <n-form-item label="显示名称" path="display_name">
          <n-input v-model:value="form.display_name" placeholder="可选，如：张三的邮箱" />
        </n-form-item>
        <n-form-item label="申请理由" path="reason">
          <n-input v-model:value="form.reason" type="textarea" placeholder="可选，说明申请原因" :rows="3" />
        </n-form-item>

        <!-- 主要材料上传（拖拽上传 + 图片预览） -->
        <n-form-item label="证明材料">
          <div class="w-full">
            <n-alert type="info" class="mb-12" :bordered="false">
              <template #icon>
                <i class="i-fe:info text-16" />
              </template>
              请上传学生证、校园卡或录取通知书等材料，辅助管理员验证申请的合规性。支持 JPG / PNG 图片格式，单文件不超过 10MB，最多 5 张。
            </n-alert>

            <n-upload
              :custom-request="handleImageUpload"
              :show-file-list="false"
              accept=".png,.jpg,.jpeg"
              :max="5"
              @before-upload="onBeforeImageUpload"
            >
              <n-upload-dragger>
                <div class="h-120 f-c-c flex-col">
                  <i class="i-fe:upload-cloud mb-12 text-48 color-primary" />
                  <n-text class="text-14 color-gray">
                    点击或拖动图片到此处上传
                  </n-text>
                  <n-text class="mt-4 text-12 opacity-40">
                    已上传 {{ imageList.length }} / 5 张
                  </n-text>
                </div>
              </n-upload-dragger>
            </n-upload>

            <!-- 图片预览列表 -->
            <div v-if="imageList.length" class="mt-12">
              <n-image-group>
                <n-space>
                  <div v-for="(img, index) in imageList" :key="index" class="image-card">
                    <n-image width="120" height="120" :src="img.url" object-fit="cover" class="rounded-8" preview-disabled />
                    <div class="image-card-actions">
                      <NButton text type="primary" size="tiny" @click="previewImage(img)">
                        <i class="i-fe:eye text-14" />
                      </NButton>
                      <NButton text type="error" size="tiny" @click="removeImage(index)">
                        <i class="i-fe:trash-2 text-14" />
                      </NButton>
                    </div>
                    <div class="image-card-name mt-4 max-w-120px truncate text-11 opacity-60">
                      {{ img.fileName }}
                    </div>
                  </div>
                </n-space>
              </n-image-group>
            </div>
          </div>
        </n-form-item>

        <!-- 补充材料上传（按钮式，支持 PDF 等） -->
        <n-form-item label="补充材料">
          <div class="w-full">
            <n-alert type="default" class="mb-12" :bordered="false">
              <template #icon>
                <i class="i-fe:paperclip text-16" />
              </template>
              可选。如有补充说明文件（如导师审批表、院系证明等），可在此上传。支持 PDF 格式，最多 3 份。
            </n-alert>
            <n-upload
              :custom-request="handleFileUpload"
              :file-list="fileList"
              :max="3"
              accept=".pdf"
              list-type="image"
              multiple
              :on-exceed="handleFileExceed"
              :on-before-upload="onBeforeFileUpload"
            >
              <NButton type="primary" ghost>
                <template #icon>
                  <i class="i-fe:upload text-16" />
                </template>
                上传补充材料
              </NButton>
            </n-upload>
          </div>
        </n-form-item>

        <!-- 提交操作区 -->
        <n-divider />
        <div class="submit-area">
          <div class="submit-info">
            <i class="i-fe:info text-16 color-primary" />
            <span class="text-13 opacity-60">提交后管理员将审核你的申请，审核结果将通过系统通知</span>
          </div>
          <n-space>
            <NButton type="primary" :loading="submitting" :disabled="submitting" @click="handleSubmit">
              <template #icon>
                <i class="i-fe:send text-16" />
              </template>
              提交申请
            </NButton>
            <NButton :disabled="submitting" @click="handleReset">
              <template #icon>
                <i class="i-fe:refresh-ccw text-16" />
              </template>
              重置
            </NButton>
          </n-space>
        </div>
      </n-form>
    </n-card>

    <n-card class="mt-12" segmented>
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:clipboard text-18" /> 我的申请记录</span>
      </template>
      <n-data-table :columns="columns" :data="applications" :loading="loading" />
    </n-card>

    <!-- 图片大图预览 -->
    <n-modal v-model:show="imagePreviewVisible" preset="card" :title="imagePreviewName" style="max-width: 640px;">
      <div class="flex justify-center">
        <img :src="imagePreviewUrl" class="max-h-500px max-w-full rounded-8" alt="preview">
      </div>
    </n-modal>

    <!-- 附件预览弹窗 -->
    <n-modal v-model:show="previewModal.visible" preset="card" :title="previewModal.title" style="max-width: 720px;">
      <div class="preview-container">
        <div v-for="(att, i) in previewModal.attachments" :key="i" class="preview-item">
          <div class="flex items-center gap-8 text-14 font-bold">
            <i :class="getFileIcon(att.content_type)" class="text-16" />
            {{ att.filename }}
            <NTag size="tiny" :bordered="false">
              {{ formatSize(att.size) }}
            </NTag>
          </div>
          <div class="mt-8">
            <img v-if="att.url && isImage(att.content_type)" :src="att.url" class="preview-image" alt="preview">
            <div v-else-if="isImage(att.content_type)" class="preview-placeholder">
              <i class="i-fe:image text-48 opacity-20" />
              <span class="mt-8 text-12 opacity-40">图片预览（Mock 模式无实际文件）</span>
            </div>
            <div v-else class="preview-placeholder">
              <i class="i-fe:file-text text-48 opacity-20" />
              <span class="mt-8 text-12 opacity-40">PDF 文件预览（Mock 模式无实际文件）</span>
            </div>
          </div>
        </div>
      </div>
    </n-modal>
  </AppPage>
</template>

<script setup>
import { NButton, NTag } from 'naive-ui'
import { h, onMounted, ref } from 'vue'
import { applyMailbox, getMyApplications } from '@/api/wicmail'
import { AppPage } from '@/components'

const formRef = ref(null)
const submitting = ref(false)
const loading = ref(false)
const applications = ref([])

// 主材料 - 图片列表（拖拽上传）
const imageList = reactive([])
// 补充材料 - 文件列表（按钮上传）
const fileList = ref([])

const form = ref({
  prefix: '',
  display_name: '',
  reason: '',
})

const rules = {
  prefix: [
    { required: true, message: '请输入邮箱前缀' },
    { pattern: /^[a-z0-9][\w.-]{2,29}$/i, message: '只能包含字母、数字、点、横杠、下划线，3-30字符' },
  ],
}

const statusMap = {
  pending: { label: '待审核', type: 'warning' },
  approved: { label: '已批准', type: 'success' },
  rejected: { label: '已拒绝', type: 'error' },
}

// 大图预览
const imagePreviewVisible = ref(false)
const imagePreviewUrl = ref('')
const imagePreviewName = ref('')

// 附件弹窗
const previewModal = reactive({
  visible: false,
  title: '',
  attachments: [],
})

function isImage(contentType) {
  return contentType?.startsWith('image/')
}

function getFileIcon(contentType) {
  if (isImage(contentType))
    return 'i-fe:image'
  if (contentType?.includes('pdf'))
    return 'i-fe:file-text'
  return 'i-fe:file'
}

function formatSize(bytes) {
  if (!bytes)
    return '0 B'
  if (bytes < 1024)
    return `${bytes} B`
  if (bytes < 1024 * 1024)
    return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

// ========== 主材料图片上传 ==========
function onBeforeImageUpload({ file }) {
  if (!file.file?.type.startsWith('image/')) {
    $message.error('只能上传图片文件（JPG / PNG）')
    return false
  }
  if (file.file.size > 10 * 1024 * 1024) {
    $message.error(`文件 ${file.name} 超过 10MB 限制`)
    return false
  }
  if (imageList.length >= 5) {
    $message.warning('最多上传 5 张图片')
    return false
  }
  return true
}

function handleImageUpload({ file, onFinish }) {
  if (!file?.file) {
    $message.error('请选择文件')
    return
  }
  $message.loading('上传中...', { key: 'img-upload' })
  setTimeout(() => {
    const url = URL.createObjectURL(file.file)
    imageList.push({ fileName: file.name, url, file: file.file })
    $message.success('上传成功', { key: 'img-upload' })
    onFinish()
  }, 800)
}

function removeImage(index) {
  URL.revokeObjectURL(imageList[index].url)
  imageList.splice(index, 1)
}

function previewImage(img) {
  imagePreviewUrl.value = img.url
  imagePreviewName.value = img.fileName
  imagePreviewVisible.value = true
}

// ========== 补充材料文件上传 ==========
function onBeforeFileUpload({ file }) {
  if (file.file?.size > 10 * 1024 * 1024) {
    $message.error(`文件 ${file.name} 超过 10MB 限制`)
    return false
  }
  return true
}

function handleFileUpload({ file, onFinish }) {
  const rawFile = file.file
  if (rawFile) {
    const reader = new FileReader()
    reader.onload = (e) => {
      file.url = e.target.result
      onFinish()
    }
    reader.readAsDataURL(rawFile)
  }
  else {
    onFinish()
  }
}

function handleFileExceed() {
  $message.warning('最多上传 3 份补充材料')
}

// ========== 查看历史申请附件 ==========
function showAttachments(row) {
  if (!row.attachments?.length)
    return
  previewModal.title = `申请材料 - ${row.requested_address}`
  previewModal.attachments = row.attachments
  previewModal.visible = true
}

const columns = [
  { title: '申请地址', key: 'requested_address', ellipsis: { tooltip: true } },
  { title: '显示名称', key: 'display_name', render: row => row.display_name || '-', width: 130 },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render(row) {
      const s = statusMap[row.status] || { label: row.status, type: 'default' }
      return h(NTag, { type: s.type, size: 'small', round: true }, { default: () => s.label })
    },
  },
  {
    title: '材料',
    key: 'attachments',
    width: 110,
    render(row) {
      const count = row.attachments?.length || 0
      if (!count)
        return h('span', { class: 'opacity-40' }, '无')
      return h(NButton, { size: 'small', text: true, type: 'primary', onClick: () => showAttachments(row) }, {
        icon: () => h('i', { class: 'i-fe:paperclip text-14' }),
        default: () => `${count} 份材料`,
      })
    },
  },
  { title: '申请理由', key: 'reason', ellipsis: { tooltip: true }, render: row => row.reason || '-' },
  { title: '审核备注', key: 'review_comment', ellipsis: { tooltip: true }, render: row => row.review_comment || '-' },
  {
    title: '申请时间',
    key: 'created_at',
    width: 160,
    render: row => row.created_at?.replace('T', ' ').slice(0, 16) || '-',
  },
]

function handleReset() {
  form.value = { prefix: '', display_name: '', reason: '' }
  imageList.splice(0, imageList.length)
  fileList.value = []
  formRef.value?.restoreValidation()
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
  }
  catch { return }
  submitting.value = true
  try {
    // 收集主材料图片
    const images = imageList.map(img => ({
      name: img.fileName,
      type: img.file?.type || 'image/jpeg',
      size: img.file?.size || 0,
      url: img.url || null,
    }))
    // 收集补充材料文件
    const files = fileList.value
      .filter(f => f.status === 'finished')
      .map(f => ({
        name: f.name,
        type: f.type || 'application/pdf',
        size: f.file?.size || 0,
        url: f.url || null,
      }))

    await applyMailbox({
      ...form.value,
      attachments: [...images, ...files],
    })
    $message.success('申请已提交，等待审核')
    form.value = { prefix: '', display_name: '', reason: '' }
    imageList.splice(0, imageList.length)
    fileList.value = []
    await loadApplications()
  }
  catch (err) {
    $message.error(err.message || '申请失败')
  }
  submitting.value = false
}

async function loadApplications() {
  loading.value = true
  try {
    const res = await getMyApplications()
    const data = res.data || res
    applications.value = data.applications || (Array.isArray(data) ? data : [])
  }
  catch (err) {
    console.error('加载申请记录失败:', err)
  }
  finally {
    loading.value = false
  }
}

onMounted(() => loadApplications())
</script>

<style scoped>
.image-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.image-card-actions {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}
.submit-area {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 0 0;
}
.submit-info {
  display: flex;
  align-items: center;
  gap: 6px;
}
.preview-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 65vh;
  overflow-y: auto;
}
.preview-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
}
.preview-image {
  max-width: 100%;
  max-height: 400px;
  border-radius: 6px;
  object-fit: contain;
}
.preview-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: #f8fafc;
  border-radius: 6px;
}
</style>
