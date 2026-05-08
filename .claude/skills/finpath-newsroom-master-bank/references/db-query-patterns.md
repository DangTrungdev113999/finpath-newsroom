# DB Query Patterns — Bank Sector

Code patterns for querying 6 Bank Notion DBs + KB ngành Ngân hàng + DB Crawl Log persist.

## Pattern 1 — BCTC Quarter row by Ticker+Quarter

```python
# DB BCTC Bank Quarter
result = query_data_sources(
    data_source_id="ee0e7746-f057-4350-bad7-42f461921aa8",
    sql="""
        SELECT * FROM data_source 
        WHERE "Ticker" = 'VCB' AND "Quarter" = '2026-Q1' 
        LIMIT 1
    """
)
```

⚠️ **Quarter format**: `YYYY-QN` (vd "2026-Q1", "2025-Q4"). Không dùng "Q1/2026" hay "1Q26".

## Pattern 2 — BCTC Annual row by Ticker+Year

```python
result = query_data_sources(
    data_source_id="a76139a4-aab9-42e1-8837-99b202a13abe",
    sql="""
        SELECT * FROM data_source 
        WHERE "Ticker" = 'VCB' AND "Year" = 2025
        LIMIT 1
    """
)
```

## Pattern 3 — Targets vs Actual (per năm)

```python
result = query_data_sources(
    data_source_id="766a24a8-1328-48b5-8c73-b0c5574c9be9",
    sql="""
        SELECT * FROM data_source 
        WHERE "Ticker" = 'VCB' AND "Year" = 2026
        LIMIT 1
    """
)
# Có Target_LNTT, Actual_LNTT, Target_TindungGrowth, Actual_..., etc.
```

## Pattern 4 — Credit Room (NHNN allocation)

```python
result = query_data_sources(
    data_source_id="6c0335b0-0577-4b29-902f-932ae8f9a203",
    sql="""
        SELECT "Ticker", "Year", "Credit_room_pct", "Notes" 
        FROM data_source 
        WHERE "Ticker" = 'VCB' AND "Year" = 2026
    """
)
```

## Pattern 5 — M&A deals

```python
result = query_data_sources(
    data_source_id="55d84524-c800-4416-bc40-e612c278173b",
    sql="""
        SELECT * FROM data_source 
        WHERE "Acquirer" = 'VCB' OR "Target" = 'VCB'
        ORDER BY "Date" DESC
        LIMIT 5
    """
)
```

## Pattern 6 — Foreign room/ownership

```python
result = query_data_sources(
    data_source_id="7963c23c-b7db-4c5f-bee4-b0f388596456",
    sql="""
        SELECT * FROM data_source 
        WHERE "Ticker" = 'VCB'
        ORDER BY "Date" DESC
        LIMIT 1
    """
)
```

## Pattern 7 — NHNN industry policies

```python
result = query_data_sources(
    data_source_id="cfebb902-5615-49e9-ae5e-f017e71f80ff",
    sql="""
        SELECT "Title", "Effective_date", "Summary", "Affected_topics" 
        FROM data_source 
        WHERE "Effective_date" >= '2025-01-01' 
        AND "Affected_topics" LIKE '%NPL%'
        ORDER BY "Effective_date" DESC
    """
)
```

## Pattern 8 — Memory check (3 bài cũ về ticker)

```python
result = query_data_sources(
    data_source_id="74a01cc3-c3c4-4dbe-a43f-c7572fa68d20",
    sql="""
        SELECT "Tiêu đề", "Variety_guard_angle", "Insight_type", "Insight_line", "date:Published at:start" as published_at
        FROM data_source 
        WHERE "Ticker" = 'VCB' AND "Trạng thái" = 'published'
        ORDER BY "date:Published at:start" DESC 
        LIMIT 3
    """
)
# Variety guard: nếu 3 bài gần nhất cùng Insight_type → flag warning
```

## Pattern 9 — Persist row Generated News

```python
new_row = create_pages(
    parent={"data_source_id": "74a01cc3-c3c4-4dbe-a43f-c7572fa68d20"},
    pages=[{
        "properties": {
            "Tiêu đề": title,
            "Ticker": "VCB",
            "Sector": "Bank",
            "Author": "Chuyên gia ngân hàng",
            "Bài chính": body,
            "Key view": key_view,  # lạc quan|thận trọng|trung lập
            "Key claims": key_claims_summary,
            "Insight_line": insight_final,  # 1 câu
            "Insight_type": insight_type,  # phân loại cổ phiếu | decode | risk | catalyst | etc.
            "Why_chosen": brief["why_chosen"],
            "Brief_JSON": json.dumps(brief),
            "Memory_check_passed": "__YES__" if memory_ok else "__NO__",
            "Story_Editor_accepted": "__YES__",
            "Variety_guard_angle": brief["angle"],
            "Pipeline_version": "V2",
            "Trạng thái": "draft",
            "Word_count": word_count,
            "Data_sources_used": ["BCTC_Quarter", "Targets", "KB", "Live_API"],
            "Tin gốc": [crawl_log_row_url],  # relation
            "date:Published at:start": now_iso(),
            "date:Published at:is_datetime": 1,
        },
        "content": full_body_with_pipeline_log_toggle
    }]
)
```

## Pattern 10 — Persist DB Crawl Log Master_decision (V2.4)

```python
# Case ACCEPT — write_article
update_pages(
    page_id=brief["row_id"],
    properties={
        "Master_decision": "write_article",
        "Master_note": "OK — data confirm insight, accepted_hypothesis: true",
        "Trạng thái": "published"
    }
)

# Case REJECT_NO_DATA
update_pages(
    page_id=brief["row_id"],
    properties={
        "Master_decision": "reject_no_data",
        "Master_note": f"data_anchor_missing: {missing_keys_summary}. Accepted_hypothesis: false.",
        "Trạng thái": "rejected"
    }
)

# Case REJECT_DATA_CONFLICT
update_pages(
    page_id=brief["row_id"],
    properties={
        "Master_decision": "reject_data_conflict",
        "Master_note": f"insight_data_conflict: {conflict_detail}. Accepted_hypothesis: false.",
        "Trạng thái": "rejected"
    }
)
```
