<template>
  <div class="avatar-editor">
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

    <!-- 预览 -->
    <div class="preview-section">
      <div class="section-title">
        预览
      </div>
      <div class="preview-container">
        <img :src="previewUrl" alt="avatar preview" class="preview-image" :style="previewStyle">
      </div>
      <div class="preview-sizes">
        <img :src="previewUrl" alt="" class="preview-small" :style="previewStyle">
        <span class="text-12 opacity-50">40px</span>
        <img :src="previewUrl" alt="" class="preview-medium" :style="previewStyle">
        <span class="text-12 opacity-50">72px</span>
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
</script>

<style scoped>
.avatar-editor {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 8px;
}

.style-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
}

.style-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 4px;
  border-radius: 8px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
  background: #f8fafc;
}
.style-card:hover {
  border-color: #a7f3d0;
  background: #ecfdf5;
}
.style-card.active {
  border-color: #059669;
  background: #ecfdf5;
}

.style-preview {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.style-label {
  font-size: 11px;
  color: #64748b;
  text-align: center;
}

.options-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.option-label {
  font-size: 13px;
  color: #64748b;
  min-width: 70px;
  flex-shrink: 0;
}

.option-slider {
  flex: 1;
}

.option-value {
  font-size: 12px;
  color: #94a3b8;
  min-width: 36px;
  text-align: right;
}

.option-select {
  flex: 1;
}

.color-pickers {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  flex-wrap: wrap;
}

.color-picker-item {
  width: 48px !important;
}

.preview-section {
  text-align: center;
}

.preview-container {
  display: flex;
  justify-content: center;
  padding: 16px;
  background: repeating-conic-gradient(#e5e7eb 0% 25%, transparent 0% 50%) 0 0 / 16px 16px;
  border-radius: 12px;
}

.preview-image {
  width: 128px;
  height: 128px;
  object-fit: cover;
}

.preview-sizes {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 12px;
}

.preview-small {
  width: 40px;
  height: 40px;
  object-fit: cover;
}

.preview-medium {
  width: 72px;
  height: 72px;
  object-fit: cover;
}
</style>
