# Master Article Format Diversity — Design Spec V5.0

**Date**: 2026-05-11
**Author**: Brainstormed with em (Claude)
**Status**: Draft — pending user review before plan
**Supersedes**: V4.0 single-format Master article structure (gates from `2026-05-08-newsroom-v4-redesign.md`)

---

## 1. Goal

Phá vỡ tình trạng "bài nào cũng cùng một pattern" trong feed Newsroom. Sau spec này, Master sector sản xuất **4 format đa dạng** (Flash-Q&A / Standard-Q&A / Standard-Listicle / Standard-Narrative), mỗi format có pattern trình bày + word count + title style riêng. Format được **Format Director agent dedicated** (Sonnet) chọn theo data shape + category sau Story Editor.

Đồng thời thêm **Voice Layer 5 rule** áp ngang qua tất cả format để Master viết với **giọng chuyên gia kiên định** (stance rõ, không nước đôi, verdict cuối bài có hướng + khung TG + action cho NĐT đang cầm — không vi phạm pháp lý BUY/SELL).

## 2. Problem statement (từ feedback sếp)

Ba vấn đề cụ thể được sếp nêu:

1. **Thiếu tính thời điểm**: bài có insight nhưng không kết nối với mood thị trường tại thời điểm publish.
2. **Pattern dập khuôn**: 100% bài hiện tại theo cấu trúc opening + 3-6 bullets + closing với word count 200-400. Cùng 1 layout = boring dần.
3. **Nhu cầu user thực tế**:
   - Ngôn ngữ phải bình dân nhưng **không nhạt**.
   - Closing phải có **định hướng rõ** cho cổ phiếu — không ba phải, không "tùy quan điểm".

## 3. Out of scope (defer)

Trong feedback gốc của sếp có 5 subsystem độc lập. Spec này CHỈ cover **subsystem B (Format Diversity) + E (Tone+Verdict)**. Defer:

| Subsystem | Tên | Status |
|---|---|---|
| A | Hot ticker trigger (top tăng/giảm trong ngày → auto pipeline) | Defer — sau khi quality ổn |
| C | Headline craft agent riêng | Defer — Format Director đã cover title pattern per-format |
| D | Pipeline observability agent dedicated | Defer — separate spec |

Spec này chỉ inject **minimal mood-sync** (giá ngày + % change) vào brief, KHÔNG implement full hot ticker trigger.

## 4. Architecture overview

### Pipeline V5.0 (11 steps, +2 so V4.0)

```
Step 1: Crawler (Python lib/stages/run_crawler.py)
Step 1.5: Market Snapshot (Python lib/stages/run_market_snapshot.py NEW)
         fetch price_today + pct_change_today + volume_ratio_3d via Finpath API get_quote
         Soft fetch — failure → brief proceeds without ticker_market_data
Step 2: Editor V1 (subagent newsroom-editor)
Step 3: Story Editor (subagent newsroom-story-editor) — pick question + stance + narrative
         ↓
Step 3.5: Format Director (subagent newsroom-format-director NEW, Sonnet)
         enriches brief with format_id + format_reason + tone_bias + length_target per option
         ↓
Step 4: Master sector (subagent newsroom-master-{bank,ck,bds})
         receives brief V5.0 with format pre-picked → apply format pattern + 9 gates + Voice Layer
         May escalate flash_qa → standard_qa ONCE if fetched data depth justifies (see §11)
Step 5: Skeptic (subagent newsroom-skeptic) — aware format khi critique, 9 angles total
Step 6: Render (Python lib/render_compare_feed.py)
Step 7-9: Phase H1 (git publish / Pages wait / Telegram) — unchanged
```

### Key changes

| Item | V4.0 | V5.0 |
|---|---|---|
| Article format | 1 fixed pattern (200-400 từ, opening+bullets+closing) | 4 formats với pattern riêng |
| Format selection | None (Master assumes V4.0 pattern) | Format Director agent step 3.5 |
| Voice rules | Stance không bắt buộc, hedging cho phép | Stance required + no-hedging + verdict-line + title-stance + contrarian-OK |
| Quality gates | 5 gates | 9 gates (3 per-format, 6 universal) |
| Brief schema | V4.0 (deep_question_options without format) | V5.0 (deep_question_options enriched with format fields) |
| Models | Story Editor + Master = Opus | + Format Director = Sonnet |
| Market context | none | Step 1.5 Market Snapshot fetches price + pct_change (soft) |
| Migration | n/a | `pipeline_version` column gates new schema validation; V4.0 rows skip new checks |
| Skeptic angles | 6 | 9 (+ `lifeless_writing`, `verdict_weak`, `stance_drift`) |

## 5. Format Catalog

### 5.1 flash_qa (100-150 từ)

**Khi nào dùng**: 1 câu hỏi factual đơn lẻ ("X là gì", "Y cao hay thấp", "Z có thật không") — KHÔNG fit vào 5 deep_question category (paradox/why_now/hidden_mechanism/comparison_deep/early_signal).

**Pattern**:
- Title: question (MUST có `?`)
- Body: **paragraph thuần, NO bullets**. 1 đoạn 100-150 từ trả lời thẳng câu hỏi.
- Closing: compressed verdict trong câu cuối (1 câu chứa 3 yếu tố verdict).

