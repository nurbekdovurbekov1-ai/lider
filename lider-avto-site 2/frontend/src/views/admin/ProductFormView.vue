<template>
  <div class="max-w-3xl space-y-6">
    <div class="flex items-center gap-3">
      <router-link to="/admin/products" class="btn-sm btn-ghost text-slate-400 p-2">
        <ChevronLeft class="w-5 h-5" />
      </router-link>
      <h1 class="text-2xl font-bold text-white">{{ isEdit ? 'Mahsulotni Tahrirlash' : 'Yangi Mahsulot' }}</h1>
    </div>

    <form @submit.prevent="submit" class="space-y-6">
      <!-- Basic Info -->
      <div class="bg-slate-800 rounded-2xl p-6 border border-slate-700 space-y-4">
        <h2 class="font-semibold text-white mb-2">Asosiy ma'lumotlar</h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="form-label text-slate-300">Mahsulot nomi *</label>
            <input v-model="form.name" type="text" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500 focus:border-brand-500" id="product-form-name" required />
          </div>
          <div>
            <label class="form-label text-slate-300">Kategoriya *</label>
            <select v-model="form.category" class="form-select bg-slate-700 border-slate-600 text-white focus:border-brand-500" id="product-form-category" required>
              <option value="">Tanlang...</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
            <div v-if="!showNewCat" class="mt-1.5">
              <button type="button" @click="showNewCat = true" class="text-xs text-brand-400 hover:text-brand-300 inline-flex items-center gap-1">
                <Plus class="w-3.5 h-3.5" /> Yangi kategoriya qo'shish
              </button>
            </div>
            <div v-else class="mt-2 flex gap-2">
              <input v-model="newCatName" @keydown.enter.prevent="quickAddCategory" type="text" placeholder="Kategoriya nomi"
                class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500 flex-1" />
              <button type="button" @click="quickAddCategory" :disabled="addingCat" class="btn-sm btn-primary">{{ addingCat ? '...' : 'Qo\'shish' }}</button>
              <button type="button" @click="showNewCat = false; newCatName = ''" class="btn-sm bg-slate-700 text-slate-300 hover:bg-slate-600">
                <X class="w-4 h-4" />
              </button>
            </div>
          </div>
          <div>
            <label class="form-label text-slate-300">Sifat turi</label>
            <select v-model="form.quality" class="form-select bg-slate-700 border-slate-600 text-white focus:border-brand-500">
              <option value="">Tanlanmagan</option>
              <option value="original">Original</option>
              <option value="analog">Analog (sifatli)</option>
              <option value="premium">Premium</option>
            </select>
          </div>
          <div>
            <label class="form-label text-slate-300">Narx (1 dona uchun, UZS) *</label>
            <input v-model.number="form.base_price" type="number" min="0" step="1000" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500 focus:border-brand-500" id="product-form-price" required />
          </div>
          <div>
            <label class="form-label text-slate-300">Omborda qoldiq (dona) *</label>
            <input v-model.number="form.stock" type="number" min="0" step="1" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500 focus:border-brand-500" id="product-form-stock" />
          </div>
          <div>
            <label class="form-label text-slate-300">Badge (ixtiyoriy)</label>
            <select v-model="form.badge" class="form-select bg-slate-700 border-slate-600 text-white focus:border-brand-500">
              <option value="">Yo'q</option>
              <option value="new">Yangi</option>
              <option value="hit">Ommabop</option>
              <option value="sale">Sotuvda</option>
            </select>
          </div>
          <div class="sm:col-span-2">
            <label class="form-label text-slate-300">Mos mashinalar</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="c in carModels"
                :key="c.id"
                type="button"
                @click="toggleCar(c.id)"
                class="px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors"
                :class="form.car_models.includes(c.id) ? 'bg-accent-500 border-accent-500 text-white' : 'border-slate-600 text-slate-300 hover:border-slate-400'"
              >{{ c.name }}</button>
            </div>
            <div class="mt-3 flex gap-2 max-w-sm">
              <input v-model="newCarName" @keydown.enter.prevent="quickAddCar" type="text" placeholder="Yangi mashina (masalan: Nexia 3)"
                class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500 flex-1" />
              <button type="button" @click="quickAddCar" :disabled="addingCar" class="btn-sm btn-primary inline-flex items-center gap-1">
                <Plus class="w-4 h-4" /> {{ addingCar ? '...' : 'Qo\'shish' }}
              </button>
            </div>
          </div>
        </div>

        <div>
          <label class="form-label text-slate-300">Tavsif</label>
          <textarea v-model="form.description" rows="3" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500 focus:border-brand-500 resize-none" />
        </div>

        <div>
          <label class="form-label text-slate-300">Nima uchun ishlatiladi?</label>
          <textarea v-model="form.usage" rows="3" placeholder="Qismning vazifasi va qachon almashtirish kerakligi" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500 focus:border-brand-500 resize-none" />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label class="form-label text-slate-300">Brend</label>
            <input v-model="form.brand" type="text" placeholder="Bosch" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500" />
          </div>
          <div>
            <label class="form-label text-slate-300">Artikul</label>
            <input v-model="form.article" type="text" placeholder="BS-0986" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500" />
          </div>
          <div>
            <label class="form-label text-slate-300">Kafolat</label>
            <input v-model="form.warranty" type="text" placeholder="6 oy" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500" />
          </div>
        </div>

        <label class="flex items-center gap-2 cursor-pointer">
          <input v-model="form.is_active" type="checkbox" class="w-4 h-4" />
          <span class="text-slate-300 text-sm">Aktiv (saytda ko'rsatiladi)</span>
        </label>
      </div>

      <!-- Images -->
      <div class="bg-slate-800 rounded-2xl p-6 border border-slate-700">
        <h2 class="font-semibold text-white mb-1">Mahsulot Rasmlari</h2>
        <p class="text-slate-400 text-xs mb-4">Rasm qo'shish, o'chirish va asosiy rasmni belgilash</p>

        <!-- Yangi rasm yuklash -->
        <label
          class="flex flex-col items-center justify-center gap-2 w-full h-28 border-2 border-dashed border-slate-600 rounded-xl cursor-pointer hover:border-brand-500/60 hover:bg-brand-500/5 transition-colors mb-5"
        >
          <ImagePlus class="w-6 h-6 text-slate-500" />
          <span class="text-sm text-slate-400">Rasm tanlash / yuklash</span>
          <input ref="fileInputRef" type="file" accept="image/*" multiple class="hidden" @change="handleFileSelect" />
        </label>

        <!-- Boshqa/yangi rasmlar grid -->
        <div v-if="uploadFiles.length || existingImages.length" class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3">
          <!-- Mavjud rasmlar -->
          <div v-for="img in existingImages" :key="img.id" class="relative group rounded-xl overflow-hidden border border-slate-700 aspect-square bg-slate-700">
            <img :src="img.image" alt="Mahsulot rasmi" class="w-full h-full object-cover" />
            <div class="absolute top-1 right-1 flex gap-1">
              <button
                v-if="!img.is_main"
                type="button"
                @click="setMainImage(img)"
                title="Asosiy qilish"
                class="bg-slate-900/80 hover:bg-brand-600 text-white rounded-lg p-1.5 transition-colors"
              >
                <Star class="w-3.5 h-3.5" />
              </button>
              <button
                type="button"
                @click="removeExistingImage(img)"
                title="O'chirish"
                class="bg-slate-900/80 hover:bg-red-600 text-white rounded-lg p-1.5 transition-colors"
              >
                <Trash2 class="w-3.5 h-3.5" />
              </button>
            </div>
            <span
              v-if="img.is_main"
              class="absolute bottom-1 left-1 text-[10px] font-bold uppercase tracking-wide bg-brand-600/90 text-white px-2 py-0.5 rounded-md"
            >
              Asosiy
            </span>
          </div>

          <!-- Yangi tanlangan rasmlar -->
          <div v-for="(file, i) in uploadFiles" :key="'new-' + i" class="relative group rounded-xl overflow-hidden border border-slate-700 aspect-square bg-slate-700">
            <img :src="file.preview" alt="Yangi rasm" class="w-full h-full object-cover" />
            <button
              type="button"
              @click="uploadFiles.splice(i, 1)"
              title="O'chirish"
              class="absolute top-1 right-1 bg-slate-900/80 hover:bg-red-600 text-white rounded-lg p-1.5 transition-colors"
            >
              <X class="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <p v-else class="text-slate-500 text-sm text-center py-4 border border-dashed border-slate-700 rounded-xl">
          Hozircha rasm yo'q. Yuqoridan rasm yuklang.
        </p>
        <div v-if="existingImages.length === 0 && uploadFiles.length > 0" class="mt-3 text-xs text-slate-500">
          Birinchi yuklangan rasm asosiy rasm bo'ladi.
        </div>
      </div>

      <!-- Colors -->
      <div class="bg-slate-800 rounded-2xl p-6 border border-slate-700">
        <div class="flex items-center justify-between mb-2">
          <h2 class="font-semibold text-white">Variantlar va narxlari (ixtiyoriy)</h2>
          <span class="text-xs text-slate-400">Jami: {{ form.colors.length }} ta variant</span>
        </div>
        <p class="text-slate-400 text-xs mb-4">
          Har bir rang uchun o'z narxini kiriting (masalan: Oq 12 000, Qora 18 000, Kulrang 15 000). Narx kiritilmasa, mahsulotning asosiy narxi ishlatiladi.
        </p>

        <div class="space-y-3 mb-4">
          <div
            v-for="(color, i) in form.colors"
            :key="color.id || i"
            class="flex flex-col sm:flex-row sm:items-center gap-2.5 sm:gap-3 bg-slate-700/80 rounded-xl p-3 border border-slate-600/60"
          >
            <!-- Name & Hex swatch -->
            <div class="flex items-center gap-2 flex-1 min-w-[160px]">
              <input
                v-model="color.hex_code"
                type="color"
                class="w-9 h-9 rounded-lg cursor-pointer bg-transparent border border-slate-500/80 p-0.5 flex-shrink-0"
                title="Rang tanlash"
              />
              <input
                v-model="color.name"
                type="text"
                placeholder="Variant nomi (masalan: Original, Analog)"
                class="form-input bg-slate-600 border-slate-500 text-white text-xs sm:text-sm py-1.5 flex-1"
              />
            </div>

            <!-- Price input & Delta badge -->
            <div class="flex items-center gap-2 w-full sm:w-auto">
              <div class="relative flex-1 sm:w-44">
                <input
                  v-model.number="color.price"
                  @input="onColorPriceInput(color)"
                  type="number"
                  step="1000"
                  min="0"
                  placeholder="Rang narxi (so'm)"
                  class="form-input bg-slate-600 border-slate-500 text-white text-xs sm:text-sm py-1.5 w-full pr-12"
                />
                <span class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[10px] text-slate-400 font-medium">so'm</span>
              </div>

              <!-- Price diff indicator -->
              <span
                class="text-[11px] px-2 py-1 rounded-md font-medium whitespace-nowrap min-w-[70px] text-center"
                :class="colorDiffClass(color)"
              >
                {{ colorDiffLabel(color) }}
              </span>

              <!-- Delete -->
              <button
                type="button"
                @click="removeColor(i)"
                class="p-2 text-slate-400 hover:text-red-400 rounded-lg hover:bg-red-950/30 flex-shrink-0"
                title="O'chirish"
              >
                <X class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <button
          type="button"
          @click="addColor"
          class="btn-sm btn-outline border-slate-600 text-slate-300 hover:bg-slate-700"
          id="add-color-btn"
        >
          <Plus class="w-4 h-4" /> Variant qo'shish
        </button>
      </div>

      <!-- Submit -->
      <div class="flex flex-col sm:flex-row gap-3 pt-2">
        <button type="submit" :disabled="submitting" class="btn-md sm:btn-lg btn-primary justify-center" id="product-form-submit">
          <span v-if="!submitting">{{ isEdit ? 'Saqlash' : 'Mahsulot qo\'shish' }}</span>
          <div v-else class="spinner" />
        </button>
        <router-link to="/admin/products" class="btn-md sm:btn-lg bg-slate-700 hover:bg-slate-600 text-white border border-slate-600 justify-center text-center">Bekor qilish</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ChevronLeft, Plus, X, ImagePlus, Star, Trash2 } from '@lucide/vue'
