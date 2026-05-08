# Newsroom V4.0 — Redesign Spec

- **Date**: 2026-05-08
- **Status**: Draft for review
- **Predecessor**: V3.6 (in `docs/superpowers/specs/2026-05-08-newsroom-cli-migration-design.md`)
- **Trigger**: User feedback sau /tin TCB run đầu tiên — bài "liệt kê data, không có insight cụ thể"

---

## 1. Problem Statement

Bài V3.6 chạy trên TCB cho ra format đúng 5 quality gates nhưng "ai chả nói được" — đúng warning sếp đã raise ở Newsroom V2 Direction page (Notion 357273c7-a9a1-8135-8b99-defb7a16cd1a).

**Reference articles user accept:**
- "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?" (Notion 359273c7-a9a1-81d4-b7b2-eed4e66fbd54)
- "VCB target 2026 chỉ +5%: Vì sao ngân hàng to nhất lại đi chậm nhất?" (Notion 359273c7-a9a1-81fd-bbf7-c3e9f3998f74)

Title = HOOK (question hoặc declarative paradox), body có luận điểm, không liệt kê.

**Reference principle (V2 Direction):**
> Các tin truyền thống đăng "TCB chia cổ tức 67%, tăng vốn 113.738 tỷ, rút bất động sản dưới 30%" — đó là **liệt kê sự kiện**.
> Tổng biên tập của ta đặt câu hỏi: "**Vì sao 2 quyết định ngược chiều xảy ra cùng lúc?**" — đây là **câu hỏi đào sâu**. Phóng viên buộc phải tìm 4-5 lý do thật giải thích, không thể né bằng cách liệt kê facts.

---

## 2. 9 Changes V4.0

### Change 1 — Story Editor outputs 2-3 deep_question OPTIONS

**Reasoning**: Editorial transparency — sếp đọc cột phải thấy Story Editor đề xuất 3 hướng, Master chọn 1 với lý do. Đó là editorial judgment thật.

**Schema brief V4.0** (replaces V3.6 single deep_question):

```yaml
brief_v4:
  # Narrative fields (user-readable Vietnamese, written by Story Editor directly)
  why_chosen_narrative: |
    3-5 câu narrative — vì sao chọn bài này. Nhắc tới yếu tố hiếm + paradox + 
    timing + data foundation. KHÔNG enum, KHÔNG technical jargon.
  
  angle_label: "Tag ngắn — vd 'Đánh đổi chủ động — chuyển hướng chiến lược'"
  
  angle_narrative: |
    2-3 câu — bài đi theo hướng nào, tại sao. Ví dụ: "Bài đi theo hướng 
    nghịch lý — TCB cùng lúc làm 2 hành động ngược chiều: chia cổ tức kỷ lục 
    + rút BĐS dưới 30%. Đào sâu cơ chế đằng sau."
  
  source_rationale: "1-2 câu — vì sao chọn nguồn này trong batch"
  
  # Multi-option questions (NEW)
  deep_question_options:
    - question: "Vì sao 2 quyết định ngược chiều xảy ra cùng lúc?"
      category: paradox
      pick_hint: "Có quote CEO mạnh + 2 hành động đối lập rõ"
    - question: "Vì sao bây giờ là thời điểm rút BĐS, không phải 2023?"
      category: why_now
      pick_hint: "Timing với khủng hoảng BĐS 2022-23, dễ liên hệ Vạn Thịnh Phát"
    - question: "TCB hy sinh 5.000 tỷ/năm — phép tính nào ra con số đó?"
      category: hidden_mechanism
      pick_hint: "Cần report nội bộ TCB, web search có thể fail"
  
  insight_hypothesis: "1 câu specific Master verify với data"
  memory_check: { passed: bool, recent_angles: [...] }
```

**Removed từ V3.6**: `data_spec`, `data_anchor`, `angle_alternatives`, single `deep_question` field.

**Master output additions** (Master picks 1 option):

