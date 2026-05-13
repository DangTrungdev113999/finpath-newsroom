"""Tests for lib/llm/gemini_client.py — Gemini wrapper for Step 4.3."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from lib.llm import gemini_client


def _write_secrets(tmp_path: Path, key_value: str) -> Path:
    secrets = tmp_path / "secrets.yaml"
    secrets.write_text(
        f"gemini:\n  api_key: {key_value!r}\n",
        encoding="utf-8",
    )
    return secrets


def test_load_api_key_returns_string(tmp_path: Path) -> None:
    path = _write_secrets(tmp_path, "real-key-123")
    assert gemini_client.load_api_key(path) == "real-key-123"


def test_load_api_key_missing_file_returns_none(tmp_path: Path) -> None:
    path = tmp_path / "nonexistent.yaml"
    assert gemini_client.load_api_key(path) is None


def test_load_api_key_placeholder_returns_none(tmp_path: Path) -> None:
    path = _write_secrets(tmp_path, "REPLACE_WITH_GEMINI_API_KEY")
    assert gemini_client.load_api_key(path) is None


def test_load_api_key_missing_section_returns_none(tmp_path: Path) -> None:
    path = tmp_path / "secrets.yaml"
    path.write_text("telegram:\n  bot_token: x\n", encoding="utf-8")
    assert gemini_client.load_api_key(path) is None


def _mock_factory(response_text: str | None = None, raise_exc: Exception | None = None):
    """Build a client factory that records calls and returns scripted responses."""
    factory_mock = MagicMock()

    def factory(api_key: str):
        client = MagicMock()
        factory_mock(api_key=api_key)
        if raise_exc is not None:
            client.models.generate_content.side_effect = raise_exc
        else:
            response = MagicMock()
            response.text = response_text
            client.models.generate_content.return_value = response
        return client

    return factory, factory_mock


def test_generate_success_parses_json() -> None:
    payload = {"title": "ACB lãi 5.000 tỷ Q1", "body": "Body text.", "word_count": 50}
    factory, _ = _mock_factory(response_text=json.dumps(payload))
    result = gemini_client.generate_article(
        prompt="hi",
        api_key="fake-key",
        _client_factory=factory,
    )
    assert result["ok"] is True
    assert result["title"] == "ACB lãi 5.000 tỷ Q1"
    assert result["body"] == "Body text."
    assert result["word_count"] == 50
    assert result["error"] is None
    assert result["model"] == "gemini-2.5-pro"
    assert isinstance(result["duration_ms"], int)


def test_generate_missing_api_key_returns_error() -> None:
    result = gemini_client.generate_article(
        prompt="hi",
        api_key=None,
        _client_factory=lambda key: MagicMock(),  # never called
    )
    assert result["ok"] is False
    assert result["error"] == "missing_api_key"


def test_generate_invalid_json_returns_parse_error() -> None:
    factory, _ = _mock_factory(response_text="not json {{{")
    result = gemini_client.generate_article(
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

    def factory(api_key: str):
        client = MagicMock()

        def side_effect(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise TimeoutError("first attempt timed out")
            response = MagicMock()
            response.text = json.dumps(payload)
            return response

        client.models.generate_content.side_effect = side_effect
        return client

    result = gemini_client.generate_article(
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
    result = gemini_client.generate_article(
        prompt="hi",
        api_key="fake-key",
        _client_factory=factory,
    )
    assert result["ok"] is False
    assert "server boom" in result["error"]


def test_generate_missing_required_fields_returns_parse_error() -> None:
    """JSON parses but missing title or body → parse_error."""
    factory, _ = _mock_factory(response_text=json.dumps({"title": "x"}))  # body missing
    result = gemini_client.generate_article(
        prompt="hi",
        api_key="fake-key",
        _client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "parse_error"
