# WicMail API 文档

> Base URL: `https://wicmail-api.opxqo.cn`
> 
> 认证方式: `Authorization: Bearer <access_token>`
> 
> 所有响应均为 JSON 格式，错误返回 `{"detail": "错误信息"}`

---

## 通用说明

| 认证标记 | 说明 |
|---------|------|
| 🔓 | 无需认证 |
| 🔑 | 需要 JWT |
| 👑 | 需要 JWT + 管理员权限 |

---

## 1. 认证 `/api/auth`

### 1.1 `POST /api/auth/register` — 注册 🔓

**Request:**
```json
{ "username": "zhang_san", "student_id": "2021001", "password": "securepass123" }
```
| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| username | string | ✅ | 3-50字符，`^[a-z0-9_-]+$` |
| student_id | string | ✅ | 1-20字符，自动转大写 |
| password | string | ✅ | 6-100字符 |

**Response `201`:**
```json
{ "id": 1, "username": "zhang_san", "student_id": "2021001", "email": null, "avatar_url": null, "real_name": null, "is_active": true, "is_admin": false }
```

### 1.2 `POST /api/auth/login` — 登录 🔓

**Request:**
```json
{ "username": "zhang_san", "password": "securepass123" }
```

**Response `200`:**
```json
{ "access_token": "eyJhbGciOiJIUzI1NiIs...", "token_type": "bearer" }
```

### 1.3 `GET /api/auth/me` — 当前用户信息 🔑

**Response `200`:**
```json
{ "id": 1, "username": "zhang_san", "student_id": "2021001", "email": "zhang@example.com", "avatar_url": "https://...", "real_name": "张三", "is_active": true, "is_admin": false }
```

### 1.4 `GET /api/auth/profile` — 完整资料 🔑

**Response `200`:**
```json
{ "id": 1, "username": "zhang_san", "student_id": "2021001", "email": "zhang@example.com", "avatar_url": "https://...", "real_name": "张三", "department": "计算机系", "major": "软件工程", "class_name": "软工2101", "grade": "2021", "profile_complete": true, "missing_fields": [], "is_active": true, "is_admin": false }
```

### 1.5 `PATCH /api/auth/profile` — 更新资料 🔑

**Request（所有字段可选，部分更新）:**
```json
{ "real_name": "张三", "department": "计算机系", "avatar_url": "https://api.dicebear.com/..." }
```
| 字段 | 类型 | 约束 |
|------|------|------|
| email | string? | 合法邮箱格式 |
| avatar_url | string? | 最大500字符 |
| real_name | string? | 1-50字符 |
| department | string? | 1-100字符 |
| major | string? | 1-100字符 |
| class_name | string? | 1-50字符 |
| grade | string? | 1-10字符 |

**Response `200`:** 同 1.4

### 1.6 `POST /api/auth/change-password` — 修改密码 🔑

**Request:**
```json
{ "old_password": "oldpass123", "new_password": "newpass456" }
```

**Response `200`:**
```json
{ "status": "ok", "message": "密码修改成功" }
```

---

## 2. 邮箱 `/api/mailbox`

### 2.1 `POST /api/mailbox/apply` — 申请邮箱 🔑

**Request:**
```json
{ "prefix": "zhangsan", "display_name": "Zhang San", "reason": "学习需要" }
```
| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| prefix | string | ✅ | 3-30字符 |
| display_name | string? | ❌ | |
| reason | string? | ❌ | |

**Response `201`:**
```json
{ "id": 1, "requested_address": "zhangsan@wic.edu.kg", "display_name": "Zhang San", "status": "pending", "reason": "学习需要", "review_comment": null, "created_at": "2026-06-12T10:00:00", "reviewed_at": null }
```

### 2.2 `GET /api/mailbox/applications` — 我的申请列表 🔑

**Response `200`:**
```json
{ "total": 2, "applications": [{ "id": 1, "requested_address": "zhangsan@wic.edu.kg", "display_name": "Zhang San", "status": "pending", "reason": "学习需要", "review_comment": null, "created_at": "2026-06-12T10:00:00", "reviewed_at": null }] }
```

### 2.3 `GET /api/mailbox` — 我的已批准邮箱 🔑

**Response `200`:**
```json
[{ "id": 1, "address": "zhangsan@wic.edu.kg", "display_name": "Zhang San", "is_active": true, "created_at": "2026-06-12T10:00:00" }]
```

---

## 3. 邮件 `/api/emails`