```yaml
master_v4:
  # Existing
  title, body, word_count, key_view, insight_final, accepted_hypothesis, ...
  
  # NEW — pick reasoning persisted explicitly per question
  chosen_question_idx: 0   # index in deep_question_options
  chosen_pick_reason: "Câu 1 (paradox) có quote CEO mạnh + 2 hành động đối lập rõ..."
  skip_reasons:            # dict — explicit per skipped option (advisor recommendation)
    1: "Timing argument cần data mechanism BĐS 2022-23 mà brief không có anchor"
    2: "Cần report nội bộ TCB không công khai — risk web search miss"
  
  # NEW — data trail per source (Step 4 transparency)
  data_trail:
    - source: "WebFetch [Báo Pháp luật](url)"
      fetched: "Quote CEO Lottner: 'ngân hàng hy sinh khoảng 5.000 tỷ lợi nhuận tiềm năng/năm'"
      used_for: "Bullet 1 — anchor quote, chứng minh CEO công khai trade-off"
    - source: "Finpath API /bankfinancialratios/TCB"
      fetched: "Q1/2026 BĐS ratio = 28.9% (Q4/2025 = 30.1%)"
      used_for: "Bullet 2 — verify milestone 'lần đầu < 30%'"
    - source: "KB/frameworks/bank-target-vs-actual-pattern.md"
      fetched: "Pattern under-promise over-deliver"
      used_for: "Closing insight phân loại NĐT giá trị"
```

### Change 2 — Body Pattern V4.0 + 5 Quality Gates

**Pattern visualized:**

```
[Title hook — question hoặc declarative paradox]

[Opening paragraph 30-60 từ — sự kiện + tension setup HOẶC câu hỏi]

- **Bold highlight 1**: bullet ≥20 từ giải thích mechanism với connector
- **Bold highlight 2**: bullet ≥20 từ
- **Bold highlight 3**: bullet ≥20 từ
- ... up to 7 bullets

[Closing — 1 câu phân loại NĐT phù hợp]
```

**Drop từ V3.6**: `## Cần để ý` section entirely. Caveats compress into closing sentence hoặc inline trong bullets.

**Opening paragraph** can end với question/tension marker (advisor item b — confirmed). Vd:
> "Đại hội đồng cổ đông Techcombank 25/4 thông qua chia cổ tức tổng tỷ lệ 67% — nhưng câu chuyện thật là chiến lược ngược chiều thị trường."

**5 Gates V4.0** (replace V3.6 gates):

| # | Gate | Mechanical check |
|---|---|---|
| 1 | 0% từ tiếng Anh | Same V3.6 — `lib/quality_gates.py` `check_no_english_jargon` |
| 2 | Word count 200-400 | Same V3.6 |
| 3 | **Body pattern** | 1 opening paragraph (≥30 từ, no bullet) + 3-7 bullets (each ≥20 từ + ≥1 bold) + 1 closing sentence (no bullet, no heading). KHÔNG `## Cần để ý` heading. |
| 4 | **Title-as-hook** (NEW) | Title chứa `?` HOẶC `—` + ≥1 tension word: `hy sinh`, `đánh đổi`, `nghịch lý`, `vì sao`, `đổi lấy`, `không phải`, `bù lại`, `thay vì`, `chấp nhận` |
| 5 | No metadata leak | Same V3.6 — `check_no_metadata_leak` |

**Drop từ V3.6**: gate 3 mechanism count (3-7 bullets) → replaced by structural pattern. Gate 4 "Cần để ý" narrative → dropped.

### Change 3 — Bullet Substance Examples in Master Skill (advisor #1)

Mechanical gate (≥20 từ + ≥1 bold) catches obvious failures nhưng KHÔNG enforce substance. Master skill MUST có concrete examples:

**Add to `.claude/skills/finpath-newsroom-master-bank/references/bullet-examples.md`:**