**Ví dụ**:
> **VCB chia cổ tức 21% bằng cổ phiếu — pha loãng tới mức nào?**
>
> VCB ngày 09/05 chốt phương án phát hành 21:1 — vốn điều lệ tăng từ 83.557 lên 101.124 tỷ. Pha loãng EPS giấy tờ ~17% nhưng P/E forward thực tế gần như không đổi vì cổ tức cổ phiếu là chuyển hạch toán lợi nhuận chưa phân phối → vốn cổ phần, không đổi giá trị doanh nghiệp. Khớp NĐT giữ VCB dài hạn theo cốt lõi tăng trưởng tín dụng + tỷ suất sinh lời vốn chủ >20%.

### 5.2 standard_qa (200-300 từ)

**Khi nào dùng**: `paradox`, `why_now`, `hidden_mechanism` (case mechanism KHÔNG có timeline flow).

**Pattern**:
- Title: question (`?`) HOẶC declarative paradox (`—` + tension word: "hy sinh", "đánh đổi", "nghịch lý", "không phải", "bù lại", "vì sao").
- Body: opening ≥30 từ + **3-6 bullets each ≥20 từ với ≥1 bold highlight** + closing 1-2 câu (verdict line).
- Bullet pool: contrast / causation / warning / revelation (xem section 7).

**Ví dụ**: "Vì sao to nhất sàn lại đi chậm nhất quý này?" (mẫu V4.0 hiện tại — giữ pattern này nhưng chỉ là 1 trong 4 format).

### 5.3 standard_listicle (250-350 từ)

**Khi nào dùng**: `comparison_deep`, `early_signal`.

**Pattern**:
- Title: declarative numbered ("5 dấu hiệu...", "3 lý do...", "5 chỉ số...") hoặc declarative comparison ("Big4 vs tư nhân — ai...").
- Body: opening ngắn ≤30 từ + **4-7 bullets dày each ≥25 từ** + closing ngắn 1 câu.
- Opening compress, bullets là main content.

**Ví dụ**:
> **5 dấu hiệu Big4 và tư nhân đang đi 2 hướng ngược nhau**
>
> Q1/2026 ghi nhận khoảng cách rõ rệt — không về lợi nhuận tuyệt đối mà về cách họ định hình bảng cân đối 2026-2027.
>
> - **Big4 tăng dự phòng, tư nhân giảm**: Big4 +28% chi phí dự phòng YoY, tư nhân -5% — Big4 tích lũy buffer, tư nhân làm xong từ 2024.
> - ... (4 more bullets)
>
> Khớp NĐT diversify Big4 + tư nhân top theo 60/40 thay vì chỉ chọn 1 nhóm.

### 5.4 standard_narrative (250-350 từ)

**Khi nào dùng**: `hidden_mechanism` (case có chuỗi nguyên nhân-kết quả theo flow thời gian — narrative_setup chứa ≥3 timeline marker: "Q1/2025", "tháng X", "năm Y").

**Pattern**:
- Title: declarative story ("X — câu chuyện Y", "X — hành trình Z").
- Body: opening ≥40 từ + **flow đoạn văn (3-5 đoạn)** + 0-2 bullet highlight bold (không dense bullet) + closing 2 câu.
- Reads like a story, KHÔNG cứng nhắc bullet-list.

**Ví dụ**: "TCB chia cổ tức 67% — câu chuyện CASA 12 tháng qua" (kể chuyện flow theo thời gian).

## 6. Voice Layer (5 rule cross-cutting)

Áp dụng TẤT CẢ 4 format:

### V1 — Stance required
Brief V5.0 có field `stance` per deep_question_option. Story Editor pick 1 trong 3:
- `bullish` (tích cực)
- `bearish` (tiêu cực / cảnh báo)
- `divergent` (phân hoá rõ — phải nói rõ 2 phía, không "tùy quan điểm")

Master MUST bám stance. Skeptic critique nếu Master mềm yếu.

### V2 — No-hedging (Gate 6)
Reject từ ngữ nước đôi trong body:
- BANNED: "có thể", "tùy thuộc", "vẫn chờ", "khả năng cao", "đáng theo dõi", "nhiều khả năng", "chưa rõ"
- ALLOWED: "sẽ", "cần", "đang", "phải", "không nên", "đáng giữ" (verb dứt khoát)

### V3 — Verdict line bắt buộc (Gate 7)
Closing MUST có **3 yếu tố**:
1. Hướng (tích cực / tiêu cực / cảnh báo) — dứt khoát
2. Khung thời gian (12 tháng / 6 tháng / Q tới)
3. Action implication cho NĐT ĐANG cầm (không phải khuyến nghị MUA/BÁN — gợi ý cho holder existing: "giữ" / "chờ tích lũy thêm" / "thận trọng")

Không vi phạm pháp lý vì đối tượng là người ĐÃ cầm cổ phiếu.

Ví dụ ĐÚNG:
> "Tích cực dài hạn cho VCB. NĐT đang cầm nên giữ 12-18 tháng — chiến lược phòng thủ Q1 sẽ thành lợi thế khi nợ xấu BĐS bùng 2027. **Không cắt lỗ chỉ vì LNTT Q1 yếu — đây là chủ đích.**"

Ví dụ SAI (ba phải, reject):
> "Khớp NĐT giá trị giữ trung-dài hạn. Cần theo dõi Q2 để xác định xu hướng."

### V4 — Title stance (within Gate 4)
Title không treo câu hỏi không trả lời. Câu hỏi OK CHỈ KHI:
- Là paradox/why_now thật sự
- Body trả lời rõ câu hỏi trong opening hoặc bullet đầu

