# Newsroom V2 — Direction & Project Instructions

> Cập nhật: 2026-05-12 PM — Pipeline V5.1.2
>
> Đây là tổng quan toàn pipeline mới sau 4 đợt spec (Format Diversity / Headline Craft / Hot Ticker / Observability).

---

## 🎯 Mục tiêu V5.1.2

Phá vỡ tình trạng "bài nào cũng cùng pattern" + "bài nào cũng có góc nhìn ngược" + "title em dash AI-tell" + "stance dập khuôn theo metric". Sau V5.1.2:

1. **4 format đa dạng** — bài ngắn 100-150 từ (mã đang Hot) đến bài dài 250-350 từ (data nhiều)
2. **Stance-driven** — Story Editor judge stance dựa 7-layer nội lực, Master execute theo hướng
3. **Headline craft riêng** — agent dedicated giật tít, 5 hard criteria + 4 lối flexible (NO em dash)
4. **Observability fail-loud** — schema check `model + duration_ms` per step
5. **Skill SPLIT** — file ≤200 lines, dễ navigate

---

## 🔥 Triggers

| Command | Behavior |
|---|---|
| `/tin <TICKER>` | Single ticker dispatch — 1 pipeline run |
| `/tin-hot N` | Top N × 4 nhóm Hot — sequential dispatch (4N ticker, intersect 61 universe TRƯỚC compute top) |

**4 nhóm Hot** (mirror finpath-web `stockDataUtils.ts`):
- Tăng giá — `topPriceIncrement`
- Giảm giá — `topPriceDecrement`
- Bùng nổ volume — `topVolumeExplosion`
- Cạn cung — `topDepletedSupply`

`/tin-hot 3` = 12 ticker (3 × 4 nhóm). Sequential dispatch để observability rõ.

---

## 📋 Pipeline 12 step (V5.1.2)

> ⏸ Step 5 Skeptic PAUSED từ 2026-05-12 → 11 step active. Re-enable khi quyết định format nào cần Skeptic.

```
1. Crawler (Python)
   ↓
1.5. Market Snapshot (Python NEW V5.0)
   ↓
2. Editor V1 (subagent — gate + sector)
   ↓
3. Story Editor (subagent — brief + stance_directive NEW V5.1.2)
   ↓
3.5. Format Director (subagent Sonnet NEW V5.0)
   ↓
4. Master sector (subagent Bank/CK/BĐS — body only, NO title V5.1)
   ↓
4.5. Headline Craft (subagent Sonnet NEW V5.1)
   ↓
⏸ 5. Skeptic (PAUSED 2026-05-12)
   ↓
6. Render markdown (Python)
   ↓
7. Git publish (Python)
   ↓
8. Pages wait (Python)
   ↓
9. Telegram notify (Python + subagent dispatch)
```

---

## Step 1: Crawler

- **Type**: Python mechanical
- **File**: `lib/stages/run_crawler.py`
- **Input**: ticker
- **Action**: WebSearch + WebFetch top 5-15 article về ticker từ cafef / vneconomy / znews
- **Output**: insert N rows vào `crawl_log` SQLite
- **Persist**: `crawl_log` table

## Step 1.5: Market Snapshot (NEW V5.0)

- **Type**: Python mechanical
- **File**: `lib/stages/run_market_snapshot.py`
- **Input**: ticker
- **Action**: Call Finpath API → price + volume → compute:
  - `ticker_status`: Hot / Cold / Normal
  - `day_change_pct`: float
  - (Có thể mở rộng: `volume_x_avg`, `gap_to_ceiling`)
- **Output**: stamp `market_snapshot` field vào crawl_log rows + standalone snapshot row
- **Persist**: pipeline_log `step_1_5_market_snapshot`

## Step 2: Editor V1

- **Type**: Subagent `newsroom-editor`
- **Action**: Đọc 1 row crawl_log → detect ticker → validate universe 61 mã → set sector (Bank/CK/BĐS)
- **Output**: `editor_v1_decision` (route_to_story_editor | reject) + `editor_v1_note`
- **Persist**: UPDATE crawl_log row

## Step 3: Story Editor — V5.1.2 thay đổi lớn

