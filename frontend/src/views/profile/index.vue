<template>
  <AppPage show-footer>
    <!-- 用户概览卡片 -->
    <n-card>
      <div class="flex items-center gap-24">
        <div class="relative flex-shrink-0">
          <n-avatar round :size="72" :src="profile?.avatar_url" class="bg-primary/10 text-28 text-primary">
            {{ (userStore.nickName ?? userStore.username)?.charAt(0) }}
          </n-avatar>
          <n-button
            size="tiny"
            circle
            type="primary"
            class="absolute z-1 shadow-sm -bottom-2 -right-2"
            @click="openAvatarEditor"
          >
            <i class="i-fe:camera text-12" />
          </n-button>
        </div>
        <div class="flex-1">
          <div class="flex items-center gap-12">
            <span class="text-20 font-bold">{{ profile?.real_name || userStore.username }}</span>
            <n-tag size="small" :type="profile?.is_admin ? 'warning' : 'default'" round :bordered="false">
              {{ profile?.is_admin ? '管理员' : '普通用户' }}
            </n-tag>
          </div>
          <div class="mt-6 text-13 opacity-50">
            用户名：{{ userStore.username }}
            <span class="ml-16">学号：{{ profile?.student_id || '未设置' }}</span>
          </div>
          <div class="mt-12 flex items-center gap-12">
            <n-progress
              type="line"
              :percentage="completionPercent"
              :status="completionPercent === 100 ? 'success' : 'warning'"
              :show-indicator="false"
              :height="8"
              :border-radius="4"
              style="width: 200px"
            />
            <span class="text-13" :class="completionPercent === 100 ? 'text-green-600' : 'opacity-50'">
              {{ completionPercent === 100 ? '资料已完善' : `资料完善度 ${completionPercent}%` }}
            </span>
          </div>
        </div>
      </div>
    </n-card>

    <!-- 缺失字段提示 -->
    <n-alert
      v-if="profile?.missing_fields?.length"
      type="warning"
      class="mt-12"
      :bordered="false"
    >
      <template #icon>
        <i class="i-fe:alert-triangle text-18" />
      </template>
      <div class="flex items-center gap-8">
        <span>以下字段尚未填写，完善后才能申请邮箱：</span>
        <n-space :size="4">
          <n-tag v-for="field in profile.missing_fields" :key="field" type="warning" size="small" round :bordered="false">
            {{ field }}
          </n-tag>
        </n-space>
      </div>
    </n-alert>

    <!-- 资料展示 -->
    <n-card class="mt-12">
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:user text-18" /> 个人资料信息</span>
      </template>
      <template #header-extra>
        <n-button type="primary" text @click="openEditModal">
          <i class="i-fe:edit mr-4" /> 修改资料
        </n-button>
      </template>

      <n-descriptions label-placement="left" :label-style="{ width: '120px' }" :column="1" bordered>
        <n-descriptions-item label="学号">
          <span>{{ profile?.student_id || '未设置' }}</span>
        </n-descriptions-item>
        <n-descriptions-item label="邮箱">
          <span :class="{ 'opacity-30': !profile?.email }">{{ profile?.email || '未填写' }}</span>
        </n-descriptions-item>
        <n-descriptions-item label="真实姓名">
          <span :class="{ 'opacity-30': !profile?.real_name }">{{ profile?.real_name || '未填写' }}</span>
        </n-descriptions-item>
        <n-descriptions-item label="学部">
          <span :class="{ 'opacity-30': !profile?.department }">{{ profile?.department || '未填写' }}</span>
        </n-descriptions-item>
        <n-descriptions-item label="专业">
          <span :class="{ 'opacity-30': !profile?.major }">{{ profile?.major || '未填写' }}</span>
        </n-descriptions-item>
        <n-descriptions-item label="班级">
          <span :class="{ 'opacity-30': !profile?.class_name }">{{ profile?.class_name || '未填写' }}</span>
        </n-descriptions-item>
        <n-descriptions-item label="年级">
          <span :class="{ 'opacity-30': !profile?.grade }">{{ profile?.grade || '未填写' }}</span>
        </n-descriptions-item>
      </n-descriptions>
    </n-card>

    <!-- 修改资料弹窗 -->
    <MeModal ref="editModalRef" title="修改资料" width="480px" @ok="handleSave">
      <n-form ref="editFormRef" :model="editForm" label-placement="left" label-width="80">
        <n-form-item label="邮箱" path="email">
          <n-input v-model:value="editForm.email" placeholder="请输入邮箱" />
        </n-form-item>
        <n-form-item label="真实姓名" path="real_name">
          <n-input v-model:value="editForm.real_name" placeholder="请输入真实姓名" />
        </n-form-item>
        <n-form-item label="学部" path="department">
          <n-input v-model:value="editForm.department" placeholder="请输入学部" />
        </n-form-item>
        <n-form-item label="专业" path="major">
          <n-input v-model:value="editForm.major" placeholder="请输入专业" />
        </n-form-item>
        <n-form-item label="班级" path="class_name">
          <n-input v-model:value="editForm.class_name" placeholder="请输入班级" />
        </n-form-item>
        <n-form-item label="年级" path="grade">
          <n-input v-model:value="editForm.grade" placeholder="请输入年级，如 2024" />
        </n-form-item>
      </n-form>
    </MeModal>

    <!-- 头像编辑器弹窗 -->
    <n-modal
      v-model:show="avatarModalVisible"
      preset="card"
      title="自定义头像"
      style="max-width: 640px;"
      :mask-closable="false"
    >
      <AvatarEditor
        v-model="avatarUrl"
        :username="userStore.username"
      />
      <template #footer>
        <div class="flex justify-end gap-8">
          <n-button @click="avatarModalVisible = false">
            取消
          </n-button>
          <n-button type="primary" :loading="savingAvatar" @click="saveAvatar">
            保存头像
          </n-button>
        </div>
      </template>
    </n-modal>
  </AppPage>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { getProfile, updateProfile } from '@/api/wicmail'