### V5 — Contrarian-when-warranted
Stance KHÔNG cần khớp mood ngày. Khi data justify, ngược chiều market được encouraged:
- Mã giảm 6% hôm nay nhưng dòng tiền tổ chức tăng mua → bullish ngắn hạn có lý
- Mã tăng kịch trần nhưng cycle nợ xấu mới hiện hữu → bearish cảnh báo đỉnh

Verdict mẫu contrarian:
> "Ngược với phản ứng thị trường hôm nay, VHM vẫn tích cực dài hạn..."

### Mood-sync minimal — data source resolved

Inject `price_today` + `pct_change_today` + `volume_ratio_3d` vào brief để Master AWARE opening — KHÔNG force stance follow.

**Source**: Step 1.5 Market Snapshot — `lib/stages/run_market_snapshot.py` (NEW Python helper ~30 LOC) gọi Finpath API `get_quote(ticker)` ngay sau Crawler. Output schema injected vào brief:

```json
{
  "ticker_market_data": {
    "price_today": 92500,
    "pct_change_today": -3.2,
    "volume_ratio_3d": 1.4,
    "fetched_at": "2026-05-11T14:32:00+07:00"
  }
}
```

**Soft fetch semantics**: nếu Finpath API fail / ticker missing / timeout → brief proceeds without `ticker_market_data` field. Format Director defaults `tone_bias: neutral`. V5 Contrarian degrades to prose-only guidance for that run (Master can still write contrarian từ data, just không có market mood context).

Đây không phải hot-ticker trigger full (Subsystem A defer) — chỉ là **inline lightweight fetch** sau Crawler đã có ticker. Subsystem A khác ở chỗ: auto-discover top movers + auto-trigger pipeline; Subsystem này chỉ enrich existing pipeline run.

### Bullet pool (technique, not enforced strict)
Master sử dụng đa dạng 4 loại bullet:
- **Contrast** (>< nhưng): "**Big4 +28%, tư nhân -5%** — nhưng 2 hướng cùng có lý."
- **Causation** (vì vậy): "**CASA giảm xuống 35%** — vì vậy NIM 2026 sẽ phải xuống theo."
- **Warning** (coi chừng): "**Nợ xấu nhóm 2 vượt 2,4%** — coi chừng pattern 2022 lặp lại."
- **Revelation** (thật ra): "**Lãi 3.842 tỷ trông đẹp** — thật ra chỉ FE Credit kéo, core bank đi ngang."

Mỗi bài KHÔNG bắt buộc đủ 4 loại nhưng nên có ≥2 loại khác nhau.

## 7. 9 Gates V5.0 specification

| # | Gate | Type | Rule |
|---|---|---|---|
| 1 | no_english_jargon | Universal | 0% từ tiếng Anh trong body (giữ exception V4.0: tên riêng + pipeline log internal). |
| 2 | word_count | Per-format | flash_qa: 100-150 / standard_qa: 200-300 / standard_listicle: 250-350 / standard_narrative: 250-350 |
| 3 | body_pattern | Per-format | flash_qa: paragraph only NO bullet / standard_qa: opening ≥30 + 3-6 bullets each ≥20 từ + closing / standard_listicle: opening ≤30 + 4-7 bullets each ≥25 từ + closing ngắn / standard_narrative: opening ≥40 + flow paragraphs + 0-2 bullet highlight + closing |
| 4 | title_pattern | Per-format | flash_qa: MUST `?` / standard_qa: `?` HOẶC `—` + tension word / standard_listicle: declarative numbered / standard_narrative: declarative story |
| 5 | no_metadata_leak | Universal | KHÔNG `strategic-shift`, `risk_highlight`, `insight_type`, `Critique angle`, 5-category enum, format_id leak vào body đọc. |
| 6 | no_hedging (NEW) | Universal | Reject "có thể", "tùy thuộc", "vẫn chờ", "khả năng cao", "đáng theo dõi", "nhiều khả năng", "chưa rõ". |
| 7 | verdict_line (NEW) | Universal | Closing có 3 yếu tố: hướng + khung TG + action cho NĐT ĐANG cầm. |
| 8 | stance_consistency (NEW) | Universal | Master viết bám stance brief. Reject nếu brief=bearish nhưng article tone bullish (hoặc vice versa). |
| 9 | sentence_density (NEW) | Universal | ≥80% câu trong body có ≥1 trong 6 element: số / tên riêng / comparative / time marker / mechanism word / action verb. Banned pure-fluff: "Đây là điều cần lưu ý", "Cần theo dõi sát sao". |

### Implementation — `lib/gate_checker.py` (NEW module)

```python
@dataclass
class GateResult:
    gate_id: str
    passed: bool
    reason: str | None

def check_all_gates(article: ArticleDraft, format_id: str, stance: str) -> list[GateResult]:
    universal = [
        check_no_english_jargon(article),
        check_no_metadata_leak(article),
        check_no_hedging(article),
        check_verdict_line(article),
        check_stance_consistency(article, stance),
        check_sentence_density(article),
    ]
    per_format_checker = FORMAT_GATE_REGISTRY[format_id]
    per_format = per_format_checker(article)  # returns 3 results: word_count, body_pattern, title_pattern
    return universal + per_format
```

`FORMAT_GATE_REGISTRY: dict[str, Callable]` — registry pattern parallel với `data/format_registry.yaml`. Add format mới chỉ cần thêm gate function + registry entry.

