"""Tests for lib.telegram_publisher — Telegram Bot API push (Phase G T12)."""
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
import pytest

from lib.telegram_publisher import TelegramPublisher, load_telegram_config


def test_publisher_init():
    p = TelegramPublisher("token123", "chat-1", "http://localhost:5174/")
    assert p.bot_token == "token123"
    assert p.chat_id == "chat-1"
    assert p.base_url == "http://localhost:5174"  # trailing slash stripped


def test_publisher_html_escape():
    """Title containing < > & must be HTML-escaped to avoid Telegram parse_mode=HTML breakage."""
    assert TelegramPublisher._escape_html("A & B <div>") == "A &amp; B &lt;div&gt;"
    assert TelegramPublisher._escape_html("Plain text") == "Plain text"


def test_publisher_push_success():
    """Mock urlopen returns ok=True → status=pushed + message_id."""
    p = TelegramPublisher("t", "c", "http://localhost:5174")
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "ok": True,
        "result": {"message_id": 42},
    }).encode("utf-8")
    mock_resp.__enter__ = lambda self: self
    mock_resp.__exit__ = lambda *args: None

    with patch("lib.telegram_publisher.urllib.request.urlopen", return_value=mock_resp):
        result = p.publish_article("Test title", "test-slug")
    assert result == {"status": "pushed", "telegram_message_id": 42, "error": None}


def test_publisher_push_telegram_returns_error():
    """Mock urlopen returns ok=False → status=failed + error message."""
    p = TelegramPublisher("t", "c", "http://localhost:5174")
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "ok": False,
        "description": "Bad chat_id",
    }).encode("utf-8")
    mock_resp.__enter__ = lambda self: self
    mock_resp.__exit__ = lambda *args: None

    with patch("lib.telegram_publisher.urllib.request.urlopen", return_value=mock_resp):
        result = p.publish_article("T", "s")
    assert result["status"] == "failed"
    assert result["telegram_message_id"] is None
    assert "Bad chat_id" in result["error"]


def test_publisher_push_network_exception():
    """urlopen raises → caught, status=failed + exception str."""
    p = TelegramPublisher("t", "c", "http://localhost:5174")
    with patch("lib.telegram_publisher.urllib.request.urlopen", side_effect=ConnectionError("dns fail")):
        result = p.publish_article("T", "s")
    assert result["status"] == "failed"
    assert "dns fail" in result["error"]


def test_load_config_missing_file_returns_none(tmp_path):
    assert load_telegram_config(tmp_path / "no.yaml") is None


def test_load_config_missing_telegram_section_returns_none(tmp_path):
    p = tmp_path / "secrets.yaml"
    p.write_text("other: value\n")
    assert load_telegram_config(p) is None


def test_load_config_partial_telegram_returns_none(tmp_path):
    p = tmp_path / "secrets.yaml"
    p.write_text("telegram:\n  bot_token: t\n")  # missing chat_id + base_url
    assert load_telegram_config(p) is None


def test_load_config_full_returns_publisher(tmp_path):
    p = tmp_path / "secrets.yaml"
    p.write_text("telegram:\n  bot_token: tk\n  chat_id: c1\n  base_url: http://x\n")
    pub = load_telegram_config(p)
    assert pub is not None
    assert pub.bot_token == "tk"
    assert pub.chat_id == "c1"
    assert pub.base_url == "http://x"