import { adminApi } from '@/api/admin'
import { productsApi } from '@/api/products'
import { useAlertStore } from '@/stores/alert'

const route = useRoute()
const router = useRouter()
const alertStore = useAlertStore()

const isEdit = computed(() => !!route.params.id && route.params.id !== 'new')
const categories = ref([])
const submitting = ref(false)

const existingImages = ref([])
const uploadFiles = ref([])
const fileInputRef = ref(null)
const deletedColorIds = ref([])

const form = ref({
  name: '', description: '', category: '', quality: 'original',
  base_price: '', badge: '', car_models: [],
  brand: '', article: '', warranty: '6 oy', usage: '',
  stock: 0, is_active: true, colors: [],
})
const carModels = ref([])

const showNewCat = ref(false)
const newCatName = ref('')
const addingCat = ref(false)
const newCarName = ref('')
const addingCar = ref(false)

async function quickAddCategory() {
  const name = newCatName.value.trim()
  if (!name || addingCat.value) return
  addingCat.value = true
  try {
    const fd = new FormData()
    fd.append('name', name)
    const res = await adminApi.createCategory(fd)
    categories.value.push(res.data)
    form.value.category = res.data.id
    newCatName.value = ''
    showNewCat.value = false
    alertStore.success("Kategoriya qo'shildi")
  } catch (e) {
    const d = e.response?.data
    alertStore.error((Array.isArray(d?.name) ? d.name[0] : d?.name) || 'Kategoriya qo\'shib bo\'lmadi')
  }
  addingCat.value = false
}

