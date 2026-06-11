<template>
  <div
    class="loading-screen"
    :class="{ 'loading-screen-exit': isExiting, 'loading-screen-dark': isDark }"
    :style="screenVars"
  >
    <div v-if="isDark" class="meteor-field" aria-hidden="true">
      <span v-for="item in meteors" :key="item" />
    </div>

    <div class="loader-logo" aria-label="武汉城市学院开屏动画" v-html="logoSvg" />

    <div class="loader-text">
      <div class="loader-title-wrap">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 366.015625 66.5625"
          class="loader-title-svg"
          aria-hidden="true"
        >
          <g>
            <text transform="translate(-3.75, 0.234375)">
              <tspan
                x="0"
                y="51.09375"
                font-size="60"
                :fill="textColor"
                font-family="草檀斋毛泽东字体, MaoZedong, STKaiti, KaiTi, serif"
                letter-spacing="2"
              >武汉城市学院</tspan>
            </text>
          </g>
        </svg>
      </div>
      <div class="loader-subtitle-wrap">
        <p class="loader-subtitle">
          City University of Wuhan
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useAppStore } from '@/store'

const emit = defineEmits(['finished'])

const appStore = useAppStore()
const isExiting = ref(false)
const logoSvg = ref('')
const meteors = Array.from({ length: 18 }, (_, index) => index)

let exitTimer
let finishTimer

const isDark = computed(() => appStore.isDark)
const primaryColor = computed(() => isDark.value ? '#6ee7b7' : '#394E28')
const secondaryColor = computed(() => isDark.value ? '#0f172a' : '#FFFFFF')
const textColor = computed(() => isDark.value ? '#e2e8f0' : '#000000')
const bgColor = computed(() => isDark.value ? '#0f172a' : '#fdfdfd')

const screenVars = computed(() => ({
  '--loader-bg': bgColor.value,
  '--loader-primary': primaryColor.value,
  '--loader-secondary': secondaryColor.value,
  '--loader-text': textColor.value,
}))

function buildAnimatedSvg(svgText) {
  const parser = new DOMParser()
  const doc = parser.parseFromString(svgText, 'image/svg+xml')
  const svg = doc.querySelector('svg')

  if (!svg)
    return ''

  svg.removeAttribute('width')
  svg.removeAttribute('height')
  svg.setAttribute('viewBox', '0 0 271.8 271.8')
  svg.setAttribute('class', 'loader-emblem-svg')
  svg.setAttribute('role', 'img')
  svg.setAttribute('aria-label', '武汉城市学院校徽')

  const circles = [...svg.querySelectorAll('circle')]
  circles.forEach((circle, index) => {
    circle.setAttribute('class', index === 0 ? 'anim-circle-outer' : 'anim-circle-inner')
    circle.setAttribute('fill', index === 0 ? 'var(--loader-primary)' : 'var(--loader-secondary)')
  })

  const shapes = [...svg.querySelectorAll('path, rect')]
  shapes.forEach((shape, index) => {
    shape.setAttribute('class', 'anim-shape')
    shape.setAttribute('fill', 'var(--loader-primary)')
    shape.setAttribute('stroke', 'var(--loader-primary)')
    shape.setAttribute('style', `animation-delay: ${0.8 + index * 0.05}s`)
  })

  return new XMLSerializer().serializeToString(svg)
}

async function loadLogo() {
  try {
    const response = await fetch('/wic-emblem.svg')
    const svgText = await response.text()
    logoSvg.value = buildAnimatedSvg(svgText)
  }
  catch {
    logoSvg.value = '<img src="/wic-emblem.svg" alt="武汉城市学院校徽" class="loader-emblem-fallback">'
  }
}

onMounted(() => {
  loadLogo()

  exitTimer = window.setTimeout(() => {
    isExiting.value = true
  }, 4200)

  finishTimer = window.setTimeout(() => {
    emit('finished')
  }, 5000)
})

onUnmounted(() => {
  window.clearTimeout(exitTimer)
  window.clearTimeout(finishTimer)
})
</script>

<style>
.loading-screen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: var(--loader-bg);
  transition: opacity 1s cubic-bezier(0.76, 0, 0.24, 1);
}

.loading-screen-exit {
  opacity: 0;
  pointer-events: none;
}

.loader-logo {
  position: relative;
  z-index: 2;
  width: 224px;
  height: 224px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader-emblem-svg,
.loader-emblem-fallback {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 22px 34px rgba(0, 0, 0, 0.18));
}

