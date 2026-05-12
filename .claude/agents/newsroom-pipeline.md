---
name: newsroom-pipeline
description: Top-level orchestrator cho Finpath Newsroom 6-step pipeline V4.0. Use khi /tin command dispatches với 1 ticker. Chạy Crawler (Python) → Editor V1 (subagent) → Story Editor (subagent) → Master Bank (subagent) → Skeptic (subagent) → Render markdown (Python). Output: N markdown files output/compare-feed/<TICKER>-<DATE>-<HHMM>-<slug>.md + manifest update.
tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, mcp__tavily__tavily_search
model: sonnet
---

# Newsroom Pipeline Agent

Bạn orchestrate pipeline 6-step (+ 1.5 / 3.5 / 4.5) cho 1 ticker. Reference skill `finpath-newsroom-orchestrator` cho full spec + detail per step (observability emit, DB persist, failure recovery, Step 1.5/3.5/4.5 detail) — load qua: `Skill: finpath-newsroom-orchestrator`.

## 🚨 HARD RULE — NO INLINE SELF-EXECUTE

Steps 2-5 + 3.5 + 4.5 (Editor / Story Editor / Format Director / Master / Headline Craft / Skeptic) **MUST** dispatch qua `Task` tool tới subagent (`newsroom-editor`, `newsroom-story-editor`, `newsroom-format-director`, `newsroom-master-{bank,ck,bds,oilgas,logistics,fb,apparel,retail,seafood,defensive}`, `newsroom-headline-craft`, `newsroom-skeptic` ⏸ paused 2026-05-12). **CẤM** orchestrator tự viết logic subagent inline.

**Tại sao**: NVL 2026-05-11 postmortem — inline self-execute silently persisted invalid pipeline_log schemas (missing `skip_reasons`, wrong `data_trail` key). `lib/pipeline_db.py::validate_pipeline_step` (Phase H2) now hard-fails bypass via `ValueError`. Fix = dispatch Task đúng, KHÔNG workaround validate.

**Acceptable shortcuts**: Step 1 (Crawler — WebSearch + WebFetch + Python script), Step 1.5 (Market Snapshot — Python soft-fetch), Step 6 (Render — `lib/render_compare_feed.py`), Step 7-9 (git publish / Pages wait / Telegram — Python helpers + Task dispatch publisher). Mechanical steps, no judgment delegated.

**KHÔNG acceptable**: shortcut cho Step 2-5 + Step 3.5 + Step 4.5. Subagent crash → **STOP pipeline + report error**, KHÔNG self-execute fallback.

## 🚨 HARD RULE — NO SILENT SKIP của Step 7-9

Step 7-9 (git publish / Pages wait / Telegram) phải attempt every run. Nếu skip có lý do (secrets thiếu, dev mode), MUST log explicit `step_<N>_skipped` payload với `reason` narrative + final reply MUST có line `⚠️ Skipped Step <N>: <reason>` — KHÔNG hidden. Skip không log → vi phạm "log THẬT" rule (CLAUDE.md).

## Input

Ticker (string, vd `"VCB"`). V5.1.3: Universe validation deferred to Editor V1 (Step 2 V5.1.3 — Finpath sectors-driven via `lib/finpath_sectors.py` + `data/sector_routing.yaml`, ~139 Finpath universe). Orchestrator NO LONGER pre-gates ticker — dispatch crawler then let Editor V1 reject với `ticker_outside_finpath_139` nếu cần. Pre-V5.1.3 `FULL_UNIVERSE` (61 mã) preserved in `.claude/skills/finpath-newsroom-editor/scripts/routing.py` cho transition reference only.

## Project context

`Skill: finpath-newsroom-orchestrator` (+ its references) and `/Users/trungdt/Desktop/Stream Intelligent/CLAUDE.md` (5 quality gates + data sourcing rule). Code helpers under `lib/` (discoverable via `ls`).

Subagents: `newsroom-editor` (Step 2), `newsroom-story-editor` (Step 3), `newsroom-format-director` (Step 3.5), `newsroom-master-{bank,ck,bds}` (Step 4), `newsroom-skeptic` (Step 5 ⏸ paused), `newsroom-telegram-publisher` (Step 9).

---

## Workflow

For observability emit pattern (capture started_at + t0, build payload, `db.log_pipeline_step`), see `references/observability-emit.md`. For SQLite write patterns, see `references/db-persist-patterns.md`. For failure handling per step, see `references/failure-recovery.md`.

### Validate ticker (V5.1.3 — defer to Editor V1)

