<template>
  <div class="space-y-5 max-w-full overflow-hidden">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-white">Bannerlar</h1>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">Bosh sahifadagi katta rasm. Tartibi eng kichik faol banner ko'rsatiladi.</p>
      </div>
      <button @click="openCreate" class="btn-sm sm:btn-md btn-primary shadow-sm">
        <Plus class="w-4 h-4" /> <span>Yangi banner</span>
      </button>
    </div>

    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="i in 2" :key="i" class="skeleton h-56 rounded-2xl bg-slate-800" />
    </div>

    <div v-else-if="!banners.length" class="text-center py-16 bg-slate-800/80 rounded-2xl border border-slate-700/80">
      <ImagePlus class="w-12 h-12 text-slate-600 mx-auto mb-3" />
      <p class="text-slate-400 text-sm mb-4">Hali banner yo'q</p>
      <button @click="openCreate" class="btn-md btn-primary">Banner qo'shish</button>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="b in banners" :key="b.id" class="bg-slate-800/90 rounded-2xl border border-slate-700/80 overflow-hidden shadow-sm">
        <div class="relative h-40 bg-slate-700">
          <img v-if="b.image" :src="b.image" :alt="b.title" class="w-full h-full object-cover" @error="onImgError(b)" />
          <div v-if="!b.image || b._broken" class="absolute inset-0 flex items-center justify-center text-xs text-red-300 bg-slate-900/70 px-4 text-center">
            Rasm yuklanmadi. Backend DJANGO_DEBUG=1 bilan ishlayotganini tekshiring.
          </div>
          <span class="absolute top-2 left-2 text-[11px] px-2 py-1 rounded-lg font-medium"
            :class="b.is_active ? 'bg-emerald-500/90 text-white' : 'bg-slate-900/80 text-slate-300'">
            {{ b.is_active ? 'Faol' : 'Nofaol' }}
          </span>
          <span class="absolute top-2 right-2 text-[11px] px-2 py-1 rounded-lg bg-slate-900/80 text-slate-200">Tartib: {{ b.order }}</span>
        </div>
        <div class="p-4">
          <p class="font-semibold text-white truncate">{{ b.title }}</p>
          <p v-if="b.subtitle" class="text-xs text-slate-400 truncate mt-0.5">{{ b.subtitle }}</p>
          <div class="flex items-center justify-between mt-3 gap-2">
            <button @click="toggleActive(b)" class="px-3 py-1.5 rounded-xl text-xs font-medium bg-slate-700/80 text-slate-200 hover:bg-slate-700">
              {{ b.is_active ? "O'chirib qo'yish" : 'Yoqish' }}
            </button>
            <div class="flex items-center gap-1">
              <button @click="openEdit(b)" class="p-2 text-slate-400 hover:text-brand-400 hover:bg-slate-700 rounded-xl" title="Tahrirlash"><Pencil class="w-4 h-4" /></button>
              <button @click="confirmModal = { show: true, banner: b }" class="p-2 text-slate-400 hover:text-red-400 hover:bg-red-950/40 rounded-xl" title="O'chirish"><Trash2 class="w-4 h-4" /></button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add / Edit -->
    <Transition name="modal">
      <div v-if="modal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm" @click.self="modal.show = false">
        <div class="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-w-lg w-full p-5 sm:p-6 text-white max-h-[92vh] overflow-y-auto">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold">{{ modal.editId ? 'Bannerni tahrirlash' : 'Yangi banner' }}</h3>
            <button @click="modal.show = false" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800"><X class="w-5 h-5" /></button>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-xs text-slate-400 mb-1.5">Banner rasmi {{ modal.editId ? '' : '*' }}</label>
              <div class="rounded-xl bg-slate-800 border border-slate-600 overflow-hidden h-40 flex items-center justify-center mb-2">
                <img v-if="preview" :src="preview" class="w-full h-full object-cover" />
                <ImagePlus v-else class="w-8 h-8 text-slate-500" />
              </div>
              <label class="btn-sm bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700 cursor-pointer inline-flex w-fit">
                Rasm tanlash
                <input type="file" accept="image/*" class="hidden" @change="onPick" />
              </label>
              <p v-if="errors.image" class="text-xs text-red-400 mt-1">{{ errors.image }}</p>
            </div>

            <div>
              <label class="block text-xs text-slate-400 mb-1.5">Sarlavha *</label>
              <input v-model="form.title" type="text" class="bg-slate-800 text-slate-200 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
              <p v-if="errors.title" class="text-xs text-red-400 mt-1">{{ errors.title }}</p>
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1.5">Pastki sarlavha</label>
              <input v-model="form.subtitle" type="text" class="bg-slate-800 text-slate-200 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs text-slate-400 mb-1.5">Tugma matni</label>
                <input v-model="form.button_text" type="text" placeholder="Katalogni ko'rish" class="bg-slate-800 text-slate-200 placeholder-slate-500 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1.5">Tugma havolasi</label>
                <input v-model="form.button_url" type="text" placeholder="/catalog" class="bg-slate-800 text-slate-200 placeholder-slate-500 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1.5">Tartib raqami</label>
                <input v-model.number="form.order" type="number" min="0" class="bg-slate-800 text-slate-200 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1.5">Holat</label>
                <select v-model="form.is_active" class="bg-slate-800 text-slate-200 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500">
                  <option :value="true">Faol</option>
                  <option :value="false">Nofaol</option>
                </select>
              </div>
            </div>
          </div>

          <div class="flex gap-3 mt-6">
            <button @click="modal.show = false" class="flex-1 btn-md bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700">Bekor qilish</button>
            <button @click="save" :disabled="saving" class="flex-1 btn-md btn-primary disabled:opacity-60">{{ saving ? 'Saqlanmoqda...' : 'Saqlash' }}</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Delete -->
    <Transition name="modal">
      <div v-if="confirmModal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
        <div class="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-w-sm w-full p-6 text-white">
          <div class="w-12 h-12 bg-red-500/15 rounded-2xl flex items-center justify-center mb-4 mx-auto"><AlertCircle class="w-6 h-6 text-red-400" /></div>
          <h3 class="text-lg font-bold text-center mb-2">Bannerni o'chirish</h3>
          <p class="text-slate-400 text-center text-xs sm:text-sm mb-6"><b class="text-white">{{ confirmModal.banner?.title }}</b> bannerini o'chirishni tasdiqlaysizmi?</p>
          <div class="flex gap-3">
            <button @click="confirmModal.show = false" class="flex-1 btn-md bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700">Bekor qilish</button>
            <button @click="confirmDelete" class="flex-1 btn-md btn-danger">O'chirish</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Pencil, Trash2, X, AlertCircle, ImagePlus } from '@lucide/vue'
