# Finpath Newsroom — Migration sang Claude Code CLI (Design Spec)

- **Date**: 2026-05-08
- **Status**: Draft for review
- **Author**: Pair-design với user (dangtrungicloud@gmail.com)
- **Project root**: `/Users/trungdt/Desktop/Stream Intelligent/`
- **Pipeline source**: 8 skill V3.6 đang dùng trên Claude Desktop + Notion

---

## 1. Background & Problem

User đang chạy Finpath Newsroom V3.6 trên **Claude Desktop + Notion** với pipeline 6-step viết bài tin chuyên sâu cho 16 mã cổ phiếu Việt (Bank/CK/BĐS). Vấn đề:

- **Token cost cao**: insert/query data DB và KB qua Notion MCP tốn rất nhiều token mỗi pipeline run
- **Khó iterate**: skill content + DB schema sống trong Claude Desktop user-level, khó version-control + portable
- **Chỉ cần Notion làm output đẹp** cho người đọc, các bước trung gian không cần Notion

**Mục tiêu**: chuyển toàn bộ workflow sang Claude Code CLI trong project local. Giữ structure 6-step + 8 skill. Output cuối là markdown file (tạm bỏ Notion publish), web React đọc + render layout 2 cột giống Notion Compare Feed.

---

## 2. Goals & Non-Goals

### Goals (MVP)
- ✅ Pipeline chạy lệnh `/tin <TICKER>` từ Claude Code → output markdown trong `output/compare-feed/`
- ✅ Web React app render markdown với layout 2 cột (1:1 fidelity với screenshot Notion)
- ✅ Scope: **Bank only (7 mã: TCB/VCB/MBB/ACB/BID/CTG/VPB)**
- ✅ Pipeline state local: SQLite + YAML + Notion KB lazy-fetch
- ✅ Financial data từ Finpath API (verified 25+ endpoint, public no-auth)
- ✅ 5 quality gates V3.6 inheritance (0% Anh, 200-400 từ, 3-7 mechanism, narrative caveat, no metadata leak)

### Non-Goals (defer)
- ❌ Notion publish (bỏ khỏi flow MVP — Phase 6 thêm sau)
- ❌ CK + BĐS sectors (replicate sau khi Bank chạy ổn)
- ❌ Compare Feed prepend logic + Pipeline log toggle ở Notion
- ❌ Realtime quote endpoint (path /v2/overview 404 — verify lại sau khi cần)
- ❌ KBC ticker (BĐS KCN khác pattern — defer trong V3.6 gốc)

---

## 3. Architecture overview

### 3.1 Folder structure đầy đủ

```
Stream Intelligent/
├── .claude/
│   ├── commands/
│   │   └── tin.md                       # /tin <TICKER> — entry point
│   ├── agents/                          # 4 LLM agent (judgment/writing-heavy)
│   │   ├── newsroom-pipeline.md         # main orchestrator (đọc skill orchestrator)
│   │   ├── newsroom-editor.md           # Editor V1 — đọc bài + detect ticker
│   │   ├── newsroom-story-editor.md     # 6 expert questions, output 0-3 brief
│   │   ├── newsroom-master-bank.md      # 9-step writing + 5 quality gates
│   │   └── newsroom-skeptic.md          # 6 critique angles
│   └── skills/                          # 8 skill (knowledge/instruction modules)
│       ├── finpath-newsroom-orchestrator/
│       ├── finpath-newsroom-crawler/
│       ├── finpath-newsroom-editor/
│       ├── finpath-newsroom-story-editor/
│       ├── finpath-newsroom-master-bank/
│       ├── finpath-newsroom-master-ck/      # placeholder MVP, không build
│       ├── finpath-newsroom-master-bds/     # placeholder MVP, không build
│       └── finpath-newsroom-skeptic/
├── lib/
│   ├── finpath_api.py                   # Wrapper 10+ endpoint Bank, type-safe + cache
│   ├── pipeline_db.py                   # SQLite ops (crawl_log + generated_news)
│   ├── render_compare_feed.py           # JSON state → markdown frontmatter format
│   ├── kb_loader.py                     # Local markdown loader (read kb/ folder, grep/glob)
│   ├── kb_ingest.py                     # One-time bootstrap: Notion → kb/ markdown
│   ├── notion_fetch.py                  # Helper read-only Notion via MCP (dùng cho ingest)
│   └── stages/
│       └── run_crawler.py               # Step 1 standalone Python (mechanical)
├── data/
│   ├── pipeline.db                      # SQLite — gitignore content, schema track riêng
│   ├── pipeline.schema.sql              # schema definition, git-track
│   └── manual/                          # YAML curated, git-track
│       ├── targets.yaml                 # Targets vs Actual ĐHĐCĐ → quý
│       ├── credit_room.yaml             # NHNN allocation per bank per năm
│       └── nhnn_circulars.yaml          # thông tư NHNN affecting Bank
├── kb/                                  # KB markdown bootstrap từ Notion (git-track)
│   └── bank/
│       ├── frameworks/                  # vd bank-liquidity-3-layer.md, big4-vs-tunhan.md
│       ├── trends/                      # CASA-evolution.md, credit-growth-policy-NHNN.md
│       ├── history/                     # 2018-NPL-spike.md, 2022-bond-crisis.md
│       └── per-ticker/                  # VCB.md, TCB.md (1 file/mã)
├── output/
│   └── compare-feed/                    # markdown 1 file/bài
│       ├── VCB-20260508-1530.md
│       └── ...
├── web/                                 # Vite + React 18 + TS + Tailwind viewer
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── pages/
│       │   ├── IndexPage.tsx            # list bài, sort by crawled_at desc
│       │   └── ArticlePage.tsx          # 2-column view per bài
│       ├── components/
│       │   ├── CompareFeedLayout.tsx    # 2-col grid responsive
│       │   ├── LeftColumn.tsx           # ✍️ Bài AI viết lại
│       │   ├── RightColumn.tsx          # 📰 Raw + meta + funnel
│       │   ├── InsightCallout.tsx       # 💡 callout vàng nhạt
│       │   ├── CrawlFunnel.tsx          # collapsible funnel
│       │   ├── PipelineLog.tsx          # collapsible Step 1-6 log
│       │   └── ArticleCard.tsx          # IndexPage card item
│       └── lib/
│           ├── parseArticle.ts          # gray-matter + section split
│           └── articleLoader.ts         # Vite glob import từ ../../output/
├── config/
│   ├── finpath_api.yaml                 # base URL + endpoint catalog
│   └── notion.yaml                      # KB integration name + future publish page_id
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-05-08-newsroom-cli-migration-design.md   # this file
├── .env                                 # FINPATH_TOKEN nếu sau cần (Bank API hiện public)
├── .gitignore                           # data/pipeline.db, data/kb_cache/, .env, node_modules/
├── pyproject.toml                       # uv-style: requests, pyyaml, python-frontmatter
├── README.md                            # quickstart + architecture pointer
└── CLAUDE.md                            # global rules V3.6 + parallel work + Vietnamese default
```

