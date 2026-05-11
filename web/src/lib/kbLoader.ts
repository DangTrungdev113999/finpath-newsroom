import { extractHeadings, parseFrontmatter } from './kbParse';
import type { KbDoc } from './kbTypes';

// Vite import.meta.glob: at build time, every kb/bds/**/*.md is read as raw
// text and inlined into the JS bundle. Path resolves relative to this file:
//   web/src/lib/kbLoader.ts → ../../../kb/bds/**/*.md → repo-root/kb/bds/
// Dev mode needs vite.config.ts server.fs.allow ['..', '.'] (set in Task 1).
//
// Spike verified 2026-05-11: 21 files inline to 47KB gzipped bundle.
const bdsRawModules = import.meta.glob('../../../kb/bds/**/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>;

function pathToSlug(path: string): string {
  // '../../../kb/bds/frameworks/bds-res-land-bank-nav.md' → 'bds-res-land-bank-nav'
  const file = path.split('/').pop() ?? '';
  return file.replace(/\.md$/, '');
}

function buildDocs(
  modules: Record<string, string>,
  sector: 'bds' | 'bank' | 'ck',
): KbDoc[] {
  const docs: KbDoc[] = [];
  for (const [path, raw] of Object.entries(modules)) {
    const slug = pathToSlug(path);
    const { meta, body } = parseFrontmatter(raw);
    const headings = extractHeadings(body);
    docs.push({ slug, sector, meta, body, headings });
  }
  docs.sort((a, b) => a.slug.localeCompare(b.slug));
  return docs;
}

export const BDS_DOCS: KbDoc[] = buildDocs(bdsRawModules, 'bds');

// Bank + CK come later. Empty arrays so UI can show "sắp có" state safely.
export const BANK_DOCS: KbDoc[] = [];
export const CK_DOCS: KbDoc[] = [];

export function docsForSector(sector: 'bds' | 'bank' | 'ck'): KbDoc[] {
  if (sector === 'bds') return BDS_DOCS;
  if (sector === 'bank') return BANK_DOCS;
  return CK_DOCS;
}

export function findDoc(sector: 'bds' | 'bank' | 'ck', slug: string): KbDoc | undefined {
  return docsForSector(sector).find((d) => d.slug === slug);
}
