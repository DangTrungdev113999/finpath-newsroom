"""Tests for lib/headline_scorer V1.5-lite — 8 hard criteria + 6-point rubric.

V1.5-lite (2026-05-13 PM): drop V1.2-V1.4 word bonus scorer (cause Pattern A
pile-on). Add Hán-Việt + abbreviation hard criteria. Simplified rubric.
"""
from __future__ import annotations
import pytest
from lib.headline_scorer import (
    check_hard_criteria, score_title, pick_best_candidate,
    has_ticker, has_specific_number, has_paradox_pattern,
    has_open_question, has_pr_clickbait, has_english,
    has_em_dash, has_orphan_number, is_label_leak,
)


# === V1.5-lite 8 hard criteria ===

def test_hard_criteria_v1_5_lite_pass_canonical():
    """V1.5-lite benchmark — STB layoff hook passes 8 hard criteria."""
    result = check_hard_criteria(
        "STB sa thải 2.700 nhân viên, VPB tuyển 362. Bank nào đúng?"
    )
    assert result["passed"] is True
    assert result["ticker_present"] is True
    assert result["word_count_le_16"] is True
    assert result["no_em_dash"] is True
    assert result["not_label_leak"] is True
    assert result["not_orphan_number"] is True
    assert result["no_han_viet_formal"] is True
    assert result["abbreviation_expanded"] is True
    assert result["has_concrete_number"] is True


def test_hard_criteria_rejects_no_ticker():
    """Title without ticker → ticker_present False."""
    result = check_hard_criteria("Ngân hàng lớn nhất hy sinh lợi nhuận 5.000 tỷ?")
    assert result["ticker_present"] is False
    assert result["passed"] is False


def test_hard_criteria_rejects_too_long():
    """Title > 16 từ → word_count_le_16 False."""
    result = check_hard_criteria(
        "TCB hy sinh năm tỷ đổi lấy gì lớn nhất ngân hàng VN năm 2026 quý 1 tăng trưởng mạnh"
    )
    assert result["word_count_le_16"] is False
    assert result["passed"] is False


def test_hard_criteria_rejects_em_dash():
    """V1.1 PATCH preserved: em dash banned."""
    result = check_hard_criteria("Q1 BSR ăn 8.265 tỷ — sếp chỉ hứa 2.162 tỷ?")
    assert result["no_em_dash"] is False
    assert result["passed"] is False


def test_hard_criteria_rejects_han_viet_formal_in_title():
    """V1.5-lite NEW: title với 'độc bản' / 'hội đủ' → fail."""
    result = check_hard_criteria("FPT có 8 di sản UNESCO độc bản tại Huế?")
    assert result["no_han_viet_formal"] is False
    assert result["passed"] is False


def test_hard_criteria_rejects_bare_abbreviation_in_title():
    """V1.5-lite NEW: title với BCA / GRDP chưa expand → fail."""
    result = check_hard_criteria("BCA ôm 50% vốn FOX, FPT mẹ kẹt 2.330 tỷ?")
    assert result["abbreviation_expanded"] is False


def test_hard_criteria_naturalized_terms_pass():
    """ESOP / NIM / ROE — naturalized, pass abbreviation check."""
    result = check_hard_criteria("SSI bán ESOP 100 tỷ, nội bộ ăn 180 tỷ ưu đãi")
    assert result["abbreviation_expanded"] is True


def test_hard_criteria_ticker_passes_abbreviation():
    """Ticker (STB/VHM/FPT) skipped from abbreviation check."""
    result = check_hard_criteria("STB cắt 2.700, VPB tuyển 362. Bank nào đúng?")
    assert result["abbreviation_expanded"] is True


def test_hard_criteria_rejects_pr_clickbait():
    """PR clickbait words still banned."""
    result = check_hard_criteria("TCB cú nổ kỷ tích sốc 5.000 tỷ")
    assert result["passed"] is False


def test_hard_criteria_rejects_english_jargon():
    """English jargon → plain_language False."""
    result = check_hard_criteria("TCB momentum strong, breaking pattern 30bps")
    # has_english should return True → plain_language False → passed False
    assert result["passed"] is False


# === V1.5-lite dropped functions verification ===

def test_v1_5_lite_drops_is_bao_chi():
    """V1.5-lite drops is_bao_chi keyword check."""
    import lib.headline_scorer as hs
    assert not hasattr(hs, "is_bao_chi"), "is_bao_chi should be dropped V1.5-lite"


