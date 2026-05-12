"""Integration test for Headline Craft Step 4.5 — schema-level (no real LLM).

Verifies:
- Insert article with V5.1 pipeline_version
- log_pipeline_step accepts valid step_4_5_headline_craft payload
- log_pipeline_step rejects weak title (fails hard criteria)
- UPDATE generated_news.title with valid Headline pick
- V5.0 back-compat: step_4_5 schema not enforced

Schema-level only — real LLM dispatch deferred to /tin VCB live run.
"""
from __future__ import annotations
import json
from pathlib import Path

import pytest

from lib.headline_scorer import check_hard_criteria
from lib.pipeline_db import PipelineDB


@pytest.fixture
def db_v5_1():
    """Fresh in-memory DB initialized with canonical schema.

    Matches existing tests/test_pipeline_db.py fixture pattern.
    """
    schema_path = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db = PipelineDB(":memory:")
    db.init_schema(schema_path)
    yield db
    db.close()


def _seed_article(db, article_id="a1", pipeline_version="V5.1"):
    """Insert crawl_log row + generated_news placeholder row.

    Uses unique row_id + source_url per article_id so test isolation holds
    even if a single fixture spawns multiple articles.
    """
    suffix = article_id
    db.insert_crawl_row({
        "row_id": f"r-{suffix}",
        "funnel_batch_id": "b1",
        "ticker": "TCB",
        "source_name": "CafeF",
        "source_url": f"http://example.com/{suffix}",
        "title": "Test",
        "crawled_at": "2026-05-12T00:00:00Z",
    })
    db.insert_generated_news({
        "article_id": article_id,
        "row_id": f"r-{suffix}",
        "ticker": "TCB",
        "sector": "Bank",
        # Master places placeholder; Headline overrides at Step 4.5.
        # Em dash here is in generated_news.title (not the validated
        # step_4_5_headline_craft.final_title) — schema does not check.
        "title": "PLACEHOLDER — Headline overrides",
        "body": "Body content placeholder for test",
        "accepted_hypothesis": 1,
        "status": "draft",
        "pipeline_version": pipeline_version,
    })


def test_step_4_5_valid_payload_persists(db_v5_1):
    """Headline picks valid title → log_pipeline_step persists merged log."""
    _seed_article(db_v5_1, article_id="a1", pipeline_version="V5.1")
    payload = {
        "model": "claude-sonnet-4-6",
        "duration_ms": 5000,
        "final_title": "Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?",
        "final_loi": "Question",
        "picked_score": 7,
        "candidates": [
            {"text": "Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?", "loi": "Question", "score": 7}
        ],
        "hard_criteria_pass": {
            "ticker_present": True,
            "word_count_le_12": True,
            "hook_strong": {"tension_present": True, "click_test_pass": True},
            "binh_dan_nguy_hiem": {"plain_language": True, "sharp_edge": True},
            "no_em_dash": True,
        },
    }
    db_v5_1.log_pipeline_step("a1", "step_4_5_headline_craft", payload)

    # Verify persisted
    row = db_v5_1.conn.execute(
        "SELECT pipeline_log FROM generated_news WHERE article_id='a1'"
    ).fetchone()
    log = json.loads(row["pipeline_log"])
    assert "step_4_5_headline_craft" in log
    assert log["step_4_5_headline_craft"]["final_title"] == "Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?"


def test_step_4_5_weak_title_rejected(db_v5_1):
    """Headline emits weak title → log_pipeline_step raises ValueError."""
    _seed_article(db_v5_1, article_id="a2", pipeline_version="V5.1")
    payload = {
        "model": "claude-sonnet-4-6",
        "duration_ms": 5000,
        "final_title": "Tin tức quý 1",  # No ticker, no hook → fails 5 criteria
        "final_loi": "Question",
        "picked_score": 0,
        "candidates": [],
        "hard_criteria_pass": {
            "ticker_present": False,
            "word_count_le_12": True,
            "hook_strong": {"tension_present": False, "click_test_pass": False},
            "binh_dan_nguy_hiem": {"plain_language": True, "sharp_edge": False},
            "no_em_dash": True,
        },
    }
    with pytest.raises(ValueError, match="hard criteria"):
        db_v5_1.log_pipeline_step("a2", "step_4_5_headline_craft", payload)


def test_step_4_5_em_dash_title_rejected(db_v5_1):
    """V1.1 PATCH: em dash in final_title → ValueError (no_em_dash fail)."""
    _seed_article(db_v5_1, article_id="a3", pipeline_version="V5.1")
    payload = {
        "model": "claude-sonnet-4-6",
        "duration_ms": 5000,
        "final_title": "Q1 BSR ăn 8.265 tỷ — sếp chỉ hứa 2.162 tỷ?",  # em dash present
        "final_loi": "Declarative tension",
        "picked_score": 6,
        "candidates": [],
        "hard_criteria_pass": {
            "ticker_present": True,
            "word_count_le_12": True,
            "hook_strong": {"tension_present": True, "click_test_pass": True},
            "binh_dan_nguy_hiem": {"plain_language": True, "sharp_edge": True},
            "no_em_dash": False,
        },
    }
    with pytest.raises(ValueError, match="hard criteria|no_em_dash"):
        db_v5_1.log_pipeline_step("a3", "step_4_5_headline_craft", payload)


def test_update_generated_news_title_after_headline(db_v5_1):
    """End-to-end: Master placeholder → Headline overrides via UPDATE."""
    _seed_article(db_v5_1, article_id="a4", pipeline_version="V5.1")

    # Verify placeholder
    row = db_v5_1.conn.execute(
        "SELECT title FROM generated_news WHERE article_id='a4'"
    ).fetchone()
    assert "PLACEHOLDER" in row["title"]

    # Headline UPDATE
    final_title = "Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?"
    db_v5_1.conn.execute(
        "UPDATE generated_news SET title = ? WHERE article_id = ?",
        (final_title, "a4"),
    )
    db_v5_1.conn.commit()

    # Verify
    row = db_v5_1.conn.execute(
        "SELECT title FROM generated_news WHERE article_id='a4'"
    ).fetchone()
    assert row["title"] == final_title

    # Verify final title passes hard criteria
    hc = check_hard_criteria(final_title)
    assert hc["passed"] is True


def test_v5_0_article_skips_step_4_5_validation(db_v5_1):
    """V5.0 row should NOT enforce step_4_5 schema (back-compat)."""
    _seed_article(db_v5_1, article_id="a5", pipeline_version="V5.0")
    # Weak payload — would fail V5.1 but should be accepted in V5.0
    payload = {
        "model": "claude-sonnet-4-6",
        "duration_ms": 5000,
        "final_title": "Tin tức",  # Weak — but V5.0 doesn't enforce
        "final_loi": "Question",
        "picked_score": 0,
        "candidates": [],
        "hard_criteria_pass": {},
    }
    # Should not raise — V5.0 skips step_4_5 check
    db_v5_1.log_pipeline_step("a5", "step_4_5_headline_craft", payload)
