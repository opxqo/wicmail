<template>
  <div ref="pageRef" class="landing-page">
    <!-- 导航栏 - CC Switch 风格 -->
    <header class="site-nav" :class="{ 'site-nav-solid': isScrolled }">
      <div class="nav-inner">
        <!-- Logo -->
        <router-link to="/" class="nav-logo" aria-label="WicMail 首页">
          <img src="/wic-emblem.svg" alt="WicMail" class="nav-logo-img">
          <span class="nav-logo-text">WicMail</span>
        </router-link>

        <!-- 居中导航（桌面端） -->
        <nav class="nav-links" aria-label="首页导航">
          <a
            v-for="item in navItems"
            :key="item.target"
            :href="`#${item.target}`"
            class="nav-link"
            @click.prevent="scrollToSection(item.target)"
          >
            {{ item.label }}
          </a>
        </nav>

        <!-- 右侧操作（桌面端） -->
        <div class="nav-right">
          <a class="nav-icon-btn" href="https://www.wic.edu.kg" target="_blank" rel="noopener noreferrer" aria-label="学校官网">
            <i class="i-fe:globe text-18" />
          </a>
          <a class="nav-icon-btn" href="https://github.com/opxqo" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
            <i class="i-fe:github text-18" />
          </a>
          <router-link class="nav-cta-btn" to="/login">
            <i class="i-fe:user text-14" />
            登录工作台
          </router-link>
        </div>

        <!-- 移动端菜单按钮 -->
        <button class="mobile-menu-btn" :class="{ 'mobile-menu-active': mobileOpen }" @click="mobileOpen = !mobileOpen">
          <i :class="mobileOpen ? 'i-fe:x' : 'i-fe:menu'" class="text-20" />
        </button>
      </div>

      <!-- 移动端下拉菜单 -->
      <div class="mobile-dropdown" :class="{ 'mobile-dropdown-open': mobileOpen }">
        <a
          v-for="item in navItems"
          :key="item.target"
          :href="`#${item.target}`"
          class="mobile-link"
          @click.prevent="scrollToSection(item.target); mobileOpen = false"
        >
          {{ item.label }}
        </a>
        <router-link class="mobile-cta" to="/login" @click="mobileOpen = false">
          <i class="i-fe:user text-16" />
          登录工作台
        </router-link>
      </div>
    </header>

    <main>
      <!-- Hero - CC Switch 风格：左文字右产品截图 -->
      <section id="hero" class="hero-section">
        <!-- 背景层 -->
        <div class="hero-bg-layer" />
        <div class="hero-gradient" />
        <div class="hero-grid-pattern" />

        <div class="hero-container">
          <div class="hero-grid">
            <!-- 左侧文字 -->
            <div class="hero-text">
              <!-- 徽章 -->
              <div class="hero-badge">
                <span>💡 学生自建公益非盈利平台</span>
              </div>

              <!-- Logo + 标题 -->
              <div class="hero-title-row">
                <img src="/wic-emblem.svg" alt="WicMail" class="hero-emblem">
                <h1 class="hero-title">
                  WicMail
                </h1>
              </div>

              <h2 class="hero-tagline">
                搭建起校园学术与沟通的免费桥梁
              </h2>

              <p class="hero-description">
                本平台为学生自建的公益非盈利项目，非学校官方建设。由于武汉城市学院已不再为学生分配校园个人教育邮箱，我们自发搭建了 WicMail。基于 Cloudflare 邮件代理解析与高效流转架构，为您提供免费的专属学术邮箱后缀申请与安全的收发信管理。
              </p>

              <!-- 核心优势特色列表 -->
              <ul class="hero-features">
                <li>
                  <i class="i-fe:check-circle" />
                  <span><strong>专属学术邮箱</strong>：公益免费提供 @wic.edu.kg 后缀邮箱申请</span>
                </li>
                <li>
                  <i class="i-fe:shield" />
                  <span><strong>自治材料审核</strong>：学生志愿者在线审核，全流程安全防滥用审计</span>
                </li>
                <li>
                  <i class="i-fe:zap" />
                  <span><strong>高效稳定流转</strong>：依托 Cloudflare 与阿里云解析，保障信件稳定接收转发</span>
                </li>
              </ul>

              <!-- CTA 按钮 -->
              <div class="hero-cta">
                <router-link to="/login" class="hero-btn-primary">
                  <i class="i-fe:mail text-16" />
                  申请校园邮箱
                </router-link>
                <router-link to="/login" class="hero-btn-secondary">
                  进入工作台
                  <i class="i-fe:arrow-right text-14" />
                </router-link>
              </div>
              <p class="hero-platform">
                学生自发维护 · 纯属公益非盈利 · 供学术交流与求职认证使用
              </p>
            </div>

            <!-- 右侧：1:1 复刻真实工作台 -->
            <div class="hero-demo">
              <div class="demo-glow" />
              <div v-if="!demoIsClosed" class="demo-window" :class="{ 'demo-dark-theme': demoDarkMode, 'demo-window-fullscreen': demoIsFullscreen }" @mousedown="stopAutoplay">
                <!-- macOS 标题栏 -->
                <div class="demo-titlebar">
                  <div class="demo-dots">
                    <span class="dot dot-red" title="关闭演示" @click="closeDemoWindow">
                      <svg viewBox="0 0 10 10" class="dot-svg-icon"><path d="M1.5 1.5l7 7M8.5 1.5l-7 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" /></svg>
                    </span>
                    <span class="dot dot-yellow" title="最小化" @click="triggerToast('warning', '该窗口不支持最小化')">
                      <svg viewBox="0 0 10 10" class="dot-svg-icon"><path d="M1 5h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" /></svg>
                    </span>
                    <span class="dot dot-green" title="全屏模式 (按 ESC 退出)" @click="toggleFullscreen">
                      <svg viewBox="0 0 10 10" class="dot-svg-icon"><path d="M1.5 1.5h4M1.5 1.5v4M8.5 8.5H4.5M8.5 8.5V4.5M1.5 1.5l7 7" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                  <span class="demo-titlebar-text">WicMail - 校园邮箱工作台</span>
                </div>
                <!-- 应用布局：侧边栏 + 内容 -->
                <div class="demo-body">
                  <!-- 侧边栏 -->
                  <div class="demo-sidebar" :class="{ 'demo-sidebar-collapsed': demoCollapsed }">
                    <div class="demo-sidebar-logo">
                      <img src="/wic-emblem.svg" alt="WicMail" class="demo-sidebar-logo-img">
                      <span v-if="!demoCollapsed" class="demo-sidebar-logo-text">WicMail</span>
                    </div>
                    <div class="demo-sidebar-nav">
                      <!-- 工作台 -->
                      <div
                        class="demo-nav-item tour-nav-dashboard"
                        :class="{ 'demo-nav-active': demoActiveNav === 'dashboard' }"
                        @click="openTab('dashboard', '工作台')"
                      >
                        <i class="demo-nav-icon i-fe:home" />
                        <span v-if="!demoCollapsed">工作台</span>
                      </div>

                      <!-- 邮箱管理 -->
                      <div class="demo-nav-group">
                        <div
                          class="demo-nav-item"
                          @click="handleGroupClick('mailbox')"
                        >
                          <i class="demo-nav-icon i-fe:mail" />
                          <span v-if="!demoCollapsed">邮箱管理</span>
                          <i v-if="!demoCollapsed" :class="demoSubmenuExpanded.mailbox ? 'i-fe:chevron-down' : 'i-fe:chevron-right'" class="demo-nav-arrow" />
                        </div>
                        <div v-show="demoSubmenuExpanded.mailbox && !demoCollapsed" class="demo-nav-sub">
                          <div
                            class="demo-nav-sub-item tour-nav-apply"
                            :class="{ 'demo-nav-sub-active': demoActiveNav === 'apply' }"
                            @click="openTab('apply', '申请邮箱')"
                          >
                            <i class="demo-nav-icon i-fe:plus-circle" />
                            <span>申请邮箱</span>
                          </div>
                          <div
                            class="demo-nav-sub-item tour-nav-my-mailboxes"
                            :class="{ 'demo-nav-sub-active': demoActiveNav === 'my-mailboxes' }"
                            @click="openTab('my-mailboxes', '我的邮箱')"
                          >
                            <i class="demo-nav-icon i-fe:inbox" />
                            <span>我的邮箱</span>
                          </div>
                        </div>
                      </div>

                      <!-- 邮件中心 -->
                      <div
                        class="demo-nav-item tour-nav-emails"
                        :class="{ 'demo-nav-active': demoActiveNav === 'emails' }"
                        @click="openTab('emails', '邮件中心')"
                      >
                        <i class="demo-nav-icon i-fe:inbox" />
                        <span v-if="!demoCollapsed">邮件中心</span>
                        <span v-if="demoUnreadEmailCount && !demoCollapsed" class="demo-menu-badge">
                          {{ demoUnreadEmailCount }}
                        </span>
                      </div>

                      <!-- 管理后台 -->
                      <div class="demo-nav-group">
                        <div
                          class="demo-nav-item"
                          @click="handleGroupClick('admin')"
                        >
                          <i class="demo-nav-icon i-fe:settings" />
                          <span v-if="!demoCollapsed">管理后台</span>
                          <i v-if="!demoCollapsed" :class="demoSubmenuExpanded.admin ? 'i-fe:chevron-down' : 'i-fe:chevron-right'" class="demo-nav-arrow" />
                        </div>
                        <div v-show="demoSubmenuExpanded.admin && !demoCollapsed" class="demo-nav-sub">
                          <div
                            class="demo-nav-sub-item tour-nav-admin-apps"
                            :class="{ 'demo-nav-sub-active': demoActiveNav === 'admin-apps' }"
                            @click="openTab('admin-apps', '申请审核')"
                          >
                            <i class="demo-nav-icon i-fe:check-square" />
                            <span>申请审核</span>
                            <span v-if="demoPendingAppCount && !demoCollapsed" class="demo-menu-badge-alert">
                              {{ demoPendingAppCount }}
                            </span>
                          </div>
                          <div
                            class="demo-nav-sub-item"
                            :class="{ 'demo-nav-sub-active': demoActiveNav === 'admin-users' }"
                            @click="openTab('admin-users', '用户管理')"
                          >
                            <i class="demo-nav-icon i-fe:users" />
                            <span>用户管理</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 右侧主区域：头部 + 页面内容 -->
                  <div class="demo-main">
                    <!-- 顶部 Header -->
                    <div class="demo-header">
                      <div class="demo-header-left">
                        <i class="demo-collapse-btn i-fe:menu" @click="demoCollapsed = !demoCollapsed" />
                        <span class="demo-header-divider" />
                        <div class="demo-tabs">
                          <div
                            v-for="tab in demoTabs"
                            :key="tab.key"
                            class="demo-tab-item"
                            :class="{ 'demo-tab-active': demoActiveTab === tab.key }"
                            @click="openTab(tab.key, tab.title)"
                          >
                            <span class="demo-tab-title">{{ tab.title }}</span>
                            <i
                              v-if="tab.closable"
                              class="demo-tab-close i-fe:x"
                              @click.stop="closeTab(tab.key)"
                            />
                          </div>
                        </div>
                      </div>
                      <div class="demo-header-right">
                        <i class="demo-tool-icon i-fe:help-circle" title="新手引导" @click="triggerToast('info', '点击右侧「开启演示」体验自动流程')" />
                        <i :class="demoDarkMode ? 'i-fe:sun' : 'i-fe:moon'" class="demo-tool-icon" title="切换主题" @click="demoDarkMode = !demoDarkMode" />
                        <i :class="demoIsFullscreen ? 'i-fe:minimize' : 'i-fe:maximize'" class="demo-tool-icon" title="全屏模式" @click="toggleFullscreen" />
                        <a href="https://github.com/lucas-luo/wicmail" target="_blank" class="demo-tool-link" title="GitHub 仓库">
                          <i class="demo-tool-icon i-fe:github" />
                        </a>
                        <i class="demo-tool-icon i-fe:settings" title="主题配置" @click="triggerToast('info', '主题配置为演示环境预设')" />

                        <span class="demo-header-divider" style="margin: 0 8px; height: 14px;" />

                        <div class="demo-user-trigger" @click="demoUserDropdownOpen = !demoUserDropdownOpen">
                          <div class="demo-header-avatar">
                            张
                          </div>
                          <span class="demo-header-username">zhangsan</span>
                          <i class="i-fe:chevron-down text-10" />
                          <div v-show="demoUserDropdownOpen" class="demo-user-dropdown-menu">
                            <div class="demo-dropdown-user-info">
                              <span class="demo-dropdown-username">zhangsan</span>
                              <span class="demo-dropdown-role">[普通用户]</span>
                            </div>
                            <div class="demo-dropdown-divider" />
                            <div class="demo-dropdown-item" @click.stop="openTab('profile', '个人资料'); demoUserDropdownOpen = false">
                              <i class="i-fe:user mr-4 text-12" /> 个人资料
                            </div>
                            <div class="demo-dropdown-item" @click.stop="demoUserDropdownOpen = false">
                              <i class="i-fe:log-out mr-4 text-12" /> 退出登录
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- 主内容区 -->
                    <div class="demo-content">
                      <transition name="fade-slide" mode="out-in">
                        <div :key="demoActiveNav" style="display: flex; flex-direction: column; flex: 1; min-height: 0; gap: 12px;">
                          <!-- ===== 工作台 ===== -->
                          <template v-if="demoActiveNav === 'dashboard'">
                            <!-- 顶部双卡片 -->
                            <div class="demo-top-row">
                              <div class="demo-card demo-card-user">
                                <div class="demo-user-row">
                                  <div class="demo-avatar">
                                    张
                                  </div>
                                  <div class="demo-user-info">
                                    <span class="demo-user-name">你好，zhangsan</span>
                                    <span class="demo-user-role">普通用户</span>
                                  </div>
                                </div>
                                <p class="demo-user-desc">
                                  WicMail 校园邮箱，让沟通更简单。
                                </p>
                              </div>
                              <div class="demo-card demo-card-overview">
                                <div class="demo-card-header">
                                  <i class="demo-card-header-icon i-fe:layout" />
                                  工作台概览
                                </div>
                                <p class="demo-card-text">
                                  在这里管理你的校园邮箱、查看邮件和处理申请。
                                </p>
                                <div class="demo-card-actions">
                                  <span class="demo-btn demo-btn-ghost" @click="demoActiveNav = 'apply'">申请新邮箱</span>
                                  <span class="demo-btn demo-btn-primary" @click="demoActiveNav = 'emails'">查看邮件</span>
                                </div>
                              </div>
                            </div>
                            <!-- 统计卡片 (n-statistic 风格) -->
                            <div class="demo-stat-row">
                              <div v-for="stat in demoStats" :key="stat.label" class="demo-stat-card">
                                <div class="demo-stat-label">
                                  {{ stat.label }}
                                </div>
                                <div class="demo-stat-value-container">
                                  <i :class="stat.icon" class="demo-stat-prefix-icon" />
                                  <span class="demo-stat-value">{{ stat.value }}</span>
                                </div>
                              </div>
                            </div>
                            <!-- 底部双栏：邮件表格 + 我的邮箱 -->
                            <div class="demo-bottom-row">
                              <div class="demo-card demo-card-emails">
                                <div class="demo-card-header">
                                  <i class="demo-card-header-icon i-fe:inbox" />
                                  最近邮件
                                </div>
                                <table class="demo-table">
                                  <thead>
                                    <tr>
                                      <th>发件人</th>
                                      <th>主题</th>
                                      <th>状态</th>
                                      <th>时间</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    <tr
                                      v-for="email in demoEmails.slice(0, 4)"
                                      :key="email.id"
                                      class="demo-table-row"
                                      @click="openEmailDetail(email)"
                                    >
                                      <td class="demo-td-from">
                                        {{ email.from }}
                                      </td>
                                      <td class="demo-td-subject">
                                        {{ email.subject }}
                                      </td>
                                      <td>
                                        <span class="demo-tag" :class="email.isRead ? 'demo-tag-default' : 'demo-tag-info'">
                                          {{ email.isRead ? '已读' : '未读' }}
                                        </span>
                                      </td>
                                      <td class="demo-td-time">
                                        {{ email.fullTime?.slice(0, 16) }}
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </div>
                              <div class="demo-card demo-card-mailbox">
                                <div class="demo-card-header">
                                  <i class="demo-card-header-icon i-fe:mail" />
                                  我的邮箱
                                </div>
                                <div class="demo-mailbox-list">
                                  <div v-for="mb in demoMailboxes" :key="mb.address" class="demo-mailbox-item">
                                    <div class="demo-mailbox-info">
                                      <span class="demo-mailbox-addr">{{ mb.address }}</span>
                                      <span class="demo-mailbox-name">{{ mb.display_name }}</span>
                                    </div>
                                    <span class="demo-tag demo-tag-success">活跃</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </template>

                          <!-- ===== 申请邮箱 ===== -->
                          <template v-if="demoActiveNav === 'apply'">
                            <div class="demo-page-header">
                              <i class="demo-page-icon i-fe:plus-circle" />
                              申请新邮箱
                            </div>

                            <!-- 申请提示 Alert -->
                            <div class="demo-alert demo-alert-info mb-12">
                              <i class="demo-alert-icon i-fe:info" />
                              <div class="demo-alert-content">
                                <span class="demo-alert-title">邮箱申请规范</span>
                                <span class="demo-alert-desc">前缀由 3-30 位字母、数字、点或下划线组成。请上传学生证/校园卡扫描件作为身份证明材料。</span>
                              </div>
                            </div>

                            <div class="demo-form-card">
                              <div class="demo-form-row">
                                <label>邮箱前缀</label>
                                <div class="demo-input-group">
                                  <input v-model="demoApplyForm.prefix" class="demo-input tour-input-prefix" placeholder="输入前缀，如 zhangsan">
                                  <span class="demo-input-addon">@wic.edu.kg</span>
                                </div>
                              </div>
                              <div class="demo-form-row">
                                <label>显示名称</label>
                                <input v-model="demoApplyForm.display_name" class="demo-input" placeholder="可选，如：张三的邮箱">
                              </div>
                              <div class="demo-form-row">
                                <label>申请理由</label>
                                <textarea v-model="demoApplyForm.reason" class="demo-textarea" placeholder="可选，说明申请原因" />
                              </div>
                              <div class="demo-form-row">
                                <label>证明材料</label>
                                <div class="demo-upload-container">
                                  <div class="demo-upload-zone tour-upload-zone-img" @click="simulateUpload('img')">
                                    <i class="demo-upload-icon i-fe:upload-cloud" />
                                    <span>点击模拟上传证明图片 (JPG/PNG)</span>
                                    <span class="demo-upload-hint">已选 {{ demoApplyUploads.filter(u => u.type.startsWith('image/')).length }} / 5 张</span>
                                  </div>
                                  <div class="demo-upload-zone" @click="simulateUpload('pdf')">
                                    <i class="demo-upload-icon i-fe:paperclip" />
                                    <span>点击模拟上传补充材料 (PDF)</span>
                                    <span class="demo-upload-hint">已选 {{ demoApplyUploads.filter(u => u.type.includes('pdf')).length }} / 3 张</span>
                                  </div>
                                </div>
                              </div>
                              <!-- 文件预览 (n-upload 图片预览网格) -->
                              <div v-if="demoApplyUploads.length" class="demo-form-row">
                                <label>已选材料</label>
                                <div class="demo-upload-file-list-grid">
                                  <div v-for="(file, idx) in demoApplyUploads" :key="idx" class="demo-upload-file-card">
                                    <div v-if="file.type.startsWith('image/')" class="demo-upload-thumbnail-container">
                                      <img :src="file.url || '/wic-emblem.svg'" class="demo-upload-thumbnail" @click="openAttachmentPreview(file)">
                                      <div class="demo-upload-thumbnail-hover">
                                        <i class="i-fe:eye mr-8 cursor-pointer text-14" @click="openAttachmentPreview(file)" />
                                        <i class="i-fe:trash-2 cursor-pointer text-14" @click="removeUpload(idx)" />
                                      </div>
                                    </div>
                                    <div v-else class="demo-upload-file-container">
                                      <i class="i-fe:file-text mb-4 text-24 text-emerald-500" />
                                      <span class="demo-upload-filename" :title="file.name" @click="openAttachmentPreview(file)">{{ file.name }}</span>
                                      <div class="demo-upload-file-actions">
                                        <i class="i-fe:eye mr-6 cursor-pointer text-12" @click="openAttachmentPreview(file)" />
                                        <i class="i-fe:trash-2 cursor-pointer text-12 text-red-500" @click="removeUpload(idx)" />
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                              <div class="demo-form-row">
                                <label />
                                <div class="demo-action-buttons">
                                  <span class="demo-btn demo-btn-primary tour-btn-submit" @click="handleApplySubmit">
                                    <i class="i-fe:send mr-4 text-12" /> 提交申请
                                  </span>
                                  <span class="demo-btn demo-btn-ghost" @click="handleApplyReset">重置</span>
                                </div>
                              </div>
                            </div>

                            <!-- 我的申请记录 -->
                            <div class="demo-card mt-12">
                              <div class="demo-card-header">
                                <i class="demo-card-header-icon i-fe:clipboard" />
                                我的申请记录
                              </div>
                              <table class="demo-table">
                                <thead>
                                  <tr>
                                    <th>申请地址</th>
                                    <th>显示名称</th>
                                    <th>状态</th>
                                    <th>材料</th>
                                    <th>申请时间</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr v-for="app in demoApplications.filter(a => a.user === 'zhangsan')" :key="app.id">
                                    <td>{{ app.email }}</td>
                                    <td>{{ app.display_name || '-' }}</td>
                                    <td>
                                      <span
                                        class="demo-tag" :class="{
                                          'demo-tag-warning': app.status === 'pending',
                                          'demo-tag-success': app.status === 'approved',
                                          'demo-tag-error': app.status === 'rejected',
                                        }"
                                      >{{ app.statusText }}</span>
                                    </td>
                                    <td>
                                      <span v-if="app.attachments?.length" class="demo-attachment-count">
                                        <i class="i-fe:paperclip text-12" /> {{ app.attachments.length }} 份材料
                                      </span>
                                      <span v-else class="opacity-40">-</span>
                                    </td>
                                    <td>{{ app.created_at?.slice(0, 16) }}</td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                          </template>

                          <!-- ===== 我的邮箱 ===== -->
                          <template v-if="demoActiveNav === 'my-mailboxes'">
                            <div class="demo-page-header">
                              <i class="demo-page-icon i-fe:mail" />
                              我的邮箱
                            </div>
                            <div class="demo-mailbox-grid">
                              <div v-for="mb in demoMailboxes" :key="mb.id" class="demo-mailbox-card-full">
                                <div class="demo-mb-card-header">
                                  <div class="demo-mb-avatar">
                                    <i class="i-fe:mail text-16" />
                                  </div>
                                  <div class="demo-mb-details">
                                    <div class="demo-mb-addr">
                                      {{ mb.address }}
                                    </div>
                                    <div class="demo-mb-name">
                                      {{ mb.display_name || '未设置显示名称' }}
                                    </div>
                                  </div>
                                </div>
                                <div class="demo-mb-card-actions-row">
                                  <span class="demo-mb-action-btn" @click="openEmailsAndFilter(mb.address)">
                                    <i class="i-fe:mail mr-2 text-10" /> 查看邮件
                                  </span>
                                  <span class="demo-mb-action-btn" @click="copyToClipboard(mb.address)">
                                    <i class="i-fe:copy mr-2 text-10" /> 复制地址
                                  </span>
                                </div>
                                <div class="demo-mb-card-footer">
                                  <span class="demo-tag demo-tag-success">活跃</span>
                                  <span class="demo-mb-date">{{ mb.created_at?.slice(0, 10) }}</span>
                                </div>
                              </div>
                              <div v-if="!demoMailboxes.length" class="demo-mailbox-empty">
                                暂无活跃邮箱
                              </div>
                            </div>
                          </template>

                          <!-- ===== 邮件中心 ===== -->
                          <template v-if="demoActiveNav === 'emails'">
                            <div class="demo-page-header">
                              <i class="demo-page-icon i-fe:inbox" />
                              邮件中心
                              <span v-if="demoEmailFilterAddress" class="demo-tag demo-tag-info ml-8 inline-flex cursor-pointer items-center gap-4" title="清除过滤" style="font-size: 11px; padding: 2px 6px;" @click="demoEmailFilterAddress = ''">
                                过滤: {{ demoEmailFilterAddress }} <i class="i-fe:x text-10" />
                              </span>
                            </div>
                            <div class="demo-card">
                              <table class="demo-table demo-table-full">
                                <thead>
                                  <tr>
                                    <th>状态</th>
                                    <th>发件人</th>
                                    <th>主题</th>
                                    <th>收件箱</th>
                                    <th>附件</th>
                                    <th>时间</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr
                                    v-for="(email, idx) in filteredDemoEmails"
                                    :key="email.id"
                                    class="demo-table-row"
                                    :class="{ 'tour-email-row-first': idx === 0 }"
                                    @click="openEmailDetail(email)"
                                  >
                                    <td>
                                      <span class="demo-tag" :class="email.isRead ? 'demo-tag-default' : 'demo-tag-info'">
                                        {{ email.isRead ? '已读' : '未读' }}
                                      </span>
                                    </td>
                                    <td class="demo-td-from">
                                      {{ email.from }}
                                    </td>
                                    <td class="demo-td-subject">
                                      {{ email.subject }}
                                    </td>
                                    <td>{{ email.to }}</td>
                                    <td>
                                      <i v-if="email.attachment_count" class="i-fe:paperclip text-12" />
                                      <span v-else class="opacity-30">-</span>
                                    </td>
                                    <td class="demo-td-time">
                                      {{ email.fullTime?.slice(0, 16) }}
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                          </template>

                          <!-- ===== 申请审核 ===== -->
                          <template v-if="demoActiveNav === 'admin-apps'">
                            <div class="demo-page-header">
                              <i class="demo-page-icon i-fe:check-square" />
                              申请审核
                              <!-- 筛选栏 -->
                              <select v-model="demoAdminFilter" class="demo-admin-filter">
                                <option value="all">
                                  全部状态
                                </option>
                                <option value="pending">
                                  待审核
                                </option>
                                <option value="approved">
                                  已批准
                                </option>
                                <option value="rejected">
                                  已拒绝
                                </option>
                              </select>
                            </div>
                            <div class="demo-card">
                              <table class="demo-table demo-table-full">
                                <thead>
                                  <tr>
                                    <th>ID</th>
                                    <th>申请人</th>
                                    <th>申请地址</th>
                                    <th>状态</th>
                                    <th>材料</th>
                                    <th>申请时间</th>
                                    <th>操作</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr v-for="app in filteredApplications" :key="app.id">
                                    <td>{{ app.id }}</td>
                                    <td>{{ app.user }}</td>
                                    <td>{{ app.email }}</td>
                                    <td>
                                      <span
                                        class="demo-tag" :class="{
                                          'demo-tag-warning': app.status === 'pending',
                                          'demo-tag-success': app.status === 'approved',
                                          'demo-tag-error': app.status === 'rejected',
                                        }"
                                      >{{ app.statusText }}</span>
                                    </td>
                                    <td>
                                      <span v-if="app.attachments?.length" class="demo-attachment-count">
                                        <i class="i-fe:paperclip text-12" /> {{ app.attachments.length }} 份
                                      </span>
                                      <span v-else class="opacity-40">-</span>
                                    </td>
                                    <td>{{ app.created_at?.slice(0, 16) }}</td>
                                    <td>
                                      <div v-if="app.status === 'pending'" class="demo-action-group">
                                        <span class="demo-action-btn demo-action-approve tour-btn-approve" @click="openReview(app, 'approve')">批准</span>
                                        <span class="demo-action-btn demo-action-reject" @click="openReview(app, 'reject')">拒绝</span>
                                      </div>
                                      <span v-else class="demo-action-disabled">已处理</span>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                          </template>

                          <!-- ===== 用户管理 ===== -->
                          <template v-if="demoActiveNav === 'admin-users'">
                            <div class="demo-page-header">
                              <i class="demo-page-icon i-fe:users" />
                              用户管理
                            </div>
                            <div class="demo-card">
                              <table class="demo-table demo-table-full">
                                <thead>
                                  <tr>
                                    <th>ID</th>
                                    <th>用户名</th>
                                    <th>邮箱</th>
                                    <th>角色</th>
                                    <th>状态</th>
                                    <th>操作</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr v-for="user in demoUsers" :key="user.id">
                                    <td>{{ user.id }}</td>
                                    <td>{{ user.username }}</td>
                                    <td>{{ user.email || '-' }}</td>
                                    <td>
                                      <span class="demo-tag" :class="user.is_admin ? 'demo-tag-warning' : 'demo-tag-default'">
                                        {{ user.is_admin ? '管理员' : '用户' }}
                                      </span>
                                    </td>
                                    <td>
                                      <span class="demo-tag" :class="user.is_active ? 'demo-tag-success' : 'demo-tag-error'">
                                        {{ user.is_active ? '正常' : '已禁用' }}
                                      </span>
                                    </td>
                                    <td>
                                      <span class="demo-btn demo-btn-ghost px-6 py-2 text-11" :class="user.is_active ? 'color-red-500!' : 'color-green-500!'" @click="toggleUserActive(user)">
                                        {{ user.is_active ? '禁用' : '启用' }}
                                      </span>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                          </template>

                          <!-- ===== 个人资料 ===== -->
                          <template v-if="demoActiveNav === 'profile'">
                            <div class="demo-page-header">
                              <i class="demo-page-icon i-fe:user" />
                              个人资料中心
                            </div>

                            <!-- 概览卡片 -->
                            <div class="demo-profile-header-card demo-card mb-12">
                              <div class="demo-profile-avatar-section">
                                <div class="demo-profile-avatar">
                                  张
                                </div>
                                <div class="demo-profile-user-details">
                                  <div class="demo-profile-name-row">
                                    <span class="demo-profile-name">张三</span>
                                    <span class="demo-tag demo-tag-info ml-8" style="padding: 1px 6px; font-size: 11px;">普通用户</span>
                                  </div>
                                  <div class="demo-profile-subtext">
                                    学号：20240901001 | 邮箱：zhangsan@wic.edu.kg
                                  </div>
                                </div>
                              </div>
                              <div class="demo-profile-progress-section">
                                <div class="demo-profile-progress-label">
                                  <span>资料完善度</span>
                                  <span>85%</span>
                                </div>
                                <div class="demo-profile-progress-bar">
                                  <div class="demo-profile-progress-fill" style="width: 85%" />
                                </div>
                              </div>
                            </div>

                            <!-- 缺失字段警告 -->
                            <div class="demo-alert demo-alert-warning mb-12">
                              <i class="demo-alert-icon i-fe:alert-triangle" />
                              <div class="demo-alert-content">
                                <span class="demo-alert-title">信息待补全</span>
                                <span class="demo-alert-desc">您的密保问题与手机号尚未绑定，这可能会影响您的账号安全，请尽快补全。</span>
                              </div>
                            </div>

                            <div class="demo-profile-grid">
                              <!-- 左侧：基础信息 -->
                              <div class="demo-card demo-profile-card">
                                <div class="demo-card-header" style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--demo-border); padding-bottom: 10px; margin-bottom: 12px;">
                                  <div style="display: flex; align-items: center; gap: 8px;">
                                    <i class="demo-card-header-icon i-fe:info" />
                                    基本账号信息
                                  </div>
                                  <span class="demo-btn demo-btn-ghost demo-btn-xs" style="padding: 2px 8px; font-size: 11px;" @click="triggerToast('info', '当前已经是最新资料')">修改资料</span>
                                </div>
                                <table class="demo-descriptions-table">
                                  <tbody>
                                    <tr>
                                      <td class="demo-desc-label">
                                        用户名
                                      </td>
                                      <td class="demo-desc-value">
                                        zhangsan
                                      </td>
                                    </tr>
                                    <tr>
                                      <td class="demo-desc-label">
                                        真实姓名
                                      </td>
                                      <td class="demo-desc-value">
                                        张三
                                      </td>
                                    </tr>
                                    <tr>
                                      <td class="demo-desc-label">
                                        所属院系
                                      </td>
                                      <td class="demo-desc-value">
                                        计算机科学与技术系
                                      </td>
                                    </tr>
                                    <tr>
                                      <td class="demo-desc-label">
                                        学号 / 工号
                                      </td>
                                      <td class="demo-desc-value">
                                        20240901001
                                      </td>
                                    </tr>
                                    <tr>
                                      <td class="demo-desc-label">
                                        账号状态
                                      </td>
                                      <td class="demo-desc-value">
                                        <span class="demo-tag demo-tag-success">正常使用</span>
                                      </td>
                                    </tr>
                                    <tr>
                                      <td class="demo-desc-label">
                                        安全级别
                                      </td>
                                      <td class="demo-desc-value">
                                        <span class="demo-tag demo-tag-info">中级</span>
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </div>
                              <!-- 右侧：安全密码修改 -->
                              <div class="demo-form-card demo-profile-form">
                                <div class="demo-card-header" style="border-bottom: 1px solid var(--demo-border); padding-bottom: 10px; margin-bottom: 12px;">
                                  <i class="demo-card-header-icon i-fe:lock" />
                                  安全密码修改
                                </div>
                                <div class="demo-form-row">
                                  <label>旧密码</label>
                                  <input v-model="demoProfileForm.oldPassword" type="password" class="demo-input" placeholder="请输入当前密码">
                                </div>
                                <div class="demo-form-row">
                                  <label>新密码</label>
                                  <input v-model="demoProfileForm.newPassword" type="password" class="demo-input" placeholder="请输入新密码 (不少于6位)">
                                </div>
                                <div class="demo-form-row">
                                  <label>确认密码</label>
                                  <input v-model="demoProfileForm.confirmPassword" type="password" class="demo-input" placeholder="请再次输入新密码">
                                </div>
                                <div class="demo-form-row">
                                  <label />
                                  <div class="demo-action-buttons">
                                    <span class="demo-btn demo-btn-primary" @click="handleProfileSave">
                                      <i class="i-fe:check-circle mr-4 text-12" /> 保存修改
                                    </span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </template>
                        </div>
                      </transition>
                    </div>

                    <!-- Slide-out Email Drawer -->
                    <div v-show="demoDrawerOpen" class="demo-drawer-overlay" @click="demoDrawerOpen = false" />
                    <div class="demo-drawer" :class="{ 'demo-drawer-open': demoDrawerOpen }">
                      <div v-if="demoSelectedEmail" class="demo-drawer-container">
                        <div class="demo-drawer-header">
                          <div class="demo-drawer-title-row">
                            <span class="demo-drawer-title">{{ demoSelectedEmail.subject }}</span>
                            <i class="demo-drawer-close i-fe:x" @click="demoDrawerOpen = false" />
                          </div>
                          <div class="demo-drawer-meta">
                            <div><strong>发件人：</strong>{{ demoSelectedEmail.from }}</div>
                            <div><strong>收件人：</strong>{{ demoSelectedEmail.to }}</div>
                            <div><strong>时间：</strong>{{ demoSelectedEmail.fullTime }}</div>
                          </div>
                        </div>
                        <div class="demo-drawer-body">
                          <div class="demo-email-body-html" v-html="formatEmailBody(demoSelectedEmail.body)" />
                        </div>
                        <div v-if="demoSelectedEmail.attachments?.length" class="demo-drawer-attachments">
                          <div class="demo-drawer-section-title">
                            <i class="i-fe:paperclip mr-4 text-12" /> 附件 ({{ demoSelectedEmail.attachments.length }}，点击预览)
                          </div>
                          <div class="demo-drawer-file-list">
                            <div
                              v-for="(att, i) in demoSelectedEmail.attachments"
                              :key="i"
                              class="demo-drawer-file-item demo-drawer-file-item-clickable"
                              @click="openAttachmentPreview({ name: att.filename, type: 'application/pdf' })"
                            >
                              <i class="i-fe:file-text mr-4 text-14 text-emerald-500" />
                              <span class="demo-drawer-file-name">{{ att.filename }}</span>
                              <i class="i-fe:eye ml-auto text-11 opacity-60" />
                            </div>
                          </div>
                        </div>
                        <div class="demo-drawer-footer">
                          <span class="demo-btn demo-btn-ghost" @click="toggleEmailReadState(demoSelectedEmail)">
                            {{ demoSelectedEmail.isRead ? '标记未读' : '标记已读' }}
                          </span>
                        </div>
                      </div>
                    </div>

                    <!-- Modal Dialog for Admin Review -->
                    <div v-if="demoDialogOpen" class="demo-dialog-overlay" @click="demoDialogOpen = false" />
                    <div v-if="demoDialogOpen" class="demo-dialog-card">
                      <div class="demo-dialog-header">
                        <span class="demo-dialog-title">
                          {{ demoReviewAction === 'approve' ? '批准邮箱申请' : '拒绝邮箱申请' }}
                        </span>
                        <i class="demo-dialog-close i-fe:x" @click="demoDialogOpen = false" />
                      </div>
                      <div v-if="demoSelectedApp" class="demo-dialog-body">
                        <div class="demo-dialog-info-row">
                          <strong>申请账号：</strong>{{ demoSelectedApp.email }}
                        </div>
                        <div class="demo-dialog-info-row">
                          <strong>申请理由：</strong>{{ demoSelectedApp.reason || '无' }}
                        </div>
                        <!-- 证明材料预览 -->
                        <div v-if="demoSelectedApp.attachments?.length" class="demo-dialog-attachments-section">
                          <div class="demo-dialog-section-title">
                            证明材料 (点击预览)
                          </div>
                          <div class="demo-dialog-attachments-grid">
                            <div v-for="(file, idx) in demoSelectedApp.attachments" :key="idx" class="demo-dialog-attachment-card demo-dialog-attachment-clickable" @click="openAttachmentPreview(file)">
                              <i :class="file.type.startsWith('image/') ? 'i-fe:image' : 'i-fe:file-text'" class="text-24 text-emerald-500 opacity-60" />
                              <span class="demo-dialog-file-name" :title="file.name">{{ file.name }}</span>
                              <i class="i-fe:eye mt-4 text-10 opacity-50" />
                            </div>
                          </div>
                        </div>
                        <div class="demo-dialog-comment-row">
                          <label>审核备注</label>
                          <textarea v-model="demoReviewComment" class="demo-textarea" placeholder="填写审核意见（可选）" />
                        </div>
                      </div>
                      <div class="demo-dialog-footer">
                        <span class="demo-btn demo-btn-ghost mr-8" @click="demoDialogOpen = false">取消</span>
                        <span
                          class="demo-btn tour-btn-confirm"
                          :class="demoReviewAction === 'approve' ? 'demo-btn-success' : 'demo-btn-error'"
                          @click="handleReviewConfirm"
                        >
                          {{ demoReviewAction === 'approve' ? '批准' : '拒绝' }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Toast Message (Naive UI n-message style) -->
                <transition name="demo-toast-fade">
                  <div v-if="demoToast.show" class="demo-toast-container">
                    <div class="demo-toast" :class="`demo-toast-${demoToast.type}`">
                      <i :class="getToastIcon(demoToast.type)" class="demo-toast-icon" />
                      <span class="demo-toast-msg">{{ demoToast.msg }}</span>
                    </div>
                  </div>
                </transition>

                <!-- Image/Attachment Preview Dialog -->
                <div v-if="demoAttachmentPreviewVisible" class="demo-preview-overlay" @click="demoAttachmentPreviewVisible = false" />
                <div v-if="demoAttachmentPreviewVisible" class="demo-preview-card">
                  <div class="demo-preview-header">
                    <span class="demo-preview-title">{{ demoAttachmentPreviewName }}</span>
                    <i class="demo-preview-close i-fe:x" @click="demoAttachmentPreviewVisible = false" />
                  </div>
                  <div class="demo-preview-body">
                    <img v-if="demoAttachmentPreviewUrl && demoAttachmentPreviewUrl !== ''" :src="demoAttachmentPreviewUrl" class="demo-preview-img" alt="Preview">
                    <div v-else class="demo-preview-file-placeholder">
                      <i class="i-fe:file-text text-48 opacity-40" />
                      <p class="mt-8">
                        该文件格式不支持直接预览
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Automated Tour Cursor -->
                <div
                  v-if="tourActive && !demoIsClosed"
                  class="demo-simulated-cursor"
                  :class="{ 'cursor-clicked': cursorClicked }"
                  :style="{ left: `${cursorX}%`, top: `${cursorY}%` }"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" class="cursor-pointer-svg">
                    <title>pointer-filled</title>
                    <path fill="currentColor" d="M3.039 4.277L6.943 17.84c.185.837.92 1.516 1.831 1.642l.17.016a2.2 2.2 0 0 0 1.982-1.006l.045-.078l1.4-2.072l4.05 4.05a2.067 2.067 0 0 0 2.924 0l1.047-1.047c.388-.388.606-.913.606-1.461l-.008-.182a2.07 2.07 0 0 0-.598-1.28l-4.047-4.048l2.103-1.412c.726-.385 1.18-1.278 1.053-2.189A2.2 2.2 0 0 0 17.8 6.928L4.276 3.038a1 1 0 0 0-1.236 1.24z" />
                  </svg>
                  <div class="cursor-click-ripple" />

                  <!-- Step description bubble -->
                  <div v-if="tourStep >= 0 && tourStep < tourStepDescriptions.length" class="demo-cursor-tooltip">
                    {{ tourStepDescriptions[tourStep] }}
                  </div>
                </div>

                <!-- Bottom step progress indicator -->
                <div v-if="tourActive && !demoIsClosed" class="demo-tour-progress-bar">
                  <div class="demo-tour-progress-fill" :style="{ width: `${(tourStep + 1) / 11 * 100}%` }" />
                </div>
              </div>

              <!-- Closed State Placeholder -->
              <div v-else class="demo-closed-placeholder">
                <div class="demo-closed-icon">
                  <i class="i-fe:terminal text-42" />
                </div>
                <h3>WicMail 演示工作台已关闭</h3>
                <p>您可以重新加载以体验高防真的 Naive UI 邮箱管理与审批中心。</p>
                <button class="demo-btn demo-btn-primary" @click="reopenDemoWindow">
                  <i class="i-fe:play mr-6" /> 开启在线演示
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="intro" class="intro-section">
        <div class="section-container intro-grid">
          <div class="intro-copy">
            <p class="section-kicker">
              PROJECT ORIGIN
            </p>
            <h2>解决校园邮箱停发之痛，做纯粹的公益服务</h2>
            <p>
              WicMail 诞生于校内学生的自发努力。由于学校不再主动为同学们分配教育邮箱，我们在学术研究、折扣认证以及与校外导师沟通时面临诸多不便。为此，我们搭建了这套免费系统，围绕身份材料、模拟申请与管理收发组织功能，首页提供规则说明，所有管理均在用户工作台自治完成。
            </p>
            <div class="intro-actions">
              <router-link to="/login" class="text-link">
                开始申请 <i class="i-fe:chevron-right text-15" />
              </router-link>
              <a href="#faq" class="text-link muted" @click.prevent="scrollToSection('faq')">
                查看常见问题
              </a>
            </div>
          </div>

          <div class="promise-panel">
            <div v-for="item in promises" :key="item.title" class="promise-item">
              <div class="promise-icon">
                <i :class="item.icon" class="text-22" />
              </div>
              <div>
                <h3>{{ item.title }}</h3>
                <p>{{ item.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="process" class="process-section">
        <div class="section-container">
          <div class="section-header">
            <p class="section-kicker">
              APPLICATION FLOW
            </p>
            <h2>四步完成邮箱申请</h2>
            <p>流程保持轻量，但每一步都围绕真实身份与可审核材料设计。</p>
          </div>

          <div class="process-grid">
            <article v-for="(item, index) in processSteps" :key="item.title" class="process-card">
              <div class="step-index">
                {{ String(index + 1).padStart(2, '0') }}
              </div>
              <i :class="item.icon" class="process-icon text-28" />
              <h3>{{ item.title }}</h3>
              <p>{{ item.desc }}</p>
            </article>
          </div>
        </div>
      </section>

      <section id="features" class="feature-section">
        <div class="section-container feature-layout">
          <div class="feature-lead">
            <p class="section-kicker">
              CAPABILITIES
            </p>
            <h2>为校园邮箱而不是泛用邮箱系统设计</h2>
            <p>
              WicMail 的首页只展示确定能力：申请入口、审核链路、邮件中心、权限区分和移动端适配。后续真实数据与公告可以接入接口后再展示。
            </p>
          </div>

          <div class="feature-grid">
            <article v-for="item in capabilityCards" :key="item.title" class="feature-card">
              <i :class="item.icon" class="text-26" />
              <h3>{{ item.title }}</h3>
              <p>{{ item.desc }}</p>
            </article>
          </div>
        </div>
      </section>

      <section id="scenarios" class="scenario-section">
        <div class="section-container">
          <div class="section-header">
            <p class="section-kicker">
              USE CASES
            </p>
            <h2>适合这些校园沟通场景</h2>
          </div>

          <div class="scenario-grid">
            <article v-for="item in scenarios" :key="item.title" class="scenario-card">
              <span>{{ item.tag }}</span>
              <h3>{{ item.title }}</h3>
              <p>{{ item.desc }}</p>
            </article>
          </div>
        </div>
      </section>

      <section id="faq" class="faq-section">
        <div class="section-container faq-layout">
          <div>
            <p class="section-kicker">
              FAQ
            </p>
            <h2>申请前可以先了解这些</h2>
            <p class="faq-lead">
              首页只做说明和入口，具体审核状态、邮箱列表和邮件内容请登录工作台查看。
            </p>
          </div>

          <div class="faq-list">
            <details v-for="item in faqs" :key="item.question" class="faq-item">
              <summary>{{ item.question }}</summary>
              <p>{{ item.answer }}</p>
            </details>
          </div>
        </div>
      </section>

      <section class="cta-section">
        <div class="section-container cta-panel">
          <div>
            <p class="section-kicker light">
              READY
            </p>
            <h2>准备好开通你的校园邮箱了吗？</h2>
            <p>登录工作台后提交资料与邮箱申请，审核通过后即可使用校园邮箱相关服务。</p>
          </div>
          <router-link to="/login" class="btn btn-primary cta-btn">
            前往工作台
            <i class="i-fe:arrow-right text-16" />
          </router-link>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <div class="footer-inner">
        <!-- 4列网格 -->
        <div class="footer-grid">
          <!-- 列1: 品牌 -->
          <div class="footer-brand">
            <router-link to="/" class="footer-logo-link">
              <img src="/wic-emblem.svg" alt="武汉城市学院校徽" class="footer-emblem">
              <div class="footer-brand-text">
                <span class="footer-brand-name">WicMail</span>
                <span class="footer-brand-sub">校园邮箱服务</span>
              </div>
            </router-link>
            <p class="footer-desc">
              本站是由武汉城市学院学生自建、运行的完全公益非盈利服务（非官方建设）。旨在为校内师生有学术交流、求职及认证需求时提供免费的专属教育邮箱申请与管理通道。
            </p>
            <div class="footer-socials">
              <a href="https://github.com/opxqo" target="_blank" rel="noopener noreferrer" class="footer-social-btn" aria-label="GitHub">
                <i class="i-fe:github text-16" />
              </a>
              <a href="https://www.wic.edu.kg" target="_blank" rel="noopener noreferrer" class="footer-social-btn" aria-label="学校官网">
                <i class="i-fe:globe text-16" />
              </a>
              <a href="mailto:admin@wic.edu.kg" class="footer-social-btn" aria-label="邮件联系">
                <i class="i-fe:mail text-16" />
              </a>
            </div>
          </div>

          <!-- 列2: 快捷入口 -->
          <div class="footer-col">
            <button class="footer-col-toggle" @click="footerOpen[0] = !footerOpen[0]">
              <h3>快捷入口</h3>
              <i class="footer-chevron i-fe:chevron-down text-16" :class="{ 'footer-chevron-open': footerOpen[0] }" />
            </button>
            <div class="footer-col-body" :class="{ 'footer-col-open': footerOpen[0] }">
              <router-link to="/login" class="footer-link">
                <i class="footer-link-icon i-fe:log-in text-14" /> 登录工作台
              </router-link>
              <router-link to="/login" class="footer-link">
                <i class="footer-link-icon i-fe:plus-circle text-14" /> 申请邮箱
              </router-link>
              <router-link to="/login" class="footer-link">
                <i class="footer-link-icon i-fe:inbox text-14" /> 邮件中心
              </router-link>
              <a href="https://www.wic.edu.kg" target="_blank" rel="noopener noreferrer" class="footer-link">
                <i class="footer-link-icon i-fe:external-link text-14" /> 学校官网
                <i class="footer-ext-icon i-fe:external-link text-10" />
              </a>
            </div>
          </div>

          <!-- 列3: 页面导航 -->
          <div class="footer-col">
            <button class="footer-col-toggle" @click="footerOpen[1] = !footerOpen[1]">
              <h3>页面导航</h3>
              <i class="footer-chevron i-fe:chevron-down text-16" :class="{ 'footer-chevron-open': footerOpen[1] }" />
            </button>
            <div class="footer-col-body" :class="{ 'footer-col-open': footerOpen[1] }">
              <a href="#intro" class="footer-link" @click.prevent="scrollToSection('intro')">
                <i class="footer-link-icon i-fe:info text-14" /> 服务介绍
              </a>
              <a href="#process" class="footer-link" @click.prevent="scrollToSection('process')">
                <i class="footer-link-icon i-fe:list text-14" /> 申请流程
              </a>
              <a href="#features" class="footer-link" @click.prevent="scrollToSection('features')">
                <i class="footer-link-icon i-fe:shield text-14" /> 核心能力
              </a>
              <a href="#faq" class="footer-link" @click.prevent="scrollToSection('faq')">
                <i class="footer-link-icon i-fe:help-circle text-14" /> 常见问题
              </a>
            </div>
          </div>

          <!-- 列4: 联系我们 -->
          <div class="footer-col">
            <button class="footer-col-toggle" @click="footerOpen[2] = !footerOpen[2]">
              <h3>联系我们</h3>
              <i class="footer-chevron i-fe:chevron-down text-16" :class="{ 'footer-chevron-open': footerOpen[2] }" />
            </button>
            <div class="footer-col-body" :class="{ 'footer-col-open': footerOpen[2] }">
              <div class="footer-contact-item">
                <i class="footer-contact-icon i-fe:map-pin text-18" />
                <span>湖北省武汉市洪山区黄家湖大学城</span>
              </div>
              <div class="footer-contact-item">
                <i class="footer-contact-icon i-fe:phone text-18" />
                <span>027-86490575</span>
              </div>
              <div class="footer-contact-item">
                <i class="footer-contact-icon i-fe:mail text-18" />
                <a href="mailto:admin@wic.edu.kg" class="footer-contact-link">admin@wic.edu.kg</a>
              </div>
            </div>
          </div>
        </div>
        <div class="footer-bottom">
          <div class="footer-bottom-inner">
            <p class="footer-copy">
              © {{ currentYear }} WicMail · Wuhan City University. All rights reserved.
            </p>
            <img src="/校训.svg" alt="励志修德 勤学创新" class="footer-motto">
            <div class="footer-credit">
              <span>Designed & Built by</span>
              <strong>OPXQO LT</strong>
              <i class="i-fe:heart fill-current text-10 text-red-400" />
            </div>
          </div>
          <p class="footer-legal">
            WicMail 是武汉城市学院学生自发建设的非官方、完全公益性服务平台。本站与学校官方无行政隶属关系，仅供校内师生在学术、沟通及认证场景下免费学习与使用。
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, reactive, ref } from 'vue'

const pageRef = ref(null)
const scrollY = ref(0)
const isScrolled = computed(() => scrollY.value > 24)
const mobileOpen = ref(false)
const footerOpen = reactive([false, false, false])
const currentYear = new Date().getFullYear()

const navItems = [
  { label: '服务介绍', target: 'intro' },
  { label: '申请流程', target: 'process' },
  { label: '核心能力', target: 'features' },
  { label: '常见问题', target: 'faq' },
]

const promises = [
  { title: '校园身份专属', desc: '围绕 @wic.edu.kg 邮箱申请和身份资料建立入口。', icon: 'i-fe:home' },
  { title: '流程清晰', desc: '注册、资料、申请、审核状态集中在工作台处理。', icon: 'i-fe:list' },
  { title: '审核可控', desc: '管理员审核申请材料，降低邮箱滥用和误开通风险。', icon: 'i-fe:shield' },
]

const processSteps = [
  { title: '登录或注册账号', desc: '进入工作台，使用平台账号开始邮箱申请流程。', icon: 'i-fe:user-plus' },
  { title: '完善身份资料', desc: '补充姓名、院系、专业等用于审核的基础信息。', icon: 'i-fe:edit-3' },
  { title: '提交邮箱申请', desc: '填写期望邮箱前缀，并根据要求提交辅助材料。', icon: 'i-fe:send' },
  { title: '审核通过后使用', desc: '通过后可在工作台查看邮箱信息和邮件内容。', icon: 'i-fe:check-circle' },
]

const capabilityCards = [
  { title: '邮箱申请', desc: '把邮箱前缀申请、资料补充和审核状态放到同一个入口。', icon: 'i-fe:plus-circle' },
  { title: '邮件中心', desc: '为后续邮件查看、收件记录和消息管理预留清晰的信息层级。', icon: 'i-fe:inbox' },
  { title: '权限分区', desc: '普通用户和管理员功能分开，保留审核、用户管理等后台入口。', icon: 'i-fe:lock' },
  { title: '多端适配', desc: '首页和工作台入口在手机、平板、桌面端都保持可读可点击。', icon: 'i-fe:smartphone' },
]

const scenarios = [
  { tag: '学术交流', title: '课程与项目沟通', desc: '使用校园邮箱作为课程通知、项目协作和校内沟通的稳定身份标识。' },
  { tag: '身份认证', title: '校园服务注册', desc: '在需要校园邮箱的服务中使用统一邮箱地址，减少个人邮箱混用。' },
  { tag: '通知归档', title: '重要邮件留存', desc: '把学校相关邮件集中到校园邮箱，便于后续查询和管理。' },
]

const faqs = [
  { question: '本站是武汉城市学院官方网站吗？', answer: '不是。本站是因学校停发学生个人教育邮箱，由学生志愿者自发搭建、维护的完全公益、非盈利性服务平台。所申请的邮箱后缀仅用于学术研究与沟通使用。' },
  { question: '首页可以直接收发邮件吗？', answer: '首页只提供介绍和入口。邮箱申请、邮件查看和管理功能需要进入登录后的工作台。' },
  { question: '申请需要付费吗？审核时间多久？', answer: '完全免费。平台不收取任何费用，由学生管理员利用课余时间在线审批，一般在提交申请后的 24 小时内完成审核。' },
  { question: '忘记账号或遇到使用问题怎么办？', answer: '可以通过页脚中公布的管理员邮箱联系，或在工作台的帮助反馈中心提交工单。' },
]

// ===== 右侧工作台模拟数据 =====
const demoCollapsed = ref(false)
const demoDarkMode = ref(false)
const demoActiveNav = ref('dashboard')
const demoSubmenuExpanded = reactive({
  mailbox: true,
  admin: true,
})
const demoIsClosed = ref(false)
const tourActive = ref(true)
const tourStep = ref(-1)
const tourStepDescriptions = [
  '正在访问工作台',
  '正在打开申请邮箱页面',
  '正在输入邮箱前缀',
  '正在上传证明材料',
  '正在提交邮箱申请',
  '进入管理后台审批申请',
  '正在审查李四的邮箱申请',
  '批准该申请并开通邮箱',
  '查看我的已开通邮箱',
  '正在访问邮件中心',
  '正在阅读系统欢迎邮件',
]
const cursorX = ref(50)
const cursorY = ref(50)
const cursorClicked = ref(false)
let tourTimer = null

function stopAutoplay() {
  if (tourActive.value) {
    tourActive.value = false
    if (tourTimer) {
      clearTimeout(tourTimer)
      tourTimer = null
    }
    triggerToast('info', '您已接管演示，自动播放已停止')
  }
}

function closeDemoWindow() {
  demoIsClosed.value = true
  if (tourTimer) {
    clearTimeout(tourTimer)
    tourTimer = null
  }
  tourActive.value = false
  triggerToast('info', '已关闭演示窗口。您可以点击下方的按钮重新开启。')
}

function reopenDemoWindow() {
  demoIsClosed.value = false
  triggerToast('success', '已重新加载演示工作台')
  // Re-start autoplay on reload
  startTour()
}

function simulateClick() {
  cursorClicked.value = true
  setTimeout(() => {
    cursorClicked.value = false
  }, 400)
}

function alignCursorTo(selector, fallbackX, fallbackY) {
  nextTick(() => {
    const container = document.querySelector('.demo-window')
    const target = document.querySelector(selector)
    if (container && target) {
      const containerRect = container.getBoundingClientRect()
      const targetRect = target.getBoundingClientRect()
      // Calculate center of target relative to container
      const x = ((targetRect.left + targetRect.width / 2) - containerRect.left) / containerRect.width * 100
      const y = ((targetRect.top + targetRect.height / 2) - containerRect.top) / containerRect.height * 100
      cursorX.value = Number(x.toFixed(1))
      cursorY.value = Number(y.toFixed(1))
    }
    else {
      cursorX.value = fallbackX
      cursorY.value = fallbackY
    }
  })
}

function runTourStep() {
  if (!tourActive.value || demoIsClosed.value)
    return

  tourStep.value = (tourStep.value + 1) % 11

  switch (tourStep.value) {
    case 0: // Reset: Move to Dashboard menu tab
      alignCursorTo('.tour-nav-dashboard', 12, 16)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        openTab('dashboard', '工作台')
      }, 1000)
      break

    case 1: // Go to Apply Mailbox
      alignCursorTo('.tour-nav-apply', 14, 26)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        openTab('apply', '申请邮箱')
      }, 1000)
      break

    case 2: // Move to prefix input and simulate typing "autodemo"
      alignCursorTo('.tour-input-prefix', 48, 35)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        demoApplyForm.prefix = 'auto'
        setTimeout(() => {
          if (tourActive.value)
            demoApplyForm.prefix = 'autodemo'
        }, 300)
      }, 1000)
      break

    case 3: // Click upload zone
      alignCursorTo('.tour-upload-zone-img', 48, 60)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        simulateUpload('img')
      }, 1000)
      break

    case 4: // Click Submit
      alignCursorTo('.tour-btn-submit', 42, 87)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        handleApplySubmit()
      }, 1000)
      break

    case 5: // Go to Admin Review
      alignCursorTo('.tour-nav-admin-apps', 14, 48)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        openTab('admin-apps', '申请审核')
      }, 1000)
      break

    case 6: // Click Approve on the top pending row
      alignCursorTo('.tour-btn-approve', 92, 28)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        const pendingApp = demoApplications.find(a => a.status === 'pending')
        if (pendingApp) {
          openReview(pendingApp, 'approve')
        }
      }, 1000)
      break

    case 7: // Confirm in approval dialog
      alignCursorTo('.tour-btn-confirm', 61, 67)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        handleReviewConfirm()
      }, 1000)
      break

    case 8: // Go to My Mailboxes
      alignCursorTo('.tour-nav-my-mailboxes', 14, 32)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        openTab('my-mailboxes', '我的邮箱')
      }, 1000)
      break

    case 9: // Go to Email Center
      alignCursorTo('.tour-nav-emails', 12, 38)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        openTab('emails', '邮件中心')
      }, 1000)
      break

    case 10: // Click first email row
      alignCursorTo('.tour-email-row-first', 53, 27)
      setTimeout(() => {
        if (!tourActive.value)
          return
        simulateClick()
        if (demoEmails.length > 0) {
          openEmailDetail(demoEmails[0])
        }
      }, 1000)
      break
  }
}

