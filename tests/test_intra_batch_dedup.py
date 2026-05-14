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


# ---- merge_briefs_in_batch (V5.1.8 NEW) --------------------------------------


def test_merge_two_same_category_enriches_winner() -> None:
    """V5.1.8: 2 brief same dominant_category → winner gets merged options +
    absorbed loser; loser marked `absorbed_into_<winner>`."""
    briefs = [
        {
            "row_id": "r_weak",
            "ticker": "MSN",
            "deep_question_options": [
                {"category": "paradox", "question": "Q_weak", "key_metric_count": 1},
            ],
        },
        {
            "row_id": "r_strong",
            "ticker": "MSN",
            "deep_question_options": [
                {"category": "paradox", "question": "Q_strong_1", "key_metric_count": 3},
                {"category": "paradox", "question": "Q_strong_2", "key_metric_count": 3},
            ],
        },
    ]
    out = intra_batch_dedup.merge_briefs_in_batch(briefs)
    by_id = {b["row_id"]: b for b in out}

    assert by_id["r_strong"]["merge_decision"] == "merged"
    assert by_id["r_weak"]["merge_decision"] == "absorbed_into_r_strong"

    winner_questions = {opt["question"] for opt in by_id["r_strong"]["deep_question_options"]}
    assert winner_questions == {"Q_strong_1", "Q_strong_2", "Q_weak"}
    assert by_id["r_strong"]["merged_from_briefs"][0]["row_id"] == "r_weak"


def test_merge_singleton_kept_decision() -> None:
    """Singleton group → merge_decision='keep'. No merged_from_briefs field set."""
    briefs = [_brief(row_id="r1", ticker="ACB", options_cats=["paradox"])]
    out = intra_batch_dedup.merge_briefs_in_batch(briefs)
    assert out[0]["merge_decision"] == "keep"
    assert "merged_from_briefs" not in out[0]


def test_merge_options_capped_at_five() -> None:
    """Winner enriched options capped at 5 to prevent context bloat."""
    briefs = [
        {
            "row_id": "r_winner",
            "ticker": "MSN",
            "deep_question_options": [
                {"category": "paradox", "question": f"W{i}", "key_metric_count": 5} for i in range(4)
            ],
        },
        {
            "row_id": "r_loser",
            "ticker": "MSN",
            "deep_question_options": [
                {"category": "paradox", "question": f"L{i}", "key_metric_count": 1} for i in range(4)
            ],
        },
    ]
    out = intra_batch_dedup.merge_briefs_in_batch(briefs)
    by_id = {b["row_id"]: b for b in out}
    assert len(by_id["r_winner"]["deep_question_options"]) == 5  # capped


def test_merge_key_evidence_union_dedupes() -> None:
    """Winner gets merged_key_evidence — union with first-seen order preserved."""
    briefs = [
        {
            "row_id": "r_winner",
            "ticker": "MSN",
            "deep_question_options": [
                {
                    "category": "paradox",
                    "question": "Q1",
                    "stance_directive": {"key_evidence": ["A", "B"]},
                },
                {
                    "category": "paradox",
                    "question": "Q2",
                    "stance_directive": {"key_evidence": ["B", "C"]},
                },
            ],
        },
        {
            "row_id": "r_loser",
            "ticker": "MSN",
            "deep_question_options": [
                {
                    "category": "paradox",
                    "question": "Q3",
                    "stance_directive": {"key_evidence": ["D", "A"]},
                },
            ],
        },
    ]
    out = intra_batch_dedup.merge_briefs_in_batch(briefs)
    by_id = {b["row_id"]: b for b in out}
    # r_winner has more options → strength wins
    winner_evidence = by_id["r_winner"]["merged_key_evidence"]
    assert winner_evidence == ["A", "B", "C", "D"]  # first-seen order


def test_merge_different_dominant_categories_no_merge() -> None:
    briefs = [
        _brief(row_id="r1", ticker="ACB", options_cats=["paradox"]),
        _brief(row_id="r2", ticker="ACB", options_cats=["why_now"]),
    ]
    out = intra_batch_dedup.merge_briefs_in_batch(briefs)
    assert all(b["merge_decision"] == "keep" for b in out)
    for b in out:
        assert "merged_from_briefs" not in b


def test_merge_three_same_cat_one_winner_two_absorbed() -> None:
    briefs = [
        _brief(row_id="r1", ticker="MSN", options_cats=["paradox"], n_data_trail=1),
        _brief(row_id="r2", ticker="MSN", options_cats=["paradox", "why_now"], n_data_trail=2),
        _brief(row_id="r3", ticker="MSN", options_cats=["paradox", "why_now", "comparison_deep"], n_data_trail=4),
    ]
    out = intra_batch_dedup.merge_briefs_in_batch(briefs)
    by_id = {b["row_id"]: b for b in out}
    assert by_id["r3"]["merge_decision"] == "merged"
    assert by_id["r2"]["merge_decision"] == "absorbed_into_r3"
    assert by_id["r1"]["merge_decision"] == "absorbed_into_r3"
    # Winner has 2 absorbed entries in merged_from_briefs
    assert len(by_id["r3"]["merged_from_briefs"]) == 2


def test_dedup_wrapper_maps_to_merge_outcomes() -> None:
    """V5.1.6 backward-compat: dedup_decision='keep' for winner+singleton,
    'drop_dup_thesis' for absorbed."""
    briefs = [
        _brief(row_id="r1", ticker="MSN", options_cats=["paradox"], n_data_trail=1),
        _brief(row_id="r2", ticker="MSN", options_cats=["paradox", "why_now"], n_data_trail=5),
    ]
    out = intra_batch_dedup.dedup_briefs_in_batch(briefs)
    by_id = {b["row_id"]: b for b in out}
    assert by_id["r2"]["dedup_decision"] == "keep"  # merged winner
    assert by_id["r1"]["dedup_decision"] == "drop_dup_thesis"  # absorbed loser
    # New merge fields also present
    assert by_id["r2"]["merge_decision"] == "merged"
