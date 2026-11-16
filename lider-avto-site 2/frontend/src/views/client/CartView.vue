<template>
  <!-- Soft blue background like Figma -->
  <div class="min-h-screen page-shell">

    <!-- Page Header -->
    <div class="nav-glass px-4 pt-5 pb-4">
      <div class="max-w-6xl mx-auto">
        <h1 class="text-2xl font-bold text-slate-900 dark:text-white">{{ t('cart_title') }}</h1>
      </div>
    </div>

    <!-- Empty Cart -->
    <div v-if="!cartStore.loading && !cartStore.items.length" class="flex flex-col items-center justify-center py-24 px-4">
      <div class="w-24 h-24 bg-white dark:bg-slate-800 rounded-2xl flex items-center justify-center mb-5 shadow-sm border border-[#DCE4F0]/50 dark:border-slate-700">
        <ShoppingCart class="w-12 h-12 text-slate-300 dark:text-slate-600" />
      </div>
      <h2 class="text-xl font-bold text-slate-700 dark:text-slate-200 mb-2">{{ t('cart_empty') }}</h2>
      <p class="text-slate-400 dark:text-slate-500 text-sm mb-6">{{ t('cart_empty_sub2') }}</p>
      <router-link to="/catalog" class="btn-md btn-primary px-8">{{ t('cart_to_catalog') }}</router-link>
    </div>

    <!-- Loading -->
    <div v-if="cartStore.loading" class="max-w-6xl mx-auto p-4 space-y-3">
      <div v-for="i in 3" :key="i" class="skeleton h-32 rounded-xl" />
    </div>

    <!-- Cart Content -->
    <div v-if="!cartStore.loading && cartStore.items.length" class="max-w-6xl mx-auto p-4">

      <!-- Desktop: Two-column grid | Mobile: single column -->
      <div class="lg:grid lg:grid-cols-3 lg:gap-6 flex flex-col gap-4">

        <!-- LEFT: Items List (2/3 width on desktop) -->
        <div class="lg:col-span-2 space-y-3">
          <TransitionGroup name="fade">
            <div
              v-for="item in cartStore.items"
              :key="item.id"
              class="bg-white dark:bg-slate-800 rounded-xl border border-[#DCE4F0]/50 dark:border-slate-700 p-3 flex gap-3 relative shadow-sm"
            >
              <!-- Product Image -->
              <div class="w-20 h-20 lg:w-24 lg:h-24 rounded-lg bg-[#F3F6FB] dark:bg-slate-900 flex-shrink-0 flex items-center justify-center overflow-hidden">
                <img
                  :src="item.main_image || '/no-image.svg'"
                  :alt="item.product_name"
                  class="max-w-full max-h-full object-contain"
                />
              </div>

              <!-- Info -->
              <div class="flex-1 min-w-0 pr-6">
                <router-link :to="`/product/${item.product_slug}`" class="text-sm font-bold text-slate-900 dark:text-white hover:text-brand-600 dark:hover:text-brand-400 line-clamp-1 block leading-snug mb-1">
                  {{ item.product_name }}
                </router-link>

                <!-- Tags -->
                <div class="flex flex-wrap items-center gap-1.5 mb-3">
                  <span v-if="item.color_name" class="flex items-center gap-1 px-2 py-0.5 bg-[#F3F6FB] dark:bg-slate-700 rounded text-[11px] text-slate-600 dark:text-slate-300">
                    {{ item.color_name }}
                  </span>
                </div>

                <!-- Qty + Price -->
                <div class="flex items-center justify-between">
                  <div class="inline-flex items-center bg-[#F3F6FB] dark:bg-slate-700 rounded-lg h-8">
                    <button @click="changeQty(item, item.quantity - 1)" :disabled="item.quantity <= 1"
                      class="w-8 h-8 flex items-center justify-center text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white disabled:opacity-40 text-base font-semibold">
                      −
                    </button>
                    <span class="w-8 text-center text-sm font-bold text-slate-900 dark:text-white">{{ item.quantity }}</span>
                    <button @click="changeQty(item, item.quantity + 1)"
                      class="w-8 h-8 flex items-center justify-center text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white text-base font-semibold">
                      +
                    </button>
                  </div>
                  <span class="text-base font-bold text-slate-900 dark:text-white">{{ formatPrice(item.total_price) }}</span>
                </div>
              </div>

              <!-- Delete -->
              <button @click="removeItem(item.id)" class="absolute top-3 right-3 text-slate-300 dark:text-slate-500 hover:text-red-500 transition-colors">
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </TransitionGroup>

          <!-- Clear Cart -->
          <div class="flex justify-end pt-1">
            <button @click="clearCart" class="text-xs text-red-400 hover:text-red-600 transition-colors flex items-center gap-1">
              <Trash2 class="w-3.5 h-3.5" /> {{ t('cart_clear') }}
            </button>
          </div>
        </div>

        <!-- RIGHT: Summary (1/3 width on desktop) -->
        <div class="lg:col-span-1">
          <div class="bg-white dark:bg-slate-800 rounded-xl border border-[#DCE4F0]/50 dark:border-slate-700 p-5 shadow-sm lg:sticky lg:top-24">
            <h2 class="font-bold text-slate-900 dark:text-white text-base mb-5">{{ t('cart_summary') }}</h2>

            <div class="space-y-3 text-sm mb-5">
              <div class="flex justify-between text-slate-600 dark:text-slate-300">
                <span>{{ t('cart_items_count') }}</span>
                <span class="font-semibold text-slate-900 dark:text-white">{{ cartStore.itemCount }} {{ t('cart_qty') }}</span>
              </div>
              <div class="flex justify-between text-slate-600 dark:text-slate-300">
                <span>{{ t('cart_items_price') }}</span>
                <span class="font-semibold text-slate-900 dark:text-white">{{ formatPrice(cartStore.subtotal) }}</span>
              </div>
              <div class="flex justify-between text-slate-600 dark:text-slate-300">
                <span>{{ t('cart_delivery') }}</span>
                <span class="font-semibold text-emerald-600">{{ t('cart_free') }}</span>
              </div>
            </div>

            <div class="h-px bg-[#DCE4F0]/40 dark:bg-slate-700 mb-5" />

            <div class="flex justify-between items-end mb-5">
              <span class="text-sm font-bold text-slate-900 dark:text-white">{{ t('cart_total') }}</span>
              <span class="text-2xl font-bold text-brand-700 dark:text-brand-400">{{ formatPrice(cartStore.subtotal) }}</span>
            </div>

            <router-link
              to="/checkout"
              class="block w-full text-center py-3.5 btn-primary text-white rounded-xl font-bold text-sm uppercase tracking-wider transition-colors"
            >
              {{ t('cart_checkout') }}
            </router-link>

            <p class="text-[10px] text-center text-slate-400 dark:text-slate-500 mt-3 leading-relaxed">
              {{ t('cart_terms') }}
            </p>
          </div>
        </div>

      </div>
    </div>

    <!-- Confirm Modal -->
    <Transition name="fade">
      <div v-if="confirmModal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
        <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-xl max-w-sm w-full p-6">
          <div class="w-12 h-12 bg-red-100 dark:bg-red-500/15 rounded-full flex items-center justify-center mb-4 mx-auto">
            <AlertCircle class="w-6 h-6 text-red-500" />
          </div>
          <h3 class="text-lg font-bold text-slate-900 dark:text-white text-center mb-2">{{ confirmModal.title }}</h3>
          <p class="text-slate-500 dark:text-slate-400 text-center text-sm mb-6">{{ confirmModal.text }}</p>
          <div class="flex gap-3">
            <button @click="confirmModal.show = false" class="flex-1 btn-md btn-outline border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-200">{{ t('common_cancel') }}</button>
            <button @click="executeConfirm" class="flex-1 btn-md btn-danger">{{ t('cart_confirm') }}</button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ShoppingCart, Trash2, AlertCircle } from '@lucide/vue'
import { useCartStore } from '@/stores/cart'
import { useAlertStore } from '@/stores/alert'
import { useI18n } from '@/i18n'

const cartStore  = useCartStore()
const alertStore = useAlertStore()
const { t } = useI18n()

function formatPrice(price) {
  if (!price && price !== 0) return '—'
  return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(price)
}

async function changeQty(item, qty) {
  if (qty < 1) return
  const result = await cartStore.updateItem(item.id, { quantity: qty })
  if (!result.success) alertStore.error(t('cart_error'))
}

async function removeItem(id) {
  await cartStore.removeItem(id)
  alertStore.info(t('cart_removed'))
}

const confirmModal = ref({ show: false, title: '', text: '', action: null })
function showConfirm(title, text, action) {
  confirmModal.value = { show: true, title, text, action }
}
async function executeConfirm() {
  if (confirmModal.value.action) await confirmModal.value.action()
  confirmModal.value.show = false
}

function clearCart() {
  showConfirm(
    t('cart_clear_title'),
    t('cart_clear_text'),
    async () => {
      await cartStore.clearCart()
      alertStore.info(t('cart_cleared'))
    }
  )
}

onMounted(async () => {
  await cartStore.fetchCart()
})
</script>