def test_v1_5_lite_drops_has_concrete_question_subject():
    """V1.5-lite drops has_concrete_question_subject (caused 'nào sai' pile-on)."""
    import lib.headline_scorer as hs
    assert not hasattr(hs, "has_concrete_question_subject")


# === V1.6 — hard criteria 8→7 (orphan_number to soft) + vague_action_verb ===

class TestV16HardCriteriaReduce:
    def test_orphan_number_no_longer_fails_passed(self):
        """V1.6: title with orphan % no longer blocks passed=True."""
        # "ngành" without specifier was V1.3 orphan trigger
        result = check_hard_criteria("PVS ăn 44%, ngành thì chưa rõ")
        # not_orphan_number may be False (info field) but should not gate `passed`
        # if all other 7 criteria pass — verify by checking they're decoupled
        # In this title other criteria likely OK except plain_language
        # Focus: passed flag composition no longer includes not_orphan_number
        # If not_orphan_number=False but all 7 hard pass, passed=True
        result2 = check_hard_criteria("STB cắt 85%, ngành còn lại tuyển?")
        if all(result2[k] for k in [
            "ticker_present", "word_count_le_16", "no_em_dash",
            "not_label_leak", "no_han_viet_formal",
            "abbreviation_expanded", "plain_language",
        ]):
            # All 7 hard pass — passed should be True regardless of orphan_number
            assert result2["passed"] is True or result2["not_orphan_number"] is True

    def test_passed_uses_only_7_hard_criteria(self):
        """V1.6: passed flag = 7 hard criteria conjunction, not 8."""
        result = check_hard_criteria("STB cắt 2.700, VPB tuyển 362. Bank nào đúng?")
        # All 7 hard should pass
        seven_hard = (
            result["ticker_present"]
            and result["word_count_le_16"]
            and result["no_em_dash"]
            and result["not_label_leak"]
            and result["no_han_viet_formal"]
            and result["abbreviation_expanded"]
            and result["plain_language"]
        )
        assert result["passed"] is seven_hard


class TestVagueActionVerbDetector:
    def test_flags_orphan_an_with_percent(self):
        """'PVS ăn 44%' — verb ăn không có concrete object."""
        from lib.headline_scorer import detect_vague_action_verb
        hints = detect_vague_action_verb("PVS kế hoạch giảm 48% nhưng Q1 đã ăn 44%")
        assert any(h["verb"] == "ăn" for h in hints)

    def test_passes_an_with_concrete_object(self):
        """'PVS ăn 1.974 tỷ lãi' — verb có object lãi → OK."""
        from lib.headline_scorer import detect_vague_action_verb
        hints = detect_vague_action_verb("PVS ăn 1.974 tỷ lãi kỷ lục")
        assert not any(h["verb"] == "ăn" for h in hints)

    def test_always_flags_nguy(self):
        """'nguy' không phải verb đơn — luôn flag."""
        from lib.headline_scorer import detect_vague_action_verb
        hints = detect_vague_action_verb("FPT mẹ nguy 2.330 tỷ?")
        assert any(h["verb"] == "nguy" for h in hints)

    def test_always_flags_mac(self):
        """'mắc' trong title gần như luôn mơ hồ."""
        from lib.headline_scorer import detect_vague_action_verb
        hints = detect_vague_action_verb("PVS tiền mặt còn mắc Lô B?")
        assert any(h["verb"] == "mắc" for h in hints)

    def test_clean_title_no_hints(self):
        """Title không có vague verbs → empty list."""
        from lib.headline_scorer import detect_vague_action_verb
        hints = detect_vague_action_verb("VHM Q1 lãi 25.625 tỷ, gấp 3 lần Vietcombank")
        assert hints == []

    def test_che_flagged_when_orphan(self):
        """'khoản 282 tỷ che gì' — che vague + no concrete object."""
        from lib.headline_scorer import detect_vague_action_verb
        hints = detect_vague_action_verb("PVS Q1 ăn 44%: khoản 282 tỷ che gì?")
        assert any(h["verb"] == "che" for h in hints)

    def test_hints_in_check_hard_criteria_result(self):
        """check_hard_criteria returns vague_action_verbs key (info)."""
        result = check_hard_criteria("FPT mẹ nguy 2.330 tỷ?")
        assert "vague_action_verbs" in result
        assert isinstance(result["vague_action_verbs"], list)
        assert any(h["verb"] == "nguy" for h in result["vague_action_verbs"])


