"""Test crawl_log inserts carry session_id + trigger fields (Plan H Task 2).

Schema upgrade columns added by H-1 (PipelineDB._upgrade_crawl_log_schema):
session_id, trigger_type, trigger_args.

Tests follow the canonical fixture pattern from test_pipeline_db.py:
PipelineDB(...) + db.init_schema(schema_path).

Adaptation from plan example tests:
- Pass `row_id` explicitly (matches the PRIMARY KEY NOT NULL column in the
  real schema — current schema has TEXT row_id PK, NOT auto-increment INTEGER).
- Use real schema column names (`title`/`raw_content`/`published_time`)
  not the placeholder names from the plan example (`raw_title`/`raw_body`/
  `published_at`).
"""
import uuid
from pathlib import Path

import pytest

from lib.pipeline_db import PipelineDB


SCHEMA_PATH = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"


def _open_db(tmp_path) -> PipelineDB:
    """Construct PipelineDB + load canonical schema (matches existing fixture)."""
    db = PipelineDB(str(tmp_path / "test.db"))
    db.init_schema(SCHEMA_PATH)
    return db


def test_insert_crawl_row_with_session_fields(tmp_path):
    db = _open_db(tmp_path)
    row_id = str(uuid.uuid4())
    db.insert_crawl_row({
        "row_id": row_id,
        "ticker": "VHM",
        "source_name": "VnEconomy",
        "source_url": "https://example.com/vhm-1",
        "title": "VHM Q1",
        "raw_content": "...",
        "published_time": "2026-05-12",
        "crawled_at": "2026-05-12T14:30:00Z",
        "funnel_batch_id": "VHM-20260512-1430",
        "session_id": "abc-123",
        "trigger_type": "tin-hot",
        "trigger_args": "N=3",
    })
    cur = db.conn.execute(
        "SELECT session_id, trigger_type, trigger_args FROM crawl_log WHERE row_id = ?",
        (row_id,),
    )
    row = cur.fetchone()
    assert row["session_id"] == "abc-123"
    assert row["trigger_type"] == "tin-hot"
    assert row["trigger_args"] == "N=3"
    db.close()


def test_insert_crawl_row_session_fields_optional(tmp_path):
    """Legacy callers without session fields still work (nullable)."""
    db = _open_db(tmp_path)
    row_id = str(uuid.uuid4())
    db.insert_crawl_row({
        "row_id": row_id,
        "ticker": "VHM",
        "source_name": "VnEconomy",
        "source_url": "https://example.com/vhm-2",
        "title": "VHM Q1",
        "raw_content": "...",
        "published_time": "2026-05-12",
        "crawled_at": "2026-05-12T14:30:00Z",
        "funnel_batch_id": "VHM-20260512-1430",
    })
    cur = db.conn.execute(
        "SELECT session_id, trigger_type, trigger_args FROM crawl_log WHERE row_id = ?",
        (row_id,),
    )
    row = cur.fetchone()
    assert row["session_id"] is None
    assert row["trigger_type"] is None
    assert row["trigger_args"] is None
    db.close()
