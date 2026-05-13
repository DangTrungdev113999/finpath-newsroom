"""Tests for lib/headline_scorer V1.1 — 5 hard criteria + 8-point rubric."""
from __future__ import annotations
import pytest
from lib.headline_scorer import (
    check_hard_criteria, score_title, pick_best_candidate,
    has_ticker, has_specific_number, has_dramatic_verb, has_tension_word,
    has_paradox_pattern, has_open_question, has_pr_clickbait, has_english,
    has_em_dash,
)


# === Hard criteria — 5 keys V1.1 ===

def test_hard_criteria_pass_canonical_example():
    """Benchmark: 'Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?' passes all 5."""
    result = check_hard_criteria("Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?")
    assert result["passed"] is True
    assert result["ticker_present"] is True
    assert result["word_count_le_16"] is True
    assert result["hook_strong"]["tension_present"] is True
    assert result["binh_dan_nguy_hiem"]["plain_language"] is True
    assert result["no_em_dash"] is True


def test_hard_criteria_rejects_em_dash():
    """V1.1: title with em dash '—' fails no_em_dash."""
    result = check_hard_criteria("Q1 BSR ăn 8.265 tỷ — sếp chỉ hứa 2.162 tỷ?")
    assert result["no_em_dash"] is False
    assert result["passed"] is False


def test_hard_criteria_hook_strong_2_subtests():
    """hook_strong returns dict with tension_present + click_test_pass keys."""
    result = check_hard_criteria("Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?")
    assert isinstance(result["hook_strong"], dict)
    assert "tension_present" in result["hook_strong"]
    assert "click_test_pass" in result["hook_strong"]


def test_hard_criteria_binh_dan_nguy_hiem_2_subtests():
    """binh_dan_nguy_hiem returns dict with plain_language + sharp_edge keys."""
    result = check_hard_criteria("Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?")
    assert isinstance(result["binh_dan_nguy_hiem"], dict)
    assert "plain_language" in result["binh_dan_nguy_hiem"]
    assert "sharp_edge" in result["binh_dan_nguy_hiem"]


def test_hard_criteria_rejects_no_ticker():
    """Title without ticker → ticker_present False."""
    result = check_hard_criteria("Ngân hàng lớn nhất hy sinh lợi nhuận 5.000 tỷ?")
    assert result["ticker_present"] is False
    assert result["passed"] is False


def test_hard_criteria_rejects_too_long():
    """Title > 16 từ → word_count_le_16 False."""
    # V1.3: 17 từ
    result = check_hard_criteria("TCB hy sinh năm tỷ đổi lấy gì lớn nhất ngân hàng VN năm 2026 quý 1 tăng trưởng mạnh")
    assert result["word_count_le_16"] is False
    assert result["passed"] is False


def test_hard_criteria_rejects_pr_clickbait():
    """PR clickbait words → binh_dan.sharp_edge True nhưng plain_language False."""
    result = check_hard_criteria("TCB cú nổ kỷ tích sốc 5.000 tỷ")
    assert result["binh_dan_nguy_hiem"]["plain_language"] is False
    assert result["passed"] is False


def test_hard_criteria_rejects_english_jargon():
    """English jargon → plain_language False."""
    result = check_hard_criteria("TCB momentum strong, NIM expansion 30bps")
    assert result["binh_dan_nguy_hiem"]["plain_language"] is False
    assert result["passed"] is False


# === Detector functions ===

def test_has_ticker_bank_universe():
    assert has_ticker("TCB Q1 2026 lãi vượt 30%") is True
    assert has_ticker("Ngân hàng lớn nhất hy sinh lợi nhuận?") is False


def test_has_ticker_group_ref():
    assert has_ticker("Big4 tăng trưởng vượt tư nhân") is True


def test_has_specific_number():
    assert has_specific_number("TCB lãi 5.000 tỷ Q1") is True
    assert has_specific_number("TCB tăng trưởng mạnh") is False


def test_has_dramatic_verb():
    assert has_dramatic_verb("TCB hy sinh 5.000 tỷ") is True
    assert has_dramatic_verb("TCB lãi 5.000 tỷ Q1") is False


def test_has_tension_word():
    assert has_tension_word("TCB hy sinh để đổi lấy gì?") is True
    assert has_tension_word("TCB Q1 lãi mạnh") is False


