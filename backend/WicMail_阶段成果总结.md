# WicMail 后端 — 阶段成果总结

## 项目概述

WicMail 是一个**私人收件系统**，核心链路为：

```
发件人 → Cloudflare Email Routing → Email Worker → FastAPI → MySQL
```

目前已完成**第一阶段（MVP）**和**第二阶段（数据库接入）**的全部工作。

---

## 已完成的工作

### 一、Cloudflare Email Worker（项目启动前已完成）

- 已编写 Email Worker 代码，负责接收邮件并 POST JSON 到 FastAPI
- 已在 Cloudflare Dashboard 配置 Email Routing 规则
- 域名：`wic.edu.kg`
- 已通过 Webhook.site 调试成功，链路跑通
- 获取了 4 封真实邮件作为测试数据

### 二、FastAPI 后端 MVP（第一阶段）

| 功能 | 状态 |
|---|---|
| `POST /api/inbound/cloudflare` 接收接口 | ✅ |
| `X-Secret-Key` 密钥校验 | ✅ |
| base64 解码 raw 邮件 | ✅ |
| `email.message_from_bytes()` 解析邮件 | ✅ |
| 提取 subject、from、to、text、html、attachments | ✅ |
| GBK/UTF-8 等多编码兼容 | ✅ |
| `raw_too_large` 场景不崩溃 | ✅ |
| `GET /health` 健康检查 | ✅ |

### 三、MySQL 数据库接入（第二阶段）

| 功能 | 状态 |
|---|---|
| SQLAlchemy 2.x async 异步引擎 | ✅ |
| Alembic 迁移脚本 + 自动建表 | ✅ |
| 三张表：`mailboxes`、`email_messages`、`attachments` | ✅ |
| 邮件入库逻辑 | ✅ |
| `message_id` / `raw_sha256` 去重 | ✅ |
| `GET /api/emails` 分页邮件列表 | ✅ |
| `GET /api/emails/{id}` 邮件详情 + 自动标记已读 | ✅ |
| 解析失败也保存元数据 | ✅ |

### 四、测试

| 测试项 | 数量 | 状态 |
|---|---|---|
| 密钥校验 | 2 | ✅ |
| 邮件解析（text/html/subject/base64） | 4 | ✅ |
| raw_too_large 容错 | 1 | ✅ |
| 返回格式（request_id/email_id） | 2 | ✅ |
| 去重 | 1 | ✅ |
| 邮件列表 + 分页 | 2 | ✅ |
| 邮件详情 + 已读标记 | 2 | ✅ |
| 404 处理 | 1 | ✅ |
| **合计** | **15** | **全部通过** |

---

## 当前 API 接口

| 方法 | 路径 | 功能 |
|---|---|---|
| `POST` | `/api/inbound/cloudflare` | 接收 Worker 邮件 → 解析 → 入库 |
| `GET` | `/api/emails?page=1&page_size=20` | 分页查询邮件列表 |
| `GET` | `/api/emails/{email_id}` | 查看邮件详情（自动标记已读） |
| `GET` | `/health` | 健康检查 |

---

