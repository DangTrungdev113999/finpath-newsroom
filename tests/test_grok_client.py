"""Tests for lib/llm/grok_client.py — xAI Grok wrapper for Step 4.4."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from lib.llm import grok_client


def _write_secrets(tmp_path: Path, key_value: str, model: str | None = None) -> Path:
    secrets = tmp_path / "secrets.yaml"
    body = f"grok:\n  api_key: {key_value!r}\n"
    if model is not None:
        body += f"  model: {model!r}\n"
    secrets.write_text(body, encoding="utf-8")
    return secrets


# ---- load_api_key ----------------------------------------------------------


def test_load_api_key_returns_string(tmp_path: Path) -> None:
    path = _write_secrets(tmp_path, "xai-key-123")
    assert grok_client.load_api_key(path) == "xai-key-123"


def test_load_api_key_missing_file_returns_none(tmp_path: Path) -> None:
    path = tmp_path / "nonexistent.yaml"
    assert grok_client.load_api_key(path) is None


def test_load_api_key_placeholder_returns_none(tmp_path: Path) -> None:
    path = _write_secrets(tmp_path, "REPLACE_WITH_GROK_API_KEY")
    assert grok_client.load_api_key(path) is None


def test_load_api_key_missing_section_returns_none(tmp_path: Path) -> None:
    path = tmp_path / "secrets.yaml"
    path.write_text("telegram:\n  bot_token: x\n", encoding="utf-8")
    assert grok_client.load_api_key(path) is None


# ---- load_model -----------------------------------------------------------


def test_load_model_returns_override(tmp_path: Path) -> None:
    path = _write_secrets(tmp_path, "k", model="grok-4-0709")
    assert grok_client.load_model(path) == "grok-4-0709"


def test_load_model_returns_default_when_missing(tmp_path: Path) -> None:
    path = _write_secrets(tmp_path, "k")
    assert grok_client.load_model(path) == grok_client.DEFAULT_MODEL


def test_load_model_returns_default_when_file_missing(tmp_path: Path) -> None:
    assert grok_client.load_model(tmp_path / "nope.yaml") == grok_client.DEFAULT_MODEL


# ---- generate_article ------------------------------------------------------


def _mock_factory(response_text: str | None = None, raise_exc: Exception | None = None):
    """Build a client factory that records calls and returns scripted responses."""
    captured = {}

    def factory(api_key: str, base_url: str):
        client = MagicMock()
        captured["api_key"] = api_key
        captured["base_url"] = base_url
        if raise_exc is not None:
            client.chat.completions.create.side_effect = raise_exc
        else:
            choice = MagicMock()
            choice.message.content = response_text
            response = MagicMock()
            response.choices = [choice]
            client.chat.completions.create.return_value = response
        return client

    return factory, captured


def test_generate_success_parses_json() -> None:
    payload = {"title": "ACB lãi 5.000 tỷ Q1", "body": "Body text.", "word_count": 50}
    factory, captured = _mock_factory(response_text=json.dumps(payload))
    result = grok_client.generate_article(
        prompt="hi",
        api_key="fake-key",
        _client_factory=factory,
    )
    assert result["ok"] is True
    assert result["title"] == "ACB lãi 5.000 tỷ Q1"
    assert result["body"] == "Body text."
    assert result["word_count"] == 50
    assert result["error"] is None
    assert result["model"] == grok_client.DEFAULT_MODEL
    assert isinstance(result["duration_ms"], int)
    assert captured["base_url"] == "https://api.x.ai/v1"
    assert captured["api_key"] == "fake-key"


def test_generate_missing_api_key_returns_error() -> None:
    result = grok_client.generate_article(
        prompt="hi",
        api_key=None,
        _client_factory=lambda api_key, base_url: MagicMock(),  # never called
    )
    assert result["ok"] is False
    assert result["error"] == "missing_api_key"


def test_generate_invalid_json_returns_parse_error() -> None:
    factory, _ = _mock_factory(response_text="not json {{{")
    result = grok_client.generate_article(
        prompt="hi",
        api_key="fake-key",
        _client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "parse_error"


def test_generate_retry_then_success() -> None:
    """First call raises, second succeeds — retry once → ok=True."""
    payload = {"title": "T", "body": "B", "word_count": 1}
    call_count = {"n": 0}

    def factory(api_key: str, base_url: str):
        client = MagicMock()

        def side_effect(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise TimeoutError("first attempt timed out")
            choice = MagicMock()
            choice.message.content = json.dumps(payload)
            response = MagicMock()
            response.choices = [choice]
            return response

        client.chat.completions.create.side_effect = side_effect
        return client

    result = grok_client.generate_article(
        prompt="hi",
        api_key="fake-key",
        _client_factory=factory,
    )
    assert result["ok"] is True
    assert result["title"] == "T"
    assert call_count["n"] == 2


def test_generate_hard_fail_after_retry() -> None:
    """Both attempts fail → ok=False, error reflects last exception."""
    factory, _ = _mock_factory(raise_exc=RuntimeError("server boom"))
    result = grok_client.generate_article(
        prompt="hi",
        api_key="fake-key",
        _client_factory=factory,
    )
    assert result["ok"] is False
    assert "server boom" in result["error"]


def test_generate_missing_required_fields_returns_parse_error() -> None:
    """JSON parses but missing title or body → parse_error."""
    factory, _ = _mock_factory(response_text=json.dumps({"title": "x"}))  # body missing
    result = grok_client.generate_article(
        prompt="hi",
        api_key="fake-key",
        _client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "parse_error"


def test_generate_empty_choices_returns_error() -> None:
    """response.choices = [] → caller error reported, not parse_error."""

    def factory(api_key: str, base_url: str):
        client = MagicMock()
        response = MagicMock()
        response.choices = []
        client.chat.completions.create.return_value = response
        return client

    result = grok_client.generate_article(
        prompt="hi",
        api_key="fake-key",
        _client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] is not None


def test_generate_uses_custom_model() -> None:
    payload = {"title": "T", "body": "B", "word_count": 1}
    captured = {}

    def factory(api_key: str, base_url: str):
        client = MagicMock()

        def side_effect(*, model, **kwargs):
            captured["model"] = model
            choice = MagicMock()
            choice.message.content = json.dumps(payload)
            response = MagicMock()
            response.choices = [choice]
            return response

        client.chat.completions.create.side_effect = side_effect
        return client

    grok_client.generate_article(
        prompt="hi",
        api_key="fake-key",
        model="grok-4-0709",
        _client_factory=factory,
    )
    assert captured["model"] == "grok-4-0709"
