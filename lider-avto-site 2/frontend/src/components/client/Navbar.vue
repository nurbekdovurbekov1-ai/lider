<template>
  <!-- Desktop Navbar (md+) -->
  <header class="nav-glass sticky top-0 z-50">
    <div class="container-custom">
      <div class="flex items-center justify-between h-16">

        <!-- Logo -->
        <router-link to="/" class="group flex items-center gap-2.5 flex-shrink-0">
          <span class="hidden sm:grid w-9 h-9 rounded-xl bg-brand-gradient text-white place-items-center font-extrabold text-lg shadow-glow transition-transform duration-300 group-hover:-rotate-6">L</span>
          <span class="font-extrabold text-2xl text-brand-950 dark:text-white tracking-tight">Lider <span class="text-accent-500">Avto</span></span>
        </router-link>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center gap-6">
          <router-link to="/" class="nav-link" :class="{ active: route.path === '/' }">{{ t('nav_home') }}</router-link>
          <router-link to="/catalog" class="nav-link" :class="{ active: route.path.startsWith('/catalog') }">{{ t('nav_catalog') }}</router-link>
          <router-link to="/about" class="nav-link" :class="{ active: route.path === '/about' }">{{ t('nav_about') }}</router-link>
          <router-link to="/contact" class="nav-link" :class="{ active: route.path === '/contact' }">{{ t('nav_contact') }}</router-link>
          <router-link to="/profile?tab=orders" class="nav-link">{{ t('nav_orders') }}</router-link>
        </nav>

        <!-- Right Actions -->
        <div class="flex items-center gap-1.5 sm:gap-2">

          <!-- Language Switcher -->
          <div class="hidden sm:flex items-center rounded-xl border border-slate-200 dark:border-slate-600 overflow-hidden">
            <button
              v-for="l in locales"
              :key="l.code"
              @click="setLocale(l.code)"
              class="px-2 py-1.5 text-[11px] font-bold transition-colors"
              :class="locale === l.code
                ? 'bg-brand-600 text-white'
                : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700'"
            >{{ l.label }}</button>
          </div>

          <!-- Theme Toggle -->
          <button
            @click="toggleTheme"
            class="theme-toggle"
            :aria-label="isDark ? t('theme_light') : t('theme_dark')"
          >
            <Sun v-if="isDark" class="w-5 h-5" />
            <Moon v-else class="w-5 h-5" />
          </button>

          <!-- Live Search (Desktop only) -->
          <div class="hidden lg:block w-52 focus-within:w-80 transition-all duration-300">
            <LiveSearch
              :placeholder="t('nav_search')"
              min-dropdown-width="380"
              custom-input-class="pl-9 pr-8 py-2 rounded-xl border border-slate-200 bg-slate-50 text-sm text-slate-700 placeholder-slate-400 focus:bg-white dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100 dark:placeholder-slate-500 dark:focus:bg-slate-800"
            />
          </div>

          <!-- Mobile Search Toggle Button (md:hidden) -->
          <button
            @click="mobileSearchOpen = !mobileSearchOpen"
            class="md:hidden p-2 text-slate-700 dark:text-slate-300 hover:text-brand-600 dark:hover:text-accent-400 transition-colors rounded-xl"
            :aria-label="t('common_search')"
          >
            <Search class="w-5 h-5" />
          </button>

          <!-- Cart Icon -->
          <router-link to="/cart" class="relative p-2 text-slate-700 dark:text-slate-300 hover:text-brand-600 dark:hover:text-accent-400 transition-colors">
            <ShoppingCart class="w-5 h-5 sm:w-6 sm:h-6" />
            <span v-if="cartStore.itemCount > 0" class="absolute top-0 right-0 w-5 h-5 bg-red-500 text-white text-[11px] font-bold rounded-full flex items-center justify-center border-2 border-white dark:border-slate-900 transform translate-x-1 -translate-y-1">
              {{ cartStore.itemCount }}
            </span>
          </router-link>


          <!-- User Menu (desktop) -->
          <div v-if="authStore.isLoggedIn" class="hidden md:block relative" ref="userMenuRef">
            <button @click="userMenuOpen = !userMenuOpen" class="flex items-center gap-2 btn-md btn-primary">
              <User class="w-4 h-4" />
              <span class="hidden sm:block text-sm font-medium">{{ t('nav_profile') }}</span>
            </button>
            <Transition name="modal">
              <div v-if="userMenuOpen" class="absolute right-0 mt-2 w-52 bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-100 dark:border-slate-700 py-2 z-50">
                <router-link to="/profile" @click="userMenuOpen = false" class="dropdown-item">
                  <User class="w-4 h-4" /> {{ t('nav_profile') }}
                </router-link>
                <router-link to="/profile?tab=orders" @click="userMenuOpen = false" class="dropdown-item">
                  <Package class="w-4 h-4" /> {{ t('nav_orders') }}
                </router-link>
                <router-link to="/profile?tab=addresses" @click="userMenuOpen = false" class="dropdown-item">
                  <MapPin class="w-4 h-4" /> {{ t('nav_addresses') }}
                </router-link>
                <template v-if="authStore.isAdmin">
                  <div class="h-px bg-slate-100 dark:bg-slate-700 my-1 mx-3" />
                  <router-link to="/admin/dashboard" @click="userMenuOpen = false" class="dropdown-item text-brand-600 dark:text-brand-400">
                    <LayoutDashboard class="w-4 h-4" /> {{ t('nav_admin') }}
                  </router-link>
                </template>
                <div class="h-px bg-slate-100 dark:bg-slate-700 my-1 mx-3" />
                <button @click="handleLogout" class="dropdown-item w-full text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10">
                  <LogOut class="w-4 h-4" /> {{ t('nav_logout') }}
                </button>
              </div>
            </Transition>
          </div>

          <!-- Login Button (desktop) -->
          <button v-if="!authStore.isLoggedIn" @click="authModalOpen = true" class="hidden md:inline-flex btn-md btn-primary" id="navbar-login-btn">
            <User class="w-4 h-4" />
            <span class="hidden sm:inline">{{ t('nav_login') }}</span>
          </button>

          <!-- Hamburger (mobile only) - still available -->
          <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden btn-ghost btn-sm rounded-xl p-2">
            <Menu v-if="!mobileMenuOpen" class="w-5 h-5" />
            <X v-else class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Live Search Slide Bar -->
    <Transition name="slide-down">
      <div v-if="mobileSearchOpen" class="md:hidden border-t border-[color:var(--border)] bg-[color:var(--glass)] backdrop-blur-xl px-4 py-3 shadow-md">
        <div class="flex items-center gap-2">
          <div class="flex-1">
            <LiveSearch
              :autofocus="true"
              :placeholder="t('nav_search_placeholder')"
              @select="mobileSearchOpen = false"
              @search-submit="mobileSearchOpen = false"
            />
          </div>
          <button
            @click="mobileSearchOpen = false"
            class="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-xl"
          >
            <X class="w-5 h-5" />
          </button>
        </div>
      </div>
    </Transition>

    <!-- Mobile Hamburger Drawer (slide from top) -->
    <Transition name="slide-down">
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-[color:var(--border)] bg-[color:var(--surface-1)] px-4 py-4 flex flex-col gap-2 shadow-lg">
        <!-- Live Search in drawer -->
        <div class="mb-2">
          <LiveSearch
            :placeholder="t('nav_search_products')"
            @select="mobileMenuOpen = false"
            @search-submit="mobileMenuOpen = false"
          />
        </div>
        <router-link to="/" @click="mobileMenuOpen = false" class="mobile-nav-link" :class="{ 'text-brand-600 bg-brand-50 dark:bg-brand-500/15 dark:text-brand-400': route.path === '/' }">
          <Home class="w-4 h-4" /> {{ t('nav_home') }}
        </router-link>
        <router-link to="/catalog" @click="mobileMenuOpen = false" class="mobile-nav-link" :class="{ 'text-brand-600 bg-brand-50 dark:bg-brand-500/15 dark:text-brand-400': route.path.startsWith('/catalog') }">
          <Grid class="w-4 h-4" /> {{ t('nav_catalog') }}
        </router-link>
        <router-link to="/profile?tab=orders" @click="mobileMenuOpen = false" class="mobile-nav-link">
          <Package class="w-4 h-4" /> {{ t('nav_orders') }}
        </router-link>
        <router-link to="/about" @click="mobileMenuOpen = false" class="mobile-nav-link" :class="{ 'text-brand-600 bg-brand-50 dark:bg-brand-500/15 dark:text-brand-400': route.path === '/about' }">
          <Info class="w-4 h-4" /> {{ t('nav_about') }}
        </router-link>
        <router-link to="/contact" @click="mobileMenuOpen = false" class="mobile-nav-link" :class="{ 'text-brand-600 bg-brand-50 dark:bg-brand-500/15 dark:text-brand-400': route.path === '/contact' }">
          <Phone class="w-4 h-4" /> {{ t('nav_contact') }}
        </router-link>
        <template v-if="authStore.isLoggedIn">
          <div class="h-px bg-slate-100 dark:bg-slate-700 my-1" />
          <router-link to="/profile" @click="mobileMenuOpen = false" class="mobile-nav-link">
            <User class="w-4 h-4" /> {{ t('nav_profile') }}
          </router-link>
          <template v-if="authStore.isAdmin">
            <router-link to="/admin/dashboard" @click="mobileMenuOpen = false" class="mobile-nav-link text-brand-600 dark:text-brand-400">
              <LayoutDashboard class="w-4 h-4" /> {{ t('nav_admin') }}
            </router-link>
          </template>
          <button @click="handleLogout; mobileMenuOpen = false" class="mobile-nav-link text-red-500 w-full text-left">
            <LogOut class="w-4 h-4" /> {{ t('nav_logout') }}
          </button>
        </template>
        <template v-else>
          <div class="h-px bg-slate-100 dark:bg-slate-700 my-1" />
          <button @click="authModalOpen = true; mobileMenuOpen = false" class="btn-md btn-primary w-full">
            <User class="w-4 h-4" /> {{ t('nav_login_register') }}
          </button>
        </template>
        <!-- Mobile: Language & Theme -->
        <div class="h-px bg-slate-100 dark:bg-slate-700 my-1" />
        <div class="flex items-center justify-between px-4 py-2">
          <div class="flex items-center rounded-xl border border-slate-200 dark:border-slate-600 overflow-hidden">
            <button
              v-for="l in locales"
              :key="l.code"
              @click="setLocale(l.code)"
              class="px-3 py-1.5 text-xs font-bold transition-colors"
              :class="locale === l.code
                ? 'bg-brand-600 text-white'
                : 'text-slate-500 dark:text-slate-400'"
            >{{ l.label }}</button>
          </div>
          <button
            @click="toggleTheme"
            class="flex items-center gap-2 px-3 py-1.5 rounded-xl border border-[color:var(--border)] bg-[color:var(--surface-3)] text-sm font-medium text-slate-600 dark:text-slate-300"
          >
            <Sun v-if="isDark" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
            {{ isDark ? t('theme_light') : t('theme_dark') }}
          </button>
        </div>
      </div>
    </Transition>
  </header>

  <!-- ─── Mobile Bottom Tab Bar (md dan kichik ekranlar uchun) ─── -->
  <nav class="md:hidden fixed bottom-0 left-0 right-0 z-50 nav-glass border-t safe-area-bottom">
    <div class="grid grid-cols-5 h-16">

      <!-- Bosh sahifa -->
      <router-link to="/" class="bottom-tab" :class="{ active: route.path === '/' }">
        <Home class="w-5 h-5" />
        <span>{{ t('nav_home') }}</span>
      </router-link>

      <!-- Katalog -->
      <router-link to="/catalog" class="bottom-tab" :class="{ active: route.path.startsWith('/catalog') }">
        <Grid class="w-5 h-5" />
        <span>{{ t('nav_catalog') }}</span>
      </router-link>

      <!-- Buyurtmalarim -->
      <router-link to="/profile?tab=orders" class="bottom-tab" :class="{ active: route.path === '/profile' && route.query.tab === 'orders' }">
        <Package class="w-5 h-5" />
        <span>{{ t('nav_orders') }}</span>
      </router-link>

      <!-- Savat -->
      <router-link to="/cart" class="bottom-tab relative" :class="{ active: route.path === '/cart' }">
        <div class="relative">
          <ShoppingCart class="w-5 h-5" />
          <span v-if="cartStore.itemCount > 0" class="absolute -top-1.5 -right-2 w-4 h-4 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
            {{ cartStore.itemCount > 9 ? '9+' : cartStore.itemCount }}
          </span>
        </div>
        <span>{{ t('cart_title') }}</span>
      </router-link>

      <!-- Profil -->
      <button
        v-if="!authStore.isLoggedIn"
        @click="authModalOpen = true"
        class="bottom-tab"
      >
        <User class="w-5 h-5" />
        <span>{{ t('nav_login') }}</span>
      </button>
      <router-link v-else to="/profile" class="bottom-tab" :class="{ active: route.path === '/profile' && !route.query.tab }">
        <User class="w-5 h-5" />
        <span>{{ t('nav_profile') }}</span>
      </router-link>

    </div>
  </nav>

  <!-- Auth Modal -->
  <AuthModal :open="authModalOpen" @close="authModalOpen = false" @success="authModalOpen = false" />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Search, ShoppingCart, User, Package, MapPin, LogOut, Menu, X, LayoutDashboard, Home, Grid, Phone, Info, Sun, Moon } from '@lucide/vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useAlertStore } from '@/stores/alert'
