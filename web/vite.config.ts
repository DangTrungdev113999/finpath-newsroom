import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Phase G GitHub Pages deploy: base = '/finpath-newsroom/' khi build production.
// Dev (vite) giữ base '/' để localhost:5174 work bình thường.
// Tests config moved to vitest.config.ts (vite + vitest version drift).
const isProd = process.env.NODE_ENV === 'production' || process.env.VITE_DEPLOY === '1';

export default defineConfig({
  plugins: [react()],
  base: isProd ? '/finpath-newsroom/' : '/',
  server: {
    // KB markdown files (kb/) live sibling to web/. import.meta.glob('../../../kb/...')
    // from src/lib/kbLoader.ts needs fs.allow for dev server. Build mode resolves
    // statically and doesn't use this — keeping symmetric for clarity.
    fs: { allow: ['..', '.'] },
  },
});