```markdown
# Bullet Substance Examples — V4.0

## ❌ Bad: data summary (passes mechanical gate, fails substance)

`**TCB Q1/2026 lãi 8.900 tỷ**: tăng 22,6% so cùng kỳ, cao nhất lịch sử quý 1.`
→ Đây là tóm tắt fact, không phải mechanism. ≥20 từ + bold đủ pass mechanical, 
  nhưng reader không học được "vì sao".

`**CASA 37,9%**: giảm từ đỉnh 40,4% cuối 2025, do chu kỳ Tết hết tiền.`
→ Có data + nguyên nhân, nhưng vẫn data-driven. Chưa connect với insight.

## ✅ Good: mechanism with paradox + contrastive

`**Cổ tức 67% tách thành hai phần khác bản chất**: 7% tiền mặt tương đương 
**4.960 tỷ đồng**, còn 60% là cổ phiếu thưởng phát hành từ lợi nhuận giữ lại — 
không rút đồng tiền mặt nào khỏi ngân hàng.`
→ Bold = keypoint paradox. Body unpacks "tách hai phần khác bản chất" → 
  reader hiểu cơ chế kế toán, không chỉ thấy "67% lớn".

`**Lần đầu trong lịch sử, BĐS giảm xuống 28,9%**: bán lẻ + SME tăng 33% so 
cùng kỳ, đạt 395 nghìn tỷ — bù vào chỗ trống. CEO Jens Lottner thừa nhận 
ngân hàng "hy sinh" khoảng **5.000 tỷ lợi nhuận tiềm năng/năm** so với cho 
vay phân khúc rủi ro cao, để duy trì 3 lớp phòng thủ thanh khoản.`
→ Bold = milestone + quote anchor. Bullet kết nối: BĐS giảm + bán lẻ tăng 
  + CEO admit trade-off + structural reason (3 layer phòng thủ). 4 facts 
  thành 1 luận điểm.

## Recipe cho 1 bullet substantive

1. Bold = keypoint paradox / milestone / contrastive (KHÔNG chỉ data point)
2. Body bullet kết nối 2-3 facts thành argument (không tóm tắt)
3. Có connector: `vì`, `do đó`, `đánh đổi`, `bù lại`, `nhưng`, `trong khi`, `thay vì`
4. Có data anchor cụ thể (số + đơn vị + so sánh)
5. Reader học được mechanism: quy định / phép tính / chu kỳ / cạnh tranh / customer behavior
```

Master prompt MUST include reference to this file: "Đọc `references/bullet-examples.md` TRƯỚC khi viết body."

### Change 4 — Compare Feed Right Column (8 sections)

```markdown
## 📰 Bài gốc
[Title gốc] — *Nguồn: [name](url) · Published DD/MM/YYYY*

## 🎯 Vì sao chọn bài này
[Story Editor.why_chosen_narrative — 3-5 câu user-readable]

## 🧭 Hướng tiếp cận
**[angle_label]** — [angle_narrative 2-3 câu]

## 🤔 Tổng biên tập đề xuất 3 câu hỏi đào sâu

1. **(✓ Đã chọn)** [question 1]
   *Phóng viên pick vì*: [chosen_pick_reason]
2. [question 2]
   *Skip vì*: [skip_reasons[1]]
3. [question 3]
   *Skip vì*: [skip_reasons[2]]

## 📊 Crawl funnel — đã quét N nguồn, gom M bài, chọn 1, loại K (click chi tiết)

✅ ĐÃ CHỌN (1)
• [Source name](url) (DD/MM/YYYY)
  Lý do chọn: [why anchor — narrative]

❌ KHÔNG CHỌN (K)
• [Source](url) (DD/MM/YYYY) — *Tổng biên tập bỏ*
  Vì sao bỏ: [narrative compare-vs-picked, 1-2 câu]
• [Source](url) (DD/MM/YYYY) — *Gác cổng bỏ*
  Vì sao bỏ: [narrative]
• [Source](url) (DD/MM/YYYY) — *Phóng viên bỏ*
  Vì sao bỏ: [narrative]

## 📋 Phóng viên đã tra ở đâu (Master data_trail)

→ [Source link/name](url)
   Tra được: [fetched data 1 line]
   Dùng cho: [used_for — bullet X / closing Y]

→ [Source 2]
   ...

## 🔍 Reviewer ngoài đã tra ở đâu (Skeptic data_trail)

→ [Source]
   Tra được: ...
   Dùng cho: counter-evidence cho [...]

## 📖 Đọc bài gốc
→ [External link to original article](url) — KHÔNG embed full content
```

