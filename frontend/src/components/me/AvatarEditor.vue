<template>
  <div class="avatar-editor">
    <!-- 左侧：参数控制区 -->
    <div class="editor-left">
      <!-- 风格选择 -->
      <div class="style-section">
        <div class="section-title">
          选择风格
        </div>
        <div class="style-grid">
          <div
            v-for="style in styles"
            :key="style.name"
            class="style-card"
            :class="{ active: selectedStyle === style.name }"
            @click="selectStyle(style.name)"
          >
            <img
              :src="getStylePreviewUrl(style.name)"
              :alt="style.label"
              class="style-preview"
            >
            <div class="style-label">
              {{ style.label }}
            </div>
          </div>
        </div>
      </div>

      <!-- 参数调节 -->
      <div class="options-section">
        <div class="section-title">
          自定义参数
        </div>

        <!-- Seed -->
        <div class="option-row">
          <span class="option-label">种子 (Seed)</span>
          <n-input v-model:value="options.seed" size="small" placeholder="默认使用用户名" @update:value="emitUpdate" />
        </div>

        <!-- 背景色 -->
        <div class="option-row">
          <span class="option-label">背景色</span>
          <div class="color-pickers">
            <n-color-picker
              v-for="(_, i) in options.backgroundColors"
              :key="i"
              v-model:value="options.backgroundColors[i]"
              size="small"
              :show-alpha="false"
              :modes="['hex']"
              class="color-picker-item"
              @update:value="emitUpdate"
            />
            <n-button
              v-if="options.backgroundColors.length < 4"
              size="tiny"
              quaternary
              @click="addBgColor"
            >
              + 添加
            </n-button>
            <n-button
              v-if="options.backgroundColors.length > 1"
              size="tiny"
              quaternary
              type="error"
              @click="removeLastBgColor"
            >
              - 移除
            </n-button>
          </div>
        </div>

        <!-- 圆角 -->
        <div class="option-row">
          <span class="option-label">圆角</span>
          <n-slider
            v-model:value="options.borderRadius"
            :min="0"
            :max="50"
            :step="1"
            class="option-slider"
            @update:value="emitUpdate"
          />
          <span class="option-value">{{ options.borderRadius }}%</span>
        </div>

        <!-- 翻转 -->
        <div class="option-row">
          <span class="option-label">翻转</span>
          <n-select
            v-model:value="options.flip"
            :options="flipOptions"
            size="small"
            class="option-select"
            @update:value="emitUpdate"
          />
        </div>

        <!-- 旋转 -->
        <div class="option-row">
          <span class="option-label">旋转</span>
          <n-slider
            v-model:value="options.rotate"
            :min="0"
            :max="360"
            :step="1"
            class="option-slider"
            @update:value="emitUpdate"
          />
          <span class="option-value">{{ options.rotate }}°</span>
        </div>

        <!-- 风格特色选项（动态加载） -->
        <template v-if="styleOptions.length">
          <n-divider class="my-8!" />
          <div class="section-title text-12 opacity-50">
            风格特色选项
          </div>
          <div v-for="opt in styleOptions" :key="opt.key" class="option-row">
            <span class="option-label">{{ opt.label }}</span>
            <n-select
              v-model:value="opt.value"
              :options="opt.choices"
              size="small"
              class="option-select"
              @update:value="emitUpdate"
            />
          </div>
        </template>
      </div>
    </div>

    <!-- 右侧：实时预览与快捷操作 -->
    <div class="editor-right">
      <div class="preview-section">
        <div class="section-title">
          实时预览
        </div>
        <div class="preview-container">
          <img :src="previewUrl" alt="avatar preview" class="preview-image" :style="previewStyle">
        </div>
        <div class="preview-sizes">
          <div class="preview-size-item">
            <img :src="previewUrl" alt="" class="preview-medium" :style="previewStyle">
            <span class="size-label">72px</span>
          </div>
          <div class="preview-size-item">
            <img :src="previewUrl" alt="" class="preview-small" :style="previewStyle">
            <span class="size-label">40px</span>
          </div>
        </div>

        <div class="editor-actions">
          <n-button secondary type="primary" class="flex-1" @click="randomize">
            <template #icon>
              <i class="i-fe:shuffle" />
            </template>
            随机搭配
          </n-button>
          <n-button secondary @click="resetOptions">
            重置
          </n-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const props = defineProps({
  username: { type: String, default: '' },
  modelValue: { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue'])

const DICEBEAR_BASE = 'https://api.dicebear.com/10.x'

const styles = [
  { name: 'lorelei', label: '手绘风' },
  { name: 'pixel-art', label: '像素风' },
  { name: 'bottts', label: '机器人' },
  { name: 'avataaars', label: '卡通' },
  { name: 'adventurer', label: '冒险者' },
  { name: 'big-smile', label: '大笑脸' },
  { name: 'notionists', label: '简约' },
  { name: 'open-peeps', label: '涂鸦' },
  { name: 'micah', label: '插画' },
  { name: 'croodles', label: '手绘' },
  { name: 'fun-emoji', label: '表情' },
  { name: 'thumbs', label: '简约脸' },
]

const selectedStyle = ref('lorelei')
const styleOptions = ref([])

const options = ref({
  seed: props.username || '',
  backgroundColors: ['b6e3f4', 'c0aede', 'd1d4f9'],
  borderRadius: 50,
  flip: 'none',
  rotate: 0,
})

const flipOptions = [
  { label: '无', value: 'none' },
  { label: '水平翻转', value: 'horizontal' },
  { label: '垂直翻转', value: 'vertical' },
  { label: '双向翻转', value: 'both' },
]

function getStylePreviewUrl(styleName) {
  return `${DICEBEAR_BASE}/${styleName}/svg?seed=${props.username || 'demo'}&size=80&backgroundColor=b6e3f4,c0aede,d1d4f9`
}

function buildQueryString(paramsObj) {
  return Object.entries(paramsObj)
    .filter(([, v]) => v !== null && v !== undefined && v !== '')
    .map(([k, v]) => `${encodeURIComponent(k)}=${String(v).split(',').map(encodeURIComponent).join(',')}`)
    .join('&')
}

const previewUrl = computed(() => {
  const params = {
    seed: options.value.seed || props.username || 'demo',
    size: '200',
  }

  if (options.value.backgroundColors.length) {
    params.backgroundColor = options.value.backgroundColors.join(',')
  }
  if (options.value.borderRadius > 0) {
    params.borderRadius = String(options.value.borderRadius)
  }
  if (options.value.flip !== 'none') {
    params.flip = options.value.flip
  }
  if (options.value.rotate > 0) {
    params.rotate = String(options.value.rotate)
  }

  // 风格特色选项
  for (const opt of styleOptions.value) {
    if (opt.value && opt.value !== '__random__') {
      params[opt.key] = opt.value
    }
  }

  return `${DICEBEAR_BASE}/${selectedStyle.value}/svg?${buildQueryString(params)}`
})

const previewStyle = computed(() => ({
  borderRadius: `${options.value.borderRadius}%`,
}))

const finalUrl = computed(() => {
  const params = {
    seed: options.value.seed || props.username || 'demo',
  }

  if (options.value.backgroundColors.length) {
    params.backgroundColor = options.value.backgroundColors.join(',')
  }
  if (options.value.borderRadius > 0) {
    params.borderRadius = String(options.value.borderRadius)
  }
  if (options.value.flip !== 'none') {
    params.flip = options.value.flip
  }
  if (options.value.rotate > 0) {
    params.rotate = String(options.value.rotate)
  }

  for (const opt of styleOptions.value) {
    if (opt.value && opt.value !== '__random__') {
      params[opt.key] = opt.value
    }
  }

  return `${DICEBEAR_BASE}/${selectedStyle.value}/svg?${buildQueryString(params)}`
})

function emitUpdate() {
  emit('update:modelValue', finalUrl.value)
}

function addBgColor() {
  const colors = ['ffd5dc', 'ffdfbf', 'd1d4f9', 'b6e3f4', 'c0aede', 'ffc3a0']
  const next = colors.find(c => !options.value.backgroundColors.includes(c)) || 'ffd5dc'
  options.value.backgroundColors.push(next)
  emitUpdate()
}

function removeLastBgColor() {
  options.value.backgroundColors.pop()
  emitUpdate()
}

async function selectStyle(name) {
  selectedStyle.value = name
  styleOptions.value = []
  emitUpdate()

  // 动态加载风格特色选项
  try {
    const res = await fetch(`${DICEBEAR_BASE}/${name}/options.json`)
    if (!res.ok)
      return
    const schema = await res.json()

    // 只展示 enum 类型的特色选项（排除核心选项）
    const coreKeys = new Set(['seed', 'flip', 'size', 'borderRadius', 'rotate', 'scale', 'translateX', 'translateY', 'backgroundColor'])
    const featureOptions = []

    for (const [key, def] of Object.entries(schema)) {
      if (coreKeys.has(key))
        continue
      if (def.type === 'enum' && def.values?.length > 1 && key.endsWith('Variant')) {
        const label = key.replace(/Variant$/, '').replace(/([A-Z])/g, ' $1').trim()
        const labelMap = {
          hair: '发型',
          eyes: '眼睛',
          eyebrows: '眉毛',
          mouth: '嘴巴',
          nose: '鼻子',
          beard: '胡子',
          glasses: '眼镜',
          earrings: '耳饰',
          freckles: '雀斑',
          head: '头型',
          skin: '肤色',
          accessories: '配饰',
        }
        featureOptions.push({
          key,
          label: labelMap[label] || label,
          value: '__random__',
          choices: [
            { label: '随机', value: '__random__' },
            ...def.values.slice(0, 20).map(v => ({ label: v, value: v })),
          ],
        })
      }
      // 只展示前 4 个特色选项，避免太多
      if (featureOptions.length >= 4)
        break
    }

    styleOptions.value = featureOptions
  }
  catch (e) {
    console.warn('加载风格选项失败:', e)
  }
}

// 从已有 URL 解析配置
function parseExistingUrl(url) {
  if (!url || !url.includes('dicebear.com'))
    return
  try {
    const urlObj = new URL(url)
    const parts = urlObj.pathname.split('/')
    if (parts.length >= 3) {
      selectedStyle.value = parts[2] // /10.x/{style}/svg
    }
    const params = urlObj.searchParams
    if (params.has('seed'))
      options.value.seed = params.get('seed')
    if (params.has('backgroundColor'))
      options.value.backgroundColors = params.get('backgroundColor').split(',')
    if (params.has('borderRadius'))
      options.value.borderRadius = Number(params.get('borderRadius'))
    if (params.has('flip'))
      options.value.flip = params.get('flip')
    if (params.has('rotate'))
      options.value.rotate = Number(params.get('rotate'))
  }
  catch { /* ignore */ }
}

onMounted(() => {
  if (props.modelValue) {
    parseExistingUrl(props.modelValue)
  }
  emitUpdate()
})

watch(() => props.username, (val) => {
  if (!options.value.seed) {
    options.value.seed = val || ''
    emitUpdate()
  }
})

// 随机搭配
async function randomize() {
  const randomStyle = styles[Math.floor(Math.random() * styles.length)].name

  // 1. 先加载随机风格的选项定义
  await selectStyle(randomStyle)

  // 2. 随机核心配置
  const randomSeed = Math.random().toString(36).substring(2, 10)
  const randomColors = ['b6e3f4', 'c0aede', 'd1d4f9', 'ffd5dc', 'ffdfbf', 'ffc3a0', 'bbf7d0', 'fecdd3', 'e2e8f0', 'cbd5e1']
  const bgCount = Math.floor(Math.random() * 3) + 1
  const bgColors = []
  while (bgColors.length < bgCount) {
    const c = randomColors[Math.floor(Math.random() * randomColors.length)]
    if (!bgColors.includes(c))
      bgColors.push(c)
  }

  options.value = {
    seed: randomSeed,
    backgroundColors: bgColors,
    borderRadius: Math.random() > 0.5 ? 50 : (Math.random() > 0.5 ? 0 : Math.floor(Math.random() * 30)),
    flip: flipOptions[Math.floor(Math.random() * flipOptions.length)].value,
    rotate: Math.random() > 0.5 ? 0 : Math.floor(Math.random() * 36) * 10,
  }

  // 3. 随机选择该风格下的微调特色选项
  if (styleOptions.value.length) {
    styleOptions.value.forEach((opt) => {
      if (opt.choices.length > 1) {
        const idx = Math.floor(Math.random() * (opt.choices.length - 1)) + 1
        opt.value = opt.choices[idx].value
      }
    })
  }

  emitUpdate()
}

// 重置参数
function resetOptions() {
  options.value = {
    seed: props.username || '',
    backgroundColors: ['b6e3f4', 'c0aede', 'd1d4f9'],
    borderRadius: 50,
    flip: 'none',
    rotate: 0,
  }
  if (styleOptions.value.length) {
    styleOptions.value.forEach((opt) => {
      opt.value = '__random__'
    })
  }
  emitUpdate()
}
</script>

<style scoped>
.avatar-editor {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 24px;
  align-items: start;
}

.editor-left {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-height: 480px;
  overflow-y: auto;
  padding-right: 8px;
}

/* 自定义控制区滚动条 */
.editor-left::-webkit-scrollbar {
  width: 5px;
}
.editor-left::-webkit-scrollbar-track {
  background: transparent;
}
.editor-left::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}
:global(.dark) .editor-left::-webkit-scrollbar-thumb,
.dark .editor-left::-webkit-scrollbar-thumb {
  background: #475569;
}

.editor-right {
  position: sticky;
  top: 0;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 10px;
}
:global(.dark) .section-title,
.dark .section-title {
  color: #94a3b8;
}

/* 风格选择网格，在双栏下左侧空间缩小，4列最为精美 */
.style-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.style-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 8px 4px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #f8fafc;
}
:global(.dark) .style-card,
.dark .style-card {
  background: #1e293b;
  border-color: #334155;
}

.style-card:hover {
  border-color: #059669;
  background: #ecfdf5;
}
:global(.dark) .style-card:hover,
.dark .style-card:hover {
  background: #064e3b;
  border-color: #059669;
}

.style-card.active {
  border-color: #059669;
  background: #ecfdf5;
  box-shadow: 0 0 0 2px rgba(5, 150, 105, 0.15);
}
:global(.dark) .style-card.active,
.dark .style-card.active {
  background: #064e3b;
  border-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
}

.style-preview {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  background: #e2e8f0;
}
:global(.dark) .style-preview,
.dark .style-preview {
  background: #334155;
}

.style-label {
  font-size: 11px;
  font-weight: 500;
  color: #475569;
  text-align: center;
}
:global(.dark) .style-label,
.dark .style-label {
  color: #cbd5e1;
}

.options-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.option-label {
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
  min-width: 80px;
  flex-shrink: 0;
}
:global(.dark) .option-label,
.dark .option-label {
  color: #94a3b8;
}

.option-slider {
  flex: 1;
}

.option-value {
  font-size: 11px;
  font-family: monospace;
  color: #64748b;
  min-width: 32px;
  text-align: right;
}
:global(.dark) .option-value,
.dark .option-value {
  color: #94a3b8;
}

.option-select {
  flex: 1;
}

.color-pickers {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  flex-wrap: wrap;
}

/* 彻底解决 n-color-picker 被 flex 拉伸的问题 */
.color-picker-item {
  width: 36px !important;
  height: 36px !important;
  flex-grow: 0 !important;
  flex-shrink: 0 !important;
  border-radius: 6px !important;
  overflow: hidden;
}

.preview-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #e2e8f0;
}
:global(.dark) .preview-section,
.dark .preview-section {
  background: #1e293b;
  border-color: #334155;
}

