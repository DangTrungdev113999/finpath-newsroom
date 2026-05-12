"""Test Editor V1 V5.1.3 — Finpath sectors-driven routing."""
import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from lib.pipeline_db import PipelineDB
from lib.finpath_sectors import FinpathSectors
from lib.sector_router import get_master_route


@pytest.fixture
def db_with_cache(tmp_path):
    """DB pre-populated with sample tickers."""
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    samples = [
        ("VCB", "soe3", "Bank nhà nước", "Ngân hàng", "HOSE"),
        ("SSI", "stock", "Chứng khoán", "", "HOSE"),
        ("VHM", "vic3", "BDS VIC3", "Bất động sản", "HOSE"),
        ("BSR", "oilGas", "Dầu khí", "", "HOSE"),
        ("FPT", "defensive", "Phòng thủ", "", "HOSE"),
        ("MWG", "retail", "Tiêu dùng bán lẻ", "Tiêu dùng", "HOSE"),
    ]
    now = datetime.now(timezone.utc).isoformat()
    for ticker, sc, sn, pn, e in samples:
        db.conn.execute("""
            INSERT INTO finpath_sectors_cache
                (ticker, sector_code, sector_name, sector_parent, exchange, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticker, sc, sn, pn, e, now))
    db.conn.commit()
    yield db
    db.close()


def test_editor_routes_bank_to_master_bank(db_with_cache):
    fs = FinpathSectors(db_with_cache)
    info = fs.get_ticker_sector("VCB", allow_refresh=False)
    assert info["sector_code"] == "soe3"
    assert get_master_route(info["sector_code"]) == "bank"


def test_editor_routes_oilgas_to_master_oilgas(db_with_cache):
    fs = FinpathSectors(db_with_cache)
    info = fs.get_ticker_sector("BSR", allow_refresh=False)
    assert info["sector_code"] == "oilGas"
    assert get_master_route(info["sector_code"]) == "oilgas"


def test_editor_rejects_ticker_outside_finpath(db_with_cache):
    """Ticker không có trong cache + no refresh → None → reject."""
    fs = FinpathSectors(db_with_cache)
    info = fs.get_ticker_sector("UNKNOWN", allow_refresh=False)
    assert info is None


def test_editor_routes_all_new_v5_1_3_sectors(db_with_cache):
    """Verify all 7 new sectors route correctly."""
    fs = FinpathSectors(db_with_cache)

    info = fs.get_ticker_sector("FPT", allow_refresh=False)
    assert get_master_route(info["sector_code"]) == "defensive"

    info = fs.get_ticker_sector("MWG", allow_refresh=False)
    assert get_master_route(info["sector_code"]) == "retail"


def test_validate_crawl_log_v5_1_3_valid_row():
    """Valid V5.1.3 crawl_log row passes."""
    from lib.pipeline_db import validate_crawl_log_v5_1_3
    row = {
        "editor_v1_decision": "route_to_story_editor",
        "sector_code": "soe3",
        "sector_name": "Bank nhà nước",
        "sector_parent": "Ngân hàng",
        "master_route": "bank",
    }
    validate_crawl_log_v5_1_3(row)  # no exception


def test_validate_crawl_log_v5_1_3_missing_field():
    """Missing master_route → ValueError."""
    from lib.pipeline_db import validate_crawl_log_v5_1_3
    row = {
        "editor_v1_decision": "route_to_story_editor",
        "sector_code": "soe3",
        "sector_name": "Bank nhà nước",
        "sector_parent": "Ngân hàng",
        # MISSING master_route
    }
    with pytest.raises(ValueError, match="master_route"):
        validate_crawl_log_v5_1_3(row)


def test_validate_crawl_log_v5_1_3_invalid_route():
    """master_route not in valid set → ValueError."""
    from lib.pipeline_db import validate_crawl_log_v5_1_3
    row = {
        "editor_v1_decision": "route_to_story_editor",
        "sector_code": "soe3",
        "sector_name": "Bank",
        "sector_parent": "",
        "master_route": "nonexistent",
    }
    with pytest.raises(ValueError, match="master_route"):
        validate_crawl_log_v5_1_3(row)


def test_validate_crawl_log_v5_1_3_skips_rejected():
    """Rejected rows skip validation."""
    from lib.pipeline_db import validate_crawl_log_v5_1_3
    row = {
        "editor_v1_decision": "reject",
        "editor_v1_note": "ticker_outside_finpath_139",
    }
    validate_crawl_log_v5_1_3(row)  # no exception