- **Type**: Subagent `newsroom-story-editor`
- **V5.1.2 thêm**: brief schema có `stance_directive` object
- **Action**:
  - Đọc batch crawl_log rows (after Editor V1 route)
  - Cross-intersect Market Snapshot (price event) × 7-layer nội lực (broad)
  - Judge stance — KHÔNG matrix 2×2 cứng
  - Output 0-3 brief V5.1.2 JSON
- **Output schema**:

```yaml
brief:
  deep_question_options:
    - question: "..."
      category: paradox | why_now | hidden_mechanism | comparison_deep | early_signal
  angle_label: "..."
  angle_narrative: "..."
  stance_directive:                  # NEW V5.1.2
    direction: positive | negative | neutral
    confidence: high | medium | low
    reason: "Free-form prose 1-3 câu giải thích WHY stance"
    key_evidence:
      - "..."
      - "..."
```

- **7-layer nội lực** (Story Editor judge dựa context, KHÔNG metric đơn lẻ):

| Layer | Examples |
|---|---|
| 1. Tài chính | Chỉ số kinh doanh + dòng tiền + nợ (ROA/ROE/NPL/NIM/CASA chỉ là 1 phần) |
| 2. Quản trị | HĐQT ổn định, pháp lý sạch, ESG |
| 3. Chiến lược | Roadmap rõ, M&A đúng hướng, expansion solid |
| 4. Vận hành | Market share, customer base, hiệu quả |
| 5. Sản phẩm | Innovation, dẫn dắt thị trường |
| 6. Sector cycle | Đang đỉnh hay đáy chu kỳ ngành |
| 7. Vĩ mô | Lãi suất, regulation, sector tailwind |

- **Quan trọng**: KHÔNG dập khuôn "PE cao = negative" hoặc "giảm sàn = positive". Stance dựa REASON narrative cross-intersect.

## Step 3.5: Format Director (NEW V5.0)

- **Type**: Subagent Sonnet `newsroom-format-director`
- **Action**:
  - Input: briefs[] + market_snapshot + variety_guard (last 3 format used)
  - Apply 4-factor scoring matrix (Hot status / category / data richness / variety penalty)
  - Output: `format_picks[]` — 1 format per brief
- **4 format choices**:

| ID | Word count | Khi nào |
|---|---|---|
| `flash_qa` | 100-150 từ | Ticker Hot (top tăng/giảm/bùng nổ/cạn cung) + data low |
| `standard_qa` | 200-300 từ | Category paradox/why_now + data medium |
| `standard_listicle` | 250-350 từ | Data high — current default V4.0 |
| `standard_narrative` | 250-350 từ | Cần dẫn dắt kể chuyện thay vì bullet |

- **Hybrid scoring**: Rule-based 80% case + Sonnet judgment 20% case khó (tie hoặc gần). Variety guard penalty -1 nếu format đã dùng 2/3 bài gần nhất.
- **Persist**: pipeline_log `step_3_5_format_director` (model + duration_ms + format_picks)

## Step 4: Master sector — V5.1.2 thay đổi lớn

- **Type**: Subagent (route theo sector từ Editor V1)
  - Bank → `newsroom-master-bank`
  - CK → `newsroom-master-ck`
  - BĐS → `newsroom-master-bds`
- **V5.1.2 thay đổi**:
  - **KHÔNG generate title** (delegate to Headline)
  - **Receive `stance_directive`** từ brief → write theo hướng
  - **Em dash body** ≤ 1/100 từ
  - **8 quality gates** (was 5 V4.0)
- **Action**:
  - Read `format_id_used` từ Format Director
  - Apply format-specific body pattern (`references/format-bodies/{format_id}.md`)
  - Apply 5 Voice Layer rules (`references/voice-layer-rules.md`)
  - Apply stance_directive (`references/stance-directive-handler.md`)
  - Self-check 8 gates V5.1.2 BEFORE persist
- **Output**:

```json
{
  "article_id": "uuid",
  "body": "...",
  "insight_final": "...",
  "data_trail": [...],
  "quality_gates": {...},
  "format_id_used": "standard_listicle",
  "accepted_hypothesis": true
}
```

→ KHÔNG có field `title`. Title nullable trong DB, Headline UPDATE sau.

## Step 4.5: Headline Craft (NEW V5.1)

- **Type**: Subagent Sonnet `newsroom-headline-craft`
- **Input**:

