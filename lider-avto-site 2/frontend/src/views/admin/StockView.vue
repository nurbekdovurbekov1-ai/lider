<template>
  <div class="space-y-5 max-w-full overflow-hidden">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-white">Ombor</h1>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">Har bir mahsulotdan nechta dona qolgani</p>
      </div>
    </div>

    <!-- Summary cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <button @click="setFilter('')" class="text-left bg-slate-800/90 border rounded-2xl p-4 transition-colors"
        :class="filter === '' ? 'border-brand-500' : 'border-slate-700/80 hover:border-slate-600'">
        <div class="flex items-center gap-2 text-slate-400 text-xs"><Package class="w-4 h-4" /> Jami dona</div>
        <p class="text-2xl font-bold text-white mt-1">{{ summary.total_units ?? '—' }}</p>
        <p class="text-[11px] text-slate-500">{{ summary.total_products ?? 0 }} ta mahsulot</p>
      </button>
      <button @click="setFilter('ok')" class="text-left bg-slate-800/90 border rounded-2xl p-4 transition-colors"
        :class="filter === 'ok' ? 'border-emerald-500' : 'border-slate-700/80 hover:border-slate-600'">
        <div class="flex items-center gap-2 text-emerald-400 text-xs"><CheckCircle class="w-4 h-4" /> Yetarli</div>
        <p class="text-2xl font-bold text-white mt-1">{{ summary.ok ?? '—' }}</p>
        <p class="text-[11px] text-slate-500">{{ (summary.threshold ?? 5) + 1 }} dona va undan ko'p</p>
      </button>
      <button @click="setFilter('low')" class="text-left bg-slate-800/90 border rounded-2xl p-4 transition-colors"
        :class="filter === 'low' ? 'border-amber-500' : 'border-slate-700/80 hover:border-slate-600'">
        <div class="flex items-center gap-2 text-amber-400 text-xs"><AlertTriangle class="w-4 h-4" /> Kam qolgan</div>
        <p class="text-2xl font-bold text-white mt-1">{{ summary.low ?? '—' }}</p>
        <p class="text-[11px] text-slate-500">1–{{ summary.threshold ?? 5 }} dona</p>
      </button>
      <button @click="setFilter('out')" class="text-left bg-slate-800/90 border rounded-2xl p-4 transition-colors"
        :class="filter === 'out' ? 'border-red-500' : 'border-slate-700/80 hover:border-slate-600'">
        <div class="flex items-center gap-2 text-red-400 text-xs"><X class="w-4 h-4" /> Tugagan</div>
        <p class="text-2xl font-bold text-white mt-1">{{ summary.out ?? '—' }}</p>
        <p class="text-[11px] text-slate-500">0 dona</p>
      </button>
    </div>

    <!-- Toolbar -->
    <div class="bg-slate-800/90 rounded-2xl p-3 sm:p-4 border border-slate-700/80 flex flex-col sm:flex-row gap-3">
      <div class="flex-1 relative">
        <input v-model="search" @input="debounceFetch" type="text" placeholder="Mahsulot nomi, brend yoki artikul..."
          class="bg-slate-700/80 text-slate-200 placeholder-slate-400 border border-slate-600 rounded-xl px-4 py-2.5 pl-10 w-full text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
      </div>
      <select v-model="filterCategory" @change="reload"
        class="bg-slate-700/80 text-slate-300 border border-slate-600 rounded-xl px-4 py-2.5 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 w-full sm:w-auto min-w-[180px]">
        <option value="">Barcha kategoriyalar</option>
        <option v-for="cat in categories" :key="cat.slug" :value="cat.slug">{{ cat.name }}</option>
      </select>
    </div>

    <!-- Table -->
    <div class="bg-slate-800/90 rounded-2xl border border-slate-700/80 overflow-hidden shadow-sm">
      <div v-if="loading" class="p-4 sm:p-6 space-y-3">
        <div v-for="i in 6" :key="i" class="skeleton h-14 rounded-xl bg-slate-700" />
      </div>

      <div v-else-if="!products.length" class="py-16 text-center px-4">
        <Building2 class="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p class="text-slate-400 text-sm">Mahsulotlar topilmadi</p>
      </div>

      <div v-else class="overflow-x-auto w-full">
        <table class="w-full text-sm text-left min-w-[640px]">
          <thead class="bg-slate-900/60 border-b border-slate-700/80">
            <tr>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Mahsulot</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Kategoriya</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Holat</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Qoldiq (dona)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700/60">
            <tr v-for="p in products" :key="p.id" class="hover:bg-slate-700/40 transition-colors">
              <td class="px-4 py-3">
                <div class="flex items-center gap-3 min-w-0">
                  <img :src="mainImage(p)" :alt="p.name" class="w-10 h-10 rounded-xl object-cover bg-slate-700 flex-shrink-0" />
                  <div class="min-w-0">
                    <p class="font-semibold text-white truncate max-w-[220px]">{{ p.name }}</p>
                    <p class="text-xs text-slate-400 truncate max-w-[220px]">{{ p.brand || p.article || '—' }}</p>
                  </div>
                </div>
              </td>
              <td class="px-4 py-3 text-slate-300 whitespace-nowrap">{{ p.category_name }}</td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span class="badge text-[10px] font-semibold" :class="levelClass(p.stock)">{{ levelText(p.stock) }}</span>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center gap-1.5">
                  <button @click="step(p, -1)" :disabled="p.stock <= 0 || p._saving"
                    class="w-8 h-8 rounded-lg bg-slate-700 hover:bg-slate-600 text-white disabled:opacity-40 flex items-center justify-center" title="Kamaytirish">
                    <span class="text-lg leading-none">−</span>
                  </button>
                  <input
                    v-model.number="p._edit" type="number" min="0"
                    @keyup.enter="saveStock(p)" @blur="saveStock(p)"
                    class="w-20 text-center bg-slate-700/80 text-white border border-slate-600 rounded-lg py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                  />
                  <button @click="step(p, 1)" :disabled="p._saving"
                    class="w-8 h-8 rounded-lg bg-slate-700 hover:bg-slate-600 text-white disabled:opacity-40 flex items-center justify-center" title="Ko'paytirish">
                    <Plus class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 p-3.5 sm:p-4 border-t border-slate-700/80 bg-slate-900/40">
        <button @click="setPage(page - 1)" :disabled="page <= 1" class="px-3 py-1.5 rounded-lg bg-slate-700 text-slate-300 hover:bg-slate-600 disabled:opacity-40 text-xs sm:text-sm">‹ Oldingi</button>
        <span class="text-slate-400 text-xs sm:text-sm px-2">{{ page }} / {{ totalPages }}</span>
        <button @click="setPage(page + 1)" :disabled="page >= totalPages" class="px-3 py-1.5 rounded-lg bg-slate-700 text-slate-300 hover:bg-slate-600 disabled:opacity-40 text-xs sm:text-sm">Keyingi ›</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, Building2, Package, CheckCircle, AlertTriangle, X, Plus } from '@lucide/vue'
