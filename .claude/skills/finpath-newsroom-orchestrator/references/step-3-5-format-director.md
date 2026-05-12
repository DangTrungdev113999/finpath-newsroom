# Step 3.5 — Format Director (Task dispatch detail)

> Loaded from `Skill: finpath-newsroom-orchestrator` references. Subagent `newsroom-format-director` enriches Story Editor brief with `format_id` + `tone_bias` + `length_target` per `deep_question_option` BEFORE Master picks question. V5.0 (Phase B-11).

## HARD RULE — no inline self-execute

Orchestrator MUST dispatch via `Task` tool. Inline pick = silently wrong format → Master writes wrong pattern → 9-gate reject loop. Schema validation in `lib.pipeline_db.validate_pipeline_step` enforces `step_3_5_format_director.format_picks` is non-empty list. If subagent crashes, **STOP pipeline + report error** — KHÔNG fallback self-execute.

## Task dispatch

```
Task tool:
  description: "Format Director batch <BATCH_ID>"
  subagent_type: newsroom-format-director
  prompt: <JSON input — see "Input contract" below>
```

## Input contract

```json
{
  "brief": {
    "ticker": "VCB",
    "deep_question_options": [
      {
        "question": "...",
        "category": "paradox | why_now | hidden_mechanism | comparison_deep | early_signal",
        "stance_directive": { ... }  // V5.0 + V5.1.2 PATCH
      },
      ...
    ],
    "angle_label": "...",
    "angle_narrative": "...",
    "insight_hypothesis": "..."
  },
  "ticker_market_data": {
    "price": 89500.0,
    "pct_change": -1.23,
    "as_of": "2026-05-12T09:30:00Z"
  }
  // OR ticker_market_data: null (Step 1.5 soft-failed)
}
```

## Output contract

```json
{
  "brief_enriched": {
    // ... original brief fields ...
    "deep_question_options": [
      {
        "question": "...",
        "category": "...",
        "stance_directive": { ... },
        // 4 NEW FIELDS per option:
        "format_id": "standard_narrative | standard_listicle | flash_qa | standard_qa | ...",
        "tone_bias": "bullish | bearish | neutral | defensive",
        "length_target": 250,
        "format_reasoning": "narrative why this format was picked"
      },
      ...
    ]
  },
  "format_director_log": {
    "format_picks": [...],
    "candidates_considered_per_option": {...},
    "variety_check": {...}
  }
}
```

## Pre-Master substitution

Replace the original brief with `brief_enriched` before dispatching Step 4 Master. Master receives V5.0 brief with format pre-picked per option; Master picks 1 option (with its bundled format_id) and applies pattern from `data/format_registry.yaml`.

## Observability emit (defer persist to after Step 4)

```python
payload_fd = {
    "model": "claude-sonnet-4-6",
    "started_at": started_at_fd,
    "duration_ms": int((time.time() - t0_fd) * 1000),
    "tokens": parse_task_usage(task_return_fd),
    "format_picks": format_picks,                      # required, non-empty list
    "candidates_considered_per_option": candidates_per_option,
    "variety_check": variety_check_dict,
}
# Defer per-article_id log_pipeline_step(article_id, "step_3_5_format_director", payload_fd)
# to after Step 4 — batch-level duplication pattern.
```

## Schema validation

`step_3_5_format_director.format_picks` MUST be a non-empty list. Enforced by `lib.pipeline_db.validate_pipeline_step`. Validation failure → `ValueError` on persist → STOP that brief, log, continue next brief.

## Variety check

Format Director reads recent N articles in same batch + recent published from `generated_news` to avoid clustering same format_id. Returns `variety_check.format_distribution` for diagnostics.

## Failure modes

- Subagent crash → STOP pipeline + report. NO inline fallback.
- Output `format_picks` empty → schema validation rejects payload → STOP this brief.
- Tie-break ambiguity → subagent uses skill `finpath-newsroom-format-director` deterministic tie-break (timeline markers, length downgrade, tone bias). Not orchestrator's concern.

## Related skill

Full Format Director logic (5-step flow, format candidate filter, hidden_mechanism tie-break, length downgrade heuristic, tone bias, variety guard) lives in `Skill: finpath-newsroom-format-director` — load that skill when implementing/debugging the agent, not when running orchestrator.
