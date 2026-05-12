---
name: finpath-newsroom-crawler
description: V3.0 Tavily-primary crawler. Calls MCP tavily_search per ticker (time_range=week + 20-source domain whitelist + max_results=20 + country=Vietnam) to fetch latest news for stock ticker in 61-mã universe (Bank/CK/BĐS). Auto-fallbacks to built-in WebSearch tool if Tavily fails (out-of-credit / API error / empty), then to legacy 20-source crawler as last resort. Writes rows to SQLite crawl_log via lib/tavily_crawler.crawl(). Pipeline log emits data_trail entry with tier_used (Tavily / WebSearch / Crawler-legacy). NEVER use for non-universe tickers.
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
      "row_id": "<uuid>",
      "tieu_de": "...",
      "nguon": "CafeF",
      "link_goc": "https://..."
    }
  ],
  "rows_skipped_dedupe": 5,
  "errors": []
}
```

## Workflow V3.0 (Tavily migration)

### 1. Validate ticker + build batch_id

```python
from lib.stages.run_crawler import FULL_UNIVERSE  # 61 mã
ticker = "TCB"  # from input
if ticker not in FULL_UNIVERSE:
    raise ValueError(f"{ticker} not in 61-mã universe")
batch_id = f"{ticker}-{datetime.now().strftime('%Y%m%d-%H%M')}"
```

### 2. Call lib/tavily_crawler.crawl() (3-tier orchestrator)

The orchestrator transparently tries:
- **Tier 1: Tavily MCP** — `mcp__tavily__tavily_search` với time_range=week, 20 source whitelist, max_results=20, country=Vietnam
- **Tier 2: Built-in WebSearch** — if Tier 1 returns []
- **Tier 3: Legacy 20-source crawler** — if Tier 2 returns []

```python
from lib.tavily_crawler import crawl
rows, tier_used = crawl(ticker, batch_id)
print(f"Crawled {len(rows)} candidates via {tier_used}")
```

### 3. Persist rows vào SQLite crawl_log

```python
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
for row in rows:
    db.insert_crawl_row(row)
db.conn.close()
```

### 4. Emit data_trail entry to pipeline log

```python
data_trail.append({
    "source": f"{tier_used}/{'tavily_search' if tier_used == 'Tavily' else tier_used.lower()}",
    "fetched": f"{len(rows)} candidates",
    "purpose": "Step 1 crawler input",
    "supports_argument": "Editor V1 + Story Editor downstream"
})
```

### Tier-specific MCP/tool invocation

Crawler skill (or agent calling this skill) **MUST have access** to:
- `mcp__tavily__tavily_search` (for Tier 1 — required for primary path)
- Built-in `WebSearch` tool (for Tier 2 fallback)

If running headless (no MCP), Tier 1 + 2 will fail → automatic Tier 3 (legacy crawler) takes over.

### Notes

- Crawler V3.0 đầu pipeline. Output = rows in crawl_log table với primary_ticker NULL → Editor V1 fills primary_ticker downstream.
- Pipeline log audit trail: `data_trail.source` field shows which tier was used for transparency.
- Free tier Tavily limit 1.000 searches/month. Per Q2=A spec: no usage tracking, fail gracefully via fallback.
- Master Bank/CK/BĐS Step 6 web_search KHÔNG dùng Tavily (per user "tiết kiệm credit").

## Constraints

- **Max candidates V2.4**: 20 nguồn × 3 tin (mới nhất) = 60 candidates max per call
- **Recent filter**: tin trong vòng 30 ngày
- **Content cap**: 2000 chars per row (tránh DB bloat)
- **Error tolerance**: search/fetch fail 1 nguồn → skip nguồn đó, không fail toàn bộ
- **Rate limit**: 1 trigger / 30s / user (orchestrator enforce)

## Tools used

- `web_search` (built-in) — search engine top 10 results
- `web_fetch` (built-in) — fetch full content from URL → text
- `lib/pipeline_db.py` `PipelineDB` — dedupe check + write rows mới vào `crawl_log` table (`data/pipeline.db`)

## Error handling

| Lỗi | Hành động |
|-----|-----------|
| Search fail nguồn X | Skip nguồn đó, log error, vẫn process nguồn khác |
| Fetch fail URL Y | Skip URL đó, log error, không fail toàn bộ |
| Tổng candidates = 0 | Return empty rows_created + note "Không tìm thấy tin trong 30 ngày" |
| SQLite write fail | Retry max 3 lần, sau đó skip row đó, log error |

## Helper scripts

- `scripts/source_whitelist.py` — 8 sources mapping + universe constants
- `scripts/search_queries.py` — query builder per ticker + sector
- `scripts/dedupe.py` — check Link gốc đã tồn tại

## Reference

- `lib/pipeline_db.py` — PipelineDB helper (insert/update/query `crawl_log` and `generated_news`)
- `data/pipeline.db` — SQLite database (crawl_log schema in `data/schema.sql`)

## Notes

- **Tiếng Việt thuần**: title trong Tiêu đề giữ nguyên từ source. Comments/logs có thể English. User-facing reply tiếng Việt.
- **Date filter implementation**: web_search có thể trả date trong snippet. Nếu không có date → fetch full content và parse meta tag. Nếu không parse được → giả sử recent OK (better false positive than miss).