### 3.1 `GET /api/emails` — 我的邮件列表 🔑

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| page | int | ❌ | 1 | ≥1 |
| page_size | int | ❌ | 20 | 1-100 |
| q | string | ❌ | - | 搜索关键词（发件人/主题/正文） |
| sender | string | ❌ | - | 按发件人筛选 |
| mailbox_id | int | ❌ | - | 按收件邮箱筛选 |
| is_read | bool | ❌ | - | 按已读/未读筛选 |

**Response `200`:**
```json
{ "total": 42, "page": 1, "page_size": 20, "emails": [{ "id": 101, "mailbox_address": "zhangsan@wic.edu.kg", "subject": "Welcome", "header_from": "admin@wic.edu.kg", "header_to": "zhangsan@wic.edu.kg", "envelope_from": "admin@wic.edu.kg", "envelope_to": "zhangsan@wic.edu.kg", "received_at": "2026-06-12T09:30:00", "is_read": false, "attachment_count": 1 }] }
```

### 3.2 `GET /api/emails/unread-count` — 未读数量 🔑

**Response `200`:**
```json
{ "unread_count": 5 }
```

### 3.3 `GET /api/emails/{email_id}` — 邮件详情 🔑

**Response `200`:**
```json
{ "id": 101, "mailbox_address": "zhangsan@wic.edu.kg", "subject": "Welcome", "header_from": "Admin <admin@wic.edu.kg>", "header_to": "zhangsan@wic.edu.kg", "header_cc": null, "header_reply_to": null, "envelope_from": "admin@wic.edu.kg", "envelope_to": "zhangsan@wic.edu.kg", "message_id": "<abc123@mail.wic.edu.kg>", "sent_at": "2026-06-12T09:28:00", "received_at": "2026-06-12T09:30:00", "raw_size": 15234, "body_text": "Hello ...", "body_html": "<p>Hello ...</p>", "parse_status": "completed", "is_read": false, "attachments": [{ "id": 1, "filename": "report.pdf", "content_type": "application/pdf", "size": 52400, "has_file": true }] }
```

### 3.4 `GET /api/emails/attachments/{attachment_id}/download` — 获取附件下载链接 🔑

仅允许下载当前用户已审批邮箱下邮件的 R2 附件。历史元数据附件没有实际文件时返回 `404`。

**Response `200`:**
```json
{ "download_url": "https://...", "filename": "report.pdf", "content_type": "application/pdf", "size": 52400, "expires_in": 3600 }
```

### 3.5 `PATCH /api/emails/{email_id}/read` — 标记已读 🔑

**Response `200`:** `{ "status": "ok", "email_id": 101, "is_read": true }`

### 3.6 `PATCH /api/emails/{email_id}/unread` — 标记未读 🔑

**Response `200`:** `{ "status": "ok", "email_id": 101, "is_read": false }`

---

## 4. 管理 — 用户 `/api/admin/users` 👑

### 4.1 `GET /api/admin/users` — 用户列表

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | ❌ | 默认1 |
| page_size | int | ❌ | 默认20，最大100 |
| q | string | ❌ | 搜索用户名/姓名/学号/邮箱 |
| is_active | bool | ❌ | 筛选启用/禁用 |
| is_admin | bool | ❌ | 筛选管理员 |

**Response `200`:**
```json
{ "total": 100, "page": 1, "page_size": 20, "users": [{ "id": 1, "username": "zhang_san", "student_id": "2021001", "email": "zhang@example.com", "avatar_url": null, "real_name": "张三", "department": "计算机系", "major": "软件工程", "class_name": "软工2101", "grade": "2021", "is_active": true, "is_admin": false, "created_at": "2026-06-01T08:00:00" }] }
```

### 4.2 `GET /api/admin/users/{user_id}` — 用户详情

**Response `200`:** 同 4.1 用户字段 + `"profile_complete": true, "missing_fields": [], "updated_at": "...", "mailbox_count": 1, "application_count": 2`

### 4.3 `PATCH /api/admin/users/{user_id}` — 修改用户

**Request（所有字段可选）:**
```json
{ "real_name": "李四", "is_active": false }
```
可改字段: email, real_name, department, major, class_name, grade, is_active, is_admin

### 4.4 `PATCH /api/admin/users/{user_id}/toggle-active` — 启用/禁用

**Response:** `{ "status": "ok", "message": "已禁用用户: zhang_san", "is_active": false }`

### 4.5 `DELETE /api/admin/users/{user_id}` — 删除用户

**Response:** `{ "status": "ok", "message": "已删除用户: zhang_san" }`