function runTourNextStep() {
  if (!tourActive.value || demoIsClosed.value)
    return
  runTourStep()

  // Determine delay based on current step
  let delay = 3800
  if (tourStep.value === 4 || tourStep.value === 7) {
    delay = 5500
  }

  tourTimer = setTimeout(runTourNextStep, delay)
}

function startTour() {
  if (tourTimer)
    clearTimeout(tourTimer)
  tourActive.value = true
  tourStep.value = -1
  // Run first step after 3.8 seconds
  tourTimer = setTimeout(runTourNextStep, 3800)
}

function handleGroupClick(group) {
  if (demoCollapsed.value) {
    demoCollapsed.value = false
  }
  demoSubmenuExpanded[group] = !demoSubmenuExpanded[group]
}

function copyToClipboard(text) {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => {
      triggerToast('success', '已成功复制邮箱地址到剪切板！')
    }).catch(() => {
      fallbackCopy(text)
    })
  }
  else {
    fallbackCopy(text)
  }
}

function fallbackCopy(text) {
  try {
    const input = document.createElement('input')
    input.value = text
    input.style.position = 'fixed'
    input.style.opacity = '0'
    document.body.appendChild(input)
    input.select()
    document.execCommand('copy')
    document.body.removeChild(input)
    triggerToast('success', '已成功复制邮箱地址到剪切板！')
  }
  catch (err) {
    triggerToast('error', '复制失败，请手动选择复制。')
  }
}

