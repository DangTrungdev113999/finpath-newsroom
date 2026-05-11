# Bank KB Refactor v2.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor Bank KB (4 markdown + drop targets.yaml) + Master Bank SKILL.md + agent file để parity với CK v1.2 pure-static pattern + auto-fallback protocol.

**Architecture:** Strip Notion frontmatter từ 4 KB markdown, replace per-Q4/2025 anchor data với benchmark ranges historical, add Realtime data fetch guidance + Phần suy luận sections per CK v1.2 pattern. Drop `targets.yaml` (Master fetch ĐHĐCĐ + actual via Finpath API + web_search). Update Master Bank SKILL.md add `## Data fetching protocol — auto-fallback` section.

**Tech Stack:** Python 3 / `lib/kb_loader.py` / `lib/finpath_api.py` / PyYAML / Markdown.

**Spec:** `docs/superpowers/specs/2026-05-11-bank-kb-refactor-design.md`

---

## File Structure

**Will modify (6 file):**

```
kb/bank/frameworks/
├── bank-nim-cycle.md                       # Task 1
├── bank-npl-reading.md                     # Task 2
├── bank-target-vs-actual-pattern.md        # Task 3
└── bank-industry-master-reference.md       # Task 4 (last — cross-link 3 deep dives)

.claude/skills/finpath-newsroom-master-bank/
└── SKILL.md                                # Task 6

.claude/agents/
└── newsroom-master-bank.md                 # Task 7
```

**Will delete (1 file):**

```
data/manual/targets.yaml                    # Task 5
```

**Will NOT touch:**
- `lib/finpath_api.py` / `lib/kb_loader.py` — generic, work for both Bank + CK
- `data/manual/credit_room.yaml` + `nhnn_circulars.yaml` + `ssc_circulars.yaml` — keep
- `kb/ck/` — independent, just done v1.2
- `.claude/skills/finpath-newsroom-master-bank/references/` — keep existing
- `lib/kb_ingest.py` / `lib/notion_fetch.py` — Bank bootstrap done, leave alone

---

## Common refactor pattern (apply to Tasks 1-4)

Each markdown file refactor:

**Frontmatter:**

```yaml
# OLD (3 Notion lines to strip)
---
notion_page_id: "<uuid>"
source_url: "https://www.notion.so/..."
last_synced: 2026-05-08T...
category: frameworks
title: "Bank-<Name>"
---

# NEW
---
category: frameworks
title: "Bank-<Name>"
last_updated: 2026-05-11
---
```

**Body — keep existing nội dung, apply 3 modifications:**

1. **Replace** any "Q4/2025 anchor data" sections (per-bank quarterly snapshot tables) với "Benchmark dài hạn (ranges)" — historical ranges KHÔNG per-quarter.
2. **Add** new section `## Realtime data fetch guidance (cho Master Bank)` — explicit Finpath API endpoints + web_search keywords cho từng data type relevant đến file framework đó.
3. **Ensure** sections present (add nếu missing): `## 5 câu hỏi cho Master agent`, `## Cross-link`, `## Phần suy luận (cần verify)` (H2 riêng — extract inline notes nếu có).

**KEEP intact:**
- Khái niệm & cơ chế / công thức definitions
- Quy định pháp lý (Basel, NHNN circulars)
- Case study lịch sử + chu kỳ
- Bẫy / pitfalls
- Source log (URLs)

---

## Task 1: Refactor `bank-nim-cycle.md`

**Files:**
- Modify: `kb/bank/frameworks/bank-nim-cycle.md`

- [ ] **Step 1: Read full current file**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cat kb/bank/frameworks/bank-nim-cycle.md
```

Memorize: Notion frontmatter (3 lines) + section "2. Profile NIM theo bank type (Q4/2025 reference)" line 28+ + section "3. CASA — driver số 1 ở VN" with Q4/2025 per-bank breakdown line 35+.

- [ ] **Step 2: Strip Notion frontmatter**

Use Edit tool. Replace:
```yaml
---
notion_page_id: "358273c7-a9a1-8153-addd-f609f1239daf"
source_url: "https://www.notion.so/358273c7a9a18153adddf609f1239daf"
last_synced: 2026-05-08T09:07:07.892478+00:00
category: frameworks
title: "Bank-NIM-cycle"
---
```

With:
```yaml
---
category: frameworks
title: "Bank-NIM-cycle"
last_updated: 2026-05-11
---
```

- [ ] **Step 3: Replace per-Q4/2025 anchor sections với benchmark ranges**

Find section "### 2. Profile NIM theo bank type (Q4/2025 reference)" + section "### 3. CASA — driver số 1 ở VN" (Q4/2025 per-bank breakdown).

Replace với new section "## Benchmark dài hạn + ranges (NIM/CASA per bank type)":

```markdown
## Benchmark dài hạn + ranges (NIM/CASA per bank type)

KHÔNG per-bank per-quarter snapshot. Dùng cho Master sanity-check khi Finpath API trả số realtime.

### NIM range theo bank type (historical 2020-2026)

| Tier | NIM range | Bank typical |
|---|---|---|
| **High** | >4% | Tư nhân consumer-finance heavy (VPB), tư nhân retail-strong (TCB, MBB, VIB) |
| **Mid** | 3-4% | Tư nhân corporate (ACB, STB, HDB) |
| **Low stable** | ~3% | Quốc doanh (VCB, CTG, BID) — cho vay corporate yield thấp do chính sách ngành |