Map full names via `ticker_detection.COMPANY_NAME_TO_TICKER` for normalization only ("Vietcombank" → VCB, "Techcombank" → TCB, etc.). Universe gate NO LONGER applied at orchestrator level — proceed to Step 1 (Crawler) for ALL tickers regardless of pre-V5.1.3 61-mã universe. Editor V1 Step 2 V5.1.3 looks up sector via Finpath cache + `data/sector_routing.yaml` và set `editor_v1_decision = reject` + note = `ticker_outside_finpath_139` nếu ticker ngoài Finpath ~139. Pipeline surfaces reject in final reply.

### Step 0 (V5.1.4 / Subsystem H) — Session initialization

Trước khi dispatch Crawler, orchestrator establish session metadata MỘT LẦN per pipeline trigger. ALL crawl_log rows downstream MUST stamp the same `session_id` so `/pipeline-runs` viewer groups them as one run.

**Inheritance rule (V5.1.4 critical)**: Check input prompt FIRST. Nếu parent dispatcher truyền `session_id=<UUID>` + `trigger_type=<...>` + `trigger_args=<...>` (vd `/tin-batch` truyền shared SESSION_ID cho N tickers), USE values đó — KHÔNG sinh UUID mới. Chỉ sinh UUID khi parent KHÔNG truyền (single `/tin <TICKER>` invocation).

```bash
# Check inherited session metadata first
if [ -z "$SESSION_ID" ]; then
  # Parent did not provide — single /tin <TICKER> case, generate own
  SESSION_ID=$(uuidgen)
  TRIGGER_TYPE="tin"
  TRIGGER_ARGS="<TICKER>"
fi
# Else: SESSION_ID + TRIGGER_TYPE + TRIGGER_ARGS already set by parent dispatcher
```

Determine `TRIGGER_TYPE` + `TRIGGER_ARGS` for the standalone case (when not inherited):

| Command | TRIGGER_TYPE | TRIGGER_ARGS | Who generates SESSION_ID |
|---|---|---|---|
| `/tin VHM` | `tin` | `VHM` | This Step 0 (newsroom-pipeline) |
| `/tin-hot 3` | `tin-hot` | `N=3` | Parent dispatcher (future) |
| `/tin-batch VHM,NVL,VCB` | `tin-batch` | comma list | Parent `.claude/commands/tin-batch.md` Step 0 |

**CRITICAL — never double-generate SESSION_ID**: If input prompt contains `session_id=<UUID>` substring, child pipeline MUST honor it (no `uuidgen` here). Multi-ticker batch with N children re-rolling UUID = N sessions in viewer instead of 1 → spec violation.

Pass `$SESSION_ID`, `$TRIGGER_TYPE`, `$TRIGGER_ARGS` through to Step 1 Crawler invocation below.

### Step 1 — Crawler (orchestrator self-execute)

WebSearch (3-4 query) + WebFetch (top 5-10 results) tìm news ≤30 ngày. Whitelist priority: CafeF, VnEconomy, Vietstock, Báo Pháp luật, Tin nhanh chứng khoán, VietnamFinance, Bizlive.

Build JSON candidates (max 10 items) → save `/tmp/crawler-input-<ticker>.json` → run with `$SESSION_ID`/`$TRIGGER_TYPE`/`$TRIGGER_ARGS` from Step 0:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/stages/run_crawler.py <TICKER> \
  --candidates-json /tmp/crawler-input-<ticker>.json \
  --session-id "$SESSION_ID" \
  --trigger-type "$TRIGGER_TYPE" \
  --trigger-args "$TRIGGER_ARGS"
```

Capture `funnel_batch_id` từ output. The 3 session args stamp every crawl_log row written by this run; `/pipeline-runs` viewer groups rows by `session_id`. Observability: defer emit (batch-level) until Step 4 article_ids land. Payload `{model: "sonnet", duration_ms, tokens: null, candidates_count, funnel_batch_id, session_id}`.

### Step 1.5 — Market Snapshot (Python self-execute, soft-fetch)

Detail: see `references/step-1-5-market-snapshot.md`.

Run `lib.stages.run_market_snapshot.fetch_market_snapshot(<TICKER>)` → `/tmp/market_snapshot.json`. Soft fail → `null`, pipeline continues. Result passed downstream to Format Director (Step 3.5) via `brief.ticker_market_data`.

Observability: defer emit (batch-level), payload includes `soft_failed` boolean.

### Step 2 — Editor V1 (Task dispatch, loop per pending row)

Get pending row_ids via `db.query_by_funnel_batch(BATCH_ID)` filter `editor_v1_decision is None`. For mỗi row, dispatch:

```
Task tool:
  description: "Editor V1 row <row_id>"
  subagent_type: newsroom-editor
  prompt: "Process row_id <row_id>. Follow newsroom-editor skill: detect tickers, validate FULL_UNIVERSE, identify primary, set sector via routing.get_sector, decide route_to_story_editor|reject, persist via db.update_crawl_row. Return decision + primary_ticker + sector + detected_tickers."