```python
@dataclass
class HeadlineInput:
    article_id: str
    body: str
    insight_final: str
    format_id: str
    brief_deep_question: str
    brief_angle_label: str
    brief_angle_narrative: str
    stance_directive: dict
    ticker: str
```

- **Workflow 5 step**:
  1. Parse input + pick 1 of 4 lối based on body shape
  2. Generate 3 candidate cùng lối
  3. Apply 5 hard criteria
  4. 8-point scoring → pick max
  5. UPDATE generated_news.title + persist pipeline_log

- **4 lối giật tít flexible** (NO em dash):

| Lối | Khi nào | Ví dụ |
|---|---|---|
| **Question** | Body chứa nghịch lý hoặc câu hỏi sắc | "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?" |
| **Declarative tension** | Body có 2 fact ngược chiều (dùng `,` hoặc `:` thay em dash) | "BIDV lãi tăng 15,6%, nợ xấu cũng tăng 21,9%" |
| **Quote** | Brief có câu nói nhân vật ấn tượng | '"Chúng tôi tự tin": VHM nói gì sau Q1?' |
| **Contrast verb** | Body so sánh 2 nhóm | "VCB chọn thận trọng, CTG chọn bứt tốc, ai đặt cược đúng?" |

- **5 hard criteria**:

| # | Criterion | Type |
|---|---|---|
| 1 | Ticker present (regex `\b[A-Z]{3,4}\b`) | Hard rule |
| 2 | ≤12 từ (`len(title.split())`) | Hard rule |
| 3 | Hook strong — definition + 2 sub-test (tension + click test) | LLM-as-judge |
| 4 | Bình dân nguy hiểm — definition + 2 sub-test (plain + sharp edge) | LLM-as-judge |
| 5 | No em dash (regex `[—]`) — V1.1 NEW | Hard rule |

- **Em dash BANNED** (`—` U+2014) — User feedback: "nhìn dấu này là biết AI viết bài". Replace: `:` > `,` > `?` > `.` > `""` > `()`.
- **Output**:

```json
{
  "final_title": "...",
  "final_loi": "Question",
  "picked_score": 7,
  "candidates": [...],
  "hard_criteria_pass": {...}
}
```

- **Persist**:
  - SQL: `UPDATE generated_news SET title = ?, headline_final = ?, updated_at = NOW() WHERE article_id = ?`
  - pipeline_log: `step_4_5_headline_craft`

## ⏸ Step 5: Skeptic (PAUSED 2026-05-12)

**Lý do**: User feedback "cái gì cũng cho góc nhìn ngược vào thì không hợp lý". Đợi quyết định format nào (flash_qa / standard_qa / standard_listicle / standard_narrative) sẽ có Skeptic.

**Hành động hiện tại**: BỎ QUA Step 5 — KHÔNG dispatch `newsroom-skeptic`. Article publish bình thường sau Step 4.5 Headline.

**Re-enable**: Khi quyết định, uncomment block trong `.claude/agents/newsroom-pipeline.md` + thêm rule "chỉ dispatch nếu format_id ∈ {allowed_formats}".

## Step 6: Render markdown

- **Type**: Python mechanical
- **File**: `lib/render_compare_feed.py`
- **Action**: Read generated_news + pipeline_log → render markdown V5.1.2
- **Output**: 1 file per article `output/compare-feed/<TICKER>-<DATE>-<HHMM>-<slug>.md`
- **Manifest**: `output/compare-feed/manifest.json` với `format_id` field cho FormatFilter UI

## Step 7: Git publish

- **Type**: Python mechanical
- **File**: `lib/stages/run_git_publish.py`
- **Action**: `git add output/compare-feed/` → commit → push origin main
- **Self-heal**: retry on conflict + force-pull-rebase, max 3 retry

## Step 8: Pages wait

- **Type**: Python mechanical
- **File**: `lib/stages/run_pages_wait.py`
- **Action**: Poll GitHub Pages workflow status until publish complete
- **Timeout**: 5 phút

## Step 9: Telegram notify

- **Type**: Python + subagent dispatch `newsroom-telegram-publisher`
- **Action**: Send notify với link `/article/<public_slug>` đến channel

---

## 🎨 4 Article Format V5.1.2

