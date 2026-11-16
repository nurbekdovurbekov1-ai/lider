<template>
  <div class="space-y-5 max-w-full overflow-hidden">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-white">Kategoriyalar</h1>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">{{ categories.length }} ta kategoriya</p>
      </div>
      <button @click="openCreate" class="btn-sm sm:btn-md btn-primary shadow-sm">
        <Plus class="w-4 h-4" /> <span>Yangi kategoriya</span>
      </button>
    </div>

    <!-- Search -->
    <div class="bg-slate-800/90 rounded-2xl p-3 sm:p-4 border border-slate-700/80">
      <div class="relative">
        <input
          v-model="search"
          type="text"
          placeholder="Kategoriya nomi..."
          class="bg-slate-700/80 text-slate-200 placeholder-slate-400 border border-slate-600 rounded-xl px-4 py-2.5 pl-10 w-full text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
      </div>
    </div>

    <!-- List -->
    <div class="bg-slate-800/90 rounded-2xl border border-slate-700/80 overflow-hidden shadow-sm">
      <div v-if="loading" class="p-4 sm:p-6 space-y-3">
        <div v-for="i in 5" :key="i" class="skeleton h-14 rounded-xl bg-slate-700" />
      </div>

      <div v-else-if="!filtered.length" class="py-16 text-center px-4">
        <Grid class="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p class="text-slate-400 text-sm mb-4">Kategoriyalar topilmadi</p>
        <button @click="openCreate" class="btn-md btn-primary">Kategoriya qo'shish</button>
      </div>

      <div v-else class="overflow-x-auto w-full">
        <table class="w-full text-sm text-left min-w-[560px]">
          <thead class="bg-slate-900/60 border-b border-slate-700/80">
            <tr>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Kategoriya</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Slug</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Tartib</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Mahsulotlar</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Holat</th>
              <th class="px-4 py-3" />
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700/60">
            <tr v-for="cat in filtered" :key="cat.id" class="hover:bg-slate-700/40 transition-colors">
              <td class="px-4 py-3">
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-10 h-10 rounded-xl bg-slate-700 border border-slate-600 flex items-center justify-center overflow-hidden flex-shrink-0">
                    <img v-if="cat.icon" :src="cat.icon" :alt="cat.name" class="w-full h-full object-cover" />
                    <Grid v-else class="w-4 h-4 text-slate-400" />
                  </div>
                  <span class="font-medium text-white truncate">{{ cat.name }}</span>
                </div>
              </td>
              <td class="px-4 py-3 text-slate-400 text-xs">{{ cat.slug }}</td>
              <td class="px-4 py-3 text-slate-300">{{ cat.order }}</td>
              <td class="px-4 py-3 text-slate-300">{{ cat.products_count }}</td>
              <td class="px-4 py-3">
                <span :class="cat.is_active ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-600/40 text-slate-400'" class="px-2.5 py-1 rounded-lg text-xs font-medium">
                  {{ cat.is_active ? 'Faol' : 'Nofaol' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center justify-end gap-1">
                  <button @click="openEdit(cat)" class="p-2 text-slate-400 hover:text-brand-400 hover:bg-slate-700 rounded-xl transition-colors" title="Tahrirlash">
                    <Pencil class="w-4 h-4" />
                  </button>
                  <button @click="askDelete(cat)" class="p-2 text-slate-400 hover:text-red-400 hover:bg-red-950/40 rounded-xl transition-colors" title="O'chirish">
                    <Trash2 class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add / Edit Modal -->
    <Transition name="modal">
      <div v-if="modal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm" @click.self="closeModal">
        <div class="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-w-md w-full p-5 sm:p-6 text-white max-h-[92vh] overflow-y-auto">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold">{{ modal.editId ? 'Kategoriyani tahrirlash' : 'Yangi kategoriya' }}</h3>
            <button @click="closeModal" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800"><X class="w-5 h-5" /></button>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-xs text-slate-400 mb-1.5">Nomi *</label>
              <input v-model="form.name" type="text" placeholder="Masalan: Tormoz"
                class="bg-slate-800 text-slate-200 placeholder-slate-500 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                :class="errors.name ? 'border-red-500' : ''" />
              <p v-if="errors.name" class="text-xs text-red-400 mt-1">{{ errors.name }}</p>
            </div>

            <div>
              <label class="block text-xs text-slate-400 mb-1.5">Slug <span class="text-slate-500">(bo'sh qoldirsangiz avtomatik)</span></label>
              <input v-model="form.slug" type="text" placeholder="tormoz"
                class="bg-slate-800 text-slate-200 placeholder-slate-500 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                :class="errors.slug ? 'border-red-500' : ''" />
              <p v-if="errors.slug" class="text-xs text-red-400 mt-1">{{ errors.slug }}</p>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs text-slate-400 mb-1.5">Tartib raqami</label>
                <input v-model.number="form.order" type="number" min="0"
                  class="bg-slate-800 text-slate-200 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1.5">Holat</label>
                <select v-model="form.is_active"
                  class="bg-slate-800 text-slate-200 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500">
                  <option :value="true">Faol</option>
                  <option :value="false">Nofaol</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block text-xs text-slate-400 mb-1.5">Ikonka / rasm</label>
              <div class="flex items-center gap-3">
                <div class="w-14 h-14 rounded-xl bg-slate-800 border border-slate-600 flex items-center justify-center overflow-hidden flex-shrink-0">
                  <img v-if="iconPreview" :src="iconPreview" class="w-full h-full object-cover" />
                  <ImagePlus v-else class="w-5 h-5 text-slate-500" />
                </div>
                <div class="flex flex-col gap-1.5 min-w-0">
                  <label class="btn-sm bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700 cursor-pointer inline-flex w-fit">
                    Rasm tanlash
                    <input type="file" accept="image/*" class="hidden" @change="onIconPick" />
                  </label>
                  <button v-if="iconPreview" type="button" @click="clearIcon" class="text-xs text-red-400 hover:text-red-300 text-left w-fit">Rasmni olib tashlash</button>
                </div>
              </div>
              <p v-if="errors.icon" class="text-xs text-red-400 mt-1">{{ errors.icon }}</p>
            </div>
          </div>

          <div class="flex gap-3 mt-6">
            <button @click="closeModal" class="flex-1 btn-md bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700">Bekor qilish</button>
            <button @click="save" :disabled="saving" class="flex-1 btn-md btn-primary disabled:opacity-60">
              {{ saving ? 'Saqlanmoqda...' : 'Saqlash' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Delete Confirm -->
    <Transition name="modal">
      <div v-if="confirmModal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
        <div class="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-w-sm w-full p-6 text-white">
          <div class="w-12 h-12 bg-red-500/15 rounded-2xl flex items-center justify-center mb-4 mx-auto">
            <AlertCircle class="w-6 h-6 text-red-400" />
          </div>
          <h3 class="text-lg font-bold text-center mb-2">Kategoriyani o'chirish</h3>
          <p class="text-slate-400 text-center text-xs sm:text-sm mb-1">
            <b class="text-white">{{ confirmModal.cat?.name }}</b> kategoriyasini o'chirishni tasdiqlaysizmi?
          </p>
          <p v-if="confirmModal.cat?.products_count" class="text-amber-400 text-center text-xs mb-5">
            Bu kategoriyadagi {{ confirmModal.cat.products_count }} ta mahsulot o'chmaydi, lekin kategoriyasiz qoladi.
          </p>
          <div v-else class="mb-5" />
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
import { ref, computed, onMounted } from 'vue'
import { Plus, Search, Grid, Pencil, Trash2, X, AlertCircle, ImagePlus } from '@lucide/vue'
import { adminApi } from '@/api/admin'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()
const categories = ref([])
const loading = ref(true)
const search = ref('')
const saving = ref(false)

const modal = ref({ show: false, editId: null })
const confirmModal = ref({ show: false, cat: null })
const form = ref({ name: '', slug: '', order: 0, is_active: true })
const errors = ref({})
const iconFile = ref(null)
const iconPreview = ref('')
const removeIcon = ref(false)

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  return q ? categories.value.filter(c => c.name.toLowerCase().includes(q)) : categories.value
})

async function fetchCategories() {
  loading.value = true
  try {
    const res = await adminApi.getCategories()
    categories.value = res.data.results || res.data
  } catch {
    alertStore.error("Kategoriyalarni yuklab bo'lmadi")
  }
  loading.value = false
}

function resetForm() {
  form.value = { name: '', slug: '', order: 0, is_active: true }
  errors.value = {}
  iconFile.value = null
  iconPreview.value = ''
  removeIcon.value = false
}

function openCreate() {
  resetForm()
  const maxOrder = categories.value.reduce((m, c) => Math.max(m, c.order || 0), 0)
  form.value.order = categories.value.length ? maxOrder + 1 : 0
  modal.value = { show: true, editId: null }
}

function openEdit(cat) {
  resetForm()
  form.value = { name: cat.name, slug: cat.slug, order: cat.order, is_active: cat.is_active }
  iconPreview.value = cat.icon || ''
  modal.value = { show: true, editId: cat.id }
}

function closeModal() {
  modal.value.show = false
}

function onIconPick(e) {
  const file = e.target.files?.[0]
  if (!file) return
  iconFile.value = file
  iconPreview.value = URL.createObjectURL(file)
  removeIcon.value = false
}

function clearIcon() {
  iconFile.value = null
  iconPreview.value = ''
  removeIcon.value = true
}

function firstError(v) {
  return Array.isArray(v) ? v[0] : v
}

async function save() {
  errors.value = {}
  if (!form.value.name.trim()) {
    errors.value.name = 'Nomini kiriting'
    return
  }

  const fd = new FormData()
  fd.append('name', form.value.name.trim())
  fd.append('slug', (form.value.slug || '').trim())
  fd.append('order', form.value.order ?? 0)
  fd.append('is_active', form.value.is_active ? 'true' : 'false')
  if (iconFile.value) fd.append('icon', iconFile.value)
  if (removeIcon.value && !iconFile.value) fd.append('remove_icon', 'true')

  saving.value = true
  try {
    if (modal.value.editId) {
      await adminApi.updateCategory(modal.value.editId, fd)
      alertStore.success('Kategoriya yangilandi')
    } else {
      await adminApi.createCategory(fd)
      alertStore.success("Kategoriya qo'shildi")
    }
    modal.value.show = false
    await fetchCategories()
  } catch (e) {
    const data = e.response?.data
    if (data && typeof data === 'object') {
      for (const k of ['name', 'slug', 'icon']) if (data[k]) errors.value[k] = firstError(data[k])
    }
    if (!Object.keys(errors.value).length) alertStore.error('Xatolik yuz berdi')
  }
  saving.value = false
}

function askDelete(cat) {
  confirmModal.value = { show: true, cat }
}

async function confirmDelete() {
  const cat = confirmModal.value.cat
  try {
    await adminApi.deleteCategory(cat.id)
    categories.value = categories.value.filter(c => c.id !== cat.id)
    alertStore.info("Kategoriya o'chirildi")
  } catch {
    alertStore.error("O'chirib bo'lmadi")
  }
  confirmModal.value.show = false
}

onMounted(fetchCategories)
</script>
