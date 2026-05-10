"""Tests for lib.pipeline_db — SQLite ops on crawl_log + generated_news."""
import json
import pytest
from pathlib import Path

from lib.pipeline_db import PipelineDB, parse_task_usage


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


# ---------------------------------------------------------------------------
# Phase F T10 — per-step observability (log_pipeline_step + parse_task_usage)
# ---------------------------------------------------------------------------


def _seed_article(db, article_id: str = "art-obs", pipeline_log: str | None = None):
    """Helper: insert a minimal crawl_log + generated_news row for obs tests."""
    db.insert_crawl_row({
        "row_id": f"row-{article_id}",
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": f"https://example.com/{article_id}",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    payload = {
        "article_id": article_id,
        "row_id": f"row-{article_id}",
        "ticker": "VCB",
        "sector": "Bank",
        "title": "Article",
        "body": "Body...",
        "word_count": 300,
        "accepted_hypothesis": 1,
        "status": "draft",
    }
    if pipeline_log is not None:
        payload["pipeline_log"] = pipeline_log
    db.insert_generated_news(payload)


def test_log_pipeline_step_creates_entry(db):
    """Empty pipeline_log → log_pipeline_step writes step_1 entry."""
    _seed_article(db, "art-1")
    db.log_pipeline_step("art-1", "step_1_crawler", {
        "model": "sonnet",
        "duration_ms": 1234,
        "tokens": None,
        "candidates_count": 10,
    })
    row = db.conn.execute(
        "SELECT pipeline_log FROM generated_news WHERE article_id = 'art-1'"
    ).fetchone()
    log = json.loads(row["pipeline_log"])
    assert "step_1_crawler" in log
    assert log["step_1_crawler"]["model"] == "sonnet"
    assert log["step_1_crawler"]["duration_ms"] == 1234
    assert log["step_1_crawler"]["tokens"] is None
    assert log["step_1_crawler"]["candidates_count"] == 10


def test_log_pipeline_step_merges_existing(db):
    """log_pipeline_step adds step_4 to existing pipeline_log with step_3 → both present."""
    existing = json.dumps({"step_3_story_editor": {"model": "opus", "duration_ms": 5000, "tokens": 12000}})
    _seed_article(db, "art-2", pipeline_log=existing)
    db.log_pipeline_step("art-2", "step_4_master", {
        "model": "opus",
        "duration_ms": 8000,
        "tokens": 25000,
    })
    row = db.conn.execute(
        "SELECT pipeline_log FROM generated_news WHERE article_id = 'art-2'"
    ).fetchone()
    log = json.loads(row["pipeline_log"])
    assert "step_3_story_editor" in log
    assert "step_4_master" in log
    assert log["step_3_story_editor"]["tokens"] == 12000
    assert log["step_4_master"]["tokens"] == 25000


def test_log_pipeline_step_overwrites_same_key(db):
    """Calling log_pipeline_step twice with same step_key → only latest payload."""
    _seed_article(db, "art-3")
    db.log_pipeline_step("art-3", "step_4_master", {"duration_ms": 1000, "tokens": 5000})
    db.log_pipeline_step("art-3", "step_4_master", {"duration_ms": 2000, "tokens": 10000})
    row = db.conn.execute(
        "SELECT pipeline_log FROM generated_news WHERE article_id = 'art-3'"
    ).fetchone()
    log = json.loads(row["pipeline_log"])
    assert log["step_4_master"]["duration_ms"] == 2000
    assert log["step_4_master"]["tokens"] == 10000
    # Only one entry for step_4_master
    assert list(log.keys()) == ["step_4_master"]


def test_log_pipeline_step_missing_article_id_noop(db):
    """Non-existent article_id → no error, no insert."""
    # Should not raise
    db.log_pipeline_step("does-not-exist", "step_1_crawler", {"model": "sonnet"})
    # Verify no row was inserted
    row = db.conn.execute(
        "SELECT * FROM generated_news WHERE article_id = 'does-not-exist'"
    ).fetchone()
    assert row is None


def test_parse_task_usage_present():
    """Input with <usage>total_tokens: N ...</usage> → returns N."""
    text = "Result text\n<usage>total_tokens: 5000 tool_uses: 10</usage>"
    assert parse_task_usage(text) == 5000


def test_parse_task_usage_absent():
    """Input without <usage> block → None."""
    assert parse_task_usage("No usage block here") is None


def test_parse_task_usage_empty():
    """Empty string or None → None."""
    assert parse_task_usage("") is None
    assert parse_task_usage(None) is None


def test_parse_task_usage_malformed():
    """Malformed <usage> block (no total_tokens) → None, no exception."""
    assert parse_task_usage("<usage>broken format</usage>") is None
    assert parse_task_usage("<usage>total_tokens: not_a_number</usage>") is None
    assert parse_task_usage("<usage>") is None


# ---------------------------------------------------------------------------
# Phase G T1 — WAL mode + concurrent multi-pipeline writes
# ---------------------------------------------------------------------------


def test_wal_mode_concurrent_writes_succeed(tmp_path):
    """3 subprocess writers concurrent writes via WAL mode → all succeed.

    Phase G T1 — verifies WAL mode permits concurrent multi-pipeline writes
    without 'database is locked' errors. Subprocess based (not threading)
    because real /tin-batch spawns separate Claude Code workers.
    """
    import subprocess
    from pathlib import Path

    # Setup: real disk DB initialized with schema (WAL doesn't work :memory:)
    db_path = tmp_path / "concurrent.db"
    schema_path = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db = PipelineDB(str(db_path))
    db.init_schema(schema_path)
    db.close()

    helper = Path(__file__).parent / "helpers" / "concurrent_writer.py"
    batch_id = "CONCURRENT-TEST-001"

    # Spawn 3 concurrent writers, each inserts 1 row with unique source_url
    procs = [
        subprocess.Popen(
            ["uv", "run", "python", str(helper), str(db_path), batch_id, f"https://test.example/{i}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        for i in range(3)
    ]
    results = [p.wait(timeout=60) for p in procs]
    assert all(rc == 0 for rc in results), \
        f"Subprocess failed: {[(p.returncode, p.stderr.read().decode()) for p in procs]}"

    # Verify all 3 rows persisted
    db = PipelineDB(str(db_path))
    rows = db.query_by_funnel_batch(batch_id)
    db.close()
    assert len(rows) == 3, f"Expected 3 rows, got {len(rows)}"


# ---------------------------------------------------------------------------
# Phase G T11 — Telegram publish idempotency tracking
# ---------------------------------------------------------------------------


def test_generated_news_has_telegram_pushed_at_column(db):
    """Phase G T11 — schema includes telegram_pushed_at column."""
    cur = db.conn.execute("PRAGMA table_info(generated_news)")
    cols = {row["name"] for row in cur.fetchall()}
    assert "telegram_pushed_at" in cols, f"Missing column. Found: {sorted(cols)}"


def test_telegram_pushed_at_default_null(db):
    """Phase G T11 — telegram_pushed_at defaults to NULL on new article."""
    db.insert_crawl_row({
        "row_id": "r1",
        "funnel_batch_id": "b1",
        "source_name": "test",
        "source_url": "https://t/1",
        "title": "t",
        "ticker": "TST",
        "raw_content": "c",
        "crawled_at": "2026-05-10T00:00:00Z",
    })
    db.insert_generated_news({
        "article_id": "a1",
        "row_id": "r1",
        "ticker": "TST",
        "sector": "Bank",
        "title": "Test",
        "body": "body",
        "word_count": 100,
        "key_view": "trung lập",
        "insight_final": "i",
        "accepted_hypothesis": 1,
        "status": "draft",
        "pipeline_version": "V4.0",
    })
    cur = db.conn.execute(
        "SELECT telegram_pushed_at FROM generated_news WHERE article_id = ?",
        ("a1",),
    )
    row = cur.fetchone()
    assert row["telegram_pushed_at"] is None
