"""Tests for refresh_sector_cache CLI."""
from unittest.mock import patch, MagicMock
import pytest
from lib.pipeline_db import PipelineDB
from lib.refresh_sector_cache import main


@pytest.fixture
def mock_api_response():
    return {
        "data": {
            "sectors": [
                {
                    "k": "oilGas", "n": "Dầu khí", "pn": "",
                    "s": [{"c": "BSR", "e": "HOSE"}]
                }
            ]
        }
    }


def test_refresh_populates_cache(tmp_path, mock_api_response, capsys):
    db_path = tmp_path / "test.db"
    PipelineDB(str(db_path)).close()

    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = main(db_path=str(db_path), force=False)

    assert result == 0
    captured = capsys.readouterr()
    assert "Cached" in captured.out
    assert "BSR" in captured.out or "1 tickers" in captured.out


def test_refresh_force_clears_stale(tmp_path, mock_api_response):
    """--force flag clears all cache before refresh."""
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    db.conn.execute("""
        INSERT INTO finpath_sectors_cache (ticker, sector_code, sector_name, sector_parent, exchange, fetched_at)
        VALUES ('OLDSTOCK', 'oldcode', 'Old', '', 'HOSE', '2020-01-01T00:00:00+00:00')
    """)
    db.conn.commit()
    db.close()

    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        main(db_path=str(db_path), force=True)

    db = PipelineDB(str(db_path))
    cur = db.conn.execute("SELECT COUNT(*) as cnt FROM finpath_sectors_cache WHERE ticker = 'OLDSTOCK'")
    assert cur.fetchone()["cnt"] == 0
    db.close()