async function quickAddCar() {
  const name = newCarName.value.trim()
  if (!name || addingCar.value) return
  addingCar.value = true
  try {
    const res = await adminApi.createCarModel({ name })
    carModels.value.push(res.data)
    form.value.car_models.push(res.data.id)
    newCarName.value = ''
    alertStore.success("Mashina turi qo'shildi")
  } catch (e) {
    const d = e.response?.data
    alertStore.error((Array.isArray(d?.name) ? d.name[0] : d?.name) || 'Mashina qo\'shib bo\'lmadi')
  }
  addingCar.value = false
}

function toggleCar(id) {
  const i = form.value.car_models.indexOf(id)
  if (i >= 0) form.value.car_models.splice(i, 1)
  else form.value.car_models.push(id)
}

function addColor() {
  const base = form.value.base_price ? Number(form.value.base_price) : 0
  form.value.colors.push({
    name: '',
    hex_code: '#FFFFFF',
    price: base || null,
    price_modifier: 0,
    is_available: true,
  })
}

function removeColor(index) {
  const color = form.value.colors[index]
  if (color && color.id) {
    deletedColorIds.value.push(color.id)
  }
  form.value.colors.splice(index, 1)
}

function onColorPriceInput(color) {
  if (color.price !== null && color.price !== undefined && form.value.base_price) {
    color.price_modifier = Number(color.price) - Number(form.value.base_price)
  }
}

