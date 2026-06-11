<template>
  <div class="wh-full flex-col bg-[url(@/assets/images/login_bg.webp)] bg-cover">
    <div
      class="m-auto max-w-700 min-w-345 flex rounded-8 auto-bg bg-opacity-20 bg-cover p-12 card-shadow"
    >
      <div class="hidden w-380 px-20 py-35 md:block">
        <img src="@/assets/images/login_banner.webp" class="w-full" alt="login_banner">
      </div>

      <div ref="formAreaRef" class="relative w-320 flex-col overflow-hidden px-20 py-32">
        <!-- 登录表单 -->
        <div
          v-show="isLoginMode || isTransitioning"
          ref="loginFormRef"
          class="w-full flex flex-col"
        >
          <h2 class="f-c-c text-24 text-#6a6a6a font-normal">
            <img src="https://r2.wic.edu.kg/images/favicon.svg" class="mr-12 h-40 w-40" alt="logo">
            登录 WicMail
          </h2>
          <p class="mt-8 f-c-c text-13 opacity-40">
            校园邮箱管理平台
          </p>

          <n-input
            v-model:value="loginInfo.username"
            autofocus
            class="mt-32 h-40 items-center"
            placeholder="请输入用户名"
            :maxlength="20"
          >
            <template #prefix>
              <i class="i-fe:user mr-12 opacity-20" />
            </template>
          </n-input>
          <n-input
            v-model:value="loginInfo.password"
            class="mt-20 h-40 items-center"
            type="password"
            show-password-on="mousedown"
            placeholder="请输入密码"
            :maxlength="50"
            @keydown.enter="handleLogin()"
          >
            <template #prefix>
              <i class="i-fe:lock mr-12 opacity-20" />
            </template>
          </n-input>

          <n-checkbox
            class="mt-20"
            :checked="isRemember"
            label="记住我"
            :on-update:checked="(val) => (isRemember = val)"
          />

          <div class="mt-20 flex items-center">
            <n-button
              class="h-40 flex-1 rounded-5 text-16"
              type="primary"
              ghost
              @click="quickLogin()"
            >
              一键体验
            </n-button>

            <n-button
              class="ml-32 h-40 flex-1 rounded-5 text-16"
              type="primary"
              :loading="loading"
              @click="handleLogin()"
            >
              登录
            </n-button>
          </div>

          <div class="mt-20 flex items-center justify-between text-12">
            <span class="cursor-pointer text-primary hover:underline" @click="switchMode(false)">没有账号？点击注册</span>
            <router-link to="/" class="opacity-40 hover:underline">
              ← 返回首页
            </router-link>
          </div>
        </div>

        <!-- 注册表单 -->
        <div
          v-show="!isLoginMode || isTransitioning"
          ref="registerFormRef"
          class="w-full flex flex-col"
        >
          <h2 class="f-c-c text-24 text-#6a6a6a font-normal">
            <img src="https://r2.wic.edu.kg/images/favicon.svg" class="mr-12 h-40 w-40" alt="logo">
            注册账号
          </h2>
          <p class="mt-8 f-c-c text-13 opacity-40">
            校园邮箱管理平台
          </p>

          <n-input
            v-model:value="registerInfo.username"
            autofocus
            class="mt-24 h-40 items-center"
            placeholder="请输入用户名 (小写字母/数字/下划线)"
            :maxlength="20"
          >
            <template #prefix>
              <i class="i-fe:user mr-12 opacity-20" />
            </template>
          </n-input>

          <n-input
            v-model:value="registerInfo.student_id"
            class="mt-20 h-40 items-center"
            placeholder="请输入学号"
            :maxlength="20"
          >
            <template #prefix>
              <i class="i-fe:credit-card mr-12 opacity-20" />
            </template>
          </n-input>

          <n-input
            v-model:value="registerInfo.password"
            class="mt-20 h-40 items-center"
            type="password"
            show-password-on="mousedown"
            placeholder="请输入密码 (至少 6 位)"
            :maxlength="50"
          >
            <template #prefix>
              <i class="i-fe:lock mr-12 opacity-20" />
            </template>
          </n-input>

          <n-input
            v-model:value="registerInfo.confirmPassword"
            class="mt-20 h-40 items-center"
            type="password"
            show-password-on="mousedown"
            placeholder="请再次输入密码"
            :maxlength="50"
            @keydown.enter="handleRegister()"
          >
            <template #prefix>
              <i class="i-fe:lock mr-12 opacity-20" />
            </template>
          </n-input>

          <div class="mt-24 flex items-center">
            <n-button
              class="h-40 flex-1 rounded-5 text-16"
              type="primary"
              ghost
              @click="switchMode(true)"
            >
              返回登录
            </n-button>

            <n-button
              class="ml-32 h-40 flex-1 rounded-5 text-16"
              type="primary"
              :loading="registerLoading"
              @click="handleRegister()"
            >
              注册
            </n-button>
          </div>

          <div class="mt-20 flex items-center justify-between text-12">
            <span class="cursor-pointer text-primary hover:underline" @click="switchMode(true)">已有账号？立即登录</span>
            <router-link to="/" class="opacity-40 hover:underline">
              ← 返回首页
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <TheFooter class="py-12" />
  </div>
