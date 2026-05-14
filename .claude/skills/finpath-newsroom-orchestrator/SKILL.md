---
name: finpath-newsroom-orchestrator
description: Top-level orchestrator V2.4 cho Finpath Newsroom — viết bài tin chuyên sâu về cổ phiếu Việt Nam (V5.1.3 — ~139 mã Finpath universe, sector routing qua Finpath cache + sector_routing.yaml). Use khi user gõ "tin về [TICKER]", "viết tin [TICKER]", hoặc bất cứ yêu cầu nào về tạo bài tin/phân tích chuyên gia/news report về 1 mã cổ phiếu. Pipeline 6 step: Crawler → Editor V1 → Story Editor V2.4 → Master sector → Skeptic V2.4 → Publish + Compare Feed prepend. ALWAYS use this skill when ticker xuất hiện, kể cả không nói "viết tin" rõ ràng. ALWAYS dispatch ticker to Editor V1 (Step 2 V5.1.3 — Finpath sectors-driven). Editor V1 validates ticker against ~139 Finpath universe + routes to appropriate master. NEVER pre-gate at orchestrator level — let Editor V1 reject if outside Finpath.
---

# Orchestrator V2.4 — Pipeline 6 step

Top-level coordinator gọi 5 sub-skills tuần tự + persist + render Compare Feed.

## Trigger
- User gõ "tin về [TICKER]" / "viết tin [TICKER]" / "phân tích [TICKER]"
- Bất cứ message nào có ticker + intent tạo content
- ALWAYS dispatch ticker to Editor V1 (Step 2 V5.1.3) — Editor V1 validates against Finpath ~139 universe và reject với note `ticker_outside_finpath_139` nếu không thuộc. KHÔNG pre-gate at orchestrator level.

## Universe — V5.1.3 (~139 mã Finpath)

Universe gate now lives in Editor V1 Step 2 V5.1.3 (Finpath sectors-driven). Orchestrator KHÔNG hard-code enumeration. Sector routing flows:

| Sector parent (Finpath) | Master skill |
|---|---|
| Tài chính (Bank/CK) | route via `sector_code` → `data/sector_routing.yaml` → `finpath-newsroom-master-bank` hoặc `finpath-newsroom-master-ck` |
| Bất động sản (residential subset) | `finpath-newsroom-master-bds` |
| Khác (industrial/consumer/...) | Editor V1 reject hoặc route generic — see `data/sector_routing.yaml` |

Source of truth: `lib/finpath_sectors.py` (API client + cache) + `data/sector_routing.yaml` (sector_code → master_route mapping). Pre-V5.1.3 hardcoded `FULL_UNIVERSE` preserved cho transition reference only — KHÔNG dùng runtime.

⚠️ KBC defer (BĐS KCN, pattern khác).

## 6-step pipeline

### Step 1 — Crawler invoke
Skill: `finpath-newsroom-crawler`. Input: ticker. Output: N rows in `crawl_log` table (`data/pipeline.db`) với `funnel_batch_id` + `published_time`.

### Step 2 — Editor V1 invoke (per row)
Skill: `finpath-newsroom-editor`. Cho mỗi row pending:
- Detect ticker + validate universe + identify primary + route sector
- Set `editor_v1_decision` (route_to_story_editor / reject) + `editor_v1_note`

### Step 3 — Story Editor V2.4 invoke (per batch)
Skill: `finpath-newsroom-story-editor`. Input: tất cả rows với `editor_v1_decision = route_to_story_editor` (cùng sector). Output: 0-3 brief JSON. 
Persist `story_editor_decision` + `story_editor_note` vào `crawl_log`.

### Step 4 — Master sector invoke (per brief)
Skill: `finpath-newsroom-master-{bank|ck|bds}` theo sector. Input: brief + row_id. Output: bài 200-350 từ + insight_final + accepted_hypothesis.
Persist vào `generated_news` table + `crawl_log` master_decision.

