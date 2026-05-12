"""Test crawl_log schema extension for session grouping (Subsystem H V5.1.4).

Schema upgrade uses Option B: Python-side conditional ALTER TABLE via
PipelineDB._upgrade_crawl_log_schema(). Indexes also created in the same
helper (avoids ordering dependency with the .sql migration runner).

Tests follow the canonical fixture pattern from test_pipeline_db.py —
PipelineDB(...) + db.init_schema(schema_path). The upgrade helper runs
from both __init__ (idempotent re-open) AND init_schema (fresh bootstrap).
"""
from pathlib import Path

import pytest

from lib.pipeline_db import PipelineDB


SCHEMA_PATH = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"


def _open_db(tmp_path, name: str = "test.db") -> PipelineDB:
    """Construct PipelineDB + load canonical schema (matches existing fixture)."""
    db = PipelineDB(str(tmp_path / name))
    db.init_schema(SCHEMA_PATH)
    return db


def test_crawl_log_has_session_id_column(tmp_path):
    db = _open_db(tmp_path)
    cur = db.conn.execute("PRAGMA table_info(crawl_log)")
    columns = {row["name"] for row in cur.fetchall()}
    assert "session_id" in columns
    db.close()


def test_crawl_log_has_trigger_type_column(tmp_path):
    db = _open_db(tmp_path)
    cur = db.conn.execute("PRAGMA table_info(crawl_log)")
    columns = {row["name"] for row in cur.fetchall()}
    assert "trigger_type" in columns
    db.close()


def test_crawl_log_has_trigger_args_column(tmp_path):
    db = _open_db(tmp_path)
    cur = db.conn.execute("PRAGMA table_info(crawl_log)")
    columns = {row["name"] for row in cur.fetchall()}
    assert "trigger_args" in columns
    db.close()


def test_session_id_index_exists(tmp_path):
    db = _open_db(tmp_path)
    cur = db.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_crawl_log_session'"
    )
    assert cur.fetchone() is not None
    db.close()


def test_upgrade_is_idempotent_on_reopen(tmp_path):
    """Critical: second PipelineDB(...) on same file must not raise duplicate column error."""
    db_path = str(tmp_path / "test.db")
    db1 = PipelineDB(db_path)
    db1.init_schema(SCHEMA_PATH)
    db1.close()

    # Reopen — _upgrade_crawl_log_schema must be no-op for already-applied columns.
    db2 = PipelineDB(db_path)
    cur = db2.conn.execute("PRAGMA table_info(crawl_log)")
    columns = {row["name"] for row in cur.fetchall()}
    assert "session_id" in columns
    assert "trigger_type" in columns
    assert "trigger_args" in columns
    db2.close()