function getToastIcon(type) {
  switch (type) {
    case 'success': return 'i-fe:check-circle'
    case 'error': return 'i-fe:alert-circle'
    case 'warning': return 'i-fe:alert-triangle'
    case 'info': return 'i-fe:info'
    default: return 'i-fe:info'
  }
}

const demoEmailFilterAddress = ref('')
const filteredDemoEmails = computed(() => {
  if (!demoEmailFilterAddress.value)
    return demoEmails
  return demoEmails.filter(e => e.to === demoEmailFilterAddress.value || e.from === demoEmailFilterAddress.value)
})

function openEmailsAndFilter(address) {
  demoEmailFilterAddress.value = address
  openTab('emails', '邮件中心', true)
  triggerToast('info', `已过滤收发件人为 ${address} 的邮件`)
}

// Simulated Toast state
const demoToast = reactive({
  show: false,
  type: 'success',
  msg: '',
  timer: null,
})

function triggerToast(type, msg) {
  if (demoToast.timer)
    clearTimeout(demoToast.timer)
  demoToast.type = type
  demoToast.msg = msg
  demoToast.show = true
  demoToast.timer = setTimeout(() => {
    demoToast.show = false
  }, 2500)
}

// Simulated tab/tag state
const demoTabs = reactive([
  { path: '/dashboard', title: '工作台', key: 'dashboard', closable: false },
])
const demoActiveTab = ref('dashboard')