**Reject agent labels** (mapping enum → vai trò Vietnamese):
- `editor_v1` → "Gác cổng bỏ"
- `story_editor` → "Tổng biên tập bỏ"
- `master` → "Phóng viên bỏ"

**Reject reasons** = narrative tiếng Việt thuần, KHÔNG enum (`dup_event`, `low_writeability`, etc.).

### Change 5 — IndexPage Card Format

```
🏦 TCB                                                400 từ · 08/05 10:23
"TCB chia cổ tức 67% kỷ lục — nhưng phần lớn không phải tiền mặt"
                                                    [hook = title]
```

Card structure:
- Sector icon + ticker badge (top-left)
- Word count + crawled_at (top-right, secondary text)
- **Hook (= title)**: prominent text, dòng dưới, ≥18px, bold

KHÔNG hiển thị: angle category, key_view chip, sector text. Chỉ ticker + hook + meta.

3 articles cùng batch = 3 cards riêng, sort by crawled_at desc, mixed với articles ticker khác.

### Change 6 — Multi-article Output File Naming

**Pattern**: `<TICKER>-<YYYYMMDD>-<HHMM>-<hook-slug>.md`

`hook-slug` = title hook slugified:
- Lowercase
- Strip Vietnamese diacritics (NFKD + remove combining)
- Replace non-alphanumeric với `-`
- Trim consecutive hyphens
- Truncate to 60 chars max
- Strip trailing partial words

**Examples**:
```
TCB-20260508-1023-chia-co-tuc-67-khong-phai-tien-mat.md
TCB-20260508-1023-doi-giay-lay-ngoi-vuong-von-dieu-le.md
TCB-20260508-1023-thu-phi-dich-vu-lap-dinh.md
VCB-20260508-1530-vi-sao-to-nhat-di-cham-nhat.md
```

**Collision handling**: 2 batches cùng ngày + slug giống → suffix `-2`, `-3`, etc.

**DB schema additions**:
- `generated_news.public_slug` TEXT NOT NULL UNIQUE — generated at persist time

**Manifest entry**:
```json
{
  "id": "TCB-20260508-1023-chia-co-tuc-67-khong-phai-tien-mat",
  "ticker": "TCB",
  "sector": "Bank",
  "title": "TCB chia cổ tức 67% kỷ lục — nhưng phần lớn không phải tiền mặt",
  "crawled_at": "...",
  "word_count": 400
}
```

URL: `/article/<id>` (= public_slug).

**Render flow update**: `lib/render_compare_feed.py` loops ALL anchor rows in batch (not first only). For each anchor + article, generate slug + write file + append manifest entry.

### Change 7 — KB Cleanup

Keep CHỈ 4 file Frameworks gốc:
```
kb/bank/frameworks/
├── bank-industry-master-reference.md
├── bank-npl-reading.md
├── bank-nim-cycle.md
└── bank-target-vs-actual-pattern.md
```

Delete 39 files khác:
- `kb/bank/history/` (10 files) — search web đúng hơn
- `kb/bank/per-ticker/` (21 files) — search web đúng hơn
- `kb/bank/frameworks/` 8 files không phải sub-page Frameworks gốc:
  - `bank-ceo-cfo-master-reference.md`
  - `banking-MA-Vietnam-Master-Reference.md`
  - `bank-MA-Master-Reference.md`
  - `research-reports-index.md`
  - `bank-research-reports-master-reference.md`
  - `research-VCBS-banking-2025.md`
  - (và 2 file khác từ Phase 3.5 sweep)

**Rationale**: KB role = "kiến thức chuyên sâu để giọng văn tự nhiên". 4 frameworks (NPL reading, NIM cycle, target patterns, master reference) đủ. Per-ticker / M&A / Research → search web bù được.

### Change 8 — Image #5 Raw Content: Link External Only

**Current bug** (Phase 1 sample): "Click đọc full bài viết gốc" toggle embed full body content (3000-5000 chars) inline.