### 7.1 Gates 7 + 8 — Hybrid enforcement detail (semantic gates)

Verdict_line (Gate 7) và stance_consistency (Gate 8) không enforce 100% bằng regex (semantic), do đó implement **2-layer hybrid**:

#### Gate 7 — verdict_line

**Layer 1 — Regex catch obvious (hard reject in `lib/gate_checker.py`)**:

```python
DIRECTION_KEYWORDS = r"(tích cực|tiêu cực|cảnh báo|đáng giữ|đáng chú ý|rủi ro|cơ hội|nên giữ|nên chờ|nên thận trọng|tăng trưởng dài hạn|đỉnh ngắn hạn|đáng lo|không nên cắt)"
TIMEFRAME_KEYWORDS = r"(12 tháng|18 tháng|6 tháng|3 tháng|Q[1-4](/\d{4})?|năm \d{4}|ngắn hạn|trung hạn|dài hạn|trung-dài hạn)"
HOLDER_ACTION_KEYWORDS = r"(NĐT|nhà đầu tư|người giữ|người cầm|đang cầm|đang giữ).{0,30}(giữ|chờ|tích lũy|thận trọng|cắt|không nên|nên)"

def check_verdict_line(article: ArticleDraft) -> GateResult:
    closing = extract_closing_paragraphs(article.body, n_last=2)
    checks = {
        "direction": bool(re.search(DIRECTION_KEYWORDS, closing, re.IGNORECASE)),
        "timeframe": bool(re.search(TIMEFRAME_KEYWORDS, closing, re.IGNORECASE)),
        "action_for_holder": bool(re.search(HOLDER_ACTION_KEYWORDS, closing, re.IGNORECASE)),
    }
    missing = [k for k, v in checks.items() if not v]
    return GateResult(
        gate_id="verdict_line",
        passed=(len(missing) == 0),
        reason=f"Missing verdict elements: {missing}" if missing else None,
    )
```

**Layer 2 — Skeptic critique angle `verdict_weak`**:
Skeptic flag nếu Layer 1 pass nhưng verdict thực chất ba phải / hedging trá hình. Vd "Cần thận trọng nhưng vẫn có thể tích lũy" — pass Layer 1 (regex thấy direction + action) nhưng mâu thuẫn nội tại.

#### Gate 8 — stance_consistency

**Layer 1 — Regex keyword ratio (hard reject)**:

```python
BULLISH_TERMS = {
    "tăng trưởng", "tích cực", "đáng giữ", "đáng chú ý", "cơ hội",
    "tốt", "mạnh", "ổn định", "lợi thế", "phòng thủ thành công",
    "buffer tích lũy", "cao hơn", "vượt", "lấn", "ngon", "tăng mua",
}
BEARISH_TERMS = {
    "rủi ro", "cảnh báo", "yếu", "lỗ", "giảm",
    "đỉnh ngắn hạn", "không nên", "đáng lo", "đe dọa", "căng thẳng",
    "tiêu cực", "bùng phát", "lao dốc", "cẩn thận", "thận trọng",
}

def check_stance_consistency(article: ArticleDraft, stance: str) -> GateResult:
    body_lower = article.body.lower()
    bullish_count = sum(1 for t in BULLISH_TERMS if t in body_lower)
    bearish_count = sum(1 for t in BEARISH_TERMS if t in body_lower)
    total = bullish_count + bearish_count
    if total == 0:
        return GateResult(
            gate_id="stance_consistency", passed=False,
            reason="Article has no stance keywords (lifeless)",
        )
    bull_ratio = bullish_count / total
    if stance == "bullish" and bull_ratio < 0.5:
        return GateResult(gate_id="stance_consistency", passed=False,
            reason=f"Brief=bullish but body tone bearish ({bullish_count} bull vs {bearish_count} bear)")
    if stance == "bearish" and bull_ratio > 0.5:
        return GateResult(gate_id="stance_consistency", passed=False,
            reason=f"Brief=bearish but body tone bullish ({bullish_count} bull vs {bearish_count} bear)")
    if stance == "divergent" and (bull_ratio < 0.3 or bull_ratio > 0.7):
        return GateResult(gate_id="stance_consistency", passed=False,
            reason=f"Brief=divergent but body one-sided (ratio {bull_ratio:.0%} bullish)")
    return GateResult(gate_id="stance_consistency", passed=True, reason=None)
```

**Layer 2 — Skeptic critique angle `stance_drift`**:
Skeptic compare `brief.stance` với executed tone of article subtly (e.g., bullish brief nhưng article hedge bằng caveat dồn dập). Flag drift even when Layer 1 ratio test passes.

**Tuning note**: BULLISH_TERMS + BEARISH_TERMS lexicon là heuristic ban đầu — sau khi production data đủ (10+ bài per stance), reassess + tune weights. Initial threshold `bull_ratio < 0.5` cũng có thể adjust (vd `< 0.4` softer reject).

## 8. Format Director Agent — design

### File: `.claude/agents/newsroom-format-director.md` (NEW)

**Model**: Claude Sonnet 4.6
**Role**: Pick format_id per deep_question_option in brief, enrich brief with format metadata.

### Input