### `flash_qa` (100-150 từ)

- **Khi**: Ticker_status Hot (top tăng/giảm/bùng nổ/cạn cung) + data low
- **Pattern**:
  - 1 câu mở (≥20 từ): nêu question chính
  - 1 paragraph trả lời (60-100 từ): answer + verdict
  - 1 câu closing (≤20 từ): verdict ngắn
- **KHÔNG** bullet, KHÔNG heading "## Cần để ý"

### `standard_qa` (200-300 từ)

- **Khi**: Category paradox/why_now + data medium
- **Pattern**:
  - Opening (30-50 từ): tension + setup
  - 2-3 bullet (each ≥20 từ + ≥1 bold highlight)
  - Closing (1 câu phân loại NĐT)

### `standard_listicle` (250-350 từ) — current default V4.0

- **Khi**: Data high (≥5 datapoint)
- **Pattern**:
  - Opening (30-60 từ)
  - 4-6 bullet (each ≥20 từ + ≥1 bold highlight)
  - Closing (1 câu phân loại NĐT)

### `standard_narrative` (250-350 từ)

- **Khi**: Cần dẫn dắt kể chuyện thay vì liệt kê
- **Pattern**:
  - Opening (40-80 từ)
  - 2-3 paragraph prose (each 60-100 từ)
  - Closing (1 câu phân loại NĐT)
- **KHÔNG** bullet hoặc tối đa 1 bullet

---

## ✅ 8 Quality Gates V5.1.2 (Master)

| # | Gate | Type | Enforce |
|---|---|---|---|
| 1 | No English jargon (NPL/NIM/CASA → tiếng Việt) | Hard regex | Pre-persist |
| 2 | No metadata leak (strategic-shift, insight_type, ...) | Hard regex | Pre-persist |
| 3 | No-hedging (LLM-as-judge 2 test) | Definition-based | Pre-persist |
| 4 | Verdict line bắt buộc | LLM-as-judge | Pre-persist |
| 5 | Stance consistency (cite ≥1 evidence + direction match) | Substring + LLM | Pre-persist |
| 6 | Em dash density body (≤1/100 từ) | Hard regex | Pre-persist |
| 7 | Word count per format | Hard math | Pre-persist |
| 8 | Body pattern per format (bullets / paragraphs check) | LLM-as-judge | Pre-persist |

**Title gates** (Headline owns, separate from Master):
- Ticker present (hard regex)
- ≤12 từ (hard math)
- Hook strong (LLM-as-judge 2 sub-test)
- Bình dân nguy hiểm (LLM-as-judge 2 sub-test)
- No em dash (hard regex)

---

## 🎭 Voice Layer 5 Rules (Master)

| Rule | Mô tả |
|---|---|
| V1: Stance required | Bài MUST có quan điểm rõ (theo stance_directive từ Story Editor) |
| V2: No-hedging | Definition-based: câu phải có direction cam kết. Test 1 reverse-truth + Test 2 direction. KHÔNG list từ cấm. |
| V3: Verdict line | Closing MUST có verdict cụ thể cho NĐT phân loại |
| V4: Title stance | Delegated to Headline — Master chỉ đảm bảo body stance rõ |
| V5: Contrarian-when-warranted | Chỉ nghịch insight khi data clear support, KHÔNG override stance_directive |

### V2 No-hedging — định nghĩa (KHÔNG list từ)

**"Ba phải"** = câu khẳng định trung tính không cam kết hướng nào, có thể đúng dù sự thật ngược lại.

**Test 1 — Reverse-truth**: Đảo ngược sự thật, câu vẫn đúng → fail
- ❌ "Cổ phiếu có thể tăng tùy thuộc thị trường" → BA PHẢI
- ✅ "Cổ phiếu sẽ tăng vì Q1 lãi vượt 30%" → KHÔNG ba phải

**Test 2 — Direction check**: Có cam kết direction không?
- ❌ "Vẫn còn phải chờ thêm dữ liệu mới biết"
- ✅ "Đà tăng có thể chững lại Q2 nếu NHNN siết lãi suất"

→ LLM-as-judge dùng 2 test, KHÔNG regex match keyword.

---

## 📊 Case Study Stance — PE/PB cao + tăng trần

### Case A: PE cao nhưng vẫn còn room (positive stance)

