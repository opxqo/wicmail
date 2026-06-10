<template>
  <div ref="pageRef" class="landing-page">
    <header class="site-nav" :class="{ 'site-nav-solid': isScrolled }">
      <router-link to="/" class="brand-link" aria-label="WicMail 首页">
        <img src="/wic-emblem.svg" alt="武汉城市学院校徽" class="brand-emblem">
        <div class="brand-copy">
          <span class="brand-title">WicMail</span>
          <span class="brand-subtitle">校园邮箱服务</span>
        </div>
      </router-link>

      <nav class="desktop-nav" aria-label="首页导航">
        <a
          v-for="item in navItems"
          :key="item.target"
          :href="`#${item.target}`"
          @click.prevent="scrollToSection(item.target)"
        >
          {{ item.label }}
        </a>
      </nav>

      <div class="nav-actions">
        <a class="nav-ghost" href="https://www.wic.edu.kg" target="_blank" rel="noopener noreferrer">
          学校官网
        </a>
        <router-link class="nav-primary" to="/login">
          登录工作台
        </router-link>
      </div>
    </header>

    <main>
      <section id="hero" class="hero-section" aria-labelledby="hero-title">
        <div class="hero-bg" :style="{ transform: `translateY(${scrollY * 0.18}px)` }">
          <img src="/cover.avif" alt="武汉城市学院校园风光" class="hero-img">
          <div class="hero-overlay" />
        </div>

        <div class="hero-content">
          <div class="hero-badge">
            <i class="i-fe:shield text-13 text-emerald-200" />
            <span>面向师生的 @wic.edu.kg 邮箱服务</span>
          </div>

          <h1 id="hero-title" class="hero-title">
            <span>WicMail</span>
            <small>校园邮箱申请与管理平台</small>
          </h1>

          <p class="hero-desc">
            统一完成校园邮箱申请、资料审核、邮箱查看与管理入口。用一个清晰可靠的工作台，把校园身份、学术沟通和日常通知连接起来。
          </p>

          <div class="hero-actions">
            <router-link to="/login" class="btn btn-primary">
              申请校园邮箱
              <i class="i-fe:arrow-right text-16" />
            </router-link>
            <router-link to="/login" class="btn btn-secondary">
              进入工作台
            </router-link>
          </div>

          <div class="mobile-quick-grid" aria-label="快捷入口">
            <router-link v-for="item in quickActions" :key="item.label" :to="item.to" class="quick-item">
              <span class="quick-icon">
                <i :class="item.icon" class="text-22" />
              </span>
              <span>{{ item.label }}</span>
            </router-link>
          </div>
        </div>

        <a class="scroll-cue" href="#intro" aria-label="继续浏览" @click.prevent="scrollToSection('intro')">
          <img src="/BxsMouseAlt.svg" class="scroll-mouse-icon" alt="scroll">
          <small>SCROLL</small>
        </a>
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
      <div class="section-container footer-grid">
        <div class="footer-brand">
          <div class="footer-logo">
            <img src="/wic-emblem.svg" alt="武汉城市学院校徽">
            <div>
              <strong>WicMail</strong>
              <span>校园邮箱服务</span>
            </div>
          </div>
          <p>为校园身份、学术沟通与日常通知提供清晰可靠的邮箱申请和管理入口。</p>
          <img src="/wic-motto.svg" alt="励志修德 勤学创新" class="motto-img">
        </div>

        <div class="footer-col">
          <h3>快捷入口</h3>
          <router-link to="/login">登录工作台</router-link>
          <router-link to="/login">申请邮箱</router-link>
          <router-link to="/login">邮件中心</router-link>
        </div>

        <div class="footer-col">
          <h3>页面导航</h3>
          <a href="#intro" @click.prevent="scrollToSection('intro')">服务介绍</a>
          <a href="#process" @click.prevent="scrollToSection('process')">申请流程</a>
          <a href="#features" @click.prevent="scrollToSection('features')">核心能力</a>
          <a href="#faq" @click.prevent="scrollToSection('faq')">常见问题</a>
        </div>

        <div class="footer-col">
          <h3>联系与链接</h3>
          <a href="mailto:admin@wic.edu.kg">admin@wic.edu.kg</a>
          <a href="https://www.wic.edu.kg" target="_blank" rel="noopener noreferrer">www.wic.edu.kg</a>
          <span>武汉城市学院校园服务</span>
        </div>
      </div>

      <div class="footer-bottom">
        <span>© {{ currentYear }} WicMail · 武汉城市学院 · 校园邮箱服务平台</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const pageRef = ref(null)
