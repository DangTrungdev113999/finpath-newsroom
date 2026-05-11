---
name: finpath-newsroom-orchestrator
description: Top-level orchestrator V2.4 cho Finpath Newsroom — viết bài tin chuyên sâu về cổ phiếu Việt Nam (61 mã thuộc 3 sector Bank/CK/BĐS). Use khi user gõ "tin về [TICKER]", "viết tin [TICKER]", hoặc bất cứ yêu cầu nào về tạo bài tin/phân tích chuyên gia/news report về 1 mã cổ phiếu trong 61 mã universe (27 Bank + 30 CK + 4 BĐS — see routing.FULL_UNIVERSE). Pipeline 6 step: Crawler → Editor V1 → Story Editor V2.4 → Master sector → Skeptic V2.4 → Publish + Compare Feed prepend. ALWAYS use this skill when ticker xuất hiện, kể cả không nói "viết tin" rõ ràng. NEVER use cho ticker ngoài 61 mã universe.
---

# Orchestrator V2.4 — Pipeline 6 step

Top-level coordinator gọi 5 sub-skills tuần tự + persist + render Compare Feed.

## Trigger
- User gõ "tin về [TICKER]" / "viết tin [TICKER]" / "phân tích [TICKER]"
- Bất cứ message nào có ticker 61 mã universe + intent tạo content
- KHÔNG trigger cho ticker ngoài universe → reply "Ticker [X] không thuộc 61 mã universe Finpath Newsroom."

## Universe 61 mã

| Sector | Count | Source of truth | Master skill |
|---|---|---|---|
| Bank | 27 (HOSE 16 + HNX 4 + UPCOM 7) | `routing.BANK_UNIVERSE` | `finpath-newsroom-master-bank` |
| CK | 30 (HOSE 5 + HNX 15 + UPCOM 10) | `routing.CK_UNIVERSE` | `finpath-newsroom-master-ck` |
| BĐS | 4 (VHM, NVL, KDH, DXG) | `routing.BDS_UNIVERSE` | `finpath-newsroom-master-bds` |

Routing module: `.claude/skills/finpath-newsroom-editor/scripts/routing.py::FULL_UNIVERSE` (single source of truth — KHÔNG hard-code enumeration trong skill/agent file).

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

- User gõ ticker không trong 16 → reply universe limitation
- Ticker = KBC → reply "KBC defer trong V2.4 (BĐS KCN khác pattern)"
- 2 ticker trong message (vd "VCB vs TCB") → trigger pipeline cho mỗi ticker (2 separate runs)
- User gõ tên đầy đủ "Vietcombank" → map về VCB

## References
- `references/compare-feed-layout.md` — Compare Feed prepend layout 2 cột
- `references/pipeline-log-format.md` — Pipeline log Step 1-4 format
