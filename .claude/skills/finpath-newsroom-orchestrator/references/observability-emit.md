# Pipeline Observability — Emit pattern per step

> Loaded from `Skill: finpath-newsroom-orchestrator` references. Orchestrator MUST emit `pipeline_log` payload after each step with required schema. Validation enforced by `lib/pipeline_db.py::validate_pipeline_step`.

## Required fields V5.0+ (fail-loud)

Per `lib/pipeline_db.py::_OBSERVABILITY_REQUIRED`, every payload MUST include:
- `model: str` — agent model used (opus / sonnet / python / claude-sonnet-4-6)
- `duration_ms: int` — wall time milliseconds
- `tokens: int | None` — optional (Claude Code không guarantee `<usage>` block in Task return)

`started_at` (ISO 8601 UTC) is highly recommended for timeline reconstruction.

## Per-step extras (validation rules)

| step_key | Required extras |
|---|---|
| `step_3_5_format_director` | `format_picks` (non-empty list), `candidates_considered_per_option`, `variety_check` |
| `step_4_master` | `chosen_question_idx`, `chosen_pick_reason`, `skip_reasons`, `data_trail`, `format_id_used`, `accepted_hypothesis` |
| `step_5_skeptic` | `angle`, `verdict`, `skeptic_data_trail` ⏸ PAUSED 2026-05-12 |

Missing required keys → `ValueError` on persist. Do NOT workaround — dispatch the proper subagent so the schema is produced naturally.

## Emit pattern (Python — wrap each step)

```python
import time
from datetime import datetime, timezone
from lib.pipeline_db import PipelineDB, parse_task_usage

db = PipelineDB('data/pipeline.db')

# BEFORE step
started_at = datetime.now(timezone.utc).isoformat()
t0 = time.time()

# ... run step (Task dispatch hoặc self-execute) ...
task_return = "<text returned by Task tool — may contain <usage>...</usage>>"

# AFTER step
duration_ms = int((time.time() - t0) * 1000)
tokens = parse_task_usage(task_return)  # None nếu <usage> block missing — defensive

payload = {
    "model": "<sonnet|opus|python|claude-sonnet-4-6>",
    "started_at": started_at,
    "duration_ms": duration_ms,
    "tokens": tokens,
    # step-specific extras here
}

# Per-article persist for steps 4, 5; batch-level steps 1, 1.5, 2, 3, 3.5, 6, 7, 8
# duplicated across N articles in same batch (each article self-contained)
for article_id in [a["article_id"] for a in batch_articles]:
    db.log_pipeline_step(article_id, "step_1_crawler", payload)
```

## Step model convention

| step_key | model | tokens source |
|---|---|---|
| `step_1_crawler` | `sonnet` (orchestrator self-runs Crawler) | `null` (orchestrator can't introspect own tokens) |
| `step_1_5_market_snapshot` | `python` | `null` |
| `step_2_editor` | `sonnet` (Task dispatch) | `parse_task_usage(...)` |
| `step_3_story_editor` | `opus` (Task dispatch) | parsed |
| `step_3_5_format_director` | `claude-sonnet-4-6` (Task dispatch) | parsed |
| `step_4_master` | `opus` (per brief) | parsed |
| `step_5_skeptic` | `opus` ⏸ paused | parsed |
| `step_6_render` | `python` | `null` |
| `step_7_git_publish` | `python` | `null` |
| `step_8_pages_wait` | `python` | `null` |
| `step_9_telegram` | `sonnet` (per article) | parsed |

## Batch-level vs per-article persist

- **Batch-level**: Steps 1, 1.5, 2, 3, 3.5, 6, 7, 8 → mỗi article trong batch ghi entry GIỐNG NHAU (same numbers across N articles, by design — accepted duplication for self-contained per-article logs).
- **Per-article**: Steps 4, 5, 9 → entry KHÁC NHAU per article.

## Defensive notes

- `parse_task_usage` never raises — returns `None` nếu `<usage>` block absent / malformed. Token capture là nice-to-have, KHÔNG phải blocker.
- Duration + model + started_at là deterministic primary signals — ALWAYS log đúng.
- Idempotent: gọi `log_pipeline_step` 2 lần với cùng `step_key` → overwrite (allows agent retry to update timing).
- Defer batch-level emits to AFTER Step 4 when `article_ids` are first available — pre-compute payload, persist when ids land.
