# Design — Page `/tai-lieu` cho visualize KB lên web

**Ngày**: 2026-05-11
**Trạng thái**: Approved, sẵn sàng implementation plan
**Scope v1**: BĐS tab (21 file). Bank + CK tab placeholder "sắp có".

## 1. Mục đích

Trực quan hóa knowledge base ngành (kb/{bank,ck,bds}/frameworks/*.md) lên web React hiện có, để:

- **Reviewer (Trung)**: review UI + nội dung KB ngay trong môi trường người đọc thật, không phải đọc file raw markdown trong editor
- **Team**: đọc KB có hệ thống — nhìn phụ lục bên trái biết KB nào con của KB nào, click qua dễ dàng, search được khi tìm khái niệm cụ thể (NAV/POS/FDI demand mechanism)
- **Auto-update**: thêm 1 file `.md` mới vào `kb/bds/frameworks/`, push lên main → GH Actions build → bài tự xuất hiện trên web. Không cần update config/manifest nào tay.

## 2. Non-goals (v1)

- **KHÔNG** edit KB từ web. Chỉ read-only.
- **KHÔNG** auto-link plain text mention giữa KB (vd "NIM-cycle" trong master file → KB Bank NIM). Defer phase sau.
- **KHÔNG** graph view / knowledge graph visualization (như arkon). Phụ lục tree là đủ cho 21 file.
- **KHÔNG** versioning / changelog timeline UI. File MD có changelog table trong content thì render bình thường, không tách riêng.
- **KHÔNG** bookmark / reading progress / dark-mode-specific styling. Reuse theme system hiện có.
- **KHÔNG** Bank + CK tab content. Hai tab này disabled với label "sắp có". Refactor structure sau khi pipeline ổn định.

## 3. Cấu trúc URL + navigation

### Route mới
```
/tai-lieu              → tab BĐS, KB Master Reference (first)
/tai-lieu/<slug>       → KB cụ thể, slug = filename không có `.md`
                         vd: /tai-lieu/bds-res-land-bank-nav
```

Sau này khi mở Bank + CK:
```
/tai-lieu?sector=bank
/tai-lieu/bank-nim-cycle
```

Sector state lưu trong URL search param `?sector=bds|bank|ck` (default `bds`). Slug = path segment.

### Header nav
Thêm 3rd link "Tài liệu" trong `Header.tsx`, position sau "Dòng tin":
```
[Logo] · Bài viết · Dòng tin · Tài liệu · ThemeSwitcher
```

## 4. Layout

### Desktop (≥1024px)
```
┌─── 280px ───┬─────── max 760px content ──────────┐
│  KB SIDEBAR │  KB CONTENT PANEL                   │
│             │                                     │
│  🔍 Search  │  Tham chiếu ngành                  │
│  Phụ lục    │  cập nhật 2026-05-11 · áp dụng: all │
│  - Tree...  │  ─────────────────────────────────  │
│             │  [rendered markdown body]           │
└─────────────┴─────────────────────────────────────┘
```

Sidebar fixed width 280px. Content panel max 760px (reading width). Khoảng cách giữa hai cột: 32px gap.

### Mobile (<1024px)
- Sidebar = drawer collapsible. Default closed.
- Header KB row có icon ☰ để mở drawer.
- Drawer slide từ trái, overlay backdrop. Click outside hoặc nhấn ESC để close.

## 5. Sidebar

### 5.1 Search box (top)
- Fuse.js fuzzy search, index 3 fields:
  - `title` (weight 3) — từ map kbTree.ts hoặc H1 body
  - `headings` (weight 2) — extract H2 + H3 từ body bằng regex `/^#{2,3}\s+(.+)$/gm`
  - `body` (weight 1) — content sau khi strip markdown syntax
- Threshold 0.4 (giống SymbolFilter pattern)
- Hiện top 5 kết quả, mỗi result:
  - KB label (Vietnamese)
  - snippet 120 chars quanh match, highlight `<mark>` token
- Click result → navigate to `/tai-lieu/<slug>` + scroll content panel đến anchor match (anchor = heading slug nếu match trong heading, top of doc nếu match in body)
- ESC clear search input + đóng kết quả popup

### 5.2 Phụ lục tree
Derived từ filename prefix bằng `lib/kbTree.ts`. Static config:

```ts
// kbTree.ts — BĐS group config. Match in order, first match wins.
// Cuối list = catch-all group "Khác" để bắt KB mới chưa có prefix biết trước.
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
  // Catch-all — KB mới không match prefix nào trên rơi vào đây.
  // Giữ slug ở đây cho đến khi maintainer quyết định thêm group mới.
  { id: 'other',   icon: '📎', label: 'Khác',
    match: () => true },
];
```

Tree behavior:
- Group expand/collapse, state nhớ trong localStorage `kb.expanded.<sector>`. Default tất cả expanded.
- Group "Tham chiếu ngành" (master) chỉ có 1 item — render flat không cần collapsible
- Active KB highlighted với `bg-brand/10` + `border-l-2 border-brand`
- Số lượng KB trong group hiện badge `(3)` mờ bên phải label group

### 5.3 Map title tiếng Việt
Bổ sung trong `kbTree.ts`:

```ts
export const BDS_TITLES: Record<string, string> = {
  'bds-industry-master-reference':        'Tham chiếu ngành',
  'bds-macro-cycle-credit':               'Chu kỳ vĩ mô & tín dụng',
  'bds-legal-framework':                  'Khung pháp lý',
  'bds-debt-leverage':                    'Đòn bẩy nợ',
  'bds-revenue-recognition-vas':          'Ghi nhận doanh thu (VAS)',
  'bds-hybrid-business-models':           'Mô hình kinh doanh lai',
  'bds-res-land-bank-nav':                'Quỹ đất & NAV',
  'bds-res-project-lifecycle':            'Vòng đời dự án',
  'bds-res-presales-backlog':             'Bán trước & backlog',
  'bds-kcn-fdi-demand-mechanism':         'Cơ chế cầu FDI',
  'bds-kcn-lease-structure':              'Cấu trúc thuê đất',
  'bds-kcn-inventory-pricing':            'Tồn kho & giá thuê',
  'bds-retail-footfall-mechanism':        'Lưu lượng khách',
  'bds-retail-anchor-vs-sme-tenants':     'Anchor & khách thuê SME',
  'bds-retail-tenant-mix-quality':        'Chất lượng tenant mix',
  'bds-office-class-tiering':             'Phân hạng văn phòng',
  'bds-office-hybrid-work-impact':        'Tác động làm việc kết hợp',
  'bds-resort-tourism-cycle':             'Chu kỳ du lịch',
  'bds-resort-condotel-legal-pitfalls':   'Cạm bẫy pháp lý condotel',
  'bds-resort-hybrid-model':              'Mô hình lai nghỉ dưỡng',
  'bds-dc-hyperscaler-power':             'Điện cho hyperscaler',
};
```

**Fallback rule** khi KB mới được thêm mà chưa có entry trong map:
1. Dùng H1 đầu tiên trong body (`/^#\s+(.+)$/m`)
2. Nếu không có H1, dùng `title` frontmatter
3. Nếu không có cả 2, dùng slug

## 6. Content panel

### 6.1 Header strip
```tsx
<header>
  <h1>{title}</h1>
  <div className="meta">
    cập nhật {last_updated} · áp dụng: {applies_to.join(' · ')}
  </div>
</header>
```

**Title strategy (cùng nguồn cho tree + content header)**:
- Resolve theo thứ tự: `BDS_TITLES[slug]` → H1 đầu tiên trong body → `meta.title` frontmatter → slug raw
- Tree sidebar VÀ content header h1 đều dùng cùng resolved title
- → reader thấy title trong tree match title trên content, không bị mismatch
- → H1 trong body bị ẩn (`h1: () => null` trong KbMarkdown) để tránh duplicate
- → KB hiện tại: master file có H1 dài "Ngành bất động sản Việt Nam — Tham chiếu ngành (6 lớp mental model)" nhưng BDS_TITLES override thành "Tham chiếu ngành". Editorial decision: ưu tiên short label cho consistency.

`last_updated` từ frontmatter (format: 2026-05-11). `applies_to` array: render chips space-separated. Special: nếu `["all"]` → "tất cả mã ngành". Nếu thiếu trường nào → ẩn (graceful degrade, không hiện "undefined").

### 6.2 Body
Tạo `<KbMarkdown>` riêng (KHÔNG modify `Markdown.tsx` hiện có — component đó article-specific). Cấu hình react-markdown:

```tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSlug from 'rehype-slug';   // ← thêm để gắn id vào heading

<ReactMarkdown
  remarkPlugins={[remarkGfm]}
  rehypePlugins={[rehypeSlug]}           // ← h2/h3 sẽ có id="<slugified-text>"
  components={{
    h1: () => null,                              // ẩn H1 trong body (đã render header strip)
    h2: ({ id, children }) => (
      <h2 id={id} className="...same style as Markdown.tsx h2..." />
    ),
    h3: ({ id, children }) => (
      <h3 id={id} className="text-[14px] font-semibold mt-5 mb-3 text-fg-0" />
    ),
    blockquote: 'border-l-4 border-brand bg-brand/5 ...',
    table: ({ children }) => (
      <div className="overflow-x-auto"><table className="...">{children}</table></div>
    ),
    a: ({ href, children }) => {
      // Cross-reference: ./other-file.md hoặc other-file.md → React Router link
      const isInternalKb = href && /\.md$/.test(href);
      if (isInternalKb) {
        const slug = href.replace(/^\.\//, '').replace(/\.md$/, '');
        return <Link to={`/tai-lieu/${slug}`}>{children}</Link>;
      }
      return <a href={href} target="_blank" rel="noopener noreferrer">{children}</a>;
    },
  }}
>
  {body}
</ReactMarkdown>
```

**Tại sao `rehype-slug`**: section 5.1 nói search result match heading → scroll đến anchor heading. Cần `<h2 id="...">` trên DOM. `rehype-slug` tự gắn id từ heading text (giống GitHub slug). `extractHeadings` (§7.4) phải dùng cùng thuật toán slugify để index slug khớp DOM id.

**Slugify algorithm**: dùng `github-slugger` (cùng lib rehype-slug dùng) qua `extractHeadings`. Bảo đảm consistency.

H1 ẩn vì title đã render trong header strip. Frontmatter cũng được strip bởi `kbLoader` parse, không reach markdown render.

### 6.3 Cross-references
- Markdown link `[text](./other-file.md)` hoặc `[text](other-file.md)` → React Router `<Link to="/tai-lieu/<slug>">`
- Link external `https://...` → `<a target="_blank">`
- Plain text mention KB khác → KHÔNG auto-link (defer)

Implementation: ReactMarkdown custom `a` component, detect URL pattern.

## 7. Data loading — Vite `import.meta.glob`

### 7.1 Loader strategy
```ts
// web/src/lib/kbLoader.ts
const rawModules = import.meta.glob('/kb/bds/**/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>;

// Path → slug:  '/kb/bds/frameworks/bds-res-land-bank-nav.md'
//             → 'bds-res-land-bank-nav'

export const BDS_DOCS: KbDoc[] = Object.entries(rawModules).map(([path, raw]) => {
  const slug = path.split('/').pop()!.replace(/\.md$/, '');
  const { meta, body } = parseFrontmatter(raw);
  return { slug, meta, body, headings: extractHeadings(body) };
});
```

Vite build inline tất cả 21 file BĐS thành JS bundle. Khoảng 100KB gzipped (markdown compress tốt). Eager mode → sẵn sàng cho search index ngay khi page load, không cần fetch async.

### 7.2 Path resolution
Vite project root = `web/`. KB folder `kb/` nằm SIBLING của web, NGOÀI root. Hai bước để glob được:

1. **`vite.config.ts`** — thêm `server.fs.allow` cho dev server access ngoài root:
   ```ts
   export default defineConfig({
     // ... existing config ...
     server: {
       fs: { allow: ['..', '.'] },  // cho phép glob ../kb
     },
   });
   ```

2. **Glob path relative từ caller file** — `web/src/lib/kbLoader.ts`:
   ```ts
   const rawModules = import.meta.glob('../../../kb/bds/**/*.md', {
     query: '?raw',
     import: 'default',
     eager: true,
   }) as Record<string, string>;
   ```
   `../../../kb/bds/` = `web/src/lib/` → `web/src/` → `web/` → root → `kb/bds/`.

3. **Build mode**: Vite `import.meta.glob` resolve tại build time, inline content vào bundle. `fs.allow` chỉ ảnh hưởng dev server, không ảnh hưởng build. Production bundle tự chứa.

**Spike verified 2026-05-11**: tạo `web/src/_kb_spike.ts` với glob `'../../kb/bds/**/*.md'`, chạy `npx vite build --config vite.spike.config.ts` → bundle output `dist-spike/kb-spike.js` 186KB raw / **47KB gzipped** chứa 21 module transformed + KB strings ("bds-res-land-bank-nav", "Tham chiếu"). Cả config `fs.allow` + relative path approach work. Implementation lock theo path config trên.

### 7.3 Frontmatter parser (inline)
```ts
function parseFrontmatter(raw: string): { meta: KbMeta; body: string } {
  const m = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) return { meta: {}, body: raw };
  const meta: any = {};
  for (const line of m[1].split('\n')) {
    const kv = line.match(/^(\w+):\s*(.*)$/);
    if (!kv) continue;
    const [, key, val] = kv;
    if (val.startsWith('[') && val.endsWith(']')) {
      try { meta[key] = JSON.parse(val); }
      catch { meta[key] = val; }
    } else {
      meta[key] = val.replace(/^["']|["']$/g, '');
    }
  }
  return { meta, body: m[2] };
}
```

Frontmatter trong KB hiện tại đều flat key:value. Không nested. Không cần `gray-matter` library.

### 7.4 Heading extraction
```ts
function extractHeadings(body: string): Heading[] {
  const matches = [...body.matchAll(/^(#{2,3})\s+(.+)$/gm)];
  return matches.map((m) => ({
    level: m[1].length,
    text: m[2].trim(),
    slug: slugify(m[2]),
  }));
}
```

Headings dùng cho:
- Search index field
- (Future) on-page TOC sidebar

## 8. Search implementation

### 8.1 Index build
```ts
import Fuse from 'fuse.js';

const searchIndex = new Fuse(BDS_DOCS, {
  keys: [
    { name: 'meta.title', weight: 3 },
    { name: 'headings.text', weight: 2 },
    { name: 'body', weight: 1 },
  ],
  includeMatches: true,
  ignoreLocation: true,
  threshold: 0.4,
  minMatchCharLength: 2,
});
```

### 8.2 Result render
```ts
const results = searchIndex.search(query, { limit: 5 });
// → [{ item: KbDoc, matches: [{ key, indices, value }] }]
```

Mỗi result:
- Label: VN title từ `BDS_TITLES[slug]` hoặc fallback
- Snippet: extract 60 chars trước + 60 chars sau match indices, render `<mark>` cho match range
- Click → navigate + auto-scroll

### 8.3 Empty state
- Query empty → ẩn results panel, hiện phụ lục bình thường
- Query có nhưng 0 result → "Không có KB nào khớp '{query}'."

## 9. Files

### 9.1 Mới
| Path | Mục đích |
|---|---|
| `web/src/pages/KbPage.tsx` | Route handler — read URL state, render sidebar + content |
| `web/src/components/kb/KbSidebar.tsx` | Container — search box + tree |
| `web/src/components/kb/KbTree.tsx` | Tree render — groups collapse/expand, active state |
| `web/src/components/kb/KbSearch.tsx` | Fuse.js search box + results popup |
| `web/src/components/kb/KbContent.tsx` | Header strip + Markdown body |
| `web/src/components/kb/KbTabs.tsx` | 3 sector tabs (BĐS active, Bank/CK disabled) |
| `web/src/lib/kbLoader.ts` | Vite glob + parse frontmatter + extract headings |
| `web/src/lib/kbTree.ts` | Group config + VN title map + helpers |
| `web/src/components/kb/KbMarkdown.tsx` | react-markdown setup riêng cho KB (rehype-slug + internal link routing) |

### 9.2 Edit
| Path | Thay đổi |
|---|---|
| `web/src/App.tsx` | Add route `/tai-lieu` + `/tai-lieu/:slug` |
| `web/src/components/Header.tsx` | Add 3rd nav link "Tài liệu" |
| `web/vite.config.ts` | Add `server.fs.allow: ['..', '.']` cho dev server glob outside web/ |
| `web/package.json` | Add deps: `fuse.js` (~5KB gz) + `rehype-slug` (~1KB gz) + `github-slugger` (~1KB gz) |

### 9.3 Không động
- KB markdown files (kb/bds/frameworks/*.md) — unchanged
- Pipeline (lib/, .claude/skills/) — unchanged
- Existing pages (Index, Feed, Article) — unchanged

## 10. Auto-update flow

```
1. Trung viết KB mới: kb/bds/frameworks/bds-retail-format-shift.md
2. git add kb/bds/frameworks/bds-retail-format-shift.md
3. git commit -m "kb(bds): add retail format shift"
4. git push origin main
5. GH Actions trigger:
   - npm install (web/)
   - npm run build (web/)
     - Vite import.meta.glob picks up new .md → inline as raw string
     - Build output: dist/assets/index-<hash>.js with new KB content
   - gh-pages deploy
6. Web cập nhật:
   - Sidebar tree: file mới fallback vào group "Bán lẻ" (prefix bds-retail-*)
   - URL accessible: /tai-lieu/bds-retail-format-shift
   - Search index: bao gồm content mới
7. Trung báo team: "có KB mới về retail format shift, vào /tai-lieu xem"
```

Trường hợp KB mới không match prefix nào (vd `bds-newcategory-foo.md`):
- Fallback: render trong group "Khái niệm chung" (catch-all cuối tree)
- Title: dùng H1 hoặc frontmatter
- Cần update `BDS_GROUPS` config khi muốn tạo nhóm mới

## 11. Edge cases + error handling

| Tình huống | Hành vi |
|---|---|
| KB file thiếu frontmatter | Parse trả `meta = {}`, body = full raw. Header strip ẩn meta line. Title = H1 body hoặc slug. |
| KB file thiếu `last_updated` | Ẩn "cập nhật ..." trong header strip. |
| KB file thiếu `applies_to` | Ẩn "áp dụng: ..." trong header strip. |
| URL `/tai-lieu/<slug-không-tồn-tại>` | Render error state "KB này không tồn tại. Xem [danh sách KB](/tai-lieu)." |
| URL `/tai-lieu` không có slug | Auto-redirect đến KB Master (bds-industry-master-reference) |
| Tree fallback khi prefix không match | Group "Khái niệm chung" |
| Search query 1 ký tự | minMatchCharLength=2 → không show kết quả, không lỗi |
| Tab Bank/CK click | Button disabled, hover hiện tooltip "Sắp có — đang refactor pipeline" |

## 12. Phụ lục: arkon analysis

[GitHub nduckmink/arkon](https://github.com/nduckmink/arkon) là enterprise knowledge wiki — full stack FastAPI + PostgreSQL + pgvector + Redis + MinIO + Next.js + MCP server. Mục tiêu: org-wide AI knowledge hub.

**Áp dụng được gì:**
- ✅ **3-panel browser pattern** (page tree | content | backlinks/meta) — vay mượn ý tưởng 2-panel ở v1 (tree | content), defer backlinks panel
- ✅ **Organize by knowledge type** (SOP, Product, HR Policy) — tương đương concept "group by prefix" trong design này
- ✅ **Page cross-references** — defer v2, plain text mention không auto-link

**KHÔNG áp dụng:**
- ❌ Full backend stack (Postgres + Redis + MinIO) — web hiện static GH Pages, không có backend
- ❌ MRP pipeline (MAP→REDUCE→PLAN→REFINE→VERIFY) compilation — KB hiện hand-craft markdown, không cần compile từ raw docs
- ❌ MCP server cho Claude integration — out of scope cho viewer
- ❌ Workspace + RBAC — newsroom là single tenant
- ❌ Draft/review workflow — KB review qua git PR, không cần in-app

**Kết luận**: arkon overkill cho use case này. Vay mượn 2-panel UX, không vay mượn architecture.

## 13. Verification checklist (sau khi implement)

- [ ] `/tai-lieu` mở được trên localhost dev, hiện sidebar + Master KB content
- [ ] Click từng group → expand/collapse smooth
- [ ] Click 1 KB → URL đổi `/tai-lieu/<slug>`, content panel render đúng, active state highlight trong tree
- [ ] Browser back/forward navigate qua các KB work
- [ ] Search "NAV" → top 5 result hiện, click → navigate + scroll match
- [ ] Search empty → results panel ẩn, tree hiện
- [ ] Mobile <1024px: sidebar drawer, toggle hoạt động
- [ ] Theme switch (light/dark/pink/...) → sidebar + content theme-aware
- [ ] Build production (`npm run build`) → bundle size không vượt 300KB gzipped (web hiện ~200KB, +100KB KB)
- [ ] Push deploy GH Pages → URL `/finpath-newsroom/tai-lieu` work
- [ ] Tạo 1 file KB test mới (`bds-test-temp.md`) → push → re-deploy → file xuất hiện trong tree group đúng. Sau verify xóa file test.
- [ ] Tab Bank + CK disabled, tooltip "Sắp có" hiện đúng

## 14. Open questions (defer phase 2)

- KB Bank + CK khi mở: cần refactor pipeline trước hay parallel? → Sau khi BĐS ổn định, đánh giá tách.
- Wiki-link auto-detect plain text "NIM-cycle" → KB Bank NIM: cần backlink registry, defer
- KB cross-sector references (vd BĐS macro reference Bank credit policy): hyperlink giữa tab → defer v2
- Per-KB changelog UI tách riêng khỏi body markdown table: hiện đủ trong body, defer redesign
- Print stylesheet / PDF export: defer khi có demand thực
- Reading progress (đánh dấu KB đã đọc): defer, cần localStorage state
- KB search ranking improvement (BM25 thay vì Fuse): defer khi corpus > 100 file

## 15. Changelog spec

| Ngày | Thay đổi |
|---|---|
| 2026-05-11 | Initial — brainstorm với user, 5 quyết định lock (scope BĐS only, 2-panel, search yes, nav "Tài liệu", tree label tiếng Việt). |
| 2026-05-11 | Advisor review fix — (1) thêm catch-all group "Khác" cuối BDS_GROUPS để auto-update không drop file; (2) thêm `rehype-slug` + `github-slugger` cho heading anchor IDs (search result scroll); (3) lock title strategy = BDS_TITLES short cho cả tree + content header (consistency); (4) spike Vite `../../kb/...` glob path → confirmed work, 47KB gz bundle, lock implementation. |