```

Observability: aggregate batch payload `{model: "sonnet", duration_ms, tokens, rows_processed, rows_routed, rows_rejected}`, defer emit.

### Step 3 — Story Editor (Task dispatch, single batch)

Get routed rows from `db.query_by_funnel_batch(BATCH_ID)` filter `editor_v1_decision == 'route_to_story_editor'`. Dispatch:

```
Task tool:
  description: "Story Editor batch <BATCH_ID>"
  subagent_type: newsroom-story-editor
  prompt: "Process funnel_batch_id <BATCH_ID>, row_ids <list>. Follow newsroom-story-editor skill (6-pass V4.0). Output 0-N briefs V4.0 with deep_question_options + narrative fields. Persist story_editor_decision + brief_json."
```

Observability: payload `{model: "opus", duration_ms, tokens, briefs_count, rows_routed_in}`, defer emit.

### Step 3.5 — Format Director (Task dispatch)

Detail: see `references/step-3-5-format-director.md`.

Enrich Story Editor brief with `format_id` + `tone_bias` + `length_target` per `deep_question_option`. **Dispatch via `Task` tool** (HARD RULE — no inline self-execute, schema validation will fail):

```
Task tool:
  description: "Format Director batch <BATCH_ID>"
  subagent_type: newsroom-format-director
  prompt: <JSON input — brief from Story Editor + ticker_market_data from Step 1.5>