function openTab(key, title, keepFilter = false) {
  demoActiveNav.value = key
  demoActiveTab.value = key
  demoSelectedEmail.value = null
  if (!keepFilter) {
    demoEmailFilterAddress.value = ''
  }

  if (!demoTabs.some(tab => tab.key === key)) {
    demoTabs.push({
      path: `/${key}`,
      title,
      key,
      closable: true,
    })
  }
}

function closeTab(key) {
  const index = demoTabs.findIndex(tab => tab.key === key)
  if (index === -1)
    return

  demoTabs.splice(index, 1)
  if (demoActiveTab.value === key) {
    const nextActiveTab = demoTabs[demoTabs.length - 1]
    demoActiveNav.value = nextActiveTab.key
    demoActiveTab.value = nextActiveTab.key
    demoSelectedEmail.value = null
  }
}

const demoApplyForm = reactive({
  prefix: '',
  display_name: '',
  reason: '',
})
const demoApplyUploads = reactive([])

const demoSelectedEmail = ref(null)
const demoDrawerOpen = ref(false)

const demoDialogOpen = ref(false)
const demoReviewComment = ref('')
const demoReviewAction = ref('')
const demoSelectedApp = ref(null)

const demoAdminFilter = ref('all')
const demoUserDropdownOpen = ref(false)

// For simulated fullscreen inside mockup
const demoIsFullscreen = ref(false)

function toggleFullscreen() {
  demoIsFullscreen.value = !demoIsFullscreen.value
  if (demoIsFullscreen.value) {
    triggerToast('info', '已进入全屏演示模式，按 ESC 键或再次点击绿点可退出')
  }
  else {
    triggerToast('info', '已退出全屏演示模式')
  }
}

function handleKeyDown(e) {
  if (e.key === 'Escape' && demoIsFullscreen.value) {
    demoIsFullscreen.value = false
    triggerToast('info', '已退出全屏演示模式')
  }
}

function formatEmailBody(body) {
  if (!body)
    return ''
  return body.replace(/\n/g, '<br>')
}

// Detail modal preview for attachments
const demoAttachmentPreviewVisible = ref(false)
const demoAttachmentPreviewUrl = ref('')
const demoAttachmentPreviewName = ref('')

function openAttachmentPreview(file) {
  demoAttachmentPreviewName.value = file.name || file.filename || '证明文件'
  demoAttachmentPreviewUrl.value = file.url || '/wic-emblem.svg'
  demoAttachmentPreviewVisible.value = true
}

const demoMailboxes = reactive([
  { id: 1, address: 'zhangsan@wic.edu.kg', display_name: '张三的邮箱', is_active: true, created_at: '2024-09-01T09:00:00Z' },
  { id: 2, address: 'lab@wic.edu.kg', display_name: '实验室公共邮箱', is_active: true, created_at: '2024-09-20T08:30:00Z' },
])

