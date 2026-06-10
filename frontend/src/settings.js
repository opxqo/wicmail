/**********************************
 * WicMail 项目配置
 **********************************/

export const defaultLayout = 'normal'

export const defaultPrimaryColor = '#059669'

// 控制 LayoutSetting 组件是否可见（隐藏，用户不可自主修改）
export const layoutSettingVisible = false

export const naiveThemeOverrides = {
  common: {
    primaryColor: '#059669FF',
    primaryColorHover: '#10b981FF',
    primaryColorPressed: '#047857FF',
    primaryColorSuppl: '#10b981FF',
  },
}

// WicMail 菜单权限配置（静态菜单，无需后端返回）
export const basePermissions = [
  {
    code: 'Profile',
    name: '个人资料',
    type: 'MENU',
    path: '/profile',
    component: '/src/views/profile/index.vue',
    icon: 'i-fe:user',
    order: 0,
    enable: true,
    show: false,
  },
  {
    code: 'Dashboard',
    name: '工作台',
    type: 'MENU',
    path: '/dashboard',
    component: '/src/views/dashboard/index.vue',
    icon: 'i-fe:home',
    order: 1,
    enable: true,
    show: true,
    keepAlive: true,
  },
  {
    code: 'MailboxManage',
    name: '邮箱管理',
    type: 'MENU',
    icon: 'i-fe:mail',
    order: 2,
    enable: true,
    show: true,
    children: [
      {
        code: 'MailboxApply',
        name: '申请邮箱',
        type: 'MENU',
        path: '/mailbox-apply',
        component: '/src/views/mailbox/apply.vue',
        icon: 'i-fe:plus-circle',
        order: 1,
        enable: true,
        show: true,
      },
      {
        code: 'MyMailboxes',
        name: '我的邮箱',
        type: 'MENU',
        path: '/my-mailboxes',
        component: '/src/views/mailbox/list.vue',
        icon: 'i-fe:inbox',
        order: 2,
        enable: true,
        show: true,
      },
    ],
  },
  {
    code: 'EmailCenter',
    name: '邮件中心',
    type: 'MENU',
    path: '/emails',
    component: '/src/views/emails/index.vue',
    icon: 'i-fe:inbox',
    order: 3,
    enable: true,
    show: true,
    keepAlive: true,
  },
  {
    code: 'AdminPanel',
    name: '管理后台',
    type: 'MENU',
    icon: 'i-fe:settings',
    order: 99,
    enable: true,
    show: true,
    children: [
      {
        code: 'AppReview',
        name: '申请审核',
        type: 'MENU',
        path: '/admin/applications',
        component: '/src/views/admin/applications.vue',
        icon: 'i-fe:check-square',
        order: 1,
        enable: true,
        show: true,
      },
      {
        code: 'UserManage',
        name: '用户管理',
        type: 'MENU',
        path: '/admin/users',
        component: '/src/views/admin/users.vue',
        icon: 'i-fe:users',
        order: 2,
        enable: true,
        show: true,
      },
    ],
  },
]
