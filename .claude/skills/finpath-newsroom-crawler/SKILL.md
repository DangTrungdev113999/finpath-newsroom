---
name: finpath-newsroom-crawler
description: V3.2 Tavily-primary crawler (agent-fetch + script-persist). Agent invokes mcp__tavily__tavily_search với query enriched theo sector (vd "Tin mới nhất về HPG Hòa Phát ngành Thép"), max_results=50, time_range=week, 20-source whitelist, include_raw_content=True. Script post-fetch filter: PDF skip + corporate site skip + URL dedup + title relevance (ticker OR full_name diacritic-folded) + 3-day window (optimistic on missing date). Sector_name resolve qua lib/finpath_sectors.FinpathSectors cache. Auto-fallback WebSearch built-in → legacy crawler. Pipeline log emits data_trail entry với tier_used (Tavily / WebSearch / Crawler-legacy).
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

## Workflow V3.2 (agent-fetch + script-persist)

### 1. Build batch_id + Tavily args (sector-enriched)

```python
from lib.tavily_crawler import build_tavily_args
ticker = "HPG"  # from input
batch_id = f"{ticker}-{datetime.now().strftime('%Y%m%d-%H%M')}"
tavily_args = build_tavily_args(ticker)
# V3.2 sample for HPG:
#   query = "Tin mới nhất về HPG Hòa Phát ngành Thép"
#   max_results = 50
#   time_range = "week"
#   include_domains = [20 VN news sources]
#   include_raw_content = True
# sector_name auto-resolved via lib/finpath_sectors.FinpathSectors cache;
# unknown sector → query degrades to "Tin mới nhất về <TICKER> <full_name>" (still functional).
```

Universe validation deferred to Editor V1 (V5.1.3 — Finpath ~139 cache). Crawler accepts ALL tickers; Editor V1 rejects outside Finpath với `editor_v1_note="ticker_outside_finpath_139"`.

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

### V3.2 post-fetch filter (all 3 tiers)

`lib.tavily_crawler.filter_results()` applies 5 rules in order. PDF/corporate/dedup là V3.1 baseline; title relevance + date window là V3.2 add-on:

1. **PDF skip** — URL path endswith `.pdf` → reject.
2. **Corporate site skip** — domain match `_CORPORATE_DOMAINS[ticker]` → reject (vd HPG bài trên `hoaphat.com.vn` skipped).
3. **URL dedup** — canonical URL (strip `?query`) seen → reject.
4. **Title relevance (V3.2)** — title phải mention `ticker` OR `full_name` sau diacritic-fold (Hòa Phát/Hoa Phat đều match). Bài chỉ mention sector ("Ngành thép quý 1") → reject. Ticker lookup table `_TICKER_FULL_NAMES` covers ~90 mã (Bank/CK/BĐS + V5.1.3 expansion non-financial large-cap).
5. **Date window 3 ngày (V3.2)** — parse `result["published_date"]` ISO/YYYY-MM-DD. Older than `now() - 3 days` → reject. **Missing date → optimistic keep** (per design — Tavily đã pre-filter `time_range="week"` ở API level, trust khi missing).

Constants: `DATE_WINDOW_DAYS = 3` ở `lib/tavily_crawler.py`. Override qua `filter_results(date_window_days=N, now=...)` cho tests.

Backward compat: gọi `filter_results(results, ticker)` không pass `full_name` → title relevance không enforce (chỉ PDF + corporate + dedup + date).

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