const demoEmails = reactive([
  { id: 1, from: 'noreply@wic.edu.kg', to: 'zhangsan@wic.edu.kg', subject: '欢迎使用 WicMail 校园邮箱服务', time: '09:00', fullTime: '2024-09-01 09:00:01', isRead: true, attachment_count: 0, body: '欢迎使用 WicMail 校园邮箱服务！您的邮箱 zhangsan@wic.edu.kg 已成功开通。您可以开始收发邮件了！如有问题请联系管理员。' },
  { id: 2, from: 'system@wic.edu.kg', to: 'zhangsan@wic.edu.kg', subject: '【系统通知】邮箱服务维护公告', time: '10:00', fullTime: '2024-09-25 10:00:02', isRead: false, attachment_count: 0, body: '尊敬的用户：系统将于本周六凌晨 2:00-4:00 进行例行维护，届时邮件服务将短暂中断。给您带来的不便，敬请谅解。' },
  { id: 3, from: 'wangwu@gmail.com', to: 'zhangsan@wic.edu.kg', subject: 'Re: 课程项目讨论', time: '14:30', fullTime: '2024-09-24 14:30:05', isRead: false, attachment_count: 1, body: '张三你好，关于课程项目的分工我已经整理了一份文档。主要内容包括：1. 前端模块 - 由你负责 2. 后端模块 - 由我负责 3. 测试与部署 - 共同完成。请在周五前确认你的部分，谢谢！', attachments: [{ filename: '分工明细.pdf', size: 1048576 }] },
  { id: 4, from: 'noreply@github.com', to: 'zhangsan@wic.edu.kg', subject: 'GitHub: Your personal access token will expire in 7 days', time: '08:00', fullTime: '2024-09-23 08:00:03', isRead: true, attachment_count: 0, body: 'Your personal access token "WicMail CI" will expire on October 1, 2024. Please regenerate your token to continue using GitHub API access.' },
  { id: 5, from: 'professor.liu@wic.edu.kg', to: 'lab@wic.edu.kg', subject: '实验室周报 - 第38周', time: '09:15', fullTime: '2024-09-22 09:15:02', isRead: false, attachment_count: 0, body: '各位同学好，请在本周五前提交第38周的实验报告，报告格式请参考上周的模板。本周重点：完成模型训练实验、整理实验数据、撰写实验分析。' },
  { id: 6, from: 'noreply@wic.edu.kg', to: 'zhangsan@wic.edu.kg', subject: '新的邮箱申请待审核', time: '08:30', fullTime: '2024-09-20 08:30:03', isRead: true, attachment_count: 0, body: '您提交的邮箱申请 lab@wic.edu.kg 已进入审核流程，请耐心等待管理员审批。您可以在工作台中随时查看审核进度。' },
])

const demoApplications = reactive([
  { id: 1, user: 'admin', email: 'admin@wic.edu.kg', display_name: '系统管理员', status: 'approved', statusText: '已批准', reason: '初始化账户', review_comment: '自动开通', created_at: '2024-09-01 08:00:00' },
  { id: 2, user: 'zhangsan', email: 'zhangsan@wic.edu.kg', display_name: '张三的邮箱', status: 'approved', statusText: '已批准', reason: '个人学术交流', review_comment: '符合规范', created_at: '2024-09-01 09:00:00' },
  { id: 3, user: 'zhangsan', email: 'lab@wic.edu.kg', display_name: '实验室公共邮箱', status: 'approved', statusText: '已批准', reason: '实验室项目通知', review_comment: '导师已签字', created_at: '2024-09-20 08:30:00' },
  { id: 4, user: 'lisi', email: 'lisi@wic.edu.kg', display_name: '李四的邮箱', status: 'pending', statusText: '待审核', reason: '毕业设计联系导师', review_comment: '', created_at: '2024-09-25 10:00:00', attachments: [{ name: 'student_card.png', type: 'image/png', size: 1536240 }] },
  { id: 5, user: 'lisi', email: 'test123@wic.edu.kg', display_name: '测试邮箱', status: 'rejected', statusText: '已拒绝', reason: '测试申请', review_comment: '字符长度不足或名称不合规', created_at: '2024-09-20 11:00:00' },
])

const demoUsers = reactive([
  { id: 1, username: 'admin', email: 'admin@wic.edu.kg', is_admin: true, is_active: true, created_at: '2024-09-01 08:00:00' },
  { id: 2, username: 'zhangsan', email: 'zhangsan@wic.edu.kg', is_admin: false, is_active: true, created_at: '2024-09-01 09:00:00' },
  { id: 3, username: 'lisi', email: 'lisi@wic.edu.kg', is_admin: false, is_active: true, created_at: '2024-09-02 10:00:00' },
  { id: 4, username: 'wangwu', email: 'wangwu@gmail.com', is_admin: false, is_active: false, created_at: '2024-09-03 11:30:00' },
])

const demoUnreadEmailCount = computed(() => demoEmails.filter(e => !e.isRead).length)
const demoPendingAppCount = computed(() => demoApplications.filter(a => a.status === 'pending').length)

const demoStats = computed(() => [
  { value: demoMailboxes.length, label: '我的邮箱', icon: 'i-fe:mail' },
  { value: demoEmails.length, label: '总邮件数', icon: 'i-fe:inbox' },
  { value: demoUnreadEmailCount.value, label: '未读邮件', icon: 'i-fe:bell' },
  { value: demoPendingAppCount.value, label: '待审申请', icon: 'i-fe:clock' },
])

const filteredApplications = computed(() => {
  if (demoAdminFilter.value === 'all')
    return demoApplications
  return demoApplications.filter(app => app.status === demoAdminFilter.value)
})

const demoProfileForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

function handleProfileSave() {
  if (!demoProfileForm.oldPassword) {
    triggerToast('error', '请输入当前旧密码')
    return
  }
  if (!demoProfileForm.newPassword) {
    triggerToast('error', '请输入新密码')
    return
  }
  if (demoProfileForm.newPassword.length < 6) {
    triggerToast('error', '新密码长度不能小于 6 位')
    return
  }
  if (demoProfileForm.newPassword !== demoProfileForm.confirmPassword) {
    triggerToast('error', '新密码与确认密码不一致')
    return
  }
  triggerToast('success', '密码及安全信息已更新！')
  demoProfileForm.oldPassword = ''
  demoProfileForm.newPassword = ''
  demoProfileForm.confirmPassword = ''
}

function handleApplySubmit() {
  if (!demoApplyForm.prefix) {
    triggerToast('error', '请输入邮箱前缀')
    return
  }
  if (!/^[a-z0-9][\w.-]{2,29}$/i.test(demoApplyForm.prefix)) {
    triggerToast('error', '前缀格式不正确')
    return
  }
  const email = `${demoApplyForm.prefix}@wic.edu.kg`
  if (demoApplications.some(app => app.email === email && app.status !== 'rejected')) {
    triggerToast('error', '该邮箱前缀已被申请或已占用')
    return
  }

  const newApp = {
    id: demoApplications.length + 1,
    user: 'zhangsan',
    email,
    display_name: demoApplyForm.display_name,
    status: 'pending',
    statusText: '待审核',
    reason: demoApplyForm.reason,
    review_comment: '',
    created_at: new Date().toISOString().replace('T', ' ').slice(0, 16).replace(/-/g, '/'),
    attachments: [...demoApplyUploads],
  }

  demoApplications.unshift(newApp)
  demoApplyForm.prefix = ''
  demoApplyForm.display_name = ''
  demoApplyForm.reason = ''
  demoApplyUploads.splice(0, demoApplyUploads.length)
}

function handleApplyReset() {
  demoApplyForm.prefix = ''
  demoApplyForm.display_name = ''
  demoApplyForm.reason = ''
  demoApplyUploads.splice(0, demoApplyUploads.length)
}

function simulateUpload(type) {
  if (demoApplyUploads.length >= 5)
    return
  const filename = type === 'img'
    ? `student_card_mock_${demoApplyUploads.length + 1}.png`
    : `supplementary_file_${demoApplyUploads.length + 1}.pdf`
  demoApplyUploads.push({
    name: filename,
    type: type === 'img' ? 'image/png' : 'application/pdf',
    size: Math.floor(Math.random() * 2000000) + 500000,
    url: type === 'img' ? '/wic-emblem.svg' : '',
  })
}

function removeUpload(index) {
  demoApplyUploads.splice(index, 1)
}

function openEmailDetail(email) {
  demoSelectedEmail.value = email
  demoDrawerOpen.value = true
  email.isRead = true
}

function toggleEmailReadState(email) {
  email.isRead = !email.isRead
}

function openReview(app, action) {
  demoSelectedApp.value = app
  demoReviewAction.value = action
  demoReviewComment.value = ''
  demoDialogOpen.value = true
}

function handleReviewConfirm() {
  if (!demoSelectedApp.value)
    return
  const app = demoSelectedApp.value
  if (demoReviewAction.value === 'approve') {
    app.status = 'approved'
    app.statusText = '已批准'
    demoMailboxes.push({
      id: demoMailboxes.length + 1,
      address: app.email,
      display_name: app.display_name || '未命名邮箱',
      is_active: true,
      created_at: new Date().toISOString(),
    })
  }
  else {
    app.status = 'rejected'
    app.statusText = '已拒绝'
  }
  app.review_comment = demoReviewComment.value
  demoDialogOpen.value = false
  demoSelectedApp.value = null
}

function toggleUserActive(user) {
  user.is_active = !user.is_active
  triggerToast('success', `用户 ${user.username} 已${user.is_active ? '启用' : '禁用'}`)
}

function handleScroll() {
  scrollY.value = pageRef.value?.scrollTop || window.scrollY
}

function scrollToSection(id) {
  const page = pageRef.value
  const target = document.getElementById(id)
  if (!page || !target)
    return

  const pageTop = page.getBoundingClientRect().top
  const targetTop = target.getBoundingClientRect().top
  page.scrollTo({
    top: page.scrollTop + targetTop - pageTop - 72,
    behavior: 'smooth',
  })
}

function handleDocumentClick(e) {
  const trigger = document.querySelector('.demo-user-trigger')
  if (trigger && !trigger.contains(e.target)) {
    demoUserDropdownOpen.value = false
  }
}

onMounted(() => {
  handleScroll()
  pageRef.value?.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('keydown', handleKeyDown)
  document.addEventListener('click', handleDocumentClick)
  // Start automated tour
  startTour()
})

onUnmounted(() => {
  pageRef.value?.removeEventListener('scroll', handleScroll)
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('keydown', handleKeyDown)
  document.removeEventListener('click', handleDocumentClick)
  if (tourTimer) {
    clearTimeout(tourTimer)
    tourTimer = null
  }
})
</script>

<style scoped>
.landing-page {
  --wic-primary: #31552b;
  --wic-primary-strong: #243f20;
  --wic-accent: #9ee7a8;
  --wic-ink: #172216;
  --wic-muted: #627067;
  --wic-line: rgba(49, 85, 43, 0.14);
  --surface: #f7faf5;
  position: absolute;
  inset: 0;
  overflow-x: hidden;
  overflow-y: auto;
  color: var(--wic-ink);
  background: #fbfcfa;
  scroll-behavior: smooth;
  scrollbar-width: none;
  -webkit-overflow-scrolling: touch;
}

.landing-page::-webkit-scrollbar {
  display: none;
}

/* ==================== Navbar ==================== */
.site-nav {
  position: fixed;
  z-index: 50;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0);
  border-bottom: 1px solid transparent;
  transition:
    background-color 0.3s ease,
    border-color 0.3s ease,
    box-shadow 0.3s ease,
    backdrop-filter 0.3s ease;
}

.site-nav-solid {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom-color: rgba(0, 0, 0, 0.06);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 clamp(16px, 4vw, 48px);
  display: flex;
  align-items: center;
  height: 64px;
}

@media (min-width: 768px) {
  .nav-inner {
    height: 72px;
  }
}

/* Logo */
.nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  min-width: 140px;
  flex-shrink: 0;
}

.nav-logo-img {
  width: 36px;
  height: 36px;
  object-fit: contain;
  transition: transform 0.2s ease;
}

@media (min-width: 768px) {
  .nav-logo-img {
    width: 40px;
    height: 40px;
  }
}

.nav-logo:hover .nav-logo-img {
  transform: scale(1.05);
}

.nav-logo-text {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  white-space: nowrap;
}

.site-nav:not(.site-nav-solid) .nav-logo-text {
  color: #1e293b;
}

/* Nav Links (Desktop) */
.nav-links {
  display: none;
  align-items: center;
  gap: 32px;
  margin-left: 32px;
}

@media (min-width: 768px) {
  .nav-links {
    display: flex;
  }
}

.nav-link {
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  text-decoration: none;
  white-space: nowrap;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: #1e293b;
}

/* Right Actions */
.nav-right {
  flex: 1;
  display: none;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
}

@media (min-width: 768px) {
  .nav-right {
    display: flex;
  }
}

.nav-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  color: #64748b;
  text-decoration: none;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
}

.nav-icon-btn:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #1e293b;
}

.nav-cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  color: #fff;
  background: var(--wic-primary, #3f632f);
  transition:
    background-color 0.2s ease,
    transform 0.15s ease;
}

