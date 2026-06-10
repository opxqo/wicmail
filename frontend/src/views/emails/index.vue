<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:inbox text-18" /> 邮件中心</span>
      </template>
      <n-data-table
        :columns="columns"
        :data="emails"
        :loading="loading"
        :pagination="pagination"
        :row-props="rowProps"
        remote
        @update:page="handlePageChange"
      />
    </n-card>

    <!-- 邮件详情抽屉 -->
    <n-drawer v-model:show="drawerVisible" :width="680" placement="right">
      <n-drawer-content v-if="currentEmail" :title="currentEmail.subject || '(无主题)'" closable>
        <div class="email-meta">
          <div class="meta-row">
            <span class="meta-label">发件人：</span>
            <span>{{ currentEmail.header_from }}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">收件人：</span>
            <span>{{ currentEmail.header_to || currentEmail.envelope_to }}</span>
          </div>
          <div v-if="currentEmail.header_cc" class="meta-row">
            <span class="meta-label">抄送：</span>
            <span>{{ currentEmail.header_cc }}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">时间：</span>
            <span>{{ currentEmail.received_at?.replace('T', ' ').slice(0, 19) }}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">邮箱：</span>
            <n-tag size="small" type="info" round>{{ currentEmail.mailbox_address }}</n-tag>
          </div>
        </div>

        <n-divider />

        <!-- 邮件正文 -->
        <div v-if="currentEmail.body_html" class="email-body" v-html="currentEmail.body_html" />
        <pre v-else class="email-body-text">{{ currentEmail.body_text }}</pre>

        <!-- 附件 -->
        <template v-if="currentEmail.attachments?.length">
          <n-divider />
          <h4 class="flex items-center gap-8"><i class="i-fe:paperclip text-16" /> 附件 ({{ currentEmail.attachments.length }})</h4>
          <div class="mt-8 flex flex-col gap-8">
            <div v-for="att in currentEmail.attachments" :key="att.id" class="flex items-center justify-between rounded-8 bg-gray-100 p-12">
              <div class="flex items-center gap-8">
                <i class="i-fe:file-text text-16" />
                <span class="text-14">{{ att.filename }}</span>
              </div>
              <span class="text-12 opacity-50">{{ formatSize(att.size) }}</span>
            </div>
          </div>
        </template>

        <template #footer>
          <n-button
            :type="currentEmail.is_read ? 'default' : 'primary'"
            ghost
            @click="toggleRead"
          >
            {{ currentEmail.is_read ? '标记未读' : '标记已读' }}
          </n-button>
        </template>
      </n-drawer-content>
    </n-drawer>
  </AppPage>
</template>

<script setup>
import { h, ref, onMounted } from 'vue'
import { NTag } from 'naive-ui'
import { AppPage } from '@/components'
import { mockApi, isMock } from '@/mock/data'

const loading = ref(false)
const emails = ref([])
const drawerVisible = ref(false)
const currentEmail = ref(null)

const pagination = reactive({
  page: 1,
  pageSize: 20,
  pageCount: 1,
  itemCount: 0,
  showSizePicker: false,
  onUpdatePage: handlePageChange,
})

const columns = [
  {
    title: '状态',
    key: 'is_read',
    width: 70,
    render(row) {
      return h(NTag, {
        type: row.is_read ? 'default' : 'info',
        size: 'small',
        round: true,
      }, { default: () => row.is_read ? '已读' : '未读' })
    },
  },
  { title: '发件人', key: 'header_from', width: 180, ellipsis: { tooltip: true } },
  { title: '主题', key: 'subject', ellipsis: { tooltip: true }, render: row => row.subject || '(无主题)' },
  {
    title: '收件箱',
    key: 'mailbox_address',
    width: 180,
    ellipsis: { tooltip: true },
  },
  {
    title: '附件',
    key: 'attachment_count',
    width: 70,
    render(row) {
      if (row.attachment_count <= 0) return ''
      return h('span', { class: 'flex items-center gap-2' }, [
        h('i', { class: 'i-fe:paperclip text-14' }),
        String(row.attachment_count),
      ])
    },
  },
  {
    title: '时间',
    key: 'received_at',
    width: 160,
    render: row => row.received_at?.replace('T', ' ').slice(0, 16) || '-',
  },
]

function rowProps(row) {
  return {
    style: { cursor: 'pointer' },
    onClick: () => openEmail(row),
  }
}

async function openEmail(row) {
  if (isMock()) {
    const res = await mockApi.getEmailDetail(row.id)
    currentEmail.value = res.data
    drawerVisible.value = true
    if (!row.is_read) {
      await mockApi.markEmailRead(row.id)
      row.is_read = true
    }
  }
}

async function toggleRead() {
  if (!currentEmail.value || !isMock()) return
  if (currentEmail.value.is_read) {
    await mockApi.markEmailUnread(currentEmail.value.id)
    currentEmail.value.is_read = false
  }
  else {
    await mockApi.markEmailRead(currentEmail.value.id)
    currentEmail.value.is_read = true
  }
  // 同步列表中的状态
  const item = emails.value.find(e => e.id === currentEmail.value.id)
  if (item) item.is_read = currentEmail.value.is_read
}

function handlePageChange(page) {
  pagination.page = page
  loadEmails()
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

async function loadEmails() {
  loading.value = true
  try {
    if (isMock()) {
      const res = await mockApi.getEmails({ page: pagination.page, page_size: pagination.pageSize })
      emails.value = res.data.emails
      pagination.itemCount = res.data.total
      pagination.pageCount = Math.ceil(res.data.total / pagination.pageSize)
    }
  }
  finally {
    loading.value = false
  }
}

onMounted(() => loadEmails())
</script>

<style scoped>
.email-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.meta-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}
.meta-label {
  color: #64748b;
  min-width: 60px;
  flex-shrink: 0;
}
.email-body {
  padding: 16px 0;
  overflow-x: auto;
}
.email-body-text {
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.6;
}
</style>
