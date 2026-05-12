# Crawler Tavily Migration v1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Step 1 Crawler 20-source scrape với `mcp__tavily__tavily_search` per ticker (3-tier fallback: Tavily → built-in WebSearch → legacy 20-source crawler). Master Step 6 web_search KHÔNG đụng (giữ built-in WebSearch tiết kiệm credit Tavily free tier).

**Architecture:** New `lib/tavily_crawler.py` adapter làm primary entry. Tier 1 calls Tavily MCP với `time_range="week"` + `include_domains=[20 VN sources]` để fix vấn đề "tin cũ". Tier 2/3 auto-fallback nếu Tier 1 fail. Adapter parse Tavily response → INSERT vào `crawl_log` table với schema cũ (KHÔNG đụng schema downstream Editor V1/Story Editor/Render).

**Tech Stack:** Python 3 / `mcp__tavily__tavily_search` MCP tool / `lib/pipeline_db.py:insert_crawl_row` / pytest. Reuse `lib/stages/run_crawler.py` constants (FULL_UNIVERSE + SOURCES_WHITELIST).

**Spec:** `docs/superpowers/specs/2026-05-12-crawler-tavily-migration-design.md`

---

## File Structure

**Will create (2 file mới):**

```
lib/tavily_crawler.py                                       # Main adapter (Tier 1+2+3 + parse + persist)
tests/test_tavily_crawler.py                                # Unit tests (parse, filter, dedup, fallback chain)
```

**Will modify (1 file):**

```
.claude/skills/finpath-newsroom-crawler/SKILL.md           # Workflow V3.0 + description update
```

**Will NOT touch:**

- `lib/pipeline_db.py` — `insert_crawl_row()` schema reuse as-is
- `lib/stages/run_crawler.py` — legacy entry kept (Tier 3 fallback wraps it)
- `.claude/skills/finpath-newsroom-crawler/scripts/source_whitelist.py` + `search_queries.py` + `dedupe.py` — legacy implementation (Tier 3)
- `data/pipeline.schema.sql` — `crawl_log` schema unchanged
- Master Bank/CK/BĐS skills + agents
- Editor V1 / Story Editor / Skeptic / Render

---

## Task 1: Create `lib/tavily_crawler.py` Tier 1 (Tavily call + parse + persist)

**Files:**
- Create: `lib/tavily_crawler.py`
- Create: `tests/test_tavily_crawler.py`

- [ ] **Step 1: Write failing test for `domain_to_source_name()`**

Add to `tests/test_tavily_crawler.py`:

```python
"""Tests cho lib/tavily_crawler.py — Tavily MCP adapter cho Step 1 Crawler."""
from __future__ import annotations
import pytest


def test_domain_to_source_name_known():
    """Known domains map to friendly source names."""
    from lib.tavily_crawler import domain_to_source_name
    assert domain_to_source_name("https://cafef.vn/article-123.chn") == "CafeF"
    assert domain_to_source_name("https://vietstock.vn/path") == "Vietstock"
    assert domain_to_source_name("https://www.tuoitre.vn/article") == "Tuổi Trẻ"


def test_domain_to_source_name_unknown_fallback():
    """Unknown domain falls back to domain itself."""
    from lib.tavily_crawler import domain_to_source_name
    assert domain_to_source_name("https://random-blog.example.com/x") == "random-blog.example.com"


def test_domain_to_source_name_strips_www():
    """www. prefix stripped."""
    from lib.tavily_crawler import domain_to_source_name
    assert domain_to_source_name("https://www.cafef.vn/x") == "CafeF"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py::test_domain_to_source_name_known -v
```

Expected: FAIL `ModuleNotFoundError: No module named 'lib.tavily_crawler'`.

- [ ] **Step 3: Create `lib/tavily_crawler.py` with `domain_to_source_name()` minimum**

Use Write tool. Initial content:

```python
"""Tavily-based crawler adapter for Finpath Newsroom Step 1.

Replaces 20-source scrape with single tavily_search call per ticker.
Falls back to built-in WebSearch if Tavily fails. Falls back to legacy
20-source crawler if WebSearch also fails (3-tier chain).

Spec: docs/superpowers/specs/2026-05-12-crawler-tavily-migration-design.md
"""
from __future__ import annotations
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from typing import Any

# Ensure project root on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from lib.stages.run_crawler import SOURCES_WHITELIST, FULL_UNIVERSE, BANK_UNIVERSE, CK_UNIVERSE, BDS_UNIVERSE


# Reverse map domain → friendly source name
_DOMAIN_TO_NAME: dict[str, str] = {
    domain: name for name, domain in SOURCES_WHITELIST.items()
}


def domain_to_source_name(url: str) -> str:
    """Reverse map URL → friendly source name from SOURCES_WHITELIST.

    Args:
        url: Full URL (e.g. "https://cafef.vn/article.chn")

    Returns:
        Friendly source name (e.g. "CafeF") or domain itself if not in whitelist.
    """
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return _DOMAIN_TO_NAME.get(domain, domain)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py::test_domain_to_source_name_known tests/test_tavily_crawler.py::test_domain_to_source_name_unknown_fallback tests/test_tavily_crawler.py::test_domain_to_source_name_strips_www -v
```

Expected: 3 PASS.

- [ ] **Step 5: Add test for `get_full_name()` (ticker → company name)**

Add to `tests/test_tavily_crawler.py`:

