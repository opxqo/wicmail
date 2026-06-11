# AGENTS.md

WicMail 校园邮箱平台 — 三模块独立项目，无 monorepo 工具。

## 语言

所有代码注释、提交信息、文档使用 **中文**。

## 模块结构

| 模块 | 技术 | 端口 | 职责 |
|---|---|---|---|
| `backend-mail/` | FastAPI + SQLAlchemy (asyncmy) | 8000 | 接收 Cloudflare 转发的邮件 |
| `backend-wic/` | FastAPI + SQLAlchemy (asyncmy) | 8001 | 用户注册/邮箱申请/管理审核 |
| `frontend/` | Vue 3 + Vite + Naive UI + UnoCSS | 3200 | Web 前端 |

两个后端**共享同一个 MySQL 数据库** (`wicmail`)，表结构相同。

## 常用命令

### 后端 (backend-mail / backend-wic)

```bash
cd backend-mail  # 或 backend-wic
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000  # mail, wic 用 8001
pytest tests/ -v
```

### 前端

```bash
cd frontend
npm install
npm run dev        # 端口 3200
npm run build
npm run lint:fix
```

## 关键注意事项

- **测试需要真实 MySQL**：conftest.py 直连数据库，无 SQLite 回退
- **Alembic 迁移**：env.py 将 `asyncmy` 替换为 `pymysql` 做同步迁移
- **backend-mail 启动自动建表+创建 admin**：`admin/admin123456`，生产需改
- **JWT Secret 需一致**：两个后端的 `.env` 中 `JWT_SECRET_KEY` 必须相同
- **前端 Mock 模式**：`VITE_USE_MOCK=true` 可脱离后端开发
- **前端代理**：vite.config.js 将 `/api` 代理到 `VITE_PROXY_TARGET`
- **Pre-commit**：前端通过 simple-git-hooks + lint-staged 自动 eslint --fix
- **邮箱域名**：`wic.edu.kg`，格式 `{prefix}@wic.edu.kg`

## 数据库表 (5 张)

- `users` — 用户账号
- `mailboxes` — 邮箱地址
- `email_messages` — 邮件内容
- `attachments` — 附件元数据
- `mailbox_applications` — 邮箱申请 (仅 backend-wic 定义)

## 已知风险

- backend-mail 的 `get_or_create_mailbox` 可能与 backend-wic 的审批流程产生竞态
- 两个后端 JWT Secret 默认不同，需手动统一

## 详细参考

架构详情、API 端点列表见 `CLAUDE.md` 和 `wicmail_architecture_analysis.md`。
