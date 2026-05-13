"""Tests for lib/stages/run_gemini_writer.py — Step 4.3 orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from lib import pipeline_db
from lib.stages import run_gemini_writer

SCHEMA_SQL = Path(__file__).resolve().parents[1] / "data" / "pipeline.schema.sql"


@pytest.fixture
def db(tmp_path: Path):
    target = tmp_path / "pipeline.db"
    conn = pipeline_db.PipelineDB(str(target))
    conn.init_schema(SCHEMA_SQL)
    yield conn
    conn.close()


@pytest.fixture
def secrets_with_key(tmp_path: Path) -> Path:
    p = tmp_path / "secrets.yaml"
    p.write_text("gemini:\n  api_key: 'real-key'\n", encoding="utf-8")
    return p


@pytest.fixture
def secrets_missing_key(tmp_path: Path) -> Path:
    p = tmp_path / "secrets.yaml"
    p.write_text("gemini:\n  api_key: 'REPLACE_WITH_GEMINI_API_KEY'\n", encoding="utf-8")
    return p


@pytest.fixture
def prompt_template(tmp_path: Path) -> Path:
    p = tmp_path / "prompt.md"
    p.write_text(
        "Ticker: {{ticker}}\n"
        "Format: {{format_id}}\n"
        "Question: {{brief_deep_question}}\n"
        "Stance: {{brief_stance_direction}}\n"
        "Raw title: {{raw_news_title}}\n"
        "Data trail: {{data_trail_json}}\n",
        encoding="utf-8",
    )
    return p


def _seed_full_article(db, *, article_id: str = "art-001") -> None:
    """Seed crawl_log with full V5 brief + generated_news with master picked summary."""
    crawl_brief = {
        "row_id": "row-001",
        "ticker": "ACB",
        "sector": "bank",
        "primary_ticker": "ACB",
        "master_route": "bank",
        "deep_question_options": [
            {
                "question": "ACB tăng vốn 30% có pha loãng cổ đông?",
                "category": "why_now",
                "stance_directive": {
                    "direction": "bullish",
                    "confidence": "high",
                    "reason": "ROE 25%, CASA 28%",
                    "key_evidence": ["ROE", "CASA"],
                },
                "format_id": "standard_qa",
                "tone_bias": "neutral",
                # Real Story Editor stores integer word count (200/250/300/...), not
                # categorical string. Regression for crash on _substitute() type error.
                "length_target": 250,
            }
        ],
    }
    db.conn.execute(
        "INSERT INTO crawl_log (row_id, funnel_batch_id, ticker, source_name, "
        "source_url, title, raw_content, crawled_at, brief_json) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            "row-001",
            "batch-001",
            "ACB",
            "cafef",
            "https://cafef.vn/acb-q1",
            "ACB lãi Q1 vượt 5.000 tỷ — Big4 áp lực",
            "ACB công bố lãi trước thuế Q1 đạt 5.200 tỷ, tăng 18%...",
            "2026-05-13",
            json.dumps(crawl_brief, ensure_ascii=False),
        ),
    )
    gn_brief = {
        "chosen_question_idx": 0,
        "stance_directive": crawl_brief["deep_question_options"][0]["stance_directive"],
        "format_id": "standard_qa",
    }
    pipeline_log = {
        "step_4_master": {
            "chosen_question_idx": 0,
            "chosen_pick_reason": "match data depth",
            "skip_reasons": {},
            "format_id_used": "standard_qa",
            "data_trail": [
                {
                    "source": "Finpath_API/bankfinancialratios",
                    "fetched": "ROE 25,3% Q1",
                    "purpose": "validate stance",
                    "supports_argument": "opening",
                }
            ],
            "model": "claude-sonnet-4",
            "duration_ms": 12000,
            "tokens": {"input": 5000, "output": 1200},
            "count": 1,
        }
    }
    db.conn.execute(
        "INSERT INTO generated_news (article_id, row_id, ticker, sector, title, body, "
        "accepted_hypothesis, brief_json, pipeline_log) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            article_id,
            "row-001",
            "ACB",
            "bank",
            "ACB Q1 lãi 5.200 tỷ",
            "Body từ Claude Master.",
            1,
            json.dumps(gn_brief, ensure_ascii=False),
            json.dumps(pipeline_log, ensure_ascii=False),
        ),
    )
    db.conn.commit()


def _mock_factory(payload: dict | None = None, raise_exc: Exception | None = None):
    captured = {}

    def factory(api_key: str):
        client = MagicMock()
        captured["api_key"] = api_key

        def gen(*, model, contents, config):
            captured.setdefault("calls", []).append({"model": model, "contents": contents})
            if raise_exc is not None:
                raise raise_exc
            response = MagicMock()
            response.text = json.dumps(payload) if payload is not None else "{}"
            return response

        client.models.generate_content.side_effect = gen
        return client

    return factory, captured


def test_run_writes_success_columns(db, secrets_with_key, prompt_template) -> None:
    _seed_full_article(db)
    factory, captured = _mock_factory(
        payload={
            "title": "ACB tăng vốn 30% pha loãng nhưng ROE giữ 25%",
            "body": "**ACB** ăn lãi quý 1...",
            "word_count": 250,
        }
    )
    result = run_gemini_writer.run_gemini_writer(
        article_id="art-001",
        db=db,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is True
    assert result["title"].startswith("ACB tăng vốn 30%")

    # DB row populated
    cur = db.conn.execute(
        "SELECT gemini_status, gemini_title, gemini_body, gemini_word_count, "
        "gemini_model, gemini_error FROM generated_news WHERE article_id = ?",
        ("art-001",),
    )
    row = cur.fetchone()
    assert row["gemini_status"] == "success"
    assert row["gemini_title"] == "ACB tăng vốn 30% pha loãng nhưng ROE giữ 25%"
    assert "ăn lãi" in row["gemini_body"]
    assert row["gemini_word_count"] == 250
    assert row["gemini_model"] == "gemini-2.5-pro"
    assert row["gemini_error"] is None

    # Prompt substitution: ticker + format_id + question + raw_news + data_trail all populated
    sent_prompt = captured["calls"][0]["contents"]
    assert "ACB" in sent_prompt
    assert "standard_qa" in sent_prompt
    assert "ACB tăng vốn 30% có pha loãng cổ đông?" in sent_prompt
    assert "bullish" in sent_prompt
    assert "ACB lãi Q1 vượt 5.000 tỷ" in sent_prompt
    assert "Finpath_API/bankfinancialratios" in sent_prompt
    # No unresolved placeholders
    assert "{{ticker}}" not in sent_prompt


def test_run_missing_api_key_writes_skipped_disabled(
    db, secrets_missing_key, prompt_template
) -> None:
    _seed_full_article(db)
    factory, _ = _mock_factory(payload={"title": "x", "body": "y", "word_count": 1})
    result = run_gemini_writer.run_gemini_writer(
        article_id="art-001",
        db=db,
        secrets_path=secrets_missing_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "missing_api_key"

    cur = db.conn.execute(
        "SELECT gemini_status, gemini_error, gemini_body FROM generated_news WHERE article_id = ?",
        ("art-001",),
    )
    row = cur.fetchone()
    assert row["gemini_status"] == "skipped_disabled"
    assert row["gemini_error"] == "missing_api_key"
    assert row["gemini_body"] is None


def test_run_hard_fail_writes_skipped_failure(db, secrets_with_key, prompt_template) -> None:
    _seed_full_article(db)
    factory, _ = _mock_factory(raise_exc=RuntimeError("upstream 503"))
    result = run_gemini_writer.run_gemini_writer(
        article_id="art-001",
        db=db,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is False
    assert "upstream 503" in result["error"]

    cur = db.conn.execute(
        "SELECT gemini_status, gemini_error FROM generated_news WHERE article_id = ?",
        ("art-001",),
    )
    row = cur.fetchone()
    assert row["gemini_status"] == "skipped_failure"
    assert "upstream 503" in row["gemini_error"]


def test_run_article_not_found_returns_error_no_db_write(
    db, secrets_with_key, prompt_template
) -> None:
    factory, _ = _mock_factory(payload={"title": "x", "body": "y", "word_count": 1})
    result = run_gemini_writer.run_gemini_writer(
        article_id="does-not-exist",
        db=db,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "article_not_found"


def test_run_missing_data_trail_still_proceeds(db, secrets_with_key, prompt_template) -> None:
    """Even when Claude Master persisted no data_trail (unusual), Gemini still runs
    with empty array. Pipeline must not block."""
    _seed_full_article(db)
    # Mutate pipeline_log to remove data_trail
    db.conn.execute(
        "UPDATE generated_news SET pipeline_log = ? WHERE article_id = ?",
        (json.dumps({"step_4_master": {"chosen_question_idx": 0}}), "art-001"),
    )
    db.conn.commit()
    factory, captured = _mock_factory(payload={"title": "T", "body": "B", "word_count": 5})
    result = run_gemini_writer.run_gemini_writer(
        article_id="art-001",
        db=db,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is True
    sent_prompt = captured["calls"][0]["contents"]
    assert "[]" in sent_prompt  # empty data_trail JSON
