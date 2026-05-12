---
name: finpath-newsroom-headline-craft
description: Headline Craft skill V1.1 — 5 hard criteria + 4 lối + 8-point rubric for title generation. Use when newsroom-headline-craft agent runs Step 4.5 of pipeline. Em dash banned (V1.1 PATCH).
---

# Headline Craft Skill V1.1

Compact reference for Headline Craft agent. Loaded via `Skill: finpath-newsroom-headline-craft`.

## V1.1 PATCH note

Em dash `—` (U+2014) BANNED trong title (AI-tell signal). See `references/no-em-dash-policy.md`.

## Workflow summary

1. Read body + brief + stance_directive
2. Pick 1 lối (4 options — see `references/4-loi-giat-tit.md`)
3. Generate 3 candidate titles cùng lối
4. Apply 5 hard criteria (see `references/criteria-definitions.md`)
5. Score 8-point rubric (see `references/candidates-scoring.md`)
6. UPDATE generated_news.title + persist step_4_5_headline_craft

## Output schema (strict V1.1)

```json
{
  "model": "claude-sonnet-4-6",
  "duration_ms": int,
  "tokens": int | null,
  "final_title": "string — passes 5 hard criteria",
  "final_loi": "Question | Declarative tension | Quote | Contrast verb",
  "picked_score": int,
  "candidates": [
    {"title": "...", "loi": "...", "score": int, "criteria": {...}}
  ],
  "hard_criteria_pass": {
    "ticker_present": true,
    "word_count_le_12": true,
    "hook_strong": {"tension_present": true, "click_test_pass": true},
    "binh_dan_nguy_hiem": {"plain_language": true, "sharp_edge": true},
    "no_em_dash": true
  }
}
```

Validation enforced at persist: `lib.pipeline_db.validate_pipeline_step('step_4_5_headline_craft', payload, pipeline_version="V5.1")`. Fail → ValueError.

## Scorer module

Python implementation: `lib/headline_scorer.py`. Pure functions callable via:

```python
from lib.headline_scorer import check_hard_criteria, score_title, pick_best_candidate
```

Tests in `tests/test_headline_scorer.py` — 21 tests covering 5 criteria + 8-point rubric + benchmark.

## References (load on-demand)

- `references/4-loi-giat-tit.md` — 4 lối catalog + decision tree + anti-patterns
- `references/criteria-definitions.md` — 5 hard criteria with sub-tests + examples + reference pools
- `references/no-em-dash-policy.md` — V1.1 em dash ban policy + substitution patterns
- `references/candidates-scoring.md` — 8-point rubric + benchmark + anti-gaming

## Hard rules

- KHÔNG sửa body — only replace title
- KHÔNG cross-format swap — format đã fix
- KHÔNG sinh title không ticker
- KHÔNG em dash (V1.1)
- KHÔNG PR clickbait / English jargon / hedging
- 3 candidate per lối khác angle, không cùng style