Trend dài hạn 2011-2025: NIM bình quân 27 NH giảm từ 3,88% → 2,93% (secular compression).

### CASA range theo bank type

| Tier | CASA range | Bank typical |
|---|---|---|
| **Top** | 30-37% | MBB, TCB, VCB |
| **Mid** | 18-25% | CTG, ACB, BID, TPB |
| **Low** | <15% | STB, VIB, VPB, HDB, SHB |

**KEY INSIGHT**: CASA cao ≠ NIM cao tự động. Phụ thuộc loan mix (corporate yield thấp vs retail/SME yield cao).

### Loan yield range theo segment

| Segment | Yield range |
|---|---|
| Retail / consumer finance | 12-20%/năm |
| SME | 9-12%/năm |
| Corporate big | 7-9%/năm |
| DNNN / state-led project | 5-7%/năm |

**Decision rule**: NIM expansion thực chất từ shift mix sang retail/SME — KHÔNG phải chỉ repricing chu kỳ.
```

- [ ] **Step 4: Add `## Realtime data fetch guidance (cho Master Bank)` section**

Insert TRƯỚC section "## Cross-link" (hoặc trước "## Source log" nếu Cross-link chưa có):

```markdown
## Realtime data fetch guidance (cho Master Bank)

Khi viết bài quý cụ thể về NIM/CASA, Master KHÔNG đọc số từ KB. Phải fetch realtime:

- **NIM/CASA/COF/NPL/LDR realtime per bank**: Finpath API `get_bank_ratios(ticker)` — endpoint `/api/stocks/bankfinancialratios/{ticker}` trả NIM/CASA/COF/NPL/LDR/PE/PB/ROE quarterly + yearly.
- **NIM trend nhiều quý**: parse `quarterlyProfits` từ `get_bank_ratios` (trả 8+ quarters).
- **NIM batch nhiều bank cùng lúc**: `get_bank_ratios_batch(['VCB', 'TCB', 'MBB'])` cho competitive comparison.
- **Net interest income breakdown**: `get_net_interest_income(ticker)`.
- **Loan + deposit growth**: `get_deposit_credit(ticker)` — credit growth + deposit composition (CASA breakdown).
- **Lãi suất điều hành NHNN realtime**: web_search "NHNN lãi suất tái cấp vốn [date]" hoặc "lãi suất điều hành NHNN [năm]".
- **CASA peer comparison toàn ngành quarter**: web_search "CASA Q[X]/[Y] toàn ngành" hoặc "top 10 ngân hàng CASA quý [X]".

Pipeline log: `data_trail[].source = "Finpath_API/bankfinancialratios"` hoặc `"WebSearch/<keyword>"`.
```

- [ ] **Step 5: Ensure `## Cross-link` section present**

Find existing Cross-link section. If exists, KEEP. If missing, add BEFORE Source log:

```markdown
## Cross-link

- [bank-npl-reading.md](./bank-npl-reading.md) — NIM compress mạnh có thể che dấu nợ xấu tăng (giảm trích lập để giữ lợi nhuận).
- [bank-target-vs-actual-pattern.md](./bank-target-vs-actual-pattern.md) — Bank đặt target NIM cao hơn historical = pre-bid kỳ vọng repricing thuận lợi → hợp lý hay aggressive?
- [bank-industry-master-reference.md](./bank-industry-master-reference.md) — Lớp 3 chu kỳ lãi suất NHNN ↔ NIM phase analysis.
```

- [ ] **Step 6: Ensure `## Phần suy luận (cần verify)` section H2 riêng**

If existing inline notes về suy luận, extract thành H2 riêng AFTER Source log. Format:

```markdown
## Phần suy luận (cần verify)

- [Inference 1 — bullet point with caveat]
- [Inference 2]
```

- [ ] **Step 7: Smoke check loadable + frontmatter clean**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && head -5 kb/bank/frameworks/bank-nim-cycle.md && echo "---" && grep -c "notion_page_id\|last_synced" kb/bank/frameworks/bank-nim-cycle.md
```

Expected: frontmatter 5 lines (no notion_page_id/last_synced), grep returns `0`.

- [ ] **Step 8: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add kb/bank/frameworks/bank-nim-cycle.md && git commit -m "kb(bank): refactor NIM cycle to pure static (v2.0 parity CK)

- Strip Notion frontmatter (notion_page_id/source_url/last_synced)
- Replace Q4/2025 per-bank CASA/NIM anchor với benchmark ranges
  historical (top/mid/low tier) + loan yield per segment ranges
- Add ## Realtime data fetch guidance section (Finpath API
  get_bank_ratios endpoint + web_search keywords)
- Ensure Cross-link + Phần suy luận sections present

Spec: docs/superpowers/specs/2026-05-11-bank-kb-refactor-design.md"
```

---

## Task 2: Refactor `bank-npl-reading.md`

**Files:**
- Modify: `kb/bank/frameworks/bank-npl-reading.md`

- [ ] **Step 1: Read full current file**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cat kb/bank/frameworks/bank-npl-reading.md
```

Identify: Notion frontmatter (3 lines) + any per-bank Q4/2025 NPL/coverage ratio snapshot sections.

- [ ] **Step 2: Strip Notion frontmatter**

Replace top frontmatter (5-6 line block ending `---`) với clean version:
```yaml
---
category: frameworks
title: "Bank-NPL-reading"
last_updated: 2026-05-11
---
```

- [ ] **Step 3: Replace per-bank Q4/2025 NPL anchor (nếu có) với benchmark ranges**

Find any sections containing per-bank NPL Q4/2025 numbers (vd "VCB NPL 0.96%, MBB 1.41%", etc.). Replace với new section "## Benchmark dài hạn + ranges (NPL + coverage + nợ xấu thật)":

```markdown
## Benchmark dài hạn + ranges (NPL + coverage + nợ xấu thật)