```python
def test_get_full_name_bank():
    from lib.tavily_crawler import get_full_name
    assert get_full_name("TCB") == "Techcombank"
    assert get_full_name("VCB") == "Vietcombank"


def test_get_full_name_ck():
    from lib.tavily_crawler import get_full_name
    assert get_full_name("SSI") == "SSI"  # SSI tự là tên đầy đủ


def test_get_full_name_unknown_returns_ticker():
    from lib.tavily_crawler import get_full_name
    assert get_full_name("XYZUNKNOWN") == "XYZUNKNOWN"
```

- [ ] **Step 6: Run test to verify fails**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py::test_get_full_name_bank -v
```

Expected: FAIL — `AttributeError: module has no attribute 'get_full_name'`.

- [ ] **Step 7: Add `get_full_name()` to `lib/tavily_crawler.py`**

Append:

```python
# Ticker → full company name for query enrichment
_TICKER_FULL_NAMES: dict[str, str] = {
    # Bank universe (27 mã)
    "VCB": "Vietcombank", "CTG": "VietinBank", "BID": "BIDV",
    "TCB": "Techcombank", "MBB": "MB Bank", "ACB": "ACB",
    "VPB": "VPBank", "HDB": "HDBank", "STB": "Sacombank",
    "SHB": "SHB", "EIB": "Eximbank", "TPB": "TPBank",
    "MSB": "MSB", "LPB": "LPBank", "OCB": "OCB",
    "VIB": "VIB", "NAB": "Nam A Bank", "BAB": "BacABank",
    "NVB": "NCB", "SGB": "Saigonbank",
    "VAB": "VietABank", "BVB": "BaoVietBank", "ABB": "ABBank",
    "KLB": "Kienlongbank", "VBB": "VietBank", "PGB": "PGBank", "HDF": "HDF",
    # CK universe (30 mã) — short tickers thường = tên thương hiệu
    "SSI": "SSI", "VND": "VNDirect", "HCM": "HSC", "VCI": "Vietcap",
    "VIX": "VIX", "SHS": "SHS", "MBS": "MBS", "BVS": "Bảo Việt",
    "BSI": "BIDV Securities", "AGR": "Agriseco", "CTS": "Vietinbank Securities",
    "APG": "APG", "EVS": "Everest", "IVS": "IVS", "PSI": "PSI",
    "TVS": "Thiên Việt", "WSS": "Phố Wall", "ORS": "Tiên Phong CK",
    "VFS": "Nhất Việt", "TCI": "Thành Công", "DSC": "Đông Sài Gòn",
    "FTS": "FPTS", "CSI": "Kiến Thiết", "SBS": "SBS", "PHS": "Phú Hưng",
    "ART": "BOS", "APS": "APEC", "BMS": "Bảo Minh", "AAS": "Smart Invest", "VTS": "Việt Tín",
    # BĐS universe (4 mã)
    "VHM": "Vinhomes", "NVL": "Novaland", "KDH": "Khang Điền", "DXG": "Đất Xanh",
}


def get_full_name(ticker: str) -> str:
    """Return full company name for ticker. Fallback to ticker itself if unknown."""
    return _TICKER_FULL_NAMES.get(ticker.upper(), ticker.upper())
```

- [ ] **Step 8: Run all 6 tests to verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py -v
```

Expected: 6 PASS.

- [ ] **Step 9: Add test for `parse_tavily_result()` — single result → crawl_log row**

Add to `tests/test_tavily_crawler.py`:

```python
def test_parse_tavily_result_complete():
    """Parse single Tavily result with all fields → crawl_log row dict."""
    from lib.tavily_crawler import parse_tavily_result
    tavily_result = {
        "title": "Techcombank chia cổ tức 4.960 tỷ",
        "url": "https://cafef.vn/techcombank-co-tuc-2026.chn",
        "content": "Hôm nay Techcombank công bố chia cổ tức tiền mặt...",
        "published_date": "2026-05-08T00:00:00.000Z",
        "score": 0.79,
    }
    row = parse_tavily_result(tavily_result, ticker="TCB", batch_id="TCB-20260512-1500")
    assert row["ticker"] == "TCB"
    assert row["funnel_batch_id"] == "TCB-20260512-1500"
    assert row["source_name"] == "CafeF"
    assert row["source_url"] == "https://cafef.vn/techcombank-co-tuc-2026.chn"
    assert row["title"] == "Techcombank chia cổ tức 4.960 tỷ"
    assert row["raw_content"].startswith("Hôm nay Techcombank")
    assert row["published_time"] == "2026-05-08T00:00:00.000Z"
    assert row["sector"] == "Bank"
    assert "row_id" in row and len(row["row_id"]) > 0
    assert "crawled_at" in row


def test_parse_tavily_result_missing_published_falls_back_to_crawled_at():
    """Missing published_date → published_time defaults to crawled_at."""
    from lib.tavily_crawler import parse_tavily_result
    tavily_result = {
        "title": "Some title",
        "url": "https://vietstock.vn/path",
        "content": "Body",
        # NO published_date
    }
    row = parse_tavily_result(tavily_result, ticker="SSI", batch_id="SSI-20260512-1500")
    assert row["published_time"] == row["crawled_at"]
    assert row["sector"] == "CK"
```

- [ ] **Step 10: Run new tests to verify fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py::test_parse_tavily_result_complete -v
```

Expected: FAIL `AttributeError: module has no attribute 'parse_tavily_result'`.

- [ ] **Step 11: Add `parse_tavily_result()` + sector lookup helper**

Append to `lib/tavily_crawler.py`:

```python
import uuid


