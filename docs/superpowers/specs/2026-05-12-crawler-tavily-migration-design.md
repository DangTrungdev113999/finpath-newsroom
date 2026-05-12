# Crawler Tavily Migration v1.0 — Design Spec

**Date:** 2026-05-12
**Author:** Claude (drafted via brainstorming với user @dangtrungicloud)
**Status:** Approved — proceeding to plan

## 1. Mục tiêu

Replace Step 1 Crawler hiện tại (20-source scraping với latency ~40s/call) bằng `tavily_search` MCP per ticker (latency ~3s/call). Giải quyết 2 vấn đề user feedback:

1. **"Quá tin để sàng lọc lại còn nhiều tin cũ"** — Tavily có `time_range="week"` filter strict thời gian.
2. **Hit rate thấp** với Finpath harvester (0-8% per call) — Tavily test cho thấy 100% per-ticker hit rate (15/15 results về TCB).

Goal architecture cuối:
- **Crawler Step 1**: Tavily MCP làm primary source. Fallback chain Tavily → built-in WebSearch → existing 20-source crawler (3-tier guarantee).
- **Master Step 6 web_search**: KHÔNG đụng. Giữ built-in WebSearch để tiết kiệm credit Tavily free tier.

## 2. Scope

### In scope (deliverable)

- New `lib/tavily_crawler.py` — adapter wrapper Tavily call + parse + persist
- Update `.claude/skills/finpath-newsroom-crawler/SKILL.md` — workflow V3.0 với 3-tier fallback chain
- Reuse existing scripts (`source_whitelist.py`, `search_queries.py`, `dedupe.py`) làm Tier 3 fallback (KHÔNG xóa)

### Out of scope (defer / không động)

- Master Bank/CK/BĐS Step 6 web_search — vẫn dùng built-in WebSearch (per user "tiết kiệm credit")
- Editor V1 / Story Editor / Skeptic / Render right column — input schema giữ nguyên (`crawl_log` rows)
- DB schema `crawl_log` — KHÔNG đụng (Tavily output map vào schema cũ qua adapter)
- Tavily usage tracking / rate limit — defer (per Q2 = A: accept fail risk, fallback handles)
- Existing crawler scripts — KEEP nguyên, chỉ demote thành Tier 3 fallback
- Master Bank V4.0 SKILL.md / agent file — KHÔNG đụng
- Tests automated — chỉ smoke check manual + user E2E
- Notion publish — KHÔNG đụng

## 3. Architecture — 3-tier fallback chain

```
/tin TCB → Crawler skill V3.0
    ↓
[Tier 1: Tavily MCP — primary]
    tavily_search(
      query="TCB Techcombank tin tức",
      time_range="week",        # fix vấn đề "tin cũ"
      include_domains=[20 VN sources whitelist],
      max_results=20,
      country="Vietnam"
    )
    ↓ if Tavily fail (out-of-credit / API error / 0 results)
[Tier 2: Built-in WebSearch — fallback 1]
    WebSearch tool với query similar
    ↓ if WebSearch fail / 0 results
[Tier 3: Existing 20-source crawler — fallback 2 last resort]
    Run lib/scripts/source_whitelist.py + search_queries.py legacy code
    ↓
[Adapter: parse → INSERT crawl_log]
    parse_tavily_results(result_list, ticker, batch_id) → rows
    db.insert_crawl_log(rows)
```

**Pipeline log emit `data_trail` entry với tier_used:**
- Tier 1 success: `data_trail[].source = "Tavily/tavily_search:<query>"`
- Tier 2 fallback: `data_trail[].source = "WebSearch/<query>"`
- Tier 3 fallback: `data_trail[].source = "Crawler-legacy/20-source"`

→ Audit trail rõ tier nào được dùng cho mỗi `/tin TCB` run.

## 4. New file `lib/tavily_crawler.py`

### Public interface

