---
name: finpath-newsroom-crawler
description: V3.1 Tavily-primary crawler (agent-fetch + script-persist). Agent invokes mcp__tavily__tavily_search directly (time_range=week + 20-source domain whitelist + max_results=20 + country=Vietnam), captures raw JSON, pipes to lib.tavily_crawler script for parse + persist. Auto-fallback to built-in WebSearch tool if Tavily fails, then to legacy 20-source crawler as last resort. Writes rows to SQLite crawl_log. Pipeline log emits data_trail entry with tier_used (Tavily / WebSearch / Crawler-legacy). NEVER use for non-universe tickers.
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

## Workflow V3.1 (agent-fetch + script-persist)

### 1. Validate ticker + build batch_id + Tavily args

```python
from lib.tavily_crawler import build_tavily_args
from lib.stages.run_crawler import FULL_UNIVERSE
ticker = "TCB"  # from input
if ticker not in FULL_UNIVERSE:
    raise ValueError(f"{ticker} not in 61-mã universe")
batch_id = f"{ticker}-{datetime.now().strftime('%Y%m%d-%H%M')}"
tavily_args = build_tavily_args(ticker)
# tavily_args = {"query": "TCB Techcombank tin tức", "time_range": "week", ...}
```

### 2. Tier 1 — Agent invoke `mcp__tavily__tavily_search` tool

Agent calls MCP tool directly với `tavily_args`. Capture raw response JSON.

If results ≥1 → skip to Step 5 with `tier_used="Tavily"`.

If response empty / API error / out-of-credit → fallback Step 3.

### 3. Tier 2 fallback — Agent invoke built-in `WebSearch` tool

Agent calls `WebSearch` tool với query: `f"{ticker} {full_name} tin tức 2026"`.
Capture results array. Wrap thành `{"results": [...]}` để pass tới script.

If results ≥1 → skip to Step 5 with `tier_used="WebSearch"`.

If empty → fallback Step 4.

### 4. Tier 3 fallback — Existing legacy crawler

Agent invokes existing `lib/stages/run_crawler.py` legacy logic (already
follows agent-fetch pattern).

If empty → all 3 tiers failed, log + return.

### 5. Pipe results to parse+persist script

```bash
echo "$TAVILY_RESPONSE_JSON" | uv run python -m lib.tavily_crawler $ticker $batch_id
```

Script reads JSON từ stdin, parses + filters + INSERTs vào `crawl_log`,
prints count.

### 6. Emit data_trail to pipeline log

```python
data_trail.append({
    "source": f"{tier_used}/{'tavily_search' if tier_used == 'Tavily' else tier_used.lower()}",
    "fetched": f"{count} candidates",
    "purpose": "Step 1 crawler input",
    "supports_argument": "Editor V1 + Story Editor downstream"
})
```

### Notes

- Pattern: agent fetches via MCP/WebSearch tool, Python script persists. Match existing `lib/stages/run_crawler.py` pattern (line 3-4 "script does NOT make HTTP calls itself").
- Free tier Tavily limit 1.000 searches/month. Per Q2=A spec: no usage tracking, fail gracefully via fallback chain.
- Master Bank/CK/BĐS Step 6 web_search KHÔNG dùng Tavily (per user "tiết kiệm credit").
- All 3 tiers feed parsed JSON to same script for consistent persistence.

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
