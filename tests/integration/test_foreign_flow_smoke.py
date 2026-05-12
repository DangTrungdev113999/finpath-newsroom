"""Live API smoke tests for foreign flow endpoints.

Run only with explicit -m integration marker:
    uv run pytest tests/integration/test_foreign_flow_smoke.py -v -m integration
"""
import pytest
from lib.pipeline_db import PipelineDB
from lib.finpath_api import FinpathAPI


@pytest.mark.integration
def test_real_rooms_api_returns_data(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)
    rooms = api.get_foreign_rooms()
    assert len(rooms) > 1000, f"Expected ~1902 records, got {len(rooms)}"

    vhm = next((r for r in rooms if r["c"] == "VHM"), None)
    assert vhm is not None
    assert "dnva" in vhm
    assert "ste" in vhm
    db.close()


@pytest.mark.integration
def test_real_roomstatistics_vhm_1w(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)
    stats = api.get_foreign_roomstatistics("VHM", period="1W")
    assert stats is not None
    db.close()


@pytest.mark.integration
def test_real_roombars_vhm(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)
    bars = api.get_foreign_roombars("VHM")
    assert isinstance(bars, list)
    db.close()


@pytest.mark.integration
def test_cache_hit_second_call(tmp_path):
    """Second call within TTL → fetched_at unchanged."""
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)

    api.get_foreign_rooms()

    cur = db.conn.execute(
        "SELECT fetched_at FROM finpath_foreign_cache WHERE cache_key = 'rooms'"
    )
    first_fetched = cur.fetchone()["fetched_at"]

    api.get_foreign_rooms()

    cur = db.conn.execute(
        "SELECT fetched_at FROM finpath_foreign_cache WHERE cache_key = 'rooms'"
    )
    second_fetched = cur.fetchone()["fetched_at"]

    assert first_fetched == second_fetched, "Cache hit should not refresh fetched_at"
    db.close()
