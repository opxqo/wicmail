/**
 * WicMail Mock 数据
 * 模拟 backend-wic 全部 API 响应数据
 */

// ============ 用户数据 ============
const users = [
  {
    id: 1,
    username: 'admin',
    student_id: 'WIC2024001',
    email: 'admin@wic.edu.kg',
    real_name: '管理员',
    department: '信息技术学部',
    major: '计算机科学与技术',
    class_name: '计科2401',
    grade: '2024',
    is_active: true,
    is_admin: true,
    profile_complete: true,
    missing_fields: [],
    created_at: '2024-09-01T08:00:00',
    updated_at: '2024-09-15T10:30:00',
  },
  {
    id: 2,
    username: 'zhangsan',
    student_id: 'WIC2024002',
    email: 'zhangsan@wic.edu.kg',
    real_name: '张三',
    department: '信息技术学部',
    major: '软件工程',
    class_name: '软工2401',
    grade: '2024',
    is_active: true,
    is_admin: false,
    profile_complete: true,
    missing_fields: [],
    created_at: '2024-09-02T09:00:00',
    updated_at: '2024-09-10T14:20:00',
  },
  {
    id: 3,
    username: 'lisi',
    student_id: 'WIC2024003',
    email: null,
    real_name: null,
    department: null,
    major: null,
    class_name: null,
    grade: null,
    is_active: true,
    is_admin: false,
    profile_complete: false,
    missing_fields: ['邮箱', '真实姓名', '学部', '专业', '班级', '年级'],
    created_at: '2024-09-05T11:00:00',
    updated_at: '2024-09-05T11:00:00',
  },
]

// ============ 邮箱数据 ============
const mailboxes = [
  { id: 1, address: 'admin@wic.edu.kg', display_name: '管理员邮箱', is_active: true, created_at: '2024-09-01T08:00:00' },
  { id: 2, address: 'zhangsan@wic.edu.kg', display_name: '张三的邮箱', is_active: true, created_at: '2024-09-10T14:00:00' },
  { id: 3, address: 'lab@wic.edu.kg', display_name: '实验室公共邮箱', is_active: true, created_at: '2024-09-15T09:00:00' },
]

// ============ 邮箱申请数据 ============
let attachmentIdCounter = 100
const applications = [
  {
    id: 1,
    user_id: 1,
    username: 'admin',
    requested_address: 'admin@wic.edu.kg',
    display_name: '管理员邮箱',
    status: 'approved',
    reason: '管理员工作邮箱',
    review_comment: '已批准',
    created_at: '2024-09-01T08:00:00',
    reviewed_at: '2024-09-01T09:00:00',
    attachments: [],
  },
  {
    id: 2,
    user_id: 2,
    username: 'zhangsan',
    requested_address: 'zhangsan@wic.edu.kg',
    display_name: '张三的邮箱',
    status: 'approved',
    reason: '个人学习使用',
    review_comment: null,
    created_at: '2024-09-08T10:00:00',
    reviewed_at: '2024-09-10T14:00:00',
    attachments: [
      { id: 1, filename: '学生证正面.jpg', content_type: 'image/jpeg', size: 245760, url: null },
      { id: 2, filename: '校园卡.jpg', content_type: 'image/jpeg', size: 189440, url: null },
    ],
  },
  {
    id: 3,
    user_id: 2,
    username: 'zhangsan',
    requested_address: 'lab@wic.edu.kg',
    display_name: '实验室公共邮箱',
    status: 'approved',
    reason: '实验室项目通讯',
    review_comment: null,
    created_at: '2024-09-12T16:00:00',
    reviewed_at: '2024-09-15T09:00:00',
    attachments: [
      { id: 3, filename: '导师审批表.pdf', content_type: 'application/pdf', size: 512000, url: null },
    ],
  },
  {
    id: 4,
    user_id: 3,
    username: 'lisi',
    requested_address: 'lisi@wic.edu.kg',
    display_name: '李四的邮箱',
    status: 'pending',
    reason: '课程作业需要',
    review_comment: null,
    created_at: '2024-09-20T08:30:00',
    reviewed_at: null,
    attachments: [
      { id: 4, filename: '录取通知书.jpg', content_type: 'image/jpeg', size: 327680, url: null },
      { id: 5, filename: '学生证正面.jpg', content_type: 'image/jpeg', size: 215040, url: null },
      { id: 6, filename: '学生证反面.jpg', content_type: 'image/jpeg', size: 198656, url: null },
    ],
  },
  {
    id: 5,
    user_id: 3,
    username: 'lisi',
    requested_address: 'test123@wic.edu.kg',
    display_name: null,
    status: 'rejected',
    reason: '测试用途',
    review_comment: '邮箱前缀不符合规范，请使用真实姓名拼音',
    created_at: '2024-09-18T15:00:00',
    reviewed_at: '2024-09-19T10:00:00',
    attachments: [],
  },
]

