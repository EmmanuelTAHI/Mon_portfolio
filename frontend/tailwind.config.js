/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        orbitron: ['Orbitron', 'system-ui', 'sans-serif'],
        inter: ['Inter', 'system-ui', 'sans-serif'],
        jetbrains: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        neonGreen: '#00ff9f',
        cyberBlue: '#00d9ff',
        accentPurple: '#8a2be2',
        darkBg: '#0a0f1c',
        lightBg: '#f5f7fa',
      },
      boxShadow: {
        'neon-green': '0 0 20px rgba(0, 255, 159, 0.6)',
        'neon-cyan': '0 0 20px rgba(0, 217, 255, 0.6)',
        'neon-purple': '0 0 20px rgba(138, 43, 226, 0.5)',
        'glow-green': '0 0 30px rgba(0, 255, 159, 0.4), 0 0 60px rgba(0, 255, 159, 0.2)',
        'glow-cyan': '0 0 30px rgba(0, 217, 255, 0.4), 0 0 60px rgba(0, 217, 255, 0.2)',
      },
      keyframes: {
        scanline: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        },
        glitch: {
          '0%, 100%': { transform: 'translate(0)' },
          '20%': { transform: 'translate(-2px, 2px)' },
          '40%': { transform: 'translate(-2px, -2px)' },
          '60%': { transform: 'translate(2px, 2px)' },
          '80%': { transform: 'translate(2px, -2px)' },
        },
        'cursor-blink': {
          '0%, 50%': { opacity: 1 },
          '50.01%, 100%': { opacity: 0 },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: 0.6, boxShadow: '0 0 20px rgba(0, 255, 159, 0.4)' },
          '50%': { opacity: 1, boxShadow: '0 0 30px rgba(0, 255, 159, 0.7)' },
        },
        radar: {
          '0%': { transform: 'rotate(0deg)', opacity: 0.8 },
          '100%': { transform: 'rotate(360deg)', opacity: 0 },
        },
        'fade-in-up': {
          '0%': { opacity: 0, transform: 'translateY(20px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        'fade-in': {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        'slide-in-right': {
          '0%': { opacity: 0, transform: 'translateX(10px)' },
          '100%': { opacity: 1, transform: 'translateX(0)' },
        },
        'border-glow': {
          '0%, 100%': { borderColor: 'rgba(255, 255, 255, 0.1)', boxShadow: '0 0 15px rgba(0, 255, 159, 0.1)' },
          '50%': { borderColor: 'rgba(0, 255, 159, 0.4)', boxShadow: '0 0 25px rgba(0, 255, 159, 0.2)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0) translateX(0)' },
          '33%': { transform: 'translateY(-6px) translateX(3px)' },
          '66%': { transform: 'translateY(3px) translateX(-3px)' },
        },
      },
      animation: {
        scanline: 'scanline 4s linear infinite',
        glitch: 'glitch 1.5s infinite',
        'cursor-blink': 'cursor-blink 1s steps(2, start) infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        radar: 'radar 3s linear infinite',
        'fade-in-up': 'fade-in-up 0.6s ease-out forwards',
        'fade-in': 'fade-in 0.5s ease-out forwards',
        'slide-in-right': 'slide-in-right 0.4s ease-out forwards',
        'border-glow': 'border-glow 3s ease-in-out infinite',
        float: 'float 6s ease-in-out infinite',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('daisyui'),
  ],
  daisyui: {
    themes: [
      {
        cyberdark: {
          primary: '#00ff9f',
          secondary: '#00d9ff',
          accent: '#8a2be2',
          neutral: '#1f2937',
          'base-100': '#0a0f1c',
          info: '#00d9ff',
          success: '#00ff9f',
          warning: '#f97316',
          error: '#ef4444',
        },
      },
      {
        cyberlight: {
          primary: '#00ff9f',
          secondary: '#00d9ff',
          accent: '#8a2be2',
          neutral: '#0f172a',
          'base-100': '#f5f7fa',
          info: '#00d9ff',
          success: '#00ff9f',
          warning: '#f97316',
          error: '#ef4444',
        },
      },
    ],
  },
}