**External**: TCB +6.8% (kịch trần), PE 18x vs ngành 11x, PB 2.1x vs 1.3x.

**Rule cứng nói**: PE/PB cao = đắt → negative.

**Phân tích 7-layer**:

| Layer | Context | Signal |
|---|---|---|
| Tài chính | ROE 22%, CASA 38%, NPL 0.9% | Mạnh |
| Quản trị | Cổ tức 67%, CEO clean | Mạnh |
| Chiến lược | Spin-off BĐS Q4/2026 | Catalyst |
| Vận hành | Retail share +22% YoY | Momentum |
| Sản phẩm | Mobile-first | Innovation |
| Sector cycle | NHNN nới lỏng | Tailwind |
| Vĩ mô | Lãi suất giảm 2 lần | Tích cực |

**PEG** = 18 / 25 (growth) = **0.72** → growth-adjusted vẫn cheap.

**Stance**: `positive (high confidence)` — "TCB tăng trần dù PE/PB cao hơn ngành 60%. 7 layer mạnh, PE cao là growth premium, KHÔNG bubble. PEG 0.72."

**Title (Headline pick lối Question)**: "TCB PE 18x cao gấp đôi ngành, vì sao vẫn được tích lũy?"

### Case B (đối lập): PE cao + tăng trần = bong bóng (negative stance)

**External**: NVL2 +6.5% (kịch trần), PE 35x vs ngành 8x, volume x8 average.

**Phân tích 7-layer**: 6/7 layer YẾU (ROE 4%, lỗ Q3-Q4, sector đáy, dự án thanh tra).

**Stance**: `negative (high confidence)` — "NVL2 tăng trần volume bất thường. ROE 4%, lỗ liên tiếp, sector BĐS đáy. Pump pattern rõ ràng, no fundamental."

**Title (Headline pick lối Declarative tension)**: "NVL2 tăng trần phiên 12/5, ROE 4% và lỗ 2 quý liên tiếp"

### Key takeaway

External signal giống nhau (tăng trần + PE cao) → KHÔNG đủ judge stance. Phải nhìn 7-layer nội lực + PEG ratio + volume pattern + catalyst pipeline → stance phụ thuộc REASON narrative, không rule cứng.

---

## 🗂 File Structure V5.1.2

### Agents (10 files)

```
.claude/agents/
├── newsroom-pipeline.md           (~180 lines sau split)
├── newsroom-editor.md
├── newsroom-story-editor.md
├── newsroom-format-director.md    (NEW V5.0)
├── newsroom-master-bank.md
├── newsroom-master-ck.md
├── newsroom-master-bds.md
├── newsroom-headline-craft.md     (NEW V5.1)
├── newsroom-skeptic.md            (⏸ paused)
└── newsroom-telegram-publisher.md
```

### Skills (10 folders)

```
.claude/skills/finpath-newsroom-orchestrator/
├── SKILL.md (~140 lines)
└── references/
    ├── observability-emit.md
    ├── db-persist-patterns.md
    ├── failure-recovery.md
    ├── step-1-5-market-snapshot.md
    ├── step-3-5-format-director.md
    ├── step-4-5-headline-craft.md
    └── compare-feed-layout.md
```

```
.claude/skills/finpath-newsroom-master-bank/   (same pattern for ck + bds)
├── SKILL.md (~180 lines)
└── references/
    ├── format-bodies/
    │   ├── flash-qa.md
    │   ├── standard-qa.md
    │   ├── standard-listicle.md
    │   └── standard-narrative.md
    ├── voice-layer-rules.md      (duplicate 3 copies vì CLAUDE.md cấm shared folder)
    ├── stance-directive-handler.md
    ├── format-examples.md
    ├── db-query-patterns.md
    ├── jargon-mapping.md
    ├── master-pitfalls.md
    └── compare-feed-spec.md
```

```
.claude/skills/finpath-newsroom-headline-craft/  (NEW V5.1)
├── SKILL.md (~150 lines)
└── references/
    ├── 4-loi-giat-tit.md
    ├── criteria-definitions.md
    ├── no-em-dash-policy.md
    └── candidates-scoring.md
```

