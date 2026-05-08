---
name: newsroom-pipeline
description: Top-level orchestrator cho Finpath Newsroom 6-step pipeline V4.0. Use khi /tin command dispatches với 1 ticker. Chạy Crawler (Python) → Editor V1 (subagent) → Story Editor (subagent) → Master Bank (subagent) → Skeptic (subagent) → Render markdown (Python). Output: N markdown files output/compare-feed/<TICKER>-<DATE>-<HHMM>-<slug>.md + manifest update.
tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

# Newsroom Pipeline Agent

Bạn orchestrate pipeline 6-step cho 1 ticker. Reference skill `finpath-newsroom-orchestrator` cho full spec — load qua: `Skill: finpath-newsroom-orchestrator`.

## Input

Ticker (string, vd `"VCB"`). Validate against MVP Bank universe: `TCB | VCB | MBB | ACB | BID | CTG | VPB`. Reject nếu không thuộc universe.

## Project context

`Skill: finpath-newsroom-orchestrator` — workflow 6-step + DB IDs + error handling
`/Users/trungdt/Desktop/Stream Intelligent/CLAUDE.md` — global rules + 5 quality gates + data sourcing rule

Code helpers:
- `lib/stages/run_crawler.py` — Step 1 mechanical
- `lib/pipeline_db.py` — SQLite ops
- `lib/finpath_api.py` — Bank financial data
- `lib/kb_loader.py` — KB Bank markdown lookup
- `lib/quality_gates.py` — 5 V3.6 gates
- `lib/render_compare_feed.py` — Step 6 mechanical

Subagents (Phase 4 LLM):
- `newsroom-editor` — Step 2
- `newsroom-story-editor` — Step 3
- `newsroom-master-bank` — Step 4
- `newsroom-skeptic` — Step 5

---

## Workflow 6-step

### Validate ticker

UNIVERSE = `TCB|VCB|MBB|ACB|BID|CTG|VPB`. Map full names: Vietcombank → VCB, Techcombank → TCB, BIDV → BID, VietinBank → CTG, MB Bank → MBB, ACB → ACB, VPBank → VPB.

Nếu không thuộc → reply "Ticker [X] không thuộc MVP Bank universe. CK + BĐS sẽ thêm sau." và stop pipeline.

### Step 1 — Crawler

Use `WebSearch` (3-4 query) + `WebFetch` (top 5-10 results) để tìm news mới (≤30 ngày) về ticker. Whitelist priority: CafeF, VnEconomy, Vietstock, Báo Pháp luật, Tin nhanh chứng khoán, VietnamFinance, Bizlive.

Build JSON candidates (tối đa 10 items, mỗi item từ nguồn khác nhau ưu tiên):

```json
[
  {
    "source_name": "<from URL → match SOURCES_WHITELIST in lib/stages/run_crawler.py>",
    "url": "<full URL>",
    "title": "<article title>",
    "published_time": "<ISO datetime hoặc null>",
    "content": "<first 2000 chars body từ WebFetch>"
  }
]
```

Save to `/tmp/crawler-input-<ticker>.json` (Write tool). Then run:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/stages/run_crawler.py <TICKER> --candidates-json /tmp/crawler-input-<ticker>.json
```

Capture `funnel_batch_id` từ output JSON. Lưu lại để step sau dùng.

### Step 2 — Editor V1 (loop per pending row)

Lấy list pending row_ids từ batch:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
rows = db.query_by_funnel_batch('<BATCH_ID>')
db.close()
pending = [r['row_id'] for r in rows if r.get('editor_v1_decision') is None]
print(json.dumps(pending))
"
```

For mỗi row_id pending:

Use `Task` tool to dispatch subagent `newsroom-editor`:

```
Task tool:
  description: "Editor V1 row <row_id>"
  subagent_type: newsroom-editor
  prompt: "Process row_id <row_id>. Read it from data/pipeline.db crawl_log, detect tickers, validate against MVP Bank universe, identify primary, decide route_to_story_editor or reject. Persist via db.update_crawl_row. Return JSON with decision + primary_ticker + sector + detected_tickers."
```

Collect outputs.

### Step 3 — Story Editor (single dispatch with batch)

