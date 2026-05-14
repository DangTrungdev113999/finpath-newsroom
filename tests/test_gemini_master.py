"""Tests for lib/llm/gemini_master.py — Gemini Master with tool access."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from lib.llm import gemini_master, research_tools


def _build_tools(db=None):
    return research_tools.build_research_tools(
        db=db or MagicMock(),
        secrets_path=Path("/nonexistent"),
    )


def _mock_factory(response_text: str = "{}", usage_meta: dict | None = None,
                  raise_exc: Exception | None = None):
    captured: dict = {}

    def factory(api_key: str):
        captured["api_key"] = api_key
        client = MagicMock()

        def gen(*, model, contents, config):
            captured.setdefault("calls", []).append({"model": model, "contents": contents})
            if raise_exc:
                raise raise_exc
            response = MagicMock()
            response.text = response_text
            if usage_meta is not None:
                response.usage_metadata.prompt_token_count = usage_meta.get("prompt_tokens", 0)
                response.usage_metadata.candidates_token_count = usage_meta.get("completion_tokens", 0)
            else:
                response.usage_metadata = None
            return response

        client.models.generate_content.side_effect = gen
        return client

    return factory, captured


def test_generate_article_success_returns_payload():
    valid_output = {
        "title": "SHB lãi Q1 vượt 4656 tỷ",
        "body": "Body here",
        "word_count": 250,
        "chosen_question_idx": 0,
        "chosen_pick_reason": "data depth",
        "skip_reasons": {"1": "thin"},
        "insight_final": "Big4 áp lực",
        "key_view": "thận trọng",
        "variety_guard_angle": "paradox",
        "format_id_used": "standard_qa",
        "format_escalation_reason": None,
        "data_trail": [{"source": "Finpath_API/income_statement", "fetched": "Q1 4656 tỷ"}],
        "gates_passed": True,
    }
    factory, captured = _mock_factory(
        response_text=json.dumps(valid_output),
        usage_meta={"prompt_tokens": 50000, "completion_tokens": 2000},
    )
    result = gemini_master.generate_article(
        prompt="test prompt",
        tools=_build_tools(),
        api_key="real-key",
        _client_factory=factory,
    )
    assert result["ok"] is True
    assert result["payload"]["title"] == "SHB lãi Q1 vượt 4656 tỷ"
    assert result["payload"]["data_trail"][0]["source"] == "Finpath_API/income_statement"
    assert result["usage"]["prompt_tokens"] == 50000


def test_missing_api_key_returns_error_no_call():
    factory, captured = _mock_factory()
    result = gemini_master.generate_article(
        prompt="x", tools=_build_tools(), api_key=None, _client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "missing_api_key"
    assert "calls" not in captured


def test_sdk_exception_returns_error():
    factory, _ = _mock_factory(raise_exc=RuntimeError("genai timeout"))
    result = gemini_master.generate_article(
        prompt="x", tools=_build_tools(), api_key="k", _client_factory=factory,
    )
    assert result["ok"] is False
    assert "genai timeout" in result["error"]


def test_parse_error_when_response_not_json():
    factory, _ = _mock_factory(response_text="not json at all")
    result = gemini_master.generate_article(
        prompt="x", tools=_build_tools(), api_key="k", _client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "parse_error"


def test_missing_required_fields_returns_error():
    """Response is valid JSON but missing title/body — caller knows to skip."""
    factory, _ = _mock_factory(response_text=json.dumps({"foo": "bar"}))
    result = gemini_master.generate_article(
        prompt="x", tools=_build_tools(), api_key="k", _client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "missing_required_fields"