KHÔNG per-bank per-quarter snapshot. Dùng cho Master sanity-check khi Finpath API trả số realtime.

### NPL reported range (historical 2020-2026)

| Tier | NPL reported | Bank typical |
|---|---|---|
| **Low risk** | <1% | Quốc doanh (VCB, BID, CTG) — cho vay corporate được bảo lãnh chính sách |
| **Mid** | 1-2% | Tư nhân lớn quản lý risk tốt (TCB, MBB, ACB) |
| **High** | 2-3% | Tư nhân consumer/SME-heavy (VPB, HDB) — cho vay segment yield cao + risk cao |

### Coverage ratio (LLR — Loan Loss Reserve / NPL) range

| Tier | Coverage ratio | Bank typical |
|---|---|---|
| **Conservative** | >200% | Quốc doanh + tư nhân top conservative (VCB, MBB, ACB) — over-reserved |
| **Adequate** | 100-200% | Tư nhân healthy (TCB, HDB) |
| **Stressed** | <100% | Bank đang stress (VPB FE Credit cycle 2022-2024) |

### Nợ xấu thật vs reported công thức

```
Nợ xấu thật = NPL reported + Nợ tái cơ cấu + Trái phiếu VAMC + TPDN BĐS exposure
```

VD historical: NPL 1.5% reported + Tái cơ cấu 2.0% + VAMC 0.5% = Nợ xấu thật ~4.0%.

### Threshold cảnh báo

- **Coverage <100%**: bank under-reserved, risk khi NPL spike
- **Nợ xấu thật > 5%**: bank trong stress mode, cần quan sát quarterly
- **NPL spike >50% YoY**: bank flag risk lớn (vd VPB FE Credit 2022 spike consumer NPL)
```

- [ ] **Step 4: Add `## Realtime data fetch guidance` section**

Insert trước Cross-link:

```markdown
## Realtime data fetch guidance (cho Master Bank)

Khi viết bài quý cụ thể về NPL, Master KHÔNG đọc số từ KB. Phải fetch realtime:

- **NPL realtime per bank**: Finpath API `get_bank_ratios(ticker)` → field NPL trong response.
- **Bad debt detail**: `get_bad_debt(ticker)` — endpoint `/api/stocks/baddebt/{ticker}` — phân nhóm 3-5 + tái cơ cấu + VAMC.
- **Coverage ratio (LLR)**: parse từ `get_bank_ratios` (nếu có) hoặc tính từ `get_balance_sheet` (Loan Loss Reserve / Total NPL).
- **TPDN exposure ẩn**: `get_balance_sheet(ticker)` → "Tài sản tài chính sẵn sàng để bán" hoặc thuyết minh BCTC chi tiết. Web_search bổ sung "[TICKER] TPDN exposure BCTC Q[X]/[Y]".
- **Nợ tái cơ cấu** (TT 02/2023 / TT 53/2024): web_search "[TICKER] nợ tái cơ cấu Q[X]/[Y]" hoặc thuyết minh BCTC.
- **NHNN circular impact recent**: query `data/manual/nhnn_circulars.yaml` first, web_search bổ sung nếu cần.

Pipeline log: `data_trail[].source = "Finpath_API/bankfinancialratios"` / `"Finpath_API/baddebt"` / `"YAML/nhnn_circulars.yaml"` / `"WebSearch/<keyword>"`.
```

- [ ] **Step 5: Ensure Cross-link + Phần suy luận sections present**

Add nếu missing (parallel Task 1 Step 5-6 pattern). Cross-link suggestions:

```markdown
## Cross-link

- [bank-nim-cycle.md](./bank-nim-cycle.md) — Bank NIM compress mạnh có thể đi đôi với giảm trích lập (move risk to balance sheet) — coverage ratio drop là tín hiệu sớm.
- [bank-target-vs-actual-pattern.md](./bank-target-vs-actual-pattern.md) — Bank đặt target NPL thấp hơn historical → có realistic không? Cần verify với credit growth target.
- [bank-industry-master-reference.md](./bank-industry-master-reference.md) — Lớp 2 đọc số (Tier 1: NPL + coverage), Lớp 6 case study TPDN crisis 2022.
```

- [ ] **Step 6: Smoke check + commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -c "notion_page_id\|last_synced" kb/bank/frameworks/bank-npl-reading.md && git add kb/bank/frameworks/bank-npl-reading.md && git commit -m "kb(bank): refactor NPL reading to pure static (v2.0 parity CK)

- Strip Notion frontmatter
- Replace per-bank Q4/2025 NPL/coverage anchor với benchmark ranges
  historical (low/mid/high risk tier + coverage tier)
- Add ## Realtime data fetch guidance (Finpath API get_bad_debt +
  get_bank_ratios + web_search TPDN exposure keywords)
- Ensure Cross-link + Phần suy luận sections

Spec: docs/superpowers/specs/2026-05-11-bank-kb-refactor-design.md"
```

Expected smoke check: `0`.

---

## Task 3: Refactor `bank-target-vs-actual-pattern.md`

**Files:**
- Modify: `kb/bank/frameworks/bank-target-vs-actual-pattern.md`

- [ ] **Step 1: Read full current file**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cat kb/bank/frameworks/bank-target-vs-actual-pattern.md
```