## 项目文件结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI 入口 + lifespan
│   ├── config.py                # pydantic-settings 配置
│   ├── database.py              # 异步引擎 + Session
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── inbound.py           # POST 入站接口
│   │   └── emails.py            # GET 查询接口
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── inbound.py           # Worker payload + 解析结果模型
│   │   └── email.py             # 邮件列表/详情响应模型
│   ├── services/
│   │   ├── __init__.py
│   │   ├── mail_parser.py       # 邮件解析服务
│   │   └── email_storage.py     # 入库服务
│   └── models/
│       ├── __init__.py
│       └── email.py             # SQLAlchemy 模型（3 张表）
├── alembic/                     # 数据库迁移
│   ├── env.py
│   └── versions/
│       └── f396171c47b5_initial.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest 配置（NullPool 引擎）
│   ├── test_inbound.py          # 15 个测试用例
│   └── fixtures/
│       ├── cloudflare_payload_sample.json   # 简化测试 payload
│       ├── real_gmail_test.json             # 真实 Gmail 邮件
│       ├── real_163mail_gbk.json            # 真实 163 邮箱（GBK）
│       ├── real_xai_confirmation_1.json     # 真实 xAI 验证码邮件
│       └── real_xai_confirmation_2.json     # 真实 xAI 验证码邮件
├── requirements.txt
├── alembic.ini
├── README.md
├── .env
├── .env.example
├── .gitignore
├── email_service.py             # SMTP 发件服务（独立工具）
└── test_db.py                   # 数据库连接测试（独立工具）
```

---

## 数据库表结构

### mailboxes

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INT PK | 主键 |
| address | VARCHAR(255) UNIQUE | 邮箱地址 |
| display_name | VARCHAR(255) | 显示名 |
| is_active | BOOLEAN | 是否启用 |
| created_at / updated_at | DATETIME | 时间戳 |

### email_messages

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INT PK | 主键 |
| mailbox_id | INT FK | 关联 mailbox |
| request_id | VARCHAR(255) | Worker request_id |
| message_id | VARCHAR(512) UNIQUE | 邮件 Message-ID |
| raw_sha256 | VARCHAR(64) UNIQUE | 去重 hash |
| envelope_from / envelope_to | VARCHAR(255) | 信封地址 |
| header_from / to / cc / reply_to | VARCHAR(512) | 头信息 |
| subject | VARCHAR(1000) | 主题 |
| sent_at / received_at | DATETIME | 时间 |
| raw_size / raw_too_large | INT / BOOLEAN | 原始大小 |
| headers_json | JSON | 完整 headers |
| body_text / body_html | TEXT | 正文 |
| parse_status | VARCHAR(20) | received / parsed / failed |
| is_read | BOOLEAN | 是否已读 |
| created_at / updated_at | DATETIME | 时间戳 |

### attachments

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INT PK | 主键 |
| email_id | INT FK | 关联 email_messages |
| filename | VARCHAR(500) | 文件名 |
| content_type | VARCHAR(255) | MIME 类型 |
| size | INT | 字节大小 |
| created_at | DATETIME | 时间戳 |

---

## 依赖

```
fastapi              # Web 框架
uvicorn              # ASGI 服务器
pydantic             # 数据校验
pydantic-settings    # 环境变量管理
python-dotenv        # .env 文件
sqlalchemy[asyncio]  # ORM（异步）
asyncmy              # MySQL 异步驱动
pymysql              # MySQL 同步驱动（Alembic 迁移用）
alembic              # 数据库迁移
pytest / httpx       # 测试
cryptography         # SSL 支持
```

---

## 已入库的真实邮件

| ID | 来源 | 主题 | 编码 |
|---|---|---|---|
| 1 | bilalbetesman@gmail.com | asdadad | UTF-8 |
| 2 | 18727430326@163.com | 好嘟嘟嘟嘟 | GBK |
| 3 | noreply@x.ai | 5WL-T3H xAI confirmation code | UTF-8 |

---

## 本地运行

```bash
# 安装依赖
pip3 install -r requirements.txt

# 运行测试（15 个用例）
pytest tests/ -v

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 数据库迁移
alembic upgrade head
```

---

## 待做事项（后续阶段）

| 阶段 | 内容 | 优先级 |
|---|---|---|
| 前端 | Web 管理界面，邮件查看页面 | 高 |
| 部署 | 正式部署到服务器，配置域名和 HTTPS | 高 |
| Worker 对接 | 将 Worker 的 `FASTAPI_URL` 指向正式后端 | 高 |
| 密钥轮换 | 生成正式 `SECRET_KEY`，同步更新 Worker 和 FastAPI | 高 |
| 附件下载 | 附件文件落盘 + 下载接口 | 中 |
| 发件系统 | SMTP 发件（已有 email_service.py 基础） | 中 |
| 用户认证 | 登录后台 + JWT 鉴权 | 中 |
| 邮件搜索 | 按主题、发件人、时间等条件搜索 | 低 |
