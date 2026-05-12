# Step 4.5 — Headline Craft (Plan C — TBD)

> Loaded from `Skill: finpath-newsroom-orchestrator` references.

⚠️ This reference is a PLACEHOLDER. **Plan C** (Headline Craft agent) will fill in the detailed dispatch contract + UPDATE `generated_news.title` pattern.

## Pending Plan C completion

- `newsroom-headline-craft` agent prose (`.claude/agents/newsroom-headline-craft.md`)
- Step 4.5 dispatch pattern post-Master (Task tool invocation)
- UPDATE SQL for title persist (`db.update_generated_news(article_id, title=..., headline_meta=...)`)
- `step_4_5_headline_craft` observability schema + validation in `lib/pipeline_db.py::validate_pipeline_step`

## Interim behavior (until Plan C ships)

Master returns body + provisional title. Render uses Master's provisional title verbatim. No refinement step.

## Anticipated dispatch (subject to change)

```
Task tool:
  description: "Headline Craft <ticker>"
  subagent_type: newsroom-headline-craft
  prompt: "Refine title for article_id=<id>. Read body + insight_final. Apply title-as-hook test 5s preference: Quote > Question > Paradox > Event summary. Persist refined title via db.update_generated_news."
```

## Anticipated observability payload

```python
payload_headline = {
    "model": "opus",  # tentative
    "started_at": ...,
    "duration_ms": ...,
    "tokens": parse_task_usage(...),
    "title_before": "...",
    "title_after": "...",
    "hook_type": "quote | question | paradox | event",
    "tension_words_used": [...],
}
db.log_pipeline_step(article_id, "step_4_5_headline_craft", payload_headline)
```

## Position in pipeline

```
Step 4 Master → Step 4.5 Headline Craft → [Step 5 Skeptic ⏸ paused] → Step 6 Render
```

Per-article (same as Step 4 + 5).

---

**Status**: PLACEHOLDER — fill in when Plan C lands.