function colorDiffLabel(color) {
  const base = Number(form.value.base_price) || 0
  const p = color.price !== null && color.price !== undefined ? Number(color.price) : (base + Number(color.price_modifier || 0))
  const diff = p - base
  if (diff === 0) return 'Baza narx'
  if (diff > 0) return `+${new Intl.NumberFormat('uz-UZ').format(diff)}`
  return `${new Intl.NumberFormat('uz-UZ').format(diff)}`
}

function colorDiffClass(color) {
  const base = Number(form.value.base_price) || 0
  const p = color.price !== null && color.price !== undefined ? Number(color.price) : (base + Number(color.price_modifier || 0))
  const diff = p - base
  if (diff === 0) return 'bg-slate-600/60 text-slate-300'
  if (diff > 0) return 'bg-amber-500/20 text-amber-300'
  return 'bg-emerald-500/20 text-emerald-300'
}

function handleFileSelect(e) {
  const files = Array.from(e.target.files || [])
  for (const file of files) {
    if (!file.type.startsWith('image/')) continue
    uploadFiles.value.push({
      file,
      preview: URL.createObjectURL(file),
    })
  }
  e.target.value = ''
}

async function setMainImage(img) {
  try {
    await adminApi.setProductMainImage(savedProductId(), img.id)
    existingImages.value.forEach(i => i.is_main = false)
    img.is_main = true
    alertStore.success('Asosiy rasm o\'rnatildi')
  } catch {
    alertStore.error('Xatolik yuz berdi')
  }
}