### 3.2 Mapping vai trò: Skills vs Agents vs Commands vs Scripts

Concept Claude Code có 3 layer + 1 helper:

| Layer | Vai trò | Khi dùng | File extension |
|---|---|---|---|
| **Slash Command** | Entry point, 1-line trigger | User gõ `/tin VCB` | `.claude/commands/*.md` |
| **Subagent** | Isolated context window cho judgment/writing nặng | Dispatch khi cần "thinking" độc lập | `.claude/agents/*.md` |
| **Skill** | Knowledge/instruction module (rule, workflow, examples) | Loaded by agent khi cần expertise | `.claude/skills/<name>/SKILL.md` + `references/` |
| **Python script** | Mechanical (scrape, regex, SQL, file I/O) | Agent gọi qua Bash, no LLM thinking needed | `lib/*.py` |

**Quy tắc chia layer**:
- Bước thuần mechanical (search, regex, dedupe, write SQLite) → **Python script**
- Bước cần đọc bài + judgment/regex hybrid (Editor V1 detect ticker với fallback "Vietcombank" → VCB) → **Agent**
- Bước có rule cứng + format strict (Master writing 5 gates) → **Agent + Skill**
- Bước cần variety guard, fresh impression bias-free (Story Editor, Skeptic) → **Agent + Skill** (subagent isolate context để tránh leak)

### 3.3 Pipeline 6-step mapping

| Step | Source skill | Implementation Phase X | Mechanism |
|---|---|---|---|
| 1. Crawler | `finpath-newsroom-crawler` | **Python script** `lib/stages/run_crawler.py` (single file, inline-port 3 helpers `source_whitelist.py` + `search_queries.py` + `dedupe.py` từ skill `scripts/` — KHÔNG copy như package vì folder skill có hyphen, invalid Python module name) | Pipeline agent gọi qua Bash. Web search + fetch + dedupe + write `crawl_log` SQLite. Skill `references/` chỉ provide rule docs + source whitelist data. |
| 2. Editor V1 | `finpath-newsroom-editor` | **Subagent** `newsroom-editor` | Đọc 1 row pending → detect ticker (regex + name fallback) → universe filter → route sector. Update SQLite. |
| 3. Story Editor | `finpath-newsroom-story-editor` | **Subagent** `newsroom-story-editor` | Đọc batch rows → 6 expert questions per candidate → Pass 2.5 lightweight access (Notion KB grep + web snippet) → output 0-3 brief JSON. |
| 4. Master Bank | `finpath-newsroom-master-bank` | **Subagent** `newsroom-master-bank` per brief | 9-step workflow: validate → memory → query 6 Bank DB (qua `finpath_api.py`) → query KB Notion (qua `kb_loader.py`) → web search fallback → write 200-400 từ → 5-step self-check → persist `generated_news` SQLite. |
| 5. Skeptic | `finpath-newsroom-skeptic` | **Subagent** `newsroom-skeptic` | Pass 1 fresh impression (đọc body only, không xem insight) → Pass 2 compare insight → pick 1 of 6 angles → write 100-300 từ critique → append vào row generated_news. |
| 6. Render | (orchestrator + compare-feed-layout reference) | **Python script** `lib/render_compare_feed.py` | Đọc row generated_news + crawl_log filter by funnel_batch_id → render frontmatter YAML + 2 section markdown → ghi `output/compare-feed/<ticker>-<batch_id>.md`. |

### 3.4 Pipeline flow khi user gõ `/tin VCB`

```
User: /tin VCB
  ↓
Slash command tin.md → invoke agent newsroom-pipeline
  ↓
[newsroom-pipeline agent]
  ├── Bash: python lib/stages/run_crawler.py VCB
  │   → SQLite crawl_log có N row với funnel_batch_id=VCB-20260508-1530
  │
  ├── Loop mỗi pending row:
  │   └── Dispatch subagent newsroom-editor (row_id, row_data)
  │       → updates SQLite: Editor_V1_decision = route_to_story_editor / reject
  │
  ├── Dispatch subagent newsroom-story-editor (batch processed rows)
  │   → returns 0-3 brief JSON
  │
  ├── Loop mỗi brief:
  │   ├── Dispatch subagent newsroom-master-bank (brief)
  │   │   → returns article + accepted_hypothesis
  │   │   → persists generated_news SQLite + master_decision crawl_log
  │   │
  │   └── Dispatch subagent newsroom-skeptic (master_output, brief)
  │       → returns critique
  │       → appends to generated_news row
  │
  └── Bash: python lib/render_compare_feed.py --batch VCB-20260508-1530
      → output/compare-feed/VCB-20260508-1530.md
  ↓
Web React (đang chạy `npm run dev`) hot-reload tự động pickup file mới
  ↓
User mở localhost:5173 → IndexPage list bài mới ở top → click → ArticlePage 2-column
```

---

## 4. Data layer

### 4.1 SQLite — `data/pipeline.db`

**Bảng `crawl_log`** (Step 1-5 state):

```sql
CREATE TABLE crawl_log (
  row_id              TEXT PRIMARY KEY,         -- UUID v4 generated by run_crawler.py
  funnel_batch_id     TEXT NOT NULL,            -- vd VCB-20260508-1530
  ticker              TEXT NOT NULL,
  -- Crawler fields
  source_name         TEXT NOT NULL,            -- vd "Báo Pháp luật"
  source_url          TEXT NOT NULL,
  title               TEXT NOT NULL,
  raw_content         TEXT,                     -- full body, có thể 5000+ chars
  published_time      TEXT,                     -- ISO datetime, may NULL
  crawled_at          TEXT NOT NULL,            -- ISO datetime
  -- Editor V1 fields
  detected_tickers    TEXT,                     -- JSON array
  primary_ticker      TEXT,
  sector              TEXT,                     -- Bank|CK|BĐS|rejected
  editor_v1_decision  TEXT,                     -- route_to_story_editor|reject
  editor_v1_note      TEXT,
  -- Story Editor fields
  story_editor_decision TEXT,                   -- write_brief|reject
  story_editor_note   TEXT,                     -- reject reason hoặc why_chosen
  brief_json          TEXT,                     -- full brief JSON nếu write_brief
  -- Master fields
  master_decision     TEXT,                     -- write_article|reject_no_data|reject_data_conflict
  master_note         TEXT,
  -- Pipeline state
  status              TEXT NOT NULL DEFAULT 'pending', -- pending|processed|published|rejected
  pipeline_version    TEXT NOT NULL DEFAULT 'V3.6',
  pipeline_log        TEXT,                     -- step-by-step log JSON
  notes               TEXT
);

CREATE INDEX idx_crawl_log_funnel ON crawl_log(funnel_batch_id);
CREATE INDEX idx_crawl_log_ticker_status ON crawl_log(ticker, status);
CREATE INDEX idx_crawl_log_url ON crawl_log(source_url);  -- dedupe
```

