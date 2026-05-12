"""Tests for lib/sector_router.py."""
import pytest
from lib.sector_router import get_master_route, MasterRouteError


def test_get_master_route_bank_sector():
    assert get_master_route("private7") == "bank"
    assert get_master_route("soe3") == "bank"
    assert get_master_route("smallLegacy") == "bank"


def test_get_master_route_ck_sector():
    assert get_master_route("stock") == "ck"


def test_get_master_route_bds_subsectors():
    assert get_master_route("materialContractor") == "bds"
    assert get_master_route("vic3") == "bds"
    assert get_master_route("industrial") == "bds"
    assert get_master_route("exvic") == "bds"


def test_get_master_route_new_v5_1_3_sectors():
    assert get_master_route("oilGas") == "oilgas"
    assert get_master_route("logistics") == "logistics"
    assert get_master_route("fb") == "fb"
    assert get_master_route("apparel") == "apparel"
    assert get_master_route("retail") == "retail"
    assert get_master_route("seafood") == "seafood"
    assert get_master_route("defensive") == "defensive"


def test_get_master_route_unknown_sector_raises():
    """Fail-loud when sector_code not in YAML."""
    with pytest.raises(MasterRouteError) as exc:
        get_master_route("nonexistent_sector")
    assert "nonexistent_sector" in str(exc.value)
    assert "sector_routing.yaml" in str(exc.value)
