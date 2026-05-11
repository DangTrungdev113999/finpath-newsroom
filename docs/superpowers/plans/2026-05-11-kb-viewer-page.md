# KB Viewer Page `/tai-lieu` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a static-page KB viewer at `/tai-lieu` that visualizes 21 BĐS knowledge-base markdown files (kb/bds/frameworks/*.md), with a 2-panel sidebar (Fuse.js search + grouped tree) and a markdown content panel. New KB files appear automatically on next `npm run build` — no config edits.

**Architecture:** Vite `import.meta.glob` inlines raw `.md` content at build time (eager, ~47KB gzipped). Frontmatter parsed by tiny inline regex parser. Group-by-prefix derives the "phụ lục" tree from filename. Search via Fuse.js with title/heading/body fields. Markdown rendered through a KB-specific wrapper (separate from article Markdown.tsx) that adds `rehype-slug` for heading anchors and routes `[text](./other.md)` cross-references through React Router. Bank + CK tabs render disabled placeholders.

**Tech Stack:** React 19 + Vite 8 + TypeScript + React Router DOM v6 + Tailwind + Fuse.js + react-markdown + rehype-slug + github-slugger. Tests: Vitest + jsdom.

**Spec reference:** `docs/superpowers/specs/2026-05-11-kb-viewer-page-design.md`

---

## File map

**New files (in `web/`):**

| Path | Responsibility |
|---|---|
| `src/lib/kbTypes.ts` | TypeScript types: KbMeta, KbDoc, Heading, GroupConfig |
| `src/lib/kbTree.ts` | BDS_GROUPS config + BDS_TITLES map + groupForSlug + titleForSlug |
| `src/lib/kbTree.test.ts` | Tests for groupForSlug (incl. catch-all) + titleForSlug fallback chain |
| `src/lib/kbParse.ts` | Pure helpers: parseFrontmatter + extractHeadings + slugify |
| `src/lib/kbParse.test.ts` | Tests for parser + heading extraction + slug consistency |
| `src/lib/kbLoader.ts` | Vite import.meta.glob → assemble BDS_DOCS |
| `src/components/kb/KbMarkdown.tsx` | react-markdown wrapper with rehype-slug + internal link routing |
| `src/components/kb/KbContent.tsx` | Header strip (title/meta/applies_to chips) + KbMarkdown body |
| `src/components/kb/KbTree.tsx` | Sidebar tree render — groups, collapse/expand, active state |
| `src/components/kb/KbSearch.tsx` | Fuse.js search box + results popup with snippet highlight |
| `src/components/kb/KbTabs.tsx` | 3 sector tabs (BĐS active, Bank/CK disabled "sắp có") |
| `src/components/kb/KbSidebar.tsx` | Compose tabs + search + tree, handle mobile drawer state |
| `src/pages/KbPage.tsx` | Route handler, URL state (sector + slug), 2-panel layout |

**Edits:**

| Path | Change |
|---|---|
| `vite.config.ts` | Add `server.fs.allow: ['..', '.']` |
| `package.json` | Add deps: fuse.js, rehype-slug, github-slugger |
| `src/App.tsx` | Add routes /tai-lieu + /tai-lieu/:slug |
| `src/components/Header.tsx` | Add 3rd nav link "Tài liệu" |

---

## Task 1: Install dependencies + Vite config + types stub

**Files:**
- Modify: `web/package.json`
- Modify: `web/vite.config.ts`
- Create: `web/src/lib/kbTypes.ts`

- [ ] **Step 1: Install runtime deps**

Run from `web/`:

    npm install fuse.js rehype-slug github-slugger

Expected: 3 packages added to dependencies. No vulnerabilities. Lock file updated.

- [ ] **Step 2: Update `vite.config.ts` to allow glob outside web/ root**

Open `web/vite.config.ts`. Replace existing content with:

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

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
```

- [ ] **Step 3: Create types module**

Create `web/src/lib/kbTypes.ts`:

```ts
export interface KbMeta {
  category?: string;
  title?: string;
  last_updated?: string;
  applies_to?: string[];
  notion_page_id?: string;
  source_url?: string;
  [extra: string]: unknown;
}

export interface Heading {
  level: 2 | 3;
  text: string;
  slug: string;
}

export interface KbDoc {
  slug: string;
  sector: 'bds' | 'bank' | 'ck';
  meta: KbMeta;
  body: string;
  headings: Heading[];
}

export interface GroupConfig {
  id: string;
  icon: string;
  label: string;
  match: (slug: string) => boolean;
}
```

- [ ] **Step 4: Verify build still works**

Run from `web/`:

    npx tsc --noEmit

Expected: no errors.

- [ ] **Step 5: Commit**

    git add web/package.json web/package-lock.json web/vite.config.ts web/src/lib/kbTypes.ts
    git commit -m "feat(kb): install deps + vite fs.allow + types stub"

---

## Task 2: kbTree.ts — group config + title map

**Files:**
- Create: `web/src/lib/kbTree.ts`
- Create: `web/src/lib/kbTree.test.ts`

- [ ] **Step 1: Write failing tests**

Create `web/src/lib/kbTree.test.ts`:

```ts
import { describe, expect, it } from 'vitest';
import { BDS_GROUPS, BDS_TITLES, groupForSlug, titleForSlug } from './kbTree';

describe('BDS_GROUPS — catch-all guarantee', () => {
  it('last group matches anything (catch-all)', () => {
    const last = BDS_GROUPS[BDS_GROUPS.length - 1];
    expect(last.id).toBe('other');
    expect(last.match('completely-unknown-slug')).toBe(true);
  });

  it('master slug matches master group', () => {
    expect(groupForSlug('bds-industry-master-reference').id).toBe('master');
  });

  it('res prefix → residential group', () => {
    expect(groupForSlug('bds-res-land-bank-nav').id).toBe('res');
    expect(groupForSlug('bds-res-project-lifecycle').id).toBe('res');
  });

  it('macro/legal/debt/revenue/hybrid prefixes → general group', () => {
    expect(groupForSlug('bds-macro-cycle-credit').id).toBe('general');
    expect(groupForSlug('bds-legal-framework').id).toBe('general');
    expect(groupForSlug('bds-debt-leverage').id).toBe('general');
    expect(groupForSlug('bds-revenue-recognition-vas').id).toBe('general');
    expect(groupForSlug('bds-hybrid-business-models').id).toBe('general');
  });

  it('kcn/retail/office/resort/dc prefixes → respective groups', () => {
    expect(groupForSlug('bds-kcn-lease-structure').id).toBe('kcn');
    expect(groupForSlug('bds-retail-footfall-mechanism').id).toBe('retail');
    expect(groupForSlug('bds-office-class-tiering').id).toBe('office');
    expect(groupForSlug('bds-resort-tourism-cycle').id).toBe('resort');
    expect(groupForSlug('bds-dc-hyperscaler-power').id).toBe('dc');
  });

  it('unknown slug falls through to catch-all "other"', () => {
    expect(groupForSlug('bds-newcategory-foo').id).toBe('other');
    expect(groupForSlug('something-random').id).toBe('other');
  });
});

