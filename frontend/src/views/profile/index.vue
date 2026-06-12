<template>
  <AppPage show-footer>
    <!-- 用户概览卡片 -->
    <n-card>
      <div class="flex items-center gap-24">
        <div class="relative flex-shrink-0">
          <div class="flex flex-shrink-0 items-center justify-center overflow-hidden rounded-full bg-primary/10 text-28 text-primary" style="width: 72px; height: 72px;">
            <img v-if="profile?.avatar_url" :src="profile.avatar_url" alt="avatar" class="h-full w-full object-cover">
            <span v-else>{{ (userStore.nickName ?? userStore.username)?.charAt(0) }}</span>
          </div>
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
        <n-button type="primary" text class="mr-12" @click="openPasswordModal">
          <i class="i-fe:lock mr-4" /> 修改密码
        </n-button>
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
          <n-select v-model:value="editForm.department" :options="departmentOptions" placeholder="请选择学部" @update:value="handleDepartmentChange" />
        </n-form-item>
        <n-form-item label="专业" path="major">
          <n-select v-model:value="editForm.major" :options="majorOptions" placeholder="请选择专业" :disabled="!editForm.department" />
        </n-form-item>
        <n-form-item label="班级" path="class_name">
          <n-select v-model:value="editForm.class_name" :options="classNameOptions" placeholder="请选择班级" />
        </n-form-item>
        <n-form-item label="年级" path="grade">
          <n-select v-model:value="editForm.grade" :options="gradeOptions" placeholder="请选择年级" />
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

    <!-- 修改密码弹窗 -->
    <MeModal ref="passwordModalRef" title="修改密码" width="420px" @ok="handleChangePassword">
      <n-form ref="passwordFormRef" :model="passwordForm" label-placement="left" label-width="80">
        <n-form-item label="旧密码" path="old_password">
          <n-input v-model:value="passwordForm.old_password" type="password" show-password-on="mousedown" placeholder="请输入当前密码" />
        </n-form-item>
        <n-form-item label="新密码" path="new_password">
          <n-input v-model:value="passwordForm.new_password" type="password" show-password-on="mousedown" placeholder="至少 6 位" />
        </n-form-item>
        <n-form-item label="确认密码" path="confirm_password">
          <n-input v-model:value="passwordForm.confirm_password" type="password" show-password-on="mousedown" placeholder="再次输入新密码" />
        </n-form-item>
      </n-form>
    </MeModal>
  </AppPage>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { changePassword, getProfile, updateProfile } from '@/api/wicmail'
import { MeModal } from '@/components'
import AvatarEditor from '@/components/me/AvatarEditor.vue'
import { useModal } from '@/composables'
import { useUserStore } from '@/store'
import { getUserInfo } from '@/store/helper'

const userStore = useUserStore()
const profile = ref(null)
const [editModalRef] = useModal()
const editFormRef = ref(null)
const [passwordModalRef] = useModal()
const passwordFormRef = ref(null)

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

const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

// 武汉城市学院 学部与专业标准字典
const DEPARTMENT_MAJORS = {
  信息工程学部: ['计算机科学与技术', '软件工程', '数据科学与大数据技术', '电子信息工程', '物联网工程'],
  机电工程学部: ['机械设计制造及其自动化', '电气工程及其自动化', '自动化', '机器人工程'],
  城市建设学部: ['土木工程', '建筑学', '工程造价', '风景园林'],
  医学部: ['护理学', '康复治疗学', '药学'],
  经济与管理学部: ['会计学', '财务管理', '市场营销', '国际经济与贸易', '电子商务'],
  艺术设计学部: ['视觉传达设计', '环境设计', '产品设计'],
  外语学部: ['英语', '商务英语'],
}