```json
{
  "brief": {
    "ticker": "VCB",
    "sector": "Bank",
    "deep_question_options": [
      {
        "question": "Vì sao to nhất lại đi chậm nhất?",
        "category": "paradox",
        "stance": "bullish",
        "narrative_setup": "Q1/2026 VCB LNTT 11.218 tỷ +1,3%...",
        "data_trail_preview": [...]
      },
      ...
    ]
  },
  "ticker_market_data": {
    "price_today": 92500,
    "pct_change_today": -3.2,
    "volume_ratio_3d": 1.4
  },
  "format_registry": [...]  // loaded from data/format_registry.yaml
}
```

### Logic — 5-step flow (deterministic + light judgment)

**FOREACH `deep_question_option`:**

**Step 1 — Category → candidate formats (filter):**
- `paradox` → `[standard_qa]`
- `why_now` → `[standard_qa]`
- `hidden_mechanism` → `[standard_qa, standard_narrative]` ← multi-candidate
- `comparison_deep` → `[standard_listicle]`
- `early_signal` → `[standard_listicle]`
- (factual single Q, không match 5 category) → `[flash_qa]`

**Step 2 — Tie-breaking (chỉ chạy khi >1 candidate):**

Hidden_mechanism case duy nhất:
- IF `narrative_setup` chứa ≥3 timeline marker ("Q1/2025", "2024", "tháng 5", "cuối năm") → `standard_narrative`
- ELSE → `standard_qa`

**Step 3 — Length-tier downgrade:**
- IF `data_trail_preview` ≤ 2 sources AND chỉ số chính trong narrative ≤ 1 → downgrade `standard_*` → `flash_qa`
- ELSE keep standard tier
- Rationale: bài nông không ép dài → fluff

**Step 4 — Tone bias (KHÔNG đổi format, chỉ tag hint):**
- IF `|pct_change_today| > 3%` AND direction=red → `tone_bias: "acknowledge_market_red"`
- IF `|pct_change_today| > 3%` AND direction=green → `tone_bias: "acknowledge_market_green"`
- ELSE → `tone_bias: "neutral"`

**Step 5 — Length target (mid-range):**
- flash_qa: 130
- standard_qa: 250
- standard_listicle: 300
- standard_narrative: 300

### Output

```json
{
  "brief_enriched": {
    "ticker": "VCB",
    "deep_question_options": [
      {
        "question": "Vì sao to nhất lại đi chậm nhất?",
        "category": "paradox",
        "stance": "bullish",
        "narrative_setup": "...",
        "data_trail_preview": [...],
        // ENRICHMENT FIELDS:
        "format_id": "standard_qa",
        "format_reason": "Category=paradox → candidate=[standard_qa]. Length target: 250.",
        "tone_bias": "acknowledge_market_red",
        "length_target": 250
      },
      ...
    ]
  },
  "format_director_log": {
    "candidates_considered_per_option": [
      {"option_idx": 0, "category": "paradox", "candidates": ["standard_qa"]},
      {"option_idx": 1, "category": "hidden_mechanism", "candidates": ["standard_qa", "standard_narrative"], "tie_break_reason": "narrative_setup contains 4 timeline markers → pick standard_narrative"}
    ],
    "variety_check": {
      "recent_3_articles_same_ticker_formats": ["standard_qa", "standard_qa", "standard_listicle"],
      "current_pick_diversity_warning": false
    },
    "ticker_market_data_used": true
  }
}
```

### Anti-hallucination guards

1. **Structured JSON output ONLY** — no free prose
2. **`format_id` validation**: MUST be in `format_registry` IDs. Code-level check, reject invalid output.
3. **`format_reason` template-filled** (not free-write):
   ```
   "Category={X} → candidates={Y}. Tie-break: {Z if applicable}. Downgrade: {W if applicable}. Length target: {N}."
   ```
4. **Fallback default**: nếu agent confused / output không parse được → fallback `format_id = standard_qa` (safest middle ground). Log fallback in `format_director_log`.
5. **5-step flowchart explicit trong agent prompt** — agent follow flowchart, không "sáng tạo step mới".

### Variety guard (anti-self-bias)

- Query `recent_generated_news(ticker, limit=3)` từ `lib/pipeline_db.py`
- Extract `format_id` từ pipeline_log của 3 bài gần nhất
- IF cả 3 cùng format → set `current_pick_diversity_warning: true` trong log + prompt agent "consider alternative if data supports"
- KHÔNG hard reject (vì data có thể justify cùng format)

## 9. Format Registry — file structure

### File: `data/format_registry.yaml` (NEW)

```yaml
formats:
  flash_qa:
    length_range: [100, 150]
    length_target: 130
    structure: paragraph_only
    bullets_count: [0, 0]
    bullet_min_length: 0
    title_pattern: question
    title_must_contain: ["?"]
    tags: [factual, short]
    trigger_categories: []  # fallback when factual single Q, not in 5 deep_question category

  standard_qa:
    length_range: [200, 300]
    length_target: 250
    structure: opening_bullets_closing
    opening_min: 30
    opening_max: 80
    bullets_count: [3, 6]
    bullet_min_length: 20
    title_pattern: question_or_paradox
    title_must_contain_one_of: ["?", "—"]
    title_tension_words: ["hy sinh", "đánh đổi", "nghịch lý", "vì sao", "đổi lấy", "không phải", "bù lại", "thay vì", "chấp nhận"]
    tags: [insight, paradox]
    trigger_categories: [paradox, why_now, hidden_mechanism]

  standard_listicle:
    length_range: [250, 350]
    length_target: 300
    structure: short_opening_dense_bullets
    opening_max: 30
    bullets_count: [4, 7]
    bullet_min_length: 25
    title_pattern: numbered_declarative
    title_must_match_regex: "^(\\d+|[Mm]ột|[Hh]ai|[Bb]a|[Bb][ốố]n|[Nn][ăă]m)\\s+"  # số đầu title
    tags: [comparison, signals]
    trigger_categories: [comparison_deep, early_signal]

  standard_narrative:
    length_range: [250, 350]
    length_target: 300
    structure: flow_paragraphs
    opening_min: 40
    bullets_count: [0, 2]
    bullet_min_length: 20  # if bullet present
    title_pattern: declarative_story
    title_must_contain: ["—"]  # narrative bao giờ cũng có em dash chia 2 vế
    tags: [mechanism, time_flow]
    trigger_categories: [hidden_mechanism]  # alt to standard_qa
    tie_break_signal: narrative_timeline_markers  # ≥3 timeline markers → pick này
```

