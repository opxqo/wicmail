<template>
  <AppPage show-footer>
    <div class="flex">
      <n-card class="min-w-200 w-30%">
        <div class="flex items-center">
          <n-avatar round :size="60" :src="userStore.avatar" class="flex-shrink-0">
            {{ (userStore.nickName ?? userStore.username)?.charAt(0) }}
          </n-avatar>
          <div class="ml-20 flex-col">
            <span class="text-20 opacity-80">
              你好，{{ userStore.nickName ?? userStore.username }}
            </span>
            <span class="mt-4 opacity-50">{{ userStore.currentRole?.name }}</span>
          </div>
        </div>
        <p class="mt-28 text-14 opacity-60">
          WicMail 校园邮箱，让沟通更简单。
        </p>
      </n-card>
      <n-card class="ml-12 w-70%">
        <template #header>
          <span class="flex items-center gap-8"><i class="i-fe:layout text-18" /> 工作台概览</span>
        </template>
        <p class="opacity-60">
          在这里管理你的校园邮箱、查看邮件和处理申请。
        </p>
        <footer class="mt-12 flex items-center justify-end">
          <n-button type="primary" ghost @click="$router.push('/mailbox-apply')">
            申请新邮箱
          </n-button>
          <n-button type="primary" class="ml-12" @click="$router.push('/emails')">
            查看邮件
          </n-button>
        </footer>
      </n-card>
    </div>

    <!-- 统计卡片 -->
    <div class="mt-12 grid grid-cols-4 gap-12">
      <n-card v-for="item in statCards" :key="item.label" class="text-center">
        <n-statistic :label="item.label" :value="item.value">
          <template #prefix>
            <i :class="item.icon" class="text-18" />
          </template>
        </n-statistic>
      </n-card>
    </div>

    <!-- 最近邮件 & 我的邮箱 -->
    <div class="mt-12 flex gap-12">
      <n-card class="w-60%" segmented>
        <template #header>
          <span class="flex items-center gap-8"><i class="i-fe:inbox text-18" /> 最近邮件</span>
        </template>
        <n-data-table
          :columns="emailColumns"
          :data="recentEmails"
          :bordered="false"
          size="small"
        />
      </n-card>
      <n-card class="w-40%" segmented>
        <template #header>
          <span class="flex items-center gap-8"><i class="i-fe:mail text-18" /> 我的邮箱</span>
        </template>
        <div v-for="mb in myMailboxes" :key="mb.id" class="mb-8 flex items-center justify-between rounded-8 bg-gray-100 p-12">
          <div>
            <div class="text-14 font-bold">{{ mb.address }}</div>
            <div class="mt-2 text-12 opacity-50">{{ mb.display_name }}</div>
          </div>
          <n-tag type="success" size="small" round>活跃</n-tag>
        </div>
        <n-empty v-if="!myMailboxes.length" description="暂无邮箱" />
      </n-card>
    </div>
  </AppPage>
</template>

<script setup>
import { h, ref, onMounted } from 'vue'
import { NTag } from 'naive-ui'
import { AppPage } from '@/components'
import { useUserStore } from '@/store'
import { mockApi, isMock } from '@/mock/data'

const userStore = useUserStore()

const recentEmails = ref([])
const myMailboxes = ref([])

const statCards = ref([
  { label: '我的邮箱', value: 0, icon: 'i-fe:mail' },
  { label: '总邮件数', value: 0, icon: 'i-fe:inbox' },
  { label: '未读邮件', value: 0, icon: 'i-fe:bell' },
  { label: '待审申请', value: 0, icon: 'i-fe:clock' },
])

const emailColumns = [
  { title: '发件人', key: 'header_from', ellipsis: { tooltip: true } },
  { title: '主题', key: 'subject', ellipsis: { tooltip: true } },
  {
    title: '状态',
    key: 'is_read',
    width: 80,
    render(row) {
      return h(NTag, { type: row.is_read ? 'default' : 'info', size: 'small', round: true }, { default: () => row.is_read ? '已读' : '未读' })
    },
  },
  {
    title: '时间',
    key: 'received_at',
    width: 160,
    render(row) {
      return row.received_at?.replace('T', ' ').slice(0, 16) || '-'
    },
  },
]

onMounted(async () => {
  if (isMock()) {
    const [emailRes, mbRes] = await Promise.all([
      mockApi.getEmails({ page: 1, page_size: 5 }),
      mockApi.getMyMailboxes(),
    ])
    recentEmails.value = emailRes.data.emails
    myMailboxes.value = mbRes.data
    statCards.value[0].value = mbRes.data.length
    statCards.value[1].value = emailRes.data.total
    statCards.value[2].value = emailRes.data.emails.filter(e => !e.is_read).length
    statCards.value[3].value = 1
  }
})
</script>