describe('titleForSlug — fallback chain', () => {
  it('returns mapped VN title when in BDS_TITLES', () => {
    expect(titleForSlug('bds-res-land-bank-nav', '', undefined)).toBe('Quỹ đất & NAV');
    expect(titleForSlug('bds-industry-master-reference', '', undefined)).toBe('Tham chiếu ngành');
  });

  it('falls back to H1 of body when slug not mapped', () => {
    const body = '# My Custom Title\n\nbody content';
    expect(titleForSlug('bds-unknown-foo', body, undefined)).toBe('My Custom Title');
  });

  it('falls back to frontmatter title when no H1', () => {
    expect(titleForSlug('bds-unknown-foo', 'body without h1', 'Frontmatter Title'))
      .toBe('Frontmatter Title');
  });

  it('falls back to slug when nothing else', () => {
    expect(titleForSlug('bds-unknown-foo', 'body', undefined)).toBe('bds-unknown-foo');
  });

  it('mapped title wins over body H1 + frontmatter (consistency rule)', () => {
    const body = '# Ngành bất động sản Việt Nam — Tham chiếu ngành';
    expect(titleForSlug('bds-industry-master-reference', body, 'Some Frontmatter Title'))
      .toBe('Tham chiếu ngành');
  });
});

describe('BDS_TITLES — all 21 expected slugs present', () => {
  const expectedSlugs = [
    'bds-industry-master-reference',
    'bds-macro-cycle-credit',
    'bds-legal-framework',
    'bds-debt-leverage',
    'bds-revenue-recognition-vas',
    'bds-hybrid-business-models',
    'bds-res-land-bank-nav',
    'bds-res-project-lifecycle',
    'bds-res-presales-backlog',
    'bds-kcn-fdi-demand-mechanism',
    'bds-kcn-lease-structure',
    'bds-kcn-inventory-pricing',
    'bds-retail-footfall-mechanism',
    'bds-retail-anchor-vs-sme-tenants',
    'bds-retail-tenant-mix-quality',
    'bds-office-class-tiering',
    'bds-office-hybrid-work-impact',
    'bds-resort-tourism-cycle',
    'bds-resort-condotel-legal-pitfalls',
    'bds-resort-hybrid-model',
    'bds-dc-hyperscaler-power',
  ];
  for (const slug of expectedSlugs) {
    it(`has VN title for ${slug}`, () => {
      expect(BDS_TITLES[slug]).toBeTruthy();
      expect(BDS_TITLES[slug]).not.toBe(slug);
    });
  }
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run from `web/`:

    npx vitest run src/lib/kbTree.test.ts

Expected: FAIL — `Cannot find module './kbTree'`.

- [ ] **Step 3: Implement `kbTree.ts`**

Create `web/src/lib/kbTree.ts`:

```ts
import type { GroupConfig } from './kbTypes';

// BĐS group config. Match order = display order in sidebar. First match wins.
// Last entry "other" is a catch-all so new KB files never disappear from the tree.
export const BDS_GROUPS: GroupConfig[] = [
  { id: 'master',  icon: '🏛', label: 'Tham chiếu ngành',
    match: (slug) => slug === 'bds-industry-master-reference' },
  { id: 'general', icon: '📊', label: 'Khái niệm chung',
    match: (slug) => /^bds-(macro|legal|debt|revenue|hybrid)-/.test(slug) },
  { id: 'res',     icon: '🏘', label: 'Phát triển dân cư',
    match: (slug) => /^bds-res-/.test(slug) },
  { id: 'kcn',     icon: '🏭', label: 'Khu công nghiệp',
    match: (slug) => /^bds-kcn-/.test(slug) },
  { id: 'retail',  icon: '🛍', label: 'Bán lẻ trung tâm',
    match: (slug) => /^bds-retail-/.test(slug) },
  { id: 'office',  icon: '🏢', label: 'Văn phòng cho thuê',
    match: (slug) => /^bds-office-/.test(slug) },
  { id: 'resort',  icon: '🏖', label: 'Nghỉ dưỡng',
    match: (slug) => /^bds-resort-/.test(slug) },
  { id: 'dc',      icon: '🖥', label: 'Trung tâm dữ liệu',
    match: (slug) => /^bds-dc-/.test(slug) },
  { id: 'other',   icon: '📎', label: 'Khác',
    match: () => true },
];

export const BDS_TITLES: Record<string, string> = {
  'bds-industry-master-reference': 'Tham chiếu ngành',
  'bds-macro-cycle-credit': 'Chu kỳ vĩ mô & tín dụng',
  'bds-legal-framework': 'Khung pháp lý',
  'bds-debt-leverage': 'Đòn bẩy nợ',
  'bds-revenue-recognition-vas': 'Ghi nhận doanh thu (VAS)',
  'bds-hybrid-business-models': 'Mô hình kinh doanh lai',
  'bds-res-land-bank-nav': 'Quỹ đất & NAV',
  'bds-res-project-lifecycle': 'Vòng đời dự án',
  'bds-res-presales-backlog': 'Bán trước & backlog',
  'bds-kcn-fdi-demand-mechanism': 'Cơ chế cầu FDI',
  'bds-kcn-lease-structure': 'Cấu trúc thuê đất',
  'bds-kcn-inventory-pricing': 'Tồn kho & giá thuê',
  'bds-retail-footfall-mechanism': 'Lưu lượng khách',
  'bds-retail-anchor-vs-sme-tenants': 'Anchor & khách thuê SME',
  'bds-retail-tenant-mix-quality': 'Chất lượng tenant mix',
  'bds-office-class-tiering': 'Phân hạng văn phòng',
  'bds-office-hybrid-work-impact': 'Tác động làm việc kết hợp',
  'bds-resort-tourism-cycle': 'Chu kỳ du lịch',
  'bds-resort-condotel-legal-pitfalls': 'Cạm bẫy pháp lý condotel',
  'bds-resort-hybrid-model': 'Mô hình lai nghỉ dưỡng',
  'bds-dc-hyperscaler-power': 'Điện cho hyperscaler',
};

export function groupForSlug(slug: string): GroupConfig {
  for (const group of BDS_GROUPS) {
    if (group.match(slug)) return group;
  }
  return BDS_GROUPS[BDS_GROUPS.length - 1];
}

// Resolve display title for a KB slug.
// Order: BDS_TITLES map → first H1 in body → frontmatter title → slug.
export function titleForSlug(
  slug: string,
  body: string,
  frontmatterTitle: string | undefined,
): string {
  if (BDS_TITLES[slug]) return BDS_TITLES[slug];
  const h1Match = body.match(/^#\s+(.+)$/m);
  if (h1Match) return h1Match[1].trim();
  if (frontmatterTitle) return frontmatterTitle;
  return slug;
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run from `web/`:

    npx vitest run src/lib/kbTree.test.ts

Expected: all tests PASS.

- [ ] **Step 5: Commit**

    git add web/src/lib/kbTree.ts web/src/lib/kbTree.test.ts
    git commit -m "feat(kb): kbTree config + title map with catch-all group"

---

## Task 3: kbParse.ts — frontmatter parser + heading extractor

**Files:**
- Create: `web/src/lib/kbParse.ts`
- Create: `web/src/lib/kbParse.test.ts`

- [ ] **Step 1: Write failing tests**

Create `web/src/lib/kbParse.test.ts`:

```ts
import { describe, expect, it } from 'vitest';
import { parseFrontmatter, extractHeadings, slugify } from './kbParse';

describe('parseFrontmatter', () => {
  it('parses flat key:value frontmatter', () => {
    const raw = `---
category: frameworks
title: "Bank-NIM-Cycle"
last_updated: 2026-05-11
---
# Body heading

Body content here.`;
    const { meta, body } = parseFrontmatter(raw);
    expect(meta.category).toBe('frameworks');
    expect(meta.title).toBe('Bank-NIM-Cycle');
    expect(meta.last_updated).toBe('2026-05-11');
    expect(body).toBe('# Body heading\n\nBody content here.');
  });

  it('parses array values via JSON.parse', () => {
    const raw = `---
applies_to: ["VHM", "NVL", "KDH"]
---
body`;
    const { meta } = parseFrontmatter(raw);
    expect(meta.applies_to).toEqual(['VHM', 'NVL', 'KDH']);
  });

  it('handles ["all"] special array', () => {
    const raw = `---
applies_to: ["all"]
---
body`;
    const { meta } = parseFrontmatter(raw);
    expect(meta.applies_to).toEqual(['all']);
  });

  it('strips quotes from string values', () => {
    const raw = `---
title: 'single quoted'
notion_page_id: "abc-123"
---
body`;
    const { meta } = parseFrontmatter(raw);
    expect(meta.title).toBe('single quoted');
    expect(meta.notion_page_id).toBe('abc-123');
  });

  it('returns empty meta + full body when no frontmatter', () => {
    const raw = 'no frontmatter\n\njust body';
    const { meta, body } = parseFrontmatter(raw);
    expect(meta).toEqual({});
    expect(body).toBe(raw);
  });
});

describe('extractHeadings', () => {
  it('extracts H2 and H3 with level + text + slug', () => {
    const body = `# Top H1 ignored

## Section A

### A.1 Sub

## Section B`;
    const headings = extractHeadings(body);
    expect(headings.length).toBe(3);
    expect(headings[0]).toMatchObject({ level: 2, text: 'Section A' });
    expect(headings[1]).toMatchObject({ level: 3, text: 'A.1 Sub' });
    expect(headings[2]).toMatchObject({ level: 2, text: 'Section B' });
    expect(headings[0].slug).toBeTruthy();
  });

  it('skips H1 and H4+', () => {
    const body = `# H1
## H2 only
#### H4 skipped`;
    const headings = extractHeadings(body);
    expect(headings.length).toBe(1);
    expect(headings[0].text).toBe('H2 only');
  });

  it('returns empty array when no H2/H3', () => {
    expect(extractHeadings('plain text only')).toEqual([]);
  });
});

describe('slugify — same output as github-slugger', () => {
  it('produces lowercase hyphen-separated slugs', () => {
    expect(slugify('Plain English')).toBe('plain-english');
    expect(slugify('Multiple  Spaces')).toBe('multiple-spaces');
    // Note: github-slugger output for Vietnamese with diacritics depends on lib version;
    // test asserts non-empty + lowercase + no spaces, not exact form.
    const viet = slugify('Lớp 1: Hiểu ngành');
    expect(viet.length).toBeGreaterThan(0);
    expect(viet).toBe(viet.toLowerCase());
    expect(viet).not.toMatch(/\s/);
  });
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run from `web/`:

    npx vitest run src/lib/kbParse.test.ts

Expected: FAIL — `Cannot find module './kbParse'`.

- [ ] **Step 3: Implement `kbParse.ts`**

Create `web/src/lib/kbParse.ts`:

```ts
import GithubSlugger from 'github-slugger';
import type { Heading, KbMeta } from './kbTypes';

// Parse YAML frontmatter from a raw markdown string. Handles flat key:value
// pairs and JSON array values like `applies_to: ["VHM", "NVL"]`.
// KB frontmatter is intentionally flat — no nesting needed, so no js-yaml dep.
export function parseFrontmatter(raw: string): { meta: KbMeta; body: string } {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!m) return { meta: {}, body: raw };

  const meta: KbMeta = {};
  for (const rawLine of m[1].split(/\r?\n/)) {
    const kv = rawLine.match(/^(\w+):\s*(.*)$/);
    if (!kv) continue;
    const [, key, val] = kv;
    if (val.startsWith('[') && val.endsWith(']')) {
      try {
        meta[key] = JSON.parse(val);
        continue;
      } catch {
        // fall through to string assign
      }
    }
    meta[key] = val.replace(/^["']|["']$/g, '');
  }
  return { meta, body: m[2] };
}

// Extract H2 and H3 headings from a markdown body. Each heading gets the
// same slug that rehype-slug will emit as id="..." on the rendered DOM,
// so search results can scroll to anchors reliably.
export function extractHeadings(body: string): Heading[] {
  const slugger = new GithubSlugger();
  const headings: Heading[] = [];
  const re = /^(#{2,3})\s+(.+)$/gm;
  let match: RegExpExecArray | null;
  while ((match = re.exec(body)) !== null) {
    const level = match[1].length as 2 | 3;
    const text = match[2].trim();
    headings.push({ level, text, slug: slugger.slug(text) });
  }
  return headings;
}

// Slugify a single heading text using github-slugger. Fresh slugger per call
// so dup-text suffix counters don't leak across calls.
export function slugify(text: string): string {
  const slugger = new GithubSlugger();
  return slugger.slug(text);
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run from `web/`:

    npx vitest run src/lib/kbParse.test.ts

Expected: all tests PASS.

- [ ] **Step 5: Commit**

    git add web/src/lib/kbParse.ts web/src/lib/kbParse.test.ts
    git commit -m "feat(kb): frontmatter parser + heading extractor with github-slugger"

---

## Task 4: kbLoader.ts — Vite glob + assemble docs

**Files:**
- Create: `web/src/lib/kbLoader.ts`

- [ ] **Step 1: Implement loader**

Create `web/src/lib/kbLoader.ts`:

```ts
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
```

- [ ] **Step 2: Verify TypeScript compiles cleanly**

Run from `web/`:

    npx tsc --noEmit

Expected: no errors.

- [ ] **Step 3: Smoke-test build picks up KB**

Run from `web/`:

    npm run build

Expected: `tsc -b` + `vite build` complete. After build:

    grep -o "bds-res-land-bank-nav\|Tham chiếu ngành" dist/assets/*.js | sort -u | head -5

Expected: both strings present (confirms 21 KB inlined into prod bundle).

- [ ] **Step 4: Commit**

    git add web/src/lib/kbLoader.ts
    git commit -m "feat(kb): kbLoader with Vite glob — inline 21 BĐS docs"

---

## Task 5: KbMarkdown component — rehype-slug + internal link routing

**Files:**
- Create: `web/src/components/kb/KbMarkdown.tsx`

- [ ] **Step 1: Create component**

Create `web/src/components/kb/KbMarkdown.tsx`:

```tsx
import { Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSlug from 'rehype-slug';

// KB-specific markdown renderer. Separate from <Markdown> (article-specific)
// to avoid coupling article styling to KB styling.
//
// - rehype-slug emits id="<slug>" on h2/h3 so search result clicks can
//   scroll to anchors (KbSearch uses location.hash).
// - h1 hidden (title rendered in KbContent header strip).
// - Internal link [text](./other.md) or [text](other.md) → React Router Link.
// - External link → new tab.
export function KbMarkdown({ children }: { children: string }) {
  return (
    <div className="prose-content max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeSlug]}
        components={{
          h1: () => null,
          h2: ({ id, children }) => (
            <h2
              id={id}
              className="!mt-6 !mb-5 px-4 py-2.5 rounded-r-xl bg-bg-2 border-l-[3px] border-fg-4 text-base font-semibold text-fg-0 scroll-mt-20"
            >
              {children}
            </h2>
          ),
          h3: ({ id, children }) => (
            <h3
              id={id}
              className="mt-5 mb-3 text-[14px] font-semibold text-fg-0 scroll-mt-20"
            >
              {children}
            </h3>
          ),
          strong: ({ children }) => (
            <strong className="font-semibold text-fg-0">{children}</strong>
          ),
          blockquote: ({ children }) => (
            <blockquote className="my-4 border-l-4 border-brand bg-brand/5 pl-4 py-2 text-fg-1">
              {children}
            </blockquote>
          ),
          table: ({ children }) => (
            <div className="my-4 overflow-x-auto">
              <table className="w-full border-collapse text-sm">{children}</table>
            </div>
          ),
          th: ({ children }) => (
            <th className="border border-fg-4/40 bg-bg-2 px-3 py-2 text-left font-semibold">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border border-fg-4/40 px-3 py-2 align-top">{children}</td>
          ),
          a: ({ href, children }) => {
            if (href && /^[a-z0-9-]+\.md$|^\.\/[a-z0-9-]+\.md$/i.test(href)) {
              const slug = href.replace(/^\.\//, '').replace(/\.md$/i, '');
              return (
                <Link to={`/tai-lieu/${slug}`} className="text-brand hover:underline">
                  {children}
                </Link>
              );
            }
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-brand hover:underline"
              >
                {children}
              </a>
            );
          },
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}
```

- [ ] **Step 2: Verify TypeScript compiles**

Run from `web/`:

    npx tsc --noEmit

Expected: no errors.

- [ ] **Step 3: Commit**

    git add web/src/components/kb/KbMarkdown.tsx
    git commit -m "feat(kb): KbMarkdown with heading anchors + link routing"

---

## Task 6: KbContent component — header strip + body

**Files:**
- Create: `web/src/components/kb/KbContent.tsx`

- [ ] **Step 1: Create component**

Create `web/src/components/kb/KbContent.tsx`:

```tsx
import type { KbDoc } from '../../lib/kbTypes';
import { titleForSlug } from '../../lib/kbTree';
import { KbMarkdown } from './KbMarkdown';

export function KbContent({ doc }: { doc: KbDoc }) {
  const title = titleForSlug(doc.slug, doc.body, doc.meta.title);
  const lastUpdated = doc.meta.last_updated;
  const appliesTo = doc.meta.applies_to;

  return (
    <article className="mx-auto w-full max-w-[760px] px-6 py-8">
      <header className="mb-8 border-b border-fg-4/40 pb-5">
        <h1 className="font-sans text-3xl font-semibold tracking-tight text-fg-0">
          {title}
        </h1>
        <MetaStrip lastUpdated={lastUpdated} appliesTo={appliesTo} />
      </header>
      <KbMarkdown>{doc.body}</KbMarkdown>
    </article>
  );
}

function MetaStrip({
  lastUpdated,
  appliesTo,
}: {
  lastUpdated: string | undefined;
  appliesTo: string[] | undefined;
}) {
  const hasUpdate = Boolean(lastUpdated);
  const hasApplies = Array.isArray(appliesTo) && appliesTo.length > 0;
  if (!hasUpdate && !hasApplies) return null;

  return (
    <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1.5 font-sans text-[12px] text-fg-2">
      {hasUpdate && (
        <span>
          cập nhật <span className="font-medium text-fg-1">{lastUpdated}</span>
        </span>
      )}
      {hasUpdate && hasApplies && (
        <span aria-hidden className="text-fg-4">·</span>
      )}
      {hasApplies && <AppliesToChips items={appliesTo!} />}
    </div>
  );
}

function AppliesToChips({ items }: { items: string[] }) {
  if (items.length === 1 && items[0] === 'all') {
    return <span>áp dụng: tất cả mã ngành</span>;
  }
  return (
    <span className="flex flex-wrap items-center gap-1.5">
      <span>áp dụng:</span>
      {items.map((t) => (
        <span
          key={t}
          className="inline-flex h-5 items-center rounded-full border border-emerald-400/40 bg-emerald-400/10 px-2 font-mono text-[10.5px] font-medium tabular-nums text-emerald-300"
        >
          {t}
        </span>
      ))}
    </span>
  );
}

export function KbContentNotFound({ slug }: { slug: string }) {
  return (
    <div className="mx-auto w-full max-w-[760px] px-6 py-12">
      <p className="text-fg-2">
        KB <code className="rounded bg-bg-2 px-1.5 py-0.5">{slug}</code> không
        tồn tại trong sector này. Chọn 1 KB từ sidebar bên trái.
      </p>
    </div>
  );
}
```

- [ ] **Step 2: Verify compile**

Run from `web/`:

    npx tsc --noEmit

Expected: no errors.

- [ ] **Step 3: Commit**

    git add web/src/components/kb/KbContent.tsx
    git commit -m "feat(kb): KbContent — header strip with title + meta + applies_to chips"

---

## Task 7: KbTree component — sidebar tree with collapse

**Files:**
- Create: `web/src/components/kb/KbTree.tsx`

- [ ] **Step 1: Create component**

Create `web/src/components/kb/KbTree.tsx`:

```tsx
import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ChevronDown } from 'lucide-react';
import type { KbDoc } from '../../lib/kbTypes';
import { BDS_GROUPS, groupForSlug, titleForSlug } from '../../lib/kbTree';
import { cn } from '../../shared/lib/cn';

interface Props {
  docs: KbDoc[];
  sector: 'bds' | 'bank' | 'ck';
}

interface GroupedDocs {
  groupId: string;
  icon: string;
  label: string;
  docs: KbDoc[];
}

export function KbTree({ docs, sector }: Props) {
  const { slug: activeSlug } = useParams<{ slug?: string }>();

  const grouped = useMemo<GroupedDocs[]>(() => {
    const result: GroupedDocs[] = BDS_GROUPS.map((g) => ({
      groupId: g.id,
      icon: g.icon,
      label: g.label,
      docs: [] as KbDoc[],
    }));
    for (const doc of docs) {
      const group = groupForSlug(doc.slug);
      const bucket = result.find((g) => g.groupId === group.id);
      if (bucket) bucket.docs.push(doc);
    }
    return result.filter((g) => g.docs.length > 0);
  }, [docs]);

  const storageKey = `kb.expanded.${sector}`;
  const [expanded, setExpanded] = useState<Set<string>>(() => {
    try {
      const raw = localStorage.getItem(storageKey);
      if (raw) return new Set(JSON.parse(raw) as string[]);
    } catch { /* ignore */ }
    return new Set(grouped.map((g) => g.groupId));
  });

  useEffect(() => {
    try {
      localStorage.setItem(storageKey, JSON.stringify([...expanded]));
    } catch { /* ignore */ }
  }, [expanded, storageKey]);

  useEffect(() => {
    if (!activeSlug) return;
    const owner = groupForSlug(activeSlug);
    setExpanded((prev) => (prev.has(owner.id) ? prev : new Set([...prev, owner.id])));
  }, [activeSlug]);

  const toggle = (id: string) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  return (
    <nav aria-label="Phụ lục KB" className="flex flex-col gap-1">
      <p className="px-3 pb-1 pt-2 font-sans text-[10.5px] uppercase tracking-[0.14em] text-fg-3">
        Phụ lục
      </p>
      {grouped.map((group) => {
        const isOpen = expanded.has(group.groupId);
        const isMasterOnly = group.groupId === 'master' && group.docs.length === 1;
        return (
          <div key={group.groupId}>
            {!isMasterOnly && (
              <button
                type="button"
                onClick={() => toggle(group.groupId)}
                className={cn(
                  'group flex w-full items-center gap-2 rounded-md px-3 py-1.5 text-left transition-colors duration-fast',
                  'hover:bg-bg-2',
                )}
                aria-expanded={isOpen}
              >
                <span aria-hidden className="w-5 text-base leading-none">{group.icon}</span>
                <span className="flex-1 font-sans text-[13px] font-semibold text-fg-1">
                  {group.label}
                </span>
                <span className="font-mono text-[10px] tabular-nums text-fg-3">
                  {group.docs.length}
                </span>
                <ChevronDown
                  className={cn(
                    'h-3.5 w-3.5 text-fg-3 transition-transform duration-fast',
                    !isOpen && '-rotate-90',
                  )}
                  strokeWidth={2.2}
                  aria-hidden
                />
              </button>
            )}
            {(isMasterOnly || isOpen) && (
              <ul className={cn('flex flex-col gap-0.5', !isMasterOnly && 'pl-3')}>
                {group.docs.map((doc) => {
                  const title = titleForSlug(doc.slug, doc.body, doc.meta.title);
                  const isActive = doc.slug === activeSlug;
                  return (
                    <li key={doc.slug}>
                      <Link
                        to={`/tai-lieu/${doc.slug}`}
                        className={cn(
                          'flex items-center gap-2 rounded-md px-3 py-1.5 font-sans text-[12.5px] transition-colors duration-fast',
                          isMasterOnly && 'gap-2.5',
                          isActive
                            ? 'bg-brand/10 text-fg-0 border-l-2 border-brand pl-[10px]'
                            : 'text-fg-2 hover:bg-bg-2 hover:text-fg-0',
                        )}
                      >
                        {isMasterOnly && (
                          <span aria-hidden className="text-base leading-none">{group.icon}</span>
                        )}
                        <span className="truncate">{title}</span>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
        );
      })}
    </nav>
  );
}
```

- [ ] **Step 2: Verify compile**

Run from `web/`:

    npx tsc --noEmit

Expected: no errors.

- [ ] **Step 3: Commit**

    git add web/src/components/kb/KbTree.tsx
    git commit -m "feat(kb): KbTree sidebar — grouped, collapsible, active highlight"

---

## Task 8: KbSearch component — Fuse.js with snippet highlight

**Files:**
- Create: `web/src/components/kb/KbSearch.tsx`

- [ ] **Step 1: Create component**

Create `web/src/components/kb/KbSearch.tsx`:

```tsx
import { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Fuse, { type FuseResult, type FuseResultMatch } from 'fuse.js';
import { Search, X } from 'lucide-react';
import type { KbDoc } from '../../lib/kbTypes';
import { titleForSlug } from '../../lib/kbTree';
import { cn } from '../../shared/lib/cn';

interface Props { docs: KbDoc[]; }

interface IndexedDoc extends KbDoc {
  title: string;
  headingText: string;
}

const SNIPPET_RADIUS = 60;
const MAX_RESULTS = 5;

export function KbSearch({ docs }: Props) {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const indexed = useMemo<IndexedDoc[]>(
    () =>
      docs.map((d) => ({
        ...d,
        title: titleForSlug(d.slug, d.body, d.meta.title),
        headingText: d.headings.map((h) => h.text).join(' \n '),
      })),
    [docs],
  );

  const fuse = useMemo(
    () =>
      new Fuse(indexed, {
        keys: [
          { name: 'title', weight: 3 },
          { name: 'headingText', weight: 2 },
          { name: 'body', weight: 1 },
        ],
        includeMatches: true,
        ignoreLocation: true,
        threshold: 0.4,
        minMatchCharLength: 2,
      }),
    [indexed],
  );

  const results = useMemo(() => {
    const q = query.trim();
    if (q.length < 2) return [];
    return fuse.search(q, { limit: MAX_RESULTS });
  }, [fuse, query]);

  const onPick = (slug: string, anchor?: string) => {
    const url = anchor ? `/tai-lieu/${slug}#${anchor}` : `/tai-lieu/${slug}`;
    navigate(url);
    setQuery('');
  };

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape' && document.activeElement === inputRef.current) {
        setQuery('');
        inputRef.current?.blur();
      }
    }
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);

  const isOpen = query.trim().length >= 2;

  return (
    <div className="relative px-3 pb-2">
      <div className="relative">
        <Search
          className="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-fg-3"
          strokeWidth={2}
          aria-hidden
        />
        <input
          ref={inputRef}
          type="search"
          placeholder="tìm KB..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="h-9 w-full rounded-md border border-fg-4/40 bg-bg-1 pl-9 pr-8 font-sans text-[13px] text-fg-0 placeholder:text-fg-3 focus:border-brand/60 focus:outline-none focus:ring-2 focus:ring-brand/30"
        />
        {query && (
          <button
            type="button"
            onClick={() => setQuery('')}
            className="absolute right-2 top-1/2 flex h-5 w-5 -translate-y-1/2 items-center justify-center rounded text-fg-3 hover:bg-bg-2 hover:text-fg-0"
            aria-label="Xoá tìm kiếm"
          >
            <X className="h-3 w-3" strokeWidth={2.2} aria-hidden />
          </button>
        )}
      </div>
      {isOpen && (
        <div className="mt-1.5 overflow-hidden rounded-md border border-fg-4/40 bg-bg-1 shadow-lg">
          {results.length === 0 ? (
            <p className="px-3 py-3 font-sans text-[12px] text-fg-3">
              Không có KB nào khớp "<span className="text-fg-1">{query}</span>".
            </p>
          ) : (
            <ul role="listbox" className="flex flex-col">
              {results.map((r) => (
                <ResultRow key={r.item.slug} result={r} onPick={onPick} />
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

function ResultRow({
  result,
  onPick,
}: {
  result: FuseResult<IndexedDoc>;
  onPick: (slug: string, anchor?: string) => void;
}) {
  const { item, matches } = result;
  const { snippet, headingSlug } = useMemo(
    () => buildSnippet(item, matches ?? []),
    [item, matches],
  );

  return (
    <li>
      <button
        type="button"
        onClick={() => onPick(item.slug, headingSlug)}
        className="flex w-full flex-col gap-1 px-3 py-2.5 text-left transition-colors duration-fast hover:bg-bg-2"
      >
        <span className="font-sans text-[12.5px] font-semibold text-fg-0">
          {item.title}
        </span>
        <span
          className="font-sans text-[11.5px] leading-snug text-fg-2"
          dangerouslySetInnerHTML={{ __html: snippet }}
        />
      </button>
    </li>
  );
}

function buildSnippet(
  doc: IndexedDoc,
  matches: readonly FuseResultMatch[],
): { snippet: string; headingSlug?: string } {
  const headingMatch = matches.find((m) => m.key === 'headingText');
  const bodyMatch = matches.find((m) => m.key === 'body');
  const titleMatch = matches.find((m) => m.key === 'title');

  if (bodyMatch?.indices?.length) {
    const [start, end] = bodyMatch.indices[0];
    return { snippet: sliceSnippet(doc.body, start, end) };
  }

  if (headingMatch?.indices?.length) {
    const [start, end] = headingMatch.indices[0];
    const text = doc.headingText;
    const snippet = sliceSnippet(text, start, end);
    let cumulative = 0;
    for (const h of doc.headings) {
      const next = cumulative + h.text.length + 3;
      if (start >= cumulative && start < next) {
        return { snippet, headingSlug: h.slug };
      }
      cumulative = next;
    }
    return { snippet };
  }

  if (titleMatch) {
    return { snippet: escapeHtml(doc.title) };
  }

  return { snippet: escapeHtml(doc.body.slice(0, 120)) + '...' };
}

function sliceSnippet(text: string, start: number, end: number): string {
  const left = Math.max(0, start - SNIPPET_RADIUS);
  const right = Math.min(text.length, end + 1 + SNIPPET_RADIUS);
  const prefix = left > 0 ? '...' : '';
  const suffix = right < text.length ? '...' : '';
  const before = escapeHtml(text.slice(left, start));
  const match = escapeHtml(text.slice(start, end + 1));
  const after = escapeHtml(text.slice(end + 1, right));
  return `${prefix}${before}<mark class="bg-brand/30 text-fg-0 rounded px-0.5">${match}</mark>${after}${suffix}`;
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
```

- [ ] **Step 2: Verify compile**

Run from `web/`:

    npx tsc --noEmit

Expected: no errors.

- [ ] **Step 3: Commit**

    git add web/src/components/kb/KbSearch.tsx
    git commit -m "feat(kb): KbSearch with Fuse.js + snippet highlight + anchor scroll"

---

## Task 9: KbTabs component — sector switcher with disabled placeholders

**Files:**
- Create: `web/src/components/kb/KbTabs.tsx`

- [ ] **Step 1: Create component**

Create `web/src/components/kb/KbTabs.tsx`:

```tsx
import { useSearchParams } from 'react-router-dom';
import { cn } from '../../shared/lib/cn';

type Sector = 'bds' | 'bank' | 'ck';

const TABS: { id: Sector; label: string; enabled: boolean }[] = [
  { id: 'bds', label: 'Bất động sản', enabled: true },
  { id: 'bank', label: 'Ngân hàng', enabled: false },
  { id: 'ck', label: 'Chứng khoán', enabled: false },
];

export function KbTabs({ active }: { active: Sector }) {
  const [params, setParams] = useSearchParams();

  const onSelect = (sector: Sector) => {
    const next = new URLSearchParams(params);
    if (sector === 'bds') next.delete('sector');
    else next.set('sector', sector);
    setParams(next, { replace: true });
  };

  return (
    <div
      role="tablist"
      aria-label="Sector"
      className="flex items-center gap-1 border-b border-fg-4/40 px-2"
    >
      {TABS.map((t) => {
        const isActive = t.id === active;
        return (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={isActive}
            disabled={!t.enabled}
            title={t.enabled ? undefined : 'Sắp có — đang refactor pipeline'}
            onClick={() => t.enabled && onSelect(t.id)}
            className={cn(
              'relative h-9 px-3 font-sans text-[12.5px] font-medium transition-colors duration-fast',
              t.enabled
                ? isActive
                  ? 'text-fg-0'
                  : 'text-fg-2 hover:text-fg-0'
                : 'cursor-not-allowed text-fg-3 opacity-60',
            )}
          >
            {t.label}
            {!t.enabled && (
              <span className="ml-1 align-middle font-mono text-[9px] uppercase tracking-wider text-fg-3">
                sắp có
              </span>
            )}
            {isActive && (
              <span
                aria-hidden
                className="absolute inset-x-2 -bottom-px h-[2px] rounded-full bg-brand"
              />
            )}
          </button>
        );
      })}
    </div>
  );
}
```

- [ ] **Step 2: Verify compile**

Run from `web/`:

    npx tsc --noEmit

Expected: no errors.

- [ ] **Step 3: Commit**

    git add web/src/components/kb/KbTabs.tsx
    git commit -m "feat(kb): KbTabs — 3 sector tabs, Bank+CK disabled 'sắp có'"

---

## Task 10: KbSidebar — compose tabs + search + tree, mobile drawer

**Files:**
- Create: `web/src/components/kb/KbSidebar.tsx`

- [ ] **Step 1: Create component**

Create `web/src/components/kb/KbSidebar.tsx`:

```tsx
import { useEffect } from 'react';
import { X } from 'lucide-react';
import type { KbDoc } from '../../lib/kbTypes';
import { cn } from '../../shared/lib/cn';
import { KbSearch } from './KbSearch';
import { KbTabs } from './KbTabs';
import { KbTree } from './KbTree';

type Sector = 'bds' | 'bank' | 'ck';

interface Props {
  sector: Sector;
  docs: KbDoc[];
  isDrawerOpen: boolean;
  onClose: () => void;
}

export function KbSidebar({ sector, docs, isDrawerOpen, onClose }: Props) {
  useEffect(() => {
    if (!isDrawerOpen) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose();
    }
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [isDrawerOpen, onClose]);

  const body = (
    <div className="flex h-full flex-col">
      <KbTabs active={sector} />
      <div className="flex-1 overflow-y-auto pb-4">
        <KbSearch docs={docs} />
        {docs.length === 0 ? (
          <p className="px-3 pt-4 font-sans text-[12px] text-fg-3">
            Sector này chưa có KB. Sắp có.
          </p>
        ) : (
          <KbTree docs={docs} sector={sector} />
        )}
      </div>
    </div>
  );

  return (
    <>
      <aside className="hidden w-[280px] shrink-0 border-r border-fg-4/40 bg-bg-1 lg:block">
        {body}
      </aside>

      <div
        className={cn(
          'fixed inset-0 z-40 lg:hidden',
          isDrawerOpen ? 'pointer-events-auto' : 'pointer-events-none',
        )}
        aria-hidden={!isDrawerOpen}
      >
        <button
          type="button"
          aria-label="Đóng phụ lục"
          onClick={onClose}
          className={cn(
            'absolute inset-0 bg-bg-0/60 backdrop-blur-sm transition-opacity duration-fast',
            isDrawerOpen ? 'opacity-100' : 'opacity-0',
          )}
        />
        <aside
          className={cn(
            'absolute left-0 top-0 h-full w-[280px] border-r border-fg-4/40 bg-bg-1 shadow-xl transition-transform duration-med ease-out-quart',
            isDrawerOpen ? 'translate-x-0' : '-translate-x-full',
          )}
        >
          <div className="flex items-center justify-end px-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded-md p-1.5 text-fg-2 hover:bg-bg-2 hover:text-fg-0"
              aria-label="Đóng"
            >
              <X className="h-4 w-4" strokeWidth={2.2} aria-hidden />
            </button>
          </div>
          {body}
        </aside>
      </div>
    </>
  );
}
```

- [ ] **Step 2: Verify compile**

Run from `web/`:

    npx tsc --noEmit

Expected: no errors.

- [ ] **Step 3: Commit**

    git add web/src/components/kb/KbSidebar.tsx
    git commit -m "feat(kb): KbSidebar — desktop fixed + mobile drawer"

---

## Task 11: KbPage + App route + hash anchor scroll

**Files:**
- Create: `web/src/pages/KbPage.tsx`
- Modify: `web/src/App.tsx`

- [ ] **Step 1: Create `KbPage.tsx`**

Create `web/src/pages/KbPage.tsx`:

```tsx
import { useEffect, useMemo, useState } from 'react';
import { Navigate, useLocation, useParams, useSearchParams } from 'react-router-dom';
import { Menu } from 'lucide-react';
import { docsForSector } from '../lib/kbLoader';
import { KbContent, KbContentNotFound } from '../components/kb/KbContent';
import { KbSidebar } from '../components/kb/KbSidebar';

type Sector = 'bds' | 'bank' | 'ck';

function isSector(v: string | null): v is Sector {
  return v === 'bds' || v === 'bank' || v === 'ck';
}

export function KbPage() {
  const { slug } = useParams<{ slug?: string }>();
  const [params] = useSearchParams();
  const location = useLocation();

  const sectorParam = params.get('sector');
  const sector: Sector = isSector(sectorParam) ? sectorParam : 'bds';

  const docs = useMemo(() => docsForSector(sector), [sector]);

  const [drawerOpen, setDrawerOpen] = useState(false);

  useEffect(() => {
    setDrawerOpen(false);
  }, [location.pathname, location.search]);

  useEffect(() => {
    if (!location.hash) {
      window.scrollTo({ top: 0 });
      return;
    }
    const id = location.hash.slice(1);
    const t = setTimeout(() => {
      const el = document.getElementById(id);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 50);
    return () => clearTimeout(t);
  }, [location.hash, location.pathname]);

  if (!slug) {
    if (docs.length === 0) {
      return (
        <PageShell
          sector={sector}
          docs={docs}
          drawerOpen={drawerOpen}
          setDrawerOpen={setDrawerOpen}
        >
          <div className="mx-auto max-w-[760px] px-6 py-12 text-fg-2">
            Sector này chưa có KB.
          </div>
        </PageShell>
      );
    }
    const firstSlug =
      docs.find((d) => d.slug === 'bds-industry-master-reference')?.slug ??
      docs[0].slug;
    const qs = sector === 'bds' ? '' : `?sector=${sector}`;
    return <Navigate to={`/tai-lieu/${firstSlug}${qs}`} replace />;
  }

  const doc = docs.find((d) => d.slug === slug);

  return (
    <PageShell
      sector={sector}
      docs={docs}
      drawerOpen={drawerOpen}
      setDrawerOpen={setDrawerOpen}
    >
      {doc ? <KbContent doc={doc} /> : <KbContentNotFound slug={slug} />}
    </PageShell>
  );
}

function PageShell({
  sector,
  docs,
  drawerOpen,
  setDrawerOpen,
  children,
}: {
  sector: Sector;
  docs: ReturnType<typeof docsForSector>;
  drawerOpen: boolean;
  setDrawerOpen: (v: boolean) => void;
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-[calc(100vh-56px)]">
      <KbSidebar
        sector={sector}
        docs={docs}
        isDrawerOpen={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      />
      <main className="min-w-0 flex-1">
        <div className="flex items-center justify-between border-b border-fg-4/40 px-3 py-2 lg:hidden">
          <button
            type="button"
            onClick={() => setDrawerOpen(true)}
            className="flex items-center gap-2 rounded-md px-2 py-1.5 font-sans text-[12.5px] text-fg-2 hover:bg-bg-2 hover:text-fg-0"
            aria-label="Mở phụ lục"
          >
            <Menu className="h-4 w-4" strokeWidth={2.2} aria-hidden />
            Phụ lục
          </button>
        </div>
        {children}
      </main>
    </div>
  );
}
```

- [ ] **Step 2: Wire route in `App.tsx`**

Open `web/src/App.tsx`. Replace existing content with:

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { IndexPage } from './pages/IndexPage';
import { ArticlePage } from './pages/ArticlePage';
import { FeedPage } from './pages/FeedPage';
import { KbPage } from './pages/KbPage';
import { Header } from './components/Header';

const BASENAME = import.meta.env.BASE_URL.replace(/\/$/, '') || '/';

export default function App() {
  return (
    <BrowserRouter basename={BASENAME}>
      <Header />
      <Routes>
        <Route path="/" element={<IndexPage />} />
        <Route path="/feed" element={<FeedPage />} />
        <Route path="/article/:id" element={<ArticlePage />} />
        <Route path="/tai-lieu" element={<KbPage />} />
        <Route path="/tai-lieu/:slug" element={<KbPage />} />
      </Routes>
    </BrowserRouter>
  );
}
```

- [ ] **Step 3: Verify compile**

Run from `web/`:

    npx tsc --noEmit

Expected: no errors.

- [ ] **Step 4: Commit**

    git add web/src/pages/KbPage.tsx web/src/App.tsx
    git commit -m "feat(kb): KbPage route /tai-lieu/:slug with sector + hash scroll"

---

## Task 12: Header.tsx — add "Tài liệu" nav link

**Files:**
- Modify: `web/src/components/Header.tsx`

- [ ] **Step 1: Update header nav**

Open `web/src/components/Header.tsx`. Locate the existing predicates + nav block. Make these 2 edits:

(a) Add `isKb` predicate near existing `isCards` / `isFeed`:

```tsx
const isCards = pathname === '/' || pathname.startsWith('/article/');
const isFeed = pathname === '/feed';
const isKb = pathname === '/tai-lieu' || pathname.startsWith('/tai-lieu/');
```

(b) Add 3rd NavLink + separator after "Dòng tin" inside the `<nav>`:

```tsx
<nav
  aria-label="Điều hướng chính"
  className="flex shrink-0 items-center gap-3 sm:gap-5"
>
  <NavLink to="/" active={isCards}>
    Bài viết
  </NavLink>
  <span aria-hidden className="h-3 w-px bg-fg-4/60" />
  <NavLink to="/feed" active={isFeed}>
    Dòng tin
  </NavLink>
  <span aria-hidden className="h-3 w-px bg-fg-4/60" />
  <NavLink to="/tai-lieu" active={isKb}>
    Tài liệu
  </NavLink>
</nav>
```

- [ ] **Step 2: Verify compile**

Run from `web/`:

    npx tsc --noEmit

Expected: no errors.

- [ ] **Step 3: Commit**

    git add web/src/components/Header.tsx
    git commit -m "feat(kb): Header nav add 'Tài liệu' link to /tai-lieu"

---

## Task 13: End-to-end manual verification — dev server

**Files:** No file changes (verification only)

- [ ] **Step 1: Start dev server**

Run from `web/`:

    npm run dev

Expected: server starts on port 5174 (or similar). Console shows "Local: http://localhost:5174/". Keep running for steps 2-9.

- [ ] **Step 2: Initial route works**

Open browser to `http://localhost:5174/tai-lieu`.

Expected:
- Header shows "Bài viết · Dòng tin · Tài liệu" with "Tài liệu" highlighted
- URL redirects to `/tai-lieu/bds-industry-master-reference`
- Sidebar shows 8 groups: 🏛 Tham chiếu ngành (1 flat) · 📊 Khái niệm chung (5) · 🏘 Phát triển dân cư (3) · 🏭 Khu công nghiệp (3) · 🛍 Bán lẻ trung tâm (3) · 🏢 Văn phòng cho thuê (2) · 🏖 Nghỉ dưỡng (3) · 🖥 Trung tâm dữ liệu (1)
- Content panel shows "Tham chiếu ngành" h1 + "cập nhật 2026-05-11 · áp dụng: tất cả mã ngành" meta strip + markdown body

- [ ] **Step 3: Click navigation through tree**

Click "Quỹ đất & NAV" under Phát triển dân cư.

Expected: URL changes to `/tai-lieu/bds-res-land-bank-nav`. Content swaps. Active state: brand-tinted background + left border. Browser back returns to Master.

- [ ] **Step 4: Group collapse/expand**

Click "🏭 Khu công nghiệp" group header chevron.

Expected: items collapse with chevron rotation. Click again → expand. Refresh page → state persists (localStorage).

- [ ] **Step 5: Search works**

Type "NAV" into search box.

Expected: 1-5 results appear. Each shows title + snippet with `<mark>` highlight. Click first → navigates + scrolls if heading match.

Try "không có gì" → empty state message. Press ESC → query clears.

- [ ] **Step 6: Heading anchor scroll**

In a doc with H2 headings, inspect DOM for `<h2 id=...>`. Copy URL with `#<id>`. Open in fresh tab.

Expected: page scrolls to that h2. `scroll-mt-20` offset keeps heading visible below sticky header.

- [ ] **Step 7: Disabled tabs**

Hover "Ngân hàng" tab.

Expected: cursor not-allowed, tooltip "Sắp có — đang refactor pipeline". Click does nothing.

- [ ] **Step 8: Mobile drawer**

Resize browser to <1024px (or use device toolbar at 375px).

Expected:
- Sidebar hidden
- "≡ Phụ lục" button appears at top of content
- Click → drawer slides from left with backdrop
- Click backdrop or X or ESC → drawer closes
- Click tree item → drawer closes + content updates

- [ ] **Step 9: Theme switching**

Toggle theme via ThemeSwitcher in header.

Expected: sidebar bg, content prose, search results, tree active state all swap to new palette correctly.

- [ ] **Step 10: Cleanup if issues found**

If any of steps 2-9 failed, fix in place and re-verify. Otherwise stop dev server.

- [ ] **Step 11: Commit any fixes**

If fixes were needed:

    git add -A
    git commit -m "fix(kb): <specific issue> from manual verification"

If no fixes needed, skip.

---

## Task 14: Production build verification

**Files:** No file changes (verification only)

- [ ] **Step 1: Run production build**

Run from `web/`:

    npm run build

Expected: `tsc -b` passes. Vite build completes. Output bundle includes ~45-50KB gzipped from KB inline.

- [ ] **Step 2: Verify KB content in bundle**

Run from `web/`:

    grep -o "bds-res-land-bank-nav\|Tham chiếu ngành\|Lớp 1" dist/assets/*.js | sort -u | head -5

Expected: 3 distinct strings present.

- [ ] **Step 3: Preview production build**

Run from `web/`:

    npm run preview

Open URL printed. Navigate to `/tai-lieu`.

Expected: page renders identical to dev, with `/finpath-newsroom/` basename applied. All routes work. No 404 on KB content.

Stop preview server.

- [ ] **Step 4: Commit if production-only fixes needed**

If issues:

    git add -A
    git commit -m "fix(kb): <specific issue> from production build"

Otherwise skip.

---

## Task 15: Auto-update smoke test (temporary KB file)

**Files:**
- Create + remove: `kb/bds/frameworks/bds-_smoke-test-temp.md`

- [ ] **Step 1: Drop a temporary KB file**

Create `kb/bds/frameworks/bds-_smoke-test-temp.md`:

```md
---
category: frameworks
title: "BDS-Smoke-Test-Temp"
last_updated: 2026-05-11
applies_to: ["all"]
---

# Smoke test temporary KB

This file verifies that the auto-update flow works end-to-end. It will be
removed after verification.

## Section A

Body text for section A.

## Section B

Body text for section B.
```

- [ ] **Step 2: Restart dev server + verify appears**

Run from `web/`:

    npm run dev

Open `http://localhost:5174/tai-lieu`. Look in sidebar.

Expected:
- New "Khác" group appears with 1 item (slug doesn't match any named prefix)
- Click → content panel renders the temp KB
- Search "smoke" → result appears

- [ ] **Step 3: Stop dev server + remove temp file**

Stop dev server. Then:

    rm "kb/bds/frameworks/bds-_smoke-test-temp.md"

- [ ] **Step 4: No commit**

This task creates and removes a temp file. If accidentally staged:

    git restore --staged kb/bds/frameworks/bds-_smoke-test-temp.md 2>/dev/null
    git checkout HEAD -- kb/bds/frameworks/ 2>/dev/null

---

## Task 16: Final push to GH Pages

**Files:** No file changes (housekeeping)

- [ ] **Step 1: Verify clean working tree**

Run from repo root:

    git status

Expected: working tree clean.

- [ ] **Step 2: Push to remote**

    git push origin main

Expected: GH Actions trigger. After ~2-3 minutes, GH Pages deploys.

- [ ] **Step 3: Verify GH Pages**

Open the configured Pages URL + `/tai-lieu`.

Expected: page loads. Sidebar + Master KB visible. Same behavior as local.

- [ ] **Step 4: Notify team**

Per user requirement ("báo team vào check"). Done via user's own channel — not a Claude task.

---

## Verification checklist (mirrors spec §13)

After all tasks complete, all of these must pass:

- [ ] `/tai-lieu` mở được trên localhost dev, sidebar + Master KB hiện
- [ ] Click từng group → expand/collapse smooth, state persist localStorage
- [ ] Click 1 KB → URL đổi, content render, active state highlight
- [ ] Browser back/forward navigate qua các KB work
- [ ] Search "NAV" → top 5 result, click → navigate + scroll match
- [ ] Search empty / <2 chars → results ẩn, tree hiện
- [ ] Mobile <1024px: drawer toggle work, ESC + click-outside close
- [ ] Theme switch → sidebar + content theme-aware
- [ ] `npm run build` → bundle có KB content (grep verify)
- [ ] GH Pages URL `/finpath-newsroom/tai-lieu` work
- [ ] Smoke test KB mới → group "Khác" hiện file, sau xóa
- [ ] Tab Bank + CK disabled, tooltip "Sắp có" hiện

---

## Out of scope (defer — also documented in spec §14)

- KB Bank + CK content
- Wiki-link auto-detect plain text mentions
- `applies_to` chips → cross-link to article filter (`/?t=VHM`)
- Graph view / backlinks panel
- Reading progress / bookmarks
- Per-KB changelog timeline UI
- Print stylesheet / PDF export
- Reading time estimation
- Copy-to-clipboard heading deep-link
