# 6-Point Scoring Rubric — Headline V1.5-lite

> Apply only to candidates passing 8 hard criteria.

## V1.5-lite PATCH (2026-05-13 PM)

DROPPED V1.2-V1.4 word bonuses (Pattern A pile-on cause):
- dramatic_verb +2 (DRAMATIC_VERBS list — replaced by Master prompt "DO NOT invent" examples)
- concrete_question_subject +1 (CONCRETE_QUESTION_SUBJECTS list)
- self_explanatory +1 (V1.3)
- tension_word +1 (TITLE_TENSION_WORDS list)

Simplified 6-point rubric — mechanical signals only.

## Rubric V1.5-lite

| Element | Points | Detector |
|---|---|---|
| Has concrete number (number + subject, no orphan) | +2 | `has_specific_number(title) and not has_orphan_number(title)` |
| Open question ending `?` | +1 | `has_open_question()` |
| Paradox pattern (mà / nhưng / thật ra) | +1 | `has_paradox_pattern()` |
| Extra concise (≤10 từ) | +1 | `len(title.split()) <= 10` |
| Has ticker (bonus for prominence) | +1 | `has_ticker()` |

**Max**: 6.

## Selection

`pick_best_candidate(candidates) -> {final_title, picked_score, all_scored}`:

1. Filter all candidates → drop fail hard criteria (8 keys)
2. If 0 pass → `ValueError("All N candidates failed")` — agent regenerate
3. Sort passing: by score DESC, tie-break length ASC
4. Return top

## V1.5-lite Benchmark

**"STB sa thải 2.700 nhân viên, VPB tuyển 362. Bank nào đúng?"** — 10 từ, score 5/6
- STB / VPB tickers — has_ticker **+1**
- 2.700 / 362 — has_concrete_number **+2**
- ? — open_question **+1**
- 10 từ — extra_concise **+1**
- No paradox pattern → 0

Total = 5/6.

## Scoring philosophy V1.5-lite

- **has_concrete_number +2** vì concreteness; V1.3 accepted financial unit + headcount + bare 4-digit, V1.5-lite preserves
- **Open question +1** vì curiosity hook
- **Paradox pattern +1** vì sets up contrast
- **Extra concise +1** vì scan time bonus
- **Has ticker +1** vì identification at-a-glance

V1.5-lite removes word bonuses — no more verb stuffing reward. Scorer rewards mechanical structure only. AI must pick natural verbs per ngữ cảnh, not list.

## Anti-gaming

- Stuffing dramatic verbs ("hy sinh đánh đổi") — no longer scores (V1.5-lite removed)
- Stuffing concrete_question_subjects ("nào sai") — no longer scores
- Long titles for "self_explanatory" — no longer scores (V1.5-lite removed)
- Real anti-gaming: 8 hard criteria + 6-point rubric reward concrete + curiosity hook, nothing else