.nav-cta-btn:hover {
  background: var(--wic-secondary, #5c8d44);
  transform: translateY(-1px);
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: none;
  background: none;
  color: #64748b;
  cursor: pointer;
  margin-left: auto;
  transition: background-color 0.2s ease;
}

.mobile-menu-btn:hover {
  background: rgba(0, 0, 0, 0.05);
}

@media (min-width: 768px) {
  .mobile-menu-btn {
    display: none;
  }
}

.mobile-menu-active {
  color: #1e293b;
}

/* Mobile Dropdown */
.mobile-dropdown {
  max-height: 0;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  transition:
    max-height 0.3s ease,
    padding 0.3s ease;
  padding: 0 16px;
}

.mobile-dropdown-open {
  max-height: 400px;
  padding: 8px 16px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

@media (min-width: 768px) {
  .mobile-dropdown {
    display: none;
  }
}

.mobile-link {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  color: #475569;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.mobile-link:hover {
  background: rgba(0, 0, 0, 0.03);
  color: var(--wic-primary, #3f632f);
}

.mobile-cta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
  padding: 12px;
  border-radius: 8px;
  background: var(--wic-primary, #3f632f);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.mobile-cta:hover {
  background: var(--wic-secondary, #5c8d44);
}

/* ==================== Hero ==================== */
.hero-section {
  position: relative;
  overflow: hidden;
  padding-top: 96px;
  padding-bottom: 64px;
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
}

@media (min-width: 1024px) {
  .hero-section {
    min-height: 100vh;
    align-items: center;
    padding-top: 80px;
    padding-bottom: 0;
  }
}

.hero-bg-layer {
  position: absolute;
  inset: 0;
  background: #fff;
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(63, 99, 47, 0.04), transparent 40%, transparent);
}

.hero-grid-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.15;
  background-image:
    linear-gradient(rgba(0, 0, 0, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 0, 0, 0.03) 1px, transparent 1px);
  background-size: 48px 48px;
}

@media (prefers-color-scheme: dark) {
  .hero-grid-pattern {
    opacity: 0.06;
  }
}

.hero-container {
  position: relative;
  z-index: 10;
  max-width: 1600px;
  margin: 0 auto;
  padding: 16px clamp(16px, 4vw, 48px);
  width: 100%;
}

@media (min-width: 640px) {
  .hero-container {
    padding: 24px clamp(16px, 4vw, 48px);
  }
}

@media (min-width: 768px) {
  .hero-container {
    padding: 48px clamp(16px, 4vw, 48px);
  }
}

.hero-grid {
  display: grid;
  gap: 24px;
  align-items: center;
}

@media (min-width: 1024px) {
  .hero-grid {
    grid-template-columns: 4.2fr 5.8fr;
    gap: 24px;
  }
}

@media (min-width: 1280px) {
  .hero-grid {
    grid-template-columns: 1fr 2fr;
    gap: 32px;
  }
}

/* Hero Text (Left) */
.hero-text {
  text-align: center;
  margin: 0 auto;
}

@media (min-width: 1024px) {
  .hero-text {
    text-align: left;
    padding-left: 16px;
    padding-right: 16px;
    margin: 0;
  }
}

@media (min-width: 1280px) {
  .hero-text {
    padding-left: 32px;
  }
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  border-radius: 999px;
  border: 1px solid rgba(63, 99, 47, 0.15);
  background: rgba(63, 99, 47, 0.06);
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 32px;
}

@media (min-width: 640px) {
  .hero-badge {
    padding: 8px 20px;
    font-size: 16px;
    margin-bottom: 40px;
  }
}

.hero-title-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 24px;
}

@media (min-width: 1024px) {
  .hero-title-row {
    justify-content: flex-start;
  }
}

@media (min-width: 640px) {
  .hero-title-row {
    gap: 20px;
    margin-bottom: 32px;
  }
}

.hero-emblem {
  width: 44px;
  height: 44px;
  object-fit: contain;
  flex-shrink: 0;
}

@media (min-width: 640px) {
  .hero-emblem {
    width: 48px;
    height: 48px;
  }
}

@media (min-width: 768px) {
  .hero-emblem {
    width: 56px;
    height: 56px;
  }
}

@media (min-width: 1024px) {
  .hero-emblem {
    width: 64px;
    height: 64px;
  }
}

.hero-title {
  font-size: 30px;
  font-weight: 700;
  color: #1e293b;
  white-space: nowrap;
  margin: 0;
}

@media (min-width: 640px) {
  .hero-title {
    font-size: 36px;
  }
}

@media (min-width: 768px) {
  .hero-title {
    font-size: 36px;
  }
}

@media (min-width: 1024px) {
  .hero-title {
    font-size: 48px;
  }
}

@media (min-width: 1280px) {
  .hero-title {
    font-size: 60px;
  }
}

.hero-tagline {
  font-size: 20px;
  font-weight: 700;
  color: var(--wic-primary, #3f632f);
  margin: 0 0 12px 0;
  line-height: 1.3;
}

@media (min-width: 768px) {
  .hero-tagline {
    font-size: 24px;
  }
}

@media (min-width: 1024px) {
  .hero-tagline {
    font-size: 26px;
  }
}

.hero-description {
  font-size: 14px;
  line-height: 1.6;
  color: #64748b;
  margin-top: 14px;
  margin-bottom: 24px;
  max-width: 520px;
}

@media (min-width: 768px) {
  .hero-description {
    font-size: 15px;
    margin-top: 16px;
    margin-bottom: 28px;
  }
}

.hero-features {
  list-style: none;
  padding: 0;
  margin: 0 0 28px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 520px;
}

.hero-features li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 13px;
  line-height: 1.5;
  color: #475569;
  text-align: left;
}

@media (min-width: 768px) {
  .hero-features li {
    font-size: 14px;
  }
}

.hero-features i {
  color: var(--wic-primary, #3f632f);
  font-size: 16px;
  margin-top: 2px;
  flex-shrink: 0;
}

.hero-features strong {
  color: #1e293b;
}

.hero-cta {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 768px;
  margin: 0 auto;
}

@media (min-width: 640px) {
  .hero-cta {
    flex-direction: row;
    gap: 16px;
  }
}

@media (min-width: 1024px) {
  .hero-cta {
    justify-content: flex-start;
    margin: 0;
  }
}

.hero-btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 28px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  color: #fff;
  background: var(--wic-primary, #3f632f);
  box-shadow: 0 4px 12px rgba(63, 99, 47, 0.2);
  transition: all 0.2s ease;
  width: 100%;
}

.hero-btn-primary:hover {
  background: var(--wic-secondary, #5c8d44);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(63, 99, 47, 0.3);
}

.hero-btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 28px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  color: #1e293b;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
  width: 100%;
}

.hero-btn-secondary:hover {
  background: rgba(0, 0, 0, 0.03);
  border-color: rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

@media (min-width: 640px) {
  .hero-btn-primary,
  .hero-btn-secondary {
    width: auto;
    padding: 14px 32px;
    font-size: 16px;
  }
}

.hero-platform {
  margin-top: 16px;
  font-size: 12px;
  color: #94a3b8;
  text-align: center;
}

@media (min-width: 1024px) {
  .hero-platform {
    text-align: left;
  }
}

/* Hero Demo (Right - Product Mockup) */
.hero-demo {
  display: none;
  justify-content: flex-end;
  position: relative;
}

@media (min-width: 1024px) {
  .hero-demo {
    display: flex;
  }
}

/* ==================== Demo: Theme Variables & Window ==================== */
.demo-glow {
  position: absolute;
  inset: -40px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(5, 150, 105, 0.12), rgba(128, 90, 213, 0.08));
  filter: blur(48px);
  pointer-events: none;
}

.demo-window {
  --demo-bg: #f7f7fa;
  --demo-sidebar-bg: #ffffff;
  --demo-card-bg: #ffffff;
  --demo-header-bg: #ffffff;
  --demo-text: #333639;
  --demo-text-muted: #767c82;
  --demo-border: #efeff5;
  --demo-input-bg: #ffffff;
  --demo-primary: #18a058;
  --demo-primary-hover: #36ad6a;
  --demo-accent-bg: rgba(24, 160, 88, 0.08);
  --demo-accent-hover: rgba(24, 160, 88, 0.12);
  --demo-item-hover: #f3f3f5;
  --demo-shadow:
    0 1px 2px -2px rgba(0, 0, 0, 0.08), 0 3px 6px 0 rgba(0, 0, 0, 0.06), 0 5px 12px 8px rgba(0, 0, 0, 0.04);

  position: relative;
  height: 530px;
  width: 100%;
  max-width: 800px;
  overflow: hidden;
  border-radius: 8px;
  border: 1px solid var(--demo-border);
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
  background: var(--demo-bg);
  color: var(--demo-text);
  font-family:
    Inter,
    system-ui,
    -apple-system,
    sans-serif;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@media (min-width: 1280px) {
  .demo-window {
    height: 640px;
    max-width: 960px;
  }
}

@media (min-width: 1536px) {
  .demo-window {
    height: 730px;
    max-width: 1120px;
  }
}

.demo-window.demo-window-fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  max-width: none;
  max-height: none;
  border-radius: 0;
  z-index: 9999;
}

.demo-window.demo-dark-theme {
  --demo-bg: #101014;
  --demo-sidebar-bg: #18181c;
  --demo-card-bg: #18181c;
  --demo-header-bg: #18181c;
  --demo-text: rgba(255, 255, 255, 0.82);
  --demo-text-muted: rgba(255, 255, 255, 0.52);
  --demo-border: #303033;
  --demo-input-bg: #101014;
  --demo-primary: #63e2b7;
  --demo-primary-hover: #7fe7c4;
  --demo-accent-bg: rgba(99, 226, 183, 0.12);
  --demo-accent-hover: rgba(99, 226, 183, 0.18);
  --demo-item-hover: rgba(255, 255, 255, 0.09);
  --demo-shadow:
    0 1px 2px -2px rgba(0, 0, 0, 0.24), 0 3px 6px 0 rgba(0, 0, 0, 0.18), 0 5px 12px 8px rgba(0, 0, 0, 0.12);
}

.demo-closed-placeholder {
  width: 100%;
  height: 480px;
  background: var(--demo-card-bg, #ffffff);
  border: 1px dashed var(--demo-border, #efeff5);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  text-align: center;
  color: var(--demo-text, #333639);
}

@media (min-width: 1280px) {
  .demo-closed-placeholder {
    height: 560px;
  }
}

@media (min-width: 1536px) {
  .demo-closed-placeholder {
    height: 610px;
  }
}

.demo-closed-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(24, 160, 88, 0.1);
  color: #18a058;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.demo-closed-placeholder h3 {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.demo-closed-placeholder p {
  font-size: 12px;
  color: var(--demo-text-muted, #767c82);
  margin: 0 0 24px 0;
  max-width: 320px;
  line-height: 1.6;
}

.demo-titlebar {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 38px;
  padding: 0 12px;
  border-bottom: 1px solid var(--demo-border);
  background: var(--demo-sidebar-bg);
  flex-shrink: 0;
  z-index: 10;
}

.demo-dots {
  display: flex;
  gap: 7px;
}
.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: filter 0.2s;
}
.dot:hover {
  filter: brightness(0.85);
}
.dot-red {
  background: #ff5f57;
}
.dot-yellow {
  background: #febc2e;
}
.dot-green {
  background: #28c840;
}

.dot-svg-icon {
  width: 6px;
  height: 6px;
  opacity: 0;
  transition: opacity 0.15s ease;
  display: block;
}
.demo-dots:hover .dot-svg-icon {
  opacity: 1;
}

.dot-red .dot-svg-icon {
  color: #4c0002;
}
.dot-yellow .dot-svg-icon {
  color: #5c3e00;
}
.dot-green .dot-svg-icon {
  color: #024c00;
}

.demo-titlebar-text {
  flex: 1;
  text-align: center;
  font-size: 12px;
  color: var(--demo-text-muted);
  margin-right: 44px;
}

/* ==================== Demo: Layout ==================== */
.demo-body {
  display: flex;
  flex: 1;
  overflow: hidden;
  background: var(--demo-bg);
  position: relative;
}

/* Sidebar */
.demo-sidebar {
  width: 220px;
  background: var(--demo-sidebar-bg);
  border-right: 1px solid var(--demo-border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  padding: 0;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.demo-sidebar-collapsed {
  width: 60px;
}

.demo-sidebar-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 16px 12px;
  border-bottom: 1px solid var(--demo-border);
  height: 52px;
  box-sizing: border-box;
}

.demo-sidebar-logo-img {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.demo-sidebar-logo-text {
  font-size: 15px;
  font-weight: 700;
  color: var(--demo-text);
  white-space: nowrap;
}

.demo-sidebar-nav {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
  flex: 1;
}

.demo-sidebar-nav::-webkit-scrollbar {
  display: none;
}

.demo-nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
  color: var(--demo-text-muted);
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
  position: relative;
  white-space: nowrap;
}

.demo-nav-item:hover {
  background: var(--demo-item-hover);
  color: var(--demo-text);
}

.demo-nav-active {
  background: var(--demo-accent-bg);
  color: var(--demo-primary);
  font-weight: 600;
}

.demo-nav-active:hover {
  background: var(--demo-accent-hover);
  color: var(--demo-primary);
}

.demo-nav-icon {
  font-size: 16px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.demo-nav-arrow {
  margin-left: auto;
  font-size: 10px;
  opacity: 0.6;
}

.demo-nav-group {
  display: flex;
  flex-direction: column;
}

.demo-nav-sub {
  padding-left: 18px;
  margin-top: 2px;
  margin-bottom: 4px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.demo-nav-sub-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  color: var(--demo-text-muted);
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.demo-nav-sub-item:hover {
  background: var(--demo-item-hover);
  color: var(--demo-text);
}

.demo-nav-sub-active {
  color: var(--demo-primary);
  font-weight: 600;
  background: var(--demo-accent-bg);
}

.demo-menu-badge {
  margin-left: auto;
  background: #2080f0;
  color: #fff;
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 99px;
  font-weight: 700;
  line-height: 1;
}

.demo-menu-badge-alert {
  margin-left: auto;
  background: #f0a020;
  color: #fff;
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 99px;
  font-weight: 700;
  line-height: 1;
}

/* Main Area Layout */
.demo-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.demo-header {
  height: 52px;
  background: var(--demo-header-bg);
  border-bottom: 1px solid var(--demo-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  flex-shrink: 0;
  z-index: 5;
}

.demo-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 100%;
  flex: 1;
  min-width: 0;
}

.demo-collapse-btn {
  font-size: 16px;
  color: var(--demo-text-muted);
  cursor: pointer;
  transition: color 0.2s;
  padding: 4px;
  border-radius: 4px;
  align-self: center;
}

.demo-collapse-btn:hover {
  color: var(--demo-text);
  background: var(--demo-item-hover);
}

.demo-tabs {
  display: flex;
  gap: 4px;
  align-items: flex-end;
  height: 100%;
  padding-top: 8px;
  overflow-x: auto;
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  scrollbar-width: none; /* Firefox */
}

.demo-tabs::-webkit-scrollbar {
  display: none; /* Safari and Chrome */
}

.demo-tabs::-webkit-scrollbar {
  display: none;
}

.demo-tab-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  padding: 4px 10px;
  background: var(--demo-bg);
  border: 1px solid var(--demo-border);
  border-bottom: none;
  border-radius: 4px 4px 0 0;
  color: var(--demo-text-muted);
  cursor: pointer;
  transition: all 0.15s ease;
  height: 28px;
  box-sizing: border-box;
  margin-bottom: -1px;
  position: relative;
  white-space: nowrap;
}

.demo-tab-item:hover {
  color: var(--demo-text);
  background: var(--demo-item-hover);
}

.demo-tab-active {
  background: var(--demo-card-bg);
  color: var(--demo-primary);
  border-bottom: 1px solid var(--demo-card-bg);
  height: 29px;
  font-weight: 600;
  z-index: 2;
}

.demo-tab-title {
  line-height: 1;
}

.demo-tab-close {
  font-size: 9px;
  opacity: 0.5;
  transition: all 0.15s;
  border-radius: 50%;
  padding: 2px;
  width: 12px;
  height: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.demo-tab-close:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.08);
  color: var(--demo-primary);
}

.demo-dark-theme .demo-tab-close:hover {
  background: rgba(255, 255, 255, 0.15);
}

.demo-header-right {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}

.demo-tool-icon {
  font-size: 16px;
  color: var(--demo-text-muted);
  cursor: pointer;
  transition: color 0.2s;
  padding: 4px;
  border-radius: 4px;
}

.demo-tool-icon:hover {
  color: var(--demo-text);
  background: var(--demo-item-hover);
}

.demo-user-trigger {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  position: relative;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.demo-user-trigger:hover {
  background: var(--demo-item-hover);
}

.demo-header-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--demo-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
}

.demo-header-username {
  font-size: 12px;
  font-weight: 500;
  color: var(--demo-text);
}

.demo-user-dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  background: var(--demo-card-bg);
  border: 1px solid var(--demo-border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  width: 110px;
  padding: 4px;
  z-index: 100;
}

.demo-dropdown-item {
  display: flex;
  align-items: center;
  padding: 6px 10px;
  font-size: 11px;
  color: var(--demo-text-muted);
  border-radius: 3px;
  transition: all 0.15s;
}

.demo-dropdown-item:hover {
  background: var(--demo-item-hover);
  color: var(--demo-text);
}

/* ==================== Demo: Content Area ==================== */
.demo-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: relative;
}

/* Page header */
.demo-page-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  color: var(--demo-text);
  margin-bottom: 2px;
}

.demo-page-icon {
  font-size: 16px;
  color: var(--demo-primary);
}

.demo-admin-filter {
  margin-left: auto;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 3px;
  border: 1px solid var(--demo-border);
  background: var(--demo-input-bg);
  color: var(--demo-text);
  outline: none;
  cursor: pointer;
}

/* ==================== Demo: Cards (Naive UI style) ==================== */
.demo-card {
  background: var(--demo-card-bg);
  border-radius: 6px;
  border: 1px solid var(--demo-border);
  padding: 12px;
  box-shadow: var(--demo-shadow);
  transition:
    background-color 0.3s,
    border-color 0.3s,
    box-shadow 0.3s;
}

.demo-card-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: var(--demo-text);
  padding-bottom: 8px;
  border-bottom: 1px solid var(--demo-border);
  margin-bottom: 8px;
}

.demo-card-header-icon {
  font-size: 15px;
  color: var(--demo-primary);
}

.demo-card-text {
  font-size: 12px;
  color: var(--demo-text-muted);
  line-height: 1.6;
  margin: 0 0 10px;
}

.demo-card-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

/* ==================== Demo: Buttons (Naive UI style) ==================== */
.demo-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  user-select: none;
}

.demo-btn-primary {
  background: var(--demo-primary);
  color: #fff;
  border-color: var(--demo-primary);
}

.demo-btn-primary:hover {
  background: var(--demo-primary-hover);
  border-color: var(--demo-primary-hover);
}

.demo-btn-ghost {
  background: transparent;
  color: var(--demo-primary);
  border-color: var(--demo-primary);
}

.demo-btn-ghost:hover {
  background: var(--demo-accent-bg);
}

/* ==================== Demo: Top Row ==================== */
.demo-top-row {
  display: flex;
  gap: 12px;
}

.demo-card-user {
  width: 30%;
  flex-shrink: 0;
}

.demo-card-overview {
  flex: 1;
}

.demo-user-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.demo-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: var(--demo-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  flex-shrink: 0;
}

.demo-user-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.demo-user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--demo-text);
}

.demo-user-role {
  font-size: 11px;
  color: var(--demo-text-muted);
}

.demo-user-desc {
  margin: 10px 0 0;
  font-size: 11px;
  color: var(--demo-text-muted);
  line-height: 1.5;
}

/* ==================== Demo: Stat Cards ==================== */
.demo-stat-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.demo-stat-card {
  background: var(--demo-card-bg);
  border-radius: 6px;
  border: 1px solid var(--demo-border);
  padding: 10px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1px;
  box-shadow: var(--demo-shadow);
}

.demo-stat-icon {
  font-size: 15px;
  color: var(--demo-primary);
  margin-bottom: 2px;
}

.demo-stat-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--demo-text);
  line-height: 1.2;
}

.demo-stat-label {
  font-size: 11px;
  color: var(--demo-text-muted);
}

/* ==================== Demo: Bottom Row ==================== */
.demo-bottom-row {
  display: flex;
  gap: 12px;
  flex: 1;
  min-height: 0;
}

.demo-card-emails {
  flex: 6;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.demo-card-mailbox {
  flex: 4;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.demo-mailbox-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow-y: auto;
  flex: 1;
}

.demo-mailbox-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  background: var(--demo-bg);
  border-radius: 4px;
}

.demo-mailbox-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.demo-mailbox-addr {
  font-size: 12px;
  font-weight: 600;
  color: var(--demo-text);
}

.demo-mailbox-name {
  font-size: 10px;
  color: var(--demo-text-muted);
}

