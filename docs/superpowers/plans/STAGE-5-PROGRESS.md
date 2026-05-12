# Stage 5 Progress — Plan H Pipeline Run History V1.0.1

> **Last updated**: 2026-05-12 evening (Stage 5 COMPLETE).
> **Master sequence**: `docs/superpowers/plans/2026-05-12-MASTER-EXECUTION-SEQUENCE.md`

## Status: ✅ COMPLETE — 9/9 task done (H-9 CLAUDE.md note deferred to Stage 6)

**Gate 5 verification PASSED**: 416 passed + 10 deselected default suite. Live `-m integration`: 10/10 pass (7 from Stage 4 + 3 new pipeline-runs E2E).

9 commits Stage 5 (H-1 → H-9): `0119432` → `f926b4a`.

## User requirement met (compact-args)

> "phần này cho mỗi bài viết không cần nữa, nhưng không bỏ, tôi cần vẫn cần đọc để biết pipeline đó chạy thì bao nhiêu tin được tìm thấy, reject tin nào lý do reject. giờ bố trí cái crawl funnel đó ở đâu thì hợp lý dể xem được lịch sử những lần chạy"

Implementation:
- ✅ Funnel REMOVED from per-article RightColumn (H-7 — section 5 dropped, sections renumbered 6→5/7→6/8→7)
- ✅ Funnel data MOVED to dedicated `/pipeline-runs` page (H-6)
- ✅ Per-pipeline-run view shows fetched / chosen / rejected counts + reasons (H-3 builder + H-5 components)
- ✅ Vietnamese nav "Lịch sử pipeline" → `/pipeline-runs` (H-8)
- ✅ Article header `funnel_batch_id` is now hyperlink → `/pipeline-runs?batch_id=X` (H-8)

## Task summary — Plan H V1.0.1

### Phase 1 — Schema + backend (H-1 to H-3)

| Task | Subject | Commit |
|---|---|---|
| ✅ H-1 | crawl_log session_id + trigger_type + trigger_args (Python upgrade helper Option B) | `0119432` |
| ✅ H-2 | Orchestrator session_id emission + run_crawler CLI args + Step 0 prompt | `5f9b71c` |
| ✅ H-3 | build_pipeline_runs_manifest backend builder | `0748e88` |

H-1 deviation: ALTER TABLE not idempotent in SQLite → Python helper `_upgrade_crawl_log_schema()` called from BOTH `__init__` (post `_apply_migrations`) and `init_schema()` (post schema bootstrap) with guard for missing `crawl_log` table. No .sql migration file (columns + indexes both in Python).

H-3 schema mismatches resolved:
- Real columns: `crawl_log.title` / `raw_content` / `published_time` (not raw_title/raw_body/published_at)
- `crawl_log.story_editor_note` single column (no separate `_label`/`_reason`)
- `sector_code` / `hot_nhom` / `hot_rank` NOT yet on crawl_log (forward-compat slots = None in JSON)

### Phase 2 — Frontend (H-4 to H-6)

| Task | Subject | Commit |
|---|---|---|
| ✅ H-4 | web/types + pipelineRunsLoader.ts + test | `a1a879c` |
| ✅ H-5 | PipelineBatch + PipelineSession components | `60f9216` |
| ✅ H-6 | PipelineRunsPage + route /pipeline-runs + filter | `c450cb2` |

H-4 deviation: loader URL = `/articles/pipeline-runs.json` (matches existing articleLoader.ts pattern — `web/public/articles` symlinks to `output/compare-feed/`). Added `cache: 'no-store'` for parity.

### Phase 3 — Article view (H-7 to H-8)

| Task | Subject | Commit |
|---|---|---|
| ✅ H-7 | Remove RightColumn section 5 (CrawlFunnel) — file preserved for reuse | `bf8aa5d` |
| ✅ H-8 | Article header batch_id hyperlink + Header "Lịch sử pipeline" nav | `67ca329` |

### Phase 4 — Verification (H-9)

| Task | Subject | Commit |
|---|---|---|
| ✅ H-9 | E2E smoke (3 integration tests) | `f926b4a` |
| ⏸ H-9b | CLAUDE.md note (BLOCKED → Stage 6 aggregate) | — |

## Test count

- Default suite: **416 passed, 10 deselected** (7 from Stage 4 + 3 new H-9 E2E)
- Live integration (`-m integration`): **10 passed** (7 foreign flow + 3 pipeline runs)
- New tests added during Stage 5: **18** unit + **3** integration = 21

## Architecture state after Stage 5

### crawl_log schema extension

