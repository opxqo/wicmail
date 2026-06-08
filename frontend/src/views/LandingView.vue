<template>
  <div id="top" :class="['landing-page', { 'menu-open': isMenuOpen }]">
    <a class="skip-link" href="#main">跳到主要内容</a>

    <header class="site-header" aria-label="WicMail 顶部导航">
      <div class="header-inner">
        <router-link class="brand" to="/" aria-label="WicMail 首页">
          <span class="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path
                d="M4 6.5L7.35 17.5L11.95 8.5L16.65 17.5L20 6.5"
                stroke="currentColor"
                stroke-width="2.3"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </span>
          <span>WicMail</span>
        </router-link>

        <nav class="nav" aria-label="主导航">
          <a href="#apply" @click="closeMenu">申请流程</a>
          <a href="#features" @click="closeMenu">平台能力</a>
          <a href="#data" @click="closeMenu">服务数据</a>
          <a href="#start" @click="closeMenu">开始使用</a>
        </nav>

        <div class="header-actions">
          <router-link class="button secondary" to="/login">登录</router-link>
          <router-link class="button primary" to="/register">申请邮箱</router-link>
        </div>

        <button
          class="mobile-toggle"
          type="button"
          :aria-label="isMenuOpen ? '关闭导航菜单' : '打开导航菜单'"
          :aria-expanded="String(isMenuOpen)"
          @click="isMenuOpen = !isMenuOpen"
        >
          <el-icon><Close v-if="isMenuOpen" /><Menu v-else /></el-icon>
        </button>
      </div>
    </header>

    <main id="main">
      <section class="hero">
        <div class="hero-inner">
          <div class="hero-copy">
            <div class="eyebrow">
              <el-icon><Lock /></el-icon>
              为校园身份打造的私人邮局
            </div>
            <h1>一个更轻、更快的校园邮箱入口</h1>
            <p class="hero-lead">
              把邮箱申请、审核通知、进度查询和邮件管理收进一个干净界面。WicMail
              让学生、教师与校内组织都能清晰完成邮箱开通。
            </p>
            <div class="hero-actions">
              <router-link class="button primary" to="/register">
                立即申请邮箱
                <el-icon><Right /></el-icon>
              </router-link>
              <a class="button secondary" href="#features">了解开通条件</a>
            </div>
            <div class="trust-row" aria-label="平台特点">
              <span class="trust-pill"><el-icon><Check /></el-icon>申请进度透明</span>
              <span class="trust-pill"><el-icon><TrendCharts /></el-icon>邮箱状态可追踪</span>
              <span class="trust-pill"><el-icon><Lock /></el-icon>角色权限安全</span>
            </div>
          </div>

          <div class="hero-visual" aria-label="WicMail 邮箱界面预览">
            <div class="mail-shell">
              <div class="mail-topbar">
                <div class="window-dots" aria-hidden="true"><span></span><span></span><span></span></div>
                <div class="mail-domain">mail.wic.edu</div>
              </div>
              <div class="mail-body">
                <div class="mail-heading">
                  <h2>收件箱预览</h2>
                  <span class="status-badge">审核中</span>
                </div>
                <div class="inbox-list">
                  <article v-for="item in inboxPreview" :key="item.title" class="inbox-item">
                    <div class="inbox-icon" aria-hidden="true">
                      <el-icon><component :is="item.icon" /></el-icon>
                    </div>
                    <div class="inbox-copy">
                      <strong>{{ item.title }}</strong>
                      <span>{{ item.text }}</span>
                    </div>
                    <span class="inbox-time">{{ item.time }}</span>
                  </article>
                </div>
              </div>
            </div>

            <div class="hero-card progress-card" aria-hidden="true">
              <strong>申请进度 75%</strong>
              <div class="progress-line"><span></span><span></span><span></span><span></span></div>
            </div>

            <div class="hero-card capacity-card" aria-hidden="true">
              <strong>邮箱容量</strong>
              <div class="capacity-ring">72%</div>
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="apply">
        <div class="section-header">
          <p class="section-kicker">APPLY FLOW</p>
          <h2 class="section-title">四步完成校园邮箱开通</h2>
          <p class="section-text">首页优先呈现用户最关心的路径：怎么申请、审核到哪一步、通过后在哪里查看邮箱。</p>
        </div>
        <div class="process-grid">
          <article v-for="step in steps" :key="step.title" class="process-card">
            <div class="step-number">{{ step.index }}</div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.text }}</p>
          </article>
        </div>
      </section>

      <section class="feature-band" id="features">
        <div class="section feature-layout">
          <div class="feature-panel">
            <h2>年轻化界面，系统级能力</h2>
            <p>WicMail 首页不是传统公告站，而是一个清爽的平台入口。用户看到的是下一步操作，管理员看到的是可处理的申请队列。</p>
            <div class="feature-metrics">
              <div class="metric-mini"><strong>2 端</strong><span>用户端与管理端</span></div>
              <div class="metric-mini"><strong>4 步</strong><span>完整申请闭环</span></div>
            </div>
          </div>

          <div class="features-grid">
            <article v-for="feature in features" :key="feature.title" class="feature-card">
              <div class="feature-icon" aria-hidden="true">
                <el-icon><component :is="feature.icon" /></el-icon>
              </div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.text }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section" id="data">
        <div class="section-header">
          <p class="section-kicker">SERVICE DATA</p>
          <h2 class="section-title">关键数据一眼可见</h2>
          <p class="section-text">用少量数字建立平台可信度，同时避免传统官网堆内容的问题。</p>
        </div>
        <div class="metric-grid">
          <article class="metric-card"><strong>24h</strong><span>邮件接收服务持续在线，重要通知及时触达。</span></article>
          <article class="metric-card"><strong>1 天</strong><span>常规申请预计一个工作日内完成初审。</span></article>
          <article class="metric-card"><strong>100%</strong><span>申请状态、审核结果和邮箱信息在平台内可追踪。</span></article>
        </div>
      </section>

      <section class="section cta-section" id="start">
        <div class="cta-panel">
          <div class="cta-content">
            <h2>准备好开通你的校园邮箱了吗？</h2>
            <p>从首页进入申请流程，提交资料后即可在进度页查看审核状态。管理员通过后，邮箱信息会出现在你的用户中心。</p>
            <div class="cta-actions">
              <router-link class="button primary" to="/register">开始申请</router-link>
              <router-link class="button secondary" to="/login">进入控制台</router-link>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <div class="footer-inner">
        <div>© 2026 WicMail 校园邮箱申请平台</div>
        <div class="footer-links">
          <a href="#apply">申请流程</a>
          <a href="#features">平台能力</a>
          <a href="#start">开始使用</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isMenuOpen = ref(false)