import { useI18n } from '@/i18n'
import { useTheme } from '@/stores/theme'
import AuthModal from '@/components/client/AuthModal.vue'
import LiveSearch from '@/components/client/LiveSearch.vue'

const router = useRouter()
const route  = useRoute()
const authStore  = useAuthStore()
const cartStore  = useCartStore()
const alertStore = useAlertStore()
const { t, locale, setLocale, locales } = useI18n()
const { isDark, toggle: toggleTheme } = useTheme()

const searchQuery      = ref('')
const mobileMenuOpen   = ref(false)
const mobileSearchOpen = ref(false)
const userMenuOpen     = ref(false)
const authModalOpen    = ref(false)
const userMenuRef      = ref(null)

function doSearch() {
  if (searchQuery.value.trim()) {
    router.push({ name: 'catalog', query: { search: searchQuery.value.trim() } })
    searchQuery.value = ''
    mobileMenuOpen.value = false
  }
}

async function handleLogout() {
  userMenuOpen.value = false
  await authStore.logout()
  cartStore.resetCart()
  alertStore.success('Tizimdan chiqdingiz')
  router.push('/')
}

function handleClickOutside(e) {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    userMenuOpen.value = false
  }
}

function openAuthModal() { authModalOpen.value = true }

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('auth:open-modal', openAuthModal)
})
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('auth:open-modal', openAuthModal)
})
</script>

