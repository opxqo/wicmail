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
                <span>🎉 校园邮箱服务已上线</span>
              </div>

              <!-- Logo + 标题 -->
              <div class="hero-title-row">
                <img src="/wic-emblem.svg" alt="WicMail" class="hero-emblem">
                <h1 class="hero-title">WicMail</h1>
              </div>

              <p class="hero-tagline">统一管理你的校园邮箱工作流</p>

              <!-- 间距 -->
              <div class="hero-spacer" />

              <!-- CTA 按钮 -->
              <div class="hero-cta">
                <router-link to="/login" class="hero-btn-primary">
                  <i class="i-fe:mail text-18" />
                  申请校园邮箱
                </router-link>
                <router-link to="/login" class="hero-btn-secondary">
                  进入工作台
                  <i class="i-fe:arrow-right text-16" />
                </router-link>
              </div>
              <p class="hero-platform">支持师生邮箱申请 · 资料审核 · 邮件收发</p>
            </div>

            <!-- 右侧：1:1 复刻真实工作台 -->
            <div class="hero-demo">
              <div class="demo-glow" />
              <div class="demo-window">
                <!-- macOS 标题栏 -->
                <div class="demo-titlebar">
                  <div class="demo-dots">
                    <span class="dot dot-red" />
                    <span class="dot dot-yellow" />
                    <span class="dot dot-green" />
                  </div>
                  <span class="demo-titlebar-text">WicMail - 工作台</span>
                </div>
                <!-- 应用布局：侧边栏 + 内容 -->
                <div class="demo-body">
                  <!-- 侧边栏 -->
                  <div class="demo-sidebar">
                    <div class="demo-sidebar-logo">
                      <img src="/wic-emblem.svg" alt="WicMail" class="demo-sidebar-logo-img">
                      <span class="demo-sidebar-logo-text">WicMail</span>
                    </div>
                    <div class="demo-sidebar-nav">
                      <div
                        v-for="nav in demoNav"
                        :key="nav.id"
                        class="demo-nav-item"
                        :class="{ 'demo-nav-active': demoActiveNav === nav.id }"
                        @click="demoActiveNav = nav.id; demoSelectedEmail = null"
                      >
                        <i :class="nav.icon" class="demo-nav-icon" />
                        <span>{{ nav.label }}</span>
                      </div>
                    </div>
                  </div>

                  <!-- 主内容区 -->
                  <div class="demo-content">
                    <!-- ===== 工作台 ===== -->
                    <template v-if="demoActiveNav === 'dashboard'">
                      <!-- 顶部双卡片 -->
                      <div class="demo-top-row">
                        <div class="demo-card demo-card-user">
                          <div class="demo-user-row">
                            <div class="demo-avatar">张</div>
                            <div class="demo-user-info">
                              <span class="demo-user-name">你好，zhangsan</span>
                              <span class="demo-user-role">普通用户</span>
                            </div>
                          </div>
                          <p class="demo-user-desc">WicMail 校园邮箱，让沟通更简单。</p>
                        </div>
                        <div class="demo-card demo-card-overview">
                          <div class="demo-card-header">
                            <i class="i-fe:layout demo-card-header-icon" />
                            工作台概览
                          </div>
                          <p class="demo-card-text">在这里管理你的校园邮箱、查看邮件和处理申请。</p>
                          <div class="demo-card-actions">
                            <span class="demo-btn demo-btn-ghost" @click="demoActiveNav = 'apply'">申请新邮箱</span>
                            <span class="demo-btn demo-btn-primary" @click="demoActiveNav = 'emails'">查看邮件</span>
                          </div>
                        </div>
                      </div>
                      <!-- 统计卡片 -->
                      <div class="demo-stat-row">
                        <div class="demo-stat-card" v-for="stat in demoStats" :key="stat.label">
                          <i :class="stat.icon" class="demo-stat-icon" />
                          <span class="demo-stat-value">{{ stat.value }}</span>
                          <span class="demo-stat-label">{{ stat.label }}</span>
                        </div>
                      </div>
                      <!-- 底部双栏：邮件表格 + 我的邮箱 -->
                      <div class="demo-bottom-row">
                        <div class="demo-card demo-card-emails">
                          <div class="demo-card-header">
                            <i class="i-fe:inbox demo-card-header-icon" />
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
                                @click="demoActiveNav = 'emails'; demoSelectedEmail = email"
                              >
                                <td class="demo-td-from">{{ email.from }}</td>
                                <td class="demo-td-subject">{{ email.subject }}</td>
                                <td>
                                  <span class="demo-tag" :class="email.isRead ? 'demo-tag-default' : 'demo-tag-info'">
                                    {{ email.isRead ? '已读' : '未读' }}
                                  </span>
                                </td>
                                <td class="demo-td-time">{{ email.fullTime?.slice(0, 16) }}</td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                        <div class="demo-card demo-card-mailbox">
                          <div class="demo-card-header">
                            <i class="i-fe:mail demo-card-header-icon" />
                            我的邮箱
                          </div>
                          <div class="demo-mailbox-list">
                            <div class="demo-mailbox-item" v-for="mb in demoMailboxes" :key="mb.address">
                              <div class="demo-mailbox-info">
                                <span class="demo-mailbox-addr">{{ mb.address }}</span>
                                <span class="demo-mailbox-name">{{ mb.name }}</span>
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
                        <i class="i-fe:plus-circle demo-page-icon" />
                        申请新邮箱
                      </div>
                      <div class="demo-form-card">
                        <div class="demo-form-row">
                          <label>邮箱前缀</label>
                          <div class="demo-input-group">
                            <input class="demo-input" value="zhangsan" readonly>
                            <span class="demo-input-addon">@wic.edu.kg</span>
                          </div>
                        </div>
                        <div class="demo-form-row">
                          <label>显示名称</label>
                          <input class="demo-input" placeholder="可选，如：张三的邮箱" readonly>
                        </div>
                        <div class="demo-form-row">
                          <label>申请理由</label>
                          <textarea class="demo-textarea" placeholder="可选，说明申请原因" readonly />
                        </div>
                        <div class="demo-form-row">
                          <label>证明材料</label>
                          <div class="demo-upload-zone">
                            <i class="i-fe:upload-cloud demo-upload-icon" />
                            <span>点击或拖动图片到此处上传</span>
                            <span class="demo-upload-hint">支持 JPG / PNG，单文件不超过 10MB，最多 5 张</span>
                          </div>
                        </div>
                        <div class="demo-form-row">
                          <label />
                          <span class="demo-btn demo-btn-primary">提交申请</span>
                        </div>
                      </div>
                    </template>

                    <!-- ===== 邮件中心 ===== -->
                    <template v-if="demoActiveNav === 'emails'">
                      <div class="demo-page-header">
                        <i class="i-fe:inbox demo-page-icon" />
                        邮件中心
                      </div>
                      <div v-if="!demoSelectedEmail" class="demo-card">
                        <table class="demo-table demo-table-full">
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
                              v-for="email in demoEmails"
                              :key="email.id"
                              class="demo-table-row"
                              @click="demoSelectedEmail = email"
                            >
                              <td class="demo-td-from">{{ email.from }}</td>
                              <td class="demo-td-subject">{{ email.subject }}</td>
                              <td>
                                <span class="demo-tag" :class="email.isRead ? 'demo-tag-default' : 'demo-tag-info'">
                                  {{ email.isRead ? '已读' : '未读' }}
                                </span>
                              </td>
                              <td class="demo-td-time">{{ email.fullTime?.slice(0, 16) }}</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div v-else class="demo-detail-card">
                        <div class="demo-detail-toolbar" @click="demoSelectedEmail = null">
                          <i class="i-fe:arrow-left" /> 返回列表
                        </div>
                        <div class="demo-detail-title">{{ demoSelectedEmail.subject }}</div>
                        <div class="demo-detail-meta">
                          <div><strong>发件人：</strong>{{ demoSelectedEmail.from }}</div>
                          <div><strong>收件人：</strong>{{ demoSelectedEmail.to }}</div>
                          <div><strong>时间：</strong>{{ demoSelectedEmail.fullTime }}</div>
                        </div>
                        <div class="demo-detail-body">{{ demoSelectedEmail.body }}</div>
                      </div>
                    </template>

                    <!-- ===== 管理后台 ===== -->
                    <template v-if="demoActiveNav === 'admin'">
                      <div class="demo-page-header">
                        <i class="i-fe:check-square demo-page-icon" />
                        申请审核
                      </div>
                      <div class="demo-card">
                        <table class="demo-table demo-table-full">
                          <thead>
                            <tr>
                              <th>申请人</th>
                              <th>申请地址</th>
                              <th>状态</th>
                              <th>操作</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="app in demoApplications" :key="app.id" class="demo-table-row">
                              <td>{{ app.user }}</td>
                              <td>{{ app.email }}</td>
                              <td>
                                <span class="demo-tag" :class="{
                                  'demo-tag-warning': app.status === 'pending',
                                  'demo-tag-success': app.status === 'approved',
                                  'demo-tag-error': app.status === 'rejected',
                                }">{{ app.statusText }}</span>
                              </td>
                              <td>
                                <div v-if="app.status === 'pending'" class="demo-action-group">
                                  <span class="demo-action-btn demo-action-approve" @click="app.status = 'approved'; app.statusText = '已批准'">批准</span>
                                  <span class="demo-action-btn demo-action-reject" @click="app.status = 'rejected'; app.statusText = '已拒绝'">拒绝</span>
                                </div>
                                <span v-else class="demo-action-disabled">已处理</span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="intro" class="intro-section">
        <div class="section-container intro-grid">
          <div class="intro-copy">
            <p class="section-kicker">SERVICE OVERVIEW</p>
            <h2>把校园邮箱申请流程收进一个可靠入口</h2>
            <p>
              WicMail 服务于武汉城市学院相关邮箱场景，围绕身份资料、邮箱申请、审核管理和邮件查看组织功能。首页承担官网说明与入口分流，真正的操作在用户工作台完成。
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
            <p class="section-kicker">APPLICATION FLOW</p>
            <h2>四步完成邮箱申请</h2>
            <p>流程保持轻量，但每一步都围绕真实身份与可审核材料设计。</p>
          </div>

          <div class="process-grid">
            <article v-for="(item, index) in processSteps" :key="item.title" class="process-card">
              <div class="step-index">{{ String(index + 1).padStart(2, '0') }}</div>
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
            <p class="section-kicker">CAPABILITIES</p>
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
            <p class="section-kicker">USE CASES</p>
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
            <p class="section-kicker">FAQ</p>
            <h2>申请前可以先了解这些</h2>
            <p class="faq-lead">首页只做说明和入口，具体审核状态、邮箱列表和邮件内容请登录工作台查看。</p>
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
            <p class="section-kicker light">READY</p>
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
            <p class="footer-desc">为武汉城市学院师生提供专业、安全的校园邮箱申请与管理服务，覆盖邮箱申请、审核管理、邮件收发全流程。</p>
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
              <i class="i-fe:chevron-down text-16 footer-chevron" :class="{ 'footer-chevron-open': footerOpen[0] }" />
            </button>
            <div class="footer-col-body" :class="{ 'footer-col-open': footerOpen[0] }">
              <router-link to="/login" class="footer-link">
                <i class="i-fe:log-in text-14 footer-link-icon" /> 登录工作台
              </router-link>
              <router-link to="/login" class="footer-link">
                <i class="i-fe:plus-circle text-14 footer-link-icon" /> 申请邮箱
              </router-link>
              <router-link to="/login" class="footer-link">
                <i class="i-fe:inbox text-14 footer-link-icon" /> 邮件中心
              </router-link>
              <a href="https://www.wic.edu.kg" target="_blank" rel="noopener noreferrer" class="footer-link">
                <i class="i-fe:external-link text-14 footer-link-icon" /> 学校官网
                <i class="i-fe:external-link text-10 footer-ext-icon" />
              </a>
            </div>
          </div>

          <!-- 列3: 页面导航 -->
          <div class="footer-col">
            <button class="footer-col-toggle" @click="footerOpen[1] = !footerOpen[1]">
              <h3>页面导航</h3>
              <i class="i-fe:chevron-down text-16 footer-chevron" :class="{ 'footer-chevron-open': footerOpen[1] }" />
            </button>
            <div class="footer-col-body" :class="{ 'footer-col-open': footerOpen[1] }">
              <a href="#intro" class="footer-link" @click.prevent="scrollToSection('intro')">
                <i class="i-fe:info text-14 footer-link-icon" /> 服务介绍
              </a>
              <a href="#process" class="footer-link" @click.prevent="scrollToSection('process')">
                <i class="i-fe:list text-14 footer-link-icon" /> 申请流程
              </a>
              <a href="#features" class="footer-link" @click.prevent="scrollToSection('features')">
                <i class="i-fe:shield text-14 footer-link-icon" /> 核心能力
              </a>
              <a href="#faq" class="footer-link" @click.prevent="scrollToSection('faq')">
                <i class="i-fe:help-circle text-14 footer-link-icon" /> 常见问题
              </a>
            </div>
          </div>

          <!-- 列4: 联系我们 -->
          <div class="footer-col">
            <button class="footer-col-toggle" @click="footerOpen[2] = !footerOpen[2]">
              <h3>联系我们</h3>
              <i class="i-fe:chevron-down text-16 footer-chevron" :class="{ 'footer-chevron-open': footerOpen[2] }" />
            </button>
            <div class="footer-col-body" :class="{ 'footer-col-open': footerOpen[2] }">
              <div class="footer-contact-item">
                <i class="i-fe:map-pin text-18 footer-contact-icon" />
                <span>湖北省武汉市洪山区黄家湖大学城</span>
              </div>
              <div class="footer-contact-item">
                <i class="i-fe:phone text-18 footer-contact-icon" />
                <span>027-86490575</span>
              </div>
              <div class="footer-contact-item">
                <i class="i-fe:mail text-18 footer-contact-icon" />
                <a href="mailto:admin@wic.edu.kg" class="footer-contact-link">admin@wic.edu.kg</a>
              </div>
            </div>
          </div>
        </div>

        <!-- 底栏 -->
        <div class="footer-bottom">
          <div class="footer-bottom-inner">
            <p class="footer-copy">© {{ currentYear }} WicMail · Wuhan City University. All rights reserved.</p>
            <img src="/校训.svg" alt="励志修德 勤学创新" class="footer-motto">
            <div class="footer-credit">
              <span>Designed & Built by</span>
              <strong>OPXQO LT</strong>
              <i class="i-fe:heart text-10 text-red-400 fill-current" />
            </div>
          </div>
          <p class="footer-legal">
            WicMail 为武汉城市学院校园邮箱服务平台，仅供校内师生使用。如有问题请联系管理员。
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
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
  { question: '首页可以直接收发邮件吗？', answer: '首页只提供介绍和入口。邮箱申请、邮件查看和管理功能需要进入登录后的工作台。' },
  { question: '邮箱申请一定会通过吗？', answer: '申请需要根据资料和规则进行审核，提交后请在工作台查看审核状态。' },
  { question: '忘记账号或遇到申请问题怎么办？', answer: '可以通过页脚邮箱联系管理员，或等待后续帮助中心功能接入。' },
]