function closeMenu() {
  isMenuOpen.value = false
}

const inboxPreview = [
  { title: '邮箱申请已进入审核', text: '你的材料已提交至管理员队列', time: '新', icon: 'Message' },
  { title: '校园账号绑定提醒', text: '请确认学号与实名信息一致', time: '10:24', icon: 'CircleCheck' },
  { title: '欢迎使用 WicMail', text: '开通后可在用户中心管理邮箱容量', time: '昨天', icon: 'Document' },
]

const steps = [
  { index: 1, title: '注册账号', text: '使用校内身份信息创建账户，为后续申请和邮箱管理建立专属入口。' },
  { index: 2, title: '提交申请', text: '选择学生、教师或组织身份，填写邮箱前缀、用途说明和联系方式。' },
  { index: 3, title: '审核材料', text: '管理员在线查看申请材料，审核结果会同步到进度查询和站内通知。' },
  { index: 4, title: '开通邮箱', text: '申请通过后进入用户中心查看邮箱地址、容量状态和近期邮件。' },
]

const features = [
  { title: '统一申请入口', text: '把注册、申请、材料上传和进度查询放在同一套流程里，降低用户找入口的成本。', icon: 'Menu' },
  { title: '进度实时反馈', text: '每个申请节点都有明确状态，减少重复询问，也方便用户判断是否需要补充材料。', icon: 'Timer' },
  { title: '权限安全清晰', text: '用户只能查看自己的邮箱和邮件，管理员负责审核、用户管理和邮箱状态维护。', icon: 'Lock' },
  { title: '邮件管理延展', text: '首页视觉已经预留邮箱、容量、未读邮件等系统信息，为后续用户中心自然衔接。', icon: 'Message' },
]
</script>
