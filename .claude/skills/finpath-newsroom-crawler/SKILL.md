---
name: finpath-newsroom-crawler
description: Crawls 20 Vietnamese financial/general news sources for latest 3 articles per source (sort by publish time desc) about a stock ticker in Bank/CK/BĐS universe — sub-skill in Finpath Newsroom V2.4 pipeline. Use when orchestrator triggers Step 1, or user explicit "crawl tin về [TICKER]". Writes rows to DB Crawl Log with Published_time + Funnel_batch_id (format ticker-YYYYMMDD-HHMM) for downstream Editor V1 + Story Editor + Compare Feed Crawl Funnel section. NEVER use for non-universe tickers. NEVER pull more than 3 articles per source — must be 3 newest only.
---

# Finpath Newsroom Crawler

Crawler agent V2.4 — input đầu pipeline Newsroom. Search + fetch tin từ **20 nguồn báo chí Việt Nam**, lấy **3 bài mới nhất per nguồn** (sort by publish time desc), write vào DB Crawl Log với Published_time + Funnel_batch_id để Editor + Story Editor process tiếp.

## Khi nào trigger

- Orchestrator gọi với input ticker
- User gõ explicit "crawl tin về [TICKER]" (test riêng skill này)

## Input

```json
{
  "ticker": "VCB"
}
```

## Output

```json
{
  "ticker": "VCB",
  "sector": "Bank",
  "rows_created": [
    {
      "row_id": "<notion_page_id>",
      "tieu_de": "...",
      "nguon": "CafeF",
      "link_goc": "https://..."
    }
  ],
  "rows_skipped_dedupe": 5,
  "errors": []
}
```

## Workflow 7 bước

### Bước 1 — Validate ticker

```python
from scripts.source_whitelist import get_sector_for_ticker, BANK_UNIVERSE

ticker = input["ticker"].upper()

if ticker not in BANK_UNIVERSE:  # M1 Bank only
    return {"error": f"M1 chỉ Bank: {BANK_UNIVERSE}", "ticker": ticker}

sector = "Bank"
```

### Bước 2 — Build search queries

```python
from scripts.search_queries import build_queries

queries = build_queries(ticker, sector)
# Example for VCB:
# ["VCB Vietcombank", "VCB kết quả kinh doanh", 
#  "VCB cổ phiếu tin tức", "VCB ngân hàng"]
```

### Bước 3 — Search per source (V2.4: 20 nguồn, sort by publish time desc, top 3)

For mỗi nguồn trong whitelist (20 nguồn):
```python
from scripts.source_whitelist import SOURCES_WHITELIST
import datetime as dt

# Generate Funnel_batch_id ONCE per ticker call (link tất cả tin trong batch)
funnel_batch_id = f"{ticker}-{dt.datetime.now().strftime('%Y%m%d-%H%M')}"
# vd: "TCB-20260507-1430"

candidates = []
for source_name, domain in SOURCES_WHITELIST.items():
    for query in queries:
        # Use web_search tool
        full_query = f"{query} site:{domain}"
        results = web_search(full_query)
        
        # V2.4: Sort by publish time DESC + take top 3 NEWEST
        # web_search results đã có metadata.published_time hoặc parse từ snippet
        sorted_results = sorted(
            [r for r in results if has_recent_date(r, days=30)],
            key=lambda r: r.get("published_time", "1970-01-01"),
            reverse=True  # newest first
        )
        top_3_newest = sorted_results[:3]
        
        for r in top_3_newest:
            candidates.append({
                "source_name": source_name,
                "url": r["url"],
                "title_preview": r["title"],
                "published_time": r.get("published_time"),  # ISO datetime, may be None
                "funnel_batch_id": funnel_batch_id
            })
```

⚠️ **V2.4 CRITICAL**: Sort by `published_time` desc, take top 3 mới nhất per nguồn. KHÔNG lấy tin cũ. User check 3 bài newest qua field `Published_time` trên DB Crawl Log row.

⚠️ **published_time fallback**: nếu web_search không return published_time field, parse từ:
1. URL pattern (vd `cafef.vn/2026/05/07/article-slug` → 2026-05-07)
2. Article snippet "Đăng ngày DD/MM/YYYY"
3. Nếu không parse được → set Published_time = NULL, ghi chú trong `Ghi chú pipeline`

### Bước 4 — Dedupe candidates

```python
from scripts.dedupe import filter_existing_urls

# Query DB Crawl Log filter by Link gốc
existing_urls = query_data_source(
    data_source_id="8aad4abe-496f-480f-ad13-8996d22fe447",
    filter={"Link gốc": [c["url"] for c in candidates]}
)

candidates_new = [c for c in candidates if c["url"] not in existing_urls]
rows_skipped_dedupe = len(candidates) - len(candidates_new)
```

### Bước 5 — Fetch full content

For mỗi candidate mới:
```python
errors = []
for c in candidates_new:
    try:
        # Use web_fetch tool
        content = web_fetch(c["url"])
        c["full_content"] = content["text"]
        c["full_title"] = content["title"]
    except Exception as e:
        errors.append({"url": c["url"], "error": str(e)})
```

### Bước 6 — Write rows vào DB (V2.4: thêm Published_time + Funnel_batch_id)