/* ==================== Demo: Table ==================== */
.demo-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
}

.demo-table th {
  text-align: left;
  padding: 6px 8px;
  font-weight: 600;
  color: var(--demo-text);
  border-bottom: 1px solid var(--demo-border);
  white-space: nowrap;
}

.demo-table td {
  padding: 6px 8px;
  color: var(--demo-text-muted);
  border-bottom: 1px solid var(--demo-border);
}

.demo-table-full {
  flex: 1;
}

.demo-table-row {
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.demo-table-row:hover {
  background: var(--demo-item-hover);
}

.demo-td-from {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 90px;
  font-weight: 600;
  color: var(--demo-text);
}

.demo-td-subject {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 130px;
}

.demo-td-time {
  white-space: nowrap;
  color: var(--demo-text-muted);
  font-size: 10px;
}

.demo-attachment-count {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  color: var(--demo-primary);
  font-weight: 500;
}

/* ==================== Demo: Tags ==================== */
.demo-tag {
  display: inline-flex;
  align-items: center;
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 10px;
  font-weight: 500;
  white-space: nowrap;
  line-height: 1.2;
}

.demo-tag-default {
  background: var(--demo-bg);
  color: var(--demo-text-muted);
  border: 1px solid var(--demo-border);
}

.demo-tag-info {
  background: rgba(32, 128, 240, 0.1);
  color: #2080f0;
  border: 1px solid rgba(32, 128, 240, 0.2);
}

.demo-tag-success {
  background: rgba(24, 160, 88, 0.1);
  color: #18a058;
  border: 1px solid rgba(24, 160, 88, 0.2);
}

.demo-tag-warning {
  background: rgba(240, 160, 32, 0.1);
  color: #f0a020;
  border: 1px solid rgba(240, 160, 32, 0.2);
}

.demo-tag-error {
  background: rgba(208, 48, 80, 0.1);
  color: #d03050;
  border: 1px solid rgba(208, 48, 80, 0.2);
}

/* ==================== Demo: Form ==================== */
.demo-form-card {
  background: var(--demo-card-bg);
  border-radius: 6px;
  border: 1px solid var(--demo-border);
  padding: 14px;
}

.demo-form-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.demo-form-row:last-child {
  margin-bottom: 0;
}

.demo-form-row label {
  width: 64px;
  font-size: 12px;
  color: var(--demo-text);
  padding-top: 4px;
  text-align: right;
  flex-shrink: 0;
}

.demo-input {
  flex: 1;
  padding: 4px 10px;
  border: 1px solid var(--demo-border);
  border-radius: 4px;
  font-size: 12px;
  color: var(--demo-text);
  background: var(--demo-input-bg);
  outline: none;
  transition: border-color 0.2s ease;
}

.demo-input:focus {
  border-color: var(--demo-primary);
}

.demo-input::placeholder {
  color: var(--demo-text-muted);
  opacity: 0.5;
}

.demo-input-group {
  flex: 1;
  display: flex;
}

.demo-input-group .demo-input {
  border-radius: 4px 0 0 4px;
  border-right: none;
}

.demo-input-addon {
  display: flex;
  align-items: center;
  padding: 4px 10px;
  background: var(--demo-bg);
  border: 1px solid var(--demo-border);
  border-radius: 0 4px 4px 0;
  font-size: 12px;
  color: var(--demo-text-muted);
  white-space: nowrap;
}

.demo-textarea {
  flex: 1;
  padding: 4px 10px;
  border: 1px solid var(--demo-border);
  border-radius: 4px;
  font-size: 12px;
  color: var(--demo-text);
  background: var(--demo-input-bg);
  resize: none;
  height: 48px;
  outline: none;
  font-family: inherit;
}

.demo-textarea:focus {
  border-color: var(--demo-primary);
}

.demo-upload-container {
  flex: 1;
  display: flex;
  gap: 8px;
}

.demo-upload-zone {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  padding: 12px;
  border: 1.5px dashed var(--demo-border);
  border-radius: 4px;
  color: var(--demo-text-muted);
  font-size: 10px;
  cursor: pointer;
  transition:
    border-color 0.2s ease,
    background-color 0.2s;
  text-align: center;
}

.demo-upload-zone:hover {
  border-color: var(--demo-primary);
  background: var(--demo-accent-bg);
}

.demo-upload-icon {
  font-size: 18px;
  color: var(--demo-text-muted);
  opacity: 0.7;
}

.demo-upload-hint {
  font-size: 9px;
  color: var(--demo-text-muted);
  opacity: 0.6;
}

.demo-uploaded-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.demo-file-card {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  background: var(--demo-bg);
  border: 1px solid var(--demo-border);
  border-radius: 4px;
  font-size: 11px;
}

.demo-file-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--demo-text);
}

.demo-file-delete {
  color: #d03050;
  cursor: pointer;
  opacity: 0.7;
  padding: 2px;
  border-radius: 3px;
}

.demo-file-delete:hover {
  opacity: 1;
  background: rgba(208, 48, 80, 0.1);
}

.demo-action-buttons {
  display: flex;
  gap: 8px;
}

/* ==================== Demo: My Mailboxes Grid ==================== */
.demo-mailbox-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.demo-mailbox-card-full {
  background: var(--demo-card-bg);
  border: 1px solid var(--demo-border);
  border-radius: 6px;
  padding: 10px;
  box-shadow: var(--demo-shadow);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.demo-mb-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.demo-mb-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--demo-accent-bg);
  color: var(--demo-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.demo-mb-details {
  flex: 1;
  overflow: hidden;
}

.demo-mb-addr {
  font-size: 12px;
  font-weight: 700;
  color: var(--demo-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.demo-mb-name {
  font-size: 10px;
  color: var(--demo-text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.demo-mb-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--demo-border);
  padding-top: 8px;
}

.demo-mb-date {
  font-size: 10px;
  color: var(--demo-text-muted);
  opacity: 0.6;
}

.demo-mailbox-empty {
  grid-column: span 2;
  text-align: center;
  padding: 30px 0;
  color: var(--demo-text-muted);
  font-size: 12px;
}

/* ==================== Demo: Slide-out Drawer ==================== */
.demo-drawer-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 90;
}

.demo-drawer {
  position: absolute;
  top: 52px;
  right: 0;
  bottom: 0;
  width: 75%;
  background: var(--demo-card-bg);
  border-left: 1px solid var(--demo-border);
  box-shadow: -4px 0 16px rgba(0, 0, 0, 0.1);
  transform: translateX(100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 95;
  display: flex;
  flex-direction: column;
}

.demo-drawer-open {
  transform: translateX(0);
}

.demo-drawer-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.demo-drawer-header {
  padding: 12px;
  border-bottom: 1px solid var(--demo-border);
  flex-shrink: 0;
}

.demo-drawer-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.demo-drawer-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--demo-text);
}

.demo-drawer-close {
  font-size: 16px;
  color: var(--demo-text-muted);
  cursor: pointer;
  padding: 2px;
  border-radius: 4px;
}

.demo-drawer-close:hover {
  background: var(--demo-item-hover);
  color: var(--demo-text);
}

.demo-drawer-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 10px;
  color: var(--demo-text-muted);
}

.demo-drawer-meta strong {
  color: var(--demo-text);
}

.demo-drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  font-size: 12px;
  line-height: 1.6;
  color: var(--demo-text);
  white-space: pre-wrap;
}

.demo-drawer-attachments {
  padding: 12px;
  background: var(--demo-bg);
  border-top: 1px solid var(--demo-border);
  flex-shrink: 0;
}

.demo-drawer-section-title {
  font-size: 11px;
  font-weight: 700;
  color: var(--demo-text);
  margin-bottom: 6px;
}

.demo-drawer-file-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.demo-drawer-file-item {
  display: flex;
  align-items: center;
  font-size: 11px;
  color: var(--demo-text);
  padding: 4px 8px;
  background: var(--demo-card-bg);
  border: 1px solid var(--demo-border);
  border-radius: 4px;
}

.demo-drawer-file-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.demo-drawer-footer {
  padding: 10px 12px;
  border-top: 1px solid var(--demo-border);
  display: flex;
  justify-content: flex-end;
  flex-shrink: 0;
}

/* ==================== Demo: Modal Dialog ==================== */
.demo-dialog-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 110;
}

.demo-dialog-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  max-width: 480px;
  background: var(--demo-card-bg);
  border: 1px solid var(--demo-border);
  border-radius: 6px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  z-index: 120;
  display: flex;
  flex-direction: column;
}

.demo-dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border-bottom: 1px solid var(--demo-border);
}

.demo-dialog-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--demo-text);
}

.demo-dialog-close {
  font-size: 14px;
  color: var(--demo-text-muted);
  cursor: pointer;
  padding: 2px;
  border-radius: 4px;
}

.demo-dialog-close:hover {
  background: var(--demo-item-hover);
  color: var(--demo-text);
}

.demo-dialog-body {
  padding: 12px;
  font-size: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.demo-dialog-info-row {
  color: var(--demo-text);
  line-height: 1.5;
}

.demo-dialog-info-row strong {
  color: var(--demo-text-muted);
}

.demo-dialog-attachments-section {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.demo-dialog-section-title {
  font-weight: 700;
  color: var(--demo-text);
  margin-bottom: 2px;
}

.demo-dialog-attachments-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 6px;
}

.demo-dialog-attachment-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 6px;
  border: 1px solid var(--demo-border);
  border-radius: 4px;
  background: var(--demo-bg);
  overflow: hidden;
}

.demo-dialog-file-name {
  font-size: 9px;
  color: var(--demo-text-muted);
  text-align: center;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-top: 4px;
}

.demo-dialog-comment-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 4px;
}

.demo-dialog-comment-row label {
  font-weight: 700;
  color: var(--demo-text);
}

.demo-dialog-footer {
  padding: 10px 12px;
  border-top: 1px solid var(--demo-border);
  display: flex;
  justify-content: flex-end;
}

/* ==================== Demo: Admin Actions ==================== */
.demo-action-group {
  display: flex;
  gap: 6px;
}

.demo-action-btn {
  font-size: 10px;
  font-weight: 500;
  padding: 1px 6px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
  user-select: none;
}

.demo-action-approve {
  color: #18a058;
  border-color: #18a058;
}

.demo-action-approve:hover {
  background: #18a058;
  color: #fff;
}

.demo-action-reject {
  color: #d03050;
  border-color: #d03050;
}

.demo-action-reject:hover {
  background: #d03050;
  color: #fff;
}

.demo-action-disabled {
  font-size: 10px;
  color: var(--demo-text-muted);
  opacity: 0.5;
}

.section-container {
  width: min(100%, 1180px);
  margin: 0 auto;
  padding: 0 24px;
}

.section-kicker {
  margin: 0 0 10px;
  color: var(--wic-primary);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.18em;
}

.section-kicker.light {
  color: var(--wic-accent);
}

.section-header {
  max-width: 680px;
  margin-bottom: 38px;
}

.section-header h2,
.intro-copy h2,
.feature-lead h2,
.faq-layout h2,
.cta-panel h2 {
  margin: 0;
  color: var(--wic-ink);
  font-size: clamp(28px, 4vw, 44px);
  line-height: 1.16;
}

.section-header p:not(.section-kicker),
.intro-copy p,
.feature-lead p,
.faq-lead,
.cta-panel p,
.promise-item p,
.process-card p,
.feature-card p,
.scenario-card p,
.faq-item p,
.footer-brand p {
  color: var(--wic-muted);
  font-size: 15px;
  line-height: 1.78;
}

.intro-section,
.process-section,
.feature-section,
.scenario-section,
.faq-section {
  padding: 96px 0;
}

.intro-section,
.feature-section {
  background: #fff;
}

.process-section,
.faq-section {
  background: var(--surface);
}

.intro-grid,
.feature-layout,
.faq-layout {
  display: grid;
  grid-template-columns: minmax(0, 0.92fr) minmax(0, 1.08fr);
  gap: 46px;
  align-items: center;
}

.intro-copy p {
  max-width: 620px;
  margin: 18px 0 0;
}

.intro-actions {
  gap: 18px;
  margin-top: 26px;
}

.text-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--wic-primary);
  font-weight: 800;
  text-decoration: none;
}

.text-link.muted {
  color: var(--wic-muted);
}

.promise-panel {
  display: grid;
  gap: 14px;
}

.promise-item,
.process-card,
.feature-card,
.scenario-card,
.faq-item {
  border: 1px solid var(--wic-line);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 18px 44px rgba(38, 63, 34, 0.06);
}

.promise-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  border-radius: 14px;
}

.promise-icon {
  width: 48px;
  height: 48px;
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  color: var(--wic-primary);
  background: rgba(49, 85, 43, 0.08);
}

.promise-item h3,
.process-card h3,
.feature-card h3,
.scenario-card h3 {
  margin: 0 0 8px;
  color: var(--wic-ink);
  font-size: 18px;
}

.promise-item p,
.process-card p,
.feature-card p,
.scenario-card p {
  margin: 0;
}

.process-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}

.process-card {
  position: relative;
  min-height: 252px;
  padding: 26px;
  border-radius: 16px;
  overflow: hidden;
}

.step-index {
  position: absolute;
  top: 18px;
  right: 20px;
  color: rgba(49, 85, 43, 0.12);
  font-size: 46px;
  font-weight: 900;
  line-height: 1;
}

.process-icon,
.feature-card i {
  color: var(--wic-primary);
}

.process-icon {
  margin-bottom: 42px;
}

.feature-layout {
  align-items: start;
}

.feature-lead {
  position: sticky;
  top: 100px;
}

.feature-lead p {
  margin-top: 18px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.feature-card {
  min-height: 210px;
  padding: 24px;
  border-radius: 16px;
}

.feature-card i {
  margin-bottom: 24px;
}

.scenario-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.scenario-card {
  min-height: 220px;
  padding: 26px;
  border-radius: 16px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.78)), var(--surface);
}

.scenario-card span {
  display: inline-flex;
  margin-bottom: 34px;
  padding: 6px 10px;
  border-radius: 999px;
  color: var(--wic-primary);
  background: rgba(49, 85, 43, 0.08);
  font-size: 12px;
  font-weight: 800;
}

.faq-layout {
  align-items: start;
}

.faq-list {
  display: grid;
  gap: 12px;
}

.faq-item {
  border-radius: 14px;
  overflow: hidden;
}

.faq-item summary {
  min-height: 58px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  cursor: pointer;
  color: var(--wic-ink);
  font-weight: 800;
  list-style: none;
}

.faq-item summary::-webkit-details-marker {
  display: none;
}

.faq-item summary::after {
  content: '+';
  margin-left: auto;
  color: var(--wic-primary);
  font-size: 22px;
  line-height: 1;
}

.faq-item[open] summary::after {
  content: '-';
}

.faq-item p {
  margin: 0;
  padding: 0 20px 20px;
}

.cta-section {
  padding: 64px 0 90px;
  background: #fff;
}

.cta-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  padding: 42px;
  border-radius: 22px;
  color: #fff;
  background:
    linear-gradient(135deg, rgba(49, 85, 43, 0.96), rgba(25, 53, 24, 0.96)),
    url('/cover.avif') center / cover;
  box-shadow: 0 28px 70px rgba(49, 85, 43, 0.24);
}

.cta-panel h2,
.cta-panel p {
  color: #fff;
}

.cta-panel p {
  max-width: 610px;
  margin: 12px 0 0;
  opacity: 0.78;
}

.cta-btn {
  flex: 0 0 auto;
}

/* ==================== Footer ==================== */
.site-footer {
  background: #f8fafc;
  border-top: 4px solid var(--wic-primary, #3f632f);
  color: #334155;
  transition: background 0.3s ease;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 clamp(16px, 4vw, 48px);
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0;
  padding-top: 40px;
  padding-bottom: 32px;
}

@media (min-width: 1024px) {
  .footer-grid {
    grid-template-columns: 1.5fr 1fr 1fr 1.2fr;
    gap: 48px;
  }
}

/* Brand Column */
.footer-brand {
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 4px;
}

@media (min-width: 1024px) {
  .footer-brand {
    border-bottom: none;
    padding-bottom: 0;
    margin-bottom: 0;
  }
}

.footer-logo-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: inherit;
  margin-bottom: 12px;
}

.footer-logo-link:hover .footer-emblem {
  transform: scale(1.06);
}

.footer-emblem {
  width: 40px;
  height: 40px;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.footer-brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
}

.footer-brand-name {
  font-size: 18px;
  font-weight: 800;
  color: #1e293b;
}

.footer-brand-sub {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 2px;
}

.footer-desc {
  font-size: 14px;
  color: #64748b;
  line-height: 1.7;
  max-width: 320px;
  margin: 0 0 16px;
}

