<template>
  <div class="min-h-screen page-shell">
    <!-- Loading State -->
    <div v-if="loading" class="container-custom py-20">
      <div class="flex flex-col items-center justify-center gap-6">
        <div class="spinner-lg" />
        <p class="text-slate-500 dark:text-slate-400">{{ t('common_loading') }}</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="!product" class="container-custom py-20 text-center">
      <Package class="w-16 h-16 text-slate-300 mx-auto mb-4" />
      <h2 class="text-2xl font-bold text-slate-700 dark:text-slate-200 mb-3">{{ t('product_not_found') }}</h2>
      <router-link to="/catalog" class="btn-md btn-primary">{{ t('product_back_catalog') }}</router-link>
    </div>

    <template v-else>
      <!-- Breadcrumb -->
      <div class="nav-glass">
        <div class="container-custom py-4">
          <div class="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
            <router-link to="/" class="hover:text-brand-600 dark:hover:text-brand-400">{{ t('nav_home') }}</router-link>
            <ChevronRight class="w-4 h-4" />
            <router-link to="/catalog" class="hover:text-brand-600 dark:hover:text-brand-400">{{ t('nav_catalog') }}</router-link>
            <ChevronRight class="w-4 h-4" />
            <span class="text-slate-900 dark:text-white font-medium truncate max-w-xs">{{ product.name }}</span>
          </div>
        </div>
      </div>

      <div class="container-custom py-10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">

          <!-- ===== IMAGE GALLERY ===== -->
          <div class="space-y-4">
            <!-- Main Image -->
            <div class="relative rounded-3xl overflow-hidden product-media aspect-[4/3]">
              <img
                :src="selectedImage"
                :alt="product.name"
                class="w-full h-full object-cover transition-all duration-500"
                @error="handleImgError"
              />
              <div v-if="product.badge" class="absolute top-4 left-4">
                <span class="badge badge-new px-3 py-1.5 text-sm">{{ ({ new: t('product_badge_new'), hit: t('product_badge_hit'), sale: t('product_badge_sale') })[product.badge] || product.badge }}</span>
              </div>
            </div>

            <!-- Thumbnails -->
            <div v-if="product.images?.length > 1" class="flex gap-3 overflow-x-auto pb-1">
              <button
                v-for="img in product.images"
                :key="img.id"
                @click="selectedImage = img.image"
                class="w-20 h-20 rounded-xl overflow-hidden flex-shrink-0 border-2 transition-all duration-200"
                :class="selectedImage === img.image ? 'border-brand-500 shadow-md' : 'border-slate-200 dark:border-slate-600 hover:border-slate-300 dark:hover:border-slate-500'"
              >
                <img :src="img.image" :alt="product.name" class="w-full h-full object-cover" />
              </button>
            </div>
          </div>

          <!-- ===== PRODUCT INFO & CALCULATOR ===== -->
          <div class="space-y-6">
            <div>
              <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">{{ categoryName(product.category_name) }}</p>
              <h1 class="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-2">{{ product.name }}</h1>
              <p v-if="product.brand || product.article" class="text-sm text-slate-500 dark:text-slate-400 mb-3">
                <span v-if="product.brand">{{ t('product_brand') }} <b class="text-slate-800 dark:text-slate-200">{{ product.brand }}</b></span>
                <span v-if="product.brand && product.article"> · </span>
                <span v-if="product.article">{{ t('product_article') }} <b class="text-slate-800 dark:text-slate-200">{{ product.article }}</b></span>
              </p>
              
              <!-- Color-based Price Display -->
              <div class="flex items-baseline gap-3 mb-6 flex-wrap">
                <p class="text-3xl font-extrabold text-brand-600">
                  {{ formatPrice(currentColorPrice) }}
                  <span class="text-sm font-medium text-slate-400">{{ t('common_per_piece') }}</span>
                </p>
                <span v-if="selectedColor" class="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-600">
                  {{ selectedColor.name }}
                </span>
              </div>
            </div>

            <!-- MOS MASHINALAR -->
            <div v-if="product.car_models?.length">
              <p class="text-sm font-bold text-slate-900 dark:text-white mb-2">{{ t('product_compatible') }}</p>
              <div class="flex flex-wrap gap-2">
                <router-link
                  v-for="c in product.car_models"
                  :key="c.id"
                  :to="`/catalog?car=${c.slug}`"
                  class="px-3 py-1.5 rounded-full text-xs font-semibold bg-brand-50 dark:bg-brand-500/15 text-brand-700 dark:text-brand-400 hover:bg-brand-100 dark:hover:bg-brand-500/25 transition-colors"
                >{{ c.name }}</router-link>
              </div>
            </div>

            <!-- MIQDOR VA SAVAT -->
            <div class="space-y-6">
              
              <!-- Color Selection -->
              <div v-if="colors.length">
                <div class="flex items-center justify-between mb-2.5">
                  <p class="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <svg class="w-4 h-4 text-brand-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path></svg>
                    {{ t('product_select_variant') }}
                  </p>
                  <span class="text-xs font-semibold text-slate-700">
                    {{ selectedColor?.name }}
                  </span>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                  <button
                    v-for="color in colors"
                    :key="color.id"
                    type="button"
                    @click="selectColor(color)"
                    class="flex items-center gap-2.5 p-2.5 rounded-xl border-2 text-left transition-all relative overflow-hidden"
                    :class="selectedColor?.id === color.id
                      ? 'border-brand-600 bg-brand-50/50 dark:bg-brand-500/10 shadow-xs'
                      : 'border-slate-200 dark:border-slate-600 hover:border-slate-300 dark:hover:border-slate-500 bg-white dark:bg-slate-800'"
                  >
                    <div
                      class="w-6 h-6 rounded-full border border-slate-300 dark:border-slate-600 flex-shrink-0 shadow-xs"
                      :style="{ backgroundColor: color.hex_code }"
                    />
                    <div class="min-w-0 flex-1">
                      <p class="text-xs font-bold text-slate-900 dark:text-white truncate">{{ color.name }}</p>
                      <p class="text-[11px] font-semibold text-brand-600 truncate">
                        {{ formatPrice(color.calculated_price ?? color.price ?? (Number(product.base_price) + Number(color.price_modifier || 0))) }}
                      </p>
                    </div>
                    <div v-if="selectedColor?.id === color.id" class="w-2 h-2 rounded-full bg-brand-600 flex-shrink-0" />
                  </button>
                </div>
              </div>

              <!-- Quantity -->
              <div>
                <label class="block text-xs font-bold text-slate-900 dark:text-white mb-2">{{ t('product_quantity') }}</label>
                <div class="inline-flex items-center bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 rounded-lg">
                  <button @click="qty > 1 ? qty-- : null" class="w-10 h-10 flex items-center justify-center text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors">−</button>
                  <span class="w-12 text-center text-sm font-semibold text-slate-900 dark:text-white">{{ qty }}</span>
                  <button @click="qty++" class="w-10 h-10 flex items-center justify-center text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors">+</button>
                </div>
              </div>

              <!-- Jami narx -->
              <div class="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-600 rounded-2xl p-4">
                <div class="flex items-baseline justify-between">
                  <span class="text-sm font-bold text-slate-900 dark:text-white">{{ t('product_total_price') }} ({{ qty }} {{ t('cart_qty') }}):</span>
                  <span class="text-2xl font-extrabold text-brand-600">{{ formatPrice(currentColorPrice * qty) }}</span>
                </div>
              </div>

              <!-- Buttons -->
              <div class="flex flex-col gap-3 pt-2">
                <button
                  @click="addToCart"
                  :disabled="addingToCart || product.status === 'out_of_stock'"
                  class="w-full btn-md btn-primary text-white font-medium uppercase tracking-wider text-sm py-3.5 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
                >
                  <ShoppingCart class="w-4 h-4" />
                  <span v-if="!addingToCart">{{ t('product_add_to_cart') }}</span>
                  <span v-else>{{ t('product_adding') }}</span>
                </button>

                <a href="/#contact" class="w-full btn-md bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 font-medium uppercase tracking-wider text-sm py-3.5 rounded-lg flex items-center justify-center gap-2 transition-colors">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                  {{ t('home_cta_btn') }}
                </a>
              </div>

            </div>
          </div>
        </div>

        <!-- Accordions Section -->
        <div class="max-w-3xl space-y-4">
          <!-- Description Accordion -->
          <details class="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 group">
            <summary class="flex justify-between items-center font-bold text-slate-900 dark:text-white p-5 cursor-pointer list-none">
              {{ t('product_about') }}
              <ChevronRight class="w-4 h-4 text-slate-400 group-open:rotate-90 transition-transform" />
            </summary>
            <div class="p-5 pt-0 text-slate-600 dark:text-slate-300 text-sm leading-relaxed">
              {{ product.description }}
            </div>
          </details>

          <!-- Specs Accordion -->
          <details class="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 group" open>
            <summary class="flex justify-between items-center font-bold text-slate-900 dark:text-white p-5 cursor-pointer list-none border-b border-slate-100 dark:border-slate-700">
              {{ t('product_specs_title') }}
              <ChevronRight class="w-4 h-4 text-slate-400 group-open:rotate-90 transition-transform" />
            </summary>
            <div class="p-5">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
                <div v-for="row in specRows" :key="row.label" class="flex justify-between border-b border-slate-100 dark:border-slate-700 border-dashed pb-2">
                  <span class="text-xs text-slate-500 dark:text-slate-400">{{ row.label }}</span>
                  <span class="text-xs font-semibold text-slate-900 dark:text-white">{{ row.value }}</span>
                </div>
              </div>
            </div>
          </details>

          <details class="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 group">
            <summary class="flex justify-between items-center font-bold text-slate-900 dark:text-white p-5 cursor-pointer list-none">
              {{ t('product_usage_title') }}
              <ChevronRight class="w-4 h-4 text-slate-400 group-open:rotate-90 transition-transform" />
            </summary>
            <div class="p-5 pt-0 text-slate-600 dark:text-slate-300 text-sm leading-relaxed">
              {{ product.usage || t('product_usage_fallback') }}
            </div>
          </details>

          <details class="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 group">
            <summary class="flex justify-between items-center font-bold text-slate-900 dark:text-white p-5 cursor-pointer list-none">
              {{ t('product_delivery_title') }}
              <ChevronRight class="w-4 h-4 text-slate-400 group-open:rotate-90 transition-transform" />
            </summary>
            <div class="p-5 pt-0 text-slate-600 dark:text-slate-300 text-sm">
              {{ product.delivery_info || t('product_delivery_info') }} {{ t('product_delivery_free') }}
            </div>
          </details>
        </div>
      </div>
    </template>

    <!-- Auth Modal -->
    <AuthModal :open="authModalOpen" @close="authModalOpen = false" @success="authModalOpen = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronRight, ShoppingCart, Check, Package } from '@lucide/vue'
