<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <div class="w-full flex items-center justify-between">
          <span class="flex items-center gap-8"><i class="i-fe:shield text-18" /> 管理员管理</span>
          <NButton type="primary" size="small" @click="showAddModal = true">
            <template #icon>
              <i class="i-fe:plus" />
            </template>
            提拔管理员
          </NButton>
        </div>
      </template>

      <n-data-table :columns="columns" :data="admins" :loading="loading" />
    </n-card>

    <!-- 新增管理员弹窗 -->
    <n-modal
      v-model:show="showAddModal"
      preset="card"
      title="提拔新管理员"
      style="width: 450px"
      :segmented="{ content: 'soft', footer: 'soft' }"
    >
      <div class="mb-12 text-13 opacity-70">
        请输入已注册普通用户的用户名。确认后，该用户将被提拔，获得管理员后台登录及操作权限。
      </div>
      <n-form ref="formRef" :model="addForm" :rules="rules" label-placement="left" label-width="80">
        <n-form-item label="用户名" path="username">
          <n-input v-model:value="addForm.username" placeholder="请输入精确用户名" />
        </n-form-item>
      </n-form>
      <template #footer>
        <div class="flex justify-end gap-12">
          <NButton ghost @click="showAddModal = false">
            取消
          </NButton>
          <NButton type="primary" :loading="submitLoading" @click="handleAddAdmin">
            确定提拔
          </NButton>
        </div>
      </template>
    </n-modal>
  </AppPage>
</template>

<script setup>
import { NButton, NPopconfirm, NSpace, NTag } from 'naive-ui'
import { h, onMounted, ref } from 'vue'
import { addAdmin, getAdminList, removeAdmin, updateAdminRole } from '@/api/wicmail'
import { AppPage } from '@/components'
import { useUserStore } from '@/store'

const userStore = useUserStore()
const loading = ref(false)
const submitLoading = ref(false)
const admins = ref([])

const showAddModal = ref(false)
const addForm = ref({ username: '' })
const formRef = ref(null)
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
}

const columns = [
  { title: 'ID', key: 'id', width: 60 },
  { title: '用户名', key: 'username', width: 140 },
  { title: '邮箱', key: 'email', render: row => row.email || '-', ellipsis: { tooltip: true } },
  { title: '真实姓名', key: 'real_name', width: 120, render: row => row.real_name || '-' },
  {
    title: '角色状态',
    key: 'is_admin',
    width: 120,
    render(row) {
      return h(
        NTag,
        { type: row.is_admin ? 'warning' : 'default', size: 'small', round: true },
        { default: () => (row.is_admin ? '超级管理员' : '普通用户') },
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
    width: 180,
    fixed: 'right',
    render(row) {
      // 超级管理员自己不能将自己降权或解除授权
      const isSelf = row.id === userStore.userInfo?.id
      return h(
        NSpace,
        { size: 8 },
        {
          default: () => [
            h(
              NPopconfirm,
              { onPositiveClick: () => handleDemote(row) },
              {
                trigger: () =>
                  h(
                    NButton,
                    { size: 'small', type: 'warning', ghost: true, disabled: isSelf },
                    { default: () => '降权' },
                  ),
                default: () => `确认将管理员 ${row.username} 降权为普通用户吗？`,
              },
            ),
            h(
              NPopconfirm,
              { onPositiveClick: () => handleRemove(row) },
              {
                trigger: () =>
                  h(
                    NButton,
                    { size: 'small', type: 'error', ghost: true, disabled: isSelf },
                    { default: () => '解除授权' },
                  ),
                default: () => `确认移除 ${row.username} 的管理员身份吗？`,
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
    const res = await getAdminList()
    const data = res.data || res
    admins.value = Array.isArray(data) ? data : []
  }
  catch (err) {
    console.error('加载管理员列表失败:', err)
  }
  finally {
    loading.value = false
  }
}

async function handleDemote(row) {
  try {
    const res = await updateAdminRole(row.id, { is_admin: false })
    const data = res.data || res
    $message.success(data.message || '操作成功')
    await loadData()
  }
  catch (err) {
    $message.error(err.message || '操作失败')
  }
}

async function handleRemove(row) {
  try {
    const res = await removeAdmin(row.id)
    const data = res.data || res
    $message.success(data.message || '操作成功')
    await loadData()
  }
  catch (err) {
    $message.error(err.message || '操作失败')
  }
}

function handleAddAdmin() {
  formRef.value?.validate(async (errors) => {
    if (errors)
      return
    submitLoading.value = true
    try {
      await addAdmin(addForm.value.username)
      $message.success('成功提拔新管理员')
      showAddModal.value = false
      addForm.value.username = ''
      await loadData()
    }
    catch (err) {
      $message.error(err.message || '提拔管理员失败')
    }
    finally {
      submitLoading.value = false
    }
  })
}

onMounted(() => loadData())
</script>
