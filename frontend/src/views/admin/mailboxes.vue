<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <div class="w-full flex items-center justify-between">
          <span class="flex items-center gap-8"><i class="i-fe:mail text-18" /> 邮箱管理</span>
          <NButton type="primary" size="small" @click="showCreateModal = true">
            <template #icon>
              <i class="i-fe:plus" />
            </template>
            创建邮箱
          </NButton>
        </div>
      </template>

      <!-- 搜索筛选区 -->
      <div class="mb-16 flex flex-wrap items-center gap-16">
        <n-input
          v-model:value="searchParams.q"
          placeholder="搜索邮箱地址 / 描述"
          clearable
          style="width: 260px"
          @keyup.enter="handleSearch"
        />
        <n-select
          v-model:value="searchParams.is_active"
          placeholder="激活状态"
          clearable
          :options="[
            { label: '已启用', value: 'true' },
            { label: '已停用', value: 'false' },
          ]"
          style="width: 140px"
          @update:value="handleSearch"
        />
        <NButton type="primary" ghost @click="handleSearch">
          查询
        </NButton>
        <NButton ghost @click="handleReset">
          重置
        </NButton>
      </div>

      <n-data-table :columns="columns" :data="mailboxes" :loading="loading" />
    </n-card>

    <!-- 创建邮箱弹窗 -->
    <n-modal
      v-model:show="showCreateModal"
      preset="card"
      title="创建邮箱"
      style="width: 500px"
      :segmented="{ content: 'soft', footer: 'soft' }"
    >
      <n-form ref="formRef" :model="createForm" :rules="rules" label-placement="left" label-width="90">
        <n-form-item label="邮箱地址" path="address">
          <n-input v-model:value="createForm.address" placeholder="如 test@wic.edu.kg" />
        </n-form-item>
        <n-form-item label="显示名称" path="display_name">
          <n-input v-model:value="createForm.display_name" placeholder="如 测试邮箱" />
        </n-form-item>
      </n-form>
      <template #footer>
        <div class="flex justify-end gap-12">
          <NButton ghost @click="showCreateModal = false">
            取消
          </NButton>
          <NButton type="primary" :loading="submitLoading" @click="handleCreate">
            确定
          </NButton>
        </div>
      </template>
    </n-modal>

    <!-- 邮箱详情弹窗 -->
    <n-modal
      v-model:show="showDetailModal"
      preset="card"
      title="邮箱详情"
      style="width: 500px"
      :segmented="{ content: 'soft' }"
    >
      <n-descriptions bordered label-placement="left" :column="1">
        <n-descriptions-item label="邮箱地址">
          {{ currentDetail.address }}
        </n-descriptions-item>
        <n-descriptions-item label="显示名称">
          {{ currentDetail.display_name || '-' }}
        </n-descriptions-item>
        <n-descriptions-item label="所有者用户名">
          {{ currentDetail.owner_username || '-' }} (ID: {{ currentDetail.owner_user_id || '-' }})
        </n-descriptions-item>
        <n-descriptions-item label="收信数量">
          {{ currentDetail.email_count ?? 0 }} 封
        </n-descriptions-item>
        <n-descriptions-item label="未读邮件">
          <NTag :type="(currentDetail.unread_count ?? 0) > 0 ? 'warning' : 'default'" size="small">
            {{ currentDetail.unread_count ?? 0 }} 封
          </NTag>
        </n-descriptions-item>
        <n-descriptions-item label="激活状态">
          <NTag :type="currentDetail.is_active ? 'success' : 'error'" size="small">
            {{ currentDetail.is_active ? '已启用' : '已禁用' }}
          </NTag>
        </n-descriptions-item>
        <n-descriptions-item label="创建时间">
          {{ currentDetail.created_at?.replace('T', ' ').slice(0, 16) || '-' }}
        </n-descriptions-item>
      </n-descriptions>
    </n-modal>
  </AppPage>
</template>

<script setup>
import { NButton, NPopconfirm, NSpace, NTag } from 'naive-ui'
import { h, onMounted, ref } from 'vue'
import {
  createAdminMailbox,
  deleteMailbox,
  getAdminMailboxDetail,
  getAdminMailboxes,
  toggleMailboxActive,
} from '@/api/wicmail'
import { AppPage } from '@/components'

const loading = ref(false)
const submitLoading = ref(false)
const mailboxes = ref([])

const searchParams = ref({
  q: '',
  is_active: null,
})

