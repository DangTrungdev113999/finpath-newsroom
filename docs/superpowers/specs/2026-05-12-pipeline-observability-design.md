# Pipeline Observability — Python Adapter Layer Design Spec V1.0

**Date**: 2026-05-12
**Author**: Brainstormed with em (Claude)
**Status**: Draft — pending user review before plan
**Subsystem**: D (Pipeline Observability) from initial 5-subsystem feedback
**Depends on**: V5.1 spec (Format Director + Headline Craft both add new step_3_5 and step_4_5 logs); compatible with V5.0/V5.1 schema.

---

## 1. Goal

Tách trách nhiệm logging khỏi agent prompts. Mỗi subagent chỉ emit **loose result JSON** sau khi xong task; **`lib/log_adapter.py` Python helper** normalize sang canonical pipeline_log schema và persist. Mục tiêu: zero hallucination khi logging, future-proof Haiku downgrade, observability deterministic.

## 2. Problem statement

User concern: "**tôi sợ các agent tự làm việc đó sẽ bị nhiều việc dẫn đến sai sót + ảo giác khi dùng model thấp hơn opus**".

Hiện tại (V5.1) mỗi subagent agent prompt chứa bash block tự gọi `db.log_pipeline_step(article_id, step_key, payload)` với payload đúng exact schema. Đầu bếp (agent) vừa nấu (core task) vừa viết hoá đơn (log) — cognitive load = hallucinate risk khi model thấp.

Đặc biệt nếu downgrade nào sang Haiku (vd Format Director hiện Sonnet — có thể downgrade Haiku cho cost) → risk thực sự xuất hiện.

## 3. Architectural shift

| Before (V5.1) | After (V5.2 with Adapter) |
|---|---|
| Agent emits exact `step_N_*` schema JSON | Agent emits loose result JSON (whatever shape natural) |
| Agent runs bash `db.log_pipeline_step(...)` in prompt | Agent only returns result via Task tool |
| Orchestrator parses + dispatches next step | Orchestrator: (1) parse result, (2) call `adapt_step_N(result, observability)`, (3) call `db.log_pipeline_step(...)`, (4) validation runs inside db.log_pipeline_step |
| Risk: agent hallucinate schema fields | Risk: zero (adapter is Python deterministic) |

## 4. Scope

### In scope

- `lib/log_adapter.py` module với 7 adapter function (1 per subagent step)
- Refactor 7 subagent agent .md: remove `db.log_pipeline_step` bash blocks
- Refactor `newsroom-pipeline.md` orchestrator: insert adapter+persist after each Task dispatch
- Unit tests per adapter (Python — pure functions)
- Migration: V5.1 → V5.2 (bump pipeline_version)

### Out of scope (defer)

- Logger Agent (Option 1 from brainstorm) — superseded by adapter approach
- Skill split per agent (Option 2) — superseded
- Real-time stream / Grafana dashboard / external observability
- A/B test logging behavior
- Existing Python step logging (Steps 1, 1.5, 6, 7, 8) — already deterministic, no change
- Replay tool (re-run agent from logs) — separate spec if needed later
- Anomaly detection on logs

## 5. Adapter coverage (7 subagent steps)

| Step | Subagent | Adapter function | Schema fields adapter outputs |
|---|---|---|---|
| 2 | newsroom-editor | `adapt_step_2_editor` | model, duration_ms, tokens, rows_processed, routing_decisions |
| 3 | newsroom-story-editor | `adapt_step_3_story_editor` | model, duration_ms, tokens, briefs_count, batch_id |
| 3.5 | newsroom-format-director | `adapt_step_3_5_format_director` | model, duration_ms, tokens, format_picks, candidates_considered_per_option, variety_check |
| 4 | newsroom-master-{bank,ck,bds} | `adapt_step_4_master` | model, duration_ms, tokens, chosen_question_idx, chosen_pick_reason, skip_reasons, data_trail, format_id_used, gates_passed |
| 4.5 | newsroom-headline-craft | `adapt_step_4_5_headline_craft` | model, duration_ms, tokens, final_title, picked_score, candidates, rewrites_attempted |
| 5 | newsroom-skeptic | `adapt_step_5_skeptic` | model, duration_ms, tokens, angle, verdict, skeptic_data_trail |
| 9 | newsroom-telegram-publisher | `adapt_step_9_telegram` | model, duration_ms, status, message_id, retry_count, error_if_any |