```python
# Added columns (Python helper Option B, not .sql migration)
session_id TEXT    # UUID per pipeline trigger
trigger_type TEXT  # 'tin' | 'tin-hot' | 'tin-batch'
trigger_args TEXT  # ticker for /tin, 'N=3' for /tin-hot

# Indexes
idx_crawl_log_session  ON crawl_log(session_id)
idx_crawl_log_crawled_desc  ON crawl_log(crawled_at DESC)
```

### Orchestrator changes

- `newsroom-pipeline.md` — new "Step 0 (V5.1.4 / Subsystem H): Session initialization" with `SESSION_ID=$(uuidgen)` + trigger mapping table
- `lib/stages/run_crawler.py` — 3 new CLI args (`--session-id` / `--trigger-type` / `--trigger-args`) propagated through `write_candidate_to_db()` to `insert_crawl_row()`

⚠ Out-of-scope follow-up: `/tin-hot N` dispatcher in `.claude/commands/tin-hot.md` (or wherever it lives) needs to generate `SESSION_ID` ONCE before the N-ticker loop and pass to each child invocation. H-2 stamped the single-ticker agent only.

### Backend builder

```python
# lib/render_compare_feed.py
build_pipeline_runs_manifest(db, output_path: Path) -> int
_query_sessions(db) -> list[dict]
_classify_reject(row) -> (reject_agent, reject_label, reason)
```

Emits `output/compare-feed/pipeline-runs.json`. Atomic write via `.tmp` suffix + `os.replace`. Skips rows where `session_id IS NULL` (V1.0.1 Q2 resolution).

### Frontend additions

- `web/src/types.ts` — 6 new interfaces (PipelinePickedItem / Rejected / FunnelDetail / Batch / Session / Manifest)
- `web/src/lib/pipelineRunsLoader.ts` — fetch `/articles/pipeline-runs.json`
- `web/src/components/PipelineBatch.tsx` — collapsible per-batch view
- `web/src/components/PipelineSession.tsx` — collapsible per-session group
- `web/src/pages/PipelineRunsPage.tsx` — page with date/status filters via URL query params
- `web/src/components/RightColumn.tsx` — section 5 funnel REMOVED, renumber comments
- `web/src/components/CompareFeedLayout.tsx` — funnel_batch_id is `<Link>` to `/pipeline-runs?batch_id=...`
- `web/src/components/Header.tsx` — "Lịch sử pipeline" nav added
- `web/src/App.tsx` — `<Route path="/pipeline-runs" element={<PipelineRunsPage />} />`

### Routing

```
/                       → IndexPage (articles list)
/article/:slug          → CompareFeedLayout (article view, NO crawl funnel)
/pipeline-runs          → PipelineRunsPage (history page, NEW)
/pipeline-runs?batch_id=X → auto-expand specific batch
```

## Gate 5 verification

```bash
# Default suite (Python)
uv run pytest -q
# Expected: 416 passed, 10 deselected

# Integration suite (opt-in, local DB only — no network)
uv run pytest tests/integration/test_pipeline_runs_end_to_end.py -v -m integration
# Expected: 3 passed (single-ticker / tin-hot 3 grouping / legacy skipped)

# Frontend build
cd web && npx tsc --noEmit
# Expected: no errors

cd web && npm run build
# Expected: build succeeds (chunk-size warning unrelated, pre-existing)
```

## Known deferred items

- H-9b CLAUDE.md note (architecture map + Pipeline Run History section) — Stage 6 aggregate together with F-15 + G-7
- `/tin-hot N` cross-command session_id sharing — needs follow-up patch to dispatcher
- `sector_code` / `hot_nhom` / `hot_rank` columns not yet on crawl_log — JSON has forward-compat `None` slots
- `story_editor_note` collapses `reject_label` + `reject_reason` to same value (real schema limitation)
- 5 pre-existing CommentSection.test.tsx failures unrelated to Stage 5 (user's dirty working tree pre-existing)

## Cumulative ahead of origin

Stage 1: 63. Stage 2: 8. Stage 3: 8. Stage 4: 9. Stage 5: 9. **Total ahead: ~97 commits**.

User instruction: "đúng ui đừng push lên main vội" — kept local.

## Next: Stage 6 — Final aggregate (1 task) + Gate 6 E2E smoke

Per MASTER-EXECUTION-SEQUENCE.md:

- CLAUDE.md aggregate combining 3 deferred updates:
  - F-15 (Plan F Universe Expansion — universe 61→139 in CLAUDE.md universe section)
  - G-7 (Plan G Foreign Flow — data sourcing rule note + foreign flow data source)
  - H-9b (Plan H Pipeline Run History — architecture map + Pipeline Run History section)
- Gate 6 E2E final smoke: full pipeline run verification end-to-end
- Optional: STAGE-2/3/5 progress doc commit consolidation
