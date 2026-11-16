<template>
  <div class="min-h-screen page-shell">

    <!-- Page Header -->
    <div class="nav-glass px-4 pt-4 pb-3">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-3">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-white">{{ t('catalog_title') }}</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ t('catalog_sub') }}</p>
        </div>
        <!-- Prominent Live Search in Catalog -->
        <div class="w-full sm:w-80">
          <LiveSearch
            :placeholder="t('catalog_search_ph')"
            min-dropdown-width="340"
            @search-submit="onCatalogSearchSubmit"
          />
        </div>
      </div>

      <!-- Mobile Filter Chips Row -->
      <div class="flex items-center gap-2 mt-3 overflow-x-auto scrollbar-hide -mx-4 px-4 pb-1">
        <!-- Filter Toggle -->
        <button
          @click="showMobileFilters = true"
          class="flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-sm font-medium transition-colors"
          :class="hasActiveFilters ? 'border-brand-500 bg-brand-50 dark:bg-brand-500/15 text-brand-700 dark:text-brand-400' : 'border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300'"
        >
          <Filter class="w-3.5 h-3.5" />
          {{ t('catalog_filter') }}
          <span v-if="hasActiveFilters" class="w-4 h-4 bg-brand-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">!</span>
        </button>

        <!-- Sort -->
        <button
          @click="showSortMenu = !showSortMenu"
          class="flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 text-sm font-medium"
        >
          <ArrowUpDown class="w-3.5 h-3.5" />
          {{ t('catalog_sort') }}
        </button>

        <!-- Category Quick Chips -->
        <button
          class="flex-shrink-0 px-3 py-1.5 rounded-full text-sm font-medium transition-colors"
          :class="!filters.category ? 'bg-brand-600 text-white' : 'border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300'"
          @click="setCategory('')"
        >{{ t('common_all') }}</button>
        <button
          v-for="cat in categories.slice(0, 5)"
          :key="cat.slug"
          @click="setCategory(cat.slug)"
          class="flex-shrink-0 px-3 py-1.5 rounded-full text-sm font-medium transition-colors whitespace-nowrap"
          :class="filters.category === cat.slug ? 'bg-brand-600 text-white' : 'border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300'"
        >{{ categoryName(cat) }}</button>
      </div>

      <!-- Sort Dropdown -->
      <Transition name="fade">
        <div v-if="showSortMenu" class="mt-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-lg p-1">
          <button
            v-for="opt in sortOptions"
            :key="opt.value"
            @click="filters.ordering = opt.value; fetchProducts(true); showSortMenu = false"
            class="block w-full text-left px-4 py-2.5 rounded-lg text-sm font-medium transition-colors"
            :class="filters.ordering === opt.value ? 'bg-brand-50 dark:bg-brand-500/15 text-brand-700 dark:text-brand-400' : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700'"
          >{{ opt.label }}</button>
        </div>
      </Transition>
    </div>

    <!-- Active Filters -->
    <div v-if="hasActiveFilters" class="flex items-center gap-2 px-4 py-2 bg-white dark:bg-slate-900 border-b border-slate-100 dark:border-slate-700 overflow-x-auto scrollbar-hide">
      <span v-if="filters.search" class="flex items-center gap-1 px-2.5 py-1 bg-slate-100 dark:bg-slate-700 rounded-full text-xs text-slate-700 dark:text-slate-200">
        "{{ filters.search }}"
        <button @click="filters.search = ''; fetchProducts(true)"><X class="w-3 h-3" /></button>
      </span>
      <span v-if="filters.category" class="flex items-center gap-1 px-2.5 py-1 bg-brand-50 dark:bg-brand-500/15 text-brand-700 dark:text-brand-400 rounded-full text-xs">
        {{ categories.find(c => c.slug === filters.category)?.name }}
        <button @click="setCategory('')"><X class="w-3 h-3" /></button>
      </span>
      <span v-if="filters.car" class="flex items-center gap-1 px-2.5 py-1 bg-slate-100 dark:bg-slate-700 rounded-full text-xs text-slate-700 dark:text-slate-200">
        {{ carModels.find(c => c.value === filters.car)?.label }}
        <button @click="toggleFilter('car', '')"><X class="w-3 h-3" /></button>
      </span>
      <button @click="resetFilters" class="flex-shrink-0 text-xs text-red-500 underline ml-auto">{{ t('catalog_reset') }}</button>
    </div>

    <!-- Content -->
    <div class="p-4">

      <!-- Desktop Sidebar + Grid layout -->
      <div class="hidden lg:flex gap-8">
        <!-- Desktop Sidebar -->
        <aside class="w-64 flex-shrink-0">
          <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-100 dark:border-slate-700 p-6 sticky top-24">
            <div class="flex items-center justify-between mb-5">
              <h2 class="font-bold text-slate-900 dark:text-white text-base">{{ t('catalog_filters') }}</h2>
              <button v-if="hasActiveFilters" @click="resetFilters" class="text-xs text-brand-600 dark:text-brand-400 font-medium">{{ t('catalog_reset') }}</button>
            </div>
            <!-- Categories -->
            <div class="mb-5">
              <p class="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">{{ t('catalog_product_type') }}</p>
              <div class="space-y-1.5">
                <label v-for="cat in categories" :key="cat.slug" class="flex items-center gap-3 cursor-pointer group py-0.5">
                  <div class="w-4 h-4 rounded border flex items-center justify-center transition-colors flex-shrink-0"
                       :class="filters.category === cat.slug ? 'bg-brand-600 border-brand-600' : 'border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700'">
                    <Check v-if="filters.category === cat.slug" class="w-2.5 h-2.5 text-white" />
                  </div>
                  <span class="text-sm text-slate-600 dark:text-slate-300 group-hover:text-slate-900 dark:group-hover:text-white">{{ categoryName(cat) }}</span>
                  <input type="checkbox" class="hidden" :checked="filters.category === cat.slug" @change="setCategory(cat.slug)" />
                </label>
              </div>
            </div>
            <div class="h-px bg-slate-100 dark:bg-slate-700 my-4" />
            <!-- Mashina turi -->
            <div class="mb-5">
              <p class="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">{{ t('catalog_car_type') }}</p>
              <div class="space-y-1.5">
                <label v-for="mat in carModels" :key="mat.value" class="flex items-center gap-3 cursor-pointer group py-0.5">
                  <div class="w-4 h-4 rounded border flex items-center justify-center transition-colors flex-shrink-0"
                       :class="filters.car === mat.value ? 'bg-brand-600 border-brand-600' : 'border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700'">
                    <Check v-if="filters.car === mat.value" class="w-2.5 h-2.5 text-white" />
                  </div>
                  <span class="text-sm text-slate-600 dark:text-slate-300 group-hover:text-slate-900 dark:group-hover:text-white">{{ mat.label }}</span>
                  <input type="checkbox" class="hidden" :checked="filters.car === mat.value" @change="toggleFilter('car', mat.value)" />
                </label>
              </div>
            </div>
            <!-- Sort Desktop -->
            <div class="h-px bg-slate-100 dark:bg-slate-700 my-4" />
            <div>
              <p class="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">{{ t('catalog_sort') }}</p>
              <select v-model="filters.ordering" @change="fetchProducts(true)" class="w-full text-sm border border-slate-200 dark:border-slate-600 rounded-lg px-3 py-2 text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-brand-400">
                <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
              </select>
            </div>
          </div>
        </aside>

        <!-- Desktop Products Grid -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between mb-5 text-sm text-slate-500 dark:text-slate-400">
            <span><strong class="text-slate-900 dark:text-white">{{ totalCount }}</strong> {{ t('catalog_items_count') }}</span>
          </div>
          <div v-if="loading" class="grid grid-cols-2 xl:grid-cols-3 gap-5">
            <div v-for="i in 9" :key="i" class="skeleton rounded-2xl h-80" />
          </div>
          <div v-else-if="!products.length" class="text-center py-20">
            <div class="w-20 h-20 bg-slate-100 dark:bg-slate-700 rounded-full flex items-center justify-center mx-auto mb-4">
              <Package class="w-10 h-10 text-slate-300 dark:text-slate-500" />
            </div>
            <h3 class="text-xl font-bold text-slate-700 dark:text-slate-200 mb-2">{{ t('catalog_no_results') }}</h3>
            <p class="text-slate-500 dark:text-slate-400 mb-5">{{ t('catalog_no_results_sub') }}</p>
            <button @click="resetFilters" class="btn-md btn-outline">{{ t('catalog_reset') }}</button>
          </div>
          <div v-else class="grid grid-cols-2 xl:grid-cols-3 gap-5">
            <ProductCard v-for="product in products" :key="product.id" :product="product" />
          </div>
          <!-- Pagination (desktop) -->
          <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-10">
            <button @click="setPage(page - 1)" :disabled="page <= 1" class="btn-md btn-secondary"><ChevronLeft class="w-4 h-4" /></button>
            <button v-for="p in visiblePages" :key="p" @click="setPage(p)"
              class="w-10 h-10 rounded-xl text-sm font-medium transition-all"
              :class="p === page ? 'bg-brand-500 text-white' : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-600'">
              {{ p }}
            </button>
            <button @click="setPage(page + 1)" :disabled="page >= totalPages" class="btn-md btn-secondary"><ChevronRight class="w-4 h-4" /></button>
          </div>
        </div>
      </div>

      <!-- Mobile Products Grid -->
      <div class="lg:hidden">
        <!-- Loading -->
        <div v-if="loading" class="grid grid-cols-2 gap-3">
          <div v-for="i in 6" :key="i" class="skeleton rounded-xl h-64" />
        </div>

        <!-- Empty -->
        <div v-else-if="!products.length" class="text-center py-20">
          <div class="w-16 h-16 bg-slate-100 dark:bg-slate-700 rounded-full flex items-center justify-center mx-auto mb-4">
            <Package class="w-8 h-8 text-slate-300 dark:text-slate-500" />
          </div>
          <h3 class="font-bold text-slate-700 dark:text-slate-200 mb-2">{{ t('catalog_no_results') }}</h3>
          <p class="text-slate-500 dark:text-slate-400 text-sm mb-4">{{ t('catalog_no_results_sub') }}</p>
          <button @click="resetFilters" class="btn-sm btn-outline">{{ t('catalog_reset') }}</button>
        </div>

        <!-- Mobile Grid -->
        <div v-else class="grid grid-cols-2 gap-3">
          <div
            v-for="product in products"
            :key="product.id"
            class="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 overflow-hidden"
          >
            <!-- Image -->
            <div
              class="relative bg-slate-50 dark:bg-slate-900 aspect-[4/3] flex items-center justify-center p-3 cursor-pointer"
              @click="$router.push(`/product/${product.slug}`)"
            >
              <img
                :src="product.main_image || '/no-image.svg'"
                :alt="product.name"
                class="max-w-full max-h-full object-contain"
                loading="lazy"
              />
              <div v-if="product.badge" class="absolute top-2 left-2 px-1.5 py-0.5 bg-brand-500 text-white text-[9px] font-bold rounded uppercase">{{ product.badge }}</div>
            </div>
            <!-- Info -->
            <div class="p-3">
              <p class="text-[9px] font-semibold text-slate-400 uppercase tracking-wider mb-0.5">{{ categoryName(product.category_name) }}</p>
              <p class="text-sm font-bold text-slate-900 dark:text-white line-clamp-2 leading-snug mb-1">{{ product.name }}</p>
              <div class="flex items-baseline justify-between mb-2">
                <span class="text-xs font-bold text-brand-700 dark:text-brand-400">
                  {{ formatPrice(product.min_price || product.base_price) }}
                </span>
                <span class="text-[10px] text-slate-400">{{ t('common_per_piece') }}</span>
              </div>
              <router-link
                :to="`/product/${product.slug}`"
                class="block w-full text-center py-2 btn-primary text-white text-xs font-semibold rounded-lg transition-colors"
              >
                {{ t('common_details') }}
              </router-link>
            </div>
          </div>
        </div>

        <!-- Mobile Load More -->
        <div v-if="page < totalPages" class="mt-6 text-center">
          <button @click="loadMore" :disabled="loading" class="btn-md btn-outline w-full">
            <span v-if="!loading">{{ t('catalog_load_more') }}</span>
            <div v-else class="spinner" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Filter Sheet (Bottom Drawer) -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showMobileFilters" class="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm" @click.self="showMobileFilters = false">
          <Transition name="slide-up">
            <div v-if="showMobileFilters" class="absolute bottom-0 left-0 right-0 bg-white dark:bg-slate-800 rounded-t-2xl max-h-[80vh] overflow-y-auto">
              <div class="sticky top-0 bg-white dark:bg-slate-800 flex items-center justify-between px-5 py-4 border-b border-slate-100 dark:border-slate-700">
                <h3 class="font-bold text-slate-900 dark:text-white text-base">{{ t('catalog_filters') }}</h3>
                <div class="flex items-center gap-3">
                  <button v-if="hasActiveFilters" @click="resetFilters" class="text-sm text-red-500 font-medium">{{ t('catalog_reset') }}</button>
                  <button @click="showMobileFilters = false" class="p-1.5 rounded-xl bg-slate-100 dark:bg-slate-700"><X class="w-4 h-4 text-slate-600 dark:text-slate-300" /></button>
                </div>
              </div>
              <div class="p-5 space-y-6">
                <!-- Categories -->
                <div>
                  <p class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">{{ t('catalog_product_type') }}</p>
                  <div class="flex flex-wrap gap-2">
                    <button
                      @click="setCategory('')"
                      class="px-3 py-1.5 rounded-full text-sm font-medium transition-colors border"
                      :class="!filters.category ? 'bg-brand-600 text-white border-brand-600' : 'border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-300'"
                    >{{ t('common_all') }}</button>
                    <button
                      v-for="cat in categories"
                      :key="cat.slug"
                      @click="setCategory(cat.slug)"
                      class="px-3 py-1.5 rounded-full text-sm font-medium transition-colors border"
                      :class="filters.category === cat.slug ? 'bg-brand-600 text-white border-brand-600' : 'border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-300'"
                    >{{ categoryName(cat) }}</button>
                  </div>
                </div>
                <!-- Mashina turi -->
                <div>
                  <p class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">{{ t('catalog_car_type') }}</p>
                  <div class="flex flex-wrap gap-2">
                    <button
                      v-for="mat in carModels"
                      :key="mat.value"
                      @click="toggleFilter('car', mat.value)"
                      class="px-3 py-1.5 rounded-full text-sm font-medium transition-colors border"
                      :class="filters.car === mat.value ? 'bg-brand-600 text-white border-brand-600' : 'border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-300'"
                    >{{ mat.label }}</button>
                  </div>
                </div>
                <!-- Sort -->
                <div>
                  <p class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">{{ t('catalog_sort') }}</p>
                  <div class="space-y-1">
                    <button
                      v-for="opt in sortOptions"
                      :key="opt.value"
                      @click="filters.ordering = opt.value; fetchProducts(true)"
                      class="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
                      :class="filters.ordering === opt.value ? 'bg-brand-50 dark:bg-brand-500/15 text-brand-700 dark:text-brand-400' : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700'"
                    >
                      <div class="w-4 h-4 rounded-full border-2 flex items-center justify-center flex-shrink-0"
                           :class="filters.ordering === opt.value ? 'border-brand-600' : 'border-slate-300 dark:border-slate-600'">
                        <div v-if="filters.ordering === opt.value" class="w-2 h-2 rounded-full bg-brand-600" />
                      </div>
                      {{ opt.label }}
                    </button>
                  </div>
                </div>
                <button @click="showMobileFilters = false" class="btn-lg btn-primary w-full">
                  {{ t('catalog_show_results') }} ({{ totalCount }})
                </button>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Filter, ArrowUpDown, X, Package, ChevronLeft, ChevronRight, Check } from '@lucide/vue'