// ===== 右侧工作台模拟数据 =====
const demoActiveNav = ref('dashboard')
const demoSelectedEmail = ref(null)

const demoNav = computed(() => [
  { id: 'dashboard', label: '工作台', icon: 'i-fe:home', badge: null },
  { id: 'apply', label: '申请邮箱', icon: 'i-fe:plus-circle', badge: null },
  { id: 'emails', label: '邮件中心', icon: 'i-fe:inbox', badge: '3' },
  { id: 'admin', label: '管理后台', icon: 'i-fe:settings', badge: null },
])

const demoStats = [
  { value: 2, label: '我的邮箱', icon: 'i-fe:mail' },
  { value: 6, label: '总邮件数', icon: 'i-fe:inbox' },
  { value: 3, label: '未读邮件', icon: 'i-fe:bell' },
  { value: 1, label: '待审申请', icon: 'i-fe:clock' },
]

const demoMailboxes = [
  { address: 'zhangsan@wic.edu.kg', name: '张三的邮箱' },
  { address: 'lab@wic.edu.kg', name: '实验室公共邮箱' },
]

const demoEmails = reactive([
  { id: 1, from: 'noreply@wic.edu.kg', to: 'zhangsan@wic.edu.kg', subject: '欢迎使用 WicMail 校园邮箱服务', time: '09:00', fullTime: '2024-09-01 09:00:01', isRead: true, body: '欢迎使用 WicMail 校园邮箱服务！您的邮箱 zhangsan@wic.edu.kg 已成功开通。您可以开始收发邮件了！如有问题请联系管理员。' },
  { id: 2, from: 'system@wic.edu.kg', to: 'zhangsan@wic.edu.kg', subject: '【系统通知】邮箱服务维护公告', time: '10:00', fullTime: '2024-09-25 10:00:02', isRead: false, body: '尊敬的用户：系统将于本周六凌晨 2:00-4:00 进行例行维护，届时邮件服务将短暂中断。给您带来的不便，敬请谅解。' },
  { id: 3, from: 'wangwu@gmail.com', to: 'zhangsan@wic.edu.kg', subject: 'Re: 课程项目讨论', time: '14:30', fullTime: '2024-09-24 14:30:05', isRead: false, body: '张三你好，关于课程项目的分工我已经整理了一份文档。主要内容包括：1. 前端模块 - 由你负责 2. 后端模块 - 由我负责 3. 测试与部署 - 共同完成。请在周五前确认你的部分，谢谢！' },
  { id: 4, from: 'noreply@github.com', to: 'zhangsan@wic.edu.kg', subject: 'GitHub: Your personal access token will expire in 7 days', time: '08:00', fullTime: '2024-09-23 08:00:03', isRead: true, body: 'Your personal access token "WicMail CI" will expire on October 1, 2024. Please regenerate your token to continue using GitHub API access.' },
  { id: 5, from: 'professor.liu@wic.edu.kg', to: 'lab@wic.edu.kg', subject: '实验室周报 - 第38周', time: '09:15', fullTime: '2024-09-22 09:15:02', isRead: false, body: '各位同学好，请在本周五前提交第38周的实验报告，报告格式请参考上周的模板。本周重点：完成模型训练实验、整理实验数据、撰写实验分析。' },
  { id: 6, from: 'noreply@wic.edu.kg', to: 'zhangsan@wic.edu.kg', subject: '新的邮箱申请待审核', time: '08:30', fullTime: '2024-09-20 08:30:03', isRead: true, body: '您提交的邮箱申请 lab@wic.edu.kg 已进入审核流程，请耐心等待管理员审批。您可以在工作台中随时查看审核进度。' },
])