**Bảng `generated_news`** (Step 4 + 5 output):

```sql
CREATE TABLE generated_news (
  article_id          TEXT PRIMARY KEY,         -- UUID v4
  row_id              TEXT NOT NULL,            -- FK to crawl_log.row_id
  ticker              TEXT NOT NULL,
  sector              TEXT NOT NULL,
  -- Master output
  title               TEXT NOT NULL,
  body                TEXT NOT NULL,            -- main article 200-400 từ
  word_count          INTEGER,
  key_view            TEXT,                     -- lạc quan|thận trọng|trung lập
  insight_final       TEXT,                     -- 1 câu
  insight_type        TEXT,                     -- enum metadata, không leak narrative
  variety_guard_angle TEXT,                     -- free-text VN
  accepted_hypothesis INTEGER NOT NULL,         -- 0 | 1
  data_sources_used   TEXT,                     -- JSON array
  brief_json          TEXT,                     -- snapshot brief Story Editor
  history_referenced  TEXT,                     -- JSON array
  -- Skeptic output
  skeptic_critique    TEXT,                     -- 100-300 từ
  skeptic_angle       TEXT,                     -- 1 of 6 enum
  skeptic_verdict     TEXT,                     -- pass|pass_with_caveats|fail
  -- State
  status              TEXT NOT NULL DEFAULT 'draft', -- draft|published
  published_at        TEXT,
  pipeline_version    TEXT NOT NULL DEFAULT 'V3.6',
  pipeline_log        TEXT,                     -- full step 1-6 log JSON
  FOREIGN KEY (row_id) REFERENCES crawl_log(row_id)
);

CREATE INDEX idx_generated_ticker_published ON generated_news(ticker, published_at DESC);
```

**Memory check** (variety guard) trước Master invoke:
```sql
SELECT title, variety_guard_angle, insight_type, insight_final, published_at
FROM generated_news
WHERE ticker = ? AND status = 'published'
ORDER BY published_at DESC LIMIT 3;
```

### 4.2 YAML curated — `data/manual/`

**`targets.yaml`** — Targets vs Actual (kế hoạch ĐHĐCĐ vs thực tế):

```yaml
# data/manual/targets.yaml
- ticker: VCB
  year: 2026
  target_lntt_ty: 44000          # tỷ đồng
  target_credit_growth_pct: 16.5
  actual_lntt_q1_ty: 11803
  actual_credit_growth_q1_pct: 4.2
  source: "Nghị quyết ĐHĐCĐ 25/4/2026"
  source_url: "https://..."
- ticker: TCB
  year: 2026
  ...
```

**`credit_room.yaml`** — NHNN allocation:

```yaml
- ticker: VCB
  year: 2026
  credit_room_pct: 16.0
  notes: "Big4 chuẩn vốn quốc tế cao hơn → room ưu đãi"
```

**`nhnn_circulars.yaml`** — thông tư NHNN affecting Bank:

```yaml
- title: "Thông tư 02/2025/TT-NHNN"
  effective_date: 2025-04-01
  affected_topics: ["NPL classification", "Coverage ratio"]
  summary: "Siết tiêu chí phân loại nợ xấu nhóm 3-5..."
  url: "https://..."
```

### 4.3 KB markdown — bootstrap once từ Notion → local files

**Strategy** (updated): KB topics fetch ONE TIME từ Notion về project local làm markdown files. Pipeline runtime chỉ đọc local, KHÔNG gọi Notion. Lý do:
- Zero token cost runtime (grep/glob 1ms vs Notion API 200ms+)
- Git-track KB content → biết version + diff khi update
- User edit markdown trực tiếp nếu thấy KB sai/cũ
- Predictable: pipeline không phụ thuộc Notion uptime

**Source root — Bank Sector hub page**:
- URL: `https://www.notion.so/Bank-Sector-359273c7a9a1810f9306cb6227d9c94a`
- Page ID: `359273c7-a9a1-810f-9306-cb6227d9c94a` ✓ shared với `claude-mcp` integration đã verify
- Page chứa: 7 module DB (BCTC Quarter/Annual/Targets/Credit Room/M&A/Foreign/NHNN) + 1 KB sub-page "📚 KB ngành Ngân hàng" + 1 frameworks sub-page "🔬 Frameworks" (id `358273c7-a9a1-81a6-82fa-c31c02a5df62`)
- KB ingest start từ Bank Sector page → traverse mention links + child pages → tìm KB sub-page → fetch tất cả topic bên trong

**Bootstrap script — `lib/kb_ingest.py`**:

```python
def ingest_bank_sector(hub_page_id: str = "359273c7-a9a1-810f-9306-cb6227d9c94a", output_dir: str = "kb/bank/") -> dict:
    """
    One-time fetch toàn bộ KB Bank từ Notion Bank Sector page → markdown files.

    Steps:
    1. retrieve_page(hub_page_id) + get_block_children → list child pages + mentions
    2. Find sub-pages: "📚 KB ngành Ngân hàng" + "🔬 Frameworks"
    3. For mỗi sub-page → get_block_children recursively → render blocks to markdown
       (paragraph, heading_1/2/3, bulleted_list_item, numbered_list_item, callout,
        code, quote, divider, child_page, mention)
    4. Categorize: frameworks/ trends/ history/ per-ticker/ (mapped from page hierarchy hoặc tag)
    5. Slugify title → file path: kb/bank/<category>/<slug>.md
    6. Frontmatter: {notion_page_id, source_url, last_synced, category, title, breadcrumb}
    7. Idempotent: skip nếu file existed + last_synced < 24h, --force flag bypass

    Returns: {fetched: N, skipped: M, errors: [...]}
    """

# CLI: python lib/kb_ingest.py [--hub <page_id>] [--output kb/bank/] [--force]
```

**Runtime loader — `lib/kb_loader.py`** (simple local read, no Notion):

```python
def search_kb(keywords: list[str], category: str | None = None) -> list[dict]:
    """
    Grep markdown files trong kb/bank/. Return matches sorted by relevance.
    
    Returns: [{path, title, category, snippet, score}, ...]
    """

def load_kb_topic(slug_or_path: str) -> str:
    """Read full markdown content."""
```