This file content = framework cho Master analyze ĐHĐCĐ kế hoạch vs actual quarter pattern. Đặc biệt critical vì Task 5 sẽ delete `targets.yaml` — nội dung framework này hướng dẫn Master fetch realtime thay thế.

- [ ] **Step 2: Strip Notion frontmatter**

Replace với:
```yaml
---
category: frameworks
title: "Bank-Target-vs-Actual-pattern"
last_updated: 2026-05-11
---
```

- [ ] **Step 3: Replace any per-bank target/actual snapshot với benchmark patterns**

If file có sections per-bank target Q1/Q2 numbers (specific bank kế hoạch năm + actual), replace với generic patterns:

```markdown
## Benchmark dài hạn + patterns

KHÔNG per-bank specific year numbers. Pattern phân loại bank by ĐHĐCĐ posture:

### Pattern phân loại bank theo ĐHĐCĐ posture

| Posture | Đặc trưng kế hoạch | Bank typical |
|---|---|---|
| **Conservative** | LNTT growth ≤ 10% YoY, credit growth ≤ room cấp đầu năm | Quốc doanh (VCB, BID, CTG) — đảm bảo deliver, ít upside |
| **Realistic** | LNTT growth 10-25%, credit growth ≤ room | Tư nhân healthy (TCB, ACB, MBB) — match với historical capability |
| **Aggressive** | LNTT growth >25%, credit growth = room đầu năm hoặc target nâng room mid-year | Tư nhân ambition (VPB, HDB, TPB) — pre-bid expectations |

### Pattern Q1 actual vs annual target (% completion benchmarks)

- **On track**: Q1 đạt 22-28% kế hoạch năm (proportional 25%/quý)
- **Ahead of pace**: Q1 >28% — credit/NIM expansion tốt → có thể beat
- **Behind pace**: Q1 <22% — chậm tiến độ, Q2-Q4 cần catch-up
- **Severely behind**: Q1 <15% — risk miss target, watch Q2 announcement

### Decision rule khi viết bài

- Q1 % kế hoạch + delta vs cùng kỳ năm trước = sentiment (positive/neutral/concerning)
- So sánh với peer bank cùng tier để contextualize
- Nếu bank nâng room mid-year → revise % completion calculation
```

- [ ] **Step 4: Add `## Realtime data fetch guidance` (CRITICAL — replace targets.yaml)**

Insert section explicit để Master biết KHÔNG dùng targets.yaml nữa:

```markdown
## Realtime data fetch guidance (cho Master Bank — REPLACES dropped targets.yaml)

`targets.yaml` ĐÃ BỊ DROP per refactor v2.0 (dynamic data, stale theo quý). Master fetch realtime:

- **ĐHĐCĐ kế hoạch năm (LNTT + credit growth target)**: Finpath API `get_events(ticker)` → filter event type "ĐHĐCĐ" hoặc "Annual General Meeting", lấy summary + attachments. Bổ sung: web_search "[TICKER] nghị quyết ĐHĐCĐ [năm]" → top hit thường là cafef.vn hoặc website bank chính thức.
- **Actual Q[X] LNTT + credit growth**: parse từ Finpath API `get_income_statement(ticker)` (LNTT) + `get_deposit_credit(ticker)` (credit growth quarter).
- **% kế hoạch completion**: tính bằng (actual_lntt_q[x] / target_lntt_year). Master tự compute từ 2 nguồn trên.
- **NHNN nới room mid-year** (case 28/8/2024 TCB/ACB/HDB): web_search "NHNN nới room [TICKER] [năm]" hoặc "NHNN cấp room đợt 2 [năm]".

Pipeline log: `data_trail[].source = "Finpath_API/events"` / `"Finpath_API/incomes"` / `"WebSearch/<keyword>"`.

**KHÔNG**: load `data/manual/targets.yaml` — file ĐÃ DELETED.
```

- [ ] **Step 5: Ensure Cross-link + Phần suy luận**

Add Cross-link nếu missing:

```markdown
## Cross-link

- [bank-nim-cycle.md](./bank-nim-cycle.md) — Bank target NIM aggressive → có realistic không cycle lãi suất hiện tại?
- [bank-npl-reading.md](./bank-npl-reading.md) — Bank target credit growth high + NPL low đồng thời → có sustainable không?
- [bank-industry-master-reference.md](./bank-industry-master-reference.md) — Lớp 1.3.bis NHNN room logic + Lớp 5.5.bis P/B trap state-owned (Big4 conservative posture).
```

- [ ] **Step 6: Smoke check + commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -c "notion_page_id\|last_synced" kb/bank/frameworks/bank-target-vs-actual-pattern.md && git add kb/bank/frameworks/bank-target-vs-actual-pattern.md && git commit -m "kb(bank): refactor target-vs-actual to pure static (v2.0)

- Strip Notion frontmatter
- Replace per-bank target snapshot với pattern phân loại
  (conservative/realistic/aggressive posture)
- Q1 % completion benchmarks (on-track/ahead/behind/severe)
- Add ## Realtime data fetch guidance — explicit hướng dẫn fetch
  ĐHĐCĐ + actual quarter via Finpath API + web_search (REPLACES
  dropped targets.yaml)
- Cross-link + Phần suy luận sections