5 Python-self-execute steps (1, 1.5, 6, 7, 8) — NO adapter cần (Python tự log deterministic).

## 6. Adapter API contract

Mỗi adapter function ký hiệu:

```python
def adapt_step_N_<name>(
    agent_result: dict,
    observability: dict,
) -> dict:
    """Transform agent loose result → canonical pipeline_log schema.

    Args:
      agent_result: Free-shape JSON from Task tool return (parsed).
                    Adapter must handle missing fields with sensible defaults.
      observability: {model, started_at, duration_ms, tokens} from orchestrator.
                     Always populated by orchestrator.

    Returns:
      dict matching _STEP_N_REQUIRED schema in lib/pipeline_db.py.

    Raises:
      ValueError if agent_result is fundamentally malformed (e.g. dict expected, got string).
    """
```

### Common patterns

**Pattern 1: Missing field default**

```python
def adapt_step_4_master(result: dict, obs: dict) -> dict:
    return {
        "chosen_question_idx": result.get("picked") or result.get("chosen_question_idx", 0),
        "chosen_pick_reason": result.get("reason") or result.get("chosen_pick_reason") or "Default — agent emit thiếu reason",
        "skip_reasons": result.get("skip_reasons") or result.get("skipped") or {},
        "data_trail": _normalize_data_trail(result.get("data_sources") or result.get("data_trail") or []),
        "format_id_used": result.get("format") or result.get("format_id_used") or "standard_qa",
        **obs,
    }
```

Adapter accepts multiple agent emit styles (legacy or new) → normalize. Adapter never raises on minor field absence.

**Pattern 2: Defensive type coercion**

```python
def _normalize_data_trail(raw) -> list[dict]:
    """Handle V3.6 string entries + V4.0 dict entries + missing fields."""
    if not isinstance(raw, list):
        return []
    out = []
    for entry in raw:
        if isinstance(entry, str):
            # Legacy V3.6 string → V4.0 dict shape
            out.append({"source": entry, "fetched": "", "purpose": ""})
        elif isinstance(entry, dict):
            normalized = {
                "source": entry.get("source", ""),
                "fetched": entry.get("fetched", ""),
                "purpose": entry.get("purpose", ""),
            }
            # Pass through any other keys for back-compat
            for k, v in entry.items():
                if k not in normalized:
                    normalized[k] = v
            out.append(normalized)
        # else: skip non-string non-dict entry (defensive)
    return out
```

**Pattern 3: Required field fail-loud**

Some fields are critical — adapter should fail-loud if agent didn't provide:

```python
def adapt_step_4_5_headline_craft(result: dict, obs: dict) -> dict:
    title = result.get("final_title") or result.get("title")
    if not title:
        raise ValueError(
            f"adapt_step_4_5_headline_craft: agent result missing both "
            f"'final_title' and 'title' keys. Got: {list(result.keys())}"
        )
    # ... rest of fields
```

## 7. Adapter implementations

### 7.1 `adapt_step_2_editor`

```python
def adapt_step_2_editor(result: dict, obs: dict) -> dict:
    """Editor V1 — routing decisions per row."""
    return {
        **obs,
        "rows_processed": result.get("rows_processed") or len(result.get("decisions", [])),
        "routing_decisions": result.get("decisions", []),
    }
```

### 7.2 `adapt_step_3_story_editor`

```python
def adapt_step_3_story_editor(result: dict, obs: dict) -> dict:
    """Story Editor — briefs picked + rejected."""
    return {
        **obs,
        "briefs_count": result.get("briefs_count") or len(result.get("briefs", [])),
        "rejected_count": len(result.get("rejected", [])),
        "batch_id": result.get("batch_id", ""),
    }
```

