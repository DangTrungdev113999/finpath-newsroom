"""Verify Master agents can call foreign flow API via lib.finpath_api.

Run only with explicit -m integration marker (hits live Finpath API):
    uv run pytest tests/integration/test_master_uses_foreign_flow.py -v -m integration
"""
import pytest
from lib.pipeline_db import PipelineDB
from lib.finpath_api import FinpathAPI


@pytest.mark.integration
def test_master_can_call_get_foreign_rooms(tmp_path):
    """Master agent imports FinpathAPI and call get_foreign_rooms — no crash."""
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)
    rooms = api.get_foreign_rooms()
    assert len(rooms) > 0
    db.close()


@pytest.mark.integration
def test_master_can_call_roomstatistics_with_period(tmp_path):
    """Master calls roomstatistics with valid periods."""
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)
    for period in ["1D", "1W", "1M"]:
        stats = api.get_foreign_roomstatistics("VHM", period=period)
        assert stats is not None
    db.close()


@pytest.mark.integration
def test_master_uses_cache_efficiently(tmp_path):
    """3 sequential calls to same (ticker, period) → only 1 cache row."""
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)

    api.get_foreign_roomstatistics("VHM", period="1W")
    api.get_foreign_roomstatistics("VHM", period="1W")
    api.get_foreign_roomstatistics("VHM", period="1W")

    cur = db.conn.execute(
        "SELECT COUNT(*) as cnt FROM finpath_foreign_cache WHERE cache_key = 'roomstat:VHM:1W'"
    )
    assert cur.fetchone()["cnt"] == 1
    db.close()
