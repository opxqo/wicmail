import { cloneDeep } from 'lodash-es'
import { basePermissions } from '@/settings'
import loginApi from '@/views/login/api'

export async function getUserInfo() {
  const res = await loginApi.getUser()
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
  // 使用静态菜单配置，无需从后端获取
  return cloneDeep(basePermissions)
}