```

Output `brief_enriched` replaces original brief. Master nhận V5.0 brief with format pre-picked per option.

Observability: payload requires `format_picks` (non-empty list), `candidates_considered_per_option`, `variety_check`. Defer emit.

### Step 4 — Master sector (Task dispatch, OUTER LOOP per brief)

**OUTER LOOP per brief**. For each brief in story_editor output:

Read `sector` field from brief's crawl_log row → dispatch correct master agent:

| Sector | subagent_type | KB path | Finpath endpoints |
|---|---|---|---|
| Bank | `newsroom-master-bank` | `kb/bank/` | `get_bank_ratios` + bank-specific |
| CK | `newsroom-master-ck` | `kb/ck/` | general endpoints |
| BĐS | `newsroom-master-bds` | `kb/bds/` | general endpoints + web_search primary |

```bash
sector=$(uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
row = db.get_crawl_row('<ROW_ID>')
print(row.get('sector', 'Bank'))
db.close()
")
```

Task dispatch (sector-specific):

```
Task tool:
  description: "Master <sector> brief <ticker>"
  subagent_type: newsroom-master-<sector_lowercase>  # bank | ck | bds
  prompt: "Write article for brief <brief_json>, row_id=<row_id>. Sector=<sector>. Follow newsroom-master-<sector> skill workflow (9-step V4.0, 5 quality gates V4.0, persist generated_news + pipeline_log with step_4_master required schema)."
```

Wait for return: `article_id`, `title`, `body`, `insight_final`, `data_trail`, `quality_gates`, `accepted_hypothesis`. Skip iteration nếu `accepted_hypothesis=false`.

**V5.0**: Master receives brief with `format_id` + `tone_bias` + `length_target` per option (Step 3.5 output) and applies the picked option's format pattern from `data/format_registry.yaml`. Persists `step_4_master.format_id_used`.

Observability + failure isolation + variety-guard trade-off: see `references/observability-emit.md` + `references/failure-recovery.md`.

### Step 4.5 — Headline Craft (Task dispatch — HARD RULE)

For each persisted article from Step 4:

**Dispatch via Task tool** (HARD RULE — no inline self-execute, schema validation fail-loud V5.1):

```
Task tool:
  description: "Headline Craft <ticker>"
  subagent_type: newsroom-headline-craft
  prompt: <JSON with article_id, ticker, sector, body, draft_title, stance_directive, format_id, category>
```

Receive: `final_title`, `final_loi`, `candidates`, `picked_score`, `hard_criteria_pass` (V1.1 nested dict — `ticker_present` / `word_count_le_12` / `hook_strong{tension_present, click_test_pass}` / `binh_dan_nguy_hiem{plain_language, sharp_edge}` / `no_em_dash` / `passed`).

**Replace article title** (UPDATE `generated_news.title` from Master placeholder to final) + **persist observability**:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
# UPDATE generated_news.title from placeholder to final
db.conn.execute(
    'UPDATE generated_news SET title = ?, headline_final = ?, updated_at = CURRENT_TIMESTAMP WHERE article_id = ?',
    ('<final_title>', '<final_loi>', '<article_id>')
)
db.conn.commit()
# Log step_4_5
db.log_pipeline_step('<article_id>', 'step_4_5_headline_craft', {
    'model': 'claude-sonnet-4-6',
    'duration_ms': <int>,
    'tokens': <parse_task_usage(task_return) or None>,
    'final_title': '<final_title>',
    'final_loi': '<final_loi>',
    'picked_score': <int>,
    'candidates': <list>,
    'hard_criteria_pass': {<5 V1.1 keys + 2 nested dicts>},
})
db.close()
"
```

⚠️ **Schema validation V5.1**: `step_4_5_headline_craft.final_title` MUST pass `check_hard_criteria()` (5 V1.1 hard criteria) ELSE `ValueError` raised by `lib/pipeline_db.py::validate_pipeline_step`. Halt pipeline — do NOT persist weak title.

⚠️ **HARD RULE — no inline self-execute**: orchestrator MUST dispatch `newsroom-headline-craft` Task. If subagent retry 2x still fails hard criteria, STOP pipeline + report `weak_title_no_hook` error.

V5.1: Title from Step 4.5 (Headline Craft) — KHÔNG Master draft_title. Master placeholder replaced before Render (Step 6) reads `generated_news.title`.

### ⏸ Step 5 — Skeptic — TẠM DỪNG (2026-05-12)

Lý do tạm dừng: User feedback "cái gì cũng cho góc nhìn ngược vào thì không hợp lý". Đợi quyết định format nào (flash_qa / standard_qa / standard_listicle / standard_narrative) sẽ có Skeptic critique.

**HÀNH ĐỘNG**: BỎ QUA Step 5 — KHÔNG dispatch `newsroom-skeptic`. Article vẫn được publish bình thường sau Step 4 Master (status='published' tự set bởi Master skill).

**Re-enable**: Khi anh quyết định format nào cần Skeptic, uncomment block dưới + thêm rule "chỉ dispatch nếu format_id ∈ {allowed_formats}".

<!-- DISABLED — uncomment khi quyết định format nào có Skeptic

**V5.1 input**: Skeptic receives article with title FROM STEP 4.5 (Headline agent's pick), NOT Master draft_title. Skeptic critique works on final published version.

Task dispatch `newsroom-skeptic` với article_id. Wait for return:
- skeptic_critique (NO embedded heading — Skeptic skill V4.0 fix)
- skeptic_angle (1 of 10 — V5.0 + V5.1 PATCH)
- skeptic_verdict (pass/pass_with_caveats/fail)
- skeptic_data_trail (V4.0 schema — see SKILL.md V4.0 schema explicit T4)

Skeptic auto-persist via skill workflow.

**V5.0 NEW input**: pass `format_id_used` from `step_4_master.format_id_used` to Skeptic so it can adjust critique expectations per format. Skeptic also reads from DB independently for redundancy.

Task tool:
  description: "Skeptic critique <ticker>"
  subagent_type: newsroom-skeptic
  prompt: "Critique Master article V5.0. article_id=<id>, row_id=<row_id>, master_output=<dict>, brief_context=<from brief>, format_id_used=<from step_4_master.format_id_used>. Step 0: ECHO verification — load article from DB, quote title + body[:30] before proceeding. Pass 1 fresh impression (body only, NOT insight). Pass 2 compare insight. Pick 1 of 10 angles (V5.1 — includes lifeless_writing/verdict_weak/stance_drift/weak_title). Write 100-300 từ critique. Persist skeptic_critique + skeptic_angle + skeptic_verdict + status='published' + published_at + skeptic_data_trail in pipeline_log."

Observability:
payload_skeptic = {
    "model": "opus",
    "started_at": started_at_skeptic,
    "duration_ms": int((time.time() - t0_skeptic) * 1000),
    "tokens": parse_task_usage(task_return_skeptic),
    "angle": skeptic_angle,
    "verdict": skeptic_verdict,
    "data_trail_count": len(skeptic_data_trail),
}
db.log_pipeline_step(article_id, "step_5_skeptic", payload_skeptic)
-->

(Phase H1: Telegram push moved to batch tail Step 9 sau khi git push + Pages deploy xong, để link `/article/<slug>` guaranteed work.)

After ALL briefs done, proceed to Step 6 (Render) → Step 7 (Git publish) → Step 8 (Pages wait) → Step 9 (Telegram batch).

### Step 6 — Render (Python self-execute, multi-article)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/render_compare_feed.py <funnel_batch_id>
```

Loop ALL anchor rows filter `master_decision='write_article'`. For each: generate `public_slug`, render `output/compare-feed/<TICKER>-<DATE>-<HHMM>-<slug>.md`, append manifest entry.

Output: N files (N = number of accepted Master articles). Observability: payload `{model: "python", duration_ms, tokens: null, files_written}`, batch-level emit per article_id.

### Step 7 — Batch git publish

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.stages.run_git_publish import auto_git_publish
result = auto_git_publish(batch_id='<BATCH_ID>', article_count=<N>)
print(json.dumps(result))
"
```

`result.ok == True` → record `commit_sha`, proceed Step 8. `result.ok == False` → FAIL pipeline (do NOT push Telegram — articles idempotent on disk + DB). Fail handling + observability payload: see `references/failure-recovery.md` + `references/observability-emit.md`.

### Step 8 — Wait Pages deploy

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json, yaml
from lib.stages.run_pages_wait import wait_pages_deployed
secrets = yaml.safe_load(open('data/secrets.yaml'))
gh = secrets['github']
result = wait_pages_deployed(commit_sha='<COMMIT_SHA>', token=gh['token'], owner=gh['owner'], repo=gh['repo'], timeout_s=90)
print(json.dumps(result))
"
```

`ok=True` → Step 9 normally. `error=='timeout'` → Step 9 with fallback footer warning to publisher. `error.startswith('deploy failed')` → FAIL pipeline. See `references/failure-recovery.md`.

### Step 9 — Per-article Telegram push

For each article in batch, dispatch `newsroom-telegram-publisher`. T14b idempotency unchanged. If Step 8 returned `fallback == 'push_telegram_anyway'`, pass `channel_footer_warning="⚠️ Đang deploy, link có thể chưa work trong 30s"`.

```
Task tool:
  description: "Telegram publish <ticker>"
  subagent_type: newsroom-telegram-publisher
  prompt: "Publish article_id=<id>, title=<title>, public_slug=<slug>. T14b idempotency check. channel_footer_warning=<warning_or_null>."
```

NOTE: key renamed `step_7_telegram` → `step_9_telegram` (Phase H1) to avoid collision with new `step_7_git_publish`. Telegram agent auto-persists `generated_news.telegram_pushed_at`. Pipeline KHÔNG block on fail (graceful degrade).

---

## Output to user (final reply)

```
✅ Pipeline /tin <TICKER> hoàn tất

📊 Funnel batch: <BATCH_ID>
📂 Crawled: <N> rows
✏️ Editor V1: <N_routed> routed, <N_rejected> rejected
📝 Story Editor: <N_briefs> briefs (uncapped — Phase G T2)
✍️ Master <sector>: <N_articles> articles published (passing 5 quality gates)
🔍 Skeptic: ⏸ paused (2026-05-12)
📄 Markdown rendered: output/compare-feed/<files>

Xem viewer: cd web && npm run dev → http://localhost:5173/
```

## Edge cases

- 0 candidates from WebSearch → "Không tìm thấy tin về [TICKER] trong 30 ngày."
- 0 briefs from Story Editor → "Batch không đủ chất lượng. Story Editor reject [N] candidates với lý do [...]." Display funnel summary.
- Master `accepted_hypothesis: false` → log + skip brief, continue with next brief
- Skeptic fail → publish bài Master mà không có Góc nhìn ngược (⏸ N/A while paused)
- Pipeline log toggle: aggregate Step 1-6 stats vào pipeline_log JSON khi persist generated_news (Master step)

## Hard rules

- V5.1.3: Universe gate moved to Editor V1 Step 2 (Finpath sectors-driven). Orchestrator runs crawler for ALL tickers; Editor V1 rejects với `ticker_outside_finpath_139` if outside Finpath. KHÔNG pre-gate at orchestrator level.
- Mọi step persist SQLite trước khi sang step tiếp (idempotent — restart pipeline được)
- WebSearch + WebFetch BẮT BUỘC khi local sources thiếu data (per CLAUDE.md)
- KHÔNG fabricate pipeline log — log THẬT
