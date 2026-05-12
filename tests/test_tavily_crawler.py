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


def test_filter_results_skips_pdf():
    """PDF URLs filtered out, including with query strings."""
    from lib.tavily_crawler import filter_results
    results = [
        {"url": "https://example.com/report.pdf", "title": "PDF report"},
        {"url": "https://example.com/download.pdf?ver=2", "title": "PDF with query"},
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