.anim-circle-outer {
  transform-origin: center;
  animation: loaderPopIn 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

.anim-circle-inner {
  transform-origin: center;
  animation: loaderPopIn 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: 0.1s;
  opacity: 0;
}

.anim-shape {
  stroke-width: 0.8px;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  fill-opacity: 0;
  opacity: 0;
  animation: sequentialDraw 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.loader-text {
  position: relative;
  z-index: 2;
  margin-top: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loader-title-wrap {
  width: 288px;
  max-width: 72vw;
  overflow: hidden;
  opacity: 0;
  transform: translateY(32px);
  animation: loaderTextSlideUp 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
  animation-delay: 3s;
}

.loader-title-svg {
  width: 100%;
  height: auto;
  display: block;
}

.loader-subtitle-wrap {
  margin-top: 12px;
  overflow: hidden;
}

.loader-subtitle {
  margin: 0;
  color: var(--loader-text);
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  opacity: 0;
  transform: translateY(16px);
  animation: loaderTextSlideUp 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
  animation-delay: 3.2s;
}

.meteor-field {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.meteor-field span {
  position: absolute;
  top: -10%;
  left: calc(var(--meteor-index, 0) * 6%);
  width: 140px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(110, 231, 183, 0.75), transparent);
  opacity: 0;
  transform: rotate(-35deg);
  animation: meteorPass 3.8s linear infinite;
}

.meteor-field span:nth-child(1) {
  --meteor-index: 1;
  animation-delay: 0.1s;
}
.meteor-field span:nth-child(2) {
  --meteor-index: 4;
  animation-delay: 0.7s;
}
.meteor-field span:nth-child(3) {
  --meteor-index: 8;
  animation-delay: 1.2s;
}
.meteor-field span:nth-child(4) {
  --meteor-index: 11;
  animation-delay: 1.8s;
}
.meteor-field span:nth-child(5) {
  --meteor-index: 14;
  animation-delay: 2.4s;
}
.meteor-field span:nth-child(6) {
  --meteor-index: 17;
  animation-delay: 3s;
}
.meteor-field span:nth-child(7) {
  --meteor-index: 3;
  animation-delay: 3.6s;
}
.meteor-field span:nth-child(8) {
  --meteor-index: 7;
  animation-delay: 4.2s;
}
.meteor-field span:nth-child(9) {
  --meteor-index: 13;
  animation-delay: 4.8s;
}
.meteor-field span:nth-child(10) {
  --meteor-index: 2;
  animation-delay: 5.4s;
}
.meteor-field span:nth-child(11) {
  --meteor-index: 6;
  animation-delay: 6s;
}
.meteor-field span:nth-child(12) {
  --meteor-index: 10;
  animation-delay: 6.6s;
}
.meteor-field span:nth-child(13) {
  --meteor-index: 15;
  animation-delay: 7.2s;
}
.meteor-field span:nth-child(14) {
  --meteor-index: 18;
  animation-delay: 7.8s;
}
.meteor-field span:nth-child(15) {
  --meteor-index: 5;
  animation-delay: 8.4s;
}
.meteor-field span:nth-child(16) {
  --meteor-index: 9;
  animation-delay: 9s;
}
.meteor-field span:nth-child(17) {
  --meteor-index: 12;
  animation-delay: 9.6s;
}
.meteor-field span:nth-child(18) {
  --meteor-index: 16;
  animation-delay: 10.2s;
}

@keyframes loaderPopIn {
  0% {
    opacity: 0;
    transform: scale(0.6);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes sequentialDraw {
  0% {
    opacity: 0;
    stroke-dashoffset: 1000;
    fill-opacity: 0;
  }
  10% {
    opacity: 1;
  }
  50% {
    stroke-dashoffset: 0;
    fill-opacity: 0;
  }
  100% {
    opacity: 1;
    stroke-dashoffset: 0;
    fill-opacity: 1;
    stroke-width: 0;
  }
}

@keyframes loaderTextSlideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes meteorPass {
  0% {
    opacity: 0;
    transform: translate3d(-20vw, -10vh, 0) rotate(-35deg);
  }
  12% {
    opacity: 1;
  }
  75% {
    opacity: 0.9;
  }
  100% {
    opacity: 0;
    transform: translate3d(120vw, 95vh, 0) rotate(-35deg);
  }
}

@media (min-width: 768px) {
  .loader-logo {
    width: 288px;
    height: 288px;
  }
}

@media (max-width: 640px) {
  .loader-logo {
    width: 224px;
    height: 224px;
  }

  .loader-text {
    margin-top: 40px;
  }

  .loader-title-wrap {
    width: 192px;
  }

  .loader-subtitle {
    font-size: 14px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .loading-screen {
    transition-duration: 0.01ms;
  }

  .anim-circle-outer,
  .anim-circle-inner,
  .anim-shape,
  .loader-title-wrap,
  .loader-subtitle,
  .meteor-field span {
    animation-duration: 0.01ms !important;
    animation-delay: 0ms !important;
    animation-iteration-count: 1 !important;
  }
}
</style>