**Rule re-ingest**: khi user update KB Notion → chạy lại `python lib/kb_ingest.py --force` → pull về. Quy trình thủ công (không cron auto-sync MVP).

**Phase 2 sẽ implement**: bootstrap script + ingest TẤT CẢ topic Bank dưới Bank Sector hub. Bank Sector page đã share với `claude-mcp` integration ✓ verified.

### 4.4 Finpath API — `lib/finpath_api.py`

**Base URL**: `https://api.finpath.vn` (verified 2026-05-08, 200 OK no auth, CloudFront cached)

**Endpoint catalog locked cho Bank**:

| Function | Endpoint | Use case |
|---|---|---|
| `get_bank_ratios(ticker)` | `GET /api/stocks/bankfinancialratios/{code}` | NIM/CASA/COF/NPL/LDR + P/E/P/B/ROE quarterly + yearly |
| `get_bank_ratios_batch(tickers)` | `GET /api/stocks/bankfinancialratios-eboard?codes=...` | Batch nhiều ticker 1 call |
| `get_income_statement(ticker)` | `GET /api/stocks/incomes/{code}` | KQKD quarterly + yearly |
| `get_full_income(ticker)` | `GET /api/stocks/fullincomestatements/{code}` | Full income detail |
| `get_balance_sheet(ticker)` | `GET /api/stocks/balancesheets/{code}` | BS quarterly + yearly |
| `get_full_balance_sheet(ticker)` | `GET /api/stocks/fullbalancesheets/{code}` | Full BS detail |
| `get_cashflow(ticker)` | `GET /api/stocks/fullcashflows/{code}` | CFS |
| `get_net_interest_income(ticker)` | `GET /api/stocks/netinterestincomes/{code}` | Doanh thu lãi thuần |
| `get_deposit_credit(ticker)` | `GET /api/stocks/depositcredit/{code}` | Tín dụng + tiền gửi |
| `get_bad_debt(ticker)` | `GET /api/stocks/baddebt/{code}` | NPL + dự phòng |
| `get_shareholders(ticker)` | `GET /api/stocks/shareholderstructure/{code}` | Foreign + state ownership |
| `get_events(ticker)` | `GET /api/events/{code}` | Dividend, ĐHĐCĐ, M&A |
| `get_news(ticker)` | `GET /api/news/{code}` | News by ticker |
| `get_company_profile(ticker)` | `GET /api/stocks/companyprofile/{code}` | Sector, industry |

**TBD** — chưa verify path đúng:
- Live realtime quote (giá/volume/change_pct) — `/api/stocks/v2/overview/{code}` returned 404 ngày 2026-05-08, cần dò path đúng khi Phase 4 cần

**Caching**: HTTP cache CloudFront 24h sẵn. Local layer thêm in-memory dict per pipeline run để tránh duplicate call cùng ticker trong 1 batch.

---

## 5. Output format — markdown 1 file/bài

### 5.1 File naming

`output/compare-feed/<TICKER>-<YYYYMMDD>-<HHMM>.md`

vd: `output/compare-feed/VCB-20260508-1530.md`

⚠️ **Design intent**: file `.md` là **structured data**, KHÔNG phải bài đọc trực tiếp. React component render heading `## ✍️ Bài AI viết lại` + `## 📰 Raw text gốc` từ component code, không từ markdown body. Nếu user `cat` file sẽ chỉ thấy frontmatter + 2 section markers + body raw — đó là correct design.

Bên cạnh mỗi bài, `output/compare-feed/manifest.json` track tất cả articles (dùng cho IndexPage list nhanh, không cần parse từng file):

```json
{
  "articles": [
    {
      "id": "VCB-20260508-1530",
      "ticker": "VCB",
      "sector": "Bank",
      "title": "VCB quý I: lãi vẫn tăng 9% dù bỏ thêm 1.700 tỷ vào quỹ phòng nợ xấu",
      "crawled_at": "2026-05-08T15:30:00+07:00",
      "key_view": "thận trọng",
      "word_count": 354
    }
  ]
}
```

### 5.2 Schema

```markdown
---
# === metadata ===
title: "VCB quý I: lãi vẫn tăng 9% dù bỏ thêm 1.700 tỷ vào quỹ phòng nợ xấu"
ticker: VCB
sector: Bank
sector_icon: "🏦"
crawled_at: 2026-05-08T15:30:00+07:00
funnel_batch_id: VCB-20260508-1530

# === left column meta ===
left_meta:
  author: "Chuyên gia ngân hàng"
  word_count: 354
  key_view: "thận trọng"           # lạc quan | thận trọng | trung lập
  skeptic_verdict: "pass_with_caveats"
  pipeline_version: "V3.6"
  format_check: "0% Anh + 400 hard cap"

# === right column meta ===
right_source:
  name: "Báo Pháp luật"
  url: "https://doanhnhan.baophapluat.vn/..."
  published: 2026-05-07
  raw_title: "Vietcombank (VCB): Lợi nhuận quý I/2026 đạt gần 11.803 tỷ đồng..."

# === insight (left column callout) ===
insight: "Phù hợp nhà đầu tư giá trị giữ trên 12 tháng — lãi không bùng nhưng độ bền cao và rủi ro chất lượng tài sản đã được chủ động cách ly."

# === why chosen (right column section) ===
why_chosen:
  - label: "Vì sao chọn bài này"
    content: "Tin Q1/2026 KQKD mới 1 day ago, paradox mạnh — dự phòng nhân hơn 3 lần nhưng nợ xấu vẫn 0,62%..."
  - label: "Angle chọn"
    content: "Chủ động xây bộ đệm — đánh đổi tốc độ lấy độ bền (hidden_mechanism)..."
  - label: "Data anchor"
    content: "DB BCTC Quarter VCB-2026-Q1 (LNTT 11.803 tỷ, dự phòng -2.493 tỷ, NPL 0,62%, NIM 2,76%)..."

# === crawl funnel (right column collapsible) ===
crawl_funnel:
  picked:
    - source: "Báo Pháp luật"
      url: "https://..."
      published: 2026-05-07
      reason: "Anchor — đầy đủ 4 con số decode mechanism"
  rejected_editor_v1: []
  rejected_story_editor:
    - source: "VnEconomy"
      url: "https://..."
      published: 2026-05-06
      reason: "dup_event: cùng story KQKD Q1, BPL anchor đầy đủ hơn"
  rejected_master: []

# === pipeline log (left column collapsible) ===
pipeline_log:
  step_1_crawler:
    sources_searched: 20
    candidates_fetched: 12
    candidates_after_dedupe: 8
  step_2_editor_v1:
    routed_to_story_editor: 5
    rejected: 3
  step_3_story_editor:
    briefs_output: 1
    rejected: 7
  step_4_master:
    accepted_hypothesis: true
    data_sources_used: ["Finpath_API/bankfinancialratios", "Finpath_API/baddebt", "Notion_KB/Big4-vs-Tu-nhan-target-pattern"]
  step_5_skeptic:
    angle: "data_skepticism"
    verdict: "pass_with_caveats"
  step_6_render:
    rendered_at: 2026-05-08T15:32:14+07:00
---

<!-- left -->

Lợi nhuận trước thuế quý I/2026 của Vietcombank đạt **11.803 tỷ đồng**, tăng 9% so cùng kỳ — nhưng đáng chú ý là chi phí dự phòng rủi ro tín dụng tăng từ 752 tỷ lên **2.493 tỷ đồng**, gấp hơn 3 lần. Vì sao một ngân hàng có tỷ lệ nợ xấu chỉ **0,62%** lại quyết liệt trích lập như vậy?

- **Tăng đệm khi đệm chưa cần dùng**: nợ xấu đã giảm từ 1,03% (cùng kỳ) xuống 0,62%. Thời điểm "bình yên" chính là lúc ngân hàng kỷ luật nhất xây dự phòng để đón chu kỳ...
- ...

## Cần để ý

[narrative caveat 50-100 từ — symbolic moment + lookforward + caveat ngược + data anchor + hàm ý NĐT]

## Góc nhìn ngược

[Skeptic 100-300 từ critique theo angle data_skepticism]

<!-- right -->

**[Title gốc full từ source]**

[Raw full article body từ web_fetch primary URL — 6 section gốc, 3000-5000 chars, giữ original heading + quote CEO/Chủ tịch nguyên italic]
```

