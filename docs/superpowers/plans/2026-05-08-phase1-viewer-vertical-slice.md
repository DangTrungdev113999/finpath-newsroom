# Phase 1 — Viewer Vertical Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build React+Vite viewer rendering 1 sample VCB article with 2-column layout matching Notion Compare Feed screenshot 1:1, sourcing markdown from `output/compare-feed/` via symlink.

**Architecture:** React 18 + TypeScript + Vite + Tailwind 3 + react-markdown. Markdown files in `output/compare-feed/` exposed to web via symlink to `web/public/articles/`. App fetches `manifest.json` for IndexPage list, then individual `.md` files for ArticlePage. `gray-matter` parses frontmatter; regex split on `<!-- left -->`/`<!-- right -->` markers separates 2 columns. Pure-function parser is unit tested; visual fidelity verified by running dev server and comparing to the screenshot user provided in spec.

**Tech Stack:** Vite 5, React 18, TypeScript 5 (strict), Tailwind CSS 3, react-router-dom 6, react-markdown 9, remark-gfm 4, gray-matter 4, vitest 1 (unit tests).

**Spec reference:** `docs/superpowers/specs/2026-05-08-newsroom-cli-migration-design.md` Section 5 (output format), Section 6 (web viewer), Phase 1 build order.

**Project instructions:** `CLAUDE.md` (project root) — đọc trước khi action: 5 quality gates, universe MVP, data sourcing rule, hard rules Master/Skeptic.

**Project root:** `/Users/trungdt/Desktop/Stream Intelligent/`

---

## File Structure

### Created
```
.gitignore
docs/superpowers/plans/2026-05-08-phase1-viewer-vertical-slice.md   # this file
output/compare-feed/
├── VCB-20260508-1530.md            # sample bootstrap (Notion → hand-craft)
└── manifest.json                    # IndexPage list
web/                                  # symlinked output via web/public/articles
├── package.json
├── vite.config.ts
├── tailwind.config.ts
├── postcss.config.js
├── tsconfig.json
├── tsconfig.node.json
├── index.html
├── public/
│   └── articles                     # symlink → ../../output/compare-feed/
└── src/
    ├── main.tsx                     # React entry
    ├── App.tsx                      # router root
    ├── index.css                    # Tailwind directives + base
    ├── types.ts                     # Article + meta types
    ├── lib/
    │   ├── parseArticle.ts          # gray-matter + section split
    │   ├── parseArticle.test.ts     # vitest tests
    │   ├── articleLoader.ts         # manifest + .md fetch
    │   └── format.ts                # date/number formatters
    ├── components/
    │   ├── CompareFeedLayout.tsx    # 2-col grid wrapper
    │   ├── LeftColumn.tsx           # ✍️ Bài AI viết lại
    │   ├── RightColumn.tsx          # 📰 Raw + meta + funnel
    │   ├── InsightCallout.tsx       # 💡 callout vàng
    │   ├── CrawlFunnel.tsx          # collapsible 4-group funnel
    │   ├── PipelineLog.tsx          # collapsible 6-step log
    │   ├── ArticleCard.tsx          # IndexPage card item
    │   └── Markdown.tsx             # react-markdown wrapper
    └── pages/
        ├── IndexPage.tsx            # list articles
        └── ArticlePage.tsx          # 2-col view per article
```

### Not modified (none — fresh project)

---

## Tasks

### Task 1: Project init + git + .gitignore

**Files:**
- Create: `.gitignore`
- Run: `git init` in project root

- [ ] **Step 1: Verify project root + state**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && ls -la && git rev-parse --is-inside-work-tree 2>&1
```

Expected: only `.DS_Store` + `docs/` exist; "fatal: not a git repository" message.

- [ ] **Step 2: Initialize git repo**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git init && git branch -m main
```

Expected: "Initialized empty Git repository... Switched to branch 'main'".

- [ ] **Step 3: Create `.gitignore`**

Write `/Users/trungdt/Desktop/Stream Intelligent/.gitignore`:

```
# OS
.DS_Store

# Node
node_modules/
*.log
npm-debug.log*

# Vite build
dist/
web/dist/

# Python (Phase 2+)
__pycache__/
*.pyc
.venv/
.pytest_cache/

# Local data (track schema only)
data/pipeline.db
data/pipeline.db-journal

# Env
.env
.env.local

# Editor
.vscode/
.idea/
```

