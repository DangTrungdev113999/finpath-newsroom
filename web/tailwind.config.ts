import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // shadcn/ui bridge — HSL CSS vars from active theme
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        // brand tokens — flip per theme
        brand: {
          DEFAULT: 'hsl(var(--brand))',
          hot: 'hsl(var(--brand-hot))',
          dim: 'hsl(var(--brand-dim))',
          fg: 'hsl(var(--brand-fg))',
        },
        rec: 'hsl(var(--rec))',
        done: 'hsl(var(--done))',
        warn: 'hsl(var(--warn))',
        // surface scale
        bg: {
          0: 'hsl(var(--bg-0))',
          1: 'hsl(var(--bg-1))',
          2: 'hsl(var(--bg-2))',
          3: 'hsl(var(--bg-3))',
        },
        fg: {
          0: 'hsl(var(--fg-0))',
          1: 'hsl(var(--fg-1))',
          2: 'hsl(var(--fg-2))',
          3: 'hsl(var(--fg-3))',
          4: 'hsl(var(--fg-4))',
        },
        // legacy callout (still used by InsightCallout)
        callout: {
          bg: '#FBF3DB',
          border: '#E9D77E',
          icon: '#A68A0E',
        },
      },
      fontFamily: {
        sans: ['var(--font-sans)'],
        serif: ['var(--font-serif)'],
        display: ['var(--font-serif)'],
        mono: ['var(--font-mono)'],
      },
      borderRadius: {
        sm: '4px',
        md: '6px',
        lg: '8px',
        xl: '12px',
        '2xl': '16px',
        '3xl': '24px',
        '4xl': '32px',
        pill: '999px',
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        glow: 'var(--shadow-glow)',
      },
      transitionDuration: {
        fast: '120ms',
        med: '180ms',
        slow: '320ms',
      },
      transitionTimingFunction: {
        'out-quart': 'cubic-bezier(0.25, 1, 0.5, 1)',
        'out-expo': 'cubic-bezier(0.22, 1, 0.36, 1)',
        'in-out-sine': 'cubic-bezier(0.65, 0, 0.35, 1)',
      },
      keyframes: {
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(4px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        'fade-up': 'fade-up 320ms cubic-bezier(0.25, 1, 0.5, 1) both',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
} satisfies Config;