import { productsApi } from '@/api/products'
import ProductCard from '@/components/client/ProductCard.vue'
import LiveSearch from '@/components/client/LiveSearch.vue'
import { useI18n } from '@/i18n'

const { t, categoryName } = useI18n()
const route  = useRoute()
const router = useRouter()

const products    = ref([])
const categories  = ref([])
const loading     = ref(true)
const totalCount  = ref(0)
const page        = ref(1)
const pageSize    = 12

const showMobileFilters = ref(false)
const showSortMenu      = ref(false)

const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))
const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, page.value - 2)
  const end   = Math.min(totalPages.value, page.value + 2)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

const filters = ref({
  search:   route.query.search || '',
  category: route.query.category || '',
  car:      route.query.car || '',
  ordering: '-created_at',
})

// Watch route changes to update search/category in catalog automatically
watch(
  () => route.query,
  (newQuery) => {
    filters.value.search   = newQuery.search || ''
    filters.value.category = newQuery.category || ''
    filters.value.car      = newQuery.car || ''
    fetchProducts(true)
  }
)

function onCatalogSearchSubmit(q) {
  filters.value.search = q
  router.replace({ query: { ...route.query, search: q || undefined } })
}

const hasActiveFilters = computed(() =>
  filters.value.category || filters.value.car || filters.value.search
)

