import { ref, computed } from 'vue'

const STORAGE_KEY = 'lider_theme'
const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

const theme = ref(localStorage.getItem(STORAGE_KEY) || (mediaQuery.matches ? 'dark' : 'light'))

let transitionTimer = null

function applyTheme(value, animate = false) {
  const root = document.documentElement

  if (animate) {
    root.classList.add('theme-transition')
    clearTimeout(transitionTimer)
    transitionTimer = setTimeout(() => root.classList.remove('theme-transition'), 380)
  }

  if (value === 'dark') {
    root.classList.add('dark')
  } else {
    root.classList.remove('dark')
  }
  root.setAttribute('data-theme', value)
  root.style.colorScheme = value
}

applyTheme(theme.value)

mediaQuery.addEventListener('change', (e) => {
  if (!localStorage.getItem(STORAGE_KEY)) {
    theme.value = e.matches ? 'dark' : 'light'
    applyTheme(theme.value, true)
  }
})

export function useTheme() {
  const isDark = computed(() => theme.value === 'dark')

  function toggle() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    localStorage.setItem(STORAGE_KEY, theme.value)
    applyTheme(theme.value, true)
  }

  function setTheme(value) {
    theme.value = value
    localStorage.setItem(STORAGE_KEY, value)
    applyTheme(value, true)
  }

  return { theme, isDark, toggle, setTheme }
}
