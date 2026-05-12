"""Tests for lib/finpath_sectors.py — FinpathSectors client."""
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
import pytest
from lib.pipeline_db import PipelineDB
from lib.finpath_sectors import FinpathSectors


@pytest.fixture
def db(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    yield db
    db.close()


@pytest.fixture
def mock_api_response():
    """Sample 2-sector Finpath API response."""
    return {
        "data": {
            "sectors": [
                {
                    "k": "oilGas",
                    "c": "oilGas",
                    "n": "Dầu khí",
                    "pk": "",
                    "pc": "",
                    "pn": "",
                    "s": [
                        {"c": "BSR", "pe": 12.5, "pb": 1.8, "roa": 8.5, "roe": 18.2, "e": "HOSE", "eps": 1200, "mc": 100000000000},
                        {"c": "PVS", "pe": 14.0, "pb": 2.0, "roa": 9.0, "roe": 19.0, "e": "HNX", "eps": 1500, "mc": 80000000000},
                    ]
                },
                {
                    "k": "bank",
                    "c": "bank",
                    "n": "Ngân hàng",
                    "s": []
                }
            ]
        }
    }


def test_get_ticker_sector_cache_miss_triggers_refresh(db, mock_api_response):
    """First lookup with empty cache: should call API + populate cache."""
    fs = FinpathSectors(db)
    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fs.get_ticker_sector("BSR")

    assert result is not None
    assert result["sector_code"] == "oilGas"
    assert result["sector_name"] == "Dầu khí"
    assert result["sector_parent"] == ""
    assert result["exchange"] == "HOSE"
    mock_get.assert_called_once()


def test_get_ticker_sector_cache_hit_no_api_call(db, mock_api_response):
    """Fresh cache: no API call."""
    fs = FinpathSectors(db)
    db.conn.execute("""
        INSERT INTO finpath_sectors_cache (ticker, sector_code, sector_name, sector_parent, exchange, fetched_at)
        VALUES ('VHM', 'vic3', 'BDS VIC3', 'Bất động sản', 'HOSE', ?)
    """, (datetime.now(timezone.utc).isoformat(),))
    db.conn.commit()

    with patch("lib.finpath_sectors.requests.get") as mock_get:
        result = fs.get_ticker_sector("VHM")

    assert result["sector_code"] == "vic3"
    mock_get.assert_not_called()


def test_skip_wrapper_sectors(db, mock_api_response):
    """Wrapper sectors (s=[]) should NOT pollute cache."""
    fs = FinpathSectors(db)
    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        fs.refresh_cache()

    cur = db.conn.execute("SELECT COUNT(*) as cnt FROM finpath_sectors_cache WHERE sector_code = 'bank'")
    assert cur.fetchone()["cnt"] == 0
    cur = db.conn.execute("SELECT COUNT(*) as cnt FROM finpath_sectors_cache WHERE sector_code = 'oilGas'")
    assert cur.fetchone()["cnt"] == 2


def test_get_ticker_sector_unknown_returns_none(db, mock_api_response):
    """Ticker not in API response → None after refresh attempt."""
    fs = FinpathSectors(db)
    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fs.get_ticker_sector("NONEXIST")

    assert result is None


def test_stale_cache_graceful_degradation(db, mock_api_response):
    """API down + cache stale: return stale + warning, not None."""
    fs = FinpathSectors(db)
    stale_date = (datetime.now(timezone.utc) - timedelta(days=366)).isoformat()
    db.conn.execute("""
        INSERT INTO finpath_sectors_cache (ticker, sector_code, sector_name, sector_parent, exchange, fetched_at)
        VALUES ('STALE', 'oilGas', 'Dầu khí', '', 'HOSE', ?)
    """, (stale_date,))
    db.conn.commit()

    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("API down")
        result = fs.get_ticker_sector("STALE")

    assert result is not None
    assert result["sector_code"] == "oilGas"