### 4.6 `POST /api/admin/users/{user_id}/reset-password` — 重置密码

**Request:** `{ "new_password": "newpass123" }`

**Response:** `{ "status": "ok", "message": "已重置用户 zhang_san 的密码" }`

---

## 5. 管理 — 申请审核 `/api/admin/applications` 👑

### 5.1 `GET /api/admin/applications` — 申请列表

| 参数 | 类型 | 说明 |
|------|------|------|
| status | string? | `pending` / `approved` / `rejected` |

**Response `200`:**
```json
[{ "id": 1, "user_id": 1, "username": "zhang_san", "requested_address": "zhangsan@wic.edu.kg", "display_name": "Zhang San", "status": "pending", "reason": "学习需要", "review_comment": null, "reviewed_at": null, "created_at": "2026-06-12T10:00:00" }]
```

### 5.2 `GET /api/admin/applications/{app_id}` — 申请详情

**Response `200`:** 同 5.1 + `"reviewed_by": null, "mailbox_id": null, "user_email": "...", "user_real_name": "...", "user_student_id": "..."`

### 5.3 `PATCH /api/admin/applications/{app_id}/approve` — 批准

**Request（可选）:** `{ "comment": "同意" }`

**Response:** `{ "status": "ok", "message": "已批准: zhangsan@wic.edu.kg" }`

### 5.4 `PATCH /api/admin/applications/{app_id}/reject` — 拒绝

**Request（可选）:** `{ "comment": "前缀不合规" }`

**Response:** `{ "status": "ok", "message": "已拒绝: zhangsan@wic.edu.kg" }`

### 5.5 `POST /api/admin/applications/batch-approve` — 批量批准

**Request:** `{ "ids": [1, 2, 3], "comment": "批量通过" }`

**Response:** `{ "status": "ok", "approved": ["a@wic.edu.kg", "b@wic.edu.kg"], "count": 2 }`

### 5.6 `POST /api/admin/applications/batch-reject` — 批量拒绝

**Request:** `{ "ids": [4, 5], "comment": "理由不充分" }`

**Response:** `{ "status": "ok", "rejected": ["c@wic.edu.kg"], "count": 1 }`

---

## 6. 管理 — 邮箱 `/api/admin/mailboxes` 👑

### 6.1 `GET /api/admin/mailboxes` — 邮箱列表

| 参数 | 类型 | 说明 |
|------|------|------|
| q | string? | 搜索邮箱地址 |
| is_active | bool? | 筛选启停 |

**Response `200`:** `[{ "id": 1, "address": "zhangsan@wic.edu.kg", "display_name": "...", "is_active": true, "created_at": "..." }]`

### 6.2 `GET /api/admin/mailboxes/{mailbox_id}` — 邮箱详情

**Response `200`:** 同 6.1 + `"email_count": 42, "unread_count": 5, "owner_username": "zhang_san", "owner_user_id": 1`

### 6.3 `POST /api/admin/mailboxes` — 创建邮箱

**Request:** `{ "address": "test@wic.edu.kg", "display_name": "Test" }`

**Response `201`:** 同 6.1 单个对象

### 6.4 `PATCH /api/admin/mailboxes/{mailbox_id}/toggle-active` — 启停

**Response:** `{ "status": "ok", "message": "已停用邮箱: ...", "is_active": false }`

### 6.5 `DELETE /api/admin/mailboxes/{mailbox_id}` — 删除

**Response:** `{ "status": "ok", "message": "已删除邮箱: ..." }`

---

## 7. 管理 — 邮件 `/api/admin/emails` 👑

### 7.1 `GET /api/admin/emails` — 所有邮件（跨用户）

| 参数 | 类型 | 说明 |
|------|------|------|
| page / page_size | int | 分页 |
| q | string? | 搜索关键词 |
| sender | string? | 按发件人 |
| is_read | bool? | 已读/未读 |

**Response `200`:** `{ "total": 500, "page": 1, "page_size": 20, "emails": [...] }`（同 3.1 格式）

### 7.2 `GET /api/admin/emails/search` — 全文搜索

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | ✅ | 搜索词（也搜 body_html 和 envelope_from） |
| page / page_size | int | ❌ | 分页 |

### 7.3 `GET /api/admin/emails/{email_id}` — 详情

**Response:** 同 3.3

### 7.4 `DELETE /api/admin/emails/{email_id}` — 删除

**Response:** `{ "status": "ok", "message": "已删除邮件 #101" }`

### 7.5 `POST /api/admin/emails/batch-delete` — 批量删除

**Request:** `{ "ids": [101, 102, 103] }`

