<template>
  <footer class="relative overflow-hidden bg-navy-gradient text-white pt-16 pb-8 mt-10">
    <!-- top accent line -->
    <div class="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-accent-500 via-accent-400 to-brand-500" />
    <div class="glow-blob -top-24 -right-16 w-72 h-72 bg-brand-500/25" />
    <div class="glow-blob -bottom-28 -left-20 w-72 h-72 bg-accent-500/15" />

    <div class="container-custom relative">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-10 mb-16">
        
        <!-- Brand -->
        <div class="col-span-1">
          <h3 class="font-extrabold text-2xl mb-4 tracking-tight">Lider <span class="text-accent-500">Avto</span></h3>
          <p class="text-sm text-slate-300/80 leading-relaxed max-w-[220px]">
            {{ footerAboutText }}
          </p>
        </div>

        <!-- Links 1 -->
        <div class="col-span-1 flex flex-col gap-3 text-sm">
          <router-link to="/catalog" class="footer-link">{{ t('footer_catalog') }}</router-link>
          <router-link to="/about" class="footer-link">{{ t('footer_about') }}</router-link>
          <router-link to="/contact" class="footer-link">{{ t('footer_contact') }}</router-link>
        </div>

        <!-- Contacts -->
        <div class="col-span-1 flex flex-col gap-3 text-sm">
          <a v-if="siteStore.telegramUrl" :href="siteStore.telegramUrl" target="_blank" class="footer-link">Telegram</a>
          <a v-if="siteStore.instagramUrl" :href="siteStore.instagramUrl" target="_blank" class="footer-link">Instagram</a>
          <p class="text-slate-300/80">
            <span class="font-semibold">{{ t('footer_address') }}</span> {{ siteStore.address || "O'zbekiston" }}
          </p>
          <a v-if="siteStore.phoneMain" :href="`tel:${siteStore.phoneMain}`" class="footer-link">{{ siteStore.phoneMain }}</a>
        </div>

        <!-- Terms -->
        <div class="col-span-1 flex flex-col gap-3 text-sm">
          <a href="#" class="footer-link">{{ t('footer_privacy') }}</a>
          <a href="#" class="footer-link">{{ t('footer_terms') }}</a>
        </div>
      </div>

      <!-- Copyright -->
      <div class="text-center text-xs text-slate-300/60 pt-8 border-t border-white/10">
        © {{ new Date().getFullYear() }} {{ footerCopyrightText }}
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useSiteStore } from '@/stores/site'
import { useI18n } from '@/i18n'

const siteStore = useSiteStore()
const { t, locale } = useI18n()

const footerAboutText = computed(() =>
  locale.value === 'uz' && siteStore.footerAbout ? siteStore.footerAbout : t('footer_about_text')
)
const footerCopyrightText = computed(() =>
  locale.value === 'uz' && siteStore.footerCopyright ? siteStore.footerCopyright : t('footer_copyright_text')
)

onMounted(() => {
  siteStore.fetchSettings()
})
</script>

<style scoped>
.footer-link {
  @apply text-slate-300/80 hover:text-white transition-colors;
  display: inline-block;
  width: fit-content;
}
.footer-link:hover { transform: translateX(2px); }
.footer-link { transition: color 0.2s ease, transform 0.2s ease; }
</style>