const carModels = ref([])

const sortOptions = computed(() => [
  { label: t('catalog_sort_new'),       value: '-created_at' },
  { label: t('catalog_sort_cheap'),     value: 'base_price' },
  { label: t('catalog_sort_expensive'), value: '-base_price' },
])

async function fetchProducts(reset = false) {
  if (reset) page.value = 1
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize, ordering: filters.value.ordering }
    if (filters.value.search)   params.search   = filters.value.search
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.car) params.car = filters.value.car
    const res = await productsApi.getProducts(params)
    products.value  = res.data.results || res.data
    totalCount.value = res.data.count || products.value.length
  } catch {}
  loading.value = false
}

async function loadMore() {
  if (page.value >= totalPages.value) return
  page.value++
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize, ordering: filters.value.ordering }
    if (filters.value.search)   params.search   = filters.value.search
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.car) params.car = filters.value.car
    const res = await productsApi.getProducts(params)
    products.value.push(...(res.data.results || []))
    totalCount.value = res.data.count || products.value.length
  } catch {}
  loading.value = false
}

function setCategory(slug) {
  filters.value.category = filters.value.category === slug ? '' : slug
  fetchProducts(true)
}

function toggleFilter(key, value) {
  filters.value[key] = filters.value[key] === value ? '' : value
  fetchProducts(true)
}

function resetFilters() {
  filters.value = { search: '', category: '', car: '', ordering: '-created_at' }
  fetchProducts(true)
  showMobileFilters.value = false
}

function setPage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function formatPrice(p) {
  if (!p && p !== 0) return '—'
  return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(p)
}

onMounted(async () => {
  const catsRes = await productsApi.getCategories()
  categories.value = catsRes.data.results || catsRes.data
  try {
    const carsRes = await productsApi.getCarModels()
    carModels.value = (carsRes.data.results || carsRes.data).map(c => ({ label: c.name, value: c.slug }))
  } catch {}
  await fetchProducts()
})
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }

.slide-up-enter-active, .slide-up-leave-active { transition: transform 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); }
</style>
