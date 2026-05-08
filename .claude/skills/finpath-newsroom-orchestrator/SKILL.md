---
name: finpath-newsroom-orchestrator
description: Top-level orchestrator V2.4 cho Finpath Newsroom — viết bài tin chuyên sâu về cổ phiếu Việt Nam (16 mã thuộc 3 sector Bank/CK/BĐS). Use khi user gõ "tin về [TICKER]", "viết tin [TICKER]", hoặc bất cứ yêu cầu nào về tạo bài tin/phân tích chuyên gia/news report về 1 mã cổ phiếu trong universe (TCB/VCB/MBB/ACB/BID/CTG/VPB/SSI/VND/HCM/VCI/SHS/VHM/NVL/KDH/DXG). Pipeline 6 step: Crawler → Editor V1 → Story Editor V2.4 → Master sector → Skeptic V2.4 → Publish + Compare Feed prepend. ALWAYS use this skill when ticker xuất hiện, kể cả không nói "viết tin" rõ ràng. NEVER use cho ticker ngoài 16 universe.
---

# Orchestrator V2.4 — Pipeline 6 step

Top-level coordinator gọi 5 sub-skills tuần tự + persist + render Compare Feed.

## Trigger
- User gõ "tin về [TICKER]" / "viết tin [TICKER]" / "phân tích [TICKER]"
- Bất cứ message nào có ticker 16 universe + intent tạo content
- KHÔNG trigger cho ticker ngoài universe → reply "Ticker [X] không thuộc 16 mã universe Finpath Newsroom."

## Universe 16 mã

| Sector | Tickers | Master skill |
|---|---|---|
| Bank (7) | TCB, VCB, MBB, ACB, BID, CTG, VPB | `finpath-newsroom-master-bank` |
| CK (5) | SSI, VND, HCM, VCI, SHS | `finpath-newsroom-master-ck` |
| BĐS (4) | VHM, NVL, KDH, DXG | `finpath-newsroom-master-bds` |

⚠️ KBC defer (BĐS KCN, pattern khác).

## 6-step pipeline

### Step 1 — Crawler invoke
Skill: `finpath-newsroom-crawler`. Input: ticker. Output: N rows in DB Crawl Log với Funnel_batch_id + Published_time.

### Step 2 — Editor V1 invoke (per row)
Skill: `finpath-newsroom-editor`. Cho mỗi row pending:
- Detect ticker + validate universe + identify primary + route sector
- Set `Editor_V1_decision` (route_to_story_editor / reject) + `Editor_V1_note`

### Step 3 — Story Editor V2.4 invoke (per batch)
Skill: `finpath-newsroom-story-editor`. Input: tất cả rows với `Editor_V1_decision = route_to_story_editor` (cùng sector). Output: 0-3 brief JSON. 
Persist `Story_Editor_decision` + `Story_Editor_note` vào DB Crawl Log.

### Step 4 — Master sector invoke (per brief)
Skill: `finpath-newsroom-master-{bank|ck|bds}` theo sector. Input: brief + row_id. Output: bài 200-350 từ + insight_final + accepted_hypothesis.
Persist vào DB Generated News + DB Crawl Log Master_decision.

### Step 5 — Skeptic V2.4 invoke (per master output)
Skill: `finpath-newsroom-skeptic`. Input: master_output + brief_context (V2.4). Output: critique 100-300 từ + critique_angle (1 of 6).
Append "## Góc nhìn ngược" vào page body + update DB properties.

### Step 6 — Publish + Compare Feed prepend
- Update DB Generated News: `Trạng thái = published`, `Published at = now`
- Prepend section vào Compare Feed page (newest-first)
- Layout 2 cột chi tiết: see `references/compare-feed-layout.md`

## DB IDs

| Resource | ID |
|---|---|
| DB Crawl Log | `8aad4abe-496f-480f-ad13-8996d22fe447` |
| DB Generated News | `74a01cc3-c3c4-4dbe-a43f-c7572fa68d20` |
| Compare Feed page | `359273c7-a9a1-81bd-88f6-ebf0d954551d` |
| Bank Sector hub | `359273c7-a9a1-810f-9306-cb6227d9c94a` |

## Pipeline log toggle (V2)

Master tạo `<details>📋 Pipeline log</details>` vào page body row Generated News. Format Step 1-4: see `references/pipeline-log-format.md`. Skeptic append Step 5-6.

## Compare Feed prepend logic

Layout 2 cột (cột trái = bài AI viết lại với 💡 Insight callout, cột phải = raw + meta + Crawl Funnel section + raw text expand). Detail spec: see `references/compare-feed-layout.md`.

⚠️ **Crawl Funnel section V2.4 mới**: Default COLLAPSE, list format, đặt TRƯỚC raw text expand. Render từ DB Crawl Log filter by `Funnel_batch_id` của primary row.

## Error handling

- Step 1 fail (Crawler) → reply user "Không tìm thấy tin về [TICKER] trong 30 ngày. Có thể ticker này ít news hoặc network issue."
- Step 3 output 0 brief (Story Editor reject all) → reply "Batch tin về [TICKER] không đủ chất lượng để viết sâu. Story Editor đã reject [N] candidates với lý do [...]." Display funnel summary.
- Step 4 reject (Master accepted_hypothesis: false) → log to Crawl Log + skip this brief, continue với brief khác trong batch
- Step 5 fail (Skeptic) → publish bài Master mà không có "Góc nhìn ngược" section, log warning

## Edge cases

- User gõ ticker không trong 16 → reply universe limitation
- Ticker = KBC → reply "KBC defer trong V2.4 (BĐS KCN khác pattern)"
- 2 ticker trong message (vd "VCB vs TCB") → trigger pipeline cho mỗi ticker (2 separate runs)
- User gõ tên đầy đủ "Vietcombank" → map về VCB

## References
- `references/compare-feed-layout.md` — Compare Feed prepend layout 2 cột
- `references/pipeline-log-format.md` — Pipeline log Step 1-4 format
