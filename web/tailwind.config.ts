import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        callout: {
          bg: '#FBF3DB',          // Notion yellow_background pastel
          border: '#E9D77E',
          icon: '#A68A0E',
        },
      },
      typography: {
        DEFAULT: {
          css: {
            'h2': { fontSize: '1.5rem', fontWeight: '700', marginTop: '2rem' },
          },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
