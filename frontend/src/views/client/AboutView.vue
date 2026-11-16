<template>
  <div class="min-h-screen page-shell">

    <!-- Breadcrumb & Header -->
    <div class="nav-glass px-4 pt-5 pb-4">
      <div class="max-w-5xl mx-auto">
        <div class="flex items-center gap-2 text-sm text-slate-400 mb-2">
          <router-link to="/" class="hover:text-brand-600 dark:hover:text-brand-400">{{ t('nav_home') }}</router-link>
          <span>/</span>
          <span class="text-slate-700 dark:text-slate-200 font-medium">{{ t('nav_about') }}</span>
        </div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">
          {{ about.title || t('about_title') }}
        </h1>
        <p v-if="about.subtitle" class="text-slate-500 text-sm mt-1">
          {{ about.subtitle }}
        </p>
      </div>
    </div>

    <!-- Main Container -->
    <div class="max-w-5xl mx-auto px-4 py-6 md:py-10 space-y-8">

      <!-- Loading skeleton -->
      <div v-if="loading" class="space-y-6">
        <div class="skeleton h-80 rounded-3xl" />
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div v-for="i in 4" :key="i" class="skeleton h-24 rounded-2xl" />
        </div>
      </div>

      <template v-else>
        <!-- Top Hero Card: Image + Content in Bento Layout -->
        <div class="bg-white dark:bg-slate-800 rounded-3xl border border-[#DCE4F0]/50 dark:border-slate-700 overflow-hidden shadow-sm">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-0 items-stretch">
            
            <!-- Left: Text content -->
            <div class="lg:col-span-7 p-6 sm:p-8 md:p-10 flex flex-col justify-center space-y-4">
              <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-50 dark:bg-brand-500/15 border border-brand-200/60 dark:border-brand-500/30 text-brand-800 dark:text-brand-300 text-xs font-semibold w-fit">
                <Building2 class="w-3.5 h-3.5 text-brand-600 dark:text-brand-400" />
                <span>{{ t('about_company') }}</span>
              </div>

              <h2 class="text-xl sm:text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white leading-snug">
                {{ about.title || t('about_fallback_title') }}
              </h2>

              <div class="text-slate-600 dark:text-slate-300 text-sm sm:text-base leading-relaxed whitespace-pre-line space-y-3">
                <p>{{ about.content }}</p>
              </div>

              <!-- Mission quote / highlight -->
              <div v-if="about.mission" class="mt-4 p-4 rounded-2xl bg-[#F3F6FB]/60 dark:bg-slate-700/40 border-l-4 border-brand-600">
                <p class="text-xs font-semibold uppercase tracking-wider text-brand-700 dark:text-brand-400 mb-1">{{ t('about_mission_label') }}</p>
                <p class="text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-relaxed italic">
                  "{{ about.mission }}"
                </p>
              </div>
            </div>

            <!-- Right: Image with Badge -->
            <div class="lg:col-span-5 relative bg-gradient-to-br from-slate-100 to-slate-200 min-h-[280px] lg:min-h-[420px] flex items-center justify-center overflow-hidden">
              <img
                v-if="about.image"
                :src="about.image"
                :alt="about.title"
                class="w-full h-full object-cover object-center absolute inset-0"
              />
              <!-- Fallback placeholder visual if no image uploaded -->
              <div v-else class="flex flex-col items-center justify-center p-8 text-center text-slate-400">
                <Building2 class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-2" />
                <span class="text-xs font-medium text-slate-500 dark:text-slate-400">{{ t('about_store') }}</span>
              </div>

              <!-- Experience Float Badge -->
              <div
                v-if="about.experience_years"
                class="absolute bottom-4 left-4 bg-white/95 dark:bg-slate-800/95 backdrop-blur-md border border-white/50 dark:border-slate-700 shadow-lg rounded-2xl px-4 py-3 flex items-center gap-3 z-10"
              >
                <div class="w-10 h-10 rounded-xl bg-brand-600 text-white flex items-center justify-center font-extrabold text-sm">
                  {{ about.experience_years }}
                </div>
                <div>
                  <p class="text-xs font-bold text-slate-900 dark:text-white">{{ t('about_experience') }}</p>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400">{{ t('about_experience_sub') }}</p>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- Dynamic Stats Grid from Database -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
          <div v-if="about.stat_1_number" class="bg-white dark:bg-slate-800 rounded-2xl border border-[#DCE4F0]/50 dark:border-slate-700 p-4 sm:p-5 text-center shadow-sm">
            <p class="text-2xl sm:text-3xl font-extrabold text-brand-900 dark:text-brand-400 mb-1">{{ about.stat_1_number }}</p>
            <p class="text-xs text-slate-500 dark:text-slate-400 font-medium">{{ about.stat_1_label || "Ehtiyot qismlar" }}</p>
          </div>
          <div v-if="about.stat_2_number" class="bg-white dark:bg-slate-800 rounded-2xl border border-[#DCE4F0]/50 dark:border-slate-700 p-4 sm:p-5 text-center shadow-sm">
            <p class="text-2xl sm:text-3xl font-extrabold text-emerald-600 mb-1">{{ about.stat_2_number }}</p>
            <p class="text-xs text-slate-500 dark:text-slate-400 font-medium">{{ about.stat_2_label || "Mijozlar" }}</p>
          </div>
          <div v-if="about.stat_3_number" class="bg-white dark:bg-slate-800 rounded-2xl border border-[#DCE4F0]/50 dark:border-slate-700 p-4 sm:p-5 text-center shadow-sm">
            <p class="text-2xl sm:text-3xl font-extrabold text-blue-600 mb-1">{{ about.stat_3_number }}</p>
            <p class="text-xs text-slate-500 dark:text-slate-400 font-medium">{{ about.stat_3_label || "Sifat kafolati" }}</p>
          </div>
          <div v-if="about.stat_4_number" class="bg-white dark:bg-slate-800 rounded-2xl border border-[#DCE4F0]/50 dark:border-slate-700 p-4 sm:p-5 text-center shadow-sm">
            <p class="text-2xl sm:text-3xl font-extrabold text-purple-600 mb-1">{{ about.stat_4_number }}</p>
            <p class="text-xs text-slate-500 dark:text-slate-400 font-medium">{{ about.stat_4_label || "Qo'llab-quvvatlash" }}</p>
          </div>
        </div>

        <!-- Core Values / Why Us Grid -->
        <div class="bg-white dark:bg-slate-800 rounded-3xl border border-[#DCE4F0]/50 dark:border-slate-700 p-6 md:p-8 shadow-sm">
          <h3 class="text-lg md:text-xl font-bold text-slate-900 dark:text-white mb-5">{{ t('about_why_title') }}</h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex items-start gap-3.5 p-4 rounded-2xl bg-[#F3F6FB]/50 dark:bg-slate-700/40 border border-[#DCE4F0]/40 dark:border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-500/15 flex items-center justify-center flex-shrink-0">
                <ShieldCheck class="w-5 h-5 text-blue-700 dark:text-blue-400" />
              </div>
              <div>
                <h4 class="text-sm font-bold text-slate-900 dark:text-white mb-1">{{ t('about_value1_title') }}</h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{{ t('about_value1_text') }}</p>
              </div>
            </div>

            <div class="flex items-start gap-3.5 p-4 rounded-2xl bg-[#F3F6FB]/50 dark:bg-slate-700/40 border border-[#DCE4F0]/40 dark:border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-500/15 flex items-center justify-center flex-shrink-0">
                <Truck class="w-5 h-5 text-emerald-700 dark:text-emerald-400" />
              </div>
              <div>
                <h4 class="text-sm font-bold text-slate-900 dark:text-white mb-1">{{ t('about_value2_title') }}</h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{{ t('about_value2_text') }}</p>
              </div>
            </div>

            <div class="flex items-start gap-3.5 p-4 rounded-2xl bg-[#F3F6FB]/50 dark:bg-slate-700/40 border border-[#DCE4F0]/40 dark:border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-500/15 flex items-center justify-center flex-shrink-0">
                <Sparkles class="w-5 h-5 text-amber-700 dark:text-amber-400" />
              </div>
              <div>
                <h4 class="text-sm font-bold text-slate-900 dark:text-white mb-1">{{ t('about_value3_title') }}</h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{{ t('about_value3_text') }}</p>
              </div>
            </div>

            <div class="flex items-start gap-3.5 p-4 rounded-2xl bg-[#F3F6FB]/50 dark:bg-slate-700/40 border border-[#DCE4F0]/40 dark:border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-purple-100 dark:bg-purple-500/15 flex items-center justify-center flex-shrink-0">
                <Headphones class="w-5 h-5 text-purple-700 dark:text-purple-400" />
              </div>
              <div>
                <h4 class="text-sm font-bold text-slate-900 dark:text-white mb-1">{{ t('about_value4_title') }}</h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{{ t('about_value4_text') }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Contact / Catalog Action Card -->
        <div class="bg-gradient-to-r from-brand-950 to-slate-900 text-white rounded-3xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6 shadow-sm">
          <div>
            <h3 class="text-lg md:text-xl font-bold mb-1">{{ t('about_cta_title') }}</h3>
            <p class="text-xs md:text-sm text-slate-300">{{ t('about_cta_sub') }}</p>
          </div>
          <div class="flex items-center gap-3 w-full md:w-auto">
            <router-link
              to="/catalog"
              class="flex-1 md:flex-none text-center px-5 py-3 bg-white text-slate-900 dark:bg-slate-800 dark:text-white rounded-xl text-xs font-bold hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors shadow"
            >
              {{ t('cart_to_catalog') }}
            </router-link>
            <router-link
              to="/contact"
              class="flex-1 md:flex-none text-center px-5 py-3 bg-white/10 border border-white/20 text-white rounded-xl text-xs font-bold hover:bg-white/20 transition-colors"
            >
              {{ t('about_contact_page') }}
            </router-link>
          </div>
        </div>

      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Building2, ShieldCheck, Truck, Sparkles, Headphones } from '@lucide/vue'
import { siteApi } from '@/api/site'
import { useI18n } from '@/i18n'

const { t } = useI18n()
const about = ref({})
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await siteApi.getAbout()
    about.value = res.data
  } catch (err) {
    console.error("About data fetch error:", err)
  } finally {
    loading.value = false
  }
})
</script>