**Fix V4.0**: Section "📖 Đọc bài gốc" chỉ là LINK ra bài external, KHÔNG embed content. 1 dòng:

```markdown
## 📖 Đọc bài gốc
→ [Báo Pháp luật — TCB ĐHĐCĐ 2026](url) (25/04/2026)
```

User click → external browser tab. Render layer KHÔNG fetch + embed raw content.

### Change 9 — Bug Fixes

**Bug #1 — Slash command `$1` not substituting**
- Root cause: `.claude/commands/tin.md` uses `$1` syntax. Claude Code may need `$ARGUMENTS` or other.
- Fix: change `$1` → `$ARGUMENTS` in command file. Test với `/tin TCB` → command body shows "TCB" not empty.

**Bug #2 — Skeptic article confusion** (advisor #2 fix)
- Root cause: agent loaded right article from DB (SQL filter strict), but reasoned about wrong content — likely skill content bleed or prompt confusion.
- **REAL fix** (NOT just SQL):
  1. Skeptic dispatch prompt MUST require: "Trước Pass 1, ECHO 30 ký tự đầu của body article đã load."
  2. Skeptic skill SKILL.md instruct: "Trước khi critique, quote title + 30 ký tự đầu body để verify đúng article. Nếu không match input article_id, ABORT."
- This catches loading errors before critique starts.

**Bug #3 — Multi-article render orphan** (Phase 4 bug)
- Root cause: `render_for_funnel_batch` picks first anchor only, renders 1 file/batch.
- Fix: loop ALL anchor rows in batch (filter `master_decision='write_article'`). For each anchor, query its `generated_news` row, render 1 file with slug derived from hook. Append entry to manifest.

---

## 3. Build Order V4.0

### Phase A — Spec + Code Schema Changes (1 day)

1. Update CLAUDE.md với V4.0 rules
2. Migrate SQLite schema: add `generated_news.public_slug` UNIQUE column
3. Update `lib/quality_gates.py`:
   - Drop `check_mechanism_count` + `check_can_de_y_narrative`
   - Add `check_body_pattern` (1 para + 3-7 bullets each ≥20 từ với ≥1 bold + 1 closing)
   - Add `check_title_as_hook` (regex `?` OR `—` + tension word list)
4. Update tests (add 8-10 new tests for V4.0 gates)

### Phase B — Skill Rewrite (1.5 day)

5. Update `finpath-newsroom-story-editor/SKILL.md`:
   - Brief schema V4.0 (narratives + 3 question options)
   - Output user-readable narratives directly (no enum-to-text translation needed)