import { productsApi } from '@/api/products'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useAlertStore } from '@/stores/alert'
import { useSiteStore } from '@/stores/site'
import { useI18n } from '@/i18n'
import AuthModal from '@/components/client/AuthModal.vue'

const { t, categoryName } = useI18n()
const route = useRoute()
const cartStore = useCartStore()
const authStore = useAuthStore()
const alertStore = useAlertStore()
const siteStore = useSiteStore()

const product = ref(null)
const colors = ref([])
const loading = ref(true)
const selectedColor = ref(null)
const selectedImage = ref(null)
const qty = ref(1)
const addingToCart = ref(false)
const authModalOpen = ref(false)

const specRows = computed(() => {
  const p = product.value || {}
  return [
    { label: 'Brend', value: p.brand },
    { label: 'Artikul', value: p.article },
    { label: 'Sifat turi', value: p.quality_display },
    { label: 'Kategoriya', value: categoryName(p.category_name) },
    { label: 'Kafolat', value: p.warranty },
  ].filter(r => r.value)
})

function handleImgError(e) {
  e.target.src = '/no-image.svg'
}

const currentColorPrice = computed(() => {
  if (selectedColor.value) {
    if (selectedColor.value.price !== null && selectedColor.value.price !== undefined) {
      return Number(selectedColor.value.price)
    }
    if (selectedColor.value.calculated_price !== undefined) {
      return Number(selectedColor.value.calculated_price)
    }
    return (Number(product.value?.base_price) || 0) + (Number(selectedColor.value.price_modifier) || 0)
  }
  return Number(product.value?.base_price) || 0
})

