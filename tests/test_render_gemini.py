"""Tests for Step 4.3 Gemini block in markdown frontmatter (C1)."""

from __future__ import annotations

import json
from typing import Any

import frontmatter
import pytest

from lib.render_compare_feed import render_article_md_v4


_GEMINI_BODY_REAL = (
    "**Test ăn 1.974 tỷ Q1**, gấp đôi cùng kỳ.\n\n"
    "- **Bold 1 với colon: và dash—em**: ≥25 từ dense + 1 con số rõ.\n"
    "- **Bold 2**: ≥25 từ dense.\n\n"
    "NĐT giá trị nên tích lũy vùng 75-80, mục tiêu 100 trong 18 tháng."
)


def _base_article(**overrides: Any) -> dict:
    article = {
        "article_id": "art-gem",
        "row_id": "anchor-1",
        "ticker": "ACB",
        "sector": "Bank",
        "title": "ACB Q1 lãi vượt 5.000 tỷ",
        "body": "Body Claude.",
        "word_count": 50,
        "key_view": "lạc quan",
        "insight_final": "Insight.",
        "skeptic_critique": None,
        "skeptic_angle": None,
        "skeptic_verdict": "pass",
        "pipeline_log": json.dumps({
            "step_4_master": {
                "chosen_question_idx": 0,
                "chosen_pick_reason": "test",
                "skip_reasons": {},
                "data_trail": [],
            }
        }, ensure_ascii=False),
        "public_slug": "ACB-test",
        "gemini_status": None,
        "gemini_title": None,
        "gemini_body": None,
        "gemini_word_count": None,
        "gemini_model": None,
        "gemini_generated_at": None,
        "gemini_error": None,
    }
    article.update(overrides)
    return article


def _base_anchor() -> dict:
    return {
        "row_id": "anchor-1",
        "funnel_batch_id": "ACB-test",
        "ticker": "ACB",
        "source_name": "src",
        "source_url": "https://src/a",
        "title": "Raw",
        "crawled_at": "2026-05-13T10:00:00+07:00",
        "published_time": "2026-05-13T09:00:00+07:00",
        "master_decision": "write_article",
        "master_note": "Anchor",
        "brief_json": json.dumps({
            "why_chosen_narrative": "",
            "angle_label": "",
            "angle_narrative": "",
            "deep_question_options": [],
        }, ensure_ascii=False),
    }


def test_render_includes_gemini_block_when_success() -> None:
    article = _base_article(
        gemini_status="success",
        gemini_title="ACB tăng vốn 30% nhưng ROE giữ 25%",
        gemini_body=_GEMINI_BODY_REAL,
        gemini_word_count=250,
        gemini_model="gemini-2.5-pro",
        gemini_generated_at="2026-05-13T10:01:23+00:00",
    )
    output = render_article_md_v4(article, _base_anchor(), [_base_anchor()])
    parsed = frontmatter.loads(output)
    gemini = parsed.metadata.get("gemini")
    assert isinstance(gemini, dict), "frontmatter must contain `gemini` block on success"
    assert gemini["title"] == "ACB tăng vốn 30% nhưng ROE giữ 25%"
    assert gemini["body"] == _GEMINI_BODY_REAL  # round-trip exact
    assert gemini["word_count"] == 250
    assert gemini["model"] == "gemini-2.5-pro"
    assert gemini["generated_at"] == "2026-05-13T10:01:23+00:00"


def test_render_omits_gemini_block_when_skipped_failure() -> None:
    article = _base_article(
        gemini_status="skipped_failure",
        gemini_error="upstream 503",
    )
    output = render_article_md_v4(article, _base_anchor(), [_base_anchor()])
    parsed = frontmatter.loads(output)
    assert parsed.metadata.get("gemini") is None


def test_render_omits_gemini_block_when_skipped_disabled() -> None:
    article = _base_article(
        gemini_status="skipped_disabled",
        gemini_error="missing_api_key",
    )
    output = render_article_md_v4(article, _base_anchor(), [_base_anchor()])
    parsed = frontmatter.loads(output)
    assert parsed.metadata.get("gemini") is None


def test_render_omits_gemini_block_when_legacy_null_status() -> None:
    """Legacy articles persisted before Step 4.3 existed have gemini_status=NULL."""
    article = _base_article()  # all gemini_* fields None
    output = render_article_md_v4(article, _base_anchor(), [_base_anchor()])
    parsed = frontmatter.loads(output)
    assert parsed.metadata.get("gemini") is None


def test_render_omits_gemini_when_body_missing_even_if_status_success() -> None:
    """Defensive: status says success but body missing → still omit (no half-broken block)."""
    article = _base_article(
        gemini_status="success",
        gemini_title="x",
        gemini_body=None,  # corrupt state
    )
    output = render_article_md_v4(article, _base_anchor(), [_base_anchor()])
    parsed = frontmatter.loads(output)
    assert parsed.metadata.get("gemini") is None