### 7.3 `adapt_step_3_5_format_director`

```python
def adapt_step_3_5_format_director(result: dict, obs: dict) -> dict:
    """Format Director — format picks per option + variety check."""
    log_data = result.get("format_director_log") or result
    return {
        **obs,
        "format_picks": log_data.get("format_picks") or [],
        "candidates_considered_per_option": log_data.get("candidates_considered_per_option") or [],
        "variety_check": log_data.get("variety_check") or {},
    }
```

### 7.4 `adapt_step_4_master`

```python
def adapt_step_4_master(result: dict, obs: dict) -> dict:
    """Master — most complex schema."""
    return {
        **obs,
        "chosen_question_idx": result.get("chosen_question_idx") or result.get("picked") or 0,
        "chosen_pick_reason": result.get("chosen_pick_reason") or result.get("pick_reason") or "auto",
        "skip_reasons": result.get("skip_reasons") or {},
        "data_trail": _normalize_data_trail(result.get("data_trail") or result.get("data_sources") or []),
        "format_id_used": result.get("format_id_used") or result.get("format") or "standard_qa",
        "format_escalation_reason": result.get("format_escalation_reason"),  # may be None
        "gates_passed": result.get("gates_passed", True),
    }
```

### 7.5 `adapt_step_4_5_headline_craft`

```python
def adapt_step_4_5_headline_craft(result: dict, obs: dict) -> dict:
    """Headline — title + candidates + score."""
    title = result.get("final_title") or result.get("title")
    if not title:
        raise ValueError(
            f"adapt_step_4_5_headline_craft: missing final_title in agent result. "
            f"Keys: {list(result.keys())}"
        )
    return {
        **obs,
        "final_title": title,
        "picked_score": int(result.get("picked_score") or result.get("score") or 0),
        "candidates": result.get("candidates") or [],
        "rewrites_attempted": int(result.get("rewrites_attempted", 0)),
    }
```

### 7.6 `adapt_step_5_skeptic`

```python
def adapt_step_5_skeptic(result: dict, obs: dict) -> dict:
    """Skeptic — critique angle + verdict + data trail."""
    return {
        **obs,
        "angle": result.get("angle") or "data_skepticism",  # default safest angle
        "verdict": result.get("verdict") or "",
        "skeptic_data_trail": _normalize_data_trail(result.get("skeptic_data_trail") or result.get("data_trail") or []),
    }
```

### 7.7 `adapt_step_9_telegram`

```python
def adapt_step_9_telegram(result: dict, obs: dict) -> dict:
    """Telegram — push status + retry."""
    return {
        **obs,
        "status": result.get("status") or "unknown",
        "message_id": result.get("message_id"),
        "retry_count": int(result.get("retry_count", 0)),
        "error": result.get("error"),
    }
```

## 8. Orchestrator workflow change

### Before (V5.1)

```markdown
### Step 4 — Master (Task dispatch)

```
Task: newsroom-master-{sector}
prompt: <brief JSON>
```

Master returns JSON + persists pipeline_log itself via bash inside prompt.
```

### After (V5.2)

```markdown
### Step 4 — Master (Task dispatch + adapter persist)

```
Task: newsroom-master-{sector}
prompt: <brief JSON>
```

After Master returns:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json, time
from datetime import datetime, timezone
from lib.log_adapter import adapt_step_4_master
from lib.pipeline_db import PipelineDB, parse_task_usage

agent_result = json.loads('<MASTER RETURN JSON>')
task_return_text = '<RAW TASK RETURN TEXT>'

obs = {
    'model': 'claude-opus-4-7',
    'started_at': '<ISO>',
    'duration_ms': <int>,
    'tokens': parse_task_usage(task_return_text),
}
payload = adapt_step_4_master(agent_result, obs)

db = PipelineDB('data/pipeline.db')
db.log_pipeline_step('<article_id>', 'step_4_master', payload)
db.close()
"
```

