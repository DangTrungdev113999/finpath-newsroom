"""Tests for Step 4.4 Grok block in markdown frontmatter (Phase C1)."""

from __future__ import annotations

import json
from typing import Any

import frontmatter

from lib.render_compare_feed import render_article_md_v4


_GROK_BODY_REAL = (
    "**Test ăn 2.000 tỷ Q1**, gấp đôi cùng kỳ.\n\n"
    "- **Bold 1 với colon: và dash—em**: ≥25 từ dense + 1 con số rõ.\n"
    "- **Bold 2**: ≥25 từ dense.\n\n"
    "NĐT giá trị nên tích lũy vùng 75-80, mục tiêu 100 trong 18 tháng."
)


def _base_article(**overrides: Any) -> dict:
    article = {
        "article_id": "art-grok",
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
        # Gemini side (null) — exercise both blocks independent
        "gemini_status": None,
        "gemini_title": None,
        "gemini_body": None,
        "gemini_word_count": None,
        "gemini_model": None,
        "gemini_generated_at": None,
        "gemini_error": None,
        # Grok side defaults
        "grok_status": None,
        "grok_title": None,
        "grok_body": None,
        "grok_word_count": None,
        "grok_model": None,
        "grok_generated_at": None,
        "grok_error": None,
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
        "crawled_at": "2026-05-14T10:00:00+07:00",
        "published_time": "2026-05-14T09:00:00+07:00",
        "master_decision": "write_article",
        "master_note": "Anchor",
        "brief_json": json.dumps({
            "why_chosen_narrative": "",
            "angle_label": "",
            "angle_narrative": "",
            "deep_question_options": [],
        }, ensure_ascii=False),
    }


def test_render_includes_grok_block_when_success() -> None:
    article = _base_article(
        grok_status="success",
        grok_title="Grok ACB hỏi xoáy đáp xoay",
        grok_body=_GROK_BODY_REAL,
        grok_word_count=270,
        grok_model="grok-4-fast-non-reasoning",
        grok_generated_at="2026-05-14T10:01:23+00:00",
    )
    output = render_article_md_v4(article, _base_anchor(), [_base_anchor()])
    parsed = frontmatter.loads(output)
    grok = parsed.metadata.get("grok")
    assert isinstance(grok, dict)
    assert grok["title"] == "Grok ACB hỏi xoáy đáp xoay"
    assert grok["body"] == _GROK_BODY_REAL
    assert grok["word_count"] == 270
    assert grok["model"] == "grok-4-fast-non-reasoning"
    assert grok["generated_at"] == "2026-05-14T10:01:23+00:00"


def test_render_omits_grok_block_when_skipped_failure() -> None:
    article = _base_article(grok_status="skipped_failure", grok_error="upstream")
    output = render_article_md_v4(article, _base_anchor(), [_base_anchor()])
    parsed = frontmatter.loads(output)
    assert parsed.metadata.get("grok") is None


def test_render_omits_grok_block_when_skipped_disabled() -> None:
    article = _base_article(grok_status="skipped_disabled", grok_error="missing_api_key")
    output = render_article_md_v4(article, _base_anchor(), [_base_anchor()])
    parsed = frontmatter.loads(output)
    assert parsed.metadata.get("grok") is None


def test_render_omits_grok_block_when_legacy_null_status() -> None:
    article = _base_article()
    output = render_article_md_v4(article, _base_anchor(), [_base_anchor()])
    parsed = frontmatter.loads(output)
    assert parsed.metadata.get("grok") is None


def test_render_emits_both_gemini_and_grok_blocks_independently() -> None:
    article = _base_article(
        gemini_status="success",
        gemini_title="Gemini title",
        gemini_body="Gemini body.",
        gemini_word_count=200,
        gemini_model="gemini-2.5-pro",
        grok_status="success",
        grok_title="Grok title",
        grok_body=_GROK_BODY_REAL,
        grok_word_count=270,
        grok_model="grok-4-fast-non-reasoning",
    )
    output = render_article_md_v4(article, _base_anchor(), [_base_anchor()])
    parsed = frontmatter.loads(output)
    assert parsed.metadata["gemini"]["title"] == "Gemini title"
    assert parsed.metadata["grok"]["title"] == "Grok title"
    # Sanity — bodies preserved through YAML round-trip
    assert parsed.metadata["gemini"]["body"] == "Gemini body."
    assert parsed.metadata["grok"]["body"] == _GROK_BODY_REAL
