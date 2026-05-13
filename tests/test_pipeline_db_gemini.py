"""Tests for Gemini DB columns + writer method (Phase A5)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from lib import pipeline_db


SCHEMA_SQL = Path(__file__).resolve().parents[1] / "data" / "pipeline.schema.sql"


@pytest.fixture
def db(tmp_path: Path):
    target = tmp_path / "pipeline.db"
    conn = pipeline_db.PipelineDB(str(target))
    conn.init_schema(SCHEMA_SQL)
    yield conn
    conn.close()


GEMINI_COLUMNS = {
    "gemini_title",
    "gemini_body",
    "gemini_word_count",
    "gemini_model",
    "gemini_generated_at",
    "gemini_status",
    "gemini_error",
}


def test_gemini_columns_exist_after_init(db) -> None:
    cur = db.conn.execute("PRAGMA table_info(generated_news)")
    cols = {row["name"] for row in cur.fetchall()}
    assert GEMINI_COLUMNS.issubset(cols), f"missing: {GEMINI_COLUMNS - cols}"


def _seed_article(db, article_id: str = "test-001") -> None:
    # Seed crawl_log row required by FK
    db.conn.execute(
        "INSERT INTO crawl_log (row_id, funnel_batch_id, ticker, source_name, "
        "source_url, title, crawled_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("row-001", "batch-001", "ACB", "test", "http://x", "raw", "2026-05-13"),
    )
    db.conn.execute(
        "INSERT INTO generated_news (article_id, row_id, ticker, sector, title, body, "
        "accepted_hypothesis) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (article_id, "row-001", "ACB", "bank", "T", "B", 1),
    )
    db.conn.commit()


def test_update_gemini_output_success(db) -> None:
    _seed_article(db)
    db.update_gemini_output(
        article_id="test-001",
        status="success",
        title="ACB lãi 5.000 tỷ",
        body="Body markdown",
        word_count=42,
        model="gemini-2.5-pro",
        generated_at="2026-05-13T10:00:00Z",
        error=None,
    )
    cur = db.conn.execute(
        "SELECT gemini_title, gemini_body, gemini_word_count, gemini_model, "
        "gemini_generated_at, gemini_status, gemini_error FROM generated_news "
        "WHERE article_id = ?",
        ("test-001",),
    )
    row = cur.fetchone()
    assert row["gemini_title"] == "ACB lãi 5.000 tỷ"
    assert row["gemini_body"] == "Body markdown"
    assert row["gemini_word_count"] == 42
    assert row["gemini_model"] == "gemini-2.5-pro"
    assert row["gemini_generated_at"] == "2026-05-13T10:00:00Z"
    assert row["gemini_status"] == "success"
    assert row["gemini_error"] is None


def test_update_gemini_output_skipped_failure(db) -> None:
    _seed_article(db)
    db.update_gemini_output(
        article_id="test-001",
        status="skipped_failure",
        error="timeout after retry",
    )
    cur = db.conn.execute(
        "SELECT gemini_status, gemini_error, gemini_body FROM generated_news WHERE article_id = ?",
        ("test-001",),
    )
    row = cur.fetchone()
    assert row["gemini_status"] == "skipped_failure"
    assert row["gemini_error"] == "timeout after retry"
    assert row["gemini_body"] is None  # not populated on failure


def test_update_gemini_output_invalid_status_raises(db) -> None:
    _seed_article(db)
    with pytest.raises(ValueError, match="gemini_status"):
        db.update_gemini_output(article_id="test-001", status="bogus")


def test_legacy_row_has_null_gemini_columns(db) -> None:
    _seed_article(db, article_id="legacy-001")
    cur = db.conn.execute(
        "SELECT gemini_title, gemini_body, gemini_status FROM generated_news WHERE article_id = ?",
        ("legacy-001",),
    )
    row = cur.fetchone()
    assert row["gemini_title"] is None
    assert row["gemini_body"] is None
    assert row["gemini_status"] is None