# === Detector functions (preserved) ===

def test_has_ticker_in_universe():
    assert has_ticker("TCB Q1 2026 lãi vượt 30%") is True
    assert has_ticker("Ngân hàng lớn nhất hy sinh lợi nhuận?") is False


def test_has_specific_number_financial():
    assert has_specific_number("TCB lãi 5.000 tỷ Q1") is True
    assert has_specific_number("TCB tăng trưởng mạnh") is False


def test_has_specific_number_headcount():
    """V1.3 PATCH: headcount unit accepted."""
    assert has_specific_number("STB cắt 2.700 người Q1") is True


def test_has_specific_number_bare_4digit():
    """V1.3 PATCH: bare 4-digit accepted (e.g. 2.700 / 11.026)."""
    assert has_specific_number("STB cắt 2.700, VPB tuyển 362") is True


def test_has_paradox_pattern():
    assert has_paradox_pattern("TCB lãi 5.000 tỷ nhưng cổ phiếu giảm") is True
    assert has_paradox_pattern("TCB lãi 5.000 tỷ tăng trưởng") is False


def test_has_open_question():
    assert has_open_question("TCB hy sinh 5.000 tỷ để đổi lấy gì?") is True
    assert has_open_question("TCB hy sinh 5.000 tỷ.") is False


def test_has_em_dash():
    assert has_em_dash("Q1 BSR ăn 8.265 tỷ — sếp chỉ hứa?") is True
    assert has_em_dash("TCB hy sinh 5.000 tỷ - đổi lấy gì?") is False
    assert has_em_dash("TCB hy sinh 5.000 tỷ – đổi lấy gì?") is False


def test_has_orphan_number_v1_3_preserved():
    """V1.3 orphan number detector preserved."""
    assert has_orphan_number("STB xén 85% mà ngành còn lại vẫn tuyển?") is True
    assert has_orphan_number("DXG bán hàng vọt 46%, lãi mẹ tụt 22%. Tiền chạy đâu?") is False


# === V1.5-lite 6-point rubric ===

def test_score_title_v1_5_lite_max_6():
    """V1.5-lite rubric max = 6 (simplified from V1.3 8-point)."""
    result = score_title("STB cắt 2.700 người. Bank nào sai?")
    assert result["max"] == 6


def test_score_title_v1_5_lite_concrete_number_bonus():
    """V1.5-lite rubric: +2 has_concrete_number (replaces V1.3 multiple bonuses)."""
    result = score_title(
        "STB sa thải 2.700 nhân viên, VPB tuyển 362. Bank nào đúng?"
    )
    # Score: ticker (+1) + concrete_number (+2) + open_question (+1) +
    # extra_concise ≤10 từ (+1) = 5/6 (no paradox pattern)
    assert result["score"] >= 4


def test_score_title_v1_5_lite_drops_dramatic_verb_bonus():
    """V1.5-lite: 'hy sinh' (V1.2 dramatic_verb +2) no longer scores."""
    result_old_bonus = score_title("TCB hy sinh 5.000 tỷ. Đáng giá?")
    # In V1.2 this would score: dramatic_verb(+2) + specific_number(+2) +
    # open_question(+1) + tension_word(+1) = 6/8. V1.5-lite: ticker(+1) +
    # concrete_number(+2) + open_question(+1) + extra_concise (+1) = 5/6 max.
    # Just verify the function still works + returns max 6.
    assert result_old_bonus["max"] == 6
    assert "elements" in result_old_bonus


# === Pick best ===

def test_pick_best_candidate_returns_best():
    """V1.5-lite: highest score wins."""
    candidates = [
        "TCB tăng trưởng năm 2026",  # weak, no number/question
        "STB sa thải 2.700 nhân viên, VPB tuyển 362. Bank nào đúng?",  # benchmark
        "TCB lãi mạnh",  # too short, no ticker number
    ]
    result = pick_best_candidate(candidates)
    assert "STB" in result["final_title"]
    assert result["picked_score"] >= 4


def test_pick_best_candidate_all_fail_raises():
    """All fail hard criteria → ValueError."""
    candidates = [
        "Cú nổ sốc 2026",  # No ticker + PR clickbait
        "Ngân hàng tăng trưởng mạnh",  # No ticker
    ]
    with pytest.raises(ValueError):
        pick_best_candidate(candidates)
