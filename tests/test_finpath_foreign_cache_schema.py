"""Test finpath_foreign_cache table schema."""
import pytest
from lib.pipeline_db import PipelineDB


def test_finpath_foreign_cache_table_exists(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    cur = db.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='finpath_foreign_cache'"
    )
    assert cur.fetchone() is not None
    db.close()


def test_finpath_foreign_cache_columns(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    cur = db.conn.execute("PRAGMA table_info(finpath_foreign_cache)")
    columns = {row["name"] for row in cur.fetchall()}
    expected = {"cache_key", "endpoint", "payload", "fetched_at", "ttl_seconds"}
    assert expected.issubset(columns)
    db.close()


def test_finpath_foreign_cache_primary_key(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    cur = db.conn.execute("PRAGMA table_info(finpath_foreign_cache)")
    pk = [row["name"] for row in cur.fetchall() if row["pk"] > 0]
    assert pk == ["cache_key"]
    db.close()
