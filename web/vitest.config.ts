/// <reference types="vitest" />
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

// Vitest config riêng (Phase G — split from vite.config.ts vì version drift
// giữa vite vs vitest's bundled vite gây type errors trong production build).
export default defineConfig({
  plugins: [react()],
  // plugin-react v6 defaults to JSX runtime detected from tsconfig — but
  // tsconfig.app.json excludes tests, so force automatic runtime here.
  esbuild: {
    jsx: 'automatic',
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
  },
});
