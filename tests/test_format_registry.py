"""Tests for lib/format_registry — load + lookup format definitions."""
from __future__ import annotations
import pytest
from lib.format_registry import (
    load_registry, get_format, get_candidates_for_category, FORMAT_IDS,
)


def test_load_registry_returns_4_formats():
    reg = load_registry()
    assert set(reg.keys()) == {"flash_qa", "standard_qa", "standard_listicle", "standard_narrative"}


def test_format_ids_constant_matches_registry():
    reg = load_registry()
    assert set(FORMAT_IDS) == set(reg.keys())


def test_get_format_flash_qa_fields():
    fmt = get_format("flash_qa")
    # V1.3: shrunk from [100, 150] → [80, 120] (Twitter style)
    assert fmt["length_range"] == [80, 120]
    assert fmt["length_target"] == 100
    assert fmt["structure"] == "paragraph_only"
    assert fmt["bullets_count"] == [0, 0]


def test_v1_3_length_ranges():
    """V1.3 shrunk ~20% across all 4 formats."""
    assert get_format("flash_qa")["length_range"] == [80, 120]
    assert get_format("standard_qa")["length_range"] == [180, 240]
    assert get_format("standard_listicle")["length_range"] == [220, 280]
    assert get_format("standard_narrative")["length_range"] == [220, 280]


def test_v1_3_bold_density_min_present():
    """V1.3 added bold_density_min per format."""
    for fid in ["flash_qa", "standard_qa", "standard_listicle", "standard_narrative"]:
        fmt = get_format(fid)
        assert "bold_density_min" in fmt
        assert fmt["bold_density_min"]["mode"] in ("absolute", "ratio")
        assert fmt["bold_density_min"]["value"] > 0

    # flash_qa absolute mode (Twitter style)
    assert get_format("flash_qa")["bold_density_min"]["mode"] == "absolute"
    assert get_format("flash_qa")["bold_density_min"]["value"] == 3

    # Others ratio mode
    assert get_format("standard_qa")["bold_density_min"]["value"] == 0.04
    assert get_format("standard_listicle")["bold_density_min"]["value"] == 0.05
    assert get_format("standard_narrative")["bold_density_min"]["value"] == 0.03


def test_get_candidates_paradox():
    candidates = get_candidates_for_category("paradox")
    assert candidates == ["standard_qa"]


def test_get_candidates_hidden_mechanism_returns_2():
    candidates = set(get_candidates_for_category("hidden_mechanism"))
    assert candidates == {"standard_qa", "standard_narrative"}


def test_get_candidates_comparison_deep():
    assert get_candidates_for_category("comparison_deep") == ["standard_listicle"]


def test_get_candidates_unknown_returns_empty():
    assert get_candidates_for_category("nonexistent_category") == []


def test_get_format_invalid_raises():
    with pytest.raises(KeyError):
        get_format("nonexistent_format")
