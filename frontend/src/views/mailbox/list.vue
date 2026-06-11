<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:inbox text-18" /> 我的邮箱</span>
      </template>
      <div v-if="loading" class="flex justify-center py-40">
        <n-spin size="large" />
      </div>
      <div v-else-if="!mailboxes.length" class="py-40 text-center">
        <n-empty description="暂无邮箱">
          <template #extra>
            <n-button type="primary" @click="$router.push('/mailbox-apply')">
              申请邮箱
            </n-button>
          </template>
        </n-empty>
      </div>
      <div v-else class="grid grid-cols-1 gap-12 lg:grid-cols-3 md:grid-cols-2">
        <n-card v-for="mb in mailboxes" :key="mb.id" hoverable>
          <div class="flex items-center gap-12">
            <n-avatar round :size="48" class="flex-shrink-0 bg-primary/10 text-primary">
              <i class="i-fe:mail text-20" />
            </n-avatar>
            <div class="flex-1 overflow-hidden">
              <div class="truncate text-16 font-bold">
                {{ mb.address }}
              </div>
              <div class="mt-4 truncate text-12 opacity-50">
                {{ mb.display_name || '未设置显示名称' }}
              </div>
            </div>
          </div>
          <div class="mt-16 flex items-center justify-between">
            <n-tag :type="mb.is_active ? 'success' : 'default'" size="small" round>
              {{ mb.is_active ? '活跃' : '已停用' }}
            </n-tag>
            <span class="text-12 opacity-40">
              {{ mb.created_at?.replace('T', ' ').slice(0, 10) }}
            </span>
          </div>
        </n-card>
      </div>
    </n-card>
  </AppPage>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getMyMailboxes } from '@/api/wicmail'
import { AppPage } from '@/components'

const loading = ref(false)
const mailboxes = ref([])

onMounted(async () => {
  loading.value = true
  try {
    const res = await getMyMailboxes()
    const data = res.data || res
    mailboxes.value = Array.isArray(data) ? data : (data.mailboxes || [])
  }
  catch (err) {
    console.error('加载邮箱列表失败:', err)
  }
  finally {
    loading.value = false
  }
})
</script>
