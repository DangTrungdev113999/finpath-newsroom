# DB Query Patterns — Bank Sector (local-first)

Code patterns for querying 6 Bank data sources + KB ngành Ngân hàng + pipeline.db persist.

## Imports

```python
from lib.pipeline_db import PipelineDB
from lib.finpath_api import FinpathAPI
from lib.kb_loader import KBLoader
import yaml, json, uuid

db = PipelineDB("data/pipeline.db")
api = FinpathAPI()
```

## Pattern 1 — BCTC Quarter / Bank Ratios (NIM, CASA, COF, NPL, LDR, ROE)

```python
# NIM, CASA, COF, NPL, LDR, P/E, P/B, ROE — quarterly + yearly
ratios = api.get_bank_ratios("VCB")
# Returns: {"quarterlyProfits": [...], "yearlyProfits": [...]}

# Full income statement (doanh thu, chi phí, lãi trước thuế)
full_income = api.get_full_income("VCB")
```

⚠️ **Quarter format in data**: check `ratios["quarterlyProfits"]` for field `quarter` (vd "2026-Q1"). Filter bằng list comprehension:
```python
q1_2026 = [r for r in ratios["quarterlyProfits"] if r.get("quarter") == "2026-Q1"]
```

## Pattern 2 — BCTC Annual (balance sheet + cashflow)

```python
# Full balance sheet (tài sản, nợ, vốn)
balance = api.get_full_balance_sheet("VCB")

# Cashflow
cashflow = api.get_cashflow("VCB")

# Tổng hợp income + balance cho phân tích năm
income = api.get_full_income("VCB")
```

## Pattern 3 — Targets vs Actual (per năm)

```python
with open("data/manual/targets.yaml", encoding="utf-8") as f:
    targets_data = yaml.safe_load(f)

# targets_data là dict: {ticker: {year: {Target_LNTT, Actual_LNTT, Target_TindungGrowth, ...}}}
vcb_2026 = targets_data.get("VCB", {}).get(2026, {})
# vcb_2026 = {"Target_LNTT": ..., "Actual_LNTT": ..., "Target_TindungGrowth": ..., ...}
```

## Pattern 4 — Credit Room (NHNN allocation)

```python
with open("data/manual/credit_room.yaml", encoding="utf-8") as f:
    credit_data = yaml.safe_load(f)

# credit_data là dict: {ticker: {year: {credit_room_pct, notes}}}
vcb_credit = credit_data.get("VCB", {}).get(2026, {})
# vcb_credit = {"credit_room_pct": ..., "notes": "..."}
```

## Pattern 5 — M&A deals

```python
events = api.get_events("VCB")
# events là list[dict] với type, date, title, description, ...
ma_events = [e for e in events if "M&A" in e.get("type", "") or "acquisition" in e.get("type", "").lower()]
# Sort by date desc
ma_events.sort(key=lambda e: e.get("date", ""), reverse=True)
ma_recent = ma_events[:5]
```

## Pattern 6 — Foreign room/ownership

```python
shareholders = api.get_shareholders("VCB")
# shareholders = {"data": [...], ...} hoặc list với foreign_owned_pct, foreign_room_pct, ...
# Lấy latest entry:
latest_foreign = shareholders[0] if isinstance(shareholders, list) else shareholders
```

## Pattern 7 — NHNN industry policies

```python
with open("data/manual/nhnn_circulars.yaml", encoding="utf-8") as f:
    nhnn_data = yaml.safe_load(f)

# nhnn_data là list[dict]: [{title, effective_date, summary, affected_topics}]
# Filter circulars có affected_topics chứa "NPL" và effective_date >= 2025-01-01
recent_npl = [
    c for c in nhnn_data
    if "NPL" in c.get("affected_topics", []) and c.get("effective_date", "") >= "2025-01-01"
]
recent_npl.sort(key=lambda c: c.get("effective_date", ""), reverse=True)
```

## Pattern 8 — Memory check (3 bài cũ về ticker)

```python
recent = db.recent_generated_news("VCB", limit=3)
# recent là list[dict] với fields: ticker, title, variety_guard_angle, insight_type, insight_final, published_at
# Variety guard: nếu 3 bài gần nhất cùng insight_type → flag warning
```

## Pattern 9 — Persist row generated_news

```python
article_id = str(uuid.uuid4())
db.insert_generated_news({
    "article_id": article_id,
    "row_id": row_id,                # FK → crawl_log.row_id
    "ticker": "VCB",
    "sector": "Bank",
    "title": title,
    "body": body,
    "word_count": word_count,
    "key_view": key_view,            # lạc quan|thận trọng|trung lập
    "insight_final": insight_final,  # 1 câu
    "insight_type": insight_type,    # phân loại cổ phiếu | decode | risk | catalyst | etc.
    "variety_guard_angle": brief["angle_label"],
    "accepted_hypothesis": 1 if accepted_hypothesis else 0,
    "data_sources_used": json.dumps(["BCTC_Quarter", "Targets", "KB", "Live_API"]),
    "brief_json": json.dumps(brief),
    "history_referenced": json.dumps(history_referenced),
    "pipeline_version": "V2",
    "status": "draft",
    "published_at": now_iso(),
    "pipeline_log": full_body_with_pipeline_log_toggle,
})
```

## Pattern 10 — Persist crawl_log Master_decision (V2.4)

```python
# Case ACCEPT — write_article
db.update_crawl_row(brief["row_id"], {
    "master_decision": "write_article",
    "master_note": "OK — data confirm insight, accepted_hypothesis: true",
    "status": "published"
})

# Case REJECT_NO_DATA
db.update_crawl_row(brief["row_id"], {
    "master_decision": "reject_no_data",
    "master_note": f"data_anchor_missing: {missing_keys_summary}. Accepted_hypothesis: false.",
    "status": "rejected"
})

# Case REJECT_DATA_CONFLICT
db.update_crawl_row(brief["row_id"], {
    "master_decision": "reject_data_conflict",
    "master_note": f"insight_data_conflict: {conflict_detail}. Accepted_hypothesis: false.",
    "status": "rejected"
})
```

## Pattern 11 — KB ngành Ngân hàng

```python
loader = KBLoader("kb/bank/")

# Lightweight check (Story Editor / Master Bước 4)
matches = loader.search(["Lottner"])
exists = len(matches) > 0

# Full content (Master Bước 4)
if matches:
    topic_body = loader.load_topic(matches[0]["path"])
    # topic_body = full markdown text của KB topic
```
