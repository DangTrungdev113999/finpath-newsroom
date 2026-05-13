"""Tavily-based crawler adapter for Finpath Newsroom Step 1.

Agent-fetch + script-persist pattern (V1.1):
- Agent invokes MCP/WebSearch tools and captures raw JSON response.
- Agent pipes JSON to this script via stdin for parse + persist.
- Script does NOT make HTTP calls itself (matches lib/stages/run_crawler.py).

Spec v1.1: docs/superpowers/specs/2026-05-12-crawler-tavily-migration-design.md
"""
from __future__ import annotations
import sys
import unicodedata
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse
from typing import Any

# V3.2 — 3-day window for post-fetch date filter.
DATE_WINDOW_DAYS = 3

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
    # V5.1.3 expansion — non-financial large caps (Finpath ~139 universe)
    "HPG": "Hòa Phát", "HSG": "Hoa Sen", "NKG": "Nam Kim",
    "VNM": "Vinamilk", "MSN": "Masan", "SAB": "Sabeco", "BHN": "Habeco",
    "KDC": "Kido", "MCM": "Mộc Châu Milk", "QNS": "Đường Quảng Ngãi",
    "MWG": "Thế Giới Di Động", "FRT": "FPT Retail", "DGW": "Digiworld",
    "PNJ": "Phú Nhuận", "AST": "Taseco Airs",
    "VHC": "Vĩnh Hoàn", "ANV": "Nam Việt", "MPC": "Minh Phú",
    "FMC": "Sao Ta", "IDI": "IDI", "CMX": "Camimex",
    "TCM": "Thành Công", "MSH": "May Sông Hồng", "TNG": "TNG",
    "BSR": "Bình Sơn", "PVS": "PTSC", "GAS": "PV Gas", "POW": "PV Power",
    "PLX": "Petrolimex", "OIL": "PVOIL", "PVD": "PV Drilling", "PVT": "PVTrans",
    "GMD": "Gemadept", "HAH": "Hải An", "VOS": "Vinaship", "VSC": "Viconship",
    "PHP": "Cảng Hải Phòng", "CDN": "Cảng Đà Nẵng", "HAX": "Haxaco",
    "FPT": "FPT", "REE": "REE", "PC1": "PC1", "GEX": "Gelex",
    "ITD": "ITD", "TRA": "Traphaco", "DBD": "Bidiphar",
    "IMP": "Imexpharm", "ELC": "ELC", "VIC": "Vingroup", "VRE": "Vincom Retail",
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


def fold_vn(s: str) -> str:
    """Lowercase + strip Vietnamese diacritics for substring match.

    "Hòa Phát" → "hoa phat", "Ngân hàng" → "ngan hang".
    """
    if not s:
        return ""
    stripped = "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )
    return stripped.replace("đ", "d").replace("Đ", "D").lower()


def _title_mentions_company(title: str, ticker: str, full_name: str) -> bool:
    """Return True if title mentions ticker code OR full company name.

    Case-insensitive + diacritic-folded. Matches BOTH "HPG" code AND
    "Hòa Phát" / "Hoa Phat" (some báo phổ thông write company name only).
    """
    folded = fold_vn(title)
    if not folded:
        return False
    if ticker.lower() in folded:
        return True
    full_folded = fold_vn(full_name)
    return bool(full_folded) and full_folded in folded


