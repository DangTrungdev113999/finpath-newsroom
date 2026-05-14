"""Tests for lib/voice_rules V1.5-lite — mechanical bans only."""
from __future__ import annotations
import re


# === V1.5-lite KEEP constants ===

def test_naturalized_finance_terms_exists():
    from lib.voice_rules import NATURALIZED_FINANCE_TERMS
    assert isinstance(NATURALIZED_FINANCE_TERMS, set)
    assert "esop" in NATURALIZED_FINANCE_TERMS
    assert "nim" in NATURALIZED_FINANCE_TERMS
    assert "roe" in NATURALIZED_FINANCE_TERMS


def test_closing_vague_ban_exists():
    from lib.voice_rules import CLOSING_VAGUE_BAN
    assert isinstance(CLOSING_VAGUE_BAN, list)
    assert "cần theo dõi" in CLOSING_VAGUE_BAN
    assert "làm chỉ báo" in CLOSING_VAGUE_BAN


def test_stance_verbs_exists():
    from lib.voice_rules import STANCE_VERBS
    assert isinstance(STANCE_VERBS, list)
    assert "nên cầm" in STANCE_VERBS
    assert "phù hợp NĐT" in STANCE_VERBS


# === V1.5-lite NEW HAN_VIET_FORMAL_BAN ===

def test_han_viet_formal_ban_is_dict():
    from lib.voice_rules import HAN_VIET_FORMAL_BAN
    assert isinstance(HAN_VIET_FORMAL_BAN, dict)
    assert len(HAN_VIET_FORMAL_BAN) >= 15


def test_han_viet_formal_ban_contains_audit_terms():
    """User audit 2026-05-13: độc bản / hội đủ / tái định giá flagged."""
    from lib.voice_rules import HAN_VIET_FORMAL_BAN
    assert "độc bản" in HAN_VIET_FORMAL_BAN
    assert HAN_VIET_FORMAL_BAN["độc bản"] == "duy nhất"
    assert "hội đủ" in HAN_VIET_FORMAL_BAN
    assert HAN_VIET_FORMAL_BAN["hội đủ"] == "đủ"
    assert "tái định giá" in HAN_VIET_FORMAL_BAN
    assert HAN_VIET_FORMAL_BAN["tái định giá"] == "định giá lại"


def test_han_viet_formal_ban_replacement_is_string():
    """Each key maps to a bình dân replacement string."""
    from lib.voice_rules import HAN_VIET_FORMAL_BAN
    for formal, bd in HAN_VIET_FORMAL_BAN.items():
        assert isinstance(bd, str)
        assert len(bd) > 0


# === V1.5-lite DROPPED constants verification ===

def test_dropped_dramatic_verbs():
    """V1.5-lite drops DRAMATIC_VERBS (cause Pattern A pile-on)."""
    import lib.voice_rules as vr
    assert not hasattr(vr, "DRAMATIC_VERBS"), "DRAMATIC_VERBS should be dropped V1.5-lite"


def test_dropped_preferred_body_verbs():
    """V1.5-lite drops PREFERRED_BODY_VERBS (force pile-on)."""
    import lib.voice_rules as vr
    assert not hasattr(vr, "PREFERRED_BODY_VERBS")


def test_dropped_bao_chi_body_verbs():
    """V1.5-lite drops BAO_CHI_BODY_VERBS (replaced by Master prompt examples)."""
    import lib.voice_rules as vr
    assert not hasattr(vr, "BAO_CHI_BODY_VERBS")


def test_dropped_metaphor_markers():
    """V1.5-lite drops METAPHOR_MARKERS (force cưỡng ép metaphors)."""
    import lib.voice_rules as vr
    assert not hasattr(vr, "METAPHOR_MARKERS")


def test_dropped_concrete_question_subjects():
    """V1.5-lite drops CONCRETE_QUESTION_SUBJECTS (force 'nào sai' patterns)."""
    import lib.voice_rules as vr
    assert not hasattr(vr, "CONCRETE_QUESTION_SUBJECTS")


def test_dropped_rubric_label_leak():
    """V1.5-lite drops RUBRIC_LABEL_LEAK (Headline rubric concern, moved to local)."""
    import lib.voice_rules as vr
    assert not hasattr(vr, "RUBRIC_LABEL_LEAK")


def test_dropped_bao_chi_quarter_pattern():
    """V1.5-lite drops BAO_CHI_QUARTER_PATTERN (V5.1.8: Headline retired — pattern obsolete)."""
    import lib.voice_rules as vr
    assert not hasattr(vr, "BAO_CHI_QUARTER_PATTERN")
