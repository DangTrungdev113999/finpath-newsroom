"""Test finpath_sectors_cache table creation + columns."""
import pytest
from lib.pipeline_db import PipelineDB


def test_finpath_sectors_cache_table_exists(tmp_path):
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    cur = db.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='finpath_sectors_cache'"
    )
    assert cur.fetchone() is not None, "finpath_sectors_cache table should exist after PipelineDB init"
    db.close()


def test_finpath_sectors_cache_required_columns(tmp_path):
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    cur = db.conn.execute("PRAGMA table_info(finpath_sectors_cache)")
    columns = {row["name"]: row["type"] for row in cur.fetchall()}
    assert columns["ticker"] == "TEXT"
    assert columns["sector_code"] == "TEXT"
    assert columns["sector_name"] == "TEXT"
    assert columns["sector_parent"] == "TEXT"
    assert columns["exchange"] == "TEXT"
    assert columns["fetched_at"] == "TIMESTAMP"
    db.close()


def test_finpath_sectors_cache_primary_key_ticker(tmp_path):
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    cur = db.conn.execute("PRAGMA table_info(finpath_sectors_cache)")
    pk_columns = [row["name"] for row in cur.fetchall() if row["pk"] > 0]
    assert pk_columns == ["ticker"], "ticker should be primary key"
    db.close()
