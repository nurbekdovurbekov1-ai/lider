<template>
  <div class="product-surface flex flex-col overflow-hidden group">
    <!-- Image Area -->
    <div class="relative product-media p-4 flex items-center justify-center aspect-[4/3] overflow-hidden">
      <img
        :src="mainImage"
        :alt="product.name"
        class="max-w-full max-h-full object-contain group-hover:scale-105 transition-transform duration-500 cursor-pointer"
        loading="lazy"
        @error="handleImgError"
        @click="goToDetail"
      />
      <!-- Badges -->
      <div class="absolute top-4 right-4 flex flex-col gap-2">
        <span v-if="product.badge" class="px-2.5 py-1 bg-brand-50 dark:bg-brand-500/15 text-brand-600 dark:text-brand-400 text-[10px] font-bold uppercase tracking-wider rounded">{{ ({ new: t('product_badge_new'), hit: t('product_badge_hit'), sale: t('product_badge_sale') })[product.badge] || product.badge }}</span>
      </div>
    </div>

    <!-- Content Area -->
    <div class="p-5 flex flex-col flex-1">
      <!-- Category -->
      <p class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest mb-1">{{ categoryName(product.category_name) }}</p>
      
      <!-- Title -->
      <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-3">{{ product.name }}</h3>

      <!-- Brend / artikul -->
      <div class="flex items-center gap-1.5 mb-4 text-xs text-slate-500 dark:text-slate-400">
        <span>{{ product.brand || t('product_part_fallback') }}</span>
        <span v-if="product.article">· {{ product.article }}</span>
      </div>

      <!-- Price -->
      <div class="mb-3">
        <p class="text-base font-extrabold text-brand-700 dark:text-brand-300">
          {{ formatPrice(displayPrice) }}
          <span class="text-[11px] font-normal text-slate-400">{{ t('common_per_piece') }}</span>
        </p>
      </div>

      <!-- Colors -->
      <div v-if="product.colors?.length" class="flex items-center gap-1.5 mb-5">
        <div
          v-for="color in product.colors.slice(0, 5)"
          :key="color.id"
          class="w-4.5 h-4.5 rounded-full border border-slate-200 dark:border-slate-600 shadow-xs cursor-help"
          :style="{ backgroundColor: color.hex_code }"
          :title="`${color.name}: ${formatPrice(color.calculated_price ?? color.price ?? (Number(product.base_price) + Number(color.price_modifier || 0)))}`"
        />
        <span v-if="product.colors.length > 5" class="text-[10px] font-medium text-slate-400 dark:text-slate-500 ml-1">+{{ product.colors.length - 5 }}</span>
      </div>

      <!-- Buttons -->
      <div class="mt-auto flex items-center gap-3">
        <router-link :to="`/product/${product.slug}`" class="flex-1 btn-md btn-primary font-medium text-xs uppercase tracking-wider text-center py-2.5 rounded-lg">
          {{ t('common_details') }}
        </router-link>
        <button @click="goToDetail" class="w-10 h-10 rounded-lg bg-slate-100 dark:bg-slate-700 hover:bg-brand-50 dark:hover:bg-brand-500/20 flex items-center justify-center text-slate-600 dark:text-slate-300 hover:text-brand-600 dark:hover:text-brand-300 transition-colors" :title="t('common_details')">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '@/i18n'
import { getMediaUrl } from '@/utils/mediaUrl'

const { t, categoryName } = useI18n()
const router = useRouter()

function goToDetail() {
  router.push(`/product/${props.product.slug}`)
}

const props = defineProps({
  product: { type: Object, required: true }
})

function formatPrice(p) {
  if (!p && p !== 0) return '—'
  return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(p)
}

const displayPrice = computed(() => {
  return props.product.min_price || props.product.base_price || 0
})

const mainImage = computed(() => {
  // Use main_image if available (from ProductListSerializer)
  if (props.product.main_image) return getMediaUrl(props.product.main_image);
  // Fallback for ProductDetailSerializer where images list is available
  const mainImg = props.product.images?.find(i => i.is_main) || props.product.images?.[0]
  return getMediaUrl(mainImg?.image)
})

function handleImgError(e) {
  e.target.src = '/no-image.svg'
}
</script>
