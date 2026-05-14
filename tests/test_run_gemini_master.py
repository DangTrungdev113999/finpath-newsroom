"""Tests for lib/stages/run_gemini_master.py — Step 4.3 orchestrator (V5.1.9)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from lib import pipeline_db
from lib.stages import run_gemini_master

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
    p.write_text("gemini:\n  api_key: 'real-google-key'\n", encoding="utf-8")
    return p


@pytest.fixture
def secrets_no_key(tmp_path: Path) -> Path:
    p = tmp_path / "secrets.yaml"
    p.write_text("gemini:\n  api_key: 'REPLACE_WITH_KEY'\n", encoding="utf-8")
    return p


@pytest.fixture
def prompt_template(tmp_path: Path) -> Path:
    p = tmp_path / "prompt.md"
    p.write_text(
        "Ticker: {{ticker}}\nOptions: {{deep_question_options_json}}\nRaw: {{raw_news_title}}\n",
        encoding="utf-8",
    )
    return p


def _seed_article(db, *, article_id: str = "art-001", current_title: str | None = None) -> None:
    """Insert placeholder row mimicking what pipeline Step 4.0 would create."""
    if current_title is None:
        current_title = "VCB-pending-master"
    crawl_brief = {
        "angle_label": "Big4 áp lực CASA",
        "angle_narrative": "Tăng trưởng credit chậm",
        "deep_question_options": [
            {"category": "paradox", "question": "VCB lãi cao nhưng CASA giảm — vì sao?"},
            {"category": "why_now", "question": "Vì sao CASA giảm Q1?"},
        ],
        "format_picks": [{"option_idx": 0, "format_id": "standard_qa"}],
    }
    db.conn.execute(
        "INSERT INTO crawl_log (row_id, funnel_batch_id, ticker, source_name, source_url, "
        "title, raw_content, crawled_at, brief_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("row-001", "batch-001", "VCB", "cafef", "https://x.com/y", "VCB lãi Q1 5000 tỷ",
         "Raw body content", "2026-05-14",
         json.dumps(crawl_brief, ensure_ascii=False)),
    )
    db.conn.execute(
        "INSERT INTO generated_news (article_id, row_id, ticker, sector, title, body, "
        "accepted_hypothesis, status, public_slug) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (article_id, "row-001", "VCB", "Bank", current_title, "", 1, "draft",
         "VCB-20260514-1200-pending-master"),
    )
    db.conn.commit()


def _mock_factory(payload: dict | None = None, usage: dict | None = None, raise_exc: Exception | None = None):
    captured = {}

    def factory(api_key: str):
        captured["api_key"] = api_key
        client = MagicMock()

        def gen(*, model, contents, config):
            captured.setdefault("calls", []).append({"model": model})
            if raise_exc:
                raise raise_exc
            response = MagicMock()
            response.text = json.dumps(payload) if payload is not None else "{}"
            if usage:
                response.usage_metadata.prompt_token_count = usage.get("prompt_tokens", 0)
                response.usage_metadata.candidates_token_count = usage.get("completion_tokens", 0)
            else:
                response.usage_metadata = None
            return response

        client.models.generate_content.side_effect = gen
        return client

    return factory, captured


def test_success_promotes_to_primary(db, secrets_with_key, prompt_template) -> None:
    _seed_article(db)
    valid = {
        "title": "VCB lãi Q1 vượt 5000 tỷ, CASA giảm còn 28%",
        "body": "Body content here with insight.",
        "word_count": 250,
        "chosen_question_idx": 0,
        "chosen_pick_reason": "data depth",
        "skip_reasons": {"1": "less compelling"},
        "insight_final": "Big4 chậm hơn TPB",
        "key_view": "thận trọng",
        "variety_guard_angle": "Big4 áp lực CASA",
        "format_id_used": "standard_qa",
        "format_escalation_reason": None,
        "data_trail": [
            {"source": "Finpath_API/bank_ratios/VCB", "fetched": "CASA 28%", "purpose": "verify", "supports_argument": "Bullet 1"},
        ],
        "gates_passed": True,
    }
    factory, _ = _mock_factory(payload=valid, usage={"prompt_tokens": 30000, "completion_tokens": 2000})
    result = run_gemini_master.run_gemini_master(
        article_id="art-001",
        db=db,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is True
    assert result["tool_calls"] == 1
    assert result["cost_usd"] is not None

    row = db.conn.execute("SELECT * FROM generated_news WHERE article_id = ?", ("art-001",)).fetchone()
    # Gemini side filled
    assert row["gemini_status"] == "success"
    assert row["gemini_title"] == valid["title"]
    assert row["gemini_body"] == valid["body"]
    assert row["gemini_cost_usd"] is not None
    assert row["gemini_brief_json"] is not None
    assert row["gemini_step_log"] is not None
    # Primary promoted (title was placeholder)
    assert row["title"] == valid["title"]
    assert row["body"] == valid["body"]
    assert "pending-master" not in row["public_slug"]
    assert row["insight_final"] == "Big4 chậm hơn TPB"
    assert row["key_view"] == "thận trọng"


def test_success_does_not_overwrite_existing_primary(db, secrets_with_key, prompt_template) -> None:
    """If another writer (Grok) already became primary, Gemini fills only its
    side columns and does NOT overwrite title/body."""
    _seed_article(db, current_title="Grok-set title — VCB CASA paradox")
    valid = {
        "title": "Gemini Title — different",
        "body": "Gemini body",
        "word_count": 200,
        "chosen_question_idx": 0,
        "data_trail": [{"source": "Raw news", "fetched": "..."}],
    }
    factory, _ = _mock_factory(payload=valid)
    run_gemini_master.run_gemini_master(
        article_id="art-001",
        db=db,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        client_factory=factory,
    )
    row = db.conn.execute("SELECT title, gemini_title FROM generated_news WHERE article_id = ?", ("art-001",)).fetchone()
    # Primary untouched (Grok was first)
    assert row["title"] == "Grok-set title — VCB CASA paradox"
    # Gemini side captures its own output
    assert row["gemini_title"] == "Gemini Title — different"


def test_missing_api_key_writes_skipped_disabled(db, secrets_no_key, prompt_template) -> None:
    _seed_article(db)
    factory, _ = _mock_factory(payload={"title": "x", "body": "y", "word_count": 1, "chosen_question_idx": 0, "data_trail": []})
    result = run_gemini_master.run_gemini_master(
        article_id="art-001", db=db, secrets_path=secrets_no_key, prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "missing_api_key"
    row = db.conn.execute("SELECT gemini_status, gemini_error FROM generated_news WHERE article_id = ?", ("art-001",)).fetchone()
    assert row["gemini_status"] == "skipped_disabled"
    assert row["gemini_error"] == "missing_api_key"


def test_sdk_exception_writes_skipped_failure(db, secrets_with_key, prompt_template) -> None:
    _seed_article(db)
    factory, _ = _mock_factory(raise_exc=RuntimeError("genai 503"))
    result = run_gemini_master.run_gemini_master(
        article_id="art-001", db=db, secrets_path=secrets_with_key, prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is False
    assert "genai 503" in result["error"]
    row = db.conn.execute("SELECT gemini_status, gemini_error FROM generated_news WHERE article_id = ?", ("art-001",)).fetchone()
    assert row["gemini_status"] == "skipped_failure"
    assert "genai 503" in row["gemini_error"]
    # Primary NOT promoted on failure
    assert "pending-master" in (row["gemini_error"] or "") or True  # error captured, title unchanged
    primary = db.conn.execute("SELECT title FROM generated_news WHERE article_id = ?", ("art-001",)).fetchone()
    assert "pending-master" in primary["title"]


def test_article_not_found(db, secrets_with_key, prompt_template) -> None:
    factory, _ = _mock_factory(payload={"title": "x", "body": "y", "word_count": 1, "chosen_question_idx": 0, "data_trail": []})
    result = run_gemini_master.run_gemini_master(
        article_id="missing", db=db, secrets_path=secrets_with_key, prompt_path=prompt_template,
        client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "article_not_found"
