"""Test build_pipeline_runs_manifest builder (Plan H Task 3 — Subsystem H V5.1.4).

Builds output/compare-feed/pipeline-runs.json from crawl_log + generated_news.

Adapts to REAL schema (not the plan template):
- crawl_log uses `title` / `raw_content` / `published_time` (not `raw_title`/etc.)
- `story_editor_note` is the only story-editor reject field (no separate
  `_label` / `_reason` columns).
- `sector_code` / `sector_name` / `hot_nhom` / `hot_rank` do NOT exist on
  crawl_log — those Plan H columns belong to later tasks. Builder leaves
  per-batch slots as None.
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path

import pytest

from lib.pipeline_db import PipelineDB
from lib.render_compare_feed import build_pipeline_runs_manifest


SCHEMA_PATH = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"


@pytest.fixture
def db(tmp_path):
    """Fresh PipelineDB on disk (Plan H needs WAL-friendly file path)."""
    db = PipelineDB(str(tmp_path / "test.db"))
    db.init_schema(str(SCHEMA_PATH))
    yield db
    db.close()


def _insert_row(db, **kwargs) -> str:
    """Insert a crawl_log row with REAL column names. Returns row_id."""
    defaults = {
        "row_id": str(uuid.uuid4()),
        "ticker": "VHM",
        "source_name": "VnEconomy",
        "source_url": f"https://example.com/{uuid.uuid4().hex[:8]}",
        "published_time": "2026-05-12",
        "crawled_at": "2026-05-12T14:30:00Z",
        "title": "title",
        "raw_content": "body",
        "funnel_batch_id": "VHM-20260512-1430",
        "session_id": "session-1",
        "trigger_type": "tin",
        "trigger_args": "VHM",
    }
    defaults.update(kwargs)
    # Drop None values so we leave columns at SQL default (relevant for
    # session_id=None — schema column added by H-1 migration is nullable).
    payload = {k: v for k, v in defaults.items() if v is not None}
    return db.insert_crawl_row(payload)


def test_empty_crawl_log_returns_empty_sessions(db, tmp_path):
    output_path = tmp_path / "pipeline-runs.json"
    count = build_pipeline_runs_manifest(db, output_path)
    assert count == 0
    payload = json.loads(output_path.read_text())
    assert payload["sessions"] == []


def test_single_session_single_batch(db, tmp_path):
    _insert_row(db)
    output_path = tmp_path / "pipeline-runs.json"
    count = build_pipeline_runs_manifest(db, output_path)
    assert count == 1
    payload = json.loads(output_path.read_text())
    assert len(payload["sessions"]) == 1
    session = payload["sessions"][0]
    assert session["session_id"] == "session-1"
    assert session["trigger_type"] == "tin"
    assert session["trigger_args"] == "VHM"
    assert len(session["batches"]) == 1
    batch = session["batches"][0]
    assert batch["ticker"] == "VHM"
    assert batch["funnel_batch_id"] == "VHM-20260512-1430"


def test_legacy_rows_without_session_id_skipped(db, tmp_path):
    """Q2 resolution: WHERE session_id IS NOT NULL filter."""
    _insert_row(db, session_id=None)
    _insert_row(db)  # default session-1
    output_path = tmp_path / "pipeline-runs.json"
    count = build_pipeline_runs_manifest(db, output_path)
    assert count == 1
    payload = json.loads(output_path.read_text())
    assert len(payload["sessions"]) == 1


def test_multi_ticker_session_groups_batches(db, tmp_path):
    """/tin-hot 3: 3 tickers × 2 rows each = 1 session, 3 batches."""
    for ticker, batch_id in [
        ("VHM", "VHM-20260512-1430"),
        ("FPT", "FPT-20260512-1430"),
        ("BSR", "BSR-20260512-1430"),
    ]:
        for _ in range(2):
            _insert_row(
                db,
                ticker=ticker,
                funnel_batch_id=batch_id,
                session_id="hot-session-1",
                trigger_type="tin-hot",
                trigger_args="N=3",
            )

    output_path = tmp_path / "pipeline-runs.json"
    count = build_pipeline_runs_manifest(db, output_path)
    assert count == 1
    payload = json.loads(output_path.read_text())
    session = payload["sessions"][0]
    assert session["trigger_type"] == "tin-hot"
    assert len(session["batches"]) == 3
    assert {b["ticker"] for b in session["batches"]} == {"VHM", "FPT", "BSR"}


def test_fetched_chosen_rejected_aggregate(db, tmp_path):
    """Session totals = sum of batch counts (5 rows, 2 chosen via generated_news)."""
    row_ids = []
    for _ in range(5):
        rid = _insert_row(db)
        row_ids.append(rid)
    # Mark 2 as chosen via generated_news (real schema columns)
    for i, rid in enumerate(row_ids[:2]):
        db.conn.execute(
            """INSERT INTO generated_news (
                article_id, row_id, title, body, public_slug, ticker, sector,
                accepted_hypothesis, pipeline_log, published_at
            ) VALUES (?, ?, 'title', 'body', ?, 'VHM', 'BĐS', 1, '{}', '2026-05-12T14:35:00Z')""",
            (f"art-{i}", rid, f"slug-{i}"),
        )
    db.conn.commit()

    output_path = tmp_path / "pipeline-runs.json"
    build_pipeline_runs_manifest(db, output_path)
    payload = json.loads(output_path.read_text())
    session = payload["sessions"][0]
    assert session["fetched_total"] == 5
    assert session["chosen_total"] == 2
    assert session["rejected_total"] == 3


def test_reject_classification_editor_v1(db, tmp_path):
    """Editor V1 reject → reject_agent='editor_v1', label = editor_v1_note."""
    rid = _insert_row(db)
    db.conn.execute(
        "UPDATE crawl_log SET editor_v1_decision = 'reject', "
        "editor_v1_note = 'ticker_undetected' WHERE row_id = ?",
        (rid,),
    )
    db.conn.commit()
    output_path = tmp_path / "pipeline-runs.json"
    build_pipeline_runs_manifest(db, output_path)
    payload = json.loads(output_path.read_text())
    rejected = payload["sessions"][0]["batches"][0]["funnel_detail"]["rejected"][0]
    assert rejected["reject_agent"] == "editor_v1"
    assert rejected["reject_label"] == "ticker_undetected"


def test_atomic_write_creates_temp_file_first(db, tmp_path):
    """Atomic rename pattern — temp file must not be left behind."""
    _insert_row(db)
    output_path = tmp_path / "pipeline-runs.json"
    build_pipeline_runs_manifest(db, output_path)
    assert output_path.exists()
    assert not (tmp_path / "pipeline-runs.json.tmp").exists()
