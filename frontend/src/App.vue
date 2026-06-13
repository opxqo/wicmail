<!--------------------------------
 - @Author: Ronnie Zhang
 - @LastEditor: Ronnie Zhang
 - @LastEditTime: 2023/12/16 18:49:42
 - @Email: zclzone@outlook.com
 - Copyright © 2023 Ronnie Zhang(大脸怪) | https://isme.top
 --------------------------------->

<template>
  <n-config-provider
    class="wh-full"
    :locale="zhCN"
    :date-locale="dateZhCN"
    :theme="appStore.isDark ? darkTheme : undefined"
    :theme-overrides="appStore.naiveThemeOverrides"
  >
    <LoadingScreen
      v-if="showLoadingScreen"
      :variant="loadingScreenVariant"
      :duration="loadingScreenDuration"
      @finished="handleLoadingFinished"
    />

    <router-view v-if="Layout" v-slot="{ Component, route: curRoute }">
      <component :is="Layout">
        <transition name="fade-slide" mode="out-in" appear>
          <KeepAlive :include="keepAliveNames">
            <component :is="Component" v-if="!tabStore.reloading" :key="curRoute.fullPath" />
          </KeepAlive>
        </transition>
      </component>

      <LayoutSetting v-if="layoutSettingVisible" class="fixed right-12 top-1/2 z-999" />
    </router-view>
  </n-config-provider>
</template>

<script setup>
import { darkTheme, dateZhCN, zhCN } from 'naive-ui'
import { LayoutSetting } from '@/components'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import { useAppStore, useTabStore } from '@/store'
import { layoutSettingVisible } from './settings'

const SPLASH_STORAGE_KEY = 'wicmail:startup-splash-shown'
const STARTUP_REVEAL_DELAY = 350
const FULL_SPLASH_DURATION = 1200
const COMPACT_SPLASH_DURATION = 700
const SLOW_BOOT_THRESHOLD = 900

function getStartupElapsed() {
  return typeof performance === 'undefined' ? 0 : performance.now()
}

function hasShownStartupSplash() {
  try {
    return sessionStorage.getItem(SPLASH_STORAGE_KEY) === 'true'
  }
  catch {
    return false
  }
}

function markStartupSplashShown() {
  try {
    sessionStorage.setItem(SPLASH_STORAGE_KEY, 'true')
  }
  catch {}
}

function removeStartupPlaceholder(immediate = false) {
  if (typeof document === 'undefined')
    return

  const placeholder = document.getElementById('startup-splash')
  if (!placeholder)
    return

  if (immediate) {
    placeholder.remove()
    return
  }

  placeholder.classList.add('startup-splash-leaving')
  window.setTimeout(() => placeholder.remove(), 260)
}

const startupElapsed = getStartupElapsed()
const hasShownSplash = hasShownStartupSplash()
const shouldShowFullSplash = !hasShownSplash && startupElapsed >= STARTUP_REVEAL_DELAY
const shouldShowCompactSplash = hasShownSplash && startupElapsed >= SLOW_BOOT_THRESHOLD

if (shouldShowFullSplash)
  markStartupSplashShown()

const showLoadingScreen = ref(shouldShowFullSplash || shouldShowCompactSplash)
const loadingScreenVariant = ref(shouldShowFullSplash ? 'full' : 'compact')
const loadingScreenDuration = computed(() => {
  return loadingScreenVariant.value === 'compact' ? COMPACT_SPLASH_DURATION : FULL_SPLASH_DURATION
})

function handleLoadingFinished() {
  showLoadingScreen.value = false
  removeStartupPlaceholder(true)
}

onMounted(() => {
  nextTick(() => {
    removeStartupPlaceholder(startupElapsed < STARTUP_REVEAL_DELAY && !showLoadingScreen.value)
  })
})

const layouts = new Map()
function getLayout(name) {
  // 利用map将加载过的layout缓存起来，防止重新加载layout导致页面闪烁
  if (layouts.get(name))
    return layouts.get(name)
  const layout = markRaw(defineAsyncComponent(() => import(`@/layouts/${name}/index.vue`)))
  layouts.set(name, layout)
  return layout
}

const route = useRoute()
const appStore = useAppStore()
if (appStore.layout === 'default')
  appStore.setLayout('')
const Layout = computed(() => {
  if (!route.matched?.length)
    return null
  return getLayout(route.meta?.layout || appStore.layout)
})

const tabStore = useTabStore()
const keepAliveNames = computed(() => {
  return tabStore.tabs.filter(item => item.keepAlive).map(item => item.name)
})

watchEffect(() => {
  appStore.setThemeColor(appStore.primaryColor, appStore.isDark)
})
</script>