import { MeModal } from '@/components'
import AvatarEditor from '@/components/me/AvatarEditor.vue'
import { useModal } from '@/composables'
import { useUserStore } from '@/store'
import { getUserInfo } from '@/store/helper'

const userStore = useUserStore()
const profile = ref(null)
const [editModalRef] = useModal()
const editFormRef = ref(null)

// 头像编辑器
const avatarModalVisible = ref(false)
const avatarUrl = ref('')
const savingAvatar = ref(false)

const editForm = ref({
  email: '',
  real_name: '',
  department: '',
  major: '',
  class_name: '',
  grade: '',
})

// 资料完善度百分比
const completionPercent = computed(() => {
  if (!profile.value)
    return 0
  const total = 6 // email, real_name, department, major, class_name, grade
  const missing = profile.value.missing_fields?.length || 0
  return Math.round(((total - missing) / total) * 100)
})

function openEditModal() {
  editForm.value = {
    email: profile.value?.email || '',
    real_name: profile.value?.real_name || '',
    department: profile.value?.department || '',
    major: profile.value?.major || '',
    class_name: profile.value?.class_name || '',
    grade: profile.value?.grade || '',
  }
  editModalRef.value.open()
}

async function handleSave() {
  try {
    await updateProfile(editForm.value)
    $message.success('资料修改成功')
    await loadProfile()
  }
  catch (err) {
    $message.error(err.message || '修改失败')
  }
}

async function loadProfile() {
  try {
    const res = await getProfile()
    profile.value = res.data || res

    // 同步 userStore
    const user = await getUserInfo()
    userStore.setUser(user)
  }
  catch (err) {
    console.error('加载个人资料失败:', err)
  }
}

function openAvatarEditor() {
  avatarUrl.value = profile.value?.avatar_url || ''
  avatarModalVisible.value = true
}

async function saveAvatar() {
  if (!avatarUrl.value) {
    $message.warning('请选择头像')
    return
  }
  savingAvatar.value = true
  try {
    await updateProfile({ avatar_url: avatarUrl.value })
    $message.success('头像已更新')
    avatarModalVisible.value = false
    await loadProfile()
  }
  catch (err) {
    $message.error(err.message || '保存失败')
  }
  finally {
    savingAvatar.value = false
  }
}

onMounted(() => loadProfile())
</script>
