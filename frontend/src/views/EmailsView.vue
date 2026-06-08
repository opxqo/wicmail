<template>
  <div class="page-stack">
    <el-card class="panel-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>邮件列表</span>
          <el-button :icon="Refresh" @click="loadEmails">刷新</el-button>
        </div>
      </template>

      <el-table :data="emails" class="data-table" @row-click="openEmail">
        <el-table-column width="52">
          <template #default="{ row }">
            <span :class="['read-dot', { unread: !row.is_read }]"></span>
          </template>
        </el-table-column>
        <el-table-column prop="subject" label="主题" min-width="220" />
        <el-table-column prop="header_from" label="发件人" min-width="220" />
        <el-table-column prop="mailbox_address" label="收件邮箱" min-width="180" />
        <el-table-column label="附件" width="90">
          <template #default="{ row }">{{ row.attachment_count || 0 }}</template>
        </el-table-column>
        <el-table-column prop="received_at" label="接收时间" min-width="180" />
      </el-table>

      <div class="pagination-row">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          layout="prev, pager, next"
          :total="total"
          @current-change="loadEmails"
        />
      </div>
    </el-card>

    <el-drawer v-model="drawerVisible" size="min(720px, 100%)" :title="selectedEmail?.subject || '邮件详情'">
      <div v-if="selectedEmail" class="email-detail">
        <dl>
          <div><dt>发件人</dt><dd>{{ selectedEmail.header_from }}</dd></div>
          <div><dt>收件人</dt><dd>{{ selectedEmail.header_to }}</dd></div>
          <div><dt>接收时间</dt><dd>{{ selectedEmail.received_at }}</dd></div>
        </dl>

        <div class="email-body">{{ selectedEmail.body_text || '暂无纯文本正文' }}</div>

        <el-divider>附件</el-divider>
        <el-empty v-if="selectedEmail.attachments?.length === 0" description="无附件" />
        <el-tag v-for="attachment in selectedEmail.attachments" :key="attachment.id" class="attachment-tag">
          {{ attachment.filename }}
        </el-tag>

        <div class="drawer-actions">
          <el-button v-if="selectedEmail.is_read" @click="markUnread(selectedEmail)">标记未读</el-button>
          <el-button v-else type="primary" @click="markRead(selectedEmail)">标记已读</el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { api } from '@/services/http'

const emails = ref([])
const selectedEmail = ref(null)
const drawerVisible = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

async function loadEmails() {
  const data = await api.listEmails({ page: page.value, page_size: pageSize.value })
  emails.value = data.emails
  total.value = data.total
}

async function openEmail(row) {
  selectedEmail.value = await api.getEmail(row.id)
  drawerVisible.value = true
}

async function markRead(email) {
  await api.markRead(email.id)
  email.is_read = true
  await loadEmails()
}

async function markUnread(email) {
  await api.markUnread(email.id)
  email.is_read = false
  await loadEmails()
}

onMounted(loadEmails)
</script>
