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

export async function getPermissions(user) {
  const perms = cloneDeep(basePermissions)
  // 非管理员用户隐藏管理后台菜单
  const isAdmin = user?.roles?.some(r => r.code === 'admin')
  if (!isAdmin) {
    return perms.filter(p => p.code !== 'AdminPanel')
  }
  return perms
}
