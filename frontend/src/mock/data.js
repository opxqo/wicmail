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
      { id: 1, filename: '项目分工方案.pdf', content_type: 'application/pdf', size: 102400, has_file: true },
      { id: 2, filename: '进度计划.xlsx', content_type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', size: 51200, has_file: true },
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
      { id: 3, filename: '周报模板.docx', content_type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', size: 25600, has_file: false },
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

// ============ 日志数据 ============
const logs = [
  { id: 1, admin_id: 1, admin_username: 'admin', action: 'approve_application', target_type: 'application', target_id: 2, target_name: 'zhangsan@wic.edu.kg', detail: '批准邮箱申请: zhangsan@wic.edu.kg', ip_address: '192.168.1.1', created_at: '2024-09-10T14:00:00' },
  { id: 2, admin_id: 1, admin_username: 'admin', action: 'toggle_user_active', target_type: 'user', target_id: 3, target_name: 'lisi', detail: '启用用户: lisi', ip_address: '192.168.1.1', created_at: '2024-09-20T09:00:00' },
  { id: 3, admin_id: 1, admin_username: 'admin', action: 'update_config', target_type: 'config', target_id: 0, target_name: 'application_enabled', detail: '修改配置 application_enabled 为 true', ip_address: '192.168.1.1', created_at: '2024-09-21T10:30:00' },
]

// ============ 配置数据 ============
const configs = [
  { key: 'mailbox_domain', value: 'wic.edu.kg', description: '邮箱域名' },
  { key: 'application_enabled', value: 'true', description: '是否开放申请' },
  { key: 'max_mailboxes_per_user', value: '3', description: '每人最大邮箱数' },
  { key: 'max_attachment_size_mb', value: '10', description: '单附件大小限制(MB)' },
  { key: 'application_require_profile', value: 'true', description: '申请前是否需完善资料' },
]

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
          avatar: user.avatar_url || null,
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
  async getEmails({ page = 1, page_size = 20, q, sender, is_read } = {}) {
    await delay()
    let filtered = [...emails]
    if (q) {
      const kw = q.toLowerCase()
      filtered = filtered.filter(e =>
        (e.header_from && e.header_from.toLowerCase().includes(kw))
        || (e.subject && e.subject.toLowerCase().includes(kw))
        || (e.body_text && e.body_text.toLowerCase().includes(kw))
        || (e.body_html && e.body_html.toLowerCase().includes(kw)),
      )
    }
    if (sender) {
      const s = sender.toLowerCase()
      filtered = filtered.filter(e => e.header_from && e.header_from.toLowerCase().includes(s))
    }
    if (is_read !== undefined && is_read !== null && is_read !== '') {
      const readVal = String(is_read) === 'true'
      filtered = filtered.filter(e => e.is_read === readVal)
    }
    const start = (page - 1) * page_size
    const paged = filtered.slice(start, start + page_size)
    return {
      code: 0,
      data: {
        total: filtered.length,
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
          attachment_count: e.attachments?.length || 0,
        })),
      },
    }
  },

  async getUnreadCount() {
    await delay()
    const count = emails.filter(e => !e.is_read).length
    return {
      code: 0,
      data: {
        unread_count: count,
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

  async downloadAttachment(id) {
    await delay()
    const attachment = emails
      .flatMap(e => e.attachments || [])
      .find(att => att.id === id)
    if (!attachment || !attachment.has_file)
      return Promise.reject({ code: 404, message: '附件文件不可用' })
    return {
      code: 0,
      data: {
        download_url: 'https://example.com/mock-download',
        filename: attachment.filename,
        content_type: attachment.content_type,
        size: attachment.size,
        expires_in: 3600,
      },
    }
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

  async deleteUser(userId) {
    await delay()
    const idx = users.findIndex(u => u.id === userId)
    if (idx === -1)
      return Promise.reject({ code: 404, message: '用户不存在' })
    const user = users[idx]
    users.splice(idx, 1)
    return { code: 0, data: { status: 'ok', message: `已删除用户: ${user.username}` } }
  },

  // ---- 管理员 — 邮箱 ----
  async getAdminMailboxes({ q, is_active } = {}) {
    await delay()
    let result = [...mailboxes]
    if (q) {
      const kw = q.toLowerCase()
      result = result.filter(m => m.address.toLowerCase().includes(kw) || (m.display_name && m.display_name.toLowerCase().includes(kw)))
    }
    if (is_active !== undefined && is_active !== null && is_active !== '') {
      const activeVal = String(is_active) === 'true'
      result = result.filter(m => m.is_active === activeVal)
    }
    return { code: 0, data: result }
  },

  async getAdminMailboxDetail(id) {
    await delay()
    const m = mailboxes.find(item => item.id === Number(id))
    if (!m)
      return Promise.reject({ code: 404, message: '邮箱不存在' })
    const owner = users.find(u => u.email === m.address) || users[0]
    const emailCount = emails.filter(e => e.mailbox_address === m.address).length
    const unreadCount = emails.filter(e => e.mailbox_address === m.address && !e.is_read).length
    return {
      code: 0,
      data: {
        ...m,
        email_count: emailCount,
        unread_count: unreadCount,
        owner_username: owner.username,
        owner_user_id: owner.id,
      },
    }
  },

  async createAdminMailbox(data) {
    await delay()
    if (mailboxes.some(m => m.address === data.address)) {
      return Promise.reject({ code: 400, message: '该邮箱地址已存在' })
    }
    const newMailbox = {
      id: mailboxes.length + 1,
      address: data.address,
      display_name: data.display_name || '系统分配邮箱',
      is_active: true,
      created_at: new Date().toISOString(),
    }
    mailboxes.push(newMailbox)
    return { code: 0, data: newMailbox }
  },

  async toggleMailboxActive(id) {
    await delay()
    const m = mailboxes.find(item => item.id === Number(id))
    if (!m)
      return Promise.reject({ code: 404, message: '邮箱不存在' })
    m.is_active = !m.is_active
    const state = m.is_active ? '启用' : '停用'
    return { code: 0, data: { status: 'ok', message: `已${state}邮箱: ${m.address}`, is_active: m.is_active } }
  },

  async deleteMailbox(id) {
    await delay()
    const idx = mailboxes.findIndex(item => item.id === Number(id))
    if (idx === -1)
      return Promise.reject({ code: 404, message: '邮箱不存在' })
    const m = mailboxes[idx]
    mailboxes.splice(idx, 1)
    return { code: 0, data: { status: 'ok', message: `已删除邮箱: ${m.address}` } }
  },

  // ---- 管理员 — 邮件 ----
  async getAdminEmails({ page = 1, page_size = 20, q, sender, is_read } = {}) {
    await delay()
    let filtered = [...emails]
    if (q) {
      const kw = q.toLowerCase()
      filtered = filtered.filter(e =>
        (e.header_from && e.header_from.toLowerCase().includes(kw))
        || (e.subject && e.subject.toLowerCase().includes(kw))
        || (e.body_text && e.body_text.toLowerCase().includes(kw))
        || (e.body_html && e.body_html.toLowerCase().includes(kw)),
      )
    }
    if (sender) {
      const s = sender.toLowerCase()
      filtered = filtered.filter(e => e.header_from && e.header_from.toLowerCase().includes(s))
    }
    if (is_read !== undefined && is_read !== null && is_read !== '') {
      const readVal = String(is_read) === 'true'
      filtered = filtered.filter(e => e.is_read === readVal)
    }
    const start = (page - 1) * page_size
    const paged = filtered.slice(start, start + page_size)
    return {
      code: 0,
      data: {
        total: filtered.length,
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
          attachment_count: e.attachments?.length || 0,
          raw_size: e.raw_size || 1024,
        })),
      },
    }
  },

  async searchAdminEmails(params = {}) {
    return this.getAdminEmails(params)
  },

  async getAdminEmailDetail(id) {
    return this.getEmailDetail(id)
  },

  async deleteAdminEmail(id) {
    await delay()
    const idx = emails.findIndex(e => e.id === Number(id))
    if (idx === -1)
      return Promise.reject({ code: 404, message: '邮件不存在' })
    emails.splice(idx, 1)
    return { code: 0, data: { status: 'ok', message: `已删除邮件 #${id}` } }
  },

  async batchDeleteAdminEmails(ids) {
    await delay()
    let count = 0
    const deletedIds = []
    ids.forEach((id) => {
      const idx = emails.findIndex(e => e.id === Number(id))
      if (idx !== -1) {
        emails.splice(idx, 1)
        deletedIds.push(id)
        count++
      }
    })
    return { code: 0, data: { status: 'ok', deleted: deletedIds, count } }
  },

  // ---- 管理员 — 统计 ----
  async getAdminStatsOverview() {
    await delay()
    const totalUsers = users.length
    const activeUsers = users.filter(u => u.is_active).length
    const totalMailboxes = mailboxes.length
    const activeMailboxes = mailboxes.filter(m => m.is_active).length
    const totalEmails = emails.length
    const unreadEmails = emails.filter(e => !e.is_read).length
    const totalApplications = applications.length
    const pendingApplications = applications.filter(a => a.status === 'pending').length
    const totalAttachments = emails.reduce((sum, e) => sum + (e.attachments?.length || 0), 0)
    return {
      code: 0,
      data: {
        total_users: totalUsers,
        active_users: activeUsers,
        total_mailboxes: totalMailboxes,
        active_mailboxes: activeMailboxes,
        total_emails: totalEmails,
        unread_emails: unreadEmails,
        total_applications: totalApplications,
        pending_applications: pendingApplications,
        total_attachments: totalAttachments,
        today_new_users: 2,
        today_new_emails: 8,
      },
    }
  },

  async getAdminStatsUsers(days = 30) {
    await delay()
    const result = []
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      const dateStr = date.toISOString().slice(0, 10)
      const count = Math.floor(Math.sin(i / 3) * 3 + 5) + (i % 5 === 0 ? 3 : 0)
      result.push({ date: dateStr, count: Math.max(0, count) })
    }
    return { code: 0, data: result }
  },

  async getAdminStatsEmails(days = 30) {
    await delay()
    const result = []
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      const dateStr = date.toISOString().slice(0, 10)
      const count = Math.floor(Math.cos(i / 2) * 15 + 25) + (i % 7 === 0 ? 12 : 0)
      result.push({ date: dateStr, count: Math.max(0, count) })
    }
    return { code: 0, data: result }
  },

  async getAdminStatsApplications() {
    await delay()
    const counts = { pending: 0, approved: 0, rejected: 0 }
    applications.forEach((a) => {
      if (counts[a.status] !== undefined)
        counts[a.status]++
    })
    return {
      code: 0,
      data: [
        { status: 'pending', count: counts.pending },
        { status: 'approved', count: counts.approved },
        { status: 'rejected', count: counts.rejected },
      ],
    }
  },

  async getAdminStatsMailboxes(limit = 20) {
    await delay()
    const result = mailboxes.map((m) => {
      const count = emails.filter(e => e.mailbox_address === m.address).length
      const unread = emails.filter(e => e.mailbox_address === m.address && !e.is_read).length
      return {
        id: m.id,
        address: m.address,
        email_count: count,
        unread_count: unread,
      }
    })
    result.sort((a, b) => b.email_count - a.email_count)
    return { code: 0, data: result.slice(0, limit) }
  },

  async getAdminStatsStorage() {
    await delay()
    const totalSize = emails.reduce((sum, e) => sum + (e.raw_size || 1024), 0) + 12048576
    return {
      code: 0,
      data: {
        total_size_bytes: totalSize,
        total_size_mb: Number((totalSize / (1024 * 1024)).toFixed(2)),
        total_attachments: emails.reduce((sum, e) => sum + (e.attachments?.length || 0), 0) + 12,
        avg_email_size_bytes: Math.floor(totalSize / (emails.length + 10)),
      },
    }
  },

  // ---- 管理员 — 日志 ----
  async getAdminLogs({ page = 1, page_size = 20, action, target_type, admin_username, start_date, end_date } = {}) {
    await delay()
    let result = [...logs]
    if (action)
      result = result.filter(l => l.action === action)
    if (target_type)
      result = result.filter(l => l.target_type === target_type)
    if (admin_username)
      result = result.filter(l => l.admin_username.toLowerCase().includes(admin_username.toLowerCase()))
    if (start_date)
      result = result.filter(l => l.created_at >= start_date)
    if (end_date)
      result = result.filter(l => l.created_at <= `${end_date}T23:59:59`)

    const start = (page - 1) * page_size
    const paged = result.slice(start, start + page_size)
    return {
      code: 0,
      data: {
        total: result.length,
        page,
        page_size,
        logs: paged,
      },
    }
  },

  // ---- 管理员 — 配置 ----
  async getAdminConfigs() {
    await delay()
    return { code: 0, data: configs }
  },

  async updateAdminConfigs(configsInput) {
    await delay()
    const updatedKeys = []
    Object.keys(configsInput).forEach((key) => {
      const item = configs.find(c => c.key === key)
      if (item) {
        item.value = String(configsInput[key])
        updatedKeys.push(key)

        // 同时模拟生成一条操作日志
        logs.unshift({
          id: logs.length + 1,
          admin_id: 1,
          admin_username: 'admin',
          action: 'update_config',
          target_type: 'config',
          target_id: 0,
          target_name: key,
          detail: `修改配置 ${key} 为 ${configsInput[key]}`,
          ip_address: '127.0.0.1',
          created_at: new Date().toISOString(),
        })
      }
    })
    return { code: 0, data: { status: 'ok', updated: updatedKeys } }
  },

  async testCloudflareConnection() {
    await delay(600)
    return {
      code: 0,
      data: {
        status: 'ok',
        message: 'Cloudflare Email Worker 服务可达',
        data: { ping: 'pong', timestamp: Date.now(), worker_version: '1.2.0' },
      },
    }
  },

  async checkDomainDns() {
    await delay(500)
    return {
      code: 0,
      data: {
        domain: 'wic.edu.kg',
        checks: {
          mx: ['10 mx1.cloudflare.net', '20 mx2.cloudflare.net'],
          a: ['172.67.200.10', '104.21.75.80'],
          resolved_ip: '104.21.75.80',
        },
      },
    }
  },

  // ---- 管理员 — 管理员管理 ----
  async getAdminList() {
    await delay()
    const adminUsers = users.filter(u => u.is_admin)
    return { code: 0, data: adminUsers }
  },

  async addAdmin(usernameInput) {
    await delay()
    const user = users.find(u => u.username === usernameInput)
    if (!user)
      return Promise.reject({ code: 404, message: '找不到此用户，请先确保用户已注册' })
    if (user.is_admin)
      return Promise.reject({ code: 400, message: '该用户已经是管理员' })
    user.is_admin = true
    return { code: 0, data: user }
  },

  async removeAdmin(id) {
    await delay()
    const user = users.find(u => u.id === Number(id))
    if (!user)
      return Promise.reject({ code: 404, message: '管理员不存在' })
    user.is_admin = false
    return { code: 0, data: { status: 'ok', message: `已移除 ${user.username} 的管理员权限` } }
  },

  async updateAdminRole(id, data) {
    await delay()
    const user = users.find(u => u.id === Number(id))
    if (!user)
      return Promise.reject({ code: 404, message: '用户不存在' })
    if (data.is_admin !== undefined) {
      user.is_admin = data.is_admin
    }
    return { code: 0, data: { status: 'ok', message: `已更新用户 ${user.username} 角色属性` } }
  },
}

export const isMock = () => import.meta.env.VITE_USE_MOCK === 'true'