<style scoped>
/* Desktop nav links */
.nav-link {
  @apply relative px-1 py-2 text-sm font-semibold transition-colors duration-200;
  color: var(--text-secondary);
}
.nav-link::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -2px;
  height: 2px;
  border-radius: 99px;
  background: linear-gradient(90deg, var(--brand-primary), var(--brand-accent));
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.25s ease;
}
.nav-link:hover { color: var(--brand-primary); }
.nav-link:hover::after { transform: scaleX(1); }
.nav-link.active { color: var(--brand-primary); }
.nav-link.active::after { transform: scaleX(1); }
.dark .nav-link { color: var(--text-secondary); }
.dark .nav-link:hover,
.dark .nav-link.active { color: #9bb9ff; }

/* Theme switch button */
.theme-toggle {
  @apply grid place-items-center w-10 h-10 rounded-xl border transition-all duration-300;
  background: var(--surface-3);
  border-color: var(--border);
  color: var(--text-secondary);
}
.theme-toggle:hover {
  color: var(--brand-primary);
  border-color: var(--brand-primary);
  transform: rotate(-12deg);
  box-shadow: 0 8px 20px -10px rgba(61, 108, 235, 0.7);
}
.dark .theme-toggle:hover { color: #ffb56f; border-color: rgba(249, 115, 22, 0.5); box-shadow: 0 8px 20px -10px rgba(249, 115, 22, 0.5); }

/* Dropdown items */
.dropdown-item {
  @apply flex items-center gap-2.5 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 hover:text-slate-900 transition-colors duration-150 w-full text-left dark:text-slate-300 dark:hover:bg-slate-700 dark:hover:text-white;
}

/* Hamburger drawer links */
.mobile-nav-link {
  @apply flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-700 hover:bg-slate-50 hover:text-slate-900 transition-colors dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-white;
}

/* Bottom Tab Bar items */
.bottom-tab {
  @apply flex flex-col items-center justify-center gap-0.5 text-slate-400 text-[10px] font-medium transition-all duration-200 w-full dark:text-slate-500;
}
.bottom-tab.active {
  @apply text-brand-600 dark:text-brand-400;
}
.bottom-tab.active svg {
  @apply text-brand-600 dark:text-brand-400;
}
.bottom-tab.active::before {
  content: '';
  position: absolute;
  top: 0;
  width: 22px;
  height: 2px;
  border-radius: 99px;
  background: linear-gradient(90deg, var(--brand-primary), var(--brand-accent));
}
.bottom-tab { position: relative; }

/* Slide down animation for hamburger menu */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.25s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Safe area for iOS notch */
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
</style>