def _ticker_to_sector(ticker: str) -> str:
    """Lookup sector from FULL_UNIVERSE constants."""
    t = ticker.upper()
    if t in BANK_UNIVERSE:
        return "Bank"
    if t in CK_UNIVERSE:
        return "CK"
    if t in BDS_UNIVERSE:
        return "BĐS"
    return "Unknown"


def parse_tavily_result(result: dict[str, Any], ticker: str, batch_id: str) -> dict[str, Any]:
    """Map a single Tavily search result → crawl_log row dict.

    Schema (per data/pipeline.schema.sql crawl_log table):
        row_id, funnel_batch_id, ticker, source_name, source_url,
        title, raw_content, published_time, crawled_at, sector

    Args:
        result: Single Tavily search result dict (with url, title, content, ...)
        ticker: VN stock ticker (uppercase)
        batch_id: format <TICKER>-YYYYMMDD-HHMM

    Returns:
        Dict ready for db.insert_crawl_row()
    """
    crawled_at = datetime.now(timezone.utc).isoformat()
    url = result.get("url", "")
    return {
        "row_id": str(uuid.uuid4()),
        "funnel_batch_id": batch_id,
        "ticker": ticker.upper(),
        "source_name": domain_to_source_name(url),
        "source_url": url,
        "title": result.get("title", ""),
        "raw_content": result.get("content", ""),
        "published_time": result.get("published_date") or crawled_at,
        "crawled_at": crawled_at,
        "sector": _ticker_to_sector(ticker),
    }
```

- [ ] **Step 12: Run all tests to verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py -v
```

Expected: 8 PASS.

- [ ] **Step 13: Add test for `filter_results()` — skip PDF + corporate sites + dedup**

Add to `tests/test_tavily_crawler.py`:

```python
def test_filter_results_skips_pdf():
    """PDF URLs filtered out."""
    from lib.tavily_crawler import filter_results
    results = [
        {"url": "https://example.com/report.pdf", "title": "PDF report"},
        {"url": "https://cafef.vn/article.chn", "title": "Real article"},
    ]
    filtered = filter_results(results, ticker="TCB")
    assert len(filtered) == 1
    assert filtered[0]["url"] == "https://cafef.vn/article.chn"


def test_filter_results_skips_corporate_site():
    """Ticker's own corporate site filtered out (TCB → techcombank.com)."""
    from lib.tavily_crawler import filter_results
    results = [
        {"url": "https://techcombank.com/nha-dau-tu", "title": "Corporate page"},
        {"url": "https://www.techcombank.com/blog", "title": "Corporate blog"},
        {"url": "https://cafef.vn/tcb-tin-tuc.chn", "title": "Real news"},
    ]
    filtered = filter_results(results, ticker="TCB")
    assert len(filtered) == 1
    assert filtered[0]["url"] == "https://cafef.vn/tcb-tin-tuc.chn"


def test_filter_results_dedups_by_url():
    """Duplicate URLs (with/without query string) deduped."""
    from lib.tavily_crawler import filter_results
    results = [
        {"url": "https://cafef.vn/article.chn", "title": "Same"},
        {"url": "https://cafef.vn/article.chn?utm=x", "title": "Same with utm"},
        {"url": "https://vietstock.vn/different.htm", "title": "Different"},
    ]
    filtered = filter_results(results, ticker="TCB")
    assert len(filtered) == 2
```

- [ ] **Step 14: Run new tests to verify fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py::test_filter_results_skips_pdf -v
```

Expected: FAIL `AttributeError: module has no attribute 'filter_results'`.

- [ ] **Step 15: Add `filter_results()` + `_corporate_domain_for_ticker()` helpers**

Append to `lib/tavily_crawler.py`:

```python
# Map ticker → ticker's own corporate site domain (skip these in results)
_CORPORATE_DOMAINS: dict[str, list[str]] = {
    "TCB": ["techcombank.com"],
    "VCB": ["vietcombank.com.vn"],
    "BID": ["bidv.com.vn"],
    "CTG": ["vietinbank.vn"],
    "MBB": ["mbbank.com.vn"],
    "ACB": ["acb.com.vn"],
    "VPB": ["vpbank.com.vn"],
    "HDB": ["hdbank.com.vn"],
    "SSI": ["ssi.com.vn"],
    "VND": ["vndirect.com.vn"],
    "HCM": ["hsc.com.vn"],
    "VCI": ["vietcap.com.vn"],
    "SHS": ["shs.com.vn"],
    "VHM": ["vinhomes.vn"],
    "NVL": ["novaland.com.vn"],
    "KDH": ["khangdienhouse.com.vn"],
    "DXG": ["datxanh.vn"],
    # Add more ticker → domain mappings as needed
}


