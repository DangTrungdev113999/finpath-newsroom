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
