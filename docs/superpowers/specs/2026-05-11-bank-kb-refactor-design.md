# Bank KB Refactor v2.0 — Design Spec

**Date:** 2026-05-11
**Author:** Claude (drafted via brainstorming với user @dangtrungicloud)
**Status:** Approved — proceeding to plan

## 1. Mục tiêu

Refactor Bank KB để parity với CK KB v1.2 pattern (pure static + Realtime data fetch guidance + auto-fallback protocol). Lý do:

- CK KB v1.2 bootstrap đã establish pattern tốt hơn: KB chứa kiến thức TĨNH (framework + threshold + case study), data động → Master fetch realtime qua Finpath API + web_search, pipeline log audit trail rõ.
- Bank KB hiện tại có:
  - Notion-coupled frontmatter (`notion_page_id`, `source_url`, `last_synced`) — không cần runtime, legacy from Notion bootstrap
  - Per-Q4/2025 anchor data (vd CASA per bank: "MBB 36.83%, TCB 34.48%") — sẽ stale
  - `targets.yaml` quarterly dynamic (kế hoạch ĐHĐCĐ + Q1/Q2/Q3/Q4 actuals) — Master nên fetch Finpath API + web_search
  - Master Bank SKILL.md không có `## Data fetching protocol — auto-fallback` explicit chain

Mục tiêu cuối: 2 sectors (Bank + CK) cùng pattern, easier add BĐS sau.

## 2. Scope

### In scope (deliverable)

- Refactor 4 markdown KB tại `kb/bank/frameworks/`:
  - Strip Notion frontmatter (giữ `category`, `title`, `last_updated`)
  - Replace per-Q4/2025 anchor data với benchmark ranges historical
  - Add `## Realtime data fetch guidance` section (Finpath API endpoints + web_search keywords)
  - Add `## Phần suy luận (cần verify)` section H2 riêng
  - Ensure `## Cross-link` section explicit per file
- Delete `data/manual/targets.yaml`
- Update `.claude/skills/finpath-newsroom-master-bank/SKILL.md`:
  - Update wording data source priority
  - Add `## Data fetching protocol — auto-fallback` section (parallel CK)
  - Update References section (remove targets.yaml)
- Update `.claude/agents/newsroom-master-bank.md`:
  - Drop `targets.yaml` load step
  - Ensure `data_trail` schema emit per V4.0
  - Wire fallback chain note vào workflow steps

### Out of scope (defer / không động)

- `lib/finpath_api.py` — already works, no change
- `lib/kb_loader.py` — already generic (accepts arbitrary root path)
- `kb/ck/` — just done v1.2, independent
- `data/manual/credit_room.yaml` + `nhnn_circulars.yaml` — semi-static + static, KEEP
- **End-to-end pipeline test** (`/tin TCB` E2E) — USER will run after handoff
- Tests automated — chỉ smoke check manual
- Notion linkage runtime restoration — KHÔNG (per CLAUDE.md, Notion only used 1-time bootstrap)

## 3. File layout (after refactor)

```
kb/bank/frameworks/
├── bank-industry-master-reference.md       # refactored — no Notion frontmatter, no Q4/2025 anchor
├── bank-nim-cycle.md                       # refactored — Q4/2025 CASA per bank → ranges
├── bank-npl-reading.md                     # refactored
└── bank-target-vs-actual-pattern.md        # refactored — content stays (framework cho ĐHĐCĐ pattern)

data/manual/
├── credit_room.yaml                        # KEEP (yearly semi-static)
├── nhnn_circulars.yaml                     # KEEP (static)
└── ssc_circulars.yaml                      # KEEP (CK, đã có)
# targets.yaml                              # DELETED

.claude/skills/finpath-newsroom-master-bank/
├── SKILL.md                                # UPDATED — auto-fallback section
└── references/                             # KEEP existing
    ├── kb-topics-bank.md
    ├── db-query-patterns.md
    └── master-pitfalls.md

.claude/agents/
└── newsroom-master-bank.md                 # UPDATED — drop targets.yaml + data_trail schema
```

## 4. Markdown refactor pattern (per file)

### Frontmatter — strip Notion fields

```yaml
# OLD
---
notion_page_id: "358273c7-a9a1-8153-addd-f609f1239daf"
source_url: "https://www.notion.so/358273c7a9a18153adddf609f1239daf"
last_synced: 2026-05-08T09:07:07.892478+00:00
category: frameworks
title: "Bank-NIM-cycle"
---

# NEW
---
category: frameworks
title: "Bank-NIM-cycle"
last_updated: 2026-05-11
---
```