function formatPrice(price) {
  if (!price && price !== 0) return '—'
  return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(price)
}

function selectColor(color) {
  selectedColor.value = color
}

async function addToCart() {
  if (!authStore.isLoggedIn) { authModalOpen.value = true; return }
    addingToCart.value = true
  const result = await cartStore.addItem({
    product_id: product.value.id,
    color_id: selectedColor.value ? selectedColor.value.id : null,
    width_mm: 1000,
    height_mm: 1000,
    quantity: qty.value,
  })
  addingToCart.value = false
  if (result.success) {
    alertStore.success(t('product_added_success'))
  } else {
    alertStore.error(t('product_error'))
  }
}

function openAuthModal() {
  authModalOpen.value = true
}

onMounted(async () => {
  siteStore.fetchSettings()
  const slug = route.params.slug
  try {
    const [productRes, colorsRes] = await Promise.all([
      productsApi.getProduct(slug),
      productsApi.getProductColors(slug),
    ])
    product.value = productRes.data
    colors.value = colorsRes.data

    const mainImg = product.value.images?.find(i => i.is_main) || product.value.images?.[0]
    selectedImage.value = mainImg?.image || null

    if (colors.value.length) {
      selectedColor.value = colors.value[0]
    }
  } catch (e) {
    console.error(e)
  }
  loading.value = false
})
</script>