- [ ] **Step 4: First commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .gitignore docs/ CLAUDE.md && git commit -m "chore: init repo + spec + Phase 1 plan + CLAUDE.md instructions"
```

Expected: commit success including `.gitignore`, `docs/superpowers/{specs,plans}/*.md`, and `CLAUDE.md`.

---

### Task 2: Scaffold web/ with Vite + React + TS

**Files:**
- Create: `web/package.json`, `web/vite.config.ts`, `web/tsconfig.json`, `web/tsconfig.node.json`, `web/index.html`, `web/src/main.tsx`, `web/src/App.tsx`, `web/src/index.css`

- [ ] **Step 1: Run Vite scaffold (non-interactive)**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && npm create vite@latest web -- --template react-ts
```

Expected: creates `web/` with React + TS template. If prompted to overwrite, abort and ask user (shouldn't happen in fresh repo).

- [ ] **Step 2: Install base deps**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm install
```

Expected: `node_modules/` populated, no errors.

- [ ] **Step 3: Verify dev server boots**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && timeout 8 npm run dev || true
```

Expected: Vite output shows "Local: http://localhost:5173/" within 5 seconds.

- [ ] **Step 4: Install runtime deps**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm install react-router-dom@6 react-markdown@9 remark-gfm@4 gray-matter@4
```

Expected: 4 packages added without peer warnings.

- [ ] **Step 5: Install dev deps (Tailwind + vitest)**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm install -D tailwindcss@3 postcss autoprefixer vitest@1 @vitest/ui
```

Expected: 5 packages added.

- [ ] **Step 6: Commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add web/ && git commit -m "feat(web): scaffold Vite + React + TS + Tailwind + vitest deps"
```

---

### Task 3: Tailwind config + base styles

**Files:**
- Create: `web/tailwind.config.ts`, `web/postcss.config.js`
- Modify: `web/src/index.css` (replace template content with Tailwind directives + base)

- [ ] **Step 1: Initialize Tailwind config**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tailwindcss init -p
```

Expected: creates `tailwind.config.js` + `postcss.config.js`.

- [ ] **Step 2: Rename to TS + configure content paths**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && mv tailwind.config.js tailwind.config.ts
```

Write `web/tailwind.config.ts`:

```ts
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
```

- [ ] **Step 3: Replace `web/src/index.css`**

Write `web/src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-white text-gray-900 font-sans antialiased;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", "Inter", sans-serif;
  }
  h1 { @apply text-3xl font-bold leading-tight; }
  h2 { @apply text-xl font-semibold mt-8 mb-3; }
  h3 { @apply text-base font-semibold mt-6 mb-2; }
  p  { @apply leading-relaxed mb-3; }
  ul { @apply list-disc pl-6 mb-3 space-y-1; }
  li { @apply leading-relaxed; }
  a  { @apply text-blue-600 underline hover:text-blue-800; }
  details { @apply my-3; }
  summary { @apply cursor-pointer text-gray-600 hover:text-gray-900 select-none; }
}
```

- [ ] **Step 4: Verify Tailwind compiles**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && timeout 8 npm run dev 2>&1 | grep -E "(Local|error|Error)" | head -5
```

Expected: "Local: http://localhost:5173/" with no Tailwind compile errors.

- [ ] **Step 5: Commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add web/ && git commit -m "feat(web): tailwind config + base typography"
```

---

### Task 4: Types + parseArticle (TDD)

**Files:**
- Create: `web/src/types.ts`
- Create: `web/src/lib/parseArticle.ts`
- Test: `web/src/lib/parseArticle.test.ts`
- Modify: `web/package.json` (add `test` script)
- Modify: `web/vite.config.ts` (add vitest config)

- [ ] **Step 1: Add `test` script + vitest config**

Modify `web/package.json` — add `"test": "vitest"` to scripts:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "eslint .",
    "preview": "vite preview",
    "test": "vitest"
  }
}
```

Modify `web/vite.config.ts` — add vitest test config:
```ts
/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'node',
    globals: true,
  },
});
```

- [ ] **Step 2: Write `web/src/types.ts`**

Write:
```ts
export interface SourceMeta {
  name: string;
  url: string;
  published: string; // ISO date YYYY-MM-DD
  raw_title: string;
}

export interface LeftMeta {
  author: string;
  word_count: number;
  key_view: 'lạc quan' | 'thận trọng' | 'trung lập';
  skeptic_verdict: string;
  pipeline_version: string;
  format_check: string;
}

export interface WhyChosenItem {
  label: string;
  content: string;
}

export interface FunnelItem {
  source: string;
  url: string;
  published: string;
  reason: string;
}

export interface CrawlFunnelData {
  picked: FunnelItem[];
  rejected_editor_v1: FunnelItem[];
  rejected_story_editor: FunnelItem[];
  rejected_master: FunnelItem[];
}

export interface ArticleMeta {
  title: string;
  ticker: string;
  sector: string;
  sector_icon: string;
  crawled_at: string;
  funnel_batch_id: string;
  left_meta: LeftMeta;
  right_source: SourceMeta;
  insight: string;
  why_chosen: WhyChosenItem[];
  crawl_funnel: CrawlFunnelData;
  pipeline_log: Record<string, unknown>;
}

export interface Article {
  id: string;
  meta: ArticleMeta;
  leftMarkdown: string;
  rightMarkdown: string;
}

export interface ArticleSummary {
  id: string;
  ticker: string;
  sector: string;
  title: string;
  crawled_at: string;
  key_view: string;
  word_count: number;
}

export interface Manifest {
  articles: ArticleSummary[];
}
```

- [ ] **Step 3: Write the failing test**

Write `web/src/lib/parseArticle.test.ts`:

```ts
import { describe, it, expect } from 'vitest';
import { parseArticle } from './parseArticle';

const SAMPLE = `---
title: "VCB quý I"
ticker: VCB
sector: Bank
sector_icon: "🏦"
crawled_at: 2026-05-08T15:30:00+07:00
funnel_batch_id: VCB-20260508-1530
left_meta:
  author: "Chuyên gia ngân hàng"
  word_count: 354
  key_view: "thận trọng"
  skeptic_verdict: "pass_with_caveats"
  pipeline_version: "V3.6"
  format_check: "0% Anh + 400 hard cap"
right_source:
  name: "Báo Pháp luật"
  url: "https://example.com/article"
  published: 2026-05-07
  raw_title: "Vietcombank Q1"
insight: "Phù hợp NĐT giá trị giữ trên 12 tháng."
why_chosen: []
crawl_funnel:
  picked: []
  rejected_editor_v1: []
  rejected_story_editor: []
  rejected_master: []
pipeline_log: {}
---

<!-- left -->

Lợi nhuận quý I/2026 đạt **11.803 tỷ đồng**.

## Cần để ý

caveat narrative.

<!-- right -->

Raw text gốc full body.
`;

describe('parseArticle', () => {
  it('extracts frontmatter into meta', () => {
    const article = parseArticle('VCB-20260508-1530', SAMPLE);
    expect(article.id).toBe('VCB-20260508-1530');
    expect(article.meta.ticker).toBe('VCB');
    expect(article.meta.sector_icon).toBe('🏦');
    expect(article.meta.left_meta.word_count).toBe(354);
    expect(article.meta.right_source.name).toBe('Báo Pháp luật');
  });

  it('splits left markdown ending at <!-- right --> marker', () => {
    const article = parseArticle('id', SAMPLE);
    expect(article.leftMarkdown).toContain('Lợi nhuận quý I/2026');
    expect(article.leftMarkdown).toContain('## Cần để ý');
    expect(article.leftMarkdown).not.toContain('Raw text gốc');
    expect(article.leftMarkdown).not.toContain('<!-- right -->');
  });

  it('extracts right markdown after <!-- right --> marker', () => {
    const article = parseArticle('id', SAMPLE);
    expect(article.rightMarkdown).toContain('Raw text gốc full body');
    expect(article.rightMarkdown).not.toContain('<!-- right -->');
    expect(article.rightMarkdown).not.toContain('Lợi nhuận');
  });

  it('throws when <!-- left --> marker missing', () => {
    const bad = `---\ntitle: x\n---\n\nno markers here`;
    expect(() => parseArticle('id', bad)).toThrow(/left.*marker/i);
  });

  it('throws when <!-- right --> marker missing', () => {
    const bad = `---\ntitle: x\n---\n\n<!-- left -->\nonly left`;
    expect(() => parseArticle('id', bad)).toThrow(/right.*marker/i);
  });
});
```

- [ ] **Step 4: Run test to verify it fails**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm test -- --run parseArticle
```

Expected: FAIL with "Cannot find module './parseArticle'" or similar.

- [ ] **Step 5: Write `web/src/lib/parseArticle.ts`**

Write:
```ts
import matter from 'gray-matter';
import type { Article, ArticleMeta } from '../types';

const LEFT_MARKER = '<!-- left -->';
const RIGHT_MARKER = '<!-- right -->';

export function parseArticle(id: string, raw: string): Article {
  const { data, content } = matter(raw);

  const leftIdx = content.indexOf(LEFT_MARKER);
  const rightIdx = content.indexOf(RIGHT_MARKER);

  if (leftIdx === -1) {
    throw new Error(`Article ${id}: missing <!-- left --> marker`);
  }
  if (rightIdx === -1) {
    throw new Error(`Article ${id}: missing <!-- right --> marker`);
  }

  const leftMarkdown = content.slice(leftIdx + LEFT_MARKER.length, rightIdx).trim();
  const rightMarkdown = content.slice(rightIdx + RIGHT_MARKER.length).trim();

  return {
    id,
    meta: data as ArticleMeta,
    leftMarkdown,
    rightMarkdown,
  };
}
```

- [ ] **Step 6: Run test to verify pass**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm test -- --run parseArticle
```

Expected: 5 tests PASS.

- [ ] **Step 7: Commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add web/ && git commit -m "feat(web): types + parseArticle with frontmatter + section split (TDD)"
```

---

### Task 5: Article loader

**Files:**
- Create: `web/src/lib/articleLoader.ts`
- Create: `web/src/lib/format.ts`

- [ ] **Step 1: Write `web/src/lib/articleLoader.ts`**

Write:
```ts
import type { Article, ArticleSummary, Manifest } from '../types';
import { parseArticle } from './parseArticle';

const ARTICLES_BASE = '/articles';

export async function loadManifest(): Promise<ArticleSummary[]> {
  const res = await fetch(`${ARTICLES_BASE}/manifest.json`, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error(`Manifest fetch failed: ${res.status}`);
  }
  const data = (await res.json()) as Manifest;
  return [...data.articles].sort((a, b) =>
    b.crawled_at.localeCompare(a.crawled_at),
  );
}

export async function loadArticle(id: string): Promise<Article> {
  const res = await fetch(`${ARTICLES_BASE}/${id}.md`, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error(`Article ${id} fetch failed: ${res.status}`);
  }
  const raw = await res.text();
  return parseArticle(id, raw);
}
```

- [ ] **Step 2: Write `web/src/lib/format.ts`**

Write:
```ts
export function formatCrawledAt(iso: string): string {
  const d = new Date(iso);
  const dd = String(d.getDate()).padStart(2, '0');
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const yyyy = d.getFullYear();
  const hh = String(d.getHours()).padStart(2, '0');
  const mi = String(d.getMinutes()).padStart(2, '0');
  return `${dd}/${mm}/${yyyy} ${hh}:${mi}`;
}

export function formatPublishedDate(iso: string): string {
  const d = new Date(iso);
  const dd = String(d.getDate()).padStart(2, '0');
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const yyyy = d.getFullYear();
  return `${dd}/${mm}/${yyyy}`;
}

const KEY_VIEW_COLOR: Record<string, string> = {
  'lạc quan': 'bg-green-100 text-green-800',
  'thận trọng': 'bg-amber-100 text-amber-800',
  'trung lập': 'bg-gray-100 text-gray-800',
};

export function keyViewBadgeClass(keyView: string): string {
  return KEY_VIEW_COLOR[keyView] ?? 'bg-gray-100 text-gray-800';
}
```

- [ ] **Step 3: TypeScript check**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

Expected: zero errors.

- [ ] **Step 4: Commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add web/ && git commit -m "feat(web): articleLoader (manifest + .md fetch) + formatters"
```

---

### Task 6: Markdown wrapper + atom components

**Files:**
- Create: `web/src/components/Markdown.tsx`
- Create: `web/src/components/InsightCallout.tsx`
- Create: `web/src/components/ArticleCard.tsx`

- [ ] **Step 1: Write `web/src/components/Markdown.tsx`**

Write:
```tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export function Markdown({ children }: { children: string }) {
  return (
    <div className="prose-content">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          strong: ({ children }) => (
            <strong className="font-semibold text-gray-900">{children}</strong>
          ),
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}
```

- [ ] **Step 2: Write `web/src/components/InsightCallout.tsx`**

Write:
```tsx
export function InsightCallout({ insight }: { insight: string }) {
  return (
    <div className="my-5 flex gap-3 rounded-md border border-callout-border bg-callout-bg px-4 py-3">
      <span className="text-callout-icon text-lg leading-relaxed shrink-0">💡</span>
      <p className="leading-relaxed m-0">
        <strong className="font-semibold">Insight</strong>: {insight}
      </p>
    </div>
  );
}
```

- [ ] **Step 3: Write `web/src/components/ArticleCard.tsx`**

Write:
```tsx
import { Link } from 'react-router-dom';
import type { ArticleSummary } from '../types';
import { formatCrawledAt, keyViewBadgeClass } from '../lib/format';

export function ArticleCard({ article }: { article: ArticleSummary }) {
  return (
    <Link
      to={`/article/${article.id}`}
      className="block rounded-lg border border-gray-200 p-4 hover:border-gray-400 hover:shadow-sm transition no-underline"
    >
      <div className="flex items-center gap-2 mb-2">
        <span className="text-xs font-semibold rounded bg-blue-100 text-blue-800 px-2 py-0.5">
          {article.ticker}
        </span>
        <span
          className={`text-xs rounded px-2 py-0.5 ${keyViewBadgeClass(article.key_view)}`}
        >
          {article.key_view}
        </span>
        <span className="text-xs text-gray-500 ml-auto">{article.word_count} từ</span>
      </div>
      <h3 className="text-base font-semibold text-gray-900 leading-snug mb-2 mt-0">
        {article.title}
      </h3>
      <p className="text-xs text-gray-500 m-0">
        🕐 {formatCrawledAt(article.crawled_at)}
      </p>
    </Link>
  );
}
```

- [ ] **Step 4: TypeScript check**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

Expected: zero errors.

- [ ] **Step 5: Commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add web/ && git commit -m "feat(web): Markdown wrapper + InsightCallout + ArticleCard atoms"
```

---

### Task 7: Collapsible components (CrawlFunnel + PipelineLog)

**Files:**
- Create: `web/src/components/CrawlFunnel.tsx`
- Create: `web/src/components/PipelineLog.tsx`

- [ ] **Step 1: Write `web/src/components/CrawlFunnel.tsx`**

Write:
```tsx
import type { CrawlFunnelData, FunnelItem } from '../types';
import { formatPublishedDate } from '../lib/format';

function FunnelGroup({
  emoji,
  label,
  items,
  type,
}: {
  emoji: string;
  label: string;
  items: FunnelItem[];
  type: 'picked' | 'rejected';
}) {
  if (items.length === 0) return null;
  const labelColor = type === 'picked' ? 'text-green-700' : 'text-red-700';
  return (
    <div className="mb-3">
      <p className={`font-semibold mb-1 ${labelColor}`}>
        {emoji} <strong>{label}</strong> ({items.length})
      </p>
      <ul className="text-sm pl-4 space-y-1 mb-0">
        {items.map((item, i) => (
          <li key={i}>
            <a href={item.url} target="_blank" rel="noopener noreferrer">
              <strong>{item.source}</strong>
            </a>{' '}
            <span className="text-gray-500">({formatPublishedDate(item.published)})</span>{' '}
            — {item.reason}
          </li>
        ))}
      </ul>
    </div>
  );
}

export function CrawlFunnel({
  data,
  funnelBatchId,
}: {
  data: CrawlFunnelData;
  funnelBatchId: string;
}) {
  const total =
    data.picked.length +
    data.rejected_editor_v1.length +
    data.rejected_story_editor.length +
    data.rejected_master.length;

  return (
    <details>
      <summary className="text-sm">
        📊 Crawl funnel — đã search nhiều nguồn, {total} candidate, {data.picked.length} picked
      </summary>
      <div className="mt-3 text-sm">
        <p className="text-gray-500 text-xs mb-3">
          <strong>Funnel batch</strong>: <code>{funnelBatchId}</code> · Sort: by Published_time desc
        </p>
        <FunnelGroup emoji="✅" label="Picked" items={data.picked} type="picked" />
        <FunnelGroup
          emoji="❌"
          label="Rejected by Editor V1"
          items={data.rejected_editor_v1}
          type="rejected"
        />
        <FunnelGroup
          emoji="❌"
          label="Rejected by Story Editor"
          items={data.rejected_story_editor}
          type="rejected"
        />
        <FunnelGroup
          emoji="❌"
          label="Rejected by Master"
          items={data.rejected_master}
          type="rejected"
        />
      </div>
    </details>
  );
}
```

- [ ] **Step 2: Write `web/src/components/PipelineLog.tsx`**

Write:
```tsx
export function PipelineLog({ log }: { log: Record<string, unknown> }) {
  if (!log || Object.keys(log).length === 0) return null;
  return (
    <details className="mt-6 border-t border-gray-200 pt-3">
      <summary className="text-sm">📋 Pipeline log</summary>
      <pre className="mt-3 bg-gray-50 rounded p-3 overflow-x-auto text-xs leading-relaxed">
        {JSON.stringify(log, null, 2)}
      </pre>
    </details>
  );
}
```

- [ ] **Step 3: TypeScript check**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

Expected: zero errors.

- [ ] **Step 4: Commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add web/ && git commit -m "feat(web): CrawlFunnel + PipelineLog collapsible components"
```

---

### Task 8: LeftColumn + RightColumn

**Files:**
- Create: `web/src/components/LeftColumn.tsx`
- Create: `web/src/components/RightColumn.tsx`

- [ ] **Step 1: Write `web/src/components/LeftColumn.tsx`**

Write:
```tsx
import type { LeftMeta } from '../types';
import { Markdown } from './Markdown';
import { InsightCallout } from './InsightCallout';
import { PipelineLog } from './PipelineLog';

export function LeftColumn({
  title,
  meta,
  insight,
  body,
  pipelineLog,
}: {
  title: string;
  meta: LeftMeta;
  insight: string;
  body: string;
  pipelineLog: Record<string, unknown>;
}) {
  return (
    <section>
      <h2>✍️ Bài AI viết lại</h2>
      <p className="text-base font-semibold text-gray-800 mb-1 mt-0">
        <a href="#" className="underline">
          {title}
        </a>
      </p>
      <p className="text-sm text-gray-500 italic mb-4">
        — {meta.author} · {meta.word_count} từ · key view: {meta.key_view} · Skeptic:{' '}
        <code>{meta.skeptic_verdict}</code> · {meta.pipeline_version}
        <br />
        {meta.format_check}
      </p>

      <InsightCallout insight={insight} />
      <Markdown>{body}</Markdown>
      <PipelineLog log={pipelineLog} />
    </section>
  );
}
```

- [ ] **Step 2: Write `web/src/components/RightColumn.tsx`**

Write:
```tsx
import type { CrawlFunnelData, SourceMeta, WhyChosenItem } from '../types';
import { Markdown } from './Markdown';
import { CrawlFunnel } from './CrawlFunnel';
import { formatPublishedDate } from '../lib/format';

export function RightColumn({
  source,
  whyChosen,
  crawlFunnel,
  funnelBatchId,
  rawBody,
}: {
  source: SourceMeta;
  whyChosen: WhyChosenItem[];
  crawlFunnel: CrawlFunnelData;
  funnelBatchId: string;
  rawBody: string;
}) {
  return (
    <section>
      <h2>📰 Raw text gốc + meta</h2>
      <p className="text-base font-semibold text-gray-800 mb-1 mt-0">{source.raw_title}</p>
      <p className="text-sm text-gray-500 italic mb-4">
        Nguồn:{' '}
        <a href={source.url} target="_blank" rel="noopener noreferrer">
          {source.name} — bấm để đọc bài gốc
        </a>{' '}
        · Published {formatPublishedDate(source.published)}
      </p>

      <div className="mb-5">
        <p className="font-semibold mb-2">Cách viết & lý do chọn:</p>
        <ul>
          {whyChosen.map((item, i) => (
            <li key={i}>
              <strong>{item.label}</strong>: {item.content}
            </li>
          ))}
        </ul>
      </div>

      <CrawlFunnel data={crawlFunnel} funnelBatchId={funnelBatchId} />

      <details className="mt-4">
        <summary className="text-sm">📖 Click đọc full bài viết gốc</summary>
        <div className="mt-3 text-sm">
          <Markdown>{rawBody}</Markdown>
        </div>
      </details>
    </section>
  );
}
```

- [ ] **Step 3: TypeScript check**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

Expected: zero errors.

- [ ] **Step 4: Commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add web/ && git commit -m "feat(web): LeftColumn + RightColumn composing all sub-components"
```

---

### Task 9: CompareFeedLayout (2-col wrapper)

**Files:**
- Create: `web/src/components/CompareFeedLayout.tsx`

- [ ] **Step 1: Write `web/src/components/CompareFeedLayout.tsx`**

Write:
```tsx
import type { Article } from '../types';
import { LeftColumn } from './LeftColumn';
import { RightColumn } from './RightColumn';
import { formatCrawledAt } from '../lib/format';

export function CompareFeedLayout({ article }: { article: Article }) {
  const { meta, leftMarkdown, rightMarkdown } = article;
  return (
    <article className="max-w-7xl mx-auto px-4 py-6">
      <header>
        <h1 className="leading-tight">
          {meta.sector_icon} {meta.title}
        </h1>
        <p className="text-sm text-gray-500 italic mt-2">
          🕐 Crawled {formatCrawledAt(meta.crawled_at)} · Funnel batch: {meta.funnel_batch_id}
        </p>
      </header>

      <hr className="my-5 border-gray-200" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-10 gap-y-6">
        <LeftColumn
          title={meta.title}
          meta={meta.left_meta}
          insight={meta.insight}
          body={leftMarkdown}
          pipelineLog={meta.pipeline_log}
        />
        <RightColumn
          source={meta.right_source}
          whyChosen={meta.why_chosen}
          crawlFunnel={meta.crawl_funnel}
          funnelBatchId={meta.funnel_batch_id}
          rawBody={rightMarkdown}
        />
      </div>
    </article>
  );
}
```

- [ ] **Step 2: TypeScript check**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

Expected: zero errors.

- [ ] **Step 3: Commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add web/ && git commit -m "feat(web): CompareFeedLayout 2-col grid wrapper"
```

---

### Task 10: Pages + react-router

**Files:**
- Create: `web/src/pages/IndexPage.tsx`
- Create: `web/src/pages/ArticlePage.tsx`
- Modify: `web/src/App.tsx`
- Modify: `web/src/main.tsx`

- [ ] **Step 1: Write `web/src/pages/IndexPage.tsx`**

Write:
```tsx
import { useEffect, useState } from 'react';
import type { ArticleSummary } from '../types';
import { loadManifest } from '../lib/articleLoader';
import { ArticleCard } from '../components/ArticleCard';

export function IndexPage() {
  const [articles, setArticles] = useState<ArticleSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadManifest()
      .then((list) => {
        setArticles(list);
        setLoading(false);
      })
      .catch((e: Error) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <header className="mb-6">
        <h1>📰 Newsroom Compare Feed</h1>
        <p className="text-sm text-gray-500 mt-2">
          {loading ? 'Loading…' : `${articles.length} bài`}
        </p>
      </header>

      {error && (
        <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-800">
          Lỗi load manifest: {error}
        </div>
      )}

      {!loading && !error && articles.length === 0 && (
        <p className="text-gray-500">
          Chưa có bài nào. Chạy pipeline (Phase 3+) để generate bài mới.
        </p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {articles.map((a) => (
          <ArticleCard key={a.id} article={a} />
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Write `web/src/pages/ArticlePage.tsx`**

Write:
```tsx
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import type { Article } from '../types';
import { loadArticle } from '../lib/articleLoader';
import { CompareFeedLayout } from '../components/CompareFeedLayout';

export function ArticlePage() {
  const { id } = useParams<{ id: string }>();
  const [article, setArticle] = useState<Article | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setArticle(null);
    setError(null);
    loadArticle(id)
      .then(setArticle)
      .catch((e: Error) => setError(e.message));
  }, [id]);

  return (
    <div>
      <nav className="max-w-7xl mx-auto px-4 pt-4">
        <Link to="/" className="text-sm">
          ← Quay lại danh sách
        </Link>
      </nav>
      {error && (
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-800">
            Lỗi load bài: {error}
          </div>
        </div>
      )}
      {!article && !error && (
        <p className="max-w-7xl mx-auto px-4 py-6 text-gray-500">Loading…</p>
      )}
      {article && <CompareFeedLayout article={article} />}
    </div>
  );
}
```

- [ ] **Step 3: Replace `web/src/App.tsx`**

Write:
```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { IndexPage } from './pages/IndexPage';
import { ArticlePage } from './pages/ArticlePage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<IndexPage />} />
        <Route path="/article/:id" element={<ArticlePage />} />
      </Routes>
    </BrowserRouter>
  );
}
```

- [ ] **Step 4: Verify `web/src/main.tsx` imports `index.css`**

Open `web/src/main.tsx`. Confirm the file contains `import './index.css';`. If not, add it. The Vite template usually includes this; only edit if missing.

- [ ] **Step 5: TypeScript check**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

Expected: zero errors.

- [ ] **Step 6: Commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add web/ && git commit -m "feat(web): IndexPage + ArticlePage + react-router setup"
```

---

### Task 11: Bootstrap sample VCB markdown từ Notion

**Files:**
- Create: `output/compare-feed/VCB-20260508-1530.md`

This task uses Notion MCP to fetch the existing VCB article on Compare Feed page, then hand-converts it to the markdown frontmatter format. Mock fields are filled where the existing Notion article doesn't have V3.6-shape data.

- [ ] **Step 1: Fetch Compare Feed page block tree via MCP**

Use these MCP calls to traverse:
- `mcp__notion__API-get-block-children(block_id="359273c7-a9a1-81bd-88f6-ebf0d954551d", page_size=20)` → root blocks (heading, crawled_meta paragraph, column_list, divider, ...)
- For column_list block (id known to be `a70fe9fc-8ee0-4fc1-8352-9e7d1a3204e9`), get its 2 column children:
  - Left column `4d69490d-f42a-430e-8609-936cbc8e6aca`
  - Right column `597ef5da-e41b-43d3-b74f-8d9d035092cc`
- For each column, recursively `get-block-children` to extract headings, paragraphs, bulleted_list_item, callouts, toggles, code blocks
- Walk and concatenate `rich_text` plain_text from each block, preserving structure

Render rules block→markdown:
- `heading_2` → `## <text>`
- `heading_3` → `### <text>`
- `paragraph` → text + double newline
- `bulleted_list_item` → `- <text>` per line
- `callout` (insight) → extract content into frontmatter `insight` field, NOT body
- `toggle` (Pipeline log, Crawl funnel) → extract internals + populate frontmatter `pipeline_log` / `crawl_funnel` JSON
- `bold` annotation → `**text**`
- `italic` annotation → `*text*`
- `code` annotation → `` `text` ``

- [ ] **Step 2: Write `output/compare-feed/VCB-20260508-1530.md`**

Create directory + file. Schema MUST follow spec Section 5.2 with ALL frontmatter keys present (use mock values where Notion lacks data).

Mandatory frontmatter keys (fill from Notion if available, mock with realistic V3.6-style values otherwise — mark mock fields with `# MOCK — replace Phase 4`):

```yaml
title: "<from Notion heading_1>"
ticker: VCB
sector: Bank
sector_icon: "🏦"
crawled_at: 2026-05-08T15:30:00+07:00          # from Notion crawled paragraph
funnel_batch_id: VCB-20260508-1530             # from Notion crawled paragraph
left_meta:
  author: "<from Notion left meta line, e.g. 'Chuyên gia ngân hàng'>"
  word_count: <count words in body>
  key_view: "<from Notion meta line, e.g. 'thận trọng'>"
  skeptic_verdict: "<from Notion, e.g. 'pass_with_caveats'>"
  pipeline_version: "V3.6"
  format_check: "0% Anh + 400 hard cap"
right_source:
  name: "<from Notion right column source line>"
  url: "<href from Notion source link>"
  published: <YYYY-MM-DD from Notion>
  raw_title: "<from Notion right column raw title>"
insight: "<from Notion left column callout>"
why_chosen:
  - label: "Vì sao chọn bài này"
    content: "<from Notion right column 'Cách viết' bullet>"
  - label: "Angle chọn"
    content: "<from Notion>"
  - label: "Data anchor"
    content: "<from Notion>"
crawl_funnel:                                   # MOCK — replace Phase 4
  picked:
    - source: "<from Notion picked entry>"
      url: "<href>"
      published: <date>
      reason: "Anchor — đầy đủ data decode mechanism"
  rejected_editor_v1: []                        # MOCK — replace Phase 4
  rejected_story_editor:                        # MOCK — replace Phase 4
    - source: "VnEconomy"
      url: "https://vneconomy.vn/example-mock"
      published: 2026-05-06
      reason: "dup_event: cùng story KQKD Q1, BPL anchor đầy đủ hơn"
  rejected_master: []                           # MOCK — replace Phase 4
pipeline_log:                                   # MOCK — replace Phase 4
  step_1_crawler:
    sources_searched: 20
    candidates_fetched: 12
  step_2_editor_v1:
    routed_to_story_editor: 5
    rejected: 3
  step_3_story_editor:
    briefs_output: 1
    rejected: 7
  step_4_master:
    accepted_hypothesis: true
    data_sources_used: ["Finpath_API/bankfinancialratios", "Notion_KB/Big4-vs-Tu-nhan-target-pattern"]
  step_5_skeptic:
    angle: "data_skepticism"
    verdict: "pass_with_caveats"
  step_6_render:
    rendered_at: 2026-05-08T15:32:14+07:00
```

Body:
```markdown
<!-- left -->

<body content from Notion left column — preserve bullets, bold, ## Cần để ý heading, ## Góc nhìn ngược heading from Skeptic if present>

<!-- right -->

<raw text full body from Notion right column "Click đọc full bài viết gốc" toggle — if missing, use the source paragraph + bullets that ARE in Notion right column>
```

- [ ] **Step 3: Validate parses successfully**

Run a quick parse test (one-off):
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && cat > /tmp/parse-check.mjs <<'EOF'
import { readFileSync } from 'fs';
import { parseArticle } from './src/lib/parseArticle.ts';
const raw = readFileSync('../output/compare-feed/VCB-20260508-1530.md', 'utf8');
const a = parseArticle('VCB-20260508-1530', raw);
console.log('OK', { ticker: a.meta.ticker, leftLen: a.leftMarkdown.length, rightLen: a.rightMarkdown.length });
EOF
npx tsx /tmp/parse-check.mjs
```

Expected: `OK { ticker: 'VCB', leftLen: <large>, rightLen: <large> }` with no thrown error.

If `tsx` not installed, use vitest instead:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && cat > /tmp/parse-check.test.ts <<'EOF'
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { parseArticle } from '../src/lib/parseArticle';

describe('sample VCB article', () => {
  it('parses without error and contains expected sections', () => {
    const raw = readFileSync(
      resolve(__dirname, '../../output/compare-feed/VCB-20260508-1530.md'),
      'utf8',
    );
    const a = parseArticle('VCB-20260508-1530', raw);
    expect(a.meta.ticker).toBe('VCB');
    expect(a.leftMarkdown.length).toBeGreaterThan(200);
    expect(a.rightMarkdown.length).toBeGreaterThan(50);
  });
});
EOF
mv /tmp/parse-check.test.ts src/lib/sampleArticle.test.ts
npm test -- --run sampleArticle
```

Expected: 1 test PASS.

- [ ] **Step 4: Commit**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add output/ web/src/lib/sampleArticle.test.ts && git commit -m "feat: bootstrap sample VCB markdown from Notion (mock V3.6 fields)"
```

---

### Task 12: Manifest + symlink + visual verification

**Files:**
- Create: `output/compare-feed/manifest.json`
- Create symlink: `web/public/articles → ../../output/compare-feed`

- [ ] **Step 1: Write `output/compare-feed/manifest.json`**

Write:
```json
{
  "articles": [
    {
      "id": "VCB-20260508-1530",
      "ticker": "VCB",
      "sector": "Bank",
      "title": "<EXACT title from VCB-20260508-1530.md frontmatter>",
      "crawled_at": "2026-05-08T15:30:00+07:00",
      "key_view": "thận trọng",
      "word_count": <SAME word_count as the .md frontmatter>
    }
  ]
}
```

Replace placeholders with actual values copied from `VCB-20260508-1530.md` frontmatter.

- [ ] **Step 2: Create symlink**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web/public" && ln -s ../../output/compare-feed articles && ls -la articles/
```

Expected: `articles -> ../../output/compare-feed` symlink visible; listing shows `VCB-20260508-1530.md` + `manifest.json`.

- [ ] **Step 3: Boot dev server + smoke check via curl**

Run dev server in background:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm run dev &
DEV_PID=$!
sleep 4
curl -sf http://localhost:5173/articles/manifest.json | head -20
curl -sf http://localhost:5173/articles/VCB-20260508-1530.md | head -10
kill $DEV_PID 2>/dev/null || true
```

Expected:
- `manifest.json` returns JSON with VCB entry
- `.md` file returns frontmatter starting with `---`
- No 404 errors

- [ ] **Step 4: Visual verification (manual)**

Tell user:
> "Phase 1 implementation complete. Run `cd web && npm run dev` and open http://localhost:5173/. You should see:
> 1. **Index page** with 1 article card showing VCB ticker badge, "thận trọng" key view chip, title, word count, crawled time
> 2. Click the card → **Article page** with 2-column layout
> 3. **Left column**: title + meta line (italic gray) + 💡 Insight callout (yellow background) + body markdown with bold numbers + `## Cần để ý` heading + `## Góc nhìn ngược` heading + 📋 Pipeline log toggle at bottom
> 4. **Right column**: raw title + source link (blue) + 'Cách viết & lý do chọn' bullets + 📊 Crawl funnel collapsible + 📖 Click đọc full bài viết gốc collapsible
>
> Compare side-by-side with the Notion screenshot in spec Section 13. Flag any visual mismatch (color, spacing, typography, layout). The 💡 Insight callout should have pastel yellow bg and 💡 icon to match Notion. The 2 columns should split at lg: breakpoint (≥1024px); mobile stacks them vertically."

If user reports mismatches: file follow-up task list, fix, re-verify. Do NOT mark Phase 1 complete until visual approval.

- [ ] **Step 5: Final commit**

After visual approval:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add output/compare-feed/manifest.json web/public/articles && git commit -m "feat: manifest.json + public/articles symlink — Phase 1 viewer end-to-end"
```

- [ ] **Step 6: Tag Phase 1 done**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git tag phase-1-viewer
```

Expected: tag created, no errors.

---

## Acceptance criteria for Phase 1 done

1. ✅ `cd web && npm run dev` boots without error
2. ✅ http://localhost:5173/ shows IndexPage with 1 VCB card
3. ✅ Clicking card navigates to ArticlePage with 2-column layout
4. ✅ Left column: title + meta italic line + insight callout (yellow) + body markdown + Cần để ý + Góc nhìn ngược + Pipeline log toggle
5. ✅ Right column: raw title + source link + why-chosen bullets + Crawl funnel toggle + raw text toggle
6. ✅ `npm test` passes 6+ tests (5 parseArticle + 1 sampleArticle)
7. ✅ `npx tsc --noEmit` zero errors
8. ✅ Visual layout matches Notion screenshot 1:1 (yellow insight callout, italic meta, 2-col grid, collapsibles)
9. ✅ All commits made; `git log --oneline` shows ~12 commits with feat/chore prefixes
10. ✅ Tag `phase-1-viewer` created

---

## Out of scope for Phase 1 (defer to later phases)

- ❌ Pipeline DB SQLite ops (Phase 2)
- ❌ Finpath API wrapper (Phase 2)
- ❌ KB ingest from Notion (Phase 2 + Phase 2.0 prereq)
- ❌ YAML curated data (Phase 2)
- ❌ Crawler Python script (Phase 3)
- ❌ render_compare_feed.py (Phase 3)
- ❌ Slash command `/tin <ticker>` (Phase 3)
- ❌ LLM agents (Phase 4)
- ❌ Notion publish (Phase 6, optional)

If during Phase 1 execution you discover something needed for the viewer that wasn't planned (e.g., a Tailwind plugin, an additional library), add it as a sub-task here, don't pull from later phases.