</template>

<script setup>
import { useStorage } from '@vueuse/core'
import { createTimeline } from 'animejs'
import { useAuthStore } from '@/store'
import { lStorage } from '@/utils'
import api from './api'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const isLoginMode = ref(true)
const isTransitioning = ref(false)

const formAreaRef = ref(null)
const loginFormRef = ref(null)
const registerFormRef = ref(null)

const loginInfo = ref({
  username: '',
  password: '',
})

const registerLoading = ref(false)
const registerInfo = ref({
  username: '',
  student_id: '',
  password: '',
  confirmPassword: '',
})

const localLoginInfo = lStorage.get('loginInfo')
if (localLoginInfo) {
  loginInfo.value.username = localLoginInfo.username || ''
  loginInfo.value.password = localLoginInfo.password || ''
}

function quickLogin() {
  loginInfo.value.username = 'admin'
  loginInfo.value.password = 'admin123456'
  handleLogin(true)
}

const isRemember = useStorage('isRemember', true)
const loading = ref(false)

async function switchMode(toLogin) {
  if (isTransitioning.value || isLoginMode.value === toLogin)
    return
  isTransitioning.value = true

  const container = formAreaRef.value
  const loginEl = loginFormRef.value
  const registerEl = registerFormRef.value

  if (!container || !loginEl || !registerEl) {
    isLoginMode.value = toLogin
    isTransitioning.value = false
    return
  }

  // 1. Measure start height
  const startHeight = container.offsetHeight

  // Elements that will animate
  const activeEl = toLogin ? registerEl : loginEl
  const targetEl = toLogin ? loginEl : registerEl

  // 2. Prepare for layout measurement:
  // Make activeEl absolute so it doesn't affect container height
  activeEl.style.position = 'absolute'
  activeEl.style.top = '32px'
  activeEl.style.left = '20px'
  activeEl.style.width = 'calc(100% - 40px)'
  activeEl.style.pointerEvents = 'none'

  // Ensure targetEl is in normal flow
  targetEl.style.position = ''
  targetEl.style.top = ''
  targetEl.style.left = ''
  targetEl.style.width = ''
  targetEl.style.opacity = ''
  targetEl.style.transform = ''
  targetEl.style.pointerEvents = ''
  targetEl.style.display = ''

  // Ensure container height is auto during measurement so it shrinks/grows naturally
  container.style.height = ''

  // Perform state change to trigger Vue layout render
  isLoginMode.value = toLogin

  await nextTick()

  // Measure target height now that it's the only one in normal flow
  const endHeight = container.offsetHeight

  // 3. Set up absolute positions and starting animation states for both elements
  // Lock container to startHeight for the start of animation
  container.style.height = `${startHeight}px`

  // Now make targetEl absolute for slide-in animation
  targetEl.style.position = 'absolute'
  targetEl.style.top = '32px'
  targetEl.style.left = '20px'
  targetEl.style.width = 'calc(100% - 40px)'
  targetEl.style.opacity = '0'
  targetEl.style.transform = toLogin ? 'translateX(-40px)' : 'translateX(40px)'
  targetEl.style.pointerEvents = 'none'

  // Ensure activeEl starts at full opacity and zero transform
  activeEl.style.opacity = '1'
  activeEl.style.transform = 'translateX(0px)'

  // Create timeline
  const tl = createTimeline({
    ease: 'cubicBezier(0.4, 0, 0.2, 1)',
    onComplete: () => {
      // Clean up styles
      container.style.height = ''

      activeEl.style.position = ''
      activeEl.style.top = ''
      activeEl.style.left = ''
      activeEl.style.width = ''
      activeEl.style.opacity = ''
      activeEl.style.transform = ''
      activeEl.style.pointerEvents = ''

      targetEl.style.position = ''
      targetEl.style.top = ''
      targetEl.style.left = ''
      targetEl.style.width = ''
      targetEl.style.opacity = ''
      targetEl.style.transform = ''
      targetEl.style.pointerEvents = ''
      targetEl.style.display = ''

      isTransitioning.value = false
    },
  })

  // Height animation
  tl.add(container, {
    height: [startHeight, endHeight],
    duration: 450,
  }, 0)

  // Slide out active form
  tl.add(activeEl, {
    opacity: [1, 0],
    translateX: toLogin ? [0, 40] : [0, -40],
    duration: 350,
  }, 0)

  // Slide in target form
  tl.add(targetEl, {
    opacity: [0, 1],
    translateX: toLogin ? [-40, 0] : [40, 0],
    duration: 400,
  }, 50)
}


