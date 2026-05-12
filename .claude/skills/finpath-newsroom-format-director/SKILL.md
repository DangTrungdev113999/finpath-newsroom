---
name: finpath-newsroom-format-director
description: Format Director skill V5.0 — 5-step flow to pick format_id per deep_question_option. Use when newsroom-format-director agent runs Step 3.5 of pipeline. Covers category → candidate filter, hidden_mechanism tie-break via timeline markers, length downgrade heuristic, tone bias from market mood, variety guard.
---

# Format Director Skill V5.0

Compact reference for the Format Director agent. Loaded via `Skill: finpath-newsroom-format-director` at agent invocation.

V5.1: Format Director KHÔNG quyết title. Title craft thuộc Headline agent (Step 4.5).

## Format catalog summary (load `data/format_registry.yaml` for full spec)

| format_id | length | structure | trigger categories |
|---|---|---|---|
| `flash_qa` | 100-150 từ | paragraph only, no bullets | fallback (factual single Q) |
| `standard_qa` | 200-300 từ | opening + 3-6 bullets + closing | paradox, why_now, hidden_mechanism |
| `standard_listicle` | 250-350 từ | opening ≤30 + 4-7 dense bullets + closing | comparison_deep, early_signal |
| `standard_narrative` | 250-350 từ | flow paragraphs, 0-2 bullets | hidden_mechanism (tie-break) |

## 5-step flow (deterministic, no creativity)

1. **Category → candidates filter** (5 trigger_categories defined). No match → fallback `flash_qa`.
2. **Tie-break** (only when 2 candidates, only for `hidden_mechanism`): count timeline markers in `narrative_setup` matching `(Q[1-4]/?\d{0,4}|(?:năm|hồi|từ|đến|cuối|đầu)\s+\d{4}|tháng \d{1,2}|cuối năm|đầu năm)`. ≥3 → narrative; else → qa. ⚠ Bare 4-digit currency (vd "5000 tỷ") KHÔNG match — required year context.
3. **Length downgrade**: IF `len(data_trail_preview) ≤ 2` AND `key_metric_count ≤ 1` AND picked starts with `standard_` → downgrade to `flash_qa`. Rationale: shallow data → don't pad.
4. **Tone bias**: `pct_change_today ≤ -3%` → `acknowledge_market_red`; `≥ +3%` → `acknowledge_market_green`; else → `neutral`.
5. **Length target** from registry: flash=130, qa=250, listicle/narrative=300.

## Output schema (strict)

```json
{
  "brief_enriched": { /* original brief + 4 new fields per option */ },
  "format_director_log": {
    "format_picks": [{"option_idx": 0, "format_id": "standard_qa", "format_reason": "...", "tone_bias": "neutral", "length_target": 250}],
    "candidates_considered_per_option": [{"option_idx": 0, "category": "paradox", "candidates": ["standard_qa"]}],
    "variety_check": {"recent_3_articles_same_ticker_formats": ["..."], "current_pick_diversity_warning": false}
  }
}
```

Each `format_pick.format_id` MUST ∈ {flash_qa, standard_qa, standard_listicle, standard_narrative}. Validation enforced at persist by `lib.pipeline_db.validate_pipeline_step('step_3_5_format_director', ...)`.

## Anti-hallucination guards

- `format_reason` follows template: `"Category={X} → candidates={Y}. Picked={Z}. {extra}"`. No free-form essay.
- Fallback `flash_qa` when confused — don't try to invent.
- No new format ideas — `format_registry.yaml` is closed catalog. Add format → edit yaml + restart pipeline.

## Variety guard

Query 3 most-recent articles via:

```python
db.recent_generated_news(ticker, limit=3)
```

If `len(formats) == 3` AND all 3 same `format_id_used` (read from each `pipeline_log.step_4_master.format_id_used`) AND current pick same → emit `current_pick_diversity_warning: true` + note in `format_reason`. Do NOT change pick — data justifies pick wins.

⚠ Cold start: nếu ticker chưa có 3 article prior, `current_pick_diversity_warning: false` — không trigger warning.

## Edge cases

- `category` not in 5 known → fallback `flash_qa`.
- `data_trail_preview` missing or empty → treat as `n_sources=0`, may downgrade.
- `market_data` null (Step 1.5 soft-failed) → `tone_bias: neutral` always.
- `narrative_setup` empty → 0 timeline markers → hidden_mechanism picks qa.
