/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand Colors — royal blue with a deeper navy tail
        brand: {
          50:  '#eef4ff',
          100: '#dde8ff',
          200: '#c3d6ff',
          300: '#9bb9ff',
          400: '#6b92fa',
          500: '#3d6ceb',
          600: '#2554d4',
          700: '#1c43ac',
          800: '#183a8c',
          900: '#17316f',
          950: '#0a1d40',
        },
        // Cool slate palette tuned for both themes
        slate: {
          50:  '#f7f9fc',
          100: '#edf1f7',
          200: '#e0e7f0',
          300: '#c8d3e2',
          400: '#93a1b7',
          500: '#64748b',
          600: '#46566b',
          700: '#2c3b52',
          800: '#15233b',
          900: '#0b1426',
          950: '#050b18',
        },
        // Orange accent
        accent: {
          50:  '#fff6ed',
          100: '#ffead5',
          200: '#ffd4a8',
          300: '#ffb56f',
          400: '#ff9136',
          500: '#f97316',
          600: '#e05e07',
          700: '#b94709',
          800: '#93390e',
          900: '#772f0f',
        },
        // Status colors
        success: '#10b981',
        warning: '#f59e0b',
        info:    '#3b82f6',
        danger:  '#ef4444',
      },
      fontFamily: {
        sans: ['Inter', 'Plus Jakarta Sans', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'xl':  '12px',
        '2xl': '16px',
        '3xl': '24px',
        '4xl': '32px',
      },
      boxShadow: {
        'card': '0 1px 2px rgba(15,23,42,0.04), 0 10px 30px -12px rgba(15,23,42,0.14)',
        'card-hover': '0 20px 45px -16px rgba(15,23,42,0.22), 0 6px 16px -8px rgba(15,23,42,0.10)',
        'glow': '0 0 0 1px rgba(61,108,235,0.20), 0 12px 34px -8px rgba(61,108,235,0.55)',
        'glow-accent': '0 0 0 1px rgba(249,115,22,0.18), 0 12px 34px -8px rgba(249,115,22,0.45)',
        'inner-light': 'inset 0 1px 0 rgba(255,255,255,0.65)',
        'dark-card': '0 1px 0 rgba(255,255,255,0.03) inset, 0 18px 40px -20px rgba(0,0,0,0.75)',
      },
      backgroundImage: {
        'brand-gradient': 'linear-gradient(135deg, #3d6ceb 0%, #2554d4 52%, #1c43ac 100%)',
        'accent-gradient': 'linear-gradient(135deg, #ffb56f 0%, #f97316 60%, #e05e07 100%)',
        'navy-gradient': 'linear-gradient(135deg, #0a1d40 0%, #0d2650 48%, #07152f 100%)',
        'mesh-light': 'radial-gradient(1000px 520px at 8% -8%, rgba(61,108,235,0.12), transparent 62%), radial-gradient(820px 460px at 102% 0%, rgba(249,115,22,0.10), transparent 58%)',
        'mesh-dark': 'radial-gradient(1100px 600px at 12% -10%, rgba(61,108,235,0.22), transparent 64%), radial-gradient(900px 520px at 104% 0%, rgba(249,115,22,0.12), transparent 58%)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'pulse-slow': 'pulse 2.5s infinite',
        'spin-slow': 'spin 2s linear infinite',
        'bounce-x': 'bounceX 1s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(16px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        bounceX: {
          '0%, 100%': { transform: 'translateX(0)' },
          '50%': { transform: 'translateX(4px)' },
        },
      },
    },
  },
  plugins: [],
}