Adapter does normalization + defensive defaults. Validation runs inside `db.log_pipeline_step` (fail-loud if adapter logic bug). Master agent **NO LONGER writes log itself** — emit result only.
```

Same pattern for all 7 subagent steps.

## 9. Agent prompt simplification

### Example: `newsroom-master-bank.md` BEFORE (V5.1)

```markdown
### Step 9 — Persist

```bash
db.log_pipeline_step(article_id, "step_4_master", {
    "chosen_question_idx": 0,
    "chosen_pick_reason": "...",
    "skip_reasons": {...},
    "data_trail": [...],
    "format_id_used": "standard_qa",
    "model": "claude-opus-4-7",
    "duration_ms": ...,
    "tokens": ...,
})
```
```

### Example: `newsroom-master-bank.md` AFTER (V5.2)

```markdown
### Step 9 — Output result

Return JSON result via Task tool:

```json
{
    "picked": 0,
    "reason": "Câu hỏi paradox phù hợp...",
    "skip_reasons": {1: "...", 2: "..."},
    "data_sources": ["Finpath_API/...", "KB/..."],
    "format": "standard_qa",
    "gates_passed": true,
    "final_body": "<article body>",
    "final_title": "<draft title for Headline agent>"
}
```

**KHÔNG cần write log** — orchestrator handles via adapter + `db.log_pipeline_step`. Just return result with whatever shape feels natural; adapter normalizes.