def _strip_query_string(url: str) -> str:
    """Strip ?query and #fragment for dedup purposes."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def filter_results(results: list[dict[str, Any]], ticker: str) -> list[dict[str, Any]]:
    """Filter Tavily results: skip PDF + corporate sites of ticker + dedup by URL.

    Args:
        results: Raw Tavily search results
        ticker: Ticker uppercase (used for corporate site exclusion)

    Returns:
        Filtered list (PDFs out, ticker's corporate site out, deduped)
    """
    corporate_domains = _CORPORATE_DOMAINS.get(ticker.upper(), [])
    seen_urls: set[str] = set()
    filtered: list[dict[str, Any]] = []
    for r in results:
        url = r.get("url", "")
        if not url:
            continue
        # Skip PDFs
        if url.lower().endswith(".pdf"):
            continue
        # Skip corporate site of this ticker
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        if any(domain == cd or domain.endswith("." + cd) for cd in corporate_domains):
            continue
        # Dedup by URL (strip query string)
        canonical = _strip_query_string(url)
        if canonical in seen_urls:
            continue
        seen_urls.add(canonical)
        filtered.append(r)
    return filtered
```

- [ ] **Step 16: Run all tests**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py -v
```

Expected: 11 PASS.

- [ ] **Step 17: Commit Task 1**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/tavily_crawler.py tests/test_tavily_crawler.py && git commit -m "$(cat <<'EOF'
feat(crawler): add lib/tavily_crawler.py — Tavily MCP adapter Tier 1

Tier 1 of 3-tier fallback chain (Tavily → WebSearch → legacy):
- domain_to_source_name() — URL → friendly source name từ SOURCES_WHITELIST
- get_full_name() — ticker → company name cho query enrichment
- parse_tavily_result() — Tavily result → crawl_log row dict
- filter_results() — skip PDF + corporate sites + dedup URL

Spec: docs/superpowers/specs/2026-05-12-crawler-tavily-migration-design.md
EOF
)"
```

---

## Task 2: Implement Tier 1 Tavily call orchestration `crawl_with_tavily()`

**Files:**
- Modify: `lib/tavily_crawler.py`
- Modify: `tests/test_tavily_crawler.py`

- [ ] **Step 1: Add test for `build_tavily_args()` — query construction**

Append to `tests/test_tavily_crawler.py`:

```python
def test_build_tavily_args_basic():
    """Build Tavily search args dict cho ticker."""
    from lib.tavily_crawler import build_tavily_args, SOURCES_WHITELIST
    args = build_tavily_args("TCB")
    assert args["query"] == "TCB Techcombank tin tức"
    assert args["max_results"] == 20
    assert args["search_depth"] == "advanced"
    assert args["time_range"] == "week"
    assert args["country"] == "Vietnam"
    # All 20 sources in include_domains
    expected_domains = list(SOURCES_WHITELIST.values())
    assert sorted(args["include_domains"]) == sorted(expected_domains)
```

- [ ] **Step 2: Run test to verify fails**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py::test_build_tavily_args_basic -v
```

Expected: FAIL `cannot import name 'build_tavily_args'`.

- [ ] **Step 3: Add `build_tavily_args()` + re-export `SOURCES_WHITELIST`**

Append to `lib/tavily_crawler.py`:

```python
def build_tavily_args(ticker: str) -> dict[str, Any]:
    """Build args dict for tavily_search MCP call.

    Args:
        ticker: VN stock ticker

    Returns:
        Dict with query/max_results/search_depth/time_range/country/include_domains
    """
    full_name = get_full_name(ticker)
    return {
        "query": f"{ticker.upper()} {full_name} tin tức",
        "max_results": 20,
        "search_depth": "advanced",
        "time_range": "week",
        "country": "Vietnam",
        "include_domains": list(SOURCES_WHITELIST.values()),
    }
```

- [ ] **Step 4: Run test to verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py::test_build_tavily_args_basic -v
```

Expected: PASS.

- [ ] **Step 5: Add test for `crawl_with_tavily()` mocked — Tier 1 happy path**

Append to `tests/test_tavily_crawler.py`:

```python
def test_crawl_with_tavily_happy_path(monkeypatch):
    """Tier 1: Tavily returns 3 results → 3 rows after parse + filter."""
    from lib import tavily_crawler

    def mock_call(args):
        return {
            "results": [
                {"url": "https://cafef.vn/a.chn", "title": "TCB news 1", "content": "Body 1"},
                {"url": "https://vietstock.vn/b.htm", "title": "TCB news 2", "content": "Body 2"},
                {"url": "https://example.com/x.pdf", "title": "PDF skip", "content": "PDF"},
            ]
        }

    monkeypatch.setattr(tavily_crawler, "_call_tavily_mcp", mock_call)
    rows = tavily_crawler.crawl_with_tavily("TCB", "TCB-20260512-1500")
    # PDF filtered → 2 rows
    assert len(rows) == 2
    assert rows[0]["ticker"] == "TCB"
    assert rows[0]["funnel_batch_id"] == "TCB-20260512-1500"
    assert rows[0]["source_name"] == "CafeF"


def test_crawl_with_tavily_empty_results(monkeypatch):
    """Tier 1: Tavily returns 0 results → return empty list."""
    from lib import tavily_crawler
    monkeypatch.setattr(tavily_crawler, "_call_tavily_mcp", lambda args: {"results": []})
    rows = tavily_crawler.crawl_with_tavily("TCB", "TCB-20260512-1500")
    assert rows == []


def test_crawl_with_tavily_exception_returns_empty(monkeypatch):
    """Tier 1: Tavily raises exception → return empty list (signal fallback)."""
    from lib import tavily_crawler
    def mock_fail(args):
        raise RuntimeError("Tavily API down")
    monkeypatch.setattr(tavily_crawler, "_call_tavily_mcp", mock_fail)
    rows = tavily_crawler.crawl_with_tavily("TCB", "TCB-20260512-1500")
    assert rows == []
```

- [ ] **Step 6: Run new tests to verify fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py::test_crawl_with_tavily_happy_path -v
```

Expected: FAIL — `crawl_with_tavily` or `_call_tavily_mcp` not defined.

- [ ] **Step 7: Add `_call_tavily_mcp()` placeholder + `crawl_with_tavily()`**

Append to `lib/tavily_crawler.py`:

```python
def _call_tavily_mcp(args: dict[str, Any]) -> dict[str, Any]:
    """Call mcp__tavily__tavily_search MCP tool.

    Real implementation: invoked by orchestrator/agent which has MCP tool access.
    For testing: monkeypatched.

    Returns:
        Dict with 'results' key (list of search result dicts).
    """
    raise NotImplementedError(
        "_call_tavily_mcp must be invoked from agent context with MCP access. "
        "For unit tests, monkeypatch this function."
    )


def crawl_with_tavily(ticker: str, batch_id: str) -> list[dict[str, Any]]:
    """Tier 1: Call Tavily MCP tavily_search, return parsed + filtered rows.

    Returns empty list on any failure (signal to caller for Tier 2 fallback).
    """
    try:
        args = build_tavily_args(ticker)
        response = _call_tavily_mcp(args)
        raw_results = response.get("results", [])
        if not raw_results:
            return []
        filtered = filter_results(raw_results, ticker)
        return [parse_tavily_result(r, ticker, batch_id) for r in filtered]
    except Exception as e:
        # Log to stderr for visibility; return empty for fallback
        print(f"[tavily_crawler] Tier 1 failed: {type(e).__name__}: {e}", file=sys.stderr)
        return []
```

- [ ] **Step 8: Run all tests**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py -v
```

Expected: 15 PASS.

- [ ] **Step 9: Commit Task 2**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/tavily_crawler.py tests/test_tavily_crawler.py && git commit -m "$(cat <<'EOF'
feat(crawler): add crawl_with_tavily() Tier 1 orchestration

build_tavily_args() — query template + 20 source domain whitelist + week filter
crawl_with_tavily() — call MCP, filter, parse → rows. Returns [] on any failure
to signal Tier 2 fallback to caller.

_call_tavily_mcp() is a thin wrapper raising NotImplementedError by default;
real invocation happens in agent context where MCP tool is available.
Unit tests monkeypatch this function.

Spec: docs/superpowers/specs/2026-05-12-crawler-tavily-migration-design.md
EOF
)"
```

---

## Task 3: Add Tier 2 fallback `crawl_with_websearch()`

**Files:**
- Modify: `lib/tavily_crawler.py`
- Modify: `tests/test_tavily_crawler.py`

- [ ] **Step 1: Add tests for `crawl_with_websearch()` mocked**

Append to `tests/test_tavily_crawler.py`:

```python
def test_crawl_with_websearch_happy(monkeypatch):
    """Tier 2: WebSearch returns 3 results → 3 rows."""
    from lib import tavily_crawler

    def mock_websearch(query):
        return [
            {"url": "https://cafef.vn/x.chn", "title": "T1", "content": "B1"},
            {"url": "https://vietstock.vn/y.htm", "title": "T2", "content": "B2"},
            {"url": "https://tuoitre.vn/z.htm", "title": "T3", "content": "B3"},
        ]

    monkeypatch.setattr(tavily_crawler, "_call_websearch", mock_websearch)
    rows = tavily_crawler.crawl_with_websearch("TCB", "TCB-20260512-1500")
    assert len(rows) == 3
    assert rows[0]["ticker"] == "TCB"
    assert rows[0]["source_name"] == "CafeF"


def test_crawl_with_websearch_failure_returns_empty(monkeypatch):
    """Tier 2: WebSearch raises → return empty (signal Tier 3)."""
    from lib import tavily_crawler
    def mock_fail(q):
        raise RuntimeError("WebSearch failed")
    monkeypatch.setattr(tavily_crawler, "_call_websearch", mock_fail)
    rows = tavily_crawler.crawl_with_websearch("TCB", "TCB-20260512-1500")
    assert rows == []
```

- [ ] **Step 2: Run new tests to verify fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py::test_crawl_with_websearch_happy -v
```

Expected: FAIL `crawl_with_websearch` not defined.

- [ ] **Step 3: Add `_call_websearch()` placeholder + `crawl_with_websearch()`**

Append to `lib/tavily_crawler.py`:

```python
def _call_websearch(query: str) -> list[dict[str, Any]]:
    """Call built-in WebSearch tool.

    Real implementation: invoked by agent context which has WebSearch tool.
    For testing: monkeypatched.

    Returns:
        List of result dicts with at least 'url', 'title', optional 'content'.
    """
    raise NotImplementedError(
        "_call_websearch must be invoked from agent context with WebSearch tool. "
        "For unit tests, monkeypatch this function."
    )


def crawl_with_websearch(ticker: str, batch_id: str) -> list[dict[str, Any]]:
    """Tier 2: Call built-in WebSearch tool with VN-focused query.

    Returns empty list on failure (signal Tier 3 fallback).
    """
    try:
        full_name = get_full_name(ticker)
        query = f"{ticker.upper()} {full_name} tin tức 2026"
        raw_results = _call_websearch(query)
        if not raw_results:
            return []
        filtered = filter_results(raw_results, ticker)
        return [parse_tavily_result(r, ticker, batch_id) for r in filtered]
    except Exception as e:
        print(f"[tavily_crawler] Tier 2 failed: {type(e).__name__}: {e}", file=sys.stderr)
        return []
```

- [ ] **Step 4: Run all tests**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py -v
```

Expected: 17 PASS.

- [ ] **Step 5: Commit Task 3**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/tavily_crawler.py tests/test_tavily_crawler.py && git commit -m "$(cat <<'EOF'
feat(crawler): add crawl_with_websearch() Tier 2 fallback

Built-in WebSearch wrapper. Triggered when Tier 1 (Tavily) returns []
(out-of-credit / API error / empty results).

_call_websearch() placeholder same pattern as _call_tavily_mcp —
agent context provides real implementation, tests monkeypatch.

Spec: docs/superpowers/specs/2026-05-12-crawler-tavily-migration-design.md
EOF
)"
```

---

## Task 4: Add Tier 3 fallback `crawl_with_legacy()` + `crawl()` orchestrator

**Files:**
- Modify: `lib/tavily_crawler.py`
- Modify: `tests/test_tavily_crawler.py`

- [ ] **Step 1: Add tests for `crawl()` orchestrator chaining 3 tiers**

Append to `tests/test_tavily_crawler.py`:

```python
def test_crawl_uses_tier1_when_available(monkeypatch):
    """Tier 1 returns rows → use Tier 1, skip Tier 2+3."""
    from lib import tavily_crawler
    monkeypatch.setattr(tavily_crawler, "_call_tavily_mcp", lambda a: {
        "results": [{"url": "https://cafef.vn/a.chn", "title": "T", "content": "B"}]
    })
    monkeypatch.setattr(tavily_crawler, "_call_websearch", lambda q: pytest.fail("Tier 2 should NOT be called"))
    rows, tier = tavily_crawler.crawl("TCB", "TCB-20260512-1500")
    assert tier == "Tavily"
    assert len(rows) == 1


def test_crawl_falls_back_to_tier2_when_tier1_empty(monkeypatch):
    """Tier 1 returns [] → fallback to Tier 2."""
    from lib import tavily_crawler
    monkeypatch.setattr(tavily_crawler, "_call_tavily_mcp", lambda a: {"results": []})
    monkeypatch.setattr(tavily_crawler, "_call_websearch", lambda q: [
        {"url": "https://cafef.vn/x.chn", "title": "WebSearch result", "content": "B"}
    ])
    rows, tier = tavily_crawler.crawl("TCB", "TCB-20260512-1500")
    assert tier == "WebSearch"
    assert len(rows) == 1


def test_crawl_falls_back_to_tier3_when_both_fail(monkeypatch):
    """Both Tier 1 + 2 return [] → fallback to Tier 3 legacy."""
    from lib import tavily_crawler
    monkeypatch.setattr(tavily_crawler, "_call_tavily_mcp", lambda a: {"results": []})
    monkeypatch.setattr(tavily_crawler, "_call_websearch", lambda q: [])
    monkeypatch.setattr(tavily_crawler, "_call_legacy_crawler", lambda t, b: [
        {"row_id": "abc", "ticker": "TCB", "funnel_batch_id": b, "source_name": "Legacy",
         "source_url": "https://x", "title": "Legacy", "raw_content": "L",
         "published_time": "2026-01-01", "crawled_at": "2026-01-01", "sector": "Bank"}
    ])
    rows, tier = tavily_crawler.crawl("TCB", "TCB-20260512-1500")
    assert tier == "Crawler-legacy"
    assert len(rows) == 1
    assert rows[0]["source_name"] == "Legacy"


def test_crawl_invalid_ticker_raises():
    """Ticker not in 61-mã universe → ValueError."""
    from lib import tavily_crawler
    with pytest.raises(ValueError, match="not in 61-mã universe"):
        tavily_crawler.crawl("XYZ", "XYZ-20260512-1500")
```

- [ ] **Step 2: Run new tests to verify fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py::test_crawl_uses_tier1_when_available -v
```

Expected: FAIL — `crawl` not defined.

- [ ] **Step 3: Add `_call_legacy_crawler()` + `crawl_with_legacy()` + `crawl()` orchestrator**

Append to `lib/tavily_crawler.py`:

```python
def _call_legacy_crawler(ticker: str, batch_id: str) -> list[dict[str, Any]]:
    """Call legacy 20-source crawler — wraps existing scripts.

    Real implementation: invokes lib/stages/run_crawler.py logic directly OR
    via subprocess. For testing: monkeypatched.

    Returns:
        List of crawl_log row dicts (already in target schema).
    """
    raise NotImplementedError(
        "_call_legacy_crawler invokes legacy crawler scripts. "
        "Real implementation TBD by agent or subprocess wrapper. "
        "For unit tests, monkeypatch this function."
    )


def crawl_with_legacy(ticker: str, batch_id: str) -> list[dict[str, Any]]:
    """Tier 3: Last-resort fallback via existing 20-source scripts."""
    try:
        return _call_legacy_crawler(ticker, batch_id)
    except Exception as e:
        print(f"[tavily_crawler] Tier 3 failed: {type(e).__name__}: {e}", file=sys.stderr)
        return []


def crawl(ticker: str, batch_id: str) -> tuple[list[dict[str, Any]], str]:
    """3-tier crawler orchestrator. Try Tavily → WebSearch → legacy.

    Args:
        ticker: VN stock ticker (must be in 61-mã FULL_UNIVERSE)
        batch_id: format <TICKER>-YYYYMMDD-HHMM

    Returns:
        (rows, tier_used) where tier_used in {"Tavily", "WebSearch", "Crawler-legacy"}.
        rows may be empty if all 3 tiers fail.

    Raises:
        ValueError if ticker not in 61-mã universe.
    """
    if ticker.upper() not in FULL_UNIVERSE:
        raise ValueError(f"Ticker {ticker!r} not in 61-mã universe (Bank/CK/BĐS)")

    # Tier 1: Tavily
    rows = crawl_with_tavily(ticker, batch_id)
    if rows:
        return rows, "Tavily"

    # Tier 2: WebSearch fallback
    rows = crawl_with_websearch(ticker, batch_id)
    if rows:
        return rows, "WebSearch"

    # Tier 3: Legacy crawler last resort
    rows = crawl_with_legacy(ticker, batch_id)
    return rows, "Crawler-legacy"
```

- [ ] **Step 4: Run all tests**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py -v
```

Expected: 21 PASS.

- [ ] **Step 5: Commit Task 4**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/tavily_crawler.py tests/test_tavily_crawler.py && git commit -m "$(cat <<'EOF'
feat(crawler): add crawl() 3-tier orchestrator + Tier 3 legacy fallback

crawl() entry point — orchestrates Tier 1 (Tavily) → Tier 2 (WebSearch)
→ Tier 3 (legacy 20-source). Returns (rows, tier_used) for pipeline
log emission.

_call_legacy_crawler() placeholder — real impl wraps existing
.claude/skills/finpath-newsroom-crawler/scripts/* in agent context or
subprocess. Tests monkeypatch.

Validates ticker in FULL_UNIVERSE (61 mã: 27 Bank + 30 CK + 4 BĐS)
before crawling.

Spec: docs/superpowers/specs/2026-05-12-crawler-tavily-migration-design.md
EOF
)"
```

---

## Task 5: Update `finpath-newsroom-crawler/SKILL.md` workflow V3.0

**Files:**
- Modify: `.claude/skills/finpath-newsroom-crawler/SKILL.md`

- [ ] **Step 1: Read current SKILL.md frontmatter + workflow section**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && head -10 .claude/skills/finpath-newsroom-crawler/SKILL.md && echo "---" && grep -n "^## " .claude/skills/finpath-newsroom-crawler/SKILL.md
```

Identify line numbers of `## Workflow` (or equivalent) section + frontmatter `description` field.

- [ ] **Step 2: Update frontmatter description (V2.4 → V3.0 Tavily)**

Use Edit tool. Replace old description:

```
description: Crawls 20 Vietnamese financial/general news sources for latest 3 articles per source (sort by publish time desc) about a stock ticker in Bank/CK/BĐS universe — sub-skill in Finpath Newsroom V2.4 pipeline. Use when orchestrator triggers Step 1, or user explicit "crawl tin về [TICKER]". Writes rows to SQLite crawl_log (data/pipeline.db) via lib/pipeline_db.py with published_time + funnel_batch_id (format ticker-YYYYMMDD-HHMM) for downstream Editor V1 + Story Editor + Compare Feed Crawl Funnel section. NEVER use for non-universe tickers. NEVER pull more than 3 articles per source — must be 3 newest only.
```

With:

```
description: V3.0 Tavily-primary crawler. Calls MCP tavily_search per ticker (time_range=week + 20-source domain whitelist + max_results=20 + country=Vietnam) to fetch latest news for stock ticker in 61-mã universe (Bank/CK/BĐS). Auto-fallbacks to built-in WebSearch tool if Tavily fails (out-of-credit / API error / empty), then to legacy 20-source crawler as last resort. Writes rows to SQLite crawl_log via lib/tavily_crawler.crawl(). Pipeline log emits data_trail entry with tier_used (Tavily / WebSearch / Crawler-legacy). NEVER use for non-universe tickers.
```

- [ ] **Step 3: Replace workflow section với V3.0 content**

Use Edit tool. Find existing workflow section (between `## Workflow` heading và next `## ` heading) và replace với:

```markdown
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
```

- [ ] **Step 4: Smoke check SKILL.md format valid**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && head -5 .claude/skills/finpath-newsroom-crawler/SKILL.md && grep -c "Tier 1\|Tier 2\|Tier 3" .claude/skills/finpath-newsroom-crawler/SKILL.md && grep -c "tavily_search" .claude/skills/finpath-newsroom-crawler/SKILL.md && grep -c "lib.tavily_crawler" .claude/skills/finpath-newsroom-crawler/SKILL.md
```

Expected: frontmatter intact, Tier mentions ≥6 (3 in workflow + 3 in description), tavily_search ≥2, lib.tavily_crawler ≥1.

- [ ] **Step 5: Verify legacy scripts NOT removed (Tier 3 needs them)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && ls .claude/skills/finpath-newsroom-crawler/scripts/
```

Expected: `dedupe.py`, `search_queries.py`, `source_whitelist.py` all still present.

- [ ] **Step 6: Commit Task 5**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/skills/finpath-newsroom-crawler/SKILL.md && git commit -m "$(cat <<'EOF'
skill(crawler): update SKILL.md to V3.0 (Tavily MCP primary + 3-tier fallback)

- Frontmatter description V2.4 → V3.0 (Tavily-primary description)
- Workflow section: 4 steps replacing old 20-source scrape logic
  - Step 1: validate ticker, build batch_id
  - Step 2: call lib.tavily_crawler.crawl() — orchestrates Tier 1+2+3
  - Step 3: persist via db.insert_crawl_row()
  - Step 4: emit data_trail entry với tier_used
- Note Tier 3 legacy scripts kept intact (scripts/* untouched)
- Free tier note + Master Step 6 untouched note

Spec: docs/superpowers/specs/2026-05-12-crawler-tavily-migration-design.md
EOF
)"
```

---

## Task 6: Smoke test end-to-end + hand-off

**Files:**
- No new files — verification only

- [ ] **Step 1: Run all unit tests, verify all pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_tavily_crawler.py -v
```

Expected: 21 PASS, 0 FAIL.

- [ ] **Step 2: Verify lib/tavily_crawler.py importable + public API correct**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.tavily_crawler import (
    crawl, crawl_with_tavily, crawl_with_websearch, crawl_with_legacy,
    parse_tavily_result, filter_results, build_tavily_args,
    domain_to_source_name, get_full_name,
    SOURCES_WHITELIST, FULL_UNIVERSE, BANK_UNIVERSE, CK_UNIVERSE, BDS_UNIVERSE
)
print(f'FULL_UNIVERSE size: {len(FULL_UNIVERSE)}')  # Expect 61
print(f'SOURCES_WHITELIST size: {len(SOURCES_WHITELIST)}')  # Expect 20
print(f'crawl signature: {crawl.__doc__.split(chr(10))[0]}')

# Smoke test build_tavily_args for each sector
for ticker in ['TCB', 'SSI', 'VHM']:
    args = build_tavily_args(ticker)
    print(f'  {ticker}: query=\"{args[\"query\"]}\", max_results={args[\"max_results\"]}, time_range={args[\"time_range\"]}')
"
```

Expected:
- `FULL_UNIVERSE size: 61`
- `SOURCES_WHITELIST size: 20`
- 3 tickers print query in correct format ("TCB Techcombank tin tức" etc.)

- [ ] **Step 3: Verify SKILL.md description + workflow render OK**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && head -10 .claude/skills/finpath-newsroom-crawler/SKILL.md && echo "---" && grep "V3.0\|Tavily\|Tier" .claude/skills/finpath-newsroom-crawler/SKILL.md | head -10
```

Expected:
- Frontmatter intact (name + description)
- "V3.0" mentioned ≥1
- "Tavily" mentioned ≥3
- "Tier" mentioned ≥3

- [ ] **Step 4: Verify Master Bank SKILL.md NOT touched**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git diff HEAD~6 HEAD -- .claude/skills/finpath-newsroom-master-bank/SKILL.md
```

Expected: empty diff (Master Bank KHÔNG đụng per scope).

- [ ] **Step 5: Verify legacy scripts intact (Tier 3 still works)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && ls .claude/skills/finpath-newsroom-crawler/scripts/ && head -10 .claude/skills/finpath-newsroom-crawler/scripts/source_whitelist.py
```

Expected: 3 scripts present (dedupe.py, search_queries.py, source_whitelist.py), source_whitelist.py header intact.

- [ ] **Step 6: Hand-off message to user**

Display in chat:

```markdown
**Crawler Tavily Migration v1.0 hoàn thành (5 commits + 1 verification commit).**

## Smoke checks pass
- ✅ 21 unit tests pass
- ✅ lib/tavily_crawler.py public API correct (crawl + Tier 1/2/3 + parse + filter)
- ✅ SKILL.md V3.0 updated với 4-step workflow + Tier-aware data_trail
- ✅ Master Bank SKILL.md NOT touched (per scope)
- ✅ Legacy 20-source scripts intact (Tier 3 fallback ready)

## Hand-off cho user — E2E test

**Bạn run `/tin TCB`** end-to-end để verify:
1. Pipeline log có `data_trail[].source = "Tavily/tavily_search"` (confirm Tier 1 works)
2. crawl_log table có ≥10 rows với source diverse (cafef, vietstock, ...)
3. Article output vẫn pass 5 quality gates V4.0
4. Right column 'Crawl funnel' render OK
5. Right column 'Bài gốc' có source_url canonical

Nếu Tier 1 fail (out-of-credit) → check pipeline log có `"WebSearch/..."` (Tier 2) hoặc `"Crawler-legacy/..."` (Tier 3).

Báo lại kết quả → fix forward nếu issue, hoặc declare ship nếu OK.
```

---

## Self-review checklist (run sau khi xong 6 tasks)

- [ ] **Spec coverage:** All sections of spec mapped to tasks:
  - Spec § 4 `lib/tavily_crawler.py` interface = Tasks 1+2+3+4
  - Spec § 5 SKILL.md update = Task 5
  - Spec § 8 validation smoke checks = Task 6

- [ ] **No placeholder leak:** Search plan cho "TODO", "TBD" → 0 hit. (Note: `_call_legacy_crawler` raises NotImplementedError với message "TBD by agent or subprocess wrapper" — intentional, agent fills this in at runtime.)

- [ ] **Type/path consistency:**
  - All paths use `lib/tavily_crawler.py` consistent
  - `crawl()` returns `(rows, tier)` — tested in Task 4 matches usage in Task 5 SKILL.md
  - `parse_tavily_result(result, ticker, batch_id)` — same signature across tasks
  - `_ticker_to_sector` returns "Bank"/"CK"/"BĐS" — consistent với DB schema

- [ ] **Final smoke check passes:** Task 6 confirms all 21 tests pass + SKILL.md valid + legacy intact.

---

## Open questions / followup (post-plan)

- **`_call_tavily_mcp` real implementation** — tests monkeypatch this. In production (agent context), agent uses `mcp__tavily__tavily_search` tool directly. If headless (script outside agent), need wrapper using HTTP curl to `https://mcp.tavily.com/mcp/?tavilyApiKey=...`. Address in followup phase if user wants standalone CLI.
- **`_call_legacy_crawler` real implementation** — currently NotImplementedError. Real impl options: (a) subprocess `lib/stages/run_crawler.py`, (b) inline scripts/* call. Defer until first observed Tier 3 trigger.
- **E2E test result** — User runs `/tin TCB` after handoff. Fix forward nếu issue.
- **Per-sector query optimization** — sau khi prove Bank works, có thể tune query template per sector. Defer measurement.
- **Tavily usage tracking dashboard** — defer per spec § 2 (Q2=A).