import { adminApi } from '@/api/admin'
import { productsApi } from '@/api/products'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()
const products = ref([])
const categories = ref([])
const summary = ref({})
const loading = ref(true)
const search = ref('')
const filterCategory = ref('')
const filter = ref('')
const page = ref(1)
const pageSize = 20
const totalCount = ref(0)
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))

function mainImage(p) {
  const img = p.images?.find(i => i.is_main) || p.images?.[0]
  return img?.image || '/no-image.svg'
}
function levelClass(n) { return n <= 0 ? 'badge-red' : (n <= (summary.value.threshold ?? 5) ? 'badge-amber' : 'badge-green') }
function levelText(n) { return n <= 0 ? 'Tugagan' : (n <= (summary.value.threshold ?? 5) ? 'Kam qoldi' : 'Yetarli') }

async function fetchSummary() {
  try { summary.value = (await adminApi.getStockSummary()).data } catch {}
}

async function fetchProducts() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize }
    if (search.value) params.search = search.value
    if (filterCategory.value) params.category = filterCategory.value
    if (filter.value) params.stock_status = filter.value
    const res = await adminApi.getProducts(params)
    const list = res.data.results || res.data
    products.value = list.map(p => ({ ...p, _edit: p.stock, _saving: false }))
    totalCount.value = res.data.count || products.value.length
  } catch {
    alertStore.error("Mahsulotlarni yuklab bo'lmadi")
  }
  loading.value = false
}

function reload() { page.value = 1; fetchProducts() }
function setFilter(v) { filter.value = v; reload() }
function setPage(p) { page.value = p; fetchProducts() }

let timer
function debounceFetch() { clearTimeout(timer); timer = setTimeout(reload, 400) }

function step(p, d) {
  p._edit = Math.max(0, (Number(p._edit) || 0) + d)
  saveStock(p)
}

async function saveStock(p) {
  const val = Math.max(0, Math.floor(Number(p._edit) || 0))
  p._edit = val
  if (val === p.stock || p._saving) return
  p._saving = true
  try {
    await adminApi.updateProduct(p.id, { stock: val })
    p.stock = val
    fetchSummary()
  } catch {
    p._edit = p.stock
    alertStore.error("Qoldiqni saqlab bo'lmadi")
  }
  p._saving = false
}

onMounted(async () => {
  try {
    const cats = await productsApi.getCategories()
    categories.value = cats.data.results || cats.data
  } catch {}
  fetchSummary()
  fetchProducts()
})
</script>
