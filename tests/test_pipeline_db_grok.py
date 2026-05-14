"""Tests for Grok DB columns + writer method (Phase A6)."""

from __future__ import annotations

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


GROK_COLUMNS = {
    "grok_title",
    "grok_body",
    "grok_word_count",
    "grok_model",
    "grok_generated_at",
    "grok_status",
    "grok_error",
}


def test_grok_columns_exist_after_init(db) -> None:
    cur = db.conn.execute("PRAGMA table_info(generated_news)")
    cols = {row["name"] for row in cur.fetchall()}
    assert GROK_COLUMNS.issubset(cols), f"missing: {GROK_COLUMNS - cols}"


def _seed_article(db, article_id: str = "test-001") -> None:
    db.conn.execute(
        "INSERT INTO crawl_log (row_id, funnel_batch_id, ticker, source_name, "
        "source_url, title, crawled_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("row-001", "batch-001", "ACB", "test", "http://x", "raw", "2026-05-14"),
    )
    db.conn.execute(
        "INSERT INTO generated_news (article_id, row_id, ticker, sector, title, body, "
        "accepted_hypothesis) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (article_id, "row-001", "ACB", "bank", "T", "B", 1),
    )
    db.conn.commit()


def test_update_grok_output_success(db) -> None:
    _seed_article(db)
    db.update_grok_output(
        article_id="test-001",
        status="success",
        title="Grok title",
        body="Grok body markdown",
        word_count=42,
        model="grok-4-latest",
        generated_at="2026-05-14T10:00:00Z",
        error=None,
    )
    cur = db.conn.execute(
        "SELECT grok_title, grok_body, grok_word_count, grok_model, "
        "grok_generated_at, grok_status, grok_error FROM generated_news "
        "WHERE article_id = ?",
        ("test-001",),
    )
    row = cur.fetchone()
    assert row["grok_title"] == "Grok title"
    assert row["grok_body"] == "Grok body markdown"
    assert row["grok_word_count"] == 42
    assert row["grok_model"] == "grok-4-latest"
    assert row["grok_generated_at"] == "2026-05-14T10:00:00Z"
    assert row["grok_status"] == "success"
    assert row["grok_error"] is None


def test_update_grok_output_skipped_failure(db) -> None:
    _seed_article(db)
    db.update_grok_output(
        article_id="test-001",
        status="skipped_failure",
        error="timeout after retry",
    )
    cur = db.conn.execute(
        "SELECT grok_status, grok_error, grok_body FROM generated_news WHERE article_id = ?",
        ("test-001",),
    )
    row = cur.fetchone()
    assert row["grok_status"] == "skipped_failure"
    assert row["grok_error"] == "timeout after retry"
    assert row["grok_body"] is None


def test_update_grok_output_invalid_status_raises(db) -> None:
    _seed_article(db)
    with pytest.raises(ValueError, match="grok_status"):
        db.update_grok_output(article_id="test-001", status="bogus")


def test_legacy_row_has_null_grok_columns(db) -> None:
    _seed_article(db, article_id="legacy-001")
    cur = db.conn.execute(
        "SELECT grok_title, grok_body, grok_status FROM generated_news WHERE article_id = ?",
        ("legacy-001",),
    )
    row = cur.fetchone()
    assert row["grok_title"] is None
    assert row["grok_body"] is None
    assert row["grok_status"] is None