```
.claude/skills/finpath-newsroom-format-director/ (NEW V5.0)
├── SKILL.md (~150 lines)
└── references/
    ├── decision-matrix.md
    ├── variety-guard.md
    └── 4-format-overview.md
```

---

## 🌐 Universe — 3 sector (61 mã)

| Sector | HOSE | HNX | UPCOM | Total |
|---|---|---|---|---|
| Bank | 16 | 4 | 7 | 27 |
| CK | 5 | 15 | 10 | 30 |
| BĐS | 4 | - | - | 4 |
| **Total** | **25** | **19** | **17** | **61** |

**Bank** (27): VCB CTG BID TCB MBB ACB VPB HDB STB SHB EIB TPB MSB LPB OCB VIB · NAB BAB NVB SGB · VAB BVB ABB KLB VBB PGB HDF

**CK** (30): SSI VND HCM VCI VIX · SHS MBS BVS BSI AGR CTS APG EVS IVS PSI TVS WSS ORS VFS TCI · DSC FTS CSI SBS PHS ART APS BMS AAS VTS

**BĐS** (4): VHM NVL KDH DXG (KBC defer — KCN pattern khác)

---

## 🎨 Frontend Viewer

### FeedPage filter UI

3 filter (URL-persisted):
- **SymbolFilter** (ticker) — `?s=VCB,TCB`
- **FormatFilter** (4 format) — `?f=standard_listicle,flash_qa` — NEW V5.1
- **AngleFilter** (5 category) — `?c=paradox,why_now`

**Conditional render AngleFilter**: ẩn khi user pin chỉ `flash_qa` (format không dùng 5-category enum).

### Article layout

- **Left column**: Master body + Skeptic critique (nếu có — Step 5 paused 2026-05-12)
- **Right column**: 7 sections (was 8, ẩn Skeptic data trail) — Source / Why chosen / Angle / Deep question / Crawl funnel / Master data trail / Đọc bài gốc + Appendix Pipeline observability

### Per-format viewer adapt (future)

- `flash_qa`: compact right column (3 sections)
- `standard_*`: full right column (7 sections)

---

## 🧠 Triết lý design V5.1.2

1. **Define principle, không rule cứng** — anti-pattern dùng definition + test logic + example pair (KHÔNG list từ cấm)
2. **Stance-driven Master** — Story Editor judge stance, Master execute theo hướng (không tự quyết)
3. **Title craft = nghệ thuật riêng** — tách Headline agent dedicated
4. **Em dash `—` BANNED title** — AI-tell, không nhân tính
5. **Flexible judgment, không matrix rigid** — PE/PB cao KHÔNG auto = negative; check 7-layer nội lực + context
6. **Skill SPLIT** — file ≤200 lines, references/ on-demand
7. **Observability fail-loud** — schema check `model + duration_ms` mỗi step

---

## 📜 5 Spec / 5 Plan đang lock

| # | Subsystem | Spec | Plan |
|---|---|---|---|
| **B+E** | Format Diversity + Voice Layer | `2026-05-11-master-article-format-diversity-design.md` V1.2 | `2026-05-11-master-article-format-diversity.md` (V5.1.2 PATCH) |
| **C** | Headline Craft | `2026-05-12-headline-craft-agent-design.md` V1.1 | `2026-05-12-headline-craft-agent.md` (V1.1 PATCH) |
| **A** | Hot Ticker | `2026-05-12-hot-ticker-trigger-design.md` V1.1 | `2026-05-12-hot-ticker-trigger.md` |
| **D** | Observability | folded vào B+C schema | - |

---

## 🎯 Implementation Status

| Phase | Spec/Plan | Implementation |
|---|---|---|
| Spec design | ✅ 5 spec lock V1.2 / V1.1 | - |
| Plan ready | ✅ 5 plan với V5.1.2 PATCH NOTICE | - |
| Code execution | ⏳ Pending | Awaiting user trigger |

---

## 🚀 Next steps

1. Brainstorm thêm gap còn lại (nếu có)
2. Spec self-review by user
3. Launch subagent-driven-development → execute Plan B + C + A
4. Skeptic re-enable decision (khi user quyết format nào cần)

---

*Tài liệu này được sinh tự động từ session brainstorm 2026-05-12. Source of truth: 5 spec/plan trong `docs/superpowers/specs/` + `docs/superpowers/plans/`.*