import { adminApi } from '@/api/admin'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()
const banners = ref([])
const loading = ref(true)
const saving = ref(false)
const modal = ref({ show: false, editId: null })
const confirmModal = ref({ show: false, banner: null })
const form = ref({ title: '', subtitle: '', button_text: '', button_url: '', order: 0, is_active: true })
const errors = ref({})
const imageFile = ref(null)
const preview = ref('')

async function fetchBanners() {
  loading.value = true
  try {
    const res = await adminApi.getBanners()
    banners.value = (res.data.results || res.data).map(b => ({ ...b, _broken: false }))
  } catch {
    alertStore.error("Bannerlarni yuklab bo'lmadi")
  }
  loading.value = false
}

function onImgError(b) { b._broken = true }

function resetForm() {
  form.value = { title: '', subtitle: '', button_text: '', button_url: '', order: 0, is_active: true }
  errors.value = {}
  imageFile.value = null
  preview.value = ''
}

function openCreate() {
  resetForm()
  form.value.order = banners.value.length
  modal.value = { show: true, editId: null }
}

function openEdit(b) {
  resetForm()
  form.value = {
    title: b.title, subtitle: b.subtitle || '', button_text: b.button_text || '',
    button_url: b.button_url || '', order: b.order, is_active: b.is_active,
  }
  preview.value = b.image || ''
  modal.value = { show: true, editId: b.id }
}

function onPick(e) {
  const file = e.target.files?.[0]
  if (!file) return
  imageFile.value = file
  preview.value = URL.createObjectURL(file)
}

function firstError(v) { return Array.isArray(v) ? v[0] : v }

async function save() {
  errors.value = {}
  if (!form.value.title.trim()) { errors.value.title = 'Sarlavhani kiriting'; return }
  if (!modal.value.editId && !imageFile.value) { errors.value.image = 'Rasm tanlang'; return }

  const fd = new FormData()
  fd.append('title', form.value.title.trim())
  fd.append('subtitle', form.value.subtitle || '')
  fd.append('button_text', form.value.button_text || '')
  fd.append('button_url', form.value.button_url || '')
  fd.append('order', form.value.order ?? 0)
  fd.append('is_active', form.value.is_active ? 'true' : 'false')
  if (imageFile.value) fd.append('image', imageFile.value)

  saving.value = true
  try {
    if (modal.value.editId) {
      await adminApi.updateBanner(modal.value.editId, fd)
      alertStore.success('Banner yangilandi')
    } else {
      await adminApi.createBanner(fd)
      alertStore.success("Banner qo'shildi")
    }
    modal.value.show = false
    await fetchBanners()
  } catch (e) {
    const d = e.response?.data
    if (d && typeof d === 'object') {
      for (const k of ['title', 'image']) if (d[k]) errors.value[k] = firstError(d[k])
    }
    if (!Object.keys(errors.value).length) alertStore.error('Xatolik yuz berdi')
  }
  saving.value = false
}

async function toggleActive(b) {
  const fd = new FormData()
  fd.append('is_active', b.is_active ? 'false' : 'true')
  try {
    await adminApi.updateBanner(b.id, fd)
    b.is_active = !b.is_active
  } catch { alertStore.error('Xatolik yuz berdi') }
}

async function confirmDelete() {
  const b = confirmModal.value.banner
  try {
    await adminApi.deleteBanner(b.id)
    banners.value = banners.value.filter(x => x.id !== b.id)
    alertStore.info("Banner o'chirildi")
  } catch { alertStore.error("O'chirib bo'lmadi") }
  confirmModal.value.show = false
}

onMounted(fetchBanners)
</script>