### Loader: `lib/format_registry.py` (NEW)

```python
import yaml
from pathlib import Path

REGISTRY_PATH = Path("data/format_registry.yaml")

def load_registry() -> dict:
    return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))["formats"]

def get_format(format_id: str) -> dict:
    return load_registry()[format_id]

def get_candidates_for_category(category: str) -> list[str]:
    return [fid for fid, f in load_registry().items() if category in f.get("trigger_categories", [])]
```

## 10. Brief V5.0 schema

### Migration V4.0 → V5.0

| V4.0 field | V5.0 field | Change |
|---|---|---|
| `deep_question_options[].question` | unchanged | — |
| `deep_question_options[].category` | unchanged | — |
| `deep_question_options[].narrative_setup` | unchanged | — |
| `deep_question_options[].data_trail_preview` | unchanged | — |
| — | `deep_question_options[].stance` | NEW required (V1 rule) |
| — | `deep_question_options[].format_id` | NEW required (Format Director enriches) |
| — | `deep_question_options[].format_reason` | NEW required |
| — | `deep_question_options[].tone_bias` | NEW required |
| — | `deep_question_options[].length_target` | NEW required |
| — | `ticker_market_data` | NEW optional — inject when available |

### Persist: `pipeline_log.step_3_5_format_director`

New schema validation in `lib/pipeline_db.py`:

```python
_STEP_3_5_REQUIRED = {
    "format_picks": list,  # array of {option_idx, format_id, format_reason, tone_bias, length_target}
    "candidates_considered_per_option": list,
    "variety_check": dict,
    "model": str,
    "duration_ms": int,
}
_NON_EMPTY_FIELDS["step_3_5_format_director"] = {"format_picks"}
```

### Persist: `pipeline_log.step_4_master` (extended)

Add field `format_id_used` để Skeptic + render đọc:

```python
_STEP_4_REQUIRED["format_id_used"] = str  # NEW required in V5.0
```

### 10.1 Pipeline version column + migration

Add column `pipeline_version` vào `generated_news` table:

```sql
ALTER TABLE generated_news ADD COLUMN pipeline_version TEXT NOT NULL DEFAULT 'V4.0';
```

Migration semantics:
- **Existing rows (legacy V4.0)**: keep `pipeline_version = 'V4.0'` via DEFAULT
- **New rows (V5.0)**: insert với explicit `pipeline_version = 'V5.0'` in `lib/pipeline_db.py:insert_generated_news`
- **`validate_pipeline_step` becomes version-aware** — only enforce V5.0 schema (step_3_5, format_id_used) when row's `pipeline_version >= 'V5.0'`:

```python
def validate_pipeline_step(step_key: str, payload: dict, pipeline_version: str = "V4.0") -> None:
    """Validate per pipeline_version. V4.0 baseline always enforced (step_4_master + step_5_skeptic).
    V5.0 adds step_3_5_format_director + step_4_master.format_id_used.
    """
    # Always-validated steps (V4.0 baseline schema)
    required_map = {
        "step_4_master": _STEP_4_REQUIRED_V4,  # without format_id_used
        "step_5_skeptic": _STEP_5_REQUIRED,
    }
    # V5.0 schema additions (only when row is V5.0)
    if _version_ge(pipeline_version, "V5.0"):
        required_map["step_3_5_format_director"] = _STEP_3_5_REQUIRED
        required_map["step_4_master"] = _STEP_4_REQUIRED_V5  # adds format_id_used
    required = required_map.get(step_key)
    # ... (rest same as before)
```

Callers of `log_pipeline_step` + `insert_generated_news` MUST pass `pipeline_version` from the row (default `'V4.0'` for back-compat).

**Frontend `FormatPickPanel.tsx` graceful degrade**: hide entire panel nếu:
- `pipeline_log.step_3_5_format_director` field missing, OR
- Article frontmatter `pipeline_version < V5.0`

Legacy V4.0 articles continue rendering without format panel.

## 11. Master agents impact

### File touch: `.claude/agents/newsroom-master-{bank,ck,bds}.md`