const scrollY = ref(0)
const isScrolled = computed(() => scrollY.value > 24)
const currentYear = new Date().getFullYear()

const navItems = [
  { label: '服务介绍', target: 'intro' },
  { label: '申请流程', target: 'process' },
  { label: '核心能力', target: 'features' },
  { label: '常见问题', target: 'faq' },
]

const quickActions = [
  { label: '申请邮箱', icon: 'i-fe:mail', to: '/login' },
  { label: '查看邮件', icon: 'i-fe:inbox', to: '/login' },
  { label: '资料审核', icon: 'i-fe:check-square', to: '/login' },
  { label: '工作台', icon: 'i-fe:grid', to: '/login' },
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

.site-nav {
  position: fixed;
  z-index: 80;
  top: 0;
  left: 0;
  right: 0;
  height: 78px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 0 clamp(18px, 4vw, 56px);
  border-bottom: 1px solid transparent;
  color: #fff;
  transition: background 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease, height 0.25s ease;
}

.site-nav-solid {
  height: 68px;
  color: var(--wic-ink);
  background: rgba(255, 255, 255, 0.88);
  border-color: rgba(49, 85, 43, 0.12);
  box-shadow: 0 16px 40px rgba(16, 31, 14, 0.08);
  backdrop-filter: blur(18px);
}

.brand-link,
.nav-actions,
.desktop-nav,
.hero-actions,
.intro-actions {
  display: flex;
  align-items: center;
}

.brand-link {
  min-width: 0;
  gap: 12px;
  color: inherit;
  text-decoration: none;
}

.brand-emblem {
  width: 42px;
  height: 42px;
  object-fit: contain;
  padding: 4px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.18);
}

.brand-copy {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.brand-title {
  font-size: 18px;
  font-weight: 800;
}

.brand-subtitle {
  margin-top: 4px;
  font-size: 12px;
  opacity: 0.72;
}

.desktop-nav {
  gap: 8px;
  padding: 6px;
  border: 1px solid currentColor;
  border-color: rgba(255, 255, 255, 0.16);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
}

.site-nav-solid .desktop-nav {
  border-color: rgba(49, 85, 43, 0.12);
  background: rgba(49, 85, 43, 0.06);
}

.desktop-nav a,
.nav-ghost,
.nav-primary {
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 650;
}

.desktop-nav a {
  padding: 0 16px;
  color: inherit;
  opacity: 0.82;
}

.desktop-nav a:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.14);
}

.site-nav-solid .desktop-nav a:hover {
  background: rgba(49, 85, 43, 0.1);
}

.nav-actions {
  gap: 10px;
}

.nav-ghost {
  padding: 0 16px;
  color: inherit;
  border: 1px solid rgba(255, 255, 255, 0.24);
}

.site-nav-solid .nav-ghost {
  border-color: rgba(49, 85, 43, 0.16);
}

.nav-primary {
  padding: 0 18px;
  color: var(--wic-primary);
  background: #fff;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.16);
}

.site-nav-solid .nav-primary {
  color: #fff;
  background: var(--wic-primary);
  box-shadow: 0 12px 28px rgba(49, 85, 43, 0.22);
}

.hero-section {
  position: relative;
  min-height: 100dvh;
  display: flex;
  align-items: center;
  overflow: hidden;
  padding: 110px 24px 82px;
}

