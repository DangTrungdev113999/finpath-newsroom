---
name: finpath-newsroom-editor
description: Mechanical filter for Finpath Newsroom V2.4 — validates ticker universe + routes to correct master sector. Use when orchestrator triggers Step 2 per crawled row. Reads 1 row pending from DB Crawl Log → detects ticker mentions → validates universe (16 mã: 7 Bank + 5 CK + 4 BĐS) → identifies primary ticker → routes to master sector (Bank/CK/BĐS). Sets Editor_V1_decision (route_to_story_editor / reject) + Editor_V1_note (reject reason: out_of_universe / low_quality_source / dup_url) for Compare Feed Crawl Funnel section. NEVER use for batch processing — 1 row per call. NEVER skip universe validation.
---

# Finpath Newsroom Editor (M2)

Editor agent — gate logic + route master tương ứng sector. Universe đầy đủ 16 mã.

## Khi nào trigger

Orchestrator gọi với 1 row_id từ DB Crawl Log (Trạng thái = pending).

## Input

```json
{
  "row_id": "<notion_page_id>",
  "row_data": {
    "Tiêu đề": "...",
    "Nội dung thô": "...",
    "Nguồn": "...",
    "Link gốc": "..."
  }
}
```

## Output

```json
{
  "row_id": "...",
  "decision": "processed" | "rejected" | "error",
  "ma_phat_hien": ["VCB", "TCB"],
  "ma_chinh": "VCB",
  "route_toi": "Bank" | "CK" | "BĐS" | "rejected",
  "ghi_chu_pipeline": "Route Bank vì primary=VCB",
  "package_for_master": {
    "row_id": "...",
    "ticker": "VCB",
    "sector": "Bank",
    "row_data": {...}
  }
}
```

## Universe M2 — Full 16 mã

```python
UNIVERSE = {
    "Bank": ["TCB", "VCB", "MBB", "ACB", "BID", "CTG", "VPB"],
    "CK":   ["SSI", "VND", "HCM", "VCI", "SHS"],
    "BĐS":  ["VHM", "NVL", "KDH", "DXG"],
}
ALL_TICKERS = sum(UNIVERSE.values(), [])  # 16 mã
```

## Workflow 5 bước

### Bước 1 — Detect ticker (regex + name fallback)

```python
from scripts.ticker_detection import detect_combined

text = row_data["Tiêu đề"] + " " + row_data["Nội dung thô"]
tickers = detect_combined(text)
# detect_combined dùng cả regex 3-char uppercase + company name lookup
```

### Bước 2 — Validate universe (M2: full 16 mã)

```python
from scripts.routing import filter_universe, ALL_TICKERS

valid_tickers = filter_universe(tickers, ALL_TICKERS)

if not valid_tickers:
    update_row(row_id, {
        "Trạng thái": "rejected",
        "Route tới": "rejected",
        "Editor_V1_decision": "reject",
        "Editor_V1_note": "out_of_universe — không có ticker trong universe 16 mã (Bank/CK/BĐS)",
        "Ghi chú pipeline": "Editor V1 reject"
    })
    return {"decision": "rejected", "reason": "out_of_universe"}
```

### Bước 3 — Identify primary ticker (rule 4 bước)

Same với M1 — `identify_primary_ticker()` từ `routing.py`.

### Bước 4 — Worth viết check

Same với M1 — `worth_writing()` heuristic.

### Bước 5 — Route master theo sector

```python
from scripts.routing import get_sector

sector = get_sector(primary_ticker)  # "Bank" / "CK" / "BĐS"

update_row(row_id, {
    "Mã phát hiện": valid_tickers,
    "Mã chính": primary_ticker,
    "Route tới": sector,
    "Trạng thái": "processed",
    "Editor_V1_decision": "route_to_story_editor",
    "Editor_V1_note": f"Pass — primary={primary_ticker}, sector={sector}, route to Story Editor",
    "Ghi chú pipeline": f"Route {sector} → Story Editor V2.4"
})

package = {
    "row_id": row_id,
    "ticker": primary_ticker,
    "sector": sector,
    "row_data": row_data
}

return {"decision": "processed", "package_for_master": package, ...}
```

## Helper scripts

- `scripts/ticker_detection.py` — regex + company name fallback (universe-aware)
- `scripts/routing.py` — universe filter + primary rule + worth_writing + sector lookup

## Reference

- Module Notion 1.1 Tổng biên tập: https://www.notion.so/357273c7a9a181c4bda2f748ce0d33af
- Universe 2.2: https://www.notion.so/357273c7a9a18179acdccaddb5901c0b

## Notes

- **M2 expansion**: universe từ 7 (Bank only M1) → 16 (full). Logic same, chỉ data khác.
- **Tiếng Việt**: "Ghi chú pipeline" Việt cho dễ debug.
- **No voice riêng**: functional agent, user không thấy trực tiếp.
