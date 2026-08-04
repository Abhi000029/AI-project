/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: '#0A0E14',
          panel: '#11161F',
          raised: '#171D29',
          border: '#232B3A',
        },
        text: {
          primary: '#E6EAF2',
          muted: '#8A93A6',
          faint: '#5A6478',
        },
        brand: {
          DEFAULT: '#6C8EFF',
          soft: '#8FA6FF',
          dim: '#3A4B99',
        },
        severity: {
          critical: '#FF4757',
          high: '#FF8B5E',
          medium: '#FFD166',
          low: '#6FCF97',
          info: '#7C9CFF',
        },
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        body: ['"IBM Plex Sans"', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
      keyframes: {
        scan: {
          '0%': { transform: 'translateY(0%)', opacity: '0.9' },
          '100%': { transform: 'translateY(100%)', opacity: '0.2' },
        },
        pulseDot: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.35' },
        },
      },
      animation: {
        scan: 'scan 1.4s ease-in-out infinite alternate',
        pulseDot: 'pulseDot 1.6s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