```python
def crawl(ticker: str, batch_id: str) -> tuple[list[dict], str]:
    """Try Tier 1 → 2 → 3, return (rows, tier_used).

    Args:
        ticker: VN stock ticker (must be in 61-mã universe)
        batch_id: format <TICKER>-YYYYMMDD-HHMM

    Returns:
        (rows, tier): list of crawl_log row dicts + tier name string

    Tiers:
        1: "Tavily" — MCP tavily_search call
        2: "WebSearch" — built-in WebSearch tool
        3: "Crawler-legacy" — existing 20-source scrape

    Raises:
        ValueError if ticker not in universe (orchestrator should catch first)
    """
```

### Internal helpers

```python
def crawl_with_tavily(ticker: str, full_name: str, batch_id: str) -> list[dict]:
    """Tier 1: call MCP tavily_search via tool.
       Returns parsed rows or [] on failure."""

def crawl_with_websearch(ticker: str, full_name: str, batch_id: str) -> list[dict]:
    """Tier 2: call built-in WebSearch tool.
       Returns parsed rows or [] on failure."""

def crawl_with_legacy(ticker: str, batch_id: str) -> list[dict]:
    """Tier 3: invoke existing scripts/* legacy code."""

def parse_tavily_result(r: dict, ticker: str, batch_id: str) -> dict:
    """Map Tavily search result → crawl_log row schema.

    Returns dict with keys:
        source_name, source_url, title, body, published_time,
        crawled_at, ticker, funnel_batch_id, sector
    """

def domain_to_source_name(url: str) -> str:
    """Reverse map domain → friendly source name.

    cafef.vn → 'CafeF'
    vietstock.vn → 'Vietstock'
    Fallback: domain itself if not in whitelist.
    """

def get_full_name(ticker: str) -> str:
    """Get full bank/CK name for query enrichment.

    TCB → 'Techcombank'
    VCB → 'Vietcombank'
    SSI → 'SSI Securities'
    Use lib/routing.py BANK_UNIVERSE / CK_UNIVERSE / BDS_UNIVERSE.
    """
```

### Tavily query construction

```python
query = f"{ticker} {full_name} tin tức"
# vd "TCB Techcombank tin tức"

include_domains = list(SOURCES_WHITELIST.values())
# 20 VN sources: cafef.vn, vietstock.vn, tuoitre.vn, ...

tavily_args = {
    "query": query,
    "max_results": 20,
    "search_depth": "advanced",  # better quality vs basic
    "time_range": "week",        # last 7 days
    "country": "Vietnam",
    "include_domains": include_domains,
}
```

### Result filtering (post-fetch)

After Tavily returns N results, filter:
- Skip URLs ending `.pdf` (PDF reports không parse text được)
- Skip ticker's own corporate site (vd TCB → skip techcombank.com, VCB → skip vietcombank.com.vn) — own corporate sites không phải tin báo
- Dedup by URL (case `dnse.com.vn/...` vs `dnse.com.vn/...?utm=` — strip query string trước dedup)
- Sort by `score` desc nếu có

## 5. SKILL.md update — `finpath-newsroom-crawler/SKILL.md`

### Replace workflow section với V3.0

```markdown
## Workflow V3.0 (Tavily migration)

### 1. Validate ticker + build query

- Validate ticker in 61-mã universe (BANK_UNIVERSE / CK_UNIVERSE / BDS_UNIVERSE từ lib/routing.py)
- full_name = lookup từ universe constants
- query = f"{ticker} {full_name} tin tức"
- batch_id = f"{ticker}-{YYYYMMDD-HHMM}"

### 2. Tier 1 — Tavily MCP tavily_search

```python
from lib.tavily_crawler import crawl
rows, tier = crawl(ticker, batch_id)
```

Internal call:
- Tool: `mcp__tavily__tavily_search`
- Args: query / time_range="week" / max_results=20 / country="Vietnam" / include_domains=[20 VN sources]
- Filter: skip PDF, skip corporate sites của ticker, dedup URL
- Parse → rows

### 3. Tier 2 fallback — Built-in WebSearch

Auto-trigger nếu Tavily:
- Out of credit (free tier 1.000/month cạn)
- API error (network / rate limit)
- 0 results sau filter

```python
from lib.tavily_crawler import crawl_with_websearch
rows = crawl_with_websearch(ticker, full_name, batch_id)
```

### 4. Tier 3 fallback — Legacy 20-source crawler

Auto-trigger nếu cả Tier 1 + Tier 2 fail:
```python
from lib.tavily_crawler import crawl_with_legacy
rows = crawl_with_legacy(ticker, batch_id)
```

Internal: invoke `.claude/skills/finpath-newsroom-crawler/scripts/source_whitelist.py` + `search_queries.py` (legacy implementation).

### 5. Persist + emit data_trail

```python
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.insert_crawl_log(rows)