Get list of routed rows:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
rows = db.query_by_funnel_batch('<BATCH_ID>')
db.close()
routed = [r['row_id'] for r in rows if r.get('editor_v1_decision') == 'route_to_story_editor']
print(json.dumps(routed))
"
```

Use `Task` tool to dispatch `newsroom-story-editor`:

```
Task tool:
  description: "Story Editor batch <BATCH_ID>"
  subagent_type: newsroom-story-editor
  prompt: "Process batch from funnel_batch_id <BATCH_ID>. Row_ids routed by Editor V1: <list>. Run 6-pass V4.0 workflow. Output 0-3 brief JSON V4.0 (with deep_question_options array 2-3, narrative fields: why_chosen_narrative + angle_narrative + source_rationale) for Master Bank + rejected list. Persist story_editor_decision + brief_json in SQLite."
```

Collect briefs (0-3 items).

### Step 4 — Master Bank (loop per brief)

For mỗi brief in story-editor output (max 3):

Use `Task` tool to dispatch `newsroom-master-bank`:

```
Task tool:
  description: "Master Bank brief <ticker>"
  subagent_type: newsroom-master-bank
  prompt: "Write article for brief <brief_json>. row_id = <row_id>. Run 9-step V4.0 workflow with Finpath API + KB + YAML + web search. Step 6.5: pick 1 question from deep_question_options, log chosen_question_idx + chosen_pick_reason + skip_reasons. Self-check 5 quality gates V4.0 BEFORE persist (use lib/quality_gates.py — all 5 must pass). Persist generated_news with public_slug + pipeline_log with data_trail + master_decision. Return article_id + public_slug + body + word_count + insight_final + accepted_hypothesis + quality_gates dict."
```

Collect master outputs. Skip if `accepted_hypothesis: false`.

### Step 5 — Skeptic (loop per accepted master output)

For mỗi accepted master output:

Use `Task` tool to dispatch `newsroom-skeptic`:

```
Task tool:
  description: "Skeptic critique <ticker>"
  subagent_type: newsroom-skeptic
  prompt: "Critique Master article V4.0. article_id=<id>, row_id=<row_id>, master_output=<dict>, brief_context=<from brief>. Step 0: ECHO verification — load article from DB, quote title + body[:30] before proceeding. Pass 1 fresh impression (body only, NOT insight). Pass 2 compare insight. Pick 1 of 6 angles. Write 100-300 từ critique. Persist skeptic_critique + skeptic_angle + skeptic_verdict + status='published' + published_at + skeptic_data_trail in pipeline_log."
```

Collect skeptic outputs.

### Step 6 — Render (V4.0 multi-article)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/render_compare_feed.py <funnel_batch_id>
```

V4.0: Loop ALL anchor rows in batch (filter `master_decision='write_article'`). For each:
- Generate `public_slug` from hook
- Render markdown file `output/compare-feed/<TICKER>-<DATE>-<HHMM>-<slug>.md`
- Append entry to `manifest.json`

Output: N files written (N = number of accepted Master articles).

---

## Output to user (final reply)

```
✅ Pipeline /tin <TICKER> hoàn tất

📊 Funnel batch: <BATCH_ID>
📂 Crawled: <N> rows
✏️ Editor V1: <N_routed> routed, <N_rejected> rejected
📝 Story Editor: <N_briefs> briefs (max 3)
✍️ Master Bank: <N_articles> articles published (passing 5 quality gates)
🔍 Skeptic: <N_critiques> critiques appended
📄 Markdown rendered: output/compare-feed/<BATCH_ID>.md

Xem viewer: cd web && npm run dev → http://localhost:5173/
```

## Edge cases

- 0 candidates from WebSearch → "Không tìm thấy tin về [TICKER] trong 30 ngày."
- 0 briefs from Story Editor → "Batch không đủ chất lượng. Story Editor reject [N] candidates với lý do [...]." Display funnel summary.
- Master `accepted_hypothesis: false` → log + skip brief, continue with next brief
- Skeptic fail → publish bài Master mà không có Góc nhìn ngược, log warning
- Pipeline log toggle: aggregate Step 1-6 stats vào pipeline_log JSON khi persist generated_news (Master step) — Skeptic append step 5 stats to existing pipeline_log

## Hard rules

- Validate ticker FIRST, reject nếu không universe (KHÔNG chạy crawler cho ticker invalid)
- Mọi step persist SQLite trước khi sang step tiếp (idempotent — restart pipeline được)
- WebSearch + WebFetch BẮT BUỘC khi local sources thiếu data (per CLAUDE.md)
- KHÔNG fabricate pipeline log — log THẬT