Spec: docs/superpowers/specs/2026-05-11-bank-kb-refactor-design.md"
```

Expected: `0`.

---

## Task 4: Refactor `bank-industry-master-reference.md`

**Files:**
- Modify: `kb/bank/frameworks/bank-industry-master-reference.md`

- [ ] **Step 1: Read full current file**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cat kb/bank/frameworks/bank-industry-master-reference.md
```

Identify: Notion frontmatter (3 lines) + any per-bank Q4/2025 anchor data scattered (CASA/NIM specific numbers per bank trong Lớp 1.2 / 2.1 / 5.5).

- [ ] **Step 2: Strip Notion frontmatter**

Replace với:
```yaml
---
category: frameworks
title: "Bank-Industry-Master-Reference"
last_updated: 2026-05-11
---
```

- [ ] **Step 3: Replace per-Q4/2025 anchor data inline với ranges**

Scan toàn bộ file, find any per-bank specific numbers Q4/2025 (vd "MBB 36.83%, TCB 34.48%" trong Lớp 1.2 hoặc Lớp 2). Replace với ranges (vd "Top tier 30-37%").

Specifically check:
- Lớp 1.2 "Phân loại ngân hàng" — keep classification structural, remove per-bank Q4/2025 NIM/CASA numbers
- Lớp 2.1 metrics tier 1/2/3 — keep tier definitions, remove specific Q4/2025 benchmarks
- Lớp 5 định giá — keep P/B vs P/E framework, remove specific P/B numbers per bank

Pattern: per-bank STRUCTURAL positioning OK (vd "MBB = tech bank positioning"), per-quarter quantitative numbers REMOVE.

- [ ] **Step 4: Add `## Hướng dẫn tra dữ liệu thời gian thực` section** (parallel CK master ref)

Insert section sau Lớp 6 case study, trước Cross-link:

```markdown
## Hướng dẫn tra dữ liệu thời gian thực (cho Master Bank)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quarter cụ thể, Master phải:

1. **Query KB framework** (file này + 3 deep dive: NIM-cycle, NPL-reading, Target-vs-Actual) — static guidance.
2. **Query YAML** (`data/manual/credit_room.yaml` + `nhnn_circulars.yaml`) — semi-static + regulatory archive.
3. **Finpath API** cho data realtime:
   - `get_bank_ratios(ticker)` — NIM/CASA/COF/NPL/LDR/PE/PB/ROE quarterly + yearly
   - `get_bank_ratios_batch([t1,t2,t3])` — competitive comparison
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quarter
   - `get_deposit_credit(ticker)` — credit growth + deposit composition
   - `get_bad_debt(ticker)` — NPL detail nhóm 3-5 + tái cơ cấu + VAMC
   - `get_net_interest_income(ticker)` — NII breakdown
   - `get_shareholders(ticker)` + `get_events(ticker)` + `get_news(ticker)` — ownership + ĐHĐCĐ + tin
4. **Web_search** cho data Finpath API không có:
   - ĐHĐCĐ kế hoạch chi tiết + actual quarter (parse từ income_statement + ratios)
   - NHNN nới room mid-year (case 28/8/2024)
   - Recent regulatory updates (TT mới NHNN)
   - Sự kiện thị trường ảnh hưởng sector

Pipeline log V4.0 emit `data_trail` array: `{source, fetched, purpose, supports_argument}` per fact. KHÔNG bịa số.
```

- [ ] **Step 5: Update Cross-link section**

Find existing Cross-link (or add). Ensure 3 deep dive cross-link explicit:

```markdown
## Cross-link

| Deep dive | Nội dung chính |
|---|---|
| [`bank-nim-cycle.md`](./bank-nim-cycle.md) | Chu kỳ NIM + CASA + loan mix; phase repricing lãi suất NHNN |
| [`bank-npl-reading.md`](./bank-npl-reading.md) | Đọc nợ xấu thật vs reported (NPL + tái cơ cấu + VAMC + TPDN); coverage ratio threshold |
| [`bank-target-vs-actual-pattern.md`](./bank-target-vs-actual-pattern.md) | Pattern ĐHĐCĐ posture (conservative/realistic/aggressive) + Q1 % completion benchmark |
```

- [ ] **Step 6: Ensure Phần suy luận tách H2**

If existing inline notes về suy luận, extract H2 riêng AFTER Source log.

- [ ] **Step 7: Smoke check + commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -c "notion_page_id\|last_synced" kb/bank/frameworks/bank-industry-master-reference.md && grep -c "MBB 36.83\|TCB 34.48\|VCB 33.72" kb/bank/frameworks/bank-industry-master-reference.md && git add kb/bank/frameworks/bank-industry-master-reference.md && git commit -m "kb(bank): refactor master reference to pure static (v2.0)

- Strip Notion frontmatter
- Remove per-bank Q4/2025 specific numbers (CASA/NIM benchmarks),
  keep structural positioning per bank
- Add ## Hướng dẫn tra dữ liệu thời gian thực section (parallel CK
  master ref) — explicit 4-step chain (KB → YAML → Finpath API →
  web_search) with all 13 endpoints listed
- Update Cross-link table với 3 deep dive
- Phần suy luận H2 riêng

Spec: docs/superpowers/specs/2026-05-11-bank-kb-refactor-design.md"
```

Expected: `0` for both grep checks.

---

## Task 5: Delete `targets.yaml`

**Files:**
- Delete: `data/manual/targets.yaml`

- [ ] **Step 1: Verify `targets.yaml` exists + content (final backup mental note)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && ls data/manual/targets.yaml && cat data/manual/targets.yaml | head -10
```

Expected: file exists with 4 ticker rows (VCB/TCB/MBB/ACB).

