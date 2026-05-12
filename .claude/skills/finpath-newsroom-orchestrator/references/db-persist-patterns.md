# DB Persist Patterns — PipelineDB API

> Loaded from `Skill: finpath-newsroom-orchestrator` references. SQLite writes via `lib/pipeline_db.py::PipelineDB`. Always persist BEFORE proceeding to next step (idempotent pipeline — restart-safe).

## API surface

```python
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')

# Crawler row writes (Step 1) — usually mechanical via lib/stages/run_crawler.py
db.upsert_crawl_row(...)

# Editor / Story Editor field updates (Step 2 / 3)
db.update_crawl_row(row_id, editor_v1_decision=..., editor_v1_note=..., sector=...)
db.update_crawl_row(row_id, story_editor_decision=..., story_editor_note=..., brief_json=...)

# Master persist (Step 4)
db.insert_generated_news(article_id, public_slug, ticker, title, body, ...)
db.update_crawl_row(row_id, master_decision='write_article', article_id=article_id)

# Pipeline observability (every step)
db.log_pipeline_step(article_id, step_key, payload_dict)

# Query helpers
rows = db.query_by_funnel_batch(batch_id)
row = db.get_crawl_row(row_id)
article = db.get_generated_news(article_id)
```

## Order of operations per brief

```
brief → Step 4 (Master) → insert_generated_news + update_crawl_row → log_pipeline_step(article_id, "step_4_master", payload)
       → [Step 5 Skeptic ⏸ paused — when re-enabled: append critique + log_pipeline_step]
```

## Atomic per-article write (Step 4)

`newsroom-master-{sector}` skill handles insert internally. Orchestrator only needs to:
1. Wait for Task return (`article_id`, `public_slug`, ...)
2. Verify `accepted_hypothesis == True` — skip if false (no article persisted by Master)
3. Persist `step_4_master` payload via `log_pipeline_step`

## UPDATE title pattern (reserved for Step 4.5 Plan C)

When `newsroom-headline-craft` lands (Plan C), orchestrator will dispatch post-Master to refine title. Pattern (TBD):

```python
# After Headline Craft Task returns
db.update_generated_news(article_id, title=refined_title, headline_meta=meta_dict)
db.log_pipeline_step(article_id, "step_4_5_headline_craft", payload)
```

Implementation pending — see `references/step-4-5-headline-craft.md`.

## Batch-level persist after Step 4

Steps 1, 1.5, 2, 3, 3.5 emit observability deferred until article_ids land (Step 4 done). Then:

```python
article_ids = [a["article_id"] for a in accepted_master_outputs]
for aid in article_ids:
    db.log_pipeline_step(aid, "step_1_crawler", payload_crawler)
    db.log_pipeline_step(aid, "step_1_5_market_snapshot", payload_market)
    db.log_pipeline_step(aid, "step_2_editor", payload_editor)
    db.log_pipeline_step(aid, "step_3_story_editor", payload_story)
    db.log_pipeline_step(aid, "step_3_5_format_director", payload_fd)
```

Duplicated across N articles by design (each article carries full lineage).

## Step 6 render persist

`lib/render_compare_feed.py <batch_id>` does:
1. Query `db.query_by_funnel_batch(batch_id)` filter `master_decision == 'write_article'`
2. Generate public_slug if missing (`lib/slugify.py::slugify_hook`)
3. Write markdown to `output/compare-feed/<TICKER>-<DATE>-<HHMM>-<slug>.md`
4. Append manifest entry to `output/compare-feed/manifest.json`

Output: N files (N = accepted Master articles). Then orchestrator emits `step_6_render` payload per article_id.

## Step 7 / 8 / 9 persist

`lib/stages/run_git_publish.py`, `lib/stages/run_pages_wait.py`, `newsroom-telegram-publisher` agent each return result dict. Orchestrator captures + logs:

```python
db.log_pipeline_step(aid, "step_7_git_publish", payload_git)   # batch-level
db.log_pipeline_step(aid, "step_8_pages_wait", payload_pages)  # batch-level
db.log_pipeline_step(aid, "step_9_telegram", payload_telegram) # per-article
```

Telegram agent auto-persists `generated_news.telegram_pushed_at` on success.