### 5.3 Web parser

**`web/src/lib/parseArticle.ts`**:

```ts
import matter from 'gray-matter';

export interface Article {
  meta: {
    title: string;
    ticker: string;
    sector: string;
    sector_icon: string;
    crawled_at: string;
    funnel_batch_id: string;
    left_meta: { author: string; word_count: number; key_view: string; skeptic_verdict: string; pipeline_version: string; format_check: string };
    right_source: { name: string; url: string; published: string; raw_title: string };
    insight: string;
    why_chosen: { label: string; content: string }[];
    crawl_funnel: {
      picked: FunnelItem[];
      rejected_editor_v1: FunnelItem[];
      rejected_story_editor: FunnelItem[];
      rejected_master: FunnelItem[];
    };
    pipeline_log: Record<string, any>;
  };
  leftMarkdown: string;   // body bài AI viết lại
  rightMarkdown: string;  // raw text gốc
}

export function parseArticle(rawMd: string): Article {
  const { data, content } = matter(rawMd);
  const leftMatch = content.match(/<!-- left -->([\s\S]*?)<!-- right -->/);
  const rightMatch = content.match(/<!-- right -->([\s\S]*)$/);
  return {
    meta: data as Article['meta'],
    leftMarkdown: leftMatch?.[1].trim() ?? '',
    rightMarkdown: rightMatch?.[1].trim() ?? '',
  };
}
```

**`web/src/lib/articleLoader.ts`** (Symlink + manifest pattern — không dùng Vite glob vì Vite watcher không cover path ngoài `web/`):

**Setup mechanism**:
1. Tạo symlink: `ln -s ../../output/compare-feed web/public/articles` → markdown files served qua Vite static server tại `/articles/<id>.md`
2. `lib/render_compare_feed.py` mỗi lần render xong cập nhật `output/compare-feed/manifest.json`:
   ```json
   {
     "articles": [
       { "id": "VCB-20260508-1530", "ticker": "VCB", "crawled_at": "...", "title": "...", "key_view": "thận trọng" }
     ]
   }
   ```
3. React fetch manifest + individual markdown files:

```ts
export async function loadAllArticles(): Promise<ArticleSummary[]> {
  const res = await fetch('/articles/manifest.json');
  const { articles } = await res.json();
  return articles.sort((a, b) => b.crawled_at.localeCompare(a.crawled_at));
}

export async function loadArticle(id: string): Promise<Article> {
  const res = await fetch(`/articles/${id}.md`);
  const raw = await res.text();
  return parseArticle(raw);
}
```

**Hot reload**: Vite serves từ `web/public/` với HMR. New file in `output/compare-feed/` → ghi manifest → user reload trang (auto refresh nếu add manifest polling sau, MVP manual).

**Why không Vite glob**: `import.meta.glob('../../output/...')` cần `server.fs.allow: ['..']` config + watch path ngoài root, fragile, không HMR cho file thêm sau server start.

---

## 6. Web viewer — React + Vite + Tailwind

### 6.1 Tech stack

- **Vite 5** (dev server, HMR, glob import)
- **React 18** + TypeScript strict
- **Tailwind CSS** 3.x
- **react-markdown** + `remark-gfm` (table, strikethrough) + `rehype-raw` (HTML inline nếu cần)
- **gray-matter** (parse frontmatter)
- **react-router-dom** (Index ↔ Article routes)

### 6.2 Layout 2 cột (CSS grid)

```tsx
// CompareFeedLayout.tsx
<div className="max-w-7xl mx-auto px-4 py-6">
  <header>
    <h1 className="text-3xl font-bold">{sector_icon} {title}</h1>
    <p className="text-sm text-gray-500 italic">🕐 Crawled {crawled_at_display} · Funnel batch: {funnel_batch_id}</p>
  </header>
  <hr className="my-4" />
  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
    <LeftColumn meta={left_meta} insight={insight} body={leftMarkdown} pipelineLog={pipeline_log} />
    <RightColumn source={right_source} whyChosen={why_chosen} crawlFunnel={crawl_funnel} body={rightMarkdown} />
  </div>
</div>
```

### 6.3 Component breakdown

| Component | Responsibility |
|---|---|
| `CompareFeedLayout` | wrapper 2-col + header (title + crawled meta) |
| `LeftColumn` | render `## ✍️ Bài AI viết lại` + meta line + `InsightCallout` + body markdown + `PipelineLog` collapsible |
| `RightColumn` | render `## 📰 Raw text gốc + meta` + source link + 3 `WhyChosen` bullets + `CrawlFunnel` collapsible + raw body markdown |
| `InsightCallout` | callout box vàng nhạt với 💡 icon + insight text 1 câu |
| `CrawlFunnel` | `<details>` element, render 4 group: picked / rejected_editor_v1 / rejected_story_editor / rejected_master với link click ra được |
| `PipelineLog` | `<details>` element, render 6 step log JSON pretty-formatted |
| `ArticleCard` | IndexPage card item: ticker badge, title, key_view chip, word count, crawled_at relative time |

