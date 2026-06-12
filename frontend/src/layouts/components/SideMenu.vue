<!--------------------------------
 - @Author: Ronnie Zhang
 - @LastEditor: Ronnie Zhang
 - @LastEditTime: 2023/12/16 18:50:35
 - @Email: zclzone@outlook.com
 - Copyright © 2023 Ronnie Zhang(大脸怪) | https://isme.top
 --------------------------------->

<template>
  <n-menu
    ref="menu"
    class="side-menu"
    accordion
    :indent="18"
    :collapsed-icon-size="22"
    :collapsed-width="64"
    :collapsed="appStore.collapsed"
    :options="permissionStore.menus"
    :value="activeKey"
    :render-label="renderMenuLabel"
    :render-icon="renderMenuIcon"
    @update:value="handleMenuSelect"
  />
</template>

<script setup>
import { h, computed, nextTick, onMounted, ref, watch } from 'vue'
import { NBadge } from 'naive-ui'
import { useAppStore, usePermissionStore, useUserStore } from '@/store'
import { isExternal } from '@/utils'

const router = useRouter()
const route = useRoute()
const appStore = useAppStore()
const permissionStore = usePermissionStore()
const userStore = useUserStore()

const activeKey = computed(() => route.meta?.parentKey || route.name)

const menu = ref(null)

function renderMenuLabel(option) {
  if (option.key === 'EmailCenter' && userStore.unreadCount > 0 && !appStore.collapsed) {
    return h(
      'div',
      { class: 'flex items-center justify-between w-full pr-12' },
      [
        h('span', null, option.label),
        h(NBadge, { value: userStore.unreadCount, processing: true }),
      ],
    )
  }
  return option.label
}

function renderMenuIcon(option) {
  const iconVNode = option.icon ? option.icon() : null
  if (option.key === 'EmailCenter' && userStore.unreadCount > 0 && appStore.collapsed) {
    return h(NBadge, { dot: true, processing: true }, { default: () => iconVNode })
  }
  return iconVNode
}

watch(route, async () => {
  await nextTick()
  menu.value?.showOption()
  userStore.updateUnreadCount()
})

onMounted(() => {
  userStore.updateUnreadCount()
})

function handleMenuSelect(key, item) {
  if (isExternal(item.originPath)) {
    $dialog.confirm({
      type: 'info',
      title: `请选择打开方式`,
      positiveText: '外链打开',
      negativeText: '在本站内嵌打开',
      confirm() {
        window.open(item.originPath)
      },
      cancel: () => {
        router.push(item.path)
      },
    })
  }
  else {
    if (!item.path)
      return
    router.push(item.path)
  }
}
</script>

<style>
.side-menu:not(.n-menu--collapsed) {
  .n-menu-item-content {
    &::before {
      left: 8px;
      right: 8px;
    }
    &.n-menu-item-content--selected::before {
      border-left: 4px solid rgb(var(--primary-color));
    }
  }
}
</style>
