"""Tavily-based crawler adapter for Finpath Newsroom Step 1.

Agent-fetch + script-persist pattern (V1.1):
- Agent invokes MCP/WebSearch tools and captures raw JSON response.
- Agent pipes JSON to this script via stdin for parse + persist.
- Script does NOT make HTTP calls itself (matches lib/stages/run_crawler.py).

Spec v1.1: docs/superpowers/specs/2026-05-12-crawler-tavily-migration-design.md
"""
from __future__ import annotations
import sys
import uuid
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
        # Skip PDFs — parse path (not full URL) to catch ?query=string suffix
        parsed = urlparse(url)
        if parsed.path.lower().endswith(".pdf"):
            continue
        # Skip corporate site of this ticker
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


def parse_tavily_response(response: dict[str, Any], ticker: str, batch_id: str) -> list[dict[str, Any]]:
    """Parse Tavily MCP response → list of crawl_log row dicts.

    Pure function. Agent calls mcp__tavily__tavily_search separately and
    passes response here for parsing + filtering.

    Args:
        response: Raw Tavily response dict (with 'results' key)
        ticker: VN stock ticker (must be in 61-mã universe — caller validates)
        batch_id: format <TICKER>-YYYYMMDD-HHMM

    Returns:
        List of crawl_log row dicts ready for persist_rows().
        Empty list if response has no 'results' or all filtered out.

    Raises:
        ValueError if ticker not in 61-mã universe.
    """
    # V5.1.3: Universe validation deferred to Editor V1 (Step 2 V5.1.3 — Finpath
    # sectors cache, ~139 mã). Tavily crawler accepts ALL tickers; Editor V1
    # rejects with editor_v1_note="ticker_outside_finpath_139" if not in cache.
    raw_results = response.get("results", [])
    if not raw_results:
        return []
    filtered = filter_results(raw_results, ticker)
    return [parse_tavily_result(r, ticker, batch_id) for r in filtered]


def persist_rows(rows: list[dict[str, Any]], db: Any) -> int:
    """INSERT rows vào crawl_log table.

    Args:
        rows: list of dicts (output từ parse_tavily_response)
        db: PipelineDB instance (caller manages connection lifecycle)

    Returns:
        Count of rows inserted.
    """
    count = 0
    for row in rows:
        db.insert_crawl_row(row)
        count += 1
    return count


def main() -> int:
    """CLI entry. Usage:
        echo "$TAVILY_JSON" | python -m lib.tavily_crawler <ticker> <batch_id> [--db PATH]

    Reads Tavily MCP response (or WebSearch results array) from stdin,
    parses into crawl_log rows, INSERT into SQLite, print count.

    Stdin format: JSON dict with 'results' key (Tavily-style) OR JSON array
    (WebSearch-style — wrapped to {"results": [...]}).
    """
    import argparse
    import json
    from lib.pipeline_db import PipelineDB

    parser = argparse.ArgumentParser(description="Parse Tavily/WebSearch results + persist to crawl_log")
    parser.add_argument("ticker", help="VN stock ticker (uppercase)")
    parser.add_argument("batch_id", help="Format <TICKER>-YYYYMMDD-HHMM")
    parser.add_argument("--db", default="data/pipeline.db", help="SQLite DB path")
    args = parser.parse_args()

    raw = json.loads(sys.stdin.read())
    # Accept both Tavily dict ({"results": [...]}) and WebSearch array ([...])
    if isinstance(raw, list):
        response = {"results": raw}
    else:
        response = raw

    rows = parse_tavily_response(response, args.ticker, args.batch_id)
    db = PipelineDB(args.db)
    try:
        count = persist_rows(rows, db)
        print(json.dumps({"inserted": count, "ticker": args.ticker, "batch_id": args.batch_id}))
        return 0
    finally:
        db.conn.close()


if __name__ == "__main__":
    sys.exit(main())