### 6.4 IndexPage layout

- Header: "📰 Newsroom Compare Feed" + count bài
- Filter sidebar: by ticker (dropdown 7 mã Bank), by key_view chip, by date range
- Grid: 2-3 col responsive, ArticleCard sort by crawled_at desc

---

## 7. Skills/Agents/Commands inventory

### 7.1 Skills (8) — `.claude/skills/<name>/SKILL.md` + `references/`

Giải nén từ 8 file `.skill` (zip) trên Desktop sang folder unzipped. Nội dung skill giữ nguyên V3.6 (rule + workflow). Edit nhỏ:
- Replace mọi `query_data_sources(data_source_id=...)` → reference `lib/finpath_api.py` hoặc `lib/pipeline_db.py` hoặc `lib/kb_loader.py`
- Replace `create_pages` / `update_pages` Notion calls → `lib/pipeline_db.py` SQLite ops
- Giữ rule structure: `Khi nào trigger`, `Workflow X bước`, `Hard rules`, `Edge cases`, `References`

### 7.2 Agents (4) — `.claude/agents/<name>.md`

Format Claude Code agent definition:

```markdown
---
name: newsroom-master-bank
description: Writing in-depth bank stock news 200-400 words from Story Editor brief. Use when pipeline routes a Bank brief.
tools: Bash, Read, Write, Edit, Grep, Glob, mcp__notion__API-retrieve-a-page, mcp__notion__API-query-data-source
---

# Master Bank Agent

You are the writing specialist for Vietnamese banking stocks (TCB/VCB/MBB/ACB/BID/CTG/VPB).

## Load skill
Use `Skill` tool: `Skill: finpath-newsroom-master-bank` — Claude Code tự load SKILL.md + references/. KHÔNG dùng Read tool cho skill files (token-inefficient, lose Skill tool's caching).

## Available tools
- `lib/finpath_api.py` for BCTC data (Bash: `python -c "from lib.finpath_api import *; ..."`)
- `lib/kb_loader.py` for Notion KB topics (lazy fetch + cache)
- `lib/pipeline_db.py` for memory check + persist generated_news

## Input (from pipeline agent)
- brief: JSON object from Story Editor
- row_id: SQLite crawl_log row ID

## Output
JSON with title/body/key_view/insight_final/accepted_hypothesis fields. See SKILL.md output schema.

## Quality gates (MUST pass before persist)
Run 5-step self-check from SKILL.md Bước 8.5. If fail → rewrite, không persist.
```

| Agent | Skill loaded | Tools cần |
|---|---|---|
| `newsroom-pipeline` | orchestrator | Bash, Task (dispatch), Read, Write |
| `newsroom-editor` | editor | Bash (call SQLite + ticker_detection script), Read |
| `newsroom-story-editor` | story-editor | Bash (SQLite memory query + KB grep), Read, Grep, **WebSearch**, **WebFetch** |
| `newsroom-master-bank` | master-bank + references | Bash (finpath_api + kb_loader + pipeline_db), Read, Write, Edit, Grep, Glob, **WebSearch**, **WebFetch** |
| `newsroom-skeptic` | skeptic | Bash (independent fetch + KB read), Read, Grep, **WebSearch**, **WebFetch** |

⚠️ Tất cả KB lookup runtime đều LOCAL (`kb/bank/` markdown). Notion MCP chỉ dùng ONE-TIME ở `lib/kb_ingest.py` bootstrap script — KHÔNG ở agent runtime.

⚠️ **WebSearch + WebFetch BẮT BUỘC** cho 3 agent thinking-heavy (Story Editor, Master, Skeptic) — xem Section 8.5 data sourcing rule. Agent phải tự research khi local sources thiếu.

### 7.3 Slash command (1) — `.claude/commands/tin.md`

```markdown
---
description: Viết bài tin chuyên sâu về 1 mã cổ phiếu Việt Nam (Bank universe MVP)
argument-hint: <TICKER>
allowed-tools: Bash, Task
---

Trigger pipeline 6-step Newsroom V3.6 for ticker $1 (Bank universe MVP only — TCB/VCB/MBB/ACB/BID/CTG/VPB).

Use the Task tool to dispatch the `newsroom-pipeline` agent with input ticker = $1.

If $1 is not in MVP universe, reply: "Ticker $1 không thuộc MVP Bank universe. CK + BĐS sẽ thêm sau."
```

---

## 8. Build order — 6 phase

### Phase 1 — Viewer vertical slice (1-2 ngày)
**Goal**: Web React render 1 sample VCB markdown đẹp 1:1 screenshot Notion.

Tasks:
1. Khởi tạo `web/` Vite + React + TS + Tailwind
2. `parseArticle.ts` (gray-matter + section split)
3. `articleLoader.ts` (fetch manifest.json + individual .md từ `/articles/` symlink)
4. `CompareFeedLayout` + `LeftColumn` + `RightColumn` + `InsightCallout` + `CrawlFunnel` + `PipelineLog`
5. `IndexPage` + `ArticlePage` + react-router setup
6. Tailwind theme: callout vàng nhạt, divider, italic gray meta line, sector icon, badge
7. Bootstrap sample: agent dùng tool `mcp__notion__API-get-block-children` fetch tất cả block của Compare Feed page (ID `359273c7-a9a1-81bd-88f6-ebf0d954551d`, đã share) → hand-convert sang markdown frontmatter format → save `output/compare-feed/VCB-20260508-1530.md`. Bài VCB hiện trên Notion có thể thiếu một số field V3.6 mới (`pipeline_log`, `crawl_funnel.rejected_master`, `data_sources_used`...) — fill bằng **mock data hợp lý preserving spec structure**, sẽ replace bằng data thật khi Phase 4 generate. Đánh dấu mock fields trong file bằng comment `# MOCK — replace Phase 4`.
8. Tạo `output/compare-feed/manifest.json` initial với 1 entry (VCB sample)
9. Symlink setup: `cd web && ln -s ../output/compare-feed public/articles`
8. Visual check: render giống screenshot user đã gửi

Exit criteria: web chạy `npm run dev` → localhost:5173 → IndexPage list 1 bài → click → ArticlePage 2-column khớp Notion.

### Phase 2.0 — Prereq (RESOLVED 2026-05-08)
**Goal**: Notion access cho ingest sẵn sàng.

✓ Bank Sector hub page `359273c7-a9a1-810f-9306-cb6227d9c94a` đã share với `claude-mcp` integration. Verified retrieve được. Không cần thêm action.

### Phase 2 — Data layer (2-3 ngày)
**Goal**: SQLite + finpath_api + KB ingested + YAML stub sẵn sàng.