6. Update `finpath-newsroom-master-bank/SKILL.md`:
   - 9-step workflow accepts brief V4.0
   - Master picks 1 of 3 deep_question options + log skip_reasons per other
   - Body pattern V4.0 (1 para + 3-7 bullets + closing)
   - Drop "Cần để ý" instruction
   - Add `references/bullet-examples.md` (Change 3 advisor #1)
7. Update `finpath-newsroom-skeptic/SKILL.md`:
   - Pass 1 verification protocol: ECHO title + 30 chars body before critique
   - Add data_trail output schema
   - Drop reference to `## Cần để ý` (no longer in Master output)
8. Delete 39 KB files (Change 7)

### Phase C — Agent Definitions Update (0.5 day)

9. Update `.claude/agents/newsroom-story-editor.md`: prompt force narrative output
10. Update `.claude/agents/newsroom-master-bank.md`: prompt force pick-question + skip_reasons + data_trail
11. Update `.claude/agents/newsroom-skeptic.md`: prompt force ECHO verification (advisor #2)
12. Fix `.claude/commands/tin.md`: `$1` → `$ARGUMENTS`

### Phase D — Render Layer Rewrite (≥2 days, advisor #3)

13. `lib/render_compare_feed.py` rewrite from ~200 → ~400-500 lines:
    - Loop all anchor rows in batch (multi-article fix)
    - Generate `public_slug` from hook
    - Build 8-section right column from brief_json + pipeline_log + crawl_log aggregate
    - Reject narrative formatter (vai trò labels)
    - Data trail formatter (per source link + fetched + used_for)
    - Manifest update per article
14. Update React `web/src/components/RightColumn.tsx`:
    - 8 sections (was 4)
    - Reject agent labels in funnel
    - Data trail expandable sections
    - Drop "click full bài viết gốc" embed → link only

### Phase E — Verification (0.5 day)

15. Run `/tin MBB` (fresh ticker, no Phase 4 baggage)
16. Verify 3 articles output, all pass 5 gates V4.0
17. Visual check viewer — 8 sections render correctly, hook clickable
18. Manual sanity: bài có "luận điểm" hay vẫn "liệt kê"?
   - PASS: title hook + body có connector + bullet có substance không phải data dump
   - FAIL: iterate Master prompt + bullet examples

**Total estimate: ~5.5 days**.

---

## 4. Token Cost Increase

Master prompt V4.0 carries: pick-question + skip_reasons + data_trail + body pattern + 5 gates + bullet examples reference. **Estimated +30% tokens per /tin run** vs V3.6. Budget: 1 run ~$0.5-1 USD V3.6 → ~$0.7-1.3 USD V4.0.

---

## 5. Open Issues / Defer

- **Filename slug collisions**: 2 batches same date with similar hooks → suffix `-2`. Edge case, ignore unless seen.
- **Bullet substance enforcement**: mechanical gates can't force argument quality. Mitigate via examples + Skeptic Pass 1. If first /tin MBB still listy → tighten via prompt iteration, not new gate.
- **Render rewrite estimate**: advisor flagged ≥2 days. If Phase D blows budget, split into D1 (server-side render) + D2 (React component update) sequential.
- **Skeptic angle clustering**: 2/3 Skeptic dispatches in /tin TCB used `alt_interpretation`. Variety guard memory check pass (empty memory). Future: enforce 3-recent angle diversity.

---

## 6. Acceptance Criteria for V4.0 Done

1. ✅ `uv run pytest -v` passes ~45 tests (37 existing + 8 new V4.0 gate tests)
2. ✅ `/tin MBB` produces 1-3 markdown files, each:
   - Filename = `MBB-<date>-<hhmm>-<hook-slug>.md`
   - Title is hook (passes Gate 4)
   - Body = 1 para + 3-7 bullets + closing (passes Gate 3)
   - Pass all 5 gates V4.0
3. ✅ Compare Feed right column shows 8 sections, all user-readable Vietnamese, no enum
4. ✅ Multi-article: 3 briefs → 3 files → 3 cards on IndexPage
5. ✅ Crawl funnel reject reasons = narrative + vai trò labels (Gác cổng / Tổng biên tập / Phóng viên bỏ)
6. ✅ Master data_trail + Skeptic data_trail render trên cột phải
7. ✅ Bug 1, 2, 3 fixed
8. ✅ KB Bank only 4 frameworks files
9. ✅ Manual sanity check: bài MBB CÓ "luận điểm" + hook clickable, KHÔNG liệt kê

---

## 7. Glossary V4.0

- **Hook**: title compelling makes-you-want-to-click. Pattern question OR declarative paradox.
- **Tension word**: từ trong title báo hiệu paradox/argument: `hy sinh`, `đánh đổi`, `nghịch lý`, `vì sao`, `đổi lấy`, `không phải`, `bù lại`, `thay vì`, `chấp nhận`.
- **Substantive bullet**: bullet ≥20 words với ≥1 bold highlight + connector + mechanism reasoning. Not data dump.
- **Data trail**: per-source log (where + what fetched + what used for in article). Master and Skeptic both produce.
- **Vai trò Vietnamese reject labels**: Gác cổng (Editor V1) / Tổng biên tập (Story Editor) / Phóng viên (Master).
- **Public slug**: filename + URL identifier derived from hook title (lowercase + ASCII + hyphen + max 60 chars).

---

## 8. Next Step

1. User review spec
2. If approved → invoke `superpowers:writing-plans` for V4.0 implementation plan
3. Plan execution via subagent-driven-development
4. Verify with `/tin MBB` (fresh ticker, no Phase 4 contamination)
5. Iterate prompts if first run still listy