### Body sections — apply v1.2 pattern

10 sections (parallel CK pattern):

1. **Khái niệm & cơ chế** — định nghĩa + cơ chế (giữ existing nội dung)
2. **Quy định pháp lý + threshold cứng** — NHNN circulars + Basel + LDR/CAR threshold
3. **Benchmark dài hạn (ranges)** — REPLACE per-Q4/2025 anchor (vd "MBB CASA 36.83%, TCB 34.48%, VCB 33.72%") với ranges historical:
   - Top tier CASA: 30-37%
   - Mid tier CASA: 20-25%
   - Low tier CASA: <15%
   - NIM range per bank type (high/mid/low) — ranges historical 2020-2026
4. **Case study lịch sử + chu kỳ** — GIỮ existing (TCB cycle 2022-2025, VPB FE Credit cycle, etc.)
5. **Bẫy khi đọc số** — GIỮ existing pitfalls
6. **5 câu hỏi cho Master agent** — ADD nếu missing (giống CK pattern)
7. **Realtime data fetch guidance** — NEW section, explicit:
   - **NIM/CASA/COF/NPL/LDR realtime per bank**: Finpath API `get_bank_ratios(ticker)` (work cho Bank ticker)
   - **BCTC quarter**: `get_income_statement(ticker)` + `get_balance_sheet(ticker)` + `get_full_income(ticker)`
   - **Deposit + credit growth**: `get_deposit_credit(ticker)`
   - **Bad debt detail**: `get_bad_debt(ticker)`
   - **NHNN room realtime nếu nới mid-year**: web_search "NHNN nới room [TICKER] [năm]"
   - **ĐHĐCĐ kế hoạch + actual quarter**: `get_events(ticker)` + web_search "[TICKER] nghị quyết ĐHĐCĐ [năm]"
   - **Sự kiện recent**: `get_news(ticker)` + web_search
8. **Cross-link** — relative path đến framework Bank khác + (optional) Master reference
9. **Source log** — web URLs + dates verified, KHÔNG Notion link
10. **Phần suy luận (cần verify)** — H2 riêng, extract inline notes

## 5. SKILL.md updates (`.claude/skills/finpath-newsroom-master-bank/SKILL.md`)

### (a) Update wording — clarify data source priority

Find existing wording về data sources, replace với:

> "Master Bank query data theo thứ tự: (1) local KB `kb/bank/frameworks/` cho framework + threshold + case study + pitfalls (kiến thức tĩnh); (2) `data/manual/credit_room.yaml` + `nhnn_circulars.yaml` cho semi-static data; (3) **Finpath API** cho BCTC + Bank ratios + events (`get_bank_ratios`, `get_income_statement`, `get_balance_sheet`, `get_deposit_credit`, `get_bad_debt`, `get_shareholders`, `get_events`, `get_news`, etc.); (4) **web_search** cho data Finpath API không có (ĐHĐCĐ kế hoạch + actual quarter, NHNN nới room mid-year, recent news/events)."

### (b) Add NEW section `## Data fetching protocol — auto-fallback`

