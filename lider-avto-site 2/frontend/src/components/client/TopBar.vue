<template>
  <div class="hidden md:block relative overflow-hidden bg-navy-gradient text-white/80 text-xs border-b border-white/10">
    <div class="absolute -top-10 right-1/4 w-64 h-32 rounded-full bg-brand-500/25 blur-3xl pointer-events-none" />
    <div class="container-custom relative flex items-center justify-between h-9">
      <div class="flex items-center gap-5">
        <a :href="`tel:${siteStore.phoneMain || '+998900000000'}`" class="font-semibold text-white/90 hover:text-white transition-colors">
          📞 {{ siteStore.phoneMain || '+998 90 000 00 00' }}
        </a>
        <span>🕘 {{ workHoursText }}</span>
      </div>
      <span class="text-accent-300 font-semibold">🚚 {{ t('topbar_free_delivery') }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSiteStore } from '@/stores/site'
import { useI18n } from '@/i18n'

const siteStore = useSiteStore()
const { t, locale } = useI18n()

const workHoursText = computed(() =>
  locale.value === 'uz' && siteStore.workHours ? siteStore.workHours : t('work_hours_text')
)
</script>