.footer-socials {
  display: flex;
  gap: 10px;
}

.footer-social-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #e2e8f0;
  color: #64748b;
  text-decoration: none;
  transition: all 0.3s ease;
}

.footer-social-btn:hover {
  background: var(--wic-primary, #3f632f);
  color: #fff;
}

/* Footer Columns */
.footer-col {
  border-bottom: 1px solid #e2e8f0;
}

.footer-col:last-child {
  border-bottom: none;
}

@media (min-width: 1024px) {
  .footer-col {
    border-bottom: none;
  }
}

.footer-col-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 16px 0;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
}

@media (min-width: 1024px) {
  .footer-col-toggle {
    padding: 0;
    margin-bottom: 20px;
    cursor: default;
  }
}

.footer-col-toggle h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.footer-chevron {
  color: #94a3b8;
  transition: transform 0.3s ease;
}

.footer-chevron-open {
  transform: rotate(180deg);
}

@media (min-width: 1024px) {
  .footer-chevron {
    display: none;
  }
}

.footer-col-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow: hidden;
  max-height: 0;
  padding-bottom: 0;
  transition:
    max-height 0.35s cubic-bezier(0.4, 0, 0.2, 1),
    padding-bottom 0.35s ease;
}

.footer-col-open {
  max-height: 300px;
  padding-bottom: 16px;
}

@media (min-width: 1024px) {
  .footer-col-body {
    max-height: none;
    overflow: visible;
    padding-bottom: 0;
  }
}

/* Footer Links */
.footer-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #64748b;
  text-decoration: none;
  transition: color 0.2s ease;
  width: fit-content;
}

.footer-link:hover {
  color: var(--wic-primary, #3f632f);
}

.footer-link-icon {
  color: #94a3b8;
  flex-shrink: 0;
  transition: color 0.2s ease;
}

.footer-link:hover .footer-link-icon {
  color: var(--wic-primary, #3f632f);
}

.footer-ext-icon {
  margin-left: 2px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.footer-link:hover .footer-ext-icon {
  opacity: 1;
}

/* Contact Items */
.footer-contact-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
}

.footer-contact-icon {
  color: var(--wic-primary, #3f632f);
  flex-shrink: 0;
  margin-top: 2px;
}

.footer-contact-link {
  color: #64748b;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-contact-link:hover {
  color: var(--wic-primary, #3f632f);
}

/* Bottom Bar */
.footer-bottom {
  border-top: 1px solid #e2e8f0;
  padding: 24px 0 20px;
  margin-top: 8px;
}

.footer-bottom-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
}

@media (min-width: 768px) {
  .footer-bottom-inner {
    flex-direction: row;
    justify-content: space-between;
    text-align: left;
  }
}

.footer-copy {
  font-size: 12px;
  color: #94a3b8;
  margin: 0;
}

.footer-motto {
  height: 44px;
  width: auto;
  opacity: 0.7;
  display: none;
}

@media (min-width: 768px) {
  .footer-motto {
    display: block;
  }
}

.footer-credit {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #94a3b8;
  background: #fff;
  padding: 5px 12px;
  border-radius: 999px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  border: 1px solid #f1f5f9;
}

.footer-credit strong {
  color: #475569;
  font-weight: 700;
}

.footer-legal {
  margin: 16px 0 0;
  padding-top: 16px;
  border-top: 1px solid rgba(226, 232, 240, 0.5);
  font-size: 10px;
  color: #cbd5e1;
  text-align: center;
  max-width: 640px;
  line-height: 1.7;
}

@media (min-width: 768px) {
  .footer-legal {
    margin-left: auto;
    margin-right: auto;
  }
}

@media (max-width: 1024px) {
  .intro-grid,
  .feature-layout,
  .faq-layout {
    grid-template-columns: 1fr;
  }

  .feature-lead {
    position: static;
  }

  .process-grid,
  .footer-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .site-nav {
    height: 66px;
    padding: 0 16px;
  }

  .nav-inner,
  .site-nav-solid .nav-inner {
    height: 66px;
    padding: 0;
  }

  .mobile-dropdown {
    opacity: 0;
    padding: 0;
    border-bottom: 0;
    pointer-events: none;
  }

  .mobile-dropdown-open {
    opacity: 1;
    padding: 8px 16px 16px;
    border-bottom: 1px solid rgba(49, 85, 43, 0.1);
    pointer-events: auto;
  }

  .intro-section,
  .process-section,
  .feature-section,
  .scenario-section,
  .faq-section {
    padding: 70px 0;
  }

  .section-container {
    padding: 0 18px;
  }

  .process-grid,
  .feature-grid,
  .scenario-grid,
  .footer-grid {
    grid-template-columns: 1fr;
  }

  .process-card,
  .feature-card,
  .scenario-card {
    min-height: auto;
  }

  .cta-section {
    padding: 34px 0 70px;
  }

  .cta-panel {
    align-items: flex-start;
    flex-direction: column;
    padding: 28px;
    border-radius: 18px;
  }

  .cta-btn {
    width: 100%;
  }
}

/* ==================== Demo: Stage 2 Additions ==================== */
.demo-profile-grid {
  display: grid;
  grid-template-columns: minmax(0, 4fr) minmax(0, 5fr);
  gap: 12px;
}

.demo-profile-card {
  display: flex;
  flex-direction: column;
}

.demo-profile-form {
  display: flex;
  flex-direction: column;
}

.demo-description-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 4px 0;
}

.demo-desc-item {
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--demo-border);
  padding-bottom: 8px;
  font-size: 11px;
}

.demo-desc-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.demo-desc-label {
  width: 90px;
  color: var(--demo-text-muted);
  font-weight: 500;
  flex-shrink: 0;
}

.demo-desc-value {
  color: var(--demo-text);
  font-weight: 600;
}

.demo-clickable-text {
  cursor: pointer;
  transition: color 0.15s ease;
}
.demo-clickable-text:hover {
  color: var(--demo-primary);
  text-decoration: underline;
}

.demo-mb-card-actions-row {
  display: flex;
  gap: 12px;
  padding: 8px 0 0;
  border-top: 1px dashed var(--demo-border);
  margin-top: auto;
}

.demo-mb-action-btn {
  font-size: 10px;
  color: var(--demo-primary);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: opacity 0.15s ease;
  padding: 2px 4px;
  border-radius: 3px;
}
.demo-mb-action-btn:hover {
  background: var(--demo-accent-bg);
  opacity: 0.9;
}

.demo-dialog-attachment-clickable {
  cursor: pointer;
  transition: all 0.2s ease;
}
.demo-dialog-attachment-clickable:hover {
  border-color: var(--demo-primary) !important;
  background: var(--demo-accent-bg) !important;
  transform: translateY(-2px);
}

.demo-drawer-file-item-clickable {
  cursor: pointer;
  transition: all 0.15s ease;
}
.demo-drawer-file-item-clickable:hover {
  border-color: var(--demo-primary) !important;
  background: var(--demo-accent-bg) !important;
  color: var(--demo-primary) !important;
}

/* Toast Notification (n-message mockup) */
.demo-toast-container {
  position: absolute;
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  pointer-events: none;
}
.demo-toast {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 3px;
  background: var(--demo-card-bg);
  box-shadow:
    0 3px 6px -4px rgba(0, 0, 0, 0.12),
    0 6px 16px 0 rgba(0, 0, 0, 0.08),
    0 9px 28px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--demo-border);
  font-size: 12px;
  pointer-events: auto;
  min-width: 200px;
  box-sizing: border-box;
}
.demo-toast-icon {
  font-size: 14px;
}
.demo-toast-success {
  border-color: rgba(24, 160, 88, 0.15);
}
.demo-toast-success .demo-toast-icon {
  color: #18a058;
}
.demo-toast-error {
  border-color: rgba(208, 48, 80, 0.15);
}
.demo-toast-error .demo-toast-icon {
  color: #d03050;
}
.demo-toast-warning {
  border-color: rgba(240, 160, 32, 0.15);
}
.demo-toast-warning .demo-toast-icon {
  color: #f0a020;
}
.demo-toast-info {
  border-color: rgba(32, 128, 240, 0.15);
}
.demo-toast-info .demo-toast-icon {
  color: #2080f0;
}
.demo-toast-msg {
  color: var(--demo-text);
  font-weight: 500;
}

/* Toast Transition animations */
.demo-toast-fade-enter-active,
.demo-toast-fade-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.demo-toast-fade-enter-from {
  opacity: 0;
  transform: translate(-50%, -20px) !important;
}
.demo-toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px) !important;
}

/* Global Attachment Preview Overlay and Modal Dialog */
.demo-preview-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  backdrop-filter: blur(2px);
}
.demo-preview-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 85%;
  max-width: 540px;
  background: var(--demo-card-bg);
  border: 1px solid var(--demo-border);
  border-radius: 6px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
  z-index: 1010;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.demo-preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--demo-border);
  background: var(--demo-sidebar-bg);
}
.demo-preview-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--demo-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 400px;
}
.demo-preview-close {
  font-size: 14px;
  color: var(--demo-text-muted);
  cursor: pointer;
  padding: 2px;
  border-radius: 4px;
  transition: all 0.15s;
}
.demo-preview-close:hover {
  background: var(--demo-item-hover);
  color: var(--demo-text);
}
.demo-preview-body {
  padding: 20px;
  background: var(--demo-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 260px;
  max-height: 400px;
  overflow-y: auto;
}
.demo-preview-img {
  max-width: 100%;
  max-height: 360px;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--demo-border);
}
.demo-preview-file-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--demo-text-muted);
  font-size: 12px;
}

/* Simulated Cursor styling for autoplay */
.demo-simulated-cursor {
  position: absolute;
  width: 15px;
  height: 22px;
  z-index: 2000;
  pointer-events: none;
  transition:
    left 1.2s cubic-bezier(0.25, 0.8, 0.25, 1),
    top 1.2s cubic-bezier(0.25, 0.8, 0.25, 1);
  transform: translate(-1px, -1px);
}

.cursor-pointer-svg {
  width: 100%;
  height: 100%;
  color: #000000;
  filter: drop-shadow(1px 2px 2px rgba(0, 0, 0, 0.35));
}

.cursor-pointer-svg path {
  stroke: #ffffff;
  stroke-width: 1.5px;
  stroke-linejoin: round;
}

.cursor-click-ripple {
  position: absolute;
  top: -9px;
  left: -9px;
  width: 18px;
  height: 18px;
  border: 2px solid var(--demo-primary);
  border-radius: 50%;
  opacity: 0;
  transform: scale(0.2);
  pointer-events: none;
  box-sizing: border-box;
}

.cursor-clicked .cursor-click-ripple {
  animation: click-ripple-anim 0.4s ease-out;
}

@keyframes click-ripple-anim {
  0% {
    opacity: 0.8;
    transform: scale(0.2);
  }
  100% {
    opacity: 0;
    transform: scale(1.8);
  }
}

/* ==================== High Fidelity UI Enhancements ==================== */

.demo-header-divider {
  width: 1px;
  height: 16px;
  background: var(--demo-border);
  opacity: 0.6;
  margin: 0 12px;
}

.demo-tool-link {
  display: flex;
  align-items: center;
  text-decoration: none;
}

/* Sidebar selected item styling with left border & padding indent */
.demo-sidebar .demo-nav-item,
.demo-sidebar .demo-nav-sub-item {
  position: relative;
}

.demo-sidebar .demo-nav-item.demo-nav-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: var(--demo-primary);
}

.demo-sidebar .demo-nav-sub-item.demo-nav-sub-active {
  background: var(--demo-accent-bg);
  color: var(--demo-primary);
  font-weight: 600;
}

.demo-sidebar .demo-nav-sub-item.demo-nav-sub-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: var(--demo-primary);
}

/* Collapsed sidebar adjustments */
.demo-sidebar-collapsed {
  width: 64px !important;
}

.demo-sidebar-collapsed .demo-sidebar-logo {
  justify-content: center !important;
  padding: 16px 0 12px !important;
}

.demo-sidebar-collapsed .demo-sidebar-logo-text {
  display: none !important;
}

.demo-sidebar-collapsed .demo-nav-item {
  justify-content: center !important;
  padding: 8px 0 !important;
  gap: 0 !important;
}

.demo-sidebar-collapsed .demo-nav-icon {
  font-size: 20px !important;
  width: 20px !important;
  height: 20px !important;
  margin: 0 auto !important;
}

.demo-sidebar-collapsed .demo-nav-arrow,
.demo-sidebar-collapsed .demo-menu-badge,
.demo-sidebar-collapsed .demo-menu-badge-alert {
  display: none !important;
}

/* User avatar dropdown styling */
.demo-dropdown-user-info {
  padding: 8px 12px;
  display: flex;
  flex-direction: column;
  text-align: left;
}

.demo-dropdown-username {
  font-size: 13px;
  font-weight: 600;
  color: var(--demo-text);
}

.demo-dropdown-role {
  font-size: 11px;
  color: var(--demo-text-muted);
  margin-top: 2px;
}

.demo-dropdown-divider {
  height: 1px;
  background: var(--demo-border);
  margin: 4px 0;
}

/* n-statistic statistics style */
.demo-stat-card {
  align-items: flex-start !important;
  text-align: left !important;
  padding: 12px 16px !important;
  gap: 4px !important;
}

.demo-stat-value-container {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
}

.demo-stat-prefix-icon {
  font-size: 18px;
  color: var(--demo-primary);
}

/* Profile header overview card and progress bars */
.demo-profile-header-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  margin-bottom: 12px;
}

.demo-profile-avatar-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.demo-profile-avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: var(--demo-primary);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
}

.demo-profile-user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.demo-profile-name-row {
  display: flex;
  align-items: center;
}

.demo-profile-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--demo-text);
}

.demo-profile-subtext {
  font-size: 12px;
  color: var(--demo-text-muted);
}

.demo-profile-progress-section {
  width: 200px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.demo-profile-progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--demo-text-muted);
}

.demo-profile-progress-bar {
  height: 6px;
  background: var(--demo-border);
  border-radius: 3px;
  overflow: hidden;
}

.demo-profile-progress-fill {
  height: 100%;
  background: var(--demo-primary);
  border-radius: 3px;
  transition: width 0.3s ease;
}

/* Alert warnings and infos */
.demo-alert {
  display: flex;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 6px;
  align-items: flex-start;
  border: 1px solid transparent;
  text-align: left;
}

.demo-alert-warning {
  background: rgba(240, 160, 32, 0.08);
  border-color: rgba(240, 160, 32, 0.2);
  color: #c9750c;
}

.demo-alert-warning .demo-alert-icon {
  color: #f0a020;
}

.demo-alert-info {
  background: rgba(32, 128, 240, 0.08);
  border-color: rgba(32, 128, 240, 0.2);
  color: #1060c0;
}

.demo-alert-info .demo-alert-icon {
  color: #2080f0;
}

.demo-alert-icon {
  font-size: 16px;
  flex-shrink: 0;
  margin-top: 1px;
}

.demo-alert-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.demo-alert-title {
  font-weight: 600;
  font-size: 12px;
  color: var(--demo-text);
}

.demo-alert-desc {
  font-size: 11px;
  color: var(--demo-text-muted);
  line-height: 1.4;
}

/* Descriptions bordered grid table */
.demo-descriptions-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--demo-border);
  border-radius: 4px;
  overflow: hidden;
}

.demo-descriptions-table td {
  padding: 8px 12px;
  border: 1px solid var(--demo-border);
  font-size: 12px;
  text-align: left;
}

.demo-descriptions-table .demo-desc-label {
  background: rgba(0, 0, 0, 0.02);
  color: var(--demo-text-muted);
  font-weight: 500;
  width: 30%;
}

.demo-window.demo-dark-theme .demo-descriptions-table .demo-desc-label {
  background: rgba(255, 255, 255, 0.02);
}

.demo-descriptions-table .demo-desc-value {
  color: var(--demo-text);
}

/* Page switch transition dynamic slide-fade */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Tour bubble tooltip text */
.demo-cursor-tooltip {
  position: absolute;
  left: 20px;
  top: 10px;
  background: #18a058;
  color: #ffffff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  pointer-events: none;
  animation: tooltip-fade-in 0.2s ease-out;
}

@keyframes tooltip-fade-in {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Bottom progress indicator */
.demo-tour-progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: rgba(0, 0, 0, 0.06);
  z-index: 1000;
}

.demo-window.demo-dark-theme .demo-tour-progress-bar {
  background: rgba(255, 255, 255, 0.06);
}

.demo-tour-progress-fill {
  height: 100%;
  background: var(--demo-primary);
  width: 0%;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@media (prefers-reduced-motion: reduce) {
  .landing-page {
    scroll-behavior: auto;
  }

  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