Tasks:
1. `data/pipeline.schema.sql` + `lib/pipeline_db.py` ops (insert, update, query)
2. `lib/finpath_api.py` wrapper 14 endpoint Bank, type-safe (TypedDict response), in-memory cache
3. `lib/notion_fetch.py` helper read-only (page + data source query) qua MCP
4. `lib/kb_ingest.py` bootstrap script — start từ Bank Sector hub `359273c7-a9a1-810f-9306-cb6227d9c94a`, traverse child pages (📚 KB ngành Ngân hàng + 🔬 Frameworks + 7 module DB) → markdown files vào `kb/bank/<category>/<slug>.md` (idempotent với `--force` flag)
5. Run `python lib/kb_ingest.py` → pull TẤT CẢ topic Bank về local
6. `lib/kb_loader.py` runtime loader — grep `kb/bank/` (no Notion call)
7. `data/manual/targets.yaml`, `credit_room.yaml`, `nhnn_circulars.yaml` — stub 3-5 row VCB+TCB cho test
8. Unit test: `pytest lib/` — 1 test/function (ratios fetch, SQLite insert/update/query, KB grep, YAML load)

Exit criteria: `python -c "from lib.finpath_api import get_bank_ratios; print(get_bank_ratios('VCB'))"` trả về dict đúng shape.

### Phase 3 — Pipeline mechanical (2-3 ngày)
**Goal**: Crawler chạy + render layer hoàn chỉnh.

Tasks:
1. `lib/stages/run_crawler.py` — single Python file inline-port 3 helper từ skill `finpath-newsroom-crawler/scripts/` (không copy như package vì folder skill name có hyphen, invalid module name):
   - SOURCES_WHITELIST dict (20 nguồn VN + Bank universe constants)
   - `build_queries(ticker, sector)` (per ticker + sector)
   - `filter_existing_urls(urls, db_path)` SQLite dedupe
2. `lib/render_compare_feed.py`:
   - Đọc generated_news + crawl_log filter funnel_batch_id
   - Render frontmatter YAML + `<!-- left -->` body + `<!-- right -->` raw
   - Ghi `output/compare-feed/<ticker>-<batch_id>.md`
3. `.claude/commands/tin.md` slash command + `.claude/agents/newsroom-pipeline.md`
4. End-to-end test pipeline mechanical: `/tin VCB` → crawler chạy → SQLite có rows → render trống (chưa có Master output)

Exit criteria: `/tin VCB` không lỗi, SQLite có ≥1 row pending.

### Phase 4 — LLM agents (3-5 ngày)
**Goal**: 4 agent chạy + tạo bài thật.

Tasks:
1. Convert 8 skill V3.6 từ Notion-first → Claude Code-first (replace Notion calls với lib/ wrappers, giữ rule + workflow)
2. `.claude/agents/newsroom-editor.md` + integrate skill editor
3. `.claude/agents/newsroom-story-editor.md` + integrate skill story-editor
4. `.claude/agents/newsroom-master-bank.md` + integrate skill master-bank + 5 quality gates self-check inline
5. `.claude/agents/newsroom-skeptic.md` + integrate skill skeptic
6. Test ticker VCB end-to-end: `/tin VCB` → bài 200-400 từ pass 5 quality gates

Exit criteria: 1 bài VCB đẹp xuất hiện ở `output/compare-feed/` + web auto-render đúng.

### Phase 5 — Iteration polish (1-2 ngày)
**Goal**: Xử lý edge cases user phát hiện qua test.

Tasks:
1. Run 6 ticker còn lại (TCB, MBB, ACB, BID, CTG, VPB) → fix data issues
2. Tune Web UI theo feedback
3. Bug fix: data null handling, fetch fail retry, ticker name fallback edge cases

Exit criteria: 7 ticker Bank đều ra bài pass 5 gates.

### Phase 6 — Notion publish (defer, optional)
**Goal**: Re-add Notion Compare Feed prepend.

Tasks:
1. Share Compare Feed page với `claude-mcp` integration ✓ (đã share rồi)
2. `lib/notion_publish.py` — prepend column_list block với column_left + column_right children
3. Add Step 7 vào pipeline: render markdown xong → publish Notion
4. Test: bài VCB mới ghi đè / prepend đúng vị trí trong Notion page

---

## 8.5. Data sourcing — KHÔNG restrict, web search fallback bắt buộc

**Nguyên tắc**: Agent (đặc biệt Master Bank, Story Editor, Skeptic) có nhu cầu data XYZ để viết bài → tra theo thứ tự ưu tiên, KHÔNG dừng nếu source đầu thiếu data.

**Thứ tự lookup recommend (Master Bank Bước 3-6)**:

1. **Finpath API** (`lib/finpath_api.py`) — BCTC, ratios, ownership, events. Verified public. Token-cheap.
2. **Local YAML curated** (`data/manual/*.yaml`) — Targets / Credit Room / NHNN circulars
3. **Local KB markdown** (`kb/bank/`) — frameworks, history, per-ticker analysis
4. **SQLite memory** (`data/pipeline.db generated_news`) — variety guard 3 bài cũ
5. **Web search fallback BẮT BUỘC** — nếu 1-4 thiếu data, agent MUST `WebSearch` / `WebFetch` để tìm số/sự kiện từ web

**Quy tắc**:
- ❌ KHÔNG `accepted_hypothesis: false` chỉ vì local sources thiếu data — phải thử web search trước
- ✅ Web search là first-class data source, không phải last-resort. Master có quyền dùng web search ngay khi nhận brief nếu hypothesis cần data ngoài Finpath/KB scope (vd "ý kiến CEO Q1/2026" — Finpath không có, web search source chính)
- ✅ Log `data_sources_used` trong row `generated_news` đầy đủ: `["Finpath_API/bankfinancialratios", "KB/Big4-vs-Tunhan", "WebSearch/cafef.vn-q1-2026-vcb"]`
- ✅ Pipeline log toggle ở Compare Feed phải show RÕ web search query/keywords/URL fetch — không hide
- ❌ Reject `accepted_hypothesis: false` CHỈ khi: data thật sự không tồn tại trên web (đã 3+ search query khác nhau không ra) HOẶC data conflict insight rõ ràng

**Ngữ cảnh**: nhiều Notion DB Bank trước đây cũng được fill bằng web search → thông tin manual curate. Migrate sang CLI không restrict — agent tự research như analyst thật.

**Implementation**: trong agent definition `.claude/agents/newsroom-master-bank.md`, allowed-tools phải có `WebSearch` + `WebFetch` cùng với Bash. Trong skill SKILL.md Bước 6 fallback path phải explicit "MUST web_search nếu local missing".