# Pipeline log
data_trail.append({
    "source": f"{tier}/{tool_name}",  # vd "Tavily/tavily_search"
    "fetched": f"{len(rows)} candidates",
    "purpose": "Step 1 crawler input",
    "supports_argument": "Editor V1 + Story Editor downstream"
})
```
```

### Update description metadata

Old description (V2.4):
> "Crawls 20 Vietnamese financial/general news sources for latest 3 articles per source..."

New description (V3.0):
> "V3.0 Tavily-primary crawler. Calls MCP tavily_search per ticker with time_range=week + 20-source domain whitelist. Falls back to built-in WebSearch tool if Tavily fails. Last-resort fallback to legacy 20-source scrape."

## 6. Implementation order (atomic commits)

1. **Commit 1** — Spec + plan
2. **Commit 2** — Add `lib/tavily_crawler.py` Tier 1 only (Tavily call + parse + filter + persist)
3. **Commit 3** — Add Tier 2 fallback (WebSearch built-in wrapper)
4. **Commit 4** — Add Tier 3 fallback (wrap legacy crawler scripts)
5. **Commit 5** — Update `finpath-newsroom-crawler/SKILL.md` workflow V3.0 + description
6. **Commit 6** — Smoke test results commit (manual run + verify rows in DB)

Each commit atomic, easy revert per tier.

## 7. Risks + mitigation

- **Risk 1: API key expose** — `tvly-dev-...` key NEVER commit vào code. Code dùng MCP tool name `mcp__tavily__tavily_search` (key resolution happens client-side in `~/.claude.json`).
- **Risk 2: Free tier 1.000/month cạn** — Fallback Tier 2/3 handle automatic. Per user Q2 = A: accept risk, không track usage.
- **Risk 3: Tavily response schema thay đổi** — Adapter dùng `.get()` defensive parsing. Log warning nếu unexpected field.
- **Risk 4: published_date often N/A** — Fallback `crawled_at` (current timestamp). Note trong row để Editor V1 / Story Editor biết time data unreliable.
- **Risk 5: Existing crawler break sau demote** — Smoke test Tier 3 trigger để verify legacy code vẫn chạy.

## 8. Validation (smoke only — STOP before user E2E)