```python
rows_created = []
for c in candidates_new:
    if "full_content" not in c:
        continue  # fetch failed, skip
    
    properties = {
        "Tiêu đề": c["full_title"],
        "Nguồn": c["source_name"],
        "Link gốc": c["url"],
        "Nội dung thô": c["full_content"][:2000],  # cap 2000 chars
        "Trạng thái": "pending",
        "Route tới": "pending",
        "Pipeline_version": "V2",
        "Funnel_batch_id": c["funnel_batch_id"],  # V2.4 thêm
        "date:Crawl lúc:start": now_iso(),
        "date:Crawl lúc:is_datetime": 1,
    }
    
    # V2.4: log Published_time nếu có
    if c.get("published_time"):
        properties["date:Published_time:start"] = c["published_time"]
        properties["date:Published_time:is_datetime"] = 1
    
    # Use Notion MCP create_pages
    row = create_pages(
        parent={"data_source_id": "8aad4abe-496f-480f-ad13-8996d22fe447"},
        pages=[{"properties": properties}]
    )
    
    rows_created.append({
        "row_id": row["id"],
        "tieu_de": c["full_title"],
        "nguon": c["source_name"],
        "link_goc": c["url"],
        "published_time": c.get("published_time"),
        "funnel_batch_id": c["funnel_batch_id"]
    })
```

⚠️ **V2.4 fields mới được set**:
- `Published_time` — thời gian publish bài gốc (date, có thể NULL nếu không parse được)
- `Funnel_batch_id` — link tất cả tin trong batch để Compare Feed render Crawl Funnel section

### 🚨 NEVER skip candidates — TẤT CẢ phải log vào DB Crawl Log

Crawler là source of truth cho Compare Feed Crawl Funnel section. Section này render TẤT CẢ candidates trong batch (1 picked + N rejected) với agent reject + reason. Nếu Crawler chỉ log 3/10 candidates, Compare Feed sẽ thiếu data và user thấy funnel "rỗng".

**ALWAYS log mọi candidate fetch được, kể cả**:
- Candidate bị Editor V1 reject sau (out_of_universe / low_quality_source / dup_url)
- Candidate bị Story Editor reject sau (dup_event / low_writeability / wait_more_data)
- Candidate fetch fail nội dung (vẫn log row với `Nội dung thô = "[fetch failed]"` + log error)
- Candidate trùng story angle với candidate khác trong cùng batch

**Mục tiêu**: Sau khi Crawler chạy xong, DB Crawl Log phải có **đủ N row** với cùng `Funnel_batch_id`, để Editor V1 + Story Editor + Compare Feed render đầy đủ funnel.

**Anti-pattern (KHÔNG làm)**:
- Crawler chỉ search 1-2 query rồi return 3 candidates "tiêu biểu" — sai. Phải search per nguồn từ whitelist.
- Crawler tự reject candidate nếu thấy "trùng story" — sai. Đó là việc của Story Editor, không phải Crawler.
- Crawler skip nguồn khi web_search broad query đã có 3 kết quả từ nguồn khác — sai. Mỗi nguồn phải search riêng để có 3 newest từ nguồn đó.

**Pattern đúng — broad search fallback**:
Nếu loop `for source in WHITELIST` quá tốn token (20 search calls), pattern thay thế OK:
1. Search broad query: `"[TICKER] [tên cty]"` (1-2 search call)
2. Map kết quả về whitelist domain (parse URL)
3. Lấy top 3 newest per domain (group by source domain, sort desc)
4. **CRITICAL**: log explicit `"broadcast_search_used: true"` vào field `Ghi chú pipeline` của mỗi row, để downstream biết đây là broadcast search (có thể miss tin từ nguồn ít rank cao)

### Bước 7 — Return output

```json
{
  "ticker": "VCB",
  "sector": "Bank",
  "rows_created": [...],
  "rows_skipped_dedupe": 5,
  "errors": []
}
```

## Constraints

- **Max candidates V2.4**: 20 nguồn × 3 tin (mới nhất) = 60 candidates max per call
- **Recent filter**: tin trong vòng 30 ngày
- **Content cap**: 2000 chars per row (tránh DB bloat)
- **Error tolerance**: search/fetch fail 1 nguồn → skip nguồn đó, không fail toàn bộ
- **Rate limit**: 1 trigger / 30s / user (orchestrator enforce)

## Tools used

- `web_search` (built-in) — search engine top 10 results
- `web_fetch` (built-in) — fetch full content from URL → text
- Notion MCP `query_data_sources` — dedupe check
- Notion MCP `create_pages` (parent: data_source_id DB Crawl Log) — write rows mới

## Error handling

| Lỗi | Hành động |
|-----|-----------|
| Search fail nguồn X | Skip nguồn đó, log error, vẫn process nguồn khác |
| Fetch fail URL Y | Skip URL đó, log error, không fail toàn bộ |
| Tổng candidates = 0 | Return empty rows_created + note "Không tìm thấy tin trong 30 ngày" |
| Notion API fail | Retry max 3 lần, sau đó skip row đó, log error |

## Helper scripts

- `scripts/source_whitelist.py` — 8 sources mapping + universe constants
- `scripts/search_queries.py` — query builder per ticker + sector
- `scripts/dedupe.py` — check Link gốc đã tồn tại

## Reference

- Module Notion: 1.0 Crawler — https://www.notion.so/357273c7a9a1812fbd07de47b9b90749
- DB Newsroom Crawl Log schema: https://www.notion.so/357273c7a9a181359021c964151bf571

## Notes

- **Tiếng Việt thuần**: title trong Tiêu đề giữ nguyên từ source. Comments/logs có thể English. User-facing reply tiếng Việt.
- **Date filter implementation**: web_search có thể trả date trong snippet. Nếu không có date → fetch full content và parse meta tag. Nếu không parse được → giả sử recent OK (better false positive than miss).