// 动态学部下拉项，兼容历史非标准值
const departmentOptions = computed(() => {
  const standardDepts = Object.keys(DEPARTMENT_MAJORS)
  const opts = standardDepts.map(dept => ({ label: dept, value: dept }))
  const currentVal = editForm.value.department
  if (currentVal && !standardDepts.includes(currentVal)) {
    opts.unshift({ label: `${currentVal} (非标准)`, value: currentVal })
  }
  return opts
})

// 动态专业下拉项，根据学部联动，兼容历史非标准专业值
const majorOptions = computed(() => {
  const dept = editForm.value.department
  if (!dept)
    return []
  const standardMajors = DEPARTMENT_MAJORS[dept] || []
  const opts = standardMajors.map(m => ({ label: m, value: m }))
  const currentMajor = editForm.value.major
  if (currentMajor && !standardMajors.includes(currentMajor)) {
    opts.unshift({ label: `${currentMajor} (非标准)`, value: currentMajor })
  }
  return opts
})

// 学部变更时联动重置专业（若不属于新学部的专业列表）
function handleDepartmentChange(value) {
  const standardMajors = DEPARTMENT_MAJORS[value] || []
  if (!standardMajors.includes(editForm.value.major)) {
    editForm.value.major = ''
  }
}

// 年级下拉选项（近 6 年）
const gradeOptions = computed(() => {
  const currentYear = new Date().getFullYear()
  const standardGrades = []
  for (let i = 0; i < 6; i++) {
    standardGrades.push(String(currentYear - i))
  }
  const opts = standardGrades.map(g => ({ label: `${g} 级`, value: g }))
  const currentVal = editForm.value.grade
  if (currentVal && !standardGrades.includes(currentVal)) {
    opts.unshift({ label: `${currentVal} (非标准)`, value: currentVal })
  }
  return opts
})

// 班级下拉选项（1 到 10 班）
const classNameOptions = computed(() => {
  const standardClasses = Array.from({ length: 10 }, (_, i) => String(i + 1))
  const opts = standardClasses.map(c => ({ label: `${c} 班`, value: c }))
  const currentVal = editForm.value.class_name
  if (currentVal && !standardClasses.includes(currentVal)) {
    opts.unshift({ label: `${currentVal} (非标准)`, value: currentVal })
  }
  return opts
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
  let dept = profile.value?.department || ''
  // 智能修复旧版本数据库存储的无“学部”后缀的旧字段值
  if (dept === '信息工程')
    dept = '信息工程学部'
  else if (dept === '机电工程')
    dept = '机电工程学部'
  else if (dept === '城市建设')
    dept = '城市建设学部'
  else if (dept === '经济与管理')
    dept = '经济与管理学部'
  else if (dept === '艺术设计')
    dept = '艺术设计学部'
  else if (dept === '外语')
    dept = '外语学部'

  // 纠错规范化年级和班级数据（剥离可能的中文后缀以符合纯数字标准）
  let grade = profile.value?.grade || ''
  if (grade) {
    grade = grade.replace('级', '').trim()
  }
  let className = profile.value?.class_name || ''
  if (className) {
    className = className.replace('班', '').trim()
  }

  editForm.value = {
    email: profile.value?.email || '',
    real_name: profile.value?.real_name || '',
    department: dept,
    major: profile.value?.major || '',
    class_name: className,
    grade,
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

function openPasswordModal() {
  passwordForm.value = { old_password: '', new_password: '', confirm_password: '' }
  passwordModalRef.value.open()
}

async function handleChangePassword() {
  const { old_password, new_password, confirm_password } = passwordForm.value
  if (!old_password)
    return $message.warning('请输入旧密码')
  if (!new_password || new_password.length < 6)
    return $message.warning('新密码至少 6 位')
  if (new_password !== confirm_password)
    return $message.warning('两次输入的密码不一致')
  try {
    await changePassword({ old_password, new_password })
    $message.success('密码修改成功')
  }
  catch (err) {
    $message.error(err.message || '修改失败')
  }
}

onMounted(() => loadProfile())
</script>
