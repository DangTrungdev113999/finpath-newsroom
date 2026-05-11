"""Tests for finpath-newsroom-editor ticker_detection — covers Bug A fix.

Module lives at `.claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py`
(không phải `lib/`), nên prepend sys.path để import được.

Bug A: Editor V1 missed "MB" alone (2-char) trong tin "MB chia cổ tức..." vì
TICKER_PATTERN regex chỉ bắt 3-char uppercase. Pass 2 uppercase short-form fix
adds `\\b(MB|VCB|...)\\b` case-sensitive trên raw text.
"""
import sys
from pathlib import Path

import pytest

# Prepend scripts dir to sys.path để import ticker_detection.py
SCRIPTS_DIR = (
    Path(__file__).parent.parent
    / ".claude"
    / "skills"
    / "finpath-newsroom-editor"
    / "scripts"
)
sys.path.insert(0, str(SCRIPTS_DIR))

import ticker_detection  # noqa: E402
from ticker_detection import (  # noqa: E402
    COMPANY_NAME_TO_TICKER,
    SHORT_FORM_TO_TICKER,
    detect_combined,
    detect_short_form_uppercase,
    detect_via_company_name,
)


# ---------------------------------------------------------------------------
# Bug A fix — primary tests
# ---------------------------------------------------------------------------


def test_detect_mb_standalone():
    """MB alone (2-char) trong tin → MBB. Đây là bug chính."""
    text = "MB chia cổ tức 25%"
    assert detect_combined(text) == ["MBB"]


def test_detect_lowercase_false_positive_avoided():
    """Lowercase 'mb' trong 'miễn bàn'/'mb chi' KHÔNG được match.

    Đây là lý do KHÔNG thêm 'mb' lowercase vào COMPANY_NAME_TO_TICKER —
    sẽ trigger false positive với cụm tiếng Việt thông thường.
    """
    text = "miễn bàn về cổ phiếu"
    assert detect_combined(text) == []


def test_detect_multiple_tickers():
    """MB + VCB cùng xuất hiện → cả hai detected."""
    text = "MB và VCB cùng tăng vốn"
    assert sorted(detect_combined(text)) == ["MBB", "VCB"]


def test_detect_company_name_still_works():
    """Pass 1 (lowercase company name) vẫn hoạt động sau khi thêm Pass 2."""
    text = "Vietcombank công bố kết quả kinh doanh"
    assert detect_combined(text) == ["VCB"]


def test_detect_quan_doi():
    """'Ngân hàng Quân đội' → MBB qua alias mới."""
    text = "Ngân hàng Quân đội báo lãi quý 1"
    assert detect_combined(text) == ["MBB"]


def test_no_ticker_in_text():
    """Text không có ticker nào → empty list."""
    text = "Ngân hàng Nhà nước họp định kỳ tuần này"
    assert detect_combined(text) == []


# ---------------------------------------------------------------------------
# Pass 2 detection — direct unit tests
# ---------------------------------------------------------------------------


def test_pass2_uppercase_only():
    """detect_short_form_uppercase chỉ match uppercase, KHÔNG lowercase."""
    assert detect_short_form_uppercase("MB chia cổ tức") == ["MBB"]
    assert detect_short_form_uppercase("mb chi tiêu") == []


def test_pass2_word_boundary_with_punctuation():
    """\\b boundary handle dấu câu xung quanh ticker (MB., MB,, (MB))."""
    assert detect_short_form_uppercase("Cổ phiếu MB. tăng mạnh") == ["MBB"]
    assert detect_short_form_uppercase("MB, VCB tăng giá") == ["MBB", "VCB"]
    assert detect_short_form_uppercase("(MB) báo lãi") == ["MBB"]


def test_pass2_does_not_match_inside_word():
    """\\b boundary KHÔNG match khi ticker là substring của word dài hơn."""
    # "MBA" (Master of Business Admin) không được match như "MB"
    assert detect_short_form_uppercase("Bằng MBA quốc tế") == []
    # "VCBNews" hypothetical compound không match VCB
    assert detect_short_form_uppercase("VCBNews đăng tin") == []


def test_pass2_dedupe_preserves_order():
    """Nhiều mention cùng ticker → dedupe, giữ thứ tự xuất hiện đầu."""
    text = "MB tăng. VCB cũng tăng. MB lại giảm."
    assert detect_short_form_uppercase(text) == ["MBB", "VCB"]


def test_pass2_empty_text():
    """Empty text → empty list (no exception)."""
    assert detect_short_form_uppercase("") == []
    assert detect_short_form_uppercase(None) == []


# ---------------------------------------------------------------------------
# Combined detection — priority + dedup
# ---------------------------------------------------------------------------


def test_combined_dedup_across_passes():
    """VCB xuất hiện cả 3-char regex + Pass 2 + company name → 1 lần."""
    text = "VCB Vietcombank công bố"
    assert detect_combined(text) == ["VCB"]


def test_combined_mbb_3char_and_mb_2char_dedup():
    """MBB (3-char regex) + MB (Pass 2) → cả hai map về MBB, dedupe."""
    text = "MBB và MB cùng đề cập"
    # detect_tickers (3-char) bắt MBB, Pass 2 cũng bắt MBB từ "MBB" + MB→MBB.
    # Kết quả final: chỉ ["MBB"].
    assert detect_combined(text) == ["MBB"]


# ---------------------------------------------------------------------------
# Sanity / regression — alias table
# ---------------------------------------------------------------------------


def test_quan_doi_alias_present():
    """COMPANY_NAME_TO_TICKER có 'quân đội' → MBB."""
    assert COMPANY_NAME_TO_TICKER.get("quân đội") == "MBB"


def test_short_form_table_complete():
    """SHORT_FORM_TO_TICKER cover toàn bộ 61 mã universe (Bank 27 + CK 30 + BĐS 4)
    + legacy alias "MB" → MBB. Total 62 keys."""
    expected = {
        # Special legacy alias
        "MB",
        # Bank HOSE (16)
        "VCB", "CTG", "BID", "TCB", "MBB", "ACB", "VPB", "HDB",
        "STB", "SHB", "EIB", "TPB", "MSB", "LPB", "OCB", "VIB",
        # Bank HNX (4)
        "NAB", "BAB", "NVB", "SGB",
        # Bank UPCOM (7)
        "VAB", "BVB", "ABB", "KLB", "VBB", "PGB", "HDF",
        # CK HOSE (5)
        "SSI", "VND", "HCM", "VCI", "VIX",
        # CK HNX (15)
        "SHS", "MBS", "BVS", "BSI", "AGR", "CTS", "APG", "EVS",
        "IVS", "PSI", "TVS", "WSS", "ORS", "VFS", "TCI",
        # CK UPCOM (10)
        "DSC", "FTS", "CSI", "SBS", "PHS", "ART", "APS", "BMS", "AAS", "VTS",
        # BĐS (4)
        "VHM", "NVL", "KDH", "DXG",
    }
    assert set(SHORT_FORM_TO_TICKER.keys()) == expected


def test_no_lowercase_mb_in_company_dict():
    """KHÔNG có 'mb' lowercase trong dict — chống false positive 'miễn bàn'."""
    assert "mb" not in COMPANY_NAME_TO_TICKER


def test_company_name_helper_quan_doi():
    """detect_via_company_name (Pass 1) trực tiếp bắt 'quân đội' → MBB."""
    assert detect_via_company_name("Ngân hàng Quân đội báo lãi") == ["MBB"]
