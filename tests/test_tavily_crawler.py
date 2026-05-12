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


def test_parse_tavily_response_happy():
    """Tavily response → list of rows after filter + parse."""
    from lib.tavily_crawler import parse_tavily_response
    response = {
        "results": [
            {"url": "https://cafef.vn/x.chn", "title": "T1", "content": "B1"},
            {"url": "https://example.com/skip.pdf", "title": "PDF", "content": "X"},
            {"url": "https://vietstock.vn/y.htm", "title": "T2", "content": "B2"},
        ]
    }
    rows = parse_tavily_response(response, ticker="TCB", batch_id="TCB-20260512-1500")
    assert len(rows) == 2  # PDF filtered
    assert rows[0]["ticker"] == "TCB"
    assert rows[0]["funnel_batch_id"] == "TCB-20260512-1500"
    assert rows[0]["source_name"] == "CafeF"


def test_parse_tavily_response_empty():
    """Empty results → empty rows."""
    from lib.tavily_crawler import parse_tavily_response
    rows = parse_tavily_response({"results": []}, "TCB", "TCB-20260512-1500")
    assert rows == []


def test_parse_tavily_response_accepts_all_tickers_v5_1_3():
    """V5.1.3: Universe validation deferred to Editor V1 (Finpath sectors cache).
    Tavily crawler accepts ALL tickers — does not pre-gate. Editor V1 Step 2
    V5.1.3 rejects with editor_v1_note='ticker_outside_finpath_139' if needed.
    """
    from lib.tavily_crawler import parse_tavily_response
    rows = parse_tavily_response({"results": []}, "XYZ", "XYZ-20260512-1500")
    assert rows == []


def test_persist_rows_inserts_to_db(tmp_path):
    """persist_rows INSERT rows into crawl_log table."""
    from lib.tavily_crawler import persist_rows
    from lib.pipeline_db import PipelineDB
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    db.init_schema("data/pipeline.schema.sql")

    rows = [
        {
            "row_id": "test-row-1",
            "funnel_batch_id": "TCB-20260512-1500",
            "ticker": "TCB",
            "source_name": "CafeF",
            "source_url": "https://cafef.vn/test.chn",
            "title": "Test article",
            "raw_content": "Body content",
            "published_time": "2026-05-12T00:00:00+00:00",
            "crawled_at": "2026-05-12T15:00:00+00:00",
            "sector": "Bank",
        }
    ]
    count = persist_rows(rows, db)
    assert count == 1

    # Verify row in DB
    cur = db.conn.execute("SELECT row_id, ticker, source_name FROM crawl_log WHERE row_id = ?", ("test-row-1",))
    row = cur.fetchone()
    assert row is not None
    assert row["ticker"] == "TCB"
    assert row["source_name"] == "CafeF"
    db.conn.close()