- [ ] **Step 2: Delete file**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git rm data/manual/targets.yaml
```

- [ ] **Step 3: Verify deletion**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && ls data/manual/targets.yaml 2>&1
```

Expected: `ls: data/manual/targets.yaml: No such file or directory`.

- [ ] **Step 4: Verify remaining YAMLs**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && ls data/manual/
```

Expected: `credit_room.yaml`, `nhnn_circulars.yaml`, `ssc_circulars.yaml` (3 files).

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git commit -m "data(bank): drop targets.yaml — Master fetch ĐHĐCĐ realtime

targets.yaml chứa kế hoạch ĐHĐCĐ + actual quarter per bank — DYNAMIC
data, stale theo quý. Per refactor v2.0 (parity với CK pivot v1.2),
KB chỉ giữ kiến thức tĩnh; data động Master fetch realtime qua:
- Finpath API get_events(ticker) cho ĐHĐCĐ
- Finpath API get_income_statement(ticker) cho actual quarter
- web_search bổ sung cho keyword 'nghị quyết ĐHĐCĐ' + actual quarter

Hướng dẫn explicit trong kb/bank/frameworks/bank-target-vs-actual-pattern.md
section 'Realtime data fetch guidance' (Task 3).

Master Bank skill + agent file update sẽ remove load step (Task 6+7).

Spec: docs/superpowers/specs/2026-05-11-bank-kb-refactor-design.md"
```

---

## Task 6: Update Master Bank SKILL.md

**Files:**
- Modify: `.claude/skills/finpath-newsroom-master-bank/SKILL.md`

- [ ] **Step 1: Read current SKILL.md để identify exact lines**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -n "targets.yaml\|targets'\|targets\"\|primary source\|## References\|## Output" .claude/skills/finpath-newsroom-master-bank/SKILL.md
```

Memorize line numbers for each edit.

- [ ] **Step 2: Edit (a) — Remove targets.yaml references**

Find line 187 (Pipeline log spec example):
```markdown
| `Manual_YAML/` | `Manual_YAML/<file>:<row_key>` (vd `Manual_YAML/targets.yaml:MBB-2026`) | `<code>` mono |
```

Replace example với:
```markdown
| `Manual_YAML/` | `Manual_YAML/<file>:<row_key>` (vd `Manual_YAML/credit_room.yaml:MBB-2026`) | `<code>` mono |
```

Find line 242 (References table):
```markdown
| Targets vs Actual | `data/manual/targets.yaml` (load with pyyaml) |
```

Remove line entirely (no replacement — file deleted).

- [ ] **Step 3: Edit (b) — Add `## Data fetching protocol — auto-fallback` section**

Find a good insertion point (sau "## References" section hoặc trước "## Output", parallel với CK pattern). Insert:

```markdown
## Data fetching protocol — auto-fallback

Khi viết bài, Master Bank PHẢI chain data sources theo thứ tự, KHÔNG skip. Pipeline log emit `data_trail` array per V4.0 schema.

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

**KHÔNG còn `targets.yaml`** — đã drop trong refactor v2.0. Master fetch ĐHĐCĐ + actual quarter qua Finpath API + web_search (xem step 3-4).

### 3. Finpath API

Fetch realtime BCTC + Bank ratios + events:

```python
from lib.finpath_api import FinpathAPI
api = FinpathAPI()
# Bank-specific ratios
ratios = api.get_bank_ratios(ticker)             # NIM/CASA/COF/NPL/LDR/PE/PB/ROE
ratios_batch = api.get_bank_ratios_batch([t1, t2])  # competitive comparison
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
# Ownership + events + news
shareholders = api.get_shareholders(ticker)
events = api.get_events(ticker)                   # ĐHĐCĐ events (replaces targets.yaml lookup)
news = api.get_news(ticker)
profile = api.get_company_profile(ticker)
```

`data_trail[].source = "Finpath_API/<endpoint_name>"` (vd `Finpath_API/bankfinancialratios`)

### 4. Web_search — fallback khi 1-3 thiếu

ESPECIALLY web_search cho:
- **ĐHĐCĐ kế hoạch năm chi tiết** (Finpath events có summary nhưng không full plan): keywords `"[TICKER] nghị quyết ĐHĐCĐ [năm]"`, `"[TICKER] kế hoạch lợi nhuận [năm]"`, `"[TICKER] ĐHĐCĐ [năm] room tín dụng"`
- **Actual quarter completion %**: keywords `"[TICKER] kết quả Q[X]/[năm]"`, `"[TICKER] đạt bao nhiêu kế hoạch năm"`
- **NHNN nới room mid-year** (case 28/8/2024): keywords `"NHNN nới room [TICKER] [năm]"`, `"NHNN cấp room đợt 2 [năm]"`
- **Tin tức recent về bank cụ thể**: keywords `"[TICKER] [topic] [date]"`
- **Sự kiện thị trường ảnh hưởng sector**: keywords `"ngành ngân hàng [topic] [date]"`

`data_trail[].source = "WebSearch/<sanitized-keyword>"`

### Reject rule

KHÔNG bịa số khi data không có. Sau cả 4 step (KB + YAML + Finpath API + web_search 3+ keywords khác nhau) vẫn không có data → reject với `master_decision: reject_no_data` + `data_trail` ghi rõ search attempts (transparency).
```

- [ ] **Step 4: Edit (c) — Update References section**

