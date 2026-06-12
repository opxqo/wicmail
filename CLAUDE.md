# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WicMail is a campus email application and management platform (校园邮箱申请与管理平台) for students to apply for `@wic.edu.kg` email addresses, with admin review workflows. The domain is `wic.edu.kg`.

All code comments, commit messages, and documentation are in **Chinese (中文)**.

## Repository Structure

Three independent modules (no monorepo tooling):

- **backend-mail/**: FastAPI service (port 8000) — receives and parses emails from Cloudflare Email Worker
- **backend-wic/**: FastAPI service (port 8001) — user registration, mailbox applications, admin approval, email viewing
- **frontend/**: Vue 3 SPA (dev port 3200) — main application interface

Both backends share a single MySQL database (`wicmail`) with identical table definitions.

## Commands

### Backend (both backend-mail and backend-wic)

```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000  # backend-mail
uvicorn app.main:app --reload --port 8001  # backend-wic

# Run tests
pytest tests/ -v
```

### Frontend

```bash
# Install dependencies
npm install

# Start development server (port 3200)
npm run dev

# Build for production
npm run build

# Lint and fix
npm run lint:fix
```

## Architecture

### Data Flow

External senders → Cloudflare Email Routing → backend-mail (POST /api/inbound/cloudflare) → MySQL
Frontend → backend-wic (REST API) → MySQL

### Database Schema (5 shared tables)

- **users**: student accounts with profile fields (student_id, department, major, etc.)
- **mailboxes**: email addresses (prefix@wic.edu.kg)
- **email_messages**: stored emails with parsed content
- **attachments**: email attachment metadata
- **mailbox_applications**: user applications for mailboxes (status: pending/approved/rejected)

### Key Design Decisions

- **Shared database**: Both backends connect to the same MySQL instance; table-level isolation only
- **Auto-created admin**: backend-mail creates `admin/admin123456` on first startup — change in production
- **JWT secrets should match** between backends (currently may differ)
- **Mailbox auto-creation race**: backend-mail's `get_or_create_mailbox` can race with backend-wic's approval flow
- **Frontend mock mode**: Supports development without backends via Apifox cloud mock or local mock data

## Tech Stack Details

### Backend

- FastAPI + SQLAlchemy (async with asyncmy)
- Alembic for migrations
- JWT authentication (PyJWT + bcrypt)
- Python 3.11 in Docker (dev on 3.9+)

### Frontend

- Vue 3.5 + Vite 8 (JavaScript, not TypeScript)
- **Naive UI** component library (not Element Plus)
- UnoCSS for atomic CSS
- Pinia 3 with persisted state
- Vue Router 5 (hash mode in dev)
- ESLint with @antfu/eslint-config
- Pre-commit hooks via simple-git-hooks + lint-staged

The frontend is based on the [vue-naive-admin](https://github.com/zclzone/vue-naive-admin) template.

## Environment Variables

Copy `.env.example` to `.env` in each module:

- **backend-mail**: DATABASE_URL, JWT_SECRET_KEY, CLOUDFLARE_EMAIL_SECRET_KEY, SMTP settings
- **backend-wic**: DATABASE_URL, JWT_SECRET_KEY, MAILBOX_DOMAIN (wic.edu.kg)
- **frontend**: VITE_PROXY_TARGET (backend-wic URL), VITE_USE_MOCK, VITE_USE_HASH

## Deployment

- Both backends have Dockerfiles and Procfiles for Zeabur deployment
- No CI/CD pipelines configured
- Target: MySQL at your-database-host, services on Zeabur
