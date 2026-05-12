"""Tests for Bank + CK universe expansion (spec 2026-05-11)."""
import sys
from pathlib import Path

# Add skill scripts to path for import
SCRIPTS_DIR = Path(__file__).parent.parent / ".claude" / "skills" / "finpath-newsroom-editor"
sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.routing import BANK_UNIVERSE, CK_UNIVERSE, BDS_UNIVERSE, FULL_UNIVERSE, get_sector
from scripts.ticker_detection import detect_combined, COMPANY_NAME_TO_TICKER, SHORT_FORM_TO_TICKER


# === Universe size assertions ===

def test_bank_universe_27_tickers():
    assert len(BANK_UNIVERSE) == 27


def test_ck_universe_30_tickers():
    assert len(CK_UNIVERSE) == 30


def test_bds_universe_unchanged():
    assert BDS_UNIVERSE == ["VHM", "NVL", "KDH", "DXG"]


def test_full_universe_71_tickers():
    # 61 (Bank 27 + CK 30 + BĐS 4) + 10 (Oil-Gas) = 71 post-merge with remote.
    # V5.1.3 runtime uses Finpath sectors cache (~139 mã) via lib/sector_router.py;
    # FULL_UNIVERSE preserved for migration audit reference only.
    assert len(FULL_UNIVERSE) == 71


# === Bank universe membership ===

def test_bank_hose_tickers_present():
    expected = ["VCB", "CTG", "BID", "TCB", "MBB", "ACB", "VPB", "HDB",
                "STB", "SHB", "EIB", "TPB", "MSB", "LPB", "OCB", "VIB"]
    for t in expected:
        assert t in BANK_UNIVERSE, f"Missing HOSE bank: {t}"


def test_bank_hnx_tickers_present():
    for t in ["NAB", "BAB", "NVB", "SGB"]:
        assert t in BANK_UNIVERSE, f"Missing HNX bank: {t}"


def test_bank_upcom_tickers_present():
    for t in ["VAB", "BVB", "ABB", "KLB", "VBB", "PGB", "HDF"]:
        assert t in BANK_UNIVERSE, f"Missing UPCOM bank: {t}"


# === CK universe membership ===

def test_ck_hose_tickers_present():
    for t in ["SSI", "VND", "HCM", "VCI", "VIX"]:
        assert t in CK_UNIVERSE, f"Missing HOSE CK: {t}"


def test_ck_hnx_tickers_present():
    expected = ["SHS", "MBS", "BVS", "BSI", "AGR", "CTS", "APG", "EVS",
                "IVS", "PSI", "TVS", "WSS", "ORS", "VFS", "TCI"]
    for t in expected:
        assert t in CK_UNIVERSE, f"Missing HNX CK: {t}"


def test_ck_upcom_tickers_present():
    expected = ["DSC", "FTS", "CSI", "SBS", "PHS", "ART", "APS", "BMS", "AAS", "VTS"]
    for t in expected:
        assert t in CK_UNIVERSE, f"Missing UPCOM CK: {t}"


# === get_sector for all expanded tickers ===

def test_get_sector_all_bank():
    for ticker in BANK_UNIVERSE:
        assert get_sector(ticker) == "Bank", f"{ticker} should map to Bank"


def test_get_sector_all_ck():
    for ticker in CK_UNIVERSE:
        assert get_sector(ticker) == "CK", f"{ticker} should map to CK"


def test_get_sector_unknown_ticker_returns_none():
    assert get_sector("XYZ") is None
    assert get_sector("ZZZ") is None


# === Alias detection — new Bank companies ===

def test_alias_sacombank_detects_stb():
    assert "STB" in detect_combined("Sacombank công bố lợi nhuận quý 1")


def test_alias_eximbank_detects_eib():
    assert "EIB" in detect_combined("Eximbank tăng vốn điều lệ năm 2026")


def test_alias_hdbank_detects_hdb():
    assert "HDB" in detect_combined("HDBank phát hành cổ phiếu thưởng")


def test_alias_tpbank_detects_tpb():
    assert "TPB" in detect_combined("TPBank công bố BCTC quý 2")


def test_alias_lpbank_detects_lpb():
    assert "LPB" in detect_combined("LPBank đổi tên từ LienVietPostBank")


def test_alias_maritime_bank_detects_msb():
    assert "MSB" in detect_combined("Maritime Bank tăng tín dụng 12%")


def test_alias_nam_a_bank_detects_nab():
    assert "NAB" in detect_combined("Nam Á Bank niêm yết HNX 2024")


# === Alias detection — new CK companies ===

def test_alias_fpts_detects_fts():
    assert "FTS" in detect_combined("FPTS báo cáo doanh thu môi giới")


def test_alias_mbs_detects():
    assert "MBS" in detect_combined("MB Securities tăng vốn cho vay ký quỹ")


def test_alias_bsi_detects():
    assert "BSI" in detect_combined("BIDV Securities công bố lợi nhuận quý 1")


def test_alias_agriseco_detects_agr():
    assert "AGR" in detect_combined("Agriseco mở rộng thị phần môi giới")


def test_alias_petrosetco_detects_psi():
    assert "PSI" in detect_combined("Petrosetco công bố doanh thu tự doanh")


# === Pass 2 short-form uppercase regex ===

def test_short_form_regex_covers_all_universe():
    """SHORT_FORM_TO_TICKER must cover all 57 new tickers + 4 BĐS."""
    for ticker in BANK_UNIVERSE + CK_UNIVERSE + BDS_UNIVERSE:
        assert ticker in SHORT_FORM_TO_TICKER, f"Missing SHORT_FORM entry: {ticker}"


def test_short_form_detects_raw_uppercase_stb():
    """STB alone (no Sacombank in text) should still detect."""
    assert "STB" in detect_combined("STB công bố lợi nhuận Q2/2026")


def test_short_form_detects_raw_uppercase_eib():
    assert "EIB" in detect_combined("EIB tăng vốn lên 25 nghìn tỷ")


# === No regression — existing MVP detection still works ===

def test_existing_mvp_bank_detection():
    """VCB/TCB/MBB detection still works after expansion."""
    text = "Vietcombank công bố lợi nhuận quý 1, Techcombank cùng giảm NIM."
    detected = detect_combined(text)
    assert "VCB" in detected
    assert "TCB" in detected


def test_existing_mvp_ck_detection():
    text = "SSI và VNDirect cạnh tranh thị phần môi giới HOSE."
    detected = detect_combined(text)
    assert "SSI" in detected
    assert "VND" in detected