Find `## References` section (around line 240+). Verify references list:
- Remove "Targets vs Actual | `data/manual/targets.yaml`" line (already done in Step 2)
- Ensure 4 KB markdown links present:

```markdown
## References (data sources for Master Bank)

| Resource | Pattern |
|---|---|
| KB ngành Ngân hàng | `KBLoader('kb/bank/').search([keywords])` + `loader.load_topic(path)` |
| Credit Room | `data/manual/credit_room.yaml` (load with pyyaml) |
| NHNN Circulars | `data/manual/nhnn_circulars.yaml` (load with pyyaml) |
| Finpath API | `lib.finpath_api.FinpathAPI()` — 14 endpoints (xem Data fetching protocol) |
| Web Search | `WebSearch` tool — fallback khi local thiếu |
```

(Adjust to match existing table style — keep existing rows for non-targets data sources.)

- [ ] **Step 5: Smoke check edits applied**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
echo "(a) targets.yaml mentions:"
grep -c "targets.yaml" .claude/skills/finpath-newsroom-master-bank/SKILL.md
# Expected: 0 (or 1 if explicitly referencing as "dropped" in protocol)
echo "(b) Auto-fallback section:"
grep -c "Data fetching protocol — auto-fallback" .claude/skills/finpath-newsroom-master-bank/SKILL.md
# Expected: 1
echo "(c) KB Bank references:"
grep -c "kb/bank/frameworks/" .claude/skills/finpath-newsroom-master-bank/SKILL.md
# Expected: ≥4
```

- [ ] **Step 6: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/skills/finpath-newsroom-master-bank/SKILL.md && git commit -m "skill(bank): add auto-fallback protocol + remove targets.yaml refs

Refactor v2.0 — parity với CK v1.2 pattern:
(a) Remove targets.yaml mentions (file deleted Task 5)
(b) Add ## Data fetching protocol — auto-fallback section (parallel
    CK SKILL.md) — chain 4 sources (KB → YAML → Finpath API →
    web_search) with reject_no_data rule
(c) Update References section (4 KB markdown + 2 YAML + Finpath API
    + web_search)

Master Bank skill bây giờ explicit về data flow + audit trail rõ ràng
trong pipeline log (data_trail array V4.0 schema).

Spec: docs/superpowers/specs/2026-05-11-bank-kb-refactor-design.md"
```

---

## Task 7: Update agent file `newsroom-master-bank.md`

**Files:**
- Modify: `.claude/agents/newsroom-master-bank.md`

- [ ] **Step 1: Read current state**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && sed -n '94,110p' .claude/agents/newsroom-master-bank.md
```

Verify Step 5 (Query manual YAML) loads `['targets', 'credit_room', 'nhnn_circulars']`.

- [ ] **Step 2: Edit Step 5 — drop `targets` from YAML load list**

Use Edit tool. Replace:

```python
for name in ['targets', 'credit_room', 'nhnn_circulars']:
    data = yaml.safe_load(Path(f'data/manual/{name}.yaml').read_text())
    matches = [d for d in data if d.get('ticker') == '<TICKER>']
    print(f'{name}:', json.dumps(matches, ensure_ascii=False))
```

With:

```python
for name in ['credit_room', 'nhnn_circulars']:
    data = yaml.safe_load(Path(f'data/manual/{name}.yaml').read_text())
    matches = [d for d in data if d.get('ticker') == '<TICKER>']
    print(f'{name}:', json.dumps(matches, ensure_ascii=False))
# targets.yaml DROPPED v2.0 — Master fetch ĐHĐCĐ + actual via:
#   - api.get_events(ticker) for ĐHĐCĐ events
#   - api.get_income_statement(ticker) for actual quarter LNTT
#   - web_search '[TICKER] nghị quyết ĐHĐCĐ [năm]' for full plan detail
```

- [ ] **Step 3: Edit line 267 (pipeline log spec example)**

Find:
```markdown
- YAML → `Manual_YAML/<file>:<row_key>` (e.g. `Manual_YAML/targets.yaml:MBB-2026`)
```

Replace với:
```markdown
- YAML → `Manual_YAML/<file>:<row_key>` (e.g. `Manual_YAML/credit_room.yaml:MBB-2026`)
```

- [ ] **Step 4: Smoke check no more targets.yaml references**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -c "targets.yaml\|'targets'" .claude/agents/newsroom-master-bank.md
# Expected: 0
```

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/agents/newsroom-master-bank.md && git commit -m "agent(bank): remove targets.yaml load + reference per refactor v2.0

- Step 5 Query manual YAML: drop 'targets' from load list, only
  load credit_room + nhnn_circulars (targets.yaml DELETED Task 5)
- Add inline comment explaining Master fetch ĐHĐCĐ + actual via
  Finpath API + web_search instead
- Line 267 pipeline log spec example: targets.yaml → credit_room.yaml

Spec: docs/superpowers/specs/2026-05-11-bank-kb-refactor-design.md"
```

---

## Task 8: Cross-file numerical consistency check

**Files:**
- Verify (no code change): all 4 KB markdown files

- [ ] **Step 1: Compare same metrics across files**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && echo "=== NIM ranges ===" && grep -nH "NIM.*range\|NIM tier\|NIM bình quân\|NIM 2[0-9]" kb/bank/frameworks/*.md | head -10 && echo "=== CASA ranges ===" && grep -nH "CASA range\|CASA tier\|CASA bình quân\|Top tier.*CASA" kb/bank/frameworks/*.md | head -10 && echo "=== NPL ranges ===" && grep -nH "NPL range\|NPL tier\|NPL bình quân" kb/bank/frameworks/*.md | head -10
```

