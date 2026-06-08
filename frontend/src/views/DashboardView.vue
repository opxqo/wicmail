<template>
  <div class="page-stack">
    <div class="stat-grid">
      <el-card v-for="item in stats" :key="item.label" class="stat-card" shadow="never">
        <div class="stat-icon">
          <el-icon><component :is="item.icon" /></el-icon>
        </div>
        <div>
          <p>{{ item.label }}</p>
          <strong>{{ item.value }}</strong>
        </div>
      </el-card>
    </div>

    <div class="content-grid">
      <el-card class="panel-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span>邮箱状态</span>
            <router-link to="/app/mailboxes">管理</router-link>
          </div>
        </template>
        <el-empty v-if="mailboxes.length === 0" description="暂无已开通邮箱" />
        <div v-else class="mailbox-list">
          <article v-for="mailbox in mailboxes" :key="mailbox.id" class="mailbox-row">
            <div>
              <strong>{{ mailbox.address }}</strong>
              <p>{{ mailbox.display_name || '校园邮箱' }}</p>
            </div>
            <el-tag :type="mailbox.is_active ? 'success' : 'info'">{{ mailbox.is_active ? '可用' : '停用' }}</el-tag>
          </article>
        </div>
      </el-card>

      <el-card class="panel-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span>最近邮件</span>
            <router-link to="/app/emails">查看全部</router-link>
          </div>
        </template>
        <div class="compact-list">
          <article v-for="email in emails" :key="email.id">
            <span :class="['read-dot', { unread: !email.is_read }]"></span>
            <div>
              <strong>{{ email.subject || '无主题邮件' }}</strong>
              <p>{{ email.header_from }}</p>
            </div>
          </article>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { api } from '@/services/http'

const mailboxes = ref([])
const emails = ref([])

const stats = computed(() => [
  { label: '已开通邮箱', value: mailboxes.value.length, icon: 'Postcard' },
  { label: '最近邮件', value: emails.value.length, icon: 'Tickets' },
  { label: '未读邮件', value: emails.value.filter((item) => !item.is_read).length, icon: 'Bell' },
])

onMounted(async () => {
  const [mailboxData, emailData] = await Promise.all([
    api.listMailboxes(),
    api.listEmails({ page: 1, page_size: 5 }),
  ])
  mailboxes.value = mailboxData
  emails.value = emailData.emails
})
</script>
