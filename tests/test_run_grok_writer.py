"""Tests for lib/stages/run_grok_writer.py — Step 4.4 orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from lib import pipeline_db
from lib.stages import run_grok_writer

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
    p.write_text("grok:\n  api_key: 'real-key'\n", encoding="utf-8")
    return p


@pytest.fixture
def secrets_missing_key(tmp_path: Path) -> Path:
    p = tmp_path / "secrets.yaml"
    p.write_text("grok:\n  api_key: 'REPLACE_WITH_GROK_API_KEY'\n", encoding="utf-8")
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
            "2026-05-14",
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
    """Factory signature mirrors grok_client._default_factory: (api_key, base_url)."""
    captured: dict = {}

    def factory(api_key: str, base_url: str):
        client = MagicMock()
        captured["api_key"] = api_key
        captured["base_url"] = base_url

        def gen(*, model, messages, response_format, timeout, **_):
            captured.setdefault("calls", []).append({
                "model": model,
                "messages": messages,
                "response_format": response_format,
            })
            if raise_exc is not None:
                raise raise_exc
            choice = MagicMock()
            choice.message.content = json.dumps(payload) if payload is not None else "{}"
            response = MagicMock()
            response.choices = [choice]
            return response

        client.chat.completions.create.side_effect = gen
        return client

    return factory, captured


def test_run_writes_success_columns(db, secrets_with_key, prompt_template) -> None:
    _seed_full_article(db)
    factory, captured = _mock_factory(
        payload={
            "title": "Grok title cho ACB",
            "body": "**ACB** ăn lãi quý 1...",
            "word_count": 250,
        }
    )
    result = run_grok_writer.run_grok_writer(
        article_id="art-001",
        db=db,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is True
    assert result["title"] == "Grok title cho ACB"

    cur = db.conn.execute(
        "SELECT grok_status, grok_title, grok_body, grok_word_count, "
        "grok_model, grok_error FROM generated_news WHERE article_id = ?",
        ("art-001",),
    )
    row = cur.fetchone()
    assert row["grok_status"] == "success"
    assert row["grok_title"] == "Grok title cho ACB"
    assert "ăn lãi" in row["grok_body"]
    assert row["grok_word_count"] == 250
    assert row["grok_model"] == "grok-4.3"
    assert row["grok_error"] is None

    sent_prompt = captured["calls"][0]["messages"][0]["content"]
    assert "ACB" in sent_prompt
    assert "standard_qa" in sent_prompt
    assert "ACB tăng vốn 30% có pha loãng cổ đông?" in sent_prompt
    assert "bullish" in sent_prompt
    assert "ACB lãi Q1 vượt 5.000 tỷ" in sent_prompt
    assert "Finpath_API/bankfinancialratios" in sent_prompt
    assert "{{ticker}}" not in sent_prompt
    # JSON mode requested
    assert captured["calls"][0]["response_format"] == {"type": "json_object"}


def test_run_missing_api_key_writes_skipped_disabled(
    db, secrets_missing_key, prompt_template
) -> None:
    _seed_full_article(db)
    factory, _ = _mock_factory(payload={"title": "x", "body": "y", "word_count": 1})
    result = run_grok_writer.run_grok_writer(
        article_id="art-001",
        db=db,
        secrets_path=secrets_missing_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "missing_api_key"

    cur = db.conn.execute(
        "SELECT grok_status, grok_error, grok_body FROM generated_news WHERE article_id = ?",
        ("art-001",),
    )
    row = cur.fetchone()
    assert row["grok_status"] == "skipped_disabled"
    assert row["grok_error"] == "missing_api_key"
    assert row["grok_body"] is None


def test_run_hard_fail_writes_skipped_failure(db, secrets_with_key, prompt_template) -> None:
    _seed_full_article(db)
    factory, _ = _mock_factory(raise_exc=RuntimeError("upstream 503"))
    result = run_grok_writer.run_grok_writer(
        article_id="art-001",
        db=db,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is False
    assert "upstream 503" in result["error"]

    cur = db.conn.execute(
        "SELECT grok_status, grok_error FROM generated_news WHERE article_id = ?",
        ("art-001",),
    )
    row = cur.fetchone()
    assert row["grok_status"] == "skipped_failure"
    assert "upstream 503" in row["grok_error"]


def test_run_article_not_found_returns_error_no_db_write(
    db, secrets_with_key, prompt_template
) -> None:
    factory, _ = _mock_factory(payload={"title": "x", "body": "y", "word_count": 1})
    result = run_grok_writer.run_grok_writer(
        article_id="does-not-exist",
        db=db,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "article_not_found"


def test_run_model_override_overrides_secrets_default(db, secrets_with_key, prompt_template) -> None:
    """Explicit `model` arg wins over secrets.grok.model + DEFAULT_MODEL."""
    _seed_full_article(db)
    factory, captured = _mock_factory(payload={"title": "T", "body": "B", "word_count": 5})
    run_grok_writer.run_grok_writer(
        article_id="art-001",
        db=db,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        model="grok-4-0709",
        client_factory=factory,
    )
    assert captured["calls"][0]["model"] == "grok-4-0709"