**Changes**:
1. Receive `format_id` from brief → load format spec from `data/format_registry.yaml`
2. Apply pattern theo format (paragraph_only / opening_bullets_closing / etc.)
3. Run 9-gate check after draft via `lib/gate_checker.py:check_all_gates(article, format_id, stance)`
4. If any gate fails → reject + rewrite (max 2 retry per format, then escalate)
5. Persist `step_4_master.format_id_used = <final_format_id>` (post-escalation if applicable)
6. Bullet pool guidance: prose section "Bullet types pool" với 4 examples + recommendation "≥2 loại khác trong 1 bài"
7. **Format escalation rule (one-shot, length-only)**:
   - Master CAN upgrade `flash_qa → standard_qa` post-fetch IF `data_trail` (full, post-fetch) has ≥3 sources AND chỉ số chính ≥2 (vs Format Director's preview-based pick được dựa trên `data_trail_preview` từ Story Editor).
   - Master CANNOT cross-tier swap (vd `standard_qa → standard_narrative` or `standard_listicle → standard_qa`) — structural decision của Format Director is final.
   - Master log `format_escalation: {from: "flash_qa", to: "standard_qa", reason: "data_trail=4 sources, key_metrics=3"}` trong `step_4_master.format_escalation_reason` (optional field — null nếu không escalate).
   - Pipeline KHÔNG re-dispatch Format Director (avoid 2nd subagent call, simplicity).

### Conflict resolution với CLAUDE.md hard rules

CLAUDE.md hiện có:
- "Body pattern V4.0: 1 opening + 3-7 bullets + 1 closing. KHÔNG `## Cần để ý` section."

V5.0 update: pattern PER FORMAT. CLAUDE.md sẽ cần update sau khi spec approved (tracked in plan task).

## 12. Skeptic agent impact

### File touch: `.claude/agents/newsroom-skeptic.md`

**Changes**:
1. Read `step_4_master.format_id_used` từ DB → understand context
2. Adjust critique expectations per format:
   - flash_qa: KHÔNG critique "thiếu bullet" (flash không có bullet)
   - standard_narrative: KHÔNG critique "ít bullet" (narrative ít cố ý)
3. NEW critique angles (3):
   - `lifeless_writing` — flag nếu có ≥2 fluff sentence (sentence_density gate catch hard, Skeptic flag soft cho border-line case)
   - `verdict_weak` — Layer 2 cho Gate 7: flag verdict mâu thuẫn nội tại / hedging trá hình that pass regex
   - `stance_drift` — Layer 2 cho Gate 8: flag subtle stance drift even when keyword ratio passes
4. **9 critique angles total** (V4.0 = 6): + `lifeless_writing`, `verdict_weak`, `stance_drift`
5. CLAUDE.md section "## 6 Critique Angles (Skeptic)" → "## 9 Critique Angles (Skeptic)" cần update (in file touch list §15).

## 13. Pipeline observability impact

### File touch: `lib/render_compare_feed.py`

Add right column section:
```
## Format chọn
- Format: standard_qa
- Lý do: Category=paradox → candidate=[standard_qa]. Length: 250.
- Tone bias: neutral
- Variety check: ✅ (3 bài gần đây: 2 standard_qa, 1 standard_listicle)
```

### File touch: `web/src/components/` — new `FormatPickPanel.tsx`

Render `step_3_5_format_director` block trong right column feed viewer. Component:
- Format ID + badge color theo type
- Format reason (1 line)
- Tone bias + variety warning if applicable
- Candidates considered (collapsible details)

## 14. Pipeline version bump V4.0 → V5.0

`pipeline_version` frontmatter trong output markdown: `V4.0` → `V5.0`. Updated touch points:

- `lib/render_compare_feed.py` default value
- `lib/pipeline_db.py` module comments + ValueError messages
- All agent .md V4.0 references
- All skill SKILL.md references
- `CLAUDE.md` extensive V4.0 → V5.0 references
- Test files

Legacy articles (V4.0 frontmatter) vẫn parse được — viewer aware version field.

## 15. File touch list (final)

| File | Action | Lines est |
|---|---|---|
| `data/format_registry.yaml` | NEW | ~70 |
| `lib/format_registry.py` | NEW | ~40 |
| `lib/stages/run_market_snapshot.py` | NEW | ~30 |
| `lib/gate_checker.py` | NEW | ~280 |
| `.claude/agents/newsroom-format-director.md` | NEW | ~250 |
| `.claude/skills/finpath-newsroom-format-director/SKILL.md` | NEW | ~180 |
| `.claude/agents/newsroom-pipeline.md` | MODIFY | +60 lines (insert step 3.5) |
| `.claude/agents/newsroom-story-editor.md` | MODIFY | +20 lines (add `stance` field, remove format hint if any) |
| `.claude/agents/newsroom-master-bank.md` | MODIFY | +80 lines (format-aware) |
| `.claude/agents/newsroom-master-ck.md` | MODIFY | +80 lines |
| `.claude/agents/newsroom-master-bds.md` | MODIFY | +80 lines |
| `.claude/agents/newsroom-skeptic.md` | MODIFY | +30 lines (format-aware critique + lifeless_writing angle) |
| `lib/pipeline_db.py` | MODIFY | +60 lines (step_3_5 schema, step_4 format_id_used, version-gate validation, pipeline_version column) |
| `lib/schema.sql` (or equivalent) | MODIFY | +1 ALTER TABLE for pipeline_version column |
| `lib/render_compare_feed.py` | MODIFY | +40 lines (format pick render) |
| `web/src/components/FormatPickPanel.tsx` | NEW | ~80 |
| `web/src/types/index.ts` | MODIFY | +10 lines (format pick types) |
| `CLAUDE.md` | MODIFY | sections: "5 Quality Gates V4.0" → "9 Quality Gates V5.0", "Body pattern V4.0" → per-format patterns, "6 Critique Angles (Skeptic)" → "9 Critique Angles", "Hard rules cho Master + Skeptic" extend với stance + verdict rules, all V4.0 → V5.0 |
| `tests/test_format_registry.py` | NEW | ~150 |
| `tests/test_format_picker_logic.py` | NEW | ~200 |
| `tests/test_gate_checker.py` | NEW | ~300 |
| `tests/test_pipeline_db.py` | MODIFY | +80 lines (step_3_5 validation, version-gate, V4.0 back-compat tests) |
| `tests/test_render_compare_feed.py` | MODIFY | +30 lines (format pick render test) |
| `tests/test_run_market_snapshot.py` | NEW | ~50 lines |

Total: ~14 modify + 7 new ≈ 1500-1800 new LOC.

## 16. Testing strategy

### Unit tests
- `test_format_registry.py`: load yaml, validate schema, get_format, get_candidates_for_category
- `test_format_picker_logic.py`: 5-step flow test cases per category, tie-break logic, length downgrade, tone bias
- `test_gate_checker.py`: 9 gates each + per-format dispatch + integration (all 9 on real article samples)

### Integration tests
- Dispatch newsroom-format-director with fixture brief → verify output schema + format_id valid
- Full pipeline test: NVL → Story Editor → Format Director → Master → Skeptic with all stages dispatching real subagents (E2E)

### Visual verification
- Run `/tin VCB` after V5.0 → check feed viewer shows format pick panel + 4 format render correctly
- Compare 3 articles in 1 batch — verify variety (not all standard_qa)

## 17. Rollout

### Phase 1 — Foundation (Day 1-2)
- Format Registry yaml + loader + tests
- Gate checker module with 9 gates + tests
- Brief V5.0 schema in pipeline_db

### Phase 2 — Format Director agent (Day 3-4)
- Agent .md prose + skill SKILL.md
- 5-step logic implementation in Python helper (lib/format_picker_logic.py — used in agent prompt as reference)
- Anti-hallu guards + fallback
- Integration with pipeline

### Phase 3 — Master + Skeptic update (Day 5-7)
- 3 Master agents apply format
- Skeptic aware format
- Bullet pool guidance
- 9-gate integration

### Phase 4 — Frontend + render (Day 8)
- FormatPickPanel.tsx component
- render_compare_feed format pick output
- Test 1 ticker E2E

### Phase 5 — CLAUDE.md + V4.0 → V5.0 (Day 9)
- Update CLAUDE.md project instructions
- Bump pipeline_version frontmatter default
- Migration note for legacy V4.0 articles

### Phase 6 — Verification (Day 10)
- Run /tin for all 3 sectors (VCB Bank / SSI CK / VHM BĐS)
- Verify each batch produces variety (≥2 different formats)
- Compare against V4.0 baseline articles — measure improvement

## 18. Open questions / deferred

1. **Mood-sync FULL trigger Subsystem A** — separate spec when auto top-mover discovery + auto-pipeline trigger needed. (Mood-sync minimal: RESOLVED via Step 1.5 Market Snapshot, §6.)
2. **Headline craft separate agent Subsystem C** — defer. Format Director per-format title_pattern đã cover. Nếu sếp still chê title, escalate sang dedicated agent.
3. **Pipeline observability dedicated agent Subsystem D** — defer. Format Director logging tự đảm bảo độ chi tiết step 3.5. Subsystem D có thể cover global logging cross-step.
4. **Bullet pool enforcement strict** — chưa quyết hard rule. Currently soft guidance. Reassess sau khi run 10+ bài.
5. **Length downgrade threshold** — `data_trail_preview ≤ 2 sources AND chỉ số chính ≤ 1` là heuristic. Tune sau khi production data.
6. **Variety check window** — hiện 3 bài gần nhất. Có thể tune (5/7) sau.
7. **Author persona per sector** — REMOVED khỏi spec (user concern dập khuôn dạng mới). Nếu sau này feedback "thiếu personality" → reopen với multi-persona rotation thay fix cứng.
8. **Stance keyword lexicon tuning** — initial BULLISH_TERMS/BEARISH_TERMS heuristic. Reassess + tune weights sau 10+ bài per stance.
9. **Verdict regex thresholds** — currently 3/3 required. Có thể relax 2/3 sau pilot nếu reject rate cao.
10. **Sentence-split heuristic for Gate 9** — using `re.split(r'[.!?]\s+', body)` baseline. Edge cases (Vietnamese punctuation, abbreviations vd "Q1.") need tuning post-launch.

### Resolved by spec patch (advisor review 2026-05-11)
- ~~Item: Mood-sync source~~ → RESOLVED §6 + §4 (Step 1.5 Market Snapshot)
- ~~Item: V4.0 migration path~~ → RESOLVED §10.1 (pipeline_version column + version-gate validation)
- ~~Item: Gates 7+8 enforceability~~ → RESOLVED §7.1 (hybrid 2-layer: regex Layer 1 + Skeptic Layer 2)
- ~~Item: Format pre-pick timing~~ → RESOLVED §11 item 7 (Master one-shot length-only escalation)

## 19. Spec changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-05-11 | Initial draft from brainstorming session. |
| 1.1 | 2026-05-11 | Advisor review patches: §6 mood-sync source (Step 1.5 Market Snapshot), §7.1 hybrid gate enforcement for Gates 7+8, §10.1 pipeline_version column + version-gate validation migration, §11 Master format escalation rule (one-shot length-only), §12 Skeptic 9 angles (+ verdict_weak, stance_drift), §14 frontend graceful degrade, §15 file touch list updates. |
