"""Tests for lib/stages/aggregate_costs.py — V5.1.8 cost aggregator."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lib import pipeline_db
from lib.stages import aggregate_costs

SCHEMA_SQL = Path(__file__).resolve().parents[1] / "data" / "pipeline.schema.sql"


@pytest.fixture
def db(tmp_path: Path):
    target = tmp_path / "pipeline.db"
    conn = pipeline_db.PipelineDB(str(target))
    conn.init_schema(SCHEMA_SQL)
    yield conn
    conn.close()


def _seed_article(
    db,
    *,
    article_id: str = "art-001",
    pipeline_log: dict | None = None,
    gemini_cost: float | None = None,
    grok_cost: float | None = None,
    image_cost: float | None = None,
) -> None:
    db.conn.execute(
        "INSERT INTO crawl_log (row_id, funnel_batch_id, ticker, source_name, "
        "source_url, title, raw_content, crawled_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("row-001", "batch-001", "VCB", "cafef", "u", "t", "raw", "2026-05-14"),
    )
    db.conn.execute(
        "INSERT INTO generated_news (article_id, row_id, ticker, sector, title, "
        "body, accepted_hypothesis, pipeline_log, gemini_cost_usd, grok_cost_usd, "
        "image_cost_usd) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (article_id, "row-001", "VCB", "Bank", "T", "B", 1,
         json.dumps(pipeline_log or {}, ensure_ascii=False),
         gemini_cost, grok_cost, image_cost),
    )
    db.conn.commit()


def test_extract_claude_usage_dict_tokens() -> None:
    log = {
        "step_4_master": {
            "model": "claude-sonnet-4-6",
            "tokens": {"input": 10_000, "output": 2_000, "cache_creation": 1_000, "cache_read": 500},
        }
    }
    out = aggregate_costs.extract_claude_usage(log)
    # input + cache_creation + cache_read all priced as input
    assert out["tokens_in"] == 11_500
    assert out["tokens_out"] == 2_000
    assert out["model"] == "claude-sonnet-4-6"


def test_extract_claude_usage_legacy_int_tokens() -> None:
    """Legacy parse_task_usage stores tokens as int total. Aggregator should
    attribute 80/20 split for billing audit."""
    log = {"step_4_master": {"model": "claude-opus-4-7", "tokens": 10_000}}
    out = aggregate_costs.extract_claude_usage(log)
    assert out["tokens_in"] == 8_000  # 80%
    assert out["tokens_out"] == 2_000  # 20%
    assert out["model"] == "claude-opus-4-7"


def test_extract_claude_usage_missing_step() -> None:
    out = aggregate_costs.extract_claude_usage({})
    assert out == {"tokens_in": None, "tokens_out": None, "model": None}


def test_aggregate_article_writes_all_columns(db) -> None:
    """Happy path: Claude usage from pipeline_log + Gemini/Grok/Image costs from
    DB → claude_cost computed + total_cost_usd = sum of all 4."""
    _seed_article(
        db,
        pipeline_log={
            "step_4_master": {
                "model": "claude-sonnet-4-6",
                "tokens": {"input": 100_000, "output": 10_000, "cache_creation": 0, "cache_read": 0},
            }
        },
        gemini_cost=0.005,
        grok_cost=0.008,
        image_cost=0.04,
    )

    result = aggregate_costs.aggregate_article_costs(db, "art-001")

    # Claude sonnet $3/$15 per 1M: 100k×$3 + 10k×$15 = 0.30 + 0.15 = 0.45
    assert result["claude_cost_usd"] == pytest.approx(0.45)
    # Total = 0.45 + 0.005 + 0.008 + 0.04 = 0.503
    assert result["total_cost_usd"] == pytest.approx(0.503)

    # Verify persisted
    row = db.conn.execute(
        "SELECT claude_cost_usd, total_cost_usd, claude_tokens_in, claude_tokens_out "
        "FROM generated_news WHERE article_id = ?",
        ("art-001",),
    ).fetchone()
    assert row["claude_cost_usd"] == pytest.approx(0.45)
    assert row["total_cost_usd"] == pytest.approx(0.503)
    assert row["claude_tokens_in"] == 100_000
    assert row["claude_tokens_out"] == 10_000


def test_aggregate_article_no_claude_usage(db) -> None:
    """When pipeline_log has no step_4_master.tokens, claude cost stays NULL
    but total_cost_usd still sums the other 3 components."""
    _seed_article(db, pipeline_log={}, gemini_cost=0.005, grok_cost=0.008)
    result = aggregate_costs.aggregate_article_costs(db, "art-001")
    assert result["claude_cost_usd"] is None
    assert result["total_cost_usd"] == pytest.approx(0.013)


def test_aggregate_article_no_costs_anywhere_keeps_total_null(db) -> None:
    """All 4 components absent → total_cost_usd remains NULL (signals 'no
    cost data' rather than fabricated 0)."""
    _seed_article(db)
    result = aggregate_costs.aggregate_article_costs(db, "art-001")
    assert result["claude_cost_usd"] is None
    assert result["total_cost_usd"] is None
    row = db.conn.execute(
        "SELECT total_cost_usd FROM generated_news WHERE article_id = ?",
        ("art-001",),
    ).fetchone()
    assert row["total_cost_usd"] is None


def test_aggregate_article_idempotent_safe_rerun(db) -> None:
    """Running aggregate twice gives the same result; no double-counting."""
    _seed_article(
        db,
        pipeline_log={
            "step_4_master": {
                "model": "claude-opus-4-7",
                "tokens": {"input": 50_000, "output": 5_000, "cache_creation": 0, "cache_read": 0},
            }
        },
        gemini_cost=0.005,
        grok_cost=0.008,
    )
    r1 = aggregate_costs.aggregate_article_costs(db, "art-001")
    r2 = aggregate_costs.aggregate_article_costs(db, "art-001")
    assert r1["total_cost_usd"] == r2["total_cost_usd"]


def test_aggregate_article_not_found(db) -> None:
    assert aggregate_costs.aggregate_article_costs(db, "missing") == {}
