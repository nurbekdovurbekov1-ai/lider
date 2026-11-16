<template>
  <div class="space-y-5 max-w-full overflow-hidden">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-white">Mashina turlari</h1>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">{{ carModels.length }} ta mashina turi (Nexia, Lacetti, Cobalt ...)</p>
      </div>
      <button @click="openCreate" class="btn-sm sm:btn-md btn-primary shadow-sm">
        <Plus class="w-4 h-4" /> <span>Yangi mashina</span>
      </button>
    </div>

    <!-- Search -->
    <div class="bg-slate-800/90 rounded-2xl p-3 sm:p-4 border border-slate-700/80">
      <div class="relative">
        <input
          v-model="search"
          type="text"
          placeholder="Mashina nomi..."
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
        <Truck class="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p class="text-slate-400 text-sm mb-4">Mashina turlari topilmadi</p>
        <button @click="openCreate" class="btn-md btn-primary">Mashina qo'shish</button>
      </div>

      <div v-else class="overflow-x-auto w-full">
        <table class="w-full text-sm text-left min-w-[520px]">
          <thead class="bg-slate-900/60 border-b border-slate-700/80">
            <tr>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Mashina</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Slug</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Tartib</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Mahsulotlar</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Holat</th>
              <th class="px-4 py-3" />
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700/60">
            <tr v-for="car in filtered" :key="car.id" class="hover:bg-slate-700/40 transition-colors">
              <td class="px-4 py-3">
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-10 h-10 rounded-xl bg-slate-700 border border-slate-600 flex items-center justify-center flex-shrink-0">
                    <Truck class="w-4 h-4 text-slate-400" />
                  </div>
                  <span class="font-medium text-white truncate">{{ car.name }}</span>
                </div>
              </td>
              <td class="px-4 py-3 text-slate-400 text-xs">{{ car.slug }}</td>
              <td class="px-4 py-3 text-slate-300">{{ car.order }}</td>
              <td class="px-4 py-3 text-slate-300">{{ car.products_count }}</td>
              <td class="px-4 py-3">
                <span :class="car.is_active ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-600/40 text-slate-400'" class="px-2.5 py-1 rounded-lg text-xs font-medium">
                  {{ car.is_active ? 'Faol' : 'Nofaol' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center justify-end gap-1">
                  <button @click="openEdit(car)" class="p-2 text-slate-400 hover:text-brand-400 hover:bg-slate-700 rounded-xl transition-colors" title="Tahrirlash">
                    <Pencil class="w-4 h-4" />
                  </button>
                  <button @click="askDelete(car)" class="p-2 text-slate-400 hover:text-red-400 hover:bg-red-950/40 rounded-xl transition-colors" title="O'chirish">
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
            <h3 class="text-lg font-bold">{{ modal.editId ? 'Mashinani tahrirlash' : 'Yangi mashina turi' }}</h3>
            <button @click="closeModal" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800"><X class="w-5 h-5" /></button>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-xs text-slate-400 mb-1.5">Mashina nomi *</label>
              <input v-model="form.name" type="text" placeholder="Masalan: Nexia 3"
                class="bg-slate-800 text-slate-200 placeholder-slate-500 border border-slate-600 rounded-xl px-4 py-2.5 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                :class="errors.name ? 'border-red-500' : ''" />
              <p v-if="errors.name" class="text-xs text-red-400 mt-1">{{ errors.name }}</p>
            </div>

            <div>
              <label class="block text-xs text-slate-400 mb-1.5">Slug <span class="text-slate-500">(bo'sh qoldirsangiz avtomatik)</span></label>
              <input v-model="form.slug" type="text" placeholder="nexia-3"
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
          <h3 class="text-lg font-bold text-center mb-2">Mashina turini o'chirish</h3>
          <p class="text-slate-400 text-center text-xs sm:text-sm mb-1">
            <b class="text-white">{{ confirmModal.car?.name }}</b> ni o'chirishni tasdiqlaysizmi?
          </p>
          <p v-if="confirmModal.car?.products_count" class="text-amber-400 text-center text-xs mb-5">
            {{ confirmModal.car.products_count }} ta mahsulot o'chmaydi, faqat shu mashinaga bog'liqligi olib tashlanadi.
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
import { Plus, Search, Truck, Pencil, Trash2, X, AlertCircle } from '@lucide/vue'
import { adminApi } from '@/api/admin'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()
const carModels = ref([])
const loading = ref(true)
const search = ref('')
const saving = ref(false)

const modal = ref({ show: false, editId: null })
const confirmModal = ref({ show: false, car: null })
const form = ref({ name: '', slug: '', order: 0, is_active: true })
const errors = ref({})

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  return q ? carModels.value.filter(c => c.name.toLowerCase().includes(q)) : carModels.value
})

async function fetchCarModels() {
  loading.value = true
  try {
    const res = await adminApi.getCarModels()
    carModels.value = res.data.results || res.data
  } catch {
    alertStore.error("Mashina turlarini yuklab bo'lmadi")
  }
  loading.value = false
}

function openCreate() {
  const maxOrder = carModels.value.reduce((m, c) => Math.max(m, c.order || 0), 0)
  form.value = { name: '', slug: '', order: carModels.value.length ? maxOrder + 1 : 0, is_active: true }
  errors.value = {}
  modal.value = { show: true, editId: null }
}

function openEdit(car) {
  form.value = { name: car.name, slug: car.slug, order: car.order, is_active: car.is_active }
  errors.value = {}
  modal.value = { show: true, editId: car.id }
}

function closeModal() {
  modal.value.show = false
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

  const payload = {
    name: form.value.name.trim(),
    slug: (form.value.slug || '').trim(),
    order: form.value.order ?? 0,
    is_active: form.value.is_active,
  }

  saving.value = true
  try {
    if (modal.value.editId) {
      await adminApi.updateCarModel(modal.value.editId, payload)
      alertStore.success('Mashina turi yangilandi')
    } else {
      await adminApi.createCarModel(payload)
      alertStore.success("Mashina turi qo'shildi")
    }
    modal.value.show = false
    await fetchCarModels()
  } catch (e) {
    const data = e.response?.data
    if (data && typeof data === 'object') {
      for (const k of ['name', 'slug']) if (data[k]) errors.value[k] = firstError(data[k])
    }
    if (!Object.keys(errors.value).length) alertStore.error('Xatolik yuz berdi')
  }
  saving.value = false
}

function askDelete(car) {
  confirmModal.value = { show: true, car }
}

async function confirmDelete() {
  const car = confirmModal.value.car
  try {
    await adminApi.deleteCarModel(car.id)
    carModels.value = carModels.value.filter(c => c.id !== car.id)
    alertStore.info("Mashina turi o'chirildi")
  } catch {
    alertStore.error("O'chirib bo'lmadi")
  }
  confirmModal.value.show = false
}

onMounted(fetchCarModels)
</script>
