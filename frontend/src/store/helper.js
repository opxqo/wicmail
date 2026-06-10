import { cloneDeep } from 'lodash-es'
import api from '@/api'
import { basePermissions } from '@/settings'
import { mockApi, isMock } from '@/mock/data'

export async function getUserInfo() {
  if (isMock()) {
    const { useAuthStore } = await import('@/store')
    const token = useAuthStore().accessToken
    const res = await mockApi.getUserDetail(token)
    const { id, username, profile, roles, currentRole } = res.data || {}
    return { id, username, avatar: profile?.avatar, nickName: profile?.nickName, email: profile?.email, roles, currentRole }
  }

  const res = await api.getUser()
  const { id, username, profile, roles, currentRole } = res.data || {}
  return {
    id,
    username,
    avatar: profile?.avatar,
    nickName: profile?.nickName,
    gender: profile?.gender,
    address: profile?.address,
    email: profile?.email,
    roles,
    currentRole,
  }
}

export async function getPermissions() {
  let asyncPermissions = []
  if (!isMock()) {
    try {
      const res = await api.getRolePermissions()
      asyncPermissions = res?.data || []
    }
    catch (error) {
      console.error(error)
    }
  }
  return cloneDeep(basePermissions).concat(asyncPermissions)
}