---

## 9. Quality gates V3.6 (inheritance từ skills)

Bài Master phải pass 5 gates trước khi persist (run trong agent self-check):

1. **0% từ tiếng Anh** trong content (kể cả viết tắt NPL/NIM/CASA/CAR/Basel/IRB/RWA/ESOP, kể cả thông dụng trade-off/anchor/momentum/defensive). Exception: tên riêng + Pipeline log internal.
2. **Word count 200-400 từ HARD CAP** body chính (mở đầu + bullet mechanism + Cần để ý + insight chốt). 401+ → reject + rewrite.
3. **Body 3-7 lý do mechanism**, mỗi lý do pass 3 test: (a) trả lời "vì sao", (b) có mechanism, (c) reader học cách thị trường vận hành. KHÔNG pad.
4. **"Cần để ý"** narrative ưu tiên (1 đoạn 50-100 từ với symbolic + lookforward + caveat ngược + data anchor + hàm ý). Exception: 2-3 bullet OK nếu caveat độc lập.
5. **No metadata leak** — không có "strategic-shift" / "risk_highlight" / "insight_type" / "Critique angle" trong bài đọc.

Heading hợp lệ DUY NHẤT: `## Cần để ý` (optional) + `## Góc nhìn ngược` (Skeptic). KHÔNG dùng "Key takeaway" / "Tóm lại" / "Tin chính".

---

## 10. CLAUDE.md (project-level instructions)

Project root sẽ có `CLAUDE.md` global với các rule:

- **Default Vietnamese** cho user-facing reply
- **Tiếng Việt thuần BẮT BUỘC** cho bài tin (5 quality gates trên)
- **No emoji** trừ khi user dùng trước
- **No BUY/SELL recommendation** (pháp lý)
- **No bịa số khi thiếu data** — Master có quyền `accepted_hypothesis: false`
- **Pipeline log THẬT** — không fabricate query/keyword/nguồn
- **Dedupe URL trước khi viết** (SQLite check)
- **Verify trước action lớn** (rename module, restructure, delete)
- **Mọi defer task** persist vào `data/manual/backlog.yaml` (sẽ tạo sau) hoặc spec doc — không note "chat sau làm tiếp"
- **Parallel work safe**: nhiều cửa sổ Claude Code OK miễn không cùng modify 1 SQLite row hoặc cùng skill file (Status board lock không cần vì SQLite có constraint)

---

## 11. Open questions / deferred decisions

| ID | Topic | Khi cần resolve | Default current |
|---|---|---|---|
| O1 | Live realtime quote endpoint path đúng | Phase 4 nếu Master cần giá realtime | Skip — quarterly đủ cho newsroom |
| O2 | KB Bank: source page lock | (resolved 2026-05-08) | Bank Sector hub `359273c7-a9a1-810f-9306-cb6227d9c94a` ✓ shared. Ingest start từ đây, traverse child pages + KB sub-page + Frameworks sub-page |
| O3 | KB re-ingest workflow khi user update Notion | Sau MVP | Manual rerun `python lib/kb_ingest.py --force`. Không cron auto-sync MVP. |
| O4 | Pipeline parallelization (đa ticker cùng lúc?) | Sau Phase 5 | Sequential single-ticker MVP |
| O5 | Backup SQLite (git lfs? sqlitedump?) | Phase 5+ | Schema track, content gitignore |
| O6 | Notion publish layout — column_list block syntax exact | Phase 6 | Defer, không block MVP |
| O7 | Replicate sang CK + BĐS (master-ck + master-bds) | Sau Bank ổn | Placeholder skill files |
| O8 | Add `npm run pipeline` Node script wrapper cho non-CC user? | Sau MVP | Defer |

---

## 12. Glossary

- **Compare Feed**: page Notion 2 cột (left = AI viết lại, right = raw + meta + funnel) — output cuối user đọc
- **Funnel batch**: `<TICKER>-<YYYYMMDD>-<HHMM>` — link tất cả candidates 1 pipeline run, dùng cho funnel rendering
- **Deep question**: câu hỏi đào sâu Story Editor giao Master, MUST thuộc 1/5 category (paradox/why_now/hidden_mechanism/comparison_deep/early_signal)
- **Angle label**: TÊN GỌI bài, free-text tiếng Việt thuần (vd "Đánh đổi chủ động — chuyển hướng chiến lược"), KHÔNG dùng enum
- **Insight type**: enum metadata internal (8 options) cho variety guard, KHÔNG leak vào content
- **Critique angle**: 1 of 6 góc Skeptic (data_skepticism / historical_analog / alt_interpretation / risk_highlight / insight_wrong / execution_unfaithful)
- **Universe**: 16 mã cổ phiếu hợp lệ (7 Bank + 5 CK + 4 BĐS). MVP scope = 7 Bank.
- **5 quality gates**: 5 rule cứng V3.6 (0% Anh, 200-400 từ, 3-7 mechanism, narrative caveat, no metadata leak)
- **Pass 1 fresh impression**: Skeptic đọc body Master ONLY, không xem insight — bias mitigation Option D hybrid

---

## 13. Acceptance criteria (definition of done MVP)

1. ✅ User gõ `/tin VCB` từ Claude Code CLI trong project root → pipeline chạy không lỗi end-to-end
2. ✅ File `output/compare-feed/VCB-<YYYYMMDD>-<HHMM>.md` tạo ra với frontmatter đầy đủ + 2 section
3. ✅ Web React `npm run dev` → localhost:5173 → IndexPage list bài → click → ArticlePage 2-column khớp screenshot Notion 1:1
4. ✅ Bài Master pass 5 quality gates V3.6 (0% Anh, ≤400 từ, 3-7 mechanism, narrative "Cần để ý", no metadata leak)
5. ✅ Skeptic critique 100-300 từ với 1 trong 6 angle, append đúng `## Góc nhìn ngược` section
6. ✅ Crawl funnel render đầy đủ: picked + rejected groups với link click ra được + reason ngắn
7. ✅ Pipeline log toggle render Step 1-6 actual data (không fabricate)
8. ✅ Test pass 7 ticker Bank universe (TCB/VCB/MBB/ACB/BID/CTG/VPB)
9. ✅ Notion publish DEFER — không trong MVP DoD

---

## 14. Next step

Sau khi user review spec này:
- Approve → invoke skill `superpowers:writing-plans` để break thành implementation plan có task atomic + checkpoint per Phase
- Request changes → cập nhật spec, re-review

Các file `.skill` đã extract sẵn ở `/tmp/skills-explore/finpath-newsroom-*/` — Phase 1 sẽ copy sang `.claude/skills/<name>/` (unzipped, plain dirs).
