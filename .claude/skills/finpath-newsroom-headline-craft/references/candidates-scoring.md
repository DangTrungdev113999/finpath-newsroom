# 8-Point Scoring Rubric — Headline V1.1

> Apply only to candidates passing 5 hard criteria (see `criteria-definitions.md`).

## Rubric

| Element | Points | Detector |
|---|---|---|
| Dramatic verb (hy sinh, đánh đổi, lao dốc, ...) | +2 | `has_dramatic_verb()` |
| Specific number with units (5.000 tỷ, 67%, /năm) | +2 | `has_specific_number()` |
| Open question ending `?` | +1 | `has_open_question()` |
| Tension word (vì sao, đánh đổi, nghịch lý, ...) | +1 | `has_tension_word()` |
| Paradox pattern (X mà Y / thật ra / kỳ thực) | +1 | `has_paradox_pattern()` |
| Extra concise (≤10 từ) | +1 | `len(title.split()) <= 10` |

**Max**: 8 (note: dramatic_verb + tension_word có thể overlap với "hy sinh" / "đánh đổi" → both count).

## Selection

`pick_best_candidate(candidates) -> {final_title, picked_score, all_scored}`:

1. Filter all candidates → drop fail hard criteria
2. If 0 pass → `ValueError("All N candidates failed hard criteria")` — agent regenerate max 2 retry
3. Sort passing: by score DESC, tie-break by length ASC
4. Return top

## Benchmark

> **"TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?"** — score 7/8

Breakdown:
- TCB (ticker) — hard criterion, không count score
- hy sinh (dramatic verb) **+2**
- 5.000 tỷ/năm (specific number) **+2**
- ? (open question) **+1**
- đổi lấy (tension word) **+1**
- 9 từ (extra concise) **+1**
- KHÔNG có "mà / nhưng / thật ra" → paradox_pattern = 0

Total = 2+2+1+1+1 = **7/8** (perfect 8 would need paradox pattern).

## Scoring philosophy

- **Dramatic verb +2** vì most differentiating signal — "hy sinh" / "đánh đổi" thấy ngay tension
- **Specific number +2** vì concreteness (5.000 tỷ > "lớn nhất")
- **Open question +1** vì curiosity hook nhưng dễ giả tạo
- **Tension word +1** vì similar to dramatic verb nhưng weaker
- **Paradox pattern +1** vì sets up contrast nhưng khó score consistently
- **Extra concise +1** vì readability bonus

## Anti-gaming

- "TCB hy sinh đánh đổi lao dốc lội ngược 5.000 tỷ?" — stuffing dramatic verbs không giúp clarity
- "TCB 5.000 tỷ 30% 12% 18% Q1?" — stuffing numbers không tạo narrative
- "TCB hy sinh hy sinh hy sinh để đổi lấy gì?" — repetition lowers quality

Scorer counts unique signals only (regex match) — repeat dramatic verb just shows boolean True, +2 once.