async function removeExistingImage(img) {
  try {
    await adminApi.deleteProductImage(savedProductId(), img.id)
    existingImages.value = existingImages.value.filter(i => i.id !== img.id)
    alertStore.success('Rasm o\'chirildi')
  } catch {
    alertStore.error('Xatolik yuz berdi')
  }
}

function savedProductId() {
  return isEdit.value ? route.params.id : null
}

async function submit() {
  submitting.value = true
  try {
    const data = { ...form.value, price_type: 'fixed', stock: Math.max(0, Number(form.value.stock) || 0) }
    delete data.colors

    let savedProduct
    if (isEdit.value) {
      const res = await adminApi.updateProduct(route.params.id, data)
      savedProduct = res.data
    } else {
      const res = await adminApi.createProduct(data)
      savedProduct = res.data
    }

    // 1. O'chirilgan ranglarni bazadan o'chirish
    for (const delId of deletedColorIds.value) {
      try {
        await adminApi.deleteProductColor(savedProduct.id, delId)
      } catch (e) {
        console.error('Delete color failed:', e)
      }
    }

    // 2. Yangi va mavjud ranglarni saqlash / yangilash
    for (const color of form.value.colors) {
      if (!color.name) continue
      const base = Number(form.value.base_price) || 0
      const colorPrice = color.price !== null && color.price !== undefined
        ? Number(color.price)
        : (base + Number(color.price_modifier || 0))
      const modifier = colorPrice - base

      const payload = {
        name: color.name,
        hex_code: color.hex_code || '#FFFFFF',
        price: colorPrice,
        price_modifier: modifier,
        is_available: color.is_available ?? true,
      }

      try {
        if (color.id) {
          await adminApi.updateProductColor(savedProduct.id, color.id, payload)
        } else {
          await adminApi.addProductColor(savedProduct.id, payload)
        }
      } catch (e) {
        console.error('Color save error:', e)
      }
    }

    // Yangi rasmlarni yuklash
    const hasExistingMain = existingImages.value.some(i => i.is_main)
    for (let i = 0; i < uploadFiles.value.length; i++) {
      const item = uploadFiles.value[i]
      const imgData = new FormData()
      imgData.append('image', item.file)
      imgData.append('is_main', (!hasExistingMain && i === 0) ? 'true' : 'false')
      await adminApi.addProductImage(savedProduct.id, imgData)
      URL.revokeObjectURL(item.preview)
    }

    alertStore.success(isEdit.value ? 'Mahsulot yangilandi!' : 'Mahsulot qo\'shildi!')
    router.push('/admin/products')
  } catch (err) {
    alertStore.error(err.response?.data?.detail || 'Xatolik yuz berdi')
  }
  submitting.value = false
}

onMounted(async () => {
  const res = await productsApi.getCategories()
  categories.value = res.data.results || res.data
  try {
    const carsRes = await productsApi.getCarModels()
    carModels.value = carsRes.data.results || carsRes.data
  } catch {}

  if (isEdit.value) {
    try {
      const productRes = await adminApi.getProduct(route.params.id)
      const p = productRes.data
      existingImages.value = p.images || []

      const loadedColors = (p.colors || []).map(c => {
        const base = Number(p.base_price) || 0
        const price = c.price !== null && c.price !== undefined
          ? Number(c.price)
          : (c.calculated_price !== undefined ? Number(c.calculated_price) : (base + Number(c.price_modifier || 0)))
        return {
          ...c,
          price,
          price_modifier: price - base,
        }
      })

      form.value = {
        name: p.name, description: p.description, category: p.category?.id ?? p.category,
        quality: p.quality || '', base_price: p.base_price, badge: p.badge || '',
        car_models: (p.car_models || []).map(c => c.id),
        brand: p.brand || '', article: p.article || '', warranty: p.warranty || '', usage: p.usage || '',
        stock: p.stock ?? 0, is_active: p.is_active, colors: loadedColors,
      }
    } catch { alertStore.error('Mahsulot topilmadi') }
  }
})
</script>