const demoApplications = reactive([
  { id: 1, user: 'admin', email: 'admin@wic.edu.kg', status: 'approved', statusText: '已批准' },
  { id: 2, user: 'zhangsan', email: 'zhangsan@wic.edu.kg', status: 'approved', statusText: '已批准' },
  { id: 3, user: 'zhangsan', email: 'lab@wic.edu.kg', status: 'approved', statusText: '已批准' },
  { id: 4, user: 'lisi', email: 'lisi@wic.edu.kg', status: 'pending', statusText: '待审核' },
  { id: 5, user: 'lisi', email: 'test123@wic.edu.kg', status: 'rejected', statusText: '已拒绝' },
])

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

onMounted(() => {
  handleScroll()
  pageRef.value?.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  pageRef.value?.removeEventListener('scroll', handleScroll)
  window.removeEventListener('scroll', handleScroll)
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
  transition: background-color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease, backdrop-filter 0.3s ease;
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
  .nav-inner { height: 72px; }
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
  .nav-logo-img { width: 40px; height: 40px; }
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
  .nav-links { display: flex; }
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
  .nav-right { display: flex; }
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
  transition: background-color 0.2s ease, color 0.2s ease;
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
  background: var(--wic-primary, #3F632F);
  transition: background-color 0.2s ease, transform 0.15s ease;
}

.nav-cta-btn:hover {
  background: var(--wic-secondary, #5C8D44);
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
  .mobile-menu-btn { display: none; }
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
  transition: max-height 0.3s ease, padding 0.3s ease;
  padding: 0 16px;
}

.mobile-dropdown-open {
  max-height: 400px;
  padding: 8px 16px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

@media (min-width: 768px) {
  .mobile-dropdown { display: none; }
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
  color: var(--wic-primary, #3F632F);
}

.mobile-cta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
  padding: 12px;
  border-radius: 8px;
  background: var(--wic-primary, #3F632F);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.mobile-cta:hover {
  background: var(--wic-secondary, #5C8D44);
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
    linear-gradient(rgba(0,0,0,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.03) 1px, transparent 1px);
  background-size: 48px 48px;
}

@media (prefers-color-scheme: dark) {
  .hero-grid-pattern { opacity: 0.06; }
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
  .hero-container { padding: 24px clamp(16px, 4vw, 48px); }
}

@media (min-width: 768px) {
  .hero-container { padding: 48px clamp(16px, 4vw, 48px); }
}

.hero-grid {
  display: grid;
  gap: 24px;
  align-items: center;
}

@media (min-width: 1024px) {
  .hero-grid {
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
}

@media (min-width: 1280px) {
  .hero-grid {
    grid-template-columns: 5fr 7fr;
    gap: 16px;
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
  .hero-title-row { justify-content: flex-start; }
}

@media (min-width: 640px) {
  .hero-title-row { gap: 20px; margin-bottom: 32px; }
}

.hero-emblem {
  width: 44px;
  height: 44px;
  object-fit: contain;
  flex-shrink: 0;
}

@media (min-width: 640px) {
  .hero-emblem { width: 48px; height: 48px; }
}

@media (min-width: 768px) {
  .hero-emblem { width: 56px; height: 56px; }
}

@media (min-width: 1024px) {
  .hero-emblem { width: 64px; height: 64px; }
}

.hero-title {
  font-size: 30px;
  font-weight: 700;
  color: #1e293b;
  white-space: nowrap;
  margin: 0;
}

@media (min-width: 640px) {
  .hero-title { font-size: 36px; }
}

@media (min-width: 768px) {
  .hero-title { font-size: 36px; }
}

@media (min-width: 1024px) {
  .hero-title { font-size: 48px; }
}

@media (min-width: 1280px) {
  .hero-title { font-size: 60px; }
}

.hero-tagline {
  font-size: 16px;
  font-weight: 500;
  color: #64748b;
  margin: 0;
}

@media (min-width: 640px) {
  .hero-tagline { font-size: 18px; }
}

@media (min-width: 768px) {
  .hero-tagline { font-size: 20px; }
}

@media (min-width: 1024px) {
  .hero-tagline { font-size: 24px; }
}

@media (min-width: 1280px) {
  .hero-tagline { font-size: 30px; }
}

.hero-spacer {
  height: 56px;
}

@media (min-width: 640px) {
  .hero-spacer { height: 80px; }
}

@media (min-width: 768px) {
  .hero-spacer { height: 128px; }
}

@media (min-width: 1024px) {
  .hero-spacer { height: 176px; }
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
  padding: 20px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  color: #fff;
  background: var(--wic-primary, #3F632F);
  box-shadow: 0 8px 24px rgba(63, 99, 47, 0.2);
  transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
  width: 100%;
}

@media (min-width: 640px) {
  .hero-btn-primary {
    width: auto;
    padding: 24px 40px;
    font-size: 18px;
  }
}

@media (min-width: 768px) {
  .hero-btn-primary {
    padding: 28px 48px;
    font-size: 20px;
  }
}

.hero-btn-primary:hover {
  background: var(--wic-secondary, #5C8D44);
  transform: scale(1.03);
  box-shadow: 0 12px 32px rgba(63, 99, 47, 0.28);
}

.hero-btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 20px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  color: #1e293b;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(8px);
  transition: background-color 0.2s ease, border-color 0.2s ease;
  width: 100%;
}

@media (min-width: 640px) {
  .hero-btn-secondary {
    width: auto;
    padding: 24px 40px;
    font-size: 18px;
  }
}

@media (min-width: 768px) {
  .hero-btn-secondary {
    padding: 28px 48px;
    font-size: 20px;
  }
}

.hero-btn-secondary:hover {
  background: rgba(0, 0, 0, 0.03);
  border-color: rgba(0, 0, 0, 0.15);
}

.hero-platform {
  margin-top: 16px;
  font-size: 13px;
  color: #94a3b8;
  text-align: center;
}

@media (min-width: 1024px) {
  .hero-platform { text-align: left; }
}

/* Hero Demo (Right - Product Mockup) */
.hero-demo {
  display: none;
  justify-content: flex-end;
  position: relative;
}

@media (min-width: 1024px) {
  .hero-demo { display: flex; }
}

/* ==================== Demo: macOS Window ==================== */
.demo-glow {
  position: absolute;
  inset: -40px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(63, 99, 47, 0.12), rgba(128, 90, 213, 0.08));
  filter: blur(48px);
  pointer-events: none;
}

.demo-window {
  position: relative;
  height: 468px;
  width: 100%;
  max-width: 720px;
  overflow: hidden;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
  background: #fff;
}

@media (min-width: 1280px) {
  .demo-window { height: 546px; max-width: 840px; }
}

@media (min-width: 1536px) {
  .demo-window { height: 598px; max-width: 920px; }
}

.demo-titlebar {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 38px;
  padding: 0 12px;
  border-bottom: 1px solid #efeff5;
  background: #fafafc;
  flex-shrink: 0;
}

.demo-dots { display: flex; gap: 7px; }
.dot { width: 12px; height: 12px; border-radius: 50%; }
.dot-red { background: #ff5f57; }
.dot-yellow { background: #febc2e; }
.dot-green { background: #28c840; }

.demo-titlebar-text {
  flex: 1;
  text-align: center;
  font-size: 12px;
  color: #999;
  margin-right: 44px;
}

/* ==================== Demo: Layout ==================== */
.demo-body {
  display: flex;
  flex: 1;
  overflow: hidden;
  background: #f2f3f5;
}

/* Sidebar */
.demo-sidebar {
  width: 200px;
  background: #fff;
  border-right: 1px solid #efeff5;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  padding: 0;
}

.demo-sidebar-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 16px 12px;
  border-bottom: 1px solid #efeff5;
}

.demo-sidebar-logo-img {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.demo-sidebar-logo-text {
  font-size: 15px;
  font-weight: 700;
  color: #333639;
}

.demo-sidebar-nav {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.demo-nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.demo-nav-item:hover {
  background: #f2f3f5;
  color: #333639;
}

.demo-nav-active {
  background: rgba(63, 99, 47, 0.08);
  color: var(--wic-primary, #3F632F);
  font-weight: 600;
}

.demo-nav-active:hover {
  background: rgba(63, 99, 47, 0.12);
  color: var(--wic-primary, #3F632F);
}

.demo-nav-icon {
  font-size: 16px;
  width: 16px;
  height: 16px;
}

/* ==================== Demo: Content Area ==================== */
.demo-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Page header */
.demo-page-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #333639;
  margin-bottom: 4px;
}

.demo-page-icon {
  font-size: 18px;
  color: var(--wic-primary, #3F632F);
}

/* ==================== Demo: Cards (Naive UI style) ==================== */
.demo-card {
  background: #fff;
  border-radius: 4px;
  border: 1px solid #efeff5;
  padding: 16px;
}

.demo-card-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #333639;
  padding-bottom: 12px;
  border-bottom: 1px solid #efeff5;
  margin-bottom: 12px;
}

.demo-card-header-icon {
  font-size: 16px;
  color: var(--wic-primary, #3F632F);
}

.demo-card-text {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  margin: 0 0 12px;
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
  padding: 5px 14px;
  border-radius: 3px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.demo-btn-primary {
  background: var(--wic-primary, #3F632F);
  color: #fff;
  border-color: var(--wic-primary, #3F632F);
}

.demo-btn-primary:hover {
  background: var(--wic-secondary, #5C8D44);
  border-color: var(--wic-secondary, #5C8D44);
}

.demo-btn-ghost {
  background: transparent;
  color: var(--wic-primary, #3F632F);
  border-color: var(--wic-primary, #3F632F);
}

.demo-btn-ghost:hover {
  background: rgba(63, 99, 47, 0.06);
}

/* ==================== Demo: Top Row (User + Overview) ==================== */
.demo-top-row {
  display: flex;
  gap: 12px;
}

.demo-card-user {
  width: 35%;
  flex-shrink: 0;
}

.demo-card-overview {
  flex: 1;
}

.demo-user-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.demo-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--wic-primary, #3F632F);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  flex-shrink: 0;
}

.demo-user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.demo-user-name {
  font-size: 15px;
  color: #333639;
  opacity: 0.8;
}

.demo-user-role {
  font-size: 12px;
  color: #999;
}

.demo-user-desc {
  margin: 16px 0 0;
  font-size: 13px;
  color: #999;
  line-height: 1.6;
}

/* ==================== Demo: Stat Cards ==================== */
.demo-stat-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.demo-stat-card {
  background: #fff;
  border-radius: 4px;
  border: 1px solid #efeff5;
  padding: 14px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.demo-stat-icon {
  font-size: 16px;
  color: var(--wic-primary, #3F632F);
  margin-bottom: 4px;
}

.demo-stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #333639;
  line-height: 1.2;
}

.demo-stat-label {
  font-size: 12px;
  color: #999;
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

/* Mailbox list */
.demo-mailbox-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.demo-mailbox-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: #f7f8fa;
  border-radius: 4px;
}

.demo-mailbox-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.demo-mailbox-addr {
  font-size: 13px;
  font-weight: 600;
  color: #333639;
}

.demo-mailbox-name {
  font-size: 11px;
  color: #999;
}

/* ==================== Demo: Table (Naive UI style) ==================== */
.demo-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.demo-table th {
  text-align: left;
  padding: 8px 10px;
  font-weight: 600;
  color: #333639;
  font-size: 12px;
  border-bottom: 1px solid #efeff5;
  white-space: nowrap;
}

.demo-table td {
  padding: 8px 10px;
  color: #666;
  border-bottom: 1px solid #f2f3f5;
}

.demo-table-full {
  flex: 1;
}

.demo-table-row {
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.demo-table-row:hover {
  background: #f7f8fa;
}

.demo-td-from {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 120px;
  font-weight: 500;
  color: #333639;
}

.demo-td-subject {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.demo-td-time {
  white-space: nowrap;
  color: #999;
  font-size: 11px;
}

/* ==================== Demo: Tags (Naive UI style) ==================== */
.demo-tag {
  display: inline-flex;
  align-items: center;
  padding: 1px 8px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 500;
  white-space: nowrap;
}

.demo-tag-default {
  background: #f2f3f5;
  color: #666;
  border: 1px solid #e0e0e6;
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

/* ==================== Demo: Form (Naive UI style) ==================== */
.demo-form-card {
  background: #fff;
  border-radius: 4px;
  border: 1px solid #efeff5;
  padding: 20px;
}

.demo-form-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.demo-form-row:last-child {
  margin-bottom: 0;
}

.demo-form-row label {
  width: 80px;
  font-size: 13px;
  color: #333639;
  padding-top: 6px;
  text-align: right;
  flex-shrink: 0;
}

.demo-input {
  flex: 1;
  padding: 5px 12px;
  border: 1px solid #e0e0e6;
  border-radius: 3px;
  font-size: 13px;
  color: #333;
  background: #fff;
  outline: none;
  transition: border-color 0.2s ease;
}

.demo-input:focus {
  border-color: var(--wic-primary, #3F632F);
}

.demo-input::placeholder {
  color: #c2c6cc;
}

.demo-input-group {
  flex: 1;
  display: flex;
}

.demo-input-group .demo-input {
  border-radius: 3px 0 0 3px;
  border-right: none;
}

.demo-input-addon {
  display: flex;
  align-items: center;
  padding: 5px 12px;
  background: #f7f8fa;
  border: 1px solid #e0e0e6;
  border-radius: 0 3px 3px 0;
  font-size: 13px;
  color: #999;
}

.demo-textarea {
  flex: 1;
  padding: 5px 12px;
  border: 1px solid #e0e0e6;
  border-radius: 3px;
  font-size: 13px;
  color: #333;
  background: #fff;
  resize: none;
  height: 60px;
  outline: none;
  font-family: inherit;
}

.demo-upload-zone {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 20px;
  border: 1.5px dashed #e0e0e6;
  border-radius: 4px;
  color: #999;
  font-size: 12px;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.demo-upload-zone:hover {
  border-color: var(--wic-primary, #3F632F);
}

.demo-upload-icon {
  font-size: 24px;
  color: #c2c6cc;
}

.demo-upload-hint {
  font-size: 11px;
  color: #c2c6cc;
}

/* ==================== Demo: Email Detail ==================== */
.demo-detail-card {
  background: #fff;
  border-radius: 4px;
  border: 1px solid #efeff5;
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.demo-detail-toolbar {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--wic-primary, #3F632F);
  cursor: pointer;
  margin-bottom: 12px;
}

.demo-detail-toolbar:hover {
  opacity: 0.8;
}

.demo-detail-title {
  font-size: 16px;
  font-weight: 600;
  color: #333639;
  margin-bottom: 12px;
}

.demo-detail-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: #666;
  padding-bottom: 12px;
  border-bottom: 1px solid #efeff5;
  margin-bottom: 12px;
}

.demo-detail-meta strong {
  color: #333639;
}

.demo-detail-body {
  font-size: 13px;
  color: #333639;
  line-height: 1.8;
}

/* ==================== Demo: Admin Actions ==================== */
.demo-action-group {
  display: flex;
  gap: 8px;
}

.demo-action-btn {
  font-size: 12px;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
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
  font-size: 12px;
  color: #c2c6cc;
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
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.78)),
    var(--surface);
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
  border-top: 4px solid var(--wic-primary, #3F632F);
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
  background: var(--wic-primary, #3F632F);
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
  transition: max-height 0.35s cubic-bezier(0.4, 0, 0.2, 1), padding-bottom 0.35s ease;
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
  color: var(--wic-primary, #3F632F);
}

.footer-link-icon {
  color: #94a3b8;
  flex-shrink: 0;
  transition: color 0.2s ease;
}

.footer-link:hover .footer-link-icon {
  color: var(--wic-primary, #3F632F);
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
  color: var(--wic-primary, #3F632F);
  flex-shrink: 0;
  margin-top: 2px;
}

.footer-contact-link {
  color: #64748b;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-contact-link:hover {
  color: var(--wic-primary, #3F632F);
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

@keyframes scrollBounce {
  0%,
  100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  50% {
    transform: translateY(4px);
    opacity: 1;
  }
}

@media (max-width: 1024px) {
  .desktop-nav {
    display: none;
  }

  .hero-content {
    grid-template-columns: minmax(0, 1fr) minmax(300px, 360px);
    gap: 34px;
  }

  .hero-console {
    min-height: 380px;
    padding: 20px;
    border-radius: 24px;
  }

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

  .brand-emblem {
    width: 36px;
    height: 36px;
  }

  .brand-title {
    font-size: 16px;
  }

  .brand-subtitle,
  .nav-ghost {
    display: none;
  }

  .nav-primary {
    min-height: 38px;
    padding: 0 14px;
    font-size: 13px;
  }

  .hero-section {
    min-height: 100dvh;
    align-items: flex-end;
    padding: 96px 18px 34px;
  }

  .hero-overlay {
    background:
      linear-gradient(180deg, rgba(5, 12, 5, 0.32), rgba(5, 12, 5, 0.9)),
      radial-gradient(circle at 18% 78%, rgba(158, 231, 168, 0.22), transparent 32%);
  }

  .hero-title {
    margin-top: 22px;
  }

  .hero-content {
    display: block;
  }

  .hero-copy {
    max-width: none;
  }

  .hero-title span {
    font-size: 52px;
    letter-spacing: -0.02em;
  }

  .hero-title small {
    font-size: 25px;
  }

  .hero-desc {
    font-size: 15px;
    line-height: 1.78;
  }

  .hero-actions {
    display: none;
  }

  .hero-console {
    display: none;
  }

  .mobile-quick-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
    margin-top: 26px;
  }

  .quick-item {
    min-width: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
  }

  .quick-icon {
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(12px);
  }

  .scroll-cue {
    display: none;
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