// 创建表单
const showCreateModal = ref(false)
const formRef = ref(null)
const createForm = ref({
  address: '',
  display_name: '',
})
const rules = {
  address: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    {
      validator(rule, value) {
        if (value && !value.endsWith('@wic.edu.kg')) {
          return new Error('邮箱必须以 @wic.edu.kg 结尾')
        }
        return true
      },
      trigger: 'blur',
    },
  ],
}

// 详情
const showDetailModal = ref(false)
const currentDetail = ref({})

const columns = [
  { title: 'ID', key: 'id', width: 60 },
  { title: '邮箱地址', key: 'address', width: 220, ellipsis: { tooltip: true } },
  { title: '显示名称', key: 'display_name', width: 180, render: row => row.display_name || '-' },
  {
    title: '状态',
    key: 'is_active',
    width: 100,
    render(row) {
      return h(
        NTag,
        { type: row.is_active ? 'success' : 'error', size: 'small', round: true },
        { default: () => (row.is_active ? '启用' : '停用') },
      )
    },
  },
  {
    title: '创建时间',
    key: 'created_at',
    width: 160,
    render: row => row.created_at?.replace('T', ' ').slice(0, 16) || '-',
  },
  {
    title: '操作',
    key: 'actions',
    width: 200,
    fixed: 'right',
    render(row) {
      return h(
        NSpace,
        { size: 8 },
        {
          default: () => [
            h(
              NButton,
              { size: 'small', type: 'primary', ghost: true, onClick: () => handleViewDetail(row.id) },
              { default: () => '详情' },
            ),
            h(
              NPopconfirm,
              { onPositiveClick: () => handleToggleActive(row) },
              {
                trigger: () =>
                  h(
                    NButton,
                    { size: 'small', type: row.is_active ? 'warning' : 'success', ghost: true },
                    { default: () => (row.is_active ? '停用' : '启用') },
                  ),
                default: () => `确认${row.is_active ? '停用' : '启用'}邮箱 ${row.address}？`,
              },
            ),
            h(
              NPopconfirm,
              { onPositiveClick: () => handleDelete(row) },
              {
                trigger: () => h(NButton, { size: 'small', type: 'error', ghost: true }, { default: () => '删除' }),
                default: () => `确认删除邮箱 ${row.address}？此操作将永久移除该邮箱所有数据！`,
              },
            ),
          ],
        },
      )
    },
  },
]

async function loadData() {
  loading.value = true
  try {
    const params = {}
    if (searchParams.value.q)
      params.q = searchParams.value.q
    if (searchParams.value.is_active !== null) {
      params.is_active = searchParams.value.is_active === 'true'
    }
    const res = await getAdminMailboxes(params)
    const data = res.data || res
    mailboxes.value = Array.isArray(data) ? data : []
  }
  catch (err) {
    console.error('加载邮箱列表失败:', err)
  }
  finally {
    loading.value = false
  }
}

function handleSearch() {
  loadData()
}

function handleReset() {
  searchParams.value.q = ''
  searchParams.value.is_active = null
  loadData()
}

async function handleViewDetail(id) {
  try {
    const res = await getAdminMailboxDetail(id)
    currentDetail.value = res.data || res
    showDetailModal.value = true
  }
  catch (err) {
    $message.error(err.message || '获取详情失败')
  }
}

async function handleToggleActive(row) {
  try {
    const res = await toggleMailboxActive(row.id)
    const data = res.data || res
    row.is_active = data.is_active ?? !row.is_active
    $message.success(data.message || '操作成功')
  }
  catch (err) {
    $message.error(err.message || '操作失败')
  }
}

async function handleDelete(row) {
  try {
    const res = await deleteMailbox(row.id)
    const data = res.data || res
    $message.success(data.message || '删除成功')
    await loadData()
  }
  catch (err) {
    $message.error(err.message || '删除失败')
  }
}

function handleCreate() {
  formRef.value?.validate(async (errors) => {
    if (errors)
      return
    submitLoading.value = true
    try {
      await createAdminMailbox(createForm.value)
      $message.success('创建邮箱成功')
      showCreateModal.value = false
      createForm.value.address = ''
      createForm.value.display_name = ''
      await loadData()
    }
    catch (err) {
      $message.error(err.message || '创建失败')
    }
    finally {
      submitLoading.value = false
    }
  })
}

onMounted(() => loadData())
</script>