**Response:** `{ "status": "ok", "deleted": [101, 102, 103], "count": 3 }`

---

## 8. 管理 — 统计 `/api/admin/stats` 👑

### 8.1 `GET /api/admin/stats/overview` — 总览

```json
{ "total_users": 150, "active_users": 140, "total_mailboxes": 120, "active_mailboxes": 115, "total_emails": 5000, "unread_emails": 320, "total_applications": 200, "pending_applications": 10, "total_attachments": 800, "today_new_users": 3, "today_new_emails": 45 }
```

### 8.2 `GET /api/admin/stats/users?days=30` — 注册趋势

```json
[{ "date": "2026-05-13", "count": 5 }, { "date": "2026-05-14", "count": 3 }]
```

### 8.3 `GET /api/admin/stats/emails?days=30` — 邮件趋势

格式同 8.2

### 8.4 `GET /api/admin/stats/applications` — 申请状态分布

```json
[{ "status": "pending", "count": 10 }, { "status": "approved", "count": 180 }, { "status": "rejected", "count": 10 }]
```

### 8.5 `GET /api/admin/stats/mailboxes?limit=20` — 邮箱使用量排行

```json
[{ "id": 1, "address": "zhangsan@wic.edu.kg", "email_count": 42, "unread_count": 5 }]
```

### 8.6 `GET /api/admin/stats/storage` — 存储统计

```json
{ "total_size_bytes": 52428800, "total_size_mb": 50.0, "total_attachments": 800, "avg_email_size_bytes": 10485 }
```

---

## 9. 管理 — 日志 `/api/admin/logs` 👑

### 9.1 `GET /api/admin/logs` — 日志列表

| 参数 | 类型 | 说明 |
|------|------|------|
| page / page_size | int | 分页 |
| action | string? | 筛选操作类型 |
| target_type | string? | 筛选目标类型 |
| admin_username | string? | 按操作人搜索 |
| start_date | string? | `YYYY-MM-DD` |
| end_date | string? | `YYYY-MM-DD` |

**Response `200`:**
```json
{ "total": 500, "page": 1, "page_size": 20, "logs": [{ "id": 1, "admin_id": 1, "admin_username": "admin", "action": "approve_application", "target_type": "application", "target_id": 5, "target_name": "zhangsan@wic.edu.kg", "detail": "批准邮箱申请", "ip_address": "192.168.1.1", "created_at": "2026-06-12T10:30:00" }] }
```

### 9.2 `GET /api/admin/logs/export` — 导出 CSV

参数同 9.1，返回 `text/csv` 文件下载，最多 10000 条。

### 9.3 `GET /api/admin/logs/{log_id}` — 日志详情

---

## 10. 管理 — 配置 `/api/admin/config` 👑

### 10.1 `GET /api/admin/config` — 获取配置

```json
[{ "key": "mailbox_domain", "value": "wic.edu.kg", "description": "邮箱域名" }, { "key": "application_enabled", "value": "true", "description": "是否开放申请" }, { "key": "max_mailboxes_per_user", "value": "3", "description": "每人最大邮箱数" }, { "key": "max_attachment_size_mb", "value": "10", "description": "单附件大小限制(MB)" }, { "key": "application_require_profile", "value": "true", "description": "申请前是否需完善资料" }]
```

### 10.2 `PATCH /api/admin/config` — 更新配置

**Request:** `{ "configs": { "application_enabled": "false", "max_mailboxes_per_user": "5" } }`

**Response:** `{ "status": "ok", "updated": ["application_enabled", "max_mailboxes_per_user"] }`

### 10.3 `POST /api/admin/config/test-cloudflare` — 测试 Cloudflare 连通性

**Response:**
```json
{ "status": "ok", "message": "Cloudflare Email Worker 服务可达", "data": {...} }
```

### 10.4 `GET /api/admin/config/domain-check` — DNS 检查

```json
{ "domain": "wic.edu.kg", "checks": { "mx": ["10 mail.wic.edu.kg"], "a": ["1.2.3.4"], "resolved_ip": "1.2.3.4" } }
```

---

## 11. 管理 — 管理员 `/api/admin/admins` 👑

### 11.1 `GET /api/admin/admins` — 管理员列表

```json
[{ "id": 1, "username": "admin", "email": "admin@wic.edu.kg", "real_name": "管理员", "is_active": true, "created_at": "2026-01-01T00:00:00" }]
```

### 11.2 `POST /api/admin/admins` — 添加管理员

**Request:** `{ "username": "zhang_san" }`

