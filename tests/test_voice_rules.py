"""Tests for lib/voice_rules — shared voice constants V1.3.

V1.3 extracts V1.2 title constants from headline_scorer.py into shared module
for title + body parallel use. Adds body-specific constants for V1.3 body
voice ("bình dân xuồng xã nguy hiểm").
"""
from __future__ import annotations
import re


# === V1.2 title constants (extracted from headline_scorer.py) ===

def test_title_tension_words_exists():
    from lib.voice_rules import TITLE_TENSION_WORDS
    assert isinstance(TITLE_TENSION_WORDS, list)
    assert "hy sinh" in TITLE_TENSION_WORDS
    assert "đánh đổi" in TITLE_TENSION_WORDS
    assert len(TITLE_TENSION_WORDS) >= 9


def test_dramatic_verbs_exists_with_binh_dan():
    from lib.voice_rules import DRAMATIC_VERBS
    assert isinstance(DRAMATIC_VERBS, list)
    # V1.2 bình dân additions
    assert "ăn lãi" in DRAMATIC_VERBS
    assert "khoe lãi" in DRAMATIC_VERBS
    assert "dồn tiền" in DRAMATIC_VERBS
    assert "xén cổ tức" in DRAMATIC_VERBS
    assert "gom hàng" in DRAMATIC_VERBS
    assert "bơm vốn" in DRAMATIC_VERBS
    assert "ngồi trên tiền" in DRAMATIC_VERBS


def test_pr_clickbait_words_exists():
    from lib.voice_rules import PR_CLICKBAIT_WORDS
    assert isinstance(PR_CLICKBAIT_WORDS, list)
    assert "cú nổ" in PR_CLICKBAIT_WORDS
    assert "sốc" in PR_CLICKBAIT_WORDS


def test_bao_chi_formulaic_phrases_exists():
    from lib.voice_rules import BAO_CHI_FORMULAIC_PHRASES
    assert isinstance(BAO_CHI_FORMULAIC_PHRASES, list)
    assert "đánh đổi gì" in BAO_CHI_FORMULAIC_PHRASES
    assert "đặt mục tiêu" in BAO_CHI_FORMULAIC_PHRASES
    assert "lao dốc" in BAO_CHI_FORMULAIC_PHRASES


def test_naturalized_finance_terms_exists():
    from lib.voice_rules import NATURALIZED_FINANCE_TERMS
    assert isinstance(NATURALIZED_FINANCE_TERMS, set)
    assert "esop" in NATURALIZED_FINANCE_TERMS
    assert "nim" in NATURALIZED_FINANCE_TERMS
    assert "roe" in NATURALIZED_FINANCE_TERMS


def test_bao_chi_quarter_pattern_exists():
    from lib.voice_rules import BAO_CHI_QUARTER_PATTERN
    assert isinstance(BAO_CHI_QUARTER_PATTERN, re.Pattern)
    # Should match báo chí summary lead
    assert BAO_CHI_QUARTER_PATTERN.match("Q1/2026 VHM ghi nhận lãi 25K tỷ")
    assert BAO_CHI_QUARTER_PATTERN.match("năm 2026 VCB lãi vượt")


def test_rubric_label_leak_exists():
    from lib.voice_rules import RUBRIC_LABEL_LEAK
    assert isinstance(RUBRIC_LABEL_LEAK, set)
    assert "question" in RUBRIC_LABEL_LEAK
    assert "declarative tension" in RUBRIC_LABEL_LEAK


def test_concrete_question_subjects_exists():
    from lib.voice_rules import CONCRETE_QUESTION_SUBJECTS
    assert isinstance(CONCRETE_QUESTION_SUBJECTS, list)
    assert "ai gom" in CONCRETE_QUESTION_SUBJECTS
    assert "tiền chạy" in CONCRETE_QUESTION_SUBJECTS
    assert "khôn hay liều" in CONCRETE_QUESTION_SUBJECTS


# === V1.3 body-specific constants (NEW) ===

def test_bao_chi_body_verbs_exists():
    """V1.3 — body-level báo chí verbs from audit top 3:
    bàn giao/ghi nhận (6x) + phát hành (5x) + công bố/dự kiến (4x)."""
    from lib.voice_rules import BAO_CHI_BODY_VERBS
    assert isinstance(BAO_CHI_BODY_VERBS, list)
    assert "bàn giao" in BAO_CHI_BODY_VERBS
    assert "ghi nhận" in BAO_CHI_BODY_VERBS
    assert "công bố" in BAO_CHI_BODY_VERBS
    assert "dự kiến đạt" in BAO_CHI_BODY_VERBS
    assert "phát hành thành công" in BAO_CHI_BODY_VERBS
    assert "đặt mục tiêu" in BAO_CHI_BODY_VERBS


def test_preferred_body_verbs_exists():
    """V1.3 — bình dân verbs preferred for body (parallel V1.2 title)."""
    from lib.voice_rules import PREFERRED_BODY_VERBS
    assert isinstance(PREFERRED_BODY_VERBS, list)
    assert "ăn" in PREFERRED_BODY_VERBS
    assert "khoe" in PREFERRED_BODY_VERBS
    assert "dồn" in PREFERRED_BODY_VERBS
    assert "xén" in PREFERRED_BODY_VERBS
    assert "gom" in PREFERRED_BODY_VERBS
    assert "bơm" in PREFERRED_BODY_VERBS


def test_metaphor_markers_exists():
    """V1.3 — analogy/metaphor markers boost sentence_density."""
    from lib.voice_rules import METAPHOR_MARKERS
    assert isinstance(METAPHOR_MARKERS, list)
    assert "như" in METAPHOR_MARKERS
    assert "kiểu" in METAPHOR_MARKERS
    assert "ví như" in METAPHOR_MARKERS
    assert "thật ra" in METAPHOR_MARKERS


def test_closing_vague_ban_exists():
    """V1.3 — closing weak phrases (auto-reject in actionable_closing gate)."""
    from lib.voice_rules import CLOSING_VAGUE_BAN
    assert isinstance(CLOSING_VAGUE_BAN, list)
    assert "cần theo dõi" in CLOSING_VAGUE_BAN
    assert "đáng theo dõi" in CLOSING_VAGUE_BAN
    assert "làm chỉ báo" in CLOSING_VAGUE_BAN


def test_stance_verbs_exists():
    """V1.3 — actionable stance verbs (closing Layer 1)."""
    from lib.voice_rules import STANCE_VERBS
    assert isinstance(STANCE_VERBS, list)
    assert "nên cầm" in STANCE_VERBS
    assert "nên giảm" in STANCE_VERBS
    assert "phù hợp NĐT" in STANCE_VERBS
