/**********************************
 * @Author: Ronnie Zhang
 * @LastEditor: Ronnie Zhang
 * @LastEditTime: 2023/12/05 21:25:59
 * @Email: zclzone@outlook.com
 * Copyright © 2023 Ronnie Zhang(大脸怪) | https://isme.top
 **********************************/

import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    unreadCount: 0,
  }),
  getters: {
    userId() {
      return this.userInfo?.id
    },
    username() {
      return this.userInfo?.username
    },
    nickName() {
      return this.userInfo?.nickName
    },
    avatar() {
      return this.userInfo?.avatar
    },
    currentRole() {
      return this.userInfo?.currentRole || {}
    },
    roles() {
      return this.userInfo?.roles || []
    },
  },
  actions: {
    setUser(user) {
      this.userInfo = user
    },
    resetUser() {
      this.$reset()
    },
    async updateUnreadCount() {
      try {
        const { getUnreadCount } = await import('@/api/wicmail')
        const res = await getUnreadCount()
        const data = res.data || res
        this.unreadCount = data.unread_count ?? 0
      }
      catch (err) {
        console.error('获取未读邮件数失败:', err)
      }
    },
  },
})