async function handleLogin() {
  const { username, password } = loginInfo.value
  if (!username || !password)
    return $message.warning('请输入用户名和密码')
  try {
    loading.value = true
    $message.loading('正在验证，请稍后...', { key: 'login' })
    const res = await api.login({ username, password: password.toString() })
    const data = res.data || res
    if (isRemember.value) {
      lStorage.set('loginInfo', { username, password })
    }
    else {
      lStorage.remove('loginInfo')
    }
    onLoginSuccess(data)
  }
  catch (error) {
    $message.destroy('login')
    $message.error(error?.message || '登录失败')
    console.error(error)
  }
  loading.value = false
}

async function handleRegister() {
  const { username, student_id, password, confirmPassword } = registerInfo.value

  if (!username)
    return $message.warning('请输入用户名')
  if (username.length < 3)
    return $message.warning('用户名长度至少为 3 个字符')
  if (!/^[a-z0-9_-]+$/.test(username)) {
    return $message.warning('用户名只能包含小写字母、数字、下划线和横线')
  }

  if (!student_id)
    return $message.warning('请输入学号')
  if (!/^[a-z0-9]+$/i.test(student_id)) {
    return $message.warning('学号只能包含字母和数字')
  }

  if (!password)
    return $message.warning('请输入密码')
  if (password.length < 6)
    return $message.warning('密码长度至少为 6 位')
  if (password !== confirmPassword)
    return $message.warning('两次输入的密码不一致')

  try {
    registerLoading.value = true
    $message.loading('正在注册，请稍后...', { key: 'register' })
    await api.register({
      username,
      student_id: student_id.toUpperCase(),
      password,
    })
    $message.success('注册成功！已为您自动填充登录信息', { key: 'register' })
    // Fill login info automatically and switch mode
    loginInfo.value.username = username
    loginInfo.value.password = password
    switchMode(true)
    // Reset register form
    registerInfo.value = {
      username: '',
      student_id: '',
      password: '',
      confirmPassword: '',
    }
  }
  catch (error) {
    $message.destroy('register')
    $message.error(error?.message || '注册失败，请稍后重试')
    console.error(error)
  }
  registerLoading.value = false
}

async function onLoginSuccess(data = {}) {
  authStore.setToken(data)
  $message.loading('登录中...', { key: 'login' })
  try {
    $message.success('登录成功', { key: 'login' })
    if (route.query.redirect) {
      const path = route.query.redirect
      delete route.query.redirect
      router.push({ path, query: route.query })
    }
    else {
      router.push('/dashboard')
    }
  }
  catch (error) {
    console.error(error)
    $message.destroy('login')
  }
}
</script>