⚠️ Hard required: `final_body`, `final_title`, `format` — orchestrator reads these for next steps.
```

Reduces cognitive load. Agent focuses on **content quality**, not schema correctness.

## 10. Migration V5.1 → V5.2

### 10.1 `pipeline_version` bump

- `lib/pipeline_db.py:insert_generated_news` default bumped V5.1 → V5.2
- `lib/render_compare_feed.py` frontmatter default bumped
- `validate_pipeline_step` adds V5.2-aware (current schema stays — no breaking field changes)

### 10.2 Back-compat for in-flight pipelines

If V5.1 pipeline is mid-run when V5.2 deployed:
- Agent still tries to write log via bash (its V5.1 prompt)
- `db.log_pipeline_step` accepts (schema unchanged)
- New pipelines use V5.2 prompts (orchestrator-managed adapter)
- Both styles coexist temporarily; V5.2 is the new path

### 10.3 Validation back-compat

`validate_pipeline_step` requires same fields V5.1+ for step_4 + step_3_5 + step_4_5. Adapter outputs same shape. No validation changes.

## 11. File touch list

| File | Action | Lines est |
|---|---|---|
| `lib/log_adapter.py` | NEW | ~350 |
| `tests/test_log_adapter.py` | NEW | ~400 (per-adapter tests + edge cases) |
| `.claude/agents/newsroom-editor.md` | MODIFY | -10 (remove bash log block, replace với "return JSON") |
| `.claude/agents/newsroom-story-editor.md` | MODIFY | -15 |
| `.claude/agents/newsroom-format-director.md` (from Plan B) | MODIFY | -15 |
| `.claude/agents/newsroom-master-bank.md` | MODIFY | -40 (large bash blocks) |
| `.claude/agents/newsroom-master-ck.md` | MODIFY | -40 |
| `.claude/agents/newsroom-master-bds.md` | MODIFY | -40 |
| `.claude/agents/newsroom-headline-craft.md` (from Plan C) | MODIFY | -25 |
| `.claude/agents/newsroom-skeptic.md` | MODIFY | -25 |
| `.claude/agents/newsroom-telegram-publisher.md` | MODIFY | -20 |
| `.claude/agents/newsroom-pipeline.md` | MODIFY | +200 (orchestrator-managed adapter+persist after each Task) |
| `lib/pipeline_db.py` | MODIFY | +5 (version bump V5.1 → V5.2 default) |
| `lib/render_compare_feed.py` | MODIFY | +1 (frontmatter version default) |
| `CLAUDE.md` | MODIFY | +30 (new "Pipeline Observability V5.2" section, agent prompt convention update) |

Total: ~2 new + ~12 modify ≈ 800-1000 LOC change.

## 12. Patches required to Plan B + Plan C

### Plan B (Format Diversity)

| Plan B Task | V5.2 patch |
|---|---|
| Task 9 Format Director agent prose | Remove bash log block. Replace với "return result JSON; orchestrator adapts via `adapt_step_3_5_format_director`". |
| Task 11 Pipeline orchestrator Step 3.5 | Update dispatch flow: Task return → adapter+persist via Python bash (orchestrator-managed). |
| Task 13-15 Master agents | Remove bash log blocks in Step 9 (Bank/CK/BĐS). Agent emits result; orchestrator adapts. |

### Plan C (Headline Craft)

| Plan C Task | V5.2 patch |
|---|---|
| Task 3 Headline agent prose | Remove bash log block. Replace với "return result; orchestrator adapts via `adapt_step_4_5_headline_craft`". |
| Task 5 Pipeline orchestrator Step 4.5 | Update dispatch flow: Task return → adapter+persist via Python bash. |

These patches will be applied INLINE to plan B + plan C concurrently with this spec — per user strategy "brainstorm all → plan all → execute" (zero implement-and-delete).

## 13. Testing strategy

### Unit tests per adapter (`tests/test_log_adapter.py`)

For each of 7 adapter functions:
- **Happy path**: full agent result with all fields → expected schema
- **Missing optional field**: adapter uses default
- **Missing required field**: adapter raises ValueError
- **Legacy V3.6 string data_trail entries**: adapter coerces to dict shape
- **Wrong type**: adapter defensive type coerce
- **Extra unknown fields**: adapter passes through or ignores cleanly
- **Empty agent result**: adapter uses all defaults

≈ 7 adapters × 6 test cases = ~42 tests + edge cases.

### Integration tests

- End-to-end: dispatch Format Director Task with fixture → adapter → persist → query DB → verify shape
- Same for Master + Headline + Skeptic

### Visual verification

- Run /tin VCB after V5.2 → check pipeline_log entries identical in shape to V5.1 (no breaking change)
- All `step_N_*` fields populated correctly (no missing defaults causing render issues)

## 14. Rollout phases

### Phase 1 — Adapter module + tests (Days 1-2)
- `lib/log_adapter.py` with 7 functions
- `tests/test_log_adapter.py` per-adapter

### Phase 2 — Orchestrator refactor (Days 3-4)
- `newsroom-pipeline.md` insert adapter+persist after each Task dispatch
- Add documentation block: "Agent emits result; orchestrator adapts + persists"

### Phase 3 — Agent prompt simplification (Day 5-6)
- 7 subagent .md files: remove bash log blocks
- Update output schema examples to "loose result JSON"

### Phase 4 — Version bump + CLAUDE.md (Day 7)
- pipeline_version V5.1 → V5.2
- CLAUDE.md observability section
- Patches to Plan B + Plan C (apply inline now per user strategy)

### Phase 5 — Verification (Day 8)
- E2E /tin VCB / SSI / VHM
- Visual + log shape inspection

Estimated: ~7-8 days after V5.1 implementation, OR concurrent with V5.1 if not yet implemented.

## 15. Open questions / deferred

1. **Adapter for Phase H1 steps (7, 8, 9)** — Steps 7 (git publish) + 8 (Pages wait) are Python — already deterministic. Step 9 Telegram is subagent — adapter added. Confirm Step 7-8 stay self-log (no adapter needed).
2. **Default values when agent fully omits field** — e.g. `chosen_pick_reason` default "auto" — may mask agent bugs. Tune defaults per field criticality.
3. **Adapter test fixtures** — should use real agent return samples? Capture 1-2 production runs as fixtures.
4. **Field name dual support** (vd `picked` vs `chosen_question_idx`) — adapter accepts both. After 30 days production, can deprecate legacy names.
5. **Observability for adapter itself** — adapter call sites should log adapter-level metrics (transformation success/fail rate). Defer to V5.3+ if needed.

## 16. Spec changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-05-12 | Initial draft. 7 adapter functions for subagent steps. Python deterministic transform agent loose result → canonical schema. Migration V5.1 → V5.2. Patches required to Plan B + Plan C (will apply inline). |
