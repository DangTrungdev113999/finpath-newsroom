"""Tests for lib/format_picker_logic — 5-step format selection flow."""
from __future__ import annotations
import pytest
from lib.format_picker_logic import pick_format_for_option


def _option(category="paradox", narrative="...", data_trail_preview=None, key_metric_count=2):
    return {
        "category": category,
        "narrative_setup": narrative,
        "data_trail_preview": data_trail_preview or [
            {"source": "Finpath_API/test"},
            {"source": "KB/test"},
            {"source": "WebSearch/test"},
        ],
        "key_metric_count": key_metric_count,
    }


def test_paradox_picks_standard_qa():
    result = pick_format_for_option(_option(category="paradox"), market_data=None)
    assert result["format_id"] == "standard_qa"
    assert result["tone_bias"] == "neutral"
    assert result["length_target"] == 250


def test_why_now_picks_standard_qa():
    result = pick_format_for_option(_option(category="why_now"), market_data=None)
    assert result["format_id"] == "standard_qa"


def test_comparison_deep_picks_listicle():
    result = pick_format_for_option(_option(category="comparison_deep"), market_data=None)
    assert result["format_id"] == "standard_listicle"


def test_early_signal_picks_listicle():
    result = pick_format_for_option(_option(category="early_signal"), market_data=None)
    assert result["format_id"] == "standard_listicle"


def test_hidden_mechanism_no_timeline_picks_qa():
    opt = _option(category="hidden_mechanism", narrative="Cơ chế NIM nội tại")
    result = pick_format_for_option(opt, market_data=None)
    assert result["format_id"] == "standard_qa"


def test_hidden_mechanism_3_timeline_markers_picks_narrative():
    opt = _option(
        category="hidden_mechanism",
        narrative="Q1/2025 TCB rút 12.000 tỷ. Đến cuối 2024 quyết định. Năm 2026 thấy kết quả.",
    )
    result = pick_format_for_option(opt, market_data=None)
    assert result["format_id"] == "standard_narrative"


def test_unknown_category_falls_back_flash_qa():
    """Factual question without 5-category → flash_qa fallback."""
    result = pick_format_for_option(_option(category="factual_single"), market_data=None)
    assert result["format_id"] == "flash_qa"


def test_length_downgrade_low_data_depth():
    """data_trail_preview≤2 sources AND key_metric_count≤1 → downgrade standard→flash."""
    opt = _option(
        category="paradox",
        data_trail_preview=[{"source": "KB/test"}],
        key_metric_count=1,
    )
    result = pick_format_for_option(opt, market_data=None)
    assert result["format_id"] == "flash_qa"


def test_mood_red_tone_bias():
    market_data = {"pct_change_today": -4.5}
    result = pick_format_for_option(_option(category="paradox"), market_data=market_data)
    assert result["tone_bias"] == "acknowledge_market_red"


def test_mood_green_tone_bias():
    market_data = {"pct_change_today": 5.0}
    result = pick_format_for_option(_option(category="paradox"), market_data=market_data)
    assert result["tone_bias"] == "acknowledge_market_green"


def test_mood_neutral_under_threshold():
    market_data = {"pct_change_today": 1.5}
    result = pick_format_for_option(_option(category="paradox"), market_data=market_data)
    assert result["tone_bias"] == "neutral"


def test_format_reason_contains_template():
    """format_reason fills template, no free-write."""
    result = pick_format_for_option(_option(category="paradox"), market_data=None)
    assert "Category=" in result["format_reason"]
    assert "paradox" in result["format_reason"]


def test_returned_keys():
    """Output shape: 4 fields."""
    result = pick_format_for_option(_option(), market_data=None)
    assert set(result.keys()) == {"format_id", "format_reason", "tone_bias", "length_target"}


def test_currency_4digit_not_timeline_marker():
    """TIMELINE_MARKER_RE must not match bare currency numbers (false positive)."""
    opt = _option(
        category="hidden_mechanism",
        narrative="Doanh thu 5000 tỷ, lợi nhuận 3000 tỷ, vốn 8000 tỷ",
    )
    result = pick_format_for_option(opt, market_data=None)
    # Should default to standard_qa (no real timeline markers, just currency)
    assert result["format_id"] == "standard_qa"