.preview-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px;
  background: repeating-conic-gradient(#e2e8f0 0% 25%, transparent 0% 50%) 0 0 / 16px 16px;
  border-radius: 12px;
  width: 100%;
  aspect-ratio: 1;
  border: 1px dashed #cbd5e1;
  box-sizing: border-box;
}
:global(.dark) .preview-container,
.dark .preview-container {
  background: repeating-conic-gradient(#334155 0% 25%, transparent 0% 50%) 0 0 / 16px 16px;
  border-color: #475569;
}

.preview-image {
  width: 128px;
  height: 128px;
  object-fit: cover;
  filter: drop-shadow(0 4px 6px -1px rgba(0, 0, 0, 0.1));
}

.preview-sizes {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 20px;
  margin: 16px 0;
  width: 100%;
}

.preview-size-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.size-label {
  font-size: 10px;
  font-family: monospace;
  color: #94a3b8;
}

.preview-small {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 50%;
  background: #f1f5f9;
}
:global(.dark) .preview-small,
.dark .preview-small {
  background: #334155;
}

.preview-medium {
  width: 72px;
  height: 72px;
  object-fit: cover;
  border-radius: 50%;
  background: #f1f5f9;
}
:global(.dark) .preview-medium,
.dark .preview-medium {
  background: #334155;
}

.editor-actions {
  display: flex;
  gap: 8px;
  width: 100%;
}

/* 响应式样式与移动端置顶 */
@media (max-width: 576px) {
  .avatar-editor {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .editor-left {
    max-height: none;
    overflow-y: visible;
    padding-right: 0;
  }

  .style-grid {
    grid-template-columns: repeat(6, 1fr);
  }

  .editor-right {
    order: -1; /* 移动端预览置顶 */
    position: static;
  }

  .preview-container {
    padding: 16px;
    height: auto;
    max-height: 180px;
  }

  .preview-image {
    width: 96px;
    height: 96px;
  }
}
</style>