.hero-bg,
.hero-overlay,
.hero-img {
  position: absolute;
  inset: 0;
}

.hero-bg {
  z-index: 0;
  height: 115%;
}

.hero-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.05);
}

.hero-overlay {
  z-index: 1;
  background:
    radial-gradient(circle at 18% 72%, rgba(158, 231, 168, 0.28), transparent 26%),
    linear-gradient(90deg, rgba(8, 16, 8, 0.86) 0%, rgba(13, 25, 12, 0.6) 46%, rgba(13, 25, 12, 0.34) 100%),
    linear-gradient(180deg, rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.62));
}

.hero-content {
  position: relative;
  z-index: 2;
  width: min(100%, 1180px);
  margin: 0 auto;
  color: #fff;
}

.hero-badge {
  width: fit-content;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border: 1px solid rgba(255, 255, 255, 0.24);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
  backdrop-filter: blur(14px);
  font-size: 13px;
  font-weight: 650;
}

.hero-title {
  max-width: 860px;
  margin: 28px 0 22px;
  line-height: 0.98;
}

.hero-title span {
  display: block;
  font-size: clamp(58px, 11vw, 128px);
  font-weight: 900;
}

.hero-title small {
  display: block;
  margin-top: 18px;
  color: var(--wic-accent);
  font-size: clamp(21px, 3.4vw, 42px);
  font-weight: 350;
  line-height: 1.22;
}

.hero-desc {
  max-width: 680px;
  margin: 0;
  color: rgba(255, 255, 255, 0.78);
  font-size: 17px;
  line-height: 1.9;
}

.hero-actions {
  gap: 14px;
  margin-top: 38px;
}

.btn {
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  padding: 0 24px;
  border-radius: 999px;
  text-decoration: none;
  font-size: 15px;
  font-weight: 800;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-primary {
  color: var(--wic-primary-strong);
  background: #fff;
  box-shadow: 0 20px 44px rgba(0, 0, 0, 0.22);
}

.btn-primary:hover {
  color: #fff;
  background: var(--wic-primary);
}

.btn-secondary {
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.34);
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
}

.mobile-quick-grid {
  display: none;
}

.quick-item {
  color: #fff;
  text-decoration: none;
}

.scroll-cue {
  position: absolute;
  z-index: 3;
  bottom: 26px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
  color: rgba(255, 255, 255, 0.72);
  text-decoration: none;
}

.scroll-mouse-icon {
  width: 20px;
  height: auto;
  opacity: 0.8;
  filter: brightness(0) invert(1);
  animation: scrollBounce 2s ease-in-out infinite;
}

.scroll-cue small {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 3px;
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

.site-footer {
  background: #10190f;
  color: #fff;
}

.footer-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) repeat(3, minmax(0, 0.75fr));
  gap: 36px;
  padding-top: 54px;
  padding-bottom: 42px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.footer-logo img {
  width: 42px;
  height: 42px;
  filter: brightness(0) invert(1);
}

.footer-logo div,
.footer-col {
  display: flex;
  flex-direction: column;
}

.footer-logo strong {
  font-size: 20px;
}

.footer-logo span,
.footer-brand p,
.footer-col a,
.footer-col span {
  color: rgba(255, 255, 255, 0.62);
}

.footer-brand p {
  max-width: 360px;
  margin: 18px 0;
}

.motto-img {
  width: 190px;
  max-width: 100%;
  filter: brightness(0) invert(1);
  opacity: 0.68;
}

.footer-col h3 {
  margin: 0 0 16px;
  color: #fff;
  font-size: 15px;
}

.footer-col a,
.footer-col span {
  width: fit-content;
  margin-bottom: 10px;
  text-decoration: none;
  font-size: 14px;
}

.footer-col a:hover {
  color: var(--wic-accent);
}

.footer-bottom {
  display: flex;
  justify-content: center;
  padding: 18px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
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

  .hero-title span {
    font-size: 52px;
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
