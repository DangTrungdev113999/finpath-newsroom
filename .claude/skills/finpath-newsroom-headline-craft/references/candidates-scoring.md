# 8-Point Scoring Rubric — Headline V1.3

> Apply only to candidates passing all hard criteria (see `criteria-definitions.md`).

## V1.3 PATCH (2026-05-13)

Replaced `extra_concise (≤10 từ) +1` → `self_explanatory (≤14 AND not orphan number) +1`.

**Why**: V1.2 rewarded short hooks even when clarity demanded subject. Result was orphan numbers ("85%" without subject) + vague references ("ngành" alone). V1.3 rewards the sweet spot: short BUT clear.

## Rubric V1.3

| Element | Points | Detector |
|---|---|---|
| Dramatic verb (hy sinh, ăn, khoe, dồn, xén, gom, bơm, tống, nhồi, ...) | +2 | `has_dramatic_verb()` |
| Specific number (V1.3 financial + headcount + bare 4-digit) | +2 | `has_specific_number()` |
| Concrete question subject (ai gom, tiền đâu, khôn hay liều, bank nào sai) | +1 | `has_concrete_question_subject()` |
| Open question ending `?` | +1 | `has_open_question()` |
| Tension word (vì sao, đánh đổi, nghịch lý) | +1 | `has_tension_word()` |
| Paradox pattern (X mà Y / thật ra / kỳ thực) | +1 | `has_paradox_pattern()` |
| **Self-explanatory (≤14 từ AND no orphan number)** | **+1** | V1.3 NEW ⭐ |

**Max**: 8.

## Selection

`pick_best_candidate(candidates) -> {final_title, picked_score, all_scored}`:

1. Filter all candidates → drop fail hard criteria (8 keys including `not_orphan_number`)
2. If 0 pass → `ValueError("All N candidates failed hard criteria")` — agent regenerate max 2 retry
3. Sort passing: by score DESC, tie-break by length ASC
4. Return top

## V1.3 Benchmarks

### Pure comparison hook (16 từ but self-explanatory)

> **"Q1 ngành bank phân hóa: STB tống 2.700, VPB+TCB+LPB nhồi thêm 700. Bank nào sai?"**

Breakdown:
- STB / VPB / TCB / LPB (tickers) — hard criterion
- tống / nhồi (dramatic verbs V1.3) **+2**
- 2.700 / 700 (specific numbers V1.3 bare) **+2**
- Bank nào sai (concrete_question_subject V1.3) **+1**
- ? (open_question) **+1**
- phân hóa (V1.3 tension word) **+1**
- KHÔNG có paradox pattern → 0
- 16 từ > 14 → self_explanatory NOT awarded → 0

Total = 2+2+1+1+1 = **7/8** (perfect 8 needs paradox + ≤14 từ).

### Shorter version (10 từ, all V1.3 hard pass)

> **"STB sa thải 2.700, VPB tuyển 362. Bank nào đúng?"**

Breakdown:
- STB / VPB (tickers) — hard criterion
- sa thải (dramatic verb V1.3) **+2**
- 2.700 / 362 (specific number V1.3) **+2**
- Bank nào đúng (concrete_question_subject V1.3) **+1**
- ? (open_question) **+1**
- 10 từ ≤14 AND no orphan → self_explanatory **+1**

Total = 2+2+1+1+1 = **7/8**.

### V1.2 canonical (still benchmark)

> **"Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?"** — score 6/8

## Scoring philosophy V1.3

- **Dramatic verb +2** vì most differentiating signal — bình dân verbs (ăn/khoe/dồn/xén/gom/bơm/tống/nhồi) thấy ngay tension + everyday voice
- **Specific number +2** vì concreteness; V1.3 accepts financial unit + headcount + bare 4-digit
- **Concrete_question_subject +1** vì "Bank nào sai?" > "vì sao?" (V1.2 bonus)
- **Open question +1** vì curiosity hook
- **Tension word +1** vì similar to dramatic verb nhưng weaker
- **Paradox pattern +1** vì sets up contrast
- **Self-explanatory +1** (V1.3) vì sweet spot 10-14 từ + no orphan = ideal scan

## Anti-gaming

- "TCB hy sinh đánh đổi lao dốc lội ngược 5.000 tỷ?" — stuffing không giúp clarity
- "STB 85% 16% 14% 2.700 700?" — stuffing numbers không tạo narrative
- Scorer counts unique signals only — repeat dramatic verb just shows boolean True, +2 once

## V1.3 trade-off

V1.2 hook 5/8 ngắn (10 từ) > V1.3 hook 7/8 dài (16 từ) ai win?

V1.3 win: scorer rewards CLARITY over CONCISENESS. The "self_explanatory +1" is a sweet spot bonus, not a hard rule — long-but-clear hooks beat short-but-orphan hooks. The hard criterion `not_orphan_number` blocks orphan hooks even if they score high otherwise.