**Response `201`:** 同 11.1 单个对象

### 11.3 `DELETE /api/admin/admins/{admin_id}` — 移除管理员权限

**Response:** `{ "status": "ok", "message": "已移除 zhang_san 的管理员权限" }`

### 11.4 `PATCH /api/admin/admins/{admin_id}/role` — 分配角色

**Request:** `{ "is_admin": false }`

**Response:** `{ "status": "ok", "message": "已将 zhang_san 设为普通用户" }`

---

## 接口总表（54 个）

| # | 方法 | 路径 | 认证 |
|---|------|------|------|
| 1 | POST | `/api/auth/register` | 🔓 |
| 2 | POST | `/api/auth/login` | 🔓 |
| 3 | GET | `/api/auth/me` | 🔑 |
| 4 | GET | `/api/auth/profile` | 🔑 |
| 5 | PATCH | `/api/auth/profile` | 🔑 |
| 6 | POST | `/api/auth/change-password` | 🔑 |
| 7 | POST | `/api/mailbox/apply` | 🔑 |
| 8 | GET | `/api/mailbox/applications` | 🔑 |
| 9 | GET | `/api/mailbox` | 🔑 |
| 10 | GET | `/api/emails` | 🔑 |
| 11 | GET | `/api/emails/unread-count` | 🔑 |
| 12 | GET | `/api/emails/{id}` | 🔑 |
| 13 | GET | `/api/emails/attachments/{attachment_id}/download` | 🔑 |
| 14 | PATCH | `/api/emails/{id}/read` | 🔑 |
| 15 | PATCH | `/api/emails/{id}/unread` | 🔑 |
| 16 | GET | `/api/admin/users` | 👑 |
| 17 | GET | `/api/admin/users/{id}` | 👑 |
| 18 | PATCH | `/api/admin/users/{id}` | 👑 |
| 19 | PATCH | `/api/admin/users/{id}/toggle-active` | 👑 |
| 20 | DELETE | `/api/admin/users/{id}` | 👑 |
| 21 | POST | `/api/admin/users/{id}/reset-password` | 👑 |
| 22 | GET | `/api/admin/applications` | 👑 |
| 23 | GET | `/api/admin/applications/{id}` | 👑 |
| 24 | PATCH | `/api/admin/applications/{id}/approve` | 👑 |
| 25 | PATCH | `/api/admin/applications/{id}/reject` | 👑 |
| 26 | POST | `/api/admin/applications/batch-approve` | 👑 |
| 27 | POST | `/api/admin/applications/batch-reject` | 👑 |
| 28 | GET | `/api/admin/mailboxes` | 👑 |
| 29 | GET | `/api/admin/mailboxes/{id}` | 👑 |
| 30 | POST | `/api/admin/mailboxes` | 👑 |
| 31 | PATCH | `/api/admin/mailboxes/{id}/toggle-active` | 👑 |
| 32 | DELETE | `/api/admin/mailboxes/{id}` | 👑 |
| 33 | GET | `/api/admin/emails` | 👑 |
| 34 | GET | `/api/admin/emails/search` | 👑 |
| 35 | GET | `/api/admin/emails/{id}` | 👑 |
| 36 | DELETE | `/api/admin/emails/{id}` | 👑 |
| 37 | POST | `/api/admin/emails/batch-delete` | 👑 |
| 38 | GET | `/api/admin/stats/overview` | 👑 |
| 39 | GET | `/api/admin/stats/users` | 👑 |
| 40 | GET | `/api/admin/stats/emails` | 👑 |
| 41 | GET | `/api/admin/stats/applications` | 👑 |
| 42 | GET | `/api/admin/stats/mailboxes` | 👑 |
| 43 | GET | `/api/admin/stats/storage` | 👑 |
| 44 | GET | `/api/admin/logs` | 👑 |
| 45 | GET | `/api/admin/logs/export` | 👑 |
| 46 | GET | `/api/admin/logs/{id}` | 👑 |
| 47 | GET | `/api/admin/config` | 👑 |
| 48 | PATCH | `/api/admin/config` | 👑 |
| 49 | POST | `/api/admin/config/test-cloudflare` | 👑 |
| 50 | GET | `/api/admin/config/domain-check` | 👑 |
| 51 | GET | `/api/admin/admins` | 👑 |
| 52 | POST | `/api/admin/admins` | 👑 |
| 53 | DELETE | `/api/admin/admins/{id}` | 👑 |
| 54 | PATCH | `/api/admin/admins/{id}/role` | 👑 |