Verify no numerical contradictions across files (vd NIM "tier high >4%" trong nim-cycle phải consistent với master-reference). If contradictions → fix forward inline.

- [ ] **Step 2: Verify Notion frontmatter completely removed all 4 files**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -c "notion_page_id\|last_synced\|source_url:.*notion" kb/bank/frameworks/*.md
```

Expected: all 4 files return `0`.

- [ ] **Step 3: Verify no per-Q4/2025 anchor data leak**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -rn "Q4/2025\|MBB 36.83\|TCB 34.48\|VCB 33.72" kb/bank/ | grep -v "verified\|http\|case study"
```

Expected: ≤2 hits (acceptable: source URL with "Q4/2025" verified date label, hoặc explicit case study reference). If many hits in narrative tables → fix forward.

- [ ] **Step 4: Smoke check end-to-end (KB load + YAML structure + SKILL.md + agent file)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.kb_loader import KBLoader
import yaml

# KB Bank
loader = KBLoader('kb/bank/')
print(f'KB Bank files: {len(loader._all_files())}')
for kw in ['NIM', 'CASA', 'NPL', 'Basel', 'target', 'room', '6 lớp']:
    matches = [r['title'] for r in loader.search([kw])]
    print(f'  search [{kw}]: {matches}')

# YAML
print()
import os
print(f'YAML files in data/manual/:')
for f in sorted(os.listdir('data/manual')):
    if f.endswith('.yaml'):
        with open(f'data/manual/{f}') as fp:
            data = yaml.safe_load(fp)
        print(f'  {f}: {len(data)} rows')

# Targets.yaml gone
assert not os.path.exists('data/manual/targets.yaml'), 'targets.yaml still exists!'
print(f'  targets.yaml: DELETED (correct)')
"
```

Expected:
- KB Bank files: 4
- YAML: credit_room.yaml + nhnn_circulars.yaml + ssc_circulars.yaml (NO targets.yaml)
- Each keyword search returns ≥1 match

- [ ] **Step 5: Smoke check SKILL.md + agent file**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
echo "=== SKILL.md ==="
echo "(a) targets.yaml refs:"
grep -c "targets.yaml" .claude/skills/finpath-newsroom-master-bank/SKILL.md
echo "(b) Auto-fallback section:"
grep -c "Data fetching protocol — auto-fallback" .claude/skills/finpath-newsroom-master-bank/SKILL.md
echo "(c) KB Bank refs:"
grep -c "kb/bank/frameworks/" .claude/skills/finpath-newsroom-master-bank/SKILL.md
echo "=== Agent file ==="
echo "(d) targets.yaml refs:"
grep -c "targets.yaml\|'targets'" .claude/agents/newsroom-master-bank.md
```

Expected: (a)=0 (or 1 nếu mention "dropped"), (b)=1, (c)≥4, (d)=0.

- [ ] **Step 6: Commit (if any reconcile needed)**

If Step 1 found contradictions hoặc Step 3 found anchor leak, fix inline + commit:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add kb/bank/frameworks/ && git commit -m "kb(bank): reconcile cross-file numerical consistency post-refactor

[describe specific reconcile if any]

Spec: docs/superpowers/specs/2026-05-11-bank-kb-refactor-design.md"
```

If no reconcile needed, skip commit (Task 8 is pure verification).

---

## Hand-off to user (CRITICAL — STOP after Task 8)

After Task 8 smoke checks pass, **HAND OFF cho user** để E2E test. Do NOT run `/tin TCB` automated.

Hand-off message format:

> "Bank KB refactor v2.0 hoàn thành (8 tasks, ~9 commits). Smoke checks pass:
> - 4 KB markdown clean (no Notion frontmatter, no Q4/2025 anchor leak)
> - targets.yaml deleted, credit_room + nhnn_circulars + ssc_circulars intact
> - SKILL.md có auto-fallback section + KB references
> - Agent file no targets.yaml load
>
> **Bạn run `/tin TCB`** để E2E test:
> - Master Bank query KB + Finpath API + web_search OK?
> - Article pass 5 quality gates V4.0?
> - Pipeline log emit `data_trail` schema correct?
>
> Báo lại kết quả → fix forward nếu issue, hoặc ship nếu OK."

---

## Self-review checklist (run sau khi xong 8 task)

- [ ] **Spec coverage:** All 11 sections of spec mapped to tasks (§ 4 markdown structure = Tasks 1-4 common pattern, § 5 SKILL.md updates = Task 6, § 6 agent file = Task 7, § 8 validation = Task 8 smoke checks).

- [ ] **No placeholder leak:** Search plan cho "TODO", "TBD", "fill in later" → 0 hit. (Note: "[describe specific reconcile if any]" trong Task 8 Step 6 commit message is intentional — only used IF reconcile happens.)

- [ ] **Type/path consistency:** All file paths consistent. `KBLoader('kb/bank/')` consistent. YAML field names match across edits.

- [ ] **Final smoke check passes:** Task 8 confirms 4 KB files load, targets.yaml deleted, SKILL.md + agent file updated.

---

## Open questions / followup (post-plan)

- **E2E test result** — User report sau khi run `/tin TCB`. Fix forward nếu issue.
- **Bank-target-vs-actual-pattern.md filename** — Per spec § 11 Open questions: keep filename (low value rename + risk break references).
- **Future BĐS sector KB** — sẽ apply cùng pattern v1.2 (parity với CK + Bank refactored).
