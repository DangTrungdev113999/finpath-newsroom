"""Tests for lib.quality_gates — 5 V3.6 quality gates."""
import pytest
from lib.quality_gates import (
    check_no_english_jargon,
    check_word_count,
    check_mechanism_count,
    check_can_de_y_narrative,
    check_no_metadata_leak,
    check_all,
)


def test_no_english_jargon_passes_clean_vietnamese():
    body = "Lợi nhuận trước thuế đạt **11.803 tỷ đồng**, tăng 9% so cùng kỳ. Nợ xấu 0,62%."
    result = check_no_english_jargon(body)
    assert result["pass"] is True


def test_no_english_jargon_fails_on_NPL():
    body = "NPL 1,05% tăng nhẹ."
    result = check_no_english_jargon(body)
    assert result["pass"] is False
    assert "npl" in result["reason"].lower()


def test_no_english_jargon_fails_on_momentum():
    body = "TCB có momentum mạnh."
    result = check_no_english_jargon(body)
    assert result["pass"] is False
    assert "momentum" in result["reason"].lower()


def test_no_english_jargon_allows_proper_nouns():
    body = "Vietcombank và Techcombank đều công bố KQKD Q1/2026. ĐHĐCĐ ngày 25/4."
    result = check_no_english_jargon(body)
    assert result["pass"] is True


def test_word_count_in_range_passes():
    body = " ".join(["word"] * 300)
    result = check_word_count(body)
    assert result["pass"] is True


def test_word_count_too_long_fails():
    body = " ".join(["word"] * 450)
    result = check_word_count(body)
    assert result["pass"] is False
    assert "450" in result["reason"]


def test_word_count_too_short_fails():
    body = " ".join(["word"] * 100)
    result = check_word_count(body)
    assert result["pass"] is False


def test_mechanism_count_3_to_7_passes():
    body = """Mở đầu giới thiệu vấn đề.
- Lý do 1 cơ chế A.
- Lý do 2 cơ chế B.
- Lý do 3 cơ chế C.
- Lý do 4 cơ chế D.
"""
    result = check_mechanism_count(body)
    assert result["pass"] is True


def test_mechanism_count_too_few_fails():
    body = "Mở đầu.\n- Một bullet.\n- Hai bullet."
    result = check_mechanism_count(body)
    assert result["pass"] is False


def test_can_de_y_narrative_passes_with_paragraph():
    body = """## Cần để ý

Lần đầu sau 19 năm, VCB chấp nhận tăng trưởng chậm để xây bộ đệm. Tín hiệu cần theo dõi: dư nợ Q2 và CASA Q3 sẽ quyết định liệu chiến lược này có lan ra ngành.
"""
    result = check_can_de_y_narrative(body)
    assert result["pass"] is True


def test_can_de_y_narrative_fails_on_data_bullets_only():
    body = """## Cần để ý

- CASA 33%
- NPL 0,62%
- LDR 80%
"""
    result = check_can_de_y_narrative(body)
    assert result["pass"] is False


def test_no_metadata_leak_fails_on_strategic_shift():
    body = "Đây là tin strategic-shift quan trọng."
    result = check_no_metadata_leak(body)
    assert result["pass"] is False


def test_no_metadata_leak_passes_clean():
    body = "Đây là tin chuyển hướng chiến lược quan trọng."
    result = check_no_metadata_leak(body)
    assert result["pass"] is True


def test_check_all_returns_all_5():
    body = "Test body content here for sanity."
    result = check_all(body)
    assert set(result.keys()) == {"no_english_jargon", "word_count", "mechanism_count", "can_de_y_narrative", "no_metadata_leak"}