def _parse_published_date(value: str | None) -> datetime | None:
    """Parse Tavily published_date (ISO or YYYY-MM-DD). Return tz-aware UTC datetime or None."""
    if not value:
        return None
    try:
        # ISO with timezone
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        # YYYY-MM-DD only
        try:
            dt = datetime.strptime(value[:10], "%Y-%m-%d")
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def filter_results(
    results: list[dict[str, Any]],
    ticker: str,
    full_name: str | None = None,
    date_window_days: int = DATE_WINDOW_DAYS,
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    """V3.2 — Filter Tavily results with 5 rules.

    Order matters — cheap checks first:
    1. Skip PDFs
    2. Skip ticker's own corporate site
    3. Dedup canonical URL
    4. NEW V3.2 — Title relevance: title must mention ticker code OR full_name
       (case-insensitive, diacritic-folded). Skipped when full_name is None
       (backward compat for callers that don't pass it).
    5. NEW V3.2 — Date window: reject if published_date older than
       (now - date_window_days). MISSING date → optimistic keep (per design).

    Args:
        results: Raw Tavily search results
        ticker: Ticker uppercase (used for corporate site exclusion + title match)
        full_name: Full company name (vd "Hòa Phát") for title relevance — V3.2
        date_window_days: Reject articles older than this many days. Default 3.
        now: Override "current time" (test seam). Default datetime.now(tz=UTC).

    Returns:
        Filtered list — order preserved from Tavily relevance ranking.
    """
    corporate_domains = _CORPORATE_DOMAINS.get(ticker.upper(), [])
    seen_urls: set[str] = set()
    filtered: list[dict[str, Any]] = []
    now_utc = now or datetime.now(timezone.utc)
    cutoff = now_utc - timedelta(days=date_window_days)
    enforce_title = bool(full_name)
    ticker_uc = ticker.upper()

    for r in results:
        url = r.get("url", "")
        if not url:
            continue
        # 1. PDF skip — parse path to catch ?query=string suffix
        parsed = urlparse(url)
        if parsed.path.lower().endswith(".pdf"):
            continue
        # 2. Corporate site skip
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        if any(domain == cd or domain.endswith("." + cd) for cd in corporate_domains):
            continue
        # 3. URL dedup (canonical)
        canonical = _strip_query_string(url)
        if canonical in seen_urls:
            continue
        # 4. V3.2 title relevance — must mention ticker OR full_name
        if enforce_title:
            title = r.get("title", "")
            if not _title_mentions_company(title, ticker_uc, full_name or ""):
                continue
        # 5. V3.2 date window — optimistic keep when missing
        pub_dt = _parse_published_date(r.get("published_date"))
        if pub_dt is not None and pub_dt < cutoff:
            continue
        seen_urls.add(canonical)
        filtered.append(r)
    return filtered


def _resolve_sector_name_safe(ticker: str) -> str:
    """Look up Finpath sector_name (VN label) for ticker. Empty string on any failure.

    V3.2 — used to enrich Tavily query so 1 broader call captures both
    company news + sector news organically (HPG → "Thép", VCB → "Ngân hàng").
    Never raises — caller treats "" as "no sector context, query degrades to
    company-only form" (still works, just less broad).
    """
    try:
        from lib.finpath_sectors import FinpathSectors
        from lib.pipeline_db import PipelineDB
        db = PipelineDB("data/pipeline.db")
        try:
            info = FinpathSectors(db).get_ticker_sector(ticker, allow_refresh=False)
            return info["sector_name"] if info else ""
        finally:
            db.conn.close()
    except Exception:
        return ""


def build_tavily_args(ticker: str, sector_name: str | None = None) -> dict[str, Any]:
    """Build args dict for tavily_search MCP call.

    V3.2 changes vs V3.1:
    - Query enriched with recency phrase + sector_name (broader recall,
      diversifies result mix beyond AGM/earnings cluster).
    - max_results bumped 20 → 50 (Tavily silently caps if free tier <50).
    - include_raw_content=True (enables content-based downstream filters
      if needed; cheap when search_depth=advanced anyway).

    Args:
        ticker: VN stock ticker.
        sector_name: Optional VN sector label (vd "Thép"). If None, resolved
            via Finpath cache. Pass explicit value to skip DB lookup (tests).

    Returns:
        Dict with query/max_results/search_depth/time_range/country/include_domains/include_raw_content
    """
    ticker_uc = ticker.upper()
    full_name = get_full_name(ticker_uc)
    if sector_name is None:
        sector_name = _resolve_sector_name_safe(ticker_uc)
    # Skip duplicate when ticker == its own fallback name (no entry in _TICKER_FULL_NAMES)
    parts = ["Tin mới nhất về", ticker_uc]
    if full_name and full_name.lower() != ticker_uc.lower():
        parts.append(full_name)
    if sector_name:
        parts.append(f"ngành {sector_name}")
    query = " ".join(parts)
    return {
        "query": query,
        "max_results": 50,
        "search_depth": "advanced",
        "time_range": "week",
        "country": "Vietnam",
        "include_domains": list(SOURCES_WHITELIST.values()),
        "include_raw_content": True,
    }


def parse_tavily_response(response: dict[str, Any], ticker: str, batch_id: str) -> list[dict[str, Any]]:
    """Parse Tavily MCP response → list of crawl_log row dicts.

    Pure function. Agent calls mcp__tavily__tavily_search separately and
    passes response here for parsing + filtering.

    V3.2 — filter_results now applies title relevance + 3-day date window
    in addition to existing PDF/corporate/dedup rules. full_name resolved
    via _TICKER_FULL_NAMES so reused across V3.1 and V3.2 call sites.

    Args:
        response: Raw Tavily response dict (with 'results' key)
        ticker: VN stock ticker
        batch_id: format <TICKER>-YYYYMMDD-HHMM

    Returns:
        List of crawl_log row dicts ready for persist_rows().
        Empty list if response has no 'results' or all filtered out.
    """
    # V5.1.3: Universe validation deferred to Editor V1 (Step 2 V5.1.3 — Finpath
    # sectors cache, ~139 mã). Tavily crawler accepts ALL tickers; Editor V1
    # rejects with editor_v1_note="ticker_outside_finpath_139" if not in cache.
    raw_results = response.get("results", [])
    if not raw_results:
        return []
    full_name = get_full_name(ticker)
    filtered = filter_results(raw_results, ticker, full_name=full_name)
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