def test_has_paradox_pattern():
    assert has_paradox_pattern("TCB lãi 5.000 tỷ nhưng cổ phiếu giảm") is True
    assert has_paradox_pattern("TCB lãi 5.000 tỷ tăng trưởng") is False


def test_has_open_question():
    assert has_open_question("TCB hy sinh 5.000 tỷ để đổi lấy gì?") is True
    assert has_open_question("TCB hy sinh 5.000 tỷ.") is False


def test_has_pr_clickbait():
    assert has_pr_clickbait("Cú nổ sốc Hot trends 2026") is True
    assert has_pr_clickbait("TCB hy sinh 5.000 tỷ?") is False


def test_has_em_dash():
    assert has_em_dash("Q1 BSR ăn 8.265 tỷ — sếp chỉ hứa 2.162 tỷ?") is True
    assert has_em_dash("TCB hy sinh 5.000 tỷ - đổi lấy gì?") is False  # hyphen OK
    assert has_em_dash("TCB hy sinh 5.000 tỷ – đổi lấy gì?") is False  # en dash OK


# === V1.3 not_orphan_number ===

def test_orphan_number_rejects_lone_percent_with_vague_ngành():
    """User feedback 2026-05-13: '85% mà ngành còn lại' → fail."""
    from lib.headline_scorer import has_orphan_number
    assert has_orphan_number("STB xén 85% mà ngành còn lại vẫn tuyển?") is True


def test_orphan_number_accepts_percent_with_subject():
    """'85% nhân sự' OK, 'lãi 85%' OK — subject within 4 tokens."""
    from lib.headline_scorer import has_orphan_number
    assert has_orphan_number("STB xén 85% nhân sự ngành bank Q1?") is False
    assert has_orphan_number("DXG bán hàng vọt 46%, lãi mẹ tụt 22%. Tiền chạy đâu?") is False


def test_orphan_number_rejects_vague_ngành_without_specifier():
    """'ngành' alone without specifier 'bank/CK/BĐS' → fail."""
    from lib.headline_scorer import has_orphan_number
    assert has_orphan_number("VHM cứu ngành sau khủng hoảng?") is True


def test_orphan_number_accepts_ngành_bank_specifier():
    """'ngành bank' with specifier → pass."""
    from lib.headline_scorer import has_orphan_number
    assert has_orphan_number("STB ôm 85% nhân sự cắt giảm ngành bank Q1, lạ?") is False


def test_hard_criteria_v1_3_pure_comparison_passes():
    """V1.3 16-từ pure comparison hook passes."""
    result = check_hard_criteria(
        "Q1 ngành bank phân hóa: STB tống 2.700, VPB+TCB+LPB nhồi thêm 700. Bank nào sai?"
    )
    assert result["passed"] is True
    assert result["not_orphan_number"] is True


def test_hard_criteria_v1_2_bad_hook_now_rejected():
    """Old V1.2 hook 'STB xén 85% mà ngành còn lại vẫn tuyển?' → fail V1.3."""
    result = check_hard_criteria("STB xén 85% mà ngành còn lại vẫn tuyển?")
    assert result["passed"] is False
    assert result["not_orphan_number"] is False


# === Scoring ===

def test_score_title_benchmark():
    """V1.2 benchmark — concrete bình dân hook should score ≥5/8."""
    result = score_title("Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?")
    assert result["score"] >= 5  # V1.2 — ăn lãi dramatic_verb + 2 numbers + question
    assert result["max"] == 8


def test_score_title_minimal():
    """Title with only ticker → low score."""
    result = score_title("TCB tăng trưởng năm 2026")
    assert result["score"] <= 4


# === Pick best ===

def test_pick_best_candidate_returns_best():
    """Multiple candidates → highest score wins. V1.2 — concrete bình dân benchmark."""
    candidates = [
        "TCB tăng trưởng năm 2026",  # weak, no number/question
        "Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?",  # V1.2 benchmark
        "TCB lãi mạnh",  # too short
    ]
    result = pick_best_candidate(candidates)
    assert "BSR" in result["final_title"]  # V1.2: bình dân benchmark wins
    assert result["picked_score"] >= 5


def test_pick_best_candidate_all_fail_raises():
    """All fail hard criteria → ValueError."""
    candidates = [
        "Cú nổ sốc 2026",  # No ticker + clickbait
        "Ngân hàng tăng trưởng mạnh",  # No ticker
    ]
    with pytest.raises(ValueError):
        pick_best_candidate(candidates)