### Tavily Tier 1 standalone test
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.tavily_crawler import crawl
rows, tier = crawl('TCB', 'TCB-20260512-SMOKE')
print(f'Tier used: {tier}')
print(f'Rows: {len(rows)}')
for r in rows[:3]:
    print(f\"  {r['source_name']} | {r['title'][:60]} | {r['source_url'][:80]}\")
"
```

Expected: `tier="Tavily"`, `rows ≥10`, all about TCB.

### Tier 2 fallback test (simulate Tavily fail)
- Manually break Tavily MCP URL temporarily
- Re-run smoke → verify `tier="WebSearch"` + rows ≥3
- Restore URL

### Tier 3 fallback test (simulate Tavily + WebSearch fail)
- Mock both fail conditions
- Verify `tier="Crawler-legacy"` + rows from existing scripts

### Adapter parse correctness
- Verify rows insert vào `crawl_log` table không break schema:
  - `source_name` not null
  - `source_url` not null + canonical format
  - `published_time` ISO format hoặc fallback `crawled_at`
  - `funnel_batch_id` correct format `TCB-YYYYMMDD-HHMM`
  - `ticker` = "TCB"
  - `sector` = "Bank" (lookup từ routing.py)

### SKILL.md workflow update verification
```bash
grep -c "Tier 1" .claude/skills/finpath-newsroom-crawler/SKILL.md
grep -c "tavily_search" .claude/skills/finpath-newsroom-crawler/SKILL.md
grep -c "lib.tavily_crawler" .claude/skills/finpath-newsroom-crawler/SKILL.md
# All expected ≥1
```

## 9. Hand-off cho user

Sau Commit 6 smoke checks pass, **HAND OFF** user:

> "Crawler Tavily migration v1.0 done. Smoke checks pass:
> - Tier 1 (Tavily) returns ≥10 rows về TCB
> - Tier 2 fallback works
> - Tier 3 fallback works
> - Adapter map vào crawl_log schema OK
>
> **Bạn run `/tin TCB` end-to-end** test:
> - Pipeline log emit `data_trail` với tier="Tavily"
> - Article output vẫn pass 5 quality gates V4.0
> - Right column 'Crawl funnel' render OK
> - Right column 'Bài gốc' có source_url canonical
>
> Nếu pass → ship. Nếu issue → fix forward hoặc revert spec để go back legacy."

## 10. Open questions / followup

- **Per-sector query optimization** — sau khi Bank/CK works, có thể tune query template per sector (vd CK: "[TICKER] [Securities] tin tức ngân hàng đầu tư") để boost relevance.
- **Multi-query parallel** — nếu Tier 1 trả ít kết quả với 1 query, có thể fan out 2-3 queries variations + merge dedup. Defer until measured.
- **Tavily usage dashboard** — Phase sau add tracking nếu thấy cạn credit thường xuyên.
- **Per-ticker query enrichment** — TCB query có thể thêm "Hồ Hùng Anh" / "ngân hàng tư nhân" boost. Defer measurement first.

## Changelog

- **v1.1 (2026-05-12) — ARCHITECTURE FIX**: Advisor review phát hiện v1.0 design có architectural mismatch — MCP tools là **agent-context tools** (KHÔNG Python-callable từ module). v1.0 placeholder `_call_tavily_mcp` raises NotImplementedError → production sẽ return empty pipeline.

  **Fix v1.1**: restructure theo pattern existing crawler (`lib/stages/run_crawler.py` line 3-4: "script writes candidates already fetched by Claude. Does NOT make HTTP calls itself"). Agent fetches via MCP/WebSearch tool → Bash invoke Python script to parse + persist.

  Changes:
  - REMOVE 3 placeholder + 3 wrapper functions (`_call_tavily_mcp`, `_call_websearch`, `_call_legacy_crawler`, `crawl_with_tavily`, `crawl_with_websearch`, `crawl_with_legacy`, `crawl()`).
  - REMOVE 10 tests using monkeypatch on those placeholders.
  - ADD `parse_tavily_response(response, ticker, batch_id) -> list[rows]` (pure function, input MCP response dict).
  - ADD `persist_rows(rows, db) -> count` (INSERT batch into crawl_log).
  - ADD CLI entry `__main__` reading JSON từ stdin → persist (allows `agent fetches | python -m lib.tavily_crawler ...` pipe).
  - REWRITE SKILL.md workflow: explicit MCP tool call by agent (Tier 1) → fallback WebSearch (Tier 2) → fallback existing legacy crawler script (Tier 3) → all 3 tiers feed parsed JSON to `parse_and_persist` script.

- **v1.0 (2026-05-12):** Initial spec, drafted via brainstorming với user. Architecture: Tavily MCP primary + WebSearch + legacy crawler fallback chain. Scope: Step 1 crawler only, Master Step 6 unchanged. Per user Q1=A (3-tier), Q2=A (no tracking), Q3=A (hard switch). **Architectural flaw fixed in v1.1.**
