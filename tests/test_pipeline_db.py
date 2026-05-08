"""Tests for lib.pipeline_db — SQLite ops on crawl_log + generated_news."""
import pytest
from pathlib import Path

from lib.pipeline_db import PipelineDB


@pytest.fixture
def db():
    """Fresh in-memory DB initialized with schema."""
    schema_path = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db = PipelineDB(":memory:")
    db.init_schema(schema_path)
    yield db
    db.close()


def test_init_schema_creates_tables(db):
    """Schema init creates crawl_log + generated_news tables."""
    tables = db.list_tables()
    assert "crawl_log" in tables
    assert "generated_news" in tables


def test_insert_crawl_row_returns_row_id(db):
    """insert_crawl_row returns the row_id used."""
    row_id = db.insert_crawl_row({
        "row_id": "uuid-1",
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "Báo Pháp luật",
        "source_url": "https://example.com/a1",
        "title": "Test article",
        "crawled_at": "2026-05-08T15:30:00+07:00",
    })
    assert row_id == "uuid-1"


def test_insert_duplicate_url_raises(db):
    """Inserting same source_url twice raises (UNIQUE constraint)."""
    base = {
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": "https://example.com/dup",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    }
    db.insert_crawl_row({"row_id": "u1", **base})
    with pytest.raises(Exception):
        db.insert_crawl_row({"row_id": "u2", **base})


def test_get_crawl_row_returns_dict(db):
    """get_crawl_row returns dict with all fields, None for unset."""
    db.insert_crawl_row({
        "row_id": "uuid-2",
        "funnel_batch_id": "TCB-20260508-1530",
        "ticker": "TCB",
        "source_name": "VnEconomy",
        "source_url": "https://example.com/a2",
        "title": "T2",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    row = db.get_crawl_row("uuid-2")
    assert row["ticker"] == "TCB"
    assert row["status"] == "pending"
    assert row["editor_v1_decision"] is None


def test_update_crawl_row_partial(db):
    """update_crawl_row updates only the keys passed."""
    db.insert_crawl_row({
        "row_id": "uuid-3",
        "funnel_batch_id": "B",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": "https://example.com/a3",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    db.update_crawl_row("uuid-3", {
        "editor_v1_decision": "route_to_story_editor",
        "primary_ticker": "VCB",
        "sector": "Bank",
    })
    row = db.get_crawl_row("uuid-3")
    assert row["editor_v1_decision"] == "route_to_story_editor"
    assert row["sector"] == "Bank"
    assert row["title"] == "T"


def test_query_by_funnel_batch(db):
    """query_by_funnel_batch returns all rows for batch_id, sorted by crawled_at desc."""
    for i, ts in enumerate(["2026-05-08T10:00:00+07:00", "2026-05-08T12:00:00+07:00"]):
        db.insert_crawl_row({
            "row_id": f"u{i}",
            "funnel_batch_id": "VCB-20260508-1530",
            "ticker": "VCB",
            "source_name": f"S{i}",
            "source_url": f"https://example.com/{i}",
            "title": "T",
            "crawled_at": ts,
        })
    rows = db.query_by_funnel_batch("VCB-20260508-1530")
    assert len(rows) == 2
    assert rows[0]["crawled_at"] == "2026-05-08T12:00:00+07:00"


def test_insert_generated_news_links_to_crawl_row(db):
    """generated_news insert with row_id FK works + recent_generated_news queries it."""
    db.insert_crawl_row({
        "row_id": "u-anchor",
        "funnel_batch_id": "B",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": "https://example.com/anchor",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    aid = db.insert_generated_news({
        "article_id": "art-1",
        "row_id": "u-anchor",
        "ticker": "VCB",
        "sector": "Bank",
        "title": "Article title",
        "body": "Body...",
        "word_count": 354,
        "accepted_hypothesis": 1,
        "status": "published",
        "published_at": "2026-05-08T16:00:00+07:00",
    })
    assert aid == "art-1"
    arts = db.recent_generated_news("VCB", limit=3)
    assert len(arts) == 1
    assert arts[0]["title"] == "Article title"