// ============ 邮件数据 ============
const emails = [
  {
    id: 1,
    mailbox_id: 1,
    mailbox_address: 'admin@wic.edu.kg',
    subject: '欢迎使用 WicMail 校园邮箱服务',
    header_from: 'noreply@wic.edu.kg',
    header_to: 'admin@wic.edu.kg',
    header_cc: null,
    header_reply_to: null,
    envelope_from: 'noreply@wic.edu.kg',
    envelope_to: 'admin@wic.edu.kg',
    message_id: '<welcome-001@wic.edu.kg>',
    body_text: '欢迎使用 WicMail 校园邮箱服务！您的邮箱已成功开通。',
    body_html: '<div style="font-family: sans-serif; padding: 20px;"><h2 style="color: #4f46e5;">欢迎使用 WicMail</h2><p>您的邮箱 <strong>admin@wic.edu.kg</strong> 已成功开通。</p><p>您可以开始收发邮件了！</p><hr><p style="color: #999; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p></div>',
    parse_status: 'success',
    is_read: true,
    sent_at: '2024-09-01T09:00:00',
    received_at: '2024-09-01T09:00:01',
    raw_size: 2048,
    attachments: [],
  },
  {
    id: 2,
    mailbox_id: 1,
    mailbox_address: 'admin@wic.edu.kg',
    subject: '【系统通知】邮箱服务维护公告',
    header_from: 'system@wic.edu.kg',
    header_to: 'admin@wic.edu.kg',
    header_cc: null,
    header_reply_to: null,
    envelope_from: 'system@wic.edu.kg',
    envelope_to: 'admin@wic.edu.kg',
    message_id: '<notice-002@wic.edu.kg>',
    body_text: '系统将于本周六凌晨2:00-4:00进行例行维护，届时邮件服务将短暂中断。',
    body_html: '<div style="font-family: sans-serif; padding: 20px;"><h3 style="color: #e11d48;">系统维护通知</h3><p>尊敬的用户：</p><p>系统将于 <strong>本周六凌晨 2:00-4:00</strong> 进行例行维护，届时邮件服务将短暂中断。</p><p>给您带来的不便，敬请谅解。</p></div>',
    parse_status: 'success',
    is_read: false,
    sent_at: '2024-09-25T10:00:00',
    received_at: '2024-09-25T10:00:02',
    raw_size: 1536,
    attachments: [],
  },
  {
    id: 3,
    mailbox_id: 2,
    mailbox_address: 'zhangsan@wic.edu.kg',
    subject: 'Re: 课程项目讨论',
    header_from: 'wangwu@gmail.com',
    header_to: 'zhangsan@wic.edu.kg',
    header_cc: 'zhaoliu@163.com',
    header_reply_to: 'wangwu@gmail.com',
    envelope_from: 'wangwu@gmail.com',
    envelope_to: 'zhangsan@wic.edu.kg',
    message_id: '<msg-003@gmail.com>',
    body_text: '张三你好，关于课程项目的分工我已经整理了一份文档，请查看附件。',
    body_html: '<div style="font-family: sans-serif; padding: 20px;"><p>张三你好，</p><p>关于课程项目的分工我已经整理了一份文档，请查看附件。</p><p>主要内容包括：</p><ol><li>前端模块 - 由你负责</li><li>后端模块 - 由我负责</li><li>测试与部署 - 共同完成</li></ol><p>请在周五前确认你的部分，谢谢！</p><p>王五</p></div>',
    parse_status: 'success',
    is_read: false,
    sent_at: '2024-09-24T14:30:00',
    received_at: '2024-09-24T14:30:05',
    raw_size: 15360,
    attachments: [
      { id: 1, filename: '项目分工方案.pdf', content_type: 'application/pdf', size: 102400 },
      { id: 2, filename: '进度计划.xlsx', content_type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', size: 51200 },
    ],
  },
  {
    id: 4,
    mailbox_id: 2,
    mailbox_address: 'zhangsan@wic.edu.kg',
    subject: 'GitHub: Your personal access token will expire in 7 days',
    header_from: 'noreply@github.com',
    header_to: 'zhangsan@wic.edu.kg',
    header_cc: null,
    header_reply_to: null,
    envelope_from: 'noreply@github.com',
    envelope_to: 'zhangsan@wic.edu.kg',
    message_id: '<msg-004@github.com>',
    body_text: 'Your personal access token "WicMail CI" will expire on October 1, 2024.',
    body_html: '<div style="font-family: sans-serif; padding: 20px; background: #f6f8fa;"><div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px;"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="32"><h3>Personal access token expiring</h3><p>Your personal access token <strong>"WicMail CI"</strong> will expire on <strong>October 1, 2024</strong>.</p><p><a href="#" style="background: #2da44e; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none;">Regenerate token</a></p></div></div>',
    parse_status: 'success',
    is_read: true,
    sent_at: '2024-09-23T08:00:00',
    received_at: '2024-09-23T08:00:03',
    raw_size: 8192,
    attachments: [],
  },
  {
    id: 5,
    mailbox_id: 3,
    mailbox_address: 'lab@wic.edu.kg',
    subject: '实验室周报 - 第38周',
    header_from: 'professor.liu@wic.edu.kg',
    header_to: 'lab@wic.edu.kg',
    header_cc: null,
    header_reply_to: 'professor.liu@wic.edu.kg',
    envelope_from: 'professor.liu@wic.edu.kg',
    envelope_to: 'lab@wic.edu.kg',
    message_id: '<msg-005@wic.edu.kg>',
    body_text: '各位同学好，请在本周五前提交第38周的实验报告。',
    body_html: '<div style="font-family: sans-serif; padding: 20px;"><p>各位同学好，</p><p>请在本周五前提交第38周的实验报告，报告格式请参考上周的模板。</p><p>本周重点：</p><ul><li>完成模型训练实验</li><li>整理实验数据</li><li>撰写实验分析</li></ul><p>刘老师</p></div>',
    parse_status: 'success',
    is_read: false,
    sent_at: '2024-09-22T09:15:00',
    received_at: '2024-09-22T09:15:02',
    raw_size: 4096,
    attachments: [
      { id: 3, filename: '周报模板.docx', content_type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', size: 25600 },
    ],
  },
  {
    id: 6,
    mailbox_id: 1,
    mailbox_address: 'admin@wic.edu.kg',
    subject: '新的邮箱申请待审核',
    header_from: 'noreply@wic.edu.kg',
    header_to: 'admin@wic.edu.kg',
    header_cc: null,
    header_reply_to: null,
    envelope_from: 'noreply@wic.edu.kg',
    envelope_to: 'admin@wic.edu.kg',
    message_id: '<notify-006@wic.edu.kg>',
    body_text: '用户 lisi 提交了一个新的邮箱申请，请及时审核。',
    body_html: '<div style="font-family: sans-serif; padding: 20px;"><h3>新申请通知</h3><p>用户 <strong>lisi</strong> 提交了一个新的邮箱申请：</p><ul><li>申请地址：lisi@wic.edu.kg</li><li>申请理由：课程作业需要</li><li>提交时间：2024-09-20 08:30</li></ul><p>请登录管理后台进行审核。</p></div>',
    parse_status: 'success',
    is_read: false,
    sent_at: '2024-09-20T08:30:01',
    received_at: '2024-09-20T08:30:03',
    raw_size: 1024,
    attachments: [],
  },
]

// ============ 模拟登录凭证 ============
const credentials = {
  admin: { password: 'admin123', userId: 1 },
  zhangsan: { password: '123456', userId: 2 },
  lisi: { password: '123456', userId: 3 },
}

// ============ Mock API 方法 ============
const delay = (ms = 200) => new Promise(resolve => setTimeout(resolve, ms))

let tokenCounter = 0

export const mockApi = {
  // ---- 认证 ----
  async register({ username, student_id, password }) {
    await delay()
    if (!username || username.length < 3 || username.length > 50) {
      return Promise.reject({ code: 400, message: '用户名长度需在 3 到 50 个字符之间' })
    }
    if (!/^[a-z0-9_-]+$/.test(username)) {
      return Promise.reject({ code: 400, message: '用户名只能包含小写字母、数字、下划线和横线' })
    }
    if (!student_id || student_id.length > 20) {
      return Promise.reject({ code: 400, message: '学号格式不正确' })
    }
    const upperStudentId = student_id.toUpperCase()
    if (!/^[A-Z0-9]+$/.test(upperStudentId)) {
      return Promise.reject({ code: 400, message: '学号只能包含字母和数字' })
    }
    if (!password || password.length < 6 || password.length > 100) {
      return Promise.reject({ code: 400, message: '密码长度需在 6 到 100 个字符之间' })
    }
    if (users.some(u => u.username === username)) {
      return Promise.reject({ code: 400, message: '用户名已存在' })
    }
    if (users.some(u => u.student_id === upperStudentId)) {
      return Promise.reject({ code: 400, message: '该学号已被注册' })
    }
    const newUser = {
      id: users.length + 1,
      username,
      student_id: upperStudentId,
      email: null,
      real_name: null,
      department: null,
      major: null,
      class_name: null,
      grade: null,
      is_active: true,
      is_admin: false,
      profile_complete: false,
      missing_fields: ['邮箱', '真实姓名', '学部', '专业', '班级', '年级'],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    users.push(newUser)
    credentials[username] = { password, userId: newUser.id }
    return { code: 0, data: newUser }
  },

  async login({ username, password }) {
    await delay()
    const cred = credentials[username]
    if (!cred || cred.password !== password) {
      return Promise.reject({ code: 401, message: '用户名或密码错误' })
    }
    const user = users.find(u => u.id === cred.userId)
    if (!user.is_active) {
      return Promise.reject({ code: 403, message: '账号已被禁用' })
    }
    tokenCounter++
    return {
      code: 0,
      data: {
        accessToken: `mock-token-${username}-${tokenCounter}`,
      },
    }
  },

  async getUserDetail(token) {
    await delay()
    const username = token?.replace('mock-token-', '')?.split('-')[0]
    const user = users.find(u => u.username === username)
    if (!user)
      return Promise.reject({ code: 401, message: '未登录' })
    return {
      code: 0,
      data: {
        id: user.id,
        username: user.username,
        profile: {
          avatar: null,
          nickName: user.real_name || user.username,
          email: user.email,
        },
        roles: user.is_admin
          ? [{ code: 'admin', name: '管理员' }]
          : [{ code: 'user', name: '普通用户' }],
        currentRole: user.is_admin
          ? { code: 'admin', name: '管理员' }
          : { code: 'user', name: '普通用户' },
      },
    }
  },

  async getProfile(token) {
    await delay()
    const username = token?.replace('mock-token-', '')?.split('-')[0]
    const user = users.find(u => u.username === username)
    if (!user)
      return Promise.reject({ code: 401, message: '未登录' })
    return { code: 0, data: user }
  },

  async updateProfile(token, data) {
    await delay()
    const username = token?.replace('mock-token-', '')?.split('-')[0]
    const user = users.find(u => u.username === username)
    if (!user)
      return Promise.reject({ code: 401, message: '未登录' })
    Object.assign(user, data)
    return { code: 0, data: user }
  },

  async getRolePermissions() {
    await delay()
    // 返回空数组，菜单由 basePermissions 提供
    return { code: 0, data: [] }
  },

  // ---- 邮箱 ----
  async applyMailbox(data) {
    await delay()
    const attachments = (data.attachments || []).map(file => ({
      id: ++attachmentIdCounter,
      filename: file.name || file.filename,
      content_type: file.type || file.content_type || 'application/octet-stream',
      size: file.size || 0,
      url: file.url || null,
    }))
    const app = {
      id: applications.length + 1,
      user_id: 2,
      username: 'zhangsan',
      requested_address: `${data.prefix}@wic.edu.kg`,
      display_name: data.display_name || null,
      status: 'pending',
      reason: data.reason || null,
      review_comment: null,
      created_at: new Date().toISOString(),
      reviewed_at: null,
      attachments,
    }
    applications.push(app)
    return { code: 0, data: app }
  },

  async getMyApplications() {
    await delay()
    const myApps = applications.filter(a => a.user_id === 2)
    return { code: 0, data: { total: myApps.length, applications: myApps } }
  },

  async getMyMailboxes() {
    await delay()
    return { code: 0, data: mailboxes.filter(m => m.address !== 'lab@wic.edu.kg' || true) }
  },

  // ---- 邮件 ----
  async getEmails({ page = 1, page_size = 20 } = {}) {
    await delay()
    const start = (page - 1) * page_size
    const paged = emails.slice(start, start + page_size)
    return {
      code: 0,
      data: {
        total: emails.length,
        page,
        page_size,
        emails: paged.map(e => ({
          id: e.id,
          mailbox_address: e.mailbox_address,
          subject: e.subject,
          header_from: e.header_from,
          header_to: e.header_to,
          envelope_from: e.envelope_from,
          envelope_to: e.envelope_to,
          received_at: e.received_at,
          is_read: e.is_read,
          attachment_count: e.attachments.length,
        })),
      },
    }
  },

  async getEmailDetail(id) {
    await delay()
    const email = emails.find(e => e.id === id)
    if (!email)
      return Promise.reject({ code: 404, message: '邮件不存在' })
    return { code: 0, data: email }
  },

  async markEmailRead(id) {
    await delay()
    const email = emails.find(e => e.id === id)
    if (email)
      email.is_read = true
    return { code: 0, data: { status: 'ok', email_id: id, is_read: true } }
  },

  async markEmailUnread(id) {
    await delay()
    const email = emails.find(e => e.id === id)
    if (email)
      email.is_read = false
    return { code: 0, data: { status: 'ok', email_id: id, is_read: false } }
  },

  // ---- 管理员 ----
  async getAdminApplications(status) {
    await delay()
    let result = [...applications]
    if (status)
      result = result.filter(a => a.status === status)
    return { code: 0, data: result }
  },

  async approveApplication(id, comment) {
    await delay()
    const app = applications.find(a => a.id === id)
    if (!app)
      return Promise.reject({ code: 404, message: '申请不存在' })
    if (app.status !== 'pending')
      return Promise.reject({ code: 400, message: `申请已处理（当前状态: ${app.status}）` })
    app.status = 'approved'
    app.review_comment = comment || null
    app.reviewed_at = new Date().toISOString()
    const newMailbox = {
      id: mailboxes.length + 1,
      address: app.requested_address,
      display_name: app.display_name,
      is_active: true,
      created_at: new Date().toISOString(),
    }
    mailboxes.push(newMailbox)
    return { code: 0, data: { status: 'ok', message: `已批准: ${app.requested_address}`, mailbox_id: newMailbox.id } }
  },

  async rejectApplication(id, comment) {
    await delay()
    const app = applications.find(a => a.id === id)
    if (!app)
      return Promise.reject({ code: 404, message: '申请不存在' })
    if (app.status !== 'pending')
      return Promise.reject({ code: 400, message: `申请已处理（当前状态: ${app.status}）` })
    app.status = 'rejected'
    app.review_comment = comment || null
    app.reviewed_at = new Date().toISOString()
    return { code: 0, data: { status: 'ok', message: `已拒绝: ${app.requested_address}` } }
  },

  async getAdminUsers() {
    await delay()
    return { code: 0, data: users.map(u => ({ id: u.id, username: u.username, email: u.email, is_active: u.is_active, is_admin: u.is_admin, created_at: u.created_at })) }
  },

  async toggleUserActive(userId) {
    await delay()
    const user = users.find(u => u.id === userId)
    if (!user)
      return Promise.reject({ code: 404, message: '用户不存在' })
    user.is_active = !user.is_active
    const action = user.is_active ? '启用' : '禁用'
    return { code: 0, data: { status: 'ok', message: `已${action}用户: ${user.username}`, is_active: user.is_active } }
  },
}

export const isMock = () => import.meta.env.VITE_USE_MOCK === 'true'