### Step 5 — Skeptic V2.4 invoke (per master output)
Skill: `finpath-newsroom-skeptic`. Input: master_output + brief_context (V2.4). Output: critique 100-300 từ + critique_angle (1 of 6).
Append "## Góc nhìn ngược" vào article body + update `generated_news` properties.

### Step 6 — Publish + Compare Feed render
- Update `generated_news`: `status = published`, `published_at = now`
- Render Compare Feed to `output/compare-feed/<batch>.md` (newest-first)
- Layout 2 cột chi tiết: see `references/compare-feed-layout.md`

## Local data sources

| Resource | Location |
|---|---|
| DB Crawl Log | `data/pipeline.db` table `crawl_log` via `lib/pipeline_db.py` |
| DB Generated News | `data/pipeline.db` table `generated_news` via `lib/pipeline_db.py` |
| Compare Feed output | `output/compare-feed/<batch>.md` — Phase 6 DEFER rendering |
| Bank Sector hub | Read-only via Notion MCP at one-time bootstrap only — NOT runtime |

## Pipeline log toggle (V2)

Master tạo `<details>📋 Pipeline log</details>` vào article body row `generated_news`. Format Step 1-4: see `references/pipeline-log-format.md`. Skeptic append Step 5-6.

## Compare Feed prepend logic

Layout 2 cột (cột trái = bài AI viết lại với 💡 Insight callout, cột phải = raw + meta + Crawl Funnel section + raw text expand). Detail spec: see `references/compare-feed-layout.md`.

⚠️ **Crawl Funnel section V2.4 mới**: Default COLLAPSE, list format, đặt TRƯỚC raw text expand. Render từ `crawl_log` filter by `funnel_batch_id` của primary row (via `db.query_by_funnel_batch(batch_id)`).

## Error handling

- Step 1 fail (Crawler) → reply user "Không tìm thấy tin về [TICKER] trong 30 ngày. Có thể ticker này ít news hoặc network issue."
- Step 3 output 0 brief (Story Editor reject all) → reply "Batch tin về [TICKER] không đủ chất lượng để viết sâu. Story Editor đã reject [N] candidates với lý do [...]." Display funnel summary.
- Step 4 reject (Master accepted_hypothesis: false) → log to `crawl_log` + skip this brief, continue với brief khác trong batch
- Step 5 fail (Skeptic) → publish bài Master mà không có "Góc nhìn ngược" section, log warning

## Edge cases

- User gõ ticker ngoài Finpath ~139 → Editor V1 reject với note `ticker_outside_finpath_139`; orchestrator surfaces reject message (KHÔNG pre-gate at orchestrator level — V5.1.3)
- Ticker = KBC → reply "KBC defer trong V2.4 (BĐS KCN khác pattern)"
- 2 ticker trong message (vd "VCB vs TCB") → trigger pipeline cho mỗi ticker (2 separate runs)
- User gõ tên đầy đủ "Vietcombank" → map về VCB

## References (load on-demand)

Detail beyond core flow above — load when needed:

- `references/observability-emit.md` — pipeline_log emit pattern per step (required schema V5.0+, model convention, batch vs per-article)
- `references/db-persist-patterns.md` — SQLite write patterns via `PipelineDB` API (Step 4 insert, batch-level deferred emits, Step 6-9 persist)
- `references/failure-recovery.md` — per-step failure handling (soft vs hard fail), brief-level isolation, batch survival, idempotency
- `references/step-1-5-market-snapshot.md` — Market Snapshot Python helper detail (soft-fetch contract, downstream tone_bias)
- `references/spawn-step-agent.md` — V5.1.5 transport: `lib/stages/spawn_step_agent.py` dispatch (claude -p --agent fresh process) thay Task tool. Pattern per step, model presets, parsing, failure modes.
- `references/step-3-5-format-director.md` — Format Director dispatch detail (input/output contract, schema validation, variety check)
- (V5.1.8 — Step 4.5 Headline Craft retired; Master self-titles via prompt section in 10 sector prompts)
- `references/compare-feed-layout.md` — Compare Feed prepend layout 2 cột
- `references/pipeline-log-format.md` — Pipeline log Step 1-4 format
