"""Tests for lib/intra_batch_dedup.py — inter-brief thesis dedup within a batch.

Problem this solves: Story Editor sometimes outputs 2+ briefs for the SAME
ticker with the SAME dominant deep_question category in 1 batch — Master
writes 2 articles with overlapping thesis (MSN/PLX duplicates 2026-05-13).
"""

from __future__ import annotations

import pytest

from lib import intra_batch_dedup


def _brief(
    *,
    row_id: str,
    ticker: str,
    options_cats: list[str],
    angle_label: str = "",
    n_data_trail: int = 1,
    n_key_metrics: int = 3,
) -> dict:
    return {
        "row_id": row_id,
        "ticker": ticker,
        "angle_label": angle_label,
        "deep_question_options": [
            {
                "category": cat,
                "question": f"Q{i} {cat}",
                "data_trail_preview": [f"d{j}" for j in range(n_data_trail)],
                "key_metric_count": n_key_metrics,
            }
            for i, cat in enumerate(options_cats)
        ],
    }


# ---- compute_dominant_category ----------------------------------------------


def test_dominant_category_most_frequent() -> None:
    b = _brief(row_id="r1", ticker="ACB", options_cats=["paradox", "paradox", "why_now"])
    assert intra_batch_dedup.compute_dominant_category(b) == "paradox"


def test_dominant_category_tie_picks_options_zero() -> None:
    b = _brief(row_id="r1", ticker="ACB", options_cats=["why_now", "paradox"])
    # Tie 1-1 → options[0].category wins
    assert intra_batch_dedup.compute_dominant_category(b) == "why_now"


def test_dominant_category_empty_options_returns_empty() -> None:
    b = {"row_id": "r1", "ticker": "ACB", "deep_question_options": []}
    assert intra_batch_dedup.compute_dominant_category(b) == ""


def test_dominant_category_missing_options_field_returns_empty() -> None:
    b = {"row_id": "r1", "ticker": "ACB"}
    assert intra_batch_dedup.compute_dominant_category(b) == ""


def test_dominant_category_option_without_category_skipped() -> None:
    b = {
        "row_id": "r1",
        "ticker": "ACB",
        "deep_question_options": [
            {"question": "Q1"},  # no category
            {"category": "paradox", "question": "Q2"},
        ],
    }
    assert intra_batch_dedup.compute_dominant_category(b) == "paradox"


# ---- dedup_briefs_in_batch --------------------------------------------------


def test_dedup_single_brief_kept() -> None:
    briefs = [_brief(row_id="r1", ticker="ACB", options_cats=["paradox"])]
    out = intra_batch_dedup.dedup_briefs_in_batch(briefs)
    assert out[0]["dedup_decision"] == "keep"


def test_dedup_two_different_categories_both_kept() -> None:
    briefs = [
        _brief(row_id="r1", ticker="ACB", options_cats=["paradox"]),
        _brief(row_id="r2", ticker="ACB", options_cats=["why_now"]),
    ]
    out = intra_batch_dedup.dedup_briefs_in_batch(briefs)
    assert [b["dedup_decision"] for b in out] == ["keep", "keep"]


def test_dedup_two_same_category_drops_weaker() -> None:
    """Weaker = fewer options entries. Strongest = keep."""
    briefs = [
        _brief(row_id="r1", ticker="ACB", options_cats=["paradox"], n_data_trail=1),
        _brief(row_id="r2", ticker="ACB", options_cats=["paradox", "why_now"], n_data_trail=3),
    ]
    out = intra_batch_dedup.dedup_briefs_in_batch(briefs)
    by_id = {b["row_id"]: b for b in out}
    assert by_id["r2"]["dedup_decision"] == "keep"  # more options + more data
    assert by_id["r1"]["dedup_decision"] == "drop_dup_thesis"


def test_dedup_three_same_category_keeps_only_strongest() -> None:
    briefs = [
        _brief(row_id="r1", ticker="ACB", options_cats=["paradox"], n_data_trail=1),
        _brief(row_id="r2", ticker="ACB", options_cats=["paradox", "why_now"], n_data_trail=2),
        _brief(row_id="r3", ticker="ACB", options_cats=["paradox", "why_now", "comparison_deep"], n_data_trail=4),
    ]
    out = intra_batch_dedup.dedup_briefs_in_batch(briefs)
    by_id = {b["row_id"]: b for b in out}
    assert by_id["r3"]["dedup_decision"] == "keep"
    assert by_id["r2"]["dedup_decision"] == "drop_dup_thesis"
    assert by_id["r1"]["dedup_decision"] == "drop_dup_thesis"


def test_dedup_mixed_groups() -> None:
    briefs = [
        _brief(row_id="r1", ticker="ACB", options_cats=["paradox"]),
        _brief(row_id="r2", ticker="ACB", options_cats=["paradox", "why_now"], n_data_trail=5),
        _brief(row_id="r3", ticker="ACB", options_cats=["why_now"]),  # different cat, lone
    ]
    out = intra_batch_dedup.dedup_briefs_in_batch(briefs)
    by_id = {b["row_id"]: b for b in out}
    assert by_id["r2"]["dedup_decision"] == "keep"  # strongest in paradox group
    assert by_id["r1"]["dedup_decision"] == "drop_dup_thesis"
    assert by_id["r3"]["dedup_decision"] == "keep"  # lone why_now


def test_dedup_different_tickers_not_grouped() -> None:
    """Same category across DIFFERENT tickers should NOT trigger dedup."""
    briefs = [
        _brief(row_id="r1", ticker="ACB", options_cats=["paradox"]),
        _brief(row_id="r2", ticker="VHM", options_cats=["paradox"]),
    ]
    out = intra_batch_dedup.dedup_briefs_in_batch(briefs)
    assert all(b["dedup_decision"] == "keep" for b in out)


def test_dedup_tie_breaks_by_first_in_list() -> None:
    """When briefs identical on options/data/metrics, first-in-list wins."""
    briefs = [
        _brief(row_id="r1", ticker="ACB", options_cats=["paradox"], n_data_trail=1),
        _brief(row_id="r2", ticker="ACB", options_cats=["paradox"], n_data_trail=1),
    ]
    out = intra_batch_dedup.dedup_briefs_in_batch(briefs)
    by_id = {b["row_id"]: b for b in out}
    assert by_id["r1"]["dedup_decision"] == "keep"
    assert by_id["r2"]["dedup_decision"] == "drop_dup_thesis"


def test_dedup_empty_dominant_does_not_group() -> None:
    """Briefs with empty dominant_category (no valid options) are skipped — kept by default."""
    briefs = [
        {"row_id": "r1", "ticker": "ACB", "deep_question_options": []},
        {"row_id": "r2", "ticker": "ACB", "deep_question_options": []},
    ]
    out = intra_batch_dedup.dedup_briefs_in_batch(briefs)
    assert all(b["dedup_decision"] == "keep" for b in out)


def test_dedup_returns_new_list_does_not_mutate_input() -> None:
    """Input briefs should NOT be mutated in place — caller may iterate them again."""
    briefs = [
        _brief(row_id="r1", ticker="ACB", options_cats=["paradox"]),
        _brief(row_id="r2", ticker="ACB", options_cats=["paradox"]),
    ]
    intra_batch_dedup.dedup_briefs_in_batch(briefs)
    for b in briefs:
        assert "dedup_decision" not in b