```markdown
Khi viết bài, Master Bank PHẢI chain data sources theo thứ tự, KHÔNG skip. Pipeline log emit `data_trail` array per V4.0 schema:

### 1. Local KB (`kb/bank/frameworks/*.md`)
LUÔN query đầu để có framework + threshold + pitfall guidance. KB chỉ chứa kiến thức TĨNH (range historical, threshold cứng, case study). KHÔNG có per-bank per-quarter snapshot.

```python
from lib.kb_loader import KBLoader
loader = KBLoader('kb/bank/')
matches = loader.search([keyword1, keyword2])
content = loader.load_topic(matches[0]['path'])
```

4 file framework available:
- `bank-industry-master-reference.md` — anchor 6 lớp mental model
- `bank-nim-cycle.md` — chu kỳ NIM + CASA + loan mix
- `bank-npl-reading.md` — đọc nợ xấu thật vs reported + TPDN exposure
- `bank-target-vs-actual-pattern.md` — pattern ĐHĐCĐ kế hoạch vs actual

`data_trail[].source = "KB/<filename>"`

### 2. YAML semi-static
- `data/manual/credit_room.yaml` — NHNN room allocation per bank per năm
- `data/manual/nhnn_circulars.yaml` — quy định NHNN ảnh hưởng Bank sector

`data_trail[].source = "YAML/<filename>"`

### 3. Finpath API
Fetch realtime BCTC + Bank ratios + events:

```python
from lib.finpath_api import FinpathAPI
api = FinpathAPI()
# Bank-specific ratios
ratios = api.get_bank_ratios(ticker)             # NIM/CASA/COF/NPL/LDR/PE/PB/ROE
# BCTC
income = api.get_income_statement(ticker)
balance = api.get_balance_sheet(ticker)
full_income = api.get_full_income(ticker)
full_balance = api.get_full_balance_sheet(ticker)
cashflow = api.get_cashflow(ticker)
# Bank-specific items
nii = api.get_net_interest_income(ticker)
deposit_credit = api.get_deposit_credit(ticker)
bad_debt = api.get_bad_debt(ticker)
# Events + news
shareholders = api.get_shareholders(ticker)
events = api.get_events(ticker)
news = api.get_news(ticker)
```

`data_trail[].source = "Finpath_API/<endpoint_name>"` (vd `Finpath_API/bankfinancialratios`)

### 4. Web_search — fallback khi 1-3 thiếu

ESPECIALLY web_search cho:
- **ĐHĐCĐ kế hoạch năm + actual quarter**: keywords `"[TICKER] nghị quyết ĐHĐCĐ [năm]"`, `"[TICKER] kế hoạch lợi nhuận [năm]"`, `"[TICKER] kết quả Q[X]/[năm]"`
- **NHNN nới room mid-year** (case 28/8/2024): keywords `"NHNN nới room [TICKER] [năm]"`, `"NHNN cấp room đợt 2 [năm]"`
- **Tin tức recent về bank cụ thể**: keywords `"[TICKER] [topic] [date]"`
- **Sự kiện thị trường ảnh hưởng sector**: keywords `"ngành ngân hàng [topic] [date]"`

`data_trail[].source = "WebSearch/<sanitized-keyword>"`

### Reject rule

KHÔNG bịa số khi data không có. Sau cả 4 step (KB + YAML + Finpath API + web_search 3+ keywords khác nhau) vẫn không có data → reject với `master_decision: reject_no_data` + `data_trail` ghi rõ search attempts (transparency).
```

### (c) Update References section

Find `## References` (or equivalent), update KB Bank file list (remove `targets.yaml` reference, ensure 4 KB markdown links present):

```markdown
- `kb/bank/frameworks/bank-industry-master-reference.md` — 6 lớp mental model anchor
- `kb/bank/frameworks/bank-nim-cycle.md` — chu kỳ NIM + CASA + loan mix
- `kb/bank/frameworks/bank-npl-reading.md` — đọc nợ xấu thật vs reported
- `kb/bank/frameworks/bank-target-vs-actual-pattern.md` — pattern ĐHĐCĐ
- `data/manual/credit_room.yaml` — NHNN room allocation
- `data/manual/nhnn_circulars.yaml` — regulatory archive
```

## 6. Agent file update (`.claude/agents/newsroom-master-bank.md`)

### (a) Drop `targets.yaml` load step

Find Step 5 (or equivalent) loading 3 YAML, remove targets:

```python
# OLD
import yaml
with open('data/manual/targets.yaml') as f: targets = yaml.safe_load(f)
with open('data/manual/credit_room.yaml') as f: credit_room = yaml.safe_load(f)
with open('data/manual/nhnn_circulars.yaml') as f: circulars = yaml.safe_load(f)

# NEW
import yaml
with open('data/manual/credit_room.yaml') as f: credit_room = yaml.safe_load(f)
with open('data/manual/nhnn_circulars.yaml') as f: circulars = yaml.safe_load(f)
# targets.yaml dropped — Master fetch ĐHĐCĐ + actual via Finpath API get_events + web_search
```

### (b) Add note ở workflow

In Step 3 (Query Finpath API), add comment about ĐHĐCĐ:

```python
# Step 3: Query Finpath API
events = api.get_events(ticker)  # Includes ĐHĐCĐ events (replaces old targets.yaml lookup)
# For actual quarter results: parse income_statement + ratios above
# For ĐHĐCĐ kế hoạch năm chi tiết: web_search "[TICKER] nghị quyết ĐHĐCĐ [năm]"
```

### (c) Ensure `data_trail` schema emit (already in V4.0)

Verify Step 8 (or equivalent — Persist row) emits `data_trail` array per V4.0 schema. Per existing agent file: "MUST emit `data_trail` array of {source, fetched, purpose, supports_argument}". No change needed if already emit — just ensure refactor doesn't accidentally remove it.

## 7. Implementation order

Atomic commits, easy revert per file:

1. **Commit 1 — Spec + plan** (this design + plan)
2. **Commit 2 — Refactor `bank-nim-cycle.md`** (most anchor data, hardest first)
3. **Commit 3 — Refactor `bank-npl-reading.md`**
4. **Commit 4 — Refactor `bank-target-vs-actual-pattern.md`**
5. **Commit 5 — Refactor `bank-industry-master-reference.md`** (last — cross-link 3 deep dives)
6. **Commit 6 — Delete `targets.yaml`**
7. **Commit 7 — Update Master Bank SKILL.md** (auto-fallback section)
8. **Commit 8 — Update agent file `newsroom-master-bank.md`** (drop targets.yaml load + workflow note)
9. **Commit 9 — Cross-file numerical consistency check + reconcile if needed**

Each commit message follow project convention (concise Vietnamese, why-focused).

## 8. Validation (smoke only — STOP before E2E)

### KB Bank load smoke
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.kb_loader import KBLoader
loader = KBLoader('kb/bank/')
print('FILES:', len(loader._all_files()))
for kw in ['NIM', 'CASA', 'NPL', 'Basel', 'target', 'room', '6 lớp']:
    matches = [r['title'] for r in loader.search([kw])]
    print(f'  search [{kw}]: {matches}')
"
```

Expected: 4 files, mỗi keyword có match.

### Pure-static check (no per-Q4/2025 anchor)
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -rn "Q4/2025\|MBB 36.83\|TCB 34.48\|VCB 33.72" kb/bank/ | grep -v "verified\|http\|case study\|Bank-NIM-cycle"
```

Expected: ≤5 hits (chỉ trong source URLs verified date / case study labels).

### YAML structure
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && ls data/manual/
# Expected: credit_room.yaml + nhnn_circulars.yaml + ssc_circulars.yaml
# NOT: targets.yaml
```

### SKILL.md auto-fallback section
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -c "Data fetching protocol — auto-fallback" .claude/skills/finpath-newsroom-master-bank/SKILL.md
# Expected: 1
```

### Agent file no longer references targets.yaml
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -c "targets.yaml" .claude/agents/newsroom-master-bank.md
# Expected: 0
```

### Frontmatter Notion-free
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -c "notion_page_id\|last_synced" kb/bank/frameworks/*.md
# Expected: 0 (all 4 files)
```

## 9. Hand-off to user

After all 9 commits + smoke checks pass, hand off với message:

> "Bank KB refactor v2.0 done. Smoke checks pass. Run `/tin TCB` để E2E test (đảm bảo Master Bank skill query KB + Finpath API + web_search OK + article pass 5 quality gates V4.0). Nếu có regression → fix forward; nếu OK → ship."

User tự run E2E. Kết quả `/tin TCB` cho biết refactor có break Master Bank không.

## 10. Risk + rollback

- **Risk**: Master Bank skill V4.0 break do refactor → article quality regress hoặc Master fail to find data → reject_no_data spike.
- **Rollback path**: `git revert <commit-range>` đưa về Bank KB v1.0 (Notion-coupled). Spec/plan committed riêng → revert KB không ảnh hưởng spec.
- **Mitigation**:
  - Atomic commit per file → revert chỉ 1 file nếu issue isolated
  - Smoke checks pass = baseline confidence
  - User E2E test = real-world validation
  - Drop only `targets.yaml` (most dynamic) → keep `credit_room` + `nhnn_circulars` (low risk)

## 11. Open questions / followup

- **Bank-target-vs-actual-pattern.md** — File name có "target" → có nên rename thành `bank-dhdcd-pattern.md`? Hoặc giữ nguyên (existing file)? **Decision: keep filename** (low value rename + risk break existing references).
- **Validation patterns trong KB Bank** — Nếu có bank-specific patterns như "data_trail emit" trong existing references/ folder, cần verify intact.
- **Notion bootstrap scripts** (`lib/kb_ingest.py`, `lib/notion_fetch.py`) — Bank-specific, KHÔNG touch (Bank đã bootstrap xong, scripts là legacy archive).

## Changelog

- **v2.0 (2026-05-11):** Initial spec — refactor Bank KB to parity với CK v1.2 (pure static + Realtime data fetch guidance + auto-fallback protocol). Drop `targets.yaml` (dynamic). Master Bank V4.0 production — refactor follow đường safe (smoke check + handoff E2E user).
