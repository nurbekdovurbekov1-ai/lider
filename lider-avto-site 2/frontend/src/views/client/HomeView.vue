<template>
  <div class="min-h-screen page-shell">

    <!-- =================== HERO BANNER =================== -->
    <section class="relative overflow-hidden">
      <!-- Mobile Hero (figmaga mos) -->
      <div class="md:hidden">
        <div class="relative h-[420px] flex flex-col justify-end overflow-hidden rounded-b-3xl">
          <!-- Gradient fon: banner yo'q yoki balandligi yetmaganda -->
          <div class="absolute inset-0 bg-gradient-to-br from-brand-900 via-brand-700 to-brand-500" />

          <!-- Banner rasmi: fonda, qoplab turadi -->
          <img
            v-if="banners.length"
            :src="banners[0].image"
            alt="Hero"
            class="absolute inset-0 w-full h-full object-cover"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-brand-950/80 via-brand-950/30 to-transparent" />

          <!-- Content card at bottom -->
          <div class="relative z-10 m-4 mb-6 bg-[color:var(--surface-elevated)] rounded-2xl p-5 shadow-lg border border-white/40 dark:border-white/5">
            <h1 class="text-xl font-bold text-slate-900 dark:text-white mb-2 leading-snug">
              {{ t('home_hero_mobile_title') }}
            </h1>
            <p class="text-sm text-slate-500 dark:text-slate-400 mb-4 leading-relaxed">
              {{ t('home_hero_mobile_sub') }}
            </p>
            <div class="flex flex-col gap-2.5">
              <!-- Asosiy tugma: Ro'yxatdan o'tish (agar kirmagan bo'lsa) / Bog'lanish (agar kirgan bo'lsa) -->
              <button
                v-if="!authStore.isLoggedIn"
                @click="openAuthModal"
                class="w-full btn btn-lg btn-accent justify-center"
              >
                {{ t('home_register') }}
              </button>
              <router-link
                v-else
                to="/contact"
                class="w-full btn btn-lg btn-accent justify-center"
              >
                {{ t('home_contact') }}
              </router-link>

              <!-- 2-tugma: Mahsulotlar (Katalog) doimiy -->
              <router-link
                to="/catalog"
                class="w-full py-3.5 border-2 border-brand-950/90 dark:border-white/80 text-brand-950 dark:text-white rounded-xl font-bold text-sm transition-colors hover:bg-brand-50 dark:hover:bg-white/10 text-center"
              >
                {{ t('home_products') }}
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Desktop Hero: banner fon sifatida, kontent ustida -->
      <div class="hidden md:block relative overflow-hidden h-[480px] lg:h-[540px]">
        <!-- Gradient fon: banner yo'q yoki balandligi yetmaganda -->
        <div class="absolute inset-0 bg-gradient-to-br from-brand-950 via-brand-800 to-brand-600" />

        <!-- Banner rasmi: fonda, qoplab turadi -->
        <img
          v-if="banners.length"
          :src="banners[0].image"
          alt="Hero"
          class="absolute inset-0 w-full h-full object-cover"
        />

        <!-- Matn kontrasti uchun ustki gradient -->
        <div class="absolute inset-0 bg-gradient-to-r from-brand-950/85 via-brand-900/55 to-transparent" />
        <div class="absolute z-[2] -right-24 -top-24 w-[420px] h-[420px] rounded-full bg-accent-500/20 blur-3xl" />
        <div class="absolute z-[2] right-48 -bottom-32 w-[360px] h-[360px] rounded-full bg-brand-400/20 blur-3xl" />

        <div class="relative z-10 container-custom h-full py-10 grid grid-cols-12 gap-10 items-center">
          <div class="col-span-7">
            <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-white/90 text-xs font-semibold border border-white/15 mb-5">
              <span class="w-2 h-2 rounded-full bg-accent-500" />
              {{ t('home_hero_badge') }}
            </span>
            <h1 class="text-4xl lg:text-5xl xl:text-6xl font-extrabold text-white leading-[1.1] mb-5">
              {{ t('home_hero_title') }} <span class="text-accent-500">{{ t('home_hero_title_accent') }}</span> {{ t('home_hero_title_end') }}
            </h1>
            <p class="text-base text-slate-200 mb-8 leading-relaxed max-w-xl">
              {{ t('home_hero_sub') }}
            </p>
            <div class="flex flex-wrap items-center gap-3.5 mb-10">
              <router-link
                to="/catalog"
                class="btn btn-lg btn-accent"
              >
                {{ t('home_view_catalog') }}
              </router-link>
              <button
                v-if="!authStore.isLoggedIn"
                @click="openAuthModal"
                class="btn btn-lg border-2 border-white/70 text-white hover:bg-white hover:text-brand-950 rounded-xl font-bold transition-all hover:-translate-y-0.5"
              >
                {{ t('home_register') }}
              </button>
              <router-link
                v-else
                to="/contact"
                class="btn btn-lg border-2 border-white/70 text-white hover:bg-white hover:text-brand-950 rounded-xl font-bold transition-all hover:-translate-y-0.5"
              >
                {{ t('home_contact') }}
              </router-link>
            </div>
            <div class="flex items-center gap-8 text-white">
              <div><p class="text-2xl font-extrabold">100%</p><p class="text-xs text-white/70">{{ t('home_stat_original') }}</p></div>
              <div><p class="text-2xl font-extrabold">6 {{ locale === 'uz' ? 'oy' : locale === 'ru' ? 'мес.' : 'mo' }}</p><p class="text-xs text-white/70">{{ t('home_stat_warranty') }}</p></div>
              <div><p class="text-2xl font-extrabold">1–2 {{ locale === 'uz' ? 'kun' : locale === 'ru' ? 'дн.' : 'days' }}</p><p class="text-xs text-white/70">{{ t('home_stat_delivery') }}</p></div>
            </div>
          </div>

          <div class="col-span-5">
            <div class="rounded-3xl bg-white/10 border border-white/15 backdrop-blur-md p-6">
              <p class="text-white font-bold text-lg mb-1">{{ t('home_select_car') }}</p>
              <p class="text-white/70 text-sm mb-4">{{ t('home_select_car_sub') }}</p>
              <div class="flex flex-wrap gap-2">
                <router-link
                  v-for="c in carModels"
                  :key="c.id"
                  :to="`/catalog?car=${c.slug}`"
                  class="px-3.5 py-1.5 rounded-full bg-white/10 border border-white/15 text-white text-sm font-semibold hover:bg-accent-500 hover:border-accent-500 hover:text-[#1a1000] transition-colors"
                >{{ c.name }}</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- =================== MASHINA TANLASH =================== -->
    <section class="px-4 pt-6 md:hidden">
      <div class="surface-panel rounded-3xl p-5 md:p-8">
        <h2 class="text-lg md:text-2xl font-bold text-slate-900 dark:text-white mb-1">{{ t('home_select_car') }}</h2>
        <p class="text-sm text-slate-500 dark:text-slate-400 mb-4">{{ t('home_select_car_sub2') }}</p>
        <div class="flex flex-wrap gap-2">
          <router-link
            v-for="c in carModels"
            :key="c.id"
            :to="`/catalog?car=${c.slug}`"
            class="px-4 py-2 rounded-full border border-[color:var(--border)] bg-[color:var(--surface-0)] text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-brand-600 hover:border-brand-600 hover:text-white transition-colors"
          >{{ c.name }}</router-link>
        </div>
      </div>
    </section>

    <!-- =================== KATEGORIYALAR =================== -->
    <section class="px-4 pt-6 pb-2 md:py-10 md:container-custom">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg md:text-2xl font-bold text-slate-900 dark:text-white">{{ t('home_categories') }}</h2>
      </div>

      <!-- Loading -->
      <div v-if="categoriesLoading" class="flex gap-4 overflow-x-auto pb-2">
        <div v-for="i in 4" :key="i" class="skeleton w-24 h-24 rounded-2xl flex-shrink-0" />
      </div>

      <!-- Mobile: horizontal scroll chips -->
      <div v-else class="md:hidden flex gap-3 overflow-x-auto pb-2 scrollbar-hide -mx-4 px-4">
        <router-link
          v-for="cat in categories"
          :key="cat.slug"
          :to="`/catalog?category=${cat.slug}`"
          class="flex-shrink-0 flex flex-col items-center gap-2 group"
        >
          <div class="w-20 h-20 rounded-2xl bg-[color:var(--surface-elevated)] border border-[color:var(--border)] flex items-center justify-center overflow-hidden shadow-sm group-hover:border-brand-400 group-hover:shadow-md transition-all">
            <img v-if="cat.icon" :src="cat.icon" :alt="cat.name" class="w-full h-full object-cover" />
            <span v-else class="text-3xl">{{ categoryEmoji(cat) }}</span>
          </div>
          <span class="text-xs font-medium text-slate-700 dark:text-slate-300 text-center w-20 line-clamp-2 leading-tight">{{ categoryName(cat) }}</span>
        </router-link>
      </div>

      <!-- Desktop: kategoriyalar to'ri -->
      <div v-if="!categoriesLoading" class="hidden md:grid grid-cols-3 lg:grid-cols-4 gap-4">
        <router-link
          v-for="cat in categories"
          :key="cat.slug"
          :to="`/catalog?category=${cat.slug}`"
          class="group product-surface p-5 flex items-center gap-4"
        >
          <div class="w-14 h-14 rounded-xl bg-brand-50 dark:bg-brand-500/15 flex items-center justify-center overflow-hidden flex-shrink-0">
            <img v-if="cat.icon" :src="cat.icon" :alt="cat.name" class="w-full h-full object-cover" />
            <span v-else class="text-2xl">{{ categoryEmoji(cat) }}</span>
          </div>
          <h3 class="text-base font-bold text-slate-900 dark:text-white group-hover:text-brand-600 dark:group-hover:text-brand-400 transition-colors">{{ categoryName(cat) }}</h3>
        </router-link>
      </div>
    </section>

    <!-- =================== OMMABOP MAHSULOTLAR =================== -->
    <section class="px-4 pt-6 pb-4 md:py-10 md:container-custom">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg md:text-2xl font-bold text-slate-900 dark:text-white">{{ t('home_popular') }}</h2>
        <router-link to="/catalog" class="group flex items-center gap-1.5 px-4 py-2 bg-brand-50 dark:bg-brand-500/15 hover:bg-brand-100 dark:hover:bg-brand-500/25 text-brand-700 dark:text-brand-400 text-sm font-bold rounded-full transition-all duration-300">
          {{ t('common_all') }}
          <ArrowRight class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="productsLoading" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-5">
        <div v-for="i in 4" :key="i" class="skeleton rounded-2xl h-56" />
      </div>

      <!-- Products Grid -->
      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-5">
        <div
          v-for="product in featuredProducts"
          :key="product.id"
          class="product-surface overflow-hidden group"
        >
          <!-- Image -->
          <div
            class="relative product-media aspect-[4/3] flex items-center justify-center p-3 cursor-pointer overflow-hidden"
            @click="$router.push(`/product/${product.slug}`)"
          >
            <img
              :src="product.main_image || '/no-image.svg'"
              :alt="product.name"
              class="max-w-full max-h-full object-contain group-hover:scale-105 transition-transform duration-300"
              loading="lazy"
            />
          </div>

          <!-- Info -->
          <div class="p-3">
            <p class="text-[10px] text-slate-400 uppercase tracking-wider font-semibold mb-0.5">{{ categoryName(product.category_name) }}</p>
            <p class="text-sm font-bold text-slate-900 dark:text-white line-clamp-2 leading-snug mb-1.5">{{ product.name }}</p>
            <div class="flex items-baseline justify-between mb-2">
              <span class="text-xs font-bold text-brand-700 dark:text-brand-300">
                {{ formatPrice(product.min_price || product.base_price) }}
              </span>
              <span class="text-[10px] text-slate-400 font-medium">{{ t('common_per_piece') }}</span>
            </div>
            <!-- Colors dots -->
            <div v-if="product.colors?.length" class="flex items-center gap-1 mb-2.5">
              <div
                v-for="c in product.colors.slice(0, 4)"
                :key="c.id"
                class="w-3.5 h-3.5 rounded-full border border-slate-200"
                :style="{ backgroundColor: c.hex_code }"
                :title="`${c.name}: ${formatPrice(c.calculated_price ?? c.price ?? product.base_price)}`"
              />
              <span v-if="product.colors.length > 4" class="text-[9px] text-slate-400 font-medium">+{{ product.colors.length - 4 }}</span>
            </div>
            <button
              @click="$router.push(`/product/${product.slug}`)"
              class="w-full btn btn-sm btn-primary justify-center"
              :title="t('common_details')"
            >
              <span>{{ t('common_details') }}</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- =================== AFZALLIKLAR =================== -->
    <section class="px-4 pb-6 md:pb-12 md:container-custom">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-5">
        <div v-for="b in benefits" :key="b.title" class="surface-panel p-4 md:p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-brand-300/70 dark:hover:border-brand-500/40">
          <div class="w-10 h-10 rounded-xl bg-brand-50 dark:bg-brand-500/15 grid place-items-center text-xl mb-2.5">{{ b.icon }}</div>
          <p class="text-sm font-bold text-slate-900 dark:text-white">{{ b.title }}</p>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ b.text }}</p>
        </div>
      </div>
    </section>

    <!-- =================== CTA BANNER =================== -->
    <section class="px-4 pb-8 md:pb-16 md:container-custom">
      <div class="relative overflow-hidden rounded-3xl bg-navy-gradient border border-white/10 p-6 md:p-10 text-center">
        <!-- Decorative glows -->
        <div class="glow-blob -top-16 -right-10 w-56 h-56 bg-brand-500/40" />
        <div class="glow-blob -bottom-20 -left-12 w-52 h-52 bg-accent-500/25" />
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_55%)] pointer-events-none" />

        <div class="relative z-10">
          <h2 class="text-xl md:text-3xl font-bold text-white mb-2">
            {{ t('home_cta_title') }}
          </h2>
          <p class="text-sm md:text-base text-brand-200 mb-6">
            {{ t('home_cta_sub') }}
          </p>
          <button
            @click="scrollToContact"
            class="btn btn-lg btn-accent"
          >
            {{ t('home_cta_btn') }}
          </button>
        </div>
      </div>
    </section>

    <!-- =================== CONTACT SECTION =================== -->
    <section id="contact" class="px-4 pb-8 md:pb-16 md:container-custom">
      <div class="surface-panel rounded-3xl p-6 md:p-10">
        <div class="md:flex md:items-center md:gap-12">
          <div class="mb-6 md:mb-0 md:flex-1">
            <h2 class="text-xl md:text-3xl font-bold text-slate-900 dark:text-white mb-3">{{ t('home_contact_title') }}</h2>
            <p class="text-slate-500 dark:text-slate-400 text-sm md:text-base mb-5">
              {{ t('home_contact_sub') }}
            </p>
            <div class="space-y-3">
              <div class="flex items-center gap-3 text-sm text-slate-700 dark:text-slate-300">
                <div class="w-9 h-9 bg-brand-50 dark:bg-brand-500/15 rounded-xl flex items-center justify-center flex-shrink-0">
                  <Phone class="w-4 h-4 text-brand-600 dark:text-brand-300" />
                </div>
                <a :href="`tel:${siteStore.phoneMain || '+998900000000'}`" class="font-semibold hover:text-brand-600 dark:hover:text-brand-400">{{ siteStore.phoneMain || '+998 90 000 00 00' }}</a>
              </div>
              <div class="flex items-center gap-3 text-sm text-slate-700 dark:text-slate-300">
                <div class="w-9 h-9 bg-brand-50 dark:bg-brand-500/15 rounded-xl flex items-center justify-center flex-shrink-0">
                  <MapPin class="w-4 h-4 text-brand-600 dark:text-brand-300" />
                </div>
                <span>{{ siteStore.address || "O'zbekiston" }}</span>
              </div>
              <div class="flex items-center gap-3 text-sm text-slate-700 dark:text-slate-300">
                <div class="w-9 h-9 bg-brand-50 dark:bg-brand-500/15 rounded-xl flex items-center justify-center flex-shrink-0">
                  <Clock class="w-4 h-4 text-brand-600 dark:text-brand-300" />
                </div>
                <span>{{ workHoursText }}</span>
              </div>
            </div>
          </div>
          <div class="md:flex-1">
            <form @submit.prevent="submitContact" class="space-y-3">
              <input v-model="contactForm.name" type="text" :placeholder="t('home_form_name')" class="form-input text-sm" required />
              <input v-model="contactForm.phone" type="tel" :placeholder="t('home_form_phone')" class="form-input text-sm" required />
              <textarea v-model="contactForm.message" rows="3" :placeholder="t('home_form_message')" class="form-input text-sm resize-none" />
              <button type="submit" :disabled="contactSending" class="w-full btn btn-lg btn-primary justify-center disabled:opacity-60">
                {{ contactSending ? t('common_sending') : t('common_send') }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import { Phone, MapPin, Clock, ArrowRight } from '@lucide/vue'
import { productsApi } from '@/api/products'
import { siteApi } from '@/api/site'
import { useAlertStore } from '@/stores/alert'
import { useSiteStore } from '@/stores/site'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from '@/i18n'

const alertStore = useAlertStore()
const siteStore  = useSiteStore()
const authStore  = useAuthStore()
const { t, locale, categoryName } = useI18n()

const workHoursText = computed(() =>
  locale.value === 'uz' && siteStore.workHours ? siteStore.workHours : t('work_hours_text')
)

const banners           = ref([])
const categories        = ref([])
const featuredProducts  = ref([])
const carModels         = ref([])
const benefits = computed(() => [
  { icon: '✅', title: t('home_benefit1_title'), text: t('home_benefit1_text') },
  { icon: '🚚', title: t('home_benefit2_title'), text: t('home_benefit2_text') },
  { icon: '🛡️', title: t('home_benefit3_title'), text: t('home_benefit3_text') },
  { icon: '↩️', title: t('home_benefit4_title'), text: t('home_benefit4_text') },
])
const categoriesLoading = ref(true)
const productsLoading   = ref(true)

const contactForm = ref({ name: '', phone: '', message: '' })
const contactSending = ref(false)

onMounted(async () => {
  try {
    siteStore.fetchSettings()
    const [bannersRes, catsRes, prodsRes, carsRes] = await Promise.all([
      productsApi.getBanners(),
      productsApi.getCategories(),
      productsApi.getProducts({ page_size: 8, ordering: '-created_at' }),
      productsApi.getCarModels(),
    ])
    carModels.value        = carsRes.data.results   || carsRes.data
    banners.value          = bannersRes.data.results || bannersRes.data
    categories.value       = catsRes.data.results   || catsRes.data
    featuredProducts.value = prodsRes.data.results  || prodsRes.data
  } catch (err) {
    console.error(err)
  } finally {
    categoriesLoading.value = false
    productsLoading.value   = false
  }
})

function openAuthModal() {
  window.dispatchEvent(new CustomEvent('auth:open-modal'))
}

const CATEGORY_EMOJI = [
  ['dvigatel', '⚙️'], ['tormoz', '🛑'], ['filtr', '🧰'], ['osma', '🔩'], ['podveska', '🔩'],
  ['elektr', '🔋'], ['yorit', '💡'], ['yog', '🛢️'], ['moy', '🛢️'], ['sovit', '❄️'],
  ['uzatma', '🕹️'], ['transmis', '🕹️'], ['kuzov', '🚗'], ['salon', '💺'],
]
function categoryEmoji(cat) {
  const key = `${cat.slug || ''} ${cat.name || ''}`.toLowerCase()
  return CATEGORY_EMOJI.find(([k]) => key.includes(k))?.[1] || '🔧'
}

function scrollToContact() {
  document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })
}

function formatPrice(p) {
  if (!p && p !== 0) return '—'
  return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(p)
}

async function submitContact() {
  if (contactSending.value) return
  contactSending.value = true
  try {
    await siteApi.submitContact(contactForm.value)
    alertStore.success(t('home_form_success'))
    contactForm.value = { name: '', phone: '', message: '' }
  } catch (err) {
    alertStore.error(err.response?.data?.detail || t('home_form_error'))
  } finally {
    contactSending.value = false
  }
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>

