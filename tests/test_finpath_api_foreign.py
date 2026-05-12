"""Test FinpathAPI foreign flow methods."""
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
import pytest
from lib.pipeline_db import PipelineDB
from lib.finpath_api import FinpathAPI


@pytest.fixture
def db(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    yield db
    db.close()


@pytest.fixture
def api(db):
    return FinpathAPI(db=db)


@pytest.fixture
def mock_rooms_response():
    return {
        "data": {
            "rooms": [
                {
                    "c": "VHM", "sn": "Vinhomes", "e": "HOSE", "ste": "S",
                    "td": "12/05/2026", "p": 50500,
                    "dnva": -85780000000, "dnv": -200000,
                    "wnva": -340000000000, "mnva": -1200000000000
                },
                {
                    "c": "FPT", "sn": "FPT", "e": "HOSE", "ste": "S",
                    "td": "12/05/2026", "p": 80000,
                    "dnva": 120000000000, "dnv": 1500000,
                    "wnva": 250000000000
                }
            ]
        }
    }


def test_get_foreign_rooms_cache_miss_calls_api(api, mock_rooms_response):
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_rooms_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        rooms = api.get_foreign_rooms()

    assert len(rooms) == 2
    assert rooms[0]["c"] == "VHM"
    assert rooms[0]["dnva"] == -85780000000
    mock_get.assert_called_once()


def test_get_foreign_rooms_cache_hit(api, mock_rooms_response):
    """Second call within TTL = no API call."""
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_rooms_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api.get_foreign_rooms()  # first: cache miss → API
        api.get_foreign_rooms()  # second: cache hit → no API

    mock_get.assert_called_once()


def test_get_foreign_roomstatistics_validates_period(api):
    """Invalid period raises ValueError."""
    with pytest.raises(ValueError, match="period"):
        api.get_foreign_roomstatistics("VHM", period="INVALID")


def test_get_foreign_roomstatistics_valid_periods(api):
    """All 6 valid periods accepted: 1D/1W/1M/3M/6M/1Y."""
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        for period in ["1D", "1W", "1M", "3M", "6M", "1Y"]:
            api.get_foreign_roomstatistics("VHM", period=period)

    assert mock_get.call_count == 6  # cached per (ticker, period) so each is a separate miss


def test_get_foreign_roombars_cache_key(api, db):
    """roombars cache_key = 'roombars:{ticker}'."""
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"bars": []}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api.get_foreign_roombars("VHM")

    cur = db.conn.execute(
        "SELECT cache_key FROM finpath_foreign_cache WHERE cache_key = 'roombars:VHM'"
    )
    assert cur.fetchone() is not None


def test_stale_cache_fallback_api_down(api, db, mock_rooms_response):
    """API down + cache stale → return stale, log warning."""
    stale_time = (datetime.now(timezone.utc) - timedelta(seconds=1000)).isoformat()
    db.conn.execute(
        """
        INSERT INTO finpath_foreign_cache (cache_key, endpoint, payload, fetched_at, ttl_seconds)
        VALUES ('rooms', '/v2/rooms', ?, ?, 900)
        """,
        (json.dumps(mock_rooms_response), stale_time),
    )
    db.conn.commit()

    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("API down")
        rooms = api.get_foreign_rooms()

    assert len(rooms) == 2  # returned stale
    assert rooms[0]["c"] == "VHM"


def test_empty_cache_api_fail_raises(api, db):
    """No cache + API down → RuntimeError."""
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("API down")
        with pytest.raises(RuntimeError, match="Finpath API"):
            api.get_foreign_rooms()


def test_rooms_cache_ttl_is_15_min(api, db, mock_rooms_response):
    """/v2/rooms cache row has ttl_seconds=900."""
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_rooms_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api.get_foreign_rooms()

    cur = db.conn.execute("SELECT ttl_seconds FROM finpath_foreign_cache WHERE cache_key = 'rooms'")
    row = cur.fetchone()
    assert row["ttl_seconds"] == 900
